import {useEffect,useMemo,useRef,useState,type CSSProperties} from 'react';
import {Award,ChevronLeft,ChevronRight,Lock,Sparkles,Trophy,X} from 'lucide-react';
import {byId} from '../data/characters';
import type {Character} from '../engine/types';
import {Portrait} from '../components/Portrait';
import {TelaTopo} from '../components/Casca';
import {ABAS,PERSONAGENS_DA_ABA,TOTAL_DE_CONQUISTAS,juntar,sugestao,tituloDe,type Aba} from '../lib/conquistas';
import {onlineCall,onlineConfigured,type RankingDeConquistas} from '../lib/online';
import type {Profile} from '../lib/storage';

/*
 * As Conquistas (pedido do jogador): todos os personagens, um por conquista.
 *
 * Sem lista infinita: quatro abas (Anime, Heróis, Games, Desenhos) e, em cada
 * uma, páginas de retratos (6 × 5) que passam de lado com o dedo, com os
 * pontinhos embaixo. O bloqueado fica cinza com cadeado; o liberado fica
 * colorido, com o anel dourado e o brilho passando, e o recém-liberado ganha
 * o selo NOVO até a tela ser vista.
 *
 * No topo, o anel com quantos já foram liberados, o título do colecionador e
 * quanto falta para o próximo; com conta, a posição no ranking de conquistas.
 * Embaixo, três sugestões do dia de quem ainda falta.
 */
const POR_PAGINA=30;
const paginas=<T,>(lista:T[])=>Array.from({length:Math.max(1,Math.ceil(lista.length/POR_PAGINA))},(_,i)=>lista.slice(i*POR_PAGINA,(i+1)*POR_PAGINA));
const data=(iso:string)=>new Date(iso).toLocaleDateString('pt-BR');

