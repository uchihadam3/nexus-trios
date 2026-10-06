import type { Battle, BattleEvent, Fighter } from './types';

export interface RunSynergyEvent {source:string;target:string;count:number;charge:number}
export interface RunBattleSummary {
  index:number;won:boolean;time:number;reason:string;score:number;survivors:number;turns:number;
  enemies:string[];fighters:{characterId:string;damage:number;healing:number;protection:number;interrupts:number;kills:number;hp:number}[];
  synergies:RunSynergyEvent[];
}
export interface RunSummary {battles:RunBattleSummary[];won:number;score:number;rank:'S'|'A'|'B'|'C';survivors:number;damage:number;healing:number;protection:number;interrupts:number;kills:number;topSynergy:RunSynergyEvent|null;lessons:string[]}

export function addSynergies(existing:RunSynergyEvent[],events:BattleEvent[]):RunSynergyEvent[]{
  const next=existing.map(item=>({...item}));
  for(const event of events){
    if(event.kind!=='synergy'||!event.source.startsWith('player-')||!event.target?.startsWith('player-'))continue;
    let item=next.find(x=>x.source===event.source&&x.target===event.target);
    if(!item){item={source:event.source,target:event.target,count:0,charge:0};next.push(item);}
    item.count++;item.charge+=event.value??0;
  }
  return next;
}
export function summarizeBattle(index:number,battle:Battle,synergies:RunSynergyEvent[]=[]):RunBattleSummary {
  const players=battle.fighters.filter(f=>f.side==='player'),enemies=battle.fighters.filter(f=>f.side==='enemy');
  const survivors=players.filter(f=>f.hp>0).length;
  const remaining=players.reduce((sum,f)=>sum+f.hp/f.maxHp,0)/3;
  const score=(battle.winner==='player'?1000:0)+survivors*120+Math.round(remaining*240)+Math.round(Math.max(0,battle.dominion)*2);
  const fighters=players.map((f:Fighter)=>({characterId:f.characterId,...f.stats,hp:Math.round(f.hp)}));
  return {index,won:battle.winner==='player',time:battle.time,reason:battle.reason,score,survivors,turns:battle.turns,enemies:enemies.map(f=>f.characterId),fighters,synergies:synergies.map(x=>({...x}))};
}
export function summarizeRun(battles:RunBattleSummary[]):RunSummary {
  const won=battles.filter(b=>b.won).length,score=battles.reduce((n,b)=>n+b.score,0);
  const totals={damage:0,healing:0,protection:0,interrupts:0,kills:0};
  const connections=new Map<string,RunSynergyEvent>();
  for(const battle of battles){
    for(const fighter of battle.fighters)for(const key of Object.keys(totals) as (keyof typeof totals)[])totals[key]+=fighter[key];
    for(const pair of battle.synergies){const key=`${pair.source}:${pair.target}`,item=connections.get(key)??{source:pair.source,target:pair.target,count:0,charge:0};item.count+=pair.count;item.charge+=pair.charge;connections.set(key,item);}
  }
  const topSynergy=[...connections.values()].sort((a,b)=>b.count-a.count||b.charge-a.charge)[0]??null;
  const lessons:string[]=[];
  if(topSynergy)lessons.push(`A ligação mais frequente ajudou um aliado ${topSynergy.count} vezes.`);
  if(totals.healing>totals.protection)lessons.push('A cura sustentou o trio mais que os bloqueios.');
  else if(totals.protection>0)lessons.push('Os bloqueios sustentaram o trio mais que a cura.');
  if(totals.interrupts>0)lessons.push(`${totals.interrupts} preparações rivais foram interrompidas ou atrasadas.`);
  if(!lessons.length)lessons.push('Experimente combinar proteção, controle e dano em uma próxima jornada.');
  const rank=won===10?'S':won>=7?'A':won>=4?'B':'C';
  return {battles,won,score,rank,survivors:battles.at(-1)?.survivors??0,...totals,topSynergy,lessons};
}
