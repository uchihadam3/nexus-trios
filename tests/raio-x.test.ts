/*
 * FASE G · o contrato do Raio-X.
 *
 * A regra que governa esta fase cabe em cinco palavras do documento: **não
 * inventar causalidade que não aconteceu**. Um pós-batalha que afirma conexões
 * plausíveis mas falsas é pior que nenhum: ensina errado, e o jogador monta o
 * próximo trio com base na mentira.
 *
 * Então os testes não conferem redação — conferem que todo elo tem evento que
 * o prove, e que nenhuma classificação aparece sem lastro.
 */
import { describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import {
  acumularRaioX, lerRaioX, quemAbsorveu, raioXVazio,
  type Classificacao, type EstadoRaioX,
} from '../src/engine/raio-x';
import type { Battle, BattleEvent } from '../src/engine/types';

/** Joga uma luta inteira acumulando como o jogo acumula: quadro a quadro. */
const jogar = (meu: string[], dele: string[], semente: number): { b: Battle; estado: EstadoRaioX; eventos: BattleEvent[] } => {
  const b = createBattle(meu, dele, semente);
  let estado = raioXVazio(), visto = 0;
  const eventos: BattleEvent[] = [];
  for (let p = 0; p < 4200 && !b.finished; p += 1) {
    stepBattle(b);
    const novos = b.events.filter((e) => e.id > visto);
    if (novos.length) {
      visto = Math.max(...novos.map((e) => e.id));
      eventos.push(...novos);
      estado = acumularRaioX(estado, novos, b);
    }
  }
  return { b, estado, eventos };
};

describe('o Raio-X não inventa causalidade', () => {
  const { b, estado, eventos } = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);

  it('a luta produziu elos para analisar', () => {
    expect(estado.elos.length).toBeGreaterThan(0);
    expect(eventos.length).toBeGreaterThan(100);
  });

  it('todo elo liga dois lutadores diferentes do próprio trio', () => {
    for (const elo of estado.elos) {
      expect(elo.de).not.toBe(elo.para);
      expect(elo.de.startsWith('player-'), `${elo.de} não é do trio`).toBe(true);
      expect(elo.para.startsWith('player-'), `${elo.para} não é do trio`).toBe(true);
      expect(elo.vezes).toBeGreaterThan(0);
    }
  });

  /*
   * Cada tipo de elo precisa de um evento que o sustente. Se o acumulador
   * inventar um elo de cura numa luta sem cura, isto cai.
   */
  it.each([
    ['cura', 'heal'],
    ['escudo', 'shield'],
    ['carga', 'synergy'],
  ])('elos de %s exigem eventos de %s', (tipo, kind) => {
    const temElo = estado.elos.some((e) => e.tipo === tipo);
    if (!temElo) return;
    const temEvento = eventos.some((e) => e.kind === kind && e.source.startsWith('player-') && e.target?.startsWith('player-'));
    expect(temEvento, `elo de ${tipo} sem nenhum evento ${kind}`).toBe(true);
  });

  it('elos de finalização exigem um abate', () => {
    if (!estado.elos.some((e) => e.tipo === 'finalizacao')) return;
    expect(eventos.some((e) => e.kind === 'ko' && e.source.startsWith('player-'))).toBe(true);
  });

  it('nunca conta mais vezes do que houve eventos', () => {
    const curas = eventos.filter((e) => e.kind === 'heal' && e.source.startsWith('player-') && e.target?.startsWith('player-') && e.target !== e.source).length;
    const contadas = estado.elos.filter((e) => e.tipo === 'cura').reduce((n, e) => n + e.vezes, 0);
    expect(contadas).toBe(curas);
  });

  it('o acumulador é puro: não altera o estado que recebe', () => {
    const antes = raioXVazio();
    const copia = JSON.stringify(antes);
    const depois = acumularRaioX(antes, eventos.slice(0, 40), b);
    expect(JSON.stringify(antes)).toBe(copia);
    expect(depois).not.toBe(antes);
  });

  it('o mesmo par de entradas sempre dá o mesmo resultado', () => {
    const um = acumularRaioX(raioXVazio(), eventos.slice(0, 80), b);
    const dois = acumularRaioX(raioXVazio(), eventos.slice(0, 80), b);
    expect(JSON.stringify(um)).toBe(JSON.stringify(dois));
  });
});

describe('a leitura dos três pares', () => {
  const { b, estado } = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);
  const pares = lerRaioX(estado, b);

  it('são exatamente os três pares do trio, nas duas direções', () => {
    expect(pares).toHaveLength(3);
    const vistos = new Set(pares.map((p) => [p.a, p.b].sort().join('|')));
    expect(vistos.size).toBe(3);
    for (const par of pares) {
      expect(par.aParaB.de).toBe(par.a);
      expect(par.aParaB.para).toBe(par.b);
      expect(par.bParaA.de).toBe(par.b);
      expect(par.bParaA.para).toBe(par.a);
    }
  });

  it('a frase de cada direção vem de um elo daquela direção', () => {
    for (const par of pares) {
      for (const dir of [par.aParaB, par.bParaA]) {
        if (dir.frase === null) { expect(dir.elos).toHaveLength(0); continue; }
        expect(dir.elos.length).toBeGreaterThan(0);
        for (const elo of dir.elos) { expect(elo.de).toBe(dir.de); expect(elo.para).toBe(dir.para); }
      }
    }
  });

  it('sem elo nenhum nas duas direções, o par é INDEPENDENTES', () => {
    const vazio = lerRaioX(raioXVazio(), b);
    for (const par of vazio) {
      expect(par.classificacao).toBe('INDEPENDENTES');
      expect(par.aParaB.frase).toBeNull();
      expect(par.bParaA.frase).toBeNull();
    }
  });
});

