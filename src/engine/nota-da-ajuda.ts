/*
 * A nota de cada ajuda do "Quem ajudou quem" (pedido do jogador: "foi boa essa ajuda? … muito ruim, ruim, na média,
 * bom, muito bom, excelente… pra pessoa bater o olho e entender na hora").
 *
 * Cada ajuda é comparada com as do mesmo tipo em lutas sorteadas (scripts/medir-ajudas.ts →
 * regua-das-ajudas.ts): a nota diz em que faixa ela ficou. O número comparado é o mesmo que a tela mostra.
 */
import type { Direcao, TipoDeElo } from './raio-x';
import { REGUA_DAS_AJUDAS } from './regua-das-ajudas';

/** O quanto a ajuda rendeu: a % de Carga, a Vida, o Escudo e os Status tirados pelo valor; o resto pelas vezes. */
const PELO_VALOR = new Set<TipoDeElo>(['carga', 'cura', 'escudo', 'purificou']);
export function medidaDaAjuda(d: Direcao): { tipo: string; valor: number } | null {
  const e = d.elos[0];
  if (!e || !d.tipo || d.tipo === 'conflito') return null;
  return { tipo: d.tipo, valor: PELO_VALOR.has(d.tipo) ? e.valor : e.vezes };
}

export type NotaDaAjuda = 0 | 1 | 2 | 3 | 4 | 5;
export const NOMES_DAS_NOTAS = ['Muito ruim', 'Ruim', 'Na média', 'Boa', 'Muito boa', 'Excelente'] as const;
/* Ajudas que decidem a luta (derrubar junto, salvar um Preparo, levantar quem caiu) nunca ficam abaixo de "Boa". */
const DECIDE = new Set(['finalizacao', 'preparo-protegido', 'levantou']);
/** A nota e quanto das ajudas iguais ficaram abaixo desta ("melhor que 72% das ajudas assim"). */
export interface AvaliacaoDaAjuda { nota: NotaDaAjuda; melhorQue: number }
/** A faixa da ajuda na régua: abaixo de 10% muito ruim, 30% ruim, 60% na média, 80% boa, 95% muito boa; acima, excelente. */
export function avaliarAjuda(tipo: string, valor: number): AvaliacaoDaAjuda | null {
  const r = REGUA_DAS_AJUDAS[tipo];
  if (!r) return DECIDE.has(tipo) ? { nota: 3, melhorQue: 60 } : null;
  // a posição no meio dos empates: muitas ajudas valem "1 vez", e 1 vez não pode ser ao mesmo tempo o pior e o melhor
  const abaixo = r.filter((x) => x < valor).length, igual = r.filter((x) => x === valor).length;
  const pos = (abaixo + igual / 2) / r.length;
  const n = (pos < 0.1 ? 0 : pos < 0.3 ? 1 : pos < 0.6 ? 2 : pos < 0.8 ? 3 : pos < 0.95 ? 4 : 5) as NotaDaAjuda;
  return { nota: DECIDE.has(tipo) ? (Math.max(3, n) as NotaDaAjuda) : n, melhorQue: Math.round(Math.min(99, pos * 100)) };
}
export const notaPelaRegua = (tipo: string, valor: number): NotaDaAjuda | null => avaliarAjuda(tipo, valor)?.nota ?? null;
export const avaliarDirecao = (d: Direcao): AvaliacaoDaAjuda | null => {
  const m = medidaDaAjuda(d);
  return m ? avaliarAjuda(m.tipo, m.valor) : null;
};
