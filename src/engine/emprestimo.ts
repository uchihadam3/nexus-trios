/*
 * O Empréstimo do dia (pedido do jogador): todo dia, 9 personagens sorteados ficam liberados para todo mundo no PvP
 * (o Treino e o Desafio online), além da coleção de cada um. São os mesmos 9 para todos, trocam à meia-noite (horário
 * de Brasília) e podem ser qualquer um dos 400. Quem já tem um deles na coleção não ganha um segundo: o personagem é
 * um só (os 3 times nunca repetem personagem), então o empréstimo só soma quem você ainda não tem.
 *
 * O servidor (supabase/functions/ranked-api/pvp.ts) usa a mesma conta para aceitar os times do Desafio online.
 */
import { characters } from '../data/characters';

export const EMPRESTADOS_POR_DIA = 9;
/** O dia do empréstimo troca à meia-noite de Brasília (UTC−3). */
const FUSO_MS = 3 * 3600 * 1000;

/** O dia do empréstimo ("2026-10-16") de um instante. */
export const diaDoEmprestimo = (agora: Date | number = Date.now()) => new Date((typeof agora === 'number' ? agora : agora.getTime()) - FUSO_MS).toISOString().slice(0, 10);

/** Quanto falta (ms) para os emprestados trocarem. */
export function faltaParaTrocar(agora: number = Date.now()) {
  const local = agora - FUSO_MS, dia = 24 * 3600 * 1000;
  return dia - (((local % dia) + dia) % dia);
}

/* o mesmo sorteio em todo aparelho e no servidor: FNV-1a do dia e xorshift */
function semente(texto: string) {
  let h = 0x811c9dc5;
  for (let i = 0; i < texto.length; i++) { h ^= texto.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return h || 1;
}

/** Os 9 emprestados de um dia: qualquer um dos 400, sem repetir. */
export function emprestadosDoDia(dia: string = diaDoEmprestimo()): string[] {
  let s = semente(`emprestimo:${dia}`);
  const r = () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  const ids = characters.map((c) => c.id), escolhidos: string[] = [];
  while (escolhidos.length < EMPRESTADOS_POR_DIA) {
    const id = ids.splice(Math.floor(r() * ids.length), 1)[0]!;
    escolhidos.push(id);
  }
  return escolhidos;
}

/** A coleção do PvP: a sua e os emprestados do dia (um personagem só aparece uma vez). */
export const comEmprestados = (colecao: readonly string[], dia: string = diaDoEmprestimo()) => [...new Set([...colecao, ...emprestadosDoDia(dia)])];
