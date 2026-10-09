/*
 * Confere, para cada personagem, as duas regras do jogador:
 *   1. ninguém é tão fraco que, mesmo com os 2 melhores parceiros, nunca vence as 10;
 *   2. ninguém é tão forte que, com 2 parceiros quaisquer, vence quase sempre.
 * Para cada personagem X: joga N jornadas com X + os 2 parceiros que mais somam
 * força e sinergia com ele ("melhor caso") e N jornadas com X + 2 sorteados
 * ("qualquer dupla"), e conta quantas vencem as 10 lutas.
 *
 * Uso: npx tsx scripts/conferir-personagens.ts <parte 0-3> <N> > saida.jsonl
 */
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { forcaDoTrio, generateCampaign } from '../src/engine/campaign';

const parte = Number(process.argv[2]), N = Number(process.argv[3]);
const ids = characters.map((c) => c.id);
let r = 1234 + parte;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
function melhoresParceiros(x: string): string[] {
  let best: string[] = [], f = -Infinity;
  for (const a of ids) for (const b of ids) {
    if (a >= b || a === x || b === x) continue;
    const t = [x, a, b], v = forcaDoTrio(t);
    if (v > f) { f = v; best = t; }
  }
  return best;
}
function campeao(team: string[], seed: number) {
  for (const [i, e] of generateCampaign(seed, team).entries()) {
    const b = createBattle(team, e.team, seed + i * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner !== 'player') return { venceu: false, lutas: i };
  }
  return { venceu: true, lutas: 10 };
}
for (const [k, x] of ids.entries()) {
  if (k % 4 !== parte) continue;
  const melhor = melhoresParceiros(x);
  let vm = 0, vq = 0, lm = 0, lq = 0;
  for (let n = 0; n < N; n++) {
    const s1 = Math.floor(rnd() * 2 ** 31), a = campeao(melhor, s1); if (a.venceu) vm++; lm += a.lutas;
    const t = new Set([x]); while (t.size < 3) t.add(ids[Math.floor(rnd() * ids.length)]!);
    const s2 = Math.floor(rnd() * 2 ** 31), q = campeao([...t], s2); if (q.venceu) vq++; lq += q.lutas;
  }
  console.log(JSON.stringify({ id: x, melhor, campeaoMelhor: vm / N, campeaoQualquer: vq / N, lutasMelhor: lm / N, lutasQualquer: lq / N }));
}
