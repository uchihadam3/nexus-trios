import { characters, byId } from '../data/characters';
import { random,shuffle } from './random';
export interface Encounter {team:string[];name:string;power:number;scale:number}
export interface Draft {team:string[];candidates:string[];skips:number;rng:number}
export function candidates(draft:Draft,exclude:string[]=[]):string[]{return shuffle(characters.filter(c=>!draft.team.includes(c.id)&&!exclude.includes(c.id)).map(c=>c.id),draft).slice(0,3);}
export function newDraft(seed:number):Draft{const d={team:[],candidates:[],skips:3,rng:seed>>>0};return {...d,candidates:candidates(d)};}
export function skipDraft(d:Draft):Draft{if(d.skips<=0)return d;const next={...d,skips:d.skips-1};next.candidates=candidates(next,d.candidates);return next;}
export function pickDraft(d:Draft,id:string):Draft{if(d.team.length>=3||!d.candidates.includes(id)||d.team.includes(id))return d;const next={...d,team:[...d.team,id]};next.candidates=next.team.length<3?candidates(next):[];return next;}
export function synergy(team:string[]):number{
  const tags=team.flatMap(id=>byId[id].tags);let score=0;
  if(tags.includes('control')&&(tags.includes('plan')||tags.includes('burst')))score+=13;
  if(tags.includes('protect')&&(tags.includes('growth')||tags.includes('plan')))score+=12;
  if(tags.includes('support')&&tags.includes('burst'))score+=10;
  if(tags.includes('tempo')&&tags.includes('growth'))score+=7;
  if(new Set(tags).size>=5)score+=5;
  return score;
}
export function teamPower(team:string[]):number{return team.reduce((n,id)=>n+byId[id].power,0)+synergy(team);}
const bosses=[['thanos','gojo','superman'],['goku','captain','strange'],['light','pikachu','wolverine'],['thor','magneto','raven'],['hulk','flash','wonderwoman']];
export function generateCampaign(seed:number):Encounter[]{
  const rng={rng:seed>>>0},pool:Array<{team:string[];power:number}>=[];
  for(let i=0;i<240;i++){const team=shuffle(characters.map(c=>c.id),rng).slice(0,3);pool.push({team,power:teamPower(team)});}
  pool.sort((a,b)=>a.power-b.power);
  const names=['Primeiro encontro','Novos rivais','O ritmo aumenta','Entre universos','Ponto de ruptura','Pressão crescente','Sem recuar','A última barreira','À altura das lendas','O confronto final'];
  return names.map((name,i)=>{
    const entry=i===9?{team:bosses[Math.floor(random(rng)*bosses.length)],power:0}:pool[Math.floor((i/11+random(rng)*.08)*pool.length)];
    return {team:[...entry.team],name,power:teamPower(entry.team),scale:[.73,.8,.87,.93,1,1.04,1.08,1.12,1.16,1.2][i]};
  });
}
