import { useLayoutEffect,useRef,useState,type CSSProperties,type ReactElement } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { SkillIcon } from './Icon';
import { ArrowDown,HeartPulse,ShieldCheck,Sparkles,Zap } from 'lucide-react';
import { statuses as statusCatalog } from '../data/statuses';
import { familia,folha,profileFor,type VfxFamily,type VfxProfile } from '../presentation/vfxProfiles';

export interface Anchor {x:number;y:number}
export type Anchors=Record<string,Anchor>;
export function fallbackPoint(uid:string):Anchor{const [side,slot]=uid.split('-');return {x:17+Number(slot)*33,y:side==='enemy'?16:76};}
export function isAreaBeat(beat:Beat|null,battle:Battle):boolean {
  if(!beat||!['basic','skill'].includes(beat.event.kind))return false;
  const source=battle.fighters.find(f=>f.uid===beat.event.source);
  if(profileFor(source?.characterId??'',beat.event.skill)?.area)return true;
  const direct=beat.events.filter(e=>e.source===beat.event.source&&e.target&&['damage','status','heal','shield'].includes(e.kind));
  return new Set(direct.map(e=>e.target)).size>1;
}

/* Beats sem ficha de habilidade (interrupção) ganham uma família direta. */
const SEM_FICHA:Partial<Record<Beat['event']['kind'],VfxFamily>>={interrupt:'onda_de_choque'};
/* Cada variante gira um pouco o impacto, para a mesma família não parecer carimbo. */
const GIRO_DA_VARIANTE=[0,16,-12,8];
/* Altura da faixa em relação ao medalhão. */
const ALTURA_DA_FAIXA:Record<string,number>={feixe:.36,feixe_pesado:.62,raio_faixa:.7,dreno:.42};

const s=(x:number)=>`${x.toFixed(3)}s`;

/**
 * Os efeitos das famílias (adendo, parte 3), em até cinco camadas por ação:
 * preparo em quem age, o projétil que voa ou o feixe esticado até o alvo, e o
 * impacto em cada alvo atingido. Cada camada é uma folha neutra tingida com a
 * cor do efeito (máscara) e com o núcleo claro por cima; o navegador só
 * posiciona, gira e troca o quadro — transform, opacity e mask-position.
 */
