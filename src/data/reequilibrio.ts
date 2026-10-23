import type { Character, Effect } from '../engine/types';
import { statuses } from './statuses';

/*
 * Buffs e debuffs que fazem diferença, sem mudar a força de ninguém (pedido do dono: "os buffs e debuffs de dano contínuo…
 * parecem tirar pouca vida e curar pouca vida… aumentar eles pra eles causar mais, só que aí talvez tirar do dano deles…
 * deixar eles na mesma força").
 *
 * Medido em 120 lutas de cada personagem: o Sangramento rendia 50 de dano por luta (5% do dano de quem usa; o Finn, 6), e
 * havia Escudo de 8, cura de 4 e Fortalecido de 2,5%. Cada personagem com efeito fraco ganhou:
 *  - PISOS: nenhum Escudo, cura ou Fortalecido/Acelerado/Enfraquecido abaixo de um mínimo que se nota;
 *  - `mult`: o efeito contínuo (Sangrando, Queimando, Envenenado, Regeneração, Marca explosiva, Espinhos, Invocação)
 *    multiplicado até render o mesmo que os bons do mesmo tipo;
 * e perdeu o mesmo tanto em outro lugar: `dano` (o dano direto do ataque básico, das habilidades e do traço) quando o que
 * ganhou ataca, `vida` (a Vida máxima) quando o que ganhou protege ou cura. O quanto tirar foi medido em lutas com as
 * mesmas sementes, até o trio dele vencer o mesmo tanto de antes (scripts/reequilibrar.ts).
 */
export const PISOS = {
  shield: 30, heal: 25, strengthened: 0.06, haste: 0.06, weakened: 0.06, exposed: 0.08, protected: 0.12, marked: 0.1, slow: 0.12,
  rooted: 0.15, electric: 0.08, cursed: 0.15, blind: 0.2, evasion: 0.15, reflect: 0.15, vampirism: 0.15, confused: 0.15,
} as const;
/* Duração mínima: o Sangrando só tira Vida quando o alvo age (a cada ~3,6 s), então dura pelo menos 8 s; os outros, 3 s
 * (os de travar — Paralisado, Congelado, Dormindo, Provocado — e a Marca explosiva têm a duração curta de propósito). */
const DURACAO_MINIMA: Partial<Record<string, number>> = { bleed: 8 };
const CURTOS_DE_PROPOSITO = new Set(['paralyzed', 'frozen', 'sleep', 'provoked', 'bomb', 'barrier']);

export interface Reequilibrio {
  /** multiplica a intensidade do Status (ou o valor do Escudo e da cura), por tipo */
  mult?: Partial<Record<string, number>>;
  /** multiplica o dano direto (nos rivais) do ataque básico, das habilidades e do traço */
  dano?: number;
  /** multiplica a Vida máxima */
  vida?: number;
  /** quanto dos pisos vale para ele (1 = inteiros): menos quando o piso sozinho já o deixava forte demais (cura no trio todo) */
  piso?: number;
}

