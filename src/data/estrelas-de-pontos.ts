/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… mostrando a porcentagem que eles somam pro trio"). Na tela, só as
 * estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, conta um só (bonusDoTrio, abaixo).
 *
 * Medido em 2,64 milhões de jornadas de trios sorteados, sem bônus (plano pontos da fábrica, scripts/fabrica/lutas.ts):
 * o que cada personagem faz numa jornada muito boa (as 1% melhores das que vencem as 10 lutas). Cada nível tem uma
 * meta, e quem não chega nela ganha o que falta (arredondado para cima, em 5%) (pedido do jogador: "se o personagem
 * não chega até o valor… você tem que dar alguma porcentagem… isso vai para todos os personagens"):
 *   ★★★  2 milhões (a Sailor Moon faz 1,87 milhão: +10%);
 *   ★★   1,75 milhão;
 *   ★    1,5 milhão (com 1 milhão, todos já chegavam: o que menos faz, faz 1,04 milhão).
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
  mario: { estrelas: 2, bonus: 55 }, // Mario
  alucardcv: { estrelas: 2, bonus: 50 }, // Alucard
  geralt: { estrelas: 2, bonus: 45 }, // Geralt de Rívia
  seiya: { estrelas: 2, bonus: 45 }, // Seiya
  sesshomaru: { estrelas: 2, bonus: 45 }, // Sesshomaru
  cloud: { estrelas: 2, bonus: 40 }, // Cloud Strife
  dio: { estrelas: 2, bonus: 40 }, // Dio Brando
  killua: { estrelas: 2, bonus: 40 }, // Killua Zoldyck
  predator: { estrelas: 2, bonus: 40 }, // Predador
  spiderman: { estrelas: 2, bonus: 40 }, // Homem-Aranha
  eren: { estrelas: 2, bonus: 30 }, // Eren Yeager
  ironman: { estrelas: 2, bonus: 30 }, // Homem de Ferro
  jotaro: { estrelas: 2, bonus: 30 }, // Jotaro Kujo
  zoro: { estrelas: 2, bonus: 30 }, // Roronoa Zoro
  frieza: { estrelas: 2, bonus: 25 }, // Freeza
  sasuke: { estrelas: 2, bonus: 25 }, // Sasuke
  sukuna: { estrelas: 2, bonus: 25 }, // Ryomen Sukuna
  superman: { estrelas: 2, bonus: 25 }, // Superman
  sakura: { estrelas: 2, bonus: 15 }, // Sakura Haruno
  aphrodite: { estrelas: 2, bonus: 10 }, // Afrodite
  captain: { estrelas: 2, bonus: 10 }, // Capitão América
  gandalf: { estrelas: 2, bonus: 10 }, // Gandalf
  groot: { estrelas: 2, bonus: 10 }, // Groot
  katara: { estrelas: 2, bonus: 10 }, // Katara
  leorio: { estrelas: 2, bonus: 10 }, // Leorio
  mulherelastica: { estrelas: 2, bonus: 10 }, // Mulher-Elástica
  odin: { estrelas: 2, bonus: 10 }, // Odin
  peach: { estrelas: 2, bonus: 10 }, // Princesa Peach
  raven: { estrelas: 2, bonus: 10 }, // Ravena
  rem: { estrelas: 2, bonus: 10 }, // Rem
  steven: { estrelas: 2, bonus: 10 }, // Steven Universo
  strange: { estrelas: 2, bonus: 10 }, // Doutor Estranho
  thanos: { estrelas: 2, bonus: 10 }, // Thanos
  apollo: { estrelas: 2, bonus: 5 }, // Apolo
  chopper: { estrelas: 2, bonus: 5 }, // Tony Tony Chopper
  cosmowanda: { estrelas: 2, bonus: 5 }, // Cosmo e Wanda
  jeangrey: { estrelas: 2, bonus: 5 }, // Jean Grey
  tsunade: { estrelas: 2, bonus: 5 }, // Tsunade
  giorno: { estrelas: 2, bonus: 0 }, // Giorno Giovanna
  jill: { estrelas: 2, bonus: 0 }, // Jill Valentine
  // ★
  t800: { estrelas: 1, bonus: 30 }, // Exterminador T-800
  jason: { estrelas: 1, bonus: 25 }, // Jason Voorhees
  hisoka: { estrelas: 1, bonus: 20 }, // Hisoka Morow
  kakashi: { estrelas: 1, bonus: 20 }, // Kakashi Hatake
  kenpachi: { estrelas: 1, bonus: 20 }, // Kenpachi Zaraki
  broly: { estrelas: 1, bonus: 15 }, // Broly
  gohan: { estrelas: 1, bonus: 15 }, // Gohan
  minato: { estrelas: 1, bonus: 15 }, // Minato Namikaze
  pernalonga: { estrelas: 1, bonus: 15 }, // Pernalonga
  ryu: { estrelas: 1, bonus: 15 }, // Ryu
  freddy: { estrelas: 1, bonus: 10 }, // Freddy Krueger
  megatron: { estrelas: 1, bonus: 10 }, // Megatron
  aizen: { estrelas: 1, bonus: 5 }, // Sosuke Aizen
  anya: { estrelas: 1, bonus: 5 }, // Anya Forger
  arthas: { estrelas: 1, bonus: 5 }, // Arthas
  athena: { estrelas: 1, bonus: 5 }, // Atena
  cartman: { estrelas: 1, bonus: 5 }, // Eric Cartman
  cyborg: { estrelas: 1, bonus: 5 }, // Ciborgue
  greenlantern: { estrelas: 1, bonus: 5 }, // Lanterna Verde
  hercules: { estrelas: 1, bonus: 5 }, // Hércules
  hulk: { estrelas: 1, bonus: 5 }, // Hulk
  jake: { estrelas: 1, bonus: 5 }, // Jake
  mewtwo: { estrelas: 1, bonus: 5 }, // Mewtwo
  optimus: { estrelas: 1, bonus: 5 }, // Optimus Prime
  rick: { estrelas: 1, bonus: 5 }, // Rick Sanchez
  salsicha: { estrelas: 1, bonus: 5 }, // Salsicha
  shera: { estrelas: 1, bonus: 5 }, // She-Ra
  shrek: { estrelas: 1, bonus: 5 }, // Shrek
  stewie: { estrelas: 1, bonus: 5 }, // Stewie Griffin
  woody: { estrelas: 1, bonus: 5 }, // Woody
  yoda: { estrelas: 1, bonus: 5 }, // Yoda
  zelda: { estrelas: 1, bonus: 5 }, // Zelda
  galactus: { estrelas: 1, bonus: 0 }, // Galactus
  ganondorf: { estrelas: 1, bonus: 0 }, // Ganondorf
  hadescz: { estrelas: 1, bonus: 0 }, // Hades
  magneto: { estrelas: 1, bonus: 0 }, // Magneto
  scooby: { estrelas: 1, bonus: 0 }, // Scooby-Doo
  senku: { estrelas: 1, bonus: 0 }, // Senku
  shaka: { estrelas: 1, bonus: 0 }, // Shaka de Virgem
  wonderwoman: { estrelas: 1, bonus: 0 }, // Mulher-Maravilha
};

/**
 * O bônus de pontos do trio (fração: 0,85 = +85%) e de quem ele vem. Conta um só: primeiro quem tem mais estrelas e,
 * entre os de mesmo número de estrelas, a maior porcentagem (pedido do jogador: "primeiro olha a estrela… depois a
 * porcentagem": quem tem mais estrelas já faz mais pontos naturalmente).
 */
export function bonusDoTrio(trio: readonly string[]): { bonus: number; de?: string } {
  let escolhido: string | undefined;
  for (const id of trio) {
    const e = ESTRELAS_DE_PONTOS[id], atual = escolhido ? ESTRELAS_DE_PONTOS[escolhido]! : undefined;
    if (e && (!atual || e.estrelas > atual.estrelas || (e.estrelas === atual.estrelas && e.bonus > atual.bonus))) escolhido = id;
  }
  const bonus = escolhido ? ESTRELAS_DE_PONTOS[escolhido]!.bonus / 100 : 0;
  return bonus > 0 ? { bonus, de: escolhido } : { bonus: 0 };
}
