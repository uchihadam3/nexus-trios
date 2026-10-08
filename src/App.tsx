import {lazy,Suspense,useEffect,useRef,useState,useMemo} from 'react';
import { ArrowUpRight,Download,Flag,RotateCcw,UserPen,WifiOff,X } from 'lucide-react';
import { Home } from './screens/Home';
import { DraftScreen } from './screens/DraftScreen';
import { BattleScreen } from './screens/BattleScreen';
import { ResultScreen } from './screens/ResultScreen';
import { RankingScreen } from './screens/RankingScreen';
import { CharactersScreen } from './screens/Auxiliary';
import { HelpScreen } from './screens/ComoJogar';
import { SettingsScreen } from './screens/Ajustes';
import { CharacterModal } from './components/CharacterModal';
import { Cabecalho,ToqueGlobal } from './components/Casca';
import { byId,characters } from './data/characters';
import { createBattle } from './engine/battle';
import { generateCampaign,newDraft,pickDraft,skipDraft } from './engine/campaign';
import type { ResultadoTop3 } from './lib/top3';
import { defaults,loadProfile,loadRun,loadSettings,resetStorage,save,storageAvailable } from './lib/storage';
import type { Run,Settings } from './lib/storage';
import { PRIORIDADE } from './audio/cues';
import { battleAudio } from './lib/audio';
import { createDirection,restoreDirection,checkpointDirection,advanceDirection,type Direction,type Beat,type BeatTrace } from './presentation/director';
import { PRESENTATION as P } from './presentation/config';
import type { Battle } from './engine/types';
import { addSynergies,summarizeBattle } from './engine/run-summary';
import { acumularRaioX,raioXVazio } from './engine/raio-x';
import {emptyTally,tallyEvents} from './engine/progression';
import { pontosDaJornada } from './engine/pontos';
import {runDigest,ENGINE_VERSION,rosterFingerprint } from './engine/ranked';
import {carregarCliente,googleConfigured,haSessaoOuRetorno,onlineCall,onlineConfigured} from './lib/online';
import {criarAutenticacaoPreguicosa,type Conta} from './lib/auth';
import {AccountScreen} from './screens/AccountScreen';
const DebugScreen=lazy(()=>import('./screens/DebugScreen').then(m=>({default:m.DebugScreen})));
const VfxLabScreen=lazy(()=>import('./screens/VfxLabScreen').then(m=>({default:m.VfxLabScreen})));
type Screen='home'|'game'|'characters'|'ranking'|'conta'|'help'|'settings'|'debug'|'vfx';
interface InstallEvent extends Event {prompt:()=>Promise<void>;userChoice:Promise<{outcome:string}>}
/* Os avisos do jogo (remake): medalhão com o anel de runas na cor do assunto, título grande, botões grandes. */
function InfoDialog({title,children,onClose,icone,cor='#c8f560'}:{title:string;children:React.ReactNode;onClose:()=>void;icone?:React.ReactNode;cor?:string}){
  const ref=useRef<HTMLDialogElement>(null);useEffect(()=>{const el=ref.current;el?.showModal();return()=>el?.close();},[]);
  return <dialog className="info-dialog gs-aviso" ref={ref} onCancel={onClose} style={{'--tela':cor} as React.CSSProperties}><button className="icon-button modal-close" onClick={onClose} aria-label="Fechar"><X size={20}/></button>{icone&&<span className="gs-medalhao gs-aviso-medalhao"><span aria-hidden className="uifx uifx-laco gs-anel" style={{'--uifx-img':'url(/assets/ui/fx/anel.webp)','--uifx-cor':cor,'--uifx-dur':'4800ms'} as React.CSSProperties}/>{icone}</span>}<h2>{title}</h2>{children}</dialog>;
}
export default function App(){
  const [screen,setScreen]=useState<Screen>(import.meta.env.DEV&&location.hash==='#debug'?'debug':'home');
  const [settings,setSettings]=useState(loadSettings),[profile,setProfile]=useState(loadProfile),[run,setRun]=useState<Run|null>(loadRun);
  const [paused,setPaused]=useState(false),[details,setDetails]=useState<string|null>(null),[menu,setMenu]=useState(false),[installHelp,setInstallHelp]=useState(false),[confirmNew,setConfirmNew]=useState(false),[confirmAbandon,setConfirmAbandon]=useState(false);
  const [onlineNotice,setOnlineNotice]=useState(''),[nameDialog,setNameDialog]=useState(false),[draftHandle,setDraftHandle]=useState(''),[pendingMode,setPendingMode]=useState<'daily'|'weekly'|null>(null),[onlineBusy,setOnlineBusy]=useState(false);
  const submission=useRef(false);
  const [installEvent,setInstallEvent]=useState<InstallEvent|null>(null),[installed,setInstalled]=useState(()=>matchMedia('(display-mode: standalone)').matches);
  const runRef=useRef(run),lastSave=useRef(0);runRef.current=run;
  const direction=useRef<Direction|null>(null);
  const [presentation,setPresentation]=useState<{battle:Battle;beat:Beat|null}|null>(null);
  const lastAudio=useRef(0),lastDominionSound=useRef(0);
  const changeRun=(next:Run|null)=>{runRef.current=next;setRun(next);save('run',next);};
  const directionFor=(current:Run)=>{
    const battle=current.battle!;
    if(current.presentation&&current.team.length===3){
      const initial=createBattle(current.team,current.encounters[current.index].team,current.seed+current.index*7919,current.encounters[current.index].scale);
      const restored=restoreDirection(initial,battle,current.presentation);
      if(restored)return restored;
    }
    return createDirection(battle);
  };
  const changeSettings=(next:Settings)=>{battleAudio.configure(next);setSettings(next);save('settings',next);};
  const navigate=(next:Screen)=>{if(next!=='game')setPaused(true);setScreen(next);setMenu(false);window.scrollTo(0,0);};
  const prepareRanked=async(mode:'daily'|'weekly')=>{
    const response=await onlineCall<{challenge:{seed:number;engine_version?:string;roster_fingerprint?:string};banned:string[]}>('challenge',{mode});
    /*
     * O servidor refaz as 10 lutas com a cópia do motor que ele tem. Se as
     * regras do jogo mudaram e o servidor ainda não foi atualizado, o
     * resultado não bateria e a jornada inteira terminaria "não validada".
     * Melhor avisar antes de começar.
     */
    const c=response.challenge;
    if((c.engine_version&&c.engine_version!==ENGINE_VERSION)||(c.roster_fingerprint&&c.roster_fingerprint!==rosterFingerprint())){
      setOnlineNotice('O ranking está sendo atualizado para as regras novas do jogo. Enquanto isso, jogue a Jornada normal — o ranqueado volta assim que o servidor for atualizado.');
      return;
    }
    const seed=c.seed;
    changeRun({seed,team:[],encounters:generateCampaign(seed),index:0,stage:'draft',draft:newDraft(seed,response.banned),battle:null,recorded:false,summaries:[],ranked:{mode,status:'draft'}});
    setConfirmNew(false);setConfirmAbandon(false);setPendingMode(null);setPaused(false);navigate('game');
  };
  const beginRanked=async(mode:'daily'|'weekly')=>{
    if(!onlineConfigured){setOnlineNotice('Ranking online ainda não está conectado. A Jornada Casual funciona sem internet.');return;}
    setOnlineBusy(true);
    try{
      const response=await onlineCall<{profile:{handle:string}|null}>('profile');
      if(!response.profile){setPendingMode(mode);setNameDialog(true);}else{setProfile(p=>{const n={...p,publicHandle:response.profile!.handle};save('profile',n);return n;});await prepareRanked(mode);}
    }catch(error){setOnlineNotice(error instanceof Error?error.message:'Não foi possível abrir o desafio online.');}
    finally{setOnlineBusy(false);}
  };
  const saveHandle=async()=>{
    setOnlineBusy(true);
    try{const response=await onlineCall<{profile:{handle:string}}> ('profile',{handle:draftHandle});setProfile(p=>{const n={...p,publicHandle:response.profile.handle};save('profile',n);return n;});setNameDialog(false);if(pendingMode)await prepareRanked(pendingMode);}
    catch(error){setOnlineNotice(error instanceof Error?error.message:'Não foi possível salvar o nome.');}
    finally{setOnlineBusy(false);}
  };
  const startNew=()=>{
    const seed=crypto.getRandomValues(new Uint32Array(1))[0];
    changeRun({seed,team:[],encounters:generateCampaign(seed),index:0,stage:'draft',draft:newDraft(seed),battle:null,recorded:false,summaries:[]});setPendingMode(null);setPaused(false);setConfirmNew(false);setConfirmAbandon(false);navigate('game');
  };
  const requestNew=()=>{setPendingMode(null);if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else startNew();};
  const requestRanked=(mode:'daily'|'weekly')=>{setPendingMode(mode);if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else void beginRanked(mode);};
  const startBattle=async(index:number)=>{
    const current=runRef.current;if(!current)return;
    const team=current.draft.team,encounters=current.ranked?current.encounters:current.stage==='draft'?generateCampaign(current.seed,team):current.encounters,encounter=encounters[index];
    let ranked=current.ranked;
    if(index===0&&ranked){setOnlineBusy(true);try{const result=await onlineCall<{run:{id:string;seed:number}}> ('start',{mode:ranked.mode,team});if(result.run.seed!==current.seed)throw new Error('O desafio mudou; inicie outra Jornada Ranqueada.');ranked={...ranked,id:result.run.id,status:'playing'};}catch(error){setOnlineNotice(error instanceof Error?error.message:'Jornada Ranqueada indisponível.');return;}finally{setOnlineBusy(false);}}
    const next={...current,team,encounters,index,stage:'battle' as const,recorded:false,presentation:undefined,battleSynergies:[],raioX:raioXVazio(),telemetry:emptyTally(),ranked,battle:createBattle(team,encounter.team,current.seed+index*7919,encounter.scale)};
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
      const now=performance.now(),elapsed=Math.max(0,Math.min(P.renderIntervalMs/1000,(now-previous)/1000));previous=now;
      if(import.meta.env.DEV){const debugWindow=window as Window & {__nexusFrames?:{count:number;visualSeconds:number;lastElapsed:number}};const frames=debugWindow.__nexusFrames??{count:0,visualSeconds:0,lastElapsed:0};frames.count++;frames.visualSeconds+=elapsed;frames.lastElapsed=elapsed;debugWindow.__nexusFrames=frames;}
      const current=runRef.current;if(!current||current.stage!=='battle'||!current.battle)return;
      if(!direction.current||direction.current.battle!==current.battle){direction.current=directionFor(current);lastAudio.current=current.battle.nextEvent-1;lastDominionSound.current=current.battle.dominion;}
      const d=direction.current;
      advanceDirection(d,elapsed,cue=>{
        if(cue.phase==='impact'&&d.active){
          const special=d.active.events.find(e=>e.kind==='ko')??d.active.events.find(e=>e.kind==='interrupt')??d.active.events.find(e=>e.kind==='block')??d.active.events.find(e=>e.kind==='turn');
          // eventos que pedem som próprio: interrupção, bloqueio, nocaute, virada; o golpe do beat toca junto
          if(special){const pan=0,chave=special.id;battleAudio.sound(special.kind==='interrupt'?'interrupcao':special.kind==='block'?'bloqueio':special.kind==='ko'?'nocaute':'virada',special.kind==='block'?PRIORIDADE.apoio:PRIORIDADE.importante,pan,chave);if(special.kind!=='turn')battleAudio.cue(cue,d.visible);}
          else battleAudio.cue(cue,d.visible);
        }else battleAudio.cue(cue,d.visible);
      },settings.speed,import.meta.env.DEV?trace=>{
        const devWindow=window as Window & {__nexusBeatTrace?:BeatTrace[]};
        const history=devWindow.__nexusBeatTrace??=[];
        history.push(trace);if(history.length>2000)history.shift();
      }:undefined);
      const fighters=d.visible.fighters,critical=fighters.filter(f=>f.hp>0&&f.hp/f.maxHp<.34).length,casts=fighters.filter(f=>f.hp>0&&f.cast).length;
      battleAudio.setMood({heat:Math.min(1,.15+critical*.13+casts*.17+Math.abs(d.visible.dominion)/150),pressure:d.visible.dominion/100,time:Math.min(1,d.visible.time/120)});
      if(Math.abs(d.visible.dominion-lastDominionSound.current)>=20){battleAudio.sound('toque',PRIORIDADE.interface);lastDominionSound.current=d.visible.dominion;}
      const ready=d.signals.find(e=>e.id>lastAudio.current&&e.kind==='ready');
      if(ready)battleAudio.sound('pronto',PRIORIDADE.interface,0,ready.id);
      if(d.signals.length)lastAudio.current=Math.max(lastAudio.current,...d.signals.map(e=>e.id));
      setPresentation({battle:d.visible,beat:d.active?{...d.active}:null});
      const battleSynergies=d.signals.length?addSynergies(current.battleSynergies??[],d.signals):current.battleSynergies??[];
      /*
       * O Raio-X acumula durante a luta, não no fim.
       *
       * `battle.events` guarda só os 180 últimos eventos, então uma leitura
       * feita depois do fim já teria perdido o começo da batalha. Os sinais de
       * cada quadro chegam uma vez só, o que torna a contagem exata.
       */
      const raioX=d.signals.length?acumularRaioX(current.raioX??raioXVazio(),d.signals,d.battle):current.raioX??raioXVazio();
      /* O quanto o trio chegou a ficar atrás: no fim da luta essa informação já não existe. */
      const telemetry=d.signals.length?tallyEvents(current.telemetry??emptyTally(),d.signals):current.telemetry??emptyTally();
      let next={...current,battle:d.battle,presentation:checkpointDirection(d),battleSynergies,raioX,telemetry};
      if(d.complete){
        const summary={...summarizeBattle(current.index,d.battle,battleSynergies),recordeAntes:current.recorded?undefined:loadProfile().recordePontos??0};
        next={...next,stage:'result',recorded:true,summaries:current.recorded?current.summaries:[...(current.summaries??[]).filter(s=>s.index!==current.index),summary]};
        if(!current.recorded){
          const won=d.battle.winner==='player',champion=won&&current.index===9;
          /* o objetivo do jogo: pontos. O recorde é o maior total de uma jornada. */
          const total=pontosDaJornada((next.summaries??[]).map(x=>({pontos:x.score,won:x.won})));
          setProfile(p=>{
            const n={...p,best:Math.max(p.best,current.index+(won?1:0)),wins:p.wins+(won?1:0),victories:p.victories+Number(champion),champion:champion?[...current.team]:p.champion,recordePontos:Math.max(p.recordePontos??0,total)};
            save('profile',n);return n;
          });
          battleAudio.sound(won?'vitoria':'derrota',PRIORIDADE.grand);}
        save('run',next);
      }
      runRef.current=next;setRun(next);
      if(now-lastSave.current>1000){save('run',next);lastSave.current=now;}
    },P.renderIntervalMs);
    return()=>clearInterval(timer);
  },[screen,paused,details,confirmNew,confirmAbandon,settings.speed,settings.volume]);
  useEffect(()=>{
    if(screen!=='game'||!settings.auto||run?.stage!=='result'||run.index>=9||run.battle?.winner!=='player')return;
    const id=window.setTimeout(()=>{const current=runRef.current;if(!current)return;const index=current.index+1,encounter=current.encounters[index];const next={...current,index,stage:'battle' as const,recorded:false,presentation:undefined,battleSynergies:[],raioX:raioXVazio(),telemetry:emptyTally(),battle:createBattle(current.team,encounter.team,current.seed+index*7919,encounter.scale)};runRef.current=next;setRun(next);save('run',next);setPaused(false);},4500);
    return()=>clearTimeout(id);
  },[screen,settings.auto,run?.stage,run?.index,run?.battle?.winner]);
  useEffect(()=>{
    if(!run?.ranked?.id||run.stage!=='result'||run.battle?.winner==='player'&&run.index<9||!['playing','validating'].includes(run.ranked.status)||submission.current)return;
    submission.current=true;const id=run.ranked.id;
    if(run.ranked.status!=='validating')changeRun({...run,ranked:{...run.ranked,status:'validating'}});
    void (async()=>{
      try{const digest=await runDigest(id,run.team,run.seed,(run.summaries??[]).map(s=>s.won));const result=await onlineCall<{score:number;daily:number|null;weekly:number|null;season:number|null;top3?:{periodo?:ResultadoTop3;temporada?:ResultadoTop3}}>('submit',{runId:id,digest});
        const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'verified',score:result.score,daily:result.daily,weekly:result.weekly,season:result.season,top3:result.top3,error:undefined}});
      }catch(error){const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'failed',error:error instanceof Error?error.message:'Falha na validação.'}});}
      finally{submission.current=false;}
    })();
  },[run?.stage,run?.index,run?.battle?.winner,run?.ranked?.status,run?.ranked?.id]);
  useEffect(()=>{battleAudio.configure(settings);},[settings]);
  useEffect(()=>{battleAudio.setBattle(screen==='game'&&run?.stage==='battle'&&!paused&&!details&&!confirmNew&&!confirmAbandon,run?`${run.seed}-${run.index}`:undefined);return()=>battleAudio.setBattle(false);},[screen,run?.stage,run?.seed,run?.index,paused,details,confirmNew,confirmAbandon]);
  const install=async()=>{if(installEvent){await installEvent.prompt();const choice=await installEvent.userChoice;setInstallEvent(null);if(choice.outcome!=='accepted')setInstallHelp(true);}else setInstallHelp(true);};
  /*
   * A conta vive fora do React: o Supabase mantém a sessão no armazenamento
   * dele e avisa por evento. Aqui só se espelha o que ele diz, incluindo a
   * sessão que expirou — nesse caso o jogador volta a ser convidado e o jogo
   * casual segue igual.
   */
  const autenticacao=useMemo(()=>criarAutenticacaoPreguicosa(carregarCliente),[]);
  const [conta,setConta]=useState<Conta|null>(null);
  useEffect(()=>{
    let vivo=true;
    /* Sem sessão guardada nem volta de link, não há conta a descobrir: o Supabase fica para quando for usado. */
    if(haSessaoOuRetorno())void autenticacao.conta().then((c:Conta|null)=>{if(vivo)setConta(c);});
    const parar=autenticacao.observar((c:Conta|null)=>{setConta(c);});
    return ()=>{vivo=false;parar();};
  },[autenticacao]);

  const reset=()=>{resetStorage();setSettings(defaults);setProfile({journeys:0,victories:0,best:0,wins:0,recordePontos:0});setRun(null);runRef.current=null;navigate('home');};
  return <div onPointerDownCapture={()=>void battleAudio.unlock()} onPointerUpCapture={()=>void battleAudio.unlock()} onTouchEndCapture={()=>void battleAudio.unlock()} onClickCapture={()=>void battleAudio.unlock()} onKeyDownCapture={e=>{if(e.key==='Enter'||e.key===' ')void battleAudio.unlock();}} className={`app ${settings.reducedMotion?'reduce-motion':''} ${screen==='game'&&run?.stage==='battle'?'in-battle':''}`}>
    <ToqueGlobal/>
    <Cabecalho tela={screen} menu={menu} onMenu={setMenu} onNavigate={navigate} recorde={profile.recordePontos??0} apelido={profile.publicHandle} online={onlineConfigured} total={characters.length}/>
    <main key={`${screen}-${screen==='game'?run?.stage??'idle':'page'}`} className={screen==='game'&&run?.stage==='battle'?'main battle-main screen-enter':'main screen-enter'}>
      {screen==='home'&&<Home profile={profile} run={run} conta={conta!==null&&conta.origem!=='convidado'} onPlay={requestNew} onRanked={requestRanked} onContinue={()=>{if(run?.stage==='battle'&&run.battle){direction.current=directionFor(run);setPresentation({battle:direction.current.visible,beat:direction.current.active});}navigate('game');setPaused(run?.stage==='battle');}} onAbandon={()=>setConfirmAbandon(true)} onNavigate={navigate} onInstall={()=>void install()}/>}
      {screen==='characters'&&<CharactersScreen onDetails={setDetails}/>}
      {screen==='ranking'&&<RankingScreen handle={profile.publicHandle} conta={conta!==null&&conta.origem!=='convidado'} onConta={()=>navigate('conta')}/>}
      {screen==='conta'&&<AccountScreen autenticacao={autenticacao} conta={conta} profile={profile} conectado={onlineConfigured} google={googleConfigured} aoMudarPerfil={p=>{save('profile',p);setProfile(p);}}/>}
      {screen==='help'&&<HelpScreen onPlay={requestNew}/>}
      {screen==='settings'&&<SettingsScreen settings={settings} onChange={changeSettings} onReset={reset} onGaleria={()=>navigate('vfx')} ranking={onlineConfigured?{nome:profile.publicHandle,onEditar:()=>{setPendingMode(null);setDraftHandle(profile.publicHandle??'');setNameDialog(true);}}:undefined}/>}
      {screen==='game'&&run?.stage==='draft'&&<DraftScreen draft={run.draft} primeiroRival={run.encounters[0]} onPick={id=>changeRun({...run,draft:pickDraft(run.draft,id)})} onSkip={()=>changeRun({...run,draft:skipDraft(run.draft)})} onDetails={setDetails} onStart={()=>void startBattle(0)} onAbandon={()=>setConfirmAbandon(true)}/>}
      {screen==='game'&&run?.stage==='battle'&&run.battle&&<BattleScreen battle={presentation&&direction.current?.battle===run.battle?presentation.battle:run.battle} beat={presentation&&direction.current?.battle===run.battle?presentation.beat:null} index={run.index} name={run.encounters[run.index].name} settings={settings} paused={paused||!!details}  onPause={()=>setPaused(!paused)} onAbandon={()=>setConfirmAbandon(true)} onSettings={changeSettings} onExit={()=>{setPaused(true);navigate('home');}}/>}
      {screen==='game'&&run?.stage==='result'&&<ResultScreen run={run} onNext={()=>void startBattle(run.index+1)} onRestart={requestNew} onAbandon={()=>setConfirmAbandon(true)} onHome={()=>navigate('home')} onRanking={()=>navigate('ranking')} onRetry={()=>{if(run.ranked)changeRun({...run,ranked:{...run.ranked,status:'validating'}});}} auto={settings.auto} onAuto={auto=>changeSettings({...settings,auto})}/>}
      {screen==='debug'&&import.meta.env.DEV&&<Suspense fallback={<p>Carregando laboratório…</p>}><DebugScreen/></Suspense>}
      {screen==='vfx'&&<Suspense fallback={<p>Carregando galeria audiovisual…</p>}><VfxLabScreen/></Suspense>}
      {!storageAvailable&&<p role="alert" className="storage-warning">Não foi possível salvar neste navegador. Sua sessão continua, mas pode não ser recuperada ao fechar.</p>}
    </main>
    {details&&<CharacterModal character={byId[details]} onClose={()=>setDetails(null)}/>}
    {confirmNew&&<InfoDialog title="Começar uma nova jornada?" icone={<RotateCcw/>} cor="#ffb86b" onClose={()=>setConfirmNew(false)}><p>A jornada de agora some. <b>Seu recorde fica salvo.</b></p><div className="result-actions"><button className="danger" onClick={()=>pendingMode?void beginRanked(pendingMode):startNew()}>Descartar e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmNew(false)}>Continuar jornada</button></div></InfoDialog>}
    {nameDialog&&<InfoDialog title="Seu nome no ranking" icone={<UserPen/>} cor="#86e3a8" onClose={()=>setNameDialog(false)}><p>De 3 a 16 letras. Aparece junto do seu trio e dos seus pontos.</p><input className="handle-input" aria-label="Nome público" maxLength={16} value={draftHandle} onChange={e=>setDraftHandle(e.target.value)} placeholder="Seu nome no Nexus"/><p>Prévia: <strong>{draftHandle.trim()||'Seu nome'}</strong></p><button className="primary" disabled={onlineBusy} onClick={()=>void saveHandle()}>Confirmar nome</button></InfoDialog>}
    {onlineNotice&&<InfoDialog title="Conexão do ranking" icone={<WifiOff/>} cor="#ff9a8a" onClose={()=>setOnlineNotice('')}><p role="alert">{onlineNotice}</p><button className="primary" onClick={()=>setOnlineNotice('')}>Entendi</button></InfoDialog>}
    {confirmAbandon&&<InfoDialog title="Desistir desta jornada?" icone={<Flag/>} cor="#ff7a6b" onClose={()=>setConfirmAbandon(false)}><p>A jornada de agora some e você monta um trio novo. <b>Seu recorde fica salvo.</b></p><div className="result-actions"><button className="danger" onClick={startNew}>Desistir e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmAbandon(false)}>Continuar jornada</button></div></InfoDialog>}
    {installHelp&&<InfoDialog title={installed?'O NEXUS já está instalado':'Leve seu trio no bolso'} icone={<Download/>} cor="#8fd3ff" onClose={()=>setInstallHelp(false)}><p>{installed?'Abra o jogo pelo ícone na tela inicial do aparelho.':<><b>Android:</b> menu do navegador → “Instalar aplicativo”.<br/><b>iPhone:</b> Compartilhar → “Adicionar à Tela de Início”.</>}</p><p>O progresso fica neste aparelho e o jogo abre mesmo sem internet.</p><button className="primary" onClick={()=>setInstallHelp(false)}>Entendi</button></InfoDialog>}
  </div>;
}
