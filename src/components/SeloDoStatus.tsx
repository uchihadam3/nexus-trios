import type { CSSProperties, ReactNode } from 'react';
import type { BattleEvent, StatusId } from '../engine/types';
import { statuses } from '../data/statuses';

/*
 * O selo do Status (pedido do jogador: "tem que verificar todo tipo de habilidade… defensiva, ofensiva, suporte…
 * tudo tem que ser muito bem feito"): quando um Status entra, o ícone dele cai grande no retrato com um anel na cor
 * dele, o nome aparece embaixo, e um desenho próprio conta o que ele faz (as estrelas girando no Paralisado, as
 * correntes no Preso, o relógio no Lento, a mira no Marcado, as setas subindo no Fortalecido…). Depois o selo desce
 * para a linha de Status, onde o ícone fica. Antes era só uma etiqueta pequena no canto do retrato.
 */
const estrela = (x: number, y: number, r: number) => {
  const p = Array.from({ length: 10 }, (_, i) => { const a = (i * Math.PI) / 5 - Math.PI / 2, d = i % 2 ? r * 0.45 : r; return `${(x + Math.cos(a) * d).toFixed(1)},${(y + Math.sin(a) * d).toFixed(1)}`; });
  return <polygon points={p.join(' ')} />;
};
const seta = (x: number, y: number, s: number, cima: boolean) => <path d={cima ? `M${x} ${y - s} L${x + s} ${y} H${x + s * 0.45} V${y + s} H${x - s * 0.45} V${y} H${x - s} Z` : `M${x} ${y + s} L${x + s} ${y} H${x + s * 0.45} V${y - s} H${x - s * 0.45} V${y} H${x - s} Z`} />;

