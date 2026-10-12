import { describe, expect, it } from 'vitest';
import { createBattle } from '../src/engine/battle';
import { PRESENTATION as P } from '../src/presentation/config';
import { advanceDirection, createDirection, VOLTA_DO_GOLPE, type Beat } from '../src/presentation/director';

/*
 * Pedido do jogador: o personagem sai para atacar, bate e volta; o efeito que ajuda o próprio trio (o
 * Acelerado do Flecha e do Flash, a cura do soco da Sakura, o Escudo da pedra da Toph) só aparece quando ele
 * já voltou para o lugar — antes, saía com ele ainda no caminho de volta.
 */
const CONTABIL = new Set(['charge', 'synergy', 'ready', 'discovery', 'basic', 'skill', 'cast', 'turn']);

function golpesQueAjudamOTrio(a: string[], b: string[], seed: number) {
  const d = createDirection(createBattle(a, b, seed));
  const vistos = new Set<number>();
  const achados: { em: number; volta: number; quem: string }[] = [];
  for (let k = 0; k < 3000 && !d.complete; k++) {
    advanceDirection(d, 0.05);
    const beat = d.active as Beat | null;
    if (!beat || vistos.has(beat.event.id)) continue;
    vistos.add(beat.event.id);
    if (!['basic', 'skill'].includes(beat.event.kind) || !beat.passos) continue;
    const ator = beat.event.source;
    const ladoDe = (u?: string) => beat.after.fighters.find((f) => f.uid === u)?.side;
    const lado = ladoDe(ator);
    if (!beat.events.some((e) => e.kind === 'damage' && e.source === ator && ladoDe(e.target) !== lado)) continue;
    const volta = (VOLTA_DO_GOLPE - P.impactAt) * (beat.base ?? 0);
    beat.passos.forEach((x, i) => {
      const noTrio = x.eventos.some((id) => {
        const e = beat.events.find((y) => y.id === id);
        return !!e && ladoDe(x.quem) === lado && ladoDe(e.target ?? e.source) === lado && !CONTABIL.has(e.kind) && !['damage', 'block', 'interrupt', 'ko'].includes(e.kind);
      });
      if (noTrio) achados.push({ em: i === 0 ? -1 : x.em, volta, quem: beat.after.fighters.find((f) => f.uid === ator)!.characterId });
    });
  }
  return achados;
}

describe('o efeito no próprio trio espera quem bateu voltar', () => {
  it('Flecha, Flash, Sakura e Toph: o Acelerado, a cura e o Escudo saem com eles já no lugar', () => {
    const achados = [...golpesQueAjudamOTrio(['dash', 'flash', 'sakura'], ['goku', 'vegeta', 'hulk'], 3), ...golpesQueAjudamOTrio(['toph', 'dash', 'flash'], ['naruto', 'sasuke', 'luffy'], 5)];
    expect(achados.length).toBeGreaterThan(5);
    for (const a of achados) expect(a.em, `${a.quem}: o efeito saiu ${a.em.toFixed(2)} s depois do golpe, antes da volta (${a.volta.toFixed(2)} s)`).toBeGreaterThanOrEqual(a.volta - 1e-6);
  });
});
