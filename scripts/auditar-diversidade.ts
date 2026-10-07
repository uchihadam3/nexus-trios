/*
 * FASE C · a auditoria de diversidade mecânica dos 250.
 *
 * O teste de assinatura que já existe garante que nenhum par é **idêntico**.
 * Isso é o piso, e não é o que a direção pediu: ela pediu que, tirando nome e
 * retrato, dois personagens não pareçam a mesma ficha com números diferentes.
 * Identidade exata é fácil de evitar; semelhança não.
 *
 * Este script responde a quatro perguntas, e cada uma tem um critério
 * explícito, porque uma auditoria sem critério é uma opinião:
 *
 *   1. QUAIS PARES SÃO PARECIDOS DEMAIS
 *      Distância entre vetores de mecânica (gatilhos de Carga, alvos,
 *      condições, famílias de efeito, formato das três habilidades). Lista os
 *      mais próximos para revisão humana — não decide sozinho quem é clone.
 *
 *   2. QUE GATILHO ESTÁ MORTO
 *      Traço ou habilidade cujo gatilho nunca dispara na simulação. Um gatilho
 *      morto é texto na ficha que não acontece no jogo.
 *
 *   3. QUE EFEITO É INALCANÇÁVEL
 *      Habilidade que exige outra que nunca fica pronta, ou condição que o
 *      motor nunca satisfaz para aquele kit.
 *
 *   4. QUE CONTROLE É PERPÉTUO
 *      Paralisia, silêncio ou raiz cuja duração cobre o próprio tempo de
 *      recarga. Perma-stun não é build forte: é tirar o jogo do adversário.
 *
 * O script não conserta nada. Ele mede, e sai com código 1 se achar algo que
 * precise de decisão humana.
 */
import { writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import type { Character, Effect, StatusId } from '../src/engine/types';
import { createBattle, stepBattle } from '../src/engine/battle';

/* ---------------------------------------------------------------------------
 * 1 · semelhança entre pares
 * ------------------------------------------------------------------------- */

/** O vocabulário mecânico de um personagem, como conjuntos comparáveis. */
const vetor = (c: Character) => {
  const efeito = (e: Effect): string =>
    e.kind === 'status' ? `status:${e.status}` : e.kind === 'interrupt' ? `interrupt:${e.mode}` : e.kind;
  const todos = [c.basic, ...c.skills].flatMap((p) => p.effects);
  return {
    cargas: new Set(c.skills.flatMap((s) => s.charge.map((r) => r.on))),
    alvos: new Set([c.basic.target, ...c.skills.map((s) => s.target)]),
    condicoes: new Set(c.skills.map((s) => s.condition)),
    efeitos: new Set(todos.map(efeito)),
    tracoGatilho: c.trait.on,
    tracoEfeitos: new Set(c.trait.effects.map(efeito)),
    formato: c.skills.map((s) => `${s.preparation > 0 ? 'P' : '-'}${s.target.startsWith('all') ? 'A' : 'S'}`).join(''),
    /* Os números entram normalizados, para não dominarem a distância. */
    hp: c.hp / 1600,
    intervalo: c.interval / 5.5,
  };
};

const jaccard = <T,>(a: Set<T>, b: Set<T>): number => {
  if (a.size === 0 && b.size === 0) return 1;
  let comuns = 0;
  for (const x of a) if (b.has(x)) comuns += 1;
  return comuns / (a.size + b.size - comuns);
};

/** 0 = fichas mecanicamente idênticas, 1 = nada em comum. */
const distancia = (a: ReturnType<typeof vetor>, b: ReturnType<typeof vetor>): number => {
  const semelhanca =
    jaccard(a.cargas, b.cargas) * 0.26 +
    jaccard(a.alvos, b.alvos) * 0.14 +
    jaccard(a.condicoes, b.condicoes) * 0.12 +
    jaccard(a.efeitos, b.efeitos) * 0.26 +
    jaccard(a.tracoEfeitos, b.tracoEfeitos) * 0.1 +
    (a.tracoGatilho === b.tracoGatilho ? 0.06 : 0) +
    (a.formato === b.formato ? 0.06 : 0);
  const numerica = 1 - Math.min(1, Math.abs(a.hp - b.hp) + Math.abs(a.intervalo - b.intervalo));
  return 1 - (semelhanca * 0.88 + numerica * 0.12);
};

const vetores = new Map(characters.map((c) => [c.id, vetor(c)]));
const pares: { a: string; b: string; distancia: number }[] = [];
for (let i = 0; i < characters.length; i += 1) {
  for (let j = i + 1; j < characters.length; j += 1) {
    const ca = characters[i]!;
    const cb = characters[j]!;
    pares.push({ a: ca.name, b: cb.name, distancia: distancia(vetores.get(ca.id)!, vetores.get(cb.id)!) });
  }
}
pares.sort((x, y) => x.distancia - y.distancia);
/* Abaixo disto, duas fichas falam a mesma língua com sotaque diferente. */
const LIMITE_DE_SEMELHANCA = 0.08;
const paresProximos = pares.filter((p) => p.distancia < LIMITE_DE_SEMELHANCA);

/* ---------------------------------------------------------------------------
 * 2 e 3 · gatilhos mortos e efeitos inalcançáveis, pela simulação
 * ------------------------------------------------------------------------- */

/*
 * Vinte sementes, e não dez.
 *
 * Com dez, o Vazio Infinito do Gojo apareceu como "nunca sai". Medido à parte
 * em quarenta lutas, ele chega a 100 de Carga em seis e é lançado em cinco —
 * raro, não morto. Uma auditoria que confunde as duas coisas manda consertar
 * o que não está quebrado.
 */
const SEMENTES = 20;
const usoDeHabilidade = new Map<string, number[]>();
const tracoDisparou = new Map<string, number>();
const lutas = new Map<string, number>();

for (const [indice, c] of characters.entries()) {
  usoDeHabilidade.set(c.id, [0, 0, 0]);
  tracoDisparou.set(c.id, 0);
  lutas.set(c.id, 0);
  for (let s = 0; s < SEMENTES; s += 1) {
    /* Aliados e inimigos variados, para não medir sempre o mesmo confronto. */
    const outros = characters.filter((o) => o.id !== c.id);
    const pega = (n: number) => outros[(indice * 7 + s * 13 + n * 29) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 1);
    const meu = b.fighters[0]!;
    /*
     * O traço disparou? Observa-se o `traitTimer`, não os eventos.
     *
     * A primeira versão desta auditoria procurava um evento com o nome do
     * traço e concluiu que 220 dos 250 estavam mortos — 88% do elenco, o que
     * já era implausível o bastante para não ser publicado. O motor nunca
     * emite esse evento: quando um traço dispara ele chama `applyEffects`
     * direto, e os eventos que saem carregam o rótulo do efeito.
     *
     * O que o motor **faz** ao disparar é pôr o `traitTimer` em recarga. Uma
     * transição de zero para positivo é um disparo, e isso é observável sem
     * tocar no motor.
     */
    let disparos = 0;
    let antes = meu.traitTimer;
    for (let passo = 0; passo < 4200 && !b.finished; passo += 1) {
      stepBattle(b);
      if (antes <= 0 && meu.traitTimer > 0) disparos += 1;
      antes = meu.traitTimer;
    }
    lutas.set(c.id, lutas.get(c.id)! + 1);
    const usos = usoDeHabilidade.get(c.id)!;
    meu.skills.forEach((st, i) => { usos[i] = (usos[i] ?? 0) + st.uses; });
    tracoDisparou.set(c.id, tracoDisparou.get(c.id)! + disparos);
  }
}

const usoPorHabilidade = characters.flatMap((c) =>
  c.skills.map((s, i) => {
    const usos = usoDeHabilidade.get(c.id)![i] ?? 0;
    return { personagem: c.name, habilidade: s.name, usos, porLuta: usos / SEMENTES };
  }),
);
/** Nunca saiu em nenhuma semente: suspeita de trava estrutural. */
const habilidadesMortas = usoPorHabilidade.filter((x) => x.usos === 0);
/** Sai, mas quase nunca. É decisão de calibragem, não de estrutura. */
const habilidadesRaras = usoPorHabilidade
  .filter((x) => x.usos > 0 && x.porLuta < 0.2)
  .sort((a, b) => a.porLuta - b.porLuta);

/* ---------------------------------------------------------------------------
 * 4 · controle perpétuo
 * ------------------------------------------------------------------------- */

const TRAVAM: readonly StatusId[] = ['paralyzed', 'rooted', 'silenced'];

/*
 * Controle perpétuo, medido na luta — não na tabela.
 *
 * A primeira versão comparava duração do Status com a recarga da habilidade e
 * acusou 29 casos. O número é enganoso: a recarga não é o que limita uma
 * habilidade, a **Carga** é. Uma skill com recarga de 3 s que precisa de 100
 * de Carga pode sair uma vez a cada vinte segundos, e aí um `rooted` de 8 s
 * não tranca ninguém.
 *
 * O que importa é quanto da luta o inimigo passa de fato sem poder agir. Isso
 * se mede observando a luta, e é o que esta versão faz.
 */
const tempoTravado = new Map<string, { travado: number; total: number }>();
for (const [indice, c] of characters.entries()) {
  let travado = 0;
  let total = 0;
  for (let s = 0; s < SEMENTES; s += 1) {
    const outros = characters.filter((o) => o.id !== c.id);
    const pega = (n: number) => outros[(indice * 11 + s * 7 + n * 23) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 101);
    for (let passo = 0; passo < 4200 && !b.finished; passo += 1) {
      stepBattle(b);
      for (const f of b.fighters) {
        if (f.side === 'player' || f.hp <= 0) continue;
        total += 1;
        if (f.statuses.some((st) => TRAVAM.includes(st.id))) travado += 1;
      }
    }
  }
  tempoTravado.set(c.id, { travado, total });
}

/* Acima disto, o adversário passa mais tempo sem jogar do que jogando. */
const LIMITE_DE_TRAVA = 0.55;
const controlePerpetuo = characters
  .map((c) => {
    const m = tempoTravado.get(c.id)!;
    return { personagem: c.name, fracaoTravada: m.total > 0 ? m.travado / m.total : 0 };
  })
  .filter((x) => x.fracaoTravada >= LIMITE_DE_TRAVA)
  .sort((a, b) => b.fracaoTravada - a.fracaoTravada);

/* ---------------------------------------------------------------------------
 * O relatório
 * ------------------------------------------------------------------------- */

const tracosMortos = characters
  .filter((c) => (tracoDisparou.get(c.id) ?? 0) === 0)
  .map((c) => ({ personagem: c.name, traco: c.trait.name, gatilho: c.trait.on }));

const relatorio = {
  personagens: characters.length,
  sementesPorPersonagem: SEMENTES,
  paresComparados: pares.length,
  limiteDeSemelhanca: LIMITE_DE_SEMELHANCA,
  paresProximos: paresProximos.map((p) => ({ ...p, distancia: Number(p.distancia.toFixed(4)) })),
  maisProximos: pares.slice(0, 15).map((p) => ({ ...p, distancia: Number(p.distancia.toFixed(4)) })),
  habilidadesMortas,
  habilidadesRaras,
  tracosMortos,
  controlePerpetuo,
};

writeFileSync('docs/auditoria-diversidade.json', `${JSON.stringify(relatorio, null, 2)}\n`);

console.log(`personagens: ${String(characters.length)} | pares comparados: ${String(pares.length)}`);
console.log(`pares abaixo de ${String(LIMITE_DE_SEMELHANCA)}: ${String(paresProximos.length)}`);
for (const p of paresProximos.slice(0, 20)) console.log(`  ${p.distancia.toFixed(4)}  ${p.a}  ~  ${p.b}`);
console.log(`\nos 8 mais próximos do catálogo inteiro:`);
for (const p of pares.slice(0, 8)) console.log(`  ${p.distancia.toFixed(4)}  ${p.a}  ~  ${p.b}`);
console.log(`\nhabilidades que nunca saem (suspeita de trava): ${String(habilidadesMortas.length)}`);
for (const h of habilidadesMortas.slice(0, 12)) console.log(`  ${h.personagem} · ${h.habilidade}`);
console.log(`habilidades raras (<0,2 uso por luta, sai mas quase nunca): ${String(habilidadesRaras.length)}`);
for (const h of habilidadesRaras.slice(0, 8)) console.log(`  ${h.personagem} · ${h.habilidade} · ${h.porLuta.toFixed(2)}/luta`);
console.log(`traços que nunca disparam: ${String(tracosMortos.length)}`);
for (const t of tracosMortos.slice(0, 12)) console.log(`  ${t.personagem} · ${t.traco} (gatilho: ${t.gatilho})`);
console.log(`\ntrios cujo adversário passa >= ${String(LIMITE_DE_TRAVA * 100)}% da luta travado: ${String(controlePerpetuo.length)}`);
for (const c of controlePerpetuo.slice(0, 12))
  console.log(`  ${c.personagem}: ${(c.fracaoTravada * 100).toFixed(1)}% do tempo inimigo sem poder agir`);
const travaMedia = characters.reduce((soma, c) => {
  const m = tempoTravado.get(c.id)!;
  return soma + (m.total > 0 ? m.travado / m.total : 0);
}, 0) / characters.length;
console.log(`trava média do catálogo: ${(travaMedia * 100).toFixed(1)}%`);

if (paresProximos.length > 0 || habilidadesMortas.length > 0 || tracosMortos.length > 0 || controlePerpetuo.length > 0) {
  process.exitCode = 1;
}
