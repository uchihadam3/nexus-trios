import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { CONTAS, DE, TOTAL_DE_TRIOS } from '../src/data/posicoes-dos-trios';
import { notaDoTrio, posicaoDoTrio } from '../src/presentation/dicas-do-trio';
import { montarRanking, textoDaPosicao } from '../src/presentation/posicao-do-trio';

/* A posição exata do time entre todos os trios (src/presentation/posicao-do-trio.ts). */
describe('posição do trio', () => {
  const ranking = montarRanking(DE, CONTAS, TOTAL_DE_TRIOS);
  const n = characters.length;

  it('a contagem soma todos os trios possíveis', () => {
    expect(CONTAS.split(',').reduce((s, c) => s + parseInt(c, 36), 0)).toBe((n * (n - 1) * (n - 2)) / 6);
    expect(TOTAL_DE_TRIOS).toBe((n * (n - 1) * (n - 2)) / 6);
  });

  it('nota maior, posição melhor; e bate com o "melhor que X%"', () => {
    const ids = characters.map((c) => c.id);
    let semente = 7;
    const sorteia = () => { semente = (semente * 1103515245 + 12345) % 2147483648; return ids[semente % ids.length]!; };
    const trios: string[][] = [];
    while (trios.length < 300) { const t = [sorteia(), sorteia(), sorteia()]; if (new Set(t).size === 3) trios.push(t); }
    const ordem = trios.map((t) => ({ nota: notaDoTrio(t), pos: ranking.posicaoDaNota(notaDoTrio(t)), pct: posicaoDoTrio(t).pct })).sort((a, b) => b.nota - a.nota);
    for (let i = 1; i < ordem.length; i++) expect(ordem[i]!.pos).toBeGreaterThanOrEqual(ordem[i - 1]!.pos);
    // melhor que X% ⇒ a posição fica dentro dos (100 − X)% de cima (com 1% de folga para os empates e o arredondamento)
    for (const o of ordem) expect(o.pos / TOTAL_DE_TRIOS).toBeLessThanOrEqual((100 - o.pct + 1) / 100);
    expect(ranking.posicaoDaNota(99)).toBe(1);
    expect(ranking.posicaoDaNota(-99)).toBe(TOTAL_DE_TRIOS);
  });

  it('o texto', () => {
    expect(textoDaPosicao(1234)).toBe('1.234º');
  });
});

/* Os trios do topo que já lutaram de verdade (src/data/topo-medido.ts). */
describe('posição medida do topo', () => {
  it('quem lutou fica com a posição da luta; quem não lutou nunca passa à frente deles', async () => {
    const { IDS, TRIOS } = await import('../src/data/topo-medido');
    const { CONTAS, DE, TOTAL_DE_TRIOS } = await import('../src/data/posicoes-dos-trios');
    const { montarTopoMedido, posicaoDoTime } = await import('../src/presentation/posicao-do-trio');
    const ranking = montarRanking(DE, CONTAS, TOTAL_DE_TRIOS), topo = montarTopoMedido(IDS, TRIOS);
    expect(topo.medidos).toBe(TRIOS.length / 6);
    const ids = IDS.split(',');
    for (const id of ids) expect(characters.some((c) => c.id === id), id).toBe(true);
    const primeiro = [0, 2, 4].map((o) => ids[parseInt(TRIOS.slice(o, o + 2), 36)]!);
    expect(posicaoDoTime(primeiro, ranking, topo)).toBe(1);
    expect(posicaoDoTime([...primeiro].reverse(), ranking, topo)).toBe(1);
    expect(posicaoDoTime(['patrick', 'pateta', 'scooby'], ranking, topo)).toBeGreaterThan(topo.medidos);
  });
});
