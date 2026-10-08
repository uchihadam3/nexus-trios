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
 * O que um número não resolve fica de fora daqui e está dito no relatório.
 * Light Yagami (13%) e Anya Forger (17%) chegaram ao fator máximo sem sair do
 * lugar — o problema deles é de mecânica: a Death Note não alcança 69 dos 250,
 * e a Anya quase não causa dano. O fator só lhes dava Vida, e a Vida a mais
 * fazia o Light ser medido como "Tanque", o que ele não é. Então eles saíram
 * da tabela. O Professor Xavier ficou: com o fator ele foi de 21% para 27%.
 *
 * O ritmo não é tocado: o intervalo do ataque básico, a Carga, o Preparo e a
 * Recarga ficam como estão, porque são o que o jogador sente. Mexe-se só em
 * quanto cada coisa vale — dano (do básico, das habilidades e da Passiva), cura
 * e Escudo, e Vida. A ficha é gerada a partir dos efeitos, então os números na
 * tela acompanham.
 *
 * A tabela entre os marcadores é escrita por `scripts/calibrar-individual.ts`,
 * que mede, ajusta quem está fora da faixa e mede de novo.
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
  agent47: { dano: 0.65, sustento: 0.65, vida: 0.806 }, // Agente 47 · 63% na conferência
  aiolia: { dano: 0.6, sustento: 0.6, vida: 0.775 }, // Aiolia de Leão · 64% na conferência
  aizen: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Sosuke Aizen · 52% na conferência
  alucardcv: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Alucard · 42% na conferência
  antman: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Homem-Formiga · 48% na conferência
  anya: { dano: 1.37, sustento: 1.37, vida: 1.17 }, // Anya Forger · 44% na conferência
  arthas: { dano: 0.72, sustento: 0.72, vida: 0.849 }, // Arthas · 50% na conferência
  azula: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Azula · 61% na conferência
  batman: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Batman · 40% na conferência
  bayonetta: { dano: 1.4, sustento: 1.4, vida: 1.183 }, // Bayonetta · 41% na conferência
  bebop: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Bebop · 41% na conferência
  ben10: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Ben 10 · 45% na conferência
  billcipher: { dano: 0.64, sustento: 0.64, vida: 0.8 }, // Bill Cipher · 60% na conferência
  bobesponja: { dano: 1.5, sustento: 1.5, vida: 1.225 }, // Bob Esponja · 53% na conferência
  buzz: { dano: 0.6, sustento: 0.6, vida: 0.775 }, // Buzz Lightyear · 55% na conferência
  capitaoplaneta: { dano: 0.57, sustento: 0.57, vida: 0.755 }, // Capitão Planeta · 64% na conferência
  cartman: { dano: 0.85, sustento: 0.85, vida: 0.922 }, // Eric Cartman · 55% na conferência
  chunli: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Chun-Li · 43% na conferência
  coiote: { dano: 1.19, sustento: 1.19, vida: 1.091 }, // Coiote · 44% na conferência
  constantine: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Constantine · 41% na conferência
  coringa: { dano: 1.63, sustento: 1.63, vida: 1.277 }, // Coringa · 45% na conferência
  cyclops: { dano: 0.63, sustento: 0.63, vida: 0.794 }, // Ciclope · 57% na conferência
  dante: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Dante · 41% na conferência
  darkseid: { dano: 0.67, sustento: 0.67, vida: 0.819 }, // Darkseid · 57% na conferência
  deadpool: { dano: 1.35, sustento: 1.35, vida: 1.162 }, // Deadpool · 44% na conferência
  dio: { dano: 1.35, sustento: 1.35, vida: 1.162 }, // Dio Brando · 41% na conferência
  docinho: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Docinho · 50% na conferência
  doctordoom: { dano: 1.6, sustento: 1.6, vida: 1.265 }, // Doutor Destino · 37% na conferência
  donald: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Pato Donald · 45% na conferência
  donatello: { dano: 1.3, sustento: 1.3, vida: 1.14 }, // Donatello · 41% na conferência
  doomslayer: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Doom Slayer · 59% na conferência
  ezio: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Ezio Auditore · 60% na conferência
  frieren: { dano: 1.3, sustento: 1.3, vida: 1.14 }, // Frieren · 43% na conferência
  garou: { dano: 0.65, sustento: 0.65, vida: 0.806 }, // Garou · 60% na conferência
  genos: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Genos · 50% na conferência
  gojo: { dano: 1.49, sustento: 1.49, vida: 1.221 }, // Gojo · 37% na conferência
  goku: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Goku · 38% na conferência
  gordon: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Gordon Freeman · 47% na conferência
  greengoblin: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Duende Verde · 52% na conferência
  hadescz: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Hades · 56% na conferência
  hayabusa: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Ryu Hayabusa · 60% na conferência
  hellboy: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Hellboy · 52% na conferência
  homer: { dano: 1.32, sustento: 1.32, vida: 1.149 }, // Homer Simpson · 43% na conferência
  hulk: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Hulk · 57% na conferência
  ichigo: { dano: 1.13, sustento: 1.13, vida: 1.063 }, // Ichigo Kurosaki · 47% na conferência
  inosuke: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Inosuke Hashibira · 47% na conferência
  iroh: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Iroh · 60% na conferência
  itachi: { dano: 1.33, sustento: 1.33, vida: 1.153 }, // Itachi Uchiha · 40% na conferência
  jeangrey: { dano: 1.76, sustento: 1.76, vida: 1.327 }, // Jean Grey · 42% na conferência
  jerry: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Jerry · 48% na conferência
  jill: { dano: 0.56, sustento: 0.56, vida: 0.748 }, // Jill Valentine · 62% na conferência
  jin: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Jin Kazama · 55% na conferência
  jinwoo: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Sung Jinwoo · 59% na conferência
  jotaro: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Jotaro Kujo · 41% na conferência
  kaiba: { dano: 1.58, sustento: 1.58, vida: 1.257 }, // Seto Kaiba · 41% na conferência
  kakashi: { dano: 1.56, sustento: 1.56, vida: 1.249 }, // Kakashi Hatake · 40% na conferência
  kenpachi: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Kenpachi Zaraki · 51% na conferência
  kirby: { dano: 1.26, sustento: 1.26, vida: 1.122 }, // Kirby · 39% na conferência
  korra: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Korra · 54% na conferência
  kratos: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Kratos · 58% na conferência
  leonardo: { dano: 0.77, sustento: 0.77, vida: 0.877 }, // Leonardo · 49% na conferência
  lexluthor: { dano: 1.39, sustento: 1.39, vida: 1.179 }, // Lex Luthor · 47% na conferência
  link: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Link · 46% na conferência
  liono: { dano: 0.8, sustento: 0.8, vida: 0.894 }, // Lion-O · 53% na conferência
  liukang: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Liu Kang · 63% na conferência
  loid: { dano: 1.49, sustento: 1.49, vida: 1.221 }, // Loid Forger · 46% na conferência
  loki: { dano: 1.18, sustento: 1.18, vida: 1.086 }, // Loki · 34% na conferência
  luffy: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Luffy · 47% na conferência
  madara: { dano: 0.86, sustento: 0.86, vida: 0.927 }, // Madara Uchiha · 66% na conferência
  magneto: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Magneto · 43% na conferência
  majinbuu: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Majin Boo · 61% na conferência
  malenia: { dano: 0.7, sustento: 0.7, vida: 0.837 }, // Malenia · 54% na conferência
  mario: { dano: 1.17, sustento: 1.17, vida: 1.082 }, // Mario · 53% na conferência
  marvin: { dano: 1.22, sustento: 1.22, vida: 1.105 }, // Marvin, o Marciano · 48% na conferência
  megaman: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Mega Man · 44% na conferência
  megatron: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Megatron · 54% na conferência
  megumi: { dano: 1.2, sustento: 1.2, vida: 1.095 }, // Megumi Fushiguro · 53% na conferência
  mewtwo: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Mewtwo · 60% na conferência
  mickey: { dano: 1.13, sustento: 1.13, vida: 1.063 }, // Mickey Mouse · 40% na conferência
  mikasa: { dano: 0.76, sustento: 0.76, vida: 0.872 }, // Mikasa Ackerman · 57% na conferência
  minato: { dano: 0.85, sustento: 0.85, vida: 0.922 }, // Minato Namikaze · 55% na conferência
  moonknight: { dano: 1.14, sustento: 1.14, vida: 1.068 }, // Cavaleiro da Lua · 50% na conferência
  mummra: { dano: 0.77, sustento: 0.77, vida: 0.877 }, // Mumm-Ra · 53% na conferência
  naruto: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Naruto · 44% na conferência
  nezuko: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Nezuko Kamado · 43% na conferência
  nobara: { dano: 0.62, sustento: 0.62, vida: 0.787 }, // Nobara Kugisaki · 56% na conferência
  omniman: { dano: 0.68, sustento: 0.68, vida: 0.825 }, // Omni-Man · 55% na conferência
  optimus: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Optimus Prime · 55% na conferência
  pain: { dano: 0.77, sustento: 0.77, vida: 0.877 }, // Pain · 67% na conferência
  pantera: { dano: 1.26, sustento: 1.26, vida: 1.122 }, // Pantera Cor-de-Rosa · 40% na conferência
  papaleguas: { dano: 1.4, sustento: 1.4, vida: 1.183 }, // Papa-Léguas · 46% na conferência
  patolino: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Patolino · 48% na conferência
  pernalonga: { dano: 1.42, sustento: 1.42, vida: 1.192 }, // Pernalonga · 52% na conferência
  piccolo: { dano: 1.81, sustento: 1.81, vida: 1.345 }, // Piccolo · 42% na conferência
  plankton: { dano: 1.14, sustento: 1.14, vida: 1.068 }, // Plankton · 50% na conferência
  popeye: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Popeye · 43% na conferência
  princeofpersia: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Príncipe da Pérsia · 52% na conferência
  professorx: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Professor Xavier · 25% na conferência
  raidenmgr: { dano: 0.81, sustento: 0.81, vida: 0.9 }, // Raiden (Metal Gear) · 48% na conferência
  raidenmk: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Raiden (Mortal Kombat) · 62% na conferência
  raven: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Ravena · 46% na conferência
  rick: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Rick Sanchez · 40% na conferência
  rocket: { dano: 1.47, sustento: 1.47, vida: 1.212 }, // Rocket Raccoon · 40% na conferência
  rogue: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Vampira · 55% na conferência
  sailormoon: { dano: 0.67, sustento: 0.67, vida: 0.819 }, // Sailor Moon · 51% na conferência
  saitama: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Saitama · 47% na conferência
  sakura: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Sakura Haruno · 54% na conferência
  salsicha: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Salsicha · 45% na conferência
  samuraijack: { dano: 0.78, sustento: 0.78, vida: 0.883 }, // Samurai Jack · 55% na conferência
  sasuke: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Sasuke · 38% na conferência
  scarletwitch: { dano: 1.6, sustento: 1.6, vida: 1.265 }, // Feiticeira Escarlate · 47% na conferência
  scorpion: { dano: 0.59, sustento: 0.59, vida: 0.768 }, // Scorpion · 52% na conferência
  seiya: { dano: 1.16, sustento: 1.16, vida: 1.077 }, // Seiya · 46% na conferência
  sekiro: { dano: 0.9, sustento: 0.9, vida: 0.949 }, // Sekiro · 59% na conferência
  sephiroth: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Sephiroth · 54% na conferência
  shadowhh: { dano: 1.12, sustento: 1.12, vida: 1.058 }, // Shadow · 42% na conferência
  shaka: { dano: 0.79, sustento: 0.79, vida: 0.889 }, // Shaka de Virgem · 56% na conferência
  shredder: { dano: 0.88, sustento: 0.88, vida: 0.938 }, // Shredder · 55% na conferência
  skeletor: { dano: 0.74, sustento: 0.74, vida: 0.86 }, // Skeletor · 64% na conferência
  snake: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Solid Snake · 39% na conferência
  sora: { dano: 0.66, sustento: 0.66, vida: 0.812 }, // Sora · 61% na conferência
  spawn: { dano: 0.77, sustento: 0.77, vida: 0.877 }, // Spawn · 50% na conferência
  spiderman: { dano: 1.15, sustento: 1.15, vida: 1.072 }, // Homem-Aranha · 43% na conferência
  srincrivel: { dano: 0.63, sustento: 0.63, vida: 0.794 }, // Sr. Incrível · 52% na conferência
  stewie: { dano: 1.54, sustento: 1.54, vida: 1.241 }, // Stewie Griffin · 42% na conferência
  strange: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Doutor Estranho · 34% na conferência
  tanjiro: { dano: 0.78, sustento: 0.78, vida: 0.883 }, // Tanjiro Kamado · 51% na conferência
  taz: { dano: 0.85, sustento: 0.85, vida: 0.922 }, // Taz · 49% na conferência
  toph: { dano: 0.57, sustento: 0.57, vida: 0.755 }, // Toph · 56% na conferência
  vegeta: { dano: 1.41, sustento: 1.41, vida: 1.187 }, // Vegeta · 45% na conferência
  vision: { dano: 1.11, sustento: 1.11, vida: 1.054 }, // Visão · 39% na conferência
  wesker: { dano: 0.67, sustento: 0.67, vida: 0.819 }, // Albert Wesker · 60% na conferência
  wolverine: { dano: 0.79, sustento: 0.79, vida: 0.889 }, // Wolverine · 52% na conferência
  woody: { dano: 0.89, sustento: 0.89, vida: 0.943 }, // Woody · 56% na conferência
  yor: { dano: 0.83, sustento: 0.83, vida: 0.911 }, // Yor Forger · 62% na conferência
  yugi: { dano: 1.9, sustento: 1.9, vida: 1.378 }, // Yugi Muto · 41% na conferência
  zeromm: { dano: 0.87, sustento: 0.87, vida: 0.933 }, // Zero · 56% na conferência
  zuko: { dano: 0.75, sustento: 0.75, vida: 0.866 }, // Zuko · 48% na conferência
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
