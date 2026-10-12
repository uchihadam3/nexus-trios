import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { unicaDe } from '../src/engine/unicas';

/*
 * Pedido do jogador: "o Wolverine, a mecânica única dele e o traço têm
 * exatamente o mesmo nome". Eram 165 nomes repetidos no elenco: mecânica
 * única com o nome do traço ou de uma habilidade, traço com o nome de uma
 * habilidade. Na ficha, duas coisas diferentes com o mesmo nome parecem a
 * mesma coisa.
 */
const norm = (s: string) => s.toLocaleLowerCase('pt-BR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]/g, '').trim();

describe('nomes do kit', () => {
  it('mecânica única, traço, ataque básico e habilidades têm nomes diferentes', () => {
    const repetidos: string[] = [];
    for (const c of characters) {
      const u = unicaDe(c.id);
      const nomes = [...(u ? [u.nome] : []), c.trait.name, c.basic.name, ...c.skills.map((s) => s.name)];
      const vistos = new Set<string>();
      for (const n of nomes) { if (vistos.has(norm(n))) repetidos.push(`${c.name}: ${n}`); vistos.add(norm(n)); }
    }
    expect(repetidos).toEqual([]);
  });

  it('cada traço e cada mecânica única tem nome próprio no elenco', () => {
    const tracos = characters.map((c) => norm(c.trait.name));
    const unicas = characters.map((c) => unicaDe(c.id)?.nome).filter((x): x is string => !!x).map(norm);
    expect(tracos.filter((t, i) => tracos.indexOf(t) !== i)).toEqual([]);
    expect(unicas.filter((t, i) => unicas.indexOf(t) !== i)).toEqual([]);
  });

  it('os nomes começam com maiúscula e não têm espaço sobrando (o Eren tinha " endurecer")', () => {
    const tortos: string[] = [];
    for (const c of characters) {
      const u = unicaDe(c.id);
      for (const n of [...(u ? [u.nome] : []), c.trait.name, c.basic.name, ...c.skills.map((s) => s.name)])
        if (n !== n.trim() || /\s{2}/.test(n) || /^[a-zà-ú]/.test(n)) tortos.push(`${c.name}: "${n}"`);
    }
    expect(tortos).toEqual([]);
  });
});