export const REEQUILIBRIO: Record<string, Reequilibrio> = {
  agent47: { mult: { poison: 6 }, dano: 0.971 }, // vence 53.4% → 53.4%
  ainz: { mult: { summon: 1.56 } }, // vence 48.6% → 49.0%
  alucardcv: { vida: 0.843 }, // vence 46.8% → 46.5%
  apollo: { mult: { regen: 2.65 }, vida: 0.938 }, // vence 49.0% → 49.3%
  aquaman: { dano: 0.967 }, // vence 48.2% → 47.5%
  arlequina: { mult: { bomb: 1.04 } }, // vence 52.1% → 52.2%
  athena: { vida: 0.794 }, // vence 48.5% → 48.1%
  bakugo: { mult: { burning: 3.89, bomb: 1.67 }, dano: 0.951 }, // vence 51.8% → 51.5%
  bowser: { dano: 0.9 }, // vence 45.6% → 45.0%
  broly: { dano: 0.947 }, // vence 52.2% → 52.9%
  capitaoplaneta: { piso: 0.5 }, // vence 53.1% → 53.1%
  carnage: { mult: { regen: 2 }, vida: 0.963 }, // vence 51.9% → 51.5%
  catwoman: { mult: { bleed: 6 }, dano: 0.976 }, // vence 48.9% → 49.2%
  charizard: { dano: 0.9 }, // vence 46.2% → 46.4%
  coiote: { mult: { bomb: 1.45 } }, // vence 46.5% → 47.0%
  coringa: { mult: { poison: 2.12 }, dano: 0.972 }, // vence 45.6% → 45.8%
  cosmowanda: { mult: { regen: 2.37 }, vida: 0.962 }, // vence 45.0% → 45.1%
  crash: { mult: { bomb: 1.74 }, dano: 0.973 }, // vence 48.2% → 48.1%
  darkseid: { dano: 0.944 }, // vence 52.5% → 52.5%
  denji: { mult: { bleed: 5.26 }, dano: 0.9 }, // vence 53.7% → 52.9%
  dio: { vida: 0.945 }, // vence 47.6% → 47.2%
  donatello: { mult: { bomb: 1.43 } }, // vence 54.9% → 55.6%
  doomslayer: { vida: 0.9 }, // vence 46.9% → 46.1%
  dracula: { mult: { burning: 1.46 } }, // vence 49.5% → 50.0%
  edward: { mult: { thorns: 2.63 }, dano: 0.861 }, // vence 51.3% → 51.0%
  fenrir: { mult: { bleed: 6 }, dano: 0.969 }, // vence 60.5% → 60.8%
  finn: { mult: { bleed: 6 }, dano: 0.9 }, // vence 47.6% → 47.1%
  freddy: { mult: { bleed: 2.56 } }, // vence 47.1% → 47.3%
  frozone: { mult: { thorns: 1.47 }, dano: 0.968 }, // vence 50.8% → 50.7%
  gaara: { mult: { thorns: 1.19 }, dano: 0.735 }, // vence 47.8% → 47.7%
  gambit: { mult: { bomb: 2.58 }, dano: 0.971 }, // vence 48.2% → 48.7%
  gamora: { mult: { bleed: 1.67 } }, // vence 47.8% → 48.4%
  ghostrider: { mult: { regen: 1.32 }, vida: 0.976 }, // vence 48.4% → 48.2%
  gohan: { dano: 0.929 }, // vence 53.5% → 53.9%
  gon: { dano: 0.941 }, // vence 51.0% → 50.7%
  greengoblin: { mult: { poison: 1.84 } }, // vence 53.3% → 53.9%
  groot: { mult: { thorns: 1.56 }, dano: 0.7, piso: 0.5 }, // vence 51.9% → 51.2%
  guts: { mult: { bleed: 2.38 }, dano: 0.918 }, // vence 55.3% → 55.8%
  hadescz: { dano: 0.957 }, // vence 55.1% → 55.1%
  hawkeye: { mult: { bomb: 2.76 }, dano: 0.9 }, // vence 41.4% → 41.6%
  hel: { mult: { summon: 1.32 } }, // vence 48.3% → 48.9%
  hellboy: { vida: 0.965 }, // vence 48.9% → 48.9%
  hisoka: { dano: 0.925 }, // vence 48.6% → 48.3%
  hyoga: { dano: 0.959 }, // vence 48.4% → 48.4%
  ikki: { mult: { burning: 2.41 }, dano: 0.959 }, // vence 58.8% → 58.7%
  inosuke: { mult: { bleed: 6 }, dano: 0.968 }, // vence 50.8% → 51.1%
  invencivel: { vida: 0.959 }, // vence 47.6% → 47.2%
  iroh: { vida: 0.921 }, // vence 48.0% → 47.9%
  jackskellington: { mult: { burning: 3.89 }, dano: 0.97 }, // vence 50.3% → 51.1%
  jeangrey: { vida: 0.965 }, // vence 49.3% → 49.8%
  jill: { vida: 0.9 }, // vence 50.6% → 50.5%
  jotaro: { mult: { summon: 1.56 }, dano: 0.978 }, // vence 47.5% → 47.9%
  kaiba: { mult: { burning: 2.06 }, dano: 0.962 }, // vence 59.9% → 59.9%
  kakashi: { dano: 0.988 }, // vence 48.2% → 47.9%
  kaneki: { vida: 0.933 }, // vence 50.1% → 49.9%
  katara: { mult: { regen: 1.96 }, vida: 0.955 }, // vence 50.0% → 50.0%
  kazuya: { mult: { burning: 4.38 }, dano: 0.9 }, // vence 50.2% → 50.1%
  kenpachi: { mult: { bleed: 2.04 }, dano: 0.935 }, // vence 51.1% → 50.7%
  korra: { mult: { burning: 1.01 }, dano: 0.973 }, // vence 55.7% → 56.4%
  kratos: { mult: { bleed: 6, burning: 1.21 }, dano: 0.9 }, // vence 49.9% → 50.5%
  kurama: { mult: { poison: 2.26 }, dano: 0.968 }, // vence 47.3% → 47.5%
  kurapika: { dano: 0.9 }, // vence 48.2% → 47.5%
  leatherface: { mult: { bleed: 3.33 }, dano: 0.978 }, // vence 57.7% → 57.6%
  leorio: { mult: { regen: 1.64 } }, // vence 50.2% → 50.9%
  luigi: { mult: { burning: 3.89 }, dano: 0.964 }, // vence 54.9% → 55.0%
  madara: { dano: 0.758 }, // vence 51.9% → 52.4%
  malenia: { vida: 0.934 }, // vence 51.2% → 51.0%
  michaelmyers: { vida: 0.978 }, // vence 50.6% → 50.4%
  moonknight: { vida: 0.983 }, // vence 47.2% → 47.6%
  mulherelastica: { vida: 0.841 }, // vence 49.7% → 49.1%
  nemesis: { mult: { bomb: 2.16 }, dano: 0.971 }, // vence 48.6% → 48.2%
  nezuko: { vida: 0.947 }, // vence 48.0% → 48.1%
  pain: { mult: { summon: 1.59 } }, // vence 59.8% → 60.5%
  pinhead: { dano: 0.843 }, // vence 45.9% → 45.4%
  poseidon: { dano: 0.944 }, // vence 45.2% → 45.2%
  power: { mult: { bleed: 1.49 } }, // vence 49.0% → 49.1%
  pyramidhead: { mult: { bleed: 2.5 }, dano: 0.9 }, // vence 45.9% → 46.0%
  rambo: { mult: { bomb: 1.95 }, dano: 0.953 }, // vence 42.4% → 42.1%
  raphael: { dano: 0.974 }, // vence 50.9% → 50.6%
  rem: { mult: { regen: 1.96 } }, // vence 47.9% → 48.7%
  rick: { vida: 0.978 }, // vence 52.7% → 53.1%
  rocket: { mult: { bomb: 1.48 }, dano: 0.983 }, // vence 44.2% → 44.2%
  rogue: { vida: 0.957 }, // vence 58.0% → 58.5%
  roy: { vida: 0.9 }, // vence 52.9% → 52.5%
  ryu: { mult: { burning: 3.04 }, dano: 0.99 }, // vence 49.8% → 50.0%
  scarecrow: { mult: { poison: 2.92 }, dano: 0.982 }, // vence 49.1% → 49.4%
  scooby: { vida: 0.952 }, // vence 42.2% → 42.2%
  seiya: { dano: 0.919 }, // vence 58.5% → 58.1%
  senku: { mult: { bomb: 2 }, dano: 0.961 }, // vence 46.6% → 46.1%
  shiryu: { vida: 0.7 }, // vence 47.9% → 48.6%
  shun: { dano: 0.782 }, // vence 46.5% → 46.2%
  sonic: { mult: { thorns: 1.92 }, dano: 0.983 }, // vence 47.5% → 47.8%
  sora: { mult: { regen: 1.84 }, vida: 0.974 }, // vence 51.9% → 51.7%
  spawn: { mult: { bleed: 6 }, dano: 0.927 }, // vence 47.9% → 47.7%
  spiderwoman: { mult: { poison: 4.12 }, dano: 0.969 }, // vence 48.7% → 48.2%
  srincrivel: { vida: 0.915 }, // vence 49.6% → 49.9%
  starlord: { dano: 0.969 }, // vence 46.2% → 46.3%
  steven: { vida: 0.725 }, // vence 44.8% → 44.4%
  stitch: { vida: 0.954 }, // vence 46.7% → 46.5%
  storm: { dano: 0.94 }, // vence 46.8% → 47.0%
  sukuna: { mult: { bleed: 6 }, dano: 0.976 }, // vence 44.6% → 44.9%
  superman: { mult: { burning: 6 } }, // vence 47.5% → 47.9%
  tanjiro: { mult: { burning: 2.8 }, dano: 0.966 }, // vence 49.0% → 48.8%
  tom: { mult: { bomb: 4.44 }, dano: 0.966 }, // vence 49.3% → 48.8%
  toph: { mult: { thorns: 1.47 }, dano: 0.949 }, // vence 50.1% → 49.9%
  trunks: { mult: { burning: 3.18 }, dano: 0.866 }, // vence 53.8% → 54.0%
  wesker: { mult: { bleed: 3.33 }, dano: 0.9 }, // vence 55.6% → 56.2%
  wolverine: { vida: 0.8 }, // vence 48.2% → 48.2%
  zelda: { dano: 0.963 }, // vence 52.0% → 52.1%
  zoro: { mult: { bleed: 1.02 } }, // vence 47.3% → 47.5%
};

