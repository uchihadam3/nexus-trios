import { useLayoutEffect,useRef,useState,type CSSProperties } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { SkillIcon } from './Icon';
import { ArrowDown,HeartPulse,ShieldCheck,Sparkles,Zap } from 'lucide-react';
import { statuses as statusCatalog } from '../data/statuses';
import { atlasFor,profileFor,type VfxFamily } from '../presentation/vfxProfiles';

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
const legacyFamily:Record<string,VfxFamily>={physical:'physical_light',energy:'energy_orb',electric:'electric',fire:'fire',magic:'magic_psychic',psychic:'magic_psychic',dark:'dark',slash:'slash',prison:'control',shield:'shield',heal:'heal_buff',regen:'heal_buff',buff:'heal_buff',debuff:'control',interrupt:'physical_heavy',ko:'physical_heavy',grand:'physical_heavy',turn:'magic_psychic'};

/** At most three atlas/beam nodes during an action. CSS animates transform, opacity and sheet position. */
export function BattleEffects({battle,beat,anchors,enabled,reduced}:{battle:Battle;beat:Beat|null;anchors:Anchors;enabled:boolean;reduced:boolean}){
  const root=useRef<HTMLDivElement>(null),[size,setSize]=useState({w:0,h:0});
  useLayoutEffect(()=>{const element=root.current;if(!element)return;const observer=new ResizeObserver(([entry])=>setSize({w:entry.contentRect.width,h:entry.contentRect.height}));observer.observe(element);return ()=>observer.disconnect();},[]);
  const point=(uid:string)=>anchors[uid]??fallbackPoint(uid);
  const source=beat?battle.fighters.find(f=>f.uid===beat.event.source):null;
  const character=source?byId[source.characterId]:null;
  const profile=profileFor(source?.characterId??'',beat?.event.skill);
  const family=profile?.family??legacyFamily[beat?.family??'physical'];
  const p1=beat&&beat.event.kind!=='turn'?point(beat.event.source):{x:50,y:50};
  const p2=beat?.event.target?point(beat.event.target):p1;
  const area=isAreaBeat(beat,battle),landed=beat?.impacted??false;
  const travel=!!beat&&beat.event.kind!=='cast'&&beat.event.kind!=='turn'&&profile?.travel&&!!beat.event.target;
  const beam=travel&&family==='energy_beam';
  const scale=(profile?.scale??1)*(beat?.grand?1.26:1);
  const dx=(p2.x-p1.x)*size.w/100,dy=(p2.y-p1.y)*size.h/100;
  const beamStyle={left:`${p1.x}%`,top:`${p1.y}%`,'--beam-length':`${Math.hypot(dx,dy)}px`,'--beam-angle':`${Math.atan2(dy,dx)}rad`,'--beam-duration':`${Math.max(.12,(beat?.duration??1)*P.impactAt)}s`} as CSSProperties;
  const outcomes=(beat?.impacted?beat.events:[]).filter(e=>e.target===beat?.event.target&&['damage','status','interrupt','shield','block','heal'].includes(e.kind)).slice(0,3);
  const outcome=(event:typeof outcomes[number])=>event.kind==='damage'?{label:'Dano',icon:Zap}:event.kind==='interrupt'?{label:'Interrompido',icon:ArrowDown}:event.kind==='status'?{label:event.status?statusCatalog[event.status].name:'Efeito',icon:Sparkles}:event.kind==='heal'?{label:'Recuperação',icon:HeartPulse}:{label:'Protegido',icon:ShieldCheck};
  const style={'--fx-color':character?.color??'#d2f276','--fx-scale':scale} as CSSProperties;
  const sprite=(anchor:Anchor,kind:'charge'|'travel'|'impact',key:string,extra='')=><div key={key} className={`effect-sprite sprite-${kind} ${extra}`} style={{left:`${anchor.x}%`,top:`${anchor.y}%`,'--sprite-image':`url(/assets/vfx/${atlasFor(family)}.webp)`,'--move-x':`${p2.x-p1.x}cqw`,'--move-y':`${p2.y-p1.y}cqh`,'--travel-duration':`${Math.max(.14,(beat?.duration??1)*P.impactAt)}s`,'--impact-duration':`${reduced?.18:Math.min(.55,Math.max(.25,(beat?.duration??1)*(1-P.impactAt)))}s`} as CSSProperties}/>;
  return <div ref={root} className={`battle-effects directed-effects ${beat?.grand?'grand-event':''} ${reduced?'reduced':''}`} aria-hidden="true" style={style}>
    {enabled&&beat&&beat.event.kind!=='turn'&&<>
      {!landed&&(beat.event.kind==='cast'||beat.event.kind==='skill')&&sprite(p1,'charge',`charge-${beat.event.id}`)}
      {travel&&!landed&&!reduced&&sprite(p1,'travel',`travel-${beat.event.id}`,beam?'sprite-beam-travel':'')}
      {beam&&!landed&&!reduced&&size.w>0&&<div className="fx-beam" style={beamStyle}/>}
      {landed&&sprite(beat.event.kind==='cast'?p1:p2,'impact',`impact-${beat.event.id}`,`${area?'sprite-area-impact':''} ${beat.grand?'sprite-grand-impact':''}`)}
      {landed&&(area||beat.grand)&&!reduced&&sprite({x:50,y:50},'impact',`accent-${beat.event.id}`,'sprite-accent')}
    </>}
    {beat&&!beat.periodic&&!['basic','ready','status'].includes(beat.event.kind)&&<div className={`action-title ${landed?'landed':''} ${beat.grand?'title-grand':''}`} key={beat.event.id}><span className="title-rule"/><SkillIcon type={beat.event.visual??'impact'} size={20} characterId={source?.characterId} skillId={source&&beat.event.skill!==undefined?character?.skills[beat.event.skill]?.id:undefined}/><div><small>{beat.event.kind==='turn'?(beat.event.source.startsWith('player')?'SEU TRIO':'RIVAIS'):character?.name??'NEXUS'}</small><strong>{beat.event.kind==='turn'?'VIRADA DE DOMÍNIO':beat.event.label}</strong>{outcomes.length>0&&<span className="action-outcomes">{outcomes.map(e=>{const x=outcome(e),Icon=x.icon;return <i key={e.id}><Icon size={12}/>{x.label}</i>;})}</span>}</div><span className="title-rule"/></div>}
  </div>;
}
