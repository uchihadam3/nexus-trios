import { createBattle,stepBattle } from '../src/engine/battle';
import { characters } from '../src/data/characters';
import { shuffle } from '../src/engine/random';

// Test-only horizon; the game itself has no battle timeout.
const horizon=1200,teams=[
  ['hulk','captain','sakura'],['wolverine','deadpool','sakura'],
  ['gojo','rukia','scarletwitch'],['superman','thanos','hulk'],
  ['giorno','muzan','piccolo'],['vision','greenlantern','captain'],
  ['ironman','inosuke','mikasa'],['sakura','rukia','scarletwitch'],
];
const cases:{player:string[];enemy:string[];seed:number}[]=[];
for(let i=0;i<teams.length;i++)for(let j=i;j<teams.length;j++)for(let seed=1;seed<=3;seed++)cases.push({player:teams[i],enemy:teams[j],seed});
const rng={rng:343};
for(let seed=0;seed<120;seed++)cases.push({player:shuffle(characters.map(c=>c.id),rng).slice(0,3),enemy:shuffle(characters.map(c=>c.id),rng).slice(0,3),seed});
const unfinished:typeof cases=[];let longest:{seconds:number;match:typeof cases[number]}={seconds:0,match:cases[0]};
for(const match of cases){
  const battle=createBattle(match.player,match.enemy,match.seed);
  for(let tick=0;tick<horizon*10&&!battle.finished;tick++)stepBattle(battle);
  if(!battle.finished)unfinished.push(match);
  if(battle.time>longest.seconds)longest={seconds:battle.time,match};
  if(battle.finished&&(battle.reason!=='Incapacitação da equipe'||battle.fighters.some(f=>f.side===battle.winner&&f.hp>0)===false))throw Error(`Invalid result ${JSON.stringify(match)}`);
}
console.log(JSON.stringify({count:cases.length,horizon,longest,unfinished},null,2));
if(unfinished.length)process.exitCode=1;
