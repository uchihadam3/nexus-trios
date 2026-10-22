/*
 * O jogo em inglês (src/i18n): com ?idioma=en, as fichas de todos os personagens têm que sair inteiras em inglês.
 *
 * O idioma é lido uma vez, quando o módulo carrega; por isso o teste monta um "navegador" pedindo inglês e importa
 * tudo de novo depois disso.
 */
import { beforeAll, describe, expect, it, vi } from 'vitest';

type Idioma = typeof import('../src/i18n/idioma');
let i: Idioma;
let fichas: typeof import('../src/engine/skill-descriptions');
let elenco: typeof import('../src/data/characters');
let unicas: typeof import('../src/engine/unicas');

beforeAll(async () => {
  vi.resetModules();
  const g = globalThis as Record<string, unknown>;
  g.window = g;
  g.location = { search: '?idioma=en' };
  const mem: Record<string, string> = {};
  g.localStorage = { getItem: (k: string) => mem[k] ?? null, setItem: (k: string, v: string) => { mem[k] = v; }, removeItem: (k: string) => { delete mem[k]; } };
  i = await import('../src/i18n/idioma');
  await i.carregarIdioma();
  fichas = await import('../src/engine/skill-descriptions');
  elenco = await import('../src/data/characters');
  unicas = await import('../src/engine/unicas');
  delete g.window; delete g.location; delete g.localStorage;
});

/* Palavras que só existem em português: se aparecem num texto em inglês, ficou um pedaço sem tradução. */
const PORTUGUES = /[ãõçáíóúâêôà]|\b(de dano|Aplica|Vida|rival mais|aliado|Carga|Preparo|Resfriamento|segundos?|quando|enquanto|golpe|habilidade|todos os|todo o trio|próprio|ferido|Escudo de|mais lento|mais rápido)\b/i;

describe('o jogo em inglês', () => {
  it('troca os textos, os números e as posições', () => {
    expect(i.IDIOMA).toBe('en');
    expect(i.t('Fechar')).toBe('Close');
    expect(i.t('{n} de 3 estrelas', { n: 2 })).toBe('2 of 3 stars');
    expect(i.numero(1234.5)).toBe('1,234.5');
    expect(i.ordinal(1)).toBe('1st');
    expect(i.ordinal(12)).toBe('12th');
    expect(i.ordinal(23)).toBe('23rd');
    expect(i.nomeDe({ id: 'spiderman', name: 'Homem-Aranha' })).toBe('Spider-Man');
  });

  it('traduz os avisos da luta montados com número', () => {
    expect(i.t('Joia 3/6')).toBe('Stone 3/6');
    expect(i.t('Nível 4')).toBe('Level 4');
    expect(i.t('Copiou: Vingança')).toBe('Copied: Vengeance');
  });

  it('as fichas de todos os personagens saem sem nenhum pedaço em português', () => {
    const sobras: string[] = [];
    const confere = (quem: string, onde: string, texto: string) => { if (PORTUGUES.test(texto)) sobras.push(`${quem} · ${onde}: ${texto}`); };
    for (const c of elenco.characters) {
      const nome = i.nomeDe(c);
      confere(nome, 'ideia', i.t(c.idea));
      const traco = fichas.presentTrait(c.trait), ativa = fichas.ativaQuando(c.trait, nome);
      confere(nome, 'traço', [i.t(c.trait.name), ...traco.effects, ativa.rotulo, ativa.resto].join(' · '));
      confere(nome, 'básico', [i.t(c.basic.name), c.basic.jeito ? fichas.textoDoJeito(c.basic.jeito) : ''].join(' · '));
      for (const s of c.skills) {
        const p = fichas.presentSkill(s);
        confere(nome, i.t(s.name), [i.t(s.name), ...p.grupos.flatMap((g) => [g.titulo, ...g.linhas.map((l) => l.texto)]), ...p.charge, p.preparation, p.requisito ?? ''].join(' · '));
      }
      const u = unicas.unicaDe(c.id);
      if (u) confere(nome, 'única', `${i.t(u.nome)} · ${i.t(u.texto)}`);
    }
    expect(sobras.slice(0, 20)).toEqual([]);
  });
});
