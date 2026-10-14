/*
 * A entrega do apoio (pedido do jogador: "tem que verificar todo tipo de habilidade… que cura, que protege, que tem
 * escudo… se tá com essa mesma qualidade de animação"): a cura, o Escudo, o reforço e o reviver que uma habilidade
 * manda para um aliado saem de quem usou e voam até ele, como o golpe voa até o rival. Antes, o efeito só aparecia no
 * aliado, ligado por uma linha fina.
 *
 * Quem protege com o próprio corpo (o Wolverine na frente do aliado, o Superman segurando) vai até o aliado em pessoa
 * (src/presentation/acting.ts); a esfera é para o resto.
 * O desenho está em src/components/EntregaDeApoio.tsx; o som da saída, em src/App.tsx.
 */
import type { BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';
import { ROTULO_DA_MECANICA, duracaoBase, type Beat } from './director';

export type TipoDeApoio = 'cura' | 'escudo' | 'reforco' | 'reviver' | 'purificar';
export interface EntregaDeApoio {
  /** quem recebe */
  alvo: string;
  /** o que vai (decide o símbolo e a cor do miolo) */
  tipo: TipoDeApoio;
  /** quando sai de quem usou e quando chega, em segundos depois do impacto do beat */
  sai: number;
  chega: number;
}
/** Habilidades em que quem usa vai até o aliado em pessoa (o corpo é a entrega). */
export const GUARDA_DE_CORPO = new Set([
  'wolverine:1', 'superman:1', 'saitama:1', 'flash:1', 'mulherelastica:2', 'shrek:1', 'robocop:1',
  'tails:1', 'aphrodite:1', 'sonic:1',
]);
const DO_APOIO = new Set<BattleEvent['kind']>(['heal', 'shield', 'status', 'revive', 'cleanse']);
const tipoDe = (es: BattleEvent[]): TipoDeApoio =>
  es.some((e) => e.kind === 'revive') ? 'reviver' : es.some((e) => e.kind === 'heal') ? 'cura' : es.some((e) => e.kind === 'shield') ? 'escudo' : es.some((e) => e.kind === 'cleanse') ? 'purificar' : 'reforco';
/** O voo da esfera (s a 1×). */
const VOO = 0.5;

export function entregasDeApoio(beat: Beat | null | undefined): EntregaDeApoio[] {
  if (!beat?.passos || beat.event.kind !== 'skill' || beat.event.skill === undefined) return [];
  const dono = beat.event.source, f = beat.after.fighters.find((x) => x.uid === dono);
  if (!f || GUARDA_DE_CORPO.has(`${f.characterId}:${beat.event.skill}`)) return [];
  const ladoDe = (uid?: string) => beat.after.fighters.find((x) => x.uid === uid)?.side;
  // o nome da habilidade aparece no começo do beat: a esfera sai depois dele
  const comeco = -duracaoBase(beat) * P.impactAt + 0.3;
  const vistos = new Set<string>(), out: EntregaDeApoio[] = [];
  for (const passo of beat.passos) {
    const es = beat.events.filter((e) => passo.eventos.includes(e.id) && e.source === dono && DO_APOIO.has(e.kind) && !!e.target && e.target !== dono
      && ladoDe(e.target) === f.side && !(e.label in ROTULO_DA_MECANICA));
    const porAlvo = new Map<string, BattleEvent[]>();
    for (const e of es) (porAlvo.get(e.target!) ?? porAlvo.set(e.target!, []).get(e.target!)!).push(e);
    for (const [alvo, deles] of porAlvo) {
      if (vistos.has(alvo)) continue;
      vistos.add(alvo);
      const chega = passo.em, sai = Math.max(comeco, chega - VOO);
      if (chega - sai < 0.18) continue;
      out.push({ alvo, tipo: tipoDe(deles), sai, chega });
    }
  }
  return out;
}