export function BattleEffects({battle,beat,anchors,enabled,reduced,medal=80}:{battle:Battle;beat:Beat|null;anchors:Anchors;enabled:boolean;reduced:boolean;medal?:number}){
  const root=useRef<HTMLDivElement>(null),[size,setSize]=useState({w:0,h:0});
  useLayoutEffect(()=>{const element=root.current;if(!element)return;const observer=new ResizeObserver(([entry])=>setSize({w:entry.contentRect.width,h:entry.contentRect.height}));observer.observe(element);return ()=>observer.disconnect();},[]);
  const point=(uid:string)=>anchors[uid]??fallbackPoint(uid);
  const px=(a:Anchor)=>({x:a.x*size.w/100,y:a.y*size.h/100});
  const source=beat?battle.fighters.find(f=>f.uid===beat.event.source):null;
  const character=source?byId[source.characterId]:null;
  const kind=beat?.event.kind;
  const perfil:VfxProfile|undefined=beat&&(kind==='basic'||kind==='skill'||kind==='cast')?profileFor(source?.characterId??'',beat.event.skill):undefined;
  const chave:VfxFamily|undefined=perfil?.family??(kind?SEM_FICHA[kind]:undefined);
  const fam=chave?familia(chave):undefined;
  const cor=perfil?.color??character?.color??'#cfe6ff';
  const landed=beat?.impacted??false;
  const area=isAreaBeat(beat,battle);
  const D=beat?.duration??2,I=P.impactAt;
  const p1=beat?point(beat.event.source):{x:50,y:50};
  const alvoPrincipal=beat?.event.target;
  const p2=alvoPrincipal?point(alvoPrincipal):p1;
  const a=px(p1),b=px(p2),dx=b.x-a.x,dy=b.y-a.y,dist=Math.hypot(dx,dy),ang=Math.atan2(dy,dx)*180/Math.PI;
  const intensidade=(perfil?.intensity??1)*(beat?.grand?1.22:1);
  const vai=!!beat&&!reduced&&kind!=='cast'&&!!alvoPrincipal&&alvoPrincipal!==beat.event.source&&!!perfil?.travel&&dist>medal*.6;

  /* Alvos que recebem impacto: quem levou dano, cura, Escudo ou Status deste beat (até três). */
  const alvos=beat?[...new Set(beat.events.filter(e=>e.target&&['damage','status','interrupt','shield','heal','ko','block'].includes(e.kind)).map(e=>e.target!))].slice(0,3):[];
  if(beat&&landed&&!alvos.length&&kind!=='turn'&&kind!=='cast')alvos.push(alvoPrincipal??beat.event.source);

  const camada=(nome:string,estilo:Record<string,string|number>,classe:string,key:string)=><span key={key} className={`fxl ${classe}`} style={{'--fx-img':`url(${folha(nome)})`,...estilo} as CSSProperties}/>;
  const nodes:ReactElement[]=[];
  if(enabled&&beat&&fam&&kind!=='turn'&&size.w>0){
    const id=beat.event.id;
    // preparo: a folha da família em laço sobre quem prepara
    if(kind==='cast'&&!landed&&fam.preparo){
      const t=medal*1.9*intensidade;
      nodes.push(camada(fam.preparo,{left:`${p1.x}%`,top:`${p1.y}%`,width:t,height:t},'fxl-laco',`prep-${id}`));
    }
    // viagem: o projétil sai depois da preparação do golpe e chega no impacto
    if(vai&&!landed&&fam.viagem){
      const t=medal*(fam.viagem==='saraivada'?1.25:1.05)*Math.min(1.25,intensidade);
      nodes.push(camada(fam.viagem,{left:`${p1.x}%`,top:`${p1.y}%`,width:t,height:t,'--dx':`${dx}px`,'--dy':`${dy}px`,'--ang':`${ang}deg`,'--voo':s(D*I*.42),'--voo-delay':s(D*I*.58)},'fxl-laco fxl-voo',`voo-${id}`));
    }
    // faixa: o feixe cresce de quem age até o alvo, segura o impacto e some
    if(vai&&fam.faixa){
      const h=medal*(ALTURA_DA_FAIXA[fam.faixa]??.4)*Math.min(1.3,intensidade);
      nodes.push(camada(fam.faixa,{left:`${p1.x}%`,top:`${p1.y}%`,width:dist,height:h,'--ang':`${ang}deg`,'--faixa':s(D*.78),'--faixa-delay':s(D*I*.55)},'fxl-laco fxl-faixa',`faixa-${id}`));
    }
    // impacto: em cada alvo, depois do contato
    if(landed){
      const dur=reduced?.35:Math.max(.42,D*(1-I)*fam.tempo);
      const giroBase=(fam.giro??0)+GIRO_DA_VARIANTE[perfil?.variant??0];
      alvos.forEach((uid,i)=>{
        const p=point(uid),q=px(p),vx=q.x-a.x,vy=q.y-a.y;
        const direcao=Math.atan2(vy,vx)*180/Math.PI;
        const espelho=!fam.aponta&&vx<-1?-1:1;
        const giro=fam.aponta?direcao:giroBase*espelho;
        const t=Math.min(medal*(perfil?.scale??fam.escala)*(beat.grand?1.25:1)*(area&&i>0?.9:1),Math.min(size.w,size.h)*.92);
        // o clarão do contato vem por baixo, no alvo principal
        if(fam.acento&&i===0&&!reduced)nodes.push(camada(fam.acento,{left:`${p.x}%`,top:`${p.y}%`,width:t*.62,height:t*.62,'--ang':`${direcao}deg`,'--dur':s(Math.max(.35,dur*.6))},'fxl-impacto fxl-acento',`ac-${id}-${uid}`));
        nodes.push(camada(fam.impacto,{left:`${p.x}%`,top:`${p.y}%`,width:t,height:t,'--ang':`${giro}deg`,'--flip':espelho,'--dur':s(dur),'--delay':s(area?i*.07:0)},`fxl-impacto ${reduced?'fxl-parado':''}`,`imp-${id}-${uid}`));
      });
    }
  }

  const outcomes=(beat?.impacted?beat.events:[]).filter(e=>e.target===beat?.event.target&&['damage','status','interrupt','shield','block','heal'].includes(e.kind)).slice(0,3);
  const outcome=(event:typeof outcomes[number])=>event.kind==='damage'?{label:'Dano',icon:Zap}:event.kind==='interrupt'?{label:'Interrompido',icon:ArrowDown}:event.kind==='status'?{label:event.status?statusCatalog[event.status].name:'Efeito',icon:Sparkles}:event.kind==='heal'?{label:'Recuperação',icon:HeartPulse}:{label:'Protegido',icon:ShieldCheck};
  const style={'--fx-cor':cor,'--fx-color':character?.color??'#d2f276'} as CSSProperties;
  return <div ref={root} className={`battle-effects directed-effects ${beat?.grand?'grand-event':''} ${reduced?'reduced':''}`} aria-hidden="true" style={style} data-familia={chave}>
    {nodes}
    {beat&&!beat.periodic&&beat.event.kind==='turn'&&<div className={`action-title ${landed?'landed':''} ${beat.grand?'title-grand':''}`} key={beat.event.id}><SkillIcon type={beat.event.visual??'impact'} size={20} characterId={source?.characterId} skillId={source&&beat.event.skill!==undefined?character?.skills[beat.event.skill]?.id:undefined}/><div><small>{beat.event.kind==='turn'?(beat.event.source.startsWith('player')?'SEU TRIO':'RIVAIS'):character?.name??'NEXUS'}</small><strong>{beat.event.kind==='turn'?'VIRADA!':beat.event.label}</strong>{outcomes.length>0&&<span className="action-outcomes">{outcomes.slice(0,2).map(e=>{const x=outcome(e),Icon=x.icon;return <i key={e.id}><Icon size={12}/>{x.label}</i>;})}</span>}</div></div>}
  </div>;
}
