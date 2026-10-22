import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import { Swords, Trophy, X } from 'lucide-react';
import { ESTRELAS_DE_PONTOS } from '../data/estrelas-de-pontos';
import { byId } from '../data/characters';
import '../presentation/estrela-de-pontos.css';
import { nomeDe, t } from '../i18n/idioma';

/*
 * O selo das estrelas dos pontos (src/data/estrelas-de-pontos.ts): só as estrelas e quanto o personagem soma aos
 * pontos do trio (pedido do jogador: "só colocar lá as estrelinhas e falar a porcentagem"). Na carta da escolha fica
 * em cima do retrato; na ficha, logo abaixo do nome; na ficha da batalha, ao lado do universo.
 * Tocar no selo abre um cartão curto dizendo o que a porcentagem é: bônus nos PONTOS, não no dano, e que não muda
 * quem ganha ou perde a luta.
 */
const COR = { 3: '#ffd34d', 2: '#e3ecf5', 1: '#e7a36a' } as const;

function CartaoDaEstrela({ id, onClose }: { id: string; onClose: () => void }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => { const d = ref.current; d?.showModal(); return () => d?.close(); }, []);
  const e = ESTRELAS_DE_PONTOS[id]!, nome = byId[id] ? nomeDe(byId[id]) : '';
  return <dialog ref={ref} className="id-card-dialog epts-dialog" aria-label={t('Estrelas de pontos')}
    onCancel={ev => { ev.preventDefault(); ev.stopPropagation(); onClose(); }}
    onClick={ev => { ev.stopPropagation(); if (ev.target === ev.currentTarget) onClose(); }}>
    <div className={`id-card epts-card n${e.estrelas}`} style={{ '--id-cor': COR[e.estrelas], '--epts': COR[e.estrelas] } as CSSProperties}>
      <button className="icon-button id-card-close" aria-label={t('Fechar')} onClick={onClose}><X size={18} /></button>
      <div className="epts-topo">
        <span className="epts-estrelas" aria-hidden="true">{Array.from({ length: e.estrelas }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties}>★</i>)}</span>
        <span className="id-card-family">{t('Estrelas de pontos')} · {nome}</span>
        <strong className="epts-numero">{e.bonus > 0 ? `+${e.bonus}%` : `${e.estrelas}★`}<small>{e.bonus > 0 ? t('nos PONTOS') : ''}</small></strong>
      </div>
      <ul className="epts-regras">
        <li className="sim"><Trophy size={18} /><span><b>{t('É bônus de pontos.')}</b> {t('No fim da luta, os pontos do trio ganham {bonus}.', { bonus: e.bonus > 0 ? `+${e.bonus}%` : t('o bônus') })}</span></li>
        <li className="nao"><Swords size={18} /><span><b>{t('Não é dano.')}</b> {t('Não muda a força e não muda quem ganha ou perde a luta.')}</span></li>
      </ul>
      <p className="epts-nota">{t('No trio vale um bônus só: o de mais estrelas; empatou, o de maior porcentagem.')}</p>
      <button className="primary id-card-ok" onClick={onClose}>{t('Entendi')}</button>
    </div>
  </dialog>;
}

export function SeloDeEstrela({ id, naFicha = false, inline = false }: { id: string; naFicha?: boolean; inline?: boolean }) {
  const [aberto, setAberto] = useState(false);
  const e = ESTRELAS_DE_PONTOS[id];
  if (!e) return null;
  return <>
    <button type="button" className={`epts-selo n${e.estrelas}${naFicha ? ' na-ficha' : ''}${inline ? ' inline' : ''}`}
      style={{ '--epts': COR[e.estrelas] } as CSSProperties}
      aria-label={`${t(e.estrelas > 1 ? '{n} estrelas' : '{n} estrela', { n: e.estrelas })}${e.bonus ? `, ${t('+{n}% nos pontos', { n: e.bonus })}` : ''}. ${t('O que é?')}`}
      onClick={ev => { ev.stopPropagation(); setAberto(true); }}>
      <i>{'★'.repeat(e.estrelas)}</i>{e.bonus > 0 && <b>+{e.bonus}%</b>}<em aria-hidden="true">PTS</em>
    </button>
    {aberto && createPortal(<CartaoDaEstrela id={id} onClose={() => setAberto(false)} />, document.body)}
  </>;
}
