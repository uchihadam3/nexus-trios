import { useCallback, useContext, useEffect, useState, type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import { ArrowLeft, Brain, Crown, Eye, Flame, Lock, LogOut, Map as MapaIcone, Medal, Moon, Play, RotateCcw, Shield, Sparkles, Star, Swords, Trophy, X } from 'lucide-react';
import { byId } from '../data/characters';
import { ArenaDoPvp } from '../components/ArenaDoPvp';
import { DESCANSO, DORMEM_NO_MAXIMO, DORMEM_POR_PARTIDA, MINIMO_DA_CAMPANHA, REGIOES, RIVAIS, TITULOS, TOTAL_DE_ESTRELAS, colecaoDoRival, escalaDoRival, liberado, livresParaJogar, proximoRival, proximoTitulo,
  rivalPorId, tituloDas, totalDeEstrelas, zerou, type Rival } from '../engine/campanha';
import type { PartidaPvp, Times } from '../engine/pvp';
import { ENGINE_VERSION } from '../engine/ranked';
import { read, save, type Settings } from '../lib/storage';
import type { Faixa, RegiaoDaMusica } from '../lib/audio';
import { textoDoErroPvp, type PartidaDaCampanha, type RespostaDaCampanha, type ServicoDaCampanha } from '../lib/pvp-online';
import { Apresentar, Confirmar, DonoDoPvp, Escolher, Fx, Montar, ResultadoDaRodada, Rosto, Vs, som, type Oponente } from './PvpScreen';
import { AvatarDoRival, CHAVE_DO_RESUMO, type ResumoDaCampanha } from '../components/CartaoDaCampanha';
import '../presentation/campanha.css';
import { nomeDe, plural, t, tx } from '../i18n/idioma';

/*
 * O Caminho do Nexus (pedido do jogador: "uma campanha mesmo… começa só um desbloqueado… muito bem gamificado"): o
 * mapa das 8 regiões com os 40 rivais (src/engine/campanha.ts), a ficha de cada um, a partida (as mesmas telas do
 * Treino, com o servidor de juiz: supabase/functions/ranked-api/campanha.ts) e o fim com as estrelas, o rival
 * liberado, a região conquistada e o título novo. O Nexus não mexe no rating do PvP: o ranking dele é o das estrelas.
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
interface Antes { partida: string; estrelas: Record<string, number> }

const regiaoDe = (r: Rival) => REGIOES[r.regiao - 1]!;
/* a música de cada região e a do chefe dela (src/lib/audio.ts, v8) */
const faixaDe = (r: Rival): Faixa => `${r.chefe ? 'chefe' : 'regiao'}-${regiaoDe(r).id as RegiaoDaMusica}`;
const comoPvp = (p: PartidaDaCampanha, ate = p.rodadas.length): PartidaPvp => ({ meus: p.meus as Times, deles: p.deles as Times, rodadas: p.rodadas.slice(0, ate), seed: 0 });

const oponenteDoRival = (r: Rival): Oponente => ({ nome: t(r.nome), cor: r.cor, avatar: (tam) => <AvatarDoRival rival={r} tamanho={tam} />, fala: t(r.fala) });

function Estrelinhas({ n, tamanho = 12 }: { n: number; tamanho?: number }) {
  return <span className="cn-estrelinhas" aria-label={t('{n} de 3 estrelas', { n })}>{[1, 2, 3].map((k) => <Star key={k} size={tamanho} className={k <= n ? 'on' : ''} />)}</span>;
}

function Descansando({ descanso, titulo = tx('DESCANSANDO'), vazio }: { descanso: Record<string, number>; titulo?: string; vazio?: string }) {
  const ids = Object.keys(descanso).filter((id) => byId[id] && descanso[id]! > 0);
  if (!ids.length && !vazio) return null;
  return <div className="cn-descanso">
    <span className="cn-descanso-titulo"><Moon size={14} />{t(titulo)}</span>
    {ids.length ? <span className="cn-descanso-rostos">{ids.map((id) => <span key={id} className="cn-zz" title={`${nomeDe(byId[id]!)}: ${plural(descanso[id]!, 'volta em {n} partida', 'volta em {n} partidas')}`}>
      <Rosto id={id} tamanho={38} apagado /><i>💤{descanso[id]}</i></span>)}</span> : <small>{t(vazio ?? '')}</small>}
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
      <div><small>{t('REGIÃO {n}', { n: regiao.n })}{regiao.aura > 0 ? ` · ${t('AURA DO CHEFE +{n}%', { n: Math.round(regiao.aura * 100) })}` : ''}</small><b>{t(regiao.nome)}</b><span>{t(regiao.lema)}</span></div>
      <span className="cn-regiao-estrelas"><Star size={14} />{feitas}/15</span>
    </header>
    <div className="cn-trilha" style={{ height: alto }}>
      <svg className="cn-caminho" viewBox={`0 0 100 ${alto}`} preserveAspectRatio="none" aria-hidden="true"><polyline points={pontos} /></svg>
      {rivais.map((r, k) => {
        const e = estrelas[r.id] ?? 0, livre = liberado(estrelas, r), agora = r.id === atual;
        return <button key={r.id} className={`cn-no ${r.chefe ? 'chefe' : ''} ${e ? 'vencido' : ''} ${agora ? 'atual' : ''} ${livre ? '' : 'bloqueado'}`}
          style={{ left: `${POSICOES[k]}%`, top: k * ALTURA, '--cor': r.cor, '--k': k } as CSSProperties} onClick={() => { som('toque'); onRival(r); }}
          aria-label={`${t(r.nome)}${livre ? '' : t(', bloqueado')}`}>
          {agora && <span className="cn-lute">{t('LUTE!')}</span>}
          <AvatarDoRival rival={r} tamanho={r.chefe ? 78 : 60} apagado={!livre} />
          {!livre && <Lock className="cn-cadeado" size={18} />}
          {r.aura > 0 && <span className="cn-aura-chip"><Flame size={10} />+{Math.round(r.aura * 100)}%</span>}
          <span className="cn-no-nome"><small>{r.chefe ? t('CHEFE') : `#${r.n}`}</small>{livre ? t(r.nome) : '???'}</span>
          {livre && <Estrelinhas n={e} />}
        </button>;
      })}
    </div>
    {!aberta && <div className="cn-regiao-trava"><Lock size={16} />{t('Vença o chefe da região {n} para abrir', { n: regiao.n - 1 })}</div>}
  </section>;
}

function Mapa({ r, onRival, onVoltar }: { r: RespostaDaCampanha; onRival: (x: Rival) => void; onVoltar: () => void }) {
  const total = totalDeEstrelas(r.progresso.estrelas), titulo = tituloDas(total), prox = proximoTitulo(total), proximo = proximoRival(r.progresso.estrelas);
  const deTitulo = prox ? (total - titulo.estrelas) / (prox.estrelas - titulo.estrelas) : 1;
  const fim = zerou(r.progresso.estrelas);
  return <section className="cn">
    <header className="cn-topo">
      <button className="icon-button" onClick={onVoltar} aria-label={t('Voltar')}><ArrowLeft size={20} /></button>
      <div><small>{t('MODO CAMPANHA')}</small><h1>{t('CAMINHO DO NEXUS')}</h1></div>
      <span className="cn-rating" title={t('Suas estrelas no Caminho do Nexus (o ranking do Nexus)')}><Star size={14} />{total}/{TOTAL_DE_ESTRELAS}</span>
    </header>

    <div className="cn-heroi" style={{ '--tc': titulo.cor } as CSSProperties}>
      <Fx nome="holofote" cor={titulo.cor} ms={5200} className="cn-fx-holofote" />
      <span className="cn-emblema"><Medal size={34} /></span>
      <div className="cn-heroi-texto">
        <small>{t('SEU TÍTULO')}</small><b>{t(titulo.nome)}</b>
        <span className="cn-barra"><i style={{ width: `${Math.round(100 * deTitulo)}%` }} /></span>
        <span className="cn-heroi-linha"><span><Star size={13} />{total}/{TOTAL_DE_ESTRELAS}</span>{prox ? <em>{t('faltam {n}★ para {titulo}', { n: prox.estrelas - total, titulo: t(prox.nome) })}</em> : <em>{t('título máximo!')}</em>}</span>
      </div>
    </div>
    {fim && <div className="cn-zerou"><Trophy size={22} /><div><b>{t('CONQUISTADOR DO NEXUS')}</b><small>{t('Você derrotou o Imperador. Agora junte as 120 estrelas!')}</small></div></div>}

    {proximo && <button className="cn-continuar" style={{ '--cor': proximo.cor } as CSSProperties} onClick={() => { som('ui-arena'); onRival(proximo); }}>
      <AvatarDoRival rival={proximo} tamanho={52} />
      <span><small>{t('PRÓXIMO RIVAL · REGIÃO {n}', { n: proximo.regiao })}</small><b>{t(proximo.nome)}</b><em>{t(proximo.estilo)}</em></span>
      <Play size={22} />
    </button>}

    <Descansando descanso={r.progresso.descanso} titulo={tx('SEUS PERSONAGENS DESCANSANDO')} vazio={t('Rodízio: os que mais lutarem nas últimas {janela} partidas descansam. Depois de cada partida dormem {dormem}, por {partidas} partidas, até {maximo} dormindo. Só conta partida contra rival que você ainda não gabaritou (★★★).', { janela: DESCANSO.janela, dormem: DORMEM_POR_PARTIDA, partidas: DESCANSO.partidas, maximo: DORMEM_NO_MAXIMO })} />

    <div className="cn-regioes">
      {REGIOES.map((g) => <Regiao key={g.id} regiao={g} estrelas={r.progresso.estrelas} atual={proximo?.id ?? null} onRival={onRival} />)}
    </div>
    <div className="cn-titulos">
      <h3><Medal size={15} />{t('TÍTULOS')}</h3>
      <div>{TITULOS.map((tit) => <span key={tit.nome} className={total >= tit.estrelas ? 'on' : ''} style={{ '--tc': tit.cor } as CSSProperties}><b>{t(tit.nome)}</b><small>{tit.estrelas}★</small></span>)}</div>
    </div>
  </section>;
}

/* ---------------------------------------------------------------------------
 * A ficha do rival
 * ------------------------------------------------------------------------- */

function Ficha({ rival, r, onFechar, onDesafiar }: { rival: Rival; r: RespostaDaCampanha; onFechar: () => void; onDesafiar: () => void }) {
  const livre = liberado(r.progresso.estrelas, rival), regiao = regiaoDe(rival), e = r.progresso.estrelas[rival.id] ?? 0, placar = r.progresso.placar[rival.id] ?? { v: 0, d: 0 };
  const livres = livresParaJogar(r.colecao, r.progresso.descanso).length, falta = Math.max(0, MINIMO_DA_CAMPANHA - r.colecao.length);
  const anterior = RIVAIS[rival.n - 2], dono = useContext(DonoDoPvp);
  return createPortal(<div className="pv-painel-fundo cn-ficha-fundo" onClick={(ev) => { if (ev.target === ev.currentTarget) onFechar(); }}>
    <section className="cn-ficha" role="dialog" aria-label={t(rival.nome)} style={{ '--cor': rival.cor, '--c1': regiao.cor, '--c2': regiao.cor2 } as CSSProperties}>
      <button className="icon-button cn-ficha-x" onClick={onFechar} aria-label={t('Fechar')}><X size={18} /></button>
      <div className="cn-ficha-capa">
        <span className="cn-ficha-regiao">{regiao.icone} {t('REGIÃO {n}', { n: regiao.n })} · {t(regiao.nome).toUpperCase()}</span>
        <AvatarDoRival rival={rival} tamanho={104} apagado={!livre} />
        {rival.chefe && <span className="cn-selo-chefe"><Crown size={13} />{rival.n === RIVAIS.length ? t('CHEFE FINAL') : t('CHEFE DA REGIÃO')}</span>}
      </div>
      <small className="cn-ficha-titulo">{t(rival.titulo).toUpperCase()}</small>
      <h2>{livre ? t(rival.nome) : '???'}</h2>
      {livre ? <>
        <div className="cn-chips">
          <span className="cn-chip estilo"><Sparkles size={12} />{t(rival.estilo)}</span>
          {dono && <span className="cn-chip" title={t('A força máxima dos times dele')}><Star size={12} />{t('times até {n}★', { n: rival.estrelas })}</span>}
          <span className="cn-chip"><Shield size={12} />{rival.espelho ? t('copia os seus') : t('{n} personagens', { n: colecaoDoRival(rival).length })}</span>
          <span className="cn-chip cerebro" title={t('Dificuldade')}><Brain size={12} />{Array.from({ length: 8 }, (_, k) => <i key={k} className={k < rival.regiao ? 'on' : ''} />)}</span>
          {rival.cerebro.escolha === 'vidente' && <span className="cn-chip vidente"><Eye size={12} />{t('vê o futuro')}</span>}
          {rival.aura > 0 && <span className="cn-chip aura"><Flame size={12} />{t('Aura +{n}% Vida', { n: Math.round(rival.aura * 100) })}</span>}
        </div>
        <p className="cn-jeito">{t(rival.jeito)}</p>
        <p className="cn-fala">“{t(rival.fala)}”</p>
        <div className="cn-ficha-linhas">
          <span><small>{t('SEU RECORDE')}</small><Estrelinhas n={e} tamanho={16} /></span>
          <span><small>{t('PLACAR')}</small><b className="v">{t('{n}V', { n: placar.v })}</b> <b className="d">{t('{n}D', { n: placar.d })}</b></span>
        </div>
        <div className="cn-premio"><Star size={14} />{t('3–0 dá ★★★ · 3–1 dá ★★ · 3–2 dá ★')}</div>
        {e >= 3 && Object.keys(r.progresso.descanso).length > 0 && <small className="cn-nota"><Moon size={12} /> {t('Você já gabaritou este rival (★★★): esta partida não acorda seus personagens.')}</small>}
        {e < 3 && <small className="cn-nota"><Moon size={12} /> {t('Aqui o rodízio põe {dormem} personagens para dormir a cada partida, por {partidas} partidas (até {maximo} dormindo).', { dormem: DORMEM_POR_PARTIDA, partidas: DESCANSO.partidas, maximo: DORMEM_NO_MAXIMO })}</small>}
        <Descansando descanso={r.progresso.descanso_rivais[rival.id] ?? {}} titulo={tx('DESCANSANDO DO LADO DELE')} />
        {falta > 0 ? <p className="cn-aviso"><Lock size={14} />{t('A campanha pede {n} personagens na coleção: faltam {falta}.', { n: MINIMO_DA_CAMPANHA, falta })}</p>
          : livres < 9 ? <p className="cn-aviso"><Moon size={14} />{t('Gente demais descansando: espere o rodízio.')}</p>
          : <button className="primary pv-grande cn-desafiar" onClick={onDesafiar}><Swords size={22} />{t('DESAFIAR')}</button>}
      </> : <p className="cn-aviso"><Lock size={14} />{t('Vença {nome} para liberar.', { nome: anterior ? t(anterior.nome) : t('o rival anterior') })}</p>}
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
  const [mostradas, setMostradas] = useState(0);
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  useEffect(() => { if (mostradas >= estrelas) return; const t = window.setTimeout(() => { setMostradas((m) => m + 1); som('pronto'); }, 520); return () => clearTimeout(t); }, [mostradas, estrelas]);
  return <section className={`pv-fim cn-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <small>{t('CAMINHO DO NEXUS')} · {t(rival.titulo).toUpperCase()}</small>
    <h1>{zerouAgora ? t('O NEXUS É SEU!') : ganhei ? t('VITÓRIA!') : t('DERROTA')}</h1>
    <AvatarDoRival rival={rival} tamanho={72} apagado={ganhei} />
    <p className="cn-fala">“{t(ganhei ? rival.perdeu : rival.venceu)}” <small>— {t(rival.nome)}</small></p>
    {ganhei && <div className="cn-fim-estrelas" aria-label={plural(estrelas, '{n} estrela', '{n} estrelas')}>{[1, 2, 3].map((k) => <Star key={k} size={44} className={k <= mostradas ? 'on' : ''} />)}</div>}
    {ganhei && recorde && mostradas >= estrelas && <span className="cn-recorde"><Sparkles size={14} />{t('NOVO RECORDE')}</span>}
    <div className="pv-fim-rodadas">{partida.rodadas.map((x, i) => <span key={i} className={x.vencedor}><b>{i + 1}</b>{x.vencedor === 'eu' ? t('V') : t('D')}</span>)}</div>
    {partida.motivo === 'abandonou' && <small className="cn-nota">{t('Abandonar conta como derrota.')}</small>}

    {zerouAgora && <div className="cn-conquista lenda"><Trophy size={26} /><div><b>{t('CONQUISTADOR DO NEXUS')}</b><small>{t('Você derrotou o Imperador e zerou a campanha!')}</small></div></div>}
    {regiaoNova && !zerouAgora && <div className="cn-conquista"><MapaIcone size={22} /><div><b>{t('REGIÃO CONQUISTADA!')}</b><small>{t('{regiao} é sua.', { regiao: t(regiaoDe(rival).nome) })} {REGIOES[rival.regiao] ? t('Abriu: {regiao}', { regiao: `${REGIOES[rival.regiao]!.icone} ${t(REGIOES[rival.regiao]!.nome)}` }) : ''}</small></div></div>}
    {tituloNovo && <div className="cn-conquista titulo" style={{ '--tc': tituloNovo.cor } as CSSProperties}><Medal size={22} /><div><b>{t('NOVO TÍTULO: {titulo}', { titulo: t(tituloNovo.nome).toUpperCase() })}</b><small>{t('{n} estrelas no caminho', { n: totalAgora })}</small></div></div>}
    {liberouAgora && <button className="cn-liberou" style={{ '--cor': liberouAgora.cor } as CSSProperties} onClick={() => onProximo(liberouAgora)}>
      <AvatarDoRival rival={liberouAgora} tamanho={50} /><span><small>{t('NOVO RIVAL LIBERADO')}</small><b>{t(liberouAgora.nome)}</b><em>{t(liberouAgora.estilo)}</em></span><Play size={20} />
    </button>}
    <Descansando descanso={r.progresso.descanso} titulo={tx('AGORA DESCANSAM')} />
    <div className="pv-fim-botoes"><button className="primary" onClick={onDeNovo}><RotateCcw size={18} />{ganhei && estrelas < 3 ? t('Buscar 3★') : t('Jogar de novo')}</button><button className="secondary" onClick={onMapa}><MapaIcone size={18} />{t('Mapa')}</button></div>
  </section>;
}

/* ---------------------------------------------------------------------------
 * A tela
 * ------------------------------------------------------------------------- */

/* No Caminho do Nexus nem a conta do dono vê as estrelas de força dos times nem tem o "Montar os melhores" (pedido dele): isso é só do treino. */
export default function CaminhoDoNexus(props: Parameters<typeof Caminho>[0]) {
  return <DonoDoPvp.Provider value={false}><Caminho {...props} /></DonoDoPvp.Provider>;
}

function Caminho({ servico, settings, onSettings, onDetails, onLutando, onVoltar }: {
  servico: ServicoDaCampanha; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onLutando: (sim: boolean) => void; onVoltar: () => void;
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
    const a = { estrelas: { ...r.progresso.estrelas } };
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
  const avisoDeErro = erro && <div className="cn-erro" role="alert"><span>{erro}</span><button className="icon-button" onClick={() => setErro('')} aria-label={t('Fechar')}><X size={14} /></button></div>;

  if (!r) return <section className="cn cn-carregando">{erro ? <><p>{erro}</p><button className="secondary" onClick={() => void abrir()}>{t('Tentar de novo')}</button><button className="secondary" onClick={onVoltar}>{t('Voltar')}</button></> : <p className="cm-carregando-tela">{t('Abrindo o Caminho do Nexus…')}</p>}</section>;

  if (tela.tipo === 'montar') {
    const alvo = tela.rival, livres = livresParaJogar(r.colecao, r.progresso.descanso);
    return <>{avisoDeErro}<Montar rival={oponenteDoRival(alvo)} colecao={livres} inicial={meusTimes} ocupado={ocupado} onDetails={onDetails}
      onVoltar={() => setTela({ tipo: 'mapa' })} onPronto={(t) => void comecar(alvo, t)}
      aviso={<Descansando descanso={r.progresso.descanso} titulo={tx('DESCANSANDO (NÃO PODEM JOGAR)')} />} /></>;
  }

  if (partida && rival && tela.tipo !== 'mapa') {
    const op = oponenteDoRival(rival), pvp = comoPvp(partida, vistas), rodada = partida.rodadas[vistas];
    const acabou = partida.estado === 'terminada';
    const aura = rival.aura > 0 && <div className="cn-aura-banner"><Flame size={16} /><b>{t('AURA DO CHEFE')}</b>{t('+{n}% de Vida em todos os personagens de {nome}', { n: Math.round(rival.aura * 100), nome: t(rival.nome) })}</div>;
    const sair = <button className="pv-sair-online" onClick={() => setConfirmar('partida')} disabled={ocupado}><LogOut size={14} />{t('Abandonar partida')}</button>;
    const confirmacao = confirmar && (confirmar === 'luta'
      ? <Confirmar titulo={t('Desistir desta luta?')} texto={t('Você perde esta rodada. A partida continua com os outros times.')} sim={t('Desistir da luta')} onNao={() => setConfirmar(null)} onSim={() => { setConfirmar(null); void render(); }} />
      : <Confirmar titulo={t('Abandonar a partida?')} texto={t('Abandonar conta como derrota contra {nome}.', { nome: t(rival.nome) })} sim={t('Abandonar')} onNao={() => setConfirmar(null)} onSim={() => { setConfirmar(null); void abandonar(); }} />);
    if (tela.tipo === 'apresentar') return <>{avisoDeErro}{aura}<Apresentar rival={op} partida={comoPvp(partida)} onComecar={() => setTela({ tipo: 'escolher' })} /></>;
    if (tela.tipo === 'escolher') return <>{avisoDeErro}{aura}<Escolher key={`${vistas}-${tentativa}`} rival={op} partida={pvp} onEscolher={(i) => void escolher(i)} />{sair}{confirmacao}</>;
    if (tela.tipo === 'vs' && rodada) return <Vs rival={op} partida={comoPvp(partida)} meu={rodada.meu} dele={rodada.dele} onLutar={() => setTela({ tipo: 'luta' })} />;
    if (tela.tipo === 'luta' && rodada) return <>{avisoDeErro}<ArenaDoPvp meu={partida.meus[rodada.meu]!} dele={partida.deles[rodada.dele]!} seed={rodada.seed} rodada={vistas + 1} rival={t(rival.nome)} settings={settings} onSettings={onSettings}
      podePausar velocidadeLivre escala={escalaDoRival(rival)} faixa={faixaDe(rival)} onFim={assistiu} onDesistir={() => setConfirmar('luta')} />{confirmacao}</>;
    if (tela.tipo === 'rodada' && vistas > 0) return <ResultadoDaRodada rival={op} partida={comoPvp(partida, vistas)} final={acabou && vistas >= partida.rodadas.length}
      onSeguir={() => setTela(acabou && vistas >= partida.rodadas.length ? { tipo: 'fim' } : { tipo: 'escolher' })} />;
    if (tela.tipo === 'fim' && acabou) return <Fim rival={rival} partida={partida} antes={antes} r={r} onMapa={() => { setR({ ...r, partida: null }); setTela({ tipo: 'mapa' }); }}
      onDeNovo={() => { setR({ ...r, partida: null }); setTela({ tipo: 'montar', rival }); }} onProximo={irPara} />;
  }

  return <>
    {avisoDeErro}
    <Mapa r={r} onRival={setFicha} onVoltar={onVoltar} />
    {ficha && <Ficha rival={ficha} r={r} onFechar={() => setFicha(null)} onDesafiar={() => { som('ui-arena'); setFicha(null); setTela({ tipo: 'montar', rival: ficha }); }} />}
    {ocupado && <div className="cn-ocupado" aria-hidden="true" />}
  </>;
}
