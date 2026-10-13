/*
 * A régua da nota de cada ajuda do "Quem ajudou quem" (pedido do jogador: "tá falando que ele ajudou… mas foi boa
 * essa ajuda? … muito ruim, ruim, na média, bom, muito bom, excelente").
 *
 * Sorteia trios, joga as lutas e guarda, para cada tipo de ajuda, quanto a ajuda principal de cada direção rendeu
 * (o mesmo número que a tela mostra: % de Carga, Vida curada, golpes travados…). A distribuição de cada tipo (de
 * 5 em 5%) vai para src/engine/regua-das-ajudas.ts.
 *
 * Uso: npx tsx scripts/medir-ajudas.ts   (LUTAS=1200 por padrão)
 */
import { writeFileSync } from 'fs';
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { acumularRaioX, lerRaioX, quemAbsorveu, raioXVazio } from '../src/engine/raio-x';
import { medidaDaAjuda } from '../src/engine/nota-da-ajuda';

const LUTAS = Number(process.env.LUTAS ?? 1200);
const amostras: Record<string, number[]> = {};
let semente = 20251013;
const sorte = () => (semente = (semente * 1103515245 + 12345) % 2147483648) / 2147483648;
const ids = characters.map((c) => c.id);
const sorteia = (fora: string[]) => { let x: string; do x = ids[Math.floor(sorte() * ids.length)]!; while (fora.includes(x)); return x; };

for (let s = 1; s <= LUTAS; s += 1) {
  const todos: string[] = [];
  for (let i = 0; i < 6; i += 1) todos.push(sorteia(todos));
  const b = createBattle(todos.slice(0, 3), todos.slice(3), s);
  let estado = raioXVazio(), visto = 0;
  for (let p = 0; p < 4200 && !b.finished; p += 1) {
    stepBattle(b);
    const novos = b.events.filter((e) => e.id > visto);
    if (novos.length) { visto = Math.max(...novos.map((e) => e.id)); estado = acumularRaioX(estado, novos, b); }
  }
  for (const par of lerRaioX(estado, b)) for (const d of [par.aParaB, par.bParaA]) {
    const m = medidaDaAjuda(d);
    if (m) (amostras[m.tipo] ??= []).push(m.valor);
  }
  const pressao = quemAbsorveu(estado, b);
  if (pressao) (amostras.pressao ??= []).push(pressao.dano);
}

const cortes: Record<string, number[]> = {};
for (const [tipo, v] of Object.entries(amostras)) {
  if (v.length < 30) continue;
  const o = [...v].sort((a, b) => a - b), p = (q: number) => o[Math.min(o.length - 1, Math.floor(o.length * q))]!;
  cortes[tipo] = Array.from({ length: 21 }, (_, i) => Math.round(p(i / 20) * 10) / 10);
  console.log(`${tipo.padEnd(18)} n=${String(v.length).padStart(5)}  p10 ${p(0.1)} · mediana ${p(0.5)} · p90 ${p(0.9)}`);
}
writeFileSync('src/engine/regua-das-ajudas.ts', `/* Gerado por scripts/medir-ajudas.ts (${LUTAS} lutas sorteadas) — não editar à mão. */
/** Quanto cada tipo de ajuda rende numa luta: os percentis 0, 5, 10… 100. */
export const REGUA_DAS_AJUDAS: Record<string, readonly number[]> = {
${Object.entries(cortes).map(([k, v]) => `  '${k}': [${v.join(', ')}],`).join('\n')}
};
`);
