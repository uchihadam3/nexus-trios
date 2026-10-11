import { describe, expect, it } from 'vitest';
import { ESCALAS, forcaDoTrio, generateCampaign } from '../src/engine/campaign';
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';

/*
 * Pedido do jogador: a campanha por faixas — cinco faixas de força (muito fracos … muito fortes), dois trios
 * sorteados de cada; o mais fraco nas lutas ímpares e o mais forte nas pares; o chefe sem trio fixo; e as
 * faixas acompanham a força do trio do jogador.
 */
describe('campanha', () => {
  const jornadas = Array.from({ length: 60 }, (_, i) => generateCampaign(1000 + i * 7919, ['goku', 'naruto', 'batman']));
  it('em cada faixa, o trio da luta ímpar é o mais fraco dos dois e o da luta par o mais forte', () => {
    for (const c of jornadas) for (let f = 0; f < 5; f++) expect(forcaDoTrio(c[2 * f + 1]!.team)).toBeGreaterThanOrEqual(forcaDoTrio(c[2 * f]!.team) - 1e-9);
  });
  it('as faixas acompanham o trio: um trio forte enfrenta rivais mais fortes que um trio fraco', () => {
    const fortes = [...characters].sort((a, b) => (FORCA[b.id] ?? 0) - (FORCA[a.id] ?? 0)).slice(0, 3).map((c) => c.id);
    const fracos = [...characters].sort((a, b) => (FORCA[a.id] ?? 0) - (FORCA[b.id] ?? 0)).slice(0, 3).map((c) => c.id);
    const media = (t: string[]) => Array.from({ length: 20 }, (_, i) => generateCampaign(77 + i * 31, t)).flat().reduce((n, e) => n + forcaDoTrio(e.team), 0) / 200;
    expect(media(fortes)).toBeGreaterThan(media(fracos));
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
