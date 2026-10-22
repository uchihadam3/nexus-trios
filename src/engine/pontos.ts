/*
 * Os pontos de cada luta — os mesmos do ranking.
 *
 * Pedidos do jogador, em ordem:
 *   - "sempre dá ~1 milhão por batalha; tem que variar, e a derrota também
 *     pontua o que você fez nela";
 *   - escala de ~10 mil (derrota feia) a ~180 mil (luta incrível);
 *   - "os pontos têm que vir dos feitos na batalha, e não da vitória em si":
 *     a vitória vale só 25 mil, fixos;
 *   - "balanceados, para que todos os personagens que jogarem bem pontuem
 *     parecido".
 *
 * Feitos de cada lutador do trio: dano, nocautes, cura e proteção,
 * habilidades e cortes, Status no rival e no trio, adiantar/atrasar ação,
 * Carga dada a aliados e investigação. Os pesos dão a cada tipo de feito a
 * sua parte da luta (o dano não engole o resto). Por cima, cada personagem
 * tem um fator medido em lutas simuladas (src/data/pontos-por-personagem.ts,
 * scripts/equilibrar-pontos.ts): quem tem um kit que gera pouco número
 * "visível" (controle, investigação, apoio) é corrigido para cima, e quem
 * gera muito, para baixo — então o jogo típico de qualquer personagem rende
 * parecido, e jogar acima disso rende mais.
 *
 * Cura e proteção contam inteiras, sem teto na luta (pedido do jogador: "eu não queria limitar desse jeito…
 * reduzir os pontos de alguns personagens, o tanto de ponto que eles fazem curando e protegendo"): quem cura ou
 * protege muito mais que os outros tem um peso próprio nisso (src/data/peso-da-cura.ts, scripts/peso-da-cura.ts),
 * que traz a média dele por luta para PESO_DA_CURA_ALVO. Numa luta normal isso tira pouco (a Orihime, a que mais
 * cura, perde uns 6% da jornada média e continua entre as que mais pontuam).
 *
 * E a luta que se arrasta rende menos por segundo: os feitos da luta toda contam inteiros até LUTA.cheio e, acima
 * disso, LUTA.acima de cada ponto. Uma luta normal dá uns 30 mil de feitos e dura uns 30 s; o trio de curandeiros
 * que ninguém derruba arrasta a luta por 100–300 s e passava de 5 milhões na jornada. Com LUTA.acima em 42% (era
 * 10%), a luta longa ainda vale muito: 2 milhões fica difícil mas possível para os trios mais fortes (1 jornada em
 * ~9) e 2,5 milhões só com muita sorte (1 em ~3.000), sem facilitar o 1,4 milhão das Dicas (pedido do jogador:
 * "chegar até uns 2 milhões, difícil, mas consegue… 2 milhões e meio… muita sorte… sem ficar mais fácil pra chegar
 * no 1 milhão e 400").
 *
 * Também contam: manter o trio vivo (Vida que sobrou e quem ficou de pé) e
 * virar o Domínio. Os feitos crescem com a altura da jornada (luta 10 ×1,45).
 * A jornada é a soma das lutas; a derrota encerra, mas os pontos dela ficam.
 *
 * As estrelas dos pontos (src/data/estrelas-de-pontos.ts): 120 personagens que, no trio, somam o bônus deles aos
 * pontos de cada luta (o maior do trio). Só os pontos: a luta não muda.
 *
 * Quem liga as Dicas de trio na escolha (src/presentation/dicas-do-trio.ts)
 * paga CUSTO_DAS_DICAS em cada luta da jornada: as dicas ensinam, mas o
 * ranking premia quem monta o trio sozinho.
 *
 * O servidor (src/engine/ranked.ts, replayRanked) usa exatamente esta conta.
 */
import type { Battle, Fighter } from './types';
import { FATOR_DE_PONTOS } from '../data/pontos-por-personagem';
import { PESO_DA_CURA } from '../data/peso-da-cura';
import { ESTRELAS_DE_PONTOS, bonusDoTrio } from '../data/estrelas-de-pontos';
import { byId } from '../data/characters';
import { LOCALE } from '../i18n/idioma';

