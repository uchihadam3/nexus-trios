import type { Character, Fighter } from '../engine/types';

/**
 * Formas que trocam o retrato no meio da luta. Gandalf cai, volta pela mecânica "O Branco" e daí em diante
 * aparece como Gandalf, o Branco, no medalhão e na ficha.
 */
const FORMAS: Record<string, { ativa: (f: Fighter) => boolean; retrato: string; nome: string }> = {
  gandalf: { ativa: (f) => !!f.voltou && (f.u?.branco ?? 0) >= 1, retrato: '/assets/portraits/formas/gandalf-branco.webp', nome: 'Gandalf, o Branco' },
};

/** A forma de agora do lutador, se ele trocou de forma. */
export const formaDe = (f: Fighter) => {
  const forma = FORMAS[f.characterId];
  return forma && forma.ativa(f) ? forma : null;
};

/** O personagem como ele aparece agora: com o retrato (e o nome) da forma nova, se trocou. */
export function naFormaDeAgora(c: Character, f: Fighter): Character {
  const forma = formaDe(f);
  return forma ? { ...c, portrait: forma.retrato, name: forma.nome } : c;
}

/** Baixa antes o retrato da forma nova, para a troca não piscar vazia no meio da luta. */
export function preCarregaFormas(ids: readonly string[]): void {
  if (typeof Image === 'undefined') return;
  for (const id of ids) if (FORMAS[id]) new Image().src = FORMAS[id].retrato;
}
