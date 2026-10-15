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
import { ENTREGA_DA_UNICA, VOO_DA_UNICA, efeitoDaUnica, entregaDaUnica, type ModoDaEntrega } from './unicas-efeitos';
import { PICO_DA_FOLHA } from './pico-das-folhas';
import { ABRE_O_LEQUE, RAJADA_DA_UNICA } from './rajada-da-unica';
import { ESFERA_QUE_CRESCE } from './esfera-que-cresce';

/** O Preparo de cada um, na mesma escala do Preparo das habilidades (0 = instantâneo). */
export const PREPARO_PROPRIO: Record<string, number> = {
  // reflexos: o nome e o efeito saem juntos
  valak: 0, neo: 0, sans: 0, sekiro: 0, minato: 0, crash: 0, sonic: 0, kenshin: 0, hiei: 0, hayabusa: 0, pernalonga: 0,
  // as que deixaram de ser 'sempre' e ativam na hora (pedido do jogador: "rápido… nada demorado")
  kurama: 0.1, natsu: 0.1, jinwoo: 0.1, yuji: 0.1, captainmarvel: 0.1, doctordoom: 0.1, scarletwitch: 0.1, chunli: 0.1,
  doomslayer: 0.1, snake: 0.1, bart: 0.1, splinter: 0.1, pateta: 0.1, zuko: 0.1, silversurfer: 0.2, samara: 0.2,
  // respostas rápidas ao golpe e golpes de surpresa
  seiya: 0.2, shiryu: 0.1, garou: 0.1, saitama: 0.1, ghostface: 0.1, jason: 0.1, michaelmyers: 0.1, batman: 0.1,
  levi: 0.1, daredevil: 0.1, morty: 0.1, harrypotter: 0.1, xenomorph: 0.1, catwoman: 0.1, blackwidow: 0.1,
  lelouch: 0.2, aizen: 0.2, kakashi: 0.2, coringa: 0.2, yor: 0.2, mikasa: 0.2,
  // o que precisa juntar energia de verdade
  // a Genki Dama cresce em quatro estágios antes de ser lançada (src/presentation/esfera-que-cresce.ts)
  // a Autodestruição do Cell: a luta para, ele incha de energia, o nome aparece e só então explode (pedido do jogador)
  cell: 0.9,
  goku: 1.1, megatron: 0.5, madara: 0.5, dovahkiin: 0.5, galactus: 0.2, light: 0.5, kaiba: 0.5, darkseid: 0.4,
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
  /** a folha do efeito começa no alvo (a chegada desenhada nela: os pássaros do Katsu voando) */
  efeitoEm: number;
  /** o efeito bate de verdade no alvo (o estouro da folha): o número, o tremor e o resultado saem aqui */
  impactoEm: number;
  /** quanto a entrega viaja */
  voo: number;
}
/** A folha do efeito no alvo dura 1,5 s a 1× (BattleEffects: efeitoNoAlvo). */
const FOLHA_NO_ALVO = 1.5;
/**
 * Quanto o estouro da folha vem depois do começo dela (src/presentation/pico-das-folhas.ts, medido em cada folha):
 * o número espera o estouro (pedido do jogador: "só aparece o dano… cadê o impacto?"). O reflexo (preparo 0: a
 * esquiva do Hiei, a armadura do Seiya) espera pouco, para a resposta continuar rápida.
 */
