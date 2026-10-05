import { byId } from '../data/characters';
import type { Battle, Effect, Fighter, Target, TargetDecision, TargetIntent } from './types';

/** Small, central knobs for readable decisions. Slot order is never part of a score. */
export const TARGETING = {
  focusMemorySeconds: 7,
  focusMemoryBonus: 2.4,
  deterministicVariation: 0.24,
  killThreatBonus: 5.5,
  imminentCastBonus: 13,
} as const;

const clamp=(n:number,lo=0,hi=1)=>Math.min(hi,Math.max(lo,n));
const effectDamage=(effects:Effect[]=[])=>(effects.reduce((n,e)=>n+(e.kind==='damage'||e.kind==='deathnote'?e.value:e.kind==='release'?250*e.multiplier:0),0));
const positiveStatuses=new Set(['protected','regen','haste','strengthened']);
const controlStatuses=new Set(['paralyzed','rooted','slow','silenced','confused']);
const harmfulStatuses=new Set(['exposed','marked','burning','electric','weakened',...controlStatuses]);
function status(f:Fighter,id:string){return f.statuses.find(s=>s.id===id)?.intensity??0;}
function stableNoise(seed:number,turn:number,actor:string,target:string,intent:TargetIntent){
  let h=2166136261;
  for(const c of `${seed}|${turn}|${actor}|${target}|${intent}`){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}
  return ((h>>>0)/4294967295-.5)*2*TARGETING.deterministicVariation;
}

export function inferTargetIntent(actor:Fighter,rule:Target,effects:Effect[]=[]):TargetIntent {
  if(rule==='allyWeak')return effects.some(e=>e.kind==='heal')?'heal':'protect';
  if(rule==='enemyCast'||effects.some(e=>e.kind==='interrupt'))return 'interrupt';
  if(effects.some(e=>e.kind==='deathnote'))return 'finisher';
  if(effects.some(e=>e.kind==='investigate'))return 'investigate';
  if(effects.some(e=>e.kind==='heal'))return 'heal';
  if(effects.some(e=>e.kind==='shield'))return 'protect';
  const statuses=effects.filter((e):e is Extract<Effect,{kind:'status'}>=>e.kind==='status').map(e=>e.status);
  if(statuses.some(id=>positiveStatuses.has(id)))return 'buff';
  if(statuses.some(id=>harmfulStatuses.has(id)))return 'control';
  if(actor.characterId==='light'||byId[actor.characterId].tags.includes('plan'))return 'investigate';
  if(effectDamage(effects)>0)return 'offense';
  return 'offense';
}

function threat(f:Fighter){
  const c=byId[f.characterId];
  const cast=f.cast&&f.cast.duration>0?f.cast:null;
  const urgency=cast?clamp(cast.elapsed/cast.duration)*TARGETING.imminentCastBonus:0;
  const ready=f.skills.some((state,i)=>state.charge>=82&&state.cooldown<=0&&byId[f.characterId].skills[i].preparation>=2.5)?2.2:0;
  return clamp((c.power-65)/31)*3.2+urgency+ready;
}
function forecastTargets(b:Battle,ally:Fighter){
  return b.fighters.some(enemy=>enemy.side!==ally.side&&enemy.cast?.targets.includes(ally.uid));
}

