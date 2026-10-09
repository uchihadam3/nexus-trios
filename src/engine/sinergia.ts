/*
 * Sinergia de verdade entre os três de um trio, lida dos kits.
 *
 * A nota antiga (`synergy` em campaign.ts) olhava 7 etiquetas que quase
 * ninguém do elenco de 250 tem, e não mudava nada na luta. Aqui a sinergia
 * vem do que as habilidades fazem: um aliado que dá Carga ajuda quem tem um
 * golpe grande para carregar; quem deixa o rival Exposto/Marcado/Paralisado/
 * Eletrizado/Queimando abre caminho para quem só ataca o rival vulnerável;
 * cura e escudo seguram quem tem pouca Vida; reforço vale mais em quem bate
 * forte; quem põe Status no rival faz disparar quem reage a Status (Light,
 * Zelda…); e assim por diante.
 *
 * Cada combinação é uma "ligação". Quanto cada ligação vale (em força de
 * luta) foi medido em lutas simuladas, junto com a força de cada personagem
 * (scripts/medir-forca.ts → src/data/forca-dos-rivais.ts). Uma ligação que
 * não ajuda de verdade na luta fica com peso zero.
 */
import { characters, byId } from '../data/characters';
import { DEIXAM_VULNERAVEL } from '../data/statuses';
import type { Character, Effect, StatusId, Target } from './types';

export const LIGACOES = ['carga-golpe', 'abre-vulneravel', 'abre-ferido', 'cuida-fragil', 'reforca-forte', 'adianta-golpe', 'protege-vinganca', 'controla-dano', 'status-gatilho', 'provoca-fragil', 'levanta-forte', 'limpa-forte'] as const;
export type Ligacao = (typeof LIGACOES)[number];

const PARA_ALIADOS: Target[] = ['allAllies', 'allyWeak'];
const PARA_RIVAIS: Target[] = ['enemyWeak', 'enemyStrong', 'enemyCast', 'investigated', 'leastInvestigated', 'allEnemies', 'randomEnemy'];
/* deixa o rival vulnerável: a mesma lista da condição das habilidades (Veneno, Sangrando… também) */
const ABRE: StatusId[] = DEIXAM_VULNERAVEL;
const PRENDE: StatusId[] = ['paralyzed', 'frozen', 'sleep', 'rooted', 'slow', 'confused', 'silenced', 'weakened', 'blind'];
const REFORCO: StatusId[] = ['strengthened', 'haste', 'protected', 'regen'];

export interface Papel {
  daCarga: boolean; adianta: boolean; reforca: boolean; cuida: boolean;
  abre: boolean; prende: boolean; golpeGrande: boolean; precisaVulneravel: boolean;
  precisaFerido: boolean; fragil: boolean; forte: boolean; vinganca: boolean;
  aplicaStatus: boolean; reageAStatus: boolean;
  /** mecânicas novas: Provocar (puxa os golpes), Reviver, Purificar */
  provoca: boolean; levanta: boolean; purifica: boolean;
}

function efeitos(c: Character): { e: Effect; alvo: Target }[] {
  const lista: { e: Effect; alvo: Target }[] = [];
  for (const s of c.skills) for (const e of s.effects) lista.push({ e, alvo: e.target ?? s.target });
  for (const e of c.trait.effects) lista.push({ e, alvo: e.target ?? c.trait.target });
  for (const e of c.basic.effects) lista.push({ e, alvo: e.target ?? c.basic.target });
  return lista;
}

const mediana = (xs: number[]) => { const o = [...xs].sort((a, b) => a - b); return o[Math.floor(o.length / 2)] ?? 0; };
const danoDe = (c: Character) => efeitos(c).reduce((n, { e }) => n + (e.kind === 'damage' ? e.value : 0), 0);
const VIDA_MEDIANA = mediana(characters.map((c) => c.hp));
const DANO_ALTO = (() => { const o = characters.map(danoDe).sort((a, b) => a - b); return o[Math.floor(o.length * 0.65)] ?? 0; })();

