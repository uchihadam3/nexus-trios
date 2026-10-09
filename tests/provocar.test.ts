import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { PROVOCAR } from '../src/data/mecanicas';
import { createBattle, stepBattle, targets } from '../src/engine/battle';
import type { Battle } from '../src/engine/types';

/*
 * Provocar: os rivais Provocados só conseguem mirar em quem provocou —
 * ataque básico e habilidades de um alvo. Golpes em todos seguem iguais, e a
 * provocação acaba se quem provocou cair.
 */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const provocadores = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'status' && e.status === 'provoked')));

describe('Provocar', () => {
  it('existe em poucos personagens, todos aguentando bastante', () => {
    expect(provocadores.length).toBeGreaterThanOrEqual(3);
    expect(provocadores.length).toBeLessThanOrEqual(8);
    const vidas = Object.values(byId).map((c) => c.hp).sort((a, b) => a - b);
    const mediana = vidas[Math.floor(vidas.length / 2)]!;
    for (const c of provocadores) expect(c.hp, c.name).toBeGreaterThan(mediana);
  });

  it('troca o Status antigo em vez de somar (o Hulk ruge sem o Lento)', () => {
    for (const [id, p] of Object.entries(PROVOCAR)) {
      const efeitos = byId[id]!.skills[p.habilidade]!.effects;
      expect(efeitos.some((e) => e.kind === 'status' && e.status === 'provoked'), id).toBe(true);
      if (p.troca) expect(efeitos.some((e) => e.kind === 'status' && e.status === p.troca), id).toBe(false);
    }
  });

  it('o rival Provocado só mira em quem provocou, em todo alvo único', () => {
    const b = createBattle(['hulk', 'sakura', 'naruto'], ['goku', 'vegeta', 'saitama'], 3);
    const hulk = quem(b, 'hulk'), goku = quem(b, 'goku');
    goku.statuses.push({ id: 'provoked', remaining: 30, intensity: 1, source: hulk.uid });
    for (const regra of ['enemyWeak', 'enemyStrong', 'randomEnemy'] as const) {
      expect(targets(b, goku, regra).map((f) => f.uid), regra).toEqual([hulk.uid]);
    }
    // golpe em todos continua em todos
    expect(targets(b, goku, 'allEnemies').length).toBe(3);
    // os ataques do Goku vão todos no Hulk enquanto durar
    for (let t = 0; t < 120; t++) stepBattle(b);
    const golpes = b.events.filter((e) => e.source === goku.uid && e.kind === 'damage' && e.target && e.target !== goku.uid);
    expect(golpes.length).toBeGreaterThan(0);
    const unicos = golpes.filter((e) => b.events.filter((x) => x.source === goku.uid && x.kind === 'damage' && Math.abs(x.time - e.time) < 1e-6).length === 1);
    for (const e of unicos) expect(e.target).toBe(hulk.uid);
  });

  it('se quem provocou cai, a provocação acaba', () => {
    const b = createBattle(['hulk', 'sakura', 'naruto'], ['goku', 'vegeta', 'saitama'], 3);
    const hulk = quem(b, 'hulk'), goku = quem(b, 'goku');
    goku.statuses.push({ id: 'provoked', remaining: 30, intensity: 1, source: hulk.uid });
    hulk.hp = 0;
    expect(targets(b, goku, 'enemyWeak').map((f) => f.uid)).not.toContain(hulk.uid);
  });

  it('a habilidade de provocar sai na luta e deixa os rivais Provocados', () => {
    for (const [id, p] of Object.entries(PROVOCAR)) {
      const b = createBattle([id, 'sakura', 'naruto'], ['goku', 'vegeta', 'saitama'], 9);
      const eu = quem(b, id);
      eu.skills[p.habilidade]!.charge = 100;
      if (id === 'bowser' || id === 'eren') eu.hp = Math.round(eu.maxHp * 0.5);
      if (id === 'captain') quem(b, 'sakura').hp = Math.round(quem(b, 'sakura').maxHp * 0.3);
      for (let t = 0; t < 80 && !b.events.some((e) => e.kind === 'status' && e.status === 'provoked'); t++) stepBattle(b);
      const provocados = b.events.filter((e) => e.kind === 'status' && e.status === 'provoked');
      expect(provocados.length, id).toBeGreaterThan(0);
      for (const e of provocados) expect(e.source, id).toBe(eu.uid);
    }
  });
});
