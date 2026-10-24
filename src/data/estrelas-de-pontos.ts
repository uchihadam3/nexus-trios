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
 * O bônus sai do que falta para a média dos outros 180 (579 mil), na mesma proporção para todos, com o maior em +75%
 * (pedido do dono: "antes as estrelas iam até 43… coloca até uns 75, pra garantir"): cada um ganha 1,79 vez o que lhe
 * falta, arredondado para o inteiro: ★★★ +33% a +75%, ★★ +21% a +32%, ★ +13% a +21%. Assim quem tem estrela passa da
 * média (o Light Yagami, 408 mil sem bônus, vai a ~714 mil, perto do Hades, o que mais faz: 699 mil).
 * Antes eram 124 com estrela, com o bônus pela meta de uma jornada muito boa (até +43%); 121 ganharam estrela, 25
 * perderam (os que ficaram mais fortes, como o Cloud Strife, ★★★ +30% → ★ +5%).
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  light: { estrelas: 3, bonus: 75 }, // Light Yagami
  kratos: { estrelas: 3, bonus: 73 }, // Kratos
  leon: { estrelas: 3, bonus: 66 }, // Leon S. Kennedy
  power: { estrelas: 3, bonus: 63 }, // Power
  ryu: { estrelas: 3, bonus: 63 }, // Ryu
  homer: { estrelas: 3, bonus: 62 }, // Homer Simpson
  vash: { estrelas: 3, bonus: 62 }, // Vash
  jacksparrow: { estrelas: 3, bonus: 61 }, // Jack Sparrow
  billcipher: { estrelas: 3, bonus: 59 }, // Bill Cipher
  patrick: { estrelas: 3, bonus: 58 }, // Patrick Estrela
  peter: { estrelas: 3, bonus: 58 }, // Peter Griffin
  natsu: { estrelas: 3, bonus: 57 }, // Natsu Dragneel
  bebop: { estrelas: 3, bonus: 56 }, // Bebop
  stitch: { estrelas: 3, bonus: 54 }, // Stitch
  coringa: { estrelas: 3, bonus: 53 }, // Coringa
  invencivel: { estrelas: 3, bonus: 52 }, // Invencível
  gon: { estrelas: 3, bonus: 51 }, // Gon Freecss
  kaneki: { estrelas: 3, bonus: 51 }, // Ken Kaneki
  rambo: { estrelas: 3, bonus: 51 }, // Rambo
  snorlax: { estrelas: 3, bonus: 51 }, // Snorlax
  tifa: { estrelas: 3, bonus: 49 }, // Tifa Lockhart
  inosuke: { estrelas: 3, bonus: 47 }, // Inosuke Hashibira
  jerry: { estrelas: 3, bonus: 47 }, // Jerry
  moonknight: { estrelas: 3, bonus: 47 }, // Cavaleiro da Lua
  donald: { estrelas: 3, bonus: 46 }, // Pato Donald
  chucky: { estrelas: 3, bonus: 45 }, // Chucky
  taz: { estrelas: 3, bonus: 45 }, // Taz
  cuphead: { estrelas: 3, bonus: 44 }, // Cuphead
  deku: { estrelas: 3, bonus: 44 }, // Izuku Midoriya
  dipper: { estrelas: 3, bonus: 44 }, // Dipper Pines
  morty: { estrelas: 3, bonus: 44 }, // Morty Smith
  arlequina: { estrelas: 3, bonus: 43 }, // Arlequina
  doomslayer: { estrelas: 3, bonus: 43 }, // Doom Slayer
  gambit: { estrelas: 3, bonus: 43 }, // Gambit
  bobesponja: { estrelas: 3, bonus: 42 }, // Bob Esponja
  finn: { estrelas: 3, bonus: 42 }, // Finn
  alucardcv: { estrelas: 3, bonus: 41 }, // Alucard
  fred: { estrelas: 3, bonus: 41 }, // Fred Jones
  marceline: { estrelas: 3, bonus: 41 }, // Marceline
  blackpanther: { estrelas: 3, bonus: 40 }, // Pantera Negra
  hellboy: { estrelas: 3, bonus: 40 }, // Hellboy
  erza: { estrelas: 3, bonus: 39 }, // Erza Scarlet
  ghostface: { estrelas: 3, bonus: 39 }, // Ghostface
  heihachi: { estrelas: 3, bonus: 39 }, // Heihachi Mishima
  kingkong: { estrelas: 3, bonus: 39 }, // King Kong
  pernalonga: { estrelas: 3, bonus: 39 }, // Pernalonga
  ares: { estrelas: 3, bonus: 38 }, // Ares
  daredevil: { estrelas: 3, bonus: 38 }, // Demolidor
  drax: { estrelas: 3, bonus: 38 }, // Drax
  hawkeye: { estrelas: 3, bonus: 38 }, // Gavião Arqueiro
  sailormercury: { estrelas: 3, bonus: 38 }, // Sailor Mercury
  vilgax: { estrelas: 3, bonus: 38 }, // Vilgax
  docinho: { estrelas: 3, bonus: 37 }, // Docinho
  nightwing: { estrelas: 3, bonus: 37 }, // Asa Noturna
  spike: { estrelas: 3, bonus: 37 }, // Spike Spiegel
  hollowknight: { estrelas: 3, bonus: 36 }, // O Cavaleiro
  link: { estrelas: 3, bonus: 36 }, // Link
  raphael: { estrelas: 3, bonus: 36 }, // Raphael
  crash: { estrelas: 3, bonus: 35 }, // Crash Bandicoot
  jason: { estrelas: 3, bonus: 35 }, // Jason Voorhees
  lara: { estrelas: 3, bonus: 35 }, // Lara Croft
  odin: { estrelas: 3, bonus: 35 }, // Odin
  sanji: { estrelas: 3, bonus: 35 }, // Sanji
  godzilla: { estrelas: 3, bonus: 34 }, // Godzilla
  trunks: { estrelas: 3, bonus: 34 }, // Trunks
  venom: { estrelas: 3, bonus: 34 }, // Venom
  caseyjones: { estrelas: 3, bonus: 33 }, // Casey Jones
  dovahkiin: { estrelas: 3, bonus: 33 }, // Dovahkiin
  eren: { estrelas: 3, bonus: 33 }, // Eren Yeager
  garnet: { estrelas: 3, bonus: 33 }, // Garnet
  poisonivy: { estrelas: 3, bonus: 33 }, // Hera Venenosa
  splinter: { estrelas: 3, bonus: 33 }, // Mestre Splinter
  tom: { estrelas: 3, bonus: 33 }, // Tom
  // ★★
  goro: { estrelas: 2, bonus: 32 }, // Goro
  jin: { estrelas: 2, bonus: 32 }, // Jin Kazama
  muzan: { estrelas: 2, bonus: 32 }, // Muzan Kibutsuji
  tenshinhan: { estrelas: 2, bonus: 32 }, // Tenshinhan
  yoshi: { estrelas: 2, bonus: 32 }, // Yoshi
  charizard: { estrelas: 2, bonus: 31 }, // Charizard
  deadpool: { estrelas: 2, bonus: 31 }, // Deadpool
  hisoka: { estrelas: 2, bonus: 31 }, // Hisoka Morow
  kurapika: { estrelas: 2, bonus: 31 }, // Kurapika
  michaelmyers: { estrelas: 2, bonus: 31 }, // Michael Myers
  samara: { estrelas: 2, bonus: 31 }, // Samara
  sans: { estrelas: 2, bonus: 31 }, // Sans
  scooby: { estrelas: 2, bonus: 31 }, // Scooby-Doo
  ursula: { estrelas: 2, bonus: 31 }, // Úrsula
  ironman: { estrelas: 2, bonus: 30 }, // Homem de Ferro
  popeye: { estrelas: 2, bonus: 30 }, // Popeye
  johnnybravo: { estrelas: 2, bonus: 29 }, // Johnny Bravo
  ultron: { estrelas: 2, bonus: 29 }, // Ultron
  xenomorph: { estrelas: 2, bonus: 29 }, // Xenomorfo
  chunli: { estrelas: 2, bonus: 28 }, // Chun-Li
  hiei: { estrelas: 2, bonus: 28 }, // Hiei
  isaac: { estrelas: 2, bonus: 28 }, // Isaac Clarke
  rocket: { estrelas: 2, bonus: 28 }, // Rocket Raccoon
  yor: { estrelas: 2, bonus: 28 }, // Yor Forger
  cartman: { estrelas: 2, bonus: 27 }, // Eric Cartman
  cheetara: { estrelas: 2, bonus: 27 }, // Cheetara
  freddy: { estrelas: 2, bonus: 27 }, // Freddy Krueger
  gordon: { estrelas: 2, bonus: 27 }, // Gordon Freeman
  kazuya: { estrelas: 2, bonus: 27 }, // Kazuya Mishima
  nemesis: { estrelas: 2, bonus: 27 }, // Nemesis
  steven: { estrelas: 2, bonus: 27 }, // Steven Universo
  antman: { estrelas: 2, bonus: 26 }, // Homem-Formiga
  coiote: { estrelas: 2, bonus: 26 }, // Coiote
  creeper: { estrelas: 2, bonus: 26 }, // Creeper
  dash: { estrelas: 2, bonus: 26 }, // Flecha Pêra
  ken: { estrelas: 2, bonus: 26 }, // Ken Masters
  luffy: { estrelas: 2, bonus: 26 }, // Luffy
  yusuke: { estrelas: 2, bonus: 26 }, // Yusuke Urameshi
  gengar: { estrelas: 2, bonus: 25 }, // Gengar
  indianajones: { estrelas: 2, bonus: 25 }, // Indiana Jones
  kenshin: { estrelas: 2, bonus: 25 }, // Kenshin Himura
  mummra: { estrelas: 2, bonus: 25 }, // Mumm-Ra
  saitama: { estrelas: 2, bonus: 25 }, // Saitama
  shrek: { estrelas: 2, bonus: 25 }, // Shrek
  bakugo: { estrelas: 2, bonus: 24 }, // Katsuki Bakugo
  bowser: { estrelas: 2, bonus: 24 }, // Bowser
  ezio: { estrelas: 2, bonus: 24 }, // Ezio Auditore
  knuckles: { estrelas: 2, bonus: 24 }, // Knuckles
  kronos: { estrelas: 2, bonus: 24 }, // Cronos
  mojojojo: { estrelas: 2, bonus: 24 }, // Macaco Louco
  nezuko: { estrelas: 2, bonus: 24 }, // Nezuko Kamado
  tanjiro: { estrelas: 2, bonus: 24 }, // Tanjiro Kamado
  woody: { estrelas: 2, bonus: 24 }, // Woody
  buzz: { estrelas: 2, bonus: 23 }, // Buzz Lightyear
  captainmarvel: { estrelas: 2, bonus: 23 }, // Capitã Marvel
  catwoman: { estrelas: 2, bonus: 23 }, // Mulher-Gato
  chopper: { estrelas: 2, bonus: 23 }, // Tony Tony Chopper
  ghostrider: { estrelas: 2, bonus: 23 }, // Motoqueiro Fantasma
  kirito: { estrelas: 2, bonus: 23 }, // Kirito
  liono: { estrelas: 2, bonus: 23 }, // Lion-O
  pantera: { estrelas: 2, bonus: 23 }, // Pantera Cor-de-Rosa
  professorx: { estrelas: 2, bonus: 23 }, // Professor Xavier
  wolverine: { estrelas: 2, bonus: 23 }, // Wolverine
  dracula: { estrelas: 2, bonus: 22 }, // Drácula
  guts: { estrelas: 2, bonus: 22 }, // Guts
  hercules: { estrelas: 2, bonus: 22 }, // Hércules
  jiraiya: { estrelas: 2, bonus: 22 }, // Jiraiya
  majinbuu: { estrelas: 2, bonus: 22 }, // Majin Boo
  patolino: { estrelas: 2, bonus: 22 }, // Patolino
  spawn: { estrelas: 2, bonus: 22 }, // Spawn
  hulk: { estrelas: 2, bonus: 21 }, // Hulk
  mickey: { estrelas: 2, bonus: 21 }, // Mickey Mouse
  subzero: { estrelas: 2, bonus: 21 }, // Sub-Zero
  // ★
  cyborg: { estrelas: 1, bonus: 21 }, // Ciborgue
  gaara: { estrelas: 1, bonus: 21 }, // Gaara
  luke: { estrelas: 1, bonus: 21 }, // Luke Skywalker
  michelangelo: { estrelas: 1, bonus: 21 }, // Michelangelo
  mrfreeze: { estrelas: 1, bonus: 21 }, // Senhor Frio
  neo: { estrelas: 1, bonus: 21 }, // Neo
  shun: { estrelas: 1, bonus: 21 }, // Shun
  artemis: { estrelas: 1, bonus: 20 }, // Ártemis
  bart: { estrelas: 1, bonus: 20 }, // Bart Simpson
  iroh: { estrelas: 1, bonus: 20 }, // Iroh
  johnwick: { estrelas: 1, bonus: 20 }, // John Wick
  pateta: { estrelas: 1, bonus: 20 }, // Pateta
  plankton: { estrelas: 1, bonus: 20 }, // Plankton
  punisher: { estrelas: 1, bonus: 20 }, // Justiceiro
  sailormars: { estrelas: 1, bonus: 20 }, // Sailor Mars
  darthvader: { estrelas: 1, bonus: 19 }, // Darth Vader
  donkeykong: { estrelas: 1, bonus: 19 }, // Donkey Kong
  jotaro: { estrelas: 1, bonus: 19 }, // Jotaro Kujo
  kakashi: { estrelas: 1, bonus: 19 }, // Kakashi Hatake
  marvin: { estrelas: 1, bonus: 19 }, // Marvin, o Marciano
  sasuke: { estrelas: 1, bonus: 19 }, // Sasuke
  sekiro: { estrelas: 1, bonus: 19 }, // Sekiro
  aku: { estrelas: 1, bonus: 18 }, // Aku
  bayonetta: { estrelas: 1, bonus: 18 }, // Bayonetta
  dante: { estrelas: 1, bonus: 18 }, // Dante
  salsicha: { estrelas: 1, bonus: 18 }, // Salsicha
  vergil: { estrelas: 1, bonus: 18 }, // Vergil
  constantine: { estrelas: 1, bonus: 17 }, // Constantine
  ichigo: { estrelas: 1, bonus: 17 }, // Ichigo Kurosaki
  ikki: { estrelas: 1, bonus: 17 }, // Ikki
  korra: { estrelas: 1, bonus: 17 }, // Korra
  loid: { estrelas: 1, bonus: 17 }, // Loid Forger
  magneto: { estrelas: 1, bonus: 17 }, // Magneto
  piccolo: { estrelas: 1, bonus: 17 }, // Piccolo
  princeofpersia: { estrelas: 1, bonus: 17 }, // Príncipe da Pérsia
  rukia: { estrelas: 1, bonus: 17 }, // Rukia Kuchiki
  seiya: { estrelas: 1, bonus: 17 }, // Seiya
  valak: { estrelas: 1, bonus: 17 }, // Valak
  vision: { estrelas: 1, bonus: 17 }, // Visão
  agentsmith: { estrelas: 1, bonus: 16 }, // Agente Smith
  blade: { estrelas: 1, bonus: 16 }, // Blade
  cloud: { estrelas: 1, bonus: 16 }, // Cloud Strife
  denji: { estrelas: 1, bonus: 16 }, // Denji
  genos: { estrelas: 1, bonus: 16 }, // Genos
  griffith: { estrelas: 1, bonus: 16 }, // Griffith
  harrypotter: { estrelas: 1, bonus: 16 }, // Harry Potter
  jinwoo: { estrelas: 1, bonus: 16 }, // Sung Jinwoo
  aerith: { estrelas: 1, bonus: 15 }, // Aerith
  agent47: { estrelas: 1, bonus: 15 }, // Agente 47
  byakuya: { estrelas: 1, bonus: 15 }, // Byakuya Kuchiki
  dannyphantom: { estrelas: 1, bonus: 15 }, // Danny Phantom
  dio: { estrelas: 1, bonus: 15 }, // Dio Brando
  frieren: { estrelas: 1, bonus: 15 }, // Frieren
  gamora: { estrelas: 1, bonus: 15 }, // Gamora
  hinata: { estrelas: 1, bonus: 15 }, // Hinata Hyuga
  kirby: { estrelas: 1, bonus: 15 }, // Kirby
  luigi: { estrelas: 1, bonus: 15 }, // Luigi
  maleficent: { estrelas: 1, bonus: 15 }, // Malévola
  megumi: { estrelas: 1, bonus: 15 }, // Megumi Fushiguro
  mulherelastica: { estrelas: 1, bonus: 15 }, // Mulher-Elástica
  nami: { estrelas: 1, bonus: 15 }, // Nami
  voldemort: { estrelas: 1, bonus: 15 }, // Voldemort
  heman: { estrelas: 1, bonus: 14 }, // He-Man
  jake: { estrelas: 1, bonus: 14 }, // Jake
  lawliet: { estrelas: 1, bonus: 14 }, // L
  masterchief: { estrelas: 1, bonus: 14 }, // Master Chief
  shredder: { estrelas: 1, bonus: 14 }, // Shredder
  steve: { estrelas: 1, bonus: 14 }, // Steve
  t800: { estrelas: 1, bonus: 14 }, // Exterminador T-800
  yennefer: { estrelas: 1, bonus: 14 }, // Yennefer
  genie: { estrelas: 1, bonus: 13 }, // Gênio
  levi: { estrelas: 1, bonus: 13 }, // Levi Ackerman
  medusa: { estrelas: 1, bonus: 13 }, // Medusa
  mewtwo: { estrelas: 1, bonus: 13 }, // Mewtwo
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
