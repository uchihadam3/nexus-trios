import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];before:Battle;after:Battle;duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean;periodic?:boolean;trace?:BeatTrace;
  /** Etapa do impacto já mostrada (0 = antes do impacto). Ver `etapaDoEvento`. */
  etapa?:number;
  /** As etapas que este beat tem, em ordem (1 golpe, 2 efeito no rival, 3 efeito no próprio trio). */
  etapas?:number[];
  /** Duração sem as etapas (o ritmo fixo da ação). */
  base?:number}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[]}
export interface PresentationCheckpoint {version?:2;battleTime:number;nextEvent:number;rng:number;visibleNextEvent:number;activeEventId:number|null;activeElapsed:number;impacted:boolean;serial:number;simIdle?:number}
export interface Cue {event:BattleEvent;family:Family;phase:'start'|'impact';grand:boolean}
export interface BeatTrace {eventId:number;kind:BattleEvent['kind'];duration:number;realStart:number;realImpact:number|null;realFinish:number|null;speed:number;queueLength:number;battleTime:number;source:string;haste:number;slow:number;rooted:number;shifts:{target:string;value:number}[]}
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
  if(event.kind==='tempo')return P.tempoSeconds;
  return grand?P.grandSeconds:event.kind==='skill'?P.skillSeconds:P.normalSeconds;
}
/*
 * Um efeito por vez.
 *
 * Pedido do jogador: quando uma habilidade bate, faz um Status ruim no rival e
 * um bom no próprio trio, tudo aparecia no mesmo instante e ficava difícil de
 * entender. O impacto agora se mostra em até três etapas:
 *   1 · o golpe — dano, bloqueio, interrupção, nocaute;
 *   2 · o efeito no rival — Status negativo, atraso;
 *   3 · o efeito no próprio trio — cura, Escudo, Status positivo, Carga.
 * Etapas vazias são puladas: um ataque simples continua com o mesmo ritmo.
 * O motor não muda nada — é só a ordem em que a tela revela o que já aconteceu.
 */
export const INTERVALO_DA_ETAPA=.34;
export function etapaDoEvento(beat:Pick<Beat,'event'|'after'>,e:BattleEvent):1|2|3{
  const lado=beat.after.fighters.find(f=>f.uid===beat.event.source)?.side;
  const alvo=beat.after.fighters.find(f=>f.uid===(e.target??e.source));
  const rival=!!alvo&&!!lado&&alvo.side!==lado;
  if(e.kind==='status'||e.kind==='tempo')return rival?2:3;
  if(e.kind==='heal'||e.kind==='shield'||e.kind==='charge'||e.kind==='synergy'||e.kind==='ready')return rival?1:3;
  return 1;
}
/** O evento já pode aparecer na tela? */
export function revelado(beat:Beat|null|undefined,e:BattleEvent):boolean{
  if(!beat?.impacted)return false;
  return etapaDoEvento(beat,e)<=(beat.etapa??3);
}
/* O que a tela mostra numa etapa: o estado de depois, com o que ainda não foi revelado voltando ao de antes. */
export function visivelNaEtapa(beat:Beat,etapa:number):Battle{
  const ultima=beat.etapas?.at(-1)??1;
  if(etapa>=ultima)return beat.after;
  const v=structuredClone(beat.after),lado=beat.after.fighters.find(f=>f.uid===beat.event.source)?.side;
  v.fighters.forEach((f,i)=>{
    const antes=beat.before.fighters[i];if(!antes)return;
    const rival=f.side!==lado;
    if(!rival&&etapa<3){f.hp=antes.hp;f.shields=structuredClone(antes.shields);f.statuses=structuredClone(antes.statuses);f.skills=f.skills.map((s,k)=>({...s,charge:antes.skills[k]?.charge??s.charge}));}
    if(rival&&etapa<2)f.statuses=structuredClone(antes.statuses);
  });
  return v;
}
/** A duração do golpe sem o tempo das etapas: o ritmo de cada ação continua fixo. */
export const duracaoBase=(beat:Beat)=>beat.base??beat.duration;
/** Em que etapa o impacto está, pelo tempo já passado do beat. */
function etapaNoTempo(beat:Beat):number{
  const etapas=beat.etapas??[1],impacto=duracaoBase(beat)*P.impactAt;
  let i=0;while(i<etapas.length-1&&beat.elapsed>=impacto+INTERVALO_DA_ETAPA*(i+1)-1e-8)i++;
  return etapas[i]!;
}
function etapasDe(beat:Beat):number[]{
  if(!['basic','skill'].includes(beat.event.kind))return [1];
  const presentes=new Set<number>(beat.events.map(e=>etapaDoEvento(beat,e)));presentes.add(1);
  return [1,2,3].filter(x=>presentes.has(x));
}

