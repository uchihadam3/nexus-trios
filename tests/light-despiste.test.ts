import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { createBattle, targets } from '../src/engine/battle';

/*
 * Tudo conforme o plano (pedido do jogador): despistar. O Light investiga um
 * rival para a Death Note e marca e enfraquece OUTRO — o menos investigado —
 * para o trio inteiro bater nesse enquanto ele prepara a execução.
 */
describe('Light: Tudo conforme o plano despista', () => {
  const plano = byId.light!.skills[1]!;
  it('a ficha diz o alvo certo', () => {
    expect(plano.name).toBe('Tudo conforme o plano');
    expect(plano.target).toBe('leastInvestigated');
    expect(plano.effects.some((e) => e.kind === 'status' && e.status === 'marked')).toBe(true);
    expect(plano.effects.some((e) => e.kind === 'status' && e.status === 'weakened')).toBe(true);
  });
  it('marca o rival menos investigado, não o que ele está investigando', () => {
    const b = createBattle(['light', 'goku', 'naruto'], ['saitama', 'thanos', 'hulk'], 3);
    const light = b.fighters.find((f) => f.characterId === 'light')!;
    const [r1, r2, r3] = b.fighters.filter((f) => f.side === 'enemy');
    light.investigation = { [r1!.uid]: 90, [r2!.uid]: 40, [r3!.uid]: 10 };
    expect(targets(b, light, plano.target, plano.effects).map((f) => f.uid)).toEqual([r3!.uid]);
    light.investigation = { [r1!.uid]: 5, [r2!.uid]: 70, [r3!.uid]: 30 };
    expect(targets(b, light, plano.target, plano.effects).map((f) => f.uid)).toEqual([r1!.uid]);
  });
});

/*
 * E o próprio Light ignora a marca que pôs (pedido do jogador: "o Light tem que
 * ignorar essa marcação… usar o ataque normal, a investigação e o Death Note em
 * outro personagem, que não tá marcado"). O trio dele continua focando no marcado.
 */
describe('Light: a marca é do plano, não dele', () => {
  const marcar = (b: ReturnType<typeof createBattle>, quem: string, de: string) => {
    b.fighters.find((f) => f.uid === quem)!.statuses.push({ id: 'marked', remaining: 10, intensity: 0.15, source: de });
  };
  it('o básico e a investigação vão em outro rival; o aliado mira no marcado', () => {
    for (const seed of [3, 7, 11, 19]) {
      const b = createBattle(['light', 'goku', 'naruto'], ['saitama', 'thanos', 'hulk'], seed);
      const light = b.fighters.find((f) => f.characterId === 'light')!;
      const goku = b.fighters.find((f) => f.characterId === 'goku')!;
      const [r1] = b.fighters.filter((f) => f.side === 'enemy');
      marcar(b, r1!.uid, light.uid);
      const c = byId.light!;
      expect(targets(b, light, c.basic.target, c.basic.effects).map((f) => f.uid), `básico, semente ${seed}`).not.toContain(r1!.uid);
      expect(targets(b, light, c.skills[0]!.target, c.skills[0]!.effects).map((f) => f.uid), `investigação, semente ${seed}`).not.toContain(r1!.uid);
      expect(targets(b, goku, byId.goku!.basic.target, byId.goku!.basic.effects).map((f) => f.uid), `aliado, semente ${seed}`).toContain(r1!.uid);
    }
  });
  it('a marca de outro personagem continua valendo para o Light', () => {
    const b = createBattle(['light', 'goku', 'naruto'], ['saitama', 'thanos', 'hulk'], 5);
    const light = b.fighters.find((f) => f.characterId === 'light')!;
    const goku = b.fighters.find((f) => f.characterId === 'goku')!;
    const [r1] = b.fighters.filter((f) => f.side === 'enemy');
    marcar(b, r1!.uid, goku.uid);
    light.discovered = {};
    expect(targets(b, light, byId.light!.basic.target, byId.light!.basic.effects).map((f) => f.uid)).toContain(r1!.uid);
  });
});
