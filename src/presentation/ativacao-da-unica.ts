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
import { PRESENTATION as P } from './config';
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

/** De quem a Mecânica única atinge, visto por quem ativou: o rival, um aliado ou ela mesma (pelo alvo do aviso). */
export function ladoDaUnica(e: BattleEvent, b: Battle): 'rival' | 'aliado' | 'si' {
  if (!e.target || e.target === e.source) return 'si';
  const de = b.fighters.find((f) => f.uid === e.source), para = b.fighters.find((f) => f.uid === e.target);
  return de && para && de.side === para.side ? 'aliado' : 'rival';
}
type BeatDaUnica = Pick<Beat, 'events' | 'after' | 'passos' | 'traco'>;
const COM_EFEITO = new Set<BattleEvent['kind']>(['damage', 'heal', 'shield', 'status', 'tempo', 'cleanse', 'dispel', 'revive', 'interrupt', 'summon', 'block', 'resist']);
/**
 * Onde a Mecânica única cai de verdade. Quem tem a entrega desenhada à mão (ENTREGA_DA_UNICA) segue o alvo do aviso
 * (o laço da Mulher-Maravilha vai no rival, mesmo o reforço ficando nela). Os outros seguem o que ela causa: o
 * aviso da Expansão de Domínio do Gojo aponta para o próprio Gojo, mas o efeito cai nos rivais.
 */
export interface DestinoDaUnica { lado: 'rival' | 'aliado' | 'si'; alvos: string[]; area: boolean }
export function destinoDaUnica(e: BattleEvent, b: Battle, beat?: BeatDaUnica): DestinoDaUnica {
  const dono = b.fighters.find((f) => f.uid === e.source);
  const rivaisDePe = () => b.fighters.filter((f) => f.side !== dono?.side && f.hp > 0).map((f) => f.uid);
  const desenhada = dono ? ENTREGA_DA_UNICA[dono.characterId] : undefined;
  const peloAviso = (): DestinoDaUnica => {
    const lado = ladoDaUnica(e, b), ent = dono ? entregaDaUnica(dono.characterId, lado) : undefined;
    if (ent?.area) return { lado: 'rival', alvos: rivaisDePe(), area: true };
    return { lado: ent?.modo === 'si' ? 'si' : lado, alvos: [ent?.modo === 'si' ? e.source : e.target ?? e.source], area: false };
  };
  if (!beat) return peloAviso();
  const efeito = peloEfeito(e, b, beat);
  // desenhada à mão: segue o aviso, a não ser que o aviso aponte quem ativou e o efeito caia em outro
  if (desenhada && !(ladoDaUnica(e, b) === 'si' && desenhada.modo !== 'si' && efeito && efeito.lado !== 'si')) return peloAviso();
  if (efeito && desenhada?.area && efeito.lado === 'rival') return { lado: 'rival', alvos: rivaisDePe(), area: true };
  return efeito ?? peloAviso();
}
function peloEfeito(e: BattleEvent, b: Battle, beat: BeatDaUnica): DestinoDaUnica | undefined {
  const dono = b.fighters.find((f) => f.uid === e.source);
  // o que ela causou: o passo de resultado logo depois dela, ou (sozinha) tudo o que quem ativou fez no beat
  const k = beat.passos?.findIndex((p) => p.eventos.includes(e.id)) ?? -1;
  const resultado = k >= 0 && beat.passos![k + 1]?.resultado ? beat.passos![k + 1]!.eventos : beat.traco ? beat.events.map((x) => x.id) : [];
  const alvos = [...new Set(beat.events.filter((x) => resultado.includes(x.id) && x.source === e.source && COM_EFEITO.has(x.kind) && x.target).map((x) => x.target!))];
  const ladoDe = (uid: string) => (uid === e.source ? 'si' : b.fighters.find((f) => f.uid === uid)?.side === dono?.side ? 'aliado' : 'rival');
  const rivais = alvos.filter((a) => ladoDe(a) === 'rival'), aliados = alvos.filter((a) => ladoDe(a) === 'aliado');
  if (rivais.length) return { lado: 'rival', alvos: rivais, area: rivais.length > 1 };
  if (aliados.length) return { lado: 'aliado', alvos: aliados, area: false };
  if (alvos.length) return { lado: 'si', alvos: [e.source], area: false };
  return undefined;
}
/** O jeito da entrega desta ativação (de onde ela cai de verdade). */
export function entregaDoEvento(e: BattleEvent, b: Battle, beat?: BeatDaUnica) {
  const dono = b.fighters.find((f) => f.uid === e.source), destino = destinoDaUnica(e, b, beat);
  const ent = entregaDaUnica(dono?.characterId ?? '', destino.lado);
  return { ...ent, area: ent.area || destino.area, destino };
}
/** Quanto a Mecânica única leva para chegar no alvo depois de soltar (o projétil voando, o feixe crescendo). */
export function vooDaUnica(e: BattleEvent, b: Battle, beat?: BeatDaUnica) {
  const ent = entregaDoEvento(e, b, beat);
  return ent.modo !== 'si' && (ent.area || ent.destino.alvos.some((a) => a !== e.source)) ? VOO_DA_UNICA[ent.modo] : 0;
}
export function fasesDoEvento(e: BattleEvent, b: Battle, beat?: BeatDaUnica): FasesDaUnica {
  const f = b.fighters.find((x) => x.uid === e.source);
  return fasesDaUnica(f?.characterId ?? '', vooDaUnica(e, b, beat));
}

