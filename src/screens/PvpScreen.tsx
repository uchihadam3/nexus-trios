import { createContext, lazy, Suspense, useContext, useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { ArrowDownAZ, ArrowLeft, ArrowRight, Award, Check, Clock, Compass, Medal, Star, Handshake, Info, WifiOff, Globe2, Layers, SlidersHorizontal, Sparkles, Crown, Hourglass, Lock, LogOut, RotateCcw, Search, Shield, Swords, Trophy, Users, Wand2, X, Zap } from 'lucide-react';
import { byId, characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { ArenaDoPvp } from '../components/ArenaDoPvp';
import { combosDoTrio } from '../engine/combos';
import { MINIMO_DA_COLECAO, NPCS, duracaoNaTela, escolhaDoNpc, problemaDosTimes, sementeDaRodada, timesDoNpc, timesLivres, vencedorDaPartida, vitoriasDosTimes,
  type Lado, type NivelNpc, type Npc, type PartidaPvp, type Times } from '../engine/pvp';
import { estrelasDoTime, ESTRELAS_MAXIMAS } from '../presentation/dicas-do-trio';
import { ESTRELAS_DOURADAS, carregarRanking, douradasDaPosicao, textoDaPosicao, usePosicaoDoTrio } from '../presentation/posicao-do-trio';
import { melhorTimeAqui } from '../presentation/melhor-time';
const ESTRELAS = Array.from({ length: ESTRELAS_MAXIMAS }, (_, k) => k + 1);
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { read, save, type Settings } from '../lib/storage';
import { diferencaDoRelogio, textoDoErroPvp, type JogadorPvp, type RankingDoNexus, type RankingPvp, type RespostaPvp, type ServicoDaCampanha, type ServicoPvp, type VistaPvp } from '../lib/pvp-online';
import { corDoNome } from '../lib/comunidade';
import { Avatar } from '../components/AvatarDaComunidade';
import { FAMILIA_DA_IDENTIDADE, ICONE_DA_IDENTIDADE } from '../components/IdentityChips';
import { familiaDaIdentidade, identidadesDe, ordemDasIdentidades, type Identidade } from '../presentation/identities';
import { AvatarDoRival, CartaoDaCampanha, CHAVE_DO_RESUMO, type ResumoDaCampanha } from '../components/CartaoDaCampanha';
import { MINIMO_DA_CAMPANHA, RIVAIS, TOTAL_DE_ESTRELAS, rivalPorId } from '../engine/campanha';
import { EMPRESTADOS_POR_DIA, comEmprestados, diaDoEmprestimo, emprestadosDoDia, faltaParaTrocar } from '../engine/emprestimo';
import { criarCampanhaDemo } from '../lib/campanha-demo';
import '../presentation/pvp.css';
import '../presentation/ui-fx.css';
import { nomeDe, numero, ordinal, plural, t, tx } from '../i18n/idioma';

/*
 * O PvP (pedido do jogador). Esta tela tem o Treino contra os 6 NPCs, do Iniciante à Lenda (src/engine/pvp.ts):
 *  1. escolher o NPC (cada um com rating, coleção e o seu placar contra ele);
 *  2. montar 3 times de 3 com a sua coleção (os personagens liberados nas Conquistas), num álbum de cartas;
 *  3. ver os 3 times dos dois lados;
 *  4. a cada rodada, escolher em segredo um time seu (o NPC escolhe o dele), o VS, e a luta (contra pessoas sempre em 3×; no treino, na velocidade do jogador);
 *  5. o time que vence fica marcado; vence a partida quem ganhar com os 3 times.
 * Treino não conta para o ranking nem para o rating: só o placar contra cada NPC, guardado no aparelho.
 * O Desafio online (outra pessoa, PartidaOnline) usa estas mesmas telas; quem manda é o servidor (src/lib/pvp-online.ts).
 */

interface Guardado { treino: Record<string, { v: number; d: number }>; times?: string[][] }
const carregar = (): Guardado => {
  const g = read('pvp') as Guardado | null;
  return { treino: g && typeof g.treino === 'object' && g.treino ? g.treino : {}, times: Array.isArray(g?.times) ? g!.times : undefined };
};
/** Os efeitos de interface desenhados em Python (tools/ui/generate_ui_fx.py): choque, holofote, raios, faíscas. */
export const Fx = ({ nome, cor, ms, className, laco = true }: { nome: string; cor: string; ms: number; className: string; laco?: boolean }) =>
  <span aria-hidden className={`uifx ${laco ? 'uifx-laco' : ''} ${className}`} style={{ '--uifx-img': `url(/assets/ui/fx/${nome}.webp)`, '--uifx-cor': cor, '--uifx-dur': `${ms}ms` } as CSSProperties} />;
export const som = (nome: 'toque' | 'pronto' | 'ui-confirma' | 'ui-arena' | 'vitoria' | 'derrota') => battleAudio.sound(nome, PRIORIDADE.interface);


type Etapa =
  | { tipo: 'lobby' }
  | { tipo: 'campanha' }
  | { tipo: 'montar'; npc: Npc }
  | { tipo: 'apresentar'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'escolher'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'vs'; npc: Npc; partida: PartidaPvp; meu: number; dele: number }
  | { tipo: 'luta'; npc: Npc; partida: PartidaPvp; meu: number; dele: number; retomar?: number }
  | { tipo: 'rodada'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'fim'; npc: Npc; partida: PartidaPvp };

/*
 * O treino guardado no aparelho a cada passo (pedido do jogador: saiu, o jogo atualizou ou fechou no meio, "você
 * clica lá no PvP e continua do mesmo lugar"). A luta volta no mesmo ponto, pausada.
 */
const CHAVE_DO_TREINO = 'pvp-treino-atual';
type Salvo = { tipo: Etapa['tipo']; npc: string; partida?: PartidaPvp; meu?: number; dele?: number; segundos?: number };
const CHAVE_DA_CAMPANHA = 'pvp-na-campanha';
const etapaSalva = (): Etapa => {
  if (read(CHAVE_DA_CAMPANHA) === true) return { tipo: 'campanha' };
  const x = read(CHAVE_DO_TREINO) as Salvo | null, npc = x && NPCS.find((n) => n.id === x.npc);
  if (!x || !npc || x.tipo === 'lobby') return { tipo: 'lobby' };
  if (x.tipo === 'montar') return { tipo: 'montar', npc };
  const p = x.partida;
  if (!p || !Array.isArray(p.meus) || !Array.isArray(p.deles) || !Array.isArray(p.rodadas)) return { tipo: 'lobby' };
  if (x.tipo === 'vs' || x.tipo === 'luta') {
    if (typeof x.meu !== 'number' || typeof x.dele !== 'number') return { tipo: 'escolher', npc, partida: p };
    return x.tipo === 'luta' ? { tipo: 'luta', npc, partida: p, meu: x.meu, dele: x.dele, retomar: Math.max(0, x.segundos ?? 0) } : { tipo: 'vs', npc, partida: p, meu: x.meu, dele: x.dele };
  }
  return { tipo: x.tipo, npc, partida: p } as Etapa;
};
const guardaEtapa = (e: Etapa, segundos?: number) => {
  save(CHAVE_DA_CAMPANHA, e.tipo === 'campanha' ? true : null);
  if (e.tipo === 'lobby' || e.tipo === 'campanha') { save(CHAVE_DO_TREINO, null); return; }
  const { npc, ...resto } = e as Exclude<Etapa, { tipo: 'lobby' } | { tipo: 'campanha' }>;
  const seg = segundos ?? (e.tipo === 'luta' ? e.retomar : undefined);
  save(CHAVE_DO_TREINO, { ...resto, npc: npc.id, ...(seg !== undefined ? { segundos: seg } : {}) });
};

/* ---------------------------------------------------------------------------
 * Peças
 * ------------------------------------------------------------------------- */

/*
 * A ficha do personagem em todo o PvP (pedido do jogador: "tem que ter alguma forma de ver a ficha dos personagens"):
 * tocar num rosto abre a ficha por cima da tela. Onde o toque já faz outra coisa (escolher o time, tirar do time), o
 * rosto não abre (`ficha={false}`); no álbum de montar há o botão ⓘ.
 */
export const FichaDoPvp = createContext<((id: string) => void) | null>(null);
export function Rosto({ id, tamanho = 54, apagado = false, ficha = true }: { id: string; tamanho?: number; apagado?: boolean; ficha?: boolean }) {
  const c = byId[id]!, abrir = useContext(FichaDoPvp), abre = ficha && abrir;
  return <span className={`pv-rosto ${apagado ? 'apagado' : ''} ${abre ? 'com-ficha' : ''}`} style={{ '--character': c.color, '--t': `${tamanho}px` } as CSSProperties} title={abre ? t('{nome}: toque para ver a ficha', { nome: nomeDe(c) }) : nomeDe(c)}
    {...(abre ? { role: 'button', tabIndex: 0, 'aria-label': t('Ficha de {nome}', { nome: nomeDe(c) }), onClick: (e: { stopPropagation: () => void }) => { e.stopPropagation(); abrir(id); }, onKeyDown: (e: { key: string }) => { if (e.key === 'Enter') abrir(id); } } : {})}><Portrait character={c} /></span>;
}

/*
 * A conta do dono (pedido dele): só ela vê as estrelas de força dos times e a posição do trio, e só no treino
 * contra os NPCs (no PvP com outras pessoas e no Caminho do Nexus, nem ela). Para os outros, em nenhum lugar do PvP.
 */
export const DonoDoPvp = createContext(false);
/*
 * A posição exata do time entre todos os trios (src/presentation/posicao-do-trio.ts). A porcentagem "melhor que X%"
 * saiu (pedido do dono: "deixar só as estrelas e a posição").
 */
function PosicaoDoTime({ time, curta = false }: { time: readonly string[]; curta?: boolean }) {
  const lugar = usePosicaoDoTrio(time);
  if (!lugar) return null;
  const titulo = t('{lugar} de {total} trios', { lugar: ordinal(lugar.posicao), total: lugar.total });
  return curta
    ? <em className="pv-pct" title={titulo}><span className="pv-lugar">#{numero(lugar.posicao)}</span></em>
    : <span className="pv-pct" title={titulo}><span className="pv-lugar">{textoDaPosicao(lugar.posicao)}</span></span>;
}

/* No 1% do topo, de 1 a 7 estrelas douradas depois das 7 de prata (src/presentation/posicao-do-trio.ts). */
function Douradas({ time }: { time: readonly string[] }) {
  const lugar = usePosicaoDoTrio(time), ouro = lugar ? douradasDaPosicao(lugar.posicao, lugar.total) : 0;
  return ouro > 0 ? <span className="pv-ouro" aria-label={plural(ouro, '{n} estrela dourada', '{n} estrelas douradas')}>{Array.from({ length: ESTRELAS_DOURADAS }, (_, k) => <i key={k} className={k < ouro ? 'on' : ''}>★</i>)}</span> : null;
}

function CartaoDoTime({ time, i, lado, venceu, escolhido, bloqueado, onClick, compacto = false }: {
  time: readonly string[]; i: number; lado: Lado; venceu?: boolean; escolhido?: boolean; bloqueado?: boolean; onClick?: () => void; compacto?: boolean;
}) {
  const estrelas = estrelasDoTime(time), combos = combosDoTrio(time).combos.length, dono = useContext(DonoDoPvp);
  const Tag = onClick ? 'button' : 'div';
  return <Tag className={`pv-time ${lado} ${venceu ? 'venceu' : ''} ${escolhido ? 'escolhido' : ''} ${bloqueado ? 'bloqueado' : ''} ${compacto ? 'compacto' : ''}`}
    onClick={onClick} disabled={onClick ? bloqueado : undefined} style={{ '--i': i } as CSSProperties}>
    <span className="pv-time-topo"><b>{t('TIME {n}', { n: i + 1 })}</b>{venceu && <em className="pv-selo-venceu"><Trophy size={12} />{t('VENCEU')}</em>}</span>
    <span className="pv-time-rostos">{time.map((id) => <Rosto key={id} id={id} tamanho={compacto ? 40 : 52} ficha={!onClick} />)}</span>
    {!compacto && <span className="pv-time-nomes">{time.map((id) => nomeDe(byId[id]!)).join(' · ')}</span>}
    <span className="pv-time-info">
      {dono && <span className="pv-estrelas" aria-label={t('Força {n} de {max}', { n: estrelas, max: ESTRELAS_MAXIMAS })}>{ESTRELAS.map((k) => <i key={k} className={k <= estrelas ? 'on' : ''}>★</i>)}<Douradas time={time} /></span>}
      {dono && <PosicaoDoTime time={time} />}
      {combos > 0 && <span className="pv-combos"><Zap size={11} />{plural(combos, '{n} combo', '{n} combos')}</span>}
    </span>
    {venceu && <span className="pv-carimbo" aria-hidden="true"><Check size={34} /></span>}
  </Tag>;
}

function Placar({ partida, rival }: { partida: Pick<PartidaPvp, 'rodadas'>; rival: Oponente }) {
  const v = vitoriasDosTimes(partida);
  return <div className="pv-placar">
    <span className="pv-placar-lado eu"><b>{t('VOCÊ')}</b><span>{v.eu.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
    <span className="pv-placar-meio"><small>{t('RODADA')}</small><b>{partida.rodadas.length + 1}</b></span>
    <span className="pv-placar-lado rival" style={{ '--npc': rival.cor } as CSSProperties}><b>{rival.nome.split(' ')[0]!.toUpperCase()}</b><span>{v.rival.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
  </div>;
}

function AvatarDoNpc({ npc, tamanho = 64 }: { npc: Npc; tamanho?: number }) {
  return <span className="pv-npc-avatar" style={{ '--npc': npc.cor, '--t': `${tamanho}px` } as CSSProperties}><Portrait character={byId[npc.avatar]!} /><i>{npc.nivel}</i></span>;
}
/** Quem está do outro lado: um NPC do treino ou uma pessoa (online). As telas da partida são as mesmas. */
export interface Oponente { nome: string; cor: string; avatar: (tamanho: number) => ReactNode; fala?: string }
const oponenteDoNpc = (n: Npc): Oponente => ({ nome: t(n.nome), cor: n.cor, avatar: (tam) => <AvatarDoNpc npc={n} tamanho={tam} />, fala: t(n.fala) });

/* ---------------------------------------------------------------------------
 * 1. O lobby
 * ------------------------------------------------------------------------- */

/*
 * O lobby do PvP em abas (pedido do dono: "tá tudo muito vertical, muito scroll… separar o rank do Nexus do PvP, bem
 * gamificado"): Nexus, Online, Treino e Ranking, cada uma cabendo numa tela. A aba fica lembrada.
 */
type AbaDoLobby = 'nexus' | 'online' | 'treino' | 'ranking';
const CHAVE_DA_ABA = 'pvp-aba';
const ABAS: readonly { id: AbaDoLobby; nome: string; icone: ReactNode }[] = [
  { id: 'nexus', nome: tx('Nexus'), icone: <Compass size={19} /> },
  { id: 'online', nome: tx('Online'), icone: <Globe2 size={19} /> },
  { id: 'treino', nome: tx('Treino'), icone: <Shield size={19} /> },
  { id: 'ranking', nome: tx('Ranking'), icone: <Trophy size={19} /> },
];

function Lobby({ colecao, propria, guardado, onTreino, onJogar, online, onCampanha, temCampanha, servicoDaCampanha }: { colecao: string[]; propria: string[]; guardado: Guardado; onTreino: (n: Npc) => void; onJogar: () => void; online?: Online | null; onCampanha: () => void; temCampanha: boolean; servicoDaCampanha: ServicoDaCampanha | null }) {
  const falta = Math.max(0, MINIMO_DA_COLECAO - colecao.length);
  const [aba, setAba] = useState<AbaDoLobby>(() => { const a = read(CHAVE_DA_ABA); return ABAS.some((x) => x.id === a) ? a as AbaDoLobby : 'nexus'; });
  const [qualRanking, setQualRanking] = useState<'nexus' | 'pvp'>('nexus');
  const trocar = (a: AbaDoLobby) => { if (a === aba) return; som('toque'); setAba(a); save(CHAVE_DA_ABA, a); };
  // o ranking do PvP (rating) e o do Nexus (estrelas), pedidos uma vez
  const [rank, setRank] = useState<RankingPvp | null>(null), [erroRank, setErroRank] = useState('');
  const [nexus, setNexus] = useState<RankingDoNexus | null>(null), [erroNexus, setErroNexus] = useState('');
  useEffect(() => {
    let vivo = true;
    if (online) void online.servico.ranking().then((r) => { if (vivo) setRank(r); }).catch((e) => { if (vivo) setErroRank(textoDoErroPvp(e)); });
    if (servicoDaCampanha) void servicoDaCampanha.ranking().then((r) => { if (vivo) setNexus(r); }).catch((e) => { if (vivo) setErroNexus(textoDoErroPvp(e)); });
    return () => { vivo = false; };
  }, [online?.servico, servicoDaCampanha]);
  const resumo = read(CHAVE_DO_RESUMO) as ResumoDaCampanha | null;
  const verRanking = (qual: 'nexus' | 'pvp') => { setQualRanking(qual); trocar('ranking'); };
  return <section className="pv-lobby pv-lobby2">
    <header className="pv-topo pv-topo-curto">
      <Fx nome="holofote" cor="#ffd36b" ms={5200} className="pv-fx-holofote" />
      <span className="pv-logo"><Swords size={24} /></span>
      <div><h1>{t('ARENA PvP')}</h1><p>{t('3 times de 3 · escolha secreta')}</p></div>
      <span className="pv-topo-chips">
        <button className="pv-chip-placar nexus" title={t('Suas estrelas no Caminho do Nexus')} onClick={() => verRanking('nexus')}><Star size={13} /><b>{resumo?.estrelas ?? 0}</b><small>/{TOTAL_DE_ESTRELAS}</small></button>
        {online && <button className="pv-chip-placar pvp" title={t('Seu rating do PvP')} onClick={() => verRanking('pvp')}><Crown size={13} /><b>{rank?.eu.rating ?? '—'}</b></button>}
      </span>
    </header>

    {falta > 0 && <div className="pv-trava">
      <Lock size={26} />
      <div><b>{t('Faltam {n} personagens na sua coleção', { n: falta })}</b><small>{t('O PvP pede {n} personagens (3 times de 3). Termine as 10 lutas de uma jornada para liberar o seu trio nas Conquistas.', { n: MINIMO_DA_COLECAO })}</small>
        <span className="pv-trava-barra"><i style={{ width: `${(100 * colecao.length) / MINIMO_DA_COLECAO}%` }} /></span><em>{colecao.length}/{MINIMO_DA_COLECAO}</em></div>
      <button className="primary" onClick={onJogar}>{t('Jogar')}</button>
    </div>}

    <nav className="pv-abas" role="tablist" aria-label={t('Modos do PvP')}>
      {ABAS.map((a) => <button key={a.id} role="tab" aria-selected={aba === a.id} className={aba === a.id ? 'ativa' : ''} onClick={() => trocar(a.id)}>{a.icone}<b>{t(a.nome)}</b></button>)}
    </nav>

    <div className="pv-aba" key={aba} role="tabpanel">
      {aba === 'nexus' && <>
        {/* a campanha contra os 40 rivais (src/screens/CaminhoDoNexus.tsx): pede a conta e só vale a coleção, sem empréstimo */}
        <CartaoDaCampanha podeJogar={temCampanha && propria.length >= MINIMO_DA_CAMPANHA} onAbrir={onCampanha}
          motivo={!temCampanha ? t('Entre na sua conta para jogar a campanha.') : t('A campanha pede {n} personagens na coleção (você tem {tem}).', { n: MINIMO_DA_CAMPANHA, tem: propria.length })} />
        <ResumoDoNexus resumo={resumo} />
        <PodioCurto titulo={t('RANKING DO NEXUS')} icone={<Star size={14} />} erro={erroNexus} carregando={!!servicoDaCampanha && !nexus && !erroNexus}
          linhas={(nexus?.ranking ?? []).slice(0, 3).map((l) => ({ id: l.id, nome: l.nome, valor: <><Star size={11} />{l.estrelas}</>, sub: t(l.titulo) }))}
          eu={nexus?.eu ? t('Você: {pos} · {n}★', { pos: ordinal(nexus.eu.posicao), n: nexus.eu.estrelas }) : null} onVer={() => verRanking('nexus')} />
      </>}
      {aba === 'online' && <>
        {online ? <CartaoOnline online={online} rank={rank} /> : <div className="pv-modo online">
          <span className="pv-modo-icone"><Users size={24} /></span>
          <div><b>{t('DESAFIO ONLINE')}</b><small>{t('Entre na sua conta para desafiar alguém pela Comunidade e subir no ranking.')}</small></div>
          <em className="pv-em-breve"><Lock size={11} />{t('com conta')}</em>
        </div>}
        {online && <PodioCurto titulo={t('RANKING PvP')} icone={<Crown size={14} />} erro={erroRank} carregando={!rank && !erroRank}
          linhas={(rank?.ranking ?? []).slice(0, 3).map((l) => ({ id: l.id, nome: l.nome, valor: <><Crown size={11} />{l.rating}</>, sub: t('{v}V {d}D', { v: l.vitorias, d: l.derrotas }) }))}
          eu={null} onVer={() => verRanking('pvp')} />}
        <CartaoDoEmprestimo propria={propria} />
      </>}
      {aba === 'treino' && <>
        <p className="pv-aba-dica"><Shield size={13} />{t('Contra os {n} NPCs, do Iniciante à Lenda. Não conta para nenhum ranking.', { n: NPCS.length })}</p>
        <div className="pv-npcs curtos">
          {NPCS.map((n, i) => {
            const p = guardado.treino[n.id] ?? { v: 0, d: 0 };
            return <button key={n.id} className="pv-npc" disabled={falta > 0} onClick={() => onTreino(n)} style={{ '--npc': n.cor, '--i': i } as CSSProperties} title={`“${t(n.fala)}”`}>
              <AvatarDoNpc npc={n} tamanho={50} />
              <span className="pv-npc-texto">
                <small>{t(n.titulo).toUpperCase()}</small><b>{t(n.nome)}</b>
                <span className="pv-npc-linha"><span className="pv-rating"><Crown size={12} />{n.rating}</span><span className="pv-colecao">{t('{n} personagens', { n: n.colecao })}</span></span>
              </span>
              <span className="pv-npc-placar"><span><b className="v">{t('{n}V', { n: p.v })}</b> <b className="d">{t('{n}D', { n: p.d })}</b></span><span className="pv-caveiras" aria-label={t('Dificuldade {n} de {max}', { n: n.nivel, max: NPCS.length })}>{NPCS.map((_, k0) => k0 + 1).map((k) => <i key={k} className={k <= n.nivel ? 'on' : ''} />)}</span></span>
            </button>;
          })}
        </div>
        <CartaoDoEmprestimo propria={propria} />
      </>}
      {aba === 'ranking' && <>
        <div className="pv-subabas" role="tablist" aria-label={t('Qual ranking')}>
          <button role="tab" aria-selected={qualRanking === 'nexus'} className={qualRanking === 'nexus' ? 'ativa nexus' : 'nexus'} onClick={() => { som('toque'); setQualRanking('nexus'); }}><Star size={15} />NEXUS<small>{t('estrelas')}</small></button>
          <button role="tab" aria-selected={qualRanking === 'pvp'} className={qualRanking === 'pvp' ? 'ativa pvp' : 'pvp'} onClick={() => { som('toque'); setQualRanking('pvp'); }}><Crown size={15} />PvP<small>{t('rating')}</small></button>
        </div>
        {qualRanking === 'nexus'
          ? <RankingCompleto erro={erroNexus} carregando={!!servicoDaCampanha && !nexus && !erroNexus} semConta={!servicoDaCampanha}
              vazio={t('Ninguém jogou o Caminho do Nexus ainda. O primeiro lugar está livre!')}
              contexto={<><Star size={13} /> {t('Caminho do Nexus · mais estrelas na frente; empate, quem usou menos partidas')}{nexus ? ` · ${t('{n} jogadores', { n: nexus.total })}` : ''}</>}
              linhas={(nexus?.ranking ?? []).map((l) => ({ posicao: l.posicao, id: l.id, nome: l.nome, valor: l.estrelas, de: t('de {n}★', { n: TOTAL_DE_ESTRELAS }), sub: `${t(l.titulo)} · ${t('{n} partidas', { n: l.partidas })}`, barra: (100 * l.estrelas) / TOTAL_DE_ESTRELAS, minha: l.id === nexus?.eu?.id }))}
              eu={nexus?.eu ? { posicao: nexus.eu.posicao, id: nexus.eu.id, nome: nexus.eu.nome, valor: nexus.eu.estrelas, de: t('de {n}★', { n: TOTAL_DE_ESTRELAS }), sub: `${t(nexus.eu.titulo)} · ${t('{n} partidas', { n: nexus.eu.partidas })}`, barra: (100 * nexus.eu.estrelas) / TOTAL_DE_ESTRELAS, minha: true } : null} />
          : <RankingCompleto erro={erroRank} carregando={!!online && !rank && !erroRank} semConta={!online}
              vazio={t('Ninguém jogou contra outra pessoa ainda. O primeiro lugar está livre!')}
              contexto={<><Crown size={13} /> {t('PvP contra pessoas · maior rating na frente')}{rank ? ` · ${t('seu rating: {r} ({v}V {d}D)', { r: rank.eu.rating, v: rank.eu.vitorias, d: rank.eu.derrotas })}` : ''}</>}
              linhas={(rank?.ranking ?? []).map((l) => ({ posicao: l.posicao, id: l.id, nome: l.nome, valor: l.rating, de: t('rating'), sub: t('{v}V {d}D', { v: l.vitorias, d: l.derrotas }), minha: l.id === rank?.eu.id }))}
              eu={rank?.eu.posicao ? (({ id, posicao }) => { const l = rank.ranking.find((x) => x.id === id); return l ? { posicao, id, nome: l.nome, valor: l.rating, de: t('rating'), sub: t('{v}V {d}D', { v: l.vitorias, d: l.derrotas }), minha: true } : null; })({ id: rank.eu.id!, posicao: rank.eu.posicao }) : null} />}
      </>}
    </div>
  </section>;
}

/** O resumo do Caminho do Nexus (guardado pela tela da campanha): estrelas, título e o próximo rival. */
function ResumoDoNexus({ resumo }: { resumo: ResumoDaCampanha | null }) {
  const proximo = resumo?.proximo ? rivalPorId(resumo.proximo) : RIVAIS[0]!, estrelas = resumo?.estrelas ?? 0;
  return <div className="pv-resumo-nexus">
    <span><small>{t('ESTRELAS')}</small><b><Star size={14} />{estrelas}<i>/{TOTAL_DE_ESTRELAS}</i></b><span className="pv-barrinha"><i style={{ width: `${(100 * estrelas) / TOTAL_DE_ESTRELAS}%` }} /></span></span>
    <span><small>{t('TÍTULO')}</small><b>{resumo?.titulo ? t(resumo.titulo) : t('Aprendiz')}</b></span>
    <span><small>{resumo?.zerou ? t('CAMINHO') : t('PRÓXIMO')}</small>{resumo?.zerou ? <b>{t('Zerado!')}</b> : proximo ? <b className="pv-resumo-rival"><AvatarDoRival rival={proximo} tamanho={22} />{t(proximo.nome)}</b> : <b>—</b>}</span>
  </div>;
}

type LinhaCurta = { id: string; nome: string; valor: ReactNode; sub: string };
/** Os 3 primeiros de um ranking, num pódio pequeno, e o botão para ver o ranking inteiro (na aba Ranking). */
function PodioCurto({ titulo, icone, linhas, erro, carregando, eu, onVer }: { titulo: string; icone: ReactNode; linhas: LinhaCurta[]; erro: string; carregando: boolean; eu: string | null; onVer: () => void }) {
  return <div className="pv-podio-curto">
    <header><b>{icone}{titulo}</b><button onClick={onVer}>{t('ver tudo')} <ArrowRight size={13} /></button></header>
    {erro ? <small className="pv-problema">{erro}</small> : carregando ? <small className="pv-vazio">{t('Carregando…')}</small> : !linhas.length ? <small className="pv-vazio">{t('Ninguém ainda. Seja o primeiro!')}</small>
      : <ol>{[linhas[1], linhas[0], linhas[2]].map((l, k) => l && <li key={l.id} className={`p${k === 1 ? 1 : k === 0 ? 2 : 3}`}>
        <Avatar id={l.id} nome={l.nome} tamanho={k === 1 ? 40 : 32} online={false} /><b>{l.nome}</b><em>{l.valor}</em><i>{k === 1 ? 1 : k === 0 ? 2 : 3}</i>
      </li>)}</ol>}
    {eu && <small className="pv-podio-eu">{eu}</small>}
  </div>;
}

type LinhaDoRanking = { posicao: number; id: string; nome: string; valor: ReactNode; de: string; sub: string; barra?: number; minha: boolean };
/*
 * Um ranking inteiro (Nexus ou PvP), com o mesmo visual do Ranking de fora (pedido do dono: "igualzinho, com pódio"):
 * a sua posição em cima, o pódio dos 3 com coroa e degraus, e a lista.
 */
function RankingCompleto({ linhas, eu, erro, carregando, semConta, vazio, contexto }: { linhas: LinhaDoRanking[]; eu: LinhaDoRanking | null; erro: string; carregando: boolean; semConta: boolean; vazio: string; contexto: ReactNode }) {
  if (semConta) return <p className="pv-vazio pv-ranking-aviso"><Lock size={14} />{t('Entre na sua conta para ver o ranking.')}</p>;
  if (erro) return <p className="pv-problema">{erro}</p>;
  if (carregando) return <div className="rk-carregando" aria-label={t('Carregando o ranking')}>{[0, 1, 2, 3].map((i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</div>;
  if (!linhas.length) return <p className="rk-vazio">{vazio}</p>;
  const podio = linhas.slice(0, 3), resto = linhas.slice(3);
  const total = (l: LinhaDoRanking) => <span className="rk-cq-total"><b>{l.valor}</b><small>{l.de}</small></span>;
  const linha = (l: LinhaDoRanking, i: number) => <button key={l.id} type="button" className={`rk-cq-linha pv-rk-linha ${l.minha ? 'mine' : ''}`} style={{ '--i': Math.min(i, 12) } as CSSProperties}>
    <span className="rk-pos">{l.posicao}</span>
    <span className="rk-quem"><b>{l.nome}</b><small>{l.sub}</small>{l.barra !== undefined && <span className="rk-cq-barra"><i style={{ width: `${l.barra}%` }} /></span>}</span>
    {total(l)}
  </button>;
  return <div className="pv-rk">
    <p className="rk-contexto">{contexto}</p>
    {eu && <div className="rk-meus"><span className="rk-meus-rotulo"><Award size={14} />{t('MINHA POSIÇÃO')}</span><div className="rk-lista" style={{ marginTop: 8 }}>{linha(eu, 0)}</div></div>}
    <div className="rk-podio">{[podio[1], podio[0], podio[2]].map((l, i) => l && <div key={l.id} className={`rk-degrau p${l.posicao} ${l.minha ? 'mine' : ''}`} style={{ '--i': i } as CSSProperties}>
      <span className="rk-coroa">{l.posicao === 1 ? <Crown size={22} /> : <Medal size={18} />}</span>
      <Avatar id={l.id} nome={l.nome} tamanho={l.posicao === 1 ? 50 : 40} online={false} />
      <b className="rk-nome">{l.nome}</b>
      {total(l)}
      <span className="rk-base">{l.posicao}</span>
    </div>)}</div>
    {resto.length > 0 && <div className="rk-lista">{resto.map(linha)}</div>}
  </div>;
}


/**
 * O Empréstimo do dia (src/engine/emprestimo.ts): os 9 personagens que todo mundo ganha hoje no PvP, a contagem até a
 * troca e o selo de quem é novo para você (quem você já tem não muda nada: o personagem é um só).
 */
const doisDigitos = (n: number) => String(n).padStart(2, '0');
function CartaoDoEmprestimo({ propria }: { propria: string[] }) {
  const agora = useAgora(true, 1000), dia = diaDoEmprestimo(agora), ids = useMemo(() => emprestadosDoDia(dia), [dia]);
  const minha = useMemo(() => new Set(propria), [propria]), novos = ids.filter((id) => !minha.has(id)).length;
  const falta = Math.floor(faltaParaTrocar(agora) / 1000);
  return <section className="pv-emprestimo curto" aria-label={t('Empréstimo do dia')} title={t('{n} personagens sorteados todo dia, os mesmos para todo mundo, para combinar com a sua coleção no Treino e no Desafio online. Amanhã vêm outros.', { n: EMPRESTADOS_POR_DIA })}>
    <header>
      <span className="pv-emprestimo-icone"><Handshake size={18} /></span>
      <div><small>{t('EMPRÉSTIMO DO DIA')}</small><b>{novos > 0 ? t('+{n} personagens hoje', { n: novos }) : t('Você já tem os 9 de hoje!')}</b></div>
      <span className="pv-emprestimo-relogio" title={t('Troca à meia-noite (Brasília)')}><Clock size={12} />{doisDigitos(Math.floor(falta / 3600))}:{doisDigitos(Math.floor((falta % 3600) / 60))}:{doisDigitos(falta % 60)}</span>
    </header>
    <div className="pv-emprestimo-faixa">
      {ids.map((id, k) => { const c = byId[id]!, ja = minha.has(id);
        return <span key={id} className={`pv-emprestado ${ja ? 'ja' : 'novo'}`} style={{ '--character': c.color, '--k': k } as CSSProperties} title={`${nomeDe(c)} · ${ja ? t('já é seu') : t('novo pra você')}`}>
          <Rosto id={id} tamanho={40} apagado={ja} />{!ja && <em>{t('NOVO')}</em>}
        </span>; })}
    </div>
  </section>;
}

/**
 * "Montar ao acaso": 9 personagens sorteados da coleção, 100% ao acaso (pedido do jogador: "não vê se é bom, se é
 * ruim, é só aleatório"). A cada toque sai outro jeito.
 */
function timesAoAcaso(colecao: string[]): string[][] | null {
  if (colecao.length < MINIMO_DA_COLECAO) return null;
  const p = [...colecao], todos: string[] = [];
  while (todos.length < 9) todos.push(p.splice(Math.floor(Math.random() * p.length), 1)[0]!);
  return [todos.slice(0, 3), todos.slice(3, 6), todos.slice(6, 9)];
}


/* ---------------------------------------------------------------------------
 * Os filtros do álbum: universo, função (as etiquetas do Draft) e a ordem
 * ------------------------------------------------------------------------- */

type Ordem = 'nome' | 'universo' | 'funcao';
interface Filtro { ordem: Ordem; universos: string[]; funcoes: Identidade[]; esconderUsados: boolean }
const FILTRO_VAZIO: Filtro = { ordem: 'nome', universos: [], funcoes: [], esconderUsados: false };
const semAcento = (t: string) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

function filtrar(colecao: string[], busca: string, f: Filtro) {
  const q = semAcento(busca.trim());
  return colecao.map((id) => byId[id]!).filter((c) =>
    (!q || semAcento(c.name).includes(q) || semAcento(nomeDe(c)).includes(q) || semAcento(c.universe).includes(q) || semAcento(t(c.universe)).includes(q))
    && (!f.universos.length || f.universos.includes(c.universe))
    && (!f.funcoes.length || f.funcoes.every((x) => identidadesDe(c).includes(x))));
}
type Personagem = (typeof characters)[number];
function agrupar(lista: Personagem[], ordem: Ordem): { titulo: string; lista: Personagem[] }[] {
  const porNome = [...lista].sort((a, b) => nomeDe(a).localeCompare(nomeDe(b)));
  if (ordem === 'nome') return [{ titulo: '', lista: porNome }];
  const mapa = new Map<string, Personagem[]>();
  for (const c of porNome) {
    const chave = ordem === 'universo' ? c.universe : (ordemDasIdentidades.find((x) => identidadesDe(c).includes(x)) ?? tx('Outros'));
    mapa.set(chave, [...(mapa.get(chave) ?? []), c]);
  }
  const chaves = [...mapa.keys()].sort((a, b) => ordem === 'universo' ? a.localeCompare(b) : ordemDasIdentidades.indexOf(a as Identidade) - ordemDasIdentidades.indexOf(b as Identidade));
  return chaves.map((k) => ({ titulo: k, lista: mapa.get(k)! }));
}

function PainelDeFiltros({ colecao, filtro, total, onFiltro, onFechar }: { colecao: string[]; filtro: Filtro; total: number; onFiltro: (f: Filtro) => void; onFechar: () => void }) {
  const [buscaUni, setBuscaUni] = useState('');
  const [todosUni, setTodosUni] = useState(false);
  const universos = useMemo(() => {
    const n = new Map<string, number>();
    for (const id of colecao) { const u = byId[id]!.universe; n.set(u, (n.get(u) ?? 0) + 1); }
    return [...n.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  }, [colecao]);
  const funcoes = useMemo(() => {
    const n = new Map<Identidade, number>();
    for (const id of colecao) for (const x of identidadesDe(id)) n.set(x, (n.get(x) ?? 0) + 1);
    return n;
  }, [colecao]);
  const q = semAcento(buscaUni.trim());
  const unisVisiveis = universos.filter(([u]) => !q || semAcento(u).includes(q) || semAcento(t(u)).includes(q));
  const mostrados = todosUni || q ? unisVisiveis : unisVisiveis.slice(0, 18);
  const alterna = <T,>(lista: T[], x: T) => (lista.includes(x) ? lista.filter((y) => y !== x) : [...lista, x]);
  const ativos = filtro.universos.length + filtro.funcoes.length + (filtro.esconderUsados ? 1 : 0);
  const familias = Object.keys(FAMILIA_DA_IDENTIDADE) as (keyof typeof FAMILIA_DA_IDENTIDADE)[];
  // por cima da tela onde o jogador está (a tela anima com transform, e um fixed dentro dela ia parar no fim da página)
  return createPortal(<div className="pv-painel-fundo" onClick={(e) => { if (e.target === e.currentTarget) onFechar(); }}>
    <section className="pv-painel" role="dialog" aria-label={t('Filtros')}>
      <span className="pv-painel-alca" aria-hidden="true" />
      <header><SlidersHorizontal size={20} /><b>{t('Filtros')}</b>{ativos > 0 && <button className="pv-painel-limpar" onClick={() => onFiltro(FILTRO_VAZIO)}>{t('Limpar tudo')}</button>}<button className="icon-button" onClick={onFechar} aria-label={t('Fechar')}><X size={18} /></button></header>

      <h4><ArrowDownAZ size={14} />{t('ORGANIZAR POR')}</h4>
      <div className="pv-ordem">
        {([['nome', tx('Nome'), ArrowDownAZ], ['universo', tx('Universo'), Globe2], ['funcao', tx('Função'), Layers]] as const).map(([v, nome, Icone]) =>
          <button key={v} className={filtro.ordem === v ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, ordem: v }); som('toque'); }}><Icone size={18} />{t(nome)}</button>)}
      </div>
      <label className="pv-livres"><input type="checkbox" checked={filtro.esconderUsados} onChange={(e) => onFiltro({ ...filtro, esconderUsados: e.target.checked })} /><span className="pv-chave" aria-hidden="true" />{t('Esconder quem já está num time')}</label>

      <h4><Sparkles size={14} />{t('FUNÇÃO')} <small>{t('o que ele faz na luta')}</small></h4>
      {familias.map((fam) => {
        const lista = ordemDasIdentidades.filter((x) => familiaDaIdentidade[x] === fam && funcoes.has(x));
        if (!lista.length) return null;
        const { nome, cor } = FAMILIA_DA_IDENTIDADE[fam];
        return <div key={fam} className="pv-familia" style={{ '--cor': cor } as CSSProperties}>
          <small>{t(nome)}</small>
          <div className="pv-chips">{lista.map((x) => { const Icone = ICONE_DA_IDENTIDADE[x]; const on = filtro.funcoes.includes(x);
            return <button key={x} className={on ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, funcoes: alterna(filtro.funcoes, x) }); som('toque'); }}><Icone size={14} />{t(x)}<i>{funcoes.get(x)}</i></button>; })}</div>
        </div>;
      })}

      <h4><Globe2 size={14} />{t('UNIVERSO')} <small>{t('{n} na sua coleção', { n: universos.length })}</small></h4>
      {universos.length > 10 && <label className="pv-busca pv-busca-uni"><Search size={14} /><input value={buscaUni} onChange={(e) => setBuscaUni(e.target.value)} placeholder={t('Procurar universo')} aria-label={t('Procurar universo')} /></label>}
      <div className="pv-chips pv-chips-uni">{mostrados.map(([u, n]) => { const on = filtro.universos.includes(u);
        return <button key={u} className={on ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, universos: alterna(filtro.universos, u) }); som('toque'); }}>{t(u)}<i>{n}</i></button>; })}</div>
      {!todosUni && !q && unisVisiveis.length > 18 && <button className="pv-ver-todos" onClick={() => setTodosUni(true)}>{t('Ver os {n} universos', { n: unisVisiveis.length })}</button>}

      <footer><button className="primary pv-grande" onClick={onFechar}><Check size={20} />{plural(total, 'Ver {n} personagem', 'Ver {n} personagens')}</button></footer>
    </section>
  </div>, document.body);
}

