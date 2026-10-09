import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle } from '../src/engine/battle';
import type { Battle } from '../src/engine/types';

/* Esquiva (escapa do golpe inteiro) e Última resistência (o golpe fatal deixa com 1 de Vida, uma vez). */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;

describe('Esquiva', () => {
  it('está numa parte do elenco', () => {
    const n = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'status' && e.status === 'evasion'))).length;
    expect(n).toBeGreaterThanOrEqual(5);
    expect(n).toBeLessThanOrEqual(12);
  });

  it('quem esquiva não leva nem o dano nem o debuff daquele golpe; às vezes leva', () => {
    let escapou = 0, levou = 0;
    for (let seed = 1; seed <= 60; seed++) {
      const b = createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], seed);
      const goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
      vegeta.statuses.push({ id: 'evasion', remaining: 9, intensity: 0.5, source: vegeta.uid });
      const vida = vegeta.hp;
      applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 100 }, { kind: 'status', status: 'slow', value: 0.3, duration: 5 }]);
      const esquivou = b.events.some((e) => e.kind === 'miss' && e.label === 'Esquivou' && e.target === vegeta.uid);
      if (esquivou) { escapou++; expect(vegeta.hp).toBe(vida); expect(vegeta.statuses.some((s) => s.id === 'slow')).toBe(false); }
      else { levou++; expect(vegeta.hp).toBeLessThan(vida); }
    }
    expect(escapou).toBeGreaterThan(15);
    expect(levou).toBeGreaterThan(15);
  });
});

describe('Última resistência', () => {
  const comResistencia = Object.values(byId).filter((c) => c.ultimaResistencia);
  it('está em poucos personagens', () => {
    expect(comResistencia.length).toBeGreaterThanOrEqual(4);
    expect(comResistencia.length).toBeLessThanOrEqual(10);
  });

  for (const c of comResistencia) {
    it(`${c.name}: o golpe fatal deixa com 1 de Vida e Protegido, só uma vez`, () => {
      const b = createBattle([c.id, 'sakura', 'gojo'], ['vegeta', 'hulk', 'thor'], 3);
      const eu = quem(b, c.id), rival = quem(b, 'vegeta');
      eu.hp = 50; eu.shields = []; eu.statuses = [];
      applyEffects(b, rival, [eu], [{ kind: 'damage', value: 9999 }]);
      expect(eu.hp).toBe(1);
      expect(eu.statuses.some((s) => s.id === 'protected')).toBe(true);
      expect(b.events.some((e) => e.kind === 'resist' && e.label === 'Última resistência')).toBe(true);
      eu.statuses = [];
      applyEffects(b, rival, [eu], [{ kind: 'damage', value: 9999 }]);
      expect(eu.hp).toBe(0);
    });
  }
});
