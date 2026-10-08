/*
 * O que restou da progressão depois que conquistas, Maestria e XP saíram do
 * jogo (o objetivo agora é fazer pontos e subir no ranking): o perfil antigo
 * migra sem perder jornadas e recordes, e a contagem de eventos que o
 * servidor do ranking usa continua certa.
 */
import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { emptyTally, tallyEvents } from '../src/engine/progression';
import { loadProfile } from '../src/lib/storage';

describe('perfil e contagem de eventos', () => {
  it('migra o perfil antigo: jornadas e recordes ficam, conquistas e Maestria saem', () => {
    const antigo = {
      journeys: 9, victories: 2, best: 10, wins: 37, champion: ['goku', 'vegeta', 'pikachu'],
      progress: { xp: 4200, title: 'Veterano', seen: ['goku'], unlocked: ['j-primeiro'], stats: { battles: 50 }, mastery: { goku: { usou: 9 } } },
    };
    const memoria = new Map([['nexus-v1-profile', JSON.stringify(antigo)]]);
    (globalThis as { localStorage?: unknown }).localStorage = { getItem: (k: string) => memoria.get(k) ?? null };
    const p = loadProfile();
    expect(p.journeys).toBe(9);
    expect(p.best).toBe(10);
    expect(p.victories).toBe(2);
    expect(p.champion).toEqual(['goku', 'vegeta', 'pikachu']);
    expect(p.recordePontos).toBe(0);
    expect((p as unknown as { progress?: unknown }).progress).toBeUndefined();
  });

  it('conta viradas, interrupções e Status do trio sem contar o mesmo evento duas vezes', () => {
    const b = createBattle(['pikachu', 'rukia', 'scarletwitch'], ['goku', 'vegeta', 'hulk'], 5);
    let t = emptyTally();
    for (let i = 0; i < 4000 && !b.finished; i++) { stepBattle(b); t = tallyEvents(t, b.events); t = tallyEvents(t, b.events); }
    expect(b.finished).toBe(true);
    expect(t.turns).toBe(b.viradasDoTrio ?? 0);
    expect(t.statuses + t.interrupts).toBeGreaterThan(0);
  });
});
