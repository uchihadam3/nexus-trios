import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { espelhar } from '../src/presentation/espelho';

/* PvP online: quem foi desafiado vê a mesma luta com o time dele embaixo. */
describe('Espelho da luta', () => {
  const b = createBattle(['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], 77);
  for (let i = 0; i < 400 && !b.finished; i++) stepBattle(b);
  const e = espelhar(b);
  it('troca os lados, os uids e o sinal da Vantagem', () => {
    const goku = e.fighters.find((f) => f.characterId === 'goku')!;
    expect(goku.side).toBe('enemy');
    expect(goku.uid).toBe('enemy-0');
    expect(e.fighters.find((f) => f.characterId === 'naruto')!.uid).toBe('player-0');
    expect(e.dominion).toBeCloseTo(-b.dominion);
    expect(e.combos?.player.map((c) => c.id)).toEqual(b.combos?.enemy.map((c) => c.id));
    const ev = b.events.find((x) => x.target)!, ev2 = e.events.find((x) => x.id === ev.id)!;
    expect(ev2.source).toBe(ev.source.startsWith('player') ? ev.source.replace('player', 'enemy') : ev.source.replace('enemy', 'player'));
  });
  it('espelhar duas vezes devolve a mesma luta', () => {
    expect(espelhar(e)).toEqual(JSON.parse(JSON.stringify(b)));
  });
  it('não mexe na luta original', () => {
    expect(b.fighters.find((f) => f.characterId === 'goku')!.side).toBe('player');
  });
});
