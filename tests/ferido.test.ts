import { describe, expect, it } from 'vitest';
import { byId, characters } from '../src/data/characters';
import { condicaoAtendida, createBattle } from '../src/engine/battle';
import { alvosDoFerido } from '../src/engine/ferido';

/*
 * "Alvo ferido" (pedido do jogador): numa habilidade que cura ou protege o
 * trio, a Vida que importa é a de quem recebe a cura — nunca a do inimigo.
 */
const DO_TRIO = ['self', 'allyWeak', 'allAllies', 'allyStrongest'];
describe('Alvo ferido', () => {
  it('toda habilidade com cura ou proteção olha a Vida do próprio trio', () => {
    for (const c of characters) for (const s of c.skills) {
      if (s.condition !== 'injured') continue;
      const cura = s.effects.some((e) => (e.kind === 'heal' || e.kind === 'shield') && DO_TRIO.includes(e.target ?? s.target));
      if (cura) expect(alvosDoFerido(s).every((t) => DO_TRIO.includes(t)), `${c.name} · ${s.name}`).toBe(true);
    }
  });

  it('o Golpe Fantasma do Ikki (cura a si mesmo) espera ele estar ferido, não o rival', () => {
    const indice = byId.ikki.skills.findIndex((s) => s.name === 'Golpe Fantasma');
    const b = createBattle(['ikki', 'goku', 'naruto'], ['saitama', 'thanos', 'hulk'], 3);
    const ikki = b.fighters.find((f) => f.characterId === 'ikki')!;
    for (const r of b.fighters.filter((f) => f.side === 'enemy')) r.hp = Math.round(r.maxHp * 0.5);
    expect(condicaoAtendida(b, ikki, byId.ikki.skills[indice]!)).toBe(false);
    ikki.hp = Math.round(ikki.maxHp * 0.5);
    expect(condicaoAtendida(b, ikki, byId.ikki.skills[indice]!)).toBe(true);
  });
});
