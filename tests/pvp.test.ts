import { describe, expect, it } from 'vitest';
import { TRIOS_DO_PVP } from '../src/data/trios-do-pvp';
import { NPCS, colecaoDoNpc, escolhaDoNpc, esperado, problemaDosTimes, sementeDaRodada, timesDoNpc, timesLivres, variacaoDoElo, vencedorDaPartida, type PartidaPvp, type Times } from '../src/engine/pvp';
import { byId } from '../src/data/characters';
import { notaDoTrio } from '../src/presentation/dicas-do-trio';

const T = (s: string) => s.split(' ').map((x) => x.split('+')) as Times;
const MEUS = T('goku+vegeta+gohan naruto+sasuke+kakashi luffy+zoro+sanji');
const DELES = T('gojo+itachi+light pikachu+charizard+mewtwo batman+superman+wonderwoman');

describe('PvP: regras da partida', () => {
  it('3 times de 3, 9 personagens diferentes, todos da coleção', () => {
    expect(problemaDosTimes(MEUS)).toBeNull();
    expect(problemaDosTimes([MEUS[0], MEUS[1]])).toMatch(/3 times/);
    expect(problemaDosTimes([MEUS[0], MEUS[1], ['goku', 'zoro', 'sanji']])).toMatch(/um time/);
    expect(problemaDosTimes(MEUS, new Set(MEUS.flat().slice(1)))).toMatch(/coleção/);
  });
  it('o time que vence fica marcado; quem perde escolhe qualquer um; vence quem ganhar com os 3', () => {
    const p: PartidaPvp = { meus: MEUS, deles: DELES, rodadas: [], seed: 7 };
    p.rodadas.push({ meu: 0, dele: 2, seed: 1, vencedor: 'eu' });
    expect(timesLivres(p, 'eu')).toEqual([1, 2]);
    expect(timesLivres(p, 'rival')).toEqual([0, 1, 2]);
    p.rodadas.push({ meu: 1, dele: 2, seed: 2, vencedor: 'rival' });
    expect(timesLivres(p, 'rival')).toEqual([0, 1]);
    p.rodadas.push({ meu: 1, dele: 0, seed: 3, vencedor: 'eu' });
    expect(vencedorDaPartida(p)).toBeNull();
    p.rodadas.push({ meu: 2, dele: 1, seed: 4, vencedor: 'eu' });
    expect(vencedorDaPartida(p)).toBe('eu');
  });
  it('a semente de cada rodada é a mesma para os dois e muda a cada rodada', () => {
    expect(sementeDaRodada(123, 0)).toBe(sementeDaRodada(123, 0));
    expect(sementeDaRodada(123, 0)).not.toBe(sementeDaRodada(123, 1));
  });
});

describe('PvP: rating (Elo)', () => {
  it('rating igual: +16 ou −16; vencer quem tem muito mais rating vale mais', () => {
    expect(esperado(1000, 1000)).toBeCloseTo(0.5);
    expect(variacaoDoElo(1000, 1000, true)).toBe(16);
    expect(variacaoDoElo(1000, 1000, false)).toBe(-16);
    expect(variacaoDoElo(1000, 1400, true)).toBeGreaterThan(25);
    expect(variacaoDoElo(1400, 1000, true)).toBeLessThan(5);
  });
});

describe('PvP: NPCs de treino', () => {
  it('seis níveis, coleções de 75 a 400, rating crescente, avatares do elenco; só a Lenda tem Aura', () => {
    expect(NPCS.map((n) => n.colecao)).toEqual([75, 130, 200, 300, 400, 400]);
    expect(NPCS.filter((n) => n.aura).map((n) => n.id)).toEqual(['lenda']);
    for (let i = 1; i < NPCS.length; i++) expect(NPCS[i]!.rating).toBeGreaterThan(NPCS[i - 1]!.rating);
    for (const n of NPCS) { expect(byId[n.avatar], n.avatar).toBeDefined(); expect(colecaoDoNpc(n)).toHaveLength(n.colecao); }
  });
  it('cada NPC monta 3 times válidos só com os personagens dele', () => {
    for (const n of NPCS) {
      const times = timesDoNpc(n.nivel, 42), dele = new Set(colecaoDoNpc(n));
      expect(problemaDosTimes(times, dele), n.nome).toBeNull();
    }
  });
  it('quanto maior o nível, melhores os times (média de várias partidas)', () => {
    const media = (nivel: 1 | 2 | 3 | 4 | 5 | 6) => [1, 2, 3, 4, 5, 6].map((s) => timesDoNpc(nivel, s * 101).reduce((n, t) => n + notaDoTrio(t), 0)).reduce((a, b) => a + b) / 18;
    const m = ([1, 2, 3, 4, 5] as const).map(media);
    for (let i = 1; i < m.length; i++) expect(m[i]!, `nível ${i + 1}`).toBeGreaterThan(m[i - 1]!);
  });
  it('a Lenda (nível 6) joga com os trios que mais vencem em luta de verdade e com a Aura', () => {
    // a nota das Dicas não ordena o topo como as lutas medidas: a Lenda vale pelos trios medidos e pela Vida a mais
    // (medido: com +15% de Vida ela vence ~67% das lutas contra os times do Mestre)
    const topo = new Set(TRIOS_DO_PVP.slice(0, 12).map((t) => t.slice(0, 3).join()));
    for (let s = 1; s <= 6; s++) expect(timesDoNpc(6, s * 101).filter((t) => topo.has(t.join())).length, `semente ${s}`).toBeGreaterThanOrEqual(2);
    expect(NPCS[5]!.aura).toBeGreaterThan(0.1);
  });
  it('o NPC só escolhe time que ainda pode jogar', () => {
    const p: PartidaPvp = { meus: MEUS, deles: timesDoNpc(5, 9), rodadas: [{ meu: 0, dele: 1, seed: 1, vencedor: 'rival' }], seed: 9 };
    for (const nivel of [1, 2, 3, 4, 5, 6] as const) for (let s = 0; s < 20; s++) expect(escolhaDoNpc(nivel, p, s)).not.toBe(1);
  });
});