export function createDirection(battle:Battle):Direction {
  return {battle,visible:structuredClone(battle),queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[]};
}
function makeBeat(event:BattleEvent,events:BattleEvent[],before:Battle,after:Battle,periodic=false,previous=false):Beat {
  const actor=after.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  const auxiliary=event.kind==='ready'||event.kind==='status';
  const seconds=previous?(periodic?.55:auxiliary?.5:duration(event,grand)):periodic?P.periodicSeconds:duration(event,grand);
  const beat:Beat={event,events,before,after,duration:seconds,family:familyOf(event,after),grand,elapsed:0,impacted:false,periodic,etapa:0,base:seconds};
  beat.etapas=etapasDe(beat);
  beat.duration+=INTERVALO_DA_ETAPA*(beat.etapas.length-1);
  return beat;
}
function collect(d:Direction,events:BattleEvent[],before:Battle,after:Battle,legacy=false,previous=false){
  if(!events.length)return;
  // Every observer callback is a chronological boundary: one action and its
  // consequences, or periodic effects. Never merge across an action boundary.
  const principal=focus(events);
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    d.queue.push(makeBeat(principal,events,before,after));
    return;
  }
  if(principal&&!previous){d.queue.push(makeBeat(principal,events,before,after));return;}
  const change=events.find(e=>e.kind==='damage'||e.kind==='heal');
  if(change){
    const burning=change.kind==='damage'&&before.fighters.find(f=>f.uid===change.target)?.statuses.some(s=>s.id==='burning');
    const event={...change,label:burning?'Queimadura':change.kind==='heal'?'Regeneração':'Efeito contínuo',status:burning?'burning' as const:change.kind==='heal'?'regen' as const:undefined};
    const last=d.queue[d.queue.length-1];
    // One fixed window covers every affected fighter, without crossing an action.
    if(last?.periodic&&(previous?(last.event.source===event.source&&last.event.target===event.target&&last.event.kind===event.kind):true)&&
       !events.some(e=>e.kind==='ko'||e.kind==='interrupt'||e.kind==='turn')&&after.time-last.before.time<=(legacy?1.01:previous?.51:P.periodicWindowSeconds+.01)){
      last.events.push(...events);last.after=after;
      if(previous)last.event.value=(last.event.value??0)+(event.value??0);
    }else d.queue.push(makeBeat(event,events,before,after,true,previous));
    return;
  }
  if(previous){
    const important=events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='turn'||e.kind==='ready'||e.kind==='status'||e.kind==='shield');
    if(important)d.queue.push(makeBeat(important,events,before,after,legacy&&(important.kind==='ready'||important.kind==='status'),true));
    return;
  }
  // Charge, ready, and status feedback rides on the visible idle simulation.
  // A standalone tempo adjustment gets its own clear target indication.
  const tempo=events.find(e=>e.kind==='tempo');
  if(tempo)d.queue.push(makeBeat(tempo,events,before,after));
  else if(d.queue.at(-1)?.periodic){d.queue.at(-1)!.events.push(...events);d.queue.at(-1)!.after=after;}
  else d.signals.push(...events);
}
function simulateStep(d:Direction,legacy=false,previousMode=false){
  let previous=structuredClone(d.battle),lastId=d.battle.nextEvent-1;
  stepBattle(d.battle,current=>{
    const events=current.events.filter(e=>e.id>lastId);
    lastId=current.nextEvent-1;
    const after=structuredClone(current);
    collect(d,events,previous,after,legacy,previousMode);
    previous=after;
  });
  const last=d.queue[d.queue.length-1];
  if(!legacy&&last?.periodic&&d.battle.time-last.before.time<=(previousMode?.51:P.periodicWindowSeconds+.01))last.after=structuredClone(d.battle);
}
export function checkpointDirection(d:Direction):PresentationCheckpoint {
  return {version:2,battleTime:d.battle.time,nextEvent:d.battle.nextEvent,rng:d.battle.rng,visibleNextEvent:d.visible.nextEvent,activeEventId:d.active?.event.id??null,activeElapsed:d.active?.elapsed??0,impacted:d.active?.impacted??false,serial:d.serial,simIdle:d.simIdle};
}
/** Rebuilds the unseen visual timeline from deterministic combat after a reload. */
export function restoreDirection(initial:Battle,saved:Battle,checkpoint:PresentationCheckpoint):Direction|null {
  if(!checkpoint||checkpoint.battleTime!==saved.time||checkpoint.nextEvent!==saved.nextEvent||checkpoint.rng!==saved.rng)return null;
  const d=createDirection(initial);
  const legacy=checkpoint.simIdle===undefined;
  const previous=checkpoint.version!==2&&!legacy;
  while(!d.battle.finished&&d.battle.time+STEP/2<saved.time)simulateStep(d,legacy,previous);
  if(d.battle.time!==saved.time||d.battle.nextEvent!==saved.nextEvent||d.battle.rng!==saved.rng)return null;
  const index=checkpoint.activeEventId===null?-1:d.queue.findIndex(beat=>beat.event.id===checkpoint.activeEventId);
  if(checkpoint.activeEventId!==null&&index<0)return null;
  if(index>=0){
    d.active=d.queue[index];d.queue=d.queue.slice(index+1);
    d.active.elapsed=Math.min(d.active.duration,Math.max(0,checkpoint.activeElapsed));
    d.active.impacted=checkpoint.impacted;
    if(d.active.impacted)d.active.etapa=etapaNoTempo(d.active);
    d.visible=d.active.impacted?visivelNaEtapa(d.active,d.active.etapa!):d.active.before;
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
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void,visualSpeed=1,onTrace?:(trace:BeatTrace)=>void):void {
  // A delayed frame may not accumulate time to rush through unseen actions.
  const speed=visualSpeed===2?2:1;
  const elapsed=Math.min(P.renderIntervalMs/1000,Math.max(0,seconds))*speed;d.signals=[];
  if(d.complete||elapsed===0)return;
  if(d.active){
    const beat=d.active;
    const impacto=duracaoBase(beat)*P.impactAt;
    const limit=beat.impacted?beat.duration:impacto;
    beat.elapsed=Math.min(limit,beat.elapsed+elapsed);
    const etapas=beat.etapas??[1];
    if(!beat.impacted&&beat.elapsed>=limit-1e-8){
      beat.impacted=true;beat.etapa=etapas[0];
      if(beat.trace)beat.trace.realImpact=performance.now();
      d.visible=visivelNaEtapa(beat,beat.etapa!);
      d.signals.push(...beat.events.filter(e=>etapaDoEvento(beat,e)<=beat.etapa!));
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});
    }else if(beat.impacted&&(beat.etapa??3)<etapas.at(-1)!&&beat.elapsed>=impacto+INTERVALO_DA_ETAPA*(etapas.indexOf(beat.etapa!)+1)-1e-8){
      /* a próxima etapa do impacto: um efeito por vez */
      const anterior=beat.etapa!;beat.etapa=etapas[etapas.indexOf(anterior)+1];
      d.visible=visivelNaEtapa(beat,beat.etapa!);
      d.signals.push(...beat.events.filter(e=>{const x=etapaDoEvento(beat,e);return x>anterior&&x<=beat.etapa!;}));
    }else if(beat.impacted&&beat.elapsed>=beat.duration-1e-8){
      if(beat.trace){beat.trace.realFinish=performance.now();onTrace?.(beat.trace);}
      d.active=null;
      return;
    }
  }else if(!d.battle.finished&&(d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
    d.simIdle+=elapsed*P.gameRate;
    while(d.simIdle>=STEP-1e-8&&!d.battle.finished&&
      (d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
      d.simIdle=Math.max(0,d.simIdle-STEP);
      simulateStep(d);
      if(!d.queue.length)d.visible=structuredClone(d.battle);
    }
  }
  // Start, impact, and finish each get their own paint. The motor stays parked
  // while an active beat or its consequences are waiting to be displayed.
  if(!d.active&&d.queue.length&&!(d.queue.length===1&&d.queue[0].periodic&&!d.battle.finished&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
    d.active=d.queue.shift()!;d.serial++;
    if(onTrace){
      const fighter=d.active.before.fighters.find(f=>f.uid===d.active!.event.source);
      const intensity=(id:string)=>fighter?.statuses.find(s=>s.id===id)?.intensity??0;
      d.active.trace={eventId:d.active.event.id,kind:d.active.event.kind,duration:duracaoBase(d.active),realStart:performance.now(),realImpact:null,realFinish:null,speed,queueLength:d.queue.length,battleTime:d.active.before.time,source:d.active.event.source,haste:intensity('haste'),slow:intensity('slow'),rooted:intensity('rooted'),shifts:d.active.events.filter(e=>e.kind==='tempo').map(e=>({target:e.target??'',value:e.value??0}))};
    }
    d.visible=d.active.before;
    onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});
    return;
  }
  if(d.battle.finished&&!d.active&&!d.queue.length){d.visible=structuredClone(d.battle);d.complete=true;}
}
