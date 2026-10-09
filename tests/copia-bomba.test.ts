import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle, stepBattle } from '../src/engine/battle';
import type { Battle } from '../src/engine/types';

/* Marca explosiva (bomba-relógio que soma) e Copiar habilidade (usa a última habilidade de um rival). */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const paraTodos = (b: Battle) => { for (const f of b.fighters) f.statuses.push({ id: 'paralyzed', remaining: 99, intensity: 1, source: f.uid }); };

describe('Marca explosiva', () => {
  it('explode no fim do tempo com o dano somado', () => {
    const b = createBattle(['gambit', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 5);
    const gambit = quem(b, 'gambit'), vegeta = quem(b, 'vegeta');
    paraTodos(b);
    applyEffects(b, gambit, [vegeta], [{ kind: 'status', status: 'bomb', value: 100, duration: 2 }, { kind: 'status', status: 'bomb', value: 50, duration: 2 }]);
    const vida = vegeta.hp;
    for (let t = 0; t < 15; t++) stepBattle(b);
    expect(vegeta.hp).toBe(vida); // ainda não deu o tempo
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(vida - vegeta.hp).toBeCloseTo(150, 0);
    expect(b.events.filter((e) => e.label === 'Explosão').length).toBe(1);
    expect(vegeta.statuses.some((s) => s.id === 'bomb')).toBe(false);
  });

  it('Purificar desarma a bomba', () => {
    const b = createBattle(['gambit', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 5);
    const gambit = quem(b, 'gambit'), vegeta = quem(b, 'vegeta'), hulk = quem(b, 'hulk');
    paraTodos(b);
    applyEffects(b, gambit, [vegeta], [{ kind: 'status', status: 'bomb', value: 100, duration: 2 }]);
    // tira o Paralisado (que este teste pôs) e a bomba
    applyEffects(b, hulk, [vegeta], [{ kind: 'cleanse', value: 2 }]);
    expect(vegeta.statuses.some((s) => s.id === 'bomb')).toBe(false);
    const vida = vegeta.hp;
    for (let t = 0; t < 25; t++) stepBattle(b);
    expect(vegeta.hp).toBe(vida);
  });

  it('está em alguns personagens', () => {
    const n = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'status' && e.status === 'bomb'))).length;
    expect(n).toBeGreaterThanOrEqual(3);
    expect(n).toBeLessThanOrEqual(10);
  });
});

describe('Copiar habilidade', () => {
  it('usa a última habilidade de um rival, do lado de quem copiou e com a fração da força', () => {
    const b = createBattle(['kakashi', 'naruto', 'sakura'], ['goku', 'hulk', 'thor'], 9);
    const kakashi = quem(b, 'kakashi'), goku = quem(b, 'goku');
    paraTodos(b);
    b.events.push({ id: b.nextEvent++, time: b.time, kind: 'skill', source: goku.uid, skill: 0, label: 'Kamehameha' });
    const vidas = b.fighters.filter((f) => f.side === 'enemy').map((f) => f.hp);
    applyEffects(b, kakashi, [], [{ kind: 'copy', value: 0.8 }]);
    expect(b.events.some((e) => e.kind === 'copy' && e.label.includes('Kamehameha') && e.source === kakashi.uid)).toBe(true);
    const depois = b.fighters.filter((f) => f.side === 'enemy').map((f) => f.hp);
    expect(depois.some((v, i) => v < vidas[i]!)).toBe(true);
    // não acerta o próprio trio
    for (const f of b.fighters.filter((f) => f.side === 'player')) expect(f.hp).toBe(f.maxHp);
  });

  it('sem habilidade rival para copiar, não faz nada', () => {
    const b = createBattle(['kakashi', 'naruto', 'sakura'], ['goku', 'hulk', 'thor'], 9);
    applyEffects(b, quem(b, 'kakashi'), [], [{ kind: 'copy', value: 0.8 }]);
    expect(b.events.some((e) => e.kind === 'copy')).toBe(false);
  });

  it('está em poucos personagens', () => {
    const n = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'copy'))).length;
    expect(n).toBeGreaterThanOrEqual(3);
    expect(n).toBeLessThanOrEqual(8);
  });
});
