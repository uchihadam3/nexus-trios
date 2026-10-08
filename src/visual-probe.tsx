import { createRoot } from 'react-dom/client';
import { BattleScreen } from './screens/BattleScreen';
import { applyEffects,createBattle } from './engine/battle';
import type { BattleEvent,Effect,Visual } from './engine/types';
import type { Beat } from './presentation/director';
import { defaults } from './lib/storage';
import './styles.css';
import './presentation/battle.css';
import './presentation/visual-game.css';

const params=new URLSearchParams(location.search),scenario=params.get('scenario')??'basic',phase=params.get('phase')??'windup';
localStorage.setItem('nexus-battle-guide-v1','1');
const battle=createBattle(['sakura','gojo','naruto'],['goku','vegeta','hulk'],99);
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
const before=structuredClone(battle),kind=scenario==='basic'||scenario==='energy'?'basic':'skill';
const event:BattleEvent={id:1000,time:0,kind,source:source.uid,target:target.uid,skill:kind==='skill'?0:undefined,label:kind==='basic'?'Ataque básico':scenario,visual};
applyEffects(battle,source,selected,effects);
const events=[event,...battle.events],after=structuredClone(battle),impacted=phase==='impact';
const beat:Beat={event,events,before,after,duration:2,elapsed:impacted?1.1:.35,impacted,family:visual==='impact'?'physical':visual==='psychic'?'psychic':visual==='bolt'?'electric':visual==='shield'?'shield':'buff',grand:false};
const settings={...defaults,volume:0,musicVolume:0,effectsVolume:0,numbers:true,explanations:'off' as const};
createRoot(document.getElementById('root')!).render(<div className="app"><main className="main battle-main"><BattleScreen battle={impacted?after:before} beat={beat} index={0} name="Prova visual de combate" settings={settings} paused={false} onPause={()=>{}} onAbandon={()=>{}} onSettings={()=>{}}/></main></div>);
