import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { generateCampaign } from '../src/engine/campaign';
import { CUSTO_DA_COLECAO, pontosDaLuta } from '../src/engine/pontos';
import { replayRanked } from '../src/engine/ranked';
import { ESTRELAS_DE_PONTOS } from '../src/data/estrelas-de-pontos';
import { byId, characters } from '../src/data/characters';
import { recusaDaColecao } from '../supabase/functions/ranked-api/colecao';
import { LUTA_ESTRELA, proximaLuta } from '../src/engine/segredos';

/* A Jornada com os seus (components/JornadaComOsSeus.tsx): o trio da coleção, sem bônus de estrela nem segredos, −30 mil por luta. */
describe('Jornada com os seus', () => {
  const estrela = Object.keys(ESTRELAS_DE_PONTOS)[0]!;
  const trio = [estrela, ...characters.map((c) => c.id).filter((id) => id !== estrela && !ESTRELAS_DE_PONTOS[id]).slice(0, 2)];

  it('a luta não ganha o bônus da estrela e custa 30 mil', () => {
    const b = createBattle(trio, generateCampaign(77)[0]!.team, 77);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    const normal = pontosDaLuta(b, 0), comOsSeus = pontosDaLuta(b, 0, false, true);
    const bonus = normal.parcelas.find((p) => p.id === 'estrela');
    expect(bonus?.valor).toBeGreaterThan(0);
    expect(comOsSeus.parcelas.some((p) => p.id === 'estrela')).toBe(false);
    expect(comOsSeus.parcelas.find((p) => p.id === 'colecao')?.valor).toBe(-CUSTO_DA_COLECAO);
    // a luta nunca vale menos que zero
    expect(comOsSeus.total).toBe(Math.max(0, normal.total - bonus!.valor - CUSTO_DA_COLECAO));
  });

  it('o servidor refaz a jornada com a regra e marca no ranking', () => {
    const seed = 4242, normal = replayRanked(trio, seed, true), comOsSeus = replayRanked(trio, seed, true, false, undefined, true);
    expect(comOsSeus.highlights.colecao).toBe(true);
    expect(normal.highlights).not.toHaveProperty('colecao');
    // as mesmas 10 lutas de sempre (a regra só mexe nos pontos; sem as extras dos segredos), cada uma valendo menos
    const dasDez = (j: typeof normal) => j.summaries.filter((s) => s.index < 10);
    expect(dasDez(comOsSeus).map((s) => s.won)).toEqual(dasDez(normal).map((s) => s.won));
    for (const s of dasDez(comOsSeus)) expect(s.score).toBeLessThanOrEqual(Math.max(0, dasDez(normal).find((x) => x.index === s.index)!.score - CUSTO_DA_COLECAO));
  }, 60000);

  it('os segredos não valem: sem as lutas extras e sem nada no Livro', () => {
    // a jornada do teste dos segredos (tests/segredos.test.ts): vence as 10 e abre a ★ e a 11
    const trioDosSegredos = ['sekhmet', 'poisonivy', 'jake'], seed = 196851108;
    const normal = replayRanked(trioDosSegredos, seed, true), comOsSeus = replayRanked(trioDosSegredos, seed, true, false, undefined, true);
    expect(normal.summaries.map((s) => s.index)).toContain(LUTA_ESTRELA);
    expect(normal.highlights.segredos?.length).toBeGreaterThan(0);
    expect(comOsSeus.summaries.map((s) => s.index)).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
    expect(comOsSeus.encountersCleared).toBe(10);
    expect(comOsSeus.highlights).not.toHaveProperty('segredos');
    expect(proximaLuta(trioDosSegredos, comOsSeus.summaries, true)).toBeNull();
  }, 60000);

  it('só com os liberados da conta e só na Jornada normal', () => {
    const minhas = new Set(trio);
    expect(recusaDaColecao(trio, minhas, 'free')).toBeNull();
    expect(recusaDaColecao(trio, minhas, 'daily')).toMatch(/Jornada normal/);
    const outro = characters.find((c) => !minhas.has(c.id))!;
    expect(recusaDaColecao([trio[0]!, trio[1]!, outro.id], minhas, 'free')).toBe(`${byId[outro.id]!.name} ainda não está liberado na sua conta.`);
  });
});
