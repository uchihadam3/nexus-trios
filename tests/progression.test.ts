/*
 * FASE H · o contrato da progressão.
 *
 * Os Objetivos saíram a pedido da direção, e com eles os testes que os
 * cobriam. O que entrou no lugar precisa de garantias mais fortes, porque as
 * conquistas são de momento: uma que ninguém consegue fica na lista para
 * sempre, o jogador tenta, não consegue, e aprende que a lista mente.
 *
 * Então aqui se cobra, além da mecânica, que o catálogo seja **alcançável** —
 * verificado jogando, não lendo.
 */
import { afterEach, describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { conquistas, conquistasDaBatalha, categorias, type Contexto } from '../src/engine/conquistas';
import { createBattle, stepBattle } from '../src/engine/battle';
import {
  acumularFeitos, desafiosDe, fecharFeitos, feitosVazios, grauAlcancado,
  podeCumprir, somarFeitos,
} from '../src/engine/maestria';
import { acumularRaioX, raioXVazio } from '../src/engine/raio-x';
import { battleDelta, emptyProgress, emptyTally, dominados, nexusLevel, recordProgress, tallyEvents } from '../src/engine/progression';
import { summarizeBattle } from '../src/engine/run-summary';
import { loadProfile } from '../src/lib/storage';

afterEach(() => { delete (globalThis as { localStorage?: unknown }).localStorage; });

/** Joga uma luta inteira acumulando como o jogo acumula. */
const jogar = (time: string[], inimigos: string[], semente: number) => {
  const b = createBattle(time, inimigos, semente);
  let feitos = feitosVazios(), raioX = raioXVazio(), tally = emptyTally(), visto = 0, maiorAtraso = 0;
  for (let p = 0; p < 4200 && !b.finished; p += 1) {
    stepBattle(b);
    maiorAtraso = Math.max(maiorAtraso, -b.dominion);
    const novos = b.events.filter((e) => e.id > visto);
    if (novos.length) {
      visto = Math.max(...novos.map((e) => e.id));
      feitos = acumularFeitos(feitos, novos, b);
      raioX = acumularRaioX(raioX, novos, b);
      tally = tallyEvents(tally, novos);
    }
  }
  return { b, feitos: fecharFeitos(feitos, b, maiorAtraso >= 8), raioX, tally, maiorAtraso: Math.round(maiorAtraso) };
};

describe('maestria dos 250', () => {
  it('tem três desafios para cada lutador', () => {
    for (const c of characters) {
      const d = desafiosDe(c.id);
      expect(d, c.name).toHaveLength(3);
      expect(d.map((x) => x.grau)).toEqual(['I', 'II', 'III']);
      for (const x of d) { expect(x.titulo.length).toBeGreaterThan(10); expect(x.meta).toBeGreaterThan(0); }
    }
    expect(characters.length * 3).toBe(750);
  });

  /*
   * "Pelo menos 2 dos 3 ligados à mecânica real", e "não usar só 'jogue 50
   * partidas'". Os desafios antigos eram três vezes "use a habilidade N
   * vezes", que falha nos dois pontos.
   */
  it('dois de cada três cobram uma mecânica, não repetição', () => {
    for (const c of characters) {
      const mecanicos = desafiosDe(c.id).filter((d) => d.mecanico);
      expect(mecanicos.length, c.name).toBeGreaterThanOrEqual(2);
      /* E os dois mecânicos são feitos diferentes: não dá para pedir a mesma coisa duas vezes. */
      expect(new Set(mecanicos.map((d) => d.feito)).size, c.name).toBe(mecanicos.length);
    }
  });

  /* Um desafio que o kit não alcança não é difícil, é quebrado. */
  it('nunca pede um feito que o personagem não consegue', () => {
    for (const c of characters) {
      for (const d of desafiosDe(c.id)) {
        expect(podeCumprir(c, d.feito), `${c.name} · ${d.titulo}`).toBe(true);
      }
    }
  });

  it('os desafios variam entre os personagens', () => {
    const pares = new Set(characters.map((c) => desafiosDe(c.id).slice(1).map((d) => d.feito).join('+')));
    expect(pares.size).toBeGreaterThan(15);
  });

  it('o grau sobe na ordem e para no primeiro degrau não cumprido', () => {
    const c = characters[0]!;
    const [, segundo, terceiro] = desafiosDe(c.id);
    expect(grauAlcancado(c.id, {})).toBe(0);
    expect(grauAlcancado(c.id, { usou: 1 })).toBe(1);
    expect(grauAlcancado(c.id, { usou: 1, [segundo!.feito]: segundo!.meta })).toBe(2);
    /* Cumprir o terceiro sem o segundo não pula o degrau. */
    expect(grauAlcancado(c.id, { usou: 1, [terceiro!.feito]: terceiro!.meta * 10 })).toBeLessThan(3);
  });

  it('soma feitos, mas guarda o maior golpe como recorde', () => {
    const junto = somarFeitos({ curou: 100, explodiu: 400 }, { curou: 50, explodiu: 250 });
    expect(junto.curou).toBe(150);
    expect(junto.explodiu).toBe(400);
  });

  it('mede feitos de uma luta de verdade', () => {
    const { b, feitos } = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);
    expect(Object.keys(feitos).length).toBe(3);
    for (const id of ['sakura', 'pikachu', 'storm']) {
      expect(feitos[id]!.usou).toBe(1);
      expect(feitos[id]!.explodiu).toBeGreaterThan(0);
    }
    /* Quem sobreviveu é quem terminou de pé, não quem o teste quis. */
    const vivos = b.fighters.filter((f) => f.side === 'player' && f.hp > 0).map((f) => f.characterId);
    for (const id of ['sakura', 'pikachu', 'storm']) {
      expect(feitos[id]!.sobreviveu ?? 0).toBe(vivos.includes(id) ? 1 : 0);
    }
  });
});

