/*
 * A Jornada com os seus (pedido do jogador): o trio sai só dos personagens que a conta já liberou nas Conquistas
 * (emprestado não vale) e só na Jornada normal. Devolve o motivo da recusa, ou null quando pode.
 */
import { characters } from '../../../src/data/characters.ts';

export function recusaDaColecao(team: readonly string[], minhas: ReadonlySet<string>, modo: 'daily' | 'weekly' | 'free'): string | null {
  if (modo !== 'free') return 'A Jornada com os seus é só na Jornada normal.';
  const falta = team.filter((id) => !minhas.has(id));
  if (!falta.length) return null;
  const nomes = falta.map((id) => characters.find((c) => c.id === id)?.name ?? id).join(', ');
  return `${nomes} ainda não ${falta.length === 1 ? 'está liberado' : 'estão liberados'} na sua conta.`;
}
