import type { CSSProperties, ReactNode } from 'react';
import type { Battle } from '../engine/types';
import { PRESENTATION as P } from '../presentation/config';
import { duracaoBase, type Beat } from '../presentation/director';
import { entregasDeApoio, type TipoDeApoio } from '../presentation/entrega-de-apoio';
import { profileFor } from '../presentation/vfxProfiles';
import { fallbackPoint, type Anchors } from './BattleEffects';

/*
 * A entrega do apoio na tela (src/presentation/entrega-de-apoio.ts):
 *   1. a esfera se forma na frente de quem usou (um brilho que cresce);
 *   2. sai e voa em arco até o aliado, com rastro e faíscas, levando o símbolo do que entrega;
 *   3. estoura no aliado no instante em que o número e o efeito da habilidade aparecem nele.
 * Tudo é calculado a cada quadro a partir do tempo do beat: pausar, acelerar ou voltar mantém a cena certa.
 */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const MIOLO: Record<TipoDeApoio, string> = { cura: '#7dffb0', escudo: '#8edeff', reforco: '#ffd36b', reviver: '#fff1a8', purificar: '#bff5ff' };

/** O símbolo do que a esfera leva. */
function Simbolo({ tipo }: { tipo: TipoDeApoio }): ReactNode {
  switch (tipo) {
    case 'cura': return <svg viewBox="0 0 24 24"><path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z" fill="#fff" /></svg>;
    case 'escudo': return <svg viewBox="0 0 24 24"><path d="M12 2 21 5.5v6.2c0 5-3.8 8.6-9 10.3-5.2-1.7-9-5.3-9-10.3V5.5z" fill="#fff" /></svg>;
    case 'reforco': return <svg viewBox="0 0 24 24"><path d="M12 3 21 12h-5.5v9h-7v-9H3z" fill="#fff" /></svg>;
    case 'reviver': return <svg viewBox="0 0 24 24"><path d="M12 2l2.6 6.6L21.5 9l-5.3 4.5L18 20.5 12 16.8 6 20.5l1.8-7L2.5 9l6.9-.4z" fill="#fff" /></svg>;
    case 'purificar': return <svg viewBox="0 0 24 24"><path d="M12 2c3.5 5 6.5 8.4 6.5 12.2A6.5 6.5 0 0 1 5.5 14.2C5.5 10.4 8.5 7 12 2z" fill="#fff" /></svg>;
  }
}

type Props = { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; reduced: boolean };
export function EntregaDeApoio({ battle, beat, anchors, box, reduced }: Props) {
  if (!beat || !box.w || reduced) return null;
  const entregas = entregasDeApoio(beat);
  if (!entregas.length) return null;
  const dono = battle.fighters.find((f) => f.uid === beat.event.source);
  if (!dono) return null;
  const cor = profileFor(dono.characterId, beat.event.skill)?.color ?? '#9fe0ff';
  const depois = beat.elapsed - duracaoBase(beat) * P.impactAt;
  const px = (uid: string) => { const a = anchors[uid] ?? fallbackPoint(uid); return { x: (a.x / 100) * box.w, y: (a.y / 100) * box.h }; };
  const M = box.medal, de = px(dono.uid), nos: ReactNode[] = [];
  entregas.forEach((x, i) => {
    const para = px(x.alvo), forma = x.sai - 0.22;
    if (depois < forma || depois > x.chega + 0.5) return;
    const estilo = (l: number, t: number, d: number, extra: CSSProperties = {}) => ({ left: l, top: t, width: d, height: d, '--ap': cor, '--ap-miolo': MIOLO[x.tipo], ...extra } as CSSProperties);
    // os aliados ficam na mesma fileira: o arco sobe para o meio da arena (o mais longe, mais alto)
    const vx = para.x - de.x, vy = para.y - de.y, rumo = dono.side === 'player' ? -1 : 1;
    const alto = Math.min(M * 1.15, Math.hypot(vx, vy) * 0.38) + M * 0.15 * i;
    const ponto = (q: number) => { const e = q * q * (3 - 2 * q), c = alto * Math.sin(Math.PI * q); return { x: de.x + vx * e, y: de.y + vy * e + c * rumo }; };
    const D = M * 0.5;
    if (depois < x.sai) {
      // a esfera se forma na frente de quem usou
      const s = clamp((depois - forma) / 0.22);
      nos.push(<i key={`forma-${i}`} className="ap-bola" style={estilo(de.x, de.y - M * 0.1, D * (0.3 + 0.7 * s), { opacity: s })}><Simbolo tipo={x.tipo} /></i>);
      nos.push(<i key={`brilho-${i}`} className="ap-anel" style={estilo(de.x, de.y - M * 0.1, D * (2.2 - s), { opacity: s * 0.8 })} />);
      return;
    }
    if (depois < x.chega) {
      const p = clamp((depois - x.sai) / (x.chega - x.sai)), aqui = ponto(p);
      for (let k = 1; k <= 5; k++) { const q = ponto(clamp(p - k * 0.05)); nos.push(<i key={`rastro-${i}-${k}`} className="ap-rastro" style={estilo(q.x, q.y, D * (1 - k * 0.13), { opacity: 0.55 - k * 0.09 })} />); }
      // as faíscas que se soltam do caminho
      for (let k = 0; k < 4; k++) { const q = clamp(p - 0.08 - k * 0.07), c = ponto(q), sobe = (p - q) * M * 1.2; nos.push(<i key={`faisca-${i}-${k}`} className="ap-faisca" style={estilo(c.x + Math.sin((k + 1) * 2.3 + i) * M * 0.12, c.y - sobe, M * 0.07, { opacity: 0.9 - (p - q) * 3 })} />); }
      nos.push(<i key={`bola-${i}`} className="ap-bola" style={estilo(aqui.x, aqui.y, D * (1 + 0.15 * Math.sin(Math.PI * p)))}><Simbolo tipo={x.tipo} /></i>);
      return;
    }
    // estoura no aliado: o anel abre e o símbolo sobe e some
    const t = clamp((depois - x.chega) / 0.5);
    nos.push(<i key={`estouro-${i}`} className="ap-anel ap-estouro" style={estilo(para.x, para.y, M * (0.6 + 1.1 * t), { opacity: 1 - t })} />);
    nos.push(<i key={`sobe-${i}`} className="ap-bola ap-sobe" style={estilo(para.x, para.y - M * (0.2 + 0.5 * t), D * (1 - 0.3 * t), { opacity: 1 - t })}><Simbolo tipo={x.tipo} /></i>);
  });
  if (!nos.length) return null;
  return <div className="entrega-de-apoio" aria-hidden="true">{nos}</div>;
}
