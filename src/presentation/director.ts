import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[]}
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
  // The engine owns all mechanical state. The presentation never stores fighter snapshots.
  return {battle,visible:battle,queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[]};
}
function makeBeat(event:BattleEvent,events:BattleEvent[],battle:Battle):Beat {
  const actor=battle.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  return {event,events,duration:duration(event,grand),family:familyOf(event,battle),grand,elapsed:0,impacted:false};
}
function enqueue(d:Direction,beat:Beat){
  // Basic attacks are visual feedback. When busy, the authoritative engine still
  // applies each action exactly once; we only omit its optional animation.
  if(beat.event.kind==='basic'&&(d.active||d.queue.length))return;
  if(d.queue.length>=12){
    if(beat.event.kind==='cast')return;
    const stale=d.queue.findIndex(item=>item.event.kind==='basic'||item.event.kind==='cast');
    if(stale>=0)d.queue.splice(stale,1);
  }
  d.queue.push(beat);
}
function collect(d:Direction,events:BattleEvent[]){
  if(!events.length)return;
  d.signals.push(...events);
  // stepBattle observes after each action. Events following its principal action
  // belong to that action; periodic effects are handled individually.
  const principal=focus(events);
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    enqueue(d,makeBeat(principal,events.filter(e=>e.id>=principal.id),d.battle));
  }else{
    for(const event of events.filter(e=>['interrupt','ko','turn'].includes(e.kind)))
      enqueue(d,makeBeat(event,[event],d.battle));
  }
}
/** The engine advances on real time; visualSpeed changes only animations. */
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void,visualSpeed=1):void {
  const elapsed=Math.max(0,seconds);d.signals=[];
  if(!d.battle.finished){
    d.simIdle+=elapsed*P.gameRate;
    while(d.simIdle>=STEP-1e-8&&!d.battle.finished){
      d.simIdle=Math.max(0,d.simIdle-STEP);
      let lastId=d.battle.nextEvent-1;
      stepBattle(d.battle,current=>{
        const events=current.events.filter(e=>e.id>lastId);
        lastId=current.nextEvent-1;
        collect(d,events);
      });
    }
  }
  // A growing visual backlog shortens playback, without changing the battle clock.
  let budget=elapsed*Math.max(1,visualSpeed)*(1+Math.min(8,d.queue.length)*1.5);
  while(budget>1e-8&&!d.complete){
    if(!d.active){
      if(!d.queue.length){if(d.battle.finished)d.complete=true;break;}
      d.active=d.queue.shift()!;d.serial++;
      onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});
    }
    const beat=d.active,take=Math.min(budget,beat.duration-beat.elapsed);
    beat.elapsed+=take;budget-=take;
    if(!beat.impacted&&beat.elapsed>=beat.duration*P.impactAt){
      beat.impacted=true;
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});
    }
    if(beat.elapsed>=beat.duration-1e-8)d.active=null;
  }
  d.visible=d.battle;
  if(d.battle.finished&&!d.active&&!d.queue.length)d.complete=true;
}
