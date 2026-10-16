import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { generateCampaign } from '../src/engine/campaign';
import { replayRanked } from '../src/engine/ranked';
import { LUTA_ESTRELA, LUTA_ONZE, SEGREDOS, proximaLuta, rivalSecreto, segredosCumpridos, type LutaDoSegredo } from '../src/engine/segredos';

/* Os seis segredos e as lutas extras (src/engine/segredos.ts). */
const luta = (index: number, won = true, x: Partial<LutaDoSegredo> = {}): LutaDoSegredo => ({ index, won, time: 40, survivors: 2, ...x });
const ate = (n: number, x: Partial<LutaDoSegredo> = {}) => Array.from({ length: n }, (_, i) => luta(i, true, x));
/* um trio de 3 estrelas, de universos diferentes: nenhum segredo vem de graça */
const trioComum = ['gojo', 'light', 'saitama'];

describe('segredos', () => {
  it('são seis: dois abrem a luta ★, dois a luta 11 e dois as duas', () => {
    expect(SEGREDOS).toHaveLength(6);
    const so = (q: string[]) => SEGREDOS.filter((s) => s.libera.join() === q.join()).length;
    expect([so(['estrela']), so(['onze']), so(['estrela', 'onze'])]).toEqual([2, 2, 2]);
  });

  it('sem segredo, a jornada são as 10 lutas de sempre', () => {
    expect(proximaLuta(trioComum, [])).toBe(0);
    expect(proximaLuta(trioComum, ate(5))).toBe(5);
    expect(proximaLuta(trioComum, ate(10))).toBeNull();
    expect(proximaLuta(trioComum, [...ate(3), luta(3, false)])).toBeNull();
  });

  it('Sem Baixas abre a luta ★ depois da 5; perder a ★ não acaba a jornada', () => {
    const lutas = [...ate(3, { survivors: 3 }), luta(3), luta(4)];
    expect(segredosCumpridos(trioComum, lutas)).toContain('sem-baixas');
    expect(proximaLuta(trioComum, lutas)).toBe(LUTA_ESTRELA);
    expect(proximaLuta(trioComum, [...lutas, luta(LUTA_ESTRELA, false)])).toBe(5);
    // a ★ vem uma vez só
    expect(proximaLuta(trioComum, [...lutas, luta(LUTA_ESTRELA), luta(5)])).toBe(6);
  });

  it('Relâmpago abre as duas; a 11 só depois de vencer as 10', () => {
    // 3 rápidas não bastam mais: são 4 das 5 primeiras
    expect(segredosCumpridos(trioComum, [luta(0, true, { time: 20 }), luta(1, true, { time: 22 }), luta(2, true, { time: 24 }), luta(3), luta(4)])).not.toContain('relampago');
    const rapido = [luta(0, true, { time: 20 }), luta(1, true, { time: 22 }), luta(2, true, { time: 24 }), luta(3), luta(4, true, { time: 21 })];
    expect(proximaLuta(trioComum, rapido)).toBe(LUTA_ESTRELA);
    const resto = [5, 6, 7, 8, 9].map((i) => luta(i));
    expect(proximaLuta(trioComum, [...rapido, luta(LUTA_ESTRELA, false), ...resto])).toBe(LUTA_ONZE);
    expect(proximaLuta(trioComum, [...rapido, luta(LUTA_ESTRELA), ...resto, luta(LUTA_ONZE)])).toBeNull();
    expect(proximaLuta(trioComum, [...rapido, luta(LUTA_ESTRELA), 5, 6].map((x) => (typeof x === 'number' ? luta(x, x !== 6) : x)))).toBeNull();
  });

  it('Trio Intacto e A Virada abrem só a 11', () => {
    expect(proximaLuta(trioComum, [...ate(9), luta(9, true, { survivors: 3 })])).toBe(LUTA_ONZE);
    const virada = [luta(0, true, { virada: true }), ...ate(10).slice(1)];
    expect(proximaLuta(trioComum, virada.slice(0, 5))).toBe(5);
    expect(proximaLuta(trioComum, virada)).toBe(LUTA_ONZE);
    // a virada numa luta perdida não conta
    expect(segredosCumpridos(trioComum, [luta(0, false, { virada: true })])).toEqual([]);
  });

  it('Davi contra Golias: um trio de 1 estrela que vence as 5 primeiras abre as duas', () => {
    const pequeno = ['goku', 'pikachu', 'batman'];
    expect(proximaLuta(pequeno, ate(5))).toBe(LUTA_ESTRELA);
    expect(segredosCumpridos(pequeno, ate(4))).not.toContain('davi');
    expect(proximaLuta(pequeno, [...ate(5), luta(LUTA_ESTRELA, false), ...[5, 6, 7, 8, 9].map((i) => luta(i))])).toBe(LUTA_ONZE);
  });

  it('Clássico do Universo: o rival é do mesmo universo, completado com versões sombrias quando faltam', () => {
    const trio = ['saitama', 'garou', 'genos'], u = byId.saitama!.universe;
    expect(trio.every((id) => byId[id]!.universe === u)).toBe(true);
    const seed = 135848164, campanha = generateCampaign(seed, trio);
    const rival = rivalSecreto(seed, trio, campanha, 'estrela', true);
    expect(rival.team).toHaveLength(3);
    expect(rival.team.every((id) => byId[id]!.universe === u)).toBe(true);
    expect(rivalSecreto(seed, trio, campanha, 'estrela', true)).toEqual(rival);
  });

  it('o rival secreto é novo na jornada e não tem ninguém do trio', () => {
    const seed = 54855668, campanha = generateCampaign(seed, trioComum), usados = new Set(campanha.flatMap((e) => e.team));
    for (const q of ['estrela', 'onze'] as const) {
      const r = rivalSecreto(seed, trioComum, campanha, q, false);
      expect(new Set(r.team).size).toBe(3);
      expect(r.team.some((id) => usados.has(id) || trioComum.includes(id))).toBe(false);
    }
  });

  it('o servidor refaz a jornada com as lutas extras, na ordem, e soma a extra só se vencer', () => {
    const r = replayRanked(['sekhmet', 'poisonivy', 'jake'], 441500124, true);
    expect(r.summaries.map((s) => s.index)).toEqual([0, 1, 2, 3, 4, LUTA_ESTRELA, 5, 6, 7, 8, 9, LUTA_ONZE]);
    expect(r.encountersCleared).toBe(10);
    expect(r.score).toBe(r.summaries.reduce((n, s) => n + s.score, 0));
    for (const s of r.summaries.filter((x) => x.index >= LUTA_ESTRELA && !x.won)) expect(s.score).toBe(0);
    expect(r.highlights.segredos).toEqual(['sem-baixas', 'intacto']);
    // desistiu depois de 7 lutas: as 5, a ★ e a 6
    expect(replayRanked(['sekhmet', 'poisonivy', 'jake'], 441500124, true, false, 7).summaries.map((s) => s.index)).toEqual([0, 1, 2, 3, 4, LUTA_ESTRELA, 5]);
  });

  it('Clássico com versões sombrias: a luta acontece até o fim', () => {
    const r = replayRanked(['saitama', 'garou', 'genos'], 135848164, true);
    expect(r.summaries.map((s) => s.index).slice(0, 6)).toEqual([0, 1, 2, 3, 4, LUTA_ESTRELA]);
    expect(r.highlights.segredos).toContain('classico');
  });
});
