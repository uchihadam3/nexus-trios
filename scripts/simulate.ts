import { characters } from '../src/data/characters';
import { simulate } from '../src/engine/battle';
import { generateCampaign } from '../src/engine/campaign';
import { shuffle } from '../src/engine/random';
const rng={rng:10203};let champions=0,total=0;const reached=Array(10).fill(0),times:number[]=[];
for(let seed=1;seed<=100;seed++){const team=shuffle(characters.map(c=>c.id),rng).slice(0,3),campaign=generateCampaign(seed);let wins=0;for(let i=0;i<10;i++){reached[i]++;const b=simulate(team,campaign[i].team,seed+i*7919,campaign[i].scale);times.push(b.time);total++;if(b.winner!=='player')break;wins++;}if(wins===10)champions++;}
times.sort((a,b)=>a-b);
console.log(JSON.stringify({journeys:100,battles:total,champions,reached,seconds:{min:times[0],median:times[Math.floor(times.length/2)],max:times.at(-1)}},null,2));
