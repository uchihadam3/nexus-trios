/*
 * FASE H · as conquistas.
 *
 * A direção pediu para tirar os Objetivos e deixar só as conquistas, "e deixe
 * interessante e divertido de conseguir". As que existiam não eram nem uma
 * coisa nem outra: cinquenta degraus de contador — vença 1, 10, 30, 100, 250;
 * bloqueie 100, 1.000, 5.000, 20.000, 60.000. Nada ali pede que você jogue
 * melhor, só que jogue mais. É grind com nome de conquista, e o próprio
 * documento já proibia grind nos Objetivos.
 *
 * Então estas são de **momento**. Cada uma descreve uma coisa específica que
 * aconteceu numa luta: derrubar alguém com um golpe só, vencer estando trinta
 * pontos atrás, terminar com os três acima de 80% de Vida, abrir o inimigo
 * para o aliado finalizar. São coisas que dão história — você lembra de quando
 * aconteceu — e que empurram para experimentar trios diferentes em vez de
 * repetir o mesmo cem vezes.
 *
 * Todas são verificadas contra o que o combate de fato produziu. Nenhuma pede
 * um número que só o tempo resolve.
 */
import { byId } from '../data/characters';
import type { EstadoRaioX } from './raio-x';
import type { FeitosPorPersonagem } from './maestria';
import type { RunBattleSummary } from './run-summary';
import type { Battle } from './types';

export type Categoria =
  | 'Jornada' | 'Combate' | 'Sinergia' | 'Experimentação' | 'Vantagem'
  | 'Controle' | 'Proteção' | 'Cura' | 'Personagens' | 'Segredos';

/** Tudo que se sabe no fim de uma batalha. */
export interface Contexto {
  battle: Battle;
  feitos: FeitosPorPersonagem;
  raioX: EstadoRaioX;
  time: string[];
  venceu: boolean;
  campeao: boolean;
  /** O quanto o trio chegou a ficar atrás na Vantagem (0 se nunca ficou). */
  maiorAtraso: number;
  /** Índice do confronto, de 0 a 9. */
  indice: number;
  /** As batalhas já concluídas nesta jornada. */
  jornada: readonly RunBattleSummary[];
  /** Personagens que o jogador já levou para a arena alguma vez. */
  vistos: readonly string[];
  /** Quantos personagens já têm Maestria III. */
  dominados: number;
}

export interface Conquista {
  id: string; nome: string; categoria: Categoria; dica: string;
  /** Secretas não mostram a dica antes de serem conquistadas. */
  secreta?: boolean;
  aconteceu: (c: Contexto) => boolean;
}

/* --------------------------------------------------------------------------
 * Atalhos de leitura
 * ------------------------------------------------------------------------ */

const meuTrio = (c: Contexto) => c.battle.fighters.filter((f) => f.side === 'player');
const feito = (c: Contexto, nome: keyof FeitosPorPersonagem[string]) =>
  c.time.reduce((n, id) => n + (c.feitos[id]?.[nome] ?? 0), 0);
const maiorFeito = (c: Contexto, nome: keyof FeitosPorPersonagem[string]) =>
  Math.max(0, ...c.time.map((id) => c.feitos[id]?.[nome] ?? 0));
const elos = (c: Contexto, tipo: string) => c.raioX.elos.filter((e) => e.tipo === tipo);
const universos = (c: Contexto) => new Set(c.time.map((id) => byId[id]?.universe)).size;

/* --------------------------------------------------------------------------
 * As conquistas
 * ------------------------------------------------------------------------ */

