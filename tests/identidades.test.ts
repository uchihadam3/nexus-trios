/*
 * FASE F · o contrato das identidades públicas.
 *
 * O documento da direção pede três coisas, e as três são verificáveis:
 * "2–4 por personagem", "sem tags incidentais enganosas", "distribuição
 * saudável". A FASE E tinha medido o que acontece quando ninguém verifica:
 * "Dano" em 250 de 250, 16 combinações para 250 lutadores, e o corte em três
 * silenciando identidade em 114 deles.
 *
 * Então os números viram teste. Se a derivação regredir, ou se alguém editar
 * src/data/identidades.ts à mão, isto cai.
 */
import { describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { identidadesPorPersonagem } from '../src/data/identidades';
import type { Identidade } from '../src/presentation/identities';
import {
  explicacaoDaIdentidade, familiaDaIdentidade, identidadesDe, identidadesDoTrio,
  lacunasDoTrio, oQueAdiciona, ordemDasIdentidades,
} from '../src/presentation/identities';

const todas = characters.map((c) => ({ c, ids: identidadesDe(c) }));

describe('identidades públicas', () => {
  /*
   * Poucas e de verdade: de 1 a 3 etiquetas, e 4 só para a exceção. Com quatro
   * em quase todo mundo a carta dizia "faz de tudo".
   */
  it('cobre os 250, com 1 a 3 cada (4 só como exceção)', () => {
    expect(Object.keys(identidadesPorPersonagem)).toHaveLength(250);
    for (const { c, ids } of todas) {
      expect(ids.length, `${c.name}: ${ids.join(', ')}`).toBeGreaterThanOrEqual(1);
      expect(ids.length, `${c.name}: ${ids.join(', ')}`).toBeLessThanOrEqual(4);
      expect(new Set(ids).size, `${c.name} repete identidade`).toBe(ids.length);
    }
    const quatro = todas.filter(({ ids }) => ids.length === 4).length;
    expect(quatro / todas.length, `${String(quatro)} personagens com 4 etiquetas`).toBeLessThanOrEqual(0.08);
    const media = todas.reduce((n, { ids }) => n + ids.length, 0) / todas.length;
    expect(media).toBeLessThanOrEqual(3);
  });

  it('só usa termos da taxonomia, e cada um tem explicação', () => {
    for (const { c, ids } of todas) {
      for (const x of ids) {
        expect(ordemDasIdentidades, `${c.name}: "${x}"`).toContain(x);
        expect(explicacaoDaIdentidade[x], `${x} sem explicação`).toBeTruthy();
        expect(familiaDaIdentidade[x], `${x} sem família`).toBeTruthy();
      }
    }
    for (const x of ordemDasIdentidades) {
      expect(explicacaoDaIdentidade[x].length).toBeGreaterThan(20);
    }
  });

  /*
   * O defeito que derrubou o sistema antigo.
   *
   * "Dano" valia para 250 de 250 porque todo mundo tem ataque básico. Uma
   * etiqueta que não separa ninguém de ninguém não informa — só ocupa uma das
   * poucas vagas da carta.
   */
  it('nenhuma identidade domina o elenco', () => {
    const contagem = new Map<Identidade, number>();
    for (const { ids } of todas) for (const x of ids) contagem.set(x, (contagem.get(x) ?? 0) + 1);
    for (const [x, n] of contagem) {
      expect(n / characters.length, `${x} aparece em ${String(n)} de 250`).toBeLessThanOrEqual(0.35);
    }
    /* E nenhuma fica tão rara que vire decoração: ou tem donos, ou não existe. */
    for (const x of ordemDasIdentidades) {
      expect(contagem.get(x) ?? 0, `${x} não tem nenhum dono`).toBeGreaterThan(0);
    }
  });

  /*
   * O outro defeito: 16 combinações para 250 personagens, de modo que duas das
   * três cartas do Draft frequentemente liam igual.
   */
  it('as combinações distinguem os personagens entre si', () => {
    const combinacoes = new Map<string, string[]>();
    for (const { c, ids } of todas) {
      const chave = [...ids].sort().join(' · ');
      combinacoes.set(chave, [...(combinacoes.get(chave) ?? []), c.name]);
    }
    expect(combinacoes.size).toBeGreaterThan(140);
    /* Com etiqueta única para quem é bom numa coisa só, a mesma etiqueta solitária se repete mais — até 12. */
    const maior = [...combinacoes.values()].sort((a, b) => b.length - a.length)[0]!;
    expect(maior.length, `combinação repetida demais: ${maior.join(', ')}`).toBeLessThanOrEqual(12);
  });

  /*
   * "Não dar Cura por cura incidental." Quem tem a etiqueta precisa ter a
   * mecânica; o inverso não vale, porque ter a mecânica não basta para ganhar
   * a etiqueta — é preciso se destacar nela.
   */
  it('quem recebe Cura cura aliado de verdade', () => {
    const curaAliado = (id: string) => {
      const c = characters.find((x) => x.id === id)!;
      const partes = [...c.skills.map((s) => ({ e: s.effects, alvo: s.target })),
        { e: c.trait.effects, alvo: c.trait.target }];
      return partes.some(({ e, alvo }) => e.some((x) =>
        (x.kind === 'heal' || (x.kind === 'status' && x.status === 'regen'))
        && ['allAllies', 'allyWeak'].includes(x.target ?? alvo)));
    };
    const mentirosos = todas.filter(({ c, ids }) => ids.includes('Cura') && !curaAliado(c.id));
    expect(mentirosos.map((x) => x.c.name)).toEqual([]);
  });

  it('quem recebe Interrupção tem como interromper', () => {
    const mentirosos = todas.filter(({ c, ids }) => ids.includes('Interrupção')
      && ![...c.skills.flatMap((s) => s.effects), ...c.trait.effects].some((e) => e.kind === 'interrupt'));
    expect(mentirosos.map((x) => x.c.name)).toEqual([]);
  });

  it('quem recebe Carga enche a Carga do trio', () => {
    const mentirosos = todas.filter(({ c, ids }) => ids.includes('Carga')
      && ![...c.skills.flatMap((s) => s.effects.map((e) => ({ e, alvo: e.target ?? s.target }))),
        ...c.trait.effects.map((e) => ({ e, alvo: e.target ?? c.trait.target }))]
        .some(({ e, alvo }) => e.kind === 'charge' && ['self', 'allAllies', 'allyWeak'].includes(alvo)));
    expect(mentirosos.map((x) => x.c.name)).toEqual([]);
  });

  /* As quatro âncoras escritas no documento da direção. */
  it.each([
    ['saitama', ['Explosão', 'Finalização', 'Sobrevivência']],
    ['storm', ['Área', 'Controle', 'Ritmo']],
    ['wolverine', ['Pressão', 'Regeneração', 'Sobrevivência']],
    ['professorx', ['Suporte', 'Controle', 'Ritmo']],
  ])('%s tem as identidades que a direção nomeou', (id, esperadas) => {
    expect([...identidadesDe(id)].sort()).toEqual([...esperadas].sort());
  });
});

describe('o que o Draft diz sobre o trio', () => {
  const trio = ['sakura', 'goku', 'pikachu'];

  it('reúne as identidades do trio sem repetir', () => {
    const juntas = identidadesDoTrio(trio);
    expect(new Set(juntas).size).toBe(juntas.length);
    for (const id of trio) for (const x of identidadesDe(id)) expect(juntas).toContain(x);
  });

  it('o que o candidato adiciona é só o que o trio não tinha', () => {
    const novas = oQueAdiciona('thanos', trio);
    const jaTinha = new Set(identidadesDoTrio(trio));
    for (const x of novas) expect(jaTinha.has(x)).toBe(false);
    for (const x of novas) expect(identidadesDe('thanos')).toContain(x);
  });

  /*
   * "Somente se calculado honestamente." Um trio com curandeiro não pode ouvir
   * que lhe falta recuperação.
   */
  it('não acusa lacuna que o trio não tem', () => {
    const comCurandeiro = lacunasDoTrio(['sakura', 'goku', 'pikachu']);
    expect(identidadesDe('sakura')).toContain('Cura');
    expect(comCurandeiro).not.toContain('Pouca recuperação');
    /* E um trio vazio não recebe diagnóstico nenhum. */
    expect(lacunasDoTrio([])).toEqual([]);
  });

  it('acusa a lacuna quando ela existe de verdade', () => {
    const semCura = characters.filter((c) => !identidadesDe(c).includes('Cura')
      && !identidadesDe(c).includes('Regeneração')).slice(0, 3).map((c) => c.id);
    expect(lacunasDoTrio(semCura)).toContain('Pouca recuperação');
  });
});
