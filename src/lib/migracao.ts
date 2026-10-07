/*
 * FASE I · o progresso do convidado quando a conta aparece.
 *
 * Regra do documento: *"Preservar progresso local. Ao criar conta: oferecer
 * sincronizar/migrar. Nunca apagar progresso silenciosamente."*
 *
 * O progresso vive no aparelho (`nexus-v1-profile`). Entrar numa conta não
 * toca nele — essa é a metade fácil, e está garantida por teste. A metade que
 * precisava de código é a outra: quando alguém que já jogou como convidado
 * cria conta, o jogo tem que *dizer* o que vai acontecer com aquelas horas, em
 * vez de seguir em frente e deixar a pessoa adivinhando.
 *
 * O que esta camada faz é só isso: reconhecer que há progresso em jogo, medir
 * o que é, oferecer uma vez por conta, e registrar a resposta. Ela nunca
 * apaga nada — não existe caminho daqui para `removeItem`. Subir o progresso
 * para o servidor é da FASE J, quando a Edge Function guardar perfil; até lá
 * "levar para a conta" significa marcar de quem é este aparelho e carimbar o
 * nome público, que é o que muda de verdade na tela do jogador.
 */
import type { Conta } from './auth';
import type { Profile } from './storage';

const CHAVE = 'nexus-v1-contas-reivindicadas';

export interface ResumoDoProgresso {
  jornadas: number;
  vitorias: number;
  conquistas: number;
  personagens: number;
  /** Se vale a pena interromper o jogador para falar disso. */
  vale: boolean;
}

/**
 * Nem todo progresso merece um aviso. Quem abriu o jogo, perdeu a primeira
 * luta e foi criar conta não precisa de uma caixa perguntando o que fazer com
 * o nada. O corte é ter concluído alguma jornada ou ter conquistado algo.
 */
export const resumoDoProgresso = (p: Profile): ResumoDoProgresso => {
  const conquistas = p.progress.unlocked.length;
  const personagens = Object.keys(p.progress.mastery).length;
  return {
    jornadas: p.journeys, vitorias: p.victories, conquistas, personagens,
    vale: p.journeys > 0 || conquistas > 0 || p.wins > 0,
  };
};

/** Quem já respondeu à oferta neste aparelho. Lista de ids de conta. */
export function contasReivindicadas(): string[] {
  try {
    const bruto: unknown = JSON.parse(localStorage.getItem(CHAVE) ?? '[]');
    return Array.isArray(bruto) ? bruto.filter((x): x is string => typeof x === 'string') : [];
  } catch { return []; }
}

export function marcarReivindicado(id: string): void {
  try {
    const lista = contasReivindicadas();
    if (!lista.includes(id)) localStorage.setItem(CHAVE, JSON.stringify([...lista, id]));
  } catch { /* Sem armazenamento a oferta reaparece. Repetir é chato; sumir seria pior. */ }
}

/**
 * A pergunta só vale para uma conta de verdade, com progresso de verdade, que
 * ainda não respondeu. Convidado não é conta: continuar jogando como
 * convidado não é "migrar" coisa nenhuma.
 */
export const deveOferecer = (conta: Conta | null, perfil: Profile, jaResponderam = contasReivindicadas()): boolean =>
  conta !== null && conta.origem !== 'convidado'
  && resumoDoProgresso(perfil).vale
  && !jaResponderam.includes(conta.id);

/**
 * Aceitar. Carimba o nome público da conta no perfil local — é o nome que vai
 * para o ranking — e registra a resposta. O resto do progresso fica onde
 * sempre esteve; não há nada para mover enquanto o servidor não guardar
 * perfil.
 */
export function levarParaAConta(perfil: Profile, conta: Conta): Profile {
  marcarReivindicado(conta.id);
  return conta.handle ? { ...perfil, publicHandle: conta.handle } : perfil;
}

/**
 * Recusar. Registra para não perguntar de novo e devolve o perfil intacto —
 * literalmente o mesmo objeto, para que nenhuma distração futura confunda
 * "recusou" com "perdeu".
 */
export function manterSeparado(perfil: Profile, conta: Conta): Profile {
  marcarReivindicado(conta.id);
  return perfil;
}
