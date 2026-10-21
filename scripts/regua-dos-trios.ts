/*
 * A régua da força dos trios: a nota das Dicas (notaDoTrio) de TODOS os 10.586.800 trios do elenco, em ordem.
 *   src/data/percentis-dos-trios.ts — PERCENTIS: a nota em cada 1% (0 a 100), de onde saem o "melhor que X%" e as estrelas;
 *   src/data/percentis-finos.ts — PERCENTIS_FINOS: a nota a cada 0,05% (0 a 2000), para o "dentro desse X%, onde ele está"
 *   (pedido do dono: "melhor que 99%… mas dentro desses 99%, tá onde?").
 * Refazer (as duas juntas) quando os personagens ou as Dicas mudarem: npx tsx scripts/regua-dos-trios.ts
 * Com --conferir, só confere se a régua de 1% gravada ainda bate com as notas de agora.
 * Também grava src/data/posicoes-dos-trios.ts: quantos trios há em cada nota (de 0,001 em 0,001), de onde sai a posição
 * exata do time entre todos (pedido do dono: "aparece a posição dele na frente depois das porcentagens").
 */
import { writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { PERCENTIS } from '../src/data/percentis-dos-trios';
import { notaDoTrio } from '../src/presentation/dicas-do-trio';

const N = characters.length, ids = characters.map((c) => c.id);
const notas = new Float64Array((N * (N - 1) * (N - 2)) / 6);
let g = 0;
const inicio = Date.now();
for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k = j + 1; k < N; k++) notas[g++] = notaDoTrio([ids[i]!, ids[j]!, ids[k]!]);
notas.sort();
console.log(`${g} trios em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);

/* a nota na posição q (0 a 1) da fila de todos os trios */
const na = (q: number) => Math.round(notas[Math.round(q * (g - 1))]! * 1000) / 1000;
const porCento = Array.from({ length: 101 }, (_, p) => na(p / 100));
const diferentes = porCento.filter((x, p) => Math.abs(x - PERCENTIS[p]!) > 0.0015).length;
console.log(`régua de 1%: ${diferentes} de 101 pontos mudaram desde a gravada`);
if (process.argv.includes('--conferir')) process.exit(diferentes ? 1 : 0);

const linhas = (l: number[], porLinha: number) => Array.from({ length: Math.ceil(l.length / porLinha) }, (_, n) => `  ${l.slice(n * porLinha, (n + 1) * porLinha).join(', ')},`).join('\n');
writeFileSync('src/data/percentis-dos-trios.ts', `/*
 * A régua da força dos trios (gerado com os ${g.toLocaleString('pt-BR')} trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
${linhas(porCento, 10)}
];
`);
const finos = Array.from({ length: 2001 }, (_, n) => na(n / 2000));
writeFileSync('src/data/percentis-finos.ts', `/*
 * A régua fina da força dos trios (gerado por scripts/regua-dos-trios.ts, com a de 1%): PERCENTIS_FINOS[n] é a nota das
 * Dicas que fica acima de n × 0,05% de todos os trios (n de 0 a 2000). Serve para o "dentro desse X%, onde ele está":
 * cada 1% da régua tem 20 pontos aqui.
 */
export const PERCENTIS_FINOS: readonly number[] = [
${linhas(finos, 20)}
];
`);
const bins = Array.from(notas, (v) => Math.round(v * 1000)), de = bins[0]!, ate = bins[g - 1]!;
const contas = new Array<number>(ate - de + 1).fill(0);
for (const b of bins) contas[b - de]!++;
writeFileSync('src/data/posicoes-dos-trios.ts', `/*
 * Quantos trios há em cada nota das Dicas (gerado por scripts/regua-dos-trios.ts, com a régua): a nota arredondada em
 * milésimos, de DE (${de / 1000}) para cima, uma contagem por milésimo em base 36, separadas por vírgula. Soma
 * ${g.toLocaleString('pt-BR')} trios. Daqui sai a posição exata do time entre todos (src/presentation/posicao-do-trio.ts);
 * é carregado só quando a tela das estrelas abre.
 */
export const TOTAL_DE_TRIOS = ${g};
export const DE = ${de};
export const CONTAS = '${contas.map((c) => c.toString(36)).join(',')}';
`);
console.log('gravado');