export type ParcelaId = 'dano' | 'nocautes' | 'apoio' | 'jogadas' | 'efeitos' | 'viradas' | 'vida' | 'vitoria' | 'estrela' | 'ajuda' | 'colecao';
export interface Parcela { id: ParcelaId; rotulo: string; valor: number }

export interface PontosDaLuta {
  total: number;
  /** As parcelas da luta, na ordem de exibição. */
  parcelas: Parcela[];
  /** O multiplicador da luta (1 na primeira, cresce a cada luta). */
  multiplicador: number;
  /** Quantos de pé e a Vida média, para o texto. */
  de_pe: number;
  vidaMedia: number;
}

/** Quanto vale cada unidade de feito (antes do fator do personagem). */
export const FEITOS = {
  porDano: 3.3,
  porNocaute: 1_450,
  porApoio: 8.5,
  porHabilidade: 370,
  porCorte: 4_250,
  /** por segundo de Status ruim posto no rival */
  porDebuff: 22,
  /** por segundo de Status bom posto no trio */
  porBuff: 14,
  /** por barra de ação adiantada (aliado) ou atrasada (rival) */
  porTempo: 1_800,
  /** por ponto de Carga dado a aliados */
  porCarga: 8.5,
  /** por ponto de investigação */
  porInvestigacao: 30,
} as const;

export const PONTOS = {
  porVirada: 2_500,
  viradasMaximo: 10_000,
  /** Manter o trio vivo é um feito: a Vida que sobrou e quem ficou de pé. */
  vidaMaxima: 62_000,
  porSobrevivente: 1_000,
  /** A vitória em si vale só isto, fixo: o resto vem do que o trio fez. */
  vitoria: 25_000,
  /** Quanto cada luta da jornada multiplica os feitos (luta 10 = ×1,45). */
  porLuta: 0.05,
} as const;

/** A média de cura e proteção por luta (em pontos, já com o fator) a que o peso de cada curandeiro leva. */
export const PESO_DA_CURA_ALVO = 3_000;

/** Os feitos da luta (já com o fator e o peso da cura de cada personagem): inteiros até `cheio`, e daí para cima `acima` de cada ponto. */
export const LUTA = { cheio: 35_000, acima: 0.42 } as const;
export const feitosDaLuta = (bruto: number) => (bruto <= LUTA.cheio ? bruto : LUTA.cheio + (bruto - LUTA.cheio) * LUTA.acima);

/** O que cada luta custa a quem montou o trio com as Dicas de trio ligadas. */
export const CUSTO_DAS_DICAS = 10_000;
/*
 * A Jornada com os seus (pedido do jogador: "fazer uma jornada com os personagens que você tem… cada luta vale 30 mil
 * pontos a menos"): o trio escolhido entre os personagens já liberados nas Conquistas, sem o bônus das estrelas de
 * pontos, e cada luta custa isto.
 */
export const CUSTO_DA_COLECAO = 30_000;

export const multiplicadorDaLuta = (indice: number) => 1 + PONTOS.porLuta * Math.max(0, indice);

/** Os feitos de um lutador, por tipo, sem o fator do personagem (usado também para medir o fator); a cura e a proteção já com o peso dele. */
export function feitosDoLutador(f: Fighter): Record<'dano' | 'nocautes' | 'apoio' | 'jogadas' | 'efeitos', number> {
  const s = f.stats;
  const investigacao = Object.values(f.investigation ?? {}).reduce((n, v) => n + v, 0);
  return {
    dano: s.damage * FEITOS.porDano,
    nocautes: s.kills * FEITOS.porNocaute,
    apoio: (s.healing + s.protection) * FEITOS.porApoio * (PESO_DA_CURA[f.characterId] ?? 1),
    jogadas: s.skills * FEITOS.porHabilidade + s.interrupts * FEITOS.porCorte,
    efeitos: (s.debuffs ?? 0) * FEITOS.porDebuff + (s.buffs ?? 0) * FEITOS.porBuff + (s.tempo ?? 0) * FEITOS.porTempo
      + (s.carga ?? 0) * FEITOS.porCarga + investigacao * FEITOS.porInvestigacao,
  };
}

