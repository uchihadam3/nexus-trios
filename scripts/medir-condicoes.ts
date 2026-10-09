/*
 * Quão difícil é usar cada habilidade que tem condição (pedido do jogador:
 * "habilidades que têm condições… medir o quão difícil é… se for difícil de
 * usar, tem que ser mais forte").
 *
 * Simula lutas e mede, para cada habilidade, quanto tempo ela fica CHEIA e
 * pronta (Carga 100, sem Resfriamento) esperando a condição (aliado ferido,
 * rival em Preparo, alvo investigado…). Uma habilidade "sempre" sai assim que
 * enche; uma com condição difícil fica parada. A espera relativa (tempo cheia
 * esperando ÷ tempo de luta vivo), descontada a espera normal das habilidades
 * sem condição, vira um reforço de 0% a 40% no que a habilidade faz —
 * escrito em src/data/peso-da-condicao.ts e aplicado na ficha antes do
 * equilíbrio de força (que acerta o total do personagem).
 *
 * Uso: npx tsx scripts/medir-condicoes.ts <lutas>
 */
import { writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';

const lutas = Number(process.argv[2] ?? 4000);
const ids = characters.map((c) => c.id);
let r = 20261009 >>> 0;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
const chave = (id: string, i: number) => `${id}:${i}`;
const pronta = new Map<string, number>(), viva = new Map<string, number>(), usos = new Map<string, number>(), vezes = new Map<string, number>();
for (let n = 0; n < lutas; n++) {
  const seis = new Set<string>();
  while (seis.size < 6) seis.add(ids[Math.floor(rnd() * ids.length)]!);
  const [a1, a2, a3, b1, b2, b3] = [...seis];
  const b = createBattle([a1!, a2!, a3!], [b1!, b2!, b3!], Math.floor(rnd() * 2 ** 31), 1);
  for (let t = 0; t < 9000 && !b.finished; t++) {
    const antes = b.time;
    stepBattle(b);
    const dt = b.time - antes;
    for (const f of b.fighters) {
      if (f.hp <= 0) continue;
      f.skills.forEach((s, i) => {
        const k = chave(f.characterId, i);
        viva.set(k, (viva.get(k) ?? 0) + dt);
        if (s.charge >= 100 && s.cooldown <= 0 && f.cast?.skill !== i) pronta.set(k, (pronta.get(k) ?? 0) + dt);
      });
    }
  }
  for (const f of b.fighters) vezes.set(f.characterId, (vezes.get(f.characterId) ?? 0) + 1);
  for (const f of b.fighters) f.skills.forEach((s, i) => usos.set(chave(f.characterId, i), (usos.get(chave(f.characterId, i)) ?? 0) + s.uses));
}
const espera = (k: string) => (pronta.get(k) ?? 0) / Math.max(1, viva.get(k) ?? 1);
// a espera normal: a mediana das habilidades sem condição
const livres = characters.flatMap((c) => c.skills.map((s, i) => ({ s, k: chave(c.id, i) }))).filter(({ s }) => s.condition === 'always' && !s.requiresSkills?.length);
const normais = livres.map(({ k }) => espera(k)).sort((a, b) => a - b);
const base = normais[Math.floor(normais.length / 2)] ?? 0;
const peso: Record<string, number> = {};
const linhas: string[] = [];
for (const c of characters) c.skills.forEach((s, i) => {
  if (s.condition === 'always' && !s.requiresSkills?.length) return;
  const k = chave(c.id, i), e = espera(k);
  // cada 10 pontos de espera acima do normal = +10% (até +40%)
  const m = Math.round(Math.min(1.4, Math.max(1, 1 + (e - base))) * 100) / 100;
  if (m > 1) peso[k] = m;
  linhas.push(`${k.padEnd(26)} ${s.condition.padEnd(13)} espera ${(e * 100).toFixed(1).padStart(5)}%  usos/luta ${((usos.get(k) ?? 0) / Math.max(1, vezes.get(c.id) ?? 1)).toFixed(2)}  → ×${m}`);
});
console.log(`espera normal (habilidades sem condição): ${(base * 100).toFixed(1)}%`);
console.log(linhas.join('\n'));
writeFileSync(new URL('../src/data/peso-da-condicao.ts', import.meta.url), `/*
 * Reforço das habilidades com condição difícil (scripts/medir-condicoes.ts):
 * quanto mais tempo a habilidade fica cheia esperando a condição, mais forte
 * ela é quando sai. Medido em ${lutas} lutas; a espera normal das habilidades
 * sem condição é ${(base * 100).toFixed(1)}% do tempo de luta.
 */
export const PESO_DA_CONDICAO: Record<string, number> = {
${Object.entries(peso).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n')}
};
`);
