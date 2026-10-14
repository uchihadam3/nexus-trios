/*
 * A esfera que cresce em estágios antes de ser lançada (pedido do jogador sobre a Genki Dama: "aparece a bolinha, aí
 * ela cresce, cresce, cresce, aí ele lança ela… uns dois segundos… igual o do Byakuya, o tempo para").
 * O desenho está em src/components/EsferaQueCresce.tsx; o tempo vem das fases da Mecânica única
 * (src/presentation/ativacao-da-unica.ts: o Preparo próprio dela dá os dois segundos).
 */
import type { FasesDaUnica } from './ativacao-da-unica';

export interface Esfera {
  /** a cor da energia (borda e brilho) */
  cor: string;
  /** o miolo */
  miolo: string;
  /** o tamanho de cada estágio, em medalhões (o diâmetro) */
  estagios: readonly number[];
  /** o som de cada estágio (o primeiro é a esfera aparecendo) */
  sons: readonly string[];
  /** o som do arremesso */
  lanca: string;
}
export const ESFERA_QUE_CRESCE: Record<string, Esfera> = {
  goku: {
    cor: '#4aa8ff', miolo: '#e8f8ff', estagios: [0.42, 0.7, 1.0, 1.42],
    sons: ['mu-genki-cresce-1', 'mu-genki-cresce-2', 'mu-genki-cresce-3', 'mu-genki-cresce-4'], lanca: 'mu-genki-lanca',
  },
};
/** Quando cada estágio começa, em segundos desde o começo da ativação: do começo até um pouco antes de soltar. */
export function estagiosDaEsfera(e: Esfera, fases: FasesDaUnica): number[] {
  const de = 0.12, ate = Math.max(de + 0.6, fases.soltaEm - 0.3), n = e.estagios.length;
  return e.estagios.map((_, k) => de + ((ate - de) * k) / Math.max(1, n - 1));
}
