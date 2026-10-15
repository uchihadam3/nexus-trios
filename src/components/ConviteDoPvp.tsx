import { useEffect, useRef, useState } from 'react';
import { Check, Crown, RotateCcw, Swords, X } from 'lucide-react';
import { Avatar } from './AvatarDaComunidade';
import { diferencaDoRelogio, textoDoErroPvp, type ServicoPvp, type VistaPvp } from '../lib/pvp-online';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import '../presentation/pvp.css';

/*
 * O aviso do PvP em qualquer tela: "Fulano te desafiou!" (aceitar abre a partida) e, para quem desafiou, "Fulano
 * aceitou!" quando a pessoa aceita com você fora da Arena. Chega pelo Realtime (pvp_partidas) e é conferido no
 * servidor ao abrir o jogo e ao voltar para ele. Quem caiu no meio de uma partida (app fechado, atualizou, sem internet)
 * vê "Retornar" ao voltar: tem 45 s, senão perde (supabase/functions/ranked-api/pvp.ts · presenca).
 */
type Aviso = { tipo: 'convite' | 'aceitou' | 'voltar'; v: VistaPvp; offset: number; desde: number };

export function ConviteDoPvp({ servico, euId, naPartida, onAbrir }: { servico: ServicoPvp; euId: string; naPartida: string | null; onAbrir: (id: string) => void }) {
  const [aviso, setAviso] = useState<Aviso | null>(null);
  const [erro, setErro] = useState('');
  const [ocupado, setOcupado] = useState(false);
  const [agora, setAgora] = useState(() => Date.now());
  const naPartidaRef = useRef(naPartida); naPartidaRef.current = naPartida;
  const ja = useRef(new Set<string>()), emAndamento = useRef(false);

  useEffect(() => {
    let vivo = true;
    const confere = async (id?: string, silencioso = false) => {
      try {
        const r = await servico.consultar(id);
        const v = r.partida;
        if (!vivo || !v || v.id === naPartidaRef.current) return;
        const chave = `${v.id}-${v.fase}`;
        const visto = ja.current.has(chave), desde = Date.now(), offset = diferencaDoRelogio(v.agora);
        emAndamento.current = v.fase === 'jogando' || v.fase === 'montando';
        if (visto && v.fase !== 'jogando' && v.fase !== 'montando') return;
        if (!visto && v.fase === 'convite' && !v.desafiante) { ja.current.add(chave); setAviso({ tipo: 'convite', v, offset, desde }); battleAudio.sound('ui-arena', PRIORIDADE.interface); }
        else if (!visto && v.fase === 'montando' && v.desafiante && id) { ja.current.add(chave); setAviso({ tipo: 'aceitou', v, offset, desde }); battleAudio.sound('pronto', PRIORIDADE.interface); }
        // caiu de uma partida em andamento (abriu o jogo de novo, ou voltou do segundo plano): Retornar
        else if (!id && !silencioso && (v.fase === 'jogando' || v.fase === 'montando')) { setAviso({ tipo: 'voltar', v, offset, desde }); battleAudio.sound('ui-arena', PRIORIDADE.interface); }
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
    // com uma partida em andamento e o jogador em outra tela do jogo, segue avisando o servidor que está aqui
    const segue = window.setInterval(() => { if (emAndamento.current && !document.hidden && !naPartidaRef.current) void confere(undefined, true); }, 15000);
    return () => { vivo = false; para(); clearInterval(segue); document.removeEventListener('visibilitychange', volta); };
  }, [servico, euId]);

  useEffect(() => { if (!aviso) return; const t = window.setInterval(() => setAgora(Date.now()), 500); return () => clearInterval(t); }, [aviso]);
  useEffect(() => { if (aviso && aviso.v.id === naPartida) setAviso(null); }, [aviso, naPartida]);
  const falta = !aviso ? 0 : aviso.tipo === 'voltar' ? Math.max(0, Math.ceil(aviso.v.ausenciaMaxima - (agora - aviso.desde) / 1000)) : Math.max(0, Math.ceil((Date.parse(aviso.v.prazo) - (agora + aviso.offset)) / 1000));
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
      <small>{aviso.tipo === 'voltar' ? 'PARTIDA EM ANDAMENTO' : 'DESAFIO PvP'}</small>
      <h2>{aviso.tipo === 'convite' ? <>{v.rival.nome} te desafiou!</> : aviso.tipo === 'voltar' ? <>Volte para a partida!</> : <>{v.rival.nome} aceitou!</>}</h2>
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {v.rival.vitorias}V {v.rival.derrotas}D</span>
      <p>{aviso.tipo === 'voltar' ? `Contra ${v.rival.nome}. Se não voltar a tempo, a vitória vai para ${v.rival.nome}:` : aviso.tipo === 'convite' ? '3 times de 3, escolha secreta. Vale rating.' : 'Monte seus 3 times antes do tempo acabar.'} <b>{Math.floor(falta / 60)}:{String(falta % 60).padStart(2, '0')}</b></p>
      {erro && <small className="pv-problema">{erro}</small>}
      {aviso.tipo === 'convite'
        ? <span className="pv-convite-botoes"><button className="secondary" disabled={ocupado} onClick={() => void responder(false)}><X size={18} />Recusar</button><button className="primary" disabled={ocupado} onClick={() => void responder(true)}><Swords size={18} />Aceitar</button></span>
        : aviso.tipo === 'voltar'
          ? <button className="primary pv-retornar" onClick={() => { setAviso(null); onAbrir(v.id); }}><RotateCcw size={20} />RETORNAR</button>
          : <span className="pv-convite-botoes"><button className="secondary" onClick={() => setAviso(null)}>Depois</button><button className="primary" onClick={() => { setAviso(null); onAbrir(v.id); }}><Check size={18} />Ir para a partida</button></span>}
    </div>
  </div>;
}
