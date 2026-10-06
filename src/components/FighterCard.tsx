import { Shield,HeartPulse,Skull,Flame } from 'lucide-react';
import type { Battle,Fighter } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { Portrait } from './Portrait';
import { AuxIcon,SkillIcon } from './Icon';
import { StatusBadge } from './StatusBadge';
import type { InspectTarget } from './BattleInspector';
type ExplanationMode='normal'|'detailed'|'off';
const reasonNames:Record<string,string>={action:'Ação',dealt:'Dano causado',received:'Dano recebido',allyHurt:'Aliado ferido',enemyHurt:'Rival ferido',interrupt:'Interrupção',status:'Efeito aplicado',protected:'Proteção útil',enemyCast:'Preparação rival',survived:'Tempo sobrevivido',losing:'Desvantagem',winning:'Vantagem',trait:'Traço ativado',synergy:'Sinergia do trio'};
export function FighterCard({fighter:f,battle,beat,onInspect,numbers,threatened,explanations='normal'}:{fighter:Fighter;battle:Battle;beat:Beat|null;onInspect:(target:InspectTarget)=>void;numbers:boolean;threatened:boolean;explanations?:ExplanationMode}){
  const c=byId[f.characterId],shield=f.shields.reduce((n,s)=>n+s.amount,0);
  const source=beat?.event.source===f.uid,impacted=beat?.impacted??false;
  const hit=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='damage'):undefined;
  const helped=impacted?beat?.events.find(e=>e.target===f.uid&&['shield','block','heal','synergy'].includes(e.kind)):undefined;
  const supporting=impacted?beat?.events.find(e=>e.source===f.uid&&e.target!==f.uid&&['block','shield','heal','synergy'].includes(e.kind)):undefined;
  const broken=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='interrupt'):undefined;
  const tempo=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='tempo'):undefined;
  const acting=source&&['basic','skill'].includes(beat?.event.kind??'');
  const preparing=!!f.cast||(source&&beat?.event.kind==='cast');
  const critical=f.hp>0&&f.hp/f.maxHp<=P.criticalCondition;
  const ring=acting&&!impacted?1:f.action;
  const reasonLine=(skill:number)=>{
    const event=beat?.impacted?beat.events.find(e=>e.kind==='charge'&&e.target===f.uid&&e.skill===skill):undefined;
    if(!event||explanations==='off')return null;
    const contributor=beat?.events.find(e=>e.kind==='synergy'&&e.target===f.uid&&e.skill===skill);
    const contributorName=contributor?battle.fighters.find(fighter=>fighter.uid===contributor.source)?.characterId:undefined;
    return <span className={`charge-reason ${explanations==='detailed'?'detailed':''}`} key={`reason-${event.id}`}><b>↑ +{Math.round(event.value??0)}%</b><small>{reasonNames[event.label]??'Acontecimento'}</small>{contributorName&&<em>{byId[contributorName].name} →</em>}</span>;
  };
  return <article className={`fighter ${f.hp<=0?'incapacitated':''} ${preparing?'casting':''} ${hit?'taking-hit':''} ${acting?'acting':''} ${critical?'critical':''} ${broken?'cast-broken':''} ${helped||supporting?'receiving-help':''} ${threatened?'threatened':''} ${ring>=P.nearAction?'action-near':''} ${tempo?'tempo-changed':''}`} data-fighter={f.uid} style={{'--character':c.color} as React.CSSProperties}>
    <span className="fighter-corner corner-left"/><span className="fighter-corner corner-right"/>
    <div className="fighter-head"><span>{String(f.slot+1).padStart(2,'0')}</span><span>{f.hp<=0?<Skull size={12}/>:critical?<HeartPulse size={12}/>:shield>0?<Shield size={12}/>:null}</span></div>
    <button className="fighter-portrait" data-portrait={f.uid} onClick={()=>onInspect({kind:'fighter',fighter:f})} aria-label={`Inspecionar ${c.name}, ${Math.ceil(f.hp)} de Condição`}>
      <span className="portrait-halo"/><Portrait character={c}/>
      <svg className="action-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46" className="ring-track"/><circle cx="50" cy="50" r="46" className="ring-ticks" pathLength="100" strokeDasharray=".3 4.7"/><circle cx="50" cy="50" r="46" className="ring-progress" pathLength="100" strokeDasharray={`${Math.min(100,ring*100)} 100`}/></svg>
      {preparing&&<svg className="preparation-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" pathLength="100" strokeDasharray={`${f.cast?Math.max(0,100*f.cast.elapsed/f.cast.duration):0} 100`}/></svg>}
      {threatened&&<span className="target-brackets"/>}{broken&&<span className="broken-flash">×</span>}
      {tempo&&<span className={`tempo-mark ${tempo.value!>0?'advanced':'delayed'}`} aria-label={tempo.label}><AuxIcon id={tempo.value!>0?'tempo-up':'tempo-down'} size={20}/></span>}
      {f.hp<=0&&<span className="ko-mark"><Skull size={30}/></span>}
      {numbers&&hit&&<span key={hit.id} className="damage-number">−{Math.round(beat!.events.filter(e=>e.kind==='damage'&&e.target===f.uid).reduce((total,e)=>total+(e.value??0),0))}</span>}
      {(helped||supporting)&&<span className="help-mark">{(helped??supporting)?.kind==='heal'?<HeartPulse size={17}/>:(helped??supporting)?.kind==='synergy'?<Flame size={17}/>:<Shield size={17}/>}</span>}
    </button>
    {tempo&&<span className="tempo-reason">{tempo.label}</span>}
    <button className="fighter-name" onClick={()=>onInspect({kind:'fighter',fighter:f})}>{c.name}</button>
    <div className="condition-bar" role="progressbar" aria-label={`Condição de ${c.name}`} aria-valuenow={Math.round(f.hp)} aria-valuemax={f.maxHp} aria-valuemin={0}><div style={{width:`${100*f.hp/f.maxHp}%`}}/>{shield>0&&<span className="shield-segment" style={{width:`${Math.min(100,shield/f.maxHp*100)}%`}}/>}</div>
    <div className="condition-meta"><span>{f.hp<=0?'INCAPACITADO':critical?'CONDIÇÃO CRÍTICA':shield>0?'PROTEGIDO':'CONDIÇÃO'}</span>{numbers&&<span>{Math.ceil(f.hp)}</span>}</div>
    <div className="skill-row" aria-label={`Habilidades de ${c.name}`}>{c.skills.map((s,i)=>{
      const st=f.skills[i],casting=f.cast?.skill===i,focused=source&&beat?.event.skill===i;
      const mode=f.hp<=0?'empty':casting?'preparing':focused?(impacted?'executing':'ready'):st.cooldown>0?'cooldown':st.charge>=100?'ready':st.charge>0?'charging':'empty';
      const fill=casting?100*(f.cast!.elapsed/f.cast!.duration):st.cooldown>0?100*(1-st.cooldown/Math.max(1,s.cooldown)):st.charge;
      const label={empty:'vazia',charging:'carregando',ready:'pronta',preparing:'preparando',executing:'executando',cooldown:'em recarga'}[mode];
      return <div className="ability-wrap" key={s.id}>
        <button data-ability={`${f.uid}-${i}`} className={`ability ${mode}`} onClick={()=>onInspect({kind:'skill',fighter:f,index:i})} aria-label={`${s.name}: ${label}. Toque para explicar`} title={`${s.name} · ${label}`}>
          <div className="ability-fill" style={{height:`${Math.max(0,Math.min(100,fill))}%`}}/>
          <SkillIcon type={s.icon} size={20} characterId={c.id} skillId={s.id}/>
          <svg className="ability-meter" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="9" pathLength="100" strokeDasharray={`${Math.max(0,Math.min(100,fill))} 100`}/></svg>
          {mode==='cooldown'&&<AuxIcon id="cooldown" size={13} className="cooldown-lock"/>} {mode==='ready'&&<AuxIcon id="ready" size={13} className="ready-dot"/>}
        </button>
        {reasonLine(i)}
      </div>;
    })}</div>
    <div className="status-row" aria-label={`Efeitos ativos em ${c.name}`}>{f.statuses.map(s=><StatusBadge key={s.id} status={s} onClick={()=>onInspect({kind:'status',fighter:f,status:s})}/>)}</div>
    {preparing&&<div className="cast-label"><AuxIcon id="preparing" size={15}/>{f.cast?c.skills[f.cast.skill].name:beat?.event.label}</div>}
    {broken&&<div className="interrupt-label"><AuxIcon id="interrupt" size={14}/>{broken.label.includes('atrasada')?'ATRASADO':'INTERROMPIDO'}</div>}
  </article>;
}
