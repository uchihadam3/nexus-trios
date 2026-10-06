import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];before:Battle;after:Battle;duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean;periodic?:boolean}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[]}
export interface PresentationCheckpoint {battleTime:number;nextEvent:number;rng:number;visibleNextEvent:number;activeEventId:number|null;activeElapsed:number;impacted:boolean;serial:number;simIdle?:number}
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
  return {battle,visible:structuredClone(battle),queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[]};
}
function makeBeat(event:BattleEvent,events:BattleEvent[],before:Battle,after:Battle,periodic=false):Beat {
  const actor=after.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  const auxiliary=event.kind==='ready'||event.kind==='status';
  const seconds=periodic?P.periodicSeconds:auxiliary?P.auxiliarySeconds:duration(event,grand);
  return {event,events,before,after,duration:seconds,family:familyOf(event,after),grand,elapsed:0,impacted:false,periodic};
}
function collect(d:Direction,events:BattleEvent[],before:Battle,after:Battle,legacy=false){
  if(!events.length)return;
  // Every observer callback is a chronological boundary: one action and its
  // consequences, or periodic effects. Never merge across an action boundary.
  const principal=focus(events);
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    d.queue.push(makeBeat(principal,events,before,after));
    return;
  }
  const change=events.find(e=>e.kind==='damage'||e.kind==='heal');
  if(change){
    const burning=change.kind==='damage'&&before.fighters.find(f=>f.uid===change.target)?.statuses.some(s=>s.id==='burning');
    const event={...change,label:burning?'Queimadura':change.kind==='heal'?'Regeneração':'Efeito contínuo',status:burning?'burning' as const:change.kind==='heal'?'regen' as const:undefined};
    const last=d.queue[d.queue.length-1];
    // Adjacent periodic ticks share one legible impact, without crossing an
    // action, a knockout, or half a second of mechanical time.
    if(last?.periodic&&!events.some(e=>e.kind==='ko'||e.kind==='interrupt'||e.kind==='turn')&&
       last.event.source===event.source&&last.event.target===event.target&&last.event.kind===event.kind&&
       after.time-last.before.time<=(legacy?1.01:.51)){
      last.events.push(...events);last.after=after;
      last.event.value=(last.event.value??0)+(event.value??0);
    }else d.queue.push(makeBeat(event,events,before,after,true));
    return;
  }
  const important=events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='turn'||e.kind==='ready'||e.kind==='status'||e.kind==='shield');
  if(important)d.queue.push(makeBeat(important,events,before,after,legacy&&(important.kind==='ready'||important.kind==='status')));
}
function simulateStep(d:Direction,legacy=false){
  let previous=structuredClone(d.battle),lastId=d.battle.nextEvent-1;
  stepBattle(d.battle,current=>{
    const events=current.events.filter(e=>e.id>lastId);
    lastId=current.nextEvent-1;
    const after=structuredClone(current);
    collect(d,events,previous,after,legacy);
    previous=after;
  });
  const last=d.queue[d.queue.length-1];
  if(!legacy&&last?.periodic&&d.battle.time-last.before.time<=.51)last.after=structuredClone(d.battle);
}
export function checkpointDirection(d:Direction):PresentationCheckpoint {
  return {battleTime:d.battle.time,nextEvent:d.battle.nextEvent,rng:d.battle.rng,visibleNextEvent:d.visible.nextEvent,activeEventId:d.active?.event.id??null,activeElapsed:d.active?.elapsed??0,impacted:d.active?.impacted??false,serial:d.serial,simIdle:d.simIdle};
}
/** Rebuilds the unseen visual timeline from deterministic combat after a reload. */
export function restoreDirection(initial:Battle,saved:Battle,checkpoint:PresentationCheckpoint):Direction|null {
  if(!checkpoint||checkpoint.battleTime!==saved.time||checkpoint.nextEvent!==saved.nextEvent||checkpoint.rng!==saved.rng)return null;
  const d=createDirection(initial);
  const legacy=checkpoint.simIdle===undefined;
  while(!d.battle.finished&&d.battle.time+STEP/2<saved.time)simulateStep(d,legacy);
  if(d.battle.time!==saved.time||d.battle.nextEvent!==saved.nextEvent||d.battle.rng!==saved.rng)return null;
  const index=checkpoint.activeEventId===null?-1:d.queue.findIndex(beat=>beat.event.id===checkpoint.activeEventId);
  if(checkpoint.activeEventId!==null&&index<0)return null;
  if(index>=0){
    d.active=d.queue[index];d.queue=d.queue.slice(index+1);
    d.active.elapsed=Math.min(d.active.duration,Math.max(0,checkpoint.activeElapsed));
    d.active.impacted=checkpoint.impacted;
    d.visible=d.active.impacted?d.active.after:d.active.before;
  }else{
    const pending=d.queue.findIndex(beat=>beat.after.nextEvent>checkpoint.visibleNextEvent);
    const completed=pending<0?d.queue.length:pending;
    d.visible=pending<0?structuredClone(saved):completed?d.queue[completed-1].after:structuredClone(initial);
    d.queue=d.queue.slice(completed);
  }
  if(d.visible.nextEvent!==checkpoint.visibleNextEvent)return null;
  d.battle=saved;d.serial=checkpoint.serial;d.simIdle=checkpoint.simIdle??0;d.complete=saved.finished&&!d.active&&!d.queue.length;
  return d;
}
/** Consume combat only between beats. One render advances at most one visual boundary. */
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void,visualSpeed=1):void {
  // A delayed frame may not accumulate time to rush through unseen actions.
  const elapsed=Math.min(.25,Math.max(0,seconds))*Math.max(1,visualSpeed);d.signals=[];
  if(d.complete||elapsed===0)return;
  if(d.active){
    const beat=d.active,limit=beat.impacted?beat.duration:beat.duration*P.impactAt;
    beat.elapsed=Math.min(limit,beat.elapsed+elapsed);
    if(!beat.impacted&&beat.elapsed>=limit-1e-8){
      beat.impacted=true;
      d.visible=beat.after;
      d.signals.push(...beat.events);
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});
    }else if(beat.impacted&&beat.elapsed>=beat.duration-1e-8)d.active=null;
  }else if(!d.battle.finished&&(d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<.49)){
    d.simIdle+=elapsed*P.gameRate;
    while(d.simIdle>=STEP-1e-8&&!d.battle.finished&&
      (d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<.49)){
      d.simIdle=Math.max(0,d.simIdle-STEP);
      simulateStep(d);
      if(!d.queue.length)d.visible=structuredClone(d.battle);
    }
  }
  // Start, impact, and finish each get their own paint. The motor stays parked
  // while an active beat or its consequences are waiting to be displayed.
  if(!d.active&&d.queue.length&&!(d.queue.length===1&&d.queue[0].periodic&&!d.battle.finished&&d.battle.time-d.queue[0].before.time<.49)){
    d.active=d.queue.shift()!;d.serial++;
    d.visible=d.active.before;
    onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});
    return;
  }
  if(d.battle.finished&&!d.active&&!d.queue.length){d.visible=structuredClone(d.battle);d.complete=true;}
}
