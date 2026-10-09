import { readFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';
const antes: Record<string, number> = Object.fromEntries([...readFileSync('/tmp/claude-0/-home-user-Uchihadamclaude/587e0930-8cf2-5006-9d19-1177b0d51d37/scratchpad/forca-antes-final.ts', 'utf8').matchAll(/"([^"]+)": (-?[\d.]+),/g)].map((m) => [m[1]!, Number(m[2])]));
const pos = (f: Record<string, number>) => { const o = Object.keys(f).filter((k) => characters.some((c) => c.id === k)).sort((a, b) => f[b]! - f[a]!); return Object.fromEntries(o.map((k, i) => [k, i + 1])); };
const pa = pos(antes), pd = pos(FORCA as Record<string, number>);
const nome = (id: string) => characters.find((c) => c.id === id)!.name;
const linhas = characters.map((c) => ({ id: c.id, a: pa[c.id]!, d: pd[c.id]!, delta: pa[c.id]! - pd[c.id]! }));
console.log('PEDIDOS:'); for (const id of ['professorx', 'goku', 'saitama', 'light', 'itachi', 'jeangrey', 'cell']) { const l = linhas.find((x) => x.id === id)!; console.log(`  ${nome(id)}: ${l.a}º → ${l.d}º`); }
console.log('SUBIRAM MAIS:'); for (const l of [...linhas].sort((a, b) => b.delta - a.delta).slice(0, 10)) console.log(`  ${nome(l.id)}: ${l.a}º → ${l.d}º`);
console.log('CAÍRAM MAIS:'); for (const l of [...linhas].sort((a, b) => a.delta - b.delta).slice(0, 10)) console.log(`  ${nome(l.id)}: ${l.a}º → ${l.d}º`);
console.log('TOP 10 AGORA:'); for (const l of [...linhas].sort((a, b) => a.d - b.d).slice(0, 10)) console.log(`  ${l.d}º ${nome(l.id)} (era ${l.a}º)`);
console.log('ÚLTIMOS 5:'); for (const l of [...linhas].sort((a, b) => b.d - a.d).slice(0, 5)) console.log(`  ${l.d}º ${nome(l.id)} (era ${l.a}º)`);
const mudou = linhas.filter((l) => Math.abs(l.delta) >= 1).length; console.log('mudaram de posição:', mudou, 'média de deslocamento', (linhas.reduce((n, l) => n + Math.abs(l.delta), 0) / linhas.length).toFixed(1));
