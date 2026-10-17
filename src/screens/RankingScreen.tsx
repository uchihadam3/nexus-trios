import {useEffect,useState,type CSSProperties,type ReactNode} from 'react';
import {createPortal} from 'react-dom';
import {Award,CheckCircle2,Crown,Lightbulb,LogIn,Lock,Medal,ShieldCheck,Trophy,WifiOff,X} from 'lucide-react';
import {byId} from '../data/characters';
import {Portrait} from '../components/Portrait';
import {TelaTopo} from '../components/Casca';
import {onlineCall,onlineConfigured,type EntradaDeConquista,type Leaderboard,type PartidaDoHistorico,type PublicRun,type RankingDeConquistas} from '../lib/online';
import {pontos} from '../lib/top3';

const modes=[['daily','HOJE'],['weekly','SEMANA'],['season','GERAL'],['mine','MEUS'],['conquistas','CONQUISTAS']] as const;
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
export function RankingScreen({handle,conta,onConta,recorde,inicial='daily',dono=false}:{handle?:string;conta:boolean;onConta:()=>void;recorde?:number;inicial?:Modo;/** a conta do dono do jogo vê as jornadas sem validar (src/lib/dicas-liberadas.ts) */dono?:boolean}){
  const [mode,setMode]=useState<Modo>(inicial),[cq,setCq]=useState<RankingDeConquistas|null>(null),[board,setBoard]=useState<Leaderboard|null>(null),[historico,setHistorico]=useState<PartidaDoHistorico[]|null>(null),[loading,setLoading]=useState(false),[maisCarregando,setMaisCarregando]=useState(false),[error,setError]=useState(''),[recarga,setRecarga]=useState(0);
  useEffect(()=>{if(!onlineConfigured||!conta)return;let active=true;setLoading(true);setError('');setHistorico(null);
    /*
     * "Meus" é o histórico completo, que só a função da FASE K entrega. Com a
     * função anterior, a ação não existe ("Ação desconhecida") e a aba volta a
     * mostrar o que mostrava: o melhor resultado da temporada.
     */
    const pedido=mode==='conquistas'
      ?onlineCall<RankingDeConquistas>('leaderboard',{mode:'conquistas'}).then(r=>{if(active){setCq(r);setBoard(null);}})
      :mode==='mine'
      ?onlineCall<{runs:PartidaDoHistorico[]}>('historico').then(r=>{if(active){setHistorico(r.runs);setBoard(null);}}).catch(e=>{if(e instanceof Error&&/desconhecida/i.test(e.message))return onlineCall<Leaderboard>('leaderboard',{mode:'season'}).then(b=>{if(active)setBoard(b);});throw e;})
      :onlineCall<Leaderboard>('leaderboard',{mode}).then(b=>{if(active)setBoard(b);});
    void pedido.then(()=>{if(active)setLoading(false);}).catch(e=>{if(active){setError(e instanceof Error?e.message:'Ranking indisponível.');setLoading(false);}});
    return()=>{active=false};},[mode,conta,recarga]);
  /*
   * "Ver mais": a próxima página entra no fim da lista. Linhas repetidas (a
   * própria conta pode vir em duas páginas) são descartadas pelo id.
   */
  const verMais=async()=>{
    if(mode==='conquistas'&&cq){setMaisCarregando(true);
      try{const prox=await onlineCall<RankingDeConquistas>('leaderboard',{mode:'conquistas',pagina:cq.pagina+1});setCq(atual=>atual&&{...prox,mine:atual.mine,entries:[...atual.entries,...prox.entries.filter(e=>!atual.entries.some(x=>x.id===e.id))]});}
      catch(e){setError(e instanceof Error?e.message:'Ranking indisponível.');}
      finally{setMaisCarregando(false);}return;}
    if(!board||mode==='mine')return;setMaisCarregando(true);
    try{const prox=await onlineCall<Leaderboard>('leaderboard',{mode,pagina:(board.pagina??0)+1});
      setBoard(atual=>atual&&{...prox,entries:[...atual.entries,...prox.entries.filter(e=>!atual.entries.some(x=>x.id===e.id))]});}
    catch(e){setError(e instanceof Error?e.message:'Ranking indisponível.');}
    finally{setMaisCarregando(false);}
  };
  const estado:EstadoDoPlacar=!onlineConfigured?{tipo:'desligado'}:!conta?{tipo:'sem-conta'}:error?{tipo:'erro',texto:error}:loading?{tipo:'carregando'}:historico?{tipo:'historico',partidas:historico}:mode==='conquistas'?{tipo:'conquistas',ranking:cq}:{tipo:'placar',board};
  return <Placar mode={mode} onMode={setMode} estado={estado} handle={handle} onConta={onConta} onMais={()=>void verMais()} maisCarregando={maisCarregando} recorde={recorde} extra={dono&&conta&&onlineConfigured?<PainelDoDono onValidou={()=>setRecarga(n=>n+1)}/>:null}/>;
}

