import { statuses } from '../data/statuses';
import type { Effect, Skill, Target, Topic, Trait, StatusId } from './types';

const n=(v:number)=>Number(v.toFixed(1)).toLocaleString('pt-BR');
const pct=(v:number)=>`${Math.round(v*100)}%`;
const secs=(v:number)=>`${n(v)} s`;
export const targetNames:Record<Target,string>={
  enemyWeak:'inimigo mais fácil de derrubar',enemyStrong:'maior ameaça',enemyCast:'inimigo preparando uma habilidade',
  investigated:'inimigo com mais Investigação',allyWeak:'aliado em maior risco',self:'o próprio personagem',
  allEnemies:'todos os inimigos',allAllies:'todo o trio',randomEnemy:'inimigo aleatório',
};
export const topicNames:Record<Topic,string>={
  time:'por segundo',action:'ao atacar',dealt:'a cada 100 de dano causado',received:'a cada 100 de dano recebido',
  allyHurt:'a cada 100 de dano sofrido por um aliado',enemyHurt:'a cada 100 de dano sofrido por um inimigo',
  interrupt:'ao interromper um Preparo',status:'quando seu trio aplica qualquer Status',
  negativeStatus:'quando seu trio aplica um Status negativo em um inimigo',
  protected:'a cada 100 de dano bloqueado',enemyCast:'quando um inimigo começa o Preparo',
  survived:'por segundo enquanto estiver na luta',losing:'por segundo enquanto seu trio estiver atrás na Vantagem',
  winning:'por segundo enquanto seu trio estiver à frente na Vantagem',
};
export const positiveStatuses=new Set<StatusId>(['protected','haste','regen','strengthened']);
export interface StatusPresentation {name:string;tone:'positivo'|'negativo';summary:string;value:string}
export function presentStatus(id:StatusId,value:number):StatusPresentation {
  const amount=Math.min(value,statuses[id].cap),percent=pct(amount),number=n(amount);
  const summary:Record<StatusId,string>={
    exposed:`Recebe +${percent} de dano`,marked:`Recebe +${percent} de dano e vira alvo preferencial`,
    slow:`Ataca e prepara habilidades ${percent} mais devagar`,rooted:`Ataca e prepara habilidades ${percent} mais devagar; acumula separadamente com Lento`,
    electric:`Recebe +${percent} de dano`,paralyzed:'Não ataca nem avança o Preparo',
    protected:`Recebe ${percent} menos dano${amount>=.3?'; Preparo não pode ser interrompido':''}`,
    haste:`Ataca e prepara habilidades ${percent} mais rápido`,confused:'25% de chance do ataque básico atingir a si mesmo',
    regen:`Recupera ${number} de Vida por segundo`,burning:`Perde ${number} de Vida por segundo`,
    silenced:'Não começa novas habilidades',strengthened:`Causa +${percent} de dano`,weakened:`Causa ${percent} menos dano`,
  };
  return {name:statuses[id].name,tone:positiveStatuses.has(id)?'positivo':'negativo',summary:summary[id],value:['regen','burning'].includes(id)?number:percent};
}
export interface SkillPresentation {summary:string;target:string;effects:string[];charge:string[];useWhen:string;preparation:string;cooldown:string}
export interface TraitPresentation {summary:string;trigger:string;frequency:string;effects:string[]}
export function presentEffect(effect:Effect,defaultTarget:Target):string {
  const target=effect.target&&effect.target!==defaultTarget?` → ${targetNames[effect.target]}`:'';
  switch(effect.kind){
    case 'damage':return `${n(effect.value)} de dano${target}`;
    case 'heal':return `+${n(effect.value)} de Vida${target}`;
    case 'shield':return `+${n(effect.value)} Escudo por até 10 s${target}`;
    case 'status':return `${statuses[effect.status].name} · ${presentStatus(effect.status,effect.value).summary} · ${secs(effect.duration)}${target}`;
    case 'interrupt':return effect.mode==='cancel'?`Interrompe o Preparo${target}`:effect.mode==='delay'?`Atrasa o Preparo em ${secs(effect.value)}${target}`:`Reduz ${pct(effect.value)} do Preparo${target}`;
    case 'shift':return `${effect.value>=0?'Adianta':'Atrasa'} ${pct(Math.abs(effect.value))} do próximo ataque${target}`;
    case 'investigate':return `+${n(effect.value)} Investigação${target}`;
    case 'deathnote':return 'Com 100 Investigação: elimina o alvo vulnerável; contra imune, 110 de dano e Exposto +55% por 14 s';
    case 'charge':return `+${n(effect.value)}% de Carga para habilidades${target}`;
    case 'store':return `Guarda ${n(effect.value)} de energia (até ${n(effect.cap)})`;
    case 'release':return `Libera energia guardada ×${n(effect.multiplier)} como dano, dividido entre inimigos vivos`;
  }
}
export function presentSkill(skill:Skill):SkillPresentation {
  const effects=skill.effects.map(effect=>presentEffect(effect,skill.target));
  const use:Record<Skill['condition'],string>={
    always:skill.target==='self'||skill.target==='allAllies'?'ficar pronta':`ficar pronta, contra ${targetNames[skill.target]}`,
    injured:'o alvo estiver com menos de 78% de Vida',
    enemyCast:'um inimigo estiver preparando uma habilidade',
    threatened:'um aliado tiver menos de 85% de Vida ou um inimigo começar o Preparo',
    investigated:'houver um alvo conhecido com 100 Investigação',
    vulnerable:'um inimigo estiver vulnerável ou sob controle',
    storedEnergy:'houver energia guardada',
  };
  return {summary:effects[0]??'Sem efeito',target:targetNames[skill.target],effects,
    charge:skill.charge.map(rule=>`+${n(rule.amount)}% ${topicNames[rule.on]}`),useWhen:use[skill.condition],
    preparation:skill.preparation>0?secs(skill.preparation):'instantâneo',cooldown:secs(skill.cooldown)};
}
export function presentTrait(trait:Trait):TraitPresentation {
  const effects=trait.effects.map(effect=>presentEffect(effect,trait.target));
  return {summary:effects[0]??'Sem efeito',trigger:topicNames[trait.on],frequency:trait.cooldown>0?`Pode ativar 1 vez a cada ${secs(trait.cooldown)}`:'Sem espera entre ativações',effects};
}
export function describeCharge(rules:Skill['charge']):string{return rules.map(rule=>`+${n(rule.amount)}% ${topicNames[rule.on]}`).join('; ')||'Sem Carga';}
export function describeEffects(effects:Effect[],target:Target):string[]{return effects.map(effect=>presentEffect(effect,target));}
export function describeSkill(skill:Skill):string{return `${targetNames[skill.target]}: ${presentSkill(skill).effects.join('; ')}`;}
export function describeSkillUse(skill:Skill):string{const p=presentSkill(skill);return `Carga: ${p.charge.join('; ')}. Usa quando: ${p.useWhen}. Preparo: ${p.preparation}. Recarga: ${p.cooldown}.`;}
export function describeTrait(trait:Trait):string{const p=presentTrait(trait);return `${p.effects.join('; ')}. Ativa ${p.trigger}. ${p.frequency}.`;}
