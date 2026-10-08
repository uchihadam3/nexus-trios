import { Shield,HeartPulse,Skull } from 'lucide-react';
import type { Battle,Fighter,Status } from '../engine/types';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import { Portrait } from './Portrait';
import { AuxIcon,SkillIcon } from './Icon';
import { StatusBadge } from './StatusBadge';
import type { InspectTarget } from './BattleInspector';
import type { UnitActing } from '../presentation/acting';

/*
 * Um lutador na arena.
 *
 * Não é um cartão: é uma unidade de pé no chão da arena. O medalhão com o
 * círculo do ataque fica do lado de dentro, virado para o centro, onde as
 * trajetórias passam; as informações ficam do lado de fora. Buffs e debuffs
 * têm linhas próprias, para que "o que ajuda" e "o que atrapalha" nunca se
 * misturem.
 */

/* Quantos Status cabem numa linha antes de virar "+N". */
const POR_LINHA=4;

function LinhaDeStatus({tipo,lista,fighter,onInspect}:{tipo:'buffs'|'debuffs';lista:Status[];fighter:Fighter;onInspect:(t:InspectTarget)=>void}){
  const visiveis=lista.slice(0,POR_LINHA),resto=lista.length-visiveis.length;
  return <div className={`status-line ${tipo} ${lista.length?'':'is-empty'}`} aria-label={tipo==='buffs'?'Efeitos que ajudam':'Efeitos que atrapalham'}>
    {visiveis.map(s=><StatusBadge key={s.id} status={s} onClick={()=>onInspect({kind:'status',fighter,status:s})}/>)}
    {resto>0&&<button className="status-more" onClick={()=>onInspect({kind:'fighter',fighter})} aria-label={`Mais ${resto} efeitos`}>+{resto}</button>}
  </div>;
}

