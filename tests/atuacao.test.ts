/*
 * Atuação (adendo, parte 2): quem age se move, quem recebe reage — e cada um
 * do jeito certo para o tipo da ação. O movimento é CSS; aqui se confere o
 * que decide qual movimento e para onde.
 */
import { describe, expect, it } from 'vitest';

import { applyEffects, createBattle } from '../src/engine/battle';
import type { BattleEvent, Effect } from '../src/engine/types';
import { atuacao, type Medida } from '../src/presentation/acting';
import type { Beat, Family } from '../src/presentation/director';

/* Rivais em cima, seu trio embaixo, num palco de 390 × 600. */
const medida: Medida = {
  w: 390, h: 600, medal: 90,
  anchors: { 'enemy-0': { x: 17, y: 20 }, 'enemy-1': { x: 50, y: 22 }, 'enemy-2': { x: 83, y: 20 }, 'player-0': { x: 17, y: 80 }, 'player-1': { x: 50, y: 78 }, 'player-2': { x: 83, y: 80 } },
};

function beat(kind: BattleEvent['kind'], fonte: number, alvos: number[], efeitos: Effect[], family: Family, impacted: boolean): Beat {
  const b = createBattle(['sakura', 'gojo', 'naruto'], ['goku', 'vegeta', 'hulk'], 99);
  const before = structuredClone(b);
  const source = b.fighters[fonte]!, targets = alvos.map((i) => b.fighters[i]!);
  applyEffects(b, source, targets, efeitos);
  const event: BattleEvent = { id: 7, time: 0, kind, source: source.uid, target: targets[0]!.uid, skill: kind === 'skill' ? 0 : undefined, label: 'x' };
  return { event, events: [event, ...b.events], before, after: structuredClone(b), duration: 2, elapsed: impacted ? 1.2 : 0.4, impacted, family, grand: false };
}

describe('atuação', () => {
  it('corpo a corpo: avança até encostar no alvo, e o alvo só reage no impacto', () => {
    const antes = beat('basic', 0, [3], [{ kind: 'damage', value: 100 }], 'physical', false);
    const a = atuacao(antes, antes.after, medida, false);
    expect(a['player-0']?.act).toBe('melee');
    /* de (66, 480) até (66, 120): sobe 360 px, para a 0,82 × 90 px do alvo */
    expect(a['player-0']!.dx).toBeCloseTo(0, 1);
    expect(a['player-0']!.dy).toBeCloseTo(-(360 - 90 * 0.82), 0);
    expect(a['enemy-0']).toBeUndefined();
    const depois = beat('basic', 0, [3], [{ kind: 'damage', value: 100 }], 'physical', true);
    const b = atuacao(depois, depois.after, medida, false);
    expect(b['enemy-0']?.react).toBe('hit');
    /* empurrado para longe de quem bateu: para cima */
    expect(b['enemy-0']!.uy).toBeLessThan(-0.99);
  });

  it('à distância: só se inclina; quem recebe muito dano reage pesado', () => {
    const x = beat('basic', 1, [4], [{ kind: 'damage', value: 400 }], 'energy', true);
    const a = atuacao(x, x.after, medida, false);
    expect(a['player-1']?.act).toBe('ranged');
    expect(Math.hypot(a['player-1']!.dx, a['player-1']!.dy)).toBeLessThanOrEqual(26.01);
    expect(a['enemy-1']?.react).toBe('hit-heavy');
  });

  it('cura e Escudo: quem ajuda pulsa para o aliado, o aliado brilha', () => {
    const cura = beat('skill', 0, [2], [{ kind: 'heal', value: 150 }], 'heal', true);
    cura.before.fighters[2]!.hp -= 300; cura.after.fighters[2]!.hp -= 150;
    const a = atuacao(cura, cura.after, medida, false);
    expect(a['player-0']?.act).toBe('support');
    const esc = beat('skill', 1, [0], [{ kind: 'shield', value: 200 }], 'shield', true);
    expect(atuacao(esc, esc.after, medida, false)['player-0']?.react).toBe('shield');
  });

  it('debuff sem dano: quem lança amaldiçoa, o alvo ganha a névoa', () => {
    const x = beat('skill', 1, [3], [{ kind: 'status', status: 'exposed', value: 0.2, duration: 6 }], 'debuff', true);
    const a = atuacao(x, x.after, medida, false);
    expect(a['player-1']?.act).toBe('curse');
    expect(a['enemy-0']?.react).toBe('curse');
  });

  it('área: sobe e bate no chão, voltado para o meio dos alvos', () => {
    const x = beat('skill', 1, [3, 4, 5], [{ kind: 'damage', value: 120 }], 'psychic', true);
    const a = atuacao(x, x.after, medida, true);
    expect(a['player-1']?.act).toBe('area');
    expect(['enemy-0', 'enemy-1', 'enemy-2'].every((u) => a[u]?.react)).toBe(true);
  });

  it('nocaute: o alvo cai', () => {
    const x = beat('basic', 0, [3], [{ kind: 'damage', value: 5000 }], 'physical', true);
    expect(atuacao(x, x.after, medida, false)['enemy-0']?.react).toBe('fall');
  });

  it('a animação recomeça a cada beat: a paridade alterna', () => {
    const x = beat('basic', 0, [3], [{ kind: 'damage', value: 10 }], 'physical', false);
    const a = atuacao(x, x.after, medida, false)['player-0']!.parity;
    x.event = { ...x.event, id: 8 };
    expect(atuacao(x, x.after, medida, false)['player-0']!.parity).not.toBe(a);
  });
});
