import {useEffect,useState,type CSSProperties} from 'react';
import {Crown,LogIn,Lock,Medal,Trophy,WifiOff,X} from 'lucide-react';
import {byId} from '../data/characters';
import {Portrait} from '../components/Portrait';
import {TelaTopo} from '../components/Casca';
import {onlineCall,onlineConfigured,type Leaderboard,type MeusTop3,type PartidaDoHistorico,type PublicRun} from '../lib/online';
import {pontos,situacaoDasVagas} from '../lib/top3';

const modes=[['daily','HOJE'],['weekly','SEMANA'],['season','TEMPORADA'],['mine','MEUS']] as const;
type Modo=(typeof modes)[number][0];

/*
 * O ranking (remake): um placar de jogo.
 *
 * Os três primeiros sobem num pódio — ouro no meio, mais alto, prata e bronze
 * dos lados — com o trio em medalhões e os pontos em dourado. Do quarto em
 * diante, uma fila de linhas com a posição num selo. As linhas da própria
 * conta brilham em verde. Tocar em qualquer um abre o cartão da jornada.
 *
 * `conta` é decidido fora, por quem já sabe se há sessão. O servidor só
 * entrega o ranking para quem tem conta: sem ela, a tela convida a entrar em
 * vez de parecer uma queda de conexão.
 */
export function RankingScreen({handle,conta,onConta,recorde}:{handle?:string;conta:boolean;onConta:()=>void;recorde?:number}){
  const [mode,setMode]=useState<Modo>('daily'),[board,setBoard]=useState<Leaderboard|null>(null),[historico,setHistorico]=useState<PartidaDoHistorico[]|null>(null),[loading,setLoading]=useState(false),[maisCarregando,setMaisCarregando]=useState(false),[error,setError]=useState('');
  useEffect(()=>{if(!onlineConfigured||!conta)return;let active=true;setLoading(true);setError('');setHistorico(null);
    /*
     * "Meus" é o histórico completo, que só a função da FASE K entrega. Com a
     * função anterior, a ação não existe ("Ação desconhecida") e a aba volta a
     * mostrar o que mostrava: o melhor resultado da temporada.
     */
    const pedido=mode==='mine'
      ?onlineCall<{runs:PartidaDoHistorico[]}>('historico').then(r=>{if(active){setHistorico(r.runs);setBoard(null);}}).catch(e=>{if(e instanceof Error&&/desconhecida/i.test(e.message))return onlineCall<Leaderboard>('leaderboard',{mode:'season'}).then(b=>{if(active)setBoard(b);});throw e;})
      :onlineCall<Leaderboard>('leaderboard',{mode}).then(b=>{if(active)setBoard(b);});
    void pedido.then(()=>{if(active)setLoading(false);}).catch(e=>{if(active){setError(e instanceof Error?e.message:'Ranking indisponível.');setLoading(false);}});
    return()=>{active=false};},[mode,conta]);
  /*
   * "Ver mais": a próxima página entra no fim da lista. Linhas repetidas (a
   * própria conta pode vir em duas páginas) são descartadas pelo id.
   */
  const verMais=async()=>{
    if(!board||mode==='mine')return;setMaisCarregando(true);
    try{const prox=await onlineCall<Leaderboard>('leaderboard',{mode,pagina:(board.pagina??0)+1});
      setBoard(atual=>atual&&{...prox,entries:[...atual.entries,...prox.entries.filter(e=>!atual.entries.some(x=>x.id===e.id))]});}
    catch(e){setError(e instanceof Error?e.message:'Ranking indisponível.');}
    finally{setMaisCarregando(false);}
  };
  const estado:EstadoDoPlacar=!onlineConfigured?{tipo:'desligado'}:!conta?{tipo:'sem-conta'}:error?{tipo:'erro',texto:error}:loading?{tipo:'carregando'}:historico?{tipo:'historico',partidas:historico}:{tipo:'placar',board};
  return <Placar mode={mode} onMode={setMode} estado={estado} handle={handle} onConta={onConta} onMais={()=>void verMais()} maisCarregando={maisCarregando} recorde={recorde}/>;
}

export type EstadoDoPlacar={tipo:'desligado'|'sem-conta'|'carregando'}|{tipo:'erro';texto:string}|{tipo:'historico';partidas:PartidaDoHistorico[]}|{tipo:'placar';board:Leaderboard|null};

