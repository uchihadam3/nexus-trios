import { describe, expect, it } from 'vitest';
import { corDoNome, haQuanto, quando, rotuloDoDia, statusDe, textoDoErro } from '../src/lib/comunidade';

/* A Comunidade fala de tempo como gente ("há 5 min", "ontem às 21:10") e traduz os erros do banco. */
const AGORA = new Date(2026, 9, 15, 14, 30).getTime();
const atras = (ms: number) => new Date(AGORA - ms).toISOString();
const MIN = 60_000, H = 60 * MIN;

describe('Comunidade: tempo e status', () => {
  it('há quanto tempo', () => {
    expect(haQuanto(atras(10_000), AGORA)).toBe('agora');
    expect(haQuanto(atras(5 * MIN), AGORA)).toBe('há 5 min');
    expect(haQuanto(atras(3 * H), AGORA)).toBe('há 3 h');
    expect(haQuanto(atras(26 * H), AGORA)).toBe('há 1 dia');
    expect(haQuanto(atras(65 * 24 * H), AGORA)).toBe('há 2 meses');
  });
  it('quando: hoje, ontem ou a data', () => {
    expect(quando(new Date(2026, 9, 15, 9, 5).toISOString(), AGORA)).toBe('hoje às 09:05');
    expect(quando(new Date(2026, 9, 14, 21, 10).toISOString(), AGORA)).toBe('ontem às 21:10');
    expect(quando(new Date(2026, 9, 2, 8, 0).toISOString(), AGORA)).toBe('02/10 às 08:00');
    expect(rotuloDoDia(new Date(2026, 9, 12, 8, 0).toISOString(), AGORA)).toBe('Segunda, 12/10');
  });
  it('status: online desde, saiu há, nunca apareceu', () => {
    expect(statusDe({ online: true, onlineDesde: atras(12 * MIN), vistoEm: atras(5_000) }, AGORA))
      .toEqual({ curto: 'Online há 12 min', longo: 'Online desde hoje às 14:18' });
    expect(statusDe({ online: false, onlineDesde: atras(5 * H), vistoEm: atras(3 * H) }, AGORA))
      .toEqual({ curto: 'Saiu há 3 h', longo: 'Visto por último hoje às 11:30' });
    expect(statusDe({ online: false, onlineDesde: null, vistoEm: null }, AGORA).curto).toBe('Ainda não apareceu');
  });
  it('erros do banco viram frase de gente', () => {
    expect(textoDoErro(new Error('chat: devagar, espere uns segundos'))).toMatch(/Calma/);
    expect(textoDoErro(new Error('chat: mensagem repetida'))).toMatch(/mesma mensagem/);
    expect(textoDoErro(new Error('comunidade: escolha seu nome antes'))).toMatch(/nome público/);
    expect(textoDoErro(new Error('Failed to fetch'))).toMatch(/internet/);
  });
  it('a cor de um nome é sempre a mesma', () => {
    expect(corDoNome('abc')).toBe(corDoNome('abc'));
    expect(corDoNome('abc')).not.toBe(corDoNome('abd'));
  });
});