/* ---------------------------------------------------------------------------
 * 2. Montar os 3 times
 * ------------------------------------------------------------------------- */

export function Montar({ rival, colecao, inicial, onPronto, onVoltar, onDetails, prazo, melhores = false, aviso, ocupado = false, emprestados }: { rival: Oponente; colecao: string[]; inicial?: string[][]; onPronto: (t: Times) => void; onVoltar: () => void; onDetails: (id: string) => void; prazo?: ReactNode;
  /** Um aviso abaixo do título (a campanha mostra quem está descansando). */
  aviso?: ReactNode;
  /** Esperando o servidor depois do PRONTO. */
  ocupado?: boolean;
  /** Os emprestados do dia que não são seus (ganham a fita EMPRESTADO e um filtro próprio). */
  emprestados?: ReadonlySet<string>;
  /** Só na conta do dono (pedido dele): um botão que monta o melhor time possível no time escolhido (ou completa ele). */
  melhores?: boolean }) {
  const dono = useContext(DonoDoPvp);
  const valido = (t?: string[][]) => !!t && t.length === 3 && t.every((x) => x.every((id) => colecao.includes(id)));
  const [times, setTimes] = useState<string[][]>(() => (valido(inicial) ? inicial!.map((t) => [...t]) : [[], [], []]));
  const [ativo, setAtivo] = useState(() => Math.max(0, times.findIndex((t) => t.length < 3)));
  const [busca, setBusca] = useState('');
  const [filtro, setFiltro] = useState<Filtro>(FILTRO_VAZIO);
  const [painel, setPainel] = useState(false);
  const usados = new Map(times.flatMap((t, i) => t.map((id) => [id, i] as const)));
  const cheios = times.every((t) => t.length === 3);
  const problema = cheios ? problemaDosTimes(times, new Set(colecao)) : null;
  const [soEmprestados, setSoEmprestados] = useState(false);
  const quantosEmprestados = emprestados ? colecao.filter((id) => emprestados.has(id)).length : 0;
  const lista = useMemo(() => filtrar(soEmprestados && emprestados ? colecao.filter((id) => emprestados.has(id)) : colecao, busca, filtro), [colecao, busca, filtro, soEmprestados, emprestados]);
  const grupos = useMemo(() => agrupar(lista, filtro.ordem), [lista, filtro.ordem]);
  const ativos = filtro.universos.length + filtro.funcoes.length + (filtro.esconderUsados ? 1 : 0);

  const tocar = (id: string) => {
    const onde = usados.get(id);
    if (onde !== undefined) { setTimes((ts) => ts.map((t, i) => (i === onde ? t.filter((x) => x !== id) : t))); setAtivo(onde); som('toque'); return; }
    let alvo = times[ativo]!.length < 3 ? ativo : times.findIndex((t) => t.length < 3);
    if (alvo < 0) return;
    const novo = times.map((t, i) => (i === alvo ? [...t, id] : t));
    setTimes(novo); som('ui-confirma');
    if (novo[alvo]!.length === 3) { const prox = novo.findIndex((t) => t.length < 3); if (prox >= 0) alvo = prox; }
    setAtivo(alvo);
  };
  const sozinho = () => { const s = timesAoAcaso(colecao); if (s) { setTimes(s); setAtivo(0); som('pronto'); } };
  const oMelhorAqui = async () => {
    const outros = new Set(times.flatMap((t, i) => (i === ativo ? [] : t)));
    const topo = await carregarRanking().then((r) => r.topo, () => undefined);
    const t = melhorTimeAqui(colecao, times[ativo]!, outros, topo);
    if (!t) return;
    const novo = times.map((x, i) => (i === ativo ? t : x));
    setTimes(novo); som('pronto');
    const prox = novo.findIndex((x) => x.length < 3);
    if (prox >= 0) setAtivo(prox);
  };

  return <section className="pv-montar">
    <header className="pv-subtopo">
      <button className="icon-button" onClick={onVoltar} aria-label={t('Voltar')}><ArrowLeft size={20} /></button>
      <div><small>{t('CONTRA {nome}', { nome: rival.nome.toUpperCase() })}</small><h1>{t('Monte seus 3 times')}</h1></div>
      {rival.avatar(44)}
    </header>
    {prazo}
    {aviso}
    {/* os 3 times e o PRONTO ficam presos no topo enquanto o álbum rola (pedido do jogador: ver o time enquanto troca) */}
    <div className="pv-fixos">
    <div className="pv-slots">
      {times.map((tm, i) => {
        const estrelas = tm.length === 3 ? estrelasDoTime(tm) : 0;
        return <button key={i} className={`pv-slot ${ativo === i ? 'ativo' : ''} ${tm.length === 3 ? 'cheio' : ''}`} onClick={() => setAtivo(i)} style={{ '--i': i } as CSSProperties}>
          <span className="pv-slot-topo"><b>{t('TIME {n}', { n: i + 1 })}</b>{tm.length === 3 && !dono ? null : tm.length === 3 ? <span className="pv-estrelas" aria-label={t('Força {n} de {max}', { n: estrelas, max: ESTRELAS_MAXIMAS })}>{ESTRELAS.map((k) => <i key={k} className={k <= estrelas ? 'on' : ''}>★</i>)}<Douradas time={tm} />{melhores && <PosicaoDoTime time={tm} curta />}</span> : <small>{tm.length}/3</small>}</span>
          <span className="pv-slot-rostos">{[0, 1, 2].map((k) => tm[k] ? <span key={k} className="pv-slot-cheio" role="button" tabIndex={0} aria-label={t('Tirar {nome}', { nome: nomeDe(byId[tm[k]!]!) })} onClick={(e) => { e.stopPropagation(); tocar(tm[k]!); }}><Rosto id={tm[k]!} tamanho={46} ficha={false} /><X size={12} className="pv-tirar" /></span> : <span key={k} className="pv-slot-vazio">+</span>)}</span>
        </button>;
      })}
    </div>
    <div className="pv-pronto-topo">
      {problema && <small className="pv-problema">{t(problema)}</small>}
      <button className="primary pv-pronto" disabled={!cheios || !!problema || ocupado} onClick={() => { som('pronto'); onPronto(times as Times); }}><Check size={20} />{ocupado ? t('Entrando…') : cheios ? t('PRONTO') : t('Faltam {n}', { n: 9 - times.flat().length })}</button>
    </div>
    </div>
    <div className="pv-ferramentas">
      <label className="pv-busca"><Search size={16} /><input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder={t('Procurar entre {n} personagens', { n: colecao.length })} aria-label={t('Procurar personagem')} />{busca && <button className="pv-limpar-busca" onClick={() => setBusca('')} aria-label={t('Limpar a busca')}><X size={14} /></button>}</label>
      <button className={`secondary pv-filtros-botao ${ativos ? 'ativo' : ''}`} onClick={() => { setPainel(true); som('toque'); }}><SlidersHorizontal size={16} />{t('Filtros')}{ativos > 0 && <i>{ativos}</i>}</button>
      <button className="secondary pv-sozinho" onClick={sozinho}><Wand2 size={16} />{t('Montar ao acaso')}</button>
      {melhores && <button className="secondary pv-melhores" onClick={() => void oMelhorAqui()} title={times[ativo]!.length === 1 || times[ativo]!.length === 2 ? t('Completa o Time {n} com quem mais combina com quem já está nele', { n: ativo + 1 }) : t('Monta o melhor time possível no Time {n}', { n: ativo + 1 })}><Crown size={16} />{times[ativo]!.length === 1 || times[ativo]!.length === 2 ? t('Completar o Time {n}', { n: ativo + 1 }) : t('Melhor no Time {n}', { n: ativo + 1 })}</button>}
      {quantosEmprestados > 0 && <button className={`secondary pv-so-emprestados ${soEmprestados ? 'ativo' : ''}`} onClick={() => { setSoEmprestados(!soEmprestados); som('toque'); }}><Handshake size={16} />{t('Emprestados')}<i>{quantosEmprestados}</i></button>}
    </div>
    {ativos > 0 && <div className="pv-filtros-ativos">
      {filtro.funcoes.map((f) => { const Icone = ICONE_DA_IDENTIDADE[f]; return <button key={f} style={{ '--cor': FAMILIA_DA_IDENTIDADE[familiaDaIdentidade[f]].cor } as CSSProperties} onClick={() => setFiltro({ ...filtro, funcoes: filtro.funcoes.filter((x) => x !== f) })}><Icone size={12} />{t(f)}<X size={12} /></button>; })}
      {filtro.universos.map((u) => <button key={u} style={{ '--cor': '#8fd3ff' } as CSSProperties} onClick={() => setFiltro({ ...filtro, universos: filtro.universos.filter((x) => x !== u) })}><Globe2 size={12} />{t(u)}<X size={12} /></button>)}
      {filtro.esconderUsados && <button style={{ '--cor': '#c8f560' } as CSSProperties} onClick={() => setFiltro({ ...filtro, esconderUsados: false })}>{t('Só os livres')}<X size={12} /></button>}
    </div>}
    {grupos.map((g) => <div key={g.titulo || 'todos'} className="pv-grupo">
      {g.titulo && <h3 className="pv-grupo-titulo"><span>{t(g.titulo)}</span><small>{g.lista.length}</small></h3>}
      <div className="pv-album">
        {g.lista.filter((c) => !filtro.esconderUsados || !usados.has(c.id)).map((c, k) => {
          const onde = usados.get(c.id);
          const emprestado = !!emprestados?.has(c.id);
          return <button key={c.id} className={`pv-carta ${onde !== undefined ? 'usada' : ''} ${emprestado ? 'emprestada' : ''}`} onClick={() => tocar(c.id)} onContextMenu={(e) => { e.preventDefault(); onDetails(c.id); }} style={{ '--character': c.color, '--k': Math.min(k, 30) } as CSSProperties} aria-label={`${nomeDe(c)}${onde !== undefined ? t(', no time {n}', { n: onde + 1 }) : ''}`}>
            <Portrait character={c} /><b>{nomeDe(c)}</b>{onde !== undefined && <em>T{onde + 1}</em>}{emprestado && <span className="pv-fita"><Handshake size={10} />{t('EMPRESTADO')}</span>}
            <span className="pv-carta-ficha" role="button" tabIndex={0} aria-label={t('Ficha de {nome}', { nome: nomeDe(c) })} onClick={(e) => { e.stopPropagation(); onDetails(c.id); }}><Info size={13} /></span>
          </button>;
        })}
      </div>
    </div>)}
    {!lista.length && <div className="pv-nada"><Search size={28} /><b>{t('Ninguém com esses filtros')}</b><button className="secondary" onClick={() => { setFiltro(FILTRO_VAZIO); setBusca(''); }}>{t('Limpar filtros')}</button></div>}
    {painel && <PainelDeFiltros colecao={colecao} filtro={filtro} total={lista.length} onFiltro={setFiltro} onFechar={() => setPainel(false)} />}
  </section>;
}

