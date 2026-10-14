import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { byId } from '../src/data/characters';
import { formaDe, naFormaDeAgora } from '../src/presentation/formas';

/*
 * Gandalf, o Branco (pedido do jogador: "quando ele morrer e voltar… ele muda a imagem dele"): o retrato só troca
 * depois que ele cai e volta pela mecânica, e não troca antes nem enquanto está caído.
 */
describe('Gandalf, o Branco', () => {
  it('troca o retrato só quando volta', () => {
    let voltou = 0;
    for (let semente = 1; semente <= 40 && voltou < 3; semente++) {
      const b = createBattle(['gandalf', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const g = b.fighters.find((f) => f.characterId === 'gandalf')!;
      let viu = false;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        if (!g.voltou) expect(formaDe(g)).toBeNull();
        else if (g.hp > 0 && !viu) {
          viu = true; voltou++;
          const c = naFormaDeAgora(byId.gandalf, g);
          expect(c.portrait).toBe('/assets/portraits/formas/gandalf-branco.webp');
          expect(c.name).toBe('Gandalf, o Branco');
        }
      }
    }
    expect(voltou).toBeGreaterThan(0);
    expect(naFormaDeAgora(byId.gandalf, { characterId: 'gandalf' } as never).portrait).toBe(byId.gandalf.portrait);
  });
});

/*
 * Ben 10 (pedido do jogador: "quando ele usar o Omnitrix… coloca certinho cada um deles… se falhar continua com o
 * Ben 10"): cada alien sorteado troca o retrato pelo dele; o Omnitrix falhando deixa o retrato do Ben.
 */
describe('Ben 10 e o Omnitrix', () => {
  it('troca o retrato pelo alien sorteado e mantém o Ben quando falha', () => {
    const vistos = new Set<string>();
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['ben10', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const ben = b.fighters.find((f) => f.characterId === 'ben10')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const alien = ben.u?.alien, c = naFormaDeAgora(byId.ben10, ben);
        if (alien === undefined || alien === 4) expect(c.portrait).toBe(byId.ben10.portrait);
        else { expect(c.name).toBe(['Quatro Braços', 'Chama', 'XLR8', 'Diamante'][alien]); vistos.add(c.portrait); }
      }
    }
    expect([...vistos].sort()).toEqual(['chama', 'diamante', 'quatro-bracos', 'xlr8'].map((n) => `/assets/portraits/formas/ben10-${n}.webp`));
  });
});
