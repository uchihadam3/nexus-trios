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
