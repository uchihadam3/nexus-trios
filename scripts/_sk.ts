import { characters } from '../src/data/characters';
const RIVAL = ['enemyWeak','enemyStrong','enemyCast','investigated','leastInvestigated','allEnemies','randomEnemy'];
for (const c of characters) c.skills.forEach((s, i) => {
  const dano = s.effects.some((e) => (e.kind === 'damage' || e.kind === 'deathnote') && RIVAL.includes(e.target ?? s.target));
  if (dano) return;
  const o = s.effects.map((e) => e.kind === 'status' ? e.status : e.kind).join(',');
  console.log(`${c.id}:${i} ${s.name} → ${o}`);
});
