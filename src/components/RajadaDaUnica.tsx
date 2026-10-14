import type { CSSProperties, ReactNode } from 'react';
import type { Battle } from '../engine/types';
import { PRESENTATION as P } from '../presentation/config';
import { duracaoBase, type Beat } from '../presentation/director';
import { ABRE_O_LEQUE, rajadaDaChave, type FormaDaRajada } from '../presentation/rajada-da-unica';
import { fallbackPoint, type Anchors } from './BattleEffects';

/*
 * A rajada na tela (src/presentation/rajada-da-unica.ts): a Mecânica única de vários golpes (com o tempo parado) e a
 * habilidade de vários golpes (src/engine/golpes.ts).
 *   1. os projéteis aparecem (em leque na frente de quem solta, quando a rajada pede);
 *   2. saem um por um, cada um no seu alvo, com rastro e uma curva leve (os golpes de perto estouram direto no alvo);
 *   3. cada um que chega estoura no alvo; o número, o tremor e o som saem no mesmo instante, pelo diretor.
 * Tudo é calculado a cada quadro a partir do tempo do beat: pausar, acelerar ou voltar mantém a cena certa.
 */
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const suave = (x: number) => x * x * (3 - 2 * x);

/** O desenho de cada projétil, apontando para a direita (o sentido do voo). */
function Projetil({ forma, cor }: { forma: FormaDaRajada; cor: string }): ReactNode {
  switch (forma) {
    case 'petala': return <svg viewBox="0 0 44 22"><defs><linearGradient id="rj-pet" x1="0" x2="1"><stop offset="0" stopColor="#fff" /><stop offset=".45" stopColor="#ffc2da" /><stop offset="1" stopColor={cor} /></linearGradient></defs><path d="M2 11 C10 2 27 0 38 6 L34.5 11 L38 16 C27 22 10 20 2 11 Z" fill="url(#rj-pet)" /><path d="M5 11 C14 8 26 8 35 11" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" opacity=".85" fill="none" /></svg>;
    case 'bala': return <svg viewBox="0 0 44 12"><rect x="0" y="4" width="44" height="4" rx="2" fill={cor} /><rect x="28" y="3" width="16" height="6" rx="3" fill="#fff" /></svg>;
    case 'garra': return <svg viewBox="0 0 40 40">{[-9, 0, 9].map((d) => <path key={d} d={`M${8 + d / 3} ${6 + d} Q 30 ${20 + d} ${12 + d / 3} ${34 + d / 2}`} stroke={cor} strokeWidth="3.4" strokeLinecap="round" fill="none" />)}</svg>;
    case 'punho': return <svg viewBox="0 0 40 40"><path d="M20 2 L24 14 L37 11 L28 21 L37 31 L24 27 L20 38 L16 27 L3 31 L12 21 L3 11 L16 14 Z" fill={cor} stroke="#fff" strokeWidth="1.6" /><text x="20" y="25" textAnchor="middle" fontSize="13" fontWeight="900" fill="#fff">!</text></svg>;
    case 'faca': return <svg viewBox="0 0 44 14"><rect x="0" y="5" width="11" height="4" rx="1.5" fill="#5a4a3a" /><rect x="10" y="3" width="2.5" height="8" fill="#ccc" /><path d="M12.5 4 L40 7 L12.5 10 Z" fill={cor} /><path d="M13 7 L38 7" stroke="#fff" strokeWidth=".8" /></svg>;
    case 'agulha': return <svg viewBox="0 0 44 8"><path d="M0 4 L44 4" stroke={cor} strokeWidth="2.4" strokeLinecap="round" /><path d="M24 4 L44 4" stroke="#fff" strokeWidth="1" /></svg>;
    case 'carta': return <svg viewBox="0 0 30 40"><rect x="2" y="2" width="26" height="36" rx="4" fill="#fff" stroke={cor} strokeWidth="2.4" /><path d="M15 11 L21 20 L15 29 L9 20 Z" fill={cor} /></svg>;
    case 'energia': return <svg viewBox="0 0 44 20"><defs><radialGradient id={`rj-en-${cor.slice(1)}`}><stop offset="0" stopColor="#fff" /><stop offset=".5" stopColor={cor} /><stop offset="1" stopColor={cor} stopOpacity="0" /></radialGradient></defs><ellipse cx="28" cy="10" rx="16" ry="10" fill={`url(#rj-en-${cor.slice(1)})`} /><path d="M0 10 L28 10" stroke={cor} strokeWidth="3" strokeLinecap="round" opacity=".6" /></svg>;
    case 'fogo': return <svg viewBox="0 0 44 22"><path d="M2 11 C12 2 22 4 32 3 C42 6 42 16 32 19 C22 18 12 20 2 11 Z" fill={cor} opacity=".85" /><circle cx="33" cy="11" r="7" fill="#ffe08a" /><circle cx="34" cy="11" r="3.5" fill="#fff" /></svg>;
    case 'meteoro': return <svg viewBox="0 0 48 24"><path d="M0 12 L30 4 L30 20 Z" fill={cor} opacity=".55" /><circle cx="34" cy="12" r="10" fill={cor} /><circle cx="35" cy="12" r="5.5" fill="#fff" /></svg>;
    case 'flecha': return <svg viewBox="0 0 48 14"><path d="M4 7 L40 7" stroke="#e8d8b0" strokeWidth="2" /><path d="M36 2.5 L47 7 L36 11.5 Z" fill={cor} /><path d="M2 2 L9 7 L2 12 M6 2 L13 7 L6 12" stroke={cor} strokeWidth="1.6" fill="none" /></svg>;
    case 'missil': return <svg viewBox="0 0 48 18"><path d="M0 9 L10 4 L10 14 Z" fill="#ffd27a" /><rect x="10" y="5" width="26" height="8" rx="2" fill="#d8dde6" /><path d="M36 5 L46 9 L36 13 Z" fill={cor} /><path d="M12 5 L16 1 L19 5 M12 13 L16 17 L19 13" fill="#9aa4b2" /></svg>;
    case 'espada': return <svg viewBox="0 0 56 16"><rect x="0" y="6" width="10" height="4" rx="1.5" fill="#6a5a8a" /><rect x="10" y="2" width="3" height="12" rx="1" fill="#ffd27a" /><path d="M13 5 L54 8 L13 11 Z" fill={cor} /><path d="M14 8 L50 8" stroke="#fff" strokeWidth="1" /></svg>;
    case 'osso': return <svg viewBox="0 0 44 16"><rect x="6" y="6" width="32" height="4" fill="#fff" /><circle cx="6" cy="5" r="4" fill="#fff" /><circle cx="6" cy="11" r="4" fill="#fff" /><circle cx="38" cy="5" r="4" fill="#fff" /><circle cx="38" cy="11" r="4" fill="#fff" /></svg>;
    case 'bolha': return <svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="12" fill={cor} fillOpacity=".25" stroke={cor} strokeWidth="2" /><circle cx="11" cy="10" r="3.5" fill="#fff" opacity=".9" /></svg>;
    case 'cristal': return <svg viewBox="0 0 44 18"><path d="M2 9 L18 2 L42 9 L18 16 Z" fill={cor} /><path d="M18 2 L22 9 L18 16 M2 9 L42 9" stroke="#fff" strokeWidth="1" opacity=".8" fill="none" /></svg>;
    case 'lamina': return <svg viewBox="0 0 40 40"><path d="M10 4 C34 10 34 30 10 36 C24 28 24 12 10 4 Z" fill={cor} /><path d="M12 7 C28 13 28 27 12 33" stroke="#fff" strokeWidth="1.2" fill="none" /></svg>;
    case 'raio': return <svg viewBox="0 0 48 20"><path d="M0 10 L12 4 L18 13 L28 5 L34 14 L48 10" stroke={cor} strokeWidth="3.2" strokeLinejoin="round" fill="none" /><path d="M0 10 L12 4 L18 13 L28 5 L34 14 L48 10" stroke="#fff" strokeWidth="1.2" strokeLinejoin="round" fill="none" /></svg>;
    default: return null;
  }
}

