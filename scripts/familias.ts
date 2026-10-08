/*
 * Junta a medição de `calibrar.ts` por família (estilo), com o intervalo de
 * confiança de cada uma. Um personagem isolado tem ±10 pontos de ruído mesmo
 * com 100 lutas; a família junta centenas e é onde a decisão se sustenta.
 *
 * Uso: SEMENTES=100 npx tsx scripts/calibrar.ts && npx tsx scripts/familias.ts
 */
import { readFileSync } from 'node:fs';

import { rosterMechanicStyles } from '../src/data/expanded-roster';

interface Medida { id: string; nome: string; vitorias: number; lutas: number; taxa: number; danoMedio: number; curaMedia: number; protecaoMedia: number }
const dados = JSON.parse(readFileSync(process.argv[2] ?? 'docs/calibragem-250.json', 'utf8')) as { medidas: Medida[]; media: number };

const grupos = new Map<string, Medida[]>();
for (const m of dados.medidas) {
  const f = rosterMechanicStyles[m.id] ?? 'originais';
  grupos.set(f, [...(grupos.get(f) ?? []), m]);
}
const linhas = [...grupos].map(([f, ms]) => {
  const v = ms.reduce((s, m) => s + m.vitorias, 0), n = ms.reduce((s, m) => s + m.lutas, 0), t = v / n;
  const media = (k: 'danoMedio' | 'curaMedia' | 'protecaoMedia') => Math.round(ms.reduce((s, m) => s + m[k], 0) / ms.length);
  return { f, t, n, erro: Math.sqrt((t * (1 - t)) / n) * 196, qtd: ms.length, dano: media('danoMedio'), cura: media('curaMedia'), prot: media('protecaoMedia'),
    extremos: [...ms].sort((a, b) => b.taxa - a.taxa).map((m) => `${m.nome} ${(m.taxa * 100).toFixed(0)}`) };
}).sort((a, b) => b.t - a.t);

console.log(`média geral ${(dados.media * 100).toFixed(1)}%\n`);
for (const l of linhas) console.log(`${(l.t * 100).toFixed(1).padStart(5)}% ±${l.erro.toFixed(1).padStart(4)}  ${l.f.padEnd(11)} ${String(l.qtd).padStart(2)} pers · dano ${String(l.dano).padStart(5)} cura ${String(l.cura).padStart(4)} prot ${String(l.prot).padStart(4)} · ${l.extremos.join(', ')}`);
const ts = linhas.map((l) => l.t);
console.log(`\namplitude entre famílias: ${((Math.max(...ts) - Math.min(...ts)) * 100).toFixed(1)} pontos`);
