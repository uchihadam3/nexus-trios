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

/*
 * Mario (pedido do jogador: "Mario pequeno… o Mario grande usa a que tem lá"): pequeno, o retrato é o do Mario
 * pequeno; depois do Super Cogumelo, volta o retrato de sempre (e encolhendo, o pequeno de novo).
 */
describe('Mario e o Super Cogumelo', () => {
  it('mostra o Mario pequeno até o cogumelo e o retrato de sempre quando cresce', () => {
    let cresceu = 0;
    for (let semente = 1; semente <= 20; semente++) {
      const b = createBattle(['mario', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const mario = b.fighters.find((f) => f.characterId === 'mario')!;
      expect(naFormaDeAgora(byId.mario, mario).portrait).toBe('/assets/portraits/formas/mario-pequeno.webp');
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const grande = !!mario.u?.grande;
        if (grande) cresceu++;
        expect(naFormaDeAgora(byId.mario, mario).portrait).toBe(grande ? byId.mario.portrait : '/assets/portraits/formas/mario-pequeno.webp');
      }
    }
    expect(cresceu).toBeGreaterThan(0);
  });
});

/* Korra (pedido do jogador: "Korra estado de avatar"): o retrato do Estado Avatar só nos 6 s em que ele dura. */
describe('Korra no Estado Avatar', () => {
  it('troca o retrato só enquanto o Estado Avatar dura', () => {
    let viu = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['korra', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const korra = b.fighters.find((f) => f.characterId === 'korra')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const ativo = (korra.u?.avatar ?? 0) > b.time;
        if (ativo) viu++;
        expect(naFormaDeAgora(byId.korra, korra, b).portrait).toBe(ativo ? '/assets/portraits/formas/korra-avatar.webp' : byId.korra.portrait);
      }
    }
    expect(viu).toBeGreaterThan(0);
  });
});

/* Hércules (pedido do jogador: "Hércules semideus"): com 12 Trabalhos vira Semideus e fica com o retrato novo. */
describe('Hércules Semideus', () => {
  it('troca o retrato quando vira Semideus e não volta mais', () => {
    let virou = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['hercules', 'hinata', 'naruto'], ['jerry', 'patolino', 'coragem'], semente);
      const h = b.fighters.find((f) => f.characterId === 'hercules')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const deus = !!h.u?.deus;
        if (deus) virou++;
        expect(naFormaDeAgora(byId.hercules, h, b).portrait).toBe(deus ? '/assets/portraits/formas/hercules-semideus.webp' : byId.hercules.portrait);
      }
    }
    expect(virou).toBeGreaterThan(0);
  });
});

/* Griffith (pedido do jogador: "Femto eclipse"): no Eclipse vira Femto e fica com o retrato novo até o fim. */
describe('Griffith vira Femto', () => {
  it('troca o retrato no Eclipse e não volta mais', () => {
    let virou = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['griffith', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const g = b.fighters.find((f) => f.characterId === 'griffith')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const femto = !!g.u?.femto;
        if (femto) virou++;
        expect(naFormaDeAgora(byId.griffith, g, b).portrait).toBe(femto ? '/assets/portraits/formas/griffith-femto.webp' : byId.griffith.portrait);
      }
    }
    expect(virou).toBeGreaterThan(0);
  });
});

/* Kenpachi (pedido do jogador: "Kenpachi sem o tapa-olho"): tirou o tapa-olho, troca o retrato até o fim da luta. */
describe('Kenpachi sem o tapa-olho', () => {
  it('troca o retrato quando tira o tapa-olho', () => {
    let tirou = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['kenpachi', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const k = b.fighters.find((f) => f.characterId === 'kenpachi')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const sem = !!k.u?.olho;
        if (sem) tirou++;
        expect(naFormaDeAgora(byId.kenpachi, k, b).portrait).toBe(sem ? '/assets/portraits/formas/kenpachi-sem-tapa-olho.webp' : byId.kenpachi.portrait);
      }
    }
    expect(tirou).toBeGreaterThan(0);
  });
});

/* Sephiroth (pedido do jogador: "Sephiroth com uma asa"): abriu a asa negra, troca o retrato até o fim da luta. */
describe('Sephiroth com uma asa', () => {
  it('troca o retrato quando abre a asa', () => {
    let abriu = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['sephiroth', 'hinata', 'naruto'], ['goku', 'vegeta', 'hulk'], semente);
      const s = b.fighters.find((f) => f.characterId === 'sephiroth')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const asa = !!s.u?.asa;
        if (asa) abriu++;
        expect(naFormaDeAgora(byId.sephiroth, s, b).portrait).toBe(asa ? '/assets/portraits/formas/sephiroth-uma-asa.webp' : byId.sephiroth.portrait);
      }
    }
    expect(abriu).toBeGreaterThan(0);
  });
});

/* Steve (pedido do jogador: "Steve armadura de diamante"): fabricou a armadura, troca o retrato até o fim da luta. */
describe('Steve de armadura de diamante', () => {
  it('troca o retrato quando fabrica a armadura', () => {
    let vestiu = 0;
    for (let semente = 1; semente <= 30; semente++) {
      const b = createBattle(['steve', 'hinata', 'naruto'], ['jerry', 'patolino', 'coragem'], semente);
      const s = b.fighters.find((f) => f.characterId === 'steve')!;
      for (let t = 0; t < 6000 && !b.finished; t++) {
        stepBattle(b);
        const armadura = (s.u?.pecas ?? 0) >= 1;
        if (armadura) vestiu++;
        expect(naFormaDeAgora(byId.steve, s, b).portrait).toBe(armadura ? '/assets/portraits/formas/steve-diamante.webp' : byId.steve.portrait);
      }
    }
    expect(vestiu).toBeGreaterThan(0);
  });
});
