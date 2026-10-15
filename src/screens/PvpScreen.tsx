import { useEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { ArrowLeft, Check, Crown, Lock, RotateCcw, Search, Shield, Swords, Trophy, Users, Wand2, X, Zap } from 'lucide-react';
import { byId, characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { ArenaDoPvp } from '../components/ArenaDoPvp';
import { combosDoTrio } from '../engine/combos';
import { MINIMO_DA_COLECAO, NPCS, escolhaDoNpc, problemaDosTimes, sementeDaRodada, sugerirTimes, timesDoNpc, timesLivres, vencedorDaPartida, vitoriasDosTimes,
  type Lado, type NivelNpc, type Npc, type PartidaPvp, type Times } from '../engine/pvp';
import { notaDoTrio } from '../presentation/dicas-do-trio';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { read, save, type Settings } from '../lib/storage';
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
 * O Desafio online (outra pessoa) usa estas mesmas telas.
 */

interface Guardado { treino: Record<string, { v: number; d: number }>; times?: string[][] }
const carregar = (): Guardado => {
  const g = read('pvp') as Guardado | null;
  return { treino: g && typeof g.treino === 'object' && g.treino ? g.treino : {}, times: Array.isArray(g?.times) ? g!.times : undefined };
};
/** Os efeitos de interface desenhados em Python (tools/ui/generate_ui_fx.py): choque, holofote, raios, faíscas. */
const Fx = ({ nome, cor, ms, className, laco = true }: { nome: string; cor: string; ms: number; className: string; laco?: boolean }) =>
  <span aria-hidden className={`uifx ${laco ? 'uifx-laco' : ''} ${className}`} style={{ '--uifx-img': `url(/assets/ui/fx/${nome}.webp)`, '--uifx-cor': cor, '--uifx-dur': `${ms}ms` } as CSSProperties} />;
const som = (nome: 'toque' | 'pronto' | 'ui-confirma' | 'ui-arena' | 'vitoria' | 'derrota') => battleAudio.sound(nome, PRIORIDADE.interface);

/** A força de um time de 0 a 100 (a nota das Dicas, que vai de ~-2 a ~8). */
const forcaDoTime = (t: readonly string[]) => Math.max(4, Math.min(100, Math.round(((notaDoTrio(t) + 2) / 10) * 100)));
const estrelasDaForca = (f: number) => Math.max(1, Math.min(5, Math.ceil(f / 20)));

type Etapa =
  | { tipo: 'lobby' }
  | { tipo: 'montar'; npc: Npc }
  | { tipo: 'apresentar'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'escolher'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'vs'; npc: Npc; partida: PartidaPvp; meu: number; dele: number }
  | { tipo: 'luta'; npc: Npc; partida: PartidaPvp; meu: number; dele: number }
  | { tipo: 'rodada'; npc: Npc; partida: PartidaPvp }
  | { tipo: 'fim'; npc: Npc; partida: PartidaPvp };

/* ---------------------------------------------------------------------------
 * Peças
 * ------------------------------------------------------------------------- */

function Rosto({ id, tamanho = 54, apagado = false }: { id: string; tamanho?: number; apagado?: boolean }) {
  const c = byId[id]!;
  return <span className={`pv-rosto ${apagado ? 'apagado' : ''}`} style={{ '--character': c.color, '--t': `${tamanho}px` } as CSSProperties} title={c.name}><Portrait character={c} /></span>;
}

function CartaoDoTime({ time, i, lado, venceu, escolhido, bloqueado, onClick, compacto = false }: {
  time: readonly string[]; i: number; lado: Lado; venceu?: boolean; escolhido?: boolean; bloqueado?: boolean; onClick?: () => void; compacto?: boolean;
}) {
  const forca = forcaDoTime(time), combos = combosDoTrio(time).combos.length;
  const Tag = onClick ? 'button' : 'div';
  return <Tag className={`pv-time ${lado} ${venceu ? 'venceu' : ''} ${escolhido ? 'escolhido' : ''} ${bloqueado ? 'bloqueado' : ''} ${compacto ? 'compacto' : ''}`}
    onClick={onClick} disabled={onClick ? bloqueado : undefined} style={{ '--i': i } as CSSProperties}>
    <span className="pv-time-topo"><b>TIME {i + 1}</b>{venceu && <em className="pv-selo-venceu"><Trophy size={12} />VENCEU</em>}</span>
    <span className="pv-time-rostos">{time.map((id) => <Rosto key={id} id={id} tamanho={compacto ? 40 : 52} />)}</span>
    {!compacto && <span className="pv-time-nomes">{time.map((id) => byId[id]!.name).join(' · ')}</span>}
    <span className="pv-time-info">
      <span className="pv-estrelas" aria-label={`Força ${estrelasDaForca(forca)} de 5`}>{[1, 2, 3, 4, 5].map((k) => <i key={k} className={k <= estrelasDaForca(forca) ? 'on' : ''}>★</i>)}</span>
      {combos > 0 && <span className="pv-combos"><Zap size={11} />{combos} combo{combos > 1 ? 's' : ''}</span>}
    </span>
    {venceu && <span className="pv-carimbo" aria-hidden="true"><Check size={34} /></span>}
  </Tag>;
}

function Placar({ partida, npc }: { partida: PartidaPvp; npc: Npc }) {
  const v = vitoriasDosTimes(partida);
  return <div className="pv-placar">
    <span className="pv-placar-lado eu"><b>VOCÊ</b><span>{v.eu.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
    <span className="pv-placar-meio"><small>RODADA</small><b>{partida.rodadas.length + 1}</b></span>
    <span className="pv-placar-lado rival" style={{ '--npc': npc.cor } as CSSProperties}><b>{npc.nome.split(' ')[0]!.toUpperCase()}</b><span>{v.rival.map((x, i) => <i key={i} className={x ? 'on' : ''}><Trophy size={14} /></i>)}</span></span>
  </div>;
}

function AvatarDoNpc({ npc, tamanho = 64 }: { npc: Npc; tamanho?: number }) {
  return <span className="pv-npc-avatar" style={{ '--npc': npc.cor, '--t': `${tamanho}px` } as CSSProperties}><Portrait character={byId[npc.avatar]!} /><i>{npc.nivel}</i></span>;
}

/* ---------------------------------------------------------------------------
 * 1. O lobby
 * ------------------------------------------------------------------------- */

function Lobby({ colecao, guardado, onTreino, onJogar }: { colecao: string[]; guardado: Guardado; onTreino: (n: Npc) => void; onJogar: () => void }) {
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

    <div className="pv-modo online">
      <span className="pv-modo-icone"><Users size={24} /></span>
      <div><b>DESAFIO ONLINE</b><small>Desafie alguém pela Comunidade. Rating de xadrez e ranking com vitórias e derrotas.</small></div>
      <em className="pv-em-breve"><Lock size={11} />em breve</em>
    </div>

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

/* ---------------------------------------------------------------------------
 * 2. Montar os 3 times
 * ------------------------------------------------------------------------- */

function Montar({ npc, colecao, inicial, onPronto, onVoltar, onDetails }: { npc: Npc; colecao: string[]; inicial?: string[][]; onPronto: (t: Times) => void; onVoltar: () => void; onDetails: (id: string) => void }) {
  const valido = (t?: string[][]) => !!t && t.length === 3 && t.every((x) => x.every((id) => colecao.includes(id)));
  const [times, setTimes] = useState<string[][]>(() => (valido(inicial) ? inicial!.map((t) => [...t]) : [[], [], []]));
  const [ativo, setAtivo] = useState(() => Math.max(0, times.findIndex((t) => t.length < 3)));
  const [busca, setBusca] = useState('');
  const usados = new Map(times.flatMap((t, i) => t.map((id) => [id, i] as const)));
  const cheios = times.every((t) => t.length === 3);
  const problema = cheios ? problemaDosTimes(times, new Set(colecao)) : null;
  const lista = useMemo(() => colecao.map((id) => byId[id]!).filter((c) => !busca.trim() || c.name.toLowerCase().includes(busca.trim().toLowerCase())).sort((a, b) => a.name.localeCompare(b.name)), [colecao, busca]);

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
  const sozinho = () => { const s = sugerirTimes(colecao, (Date.now() >>> 0) ^ 0x9e37); if (s) { setTimes(s.map((t) => [...t])); som('pronto'); } };

  return <section className="pv-montar">
    <header className="pv-subtopo">
      <button className="icon-button" onClick={onVoltar} aria-label="Voltar"><ArrowLeft size={20} /></button>
      <div><small>CONTRA {npc.nome.toUpperCase()}</small><h1>Monte seus 3 times</h1></div>
      <AvatarDoNpc npc={npc} tamanho={44} />
    </header>
    <div className="pv-slots">
      {times.map((t, i) => {
        const forca = t.length === 3 ? forcaDoTime(t) : 0;
        return <button key={i} className={`pv-slot ${ativo === i ? 'ativo' : ''} ${t.length === 3 ? 'cheio' : ''}`} onClick={() => setAtivo(i)} style={{ '--i': i } as CSSProperties}>
          <span className="pv-slot-topo"><b>TIME {i + 1}</b>{t.length === 3 ? <span className="pv-estrelas">{[1, 2, 3, 4, 5].map((k) => <i key={k} className={k <= estrelasDaForca(forca) ? 'on' : ''}>★</i>)}</span> : <small>{t.length}/3</small>}</span>
          <span className="pv-slot-rostos">{[0, 1, 2].map((k) => t[k] ? <span key={k} className="pv-slot-cheio" role="button" tabIndex={0} aria-label={`Tirar ${byId[t[k]!]!.name}`} onClick={(e) => { e.stopPropagation(); tocar(t[k]!); }}><Rosto id={t[k]!} tamanho={46} /><X size={12} className="pv-tirar" /></span> : <span key={k} className="pv-slot-vazio">+</span>)}</span>
        </button>;
      })}
    </div>
    <div className="pv-ferramentas">
      <label className="pv-busca"><Search size={16} /><input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder={`Procurar na coleção (${colecao.length})`} aria-label="Procurar personagem" /></label>
      <button className="secondary pv-sozinho" onClick={sozinho}><Wand2 size={16} />Montar sozinho</button>
    </div>
    <div className="pv-album">
      {lista.map((c, k) => {
        const onde = usados.get(c.id);
        return <button key={c.id} className={`pv-carta ${onde !== undefined ? 'usada' : ''}`} onClick={() => tocar(c.id)} onContextMenu={(e) => { e.preventDefault(); onDetails(c.id); }} style={{ '--character': c.color, '--k': Math.min(k, 30) } as CSSProperties} aria-label={`${c.name}${onde !== undefined ? `, no time ${onde + 1}` : ''}`}>
          <Portrait character={c} /><b>{c.name}</b>{onde !== undefined && <em>T{onde + 1}</em>}
        </button>;
      })}
    </div>
    <footer className="pv-rodape">
      {problema && <small className="pv-problema">{problema}</small>}
      <button className="primary pv-pronto" disabled={!cheios || !!problema} onClick={() => { som('pronto'); onPronto(times as Times); }}><Check size={20} />{cheios ? 'PRONTO' : `Faltam ${9 - times.flat().length}`}</button>
    </footer>
  </section>;
}

/* ---------------------------------------------------------------------------
 * 3–8. A partida
 * ------------------------------------------------------------------------- */

function Apresentar({ npc, partida, onComecar }: { npc: Npc; partida: PartidaPvp; onComecar: () => void }) {
  return <section className="pv-apresentar">
    <div className="pv-frente">
      <div className="pv-lado eu"><span className="pv-nome-lado">VOCÊ</span>{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" compacto />)}</div>
      <span className="pv-vs-pequeno">VS</span>
      <div className="pv-lado rival" style={{ '--npc': npc.cor } as CSSProperties}><span className="pv-nome-lado"><AvatarDoNpc npc={npc} tamanho={34} />{npc.nome}</span>{partida.deles.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="rival" compacto />)}</div>
    </div>
    <p className="pv-fala" style={{ '--npc': npc.cor } as CSSProperties}><b>{npc.nome}:</b> “{npc.fala}”</p>
    <button className="primary pv-grande" onClick={onComecar}><Swords size={22} />COMEÇAR PARTIDA</button>
  </section>;
}

function Escolher({ npc, partida, onEscolher }: { npc: Npc; partida: PartidaPvp; onEscolher: (i: number) => void }) {
  const livres = timesLivres(partida, 'eu'), v = vitoriasDosTimes(partida);
  const [sel, setSel] = useState<number | null>(livres.length === 1 ? livres[0]! : null);
  const [pensando, setPensando] = useState(false);
  return <section className="pv-escolher">
    <Placar partida={partida} npc={npc} />
    <h2 className="pv-titulo-rodada">Escolha seu time <small>em segredo: {npc.nome} escolhe ao mesmo tempo</small></h2>
    <div className="pv-escolhas">{partida.meus.map((t, i) => <CartaoDoTime key={i} time={t} i={i} lado="eu" venceu={v.eu[i]} bloqueado={!livres.includes(i)} escolhido={sel === i} onClick={() => { setSel(i); som('toque'); }} />)}</div>
    <div className="pv-rival-pensa" style={{ '--npc': npc.cor } as CSSProperties}>
      <AvatarDoNpc npc={npc} tamanho={38} />
      <span>{pensando ? `${npc.nome} está escolhendo…` : `${npc.nome} tem ${timesLivres(partida, 'rival').length} ${timesLivres(partida, 'rival').length === 1 ? 'time' : 'times'} para escolher`}</span>
      <span className="pv-mini-times">{partida.deles.map((t, i) => <span key={i} className={v.rival[i] ? 'venceu' : ''}>{t.map((id) => <Rosto key={id} id={id} tamanho={22} apagado={v.rival[i]} />)}</span>)}</span>
    </div>
    <button className="primary pv-grande" disabled={sel === null || pensando} onClick={() => { setPensando(true); som('ui-confirma'); window.setTimeout(() => onEscolher(sel!), 900); }}>
      <Check size={20} />{pensando ? 'Confirmado…' : 'CONFIRMAR TIME'}
    </button>
  </section>;
}

function Vs({ npc, partida, meu, dele, onLutar }: { npc: Npc; partida: PartidaPvp; meu: number; dele: number; onLutar: () => void }) {
  const [conta, setConta] = useState(3);
  useEffect(() => { som('ui-arena'); }, []);
  useEffect(() => { if (conta <= 0) { onLutar(); return; } const t = window.setTimeout(() => { setConta(conta - 1); som('toque'); }, 1000); return () => clearTimeout(t); }, [conta, onLutar]);
  return <section className="pv-vs" style={{ '--npc': npc.cor } as CSSProperties}>
    <span className="pv-vs-raios" aria-hidden="true" />
    <Fx nome="holofote" cor="#ffe2a0" ms={4800} className="pv-fx-holofote-vs" />
    <div className="pv-vs-lado eu"><small>VOCÊ · TIME {meu + 1}</small>{partida.meus[meu]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{byId[id]!.name}</b></span>)}</div>
    <span className="pv-vs-centro"><Fx nome="choque" cor="#ffb84d" ms={950} laco={false} className="pv-fx-choque" /><span className="pv-vs-letras" aria-label="Versus">VS</span></span>
    <div className="pv-vs-lado rival"><small>{npc.nome.toUpperCase()} · TIME {dele + 1}</small>{partida.deles[dele]!.map((id, k) => <span key={id} className="pv-vs-rosto" style={{ '--k': k } as CSSProperties}><Rosto id={id} tamanho={84} /><b>{byId[id]!.name}</b></span>)}</div>
    <button className="pv-vs-contagem" onClick={onLutar} aria-label="Começar o duelo agora"><b key={conta}>{conta > 0 ? conta : 'LUTA!'}</b><small>toque para começar</small></button>
  </section>;
}

function ResultadoDaRodada({ npc, partida, onSeguir }: { npc: Npc; partida: PartidaPvp; onSeguir: () => void }) {
  const r = partida.rodadas.at(-1)!, ganhei = r.vencedor === 'eu', time = ganhei ? partida.meus[r.meu]! : partida.deles[r.dele]!;
  useEffect(() => { som(ganhei ? 'vitoria' : 'derrota'); }, [ganhei]);
  return <section className={`pv-resultado ${ganhei ? 'ganhou' : 'perdeu'}`} style={{ '--npc': npc.cor } as CSSProperties}>
    <span className="pv-brilho" aria-hidden="true" />
    <small>RODADA {partida.rodadas.length}</small>
    <h1>{ganhei ? 'VOCÊ VENCEU!' : `${npc.nome} venceu`}</h1>
    <p>{ganhei ? `O time ${r.meu + 1} ganhou a medalha e fica marcado.` : `O time ${r.dele + 1} dele fica marcado. Você pode usar qualquer time de novo.`}</p>
    <div className="pv-resultado-time">{time.map((id) => <Rosto key={id} id={id} tamanho={64} />)}</div>
    <Placar partida={{ ...partida, rodadas: partida.rodadas }} npc={npc} />
    <button className="primary pv-grande" onClick={onSeguir}><Swords size={20} />PRÓXIMA RODADA</button>
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
 * A tela
 * ------------------------------------------------------------------------- */

export function PvpScreen({ colecao, settings, onSettings, onDetails, onJogar, onLutando }: {
  colecao: string[]; settings: Settings; onSettings: (s: Settings) => void; onDetails: (id: string) => void; onJogar: () => void; onLutando: (sim: boolean) => void;
}) {
  const [etapa, setEtapa] = useState<Etapa>({ tipo: 'lobby' });
  useEffect(() => { onLutando(etapa.tipo === 'luta'); window.scrollTo(0, 0); }, [etapa.tipo, onLutando]);
  useEffect(() => () => onLutando(false), [onLutando]);
  const [guardado, setGuardado] = useState(carregar);
  const desistir = useRef(false);
  const guardar = (g: Guardado) => { setGuardado(g); save('pvp', g); };

  const comecar = (npc: Npc, meus: Times) => {
    guardar({ ...guardado, times: meus });
    const seed = crypto.getRandomValues(new Uint32Array(1))[0]!;
    setEtapa({ tipo: 'apresentar', npc, partida: { meus, deles: timesDoNpc(npc.nivel as NivelNpc, seed), rodadas: [], seed } });
  };
  const terminouRodada = (npc: Npc, partida: PartidaPvp, meu: number, dele: number, vencedor: 'player' | 'enemy') => {
    const p: PartidaPvp = { ...partida, rodadas: [...partida.rodadas, { meu, dele, seed: sementeDaRodada(partida.seed, partida.rodadas.length), vencedor: vencedor === 'player' ? 'eu' : 'rival' }] };
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

  if (etapa.tipo === 'lobby') return <Lobby colecao={colecao} guardado={guardado} onTreino={(npc) => { som('ui-arena'); setEtapa({ tipo: 'montar', npc }); }} onJogar={onJogar} />;
  if (etapa.tipo === 'montar') return <Montar npc={etapa.npc} colecao={colecao} inicial={guardado.times} onVoltar={() => setEtapa({ tipo: 'lobby' })} onDetails={onDetails} onPronto={(t) => comecar(etapa.npc, t)} />;
  if (etapa.tipo === 'apresentar') return <Apresentar npc={etapa.npc} partida={etapa.partida} onComecar={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  if (etapa.tipo === 'escolher') return <Escolher npc={etapa.npc} partida={etapa.partida} onEscolher={(meu) => {
    const dele = escolhaDoNpc(etapa.npc.nivel as NivelNpc, etapa.partida, etapa.partida.seed + etapa.partida.rodadas.length * 7919);
    setEtapa({ tipo: 'vs', npc: etapa.npc, partida: etapa.partida, meu, dele });
  }} />;
  if (etapa.tipo === 'vs') return <Vs npc={etapa.npc} partida={etapa.partida} meu={etapa.meu} dele={etapa.dele} onLutar={() => setEtapa({ ...etapa, tipo: 'luta' })} />;
  if (etapa.tipo === 'luta') return <ArenaDoPvp meu={etapa.partida.meus[etapa.meu]!} dele={etapa.partida.deles[etapa.dele]!} seed={sementeDaRodada(etapa.partida.seed, etapa.partida.rodadas.length)}
    rodada={etapa.partida.rodadas.length + 1} rival={etapa.npc.nome} settings={settings} onSettings={onSettings} podePausar
    onFim={(v) => terminouRodada(etapa.npc, etapa.partida, etapa.meu, etapa.dele, v)} onDesistir={() => desistirDaPartida(etapa.npc, etapa.partida)} />;
  if (etapa.tipo === 'rodada') return <ResultadoDaRodada npc={etapa.npc} partida={etapa.partida} onSeguir={() => setEtapa({ tipo: 'escolher', npc: etapa.npc, partida: etapa.partida })} />;
  return <Fim npc={etapa.npc} partida={etapa.partida} placar={guardado.treino[etapa.npc.id] ?? { v: 0, d: 0 }} onDeNovo={() => setEtapa({ tipo: 'montar', npc: etapa.npc })} onSair={() => setEtapa({ tipo: 'lobby' })} />;
}

/** A coleção do jogador para o PvP: os personagens liberados nas Conquistas (todos os 400 na conta do dono, para testar). */
export const colecaoDoPvp = (conquistas: Record<string, string> | undefined, dono: boolean) =>
  dono ? characters.map((c) => c.id) : Object.keys(conquistas ?? {}).filter((id) => !!byId[id]);
