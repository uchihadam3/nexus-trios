import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { createBattle, ESPERA_PELO_MOMENTO, stepBattle } from '../src/engine/battle';
import { presentSkill } from '../src/engine/skill-descriptions';

/*
 * Pedido do jogador: o Majin Boo ficou com a Regeneração total pronta a luta
 * inteira (ela espera um rival vulnerável, e quem abria o rival já tinha
 * caído). Golpe pronto não espera o momento ideal para sempre.
 */
describe('golpe pronto não espera para sempre', () => {
  it('a Regeneração total sai mesmo sem rival vulnerável, depois da espera', () => {
    const b = createBattle(['majinbuu', 'goku', 'naruto'], ['masterchief', 'vegeta', 'hulk'], 4);
    const boo = b.fighters.find((f) => f.characterId === 'majinbuu')!;
    // só sobram o Boo e o Master Chief, ninguém com Status
    for (const f of b.fighters) if (!['majinbuu', 'masterchief'].includes(f.characterId)) { f.hp = 0; f.statuses = []; }
    const chief = b.fighters.find((f) => f.characterId === 'masterchief')!;
    chief.statuses = []; chief.hp = chief.maxHp * 5; chief.maxHp *= 5;
    boo.skills.forEach((s, i) => { s.charge = i === 2 ? 100 : 0; });
    const usou = () => b.events.some((e) => e.source === boo.uid && (e.kind === 'skill' || e.kind === 'cast') && e.skill === 2);
    for (let t = 0; t < (ESPERA_PELO_MOMENTO + 6) * 10 && !usou(); t++) {
      // ninguém deixa o Master Chief vulnerável
      chief.statuses = chief.statuses.filter((s) => !['exposed', 'marked', 'paralyzed', 'electric', 'burning'].includes(s.id));
      stepBattle(b);
    }
    expect(usou()).toBe(true);
  });

  it('a ficha avisa', () => {
    expect(presentSkill(byId.majinbuu!.skills[2]!).useWhen).toMatch(/sai depois de 6 s pronta/);
  });
});
