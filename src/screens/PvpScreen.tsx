import { createContext, lazy, Suspense, useContext, useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { ArrowDownAZ, ArrowLeft, Check, Clock, Handshake, WifiOff, Globe2, Layers, SlidersHorizontal, Sparkles, Crown, Hourglass, Lock, LogOut, RotateCcw, Search, Shield, Swords, Trophy, Users, Wand2, X, Zap } from 'lucide-react';
import { byId, characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { ArenaDoPvp } from '../components/ArenaDoPvp';
import { combosDoTrio } from '../engine/combos';
import { MINIMO_DA_COLECAO, NPCS, duracaoNaTela, escolhaDoNpc, problemaDosTimes, sementeDaRodada, timesDoNpc, timesLivres, vencedorDaPartida, vitoriasDosTimes,
  type Lado, type NivelNpc, type Npc, type PartidaPvp, type Times } from '../engine/pvp';
import { notaDoTrio, estrelasDoTime, melhorQueOsTrios, ESTRELAS_MAXIMAS } from '../presentation/dicas-do-trio';
const ESTRELAS = Array.from({ length: ESTRELAS_MAXIMAS }, (_, k) => k + 1);
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { read, save, type Settings } from '../lib/storage';
import { diferencaDoRelogio, textoDoErroPvp, type JogadorPvp, type RankingPvp, type RespostaPvp, type ServicoPvp, type VistaPvp } from '../lib/pvp-online';
import { corDoNome } from '../lib/comunidade';
import { Avatar } from '../components/AvatarDaComunidade';
import { FAMILIA_DA_IDENTIDADE, ICONE_DA_IDENTIDADE } from '../components/IdentityChips';
import { familiaDaIdentidade, identidadesDe, ordemDasIdentidades, type Identidade } from '../presentation/identities';
import { CartaoDaCampanha } from '../components/CartaoDaCampanha';
import { MINIMO_DA_CAMPANHA } from '../engine/campanha';
import { EMPRESTADOS_POR_DIA, comEmprestados, diaDoEmprestimo, emprestadosDoDia, faltaParaTrocar } from '../engine/emprestimo';
import { criarCampanhaDemo } from '../lib/campanha-demo';
import '../presentation/pvp.css';
import '../presentation/ui-fx.css';

/*
 * O PvP (pedido do jogador). Esta tela tem o Treino contra os 5 NPCs, do Iniciante ao Mestre (src/engine/pvp.ts):
 *  1. escolher o NPC (cada um com rating, coleção e o seu placar contra ele);
 *  2. montar 3 times de 3 com a sua coleção (os personagens liberados nas Conquistas), num álbum de cartas;
 *  3. ver os 3 times dos dois lados;
 *  4. a cada rodada, escolher em segredo um time seu (o NPC escolhe o dele), o VS, e a luta em 2×;
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

export function Rosto({ id, tamanho = 54, apagado = false }: { id: string; tamanho?: number; apagado?: boolean }) {
  const c = byId[id]!;
  return <span className={`pv-rosto ${apagado ? 'apagado' : ''}`} style={{ '--character': c.color, '--t': `${tamanho}px` } as CSSProperties} title={c.name}><Portrait character={c} /></span>;
}

/* A conta do dono (pedido dele): a porcentagem de "melhor que X% dos trios" aparece junto das estrelas. */
const DonoDoPvp = createContext(false);

function CartaoDoTime({ time, i, lado, venceu, escolhido, bloqueado, onClick, compacto = false }: {
  time: readonly string[]; i: number; lado: Lado; venceu?: boolean; escolhido?: boolean; bloqueado?: boolean; onClick?: () => void; compacto?: boolean;
}) {
  const estrelas = estrelasDoTime(time), combos = combosDoTrio(time).combos.length, dono = useContext(DonoDoPvp);
  const Tag = onClick ? 'button' : 'div';
  return <Tag className={`pv-time ${lado} ${venceu ? 'venceu' : ''} ${escolhido ? 'escolhido' : ''} ${bloqueado ? 'bloqueado' : ''} ${compacto ? 'compacto' : ''}`}
    onClick={onClick} disabled={onClick ? bloqueado : undefined} style={{ '--i': i } as CSSProperties}>
    <span className="pv-time-topo"><b>TIME {i + 1}</b>{venceu && <em className="pv-selo-venceu"><Trophy size={12} />VENCEU</em>}</span>
    <span className="pv-time-rostos">{time.map((id) => <Rosto key={id} id={id} tamanho={compacto ? 40 : 52} />)}</span>
    {!compacto && <span className="pv-time-nomes">{time.map((id) => byId[id]!.name).join(' · ')}</span>}
    <span className="pv-time-info">
      <span className="pv-estrelas" aria-label={`Força ${estrelas} de ${ESTRELAS_MAXIMAS}`}>{ESTRELAS.map((k) => <i key={k} className={k <= estrelas ? 'on' : ''}>★</i>)}</span>
      {dono && <span className="pv-pct" title="Melhor que esta porcentagem dos trios">melhor que <b>{melhorQueOsTrios(time)}%</b></span>}
      {combos > 0 && <span className="pv-combos"><Zap size={11} />{combos} combo{combos > 1 ? 's' : ''}</span>}
    </span>
    {venceu && <span className="pv-carimbo" aria-hidden="true"><Check size={34} /></span>}
  </Tag>;
}

function Placar({ partida, rival }: { partida: Pick<PartidaPvp, 'rodadas'>; rival: Oponente }) {
  const v = vitoriasDosTimes(partida);
  return <div className="pv-placar">
    <span className="pv-placar-lado eu"><b>VOCÊ</b><span>{v.eu.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
    <span className="pv-placar-meio"><small>RODADA</small><b>{partida.rodadas.length + 1}</b></span>
    <span className="pv-placar-lado rival" style={{ '--npc': rival.cor } as CSSProperties}><b>{rival.nome.split(' ')[0]!.toUpperCase()}</b><span>{v.rival.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
  </div>;
}

function AvatarDoNpc({ npc, tamanho = 64 }: { npc: Npc; tamanho?: number }) {
  return <span className="pv-npc-avatar" style={{ '--npc': npc.cor, '--t': `${tamanho}px` } as CSSProperties}><Portrait character={byId[npc.avatar]!} /><i>{npc.nivel}</i></span>;
}
/** Quem está do outro lado: um NPC do treino ou uma pessoa (online). As telas da partida são as mesmas. */
export interface Oponente { nome: string; cor: string; avatar: (tamanho: number) => ReactNode; fala?: string }
const oponenteDoNpc = (n: Npc): Oponente => ({ nome: n.nome, cor: n.cor, avatar: (t) => <AvatarDoNpc npc={n} tamanho={t} />, fala: n.fala });

/* ---------------------------------------------------------------------------
 * 1. O lobby
 * ------------------------------------------------------------------------- */

function Lobby({ colecao, propria, guardado, onTreino, onJogar, online, onCampanha, temCampanha }: { colecao: string[]; propria: string[]; guardado: Guardado; onTreino: (n: Npc) => void; onJogar: () => void; online?: Online | null; onCampanha: () => void; temCampanha: boolean }) {
  const falta = Math.max(0, MINIMO_DA_COLECAO - colecao.length);
  return <section className="pv-lobby">
    <header className="pv-topo">
      <Fx nome="holofote" cor="#ffd36b" ms={5200} className="pv-fx-holofote" />
      <span className="pv-logo"><Swords size={30} /></span>
      <div><h1>ARENA PvP</h1><p>3 times de 3 · escolha secreta · vence quem ganhar com os 3</p></div>
    </header>

    {falta > 0 && <div className="pv-trava">
      <Lock size={26} />
      <div><b>Faltam {falta} personagens na sua coleção</b><small>O PvP pede {MINIMO_DA_COLECAO} personagens (3 times de 3). Termine as 10 lutas de uma jornada para liberar o seu trio nas Conquistas.</small>
        <span className="pv-trava-barra"><i style={{ width: `${(100 * colecao.length) / MINIMO_DA_COLECAO}%` }} /></span><em>{colecao.length}/{MINIMO_DA_COLECAO}</em></div>
      <button className="primary" onClick={onJogar}>Jogar</button>
    </div>}

    <CartaoDoEmprestimo propria={propria} />

    {/* a campanha contra os 40 rivais (src/screens/CaminhoDoNexus.tsx): mexe no rating, então pede a conta (e só vale a coleção, sem empréstimo) */}
    <CartaoDaCampanha podeJogar={temCampanha && propria.length >= MINIMO_DA_CAMPANHA} onAbrir={onCampanha}
      motivo={!temCampanha ? 'Entre na sua conta: a campanha mexe no seu rating.' : `A campanha pede ${MINIMO_DA_CAMPANHA} personagens na coleção (você tem ${propria.length}).`} />

    {online ? <CartaoOnline online={online} /> : <div className="pv-modo online">
      <span className="pv-modo-icone"><Users size={24} /></span>
      <div><b>DESAFIO ONLINE</b><small>Entre na sua conta para desafiar alguém pela Comunidade e subir no ranking.</small></div>
      <em className="pv-em-breve"><Lock size={11} />com conta</em>
    </div>}

    <h2 className="pv-secao"><Shield size={16} />TREINO <small>não conta para o ranking nem para o rating</small></h2>
    <div className="pv-npcs">
      {NPCS.map((n, i) => {
        const p = guardado.treino[n.id] ?? { v: 0, d: 0 };
        return <button key={n.id} className="pv-npc" disabled={falta > 0} onClick={() => onTreino(n)} style={{ '--npc': n.cor, '--i': i } as CSSProperties}>
          <AvatarDoNpc npc={n} />
          <span className="pv-npc-texto">
            <small>{n.titulo.toUpperCase()}</small><b>{n.nome}</b>
            <span className="pv-npc-linha"><span className="pv-rating"><Crown size={12} />{n.rating}</span><span className="pv-colecao">{n.colecao} personagens</span></span>
            <span className="pv-npc-fala">“{n.fala}”</span>
          </span>
          <span className="pv-npc-placar"><b className="v">{p.v}V</b><b className="d">{p.d}D</b><span className="pv-caveiras" aria-label={`Dificuldade ${n.nivel} de 5`}>{[1, 2, 3, 4, 5].map((k) => <i key={k} className={k <= n.nivel ? 'on' : ''} />)}</span></span>
        </button>;
      })}
    </div>
  </section>;
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
  return <section className="pv-emprestimo" aria-label="Empréstimo do dia">
    <Fx nome="faiscas" cor="#8fe0ff" ms={4200} className="pv-fx-emprestimo" />
    <header>
      <span className="pv-emprestimo-icone"><Handshake size={24} /></span>
      <div><small>EMPRÉSTIMO DO DIA</small><b>{novos > 0 ? `+${novos} personagens hoje` : 'Você já tem os 9 de hoje!'}</b></div>
      <span className="pv-emprestimo-relogio" title="Troca à meia-noite (Brasília)"><Clock size={13} />{doisDigitos(Math.floor(falta / 3600))}:{doisDigitos(Math.floor((falta % 3600) / 60))}:{doisDigitos(falta % 60)}</span>
    </header>
    <div className="pv-emprestimo-grade">
      {ids.map((id, k) => { const c = byId[id]!, ja = minha.has(id);
        return <span key={id} className={`pv-emprestado ${ja ? 'ja' : 'novo'}`} style={{ '--character': c.color, '--k': k } as CSSProperties}>
          <Rosto id={id} tamanho={58} apagado={ja} /><b>{c.name}</b><em>{ja ? 'já é seu' : 'novo pra você'}</em>
        </span>; })}
    </div>
    <p>{EMPRESTADOS_POR_DIA} personagens sorteados todo dia, os mesmos para todo mundo, para combinar com a sua coleção no Treino e no Desafio online. Amanhã vêm outros.</p>
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

/**
 * "Montar os melhores" (só na conta do dono): os 3 times mais fortes que a coleção permite, pela mesma nota das
 * estrelas. Cada time é buscado à mão de mestre: vários começos sorteados e, em cada um, troca um por um enquanto
 * a nota sobe; fica o melhor. O sorteio dos começos faz sair um jeito diferente a cada toque, sempre entre os fortes.
 */
function timesMaisFortes(colecao: string[]): string[][] | null {
  if (colecao.length < MINIMO_DA_COLECAO) return null;
  const livres = [...colecao], times: string[][] = [];
  const ao = () => { const p = [...livres], t: string[] = []; while (t.length < 3) t.push(p.splice(Math.floor(Math.random() * p.length), 1)[0]!); return t; };
  for (let k = 0; k < 3; k++) {
    let melhor: string[] = ao(), nm = notaDoTrio(melhor);
    for (let r = 0; r < 6; r++) {
      let t = ao(), n = notaDoTrio(t);
      for (let mudou = true, voltas = 0; mudou && voltas < 6; voltas++) {
        mudou = false;
        for (let pos = 0; pos < 3; pos++) for (const c of livres) {
          if (t.includes(c)) continue;
          const novo = t.map((x, j) => (j === pos ? c : x)), nn = notaDoTrio(novo);
          if (nn > n + 1e-9) { t = novo; n = nn; mudou = true; }
        }
      }
      if (n > nm) { melhor = t; nm = n; }
    }
    times.push(melhor);
    for (const id of melhor) livres.splice(livres.indexOf(id), 1);
  }
  return times.sort((a, b) => notaDoTrio(b) - notaDoTrio(a));
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
    (!q || semAcento(c.name).includes(q) || semAcento(c.universe).includes(q))
    && (!f.universos.length || f.universos.includes(c.universe))
    && (!f.funcoes.length || f.funcoes.every((x) => identidadesDe(c).includes(x))));
}
type Personagem = (typeof characters)[number];
function agrupar(lista: Personagem[], ordem: Ordem): { titulo: string; lista: Personagem[] }[] {
  const porNome = [...lista].sort((a, b) => a.name.localeCompare(b.name));
  if (ordem === 'nome') return [{ titulo: '', lista: porNome }];
  const mapa = new Map<string, Personagem[]>();
  for (const c of porNome) {
    const chave = ordem === 'universo' ? c.universe : (ordemDasIdentidades.find((x) => identidadesDe(c).includes(x)) ?? 'Outros');
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
  const unisVisiveis = universos.filter(([u]) => !q || semAcento(u).includes(q));
  const mostrados = todosUni || q ? unisVisiveis : unisVisiveis.slice(0, 18);
  const alterna = <T,>(lista: T[], x: T) => (lista.includes(x) ? lista.filter((y) => y !== x) : [...lista, x]);
  const ativos = filtro.universos.length + filtro.funcoes.length + (filtro.esconderUsados ? 1 : 0);
  const familias = Object.keys(FAMILIA_DA_IDENTIDADE) as (keyof typeof FAMILIA_DA_IDENTIDADE)[];
  // por cima da tela onde o jogador está (a tela anima com transform, e um fixed dentro dela ia parar no fim da página)
  return createPortal(<div className="pv-painel-fundo" onClick={(e) => { if (e.target === e.currentTarget) onFechar(); }}>
    <section className="pv-painel" role="dialog" aria-label="Filtros">
      <span className="pv-painel-alca" aria-hidden="true" />
      <header><SlidersHorizontal size={20} /><b>Filtros</b>{ativos > 0 && <button className="pv-painel-limpar" onClick={() => onFiltro(FILTRO_VAZIO)}>Limpar tudo</button>}<button className="icon-button" onClick={onFechar} aria-label="Fechar"><X size={18} /></button></header>

      <h4><ArrowDownAZ size={14} />ORGANIZAR POR</h4>
      <div className="pv-ordem">
        {([['nome', 'Nome', ArrowDownAZ], ['universo', 'Universo', Globe2], ['funcao', 'Função', Layers]] as const).map(([v, nome, Icone]) =>
          <button key={v} className={filtro.ordem === v ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, ordem: v }); som('toque'); }}><Icone size={18} />{nome}</button>)}
      </div>
      <label className="pv-livres"><input type="checkbox" checked={filtro.esconderUsados} onChange={(e) => onFiltro({ ...filtro, esconderUsados: e.target.checked })} /><span className="pv-chave" aria-hidden="true" />Esconder quem já está num time</label>

      <h4><Sparkles size={14} />FUNÇÃO <small>o que ele faz na luta</small></h4>
      {familias.map((fam) => {
        const lista = ordemDasIdentidades.filter((x) => familiaDaIdentidade[x] === fam && funcoes.has(x));
        if (!lista.length) return null;
        const { nome, cor } = FAMILIA_DA_IDENTIDADE[fam];
        return <div key={fam} className="pv-familia" style={{ '--cor': cor } as CSSProperties}>
          <small>{nome}</small>
          <div className="pv-chips">{lista.map((x) => { const Icone = ICONE_DA_IDENTIDADE[x]; const on = filtro.funcoes.includes(x);
            return <button key={x} className={on ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, funcoes: alterna(filtro.funcoes, x) }); som('toque'); }}><Icone size={14} />{x}<i>{funcoes.get(x)}</i></button>; })}</div>
        </div>;
      })}

      <h4><Globe2 size={14} />UNIVERSO <small>{universos.length} na sua coleção</small></h4>
      {universos.length > 10 && <label className="pv-busca pv-busca-uni"><Search size={14} /><input value={buscaUni} onChange={(e) => setBuscaUni(e.target.value)} placeholder="Procurar universo" aria-label="Procurar universo" /></label>}
      <div className="pv-chips pv-chips-uni">{mostrados.map(([u, n]) => { const on = filtro.universos.includes(u);
        return <button key={u} className={on ? 'on' : ''} onClick={() => { onFiltro({ ...filtro, universos: alterna(filtro.universos, u) }); som('toque'); }}>{u}<i>{n}</i></button>; })}</div>
      {!todosUni && !q && unisVisiveis.length > 18 && <button className="pv-ver-todos" onClick={() => setTodosUni(true)}>Ver os {unisVisiveis.length} universos</button>}

      <footer><button className="primary pv-grande" onClick={onFechar}><Check size={20} />Ver {total} personage{total === 1 ? 'm' : 'ns'}</button></footer>
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
  /** Só na conta do dono (pedido dele): um botão que monta os times mais fortes possíveis com a coleção. */
  melhores?: boolean }) {
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
  const osMelhores = () => { const s = timesMaisFortes(colecao); if (s) { setTimes(s); setAtivo(0); som('pronto'); } };

  return <section className="pv-montar">
    <header className="pv-subtopo">
      <button className="icon-button" onClick={onVoltar} aria-label="Voltar"><ArrowLeft size={20} /></button>
      <div><small>CONTRA {rival.nome.toUpperCase()}</small><h1>Monte seus 3 times</h1></div>
      {rival.avatar(44)}
    </header>
    {prazo}
    {aviso}
    {/* os 3 times e o PRONTO ficam presos no topo enquanto o álbum rola (pedido do jogador: ver o time enquanto troca) */}
    <div className="pv-fixos">
    <div className="pv-slots">
      {times.map((t, i) => {
        const estrelas = t.length === 3 ? estrelasDoTime(t) : 0;
        return <button key={i} className={`pv-slot ${ativo === i ? 'ativo' : ''} ${t.length === 3 ? 'cheio' : ''}`} onClick={() => setAtivo(i)} style={{ '--i': i } as CSSProperties}>
          <span className="pv-slot-topo"><b>TIME {i + 1}</b>{t.length === 3 ? <span className="pv-estrelas" aria-label={`Força ${estrelas} de ${ESTRELAS_MAXIMAS}`}>{ESTRELAS.map((k) => <i key={k} className={k <= estrelas ? 'on' : ''}>★</i>)}{melhores && <em className="pv-pct">{melhorQueOsTrios(t)}%</em>}</span> : <small>{t.length}/3</small>}</span>
          <span className="pv-slot-rostos">{[0, 1, 2].map((k) => t[k] ? <span key={k} className="pv-slot-cheio" role="button" tabIndex={0} aria-label={`Tirar ${byId[t[k]!]!.name}`} onClick={(e) => { e.stopPropagation(); tocar(t[k]!); }}><Rosto id={t[k]!} tamanho={46} /><X size={12} className="pv-tirar" /></span> : <span key={k} className="pv-slot-vazio">+</span>)}</span>
        </button>;
      })}
    </div>
    <div className="pv-pronto-topo">
      {problema && <small className="pv-problema">{problema}</small>}
      <button className="primary pv-pronto" disabled={!cheios || !!problema || ocupado} onClick={() => { som('pronto'); onPronto(times as Times); }}><Check size={20} />{ocupado ? 'Entrando…' : cheios ? 'PRONTO' : `Faltam ${9 - times.flat().length}`}</button>
    </div>
    </div>
    <div className="pv-ferramentas">
      <label className="pv-busca"><Search size={16} /><input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder={`Procurar entre ${colecao.length} personagens`} aria-label="Procurar personagem" />{busca && <button className="pv-limpar-busca" onClick={() => setBusca('')} aria-label="Limpar a busca"><X size={14} /></button>}</label>
      <button className={`secondary pv-filtros-botao ${ativos ? 'ativo' : ''}`} onClick={() => { setPainel(true); som('toque'); }}><SlidersHorizontal size={16} />Filtros{ativos > 0 && <i>{ativos}</i>}</button>
      <button className="secondary pv-sozinho" onClick={sozinho}><Wand2 size={16} />Montar ao acaso</button>
      {melhores && <button className="secondary pv-melhores" onClick={osMelhores}><Crown size={16} />Montar os melhores</button>}
      {quantosEmprestados > 0 && <button className={`secondary pv-so-emprestados ${soEmprestados ? 'ativo' : ''}`} onClick={() => { setSoEmprestados(!soEmprestados); som('toque'); }}><Handshake size={16} />Emprestados<i>{quantosEmprestados}</i></button>}
    </div>
    {ativos > 0 && <div className="pv-filtros-ativos">
      {filtro.funcoes.map((f) => { const Icone = ICONE_DA_IDENTIDADE[f]; return <button key={f} style={{ '--cor': FAMILIA_DA_IDENTIDADE[familiaDaIdentidade[f]].cor } as CSSProperties} onClick={() => setFiltro({ ...filtro, funcoes: filtro.funcoes.filter((x) => x !== f) })}><Icone size={12} />{f}<X size={12} /></button>; })}
      {filtro.universos.map((u) => <button key={u} style={{ '--cor': '#8fd3ff' } as CSSProperties} onClick={() => setFiltro({ ...filtro, universos: filtro.universos.filter((x) => x !== u) })}><Globe2 size={12} />{u}<X size={12} /></button>)}
      {filtro.esconderUsados && <button style={{ '--cor': '#c8f560' } as CSSProperties} onClick={() => setFiltro({ ...filtro, esconderUsados: false })}>Só os livres<X size={12} /></button>}
    </div>}
    {grupos.map((g) => <div key={g.titulo || 'todos'} className="pv-grupo">
      {g.titulo && <h3 className="pv-grupo-titulo"><span>{g.titulo}</span><small>{g.lista.length}</small></h3>}
      <div className="pv-album">
        {g.lista.filter((c) => !filtro.esconderUsados || !usados.has(c.id)).map((c, k) => {
          const onde = usados.get(c.id);
          const emprestado = !!emprestados?.has(c.id);
          return <button key={c.id} className={`pv-carta ${onde !== undefined ? 'usada' : ''} ${emprestado ? 'emprestada' : ''}`} onClick={() => tocar(c.id)} onContextMenu={(e) => { e.preventDefault(); onDetails(c.id); }} style={{ '--character': c.color, '--k': Math.min(k, 30) } as CSSProperties} aria-label={`${c.name}${onde !== undefined ? `, no time ${onde + 1}` : ''}`}>
            <Portrait character={c} /><b>{c.name}</b>{onde !== undefined && <em>T{onde + 1}</em>}{emprestado && <span className="pv-fita"><Handshake size={10} />EMPRESTADO</span>}
          </button>;
        })}
      </div>
    </div>)}
    {!lista.length && <div className="pv-nada"><Search size={28} /><b>Ninguém com esses filtros</b><button className="secondary" onClick={() => { setFiltro(FILTRO_VAZIO); setBusca(''); }}>Limpar filtros</button></div>}
    {painel && <PainelDeFiltros colecao={colecao} filtro={filtro} total={lista.length} onFiltro={setFiltro} onFechar={() => setPainel(false)} />}
  </section>;
}

