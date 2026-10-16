/*
 * O Caminho do Nexus: a campanha do PvP contra 40 rivais (pedido do jogador: "uma campanha mesmo… você começa só
 * com um desbloqueado… cada um focado num tipo de coisa diferente… difícil… capriche").
 *
 *  - 8 regiões, do Vale do Despertar ao Trono do Nexus; cada uma com 4 rivais e um chefe. Vencer um rival libera o
 *    próximo; vencer o chefe abre a região seguinte.
 *  - Cada rival tem um jeito próprio: a coleção dele (só tanques, só veneno, só deuses, só Dragon Ball…), o quanto ele
 *    pensa para montar os times (do "de olho fechado" ao mestre) e como escolhe o time de cada rodada (ao acaso, o
 *    mais forte, contra os seus, ou "vendo o futuro": testa as lutas da rodada antes de escolher).
 *  - Os chefes das regiões 6, 7 e 8 têm a Aura do Chefe: +10%, +15% e +20% de Vida nos personagens dele.
 *  - Estrelas por rival: 3★ vencendo 3–0, 2★ com 3–1, 1★ com 3–2 (fica a melhor). São 120 estrelas, e elas dão os
 *    títulos, de Aprendiz a Lenda do Nexus.
 *  - Rodízio (pedido do jogador: "pra pessoa não usar sempre só os mesmos, tanto você quanto os NPC"): os 3
 *    personagens que mais lutaram nas últimas 5 partidas da campanha descansam as 3 partidas seguintes. Vale para
 *    você e para cada rival (o rival conta só as partidas contra você).
 *  - O rating: contra os rivais ganha 80% e perde 120% do Elo (src/engine/pvp.ts, variacaoContraNpc).
 *
 * Quem manda é o servidor (supabase/functions/ranked-api/campanha.ts): ele guarda o progresso e o descanso, monta os
 * times do rival depois de receber os seus, sorteia em segredo as sementes das lutas e a escolha do rival, e calcula
 * cada luta com este mesmo motor. Este arquivo tem as regras que o servidor e o aparelho dividem.
 */
import { byId, characters } from '../data/characters';
import { DUPLAS } from '../data/duplas-medidas';
import { estrelasDaNota, notaDoTrio } from '../presentation/dicas-do-trio';
import { identidadesDe, type Identidade } from '../presentation/identities';
import { createBattle, stepBattle } from './battle';
import { chanceDoTrio, montarTimes, sorteio, timesLivres, type JeitoDeMontar, type PartidaPvp, type Times } from './pvp';

/* ---------------------------------------------------------------------------
 * As regiões
 * ------------------------------------------------------------------------- */

export interface Regiao { n: number; id: string; nome: string; lema: string; cor: string; cor2: string; icone: string; aura: number }
export const REGIOES: readonly Regiao[] = [
  { n: 1, id: 'vila', nome: 'Vale do Despertar', lema: 'Todo duelista desperta em algum lugar.', cor: '#8fe08a', cor2: '#2f7a4a', icone: '🏡', aura: 0 },
  { n: 2, id: 'floresta', nome: 'Floresta Sombria', lema: 'As árvores têm olhos. E dentes.', cor: '#4fd39a', cor2: '#145c46', icone: '🌲', aura: 0 },
  { n: 3, id: 'neon', nome: 'Metrópole Neon', lema: 'Luzes, máquinas e gente rápida demais.', cor: '#53d6ff', cor2: '#2a3f9e', icone: '🌃', aura: 0 },
  { n: 4, id: 'deserto', nome: 'Dunas Escarlates', lema: 'O sol cansa. Os rivais, mais ainda.', cor: '#ffc061', cor2: '#9c4a1c', icone: '🏜️', aura: 0 },
  { n: 5, id: 'templo', nome: 'Santuário Proibido', lema: 'Aqui ninguém luta limpo.', cor: '#b99bff', cor2: '#3c2373', icone: '🏯', aura: 0 },
  { n: 6, id: 'vulcao', nome: 'Coração do Vulcão', lema: 'Força bruta e fogo. Muito fogo.', cor: '#ff7a45', cor2: '#7a1c12', icone: '🌋', aura: 0.1 },
  { n: 7, id: 'ceu', nome: 'Cidadela Celeste', lema: 'Os imortais não perdem fácil.', cor: '#ffe27a', cor2: '#8a6a12', icone: '☁️', aura: 0.15 },
  { n: 8, id: 'trono', nome: 'Trono do Nexus', lema: 'O fim do caminho. O Imperador espera.', cor: '#ff5fd8', cor2: '#4a0f6e', icone: '👑', aura: 0.2 },
];

/* ---------------------------------------------------------------------------
 * Os cérebros: como cada rival monta e escolhe
 * ------------------------------------------------------------------------- */

/**
 * Como o rival escolhe o time da rodada:
 *  - acaso: qualquer um;
 *  - forte: o mais forte que ainda pode usar;
 *  - esperto: o que tem mais chance contra os times que você ainda pode escolher;
 *  - mestre: como o esperto, pesando mais os seus times fortes;
 *  - vidente: antes de escolher, testa lutas de verdade de cada time dele contra cada time seu (`visoes` lutas por
 *    par, com outras sementes: ele vê como o encontro costuma terminar, não a luta exata que vai valer) e fica com o
 *    que mais vence.
 */
