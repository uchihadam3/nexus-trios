/*
 * O alinhamento de alvos mexeu em 80 efeitos. Isso é correção de defeito, não
 * balanceamento — mas um personagem que parou de bater no próprio time ficou
 * mais forte, e vale saber de quanto.
 */
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';

const N = Number(process.env.N ?? 200);
const medir = (id: string) => {
  const indice = characters.findIndex((c) => c.id === id);
  const c = characters[indice]!;
  let vit = 0;
  for (let s = 0; s < N; s += 1) {
    const outros = characters.filter((o) => o.id !== c.id);
    const pega = (n: number) => outros[(s * 37 + n * 61 + indice) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 1);
    for (let p = 0; p < 4200 && !b.finished; p += 1) stepBattle(b);
    if (b.winner === 'player') vit += 1;
  }
  const taxa = vit / N;
  return { nome: c.name, taxa, erro: Math.sqrt((taxa * (1 - taxa)) / N) * 1.96 * 100 };
};

/* A média, com a mesma regra de sorteio. */
let soma = 0; const AMOSTRA = 60;
for (let i = 0; i < AMOSTRA; i += 1) {
  const c = characters[(i * 17) % characters.length]!;
  const indice = characters.indexOf(c);
  let vit = 0;
  for (let s = 0; s < 40; s += 1) {
    const outros = characters.filter((o) => o.id !== c.id);
    const pega = (n: number) => outros[(s * 37 + n * 61 + indice) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 1);
    for (let p = 0; p < 4200 && !b.finished; p += 1) stepBattle(b);
    if (b.winner === 'player') vit += 1;
  }
  soma += vit / 40;
}
const media = soma / AMOSTRA;
console.log(`média geral: ${(media * 100).toFixed(1)}% · ${String(N)} lutas por personagem medido\n`);
for (const id of ['sakura', 'piccolo', 'ichigo', 'edward', 'itachi', 'zenitsu']) {
  if (!characters.some((c) => c.id === id)) continue;
  const m = medir(id);
  const d = (m.taxa - media) * 100;
  console.log(`${m.nome.padEnd(18)} ${(m.taxa * 100).toFixed(1)}% ± ${m.erro.toFixed(1)}  (${d >= 0 ? '+' : ''}${d.toFixed(1)} vs média)`);
}
