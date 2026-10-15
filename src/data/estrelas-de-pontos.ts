/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… mostrando a porcentagem que eles somam pro trio"). Na tela, só as
 * estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, vale só o maior bônus.
 *
 * Medido em 2,64 milhões de jornadas de trios sorteados, sem bônus (plano pontos da fábrica, scripts/fabrica/lutas.ts):
 * o que cada personagem faz numa jornada muito boa (as 1% melhores das que vencem as 10 lutas). Quem já faz isso
 * naturalmente entra com 0% (pedido do jogador: "os personagens que já fazem isso de ponto, eles já são estrela"); os
 * outros de cada nível ganham o bônus que os leva ao personagem de referência (pedido: "usa um personagem que faz um
 * milhão e meio como exemplo… não colocar um valor aleatório"):
 *   ★★★  como a Sailor Moon (1,87 milhão; 8 já fazem: Sailor Moon, Coragem, Ísis, Capitão Planeta…);
 *   ★★   como a Princesa Peach (1,65 milhão; 22 já fazem);
 *   ★    como o Salsicha (1,48 milhão; 28 já fazem).
 * Um personagem típico faz 1,29 milhão. Os outros ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  coringa: { estrelas: 3, bonus: 60 }, // Coringa
  darthvader: { estrelas: 3, bonus: 60 }, // Darth Vader
  kratos: { estrelas: 3, bonus: 60 }, // Kratos
  neo: { estrelas: 3, bonus: 60 }, // Neo
  vegeta: { estrelas: 3, bonus: 60 }, // Vegeta
  godzilla: { estrelas: 3, bonus: 55 }, // Godzilla
  guts: { estrelas: 3, bonus: 55 }, // Guts
  dante: { estrelas: 3, bonus: 50 }, // Dante
  levi: { estrelas: 3, bonus: 50 }, // Levi Ackerman
  link: { estrelas: 3, bonus: 50 }, // Link
  pikachu: { estrelas: 3, bonus: 50 }, // Pikachu
  sonic: { estrelas: 3, bonus: 50 }, // Sonic
  goku: { estrelas: 3, bonus: 45 }, // Goku
  jinwoo: { estrelas: 3, bonus: 45 }, // Sung Jinwoo
  johnwick: { estrelas: 3, bonus: 45 }, // John Wick
  luffy: { estrelas: 3, bonus: 45 }, // Luffy
  scorpion: { estrelas: 3, bonus: 45 }, // Scorpion
  sephiroth: { estrelas: 3, bonus: 45 }, // Sephiroth
  deadpool: { estrelas: 3, bonus: 40 }, // Deadpool
  ichigo: { estrelas: 3, bonus: 40 }, // Ichigo Kurosaki
  itachi: { estrelas: 3, bonus: 40 }, // Itachi Uchiha
  light: { estrelas: 3, bonus: 40 }, // Light Yagami
  madara: { estrelas: 3, bonus: 40 }, // Madara Uchiha
  masterchief: { estrelas: 3, bonus: 40 }, // Master Chief
  naruto: { estrelas: 3, bonus: 40 }, // Naruto
  batman: { estrelas: 3, bonus: 35 }, // Batman
  gojo: { estrelas: 3, bonus: 35 }, // Gojo
  thor: { estrelas: 3, bonus: 35 }, // Thor
  wolverine: { estrelas: 3, bonus: 35 }, // Wolverine
  allmight: { estrelas: 3, bonus: 30 }, // All Might
  doomslayer: { estrelas: 3, bonus: 30 }, // Doom Slayer
  saitama: { estrelas: 3, bonus: 30 }, // Saitama
  aerith: { estrelas: 3, bonus: 0 }, // Aerith
  alphonse: { estrelas: 3, bonus: 0 }, // Alphonse Elric
  capitaoplaneta: { estrelas: 3, bonus: 0 }, // Capitão Planeta
  coragem: { estrelas: 3, bonus: 0 }, // Coragem, o Cão Covarde
  isis: { estrelas: 3, bonus: 0 }, // Ísis
  orihime: { estrelas: 3, bonus: 0 }, // Orihime Inoue
  sailormoon: { estrelas: 3, bonus: 0 }, // Sailor Moon
  sora: { estrelas: 3, bonus: 0 }, // Sora
  // ★★
  mario: { estrelas: 2, bonus: 45 }, // Mario
  alucardcv: { estrelas: 2, bonus: 40 }, // Alucard
  geralt: { estrelas: 2, bonus: 35 }, // Geralt de Rívia
  seiya: { estrelas: 2, bonus: 35 }, // Seiya
  cloud: { estrelas: 2, bonus: 30 }, // Cloud Strife
  dio: { estrelas: 2, bonus: 30 }, // Dio Brando
  killua: { estrelas: 2, bonus: 30 }, // Killua Zoldyck
  predator: { estrelas: 2, bonus: 30 }, // Predador
  sesshomaru: { estrelas: 2, bonus: 30 }, // Sesshomaru
  spiderman: { estrelas: 2, bonus: 30 }, // Homem-Aranha
  eren: { estrelas: 2, bonus: 20 }, // Eren Yeager
  ironman: { estrelas: 2, bonus: 20 }, // Homem de Ferro
  jotaro: { estrelas: 2, bonus: 20 }, // Jotaro Kujo
  zoro: { estrelas: 2, bonus: 20 }, // Roronoa Zoro
  frieza: { estrelas: 2, bonus: 15 }, // Freeza
  sasuke: { estrelas: 2, bonus: 15 }, // Sasuke
  sukuna: { estrelas: 2, bonus: 15 }, // Ryomen Sukuna
  superman: { estrelas: 2, bonus: 15 }, // Superman
  aphrodite: { estrelas: 2, bonus: 0 }, // Afrodite
  apollo: { estrelas: 2, bonus: 0 }, // Apolo
  captain: { estrelas: 2, bonus: 0 }, // Capitão América
  chopper: { estrelas: 2, bonus: 0 }, // Tony Tony Chopper
  cosmowanda: { estrelas: 2, bonus: 0 }, // Cosmo e Wanda
  gandalf: { estrelas: 2, bonus: 0 }, // Gandalf
  giorno: { estrelas: 2, bonus: 0 }, // Giorno Giovanna
  groot: { estrelas: 2, bonus: 0 }, // Groot
  jeangrey: { estrelas: 2, bonus: 0 }, // Jean Grey
  jill: { estrelas: 2, bonus: 0 }, // Jill Valentine
  katara: { estrelas: 2, bonus: 0 }, // Katara
  leorio: { estrelas: 2, bonus: 0 }, // Leorio
  mulherelastica: { estrelas: 2, bonus: 0 }, // Mulher-Elástica
  odin: { estrelas: 2, bonus: 0 }, // Odin
  peach: { estrelas: 2, bonus: 0 }, // Princesa Peach
  raven: { estrelas: 2, bonus: 0 }, // Ravena
  rem: { estrelas: 2, bonus: 0 }, // Rem
  sakura: { estrelas: 2, bonus: 0 }, // Sakura Haruno
  steven: { estrelas: 2, bonus: 0 }, // Steven Universo
  strange: { estrelas: 2, bonus: 0 }, // Doutor Estranho
  thanos: { estrelas: 2, bonus: 0 }, // Thanos
  tsunade: { estrelas: 2, bonus: 0 }, // Tsunade
  // ★
  t800: { estrelas: 1, bonus: 25 }, // Exterminador T-800
  jason: { estrelas: 1, bonus: 20 }, // Jason Voorhees
  broly: { estrelas: 1, bonus: 15 }, // Broly
  gohan: { estrelas: 1, bonus: 15 }, // Gohan
  hisoka: { estrelas: 1, bonus: 15 }, // Hisoka Morow
  kakashi: { estrelas: 1, bonus: 15 }, // Kakashi Hatake
  kenpachi: { estrelas: 1, bonus: 15 }, // Kenpachi Zaraki
  megatron: { estrelas: 1, bonus: 10 }, // Megatron
  minato: { estrelas: 1, bonus: 10 }, // Minato Namikaze
  pernalonga: { estrelas: 1, bonus: 10 }, // Pernalonga
  ryu: { estrelas: 1, bonus: 10 }, // Ryu
  freddy: { estrelas: 1, bonus: 5 }, // Freddy Krueger
  aizen: { estrelas: 1, bonus: 0 }, // Sosuke Aizen
  anya: { estrelas: 1, bonus: 0 }, // Anya Forger
  arthas: { estrelas: 1, bonus: 0 }, // Arthas
  athena: { estrelas: 1, bonus: 0 }, // Atena
  cartman: { estrelas: 1, bonus: 0 }, // Eric Cartman
  cyborg: { estrelas: 1, bonus: 0 }, // Ciborgue
  galactus: { estrelas: 1, bonus: 0 }, // Galactus
  ganondorf: { estrelas: 1, bonus: 0 }, // Ganondorf
  greenlantern: { estrelas: 1, bonus: 0 }, // Lanterna Verde
  hadescz: { estrelas: 1, bonus: 0 }, // Hades
  hercules: { estrelas: 1, bonus: 0 }, // Hércules
  hulk: { estrelas: 1, bonus: 0 }, // Hulk
  jake: { estrelas: 1, bonus: 0 }, // Jake
  magneto: { estrelas: 1, bonus: 0 }, // Magneto
  mewtwo: { estrelas: 1, bonus: 0 }, // Mewtwo
  optimus: { estrelas: 1, bonus: 0 }, // Optimus Prime
  rick: { estrelas: 1, bonus: 0 }, // Rick Sanchez
  salsicha: { estrelas: 1, bonus: 0 }, // Salsicha
  scooby: { estrelas: 1, bonus: 0 }, // Scooby-Doo
  senku: { estrelas: 1, bonus: 0 }, // Senku
  shaka: { estrelas: 1, bonus: 0 }, // Shaka de Virgem
  shera: { estrelas: 1, bonus: 0 }, // She-Ra
  shrek: { estrelas: 1, bonus: 0 }, // Shrek
  stewie: { estrelas: 1, bonus: 0 }, // Stewie Griffin
  wonderwoman: { estrelas: 1, bonus: 0 }, // Mulher-Maravilha
  woody: { estrelas: 1, bonus: 0 }, // Woody
  yoda: { estrelas: 1, bonus: 0 }, // Yoda
  zelda: { estrelas: 1, bonus: 0 }, // Zelda
};

/** O bônus de pontos do trio (fração: 0,85 = +85%) e de quem ele vem: o maior entre os três. */
export function bonusDoTrio(trio: readonly string[]): { bonus: number; de?: string } {
  let melhor: { bonus: number; de?: string } = { bonus: 0 };
  for (const id of trio) { const e = ESTRELAS_DE_PONTOS[id]; if (e && e.bonus / 100 > melhor.bonus) melhor = { bonus: e.bonus / 100, de: id }; }
  return melhor;
}
