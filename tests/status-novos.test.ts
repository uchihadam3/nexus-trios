import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { applyEffects, createBattle, stepBattle } from '../src/engine/battle';
import type { Battle, StatusId } from '../src/engine/types';

/* Os sete Status da parte 5, cada um com o seu jeito. */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const nova = () => createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 31);
const st = (id: StatusId, intensity: number, remaining = 8, source = 'x') => ({ id, remaining, intensity, source });
const paraTodos = (b: Battle, menos: string[] = []) => { for (const f of b.fighters) if (!menos.includes(f.uid)) f.statuses.push(st('paralyzed', 1, 99)); };

describe('Status novos', () => {
  it('Envenenado tira Vida por segundo e passa por Escudo e Protegido', () => {
    const b = nova(), vegeta = quem(b, 'vegeta');
    paraTodos(b);
    vegeta.statuses.push(st('poison', 10, 3, quem(b, 'goku').uid), st('protected', 0.5));
    vegeta.shields.push({ amount: 999, remaining: 9, source: vegeta.uid });
    const antes = vegeta.hp;
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(antes - vegeta.hp).toBeCloseTo(10, 0);
    expect(vegeta.shields[0]!.amount).toBe(999);
  });

  it('Sangrando perde Vida a cada ação, parado não', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    goku.statuses.push(st('bleed', 30, 30, vegeta.uid));
    paraTodos(b, [goku.uid]);
    goku.skills.forEach((s) => { s.charge = 0; });
    const antes = goku.hp;
    let acoes = 0;
    for (let t = 0; t < 80; t++) { const n = b.events.length; stepBattle(b); acoes += b.events.slice(n).filter((e) => e.source === goku.uid && (e.kind === 'basic' || e.kind === 'skill')).length; }
    expect(acoes).toBeGreaterThan(0);
    expect(antes - goku.hp).toBeCloseTo(30 * acoes, 0);
  });

  it('Amaldiçoado recebe menos cura e menos Escudo', () => {
    const b = nova(), goku = quem(b, 'goku'), naruto = quem(b, 'naruto');
    naruto.hp = 300; naruto.statuses.push(st('cursed', 0.4));
    applyEffects(b, goku, [naruto], [{ kind: 'heal', value: 100 }, { kind: 'shield', value: 100 }]);
    expect(naruto.hp).toBeCloseTo(360, 5);
    expect(naruto.shields.reduce((n, s) => n + s.amount, 0)).toBeCloseTo(60, 5);
  });

  it('Congelado não age; o golpe que quebra o gelo entra mais forte', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses.push(st('frozen', 0.3, 5));
    vegeta.action = 0.99;
    for (const f of b.fighters) if (f.uid !== vegeta.uid) f.statuses.push(st('paralyzed', 1, 99));
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(b.events.some((e) => e.source === vegeta.uid && e.kind === 'basic')).toBe(false);
    const vida = vegeta.hp;
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 100 }]);
    const normal = createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 31);
    const v2 = quem(normal, 'vegeta'), vida2 = v2.hp;
    applyEffects(normal, quem(normal, 'goku'), [v2], [{ kind: 'damage', value: 100 }]);
    expect((vida - vegeta.hp) / (vida2 - v2.hp)).toBeCloseTo(1.3, 2);
    expect(vegeta.statuses.some((s) => s.id === 'frozen')).toBe(false);
  });

  it('Dormindo acorda com golpe direto, não com Queimadura', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses.push(st('sleep', 1, 20), { id: 'burning', remaining: 3, intensity: 10, source: goku.uid });
    paraTodos(b, [vegeta.uid]);
    for (let t = 0; t < 10; t++) stepBattle(b);
    expect(vegeta.statuses.some((s) => s.id === 'sleep')).toBe(true);
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 50 }]);
    expect(vegeta.statuses.some((s) => s.id === 'sleep')).toBe(false);
  });

  it('Cego erra parte dos ataques básicos', () => {
    const b = nova(), goku = quem(b, 'goku');
    goku.statuses.push(st('blind', 0.6, 999));
    paraTodos(b, [goku.uid]);
    goku.skills.forEach((s) => { s.charge = -1e9; });
    for (let t = 0; t < 600; t++) stepBattle(b);
    const golpes = b.events.filter((e) => e.source === goku.uid && e.kind === 'basic').length;
    const erros = b.events.filter((e) => e.source === goku.uid && e.kind === 'miss').length;
    expect(golpes).toBeGreaterThan(5);
    expect(erros / golpes).toBeGreaterThan(0.3);
    expect(erros / golpes).toBeLessThan(0.9);
  });

  it('Barreira anula o próximo debuff de rival e se gasta', () => {
    const b = nova(), goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    goku.statuses.push(st('barrier', 1, 8, goku.uid));
    applyEffects(b, vegeta, [goku], [{ kind: 'status', status: 'slow', value: 0.3, duration: 5 }]);
    expect(goku.statuses.some((s) => s.id === 'slow')).toBe(false);
    expect(goku.statuses.some((s) => s.id === 'barrier')).toBe(false);
    expect(b.events.some((e) => e.kind === 'resist' && e.target === goku.uid)).toBe(true);
    applyEffects(b, vegeta, [goku], [{ kind: 'status', status: 'slow', value: 0.3, duration: 5 }]);
    expect(goku.statuses.some((s) => s.id === 'slow')).toBe(true);
  });
});

