import { describe, expect, it } from 'vitest';
import { characters } from '../src/data/characters';
import { UNICAS } from '../src/engine/unicas';

/*
 * Pedido do jogador: "cada personagem tem que ser único, tem que jogar
 * realmente bem diferente um do outro". Compara o jeito de jogar (o que cada
 * habilidade faz e em quem, quando dispara, o Preparo, de onde vem a Carga, o
 * traço, o ataque básico e a Mecânica única), sem olhar os números: dois
 * kits iguais com números diferentes contam como iguais.
 */
type E = { kind: string; status?: string; target?: string };
const preparo = (p: number) => (p <= 0 ? 'p0' : p < 2.5 ? 'p1' : 'p2');
function jeitoDeJogar(c: (typeof characters)[number]): Map<string, number> {
  const t: string[] = [];
  for (const s of c.skills) {
    for (const x of new Set((s.effects as E[]).map((e) => `${e.kind}${e.status ? ':' + e.status : ''}@${e.target ?? s.target}`))) t.push('S:' + x);
    t.push('Sc:' + (s.condition ?? '-'), 'Sp:' + preparo(s.preparation));
    for (const ch of s.charge) t.push('Sch:' + ch.on);
  }
  for (const e of c.trait.effects as E[]) t.push(`T:${c.trait.on}:${e.kind}${e.status ? ':' + e.status : ''}@${e.target ?? c.trait.target}`);
  for (const e of c.basic.effects as E[]) t.push(`B:${e.kind}${e.status ? ':' + e.status : ''}`);
  t.push('J:' + (c.basic.jeito?.tipo ?? '-'));
  // a Mecânica única é só dele: pesa como uma habilidade inteira
  if (UNICAS[c.id]) for (let k = 0; k < 5; k++) t.push(`U:${c.id}${k}`);
  const m = new Map<string, number>();
  for (const x of t) m.set(x, (m.get(x) ?? 0) + 1);
  return m;
}
const semelhanca = (a: Map<string, number>, b: Map<string, number>) => {
  let i = 0, uniao = 0;
  for (const k of new Set([...a.keys(), ...b.keys()])) { const x = a.get(k) ?? 0, y = b.get(k) ?? 0; i += Math.min(x, y); uniao += Math.max(x, y); }
  return i / uniao;
};

describe('Personagens únicos', () => {
  it('nenhuma dupla de personagens joga quase igual (semelhança abaixo de 70%)', () => {
    const jeitos = characters.map(jeitoDeJogar);
    const parecidos: string[] = [];
    for (let i = 0; i < jeitos.length; i++) for (let j = i + 1; j < jeitos.length; j++) {
      const s = semelhanca(jeitos[i]!, jeitos[j]!);
      if (s >= 0.7) parecidos.push(`${characters[i]!.id} × ${characters[j]!.id}: ${Math.round(s * 100)}%`);
    }
    expect(parecidos).toEqual([]);
  });
});
