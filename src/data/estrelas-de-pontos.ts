/*
 * As estrelas dos pontos (pedido do jogador: "a gente tem alguns personagens que fazem mais ponto. Então, se você tem
 * ele no time, você acaba fazendo mais ponto… mostrando a porcentagem que eles somam pro trio"). Na tela, só as
 * estrelas e a porcentagem.
 *
 * Só os pontos: a luta e a força de todo mundo ficam iguais. Ter um deles no trio soma `bonus`% aos pontos de cada
 * luta (src/engine/pontos.ts); com mais de um no trio, conta um só (bonusDoTrio, abaixo).
 *
 * Medido em 2,64 milhões de jornadas de trios sorteados, sem bônus (plano pontos da fábrica, scripts/fabrica/lutas.ts):
 * o que cada personagem faz numa jornada muito boa (as 1% melhores das que vencem as 10 lutas). Os personagens vão
 * para as estrelas na ordem do que já fazem (pedido do jogador: "os personagens que já são maiores… no três estrelas…
 * depois os outros 40 maiores… pra não ficar tão longe a diferença um do outro na mesma estrela"): os 40 que mais
 * fazem são ★★★, os 40 seguintes ★★, os 40 seguintes ★, com no máximo 3 do mesmo universo (src/data/equipes.ts)
 * em cada nível. Cada nível tem uma meta, e quem não chega ganha o que falta (arredondado para cima, em 5%):
 *   ★★★  2 milhões   (os 40 fazem de 1,48 a 1,89 milhão: +10% a +35%);
 *   ★★   1,75 milhão (de 1,40 a 1,49 milhão: +20% a +25%);
 *   ★    1,5 milhão  (de 1,36 a 1,43 milhão: +5% a +15%).
 * Um personagem típico faz 1,29 milhão. Os outros personagens ficam iguais.
 */
export interface EstrelaDePontos { estrelas: 1 | 2 | 3; bonus: number }

