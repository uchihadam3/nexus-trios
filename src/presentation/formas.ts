import type { Character, Fighter } from '../engine/types';

/**
 * Formas que trocam o retrato no meio da luta: Gandalf volta pela mecânica "O Branco" como Gandalf, o Branco, e o
 * Ben 10 vira o alien que o Omnitrix sorteou (se o Omnitrix falha, segue o Ben). O medalhão e a ficha mostram a forma
 * de agora, e cada troca nasce de um clarão na cor da forma.
 */
interface Forma { retrato: string; nome: string; cor: string }
const DIR = '/assets/portraits/formas/';
/** Os aliens na ordem do Omnitrix (src/engine/unicas-lote9.ts: 0 Quatro Braços, 1 Chama, 2 XLR8, 3 Diamante, 4 falhou). */
const ALIENS: Forma[] = [
  { retrato: `${DIR}ben10-quatro-bracos.webp`, nome: 'Quatro Braços', cor: '#ff5a4a' },
  { retrato: `${DIR}ben10-chama.webp`, nome: 'Chama', cor: '#ffb43a' },
  { retrato: `${DIR}ben10-xlr8.webp`, nome: 'XLR8', cor: '#3fd8e8' },
  { retrato: `${DIR}ben10-diamante.webp`, nome: 'Diamante', cor: '#8dffb8' },
];
const FORMAS: Record<string, { de: (f: Fighter) => Forma | null; todas: Forma[] }> = {
  gandalf: {
    de: (f) => (f.voltou && (f.u?.branco ?? 0) >= 1 ? FORMAS.gandalf!.todas[0]! : null),
    todas: [{ retrato: `${DIR}gandalf-branco.webp`, nome: 'Gandalf, o Branco', cor: '#fffbe8' }],
  },
  ben10: { de: (f) => ALIENS[f.u?.alien ?? -1] ?? null, todas: ALIENS },
};

/** A forma de agora do lutador, se ele trocou de forma. */
export const formaDe = (f: Fighter): Forma | null => FORMAS[f.characterId]?.de(f) ?? null;

/** O personagem como ele aparece agora: com o retrato (e o nome) da forma nova, se trocou. */
export function naFormaDeAgora(c: Character, f: Fighter): Character {
  const forma = formaDe(f);
  return forma ? { ...c, portrait: forma.retrato, name: forma.nome } : c;
}

/** Baixa antes os retratos das formas, para a troca não piscar vazia no meio da luta. */
export function preCarregaFormas(ids: readonly string[]): void {
  if (typeof Image === 'undefined') return;
  for (const id of ids) for (const forma of FORMAS[id]?.todas ?? []) new Image().src = forma.retrato;
}
