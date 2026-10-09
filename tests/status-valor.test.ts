/*
 * O valor de um Status ao tocar nele na batalha.
 *
 * O pedido, nas palavras do jogador: "aplicou 10% de Exposto, você clica, tá
 * 10%. Aí o outro aplica mais 20, acumula pra 30. Você consegue ver lá que tá
 * 30% exposto agora." Estes testes usam o motor de verdade para somar.
 */
import { describe, expect, it } from 'vitest';

import { applyEffects, createBattle } from '../src/engine/battle';
import { tetoDoStatus, valorAtualDoStatus } from '../src/engine/skill-descriptions';
import type { Effect } from '../src/engine/types';

const exposto = (value: number): Effect => ({ kind: 'status', status: 'exposed', value, duration: 6 });

describe('valor do Status na batalha', () => {
  it('10% de Exposto, mais 20%: tocando, aparece 30%', () => {
    const b = createBattle(['sakura', 'gojo', 'naruto'], ['goku', 'vegeta', 'hulk'], 7);
    const [sakura, gojo, , goku] = b.fighters;
    applyEffects(b, sakura, [goku], [exposto(0.10)]);
    const primeiro = goku.statuses.find((s) => s.id === 'exposed')!;
    expect(valorAtualDoStatus('exposed', primeiro.intensity)).toBe('10%');
    applyEffects(b, gojo, [goku], [exposto(0.20)]);
    const depois = goku.statuses.find((s) => s.id === 'exposed')!;
    expect(valorAtualDoStatus('exposed', depois.intensity)).toBe('30%');
  });

  it('nunca passa do teto, e diz qual é', () => {
    expect(valorAtualDoStatus('exposed', 2)).toBe('65%');
    expect(tetoDoStatus('exposed')).toBe('65%');
  });

  it('os de Vida mostram Vida por segundo', () => {
    expect(valorAtualDoStatus('burning', 12)).toBe('12 de Vida/s');
    expect(tetoDoStatus('burning')).toBe('30 de Vida/s');
    // a Regeneração não soma: vale a mais forte (o número escrito é o que cura)
    expect(tetoDoStatus('regen')).toBeNull();
  });

  it('quem só renova não tem teto de soma', () => {
    expect(tetoDoStatus('slow')).toBeNull();
    expect(valorAtualDoStatus('slow', 0.22)).toBe('22%');
  });

  it('quem não tem intensidade não mostra número', () => {
    for (const id of ['paralyzed', 'silenced', 'confused'] as const) expect(valorAtualDoStatus(id, 1)).toBeNull();
  });
});
