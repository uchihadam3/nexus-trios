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
import { PRESENTATION as P } from './config';
import { etapaDoEvento, revelado, type Beat } from './director';
import { DESVIA_NA_UNICA, ativacaoNaTela, entregaDoEvento, golpeParado, type AtivacaoNaTela } from './ativacao-da-unica';
import { combatLinks } from './combat-links';
import { distanciaDoGolpe } from './distancia';
import { familia, profileFor } from './vfxProfiles';
import { GUARDA_DE_CORPO } from './entrega-de-apoio';

export type ActStyle = 'melee' | 'ranged' | 'area' | 'support' | 'curse' | 'cast' | 'interrupt' | 'esquiva';
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
  /** O golpe parou no meio do caminho: quem foi atacado está respondendo com a Mecânica única. */
  pausado?: boolean;
  /** Fica parado (na aura) e dispara de uma vez até o alvo: o golpe cuja faixa é o rastro de quem avança (o Kaioken). */
  relampago?: boolean;
  /** Alterna a cada passo da cadeia em que o lutador reage de novo (o dano da Mecânica única depois do golpe). */
  reacaoPar?: 'a' | 'b';
}

export interface Medida { anchors: Record<string, { x: number; y: number }>; w: number; h: number; medal: number }

/* Famílias que viajam: o golpe nasce em quem age e atravessa o palco. */
const VIAJAM = new Set(['energy', 'electric', 'fire', 'magic', 'psychic', 'dark']);

function estiloDeQuemAge(beat: Beat, battle: Battle, area: boolean): ActStyle | undefined {
  const { event } = beat;
  if (event.kind === 'cast') return 'cast';
  if (event.kind === 'interrupt') return 'interrupt';
  // a Mecânica única sozinha: o movimento sai das fases dela (atuaNaAtivacao)
  if (event.kind === 'unica' && beat.traco) return undefined;
  if (event.kind !== 'basic' && event.kind !== 'skill') return undefined;
  const links = combatLinks(beat, battle).filter((l) => l.source === event.source);
  const ataca = links.some((l) => l.kind === 'attack' || l.kind === 'interrupt');
  if (!ataca && links.length && links.every((l) => ['heal', 'shield', 'buff', 'support'].includes(l.kind))) {
    // quem protege com o próprio corpo vai até o aliado (o Wolverine na frente dele, o Superman segurando)
    const quem = battle.fighters.find((f) => f.uid === event.source);
    return quem && event.kind === 'skill' && GUARDA_DE_CORPO.has(`${quem.characterId}:${event.skill}`) && event.target && event.target !== event.source ? 'melee' : 'support';
  }
  if (!ataca && links.some((l) => l.kind === 'debuff')) return 'curse';
  if (area) return 'area';
  const source = battle.fighters.find((f) => f.uid === event.source);
  const profile = profileFor(source?.characterId ?? '', event.skill);
  // o efeito que aparece decide: lâmina e soco vão até o alvo, tiro e magia ficam de longe
  const distancia = profile && distanciaDoGolpe(source?.characterId ?? '', event.kind === 'skill' ? event.skill : undefined, profile.family);
  if (distancia) return distancia === 'perto' ? 'melee' : 'ranged';
  if (profile?.travel || VIAJAM.has(beat.family)) return 'ranged';
  return 'melee';
}

function estiloDaAtivacao(at: AtivacaoNaTela, beat: Beat, battle: Battle): ActStyle | undefined {
  const dono = battle.fighters.find((f) => f.uid === at.passo.quem);
  if (at.pausa && dono && DESVIA_NA_UNICA.has(dono.characterId)) return 'esquiva';
  if (at.t < at.fases.soltaEm || at.pausa) return 'cast';
  const e = at.evento ?? beat.event;
  const ent = entregaDoEvento(e, battle, beat);
  if (ent.modo === 'si') return at.fases.preparo > 0 ? 'cast' : undefined;
  if (ent.modo === 'corpo') return 'melee';
  if (ent.modo === 'aliado') return 'support';
  if (ent.modo === 'alvo') return 'curse';
  return 'ranged';
}
/** Quanto dura o movimento de quem ativa: a subida da concentração, ou da soltura até o impacto. */
function segundosDaAtivacao(at: AtivacaoNaTela, act: ActStyle): number {
  if (act === 'esquiva') return 0.45;
  if (act === 'cast') return Math.max(0.9, at.fases.nomeEm * 4);
  return Math.max(0.5, (at.fases.efeitoEm - at.fases.soltaEm) / P.impactAt);
}

/*
 * A reação acompanha o passo da cadeia que chegou por último no lutador (pedido do jogador: "o Deidara explode…
 * não tem impacto nenhum nos personagens"): o dano da Mecânica única que vem depois do golpe faz o alvo reagir de
 * novo, na hora em que chega, e não junto do golpe.
 */
