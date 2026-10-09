import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle, stepBattle } from '../src/engine/battle';
import type { Battle, Character, StatusId } from '../src/engine/types';

/*
 * Roubo de vida (da habilidade), Vampirismo (Status: todo golpe cura),
 * Refletir (devolve % do golpe) e Espinhos (dano fixo por golpe em quem bate).
 */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const comStatus = (s: StatusId) => (c: Character) => c.skills.some((k) => k.effects.some((e) => e.kind === 'status' && e.status === s));
const elenco = Object.values(byId);
const nova = () => createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 21);
const st = (id: StatusId, intensity: number, source = 'x') => ({ id, remaining: 30, intensity, source });

describe('quem tem cada mecânica', () => {
  it('cada uma está numa parte do elenco, nem em quase ninguém nem em todo mundo', () => {
    const roubo = elenco.filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'lifesteal')));
    for (const [nome, lista] of [['Roubo de vida', roubo], ['Vampirismo', elenco.filter(comStatus('vampirism'))], ['Refletir', elenco.filter(comStatus('reflect'))], ['Espinhos', elenco.filter(comStatus('thorns'))]] as const) {
      expect(lista.length, nome).toBeGreaterThanOrEqual(4);
      expect(lista.length, nome).toBeLessThanOrEqual(12);
    }
  });
});

describe('Roubo de vida', () => {
  it('cura quem age na fração do dano que a habilidade causou', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    goku.hp = 500;
    const antes = vegeta.hp;
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 200 }, { kind: 'lifesteal', value: 0.5 }]);
    const causado = antes - vegeta.hp;
    expect(causado).toBeGreaterThan(0);
    expect(goku.hp).toBeCloseTo(500 + causado * 0.5, 5);
    expect(b.events.some((e) => e.kind === 'heal' && e.label === 'Roubo de vida')).toBe(true);
  });
});

describe('Vampirismo', () => {
  it('golpe direto cura; Queimadura não', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    goku.hp = 500; goku.statuses.push(st('vampirism', 0.3));
    const antes = vegeta.hp;
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 200 }]);
    expect(goku.hp).toBeCloseTo(500 + (antes - vegeta.hp) * 0.3, 5);
    const hp = goku.hp;
    vegeta.statuses.push({ id: 'burning', remaining: 3, intensity: 20, source: goku.uid });
    for (const f of b.fighters) if (f.uid !== vegeta.uid) f.statuses.push(st('paralyzed', 1));
    vegeta.statuses.push(st('paralyzed', 1));
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(goku.hp).toBeCloseTo(hp, 5);
  });
});

describe('Refletir e Espinhos', () => {
  it('Refletir devolve a fração do golpe (antes do Escudo) para quem bateu', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses.push(st('reflect', 0.4, vegeta.uid));
    vegeta.shields.push({ amount: 1000, remaining: 10, source: vegeta.uid });
    const antes = goku.hp;
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 200 }]);
    expect(antes - goku.hp).toBeCloseTo(200 * 0.4, 0);
    expect(b.events.some((e) => e.kind === 'damage' && e.label === 'Refletido' && e.target === goku.uid)).toBe(true);
  });

  it('dois com Refletir não devolvem para sempre', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    goku.statuses.push(st('reflect', 0.6, goku.uid)); vegeta.statuses.push(st('reflect', 0.6, vegeta.uid));
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 200 }]);
    expect(b.events.filter((e) => e.label === 'Refletido').length).toBe(1);
  });

  it('Espinhos fere quem bate a cada golpe, inclusive em área', () => {
    const b = nova(), goku = quem(b, 'goku');
    const rivais = b.fighters.filter((f) => f.side === 'enemy');
    for (const r of rivais) r.statuses.push(st('thorns', 15, r.uid));
    const antes = goku.hp;
    applyEffects(b, goku, rivais, [{ kind: 'damage', value: 100 }]);
    expect(antes - goku.hp).toBeCloseTo(15 * 3, 0);
    expect(b.events.filter((e) => e.label === 'Espinhos').length).toBe(3);
  });

  it('Queimadura não acorda Refletir nem Espinhos', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses.push(st('reflect', 0.5, vegeta.uid), st('thorns', 20, vegeta.uid), { id: 'burning', remaining: 3, intensity: 20, source: goku.uid });
    for (const f of b.fighters) f.statuses.push(st('paralyzed', 1));
    const antes = goku.hp;
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(goku.hp).toBe(antes);
  });
});