export const ESTRELAS_DE_PONTOS: Record<string, EstrelaDePontos> = {
  // ★★★
  aizen: { estrelas: 3, bonus: 35 }, // Sosuke Aizen
  galactus: { estrelas: 3, bonus: 35 }, // Galactus
  ganondorf: { estrelas: 3, bonus: 35 }, // Ganondorf
  hadescz: { estrelas: 3, bonus: 35 }, // Hades
  magneto: { estrelas: 3, bonus: 35 }, // Magneto
  optimus: { estrelas: 3, bonus: 35 }, // Optimus Prime
  scooby: { estrelas: 3, bonus: 35 }, // Scooby-Doo
  senku: { estrelas: 3, bonus: 35 }, // Senku
  wonderwoman: { estrelas: 3, bonus: 35 }, // Mulher-Maravilha
  groot: { estrelas: 3, bonus: 30 }, // Groot
  sakura: { estrelas: 3, bonus: 30 }, // Sakura Haruno
  shaka: { estrelas: 3, bonus: 30 }, // Shaka de Virgem
  steven: { estrelas: 3, bonus: 30 }, // Steven Universo
  aphrodite: { estrelas: 3, bonus: 25 }, // Afrodite
  captain: { estrelas: 3, bonus: 25 }, // Capitão América
  gandalf: { estrelas: 3, bonus: 25 }, // Gandalf
  katara: { estrelas: 3, bonus: 25 }, // Katara
  leorio: { estrelas: 3, bonus: 25 }, // Leorio
  mulherelastica: { estrelas: 3, bonus: 25 }, // Mulher-Elástica
  odin: { estrelas: 3, bonus: 25 }, // Odin
  peach: { estrelas: 3, bonus: 25 }, // Princesa Peach
  raven: { estrelas: 3, bonus: 25 }, // Ravena
  rem: { estrelas: 3, bonus: 25 }, // Rem
  strange: { estrelas: 3, bonus: 25 }, // Doutor Estranho
  thanos: { estrelas: 3, bonus: 25 }, // Thanos
  apollo: { estrelas: 3, bonus: 20 }, // Apolo
  chopper: { estrelas: 3, bonus: 20 }, // Tony Tony Chopper
  cosmowanda: { estrelas: 3, bonus: 20 }, // Cosmo e Wanda
  jeangrey: { estrelas: 3, bonus: 20 }, // Jean Grey
  tsunade: { estrelas: 3, bonus: 20 }, // Tsunade
  capitaoplaneta: { estrelas: 3, bonus: 15 }, // Capitão Planeta
  giorno: { estrelas: 3, bonus: 15 }, // Giorno Giovanna
  jill: { estrelas: 3, bonus: 15 }, // Jill Valentine
  orihime: { estrelas: 3, bonus: 15 }, // Orihime Inoue
  sora: { estrelas: 3, bonus: 15 }, // Sora
  aerith: { estrelas: 3, bonus: 10 }, // Aerith
  alphonse: { estrelas: 3, bonus: 10 }, // Alphonse Elric
  coragem: { estrelas: 3, bonus: 10 }, // Coragem, o Cão Covarde
  isis: { estrelas: 3, bonus: 10 }, // Ísis
  sailormoon: { estrelas: 3, bonus: 10 }, // Sailor Moon
  // ★★
  aang: { estrelas: 2, bonus: 25 }, // Aang
  allmight: { estrelas: 2, bonus: 25 }, // All Might
  arthas: { estrelas: 2, bonus: 25 }, // Arthas
  batman: { estrelas: 2, bonus: 25 }, // Batman
  cyborg: { estrelas: 2, bonus: 25 }, // Ciborgue
  doomslayer: { estrelas: 2, bonus: 25 }, // Doom Slayer
  frieza: { estrelas: 2, bonus: 25 }, // Freeza
  genie: { estrelas: 2, bonus: 25 }, // Gênio
  gojo: { estrelas: 2, bonus: 25 }, // Gojo
  hulk: { estrelas: 2, bonus: 25 }, // Hulk
  iroh: { estrelas: 2, bonus: 25 }, // Iroh
  lawliet: { estrelas: 2, bonus: 25 }, // L
  poisonivy: { estrelas: 2, bonus: 25 }, // Hera Venenosa
  robocop: { estrelas: 2, bonus: 25 }, // RoboCop
  saitama: { estrelas: 2, bonus: 25 }, // Saitama
  sasuke: { estrelas: 2, bonus: 25 }, // Sasuke
  scarletwitch: { estrelas: 2, bonus: 25 }, // Feiticeira Escarlate
  shaokahn: { estrelas: 2, bonus: 25 }, // Shao Kahn
  sukuna: { estrelas: 2, bonus: 25 }, // Ryomen Sukuna
  superman: { estrelas: 2, bonus: 25 }, // Superman
  thor: { estrelas: 2, bonus: 25 }, // Thor
  toph: { estrelas: 2, bonus: 25 }, // Toph
  violet: { estrelas: 2, bonus: 25 }, // Violeta Pêra
  voldemort: { estrelas: 2, bonus: 25 }, // Voldemort
  zeus: { estrelas: 2, bonus: 25 }, // Zeus
  anya: { estrelas: 2, bonus: 20 }, // Anya Forger
  athena: { estrelas: 2, bonus: 20 }, // Atena
  cartman: { estrelas: 2, bonus: 20 }, // Eric Cartman
  greenlantern: { estrelas: 2, bonus: 20 }, // Lanterna Verde
  hercules: { estrelas: 2, bonus: 20 }, // Hércules
  jake: { estrelas: 2, bonus: 20 }, // Jake
  mewtwo: { estrelas: 2, bonus: 20 }, // Mewtwo
  rick: { estrelas: 2, bonus: 20 }, // Rick Sanchez
  salsicha: { estrelas: 2, bonus: 20 }, // Salsicha
  shera: { estrelas: 2, bonus: 20 }, // She-Ra
  shrek: { estrelas: 2, bonus: 20 }, // Shrek
  stewie: { estrelas: 2, bonus: 20 }, // Stewie Griffin
  woody: { estrelas: 2, bonus: 20 }, // Woody
  yoda: { estrelas: 2, bonus: 20 }, // Yoda
  zelda: { estrelas: 2, bonus: 20 }, // Zelda
  // ★
  buzz: { estrelas: 1, bonus: 15 }, // Buzz Lightyear
  heman: { estrelas: 1, bonus: 15 }, // He-Man
  pernalonga: { estrelas: 1, bonus: 15 }, // Pernalonga
  shiryu: { estrelas: 1, bonus: 15 }, // Shiryu
  shun: { estrelas: 1, bonus: 15 }, // Shun
  skeletor: { estrelas: 1, bonus: 15 }, // Skeletor
  tails: { estrelas: 1, bonus: 15 }, // Tails
  anubis: { estrelas: 1, bonus: 10 }, // Anúbis
  azula: { estrelas: 1, bonus: 10 }, // Azula
  bowser: { estrelas: 1, bonus: 10 }, // Bowser
  donatello: { estrelas: 1, bonus: 10 }, // Donatello
  donkeykong: { estrelas: 1, bonus: 10 }, // Donkey Kong
  elsa: { estrelas: 1, bonus: 10 }, // Elsa
  eren: { estrelas: 1, bonus: 10 }, // Eren Yeager
  erza: { estrelas: 1, bonus: 10 }, // Erza Scarlet
  freddy: { estrelas: 1, bonus: 10 }, // Freddy Krueger
  ironman: { estrelas: 1, bonus: 10 }, // Homem de Ferro
  kazuya: { estrelas: 1, bonus: 10 }, // Kazuya Mishima
  kingkong: { estrelas: 1, bonus: 10 }, // King Kong
  kirby: { estrelas: 1, bonus: 10 }, // Kirby
  lelouch: { estrelas: 1, bonus: 10 }, // Lelouch
  leonardo: { estrelas: 1, bonus: 10 }, // Leonardo
  lexluthor: { estrelas: 1, bonus: 10 }, // Lex Luthor
  luke: { estrelas: 1, bonus: 10 }, // Luke Skywalker
  megatron: { estrelas: 1, bonus: 10 }, // Megatron
  mob: { estrelas: 1, bonus: 10 }, // Mob
  omniman: { estrelas: 1, bonus: 10 }, // Omni-Man
  pyramidhead: { estrelas: 1, bonus: 10 }, // Cabeça de Pirâmide
  raidenmgr: { estrelas: 1, bonus: 10 }, // Raiden (Metal Gear)
  raidenmk: { estrelas: 1, bonus: 10 }, // Raiden (Mortal Kombat)
  samuraijack: { estrelas: 1, bonus: 10 }, // Samurai Jack
  sekiro: { estrelas: 1, bonus: 10 }, // Sekiro
  shredder: { estrelas: 1, bonus: 10 }, // Shredder
  silversurfer: { estrelas: 1, bonus: 10 }, // Surfista Prateado
  srincrivel: { estrelas: 1, bonus: 10 }, // Sr. Incrível
  ultron: { estrelas: 1, bonus: 10 }, // Ultron
  ursula: { estrelas: 1, bonus: 10 }, // Úrsula
  wolverine: { estrelas: 1, bonus: 10 }, // Wolverine
  zoro: { estrelas: 1, bonus: 10 }, // Roronoa Zoro
  flash: { estrelas: 1, bonus: 5 }, // Flash
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
