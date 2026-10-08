import {characters} from '../data/characters';
import {createBattle,stepBattle} from './battle';
import {generateCampaign} from './campaign';
import {emptyTally,tallyEvents} from './progression';
import {summarizeBattle,type RunBattleSummary} from './run-summary';

/* 250.4: Preparo mínimo de 0,5 s (leve), efeitos repetidos somados, condições alcançáveis. */
export const ENGINE_VERSION='nexus-250.4';
export const BALANCE_VERSION='season-1';
export const rosterFingerprint=()=>{
  const data=characters.map(c=>[c.id,c.hp,c.interval,c.basic,c.trait,c.skills]);
  let hash=2166136261;const raw=JSON.stringify(data);
  for(let i=0;i<raw.length;i++){hash^=raw.charCodeAt(i);hash=Math.imul(hash,16777619);}
  return `fnv1a-${(hash>>>0).toString(16).padStart(8,'0')}`;
};
export async function runDigest(id:string,team:string[],seed:number,outcomes:boolean[]):Promise<string>{
  const raw=JSON.stringify({id,team,seed,outcomes});
  const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(raw));
  return [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
export function replayRanked(team:string[],seed:number){
  if(team.length!==3||new Set(team).size!==3||team.some(id=>!characters.some(c=>c.id===id)))throw new Error('Trio inválido.');
  const encounters=generateCampaign(seed);
  const foes=new Set(encounters.flatMap(e=>e.team));if(team.some(id=>foes.has(id)))throw new Error('Trio inclui rival da campanha compartilhada.');
  let quality=0;
  const summaries:RunBattleSummary[]=[];
  for(const [index,encounter] of encounters.entries()){
    const battle=createBattle(team,encounter.team,seed+index*7919,encounter.scale);
    let tally=emptyTally();
    for(let tick=0;tick<9000&&!battle.finished;tick++){stepBattle(battle);tally=tallyEvents(tally,battle.events);}
    if(!battle.finished)throw new Error(`Replay sem conclusão no confronto ${index+1}.`);
    const summary=summarizeBattle(index,battle);summaries.push(summary);
    if(summary.won){
      const health=battle.fighters.filter(f=>f.side==='player').reduce((n,f)=>n+f.hp/f.maxHp,0)/3;
      quality+=Math.round(Math.max(0,Math.min(1,health))*10000)+summary.survivors*6000+Math.min(2000,tally.turns*500);
    }
    if(!summary.won)break;
  }
  /*
   * A qualidade era somada com 12.000 por objetivo cumprido. Com os Objetivos
   * removidos, o que pontua é o que a jornada mostrou: quantos confrontos
   * caíram, com quanta Vida e quantos lutadores de pé.
   */
  const cleared=summaries.filter(s=>s.won).length;
  quality=Math.min(999999,quality);
  return {seed,team,encountersCleared:cleared,score:cleared*1000000+quality,summaries,highlights:{survivors:summaries.at(-1)?.survivors??0,turns:summaries.reduce((n,s)=>n+s.turns,0)}};
}
