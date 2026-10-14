import { existsSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { ENTREGA_DA_UNICA, VOO_DA_UNICA, entregaDaUnica } from '../src/presentation/unicas-efeitos';

describe('Mecânica única chega no alvo como uma habilidade', () => {
  it('todo desenho que voa, estica ou prepara existe', () => {
    const faltam = Object.entries(ENTREGA_DA_UNICA).flatMap(([id, e]) => [e.viagem, e.faixa, e.preparo].filter((n): n is string => !!n && !existsSync(`public/assets/vfx/familias/${n}.webp`)).map((n) => `${id}: ${n}`));
    expect(faltam).toEqual([]);
  });

  it('só personagens que existem', () => {
    const ids = new Set(characters.map((c) => c.id));
    expect(Object.keys(ENTREGA_DA_UNICA).filter((id) => !ids.has(id))).toEqual([]);
  });

  it('a Genki Dama voa até o rival e a viagem tem tempo', () => {
    const e = entregaDaUnica('goku', 'rival');
    expect(e.modo).toBe('voa');
    expect(e.viagem).toBe('genki_dama_voo');
    expect(VOO_DA_UNICA[e.modo]).toBeGreaterThan(0);
  });

  it('sem nada definido: no rival voa, no aliado viaja até ele, sem alvo fica em si', () => {
    expect(entregaDaUnica('personagem-sem-entrega', 'rival').modo).toBe('voa');
    expect(entregaDaUnica('personagem-sem-entrega', 'aliado').modo).toBe('aliado');
    expect(entregaDaUnica('personagem-sem-entrega', 'si').modo).toBe('si');
  });
});

describe('fases da ativação da Mecânica única', () => {
  it('concentra, mostra o nome, carrega e solta, nessa ordem; o reflexo é instantâneo', async () => {
    const { fasesDaUnica, preparoProprio } = await import('../src/presentation/ativacao-da-unica');
    const genki = fasesDaUnica('goku', 0.55);
    expect(preparoProprio('goku')).toBe(1.1);
    expect(genki.nomeEm).toBeGreaterThan(0);
    expect(genki.soltaEm).toBeGreaterThan(genki.nomeEm);
    expect(genki.impactoEm).toBeCloseTo(genki.vooEm + 0.55);
    const valak = fasesDaUnica('valak', 0);
    expect(valak.nomeEm).toBe(0);
    expect(valak.soltaEm).toBe(0);
    expect(fasesDaUnica('seiya', 0).soltaEm).toBeLessThan(genki.soltaEm);
  });
});
