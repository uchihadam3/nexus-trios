import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import { random,shuffle } from './random';
import { DOMINION as D, fracaoPorAlvo} from './dominion-config';
import type { Battle, BattleEvent, Effect, Fighter, Side, Skill, StatusId, Target, Topic } from './types';
import { chooseTarget, inferTargetIntent } from './targeting';
import { INVESTIGACAO_PARA_DEATH_NOTE } from './death-note';

export const STEP=.1;
const clamp=(n:number,lo=0,hi=1)=>Math.min(hi,Math.max(lo,n));
export const alive=(f:Fighter)=>f.hp>0;
export const intensity=(f:Fighter,id:StatusId)=>f.statuses.find(s=>s.id===id)?.intensity??0;
const friendly=(b:Battle,f:Fighter)=>b.fighters.filter(x=>x.side===f.side&&alive(x));
const hostile=(b:Battle,f:Fighter)=>b.fighters.filter(x=>x.side!==f.side&&alive(x));
/* Derivado de `statuses`, nunca repetido: ver a nota de tom em data/statuses.ts. */
export const negativeStatuses=new Set<StatusId>((Object.keys(statuses) as StatusId[]).filter(id=>statuses[id].tone==='negativo'));
const sign=(f:Fighter)=>f.side==='player'?1:-1;
const pressure=(b:Battle,side:Side,points:number)=>{b.momentum=clamp(b.momentum+(side==='player'?1:-1)*points,-D.maxScore,D.maxScore);};
export function emit(b:Battle,e:Omit<BattleEvent,'id'|'time'>){b.events.push({...e,id:b.nextEvent++,time:b.time});if(b.events.length>180)b.events.shift();}

