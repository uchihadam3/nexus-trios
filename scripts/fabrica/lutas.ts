/*
 * Fábrica de simulação: lutas em lote, para medir força solo, de dupla e de
 * trio com milhões de lutas (.github/workflows/fabrica.yml roda 20 máquinas
 * × 4 processos em paralelo).
 *
 * É o motor do jogo, sem tirar nada: a CI empacota este arquivo com esbuild
 * (sem o ajudante __name do tsx, ~1,4× mais rápido) e o resultado de cada
 * luta é o mesmo de simulate().
 *
 * Uso: node lutas.mjs <plano> <parte> <partes> <lutas> <saida.txt> [semente]
 *   aleatorio  trio aleatório contra trio aleatório
 *   pares      cada dupla possível (79.800 com 400) com um terceiro aleatório,
 *              contra um trio aleatório; as duplas são divididas entre as partes
 *   jornada    trio aleatório jogando a jornada inteira (10 lutas, como o jogador)
 *   dificuldade  para cada personagem da parte, <lutas> jornadas com parceiros
 *              aleatórios, com o trio que um jogador bom montaria e com o melhor
 *              trio achado entre os mais fortes (as metas de equilíbrio)
 *
 * Cada linha (lutas): a1 a2 a3 b1 b2 b3 v (índices do elenco; v = 1 se o trio a venceu).
 * Cada linha (jornada): a1 a2 a3 v (v = lutas vencidas, 0 a 10).
 * Cada linha (dificuldade): JSON {id, aleatorio, bom, melhor, dupla}.
 * A primeira linha (# ...) diz o motor e o elenco, para não misturar medidas.
 */
import { writeFileSync, appendFileSync } from 'node:fs';
import { characters } from '../../src/data/characters';
import { createBattle, stepBattle } from '../../src/engine/battle';
import { ENGINE_VERSION, rosterFingerprint } from '../../src/engine/ranked';
import { forcaDoTrio, generateCampaign, newDraft, pickDraft, skipDraft } from '../../src/engine/campaign';
import { combosDoTrio } from '../../src/engine/combos';
import { FORCA } from '../../src/data/forca-dos-rivais';

const [plano, parteTxt, partesTxt, lutasTxt, saida, sementeTxt = '0'] = process.argv.slice(2);
const parte = Number(parteTxt), partes = Number(partesTxt), lutas = Number(lutasTxt), semente = Number(sementeTxt), semente0 = semente;
if (!plano || !saida || !(partes > 0) || !(parte >= 0 && parte < partes) || !(lutas > 0)) {
  console.error('uso: lutas <aleatorio|pares|jornada|dificuldade> <parte> <partes> <lutas> <saida.txt> [semente]');
  process.exit(1);
}
const N = characters.length;
let r = (Math.imul(parte + 1, 2654435761) ^ Math.imul(semente + 7, 40503) ^ (plano === 'pares' ? 0x9e3779b9 : 0)) >>> 0;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
const sorteia = (fora: Set<number>) => { let i: number; do i = Math.floor(rnd() * N); while (fora.has(i)); fora.add(i); return i; };

/* As duplas desta parte (pares): a k-ésima dupla da lista vai para a parte k % partes. */
const duplas: [number, number][] = [];
if (plano === 'pares') { let k = 0; for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++, k++) if (k % partes === parte) duplas.push([i, j]); }
else if (!['aleatorio', 'jornada', 'dificuldade'].includes(plano)) { console.error(`plano desconhecido: ${plano}`); process.exit(1); }

