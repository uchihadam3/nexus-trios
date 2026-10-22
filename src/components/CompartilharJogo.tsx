import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { Check, Copy, Facebook, Instagram, Mail, MessageCircle, Send, Share2, Swords, X } from 'lucide-react';
import { byId, characters } from '../data/characters';
import { Portrait } from './Portrait';
import '../presentation/compartilhar.css';
import { t } from '../i18n/idioma';

/*
 * Chamar amigos (pedido do jogador: "um botão… compartilhar mandando pelo WhatsApp, pelo Facebook, Instagram,
 * e-mail. Aí a pessoa clica e pergunta se ela quer instalar").
 *
 * O convite é o endereço do jogo com ?convite=1: quem abre cai na tela de boas-vindas
 * (src/components/BoasVindasDoConvite.tsx), que oferece instalar no celular ou jogar no navegador.
 *
 * Cada botão abre o app certo com a mensagem pronta. O Instagram não aceita mensagem por link, então ele usa o
 * compartilhar do próprio celular (que mostra o Instagram na lista) ou, sem ele, copia o convite para colar lá.
 */

/** O endereço do convite: o próprio jogo, de onde ele estiver publicado, com a marca do convite. */
export function linkDoConvite(): string {
  const url = new URL(location.href);
  url.search = '';
  url.hash = '';
  url.searchParams.set('convite', '1');
  return url.toString();
}

const mensagem = () => t('Bora jogar NEXUS — Duelo de Trios? Monte seu trio com {n} personagens (Goku, Naruto, Batman, Luffy…) e veja até onde chega nas 10 lutas. Toca no link e instala no celular:', { n: characters.length });

type Destino = { id: string; nome: string; cor: string; icone: ReactNode; abre: (link: string) => void | Promise<void> };

const abrir = (url: string) => { window.open(url, '_blank', 'noopener'); };

export function CompartilharJogo({ onClose, trio }: { onClose: () => void; trio: string[] }) {
  const ref = useRef<HTMLDialogElement>(null);
  const [aviso, setAviso] = useState<string | null>(null);
  useEffect(() => { const el = ref.current; el?.showModal(); return () => el?.close(); }, []);
  useEffect(() => { if (!aviso) return; const id = window.setTimeout(() => setAviso(null), 2600); return () => clearTimeout(id); }, [aviso]);

  const link = linkDoConvite(), MENSAGEM = mensagem();
  const texto = `${MENSAGEM} ${link}`;
  const copiar = async (msg: string) => {
    try { await navigator.clipboard.writeText(texto); setAviso(msg); } catch { setAviso(t('Não deu para copiar. Segure o link abaixo para copiar.')); }
  };
  const compartilharDoCelular = async () => {
    if (navigator.share) {
      try { await navigator.share({ title: t('NEXUS — Duelo de Trios'), text: MENSAGEM, url: link }); } catch { /* fechou sem escolher */ }
      return true;
    }
    return false;
  };

  const destinos: Destino[] = [
    { id: 'whatsapp', nome: 'WhatsApp', cor: '#25d366', icone: <MessageCircle size={26} />, abre: () => abrir(`https://wa.me/?text=${encodeURIComponent(texto)}`) },
    { id: 'facebook', nome: 'Facebook', cor: '#1877f2', icone: <Facebook size={26} />, abre: (l) => abrir(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(l)}&quote=${encodeURIComponent(MENSAGEM)}`) },
    {
      id: 'instagram', nome: 'Instagram', cor: '#e1306c', icone: <Instagram size={26} />,
      abre: async () => { if (!(await compartilharDoCelular())) await copiar(t('Convite copiado! Cole no Direct do Instagram.')); },
    },
    { id: 'email', nome: t('E-mail'), cor: '#ffb84a', icone: <Mail size={26} />, abre: () => { location.href = `mailto:?subject=${encodeURIComponent(t('Bora jogar NEXUS — Duelo de Trios?'))}&body=${encodeURIComponent(texto)}`; } },
    { id: 'telegram', nome: 'Telegram', cor: '#2aabee', icone: <Send size={26} />, abre: (l) => abrir(`https://t.me/share/url?url=${encodeURIComponent(l)}&text=${encodeURIComponent(MENSAGEM)}`) },
    { id: 'copiar', nome: t('Copiar link'), cor: '#c8f560', icone: <Copy size={26} />, abre: () => copiar(t('Convite copiado! É só colar onde quiser.')) },
  ];

  return <dialog className="info-dialog gs-aviso cvt-sheet" ref={ref} onCancel={onClose} style={{ '--tela': '#c8f560' } as CSSProperties}>
    <button className="icon-button modal-close" onClick={onClose} aria-label={t('Fechar')}><X size={20} /></button>
    <div className="cvt-cartao" aria-hidden="true">
      <span className="cvt-raios" />
      <div className="cvt-trio">{trio.slice(0, 3).map((id, i) => byId[id] && <span key={id} style={{ '--character': byId[id].color, '--i': i } as CSSProperties}><Portrait character={byId[id]} /></span>)}</div>
      <b className="cvt-logo"><Swords size={16} />NEXUS</b>
      <small>{t('DUELO DE TRIOS')}</small>
    </div>
    <h2>{t('Chame seus amigos')}</h2>
    <p>{t('Mande o convite. Quem tocar no link pode instalar no celular ou jogar direto no navegador.')}</p>
    <div className="cvt-grade">
      {destinos.map((d, i) => <button key={d.id} className={`cvt-destino cvt-${d.id}`} style={{ '--cor': d.cor, '--i': i } as CSSProperties} onClick={() => void d.abre(link)}>
        <span className="cvt-icone">{d.icone}</span><b>{d.nome}</b>
      </button>)}
    </div>
    {typeof navigator !== 'undefined' && 'share' in navigator && <button className="primary cvt-mais" onClick={() => void compartilharDoCelular()}><Share2 size={18} />{t('Outros apps do celular')}</button>}
    <button className="cvt-link" onClick={() => void copiar(t('Convite copiado! É só colar onde quiser.'))} aria-label={t('Copiar o link do convite')}><span>{link}</span>{aviso ? <Check size={16} /> : <Copy size={16} />}</button>
    {aviso && <p className="cvt-aviso" role="status"><Check size={15} />{aviso}</p>}
  </dialog>;
}
