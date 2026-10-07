import { useLayoutEffect,useRef,useState } from 'react';
import { Pause,Play,FastForward,VolumeX,Volume2,AudioLines,Check,LogOut } from 'lucide-react';
import { AuxIcon } from '../components/Icon';
import type { Battle } from '../engine/types';
import type { Settings } from '../lib/storage';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { FighterCard } from '../components/FighterCard';
import { BattleEffects,type Anchors } from '../components/BattleEffects';
import { CombatConnections } from '../components/CombatConnections';
import { combatLinks } from '../presentation/combat-links';
import { BattleInspector,type InspectTarget } from '../components/BattleInspector';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import {liveObjectives,type Objective,emptyTally} from '../engine/progression';

export function BattleScreen({battle,beat,index,name,settings,paused,objectives,telemetry,onPause,onAbandon,onSettings}:{battle:Battle;beat:Beat|null;index:number;name:string;settings:Settings;paused:boolean;objectives?:Objective[];telemetry?:ReturnType<typeof emptyTally>;onPause:()=>void;onAbandon:()=>void;onSettings:(s:Settings)=>void}){
  const arena=useRef<HTMLDivElement>(null),[anchors,setAnchors]=useState<Anchors>({}),[mixer,setMixer]=useState(false),[historyOpen,setHistoryOpen]=useState(false),[inspect,setInspect]=useState<InspectTarget|null>(null),[tutorial,setTutorial]=useState(()=>{try{return index===0&&!localStorage.getItem('nexus-battle-guide-v1')?0:-1}catch{return -1}});
  useLayoutEffect(()=>{
    const el=arena.current;if(!el)return;
    const measure=()=>{const box=el.getBoundingClientRect(),next:Anchors={};el.querySelectorAll<HTMLElement>('[data-portrait],[data-ability]').forEach(node=>{const rect=node.getBoundingClientRect(),key=node.dataset.portrait??node.dataset.ability!;next[key]={x:100*(rect.x+rect.width/2-box.x)/box.width,y:100*(rect.y+rect.height/2-box.y)/box.height};});setAnchors(next);};
    measure();const observer=new ResizeObserver(measure);observer.observe(el);return()=>observer.disconnect();
  },[battle.seed]);
  const lead=battle.dominion>3?'player':battle.dominion< -3?'enemy':'neutral';
  const label=lead==='player'?'Seu trio está à frente':lead==='enemy'?'Rivais estão à frente':'Disputa equilibrada';
  const position=50-Math.min(48,Math.max(-48,battle.dominion*.48));
  const turn=beat?.impacted&&beat.events.some(e=>e.kind==='turn');
  const threats=new Set(battle.fighters.flatMap(f=>f.cast?.targets??[]));
  const links=combatLinks(beat,battle);
  const actionTargets=new Set(links.map(link=>link.target));
  const actionSources=new Set(links.map(link=>link.source));
  if(beat&&!beat.impacted&&beat.event.target)threats.add(beat.event.target);
  const recent=battle.events.filter(e=>['damage','heal','shield','status','interrupt','ko','block','discovery','turn','synergy'].includes(e.kind)&&(!['block','shield'].includes(e.kind)||(e.value??0)>=20)).slice(-12).reverse();
  const sourceName=(uid:string)=>{const f=battle.fighters.find(x=>x.uid===uid);return f?byId[f.characterId].name:'Equipe'};
  const historyText=(event:Battle['events'][number])=>{
    const from=sourceName(event.source),to=event.target?sourceName(event.target):'';
    if(event.kind==='skill'||event.kind==='cast')return `${from}: ${event.label}${to?` → ${to}`:''}`;
    if(event.kind==='interrupt')return `${from} ${event.label.toLocaleLowerCase('pt-BR')}${to?` de ${to}`:''}`;
    if(event.kind==='ko')return `${to||from} saiu da luta`;
    if(event.kind==='damage')return `${from} acertou ${to} por ${Math.round(event.value??0)}`;
    if(event.kind==='block')return `${from} protegeu ${to}: ${Math.round(event.value??0)} bloqueado`;
    if(event.kind==='shield')return `${from} deu ${Math.round(event.value??0)} de Escudo a ${to}`;
    if(event.kind==='heal')return `${from} curou ${to} em ${Math.round(event.value??0)}`;
    if(event.kind==='discovery')return `${from} descobriu: ${to} é ${event.label.toLocaleLowerCase('pt-BR')}`;
    if(event.kind==='status')return `${from} aplicou ${event.status?statuses[event.status].name:event.label} em ${to}`;
    if(event.kind==='synergy')return `${from} ajudou ${to} a carregar uma habilidade`;
    if(event.kind==='tempo')return `${from} alterou o ritmo de ${to}`;
    if(event.kind==='turn')return 'VIRADA! A Vantagem mudou de lado';
    return `${from}: ${event.label}`;
  };
  const closeTutorial=()=>{try{localStorage.setItem('nexus-battle-guide-v1','1')}catch{setTutorial(-1)}setTutorial(-1)};
  const tutorialSteps=[['Círculo = próximo ataque básico.','Ele enche, o personagem ataca e começa de novo.'],['Três ícones = habilidades.','Cada uma ganha Carga. Com 100%, fica pronta.'],['PREPARANDO = ainda dá tempo de interromper.','O golpe só acontece quando o Preparo termina.'],['Ícones pequenos = Status.','Toque para ver o efeito e quanto tempo resta.'],['Vantagem mostra quem controla a luta.','Ela ajuda algumas habilidades, mas não decide a vitória.']];
  const live=liveObjectives(objectives??[],battle,telemetry??emptyTally()),focus=live.find(o=>o.progress<o.target)??live[0];
  return <section className={`battle-screen lead-${lead} ${turn?'dominion-turn':''} ${paused?'presentation-paused':''}`} data-beat-id={beat?.event.id} data-beat-kind={beat?.event.kind} data-beat-duration={beat?.duration} style={{'--motion-scale':1/settings.speed,'--lead-strength':Math.min(.45,Math.abs(battle.dominion)/160)} as React.CSSProperties}>
    <header className="battle-header"><div><span className="eyebrow">CONFRONTO {String(index+1).padStart(2,'0')} <span className="muted">/ 10</span></span><h2>{name}</h2></div><span className="battle-objective">ATÉ O ÚLTIMO TRIO</span></header>
    <div className="dominion"><div className="dominion-labels"><span>RIVAIS</span><strong>VANTAGEM</strong><span>SEU TRIO</span></div><div className="dominion-track" role="meter" aria-label="Vantagem: negativo rivais, positivo seu trio" aria-valuenow={Math.round(battle.dominion)} aria-valuemin={-100} aria-valuemax={100}><span className="dominion-rivals" style={{width:`${position}%`}}/><span className="dominion-player" style={{width:`${100-position}%`}}/><span className="dominion-center"/><span className="dominion-glow" style={{left:`${position}%`}}/><span className="dominion-front" style={{left:`${position}%`}}/></div><small>{turn?'VIRADA!':label}</small></div>
    {focus&&<details className="battle-goals"><summary>OBJETIVO · {focus.label} <b>{Math.min(focus.progress,focus.target).toLocaleString('pt-BR')}/{focus.target.toLocaleString('pt-BR')}</b></summary><div>{live.map(o=><p key={o.id}>{o.label}<span>{Math.min(o.progress,o.target).toLocaleString('pt-BR')} / {o.target.toLocaleString('pt-BR')}{o.progress>=o.target?' ✓':''}</span></p>)}</div></details>}
    <div ref={arena} className={`arena ${paused?'is-paused':''} ${settings.effects?'':'effects-off'}`}>
      <div className="arena-scenery" aria-hidden="true"><div className="arena-grid"/><div className="arena-orbit orbit-outer"/><div className="arena-orbit orbit-inner"/><div className="arena-axis"/><svg className="arena-sigil" viewBox="0 0 96 96"><circle cx="48" cy="48" r="34"/><circle cx="48" cy="48" r="23"/><path d="M48 8v15m0 50v15M8 48h15m50 0h15M20 20l11 11m34 34 11 11M76 20 65 31M31 65 20 76M33 18l5 19 10 11 10-11 5-19M33 78l5-19 10-11 10 11 5 19"/><path className="arena-sigil-core" d="m48 36 12 12-12 12-12-12 12-12Z"/></svg></div>
      <div className="arena-team enemy-team">{battle.fighters.filter(f=>f.side==='enemy').map(f=><FighterCard key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} linkedSource={actionSources.has(f.uid)} linkedTarget={actionTargets.has(f.uid)}/>)}</div>
      <div className="arena-gap" aria-hidden="true"/>
      <div className="arena-team player-team">{battle.fighters.filter(f=>f.side==='player').map(f=><FighterCard key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} linkedSource={actionSources.has(f.uid)} linkedTarget={actionTargets.has(f.uid)}/>)}</div>
      <CombatConnections battle={battle} beat={beat} anchors={anchors} reduced={settings.reducedMotion}/>
      <BattleEffects battle={battle} beat={beat} anchors={anchors} enabled={settings.effects} reduced={settings.reducedMotion}/>
      {paused&&<div className="paused-banner"><Pause size={16}/> BATALHA PAUSADA</div>}
    </div>
    <footer className="battle-controls"><button className="secondary compact" onClick={onPause}>{paused?<Play size={17}/>:<Pause size={17}/>} {paused?'Continuar':'Pausar'}</button><button className={`secondary compact ${settings.speed===2?'selected':''}`} aria-label={`Velocidade ${settings.speed} vezes`} onClick={()=>onSettings({...settings,speed:settings.speed===1?2:1})}><FastForward size={17}/>{settings.speed}×</button><button className={`icon-button history-button ${historyOpen?'selected':''}`} aria-label="Histórico da batalha" aria-expanded={historyOpen} onClick={()=>setHistoryOpen(!historyOpen)}><AuxIcon id="history" size={22}/></button><button className="icon-button sound-button" aria-label={settings.volume?'Silenciar':'Ativar som'} onClick={()=>onSettings({...settings,volume:settings.volume?0:P.audio.master})}>{settings.volume?<Volume2 size={18}/>:<VolumeX size={18}/>}</button><button className={`icon-button mixer-button ${mixer?'selected':''}`} aria-label="Ajustar música e efeitos" aria-expanded={mixer} onClick={()=>setMixer(!mixer)}><AudioLines size={18}/></button><label className="auto-label"><input type="checkbox" checked={settings.auto} onChange={e=>onSettings({...settings,auto:e.target.checked})}/>Sequência auto</label><button className="danger compact abandon-battle" onClick={onAbandon}><LogOut size={15}/>Desistir</button></footer>
    {historyOpen&&<aside className="battle-history"><div><strong><AuxIcon id="history" size={18}/> Momentos importantes</strong><button aria-label="Fechar histórico" onClick={()=>setHistoryOpen(false)}>×</button></div>{recent.length?recent.map(e=><p key={e.id}>{historyText(e)}</p>):<p>A luta ainda não teve momentos decisivos.</p>}</aside>}
    {mixer&&<div className="battle-mixer">{(['musicVolume','effectsVolume'] as const).map(key=><label key={key}>{key==='musicVolume'?'Música':'Efeitos'}<input type="range" min="0" max="100" value={settings[key]} onChange={e=>onSettings({...settings,[key]:Number(e.target.value)})}/></label>)}</div>}
    {settings.explanations!=='off'&&<div className="battle-hint"><span><i className="legend-circle"/>Próximo ataque</span><span><i className="legend-ready"/>Habilidade pronta</span><span><i className="legend-cast"/>Preparo</span>{settings.explanations==='detailed'&&<span>Toque em uma habilidade ou Status para entender.</span>}</div>}
    {inspect&&<BattleInspector target={inspect} battle={battle} onClose={()=>setInspect(null)} onSelect={setInspect}/>}
    {tutorial>=0&&<div className="battle-tutorial"><div><span><AuxIcon id="help" size={20}/> GUIA {tutorial+1}/5</span><button onClick={closeTutorial} aria-label="Pular guia"><Check size={17}/></button></div><p><b>{tutorialSteps[tutorial][0]}</b></p><p>{tutorialSteps[tutorial][1]}</p><button className="secondary" onClick={()=>tutorial===4?closeTutorial():setTutorial(tutorial+1)}>{tutorial===4?'Pronto. Assistir meu trio':'Entendi'}</button><button className="text-button" onClick={closeTutorial}>Pular guia</button></div>}
  </section>;
}