writeFileSync(saida, `# motor ${ENGINE_VERSION} elenco ${rosterFingerprint()} plano ${plano} parte ${parte}/${partes} semente ${semente}\n`);
if (plano === 'jornada' || plano === 'dificuldade') { (plano === 'jornada' ? jornadas : dificuldade)(); process.exit(0); }
let buffer = '', feitas = 0;
const inicio = Date.now();
for (let n = 0; n < lutas; n++) {
  const usados = new Set<number>();
  let a: number[];
  if (plano === 'pares') { const [x, y] = duplas[n % duplas.length]!; usados.add(x); usados.add(y); a = [x, y, sorteia(usados)]; }
  else a = [sorteia(usados), sorteia(usados), sorteia(usados)];
  const b = [sorteia(usados), sorteia(usados), sorteia(usados)];
  const batalha = createBattle(a.map((i) => characters[i]!.id), b.map((i) => characters[i]!.id), Math.floor(rnd() * 2 ** 31), 1);
  for (let t = 0; t < 9000 && !batalha.finished; t++) stepBattle(batalha);
  if (!batalha.finished) continue;
  buffer += `${a.join(' ')} ${b.join(' ')} ${batalha.winner === 'player' ? 1 : 0}\n`;
  if (++feitas % 1000 === 0) { appendFileSync(saida, buffer); buffer = ''; }
  if (n % 5000 === 4999) console.log(`parte ${parte}: ${n + 1}/${lutas} lutas · ${((n + 1) / ((Date.now() - inicio) / 1000)).toFixed(0)}/s`);
}
appendFileSync(saida, buffer);
console.log(`parte ${parte}: pronto, ${feitas} lutas em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);

/* A jornada inteira, como o jogador joga: quantas das 10 lutas o trio vence. */
function jornada(team: string[], seed: number) {
  for (const [i, e] of generateCampaign(seed, team).entries()) {
    const b = createBattle(team, e.team, seed + i * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner !== 'player') return i;
  }
  return 10;
}
function jornadas() {
  let buf = '';
  for (let n = 0; n < lutas; n++) {
    const usados = new Set<number>(), a = [sorteia(usados), sorteia(usados), sorteia(usados)];
    buf += `${a.join(' ')} ${jornada(a.map((i) => characters[i]!.id), Math.floor(rnd() * 2 ** 31))}\n`;
    if (n % 200 === 199) { appendFileSync(saida, buf); buf = ''; console.log(`parte ${parte}: ${n + 1}/${lutas} jornadas`); }
  }
  appendFileSync(saida, buf);
}
/*
 * As metas de equilíbrio por personagem (pedido do jogador: aleatório 0,5–9,9%, bom 10–35%, melhor 15–70%):
 *   aleatório — X com dois parceiros sorteados;
 *   bom — o trio que um jogador bom montaria em volta de X na escolha (pela nota, procurando combo);
 *   melhor — dos mais fortes (FORTES, medidos nas jornadas sorteadas) + os do mesmo universo, as duplas que a
 *   nota acha melhores, peneiradas em jornadas, e a vencedora medida em jornadas novas.
 */
function dificuldade() {
  const ids = characters.map((c) => c.id), NJ = lutas;
  const fortes = process.env.FORTES ? process.env.FORTES.split(',').filter((x) => ids.includes(x))
    : [...ids].sort((a, b) => (FORCA[b] ?? 0) - (FORCA[a] ?? 0)).slice(0, 40);
  const semente = (j: number) => (Math.imul(j + 1 + semente0 * 100003, 2654435761) >>> 1) & 0x7fffffff;
  const corte = [...Object.values(FORCA)].sort((a, b) => a - b)[Math.floor(0.6 * Object.values(FORCA).length)] ?? 0;
  const combos = (t: string[]) => (t.length < 2 ? 0 : combosDoTrio(t).combos.length);
  const trioBom = (x: string, seed: number) => {
    let d = newDraft(seed); d = { ...d, team: [x] }; d.candidates = d.candidates.filter((c) => c !== x);
    if (d.candidates.length < 3) d = skipDraft(d);
    while (d.team.length < 3) {
      const nota = (id: string) => forcaDoTrio([...d.team, id]);
      const melhor = [...d.candidates].filter((c) => c !== x).sort((a, b) => nota(b) - nota(a))[0];
      if (!melhor) { if (d.skips <= 0) break; d = skipDraft(d); continue; }
      const formaCombo = d.team.length > 0 && combos([...d.team, melhor]) > combos(d.team);
      if (d.team.length > 0 && !formaCombo && d.skips > 3 - d.team.length) { d = skipDraft(d); continue; }
      if (d.team.length === 0 && (FORCA[melhor] ?? 0) < corte && d.skips > 0) { d = skipDraft(d); continue; }
      d = pickDraft(d, melhor);
    }
    return d.team;
  };
  for (const [k, x] of ids.entries()) {
    if (k % partes !== parte) continue;
    let vAle = 0, vBom = 0;
    for (let j = 0; j < NJ; j++) {
      const s = semente(j), par = new Set<string>();
      while (par.size < 2) { const c = ids[Math.floor(rnd() * ids.length)]!; if (c !== x) par.add(c); }
      if (jornada([x, ...par], s) === 10) vAle++;
      const bom = trioBom(x, s);
      if (bom.length === 3 && jornada(bom, s) === 10) vBom++;
    }
    const uni = characters.find((c) => c.id === x)?.universe;
    const ps = [...new Set([...fortes, ...ids.filter((c) => uni && characters.find((z) => z.id === c)?.universe === uni)])].filter((c) => c !== x);
    const pares: [string, string, number][] = [];
    for (let a = 0; a < ps.length; a++) for (let b = a + 1; b < ps.length; b++) pares.push([ps[a]!, ps[b]!, forcaDoTrio([x, ps[a]!, ps[b]!])]);
    pares.sort((p, q) => q[2] - p[2]);
    const conta = (t: string[], de: number, ate: number) => { let v = 0; for (let j = de; j < ate; j++) if (jornada(t, semente(j)) === 10) v++; return v; };
    const peneira = pares.slice(0, 10).map(([a, b]) => ({ d: [a, b], v: conta([x, a, b], NJ, NJ + 8) })).sort((p, q) => q.v - p.v).slice(0, 3)
      .map((p) => ({ ...p, v: p.v + conta([x, ...p.d], NJ + 8, NJ + 24) })).sort((p, q) => q.v - p.v);
    const melhor = peneira[0]!.d, NM = Math.max(48, Math.round(NJ / 2));
    const vMel = conta([x, ...melhor], NJ + 24, NJ + 24 + NM);
    appendFileSync(saida, JSON.stringify({ id: x, aleatorio: vAle / NJ, bom: vBom / NJ, melhor: vMel / NM, dupla: melhor }) + '\n');
    console.log(`parte ${parte}: ${x} pronto`);
  }
}
