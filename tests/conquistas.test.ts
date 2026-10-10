import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { ABAS, PERSONAGENS_DA_ABA, TOTAL_DE_CONQUISTAS, juntar, liberar, limpar, sugestao, tituloDe } from '../src/lib/conquistas';

describe('Conquistas: uma por personagem', () => {
  it('são 250, e cada personagem está em exatamente uma aba', () => {
    expect(TOTAL_DE_CONQUISTAS).toBe(characters.length);
    const todos = ABAS.flatMap((a) => PERSONAGENS_DA_ABA[a.id].map((c) => c.id));
    expect(todos.length).toBe(characters.length);
    expect(new Set(todos).size).toBe(characters.length);
    for (const a of ABAS) expect(PERSONAGENS_DA_ABA[a.id].length, a.nome).toBeGreaterThan(30);
  });

  it('terminar as 10 lutas libera o trio; quem já estava liberado fica como estava', () => {
    const primeira = liberar({}, ['jill', 'vegeta', 'goku'], '2026-10-01T00:00:00.000Z');
    expect(primeira.novas).toEqual(['jill', 'vegeta', 'goku']);
    const segunda = liberar(primeira.conquistas, ['jill', 'light', 'professorx'], '2026-10-02T00:00:00.000Z');
    expect(segunda.novas).toEqual(['light', 'professorx']);
    expect(segunda.conquistas.jill).toBe('2026-10-01T00:00:00.000Z');
    expect(Object.keys(segunda.conquistas)).toHaveLength(5);
    expect(liberar(segunda.conquistas, ['jill', 'light', 'professorx']).novas).toEqual([]);
  });

  it('as do servidor entram no aparelho com a data mais antiga, e o que não existe sai', () => {
    const local = { goku: '2026-10-05T00:00:00.000Z' };
    const juntas = juntar(local, [{ id: 'goku', data: '2026-10-01T00:00:00.000Z' }, { id: 'vegeta', data: '2026-10-02T00:00:00.000Z' }, { id: 'nao-existe', data: '2026-10-02T00:00:00.000Z' }]);
    expect(juntas).toEqual({ goku: '2026-10-01T00:00:00.000Z', vegeta: '2026-10-02T00:00:00.000Z' });
    expect(limpar({ goku: 'x', vegeta: '2026-10-02T00:00:00.000Z', fantasma: '2026-10-02T00:00:00.000Z' })).toEqual({ vegeta: '2026-10-02T00:00:00.000Z' });
  });

  it('os títulos sobem com os marcos, e o último é liberar todos', () => {
    expect(tituloDe(0).atual.nome).toBe('Recruta');
    expect(tituloDe(3).atual.nome).toBe('Aventureiro');
    expect(tituloDe(9).proximo?.minimo).toBe(10);
    expect(tituloDe(TOTAL_DE_CONQUISTAS).proximo).toBeNull();
    expect(tituloDe(TOTAL_DE_CONQUISTAS).atual.nome).toBe('Senhor do Nexus');
  });

  it('o desafio do dia sugere três que faltam, o mesmo o dia todo', () => {
    const s = sugestao({ goku: '2026-10-01T00:00:00.000Z' }, '2026-10-10');
    expect(s).toHaveLength(3);
    expect(s.some((c) => c.id === 'goku')).toBe(false);
    expect(sugestao({}, '2026-10-10').map((c) => c.id)).toEqual(sugestao({}, '2026-10-10').map((c) => c.id));
  });
});
