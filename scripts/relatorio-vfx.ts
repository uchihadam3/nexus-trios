/*
 * Relatório das famílias de efeito (adendo, parte 3): quantas habilidades
 * caem em cada família, e a lista por personagem para conferir à mão.
 *
 * Uso: npx tsx scripts/relatorio-vfx.ts [--lista]
 */
import { characters } from '../src/data/characters';
import { FAMILIAS, profileFor, type VfxFamily } from '../src/presentation/vfxProfiles';

const conta = new Map<VfxFamily, number>(FAMILIAS.map((f) => [f, 0]));
const linhas: string[] = [];
let total = 0;
for (const c of characters) {
  const partes: string[] = [];
  for (const i of [undefined, 0, 1, 2] as const) {
    const p = profileFor(c.id, i)!;
    conta.set(p.family, (conta.get(p.family) ?? 0) + 1);
    total++;
    partes.push(`${i === undefined ? 'básico' : c.skills[i].name}=${p.family}${p.travel ? '→' : ''} ${p.color}`);
  }
  linhas.push(`${c.id.padEnd(16)} ${partes.join(' | ')}`);
}
if (process.argv.includes('--lista')) console.log(linhas.join('\n'));
const ordem = [...conta.entries()].sort((a, b) => b[1] - a[1]);
console.log(`\n${total} usos em ${FAMILIAS.length} famílias (${ordem.filter(([, n]) => n > 0).length} usadas)`);
for (const [f, n] of ordem) console.log(`${f.padEnd(18)} ${String(n).padStart(4)}  ${(100 * n / total).toFixed(1)}%`);
