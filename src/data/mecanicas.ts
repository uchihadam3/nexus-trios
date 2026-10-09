import type { Character } from '../engine/types';

/*
 * Mecânicas novas, por personagem (pedido do jogador: "levantar personagem
 * caído" e o resto da lista). Cada uma entra só em quem tem isso na história,
 * e o equilíbrio de força (src/data/ajuste-de-forca.ts) mede o personagem já
 * com ela.
 */

/** Reviver: a habilidade (índice) levanta o aliado caído mais forte com esta fração da Vida. */
export const REVIVER: Record<string, { habilidade: number; vida: number }> = {
  sailormoon: { habilidade: 2, vida: 0.4 }, // o Cristal de Prata devolve o trio à luta
  sora: { habilidade: 1, vida: 0.35 }, // Cura (Vida+): levanta quem caiu
};

/** Renascer: ao cair, volta sozinho depois de `atraso` segundos com esta fração da Vida. */
export const RENASCER: Record<string, { vida: number; atraso: number }> = {
  ikki: { vida: 0.5, atraso: 1.5 }, // a Fênix sempre volta das cinzas
  jeangrey: { vida: 0.4, atraso: 2 }, // a Força Fênix
  deadpool: { vida: 0.35, atraso: 2 }, // o fator de cura não deixa ele morrer
  majinbuu: { vida: 0.35, atraso: 2.5 }, // se refaz de qualquer pedaço
  mummra: { vida: 0.4, atraso: 2.5 }, // "Antigos Espíritos do Mal…": volta do sarcófago
  cell: { vida: 0.3, atraso: 2.5 }, // volta inteiro de uma célula só
};

export function aplicaMecanicas(c: Character): Character {
  const reviver = REVIVER[c.id], renascer = RENASCER[c.id];
  if (!reviver && !renascer) return c;
  return {
    ...c,
    ...(renascer ? { renascer } : {}),
    skills: c.skills.map((s, i) =>
      reviver && i === reviver.habilidade ? { ...s, effects: [...s.effects, { kind: 'revive' as const, value: reviver.vida, target: 'allyFallen' as const }] } : s) as Character['skills'],
  };
}