/* ---------------------------------------------------------------------------
 * 3–8. A partida
 * ------------------------------------------------------------------------- */

export function Apresentar({ rival, partida, onComecar }: { rival: Oponente; partida: Pick<PartidaPvp, 'meus' | 'deles'>; onComecar: () => void }) {
  return <section className="pv-apresentar">
    <div className="pv-frente">
      <div className="pv-lado eu"><span className="pv-nome-lado">{t('VOCÊ')}</span>{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" compacto />)}</div>
      <span className="pv-vs-pequeno">VS</span>
      <div className="pv-lado rival" style={{ '--npc': rival.cor } as CSSProperties}><span className="pv-nome-lado">{rival.avatar(34)}{rival.nome}</span>{partida.deles.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="rival" compacto />)}</div>
    </div>
    {rival.fala && <p className="pv-fala" style={{ '--npc': rival.cor } as CSSProperties}><b>{rival.nome}:</b> “{rival.fala}”</p>}
    <button className="primary pv-grande" onClick={onComecar}><Swords size={22} />{t('COMEÇAR PARTIDA')}</button>
  </section>;
}

export function Escolher({ rival, partida, onEscolher, jaEscolhido, prazo }: { rival: Oponente; partida: PartidaPvp; onEscolher: (i: number) => void; jaEscolhido?: number | null; prazo?: ReactNode }) {
  const livres = timesLivres(partida, 'eu'), v = vitoriasDosTimes(partida);
  const [sel, setSel] = useState<number | null>(jaEscolhido ?? (livres.length === 1 ? livres[0]! : null));
  const [pensando, setPensando] = useState(jaEscolhido !== undefined && jaEscolhido !== null);
  return <section className="pv-escolher">
    <Placar partida={partida} rival={rival} />
    {prazo}
    <h2 className="pv-titulo-rodada">{t('Escolha seu time')} <small>{t('em segredo: {nome} escolhe ao mesmo tempo', { nome: rival.nome })}</small></h2>
    <div className="pv-escolhas">{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" venceu={v.eu[i]} bloqueado={!livres.includes(i)} escolhido={sel === i} onClick={pensando ? undefined : () => { setSel(i); som('toque'); }} />)}</div>
    <div className="pv-rival-pensa" style={{ '--npc': rival.cor } as CSSProperties}>
      {rival.avatar(38)}
      <span>{pensando ? t('{nome} está escolhendo…', { nome: rival.nome }) : timesLivres(partida, 'rival').length === 1 ? t('{nome} tem {n} time para escolher', { nome: rival.nome, n: 1 }) : t('{nome} tem {n} times para escolher', { nome: rival.nome, n: timesLivres(partida, 'rival').length })}</span>
      <span className="pv-mini-times">{partida.deles.map((t, i) => <span key={i} className={v.rival[i] ? 'venceu' : ''}>{t.map((id) => <Rosto key={id} id={id} tamanho={22} apagado={v.rival[i]} />)}</span>)}</span>
    </div>
    <button className="primary pv-grande" disabled={sel === null || pensando} onClick={() => { setPensando(true); som('ui-confirma'); onEscolher(sel!); }}>
      <Check size={20} />{pensando ? t('Confirmado…') : t('CONFIRMAR TIME')}
    </button>
  </section>;
}

export function Vs({ rival, partida, meu, dele, onLutar, controle }: { rival: Oponente; partida: Pick<PartidaPvp, 'meus' | 'deles'>; meu: number; dele: number; onLutar: () => void; controle?: ReactNode }) {
  const [conta, setConta] = useState(3);
  useEffect(() => { som('ui-arena'); }, []);
  useEffect(() => { if (controle) return; if (conta <= 0) { onLutar(); return; } const t = window.setTimeout(() => { setConta(conta - 1); som('toque'); }, 1000); return () => clearTimeout(t); }, [conta, onLutar, controle]);
  return <section className="pv-vs" style={{ '--npc': rival.cor } as CSSProperties}>
    <span className="pv-vs-raios" aria-hidden="true" />
    <Fx nome="holofote" cor="#ffe2a0" ms={4800} className="pv-fx-holofote-vs" />
    {/* o rival em cima e você embaixo, como na luta (pedido do jogador) */}
    <div className="pv-vs-lado rival"><small>{rival.nome.toUpperCase()} · {t('TIME {n}', { n: dele + 1 })}</small>{partida.deles[dele]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{nomeDe(byId[id]!)}</b></span>)}</div>
    <span className="pv-vs-centro"><Fx nome="choque" cor="#ffb84d" ms={950} laco={false} className="pv-fx-choque" /><span className="pv-vs-letras" aria-label="Versus">VS</span></span>
    <div className="pv-vs-lado eu"><small>{t('VOCÊ')} · {t('TIME {n}', { n: meu + 1 })}</small>{partida.meus[meu]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{nomeDe(byId[id]!)}</b></span>)}</div>
    {controle ?? <button className="pv-vs-contagem" onClick={onLutar} aria-label={t('Começar o duelo agora')}><b key={conta}>{conta > 0 ? conta : t('LUTA!')}</b><small>{t('toque para começar')}</small></button>}
  </section>;
}

