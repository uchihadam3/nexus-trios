import type { Character, Effect, Skill } from '../engine/types';
import { PESO_DA_CONDICAO } from './peso-da-condicao';

/*
 * Habilidade difícil de usar é mais forte (pedido do jogador: "medir o quão
 * difícil é… se a habilidade tá forte pela condição dela"). O peso de cada
 * habilidade com condição vem de scripts/medir-condicoes.ts: quanto mais
 * tempo ela fica cheia esperando a condição (ou o combo), maior o dano, a
 * cura e o Escudo quando sai — até +40%. O equilíbrio de força acerta o total
 * do personagem depois.
 */
const reforca = (e: Effect, m: number): Effect =>
  e.kind === 'damage' || e.kind === 'heal' || e.kind === 'shield' ? { ...e, value: Math.round(e.value * m) } : e;

export const aplicaCondicao = (c: Character): Character => {
  if (!c.skills.some((_, i) => PESO_DA_CONDICAO[`${c.id}:${i}`])) return c;
  const skills = c.skills.map((s, i) => {
    const m = PESO_DA_CONDICAO[`${c.id}:${i}`];
    return m ? { ...s, effects: s.effects.map((e) => reforca(e, m)) } : s;
  }) as [Skill, Skill, Skill];
  return { ...c, skills };
};
