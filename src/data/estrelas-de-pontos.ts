/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… mostrando a porcentagem que eles somam pro trio"). Na tela, só as
 * estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, vale só o maior bônus.
 *
 * Medido em 2,64 milhões de jornadas de trios sorteados, sem bônus (plano pontos da fábrica, scripts/fabrica/lutas.ts):
 * o que cada personagem faz numa jornada muito boa (as 1% melhores das que vencem as 10 lutas). Cada nível tem uma
 * meta, e quem não chega nela ganha o que falta (arredondado para cima, em 5%) (pedido do jogador: "se o personagem
 * não chega até o valor… você tem que dar alguma porcentagem… isso vai para todos os personagens"):
 *   ★★★  2 milhões (a Sailor Moon faz 1,87 milhão: +10%);
 *   ★★   1,5 milhão;
 *   ★    1 milhão (todos já chegam: o que menos faz, faz 1,04 milhão).
 * Um personagem típico faz 1,29 milhão. Quem já passa da meta do nível fica com 0%. Os outros personagens ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  vegeta: { estrelas: 3, bonus: 75 }, // Vegeta
  coringa: { estrelas: 3, bonus: 70 }, // Coringa
  darthvader: { estrelas: 3, bonus: 70 }, // Darth Vader
  godzilla: { estrelas: 3, bonus: 70 }, // Godzilla
  guts: { estrelas: 3, bonus: 70 }, // Guts
  kratos: { estrelas: 3, bonus: 70 }, // Kratos
  neo: { estrelas: 3, bonus: 70 }, // Neo
  levi: { estrelas: 3, bonus: 65 }, // Levi Ackerman
  link: { estrelas: 3, bonus: 65 }, // Link
  dante: { estrelas: 3, bonus: 60 }, // Dante
  johnwick: { estrelas: 3, bonus: 60 }, // John Wick
  luffy: { estrelas: 3, bonus: 60 }, // Luffy
  pikachu: { estrelas: 3, bonus: 60 }, // Pikachu
  scorpion: { estrelas: 3, bonus: 60 }, // Scorpion
  sonic: { estrelas: 3, bonus: 60 }, // Sonic
  goku: { estrelas: 3, bonus: 55 }, // Goku
  itachi: { estrelas: 3, bonus: 55 }, // Itachi Uchiha
  jinwoo: { estrelas: 3, bonus: 55 }, // Sung Jinwoo
  light: { estrelas: 3, bonus: 55 }, // Light Yagami
  madara: { estrelas: 3, bonus: 55 }, // Madara Uchiha
  naruto: { estrelas: 3, bonus: 55 }, // Naruto
  sephiroth: { estrelas: 3, bonus: 55 }, // Sephiroth
  deadpool: { estrelas: 3, bonus: 50 }, // Deadpool
  ichigo: { estrelas: 3, bonus: 50 }, // Ichigo Kurosaki
  masterchief: { estrelas: 3, bonus: 50 }, // Master Chief
  batman: { estrelas: 3, bonus: 45 }, // Batman
  gojo: { estrelas: 3, bonus: 45 }, // Gojo
  thor: { estrelas: 3, bonus: 45 }, // Thor
  wolverine: { estrelas: 3, bonus: 45 }, // Wolverine
  allmight: { estrelas: 3, bonus: 40 }, // All Might
  doomslayer: { estrelas: 3, bonus: 40 }, // Doom Slayer
  saitama: { estrelas: 3, bonus: 40 }, // Saitama
  capitaoplaneta: { estrelas: 3, bonus: 15 }, // Capitão Planeta
  orihime: { estrelas: 3, bonus: 15 }, // Orihime Inoue
  sora: { estrelas: 3, bonus: 15 }, // Sora
  aerith: { estrelas: 3, bonus: 10 }, // Aerith
  alphonse: { estrelas: 3, bonus: 10 }, // Alphonse Elric
  coragem: { estrelas: 3, bonus: 10 }, // Coragem, o Cão Covarde
  isis: { estrelas: 3, bonus: 10 }, // Ísis
  sailormoon: { estrelas: 3, bonus: 10 }, // Sailor Moon
  // ★★
  mario: { estrelas: 2, bonus: 35 }, // Mario
  alucardcv: { estrelas: 2, bonus: 30 }, // Alucard
  geralt: { estrelas: 2, bonus: 25 }, // Geralt de Rívia
  seiya: { estrelas: 2, bonus: 25 }, // Seiya
  sesshomaru: { estrelas: 2, bonus: 25 }, // Sesshomaru
  cloud: { estrelas: 2, bonus: 20 }, // Cloud Strife
  dio: { estrelas: 2, bonus: 20 }, // Dio Brando
  killua: { estrelas: 2, bonus: 20 }, // Killua Zoldyck
  predator: { estrelas: 2, bonus: 20 }, // Predador
  spiderman: { estrelas: 2, bonus: 20 }, // Homem-Aranha
  jotaro: { estrelas: 2, bonus: 15 }, // Jotaro Kujo
  eren: { estrelas: 2, bonus: 10 }, // Eren Yeager
  ironman: { estrelas: 2, bonus: 10 }, // Homem de Ferro
  sukuna: { estrelas: 2, bonus: 10 }, // Ryomen Sukuna
  zoro: { estrelas: 2, bonus: 10 }, // Roronoa Zoro
  frieza: { estrelas: 2, bonus: 5 }, // Freeza
  sasuke: { estrelas: 2, bonus: 5 }, // Sasuke
  superman: { estrelas: 2, bonus: 5 }, // Superman
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
  aizen: { estrelas: 1, bonus: 0 }, // Sosuke Aizen
  anya: { estrelas: 1, bonus: 0 }, // Anya Forger
  arthas: { estrelas: 1, bonus: 0 }, // Arthas
  athena: { estrelas: 1, bonus: 0 }, // Atena
  broly: { estrelas: 1, bonus: 0 }, // Broly
  cartman: { estrelas: 1, bonus: 0 }, // Eric Cartman
  cyborg: { estrelas: 1, bonus: 0 }, // Ciborgue
  freddy: { estrelas: 1, bonus: 0 }, // Freddy Krueger
  galactus: { estrelas: 1, bonus: 0 }, // Galactus
  ganondorf: { estrelas: 1, bonus: 0 }, // Ganondorf
  gohan: { estrelas: 1, bonus: 0 }, // Gohan
  greenlantern: { estrelas: 1, bonus: 0 }, // Lanterna Verde
  hadescz: { estrelas: 1, bonus: 0 }, // Hades
  hercules: { estrelas: 1, bonus: 0 }, // Hércules
  hisoka: { estrelas: 1, bonus: 0 }, // Hisoka Morow
  hulk: { estrelas: 1, bonus: 0 }, // Hulk
  jake: { estrelas: 1, bonus: 0 }, // Jake
  jason: { estrelas: 1, bonus: 0 }, // Jason Voorhees
  kakashi: { estrelas: 1, bonus: 0 }, // Kakashi Hatake
  kenpachi: { estrelas: 1, bonus: 0 }, // Kenpachi Zaraki
  magneto: { estrelas: 1, bonus: 0 }, // Magneto
  megatron: { estrelas: 1, bonus: 0 }, // Megatron
  mewtwo: { estrelas: 1, bonus: 0 }, // Mewtwo
  minato: { estrelas: 1, bonus: 0 }, // Minato Namikaze
  optimus: { estrelas: 1, bonus: 0 }, // Optimus Prime
  pernalonga: { estrelas: 1, bonus: 0 }, // Pernalonga
  rick: { estrelas: 1, bonus: 0 }, // Rick Sanchez
  ryu: { estrelas: 1, bonus: 0 }, // Ryu
  salsicha: { estrelas: 1, bonus: 0 }, // Salsicha
  scooby: { estrelas: 1, bonus: 0 }, // Scooby-Doo
  senku: { estrelas: 1, bonus: 0 }, // Senku
  shaka: { estrelas: 1, bonus: 0 }, // Shaka de Virgem
  shera: { estrelas: 1, bonus: 0 }, // She-Ra
  shrek: { estrelas: 1, bonus: 0 }, // Shrek
  stewie: { estrelas: 1, bonus: 0 }, // Stewie Griffin
  t800: { estrelas: 1, bonus: 0 }, // Exterminador T-800
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
