import type { Battle,BattleEvent } from '../engine/types';
import type { Beat } from './director';

export type LinkKind='attack'|'heal'|'shield'|'buff'|'debuff'|'interrupt'|'support';
export interface CombatLink {id:string;source:string;target:string;kind:LinkKind;event?:BattleEvent}

/** Reads consequences already computed by the engine; it never selects a target. */
export function combatLinks(beat:Beat|null,battle:Battle):CombatLink[]{
  if(!beat||beat.event.kind==='turn'||beat.periodic)return [];
  const side=(uid:string)=>battle.fighters.find(f=>f.uid===uid)?.side;
  const links:CombatLink[]=[],seen=new Set<string>();
  const add=(source:string,target:string,kind:LinkKind,event?:BattleEvent)=>{
    if(!source||!target||source===target)return;
    const key=`${source}:${target}:${kind}`;
    if(seen.has(key))return;
    seen.add(key);links.push({id:key,source,target,kind,event});
  };
  for(const event of beat.events){
    const target=event.target;
    if(!target)continue;
    if(event.kind==='damage'||event.kind==='ko')add(event.source,target,'attack',event);
    if(event.kind==='heal')add(event.source,target,'heal',event);
    if(event.kind==='shield'||event.kind==='block')add(event.source,target,'shield',event);
    if(event.kind==='status')add(event.source,target,side(event.source)===side(target)?'buff':'debuff',event);
    if(event.kind==='interrupt')add(event.source,target,'interrupt',event);
    if(event.kind==='charge'||event.kind==='synergy'||event.kind==='tempo')add(event.source,target,'support',event);
  }
  if(beat.event.kind==='cast'){
    const actor=beat.after.fighters.find(f=>f.uid===beat.event.source);
    for(const target of actor?.cast?.targets??[])add(actor!.uid,target,'attack');
  }
  if(!links.length&&beat.event.target&&['basic','skill','interrupt'].includes(beat.event.kind)){
    add(beat.event.source,beat.event.target,side(beat.event.source)===side(beat.event.target)?'support':'attack');
  }
  return links.slice(0,9);
}
