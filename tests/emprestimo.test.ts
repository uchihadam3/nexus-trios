import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { EMPRESTADOS_POR_DIA, comEmprestados, diaDoEmprestimo, emprestadosDoDia, faltaParaTrocar } from '../src/engine/emprestimo';

/* O Empréstimo do dia (src/engine/emprestimo.ts): 9 personagens por dia, iguais para todo mundo, sem repetir. */
describe('Empréstimo do dia', () => {
  it('9 personagens que existem, sem repetir, os mesmos para todo mundo no mesmo dia', () => {
    const hoje = emprestadosDoDia('2026-10-16');
    expect(hoje).toHaveLength(EMPRESTADOS_POR_DIA);
    expect(new Set(hoje).size).toBe(9);
    for (const id of hoje) expect(byId[id]).toBeTruthy();
    expect(emprestadosDoDia('2026-10-16')).toEqual(hoje);
  });
  it('troca todo dia', () => {
    const dias = ['2026-10-16', '2026-10-17', '2026-10-18', '2026-10-19'].map((d) => emprestadosDoDia(d).join());
    expect(new Set(dias).size).toBe(4);
  });
  it('o dia vira à meia-noite de Brasília', () => {
    expect(diaDoEmprestimo(Date.parse('2026-10-17T02:59:00Z'))).toBe('2026-10-16');
    expect(diaDoEmprestimo(Date.parse('2026-10-17T03:00:00Z'))).toBe('2026-10-17');
    expect(faltaParaTrocar(Date.parse('2026-10-17T02:59:00Z'))).toBe(60_000);
  });
  it('quem já tem um emprestado não ganha um segundo: o personagem aparece uma vez só', () => {
    const [a, b] = emprestadosDoDia('2026-10-16');
    const minha = [a!, b!, 'goku'];
    const tudo = comEmprestados(minha, '2026-10-16');
    expect(new Set(tudo).size).toBe(tudo.length);
    expect(tudo).toHaveLength(new Set([...minha, ...emprestadosDoDia('2026-10-16')]).size);
  });
});