describe('debuff miúdo saiu e cada um tem a sua marca', () => {
  it('nenhum ataque básico põe debuff miúdo; gelo não queima', () => {
    for (const c of Object.values(byId)) for (const e of c.basic.effects)
      if (e.kind === 'status' && !['burning', 'poison', 'bleed'].includes(e.status)) expect(['protected', 'haste', 'regen', 'strengthened'].includes(e.status) || e.value > 0.08, `${c.name}: ${e.status} ${e.value}`).toBe(true);
    for (const id of ['subzero', 'hyoga', 'rukia', 'camus', 'frozone']) for (const s of byId[id]!.skills)
      expect(s.effects.some((e) => e.kind === 'status' && e.status === 'burning'), `${id} · ${s.name}`).toBe(false);
  });

  it('cada Status novo está em alguns personagens', () => {
    const tem = (s: StatusId) => Object.values(byId).filter((c) => c.skills.some((k) => k.effects.some((e) => e.kind === 'status' && e.status === s))).length;
    for (const s of ['poison', 'bleed', 'cursed', 'frozen', 'sleep', 'blind', 'barrier'] as StatusId[]) {
      expect(tem(s), s).toBeGreaterThanOrEqual(3);
      expect(tem(s), s).toBeLessThanOrEqual(10);
    }
  });
});

describe('Marcado (regra nova)', () => {
  it('não passa pelo Escudo', () => {
    const b = createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 31);
    const goku = quem(b, 'goku'), vegeta = quem(b, 'vegeta');
    vegeta.statuses.push(st('marked', 0.2, 8, goku.uid));
    vegeta.shields.push({ amount: 500, remaining: 9, source: vegeta.uid });
    const vida = vegeta.hp;
    applyEffects(b, goku, [vegeta], [{ kind: 'damage', value: 100 }]);
    expect(vegeta.hp).toBe(vida);
    expect(vegeta.shields[0]!.amount).toBeLessThan(500);
  });

  it('quem marca escolhe o rival que cai mais rápido e evita quem já está marcado', async () => {
    const { targets } = await import('../src/engine/battle');
    const b = createBattle(['goku', 'naruto', 'sakura'], ['vegeta', 'hulk', 'thor'], 31);
    const goku = quem(b, 'goku'), hulk = quem(b, 'hulk'), thor = quem(b, 'thor');
    hulk.hp = 200;
    expect(targets(b, goku, 'enemyStrong', [{ kind: 'status', status: 'marked', value: 0.2, duration: 8 }]).map((f) => f.uid)).toEqual([hulk.uid]);
    hulk.statuses.push(st('marked', 0.2, 8, goku.uid)); thor.hp = 400;
    expect(targets(b, goku, 'enemyStrong', [{ kind: 'status', status: 'marked', value: 0.2, duration: 8 }]).map((f) => f.uid)).toEqual([thor.uid]);
  });
});
