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
 * O bônus é o que falta para a média dos outros 180 (579 mil), inteiro, arredondado para o inteiro (pelo menos 1%):
 * ★★★ +18% a +42%, ★★ +12% a +18%, ★ +7% a +12% (escolha do dono: chegam à média sem passar dela, e o maior fica
 * perto dos +43% de antes).
 * Antes eram 124 com estrela, com o bônus pela meta de uma jornada muito boa (até +43%); 121 ganharam estrela, 25
 * perderam (os que ficaram mais fortes, como o Cloud Strife, ★★★ +30% → ★ +5%).
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  light: { estrelas: 3, bonus: 42 }, // Light Yagami
  kratos: { estrelas: 3, bonus: 41 }, // Kratos
  leon: { estrelas: 3, bonus: 37 }, // Leon S. Kennedy
  power: { estrelas: 3, bonus: 35 }, // Power
  ryu: { estrelas: 3, bonus: 35 }, // Ryu
  homer: { estrelas: 3, bonus: 34 }, // Homer Simpson
  jacksparrow: { estrelas: 3, bonus: 34 }, // Jack Sparrow
  vash: { estrelas: 3, bonus: 34 }, // Vash
  billcipher: { estrelas: 3, bonus: 33 }, // Bill Cipher
  patrick: { estrelas: 3, bonus: 33 }, // Patrick Estrela
  natsu: { estrelas: 3, bonus: 32 }, // Natsu Dragneel
  peter: { estrelas: 3, bonus: 32 }, // Peter Griffin
  bebop: { estrelas: 3, bonus: 31 }, // Bebop
  coringa: { estrelas: 3, bonus: 30 }, // Coringa
  stitch: { estrelas: 3, bonus: 30 }, // Stitch
  invencivel: { estrelas: 3, bonus: 29 }, // Invencível
  rambo: { estrelas: 3, bonus: 29 }, // Rambo
  gon: { estrelas: 3, bonus: 28 }, // Gon Freecss
  kaneki: { estrelas: 3, bonus: 28 }, // Ken Kaneki
  snorlax: { estrelas: 3, bonus: 28 }, // Snorlax
  tifa: { estrelas: 3, bonus: 28 }, // Tifa Lockhart
  donald: { estrelas: 3, bonus: 26 }, // Pato Donald
  inosuke: { estrelas: 3, bonus: 26 }, // Inosuke Hashibira
  jerry: { estrelas: 3, bonus: 26 }, // Jerry
  moonknight: { estrelas: 3, bonus: 26 }, // Cavaleiro da Lua
  chucky: { estrelas: 3, bonus: 25 }, // Chucky
  morty: { estrelas: 3, bonus: 25 }, // Morty Smith
  taz: { estrelas: 3, bonus: 25 }, // Taz
  arlequina: { estrelas: 3, bonus: 24 }, // Arlequina
  cuphead: { estrelas: 3, bonus: 24 }, // Cuphead
  deku: { estrelas: 3, bonus: 24 }, // Izuku Midoriya
  dipper: { estrelas: 3, bonus: 24 }, // Dipper Pines
  doomslayer: { estrelas: 3, bonus: 24 }, // Doom Slayer
  gambit: { estrelas: 3, bonus: 24 }, // Gambit
  alucardcv: { estrelas: 3, bonus: 23 }, // Alucard
  bobesponja: { estrelas: 3, bonus: 23 }, // Bob Esponja
  finn: { estrelas: 3, bonus: 23 }, // Finn
  fred: { estrelas: 3, bonus: 23 }, // Fred Jones
  marceline: { estrelas: 3, bonus: 23 }, // Marceline
  blackpanther: { estrelas: 3, bonus: 22 }, // Pantera Negra
  erza: { estrelas: 3, bonus: 22 }, // Erza Scarlet
  ghostface: { estrelas: 3, bonus: 22 }, // Ghostface
  heihachi: { estrelas: 3, bonus: 22 }, // Heihachi Mishima
  hellboy: { estrelas: 3, bonus: 22 }, // Hellboy
  kingkong: { estrelas: 3, bonus: 22 }, // King Kong
  pernalonga: { estrelas: 3, bonus: 22 }, // Pernalonga
  ares: { estrelas: 3, bonus: 21 }, // Ares
  daredevil: { estrelas: 3, bonus: 21 }, // Demolidor
  docinho: { estrelas: 3, bonus: 21 }, // Docinho
  drax: { estrelas: 3, bonus: 21 }, // Drax
  hawkeye: { estrelas: 3, bonus: 21 }, // Gavião Arqueiro
  nightwing: { estrelas: 3, bonus: 21 }, // Asa Noturna
  sailormercury: { estrelas: 3, bonus: 21 }, // Sailor Mercury
  spike: { estrelas: 3, bonus: 21 }, // Spike Spiegel
  vilgax: { estrelas: 3, bonus: 21 }, // Vilgax
  hollowknight: { estrelas: 3, bonus: 20 }, // O Cavaleiro
  lara: { estrelas: 3, bonus: 20 }, // Lara Croft
  link: { estrelas: 3, bonus: 20 }, // Link
  raphael: { estrelas: 3, bonus: 20 }, // Raphael
  sanji: { estrelas: 3, bonus: 20 }, // Sanji
  crash: { estrelas: 3, bonus: 19 }, // Crash Bandicoot
  dovahkiin: { estrelas: 3, bonus: 19 }, // Dovahkiin
  godzilla: { estrelas: 3, bonus: 19 }, // Godzilla
  jason: { estrelas: 3, bonus: 19 }, // Jason Voorhees
  odin: { estrelas: 3, bonus: 19 }, // Odin
  poisonivy: { estrelas: 3, bonus: 19 }, // Hera Venenosa
  splinter: { estrelas: 3, bonus: 19 }, // Mestre Splinter
  tom: { estrelas: 3, bonus: 19 }, // Tom
  trunks: { estrelas: 3, bonus: 19 }, // Trunks
  venom: { estrelas: 3, bonus: 19 }, // Venom
  caseyjones: { estrelas: 3, bonus: 18 }, // Casey Jones
  eren: { estrelas: 3, bonus: 18 }, // Eren Yeager
  garnet: { estrelas: 3, bonus: 18 }, // Garnet
  // ★★
  goro: { estrelas: 2, bonus: 18 }, // Goro
  jin: { estrelas: 2, bonus: 18 }, // Jin Kazama
  michaelmyers: { estrelas: 2, bonus: 18 }, // Michael Myers
  muzan: { estrelas: 2, bonus: 18 }, // Muzan Kibutsuji
  tenshinhan: { estrelas: 2, bonus: 18 }, // Tenshinhan
  yoshi: { estrelas: 2, bonus: 18 }, // Yoshi
  charizard: { estrelas: 2, bonus: 17 }, // Charizard
  deadpool: { estrelas: 2, bonus: 17 }, // Deadpool
  hisoka: { estrelas: 2, bonus: 17 }, // Hisoka Morow
  ironman: { estrelas: 2, bonus: 17 }, // Homem de Ferro
  kurapika: { estrelas: 2, bonus: 17 }, // Kurapika
  popeye: { estrelas: 2, bonus: 17 }, // Popeye
  samara: { estrelas: 2, bonus: 17 }, // Samara
  sans: { estrelas: 2, bonus: 17 }, // Sans
  scooby: { estrelas: 2, bonus: 17 }, // Scooby-Doo
  ursula: { estrelas: 2, bonus: 17 }, // Úrsula
  chunli: { estrelas: 2, bonus: 16 }, // Chun-Li
  hiei: { estrelas: 2, bonus: 16 }, // Hiei
  isaac: { estrelas: 2, bonus: 16 }, // Isaac Clarke
  johnnybravo: { estrelas: 2, bonus: 16 }, // Johnny Bravo
  rocket: { estrelas: 2, bonus: 16 }, // Rocket Raccoon
  ultron: { estrelas: 2, bonus: 16 }, // Ultron
  xenomorph: { estrelas: 2, bonus: 16 }, // Xenomorfo
  yor: { estrelas: 2, bonus: 16 }, // Yor Forger
  cartman: { estrelas: 2, bonus: 15 }, // Eric Cartman
  cheetara: { estrelas: 2, bonus: 15 }, // Cheetara
  coiote: { estrelas: 2, bonus: 15 }, // Coiote
  creeper: { estrelas: 2, bonus: 15 }, // Creeper
  dash: { estrelas: 2, bonus: 15 }, // Flecha Pêra
  freddy: { estrelas: 2, bonus: 15 }, // Freddy Krueger
  gordon: { estrelas: 2, bonus: 15 }, // Gordon Freeman
  kazuya: { estrelas: 2, bonus: 15 }, // Kazuya Mishima
  luffy: { estrelas: 2, bonus: 15 }, // Luffy
  nemesis: { estrelas: 2, bonus: 15 }, // Nemesis
  steven: { estrelas: 2, bonus: 15 }, // Steven Universo
  yusuke: { estrelas: 2, bonus: 15 }, // Yusuke Urameshi
  antman: { estrelas: 2, bonus: 14 }, // Homem-Formiga
  ezio: { estrelas: 2, bonus: 14 }, // Ezio Auditore
  gengar: { estrelas: 2, bonus: 14 }, // Gengar
  indianajones: { estrelas: 2, bonus: 14 }, // Indiana Jones
  ken: { estrelas: 2, bonus: 14 }, // Ken Masters
  kenshin: { estrelas: 2, bonus: 14 }, // Kenshin Himura
  mojojojo: { estrelas: 2, bonus: 14 }, // Macaco Louco
  mummra: { estrelas: 2, bonus: 14 }, // Mumm-Ra
  nezuko: { estrelas: 2, bonus: 14 }, // Nezuko Kamado
  saitama: { estrelas: 2, bonus: 14 }, // Saitama
  shrek: { estrelas: 2, bonus: 14 }, // Shrek
  bakugo: { estrelas: 2, bonus: 13 }, // Katsuki Bakugo
  bowser: { estrelas: 2, bonus: 13 }, // Bowser
  buzz: { estrelas: 2, bonus: 13 }, // Buzz Lightyear
  captainmarvel: { estrelas: 2, bonus: 13 }, // Capitã Marvel
  catwoman: { estrelas: 2, bonus: 13 }, // Mulher-Gato
  chopper: { estrelas: 2, bonus: 13 }, // Tony Tony Chopper
  ghostrider: { estrelas: 2, bonus: 13 }, // Motoqueiro Fantasma
  kirito: { estrelas: 2, bonus: 13 }, // Kirito
  knuckles: { estrelas: 2, bonus: 13 }, // Knuckles
  kronos: { estrelas: 2, bonus: 13 }, // Cronos
  liono: { estrelas: 2, bonus: 13 }, // Lion-O
  pantera: { estrelas: 2, bonus: 13 }, // Pantera Cor-de-Rosa
  professorx: { estrelas: 2, bonus: 13 }, // Professor Xavier
  tanjiro: { estrelas: 2, bonus: 13 }, // Tanjiro Kamado
  wolverine: { estrelas: 2, bonus: 13 }, // Wolverine
  woody: { estrelas: 2, bonus: 13 }, // Woody
  dracula: { estrelas: 2, bonus: 12 }, // Drácula
  guts: { estrelas: 2, bonus: 12 }, // Guts
  hercules: { estrelas: 2, bonus: 12 }, // Hércules
  hulk: { estrelas: 2, bonus: 12 }, // Hulk
  jiraiya: { estrelas: 2, bonus: 12 }, // Jiraiya
  majinbuu: { estrelas: 2, bonus: 12 }, // Majin Boo
  mickey: { estrelas: 2, bonus: 12 }, // Mickey Mouse
  patolino: { estrelas: 2, bonus: 12 }, // Patolino
  spawn: { estrelas: 2, bonus: 12 }, // Spawn
  subzero: { estrelas: 2, bonus: 12 }, // Sub-Zero
  // ★
  cyborg: { estrelas: 1, bonus: 12 }, // Ciborgue
  gaara: { estrelas: 1, bonus: 12 }, // Gaara
  luke: { estrelas: 1, bonus: 12 }, // Luke Skywalker
  michelangelo: { estrelas: 1, bonus: 12 }, // Michelangelo
  mrfreeze: { estrelas: 1, bonus: 12 }, // Senhor Frio
  neo: { estrelas: 1, bonus: 12 }, // Neo
  shun: { estrelas: 1, bonus: 12 }, // Shun
  artemis: { estrelas: 1, bonus: 11 }, // Ártemis
  bart: { estrelas: 1, bonus: 11 }, // Bart Simpson
  darthvader: { estrelas: 1, bonus: 11 }, // Darth Vader
  donkeykong: { estrelas: 1, bonus: 11 }, // Donkey Kong
  iroh: { estrelas: 1, bonus: 11 }, // Iroh
  johnwick: { estrelas: 1, bonus: 11 }, // John Wick
  jotaro: { estrelas: 1, bonus: 11 }, // Jotaro Kujo
  kakashi: { estrelas: 1, bonus: 11 }, // Kakashi Hatake
  marvin: { estrelas: 1, bonus: 11 }, // Marvin, o Marciano
  pateta: { estrelas: 1, bonus: 11 }, // Pateta
  plankton: { estrelas: 1, bonus: 11 }, // Plankton
  punisher: { estrelas: 1, bonus: 11 }, // Justiceiro
  sailormars: { estrelas: 1, bonus: 11 }, // Sailor Mars
  sasuke: { estrelas: 1, bonus: 11 }, // Sasuke
  sekiro: { estrelas: 1, bonus: 11 }, // Sekiro
  aku: { estrelas: 1, bonus: 10 }, // Aku
  bayonetta: { estrelas: 1, bonus: 10 }, // Bayonetta
  dante: { estrelas: 1, bonus: 10 }, // Dante
  ikki: { estrelas: 1, bonus: 10 }, // Ikki
  loid: { estrelas: 1, bonus: 10 }, // Loid Forger
  magneto: { estrelas: 1, bonus: 10 }, // Magneto
  princeofpersia: { estrelas: 1, bonus: 10 }, // Príncipe da Pérsia
  salsicha: { estrelas: 1, bonus: 10 }, // Salsicha
  seiya: { estrelas: 1, bonus: 10 }, // Seiya
  vergil: { estrelas: 1, bonus: 10 }, // Vergil
  vision: { estrelas: 1, bonus: 10 }, // Visão
  agentsmith: { estrelas: 1, bonus: 9 }, // Agente Smith
  blade: { estrelas: 1, bonus: 9 }, // Blade
  byakuya: { estrelas: 1, bonus: 9 }, // Byakuya Kuchiki
  cloud: { estrelas: 1, bonus: 9 }, // Cloud Strife
  constantine: { estrelas: 1, bonus: 9 }, // Constantine
  denji: { estrelas: 1, bonus: 9 }, // Denji
  gamora: { estrelas: 1, bonus: 9 }, // Gamora
  genos: { estrelas: 1, bonus: 9 }, // Genos
  griffith: { estrelas: 1, bonus: 9 }, // Griffith
  harrypotter: { estrelas: 1, bonus: 9 }, // Harry Potter
  ichigo: { estrelas: 1, bonus: 9 }, // Ichigo Kurosaki
  jinwoo: { estrelas: 1, bonus: 9 }, // Sung Jinwoo
  korra: { estrelas: 1, bonus: 9 }, // Korra
  luigi: { estrelas: 1, bonus: 9 }, // Luigi
  nami: { estrelas: 1, bonus: 9 }, // Nami
  piccolo: { estrelas: 1, bonus: 9 }, // Piccolo
  rukia: { estrelas: 1, bonus: 9 }, // Rukia Kuchiki
  valak: { estrelas: 1, bonus: 9 }, // Valak
  aerith: { estrelas: 1, bonus: 8 }, // Aerith
  agent47: { estrelas: 1, bonus: 8 }, // Agente 47
  dannyphantom: { estrelas: 1, bonus: 8 }, // Danny Phantom
  dio: { estrelas: 1, bonus: 8 }, // Dio Brando
  frieren: { estrelas: 1, bonus: 8 }, // Frieren
  heman: { estrelas: 1, bonus: 8 }, // He-Man
  hinata: { estrelas: 1, bonus: 8 }, // Hinata Hyuga
  jake: { estrelas: 1, bonus: 8 }, // Jake
  kirby: { estrelas: 1, bonus: 8 }, // Kirby
  lawliet: { estrelas: 1, bonus: 8 }, // L
  maleficent: { estrelas: 1, bonus: 8 }, // Malévola
  masterchief: { estrelas: 1, bonus: 8 }, // Master Chief
  megumi: { estrelas: 1, bonus: 8 }, // Megumi Fushiguro
  mulherelastica: { estrelas: 1, bonus: 8 }, // Mulher-Elástica
  shredder: { estrelas: 1, bonus: 8 }, // Shredder
  steve: { estrelas: 1, bonus: 8 }, // Steve
  t800: { estrelas: 1, bonus: 8 }, // Exterminador T-800
  voldemort: { estrelas: 1, bonus: 8 }, // Voldemort
  yennefer: { estrelas: 1, bonus: 8 }, // Yennefer
  genie: { estrelas: 1, bonus: 7 }, // Gênio
  levi: { estrelas: 1, bonus: 7 }, // Levi Ackerman
  medusa: { estrelas: 1, bonus: 7 }, // Medusa
  mewtwo: { estrelas: 1, bonus: 7 }, // Mewtwo
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
