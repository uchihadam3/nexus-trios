/*
 * A classificação do Raio-X precisa separar.
 *
 * "ÓTIMA CONEXÃO" em todo par seria o mesmo defeito do "Dano" em 250 de 250:
 * um rótulo que vale sempre não diz nada. Este script sorteia trios, joga, e
 * mostra como as cinco classes se distribuem.
 */
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { acumularRaioX, lerRaioX, raioXVazio, type Classificacao } from '../src/engine/raio-x';

const LUTAS = Number(process.env.LUTAS ?? 120);
const conta = new Map<Classificacao, number>();
const forças: number[] = [];

for (let s = 1; s <= LUTAS; s += 1) {
  const pega = (n: number) => characters[(s * 61 + n * 37) % characters.length]!.id;
  const meu = [pega(1), pega(2), pega(3)], dele = [pega(4), pega(5), pega(6)];
  if (new Set([...meu, ...dele]).size < 6) continue;
  const b = createBattle(meu, dele, s);
  let estado = raioXVazio(), visto = 0;
  for (let p = 0; p < 4200 && !b.finished; p += 1) {
    stepBattle(b);
    const novos = b.events.filter((e) => e.id > visto);
    if (novos.length) { visto = Math.max(...novos.map((e) => e.id)); estado = acumularRaioX(estado, novos, b); }
  }
  for (const par of lerRaioX(estado, b)) { conta.set(par.classificacao, (conta.get(par.classificacao) ?? 0) + 1); forças.push(par.total); }
}

const total = [...conta.values()].reduce((a, b) => a + b, 0);
console.log(`${String(total)} pares avaliados em ${String(LUTAS)} lutas\n`);
for (const c of ['ÓTIMA CONEXÃO', 'BOA CONEXÃO', 'POUCA CONEXÃO', 'INDEPENDENTES', 'CONFLITO'] as Classificacao[]) {
  const n = conta.get(c) ?? 0;
  console.log(`  ${c.padEnd(16)}${String(n).padStart(5)}  ${(n / total * 100).toFixed(0).padStart(3)}%  ${'█'.repeat(Math.round(n / total * 40))}`);
}
const ordenadas = [...forças].sort((a, b) => a - b);
const p = (q: number) => ordenadas[Math.floor(ordenadas.length * q)];
console.log(`\nforça do par: p10 ${String(p(.1))} · mediana ${String(p(.5))} · p75 ${String(p(.75))} · p90 ${String(p(.9))} · máx ${String(ordenadas.at(-1))}`);
