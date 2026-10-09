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
    expect(presentTrait(byId.kenpachi.trait).quando).toBe('Ao receber dano · no máximo 1 vez a cada 3 s');
  });
});

/*
 * Ponto fraco de verdade (pedido do jogador): cada um diz contra o quê o
 * personagem perde e por quê, com algo dele (Vida, golpe, traço), sem frase
 * genérica repetida.
 */
import { fraquezas } from '../src/data/fraquezas';
describe('pontos fracos', () => {
  it('todos têm um ponto fraco próprio, com o contra-quê e o porquê', () => {
    const textos = characters.map((c) => c.vulnerability);
    expect(new Set(textos).size).toBeGreaterThanOrEqual(characters.length - 4);
    for (const c of characters) {
      expect(c.vulnerability, c.id).toBe(fraquezas[c.id]);
      expect(c.vulnerability, c.id).toMatch(/^(Contra|Em luta longa|Depende do momento|Precisa apanhar)[^:]*: .{40,}/);
      expect(c.vulnerability.length, c.id).toBeLessThanOrEqual(240);
    }
    expect(byId.donald.vulnerability).not.toMatch(/perde o controle/i);
  });
});

/*
 * Traços próprios (pedido do jogador: "tem que ser mais criativo nos
 * traços… individualidade"): nenhum traço repetido entre os 250.
 */
describe('traço próprio de cada um', () => {
  it('os 250 têm traços com nomes diferentes', () => {
    expect(new Set(characters.map((c) => c.trait.name)).size).toBe(characters.length);
  });
  it('alguns da lore: Blaze do Charizard, Fênix da Jean Grey, caixa do Snake, chá do Iroh', () => {
    expect(byId.charizard!.trait).toMatchObject({ name: 'Blaze', on: 'losing' });
    expect(byId.jeangrey!.trait.effects[0]).toMatchObject({ kind: 'heal' });
    expect(byId.snake!.trait.effects[0]).toMatchObject({ kind: 'status', status: 'evasion' });
    expect(byId.iroh!.trait.effects[0]).toMatchObject({ kind: 'heal', target: 'allAllies' });
  });
});
