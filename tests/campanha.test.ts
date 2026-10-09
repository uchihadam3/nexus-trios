import { describe, expect, it } from 'vitest';
import { ESCALAS, forcaDoTrio, generateCampaign, sinergiaDoTrio } from '../src/engine/campaign';
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';

/* Pedido do jogador: cada luta mais difícil, mais sinergia a cada luta, e chefe sem trio fixo. */
describe('campanha', () => {
  const jornadas = Array.from({ length: 60 }, (_, i) => generateCampaign(1000 + i * 7919, ['goku', 'naruto', 'batman']));
  it('a sinergia dos rivais nunca cai de uma luta para a outra (lutas 1 a 9)', () => {
    for (const c of jornadas) for (let i = 1; i < 9; i++) expect(sinergiaDoTrio(c[i]!.team)).toBeGreaterThanOrEqual(sinergiaDoTrio(c[i - 1]!.team) - 1e-9);
  });
  it('cada luta é mais difícil: a Vida dos rivais nunca cai e o fim tem os rivais mais fortes', () => {
    for (let i = 1; i < 10; i++) expect(ESCALAS[i]!).toBeGreaterThanOrEqual(ESCALAS[i - 1]!);
    const media = (i: number) => jornadas.reduce((n, c) => n + forcaDoTrio(c[i]!.team), 0) / jornadas.length;
    const comeco = [0, 1, 2, 3, 4, 5, 6].reduce((n, i) => n + media(i), 0) / 7;
    expect(media(8)).toBeGreaterThan(comeco);
    expect(media(9)).toBeGreaterThan(media(8));
  });
  it('o chefe não é fixo: muda de uma jornada para outra', () => {
    expect(new Set(jornadas.map((c) => [...c[9]!.team].sort().join('|'))).size).toBeGreaterThan(40);
  });
  it('todo personagem tem força medida (rode scripts/medir-forca.ts se mudar o elenco)', () => {
    for (const c of characters) expect(FORCA[c.id], c.id).toBeTypeOf('number');
  });
});
