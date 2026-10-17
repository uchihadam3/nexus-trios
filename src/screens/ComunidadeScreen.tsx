import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { ArrowLeft, Award, CalendarDays, Check, CheckCheck, ChevronDown, Clock3, Crown, Flag, Globe, Lock, MessageCircle, MessagesSquare, Reply, Search, SendHorizontal, Smile, Swords, Trophy, Users, X } from 'lucide-react';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { formatarPontos } from '../engine/pontos';
import { tituloDe } from '../lib/conquistas';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { EMOJIS_DAS_REACOES, LIMITE_DA_MENSAGEM, corDoNome, haQuanto, hora, quando, rotuloDoDia, statusDe, textoDoErro,
  type Conversa, type Jogador, type Mensagem, type Reacao, type ServicoDaComunidade } from '../lib/comunidade';
import { Avatar } from '../components/AvatarDaComunidade';
import '../presentation/comunidade.css';

/*
 * A Comunidade (pedido do jogador: "ver todas as pessoas que estão online… chat global… tipo um chat de WhatsApp, até
 * melhor… clicar no nome da pessoa e mandar mensagem privada… mesmo offline… marca quando ele viu, igual o WhatsApp").
 *
 * Três abas: o chat Global, as Privadas (com ✓ enviada e ✓✓ azul quando o outro viu) e os Jogadores (online/offline,
 * desde quando, quando saiu). Tocar num nome ou numa foto abre o cartão do jogador, com o recorde, o trio, o título
 * das Conquistas e o botão de mandar mensagem. O PvP vai entrar nesse mesmo cartão ("Desafiar").
 */

type Aba = 'global' | 'privadas' | 'jogadores';
interface Props {
  servico: ServicoDaComunidade;
  euId: string;
  euNome: string;
  /** Quantas privadas não lidas (o selo da aba); a tela avisa quando lê. */
  naoLidas: number;
  onLidas: () => void;
  /** Abrir já numa conversa (vindo do aviso de mensagem nova). */
  abrirCom?: string | null;
  onDetails: (id: string) => void;
  /** Desafiar no PvP (devolve o erro em texto, ou null quando a partida abriu). */
  onDesafiar?: (id: string) => Promise<string | null>;
}

const som = (nome: 'toque' | 'pronto') => battleAudio.sound(nome, PRIORIDADE.interface);

/** "Agora" que anda sozinho, para o "há 5 min" não ficar parado. */
function useAgora(ms = 30_000) {
  const [agora, setAgora] = useState(() => Date.now());
  useEffect(() => { const t = setInterval(() => setAgora(Date.now()), ms); return () => clearInterval(t); }, [ms]);
  return agora;
}

/* ---------------------------------------------------------------------------
 * Peças pequenas
 * ------------------------------------------------------------------------- */

/** 👑 para os 3 maiores recordes da comunidade. */
function Coroa({ lugar }: { lugar?: number }) {
  if (!lugar || lugar > 3) return null;
  return <span className={`cm-coroa l${lugar}`} title={`${lugar}º maior recorde da comunidade`}><Crown size={12} /></span>;
}

function Titulo({ conquistas }: { conquistas: number }) {
  const t = tituloDe(conquistas).atual;
  return <span className="cm-titulo" style={{ '--titulo': t.cor } as CSSProperties}>{t.nome}</span>;
}

/* ---------------------------------------------------------------------------
 * O cartão do jogador
 * ------------------------------------------------------------------------- */

