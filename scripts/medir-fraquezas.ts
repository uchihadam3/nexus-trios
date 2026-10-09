/*
 * O que faz cada personagem perder — medido, não imaginado.
 *
 * O ponto fraco da ficha precisa responder "contra o quê ele é ruim e por que
 * perde". Este script simula lutas 3 contra 3 com trios sorteados e anota, para
 * cada lutador em cada luta:
 *
 * - se o trio dele venceu, e que identidades o trio rival tinha (Explosão,
 *   Interrupção, Controle, Cura…), para saber contra quem ele vence menos;
 * - quando caiu, e se caiu de um golpe grande (≥ 35% da Vida num beat);
 * - quantos Preparos começou e quantos foram cortados;
 * - quantos segundos passou preso, paralisado, silenciado ou confuso;
 * - quantos segundos passou Queimando, Envenenado ou Sangrando (dano contínuo);
 * - quantas vezes cada habilidade dele saiu, quanto dano ele causou e quanto
 *   tempo ficou de pé — o ponto fraco é o que ele não consegue fazer.
 *
 * Saída: docs/fraquezas-medidas.json. O texto de cada ponto fraco é escrito a
 * partir disso em scripts/escrever-fraquezas.ts.
 *
 * Uso: LUTAS=20000 npx tsx scripts/medir-fraquezas.ts
 */
import { writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import type { StatusId } from '../src/engine/types';
import { identidadesDe } from '../src/presentation/identities';

const LUTAS = Number(process.env.LUTAS ?? 20000);
const CONTROLE = new Set<StatusId>(['paralyzed', 'rooted', 'silenced', 'confused', 'frozen', 'sleep']);

interface Acumulado {
  id: string; lutas: number; vitorias: number;
  quedas: number; tempoDeQueda: number; primeiroACair: number; quedaPorGolpeGrande: number;
  preparos: number; preparosCortados: number; controleSegundos: number;
  danoRecebido: number; danoContinuoRecebido: number; duracaoMedia: number;
  usos: [number, number, number]; danoCausado: number; tempoDePe: number;
  /* identidade do trio rival → [lutas, vitórias] */
  contra: Record<string, [number, number]>;
}

const acc = new Map<string, Acumulado>(characters.map((c) => [c.id, {
  id: c.id, lutas: 0, vitorias: 0, quedas: 0, tempoDeQueda: 0, primeiroACair: 0, quedaPorGolpeGrande: 0,
  preparos: 0, preparosCortados: 0, controleSegundos: 0, danoRecebido: 0, danoContinuoRecebido: 0, duracaoMedia: 0, contra: {},
  usos: [0, 0, 0], danoCausado: 0, tempoDePe: 0,
}]));

/* Gerador simples e determinístico para sortear os trios. */
let semente = 20261008;
const sorteio = () => { semente = (Math.imul(semente, 1664525) + 1013904223) >>> 0; return semente / 4294967296; };
const trio = (fora: Set<string>) => {
  const ids: string[] = [];
  while (ids.length < 3) { const c = characters[Math.floor(sorteio() * characters.length)]!.id; if (!fora.has(c) && !ids.includes(c)) ids.push(c); }
  return ids;
};

const inicio = Date.now();
for (let luta = 0; luta < LUTAS; luta += 1) {
  const a = trio(new Set()), b0 = trio(new Set(a));
  const b = createBattle(a, b0, luta + 1);
  const idsDoLado = { player: new Set(a.flatMap((id) => identidadesDe(id))), enemy: new Set(b0.flatMap((id) => identidadesDe(id))) };
  let visto = -1, primeiraQueda: string | null = null;
  const danoNoBeat = new Map<string, { tempo: number; valor: number }>();
  const caiuDeGolpeGrande = new Set<string>();
  const controle = new Map<string, number>();
  const quedaDe = new Map<string, number>();
  for (let passo = 0; passo < 6000 && !b.finished; passo += 1) {
    stepBattle(b);
    for (const f of b.fighters) {
      if (f.hp <= 0) continue;
      if (f.statuses.some((s) => CONTROLE.has(s.id))) controle.set(f.uid, (controle.get(f.uid) ?? 0) + 0.1);
      if (f.statuses.some((s) => s.id === 'burning' || s.id === 'poison' || s.id === 'bleed')) acc.get(f.characterId)!.danoContinuoRecebido += 0.1;   // segundos queimando
    }
    for (const ev of b.events) {
      if (ev.id <= visto) continue;
      visto = ev.id;
      const alvo = ev.target ? b.fighters.find((f) => f.uid === ev.target) : undefined;
      const fonte = b.fighters.find((f) => f.uid === ev.source);
      if (ev.kind === 'cast' && fonte) acc.get(fonte.characterId)!.preparos += 1;
      if (ev.kind === 'skill' && fonte && ev.skill !== undefined && ev.skill < 3) acc.get(fonte.characterId)!.usos[ev.skill] += 1;
      if (ev.kind === 'damage' && alvo && fonte && fonte.side !== alvo.side) acc.get(fonte.characterId)!.danoCausado += ev.value ?? 0;
      if (ev.kind === 'interrupt' && alvo && ev.label === 'Interrompido!') acc.get(alvo.characterId)!.preparosCortados += 1;
      if (ev.kind === 'damage' && alvo && fonte && fonte.side !== alvo.side) {
        const m = acc.get(alvo.characterId)!;
        m.danoRecebido += ev.value ?? 0;
        // dano no mesmo instante soma como um golpe só
        const d = danoNoBeat.get(alvo.uid);
        const valor = d && Math.abs(d.tempo - ev.time) < 0.05 ? d.valor + (ev.value ?? 0) : (ev.value ?? 0);
        danoNoBeat.set(alvo.uid, { tempo: ev.time, valor });
      }
      if (ev.kind === 'ko' && alvo) {
        const m = acc.get(alvo.characterId)!;
        m.quedas += 1; m.tempoDeQueda += b.time; quedaDe.set(alvo.uid, b.time);
        if (!primeiraQueda) { primeiraQueda = alvo.uid; m.primeiroACair += 1; }
        const d = danoNoBeat.get(alvo.uid);
        if (d && Math.abs(d.tempo - ev.time) < 0.05 && d.valor >= alvo.maxHp * 0.35) caiuDeGolpeGrande.add(alvo.uid);
      }
    }
  }
  for (const f of b.fighters) {
    const m = acc.get(f.characterId)!;
    m.lutas += 1; m.duracaoMedia += b.time; m.tempoDePe += quedaDe.get(f.uid) ?? b.time;
    const venceu = b.winner === f.side;
    if (venceu) m.vitorias += 1;
    if (caiuDeGolpeGrande.has(f.uid)) m.quedaPorGolpeGrande += 1;
    m.controleSegundos += controle.get(f.uid) ?? 0;
    for (const id of idsDoLado[f.side === 'player' ? 'enemy' : 'player']) {
      const par = (m.contra[id] ??= [0, 0]);
      par[0] += 1; if (venceu) par[1] += 1;
    }
  }
  if (luta % 2000 === 1999) console.log(`${luta + 1} lutas · ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
}

const saida = [...acc.values()].map((m) => ({
  ...m,
  vitorias: +(m.vitorias / m.lutas).toFixed(4),
  tempoDeQueda: m.quedas ? +(m.tempoDeQueda / m.quedas).toFixed(2) : null,
  taxaDeQueda: +(m.quedas / m.lutas).toFixed(4),
  primeiroACair: +(m.primeiroACair / m.lutas).toFixed(4),
  quedaPorGolpeGrande: m.quedas ? +(m.quedaPorGolpeGrande / m.quedas).toFixed(4) : 0,
  cortados: m.preparos ? +(m.preparosCortados / m.preparos).toFixed(4) : 0,
  controleSegundos: +(m.controleSegundos / m.lutas).toFixed(2),
  danoRecebido: +(m.danoRecebido / m.lutas).toFixed(1),
  danoContinuoRecebido: +(m.danoContinuoRecebido / m.lutas).toFixed(1),
  duracaoMedia: +(m.duracaoMedia / m.lutas).toFixed(2),
  usos: m.usos.map((u) => +(u / m.lutas).toFixed(3)),
  danoCausado: +(m.danoCausado / m.lutas).toFixed(1),
  tempoDePe: +(m.tempoDePe / m.lutas).toFixed(2),
  contra: Object.fromEntries(Object.entries(m.contra).map(([k, [n, v]]) => [k, { lutas: n, vitorias: +(v / n).toFixed(4) }])),
}));
writeFileSync('docs/fraquezas-medidas.json', JSON.stringify({ lutas: LUTAS, medidas: saida }, null, 1) + '\n');
console.log(`pronto: ${LUTAS} lutas em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
