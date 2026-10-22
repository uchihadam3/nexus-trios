import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { Download, Globe, MoreVertical, Share, Smartphone, Swords, Trophy, Users, X } from 'lucide-react';
import { byId, characters } from '../data/characters';
import { Portrait } from './Portrait';
import '../presentation/compartilhar.css';
import { t } from '../i18n/idioma';

/*
 * Quem chega pelo convite (src/components/CompartilharJogo.tsx) vê esta tela primeiro: o convite de um amigo, o que é
 * o jogo em três linhas e as duas portas — instalar no celular ou jogar já no navegador.
 *
 * No Android (Chrome), "Instalar" abre o pedido de instalação do próprio celular. Onde o navegador não deixa o jogo
 * pedir (iPhone, ou o Chrome ainda não liberou), o botão mostra o passo a passo do aparelho.
 */
const ehIphone = () => typeof navigator !== 'undefined' && /iphone|ipad|ipod/i.test(navigator.userAgent);

export function BoasVindasDoConvite({ podeInstalar, onInstalar, onClose }: { podeInstalar: boolean; onInstalar: () => Promise<boolean>; onClose: () => void }) {
  const ref = useRef<HTMLDialogElement>(null);
  const [passos, setPassos] = useState(false);
  useEffect(() => { const el = ref.current; el?.showModal(); return () => el?.close(); }, []);
  const instalar = async () => {
    if (podeInstalar && await onInstalar()) { onClose(); return; }
    setPassos(true);
  };
  const trio = ['goku', 'naruto', 'luffy'];

  return <dialog className="info-dialog gs-aviso cvt-sheet cvt-boas-vindas" ref={ref} onCancel={onClose} style={{ '--tela': '#c8f560' } as CSSProperties}>
    <button className="icon-button modal-close" onClick={onClose} aria-label={t('Fechar')}><X size={20} /></button>
    <div className="cvt-cartao" aria-hidden="true">
      <span className="cvt-raios" />
      <div className="cvt-trio">{trio.map((id, i) => byId[id] && <span key={id} style={{ '--character': byId[id].color, '--i': i } as CSSProperties}><Portrait character={byId[id]} /></span>)}</div>
      <b className="cvt-logo"><Swords size={16} />NEXUS</b>
      <small>{t('DUELO DE TRIOS')}</small>
    </div>
    <span className="cvt-selo">{t('CONVITE DE UM AMIGO')}</span>
    <h2>{t('Seu amigo te chamou para a luta!')}</h2>
    <ul className="cvt-pontos">
      <li><Users size={16} /><span>{t('{n} personagens de animes, filmes, games e desenhos', { n: characters.length })}</span></li>
      <li><Swords size={16} /><span>{t('Monte seu trio e encare 10 lutas seguidas')}</span></li>
      <li><Trophy size={16} /><span>{t('Faça pontos e suba no ranking')}</span></li>
    </ul>
    {!passos ? <>
      <button className="primary cvt-instalar" onClick={() => void instalar()}><Download size={20} /><span><b>{t('Instalar no celular')}</b><small>{t('abre como app, até sem internet')}</small></span></button>
      <button className="secondary cvt-navegador" onClick={onClose}><Globe size={18} />{t('Jogar no navegador')}</button>
    </> : <>
      <div className="cvt-passos">
        <b><Smartphone size={16} />{t('Para instalar:')}</b>
        {ehIphone()
          ? <p><Share size={14} /> {t('Toque em Compartilhar embaixo da tela e depois em “Adicionar à Tela de Início”.')}</p>
          : <p><MoreVertical size={14} /> {t('Toque no menu do navegador e depois em “Instalar app” (ou “Adicionar à tela inicial”).')}</p>}
        <p>{t('O NEXUS aparece na tela do celular como um app.')}</p>
      </div>
      <button className="primary cvt-navegador" onClick={onClose}><Globe size={18} />{t('Jogar agora no navegador')}</button>
    </>}
  </dialog>;
}
