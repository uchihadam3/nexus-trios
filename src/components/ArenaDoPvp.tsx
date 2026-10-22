import { useEffect, useMemo, useRef, useState } from 'react';
import { createBattle } from '../engine/battle';
import type { Battle, Side } from '../engine/types';
import { VELOCIDADE_DO_PVP } from '../engine/pvp';
import { advanceDirection, createDirection, type Beat, type Direction } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { estadoDosSons, somDoCue, sonsDoQuadro } from '../presentation/sons-da-luta';
import { battleAudio, type Faixa } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import type { Settings } from '../lib/storage';
import { BattleScreen } from '../screens/BattleScreen';
import { espelhar } from '../presentation/espelho';
import { t } from '../i18n/idioma';

/*
 * A luta de uma rodada do PvP: o mesmo motor, o mesmo diretor de cena e os mesmos sons da jornada
 * (src/presentation/sons-da-luta.ts), a música da Arena e, contra pessoas, sempre em VELOCIDADE_DO_PVP (3×, pedido do dono). A luta é sorteada pela
 * semente da rodada: o mesmo time contra o mesmo time com a mesma semente dá sempre a mesma luta, nos dois aparelhos.
 * No online a luta é calculada com o desafiante embaixo; quem foi desafiado vê a mesma luta espelhada
 * (src/presentation/espelho.ts), com o time dele embaixo. Quem entra atrasado alcança a luta sem som, de uma vez, antes
 * do primeiro quadro (no treino, quem sai e volta reencontra a luta no mesmo ponto, pausada: onTempo guarda o ponto).
 */
const RECUPERA_POR_QUADRO = 60, MAXIMO_DE_ATRASO = 20 * 60;