export type EstadoDoPlacar={tipo:'desligado'|'sem-conta'|'carregando'}|{tipo:'erro';texto:string}|{tipo:'historico';partidas:PartidaDoHistorico[]}|{tipo:'placar';board:Leaderboard|null}|{tipo:'conquistas';ranking:RankingDeConquistas|null};

const Trio=({team,tamanho=''}:{team:string[];tamanho?:string})=><span className={`rk-trio ${tamanho}`}>{team.map(id=>byId[id]&&<span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/></span>)}</span>;

/** O desenho do ranking, sem rede: a tela de verdade e o banco de provas usam o mesmo. */
export function Placar({mode,onMode,estado,handle,onConta,onMais,maisCarregando=false,recorde,extra}:{mode:Modo;onMode:(m:Modo)=>void;estado:EstadoDoPlacar;handle?:string;onConta:()=>void;onMais:()=>void;maisCarregando?:boolean;recorde?:number;extra?:ReactNode}){
  const [selected,setSelected]=useState<PublicRun|null>(null);
  const board=estado.tipo==='placar'?estado.board:null;
  const rows=mode==='mine'?(board?.mine?[board.mine]:[]):board?.entries??[];
  /* A mesma conta pode aparecer até 3 vezes no ranking: todas as suas linhas ficam marcadas. */
  const minhas=new Set([...(board?.meus?.entries??[]).map(m=>m.id),...(board?.mine?[board.mine.id]:[])]);
  const podio=mode==='mine'?[]:rows.slice(0,3),resto=mode==='mine'?rows:rows.slice(3);
  return <section className="ranking-screen ranking-v2">
    <TelaTopo icone={mode==='conquistas'?<Award/>:<Trophy/>} cor="#ffd36b" rotulo="RANKING" titulo={mode==='conquistas'?'Quem liberou mais':'Quem fez mais pontos'}><p>{mode==='conquistas'?'Cada personagem com as 10 lutas terminadas vale uma conquista.':'Toda jornada é refeita pelo servidor antes de entrar.'}</p></TelaTopo>
    {/* o recorde deste aparelho; com conta, cada Jornada entra em Hoje, Semana e Geral ao mesmo tempo */}
    {recorde!==undefined&&<div className="rk-recorde-local"><Trophy size={16}/><span>Seu recorde na Jornada</span><b>{recorde.toLocaleString('pt-BR')}</b><small>pontos · neste aparelho</small></div>}
    <div className="rk-abas cinco" role="tablist">{modes.map(([value,label])=><button key={value} role="tab" aria-selected={mode===value} className={mode===value?'ativo':''} onClick={()=>{onMode(value);setSelected(null);}}>{label}</button>)}</div>

    {estado.tipo==='desligado'?<div className="rk-bloqueio"><span className="rk-cadeado"><WifiOff size={30}/></span><b>Ranking desligado nesta versão</b><p>A Jornada casual continua funcionando sem internet.</p></div>
    :estado.tipo==='sem-conta'?<div className="rk-bloqueio"><span className="rk-cadeado"><Lock size={30}/></span><b>Entre para ver o placar</b><p>Com conta, toda Jornada vale ranking: entra em Hoje, Semana e Geral ao mesmo tempo. Você vê as posições e coloca seu trio na disputa.</p><button className="primary gs-cta" onClick={onConta}><LogIn size={18}/> Entrar ou criar conta</button></div>
    :estado.tipo==='erro'?<p role="alert" className="rk-aviso"><WifiOff size={18}/>{estado.texto}</p>
    :estado.tipo==='carregando'?<div className="rk-carregando" aria-label="Carregando resultados verificados">{[0,1,2,3].map(i=><i key={i} style={{'--i':i} as CSSProperties}/>)}</div>
    :estado.tipo==='historico'?<Historico partidas={estado.partidas}/>
    :estado.tipo==='conquistas'?<PlacarDeConquistas ranking={estado.ranking} handle={handle} onMais={onMais} maisCarregando={maisCarregando}/>
    :<>
      <p className="rk-contexto">{mode==='daily'?'Melhores de hoje':mode==='weekly'?'Melhores da semana':mode==='season'?'Melhores de todos os tempos':'Seu melhor resultado'} · {board?.period}{handle&&<> · <b>{handle}</b></>}</p>
      {podio.length>0&&<div className="rk-podio">{[podio[1],podio[0],podio[2]].map((row,i)=>row&&<button key={row.id} className={`rk-degrau p${row.position} ${minhas.has(row.id)?'mine':''}`} style={{'--i':i} as CSSProperties} onClick={()=>setSelected(row)}>
        <span className="rk-coroa">{row.position===1?<Crown size={22}/>:<Medal size={18}/>}</span>
        <Trio team={row.team}/>
        <b className="rk-nome">{row.handle}</b>
        {row.highlights.dicas&&<ComDicas/>}
        <strong>{pontos(row.score)}</strong>
        <span className="rk-base">{row.position}</span>
      </button>)}</div>}
      <div className="ranking-list rk-lista">{resto.map((row,i)=><button key={row.id} onClick={()=>setSelected(row)} className={minhas.has(row.id)?'mine':''} style={{'--i':Math.min(i,12)} as CSSProperties}>
        <span className="rk-pos">{row.position}</span>
        <span className="rk-quem"><b>{row.handle}</b><small>{row.progress}/10{row.highlights.semBaixas!==undefined&&<> · {row.highlights.semBaixas} sem baixas</>}</small>{row.highlights.dicas&&<ComDicas/>}</span>
        <Trio team={row.team} tamanho="mini"/>
        <strong>{pontos(row.score)}</strong>
      </button>)}{!rows.length&&<p className="rk-vazio">Ainda não há resultado validado nesta aba. O primeiro lugar está livre!</p>}</div>
      {mode!=='mine'&&board?.temMais&&<button className="secondary rk-mais" disabled={maisCarregando} onClick={onMais}>{maisCarregando?'Carregando…':`Ver mais · ${rows.length} de ${pontos(board.total??rows.length)}`}</button>}
    </>}

    {/* No body (portal): dentro da tela, que anima com transform, o fixed ficava preso no fim da lista e era preciso rolar até ele. */}
    {selected&&createPortal(<div className="rk-detalhe" role="dialog" aria-label={`Jornada de ${selected.handle}`} onClick={e=>{if(e.target===e.currentTarget)setSelected(null);}}>
      <div className="rk-cartao">
        <button className="rk-fechar" onClick={()=>setSelected(null)} aria-label="Fechar detalhes"><X size={18}/></button>
        <span className="rk-cartao-pos">#{selected.position}</span>
        <h2>{selected.handle}</h2>
        {selected.highlights.dicas&&<p className="rk-cartao-dicas"><Lightbulb size={15}/>Montou o trio com as Dicas de trio ligadas · cada luta perdeu pontos</p>}
        <div className="rk-cartao-trio">{selected.team.map(id=>byId[id]&&<div key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/><span>{byId[id].name}</span></div>)}</div>
        <strong className="rk-cartao-pontos">{pontos(selected.score)}<small>pontos</small></strong>
        <div className="rk-cartao-numeros"><span><b>{selected.progress}/10</b><small>lutas</small></span><span><b>{selected.highlights.semBaixas??'—'}</b><small>lutas sem baixas</small></span><span><b>{selected.highlights.turns??0}</b><small>viradas</small></span></div>
        <small className="rk-cartao-rodape">Desafio {selected.seed} · {new Date(selected.date).toLocaleDateString('pt-BR')} · {selected.engineVersion}</small>
      </div>
    </div>,document.body)}
    {extra}
  </section>;
}

