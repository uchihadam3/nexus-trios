import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle } from '../src/engine/battle';
import type { Battle, StatusId } from '../src/engine/types';

/* Purificar tira debuffs dos aliados; Dissipar tira buffs dos rivais — os que mais pesam primeiro. */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const st = (id: StatusId, intensity = 0.2) => ({ id, remaining: 8, intensity, source: 'x' });
const nova = () => createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 13);
const elenco = Object.values(byId);

describe('Purificar e Dissipar', () => {
  it('estão numa parte do elenco', () => {
    for (const tipo of ['cleanse', 'dispel'] as const) {
      const n = elenco.filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === tipo))).length;
      expect(n, tipo).toBeGreaterThanOrEqual(4);
      expect(n, tipo).toBeLessThanOrEqual(12);
    }
  });

  it('Purificar tira primeiro o que trava (Paralisado antes de Lento) e deixa os buffs', () => {
    const b = nova(), goku = quem(b, 'goku'), naruto = quem(b, 'naruto');
    naruto.statuses = [st('slow'), st('paralyzed', 1), st('weakened'), st('haste')];
    applyEffects(b, goku, [naruto], [{ kind: 'cleanse', value: 2 }]);
    expect(naruto.statuses.map((s) => s.id).sort()).toEqual(['haste', 'weakened']);
    const e = b.events.find((x) => x.kind === 'cleanse')!;
    expect(e.removidos).toEqual(['paralyzed', 'slow']);
  });

  it('Purificar não age em rival; Dissipar não age em aliado', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta'), naruto = quem(b, 'naruto');
    vegeta.statuses = [st('slow')]; naruto.statuses = [st('protected')];
    applyEffects(b, goku, [vegeta], [{ kind: 'cleanse', value: 3 }]);
    applyEffects(b, goku, [naruto], [{ kind: 'dispel', value: 3 }]);
    expect(vegeta.statuses.length).toBe(1);
    expect(naruto.statuses.length).toBe(1);
  });

  it('Dissipar tira primeiro Protegido e Refletir, e não mexe no Escudo', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses = [st('regen', 10), st('reflect', 0.3), st('protected', 0.3), st('exposed')];
    vegeta.shields = [{ amount: 200, remaining: 8, source: vegeta.uid }];
    applyEffects(b, goku, [vegeta], [{ kind: 'dispel', value: 2 }]);
    expect(vegeta.statuses.map((s) => s.id).sort()).toEqual(['exposed', 'regen']);
    expect(vegeta.shields[0]!.amount).toBe(200);
  });

  it('sem nada para tirar, não acontece nada (nem aviso)', () => {
    const b = nova(), goku = quem(b, 'goku'), naruto = quem(b, 'naruto');
    naruto.statuses = [st('haste')];
    applyEffects(b, goku, [naruto], [{ kind: 'cleanse', value: 2 }]);
    expect(b.events.some((e) => e.kind === 'cleanse')).toBe(false);
  });
});
