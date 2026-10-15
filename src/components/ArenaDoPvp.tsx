import { useEffect, useMemo, useRef, useState } from 'react';
import { createBattle } from '../engine/battle';
import type { Battle, Side } from '../engine/types';
import { VELOCIDADE_DO_PVP } from '../engine/pvp';
import { advanceDirection, createDirection, type Beat, type Direction } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { estadoDosSons, somDoCue, sonsDoQuadro } from '../presentation/sons-da-luta';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import type { Settings } from '../lib/storage';
import { BattleScreen } from '../screens/BattleScreen';

/*
 * A luta de uma rodada do PvP: o mesmo motor, o mesmo diretor de cena e os mesmos sons da jornada
 * (src/presentation/sons-da-luta.ts), a música da Arena e sempre em 2× (pedido do jogador). A luta é sorteada pela
 * semente da rodada: o mesmo time contra o mesmo time com a mesma semente dá sempre a mesma luta, nos dois aparelhos.
 */
const RECUPERA_POR_QUADRO = 60;

export function ArenaDoPvp({ meu, dele, seed, rodada, rival, settings, onSettings, podePausar, onFim, onDesistir }: {
  meu: string[]; dele: string[]; seed: number; rodada: number; rival: string; settings: Settings; onSettings: (s: Settings) => void;
  podePausar: boolean; onFim: (vencedor: Side) => void; onDesistir: () => void;
}) {
  const inicial = useMemo(() => createBattle(meu, dele, seed), [meu, dele, seed]);
  const direcao = useRef<Direction | null>(null);
  const sons = useMemo(() => estadoDosSons(), []);
  const [tela, setTela] = useState<{ battle: Battle; beat: Beat | null }>({ battle: inicial, beat: null });
  const [pausado, setPausado] = useState(false);
  const terminou = useRef(false);
  const fim = useRef(onFim); fim.current = onFim;
  const config = useMemo(() => ({ ...settings, speed: VELOCIDADE_DO_PVP as 1 | 2 }), [settings]);

  // a música da Arena enquanto a luta corre
  useEffect(() => {
    battleAudio.setBattle(!pausado, `pvp-${seed}`, 'arena');
    return () => battleAudio.setBattle(false);
  }, [pausado, seed]);

  useEffect(() => {
    if (pausado) return;
    let antes = performance.now(), divida = 0;
    const t = window.setInterval(() => {
      const agora = performance.now(), bruto = Math.max(0, (agora - antes) / 1000), passo = Math.min(P.renderIntervalMs / 1000, bruto);
      antes = agora;
      if (!direcao.current) { direcao.current = createDirection(inicial); sons.lastAudio.current = inicial.nextEvent - 1; sons.lastDominionSound.current = inicial.dominion; }
      const d = direcao.current;
      // o tempo que o celular não deixou rodar (app em segundo plano): a luta alcança o relógio sem som
      divida = Math.min(20 * 60, divida + Math.max(0, bruto - passo));
      let resta = Math.min(divida, RECUPERA_POR_QUADRO); divida -= resta;
      while (resta > 1e-6 && !d.complete) { const p = Math.min(P.renderIntervalMs / 1000, resta); advanceDirection(d, p, undefined, VELOCIDADE_DO_PVP); resta -= p; }
      const mudo = document.hidden;
      advanceDirection(d, passo, (cue) => { if (!mudo) somDoCue(d, cue); }, VELOCIDADE_DO_PVP);
      sonsDoQuadro(d, sons, mudo);
      setTela({ battle: d.visible, beat: d.active ? { ...d.active } : null });
      if (d.complete && !terminou.current) {
        terminou.current = true;
        const vencedor = d.battle.winner ?? 'enemy';
        battleAudio.sound(vencedor === 'player' ? 'vitoria' : 'derrota', PRIORIDADE.grand);
        window.setTimeout(() => fim.current(vencedor), 1400);
      }
    }, P.renderIntervalMs);
    return () => clearInterval(t);
  }, [pausado, inicial, sons]);

  return <BattleScreen battle={tela.battle} beat={tela.beat} index={rodada - 1} name={`Rodada ${rodada}`} settings={config} paused={pausado}
    onPause={() => { if (podePausar) setPausado(!pausado); }} onAbandon={onDesistir} onSettings={(s) => onSettings({ ...s, speed: settings.speed })}
    pvp={{ rodada, voce: 'VOCÊ', rival, podePausar }} />;
}
