/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… 40 que passam de 2 milhões, 40 de 1 milhão e meio a 2, 40 de 1 milhão
 * a 1 milhão e meio… personagens que façam sentido, que são da hora… mostrando a porcentagem que eles somam pro trio").
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, vale só o maior bônus. O bônus de cada um foi medido em 640 mil
 * jornadas de trios sorteados (plano pontos da fábrica, scripts/fabrica/lutas.ts) para que, com ele e dois parceiros
 * sem estrela, as 1% melhores jornadas cheguem a:
 *   ★★★  ~2,1 milhões (passa de 2 milhões em ~2% das jornadas);
 *   ★★   ~1,7 milhão  (passa de 1,5 milhão em ~4%; 2 milhões é raríssimo);
 *   ★    ~1,25 milhão (passa de 1 milhão em ~7%).
 * Quem já pontua muito (Sailor Moon, Orihime…) ganha menos; quem pontua pouco ganha mais. Os outros ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  kratos: { estrelas: 3, bonus: 125 }, // Kratos
  guts: { estrelas: 3, bonus: 120 }, // Guts
  luffy: { estrelas: 3, bonus: 110 }, // Luffy
  coringa: { estrelas: 3, bonus: 110 }, // Coringa
  masterchief: { estrelas: 3, bonus: 110 }, // Master Chief
  goku: { estrelas: 3, bonus: 105 }, // Goku
  ichigo: { estrelas: 3, bonus: 105 }, // Ichigo Kurosaki
  dante: { estrelas: 3, bonus: 105 }, // Dante
  godzilla: { estrelas: 3, bonus: 105 }, // Godzilla
  seiya: { estrelas: 3, bonus: 105 }, // Seiya
  vegeta: { estrelas: 3, bonus: 100 }, // Vegeta
  naruto: { estrelas: 3, bonus: 100 }, // Naruto
  darthvader: { estrelas: 3, bonus: 100 }, // Darth Vader
  pikachu: { estrelas: 3, bonus: 100 }, // Pikachu
  link: { estrelas: 3, bonus: 100 }, // Link
  doomslayer: { estrelas: 3, bonus: 100 }, // Doom Slayer
  neo: { estrelas: 3, bonus: 100 }, // Neo
  wolverine: { estrelas: 3, bonus: 95 }, // Wolverine
  saitama: { estrelas: 3, bonus: 95 }, // Saitama
  sonic: { estrelas: 3, bonus: 95 }, // Sonic
  sesshomaru: { estrelas: 3, bonus: 95 }, // Sesshomaru
  optimus: { estrelas: 3, bonus: 95 }, // Optimus Prime
  gojo: { estrelas: 3, bonus: 90 }, // Gojo
  thor: { estrelas: 3, bonus: 90 }, // Thor
  deadpool: { estrelas: 3, bonus: 90 }, // Deadpool
  levi: { estrelas: 3, bonus: 90 }, // Levi Ackerman
  dio: { estrelas: 3, bonus: 90 }, // Dio Brando
  pernalonga: { estrelas: 3, bonus: 90 }, // Pernalonga
  itachi: { estrelas: 3, bonus: 85 }, // Itachi Uchiha
  johnwick: { estrelas: 3, bonus: 85 }, // John Wick
  scorpion: { estrelas: 3, bonus: 85 }, // Scorpion
  jinwoo: { estrelas: 3, bonus: 85 }, // Sung Jinwoo
  light: { estrelas: 3, bonus: 85 }, // Light Yagami
  rick: { estrelas: 3, bonus: 85 }, // Rick Sanchez
  batman: { estrelas: 3, bonus: 80 }, // Batman
  sephiroth: { estrelas: 3, bonus: 80 }, // Sephiroth
  pennywise: { estrelas: 3, bonus: 80 }, // Pennywise
  shrek: { estrelas: 3, bonus: 80 }, // Shrek
  sailormoon: { estrelas: 3, bonus: 40 }, // Sailor Moon
  capitaoplaneta: { estrelas: 3, bonus: 40 }, // Capitão Planeta
  // ★★
  mario: { estrelas: 2, bonus: 80 }, // Mario
  cloud: { estrelas: 2, bonus: 75 }, // Cloud Strife
  ryu: { estrelas: 2, bonus: 75 }, // Ryu
  kenshin: { estrelas: 2, bonus: 75 }, // Kenshin Himura
  kenpachi: { estrelas: 2, bonus: 70 }, // Kenpachi Zaraki
  geralt: { estrelas: 2, bonus: 70 }, // Geralt de Rívia
  malenia: { estrelas: 2, bonus: 70 }, // Malenia
  alucardcv: { estrelas: 2, bonus: 70 }, // Alucard
  jason: { estrelas: 2, bonus: 70 }, // Jason Voorhees
  zoro: { estrelas: 2, bonus: 65 }, // Roronoa Zoro
  ironman: { estrelas: 2, bonus: 65 }, // Homem de Ferro
  t800: { estrelas: 2, bonus: 65 }, // Exterminador T-800
  frieza: { estrelas: 2, bonus: 60 }, // Freeza
  kakashi: { estrelas: 2, bonus: 60 }, // Kakashi Hatake
  eren: { estrelas: 2, bonus: 60 }, // Eren Yeager
  hisoka: { estrelas: 2, bonus: 60 }, // Hisoka Morow
  voldemort: { estrelas: 2, bonus: 60 }, // Voldemort
  broly: { estrelas: 2, bonus: 55 }, // Broly
  sasuke: { estrelas: 2, bonus: 55 }, // Sasuke
  spiderman: { estrelas: 2, bonus: 55 }, // Homem-Aranha
  tuob: { estrelas: 2, bonus: 55 }, // 2B
  killua: { estrelas: 2, bonus: 55 }, // Killua Zoldyck
  jotaro: { estrelas: 2, bonus: 55 }, // Jotaro Kujo
  aang: { estrelas: 2, bonus: 55 }, // Aang
  makima: { estrelas: 2, bonus: 55 }, // Makima
  lelouch: { estrelas: 2, bonus: 55 }, // Lelouch
  sukuna: { estrelas: 2, bonus: 50 }, // Ryomen Sukuna
  wonderwoman: { estrelas: 2, bonus: 50 }, // Mulher-Maravilha
  magneto: { estrelas: 2, bonus: 50 }, // Magneto
  predator: { estrelas: 2, bonus: 50 }, // Predador
  freddy: { estrelas: 2, bonus: 50 }, // Freddy Krueger
  superman: { estrelas: 2, bonus: 45 }, // Superman
  yoda: { estrelas: 2, bonus: 45 }, // Yoda
  megatron: { estrelas: 2, bonus: 45 }, // Megatron
  thanos: { estrelas: 2, bonus: 40 }, // Thanos
  allmight: { estrelas: 2, bonus: 40 }, // All Might
  gandalf: { estrelas: 2, bonus: 35 }, // Gandalf
  orihime: { estrelas: 2, bonus: 20 }, // Orihime Inoue
  giorno: { estrelas: 2, bonus: 15 }, // Giorno Giovanna
  coragem: { estrelas: 2, bonus: 15 }, // Coragem, o Cão Covarde
  // ★
  blackpanther: { estrelas: 1, bonus: 30 }, // Pantera Negra
  venom: { estrelas: 1, bonus: 30 }, // Venom
  jacksparrow: { estrelas: 1, bonus: 30 }, // Jack Sparrow
  erza: { estrelas: 1, bonus: 25 }, // Erza Scarlet
  deku: { estrelas: 1, bonus: 25 }, // Izuku Midoriya
  kazuya: { estrelas: 1, bonus: 25 }, // Kazuya Mishima
  chucky: { estrelas: 1, bonus: 25 }, // Chucky
  kaneki: { estrelas: 1, bonus: 25 }, // Ken Kaneki
  yuji: { estrelas: 1, bonus: 20 }, // Yuji Itadori
  sanji: { estrelas: 1, bonus: 20 }, // Sanji
  loki: { estrelas: 1, bonus: 20 }, // Loki
  natsu: { estrelas: 1, bonus: 20 }, // Natsu Dragneel
  hiei: { estrelas: 1, bonus: 20 }, // Hiei
  chunli: { estrelas: 1, bonus: 20 }, // Chun-Li
  edward: { estrelas: 1, bonus: 20 }, // Edward Elric
  dracula: { estrelas: 1, bonus: 20 }, // Drácula
  shredder: { estrelas: 1, bonus: 20 }, // Shredder
  xenomorph: { estrelas: 1, bonus: 20 }, // Xenomorfo
  gohan: { estrelas: 1, bonus: 15 }, // Gohan
  vergil: { estrelas: 1, bonus: 15 }, // Vergil
  wesker: { estrelas: 1, bonus: 15 }, // Albert Wesker
  subzero: { estrelas: 1, bonus: 15 }, // Sub-Zero
  tanjiro: { estrelas: 1, bonus: 15 }, // Tanjiro Kamado
  maleficent: { estrelas: 1, bonus: 15 }, // Malévola
  bayonetta: { estrelas: 1, bonus: 15 }, // Bayonetta
  minato: { estrelas: 1, bonus: 10 }, // Minato Namikaze
  byakuya: { estrelas: 1, bonus: 10 }, // Byakuya Kuchiki
  flash: { estrelas: 1, bonus: 10 }, // Flash
  scarletwitch: { estrelas: 1, bonus: 10 }, // Feiticeira Escarlate
  zeus: { estrelas: 1, bonus: 10 }, // Zeus
  elsa: { estrelas: 1, bonus: 10 }, // Elsa
  samus: { estrelas: 1, bonus: 10 }, // Samus Aran
  arthurmorgan: { estrelas: 1, bonus: 10 }, // Arthur Morgan
  greenlantern: { estrelas: 1, bonus: 5 }, // Lanterna Verde
  raven: { estrelas: 1, bonus: 5 }, // Ravena
  darkseid: { estrelas: 1, bonus: 5 }, // Darkseid
  mewtwo: { estrelas: 1, bonus: 5 }, // Mewtwo
  hercules: { estrelas: 1, bonus: 5 }, // Hércules
  stewie: { estrelas: 1, bonus: 5 }, // Stewie Griffin
  sora: { estrelas: 1, bonus: 5 }, // Sora
};

/** O bônus de pontos do trio (fração: 0,85 = +85%) e de quem ele vem: o maior entre os três. */
export function bonusDoTrio(trio: readonly string[]): { bonus: number; de?: string } {
  let melhor: { bonus: number; de?: string } = { bonus: 0 };
  for (const id of trio) { const e = ESTRELAS_DE_PONTOS[id]; if (e && e.bonus / 100 > melhor.bonus) melhor = { bonus: e.bonus / 100, de: id }; }
  return melhor;
}
