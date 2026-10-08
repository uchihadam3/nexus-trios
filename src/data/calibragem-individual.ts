/*
 * Calibragem individual: o último passo do balanceamento.
 *
 * A família (`calibragemDeDano` em `expanded-roster.ts`) resolve o arquétipo.
 * Ela não resolve quem está fora da própria família: o Agente 47 ganhava 78%
 * das lutas numa família que ganhava 40%, e o multiplicador da família, que
 * existe para ajudar os outros sabotadores, só aumentava o tiro dele.
 *
 * Por isso este ajuste vem depois de tudo. O método está em
 * `scripts/calibrar-individual.ts`: mede os 250 com 200 lutas cada (±7 pontos
 * por personagem), mexe só em quem está fora da faixa de 38% a 62%, empurra
 * para dentro da faixa e não para o meio, e repete quatro vezes. Depois confere
 * com sementes que não serviram para escolher nada.
 *
 * Medido assim: o desvio entre personagens caiu de 13,4 para 8,4 pontos, o
 * mais forte de 85% para 67%, e os fora da faixa de 94 para 25. Saitama não
 * entra (âncora da direção); Tempestade não precisou.
 *
 * O Light Yagami fica de fora: o problema dele era a regra da Death Note, e
 * ela foi corrigida na mecânica (`battle.ts`, `death-note.ts`). O fator só lhe
 * daria Vida, e com a Vida a mais a medição o chamava de "Tanque" — a ficha
 * diz "Pouca Vida". O Professor Xavier ficou: com o fator ele foi de 17% para
 * 23–28%, e o resto é o valor de coordenar, que a medição não vê.
 */
import type { Character, Effect } from '../engine/types';

export interface AjusteIndividual {
  /** Multiplica o dano do ataque básico, das habilidades e da Passiva. */
  dano?: number;
  /** Multiplica cura e Escudo das habilidades e da Passiva. */
  sustento?: number;
  /** Multiplica a Vida. */
  vida?: number;
}

/*
 * Piso de dano das habilidades, como o das famílias de utilidade em
 * `expanded-roster.ts`: o número é o ataque de referência. Para quem a família
 * não cobre e quase não causa dano — a Anya causava 82 de dano numa luta
 * inteira e ganhava 7%. Escolhido à mão; o fator da tabela vem por cima.
 */
export const pisosIndividuais: Readonly<Record<string, number>> = { anya: 50 };

