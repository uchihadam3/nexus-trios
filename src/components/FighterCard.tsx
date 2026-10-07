import { Shield,HeartPulse,Skull } from 'lucide-react';
import type { Battle,Fighter } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { Portrait } from './Portrait';
import { AuxIcon,SkillIcon } from './Icon';
import { StatusBadge } from './StatusBadge';
import type { InspectTarget } from './BattleInspector';
export function FighterCard({fighter:f,battle,beat,onInspect,numbers,threatened,linkedSource=false,linkedTarget=false}:{fighter:Fighter;battle:Battle;beat:Beat|null;onInspect:(target:InspectTarget)=>void;numbers:boolean;threatened:boolean;linkedSource?:boolean;linkedTarget?:boolean}){
  const c=byId[f.characterId],shield=f.shields.reduce((n,s)=>n+s.amount,0);
  const source=beat?.event.source===f.uid,impacted=beat?.impacted??false;
  const hit=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='damage'):undefined;
  const shielded=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='shield'&&e.label==='Escudo'):undefined;
  const blocked=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='block'&&(e.value??0)>=40):undefined;
  const applied=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='status'):undefined;
  const discovered=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='discovery'):undefined;
  const knocked=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='ko'):undefined;
  const broken=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='interrupt'):undefined;
  const tempo=impacted?beat?.events.find(e=>e.target===f.uid&&e.kind==='tempo'):undefined;
  const acting=source&&['basic','skill'].includes(beat?.event.kind??'');
  const preparing=!!f.cast||(source&&beat?.event.kind==='cast');
  const critical=f.hp>0&&f.hp/f.maxHp<=P.criticalCondition;
  const ring=acting&&!impacted?1:f.action;
  const light=battle.fighters.find(actor=>actor.side!==f.side&&actor.characterId==='light');
  const knowledge=light?.discovered?.[f.uid];
  const advantageSide=battle.dominion>3?'player':battle.dominion< -3?'enemy':null;
  const advantageRule=advantageSide===f.side?'winning':advantageSide?'losing':null;
  const advantageActive=!!advantageRule&&c.skills.some(skill=>skill.charge.some(rule=>rule.on===advantageRule));
  const damage=impacted?beat?.events.filter(e=>e.kind==='damage'&&e.target===f.uid).reduce((total,e)=>total+(e.value??0),0)??0:0;
  const healing=impacted?beat?.events.filter(e=>e.kind==='heal'&&e.target===f.uid).reduce((total,e)=>total+(e.value??0),0)??0:0;
  const blockValue=impacted?beat?.events.filter(e=>e.kind==='block'&&e.target===f.uid).reduce((total,e)=>total+(e.value??0),0)??0:0;
  const basicStyle=source&&beat?.event.kind==='basic'?`basic-${beat.family}`:'';
  return <article className={`fighter ${f.hp<=0?'incapacitated':''} ${preparing?'casting':''} ${hit?'taking-hit':''} ${acting?'acting':''} ${basicStyle} ${critical?'critical':''} ${shielded||blocked?'receiving-help':''} ${linkedSource?'link-source':''} ${linkedTarget?'link-target':''} ${knocked?'newly-out':''} ${broken?'cast-broken':''} ${threatened?'threatened':''} ${ring>=P.nearAction?'action-near':''} ${tempo?'tempo-changed':''}`} data-fighter={f.uid} data-combat-role={linkedSource&&linkedTarget?'both':linkedSource?'source':linkedTarget?'target':'idle'} style={{'--character':c.color} as React.CSSProperties}>
    <span className="fighter-corner corner-left"/><span className="fighter-corner corner-right"/>
    <div className="fighter-head"><span>{String(f.slot+1).padStart(2,'0')}</span><span>{f.hp<=0?<Skull size={12}/>:advantageActive?<AuxIcon id="domain" size={13} className="advantage-active"/>:critical?<HeartPulse size={12}/>:shield>0?<Shield size={12}/>:null}</span></div>
    <button className="fighter-portrait" data-portrait={f.uid} onClick={()=>onInspect({kind:'fighter',fighter:f})} aria-label={`Inspecionar ${c.name}, ${Math.ceil(f.hp)} de Vida`}>
      <span className="portrait-halo"/><Portrait character={c}/>
      <svg className="action-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46" className="ring-track"/><circle cx="50" cy="50" r="46" className="ring-ticks" pathLength="100" strokeDasharray=".3 4.7"/><circle cx="50" cy="50" r="46" className="ring-progress" pathLength="100" strokeDasharray={`${Math.min(100,ring*100)} 100`}/></svg>
      {preparing&&<svg className="preparation-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" pathLength="100" strokeDasharray={`${f.cast?Math.max(0,100*f.cast.elapsed/f.cast.duration):0} 100`}/></svg>}
      {threatened&&<span className="target-brackets"/>}{broken&&<span className="broken-flash">×</span>}
      {tempo&&<span className={`tempo-mark ${tempo.value!>0?'advanced':'delayed'}`} aria-label={tempo.label}><AuxIcon id={tempo.value!>0?'tempo-up':'tempo-down'} size={20}/></span>}
      {f.hp<=0&&<span className="ko-mark" aria-label="Fora da luta"><Skull size={22}/></span>}
      {impacted&&<span className="combat-feedback" key={beat?.event.id}>
        {numbers&&damage>0&&<span className="damage-number">−{Math.round(damage)}</span>}
        {numbers&&healing>0&&<span className="damage-number heal-number"><HeartPulse size={13}/>+{Math.round(healing)}</span>}
        {numbers&&shielded&&<span className="damage-number shield-number"><Shield size={12}/>+{Math.round(shielded.value??0)}</span>}
        {numbers&&blockValue>0&&<span className="damage-number shield-number"><Shield size={12}/>{Math.round(blockValue)} bloqueado</span>}
      </span>}
      {applied&&<span key={applied.id} className="status-pop">{applied.status&&<img src={`/assets/statuses/${applied.status}.png`} alt=""/>}{applied.label}</span>}
      {discovered&&<span key={discovered.id} className="discovery-pop">{discovered.label}</span>}
    </button>
    {tempo&&<span className="tempo-reason">{tempo.label}</span>}
    <button className="fighter-name" onClick={()=>onInspect({kind:'fighter',fighter:f})}>{c.name}</button>
    <div className="condition-bar" role="progressbar" aria-label={`Vida de ${c.name}`} aria-valuenow={Math.round(f.hp)} aria-valuemax={f.maxHp} aria-valuemin={0}><div style={{width:`${100*f.hp/f.maxHp}%`}}/>{shield>0&&<span className="shield-segment" style={{width:`${Math.min(100,shield/f.maxHp*100)}%`}}/>}</div>
    <div className="condition-meta"><span>{f.hp<=0?'FORA DA LUTA':critical?'⚠ VIDA BAIXA':shield>0?`ESCUDO ${Math.ceil(shield)}`:'VIDA'}</span>{numbers&&<span>{Math.ceil(f.hp)}</span>}</div>
    {knowledge&&<span className={`light-knowledge ${knowledge}`}>{knowledge==='vulnerable'?'Vulnerável à Death Note':'Imune à execução'}</span>}
    <div className="skill-row" aria-label={`Habilidades de ${c.name}`}>{c.skills.map((s,i)=>{
      const st=f.skills[i],casting=f.cast?.skill===i,focused=source&&beat?.event.skill===i;
      const ready=impacted&&beat?.events.some(e=>e.source===f.uid&&e.kind==='ready'&&e.skill===i);
      const assisted=impacted&&beat?.events.some(e=>e.target===f.uid&&e.source!==f.uid&&e.kind==='charge'&&e.skill===i);
      const mode=f.hp<=0?'empty':casting?'preparing':focused?(impacted?'executing':'ready'):st.cooldown>0?'cooldown':st.charge>=100?'ready':st.charge>0?'charging':'empty';
      const fill=casting?100*(f.cast!.elapsed/f.cast!.duration):st.cooldown>0?100*(1-st.cooldown/Math.max(1,s.cooldown)):st.charge;
      const label={empty:'vazia',charging:'carregando',ready:'pronta',preparing:'preparando',executing:'executando',cooldown:'em recarga'}[mode];
      return <div className={`ability-wrap ${assisted?'ability-assisted':''}`} key={s.id}>
        <button data-ability={`${f.uid}-${i}`} className={`ability ${mode}`} onClick={()=>onInspect({kind:'skill',fighter:f,index:i})} aria-label={`${s.name}: ${label}. Toque para explicar`} title={`${s.name} · ${label}`}>
          <div className="ability-fill" style={{height:`${Math.max(0,Math.min(100,fill))}%`}}/>
          <SkillIcon type={s.icon} size={20} characterId={c.id} skillId={s.id}/>
          <svg className="ability-meter" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="9" pathLength="100" strokeDasharray={`${Math.max(0,Math.min(100,fill))} 100`}/></svg>
          {mode==='cooldown'&&<AuxIcon id="cooldown" size={13} className="cooldown-lock"/>} {mode==='ready'&&<AuxIcon id="ready" size={13} className="ready-dot"/>}
        </button>
        {ready&&<span className="ability-ready-label">PRONTA</span>}
      </div>;
    })}</div>
    <div className="status-row" aria-label={`Efeitos ativos em ${c.name}`}>{f.statuses.map(s=><StatusBadge key={s.id} status={s} onClick={()=>onInspect({kind:'status',fighter:f,status:s})}/>)}</div>
    {preparing&&<div className="cast-label"><AuxIcon id="preparing" size={15}/>{f.cast?c.skills[f.cast.skill].name:beat?.event.label}</div>}
    {broken&&<div className="interrupt-label"><AuxIcon id="interrupt" size={14}/>{broken.label.includes('atrasada')?'ATRASADO':'INTERROMPIDO'}</div>}
  </article>;
}
