import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { forcaDoTrio, generateCampaign, newDraft } from '../src/engine/campaign';
import { CUSTO_DAS_DICAS, pontosDaLuta } from '../src/engine/pontos';
import { replayRanked } from '../src/engine/ranked';
import { createBattle, stepBattle } from '../src/engine/battle';
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

  it('custa 15 mil por luta, aparece na conta e a luta nunca fica negativa', () => {
    const [a, b] = generateCampaign(5).map((e) => e.team);
    const luta = createBattle(a!, b!, 5, 1);
    for (let t = 0; t < 9000 && !luta.finished; t++) stepBattle(luta);
    const sem = pontosDaLuta(luta, 3), com = pontosDaLuta(luta, 3, true);
    expect(com.parcelas.at(-1)).toEqual({ id: 'ajuda', rotulo: 'Dicas de trio', valor: -CUSTO_DAS_DICAS });
    expect(com.total).toBe(Math.max(0, sem.total - CUSTO_DAS_DICAS));
    expect(CUSTO_DAS_DICAS).toBe(15_000);
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
