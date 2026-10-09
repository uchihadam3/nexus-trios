import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { newDraft, pickDraft, skipDraft } from '../src/engine/campaign';

/*
 * Pedido do jogador: "a chance de qualquer um aparecer tem que ser a mesma".
 * Conta quantas vezes cada personagem aparece em todas as telas da escolha
 * (a primeira, a troca e as que vêm depois de escolher) e faz o teste do
 * qui-quadrado: com o sorteio justo ele fica perto de 249 (os graus de
 * liberdade); o defeito antigo da troca dava ~450.
 */
describe('sorteio da escolha do trio', () => {
  it('todo personagem tem a mesma chance de aparecer, em todas as telas', () => {
    const ids = characters.map((c) => c.id), vezes = new Map(ids.map((i) => [i, 0]));
    let telas = 0, r = 12345;
    const conta = (c: string[]) => { telas++; for (const id of c) vezes.set(id, vezes.get(id)! + 1); };
    for (let n = 0; n < 40000; n++) {
      r = (Math.imul(r, 2654435761) + 97) >>> 0;
      let d = newDraft(r);
      conta(d.candidates); d = skipDraft(d); conta(d.candidates);
      while (d.team.length < 3) { d = pickDraft(d, d.candidates[n % 3]!); if (d.team.length < 3) conta(d.candidates); }
    }
    const esperado = (telas * 3) / ids.length, gl = ids.length - 1;
    const qui = [...vezes.values()].reduce((s, x) => s + (x - esperado) ** 2 / esperado, 0);
    // p ≈ 0,001: só falha com um vício de verdade
    expect(qui).toBeLessThan(gl + 3.1 * Math.sqrt(2 * gl));
  });

  it('a troca sorteia de novo: a tela seguinte não repete nem se amarra à primeira', () => {
    const d = newDraft(42), t = skipDraft(d);
    expect(t.rng).not.toBe(d.rng);
    expect(t.candidates.some((id) => d.candidates.includes(id))).toBe(false);
    expect(newDraft(42).rng).not.toBe(42);
  });
});
