import { useEffect,useRef,useState } from 'react';
import { Flame,Hourglass,Shield,HeartPulse,Skull,Zap } from 'lucide-react';
import { condicaoAtendida } from '../engine/battle';
import type { Battle,Fighter,Status } from '../engine/types';
import { passoAtual,revelado,type Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { folha } from '../presentation/vfxProfiles';
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

/*
 * A vida de um Status na arena (adendo, parte 4).
 *
 * Entrada: o nome curto aparece no medalhão (status-pop) e o ícone chega na
 * linha com um brilho — depois fica só o ícone (a animação roda uma vez, quando
 * o ícone nasce).
 * Renovação: um pulso discreto no anel, no máximo um a cada 1,5 s, para que um
 * Status reaplicado a cada golpe não vire pisca-pisca.
 * Saída: se o tempo acabou, some num fade; se saiu antes da hora (dissipado),
 * o ícone se parte num anel. O ícone que sai fica 0,6 s na tela para isso.
 */
type Saindo={s:Status;modo:'expirou'|'dissipado';chave:number};
function LinhaDeStatus({tipo,lista,fighter,onInspect}:{tipo:'buffs'|'debuffs';lista:Status[];fighter:Fighter;onInspect:(t:InspectTarget)=>void}){
  const visiveis=lista.slice(0,POR_LINHA),resto=lista.length-visiveis.length;
  const antes=useRef(new Map<string,Status>()),pulsos=useRef(new Map<string,{n:number;em:number}>());
  const [saindo,setSaindo]=useState<Saindo[]>([]);
  const vivo=fighter.hp>0;
  const agora=performance.now();
  for(const s of lista){
    const velho=antes.current.get(s.id),p=pulsos.current.get(s.id)??{n:0,em:0};
    if(velho&&(s.remaining>velho.remaining+.4||s.intensity>velho.intensity+1e-6)&&agora-p.em>1500)pulsos.current.set(s.id,{n:p.n+1,em:agora});
  }
  useEffect(()=>{
    const atuais=new Set(lista.map(s=>s.id)),novos:Saindo[]=[];
    if(vivo)for(const velho of antes.current.values())if(!atuais.has(velho.id))novos.push({s:velho,modo:velho.remaining>.35?'dissipado':'expirou',chave:performance.now()+Math.random()});
    antes.current=new Map(lista.map(s=>[s.id,{...s}]));
    if(novos.length){
      setSaindo(x=>[...x.filter(y=>!atuais.has(y.s.id)),...novos]);
      const t=setTimeout(()=>setSaindo(x=>x.filter(y=>!novos.includes(y))),650);
      return ()=>clearTimeout(t);
    }
    return undefined;
  },[lista,vivo]);
  const temAlgo=lista.length>0||saindo.length>0;
  return <div className={`status-line ${tipo} ${temAlgo?'':'is-empty'}`} aria-label={tipo==='buffs'?'Efeitos que ajudam':'Efeitos que atrapalham'}>
    {visiveis.map(s=>{const pulso=pulsos.current.get(s.id)?.n??0;return <span key={s.id} className="status-vida">
      <StatusBadge status={s} onClick={()=>onInspect({kind:'status',fighter,status:s})}/>
      {pulso>0&&<span key={pulso} className="status-renovado" aria-hidden/>}
    </span>;})}
    {/* quem está saindo só usa vaga livre: a linha nunca passa de POR_LINHA ícones (antes ela alargava e os ícones vazavam para fora) */}
    {saindo.filter(x=>!lista.some(s=>s.id===x.s.id)).slice(0,Math.max(0,POR_LINHA-visiveis.length)).map(x=><span key={x.chave} className={`status-vida status-saindo ${x.modo}`} aria-hidden><StatusBadge status={x.s}/></span>)}
    {resto>0&&<button className="status-more" onClick={()=>onInspect({kind:'fighter',fighter})} aria-label={`Mais ${resto} efeitos`}>+{resto}</button>}
  </div>;
}

export function ArenaUnit({fighter:f,battle,beat,onInspect,numbers,threatened,linkedSource=false,linkedTarget=false,atuacao}:{fighter:Fighter;battle:Battle;beat:Beat|null;onInspect:(target:InspectTarget)=>void;numbers:boolean;threatened:boolean;linkedSource?:boolean;linkedTarget?:boolean;atuacao?:UnitActing}){
  const c=byId[f.characterId],shield=f.shields.reduce((n,s)=>n+s.amount,0);
  const source=beat?.event.source===f.uid,impacted=beat?.impacted??false;
  const hit=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='damage'):undefined;
  const shielded=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='shield'&&e.label==='Escudo'):undefined;
  const blocked=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='block'&&(e.value??0)>=40):undefined;
  // o Status mais recente já revelado (cada passo da cadeia mostra o seu)
  const applied=impacted&&beat?[...beat.events].reverse().find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='status'):undefined;
  // este lutador está reagindo agora (o traço dele disparou no meio da ação de outro)
  const passo=passoAtual(beat),reagindo=passo?.classe==='reacao'&&passo.quem===f.uid?passo:undefined;
  const discovered=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='discovery'):undefined;
  const knocked=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='ko'):undefined;
  const broken=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='interrupt'):undefined;
  const tempo=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='tempo'):undefined;
  const acting=source&&['basic','skill'].includes(beat?.event.kind??'');
  const preparing=!!f.cast||(source&&beat?.event.kind==='cast');
  const out=f.hp<=0,critical=!out&&f.hp/f.maxHp<=P.criticalCondition;
  // caiu, mas vai renascer: fica em brasas em vez de "fora"
  const renascendo=out&&(f.renascendo??0)>0;
  const levantou=impacted?beat?.events.find(e=>revelado(beat,e)&&e.target===f.uid&&e.kind==='revive'):undefined;
  const ring=acting&&!impacted?1:f.action;
  const light=battle.fighters.find(actor=>actor.side!==f.side&&actor.characterId==='light');
  const knowledge=light?.discovered?.[f.uid];
  const advantageSide=battle.dominion>3?'player':battle.dominion< -3?'enemy':null;
  const advantageRule=advantageSide===f.side?'winning':advantageSide?'losing':null;
  const advantageActive=!!advantageRule&&c.skills.some(skill=>skill.charge.some(rule=>rule.on===advantageRule));
  const basicStyle=source&&beat?.event.kind==='basic'?`basic-${beat.family}`:'';
  const buffs=f.statuses.filter(s=>statuses[s.id].tone!=='negativo'),debuffs=f.statuses.filter(s=>statuses[s.id].tone==='negativo');
  const hpPct=Math.max(0,Math.min(100,100*f.hp/f.maxHp)),shieldPct=Math.min(100-hpPct,100*shield/f.maxHp);
  const marcas=[
    out&&'is-out',renascendo&&'is-renascendo',levantou&&'is-revived',preparing&&'is-casting',hit&&'is-hit',acting&&'is-acting',basicStyle,critical&&'is-critical',
    (shielded||blocked)&&'is-helped',linkedSource&&'is-source',linkedTarget&&'is-target',knocked&&'is-newly-out',
    broken&&'is-broken',threatened&&'is-threatened',ring>=P.nearAction&&'is-near',tempo&&'is-tempo',reagindo&&'is-reacting',
  ].filter(Boolean).join(' ');
  /* A atuação deste beat: estilo de quem age, reação de quem recebe, e para onde. */
  const atua=atuacao?[atuacao.act&&`actor act-${atuacao.act} act-${atuacao.parity}`,atuacao.react&&`reactor react-${atuacao.react}`].filter(Boolean).join(' '):'';
  const atuaStyle:Record<string,string>=atuacao?{'--act-dx':`${atuacao.dx.toFixed(1)}px`,'--act-dy':`${atuacao.dy.toFixed(1)}px`,'--act-ux':atuacao.ux.toFixed(3),'--act-uy':atuacao.uy.toFixed(3),'--beat-s':`${atuacao.seconds}s`,'--act-angle':`${(Math.atan2(atuacao.uy,atuacao.ux)*180/Math.PI).toFixed(1)}deg`}:{};
  return <article className={`unit side-${f.side} ${marcas} ${atua}`} data-fighter={f.uid} data-slot={f.slot} data-combat-role={linkedSource&&linkedTarget?'both':linkedSource?'source':linkedTarget?'target':'idle'} style={{'--character':c.color,...atuaStyle} as React.CSSProperties}>
    <div className="unit-medal">
      <span className="unit-fx" aria-hidden="true"/>
      {shield>0&&!out&&<span className="unit-escudo" aria-hidden="true"/>}
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
        {renascendo&&<span className="unit-brasas" aria-hidden="true" style={{'--fx-img':`url(${folha('brasas_renascendo')})`} as React.CSSProperties}/>}
        {out&&(renascendo
          ?<span className="unit-ko unit-renasce" aria-label={`Renascendo em ${Math.ceil(f.renascendo??0)} segundos`}><Flame size={24}/><b>RENASCE</b></span>
          :<span className="unit-ko" aria-label="Fora da luta"><Skull size={26}/><b>FORA</b></span>)}
        {levantou&&<span key={levantou.id} className="discovery-pop revive-pop">{levantou.label}</span>}
        {reagindo&&<span key={`r${reagindo.eventos[0]??0}`} className="reacao-pop"><Zap size={11} strokeWidth={3}/>{reagindo.rotulo??'Reação'}</span>}
        {reagindo&&<span key={`a${reagindo.eventos[0]??0}`} className="reacao-anel" aria-hidden="true"/>}
        {applied&&<span key={applied.id} className="status-pop">{applied.status&&<img src={`/assets/statuses/${applied.status}.png`} alt=""/>}{applied.label}</span>}
        {discovered&&<span key={discovered.id} className="discovery-pop">{discovered.label}</span>}
      </button>
      {(out||advantageActive||critical||shield>0)&&<span className={`unit-flag ${out?'flag-out':advantageActive?'flag-advantage':critical?'flag-critical':'flag-shield'}`} aria-hidden="true">{renascendo?<Flame size={12}/>:out?<Skull size={12}/>:advantageActive?<AuxIcon id="domain" size={13}/>:critical?<HeartPulse size={12}/>:<Shield size={12}/>}</span>}
      {preparing&&<div className="unit-cast"><AuxIcon id="preparing" size={13}/><span>{f.cast?c.skills[f.cast.skill].name:beat?.event.label}</span></div>}
      {/* a habilidade saindo, com ou sem Preparo: o nome aparece enquanto o golpe acontece */}
      {!preparing&&source&&beat?.event.kind==='skill'&&beat.event.skill!==undefined&&c.skills[beat.event.skill]&&<div key={beat.event.id} className="unit-cast unit-skill-name" style={{"--character":c.color} as React.CSSProperties}><SkillIcon type={c.skills[beat.event.skill].icon} size={15} characterId={c.id} skillId={c.skills[beat.event.skill].id}/><span>{c.skills[beat.event.skill].name}</span></div>}
      {broken&&<div className="unit-interrupt"><AuxIcon id="interrupt" size={13}/>{broken.label.includes('atrasada')?'ATRASADO':'INTERROMPIDO'}</div>}
      {tempo&&<span className="unit-tempo-reason">{tempo.label}</span>}
    </div>
    <div className="unit-name"><button className="fighter-name" onClick={()=>onInspect({kind:'fighter',fighter:f})}>{c.name}</button></div>
    <div className="unit-vitals">
      <div className="unit-bar" role="progressbar" aria-label={`Vida de ${c.name}`} aria-valuenow={Math.round(f.hp)} aria-valuemax={f.maxHp} aria-valuemin={0}>
        <span className="unit-bar-hp" style={{width:`${hpPct}%`}}/>
        {shieldPct>0&&<span className="unit-bar-shield" style={{left:`${hpPct}%`,width:`${shieldPct}%`}}/>}
      </div>
      <div className="unit-meta"><span>{renascendo?'RENASCENDO':out?'FORA DA LUTA':critical?'VIDA BAIXA':shield>0?<><Shield size={9}/>{Math.ceil(shield)}</>:'VIDA'}</span>{numbers&&!out&&<b>{Math.ceil(f.hp)}</b>}</div>
      {knowledge&&<span className={`light-knowledge ${knowledge}`}>{knowledge==='vulnerable'?'Vulnerável à Death Note':'Imune à execução'}</span>}
    </div>
    <div className="unit-skills" aria-label={`Habilidades de ${c.name}`}>{c.skills.map((s,i)=>{
      const st=f.skills[i],casting=f.cast?.skill===i,focused=source&&beat?.event.skill===i;
      const ready=impacted&&beat?.events.some(e=>e.source===f.uid&&e.kind==='ready'&&e.skill===i);
      const assisted=impacted&&beat?.events.some(e=>revelado(beat,e)&&e.target===f.uid&&e.source!==f.uid&&e.kind==='charge'&&e.skill===i);
      const mode=out?'empty':casting?'preparing':focused?(impacted?'executing':'ready'):st.cooldown>0?'cooldown':st.charge>=100?'ready':st.charge>0?'charging':'empty';
      const fill=casting?100*(f.cast!.elapsed/f.cast!.duration):st.cooldown>0?100*(1-st.cooldown/Math.max(1,s.cooldown)):st.charge;
      // carregada, mas a regra de uso ainda não está cumprida: espera (ampulheta)
      const espera=mode==='ready'&&!focused&&s.condition!=='always'&&!condicaoAtendida(battle,f,s);
      const label=espera?'pronta, esperando a regra de uso':{empty:'vazia',charging:'carregando',ready:'pronta',preparing:'preparando',executing:'executando',cooldown:'em recarga'}[mode];
      return <div className={`ability-wrap ${assisted?'ability-assisted':''} ${ready?'just-ready':''}`} key={s.id}>
        <button data-ability={`${f.uid}-${i}`} className={`ability ${mode} ${espera?'is-waiting':''}`} onClick={()=>onInspect({kind:'skill',fighter:f,index:i})} aria-label={`${s.name}: ${label}. Toque para explicar`} title={`${s.name} · ${label}`}>
          <span className="ability-fill" style={{height:`${Math.max(0,Math.min(100,fill))}%`}}/>
          <SkillIcon type={s.icon} size={20} characterId={c.id} skillId={s.id}/>
          <svg className="ability-meter" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="10" pathLength="100" strokeDasharray={`${Math.max(0,Math.min(100,fill))} 100`}/></svg>
          {mode==='cooldown'&&<AuxIcon id="cooldown" size={12} className="ability-lock"/>}
          {espera&&<span className="ability-espera" aria-hidden="true"><Hourglass size={10} strokeWidth={2.6}/></span>}
        </button>
      </div>;
    })}</div>
    <div className="unit-statuses">
      <LinhaDeStatus tipo="buffs" lista={buffs} fighter={f} onInspect={onInspect}/>
      <LinhaDeStatus tipo="debuffs" lista={debuffs} fighter={f} onInspect={onInspect}/>
    </div>
  </article>;
}
