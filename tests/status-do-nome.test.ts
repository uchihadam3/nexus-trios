import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { termoPorId } from '../src/presentation/glossario';
import { presentSkill, textoDaResistencia } from '../src/engine/skill-descriptions';

const byId = Object.fromEntries(characters.map((c) => [c.id, c]));
const status = (id: string, i: number) => byId[id]!.skills[i]!.effects.flatMap((e) => (e.kind === 'status' ? [e.status] : []));

describe('o Status combina com o nome do golpe', () => {
  it('a Dobra de fogo queima; o Canhão incinerador também', () => {
    expect(status('korra', 0)).toContain('burning');
    expect(status('korra', 0)).not.toContain('electric');
    expect(status('genos', 0)).toContain('burning');
  });
  it('nenhum golpe com nome de fogo dá choque, e nenhum de gelo queima', () => {
    for (const c of characters) for (const s of [...c.skills, c.basic, c.trait]) {
      const st = s.effects.flatMap((e) => (e.kind === 'status' ? [e.status] : []));
      if (/fogo|chama|incinera|flamejante/i.test(s.name)) expect(st, `${c.id} ${s.name}`).not.toContain('electric');
      if (/gelo|frost|congel|neve/i.test(s.name)) expect(st, `${c.id} ${s.name}`).not.toContain('burning');
    }
  });
});

describe('a ficha não repete o que o termo clicável já explica', () => {
  it('Última resistência mostra só o que muda de um personagem para outro', () => {
    expect(textoDaResistencia({ protegido: 0.5, duracao: 2.5 })).toBe('Última resistência · Protegido 50% por 2,5 s');
  });
  it('"vulnerável" é um termo, e a regra de uso não lista os Status', () => {
    expect(termoPorId.vulneravel?.texto).toMatch(/Exposto/);
    const regras = characters.flatMap((c) => c.skills.map((s) => presentSkill(s).requisito ?? ''));
    for (const r of regras) expect(r).not.toMatch(/Exposto, Marcado/);
  });
});

describe('os números que o jogador pediu', () => {
  it('Discurso interminável do Macaco Louco: 450 de dano e Preparo de 4 s', () => {
    const s = byId.mojojojo!.skills[2]!;
    expect(s.name).toBe('Discurso interminável');
    expect(s.preparation).toBe(4);
    expect(byId.mojojojo!.name).toBe('Macaco Louco');
    expect(s.effects.flatMap((e) => (e.kind === 'damage' ? [e.value] : []))).toEqual([450]);
  });
});
