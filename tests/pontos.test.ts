import { describe, expect, it } from 'vitest';
import { replayRanked } from '../src/engine/ranked';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { pontosDaJornada, pontosDaLuta } from '../src/engine/pontos';
import { characters } from '../src/data/characters';

/* Os pontos que a tela mostra depois de cada luta são exatamente os do ranking. */
describe('pontos', () => {
  it('a soma das lutas bate com a pontuação validada pelo servidor', () => {
    let conferidas = 0;
    for (const seed of [11, 202, 3003, 40004, 500005]) {
      const rivais = new Set(generateCampaign(seed).flatMap((e) => e.team));
      const trio = characters.map((c) => c.id).filter((id) => !rivais.has(id)).slice(seed % 40, seed % 40 + 3);
      const oficial = replayRanked(trio, seed);
      const lutas: { pontos: number; won: boolean }[] = [];
      for (const [index, encontro] of generateCampaign(seed).entries()) {
        const b = createBattle(trio, encontro.team, seed + index * 7919, encontro.scale);
        for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
        const p = pontosDaLuta(b, index);
        lutas.push({ pontos: p.total, won: b.winner === 'player' });
        if (b.winner !== 'player') break;
      }
      expect(pontosDaJornada(lutas)).toBe(oficial.score);
      // a luta perdida também pontua (o que o trio fez nela), e cada luta cabe na escala de dezenas de milhares
      for (const l of lutas) { expect(l.pontos).toBeGreaterThan(0); expect(l.pontos).toBeLessThan(400_000); }
      conferidas += lutas.length;
    }
    expect(conferidas).toBeGreaterThan(5);
  }, 60000);
});