/* ---------------------------------------------------------------------------
 * 3–8. A partida
 * ------------------------------------------------------------------------- */

export function Apresentar({ rival, partida, onComecar }: { rival: Oponente; partida: Pick<PartidaPvp, 'meus' | 'deles'>; onComecar: () => void }) {
  return <section className="pv-apresentar">
    <div className="pv-frente">
      <div className="pv-lado eu"><span className="pv-nome-lado">VOCÊ</span>{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" compacto />)}</div>
      <span className="pv-vs-pequeno">VS</span>
      <div className="pv-lado rival" style={{ '--npc': rival.cor } as CSSProperties}><span className="pv-nome-lado">{rival.avatar(34)}{rival.nome}</span>{partida.deles.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="rival" compacto />)}</div>
    </div>
    {rival.fala && <p className="pv-fala" style={{ '--npc': rival.cor } as CSSProperties}><b>{rival.nome}:</b> “{rival.fala}”</p>}
    <button className="primary pv-grande" onClick={onComecar}><Swords size={22} />COMEÇAR PARTIDA</button>
  </section>;
}

export function Escolher({ rival, partida, onEscolher, jaEscolhido, prazo }: { rival: Oponente; partida: PartidaPvp; onEscolher: (i: number) => void; jaEscolhido?: number | null; prazo?: ReactNode }) {
  const livres = timesLivres(partida, 'eu'), v = vitoriasDosTimes(partida);
  const [sel, setSel] = useState<number | null>(jaEscolhido ?? (livres.length === 1 ? livres[0]! : null));
  const [pensando, setPensando] = useState(jaEscolhido !== undefined && jaEscolhido !== null);
  return <section className="pv-escolher">
    <Placar partida={partida} rival={rival} />
    {prazo}
    <h2 className="pv-titulo-rodada">Escolha seu time <small>em segredo: {rival.nome} escolhe ao mesmo tempo</small></h2>
    <div className="pv-escolhas">{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" venceu={v.eu[i]} bloqueado={!livres.includes(i)} escolhido={sel === i} onClick={pensando ? undefined : () => { setSel(i); som('toque'); }} />)}</div>
    <div className="pv-rival-pensa" style={{ '--npc': rival.cor } as CSSProperties}>
      {rival.avatar(38)}
      <span>{pensando ? `${rival.nome} está escolhendo…` : `${rival.nome} tem ${timesLivres(partida, 'rival').length} ${timesLivres(partida, 'rival').length === 1 ? 'time' : 'times'} para escolher`}</span>
      <span className="pv-mini-times">{partida.deles.map((t, i) => <span key={i} className={v.rival[i] ? 'venceu' : ''}>{t.map((id) => <Rosto key={id} id={id} tamanho={22} apagado={v.rival[i]} />)}</span>)}</span>
    </div>
    <button className="primary pv-grande" disabled={sel === null || pensando} onClick={() => { setPensando(true); som('ui-confirma'); onEscolher(sel!); }}>
      <Check size={20} />{pensando ? 'Confirmado…' : 'CONFIRMAR TIME'}
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
    <div className="pv-vs-lado rival"><small>{rival.nome.toUpperCase()} · TIME {dele + 1}</small>{partida.deles[dele]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{byId[id]!.name}</b></span>)}</div>
    <span className="pv-vs-centro"><Fx nome="choque" cor="#ffb84d" ms={950} laco={false} className="pv-fx-choque" /><span className="pv-vs-letras" aria-label="Versus">VS</span></span>
    <div className="pv-vs-lado eu"><small>VOCÊ · TIME {meu + 1}</small>{partida.meus[meu]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{byId[id]!.name}</b></span>)}</div>
    {controle ?? <button className="pv-vs-contagem" onClick={onLutar} aria-label="Começar o duelo agora"><b key={conta}>{conta > 0 ? conta : 'LUTA!'}</b><small>toque para começar</small></button>}
  </section>;
}

