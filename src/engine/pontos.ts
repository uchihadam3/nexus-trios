/*
 * Os pontos de cada luta — os mesmos do ranking.
 *
 * Pedido do jogador: "sempre dá mais ou menos 1 milhão por batalha; tem que
 * variar mais, e se perder a batalha ainda ganha os pontos que fez nela". A
 * conta antiga era 1.000.000 por vitória e só uns 30.000 de "qualidade" — toda
 * luta vencida parecia igual, e a derrota valia zero.
 *
 * Agora a luta paga pelo que o trio fez nela:
 *   combate  · dano causado, nocautes, cura e proteção, interrupções e
 *              habilidades usadas — conta mesmo na derrota;
 *   vitória  · um bônus por vencer, mais a Vida que sobrou, quem ficou de pé
 *              e a rapidez (vencer depressa vale mais);
 *   viradas  · virar o Domínio a seu favor.
 * Tudo multiplicado pela altura da jornada (a luta 10 vale ×1,45).
 * A escala é a pedida: derrota feia ~1.000–2.000; vitória ruim ~5.000–6.000;
 * vitória razoável ~8.000–10.000; luta incrível 15.000+.
 * A jornada é a soma das lutas (a derrota encerra, mas os pontos dela ficam).
 * O servidor (src/engine/ranked.ts, replayRanked) usa exatamente esta conta.
 */
import type { Battle } from './types';

export type ParcelaId = 'dano' | 'nocautes' | 'apoio' | 'jogadas' | 'viradas' | 'vitoria' | 'vida' | 'rapidez';
export interface Parcela { id: ParcelaId; rotulo: string; valor: number }

export interface PontosDaLuta {
  total: number;
  /** As parcelas já multiplicadas pela altura da jornada, na ordem de exibição. */
  parcelas: Parcela[];
  /** O multiplicador da luta (1 na primeira, cresce a cada luta). */
  multiplicador: number;
  /** Quantos de pé e a Vida média, para o texto. */
  de_pe: number;
  vidaMedia: number;
}

export const PONTOS = {
  porDano: 0.4,
  porNocaute: 250,
  porApoio: 0.35,
  porInterrupcao: 250,
  porHabilidade: 45,
  porVirada: 120,
  viradasMaximo: 480,
  vitoria: 700,
  vidaMaxima: 4_500,
  porSobrevivente: 550,
  rapidezMaxima: 4_000,
  /** Vencer até este tempo de luta vale a rapidez inteira; depois cai até zero. */
  rapidoAte: 18,
  lentoDe: 45,
  /** Quanto cada luta da jornada multiplica a mais (luta 10 = ×1,45). */
  porLuta: 0.05,
} as const;

export const multiplicadorDaLuta = (indice: number) => 1 + PONTOS.porLuta * Math.max(0, indice);

export function pontosDaLuta(battle: Battle, indice = 0): PontosDaLuta {
  const trio = battle.fighters.filter((f) => f.side === 'player');
  const de_pe = trio.filter((f) => f.hp > 0).length;
  const vidaMedia = Math.max(0, Math.min(1, trio.reduce((n, f) => n + f.hp / f.maxHp, 0) / 3));
  const soma = (k: keyof (typeof trio)[number]['stats']) => trio.reduce((n, f) => n + f.stats[k], 0);
  const venceu = battle.winner === 'player';
  const rapidez = venceu ? Math.max(0, Math.min(1, (PONTOS.lentoDe - battle.time) / (PONTOS.lentoDe - PONTOS.rapidoAte))) : 0;
  const m = multiplicadorDaLuta(indice);
  const brutas: [ParcelaId, string, number][] = [
    ['dano', 'Dano causado', soma('damage') * PONTOS.porDano],
    ['nocautes', 'Nocautes', soma('kills') * PONTOS.porNocaute],
    ['apoio', 'Cura e proteção', (soma('healing') + soma('protection')) * PONTOS.porApoio],
    ['jogadas', 'Habilidades e cortes', soma('skills') * PONTOS.porHabilidade + soma('interrupts') * PONTOS.porInterrupcao],
    ['viradas', 'Viradas', Math.min(PONTOS.viradasMaximo, (battle.viradasDoTrio ?? 0) * PONTOS.porVirada)],
    ['vitoria', 'Vitória', venceu ? PONTOS.vitoria : 0],
    ['vida', `Vida ${Math.round(vidaMedia * 100)}% · ${de_pe} de pé`, venceu ? vidaMedia * PONTOS.vidaMaxima + de_pe * PONTOS.porSobrevivente : 0],
    ['rapidez', 'Rapidez', rapidez * PONTOS.rapidezMaxima],
  ];
  const parcelas = brutas.map(([id, rotulo, v]) => ({ id, rotulo, valor: Math.round(v * m) })).filter((p) => p.valor > 0);
  return { total: parcelas.reduce((n, p) => n + p.valor, 0), parcelas, multiplicador: m, de_pe, vidaMedia };
}

/** A pontuação da jornada: a soma das lutas jogadas (vencidas ou não). */
export function pontosDaJornada(lutas: readonly { pontos?: number; won: boolean }[]): number {
  return lutas.reduce((n, l) => n + Math.max(0, l.pontos ?? 0), 0);
}

export const formatarPontos = (n: number) => Math.round(n).toLocaleString('pt-BR');
