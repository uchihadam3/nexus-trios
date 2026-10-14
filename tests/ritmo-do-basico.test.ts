import { describe, it, expect } from 'vitest';
import { createBattle, intervaloDoBasico, stepBattle } from '../src/engine/battle';
import { byId } from '../src/data/characters';

/* O selo da velocidade do ataque básico (src/components/ArenaUnit.tsx) e a ficha usam esta conta: ela tem de bater com o
   ritmo de verdade da luta. */
describe('Velocidade do ataque básico', () => {
  it('parte do intervalo do personagem e muda com Acelerado, Lento e Congelado', () => {
    const b = createBattle(['goku', 'naruto', 'luffy'], ['vegeta', 'hinata', 'hulk'], 3);
    const goku = b.fighters.find((f) => f.characterId === 'goku')!;
    expect(intervaloDoBasico(b, goku)).toEqual({ agora: byId.goku.interval, base: byId.goku.interval });
    goku.statuses.push({ id: 'haste', intensity: 0.25, remaining: 5 } as never);
    expect(intervaloDoBasico(b, goku).agora).toBeCloseTo(byId.goku.interval / 1.25);
    goku.statuses = [{ id: 'slow', intensity: 0.2, remaining: 5 } as never];
    expect(intervaloDoBasico(b, goku).agora).toBeCloseTo(byId.goku.interval / 0.8);
    goku.statuses = [{ id: 'frozen', intensity: 0.1, remaining: 1 } as never];
    expect(intervaloDoBasico(b, goku).agora).toBeNull();
  });
  it('a base continua sendo o intervalo do personagem durante a luta', () => {
    const b = createBattle(['goku', 'naruto', 'luffy'], ['vegeta', 'hinata', 'hulk'], 5);
    const goku = b.fighters.find((f) => f.characterId === 'goku')!;
    const golpes: number[] = [];
    for (let t = 0; t < 400 && !b.finished; t++) {
      const antes = b.nextEvent;
      stepBattle(b);
      if (b.events.some((e) => e.id >= antes && e.kind === 'basic' && e.source === goku.uid)) golpes.push(b.time);
    }
    expect(golpes.length).toBeGreaterThan(1);
    expect(intervaloDoBasico(b, goku).base).toBe(byId.goku.interval);
  });
});
