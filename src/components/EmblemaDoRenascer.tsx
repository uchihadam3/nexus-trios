import { Flame } from 'lucide-react';
import type { ReactNode } from 'react';

/*
 * O ícone da bolinha de quem está renascendo (pedido do jogador: "faz todo o
 * ícone da bola… tem a ver com o personagem que vai renascer"). Desenhos
 * simples em SVG, na cor da bolinha (currentColor), com um miolo mais claro.
 */
const DESENHOS: Record<string, ReactNode> = {
  // a Ave Fênix de asas erguidas
  ikki: <><path d="M12 4c1 1.6 1 3 .4 4.4 2.6-2.3 5.8-3.4 9.6-3.2-2.2 1.2-3.6 2.8-4.4 4.8 1.4-.3 2.6-.1 3.6.4-2.6.6-4.6 2-5.8 4l1.6 5.6-3-2.6L12 20l-2-2.6-3 2.6 1.6-5.6c-1.2-2-3.2-3.4-5.8-4 1-.5 2.2-.7 3.6-.4C5.6 8 4.2 6.4 2 5.2c3.8-.2 7 .9 9.6 3.2C11 7 11 5.6 12 4z"/><circle cx="12" cy="9.4" r="1.1" className="miolo"/></>,
  // o emblema da Força Fênix: a ave de asas abertas na horizontal
  jeangrey: <><path d="M12 3.5l1.6 4.2C16.4 6 19.6 5.4 23 6c-2.4 1-4.4 2.4-5.8 4.4l3.6-.4c-2 1.4-4.2 2.4-6.4 2.8L12 21l-2.4-8.2C7.4 12.4 5.2 11.4 3.2 10l3.6.4C5.4 8.4 3.4 7 1 6c3.4-.6 6.6 0 9.4 1.7z"/><circle cx="12" cy="9.6" r="1.3" className="miolo"/></>,
  // a máscara do Deadpool: o rosto, a faixa do meio e os dois olhos
  deadpool: <><circle cx="12" cy="12" r="9.5"/><path d="M11 2.6h2v18.8h-2z" className="miolo" opacity=".35"/><path d="M4.4 9.6c1.8-.6 3.8-.4 5.4.8-1 1.8-2.8 2.6-4.8 2.2-.6-.9-.8-1.9-.6-3z" className="miolo"/><path d="M19.6 9.6c-1.8-.6-3.8-.4-5.4.8 1 1.8 2.8 2.6 4.8 2.2.6-.9.8-1.9.6-3z" className="miolo"/></>,
  // o M do Majin na testa
  majinbuu: <><path d="M3 20V4.5h3.6L12 12l5.4-7.5H21V20h-3.6v-9.2L12 18l-5.4-7.2V20z"/></>,
  // o sarcófago em pé, com os braços cruzados
  mummra: <><path d="M12 1.8l4.6 2 1.4 5.4-1.6 12.2L12 22.4l-4.4-1L6 9.2l1.4-5.4z"/><circle cx="12" cy="7" r="1.6" className="miolo"/><path d="M8.6 12.4l6.8 2.2M15.4 12.4l-6.8 2.2" stroke="currentColor" strokeWidth="1.3" className="traco"/></>,
  // uma célula: a membrana, o citoplasma e o núcleo
  cell: <><circle cx="12" cy="12" r="9.5" opacity=".55"/><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" strokeWidth="1.6"/><circle cx="13.2" cy="11" r="3.6" className="miolo"/><circle cx="7.4" cy="14.6" r="1.1" className="miolo" opacity=".7"/><circle cx="16.6" cy="16.6" r=".9" className="miolo" opacity=".7"/></>,
  // o cogumelo de uma vida
  mario: <><path d="M2.4 12.6C2.4 6.8 6.6 3 12 3s9.6 3.8 9.6 9.6z"/><path d="M6.6 12.6h10.8l-.8 6.4c-.2 1.2-1.2 2-2.4 2H9.8c-1.2 0-2.2-.8-2.4-2z" opacity=".75"/><circle cx="12" cy="6.6" r="2.3" className="miolo"/><circle cx="5.8" cy="10" r="1.6" className="miolo"/><circle cx="18.2" cy="10" r="1.6" className="miolo"/><rect x="9.6" y="14.4" width="1.3" height="3" rx=".6" className="miolo"/><rect x="13.1" y="14.4" width="1.3" height="3" rx=".6" className="miolo"/></>,
  // as três garras
  wolverine: <><path d="M5.4 21L4.6 6.2 6.8 1.8l1.6 4.4L8.8 21zM10.4 21l-.6-16.6L12 0l2.2 4.4-.6 16.6zM15.2 21l.4-14.8 1.6-4.4 2.2 4.4-.8 14.8z"/><path d="M6.8 3.6v14M12 2v16M17.2 3.6v14" stroke="currentColor" strokeWidth=".7" className="traco"/></>,
  // o morcego
  alucardcv: <><path d="M12 7.2l1-2 .6 2.4c1.4.4 2.4 1.4 2.8 2.8 1.8-1.8 4.4-2.6 7.6-2.2-1.4 1.2-2 2.8-1.8 4.6-1.2-.6-2.4-.6-3.4 0 .2 1.4-.2 2.6-1 3.6-.8-.8-1.8-1.2-3-1L12 19l-2.8-3.6c-1.2-.2-2.2.2-3 1-.8-1-1.2-2.2-1-3.6-1-.6-2.2-.6-3.4 0 .2-1.8-.4-3.4-1.8-4.6 3.2-.4 5.8.4 7.6 2.2.4-1.4 1.4-2.4 2.8-2.8L11 5.2z"/><circle cx="10.8" cy="10" r=".7" className="miolo"/><circle cx="13.2" cy="10" r=".7" className="miolo"/></>,
  // o olho de demônio com a pupila vertical
  muzan: <><path d="M1.4 12C4.4 6.8 8 4.6 12 4.6s7.6 2.2 10.6 7.4C19.6 17.2 16 19.4 12 19.4S4.4 17.2 1.4 12z"/><ellipse cx="12" cy="12" rx="4.6" ry="4.6" className="miolo"/><ellipse cx="12" cy="12" rx="1.1" ry="4.2"/></>,
  // o Rinnegan: os anéis concêntricos
  pain: <><circle cx="12" cy="12" r="10" opacity=".5"/><g fill="none" stroke="currentColor" strokeWidth="1.4" className="traco"><circle cx="12" cy="12" r="9.2"/><circle cx="12" cy="12" r="6.6"/><circle cx="12" cy="12" r="4"/></g><circle cx="12" cy="12" r="1.7" className="miolo"/></>,
};

export function EmblemaDoRenascer({ id, size = 24 }: { id: string; size?: number }) {
  const d = DESENHOS[id];
  if (!d) return <Flame size={size} />;
  return <svg className="emblema-renascer" width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{d}</svg>;
}
