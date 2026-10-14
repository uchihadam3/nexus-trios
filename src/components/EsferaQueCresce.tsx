import type { CSSProperties, ReactNode } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { ativacaoNaTela, entregaDoEvento } from '../presentation/ativacao-da-unica';
import { ESFERA_QUE_CRESCE, estagiosDaEsfera } from '../presentation/esfera-que-cresce';
import { fallbackPoint, type Anchors } from './BattleEffects';

/*
 * A esfera que cresce em estágios (src/presentation/esfera-que-cresce.ts), a Genki Dama:
 *   1. o tempo para (o véu) e a esfera aparece em cima de quem ativou;
 *   2. a energia vem de todos os lados e ela cresce, estágio por estágio, cada um com um clarão e um tranco;
 *   3. no último, ela é lançada e voa pesada até o alvo; a explosão é a folha da Mecânica única (BattleEffects).
 * Tudo é calculado a cada quadro a partir do tempo da ativação: pausar, acelerar ou voltar mantém a cena certa.
 */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
/** O tranco de cada estágio: passa um pouco do tamanho novo e assenta. */
const mola = (x: number) => (x <= 0 ? 0 : 1 - Math.exp(-x * 12) * Math.cos(x * 26));

type Props = { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; reduced: boolean };
export function EsferaQueCresce({ battle, beat, anchors, box, reduced }: Props) {
  if (!beat || !box.w) return null;
  const nos: ReactNode[] = [];
  for (const dono of battle.fighters) {
    const esfera = ESFERA_QUE_CRESCE[dono.characterId];
    if (!esfera) continue;
    const at = ativacaoNaTela(beat, dono.uid);
    if (!at) continue;
    const { t, fases } = at, e = at.evento ?? beat.event;
    const fim = fases.efeitoEm + 0.35;
    if (t < 0 || t > fim) continue;
    const px = (uid: string) => { const a = anchors[uid] ?? fallbackPoint(uid); return { x: (a.x / 100) * box.w, y: (a.y / 100) * box.h }; };
    const M = box.medal, de = px(dono.uid), frente = dono.side === 'player' ? -1 : 1;
    const alvos = entregaDoEvento(e, battle, beat).destino.alvos.filter((x) => x !== dono.uid);
    const para = alvos.length ? px(alvos[0]!) : { x: box.w / 2, y: box.h / 2 };
    const inicios = estagiosDaEsfera(esfera, fases), S = esfera.estagios;
    // o estágio de agora e o tamanho com o tranco da mola
    let k = -1;
    inicios.forEach((t0, i) => { if (t >= t0) k = i; });
    const diametro = k < 0 ? 0 : M * ((S[k - 1] ?? 0) + (S[k]! - (S[k - 1] ?? 0)) * mola(t - inicios[k]!));
    // longe da borda: a esfera maior (com o tranco da mola) cabe inteira na tela
    const raio = M * S.at(-1)! * 0.62 + 6;
    const segura = { x: Math.max(raio, Math.min(box.w - raio, de.x)), y: de.y + frente * M * 1.15 };
    // o tempo parado: entra logo, sai depois de a esfera chegar
    const veu = clamp(t / 0.25) * (1 - clamp((t - fases.efeitoEm - 0.05) / 0.3));
    nos.push(<i key="veu" className="rj-veu" style={{ opacity: veu, '--rj': esfera.cor } as CSSProperties} />);
    const estilo = (x: number, y: number, d: number, extra: CSSProperties = {}) => ({ left: x, top: y, width: d, height: d, '--esf': esfera.cor, '--esf-miolo': esfera.miolo, ...extra } as CSSProperties);
    if (t < fases.soltaEm) {
      if (k < 0) continue;
      // a energia de todos os lados, cada vez mais forte, correndo para a esfera
      if (!reduced) {
        const R = Math.max(box.w, box.h) * 0.65, n = 10 + k * 4;
        for (let j = 0; j < n; j++) {
          const periodo = 0.7 - k * 0.08, p = ((t + (j / n) * periodo) % periodo) / periodo, a = (j * 137.5 * Math.PI) / 180;
          const r = R * (1 - p) ** 1.6 + diametro * 0.45;
          nos.push(<i key={`fio-${j}`} className="esf-fio" style={estilo(segura.x + Math.cos(a) * r, segura.y + Math.sin(a) * r, M * (0.06 + 0.03 * (j % 3)), { opacity: clamp(p * 3) * (1 - clamp((p - 0.85) / 0.15)) })} />);
        }
      }
      // o clarão e o anel de cada estágio novo
      const desde = t - inicios[k]!;
      if (desde < 0.4) nos.push(<i key={`anel-${k}`} className="esf-anel" style={estilo(segura.x, segura.y, diametro * (1.1 + desde * 3.2), { opacity: 1 - desde / 0.4 })} />);
      nos.push(<i key="aura" className="esf-aura" style={estilo(segura.x, segura.y, diametro * 1.9, { opacity: 0.55 + 0.1 * k })} />);
      nos.push(<i key="esfera" className={`esf-bola${reduced ? '' : ' esf-viva'}`} style={estilo(segura.x, segura.y, diametro)} />);
      // os quatro estágios, acesos um por um, embaixo da esfera
      nos.push(<span key="marcas" className="esf-marcas" style={{ left: segura.x, top: segura.y + frente * (diametro * 0.5 + M * 0.22), '--esf': esfera.cor } as CSSProperties}>{S.map((_, i) => <b key={i} className={i <= k ? 'on' : ''} />)}</span>);
      // o fio de energia que liga quem ativou à esfera
      nos.push(<i key="liga" className="esf-liga" style={{ left: de.x, top: Math.min(de.y, segura.y), height: Math.abs(segura.y - de.y), width: M * 0.18, '--esf': esfera.cor } as CSSProperties} />);
      continue;
    }
    // lançada: sai pesada e acelera até o alvo, com rastro, crescendo um pouco
    const p = clamp((t - fases.soltaEm) / Math.max(0.1, fases.efeitoEm - fases.soltaEm)), ease = p * p * (0.3 + 0.7 * p);
    if (p >= 1) {
      const depois = t - fases.efeitoEm;
      nos.push(<i key="clarao" className="esf-clarao" style={{ opacity: 1 - clamp(depois / 0.3), '--esf': esfera.cor } as CSSProperties} />);
      continue;
    }
    const D = M * S.at(-1)! * (1 + 0.12 * p), curva = -M * 0.6 * Math.sin(Math.PI * p);
    const vx = para.x - segura.x, vy = para.y - segura.y, dist = Math.hypot(vx, vy) || 1;
    const ponto = (q: number) => { const eq = q * q * (0.3 + 0.7 * q), c = -M * 0.6 * Math.sin(Math.PI * q); return { x: segura.x + vx * eq - (vy / dist) * c * frente, y: segura.y + vy * eq + (vx / dist) * c * frente }; };
    if (!reduced) for (let r = 1; r <= 4; r++) { const q = ponto(clamp(p - r * 0.07)); nos.push(<i key={`rastro-${r}`} className="esf-bola esf-rastro" style={estilo(q.x, q.y, D * (1 - r * 0.12), { opacity: 0.4 - r * 0.08 })} />); }
    const aqui = { x: segura.x + vx * ease - (vy / dist) * curva * frente, y: segura.y + vy * ease + (vx / dist) * curva * frente };
    if (p < 0.2) nos.push(<i key="solta" className="esf-anel" style={estilo(segura.x, segura.y, D * (1.2 + p * 5), { opacity: 1 - p * 5 })} />);
    nos.push(<i key="aura" className="esf-aura" style={estilo(aqui.x, aqui.y, D * 1.8, { opacity: 0.8 })} />);
    nos.push(<i key="esfera" className={`esf-bola${reduced ? '' : ' esf-viva'}`} style={estilo(aqui.x, aqui.y, D)} />);
  }
  if (!nos.length) return null;
  return <div className="esfera-que-cresce" aria-hidden="true">{nos}</div>;
}
