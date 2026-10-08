import { useEffect,useState } from 'react';
import { createRoot } from 'react-dom/client';
import { PRESENTATION } from './presentation/config';
import { BattleScreen } from './screens/BattleScreen';
import { applyEffects,createBattle } from './engine/battle';
import { byId } from './data/characters';
import type { BattleEvent,Effect,Visual } from './engine/types';
import type { Beat } from './presentation/director';
import { defaults } from './lib/storage';
import './styles.css';
import './presentation/battle.css';
import './presentation/visual-game.css';
import './presentation/arena.css';
import './presentation/acting-motion.css';
import './presentation/acting.css';
import './presentation/vfx-families.css';

const params=new URLSearchParams(location.search),scenario=params.get('scenario')??'basic',phase=params.get('phase')??'windup';
localStorage.setItem('nexus-battle-guide-v1','1');
/*
 * `?hab=goku:0` (ou `goku:b` para o básico): a habilidade de verdade de
 * qualquer personagem, com os efeitos da ficha — para fotografar cada família
 * de efeito (adendo, parte 3) na arena, com a cor do personagem.
 */
const hab=params.get('hab');
const [habId,habSlot]=(hab??'').split(':');
const habIndex=habSlot===undefined||habSlot==='b'?undefined:Number(habSlot);
const rivais=['goku','vegeta','hulk'].filter(x=>x!==habId).concat(['thor']).slice(0,3);
/* `nomes`: os nomes mais longos do elenco, para ver se a arena aguenta. */
const aliados=['sakura','naruto','gojo'].filter(x=>x!==habId).slice(0,2);
const battle=hab?createBattle([habId,...aliados],rivais,99):scenario==='nomes'?createBattle(['coragem','raidenmk','capitaoplaneta'],['dannyphantom','lexluthor','sailormoon'],99):createBattle(['sakura','gojo','naruto'],['goku','vegeta','hulk'],99);
const [sakura,gojo,naruto,goku,vegeta,hulk]=battle.fighters;
let source=sakura,target=goku,effects:Effect[]=[{kind:'damage',value:190}],selected=[goku],visual:Visual='impact';
if(scenario==='heal'){source=sakura;target=naruto;target.hp-=240;effects=[{kind:'heal',value:170}];selected=[target];visual='shield';}
if(scenario==='shield'){source=gojo;target=naruto;effects=[{kind:'shield',value:240}];selected=[target];visual='shield';}
if(scenario==='buff'){source=naruto;target=sakura;effects=[{kind:'status',status:'haste',value:.35,duration:6}];selected=[target];visual='wave';}
if(scenario==='debuff'){source=gojo;target=goku;effects=[{kind:'status',status:'exposed',value:.22,duration:8}];selected=[target];visual='psychic';}
if(scenario==='interrupt'){source=gojo;target=goku;target.cast={skill:0,elapsed:1,duration:4,targets:[gojo.uid]};effects=[{kind:'interrupt',mode:'cancel',value:1}];selected=[target];visual='bolt';}
if(scenario==='aoe'){source=gojo;target=goku;effects=[{kind:'damage',value:180}];selected=[goku,vegeta,hulk];visual='psychic';}
if(scenario==='synergy'){source=naruto;target=sakura;effects=[{kind:'charge',value:28}];selected=[target];visual='wave';}
if(scenario==='ko'){source=sakura;target=goku;target.hp=80;effects=[{kind:'damage',value:190}];selected=[target];}
if(scenario==='energy'){source=gojo;target=goku;effects=[{kind:'damage',value:155}];selected=[target];visual='psychic';}
if(scenario==='acumulo'){
  /* O exemplo do jogador: 10% de Exposto, depois mais 20%, dá 30%. */
  applyEffects(battle,sakura,[goku],[{kind:'status',status:'exposed',value:.10,duration:8}]);
  applyEffects(battle,gojo,[goku],[{kind:'status',status:'slow',value:.22,duration:6}]);
  applyEffects(battle,naruto,[sakura],[{kind:'status',status:'haste',value:.2,duration:6}]);
  source=gojo;target=goku;effects=[{kind:'status',status:'exposed',value:.20,duration:8}];selected=[target];visual='psychic';
}
if(scenario==='estados'||scenario==='nomes'){
  /* Todos os estados difíceis de uma vez: Preparo, fora da luta, Vida baixa
   * com Escudo, muitos Status, habilidade pronta, em recarga e quase atacando. */
  goku.cast={skill:0,elapsed:1.2,duration:3,targets:[sakura.uid]};
  vegeta.hp=0;
  hulk.hp=Math.round(hulk.maxHp*.18);hulk.shields=[{amount:220,remaining:6}] as typeof hulk.shields;
  applyEffects(battle,gojo,[sakura],[{kind:'status',status:'haste',value:.2,duration:6},{kind:'status',status:'regen',value:8,duration:6},{kind:'status',status:'protected',value:.2,duration:6},{kind:'status',status:'strengthened',value:.1,duration:6},{kind:'status',status:'strengthened',value:.1,duration:6}]);
  applyEffects(battle,goku,[sakura],[{kind:'status',status:'slow',value:.2,duration:6},{kind:'status',status:'exposed',value:.2,duration:6},{kind:'status',status:'burning',value:6,duration:6},{kind:'status',status:'marked',value:.1,duration:6},{kind:'status',status:'weakened',value:.1,duration:6},{kind:'status',status:'silenced',value:1,duration:3}]);
  naruto.skills[0].charge=100;naruto.skills[1].cooldown=4;naruto.skills[2].charge=55;
  gojo.action=.93;
  source=gojo;target=goku;effects=[{kind:'damage',value:120}];selected=[target];visual='psychic';
}
let label:string=scenario,skillIndex:number|undefined=0;
let porAlvo:((e:Effect)=>typeof selected)|null=null;
if(hab){
  const c=byId[habId],ficha=habIndex===undefined?{effects:c.basic.effects,target:c.basic.target,name:c.basic.name,visual:c.basic.visual}:{...c.skills[habIndex],visual:c.skills[habIndex].icon};
  const [eu,amigo1,amigo2,r1,r2,r3]=battle.fighters;
  source=eu;label=ficha.name;skillIndex=habIndex;visual=ficha.visual;
  const ajuda=ficha.target==='self'||ficha.target==='allyWeak'||ficha.target==='allAllies';
  selected=ficha.target==='allEnemies'?[r1,r2,r3]:ficha.target==='allAllies'?[eu,amigo1,amigo2]:ficha.target==='self'?[eu]:ajuda?[amigo1]:[r2];
  target=selected[0];
  amigo1.hp-=200;
  effects=ficha.effects.filter(e=>e.kind!=='deathnote'&&e.kind!=='investigate');
  porAlvo=(e:Effect)=>e.target==='allAllies'?[eu,amigo1,amigo2]:e.target==='allyWeak'?[amigo1]:e.target==='self'?[eu]:e.target==='allEnemies'?[r1,r2,r3]:e.target&&e.target.startsWith('enemy')||e.target==='randomEnemy'?[r2]:selected;
  if(ficha.effects.some(e=>e.kind==='deathnote'))effects=[{kind:'damage',value:r2.hp}];
  if(!effects.length)effects=[{kind:'damage',value:60}];
}
const before=structuredClone(battle),kind=hab?(habIndex===undefined?'basic':'skill'):scenario==='basic'||scenario==='energy'?'basic':'skill';
const event:BattleEvent={id:1000,time:0,kind,source:source.uid,target:target.uid,skill:kind==='skill'?(hab?skillIndex:0):undefined,label:kind==='basic'?'Ataque básico':label,visual};
if(porAlvo){const alvoDe=porAlvo;for(const e of effects)applyEffects(battle,source,alvoDe(e),[{...e,target:undefined} as Effect]);}else applyEffects(battle,source,selected,effects);
const events=[event,...battle.events],after=structuredClone(battle),impacted=phase==='impact';
const beat:Beat={event,events,before,after,duration:2,elapsed:impacted?1.1:.35,impacted,family:visual==='impact'?'physical':visual==='psychic'?'psychic':visual==='bolt'?'electric':visual==='shield'?'shield':'buff',grand:false};
const settings={...defaults,volume:0,musicVolume:0,effectsVolume:0,numbers:true,explanations:'off' as const};
/*
 * `?play=1`: a ação corre em tempo real e em laço — preparação, impacto no
 * momento certo, fim — para conferir o movimento, não só um quadro parado.
 * A duração segue o tipo da ação, como no jogo.
 */