/* tabela:inicio */
export const ajustesIndividuais: Readonly<Record<string, AjusteIndividual>> = {
  agent47: { dano: 0.65, sustento: 0.65, vida: 0.806 }, // Agente 47 · 62% na conferência
  aiolia: { dano: 0.6, sustento: 0.6, vida: 0.775 }, // Aiolia de Leão · 61% na conferência
  aizen: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Sosuke Aizen · 50% na conferência
  alucardcv: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Alucard · 40% na conferência
  antman: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Homem-Formiga · 45% na conferência
  anya: { dano: 1.35, sustento: 1.35, vida: 1.162 }, // Anya Forger · 42% na conferência
  arthas: { dano: 0.72, sustento: 0.72, vida: 0.849 }, // Arthas · 50% na conferência
  azula: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Azula · 59% na conferência
  batman: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Batman · 37% na conferência
  bayonetta: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Bayonetta · 42% na conferência
  bebop: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Bebop · 41% na conferência
  ben10: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Ben 10 · 44% na conferência
  billcipher: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Bill Cipher · 61% na conferência
  bobesponja: { dano: 1.5, sustento: 1.5, vida: 1.225 }, // Bob Esponja · 58% na conferência
  buzz: { dano: 0.61, sustento: 0.61, vida: 0.781 }, // Buzz Lightyear · 55% na conferência
  camus: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Camus de Aquário · 56% na conferência
  capitaoplaneta: { dano: 0.55, sustento: 0.55, vida: 0.742 }, // Capitão Planeta · 59% na conferência
  cartman: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Eric Cartman · 56% na conferência
  chunli: { dano: 1.13, sustento: 1.13, vida: 1.063 }, // Chun-Li · 36% na conferência
  coiote: { dano: 1.19, sustento: 1.19, vida: 1.091 }, // Coiote · 40% na conferência
  constantine: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Constantine · 43% na conferência
  coringa: { dano: 1.61, sustento: 1.61, vida: 1.269 }, // Coringa · 44% na conferência
  cyclops: { dano: 0.65, sustento: 0.65, vida: 0.806 }, // Ciclope · 60% na conferência
  dannyphantom: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Danny Phantom · 55% na conferência
  dante: { dano: 1.14, sustento: 1.14, vida: 1.068 }, // Dante · 42% na conferência
  darkseid: { dano: 0.67, sustento: 0.67, vida: 0.819 }, // Darkseid · 57% na conferência
  deadpool: { dano: 1.37, sustento: 1.37, vida: 1.17 }, // Deadpool · 46% na conferência
  dio: { dano: 1.39, sustento: 1.39, vida: 1.179 }, // Dio Brando · 47% na conferência
  docinho: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Docinho · 49% na conferência
  doctordoom: { dano: 1.78, sustento: 1.78, vida: 1.334 }, // Doutor Destino · 40% na conferência
  donald: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Pato Donald · 43% na conferência
  donatello: { dano: 1.32, sustento: 1.32, vida: 1.149 }, // Donatello · 43% na conferência
  doomslayer: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Doom Slayer · 59% na conferência
  ezio: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Ezio Auditore · 63% na conferência
  frieren: { dano: 1.3, sustento: 1.3, vida: 1.14 }, // Frieren · 40% na conferência
  gambit: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Gambit · 47% na conferência
  garou: { dano: 0.63, sustento: 0.63, vida: 0.794 }, // Garou · 55% na conferência
  genos: { dano: 0.74, sustento: 0.74, vida: 0.86 }, // Genos · 49% na conferência
  gojo: { dano: 1.47, sustento: 1.47, vida: 1.212 }, // Gojo · 38% na conferência
  goku: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Goku · 40% na conferência
  gordon: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Gordon Freeman · 45% na conferência
  greengoblin: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Duende Verde · 52% na conferência
  hadescz: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Hades · 54% na conferência
  hayabusa: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Ryu Hayabusa · 60% na conferência
  hellboy: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Hellboy · 51% na conferência
  homer: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Homer Simpson · 38% na conferência
  hulk: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Hulk · 56% na conferência
  ichigo: { dano: 1.13, sustento: 1.13, vida: 1.063 }, // Ichigo Kurosaki · 49% na conferência
  inosuke: { dano: 1.14, sustento: 1.14, vida: 1.068 }, // Inosuke Hashibira · 49% na conferência
  invencivel: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Invencível · 49% na conferência
  iroh: { dano: 0.74, sustento: 0.74, vida: 0.86 }, // Iroh · 57% na conferência
  itachi: { dano: 1.35, sustento: 1.35, vida: 1.162 }, // Itachi Uchiha · 41% na conferência
  jeangrey: { dano: 1.74, sustento: 1.74, vida: 1.319 }, // Jean Grey · 42% na conferência
  jerry: { dano: 1.21, sustento: 1.21, vida: 1.1 }, // Jerry · 47% na conferência
  jill: { dano: 0.55, sustento: 0.55, vida: 0.742 }, // Jill Valentine · 62% na conferência
  jin: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Jin Kazama · 56% na conferência
  jinwoo: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Sung Jinwoo · 61% na conferência
  jotaro: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Jotaro Kujo · 38% na conferência
  kaiba: { dano: 1.54, sustento: 1.54, vida: 1.241 }, // Seto Kaiba · 40% na conferência
  kakashi: { dano: 1.56, sustento: 1.56, vida: 1.249 }, // Kakashi Hatake · 41% na conferência
  kenpachi: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Kenpachi Zaraki · 52% na conferência
  kirby: { dano: 1.27, sustento: 1.27, vida: 1.127 }, // Kirby · 40% na conferência
  korra: { dano: 0.82, sustento: 0.82, vida: 0.906 }, // Korra · 55% na conferência
  kratos: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Kratos · 56% na conferência
  leonardo: { dano: 0.76, sustento: 0.76, vida: 0.872 }, // Leonardo · 47% na conferência
  lexluthor: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Lex Luthor · 50% na conferência
  liono: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Lion-O · 54% na conferência
  liukang: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Liu Kang · 62% na conferência
  loid: { dano: 1.48, sustento: 1.48, vida: 1.217 }, // Loid Forger · 51% na conferência
  loki: { dano: 1.32, sustento: 1.32, vida: 1.149 }, // Loki · 40% na conferência
  luffy: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Luffy · 44% na conferência
  madara: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Madara Uchiha · 63% na conferência
  magneto: { dano: 1.21, sustento: 1.21, vida: 1.1 }, // Magneto · 39% na conferência
  majinbuu: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Majin Boo · 56% na conferência
  malenia: { dano: 0.71, sustento: 0.71, vida: 0.843 }, // Malenia · 56% na conferência
  mario: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Mario · 56% na conferência
  marvin: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Marvin, o Marciano · 46% na conferência
  megaman: { dano: 1.19, sustento: 1.19, vida: 1.091 }, // Mega Man · 42% na conferência
  megatron: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Megatron · 53% na conferência
  megumi: { dano: 1.19, sustento: 1.19, vida: 1.091 }, // Megumi Fushiguro · 52% na conferência
  mewtwo: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Mewtwo · 63% na conferência
  mickey: { dano: 1.14, sustento: 1.14, vida: 1.068 }, // Mickey Mouse · 42% na conferência
  mikasa: { dano: 0.76, sustento: 0.76, vida: 0.872 }, // Mikasa Ackerman · 56% na conferência
  minato: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Minato Namikaze · 57% na conferência
  moonknight: { dano: 1.13, sustento: 1.13, vida: 1.063 }, // Cavaleiro da Lua · 48% na conferência
  mummra: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Mumm-Ra · 63% na conferência
  naruto: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Naruto · 42% na conferência
  nezuko: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Nezuko Kamado · 44% na conferência
  nobara: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Nobara Kugisaki · 58% na conferência
  omniman: { dano: 0.68, sustento: 0.68, vida: 0.825 }, // Omni-Man · 55% na conferência
  optimus: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Optimus Prime · 56% na conferência
  pain: { dano: 0.77, sustento: 0.77, vida: 0.877 }, // Pain · 66% na conferência
  pantera: { dano: 1.29, sustento: 1.29, vida: 1.136 }, // Pantera Cor-de-Rosa · 42% na conferência
  papaleguas: { dano: 1.42, sustento: 1.42, vida: 1.192 }, // Papa-Léguas · 49% na conferência
  patolino: { dano: 1.25, sustento: 1.25, vida: 1.118 }, // Patolino · 54% na conferência
  pernalonga: { dano: 1.28, sustento: 1.28, vida: 1.131 }, // Pernalonga · 44% na conferência
  piccolo: { dano: 1.8, sustento: 1.8, vida: 1.342 }, // Piccolo · 47% na conferência
  plankton: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Plankton · 48% na conferência
  popeye: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Popeye · 42% na conferência
  princeofpersia: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Príncipe da Pérsia · 51% na conferência
  professorx: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Professor Xavier · 28% na conferência
  pyramidhead: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Cabeça de Pirâmide · 48% na conferência
  raidenmgr: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Raiden (Metal Gear) · 48% na conferência
  raidenmk: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Raiden (Mortal Kombat) · 59% na conferência
  raven: { dano: 1.34, sustento: 1.34, vida: 1.158 }, // Ravena · 45% na conferência
  rick: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Rick Sanchez · 39% na conferência
  rocket: { dano: 1.49, sustento: 1.49, vida: 1.221 }, // Rocket Raccoon · 37% na conferência
  rogue: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Vampira · 52% na conferência
  sailormoon: { dano: 0.79, sustento: 0.79, vida: 0.889 }, // Sailor Moon · 64% na conferência
  sakura: { dano: 0.82, sustento: 0.82, vida: 0.906 }, // Sakura Haruno · 56% na conferência
  salsicha: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Salsicha · 49% na conferência
  samuraijack: { dano: 0.79, sustento: 0.79, vida: 0.889 }, // Samurai Jack · 55% na conferência
  sasuke: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Sasuke · 41% na conferência
  scarletwitch: { dano: 1.43, sustento: 1.43, vida: 1.196 }, // Feiticeira Escarlate · 42% na conferência
  scorpion: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Scorpion · 56% na conferência
  seiya: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Seiya · 42% na conferência
  sekiro: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Sekiro · 59% na conferência
  sephiroth: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Sephiroth · 57% na conferência
  shadowhh: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Shadow · 38% na conferência
  shaka: { dano: 0.8, sustento: 0.8, vida: 0.894 }, // Shaka de Virgem · 56% na conferência
  shredder: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Shredder · 54% na conferência
  skeletor: { dano: 0.74, sustento: 0.74, vida: 0.86 }, // Skeletor · 65% na conferência
  snake: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Solid Snake · 43% na conferência
  sora: { dano: 0.67, sustento: 0.67, vida: 0.819 }, // Sora · 65% na conferência
  spawn: { dano: 0.76, sustento: 0.76, vida: 0.872 }, // Spawn · 54% na conferência
  spiderman: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Homem-Aranha · 40% na conferência
  srincrivel: { dano: 0.62, sustento: 0.62, vida: 0.787 }, // Sr. Incrível · 53% na conferência
  stewie: { dano: 1.54, sustento: 1.54, vida: 1.241 }, // Stewie Griffin · 39% na conferência
  strange: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Doutor Estranho · 36% na conferência
  tanjiro: { dano: 0.78, sustento: 0.78, vida: 0.883 }, // Tanjiro Kamado · 52% na conferência
  taz: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Taz · 50% na conferência
  toph: { dano: 0.55, sustento: 0.55, vida: 0.742 }, // Toph · 49% na conferência
  vegeta: { dano: 1.24, sustento: 1.24, vida: 1.114 }, // Vegeta · 35% na conferência
  vergil: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Vergil · 62% na conferência
  vision: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Visão · 38% na conferência
  wesker: { dano: 0.69, sustento: 0.69, vida: 0.831 }, // Albert Wesker · 60% na conferência
  wolverine: { dano: 0.79, sustento: 0.79, vida: 0.889 }, // Wolverine · 52% na conferência
  woody: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Woody · 56% na conferência
  yor: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Yor Forger · 53% na conferência
  yugi: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Yugi Muto · 41% na conferência
  zeromm: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Zero · 56% na conferência
  zuko: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Zuko · 52% na conferência
};
/* tabela:fim */

