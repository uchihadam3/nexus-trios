import type { Skill, Target } from './types';

/*
 * "Alvo ferido" (condição `injured`): de quem é a Vida que importa.
 *
 * Pedido do jogador: "se a habilidade tem cura, o alvo tem que ser o aliado —
 * esperar o inimigo estar com 78% para atacar não faz sentido". Se a
 * habilidade cura ou protege alguém do próprio trio (cura, Escudo,
 * Regeneração, Protegido, Barreira), a condição olha a Vida de quem recebe
 * isso; senão, a do alvo da habilidade (o golpe que espera o rival ferido).
 */
const SUSTENTO = new Set(['regen', 'protected', 'barrier']);
const DO_TRIO: Target[] = ['self', 'allyWeak', 'allAllies', 'allyStrongest'];

export function alvosDoFerido(s: Skill): Target[] {
  const cura = s.effects.filter((e) => (e.kind === 'heal' || e.kind === 'shield' || (e.kind === 'status' && SUSTENTO.has(e.status)))
    && DO_TRIO.includes(e.target ?? s.target));
  return cura.length ? [...new Set(cura.map((e) => e.target ?? s.target))] : [s.target];
}

/** Como a ficha diz de quem é a Vida que precisa estar abaixo de 78%. */
export function textoDoFerido(s: Skill): string {
  const alvos = alvosDoFerido(s);
  if (alvos.every((t) => t === 'self')) return 'ele mesmo estiver com menos de 78% de Vida';
  if (alvos.some((t) => DO_TRIO.includes(t))) return 'um aliado (ou ele mesmo) estiver com menos de 78% de Vida';
  return 'o inimigo estiver com menos de 78% de Vida';
}
