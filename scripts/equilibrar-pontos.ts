/*
 * Mede quanto cada personagem pontua e grava o fator que traz todos para a
 * mesma parte dos pontos (src/data/pontos-por-personagem.ts).
 *
 * Pedidos do jogador: "os pontos têm que ser balanceados para que todos os
 * personagens que jogarem bem possam pontuar parecido" e, depois das
 * mecânicas novas, "tem que ter certeza que todos os personagens conseguem
 * estar pontuando de forma parecida".
 *
 * A medida é a FATIA do personagem nos pontos de feitos do próprio trio, em
 * cada luta (3 × os dele ÷ os do trio; 1 = parte justa). A fatia não depende
 * do tamanho da luta: o personagem forte, que chega às lutas finais (mais
 * longas, com mais feitos), não parece pontuar mais só por isso. Os trios são
 * sorteados, então os parceiros se compensam. Com a fatia medida usando os
 * fatores de agora, o fator novo é o de agora ÷ a fatia.
 *
 * Uso (4 partes em paralelo, ~7 min com 2500 jornadas cada):
 *   for p in 0 1 2 3; do npx tsx scripts/equilibrar-pontos.ts simular $p 4 2500 /tmp/pontos-$p.json & done; wait
 *   npx tsx scripts/equilibrar-pontos.ts ajustar /tmp/pontos-*.json
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { feitosDoLutador } from '../src/engine/pontos';
import { FATOR_DE_PONTOS } from '../src/data/pontos-por-personagem';

const MIN = 0.3, MAX = 3, MINIMO_DE_LUTAS = 60;
type Medida = { n: number; fatia: number; fatia2: number };

function simular(parte: number, partes: number, jornadas: number, saida: string) {
  const ids = characters.map((c) => c.id), med: Record<string, Medida> = {};
  let rng = 12345 + parte * 7777, lutas = 0;
  const r = () => { rng = (rng * 1103515245 + 12345) & 0x7fffffff; return rng / 0x7fffffff; };
  for (let j = 0; j < jornadas; j++) {
    const seed = 100000 + parte * 1000003 + j, trio: string[] = [];
    while (trio.length < 3) { const x = ids[Math.floor(r() * ids.length)]!; if (!trio.includes(x)) trio.push(x); }
    for (const [i, e] of generateCampaign(seed, trio).entries()) {
      const b = createBattle(trio, e.team, seed + i * 7919, e.scale);
      for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
      lutas++;
      const meus = b.fighters.filter((x) => x.side === 'player').map((f) => ({ id: f.characterId, p: Object.values(feitosDoLutador(f)).reduce((n, v) => n + v, 0) * (FATOR_DE_PONTOS[f.characterId] ?? 1) }));
      const soma = meus.reduce((n, m) => n + m.p, 0);
      for (const m of meus) {
        const fatia = soma > 0 ? (3 * m.p) / soma : 1, a = (med[m.id] ??= { n: 0, fatia: 0, fatia2: 0 });
        a.n++; a.fatia += fatia; a.fatia2 += fatia * fatia;
      }
      if (b.winner !== 'player') break;
    }
  }
  writeFileSync(saida, JSON.stringify({ lutas, fator: FATOR_DE_PONTOS, med }));
  console.log(`parte ${parte}/${partes}: ${lutas} lutas`);
}

function ajustar(arquivos: string[]) {
  const med: Record<string, Medida> = {};
  let lutas = 0, usado: Record<string, number> | undefined;
  for (const a of arquivos) {
    const d = JSON.parse(readFileSync(a, 'utf8')) as { lutas: number; fator: Record<string, number>; med: Record<string, Medida> };
    lutas += d.lutas; usado ??= d.fator;
    if (JSON.stringify(d.fator) !== JSON.stringify(usado)) throw new Error(`${a} foi medido com outros fatores`);
    for (const [k, m] of Object.entries(d.med)) { const x = (med[k] ??= { n: 0, fatia: 0, fatia2: 0 }); x.n += m.n; x.fatia += m.fatia; x.fatia2 += m.fatia2; }
  }
  const fator: Record<string, number> = {};
  for (const c of [...characters].sort((a, b) => a.id.localeCompare(b.id))) {
    const m = med[c.id], antes = usado?.[c.id] ?? 1;
    fator[c.id] = !m || m.n < MINIMO_DE_LUTAS ? antes : Math.round(Math.max(MIN, Math.min(MAX, antes / (m.fatia / m.n))) * 100) / 100;
  }
  const corpo = Object.entries(fator).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
  writeFileSync(new URL('../src/data/pontos-por-personagem.ts', import.meta.url), `/*
 * O fator de pontos de cada personagem — gerado por scripts/equilibrar-pontos.ts
 * (${lutas} lutas de trios sorteados; fator entre ×${MIN} e ×${MAX}). Leva a fatia de
 * cada personagem nos pontos do trio para a parte justa.
 * Não editar à mão: rode o script de novo depois de mudar o elenco ou os pesos.
 */
export const FATOR_DE_PONTOS: Record<string, number> = {
${corpo}
};
`);
  const poucos = characters.filter((c) => (med[c.id]?.n ?? 0) < MINIMO_DE_LUTAS).map((c) => c.id);
  console.log(`${lutas} lutas · ${Object.keys(fator).length} fatores · com poucas lutas (fator mantido): ${poucos.join(', ') || 'nenhum'}`);
}

const [modo, ...args] = process.argv.slice(2);
if (modo === 'simular') simular(Number(args[0]), Number(args[1]), Number(args[2]), args[3]!);
else if (modo === 'ajustar') ajustar(args);
else console.log('uso: simular <parte> <partes> <jornadas> <saida> | ajustar <arquivos...>');
