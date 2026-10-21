/*
 * A posição medida dos trios do topo (pedido do dono: "começar com os times que estão sempre no topo… ver se eles estão
 * lá mesmo"): lê as rodadas do plano topo da fábrica (scripts/fabrica/lutas.ts; linhas "posicao i j k v n") e grava
 * src/data/topo-medido.ts com os trios na ordem da taxa de vitória de verdade contra o painel dos fortes.
 * Uso: npx tsx scripts/posicao-medida.ts <lutas.txt.gz>…   (só rodadas com o motor e o elenco de agora)
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { characters } from '../src/data/characters';
import { ENGINE_VERSION, rosterFingerprint } from '../src/engine/ranked';

const arqs = process.argv.slice(2);
const textos = arqs.map((f) => gunzipSync(readFileSync(f)).toString());
const cabecalho = `# motor ${ENGINE_VERSION} elenco ${rosterFingerprint()}`;
for (const [n, t] of textos.entries()) if (!t.split('\n').some((l) => l.startsWith(cabecalho))) throw new Error(`${arqs[n]}: medido com outro motor ou elenco`);
const trios = new Map<number, { t: number[]; v: number; n: number }>();
for (const t of textos) for (const l of t.split('\n')) {
  if (!l || l.startsWith('#')) continue;
  const [pos, i, j, k, v, n] = l.split(' ').map(Number);
  const x = trios.get(pos!) ?? { t: [i!, j!, k!], v: 0, n: 0 };
  x.v += v!; x.n += n!; trios.set(pos!, x);
}
// medidos de forma contínua: as posições 1 até M, sem buraco
const M = [...trios.keys()].sort((a, b) => a - b).findIndex((p, i) => p !== i + 1);
const medidos = [...trios.entries()].filter(([p]) => M < 0 || p <= M).map(([p, x]) => ({ p, ...x, taxa: x.v / x.n }));
medidos.sort((a, b) => b.taxa - a.taxa || a.p - b.p);
const ids = characters.map((c) => c.id), cod = (i: number) => i.toString(36).padStart(2, '0');
writeFileSync('src/data/topo-medido.ts', `/*
 * Os ${medidos.length.toLocaleString('pt-BR')} trios do topo pela nota das Dicas, em ordem de luta de verdade (gerado por scripts/posicao-medida.ts com o
 * plano topo da fábrica: cada um lutou ~${Math.round(medidos[0]!.n / 100) * 100} vezes contra um painel dos 3.000 trios mais fortes, trocando o lado).
 * TRIOS: 6 caracteres por trio, cada personagem com 2 caracteres em base 36 = a posição dele em IDS; o primeiro trio é o
 * que mais venceu. A posição desses trios vem daqui, não da nota (src/presentation/posicao-do-trio.ts).
 */
export const ELENCO_MEDIDO = ${JSON.stringify(rosterFingerprint())};
export const IDS = '${ids.join(',')}';
export const TRIOS = '${medidos.map((x) => x.t.map(cod).join('')).join('')}';
`);
console.log(`${medidos.length} trios; topo:`, medidos.slice(0, 5).map((x) => `${x.t.map((i) => ids[i]).join('+')} ${(100 * x.taxa).toFixed(1)}% (nota ${x.p}º)`).join(' · '));