export function createBattle(player:string[],enemy:string[],seed=Date.now(),enemyScale=1):Battle {
  if(player.length!==3||enemy.length!==3||new Set(player).size!==3||new Set(enemy).size!==3||[...player,...enemy].some(id=>!byId[id]))throw new Error('Cada equipe precisa de três personagens diferentes e válidos.');
  const b:Battle={version:1,seed,rng:seed>>>0,time:0,fighters:[],dominion:0,momentum:0,events:[],nextEvent:1,winner:null,reason:'',finished:false,turns:0,lastLead:null};
  for(const side of ['player','enemy'] as Side[]) (side==='player'?player:enemy).forEach((id,slot)=>{
    const c=byId[id], maxHp=Math.round(c.hp*(side==='enemy'?enemyScale:1));
    b.fighters.push({uid:`${side}-${slot}`,characterId:id,side,slot,hp:maxHp,maxHp,action:random(b)*.12,skills:c.skills.map(()=>({charge:0,cooldown:0,executing:0,uses:0})),statuses:[],shields:[],cast:null,investigation:{},discovered:{},traitTimer:0,storedEnergy:0,stats:{damage:0,healing:0,protection:0,interrupts:0,skills:0,kills:0}});
  });
  return b;
}
export function targets(b:Battle,actor:Fighter,rule:Target,effects:Effect[]=[],record=true):Fighter[] {
  const allies=friendly(b,actor).sort((a,z)=>a.characterId.localeCompare(z.characterId)),enemies=hostile(b,actor).sort((a,z)=>a.characterId.localeCompare(z.characterId));
  if(rule==='self')return alive(actor)?[actor]:[];
  if(rule==='allAllies')return allies;
  if(rule==='allEnemies')return enemies;
  /*
   * O Light investiga um inimigo de cada vez, até o fim. Espalhar a
   * investigação pelos três — o que ele fazia — deixava a Death Note para
   * depois de a luta acabar: ele ganhava 8% das lutas.
   */
  const emInvestigacao=()=>{
    const unknown=enemies.filter(x=>!actor.discovered?.[x.uid]);
    const foco=[...unknown].sort((a,z)=>(actor.investigation[z.uid]??0)-(actor.investigation[a.uid]??0)||a.uid.localeCompare(z.uid))[0];
    return foco&&(actor.investigation[foco.uid]??0)>0?[foco]:unknown;
  };
  if(actor.characterId==='light'&&rule==='enemyWeak'&&effects.some(effect=>effect.kind==='investigate')){
    const alvos=emInvestigacao();
    if(alvos.length)return chooseTarget(b,actor,alvos,rule,'investigate',effects,record);
  }
  if(actor.characterId==='light'&&rule==='investigated'){
    const isInvestigation=effects.some(effect=>effect.kind==='investigate');
    const isDeathNote=effects.some(effect=>effect.kind==='deathnote');
    if(isInvestigation){
      const alvos=emInvestigacao();
      if(alvos.length)return chooseTarget(b,actor,alvos,rule,'investigate',effects,record);
      return chooseTarget(b,actor,enemies,rule,'investigate',effects,record);
    }
    if(isDeathNote){
      /* Vulnerável e investigado: a Death Note elimina. */
      const vulnerable=enemies.filter(x=>actor.discovered?.[x.uid]==='vulnerable'&&(actor.investigation[x.uid]??0)>=INVESTIGACAO_PARA_DEATH_NOTE);
      if(vulnerable.length)return chooseTarget(b,actor,vulnerable,rule,'finisher',effects,record);
      /* Imune: uma vez só — dano e Exposto. Depois ele sabe, e não gasta mais nele. */
      const imunes=enemies.filter(x=>actor.discovered?.[x.uid]==='immune'&&(actor.investigation[x.uid]??0)>=INVESTIGACAO_PARA_DEATH_NOTE&&!actor.notaUsada?.[x.uid]);
      if(imunes.length)return chooseTarget(b,actor,imunes,rule,'finisher',effects,record);
      return [];
    }
  }
  const intent=inferTargetIntent(actor,rule,effects);
  if(rule==='enemyCast'){
    const casting=enemies.filter(x=>x.cast);
    if(casting.length)return chooseTarget(b,actor,casting,rule,intent,effects,record);
    if(intent==='interrupt')return [];
  }
  return chooseTarget(b,actor,rule==='allyWeak'?allies:enemies,rule,intent,effects,record);
}
/*
 * `gain` dá Carga. `trigger` dá Carga **e** dispara o traço.
 *
 * Quatro tópicos passavam só pelo `gain`: enemyHurt, winning, losing e
 * survived. O tipo `Topic` permite declarar um traço em qualquer um deles, e a
 * ficha mostrava o texto normalmente — mas o traço nunca acontecia. Catorze
 * personagens tinham traço morto por isso, entre eles o "Anjo sem coração" do
 * Sephiroth, o "Glory Kill" do Doom Slayer e o "Presença dominante" do
 * Aquaman, que é dos 100 originais.
 *
 * Agora os quatro passam pelo `trigger`. O `traitTimer` já limita a
 * frequência, e todos os traços afetados têm recarga de um segundo ou mais —
 * então `survived`, `winning` e `losing`, que ocorrem a cada passo, não viram
 * disparo a cada passo.
 */
