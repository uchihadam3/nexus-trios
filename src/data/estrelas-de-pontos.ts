/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto… mostrando a
 * porcentagem que eles somam pro trio"). Na tela, só as estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, conta um só (bonusDoTrio, abaixo).
 *
 * As estrelas vão para quem MENOS pontos faz (pedido do jogador: "seria legal se esses bônus… fossem justamente pros
 * personagens que não conseguem chegar tão fácil… senão todo mundo vai jogar com os que já são os mais fortes").
 * Medido de novo no elenco reequilibrado (buffs e debuffs, Mecânicas únicas mais fortes e a fúria do tempo), em 300.000
 * jornadas de trios sorteados, sem bônus nenhum: a média de pontos da jornada com cada personagem (~2.250 jornadas
 * cada, erro típico ±7 mil). O dono pediu mais personagens com estrela ("mais uns 100"): os 220 que menos fazem ganham
 * estrelas, em três faixas iguais (os 73 que menos fazem ★★★, os 73 seguintes ★★, os 74 seguintes ★).
 * O bônus é metade do que falta para a média dos outros 180 (579 mil), arredondado para o inteiro (pelo menos 1%):
 * ★★★ +9% a +21%, ★★ +6% a +9%, ★ +4% a +6% (o dono escolheu a metade: chegam perto da média sem passar dela).
 * Antes eram 124 com estrela, com o bônus pela meta de uma jornada muito boa (até +43%); 121 ganharam estrela, 25
 * perderam (os que ficaram mais fortes, como o Cloud Strife, ★★★ +30% → ★ +5%).
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  light: { estrelas: 3, bonus: 21 }, // Light Yagami
  kratos: { estrelas: 3, bonus: 20 }, // Kratos
  leon: { estrelas: 3, bonus: 19 }, // Leon S. Kennedy
  power: { estrelas: 3, bonus: 18 }, // Power
  ryu: { estrelas: 3, bonus: 18 }, // Ryu
  billcipher: { estrelas: 3, bonus: 17 }, // Bill Cipher
  homer: { estrelas: 3, bonus: 17 }, // Homer Simpson
  jacksparrow: { estrelas: 3, bonus: 17 }, // Jack Sparrow
  vash: { estrelas: 3, bonus: 17 }, // Vash
  bebop: { estrelas: 3, bonus: 16 }, // Bebop
  natsu: { estrelas: 3, bonus: 16 }, // Natsu Dragneel
  patrick: { estrelas: 3, bonus: 16 }, // Patrick Estrela
  peter: { estrelas: 3, bonus: 16 }, // Peter Griffin
  coringa: { estrelas: 3, bonus: 15 }, // Coringa
  invencivel: { estrelas: 3, bonus: 15 }, // Invencível
  stitch: { estrelas: 3, bonus: 15 }, // Stitch
  gon: { estrelas: 3, bonus: 14 }, // Gon Freecss
  kaneki: { estrelas: 3, bonus: 14 }, // Ken Kaneki
  rambo: { estrelas: 3, bonus: 14 }, // Rambo
  snorlax: { estrelas: 3, bonus: 14 }, // Snorlax
  tifa: { estrelas: 3, bonus: 14 }, // Tifa Lockhart
  chucky: { estrelas: 3, bonus: 13 }, // Chucky
  donald: { estrelas: 3, bonus: 13 }, // Pato Donald
  inosuke: { estrelas: 3, bonus: 13 }, // Inosuke Hashibira
  jerry: { estrelas: 3, bonus: 13 }, // Jerry
  moonknight: { estrelas: 3, bonus: 13 }, // Cavaleiro da Lua
  taz: { estrelas: 3, bonus: 13 }, // Taz
  alucardcv: { estrelas: 3, bonus: 12 }, // Alucard
  arlequina: { estrelas: 3, bonus: 12 }, // Arlequina
  bobesponja: { estrelas: 3, bonus: 12 }, // Bob Esponja
  cuphead: { estrelas: 3, bonus: 12 }, // Cuphead
  deku: { estrelas: 3, bonus: 12 }, // Izuku Midoriya
  dipper: { estrelas: 3, bonus: 12 }, // Dipper Pines
  doomslayer: { estrelas: 3, bonus: 12 }, // Doom Slayer
  finn: { estrelas: 3, bonus: 12 }, // Finn
  gambit: { estrelas: 3, bonus: 12 }, // Gambit
  morty: { estrelas: 3, bonus: 12 }, // Morty Smith
  ares: { estrelas: 3, bonus: 11 }, // Ares
  blackpanther: { estrelas: 3, bonus: 11 }, // Pantera Negra
  daredevil: { estrelas: 3, bonus: 11 }, // Demolidor
  drax: { estrelas: 3, bonus: 11 }, // Drax
  erza: { estrelas: 3, bonus: 11 }, // Erza Scarlet
  fred: { estrelas: 3, bonus: 11 }, // Fred Jones
  ghostface: { estrelas: 3, bonus: 11 }, // Ghostface
  hawkeye: { estrelas: 3, bonus: 11 }, // Gavião Arqueiro
  heihachi: { estrelas: 3, bonus: 11 }, // Heihachi Mishima
  hellboy: { estrelas: 3, bonus: 11 }, // Hellboy
  kingkong: { estrelas: 3, bonus: 11 }, // King Kong
  marceline: { estrelas: 3, bonus: 11 }, // Marceline
  pernalonga: { estrelas: 3, bonus: 11 }, // Pernalonga
  sailormercury: { estrelas: 3, bonus: 11 }, // Sailor Mercury
  vilgax: { estrelas: 3, bonus: 11 }, // Vilgax
  crash: { estrelas: 3, bonus: 10 }, // Crash Bandicoot
  docinho: { estrelas: 3, bonus: 10 }, // Docinho
  godzilla: { estrelas: 3, bonus: 10 }, // Godzilla
  hollowknight: { estrelas: 3, bonus: 10 }, // O Cavaleiro
  jason: { estrelas: 3, bonus: 10 }, // Jason Voorhees
  lara: { estrelas: 3, bonus: 10 }, // Lara Croft
  link: { estrelas: 3, bonus: 10 }, // Link
  nightwing: { estrelas: 3, bonus: 10 }, // Asa Noturna
  odin: { estrelas: 3, bonus: 10 }, // Odin
  raphael: { estrelas: 3, bonus: 10 }, // Raphael
  sanji: { estrelas: 3, bonus: 10 }, // Sanji
  spike: { estrelas: 3, bonus: 10 }, // Spike Spiegel
  venom: { estrelas: 3, bonus: 10 }, // Venom
  caseyjones: { estrelas: 3, bonus: 9 }, // Casey Jones
  dovahkiin: { estrelas: 3, bonus: 9 }, // Dovahkiin
  eren: { estrelas: 3, bonus: 9 }, // Eren Yeager
  garnet: { estrelas: 3, bonus: 9 }, // Garnet
  poisonivy: { estrelas: 3, bonus: 9 }, // Hera Venenosa
  splinter: { estrelas: 3, bonus: 9 }, // Mestre Splinter
  tom: { estrelas: 3, bonus: 9 }, // Tom
  trunks: { estrelas: 3, bonus: 9 }, // Trunks
  // ★★
  charizard: { estrelas: 2, bonus: 9 }, // Charizard
  deadpool: { estrelas: 2, bonus: 9 }, // Deadpool
  goro: { estrelas: 2, bonus: 9 }, // Goro
  hisoka: { estrelas: 2, bonus: 9 }, // Hisoka Morow
  jin: { estrelas: 2, bonus: 9 }, // Jin Kazama
  kurapika: { estrelas: 2, bonus: 9 }, // Kurapika
  michaelmyers: { estrelas: 2, bonus: 9 }, // Michael Myers
  muzan: { estrelas: 2, bonus: 9 }, // Muzan Kibutsuji
  popeye: { estrelas: 2, bonus: 9 }, // Popeye
  samara: { estrelas: 2, bonus: 9 }, // Samara
  sans: { estrelas: 2, bonus: 9 }, // Sans
  scooby: { estrelas: 2, bonus: 9 }, // Scooby-Doo
  tenshinhan: { estrelas: 2, bonus: 9 }, // Tenshinhan
  ursula: { estrelas: 2, bonus: 9 }, // Úrsula
  yoshi: { estrelas: 2, bonus: 9 }, // Yoshi
  chunli: { estrelas: 2, bonus: 8 }, // Chun-Li
  freddy: { estrelas: 2, bonus: 8 }, // Freddy Krueger
  gordon: { estrelas: 2, bonus: 8 }, // Gordon Freeman
  hiei: { estrelas: 2, bonus: 8 }, // Hiei
  ironman: { estrelas: 2, bonus: 8 }, // Homem de Ferro
  isaac: { estrelas: 2, bonus: 8 }, // Isaac Clarke
  johnnybravo: { estrelas: 2, bonus: 8 }, // Johnny Bravo
  nemesis: { estrelas: 2, bonus: 8 }, // Nemesis
  rocket: { estrelas: 2, bonus: 8 }, // Rocket Raccoon
  ultron: { estrelas: 2, bonus: 8 }, // Ultron
  xenomorph: { estrelas: 2, bonus: 8 }, // Xenomorfo
  yor: { estrelas: 2, bonus: 8 }, // Yor Forger
  antman: { estrelas: 2, bonus: 7 }, // Homem-Formiga
  bakugo: { estrelas: 2, bonus: 7 }, // Katsuki Bakugo
  bowser: { estrelas: 2, bonus: 7 }, // Bowser
  cartman: { estrelas: 2, bonus: 7 }, // Eric Cartman
  cheetara: { estrelas: 2, bonus: 7 }, // Cheetara
  chopper: { estrelas: 2, bonus: 7 }, // Tony Tony Chopper
  coiote: { estrelas: 2, bonus: 7 }, // Coiote
  creeper: { estrelas: 2, bonus: 7 }, // Creeper
  dash: { estrelas: 2, bonus: 7 }, // Flecha Pêra
  ezio: { estrelas: 2, bonus: 7 }, // Ezio Auditore
  gengar: { estrelas: 2, bonus: 7 }, // Gengar
  indianajones: { estrelas: 2, bonus: 7 }, // Indiana Jones
  kazuya: { estrelas: 2, bonus: 7 }, // Kazuya Mishima
  ken: { estrelas: 2, bonus: 7 }, // Ken Masters
  kenshin: { estrelas: 2, bonus: 7 }, // Kenshin Himura
  knuckles: { estrelas: 2, bonus: 7 }, // Knuckles
  kronos: { estrelas: 2, bonus: 7 }, // Cronos
  luffy: { estrelas: 2, bonus: 7 }, // Luffy
  mojojojo: { estrelas: 2, bonus: 7 }, // Macaco Louco
  mummra: { estrelas: 2, bonus: 7 }, // Mumm-Ra
  nezuko: { estrelas: 2, bonus: 7 }, // Nezuko Kamado
  pantera: { estrelas: 2, bonus: 7 }, // Pantera Cor-de-Rosa
  professorx: { estrelas: 2, bonus: 7 }, // Professor Xavier
  saitama: { estrelas: 2, bonus: 7 }, // Saitama
  shrek: { estrelas: 2, bonus: 7 }, // Shrek
  steven: { estrelas: 2, bonus: 7 }, // Steven Universo
  tanjiro: { estrelas: 2, bonus: 7 }, // Tanjiro Kamado
  woody: { estrelas: 2, bonus: 7 }, // Woody
  yusuke: { estrelas: 2, bonus: 7 }, // Yusuke Urameshi
  buzz: { estrelas: 2, bonus: 6 }, // Buzz Lightyear
  captainmarvel: { estrelas: 2, bonus: 6 }, // Capitã Marvel
  catwoman: { estrelas: 2, bonus: 6 }, // Mulher-Gato
  dracula: { estrelas: 2, bonus: 6 }, // Drácula
  ghostrider: { estrelas: 2, bonus: 6 }, // Motoqueiro Fantasma
  guts: { estrelas: 2, bonus: 6 }, // Guts
  hercules: { estrelas: 2, bonus: 6 }, // Hércules
  hulk: { estrelas: 2, bonus: 6 }, // Hulk
  jiraiya: { estrelas: 2, bonus: 6 }, // Jiraiya
  kirito: { estrelas: 2, bonus: 6 }, // Kirito
  liono: { estrelas: 2, bonus: 6 }, // Lion-O
  majinbuu: { estrelas: 2, bonus: 6 }, // Majin Boo
  mickey: { estrelas: 2, bonus: 6 }, // Mickey Mouse
  patolino: { estrelas: 2, bonus: 6 }, // Patolino
  spawn: { estrelas: 2, bonus: 6 }, // Spawn
  subzero: { estrelas: 2, bonus: 6 }, // Sub-Zero
  wolverine: { estrelas: 2, bonus: 6 }, // Wolverine
  // ★
  bart: { estrelas: 1, bonus: 6 }, // Bart Simpson
  cyborg: { estrelas: 1, bonus: 6 }, // Ciborgue
  gaara: { estrelas: 1, bonus: 6 }, // Gaara
  iroh: { estrelas: 1, bonus: 6 }, // Iroh
  luke: { estrelas: 1, bonus: 6 }, // Luke Skywalker
  michelangelo: { estrelas: 1, bonus: 6 }, // Michelangelo
  mrfreeze: { estrelas: 1, bonus: 6 }, // Senhor Frio
  neo: { estrelas: 1, bonus: 6 }, // Neo
  pateta: { estrelas: 1, bonus: 6 }, // Pateta
  punisher: { estrelas: 1, bonus: 6 }, // Justiceiro
  sailormars: { estrelas: 1, bonus: 6 }, // Sailor Mars
  shun: { estrelas: 1, bonus: 6 }, // Shun
  agentsmith: { estrelas: 1, bonus: 5 }, // Agente Smith
  aku: { estrelas: 1, bonus: 5 }, // Aku
  artemis: { estrelas: 1, bonus: 5 }, // Ártemis
  bayonetta: { estrelas: 1, bonus: 5 }, // Bayonetta
  cloud: { estrelas: 1, bonus: 5 }, // Cloud Strife
  constantine: { estrelas: 1, bonus: 5 }, // Constantine
  dante: { estrelas: 1, bonus: 5 }, // Dante
  darthvader: { estrelas: 1, bonus: 5 }, // Darth Vader
  denji: { estrelas: 1, bonus: 5 }, // Denji
  donkeykong: { estrelas: 1, bonus: 5 }, // Donkey Kong
  genos: { estrelas: 1, bonus: 5 }, // Genos
  ichigo: { estrelas: 1, bonus: 5 }, // Ichigo Kurosaki
  ikki: { estrelas: 1, bonus: 5 }, // Ikki
  johnwick: { estrelas: 1, bonus: 5 }, // John Wick
  jotaro: { estrelas: 1, bonus: 5 }, // Jotaro Kujo
  kakashi: { estrelas: 1, bonus: 5 }, // Kakashi Hatake
  korra: { estrelas: 1, bonus: 5 }, // Korra
  loid: { estrelas: 1, bonus: 5 }, // Loid Forger
  magneto: { estrelas: 1, bonus: 5 }, // Magneto
  marvin: { estrelas: 1, bonus: 5 }, // Marvin, o Marciano
  piccolo: { estrelas: 1, bonus: 5 }, // Piccolo
  plankton: { estrelas: 1, bonus: 5 }, // Plankton
  princeofpersia: { estrelas: 1, bonus: 5 }, // Príncipe da Pérsia
  rukia: { estrelas: 1, bonus: 5 }, // Rukia Kuchiki
  salsicha: { estrelas: 1, bonus: 5 }, // Salsicha
  sasuke: { estrelas: 1, bonus: 5 }, // Sasuke
  seiya: { estrelas: 1, bonus: 5 }, // Seiya
  sekiro: { estrelas: 1, bonus: 5 }, // Sekiro
  valak: { estrelas: 1, bonus: 5 }, // Valak
  vergil: { estrelas: 1, bonus: 5 }, // Vergil
  vision: { estrelas: 1, bonus: 5 }, // Visão
  aerith: { estrelas: 1, bonus: 4 }, // Aerith
  agent47: { estrelas: 1, bonus: 4 }, // Agente 47
  blade: { estrelas: 1, bonus: 4 }, // Blade
  byakuya: { estrelas: 1, bonus: 4 }, // Byakuya Kuchiki
  dannyphantom: { estrelas: 1, bonus: 4 }, // Danny Phantom
  dio: { estrelas: 1, bonus: 4 }, // Dio Brando
  frieren: { estrelas: 1, bonus: 4 }, // Frieren
  gamora: { estrelas: 1, bonus: 4 }, // Gamora
  genie: { estrelas: 1, bonus: 4 }, // Gênio
  griffith: { estrelas: 1, bonus: 4 }, // Griffith
  harrypotter: { estrelas: 1, bonus: 4 }, // Harry Potter
  heman: { estrelas: 1, bonus: 4 }, // He-Man
  hinata: { estrelas: 1, bonus: 4 }, // Hinata Hyuga
  jake: { estrelas: 1, bonus: 4 }, // Jake
  jinwoo: { estrelas: 1, bonus: 4 }, // Sung Jinwoo
  kirby: { estrelas: 1, bonus: 4 }, // Kirby
  lawliet: { estrelas: 1, bonus: 4 }, // L
  levi: { estrelas: 1, bonus: 4 }, // Levi Ackerman
  luigi: { estrelas: 1, bonus: 4 }, // Luigi
  maleficent: { estrelas: 1, bonus: 4 }, // Malévola
  masterchief: { estrelas: 1, bonus: 4 }, // Master Chief
  medusa: { estrelas: 1, bonus: 4 }, // Medusa
  megumi: { estrelas: 1, bonus: 4 }, // Megumi Fushiguro
  mewtwo: { estrelas: 1, bonus: 4 }, // Mewtwo
  mulherelastica: { estrelas: 1, bonus: 4 }, // Mulher-Elástica
  nami: { estrelas: 1, bonus: 4 }, // Nami
  shredder: { estrelas: 1, bonus: 4 }, // Shredder
  steve: { estrelas: 1, bonus: 4 }, // Steve
  t800: { estrelas: 1, bonus: 4 }, // Exterminador T-800
  voldemort: { estrelas: 1, bonus: 4 }, // Voldemort
  yennefer: { estrelas: 1, bonus: 4 }, // Yennefer
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
