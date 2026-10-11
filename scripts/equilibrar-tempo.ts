/*
 * Equilíbrio pelo tempo (pedido do jogador: "todo personagem tem que ter pelo
 * menos 1% de chance de ganhar no aleatório… vamos tentar manter entre 1% e
 * 5%", sem inflar números).
 *
 * Lê a medição das jornadas com trios sorteados (para cada personagem: em
 * quantas apareceu, quantas venceu as 10 e a média de lutas vencidas) e mexe no
 * ajuste de tempo (src/data/ajuste-de-tempo.ts) de quem está fora da faixa: quem
 * vence poucas lutas carrega mais depressa e prepara mais rápido; quem vence
 * demais, o contrário. A média de lutas vencidas é o guia (bem menos ruidosa que
 * a chance de vencer as 10): ~2 lutas ≈ 1%, ~3 ≈ 3%, ~3,5 ≈ 4,5%.
 *
 * Uso: npx tsx scripts/equilibrar-tempo.ts <medição.json>
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { AJUSTE_DE_TEMPO } from '../src/data/ajuste-de-tempo';
import { AJUSTE_DE_KIT } from '../src/data/ajuste-de-kit';

type Linha = { id: string; n: number; p: number; lutas: number };
const medicao = JSON.parse(readFileSync(process.argv[2]!, 'utf8')) as Linha[];
const MIN = Number(process.env.MIN ?? 2.45), MAX = Number(process.env.MAX ?? 3.5), K = Number(process.env.K ?? 0.5);
const novo: Record<string, number> = { ...AJUSTE_DE_TEMPO };
let mexidos = 0;
for (const l of medicao) {
  const s = AJUSTE_DE_TEMPO[l.id] ?? 0;
  // abaixo de 1% mesmo dentro da faixa de lutas: um empurrão pequeno
  // acima de 6% mesmo com poucas lutas (quem leva o trio sozinho às 10): um freio pequeno
  // a chance de vencer as 10 manda primeiro (quem tem poucas lutas mas leva muitas jornadas ao fim é forte)
  const PMAX = Number(process.env.PMAX ?? 0.065), PMIN = Number(process.env.PMIN ?? 0.008);
  const alvo = l.p > PMAX ? l.lutas - 0.35 - 4 * (l.p - PMAX) : l.p < PMIN ? l.lutas + 0.25 : l.lutas < MIN ? MIN + 0.15 : l.lutas > MAX ? MAX - 0.15 : l.lutas;
  const v = Math.round(Math.max(-1.5, Math.min(1.5, s + K * (alvo - l.lutas))) * 100) / 100;
  if (v !== s) mexidos++;
  if (v === 0) delete novo[l.id]; else novo[l.id] = v;
}
/*
 * O ajuste do kit (src/data/ajuste-de-kit.ts): só para quem está claramente fora da faixa — a
 * porcentagem dos Status e o intervalo do traço andam um passo (até 30% no total).
 */
const kit: Record<string, number> = { ...AJUSTE_DE_KIT };
const KMAX = Number(process.env.KMAX ?? 0.07), KMIN = Number(process.env.KMIN ?? 0.012);
for (const l of medicao) {
  const k = kit[l.id] ?? 0;
  const passo = l.p > KMAX ? (l.p > 0.09 ? -0.35 : -0.2) : l.p < KMIN ? (l.p < 0.006 ? 0.35 : 0.2) : 0;
  const v = Math.round(Math.max(-1, Math.min(1, k + passo)) * 100) / 100;
  if (v === 0) delete kit[l.id]; else kit[l.id] = v;
}
{
  const arqK = new URL('../src/data/ajuste-de-kit.ts', import.meta.url);
  const corpoK = Object.entries(kit).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
  writeFileSync(arqK, readFileSync(arqK, 'utf8').replace(/export const AJUSTE_DE_KIT: Record<string, number> = \{[\s\S]*?\n\};/, `export const AJUSTE_DE_KIT: Record<string, number> = {\n${corpoK}\n};`));
  console.log('kit: mexidos', Object.keys(kit).length, '· enfraquecidos', Object.values(kit).filter((v) => v < 0).length, '· fortalecidos', Object.values(kit).filter((v) => v > 0).length);
}
// os rivais vêm do mesmo elenco: acelerar todo mundo também acelera os inimigos. Só a diferença entre
// eles conta, então a média volta para zero (e quem estava no limite ganha espaço).
if (process.env.CENTRA) {
  const ids = medicao.map((l) => l.id), media = ids.reduce((a, id) => a + (novo[id] ?? 0), 0) / ids.length;
  for (const id of ids) {
    const v = Math.round(Math.max(-1.5, Math.min(1.5, (novo[id] ?? 0) - media)) * 100) / 100;
    if (v === 0) delete novo[id]; else novo[id] = v;
  }
  console.log('média tirada:', media.toFixed(3));
}
const corpo = Object.entries(novo).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
const arq = new URL('../src/data/ajuste-de-tempo.ts', import.meta.url);
const atual = readFileSync(arq, 'utf8');
writeFileSync(arq, atual.replace(/export const AJUSTE_DE_TEMPO: Record<string, number> = \{[\s\S]*?\n\};/, `export const AJUSTE_DE_TEMPO: Record<string, number> = {\n${corpo}\n};`));
const vs = Object.values(novo);
console.log('mexidos', mexidos, '· no limite +1:', vs.filter((v) => v >= 1.5).length, '· no limite −1:', vs.filter((v) => v <= -1.5).length);