function CartaoDoJogador({ jogador, lugar, agora, onMensagem, onDetails, onClose, onDesafiar }: { jogador: Jogador; lugar?: number; agora: number; onMensagem: () => void; onDetails: (id: string) => void; onClose: () => void; onDesafiar?: (id: string) => Promise<string | null> }) {
  const [desafiando, setDesafiando] = useState(false);
  const [erroDoDesafio, setErroDoDesafio] = useState('');
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => { const d = ref.current; d?.showModal(); return () => d?.close(); }, []);
  const st = statusDe(jogador, agora), t = tituloDe(jogador.conquistas).atual;
  return <dialog ref={ref} className="cm-cartao-dialog" aria-label={jogador.nome} onCancel={(e) => { e.preventDefault(); onClose(); }} onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
    <div className="cm-cartao" style={{ '--cor': corDoNome(jogador.id), '--titulo': t.cor } as CSSProperties}>
      <button className="icon-button cm-fechar" aria-label="Fechar" onClick={onClose}><X size={18} /></button>
      <div className="cm-cartao-topo">
        <Avatar jogador={jogador} id={jogador.id} nome={jogador.nome} tamanho={92} />
        <h2>{jogador.nome}<Coroa lugar={lugar} /></h2>
        <Titulo conquistas={jogador.conquistas} />
        <p className={`cm-cartao-status ${jogador.online ? 'online' : ''}`}><span className="cm-ponto" />{st.longo}{jogador.online && jogador.onlineDesde ? ` · ${haQuanto(jogador.onlineDesde, agora)}` : jogador.vistoEm ? ` · ${haQuanto(jogador.vistoEm, agora)}` : ''}</p>
      </div>
      <div className="cm-numeros">
        <span><Trophy size={16} /><b>{jogador.recorde ? formatarPontos(jogador.recorde) : '—'}</b><small>recorde</small></span>
        <span><Flag size={16} /><b>{jogador.jornadas.toLocaleString('pt-BR')}</b><small>{jogador.jornadas === 1 ? 'jornada' : 'jornadas'}</small></span>
        <span><Award size={16} /><b>{jogador.conquistas}</b><small>personagens</small></span>
        <span><CalendarDays size={16} /><b>{haQuanto(jogador.desde, agora).replace('há ', '')}</b><small>de conta</small></span>
      </div>
      {jogador.trio && <div className="cm-cartao-trio">
        <small>TRIO DO RECORDE</small>
        <div>{jogador.trio.map((id) => byId[id] && <button key={id} onClick={() => onDetails(id)} style={{ '--character': byId[id].color } as CSSProperties} aria-label={`Ficha de ${byId[id].name}`}>
          <Portrait character={byId[id]} /><b>{byId[id].name}</b></button>)}</div>
      </div>}
      <div className="cm-cartao-acoes">
        <button className="primary" onClick={onMensagem}><MessageCircle size={18} />Mandar mensagem</button>
        {onDesafiar
          ? <button className="secondary cm-desafiar" disabled={desafiando} onClick={() => { setDesafiando(true); setErroDoDesafio(''); void onDesafiar(jogador.id).then((e) => { if (e) { setErroDoDesafio(e); setDesafiando(false); } }); }}><Swords size={18} />{desafiando ? 'Desafiando…' : 'Desafiar no PvP'}</button>
          : <button className="secondary cm-em-breve" disabled><Swords size={18} />Desafiar<em><Lock size={11} />PvP com conta</em></button>}
      </div>
      {erroDoDesafio && <p className="cm-erro-desafio">{erroDoDesafio}</p>}
    </div>
  </dialog>;
}

/* ---------------------------------------------------------------------------
 * O chat (global ou privada)
 * ------------------------------------------------------------------------- */

const EMOJIS_RAPIDOS = ['😀', '😂', '🔥', '👏', '😎', '🙏', '💀', '❤️', '👊', '🎉', '🤝', '😭'];
type Local = Mensagem & { pendente?: boolean };

