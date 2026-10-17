import { describe, it, expect } from 'vitest';
import { byId } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';

/*
 * Pedido do dono: "o Lançar teia fala que vai no inimigo, mas o efeito mostra nele mesmo". Quem mira o rival em Preparo
 * disparava sem ninguém preparando: a habilidade saía no vazio e a tela desenhava o golpe em quem usou.
 */
describe('alvo das habilidades', () => {
  it('as de "rival em Preparo" só saem com um rival para acertar', () => {
    const quem = ['spiderman', 'wonderwoman', 'magneto', 'pantera', 'anubis', 'jackskellington'];
    let usos = 0;
    for (let semente = 1; semente <= 40; semente++) {
      const b = createBattle(quem.slice(0, 3), quem.slice(3), semente, 1);
      const lado = new Map(b.fighters.map((f) => [f.uid, f]));
      let visto = -1;
      for (let k = 0; k < 9000 && !b.finished; k++) {
        stepBattle(b);
        for (const e of b.events) {
          if (e.id <= visto) continue;
          visto = e.id;
          if (e.kind !== 'skill' || e.skill === undefined) continue;
          const f = lado.get(e.source)!, s = byId[f.characterId]!.skills[e.skill]!;
          if (s.target !== 'enemyCast' && s.target !== 'allyFallen') continue;
          usos++;
          const alvo = e.target ? lado.get(e.target) : undefined;
          expect(alvo, `${s.name} saiu sem alvo`).toBeDefined();
          expect(alvo!.side === f.side, `${s.name} acertou o lado errado`).toBe(s.target === 'allyFallen');
        }
      }
    }
    expect(usos).toBeGreaterThan(20);
  });
});
