import type { CSSProperties } from 'react';
import { ESTRELAS_DE_PONTOS } from '../data/estrelas-de-pontos';
import '../presentation/estrela-de-pontos.css';

/*
 * O selo das estrelas dos pontos (src/data/estrelas-de-pontos.ts): só as estrelas e quanto o personagem soma aos
 * pontos do trio (pedido do jogador: "só colocar lá as estrelinhas e falar a porcentagem"). Na carta da escolha fica
 * em cima do retrato; na ficha, logo abaixo do nome.
 */
const COR = { 3: '#ffd34d', 2: '#e3ecf5', 1: '#e7a36a' } as const;

export function SeloDeEstrela({ id, naFicha = false }: { id: string; naFicha?: boolean }) {
  const e = ESTRELAS_DE_PONTOS[id];
  if (!e) return null;
  return <span className={`epts-selo n${e.estrelas}${naFicha ? ' na-ficha' : ''}`} style={{ '--epts': COR[e.estrelas] } as CSSProperties}
    title={e.bonus ? `+${e.bonus}% nos pontos do trio` : undefined}>
    <i>{'★'.repeat(e.estrelas)}</i>{e.bonus > 0 && <b>+{e.bonus}%</b>}
  </span>;
}
