/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto… mostrando a
 * porcentagem que eles somam pro trio"). Na tela, só as estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, conta um só (bonusDoTrio, abaixo).
 *
 * As estrelas vão para quem MENOS chega ao fim (pedido do jogador: "seria legal se esses bônus… fossem justamente pros
 * personagens que não conseguem chegar tão fácil… senão todo mundo vai jogar com os que já são os mais fortes").
 * Medido em 2,64 milhões de jornadas de trios sorteados, sem bônus (plano pontos da fábrica, scripts/fabrica/lutas.ts):
 * em média 5,4% delas vencem as 10 lutas; com o personagem mais forte, 11%. Os 120 que menos vencem as 10 ganham
 * estrelas — quanto mais difícil, mais estrelas:
 *   ★★★  os 40 que menos terminam (2,7% a 3,9%), meta de 2 milhões;
 *   ★★   os 40 seguintes (3,9% a 4,4%), meta de 1,75 milhão;
 *   ★    os 40 seguintes (4,4% a 4,6%), meta de 1,5 milhão.
 * O bônus é o que falta para a meta a partir do que o personagem faz numa jornada muito boa (as 1% melhores das que
 * vencem as 10 lutas), arredondado para cima em 5%: ★★★ +35% a +85%, ★★ +15% a +60%,
 * ★ +5% a +40%. Os outros personagens ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  jacksparrow: { estrelas: 3, bonus: 85 }, // Jack Sparrow
  ben10: { estrelas: 3, bonus: 75 }, // Ben 10
  coringa: { estrelas: 3, bonus: 75 }, // Coringa
  dash: { estrelas: 3, bonus: 75 }, // Flecha Pêra
  rambo: { estrelas: 3, bonus: 75 }, // Rambo
  aku: { estrelas: 3, bonus: 70 }, // Aku
  geralt: { estrelas: 3, bonus: 70 }, // Geralt de Rívia
  kratos: { estrelas: 3, bonus: 70 }, // Kratos
  megumi: { estrelas: 3, bonus: 70 }, // Megumi Fushiguro
  yor: { estrelas: 3, bonus: 70 }, // Yor Forger
  yoshi: { estrelas: 3, bonus: 70 }, // Yoshi
  dovahkiin: { estrelas: 3, bonus: 65 }, // Dovahkiin
  fred: { estrelas: 3, bonus: 65 }, // Fred Jones
  gambit: { estrelas: 3, bonus: 65 }, // Gambit
  inuyasha: { estrelas: 3, bonus: 65 }, // Inuyasha
  jerry: { estrelas: 3, bonus: 65 }, // Jerry
  morty: { estrelas: 3, bonus: 65 }, // Morty Smith
  bobesponja: { estrelas: 3, bonus: 60 }, // Bob Esponja
  cloud: { estrelas: 3, bonus: 60 }, // Cloud Strife
  valak: { estrelas: 3, bonus: 60 }, // Valak
  anubis: { estrelas: 3, bonus: 55 }, // Anúbis
  cheetara: { estrelas: 3, bonus: 55 }, // Cheetara
  finn: { estrelas: 3, bonus: 55 }, // Finn
  hiei: { estrelas: 3, bonus: 55 }, // Hiei
  loid: { estrelas: 3, bonus: 55 }, // Loid Forger
  natsu: { estrelas: 3, bonus: 55 }, // Natsu Dragneel
  professorx: { estrelas: 3, bonus: 55 }, // Professor Xavier
  ryu: { estrelas: 3, bonus: 55 }, // Ryu
  ursula: { estrelas: 3, bonus: 55 }, // Úrsula
  xenomorph: { estrelas: 3, bonus: 55 }, // Xenomorfo
  agentsmith: { estrelas: 3, bonus: 50 }, // Agente Smith
  buzz: { estrelas: 3, bonus: 50 }, // Buzz Lightyear
  lelouch: { estrelas: 3, bonus: 50 }, // Lelouch
  doomslayer: { estrelas: 3, bonus: 45 }, // Doom Slayer
  erza: { estrelas: 3, bonus: 45 }, // Erza Scarlet
  lawliet: { estrelas: 3, bonus: 45 }, // L
  poisonivy: { estrelas: 3, bonus: 45 }, // Hera Venenosa
  magneto: { estrelas: 3, bonus: 35 }, // Magneto
  odin: { estrelas: 3, bonus: 35 }, // Odin
  scooby: { estrelas: 3, bonus: 35 }, // Scooby-Doo
  // ★★
  stitch: { estrelas: 2, bonus: 60 }, // Stitch
  dannyphantom: { estrelas: 2, bonus: 50 }, // Danny Phantom
  gengar: { estrelas: 2, bonus: 50 }, // Gengar
  ghostrider: { estrelas: 2, bonus: 50 }, // Motoqueiro Fantasma
  jin: { estrelas: 2, bonus: 50 }, // Jin Kazama
  michelangelo: { estrelas: 2, bonus: 50 }, // Michelangelo
  moonknight: { estrelas: 2, bonus: 50 }, // Cavaleiro da Lua
  papaleguas: { estrelas: 2, bonus: 50 }, // Papa-Léguas
  patrick: { estrelas: 2, bonus: 50 }, // Patrick Estrela
  sans: { estrelas: 2, bonus: 50 }, // Sans
  spawn: { estrelas: 2, bonus: 50 }, // Spawn
  tifa: { estrelas: 2, bonus: 50 }, // Tifa Lockhart
  blackpanther: { estrelas: 2, bonus: 45 }, // Pantera Negra
  captainmarvel: { estrelas: 2, bonus: 45 }, // Capitã Marvel
  hawkeye: { estrelas: 2, bonus: 45 }, // Gavião Arqueiro
  kronos: { estrelas: 2, bonus: 45 }, // Cronos
  nami: { estrelas: 2, bonus: 45 }, // Nami
  pantera: { estrelas: 2, bonus: 45 }, // Pantera Cor-de-Rosa
  power: { estrelas: 2, bonus: 45 }, // Power
  sailormercury: { estrelas: 2, bonus: 45 }, // Sailor Mercury
  gaara: { estrelas: 2, bonus: 40 }, // Gaara
  goku: { estrelas: 2, bonus: 40 }, // Goku
  hisoka: { estrelas: 2, bonus: 40 }, // Hisoka Morow
  mojojojo: { estrelas: 2, bonus: 40 }, // Macaco Louco
  sanji: { estrelas: 2, bonus: 40 }, // Sanji
  yusuke: { estrelas: 2, bonus: 40 }, // Yusuke Urameshi
  chunli: { estrelas: 2, bonus: 35 }, // Chun-Li
  kenshin: { estrelas: 2, bonus: 35 }, // Kenshin Himura
  luke: { estrelas: 2, bonus: 35 }, // Luke Skywalker
  mabel: { estrelas: 2, bonus: 35 }, // Mabel Pines
  masterchief: { estrelas: 2, bonus: 35 }, // Master Chief
  mickey: { estrelas: 2, bonus: 35 }, // Mickey Mouse
  samara: { estrelas: 2, bonus: 35 }, // Samara
  freddy: { estrelas: 2, bonus: 30 }, // Freddy Krueger
  iroh: { estrelas: 2, bonus: 30 }, // Iroh
  jotaro: { estrelas: 2, bonus: 30 }, // Jotaro Kujo
  saitama: { estrelas: 2, bonus: 25 }, // Saitama
  voldemort: { estrelas: 2, bonus: 25 }, // Voldemort
  jake: { estrelas: 2, bonus: 20 }, // Jake
  steven: { estrelas: 2, bonus: 15 }, // Steven Universo
  // ★
  donald: { estrelas: 1, bonus: 40 }, // Pato Donald
  invencivel: { estrelas: 1, bonus: 35 }, // Invencível
  mario: { estrelas: 1, bonus: 35 }, // Mario
  rocket: { estrelas: 1, bonus: 35 }, // Rocket Raccoon
  t800: { estrelas: 1, bonus: 35 }, // Exterminador T-800
  creeper: { estrelas: 1, bonus: 30 }, // Creeper
  deku: { estrelas: 1, bonus: 30 }, // Izuku Midoriya
  garnet: { estrelas: 1, bonus: 30 }, // Garnet
  gordon: { estrelas: 1, bonus: 30 }, // Gordon Freeman
  hellboy: { estrelas: 1, bonus: 30 }, // Hellboy
  hollowknight: { estrelas: 1, bonus: 30 }, // O Cavaleiro
  jiraiya: { estrelas: 1, bonus: 30 }, // Jiraiya
  ares: { estrelas: 1, bonus: 25 }, // Ares
  doctordoom: { estrelas: 1, bonus: 25 }, // Doutor Destino
  leon: { estrelas: 1, bonus: 25 }, // Leon S. Kennedy
  luffy: { estrelas: 1, bonus: 25 }, // Luffy
  raphael: { estrelas: 1, bonus: 25 }, // Raphael
  set: { estrelas: 1, bonus: 25 }, // Set
  zeromm: { estrelas: 1, bonus: 25 }, // Zero
  bayonetta: { estrelas: 1, bonus: 20 }, // Bayonetta
  griffith: { estrelas: 1, bonus: 20 }, // Griffith
  kenpachi: { estrelas: 1, bonus: 20 }, // Kenpachi Zaraki
  megamind: { estrelas: 1, bonus: 20 }, // Megamente
  pikachu: { estrelas: 1, bonus: 20 }, // Pikachu
  billcipher: { estrelas: 1, bonus: 15 }, // Bill Cipher
  deadpool: { estrelas: 1, bonus: 15 }, // Deadpool
  ichigo: { estrelas: 1, bonus: 15 }, // Ichigo Kurosaki
  johnnybravo: { estrelas: 1, bonus: 15 }, // Johnny Bravo
  kurama: { estrelas: 1, bonus: 15 }, // Kurama
  sailormars: { estrelas: 1, bonus: 15 }, // Sailor Mars
  zenitsu: { estrelas: 1, bonus: 15 }, // Zenitsu Agatsuma
  frieza: { estrelas: 1, bonus: 10 }, // Freeza
  mob: { estrelas: 1, bonus: 10 }, // Mob
  robocop: { estrelas: 1, bonus: 10 }, // RoboCop
  shaokahn: { estrelas: 1, bonus: 10 }, // Shao Kahn
  shera: { estrelas: 1, bonus: 10 }, // She-Ra
  sukuna: { estrelas: 1, bonus: 10 }, // Ryomen Sukuna
  ultron: { estrelas: 1, bonus: 10 }, // Ultron
  zoro: { estrelas: 1, bonus: 10 }, // Roronoa Zoro
  senku: { estrelas: 1, bonus: 5 }, // Senku
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
