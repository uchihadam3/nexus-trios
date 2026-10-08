import { describe, expect, it } from 'vitest';
import { characters, byId } from '../src/data/characters';
import { presentTrait } from '../src/engine/skill-descriptions';

/*
 * Quando o traço ativa, dito do jeito que o motor faz (pedido do jogador):
 * traço de tempo diz "a cada N s", sem "resfriamento" — o resfriamento é o
 * próprio intervalo; traço de evento diz o evento e, se houver resfriamento, o
 * limite "no máximo 1 vez a cada N s". Nada de "a cada 100 de dano" num traço
 * que ativa a cada golpe.
 */
describe('texto de quando o traço ativa', () => {
  it('tempo: só o intervalo; evento: o evento e o limite', () => {
    for (const c of characters) {
      const p = presentTrait(c.trait);
      expect(p.quando, c.id).not.toMatch(/resfriamento|por segundo/i);
      if (['time', 'survived', 'winning', 'losing'].includes(c.trait.on)) {
        expect(p.quando, c.id).toMatch(/^A cada \d+(,\d+)? s/);
        expect(p.frequency, c.id).toBe('');
      } else {
        expect(p.quando, c.id).not.toMatch(/100 de dano/);
        if (c.trait.cooldown >= 0.5) expect(p.quando, c.id).toMatch(/no máximo 1 vez a cada \d+(,\d+)? s$/);
      }
    }
  });
  it('os exemplos do jogador', () => {
    expect(presentTrait(byId.nezuko.trait).quando).toBe('A cada 2 s');
    expect(presentTrait(byId.donald.trait).quando).toBe('Ao receber dano · no máximo 1 vez a cada 3 s');
  });
});
