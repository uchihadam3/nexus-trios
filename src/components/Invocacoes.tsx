import type { CSSProperties } from 'react';
import { byId } from '../data/characters';
import { RITMO_DA_INVOCACAO } from '../data/statuses';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { fallbackPoint, type Anchors } from './BattleEffects';

/*
 * A invocação como bolinha (pedido do jogador: "quando eles invocar aparecer uma bolinha… menorzinha…
 * na diagonal… com o desenho do que eles invoca… ela vai enchendo… e quando ela enche, ela faz o
 * ataque… se ela ataca de perto, ela vai lá, bate no bicho e volta; se ataca de longe, faz o efeito").
 *
 * Um medalhão pequeno na diagonal da frente de quem invocou, virado para o meio do campo (em cima à
 * direita no seu trio, embaixo à esquerda nos rivais), com o desenho da criatura (tools/vfx/invocacoes_icones.py). O anel enche no ritmo dos
 * ataques (RITMO_DA_INVOCACAO); no ataque, quem bate de perto voa até o alvo e volta, quem ataca de
 * longe dá o tranco e o efeito da criatura sai dela (BattleEffects). Um arco fino por fora mostra o
 * tempo que falta.
 */
export const DE_PERTO = new Set(['megumi', 'jinwoo', 'bayonetta', 'jotaro', 'pain', 'mickey', 'plankton']);
export const COR_DA_INVOCACAO: Record<string, string> = {
  megumi: '#e8eef8', jinwoo: '#9a6cff', yugi: '#9a6cff', kaiba: '#7fc8ff', bayonetta: '#ff4a6e',
  jotaro: '#8aa2ff', pain: '#d8b080', mickey: '#e8c070', plankton: '#7fe07f', krang: '#ff8ac8',
};
/** Onde a bolinha fica, em px a partir do centro do medalhão de quem invocou. */
// sempre na diagonal da frente, virada para o meio do campo (pedido do jogador): no seu trio, em cima à
// direita; nos rivais (que ficam no alto), embaixo à esquerda
export const posicaoDaInvocacao = (lado: 'player' | 'enemy', medal: number) => (lado === 'player' ? { dx: medal * 0.6, dy: -medal * 0.44 } : { dx: -medal * 0.6, dy: medal * 0.44 });

export function Invocacoes({ battle, beat, anchors, box, velocidade }: { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; velocidade: number }) {
  const r = Math.round(box.medal * 0.25), C = 2 * Math.PI * (r - 3);
  return <div className="invocacoes" aria-hidden>
    {battle.fighters.map((f) => {
      const s = f.hp > 0 ? f.statuses.find((x) => x.id === 'summon') : undefined;
      if (!s) return null;
      const p = anchors[f.uid] ?? fallbackPoint(f.uid), { dx, dy } = posicaoDaInvocacao(f.side, box.medal);
      const total = s.duration ?? s.remaining, passou = total - s.remaining;
      const enche = ((passou % RITMO_DA_INVOCACAO) + RITMO_DA_INVOCACAO) % RITMO_DA_INVOCACAO / RITMO_DA_INVOCACAO;
      const resta = Math.max(0, Math.min(1, s.remaining / Math.max(total, 0.1)));
      const ataque = beat?.event.kind === 'summon' && beat.event.source === f.uid ? beat.event : undefined;
      const alvo = ataque?.target ? anchors[ataque.target] ?? fallbackPoint(ataque.target) : undefined;
      const perto = DE_PERTO.has(f.characterId);
      // até o alvo, em px (as âncoras são % da arena)
      const vai = alvo ? { x: ((alvo.x - p.x) / 100) * box.w - dx, y: ((alvo.y - p.y) / 100) * box.h - dy } : { x: 0, y: 0 };
      const cor = COR_DA_INVOCACAO[f.characterId] ?? '#c9a2ff';
      return <div key={`${f.uid}-${ataque?.id ?? 'parada'}`} className={`invocacao ${f.side} ${ataque ? (perto ? 'ataca-perto' : 'ataca-longe') : ''}`}
        style={{ left: `calc(${p.x}% + ${dx}px)`, top: `calc(${p.y}% + ${dy}px)`, width: r * 2, height: r * 2, '--cor': cor, '--vx': `${vai.x * 0.82}px`, '--vy': `${vai.y * 0.82}px`, '--dur': `${0.62 / Math.max(velocidade, 0.25)}s` } as CSSProperties}
        title={byId[f.characterId]?.invocacao}>
        {ataque && !perto && alvo && <i className="inv-disparo" style={{ width: Math.hypot(vai.x, vai.y), transform: `rotate(${Math.atan2(vai.y, vai.x)}rad)` }} />}
        <img src={`/assets/invocacoes/${f.characterId}.webp`} alt="" />
        <svg viewBox={`0 0 ${r * 2} ${r * 2}`}>
          <circle className="inv-trilho" cx={r} cy={r} r={r - 3} />
          <circle className="inv-carga" cx={r} cy={r} r={r - 3} strokeDasharray={`${C * enche} ${C}`} transform={`rotate(-90 ${r} ${r})`} />
          <circle className="inv-tempo" cx={r} cy={r} r={r - 0.5} strokeDasharray={`${2 * Math.PI * (r - 0.5) * resta} ${2 * Math.PI * r}`} transform={`rotate(-90 ${r} ${r})`} />
        </svg>
      </div>;
    })}
  </div>;
}