function rate(b:Battle,actor:Fighter,candidate:Fighter,rule:Target,intent:TargetIntent,effects:Effect[]){
  const c=byId[candidate.characterId],ratio=clamp(candidate.hp/candidate.maxHp),missing=1-ratio;
  const expected=effectDamage(effects);
  let score=0;const reasons:string[]=[];
  const add=(name:string,value:number)=>{if(Math.abs(value)>0.01){score+=value;reasons.push(`${name} ${value>0?'+':''}${value.toFixed(1)}`);}};
  const isAlly=candidate.side===actor.side;
  if(isAlly){
    const threatened=forecastTargets(b,candidate);
    if(intent==='heal'){
      add('necessidade de recuperação',missing*9.2);
      if(ratio<.32)add('condição crítica',4.6);
      if(threatened)add('sob preparação inimiga',3.1);
      add('cura excedente',-Math.max(0,expected-candidate.maxHp*missing)/Math.max(1,candidate.maxHp)*7);
    }else if(intent==='protect'){
      add('vulnerabilidade atual',missing*5.3);
      if(ratio<.44)add('risco de incapacitação',3.5);
      if(threatened)add('ameaçado por preparação',4.5);
      const protection=status(candidate,'protected');
      const existing=candidate.shields.reduce((n,s)=>n+s.amount,0)/candidate.maxHp;
      add('já protegido',-(protection*4+existing*4));
    }else if(intent==='buff'){
      add('potencial de equipe',clamp((c.power-68)/27)*2.7);
      add('ainda precisa do reforço',Math.max(0,.55-status(candidate,'strengthened'))*2.4);
      if(threatened)add('o reforço ajuda sob ameaça',1.2);
    }else add('necessidade da equipe',missing*3);
  }else{
    add('ameaça ao trio',threat(candidate)*(intent==='interrupt'?0.45:0.85));
    add('vulnerabilidade',status(candidate,'exposed')*4+status(candidate,'marked')*3+status(candidate,'electric')*1.2);
    if(rule==='enemyWeak')add('condição baixa',(1-ratio)*2.4);
    if(rule==='enemyStrong')add('poder estimado',c.power/100*2.5);
    if(rule==='investigated')add('informação reunida',(actor.investigation[candidate.uid]??0)/100*18);
    if(intent==='finisher'||intent==='offense'){
      const shields=candidate.shields.reduce((n,s)=>n+s.amount,0);
      if(expected>0&&candidate.hp+shields<=expected)add('impacto pode incapacitar',TARGETING.killThreatBonus);
      else if(ratio<.25)add('alvo perto de cair',1.7);
    }
    if(intent==='interrupt'){
      if(candidate.cast){
        const progress=clamp(candidate.cast.elapsed/Math.max(.1,candidate.cast.duration));
        const skill=byId[candidate.characterId].skills[candidate.cast.skill];
        const castValue=skill.effects.reduce((n,e)=>n+(e.kind==='damage'?e.value:e.kind==='deathnote'?candidate.maxHp*.7:0),0);
        add('preparação ativa',9+progress*TARGETING.imminentCastBonus+clamp(castValue/candidate.maxHp)*3);
      }
      if(controlStatuses.has('paralyzed')&&status(candidate,'paralyzed')>0)add('já interrompido',-2.4);
    }
    if(intent==='control'){
      add('ameaça que vale controlar',threat(candidate)*.7);
      const control=status(candidate,'paralyzed')+status(candidate,'rooted')+status(candidate,'slow')+status(candidate,'silenced');
      add('ainda não está controlado',Math.max(0,1.2-control)*3.1);
      if(candidate.cast)add('interromperia um plano ativo',3.2);
    }
    if(intent==='investigate'){
      const information=c.deathNoteCompatible?4.8:1.5;
      add(c.deathNoteCompatible?'alvo compatível com o plano':'informação útil',information);
      add('investigação incompleta',Math.max(0,1-(actor.investigation[candidate.uid]??0)/100)*4.8);
      add('importância do alvo',threat(candidate)*.65);
    }
    if(intent==='buff')add('o reforço favorece alvo vulnerável',Math.max(0,missing)*1.2);
  }

  const memory=b.targetMemory?.[actor.uid];
  if(memory?.target===candidate.uid){
    const age=Math.max(0,b.time-memory.time);
    const continuity=TARGETING.focusMemoryBonus*clamp(1-age/TARGETING.focusMemorySeconds);
    add('foco mantido',continuity);
  }
  // Tiny seeded variation breaks exact ties without depending on fighter array or slot order.
  score+=stableNoise(b.seed,b.nextEvent,actor.characterId,candidate.characterId,intent);
  return {score,reasons};
}

export function chooseTarget(b:Battle,actor:Fighter,candidates:Fighter[],rule:Target,intent:TargetIntent,effects:Effect[]=[]):Fighter[] {
  if(!candidates.length)return [];
  const ranked=candidates.map(candidate=>({candidate,...rate(b,actor,candidate,rule,intent,effects)}))
    .sort((a,z)=>z.score-a.score||a.candidate.characterId.localeCompare(z.candidate.characterId));
  const best=ranked[0];
  b.targetMemory??={};
  b.targetMemory[actor.uid]={target:best.candidate.uid,time:b.time};
  const decision:TargetDecision={time:b.time,actor:actor.uid,intent,target:best.candidate.uid,score:best.score,reasons:best.reasons};
  b.targetLog??=[];b.targetLog.push(decision);if(b.targetLog.length>120)b.targetLog.shift();
  return [best.candidate];
}
