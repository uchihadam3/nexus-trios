import { describe, it, expect } from 'vitest';
import { characters, byId } from '../src/data/characters';
import { universoDe, grupoDoUniverso } from '../src/data/equipes';

describe('Universos da ficha', () => {
  it('os parecidos dividem o mesmo universo, e cada universo tem 5 personagens ou mais', () => {
    expect(new Set(['jason', 'freddy', 'michaelmyers', 'pinhead', 'ghostface'].map((id) => universoDe(byId[id]!))).size).toBe(1);
    expect(universoDe(byId.wolverine!)).toBe('X-Men');
    expect(universoDe(byId.batman!)).toBe('Gotham');
    expect(universoDe(byId.naruto!)).toBe('Naruto');
    const conta = new Map<string, number>();
    for (const c of characters) conta.set(universoDe(c), (conta.get(universoDe(c)) ?? 0) + 1);
    for (const [u, n] of conta) expect(n, u).toBeGreaterThanOrEqual(5);
  });
  it('os combos de universo continuam olhando a série de cada um (a força não muda)', () => {
    expect(grupoDoUniverso(byId.jason!)).toBe(byId.jason!.universe);
    expect(grupoDoUniverso(byId.wolverine!)).toBe('X-Men');
  });
});
