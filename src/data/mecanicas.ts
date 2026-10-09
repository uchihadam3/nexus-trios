import type { Character, Effect, StatusId } from '../engine/types';

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

/**
 * Provocar: a habilidade deixa os rivais Provocados por `duracao` segundos (só
 * miram em quem provocou). `troca`: o Status que sai para dar lugar — o
 * personagem não ganha mais um efeito, ganha um diferente.
 */
export const PROVOCAR: Record<string, { habilidade: number; duracao: number; troca?: StatusId }> = {
  captain: { habilidade: 1, duracao: 4 }, // "Eu posso o dia todo"
  hulk: { habilidade: 1, duracao: 4, troca: 'slow' }, // o Rugido chama a briga para ele
  bowser: { habilidade: 1, duracao: 3.5 }, // o rei Koopa ruge e fica mais pesado
  eren: { habilidade: 1, duracao: 4 }, // endurece e atrai o golpe para o titã
};

type Mudanca = (effects: Effect[]) => Effect[];
const mudancasDe = (id: string): Map<number, Mudanca[]> => {
  const m = new Map<number, Mudanca[]>();
  const poe = (i: number, f: Mudanca) => m.set(i, [...(m.get(i) ?? []), f]);
  const reviver = REVIVER[id], provocar = PROVOCAR[id];
  if (reviver) poe(reviver.habilidade, (e) => [...e, { kind: 'revive', value: reviver.vida, target: 'allyFallen' }]);
  if (provocar) poe(provocar.habilidade, (e) => [
    ...e.filter((x) => !(provocar.troca && x.kind === 'status' && x.status === provocar.troca)),
    { kind: 'status', status: 'provoked', value: 1, duration: provocar.duracao, target: 'allEnemies' },
  ]);
  return m;
};

export function aplicaMecanicas(c: Character): Character {
  const renascer = RENASCER[c.id], mudancas = mudancasDe(c.id);
  if (!renascer && !mudancas.size) return c;
  return {
    ...c,
    ...(renascer ? { renascer } : {}),
    skills: c.skills.map((s, i) => {
      const fs = mudancas.get(i);
      return fs ? { ...s, effects: fs.reduce((e, f) => f(e), [...s.effects]) } : s;
    }) as Character['skills'],
  };
}
