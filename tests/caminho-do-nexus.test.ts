import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { DESCANSO, REGIOES, RIVAIS, TOTAL_DE_ESTRELAS, colecaoDoRival, contaParaODescanso, depoisDaPartida, descansoDaRegiao, seuDescanso, escolhaDoRival, estrelasDaPartida, liberado, livresParaJogar, proximoRival,
  quemLutou, timesDoRival, tituloDas, totalDeEstrelas, zerou } from '../src/engine/campanha';
import { problemaDosTimes, timesLivres, variacaoContraNpc, variacaoDoElo, type PartidaPvp, type RodadaPvp } from '../src/engine/pvp';

/* O Caminho do Nexus (src/engine/campanha.ts): os 40 rivais, as estrelas, o caminho, o rodízio e o rating. */
describe('Caminho do Nexus', () => {
  it('40 rivais em 8 regiões, 4 e um chefe em cada, do 600 ao Imperador de 2500', () => {
    expect(RIVAIS).toHaveLength(40);
    expect(REGIOES).toHaveLength(8);
    expect(new Set(RIVAIS.map((r) => r.id)).size).toBe(40);
    for (const g of REGIOES) {
      const dela = RIVAIS.filter((r) => r.regiao === g.n);
      expect(dela).toHaveLength(5);
      expect(dela.map((r) => r.chefe)).toEqual([false, false, false, false, true]);
    }
    expect(RIVAIS[0]!.rating).toBe(600);
    expect(RIVAIS[39]!.rating).toBe(2500);
    expect(RIVAIS[39]!.rating).toBeGreaterThan(1900); // mais forte que o Mestre do Treino
    for (let i = 1; i < 40; i++) expect(RIVAIS[i]!.rating).toBeGreaterThan(RIVAIS[i - 1]!.rating);
    for (const r of RIVAIS) expect(byId[r.avatar], r.id).toBeTruthy();
    expect(TOTAL_DE_ESTRELAS).toBe(120);
  });

  it('a Aura do Chefe: +10%, +15% e +20% só nos chefes das regiões 6, 7 e 8', () => {
    expect(RIVAIS.filter((r) => r.aura > 0).map((r) => [r.id, r.aura])).toEqual([['titamagma', 0.1], ['panteao', 0.15], ['imperador', 0.2]]);
  });

  it('cada rival tem gente suficiente para jogar com o rodízio (9 nos times e 3 descansando)', () => {
    for (const r of RIVAIS) expect(colecaoDoRival(r).length, r.id).toBeGreaterThanOrEqual(15);
  });

  it('os times do rival valem, repetem com a mesma semente e deixam de fora quem descansa', () => {
    for (const r of [RIVAIS[0]!, RIVAIS[9]!, RIVAIS[21]!, RIVAIS[35]!]) {
      const seus = [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']];
      const t = timesDoRival(r, 77, [], seus.flat());
      expect(problemaDosTimes(t)).toBeNull();
      expect(timesDoRival(r, 77, [], seus.flat())).toEqual(t);
      const descansa = t[0]!;
      expect(timesDoRival(r, 77, descansa, seus.flat()).flat().some((id) => descansa.includes(id))).toBe(false);
    }
  });

  it('o rival escolhe sempre um time que ainda pode usar (o vidente também)', () => {
    for (const r of [RIVAIS[1]!, RIVAIS[14]!, RIVAIS[31]!]) {
      const meus = [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] as PartidaPvp['meus'];
      const p: PartidaPvp = { meus, deles: timesDoRival(r, 5), rodadas: [{ meu: 0, dele: 1, seed: 1, vencedor: 'rival' }], seed: 0 };
      const i = escolhaDoRival(r, p, 123, 456);
      expect(timesLivres(p, 'rival')).toContain(i);
    }
  });

  it('estrelas: 3–0 dá 3, 3–1 dá 2, 3–2 dá 1, derrota dá 0', () => {
    const v = (meu: number): RodadaPvp => ({ meu, dele: 0, seed: 0, vencedor: 'eu' }), d: RodadaPvp = { meu: 0, dele: 0, seed: 0, vencedor: 'rival' };
    expect(estrelasDaPartida({ rodadas: [v(0), v(1), v(2)] })).toBe(3);
    expect(estrelasDaPartida({ rodadas: [v(0), d, v(1), v(2)] })).toBe(2);
    expect(estrelasDaPartida({ rodadas: [d, v(0), d, v(1), v(2)] })).toBe(1);
    expect(estrelasDaPartida({ rodadas: [d, v(0), d, v(1), d] })).toBe(0);
  });

  it('o caminho: só o primeiro liberado; vencer libera o próximo; o Imperador zera', () => {
    expect(RIVAIS.filter((r) => liberado({}, r)).map((r) => r.id)).toEqual(['zepipoca']);
    expect(liberado({ zepipoca: 1 }, RIVAIS[1]!)).toBe(true);
    expect(liberado({ zepipoca: 1 }, RIVAIS[2]!)).toBe(false);
    expect(proximoRival({ zepipoca: 3 })!.id).toBe(RIVAIS[1]!.id);
    const tudo = Object.fromEntries(RIVAIS.map((r) => [r.id, 3]));
    expect(proximoRival(tudo)).toBeNull();
    expect(zerou(tudo)).toBe(true);
    expect(totalDeEstrelas(tudo)).toBe(120);
    expect(tituloDas(0).nome).toBe('Aprendiz');
    expect(tituloDas(120).nome).toBe('Lenda do Nexus');
  });

  it('rodízio: os 3 que mais lutaram nas últimas 5 partidas descansam 3 partidas', () => {
    const times = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3'], ['c1', 'c2', 'c3']];
    // o time 0 lutou 3 vezes, o 1 duas, o 2 uma
    const uso = quemLutou(times, [{ time: 0 }, { time: 1 }, { time: 0 }, { time: 1 }, { time: 0 }, { time: 2 }]);
    let d = depoisDaPartida({}, [uso]);
    expect(Object.keys(d).sort()).toEqual(['a1', 'a2', 'a3']);
    expect(Object.values(d)).toEqual([DESCANSO.partidas, DESCANSO.partidas, DESCANSO.partidas]);
    // descansam as 3 partidas seguintes; só então outros 3 descansam
    d = depoisDaPartida(d, [uso, ['b1', 'b2', 'b3']]); expect(d.a1).toBe(2);
    d = depoisDaPartida(d, [uso, ['b1', 'b2', 'b3']]); expect(d.a1).toBe(1);
    d = depoisDaPartida(d, [uso, ['b1', 'b2', 'b3'], ['b1', 'b2', 'b3'], ['b1', 'b2', 'b3']]);
    expect(Object.keys(d).sort()).toEqual(['b1', 'b2', 'b3']);
    expect(livresParaJogar(['a1', 'b1', 'c1'], d)).toEqual(['a1', 'c1']);
  });

  it('rodízio: dormem 2 por partida, sempre por 3 partidas, até 6 — igual em todas as regiões', () => {
    expect(REGIOES.every((r) => descansoDaRegiao(r.n).quantos === 6 && descansoDaRegiao(r.n).porVez === 2 && descansoDaRegiao(r.n).partidas === 3)).toBe(true);
    // nunca menos de 9 livres: com 12 personagens dormem no máximo 3, com 15 ou mais até 6
    expect(seuDescanso(8, 12).quantos).toBe(3);
    expect(seuDescanso(8, 14).quantos).toBe(5);
    expect(seuDescanso(1, 15).quantos).toBe(6);
    expect(seuDescanso(8, 40).quantos).toBe(6);
    // depois da 1ª partida dormem os 2 que mais lutaram
    const times = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3'], ['c1', 'c2', 'c3']];
    const uso = quemLutou(times, [{ time: 0 }, { time: 1 }, { time: 2 }, { time: 0 }]);
    const d = depoisDaPartida({}, [uso], seuDescanso(1, 30));
    expect(Object.keys(d).sort()).toEqual(['a1', 'a2']);
    expect(Object.values(d)).toEqual([3, 3]);
  });

  it('60 partidas com 20 personagens: 2, 4, 6 dormindo e depois sempre 6 (acordam 2, dormem 2), sobrando 9 para os times', () => {
    const colecao = Array.from({ length: 20 }, (_, i) => `p${i}`), regra = seuDescanso(8, colecao.length);
    let d: Record<string, number> = {}, semente = 7;
    const rnd = () => { semente = (semente * 1103515245 + 12345) % 2147483648; return semente / 2147483648; };
    const feitas: string[][] = [], dormindo: number[] = [];
    for (let k = 0; k < 60; k++) {
      const livres = livresParaJogar(colecao, d).sort(() => rnd() - 0.5);
      expect(livres.length).toBeGreaterThanOrEqual(9);
      const times = [livres.slice(0, 3), livres.slice(3, 6), livres.slice(6, 9)];
      const rodadas = Array.from({ length: 3 + Math.floor(rnd() * 3) }, (_, n) => ({ time: n % 3 }));
      feitas.push(quemLutou(times, rodadas));
      const antes = d;
      d = depoisDaPartida(d, feitas.slice(-DESCANSO.janela), regra);
      dormindo.push(Object.keys(d).length);
      // quem adormece nesta partida: sempre 2, e cada um dorme 3 partidas
      const novos = Object.keys(d).filter((id) => !(id in antes));
      expect(novos).toHaveLength(2);
      expect(novos.every((id) => d[id] === 3)).toBe(true);
    }
    expect(dormindo.slice(0, 3)).toEqual([2, 4, 6]);
    expect(dormindo.slice(3).every((n) => n === 6)).toBe(true);
  });

  it('com 12 personagens o rodízio para em 3 dormindo (sempre 9 livres)', () => {
    const colecao = Array.from({ length: 12 }, (_, i) => `p${i}`), regra = seuDescanso(5, colecao.length);
    let d: Record<string, number> = {};
    const feitas: string[][] = [];
    for (let k = 0; k < 20; k++) {
      const livres = livresParaJogar(colecao, d);
      expect(livres.length).toBeGreaterThanOrEqual(9);
      feitas.push(livres.slice(0, 9));
      d = depoisDaPartida(d, feitas.slice(-DESCANSO.janela), regra);
      expect(Object.keys(d).length).toBeLessThanOrEqual(3);
    }
  });

  it('rival já gabaritado (★★★) não acorda ninguém; com 1 ou 2 estrelas ainda conta', () => {
    const r = RIVAIS[0]!;
    expect(contaParaODescanso({}, r)).toBe(true);
    expect(contaParaODescanso({ [r.id]: 1 }, r)).toBe(true);
    expect(contaParaODescanso({ [r.id]: 2 }, r)).toBe(true);
    expect(contaParaODescanso({ [r.id]: 3 }, r)).toBe(false);
    // com a campanha toda gabaritada, qualquer partida conta (senão ninguém acordaria mais)
    expect(contaParaODescanso(Object.fromEntries(RIVAIS.map((x) => [x.id, 3])), r)).toBe(true);
  });

  it('rating: contra rival ganha 80% e perde 120%; 400 acima não ganha nada (contra pessoas também)', () => {
    expect(variacaoDoElo(1000, 1000, true)).toBe(16);
    expect(variacaoContraNpc(1000, 1000, true)).toBe(13);
    expect(variacaoContraNpc(1000, 1000, false)).toBe(-19);
    expect(variacaoContraNpc(1000, 600, true)).toBe(0);
    expect(variacaoContraNpc(1000, 600, false)).toBeLessThan(-30);
    expect(variacaoDoElo(1400, 1000, true)).toBe(0);
    expect(variacaoDoElo(1399, 1000, true)).toBeGreaterThan(0);
    expect(variacaoDoElo(1000, 1400, false)).toBeLessThan(0);
  });
});
