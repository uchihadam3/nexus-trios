import { describe,expect,it } from 'vitest';
import { createBattle,simulate } from '../src/engine/battle';
import { addSynergies,summarizeBattle,summarizeRun } from '../src/engine/run-summary';

describe('conclusão da jornada',()=>{
 it('guarda dez confrontos, contribuições e a ligação mais recorrente',()=>{
  const player=['goku','pikachu','captain'],enemy=['vegeta','raven','hulk'];
  const battle=simulate(player,enemy,42);
  const events=[{id:1,time:1,kind:'synergy' as const,source:'player-0',target:'player-1',label:'Ajuda',value:15}];
  const synergy=addSynergies(addSynergies([],events),events);
  const summaries=Array.from({length:10},(_,index)=>summarizeBattle(index,battle,synergy));
  const result=summarizeRun(summaries);
  expect(result.battles.map(b=>b.index)).toEqual([0,1,2,3,4,5,6,7,8,9]);
  expect(result.topSynergy).toMatchObject({source:'player-0',target:'player-1',count:20,charge:300});
  expect(result.damage).toBeCloseTo(battle.fighters.filter(f=>f.side==='player').reduce((n,f)=>n+f.stats.damage,0)*10);
  expect(result.score).toBe(summaries.reduce((n,b)=>n+b.score,0));
  expect(result.rank).toBe(result.won===10?'S':result.won>=7?'A':result.won>=4?'B':'C');
 });
 it('calcula resultado da batalha sem depender do log circular de eventos',()=>{
  const battle=createBattle(['goku','pikachu','captain'],['vegeta','raven','hulk'],9);
  battle.winner='player';battle.finished=true;battle.reason='Incapacitação';battle.time=49;
  battle.fighters[0].stats.damage=700;
  battle.events=[];
  const summary=summarizeBattle(3,battle);
  expect(summary).toMatchObject({index:3,won:true,time:49,score:expect.any(Number),survivors:3});
  expect(summary.fighters[0].damage).toBe(700);
  expect(summary.enemies).toEqual(['vegeta','raven','hulk']);
 });
});