export const conquistas: readonly Conquista[] = [
  /* ---- Jornada ---- */
  { id: 'j-primeiro', nome: 'Primeiro passo', categoria: 'Jornada', dica: 'Vença o primeiro confronto de uma jornada.',
    aconteceu: (c) => c.venceu && c.indice === 0 },
  { id: 'j-metade', nome: 'Meia trilha', categoria: 'Jornada', dica: 'Chegue ao sexto confronto.',
    aconteceu: (c) => c.venceu && c.indice >= 5 },
  { id: 'j-campeao', nome: 'Trio campeão', categoria: 'Jornada', dica: 'Vença os dez confrontos de uma jornada.',
    aconteceu: (c) => c.campeao },
  { id: 'j-intacto', nome: 'Nenhum ficou para trás', categoria: 'Jornada', dica: 'Termine a jornada inteira sem perder um lutador em nenhum confronto.',
    aconteceu: (c) => c.campeao && c.jornada.every((b) => b.survivors === 3) && meuTrio(c).every((f) => f.hp > 0) },
  { id: 'j-sem-sustos', nome: 'Passeio', categoria: 'Jornada', dica: 'Vença cinco confrontos seguidos sem ficar atrás na Vantagem.',
    aconteceu: (c) => c.venceu && c.maiorAtraso === 0 && c.jornada.filter((b) => b.won).length >= 4 },
  { id: 'j-de-volta', nome: 'Volta por cima', categoria: 'Jornada', dica: 'Seja campeão numa jornada em que perdeu alguém pelo caminho.',
    aconteceu: (c) => c.campeao && c.jornada.some((b) => b.survivors < 3) },

  /* ---- Combate ---- */
  { id: 'c-um-golpe', nome: 'Um golpe só', categoria: 'Combate', dica: 'Acerte um único golpe de 600 de dano.',
    aconteceu: (c) => maiorFeito(c, 'explodiu') >= 600 },
  { id: 'c-relampago', nome: 'Nem deu tempo', categoria: 'Combate', dica: 'Vença uma luta em menos de 25 segundos.',
    aconteceu: (c) => c.venceu && c.battle.time < 25 },
  { id: 'c-intacto', nome: 'Sem um arranhão', categoria: 'Combate', dica: 'Vença com os três acima de 80% de Vida.',
    aconteceu: (c) => c.venceu && meuTrio(c).every((f) => f.hp / f.maxHp > 0.8) },
  { id: 'c-no-fio', nome: 'No fio da navalha', categoria: 'Combate', dica: 'Vença com um lutador abaixo de 5% de Vida.',
    aconteceu: (c) => c.venceu && meuTrio(c).some((f) => f.hp > 0 && f.hp / f.maxHp < 0.05) },
  { id: 'c-triplo', nome: 'Faxina', categoria: 'Combate', dica: 'Derrube os três inimigos com o mesmo lutador.',
    aconteceu: (c) => maiorFeito(c, 'abateu') >= 3 },
  { id: 'c-area', nome: 'Pega todo mundo', categoria: 'Combate', dica: 'Cause 900 de dano acertando vários inimigos de uma vez, numa luta só.',
    aconteceu: (c) => feito(c, 'area') >= 900 },

  /* ---- Sinergia ---- */
  { id: 's-ponte', nome: 'Primeira ponte', categoria: 'Sinergia', dica: 'Faça um lutador ajudar outro.',
    aconteceu: (c) => c.raioX.elos.length > 0 },
  { id: 's-mao-dupla', nome: 'Mão dupla', categoria: 'Sinergia', dica: 'Tenha uma dupla que se ajudou nas duas direções.',
    aconteceu: (c) => c.raioX.elos.some((a) => c.raioX.elos.some((b) => a.de === b.para && a.para === b.de)) },
  { id: 's-trio', nome: 'Trio afinado', categoria: 'Sinergia', dica: 'Faça os três pares se ajudarem nas duas direções, na mesma luta.',
    aconteceu: (c) => {
      const pares = new Set(c.raioX.elos
        .filter((a) => c.raioX.elos.some((b) => a.de === b.para && a.para === b.de))
        .map((e) => [e.de, e.para].sort().join('|')));
      return pares.size >= 3;
    } },
  { id: 's-assistencia', nome: 'Serviu na bandeja', categoria: 'Sinergia', dica: 'Abra um inimigo e deixe o aliado derrubar.',
    aconteceu: (c) => elos(c, 'finalizacao').length > 0 },
  { id: 's-guarda', nome: 'Guarda-costas', categoria: 'Sinergia', dica: 'Proteja o Preparo de um aliado.',
    aconteceu: (c) => elos(c, 'preparo-protegido').length > 0 },
  { id: 's-tempo', nome: 'Comprou tempo', categoria: 'Sinergia', dica: 'Trave um Preparo inimigo e dê folga ao trio.',
    aconteceu: (c) => elos(c, 'controle').length > 0 },

  /* ---- Experimentação ---- */
  { id: 'e-universos', nome: 'Três mundos', categoria: 'Experimentação', dica: 'Vença com um trio de três universos diferentes.',
    aconteceu: (c) => c.venceu && universos(c) === 3 },
  { id: 'e-estreia', nome: 'Cara nova', categoria: 'Experimentação', dica: 'Leve um lutador que você nunca usou.',
    aconteceu: (c) => c.time.some((id) => !c.vistos.includes(id)) },
  { id: 'e-trio-novo', nome: 'Tudo novo', categoria: 'Experimentação', dica: 'Leve três lutadores que você nunca usou, de uma vez.',
    aconteceu: (c) => c.time.every((id) => !c.vistos.includes(id)) },
  { id: 'e-mesmo-mundo', nome: 'Gente de casa', categoria: 'Experimentação', dica: 'Vença com os três do mesmo universo.',
    aconteceu: (c) => c.venceu && universos(c) === 1 },
  /*
   * Pedia um maior golpe de até 150, e nem o trio de menor ataque fica abaixo de 312.
   * Depois pediu 60 segundos — e em 4.000 lutas sorteadas a vitória mais longa
   * com os três vivos durou 55. Só um trio escolhido a dedo chegava lá. 45 é o
   * percentil 97 dessas vitórias, antes e depois da calibragem individual.
   */
  { id: 'e-sem-pressa', nome: 'Sem pressa', categoria: 'Experimentação', dica: 'Vença com os três vivos uma luta que passou de 45 segundos.',
    aconteceu: (c) => c.venceu && c.battle.time > 45 && meuTrio(c).every((f) => f.hp > 0) },

  /* ---- Vantagem ---- */
  { id: 'v-virada', nome: 'Virou o jogo', categoria: 'Vantagem', dica: 'Vença depois de ficar 30 pontos atrás na Vantagem.',
    aconteceu: (c) => c.venceu && c.maiorAtraso >= 30 },
  { id: 'v-virada-grande', nome: 'Ninguém dava nada', categoria: 'Vantagem', dica: 'Vença depois de ficar 45 pontos atrás.',
    aconteceu: (c) => c.venceu && c.maiorAtraso >= 45 },
  /* 65 é o percentil 90 das vitórias; 80, que esta conquista pedia antes, nunca aconteceu em 150 lutas. */
  { id: 'v-dominio', nome: 'Sem chance', categoria: 'Vantagem', dica: 'Termine uma luta com 65 pontos de Vantagem.',
    aconteceu: (c) => c.venceu && c.battle.dominion >= 65 },
  { id: 'v-sem-ceder', nome: 'Nunca atrás', categoria: 'Vantagem', dica: 'Vença sem ficar atrás na Vantagem um segundo sequer.',
    aconteceu: (c) => c.venceu && c.maiorAtraso === 0 },

  /* ---- Controle ---- */
  { id: 'k-corte', nome: 'Corte certeiro', categoria: 'Controle', dica: 'Interrompa uma habilidade durante o Preparo.',
    aconteceu: (c) => feito(c, 'interrompeu') >= 1 },
  { id: 'k-duplo', nome: 'Não deixa nem começar', categoria: 'Controle', dica: 'Interrompa três Preparos na mesma luta.',
    aconteceu: (c) => feito(c, 'interrompeu') >= 3 },
  { id: 'k-estatua', nome: 'Estátuas', categoria: 'Controle', dica: 'Mantenha inimigos travados por 20 segundos numa luta.',
    aconteceu: (c) => feito(c, 'controlou') >= 20 },
  { id: 'k-queima', nome: 'Deixa queimando', categoria: 'Controle', dica: 'Deixe inimigos perdendo Vida sozinhos por 25 segundos.',
    aconteceu: (c) => feito(c, 'continuo') >= 25 },
  { id: 'k-sozinho', nome: 'Carcereiro', categoria: 'Controle', dica: 'Trave inimigos por 15 segundos com um lutador só.',
    aconteceu: (c) => maiorFeito(c, 'controlou') >= 15 },

  /* ---- Proteção ---- */
  { id: 'p-escudo', nome: 'Primeiro escudo', categoria: 'Proteção', dica: 'Absorva 300 de dano com Escudo numa luta.',
    aconteceu: (c) => feito(c, 'protegeu') >= 300 },
  { id: 'p-muralha', nome: 'Muralha', categoria: 'Proteção', dica: 'Absorva 1.200 de dano com Escudo numa luta.',
    aconteceu: (c) => feito(c, 'protegeu') >= 1200 },
  { id: 'p-aguentou', nome: 'Saco de pancadas', categoria: 'Proteção', dica: 'Termine de pé depois de levar 2.000 de dano.',
    aconteceu: (c) => meuTrio(c).some((f) => f.hp > 0 && (c.feitos[f.characterId]?.aguentou ?? 0) >= 2000) },
  { id: 'p-dividiu', nome: 'Dividiu a dor', categoria: 'Proteção', dica: 'Termine uma luta com os três tendo levado dano parecido.',
    aconteceu: (c) => {
      const d = c.time.map((id) => c.feitos[id]?.aguentou ?? 0);
      return c.venceu && Math.min(...d) > 0 && Math.max(...d) <= Math.min(...d) * 1.6;
    } },

  /* ---- Cura ---- */
  { id: 'h-resgate', nome: 'Resgate', categoria: 'Cura', dica: 'Devolva 400 de Vida aos aliados numa luta.',
    aconteceu: (c) => feito(c, 'curou') >= 400 },
  { id: 'h-fonte', nome: 'Fonte', categoria: 'Cura', dica: 'Devolva 900 de Vida aos aliados numa luta.',
    aconteceu: (c) => feito(c, 'curou') >= 900 },
  { id: 'h-ninguem-cai', nome: 'Ninguém fica para trás', categoria: 'Cura', dica: 'Vença com os três vivos tendo curado o trio.',
    aconteceu: (c) => c.venceu && feito(c, 'curou') > 0 && meuTrio(c).every((f) => f.hp > 0) },
  { id: 'h-sem-cura', nome: 'Na raça', categoria: 'Cura', dica: 'Vença com os três vivos e nenhuma cura.',
    aconteceu: (c) => c.venceu && feito(c, 'curou') === 0 && meuTrio(c).every((f) => f.hp > 0) },

  /* ---- Personagens ---- */
  { id: 'r-dez', nome: 'Dez conhecidos', categoria: 'Personagens', dica: 'Leve dez lutadores diferentes para a arena.',
    aconteceu: (c) => new Set([...c.vistos, ...c.time]).size >= 10 },
  { id: 'r-cinquenta', nome: 'Cinquenta vozes', categoria: 'Personagens', dica: 'Leve cinquenta lutadores diferentes.',
    aconteceu: (c) => new Set([...c.vistos, ...c.time]).size >= 50 },
  { id: 'r-cem', nome: 'Cem estilos', categoria: 'Personagens', dica: 'Leve cem lutadores diferentes.',
    aconteceu: (c) => new Set([...c.vistos, ...c.time]).size >= 100 },
  { id: 'r-todos', nome: 'O elenco inteiro', categoria: 'Personagens', dica: 'Leve os 250 para a arena.',
    aconteceu: (c) => new Set([...c.vistos, ...c.time]).size >= 250 },
  { id: 'r-mestre', nome: 'Primeiro mestre', categoria: 'Personagens', dica: 'Chegue à Maestria III com um lutador.',
    aconteceu: (c) => c.dominados >= 1 },
  { id: 'r-dez-mestres', nome: 'Dez mestres', categoria: 'Personagens', dica: 'Chegue à Maestria III com dez lutadores.',
    aconteceu: (c) => c.dominados >= 10 },

  /* ---- Segredos ---- */
  { id: 'x-teto', nome: 'No limite', categoria: 'Segredos', secreta: true, dica: 'Mantenha o próprio reforço ativo por 60 segundos numa luta só.',
    aconteceu: (c) => maiorFeito(c, 'acumulou') >= 60 },
  /*
   * A versão anterior pedia vencer sem nenhuma habilidade sair, e isso não
   * acontece: as habilidades disparam sozinhas quando a Carga enche. Zero em
   * 211 vitórias medidas. Esta pede carregar o trio nas costas, que acontece.
   */
  { id: 'x-solo', nome: 'Carregou nas costas', categoria: 'Segredos', secreta: true, dica: 'Vença com um lutador causando mais dano que os outros dois juntos.',
    aconteceu: (c) => {
      const d = meuTrio(c).map((f) => f.stats.damage).sort((a, b) => b - a);
      return c.venceu && d.length === 3 && d[0]! > d[1]! + d[2]!;
    } },
  { id: 'x-um-por-cento', nome: 'Um fio de vida', categoria: 'Segredos', secreta: true, dica: 'Vença com um lutador com 1% de Vida.',
    aconteceu: (c) => c.venceu && meuTrio(c).some((f) => f.hp > 0 && f.hp / f.maxHp <= 0.01) },
  { id: 'x-maratona', nome: 'Isso não acaba', categoria: 'Segredos', secreta: true, dica: 'Passe de 100 segundos numa luta.',
    aconteceu: (c) => c.battle.time > 100 },
  { id: 'x-sozinho', nome: 'O último de pé', categoria: 'Segredos', secreta: true, dica: 'Vença com só um lutador vivo e os outros dois caídos.',
    aconteceu: (c) => c.venceu && meuTrio(c).filter((f) => f.hp > 0).length === 1 },
  { id: 'x-carga', nome: 'Motor do trio', categoria: 'Segredos', secreta: true, dica: 'Encha 400% de Carga dos aliados numa luta.',
    aconteceu: (c) => feito(c, 'carregou') >= 400 },
];

/** As conquistas novas desta batalha. */
export const conquistasDaBatalha = (c: Contexto, jaTem: readonly string[]): string[] =>
  conquistas.filter((x) => !jaTem.includes(x.id) && x.aconteceu(c)).map((x) => x.id);

export const categorias: readonly Categoria[] = [
  'Jornada', 'Combate', 'Sinergia', 'Experimentação', 'Vantagem',
  'Controle', 'Proteção', 'Cura', 'Personagens', 'Segredos',
];
