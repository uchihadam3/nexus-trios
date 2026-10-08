/*
 * A contagem de eventos de uma luta.
 *
 * Restou do sistema de progressão (XP, conquistas e Maestria, que saíram do
 * jogo: o objetivo agora é só fazer pontos e subir no ranking). O servidor do
 * ranking usa esta contagem para as viradas a favor do trio.
 */
import type { BattleEvent } from './types';
import { statuses } from '../data/statuses';

export type EventTally = { lastId: number; statuses: number; interrupts: number; turns: number; synergies: number };
export const emptyTally = (): EventTally => ({ lastId: 0, statuses: 0, interrupts: 0, turns: 0, synergies: 0 });

export function tallyEvents(tally: EventTally, events: BattleEvent[]): EventTally {
  const next = { ...tally };
  for (const e of events) {
    if (e.id <= next.lastId) continue;
    next.lastId = e.id;
    if (!e.source.startsWith('player-')) continue;
    if (e.kind === 'status' && e.status && statuses[e.status].tone === 'negativo' && e.target?.startsWith('enemy-')) next.statuses += 1;
    if (e.kind === 'interrupt') next.interrupts += 1;
    if (e.kind === 'turn') next.turns += 1;
    if (e.kind === 'synergy' && e.target?.startsWith('player-')) next.synergies += 1;
  }
  return next;
}