export function esperaDoEstouro(familia: string | undefined, preparo: number): number {
  const pico = (familia && PICO_DA_FOLHA[familia]) || 0;
  return Math.min(preparo <= 0 ? 0.25 : 0.75, pico * FOLHA_NO_ALVO);
}
export function fasesDaUnica(personagem: string, voo: number, familia?: string): FasesDaUnica {
  const preparo = preparoProprio(personagem), espera = esperaDoEstouro(familia, preparo);
  if (preparo <= 0) { const efeitoEm = voo > 0 ? voo : 0.12; return { preparo, nomeEm: 0, soltaEm: 0, vooEm: 0, efeitoEm, impactoEm: efeitoEm + espera, voo }; }
  const nomeEm = 0.25 + preparo * 0.6;
  const soltaEm = nomeEm + 0.15 + preparo;
  const vooEm = soltaEm + 0.12;
  const efeitoEm = voo > 0 ? vooEm + voo : soltaEm + 0.12;
  return { preparo, nomeEm, soltaEm, vooEm, efeitoEm, impactoEm: efeitoEm + espera, voo };
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
  const f = b.fighters.find((x) => x.uid === e.source), id = f?.characterId ?? '';
  // a rajada não usa a folha no alvo (cada projétil tem o seu impacto): nada de esperar o estouro dela
  const r = id ? RAJADA_DA_UNICA[id] : undefined, fases = fasesDaUnica(id, vooDaUnica(e, b, beat), id && !r ? efeitoDaUnica(id, e.label).familia : undefined);
  if (r) return fasesDaRajada(fases, r.voo, r.leque);
  // a esfera que cresce chega já no estouro da folha (a folha começa no meio, BattleEffects): o número sai na chegada
  return id && ESFERA_QUE_CRESCE[id] ? { ...fases, impactoEm: fases.efeitoEm } : fases;
}
/** O nome fica à vista este tanto antes de a rajada começar a aparecer. */
const LER_O_NOME = 0.3;
/**
 * A rajada sempre depois do nome (pedido do jogador: "ele carrega, aparece o nome, aparece as pétalas e usa…
 * hora nenhuma vai aparecer o nome depois"): os projéteis aparecem (o leque abre) só depois de o nome estar à vista,
 * e o primeiro chega no alvo depois de voar. Antes, o leque das pétalas abria antes do nome.
 */
export function fasesDaRajada(f: FasesDaUnica, voo: number, leque: boolean): FasesDaUnica {
  const abre = leque ? ABRE_O_LEQUE : 0.25;
  const efeitoEm = Math.max(f.efeitoEm, f.nomeEm + LER_O_NOME + abre + voo);
  const vooEm = Math.max(f.vooEm, efeitoEm - voo), soltaEm = Math.max(f.soltaEm, vooEm - 0.12);
  return { ...f, soltaEm, vooEm, efeitoEm, impactoEm: efeitoEm };
}

/**
 * Uma pausa no golpe: alguém ativa a Mecânica única antes de o golpe cair. `t` corre só enquanto o golpe está
 * parado; `dura` é a ativação inteira e um respiro.
 *  - a do próprio atacante que vale para este golpe (o Golpe mortal do Sekiro): ele ativa antes de partir (em 0);
 *  - a de quem é atingido (a Armadura de Pégaso) ou a que dispara antes do golpe cair: o golpe para no meio do
 *    caminho, ela ativa, e o golpe continua.
 */
export interface PausaDaUnica { quem: string; evento: BattleEvent; passo: number; em: number; dura: number; t: number; fases: FasesDaUnica; propria: boolean }
/** Depois de o efeito aparecer, quanto ele fica à vista antes de o golpe continuar (num reflexo, quase nada). */
const RESPIRO_DA_PAUSA = 0.45, RESPIRO_DO_REFLEXO = 0.2;
/**
 * Quem escapa do golpe (pedido do jogador sobre o Hiei: "mexe rapidinho… e o personagem erra… quase instantâneo"): na
 * pausa, em vez de concentrar, o personagem desvia para o lado num piscar.
 */
export const DESVIA_NA_UNICA = new Set(['hiei', 'sans', 'neo']);
/**
 * Avisos que só mostram o nome, sem a ativação completa: a semente do Kurama plantada (ela ativa de verdade quando
 * brota, 8 s depois) e a contagem dos dias da Samara.
 */
export function soONome(personagem: string, aviso: string): boolean {
  if (personagem === 'kurama') return aviso === 'Semente plantada';
  if (personagem === 'samara') return aviso.startsWith('Dia ');
  return false;
}
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
    pausas.push({ quem: p.quem, evento, passo: k, em: propria ? 0 : meio, dura: fases.impactoEm + (fases.preparo <= 0 ? RESPIRO_DO_REFLEXO : RESPIRO_DA_PAUSA), t: 0, fases, propria });
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
