/*
 * Mede a chance de vencer cada luta e de ser campeão para três perfis de
 * jogador: aleatorio (trio sorteado), bom (escolhe bem no draft, com
 * sinergia) e otimo (um dos 50 trios mais fortes do jogo).
 *
 * Uso: npx tsx scripts/medir-perfis.ts <aleatorio|bom|otimo> <jornadas>
 */
import {characters} from '../src/data/characters';
import {FORCA} from '../src/data/forca-dos-rivais';
import {createBattle,stepBattle} from '../src/engine/battle';
import {generateCampaign,newDraft,pickDraft,skipDraft,forcaDoTrio} from '../src/engine/campaign';
const perfil=process.argv[2]!,N=Number(process.argv[3]);const ids=characters.map(c=>c.id);
let r=9090;const rnd=()=>{r=(Math.imul(r,1664525)+1013904223)>>>0;return r/4294967296;};
const CORTE=[...Object.values(FORCA)].sort((a,b)=>a-b)[Math.floor(0.7*Object.values(FORCA).length)]!;
function bom(seed:number){let d=newDraft(seed);while(d.team.length<3){const n=(id:string)=>forcaDoTrio([...d.team,id]);const m=[...d.candidates].sort((a,b)=>n(b)-n(a))[0]!;if((FORCA[m]??0)<CORTE&&d.skips>0){d=skipDraft(d);continue;}d=pickDraft(d,m);}return d.team;}
let TOP:string[][]=[];
if(perfil==='otimo'){const m=new Map<string,{t:string[];f:number}>();for(const x of ids){let best:string[]=[],f=-1e9;for(const a of ids)for(const b of ids){if(a>=b||a===x||b===x)continue;const t=[x,a,b],v=forcaDoTrio(t);if(v>f){f=v;best=t;}}m.set([...best].sort().join('|'),{t:best,f});}TOP=[...m.values()].sort((a,b)=>b.f-a.f).slice(0,50).map(x=>x.t);}
const trio=(seed:number)=>{if(perfil==='bom')return bom(seed);if(perfil==='otimo')return TOP[Math.floor(rnd()*TOP.length)]!;const t=new Set<string>();while(t.size<3)t.add(ids[Math.floor(rnd()*ids.length)]!);return [...t];};
const v=Array(10).fill(0),alcancou=Array(10).fill(0);let camp=0,soma=0;
for(let n=0;n<N;n++){const seed=Math.floor(rnd()*2**31),team=trio(seed);soma+=forcaDoTrio(team);let vivo=true;
 generateCampaign(seed,team).forEach((e,i)=>{if(vivo)alcancou[i]++;const b=createBattle(team,e.team,seed+i*7919,e.scale);for(let t=0;t<9000&&!b.finished;t++)stepBattle(b);const w=b.winner==='player';if(w)v[i]++;if(!w)vivo=false;});if(vivo)camp++;}
console.log(JSON.stringify({perfil,porLuta:v.map(x=>Math.round(100*x/N)),chegaNaLuta:alcancou.map(x=>Math.round(100*x/N)),campeao:(100*camp/N).toFixed(1),forcaDoTrio:(soma/N).toFixed(2)}));
