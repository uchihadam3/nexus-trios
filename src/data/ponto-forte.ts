/*
 * Ponto forte em poucas palavras: uma etiqueta e o porquê, com a habilidade.
 *
 * Pedido do jogador: "você fala por que que é fraco, mas não fala por que que
 * é forte". O ponto forte é o que o personagem faz muito melhor que o resto do
 * elenco, medido em lutas simuladas (scripts/escrever-fraquezas.ts →
 * src/data/fraquezas.ts): bate muito forte, cura, protege, atrapalha os
 * rivais, corta Preparos, aguenta…
 */
import { pontosFortes } from './fraquezas';

export type TipoDeForca = 'dano' | 'nocaute' | 'cura' | 'escudo' | 'controle' | 'ritmo' | 'carga' | 'corte' | 'reforco' | 'reviver' | 'aguenta' | 'agil' | 'cedo' | 'rapido' | 'equilibrado';

export interface Forca {
  tipo: TipoDeForca;
  /** A etiqueta: "Bate muito forte", "Cura o trio"… */
  rotulo: string;
  /** Por quê, com a habilidade que faz isso. */
  motivo: string;
}

const decimal = (n: number) => (Math.round(n * 100) / 100).toLocaleString('pt-BR');

/** Os pontos fortes de um personagem (no máximo dois, o maior primeiro). */
export function pontoForte(c: { id: string; interval: number }): Forca[] {
  return (pontosFortes[c.id] ?? []).slice(0, 2).map((x) =>
    // o ritmo pode ter mudado no equilíbrio: vale o de agora
    x.tipo === 'rapido' ? { ...x, motivo: x.motivo.replace(/a cada [\d.,]+ s/, `a cada ${decimal(c.interval)} s`) } : { ...x });
}
