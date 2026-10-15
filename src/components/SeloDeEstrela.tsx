import type { CSSProperties } from 'react';
import { ESTRELAS_DE_PONTOS } from '../data/estrelas-de-pontos';
import '../presentation/estrela-de-pontos.css';

/*
 * O selo das estrelas dos pontos (src/data/estrelas-de-pontos.ts): quantas estrelas o personagem tem e quanto ele
 * soma aos pontos do trio. Na carta da escolha fica pequeno, em cima do retrato; na ficha, com a explicação.
 */
const COR = { 3: '#ffd34d', 2: '#e3ecf5', 1: '#e7a36a' } as const;
const NOME = { 3: 'Lenda dos pontos', 2: 'Estrela dos pontos', 1: 'Destaque dos pontos' } as const;
const ATE = { 3: 'passa de 2 milhões', 2: 'chega a 1,5–2 milhões', 1: 'chega a 1–1,5 milhão' } as const;

export function SeloDeEstrela({ id, grande = false }: { id: string; grande?: boolean }) {
  const e = ESTRELAS_DE_PONTOS[id];
  if (!e) return null;
  const estilo = { '--epts': COR[e.estrelas] } as CSSProperties;
  if (!grande) return <span className={`epts-selo n${e.estrelas}`} style={estilo} title={`${NOME[e.estrelas]}: +${e.bonus}% nos pontos do trio`}><i>{'★'.repeat(e.estrelas)}</i><b>+{e.bonus}%</b></span>;
  return <div className={`epts-ficha n${e.estrelas}`} style={estilo}>
    <span className="epts-estrelas" aria-hidden="true">{'★'.repeat(e.estrelas)}</span>
    <span className="epts-texto"><b>{NOME[e.estrelas]} · +{e.bonus}% nos pontos</b><small>Com ele no trio, cada luta rende +{e.bonus}% de pontos e a jornada {ATE[e.estrelas]}. Com mais de uma estrela no trio, vale a maior.</small></span>
  </div>;
}
