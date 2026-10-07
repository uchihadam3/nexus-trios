import { characters, byId } from '../data/characters';
import { random, shuffle } from './random';
export interface Encounter {team:string[];name:string;power:number;scale:number}
export interface Draft {team:string[];candidates:string[];skips:number;rng:number;banned?:string[]}
export function candidates(draft:Draft,exclude:string[]=[]):string[]{return shuffle(characters.filter(c=>!draft.team.includes(c.id)&&!draft.banned?.includes(c.id)&&!exclude.includes(c.id)).map(c=>c.id),draft).slice(0,3);}
export function newDraft(seed:number,banned:string[]=[]):Draft{const d={team:[],candidates:[],skips:3,rng:seed>>>0,banned};return {...d,candidates:candidates(d)};}
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
const scales=[.73,.8,.87,.93,1,1.04,1.08,1.12,1.16,1.2];
const names=['Primeiro encontro','Novos rivais','O ritmo aumenta','Entre universos','Ponto de ruptura','Pressão crescente','Sem recuar','A última barreira','À altura das lendas','O confronto final'];
function sampledTeams(ids:string[],rng:{rng:number},count:number):string[][]{
  const found=new Map<string,string[]>();
  const attempts=count*5;
  for(let i=0;i<attempts&&found.size<count;i++){
    const team=shuffle(ids,rng).slice(0,3);
    const key=[...team].sort().join('|');
    if(team.length===3&&!found.has(key))found.set(key,team);
  }
  return [...found.values()];
}
function selectBoss(available:string[],rng:{rng:number}):string[]{
  const eligible=bosses.filter(team=>team.length===3&&new Set(team).size===3&&team.every(id=>available.includes(id)));
  const candidates=eligible.length?eligible:sampledTeams(available,rng,256);
  if(!candidates.length)throw new Error('Elenco insuficiente para reservar um trio final válido.');
  const ranked=candidates.map(team=>({team,power:teamPower(team)})).sort((a,b)=>b.power-a.power);
  const finalists=ranked.slice(0,Math.min(3,ranked.length));
  return [...finalists[Math.floor(random(rng)*finalists.length)].team];
}
export function generateCampaign(seed:number,playerTeam:string[]=[]):Encounter[]{
  const uniquePlayer=[...new Set(playerTeam)];
  if(uniquePlayer.length!==playerTeam.length||playerTeam.some(id=>!byId[id]))throw new Error('O trio do jogador contém IDs repetidos ou inválidos.');
  if(playerTeam.length!==0&&playerTeam.length!==3)throw new Error('A campanha só pode ser gerada após a escolha de exatamente três personagens.');
  const eligible=characters.map(c=>c.id).filter(id=>!uniquePlayer.includes(id));
  if(eligible.length<30)throw new Error('Elenco insuficiente: são necessários três personagens do jogador e trinta inimigos únicos.');
  const rng={rng:seed>>>0};
  // Reserve the final trio first so the early encounters cannot consume a planned boss.
  const boss=selectBoss(eligible,rng);
  const used=new Set([...uniquePlayer,...boss]);
  const encounters:Encounter[]=[];
  for(let i=0;i<9;i++){
    const remaining=eligible.filter(id=>!used.has(id));
    const ranked=sampledTeams(remaining,rng,96).map(team=>({team,power:teamPower(team)})).sort((a,b)=>a.power-b.power);
    if(!ranked.length)throw new Error(`Elenco insuficiente para criar o encontro ${i+1} sem repetição.`);
    // Keep a broad progression while still choosing for power and synergy within
    // the currently eligible pool, instead of taking its first three IDs.
    const quantile=.12+.76*(i/8);
    const pick=Math.min(ranked.length-1,Math.floor(quantile*(ranked.length-1)));
    const team=[...ranked[pick].team];
    encounters.push({team,name:names[i],power:teamPower(team),scale:scales[i]});
    team.forEach(id=>used.add(id));
  }
  encounters.push({team:boss,name:names[9],power:teamPower(boss),scale:scales[9]});
  if(uniquePlayer.length===3){
    const result=validateCampaignUniqueness({team:uniquePlayer,encounters});
    if(!result.valid)throw new Error(`Campanha gerada com violações: ${result.errors.join('; ')}`);
  }else if(new Set(encounters.flatMap(encounter=>encounter.team)).size!==30)throw new Error('Campanha provisória gerada com personagens repetidos.');
  return encounters;
}
export function validateCampaignUniqueness(run:{team:string[];encounters:Encounter[]}):{valid:boolean;errors:string[]}{
  const errors:string[]=[];
  if(run.team.length!==3||new Set(run.team).size!==3||run.team.some(id=>!byId[id]))errors.push('O trio do jogador precisa conter três personagens válidos e distintos.');
  if(run.encounters.length!==10)errors.push('A campanha precisa conter dez encontros.');
  const used=new Set<string>(),enemyIds:string[]=[];
  run.encounters.forEach((encounter,index)=>{
    if(encounter.team.length!==3||new Set(encounter.team).size!==3)errors.push(`Encontro ${index+1}: trio inválido ou com IDs repetidos.`);
    for(const id of encounter.team){
      if(!byId[id])errors.push(`Encontro ${index+1}: personagem desconhecido (${id}).`);
      if(run.team.includes(id))errors.push(`Encontro ${index+1}: personagem do jogador usado como inimigo (${id}).`);
      if(used.has(id))errors.push(`Encontro ${index+1}: personagem inimigo repetido na jornada (${id}).`);
      used.add(id);enemyIds.push(id);
    }
  });
  if(run.encounters.length===10&&enemyIds.length!==30)errors.push('A campanha completa precisa ter trinta inimigos.');
  if(run.encounters.length===10&&new Set(enemyIds).size!==30)errors.push('Os trinta inimigos precisam ser únicos.');
  return {valid:errors.length===0,errors};
}