/*
 * Jornadas sem validar (pedido do dono do jogo: "você consegue ver quem tá
 * jogando e quem não foi validado e validar essa pessoa"). Só aparece na
 * conta do dono, e o servidor confere de novo (ação `pendentes`). Cada
 * jornada é refeita pelo servidor, uma por vez, e entra com o resultado dele.
 *
 * Quase nunca precisa: o servidor coloca sozinho no ranking toda jornada
 * terminada (perdeu, venceu as 10 ou desistiu) cujo envio não chegou. Quem
 * está jogando agora não aparece na lista, só no contador.
 */
type Pendente={id:string;handle:string;team:string[];date:string;meu:boolean};
function PainelDoDono({onValidou}:{onValidou:()=>void}){
  const [aberto,setAberto]=useState(false),[lista,setLista]=useState<Pendente[]|null>(null),[jogando,setJogando]=useState(0),[dias,setDias]=useState(7),[ocupado,setOcupado]=useState(''),[aviso,setAviso]=useState('');
  const carregar=()=>{setAviso('');void onlineCall<{dias:number;jogando?:number;runs:Pendente[]}>('pendentes').then(r=>{setLista(r.runs);setDias(r.dias);setJogando(r.jogando??0);}).catch(e=>setAviso(e instanceof Error?e.message:'Não deu para carregar.'));};
  useEffect(()=>{if(aberto&&!lista)carregar();},[aberto]);
  const validar=async(ids:string[])=>{
    let feitas=0;
    for(const id of ids){setOcupado(id);
      try{await onlineCall('validar-pendente',{runId:id});feitas++;setLista(l=>l&&l.filter(x=>x.id!==id));}
      catch(e){const msg=e instanceof Error?e.message:'';if(/já/i.test(msg))setLista(l=>l&&l.filter(x=>x.id!==id));else{setAviso(`Parou numa jornada: ${msg||'erro'}`);break;}}}
    setOcupado('');if(feitas){setAviso(`${feitas} jornada${feitas>1?'s':''} validada${feitas>1?'s':''}.`);onValidou();}
  };
  const pessoas=lista?[...new Set(lista.map(x=>x.handle))]:[];
  return <div className="rk-dono">
    <button className="secondary rk-dono-abre" onClick={()=>setAberto(a=>!a)}><ShieldCheck size={16}/>Jornadas sem validar{lista?` · ${lista.length}`:''}</button>
    {aberto&&<div className="rk-dono-corpo">
      <small>Últimos {dias} dias · só a sua conta vê isto. Jornada terminada entra sozinha no ranking em poucos minutos; aqui ficam só as que ficaram paradas.{jogando>0&&` ${jogando} ${jogando===1?'pessoa está':'pessoas estão'} jogando agora.`}</small>
      {aviso&&<p className="rk-dono-aviso">{aviso}</p>}
      {!lista?<p className="rk-dono-aviso">Carregando…</p>:!lista.length?<p className="rk-dono-aviso"><CheckCircle2 size={14}/>Nenhuma jornada esperando.</p>:<>
        <p className="rk-dono-aviso">{pessoas.length} pessoa{pessoas.length>1?'s':''}: {pessoas.join(', ')}</p>
        <button className="primary" disabled={!!ocupado} onClick={()=>void validar(lista.map(x=>x.id))}>{ocupado?'Validando…':`Validar todas (${lista.length})`}</button>
        <ol className="ranking-list rk-lista">{lista.map(x=><li key={x.id}><Trio team={x.team} tamanho="mini"/><span><b>{x.handle}</b><small>{new Date(x.date).toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})}</small></span><button className="secondary" disabled={!!ocupado} onClick={()=>void validar([x.id])}>{ocupado===x.id?'…':'Validar'}</button></li>)}</ol>
      </>}
    </div>}
  </div>;
}

