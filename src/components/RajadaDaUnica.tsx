import type { CSSProperties, ReactNode } from 'react';
import type { Battle } from '../engine/types';
import { PRESENTATION as P } from '../presentation/config';
import { duracaoBase, type Beat } from '../presentation/director';
import { ABRE_O_LEQUE, RAJADA_DA_UNICA, type FormaDaRajada, type Rajada } from '../presentation/rajada-da-unica';
import { fallbackPoint, type Anchors } from './BattleEffects';

/*
 * A rajada da Mecânica única na tela (src/presentation/rajada-da-unica.ts). Com o tempo parado:
 *   1. os projéteis aparecem (no Byakuya, as 10 pétalas abrem um leque na frente dele, uma de cada vez);
 *   2. saem um por um, cada um no seu rival, com rastro e uma curva leve;
 *   3. cada um que chega estoura no alvo (o número, o tremor e o som saem no mesmo instante, pelo diretor).
 * Tudo é calculado a cada quadro a partir do tempo do beat, então pausar, acelerar ou voltar mantém a cena certa.
 */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const suave = (x: number) => x * x * (3 - 2 * x);

function Projetil({ forma, cor }: { forma: FormaDaRajada; cor: string }): ReactNode {
  if (forma === 'petala') return <svg viewBox="0 0 44 22" aria-hidden="true">
    <defs><linearGradient id="rj-petala" x1="0" x2="1"><stop offset="0" stopColor="#fff" /><stop offset=".45" stopColor="#ffc2da" /><stop offset="1" stopColor="#e8508c" /></linearGradient></defs>
    <path d="M2 11 C10 2 27 0 38 6 L34.5 11 L38 16 C27 22 10 20 2 11 Z" fill="url(#rj-petala)" />
    <path d="M5 11 C14 8 26 8 35 11" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" opacity=".85" fill="none" />
  </svg>;
  if (forma === 'bala') return <svg viewBox="0 0 44 12" aria-hidden="true"><rect x="0" y="4" width="44" height="4" rx="2" fill={cor} /><rect x="28" y="3" width="16" height="6" rx="3" fill="#fff" /></svg>;
  if (forma === 'garra') return <svg viewBox="0 0 40 40" aria-hidden="true">{[-9, 0, 9].map((d) => <path key={d} d={`M${8 + d / 3} ${6 + d} Q 30 ${20 + d} ${12 + d / 3} ${34 + d / 2}`} stroke={cor} strokeWidth="3.4" strokeLinecap="round" fill="none" />)}</svg>;
  return <svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2 L24 14 L37 11 L28 21 L37 31 L24 27 L20 38 L16 27 L3 31 L12 21 L3 11 L16 14 Z" fill={cor} stroke="#fff" strokeWidth="1.6" /><text x="20" y="25" textAnchor="middle" fontSize="13" fontWeight="900" fill="#fff">!</text></svg>;
}