const play=params.get('play')==='1';
const durationFor=kind==='basic'?PRESENTATION.normalSeconds:PRESENTATION.skillSeconds;
function Play(){
  const [clock,setClock]=useState({id:1000,t:0});
  useEffect(()=>{let frame=0,start=performance.now(),id=1000;const tick=(now:number)=>{let t=(now-start)/1000;if(t>durationFor+.5){start=now;t=0;id+=1;}setClock({id,t});frame=requestAnimationFrame(tick);};frame=requestAnimationFrame(tick);return ()=>cancelAnimationFrame(frame);},[]);
  const hit=clock.t>=durationFor*PRESENTATION.impactAt,live:Beat={...beat,event:{...event,id:clock.id},duration:durationFor,elapsed:Math.min(clock.t,durationFor),impacted:hit};
  return <BattleScreen battle={hit?after:before} beat={clock.t<=durationFor?live:null} index={0} name="Prova visual de combate" settings={settings} paused={false} onPause={()=>{}} onAbandon={()=>{}} onSettings={()=>{}}/>;
}
createRoot(document.getElementById('root')!).render(<div className="app"><main className="main battle-main">{play?<Play/>:<BattleScreen battle={impacted?after:before} beat={beat} index={0} name="Prova visual de combate" settings={settings} paused={false} onPause={()=>{}} onAbandon={()=>{}} onSettings={()=>{}}/>}</main></div>);
