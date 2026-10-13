import { describe, expect, it } from 'vitest';
import { replayRanked } from '../src/engine/ranked';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { LUTA, PESO_DA_CURA_ALVO, feitosDaLuta, pontosDaJornada, pontosDaLuta } from '../src/engine/pontos';
import { PESO_DA_CURA } from '../src/data/peso-da-cura';
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

  it('a cura não tem teto: só quem cura muito mais que os outros tem um peso próprio nela', () => {
    expect(PESO_DA_CURA_ALVO).toBeGreaterThan(0);
    for (const [id, peso] of Object.entries(PESO_DA_CURA)) {
      expect(characters.some((c) => c.id === id), id).toBe(true);
      expect(peso, id).toBeGreaterThan(0);
      expect(peso, id).toBeLessThan(1);
    }
    // os curandeiros que mais curam têm peso; quem quase não cura conta inteiro
    expect(PESO_DA_CURA.orihime).toBeLessThan(0.5);
    expect(PESO_DA_CURA.sailormoon).toBeLessThan(0.5);
    expect(PESO_DA_CURA.goku).toBeUndefined();
  });

  it('a luta que se arrasta rende menos por segundo, mas ainda rende', () => {
    expect(feitosDaLuta(30_000)).toBe(30_000);
    expect(feitosDaLuta(LUTA.cheio)).toBe(LUTA.cheio);
    // a luta de 200 s do trio de curandeiros (uns 180 mil de feitos) vale bem mais que uma luta cheia, mas não 5 vezes
    expect(feitosDaLuta(180_000)).toBeCloseTo(LUTA.cheio + 145_000 * LUTA.acima);
    expect(feitosDaLuta(180_000)).toBeGreaterThan(2 * LUTA.cheio);
    expect(feitosDaLuta(180_000)).toBeLessThan(180_000 / 1.8);
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