describe('conquistas', () => {
  it('são mais de 50, em todas as categorias', () => {
    expect(conquistas.length).toBeGreaterThanOrEqual(50);
    for (const cat of categorias) {
      expect(conquistas.filter((c) => c.categoria === cat).length, cat).toBeGreaterThan(0);
    }
    expect(new Set(conquistas.map((c) => c.id)).size).toBe(conquistas.length);
    for (const c of conquistas) expect(c.dica.length, c.nome).toBeGreaterThan(15);
  });

  /*
   * A prova que importa. Uma conquista impossível é pior que nenhuma, e a
   * única forma de saber é jogar. Os cenários aqui são escolhidos de
   * propósito, porque um trio sorteado nunca é do mesmo universo nem tem três
   * curandeiros — e isso não as torna impossíveis, só raras no sorteio.
   */
  it('todas são alcançáveis jogando', () => {
    const alcancadas = new Set<string>();
    const base = (x: Partial<Contexto> & { battle: Contexto['battle'] }): Contexto => ({
      feitos: {}, raioX: raioXVazio(), time: [], venceu: false, campeao: false,
      maiorAtraso: 0, indice: 0, jornada: [], vistos: [], dominados: 0, ...x,
    });
    const tentar = (c: Contexto) => { for (const id of conquistasDaBatalha(c, [])) alcancadas.add(id); };

    const cenarios: [string[], string[]][] = [
      [['sakura', 'sailormoon', 'groot'], ['vegeta', 'raven', 'hulk']],
      [['pikachu', 'storm', 'gojo'], ['goku', 'naruto', 'luffy']],
      [['saitama', 'thanos', 'hulk'], ['pikachu', 'raven', 'inosuke']],
    ];
    const duros = [...characters].sort((a, b) => b.hp - a.hp).slice(0, 6).map((c) => c.id);
    cenarios.push([duros.slice(0, 3), duros.slice(3, 6)]);
    const marvel = characters.filter((c) => c.universe === 'Marvel').slice(0, 3).map((c) => c.id);
    if (marvel.length === 3) cenarios.push([marvel, ['goku', 'naruto', 'luffy']]);

    /*
     * Além dos cenários escolhidos, uma varredura de trios variados: algumas
     * conquistas dependem de como a luta correu, não de quem lutou — vencer
     * em menos de 25 segundos, virar um placar de 45 pontos — e para essas o
     * que importa é a quantidade de lutas diferentes.
     */
    for (let s = 1; s <= 100; s += 1) {
      const pega = (n: number) => characters[(s * 71 + n * 43) % characters.length]!.id;
      const time = [pega(1), pega(2), pega(3)], inimigos = [pega(4), pega(5), pega(6)];
      if (new Set([...time, ...inimigos]).size < 6) continue;
      cenarios.push([time, inimigos]);
    }

    const todos = characters.map((c) => c.id);
    for (const [time, inimigos] of cenarios) {
      for (let s = 1; s <= 6; s += 1) {
        const r = jogar(time, inimigos, s);
        tentar(base({ battle: r.b, feitos: r.feitos, raioX: r.raioX, time, venceu: r.b.winner === 'player', maiorAtraso: r.maiorAtraso }));
        /* O mesmo instante, visto como último confronto de uma jornada. */
        tentar(base({
          battle: r.b, feitos: r.feitos, raioX: r.raioX, time,
          venceu: r.b.winner === 'player', campeao: r.b.winner === 'player', indice: 9,
          maiorAtraso: r.maiorAtraso, vistos: todos, dominados: 15,
          jornada: Array.from({ length: 9 }, (_, i) => ({ ...summarizeBattle(i, r.b), survivors: i === 3 ? 2 : 3, won: true })),
        }));
      }
    }
    /* E a jornada impecável, com os três inteiros no fim. */
    const r = jogar(['goku', 'pikachu', 'gojo'], ['vegeta', 'raven', 'hulk'], 1);
    const inteiros = { ...r.b, fighters: r.b.fighters.map((f) => f.side === 'player' ? { ...f, hp: f.maxHp } : f) };
    tentar(base({
      battle: inteiros, feitos: r.feitos, raioX: r.raioX, time: ['goku', 'pikachu', 'gojo'],
      venceu: true, campeao: true, indice: 9, vistos: todos, dominados: 15,
      jornada: Array.from({ length: 9 }, (_, i) => ({ ...summarizeBattle(i, r.b), survivors: 3, won: true })),
    }));

    const nunca = conquistas.filter((c) => !alcancadas.has(c.id)).map((c) => `${c.nome} — ${c.dica}`);
    expect(nunca).toEqual([]);
    /*
     * Centenas de lutas levam mais que os 5 s padrão do Vitest. Aqui rodou em
     * 2,8 s e no runner do CI estourou — a cobertura é o ponto deste teste,
     * então quem cede é o relógio, não o número de cenários.
     */
  }, 60000);

  it('não entrega duas vezes a mesma conquista', () => {
    const r = jogar(['sakura', 'pikachu', 'storm'], ['vegeta', 'raven', 'hulk'], 7);
    const ctx: Contexto = {
      battle: r.b, feitos: r.feitos, raioX: r.raioX, time: ['sakura', 'pikachu', 'storm'],
      venceu: r.b.winner === 'player', campeao: false, maiorAtraso: r.maiorAtraso,
      indice: 0, jornada: [], vistos: [], dominados: 0,
    };
    const primeira = conquistasDaBatalha(ctx, []);
    expect(primeira.length).toBeGreaterThan(0);
    expect(conquistasDaBatalha(ctx, primeira)).toEqual([]);
  });
});

