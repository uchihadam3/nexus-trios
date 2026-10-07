/*
 * O que a ficha promete, o combate entrega.
 *
 * Esta suíte nasceu de uma pergunta sobre duas linhas repetidas na ficha da
 * Tempestade. Puxando o fio, o que apareceu foi bem maior: 80 efeitos
 * ofensivos caíam no próprio time porque herdavam o alvo de habilidades de
 * apoio. Em 30 lutas com Sakura, Piccolo e Ichigo juntos, isso era 16.158 de
 * dano e 46 debuffs no trio do jogador.
 *
 * Nenhum teste pegava, porque todos perguntavam se o motor fazia o que o dado
 * mandava — e fazia. A pergunta que faltava era se o dado mandava o que a
 * ficha dizia.
 */
import { describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import { createBattle, negativeStatuses, stepBattle } from '../src/engine/battle';
import { positiveStatuses } from '../src/engine/skill-descriptions';
import type { Character, Effect, StatusId, Target } from '../src/engine/types';

const ALIADOS: readonly Target[] = ['self', 'allyWeak', 'allAllies'];
const ehAliado = (t: Target) => ALIADOS.includes(t);

const partesDe = (c: Character) => [
  { onde: `traço "${c.trait.name}"`, effects: c.trait.effects as readonly Effect[], alvo: c.trait.target },
  { onde: 'ataque básico', effects: c.basic.effects as readonly Effect[], alvo: c.basic.target },
  ...c.skills.map((s) => ({ onde: `"${s.name}"`, effects: s.effects as readonly Effect[], alvo: s.target })),
];

describe('a ficha e o combate concordam', () => {
  /*
   * Mirar `self` é uma decisão de quem escreveu o personagem — a Sailor Moon
   * tem um traço chamado "Preço do cuidado" que cura o aliado ferindo ela, o
   * Akuma fica Exposto ao soltar o Shun Goku Satsu. Cair num aliado por falta
   * de alvo próprio é outra coisa: é descuido, e o jogador paga.
   */
  it('nenhum efeito ofensivo cai em aliado sem ser custo declarado', () => {
    const errados: string[] = [];
    for (const c of characters) {
      for (const { onde, effects, alvo } of partesDe(c)) {
        for (const e of effects) {
          const alvoReal = e.target ?? alvo;
          if (!ehAliado(alvoReal) || e.target === 'self') continue;
          const ofensivo = e.kind === 'damage' || e.kind === 'interrupt'
            || (e.kind === 'status' && statuses[e.status].tone === 'negativo');
          if (ofensivo) errados.push(`${c.name} · ${onde}: ${e.kind} em ${alvoReal}`);
        }
      }
    }
    expect(errados).toEqual([]);
  });

  it('nenhuma cura, escudo ou buff cai em inimigo', () => {
    const errados: string[] = [];
    for (const c of characters) {
      for (const { onde, effects, alvo } of partesDe(c)) {
        for (const e of effects) {
          const alvoReal = e.target ?? alvo;
          if (ehAliado(alvoReal)) continue;
          const apoio = e.kind === 'heal' || e.kind === 'shield'
            || (e.kind === 'status' && statuses[e.status].tone === 'positivo');
          if (apoio) errados.push(`${c.name} · ${onde}: ${e.kind} em ${alvoReal}`);
        }
      }
    }
    expect(errados).toEqual([]);
  });

  /*
   * `applyStatus` fecha a intensidade no teto. Uma aplicação escrita acima do
   * teto é um número que aparece na ficha e nunca acontece.
   */
  it('nenhum Status anuncia mais do que o seu teto', () => {
    const acima: string[] = [];
    for (const c of characters) {
      for (const { onde, effects } of partesDe(c)) {
        for (const e of effects) {
          if (e.kind !== 'status') continue;
          const teto = statuses[e.status].cap;
          if (e.value > teto) acima.push(`${c.name} · ${onde}: ${statuses[e.status].name} ${String(e.value)} > ${String(teto)}`);
        }
      }
    }
    expect(acima).toEqual([]);
  });

  /*
   * Status de renovação se resolvem por `Math.max` nos dois campos. Duas
   * aplicações no mesmo alvo, em que a segunda é menor ou igual nos dois, são
   * uma linha a mais na ficha e nenhuma diferença no combate.
   */
  it('nenhuma habilidade mostra uma linha que o motor ignora', () => {
    const mortas: string[] = [];
    for (const c of characters) {
      for (const { onde, effects, alvo } of partesDe(c)) {
        const aplicados = effects.flatMap((e, i) =>
          e.kind === 'status' && statuses[e.status].stack !== 'add'
            ? [{ i, s: e.status, alvo: e.target ?? alvo, v: e.value, d: e.duration }] : []);
        for (const a of aplicados) {
          const domina = aplicados.find((o) => o.i !== a.i && o.s === a.s && o.alvo === a.alvo
            && o.v >= a.v && o.d >= a.d && (o.v > a.v || o.d > a.d || o.i < a.i));
          if (domina) mortas.push(`${c.name} · ${onde}: ${statuses[a.s].name} ${String(a.v)}/${String(a.d)}s`);
        }
      }
    }
    expect(mortas).toEqual([]);
  });

  it('toda habilidade tem como ficar pronta', () => {
    for (const c of characters) {
      for (const s of c.skills) {
        const total = s.charge.reduce((t, r) => t + r.amount, 0);
        expect(total, `${c.name} · ${s.name}`).toBeGreaterThan(0);
      }
    }
  });

  /*
   * `requiresSkills` guarda índices, não ids — o motor faz `f.skills[index]`.
   * Uma habilidade que exige a si mesma nunca sai.
   */
  it('nenhuma corrente de habilidades é impossível', () => {
    for (const c of characters) {
      c.skills.forEach((s, i) => {
        for (const req of s.requiresSkills ?? []) {
          const indice = Number(req);
          expect(Number.isInteger(indice), `${c.name} · ${s.name}: "${req}"`).toBe(true);
          expect(indice, `${c.name} · ${s.name}`).toBeGreaterThanOrEqual(0);
          expect(indice, `${c.name} · ${s.name}`).toBeLessThan(c.skills.length);
          expect(indice, `${c.name} · ${s.name} exige a si mesma`).not.toBe(i);
        }
      });
    }
  });

  /* As duas listas de tom derivam de `statuses`; se divergirem, é silencioso. */
  it('positivo e negativo cobrem todos os Status, sem sobreposição', () => {
    const ids = Object.keys(statuses) as StatusId[];
    for (const id of ids) {
      const p = positiveStatuses.has(id), n = negativeStatuses.has(id);
      expect(p !== n, `${id}: positivo=${String(p)} negativo=${String(n)}`).toBe(true);
    }
    expect(positiveStatuses.size + negativeStatuses.size).toBe(ids.length);
  });

  /*
   * E a prova em combate, que é a única que não depende da minha leitura dos
   * dados estar certa.
   */
  it('ninguém fere o próprio trio em 30 lutas, fora os custos declarados', () => {
    const custoDeclarado = new Set(characters
      .filter((c) => partesDe(c).some(({ effects }) => effects.some((e) => e.target === 'self'
        && (e.kind === 'damage' || (e.kind === 'status' && statuses[e.status].tone === 'negativo')))))
      .map((c) => c.id));

    const feridos: string[] = [];
    for (let semente = 1; semente <= 30; semente += 1) {
      const b = createBattle(['sakura', 'piccolo', 'ichigo'], ['vegeta', 'raven', 'hulk'], semente);
      let visto = 0;
      for (let passo = 0; passo < 4200 && !b.finished; passo += 1) {
        stepBattle(b);
        for (const ev of b.events) {
          if (ev.id <= visto) continue;
          visto = ev.id;
          const fonte = b.fighters.find((f) => f.uid === ev.source);
          const alvo = b.fighters.find((f) => f.uid === ev.target);
          if (!fonte || !alvo || fonte.side !== alvo.side || fonte.uid === alvo.uid) continue;
          if (custoDeclarado.has(fonte.characterId)) continue;
          if (ev.kind === 'damage') feridos.push(`${fonte.characterId} causou ${String(Math.round(ev.value ?? 0))} de dano em ${alvo.characterId}`);
          if (ev.kind === 'status' && ev.status && negativeStatuses.has(ev.status as StatusId)) {
            feridos.push(`${fonte.characterId} aplicou ${ev.status} em ${alvo.characterId}`);
          }
        }
      }
    }
    expect(feridos.slice(0, 5)).toEqual([]);
  });
});
