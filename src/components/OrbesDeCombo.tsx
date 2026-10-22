import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { Link2 } from 'lucide-react';
import type { Battle, Side } from '../engine/types';
import { fallbackPoint, type Anchors } from './BattleEffects';
import { t } from '../i18n/idioma';

/*
 * As duas bolinhas de combos da luta (pedido do jogador): uma de cada lado,
 * no centro da arena, ao lado do VS (o único espaço vazio, deitado ou em pé:
 * nos cantos elas tapavam a Vida dos lutadores). Apagadas com 0 quando o trio não tem combo;
 * acesas, com o número, quando tem. Tocar abre os combos ativos daquele lado.
 *
 * Quando um combo de tempo em tempo dispara (evento `pulso`), a bolinha do
 * lado dele pulsa e um rastro sutil sai dela até quem recebe o efeito — dá
 * para ver o que ativou e para onde foi, sem atrapalhar os outros efeitos.
 */
type Rastro = { id: number; lado: Side; x0: number; y0: number; x: number; y: number };
/** O centro de um elemento em % da arena (o mesmo sistema das âncoras dos lutadores). */
function centroNaArena(el: HTMLElement | null): { x: number; y: number } | null {
  const arena = el?.closest('.arena');
  if (!el || !arena) return null;
  const a = arena.getBoundingClientRect(), r = el.getBoundingClientRect();
  if (!a.width || !a.height) return null;
  return { x: (100 * (r.left + r.width / 2 - a.left)) / a.width, y: (100 * (r.top + r.height / 2 - a.top)) / a.height };
}

export function OrbesDeCombo({ battle, anchors, onAbrir, reduzido }: { battle: Battle; anchors: Anchors; onAbrir: (lado: Side) => void; reduzido: boolean }) {
  const [pulsando, setPulsando] = useState<Record<Side, number>>({ player: 0, enemy: 0 });
  const [rastros, setRastros] = useState<Rastro[]>([]);
  const visto = useRef(0), bolas = useRef<Record<Side, HTMLSpanElement | null>>({ player: null, enemy: null });
  useEffect(() => {
    // só os pulsos novos desde a última olhada (voltar para uma luta no meio não repete os antigos)
    if (!visto.current) { visto.current = battle.nextEvent - 1; return; }
    const novos = battle.events.filter((e) => e.kind === 'pulso' && e.id > visto.current);
    visto.current = battle.nextEvent - 1;
    if (!novos.length) return;
    const agora = performance.now();
    for (const e of novos) {
      const lado = battle.fighters.find((f) => f.uid === e.source)?.side;
      if (!lado) continue;
      setPulsando((p) => ({ ...p, [lado]: agora }));
      if (e.target && !reduzido) {
        const alvo = anchors[e.target] ?? fallbackPoint(e.target), de = centroNaArena(bolas.current[lado]);
        if (de) setRastros((r) => [...r.slice(-5), { id: e.id, lado, x0: de.x, y0: de.y, x: alvo.x, y: alvo.y }]);
      }
    }
  }, [battle.nextEvent]);
  useEffect(() => {
    if (!rastros.length) return;
    const t = window.setTimeout(() => setRastros((r) => r.slice(1)), 1100);
    return () => clearTimeout(t);
  }, [rastros]);
  const combos = battle.combos;
  return <>
    <div className="cb-orbes">{(['player', 'enemy'] as Side[]).map((lado) => {
      const n = combos?.[lado].length ?? 0;
      const pulso = performance.now() - pulsando[lado] < 1300;
      return <button key={lado} type="button" className={`cb-orbe ${lado} ${n ? 'acesa' : 'apagada'} ${pulso ? 'pulsando' : ''}`}
        onClick={() => onAbrir(lado)} aria-label={`${lado === 'player' ? t('Seus combos') : t('Combos do rival')}: ${n}`}>
        <span className="cb-orbe-bola" ref={(el) => { bolas.current[lado] = el; }}>
          <Link2 size={12} className="cb-orbe-icone" />
          <span className="cb-orbe-nome">{lado === 'player' ? t('VOCÊ') : t('RIVAL')}</span>
          <b key={`${n}-${pulsando[lado]}`}>{n}</b>
        </span>
      </button>;
    })}</div>
    {rastros.map((r) => <span key={r.id} className={`cb-rastro ${r.lado}`} aria-hidden
      style={{ '--x0': `${r.x0}%`, '--y0': `${r.y0}%`, '--x1': `${r.x}%`, '--y1': `${r.y}%` } as CSSProperties} />)}
  </>;
}
