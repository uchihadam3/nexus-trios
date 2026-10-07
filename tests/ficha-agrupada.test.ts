/*
 * A ficha agrupada por alvo, conferida nos 250 personagens.
 *
 * Medido antes da mudança: 220 linhas repetiam um alvo que a própria ficha já
 * tinha dito. Agrupar resolve isso só enquanto ninguém quebrar o agrupamento —
 * e as formas de quebrar são justamente as que não aparecem olhando três
 * personagens: perder um efeito no caminho, deixar a linha "Alvo" ecoar o
 * cabeçalho, pôr um efeito sob o alvo errado.
 */
import { describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { agruparEfeitos, presentSkill } from '../src/engine/skill-descriptions';
import type { Effect } from '../src/engine/types';

const todas = characters.flatMap((c) => c.skills.map((s) => ({ c, s, p: presentSkill(s) })));

describe('ficha agrupada por alvo', () => {
  it('cobre as 750 habilidades', () => {
    expect(todas).toHaveLength(750);
  });

  it('nenhum efeito some e nenhum aparece duas vezes', () => {
    for (const { c, s, p } of todas) {
      const linhas = p.grupos.reduce((n, g) => n + g.linhas.length, 0);
      expect(linhas, `${c.name} · ${s.name}`).toBe(s.effects.length);
    }
  });

  it('cada alvo aparece uma vez só por habilidade', () => {
    for (const { c, s, p } of todas) {
      const titulos = p.grupos.map((g) => g.titulo).filter(Boolean);
      expect(new Set(titulos).size, `${c.name} · ${s.name}`).toBe(titulos.length);
    }
  });

  it('nenhuma linha agrupada repete o alvo do cabeçalho', () => {
    for (const { c, s, p } of todas) for (const g of p.grupos) for (const l of g.linhas) {
      expect(l.texto, `${c.name} · ${s.name}`).not.toMatch(/^Aplica /);
      expect(l.texto, `${c.name} · ${s.name}`).not.toContain(' → ');
    }
  });

  /*
   * A linha "Alvo" no rodapé só pode aparecer quando nenhum cabeçalho disse o
   * alvo. Com cabeçalho na tela, ela é o eco que motivou tudo isto.
   */
  it('a linha "Alvo" nunca ecoa um cabeçalho', () => {
    for (const { c, s, p } of todas) {
      if (p.grupos.some((g) => g.titulo !== '')) expect(p.mostrarAlvo, `${c.name} · ${s.name}`).toBe(false);
    }
  });

  it('as peças e o texto contam a mesma história', () => {
    for (const { p } of todas) for (const g of p.grupos) for (const l of g.linhas) {
      expect(l.partes.join(' · ')).toBe(l.texto);
      expect(l.partes.every((x) => x.trim().length > 0)).toBe(true);
    }
  });

  /*
   * Guardar energia herdaria o alvo da habilidade. Sob "No inimigo mais
   * ferido", "Guarda 40 de energia" diria uma mentira — quem guarda é o
   * próprio personagem.
   */
  it('efeitos que se explicam sozinhos ficam fora de qualquer cabeçalho', () => {
    const efeitos: Effect[] = [
      { kind: 'damage', value: 100 },
      { kind: 'store', value: 40, cap: 200 },
      { kind: 'release', multiplier: 1.2, target: 'allEnemies' },
    ];
    const grupos = agruparEfeitos(efeitos, 'enemyWeak');
    expect(grupos[0]).toMatchObject({ titulo: 'No inimigo mais ferido' });
    expect(grupos[0].linhas).toHaveLength(1);
    const semCabecalho = grupos.find((g) => g.titulo === '');
    expect(semCabecalho?.linhas.map((l) => l.texto)).toEqual([
      expect.stringContaining('Guarda'), expect.stringContaining('Libera'),
    ]);
  });

  it('a ordem dos grupos segue a ordem em que os efeitos acontecem', () => {
    const grupos = agruparEfeitos([
      { kind: 'damage', value: 100 },
      { kind: 'heal', value: 50, target: 'allAllies' },
      { kind: 'status', status: 'exposed', value: 0.12, duration: 5 },
    ], 'enemyWeak');
    expect(grupos.map((g) => g.titulo)).toEqual(['No inimigo mais ferido', 'Em todo o trio']);
    expect(grupos[0].linhas).toHaveLength(2);
  });

  /*
   * A pergunta que o jogador fez: "o Exposto é fixo, ou cada habilidade faz
   * uma coisa diferente?". Cada uma aplica a sua dose — e a ficha tem que
   * deixar o número colado no nome do Status, não perdido no fim da frase.
   */
  it('o valor do Status vem logo depois do nome dele', () => {
    const [g] = agruparEfeitos([{ kind: 'status', status: 'exposed', value: 0.12, duration: 5 }], 'enemyWeak');
    const [nome, oQueFaz] = g.linhas[0].partes;
    expect(nome).toBe('Exposto');
    expect(oQueFaz).toContain('12%');
  });
});