describe('a classificação separa os pares', () => {
  /*
   * "ÓTIMA CONEXÃO" em mais da metade dos pares seria o mesmo defeito que a
   * FASE F encontrou nas etiquetas: um rótulo que vale para a maioria não
   * separa ninguém. A primeira versão desta escala dava 56% de ótimas.
   */
  const conta = new Map<Classificacao, number>();
  let total = 0;
  for (let s = 1; s <= 40; s += 1) {
    const pega = (n: number) => characters[(s * 61 + n * 37) % characters.length]!.id;
    const meu = [pega(1), pega(2), pega(3)], dele = [pega(4), pega(5), pega(6)];
    if (new Set([...meu, ...dele]).size < 6) continue;
    const { b, estado } = jogar(meu, dele, s);
    for (const par of lerRaioX(estado, b)) { conta.set(par.classificacao, (conta.get(par.classificacao) ?? 0) + 1); total += 1; }
  }

  it('avaliou pares suficientes', () => { expect(total).toBeGreaterThan(60); });

  it('"ÓTIMA CONEXÃO" é exceção, não regra', () => {
    const otimas = conta.get('ÓTIMA CONEXÃO') ?? 0;
    expect(otimas / total, `${String(otimas)} de ${String(total)}`).toBeLessThan(0.3);
    expect(otimas, 'nenhuma ótima em 40 lutas: a escala ficou inalcançável').toBeGreaterThan(0);
  });

  /*
   * "CONFLITO somente quando houver conflito mecânico real." Depois que a FASE
   * E tirou os 80 efeitos ofensivos que caíam em aliados, nenhum personagem
   * prejudica um companheiro — então o esperado é zero, e um conflito que
   * aparecesse aqui seria notícia de regressão, não de desenho.
   */
  it('não acusa conflito onde não há fogo amigo', () => {
    expect(conta.get('CONFLITO') ?? 0).toBe(0);
  });
});

describe('quem segurou a pressão', () => {
  it('aponta o lutador que mais apanhou, com a fração do total', () => {
    const { b, estado } = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);
    const p = quemAbsorveu(estado, b);
    expect(p).not.toBeNull();
    expect(p!.uid.startsWith('player-')).toBe(true);
    expect(p!.parte).toBeGreaterThan(0);
    expect(p!.parte).toBeLessThanOrEqual(1);
    const maior = Math.max(...Object.values(estado.absorvido));
    expect(estado.absorvido[p!.uid]).toBe(maior);
  });

  it('sem dano recebido, não afirma nada', () => {
    const { b } = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);
    expect(quemAbsorveu(raioXVazio(), b)).toBeNull();
  });
});

/*
 * Os elos das mecânicas novas, provados por eventos (nada inferido do kit):
 * levantou (Reviver), purificou (Purificar) e provocou (o rival provocado
 * bateu em quem provocou, e não nos aliados).
 */
import { acumularRaioX as acumulaNovo, lerRaioX as leNovo, raioXVazio as vazioNovo } from '../src/engine/raio-x';
import { createBattle as criaNova } from '../src/engine/battle';
import type { BattleEvent as EventoNovo } from '../src/engine/types';
describe('Raio-X: elos das mecânicas novas', () => {
  const b = criaNova(['sailormoon', 'captain', 'goku'], ['hulk', 'thanos', 'saitama'], 3);
  const [moon, cap, goku] = b.fighters.filter((f) => f.side === 'player');
  const hulk = b.fighters.find((f) => f.side === 'enemy')!;
  const ev = (e: Partial<EventoNovo>): EventoNovo => ({ id: 0, time: 1, kind: 'damage', source: '', label: '', ...e }) as EventoNovo;
  it('levantou e purificou vêm dos eventos do motor', () => {
    const s = acumulaNovo(vazioNovo(), [
      ev({ kind: 'revive', source: moon!.uid, target: goku!.uid, label: 'Levantou' }),
      ev({ kind: 'cleanse', source: moon!.uid, target: cap!.uid, label: 'Purificou', removidos: ['paralyzed', 'slow'] }),
    ], b);
    expect(s.elos).toContainEqual({ de: moon!.uid, para: goku!.uid, tipo: 'levantou', vezes: 1, valor: 1 });
    expect(s.elos).toContainEqual({ de: moon!.uid, para: cap!.uid, tipo: 'purificou', vezes: 1, valor: 2 });
    const par = leNovo(s, b).find((p) => [p.a, p.b].includes(moon!.uid) && [p.a, p.b].includes(goku!.uid))!;
    expect([par.aParaB.frase, par.bParaA.frase]).toContain(`levantou ${'Goku'} depois que caiu`);
  });
  it('provocou: só conta o golpe do rival provocado em quem provocou', () => {
    const s = acumulaNovo(vazioNovo(), [
      ev({ kind: 'status', status: 'provoked', source: cap!.uid, target: hulk.uid, value: 5, label: 'Provocado' }),
      ev({ kind: 'damage', source: hulk.uid, target: cap!.uid, value: 200, time: 2 }),
      ev({ kind: 'damage', source: hulk.uid, target: cap!.uid, value: 200, time: 9 }), // já passou a provocação
    ], b);
    const puxados = s.elos.filter((e) => e.tipo === 'provocou' && e.de === cap!.uid);
    expect(puxados.map((e) => e.para).sort()).toEqual([goku!.uid, moon!.uid].sort());
    expect(puxados.every((e) => e.vezes === 1)).toBe(true);
  });
});