export type Escolha = 'acaso' | 'forte' | 'esperto' | 'mestre' | 'vidente';
export interface Cerebro extends JeitoDeMontar {
  /** De 1 a 8: a esperteza mostrada na ficha. */
  nivel: number;
  /** A chance de escolher o time da rodada ao acaso, mesmo sabendo mais. */
  acaso: number;
  escolha: Escolha;
  /** Começa pelos trios que mais vencem de verdade (src/data/trios-do-pvp.ts) entre os `melhores` que ele tem. */
  lista?: { melhores: number; variacao: number };
  /** O vidente: quantas lutas de teste ele faz para cada par de times. */
  visoes?: number;
}
const CEREBROS: Record<number, Cerebro> = {
  1: { nivel: 1, amostras: 1, erro: 0, melhora: 0, acaso: 1, escolha: 'acaso' },
  2: { nivel: 2, amostras: 4, erro: 0.6, melhora: 2, acaso: 0.6, escolha: 'forte' },
  3: { nivel: 3, amostras: 10, erro: 0.45, melhora: 15, acaso: 0.4, escolha: 'esperto' },
  4: { nivel: 4, amostras: 25, erro: 0.3, melhora: 60, acaso: 0.25, escolha: 'esperto' },
  5: { nivel: 5, amostras: 80, erro: 0.15, melhora: 400, acaso: 0.15, escolha: 'esperto' },
  6: { nivel: 6, amostras: 200, erro: 0.05, melhora: 1500, acaso: 0.08, escolha: 'mestre', lista: { melhores: 60, variacao: 10 } },
  7: { nivel: 7, amostras: 300, erro: 0.02, melhora: 2500, acaso: 0.03, escolha: 'mestre', lista: { melhores: 18, variacao: 4 } },
  8: { nivel: 8, amostras: 300, erro: 0.01, melhora: 3000, acaso: 0, escolha: 'mestre', lista: { melhores: 8, variacao: 2 } },
};
const cerebro = (nivel: number, mudar: Partial<Cerebro> = {}): Cerebro => ({ ...CEREBROS[nivel]!, ...mudar });

/* ---------------------------------------------------------------------------
 * As coleções: de onde cada rival tira os personagens
 * ------------------------------------------------------------------------- */

/** A força de cada personagem para a campanha: quanto o trio com ele vence, com dois parceiros quaisquer. */
const SOLO = (id: string) => DUPLAS[id]?.solo ?? 0.5;
const PELA_FORCA = characters.map((c) => c.id).sort((a, b) => SOLO(a) - SOLO(b) || a.localeCompare(b));
const POSICAO = new Map(PELA_FORCA.map((id, i) => [id, i / (PELA_FORCA.length - 1)]));

export interface Colecao {
  /** Quem combina com o jeito dele (sem filtro: todos). */
  filtro?: (id: string) => boolean;
  /** Até onde ele vai na régua de força (0 = o mais fraco, 1 = o mais forte). */
  teto: number;
  /** No mínimo quantos personagens (completa com os parecidos, se o filtro der menos). */
  minimo?: number;
}
const tem = (...xs: Identidade[]) => (id: string) => { const d = identidadesDe(id); return xs.some((x) => d.includes(x)); };
const etiqueta = (...xs: string[]) => (id: string) => byId[id]!.tags.some((t) => xs.includes(t));
const universo = (...xs: string[]) => (id: string) => xs.includes(byId[id]!.universe);
const ou = (...fs: ((id: string) => boolean)[]) => (id: string) => fs.some((f) => f(id));

const DESENHOS = ['Looney Tunes', 'Bob Esponja', 'Scooby-Doo', 'Hora de Aventura', 'Tom e Jerry', 'Os Simpsons', 'Family Guy', 'Johnny Bravo', 'O Laboratório de Dexter',
  'Padrinhos Mágicos', 'As Meninas Superpoderosas', 'Coragem', 'Pantera Cor-de-Rosa', 'South Park', 'Gravity Falls', 'Steven Universo', 'Danny Phantom', 'Ben 10',
  'Capitão Planeta', 'Inspetor Bugiganga', 'Lilo & Stitch', 'Popeye', 'Rick and Morty', 'Disney', 'Pica-Pau', 'Toy Story', 'Shrek', 'Megamente', 'ThunderCats'];
const TERROR = ['Sexta-Feira 13', 'A Hora do Pesadelo', 'Halloween', 'Brinquedo Assassino', 'It', 'Pânico', 'O Massacre da Serra Elétrica', 'Hellraiser', 'O Chamado',
  'Invocação do Mal', 'Alien', 'Predador', 'Silent Hill', 'Resident Evil'];

/* ---------------------------------------------------------------------------
 * Os 40 rivais
 * ------------------------------------------------------------------------- */

export interface Rival {
  /** 1 a 40, a ordem do caminho. */
  n: number; id: string; regiao: number; chefe: boolean;
  nome: string; titulo: string;
  /** O personagem que é a "cara" dele. */
  avatar: string; cor: string; rating: number;
  /** O jeito dele em poucas palavras (aparece no mapa) e explicado (na ficha). */
  estilo: string; jeito: string;
  /** O que ele diz antes, quando vence e quando perde. */
  fala: string; venceu: string; perdeu: string;
  colecao: Colecao;
  cerebro: Cerebro;
  /** Monta com personagens parecidos com os seus (O Espelho). */
  espelho?: boolean;
  /** Aura do Chefe: Vida a mais nos personagens dele. */
  aura: number;
  /** A nota máxima de cada time dele (Infinity: sem teto) e as estrelas que isso dá (o caminho sobe aos poucos). */
  teto: number; estrelas: number;
}

type SemN = Omit<Rival, 'n' | 'regiao' | 'chefe' | 'aura' | 'rating' | 'teto' | 'estrelas'>;
/*
 * O teto de força de cada rival, na ordem do caminho (pedido do dono: o 2º rival montava times 7★). É a nota máxima de
 * cada time dele (a mesma das estrelas): sem teto, quase todos juntavam combos até o 7★ e o caminho não subia. Medido
 * contra um jogador bom (60 personagens, times de 6★ e 7★): a Região 1 vai de 1★ a 5★ e ele vence quase sempre; os
 * 7★ chegam na Região 3 e a força cresce até a Região 6, onde acaba o teto (os chefes finais montam com tudo).
 */
