/*
 * A ativação da Mecânica única, nas mesmas fases de uma habilidade (pedido do jogador: "quando eles vão ativar a
 * habilidade, eles… concentrando energia, aí… aparece o nome do que eles vão fazer, e depois… carrega a habilidade e
 * depois ela solta… Na mecânica única"):
 *
 *   concentra · quem ativa sobe e junta energia (a aura e a folha de preparo dele), ainda sem nome;
 *   carga     · o nome aparece com o ícone de "preparando" e o anel de Preparo enche;
 *   solta     · o nome vira o da ativação, quem ativa avança (de perto) ou dispara (de longe) e a entrega viaja;
 *   impacto   · o efeito cai no alvo.
 *
 * O Preparo é de cada personagem (pedido do jogador: "pode ter personagem que pode ser instantâneo… 0,1, 0,2… até
 * 0,5, dependendo de como pode ser feito"): um reflexo (a Valak aparecendo atrás, o Neo desviando) é instantâneo — o
 * nome e o efeito saem juntos —; a Genki Dama, o Tiro devastador e o Fus Ro Dah juntam por 0,5.
 *
 * E quando a mecânica é a resposta a um golpe (a Armadura de Pégaso do Seiya), o golpe do rival para no meio do
 * caminho, quem foi atacado faz as fases dele, e aí o golpe continua e cai na defesa (pedido do jogador: "o ataque
 * da pessoa para e ele ativa… aparecendo o nome… e a armadura, e aí continua e ele defende").
 */
import type { Battle, BattleEvent } from '../engine/types';
import type { Beat, Passo } from './director';
import { ENTREGA_DA_UNICA, VOO_DA_UNICA, entregaDaUnica, type ModoDaEntrega } from './unicas-efeitos';

/** O Preparo de cada um, na mesma escala do Preparo das habilidades (0 = instantâneo). */
export const PREPARO_PROPRIO: Record<string, number> = {
  // reflexos: o nome e o efeito saem juntos
  valak: 0, neo: 0, sans: 0, sekiro: 0, minato: 0, crash: 0, sonic: 0, kenshin: 0, hiei: 0,
  // respostas rápidas ao golpe e golpes de surpresa
  seiya: 0.2, shiryu: 0.1, garou: 0.1, saitama: 0.1, ghostface: 0.1, jason: 0.1, michaelmyers: 0.1, batman: 0.1,
  levi: 0.1, daredevil: 0.1, morty: 0.1, harrypotter: 0.1, xenomorph: 0.1, catwoman: 0.1, blackwidow: 0.1,
  lelouch: 0.2, aizen: 0.2, kakashi: 0.2, coringa: 0.2, yor: 0.2, mikasa: 0.2,
  // o que precisa juntar energia de verdade
  goku: 0.5, megatron: 0.5, madara: 0.5, dovahkiin: 0.5, galactus: 0.5, light: 0.5, kaiba: 0.5, darkseid: 0.4,
  inuyasha: 0.4, cuphead: 0.4, zeus: 0.4, storm: 0.4, ironman: 0.4, mewtwo: 0.4, odin: 0.4, hadescz: 0.4, ursula: 0.4,
};
const PREPARO_DO_MODO: Record<ModoDaEntrega, number> = { si: 0.2, corpo: 0.2, alvo: 0.3, voa: 0.3, aliado: 0.3, raio: 0.4, cai: 0.5 };

export function preparoProprio(personagem: string): number {
  const proprio = PREPARO_PROPRIO[personagem];
  if (proprio !== undefined) return proprio;
  const dela = ENTREGA_DA_UNICA[personagem];
  const base = PREPARO_DO_MODO[dela?.modo ?? 'voa'];
  return dela?.area ? Math.min(0.5, base + 0.1) : base;
}

/** Os instantes de cada fase, em segundos de apresentação desde o começo da ativação. */
export interface FasesDaUnica {
  preparo: number;
  /** o nome aparece (fim da concentração) */
  nomeEm: number;
  /** o anel cheio: quem ativa solta */
  soltaEm: number;
  /** a entrega sai (o projétil, o feixe, quem vai de perto) */
  vooEm: number;
  /** o efeito cai no alvo */
  impactoEm: number;
  /** quanto a entrega viaja */
  voo: number;
}
export function fasesDaUnica(personagem: string, voo: number): FasesDaUnica {
  const preparo = preparoProprio(personagem);
  if (preparo <= 0) return { preparo, nomeEm: 0, soltaEm: 0, vooEm: 0, impactoEm: voo > 0 ? voo : 0.12, voo };
  const nomeEm = 0.25 + preparo * 0.6;
  const soltaEm = nomeEm + 0.15 + preparo;
  const vooEm = soltaEm + 0.12;
  return { preparo, nomeEm, soltaEm, vooEm, impactoEm: voo > 0 ? vooEm + voo : soltaEm + 0.12, voo };
}