function Historico({partidas}:{partidas:PartidaDoHistorico[]}){
  if(!partidas.length)return <p className="rk-vazio">Você ainda não tem Jornada validada no ranking. Jogue com a conta conectada: no fim, ela entra sozinha.</p>;
  return <><p className="rk-contexto">Todas as suas jornadas validadas · {partidas.length}</p><div className="ranking-list rk-lista historico">{partidas.map(p=><div key={p.id} className="historico-linha"><span className="rk-quem"><b>{new Date(p.date).toLocaleDateString('pt-BR')}</b><small>{p.progress}/10 lutas</small>{p.dicas&&<ComDicas/>}</span><Trio team={p.team} tamanho="mini"/><strong>{pontos(p.score)}</strong></div>)}</div></>;
}

/* Quem montou o trio com as Dicas de trio aparece marcado no ranking (pedido do jogador). */
function ComDicas(){return <span className="rk-dicas" title="Usou as Dicas de trio: cada luta perdeu pontos"><Lightbulb size={11}/>com dicas</span>;}

/*
 * O ranking de conquistas (pedido do jogador): quem liberou mais personagens.
 * Empatou, quem chegou ao número antes. O pódio mostra os três últimos que
 * cada um liberou; a linha da própria conta fica no topo e marcada.
 */
