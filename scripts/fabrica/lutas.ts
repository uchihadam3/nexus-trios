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
 *
 * Cada linha: a1 a2 a3 b1 b2 b3 v (índices do elenco; v = 1 se o trio a venceu).
 * A primeira linha (# ...) diz o motor e o elenco, para não misturar medidas.
 */
import { writeFileSync, appendFileSync } from 'node:fs';
import { characters } from '../../src/data/characters';
import { createBattle, stepBattle } from '../../src/engine/battle';
import { ENGINE_VERSION, rosterFingerprint } from '../../src/engine/ranked';

const [plano, parteTxt, partesTxt, lutasTxt, saida, sementeTxt = '0'] = process.argv.slice(2);
const parte = Number(parteTxt), partes = Number(partesTxt), lutas = Number(lutasTxt), semente = Number(sementeTxt);
if (!plano || !saida || !(partes > 0) || !(parte >= 0 && parte < partes) || !(lutas > 0)) {
  console.error('uso: lutas <aleatorio|pares> <parte> <partes> <lutas> <saida.txt> [semente]');
  process.exit(1);
}
const N = characters.length;
let r = (Math.imul(parte + 1, 2654435761) ^ Math.imul(semente + 7, 40503) ^ (plano === 'pares' ? 0x9e3779b9 : 0)) >>> 0;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
const sorteia = (fora: Set<number>) => { let i: number; do i = Math.floor(rnd() * N); while (fora.has(i)); fora.add(i); return i; };

/* As duplas desta parte (pares): a k-ésima dupla da lista vai para a parte k % partes. */
const duplas: [number, number][] = [];
if (plano === 'pares') { let k = 0; for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++, k++) if (k % partes === parte) duplas.push([i, j]); }
else if (plano !== 'aleatorio') { console.error(`plano desconhecido: ${plano}`); process.exit(1); }

writeFileSync(saida, `# motor ${ENGINE_VERSION} elenco ${rosterFingerprint()} plano ${plano} parte ${parte}/${partes} semente ${semente}\n`);
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