const papeis = new Map<string, Papel>();
export function papelDe(id: string): Papel {
  const pronto = papeis.get(id);
  if (pronto) return pronto;
  const c = byId[id]!, ef = efeitos(c);
  const aliado = (alvo: Target) => PARA_ALIADOS.includes(alvo);
  const rival = (alvo: Target) => PARA_RIVAIS.includes(alvo);
  const p: Papel = {
    daCarga: ef.some(({ e, alvo }) => e.kind === 'charge' && aliado(alvo)),
    adianta: ef.some(({ e, alvo }) => e.kind === 'shift' && (aliado(alvo) ? e.value > 0 : rival(alvo) && e.value < 0)),
    reforca: ef.some(({ e, alvo }) => e.kind === 'status' && REFORCO.includes(e.status) && aliado(alvo)),
    cuida: ef.some(({ e, alvo }) => (e.kind === 'heal' || e.kind === 'shield') && aliado(alvo)),
    abre: ef.some(({ e, alvo }) => e.kind === 'status' && ABRE.includes(e.status) && rival(alvo)),
    prende: ef.some(({ e, alvo }) => (e.kind === 'status' && PRENDE.includes(e.status) || e.kind === 'interrupt') && rival(alvo)),
    golpeGrande: c.skills.some((s) => s.preparation >= 2 || s.effects.some((e) => e.kind === 'damage' && e.value >= 400)),
    precisaVulneravel: c.skills.some((s) => s.condition === 'vulnerable'),
    precisaFerido: c.skills.some((s) => s.condition === 'injured'),
    fragil: c.hp < VIDA_MEDIANA * 0.94,
    forte: danoDe(c) >= DANO_ALTO,
    vinganca: ['received', 'allyHurt', 'losing', 'survived'].includes(c.trait.on) || c.skills.some((s) => s.condition === 'threatened'),
    // quando um aliado põe Status no rival, o traço dispara e as habilidades carregam (battle.ts, 'status'/'negativeStatus')
    aplicaStatus: ef.some(({ e, alvo }) => e.kind === 'status' && rival(alvo)),
    reageAStatus: ['status', 'negativeStatus'].includes(c.trait.on) || c.skills.some((s) => s.charge.some((r) => r.on === 'status' || r.on === 'negativeStatus')),
    provoca: ef.some(({ e }) => e.kind === 'status' && e.status === 'provoked'),
    levanta: ef.some(({ e }) => e.kind === 'revive'),
    purifica: ef.some(({ e, alvo }) => e.kind === 'cleanse' && aliado(alvo)),
  };
  papeis.set(id, p);
  return p;
}

/** Quantas vezes cada ligação aparece entre os três (pares ordenados, um ajudando o outro). */
export function ligacoesDoTrio(trio: readonly string[]): Record<Ligacao, number> {
  const n = Object.fromEntries(LIGACOES.map((l) => [l, 0])) as Record<Ligacao, number>;
  for (const a of trio) for (const b of trio) {
    if (a === b) continue;
    const pa = papelDe(a), pb = papelDe(b);
    if (pa.daCarga && pb.golpeGrande) n['carga-golpe']++;
    if (pa.abre && pb.precisaVulneravel) n['abre-vulneravel']++;
    if (pa.forte && pb.precisaFerido) n['abre-ferido']++;
    if (pa.cuida && pb.fragil) n['cuida-fragil']++;
    if (pa.reforca && pb.forte) n['reforca-forte']++;
    if (pa.adianta && pb.golpeGrande) n['adianta-golpe']++;
    if (pa.cuida && pb.vinganca) n['protege-vinganca']++;
    if (pa.prende && pb.forte) n['controla-dano']++;
    if (pa.aplicaStatus && pb.reageAStatus) n['status-gatilho']++;
    if (pa.provoca && pb.fragil) n['provoca-fragil']++;
    if (pa.levanta && pb.forte) n['levanta-forte']++;
    if (pa.purifica && pb.forte) n['limpa-forte']++;
  }
  // a mesma ligação repetida ajuda cada vez menos
  for (const l of LIGACOES) n[l] = Math.min(2, n[l]);
  return n;
}
