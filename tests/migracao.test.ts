/*
 * FASE I · o progresso sobrevive à chegada da conta.
 *
 * A regra do documento — *"Nunca apagar progresso silenciosamente"* — é fácil
 * de escrever num comentário e difícil de manter viva seis fases depois. Estes
 * testes existem para quebrar no dia em que alguém mexer nisso.
 */
import { beforeEach, describe, expect, it } from 'vitest';

import type { Conta } from '../src/lib/auth';
import {
  contasReivindicadas, deveOferecer, levarParaAConta, manterSeparado,
  marcarReivindicado, resumoDoProgresso,
} from '../src/lib/migracao';
import { ESCALA_DOS_PONTOS, loadProfile, type Profile } from '../src/lib/storage';

/* O ambiente de teste não tem navegador; um localStorage de mentira basta. */
const memoria = new Map<string, string>();
beforeEach(() => {
  memoria.clear();
  globalThis.localStorage = {
    getItem: (k: string) => memoria.get(k) ?? null,
    setItem: (k: string, v: string) => { memoria.set(k, v); },
    removeItem: (k: string) => { memoria.delete(k); },
    clear: () => { memoria.clear(); },
    key: (i: number) => [...memoria.keys()][i] ?? null,
    get length() { return memoria.size; },
  } as Storage;
});

const novato = (): Profile => ({ journeys: 0, victories: 0, best: 0, wins: 0, recordePontos: 0 });
const veterano = (): Profile => ({ journeys: 12, victories: 4, best: 8, wins: 31, recordePontos: 7_042_000, escalaDosPontos: ESCALA_DOS_PONTOS });

const conta = (over: Partial<Conta> = {}): Conta =>
  ({ id: 'u1', email: 'a@b.com', handle: 'Jogador_01', origem: 'email', ...over });

describe('quando vale a pena perguntar', () => {
  it('não interrompe quem ainda não tem nada', () => {
    expect(resumoDoProgresso(novato()).vale).toBe(false);
    expect(deveOferecer(conta(), novato())).toBe(false);
  });

  it('pergunta a quem tem horas em jogo', () => {
    const r = resumoDoProgresso(veterano());
    expect(r).toMatchObject({ jornadas: 12, recorde: 7_042_000, vale: true });
    expect(deveOferecer(conta(), veterano())).toBe(true);
  });

  it('convidado não é conta: não há para onde migrar', () => {
    expect(deveOferecer(conta({ origem: 'convidado' }), veterano())).toBe(false);
    expect(deveOferecer(null, veterano())).toBe(false);
  });

  it('pergunta uma vez só por conta', () => {
    expect(deveOferecer(conta(), veterano())).toBe(true);
    levarParaAConta(veterano(), conta());
    expect(deveOferecer(conta(), veterano())).toBe(false);
  });

  it('mas pergunta de novo para outra conta no mesmo aparelho', () => {
    levarParaAConta(veterano(), conta({ id: 'u1' }));
    expect(deveOferecer(conta({ id: 'u2' }), veterano())).toBe(true);
  });
});

describe('as duas respostas preservam tudo', () => {
  /*
   * O coração da regra. Aceitar e recusar mudam de quem é o nome público —
   * nada além disso. Nenhum contador, conquista ou Maestria pode mudar de
   * valor por causa de um login.
   */
  const intocado = (antes: Profile, depois: Profile) => {
    expect(depois.journeys).toBe(antes.journeys);
    expect(depois.victories).toBe(antes.victories);
    expect(depois.best).toBe(antes.best);
    expect(depois.wins).toBe(antes.wins);
    expect(depois.recordePontos).toBe(antes.recordePontos);
  };

  it('aceitar mantém o progresso e carimba o nome público', () => {
    const antes = veterano();
    const depois = levarParaAConta(antes, conta());
    intocado(antes, depois);
    expect(depois.publicHandle).toBe('Jogador_01');
  });

  it('recusar devolve o perfil exatamente como estava', () => {
    const antes = veterano();
    expect(manterSeparado(antes, conta())).toBe(antes);
  });

  it('conta sem nome público não inventa um', () => {
    const depois = levarParaAConta(veterano(), conta({ handle: null }));
    expect(depois.publicHandle).toBeUndefined();
  });

  it('nenhum caminho daqui escreve por cima do perfil guardado', () => {
    localStorage.setItem('nexus-v1-profile', JSON.stringify(veterano()));
    levarParaAConta(veterano(), conta());
    manterSeparado(veterano(), conta({ id: 'u2' }));
    /* O perfil no armazenamento continua lá, inteiro: quem salva é a tela. */
    expect(loadProfile().journeys).toBe(12);
    expect(loadProfile().recordePontos).toBe(7_042_000);
  });

  it('recorde da escala antiga (1 milhão por vitória) recomeça na escala nova, o resto do perfil fica', () => {
    localStorage.setItem('nexus-v1-profile', JSON.stringify({ journeys: 12, victories: 4, best: 8, wins: 31, recordePontos: 7_042_000 }));
    const p = loadProfile();
    expect(p).toMatchObject({ journeys: 12, victories: 4, best: 8, wins: 31, recordePontos: 0, escalaDosPontos: ESCALA_DOS_PONTOS });
  });
});

describe('o registro de quem já respondeu', () => {
  it('não duplica', () => {
    marcarReivindicado('u1'); marcarReivindicado('u1'); marcarReivindicado('u2');
    expect(contasReivindicadas()).toEqual(['u1', 'u2']);
  });

  it('aguenta lixo no armazenamento sem derrubar a tela', () => {
    localStorage.setItem('nexus-v1-contas-reivindicadas', '{isso não é json');
    expect(contasReivindicadas()).toEqual([]);
    localStorage.setItem('nexus-v1-contas-reivindicadas', '{"nem":"lista"}');
    expect(contasReivindicadas()).toEqual([]);
    localStorage.setItem('nexus-v1-contas-reivindicadas', '["u1",42,null]');
    expect(contasReivindicadas()).toEqual(['u1']);
  });

  /*
   * Navegador em aba anônima com armazenamento bloqueado: a oferta repete,
   * o que é chato, mas nada explode e nada some.
   */
  it('sobrevive a armazenamento proibido', () => {
    globalThis.localStorage = {
      getItem: () => { throw new Error('bloqueado'); },
      setItem: () => { throw new Error('bloqueado'); },
    } as unknown as Storage;
    expect(contasReivindicadas()).toEqual([]);
    expect(() => { marcarReivindicado('u1'); }).not.toThrow();
    expect(deveOferecer(conta(), veterano())).toBe(true);
  });
});
