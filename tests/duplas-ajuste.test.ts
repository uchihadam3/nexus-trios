import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { AJUSTE_DAS_DUPLAS, ALFABETO_DAS_DUPLAS, DUPLAS_MEDIDAS_COM } from '../src/data/duplas-ajuste';
import { rosterFingerprint } from '../src/engine/ranked';
import { ajusteDaDupla } from '../src/presentation/dicas-do-trio';

/* O ajuste de cada dupla vale só para o elenco medido: um personagem novo muda a ordem das duplas. */
describe('ajuste das duplas (Dicas)', () => {
  it('foi medido com o elenco de agora e tem uma letra por dupla', () => {
    expect(DUPLAS_MEDIDAS_COM).toBe(rosterFingerprint());
    const n = characters.length;
    expect(AJUSTE_DAS_DUPLAS.length).toBe((n * (n - 1)) / 2);
    expect([...AJUSTE_DAS_DUPLAS].every((ch) => ALFABETO_DAS_DUPLAS.includes(ch))).toBe(true);
  });
  it('é o mesmo nos dois sentidos e zero com ele mesmo', () => {
    const [a, b] = [characters[3]!.id, characters[250]!.id];
    expect(ajusteDaDupla(a, b)).toBe(ajusteDaDupla(b, a));
    expect(ajusteDaDupla(a, a)).toBe(0);
  });
});