export function ResultadoDaRodada({ rival, partida, onSeguir, final = false }: { rival: Oponente; partida: PartidaPvp; onSeguir: () => void; final?: boolean }) {
  const r = partida.rodadas.at(-1)!, ganhei = r.vencedor === 'eu', time = ganhei ? partida.meus[r.meu]! : partida.deles[r.dele]!;
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  return <section className={`pv-resultado ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    <span className="pv-brilho" aria-hidden="true" />
    <small>{t('RODADA {n}', { n: partida.rodadas.length })}</small>
    <h1>{ganhei ? t('VOCÊ VENCEU!') : t('{nome} venceu', { nome: rival.nome })}</h1>
    <p>{r.rendida ? `${ganhei ? t('{nome} desistiu desta luta.', { nome: rival.nome }) : t('Você desistiu desta luta.')} ` : ''}{ganhei ? t('O time {n} ganhou a medalha e fica marcado.', { n: r.meu + 1 }) : t('O time {n} dele fica marcado. Você pode usar qualquer time de novo.', { n: r.dele + 1 })}</p>
    <div className="pv-resultado-time">{time.map((id) => <Rosto key={id} id={id} tamanho={64} />)}</div>
    <Placar partida={partida} rival={rival} />
    <button className="primary pv-grande" onClick={onSeguir}>{final ? <><Trophy size={20} />{t('VER RESULTADO')}</> : <><Swords size={20} />{t('PRÓXIMA RODADA')}</>}</button>
  </section>;
}

function Fim({ npc, partida, placar, onDeNovo, onSair }: { npc: Npc; partida: PartidaPvp; placar: { v: number; d: number }; onDeNovo: () => void; onSair: () => void }) {
  const ganhei = vencedorDaPartida(partida) === 'eu';
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  return <section className={`pv-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': npc.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <span className="pv-fim-trofeu">{ganhei ? <Trophy size={58} /> : <Shield size={58} />}</span>
    <small>{t('TREINO')} · {t(npc.titulo).toUpperCase()}</small>
    <h1>{ganhei ? t('VITÓRIA!') : t('DERROTA')}</h1>
    <p>{ganhei ? t('Você venceu {nome} com os 3 times.', { nome: t(npc.nome) }) : t('{nome} venceu com os 3 times dele. Treine mais um pouco!', { nome: t(npc.nome) })}</p>
    <div className="pv-fim-rodadas">{partida.rodadas.map((r, i) => <span key={i} className={r.vencedor}><b>{i + 1}</b>{r.vencedor === 'eu' ? t('V') : t('D')}</span>)}</div>
    <div className="pv-fim-placar"><AvatarDoNpc npc={npc} tamanho={40} /><span>{t('Seu placar contra {nome}', { nome: t(npc.nome) })}</span><b className="v">{t('{n}V', { n: placar.v })}</b><b className="d">{t('{n}D', { n: placar.d })}</b></div>
    <small className="pv-nota">{t('Treino não muda o rating nem o ranking.')}</small>
    <div className="pv-fim-botoes"><button className="primary" onClick={onDeNovo}><RotateCcw size={18} />{t('Jogar de novo')}</button><button className="secondary" onClick={onSair}>{t('Voltar')}</button></div>
  </section>;
}


/* ---------------------------------------------------------------------------
 * O Desafio online
 * ------------------------------------------------------------------------- */

export interface Online { servico: ServicoPvp; partida: string | null; onPartida: (id: string | null) => void; onComunidade: () => void }

const oponenteDaPessoa = (j: JogadorPvp): Oponente => ({ nome: j.nome, cor: corDoNome(j.id), avatar: (t) => <Avatar id={j.id} nome={j.nome} tamanho={t} online /> });
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

/** Um relógio que bate enquanto a tela precisa (contagens do prazo e da luta). */
function useAgora(ligado = true, ms = 250) {
  const [agora, setAgora] = useState(() => Date.now());
  useEffect(() => { if (!ligado) return; const t = window.setInterval(() => setAgora(Date.now()), ms); return () => clearInterval(t); }, [ligado, ms]);
  return agora;
}

/** O tempo que falta, no relógio do servidor. */
function Prazo({ ate, offset, texto }: { ate: string; offset: number; texto: string }) {
  const agora = useAgora(true, 500), s = Math.max(0, Math.ceil((Date.parse(ate) - (agora + offset)) / 1000));
  return <p className={`pv-prazo ${s <= 15 ? 'urgente' : ''}`}><Clock size={14} /><b>{mmss(s)}</b>{texto}</p>;
}

/** O cartão do Desafio online no lobby: meu rating, a partida aberta e o ranking. */
function CartaoOnline({ online, rank }: { online: Online; rank: RankingPvp | null }) {
  const [aberta, setAberta] = useState<VistaPvp | null>(null);
  useEffect(() => {
    let vivo = true;
    void online.servico.consultar().then((r) => { if (vivo) setAberta(r.partida); }).catch(() => undefined);
    return () => { vivo = false; };
  }, [online.servico]);
  const eu = rank?.eu;
  return <div className="pv-online">
    <div className="pv-modo online">
      <span className="pv-modo-icone"><Users size={24} /></span>
      <div><b>{t('DESAFIO ONLINE')}</b><small>{t('Toque no nome de alguém na Comunidade e desafie. Vale rating e ranking do PvP.')}</small></div>
      <span className="pv-meu-rating"><Crown size={13} /><b>{eu?.rating ?? '—'}</b><small>{eu ? t('{v}V {d}D', { v: eu.vitorias, d: eu.derrotas }) : t('rating')}</small></span>
    </div>
    {aberta && ['convite', 'montando', 'jogando'].includes(aberta.fase) && <button className="pv-voltar-partida" onClick={() => online.onPartida(aberta.id)}>
      <Avatar id={aberta.rival.id} nome={aberta.rival.nome} tamanho={34} online />
      <span><b>{t('Partida contra {nome}', { nome: aberta.rival.nome })}</b><small>{aberta.fase === 'convite' ? (aberta.desafiante ? t('esperando aceitar') : t('te desafiou!')) : aberta.fase === 'montando' ? t('montando os times') : t('rodada {n}', { n: aberta.rodada + 1 })}</small></span>
      <em>{t('VOLTAR')}</em>
    </button>}
    <button className="primary pv-desafiar" onClick={online.onComunidade}><Swords size={18} />{t('Desafiar alguém na Comunidade')}</button>
  </div>;
}

/** Uma confirmação simples por cima da tela (sair da partida). */
export function Confirmar({ titulo, texto, sim, onSim, onNao }: { titulo: string; texto: string; sim: string; onSim: () => void; onNao: () => void }) {
  return createPortal(<div className="pv-confirmar" role="alertdialog" aria-label={titulo}>
    <div><b>{titulo}</b><p>{texto}</p><span><button className="secondary" onClick={onNao}>{t('Continuar')}</button><button className="primary pv-perigo" onClick={onSim}><LogOut size={16} />{sim}</button></span></div>
  </div>, document.body);
}

/** A espera (convite enviado, times prontos, rival escolhendo): o rival, o recado e o prazo. */
function Espera({ rival, titulo, texto, prazo, children, onSair, sair }: { rival: Oponente; titulo: string; texto: string; prazo?: ReactNode; children?: ReactNode; onSair?: () => void; sair?: string }) {
  return <section className="pv-espera" style={{ '--npc': rival.cor } as CSSProperties}>
    <span className="pv-espera-avatar">{rival.avatar(96)}<i aria-hidden="true" /></span>
    <small>{rival.nome.toUpperCase()}</small>
    <h1>{titulo}</h1>
    <p className="pv-espera-texto"><Hourglass size={15} />{texto}</p>
    {prazo}
    {children}
    {onSair && <button className="secondary" onClick={onSair}><X size={16} />{sair ?? t('Cancelar')}</button>}
  </section>;
}

/** O rival caiu: a partida segue, e ele tem um tempo para voltar (pedido do jogador: 45 s; senão a vitória é sua). */
function RivalCaiu({ nome, falta, desde }: { nome: string; falta: number; desde: number }) {
  const agora = useAgora(true, 500), s = Math.max(0, Math.ceil(falta - (agora - desde) / 1000));
  return createPortal(<div className="pv-caiu" role="status"><WifiOff size={18} /><span><b>{t('{nome} desconectou', { nome })}</b><small>{s > 0 ? t('tem {tempo} para voltar, senão a vitória é sua', { tempo: mmss(s) }) : t('a vitória é sua…')}</small></span><em>{s}</em></div>, document.body);
}

function FimOnline({ v, rival, onSair }: { v: VistaPvp; rival: Oponente; onSair: () => void }) {
  const ganhei = v.vencedor === 'eu', delta = v.delta ?? 0;
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  const porDesistencia = v.motivo === 'desistiu', porQueda = v.motivo === 'desconectou';
  return <section className={`pv-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <span className="pv-fim-trofeu">{ganhei ? <Trophy size={58} /> : <Shield size={58} />}</span>
    <small>{t('DESAFIO ONLINE · VALENDO RATING')}</small>
    <h1>{ganhei ? t('VITÓRIA!') : t('DERROTA')}</h1>
    <p>{porQueda ? (ganhei ? t('{nome} desconectou e não voltou em {s} s.', { nome: rival.nome, s: v.ausenciaMaxima }) : t('Você ficou desconectado mais de {s} s.', { s: v.ausenciaMaxima })) : porDesistencia ? (ganhei ? t('{nome} abandonou a partida.', { nome: rival.nome }) : t('Você abandonou a partida.')) : ganhei ? t('Você venceu {nome} com os 3 times.', { nome: rival.nome }) : t('{nome} venceu com os 3 times.', { nome: rival.nome })}</p>
    {v.rodadas.length > 0 && <div className="pv-fim-rodadas">{v.rodadas.map((r) => <span key={r.n} className={r.vencedor}><b>{r.n + 1}</b>{r.vencedor === 'eu' ? t('V') : t('D')}</span>)}</div>}
    <div className="pv-fim-rating">
      <Crown size={22} /><span><small>{t('SEU RATING')}</small><b>{v.voce.rating}</b></span>
      <em className={delta >= 0 ? 'sobe' : 'desce'}>{delta >= 0 ? '+' : ''}{delta}</em>
      <span className="pv-fim-vd"><b className="v">{t('{n}V', { n: v.voce.vitorias })}</b><b className="d">{t('{n}D', { n: v.voce.derrotas })}</b></span>
    </div>
    <div className="pv-fim-botoes"><button className="primary" onClick={onSair}><Trophy size={18} />{t('Ver o ranking')}</button></div>
  </section>;
}

/** O que este aparelho já mostrou da partida: a apresentação e as lutas assistidas (para não repetir ao voltar). */
interface Assistido { id: string; apresentado: boolean; vistas: number[] }
const lerAssistido = (id: string): Assistido => {
  const a = read('pvp-online') as Assistido | null;
  return a && a.id === id && Array.isArray(a.vistas) ? a : { id, apresentado: false, vistas: [] };
};

/** Até onde a partida já andou (fase, rodada, rodada resolvida, luta marcada): para não voltar com uma resposta velha. */
const FASES: Record<string, number> = { convite: 0, montando: 1, jogando: 2, terminada: 3, recusada: 3, cancelada: 3, expirada: 3 };
const progressoDaVista = (p: VistaPvp) => [FASES[p.fase] ?? 0, p.rodada, p.resolvida, p.inicioEm ? 1 : 0];
function atras(a: number[], b: number[]) {
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i]! < b[i]!;
  return false;
}

type Cena = { tipo: 'luta'; n: number; meu: string[]; dele: string[]; seed: number; atraso: number } | { tipo: 'resultado'; n: number } | null;

function PartidaOnline({ online, colecaoLocal, emprestados, settings, onSettings, onDetails, onLutando }: {
  online: Online; colecaoLocal: string[]; emprestados?: ReadonlySet<string>; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onLutando: (sim: boolean) => void;
}) {
  const id = online.partida!, { servico } = online;
  const [v, setV] = useState<VistaPvp | null>(null);
  const [colecao, setColecao] = useState<string[]>(colecaoLocal);
  const [offset, setOffset] = useState(0);
  const [recebido, setRecebido] = useState(0);
  const [erro, setErro] = useState('');
  const [sumiu, setSumiu] = useState(false);
  const [falhas, setFalhas] = useState(0);
  const [assistido, setAssistido] = useState(() => lerAssistido(id));
  const [cena, setCena] = useState<Cena>(null);
  const [sair, setSair] = useState(false);
  const [renderLuta, setRenderLuta] = useState(false);
  const [guardado] = useState(carregar);
  const marca = (a: Assistido) => { setAssistido(a); save('pvp-online', a); };

  // as respostas podem chegar fora de ordem (a de 3 em 3 s e a do aviso do Realtime): uma resposta mais atrasada que a
  // última aplicada não volta a partida para trás
  const ultima = useRef<{ id: string; progresso: number[] } | null>(null);
  const aplica = (r: RespostaPvp) => {
    if (!r.partida) { setSumiu(true); return; }
    const progresso = progressoDaVista(r.partida), u = ultima.current;
    if (u && u.id === r.partida.id && atras(progresso, u.progresso)) return;
    ultima.current = { id: r.partida.id, progresso };
    setV(r.partida); setOffset(diferencaDoRelogio(r.partida.agora)); setRecebido(Date.now());
    if (r.colecao.length) setColecao(r.colecao);
  };
  const atualizar = useRef(async () => {});
  atualizar.current = async () => { try { aplica(await servico.consultar(id)); setErro(''); } catch (e) { setErro(textoDoErroPvp(e)); } };
  const agir = async (pedido: Promise<RespostaPvp>) => {
    try { aplica(await pedido); setErro(''); return true; } catch (e) { setErro(textoDoErroPvp(e)); setFalhas((f) => f + 1); void atualizar.current(); return false; }
  };

  // o estado vem do servidor: a cada 3 s e na hora em que a partida muda (Realtime)
  const aberta = !v || ['convite', 'montando', 'jogando'].includes(v.fase) || (v.fase === 'terminada' && v.resolvida >= 0 && !v.inicioEm && v.motivo !== 'desistiu');
  useEffect(() => {
    void atualizar.current();
    const para = servico.ouvir((l) => { if (l.id === id) void atualizar.current(); });
    return para;
  }, [servico, id]);
  useEffect(() => {
    if (!aberta) return;
    const t = window.setInterval(() => { if (!document.hidden) void atualizar.current(); }, 3000);
    return () => clearInterval(t);
  }, [aberta]);

  useEffect(() => { onLutando(cena?.tipo === 'luta'); }, [cena?.tipo, onLutando]);
  useEffect(() => () => onLutando(false), [onLutando]);
  useEffect(() => { window.scrollTo(0, 0); }, [v?.fase, v?.rodada, cena?.tipo]);

  const rivalId = v?.rival.id, rivalNome = v?.rival.nome;
  const rival = useMemo(() => (rivalId && rivalNome ? oponenteDaPessoa({ id: rivalId, nome: rivalNome, rating: 0, vitorias: 0, derrotas: 0 }) : null), [rivalId, rivalNome]);
  const emLuta = cena?.tipo === 'luta';
  const agora = useAgora(!emLuta);

  // a luta da rodada que acabou de ser resolvida (as anteriores já foram vistas ou ficaram para trás)
  const pendente = v && v.resolvida >= 0 ? v.rodadas.find((r) => r.n === v.resolvida && !assistido.vistas.includes(r.n)) ?? null : null;
  // o começo de cada luta é dela só: um horário que já foi de uma luta anterior nunca vale para a próxima (senão a luta
  // nova "começava" lá atrás e aparecia já no fim, com todo mundo morto)
  const comecos = useRef(new Map<string, number>());
  const doComeco = v?.inicioEm ? comecos.current.get(v.inicioEm) : undefined;
  const inicioDaPendente = v?.inicioEm && pendente && (doComeco === undefined || doComeco === pendente.n) ? v.inicioEm : null;
  if (inicioDaPendente && pendente && doComeco === undefined) comecos.current.set(inicioDaPendente, pendente.n);
  const inicio = inicioDaPendente ? Date.parse(inicioDaPendente) - offset : null;
  const fimDaLuta = pendente && inicio !== null ? inicio + duracaoNaTela(pendente.duracao) * 1000 : null;
  useEffect(() => {
    if (!v || !pendente || inicio === null || cena) return;
    if (agora < inicio) return;
    // chegou tarde demais: a luta já acabou, mostra o resultado
    if (fimDaLuta !== null && agora > fimDaLuta) { setCena({ tipo: 'resultado', n: pendente.n }); return; }
    setCena({ tipo: 'luta', n: pendente.n, meu: v.meusTimes![pendente.meu]!, dele: v.timesDele![pendente.dele]!, seed: pendente.seed, atraso: (agora - inicio) / 1000 });
  }, [v, pendente, inicio, fimDaLuta, agora, cena]);

  /*
   * A luta só começa com os dois vendo a tela (pedido do jogador: "a luta não pode começar até os dois estarem vendo a
   * tela"): com o VS aberto e o app na frente, este aparelho avisa que está pronto; se o app vai para segundo plano
   * antes da luta começar, avisa que saiu. Quando os dois estão prontos, o servidor marca o começo nos dois aparelhos.
   */
  const noVs = !!pendente && inicio === null && (v?.fase === 'jogando' || v?.fase === 'terminada');
  const prontoNoServidor = !!v?.lutar.eu;
  const [visivel, setVisivel] = useState(() => !document.hidden);
  useEffect(() => { const muda = () => setVisivel(!document.hidden); document.addEventListener('visibilitychange', muda); return () => document.removeEventListener('visibilitychange', muda); }, []);
  const avisando = useRef(false);
  useEffect(() => {
    if (!noVs || avisando.current || visivel === prontoNoServidor) return;
    avisando.current = true;
    void servico.lutar(id, visivel).then(aplica).catch(() => undefined).finally(() => { avisando.current = false; });
  }, [noVs, visivel, prontoNoServidor, servico, id]);

  // terminei de assistir a luta: avisa o servidor (o tempo de escolher a próxima começa quando os dois terminam)
  const assistiu = cena?.tipo === 'resultado' ? cena.n : null;
  useEffect(() => { if (assistiu !== null) void servico.assisti(id, assistiu).catch(() => undefined); }, [assistiu, servico, id]);
  const semRodada = assistiu !== null && !!v && !v.rodadas.some((r) => r.n === assistiu);
  useEffect(() => { if (semRodada) setCena(null); }, [semRodada]);

  // o rival desistiu da luta que está passando: ela acaba aqui também
  const rendidaAgora = cena?.tipo === 'luta' && !!v?.rodadas.find((r) => r.n === cena.n)?.rendida;
  const nDaCena = cena?.n;
  useEffect(() => { if (rendidaAgora && nDaCena !== undefined) setCena({ tipo: 'resultado', n: nDaCena }); }, [rendidaAgora, nDaCena]);

  // alguém desistiu no meio da luta: a partida acabou, sai da luta
  const desistiram = v?.fase === 'terminada' && v.motivo === 'desistiu';
  useEffect(() => { if (desistiram) setCena(null); }, [desistiram]);

  const voltar = () => { online.onPartida(null); };
  if (sumiu) return <Espera rival={{ nome: t('Partida'), cor: '#8fd3ff', avatar: () => <Swords size={60} /> }} titulo={t('Partida não encontrada')} texto={t('Ela pode ter acabado.')} onSair={voltar} sair={t('Voltar')} />;
  if (!v || !rival) return <section className="pv-espera"><p className="cm-carregando-tela">{erro || t('Abrindo a partida…')}</p>{erro && <button className="secondary" onClick={voltar}>{t('Voltar')}</button>}</section>;
  const aviso = erro ? <p className="pv-problema pv-erro-online">{erro}</p> : null;
  const caiu = v.ausencia !== null && (v.fase === 'jogando' || v.fase === 'montando') ? <RivalCaiu nome={v.rival.nome} falta={v.ausenciaMaxima - v.ausencia} desde={recebido} /> : null;
  const confirmaSair = <>{caiu}{sair && <Confirmar titulo={v.fase === 'jogando' ? t('Abandonar a partida?') : t('Sair da partida?')}
    texto={v.fase === 'jogando' ? t('Abandonar conta como derrota e {nome} ganha o rating.', { nome: v.rival.nome }) : t('A partida é cancelada e ninguém perde rating.')}
    sim={v.fase === 'jogando' ? t('Abandonar') : t('Sair')} onNao={() => setSair(false)} onSim={() => { setSair(false); void agir(servico.desistir(id)); }} />}</>;

  // fora de jogo: convite recusado, cancelado ou expirado
  if (v.fase === 'recusada' || v.fase === 'cancelada' || v.fase === 'expirada')
    return <Espera rival={rival} titulo={v.fase === 'recusada' ? t('Desafio recusado') : v.fase === 'expirada' ? t('O convite expirou') : t('Partida cancelada')} texto={v.motivo ? t(v.motivo) : t('Ninguém perdeu rating.')} onSair={voltar} sair={t('Voltar')} />;

  if (v.fase === 'convite') {
    if (v.desafiante) return <><Espera rival={rival} titulo={t('Desafio enviado!')} texto={t('Esperando {nome} aceitar…', { nome: v.rival.nome })} prazo={<Prazo ate={v.prazo} offset={offset} texto={` ${t('para aceitar')}`} />} onSair={() => void agir(servico.desistir(id))} sair={t('Cancelar desafio')}>
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {t('{v}V {d}D', { v: v.rival.vitorias, d: v.rival.derrotas })}</span>{aviso}</Espera></>;
    return <Espera rival={rival} titulo={t('{nome} te desafiou!', { nome: v.rival.nome })} texto={t('3 times de 3, escolha secreta, vale rating.')} prazo={<Prazo ate={v.prazo} offset={offset} texto={` ${t('para responder')}`} />}>
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {t('{v}V {d}D', { v: v.rival.vitorias, d: v.rival.derrotas })}</span>{aviso}
      <span className="pv-convite-botoes"><button className="secondary" onClick={() => void agir(servico.responder(id, false))}><X size={18} />{t('Recusar')}</button><button className="primary" onClick={() => { som('ui-arena'); void agir(servico.responder(id, true)); }}><Swords size={18} />{t('Aceitar')}</button></span>
    </Espera>;
  }

  if (v.fase === 'montando') {
    // "Montar os melhores" só no treino (pedido do dono): contra outras pessoas, nem ele
    if (!v.pronto.eu) return <>{<Montar key={falhas} rival={rival} colecao={colecao} emprestados={emprestados} inicial={guardado.times} onDetails={onDetails} onVoltar={() => setSair(true)}
      prazo={<>{<Prazo ate={v.prazo} offset={offset} texto={v.pronto.rival ? ` · ${t('{nome} já está pronto!', { nome: v.rival.nome })}` : ` ${t('para montar')}`} />}{aviso}</>}
      onPronto={(t) => { save('pvp', { ...carregar(), times: t }); void agir(servico.times(id, t)); }} />}{confirmaSair}</>;
    return <><Espera rival={rival} titulo={t('Seus times estão prontos')} texto={t('Esperando {nome} montar os times…', { nome: v.rival.nome })} prazo={<Prazo ate={v.prazo} offset={offset} texto={` ${t('para montar')}`} />} onSair={() => setSair(true)} sair={t('Sair')}>
      {v.meusTimes && <div className="pv-espera-times">{v.meusTimes.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" compacto />)}</div>}{aviso}
    </Espera>{confirmaSair}</>;
  }

  // jogando ou terminada
  const meus = v.meusTimes ?? [[], [], []], deles = v.timesDele ?? [[], [], []];
  const naTela = (r: typeof v.rodadas[number]) => ({ meu: r.meu, dele: r.dele, seed: r.seed, vencedor: r.vencedor });
  /*
   * Rodada que ainda não passou na tela não entra no placar nem nos times (pedido do dono: "o jogador não pode saber se
   * ganhou ou perdeu antes da luta"). Além da pendente, esconde toda rodada não vista a partir da última resolvida: uma
   * resposta do servidor lida no meio do cálculo trazia a rodada nova com a marca antiga, e o time aparecia com o selo
   * VENCEU por um segundo antes do VS.
   */
  const naoPassou = (r: typeof v.rodadas[number]) => r.n === pendente?.n || (!assistido.vistas.includes(r.n) && r.n >= v.resolvida);
  const vistas = v.rodadas.filter((r) => !naoPassou(r)).map(naTela);
  const partida: PartidaPvp = { meus: meus as unknown as Times, deles: deles as unknown as Times, seed: v.seed, rodadas: vistas };

  if (cena?.tipo === 'luta') return <>{<ArenaDoPvp key={cena.n} meu={cena.meu} dele={cena.dele} seed={cena.seed} rodada={cena.n + 1} rival={v.rival.nome} settings={settings} onSettings={onSettings}
    podePausar={false} espelhado={!v.desafiante} atrasoInicial={cena.atraso} onFim={() => setCena({ tipo: 'resultado', n: cena.n })} onDesistir={() => setRenderLuta(true)} />}{confirmaSair}
    {renderLuta && <Confirmar titulo={t('Desistir desta luta?')} texto={t('Você perde esta rodada. A partida continua com os outros times.')} sim={t('Desistir da luta')} onNao={() => setRenderLuta(false)}
      onSim={() => { setRenderLuta(false); const n = cena.n; void agir(servico.render(id, n)).then(() => setCena({ tipo: 'resultado', n })); }} />}</>;
  // o resultado da luta que acabou de passar na tela (mesmo que a partida já tenha andado enquanto ela passava)
  const daCena = cena?.tipo === 'resultado' ? v.rodadas.find((r) => r.n === cena.n) : undefined;
  if (cena?.tipo === 'resultado' && daCena)
    return <>{caiu}<ResultadoDaRodada rival={rival} partida={{ ...partida, rodadas: v.rodadas.filter((r) => r.n <= daCena.n).map(naTela) }} final={v.fase === 'terminada' && daCena.n === v.resolvida}
      onSeguir={() => { marca({ ...assistido, apresentado: true, vistas: [...new Set([...assistido.vistas, ...v.rodadas.filter((r) => r.n <= daCena.n).map((r) => r.n)])] }); setCena(null); }} /></>;

  if (v.fase === 'terminada' && (!pendente || v.motivo === 'desistiu')) return <FimOnline v={v} rival={rival} onSair={() => { marca({ ...assistido, vistas: v.rodadas.map((r) => r.n) }); voltar(); }} />;

  if (!assistido.apresentado && v.rodadas.length === 0) return <>{caiu}<Apresentar rival={rival} partida={partida} onComecar={() => marca({ ...assistido, apresentado: true })} /></>;

  if (pendente) {
    // os dois já escolheram: o VS e o botão de começar (o duelo começa sozinho quando o tempo acaba)
    const conta = inicio !== null ? Math.max(0, Math.ceil((inicio - agora) / 1000)) : null;
    const controle = conta !== null
      ? <div className="pv-vs-contagem"><b key={conta}>{conta > 0 ? conta : t('LUTA!')}</b><small>{t('a luta começa nos dois aparelhos')}</small></div>
      : <div className="pv-vs-contagem esperando"><Hourglass size={26} />
        <small>{v.lutar.rival ? t('{nome} já está vendo a tela. Começando…', { nome: v.rival.nome }) : t('Esperando {nome} abrir a tela da luta…', { nome: v.rival.nome })}</small>
        <small className="pv-pronto-rival"><Check size={13} />{t('A luta só começa com os dois vendo a tela')}</small></div>;
    return <><Vs rival={rival} partida={partida} meu={pendente.meu} dele={pendente.dele} onLutar={() => undefined} controle={<>{controle}{aviso}</>} />{confirmaSair}</>;
  }

  return <>{<Escolher key={`${v.rodada}-${falhas}`} rival={rival} partida={partida} jaEscolhido={v.minhaEscolha}
    prazo={<>{<Prazo ate={v.prazo} offset={offset} texto={v.escolheu.rival ? ` · ${t('{nome} já escolheu!', { nome: v.rival.nome })}` : v.assistiu && !v.assistiu.rival && v.rodadas.length ? ` · ${t('{nome} ainda vê a luta', { nome: v.rival.nome })}` : ` ${t('para escolher')}`} />}{aviso}</>}
    onEscolher={(i) => void agir(servico.escolher(id, v.rodada, i))} />}
    <button className="pv-sair-online" onClick={() => setSair(true)}><LogOut size={14} />{t('Abandonar partida')}</button>{confirmaSair}</>;
}

/* ---------------------------------------------------------------------------
 * A tela
 * ------------------------------------------------------------------------- */

const CaminhoDoNexus = lazy(() => import('./CaminhoDoNexus'));
/* A campanha sem servidor (VITE_CAMPANHA_DEMO=true): só para testar as telas; nunca no jogo publicado. */
const CAMPANHA_DEMO = import.meta.env.VITE_CAMPANHA_DEMO === 'true';

export function PvpScreen(props: Parameters<typeof TelaDoPvp>[0]) {
  return <DonoDoPvp.Provider value={props.dono === true}><FichaDoPvp.Provider value={props.onDetails}><TelaDoPvp {...props} /></FichaDoPvp.Provider></DonoDoPvp.Provider>;
}

function TelaDoPvp({ colecao, settings, onSettings, onDetails, onJogar, onLutando, online, dono = false }: {
  colecao: string[]; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onJogar: () => void; onLutando: (sim: boolean) => void;
  /** O Desafio online (com conta); a partida aberta vem do App (convite aceito, desafio pela Comunidade). */
  online?: Online | null;
  /** A conta do dono: ganha o botão "Montar os melhores" (só no treino contra os NPCs). */
  dono?: boolean;
}) {
  const [etapa, setEtapa] = useState<Etapa>(etapaSalva);
  // o Empréstimo do dia (src/engine/emprestimo.ts): a coleção do PvP é a sua e os 9 de hoje (troca à meia-noite)
  const dia = diaDoEmprestimo(useAgora(true, 30000));
  const propria = colecao;
  const colecaoPvp = useMemo(() => comEmprestados(propria, dia), [propria, dia]);
  const emprestados = useMemo(() => new Set(emprestadosDoDia(dia).filter((id) => !propria.includes(id))), [propria, dia]);
  useEffect(() => { guardaEtapa(etapa); }, [etapa]);
  const naOnline = !!online?.partida;
  useEffect(() => { if (naOnline) return; onLutando(etapa.tipo === 'luta'); window.scrollTo(0, 0); }, [etapa.tipo, onLutando, naOnline]);
  useEffect(() => () => onLutando(false), [onLutando]);
  const [guardado, setGuardado] = useState(carregar);
  const desistir = useRef(false);
  const colecaoAtual = useRef(colecao); colecaoAtual.current = colecao;
  const servicoDaCampanha = useMemo(() => online?.servico.campanha ?? (CAMPANHA_DEMO ? criarCampanhaDemo(() => colecaoAtual.current) : null), [online?.servico]);
  const [confirmar, setConfirmar] = useState<'luta' | 'partida' | null>(null);
  const guardar = (g: Guardado) => { setGuardado(g); save('pvp', g); };

  const comecar = (npc: Npc, meus: Times) => {
    guardar({ ...guardado, times: meus });
    const seed = crypto.getRandomValues(new Uint32Array(1))[0]!;
    setEtapa({ tipo: 'apresentar', npc, partida: { meus, deles: timesDoNpc(npc.nivel as NivelNpc, seed), rodadas: [], seed } });
  };
  const terminouRodada = (npc: Npc, partida: PartidaPvp, meu: number, dele: number, vencedor: 'player' | 'enemy', rendida = false) => {
    const p: PartidaPvp = { ...partida, rodadas: [...partida.rodadas, { meu, dele, seed: sementeDaRodada(partida.seed, partida.rodadas.length), vencedor: vencedor === 'player' ? 'eu' : 'rival', ...(rendida ? { rendida } : {}) }] };
    const fim = vencedorDaPartida(p);
    if (fim) {
      const atual = guardado.treino[npc.id] ?? { v: 0, d: 0 };
      guardar({ ...guardado, treino: { ...guardado.treino, [npc.id]: fim === 'eu' ? { ...atual, v: atual.v + 1 } : { ...atual, d: atual.d + 1 } } });
      setEtapa({ tipo: 'fim', npc, partida: p });
    } else setEtapa({ tipo: 'rodada', npc, partida: p });
  };
  const desistirDaPartida = (npc: Npc, partida: PartidaPvp) => {
    if (desistir.current) return; desistir.current = true;
    const atual = guardado.treino[npc.id] ?? { v: 0, d: 0 };
    guardar({ ...guardado, treino: { ...guardado.treino, [npc.id]: { ...atual, d: atual.d + 1 } } });
    // desistir conta como derrota: as rodadas que faltavam vão para o rival
    const rodadas = [...partida.rodadas];
    for (const i of timesLivres({ rodadas }, 'rival')) rodadas.push({ meu: 0, dele: i, seed: 0, vencedor: 'rival' });
    setEtapa({ tipo: 'fim', npc, partida: { ...partida, rodadas } });
    window.setTimeout(() => { desistir.current = false; }, 500);
  };

  // as duas desistências do treino (pedido do jogador): na luta, só daquela rodada; na escolha do time, da partida toda
  const confirmaTreino = confirmar && (etapa.tipo === 'luta' || etapa.tipo === 'escolher') && (confirmar === 'luta'
    ? <Confirmar titulo={t('Desistir desta luta?')} texto={t('Você perde esta rodada. A partida continua com os outros times.')} sim={t('Desistir da luta')} onNao={() => setConfirmar(null)}
      onSim={() => { setConfirmar(null); if (etapa.tipo === 'luta') terminouRodada(etapa.npc, etapa.partida, etapa.meu, etapa.dele, 'enemy', true); }} />
    : <Confirmar titulo={t('Abandonar a partida?')} texto={t('Abandonar conta como derrota contra {nome}.', { nome: t(etapa.npc.nome) })} sim={t('Abandonar')} onNao={() => setConfirmar(null)}
      onSim={() => { setConfirmar(null); desistirDaPartida(etapa.npc, etapa.partida); }} />);

  // no PvP com outras pessoas, nem o dono vê as estrelas e a porcentagem (pedido dele: só no treino)
  if (online?.partida) return <DonoDoPvp.Provider value={false}><PartidaOnline key={online.partida} online={online} colecaoLocal={colecaoPvp} emprestados={emprestados} settings={settings} onSettings={onSettings} onDetails={onDetails} onLutando={onLutando} /></DonoDoPvp.Provider>;
  if (etapa.tipo === 'campanha' && servicoDaCampanha) return <Suspense fallback={<p className="cm-carregando-tela">{t('Abrindo o Caminho do Nexus…')}</p>}>
    <CaminhoDoNexus servico={servicoDaCampanha} settings={settings} onSettings={onSettings} onDetails={onDetails} onLutando={onLutando} onVoltar={() => setEtapa({ tipo: 'lobby' })} /></Suspense>;
  if (etapa.tipo === 'lobby' || etapa.tipo === 'campanha') return <Lobby colecao={colecaoPvp} propria={propria} guardado={guardado} online={online} onTreino={(npc) => { som('ui-arena'); setEtapa({ tipo: 'montar', npc }); }} onJogar={onJogar}
    temCampanha={!!servicoDaCampanha} servicoDaCampanha={servicoDaCampanha} onCampanha={() => { som('ui-arena'); setEtapa({ tipo: 'campanha' }); }} />;
  if (etapa.tipo === 'montar') return <Montar melhores={dono} rival={oponenteDoNpc(etapa.npc)} colecao={colecaoPvp} emprestados={emprestados} inicial={guardado.times} onVoltar={() => setEtapa({ tipo: 'lobby' })} onDetails={onDetails} onPronto={(t) => comecar(etapa.npc, t)} />;
  if (etapa.tipo === 'apresentar') return <Apresentar rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onComecar={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  if (etapa.tipo === 'escolher') return <><Escolher rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onEscolher={(meu) => {
    // o NPC "pensa" um pouco antes do VS
    const dele = escolhaDoNpc(etapa.npc.nivel as NivelNpc, etapa.partida, etapa.partida.seed + etapa.partida.rodadas.length * 7919);
    window.setTimeout(() => setEtapa({ tipo: 'vs', npc: etapa.npc, partida: etapa.partida, meu, dele }), 900);
  }} /><button className="pv-sair-online" onClick={() => setConfirmar('partida')}><LogOut size={14} />{t('Abandonar partida')}</button>{confirmaTreino}</>;
  if (etapa.tipo === 'vs') return <Vs rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} meu={etapa.meu} dele={etapa.dele} onLutar={() => setEtapa({ ...etapa, tipo: 'luta' })} />;
  if (etapa.tipo === 'luta') return <><ArenaDoPvp meu={etapa.partida.meus[etapa.meu]!} dele={etapa.partida.deles[etapa.dele]!} seed={sementeDaRodada(etapa.partida.seed, etapa.partida.rodadas.length)}
    rodada={etapa.partida.rodadas.length + 1} rival={t(etapa.npc.nome)} settings={settings} onSettings={onSettings} podePausar velocidadeLivre
    atrasoInicial={etapa.retomar ?? 0} comecaPausado={(etapa.retomar ?? 0) > 0} onTempo={(seg) => guardaEtapa(etapa, seg)}
    onFim={(v) => terminouRodada(etapa.npc, etapa.partida, etapa.meu, etapa.dele, v)} onDesistir={() => setConfirmar('luta')} />{confirmaTreino}</>;
  if (etapa.tipo === 'rodada') return <ResultadoDaRodada rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onSeguir={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  return <Fim npc={etapa.npc} partida={etapa.partida} placar={guardado.treino[etapa.npc.id] ?? { v: 0, d: 0 }} onDeNovo={() => setEtapa({ tipo: 'montar', npc: etapa.npc })} onSair={() => setEtapa({ tipo: 'lobby' })} />;
}
