import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';

/*
 * A Autodestruição do Cell. Arma só com o Cell de pé, entre 1 de Vida e 20% (pedido do jogador: "o Cell não pode
 * morrer pra isso acontecer… se ele morrer, ele ativa a regeneração dele"). Armada, sempre explode (pedido do
 * jogador: "se alguém curar ele e voltar à vida, a autodestruição tem que acontecer de qualquer maneira"): curado,
 * explode no tempo marcado; caiu na contagem, explode na hora em que cai.
 */
describe('Autodestruição do Cell', () => {
  it('só arma com o Cell de pé, e armada sempre explode (curado ou caído)', () => {
    let armou = 0, explodiu = 0, caidoExplodiu = 0, curadoExplodiu = 0;
    for (let semente = 1; semente <= 80; semente++) {
      const b = createBattle(['cell', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const cell = b.fighters.find((f) => f.characterId === 'cell')!;
      let visto = b.nextEvent, armado = false, curou = false, caiu = false;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        for (const e of b.events.filter((x) => x.id >= visto)) {
          if (e.kind === 'unica' && e.source === cell.uid && e.label === 'Vai explodir!') {
            const novos = b.events.filter((x) => x.id >= visto);
            if (cell.hp <= 0) expect(novos.some((x) => x.kind === 'ko' && x.target === cell.uid && x.id > e.id), `semente ${semente}: armou com o Cell de pé`).toBe(true);
            armou++; armado = true; curou = false; caiu = false;
          }
          if (armado && e.kind === 'heal' && e.target === cell.uid) curou = true;
          if (armado && e.kind === 'ko' && e.target === cell.uid) caiu = true;
          if (e.kind === 'unica' && e.source === cell.uid && e.label === 'Autodestruição') {
            explodiu++; armado = false;
            if (caiu) caidoExplodiu++;
            if (curou) curadoExplodiu++;
          }
        }
        visto = b.nextEvent;
      }
      // armou e a luta acabou sem explodir só se a luta terminou na própria contagem
      if (armado) expect(b.finished, `semente ${semente}: armou e não explodiu`).toBe(true);
    }
    expect(armou).toBeGreaterThan(0);
    expect(explodiu).toBeGreaterThan(0);
    console.log({ armou, explodiu, caidoExplodiu, curadoExplodiu });
  });
});