/** `colecao`: a Jornada com os seus (sem o bônus das estrelas de pontos; cada luta custa CUSTO_DA_COLECAO). */
export function pontosDaLuta(battle: Battle, indice = 0, dicas = false, colecao = false): PontosDaLuta {
  const trio = battle.fighters.filter((f) => f.side === 'player');
  const de_pe = trio.filter((f) => f.hp > 0).length;
  const vidaMedia = Math.max(0, Math.min(1, trio.reduce((n, f) => n + f.hp / f.maxHp, 0) / 3));
  const venceu = battle.winner === 'player';
  const m = multiplicadorDaLuta(indice);
  const soma = { dano: 0, nocautes: 0, apoio: 0, jogadas: 0, efeitos: 0 };
  for (const f of trio) {
    const fator = FATOR_DE_PONTOS[f.characterId] ?? 1;
    const x = feitosDoLutador(f);
    for (const k of Object.keys(soma) as (keyof typeof soma)[]) soma[k] += x[k] * fator;
  }
  // o que a luta longa rende a menos vale igual para cada tipo de feito, e a ficha mostra a parte de cada um
  const bruto = soma.dano + soma.nocautes + soma.apoio + soma.jogadas + soma.efeitos;
  const corte = bruto > 0 ? feitosDaLuta(bruto) / bruto : 1;
  const brutas: [ParcelaId, string, number][] = [
    ['dano', 'Dano causado', soma.dano * corte * m],
    ['nocautes', 'Nocautes', soma.nocautes * corte * m],
    ['apoio', 'Cura e proteção', soma.apoio * corte * m],
    ['jogadas', 'Habilidades e cortes', soma.jogadas * corte * m],
    ['efeitos', 'Status, ritmo e Carga', soma.efeitos * corte * m],
    ['viradas', 'Viradas', Math.min(PONTOS.viradasMaximo, (battle.viradasDoTrio ?? 0) * PONTOS.porVirada) * m],
    ['vida', `Trio vivo · ${de_pe} de pé`, (vidaMedia * PONTOS.vidaMaxima + de_pe * PONTOS.porSobrevivente) * m],
    ['vitoria', 'Vitória', venceu ? PONTOS.vitoria : 0],
  ];
  const parcelas = brutas.map(([id, rotulo, v]) => ({ id, rotulo, valor: Math.round(v) })).filter((p) => p.valor > 0);
  // a estrela do trio (src/data/estrelas-de-pontos.ts): soma o bônus dela aos pontos da luta, antes do custo das Dicas
  // (na Jornada com os seus o bônus não vale: pedido do jogador)
  const estrela: { bonus: number; de?: string } = colecao ? { bonus: 0 } : bonusDoTrio(trio.map((f) => f.characterId));
  if (estrela.de) {
    const base = parcelas.reduce((n, p) => n + p.valor, 0), e = ESTRELAS_DE_PONTOS[estrela.de]!;
    const valor = Math.round(base * estrela.bonus);
    if (valor > 0) parcelas.push({ id: 'estrela', rotulo: `${'★'.repeat(e.estrelas)} ${byId[estrela.de]?.name ?? estrela.de} +${e.bonus}%`, valor });
  }
  if (dicas) parcelas.push({ id: 'ajuda', rotulo: 'Dicas de trio', valor: -CUSTO_DAS_DICAS });
  if (colecao) parcelas.push({ id: 'colecao', rotulo: 'Jornada com os seus', valor: -CUSTO_DA_COLECAO });
  // a luta nunca vale menos que zero
  return { total: Math.max(0, parcelas.reduce((n, p) => n + p.valor, 0)), parcelas, multiplicador: m, de_pe, vidaMedia };
}

/** A pontuação da jornada: a soma das lutas jogadas (vencidas ou não). */
export function pontosDaJornada(lutas: readonly { pontos?: number; won: boolean }[]): number {
  return lutas.reduce((n, l) => n + Math.max(0, l.pontos ?? 0), 0);
}

export const formatarPontos = (n: number) => Math.round(n).toLocaleString(LOCALE);
