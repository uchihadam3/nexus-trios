/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… personagens que façam sentido, que são da hora… mostrando a porcentagem
 * que eles somam pro trio"). Na tela, só as estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, vale só o maior bônus.
 *
 * A régua é a Sailor Moon (pedido do jogador: "eu quero que nem a Sailor Moon é"). Nas 640 mil jornadas de trios
 * sorteados (plano pontos da fábrica, scripts/fabrica/lutas.ts), quem vence as 10 lutas faz em média 1,0 milhão; com a
 * Sailor Moon no trio, 1,23 milhão (de 0,83 a 2,09 milhões). O bônus leva a média de quem vence as 10 com o
 * personagem a:
 *   ★★★  ~1,23 milhão (a Sailor Moon);
 *   ★★   ~1,15 milhão;
 *   ★    ~1,07 milhão.
 * Quem já chega lá sozinho (Sailor Moon, Orihime, Capitão Planeta…) tem 0%. Os outros personagens ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  kratos: { estrelas: 3, bonus: 40 }, // Kratos
  guts: { estrelas: 3, bonus: 35 }, // Guts
  luffy: { estrelas: 3, bonus: 35 }, // Luffy
  seiya: { estrelas: 3, bonus: 35 }, // Seiya
  coringa: { estrelas: 3, bonus: 30 }, // Coringa
  dante: { estrelas: 3, bonus: 30 }, // Dante
  darthvader: { estrelas: 3, bonus: 30 }, // Darth Vader
  godzilla: { estrelas: 3, bonus: 30 }, // Godzilla
  goku: { estrelas: 3, bonus: 30 }, // Goku
  ichigo: { estrelas: 3, bonus: 30 }, // Ichigo Kurosaki
  link: { estrelas: 3, bonus: 30 }, // Link
  masterchief: { estrelas: 3, bonus: 30 }, // Master Chief
  neo: { estrelas: 3, bonus: 30 }, // Neo
  vegeta: { estrelas: 3, bonus: 30 }, // Vegeta
  doomslayer: { estrelas: 3, bonus: 25 }, // Doom Slayer
  levi: { estrelas: 3, bonus: 25 }, // Levi Ackerman
  light: { estrelas: 3, bonus: 25 }, // Light Yagami
  naruto: { estrelas: 3, bonus: 25 }, // Naruto
  pernalonga: { estrelas: 3, bonus: 25 }, // Pernalonga
  pikachu: { estrelas: 3, bonus: 25 }, // Pikachu
  sesshomaru: { estrelas: 3, bonus: 25 }, // Sesshomaru
  sonic: { estrelas: 3, bonus: 25 }, // Sonic
  wolverine: { estrelas: 3, bonus: 25 }, // Wolverine
  deadpool: { estrelas: 3, bonus: 20 }, // Deadpool
  dio: { estrelas: 3, bonus: 20 }, // Dio Brando
  gojo: { estrelas: 3, bonus: 20 }, // Gojo
  itachi: { estrelas: 3, bonus: 20 }, // Itachi Uchiha
  jinwoo: { estrelas: 3, bonus: 20 }, // Sung Jinwoo
  johnwick: { estrelas: 3, bonus: 20 }, // John Wick
  optimus: { estrelas: 3, bonus: 20 }, // Optimus Prime
  pennywise: { estrelas: 3, bonus: 20 }, // Pennywise
  rick: { estrelas: 3, bonus: 20 }, // Rick Sanchez
  saitama: { estrelas: 3, bonus: 20 }, // Saitama
  scorpion: { estrelas: 3, bonus: 20 }, // Scorpion
  shrek: { estrelas: 3, bonus: 20 }, // Shrek
  thor: { estrelas: 3, bonus: 20 }, // Thor
  batman: { estrelas: 3, bonus: 15 }, // Batman
  sephiroth: { estrelas: 3, bonus: 15 }, // Sephiroth
  capitaoplaneta: { estrelas: 3, bonus: 0 }, // Capitão Planeta
  sailormoon: { estrelas: 3, bonus: 0 }, // Sailor Moon
  // ★★
  mario: { estrelas: 2, bonus: 30 }, // Mario
  alucardcv: { estrelas: 2, bonus: 25 }, // Alucard
  cloud: { estrelas: 2, bonus: 25 }, // Cloud Strife
  eren: { estrelas: 2, bonus: 25 }, // Eren Yeager
  geralt: { estrelas: 2, bonus: 25 }, // Geralt de Rívia
  jason: { estrelas: 2, bonus: 25 }, // Jason Voorhees
  kenshin: { estrelas: 2, bonus: 25 }, // Kenshin Himura
  malenia: { estrelas: 2, bonus: 25 }, // Malenia
  ryu: { estrelas: 2, bonus: 25 }, // Ryu
  ironman: { estrelas: 2, bonus: 20 }, // Homem de Ferro
  kakashi: { estrelas: 2, bonus: 20 }, // Kakashi Hatake
  kenpachi: { estrelas: 2, bonus: 20 }, // Kenpachi Zaraki
  t800: { estrelas: 2, bonus: 20 }, // Exterminador T-800
  zoro: { estrelas: 2, bonus: 20 }, // Roronoa Zoro
  broly: { estrelas: 2, bonus: 15 }, // Broly
  frieza: { estrelas: 2, bonus: 15 }, // Freeza
  hisoka: { estrelas: 2, bonus: 15 }, // Hisoka Morow
  killua: { estrelas: 2, bonus: 15 }, // Killua Zoldyck
  makima: { estrelas: 2, bonus: 15 }, // Makima
  sasuke: { estrelas: 2, bonus: 15 }, // Sasuke
  tuob: { estrelas: 2, bonus: 15 }, // 2B
  voldemort: { estrelas: 2, bonus: 15 }, // Voldemort
  aang: { estrelas: 2, bonus: 10 }, // Aang
  allmight: { estrelas: 2, bonus: 10 }, // All Might
  freddy: { estrelas: 2, bonus: 10 }, // Freddy Krueger
  gandalf: { estrelas: 2, bonus: 10 }, // Gandalf
  jotaro: { estrelas: 2, bonus: 10 }, // Jotaro Kujo
  lelouch: { estrelas: 2, bonus: 10 }, // Lelouch
  magneto: { estrelas: 2, bonus: 10 }, // Magneto
  predator: { estrelas: 2, bonus: 10 }, // Predador
  spiderman: { estrelas: 2, bonus: 10 }, // Homem-Aranha
  sukuna: { estrelas: 2, bonus: 10 }, // Ryomen Sukuna
  superman: { estrelas: 2, bonus: 10 }, // Superman
  wonderwoman: { estrelas: 2, bonus: 10 }, // Mulher-Maravilha
  megatron: { estrelas: 2, bonus: 5 }, // Megatron
  thanos: { estrelas: 2, bonus: 5 }, // Thanos
  yoda: { estrelas: 2, bonus: 5 }, // Yoda
  coragem: { estrelas: 2, bonus: 0 }, // Coragem, o Cão Covarde
  giorno: { estrelas: 2, bonus: 0 }, // Giorno Giovanna
  orihime: { estrelas: 2, bonus: 0 }, // Orihime Inoue
  // ★
  blackpanther: { estrelas: 1, bonus: 20 }, // Pantera Negra
  jacksparrow: { estrelas: 1, bonus: 20 }, // Jack Sparrow
  chucky: { estrelas: 1, bonus: 15 }, // Chucky
  chunli: { estrelas: 1, bonus: 15 }, // Chun-Li
  deku: { estrelas: 1, bonus: 15 }, // Izuku Midoriya
  dracula: { estrelas: 1, bonus: 15 }, // Drácula
  edward: { estrelas: 1, bonus: 15 }, // Edward Elric
  kaneki: { estrelas: 1, bonus: 15 }, // Ken Kaneki
  kazuya: { estrelas: 1, bonus: 15 }, // Kazuya Mishima
  sanji: { estrelas: 1, bonus: 15 }, // Sanji
  venom: { estrelas: 1, bonus: 15 }, // Venom
  arthurmorgan: { estrelas: 1, bonus: 10 }, // Arthur Morgan
  bayonetta: { estrelas: 1, bonus: 10 }, // Bayonetta
  erza: { estrelas: 1, bonus: 10 }, // Erza Scarlet
  gohan: { estrelas: 1, bonus: 10 }, // Gohan
  hiei: { estrelas: 1, bonus: 10 }, // Hiei
  loki: { estrelas: 1, bonus: 10 }, // Loki
  natsu: { estrelas: 1, bonus: 10 }, // Natsu Dragneel
  shredder: { estrelas: 1, bonus: 10 }, // Shredder
  subzero: { estrelas: 1, bonus: 10 }, // Sub-Zero
  tanjiro: { estrelas: 1, bonus: 10 }, // Tanjiro Kamado
  xenomorph: { estrelas: 1, bonus: 10 }, // Xenomorfo
  yuji: { estrelas: 1, bonus: 10 }, // Yuji Itadori
  byakuya: { estrelas: 1, bonus: 5 }, // Byakuya Kuchiki
  darkseid: { estrelas: 1, bonus: 5 }, // Darkseid
  elsa: { estrelas: 1, bonus: 5 }, // Elsa
  hercules: { estrelas: 1, bonus: 5 }, // Hércules
  maleficent: { estrelas: 1, bonus: 5 }, // Malévola
  minato: { estrelas: 1, bonus: 5 }, // Minato Namikaze
  scarletwitch: { estrelas: 1, bonus: 5 }, // Feiticeira Escarlate
  vergil: { estrelas: 1, bonus: 5 }, // Vergil
  wesker: { estrelas: 1, bonus: 5 }, // Albert Wesker
  zeus: { estrelas: 1, bonus: 5 }, // Zeus
  flash: { estrelas: 1, bonus: 0 }, // Flash
  greenlantern: { estrelas: 1, bonus: 0 }, // Lanterna Verde
  mewtwo: { estrelas: 1, bonus: 0 }, // Mewtwo
  raven: { estrelas: 1, bonus: 0 }, // Ravena
  samus: { estrelas: 1, bonus: 0 }, // Samus Aran
  sora: { estrelas: 1, bonus: 0 }, // Sora
  stewie: { estrelas: 1, bonus: 0 }, // Stewie Griffin
};

/** O bônus de pontos do trio (fração: 0,85 = +85%) e de quem ele vem: o maior entre os três. */
export function bonusDoTrio(trio: readonly string[]): { bonus: number; de?: string } {
  let melhor: { bonus: number; de?: string } = { bonus: 0 };
  for (const id of trio) { const e = ESTRELAS_DE_PONTOS[id]; if (e && e.bonus / 100 > melhor.bonus) melhor = { bonus: e.bonus / 100, de: id }; }
  return melhor;
}
