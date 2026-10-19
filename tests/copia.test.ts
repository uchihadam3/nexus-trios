import { describe, expect, it } from 'vitest';
import { createBattle, stepBattle } from '../src/engine/battle';
import { byId } from '../src/data/characters';
import { copiaNaTela } from '../src/presentation/copia';
import { profileFor } from '../src/presentation/vfxProfiles';

/* A Cópia perfeita do Kakashi: copia na mesma ação, e a tela mostra a habilidade copiada com o efeito e o som de quem ela é. */
describe('Copiar habilidade', () => {
  it('o aviso diz qual habilidade foi copiada e a tela usa o efeito dela em quem a cópia acertou', () => {
    let vistas = 0;
    for (let seed = 1; seed <= 40 && vistas < 5; seed++) {
      const b = createBattle(['kakashi', 'naruto', 'sakura'], ['sasuke', 'itachi', 'gaara'], seed);
      for (let t = 0; t < 9000 && !b.finished && vistas < 5; t++) {
        const antes = b.nextEvent;
        stepBattle(b);
        const passo = b.events.filter((e) => e.id >= antes);
        for (const copia of passo.filter((e) => e.kind === 'copy')) {
          const dono = b.fighters.find((f) => f.uid === copia.target)!, k = copia.copiada!;
          expect(copia.label).toBe(`Copiou ${byId[dono.characterId]!.skills[k]!.name}`);
          const tela = copiaNaTela({ events: passo, after: b }, copia)!;
          expect(tela.familia).toBe(profileFor(dono.characterId, k)!.family);
          expect(tela.alvos.length).toBeGreaterThan(0);
          vistas++;
        }
      }
    }
    expect(vistas).toBeGreaterThan(0);
  }, 60000);
});