/**
 * Uma pausa no golpe: alguém ativa a Mecânica única antes de o golpe cair. `t` corre só enquanto o golpe está
 * parado; `dura` é a ativação inteira e um respiro.
 *  - a do próprio atacante que vale para este golpe (o Golpe mortal do Sekiro): ele ativa antes de partir (em 0);
 *  - a de quem é atingido (a Armadura de Pégaso) ou a que dispara antes do golpe cair: o golpe para no meio do
 *    caminho, ela ativa, e o golpe continua.
 */
export interface PausaDaUnica { quem: string; evento: BattleEvent; passo: number; em: number; dura: number; t: number; fases: FasesDaUnica; propria: boolean }
/** Depois de o efeito aparecer, quanto ele fica à vista antes de o golpe continuar. */
const RESPIRO_DA_PAUSA = 0.45;
export function pausasDoGolpe(beat: Pick<Beat, 'event' | 'events' | 'after' | 'passos' | 'traco'>, impacto: number, antecipa: number): PausaDaUnica[] {
  if (beat.event.kind !== 'basic' && beat.event.kind !== 'skill') return [];
  const ladoDe = (uid?: string) => beat.after.fighters.find((f) => f.uid === uid)?.side;
  const atacante = beat.event.source;
  // quem o golpe acerta (dano, bloqueio ou o golpe que errou nele)
  const atingidos = new Set(beat.events.filter((e) => (e.kind === 'damage' || e.kind === 'block' || e.kind === 'miss') && (e.kind === 'block' ? (e.attacker ?? e.source) : e.source) === atacante && e.target).map((e) => e.target!));
  const caiu = new Set(beat.events.filter((e) => e.kind === 'ko').map((e) => e.target));
  const primeiroDano = beat.events.findIndex((e) => e.kind === 'damage' && e.source === atacante);
  const meio = Math.max(0, Math.min(impacto * 0.6, impacto - antecipa - 0.05));
  const pausas: PausaDaUnica[] = [];
  (beat.passos ?? []).forEach((p: Passo, k) => {
    if (p.classe !== 'unica') return;
    const evento = beat.events.find((e) => e.kind === 'unica' && p.eventos.includes(e.id));
    if (!evento) return;
    const antes = primeiroDano < 0 || beat.events.indexOf(evento) < primeiroDano;
    const propria = p.quem === atacante;
    if (propria ? !antes : !(antes || (atingidos.has(p.quem) && !caiu.has(p.quem) && ladoDe(p.quem) !== ladoDe(atacante)))) return;
    const fases = fasesDoEvento(evento, beat.after, beat);
    pausas.push({ quem: p.quem, evento, passo: k, em: propria ? 0 : meio, dura: fases.impactoEm + RESPIRO_DA_PAUSA, t: 0, fases, propria });
  });
  return pausas.sort((a, b) => a.em - b.em);
}
/** A pausa que segura o golpe agora (o golpe parado, esperando a ativação). */
export function golpeParado(beat: Beat | null | undefined): PausaDaUnica | undefined {
  if (!beat?.pausas || beat.impacted) return undefined;
  const p = beat.pausas.find((x) => x.t < x.dura);
  return p && beat.elapsed >= p.em - 1e-8 ? p : undefined;
}

/** A ativação de um lutador neste quadro: em que ponto ela está (t) e as fases dela. */
export interface AtivacaoNaTela { passo: Passo; evento?: BattleEvent; t: number; fases: FasesDaUnica; pausa: boolean }
export function ativacaoNaTela(beat: Beat | null | undefined, uid: string): AtivacaoNaTela | undefined {
  if (!beat) return undefined;
  if (beat.traco && beat.passos?.[0]?.classe === 'unica' && beat.event.source === uid) {
    return { passo: beat.passos[0], evento: beat.event, t: beat.elapsed, fases: fasesDoEvento(beat.event, beat.after, beat), pausa: false };
  }
  // na pausa do golpe: a de quem foi atingido fica à vista até o golpe cair; a do atacante, só até ele partir
  const pausa = !beat.impacted ? beat.pausas?.find((p) => p.quem === uid && p.t > 0 && (p.t < p.dura || !p.propria)) : undefined;
  if (pausa) return { passo: beat.passos![pausa.passo]!, evento: pausa.evento, t: pausa.t, fases: pausa.fases, pausa: true };
  // no meio da cadeia de um golpe: o passo dela tem as mesmas fases, e o resultado dela vem no passo seguinte
  if (beat.impacted && beat.passos && beat.etapa) {
    const k = beat.etapa - 1, atual = beat.passos[k], antes = beat.passos[k - 1];
    const dela = atual?.classe === 'unica' && !atual.antecipada ? atual : atual?.resultado && antes?.classe === 'unica' && !antes.antecipada ? antes : undefined;
    if (dela && dela.quem === uid) {
      const evento = beat.events.find((e) => e.kind === 'unica' && dela.eventos.includes(e.id));
      if (evento) return { passo: dela, evento, t: beat.elapsed - (beat.base ?? beat.duration) * P.impactAt - dela.em, fases: fasesDoEvento(evento, beat.after, beat), pausa: false };
    }
  }
  return undefined;
}