type Props = { battle: Battle; beat: Beat | null; anchors: Anchors; box: { w: number; h: number; medal: number }; reduced: boolean };
export function RajadaDaUnica(props: Props) {
  const { beat, box } = props;
  if (!beat?.passos || !box.w) return null;
  // cada rajada do beat desenha a sua (a habilidade de vários golpes e, logo depois, a Mecânica única)
  const chaves = [...new Set(beat.passos.filter((x) => x.rajada).map((x) => x.rajada!.chave))];
  if (!chaves.length) return null;
  return <div className="rajada-da-unica" aria-hidden="true">{chaves.map((c) => <UmaRajada key={c} {...props} beat={beat} chave={c} />)}</div>;
}
function UmaRajada({ battle, beat, anchors, box, reduced, chave }: Props & { beat: Beat; chave: string }) {
  const golpes = beat.passos!.filter((x) => x.rajada?.chave === chave);
  if (!golpes.length) return null;
  const r = rajadaDaChave(chave);
  const dono = battle.fighters.find((f) => f.uid === golpes[0]!.quem);
  if (!dono || !r) return null;
  // o tempo do beat contado a partir do impacto (o mesmo relógio dos passos)
  const depois = beat.elapsed - duracaoBase(beat) * P.impactAt;
  const px = (uid: string) => { const a = anchors[uid] ?? fallbackPoint(uid); return { x: (a.x / 100) * box.w, y: (a.y / 100) * box.h }; };
  const de = px(dono.uid), frente = dono.side === 'player' ? -1 : 1, M = box.medal, perto = r.forma === 'golpe';
  const primeiro = golpes[0]!.em - r.voo, ultimo = golpes.at(-1)!.em;
  // nunca antes do nome (pedido do jogador: "carrega, aparece o nome, aparece as pétalas e usa"): o nome da
  // habilidade aparece no começo do beat, e o leque só abre depois dele (se o golpe é rápido, o leque abre mais rápido)
  const comeco = -duracaoBase(beat) * P.impactAt + 0.25;
  const abre = Math.min(primeiro - 0.12, Math.max(comeco, primeiro - (r.leque ? ABRE_O_LEQUE : 0.25))), abrindo = primeiro - abre;
  if (depois < abre - 0.3 || depois > ultimo + 0.6) return null;
  const nos: ReactNode[] = [];
  // o tempo parado (a Mecânica única): um véu na cor da rajada, que entra antes do leque e sai depois do último golpe
  if (r.para) {
    const veu = clamp((depois - (abre - 0.3)) / 0.3) * (1 - clamp((depois - ultimo - 0.25) / 0.35));
    nos.push(<i key="veu" className="rj-veu" style={{ opacity: veu, '--rj': r.cor } as CSSProperties} />);
  }
  const n = golpes.length, tam = M * (r.forma === 'petala' ? 0.34 : r.forma === 'espada' ? 0.5 : r.forma === 'bala' || r.forma === 'agulha' ? 0.42 : r.forma === 'carta' ? 0.3 : 0.4);
  const corte = /corte|lamina/.test(r.som);
  golpes.forEach((g, i) => {
    const ev = beat.events.find((e) => g.eventos.includes(e.id) && (e.kind === 'damage' || e.kind === 'block'));
    if (!ev?.target) return;
    // de perto, cada golpe cai num ponto um pouco diferente do alvo (a sequência de socos, de cortes)
    const solto = perto ? { x: Math.sin(i * 2.4) * M * 0.22, y: Math.cos(i * 1.7) * M * 0.2 } : { x: 0, y: 0 };
    const alvo0 = px(ev.target), alvo = { x: alvo0.x + solto.x, y: alvo0.y + solto.y }, sai = g.em - r.voo, chega = g.em;
    if (depois >= chega) {
      if (depois < chega + 0.45) nos.push(<i key={`acerto-${i}`} className={`rj-acerto rj-acerto-${perto ? (corte ? 'corte' : 'soco') : r.forma}`} style={{ left: alvo.x, top: alvo.y, width: M * (perto ? 0.7 : 0.95), height: M * (perto ? 0.7 : 0.95), '--rj': r.cor, '--giro': `${(i * 67) % 360}deg` } as CSSProperties} />);
      return;
    }
    if (perto) return;
    // o lugar no leque: um arco de 130° na frente de quem solta, longe do retrato, a ponta para fora (dentro da tela)
    const a = (frente < 0 ? -90 : 90) + (n > 1 ? -65 + (130 * i) / (n - 1) : 0), rad = (a * Math.PI) / 180;
    const slot = r.leque ? { x: Math.max(tam * 0.55, Math.min(box.w - tam * 0.55, de.x + Math.cos(rad) * M * 1.1)), y: de.y + Math.sin(rad) * M * 0.95 } : de;
    let x: number, y: number, ang: number, op = 1, escala = 1;
    if (depois < sai) {
      if (!r.leque) {
        // a bala espera na mira: o alvo marcado (Dead Eye) antes do tiro
        if (r.forma === 'bala' && r.para && depois > abre) nos.push(<i key={`mira-${i}`} className="rj-mira" style={{ left: alvo.x, top: alvo.y, width: M * 0.7, height: M * 0.7, '--rj': r.cor } as CSSProperties} />);
        return;
      }
      const surge = abre + (i * abrindo * 0.7) / n;
      if (depois < surge) return;
      const s = suave(clamp((depois - surge) / 0.18));
      x = de.x + (slot.x - de.x) * s; y = de.y + (slot.y - de.y) * s; ang = a; op = s; escala = 0.4 + 0.6 * s;
      // flutua no leque enquanto espera a vez
      y += Math.sin((depois + i) * 7) * 2;
    } else {
      const p = clamp((depois - sai) / Math.max(0.05, r.voo)), e = p * p * (0.4 + 0.6 * p);
      const curva = (r.forma === 'bala' || r.forma === 'raio' ? 0 : (i % 2 ? 1 : -1) * M * 0.35) * Math.sin(Math.PI * p);
      const vx = alvo.x - slot.x, vy = alvo.y - slot.y, d = Math.hypot(vx, vy) || 1;
      x = slot.x + vx * e - (vy / d) * curva; y = slot.y + vy * e + (vx / d) * curva;
      ang = (Math.atan2(vy, vx) * 180) / Math.PI;
      // rastro: três fantasmas atrás
      if (!reduced) for (let k = 1; k <= 3; k++) {
        const q = clamp(p - k * 0.06), eq = q * q * (0.4 + 0.6 * q), cq = (r.forma === 'bala' || r.forma === 'raio' ? 0 : (i % 2 ? 1 : -1) * M * 0.35) * Math.sin(Math.PI * q);
        nos.push(<span key={`rastro-${i}-${k}`} className={`rj-proj rj-${r.forma} rj-rastro`} style={{ left: slot.x + vx * eq - (vy / d) * cq, top: slot.y + vy * eq + (vx / d) * cq, width: tam, height: tam, opacity: 0.35 - k * 0.09, transform: `translate(-50%,-50%) rotate(${ang}deg)`, '--rj': r.cor } as CSSProperties}><Projetil forma={r.forma} cor={r.cor} /></span>);
      }
      // o clarão de quem soltou, no instante em que sai (o tiro, o arremesso)
      if (p < 0.25 && !r.leque) nos.push(<i key={`sai-${i}`} className="rj-clarao" style={{ left: de.x, top: de.y, width: M * 0.9, height: M * 0.9, '--rj': r.cor, opacity: 1 - p * 4 } as CSSProperties} />);
    }
    nos.push(<span key={`proj-${i}`} className={`rj-proj rj-${r.forma}`} style={{ left: x, top: y, width: tam, height: tam, opacity: op, transform: `translate(-50%,-50%) rotate(${ang}deg) scale(${escala})`, '--rj': r.cor } as CSSProperties}><Projetil forma={r.forma} cor={r.cor} /></span>);
  });
  return <>{nos}</>;
}
