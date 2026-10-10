import { useLayoutEffect,useRef,useState,type CSSProperties } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { combatLinks,type CombatLink,type LinkKind } from '../presentation/combat-links';
import { PRESENTATION as P } from '../presentation/config';
import { folha,profileFor } from '../presentation/vfxProfiles';
import { fallbackPoint,type Anchors } from './BattleEffects';

/*
 * As linhas de quem age até o alvo — uma coisa de cada vez.
 *
 * Antes do golpe: só a linha de quem está agindo, fina, curva, na cor do
 * efeito. Ela se desenha de um medalhão até o outro, duas luzes correm por
 * ela ("este vai atacar aquele") e ela some antes do golpe sair.
 *
 * Depois do golpe: se a mesma ação também ajuda alguém (Carga, buff, cura
 * para um aliado), aparece uma linha por vez desse ajudante até o aliado, uma
 * luz corre uma vez e o aliado brilha.
 *
 * Nada de legenda nem de várias linhas ao mesmo tempo: o movimento, a cor e o
 * efeito já dizem quem fez o quê (o histórico guarda o texto).
 */

const OFENSIVO:LinkKind[]=['attack','debuff','interrupt'];
const COR_DE_APOIO:Record<LinkKind,string>={attack:'#ffd9a8',debuff:'#c48cff',interrupt:'#ffb36b',heal:'#6dffa6',shield:'#8fe6ff',buff:'#ffd36b',support:'#ffe7a0'};

interface Linha {id:string;d:string;comprimento:number;cor:string;alvo:{x:number;y:number};fonte:{x:number;y:number}}

