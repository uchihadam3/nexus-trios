/*
 * O botão "Melhor no Time" do PvP (src/presentation/melhor-time.ts): o time que ele monta tem que ser o de melhor posição
 * que aparece na tela (pedido do dono: "ele me falou que era o melhor, eu troquei e ficou melhor ainda").
 */
import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import * as posicoes from '../src/data/posicoes-dos-trios';
import * as medido from '../src/data/topo-medido';
import { melhorTimeAqui } from '../src/presentation/melhor-time';
import { montarRanking, montarTopoMedido, posicaoDoTime } from '../src/presentation/posicao-do-trio';

const ranking = montarRanking(posicoes.DE, posicoes.CONTAS, posicoes.TOTAL_DE_TRIOS), topo = montarTopoMedido(medido.IDS, medido.TRIOS);
const todos = characters.map((c) => c.id), lugar = (t: string[]) => posicaoDoTime(t, ranking, topo);

describe('o botão de montar o melhor time', () => {
  it('com o time vazio, monta o 1º da tela', () => {
    expect(lugar(melhorTimeAqui(todos, [], new Set(), topo)!)).toBe(1);
  });
  it('sem quem está nos outros times, monta o melhor que sobra', () => {
    const primeiro = melhorTimeAqui(todos, [], new Set(), topo)!, outros = new Set(primeiro);
    const t = melhorTimeAqui(todos, [], outros, topo)!;
    expect(t.some((id) => outros.has(id))).toBe(false);
    // nenhum trio de posição melhor dá para montar sem os três do primeiro
    const melhores = [...topo.lugar.keys()].slice(0, lugar(t) - 1);
    expect(melhores.every((k) => k.split('+').some((id) => outros.has(id)))).toBe(true);
  });
  it('com um ou dois no time, completa com a melhor posição que tem eles', () => {
    for (const fixos of [['goku'], ['pikachu'], ['goku', 'naruto']]) {
      const t = melhorTimeAqui(todos, fixos, new Set(), topo)!;
      expect(t.slice(0, fixos.length)).toEqual(fixos);
      const comEles = [...topo.lugar.keys()].map((k) => k.split('+')).filter((x) => fixos.every((id) => x.includes(id)));
      if (comEles.length) expect(lugar(t)).toBe(Math.min(...comEles.map(lugar)));
    }
  });
  it('sem a lista do topo (ou fora dela), vai pela nota e não repete ninguém', () => {
    const poucos = todos.slice(0, 12), t = melhorTimeAqui(poucos, [], new Set(), topo)!;
    expect(new Set(t).size).toBe(3);
    expect(t.every((id) => poucos.includes(id))).toBe(true);
  });
});
