import {useEffect,useState} from 'react';
import {LogIn,Trophy,WifiOff} from 'lucide-react';
import {byId} from '../data/characters';
import {Portrait} from '../components/Portrait';
import {onlineCall,onlineConfigured,type Leaderboard,type MeusTop3,type PartidaDoHistorico,type PublicRun} from '../lib/online';
import {pontos,situacaoDasVagas} from '../lib/top3';

const modes=[['daily','HOJE'],['weekly','SEMANA'],['season','TEMPORADA'],['mine','MEUS RECORDES']] as const;
/*
 * `conta` é decidido fora, por quem já sabe se há sessão.
 *
 * O servidor só entrega o ranking para quem tem conta. Sem isto, o visitante
 * sem conta pedia o ranking, levava a recusa, e via um ícone de "sem internet"
 * com "Entre na sua conta para *jogar*" — parecia queda de conexão, falava de
 * jogar quando ele só queria olhar, e não oferecia como entrar.
 */
export function RankingScreen({handle,conta,onConta}:{handle?:string;conta:boolean;onConta:()=>void}){
  const [mode,setMode]=useState<(typeof modes)[number][0]>('daily'),[board,setBoard]=useState<Leaderboard|null>(null),[historico,setHistorico]=useState<PartidaDoHistorico[]|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState(''),[selected,setSelected]=useState<PublicRun|null>(null);
  useEffect(()=>{if(!onlineConfigured||!conta)return;let active=true;setLoading(true);setError('');setHistorico(null);
    /*
     * "Meus recordes" é o histórico completo, que só a função da FASE K
     * entrega. Com a função anterior, a ação não existe ("Ação desconhecida")
     * e a aba volta a mostrar o que mostrava: o melhor resultado da temporada.
     */
    const pedido=mode==='mine'
      ?onlineCall<{runs:PartidaDoHistorico[]}>('historico').then(r=>{if(active){setHistorico(r.runs);setBoard(null);}}).catch(e=>{if(e instanceof Error&&/desconhecida/i.test(e.message))return onlineCall<Leaderboard>('leaderboard',{mode:'season'}).then(b=>{if(active)setBoard(b);});throw e;})
      :onlineCall<Leaderboard>('leaderboard',{mode}).then(b=>{if(active)setBoard(b);});
    void pedido.then(()=>{if(active)setLoading(false);}).catch(e=>{if(active){setError(e instanceof Error?e.message:'Ranking indisponível.');setLoading(false);}});
    return()=>{active=false};},[mode,conta]);
  const rows=mode==='mine'?(board?.mine?[board.mine]:[]):board?.entries??[];
  /* A mesma conta pode aparecer até 3 vezes no ranking: todas as suas linhas ficam marcadas. */
  const minhas=new Set([...(board?.meus?.entries??[]).map(m=>m.id),...(board?.mine?[board.mine.id]:[])]);
  return <section className="ranking-screen"><div className="screen-title"><span className="eyebrow"><Trophy size={14}/> RESULTADOS VERIFICADOS</span><h1>Ranking Nexus.</h1><p>Jornadas Ranqueadas têm desafio compartilhado. O servidor reproduz cada luta antes de publicar a pontuação.</p></div>
    <div className="ranking-tabs">{modes.map(([value,label])=><button key={value} className={mode===value?'active':''} onClick={()=>{setMode(value);setSelected(null);}}>{label}</button>)}</div>
    {!onlineConfigured?<p className="ranking-notice"><WifiOff size={18}/> Ranking ainda não foi conectado ao servidor. Jornada Casual e Progresso continuam offline.</p>:!conta?<div className="ranking-convite"><p>O ranking é de quem joga a Jornada Ranqueada. <b>Entre ou crie sua conta</b> para ver as posições e colocar seu trio na disputa.</p><button className="primary" onClick={onConta}><LogIn size={17}/> Entrar ou criar conta</button></div>:error?<p role="alert" className="ranking-notice"><WifiOff size={18}/>{error}</p>:loading?<p className="ranking-notice">Carregando resultados verificados…</p>:historico?<Historico partidas={historico}/>:<>
      {mode!=='mine'&&board?.meus&&<MeusTres meus={board.meus} onSelect={setSelected}/>}
      <p className="ranking-context">{mode==='daily'?'Desafio de hoje':mode==='weekly'?'Desafio da semana':mode==='season'?'Melhores resultados desta temporada':'Seu melhor resultado da temporada'} · {board?.period} {handle&&`· ${handle}`}</p><div className="ranking-list">{rows.map(row=><button key={row.id} onClick={()=>setSelected(row)} className={minhas.has(row.id)?'mine':''}><strong>#{row.position}</strong><span className="ranking-name">{row.handle}</span><div className="ranking-trio">{row.team.map(id=>byId[id]&&<Portrait key={id} character={byId[id]}/>)}</div><span>{row.progress}/10 · {row.highlights.survivors??0} de pé</span><b>{row.score.toLocaleString('pt-BR')}</b></button>)}{!rows.length&&<p className="ranking-empty">Ainda não há resultado validado nesta aba.</p>}</div></>}
    {selected&&<div className="ranking-detail"><button onClick={()=>setSelected(null)} aria-label="Fechar detalhes">×</button><h2>#{selected.position} · {selected.handle}</h2><div className="ranking-detail-trio">{selected.team.map(id=>byId[id]&&<div key={id}><Portrait character={byId[id]}/><span>{byId[id].name}</span></div>)}</div><p><strong>{selected.score.toLocaleString('pt-BR')}</strong> pontos · {selected.progress}/10 confrontos · {selected.highlights.survivors??0} lutadores de pé</p><small>Desafio {selected.seed} · {new Date(selected.date).toLocaleDateString('pt-BR')} · {selected.engineVersion} · {selected.balanceVersion}</small><p>{selected.highlights.survivors??0} sobreviventes no último duelo · {selected.highlights.turns??0} viradas</p></div>}
  </section>;
}

/*
 * "MEUS 3 MELHORES TRIOS", do jeito que o documento desenha: os três, com
 * retratos e pontuação, e embaixo o que falta — "1 vaga livre." ou "Próxima
 * entrada precisa superar 1.400."
 */
function MeusTres({meus,onSelect}:{meus:MeusTop3;onSelect:(r:PublicRun)=>void}){
  return <div className="meus-tres"><span className="eyebrow">MEUS 3 MELHORES TRIOS</span>
    {meus.entries.length?<ol>{meus.entries.map(e=><li key={e.id}><button onClick={()=>onSelect(e)}><div className="ranking-trio">{e.team.map(id=>byId[id]&&<Portrait key={id} character={byId[id]}/>)}</div><span>#{e.position}</span><b>{pontos(e.score)}</b></button></li>)}</ol>
      :<p>Você ainda não tem trio neste ranking.</p>}
    <small>{situacaoDasVagas(meus.vagas,meus.precisaSuperar)}</small></div>;
}

/* "MEUS RECORDES: histórico completo." Toda partida validada, da mais recente. */
function Historico({partidas}:{partidas:PartidaDoHistorico[]}){
  if(!partidas.length)return <p className="ranking-empty">Você ainda não tem Jornada Ranqueada validada.</p>;
  return <><p className="ranking-context">Todas as suas jornadas validadas · {partidas.length}</p><div className="ranking-list historico">{partidas.map(p=><div key={p.id} className="historico-linha"><span className="historico-quando">{new Date(p.date).toLocaleDateString('pt-BR')} · {p.mode==='daily'?'Diário':'Semanal'}</span><div className="ranking-trio">{p.team.map(id=>byId[id]&&<Portrait key={id} character={byId[id]}/>)}</div><span>{p.progress}/10</span><b>{pontos(p.score)}</b></div>)}</div></>;
}