const arredonda = (v: number, era: number) => (Math.abs(era) < 1 ? Math.round(v * 1000) / 1000 : Math.round(v));
const NOS_RIVAIS = new Set(['enemyWeak', 'enemyStrong', 'enemyCast', 'investigated', 'leastInvestigated', 'allEnemies', 'randomEnemy']);

/*
 * O piso conta quantas vezes o efeito sai: o que sai a cada 4 s ou mais tem o piso inteiro; o que sai bem mais vezes (o traço
 * de 1 s do Wolverine, que cura 4 a cada golpe) tem um piso menor, até 40% dele — ali o número pequeno já soma bastante.
 */
const fracaoDoPiso = (cadencia: number) => Math.min(1, Math.max(0.4, cadencia / 4));
function efeito(e: Effect, alvo: string, a: Reequilibrio, cadencia: number): Effect {
  const f = fracaoDoPiso(cadencia) * (a.piso ?? 1);
  if (e.kind === 'shield' || e.kind === 'heal') {
    const v = Math.max(e.value, PISOS[e.kind] * f) * (a.mult?.[e.kind] ?? 1);
    return v === e.value ? e : { ...e, value: arredonda(v, e.value) };
  }
  if (e.kind === 'status') {
    const piso = (PISOS as Record<string, number>)[e.status];
    // a luta já corta no teto do Status (src/data/statuses.ts); a ficha mostra o mesmo número
    const v = Math.min(statuses[e.status].cap, (piso !== undefined ? Math.max(e.value, piso * f) : e.value) * (a.mult?.[e.status] ?? 1));
    // a duração mínima só onde o efeito não volta antes dela (o traço de 1,5 s do Professor Xavier, que dá Fortalecido ao
    // trio todo, já fica valendo direto: durar mais só empilharia)
    const minimo = DURACAO_MINIMA[e.status] ?? (CURTOS_DE_PROPOSITO.has(e.status) ? 0 : 3);
    const d = (a.piso ?? 1) > 0 && cadencia >= minimo ? Math.max(e.duration, minimo) : e.duration;
    return v === e.value && d === e.duration ? e : { ...e, value: arredonda(v, e.value), duration: d };
  }
  if (e.kind === 'damage' && a.dano !== undefined && NOS_RIVAIS.has(e.target ?? alvo)) return { ...e, value: Math.round(e.value * a.dano) };
  return e;
}

/** Aplica os pisos e o ajuste do personagem (o de REEQUILIBRIO, ou outro para medir). */
export function reequilibra(c: Character, a: Reequilibrio = REEQUILIBRIO[c.id] ?? {}): Character {
  const fx = (effects: Effect[], alvo: string, cadencia: number) => effects.map((e) => efeito(e, alvo, a, cadencia));
  return {
    ...c,
    hp: a.vida !== undefined ? Math.round(c.hp * a.vida) : c.hp,
    basic: { ...c.basic, effects: fx(c.basic.effects, c.basic.target, c.interval) },
    trait: { ...c.trait, effects: fx(c.trait.effects, c.trait.target, c.trait.cooldown) },
    skills: c.skills.map((s) => ({ ...s, effects: fx(s.effects, s.target, Math.max(s.cooldown, 4)) })) as Character['skills'],
  };
}
