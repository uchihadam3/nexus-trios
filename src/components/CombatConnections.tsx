import type { CSSProperties } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { combatLinks,type LinkKind } from '../presentation/combat-links';
import { byId } from '../data/characters';
import type { Anchors } from './BattleEffects';

const readable:Record<LinkKind,string>={attack:'ataca',heal:'cura',shield:'protege',buff:'fortalece',debuff:'afeta',interrupt:'interrompe',support:'ajuda'};
const fallback=(uid:string)=>({x:17+Number(uid.split('-')[1])*33,y:uid.startsWith('enemy')?17:78});

export function CombatConnections({battle,beat,anchors,reduced}:{battle:Battle;beat:Beat|null;anchors:Anchors;reduced:boolean}){
  const links=combatLinks(beat,battle),active=!!beat&&!beat.impacted;
  const byUid=(uid:string)=>byId[battle.fighters.find(f=>f.uid===uid)?.characterId??'']?.name??uid;
  const point=(uid:string)=>anchors[uid]??fallback(uid);
  const primary=links.find(link=>link.source===beat?.event.source)??links[0];
  const primaryTargets=primary?links.filter(link=>link.source===primary.source&&link.kind===primary.kind).map(link=>byUid(link.target)):[];
  const actionName=beat?.event.kind==='cast'?'PREPARANDO':beat?.event.kind==='basic'?'ATAQUE BÁSICO':beat?.event.kind==='skill'?'HABILIDADE':beat?.event.kind==='interrupt'?'INTERRUPÇÃO':'';
  if(!beat||!links.length)return null;
  return <div className={`combat-connections ${active?'winding':'landed'} ${reduced?'still':''}`} data-phase={active?'travel':'impact'} aria-hidden="true" style={{'--link-time':`${Math.max(.15,beat.duration*.48)}s`} as CSSProperties}>
    <svg className="combat-paths" viewBox="0 0 100 100" preserveAspectRatio="none">
      {links.map(link=>{const a=point(link.source),b=point(link.target),midX=(a.x+b.x)/2,midY=(a.y+b.y)/2+(a.y>b.y?-4:4),path=`M ${a.x} ${a.y} Q ${midX} ${midY} ${b.x} ${b.y}`;
        return <g key={link.id} className={`combat-path path-${link.kind}`} data-link={`${link.source}:${link.target}:${link.kind}`}>
          <path d={path} pathLength="100" className="combat-path-halo"/><path d={path} pathLength="100" className="combat-path-stroke"/>
          {!reduced&&active&&<circle r="1.25" className="combat-tracer"><animateMotion dur={`${Math.max(.15,beat.duration*.48)}s`} path={path} fill="freeze"/></circle>}
          <circle cx={b.x} cy={b.y} r="2.1" className="combat-target-node"/>
        </g>;
      })}
    </svg>
    {primary&&<div className={`combat-caption caption-${primary.kind}`} key={beat.event.id}>
      <small>{actionName||readable[primary.kind].toLocaleUpperCase('pt-BR')}</small>
      <strong>{byUid(primary.source)} <span>→</span> {primaryTargets.slice(0,3).join(' · ')}</strong>
      {beat.event.kind==='skill'&&<em>{beat.event.label}</em>}
    </div>}
  </div>;
}