function Chat({ servico, euId, com, porId, lugarDe, agora, onPerfil, onLidas }: {
  servico: ServicoDaComunidade; euId: string; com: string | null; porId: Map<string, Jogador>; lugarDe: Map<string, number>; agora: number;
  onPerfil: (id: string) => void; onLidas: () => void;
}) {
  const [mensagens, setMensagens] = useState<Local[]>([]);
  const [reacoes, setReacoes] = useState<Reacao[]>([]);
  const [temMais, setTemMais] = useState(false);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const [texto, setTexto] = useState('');
  const [respondendo, setRespondendo] = useState<Mensagem | null>(null);
  const [menuDe, setMenuDe] = useState<number | null>(null);
  const [emojis, setEmojis] = useState(false);
  const [digitando, setDigitando] = useState<Record<string, number>>({});
  const [novasAbaixo, setNovasAbaixo] = useState(0);
  const [piscando, setPiscando] = useState<number | null>(null);
  const lista = useRef<HTMLDivElement>(null), caixa = useRef<HTMLDivElement>(null), campo = useRef<HTMLTextAreaElement>(null);
  const noFundo = useRef(true), ultimoAviso = useRef(0);
  const nomeDe = (id: string) => id === euId ? 'Você' : porId.get(id)?.nome ?? 'Jogador';

  // a altura do chat: do topo dele até o fim da tela, para a caixa de escrever ficar sempre embaixo
  useLayoutEffect(() => {
    const ajusta = () => { const el = caixa.current; if (el) el.style.height = `${Math.max(320, window.innerHeight - el.getBoundingClientRect().top - 10)}px`; };
    ajusta(); addEventListener('resize', ajusta); return () => removeEventListener('resize', ajusta);
  }, []);

  const rolarProFim = useCallback((suave = false) => {
    const el = lista.current; if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior: suave ? 'smooth' : 'auto' });
    setNovasAbaixo(0);
  }, []);

  // quem chama passa uma função nova a cada desenho: guardada numa ref, ela não reinicia a conversa (e não entra em laço)
  const onLidasRef = useRef(onLidas);
  useEffect(() => { onLidasRef.current = onLidas; });
  const marcar = useCallback(() => {
    if (com && document.visibilityState === 'visible') void servico.marcarVistas(com).then(() => onLidasRef.current()).catch(() => undefined);
  }, [com, servico]);

  useEffect(() => {
    let vivo = true;
    setCarregando(true); setErro('');
    servico.historico(com).then((h) => {
      if (!vivo) return;
      setMensagens(h.mensagens); setReacoes(h.reacoes); setTemMais(h.temMais); setCarregando(false);
      requestAnimationFrame(() => rolarProFim());
      marcar();
    }).catch((e: unknown) => { if (vivo) { setErro(textoDoErro(e)); setCarregando(false); } });
    const parar = servico.ouvir({
      mensagem: (m, tipo) => {
        const daqui = com === null ? m.paraId === null : (m.autorId === euId && m.paraId === com) || (m.autorId === com && m.paraId === euId);
        if (!daqui) return;
        setMensagens((ms) => {
          if (tipo === 'mudou' || ms.some((x) => x.id === m.id)) return ms.map((x) => x.id === m.id ? { ...m } : x);
          return [...ms, m];
        });
        if (tipo === 'nova' && m.autorId !== euId) {
          setDigitando((d) => { const n = { ...d }; delete n[m.autorId]; return n; });
          som('toque');
          if (noFundo.current) requestAnimationFrame(() => rolarProFim(true)); else setNovasAbaixo((n) => n + 1);
          marcar();
        }
      },
      reacao: (r) => setReacoes((rs) => [...rs.filter((x) => !(x.mensagemId === r.mensagemId && x.playerId === r.playerId)), ...(r.emoji ? [r] : [])]),
      digitando: (quem, onde) => { if (onde === com && quem !== euId) setDigitando((d) => ({ ...d, [quem]: Date.now() })); },
    });
    const volta = () => { if (document.visibilityState === 'visible') marcar(); };
    document.addEventListener('visibilitychange', volta);
    return () => { vivo = false; parar(); document.removeEventListener('visibilitychange', volta); };
  }, [servico, com, euId, marcar, rolarProFim]);

  // "digitando…" some sozinho 4 s depois do último aviso
  useEffect(() => {
    if (!Object.keys(digitando).length) return;
    const t = setTimeout(() => setDigitando((d) => Object.fromEntries(Object.entries(d).filter(([, quando]) => Date.now() - quando < 4000))), 1000);
    return () => clearTimeout(t);
  }, [digitando]);

  useEffect(() => { if (!erro) return; const t = setTimeout(() => setErro(''), 4500); return () => clearTimeout(t); }, [erro]);

  const maisAntigas = async () => {
    const el = lista.current, antes = el?.scrollHeight ?? 0;
    try {
      const h = await servico.historico(com, mensagens[0]?.id);
      setMensagens((ms) => [...h.mensagens, ...ms]); setReacoes((rs) => [...h.reacoes, ...rs]); setTemMais(h.temMais);
      requestAnimationFrame(() => { if (el) el.scrollTop = el.scrollHeight - antes; });
    } catch (e) { setErro(textoDoErro(e)); }
  };

  const enviar = async () => {
    const t = texto.trim();
    if (!t) return;
    if (t.length > LIMITE_DA_MENSAGEM) { setErro(textoDoErro(new Error('500'))); return; }
    const provisoria: Local = { id: -Date.now(), autorId: euId, paraId: com, texto: t, respostaA: respondendo?.id ?? null, criadaEm: new Date().toISOString(), vistaEm: null, pendente: true };
    setMensagens((ms) => [...ms, provisoria]); setTexto(''); setRespondendo(null); setEmojis(false);
    requestAnimationFrame(() => rolarProFim(true));
    som('pronto');
    try {
      const m = await servico.enviar(t, com, provisoria.respostaA);
      setMensagens((ms) => ms.some((x) => x.id === m.id) ? ms.filter((x) => x.id !== provisoria.id) : ms.map((x) => x.id === provisoria.id ? m : x));
    } catch (e) {
      setMensagens((ms) => ms.filter((x) => x.id !== provisoria.id));
      setTexto(t); setErro(textoDoErro(e));
    }
    campo.current?.focus();
  };

  const aoDigitar = (v: string) => {
    setTexto(v);
    if (v.trim() && Date.now() - ultimoAviso.current > 2500) { ultimoAviso.current = Date.now(); servico.avisarDigitando(com); }
  };

  const reagir = (id: number, emoji: string) => {
    setMenuDe(null);
    const minha = reacoes.find((r) => r.mensagemId === id && r.playerId === euId);
    const nova = minha?.emoji === emoji ? null : emoji;
    setReacoes((rs) => [...rs.filter((r) => !(r.mensagemId === id && r.playerId === euId)), ...(nova ? [{ mensagemId: id, playerId: euId, emoji: nova }] : [])]);
    if (nova) som('toque');
    void servico.reagir(id, emoji).catch((e: unknown) => setErro(textoDoErro(e)));
  };

  const irPara = (id: number) => {
    const el = lista.current?.querySelector(`[data-msg="${id}"]`);
    if (!el) return;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setPiscando(id); setTimeout(() => setPiscando(null), 1400);
  };

  // auto-altura da caixa de texto (até ~5 linhas)
  useLayoutEffect(() => { const c = campo.current; if (!c) return; c.style.height = 'auto'; c.style.height = `${Math.min(c.scrollHeight, 128)}px`; }, [texto]);

  const quemDigita = Object.keys(digitando).map(nomeDe);
  const porMsg = useMemo(() => {
    const m = new Map<number, Map<string, string[]>>();
    for (const r of reacoes) {
      if (!r.emoji) continue;
      const g = m.get(r.mensagemId) ?? new Map<string, string[]>();
      g.set(r.emoji, [...(g.get(r.emoji) ?? []), r.playerId]); m.set(r.mensagemId, g);
    }
    return m;
  }, [reacoes]);
  const porIdMsg = useMemo(() => new Map(mensagens.map((m) => [m.id, m])), [mensagens]);

  const itens: ReactNode[] = [];
  let diaAnterior = '', autorAnterior = '', tempoAnterior = 0;
  for (const m of mensagens) {
    const dia = rotuloDoDia(m.criadaEm, agora), minha = m.autorId === euId, t = new Date(m.criadaEm).getTime();
    if (dia !== diaAnterior) { itens.push(<div key={`dia-${m.id}`} className="cm-dia"><span>{dia}</span></div>); autorAnterior = ''; }
    // mensagens seguidas da mesma pessoa (até 5 min) ficam agrupadas, sem repetir foto e nome
    const emGrupo = autorAnterior === m.autorId && t - tempoAnterior < 5 * 60_000;
    diaAnterior = dia; autorAnterior = m.autorId; tempoAnterior = t;
    const j = porId.get(m.autorId), citada = m.respostaA ? porIdMsg.get(m.respostaA) : undefined, grupos = porMsg.get(m.id);
    itens.push(<div key={m.id} data-msg={m.id} className={`cm-linha ${minha ? 'minha' : ''} ${emGrupo ? 'grupo' : ''} ${piscando === m.id ? 'pisca' : ''}`}>
      {!minha && com === null && (emGrupo ? <span className="cm-avatar-vazio" /> : <button className="cm-avatar-botao" onClick={() => onPerfil(m.autorId)} aria-label={`Perfil de ${nomeDe(m.autorId)}`}><Avatar jogador={j} id={m.autorId} nome={nomeDe(m.autorId)} tamanho={34} /></button>)}
      <div className="cm-bolha-coluna">
        <button className={`cm-bolha ${m.pendente ? 'pendente' : ''}`} onClick={() => { if (!m.pendente) setMenuDe(menuDe === m.id ? null : m.id); }} aria-label={`Mensagem de ${nomeDe(m.autorId)}: ${m.texto}`}>
          {!minha && com === null && !emGrupo && <span className="cm-autor" style={{ color: corDoNome(m.autorId) }} onClick={(e) => { e.stopPropagation(); onPerfil(m.autorId); }}>
            {nomeDe(m.autorId)}<Coroa lugar={lugarDe.get(m.autorId)} />{j && <Titulo conquistas={j.conquistas} />}</span>}
          {m.respostaA && <span className="cm-citacao" style={{ '--cor': citada ? corDoNome(citada.autorId) : '#9aa7b8' } as CSSProperties} onClick={(e) => { e.stopPropagation(); if (citada) irPara(citada.id); }}>
            <b>{citada ? nomeDe(citada.autorId) : 'Mensagem'}</b><span>{citada ? citada.texto : 'mensagem antiga'}</span></span>}
          <span className="cm-texto">{m.texto}</span>
          <span className="cm-hora">{hora(m.criadaEm)}
            {minha && com !== null && (m.pendente ? <Clock3 size={13} className="cm-tique" /> : m.vistaEm ? <CheckCheck size={15} className="cm-tique visto" aria-label={`Visto ${quando(m.vistaEm, agora)}`} /> : <Check size={15} className="cm-tique" aria-label="Enviada" />)}
            {minha && com === null && m.pendente && <Clock3 size={13} className="cm-tique" />}
          </span>
        </button>
        {grupos && <div className="cm-reacoes">{[...grupos.entries()].map(([e, quem]) => <button key={e} className={quem.includes(euId) ? 'minha' : ''} onClick={() => reagir(m.id, e)} title={quem.map(nomeDe).join(', ')}>
          <span>{e}</span>{quem.length > 1 && <b>{quem.length}</b>}</button>)}</div>}
        {menuDe === m.id && <div className="cm-menu" role="menu">
          <div className="cm-menu-emojis">{EMOJIS_DAS_REACOES.map((e) => <button key={e} onClick={() => reagir(m.id, e)} aria-label={`Reagir com ${e}`}>{e}</button>)}</div>
          <div className="cm-menu-acoes">
            <button onClick={() => { setRespondendo(m); setMenuDe(null); campo.current?.focus(); }}><Reply size={15} />Responder</button>
            {!minha && com === null && <button onClick={() => { setMenuDe(null); onPerfil(m.autorId); }}><MessageCircle size={15} />Perfil</button>}
            {minha && com !== null && m.vistaEm && <span className="cm-menu-visto"><CheckCheck size={14} />Visto {quando(m.vistaEm, agora)}</span>}
            {minha && com !== null && !m.vistaEm && <span className="cm-menu-visto"><Check size={14} />Enviada · ainda não vista</span>}
          </div>
        </div>}
      </div>
    </div>);
  }

  return <div className="cm-chat" ref={caixa}>
    <div className="cm-lista" ref={lista} onScroll={(e) => { const el = e.currentTarget; noFundo.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80; if (noFundo.current) setNovasAbaixo(0); }} onClick={(e) => { if (e.target === e.currentTarget) setMenuDe(null); }}>
      {temMais && <button className="cm-mais" onClick={() => void maisAntigas()}>Carregar mensagens antigas</button>}
      {carregando && <div className="cm-carregando"><span /><span /><span /></div>}
      {!carregando && !mensagens.length && <div className="cm-vazio">{com === null
        ? <><Globe size={34} /><b>O chat global está quietinho</b><small>Mande a primeira mensagem e puxe assunto!</small></>
        : <><MessageCircle size={34} /><b>Comece a conversa</b><small>{porId.get(com)?.online ? 'Está online agora.' : 'A mensagem fica guardada e aparece quando a pessoa entrar no jogo.'}</small></>}</div>}
      {itens}
    </div>
    {novasAbaixo > 0 && <button className="cm-novas" onClick={() => rolarProFim(true)}><ChevronDown size={16} />{novasAbaixo} {novasAbaixo === 1 ? 'nova' : 'novas'}</button>}
    <div className="cm-rodape">
      {quemDigita.length > 0 && <div className="cm-digitando"><span className="cm-pontinhos"><i /><i /><i /></span>{quemDigita.length === 1 ? `${quemDigita[0]} está digitando…` : `${quemDigita.length} pessoas digitando…`}</div>}
      {erro && <div className="cm-erro" role="alert">{erro}</div>}
      {respondendo && <div className="cm-respondendo" style={{ '--cor': corDoNome(respondendo.autorId) } as CSSProperties}>
        <Reply size={16} /><span><b>{nomeDe(respondendo.autorId)}</b><small>{respondendo.texto}</small></span>
        <button className="icon-button" aria-label="Cancelar resposta" onClick={() => setRespondendo(null)}><X size={16} /></button></div>}
      {emojis && <div className="cm-emojis">{EMOJIS_RAPIDOS.map((e) => <button key={e} onClick={() => { aoDigitar(texto + e); campo.current?.focus(); }}>{e}</button>)}</div>}
      <div className="cm-escrever">
        <button className={`icon-button cm-botao-emoji ${emojis ? 'ligado' : ''}`} aria-label="Emojis" onClick={() => setEmojis(!emojis)}><Smile size={22} /></button>
        <textarea ref={campo} rows={1} value={texto} maxLength={LIMITE_DA_MENSAGEM + 20} placeholder={com === null ? 'Mensagem para todos…' : `Mensagem para ${nomeDe(com)}…`}
          onChange={(e) => aoDigitar(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void enviar(); } }} aria-label="Escrever mensagem" />
        {texto.length > LIMITE_DA_MENSAGEM - 100 && <span className={`cm-contador ${texto.length > LIMITE_DA_MENSAGEM ? 'passou' : ''}`}>{LIMITE_DA_MENSAGEM - texto.length}</span>}
        <button className="cm-enviar" disabled={!texto.trim()} onClick={() => void enviar()} aria-label="Enviar"><SendHorizontal size={22} /></button>
      </div>
    </div>
  </div>;
}

