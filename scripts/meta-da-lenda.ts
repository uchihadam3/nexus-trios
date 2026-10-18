/*
 * O "meta" da Lenda do Nexus (o 6º NPC do treino): os trios que mais vencem dos trios fortes, não de trios sorteados.
 * Pedido do dono: a Lenda é mais forte por jogar melhor, sem Vida a mais ("é uma simulação de PvP"). Os 150 primeiros de
 * src/data/trios-do-pvp.ts (os que mais vencem de trios sorteados) lutam contra os 18 primeiros (os trios do Mestre),
 * 12 lutas por confronto, metade de cada lado; os 12 que mais vencem vão para src/data/meta-da-lenda.ts.
 * Refazer quando os personagens mudarem (junto com trios-do-pvp): npx tsx scripts/meta-da-lenda.ts
 */
import { writeFileSync } from 'node:fs';
import { TRIOS_DO_PVP } from '../src/data/trios-do-pvp';
import { createBattle, stepBattle } from '../src/engine/battle';

const candidatos = TRIOS_DO_PVP.slice(0, 150).map((t) => t.slice(0, 3) as string[]), fortes = TRIOS_DO_PVP.slice(0, 18).map((t) => t.slice(0, 3) as string[]);
const medidos = candidatos.map((trio, c) => {
  let v = 0, n = 0;
  fortes.forEach((forte, f) => {
    if (forte.some((id) => trio.includes(id))) return;
    for (let k = 0; k < 12; k++) {
      const embaixo = k % 2 === 0, seed = 7000 + c * 131 + f * 17 + k;
      const b = embaixo ? createBattle(trio, forte, seed) : createBattle(forte, trio, seed);
      for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
      if (!b.finished) continue;
      n++; if ((b.winner === 'player') === embaixo) v++;
    }
  });
  return { trio, taxa: (100 * v) / Math.max(1, n), n };
}).sort((a, b) => b.taxa - a.taxa).slice(0, 12);
writeFileSync(new URL('../src/data/meta-da-lenda.ts', import.meta.url), `/*
 * O meta da Lenda do Nexus: os trios que mais vencem dos trios fortes (os 18 primeiros de trios-do-pvp, os do Mestre), em
 * lutas de verdade (scripts/meta-da-lenda.ts). [trio, % de vitórias contra os fortes, lutas]. Não editar à mão.
 */
export const META_DA_LENDA: readonly (readonly [string, string, string, number, number])[] = [
${medidos.map((m) => `  [${m.trio.map((id) => JSON.stringify(id)).join(', ')}, ${m.taxa.toFixed(1)}, ${m.n}],`).join('\n')}
];
`);
console.log(medidos.map((m) => `${m.trio.join('+')} ${m.taxa.toFixed(1)}%`).join('\n'));
