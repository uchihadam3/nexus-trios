import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

// todo movimento de quem age tem a folha do brilho dele: sem ela, o brilho mascarado vira um retângulo colorido
describe('atuação', () => {
  it('cada estilo de quem age tem a folha do brilho', () => {
    const ts = readFileSync('src/presentation/acting.ts', 'utf8');
    const css = readFileSync('src/presentation/acting.css', 'utf8');
    const estilos = [...ts.match(/export type ActStyle = ([^;]+);/)![1]!.matchAll(/'([a-z]+)'/g)].map((m) => m[1]!);
    const sem = estilos.filter((s) => !new RegExp(`\\.act-${s}[^{}]*\\.unit-fx[^{}]*\\{[^}]*--fx-sheet`).test(css));
    expect(sem).toEqual([]);
  });
});