const Trio=({team,tamanho=''}:{team:string[];tamanho?:string})=><span className={`rk-trio ${tamanho}`}>{team.map(id=>byId[id]&&<span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/></span>)}</span>;

/** O desenho do ranking, sem rede: a tela de verdade e o banco de provas usam o mesmo. */
export function Placar({mode,onMode,estado,handle,onConta,onMais,maisCarregando=false,recorde}:{mode:Modo;onMode:(m:Modo)=>void;estado:EstadoDoPlacar;handle?:string;onConta:()=>void;onMais:()=>void;maisCarregando?:boolean;recorde?:number}){
  const [selected,setSelected]=useState<PublicRun|null>(null);
  const board=estado.tipo==='placar'?estado.board:null;
  const rows=mode==='mine'?(board?.mine?[board.mine]:[]):board?.entries??[];
  /* A mesma conta pode aparecer até 3 vezes no ranking: todas as suas linhas ficam marcadas. */
  const minhas=new Set([...(board?.meus?.entries??[]).map(m=>m.id),...(board?.mine?[board.mine.id]:[])]);
  const podio=mode==='mine'?[]:rows.slice(0,3),resto=mode==='mine'?rows:rows.slice(3);
  return <section className="ranking-screen ranking-v2">
    <TelaTopo icone={<Trophy/>} cor="#ffd36b" rotulo="RANKING" titulo="Quem fez mais pontos"><p>Toda jornada é refeita pelo servidor antes de entrar.</p></TelaTopo>
    {/* o recorde da Jornada normal fica neste aparelho; o placar abaixo é o das ranqueadas (Diária e Semanal) */}
    {recorde!==undefined&&<div className="rk-recorde-local"><Trophy size={16}/><span>Seu recorde na Jornada</span><b>{recorde.toLocaleString('pt-BR')}</b><small>pontos · neste aparelho</small></div>}
    <div className="rk-abas" role="tablist">{modes.map(([value,label])=><button key={value} role="tab" aria-selected={mode===value} className={mode===value?'ativo':''} onClick={()=>{onMode(value);setSelected(null);}}>{label}</button>)}</div>

    {estado.tipo==='desligado'?<div className="rk-bloqueio"><span className="rk-cadeado"><WifiOff size={30}/></span><b>Ranking desligado nesta versão</b><p>A Jornada casual continua funcionando sem internet.</p></div>
    :estado.tipo==='sem-conta'?<div className="rk-bloqueio"><span className="rk-cadeado"><Lock size={30}/></span><b>Entre para ver o placar</b><p>O ranking é de quem joga a Jornada Ranqueada. Com conta, você vê as posições e coloca seu trio na disputa.</p><button className="primary gs-cta" onClick={onConta}><LogIn size={18}/> Entrar ou criar conta</button></div>
    :estado.tipo==='erro'?<p role="alert" className="rk-aviso"><WifiOff size={18}/>{estado.texto}</p>
    :estado.tipo==='carregando'?<div className="rk-carregando" aria-label="Carregando resultados verificados">{[0,1,2,3].map(i=><i key={i} style={{'--i':i} as CSSProperties}/>)}</div>
    :estado.tipo==='historico'?<Historico partidas={estado.partidas}/>
    :<>
      {mode!=='mine'&&board?.meus&&<MeusTres meus={board.meus} onSelect={setSelected}/>}
      <p className="rk-contexto">{mode==='daily'?'Desafio de hoje':mode==='weekly'?'Desafio da semana':mode==='season'?'Melhores da temporada':'Seu melhor resultado da temporada'} · {board?.period}{handle&&<> · <b>{handle}</b></>}</p>
      {podio.length>0&&<div className="rk-podio">{[podio[1],podio[0],podio[2]].map((row,i)=>row&&<button key={row.id} className={`rk-degrau p${row.position} ${minhas.has(row.id)?'mine':''}`} style={{'--i':i} as CSSProperties} onClick={()=>setSelected(row)}>
        <span className="rk-coroa">{row.position===1?<Crown size={22}/>:<Medal size={18}/>}</span>
        <Trio team={row.team}/>
        <b className="rk-nome">{row.handle}</b>
        <strong>{pontos(row.score)}</strong>
        <span className="rk-base">{row.position}</span>
      </button>)}</div>}
      <div className="ranking-list rk-lista">{resto.map((row,i)=><button key={row.id} onClick={()=>setSelected(row)} className={minhas.has(row.id)?'mine':''} style={{'--i':Math.min(i,12)} as CSSProperties}>
        <span className="rk-pos">{row.position}</span>
        <span className="rk-quem"><b>{row.handle}</b><small>{row.progress}/10 · {row.highlights.survivors??0} de pé</small></span>
        <Trio team={row.team} tamanho="mini"/>
        <strong>{pontos(row.score)}</strong>
      </button>)}{!rows.length&&<p className="rk-vazio">Ainda não há resultado validado nesta aba. O primeiro lugar está livre!</p>}</div>
      {mode!=='mine'&&board?.temMais&&<button className="secondary rk-mais" disabled={maisCarregando} onClick={onMais}>{maisCarregando?'Carregando…':`Ver mais · ${rows.length} de ${pontos(board.total??rows.length)}`}</button>}
    </>}

    {selected&&<div className="rk-detalhe" role="dialog" aria-label={`Jornada de ${selected.handle}`} onClick={e=>{if(e.target===e.currentTarget)setSelected(null);}}>
      <div className="rk-cartao">
        <button className="rk-fechar" onClick={()=>setSelected(null)} aria-label="Fechar detalhes"><X size={18}/></button>
        <span className="rk-cartao-pos">#{selected.position}</span>
        <h2>{selected.handle}</h2>
        <div className="rk-cartao-trio">{selected.team.map(id=>byId[id]&&<div key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/><span>{byId[id].name}</span></div>)}</div>
        <strong className="rk-cartao-pontos">{pontos(selected.score)}<small>pontos</small></strong>
        <div className="rk-cartao-numeros"><span><b>{selected.progress}/10</b><small>lutas</small></span><span><b>{selected.highlights.survivors??0}</b><small>de pé no fim</small></span><span><b>{selected.highlights.turns??0}</b><small>viradas</small></span></div>
        <small className="rk-cartao-rodape">Desafio {selected.seed} · {new Date(selected.date).toLocaleDateString('pt-BR')} · {selected.engineVersion}</small>
      </div>
    </div>}
  </section>;
}

