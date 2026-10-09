import {characters} from '../data/characters';
import {createBattle,stepBattle} from './battle';
import {generateCampaign} from './campaign';
import {pontosDaLuta} from './pontos';
import {summarizeBattle,type RunBattleSummary} from './run-summary';

/* 250.4: Preparo mínimo de 0,5 s (leve), efeitos repetidos somados, condições alcançáveis.
 * 250.5: pontos por desempenho (src/engine/pontos.ts), e a luta perdida também pontua. */
export const ENGINE_VERSION='nexus-250.5';
/* Temporada 2: a escala dos pontos mudou (milhares por luta, não milhões); a temporada nova não mistura as duas. */
export const BALANCE_VERSION='season-2';
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
  let score=0;
  const summaries:RunBattleSummary[]=[];
  for(const [index,encounter] of encounters.entries()){
    const battle=createBattle(team,encounter.team,seed+index*7919,encounter.scale);
    for(let tick=0;tick<9000&&!battle.finished;tick++)stepBattle(battle);
    if(!battle.finished)throw new Error(`Replay sem conclusão no confronto ${index+1}.`);
    const summary=summarizeBattle(index,battle);summaries.push(summary);
    // a conta da tela (src/engine/pontos.ts): a luta perdida também soma o que o trio fez nela
    score+=pontosDaLuta(battle,index).total;
    if(!summary.won)break;
  }
  const cleared=summaries.filter(s=>s.won).length;
  return {seed,team,encountersCleared:cleared,score,summaries,highlights:{survivors:summaries.at(-1)?.survivors??0,turns:summaries.reduce((n,s)=>n+s.turns,0)}};
}
