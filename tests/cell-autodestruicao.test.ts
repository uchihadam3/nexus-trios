import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';

/*
 * A Autodestruição do Cell (pedido do jogador: "o Cell não pode morrer pra isso acontecer… tem que ficar entre 1 de
 * Vida e 20% da Vida… se ele morrer, ele ativa a regeneração dele, não ativa esse negócio").
 */
describe('Autodestruição do Cell', () => {
  it('só arma com o Cell de pé, e cair durante a contagem cancela a explosão', () => {
    let armou = 0, explodiu = 0, cancelou = 0;
    for (let semente = 1; semente <= 60; semente++) {
      const b = createBattle(['cell', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const cell = b.fighters.find((f) => f.characterId === 'cell')!;
      let visto = b.nextEvent, armadoEm = -1, caiuDepois = false;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        for (const e of b.events.filter((x) => x.id >= visto)) {
          if (e.kind === 'unica' && e.source === cell.uid && e.label === 'Vai explodir!') {
            expect(cell.hp, `semente ${semente}: armou com o Cell de pé`).toBeGreaterThan(0);
            armou++; armadoEm = e.id; caiuDepois = false;
          }
          if (e.kind === 'ko' && e.target === cell.uid && armadoEm > 0) { caiuDepois = true; cancelou++; }
          if (e.kind === 'unica' && e.source === cell.uid && e.label === 'Autodestruição') {
            expect(caiuDepois, `semente ${semente}: explodiu depois de cair`).toBe(false);
            explodiu++;
          }
        }
        visto = b.nextEvent;
      }
    }
    expect(armou).toBeGreaterThan(0);
    expect(explodiu).toBeGreaterThan(0);
    console.log({ armou, explodiu, cancelou });
  });
});