export function RajadaDaUnica({ battle, beat, anchors, box, reduced }: { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; reduced: boolean }) {
  if (!beat?.passos || !box.w) return null;
  const golpes = beat.passos.filter((x) => x.rajada);
  if (golpes.length < 2) return null;
  const dono = battle.fighters.find((f) => f.uid === golpes[0]!.quem);
  const r: Rajada | undefined = dono ? RAJADA_DA_UNICA[dono.characterId] : undefined;
  if (!dono || !r) return null;
  // o tempo do beat contado a partir do impacto (o mesmo relógio dos passos)
  const depois = beat.elapsed - duracaoBase(beat) * P.impactAt;
  const px = (uid: string) => { const a = anchors[uid] ?? fallbackPoint(uid); return { x: (a.x / 100) * box.w, y: (a.y / 100) * box.h }; };
  const de = px(dono.uid), frente = dono.side === 'player' ? -1 : 1, M = box.medal;
  const primeiro = golpes[0]!.em - r.voo, ultimo = golpes.at(-1)!.em;
  const abre = primeiro - (r.leque ? ABRE_O_LEQUE : 0.25);
  if (depois < abre - 0.3 || depois > ultimo + 0.6) return null;
  const nos: ReactNode[] = [];
  // o tempo parado: um véu na cor da rajada, que entra antes do leque e sai depois do último golpe
  const veu = clamp((depois - (abre - 0.3)) / 0.3) * (1 - clamp((depois - ultimo - 0.25) / 0.35));
  nos.push(<i key="veu" className="rj-veu" style={{ opacity: veu, '--rj': r.cor } as CSSProperties} />);
  const n = golpes.length, tam = M * (r.forma === 'petala' ? 0.34 : r.forma === 'bala' ? 0.42 : 0.4);
  golpes.forEach((g, i) => {
    const ev = beat.events.find((e) => g.eventos.includes(e.id) && (e.kind === 'damage' || e.kind === 'block'));
    if (!ev?.target) return;
    const alvo = px(ev.target), sai = g.em - r.voo, chega = g.em;
    // o lugar no leque: um arco de 130° na frente de quem ativou, longe do retrato, a ponta da pétala para fora (as da
    // ponta ficam dentro da tela)
    const a = (frente < 0 ? -90 : 90) + (n > 1 ? -65 + (130 * i) / (n - 1) : 0), rad = (a * Math.PI) / 180;
    const slot = r.leque ? { x: Math.max(tam * 0.55, Math.min(box.w - tam * 0.55, de.x + Math.cos(rad) * M * 1.1)), y: de.y + Math.sin(rad) * M * 0.95 } : de;
    let x: number, y: number, ang: number, op = 1, escala = 1;
    if (depois < sai) {
      if (!r.leque) {
        // a bala espera na mira: o alvo marcado (Dead Eye) antes do tiro
        if (r.forma === 'bala' && depois > abre) nos.push(<i key={`mira-${i}`} className="rj-mira" style={{ left: alvo.x, top: alvo.y, width: M * 0.7, height: M * 0.7, '--rj': r.cor } as CSSProperties} />);
        return;
      }
      const surge = abre + (i * ABRE_O_LEQUE * 0.7) / n;
      if (depois < surge) return;
      const s = suave(clamp((depois - surge) / 0.18));
      x = de.x + (slot.x - de.x) * s; y = de.y + (slot.y - de.y) * s; ang = a; op = s; escala = 0.4 + 0.6 * s;
      // flutua no leque enquanto espera a vez
      y += Math.sin((depois + i) * 7) * 2;
    } else if (depois < chega) {
      const p = clamp((depois - sai) / r.voo), e = p * p * (0.4 + 0.6 * p);
      const curva = (i % 2 ? 1 : -1) * M * 0.35 * Math.sin(Math.PI * p);
      const vx = alvo.x - slot.x, vy = alvo.y - slot.y, d = Math.hypot(vx, vy) || 1;
      x = slot.x + vx * e - (vy / d) * curva; y = slot.y + vy * e + (vx / d) * curva;
      ang = (Math.atan2(vy, vx) * 180) / Math.PI;
      // rastro: três fantasmas atrás
      if (!reduced) for (let k = 1; k <= 3; k++) {
        const q = clamp(p - k * 0.06), eq = q * q * (0.4 + 0.6 * q), cq = (i % 2 ? 1 : -1) * M * 0.35 * Math.sin(Math.PI * q);
        nos.push(<span key={`rastro-${i}-${k}`} className={`rj-proj rj-${r.forma} rj-rastro`} style={{ left: slot.x + vx * eq - (vy / d) * cq, top: slot.y + vy * eq + (vx / d) * cq, width: tam, height: tam, opacity: 0.35 - k * 0.09, transform: `translate(-50%,-50%) rotate(${ang}deg)` } as CSSProperties}><Projetil forma={r.forma} cor={r.cor} /></span>);
      }
      // o clarão de quem soltou, no instante em que sai (o tiro, o salto)
      if (p < 0.25 && r.forma !== 'petala') nos.push(<i key={`sai-${i}`} className="rj-clarao" style={{ left: de.x, top: de.y, width: M * 0.9, height: M * 0.9, '--rj': r.cor, opacity: 1 - p * 4 } as CSSProperties} />);
    } else {
      // chegou: o estouro no alvo
      if (depois < chega + 0.45) nos.push(<i key={`acerto-${i}`} className={`rj-acerto rj-acerto-${r.forma}`} style={{ left: alvo.x, top: alvo.y, width: M * 0.95, height: M * 0.95, '--rj': r.cor, '--giro': `${(i * 67) % 360}deg` } as CSSProperties} />);
      return;
    }
    nos.push(<span key={`proj-${i}`} className={`rj-proj rj-${r.forma}`} style={{ left: x, top: y, width: tam, height: tam, opacity: op, transform: `translate(-50%,-50%) rotate(${ang}deg) scale(${escala})`, '--rj': r.cor } as CSSProperties}><Projetil forma={r.forma} cor={r.cor} /></span>);
  });
  return <div className="rajada-da-unica" aria-hidden="true">{nos}</div>;
}
