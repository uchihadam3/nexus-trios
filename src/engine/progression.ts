/*
 * FASE H · progressão local: conquistas, Maestria e estatísticas.
 *
 * Esta versão tirou os Objetivos — de jornada, diários e semanais — por pedido
 * da direção, e a razão vale registrar porque é de desenho, não de gosto.
 *
 * Os diários e semanais são um calendário: expiram se você não jogar hoje.
 * Isso funciona num jogo de serviço com servidor; aqui é um jogo que se abre
 * quando dá vontade, e um calendário vira cobrança. Os de jornada somem quando
 * a jornada acaba, então cumprir um não deixa rastro nenhum. E os três grupos
 * pediam a mesma coisa que as conquistas pedem — vencer com os três de pé,
 * interromper Preparos, curar o trio — só que piores: eram contadores, e o
 * próprio documento já proibia grind.
 *
 * O que ficou no lugar: 52 conquistas de **momento**, em `conquistas.ts`, cada
 * uma verificada contra o que o combate produziu, e a Maestria dos 250, que
 * agora mede feitos mecânicos em vez de contar usos de habilidade.
 *
 * A progressão continua sendo prestígio: nível, título e registro. Nenhum
 * ponto de XP altera um atributo de personagem.
 */
import { characters } from '../data/characters';
import { statuses } from '../data/statuses';
import { conquistas, conquistasDaBatalha, type Contexto } from './conquistas';
import { grauAlcancado, somarFeitos, type Feitos } from './maestria';
import type { RunBattleSummary } from './run-summary';
import type { Battle, BattleEvent } from './types';

/* ---------------------------------------------------------------------------
 * Estatísticas
 * ------------------------------------------------------------------------- */

export type Metric = 'battles' | 'wins' | 'journeys' | 'champions' | 'perfect' | 'damage'
  | 'healing' | 'protection' | 'interrupts' | 'statuses' | 'turns' | 'synergies'
  | 'unique' | 'universes' | 'trios' | 'skills' | 'kos';
export type Counters = Record<Metric, number>;
export const emptyCounters = (): Counters => ({
  battles: 0, wins: 0, journeys: 0, champions: 0, perfect: 0, damage: 0, healing: 0,
  protection: 0, interrupts: 0, statuses: 0, turns: 0, synergies: 0, unique: 0,
  universes: 0, trios: 0, skills: 0, kos: 0,
});

export interface ProgressState {
  xp: number; title: string;
  /** Personagens que já entraram na arena alguma vez. */
  seen: string[];
  /** Ids das conquistas já obtidas. */
  unlocked: string[];
  stats: Counters;
  /** Feitos acumulados por personagem, que alimentam a Maestria. */
  mastery: Record<string, Feitos>;
}

type EventTally = { lastId: number; statuses: number; interrupts: number; turns: number; synergies: number };
export const emptyTally = (): EventTally => ({ lastId: 0, statuses: 0, interrupts: 0, turns: 0, synergies: 0 });

export function nexusLevel(xp: number) { return Math.max(1, Math.floor(Math.sqrt(Math.max(0, xp) / 100)) + 1); }
export function emptyProgress(): ProgressState {
  return { xp: 0, title: 'Explorador Nexus', seen: [], unlocked: [], stats: emptyCounters(), mastery: {} };
}

/** Quantos personagens chegaram à Maestria III. */
export const dominados = (p: ProgressState): number =>
  Object.entries(p.mastery).filter(([id, f]) => grauAlcancado(id, f) === 3).length;

/* ---------------------------------------------------------------------------
 * Leitura dos eventos
 * ------------------------------------------------------------------------- */

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

export function battleDelta(summary: RunBattleSummary, battle: Battle, tally: EventTally, seen: string[], team: string[]): Counters {
  const next = emptyCounters();
  next.battles = 1;
  next.wins = Number(summary.won);
  next.perfect = Number(summary.won && summary.survivors === 3);
  next.damage = summary.fighters.reduce((n, f) => n + f.damage, 0);
  next.healing = summary.fighters.reduce((n, f) => n + f.healing, 0);
  next.protection = summary.fighters.reduce((n, f) => n + f.protection, 0);
  next.interrupts = Math.max(tally.interrupts, summary.fighters.reduce((n, f) => n + f.interrupts, 0));
  next.statuses = tally.statuses;
  next.turns = tally.turns;
  next.synergies = tally.synergies;
  next.kos = summary.fighters.reduce((n, f) => n + f.kills, 0);
  next.skills = battle.fighters.filter((f) => f.side === 'player').reduce((n, f) => n + f.skills.reduce((m, s) => m + s.uses, 0), 0);
  next.unique = team.filter((id) => !seen.includes(id)).length;
  next.universes = new Set(team.map((id) => characters.find((c) => c.id === id)?.universe)).size;
  next.trios = 1;
  return next;
}

/* ---------------------------------------------------------------------------
 * Registro
 * ------------------------------------------------------------------------- */

/** O que uma batalha concluída entrega para a progressão. */
export interface Fechamento {
  delta: Counters;
  battle: Battle;
  team: string[];
  /** Feitos de cada personagem nesta batalha, de `fecharFeitos`. */
  feitos: Record<string, Feitos>;
  raioX: Contexto['raioX'];
  maiorAtraso: number;
  indice: number;
  jornada: readonly RunBattleSummary[];
  jornadaTerminou?: boolean;
  campeao?: boolean;
}

export function recordProgress(state: ProgressState, f: Fechamento): ProgressState {
  const stats = { ...state.stats };
  for (const key of Object.keys(stats) as Metric[]) stats[key] += f.delta[key];
  if (f.jornadaTerminou) { stats.journeys += 1; if (f.campeao) stats.champions += 1; }

  const seen = [...new Set([...state.seen, ...f.team])];

  /* A Maestria soma os feitos da batalha ao que o personagem já tinha. */
  const mastery = { ...state.mastery };
  for (const [id, novos] of Object.entries(f.feitos)) mastery[id] = somarFeitos(mastery[id] ?? {}, novos);

  const antesDominados = dominados(state);
  const depoisDominados = Object.entries(mastery).filter(([id, x]) => grauAlcancado(id, x) === 3).length;

  const contexto: Contexto = {
    battle: f.battle, feitos: f.feitos, raioX: f.raioX, time: f.team,
    venceu: f.battle.winner === 'player', campeao: f.campeao ?? false,
    maiorAtraso: f.maiorAtraso, indice: f.indice, jornada: f.jornada,
    vistos: state.seen, dominados: depoisDominados,
  };
  const novas = conquistasDaBatalha(contexto, state.unlocked);
  const unlocked = [...state.unlocked, ...novas];

  /*
   * XP é prestígio: nível e título, nunca atributo. Vencer dá mais que perder,
   * conquistar dá mais que vencer, e dominar um personagem dá mais que tudo.
   */
  /* `campeao` é opcional: sem o `?? false`, `Number(undefined)` envenena o XP com NaN. */
  const xp = state.xp + 20 + f.delta.wins * 30 + Number(f.campeao ?? false) * 250
    + novas.length * 90 + Math.max(0, depoisDominados - antesDominados) * 150;

  return { ...state, xp, seen, stats, mastery, unlocked };
}

export { conquistas };
export type { Conquista, Categoria } from './conquistas';
