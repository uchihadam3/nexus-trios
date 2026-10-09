import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import type { Battle, Fighter } from '../src/engine/types';

/*
 * Reviver e Renascer (pedido do jogador: "levantar personagem caído").
 *   Reviver  — uma habilidade levanta um aliado caído com parte da Vida;
 *              quem levanta faz isso uma vez por luta, e cada lutador só volta uma vez.
 *   Renascer — quem tem volta sozinho depois de cair, uma vez por luta;
 *              a Death Note impede (execução não tem volta).
 */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const derruba = (_b: Battle, f: Fighter) => { f.hp = 0; f.statuses = []; f.shields = []; f.cast = null; };
const anda = (b: Battle, segundos: number, ate?: () => boolean) => {
  for (let t = 0; t < segundos * 10 && !b.finished; t++) { stepBattle(b); if (ate?.()) return; }
};
const revivedores = Object.values(byId).filter((c) => c.skills.some((s) => s.effects.some((e) => e.kind === 'revive')));
const renascem = Object.values(byId).filter((c) => c.renascer);

describe('Reviver', () => {
  it('existe em poucos personagens, e a habilidade diz o que faz', () => {
    expect(revivedores.length).toBeGreaterThanOrEqual(2);
    expect(revivedores.length).toBeLessThanOrEqual(10);
  });

  for (const c of revivedores) {
    it(`${c.name} levanta o aliado caído uma vez, com a Vida prometida`, () => {
      const indice = c.skills.findIndex((s) => s.effects.some((e) => e.kind === 'revive'));
      const fracao = (c.skills[indice]!.effects.find((e) => e.kind === 'revive') as { value: number }).value;
      const aliados = ['goku', 'naruto', 'luffy', 'batman'].filter((id) => id !== c.id && byId[id]).slice(0, 2);
      const b = createBattle([c.id, ...aliados], ['saitama', 'thanos', 'hulk'], 7);
      const eu = quem(b, c.id), caido = quem(b, aliados[0]!);
      // os rivais não fazem nada: só a habilidade de reviver importa aqui
      for (const r of b.fighters.filter((f) => f.side === 'enemy')) r.statuses.push({ id: 'paralyzed', remaining: 999, intensity: 1, source: r.uid });
      derruba(b, caido);
      eu.skills[indice]!.charge = 100;
      anda(b, 8, () => caido.hp > 0);
      expect(caido.hp).toBe(Math.round(caido.maxHp * fracao));
      expect(b.events.some((e) => e.kind === 'revive' && e.target === caido.uid && e.source === eu.uid)).toBe(true);
      // caiu de novo: não volta mais (e quem levantou não levanta outra vez)
      derruba(b, caido);
      eu.skills[indice]!.charge = 100; eu.skills[indice]!.cooldown = 0;
      anda(b, 8);
      expect(caido.hp).toBe(0);
    });
  }
});

describe('Renascer', () => {
  it('existe em poucos personagens', () => {
    expect(renascem.length).toBeGreaterThanOrEqual(3);
    expect(renascem.length).toBeLessThanOrEqual(12);
  });

  for (const c of renascem) {
    it(`${c.name} volta sozinho uma vez, depois do tempo prometido`, () => {
      const aliados = ['goku', 'naruto', 'batman'].filter((x) => x !== c.id).slice(0, 2);
      const b = createBattle([c.id, ...aliados], ['saitama', 'thanos', 'hulk'], 11);
      const eu = quem(b, c.id);
      // os aliados já caíram: o rival só tem ele para bater (e o trio não pode perder enquanto ele vai renascer)
      for (const f of b.fighters.filter((f) => f.side === 'player' && f.uid !== eu.uid)) derruba(b, f);
      eu.hp = 1;
      anda(b, 30, () => eu.hp <= 0);
      expect(eu.hp).toBe(0);
      expect(eu.renascendo).toBeGreaterThan(0);
      const caiuEm = b.time;
      for (const r of b.fighters.filter((f) => f.side === 'enemy')) r.statuses = [{ id: 'paralyzed', remaining: 999, intensity: 1, source: r.uid }];
      anda(b, c.renascer!.atraso + 1, () => eu.hp > 0);
      expect(eu.hp).toBe(Math.round(eu.maxHp * c.renascer!.vida));
      expect(b.time - caiuEm).toBeGreaterThanOrEqual(c.renascer!.atraso - 0.11);
      expect(b.events.some((e) => e.kind === 'revive' && e.target === eu.uid && e.source === eu.uid)).toBe(true);
    });
  }

  it('a Death Note impede o renascer', () => {
    const c = renascem[0]!;
    const b = createBattle(['light', 'goku', 'naruto'], [c.id, 'thanos', 'hulk'], 3);
    const light = quem(b, 'light'), alvo = quem(b, c.id);
    light.investigation[alvo.uid] = 100; light.discovered = { [alvo.uid]: 'vulnerable' };
    for (const f of b.fighters) if (f.uid !== light.uid) f.statuses.push({ id: 'paralyzed', remaining: 999, intensity: 1, source: f.uid });
    light.skills[2]!.charge = 100;
    anda(b, 12, () => alvo.hp <= 0);
    expect(alvo.hp).toBe(0);
    anda(b, 6);
    expect(alvo.hp).toBe(0);
    expect(alvo.renascendo ?? 0).toBe(0);
  });

  it('o trio não perde enquanto alguém ainda vai renascer', () => {
    const c = renascem[0]!;
    const b = createBattle([c.id, 'goku', 'naruto'], ['saitama', 'thanos', 'hulk'], 5);
    const eu = quem(b, c.id);
    for (const f of b.fighters.filter((f) => f.side === 'player' && f.uid !== eu.uid)) derruba(b, f);
    for (const r of b.fighters.filter((f) => f.side === 'enemy')) r.statuses.push({ id: 'paralyzed', remaining: 999, intensity: 1, source: r.uid });
    eu.hp = 1;
    const rival = b.fighters.find((f) => f.side === 'enemy')!;
    rival.statuses = [];
    anda(b, 30, () => eu.hp <= 0);
    expect(eu.hp).toBe(0);
    expect(b.finished).toBe(false);
    for (const r of b.fighters.filter((f) => f.side === 'enemy')) r.statuses = [{ id: 'paralyzed', remaining: 999, intensity: 1, source: r.uid }];
    anda(b, c.renascer!.atraso + 1, () => eu.hp > 0);
    expect(eu.hp).toBeGreaterThan(0);
    expect(b.finished).toBe(false);
  });
});
