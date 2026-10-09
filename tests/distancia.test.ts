import { describe, expect, it } from 'vitest';
import { byId, characters } from '../src/data/characters';
import { distanciaDoGolpe } from '../src/presentation/distancia';
import { familiaDe } from '../src/presentation/vfxProfiles';

/*
 * Pedido do jogador: golpe de perto leva o personagem até o alvo; golpe de
 * longe (a bigorna do Coiote, o escudo do Capitão) deixa ele no lugar.
 */
const d = (id: string, i?: number) => distanciaDoGolpe(id, i, familiaDe(byId[id]!, i));

describe('De perto ou de longe', () => {
  it('lâmina e soco vão até o alvo', () => {
    for (const [id, i] of [['sasuke'], ['wolverine'], ['sakura'], ['zenitsu', 0], ['vergil', 0], ['samuraijack', 0], ['kakashi', 1], ['minato', 1], ['captainmarvel'], ['taz']] as [string, number?][]) expect(d(id, i), `${id}:${i ?? 'b'}`).toBe('perto');
  });
  it('tiro, magia, bigorna, chicote e braço que estica ficam de longe', () => {
    for (const [id, i] of [['coiote'], ['captain'], ['batman'], ['frieren'], ['luffy'], ['piccolo'], ['simonbelmont', 0], ['thor'], ['ichigo', 0], ['bart']] as [string, number?][]) expect(d(id, i), `${id}:${i ?? 'b'}`).toBe('longe');
  });
  it('todo ataque básico tem a sua distância decidida', () => {
    const sem = characters.filter((c) => !d(c.id)).map((c) => c.id);
    expect(sem).toEqual([]);
  });
});
