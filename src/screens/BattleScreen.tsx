import { useCallback,useEffect,useLayoutEffect,useRef,useState } from 'react';
import { ComTermos } from '../components/Termos';
import { battleAudio } from '../lib/audio';
import { Pause,Play,FastForward,VolumeX,Volume2,SlidersHorizontal,Check,LogOut,ChevronLeft,ScrollText } from 'lucide-react';
import { AuxIcon } from '../components/Icon';
import type { Battle } from '../engine/types';
import type { Settings } from '../lib/storage';
import type { Beat } from '../presentation/director';
import { duracaoBase } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { ArenaUnit } from '../components/ArenaUnit';
import { BattleEffects,isAreaBeat,type Anchors } from '../components/BattleEffects';
import { FloatingNumbers } from '../components/FloatingNumbers';
import { atuacao } from '../presentation/acting';
import { CombatConnections } from '../components/CombatConnections';
import { combatLinks } from '../presentation/combat-links';
import { BattleInspector,type InspectTarget } from '../components/BattleInspector';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';

export function BattleScreen({battle,beat,index,name,settings,paused,onPause,onAbandon,onSettings,onExit}:{battle:Battle;beat:Beat|null;index:number;name:string;settings:Settings;paused:boolean;onPause:()=>void;onAbandon:()=>void;onSettings:(s:Settings)=>void;onExit?:()=>void}){
  const arena=useRef<HTMLDivElement>(null),[anchors,setAnchors]=useState<Anchors>({}),[box,setBox]=useState({w:0,h:0,medal:80}),[mixer,setMixer]=useState(false),[historyOpen,setHistoryOpen]=useState(false),[inspect,setInspect]=useState<InspectTarget|null>(null),[tutorial,setTutorial]=useState(()=>{try{return index===0&&!localStorage.getItem('nexus-battle-guide-v1')?0:-1}catch{return -1}});
  /* Os sons dos seis lutadores chegam antes do primeiro golpe. */
  const elenco=battle.fighters.map(f=>f.characterId).join(',');
  useEffect(()=>{void battleAudio.precarregarLuta(elenco.split(','));},[elenco]);
  /*
   * Onde cada medalhão e cada habilidade estão, em % da arena — é para onde
   * apontam efeitos, linhas, mira e números. Medido pela posição de layout
   * (offsetLeft/offsetTop), que ignora as animações: um medalhão no meio do
   * avanço não muda o ponto de mira. E medido de novo sempre que um lutador
   * muda de tamanho (uma linha de Status aparece, o rótulo de preparo entra)
   * e a cada ação, para nunca mirar onde o medalhão estava antes.
   */
  const measure=useCallback(()=>{
    const el=arena.current;if(!el)return;
    const w=el.clientWidth,h=el.clientHeight;if(!w||!h)return;
    const local=(node:HTMLElement)=>{let x=0,y=0,n:HTMLElement|null=node;while(n&&n!==el){x+=n.offsetLeft;y+=n.offsetTop;n=n.offsetParent as HTMLElement|null;}return n===el?{x,y}:null;};
    const next:Anchors={};
    el.querySelectorAll<HTMLElement>('[data-portrait],[data-ability]').forEach(node=>{const p=local(node);if(!p)return;const key=node.dataset.portrait??node.dataset.ability!;next[key]={x:100*(p.x+node.offsetWidth/2)/w,y:100*(p.y+node.offsetHeight/2)/h};});
    const medal=el.querySelector<HTMLElement>('.unit-medal')?.offsetWidth??80;
    setAnchors(prev=>{const a=Object.keys(next);return a.length===Object.keys(prev).length&&a.every(k=>prev[k]&&Math.abs(prev[k].x-next[k].x)<.05&&Math.abs(prev[k].y-next[k].y)<.05)?prev:next;});
    setBox(prev=>prev.w===w&&prev.h===h&&prev.medal===medal?prev:{w,h,medal});
  },[]);
  useLayoutEffect(()=>{
    const el=arena.current;if(!el)return;
    measure();
    const observer=new ResizeObserver(()=>measure());observer.observe(el);
    el.querySelectorAll('.unit').forEach(u=>observer.observe(u));
    return()=>observer.disconnect();
  },[battle.seed,measure]);
  useLayoutEffect(()=>{measure();},[beat?.event.id,beat?.impacted,measure]);
  const lead=battle.dominion>3?'player':battle.dominion< -3?'enemy':'neutral';
  const label=lead==='player'?'Seu trio está à frente':lead==='enemy'?'Rivais estão à frente':'Disputa equilibrada';
  const position=50-Math.min(48,Math.max(-48,battle.dominion*.48));
  const turn=beat?.impacted&&beat.events.some(e=>e.kind==='turn');
  const threats=new Set(battle.fighters.flatMap(f=>f.cast?.targets??[]));
  const links=combatLinks(beat,battle);
  const actionTargets=new Set(links.map(link=>link.target));
  const actionSources=new Set(links.map(link=>link.source));
  if(beat&&!beat.impacted&&beat.event.target)threats.add(beat.event.target);
  const recent=battle.events.filter(e=>['damage','heal','shield','status','interrupt','ko','revive','cleanse','dispel','miss','resist','copy','summon','block','discovery','turn','synergy'].includes(e.kind)&&(!['block','shield'].includes(e.kind)||(e.value??0)>=20)).slice(-12).reverse();
  const sourceName=(uid:string)=>{const f=battle.fighters.find(x=>x.uid===uid);return f?byId[f.characterId].name:'Equipe'};
  const historyText=(event:Battle['events'][number])=>{
    const from=sourceName(event.source),to=event.target?sourceName(event.target):'';
    if(event.kind==='skill'||event.kind==='cast')return `${from}: ${event.label}${to?` → ${to}`:''}`;
    if(event.kind==='interrupt')return `${from} ${event.label.toLocaleLowerCase('pt-BR')}${to?` de ${to}`:''}`;
    if(event.kind==='ko')return `${to||from} saiu da luta`;
    if(event.kind==='summon')return `${event.label} (de ${from}) atacou ${to}`;
    if(event.kind==='copy')return `${from} ${event.label.toLocaleLowerCase('pt-BR')} de ${to}`;
    if(event.kind==='damage'&&event.label==='Explosão')return `A Marca explosiva de ${from} explodiu em ${to}: ${Math.round(event.value??0)} de dano`;
    if(event.kind==='miss')return event.label==='Esquivou'?`${to} esquivou do golpe de ${from}`:`${from} errou o golpe em ${to}`;
    if(event.kind==='resist'&&event.label==='Última resistência')return `${to||from} ficou de pé com 1 de Vida: Última resistência`;
    if(event.kind==='resist')return `A Barreira de ${to||from} anulou ${event.status?statuses[event.status].name:'o debuff'}`;
    if(event.kind==='cleanse'||event.kind==='dispel'){const nomes=(event.removidos??[]).map(id=>statuses[id].name).join(', ');return `${from} ${event.kind==='cleanse'?'purificou':'dissipou'} ${to}: ${nomes}`;}
    if(event.kind==='revive')return event.source===event.target?`${from} renasceu com ${Math.round(event.value??0)} de Vida`:`${from} levantou ${to} com ${Math.round(event.value??0)} de Vida`;
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
  const tutorialSteps=[['Círculo = próximo ataque básico.','Ele enche, o personagem ataca e começa de novo.'],['Três ícones = habilidades.','Cada uma ganha Carga. Com 100%, fica pronta.'],['PREPARANDO = ainda dá tempo de interromper.','O golpe só acontece quando o Preparo termina.'],['Linha de cima = buffs. Linha de baixo = debuffs.','Toque num Status para ver quanto ele vale e quanto tempo resta.'],['Vantagem mostra quem controla a luta.','Ela ajuda algumas habilidades, mas não decide a vitória.']];
  const papeis=atuacao(beat,battle,{anchors,...box},isAreaBeat(beat,battle));
  const unit=(f:Battle['fighters'][number])=><ArenaUnit key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} linkedSource={actionSources.has(f.uid)} linkedTarget={actionTargets.has(f.uid)} atuacao={papeis[f.uid]}/>;
  return <section className={`battle-screen arena-v2 lead-${lead} ${turn?'dominion-turn':''} ${paused?'presentation-paused':''}`} data-beat-id={beat?.event.id} data-beat-kind={beat?.event.kind} data-beat-duration={beat?duracaoBase(beat):undefined} data-beat-etapas={beat?.etapas?.length} style={{'--motion-scale':1/settings.speed,'--lead-strength':Math.min(.45,Math.abs(battle.dominion)/160),'--front':`${position}%`} as React.CSSProperties}>
    <header className="arena-hud">
      {onExit&&<button className="hud-button hud-exit" onClick={onExit} aria-label="Voltar ao início (a batalha fica pausada)"><ChevronLeft size={22}/></button>}
      <div className="hud-round" title={name}><small>CONFRONTO</small><b>{String(index+1).padStart(2,'0')}<i>/10</i></b></div>
      <div className="hud-advantage">
        <div className="hud-advantage-labels"><span>RIVAIS</span><strong>{turn?'VIRADA!':label}</strong><span>SEU TRIO</span></div>
        <div className="hud-advantage-track" role="meter" aria-label="Vantagem: negativo rivais, positivo seu trio" aria-valuenow={Math.round(battle.dominion)} aria-valuemin={-100} aria-valuemax={100}>
          <span className="hud-advantage-rivals" style={{width:`${position}%`}}/><span className="hud-advantage-allies" style={{width:`${100-position}%`}}/>
          <span className="hud-advantage-mid" aria-hidden="true"/><span className="hud-advantage-front" aria-hidden="true"/>
        </div>
      </div>
      <button className={`hud-button history-button ${historyOpen?'selected':''}`} aria-label="Histórico da batalha" aria-expanded={historyOpen} onClick={()=>setHistoryOpen(!historyOpen)}><ScrollText size={20}/></button>
    </header>
    <div ref={arena} className={`arena ${paused?'is-paused':''} ${settings.effects?'':'effects-off'}`}>
      <div className="arena-floor" aria-hidden="true"><span className="floor-glow floor-rivals"/><span className="floor-glow floor-allies"/><span className="floor-ring ring-outer"/><span className="floor-ring ring-inner"/><span className="floor-lines"/></div>
      <div className="team team-rivals">{battle.fighters.filter(f=>f.side==='enemy').map(unit)}</div>
      <div className="arena-center"><span className="arena-versus" aria-hidden="true">VS</span><span className="arena-encounter">{name}</span>
        {settings.explanations!=='off'&&<div className="battle-hint"><span><i className="legend-circle"/><ComTermos texto="Próximo ataque"/></span><span><i className="legend-ready"/><ComTermos texto="Pronta"/></span><span><i className="legend-cast"/><ComTermos texto="Preparo"/></span></div>}
      </div>
      <div className="team team-allies">{battle.fighters.filter(f=>f.side==='player').map(unit)}</div>
      <CombatConnections battle={battle} beat={beat} anchors={anchors} reduced={settings.reducedMotion} medal={box.medal}/>
      <BattleEffects battle={battle} beat={beat} anchors={anchors} enabled={settings.effects} reduced={settings.reducedMotion} medal={box.medal}/>
      <FloatingNumbers battle={battle} beat={beat} anchors={anchors} medal={box.medal} enabled={settings.numbers}/>
      {paused&&<div className="paused-banner"><Pause size={16}/> BATALHA PAUSADA</div>}
    </div>
    <footer className="arena-controls">
      <button className={`control-main ${paused?'is-paused':''}`} onClick={onPause}>{paused?<Play size={18}/>:<Pause size={18}/>}<span>{paused?'Continuar':'Pausar'}</span></button>
      <button className={`control ${settings.speed===2?'selected':''}`} aria-label={`Velocidade ${settings.speed} vezes`} onClick={()=>onSettings({...settings,speed:settings.speed===1?2:1})}><FastForward size={18}/><b>{settings.speed}×</b></button>
      <button className="control sound-button" aria-label={settings.volume?'Silenciar':'Ativar som'} onClick={()=>onSettings({...settings,volume:settings.volume?0:P.audio.master})}>{settings.volume?<Volume2 size={19}/>:<VolumeX size={19}/>}</button>
      <button className={`control mixer-button ${mixer?'selected':''}`} aria-label="Ajustes da batalha" aria-expanded={mixer} onClick={()=>setMixer(!mixer)}><SlidersHorizontal size={18}/></button>
      <button className="control control-danger abandon-battle" onClick={onAbandon} aria-label="Desistir da jornada"><LogOut size={17}/><span>Desistir</span></button>
    </footer>
    {historyOpen&&<aside className="battle-history"><div><strong><AuxIcon id="history" size={18}/> Momentos importantes</strong><button aria-label="Fechar histórico" onClick={()=>setHistoryOpen(false)}>×</button></div>{recent.length?recent.map(e=><p key={e.id}><ComTermos texto={historyText(e)}/></p>):<p>A luta ainda não teve momentos decisivos.</p>}</aside>}
    {mixer&&<div className="battle-mixer">{(['musicVolume','effectsVolume'] as const).map(key=><label key={key}>{key==='musicVolume'?'Música':'Efeitos'}<input type="range" min="0" max="100" value={settings[key]} onChange={e=>onSettings({...settings,[key]:Number(e.target.value)})}/></label>)}<label className="auto-label"><input type="checkbox" checked={settings.auto} onChange={e=>onSettings({...settings,auto:e.target.checked})}/>Próximo confronto automático</label></div>}
    {inspect&&<BattleInspector target={inspect} battle={battle} onClose={()=>setInspect(null)} onSelect={setInspect}/>}
    {tutorial>=0&&<div className="battle-tutorial"><div><span><AuxIcon id="help" size={20}/> GUIA {tutorial+1}/5</span><button onClick={closeTutorial} aria-label="Pular guia"><Check size={17}/></button></div><p><b>{tutorialSteps[tutorial][0]}</b></p><p><ComTermos texto={tutorialSteps[tutorial][1]}/></p><button className="secondary" onClick={()=>tutorial===4?closeTutorial():setTutorial(tutorial+1)}>{tutorial===4?'Pronto. Assistir meu trio':'Entendi'}</button><button className="text-button" onClick={closeTutorial}>Pular guia</button></div>}
  </section>;
}
