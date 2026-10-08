/*
 * Os pontos de cada luta — os mesmos do ranking.
 *
 * O objetivo do jogo é ir o mais longe possível nas 10 lutas e fazer o máximo
 * de pontos. A conta é a do servidor (src/engine/ranked.ts, replayRanked):
 * cada vitória vale 1.000.000, e o jeito de vencer soma mais —
 * Vida que sobrou (até 10.000), lutadores de pé (6.000 cada) e viradas a seu
 * favor no Domínio (500 cada, até 2.000). Derrota não pontua e encerra a jornada.
 * Mostrar a mesma conta na tela e no ranking evita dois placares diferentes.
 */
import type { Battle } from './types';

export interface PontosDaLuta {
  total: number;
  vitoria: number;
  vida: number;
  sobreviventes: number;
  viradas: number;
  /** Quantos de pé e a Vida média, para o texto. */
  de_pe: number;
  vidaMedia: number;
}

export const PONTOS = { vitoria: 1_000_000, vidaMaxima: 10_000, porSobrevivente: 6_000, porVirada: 500, viradasMaximo: 2_000 } as const;

export function pontosDaLuta(battle: Battle): PontosDaLuta {
  const trio = battle.fighters.filter((f) => f.side === 'player');
  const de_pe = trio.filter((f) => f.hp > 0).length;
  const vidaMedia = Math.max(0, Math.min(1, trio.reduce((n, f) => n + f.hp / f.maxHp, 0) / 3));
  if (battle.winner !== 'player') return { total: 0, vitoria: 0, vida: 0, sobreviventes: 0, viradas: 0, de_pe, vidaMedia };
  const vida = Math.round(vidaMedia * PONTOS.vidaMaxima);
  const sobreviventes = de_pe * PONTOS.porSobrevivente;
  const viradas = Math.min(PONTOS.viradasMaximo, (battle.viradasDoTrio ?? 0) * PONTOS.porVirada);
  return { total: PONTOS.vitoria + vida + sobreviventes + viradas, vitoria: PONTOS.vitoria, vida, sobreviventes, viradas, de_pe, vidaMedia };
}

/** A pontuação da jornada até agora (a qualidade é limitada a 999.999, como no servidor). */
export function pontosDaJornada(lutas: readonly { pontos?: number; won: boolean }[]): number {
  const vencidas = lutas.filter((l) => l.won).length;
  const qualidade = lutas.reduce((n, l) => n + Math.max(0, (l.pontos ?? 0) - (l.won ? PONTOS.vitoria : 0)), 0);
  return vencidas * PONTOS.vitoria + Math.min(999_999, qualidade);
}

export const formatarPontos = (n: number) => Math.round(n).toLocaleString('pt-BR');