const escalar = (efeitos: readonly Effect[], a: AjusteIndividual): Effect[] =>
  efeitos.map((e) => {
    if (e.kind === 'damage' && a.dano) return { ...e, value: Math.round(e.value * a.dano) };
    if ((e.kind === 'heal' || e.kind === 'shield') && a.sustento) return { ...e, value: Math.round(e.value * a.sustento) };
    return e;
  });

/* A mesma escada do piso das famílias: a terceira habilidade é a mais cara. */
const ESCALA_DO_PISO = [2.6, 3.2, 4.4] as const;

const comPiso = (efeitos: readonly Effect[], piso: number | undefined, indice: number): Effect[] => {
  if (!piso || efeitos.some((e) => e.kind === 'damage' || e.kind === 'release')) return [...efeitos];
  return [{ kind: 'damage', value: Math.round(piso * (ESCALA_DO_PISO[indice] ?? 3)), target: 'enemyWeak' }, ...efeitos];
};

export function calibrarIndividualmente(c: Character, ajuste?: AjusteIndividual): Character {
  const a = ajuste ?? ajustesIndividuais[c.id] ?? {};
  const piso = pisosIndividuais[c.id];
  if (!piso && Object.keys(a).length === 0) return c;
  return {
    ...c,
    hp: a.vida ? Math.round((c.hp * a.vida) / 10) * 10 : c.hp,
    basic: { ...c.basic, effects: escalar(c.basic.effects, a) },
    trait: { ...c.trait, effects: escalar(c.trait.effects, a) },
    skills: c.skills.map((s, i) => ({ ...s, effects: escalar(comPiso(s.effects, piso, i), a) })) as Character['skills'],
  };
}
