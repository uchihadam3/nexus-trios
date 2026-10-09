/*
 * Regra 1 do jogador ("nenhum personagem tão fraco que, mesmo com os melhores
 * parceiros, nunca vence as 10"), conferida nas lutas e não pela conta:
 * para cada personagem da lista, testa várias duplas de parceiros fortes
 * (inclusive os que seguram dano), fica com a dupla que vai mais longe e mede
 * quantas jornadas ela vence inteiras.
 *
 * Uso: npx tsx scripts/conferir-melhor-dupla.ts <parte 0-3> <ids separados por vírgula>
 */
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';
import { createBattle, stepBattle } from '../src/engine/battle';
import { generateCampaign } from '../src/engine/campaign';

const parte = Number(process.argv[2]), lista = process.argv[3]!.split(',');
const fortes = characters.map((c) => c.id).sort((a, b) => (FORCA[b] ?? 0) - (FORCA[a] ?? 0)).slice(0, 24);
let r = 777 + parte;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
function jornada(team: string[], seed: number) {
  for (const [i, e] of generateCampaign(seed, team).entries()) {
    const b = createBattle(team, e.team, seed + i * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner !== 'player') return i;
  }
  return 10;
}
const media = (team: string[], n: number) => { let s = 0, c = 0; for (let k = 0; k < n; k++) { const l = jornada(team, Math.floor(rnd() * 2 ** 31)); s += l; if (l === 10) c++; } return { lutas: s / n, campeao: c / n }; };
for (const [k, x] of lista.entries()) {
  if (k % 4 !== parte) continue;
  const duplas: string[][] = [];
  const pool = fortes.filter((id) => id !== x);
  while (duplas.length < Number(process.env.DUPLAS ?? 14)) { const a = pool[Math.floor(rnd() * pool.length)]!, b = pool[Math.floor(rnd() * pool.length)]!; if (a !== b && !duplas.some((d) => d.includes(a) && d.includes(b))) duplas.push([a, b]); }
  const notas = duplas.map((d) => ({ d, ...media([x, ...d], 10) })).sort((p, q) => q.lutas - p.lutas);
  const melhor = notas[0]!.d, final = media([x, ...melhor], 40);
  console.log(JSON.stringify({ id: x, forca: FORCA[x], dupla: melhor, campeao: final.campeao, lutas: final.lutas }));
}