function reacaoDoAlvo(beat: Beat, battle: Battle, uid: string): { react: ReactStyle; etapa: number } | undefined {
  if (!beat.impacted) return undefined;
  const todos = beat.events.filter((e) => e.target === uid && revelado(beat, e));
  if (!todos.length) return undefined;
  const etapa = Math.max(...todos.map((e) => etapaDoEvento(beat, e)));
  const react = estiloDaReacao(beat, battle, uid, todos.filter((e) => etapaDoEvento(beat, e) === etapa));
  return react ? { react, etapa } : undefined;
}
function estiloDaReacao(beat: Beat, battle: Battle, uid: string, sobre: Beat['events']): ReactStyle | undefined {
  if (!sobre.length) return undefined;
  if (sobre.some((e) => e.kind === 'revive')) return 'heal';
  if (sobre.some((e) => e.kind === 'cleanse')) return 'buff';
  if (sobre.some((e) => e.kind === 'dispel')) return 'curse';
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
  // quem age vai até o rival que o golpe acerta (no Cólera do Dragão, o rival, não o aliado curado)
  const ladoDe = (uid?: string) => battle.fighters.find((f) => f.uid === uid)?.side;
  const ladoDoAtor = ladoDe(beat.event.source);
  const golpeNoRival = beat.events.find((e) => e.source === beat.event.source && e.kind === 'damage' && !!e.target && ladoDe(e.target) !== ladoDoAtor)?.target;
  const principal = (beat.event.target && ladoDe(beat.event.target) !== ladoDoAtor ? beat.event.target : golpeNoRival) ?? beat.event.target ?? alvos[0];

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
    // o movimento de quem age dura o golpe, não a cadeia toda: ele volta ao lugar antes da cura no aliado
    // (parado: o golpe espera alguém ativar a Mecânica única no meio do caminho)
    const parada = golpeParado(beat);
    const perfil = act === 'melee' ? profileFor(battle.fighters.find((f) => f.uid === beat.event.source)?.characterId ?? '', beat.event.skill) : undefined;
    const relampago = !!perfil && !!familia(perfil.family).rastro;
    out[beat.event.source] = { act, dx, dy, ux, uy, seconds: beat.base ?? beat.duration, parity, pausado: !!parada && !parada.propria, ...(relampago ? { relampago } : {}) };
  }

  for (const f of battle.fighters) {
    const r = reacaoDoAlvo(beat, battle, f.uid);
    // quem golpeou só reage ao que chega depois, na cadeia (o Deidara que explode em quem o derrubou)
    if (!r || (f.uid === beat.event.source && r.etapa <= 1)) continue;
    const p = px(f.uid);
    let ux = 0, uy = 0;
    if (p && fonte) { const vx = p.x - fonte.x, vy = p.y - fonte.y, d = Math.hypot(vx, vy) || 1; ux = vx / d; uy = vy / d; }
    // depois do golpe, a reação dura o seu passo (curta e seca), não o beat inteiro
    const seconds = r.etapa > 1 ? Math.min(beat.duration, 1.1) : beat.duration;
    out[f.uid] = { react: r.react, dx: 0, dy: 0, ux, uy, seconds, parity, reacaoPar: (beat.event.id + r.etapa) % 2 ? 'b' : 'a' };
  }
  /*
   * Quem está ativando a Mecânica única agora (sozinha, na pausa do golpe ou no meio da cadeia) se move como numa
   * habilidade: concentra, e ao soltar vai até o alvo (de perto), dispara (de longe), manda a ajuda ou lança no
   * alvo. O atacante que ativa depois do próprio golpe não troca de movimento: ele ainda está voltando.
   */
  for (const f of battle.fighters) {
    const at = ativacaoNaTela(beat, f.uid);
    if (!at || (f.uid === beat.event.source && !beat.traco && !at.pausa)) continue;
    const atua = atuaNaAtivacao(at, f.uid, beat, battle, px, medida.medal);
    if (atua) out[f.uid] = { ...out[f.uid], ...atua };
  }
  return out;
}

function atuaNaAtivacao(at: AtivacaoNaTela, uid: string, beat: Beat, battle: Battle, px: (uid: string) => { x: number; y: number } | null, medal: number): UnitActing | undefined {
  const act = estiloDaAtivacao(at, beat, battle);
  if (!act) return undefined;
  const e = at.evento ?? beat.event, fonte = px(uid);
  const ent = entregaDoEvento(e, battle, beat);
  const alvos = ent.modo === 'si' ? [] : ent.destino.alvos;
  const pontos = alvos.filter((a) => a !== uid).map(px).filter((p): p is { x: number; y: number } => !!p);
  let dx = 0, dy = 0, ux = 0, uy = 0;
  if (fonte && pontos.length && act !== 'cast') {
    const d = { x: pontos.reduce((s, p) => s + p.x, 0) / pontos.length, y: pontos.reduce((s, p) => s + p.y, 0) / pontos.length };
    const vx = d.x - fonte.x, vy = d.y - fonte.y, dist = Math.hypot(vx, vy) || 1;
    ux = vx / dist; uy = vy / dist;
    const ate = act === 'melee' ? Math.max(dist * 0.4, dist - medal * 0.82) : Math.min(26, dist * 0.12);
    dx = ux * ate; dy = uy * ate;
  }
  return { act, dx, dy, ux, uy, seconds: segundosDaAtivacao(at, act), parity: e.id % 2 ? 'a' : 'b' };
}
