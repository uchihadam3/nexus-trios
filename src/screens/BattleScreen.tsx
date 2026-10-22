import { useCallback,useEffect,useLayoutEffect,useRef,useState } from 'react';
import { ComTermos } from '../components/Termos';
import { UNICAS } from '../engine/unicas';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { Swords,Pause,Play,FastForward,VolumeX,Volume2,SlidersHorizontal,Check,LogOut,ChevronLeft,ScrollText,Link2,Star } from 'lucide-react';
import { LUTA_ESTRELA,ehLutaExtra } from '../engine/segredos';
import '../presentation/segredos.css';
import { AberturaDeCombos,DescobertaNoLivro,FichaDoCombo,ListaDeCombos,type NovosNoLivro } from '../components/CombosDoTrio';
import { OrbesDeCombo } from '../components/OrbesDeCombo';
import { Invocacoes } from '../components/Invocacoes';
import { RajadaDaUnica } from '../components/RajadaDaUnica';
import { EsferaQueCresce } from '../components/EsferaQueCresce';
import { EntregaDeApoio } from '../components/EntregaDeApoio';
import { AuxIcon } from '../components/Icon';
import { BotaoAutoDaBatalha } from '../components/ChaveDoAuto';
import type { Battle, ComboAtivo, Side } from '../engine/types';
import { VELOCIDADE_DO_PVP } from '../engine/pvp';
import { VELOCIDADE_MAXIMA, type Settings } from '../lib/storage';
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
import { nomeDe, t } from '../i18n/idioma';

