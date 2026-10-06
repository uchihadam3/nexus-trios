import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];before:Battle;after:Battle;duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean;periodic?:boolean}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[];lastActionTime:number}
export interface PresentationCheckpoint {battleTime:number;nextEvent:number;rng:number;visibleNextEvent:number;activeEventId:number|null;activeElapsed:number;impacted:boolean;serial:number}
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
  return {battle,visible:structuredClone(battle),queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[],lastActionTime:-Infinity};
}
function makeBeat(event:BattleEvent,events:BattleEvent[],before:Battle,after:Battle,periodic=false,isolated=false):Beat {
  const actor=after.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  const auxiliary=event.kind==='ready'||event.kind==='status';
  const seconds=periodic?P.periodicSeconds:auxiliary?P.auxiliarySeconds:event.kind==='basic'&&!isolated?P.exchangeSeconds:duration(event,grand);
  return {event,events,before,after,duration:seconds,family:familyOf(event,after),grand,elapsed:0,impacted:false,periodic};
}
function collect(d:Direction,events:BattleEvent[],before:Battle,after:Battle){
  if(!events.length)return;
  // Every observer callback is a chronological boundary: one action and its
  // consequences, or one periodic tick. Never merge across an action boundary.
  const principal=focus(events);
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    const isolated=principal.time-d.lastActionTime>=P.isolatedActionGap;
    d.lastActionTime=principal.time;
    d.queue.push(makeBeat(principal,events,before,after,false,isolated));
    return;
  }
  const change=events.find(e=>e.kind==='damage'||e.kind==='heal');
  if(change){
    const burning=change.kind==='damage'&&before.fighters.find(f=>f.uid===change.target)?.statuses.some(s=>s.id==='burning');
    const event={...change,label:burning?'Queimadura':change.kind==='heal'?'Regeneração':'Efeito contínuo',status:burning?'burning' as const:change.kind==='heal'?'regen' as const:undefined};
    const last=d.queue[d.queue.length-1];
    // Adjacent periodic ticks may share an impact, but never swallow an action,
    // a knockout, or more than one second of mechanical time.
    if(last?.periodic&&!events.some(e=>e.kind==='ko'||e.kind==='interrupt'||e.kind==='turn')&&
       last.event.source===event.source&&last.event.target===event.target&&last.event.kind===event.kind&&
       after.time-last.before.time<=1.01){
      last.events.push(...events);last.after=after;
    }else d.queue.push(makeBeat(event,events,before,after,true));
    return;
  }
  const important=events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='turn'||e.kind==='ready'||e.kind==='status'||e.kind==='shield');
  if(important)d.queue.push(makeBeat(important,events,before,after,important.kind==='ready'||important.kind==='status'));
}
function simulateStep(d:Direction){
  let previous=structuredClone(d.battle),lastId=d.battle.nextEvent-1;
  stepBattle(d.battle,current=>{
    const events=current.events.filter(e=>e.id>lastId);
    lastId=current.nextEvent-1;
    const after=structuredClone(current);
    collect(d,events,previous,after);
    previous=after;
  });
}
export function checkpointDirection(d:Direction):PresentationCheckpoint {
  return {battleTime:d.battle.time,nextEvent:d.battle.nextEvent,rng:d.battle.rng,visibleNextEvent:d.visible.nextEvent,activeEventId:d.active?.event.id??null,activeElapsed:d.active?.elapsed??0,impacted:d.active?.impacted??false,serial:d.serial};
}
/** Rebuilds the unseen visual timeline from deterministic combat after a reload. */
export function restoreDirection(initial:Battle,saved:Battle,checkpoint:PresentationCheckpoint):Direction|null {
  if(!checkpoint||checkpoint.battleTime!==saved.time||checkpoint.nextEvent!==saved.nextEvent||checkpoint.rng!==saved.rng)return null;
  const d=createDirection(initial);
  while(!d.battle.finished&&d.battle.time+STEP/2<saved.time)simulateStep(d);
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
    d.visible=completed?d.queue[completed-1].after:structuredClone(initial);
    d.queue=d.queue.slice(completed);
  }
  if(d.visible.nextEvent!==checkpoint.visibleNextEvent)return null;
  d.battle=saved;d.serial=checkpoint.serial;d.complete=saved.finished&&!d.active&&!d.queue.length;
  return d;
}
/** The engine advances on real time; visualSpeed changes only animations. */
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void,visualSpeed=1):void {
  const elapsed=Math.max(0,seconds);d.signals=[];
  if(!d.battle.finished){
    d.simIdle+=elapsed*P.gameRate;
    while(d.simIdle>=STEP-1e-8&&!d.battle.finished){
      d.simIdle=Math.max(0,d.simIdle-STEP);
      simulateStep(d);
    }
  }
  // React paints once per caller update. Crossing two boundaries here would
  // play cues for a strike whose anticipation or impact was never drawn.
  if(!d.active&&d.queue.length){
    d.active=d.queue.shift()!;d.serial++;
    d.visible=d.active.before;
    onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});
  }else if(d.active&&elapsed>0){
    const beat=d.active,limit=beat.impacted?beat.duration:beat.duration*P.impactAt;
    beat.elapsed=Math.min(limit,beat.elapsed+elapsed*Math.max(1,visualSpeed));
    if(!beat.impacted&&beat.elapsed>=limit-1e-8){
      beat.impacted=true;
      d.visible=beat.after;
      d.signals.push(...beat.events);
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});
    }else if(beat.impacted&&beat.elapsed>=beat.duration-1e-8)d.active=null;
  }
  if(!d.active&&!d.queue.length)d.visible=structuredClone(d.battle);
  if(d.battle.finished&&!d.active&&!d.queue.length)d.complete=true;
}
