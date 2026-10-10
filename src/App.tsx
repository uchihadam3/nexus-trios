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
import { defaults,ESCALA_DOS_PONTOS,loadProfile,loadRun,loadSettings,resetStorage,save,storageAvailable } from './lib/storage';
import type { Run,Settings } from './lib/storage';
import { PRIORIDADE,type Sound } from './audio/cues';
import { battleAudio,faixaDaLuta } from './lib/audio';
import { createDirection,restoreDirection,checkpointDirection,advanceDirection,type Direction,type Beat,type BeatTrace } from './presentation/director';
import { PRESENTATION as P } from './presentation/config';
import type { Battle, BattleEvent } from './engine/types';
import { addSynergies,summarizeBattle } from './engine/run-summary';
import { acumularRaioX,raioXVazio } from './engine/raio-x';
import {emptyTally,tallyEvents} from './engine/progression';
import { pontosDaJornada } from './engine/pontos';
import {runDigest} from './engine/ranked';
import {carregarCliente,googleConfigured,haSessaoOuRetorno,onlineCall,onlineConfigured} from './lib/online';
import {criarAutenticacaoPreguicosa,type Conta} from './lib/auth';
import { dicasLiberadas,ehDono } from './lib/dicas-liberadas';
import {AccountScreen} from './screens/AccountScreen';
import {FAMILIA_DA_INVOCACAO} from './presentation/vfx-atribuicao';
import {efeitosDoJeito,somDoJeito} from './presentation/jeito-efeito';
const DebugScreen=lazy(()=>import('./screens/DebugScreen').then(m=>({default:m.DebugScreen})));
const VfxLabScreen=lazy(()=>import('./screens/VfxLabScreen').then(m=>({default:m.VfxLabScreen})));
type Screen='home'|'game'|'characters'|'ranking'|'conta'|'help'|'settings'|'debug'|'vfx';
interface InstallEvent extends Event {prompt:()=>Promise<void>;userChoice:Promise<{outcome:string}>}
/* Os avisos do jogo (remake): medalhão com o anel de runas na cor do assunto, título grande, botões grandes. */
function InfoDialog({title,children,onClose,icone,cor='#c8f560'}:{title:string;children:React.ReactNode;onClose:()=>void;icone?:React.ReactNode;cor?:string}){
  const ref=useRef<HTMLDialogElement>(null);useEffect(()=>{const el=ref.current;el?.showModal();return()=>el?.close();},[]);
  return <dialog className="info-dialog gs-aviso" ref={ref} onCancel={onClose} style={{'--tela':cor} as React.CSSProperties}><button className="icon-button modal-close" onClick={onClose} aria-label="Fechar"><X size={20}/></button>{icone&&<span className="gs-medalhao gs-aviso-medalhao"><span aria-hidden className="uifx uifx-laco gs-anel" style={{'--uifx-img':'url(/assets/ui/fx/anel.webp)','--uifx-cor':cor,'--uifx-dur':'4800ms'} as React.CSSProperties}/>{icone}</span>}<h2>{title}</h2>{children}</dialog>;
}
/** Quanto tempo de luta dá para recuperar de uma vez (uma luta longa inteira cabe com folga). */
const RECUPERACAO_MAXIMA=20*60;
/** Quanto se recupera por quadro (o resto fica para os próximos). */
const RECUPERACAO_POR_QUADRO=90;

