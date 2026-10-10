/*
 * Ponto fraco em poucas palavras: uma etiqueta e o porquê.
 *
 * Pedido do jogador: o ponto fraco é o que o próprio personagem não consegue
 * fazer — cair rápido, uma habilidade que quase não sai, o Preparo
 * longo que é cortado, o ataque lento —, nunca "contra Espinhos" ou "contra
 * Área", que pesam em todo mundo. Os pontos fracos são medidos e escritos por
 * scripts/escrever-fraquezas.ts (src/data/fraquezas.ts); aqui eles só ganham
 * os números de agora (a Vida e o ritmo mudam no equilíbrio).
 */
import { pontosFracos } from './fraquezas';

export type TipoDeFraqueza = 'cai' | 'golpe' | 'rara' | 'espera' | 'preparo' | 'demora' | 'lento' | 'dano' | 'espalha' | 'apanhar';

export interface Fraqueza {
  tipo: TipoDeFraqueza;
  /** A etiqueta: "Cai rápido", "Habilidade rara"… */
  rotulo: string;
  /** Por quê, em poucas palavras. */
  motivo: string;
}

/** Os números de agora do personagem. */
export interface QuemTemOPontoFraco { id: string; hp: number; interval: number }

const decimal = (n: number) => (Math.round(n * 100) / 100).toLocaleString('pt-BR');

/** Os pontos fracos de um personagem (no máximo dois, o maior primeiro). */
export function pontoFraco(c: QuemTemOPontoFraco): Fraqueza[] {
  return (pontosFracos[c.id] ?? []).slice(0, 2).map((x) => {
    // a Vida e o ritmo do texto guardado podem ter mudado no equilíbrio: valem os de agora
    if (/[Ss]ó [\d.]+ de Vida/.test(x.motivo)) return { ...x, motivo: x.motivo.replace(/([Ss])ó [\d.]+ de Vida/, (_, s) => `${s}ó ${Math.round(c.hp).toLocaleString('pt-BR')} de Vida`) };
    if (x.tipo === 'lento') return { ...x, motivo: x.motivo.replace(/a cada [\d.,]+ s/, `a cada ${decimal(c.interval)} s`) };
    return { ...x };
  });
}
