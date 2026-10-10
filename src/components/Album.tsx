import {useMemo,useRef,useState,type CSSProperties,type ReactNode} from 'react';
import {ChevronLeft,ChevronRight} from 'lucide-react';
import type {Character} from '../engine/types';
import {ABAS,type Aba} from '../lib/conquistas';

/*
 * O álbum de personagens (pedido do jogador: "ver bastante personagem sem
 * scroll infinito"): quatro abas (Anime, Heróis, Games, Desenhos) e, em cada
 * uma, páginas de 6 × 5 retratos que passam de lado com o dedo, com os
 * pontinhos e as setas embaixo. Usado nas Conquistas e em Personagens; cada
 * tela desenha a sua carta e diz o que a aba mostra embaixo do nome.
 */
const POR_PAGINA=30;
const paginas=<T,>(lista:T[])=>Array.from({length:Math.max(1,Math.ceil(lista.length/POR_PAGINA))},(_,i)=>lista.slice(i*POR_PAGINA,(i+1)*POR_PAGINA));

export function Album({listas,rotulo,barra,carta,vazio,aba:abaControlada,onAba}:{
  listas:Record<Aba,Character[]>;
  /** o texto embaixo do nome da aba ("13/81") */
  rotulo:(aba:Aba)=>ReactNode;
  /** a barrinha da aba, de 0 a 1 (opcional) */
  barra?:(aba:Aba)=>number;
  carta:(c:Character,i:number)=>ReactNode;
  vazio?:ReactNode;
  aba?:Aba;onAba?:(a:Aba)=>void;
}){
  const [abaLocal,setAbaLocal]=useState<Aba>('anime'),aba=abaControlada??abaLocal;
  const [pagina,setPagina]=useState(0);
  const trilho=useRef<HTMLDivElement>(null);
  const lista=listas[aba],folhas=useMemo(()=>paginas(lista),[lista]);
  const irPara=(p:number)=>{const t=trilho.current;if(!t)return;const alvo=Math.max(0,Math.min(folhas.length-1,p));t.scrollTo({left:alvo*t.clientWidth,behavior:'smooth'});setPagina(alvo);};
  const trocarAba=(a:Aba)=>{setAbaLocal(a);onAba?.(a);setPagina(0);trilho.current?.scrollTo({left:0});};
  return <>
    <div className="cq-abas" role="tablist">{ABAS.map(a=>{const b=barra?.(a.id);return <button key={a.id} role="tab" aria-selected={aba===a.id} className={aba===a.id?'ativo':''} style={{'--aba':a.cor} as CSSProperties} onClick={()=>trocarAba(a.id)}>
      <b>{a.nome}</b><small>{rotulo(a.id)}</small>{b!==undefined&&<i style={{width:`${b*100}%`}}/>}</button>;})}</div>
    <div className="cq-album" style={{'--aba':ABAS.find(a=>a.id===aba)!.cor} as CSSProperties}>
      {lista.length?<div className="cq-trilho" ref={trilho} onScroll={e=>{const t=e.currentTarget;const p=Math.round(t.scrollLeft/Math.max(1,t.clientWidth));if(p!==pagina)setPagina(p);}}>
        {folhas.map((folha,fi)=><div key={`${aba}-${fi}`} className="cq-pagina">{folha.map((c,i)=>carta(c,i))}</div>)}
      </div>:<div className="cq-album-vazio">{vazio}</div>}
      {folhas.length>1&&<div className="cq-paginas">
        <button aria-label="Página anterior" disabled={pagina===0} onClick={()=>irPara(pagina-1)}><ChevronLeft size={18}/></button>
        <span>{folhas.map((_,i)=><i key={i} className={i===pagina?'ativo':''} onClick={()=>irPara(i)}/>)}</span>
        <button aria-label="Próxima página" disabled={pagina>=folhas.length-1} onClick={()=>irPara(pagina+1)}><ChevronRight size={18}/></button>
      </div>}
    </div>
  </>;
}
