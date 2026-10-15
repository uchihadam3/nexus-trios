/*
 * Os trios que vencem de verdade, para os NPCs do treino PvP (src/data/trios-do-pvp.ts).
 *
 * A nota das Dicas (notaDoTrio) é boa para ensinar, mas, procurando os maiores valores dela entre 10 milhões de trios,
 * o NPC acha trios que só parecem bons (o "Mestre" perdia para a "Profissional"). Aqui cada trio candidato luta de
 * verdade contra um grupo fixo de trios bons, dos dois lados da arena, e o que entra na lista é a taxa de vitória.
 *
 * Uso:  npx tsx scripts/trios-fortes.ts <parte> <partes>   → uma linha JSON por candidato (para rodar em paralelo)
 */
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { forcaDoTrio } from '../src/engine/campaign';
import { timesDoNpc, type NivelNpc } from '../src/engine/pvp';
import { notaDoTrio } from '../src/presentation/dicas-do-trio';
import { FORCA } from '../src/data/forca-dos-rivais';

const [parte = 0, partes = 1] = process.argv.slice(2).map(Number);
const chave = (t: readonly string[]) => [...t].sort().join('+');

// candidatos: o que os NPCs montariam (vários sorteios), os melhores pela força medida e trios com os mais fortes
const candidatos = new Map<string, string[]>();
const junta = (t: string[]) => { if (new Set(t).size === 3) candidatos.set(chave(t), t); };
for (let s = 1; s <= 70; s++) for (const nivel of [4, 5] as NivelNpc[]) for (const t of timesDoNpc(nivel, s * 7919 + nivel)) junta(t);
for (let s = 1; s <= 40; s++) for (const t of timesDoNpc(5, s * 104729, forcaDoTrio)) junta(t);
const fortes = characters.map((c) => c.id).sort((a, b) => (FORCA[b] ?? 0) - (FORCA[a] ?? 0)).slice(0, 36);
for (let i = 0; i < fortes.length; i++) for (let j = i + 1; j < fortes.length; j++) for (let k = j + 1; k < fortes.length; k++) {
  const t = [fortes[i]!, fortes[j]!, fortes[k]!];
  if (forcaDoTrio(t) > 1.2) junta(t);
}
const lista = [...candidatos.values()].sort((a, b) => notaDoTrio(b) - notaDoTrio(a)).slice(0, 900);

// o grupo de teste: trios bons e variados (Profissional e Intermediário)
const teste: string[][] = [];
for (let s = 1; s <= 8; s++) teste.push(...timesDoNpc(4, 31337 + s * 97), ...(s <= 4 ? timesDoNpc(3, 777 + s * 13) : []));

const luta = (a: string[], b: string[], seed: number) => { const bt = createBattle(a, b, seed); let n = 0; while (!bt.finished && n < 40000) { stepBattle(bt); n++; } return bt.winner; };
lista.forEach((t, i) => {
  if (i % partes !== parte) return;
  let v = 0, n = 0;
  teste.forEach((o, j) => {
    if (o.some((x) => t.includes(x))) return;
    if (luta(t, o, 1000 + i * 131 + j) === 'player') v++;
    if (luta(o, t, 5000 + i * 137 + j) === 'enemy') v++;
    n += 2;
  });
  console.log(JSON.stringify({ trio: t, v, n, nota: +notaDoTrio(t).toFixed(3) }));
});
