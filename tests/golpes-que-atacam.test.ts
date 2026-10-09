import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { HABILIDADES_QUE_PASSAM_A_ATACAR } from '../src/data/golpes-que-atacam';

/*
 * Pedido do jogador: "o Cólera do Dragão é um poder de ataque… ele pode até
 * dar um buff pra alguém, mas ele tem que atacar o oponente".
 */
const RIVAL = ['enemyWeak', 'enemyStrong', 'enemyCast', 'investigated', 'leastInvestigated', 'allEnemies', 'randomEnemy'];

describe('Habilidade com nome de ataque ataca', () => {
  it('o Cólera do Dragão, a Masenko e as outras batem no rival e continuam com o que já faziam', () => {
    for (const k of HABILIDADES_QUE_PASSAM_A_ATACAR) {
      const [id, i] = k.split(':');
      const s = byId[id!]!.skills[Number(i)]!;
      const golpe = s.effects[0]!;
      expect(golpe.kind, k).toBe('damage');
      expect(RIVAL, k).toContain(golpe.target ?? s.target);
      expect(s.effects.length, `${k} manteve o efeito de antes`).toBeGreaterThan(1);
    }
    expect(byId.shiryu!.skills[1]!.name).toBe('Cólera do Dragão');
  });
});
