import { lazy,Suspense,useEffect,useRef,useState } from 'react';
import { ArrowLeft,ArrowUpRight,Layers,Menu,X,ShieldCheck } from 'lucide-react';
import { Home } from './screens/Home';
import { DraftScreen } from './screens/DraftScreen';
import { BattleScreen } from './screens/BattleScreen';
import { ResultScreen } from './screens/ResultScreen';
import { CharactersScreen,HelpScreen,SettingsScreen } from './screens/Auxiliary';
import { CharacterModal } from './components/CharacterModal';
import { byId,characters } from './data/characters';
import { createBattle } from './engine/battle';
import { generateCampaign,newDraft,pickDraft,skipDraft } from './engine/campaign';
import { defaults,loadProfile,loadRun,loadSettings,resetStorage,save,storageAvailable } from './lib/storage';
import type { Run,Settings } from './lib/storage';
import { battleAudio } from './lib/audio';
import { createDirection,advanceDirection,type Direction,type Beat } from './presentation/director';
import { PRESENTATION as P } from './presentation/config';
import type { Battle } from './engine/types';
const DebugScreen=lazy(()=>import('./screens/DebugScreen').then(m=>({default:m.DebugScreen})));
const VfxLabScreen=lazy(()=>import('./screens/VfxLabScreen').then(m=>({default:m.VfxLabScreen})));
type Screen='home'|'game'|'characters'|'help'|'settings'|'debug'|'vfx';
interface InstallEvent extends Event {prompt:()=>Promise<void>;userChoice:Promise<{outcome:string}>}
function InfoDialog({title,children,onClose}:{title:string;children:React.ReactNode;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null);useEffect(()=>{const el=ref.current;el?.showModal();return()=>el?.close();},[]);
  return <dialog className="info-dialog" ref={ref} onCancel={onClose}><button className="icon-button modal-close" onClick={onClose} aria-label="Fechar"><X size={20}/></button><h2>{title}</h2>{children}</dialog>;
}
export default function App(){
  const [screen,setScreen]=useState<Screen>(import.meta.env.DEV&&location.hash==='#debug'?'debug':'home');
  const [settings,setSettings]=useState(loadSettings),[profile,setProfile]=useState(loadProfile),[run,setRun]=useState<Run|null>(loadRun);
  const [paused,setPaused]=useState(false),[details,setDetails]=useState<string|null>(null),[menu,setMenu]=useState(false),[installHelp,setInstallHelp]=useState(false),[confirmNew,setConfirmNew]=useState(false),[confirmAbandon,setConfirmAbandon]=useState(false);
  const [installEvent,setInstallEvent]=useState<InstallEvent|null>(null),[installed,setInstalled]=useState(()=>matchMedia('(display-mode: standalone)').matches);
  const runRef=useRef(run),lastSave=useRef(0);runRef.current=run;
  const direction=useRef<Direction|null>(null);
  const [presentation,setPresentation]=useState<{battle:Battle;beat:Beat|null}|null>(null);
  const lastAudio=useRef(0),lastDominionSound=useRef(0);
  const changeRun=(next:Run|null)=>{runRef.current=next;setRun(next);save('run',next);};
  const changeSettings=(next:Settings)=>{battleAudio.configure(next);setSettings(next);save('settings',next);};
  const navigate=(next:Screen)=>{if(next!=='game')setPaused(true);setScreen(next);setMenu(false);window.scrollTo(0,0);};
  const startNew=()=>{
    const seed=crypto.getRandomValues(new Uint32Array(1))[0];
    changeRun({seed,team:[],encounters:generateCampaign(seed),index:0,stage:'draft',draft:newDraft(seed),battle:null,recorded:false});setPaused(false);setConfirmNew(false);setConfirmAbandon(false);navigate('game');
  };
  const requestNew=()=>{if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else startNew();};
  const startBattle=(index:number)=>{
    const current=runRef.current;if(!current)return;
    const team=current.draft.team,encounters=current.stage==='draft'?generateCampaign(current.seed,team):current.encounters,encounter=encounters[index];
    const next={...current,team,encounters,index,stage:'battle' as const,recorded:false,battle:createBattle(team,encounter.team,current.seed+index*7919,encounter.scale)};
    direction.current=null;setPresentation(null);changeRun(next);setPaused(false);navigate('game');
    if(index===0)setProfile(p=>{const n={...p,journeys:p.journeys+1};save('profile',n);return n;});
  };
  useEffect(()=>{
    const capture=(e:Event)=>{e.preventDefault();setInstallEvent(e as InstallEvent);};
    const complete=()=>{setInstalled(true);setInstallEvent(null);setInstallHelp(false);};
    addEventListener('beforeinstallprompt',capture);addEventListener('appinstalled',complete);
    return()=>{removeEventListener('beforeinstallprompt',capture);removeEventListener('appinstalled',complete);};
  },[]);
  useEffect(()=>{
    const persist=()=>save('run',runRef.current);
    const visibility=()=>{if(document.hidden){setPaused(true);persist();}};
    addEventListener('pagehide',persist);document.addEventListener('visibilitychange',visibility);
    return()=>{removeEventListener('pagehide',persist);document.removeEventListener('visibilitychange',visibility);};
  },[]);
  useEffect(()=>{
    if(screen!=='game'||paused||details||confirmNew||confirmAbandon)return;
    let previous=performance.now();
    const timer=window.setInterval(()=>{
      const now=performance.now(),elapsed=Math.max(0,Math.min(.25,(now-previous)/1000));previous=now;
      const current=runRef.current;if(!current||current.stage!=='battle'||!current.battle)return;
      if(!direction.current||direction.current.battle!==current.battle){direction.current=createDirection(current.battle);lastAudio.current=current.battle.nextEvent-1;lastDominionSound.current=current.battle.dominion;}
      const d=direction.current;
      advanceDirection(d,elapsed*settings.speed,cue=>{
        if(cue.phase==='impact'&&d.active){
          const special=d.active.events.find(e=>e.kind==='ko')??d.active.events.find(e=>e.kind==='interrupt')??d.active.events.find(e=>e.kind==='block')??d.active.events.find(e=>e.kind==='turn');
          if(special)battleAudio.sound(special.kind==='interrupt'?(special.label.includes('atrasada')?'interrupt':'shatter'):special.kind==='block'?'block':special.kind==='ko'?'ko':'turn',4);
          else battleAudio.cue(cue);
        }else battleAudio.cue(cue);
      });
      const fighters=d.visible.fighters,critical=fighters.filter(f=>f.hp>0&&f.hp/f.maxHp<.34).length,casts=fighters.filter(f=>f.hp>0&&f.cast).length;
      battleAudio.setMood({heat:Math.min(1,.15+critical*.13+casts*.17+Math.abs(d.visible.dominion)/150),pressure:d.visible.dominion/100,time:d.visible.time/120});
      if(Math.abs(d.visible.dominion-lastDominionSound.current)>=20){battleAudio.sound('dominion',2);lastDominionSound.current=d.visible.dominion;}
      const ready=d.signals.find(e=>e.id>lastAudio.current&&e.kind==='ready');
      if(ready)battleAudio.sound('ready',1);
      if(d.signals.length)lastAudio.current=Math.max(lastAudio.current,...d.signals.map(e=>e.id));
      setPresentation({battle:d.visible,beat:d.active?{...d.active}:null});
      let next={...current,battle:d.battle};
      if(d.complete){
        next={...next,stage:'result',recorded:true};
        if(!current.recorded){const won=current.battle.winner==='player';setProfile(p=>{const n={...p,best:Math.max(p.best,current.index+(won?1:0)),wins:p.wins+(won?1:0),victories:p.victories+(won&&current.index===9?1:0)};save('profile',n);return n;});battleAudio.sound(won?'victory':'defeat',5);}
        save('run',next);
      }
      runRef.current=next;setRun(next);
      if(now-lastSave.current>1000){save('run',next);lastSave.current=now;}
    },P.renderIntervalMs);
    return()=>clearInterval(timer);
  },[screen,paused,details,confirmNew,confirmAbandon,settings.speed,settings.volume]);
  useEffect(()=>{
    if(screen!=='game'||!settings.auto||run?.stage!=='result'||run.index>=9||run.battle?.winner!=='player')return;
    const id=window.setTimeout(()=>{const current=runRef.current;if(!current)return;const index=current.index+1,encounter=current.encounters[index];const next={...current,index,stage:'battle' as const,recorded:false,battle:createBattle(current.team,encounter.team,current.seed+index*7919,encounter.scale)};runRef.current=next;setRun(next);save('run',next);setPaused(false);},4500);
    return()=>clearTimeout(id);
  },[screen,settings.auto,run?.stage,run?.index,run?.battle?.winner]);
  useEffect(()=>{battleAudio.configure(settings);},[settings]);
  useEffect(()=>{battleAudio.setBattle(screen==='game'&&run?.stage==='battle'&&!paused&&!details&&!confirmNew&&!confirmAbandon);return()=>battleAudio.setBattle(false);},[screen,run?.stage,paused,details,confirmNew,confirmAbandon]);
  const install=async()=>{if(installEvent){await installEvent.prompt();const choice=await installEvent.userChoice;setInstallEvent(null);if(choice.outcome!=='accepted')setInstallHelp(true);}else setInstallHelp(true);};
  const reset=()=>{resetStorage();setSettings(defaults);setProfile({journeys:0,victories:0,best:0,wins:0});setRun(null);runRef.current=null;navigate('home');};
  return <div onPointerDownCapture={()=>void battleAudio.unlock()} onKeyDownCapture={e=>{if(e.key==='Enter'||e.key===' ')void battleAudio.unlock();}} className={`app ${settings.reducedMotion?'reduce-motion':''}`}>
    <header className="site-header"><button className="brand" onClick={()=>navigate('home')} aria-label="Nexus início"><span className="brand-mark">N</span><span>NEXUS<small>DUELO DE TRIOS</small></span></button><nav aria-label="Navegação principal" className={menu?'open':''}><button className={screen==='home'?'active':''} onClick={()=>navigate('home')}>Início</button><button className={screen==='characters'?'active':''} onClick={()=>navigate('characters')}>Personagens <span>{characters.length}</span></button><button className={screen==='help'?'active':''} onClick={()=>navigate('help')}>Como jogar</button><button className={screen==='settings'?'active':''} onClick={()=>navigate('settings')}>Configurações</button></nav><div className="header-right"><span className="local-badge"><ShieldCheck size={13}/> PROGRESSO LOCAL</span><button className="icon-button menu-toggle" aria-label="Abrir menu" aria-expanded={menu} onClick={()=>setMenu(!menu)}>{menu?<X size={20}/>:<Menu size={20}/>}</button></div></header>
    <main className={screen==='game'&&run?.stage==='battle'?'main battle-main':'main'}>
      {screen!=='home'&&<button className="back-button" onClick={()=>navigate('home')}><ArrowLeft size={15}/>Voltar ao início</button>}
      {screen==='home'&&<Home profile={profile} run={run} onPlay={requestNew} onContinue={()=>{navigate('game');setPaused(run?.stage==='battle');}} onAbandon={()=>setConfirmAbandon(true)} onNavigate={navigate} onInstall={()=>void install()}/>}
      {screen==='characters'&&<CharactersScreen onDetails={setDetails}/>}
      {screen==='help'&&<HelpScreen onPlay={requestNew}/>}
      {screen==='settings'&&<SettingsScreen settings={settings} onChange={changeSettings} onReset={reset}/>}
      {screen==='game'&&run?.stage==='draft'&&<DraftScreen draft={run.draft} onPick={id=>changeRun({...run,draft:pickDraft(run.draft,id)})} onSkip={()=>changeRun({...run,draft:skipDraft(run.draft)})} onDetails={setDetails} onStart={()=>startBattle(0)} onAbandon={()=>setConfirmAbandon(true)}/>}
      {screen==='game'&&run?.stage==='battle'&&run.battle&&<BattleScreen battle={presentation&&direction.current?.battle===run.battle?presentation.battle:run.battle} beat={presentation&&direction.current?.battle===run.battle?presentation.beat:null} index={run.index} name={run.encounters[run.index].name} settings={settings} paused={paused||!!details} onPause={()=>setPaused(!paused)} onAbandon={()=>setConfirmAbandon(true)} onSettings={changeSettings}/>}
      {screen==='game'&&run?.stage==='result'&&<ResultScreen run={run} onNext={()=>startBattle(run.index+1)} onRestart={requestNew} onAbandon={()=>setConfirmAbandon(true)} onHome={()=>navigate('home')} auto={settings.auto} onAuto={auto=>changeSettings({...settings,auto})}/>}
      {screen==='debug'&&import.meta.env.DEV&&<Suspense fallback={<p>Carregando laboratório…</p>}><DebugScreen/></Suspense>}
      {screen==='vfx'&&<Suspense fallback={<p>Carregando galeria audiovisual…</p>}><VfxLabScreen/></Suspense>}
      {!storageAvailable&&<p role="alert" className="storage-warning">Não foi possível salvar neste navegador. Sua sessão continua, mas pode não ser recuperada ao fechar.</p>}
    </main>
    <footer className="site-footer"><span><Layers size={13}/> DIFERENTES UNIVERSOS. NOVAS CONEXÕES.</span><button className="footer-lab" onClick={()=>navigate('vfx')}>Galeria de efeitos</button><span>NEXUS <i/> MVP 1.0</span></footer>
    {details&&<CharacterModal character={byId[details]} onClose={()=>setDetails(null)}/>}
    {confirmNew&&<InfoDialog title="Começar uma nova campanha?" onClose={()=>setConfirmNew(false)}><p>O progresso desta campanha será descartado. Vitórias e recordes já registrados ficam salvos.</p><div className="result-actions"><button className="danger" onClick={startNew}>Descartar e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmNew(false)}>Continuar campanha</button></div></InfoDialog>}
    {confirmAbandon&&<InfoDialog title="Desistir desta campanha?" onClose={()=>setConfirmAbandon(false)}><p>O progresso desta campanha será descartado e uma nova seleção de trio começará. Vitórias e recordes já registrados ficam salvos.</p><div className="result-actions"><button className="danger" onClick={startNew}>Desistir e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmAbandon(false)}>Continuar campanha</button></div></InfoDialog>}
    {installHelp&&<InfoDialog title={installed?'O NEXUS já está instalado.':'Leve seu trio com você.'} onClose={()=>setInstallHelp(false)}><p>{installed?'Abra o jogo pela tela inicial do seu dispositivo.':'No Chrome ou Edge, use o menu do navegador e escolha “Instalar aplicativo”. No iPhone ou iPad, use Compartilhar → Adicionar à Tela de Início.'}</p><p>Abra o jogo uma vez com conexão para salvar os arquivos. O progresso fica neste navegador. A disponibilidade de instalação depende do navegador.</p><button className="primary" onClick={()=>setInstallHelp(false)}>Entendi</button></InfoDialog>}
  </div>;
}
