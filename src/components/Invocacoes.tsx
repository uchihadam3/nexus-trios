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
export const DE_PERTO = new Set(['megumi', 'jinwoo', 'bayonetta', 'jotaro', 'pain', 'mickey', 'plankton', 'agentsmith', 'xenomorph', 'steve', 'makima', 'hel', 'dracula', 'ainz', 'jiraiya']);
export const COR_DA_INVOCACAO: Record<string, string> = {
  megumi: '#e8eef8', jinwoo: '#9a6cff', yugi: '#9a6cff', kaiba: '#7fc8ff', bayonetta: '#ff4a6e',
  jotaro: '#8aa2ff', pain: '#d8b080', mickey: '#e8c070', plankton: '#7fe07f', krang: '#ff8ac8',
  naruto: '#ffb04c', agentsmith: '#5ae08a', xenomorph: '#8ab8c0', steve: '#d8d4c8', makima: '#ff9060',
  odin: '#75b7ff', hel: '#55e8c5', pennywise: '#ef4b40', dracula: '#e35a67', ainz: '#db515a', jiraiya: '#ef9a54',
};
const imagemDaInvocacao = (id: string) => `${import.meta.env.BASE_URL}assets/invocacoes/${id}.webp`;
/** Onde a bolinha fica, em px a partir do centro do medalhão de quem invocou. */
// sempre na diagonal da frente, virada para o meio do campo (pedido do jogador): no seu trio, em cima à
// direita; nos rivais (que ficam no alto), embaixo à esquerda
export const posicaoDaInvocacao = (lado: 'player' | 'enemy', medal: number) => (lado === 'player' ? { dx: medal * 0.6, dy: -medal * 0.44 } : { dx: -medal * 0.6, dy: medal * 0.44 });

/*
 * As miniaturas da Mecânica única (pedido do jogador: "o Mickey… invoca até quatro pequenininhas… uma menor pela
 * metade do tamanho… em volta dele"): quem junta criaturas pela mecânica mostra cada uma como uma bolinha pela metade,
 * num arco em volta do medalhão (longe da invocação grande e da bolinha da mecânica). No relógio do ataque delas,
 * cada uma dá o bote para o lado dos rivais e volta.
 */
// relogio: o bote sai quando esse relógio da mecânica dá a volta; sem relógio, o bote acompanha o ataque básico de quem
// invocou. menos: quantas já aparecem na invocação grande (as cópias do Smith).
export const MINIATURAS: Record<string, { k: string; max: number; relogio?: string; menos?: number }> = {
  mickey: { k: 'vassouras', max: 4, relogio: 'relogio_vassoura' },
  agentsmith: { k: 'copias', max: 3, menos: 1 },
  naruto: { k: 'clones', max: 2 },
};
/** O arco das miniaturas, em graus da tela (0 = direita, −90 = em cima): por cima no seu trio, por baixo nos rivais. */
const ARCO_DAS_MINIATURAS = [-150, -122, -94, -66];
export const posicaoDaMiniatura = (lado: 'player' | 'enemy', i: number, medal: number) => {
  const a = ((ARCO_DAS_MINIATURAS[i] ?? -90) + (lado === 'enemy' ? 180 : 0)) * Math.PI / 180;
  return { dx: Math.cos(a) * medal * 0.6, dy: Math.sin(a) * medal * 0.6 };
};

export function Invocacoes({ battle, beat, anchors, box, velocidade }: { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; velocidade: number }) {
  const r = Math.round(box.medal * 0.25), C = 2 * Math.PI * (r - 3);
  const rm = Math.max(7, Math.round(r / 2));
  return <div className="invocacoes" aria-hidden>
    {battle.fighters.flatMap((f) => {
      const mini = f.hp > 0 ? MINIATURAS[f.characterId] : undefined;
      // as cópias do Smith só existem com a invocação de pé
      const n = !mini || (mini.menos && !f.statuses.some((x) => x.id === 'summon')) ? 0 : Math.min(mini.max, Math.floor(f.u?.[mini.k] ?? 0)) - (mini.menos ?? 0);
      if (!mini || n <= 0) return [];
      const p = anchors[f.uid] ?? fallbackPoint(f.uid);
      // o bote: logo depois que o relógio dá a volta (é quando elas batem), ou junto do ataque de quem invocou
      const bote = mini.relogio
        ? (f.u?.[`${mini.relogio}_volta`] ?? 3) - (f.u?.[mini.relogio] ?? 99) < 0.5
        : !!beat && beat.event.source === f.uid && (beat.event.kind === 'basic' || beat.event.kind === 'summon');
      const cor = COR_DA_INVOCACAO[f.characterId] ?? '#c9a2ff';
      return Array.from({ length: n }, (_, i) => {
        const { dx, dy } = posicaoDaMiniatura(f.side, i, box.medal);
        return <div key={`${f.uid}-mini-${i}`} className={`invocacao miniatura ${f.side}${bote ? ' bote' : ''}`}
          style={{ left: `calc(${p.x}% + ${dx}px)`, top: `calc(${p.y}% + ${dy}px)`, width: rm * 2, height: rm * 2, '--cor': cor, '--atraso': `${i * 0.07}s` } as CSSProperties}>
          <img src={imagemDaInvocacao(f.characterId)} alt="" />
        </div>;
      });
    })}
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
        <img src={imagemDaInvocacao(f.characterId)} alt="" />
        <svg viewBox={`0 0 ${r * 2} ${r * 2}`}>
          <circle className="inv-trilho" cx={r} cy={r} r={r - 3} />
          <circle className="inv-carga" cx={r} cy={r} r={r - 3} strokeDasharray={`${C * enche} ${C}`} transform={`rotate(-90 ${r} ${r})`} />
          <circle className="inv-tempo" cx={r} cy={r} r={r - 0.5} strokeDasharray={`${2 * Math.PI * (r - 0.5) * resta} ${2 * Math.PI * r}`} transform={`rotate(-90 ${r} ${r})`} />
        </svg>
      </div>;
    })}
  </div>;
}