function gain(b:Battle,f:Fighter,topic:Topic,amount:number,source?:Fighter){
  if(!alive(f))return;
  byId[f.characterId].skills.forEach((s,i)=>{
    const state=f.skills[i];
    if(state.cooldown>0||f.cast?.skill===i)return;
    const delta=s.charge.filter(c=>c.on===topic).reduce((sum,c)=>sum+c.amount*amount,0);
    const before=state.charge;state.charge=clamp(state.charge+delta,0,100);
    if(before<100&&state.charge>=100)emit(b,{kind:'ready',source:f.uid,skill:i,label:s.name,visual:s.icon});
    if(delta>0&&state.charge>before&&topic!=='time'){
      const gained=state.charge-before,actor=source??f;
      emit(b,{kind:'charge',source:actor.uid,target:f.uid,skill:i,label:topic,value:gained});
      if(source&&source.uid!==f.uid&&source.side===f.side){pressure(b,f.side,D.event.synergyCharge*clamp(gained/25));emit(b,{kind:'synergy',source:source.uid,target:f.uid,skill:i,label:s.name,value:gained});}
    }
  });
}
function trigger(b:Battle,f:Fighter,topic:Topic,source?:Fighter,amount=1){
  if(!alive(f))return;
  gain(b,f,topic,amount,source);
  const t=byId[f.characterId].trait;
  if(t.on===topic&&f.traitTimer<=0){
    f.traitTimer=Math.max(t.cooldown,STEP);
    applyEffects(b,f,targets(b,f,t.target,t.effects),t.effects,amount);
  }
}
function damage(b:Battle,source:Fighter,target:Fighter,raw:number){
  if(!alive(target))return;
  const outgoing=raw*(1+intensity(source,'strengthened'))*(1-intensity(source,'weakened'));
  const beforeProtection=outgoing*(1+intensity(target,'exposed')+intensity(target,'marked')+intensity(target,'electric'));
  const protection=intensity(target,'protected');
  let amount=beforeProtection*(1-protection),blocked=beforeProtection-amount;
  for(const s of target.shields){const used=Math.min(s.amount,amount);s.amount-=used;amount-=used;blocked+=used;const owner=b.fighters.find(f=>f.uid===s.source);if(owner&&used>0){owner.stats.protection+=used;pressure(b,owner.side,D.event.usefulProtectionPerFullCondition*clamp(used/target.maxHp));emit(b,{kind:'block',source:owner.uid,target:target.uid,attacker:source.uid,label:'Bloqueio',value:used,visual:'shield'});trigger(b,owner,'protected',owner,used/100);}}
  target.shields=target.shields.filter(s=>s.amount>.01);
  if(protection>0){const owner=b.fighters.find(f=>f.uid===target.statuses.find(s=>s.id==='protected')?.source);if(owner){owner.stats.protection+=beforeProtection*protection;pressure(b,owner.side,D.event.usefulProtectionPerFullCondition*clamp(beforeProtection*protection/target.maxHp));emit(b,{kind:'block',source:owner.uid,target:target.uid,attacker:source.uid,label:'Proteção',value:beforeProtection*protection,visual:'shield'});trigger(b,owner,'protected',owner,beforeProtection*protection/100);}}
  const hpBefore=target.hp;
  const dealt=Math.min(hpBefore,amount);target.hp=Math.max(0,hpBefore-dealt);source.stats.damage+=dealt;
  if(dealt>.01){
    emit(b,{kind:'damage',source:source.uid,target:target.uid,label:'Impacto',value:dealt});
    pressure(b,source.side,D.event.damagePerFullCondition*clamp(dealt/target.maxHp));
    if(beforeProtection>=hpBefore&&target.hp>0&&blocked>0)pressure(b,target.side,D.event.clutchSave);
    trigger(b,source,'dealt',source,dealt/100);
    trigger(b,target,'received',source,dealt/100);
    for(const f of b.fighters){if(f.side===target.side&&f.uid!==target.uid)trigger(b,f,'allyHurt',target,dealt/100);if(f.side!==target.side)trigger(b,f,'enemyHurt',source,dealt/100);}
  }
  if(beforeProtection>target.maxHp*D.event.criticalThreshold/100&&alive(target)&&target.hp/target.maxHp<=D.event.criticalThreshold/100)pressure(b,source.side,D.event.criticalCrossing);
  if(!alive(target)){
    pressure(b,source.side,D.event.knockout);target.cast=null;target.action=0;target.statuses=[];target.shields=[];source.stats.kills++;
    emit(b,{kind:'ko',source:source.uid,target:target.uid,label:`${byId[target.characterId].name} incapacitado`});
  }
}
function healing(b:Battle,source:Fighter,target:Fighter,value:number){
  if(!alive(target))return;
  const used=Math.min(target.maxHp-target.hp,value);target.hp+=used;source.stats.healing+=used;
  if(used>.01){pressure(b,source.side,D.event.usefulHealingPerFullCondition*clamp(used/target.maxHp));emit(b,{kind:'heal',source:source.uid,target:target.uid,label:'Recuperação',value:used});}
}
export function applyEffects(b:Battle,source:Fighter,selected:Fighter[],effects:Effect[],scale=1){
  for(const effect of effects){
    const list=effect.target?targets(b,source,effect.target,[effect]):selected;
    if(effect.kind==='release'){
      const total=(source.storedEnergy??0)*effect.multiplier;
      source.storedEnergy=0;
      const targetsAlive=list.filter(alive),share=targetsAlive.length?total/targetsAlive.length:0;
      for(const target of targetsAlive)damage(b,source,target,share);
      continue;
    }
    /*
     * Quantos alvos vivos este efeito vai alcançar.
     *
     * Precisa ser contado **antes** do laço: se o primeiro alvo cair no
     * próprio golpe, os seguintes não podem receber uma fração diferente.
     */
    const vivosNoAlvo=list.filter(alive).length;
    const fracao=fracaoPorAlvo(vivosNoAlvo);
    for(const target of list){
      if(!alive(target))continue;
      switch(effect.kind){
        case 'damage':damage(b,source,target,effect.value*fracao);break;
        case 'heal':healing(b,source,target,effect.value);break;
        case 'shield':{
          const existing=target.shields.reduce((n,s)=>n+s.amount,0);
          const added=Math.max(0,Math.min(effect.value,target.maxHp*.55-existing));
          if(added>0){target.shields.push({amount:added,remaining:10,source:source.uid});emit(b,{kind:'shield',source:source.uid,target:target.uid,label:'Escudo',value:added,visual:'shield'});}break;
        }
        case 'status':{
          const def=statuses[effect.status],existing=target.statuses.find(s=>s.id===effect.status);
          if(existing){existing.remaining=Math.max(existing.remaining,effect.duration);existing.duration=Math.max(existing.duration??0,effect.duration);existing.intensity=Math.min(def.cap,def.stack==='add'?existing.intensity+effect.value:Math.max(existing.intensity,effect.value));existing.source=source.uid;}
          else target.statuses.push({id:effect.status,remaining:effect.duration,duration:effect.duration,intensity:Math.min(def.cap,effect.value),source:source.uid});
          /*
           * A duração vai no evento para o Raio-X não precisar adivinhá-la.
           *
           * A análise causal do pós-batalha pergunta coisas como "o Exposto que
           * A aplicou ainda estava de pé quando B bateu?". Sem a duração no
           * evento, a única saída seria uma janela de tempo arbitrária — ou
           * seja, inventar causalidade, que é exatamente o que a direção
           * proibiu. Com ela, a resposta é exata.
           */
          emit(b,{kind:'status',source:source.uid,target:target.uid,label:def.name,status:effect.status,value:effect.duration});
          if(target.side!==source.side){const weight=effect.status==='paralyzed'?1:effect.status==='rooted'?.65:effect.status==='slow'?.35:effect.status==='silenced'?.55:['exposed','marked','electric','burning'].includes(effect.status)?.3:0;if(weight)pressure(b,source.side,D.event.statusApplied*weight);}
          // Status events only charge observers; they cannot recursively execute other traits.
          const negative=target.side!==source.side&&negativeStatuses.has(effect.status);
          for(const f of friendly(b,source)){gain(b,f,'status',1,source);if(negative)gain(b,f,'negativeStatus',1,source);}
          if(target.side!==source.side){for(const f of friendly(b,source)){const t=byId[f.characterId].trait;if((t.on==='status'||negative&&t.on==='negativeStatus')&&f.traitTimer<=0){f.traitTimer=Math.max(t.cooldown,STEP);applyEffects(b,f,targets(b,f,t.target),t.effects);}}}
          break;
        }
        case 'interrupt':{
          if(!target.cast)break;
          if(intensity(target,'protected')>=.3){emit(b,{kind:'shield',source:target.uid,target:target.uid,label:'Preparação protegida',visual:'shield'});break;}
          if(effect.mode==='cancel'){const i=target.cast.skill;target.cast=null;target.skills[i].charge=25;target.skills[i].cooldown=2;}
          else if(effect.mode==='delay')target.cast.elapsed=Math.max(-2,target.cast.elapsed-effect.value);
          else target.cast.elapsed=Math.max(0,target.cast.elapsed*(1-effect.value));
          source.stats.interrupts++;pressure(b,source.side,D.event.interruption);
          emit(b,{kind:'interrupt',source:source.uid,target:target.uid,label:effect.mode==='cancel'?'Interrompido!':'Preparação atrasada',visual:'bolt'});
          trigger(b,source,'interrupt',source);break;
        }
        case 'investigate':{const before=source.investigation[target.uid]??0,after=Math.min(100,before+effect.value);source.investigation[target.uid]=after;const quarters=Math.floor(after/25)-Math.floor(before/25);if(quarters>0)pressure(b,source.side,quarters*D.event.investigationQuarter+(after===100?D.event.investigationComplete:0));if(after>=INVESTIGACAO_PARA_DEATH_NOTE&&!source.discovered?.[target.uid]){source.discovered??={};source.discovered[target.uid]=byId[target.characterId].deathNoteCompatible?'vulnerable':'immune';emit(b,{kind:'discovery',source:source.uid,target:target.uid,label:source.discovered[target.uid]==='vulnerable'?'Vulnerável à Death Note':'Imune à execução'});}break;}
        case 'deathnote':{
          if((source.investigation[target.uid]??0)<INVESTIGACAO_PARA_DEATH_NOTE)break;
          if(byId[target.characterId].deathNoteCompatible){const value=target.hp;target.hp=0;target.cast=null;target.shields=[];target.statuses=[];source.stats.damage+=value;source.stats.kills++;pressure(b,source.side,D.event.deathNote);emit(b,{kind:'ko',source:source.uid,target:target.uid,label:'Sentença concluída',value});}
          else{source.notaUsada??={};source.notaUsada[target.uid]=true;applyEffects(b,source,[target],[{kind:'status',status:'exposed',value:.55,duration:14},{kind:'damage',value:110}]);}
          break;
        }
        case 'charge':target.skills.forEach((s,i)=>{if(s.cooldown<=0&&target.cast?.skill!==i){const before=s.charge;s.charge=Math.min(100,s.charge+effect.value);if(before<100&&s.charge>=100)emit(b,{kind:'ready',source:target.uid,skill:i,label:byId[target.characterId].skills[i].name,visual:byId[target.characterId].skills[i].icon});if(s.charge>before){emit(b,{kind:'charge',source:source.uid,target:target.uid,skill:i,label:source.uid===target.uid?'trait':'synergy',value:s.charge-before});if(source.uid!==target.uid){pressure(b,source.side,D.event.synergyCharge*clamp((s.charge-before)/25));emit(b,{kind:'synergy',source:source.uid,target:target.uid,skill:i,label:'Carga recebida',value:s.charge-before});}}}});break;
        case 'shift':{
          const before=target.action;target.action=clamp(target.action+effect.value);
          const delta=target.action-before;
          if(Math.abs(delta)>.005)emit(b,{kind:'tempo',source:source.uid,target:target.uid,label:delta>0?'Ação adiantada':'Ação atrasada',value:delta});
          break;
        }
        case 'store':source.storedEnergy=Math.min(effect.cap,(source.storedEnergy??0)+effect.value*scale);emit(b,{kind:'shield',source:source.uid,target:source.uid,label:'Energia cinética armazenada',value:source.storedEnergy,visual:'bolt'});break;
      }
    }
  }
}
function appropriate(b:Battle,f:Fighter,s:Skill){
  if(s.requiresSkills?.some(index=>(f.skills[index]?.uses??0)<1))return false;
  if(s.condition==='injured')return targets(b,f,s.target,s.effects).some(x=>x.hp/x.maxHp<.78);
  if(s.condition==='enemyCast')return hostile(b,f).some(x=>x.cast);
  if(s.condition==='threatened')return friendly(b,f).some(x=>x.hp/x.maxHp<.85)||hostile(b,f).some(x=>x.cast);
  if(s.condition==='investigated')return targets(b,f,s.target,s.effects,false).some(x=>(f.investigation[x.uid]??0)>=INVESTIGACAO_PARA_DEATH_NOTE);
  if(s.condition==='vulnerable')return hostile(b,f).some(x=>x.statuses.some(z=>['exposed','marked','paralyzed','electric','burning'].includes(z.id)));
  if(s.condition==='storedEnergy')return (f.storedEnergy??0)>0;
  return true;
}
function skillValue(b:Battle,f:Fighter,s:Skill,selected:Fighter[],intelligence:number):{score:number;reasons:string[]} {
  let value=0;const reasons:string[]=[],tacticalFactor=.65+intelligence/120;
  const add=(label:string,n:number)=>{if(n>0.05){value+=n;reasons.push(`${label} +${n.toFixed(1)}`);}};
  for(const effect of s.effects){
    const list=(effect.target?targets(b,f,effect.target,[effect],false):selected).filter(alive);
    if(effect.kind==='damage'||effect.kind==='deathnote'||effect.kind==='release'){
      const raw=effect.kind==='release'?(f.storedEnergy??0)*effect.multiplier:effect.value;
      for(const target of list){
        const ready=effect.kind!=='deathnote'||(f.investigation[target.uid]??0)>=INVESTIGACAO_PARA_DEATH_NOTE;
        const shields=target.shields.reduce((n,x)=>n+x.amount,0),amount=ready?Math.min(target.hp+shields,raw):0;
        add('dano útil',amount/target.maxHp*65);
        if(amount>=target.hp+shields&&amount>0)add('incapacitação provável',18);
        if(effect.kind==='deathnote'&&ready)add('sentença preparada',f.discovered?.[target.uid]==='vulnerable'?40:10);
      }
    }else if(effect.kind==='heal'){
      for(const target of list){const used=Math.min(target.maxHp-target.hp,effect.value);add('cura necessária',used/target.maxHp*48*tacticalFactor);if(target.hp/target.maxHp<.3&&used>0)add('aliado crítico',8*tacticalFactor);}
    }else if(effect.kind==='shield'){
      for(const target of list){const existing=target.shields.reduce((n,x)=>n+x.amount,0);const need=target.maxHp*(1-target.hp/target.maxHp)+target.maxHp*.12-existing;const used=Math.max(0,Math.min(effect.value,need));add('proteção preventiva',used/target.maxHp*26*tacticalFactor);}
    }else if(effect.kind==='interrupt'){
      for(const target of list)if(target.cast)add('interromper preparação',(22+Math.max(0,target.cast.elapsed/target.cast.duration)*12)*tacticalFactor);
    }else if(effect.kind==='status'){
      for(const target of list){const existing=target.statuses.find(x=>x.id===effect.status)?.intensity??0;const weight=effect.status==='paralyzed'?1:effect.status==='rooted'?.7:effect.status==='silenced'?.65:effect.status==='slow'?.4:['exposed','marked','electric','burning'].includes(effect.status)?.35:effect.status==='protected'?.5:0;add('efeito de estado',Math.max(0,effect.value-existing)*weight*24*tacticalFactor);}
    }else if(effect.kind==='investigate'){
      for(const target of list){const progress=f.investigation[target.uid]??0;add('investigação',effect.value/100*14*(1-progress/100)*tacticalFactor);}
    }else if(effect.kind==='charge'){
      add('carga de habilidades',Math.max(0,100-f.skills.reduce((n,x)=>n+x.charge,0))/300*12);
    }else if(effect.kind==='shift'){
      add('controle de ritmo',Math.abs(effect.value)*12);
    }else if(effect.kind==='store'){
      add('energia armazenada',Math.max(0,effect.cap-f.storedEnergy)/Math.max(1,effect.cap)*Math.min(18,effect.value/8));
    }
  }
  const cost=s.preparation*3+s.cooldown*.08;
  value=Math.max(0,value-cost)+s.priority*.08;
  if(cost>0)reasons.push(`custo tático -${cost.toFixed(1)}`);
  return {score:value,reasons};
}
function decideSkill(b:Battle,f:Fighter):number|null {
  const c=byId[f.characterId],intelligence=c.intelligence??50;
  const candidates=c.skills.map((s,i)=>({s,i,state:f.skills[i]}))
    .filter(({s,state})=>state.charge>=100&&state.cooldown<=0&&appropriate(b,f,s))
    .map(({s,i,state})=>{const selected=targets(b,f,s.target,s.effects,false);const result=skillValue(b,f,s,selected,intelligence);return {s,i,state,selected,...result};})
    .sort((a,z)=>z.score-a.score||a.i-z.i);
  if(!candidates.length)return null;
  const best=candidates[0];
  b.decisionLog??=[];
  b.decisionLog.push({time:b.time,actor:f.uid,intelligence,candidates:candidates.map(x=>({skill:x.s.name,score:x.score,target:x.selected[0]?.uid,reasons:x.reasons})),chosen:best.s.name});
  if(b.decisionLog.length>120)b.decisionLog.shift();
  return best.i;
}
function execute(b:Battle,f:Fighter,index:number,selected:Fighter[]){
  const s=byId[f.characterId].skills[index],eventStart=b.nextEvent;
  emit(b,{kind:'skill',source:f.uid,target:selected[0]?.uid,skill:index,label:s.name,visual:s.icon});
  applyEffects(b,f,selected,s.effects);
  const effective=b.events.some(e=>e.id>=eventStart&&(['damage','heal','block','interrupt','ko','synergy'].includes(e.kind)||e.kind==='status'&&e.target!==f.uid));
  if(effective)pressure(b,f.side,s.preparation>=2.5?D.event.grandSkill:D.event.successfulSkill);
  f.stats.skills++;
  f.skills[index].uses=(f.skills[index].uses??0)+1;
  f.skills[index].charge=0;f.skills[index].cooldown=s.cooldown;f.skills[index].executing=.7;
}
export function updateDominion(b:Battle){
  const group=(side:Side)=>b.fighters.filter(f=>f.side===side);
  const health=(side:Side)=>group(side).reduce((n,f)=>n+f.hp/f.maxHp,0)/3;
  const count=(side:Side)=>group(side).filter(alive).length;
  const controlled=(side:Side)=>group(side).filter(alive).reduce((n,f)=>n+(intensity(f,'paralyzed')*D.controlStatus.paralyzed)+(intensity(f,'slow')*D.controlStatus.slowed)+(intensity(f,'rooted')*D.controlStatus.rooted)+(intensity(f,'silenced')*D.controlStatus.silenced)+(intensity(f,'exposed')*D.controlStatus.exposed)+(intensity(f,'marked')*D.controlStatus.marked),0);
  const situation=clamp((health('player')-health('enemy'))*D.situation.condition+(count('player')-count('enemy'))*D.situation.activeFighter+(controlled('enemy')-controlled('player'))*D.situation.control,-D.maxScore,D.maxScore);
  const target=clamp(situation*D.situationWeight+b.momentum*D.eventMemoryWeight,-D.maxScore,D.maxScore);
  const approach=1-Math.exp(-STEP/D.responseSeconds);
  b.dominion=clamp(b.dominion+(target-b.dominion)*approach,-D.maxScore,D.maxScore);
  const leader=b.dominion>5?'player':b.dominion< -5?'enemy':null;
  if(leader&&b.lastLead&&leader!==b.lastLead){b.turns++;emit(b,{kind:'turn',source:`${leader}-0`,label:'O Domínio virou'});}
  if(leader)b.lastLead=leader;
}
export function resolve(b:Battle){
  const p=b.fighters.some(f=>f.side==='player'&&alive(f)),e=b.fighters.some(f=>f.side==='enemy'&&alive(f));
  if(!p||!e){b.finished=true;b.winner=p?'player':e?'enemy':null;b.reason='Incapacitação da equipe';}
}
export function stepBattle(b:Battle,observe?:(snapshot:Battle)=>void):Battle {
  if(b.finished)return b;
  b.time+=STEP;b.momentum*=Math.exp(-Math.LN2*STEP/D.memoryHalfLifeSeconds);
  for(const f of b.fighters){
    if(!alive(f))continue;
    f.traitTimer=Math.max(0,f.traitTimer-STEP);
    for(const s of [...f.statuses]){
      const origin=b.fighters.find(x=>x.uid===s.source)??f;
      if(s.id==='burning')damage(b,origin,f,s.intensity*STEP);
      if(s.id==='regen')healing(b,origin,f,s.intensity*STEP);
      s.remaining-=STEP;
    }
    resolve(b);if(b.finished){observe?.(b);return b;}
    f.statuses=f.statuses.filter(s=>s.remaining>0);f.shields.forEach(s=>s.remaining-=STEP);f.shields=f.shields.filter(s=>s.remaining>0&&s.amount>0);
    f.skills.forEach(s=>{s.cooldown=Math.max(0,s.cooldown-STEP);s.executing=Math.max(0,s.executing-STEP);});
    trigger(b,f,'time',undefined,STEP);trigger(b,f,'survived',undefined,STEP);
    if(b.dominion*sign(f)<-3)trigger(b,f,'losing',undefined,STEP);else if(b.dominion*sign(f)>3)trigger(b,f,'winning',undefined,STEP);
  }
  observe?.(b);
  for(const f of shuffle(b.fighters,b)){
    if(!alive(f))continue;
    const c=byId[f.characterId];
    const rate=(1+intensity(f,'haste'))*(1-intensity(f,'slow'))*(1-intensity(f,'rooted'));
    if(intensity(f,'paralyzed'))continue;
    if(f.cast){
      f.cast.elapsed+=STEP*rate;
      if(f.cast.elapsed>=f.cast.duration){const cast=f.cast;f.cast=null;let list=cast.targets.map(id=>b.fighters.find(x=>x.uid===id)).filter((x):x is Fighter=>!!x&&alive(x));if(!list.length&&c.skills[cast.skill].condition!=='investigated')list=targets(b,f,c.skills[cast.skill].target,c.skills[cast.skill].effects);execute(b,f,cast.skill,list);resolve(b);observe?.(b);if(b.finished)break;}
      continue;
    }
    if(!intensity(f,'silenced')){
      const selectedSkill=decideSkill(b,f);
      if(selectedSkill!==null){
        const i=selectedSkill,s=c.skills[i],list=targets(b,f,s.target,s.effects);
        if(s.preparation>0){f.cast={skill:i,elapsed:0,duration:s.preparation,targets:list.map(x=>x.uid)};emit(b,{kind:'cast',source:f.uid,target:list[0]?.uid,skill:i,label:s.name,visual:s.icon});for(const opponent of hostile(b,f))trigger(b,opponent,'enemyCast',f);}
        else execute(b,f,i,list);
        resolve(b);observe?.(b);if(b.finished)break;
        continue;
      }
    }
    f.action+=STEP*rate/c.interval;
    if(f.action>=1){
      f.action-=1;
      const selected=intensity(f,'confused')&&random(b)<.25?[f]:targets(b,f,c.basic.target,c.basic.effects);
      emit(b,{kind:'basic',source:f.uid,target:selected[0]?.uid,label:c.basic.name,visual:c.basic.visual});
      applyEffects(b,f,selected,c.basic.effects);trigger(b,f,'action',f);resolve(b);observe?.(b);if(b.finished)break;
    }
  }
  updateDominion(b);resolve(b);observe?.(b);return b;
}
export function simulate(player:string[],enemy:string[],seed=1,enemyScale=1):Battle {
  const b=createBattle(player,enemy,seed,enemyScale);while(!b.finished)stepBattle(b);return b;
}