describe('registro da progressão', () => {
  it('guarda feitos, conquistas e XP de uma batalha de verdade', () => {
    const time = ['sakura', 'pikachu', 'storm'];
    const r = jogar(time, ['vegeta', 'raven', 'hulk'], 7);
    const summary = summarizeBattle(0, r.b);
    const depois = recordProgress(emptyProgress(), {
      delta: battleDelta(summary, r.b, r.tally, [], time),
      battle: r.b, team: time, feitos: r.feitos, raioX: r.raioX,
      maiorAtraso: r.maiorAtraso, indice: 0, jornada: [],
    });
    expect(depois.seen.sort()).toEqual([...time].sort());
    expect(depois.stats.battles).toBe(1);
    expect(depois.xp).toBeGreaterThan(0);
    expect(depois.unlocked.length).toBeGreaterThan(0);
    for (const id of time) expect(depois.mastery[id]!.usou).toBe(1);
    /* Todo mundo começa no degrau I depois de uma batalha. */
    for (const id of time) expect(grauAlcancado(id, depois.mastery[id]!)).toBeGreaterThanOrEqual(1);
  });

  it('XP é prestígio: sobe de nível e nunca mexe em atributo', () => {
    expect(nexusLevel(0)).toBe(1);
    expect(nexusLevel(100)).toBe(2);
    expect(nexusLevel(400)).toBe(3);
    const antes = characters[0]!.hp;
    const r = jogar(['goku', 'pikachu', 'gojo'], ['vegeta', 'raven', 'hulk'], 3);
    recordProgress(emptyProgress(), {
      delta: battleDelta(summarizeBattle(0, r.b), r.b, r.tally, [], ['goku', 'pikachu', 'gojo']),
      battle: r.b, team: ['goku', 'pikachu', 'gojo'], feitos: r.feitos, raioX: r.raioX,
      maiorAtraso: r.maiorAtraso, indice: 0, jornada: [],
    });
    expect(characters[0]!.hp).toBe(antes);
  });

  it('conta os dominados pelo grau, não por um contador solto', () => {
    const p = emptyProgress();
    expect(dominados(p)).toBe(0);
    const c = characters[0]!;
    const [, segundo, terceiro] = desafiosDe(c.id);
    const cheio = { ...p, mastery: { [c.id]: { usou: 1, [segundo!.feito]: segundo!.meta, [terceiro!.feito]: terceiro!.meta } } };
    expect(dominados(cheio)).toBe(1);
  });

  /*
   * O perfil antigo guardava objetivos diários e semanais. Apagá-los não pode
   * levar junto recordes de quem já jogava.
   */
  it('migra o perfil antigo sem apagar recordes nem conquistas', () => {
    const antigo = {
      journeys: 9, victories: 2, best: 10, wins: 37, champion: ['goku', 'vegeta', 'pikachu'],
      progress: {
        xp: 4200, title: 'Veterano', seen: ['goku'], unlocked: ['j-primeiro'],
        stats: { battles: 50 }, mastery: { goku: { usou: 9 } },
        daily: { key: '2026-01-01', items: [{ id: 'daily-play' }] },
        weekly: { key: '2026-01-01', items: [] },
      },
    };
    const memoria = new Map([['nexus-v1-profile', JSON.stringify(antigo)]]);
    (globalThis as { localStorage?: unknown }).localStorage = { getItem: (k: string) => memoria.get(k) ?? null };
    const p = loadProfile();
    expect(p.journeys).toBe(9);
    expect(p.best).toBe(10);
    expect(p.progress.xp).toBe(4200);
    expect(p.progress.unlocked).toEqual(['j-primeiro']);
    expect(p.progress.mastery.goku).toEqual({ usou: 9 });
    expect(p.progress.stats.battles).toBe(50);
    /* E os objetivos não voltam disfarçados. */
    expect((p.progress as unknown as { daily?: unknown }).daily).toBeUndefined();
    expect((p.progress as unknown as { weekly?: unknown }).weekly).toBeUndefined();
  });
});
