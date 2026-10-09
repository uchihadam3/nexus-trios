/*
 * Atuação (adendo, parte 2): quem age se move, quem recebe reage.
 *
 * A regra do adendo é que, assistindo sem ler nada, fique óbvio quem fez o quê.
 * Por isso cada ação ganha um estilo de quem age — avança e volta, dispara e
 * recua, pulsa para o aliado — e cada alvo ganha uma reação — é empurrado para
 * trás, brilha de cura, ganha a bolha do escudo.
 *
 * Nada aqui decide combate: lê só o que o motor já calculou (o beat e as
 * consequências dele). O movimento é desenhado em CSS a partir dos números que
 * saem daqui: direção em pixels até o alvo, distância, duração do beat.
 */
import type { Battle } from '../engine/types';
import type { Beat } from './director';
import { combatLinks } from './combat-links';
import { profileFor } from './vfxProfiles';

export type ActStyle = 'melee' | 'ranged' | 'area' | 'support' | 'curse' | 'cast' | 'interrupt';
export type ReactStyle = 'hit' | 'hit-heavy' | 'block' | 'heal' | 'shield' | 'buff' | 'curse' | 'broken' | 'fall';

export interface UnitActing {
  /** Quem age: o estilo do movimento e o vetor até o alvo principal, em px. */
  act?: ActStyle;
  /** Quem recebe: a reação, e de onde veio o golpe (vetor unitário). */
  react?: ReactStyle;
  dx: number; dy: number;
  /** Vetor unitário na direção do alvo (de quem age) ou da origem para o alvo (de quem recebe). */
  ux: number; uy: number;
  /** Duração do beat em segundos de apresentação a 1×. */
  seconds: number;
  /** Alterna a cada beat, para a animação recomeçar mesmo com o mesmo estilo. */
  parity: 'a' | 'b';
}

export interface Medida { anchors: Record<string, { x: number; y: number }>; w: number; h: number; medal: number }

/* Famílias que viajam: o golpe nasce em quem age e atravessa o palco. */
const VIAJAM = new Set(['energy', 'electric', 'fire', 'magic', 'psychic', 'dark']);

function estiloDeQuemAge(beat: Beat, battle: Battle, area: boolean): ActStyle | undefined {
  const { event } = beat;
  if (event.kind === 'cast') return 'cast';
  if (event.kind === 'interrupt') return 'interrupt';
  if (event.kind !== 'basic' && event.kind !== 'skill') return undefined;
  const links = combatLinks(beat, battle).filter((l) => l.source === event.source);
  const ataca = links.some((l) => l.kind === 'attack' || l.kind === 'interrupt');
  if (!ataca && links.length && links.every((l) => ['heal', 'shield', 'buff', 'support'].includes(l.kind))) return 'support';
  if (!ataca && links.some((l) => l.kind === 'debuff')) return 'curse';
  if (area) return 'area';
  const source = battle.fighters.find((f) => f.uid === event.source);
  const profile = profileFor(source?.characterId ?? '', event.skill);
  if (profile?.travel || VIAJAM.has(beat.family)) return 'ranged';
  return 'melee';
}

function reacaoDoAlvo(beat: Beat, battle: Battle, uid: string): ReactStyle | undefined {
  if (!beat.impacted) return undefined;
  const sobre = beat.events.filter((e) => e.target === uid);
  if (!sobre.length) return undefined;
  if (sobre.some((e) => e.kind === 'revive')) return 'heal';
  if (sobre.some((e) => e.kind === 'ko')) return 'fall';
  if (sobre.some((e) => e.kind === 'interrupt')) return 'broken';
  // o golpe bateu no escudo: o escudo aparece na frente e leva a pancada
  if (sobre.some((e) => e.kind === 'block')) return 'block';
  const dano = sobre.filter((e) => e.kind === 'damage').reduce((t, e) => t + (e.value ?? 0), 0);
  if (dano > 0) {
    const alvo = battle.fighters.find((f) => f.uid === uid);
    return beat.grand || (alvo && dano >= alvo.maxHp * 0.16) ? 'hit-heavy' : 'hit';
  }
  if (sobre.some((e) => e.kind === 'heal')) return 'heal';
  if (sobre.some((e) => e.kind === 'shield')) return 'shield';
  const origem = battle.fighters.find((f) => f.uid === beat.event.source)?.side;
  const lado = battle.fighters.find((f) => f.uid === uid)?.side;
  if (sobre.some((e) => e.kind === 'status')) return origem === lado ? 'buff' : 'curse';
  return undefined;
}

/** O que cada lutador faz neste beat. Lutadores sem papel ficam de fora. */
export function atuacao(beat: Beat | null, battle: Battle, medida: Medida, area: boolean): Record<string, UnitActing> {
  const out: Record<string, UnitActing> = {};
  if (!beat || beat.periodic || beat.event.kind === 'turn' || !medida.w) return out;
  const px = (uid: string) => {
    const a = medida.anchors[uid];
    return a ? { x: (a.x * medida.w) / 100, y: (a.y * medida.h) / 100 } : null;
  };
  const parity = beat.event.id % 2 ? 'a' : 'b';
  const fonte = px(beat.event.source);
  const links = combatLinks(beat, battle);
  const alvos = [...new Set(links.filter((l) => l.source === beat.event.source).map((l) => l.target))];
  const principal = beat.event.target ?? alvos[0];

  /* O ponto para onde quem age se volta: o alvo, ou o centro dos alvos numa área. */
  const pontos = (area ? alvos : [principal]).map((uid) => (uid ? px(uid) : null)).filter((p): p is { x: number; y: number } => !!p);
  const destino = pontos.length ? { x: pontos.reduce((s, p) => s + p.x, 0) / pontos.length, y: pontos.reduce((s, p) => s + p.y, 0) / pontos.length } : null;

  const act = estiloDeQuemAge(beat, battle, area);
  if (act && fonte) {
    let dx = 0, dy = 0, ux = 0, uy = 0;
    if (destino) {
      const vx = destino.x - fonte.x, vy = destino.y - fonte.y, dist = Math.hypot(vx, vy) || 1;
      ux = vx / dist; uy = vy / dist;
      /* Corpo a corpo vai até encostar no alvo; o resto só se inclina para ele. */
      const ate = act === 'melee' || act === 'interrupt' ? Math.max(dist * 0.4, dist - medida.medal * 0.82) : Math.min(26, dist * 0.12);
      dx = ux * ate; dy = uy * ate;
    }
    out[beat.event.source] = { act, dx, dy, ux, uy, seconds: beat.duration, parity };
  }

  for (const f of battle.fighters) {
    if (f.uid === beat.event.source) continue;
    const react = reacaoDoAlvo(beat, battle, f.uid);
    if (!react) continue;
    const p = px(f.uid);
    let ux = 0, uy = 0;
    if (p && fonte) { const vx = p.x - fonte.x, vy = p.y - fonte.y, d = Math.hypot(vx, vy) || 1; ux = vx / d; uy = vy / d; }
    out[f.uid] = { react, dx: 0, dy: 0, ux, uy, seconds: beat.duration, parity };
  }
  return out;
}
