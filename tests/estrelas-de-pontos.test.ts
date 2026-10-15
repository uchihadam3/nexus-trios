import { describe, it, expect } from 'vitest';
import { ESTRELAS_DE_PONTOS, bonusDoTrio } from '../src/data/estrelas-de-pontos';
import { byId } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { pontosDaLuta } from '../src/engine/pontos';

describe('Estrelas dos pontos', () => {
  it('são 40 de cada nível, todas do elenco, com o bônus em degraus de 5%', () => {
    const lista = Object.entries(ESTRELAS_DE_PONTOS);
    for (const n of [1, 2, 3]) expect(lista.filter(([, e]) => e.estrelas === n).length, `${n} estrelas`).toBe(40);
    for (const [id, e] of lista) { expect(byId[id], id).toBeDefined(); expect(e.bonus % 5).toBe(0); expect(e.bonus).toBeGreaterThanOrEqual(0); }
  });
  it('no trio vale o maior bônus, e só os pontos mudam: a luta é a mesma', () => {
    expect(bonusDoTrio(['goku', 'vegeta', 'hinata']).de).toBe(ESTRELAS_DE_PONTOS.goku!.bonus >= ESTRELAS_DE_PONTOS.vegeta!.bonus ? 'goku' : 'vegeta');
    expect(bonusDoTrio(['hinata', 'jiraiya', 'gaara'])).toEqual({ bonus: 0 });
    const b = createBattle(['vegeta', 'hinata', 'jiraiya'], ['naruto', 'luffy', 'pikachu'], 9);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    const p = pontosDaLuta(b, 0);
    const estrela = p.parcelas.find((x) => x.id === 'estrela')!;
    const resto = p.parcelas.filter((x) => x.id !== 'estrela').reduce((n, x) => n + x.valor, 0);
    expect(estrela.rotulo).toContain('Vegeta');
    expect(estrela.valor).toBe(Math.round(resto * ESTRELAS_DE_PONTOS.vegeta!.bonus / 100));
  });
});
