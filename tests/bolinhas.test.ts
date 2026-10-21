import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { bolinhaNaTela } from '../src/presentation/bolinha-da-unica';
import { BOLINHAS, bolinhaDe } from '../src/presentation/bolinhas';
import { unicaDe } from '../src/engine/unicas';

describe('a bolinha da Mecânica única', () => {
  it('todo personagem tem a sua (e só personagens que existem)', () => {
    const ids = new Set(characters.map((c) => c.id));
    expect(Object.keys(BOLINHAS).filter((k) => !ids.has(k))).toEqual([]);
    expect(characters.filter((c) => !BOLINHAS[c.id]).map((c) => c.id)).toEqual([]);
  });

  // pedido do dono: "na bolinha… ainda tá mostrando 30" (a Genki Dama sai aos 25 s): o número da bolinha é o do texto
  it('conta o mesmo tempo, a mesma Vida e a mesma chance que o texto da Mecânica única', () => {
    const pct = (x: number) => `${String(Math.round(x * 1000) / 10).replace('.', ',')}%`;
    for (const [id, b] of Object.entries(BOLINHAS)) {
      const texto = unicaDe(id)?.texto ?? '';
      if (b.modo === 'tempo' && b.em !== undefined) expect(texto, id).toMatch(new RegExp(`\\b${b.em} s`));
      if (b.modo === 'vida') for (const l of b.lim ?? []) expect(texto, id).toContain(pct(l));
      if (b.modo === 'chance' && b.p !== undefined) expect([pct(b.p), `${Math.round(b.p * 100)}%`].some((x) => texto.includes(x)), `${id}: ${texto}`).toBe(true);
    }
  });

  it('nunca quebra nem mostra texto grande demais numa luta de verdade', () => {
    const ids = characters.map((c) => c.id);
    for (let n = 0; n < ids.length; n += 3) {
      const time = [ids[n]!, ids[(n + 1) % ids.length]!, ids[(n + 2) % ids.length]!];
      const rivais = [ids[(n + 7) % ids.length]!, ids[(n + 11) % ids.length]!, ids[(n + 13) % ids.length]!];
      if (new Set([...time, ...rivais]).size < 6) continue;
      const b = createBattle(time, rivais, n);
      for (let t = 0; t < 600 && !b.finished; t++) {
        stepBattle(b);
        if (t % 50) continue;
        for (const f of b.fighters) {
          const tela = bolinhaNaTela(bolinhaDe(f.characterId), f, b);
          expect(Number.isFinite(tela.carga), f.characterId).toBe(true);
          expect(tela.carga, f.characterId).toBeGreaterThanOrEqual(0);
          expect(tela.carga, f.characterId).toBeLessThanOrEqual(1);
          expect((tela.texto ?? '').length, `${f.characterId}: ${tela.texto}`).toBeLessThanOrEqual(3);
        }
      }
    }
  });
});