/*
 * "MEUS 3 MELHORES TRIOS": os três, com retratos e pontuação, e embaixo o que
 * falta — "1 vaga livre." ou "Próxima entrada precisa superar 1.400."
 */
function MeusTres({meus,onSelect}:{meus:MeusTop3;onSelect:(r:PublicRun)=>void}){
  return <div className="meus-tres rk-meus"><span className="rk-meus-rotulo"><Crown size={14}/>MEUS 3 MELHORES TRIOS</span>
    {meus.entries.length?<ol>{meus.entries.map(e=><li key={e.id}><button onClick={()=>onSelect(e)}><Trio team={e.team} tamanho="mini"/><span>#{e.position}</span><b>{pontos(e.score)}</b></button></li>)}{Array.from({length:Math.max(0,3-meus.entries.length)},(_,i)=><li key={`vaga-${i}`} className="rk-vaga"><span>vaga livre</span></li>)}</ol>
      :<p>Você ainda não tem trio neste ranking.</p>}
    <small>{situacaoDasVagas(meus.vagas,meus.precisaSuperar)}</small></div>;
}

/* "MEUS": o histórico completo. Toda partida validada, da mais recente. */
function Historico({partidas}:{partidas:PartidaDoHistorico[]}){
  if(!partidas.length)return <p className="rk-vazio">Você ainda não tem Jornada Ranqueada validada.</p>;
  return <><p className="rk-contexto">Todas as suas jornadas validadas · {partidas.length}</p><div className="ranking-list rk-lista historico">{partidas.map(p=><div key={p.id} className="historico-linha"><span className="rk-quem"><b>{new Date(p.date).toLocaleDateString('pt-BR')}</b><small>{p.mode==='daily'?'Diário':'Semanal'} · {p.progress}/10</small></span><Trio team={p.team} tamanho="mini"/><strong>{pontos(p.score)}</strong></div>)}</div></>;
}