export function BattleScreen({battle,beat,index,name,settings,paused,onPause,onAbandon,onSettings,onExit,novosNoLivro,pvp}:{battle:Battle;beat:Beat|null;index:number;name:string;settings:Settings;paused:boolean;onPause:()=>void;onAbandon:()=>void;onSettings:(s:Settings)=>void;onExit?:()=>void;novosNoLivro?:NovosNoLivro|null;
  /** Luta de PvP (src/screens/PvpScreen.tsx): rodada, nomes dos dois lados, contra pessoas sempre em VELOCIDADE_DO_PVP e sem AUTO; pausa só no treino. */
  pvp?:{rodada:number;voce:string;rival:string;podePausar:boolean;velocidadeLivre?:boolean}}){
  const arena=useRef<HTMLDivElement>(null),[anchors,setAnchors]=useState<Anchors>({}),[box,setBox]=useState({w:0,h:0,medal:80}),[mixer,setMixer]=useState(false),[historyOpen,setHistoryOpen]=useState(false),[combosAbertos,setCombosAbertos]=useState<false|Side>(false),[fichaDoCombo,setFichaDoCombo]=useState<ComboAtivo|null>(null),[inspect,setInspect]=useState<InspectTarget|null>(null),[tutorial,setTutorial]=useState(()=>{try{return index===0&&!localStorage.getItem('nexus-battle-guide-v1')?0:-1}catch{return -1}});
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
  const label=lead==='player'?(pvp?t('Você está à frente'):t('Seu trio está à frente')):lead==='enemy'?(pvp?t('{nome} está à frente',{nome:pvp.rival}):t('Rivais estão à frente')):t('Disputa equilibrada');
  // a barra do topo: o seu trio (verde) à esquerda, como na arena; os rivais (vermelho) à direita
  const position=50+Math.min(48,Math.max(-48,battle.dominion*.48));
  const turn=beat?.impacted&&beat.events.some(e=>e.kind==='turn');
  const threats=new Set(battle.fighters.flatMap(f=>f.cast?.targets??[]));
  const links=combatLinks(beat,battle);
  const actionTargets=new Set(links.map(link=>link.target));
  const actionSources=new Set(links.map(link=>link.source));
  if(beat&&!beat.impacted&&beat.event.target)threats.add(beat.event.target);
  const recent=battle.events.filter(e=>['damage','heal','shield','status','interrupt','ko','revive','cleanse','dispel','miss','resist','copy','summon','block','discovery','turn','synergy','unica'].includes(e.kind)&&(!['block','shield'].includes(e.kind)||(e.value??0)>=20)).slice(-12).reverse();
  const sourceName=(uid:string)=>{const f=battle.fighters.find(x=>x.uid===uid);return f?nomeDe(byId[f.characterId]):t('Equipe')};
  const historyText=(event:Battle['events'][number])=>{
    const from=sourceName(event.source),to=event.target?sourceName(event.target):'';
    const v=Math.round(event.value??0),rot=t(event.label),stt=(x?:string)=>x?t(statuses[x as keyof typeof statuses].name):'';
    if(event.kind==='skill'||event.kind==='cast')return `${from}: ${rot}${to?` → ${to}`:''}`;
    if(event.kind==='interrupt')return to?t('{de} interrompeu {para}',{de:from,para:to}):`${from}: ${rot}`;
    if(event.kind==='ko')return t('{nome} saiu da luta',{nome:to||from});
    if(event.kind==='summon')return t('{criatura} (de {de}) atacou {para}',{criatura:rot,de:from,para:to});
    if(event.kind==='copy')return t('{de} copiou {para}',{de:from,para:to});
    if(event.kind==='damage'&&event.label==='Explosão')return t('A Marca explosiva de {de} explodiu em {para}: {v} de dano',{de:from,para:to,v});
    if(event.kind==='miss')return event.label==='Esquivou'?t('{para} esquivou do golpe de {de}',{de:from,para:to}):t('{de} errou o golpe em {para}',{de:from,para:to});
    if(event.kind==='unica'){const mec=UNICAS[battle.fighters.find(x=>x.uid===event.source)?.characterId??'']?.nome;if(event.label==='Imune')return `${t('{nome} é imune a {status}',{nome:from,status:event.status?stt(event.status):t('isso')})}${mec?` (${t(mec)})`:''}`;return `${from} · ${mec?t(mec):t('Mecânica única')}: ${rot}${to&&to!==from?` → ${to}`:''}`;}
    if(event.kind==='resist'&&event.label==='Última resistência')return t('{nome} ficou de pé com 1 de Vida: Última resistência',{nome:to||from});
    if(event.kind==='resist')return t('A Barreira de {nome} anulou {status}',{nome:to||from,status:event.status?stt(event.status):t('o debuff')});
    if(event.kind==='cleanse'||event.kind==='dispel'){const nomes=(event.removidos??[]).map(id=>stt(id)).join(', ');return `${event.kind==='cleanse'?t('{de} purificou {para}',{de:from,para:to}):t('{de} dissipou {para}',{de:from,para:to})}: ${nomes}`;}
    if(event.kind==='revive')return event.source===event.target?t('{de} renasceu com {v} de Vida',{de:from,v}):t('{de} levantou {para} com {v} de Vida',{de:from,para:to,v});
    if(event.kind==='damage')return t('{de} acertou {para} por {v}',{de:from,para:to,v});
    if(event.kind==='block')return t('{de} protegeu {para}: {v} bloqueado',{de:from,para:to,v});
    if(event.kind==='shield')return t('{de} deu {v} de Escudo a {para}',{de:from,para:to,v});
    if(event.kind==='heal')return t('{de} curou {para} em {v}',{de:from,para:to,v});
    if(event.kind==='discovery')return t('{de} descobriu: {para} é {o_que}',{de:from,para:to,o_que:rot.toLocaleLowerCase()});
    if(event.kind==='status')return t('{de} aplicou {status} em {para}',{de:from,para:to,status:event.status?stt(event.status):rot});
    if(event.kind==='synergy')return t('{de} ajudou {para} a carregar uma habilidade',{de:from,para:to});
    if(event.kind==='tempo')return t('{de} alterou o ritmo de {para}',{de:from,para:to});
    if(event.kind==='turn')return t('VIRADA! A Vantagem mudou de lado');
    return `${from}: ${event.label}`;
  };
  const closeTutorial=()=>{try{localStorage.setItem('nexus-battle-guide-v1','1')}catch{setTutorial(-1)}setTutorial(-1)};
  const tutorialSteps=[[t('Círculo = próximo ataque básico.'),t('Ele enche, o personagem ataca e começa de novo.')],[t('Três ícones = habilidades.'),t('Cada uma ganha Carga. Com 100%, fica pronta.')],[t('PREPARANDO = ainda dá tempo de interromper.'),t('O golpe só acontece quando o Preparo termina.')],[t('Linha de cima = buffs. Linha de baixo = debuffs.'),t('Toque num Status para ver quanto ele vale e quanto tempo resta.')],[t('Vantagem mostra quem controla a luta.'),t('Ela ajuda algumas habilidades, mas não decide a vitória.')]];
  const papeis=atuacao(beat,battle,{anchors,...box},isAreaBeat(beat,battle));
  const unit=(f:Battle['fighters'][number])=><ArenaUnit key={f.uid} fighter={f} battle={battle} beat={beat} onInspect={setInspect} numbers={settings.numbers} threatened={threats.has(f.uid)} linkedSource={actionSources.has(f.uid)} linkedTarget={actionTargets.has(f.uid)} atuacao={papeis[f.uid]}/>;
  return <section className={`battle-screen arena-v2 lead-${lead} ${turn?'dominion-turn':''} ${paused?'presentation-paused':''}`} data-beat-id={beat?.event.id} data-beat-kind={beat?.event.kind} data-beat-duration={beat?duracaoBase(beat):undefined} data-beat-etapas={beat?.etapas?.length} style={{'--motion-scale':1/settings.speed,'--lead-strength':Math.min(.45,Math.abs(battle.dominion)/160),'--front':`${position}%`} as React.CSSProperties}>
    <header className="arena-hud">
      {onExit&&<button className="hud-button hud-exit" onClick={onExit} aria-label={t('Voltar ao início (a batalha fica pausada)')}><ChevronLeft size={22}/></button>}
      {pvp?<div className="hud-round hud-pvp" title={name}><small>{t('RODADA')}</small><b>{pvp.rodada}<i>PvP</i></b></div>
        :ehLutaExtra(index)?<div className="hud-round hud-secreta" title={name}><small>{t('SECRETA')}</small><b>{index===LUTA_ESTRELA?<Star size={17} fill="currentColor"/>:11}</b></div>
        :<div className="hud-round" title={name}><small>{t('CONFRONTO')}</small><b>{String(index+1).padStart(2,'0')}<i>/10</i></b></div>}
      <div className="hud-advantage">
        <div className="hud-advantage-labels"><span>{pvp?t('VOCÊ'):t('SEU TRIO')}</span><strong>{turn?t('VIRADA!'):label}</strong><span>{pvp?pvp.rival:t('RIVAIS')}</span></div>
        <div className="hud-advantage-track" role="meter" aria-label={t('Vantagem: seu trio à esquerda, rivais à direita')} aria-valuenow={Math.round(battle.dominion)} aria-valuemin={-100} aria-valuemax={100}>
          <span className="hud-advantage-allies" style={{width:`${position}%`}}/><span className="hud-advantage-rivals" style={{width:`${100-position}%`}}/>
          <span className="hud-advantage-mid" aria-hidden="true"/><span className="hud-advantage-front" aria-hidden="true"/>
        </div>
      </div>
      <button className={`hud-button history-button ${historyOpen?'selected':''}`} aria-label={t('Histórico da batalha')} aria-expanded={historyOpen} onClick={()=>setHistoryOpen(!historyOpen)}><ScrollText size={20}/></button>
    </header>
    <div ref={arena} className={`arena ${paused?'is-paused':''} ${settings.effects?'':'effects-off'}`}>
      <div className="arena-floor" aria-hidden="true"><span className="floor-glow floor-rivals"/><span className="floor-glow floor-allies"/><span className="floor-ring ring-outer"/><span className="floor-ring ring-inner"/><span className="floor-lines"/></div>
      <div className="team team-rivals">{battle.fighters.filter(f=>f.side==='enemy').map(unit)}</div>
      <div className="arena-center"><span className="arena-versus" aria-hidden="true">VS</span><span className="arena-encounter">{t(name)}</span>
      {/* as bolinhas de combos (src/engine/combos.ts): uma de cada lado, nos cantos; tocar abre os combos daquele lado */}
      {battle.combos&&<OrbesDeCombo battle={battle} anchors={anchors} reduzido={settings.reducedMotion} onAbrir={lado=>{setFichaDoCombo(null);setCombosAbertos(lado);}}/>}

        {settings.explanations!=='off'&&<div className="battle-hint"><span><i className="legend-circle"/><ComTermos texto={t('Próximo ataque')}/></span><span><i className="legend-ready"/><ComTermos texto={t('Pronta')}/></span><span><i className="legend-cast"/><ComTermos texto={t('Preparo')}/></span></div>}
      </div>
      <div className="team team-allies">{battle.fighters.filter(f=>f.side==='player').map(unit)}</div>
      <CombatConnections battle={battle} beat={beat} anchors={anchors} reduced={settings.reducedMotion} medal={box.medal}/>
      <BattleEffects battle={battle} beat={beat} anchors={anchors} enabled={settings.effects} reduced={settings.reducedMotion} medal={box.medal}/>
      {/* as criaturas invocadas: a bolinha ao lado de quem invocou */}
      <Invocacoes battle={battle} beat={beat} anchors={anchors} box={box} velocidade={settings.speed}/>
      <RajadaDaUnica battle={battle} beat={beat} anchors={anchors} box={box} reduced={settings.reducedMotion}/>
      {settings.effects&&<EntregaDeApoio battle={battle} beat={beat} anchors={anchors} box={box} reduced={settings.reducedMotion}/>}
      {settings.effects&&<EsferaQueCresce battle={battle} beat={beat} anchors={anchors} box={box} reduced={settings.reducedMotion}/>}
      <FloatingNumbers battle={battle} beat={beat} anchors={anchors} medal={box.medal} enabled={settings.numbers}/>
      {/* a abertura: os combos do trio entrando no começo da luta */}
      {battle.combos&&<AberturaDeCombos combos={battle.combos.player} chaveDaLuta={`${index}-${battle.seed}`} comecando={battle.time<1.5}/>}
      {/* e o que a luta acabou de pôr no Livro de Combos (do trio ou visto no rival) */}
      {novosNoLivro&&novosNoLivro.chave===`${index}-${battle.seed}`&&<DescobertaNoLivro novos={novosNoLivro} comecando={battle.time<1.5}/>}
      {/* a luta extra liberada por um segredo (src/engine/segredos.ts) abre com o nome dela */}
      {!pvp&&ehLutaExtra(index)&&<AberturaSecreta key={`${index}-${battle.seed}`} index={index} nome={name} comecando={battle.time<1.5}/>}
      {paused&&<div className="paused-banner"><Pause size={16}/> {t('BATALHA PAUSADA')}</div>}
    </div>
    <footer className="arena-controls">
      {pvp&&!pvp.podePausar&&<span className="control-main pvp-ao-vivo"><i/>{t('AO VIVO')}</span>}
      {(!pvp||pvp.podePausar)&&<button className={`control-main ${paused?'is-paused':''}`} onClick={onPause}>{paused?<Play size={18}/>:<Pause size={18}/>}<span>{paused?t('Continuar'):t('Pausar')}</span></button>}
      {pvp&&!pvp.velocidadeLivre?<><span className="control selected pvp-2x" aria-label={t('PvP sempre em {n} vezes',{n:VELOCIDADE_DO_PVP})}><FastForward size={18}/><b>{VELOCIDADE_DO_PVP}×</b></span><span className="control pvp-selo" aria-hidden="true"><Swords size={17}/><b>PvP</b></span></>:<>
      <button className={`control ${settings.speed>1?'selected':''}`} aria-label={t('Velocidade {n} vezes',{n:settings.speed})} onClick={()=>onSettings({...settings,speed:settings.speed>=VELOCIDADE_MAXIMA?1:(settings.speed+1) as Settings['speed']})}><FastForward size={18}/><b>{settings.speed}×</b></button>
      {pvp?<span className="control pvp-selo" aria-hidden="true"><Swords size={17}/><b>PvP</b></span>:<BotaoAutoDaBatalha ligado={settings.auto} onChange={auto=>onSettings({...settings,auto})}/>}</>}
      <button className="control sound-button" aria-label={settings.volume?t('Silenciar'):t('Ativar som')} onClick={()=>onSettings({...settings,volume:settings.volume?0:P.audio.master})}>{settings.volume?<Volume2 size={19}/>:<VolumeX size={19}/>}</button>
      <button className={`control mixer-button ${mixer?'selected':''}`} aria-label={t('Ajustes da batalha')} aria-expanded={mixer} onClick={()=>setMixer(!mixer)}><SlidersHorizontal size={18}/></button>
      <button className="control control-danger abandon-battle" onClick={onAbandon} aria-label={pvp?t('Desistir desta luta'):t('Desistir da jornada')}><LogOut size={17}/><span>{t('Desistir')}</span></button>
    </footer>
    {historyOpen&&<aside className="battle-history"><div><strong><AuxIcon id="history" size={18}/> {t('Momentos importantes')}</strong><button aria-label={t('Fechar histórico')} onClick={()=>setHistoryOpen(false)}>×</button></div>{recent.length?recent.map(e=><p key={e.id}><ComTermos texto={historyText(e)}/></p>):<p>{t('A luta ainda não teve momentos decisivos.')}</p>}</aside>}
    {mixer&&<div className="battle-mixer">{(['musicVolume','effectsVolume'] as const).map(key=><label key={key}>{key==='musicVolume'?t('Música'):t('Efeitos')}<input type="range" min="0" max="100" value={settings[key]} onChange={e=>onSettings({...settings,[key]:Number(e.target.value)})}/></label>)}</div>}
    {combosAbertos&&battle.combos&&<aside className="battle-history battle-combos" aria-label={t('Combos da luta')}>
      <div><strong><Link2 size={18}/> {fichaDoCombo?t(fichaDoCombo.nome):t('Combos da luta')}</strong><button aria-label={t('Fechar combos')} onClick={()=>{setCombosAbertos(false);setFichaDoCombo(null);}}>×</button></div>
      {fichaDoCombo?<><button type="button" className="cb-voltar" onClick={()=>setFichaDoCombo(null)}>‹ {t('Voltar para os combos')}</button><FichaDoCombo combo={fichaDoCombo}/></>:<>
        <nav className="cb-lados" role="tablist">{(['player','enemy'] as Side[]).map(lado=><button key={lado} role="tab" aria-selected={combosAbertos===lado} className={`${lado} ${combosAbertos===lado?'ativa':''}`} onClick={()=>setCombosAbertos(lado)}>{lado==='player'?t('VOCÊ'):t('RIVAL')}<b>{battle.combos![lado].length}</b></button>)}</nav>
        <p className="cb-dica-lista">{t('Toque num combo para ler a ficha completa.')}</p>
        <ListaDeCombos combos={battle.combos[combosAbertos]} vazio={combosAbertos==='player'?t('Nenhum combo no seu trio.'):t('Nenhum combo no trio rival.')} onEscolher={setFichaDoCombo}/>
      </>}
    </aside>}
    {inspect&&<BattleInspector target={inspect} battle={battle} onClose={()=>setInspect(null)} onSelect={setInspect}/>}
    {tutorial>=0&&<div className="battle-tutorial"><div><span><AuxIcon id="help" size={20}/> {t('GUIA {n}/5',{n:tutorial+1})}</span><button onClick={closeTutorial} aria-label={t('Pular guia')}><Check size={17}/></button></div><p><b>{tutorialSteps[tutorial][0]}</b></p><p><ComTermos texto={tutorialSteps[tutorial][1]}/></p><button className="secondary" onClick={()=>tutorial===4?closeTutorial():setTutorial(tutorial+1)}>{tutorial===4?t('Pronto. Assistir meu trio'):t('Entendi')}</button><button className="text-button" onClick={closeTutorial}>{t('Pular guia')}</button></div>}
  </section>;
}

/* A abertura da luta secreta: "LUTA SECRETA ★" com o nome do rival, por três segundos (só quando a luta começa agora). */
function AberturaSecreta({index,nome,comecando}:{index:number;nome:string;comecando:boolean}){
  const [ver,setVer]=useState(comecando);
  useEffect(()=>{if(!ver)return;battleAudio.sound('pronto',PRIORIDADE.grand);const id=window.setTimeout(()=>setVer(false),3300);return()=>clearTimeout(id);
    // uma vez por luta
  },[]);
  if(!ver)return null;
  return <div className="bt-secreta" role="status">
    <small>{t('SEGREDO LIBERADO')}</small>
    <strong>{index===LUTA_ESTRELA?t('LUTA SECRETA ★'):t('LUTA 11')}</strong>
    <span>{nome==='Luta Secreta'?t('Só vale pontos se vencer'):`${t(nome)} · ${t('só vale pontos se vencer')}`}</span>
    <i aria-hidden="true">{[0,1,2].map(k=><Star key={k} size={18} fill="currentColor" style={{'--k':k} as React.CSSProperties}/>)}</i>
  </div>;
}
