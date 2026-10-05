import { describe,it,expect } from 'vitest';
import { createBattle,simulate,applyEffects,updateDominion } from '../src/engine/battle';
import { createDirection,advanceDirection,type Direction,type Beat } from '../src/presentation/director';
import { isAreaBeat } from '../src/components/BattleEffects';
import { PRESENTATION as P } from '../src/presentation/config';
import { DOMINION as D } from '../src/engine/dominion-config';
import type { BattleEvent } from '../src/engine/types';
const a=['goku','pikachu','captain'],b=['vegeta','raven','hulk'];
function watch(d:Direction,speed=1){
 let frames=0,mechanicalFinish=-1,maxQueue=0;
 while(!d.complete&&frames<6000){
  advanceDirection(d,.04,undefined,speed);frames++;
  maxQueue=Math.max(maxQueue,d.queue.length);
  if(d.battle.finished&&mechanicalFinish<0)mechanicalFinish=frames*.04;
 }
 expect(d.complete).toBe(true);
 return {wall:frames*.04,mechanicalFinish,maxQueue};
}
describe('Direção sem alterar regras',()=>{
 it('mantém um único estado mecânico e uma fila de eventos',()=>{
  const battle=createBattle(a,b,42),d=createDirection(battle);
  expect(d.visible).toBe(battle);
  expect(P.gameRate).toBe(1);
  advanceDirection(d,1);
  expect(d.visible).toBe(d.battle);
  expect(d.battle.time).toBeCloseTo(1,6);
  expect(d.queue.every(beat=>!('before' in beat)&&!('after' in beat))).toBe(true);
 });
 it('1× e 2× mostram o mesmo combate mecânico em cada instante real',()=>{
  const one=createDirection(createBattle(a,b,42)),two=createDirection(createBattle(a,b,42));
  for(let frame=0;frame<300&&!one.battle.finished&&!two.battle.finished;frame++){
   advanceDirection(one,.04,undefined,1);
   advanceDirection(two,.04,undefined,2);
   expect(two.battle).toEqual(one.battle);
   expect(one.visible).toBe(one.battle);
   expect(two.visible).toBe(two.battle);
  }
  const oneEnd=watch(one,1),twoEnd=watch(two,2);
  expect(two.battle).toEqual(one.battle);
  expect(one.battle).toEqual(simulate(a,b,42));
  expect(oneEnd.mechanicalFinish).toBeCloseTo(twoEnd.mechanicalFinish,2);
 });
 it('120 segundos mecânicos duram aproximadamente 120 segundos reais em ambas velocidades',()=>{
  const make=()=>{
   const battle=createBattle(a,b,8);
   for(const f of battle.fighters){f.maxHp=1e8;f.hp=f.side==='enemy'?8e7:1e8;}
   return createDirection(battle);
  };
  const one=make(),two=make(),duration1=watch(one,1),duration2=watch(two,2);
  expect(one.battle.time).toBe(120);
  expect(two.battle).toEqual(one.battle);
  expect(duration1.mechanicalFinish).toBeGreaterThanOrEqual(119.9);
  expect(duration1.mechanicalFinish).toBeLessThanOrEqual(120.1);
  expect(duration2.mechanicalFinish).toBeGreaterThanOrEqual(119.9);
  expect(duration2.mechanicalFinish).toBeLessThanOrEqual(120.1);
 });
 it('tempo, HP e carga seguem eventos mecânicos sem snapshots reversos',()=>{
  const d=createDirection(createBattle(['wolverine','pikachu','captain'],b,11));
  let lastTime=0,lastHp=d.battle.fighters.map(f=>f.hp),lastCharges=d.battle.fighters.map(f=>f.skills.map(s=>s.charge));
  for(let frame=0;frame<5000&&!d.complete;frame++){
   advanceDirection(d,.04,undefined,frame%200<100?1:2);
   expect(d.visible).toBe(d.battle);
   expect(d.visible.time).toBeGreaterThanOrEqual(lastTime);
   for(let i=0;i<d.battle.fighters.length;i++){
    const fighter=d.battle.fighters[i],hpDelta=fighter.hp-lastHp[i];
    const healing=d.signals.filter(e=>e.kind==='heal'&&e.target===fighter.uid).reduce((n,e)=>n+(e.value??0),0);
    if(hpDelta>1e-5)expect(healing).toBeGreaterThanOrEqual(hpDelta-1e-5);
    for(let skill=0;skill<3;skill++)if(fighter.skills[skill].charge<lastCharges[i][skill]-1e-5){
     expect(d.signals.some(e=>e.kind==='skill'&&e.source===fighter.uid&&e.skill===skill||e.kind==='interrupt'&&e.target===fighter.uid)).toBe(true);
    }
   }
   lastTime=d.visible.time;lastHp=d.battle.fighters.map(f=>f.hp);lastCharges=d.battle.fighters.map(f=>f.skills.map(s=>s.charge));
  }
  expect(d.complete).toBe(true);
 });
 it('apresenta cada evento importante uma vez e mantém cada Beat em sua própria ação',()=>{
  const d=createDirection(createBattle(a,b,42)),starts:Beat[]=[],impacts:number[]=[];
  for(let frame=0;frame<5000&&!d.complete;frame++)advanceDirection(d,.04,cue=>{
   if(cue.phase==='start')starts.push({...d.active!,events:[...d.active!.events]});
   else impacts.push(cue.event.id);
  },frame%100<50?1:2);
  const ids=starts.map(beat=>beat.event.id);
  expect(new Set(ids).size).toBe(ids.length);
  expect(new Set(impacts).size).toBe(impacts.length);
  expect(impacts).toEqual(ids);
  for(const beat of starts){
   expect(beat.events.every(e=>e.time===beat.event.time&&e.id>=beat.event.id)).toBe(true);
   expect(beat.events.filter(e=>['basic','skill','cast'].includes(e.kind))).toHaveLength(['basic','skill','cast'].includes(beat.event.kind)?1:0);
  }
 });
 it('VFX de alvo único não herda alvos de outro evento; área real continua área',()=>{
  const battle=createBattle(['goku','thor','captain'],b,4);
  const single:BattleEvent={id:1,time:1,kind:'skill',source:'player-0',target:'enemy-0',skill:0,label:'Kamehameha',visual:'beam'};
  const damage=(id:number,source:string,target:string):BattleEvent=>({id,time:1,kind:'damage',source,target,label:'Impacto',value:30});
  const beat=(event:BattleEvent,events:BattleEvent[]):Beat=>({event,events,duration:1,family:'energy',grand:false,elapsed:0,impacted:false});
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
