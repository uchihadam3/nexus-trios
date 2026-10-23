/*
 * As Dicas e a posição da tela concordam (pedido do dono: "garantir que as posições lá nas dicas sejam tudo correto"): com dois
 * já no trio, a melhor escolha das Dicas é a que dá a melhor posição na tela, e quem dá posição melhor tem encaixe maior.
 */
import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import * as posicoes from '../src/data/posicoes-dos-trios';
import * as medido from '../src/data/topo-medido';
import { dicasDoDraft } from '../src/presentation/dicas-do-trio';
import { montarRanking, montarTopoMedido, posicaoDoTime } from '../src/presentation/posicao-do-trio';

const ranking = montarRanking(posicoes.DE, posicoes.CONTAS, posicoes.TOTAL_DE_TRIOS), topo = montarTopoMedido(medido.IDS, medido.TRIOS);
const lugar = (t: string[]) => posicaoDoTime(t, ranking, topo), ids = characters.map((c) => c.id);

describe('as Dicas e a posição da tela', () => {
  it('a melhor escolha do terceiro é a de melhor posição', () => {
    let s = 9;
    const sorteia = () => { s = (s * 1103515245 + 12345) % 2147483648; return ids[s % ids.length]!; };
    for (let k = 0; k < 40; k++) {
      const time = [sorteia(), sorteia()], cands = [sorteia(), sorteia(), sorteia()].filter((id) => !time.includes(id));
      if (new Set(time).size < 2 || new Set(cands).size < cands.length || cands.length < 2) continue;
      const d = dicasDoDraft(cands, time, [], lugar), melhor = d.find((x) => x.melhor)!;
      expect(lugar([...time, melhor.id])).toBe(Math.min(...cands.map((c) => lugar([...time, c]))));
      for (const a of d) for (const b of d) if (lugar([...time, a.id]) < lugar([...time, b.id])) expect(a.encaixe).toBeGreaterThanOrEqual(b.encaixe);
    }
  });
});
