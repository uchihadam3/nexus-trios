/*
 * A regra do Light, nas palavras do dono do jogo: investiga um personagem; se
 * for vulnerável, usa a Death Note e ele morre; se não, ele toma o dano e fica
 * Exposto — e o Light sabe que é imune, não usa mais nele, e começa a
 * investigar outro.
 */
import { describe, expect, it } from 'vitest';

import { byId } from '../src/data/characters';
import { applyEffects, createBattle, targets } from '../src/engine/battle';

const investigar = byId.light!.skills[0]!.effects;
const deathNote = byId.light!.skills[2]!.effects;

const luta = () => {
  const b = createBattle(['light', 'sakura', 'naruto'], ['jerry', 'salsicha', 'goku'], 1);
  const [light, , , jerry, salsicha, goku] = b.fighters;
  return { b, light: light!, jerry: jerry!, salsicha: salsicha!, goku: goku! };
};

describe('Light Yagami', () => {
  it('continua investigando quem já começou, em vez de espalhar', () => {
    const { b, light, goku } = luta();
    light.investigation[goku.uid] = 30;
    expect(targets(b, light, 'investigated', investigar, false).map((f) => f.uid)).toEqual([goku.uid]);
  });

  it('Death Note no vulnerável investigado: elimina', () => {
    const { b, light, salsicha } = luta();
    expect(byId.salsicha!.deathNoteCompatible).toBe(true);
    light.investigation[salsicha.uid] = 100;
    light.discovered = { [salsicha.uid]: 'vulnerable' };
    expect(targets(b, light, 'investigated', deathNote, false).map((f) => f.uid)).toEqual([salsicha.uid]);
    applyEffects(b, light, [salsicha], deathNote);
    expect(salsicha.hp).toBe(0);
  });

  it('no imune: dano e Exposto uma vez só, e a investigação passa para outro', () => {
    const { b, light, jerry, goku } = luta();
    expect(byId.jerry!.deathNoteCompatible).toBe(false);
    light.investigation[jerry.uid] = 100;
    light.discovered = { [jerry.uid]: 'immune' };
    expect(targets(b, light, 'investigated', deathNote, false).map((f) => f.uid)).toEqual([jerry.uid]);

    const antes = jerry.hp;
    applyEffects(b, light, [jerry], deathNote);
    expect(jerry.hp).toBeGreaterThan(0);
    expect(jerry.hp).toBeLessThan(antes);
    expect(jerry.statuses.some((s) => s.id === 'exposed')).toBe(true);

    /* Já sabe: não usa de novo nele. */
    expect(targets(b, light, 'investigated', deathNote, false)).toEqual([]);
    /* E investiga outro. */
    light.investigation[goku.uid] = 10;
    expect(targets(b, light, 'investigated', investigar, false).map((f) => f.uid)).toEqual([goku.uid]);
  });
});
