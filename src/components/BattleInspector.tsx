import { X,HeartPulse,Clock3,Sparkles } from 'lucide-react';
import type { Battle,Fighter,Status } from '../engine/types';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import { SkillIcon } from './Icon';
import { StatusBadge } from './StatusBadge';
import { describeSkill,describeSkillUse } from '../engine/skill-descriptions';

export type InspectTarget={kind:'fighter';fighter:Fighter}|{kind:'skill';fighter:Fighter;index:number}|{kind:'status';fighter:Fighter;status:Status};
export function BattleInspector({target,battle,onClose,onSelect}:{target:InspectTarget;battle:Battle;onClose:()=>void;onSelect:(target:InspectTarget)=>void}){
  const f=battle.fighters.find(fighter=>fighter.uid===target.fighter.uid)??target.fighter,c=byId[f.characterId],health=Math.max(0,Math.round(f.hp));
  const skillIndex=target.kind==='skill'?target.index:-1,skill=skillIndex>=0?c.skills[skillIndex]:undefined;
  const liveStatus=target.kind==='status'?f.statuses.find(status=>status.id===target.status.id)??target.status:undefined;
  const sourceName=(uid:string)=>{const source=battle.fighters.find(fighter=>fighter.uid===uid);return source?byId[source.characterId].name:'equipe';};
  return <aside className="battle-inspector" role="dialog" aria-modal="false" aria-label="Detalhes rápidos de batalha">
    <button className="inspector-close" onClick={onClose} aria-label="Fechar detalhes"><X size={17}/></button>
    {liveStatus? <>
      <div className="inspector-title"><StatusBadge status={liveStatus} onClick={()=>{}}/><div><small>EFEITO ATIVO</small><h3>{statuses[liveStatus.id].name}</h3></div></div>
      <p>{statuses[liveStatus.id].description}</p>
      <div className="inspector-meta"><span><Clock3 size={13}/>{liveStatus.remaining.toLocaleString('pt-BR',{maximumFractionDigits:1})} s restantes</span><span><Sparkles size={13}/>Aplicado por {sourceName(liveStatus.source)}</span></div>
    </>:skill?<>
      <div className="inspector-title"><SkillIcon type={skill.icon} characterId={c.id} skillId={skill.id} size={31}/><div><small>{c.name.toLocaleUpperCase('pt-BR')}</small><h3>{skill.name}</h3></div></div>
      <p>{describeSkill(skill)}</p>
      <div className="inspector-meta"><span><HeartPulse size={13}/>{Math.round(f.skills[skillIndex].charge)}% · {f.skills[skillIndex].cooldown>0?`recarga ${f.skills[skillIndex].cooldown.toFixed(1)} s`:f.cast?.skill===skillIndex?'em preparação':f.skills[skillIndex].charge>=100?'pronta':'carregando'}</span><span><Clock3 size={13}/>{skill.cooldown>0?`${skill.cooldown} s de recarga`:'Sem recarga'}</span></div>
      <div className="charge-explanation">{describeSkillUse(skill)}</div>
    </>:<>
      <div className="inspector-title"><span className="inspector-avatar" style={{'--character':c.color} as React.CSSProperties}>{c.symbol}</span><div><small>{c.universe}</small><h3>{c.name}</h3></div></div>
      <div className="inspector-meta"><span><HeartPulse size={13}/>{health} de {f.maxHp} Condição</span><span><Clock3 size={13}/>{Math.max(0,100-f.action*100).toFixed(0)}% até agir</span></div>
      <p><strong>{c.trait.name}.</strong> {c.trait.description}</p>
      <div className="inspector-skills">{c.skills.map((s,i)=><button key={s.id} onClick={()=>onSelect({kind:'skill',fighter:f,index:i})}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={19}/><span>{s.name}</span><small>{Math.round(f.skills[i].charge)}%</small></button>)}</div>
      {f.statuses.length>0&&<div className="inspector-statuses">{f.statuses.map(s=><div key={s.id}><StatusBadge status={s} onClick={()=>onSelect({kind:'status',fighter:f,status:s})}/><span>{statuses[s.id].name}</span></div>)}</div>}
    </>}
  </aside>;
}
