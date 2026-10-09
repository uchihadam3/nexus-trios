import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle, stepBattle } from '../src/engine/battle';
import type { Battle } from '../src/engine/types';

/* Invocação: uma criatura ataca sozinha a cada 1,5 s enquanto o Status durar. */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const nova = () => {
  const b = createBattle(['megumi', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 17);
  for (const f of b.fighters) f.statuses.push({ id: 'paralyzed', remaining: 99, intensity: 1, source: f.uid });
  return b;
};

describe('Invocação', () => {
  it('está numa parte do elenco, cada um com o nome da sua criatura', () => {
    const quemInvoca = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'status' && e.status === 'summon')));
    expect(quemInvoca.length).toBeGreaterThanOrEqual(5);
    expect(quemInvoca.length).toBeLessThanOrEqual(12);
    for (const c of quemInvoca) expect(c.invocacao, c.name).toBeTruthy();
  });

  it('ataca a cada 1,5 s durante o tempo, mesmo com quem invocou travado', () => {
    const b = nova(), megumi = quem(b, 'megumi');
    applyEffects(b, megumi, [megumi], [{ kind: 'status', status: 'summon', value: 40, duration: 6 }]);
    for (let t = 0; t < 80; t++) stepBattle(b);
    const ataques = b.events.filter((e) => e.kind === 'summon' && e.source === megumi.uid);
    expect(ataques.length).toBe(4);
    expect(ataques.every((e) => e.label === 'Cão divino')).toBe(true);
  });

  it('some quando quem invocou cai, e Dissipar manda embora', () => {
    const b = nova(), megumi = quem(b, 'megumi'), vegeta = quem(b, 'vegeta');
    applyEffects(b, megumi, [megumi], [{ kind: 'status', status: 'summon', value: 40, duration: 9 }]);
    applyEffects(b, vegeta, [megumi], [{ kind: 'dispel', value: 1 }]);
    expect(megumi.statuses.some((s) => s.id === 'summon')).toBe(false);
    applyEffects(b, megumi, [megumi], [{ kind: 'status', status: 'summon', value: 40, duration: 9 }]);
    megumi.hp = 1; applyEffects(b, vegeta, [megumi], [{ kind: 'damage', value: 9999 }]);
    const n = b.events.filter((e) => e.kind === 'summon').length;
    for (let t = 0; t < 40; t++) stepBattle(b);
    expect(b.events.filter((e) => e.kind === 'summon').length).toBe(n);
  });
});