/** De quem a Mecânica única atinge, visto por quem ativou: o rival, um aliado ou ela mesma. */
export function ladoDaUnica(e: BattleEvent, b: Battle): 'rival' | 'aliado' | 'si' {
  if (!e.target || e.target === e.source) return 'si';
  const de = b.fighters.find((f) => f.uid === e.source), para = b.fighters.find((f) => f.uid === e.target);
  return de && para && de.side === para.side ? 'aliado' : 'rival';
}
/** Quanto a Mecânica única leva para chegar no alvo depois de soltar (o projétil voando, o feixe crescendo). */
export function vooDaUnica(e: BattleEvent, b: Battle) {
  const f = b.fighters.find((x) => x.uid === e.source);
  if (!f) return 0;
  const ent = entregaDaUnica(f.characterId, ladoDaUnica(e, b));
  return ent.area || (e.target && e.target !== e.source) ? VOO_DA_UNICA[ent.modo] : 0;
}
export function fasesDoEvento(e: BattleEvent, b: Battle): FasesDaUnica {
  const f = b.fighters.find((x) => x.uid === e.source);
  return fasesDaUnica(f?.characterId ?? '', vooDaUnica(e, b));
}

/**
 * A pausa no golpe do rival: quem foi atacado responde com a Mecânica única antes de o golpe cair.
 * `t` corre só enquanto o golpe está parado; `dura` é a ativação inteira (até a defesa aparecer) e um respiro.
 */
export interface PausaDaUnica { quem: string; evento: BattleEvent; passo: number; em: number; dura: number; t: number; fases: FasesDaUnica }
/** Depois de o efeito da defesa aparecer, quanto ele fica à vista antes de o golpe continuar. */
const RESPIRO_DA_PAUSA = 0.45;
export function pausaDoGolpe(beat: Pick<Beat, 'event' | 'events' | 'after' | 'passos'>, impacto: number, antecipa: number): PausaDaUnica | undefined {
  if (beat.event.kind !== 'basic' && beat.event.kind !== 'skill') return undefined;
  const ladoDe = (uid?: string) => beat.after.fighters.find((f) => f.uid === uid)?.side;
  const atacante = beat.event.source, ladoDoAtacante = ladoDe(atacante);
  // quem o golpe acerta (dano, bloqueio ou o golpe que errou nele)
  const atingidos = new Set(beat.events.filter((e) => (e.kind === 'damage' || e.kind === 'block' || e.kind === 'miss') && (e.kind === 'block' ? (e.attacker ?? e.source) : e.source) === atacante && e.target).map((e) => e.target!));
  const k = (beat.passos ?? []).findIndex((p: Passo) => p.classe === 'unica' && p.quem !== atacante && ladoDe(p.quem) !== ladoDoAtacante && atingidos.has(p.quem));
  if (k < 0) return undefined;
  const passo = beat.passos![k]!;
  const evento = beat.events.find((e) => e.kind === 'unica' && passo.eventos.includes(e.id));
  if (!evento) return undefined;
  const fases = fasesDoEvento(evento, beat.after);
  // o golpe para no meio do caminho: quem vai de perto já saiu do lugar, a folha do golpe ainda não começou
  const em = Math.max(0, Math.min(impacto * 0.6, impacto - antecipa - 0.05));
  return { quem: passo.quem, evento, passo: k, em, dura: fases.impactoEm + RESPIRO_DA_PAUSA, t: 0, fases };
}

/** A ativação de um lutador neste quadro: em que ponto ela está (t) e as fases dela. */
export interface AtivacaoNaTela { passo: Passo; evento?: BattleEvent; t: number; fases: FasesDaUnica; pausa: boolean }
export function ativacaoNaTela(beat: Beat | null | undefined, uid: string): AtivacaoNaTela | undefined {
  if (!beat) return undefined;
  if (beat.traco && beat.passos?.[0]?.classe === 'unica' && beat.event.source === uid) {
    return { passo: beat.passos[0], evento: beat.event, t: beat.elapsed, fases: fasesDoEvento(beat.event, beat.after), pausa: false };
  }
  const pausa = beat.pausa;
  if (pausa && pausa.quem === uid && pausa.t > 0 && !beat.impacted) {
    return { passo: beat.passos![pausa.passo]!, evento: pausa.evento, t: pausa.t, fases: pausa.fases, pausa: true };
  }
  return undefined;
}