/** O desenho que conta o que o Status faz, em volta do retrato (viewBox 100×100, o retrato no meio). */
function Motivo({ status }: { status: StatusId }): ReactNode {
  switch (status) {
    case 'paralyzed': return <g className="ssm-gira">{estrela(50, 4, 6)}{estrela(78, 12, 5)}{estrela(22, 12, 5)}</g>;
    case 'confused': return <g className="ssm-gira"><path d="M50 2 a8 8 0 1 1 -8 8 a5 5 0 1 1 5 -5 a2.5 2.5 0 1 1 -2.5 2.5" fill="none" strokeWidth="2.6" /><circle cx="76" cy="12" r="3" /><circle cx="24" cy="12" r="3" /></g>;
    case 'slow': return <g className="ssm-pendulo"><circle cx="50" cy="8" r="9" fill="none" strokeWidth="2.4" /><path d="M50 8 V2.5 M50 8 L54 10" strokeWidth="2.2" fill="none" /></g>;
    case 'rooted': return <g className="ssm-aperta" fill="none" strokeWidth="3.2"><ellipse cx="50" cy="86" rx="40" ry="9" /><ellipse cx="50" cy="78" rx="44" ry="10" strokeDasharray="7 5" /></g>;
    case 'exposed': return <g className="ssm-racha" fill="none" strokeWidth="2.4"><path d="M30 22 L42 40 L36 52 L48 66" /><path d="M72 30 L60 44 L68 58" /></g>;
    case 'marked': return <g className="ssm-mira" fill="none" strokeWidth="2.6"><circle cx="50" cy="50" r="46" /><path d="M50 0 V16 M50 84 V100 M0 50 H16 M84 50 H100" /></g>;
    case 'weakened': return <g className="ssm-cai">{seta(22, 20, 7, false)}{seta(78, 20, 7, false)}{seta(50, 8, 6, false)}</g>;
    case 'burning': return <g className="ssm-sobe"><path d="M24 92 C16 80 26 74 24 64 C34 72 36 82 24 92 Z" /><path d="M76 92 C68 80 78 74 76 64 C86 72 88 82 76 92 Z" /><path d="M50 98 C40 84 52 76 50 64 C62 74 64 86 50 98 Z" /></g>;
    case 'electric': return <g className="ssm-pisca" fill="none" strokeWidth="2.8"><path d="M6 30 L18 38 L10 46 L22 54" /><path d="M94 30 L82 38 L90 46 L78 54" /><path d="M40 4 L50 12 L44 18 L56 24" /></g>;
    case 'silenced': return <g className="ssm-pulsa"><path d="M34 2 h32 a6 6 0 0 1 6 6 v12 a6 6 0 0 1 -6 6 h-18 l-8 7 v-7 h-6 a6 6 0 0 1 -6 -6 v-12 a6 6 0 0 1 6 -6z" /><path d="M43 7 L57 21 M57 7 L43 21" stroke="#1a1020" strokeWidth="3" /></g>;
    case 'strengthened': return <g className="ssm-sobe">{seta(20, 70, 7, true)}{seta(80, 70, 7, true)}{seta(50, 92, 6, true)}</g>;
    case 'haste': return <g className="ssm-corre" fill="none" strokeWidth="3"><path d="M2 40 H22 M6 50 H26 M2 60 H22" /><path d="M98 40 H78 M94 50 H74 M98 60 H78" /></g>;
    case 'regen': return <g className="ssm-sobe"><path d="M18 70 h4 v-4 h4 v4 h4 v4 h-4 v4 h-4 v-4 h-4z" /><path d="M72 78 h4 v-4 h4 v4 h4 v4 h-4 v4 h-4 v-4 h-4z" /><path d="M46 90 h3 v-3 h3 v3 h3 v3 h-3 v3 h-3 v-3 h-3z" /></g>;
    case 'protected': return <g className="ssm-brilha" fill="none" strokeWidth="2.6"><path d="M50 -2 L94 14 V44 C94 74 74 92 50 102 C26 92 6 74 6 44 V14 Z" /></g>;
    case 'thorns': return <g className="ssm-pulsa">{Array.from({ length: 10 }, (_, i) => { const a = (i * Math.PI) / 5; return <path key={i} d={`M${50 + Math.cos(a) * 44} ${50 + Math.sin(a) * 44} L${50 + Math.cos(a + 0.12) * 52} ${50 + Math.sin(a + 0.12) * 52} L${50 + Math.cos(a - 0.12) * 52} ${50 + Math.sin(a - 0.12) * 52}Z`} />; })}</g>;
    case 'reflect': return <g className="ssm-brilha" fill="none" strokeWidth="2.6"><path d="M8 20 L20 8 M80 8 L92 20 M8 80 L20 92 M80 92 L92 80" /><circle cx="50" cy="50" r="47" strokeDasharray="10 8" /></g>;
    case 'evasion': return <g className="ssm-corre" fill="none" strokeWidth="2.4"><circle cx="38" cy="50" r="40" opacity=".45" /><circle cx="62" cy="50" r="40" opacity=".3" /></g>;
    case 'vampirism': return <g className="ssm-sobe"><path d="M30 76 c-6 -8 -8 -14 0 -18 c8 4 6 10 0 18z" /><path d="M70 76 c-6 -8 -8 -14 0 -18 c8 4 6 10 0 18z" /></g>;
    default: return null;
  }
}

/** Os Status que entraram neste passo, no lutador (até três, um ao lado do outro). */
export function SeloDoStatus({ eventos }: { eventos: BattleEvent[] }) {
  const lista = eventos.filter((e) => e.status && statuses[e.status]).slice(0, 3);
  if (!lista.length) return null;
  return <span className="selos-de-status" aria-hidden="true">{lista.map((e, i) => {
    const st = statuses[e.status!], bom = st.tone === 'positivo';
    return <span key={e.id} className={`selo-status ${bom ? 'ss-bom' : 'ss-ruim'}`} style={{ '--st': st.color, '--ss-i': i, '--ss-n': lista.length } as CSSProperties}>
      <svg className="ss-motivo" viewBox="0 0 100 100" style={{ fill: st.color, stroke: st.color }}><Motivo status={e.status!} /></svg>
      <i className="ss-anel" />
      <img className="ss-icone" src={`/assets/statuses/${e.status}.png`} alt="" />
      <b className="ss-nome">{st.name}</b>
    </span>;
  })}</span>;
}
