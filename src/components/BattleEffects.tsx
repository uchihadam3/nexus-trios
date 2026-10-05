import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { SkillIcon } from './Icon';
import { ArrowDown,HeartPulse,ShieldCheck,Sparkles,Zap } from 'lucide-react';
import { statuses as statusCatalog } from '../data/statuses';
export interface Anchor {x:number;y:number}
export type Anchors=Record<string,Anchor>;
export function fallbackPoint(uid:string):Anchor{const [side,slot]=uid.split('-');return {x:17+Number(slot)*33,y:side==='enemy'?16:76};}
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
export function BattleEffects({battle,beat,anchors,enabled,reduced}:{battle:Battle;beat:Beat|null;anchors:Anchors;enabled:boolean;reduced:boolean}){
  const point=(uid:string)=>anchors[uid]??fallbackPoint(uid);
  const casts=battle.fighters.filter(f=>f.cast&&f.hp>0);
  const source=beat?battle.fighters.find(f=>f.uid===beat.event.source):null;
  const color=source?byId[source.characterId].color:'#d2f276';
  const p1=beat&&beat.event.kind!=='turn'?point(beat.event.source):{x:50,y:50},p2=beat?.event.target?point(beat.event.target):p1;
  const progress=beat?beat.elapsed/beat.duration:0,flight=Math.min(1,Math.max(0,(progress-.18)/.3)),burst=Math.min(1,Math.max(0,(progress-P.impactAt)/.4));
  const projectile={x:lerp(p1.x,p2.x,flight),y:lerp(p1.y,p2.y,flight)};
  const path=`M${p1.x} ${p1.y} L${p2.x} ${p2.y}`;
  const family=beat?.family??'physical';
  const atlasFamily=beat?.grand?'grand':family==='turn'?'energy':family==='physical'?'impact':family;
  const effectAnchor=beat?.event.kind==='cast'?p1:p2;
  const particleCount=Math.min(P.impactParticles,P.particleLimit);
  const connections=(beat?.impacted?beat.events:[]).filter(e=>['synergy','shield','heal','block'].includes(e.kind)&&e.target&&e.source!==e.target&&e.source.split('-')[0]===e.target.split('-')[0]).filter((e,i,a)=>a.findIndex(x=>x.source===e.source&&x.target===e.target)===i).slice(0,P.maxConnections);
  const statuses=(beat?.impacted?beat.events:[]).filter(e=>e.kind==='status').slice(0,3);
  const outcomes=(beat?.impacted?beat.events:[]).filter(e=>e.target===beat?.event.target&&['damage','status','interrupt','shield','block','heal'].includes(e.kind)).slice(0,3);
  const outcome=(event:typeof outcomes[number])=>event.kind==='damage'?{label:'Dano',icon:Zap}:event.kind==='interrupt'?{label:'Interrompido',icon:ArrowDown}:event.kind==='status'?{label:event.status?statusCatalog[event.status].name:'Efeito',icon:Sparkles}:event.kind==='heal'?{label:'Recuperação',icon:HeartPulse}:{label:'Protegido',icon:ShieldCheck};
  return <div className={`battle-effects directed-effects family-${family} ${beat?.grand?'grand-event':''} ${reduced?'reduced':''}`} aria-hidden="true" style={{'--fx-color':color,'--fx-strength':P.vfxIntensity} as React.CSSProperties}>
    {enabled&&<svg className="direction-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
      {casts.map(f=>{const a=point(f.uid),t=point(f.cast!.targets[0]??f.uid);return <g key={f.uid} className="threat-line"><path d={`M${a.x} ${a.y} Q50 50 ${t.x} ${t.y}`}/><ellipse cx={a.x} cy={a.y} rx="8" ry="5"/><path className="target-cross" d={`M${t.x-3} ${t.y}h6 M${t.x} ${t.y-2}v4`}/></g>;})}
      {beat&&beat.event.kind!=='cast'&&<g key={beat.event.id} className="directed-action">
        {!reduced&&progress>.18&&progress<.62&&<g className={`trajectory trajectory-${family}`}>
          <path d={path} className="trajectory-aura" pathLength="100" strokeDasharray={`${flight*100} 100`}/>
          {family==='electric'?<path className="electric-path" d={`M${p1.x} ${p1.y} L${p1.x+3} ${lerp(p1.y,p2.y,.2)} L${p1.x-4} ${lerp(p1.y,p2.y,.35)} L${p2.x+4} ${lerp(p1.y,p2.y,.65)} L${p2.x-3} ${lerp(p1.y,p2.y,.8)} L${p2.x} ${p2.y}`}/>:<path d={path} className="trajectory-core" pathLength="100" strokeDasharray={`${flight*100} 100`}/>}
          <ellipse className="projectile" cx={projectile.x} cy={projectile.y} rx={beat.grand?1.9:1.1} ry={beat.grand?1.2:.7}/>
        </g>}
        {beat.impacted&&<g className="impact-shape" style={{opacity:reduced ? .75 : 1-burst*.8}}>
          {['shield','prison'].includes(family)?<path className="shield-shape" d={`M${p2.x} ${p2.y-7} L${p2.x+8} ${p2.y-4} L${p2.x+7} ${p2.y+4} L${p2.x} ${p2.y+8} L${p2.x-7} ${p2.y+4} L${p2.x-8} ${p2.y-4} Z`}/>:family==='slash'?<><path className="slash-shape" d={`M${p2.x-9} ${p2.y+6} Q${p2.x} ${p2.y-2} ${p2.x+9} ${p2.y-6}`}/><path className="slash-shape" d={`M${p2.x-7} ${p2.y+8} L${p2.x+7} ${p2.y-5}`}/></>:<><ellipse cx={p2.x} cy={p2.y} rx={5+burst*9} ry={3+burst*6} className="impact-ring"/><ellipse cx={p2.x} cy={p2.y} rx={3+burst*5} ry={2+burst*3} className="impact-core"/></>}
          {['heal','regen','buff'].includes(family)&&<path className="heal-plus" d={`M${p2.x-3} ${p2.y}h6 M${p2.x} ${p2.y-2}v4`}/>}
          {!reduced&&Array.from({length:particleCount},(_,i)=>{const a=i*Math.PI*2/particleCount,r=4+burst*11;return <path className="impact-particle" key={i} d={`M${p2.x+Math.cos(a)*r} ${p2.y+Math.sin(a)*r*.65} l${Math.cos(a)*2} ${Math.sin(a)*1.3}`}/>;})}
        </g>}
      </g>}
      {connections.map(e=>{const a=point(e.source),t=e.kind==='synergy'&&e.skill!==undefined?(anchors[`${e.target}-${e.skill}`]??point(e.target!)):point(e.target!);const travel=Math.min(1,burst*1.7),cy=a.y<50?43:57,pulse={x:(1-travel)**2*a.x+2*(1-travel)*travel*50+travel**2*t.x,y:(1-travel)**2*a.y+2*(1-travel)*travel*cy+travel**2*t.y};return <g key={e.id} className={`connection connection-${e.kind}`}><path d={`M${a.x} ${a.y} Q50 ${a.y<50?43:57} ${t.x} ${t.y}`}/>{!reduced&&<ellipse className="connection-pulse" cx={pulse.x} cy={pulse.y} rx="1.1" ry=".7"/>}<ellipse cx={t.x} cy={t.y} rx="3.5" ry="2.2"/>{e.kind==='block'&&<path className="guard-dome" d={`M${t.x-8} ${t.y+2} Q${t.x} ${t.y-12} ${t.x+8} ${t.y+2}`}/>}</g>;})}
      {beat?.impacted&&beat.events.filter(e=>e.kind==='interrupt').map(e=>{const t=point(e.target!);return <g className="shattered" key={e.id}><path d={`M${t.x-7} ${t.y-5}l4 2m2 2l3 2m-8 5l3-3m3-3l4-4`}/><ellipse cx={t.x} cy={t.y} rx="9" ry="6" strokeDasharray="2 3"/></g>;})}
      {statuses.map(e=>{const t=point(e.target!);return <g key={e.id} className={`status-effect status-effect-${e.status}`}><ellipse cx={t.x} cy={t.y} rx="8" ry="5.5"/>{e.status==='regen'?<path d={`M${t.x-2} ${t.y}h4 M${t.x} ${t.y-2}v4`}/>:e.status==='rooted'?<path d={`M${t.x-7} ${t.y-4}l14 8m-14 0l14-8`}/>:null}</g>;})}
    </svg>}
    {enabled&&beat&&!reduced&&<div key={`sprite-${beat.event.id}`} className={`effect-sprite sprite-${atlasFamily} ${beat.grand?'sprite-grand':''} ${beat.event.kind==='cast'?'sprite-cast':''} ${beat.impacted?'sprite-landed':''}`} style={{left:`${effectAnchor.x}%`,top:`${effectAnchor.y}%`,'--sprite-image':`url(/assets/vfx/${atlasFamily}.webp)`} as React.CSSProperties}/>}
    {beat&&beat.event.kind!=='basic'&&<div className={`action-title ${beat.impacted?'landed':''}`} key={beat.event.id}><span className="title-rule"/><SkillIcon type={beat.event.visual??'impact'} size={18} characterId={source?.characterId} skillId={source&&beat.event.skill!==undefined?byId[source.characterId].skills[beat.event.skill]?.id:undefined}/><div><small>{beat.event.kind==='turn'?(beat.event.source.startsWith('player')?'SEU TRIO':'RIVAIS'):source?byId[source.characterId].name:'NEXUS'}</small><strong>{beat.event.kind==='turn'?'VIRADA DE DOMÍNIO':beat.event.label}</strong>{outcomes.length>0&&<span className="action-outcomes">{outcomes.map(e=>{const x=outcome(e),Icon=x.icon;return <i key={e.id}><Icon size={10}/>{x.label}</i>;})}</span>}</div><span className="title-rule"/></div>}
  </div>;
}
