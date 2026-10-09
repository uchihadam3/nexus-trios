import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { condicaoAtendida, createBattle } from '../src/engine/battle';
import { presentSkill } from '../src/engine/skill-descriptions';

/*
 * Pergunta do jogador: o Majin Boo ficou com a Regeneração total pronta e não
 * usou — onde está escrito que ela precisa de um rival vulnerável? A regra
 * fica (a habilidade só sai quando ela é cumprida), mas tem que estar à vista:
 * "Só usa quando…" em destaque, e "esperando a regra de uso" na batalha.
 */
describe('a regra de uso fica à vista', () => {
  it('toda habilidade com regra mostra "Só usa quando…"; as sem regra, não', () => {
    for (const c of Object.values(byId)) for (const s of c.skills) {
      const p = presentSkill(s);
      if (s.condition === 'always') expect(p.requisito, `${c.name} · ${s.name}`).toBeUndefined();
      else expect(p.requisito, `${c.name} · ${s.name}`).toMatch(/^Só usa quando /);
    }
    expect(presentSkill(byId.majinbuu!.skills[2]!).requisito).toMatch(/Exposto, Marcado, Paralisado, Eletrificado ou Queimando/);
  });

  it('a batalha sabe quando a habilidade pronta está esperando a regra, sem mexer na luta', () => {
    const b = createBattle(['majinbuu', 'goku', 'naruto'], ['masterchief', 'vegeta', 'hulk'], 4);
    const boo = b.fighters.find((f) => f.characterId === 'majinbuu')!, regen = byId.majinbuu!.skills[2]!;
    for (const f of b.fighters) if (f.side === 'enemy') f.statuses = [];
    const antes = JSON.stringify(b);
    expect(condicaoAtendida(b, boo, regen)).toBe(false);
    expect(JSON.stringify(b)).toBe(antes);
    const chief = b.fighters.find((f) => f.characterId === 'masterchief')!;
    chief.statuses.push({ id: 'exposed', remaining: 5, intensity: 0.1, source: boo.uid });
    expect(condicaoAtendida(b, boo, regen)).toBe(true);
  });
});
