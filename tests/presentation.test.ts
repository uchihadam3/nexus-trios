import { describe,it,expect } from 'vitest';
import { createBattle,simulate,applyEffects,updateDominion } from '../src/engine/battle';
import { createDirection,restoreDirection,checkpointDirection,advanceDirection,type Direction,type Beat } from '../src/presentation/director';
import { isAreaBeat } from '../src/components/BattleEffects';
import { PRESENTATION as P } from '../src/presentation/config';
import { DOMINION as D } from '../src/engine/dominion-config';
import { describeSkill,describeSkillUse } from '../src/engine/skill-descriptions';
import { byId } from '../src/data/characters';
import type { BattleEvent } from '../src/engine/types';
const a=['goku','pikachu','captain'],b=['vegeta','raven','hulk'];
function watch(d:Direction,speed=1,drain=true){
 let frames=0,mechanicalFinish=-1,maxQueue=0;
 while(!(drain?d.complete:d.battle.finished)&&frames<50000){
  advanceDirection(d,.04,undefined,speed);frames++;
  maxQueue=Math.max(maxQueue,d.queue.length);
  if(d.battle.finished&&mechanicalFinish<0)mechanicalFinish=frames*.04;
 }
 expect(drain?d.complete:d.battle.finished).toBe(true);
 return {wall:frames*.04,mechanicalFinish,maxQueue};
}
describe('Direção sem alterar regras',()=>{
 it('explica a regra real da habilidade, incluindo alvo, números, carga e preparação',()=>{
  const expansion=byId.gojo.skills[2];
  expect(describeSkill(expansion)).toContain('todos os inimigos');
  /* O número vem do dado, não do teste: a calibragem pode mudá-lo. */
  const dano=expansion.effects.find(e=>e.kind==='damage');
  expect(dano&&'value' in dano).toBe(true);
  expect(describeSkill(expansion)).toContain(String(dano&&'value' in dano?dano.value:''));
  expect(describeSkillUse(expansion)).toContain('+3,4% por segundo');
  expect(describeSkillUse(expansion)).toContain('Preparo: 5 s');
  expect(describeSkillUse(expansion)).toContain('Resfriamento: 14 s');
 });
 it('separa estado mecânico e visível em snapshots causais',()=>{
  const battle=createBattle(a,b,42),d=createDirection(battle);
  expect(d.visible).not.toBe(battle);
  expect(d.visible).toEqual(battle);
  expect(P.gameRate).toBe(.86);
  advanceDirection(d,1);
  expect(d.visible).not.toBe(d.battle);
  expect(d.battle.time).toBeLessThanOrEqual(.3);
  expect([...d.queue,...(d.active?[d.active]:[])].every(beat=>beat.before&&beat.after)).toBe(true);
 });
 it('1× e 2× preservam o mesmo combate; só 2× acelera a cadência',()=>{
  const one=createDirection(createBattle(a,b,42)),two=createDirection(createBattle(a,b,42));
  const oneEnd=watch(one,1),twoEnd=watch(two,2);
  expect(two.battle).toEqual(one.battle);
  expect(one.battle).toEqual(simulate(a,b,42));
  expect(twoEnd.wall).toBeLessThan(oneEnd.wall*.6);
 },15000);
 it('registra duração e contexto sem alterar duração por fila, haste ou tempo mecânico',()=>{
  const d=createDirection(createBattle(['sakura','rukia','scarletwitch'],['ironman','inosuke','mikasa'],8));
  const traces:import('../src/presentation/director').BeatTrace[]=[];
  for(let frame=0;frame<20000&&!d.complete;frame++)advanceDirection(d,.04,undefined,1,trace=>traces.push(trace));
  expect(d.complete).toBe(true);
  expect(traces.length).toBeGreaterThan(20);
  expect(traces.some(trace=>trace.shifts.length>0)).toBe(true);
  for(const trace of traces){
   expect(trace.realImpact).not.toBe(null);expect(trace.realFinish).not.toBe(null);
   expect(trace.speed).toBe(1);expect(trace.queueLength).toBeLessThanOrEqual(6);
   if(trace.kind==='basic')expect(trace.duration).toBe(P.normalSeconds);
   if(trace.kind==='skill')expect([P.skillSeconds,P.grandSeconds]).toContain(trace.duration);
  }
 });
 it('HP, KO, carga e escudo visíveis só mudam no impacto causal',()=>{
  const d=createDirection(createBattle(['wolverine','pikachu','captain'],b,11));
  let lastTime=0,checkedHp=0,checkedKo=0,checkedCharge=0;
  for(let frame=0;frame<20000&&!d.complete;frame++){
   advanceDirection(d,.04,cue=>{
    const beat=d.active!;
    if(cue.phase==='start'){
     expect(d.visible).toEqual(beat.before);
     expect(beat.before.time).toBeGreaterThanOrEqual(lastTime-1e-6);
     for(let i=0;i<6;i++)if(beat.before.fighters[i].hp!==beat.after.fighters[i].hp){
      expect(d.visible.fighters[i].hp).toBe(beat.before.fighters[i].hp);checkedHp++;
      if(beat.after.fighters[i].hp===0){expect(d.visible.fighters[i].hp).toBeGreaterThan(0);checkedKo++;}
     }
    }else{
     expect(d.visible).toEqual(beat.after);
     if(beat.events.some(e=>e.kind==='ready'||e.kind==='charge'))checkedCharge++;
    }
   },frame%200<100?1:2);
   expect(d.visible.time).toBeGreaterThanOrEqual(lastTime-1e-6);
   lastTime=d.visible.time;
  }
  expect(d.complete).toBe(true);
  expect(checkedHp).toBeGreaterThan(0);
  expect(checkedKo).toBeGreaterThan(0);
  expect(checkedCharge).toBeGreaterThan(0);
 });
 it('não descarta básicos nem skills e preserva ordem das consequências',()=>{
  const d=createDirection(createBattle(a,b,42)),starts:Beat[]=[],impacts:number[]=[],actions:number[]=[];
  let lastId=0;
  for(let frame=0;frame<20000&&!d.complete;frame++){
   advanceDirection(d,.04,cue=>{
    if(cue.phase==='start')starts.push({...d.active!,events:[...d.active!.events]});
    else impacts.push(cue.event.id);
   },frame%100<50?1:2);
   const fresh=d.battle.events.filter(e=>e.id>lastId);
   actions.push(...fresh.filter(e=>e.kind==='basic'||e.kind==='skill'||e.kind==='cast').map(e=>e.id));
   lastId=d.battle.nextEvent-1;
  }
  const ids=starts.map(beat=>beat.event.id);
  expect(starts.filter(beat=>['basic','skill','cast'].includes(beat.event.kind)).map(beat=>beat.event.id)).toEqual(actions);
  expect(new Set(ids).size).toBe(ids.length);
  expect(ids).toEqual([...ids].sort((x,y)=>x-y));
  expect(new Set(impacts).size).toBe(impacts.length);
  expect(impacts).toEqual(ids);
  for(const beat of starts){
   expect(beat.events.map(e=>e.id)).toEqual([...beat.events.map(e=>e.id)].sort((x,y)=>x-y));
   expect(beat.events.filter(e=>['basic','skill','cast'].includes(e.kind))).toHaveLength(['basic','skill','cast'].includes(beat.event.kind)?1:0);
   if(beat.events.some(e=>e.kind==='ko'))expect(beat.after.fighters.some((f,i)=>f.hp===0&&beat.before.fighters[i].hp>0)).toBe(true);
  }
 });
 it('densidade de ações, skills e efeitos não altera a velocidade de cada beat',()=>{
  const battle=createBattle(a,b,42);
  for(const fighter of battle.fighters)fighter.action=.96;
  battle.fighters[0].statuses.push({id:'regen',remaining:4,intensity:12,source:battle.fighters[0].uid});
  battle.fighters[3].statuses.push({id:'burning',remaining:4,intensity:12,source:battle.fighters[0].uid});
  battle.fighters[1].shields.push({amount:100,remaining:4,source:battle.fighters[1].uid});
  battle.fighters[2].skills[0].charge=99;
  battle.fighters[4].skills[0].charge=99;
  const d=createDirection(battle),basics:Beat[]=[],skills:Beat[]=[],periodic:Beat[]=[];
  let maxQueue=0,checkedActive=0;
  for(let frame=0;frame<25000&&!d.complete;frame++){
   const active=d.active,mechanicalTime=d.battle.time,elapsed=active?.elapsed;
   advanceDirection(d,.04,cue=>{
    if(cue.phase!=='start')return;
    const beat=d.active!;
    if(beat.event.kind==='basic')basics.push(beat);
    if(beat.event.kind==='skill')skills.push(beat);
    if(beat.periodic)periodic.push(beat);
   });
   maxQueue=Math.max(maxQueue,d.queue.length);
   if(active){
    expect(d.battle.time).toBe(mechanicalTime);
    expect(active.elapsed-elapsed!).toBeLessThanOrEqual(.040001);
    checkedActive++;
   }
  }
  expect(d.complete).toBe(true);
  expect(maxQueue).toBeGreaterThan(0);
  expect(maxQueue).toBeLessThanOrEqual(6);
  expect(checkedActive).toBeGreaterThan(100);
  expect(basics.length).toBeGreaterThan(3);
  expect(skills.length).toBeGreaterThan(1);
  expect(periodic.length).toBeGreaterThan(0);
  expect(new Set(basics.map(beat=>beat.duration))).toEqual(new Set([P.normalSeconds]));
  expect(new Set(skills.map(beat=>beat.duration))).toEqual(new Set([P.skillSeconds,P.grandSeconds].filter(value=>skills.some(beat=>beat.duration===value))));
  expect(periodic.every(beat=>beat.duration>=P.periodicSeconds)).toBe(true);
 });
 it('agrega dano e cura periódicos de alvos distintos sem criar turnos de pronta/status',()=>{
  const battle=createBattle(a,b,15),[healer,ally,,,enemy]=battle.fighters;
  ally.hp-=100;
  ally.statuses.push({id:'regen',remaining:3,intensity:10,source:healer.uid});
  enemy.statuses.push({id:'burning',remaining:3,intensity:10,source:healer.uid});
  const d=createDirection(battle),beats:Beat[]=[];
  for(let frame=0;frame<1300&&!d.complete;frame++)advanceDirection(d,.04,cue=>{if(cue.phase==='start')beats.push(d.active!);});
  expect(beats.some(beat=>beat.periodic&&new Set(beat.events.filter(e=>e.kind==='damage'||e.kind==='heal').map(e=>e.target)).size>1)).toBe(true);
  expect(beats.some(beat=>beat.event.kind==='ready'||beat.event.kind==='status')).toBe(false);
  expect(beats.filter(beat=>beat.periodic).every(beat=>beat.duration===P.periodicSeconds)).toBe(true);
 });
 it('atrasos de frame não provocam catch-up e preservam eventos e RNG',()=>{
  const steady=createDirection(createBattle(a,b,42)),delayed=createDirection(createBattle(a,b,42));
  for(let i=0;i<120;i++)advanceDirection(steady,.04);
  for(let i=0;i<120;i++)advanceDirection(delayed,1);
  expect(delayed.battle).toEqual(steady.battle);
  expect(delayed.active?.elapsed).toBe(steady.active?.elapsed);
  watch(steady);watch(delayed);
  expect(delayed.battle).toEqual(steady.battle);
  expect(delayed.visible).toEqual(delayed.battle);
  expect(steady.visible).toEqual(steady.battle);
 });
 it('cada quadro desenha início e impacto antes de avançar para outra ação',()=>{
  const d=createDirection(createBattle(a,b,42));
  let starts=0,impacts=0,previousId=0,finishes=0;
  for(let frame=0;frame<20000&&!d.complete;frame++){
    const cues:('start'|'impact')[]=[];
    const seconds=frame%5===0?1:.04;
    const finishing=d.active?.impacted&&d.active.elapsed+Math.min(P.renderIntervalMs/1000,seconds)*2>=d.active.duration-1e-8;
    advanceDirection(d,seconds,cue=>{
    cues.push(cue.phase);
    if(cue.phase==='start'){
     expect(starts).toBe(impacts);
     expect(cue.event.id).toBeGreaterThan(previousId);
     previousId=cue.event.id;starts++;
     expect(d.visible).toEqual(d.active!.before);
    }else{
     expect(starts).toBe(impacts+1);impacts++;
     expect(d.visible).toEqual(d.active!.after);
    }
   },2);
   if(finishing){expect(d.active).toBe(null);finishes++;}
   expect(cues.length).toBeLessThanOrEqual(1);
  }
  expect(d.complete).toBe(true);
  expect(starts).toBe(impacts);
  expect(starts).toBeGreaterThan(50);
  expect(finishes).toBeGreaterThan(50);
 });
 it('atualizar a página retoma a fila e o HP visível no mesmo Beat causal',()=>{
  for(const phase of ['before','after'] as const){
   const d=createDirection(createBattle(a,b,42));
   for(let frame=0;frame<2000&&!d.active;frame++)advanceDirection(d,.04);
   if(phase==='after')while(d.active&&!d.active.impacted)advanceDirection(d,.04);
   else while(d.active&&d.active.impacted)advanceDirection(d,.04);
   expect(d.active).not.toBe(null);
   const saved=JSON.parse(JSON.stringify(d.battle));
   const checkpoint=JSON.parse(JSON.stringify(checkpointDirection(d)));
   const resumed=restoreDirection(createBattle(a,b,42),saved,checkpoint);
   expect(resumed).not.toBe(null);
   expect(resumed!.visible).toEqual(d.visible);
   expect(resumed!.active?.event.id).toBe(d.active?.event.id);
   expect(resumed!.active?.elapsed).toBe(d.active?.elapsed);
   expect(resumed!.queue.map(beat=>beat.event.id)).toEqual(d.queue.map(beat=>beat.event.id));
   while(!d.complete){advanceDirection(d,.04);advanceDirection(resumed!,.04);}
   expect(resumed!.complete).toBe(true);
   expect(resumed!.battle).toEqual(d.battle);
   expect(resumed!.visible).toEqual(d.visible);
  }
 },15000);
 it('retoma um checkpoint anterior à mudança de cadência sem mostrar HP futuro',()=>{
  const initial=createBattle(a,b,42),d=createDirection(structuredClone(initial));
  while(!d.active||d.active.event.kind!=='basic')advanceDirection(d,.04);
  const saved=structuredClone(d.battle),checkpoint=checkpointDirection(d);
  const previousFormat={...checkpoint,simIdle:undefined};
  const resumed=restoreDirection(initial,saved,previousFormat);
  expect(resumed).not.toBe(null);
  expect(resumed!.visible.fighters.map(f=>f.hp)).toEqual(d.visible.fighters.map(f=>f.hp));
  expect(resumed!.active?.duration).toBe(P.normalSeconds);
 });
 it('reconstrói uma batalha salva na cadência anterior',()=>{
  const initial=createBattle(a,b,42),d=createDirection(structuredClone(initial));
  while(!d.active||d.active.event.kind!=='basic')advanceDirection(d,.04);
  const checkpoint={...checkpointDirection(d),version:undefined};
  const resumed=restoreDirection(initial,structuredClone(d.battle),checkpoint);
  expect(resumed?.active?.event.id).toBe(d.active.event.id);
  expect(resumed?.visible.fighters.map(f=>f.hp)).toEqual(d.visible.fighters.map(f=>f.hp));
 });
 it('VFX de alvo único não herda alvos de outro evento; área real continua área',()=>{
  const battle=createBattle(['goku','thor','captain'],b,4);
  const single:BattleEvent={id:1,time:1,kind:'skill',source:'player-0',target:'enemy-0',skill:0,label:'Kamehameha',visual:'beam'};
  const damage=(id:number,source:string,target:string):BattleEvent=>({id,time:1,kind:'damage',source,target,label:'Impacto',value:30});
  const beat=(event:BattleEvent,events:BattleEvent[]):Beat=>({event,events,before:battle,after:battle,duration:1,family:'energy',grand:false,elapsed:0,impacted:false});
  expect(isAreaBeat(beat(single,[single,damage(2,'player-0','enemy-0'),damage(3,'enemy-1','enemy-2')]),battle)).toBe(false);
  expect(isAreaBeat(beat(single,[single,damage(2,'player-0','enemy-0'),damage(3,'player-0','enemy-1')]),battle)).toBe(true);
  const area={...single,id:4,source:'player-1',skill:1};
  expect(isAreaBeat(beat(area,[area]),battle)).toBe(true);
 });
 it('pausa sem avanço da simulação ou da apresentação',()=>{
  const d=createDirection(createBattle(a,b,8)),before=structuredClone(d.battle);
  advanceDirection(d,0,undefined,2);
  expect(d.battle).toEqual(before);
  expect(d.active).toBe(null);
 });
 it('emite pronta também quando carga direta de aliado completa uma habilidade',()=>{const battle=createBattle(a,b,9),target=battle.fighters[1];target.skills[0].charge=95;applyEffects(battle,battle.fighters[0],[target],[{kind:'charge',value:10}]);expect(target.skills[0].charge).toBe(100);expect(battle.events.find(e=>e.kind==='ready')).toMatchObject({source:target.uid,skill:0});});
 it('informa a origem real de um bloqueio e a habilidade beneficiada por sinergia',()=>{const battle=createBattle(['light','pikachu','wolverine'],b,9),[light,pika,wolverine,attacker]=battle.fighters;applyEffects(battle,wolverine,[light],[{kind:'shield',value:100}]);applyEffects(battle,attacker,[light],[{kind:'damage',value:60}]);expect(battle.events.find(e=>e.kind==='block')).toMatchObject({source:wolverine.uid,target:light.uid,attacker:attacker.uid,value:60});applyEffects(battle,pika,[attacker],[{kind:'status',status:'paralyzed',value:1,duration:2}]);expect(battle.events.find(e=>e.kind==='synergy'&&e.target===light.uid)).toHaveProperty('skill');});
 it('dá impulso por incapacitação, mas conserva memória e inércia do Domínio',()=>{const battle=createBattle(['pikachu','light','wolverine'],b,10),enemy=battle.fighters[3];battle.dominion=60;battle.lastLead='player';applyEffects(battle,enemy,[battle.fighters[0]],[{kind:'damage',value:1000}]);expect(battle.fighters[0].hp).toBe(0);expect(battle.momentum).toBeLessThan(-D.event.knockout);updateDominion(battle);expect(battle.dominion).toBeGreaterThan(0);for(let i=0;i<80;i++)updateDominion(battle);expect(battle.dominion).toBeLessThan(0);});
 it('não pontua cura desperdiçada nem escudo ainda não usado',()=>{const battle=createBattle(['wolverine','captain','light'],b,11),[wolverine,captain,light]=battle.fighters;applyEffects(battle,wolverine,[wolverine],[{kind:'heal',value:200}]);applyEffects(battle,captain,[light],[{kind:'shield',value:200}]);expect(battle.momentum).toBe(0);light.hp-=150;applyEffects(battle,wolverine,[light],[{kind:'heal',value:100}]);expect(battle.momentum).toBeGreaterThan(0);});
});
