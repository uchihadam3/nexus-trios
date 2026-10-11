import { describe, expect, it } from 'vitest';
import { combosDoTrio, idsDosCombos, ligacoesDosCombos, LIGACOES_DOS_COMBOS } from '../src/engine/combos';
import { sinergiaDoTrio } from '../src/engine/campaign';
import { PESO_DA_LIGACAO } from '../src/data/forca-dos-rivais';
import { characters } from '../src/data/characters';

describe('Combos rápidos', () => {
  it('idsDosCombos acende exatamente os mesmos combos que combosDoTrio', () => {
    const ids = characters.map((c) => c.id);
    let semente = 12345;
    const sorteia = () => { semente = (semente * 1103515245 + 12345) >>> 0; return ids[semente % ids.length]!; };
    for (let i = 0; i < 20000; i++) {
      const trio = [sorteia(), sorteia(), sorteia()];
      if (new Set(trio).size < 3) continue;
      expect(idsDosCombos(trio)).toEqual(combosDoTrio(trio).combos.map((c) => c.id));
      // a sinergia rápida da campanha é a soma das ligações × peso, idêntica bit a bit
      const l = ligacoesDosCombos(trio);
      expect(sinergiaDoTrio(trio)).toBe(LIGACOES_DOS_COMBOS.reduce((n, k) => n + (l[k] ?? 0) * (PESO_DA_LIGACAO[k] ?? 0), 0));
    }
  });
});
