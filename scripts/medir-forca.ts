/*
 * Mede a força real de cada personagem e quanto cada ligação de sinergia vale
 * na luta, para a campanha escolher rivais cada vez mais fortes e mais
 * entrosados (src/engine/campaign.ts).
 *
 * 1. Simula lutas de trios sorteados contra trios sorteados (os dois lados
 *    com a Vida normal).
 * 2. Ajusta um modelo de "quem ganha": a chance de o trio A vencer cresce com
 *    (soma das forças de A − soma das forças de B) + (sinergia de A − de B),
 *    onde a sinergia é a soma das ligações de src/engine/sinergia.ts, cada
 *    uma com o seu peso. Uma ligação que não ajuda fica com peso zero.
 *
 * Uso:
 *   npx tsx scripts/medir-forca.ts simular <parte> <lutas> <arquivo.jsonl>   (rode várias partes em paralelo)
 *   npx tsx scripts/medir-forca.ts ajustar <arquivo.jsonl>...               (escreve src/data/forca-dos-rivais.ts)
 */
import { appendFileSync, readFileSync, writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { LIGACOES, ligacoesDoTrio } from '../src/engine/sinergia';

const ids = characters.map((c) => c.id);
const [modo, ...args] = process.argv.slice(2);

if (modo === 'simular') {
  const parte = Number(args[0]), lutas = Number(args[1]), saida = args[2]!;
  let r = (parte * 2654435761 + 97) >>> 0;
  const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
  let buffer = '';
  for (let n = 0; n < lutas; n++) {
    const seis = new Set<string>();
    while (seis.size < 6) seis.add(ids[Math.floor(rnd() * ids.length)]!);
    const [a1, a2, a3, b1, b2, b3] = [...seis];
    const a = [a1!, a2!, a3!], b = [b1!, b2!, b3!];
    const batalha = createBattle(a, b, Math.floor(rnd() * 2 ** 31), 1);
    for (let t = 0; t < 9000 && !batalha.finished; t++) stepBattle(batalha);
    if (!batalha.finished) continue;
    buffer += JSON.stringify([a, b, batalha.winner === 'player' ? 1 : 0]) + '\n';
    if (n % 500 === 499) { appendFileSync(saida, buffer); buffer = ''; }
  }
  appendFileSync(saida, buffer);
} else if (modo === 'ajustar') {
  const lutas: [string[], string[], number][] = args.flatMap((f) => readFileSync(f, 'utf8').split('\n').filter(Boolean).map((l) => JSON.parse(l)));
  const idx = new Map(ids.map((id, i) => [id, i]));
  const K = LIGACOES.length;
  const linhas = lutas.map(([a, b, y]) => {
    const la = ligacoesDoTrio(a), lb = ligacoesDoTrio(b);
    return { a: a.map((x) => idx.get(x)!), b: b.map((x) => idx.get(x)!), d: LIGACOES.map((l) => la[l] - lb[l]), y };
  });
  // regressão logística por descida de gradiente (Adam), com um pouco de regularização
  const F = new Float64Array(ids.length), W = new Float64Array(K);
  let lado = 0;
  const p = new Float64Array(ids.length + K + 1), m1 = new Float64Array(p.length), m2 = new Float64Array(p.length);
  const L2 = 0.002, taxa = 0.03;
  for (let it = 1; it <= 600; it++) {
    const g = new Float64Array(p.length);
    for (const l of linhas) {
      let z = lado;
      for (const i of l.a) z += F[i]!;
      for (const i of l.b) z -= F[i]!;
      for (let k = 0; k < K; k++) z += W[k]! * l.d[k]!;
      const e = 1 / (1 + Math.exp(-z)) - l.y;
      for (const i of l.a) g[i]! += e;
      for (const i of l.b) g[i]! -= e;
      for (let k = 0; k < K; k++) g[ids.length + k]! += e * l.d[k]!;
      g[ids.length + K]! += e;
    }
    for (let j = 0; j < p.length; j++) {
      const atual = j < ids.length ? F[j]! : j < ids.length + K ? W[j - ids.length]! : lado;
      const gj = g[j]! / linhas.length + L2 * atual;
      m1[j] = 0.9 * m1[j]! + 0.1 * gj; m2[j] = 0.999 * m2[j]! + 0.001 * gj * gj;
      const passo = taxa * (m1[j]! / (1 - 0.9 ** it)) / (Math.sqrt(m2[j]! / (1 - 0.999 ** it)) + 1e-8);
      if (j < ids.length) F[j] = atual - passo; else if (j < ids.length + K) W[j - ids.length] = Math.max(0, atual - passo); else lado = atual - passo;
    }
  }
  // força centrada em zero
  const media = F.reduce((n, x) => n + x, 0) / F.length;
  for (let i = 0; i < F.length; i++) F[i] = F[i]! - media;
  let acertos = 0;
  for (const l of linhas) {
    let z = lado; for (const i of l.a) z += F[i]!; for (const i of l.b) z -= F[i]!; for (let k = 0; k < K; k++) z += W[k]! * l.d[k]!;
    if ((z > 0 ? 1 : 0) === l.y) acertos++;
  }
  const forca = ids.map((id, i) => [id, Math.round(F[i]! * 1000) / 1000] as const).sort(([a], [b]) => a.localeCompare(b));
  const pesos = LIGACOES.map((l, k) => [l, Math.round(W[k]! * 1000) / 1000] as const);
  writeFileSync(new URL('../src/data/forca-dos-rivais.ts', import.meta.url), `/*
 * Força de cada personagem e peso de cada ligação de sinergia, medidos em
 * ${linhas.length} lutas simuladas (trios sorteados contra trios sorteados) por
 * scripts/medir-forca.ts. O modelo acerta o vencedor em ${Math.round(100 * acertos / linhas.length)}% das lutas.
 * Escala: diferença de 1 entre dois trios ≈ 73% de chance para o mais forte.
 * Não editar à mão: rode o script de novo depois de mudar o elenco.
 */
export const FORCA: Record<string, number> = {
${forca.map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n')}
};

/** Quanto cada ligação (src/engine/sinergia.ts) soma à força do trio, cada vez que aparece. */
export const PESO_DA_LIGACAO: Record<string, number> = {
${pesos.map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n')}
};
`);
  console.log('lutas', linhas.length, 'acerto', (100 * acertos / linhas.length).toFixed(1) + '%', 'lado', lado.toFixed(3));
  console.log('pesos', Object.fromEntries(pesos));
  const o = [...forca].sort((a, b) => b[1] - a[1]);
  console.log('mais fortes', o.slice(0, 8), 'mais fracos', o.slice(-5));
} else {
  console.error('uso: simular <parte> <lutas> <saida> | ajustar <arquivos...>');
  process.exit(1);
}
