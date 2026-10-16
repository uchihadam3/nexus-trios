import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { byId } from '../src/data/characters';
import type { Battle } from '../src/engine/types';

/* O Light usa a Death Note em quem chegou a 100, mesmo imune (pedido do dono): o imune toma o dano e fica Exposto, uma vez só. */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
describe('Death Note em imune', () => {
  it('chegou a 100 num imune: usa a Death Note nele, dano e Exposto, e não repete', () => {
    const b = createBattle(['light', 'naruto', 'luffy'], ['goku', 'sasuke', 'batman'], 11);
    const light = quem(b, 'light'), goku = quem(b, 'goku');
    light.investigation[goku.uid] = 100; light.discovered = { [goku.uid]: 'immune' };
    for (const f of b.fighters) if (f.uid !== light.uid) f.statuses.push({ id: 'paralyzed', remaining: 999, intensity: 1, source: f.uid });
    light.skills[2]!.charge = 100;
    const vida = goku.hp;
    for (let t = 0; t < 400 && !light.sentencados?.[goku.uid]; t++) stepBattle(b);
    expect(light.sentencados?.[goku.uid]).toBe(true);
    expect(goku.hp).toBeLessThan(vida);
    expect(goku.hp).toBeGreaterThan(0);
    expect(goku.statuses.some((s) => s.id === 'exposed')).toBe(true);
    // e a Death Note recarrega na metade do tempo
    const nota = byId.light!.skills[2]!;
    expect(light.skills[2]!.cooldown).toBeGreaterThan(nota.cooldown * 0.5 - 0.5);
    expect(light.skills[2]!.cooldown).toBeLessThanOrEqual(nota.cooldown * 0.5);
  });
});
