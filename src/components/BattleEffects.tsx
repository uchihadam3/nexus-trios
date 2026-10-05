import type { CSSProperties } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { SkillIcon } from './Icon';
import { ArrowDown,HeartPulse,ShieldCheck,Sparkles,Zap } from 'lucide-react';
import { statuses as statusCatalog } from '../data/statuses';
import { profileFor } from '../presentation/vfxProfiles';

export interface Anchor {x:number;y:number}
export type Anchors=Record<string,Anchor>;
export function fallbackPoint(uid:string):Anchor{const [side,slot]=uid.split('-');return {x:17+Number(slot)*33,y:side==='enemy'?16:76};}
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const familiesWithTravel=new Set(['energy','electric','fire','slash','magic','psychic','dark']);

/** Places generated family atlases and lets skill data choose a distinct staging motif. */
export function BattleEffects({battle,beat,anchors,enabled,reduced}:{battle:Battle;beat:Beat|null;anchors:Anchors;enabled:boolean;reduced:boolean}){
  const point=(uid:string)=>anchors[uid]??fallbackPoint(uid);
  const casts=battle.fighters.filter(f=>f.cast&&f.hp>0);
  const source=beat?battle.fighters.find(f=>f.uid===beat.event.source):null;
  const character=source?byId[source.characterId]:null;
  const profile=profileFor(source?.characterId??'',beat?.event.skill);
  const color=character?.color??'#d2f276';
  const p1=beat&&beat.event.kind!=='turn'?point(beat.event.source):{x:50,y:50};
  const p2=beat?.event.target?point(beat.event.target):p1;
  const progress=beat?beat.elapsed/beat.duration:0;
  const flight=Math.min(1,Math.max(0,(progress-.06)/(P.impactAt-.06)));
  const landed=beat?.impacted??false;
  const family=profile?.family??beat?.family??'physical';
  const atlasFamily=family==='grand'?'grand':family==='turn'?'energy':family==='physical'?'physical':family;
  const effectAnchor=beat?.event.kind==='cast'?p1:p2;
  const travel=!!beat&&beat.event.kind!=='cast'&&(profile?.travel??familiesWithTravel.has(family));
  const projectile={x:lerp(p1.x,p2.x,flight),y:lerp(p1.y,p2.y,flight)};
  const dx=p2.x-p1.x,dy=(p2.y-p1.y)*1.28;
  const beamStyle={'--beam-angle':`${Math.atan2(dy,dx)*180/Math.PI}deg`,'--beam-length':`${Math.hypot(dx,dy)*flight}%`,'--beam-mid-x':`${p1.x+dx*flight/2}%`,'--beam-mid-y':`${p1.y+(p2.y-p1.y)*flight/2}%`} as CSSProperties;
  const affected=beat?.events.filter(e=>e.target&&e.target!==e.source&&['damage','status','shield','heal','interrupt','block'].includes(e.kind))??[];
  const area=!!profile?.area||new Set(affected.map(e=>e.target)).size>=3;
  const scale=profile?.scale??(beat?.grand?1.42:1);
  const connections=(beat?.impacted?beat.events:[]).filter(e=>['synergy','shield','heal','block'].includes(e.kind)&&e.target&&e.source!==e.target&&e.source.split('-')[0]===e.target.split('-')[0]).filter((e,i,a)=>a.findIndex(x=>x.source===e.source&&x.target===e.target)===i).slice(0,P.maxConnections);
  const statuses=(beat?.impacted?beat.events:[]).filter(e=>e.kind==='status'&&e.target).slice(0,3);
  const outcomes=(beat?.impacted?beat.events:[]).filter(e=>e.target===beat?.event.target&&['damage','status','interrupt','shield','block','heal'].includes(e.kind)).slice(0,3);
  const outcome=(event:typeof outcomes[number])=>event.kind==='damage'?{label:'Dano',icon:Zap}:event.kind==='interrupt'?{label:'Interrompido',icon:ArrowDown}:event.kind==='status'?{label:event.status?statusCatalog[event.status].name:'Efeito',icon:Sparkles}:event.kind==='heal'?{label:'Recuperação',icon:HeartPulse}:{label:'Protegido',icon:ShieldCheck};
  const style={'--fx-color':color,'--fx-strength':P.vfxIntensity,'--fx-scale':scale} as CSSProperties;
  const sprite=(anchor:Anchor,extra:string,key:string,duration?:number)=><div key={key} className={`effect-sprite sprite-${atlasFamily} ${extra}`} style={{left:`${anchor.x}%`,top:`${anchor.y}%`,'--sprite-image':`url(/assets/vfx/${atlasFamily}.webp)`,...(duration?{'--travel-duration':`${duration}s`}:{})} as CSSProperties}/>;
  return <div className={`battle-effects directed-effects family-${family} motif-${profile?.motif??'default'} ${beat?.grand?'grand-event':''} ${reduced?'reduced':''}`} aria-hidden="true" style={style}>
    {enabled&&<svg className="direction-svg utility-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
      {casts.map(f=>{const a=point(f.uid),t=point(f.cast!.targets[0]??f.uid);return <g key={f.uid} className="threat-line"><path d={`M${a.x} ${a.y} Q50 50 ${t.x} ${t.y}`}/><ellipse cx={a.x} cy={a.y} rx="8" ry="5"/><path className="target-cross" d={`M${t.x-3} ${t.y}h6 M${t.x} ${t.y-2}v4`}/></g>;})}
      {connections.map(e=>{const a=point(e.source),t=point(e.target!);const q=Math.min(1,Math.max(0,(progress-P.impactAt)/.7));const pulse={x:lerp(a.x,t.x,q),y:lerp(a.y,t.y,q)};return <g key={e.id} className={`connection connection-${e.kind}`}><path d={`M${a.x} ${a.y} Q50 ${a.y<50?43:57} ${t.x} ${t.y}`}/>{!reduced&&<ellipse className="connection-pulse" cx={pulse.x} cy={pulse.y} rx="1.1" ry=".7"/>}<ellipse cx={t.x} cy={t.y} rx="3.5" ry="2.2"/></g>;})}
    </svg>}
    {enabled&&beat&&beat.event.kind!=='turn'&&<>
      {area&&<div key={`area-${beat.event.id}`} className={`area-vfx area-${family}`} style={{'--area-alpha':landed?.72:.28} as CSSProperties}/>}
      {beat.event.kind==='cast'&&sprite(effectAnchor,'sprite-cast sprite-charge',`charge-${beat.event.id}`)}
      {travel&&!landed&&!reduced&&progress>.08&&progress<P.impactAt&&sprite(projectile,`sprite-travel motif-travel-${profile?.motif??family}`,`travel-${beat.event.id}`,beat.duration*P.impactAt)}
      {travel&&!landed&&['beam','heat-vision'].includes(profile?.motif??'')&&<div className={`beam-ribbon beam-${profile?.motif}`} style={beamStyle}/>}
      {landed&&sprite(effectAnchor,`sprite-landed sprite-impact ${area?'sprite-area-impact':''}`,`impact-${beat.event.id}`)}
      {landed&&profile?.motif==='portal'&&sprite(p1,'sprite-landed portal-exit',`portal-${beat.event.id}`)}
      {landed&&['shield','buff'].includes(family)&&<div className="card-aura card-guard" style={{left:`${p2.x}%`,top:`${p2.y}%`}}/>}
      {landed&&family==='heal'&&<div className="card-aura card-heal" style={{left:`${p2.x}%`,top:`${p2.y}%`}}/>}
      {landed&&family==='electric'&&<div className="card-aura card-electric" style={{left:`${p2.x}%`,top:`${p2.y}%`}}/>}
    </>}
    {enabled&&beat?.impacted&&statuses.map(e=>{const t=point(e.target!);return sprite(t,`sprite-status status-${e.status}`,`status-${e.id}`,78);})}
    {beat&&beat.event.kind!=='basic'&&<div className={`action-title ${landed?'landed':''} ${beat.grand?'title-grand':''}`} key={beat.event.id}><span className="title-rule"/><SkillIcon type={beat.event.visual??'impact'} size={20} characterId={source?.characterId} skillId={source&&beat.event.skill!==undefined?character?.skills[beat.event.skill]?.id:undefined}/><div><small>{beat.event.kind==='turn'?(beat.event.source.startsWith('player')?'SEU TRIO':'RIVAIS'):character?.name??'NEXUS'}</small><strong>{beat.event.kind==='turn'?'VIRADA DE DOMÍNIO':beat.event.label}</strong>{outcomes.length>0&&<span className="action-outcomes">{outcomes.map(e=>{const x=outcome(e),Icon=x.icon;return <i key={e.id}><Icon size={12}/>{x.label}</i>;})}</span>}</div><span className="title-rule"/></div>}
  </div>;
}