export function ConquistasScreen({profile,conta,onProfile,onRanking}:{profile:Profile;conta:boolean;onProfile:(p:Profile)=>void;onRanking:()=>void}){
  const conquistas=profile.conquistas??{};
  const [noRanking,setNoRanking]=useState<{total:number;posicao:number|null}|null>(null);
  /* As do servidor entram no aparelho; e a posição no ranking de conquistas. */
  useEffect(()=>{if(!onlineConfigured||!conta)return;let ativo=true;
    void onlineCall<{conquistas:{id:string;data:string}[]}>('conquistas').then(r=>{if(!ativo)return;const juntas=juntar(profile.conquistas??{},r.conquistas);if(Object.keys(juntas).length!==Object.keys(profile.conquistas??{}).length||Object.entries(juntas).some(([k,v])=>profile.conquistas?.[k]!==v))onProfile({...profile,conquistas:juntas});setNoRanking(n=>({total:r.conquistas.length,posicao:n?.posicao??null}));}).catch(()=>{});
    void onlineCall<RankingDeConquistas>('leaderboard',{mode:'conquistas'}).then(r=>{if(ativo&&r.mine)setNoRanking(n=>({total:r.mine!.total,posicao:r.mine!.position??n?.posicao??null}));}).catch(()=>{});
    return()=>{ativo=false};
  },[conta]);
  /* O que estava NOVO fica visto depois de a tela ficar aberta um pouco (o selo aparece na primeira vez). */
  const [vistasAoAbrir]=useState(()=>new Set(profile.conquistasVistas??[]));
  useEffect(()=>{const id=window.setTimeout(()=>{const todas=Object.keys(profile.conquistas??{});if(todas.some(k=>!vistasAoAbrir.has(k)))onProfile({...profile,conquistasVistas:todas});},1500);return()=>window.clearTimeout(id);
  },[profile.conquistas]);

  const liberadas=Object.keys(conquistas).length,titulo=tituloDe(liberadas);
  const [aba,setAba]=useState<Aba>('anime'),[pagina,setPagina]=useState(0),[aberto,setAberto]=useState<Character|null>(null);
  const trilho=useRef<HTMLDivElement>(null);
  const lista=PERSONAGENS_DA_ABA[aba],folhas=useMemo(()=>paginas(lista),[lista]);
  const irPara=(p:number)=>{const t=trilho.current;if(!t)return;const alvo=Math.max(0,Math.min(folhas.length-1,p));t.scrollTo({left:alvo*t.clientWidth,behavior:'smooth'});setPagina(alvo);};
  const trocarAba=(a:Aba)=>{setAba(a);setPagina(0);trilho.current?.scrollTo({left:0});};
  const doDia=useMemo(()=>sugestao(conquistas),[conquistas]);
  const R=44,C=2*Math.PI*R,fracao=liberadas/TOTAL_DE_CONQUISTAS;

  return <section className="conquistas-tela">
    <TelaTopo icone={<Award/>} cor="#ffd36b" rotulo="CONQUISTAS" titulo={`Libere os ${TOTAL_DE_CONQUISTAS}`}><p>Termine as 10 lutas com um personagem no trio para liberar a conquista dele.</p></TelaTopo>

    <div className="cq-heroi" style={{'--titulo':titulo.atual.cor} as CSSProperties}>
      <div className="cq-anel" aria-label={`${liberadas} de ${TOTAL_DE_CONQUISTAS} liberados`}>
        <svg viewBox="0 0 100 100"><circle className="cq-anel-fundo" cx="50" cy="50" r={R}/><circle className="cq-anel-cheio" cx="50" cy="50" r={R} style={{strokeDasharray:`${C*fracao} ${C}`}}/></svg>
        <span><b>{liberadas}</b><small>de {TOTAL_DE_CONQUISTAS}</small><em>{Math.floor(fracao*100)}%</em></span>
      </div>
      <div className="cq-titulo">
        <span className="cq-nivel">NÍVEL {titulo.nivel}</span>
        <strong>{titulo.atual.nome}</strong>
        {titulo.proximo?<><div className="cq-barra"><i style={{width:`${Math.round(titulo.progresso*100)}%`}}/></div>
          <small>Faltam <b>{titulo.proximo.minimo-liberadas}</b> para <b style={{color:titulo.proximo.cor}}>{titulo.proximo.nome}</b></small></>
          :<small>Você liberou todos os personagens!</small>}
        {conta&&onlineConfigured&&<button className="cq-no-ranking" onClick={onRanking}><Trophy size={14}/>{noRanking?.posicao?<><b>#{noRanking.posicao}</b> no ranking · {noRanking.total} valendo</>:<>Ranking de conquistas</>}<ChevronRight size={14}/></button>}
      </div>
    </div>

    <div className="cq-abas" role="tablist">{ABAS.map(a=>{const da=PERSONAGENS_DA_ABA[a.id],tem=da.filter(c=>conquistas[c.id]).length;return <button key={a.id} role="tab" aria-selected={aba===a.id} className={aba===a.id?'ativo':''} style={{'--aba':a.cor} as CSSProperties} onClick={()=>trocarAba(a.id)}>
      <b>{a.nome}</b><small>{tem}/{da.length}</small><i style={{width:`${(tem/da.length)*100}%`}}/></button>;})}</div>

    <div className="cq-album" style={{'--aba':ABAS.find(a=>a.id===aba)!.cor} as CSSProperties}>
      <div className="cq-trilho" ref={trilho} onScroll={e=>{const t=e.currentTarget;const p=Math.round(t.scrollLeft/Math.max(1,t.clientWidth));if(p!==pagina)setPagina(p);}}>
        {folhas.map((folha,fi)=><div key={`${aba}-${fi}`} className="cq-pagina">{folha.map((c,i)=>{const quando=conquistas[c.id],novo=!!quando&&!vistasAoAbrir.has(c.id);
          return <button key={c.id} className={`cq-carta ${quando?'liberada':'bloqueada'} ${novo?'novo':''}`} style={{'--character':c.color,'--i':i} as CSSProperties} onClick={()=>setAberto(c)} aria-label={`${c.name}: ${quando?`liberado em ${data(quando)}`:'bloqueado'}`}>
            <span className="cq-retrato"><Portrait character={c}/>{!quando&&<Lock className="cq-cadeado" size={14}/>}</span>
            <small>{c.name}</small>
            {novo&&<em className="cq-novo">NOVO</em>}
          </button>;})}</div>)}
      </div>
      {folhas.length>1&&<div className="cq-paginas">
        <button aria-label="Página anterior" disabled={pagina===0} onClick={()=>irPara(pagina-1)}><ChevronLeft size={18}/></button>
        <span>{folhas.map((_,i)=><i key={i} className={i===pagina?'ativo':''} onClick={()=>irPara(i)}/>)}</span>
        <button aria-label="Próxima página" disabled={pagina>=folhas.length-1} onClick={()=>irPara(pagina+1)}><ChevronRight size={18}/></button>
      </div>}
    </div>

    {doDia.length>0&&<div className="cq-sugestao">
      <span className="cq-sugestao-rotulo"><Sparkles size={14}/>DESAFIO DO DIA</span>
      <div>{doDia.map(c=><button key={c.id} onClick={()=>setAberto(c)} style={{'--character':c.color} as CSSProperties}><Portrait character={c}/><small>{c.name}</small></button>)}</div>
      <p>Monte um trio com eles e termine as 10 lutas: são <b>3 conquistas</b> de uma vez.</p>
    </div>}

    {aberto&&<div className="cq-veu" role="dialog" aria-label={aberto.name} onClick={e=>{if(e.target===e.currentTarget)setAberto(null);}}>
      <div className={`cq-ficha ${conquistas[aberto.id]?'liberada':'bloqueada'}`} style={{'--character':aberto.color} as CSSProperties}>
        <button className="cq-fechar" onClick={()=>setAberto(null)} aria-label="Fechar"><X size={18}/></button>
        <span className="cq-ficha-retrato"><Portrait character={aberto}/>{!conquistas[aberto.id]&&<Lock size={26}/>}</span>
        <small className="cq-ficha-universo">{aberto.universe}</small>
        <h2>{aberto.name}</h2>
        {conquistas[aberto.id]
          ?<p className="cq-ficha-ok"><Award size={16}/>Conquista liberada em <b>{data(conquistas[aberto.id]!)}</b></p>
          :<p className="cq-ficha-falta">Termine as <b>10 lutas</b> de uma Jornada com {aberto.name} no trio para liberar.</p>}
      </div>
    </div>}
  </section>;
}

/* Os personagens que esta jornada liberou: a tela de resultado mostra. */
export function ConquistasLiberadas({ids}:{ids:string[]}){
  const lista=ids.map(id=>byId[id]).filter((c):c is Character=>!!c);
  if(!lista.length)return null;
  return <div className="cq-liberadas" role="status">
    <span className="cq-liberadas-rotulo"><Award size={15}/>{lista.length===1?'CONQUISTA LIBERADA':`${lista.length} CONQUISTAS LIBERADAS`}</span>
    <div>{lista.map((c,i)=><span key={c.id} className="cq-liberada" style={{'--character':c.color,'--i':i} as CSSProperties}><Portrait character={c}/><small>{c.name}</small></span>)}</div>
  </div>;
}