/* ---------------------------------------------------------------------------
 * A tela
 * ------------------------------------------------------------------------- */

export function ComunidadeScreen({ servico, euId, euNome, naoLidas, onLidas, abrirCom, onDetails, onDesafiar }: Props) {
  const [aba, setAba] = useState<Aba>(abrirCom ? 'privadas' : 'global');
  const [conversa, setConversa] = useState<string | null>(abrirCom ?? null);
  const [jogadores, setJogadores] = useState<Jogador[]>([]);
  const [conversas, setConversas] = useState<Conversa[]>([]);
  const [filtro, setFiltro] = useState<'todos' | 'online' | 'offline'>('todos');
  const [busca, setBusca] = useState('');
  const [perfil, setPerfil] = useState<string | null>(null);
  const [erro, setErro] = useState('');
  const agora = useAgora();

  const carregarJogadores = useCallback(() => { servico.jogadores().then((j) => { setJogadores(j); setErro(''); }).catch((e: unknown) => setErro(textoDoErro(e))); }, [servico]);
  const carregarConversas = useCallback(() => { servico.conversas().then(setConversas).catch(() => undefined); }, [servico]);
  useEffect(() => { carregarJogadores(); const t = setInterval(carregarJogadores, 20_000); return () => clearInterval(t); }, [carregarJogadores]);
  useEffect(() => { carregarConversas(); }, [carregarConversas, naoLidas]);
  useEffect(() => servico.ouvir({ mensagem: (m) => { if (m.paraId !== null) carregarConversas(); } }), [servico, carregarConversas]);
  useEffect(() => { if (abrirCom) { setAba('privadas'); setConversa(abrirCom); } }, [abrirCom]);

  const porId = useMemo(() => {
    const m = new Map(jogadores.map((j) => [j.id, j]));
    if (!m.has(euId)) m.set(euId, { id: euId, nome: euNome, online: true, onlineDesde: null, vistoEm: null, recorde: null, trio: null, conquistas: 0, desde: new Date().toISOString(), jornadas: 0 });
    return m;
  }, [jogadores, euId, euNome]);
  const lugarDe = useMemo(() => new Map([...jogadores].filter((j) => j.recorde).sort((a, b) => b.recorde! - a.recorde!).slice(0, 3).map((j, i) => [j.id, i + 1])), [jogadores]);
  const outros = jogadores.filter((j) => j.id !== euId);
  const online = outros.filter((j) => j.online);
  const visiveis = outros
    .filter((j) => filtro === 'todos' || (filtro === 'online') === j.online)
    .filter((j) => !busca.trim() || j.nome.toLowerCase().includes(busca.trim().toLowerCase()))
    .sort((a, b) => Number(b.online) - Number(a.online) || (b.vistoEm ?? '').localeCompare(a.vistoEm ?? '') || a.nome.localeCompare(b.nome));

  const abrirConversa = (id: string) => { setPerfil(null); setAba('privadas'); setConversa(id); som('toque'); };
  const comQuem = conversa ? porId.get(conversa) : undefined;
  const nomeDaConversa = comQuem?.nome ?? conversas.find((c) => c.comId === conversa)?.comNome ?? 'Jogador';
  const jogadorDoPerfil = perfil ? porId.get(perfil) : undefined;

  return <section className="cm-tela">
    <header className="cm-topo">
      <span className="cm-logo"><MessagesSquare size={22} /></span>
      <div><h1>COMUNIDADE</h1><p><span className="cm-ponto vivo" /><b>{online.length + 1}</b> online<span className="cm-sep">·</span><b>{outros.length + 1}</b> jogadores</p></div>
      <div className="cm-pilha" aria-hidden="true">{online.slice(0, 3).map((j) => <Avatar key={j.id} jogador={j} id={j.id} nome={j.nome} tamanho={28} />)}</div>
    </header>

    {!conversa && <nav className="cm-abas" role="tablist">
      <button role="tab" aria-selected={aba === 'global'} className={aba === 'global' ? 'ativa' : ''} onClick={() => setAba('global')}><Globe size={17} />Global</button>
      <button role="tab" aria-selected={aba === 'privadas'} className={aba === 'privadas' ? 'ativa' : ''} onClick={() => setAba('privadas')}><MessageCircle size={17} />Privadas{naoLidas > 0 && <em>{naoLidas}</em>}</button>
      <button role="tab" aria-selected={aba === 'jogadores'} className={aba === 'jogadores' ? 'ativa' : ''} onClick={() => setAba('jogadores')}><Users size={17} />Jogadores<small>{online.length}</small></button>
    </nav>}
    {erro && <p className="cm-erro-geral" role="alert">{erro}</p>}

    {aba === 'global' && !conversa && <Chat key="global" servico={servico} euId={euId} com={null} porId={porId} lugarDe={lugarDe} agora={agora} onPerfil={(id) => { if (id !== euId) setPerfil(id); }} onLidas={onLidas} />}

    {aba === 'privadas' && conversa && <>
      <div className="cm-conversa-topo">
        <button className="icon-button" aria-label="Voltar para as conversas" onClick={() => { setConversa(null); carregarConversas(); }}><ArrowLeft size={20} /></button>
        <button className="cm-conversa-quem" onClick={() => setPerfil(conversa)}>
          <Avatar jogador={comQuem} id={conversa} nome={nomeDaConversa} tamanho={40} />
          <span><b>{nomeDaConversa}<Coroa lugar={lugarDe.get(conversa)} /></b><small className={comQuem?.online ? 'online' : ''}>{comQuem ? (comQuem.online ? 'online agora' : comQuem.vistoEm ? `visto por último ${quando(comQuem.vistoEm, agora)}` : 'ainda não apareceu') : ''}</small></span>
        </button>
      </div>
      <Chat key={conversa} servico={servico} euId={euId} com={conversa} porId={porId} lugarDe={lugarDe} agora={agora} onPerfil={(id) => { if (id !== euId) setPerfil(id); }} onLidas={() => { onLidas(); carregarConversas(); }} />
    </>}

    {aba === 'privadas' && !conversa && <div className="cm-conversas">
      {!conversas.length && <div className="cm-vazio"><MessageCircle size={34} /><b>Nenhuma conversa ainda</b><small>Toque em alguém na aba Jogadores ou no chat Global para mandar uma mensagem — mesmo que esteja offline.</small>
        <button className="primary" onClick={() => setAba('jogadores')}><Users size={16} />Ver jogadores</button></div>}
      {conversas.map((c, i) => {
        const j = porId.get(c.comId);
        return <button key={c.comId} className={`cm-conversa ${c.naoLidas ? 'nao-lida' : ''}`} style={{ '--i': i } as CSSProperties} onClick={() => abrirConversa(c.comId)}>
          <Avatar jogador={j} id={c.comId} nome={c.comNome} tamanho={50} />
          <span className="cm-conversa-meio"><b>{c.comNome}<Coroa lugar={lugarDe.get(c.comId)} /></b>
            <small>{c.ultimaMinha && (c.ultimaVista ? <CheckCheck size={15} className="cm-tique visto" /> : <Check size={15} className="cm-tique" />)}{c.ultimaTexto}</small></span>
          <span className="cm-conversa-fim"><small>{rotuloDoDia(c.ultimaEm, agora) === 'Hoje' ? hora(c.ultimaEm) : rotuloDoDia(c.ultimaEm, agora).split(',')[0]}</small>{c.naoLidas > 0 && <em>{c.naoLidas}</em>}</span>
        </button>;
      })}
    </div>}

    {aba === 'jogadores' && !conversa && <div className="cm-jogadores">
      <div className="cm-filtros">
        {([['todos', 'Todos', outros.length], ['online', 'Online', online.length], ['offline', 'Offline', outros.length - online.length]] as const).map(([id, nome, n]) =>
          <button key={id} className={`cm-filtro ${id} ${filtro === id ? 'ativo' : ''}`} onClick={() => setFiltro(id)} aria-pressed={filtro === id}>{id === 'online' && <span className="cm-ponto vivo" />}{id === 'offline' && <span className="cm-ponto" />}{nome}<b>{n}</b></button>)}
      </div>
      <label className="cm-busca"><Search size={16} /><input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder="Procurar jogador" aria-label="Procurar jogador" /></label>
      {!visiveis.length && <div className="cm-vazio"><Users size={34} /><b>{filtro === 'online' ? 'Ninguém online agora' : 'Ninguém encontrado'}</b><small>{filtro === 'online' ? 'Mande uma privada: a pessoa vê quando entrar.' : 'Tente outro nome.'}</small></div>}
      {visiveis.map((j, i) => {
        const st = statusDe(j, agora);
        return <div key={j.id} className={`cm-jogador ${j.online ? 'online' : ''}`} style={{ '--i': Math.min(i, 12) } as CSSProperties}>
          <button className="cm-jogador-quem" onClick={() => setPerfil(j.id)}>
            <Avatar jogador={j} id={j.id} nome={j.nome} tamanho={48} />
            <span className="cm-jogador-info">
              <b>{j.nome}<Coroa lugar={lugarDe.get(j.id)} /></b>
              <span className="cm-jogador-linha"><Titulo conquistas={j.conquistas} />{j.recorde ? <span className="cm-jogador-recorde"><Trophy size={12} />{formatarPontos(j.recorde)}</span> : <small className="cm-sem-recorde">sem recorde</small>}</span>
              <small className="cm-status">{j.online ? <span className="cm-ponto vivo" /> : <Clock3 size={12} />}{st.curto}{!j.online && j.vistoEm && <em> · {quando(j.vistoEm, agora)}</em>}</small>
            </span>
          </button>
          <button className="cm-dm" aria-label={`Mandar mensagem para ${j.nome}`} onClick={() => abrirConversa(j.id)}><MessageCircle size={18} /></button>
        </div>;
      })}
    </div>}

    {jogadorDoPerfil && <CartaoDoJogador jogador={jogadorDoPerfil} lugar={lugarDe.get(jogadorDoPerfil.id)} agora={agora} onDetails={onDetails} onClose={() => setPerfil(null)} onMensagem={() => abrirConversa(jogadorDoPerfil.id)} onDesafiar={jogadorDoPerfil.id === euId ? undefined : onDesafiar} />}
  </section>;
}
