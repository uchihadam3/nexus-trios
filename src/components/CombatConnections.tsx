import type { CSSProperties } from 'react';
import type { Battle } from '../engine/types';
import type { Beat } from '../presentation/director';
import { combatLinks } from '../presentation/combat-links';
import type { Anchors } from './BattleEffects';

const fallback=(uid:string)=>({x:17+Number(uid.split('-')[1])*33,y:uid.startsWith('enemy')?17:78});

/*
 * As linhas de quem age até cada alvo. Sem legenda no meio da arena: o
 * movimento, a cor e o efeito já dizem quem fez o quê, e o nome por extenso
 * tapava a luta (o histórico guarda o texto).
 */
export function CombatConnections({battle,beat,anchors,reduced}:{battle:Battle;beat:Beat|null;anchors:Anchors;reduced:boolean}){
  const links=combatLinks(beat,battle),active=!!beat&&!beat.impacted;
  const point=(uid:string)=>anchors[uid]??fallback(uid);
  if(!beat||!links.length)return null;
  return <div className={`combat-connections ${active?'winding':'landed'} ${reduced?'still':''}`} data-phase={active?'travel':'impact'} aria-hidden="true" style={{'--link-time':`${Math.max(.15,beat.duration*.48)}s`} as CSSProperties}>
    <svg className="combat-paths" viewBox="0 0 100 100" preserveAspectRatio="none">
      {links.map(link=>{const a=point(link.source),b=point(link.target),midX=(a.x+b.x)/2,midY=(a.y+b.y)/2+(a.y>b.y?-4:4),path=`M ${a.x} ${a.y} Q ${midX} ${midY} ${b.x} ${b.y}`;
        return <g key={link.id} className={`combat-path path-${link.kind}`} data-link={`${link.source}:${link.target}:${link.kind}`}>
          <path d={path} pathLength="100" className="combat-path-halo"/><path d={path} pathLength="100" className="combat-path-stroke"/>
          {!reduced&&active&&<circle r="2.2" className="combat-tracer"><animateMotion dur={`${Math.max(.15,beat.duration*.48)}s`} path={path} fill="freeze"/></circle>}
          <circle cx={b.x} cy={b.y} r="2.1" className="combat-target-node"/>
        </g>;
      })}
    </svg>
  </div>;
}