export function ResultadoDaRodada({ rival, partida, onSeguir, final = false }: { rival: Oponente; partida: PartidaPvp; onSeguir: () => void; final?: boolean }) {
  const r = partida.rodadas.at(-1)!, ganhei = r.vencedor === 'eu', time = ganhei ? partida.meus[r.meu]! : partida.deles[r.dele]!;
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  return <section className={`pv-resultado ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    <span className="pv-brilho" aria-hidden="true" />
    <small>RODADA {partida.rodadas.length}</small>
    <h1>{ganhei ? 'VOCÊ VENCEU!' : `${rival.nome} venceu`}</h1>
    <p>{r.rendida ? (ganhei ? `${rival.nome} desistiu desta luta. ` : 'Você desistiu desta luta. ') : ''}{ganhei ? `O time ${r.meu + 1} ganhou a medalha e fica marcado.` : `O time ${r.dele + 1} dele fica marcado. Você pode usar qualquer time de novo.`}</p>
    <div className="pv-resultado-time">{time.map((id) => <Rosto key={id} id={id} tamanho={64} />)}</div>
    <Placar partida={partida} rival={rival} />
    <button className="primary pv-grande" onClick={onSeguir}>{final ? <><Trophy size={20} />VER RESULTADO</> : <><Swords size={20} />PRÓXIMA RODADA</>}</button>
  </section>;
}

function Fim({ npc, partida, placar, onDeNovo, onSair }: { npc: Npc; partida: PartidaPvp; placar: { v: number; d: number }; onDeNovo: () => void; onSair: () => void }) {
  const ganhei = vencedorDaPartida(partida) === 'eu';
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  return <section className={`pv-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': npc.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <span className="pv-fim-trofeu">{ganhei ? <Trophy size={58} /> : <Shield size={58} />}</span>
    <small>TREINO · {npc.titulo.toUpperCase()}</small>
    <h1>{ganhei ? 'VITÓRIA!' : 'DERROTA'}</h1>
    <p>{ganhei ? `Você venceu ${npc.nome} com os 3 times.` : `${npc.nome} venceu com os 3 times dele. Treine mais um pouco!`}</p>
    <div className="pv-fim-rodadas">{partida.rodadas.map((r, i) => <span key={i} className={r.vencedor}><b>{i + 1}</b>{r.vencedor === 'eu' ? 'V' : 'D'}</span>)}</div>
    <div className="pv-fim-placar"><AvatarDoNpc npc={npc} tamanho={40} /><span>Seu placar contra {npc.nome}</span><b className="v">{placar.v}V</b><b className="d">{placar.d}D</b></div>
    <small className="pv-nota">Treino não muda o rating nem o ranking.</small>
    <div className="pv-fim-botoes"><button className="primary" onClick={onDeNovo}><RotateCcw size={18} />Jogar de novo</button><button className="secondary" onClick={onSair}>Voltar</button></div>
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
function CartaoOnline({ online }: { online: Online }) {
  const [rank, setRank] = useState<RankingPvp | null>(null);
  const [aberta, setAberta] = useState<VistaPvp | null>(null);
  const [erro, setErro] = useState('');
  const [todos, setTodos] = useState(false);
  useEffect(() => {
    let vivo = true;
    void online.servico.ranking().then((r) => { if (vivo) setRank(r); }).catch((e) => { if (vivo) setErro(textoDoErroPvp(e)); });
    void online.servico.consultar().then((r) => { if (vivo) setAberta(r.partida); }).catch(() => undefined);
    return () => { vivo = false; };
  }, [online.servico]);
  const eu = rank?.eu, lista = rank ? (todos ? rank.ranking : rank.ranking.slice(0, 5)) : [];
  return <div className="pv-online">
    <div className="pv-modo online">
      <span className="pv-modo-icone"><Users size={24} /></span>
      <div><b>DESAFIO ONLINE</b><small>Toque no nome de alguém na Comunidade e desafie. Vale rating e ranking.</small></div>
      <span className="pv-meu-rating"><Crown size={13} /><b>{eu?.rating ?? '—'}</b><small>{eu ? `${eu.vitorias}V ${eu.derrotas}D` : 'rating'}</small></span>
    </div>
    {aberta && ['convite', 'montando', 'jogando'].includes(aberta.fase) && <button className="pv-voltar-partida" onClick={() => online.onPartida(aberta.id)}>
      <Avatar id={aberta.rival.id} nome={aberta.rival.nome} tamanho={34} online />
      <span><b>Partida contra {aberta.rival.nome}</b><small>{aberta.fase === 'convite' ? (aberta.desafiante ? 'esperando aceitar' : 'te desafiou!') : aberta.fase === 'montando' ? 'montando os times' : `rodada ${aberta.rodada + 1}`}</small></span>
      <em>VOLTAR</em>
    </button>}
    <button className="primary pv-desafiar" onClick={online.onComunidade}><Swords size={18} />Desafiar alguém na Comunidade</button>
    <div className="pv-ranking">
      <h3><Trophy size={15} />RANKING PvP</h3>
      {erro && <small className="pv-problema">{erro}</small>}
      {rank && !rank.ranking.length && <small className="pv-vazio">Ninguém jogou ainda. Seja o primeiro!</small>}
      <ol>{lista.map((r) => <li key={r.id} className={r.posicao <= 3 ? `top${r.posicao}` : ''}>
        <i>{r.posicao}</i><Avatar id={r.id} nome={r.nome} tamanho={26} online={false} /><b>{r.nome}</b><small>{r.vitorias}V {r.derrotas}D</small><em><Crown size={11} />{r.rating}</em>
      </li>)}</ol>
      {rank && rank.ranking.length > 5 && <button className="pv-ver-todos" onClick={() => setTodos(!todos)}>{todos ? 'Ver menos' : `Ver os ${rank.ranking.length}`}</button>}
    </div>
  </div>;
}

/** Uma confirmação simples por cima da tela (sair da partida). */
export function Confirmar({ titulo, texto, sim, onSim, onNao }: { titulo: string; texto: string; sim: string; onSim: () => void; onNao: () => void }) {
  return createPortal(<div className="pv-confirmar" role="alertdialog" aria-label={titulo}>
    <div><b>{titulo}</b><p>{texto}</p><span><button className="secondary" onClick={onNao}>Continuar</button><button className="primary pv-perigo" onClick={onSim}><LogOut size={16} />{sim}</button></span></div>
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
    {onSair && <button className="secondary" onClick={onSair}><X size={16} />{sair ?? 'Cancelar'}</button>}
  </section>;
}

/** O rival caiu: a partida segue, e ele tem um tempo para voltar (pedido do jogador: 45 s; senão a vitória é sua). */
function RivalCaiu({ nome, falta, desde }: { nome: string; falta: number; desde: number }) {
  const agora = useAgora(true, 500), s = Math.max(0, Math.ceil(falta - (agora - desde) / 1000));
  return createPortal(<div className="pv-caiu" role="status"><WifiOff size={18} /><span><b>{nome} desconectou</b><small>{s > 0 ? `tem ${mmss(s)} para voltar, senão a vitória é sua` : 'a vitória é sua…'}</small></span><em>{s}</em></div>, document.body);
}

function FimOnline({ v, rival, onSair }: { v: VistaPvp; rival: Oponente; onSair: () => void }) {
  const ganhei = v.vencedor === 'eu', delta = v.delta ?? 0;
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  const porDesistencia = v.motivo === 'desistiu', porQueda = v.motivo === 'desconectou';
  return <section className={`pv-fim ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': rival.cor } as CSSProperties}>
    {ganhei && <span className="pv-confete" aria-hidden="true">{Array.from({ length: 24 }, (_, i) => <i key={i} style={{ '--i': i } as CSSProperties} />)}</span>}
    {ganhei && <><Fx nome="raios" cor="#ffd36b" ms={5200} className="pv-fx-raios" /><Fx nome="faiscas" cor="#fff3b0" ms={4200} className="pv-fx-faiscas" /></>}
    <span className="pv-fim-trofeu">{ganhei ? <Trophy size={58} /> : <Shield size={58} />}</span>
    <small>DESAFIO ONLINE · VALENDO RATING</small>
    <h1>{ganhei ? 'VITÓRIA!' : 'DERROTA'}</h1>
    <p>{porQueda ? (ganhei ? `${rival.nome} desconectou e não voltou em ${v.ausenciaMaxima} s.` : `Você ficou desconectado mais de ${v.ausenciaMaxima} s.`) : porDesistencia ? (ganhei ? `${rival.nome} abandonou a partida.` : 'Você abandonou a partida.') : ganhei ? `Você venceu ${rival.nome} com os 3 times.` : `${rival.nome} venceu com os 3 times.`}</p>
    {v.rodadas.length > 0 && <div className="pv-fim-rodadas">{v.rodadas.map((r) => <span key={r.n} className={r.vencedor}><b>{r.n + 1}</b>{r.vencedor === 'eu' ? 'V' : 'D'}</span>)}</div>}
    <div className="pv-fim-rating">
      <Crown size={22} /><span><small>SEU RATING</small><b>{v.voce.rating}</b></span>
      <em className={delta >= 0 ? 'sobe' : 'desce'}>{delta >= 0 ? '+' : ''}{delta}</em>
      <span className="pv-fim-vd"><b className="v">{v.voce.vitorias}V</b><b className="d">{v.voce.derrotas}D</b></span>
    </div>
    <div className="pv-fim-botoes"><button className="primary" onClick={onSair}><Trophy size={18} />Ver o ranking</button></div>
  </section>;
}

/** O que este aparelho já mostrou da partida: a apresentação e as lutas assistidas (para não repetir ao voltar). */
interface Assistido { id: string; apresentado: boolean; vistas: number[] }
const lerAssistido = (id: string): Assistido => {
  const a = read('pvp-online') as Assistido | null;
  return a && a.id === id && Array.isArray(a.vistas) ? a : { id, apresentado: false, vistas: [] };
};

type Cena = { tipo: 'luta'; n: number; meu: string[]; dele: string[]; seed: number; atraso: number } | { tipo: 'resultado'; n: number } | null;

function PartidaOnline({ online, colecaoLocal, emprestados, settings, onSettings, onDetails, onLutando, dono = false }: {
  online: Online; colecaoLocal: string[]; emprestados?: ReadonlySet<string>; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onLutando: (sim: boolean) => void;
  dono?: boolean;
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

  const aplica = (r: RespostaPvp) => {
    if (!r.partida) { setSumiu(true); return; }
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
  const inicio = v?.inicioEm ? Date.parse(v.inicioEm) - offset : null;
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
  if (sumiu) return <Espera rival={{ nome: 'Partida', cor: '#8fd3ff', avatar: () => <Swords size={60} /> }} titulo="Partida não encontrada" texto="Ela pode ter acabado." onSair={voltar} sair="Voltar" />;
  if (!v || !rival) return <section className="pv-espera"><p className="cm-carregando-tela">{erro || 'Abrindo a partida…'}</p>{erro && <button className="secondary" onClick={voltar}>Voltar</button>}</section>;
  const aviso = erro ? <p className="pv-problema pv-erro-online">{erro}</p> : null;
  const caiu = v.ausencia !== null && (v.fase === 'jogando' || v.fase === 'montando') ? <RivalCaiu nome={v.rival.nome} falta={v.ausenciaMaxima - v.ausencia} desde={recebido} /> : null;
  const confirmaSair = <>{caiu}{sair && <Confirmar titulo={v.fase === 'jogando' ? 'Abandonar a partida?' : 'Sair da partida?'}
    texto={v.fase === 'jogando' ? `Abandonar conta como derrota e ${v.rival.nome} ganha o rating.` : 'A partida é cancelada e ninguém perde rating.'}
    sim={v.fase === 'jogando' ? 'Abandonar' : 'Sair'} onNao={() => setSair(false)} onSim={() => { setSair(false); void agir(servico.desistir(id)); }} />}</>;

  // fora de jogo: convite recusado, cancelado ou expirado
  if (v.fase === 'recusada' || v.fase === 'cancelada' || v.fase === 'expirada')
    return <Espera rival={rival} titulo={v.fase === 'recusada' ? 'Desafio recusado' : v.fase === 'expirada' ? 'O convite expirou' : 'Partida cancelada'} texto={v.motivo ?? 'Ninguém perdeu rating.'} onSair={voltar} sair="Voltar" />;

  if (v.fase === 'convite') {
    if (v.desafiante) return <><Espera rival={rival} titulo="Desafio enviado!" texto={`Esperando ${v.rival.nome} aceitar…`} prazo={<Prazo ate={v.prazo} offset={offset} texto=" para aceitar" />} onSair={() => void agir(servico.desistir(id))} sair="Cancelar desafio">
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {v.rival.vitorias}V {v.rival.derrotas}D</span>{aviso}</Espera></>;
    return <Espera rival={rival} titulo={`${v.rival.nome} te desafiou!`} texto="3 times de 3, escolha secreta, vale rating." prazo={<Prazo ate={v.prazo} offset={offset} texto=" para responder" />}>
      <span className="pv-rating-rival"><Crown size={13} />{v.rival.rating} · {v.rival.vitorias}V {v.rival.derrotas}D</span>{aviso}
      <span className="pv-convite-botoes"><button className="secondary" onClick={() => void agir(servico.responder(id, false))}><X size={18} />Recusar</button><button className="primary" onClick={() => { som('ui-arena'); void agir(servico.responder(id, true)); }}><Swords size={18} />Aceitar</button></span>
    </Espera>;
  }

  if (v.fase === 'montando') {
    if (!v.pronto.eu) return <>{<Montar key={falhas} rival={rival} colecao={colecao} emprestados={emprestados} inicial={guardado.times} onDetails={onDetails} melhores={dono} onVoltar={() => setSair(true)}
      prazo={<>{<Prazo ate={v.prazo} offset={offset} texto={v.pronto.rival ? ` · ${v.rival.nome} já está pronto!` : ' para montar'} />}{aviso}</>}
      onPronto={(t) => { save('pvp', { ...carregar(), times: t }); void agir(servico.times(id, t)); }} />}{confirmaSair}</>;
    return <><Espera rival={rival} titulo="Seus times estão prontos" texto={`Esperando ${v.rival.nome} montar os times…`} prazo={<Prazo ate={v.prazo} offset={offset} texto=" para montar" />} onSair={() => setSair(true)} sair="Sair">
      {v.meusTimes && <div className="pv-espera-times">{v.meusTimes.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" compacto />)}</div>}{aviso}
    </Espera>{confirmaSair}</>;
  }

  // jogando ou terminada
  const meus = v.meusTimes ?? [[], [], []], deles = v.timesDele ?? [[], [], []];
  const naTela = (r: typeof v.rodadas[number]) => ({ meu: r.meu, dele: r.dele, seed: r.seed, vencedor: r.vencedor });
  const vistas = v.rodadas.filter((r) => r.n !== pendente?.n).map(naTela);
  const partida: PartidaPvp = { meus: meus as unknown as Times, deles: deles as unknown as Times, seed: v.seed, rodadas: vistas };

  if (cena?.tipo === 'luta') return <>{<ArenaDoPvp key={cena.n} meu={cena.meu} dele={cena.dele} seed={cena.seed} rodada={cena.n + 1} rival={v.rival.nome} settings={settings} onSettings={onSettings}
    podePausar={false} espelhado={!v.desafiante} atrasoInicial={cena.atraso} onFim={() => setCena({ tipo: 'resultado', n: cena.n })} onDesistir={() => setRenderLuta(true)} />}{confirmaSair}
    {renderLuta && <Confirmar titulo="Desistir desta luta?" texto="Você perde esta rodada. A partida continua com os outros times." sim="Desistir da luta" onNao={() => setRenderLuta(false)}
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
      ? <div className="pv-vs-contagem"><b key={conta}>{conta > 0 ? conta : 'LUTA!'}</b><small>a luta começa nos dois aparelhos</small></div>
      : <div className="pv-vs-contagem esperando"><Hourglass size={26} />
        <small>{v.lutar.rival ? `${v.rival.nome} já está vendo a tela. Começando…` : `Esperando ${v.rival.nome} abrir a tela da luta…`}</small>
        <small className="pv-pronto-rival"><Check size={13} />A luta só começa com os dois vendo a tela</small></div>;
    return <><Vs rival={rival} partida={partida} meu={pendente.meu} dele={pendente.dele} onLutar={() => undefined} controle={<>{controle}{aviso}</>} />{confirmaSair}</>;
  }

  return <>{<Escolher key={`${v.rodada}-${falhas}`} rival={rival} partida={partida} jaEscolhido={v.minhaEscolha}
    prazo={<>{<Prazo ate={v.prazo} offset={offset} texto={v.escolheu.rival ? ` · ${v.rival.nome} já escolheu!` : v.assistiu && !v.assistiu.rival && v.rodadas.length ? ` · ${v.rival.nome} ainda vê a luta` : ' para escolher'} />}{aviso}</>}
    onEscolher={(i) => void agir(servico.escolher(id, v.rodada, i))} />}
    <button className="pv-sair-online" onClick={() => setSair(true)}><LogOut size={14} />Abandonar partida</button>{confirmaSair}</>;
}

/* ---------------------------------------------------------------------------
 * A tela
 * ------------------------------------------------------------------------- */

const CaminhoDoNexus = lazy(() => import('./CaminhoDoNexus'));
/* A campanha sem servidor (VITE_CAMPANHA_DEMO=true): só para testar as telas; nunca no jogo publicado. */
const CAMPANHA_DEMO = import.meta.env.VITE_CAMPANHA_DEMO === 'true';

export function PvpScreen(props: Parameters<typeof TelaDoPvp>[0]) {
  return <DonoDoPvp.Provider value={props.dono === true}><TelaDoPvp {...props} /></DonoDoPvp.Provider>;
}

function TelaDoPvp({ colecao, settings, onSettings, onDetails, onJogar, onLutando, online, dono = false }: {
  colecao: string[]; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onJogar: () => void; onLutando: (sim: boolean) => void;
  /** O Desafio online (com conta); a partida aberta vem do App (convite aceito, desafio pela Comunidade). */
  online?: Online | null;
  /** A conta do dono: ganha o botão "Montar os melhores". */
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
    ? <Confirmar titulo="Desistir desta luta?" texto={`Você perde esta rodada. A partida continua com os outros times.`} sim="Desistir da luta" onNao={() => setConfirmar(null)}
      onSim={() => { setConfirmar(null); if (etapa.tipo === 'luta') terminouRodada(etapa.npc, etapa.partida, etapa.meu, etapa.dele, 'enemy', true); }} />
    : <Confirmar titulo="Abandonar a partida?" texto={`Abandonar conta como derrota contra ${etapa.npc.nome}.`} sim="Abandonar" onNao={() => setConfirmar(null)}
      onSim={() => { setConfirmar(null); desistirDaPartida(etapa.npc, etapa.partida); }} />);

  if (online?.partida) return <PartidaOnline key={online.partida} online={online} colecaoLocal={colecaoPvp} emprestados={emprestados} settings={settings} onSettings={onSettings} onDetails={onDetails} onLutando={onLutando} dono={dono} />;
  if (etapa.tipo === 'campanha' && servicoDaCampanha) return <Suspense fallback={<p className="cm-carregando-tela">Abrindo o Caminho do Nexus…</p>}>
    <CaminhoDoNexus servico={servicoDaCampanha} settings={settings} onSettings={onSettings} onDetails={onDetails} onLutando={onLutando} dono={dono} onVoltar={() => setEtapa({ tipo: 'lobby' })} /></Suspense>;
  if (etapa.tipo === 'lobby' || etapa.tipo === 'campanha') return <Lobby colecao={colecaoPvp} propria={propria} guardado={guardado} online={online} onTreino={(npc) => { som('ui-arena'); setEtapa({ tipo: 'montar', npc }); }} onJogar={onJogar}
    temCampanha={!!servicoDaCampanha} onCampanha={() => { som('ui-arena'); setEtapa({ tipo: 'campanha' }); }} />;
  if (etapa.tipo === 'montar') return <Montar melhores={dono} rival={oponenteDoNpc(etapa.npc)} colecao={colecaoPvp} emprestados={emprestados} inicial={guardado.times} onVoltar={() => setEtapa({ tipo: 'lobby' })} onDetails={onDetails} onPronto={(t) => comecar(etapa.npc, t)} />;
  if (etapa.tipo === 'apresentar') return <Apresentar rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onComecar={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  if (etapa.tipo === 'escolher') return <><Escolher rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onEscolher={(meu) => {
    // o NPC "pensa" um pouco antes do VS
    const dele = escolhaDoNpc(etapa.npc.nivel as NivelNpc, etapa.partida, etapa.partida.seed + etapa.partida.rodadas.length * 7919);
    window.setTimeout(() => setEtapa({ tipo: 'vs', npc: etapa.npc, partida: etapa.partida, meu, dele }), 900);
  }} /><button className="pv-sair-online" onClick={() => setConfirmar('partida')}><LogOut size={14} />Abandonar partida</button>{confirmaTreino}</>;
  if (etapa.tipo === 'vs') return <Vs rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} meu={etapa.meu} dele={etapa.dele} onLutar={() => setEtapa({ ...etapa, tipo: 'luta' })} />;
  if (etapa.tipo === 'luta') return <><ArenaDoPvp meu={etapa.partida.meus[etapa.meu]!} dele={etapa.partida.deles[etapa.dele]!} seed={sementeDaRodada(etapa.partida.seed, etapa.partida.rodadas.length)}
    rodada={etapa.partida.rodadas.length + 1} rival={etapa.npc.nome} settings={settings} onSettings={onSettings} podePausar
    atrasoInicial={etapa.retomar ?? 0} comecaPausado={(etapa.retomar ?? 0) > 0} onTempo={(seg) => guardaEtapa(etapa, seg)}
    onFim={(v) => terminouRodada(etapa.npc, etapa.partida, etapa.meu, etapa.dele, v)} onDesistir={() => setConfirmar('luta')} />{confirmaTreino}</>;
  if (etapa.tipo === 'rodada') return <ResultadoDaRodada rival={oponenteDoNpc(etapa.npc)} partida={etapa.partida} onSeguir={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  return <Fim npc={etapa.npc} partida={etapa.partida} placar={guardado.treino[etapa.npc.id] ?? { v: 0, d: 0 }} onDeNovo={() => setEtapa({ tipo: 'montar', npc: etapa.npc })} onSair={() => setEtapa({ tipo: 'lobby' })} />;
}