export default function App(){
  const [screen,setScreen]=useState<Screen>(import.meta.env.DEV&&location.hash==='#debug'?'debug':'home');
  const [settings,setSettings]=useState(loadSettings),[profile,setProfile]=useState(loadProfile),[run,setRun]=useState<Run|null>(loadRun);
  const [paused,setPaused]=useState(false),[details,setDetails]=useState<string|null>(null),[menu,setMenu]=useState(false),[installHelp,setInstallHelp]=useState(false),[confirmNew,setConfirmNew]=useState(false),[confirmAbandon,setConfirmAbandon]=useState(false);
  const [onlineNotice,setOnlineNotice]=useState(''),[nameDialog,setNameDialog]=useState(false),[draftHandle,setDraftHandle]=useState(''),[pendingStart,setPendingStart]=useState(false),[onlineBusy,setOnlineBusy]=useState(false);
  const submission=useRef(false);
  const [installEvent,setInstallEvent]=useState<InstallEvent|null>(null),[installed,setInstalled]=useState(()=>matchMedia('(display-mode: standalone)').matches);
  const runRef=useRef(run),lastSave=useRef(0);runRef.current=run;
  const direction=useRef<Direction|null>(null);
  const [presentation,setPresentation]=useState<{battle:Battle;beat:Beat|null}|null>(null);
  const lastAudio=useRef(0),lastDominionSound=useRef(0),passoTocado=useRef({beat:-1,passo:1}),divida=useRef(0);
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
  /*
   * Um jogo só, e ele é ranqueado (pedido do jogador: "não existe casual e
   * ranqueada, tudo é ranqueado"). Com a conta conectada, falta só o nome
   * público: na primeira jornada sem ele, o jogo pede o nome e segue.
   */
  const contaConectada=()=>onlineConfigured&&conta!==null&&conta.origem!=='convidado';
  const saveHandle=async()=>{
    setOnlineBusy(true);
    try{const response=await onlineCall<{profile:{handle:string}}> ('profile',{handle:draftHandle});setProfile(p=>{const n={...p,publicHandle:response.profile.handle};save('profile',n);return n;});setNameDialog(false);if(pendingStart){setPendingStart(false);abreJornada();}}
    catch(error){setOnlineNotice(error instanceof Error?error.message:'Não foi possível salvar o nome.');}
    finally{setOnlineBusy(false);}
  };
  const startNew=async()=>{
    if(contaConectada()&&!profile.publicHandle){
      setOnlineBusy(true);
      try{
        const response=await onlineCall<{profile:{handle:string}|null}>('profile');
        if(!response.profile){setConfirmNew(false);setPendingStart(true);setNameDialog(true);return;}
        setProfile(p=>{const n={...p,publicHandle:response.profile!.handle};save('profile',n);return n;});
      }catch{/* sem servidor: joga do mesmo jeito, só fora do ranking */}
      finally{setOnlineBusy(false);}
    }
    abreJornada();
  };
  const abreJornada=()=>{
    const seed=crypto.getRandomValues(new Uint32Array(1))[0];
    changeRun({seed,team:[],encounters:generateCampaign(seed),index:0,stage:'draft',draft:newDraft(seed),battle:null,recorded:false,summaries:[]});setPaused(false);setConfirmNew(false);setConfirmAbandon(false);navigate('game');
  };
  const requestNew=()=>{if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else void startNew();};
  /*
   * Os rivais da jornada saem assim que o trio fica pronto, não ao entrar na
   * arena: assim a "Primeira luta" mostrada na escolha é exatamente a luta que
   * vem. Eles dependem do trio (ninguém repete) e, com a conta conectada, da
   * seed que o servidor do ranking sorteia — por isso a jornada é aberta no
   * servidor aqui. Antes, a prévia saía de um sorteio sem o trio e a arena
   * sorteava de novo: o jogador via um trio rival e enfrentava outro.
   */
  const preparando=useRef<Run['draft']|null>(null);
  const preparaRivais=async(r:Run)=>{
    if(preparando.current===r.draft)return;preparando.current=r.draft;
    const team=r.draft.team;let seed=r.seed,ranked=r.ranked;
    if(!ranked&&contaConectada()){
      setOnlineBusy(true);
      try{
        const result=await Promise.race([onlineCall<{run:{id:string;seed:number}}>('start',{mode:'free',team}),new Promise<never>((_,falha)=>setTimeout(()=>falha(new Error('O servidor demorou.')),8000))]);
        seed=result.run.seed;ranked={mode:'free',id:result.run.id,status:'playing'};
      }catch(error){console.warn('Jornada fora do ranking:',error instanceof Error?error.message:error);}
      finally{setOnlineBusy(false);}
    }
    const atual=runRef.current;
    if(!atual||atual.stage!=='draft'||atual.draft.team.join()!==team.join())return;
    changeRun({...atual,seed,team,encounters:generateCampaign(seed,team),ranked,preparado:true});
  };
  useEffect(()=>{
    if(run?.stage==='draft'&&run.draft.team.length===3&&!run.preparado&&!(run.ranked&&run.ranked.mode!=='free'))void preparaRivais(run);
  });
  const startBattle=async(index:number)=>{
    const current=runRef.current;if(!current)return;
    // os rivais ainda estão sendo sorteados (a prévia mostra "Sorteando os rivais…")
    if(index===0&&current.stage==='draft'&&!current.preparado&&!(current.ranked&&current.ranked.mode!=='free'))return;
    const team=current.draft.team;
    let ranked=current.ranked,seed=current.seed,encounters=current.ranked||current.preparado?current.encounters:current.stage==='draft'?generateCampaign(current.seed,team):current.encounters;
    /*
     * Toda jornada vale o ranking (Hoje, Semana e Geral). Com a conta
     * conectada, o servidor abre a jornada e sorteia os rivais (a seed); no
     * fim, ele refaz as lutas e registra a pontuação. Sem conta, sem internet
     * ou com o servidor fora, a jornada segue normal, só fora do ranking —
     * jogar nunca fica bloqueado por isso.
     */
    if(index===0&&!ranked&&!current.preparado&&current.stage==='draft'&&contaConectada()){
      setOnlineBusy(true);
      try{
        const result=await Promise.race([onlineCall<{run:{id:string;seed:number}}>('start',{mode:'free',team}),new Promise<never>((_,falha)=>setTimeout(()=>falha(new Error('O servidor demorou.')),8000))]);
        seed=result.run.seed;encounters=generateCampaign(seed,team);ranked={mode:'free',id:result.run.id,status:'playing'};
      }catch(error){console.warn('Jornada fora do ranking:',error instanceof Error?error.message:error);}
      finally{setOnlineBusy(false);}
      if(runRef.current!==current)return;
    }
    const encounter=encounters[index];
    if(index===0&&ranked&&ranked.mode!=='free'){setOnlineBusy(true);try{const result=await onlineCall<{run:{id:string;seed:number}}> ('start',{mode:ranked.mode,team});if(result.run.seed!==current.seed)throw new Error('O desafio mudou; inicie outra Jornada Ranqueada.');ranked={...ranked,id:result.run.id,status:'playing'};}catch(error){setOnlineNotice(error instanceof Error?error.message:'Jornada Ranqueada indisponível.');return;}finally{setOnlineBusy(false);}}
    const next={...current,seed,team,encounters,index,stage:'battle' as const,recorded:false,presentation:undefined,battleSynergies:[],raioX:raioXVazio(),telemetry:emptyTally(),ranked,battle:createBattle(team,encounter.team,seed+index*7919,encounter.scale)};
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
    // sair da aba não pausa mais: a luta continua (pedido do jogador); só guarda o ponto, por garantia
    const visibility=()=>{if(document.hidden)persist();};
    addEventListener('pagehide',persist);document.addEventListener('visibilitychange',visibility);
    return()=>{removeEventListener('pagehide',persist);document.removeEventListener('visibilitychange',visibility);};
  },[]);
  useEffect(()=>{
    if(screen!=='game'||paused||details||confirmNew||confirmAbandon)return;
    let previous=performance.now();
    const timer=window.setInterval(()=>{
      const now=performance.now(),bruto=Math.max(0,(now-previous)/1000),elapsed=Math.min(P.renderIntervalMs/1000,bruto);previous=now;
      // o tempo que o navegador não deixou rodar (aba escondida, app em segundo plano, celular travado)
      const atraso=bruto-elapsed;
      if(import.meta.env.DEV){const debugWindow=window as Window & {__nexusFrames?:{count:number;visualSeconds:number;lastElapsed:number}};const frames=debugWindow.__nexusFrames??{count:0,visualSeconds:0,lastElapsed:0};frames.count++;frames.visualSeconds+=elapsed;frames.lastElapsed=elapsed;debugWindow.__nexusFrames=frames;}
      const current=runRef.current;if(!current||current.stage!=='battle'||!current.battle)return;
      if(!direction.current||direction.current.battle!==current.battle){direction.current=directionFor(current);lastAudio.current=current.battle.nextEvent-1;lastDominionSound.current=current.battle.dominion;}
      const d=direction.current;
      /*
       * Jogo rodando fora da aba.
       *
       * O navegador desacelera ou congela uma aba escondida (no celular, o app
       * em segundo plano para de vez). Quando ele volta a deixar rodar, a luta
       * recupera o tempo perdido: avança quadro a quadro, sem sons nem efeitos,
       * guardando todos os sinais (Raio-X, sinergias, estatísticas), até
       * alcançar o relógio — ou até a luta acabar.
       */
      const recuperados:typeof d.signals=[];
      if(atraso>.25)divida.current=Math.min(RECUPERACAO_MAXIMA,divida.current+atraso);
      if(divida.current>1e-6){
        // no máximo um pedaço por quadro: o celular não trava, e a luta "corre" até alcançar o relógio
        let resta=Math.min(divida.current,RECUPERACAO_POR_QUADRO);divida.current-=resta;
        while(resta>1e-6&&!d.complete){const passo=Math.min(P.renderIntervalMs/1000,resta);advanceDirection(d,passo,undefined,settings.speed);recuperados.push(...d.signals);resta-=passo;}
        if(d.complete)divida.current=0;
        passoTocado.current={beat:d.active?.event.id??-1,passo:d.active?.etapa??0};
        if(recuperados.length)lastAudio.current=Math.max(lastAudio.current,...recuperados.map(e=>e.id));
      }
      const mudo=document.hidden;
      advanceDirection(d,elapsed,cue=>{
        if(mudo)return;
        if(cue.phase==='impact'&&d.active){
          // levantar/renascer: o som próprio por cima do golpe do beat
          const volta=d.active.events.find(e=>e.kind==='revive');
          if(volta)battleAudio.sound(volta.source===volta.target?'renascer':'ressurreicao',PRIORIDADE.importante,0,volta.id,volta.source===volta.target?0:.12);
          if(volta&&d.active.event.kind==='revive')return;
          // caiu, mas vai renascer: as brasas começam a crepitar logo depois do nocaute
          const brasa=d.active.events.find(e=>e.kind==='ko'&&(d.active!.after.fighters.find(f=>f.uid===e.target)?.renascendo??0)>0);
          if(brasa)battleAudio.sound('brasas-renascendo',PRIORIDADE.apoio,0,brasa.id,.45);
          // provocou: o brado por cima do golpe
          const provocou=d.active.events.find(e=>e.kind==='status'&&e.status==='provoked');
          if(provocou)battleAudio.sound('provocar',PRIORIDADE.importante,0,provocou.id,.05);
          // golpe devolvido e vida roubada: o som da mecânica, um pouco depois do golpe
          const mecanica=d.active.events.find(e=>e.kind==='damage'&&(e.label==='Refletido'||e.label==='Espinhos'))??d.active.events.find(e=>e.kind==='heal'&&(e.label==='Vampirismo'||e.label==='Roubo de vida'));
          // parte 5: errou, a Barreira anulou, e o som de cada Status novo ao entrar
          const errou=d.active.events.find(e=>e.kind==='miss');
          if(errou)battleAudio.sound(errou.label==='Esquivou'?'esquiva':'errou',PRIORIDADE.importante,0,errou.id,0);
          const criatura=d.active.event.kind==='summon'?d.active.event:undefined;
          if(criatura){const quem=d.active.after.fighters.find(f=>f.uid===criatura.source),fam=quem?FAMILIA_DA_INVOCACAO[quem.characterId]:undefined;battleAudio.sound(fam?fam.replace(/_/g,'-'):'invocacao',PRIORIDADE.importante,0,criatura.id,0);}
          const copiou=d.active.events.find(e=>e.kind==='copy');
          if(copiou)battleAudio.sound('copia',PRIORIDADE.importante,0,copiou.id,0);
          const bum=d.active.events.find(e=>e.kind==='damage'&&e.label==='Explosão');
          if(bum)battleAudio.sound('explosao',PRIORIDADE.importante,0,bum.id,0);
          const anulou=d.active.events.find(e=>e.kind==='resist');
          if(anulou)battleAudio.sound(anulou.label==='Última resistência'?'ultima-resistencia':'barreira-anula',PRIORIDADE.importante,0,anulou.id,.08);
          const SOM_DO_STATUS:Record<string,string>={poison:'veneno',bleed:'sangue',cursed:'maldicao',frozen:'bloco-de-gelo',sleep:'sono',blind:'cegueira',barrier:'barreira-magica'};
          const jaTinha=(e:BattleEvent)=>!!d.active?.before.fighters.find(f=>f.uid===e.target)?.statuses.some(s=>s.id===e.status);
          const novo=d.active.events.find(e=>e.kind==='status'&&e.status&&SOM_DO_STATUS[e.status]&&!jaTinha(e));
          if(novo?.status)battleAudio.sound(SOM_DO_STATUS[novo.status]!,PRIORIDADE.apoio,0,novo.id,.12);
          const limpeza=d.active.events.find(e=>e.kind==='cleanse'||e.kind==='dispel');
          if(limpeza)battleAudio.sound(limpeza.kind==='cleanse'?'purificacao':'dissipar',PRIORIDADE.importante,0,limpeza.id,.1);
          if(mecanica)battleAudio.sound(mecanica.label==='Refletido'?'reflexo':mecanica.label==='Espinhos'?'espinhos':'vampirismo',PRIORIDADE.importante,0,mecanica.id,.14);
          // o golpe final da série tem o som dele junto do golpe (as outras mecânicas tocam no passo delas)
          const serie=efeitosDoJeito(d.active.event,[],d.active.after.fighters)[0];
          if(serie)battleAudio.sound(somDoJeito(serie.familia),PRIORIDADE.importante,0,d.active.event.id*10+9,.02);
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
      if(recuperados.length)d.signals=[...recuperados,...d.signals];
      const fighters=d.visible.fighters,critical=fighters.filter(f=>f.hp>0&&f.hp/f.maxHp<.34).length,casts=fighters.filter(f=>f.hp>0&&f.cast).length;
      battleAudio.setMood({heat:Math.min(1,.15+critical*.13+casts*.17+Math.abs(d.visible.dominion)/150),pressure:d.visible.dominion/100,time:Math.min(1,d.visible.time/120)});
      if(Math.abs(d.visible.dominion-lastDominionSound.current)>=20){if(!mudo)battleAudio.sound('toque',PRIORIDADE.interface);lastDominionSound.current=d.visible.dominion;}
      // cada passo da cadeia (depois do golpe) tem o seu som: reação, debuff, buff, cura, escudo
      const ativo=d.active;
      if(ativo?.impacted&&ativo.passos&&ativo.etapa&&!mudo){
        const visto=passoTocado.current.beat===ativo.event.id?passoTocado.current.passo:0;
        // o primeiro passo já tem o som do golpe; um traço sozinho começa direto na reação
        for(let k=Math.max(ativo.passos[0]?.classe==='reacao'?1:2,visto+1);k<=ativo.etapa;k++){
          const passo=ativo.passos[k-1];if(!passo)continue;
          const eventos=ativo.events.filter(e=>passo.eventos.includes(e.id));
          // buff ou debuff que o alvo já tinha só renova o tempo: som curto e macio, não o de entrar (pedido do jogador)
          const status=eventos.filter(e=>e.kind==='status');
          const renova=status.length>0&&status.length===eventos.length&&status.every(e=>ativo.before.fighters.find(f=>f.uid===e.target)?.statuses.some(s=>s.id===e.status));
          const som:Sound=passo.classe==='reacao'?'reacao':passo.classe==='rival'?(renova?'renova-debuff':'enfraquecer'):eventos.some(e=>e.kind==='heal')?'cura':eventos.some(e=>e.kind==='shield')?'escudo':renova?'renova-buff':'reforco';
          // o passo de um jeito de bater (Ricochete, Roubou Carga…) toca o som próprio da mecânica
          const jeito=efeitosDoJeito({...ativo.event,kind:'skill'},eventos,ativo.after.fighters);
          if(jeito.length){jeito.forEach((x,i)=>battleAudio.sound(somDoJeito(x.familia),PRIORIDADE.habilidade,0,ativo.event.id*10+k+i*1000,x.atraso));continue;}
          battleAudio.sound(som,passo.classe==='reacao'?PRIORIDADE.habilidade:PRIORIDADE.apoio,0,ativo.event.id*10+k);
        }
        passoTocado.current={beat:ativo.event.id,passo:ativo.etapa};
      }
      const ready=d.signals.find(e=>e.id>lastAudio.current&&e.kind==='ready');
      if(ready&&!mudo)battleAudio.sound('pronto',PRIORIDADE.interface,0,ready.id);
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
        const summary={...summarizeBattle(current.index,d.battle,battleSynergies,current.dicas===true),recordeAntes:current.recorded?undefined:loadProfile().recordePontos??0};
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
      try{const digest=await runDigest(id,run.team,run.seed,(run.summaries??[]).map(s=>s.won));const result=await onlineCall<{score:number;daily:number|null;weekly:number|null;season:number|null;top3?:{periodo?:ResultadoTop3;temporada?:ResultadoTop3}}>('submit',{runId:id,digest,dicas:run.dicas===true});
        const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'verified',score:result.score,daily:result.daily,weekly:result.weekly,season:result.season,top3:result.top3,error:undefined}});
      }catch(error){const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'failed',error:error instanceof Error?error.message:'Falha na validação.'}});}
      finally{submission.current=false;}
    })();
  },[run?.stage,run?.index,run?.battle?.winner,run?.ranked?.status,run?.ranked?.id]);
  useEffect(()=>{battleAudio.configure(settings);},[settings]);
  /* versão nova publicada enquanto a aba estava aberta (src/main.tsx): oferece recarregar */
  const [versaoNova,setVersaoNova]=useState(false);
  useEffect(()=>{const ouve=()=>setVersaoNova(true);window.addEventListener('nexus:versao-nova',ouve);return()=>window.removeEventListener('nexus:versao-nova',ouve);},[]);
  useEffect(()=>{battleAudio.setBattle(screen==='game'&&run?.stage==='battle'&&!paused&&!details&&!confirmNew&&!confirmAbandon,run?`${run.seed}-${run.index}`:undefined,faixaDaLuta(run?.index??0),run&&run.index<9?faixaDaLuta(run.index+1):undefined);return()=>battleAudio.setBattle(false);},[screen,run?.stage,run?.seed,run?.index,paused,details,confirmNew,confirmAbandon]);
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
  /* O botão das Dicas de trio: a conta do dono sempre; os outros depois de META_DAS_DICAS numa jornada (src/lib/dicas-liberadas.ts) */
  const [dono,setDono]=useState(false);
  useEffect(()=>{let vivo=true;void ehDono(conta?.email).then(d=>{if(vivo)setDono(d);});return ()=>{vivo=false;};},[conta?.email]);
  const podeDicas=dicasLiberadas(dono,profile.recordePontos??0);
  /* Dicas ligadas enquanto o trio é escolhido: a jornada inteira paga o custo, mesmo desligando depois (src/engine/pontos.ts) */
  useEffect(()=>{if(settings.dicasDoTrio&&podeDicas&&run?.stage==='draft'&&run.draft.team.length<3&&!run.dicas)changeRun({...run,dicas:true});},[settings.dicasDoTrio,podeDicas,run?.stage,run?.draft.team.length,run?.dicas]);

  const reset=()=>{resetStorage();setSettings(defaults);setProfile({journeys:0,victories:0,best:0,wins:0,recordePontos:0,escalaDosPontos:ESCALA_DOS_PONTOS});setRun(null);runRef.current=null;navigate('home');};
  return <div onPointerDownCapture={()=>void battleAudio.unlock()} onPointerUpCapture={()=>void battleAudio.unlock()} onTouchEndCapture={()=>void battleAudio.unlock()} onClickCapture={()=>void battleAudio.unlock()} onKeyDownCapture={e=>{if(e.key==='Enter'||e.key===' ')void battleAudio.unlock();}} className={`app ${settings.reducedMotion?'reduce-motion':''} ${screen==='game'&&run?.stage==='battle'?'in-battle':''}`}>
    <ToqueGlobal/>
    <Cabecalho tela={screen} menu={menu} onMenu={setMenu} onNavigate={navigate} recorde={profile.recordePontos??0} apelido={profile.publicHandle} online={onlineConfigured} total={characters.length}/>
    <main key={`${screen}-${screen==='game'?run?.stage??'idle':'page'}`} className={screen==='game'&&run?.stage==='battle'?'main battle-main screen-enter':'main screen-enter'}>
      {screen==='home'&&<Home profile={profile} run={run} conta={conta!==null&&conta.origem!=='convidado'} onPlay={requestNew} onContinue={()=>{if(run?.stage==='battle'&&run.battle){direction.current=directionFor(run);setPresentation({battle:direction.current.visible,beat:direction.current.active});}navigate('game');setPaused(run?.stage==='battle');}} onAbandon={()=>setConfirmAbandon(true)} onNavigate={navigate} onInstall={()=>void install()}/>}
      {screen==='characters'&&<CharactersScreen onDetails={setDetails}/>}
      {screen==='ranking'&&<RankingScreen handle={profile.publicHandle} conta={conta!==null&&conta.origem!=='convidado'} onConta={()=>navigate('conta')} recorde={profile.recordePontos??0}/>}
      {screen==='conta'&&<AccountScreen autenticacao={autenticacao} conta={conta} profile={profile} conectado={onlineConfigured} google={googleConfigured} aoMudarPerfil={p=>{save('profile',p);setProfile(p);}}/>}
      {screen==='help'&&<HelpScreen onPlay={requestNew}/>}
      {screen==='settings'&&<SettingsScreen settings={settings} onChange={changeSettings} onReset={reset} onGaleria={()=>navigate('vfx')} ranking={onlineConfigured?{nome:profile.publicHandle,onEditar:()=>{setPendingStart(false);setDraftHandle(profile.publicHandle??'');setNameDialog(true);}}:undefined}/>}
      {screen==='game'&&run?.stage==='draft'&&<DraftScreen draft={run.draft} primeiroRival={run.preparado||run.ranked&&run.ranked.mode!=='free'?run.encounters[0]:undefined} dicas={settings.dicasDoTrio&&podeDicas} podeDicas={podeDicas} usouDicas={run.dicas===true} onDicas={ligar=>changeSettings({...settings,dicasDoTrio:ligar})} onPick={id=>changeRun({...run,draft:pickDraft(run.draft,id)})} onSkip={()=>changeRun({...run,draft:skipDraft(run.draft)})} onDetails={setDetails} onStart={()=>void startBattle(0)} onAbandon={()=>setConfirmAbandon(true)}/>}
      {screen==='game'&&run?.stage==='battle'&&run.battle&&<BattleScreen battle={presentation&&direction.current?.battle===run.battle?presentation.battle:run.battle} beat={presentation&&direction.current?.battle===run.battle?presentation.beat:null} index={run.index} name={run.encounters[run.index].name} settings={settings} paused={paused||!!details}  onPause={()=>setPaused(!paused)} onAbandon={()=>setConfirmAbandon(true)} onSettings={changeSettings} onExit={()=>{setPaused(true);navigate('home');}}/>}
      {screen==='game'&&run?.stage==='result'&&<ResultScreen run={run} onNext={()=>void startBattle(run.index+1)} onRestart={requestNew} onAbandon={()=>setConfirmAbandon(true)} onHome={()=>navigate('home')} onRanking={()=>navigate('ranking')} onRetry={()=>{if(run.ranked)changeRun({...run,ranked:{...run.ranked,status:'validating'}});}} auto={settings.auto} onAuto={auto=>changeSettings({...settings,auto})}/>}
      {screen==='debug'&&import.meta.env.DEV&&<Suspense fallback={<p>Carregando laboratório…</p>}><DebugScreen/></Suspense>}
      {screen==='vfx'&&<Suspense fallback={<p>Carregando galeria audiovisual…</p>}><VfxLabScreen/></Suspense>}
      {!storageAvailable&&<p role="alert" className="storage-warning">Não foi possível salvar neste navegador. Sua sessão continua, mas pode não ser recuperada ao fechar.</p>}
    </main>
    {details&&<CharacterModal character={byId[details]} onClose={()=>setDetails(null)}/>}
    {confirmNew&&<InfoDialog title="Começar uma nova jornada?" icone={<RotateCcw/>} cor="#ffb86b" onClose={()=>setConfirmNew(false)}><p>A jornada de agora some. <b>Seu recorde fica salvo.</b></p><div className="result-actions"><button className="danger" onClick={()=>void startNew()}>Descartar e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmNew(false)}>Continuar jornada</button></div></InfoDialog>}
    {nameDialog&&<InfoDialog title="Seu nome no ranking" icone={<UserPen/>} cor="#86e3a8" onClose={()=>{setNameDialog(false);/* sem nome, a jornada começa do mesmo jeito, só fora do ranking */if(pendingStart){setPendingStart(false);abreJornada();}}}><p>De 3 a 16 letras. Aparece junto do seu trio e dos seus pontos.</p><input className="handle-input" aria-label="Nome público" maxLength={16} value={draftHandle} onChange={e=>setDraftHandle(e.target.value)} placeholder="Seu nome no Nexus"/><p>Prévia: <strong>{draftHandle.trim()||'Seu nome'}</strong></p><button className="primary" disabled={onlineBusy} onClick={()=>void saveHandle()}>Confirmar nome</button></InfoDialog>}
    {versaoNova&&<div className="versao-nova" role="status"><span><b>Nova versão do jogo</b><small>Atualize para suas jornadas valerem no ranking.</small></span><button className="primary" onClick={()=>location.reload()}><RotateCcw size={16}/>Atualizar</button></div>}
    {onlineNotice&&<InfoDialog title="Conexão do ranking" icone={<WifiOff/>} cor="#ff9a8a" onClose={()=>setOnlineNotice('')}><p role="alert">{onlineNotice}</p><button className="primary" onClick={()=>setOnlineNotice('')}>Entendi</button></InfoDialog>}
    {confirmAbandon&&<InfoDialog title="Desistir desta jornada?" icone={<Flag/>} cor="#ff7a6b" onClose={()=>setConfirmAbandon(false)}><p>A jornada de agora some e você monta um trio novo. <b>Seu recorde fica salvo.</b></p><div className="result-actions"><button className="danger" onClick={startNew}>Desistir e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmAbandon(false)}>Continuar jornada</button></div></InfoDialog>}
    {installHelp&&<InfoDialog title={installed?'O NEXUS já está instalado':'Leve seu trio no bolso'} icone={<Download/>} cor="#8fd3ff" onClose={()=>setInstallHelp(false)}><p>{installed?'Abra o jogo pelo ícone na tela inicial do aparelho.':<><b>Android:</b> menu do navegador → “Instalar aplicativo”.<br/><b>iPhone:</b> Compartilhar → “Adicionar à Tela de Início”.</>}</p><p>O progresso fica neste aparelho e o jogo abre mesmo sem internet.</p><button className="primary" onClick={()=>setInstallHelp(false)}>Entendi</button></InfoDialog>}
  </div>;
}