function PlacarDeConquistas({ranking,handle,onMais,maisCarregando}:{ranking:RankingDeConquistas|null;handle?:string;onMais:()=>void;maisCarregando:boolean}){
  if(!ranking)return null;
  const de=ranking.de,podio=ranking.entries.slice(0,3),resto=ranking.entries.slice(3);
  const Linha=({e,i}:{e:EntradaDeConquista;i:number})=><button className={`rk-cq-linha ${e.mine?'mine':''}`} style={{'--i':Math.min(i,12)} as CSSProperties}>
    <span className="rk-pos">{e.position}</span>
    <span className="rk-quem"><b>{e.handle}</b><small>{Math.floor((e.total/de)*100)}% liberado</small><span className="rk-cq-barra"><i style={{width:`${(e.total/de)*100}%`}}/></span></span>
    <span className="rk-cq-total"><b>{e.total}</b><small>de {de}</small></span>
  </button>;
  return <>
    <p className="rk-contexto"><Award size={13}/> Quem liberou mais personagens · termine as 10 lutas com alguém para liberar{handle&&<> · <b>{handle}</b></>}</p>
    {ranking.mine&&<div className="rk-meus"><span className="rk-meus-rotulo"><Award size={14}/>MINHA POSIÇÃO</span><div className="ranking-list rk-lista" style={{marginTop:8}}><Linha e={ranking.mine} i={0}/></div></div>}
    {podio.length>0&&<div className="rk-podio">{[podio[1],podio[0],podio[2]].map((e,i)=>e&&<div key={e.id} className={`rk-degrau p${e.position} ${e.mine?'mine':''}`} style={{'--i':i} as CSSProperties}>
      <span className="rk-coroa">{e.position===1?<Crown size={22}/>:<Medal size={18}/>}</span>
      {e.ultimos.length>0&&<Trio team={e.ultimos}/>}
      <b className="rk-nome">{e.handle}</b>
      <span className="rk-cq-total"><b>{e.total}</b><small>de {de}</small></span>
      <span className="rk-base">{e.position}</span>
    </div>)}</div>}
    <div className="ranking-list rk-lista">{resto.map((e,i)=><Linha key={e.id} e={e} i={i}/>)}{!ranking.entries.length&&<p className="rk-vazio">Ninguém liberou conquistas ainda. Termine as 10 lutas de uma Jornada e seja o primeiro!</p>}</div>
    {ranking.temMais&&<button className="secondary rk-mais" disabled={maisCarregando} onClick={onMais}>{maisCarregando?'Carregando…':`Ver mais · ${ranking.entries.length} de ${pontos(ranking.total)}`}</button>}
  </>;
}
