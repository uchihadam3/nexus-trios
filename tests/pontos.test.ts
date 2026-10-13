import { describe, expect, it } from 'vitest';
import { replayRanked } from '../src/engine/ranked';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { APOIO, LUTA, apoioDaLuta, feitosDaLuta, pontosDaJornada, pontosDaLuta } from '../src/engine/pontos';
import { characters } from '../src/data/characters';
import { FATOR_DE_PONTOS } from '../src/data/pontos-por-personagem';

/* Os pontos que a tela mostra depois de cada luta são exatamente os do ranking. */
describe('pontos', () => {
  it('a soma das lutas bate com a pontuação validada pelo servidor', () => {
    let conferidas = 0;
    for (const seed of [11, 202, 3003, 40004, 500005, 61, 707, 8008, 90009, 1234567]) {
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
    expect(conferidas).toBeGreaterThan(10);
  }, 60000);

  it('cura e proteção contam inteiras numa luta normal e só um pouco do que passa disso', () => {
    expect(apoioDaLuta(5_000)).toBe(5_000);
    expect(apoioDaLuta(APOIO.cheio)).toBe(APOIO.cheio);
    // o trio de três curandeiros (uns 58 mil por luta) passa a contar menos da metade
    expect(apoioDaLuta(58_000)).toBeCloseTo(APOIO.cheio + 43_000 * APOIO.acima);
    expect(apoioDaLuta(58_000) / 58_000).toBeLessThan(0.5);
  });

  it('a luta que se arrasta não rende feitos sem fim', () => {
    expect(feitosDaLuta(30_000)).toBe(30_000);
    expect(feitosDaLuta(LUTA.cheio)).toBe(LUTA.cheio);
    // a luta de 200 s do trio de curandeiros (uns 180 mil de feitos) passa a contar pouco mais que uma luta cheia
    expect(feitosDaLuta(180_000)).toBeCloseTo(LUTA.cheio + 135_000 * LUTA.acima);
    expect(feitosDaLuta(180_000)).toBeLessThan(2 * LUTA.cheio);
  });

  it('todo personagem tem o seu fator de pontos, dentro do limite (rode scripts/equilibrar-pontos.ts se mudar o elenco)', () => {
    for (const c of characters) {
      expect(FATOR_DE_PONTOS[c.id], c.id).toBeDefined();
      // os mesmos limites de scripts/equilibrar-pontos.ts (medido pela fatia nos pontos do trio)
      expect(FATOR_DE_PONTOS[c.id]).toBeGreaterThanOrEqual(0.3);
      expect(FATOR_DE_PONTOS[c.id]).toBeLessThanOrEqual(3);
    }
  });
});
