/*
 * As frases do Top 3, conferidas contra os exemplos do documento — os
 * mesmos números, as mesmas palavras.
 */
import { describe, expect, it } from 'vitest';

import { mensagemDoTop3, situacaoDasVagas } from '../src/lib/top3';

describe('mensagens do Top 3', () => {
  it('quarto trio que não entra: "Para entrar: supere 1.300."', () => {
    expect(mensagemDoTop3({ situacao: 'fora', score: 1200, vagas: 0, precisa_superar: 1300 })).toEqual({
      titulo: '1.200 PONTOS', destaque: false,
      linhas: ['Não entrou nos seus 3 melhores.', 'Para entrar: supere 1.300.'],
    });
  });

  it('quarto trio que entra: "NOVO TOP 3"', () => {
    expect(mensagemDoTop3({ situacao: 'entrou', score: 1550, vagas: 0, precisa_superar: 1400, removido: 1300 })).toEqual({
      titulo: 'NOVO TOP 3', destaque: true,
      linhas: ['1.550 entrou no ranking.', 'O resultado de 1.300 saiu dos seus 3 melhores.'],
    });
  });

  it('mesmo trio pior mantém o recorde; melhor sobe a mesma entrada', () => {
    expect(mensagemDoTop3({ situacao: 'manteve', score: 1300, vagas: 2, precisa_superar: null, recorde: 1500 }).linhas)
      .toContain('O recorde deste trio continua 1.500.');
    expect(mensagemDoTop3({ situacao: 'melhorou', score: 1550, vagas: 2, precisa_superar: null, anterior: 1500 }).linhas[0])
      .toBe('Este trio subiu de 1.500 para 1.550.');
  });

  it('trio novo com vaga diz quantas sobram', () => {
    expect(mensagemDoTop3({ situacao: 'novo', score: 900, vagas: 1, precisa_superar: null }).linhas).toEqual(['900 entrou no ranking.', '1 vaga livre.']);
  });
});

describe('a linha das vagas', () => {
  it('"1 vaga livre." e o plural', () => {
    expect(situacaoDasVagas(1, null)).toBe('1 vaga livre.');
    expect(situacaoDasVagas(3, null)).toBe('3 vagas livres.');
  });
  it('"Próxima entrada precisa superar 1.400."', () => {
    expect(situacaoDasVagas(0, 1400)).toBe('Próxima entrada precisa superar 1.400.');
  });
});
