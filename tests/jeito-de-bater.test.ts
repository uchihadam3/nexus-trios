import { describe, expect, it } from 'vitest';
import { byId, characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { textoDoJeito } from '../src/engine/skill-descriptions';
import type { Battle, BattleEvent, Fighter } from '../src/engine/types';

/*
 * O jeito de bater (pedido do jogador: "o ataque básico também…
 * individualidade pros personagens"). Cada ataque básico tem nome próprio, e
 * quem tem jeito de bater faz o que a ficha diz.
 */
const quem = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
// só o básico: ninguém usa habilidade, e os rivais ficam parados
const soBasico = (b: Battle, eu: Fighter) => {
  for (const f of b.fighters) {
    f.statuses.push({ id: 'silenced', remaining: 999, intensity: 1, source: f.uid });
    if (f.side !== eu.side) f.statuses.push({ id: 'paralyzed', remaining: 999, intensity: 1, source: f.uid });
  }
};
// a luta guarda só os eventos mais recentes: junta tudo o que aconteceu, passo a passo
const golpes = (b: Battle, eu: Fighter, n: number): BattleEvent[] => {
  const todos: BattleEvent[] = [];
  let visto = b.nextEvent;
  for (let t = 0; t < 4000 && (eu.golpes ?? 0) < n && !b.finished; t++) {
    stepBattle(b);
    todos.push(...b.events.filter((e) => e.id >= visto));
    visto = b.nextEvent;
  }
  return todos;
};

describe('Ataque básico com nome e jeito próprios', () => {
  it('os 250 têm nome próprio, todos diferentes', () => {
    const nomes = characters.map((c) => c.basic.name);
    expect(nomes.every((n) => n && n !== 'Ataque básico')).toBe(true);
    expect(new Set(nomes).size).toBe(characters.length);
  });
  it('a maior parte bate do seu jeito, e todo jeito se explica na ficha', () => {
    const com = characters.filter((c) => c.basic.jeito);
    expect(com.length).toBeGreaterThanOrEqual(120);
    for (const c of com) expect(textoDoJeito(c.basic.jeito!).length, c.id).toBeGreaterThan(15);
    const tipos = new Set(com.map((c) => c.basic.jeito!.tipo));
    expect([...tipos].sort()).toEqual(['acelera', 'cura', 'escudo', 'largo', 'ricochete', 'rouba', 'serie']);
  });

  it('série: o 3º golpe do Naruto sai especial e bate mais forte', () => {
    const b = createBattle(['naruto', 'sakura', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'naruto');
    soBasico(b, eu);
    const meus = golpes(b, eu, 3).filter((e) => e.kind === 'basic' && e.source === eu.uid);
    expect(meus[2]!.label).toBe('Rendan Uzumaki');
    expect(meus[0]!.label).toBe('Combo do clone');
  });
  it('ricochete: o escudo do Capitão quica no segundo rival', () => {
    const b = createBattle(['captain', 'sakura', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'captain');
    soBasico(b, eu);
    golpes(b, eu, 1);
    const quique = b.events.find((e) => e.kind === 'damage' && e.source === eu.uid && e.label === 'Ricochete');
    const golpe = b.events.find((e) => e.kind === 'basic' && e.source === eu.uid)!;
    expect(quique).toBeDefined();
    expect(quique!.target).not.toBe(golpe.target);
  });
  it('largo: o Hulk pega dois', () => {
    const b = createBattle(['hulk', 'sakura', 'goku'], ['captain', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'hulk');
    soBasico(b, eu);
    golpes(b, eu, 1);
    expect(b.events.some((e) => e.kind === 'damage' && e.source === eu.uid && e.label === 'Golpe largo')).toBe(true);
  });
  it('cura: o soco da Sakura cura o aliado mais ferido', () => {
    const b = createBattle(['sakura', 'naruto', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'sakura'), ferido = quem(b, 'naruto');
    soBasico(b, eu);
    ferido.hp = ferido.maxHp * 0.4;
    golpes(b, eu, 1);
    expect(b.events.some((e) => e.kind === 'heal' && e.source === eu.uid && e.target === ferido.uid && e.label === 'Golpe que cura')).toBe(true);
  });
  it('escudo: o golpe do Alphonse vira Escudo nele', () => {
    const b = createBattle(['alphonse', 'naruto', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'alphonse');
    soBasico(b, eu);
    golpes(b, eu, 1);
    expect(eu.shields.reduce((n, s) => n + s.amount, 0)).toBeGreaterThan(0);
  });
  it('rouba: o Kakashi tira Carga do rival e põe na habilidade dele', () => {
    const b = createBattle(['kakashi', 'naruto', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'kakashi');
    soBasico(b, eu);
    for (const r of b.fighters.filter((f) => f.side === 'enemy')) for (const s of r.skills) s.charge = 50;
    for (const s of eu.skills) s.charge = 0;
    const ev = golpes(b, eu, 1);
    const roubo = ev.find((e) => e.kind === 'charge' && e.source === eu.uid && e.label === 'Roubou Carga');
    expect(roubo?.value).toBe((byId.kakashi!.basic.jeito as { valor: number }).valor);
    expect(Math.max(...eu.skills.map((s) => s.charge))).toBeGreaterThanOrEqual(roubo!.value!);
  });
  it('acelera: cada golpe do Flash adianta a próxima ação', () => {
    const b = createBattle(['flash', 'naruto', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
    const eu = quem(b, 'flash');
    soBasico(b, eu);
    golpes(b, eu, 1);
    // logo depois do golpe a barra já começa adiantada
    expect(eu.action).toBeGreaterThanOrEqual((byId.flash!.basic.jeito as { valor: number }).valor - 0.05);
  });
});
