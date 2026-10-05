import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];before:Battle;after:Battle;duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;idle:number;complete:boolean;serial:number;signals:BattleEvent[]}
export interface Cue {event:BattleEvent;family:Family;phase:'start'|'impact';grand:boolean}
export function familyOf(event:BattleEvent,battle:Battle):Family {
  if(event.kind==='ko'||event.kind==='turn'||event.kind==='interrupt')return event.kind;
  if(event.kind==='heal')return 'heal';
  if(event.kind==='shield'||event.kind==='block')return 'shield';
  if(event.status){if(event.status==='regen')return 'regen';if(event.status==='burning')return 'fire';if(['haste','strengthened','protected'].includes(event.status))return 'buff';if(['rooted','paralyzed'].includes(event.status))return 'prison';return 'debuff';}
  const f=battle.fighters.find(f=>f.uid===event.source),c=f?byId[f.characterId]:null;
  const effects=event.skill!==undefined?c?.skills[event.skill].effects:[];
  if(effects?.some(e=>e.kind==='status'&&e.status==='burning'))return 'fire';
  if(effects?.length&&!effects.some(e=>e.kind==='damage'||e.kind==='deathnote')){
    if(effects.some(e=>e.kind==='heal'))return 'heal';
    if(effects.some(e=>e.kind==='shield'))return 'shield';
    const status=effects.find(e=>e.kind==='status');
    if(status?.kind==='status'){if(status.status==='regen')return 'regen';if(status.status==='burning')return 'fire';if(['strengthened','haste','protected'].includes(status.status))return 'buff';if(['rooted','paralyzed'].includes(status.status))return 'prison';return 'debuff';}
  }
  if(c?.id==='raven'&&event.visual==='psychic')return 'dark';
  return ({impact:'physical',beam:'energy',bolt:'electric',wave:'magic',psychic:'psychic',slash:'slash',web:'prison',shield:'shield'} as const)[event.visual??'impact'];
}
function focus(events:BattleEvent[]):BattleEvent|undefined {
  return events.find(e=>e.kind==='basic'||e.kind==='skill'||e.kind==='cast')
    ??events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='turn');
}
function duration(event:BattleEvent,grand:boolean){
  if(event.kind==='cast')return P.preparationSeconds;
  if(event.kind==='ko')return P.knockoutSeconds;
  if(event.kind==='turn')return P.turnaroundSeconds;
  if(event.kind==='interrupt')return P.interruptSeconds;
  return grand?P.grandSeconds:event.kind==='skill'?P.skillSeconds:P.normalSeconds;
}
export function createDirection(battle:Battle):Direction {
  return {battle,visible:structuredClone(battle),queue:[],active:null,idle:0,complete:false,serial:0,signals:[]};
}
// The director requests at most one combat tick at a time. Its bounded queue contains
// only snapshots from that tick, so effects never trail behind a running simulation.
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void):void {
  let budget=seconds;d.signals=[];
  while(budget>1e-8&&!d.complete){
    if(d.active){
      const beat=d.active,take=Math.min(budget,beat.duration-beat.elapsed);beat.elapsed+=take;budget-=take;
      if(!beat.impacted&&beat.elapsed>=beat.duration*P.impactAt){beat.impacted=true;d.visible=beat.after;d.signals.push(...beat.events);onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});}
      if(beat.elapsed>=beat.duration-1e-8){d.visible=beat.after;d.active=null;}
      continue;
    }
    if(d.queue.length){d.active=d.queue.shift()!;d.visible=d.active.before;d.serial++;onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});continue;}
    if(d.battle.finished){d.visible=structuredClone(d.battle);d.complete=true;break;}
    const wait=STEP/P.gameRate-d.idle,take=Math.min(wait,budget);d.idle+=take;budget-=take;
    if(d.idle<STEP/P.gameRate-1e-8)continue;
    d.idle=0;let previous=structuredClone(d.battle),lastId=d.battle.nextEvent-1;
    stepBattle(d.battle,current=>{
      const events=current.events.filter(e=>e.id>lastId);lastId=current.nextEvent-1;
      const next=structuredClone(current),event=focus(events);
      if(event){
        const actor=current.fighters.find(f=>f.uid===event.source);
        const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
        const grand=event.kind==='skill'&&prep>=P.grandPreparation;
        d.queue.push({event,events,before:previous,after:next,duration:duration(event,grand),family:familyOf(event,current),grand,elapsed:0,impacted:false});
      }else if(d.queue.length){d.queue[d.queue.length-1].after=next;d.queue[d.queue.length-1].events.push(...events);}
      else {d.visible=next;d.signals.push(...events);}
      previous=next;
    });
  }
}