const SEM_TETO = Infinity;
const TETO_DOS_RIVAIS = [
  0, 0.15, 0.4, 0.6, 0.9, // Região 1: 1★ → 5★
  1, 1.2, 1.4, 1.6, 2, // Região 2: 5★ → 6★
  2.1, 2.3, 2.5, 2.7, 3, // Região 3: os primeiros 7★
  3, 3.2, 3.4, 3.6, 4, // Região 4
  4, 4.3, 4.6, 5, SEM_TETO, // Região 5
];
const POR_REGIAO: SemN[][] = [
  [
    { id: 'zepipoca', nome: 'O Apostador', titulo: 'Joga com a Sorte', avatar: 'patrick', cor: '#ffb3c7', estilo: 'Ao acaso', jeito: 'Monta os times de olho fechado e escolhe no par ou ímpar.',
      fala: 'Os dados já rolaram. Vamos ver de que lado caem.', venceu: 'A sorte escolheu o meu lado.', perdeu: 'Hoje os dados eram seus.', colecao: { teto: 0.3 }, cerebro: cerebro(1) },
    { id: 'vovococa', nome: 'Rei da Matilha', titulo: 'Senhor das Feras', avatar: 'scooby', cor: '#ffd27f', estilo: 'Só bichos', jeito: 'Só joga com bichos, monstrinhos e criaturas. Escolhe sempre o time que parece mais bravo.',
      fala: 'A matilha já sentiu o seu cheiro.', venceu: 'A matilha come primeiro.', perdeu: 'A matilha recua… por enquanto.', colecao: { filtro: etiqueta('animal', 'monster', 'beast-instinct'), teto: 0.5 }, cerebro: cerebro(3) },
    { id: 'ticodesenho', nome: 'O Animador', titulo: 'Senhor dos Desenhos', avatar: 'pernalonga', cor: '#7fd3ff', estilo: 'Desenhos animados', jeito: 'Cresceu vendo desenho e só joga com eles. Não subestime um coelho com uma bigorna.',
      fala: 'No meu mundo, a física é só uma sugestão.', venceu: 'Isso é tudo, pessoal!', perdeu: 'Fim do episódio… mas tem continuação.', colecao: { filtro: universo(...DESENHOS), teto: 0.6 }, cerebro: cerebro(3) },
    { id: 'cacadora', nome: 'Caçadora Sombria', titulo: 'Nunca Erra o Alvo', avatar: 'artemis', cor: '#c6e37a', estilo: 'Caça aos fracos', jeito: 'Escolhe quem termina os feridos: finalização e precisão. Seu personagem com pouca Vida é o alvo.',
      fala: 'Já sei quem cai primeiro.', venceu: 'Presa abatida.', perdeu: 'Hoje a caça escapou.', colecao: { filtro: ou(tem('Finalização'), etiqueta('hunter', 'precision', 'predator')), teto: 0.72 }, cerebro: cerebro(4) },
    { id: 'guardiaodavila', nome: 'Guardião do Vale', titulo: 'Chefe do Vale', avatar: 'shrek', cor: '#9be36b', estilo: 'O melhor do vale', jeito: 'Junta o que o vale tem de melhor e já sabe escolher contra os seus times.',
      fala: 'Ninguém sai do vale sem passar por mim.', venceu: 'Volte quando estiver pronto.', perdeu: 'O caminho é seu. Cuidado na floresta.', colecao: { teto: 0.65 }, cerebro: cerebro(4) },
  ],
  [
    { id: 'hackerbyte', nome: 'Código Zero', titulo: 'Mente Digital', avatar: 'cyborg', cor: '#4fe3ff', estilo: 'Tecnologia', jeito: 'Robôs, máquinas e gênios da tecnologia. Calcula tudo antes de montar.',
      fala: 'Já rodei 1 milhão de simulações. Você perde em todas.', venceu: 'Erro 404: sua vitória não foi encontrada.', perdeu: 'Bug no sistema. Isso não é possível.', colecao: { filtro: etiqueta('tech', 'artificial', 'cyborg', 'android', 'inventor', 'gadget'), teto: 0.86 }, cerebro: cerebro(5) },
    { id: 'druida', nome: 'Druida Ancestral', titulo: 'Guardiã do Verde', avatar: 'groot', cor: '#7be08f', estilo: 'Regeneração', jeito: 'Cura e regenera sem parar. Se você não derrubar rápido, ela não cai nunca.',
      fala: 'Toda folha volta a crescer.', venceu: 'A floresta sempre vence.', perdeu: 'Até o carvalho mais velho cai.', colecao: { filtro: tem('Regeneração', 'Cura', 'Sobrevivência'), teto: 0.72 }, cerebro: cerebro(4) },
    { id: 'detetive', nome: 'Detetive Sombra', titulo: 'Lê Cada Jogada', avatar: 'lawliet', cor: '#c5c9d6', estilo: 'Interrupção', jeito: 'Corta os seus preparos e responde na hora: Interrupção e Contra-ataque. Esperto na escolha.',
      fala: 'Eu já sei qual time você vai escolher.', venceu: 'Elementar.', perdeu: 'Interessante… muito interessante.', colecao: { filtro: tem('Interrupção', 'Contra-ataque'), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'shogun', nome: 'Samurai Errante', titulo: 'Lâmina sem Mestre', avatar: 'kenpachi', cor: '#d65a5a', estilo: 'Espadachins', jeito: 'Só espadachins e duelistas. Corta rápido e não foge de luta.',
      fala: 'Uma lâmina. Um golpe. Um vencedor.', venceu: 'Sua espada era cega.', perdeu: 'Um duelo digno. Sigo errante.', colecao: { filtro: etiqueta('swordsman', 'duelist', 'dualblade'), teto: 0.8 }, cerebro: cerebro(5) },
    { id: 'rainhaveneno', nome: 'Rainha do Veneno', titulo: 'Chefe da Floresta', avatar: 'poisonivy', cor: '#6be36b', estilo: 'Veneno e Status', jeito: 'Dano contínuo, veneno e aflições: cada segundo da luta tira Vida de você. Purificar ajuda muito.',
      fala: 'Respire fundo. É o último ar limpo que você vai ter.', venceu: 'O veneno sempre chega.', perdeu: 'Você… resistiu ao meu veneno?', colecao: { filtro: tem('Dano contínuo', 'Aflições', 'Debuff'), teto: 0.72 }, cerebro: cerebro(4) },
  ],
  [
    { id: 'fadatrapaca', nome: 'A Trapaceira', titulo: 'Rainha dos Truques', avatar: 'cosmowanda', cor: '#f39bff', estilo: 'Truques e fraquezas', jeito: 'Enfraquece, engana e bagunça os seus planos. Os times dela são cheios de Debuff.',
      fala: 'Pisque e você já caiu na peça.', venceu: 'Caiu direitinho na armadilha.', perdeu: 'Isso não estava no meu plano…', colecao: { filtro: ou(tem('Debuff', 'Copiar'), etiqueta('trickster', 'illusion', 'deception')), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'ermitao', nome: 'Colosso de Pedra', titulo: 'A Muralha Viva', avatar: 'snorlax', cor: '#9fc98f', estilo: 'Tanques', jeito: 'Só tanques e protetores. Luta devagar, apanha muito e não cai. Leve dano de sobra.',
      fala: 'Pode bater. Eu espero.', venceu: 'Cansou? Eu nem comecei.', perdeu: 'Hm. Você é mais forte do que parece.', colecao: { filtro: tem('Tanque', 'Proteção'), teto: 0.95 }, cerebro: cerebro(5) },
    { id: 'valquiria', nome: 'Valquíria', titulo: 'Guardiã da Liga', avatar: 'wonderwoman', cor: '#ffd36b', estilo: 'Só DC', jeito: 'A Liga inteira e seus vilões. Monta como uma estrategista de guerra.',
      fala: 'Pela Liga!', venceu: 'Justiça feita.', perdeu: 'Hoje a Liga perdeu. Amanhã não.', colecao: { filtro: universo('DC', 'Image', 'Dark Horse'), teto: 1 }, cerebro: cerebro(8, { lista: { melhores: 8, variacao: 2 } }) },
    { id: 'faisca', nome: 'Relâmpago', titulo: 'O Mais Rápido da Metrópole', avatar: 'flash', cor: '#ffd54a', estilo: 'Velocidade', jeito: 'Velocistas e Ritmo: age duas vezes antes de você agir uma.',
      fala: 'Já terminei. Você ainda vai começar?', venceu: 'Rápido demais pra você!', perdeu: 'Corri… e tropecei.', colecao: { filtro: ou(tem('Ritmo'), etiqueta('speedster', 'lightning')), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'capitaoaco', nome: 'General de Aço', titulo: 'Chefe da Metrópole', avatar: 'optimus', cor: '#7fb2ff', estilo: 'A Muralha', jeito: 'Tanques fortes, escudos e sobrevivência. A muralha de verdade: só cai com muito dano ou Exposto.',
      fala: 'Esta metrópole tem um protetor.', venceu: 'Nenhum golpe passa por mim.', perdeu: 'Você derrubou a muralha. Respeito.', colecao: { filtro: tem('Tanque', 'Proteção', 'Sobrevivência'), teto: 0.9 }, cerebro: cerebro(5) },
  ],
  [
    { id: 'doutoravida', nome: 'A Sacerdotisa', titulo: 'Ninguém Cai no Turno Dela', avatar: 'tsunade', cor: '#ff8fb1', estilo: 'Cura e Reviver', jeito: 'Cura, reviver e renascer: quem cai do lado dela volta. Derrube todos de uma vez.',
      fala: 'Enquanto eu estiver de pé, ninguém do meu lado cai.', venceu: 'Eu disse: ninguém cai.', perdeu: 'Nem a minha luz foi o bastante…', colecao: { filtro: tem('Cura', 'Reviver', 'Renascer', 'Purificar'), teto: 0.86 }, cerebro: cerebro(5) },
    { id: 'farao', nome: 'Faraó Eterno', titulo: 'O Que Não Morre', avatar: 'mummra', cor: '#e8c36a', estilo: 'Mortos-vivos', jeito: 'Deuses do Egito, múmias e mortos-vivos. Muitos voltam depois de cair.',
      fala: 'Eu já morri antes. Não funcionou.', venceu: 'Mais um para a minha pirâmide.', perdeu: 'Voltarei… daqui a mil anos.', colecao: { filtro: ou(universo('Mitologia Egípcia'), etiqueta('undead', 'vampire'), tem('Renascer')), teto: 1 }, cerebro: cerebro(6, { lista: { melhores: 200, variacao: 10 } }) },
    { id: 'escorpiao', nome: 'Lâmina das Dunas', titulo: 'O Assassino do Deserto', avatar: 'scorpion', cor: '#ffb03a', estilo: 'Assassinos', jeito: 'Assassinos e golpes fatais: explosão rápida no seu mais frágil.',
      fala: 'Venha cá!', venceu: 'Fatality.', perdeu: 'A areia engoliu meu golpe.', colecao: { filtro: ou(etiqueta('assassin', 'execution', 'finisher'), tem('Explosão')), teto: 0.8 }, cerebro: cerebro(5) },
    { id: 'mercenario', nome: 'Mercenário', titulo: 'Senhor da Marvel', avatar: 'deadpool', cor: '#ff5a5a', estilo: 'Só Marvel', jeito: 'Só heróis e vilões da Marvel, e são muitos. Monta bem os combos do universo.',
      fala: 'Oi, leitor! Ops, jogador.', venceu: 'Máximo esforço!', perdeu: 'Isso vai pro filme? Corta essa parte.', colecao: { filtro: universo('Marvel'), teto: 1 }, cerebro: cerebro(5) },
    { id: 'sultao', nome: 'Sultão das Areias', titulo: 'Chefe do Deserto', avatar: 'genie', cor: '#ffcf5a', estilo: 'O Invocador', jeito: 'Invoca criaturas que lutam do lado dele: o time dele parece maior que o seu.',
      fala: 'Três desejos: vencer, vencer e vencer.', venceu: 'Desejo concedido.', perdeu: 'Volte para a lâmpada… eu.', colecao: { filtro: ou(tem('Invocação', 'Buff'), etiqueta('summoner')), teto: 1 }, cerebro: cerebro(7, { lista: { melhores: 40, variacao: 6 } }) },
  ],
  [
    { id: 'miragem', nome: 'Miragem', titulo: 'Ilusões e Cópias', avatar: 'loki', cor: '#9be0c9', estilo: 'Ilusões', jeito: 'Ilusionistas, copiadores e mentirosos. Nada do lado dele é o que parece.',
      fala: 'Qual de mim é o verdadeiro?', venceu: 'Você lutou contra uma sombra.', perdeu: 'A miragem se desfez…', colecao: { filtro: ou(tem('Copiar', 'Controle'), etiqueta('illusion', 'deception', 'trickster', 'copy', 'hypnosis')), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'brunabrava', nome: 'A Destruidora', titulo: 'Só Sabe Atacar', avatar: 'arlequina', cor: '#ff7a8a', estilo: 'Só ataque', jeito: 'Defesa é pra quem tem medo. Monta tudo com explosão, pressão e golpe final.',
      fala: 'Defesa é para quem tem medo.', venceu: 'Nada sobra de pé.', perdeu: 'Faltou bater mais forte.', colecao: { filtro: tem('Explosão', 'Pressão', 'Finalização'), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'kage', nome: 'Kage da Folha', titulo: 'Mestre Shinobi', avatar: 'kakashi', cor: '#ff9f43', estilo: 'Só ninjas', jeito: 'Shinobis de Naruto e ninjas de outros mundos. Conhece cada combo da Folha.',
      fala: 'Esse é o meu jeito ninja!', venceu: 'Missão cumprida, ttebayo!', perdeu: 'Preciso treinar mais um pouco…', colecao: { filtro: ou(universo('Naruto'), etiqueta('assassin', 'spy')), teto: 1, minimo: 16 }, cerebro: cerebro(7, { lista: { melhores: 40, variacao: 6 } }) },
    { id: 'bruxa', nome: 'Bruxa das Trevas', titulo: 'Maldições Antigas', avatar: 'maleficent', cor: '#c07bff', estilo: 'Magia e maldição', jeito: 'Magos, bruxas e maldições. Debuff em você, poder do lado dela.',
      fala: 'Meu caldeirão já sabe o seu nome.', venceu: 'A maldição está feita.', perdeu: 'O feitiço virou contra mim…', colecao: { filtro: ou(etiqueta('magic', 'witch', 'curse', 'cursed', 'mage', 'mystic'), tem('Debuff')), teto: 1 }, cerebro: cerebro(5) },
    { id: 'terror', nome: 'A Assombração', titulo: 'Chefe do Templo', avatar: 'samara', cor: '#8f9bb3', estilo: 'Filmes de terror', jeito: 'A rainha do terror e os monstros dos filmes. Eles não correm, mas sempre alcançam.',
      fala: 'Sete dias.', venceu: 'Agora você vai ter pesadelos.', perdeu: 'Eu volto. Sempre volto.', colecao: { filtro: ou(universo(...TERROR), etiqueta('undead', 'monster', 'demon')), teto: 1 }, cerebro: cerebro(6, { lista: { melhores: 120, variacao: 8 } }) },
  ],
  [
    { id: 'monge', nome: 'Monge do Silêncio', titulo: 'Controle Total', avatar: 'shaka', cor: '#e6d38a', estilo: 'Controle', jeito: 'Atordoa, congela e prende. Se você não agir, não vence.',
      fala: 'Fique parado. Ouça o silêncio.', venceu: 'A paz venceu.', perdeu: 'O silêncio foi quebrado.', colecao: { filtro: tem('Controle', 'Interrupção'), teto: 0.9 }, cerebro: cerebro(5) },
    { id: 'saiyajin', nome: 'Príncipe Saiyajin', titulo: 'Orgulho da Raça Guerreira', avatar: 'broly', cor: '#ffd23f', estilo: 'Só Dragon Ball', jeito: 'Os guerreiros de Dragon Ball e quem treina como eles: transformação e poder que cresce. E testa as lutas antes de escolher o time.',
      fala: 'Meu poder passa de 8 mil!', venceu: 'Você nunca vai superar um Saiyajin!', perdeu: 'Impossível… um terráqueo?', colecao: { filtro: ou(universo('Dragon Ball'), tem('Transformação')), teto: 1, minimo: 16 }, cerebro: cerebro(8, { escolha: 'vidente', visoes: 1, acaso: 0, lista: { melhores: 8, variacao: 2 } }) },
    { id: 'forja', nome: 'Mestre da Forja', titulo: 'Buff e Carga', avatar: 'ironman', cor: '#ffa94d', estilo: 'Fortalecer', jeito: 'Fortalece o próprio time e carrega as habilidades rápido: cada luta dele começa fraca e termina enorme.',
      fala: 'Cada golpe meu é forjado no fogo.', venceu: 'Obra-prima.', perdeu: 'Volta pra bigorna.', colecao: { filtro: tem('Buff', 'Carga', 'Suporte'), teto: 1 }, cerebro: cerebro(8, { lista: { melhores: 8, variacao: 2 } }) },
    { id: 'dragaorubro', nome: 'Dragão Rubro', titulo: 'Senhor das Chamas', avatar: 'charizard', cor: '#ff6a3d', estilo: 'Dragões e fogo', jeito: 'Dragões e fogo: queima o seu time de longe e de perto.',
      fala: 'Sinta o calor.', venceu: 'Cinzas. Só sobraram cinzas.', perdeu: 'Minha chama… apagou?', colecao: { filtro: ou(etiqueta('dragon', 'fire', 'sun'), tem('Área')), teto: 1 }, cerebro: cerebro(7, { lista: { melhores: 40, variacao: 6 } }) },
    { id: 'titamagma', nome: 'Titã de Magma', titulo: 'Chefe do Vulcão', avatar: 'godzilla', cor: '#ff5a1f', estilo: 'Explosão em área', jeito: 'Explosão e dano em área com a Aura do Chefe: +10% de Vida em todos os dele.',
      fala: 'A montanha acordou.', venceu: 'Derretido.', perdeu: 'O vulcão… adormece.', colecao: { filtro: tem('Explosão', 'Área', 'Finalização'), teto: 0.9 }, cerebro: cerebro(5) },
  ],
  [
    { id: 'arcanjo', nome: 'Arcanjo', titulo: 'Asas da Fênix', avatar: 'ikki', cor: '#ffb86b', estilo: 'Renascer', jeito: 'Renascer, reviver e curar: cada personagem dele cai duas vezes.',
      fala: 'Das cinzas, sempre.', venceu: 'A fênix voa de novo.', perdeu: 'Até a fênix descansa.', colecao: { filtro: tem('Renascer', 'Reviver', 'Cura', 'Regeneração'), teto: 1 }, cerebro: cerebro(6, { lista: { melhores: 120, variacao: 8 } }) },
    { id: 'senhordotempo', nome: 'Senhor do Tempo', titulo: 'Para o Relógio', avatar: 'dio', cor: '#f5e663', estilo: 'Tempo e ritmo', jeito: 'Para o tempo, atrasa você e adianta os dele: Ritmo e Interrupção no nível mais alto.',
      fala: 'Toki wo tomare!', venceu: 'O tempo é meu.', perdeu: 'Ninguém escapa do tempo… exceto você?', colecao: { filtro: ou(tem('Ritmo', 'Interrupção'), etiqueta('time', 'speedster')), teto: 1 }, cerebro: cerebro(7, { lista: { melhores: 40, variacao: 6 } }) },
    { id: 'espelho', nome: 'O Espelho', titulo: 'Joga Como Você', avatar: 'mewtwo', cor: '#c9d6ff', estilo: 'Copia você', jeito: 'Olha os seus 3 times e monta os dele com personagens que fazem as mesmas coisas, só que escolhidos a dedo. E já testa as lutas antes de escolher o time.',
      fala: 'Eu sou você. Só que melhor.', venceu: 'Perdeu pra você mesmo.', perdeu: 'O reflexo trincou.', colecao: { teto: 1 }, cerebro: cerebro(8, { escolha: 'vidente', visoes: 1, acaso: 0.05, lista: { melhores: 8, variacao: 2 } }), espelho: true },
    { id: 'furia', nome: 'Fúria', titulo: 'O Berserker', avatar: 'guts', cor: '#e04848', estilo: 'Brutamontes', jeito: 'Berserkers e brutamontes: quanto mais apanham, mais batem.',
      fala: 'RAAAAAH!', venceu: 'MAIS! QUERO MAIS!', perdeu: 'Ainda… estou… de pé…', colecao: { filtro: ou(etiqueta('berserker', 'juggernaut', 'brawler'), tem('Virada')), teto: 1 }, cerebro: cerebro(6, { lista: { melhores: 200, variacao: 10 } }) },
    { id: 'panteao', nome: 'O Panteão', titulo: 'Chefe do Céu', avatar: 'zeus', cor: '#fff07a', estilo: 'Só deuses', jeito: 'Deuses de todas as mitologias, com a Aura do Chefe: +15% de Vida.',
      fala: 'Ajoelhe-se diante do Olimpo.', venceu: 'Os mortais nunca aprendem.', perdeu: 'Um mortal… no Olimpo?', colecao: { filtro: ou(etiqueta('god', 'cosmic', 'asgardian'), universo('Mitologia Grega', 'Mitologia Egípcia', 'Mitologia Nórdica')), teto: 1 }, cerebro: cerebro(8, { lista: { melhores: 8, variacao: 2 } }) },
  ],
  [
    { id: 'oraculo', nome: 'O Oráculo', titulo: 'Vê o Futuro', avatar: 'strange', cor: '#a98bff', estilo: 'Vidente', jeito: 'Monta com trios fortes e, de vez em quando, vê o futuro: testa lutas de cada time dele contra cada time seu antes de escolher.',
      fala: 'Vi 14 milhões de futuros. Você vence em um.', venceu: 'Eu disse que ia ser assim.', perdeu: 'Este era o futuro único…', colecao: { teto: 1 }, cerebro: cerebro(5, { escolha: 'vidente', visoes: 1, acaso: 0.85, lista: { melhores: 1500, variacao: 20 } }) },
    { id: 'caos', nome: 'Coringa do Caos', titulo: 'Imprevisível', avatar: 'coringa', cor: '#b46bff', estilo: 'Imprevisível', jeito: 'Tem os mais fortes do jogo e monta na loucura. Escolhe a rodada sem lógica nenhuma: não dá para ler.',
      fala: 'Por que tão sério?', venceu: 'HAHAHAHA!', perdeu: 'Hehe… essa foi boa.', colecao: { teto: 1, filtro: (id) => (POSICAO.get(id) ?? 0) >= 0.45 }, cerebro: cerebro(5, { escolha: 'acaso', acaso: 1, lista: { melhores: 300, variacao: 12 } }) },
    { id: 'sombradomestre', nome: 'A Sombra do Mestre', titulo: 'O Antigo Mestre', avatar: 'vegeta', cor: '#ffd36b', estilo: 'O Mestre', jeito: 'O Mestre do Treino com os 400 e os trios campeões. Monta e escolhe como quem já jogou mil partidas.',
      fala: 'Você treinou comigo. Agora lute comigo.', venceu: 'Ainda é cedo pra você.', perdeu: 'O aluno passou o mestre.', colecao: { teto: 1 }, cerebro: cerebro(5, { lista: { melhores: 300, variacao: 12 } }) },
    { id: 'guardiaodotrono', nome: 'Guardião do Trono', titulo: 'O Último Portão', avatar: 'gojo', cor: '#8fd8ff', estilo: 'Mestre vidente', jeito: 'Monta com os trios campeões e vê o futuro melhor que o Oráculo: quando testa as lutas, faz duas por encontro.',
      fala: 'Ninguém chega ao Imperador.', venceu: 'O portão continua fechado.', perdeu: 'Pode passar. Ele está esperando.', colecao: { teto: 1 }, cerebro: cerebro(5, { escolha: 'vidente', visoes: 2, acaso: 0.85, lista: { melhores: 300, variacao: 12 } }) },
    { id: 'imperador', nome: 'Imperador do Nexus', titulo: 'Chefe Final', avatar: 'thanos', cor: '#ff4fd8', estilo: 'O mais forte', jeito: 'Os trios campeões, a visão do futuro mais clara (três lutas de teste por encontro) e a Aura do Chefe: +20% de Vida em todos.',
      fala: 'Eu sou inevitável.', venceu: 'O Nexus é meu. Para sempre.', perdeu: 'Então… o Nexus é seu.', colecao: { teto: 1 }, cerebro: cerebro(5, { escolha: 'vidente', visoes: 3, acaso: 0.85, lista: { melhores: 300, variacao: 12 } }) },
  ],
];

/** O rating de cada rival, do primeiro (600) ao Imperador (2500). */
const ratingDo = (n: number) => (n === 40 ? 2500 : 600 + Math.round((48 * (n - 1)) / 10) * 10);

export const RIVAIS: readonly Rival[] = POR_REGIAO.flatMap((lista, r) => lista.map((x, k): Rival => {
  const n = r * 5 + k + 1, chefe = k === 4;
  const teto = TETO_DOS_RIVAIS[n - 1] ?? SEM_TETO;
  return { ...x, n, regiao: r + 1, chefe, aura: chefe ? REGIOES[r]!.aura : 0, rating: ratingDo(n), teto, estrelas: teto === SEM_TETO ? 7 : estrelasDaNota(teto) };
}));
export const rivalPorId = (id: string) => RIVAIS.find((r) => r.id === id) ?? null;
export const TOTAL_DE_ESTRELAS = RIVAIS.length * 3;

/* ---------------------------------------------------------------------------
 * A coleção de cada rival
 * ------------------------------------------------------------------------- */

const MINIMO_DO_RIVAL = 15;
const cache = new Map<string, string[]>();
/** Os personagens do rival: os do jeito dele até o teto de força (no mínimo 15, completando com os parecidos). */
export function colecaoDoRival(r: Pick<Rival, 'id' | 'colecao'>): string[] {
  const ja = cache.get(r.id);
  if (ja) return ja;
  const { filtro = () => true, teto, minimo = MINIMO_DO_RIVAL } = r.colecao;
  const doJeito = PELA_FORCA.filter(filtro);
  let lista = doJeito.filter((id) => POSICAO.get(id)! <= teto);
  // poucos até o teto: pega os mais fracos do jeito dele (passa um pouco do teto)
  if (lista.length < minimo) lista = doJeito.slice(0, minimo);
  // ainda poucos: completa com quem mais se parece com os dele (as mesmas funções), até o teto
  if (lista.length < minimo) {
    const funcoes = new Set(lista.flatMap((id) => identidadesDe(id)));
    const parecido = (id: string) => identidadesDe(id).filter((x) => funcoes.has(x)).length;
    const resto = PELA_FORCA.filter((id) => !lista.includes(id) && POSICAO.get(id)! <= Math.max(teto, 0.5)).sort((a, b) => parecido(b) - parecido(a) || SOLO(a) - SOLO(b));
    lista = [...lista, ...resto.slice(0, minimo - lista.length)];
  }
  cache.set(r.id, lista);
  return lista;
}

/** O Espelho: dos 400, os que mais fazem o que os seus 9 fazem (as funções e o universo). */
export function colecaoDoEspelho(seus: readonly string[]): string[] {
  const funcoes = new Map<Identidade, number>(), universos = new Set(seus.map((id) => byId[id]!.universe));
  for (const id of seus) for (const x of identidadesDe(id)) funcoes.set(x, (funcoes.get(x) ?? 0) + 1);
  const parecido = (id: string) => identidadesDe(id).reduce((s, x) => s + (funcoes.get(x) ?? 0), 0) + (universos.has(byId[id]!.universe) ? 2 : 0);
  return PELA_FORCA.filter((id) => !seus.includes(id)).sort((a, b) => parecido(b) - parecido(a) || SOLO(b) - SOLO(a)).slice(0, 45);
}

/* ---------------------------------------------------------------------------
 * O rival monta e escolhe
 * ------------------------------------------------------------------------- */

/**
 * Os 3 times do rival, com a coleção dele menos quem está descansando. O Espelho olha os seus times (o servidor
 * monta depois de receber os seus).
 */
export function timesDoRival(r: Rival, seed: number, descansando: readonly string[] = [], seus: readonly string[] = []): Times {
  const base = r.espelho && seus.length ? colecaoDoEspelho(seus) : colecaoDoRival(r);
  let livres = base.filter((id) => !descansando.includes(id));
  if (livres.length < 9) livres = base;
  return montarTimes(livres, r.cerebro, r.cerebro.lista, seed, notaDoTrio, r.teto < SEM_TETO ? (t) => notaDoTrio(t) <= r.teto : undefined);
}

/** A Vida a mais nos personagens do rival (a Aura do Chefe): a escala do lado dele na luta. */
export const escalaDoRival = (r: Pick<Rival, 'aura'>) => 1 + r.aura;

/** A luta de uma rodada (você de um lado, o rival do outro), até o fim. */
export function lutaDaRodada(meu: readonly string[], dele: readonly string[], seed: number, escala: number) {
  const b = createBattle([...meu], [...dele], seed, escala);
  for (let i = 0; i < 60000 && !b.finished; i++) stepBattle(b);
  return b;
}

/**
 * O rival escolhe o time da rodada. Ele vê os seus 3 times (como você vê os dele), não a sua escolha. O vidente testa
 * as lutas da rodada: para cada time dele, contra quantos dos seus times livres ele venceria com a semente que vai valer.
 */
export function escolhaDoRival(r: Rival, p: PartidaPvp, sorteioDaRodada: number, sementeDaLuta: number): number {
  const c = r.cerebro, sorte = sorteio(sorteioDaRodada ^ 0x27d4eb2f);
  const dele = timesLivres(p, 'rival'), seus = timesLivres(p, 'eu');
  if (dele.length === 1 || sorte() < c.acaso || c.escolha === 'acaso') return dele[Math.floor(sorte() * dele.length)]!;
  if (c.escolha === 'forte') return dele.reduce((a, b) => (notaDoTrio(p.deles[b]!) > notaDoTrio(p.deles[a]!) ? b : a));
  const peso = (j: number) => (c.escolha === 'esperto' ? 1 : 1 + notaDoTrio(p.meus[j]!) - Math.min(...seus.map((x) => notaDoTrio(p.meus[x]!))));
  const chance = (i: number) => seus.reduce((s, j) => s + peso(j) * chanceDoTrio(p.deles[i]!, p.meus[j]!), 0) / seus.reduce((s, j) => s + peso(j), 0);
  if (c.escolha !== 'vidente') return dele.reduce((a, b) => (chance(b) > chance(a) ? b : a));
  const escala = escalaDoRival(r), visoes = Math.max(1, c.visoes ?? 1);
  const teste = (k: number) => (Math.imul(sementeDaLuta ^ 0x5f3759df, k + 1) + 0x9e3779b9 * (k + 1)) >>> 0;
  const vence = (i: number) => seus.reduce((s, j) => {
    let v = 0;
    for (let k = 0; k < visoes; k++) if (lutaDaRodada(p.meus[j]!, p.deles[i]!, teste(k), escala).winner === 'enemy') v++;
    return s + (peso(j) * v) / visoes;
  }, 0);
  const valor = new Map(dele.map((i) => [i, vence(i) + chance(i) * 0.01]));
  return dele.reduce((a, b) => (valor.get(b)! > valor.get(a)! ? b : a));
}

/* ---------------------------------------------------------------------------
 * Estrelas, títulos e o caminho
 * ------------------------------------------------------------------------- */

/** As estrelas de uma vitória: 3–0 dá 3★, 3–1 dá 2★, 3–2 dá 1★. Derrota: 0. */
export function estrelasDaPartida(p: Pick<PartidaPvp, 'rodadas'>): number {
  const deles = p.rodadas.filter((x) => x.vencedor === 'rival').length, meus = new Set(p.rodadas.filter((x) => x.vencedor === 'eu').map((x) => x.meu)).size;
  return meus < 3 ? 0 : Math.max(1, 3 - deles);
}

export interface Titulo { nome: string; estrelas: number; cor: string }
export const TITULOS: readonly Titulo[] = [
  { nome: 'Aprendiz', estrelas: 0, cor: '#a9b4c6' },
  { nome: 'Desafiante', estrelas: 8, cor: '#8fe08a' },
  { nome: 'Guerreiro', estrelas: 20, cor: '#53d6ff' },
  { nome: 'Veterano', estrelas: 36, cor: '#ffc061' },
  { nome: 'Campeão', estrelas: 54, cor: '#b99bff' },
  { nome: 'Mestre', estrelas: 74, cor: '#ff7a45' },
  { nome: 'Grão-Mestre', estrelas: 96, cor: '#ffe27a' },
  { nome: 'Lenda do Nexus', estrelas: 120, cor: '#ff5fd8' },
];
export const tituloDas = (estrelas: number) => [...TITULOS].reverse().find((t) => estrelas >= t.estrelas)!;
export const proximoTitulo = (estrelas: number) => TITULOS.find((t) => t.estrelas > estrelas) ?? null;

/** As melhores estrelas contra cada rival (id → 1 a 3). */
export type Estrelas = Record<string, number>;
export const totalDeEstrelas = (e: Estrelas) => RIVAIS.reduce((s, r) => s + Math.min(3, Math.max(0, e[r.id] ?? 0)), 0);
/** Liberado: o primeiro, e cada um depois de vencer o anterior. */
export const liberado = (e: Estrelas, r: Pick<Rival, 'n'>) => r.n === 1 || (e[RIVAIS[r.n - 2]!.id] ?? 0) > 0;
/** O próximo rival ainda não vencido (null: o caminho inteiro já foi vencido). */
export const proximoRival = (e: Estrelas) => RIVAIS.find((r) => !(e[r.id] ?? 0)) ?? null;
export const zerou = (e: Estrelas) => (e.imperador ?? 0) > 0;

/* ---------------------------------------------------------------------------
 * O rodízio (descanso)
 * ------------------------------------------------------------------------- */

/** Quantos personagens você precisa para a campanha: 9 nos times e 3 descansando. */
export const MINIMO_DA_CAMPANHA = 12;
/** O rodízio de base (o dos rivais e o seu nas regiões 1–2). */
export const DESCANSO = { quantos: 3, partidas: 3, janela: 5 } as const;
export type RegraDoDescanso = { quantos: number; partidas: number };
/*
 * O seu rodízio (pedido do dono): descansam sempre 3 partidas; dormem 3 na região 1 e 4 da região 2 em diante (no
 * máximo 4). A região é a do rival da partida que acabou.
 */
export const DORMEM_NO_MAXIMO = 4;
export const descansoDaRegiao = (regiao: number): RegraDoDescanso =>
  ({ quantos: Math.min(DORMEM_NO_MAXIMO, DESCANSO.quantos + Math.max(1, regiao) - 1), partidas: DESCANSO.partidas });
/** O seu rodízio nesta região, sem nunca deixar menos de 9 livres (os 3 times): com 12 personagens, descansam 3. */
export const seuDescanso = (regiao: number, tamanhoDaColecao: number): RegraDoDescanso => {
  const r = descansoDaRegiao(regiao);
  return { quantos: Math.max(0, Math.min(r.quantos, tamanhoDaColecao - 9)), partidas: r.partidas };
};
/*
 * Só a partida contra um rival que ainda não tinha 3 estrelas mexe no seu descanso (pedido do dono): bater de novo num
 * rival já gabaritado não acorda ninguém (senão bastava farmar o mais fraco). Com 1 ou 2 estrelas ainda conta.
 */
export const contaParaODescanso = (estrelasAntes: Estrelas, rival: Pick<Rival, 'id'>) =>
  (estrelasAntes[rival.id] ?? 0) < 3 || totalDeEstrelas(estrelasAntes) >= TOTAL_DE_ESTRELAS; // com tudo gabaritado, qualquer uma conta
/** Quem descansa e por quantas partidas ainda (id → partidas). */
export type Descanso = Record<string, number>;

/** Quem lutou numa partida: cada personagem uma vez por rodada em que o time dele lutou. */
export function quemLutou(times: readonly (readonly string[])[], rodadas: readonly { time: number }[]): string[] {
  return rodadas.flatMap((r) => [...(times[r.time] ?? [])]);
}

/**
 * Depois de cada partida: quem descansava descansa uma partida a menos; se ninguém mais descansa, os `regra.quantos` que
 * mais lutaram nas últimas 5 partidas (`ultimas`, da mais antiga para a mais nova, esta incluída) descansam as
 * `regra.partidas` seguintes. Empate: quem lutou mais recentemente, depois o mais forte.
 */
export function depoisDaPartida(descanso: Descanso, ultimas: readonly (readonly string[])[], regra: RegraDoDescanso = DESCANSO): Descanso {
  const agora: Descanso = {};
  for (const [id, n] of Object.entries(descanso)) if (n > 1) agora[id] = n - 1;
  if (Object.keys(agora).length) return agora;
  const janela = ultimas.slice(-DESCANSO.janela), conta = new Map<string, number>(), quando = new Map<string, number>();
  janela.forEach((uso, k) => { for (const id of uso) { conta.set(id, (conta.get(id) ?? 0) + 1); quando.set(id, k); } });
  const ordem = [...conta.keys()].sort((a, b) => conta.get(b)! - conta.get(a)! || quando.get(b)! - quando.get(a)! || SOLO(b) - SOLO(a) || a.localeCompare(b));
  for (const id of ordem.slice(0, regra.quantos)) agora[id] = regra.partidas;
  return agora;
}

/** A sua coleção sem quem descansa. */
export const livresParaJogar = (colecao: readonly string[], descanso: Descanso) => colecao.filter((id) => !(descanso[id] > 0));

