import { useEffect, useRef, useState } from 'react';
import { Check, Crown, Swords, X } from 'lucide-react';
import { Avatar } from './AvatarDaComunidade';
import { diferencaDoRelogio, textoDoErroPvp, type ServicoPvp, type VistaPvp } from '../lib/pvp-online';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import '../presentation/pvp.css';

/*
 * O aviso do PvP em qualquer tela: "Fulano te desafiou!" (aceitar abre a partida) e, para quem desafiou, "Fulano
 * aceitou!" quando a pessoa aceita com você fora da Arena. Chega pelo Realtime (pvp_partidas) e é conferido no
 * servidor ao abrir o jogo e ao voltar para ele.
 */
type Aviso = { tipo: 'convite' | 'aceitou'; v: VistaPvp; offset: number };

export function ConviteDoPvp({ servico, euId, naPartida, onAbrir }: { servico: ServicoPvp; euId: string; naPartida: string | null; onAbrir: (id: string) => void }) {
  const [aviso, setAviso] = useState<Aviso | null>(null);
  const [erro, setErro] = useState('');
  const [ocupado, setOcupado] = useState(false);
  const [agora, setAgora] = useState(() => Date.now());
  const naPartidaRef = useRef(naPartida); naPartidaRef.current = naPartida;
  const ja = useRef(new Set<string>());

  useEffect(() => {
    let vivo = true;
    const confere = async (id?: string) => {
      try {
        const r = await servico.consultar(id);
        const v = r.partida;
        if (!vivo || !v || v.id === naPartidaRef.current) return;
        const chave = `${v.id}-${v.fase}`;
        if (ja.current.has(chave)) return;
        if (v.fase === 'convite' && !v.desafiante) { ja.current.add(chave); setAviso({ tipo: 'convite', v, offset: diferencaDoRelogio(v.agora) }); battleAudio.sound('ui-arena', PRIORIDADE.interface); }
        else if (v.fase === 'montando' && v.desafiante && id) { ja.current.add(chave); setAviso({ tipo: 'aceitou', v, offset: diferencaDoRelogio(v.agora) }); battleAudio.sound('pronto', PRIORIDADE.interface); }
      } catch { /* sem rede: o próximo aviso tenta de novo */ }
    };
    void confere();
    const para = servico.ouvir((l) => {
      if (l.desafiado === euId && l.fase === 'convite') void confere(l.id);
      else if (l.desafiante === euId && l.fase === 'montando') void confere(l.id);
      else setAviso((a) => (a && a.v.id === l.id && l.fase !== 'convite' && a.tipo === 'convite' ? null : a));
    });
    const volta = () => { if (!document.hidden) void confere(); };
    document.addEventListener('visibilitychange', volta);
    return () => { vivo = false; para(); document.removeEventListener('visibilitychange', volta); };
  }, [servico, euId]);

  useEffect(() => { if (!aviso) return; const t = window.setInterval(() => setAgora(Date.now()), 500); return () => clearInterval(t); }, [aviso]);
  useEffect(() => { if (aviso && aviso.v.id === naPartida) setAviso(null); }, [aviso, naPartida]);
  const falta = aviso ? Math.max(0, Math.ceil((Date.parse(aviso.v.prazo) - (agora + aviso.offset)) / 1000)) : 0;
  useEffect(() => { if (aviso && falta <= 0) setAviso(null); }, [aviso, falta]);
  if (!aviso) return null;
  const { v } = aviso;

  const responder = async (aceitar: boolean) => {
    setOcupado(true); setErro('');
    try {
      await servico.responder(v.id, aceitar);
      setAviso(null);
      if (aceitar) onAbrir(v.id);
    } catch (e) { setErro(textoDoErroPvp(e)); } finally { setOcupado(false); }
  };

  return <div className="pv-aviso" role="alertdialog" aria-label={aviso.tipo === 'convite' ? `${v.rival.nome} te desafiou` : `${v.rival.nome} aceitou`}>
    <div className="pv-aviso-cartao">
      <span className="pv-aviso-raio" aria-hidden="true" />
      <span className="pv-aviso-avatar"><Avatar id={v.rival.id} nome={v.rival.nome} tamanho={70} online /><i><Swords size={16} /></i></span>
      <small>DESAFIO PvP</small>
      <h2>{aviso.tipo === 'convite' ? <>{v.rival.nome} te desafiou!</> : <>{v.rival.nome} aceitou!</>}</h2>
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {v.rival.vitorias}V {v.rival.derrotas}D</span>
      <p>{aviso.tipo === 'convite' ? '3 times de 3, escolha secreta. Vale rating.' : 'Monte seus 3 times antes do tempo acabar.'} <b>{Math.floor(falta / 60)}:{String(falta % 60).padStart(2, '0')}</b></p>
      {erro && <small className="pv-problema">{erro}</small>}
      {aviso.tipo === 'convite'
        ? <span className="pv-convite-botoes"><button className="secondary" disabled={ocupado} onClick={() => void responder(false)}><X size={18} />Recusar</button><button className="primary" disabled={ocupado} onClick={() => void responder(true)}><Swords size={18} />Aceitar</button></span>
        : <span className="pv-convite-botoes"><button className="secondary" onClick={() => setAviso(null)}>Depois</button><button className="primary" onClick={() => { setAviso(null); onAbrir(v.id); }}><Check size={18} />Ir para a partida</button></span>}
    </div>
  </div>;
}
