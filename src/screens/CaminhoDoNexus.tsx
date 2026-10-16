import { useCallback, useEffect, useState, type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import { ArrowLeft, Brain, Crown, Eye, Flame, Lock, LogOut, Map as MapaIcone, Medal, Moon, Play, RotateCcw, Shield, Sparkles, Star, Swords, Trophy, X } from 'lucide-react';
import { byId } from '../data/characters';
import { ArenaDoPvp } from '../components/ArenaDoPvp';
import { DESCANSO, MINIMO_DA_CAMPANHA, REGIOES, RIVAIS, TITULOS, TOTAL_DE_ESTRELAS, colecaoDoRival, escalaDoRival, liberado, livresParaJogar, proximoRival, proximoTitulo,
  rivalPorId, tituloDas, totalDeEstrelas, zerou, type Rival } from '../engine/campanha';
import { variacaoContraNpc, type PartidaPvp, type Times } from '../engine/pvp';
import { ENGINE_VERSION } from '../engine/ranked';
import { read, save, type Settings } from '../lib/storage';
import { textoDoErroPvp, type PartidaDaCampanha, type RespostaDaCampanha, type ServicoDaCampanha } from '../lib/pvp-online';
import { Apresentar, Confirmar, Escolher, Fx, Montar, ResultadoDaRodada, Rosto, Vs, som, type Oponente } from './PvpScreen';
import { AvatarDoRival, CHAVE_DO_RESUMO, type ResumoDaCampanha } from '../components/CartaoDaCampanha';
import '../presentation/campanha.css';

/*
 * O Caminho do Nexus (pedido do jogador: "uma campanha mesmo… começa só um desbloqueado… muito bem gamificado"): o
 * mapa das 8 regiões com os 40 rivais (src/engine/campanha.ts), a ficha de cada um, a partida (as mesmas telas do
 * Treino, com o servidor de juiz: supabase/functions/ranked-api/campanha.ts) e o fim com as estrelas, o rating, o
 * rival liberado, a região conquistada e o título novo.
 */

const CHAVE_DAS_VISTAS = 'campanha-vistas';
const CHAVE_DOS_TIMES = 'campanha-times';

type Tela =
  | { tipo: 'mapa' }
  | { tipo: 'montar'; rival: Rival }
  | { tipo: 'apresentar' }
  | { tipo: 'escolher' }
  | { tipo: 'vs' }
  | { tipo: 'luta' }
  | { tipo: 'rodada' }
  | { tipo: 'fim' };

/** O antes da partida, para o fim mostrar o que mudou (estrelas, título, rival liberado, região). */
interface Antes { partida: string; estrelas: Record<string, number>; rating: number }

const regiaoDe = (r: Rival) => REGIOES[r.regiao - 1]!;
const faixaDe = (r: Rival) => (r.n === RIVAIS.length ? 'lenda' : r.chefe ? 'chefe' : 'arena') as 'lenda' | 'chefe' | 'arena';
const comoPvp = (p: PartidaDaCampanha, ate = p.rodadas.length): PartidaPvp => ({ meus: p.meus as Times, deles: p.deles as Times, rodadas: p.rodadas.slice(0, ate), seed: 0 });

const oponenteDoRival = (r: Rival): Oponente => ({ nome: r.nome, cor: r.cor, avatar: (t) => <AvatarDoRival rival={r} tamanho={t} />, fala: r.fala });

function Estrelinhas({ n, tamanho = 12 }: { n: number; tamanho?: number }) {
  return <span className="cn-estrelinhas" aria-label={`${n} de 3 estrelas`}>{[1, 2, 3].map((k) => <Star key={k} size={tamanho} className={k <= n ? 'on' : ''} />)}</span>;
}

function Descansando({ descanso, titulo = 'DESCANSANDO', vazio }: { descanso: Record<string, number>; titulo?: string; vazio?: string }) {
  const ids = Object.keys(descanso).filter((id) => byId[id] && descanso[id]! > 0);
  if (!ids.length && !vazio) return null;
  return <div className="cn-descanso">
    <span className="cn-descanso-titulo"><Moon size={14} />{titulo}</span>
    {ids.length ? <span className="cn-descanso-rostos">{ids.map((id) => <span key={id} className="cn-zz" title={`${byId[id]!.name}: volta em ${descanso[id]} partida${descanso[id] === 1 ? '' : 's'}`}>
      <Rosto id={id} tamanho={38} apagado /><i>💤{descanso[id]}</i></span>)}</span> : <small>{vazio}</small>}
  </div>;
}

/* ---------------------------------------------------------------------------
 * O mapa
 * ------------------------------------------------------------------------- */

/* onde cada rival fica na trilha da região (em % da largura): um zigue-zague que termina no chefe, no meio */
const POSICOES = [18, 70, 26, 74, 50];

function Regiao({ regiao, estrelas, atual, onRival }: { regiao: (typeof REGIOES)[number]; estrelas: Record<string, number>; atual: string | null; onRival: (r: Rival) => void }) {
  const rivais = RIVAIS.filter((r) => r.regiao === regiao.n);
  const aberta = liberado(estrelas, rivais[0]!), feitas = rivais.reduce((s, r) => s + (estrelas[r.id] ?? 0), 0);
  const conquistada = (estrelas[rivais[4]!.id] ?? 0) > 0;
  const ALTURA = 106, alto = ALTURA * rivais.length;
  const pontos = rivais.map((_, k) => `${POSICOES[k]},${k * ALTURA + 46}`).join(' ');
  return <section className={`cn-regiao ${aberta ? '' : 'bloqueada'} ${conquistada ? 'conquistada' : ''}`} style={{ '--c1': regiao.cor, '--c2': regiao.cor2 } as CSSProperties}>
    <header className="cn-regiao-topo">
      <span className="cn-regiao-icone" aria-hidden="true">{regiao.icone}</span>
      <div><small>REGIÃO {regiao.n}{regiao.aura > 0 ? ` · AURA DO CHEFE +${Math.round(regiao.aura * 100)}%` : ''}</small><b>{regiao.nome}</b><span>{regiao.lema}</span></div>
      <span className="cn-regiao-estrelas"><Star size={14} />{feitas}/15</span>
    </header>
    <div className="cn-trilha" style={{ height: alto }}>
      <svg className="cn-caminho" viewBox={`0 0 100 ${alto}`} preserveAspectRatio="none" aria-hidden="true"><polyline points={pontos} /></svg>
      {rivais.map((r, k) => {
        const e = estrelas[r.id] ?? 0, livre = liberado(estrelas, r), agora = r.id === atual;
        return <button key={r.id} className={`cn-no ${r.chefe ? 'chefe' : ''} ${e ? 'vencido' : ''} ${agora ? 'atual' : ''} ${livre ? '' : 'bloqueado'}`}
          style={{ left: `${POSICOES[k]}%`, top: k * ALTURA, '--cor': r.cor, '--k': k } as CSSProperties} onClick={() => { som('toque'); onRival(r); }}
          aria-label={`${r.nome}${livre ? '' : ', bloqueado'}`}>
          {agora && <span className="cn-lute">LUTE!</span>}
          <AvatarDoRival rival={r} tamanho={r.chefe ? 78 : 60} apagado={!livre} />
          {!livre && <Lock className="cn-cadeado" size={18} />}
          {r.aura > 0 && <span className="cn-aura-chip"><Flame size={10} />+{Math.round(r.aura * 100)}%</span>}
          <span className="cn-no-nome"><small>{r.chefe ? 'CHEFE' : `#${r.n}`}</small>{livre ? r.nome : '???'}</span>
          {livre && <Estrelinhas n={e} />}
        </button>;
      })}
    </div>
    {!aberta && <div className="cn-regiao-trava"><Lock size={16} />Vença o chefe da região {regiao.n - 1} para abrir</div>}
  </section>;
}

function Mapa({ r, onRival, onVoltar }: { r: RespostaDaCampanha; onRival: (x: Rival) => void; onVoltar: () => void }) {
  const total = totalDeEstrelas(r.progresso.estrelas), titulo = tituloDas(total), prox = proximoTitulo(total), proximo = proximoRival(r.progresso.estrelas);
  const deTitulo = prox ? (total - titulo.estrelas) / (prox.estrelas - titulo.estrelas) : 1;
  const fim = zerou(r.progresso.estrelas);
  return <section className="cn">
    <header className="cn-topo">
      <button className="icon-button" onClick={onVoltar} aria-label="Voltar"><ArrowLeft size={20} /></button>
      <div><small>MODO CAMPANHA</small><h1>CAMINHO DO NEXUS</h1></div>
      <span className="cn-rating" title="Seu rating do PvP"><Crown size={14} />{r.rating.rating}</span>
    </header>

    <div className="cn-heroi" style={{ '--tc': titulo.cor } as CSSProperties}>
      <Fx nome="holofote" cor={titulo.cor} ms={5200} className="cn-fx-holofote" />
      <span className="cn-emblema"><Medal size={34} /></span>
      <div className="cn-heroi-texto">
        <small>SEU TÍTULO</small><b>{titulo.nome}</b>
        <span className="cn-barra"><i style={{ width: `${Math.round(100 * deTitulo)}%` }} /></span>
        <span className="cn-heroi-linha"><span><Star size={13} />{total}/{TOTAL_DE_ESTRELAS}</span>{prox ? <em>faltam {prox.estrelas - total}★ para {prox.nome}</em> : <em>título máximo!</em>}</span>
      </div>
    </div>
    {fim && <div className="cn-zerou"><Trophy size={22} /><div><b>CONQUISTADOR DO NEXUS</b><small>Você derrotou o Imperador. Agora junte as 120 estrelas!</small></div></div>}

    {proximo && <button className="cn-continuar" style={{ '--cor': proximo.cor } as CSSProperties} onClick={() => { som('ui-arena'); onRival(proximo); }}>
      <AvatarDoRival rival={proximo} tamanho={52} />
      <span><small>PRÓXIMO RIVAL · REGIÃO {proximo.regiao}</small><b>{proximo.nome}</b><em>{proximo.estilo}</em></span>
      <Play size={22} />
    </button>}

    <Descansando descanso={r.progresso.descanso} titulo="SEUS PERSONAGENS DESCANSANDO" vazio={`Rodízio: os ${DESCANSO.quantos} que mais lutarem nas últimas ${DESCANSO.janela} partidas descansam ${DESCANSO.partidas}. Vale para os rivais também.`} />

    <div className="cn-regioes">
      {REGIOES.map((g) => <Regiao key={g.id} regiao={g} estrelas={r.progresso.estrelas} atual={proximo?.id ?? null} onRival={onRival} />)}
    </div>
    <div className="cn-titulos">
      <h3><Medal size={15} />TÍTULOS</h3>
      <div>{TITULOS.map((t) => <span key={t.nome} className={total >= t.estrelas ? 'on' : ''} style={{ '--tc': t.cor } as CSSProperties}><b>{t.nome}</b><small>{t.estrelas}★</small></span>)}</div>
    </div>
  </section>;
}

/* ---------------------------------------------------------------------------
 * A ficha do rival
 * ------------------------------------------------------------------------- */

function Ficha({ rival, r, onFechar, onDesafiar }: { rival: Rival; r: RespostaDaCampanha; onFechar: () => void; onDesafiar: () => void }) {
  const livre = liberado(r.progresso.estrelas, rival), regiao = regiaoDe(rival), e = r.progresso.estrelas[rival.id] ?? 0, placar = r.progresso.placar[rival.id] ?? { v: 0, d: 0 };
  const livres = livresParaJogar(r.colecao, r.progresso.descanso).length, falta = Math.max(0, MINIMO_DA_CAMPANHA - r.colecao.length);
  const ganha = variacaoContraNpc(r.rating.rating, rival.rating, true), perde = variacaoContraNpc(r.rating.rating, rival.rating, false);
  const anterior = RIVAIS[rival.n - 2];
  return createPortal(<div className="pv-painel-fundo cn-ficha-fundo" onClick={(ev) => { if (ev.target === ev.currentTarget) onFechar(); }}>
    <section className="cn-ficha" role="dialog" aria-label={rival.nome} style={{ '--cor': rival.cor, '--c1': regiao.cor, '--c2': regiao.cor2 } as CSSProperties}>
      <button className="icon-button cn-ficha-x" onClick={onFechar} aria-label="Fechar"><X size={18} /></button>
      <div className="cn-ficha-capa">
        <span className="cn-ficha-regiao">{regiao.icone} REGIÃO {regiao.n} · {regiao.nome.toUpperCase()}</span>
        <AvatarDoRival rival={rival} tamanho={104} apagado={!livre} />
        {rival.chefe && <span className="cn-selo-chefe"><Crown size={13} />{rival.n === RIVAIS.length ? 'CHEFE FINAL' : 'CHEFE DA REGIÃO'}</span>}
      </div>
      <small className="cn-ficha-titulo">{rival.titulo.toUpperCase()}</small>
      <h2>{livre ? rival.nome : '???'}</h2>
      {livre ? <>
        <div className="cn-chips">
          <span className="cn-chip estilo"><Sparkles size={12} />{rival.estilo}</span>
          <span className="cn-chip"><Crown size={12} />{rival.rating}</span>
          <span className="cn-chip"><Shield size={12} />{rival.espelho ? 'copia os seus' : `${colecaoDoRival(rival).length} personagens`}</span>
          <span className="cn-chip cerebro" title="Dificuldade"><Brain size={12} />{Array.from({ length: 8 }, (_, k) => <i key={k} className={k < rival.regiao ? 'on' : ''} />)}</span>
          {rival.cerebro.escolha === 'vidente' && <span className="cn-chip vidente"><Eye size={12} />vê o futuro</span>}
          {rival.aura > 0 && <span className="cn-chip aura"><Flame size={12} />Aura +{Math.round(rival.aura * 100)}% Vida</span>}
        </div>
        <p className="cn-jeito">{rival.jeito}</p>
        <p className="cn-fala">“{rival.fala}”</p>
        <div className="cn-ficha-linhas">
          <span><small>SEU RECORDE</small><Estrelinhas n={e} tamanho={16} /></span>
          <span><small>PLACAR</small><b className="v">{placar.v}V</b> <b className="d">{placar.d}D</b></span>
          <span><small>RATING</small><b className="v">{ganha > 0 ? `+${ganha}` : '+0'}</b> <b className="d">{perde}</b></span>
        </div>
        {ganha === 0 && <small className="cn-nota">Você está 400 ou mais acima dele: vencer não dá rating (as estrelas valem).</small>}
        <div className="cn-premio"><Star size={14} />3–0 dá ★★★ · 3–1 dá ★★ · 3–2 dá ★</div>
        <Descansando descanso={r.progresso.descanso_rivais[rival.id] ?? {}} titulo="DESCANSANDO DO LADO DELE" />
        {falta > 0 ? <p className="cn-aviso"><Lock size={14} />A campanha pede {MINIMO_DA_CAMPANHA} personagens na coleção: faltam {falta}.</p>
          : livres < 9 ? <p className="cn-aviso"><Moon size={14} />Gente demais descansando: espere o rodízio.</p>
          : <button className="primary pv-grande cn-desafiar" onClick={onDesafiar}><Swords size={22} />DESAFIAR</button>}
      </> : <p className="cn-aviso"><Lock size={14} />Vença {anterior ? anterior.nome : 'o rival anterior'} para liberar.</p>}
    </section>
  </div>, document.body);
}

/* ---------------------------------------------------------------------------
 * O fim da partida
 * ------------------------------------------------------------------------- */

function Fim({ rival, partida, antes, r, onMapa, onDeNovo, onProximo }: { rival: Rival; partida: PartidaDaCampanha; antes: Antes | null; r: RespostaDaCampanha; onMapa: () => void; onDeNovo: () => void; onProximo: (x: Rival) => void }) {
  const ganhei = partida.vencedor === 'eu', estrelas = partida.estrelas ?? 0;
  const eAntes = antes?.estrelas ?? {}, recorde = estrelas > (eAntes[rival.id] ?? 0);
  const totalAntes = totalDeEstrelas(eAntes), totalAgora = totalDeEstrelas(r.progresso.estrelas);
  const tituloNovo = tituloDas(totalAgora).nome !== tituloDas(totalAntes).nome ? tituloDas(totalAgora) : null;
  const liberouAgora = ganhei && !(eAntes[rival.id] ?? 0) ? RIVAIS[rival.n] ?? null : null;
  const regiaoNova = ganhei && rival.chefe && !(eAntes[rival.id] ?? 0);
  const zerouAgora = regiaoNova && rival.n === RIVAIS.length;
  const delta = partida.delta ?? 0;
  const [mostradas, setMostradas] = useState(0);
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  useEffect(() => { if (mostradas >= estrelas) return; const t = window.setTimeout(() => { setMostradas((m) => m + 1); som('pronto'); }, 520); return () => clearTimeout(t); }, [mostradas, estrelas]);
  return <section className={`pv-fim cn-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <small>CAMINHO DO NEXUS · {rival.titulo.toUpperCase()}</small>
    <h1>{zerouAgora ? 'O NEXUS É SEU!' : ganhei ? 'VITÓRIA!' : 'DERROTA'}</h1>
    <AvatarDoRival rival={rival} tamanho={72} apagado={ganhei} />
    <p className="cn-fala">“{ganhei ? rival.perdeu : rival.venceu}” <small>— {rival.nome}</small></p>
    {ganhei && <div className="cn-fim-estrelas" aria-label={`${estrelas} estrelas`}>{[1, 2, 3].map((k) => <Star key={k} size={44} className={k <= mostradas ? 'on' : ''} />)}</div>}
    {ganhei && recorde && mostradas >= estrelas && <span className="cn-recorde"><Sparkles size={14} />NOVO RECORDE</span>}
    <div className="pv-fim-rodadas">{partida.rodadas.map((x, i) => <span key={i} className={x.vencedor}><b>{i + 1}</b>{x.vencedor === 'eu' ? 'V' : 'D'}</span>)}</div>
    <div className={`cn-delta ${delta > 0 ? 'sobe' : delta < 0 ? 'cai' : ''}`}><Crown size={16} />Rating {antes?.rating ?? r.rating.rating - delta} → <b>{r.rating.rating}</b><em>{delta > 0 ? `+${delta}` : delta}</em></div>
    {ganhei && delta === 0 && <small className="cn-nota">400 ou mais acima do rival: a vitória não dá rating.</small>}
    {partida.motivo === 'abandonou' && <small className="cn-nota">Abandonar conta como derrota.</small>}

    {zerouAgora && <div className="cn-conquista lenda"><Trophy size={26} /><div><b>CONQUISTADOR DO NEXUS</b><small>Você derrotou o Imperador e zerou a campanha!</small></div></div>}
    {regiaoNova && !zerouAgora && <div className="cn-conquista"><MapaIcone size={22} /><div><b>REGIÃO CONQUISTADA!</b><small>{regiaoDe(rival).nome} é sua. {REGIOES[rival.regiao] ? `Abriu: ${REGIOES[rival.regiao]!.icone} ${REGIOES[rival.regiao]!.nome}` : ''}</small></div></div>}
    {tituloNovo && <div className="cn-conquista titulo" style={{ '--tc': tituloNovo.cor } as CSSProperties}><Medal size={22} /><div><b>NOVO TÍTULO: {tituloNovo.nome.toUpperCase()}</b><small>{totalAgora} estrelas no caminho</small></div></div>}
    {liberouAgora && <button className="cn-liberou" style={{ '--cor': liberouAgora.cor } as CSSProperties} onClick={() => onProximo(liberouAgora)}>
      <AvatarDoRival rival={liberouAgora} tamanho={50} /><span><small>NOVO RIVAL LIBERADO</small><b>{liberouAgora.nome}</b><em>{liberouAgora.estilo}</em></span><Play size={20} />
    </button>}
    <Descansando descanso={r.progresso.descanso} titulo="AGORA DESCANSAM" />
    <div className="pv-fim-botoes"><button className="primary" onClick={onDeNovo}><RotateCcw size={18} />{ganhei && estrelas < 3 ? 'Buscar 3★' : 'Jogar de novo'}</button><button className="secondary" onClick={onMapa}><MapaIcone size={18} />Mapa</button></div>
  </section>;
}

/* ---------------------------------------------------------------------------
 * A tela
 * ------------------------------------------------------------------------- */

export default function CaminhoDoNexus({ servico, settings, onSettings, onDetails, onLutando, onVoltar, dono = false }: {
  servico: ServicoDaCampanha; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onLutando: (sim: boolean) => void; onVoltar: () => void; dono?: boolean;
}) {
  const [r, setR] = useState<RespostaDaCampanha | null>(null);
  const [erro, setErro] = useState('');
  const [tela, setTela] = useState<Tela>({ tipo: 'mapa' });
  const [ficha, setFicha] = useState<Rival | null>(null);
  const [ocupado, setOcupado] = useState(false);
  const [confirmar, setConfirmar] = useState<'luta' | 'partida' | null>(null);
  const [vistas, setVistas] = useState(0);
  const [antes, setAntes] = useState<Antes | null>(null);
  const [tentativa, setTentativa] = useState(0);
  const partida = r?.partida ?? null, rival = partida ? rivalPorId(partida.rival) : null;

  // o resumo para o cartão do lobby
  useEffect(() => {
    if (!r) return;
    const e = r.progresso.estrelas, total = totalDeEstrelas(e);
    save(CHAVE_DO_RESUMO, { estrelas: total, titulo: tituloDas(total).nome, proximo: proximoRival(e)?.id ?? null, zerou: zerou(e) } satisfies ResumoDaCampanha);
  }, [r]);
  useEffect(() => { onLutando(tela.tipo === 'luta'); window.scrollTo(0, 0); }, [tela.tipo, onLutando]);
  useEffect(() => () => onLutando(false), [onLutando]);

  const guardaVistas = (id: string, n: number) => { setVistas(n); save(CHAVE_DAS_VISTAS, { partida: id, n }); };
  const abrir = useCallback(async () => {
    setErro('');
    try {
      const x = await servico.estado();
      setR(x);
      const p = x.partida;
      if (p && p.estado === 'jogando') {
        const salvo = read(CHAVE_DAS_VISTAS) as { partida?: string; n?: number } | null, n = salvo?.partida === p.id ? Math.min(p.rodadas.length, salvo.n ?? 0) : p.rodadas.length;
        setVistas(n);
        const a = read('campanha-antes') as Antes | null;
        setAntes(a?.partida === p.id ? a : null);
        setTela(n < p.rodadas.length ? { tipo: 'vs' } : p.rodadas.length ? { tipo: 'escolher' } : { tipo: 'apresentar' });
      }
    } catch (e) { setErro(textoDoErroPvp(e)); }
  }, [servico]);
  useEffect(() => { void abrir(); }, [abrir]);

  const pede = async (f: () => Promise<RespostaDaCampanha>) => {
    setOcupado(true); setErro('');
    try { const x = await f(); setR(x); return x; } catch (e) { setErro(textoDoErroPvp(e)); return null; } finally { setOcupado(false); }
  };
  const comecar = async (alvo: Rival, times: Times) => {
    if (!r) return;
    save(CHAVE_DOS_TIMES, times);
    const a = { estrelas: { ...r.progresso.estrelas }, rating: r.rating.rating };
    const x = await pede(() => servico.comecar(alvo.id, times, ENGINE_VERSION));
    if (!x?.partida) return;
    const novo = { ...a, partida: x.partida.id };
    setAntes(novo); save('campanha-antes', novo); guardaVistas(x.partida.id, 0);
    setTela({ tipo: 'apresentar' });
  };
  const escolher = async (time: number) => {
    if (!partida) return;
    const x = await pede(() => servico.escolher(partida.id, vistas, time));
    if (!x?.partida) { setTentativa((t) => t + 1); return; }
    if (x.partida.rodadas.length > vistas) setTela({ tipo: 'vs' });
    else setTentativa((t) => t + 1);
  };
  const assistiu = () => { if (!partida) return; guardaVistas(partida.id, vistas + 1); setTela({ tipo: 'rodada' }); };
  const render = async () => {
    if (!partida) return;
    const x = await pede(() => servico.render(partida.id, vistas));
    if (x?.partida) assistiu();
  };
  const abandonar = async () => {
    if (!partida) return;
    const x = await pede(() => servico.abandonar(partida.id));
    if (x?.partida) { guardaVistas(x.partida.id, x.partida.rodadas.length); setTela({ tipo: 'fim' }); }
  };
  const irPara = (alvo: Rival) => { setFicha(null); setR((x) => (x ? { ...x, partida: null } : x)); setTela({ tipo: 'mapa' }); window.setTimeout(() => setFicha(alvo), 60); };

  const meusTimes = read(CHAVE_DOS_TIMES) as string[][] | undefined;
  const avisoDeErro = erro && <div className="cn-erro" role="alert"><span>{erro}</span><button className="icon-button" onClick={() => setErro('')} aria-label="Fechar"><X size={14} /></button></div>;

  if (!r) return <section className="cn cn-carregando">{erro ? <><p>{erro}</p><button className="secondary" onClick={() => void abrir()}>Tentar de novo</button><button className="secondary" onClick={onVoltar}>Voltar</button></> : <p className="cm-carregando-tela">Abrindo o Caminho do Nexus…</p>}</section>;

  if (tela.tipo === 'montar') {
    const alvo = tela.rival, livres = livresParaJogar(r.colecao, r.progresso.descanso);
    return <>{avisoDeErro}<Montar melhores={dono} rival={oponenteDoRival(alvo)} colecao={livres} inicial={meusTimes} ocupado={ocupado} onDetails={onDetails}
      onVoltar={() => setTela({ tipo: 'mapa' })} onPronto={(t) => void comecar(alvo, t)}
      aviso={<Descansando descanso={r.progresso.descanso} titulo="DESCANSANDO (NÃO PODEM JOGAR)" />} /></>;
  }

  if (partida && rival && tela.tipo !== 'mapa') {
    const op = oponenteDoRival(rival), pvp = comoPvp(partida, vistas), rodada = partida.rodadas[vistas];
    const aura = rival.aura > 0 && <div className="cn-aura-banner"><Flame size={16} /><b>AURA DO CHEFE</b>+{Math.round(rival.aura * 100)}% de Vida em todos os personagens de {rival.nome}</div>;
    const sair = <button className="pv-sair-online" onClick={() => setConfirmar('partida')} disabled={ocupado}><LogOut size={14} />Abandonar partida</button>;
    const confirmacao = confirmar && (confirmar === 'luta'
      ? <Confirmar titulo="Desistir desta luta?" texto="Você perde esta rodada. A partida continua com os outros times." sim="Desistir da luta" onNao={() => setConfirmar(null)} onSim={() => { setConfirmar(null); void render(); }} />
      : <Confirmar titulo="Abandonar a partida?" texto={`Abandonar conta como derrota contra ${rival.nome} (e mexe no rating).`} sim="Abandonar" onNao={() => setConfirmar(null)} onSim={() => { setConfirmar(null); void abandonar(); }} />);
    if (tela.tipo === 'apresentar') return <>{avisoDeErro}{aura}<Apresentar rival={op} partida={comoPvp(partida)} onComecar={() => setTela({ tipo: 'escolher' })} /></>;
    if (tela.tipo === 'escolher') return <>{avisoDeErro}{aura}<Escolher key={`${vistas}-${tentativa}`} rival={op} partida={pvp} onEscolher={(i) => void escolher(i)} />{sair}{confirmacao}</>;
    if (tela.tipo === 'vs' && rodada) return <Vs rival={op} partida={comoPvp(partida)} meu={rodada.meu} dele={rodada.dele} onLutar={() => setTela({ tipo: 'luta' })} />;
    if (tela.tipo === 'luta' && rodada) return <>{avisoDeErro}<ArenaDoPvp meu={partida.meus[rodada.meu]!} dele={partida.deles[rodada.dele]!} seed={rodada.seed} rodada={vistas + 1} rival={rival.nome} settings={settings} onSettings={onSettings}
      podePausar escala={escalaDoRival(rival)} faixa={faixaDe(rival)} onFim={assistiu} onDesistir={() => setConfirmar('luta')} />{confirmacao}</>;
    if (tela.tipo === 'rodada' && vistas > 0) return <ResultadoDaRodada rival={op} partida={comoPvp(partida, vistas)} final={partida.estado === 'terminada' && vistas >= partida.rodadas.length}
      onSeguir={() => setTela(partida.estado === 'terminada' && vistas >= partida.rodadas.length ? { tipo: 'fim' } : { tipo: 'escolher' })} />;
    if (tela.tipo === 'fim' && partida.estado === 'terminada') return <Fim rival={rival} partida={partida} antes={antes} r={r} onMapa={() => { setR({ ...r, partida: null }); setTela({ tipo: 'mapa' }); }}
      onDeNovo={() => { setR({ ...r, partida: null }); setTela({ tipo: 'montar', rival }); }} onProximo={irPara} />;
  }

  return <>
    {avisoDeErro}
    <Mapa r={r} onRival={setFicha} onVoltar={onVoltar} />
    {ficha && <Ficha rival={ficha} r={r} onFechar={() => setFicha(null)} onDesafiar={() => { som('ui-arena'); setFicha(null); setTela({ tipo: 'montar', rival: ficha }); }} />}
    {ocupado && <div className="cn-ocupado" aria-hidden="true" />}
  </>;
}