export function ArenaDoPvp({ meu, dele, seed, rodada, rival, settings, onSettings, podePausar, onFim, onDesistir, espelhado = false, atrasoInicial = 0, comecaPausado = false, onTempo, escala = 1, faixa = 'arena', velocidadeLivre = false }: {
  meu: string[]; dele: string[]; seed: number; rodada: number; rival: string; settings: Settings; onSettings: (s: Settings) => void;
  podePausar: boolean; onFim: (vencedor: Side) => void; onDesistir: () => void;
  /** Online, para quem foi desafiado: a luta é a do desafiante (ele embaixo), desenhada do outro lado. */
  espelhado?: boolean;
  /** Segundos que a luta já correu quando a tela abriu (entrou atrasado, ou voltou para o treino). */
  atrasoInicial?: number;
  /** Abre pausada (o treino retomado: o jogador toca em Continuar). */
  comecaPausado?: boolean;
  /** Os segundos de luta já mostrados, mais ou menos a cada segundo (para retomar no mesmo ponto). */
  onTempo?: (segundos: number) => void;
  /** Contra a IA (treino e Caminho do Nexus) a velocidade é do jogador (1×, 2×, 3×); contra pessoas fica travada em VELOCIDADE_DO_PVP (3×). */
  velocidadeLivre?: boolean;
  /** A Vida a mais no lado do rival (a Aura do Chefe da campanha). */
  escala?: number;
  /** A música da luta (a campanha usa outras nos chefes). */
  faixa?: Faixa;
}) {
  const inicial = useMemo(() => (espelhado ? createBattle(dele, meu, seed) : createBattle(meu, dele, seed, escala)), [meu, dele, seed, espelhado, escala]);
  const direcao = useRef<Direction | null>(null);
  const sons = useMemo(() => estadoDosSons(), []);
  const [tela, setTela] = useState<{ battle: Battle; beat: Beat | null }>({ battle: inicial, beat: null });
  const [pausado, setPausado] = useState(comecaPausado);
  const terminou = useRef(false);
  const fim = useRef(onFim); fim.current = onFim;
  const tempo = useRef(onTempo); tempo.current = onTempo;
  const atraso = useRef(Math.min(MAXIMO_DE_ATRASO, Math.max(0, atrasoInicial)));
  const decorrido = useRef(0), avisado = useRef(-1);
  const vel = velocidadeLivre ? settings.speed : VELOCIDADE_DO_PVP;
  const config = useMemo(() => ({ ...settings, speed: vel as Settings['speed'] }), [settings, vel]);

  // a música da Arena enquanto a luta corre
  useEffect(() => {
    battleAudio.setBattle(!pausado, `pvp-${seed}`, faixa);
    return () => battleAudio.setBattle(false);
  }, [pausado, seed, faixa]);

  const mostra = (d: Direction) => setTela(espelhado ? { battle: espelhar(d.visible), beat: d.active ? espelhar({ ...d.active }) : null } : { battle: d.visible, beat: d.active ? { ...d.active } : null });
  /** A direção da luta; quem chega atrasado (ou volta ao treino) alcança o ponto de uma vez, sem som. */
  const garante = () => {
    if (direcao.current) return direcao.current;
    const d = createDirection(inicial); sons.lastAudio.current = inicial.nextEvent - 1; sons.lastDominionSound.current = inicial.dominion;
    let resta = atraso.current; atraso.current = 0; decorrido.current = resta;
    // com a velocidade livre o tempo guardado está em segundos de luta a 1× (trocar a velocidade não muda o ponto)
    while (resta > 1e-6 && !d.complete) { const p = Math.min(P.renderIntervalMs / 1000, resta); advanceDirection(d, p, undefined, velocidadeLivre ? 1 : vel); resta -= p; }
    if (decorrido.current > 0) sonsDoQuadro(d, sons, true);
    direcao.current = d;
    return d;
  };
  // o primeiro quadro já no ponto certo (importa quando abre pausada)
  useEffect(() => { mostra(garante()); }, []);

  useEffect(() => {
    if (pausado) return;
    let antes = performance.now(), divida = 0;
    const t = window.setInterval(() => {
      const agora = performance.now(), bruto = Math.max(0, (agora - antes) / 1000), passo = Math.min(P.renderIntervalMs / 1000, bruto);
      antes = agora;
      const d = garante();
      // o tempo que o celular não deixou rodar (app em segundo plano): a luta alcança o relógio sem som
      divida = Math.min(20 * 60, divida + Math.max(0, bruto - passo));
      let resta = Math.min(divida, RECUPERA_POR_QUADRO); divida -= resta; decorrido.current += (resta + passo) * (velocidadeLivre ? vel : 1);
      while (resta > 1e-6 && !d.complete) { const p = Math.min(P.renderIntervalMs / 1000, resta); advanceDirection(d, p, undefined, vel); resta -= p; }
      const mudo = document.hidden;
      advanceDirection(d, passo, (cue) => { if (!mudo) somDoCue(d, cue); }, vel);
      sonsDoQuadro(d, sons, mudo);
      mostra(d);
      const s = Math.floor(decorrido.current);
      if (s !== avisado.current && !d.complete) { avisado.current = s; tempo.current?.(s); }
      if (d.complete && !terminou.current) {
        terminou.current = true;
        const bruto = d.battle.winner ?? 'enemy', vencedor: Side = espelhado ? (bruto === 'player' ? 'enemy' : 'player') : bruto;
        battleAudio.sound(vencedor === 'player' ? 'vitoria' : 'derrota', PRIORIDADE.grand);
        window.setTimeout(() => fim.current(vencedor), 1400);
      }
    }, P.renderIntervalMs);
    return () => clearInterval(t);
  }, [pausado, inicial, sons, espelhado, vel]);

  return <BattleScreen battle={tela.battle} beat={tela.beat} index={rodada - 1} name={t('Rodada {n}', { n: rodada })} settings={config} paused={pausado}
    onPause={() => { if (podePausar) setPausado(!pausado); }} onAbandon={onDesistir} onSettings={(s) => onSettings(velocidadeLivre ? s : { ...s, speed: settings.speed })}
    pvp={{ rodada, voce: t('VOCÊ'), rival, podePausar, velocidadeLivre }} />;
}
