import { statuses } from '../data/statuses';
import type { Effect, Skill, Target, Topic, Trait } from './types';

const n=(value:number)=>Number(value.toFixed(1)).toLocaleString('pt-BR');
const percent=(value:number)=>`${Math.round(value*100)}%`;
const seconds=(value:number)=>`${n(value)} s`;
const targets:Record<Target,string>={
  enemyWeak:'o inimigo mais vulnerável',enemyStrong:'o inimigo de maior poder',enemyCast:'um inimigo que esteja preparando uma habilidade',
  investigated:'um inimigo investigado',allyWeak:'o aliado mais ferido',self:'a si mesmo',allEnemies:'todos os inimigos',
  allAllies:'todos os aliados',randomEnemy:'um inimigo aleatório',
};
const topicLabels:Record<Topic,string>={
  time:'por segundo',action:'a cada ação própria',dealt:'a cada 100 de dano causado',received:'a cada 100 de dano recebido',
  allyHurt:'a cada 100 de dano sofrido por um aliado',enemyHurt:'a cada 100 de dano sofrido por um inimigo',
  interrupt:'quando interrompe uma preparação',status:'quando aplica um estado',protected:'a cada 100 de dano realmente bloqueado',
  enemyCast:'quando um inimigo começa uma preparação',survived:'por segundo enquanto permanece ativo',
  losing:'por segundo enquanto seu trio está atrás no Domínio',winning:'por segundo enquanto seu trio lidera o Domínio',
};
export function describeCharge(rules:Skill['charge']):string{
  if(!rules.length)return 'não carrega';
  return rules.map(rule=>`+${n(rule.amount)} ${topicLabels[rule.on]}`).join('; ');
}
function statusEffect(effect:Extract<Effect,{kind:'status'}>):string{
  const def=statuses[effect.status],amount=effect.value,duration=seconds(effect.duration);
  const amountText=effect.status==='burning'||effect.status==='regen'
    ?`${n(amount)} de Condição por segundo`
    :`${percent(amount)}`;
  const mechanics:Record<string,string>={
    exposed:`recebe ${amountText} a mais de dano`,
    marked:`recebe ${amountText} a mais de dano e ganha prioridade como alvo`,
    paralyzed:'não age nem avança preparações',
    protected:`reduz o dano recebido em ${amountText}; com 30% ou mais, também resiste a interrupções`,
    slow:`ações e preparações avançam ${amountText} mais devagar`,
    haste:`ações e preparações avançam ${amountText} mais rápido`,
    rooted:`ações e preparações avançam ${amountText} mais devagar`,
    confused:'tem 25% de chance de a ação normal atingir a si mesmo',
    regen:`recupera ${amountText}`,
    burning:`perde ${amountText}`,
    electric:`recebe ${amountText} a mais de dano`,
    silenced:'não inicia habilidades; preparações já iniciadas continuam',
    strengthened:`causa ${amountText} a mais de dano`,
    weakened:`causa ${amountText} a menos de dano`,
  };
  const cap=def.cap;
  return `Aplica ${def.name} em ${targets[effect.target??'enemyWeak']} por ${duration}: ${mechanics[effect.status]??def.description}.${amount>cap?' O efeito é limitado ao teto do estado ('+${percent(cap)}).':''}`;
}
export function describeEffects(effects:Effect[],defaultTarget:Target):string[]{
  return effects.map(effect=>{
    const target=targets[effect.target??defaultTarget];
    switch(effect.kind){
      case 'damage':return `Causa ${n(effect.value)} de dano base a ${target}.`;
      case 'heal':return `Recupera ${n(effect.value)} de Condição de ${target}.`;
      case 'shield':return `Concede ${n(effect.value)} de Escudo a ${target}, por até 10 s; o Escudo total não passa de 55% da Condição máxima.`;
      case 'status':return statusEffect(effect);
      case 'interrupt':
        if(effect.mode==='cancel')return `Cancela a preparação de ${target}; o alvo fica com 25 de carga e 2 s de recarga.`;
        if(effect.mode==='delay')return `Atrasa em ${seconds(effect.value)} a preparação em andamento de ${target}, até o limite de 2 s.`;
        return `Reduz em ${percent(effect.value)} o progresso atual da preparação de ${target}.`;
      case 'shift':return effect.value>=0?`Adianta em ${percent(effect.value)} o medidor da próxima ação de ${target}.`:`Atrasa em ${percent(-effect.value)} o medidor da próxima ação de ${target}.`;
      case 'investigate':return `Acrescenta ${n(effect.value)} pontos de investigação contra ${target}, até 100; a sentença só fica disponível com investigação completa.`;
      case 'deathnote':return `Com 100 pontos de investigação, incapacita imediatamente um alvo compatível. Contra os demais, aplica 55% de Exposto por 14 s e causa 110 de dano.`;
      case 'charge':return `Concede ${n(effect.value)} de carga às habilidades disponíveis de ${target}.`;
      case 'store':return `Armazena ${n(effect.value)} de energia cinética, até o limite de ${n(effect.cap)}.`;
      case 'release':return `Libera a energia armazenada multiplicada por ${n(effect.multiplier)} como dano, dividida entre os alvos vivos.`;
    }
  });
}
export function describeSkill(skill:Skill):string{
  const effects=describeEffects(skill.effects,skill.target);
  return effects.length?effects.join(' '):'Não produz efeito mecânico.';
}
export function describeSkillUse(skill:Skill):string{
  const condition:Record<Skill['condition'],string>={
    always:'quando estiver pronta e houver um alvo válido',injured:'quando o alvo estiver abaixo de 78% de Condição',
    enemyCast:'quando um inimigo estiver preparando uma habilidade',threatened:'quando um aliado estiver ferido ou um inimigo estiver preparando uma habilidade',
    investigated:'quando houver um inimigo com investigação completa',vulnerable:'quando houver um inimigo vulnerável ou sob controle',
    storedEnergy:'quando houver energia armazenada',
  };
  const preparation=skill.preparation>0?seconds(skill.preparation):'instantânea';
  return `Carga: ${describeCharge(skill.charge)}. Condição de uso: ${condition[skill.condition]}. Preparação: ${preparation}. Recarga: ${seconds(skill.cooldown)}.`;
}
export function describeTrait(trait:Trait):string{
  const effects=describeEffects(trait.effects,trait.target);
  return `${effects.join(' ')} Ativa: ${topicLabels[trait.on]??trait.on}. Recarga interna: ${seconds(trait.cooldown)}.`;
}