export function ArenaUnit({fighter:f,battle,beat,onInspect,numbers,threatened,linkedSource=false,linkedTarget=false,atuacao}:{fighter:Fighter;battle:Battle;beat:Beat|null;onInspect:(target:InspectTarget)=>void;numbers:boolean;threatened:boolean;linkedSource?:boolean;linkedTarget?:boolean;atuacao?:UnitActing}){
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
  const out=f.hp<=0,critical=!out&&f.hp/f.maxHp<=P.criticalCondition;
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
  const buffs=f.statuses.filter(s=>statuses[s.id].tone!=='negativo'),debuffs=f.statuses.filter(s=>statuses[s.id].tone==='negativo');
  const hpPct=Math.max(0,Math.min(100,100*f.hp/f.maxHp)),shieldPct=Math.min(100-hpPct,100*shield/f.maxHp);
  const marcas=[
    out&&'is-out',preparing&&'is-casting',hit&&'is-hit',acting&&'is-acting',basicStyle,critical&&'is-critical',
    (shielded||blocked)&&'is-helped',linkedSource&&'is-source',linkedTarget&&'is-target',knocked&&'is-newly-out',
    broken&&'is-broken',threatened&&'is-threatened',ring>=P.nearAction&&'is-near',tempo&&'is-tempo',
  ].filter(Boolean).join(' ');
  /* A atuação deste beat: estilo de quem age, reação de quem recebe, e para onde. */
  const atua=atuacao?[atuacao.act&&`actor act-${atuacao.act} act-${atuacao.parity}`,atuacao.react&&`reactor react-${atuacao.react}`].filter(Boolean).join(' '):'';
  const atuaStyle:Record<string,string>=atuacao?{'--act-dx':`${atuacao.dx.toFixed(1)}px`,'--act-dy':`${atuacao.dy.toFixed(1)}px`,'--act-ux':atuacao.ux.toFixed(3),'--act-uy':atuacao.uy.toFixed(3),'--beat-s':`${atuacao.seconds}s`,'--act-angle':`${(Math.atan2(atuacao.uy,atuacao.ux)*180/Math.PI).toFixed(1)}deg`}:{};
  return <article className={`unit side-${f.side} ${marcas} ${atua}`} data-fighter={f.uid} data-slot={f.slot} data-combat-role={linkedSource&&linkedTarget?'both':linkedSource?'source':linkedTarget?'target':'idle'} style={{'--character':c.color,...atuaStyle} as React.CSSProperties}>
    <div className="unit-medal">
      <span className="unit-fx" aria-hidden="true"/>
      <span className="unit-pedestal" aria-hidden="true"/>
      <button className="fighter-portrait" data-portrait={f.uid} onClick={()=>onInspect({kind:'fighter',fighter:f})} aria-label={`Inspecionar ${c.name}, ${Math.ceil(f.hp)} de Vida`}>
        <span className="medal-aura" aria-hidden="true"/>
        <span className="medal-frame"><Portrait character={c}/></span>
        <svg className="attack-ring" viewBox="0 0 100 100" aria-hidden="true">
          <circle cx="50" cy="50" r="47" className="attack-ring-track"/>
          <circle cx="50" cy="50" r="47" className="attack-ring-ticks" pathLength="100" strokeDasharray=".4 9.6"/>
          <circle cx="50" cy="50" r="47" className="attack-ring-fill" pathLength="100" strokeDasharray={`${Math.min(100,ring*100)} 100`}/>
        </svg>
        {preparing&&<svg className="prep-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="41" pathLength="100" strokeDasharray={`${f.cast?Math.max(0,100*f.cast.elapsed/f.cast.duration):0} 100`}/></svg>}
        {threatened&&<span className="unit-brackets" aria-hidden="true"/>}
        {broken&&<span className="unit-break" aria-hidden="true">×</span>}
        {tempo&&<span className={`unit-tempo ${tempo.value!>0?'advanced':'delayed'}`} aria-label={tempo.label}><AuxIcon id={tempo.value!>0?'tempo-up':'tempo-down'} size={18}/></span>}
        {out&&<span className="unit-ko" aria-label="Fora da luta"><Skull size={26}/><b>FORA</b></span>}
        {impacted&&<span className="combat-feedback" key={beat?.event.id}>
          {numbers&&damage>0&&<span className="damage-number">−{Math.round(damage)}</span>}
          {numbers&&healing>0&&<span className="damage-number heal-number"><HeartPulse size={13}/>+{Math.round(healing)}</span>}
          {numbers&&shielded&&<span className="damage-number shield-number"><Shield size={12}/>+{Math.round(shielded.value??0)}</span>}
          {numbers&&blockValue>0&&<span className="damage-number shield-number"><Shield size={12}/>{Math.round(blockValue)} bloqueado</span>}
        </span>}
        {applied&&<span key={applied.id} className="status-pop">{applied.status&&<img src={`/assets/statuses/${applied.status}.png`} alt=""/>}{applied.label}</span>}
        {discovered&&<span key={discovered.id} className="discovery-pop">{discovered.label}</span>}
      </button>
      {(out||advantageActive||critical||shield>0)&&<span className={`unit-flag ${out?'flag-out':advantageActive?'flag-advantage':critical?'flag-critical':'flag-shield'}`} aria-hidden="true">{out?<Skull size={12}/>:advantageActive?<AuxIcon id="domain" size={13}/>:critical?<HeartPulse size={12}/>:<Shield size={12}/>}</span>}
      {preparing&&<div className="unit-cast"><AuxIcon id="preparing" size={13}/><span>{f.cast?c.skills[f.cast.skill].name:beat?.event.label}</span></div>}
      {broken&&<div className="unit-interrupt"><AuxIcon id="interrupt" size={13}/>{broken.label.includes('atrasada')?'ATRASADO':'INTERROMPIDO'}</div>}
      {tempo&&<span className="unit-tempo-reason">{tempo.label}</span>}
    </div>
    <div className="unit-name"><button className="fighter-name" onClick={()=>onInspect({kind:'fighter',fighter:f})}>{c.name}</button></div>
    <div className="unit-vitals">
      <div className="unit-bar" role="progressbar" aria-label={`Vida de ${c.name}`} aria-valuenow={Math.round(f.hp)} aria-valuemax={f.maxHp} aria-valuemin={0}>
        <span className="unit-bar-hp" style={{width:`${hpPct}%`}}/>
        {shieldPct>0&&<span className="unit-bar-shield" style={{left:`${hpPct}%`,width:`${shieldPct}%`}}/>}
      </div>
      <div className="unit-meta"><span>{out?'FORA DA LUTA':critical?'VIDA BAIXA':shield>0?<><Shield size={9}/>{Math.ceil(shield)}</>:'VIDA'}</span>{numbers&&!out&&<b>{Math.ceil(f.hp)}</b>}</div>
      {knowledge&&<span className={`light-knowledge ${knowledge}`}>{knowledge==='vulnerable'?'Vulnerável à Death Note':'Imune à execução'}</span>}
    </div>
    <div className="unit-skills" aria-label={`Habilidades de ${c.name}`}>{c.skills.map((s,i)=>{
      const st=f.skills[i],casting=f.cast?.skill===i,focused=source&&beat?.event.skill===i;
      const ready=impacted&&beat?.events.some(e=>e.source===f.uid&&e.kind==='ready'&&e.skill===i);
      const assisted=impacted&&beat?.events.some(e=>e.target===f.uid&&e.source!==f.uid&&e.kind==='charge'&&e.skill===i);
      const mode=out?'empty':casting?'preparing':focused?(impacted?'executing':'ready'):st.cooldown>0?'cooldown':st.charge>=100?'ready':st.charge>0?'charging':'empty';
      const fill=casting?100*(f.cast!.elapsed/f.cast!.duration):st.cooldown>0?100*(1-st.cooldown/Math.max(1,s.cooldown)):st.charge;
      const label={empty:'vazia',charging:'carregando',ready:'pronta',preparing:'preparando',executing:'executando',cooldown:'em recarga'}[mode];
      return <div className={`ability-wrap ${assisted?'ability-assisted':''} ${ready?'just-ready':''}`} key={s.id}>
        <button data-ability={`${f.uid}-${i}`} className={`ability ${mode}`} onClick={()=>onInspect({kind:'skill',fighter:f,index:i})} aria-label={`${s.name}: ${label}. Toque para explicar`} title={`${s.name} · ${label}`}>
          <span className="ability-fill" style={{height:`${Math.max(0,Math.min(100,fill))}%`}}/>
          <SkillIcon type={s.icon} size={20} characterId={c.id} skillId={s.id}/>
          <svg className="ability-meter" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="10" pathLength="100" strokeDasharray={`${Math.max(0,Math.min(100,fill))} 100`}/></svg>
          {mode==='cooldown'&&<AuxIcon id="cooldown" size={12} className="ability-lock"/>}
        </button>
      </div>;
    })}</div>
    <div className="unit-statuses">
      <LinhaDeStatus tipo="buffs" lista={buffs} fighter={f} onInspect={onInspect}/>
      <LinhaDeStatus tipo="debuffs" lista={debuffs} fighter={f} onInspect={onInspect}/>
    </div>
  </article>;
}
