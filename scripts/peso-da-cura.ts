/*
 * Mede quanto cada personagem cura e protege por luta e grava o peso da cura (src/data/peso-da-cura.ts).
 *
 * Pedido do jogador: tirar o teto da cura e da proteção e, no lugar, "reduzir os pontos de alguns
 * personagens, o tanto de ponto que eles fazem curando e protegendo, pra poder abaixar um pouco".
 *
 * A medida é a média, por luta, dos pontos de cura e proteção do personagem (já com o fator dele) em
 * trios sorteados, sem peso nenhum. Quem passa de PESO_DA_CURA_ALVO ganha o peso alvo ÷ média; os
 * outros contam inteiros.
 *
 * Uso (4 partes em paralelo, ~10 min com 8000 jornadas cada):
 *   for p in 0 1 2 3; do npx tsx scripts/peso-da-cura.ts simular $p 4 8000 /tmp/cura-$p.json & done; wait
 *   npx tsx scripts/peso-da-cura.ts ajustar /tmp/cura-*.json
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { FEITOS, PESO_DA_CURA_ALVO } from '../src/engine/pontos';
import { FATOR_DE_PONTOS } from '../src/data/pontos-por-personagem';

const MINIMO_DE_LUTAS = 60;
type Medida = { n: number; soma: number };

function simular(parte: number, partes: number, jornadas: number, saida: string) {
  const ids = characters.map((c) => c.id), med: Record<string, Medida> = {};
  let rng = 4242 + parte * 9973, lutas = 0;
  const r = () => { rng = (rng * 1103515245 + 12345) & 0x7fffffff; return rng / 0x7fffffff; };
  for (let j = 0; j < jornadas; j++) {
    const seed = 300000 + parte * 1000003 + j, trio: string[] = [];
    while (trio.length < 3) { const x = ids[Math.floor(r() * ids.length)]!; if (!trio.includes(x)) trio.push(x); }
    for (const [i, e] of generateCampaign(seed, trio).entries()) {
      const b = createBattle(trio, e.team, seed + i * 7919, e.scale);
      for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
      lutas++;
      for (const f of b.fighters.filter((x) => x.side === 'player')) {
        const a = (med[f.characterId] ??= { n: 0, soma: 0 });
        a.n++; a.soma += (f.stats.healing + f.stats.protection) * FEITOS.porApoio * (FATOR_DE_PONTOS[f.characterId] ?? 1);
      }
      if (b.winner !== 'player') break;
    }
  }
  writeFileSync(saida, JSON.stringify({ lutas, partes, med }));
  console.log(`parte ${parte}/${partes}: ${lutas} lutas`);
}

function ajustar(arquivos: string[]) {
  const med: Record<string, Medida> = {};
  let lutas = 0;
  for (const a of arquivos) {
    const d = JSON.parse(readFileSync(a, 'utf8')) as { lutas: number; med: Record<string, Medida> };
    lutas += d.lutas;
    for (const [k, m] of Object.entries(d.med)) { const x = (med[k] ??= { n: 0, soma: 0 }); x.n += m.n; x.soma += m.soma; }
  }
  const peso: Record<string, number> = {};
  for (const c of [...characters].sort((a, b) => a.id.localeCompare(b.id))) {
    const m = med[c.id];
    if (!m || m.n < MINIMO_DE_LUTAS) continue;
    const media = m.soma / m.n;
    const p = Math.round((PESO_DA_CURA_ALVO / media) * 100) / 100;
    if (p < 1) peso[c.id] = p;
  }
  const corpo = Object.entries(peso).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
  writeFileSync(new URL('../src/data/peso-da-cura.ts', import.meta.url), `/*
 * O peso da cura e da proteção de cada personagem nos pontos — gerado por scripts/peso-da-cura.ts
 * (${lutas} lutas de trios sorteados). Quem cura ou protege, em média, mais que PESO_DA_CURA_ALVO
 * pontos por luta tem a cura e a proteção contadas com este peso, que traz a média dele para o alvo
 * (pedido do jogador: "reduzir os pontos de alguns personagens, o tanto de ponto que eles fazem
 * curando e protegendo, pra poder abaixar um pouco, mas sem limitar"). Quem não está aqui conta inteiro.
 * Não editar à mão: rode o script de novo depois de mudar o elenco ou os pesos dos pontos.
 */
export const PESO_DA_CURA: Record<string, number> = {
${corpo}
};
`);
  console.log(`${lutas} lutas · ${Object.keys(peso).length} personagens com peso na cura`);
}

const [modo, ...args] = process.argv.slice(2);
if (modo === 'simular') simular(Number(args[0]), Number(args[1]), Number(args[2]), args[3]!);
else if (modo === 'ajustar') ajustar(args);
else console.log('uso: simular <parte> <partes> <jornadas> <saida> | ajustar <arquivos...>');
