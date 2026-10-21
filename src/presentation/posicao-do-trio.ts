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

let carregando: Promise<Ranking> | undefined;
export const carregarRanking = () => (carregando ??= import('../data/posicoes-dos-trios').then((m) => montarRanking(m.DE, m.CONTAS, m.TOTAL_DE_TRIOS)));

/** A posição do time (1 = o melhor trio de todos) e quantos trios existem; null enquanto carrega. */
export function usePosicaoDoTrio(team: readonly string[]): { posicao: number; total: number } | null {
  const [ranking, setRanking] = useState<Ranking | null>(null);
  useEffect(() => { let vivo = true; void carregarRanking().then((r) => { if (vivo) setRanking(r); }).catch(() => {}); return () => { vivo = false; }; }, []);
  return ranking && team.length === 3 ? { posicao: ranking.posicaoDaNota(notaDoTrio(team)), total: ranking.total } : null;
}

/** "1.234º" (pedido do dono: "não precisa colocar de 10 milhões, só a posição") */
export const textoDaPosicao = (posicao: number) => `${posicao.toLocaleString('pt-BR')}º`;
