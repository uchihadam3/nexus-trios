import { describe, expect, it } from 'vitest';
import { byId, characters } from '../src/data/characters';
import { forcaDoTrio, generateCampaign, newDraft } from '../src/engine/campaign';
import { CUSTO_DAS_DICAS, pontosDaLuta } from '../src/engine/pontos';
import { replayRanked } from '../src/engine/ranked';
import { createBattle, stepBattle } from '../src/engine/battle';
import { pontoFraco } from '../src/data/ponto-fraco';
import { dicasDoDraft } from '../src/presentation/dicas-do-trio';

const ids = characters.map((c) => c.id);

describe('Dicas de trio', () => {
  it('marca uma só melhor escolha, a de maior encaixe, com motivos curtos', () => {
    for (let seed = 1; seed <= 40; seed++) {
      const d = newDraft(seed), time = ids.filter((id) => !d.candidates.includes(id)).slice(seed % 50, seed % 50 + (seed % 3));
      const dicas = dicasDoDraft(d.candidates, time);
      expect(dicas.filter((x) => x.melhor)).toHaveLength(1);
      const melhor = dicas.find((x) => x.melhor)!;
      for (const x of dicas) {
        expect(x.encaixe).toBeGreaterThanOrEqual(0);
        expect(x.encaixe).toBeLessThanOrEqual(99);
        expect(x.curtos.length).toBeGreaterThan(0);
        expect(x.curtos.length).toBeLessThanOrEqual(2);
        expect(x.detalhe.length).toBeGreaterThanOrEqual(x.curtos.length);
        expect(melhor.encaixe).toBeGreaterThanOrEqual(x.encaixe);
      }
    }
  });

  it('pensa no trio inteiro: a melhor escolha é a que deixa o trio mais forte com todos que já estão nele', () => {
    const time = ['naruto', 'sakura'], candidatos = ids.filter((id) => !time.includes(id)).slice(0, 3);
    const melhor = dicasDoDraft(candidatos, time).find((x) => x.melhor)!.id;
    const nota = (id: string) => forcaDoTrio([...time, id]);
    expect(Math.max(...candidatos.map(nota))).toBe(nota(melhor));
  });

  /*
   * Seguir a dica tem que ganhar mais (pedido do jogador: "mais inteligente
   * tem que saber qual é melhor e por quê"). Um robô monta o trio pegando a
   * melhor escolha da dica entre três sorteados, outro pega um dos três ao
   * acaso; os dois enfrentam os mesmos rivais.
   */
  it('quem segue a dica monta trios que vencem mais do que quem escolhe ao acaso', () => {
    let r = 77;
    const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
    const sorteia = (fora: string[], n: number) => { const o: string[] = []; while (o.length < n) { const x = ids[Math.floor(rnd() * ids.length)]!; if (!o.includes(x) && !fora.includes(x)) o.push(x); } return o; };
    let comDica = 0, aoAcaso = 0;
    for (let jogo = 0; jogo < 70; jogo++) {
      const rivais = sorteia([], 3);
      const dica: string[] = [], acaso: string[] = [];
      for (let vez = 0; vez < 3; vez++) {
        const tres = sorteia([...rivais, ...dica, ...acaso], 3);
        dica.push(dicasDoDraft(tres, dica, rivais).find((x) => x.melhor)!.id);
        acaso.push(tres[Math.floor(rnd() * 3)]!);
      }
      for (const [time, soma] of [[dica, 1], [acaso, 0]] as const) {
        const luta = createBattle([...time], rivais, 1000 + jogo, 1);
        for (let t = 0; t < 9000 && !luta.finished; t++) stepBattle(luta);
        if (luta.winner === 'player') { if (soma) comDica++; else aoAcaso++; }
      }
    }
    expect(comDica).toBeGreaterThan(aoAcaso + 5);
  });

  it('a explicação diz o porquê com as habilidades de verdade', () => {
    const d = dicasDoDraft(['sakura'], ['raidenmk'])[0]!;
    const comPorque = d.detalhe.filter((m) => m.porque);
    expect(comPorque.length).toBeGreaterThan(0);
    // cita uma habilidade do Raiden e diz o que ela faz pela Sakura
    expect(comPorque.some((m) => /Barreira elétrica de Raiden/.test(m.porque!))).toBe(true);
  });

  it('o cuidado do draft é o ponto fraco do próprio personagem, com o porquê', () => {
    const ids = characters.slice(0, 6).map((c) => c.id);
    for (const d of dicasDoDraft(ids.slice(0, 3), [])) {
      const f = pontoFraco(byId[d.id]!)[0]!;
      expect(d.detalhe.map((x) => x.texto).some((t) => t.startsWith(`Cuidado: ${f.rotulo.charAt(0).toLowerCase()}`) && !/fraco contra/.test(t))).toBe(true);
    }
  });
  it('custa 25 mil por luta, aparece na conta e a luta nunca fica negativa', () => {
    const [a, b] = generateCampaign(5).map((e) => e.team);
    const luta = createBattle(a!, b!, 5, 1);
    for (let t = 0; t < 9000 && !luta.finished; t++) stepBattle(luta);
    const sem = pontosDaLuta(luta, 3), com = pontosDaLuta(luta, 3, true);
    expect(com.parcelas.at(-1)).toEqual({ id: 'ajuda', rotulo: 'Dicas de trio', valor: -CUSTO_DAS_DICAS });
    expect(com.total).toBe(Math.max(0, sem.total - CUSTO_DAS_DICAS));
    expect(CUSTO_DAS_DICAS).toBe(10_000);
  });

  it('o servidor desconta as dicas em cada luta jogada', () => {
    const seed = 2024, livres = ids.filter((id) => !generateCampaign(seed).some((e) => e.team.includes(id)));
    const trio = livres.slice(0, 3);
    const sem = replayRanked(trio, seed, true), com = replayRanked(trio, seed, true, true);
    expect(com.summaries.map((s) => s.won)).toEqual(sem.summaries.map((s) => s.won));
    expect(com.score).toBe(sem.summaries.reduce((n, s) => n + Math.max(0, (s.pontos!.total) - CUSTO_DAS_DICAS), 0));
    expect(com.highlights.dicas).toBe(true);
  });
});
