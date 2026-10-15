import { describe, it, expect } from 'vitest';
import { ESTRELAS_DE_PONTOS, bonusDoTrio } from '../src/data/estrelas-de-pontos';
import { byId, characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { pontosDaLuta } from '../src/engine/pontos';

const lista = Object.entries(ESTRELAS_DE_PONTOS);
const comEstrelas = (n: number) => lista.filter(([, e]) => e.estrelas === n).sort((a, b) => b[1].bonus - a[1].bonus);
const semEstrela = characters.map((c) => c.id).filter((id) => !ESTRELAS_DE_PONTOS[id]);

describe('Estrelas dos pontos', () => {
  it('são 40 de cada nível, todas do elenco, com o bônus em degraus de 5%', () => {
    for (const n of [1, 2, 3]) expect(comEstrelas(n).length, `${n} estrelas`).toBe(40);
    for (const [id, e] of lista) { expect(byId[id], id).toBeDefined(); expect(e.bonus % 5).toBe(0); expect(e.bonus).toBeGreaterThanOrEqual(0); }
  });
  it('no trio conta primeiro quem tem mais estrelas, depois a maior porcentagem', () => {
    const [tres] = comEstrelas(3).slice(-1), [doisAlto] = comEstrelas(2);
    expect(doisAlto![1].bonus).toBeGreaterThan(tres![1].bonus);
    expect(bonusDoTrio([doisAlto![0], tres![0], semEstrela[0]!]).de).toBe(tres![0]);
    const [a, b] = [comEstrelas(3)[0]!, comEstrelas(3).slice(-1)[0]!];
    expect(bonusDoTrio([b[0], a[0], semEstrela[0]!]).de).toBe(a[0]);
    expect(bonusDoTrio(semEstrela.slice(0, 3))).toEqual({ bonus: 0 });
  });
  it('só os pontos mudam: a estrela vira uma linha a mais nos pontos da luta', () => {
    const [id, e] = comEstrelas(3)[0]!;
    const b = createBattle([id, semEstrela[0]!, semEstrela[1]!], ['naruto', 'luffy', 'pikachu'], 9);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    const p = pontosDaLuta(b, 0);
    const estrela = p.parcelas.find((x) => x.id === 'estrela')!;
    const resto = p.parcelas.filter((x) => x.id !== 'estrela').reduce((n, x) => n + x.valor, 0);
    expect(estrela.rotulo).toContain(byId[id]!.name);
    expect(estrela.valor).toBe(Math.round(resto * e.bonus / 100));
  });
});
