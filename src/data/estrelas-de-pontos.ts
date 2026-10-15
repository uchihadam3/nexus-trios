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
 * vencem as 10 lutas), arredondado para cima em 5%: ★★★ +35% a +85%, ★★ +15% a +60%, ★ +5% a +40%.
 * Depois o jogador pediu metade (o bônus já ensina o caminho; "deixa 50% só"): cada um caiu pela metade, arredondado
 * para o inteiro mais perto (,5 para cima): ★★★ +18% a +43%, ★★ +8% a +30%, ★ +3% a +20%. Os outros ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  jacksparrow: { estrelas: 3, bonus: 43 }, // Jack Sparrow
  ben10: { estrelas: 3, bonus: 38 }, // Ben 10
  coringa: { estrelas: 3, bonus: 38 }, // Coringa
  dash: { estrelas: 3, bonus: 38 }, // Flecha Pêra
  rambo: { estrelas: 3, bonus: 38 }, // Rambo
  aku: { estrelas: 3, bonus: 35 }, // Aku
  geralt: { estrelas: 3, bonus: 35 }, // Geralt de Rívia
  kratos: { estrelas: 3, bonus: 35 }, // Kratos
  megumi: { estrelas: 3, bonus: 35 }, // Megumi Fushiguro
  yor: { estrelas: 3, bonus: 35 }, // Yor Forger
  yoshi: { estrelas: 3, bonus: 35 }, // Yoshi
  dovahkiin: { estrelas: 3, bonus: 33 }, // Dovahkiin
  fred: { estrelas: 3, bonus: 33 }, // Fred Jones
  gambit: { estrelas: 3, bonus: 33 }, // Gambit
  inuyasha: { estrelas: 3, bonus: 33 }, // Inuyasha
  jerry: { estrelas: 3, bonus: 33 }, // Jerry
  morty: { estrelas: 3, bonus: 33 }, // Morty Smith
  bobesponja: { estrelas: 3, bonus: 30 }, // Bob Esponja
  cloud: { estrelas: 3, bonus: 30 }, // Cloud Strife
  valak: { estrelas: 3, bonus: 30 }, // Valak
  anubis: { estrelas: 3, bonus: 28 }, // Anúbis
  cheetara: { estrelas: 3, bonus: 28 }, // Cheetara
  finn: { estrelas: 3, bonus: 28 }, // Finn
  hiei: { estrelas: 3, bonus: 28 }, // Hiei
  loid: { estrelas: 3, bonus: 28 }, // Loid Forger
  natsu: { estrelas: 3, bonus: 28 }, // Natsu Dragneel
  professorx: { estrelas: 3, bonus: 28 }, // Professor Xavier
  ryu: { estrelas: 3, bonus: 28 }, // Ryu
  ursula: { estrelas: 3, bonus: 28 }, // Úrsula
  xenomorph: { estrelas: 3, bonus: 28 }, // Xenomorfo
  agentsmith: { estrelas: 3, bonus: 25 }, // Agente Smith
  buzz: { estrelas: 3, bonus: 25 }, // Buzz Lightyear
  lelouch: { estrelas: 3, bonus: 25 }, // Lelouch
  doomslayer: { estrelas: 3, bonus: 23 }, // Doom Slayer
  erza: { estrelas: 3, bonus: 23 }, // Erza Scarlet
  lawliet: { estrelas: 3, bonus: 23 }, // L
  poisonivy: { estrelas: 3, bonus: 23 }, // Hera Venenosa
  magneto: { estrelas: 3, bonus: 18 }, // Magneto
  odin: { estrelas: 3, bonus: 18 }, // Odin
  scooby: { estrelas: 3, bonus: 18 }, // Scooby-Doo
  // ★★
  stitch: { estrelas: 2, bonus: 30 }, // Stitch
  dannyphantom: { estrelas: 2, bonus: 25 }, // Danny Phantom
  gengar: { estrelas: 2, bonus: 25 }, // Gengar
  ghostrider: { estrelas: 2, bonus: 25 }, // Motoqueiro Fantasma
  jin: { estrelas: 2, bonus: 25 }, // Jin Kazama
  michelangelo: { estrelas: 2, bonus: 25 }, // Michelangelo
  moonknight: { estrelas: 2, bonus: 25 }, // Cavaleiro da Lua
  papaleguas: { estrelas: 2, bonus: 25 }, // Papa-Léguas
  patrick: { estrelas: 2, bonus: 25 }, // Patrick Estrela
  sans: { estrelas: 2, bonus: 25 }, // Sans
  spawn: { estrelas: 2, bonus: 25 }, // Spawn
  tifa: { estrelas: 2, bonus: 25 }, // Tifa Lockhart
  blackpanther: { estrelas: 2, bonus: 23 }, // Pantera Negra
  captainmarvel: { estrelas: 2, bonus: 23 }, // Capitã Marvel
  hawkeye: { estrelas: 2, bonus: 23 }, // Gavião Arqueiro
  kronos: { estrelas: 2, bonus: 23 }, // Cronos
  nami: { estrelas: 2, bonus: 23 }, // Nami
  pantera: { estrelas: 2, bonus: 23 }, // Pantera Cor-de-Rosa
  power: { estrelas: 2, bonus: 23 }, // Power
  sailormercury: { estrelas: 2, bonus: 23 }, // Sailor Mercury
  gaara: { estrelas: 2, bonus: 20 }, // Gaara
  goku: { estrelas: 2, bonus: 20 }, // Goku
  hisoka: { estrelas: 2, bonus: 20 }, // Hisoka Morow
  mojojojo: { estrelas: 2, bonus: 20 }, // Macaco Louco
  sanji: { estrelas: 2, bonus: 20 }, // Sanji
  yusuke: { estrelas: 2, bonus: 20 }, // Yusuke Urameshi
  chunli: { estrelas: 2, bonus: 18 }, // Chun-Li
  kenshin: { estrelas: 2, bonus: 18 }, // Kenshin Himura
  luke: { estrelas: 2, bonus: 18 }, // Luke Skywalker
  mabel: { estrelas: 2, bonus: 18 }, // Mabel Pines
  masterchief: { estrelas: 2, bonus: 18 }, // Master Chief
  mickey: { estrelas: 2, bonus: 18 }, // Mickey Mouse
  samara: { estrelas: 2, bonus: 18 }, // Samara
  freddy: { estrelas: 2, bonus: 15 }, // Freddy Krueger
  iroh: { estrelas: 2, bonus: 15 }, // Iroh
  jotaro: { estrelas: 2, bonus: 15 }, // Jotaro Kujo
  saitama: { estrelas: 2, bonus: 13 }, // Saitama
  voldemort: { estrelas: 2, bonus: 13 }, // Voldemort
  jake: { estrelas: 2, bonus: 10 }, // Jake
  steven: { estrelas: 2, bonus: 8 }, // Steven Universo
  // ★
  donald: { estrelas: 1, bonus: 20 }, // Pato Donald
  invencivel: { estrelas: 1, bonus: 18 }, // Invencível
  mario: { estrelas: 1, bonus: 18 }, // Mario
  rocket: { estrelas: 1, bonus: 18 }, // Rocket Raccoon
  t800: { estrelas: 1, bonus: 18 }, // Exterminador T-800
  creeper: { estrelas: 1, bonus: 15 }, // Creeper
  deku: { estrelas: 1, bonus: 15 }, // Izuku Midoriya
  garnet: { estrelas: 1, bonus: 15 }, // Garnet
  gordon: { estrelas: 1, bonus: 15 }, // Gordon Freeman
  hellboy: { estrelas: 1, bonus: 15 }, // Hellboy
  hollowknight: { estrelas: 1, bonus: 15 }, // O Cavaleiro
  jiraiya: { estrelas: 1, bonus: 15 }, // Jiraiya
  ares: { estrelas: 1, bonus: 13 }, // Ares
  doctordoom: { estrelas: 1, bonus: 13 }, // Doutor Destino
  leon: { estrelas: 1, bonus: 13 }, // Leon S. Kennedy
  luffy: { estrelas: 1, bonus: 13 }, // Luffy
  raphael: { estrelas: 1, bonus: 13 }, // Raphael
  set: { estrelas: 1, bonus: 13 }, // Set
  zeromm: { estrelas: 1, bonus: 13 }, // Zero
  bayonetta: { estrelas: 1, bonus: 10 }, // Bayonetta
  griffith: { estrelas: 1, bonus: 10 }, // Griffith
  kenpachi: { estrelas: 1, bonus: 10 }, // Kenpachi Zaraki
  megamind: { estrelas: 1, bonus: 10 }, // Megamente
  pikachu: { estrelas: 1, bonus: 10 }, // Pikachu
  billcipher: { estrelas: 1, bonus: 8 }, // Bill Cipher
  deadpool: { estrelas: 1, bonus: 8 }, // Deadpool
  ichigo: { estrelas: 1, bonus: 8 }, // Ichigo Kurosaki
  johnnybravo: { estrelas: 1, bonus: 8 }, // Johnny Bravo
  kurama: { estrelas: 1, bonus: 8 }, // Kurama
  sailormars: { estrelas: 1, bonus: 8 }, // Sailor Mars
  zenitsu: { estrelas: 1, bonus: 8 }, // Zenitsu Agatsuma
  frieza: { estrelas: 1, bonus: 5 }, // Freeza
  mob: { estrelas: 1, bonus: 5 }, // Mob
  robocop: { estrelas: 1, bonus: 5 }, // RoboCop
  shaokahn: { estrelas: 1, bonus: 5 }, // Shao Kahn
  shera: { estrelas: 1, bonus: 5 }, // She-Ra
  sukuna: { estrelas: 1, bonus: 5 }, // Ryomen Sukuna
  ultron: { estrelas: 1, bonus: 5 }, // Ultron
  zoro: { estrelas: 1, bonus: 5 }, // Roronoa Zoro
  senku: { estrelas: 1, bonus: 3 }, // Senku
};

/**
 * O bônus de pontos do trio (fração: 0,43 = +43%) e de quem ele vem. Conta um só: primeiro quem tem mais estrelas e,
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
