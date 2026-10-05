import { useEffect,useLayoutEffect,useRef,useState } from 'react';
import { Pause,Play,FastForward,VolumeX,Volume2,AudioLines,Check,LogOut } from 'lucide-react';
import { AuxIcon } from '../components/Icon';
import type { Battle } from '../engine/types';
import type { Settings } from '../lib/storage';
import type { Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { FighterCard } from '../components/FighterCard';
import { BattleEffects,type Anchors } from '../components/BattleEffects';
import { BattleInspector,type InspectTarget } from '../components/BattleInspector';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';

type BattleNotice={id:string;actor:string;title:string;detail:string};

export function BattleScreen({battle,beat,index,name,settings,paused,onPause,onAbandon,onSettings}:{battle:Battle;beat:Beat|null;index:number;name:string;settings:Settings;paused:boolean;onPause:()=>void;onAbandon:()=>void;onSettings:(s:Settings)=>void}){
  const arena=useRef<HTMLDivElement>(null),[anchors,setAnchors]=useState<Anchors>({}),[mixer,setMixer]=useState(false),[historyOpen,setHistoryOpen]=useState(false),[inspect,setInspect]=useState<InspectTarget|null>(null),[notices,setNotices]=useState<BattleNotice[]>([]),[tutorial,setTutorial]=useState(()=>{try{return index===0&&!localStorage.getItem('nexus-battle-guide-v1')}catch{return false}});
  useLayoutEffect(()=>{
    const el=arena.current;if(!el)return;
    const measure=()=>{const box=el.getBoundingClientRect(),next:Anchors={};el.querySelectorAll<HTMLElement>('[data-portrait],[data-ability]').forEach(node=>{const rect=node.getBoundingClientRect(),key=node.dataset.portrait??node.dataset.ability!;next[key]={x:100*(rect.x+rect.width/2-box.x)/box.width,y:100*(rect.y+rect.height/2-box.y)/box.height};});setAnchors(next);};
    measure();const observer=new ResizeObserver(measure);observer.observe(el);return()=>observer.disconnect();
  },[battle.seed]);
  const remaining=Math.max(0,120-Math.floor(battle.time)),lead=battle.dominion>3?'player':battle.dominion< -3?'enemy':'neutral';
  const label=lead==='player'?'Seu trio está à frente':lead==='enemy'?'Rivais estão à frente':'Disputa equilibrada';
  const position=50-Math.min(48,Math.max(-48,battle.dominion*.48));
  const turn=beat?.impacted&&beat.events.some(e=>e.kind==='turn');
  const threats=new Set(battle.fighters.flatMap(f=>f.cast?.targets??[]));
  if(beat&&!beat.impacted&&beat.event.target)threats.add(beat.event.target);
  const recent=battle.events.filter(e=>['skill','cast','interrupt','ko','block','heal','shield','status','synergy','turn','tempo'].includes(e.kind)).slice(-7).reverse();
  const sourceName=(uid:string)=>{const f=battle.fighters.find(x=>x.uid===uid);return f?byId[f.characterId].name:'Equipe'};
  const historyText=(event:Battle['events'][number])=>{
    const from=sourceName(event.source),to=event.target?sourceName(event.target):'';
    if(event.kind==='skill'||event.kind==='cast')return `${from}: ${event.label}${to?` → ${to}`:''}`;
    if(event.kind==='interrupt')return `${from} ${event.label.toLocaleLowerCase('pt-BR')}${to?` de ${to}`:''}`;
    if(event.kind==='ko')return event.label;
    if(event.kind==='block'||event.kind==='shield')return `${from} protegeu ${to||'o trio'}`;
    if(event.kind==='heal')return `${from} recuperou ${to}`;
    if(event.kind==='status')return `${from} aplicou ${event.status?statuses[event.status].name:event.label} em ${to}`;
    if(event.kind==='synergy')return `${from} ajudou ${to}: ${event.label}`;
    if(event.kind==='tempo')return `${from} alterou o ritmo de ${to}`;
    if(event.kind==='turn')return 'O Domínio mudou de lado';
    return `${from}: ${event.label}`;
  };
  useEffect(()=>{
    if(!beat?.impacted)return;
    const charges=beat.events.filter(event=>event.kind==='charge');
    if(beat.event.kind!=='skill'&&!charges.length)return;
    const labels:Record<string,string>={action:'Ação',dealt:'Dano causado',received:'Dano recebido',allyHurt:'Aliado ferido',enemyHurt:'Rival ferido',interrupt:'Interrupção',status:'Efeito aplicado',protected:'Proteção útil',enemyCast:'Preparação rival',survived:'Tempo sobrevivido',losing:'Desvantagem',winning:'Vantagem',trait:'Traço ativado',synergy:'Sinergia do trio'};
    const effects=beat.events.filter(event=>['damage','heal','shield','block','status','interrupt','ko'].includes(event.kind));
    const detail=charges.length
      ?charges.slice(0,2).map(event=>`+${Math.round(event.value??0)}% carga · ${labels[event.label]??event.label}`).join('  /  ')
      :effects.slice(0,2).map(event=>event.kind==='damage'?`−${Math.round(event.value??0)} condição`:event.kind==='heal'?`+${Math.round(event.value??0)} recuperação`:event.kind==='status'?'Efeito aplicado':event.kind==='interrupt'?'Habilidade interrompida':event.kind==='ko'?'Nocaute':event.kind==='block'||event.kind==='shield'?'Proteção aplicada':event.label).join('  /  ')||'Habilidade executada';
    const notice={id:String(beat.event.id),actor:sourceName(beat.event.source),title:beat.event.label,detail};
    setNotices(current=>[...current.slice(-1),notice]);
    window.setTimeout(()=>setNotices(current=>current.filter(item=>item.id!==notice.id)),3600);
  },[beat?.event.id,beat?.impacted]);
  const closeTutorial=()=>{try{localStorage.setItem('nexus-battle-guide-v1','1')}catch{setTutorial(false)}setTutorial(false)};
  return <section className={`battle-screen lead-${lead} ${turn?'dominion-turn':''} ${paused?'presentation-paused':''}`} style={{'--motion-scale':1/settings.speed,'--lead-strength':Math.min(.45,Math.abs(battle.dominion)/160)} as React.CSSProperties}>
    <header className="battle-header"><div><span className="eyebrow">CONFRONTO {String(index+1).padStart(2,'0')} <span className="muted">/ 10</span></span><h2>{name}</h2></div><div className={`battle-clock ${remaining<=20?'time-critical':''}`}><span>TEMPO DE JOGO</span><strong>{Math.floor(remaining/60)}:{String(remaining%60).padStart(2,'0')}</strong></div></header>
    <div className="dominion"><div className="dominion-labels"><span>RIVAIS</span><strong>DOMÍNIO</strong><span>SEU TRIO</span></div><div className="dominion-track" role="meter" aria-label="Domínio: negativo rivais, positivo seu trio" aria-valuenow={Math.round(battle.dominion)} aria-valuemin={-100} aria-valuemax={100}><span className="dominion-rivals" style={{width:`${position}%`}}/><span className="dominion-player" style={{width:`${100-position}%`}}/><span className="dominion-center"/><span className="dominion-glow" style={{left:`${position}%`}}/><span className="dominion-front" style={{left:`${position}%`}}/></div><small>{turn?'VIRADA DE DOMÍNIO':label}</small></div>
    <div ref={arena} className={`arena ${paused?'is-paused':''} ${settings.effects?'':'effects-off'}`}>
      <div className="arena-scenery" aria-hidden="true"><div className="arena-grid"/><div className="arena-haze"/><div className="arena-orbit orbit-outer"/><div className="arena-orbit orbit-inner"/><div className="arena-axis"/><svg className="arena-sigil" viewBox="0 0 96 96"><circle cx="48" cy="48" r="34"/><circle cx="48" cy="48" r="23"/><path d="M48 8v15m0 50v15M8 48h15m50 0h15M20 20l11 11m34 34 11 11M76 20 65 31M31 65 20 76M33 18l5 19 10 11 10-11 5-19M33 78l5-19 10-11 10 11 5 19"/><path className="arena-sigil-core" d="m48 36 12 12-12 12-12-12 12-12Z"/></svg>{settings.effects&&!settings.reducedMotion&&Array.from({length:P.ambientParticles},(_,i)=><i className="ambient-particle" key={i} style={{left:`${8+(i*37)%85}%`,top:`${25+(i*13)%50}%`,animationDelay:`-${i*1.7}s`,animationDuration:`${8+i%4}s`}}/>)}</div>
      <div className="arena-team enemy-team">{battle.fighters.filter(f=>f.side==='enemy').map(f=><FighterCard key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} explanations={settings.explanations}/>)}</div>
      <div className="arena-gap"><span className="arena-coordinate">NEXUS / ARENA 01</span><span className="arena-coordinate">CONEXÃO ATIVA</span></div>
      <div className="arena-team player-team">{battle.fighters.filter(f=>f.side==='player').map(f=><FighterCard key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} explanations={settings.explanations}/>)}</div>
      <BattleEffects battle={battle} beat={beat} anchors={anchors} enabled={settings.effects} reduced={settings.reducedMotion}/>
      {notices.length>0&&<div className="battle-notice-stack" role="log" aria-live="polite" aria-label="Acontecimentos recentes da batalha">{notices.map(notice=><article className="battle-notice" key={notice.id}><small>{notice.actor}</small><strong>{notice.title}</strong><span>{notice.detail}</span></article>)}</div>}
      {paused&&<div className="paused-banner"><Pause size={16}/> BATALHA PAUSADA</div>}
    </div>
    <footer className="battle-controls"><button className="secondary compact" onClick={onPause}>{paused?<Play size={17}/>:<Pause size={17}/>} {paused?'Continuar':'Pausar'}</button><button className={`secondary compact ${settings.speed===2?'selected':''}`} aria-label={`Velocidade ${settings.speed} vezes`} onClick={()=>onSettings({...settings,speed:settings.speed===1?2:1})}><FastForward size={17}/>{settings.speed}×</button><button className={`icon-button history-button ${historyOpen?'selected':''}`} aria-label="Histórico da batalha" aria-expanded={historyOpen} onClick={()=>setHistoryOpen(!historyOpen)}><AuxIcon id="history" size={22}/></button><button className="icon-button sound-button" aria-label={settings.volume?'Silenciar':'Ativar som'} onClick={()=>onSettings({...settings,volume:settings.volume?0:P.audio.master})}>{settings.volume?<Volume2 size={18}/>:<VolumeX size={18}/>}</button><button className={`icon-button mixer-button ${mixer?'selected':''}`} aria-label="Ajustar música e efeitos" aria-expanded={mixer} onClick={()=>setMixer(!mixer)}><AudioLines size={18}/></button><label className="auto-label"><input type="checkbox" checked={settings.auto} onChange={e=>onSettings({...settings,auto:e.target.checked})}/>Sequência auto</label><button className="danger compact abandon-battle" onClick={onAbandon}><LogOut size={15}/>Desistir</button></footer>
    {historyOpen&&<aside className="battle-history"><div><strong><AuxIcon id="history" size={18}/> Momentos importantes</strong><button aria-label="Fechar histórico" onClick={()=>setHistoryOpen(false)}>×</button></div>{recent.length?recent.map(e=><p key={e.id}>{historyText(e)}</p>):<p>A luta ainda não teve momentos decisivos.</p>}</aside>}
    {mixer&&<div className="battle-mixer">{(['musicVolume','effectsVolume'] as const).map(key=><label key={key}>{key==='musicVolume'?'Música':'Efeitos'}<input type="range" min="0" max="100" value={settings[key]} onChange={e=>onSettings({...settings,[key]:Number(e.target.value)})}/></label>)}</div>}
    <div className="battle-hint"><span><i className="legend-circle"/>Próxima ação</span><span><i className="legend-ready"/>Habilidade pronta</span><span><i className="legend-cast"/>Preparando</span></div>
    {inspect&&<BattleInspector target={inspect} battle={battle} onClose={()=>setInspect(null)} onSelect={setInspect}/>}
    {tutorial&&<div className="battle-tutorial"><div><span><AuxIcon id="help" size={20}/> GUIA RÁPIDO</span><button onClick={closeTutorial} aria-label="Fechar guia"><Check size={17}/></button></div><p><i className="legend-circle"/> <b>Círculo:</b> próxima ação.</p><p><i className="legend-ready"/> <b>Três ícones:</b> habilidades.</p><p><i className="legend-status"/> <b>Ícones pequenos:</b> efeitos ativos.</p><p><AuxIcon id="domain" size={18}/> <b>Barra central:</b> Domínio.</p><button className="secondary" onClick={closeTutorial}>Entendi</button></div>}
  </section>;
}
