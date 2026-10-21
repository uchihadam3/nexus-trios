import { useEffect, useState } from 'react';
import { notaDoTrio } from './dicas-do-trio';

/*
 * A posição exata do time entre todos os trios possíveis (pedido do dono: "se o time está na posição 99,999… ou mesmo
 * aparece a posição dele na frente depois das porcentagens"). A contagem de trios por nota (src/data/posicoes-dos-trios.ts,
 * ~30 KB) só é baixada quando a tela das estrelas abre; até lá, a posição não aparece.
 */
export interface Ranking { total: number; posicaoDaNota: (nota: number) => number }

/** Monta o ranking a partir das contagens: a posição de uma nota é 1 + quantos trios têm nota maior (empate divide o lugar). */
export function montarRanking(de: number, contas: string, total: number): Ranking {
  const n = contas.split(',').map((c) => parseInt(c, 36));
  // acima[i]: quantos trios têm nota acima do milésimo de + i
  const acima = new Array<number>(n.length);
  for (let i = n.length - 1, s = 0; i >= 0; i--) { acima[i] = s; s += n[i]!; }
  return {
    total,
    posicaoDaNota: (nota) => {
      const i = Math.round(nota * 1000) - de;
      return i < 0 ? total : i >= n.length ? 1 : acima[i]! + 1;
    },
  };
}

/*
 * Os trios do topo que já lutaram de verdade (src/data/topo-medido.ts, plano topo da fábrica): a posição deles é a da luta,
 * não a da nota (pedido do dono: "ver se eles estão lá mesmo"). Eles são os M primeiros pela nota; quem não lutou ainda
 * fica com a posição da nota, nunca acima deles.
 */
export interface TopoMedido { lugar: Map<string, number>; medidos: number }
const chave = (team: readonly string[]) => [...team].sort().join('+');
export function montarTopoMedido(ids: string, trios: string): TopoMedido {
  const lista = ids.split(','), lugar = new Map<string, number>();
  for (let n = 0; n * 6 < trios.length; n++) {
    const t = [0, 2, 4].map((o) => lista[parseInt(trios.slice(n * 6 + o, n * 6 + o + 2), 36)]!);
    lugar.set(chave(t), n + 1);
  }
  return { lugar, medidos: lugar.size };
}
/** A posição do time: a medida em luta de verdade (se ele é do topo que já lutou) ou a da nota. */
export function posicaoDoTime(team: readonly string[], ranking: Ranking, topo?: TopoMedido): number {
  const medida = topo?.lugar.get(chave(team));
  if (medida) return medida;
  const pelaNota = ranking.posicaoDaNota(notaDoTrio(team));
  return topo ? Math.max(pelaNota, topo.medidos + 1) : pelaNota;
}

let carregando: Promise<{ ranking: Ranking; topo: TopoMedido }> | undefined;
export const carregarRanking = () => (carregando ??= Promise.all([import('../data/posicoes-dos-trios'), import('../data/topo-medido')])
  .then(([m, t]) => ({ ranking: montarRanking(m.DE, m.CONTAS, m.TOTAL_DE_TRIOS), topo: montarTopoMedido(t.IDS, t.TRIOS) })));

/** A posição do time (1 = o melhor trio de todos) e quantos trios existem; null enquanto carrega. */
export function usePosicaoDoTrio(team: readonly string[]): { posicao: number; total: number } | null {
  const [dados, setDados] = useState<{ ranking: Ranking; topo: TopoMedido } | null>(null);
  useEffect(() => { let vivo = true; void carregarRanking().then((r) => { if (vivo) setDados(r); }).catch(() => {}); return () => { vivo = false; }; }, []);
  return dados && team.length === 3 ? { posicao: posicaoDoTime(team, dados.ranking, dados.topo), total: dados.ranking.total } : null;
}

/** "1.234º" (pedido do dono: "não precisa colocar de 10 milhões, só a posição") */
export const textoDaPosicao = (posicao: number) => `${posicao.toLocaleString('pt-BR')}º`;