export function CombatConnections({battle,beat,anchors,reduced,medal=80}:{battle:Battle;beat:Beat|null;anchors:Anchors;reduced:boolean;medal?:number}){
  const root=useRef<HTMLDivElement>(null),[size,setSize]=useState({w:0,h:0});
  useLayoutEffect(()=>{const el=root.current;if(!el)return;const o=new ResizeObserver(([e])=>setSize({w:e.contentRect.width,h:e.contentRect.height}));o.observe(el);return ()=>o.disconnect();},[]);
  const links=beat?combatLinks(beat,battle):[];
  const ator=beat?.event.source;
  const lado=(uid:string)=>battle.fighters.find(f=>f.uid===uid)?.side;
  /* A ação principal: se ela acerta algum rival, a linha vai para os rivais; senão, para os aliados que ela ajuda. */
  const ofensiva=links.some(l=>l.source===ator&&lado(l.target)!==lado(l.source)&&OFENSIVO.includes(l.kind))||(!links.length&&!!beat?.event.target&&lado(beat.event.target)!==lado(ator??''));
  // o ricochete não é um segundo golpe saindo de quem age: ele quica do primeiro alvo para o segundo depois,
  // então quem só levou o quique não ganha linha de quem age
  const soDoQuique=new Set(links.filter(l=>l.event?.label==='Ricochete').map(l=>l.target).filter(t=>!links.some(l=>l.target===t&&l.kind==='attack'&&l.event?.label!=='Ricochete')));
  const principais=links.filter(l=>l.source===ator&&!soDoQuique.has(l.target)&&(lado(l.target)!==lado(l.source))===ofensiva)
    .filter((l,i,todas)=>todas.findIndex(x=>x.target===l.target)===i);
  const pares=new Set(principais.map(l=>`${l.source}>${l.target}`));
  /* Depois do golpe: só apoio de verdade entre aliados, um de cada vez (no máximo dois). */
  const depois=ofensiva?links.filter(l=>lado(l.source)===lado(l.target)&&!OFENSIVO.includes(l.kind)&&!pares.has(`${l.source}>${l.target}`))
    .filter((l,i,todas)=>todas.findIndex(x=>x.source===l.source&&x.target===l.target)===i).slice(0,2):[];
  const fighter=battle.fighters.find(f=>f.uid===ator);
  const perfil=profileFor(fighter?.characterId??'',beat?.event.skill),corDoEfeito=perfil?.color;

  const px=(uid:string)=>{const a=anchors[uid]??fallbackPoint(uid);return {x:a.x*size.w/100,y:a.y*size.h/100};};
  const raio=medal*.5;
  const linha=(l:CombatLink,cor:string):Linha=>{
    const a=px(l.source),b=px(l.target),dx=b.x-a.x,dy=b.y-a.y,dist=Math.hypot(dx,dy)||1,ux=dx/dist,uy=dy/dist;
    // sai da borda de um medalhão e chega na borda do outro
    const s={x:a.x+ux*raio*1.02,y:a.y+uy*raio*1.02},e={x:b.x-ux*raio*1.08,y:b.y-uy*raio*1.08};
    // curva suave, puxada para o centro da arena
    const mx=(s.x+e.x)/2,my=(s.y+e.y)/2,cx=size.w/2,cy=size.h/2;
    let nx=-uy,ny=ux;if((cx-mx)*nx+(cy-my)*ny<0){nx=-nx;ny=-ny;}
    const curva=Math.min(70,dist*.16),c={x:mx+nx*curva,y:my+ny*curva};
    return {id:l.id,d:`M ${s.x.toFixed(1)} ${s.y.toFixed(1)} Q ${c.x.toFixed(1)} ${c.y.toFixed(1)} ${e.x.toFixed(1)} ${e.y.toFixed(1)}`,comprimento:dist,cor,alvo:e,fonte:s};
  };
  if(!beat||!size.w||beat.periodic||beat.event.kind==='turn')return <div ref={root} className="combat-connections" aria-hidden="true"/>;
  const preparo=beat.event.kind==='cast';
  const W=Math.max(.3,beat.duration*(preparo?1:P.impactAt));
  // o golpe que já voa até o alvo (o Kienzan, o Kamehameha, um tiro) mostra sozinho quem acerta quem:
  // a linha por cima dele parecia um laser (pedido do jogador); no Preparo ela continua
  const voaSozinho=!preparo&&!!perfil?.travel;
  const antes=voaSozinho?[]:!beat.impacted||preparo?principais.map(l=>linha(l,ofensiva?(corDoEfeito??'#ffd9a8'):(corDoEfeito??COR_DE_APOIO[l.kind]))):[];
  /* as linhas de apoio entram na etapa do efeito no próprio trio */
  const apos=beat.impacted&&!preparo&&(beat.etapa??99)>=Math.max(1,(beat.passos?.findIndex(x=>x.classe==='aliado')??-1)+1)?depois.map(l=>linha(l,COR_DE_APOIO[l.kind])):[];
  const img=(nome:string)=>`url(${folha(nome)})`;
  const cometa=(l:Linha,classe:string,extra:Record<string,string>={})=><span key={`c-${l.id}`} className={`link-cometa ${classe}`} style={{'--cor':l.cor,'--fx-img':img('cometa'),offsetPath:`path('${l.d}')`,width:Math.round(medal*.95),height:Math.round(medal*.95),...extra} as CSSProperties}/>;
  return <div ref={root} className={`combat-connections ${reduced?'still':''}`} aria-hidden="true" style={{'--janela':`${W}s`} as CSSProperties}><div className="link-beat" key={beat.event.id}>
    <svg className="combat-paths" viewBox={`0 0 ${size.w} ${size.h}`} preserveAspectRatio="none">
      <defs>
        <filter id="brilho-da-linha" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4"/></filter>
      </defs>
      {antes.map(l=><g key={l.id} className="link-antes" style={{'--cor':l.cor} as CSSProperties}>
        <path d={l.d} pathLength={100} className="link-halo" filter="url(#brilho-da-linha)"/>
        <path d={l.d} pathLength={100} className="link-fio"/>
      </g>)}
      {apos.map((l,i)=><g key={l.id} className="link-depois" style={{'--cor':l.cor,'--atraso':`${.12+i*.42}s`} as CSSProperties}>
        <path d={l.d} pathLength={100} className="link-halo" filter="url(#brilho-da-linha)"/>
        <path d={l.d} pathLength={100} className="link-fio"/>
      </g>)}
    </svg>
    {/* a mira fecha no alvo enquanto quem age se prepara */}
    {antes.map(l=><span key={`m-${l.id}`} className="link-mira" style={{'--cor':l.cor,'--fx-img':img('mira'),left:l.alvo.x+(l.alvo.x-l.fonte.x)/Math.hypot(l.alvo.x-l.fonte.x,l.alvo.y-l.fonte.y)*raio*1.08,top:l.alvo.y+(l.alvo.y-l.fonte.y)/Math.hypot(l.alvo.x-l.fonte.x,l.alvo.y-l.fonte.y)*raio*1.08,width:Math.round(medal*1.45),height:Math.round(medal*1.45)} as CSSProperties}/>)}
    {!reduced&&antes.map(l=>cometa(l,'cometa-antes'))}
    {!reduced&&apos.map((l,i)=>cometa(l,'cometa-depois',{'--atraso':`${.12+i*.42}s`}))}
    {apos.map((l,i)=><span key={`a-${l.id}`} className="link-chegada" style={{'--cor':l.cor,'--fx-img':img('chegada'),'--atraso':`${.12+i*.42+(reduced?0:.34)}s`,left:l.alvo.x+(l.alvo.x-l.fonte.x)/Math.hypot(l.alvo.x-l.fonte.x,l.alvo.y-l.fonte.y)*raio*1.08,top:l.alvo.y+(l.alvo.y-l.fonte.y)/Math.hypot(l.alvo.x-l.fonte.x,l.alvo.y-l.fonte.y)*raio*1.08,width:Math.round(medal*1.6),height:Math.round(medal*1.6)} as CSSProperties}/>)}
  </div></div>;
}
