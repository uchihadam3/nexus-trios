import { X,HeartPulse,Clock3,Sparkles } from 'lucide-react';
import { condicaoAtendida } from '../engine/battle';
import type { Battle,Fighter,Status } from '../engine/types';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import { SkillIcon } from './Icon';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { ComTermos,TermoBotao } from './Termos';
import { termoPorId } from '../presentation/glossario';
import { StatusBadge } from './StatusBadge';
import { presentSkill,presentStatus,presentTrait,tetoDoStatus,textoDoRenascer,valorAtualDoStatus } from '../engine/skill-descriptions';

export type InspectTarget={kind:'fighter';fighter:Fighter}|{kind:'skill';fighter:Fighter;index:number}|{kind:'status';fighter:Fighter;status:Status};
export function BattleInspector({target,battle,onClose,onSelect}:{target:InspectTarget;battle:Battle;onClose:()=>void;onSelect:(target:InspectTarget)=>void}){
  const f=battle.fighters.find(fighter=>fighter.uid===target.fighter.uid)??target.fighter,c=byId[f.characterId],health=Math.max(0,Math.round(f.hp));
  const skillIndex=target.kind==='skill'?target.index:-1,skill=skillIndex>=0?c.skills[skillIndex]:undefined,presentation=skill?presentSkill(skill):null;
  const liveStatus=target.kind==='status'?f.statuses.find(status=>status.id===target.status.id)??target.status:undefined;
  const sourceName=(uid:string)=>{const source=battle.fighters.find(fighter=>fighter.uid===uid);return source?byId[source.characterId].name:'equipe';};
  return <aside className="battle-inspector" role="dialog" aria-modal="false" aria-label="Detalhes rápidos de batalha">
    <button className="inspector-close" onClick={onClose} aria-label="Fechar detalhes"><X size={17}/></button>
    {liveStatus? <>
      <div className="inspector-title"><StatusBadge status={liveStatus}/><div><small>STATUS {presentStatus(liveStatus.id,liveStatus.intensity).tone.toLocaleUpperCase('pt-BR')} · {c.name.toLocaleUpperCase('pt-BR')}</small><h3>{statuses[liveStatus.id].name}</h3></div></div>
      {/* O valor de agora, já com tudo o que foi somado, em destaque — e até onde pode chegar. */}
      {valorAtualDoStatus(liveStatus.id,liveStatus.intensity)&&<div className="inspector-valor"><b>{valorAtualDoStatus(liveStatus.id,liveStatus.intensity)}</b><span>{tetoDoStatus(liveStatus.id)?`agora · as aplicações somam até ${tetoDoStatus(liveStatus.id)}`:'agora'}</span></div>}
      <p>{presentStatus(liveStatus.id,liveStatus.intensity).summary}{liveStatus.id==='provoked'&&(()=>{const quem=battle.fighters.find(x=>x.uid===liveStatus.source);return quem?` (${byId[quem.characterId].name})`:'';})()}. <TermoBotao termo={termoPorId[liveStatus.id]!}>O que é?</TermoBotao></p>
      <div className="inspector-meta"><span><Clock3 size={13}/>{liveStatus.remaining.toLocaleString('pt-BR',{maximumFractionDigits:1})} s restantes</span><span><Sparkles size={13}/>Aplicado por {sourceName(liveStatus.source)}</span></div>
    </>:skill?<>
      <div className="inspector-title"><SkillIcon type={skill.icon} characterId={c.id} skillId={skill.id} size={31}/><div><small>{c.name.toLocaleUpperCase('pt-BR')}</small><h3>{skill.name}</h3></div></div>
      <EfeitosAgrupados grupos={presentation!.grupos}/>
      <div className="inspector-meta"><span><HeartPulse size={13}/>{Math.round(f.skills[skillIndex].charge)}% · {f.skills[skillIndex].cooldown>0?`Resfriamento ${f.skills[skillIndex].cooldown.toFixed(1)} s`:f.cast?.skill===skillIndex?'Em Preparo':f.skills[skillIndex].charge>=100?(condicaoAtendida(battle,f,skill)?'Pronta':'Pronta · esperando a regra de uso'):'Carregando'}</span><span><Clock3 size={13}/>Preparo {presentation!.preparation} · Resfriamento {presentation!.cooldown}</span></div>
      <div className="charge-explanation"><b><TermoBotao termo={termoPorId.carga!}/></b> {presentation!.charge.join(' · ')}<br/><b><TermoBotao termo={termoPorId['usa-quando']!}/></b> {presentation!.useWhen}</div>
    </>:<>
      <div className="inspector-title"><span className="inspector-avatar" style={{'--character':c.color} as React.CSSProperties}>{c.symbol}</span><div><small>{c.universe}</small><h3>{c.name}</h3></div></div>
      <div className="inspector-meta"><span><HeartPulse size={13}/>{health} de {f.maxHp} Vida</span><span><Clock3 size={13}/>{Math.max(0,100-f.action*100).toFixed(0)}% até o ataque básico</span></div>
      <p><strong>{c.trait.name}.</strong> <ComTermos texto={presentTrait(c.trait).effects.join(' · ')}/>. {presentTrait(c.trait).quando}.{c.renascer&&<> <ComTermos texto={(f.voltou?'Já renasceu nesta luta. ':'')+textoDoRenascer(c.renascer)}/>.</>}</p>
      <div className="inspector-skills">{c.skills.map((s,i)=><button key={s.id} onClick={()=>onSelect({kind:'skill',fighter:f,index:i})}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={19}/><span>{s.name}</span><small>{Math.round(f.skills[i].charge)}%</small></button>)}</div>
      {/*
        * Os Status do lutador com o valor de agora e o tempo que falta. A
        * bolinha no cartão tem 18 px e é difícil de acertar; esta lista é o
        * caminho confortável, e cada linha abre o detalhe.
        */}
      {f.statuses.length>0&&<div className="inspector-statuses">{f.statuses.map(s=>{const v=valorAtualDoStatus(s.id,s.intensity);return <button key={s.id} className="inspector-status" onClick={()=>onSelect({kind:'status',fighter:f,status:s})}><StatusBadge status={s}/><span>{statuses[s.id].name}</span>{v?<b>{v}</b>:<b/>}<small>{s.remaining.toLocaleString('pt-BR',{maximumFractionDigits:1})} s</small></button>;})}</div>}
    </>}
  </aside>;
}
