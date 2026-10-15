import {lazy,Suspense,useEffect,useRef,useState,useMemo} from 'react';
import { ArrowUpRight,Download,Flag,RotateCcw,UserPen,WifiOff,X } from 'lucide-react';
import { Home } from './screens/Home';
import { DraftScreen } from './screens/DraftScreen';
import { BattleScreen } from './screens/BattleScreen';
import { ResultScreen } from './screens/ResultScreen';
import { ESPERA_DA_PROXIMA_MS } from './components/ChaveDoAuto';
import { RankingScreen } from './screens/RankingScreen';
import { CharactersScreen } from './screens/Auxiliary';
import { HelpScreen } from './screens/ComoJogar';
import { SettingsScreen } from './screens/Ajustes';
import { LivroDeCombos } from './screens/LivroDeCombos';
import { CharacterModal } from './components/CharacterModal';
import { CompartilharJogo } from './components/CompartilharJogo';
import { BoasVindasDoConvite } from './components/BoasVindasDoConvite';
import { Cabecalho,ToqueGlobal } from './components/Casca';
import { byId,characters } from './data/characters';
import { createBattle } from './engine/battle';
import { candidates,generateCampaign,newDraft,pickDraft,skipDraft } from './engine/campaign';
import type { ResultadoTop3 } from './lib/top3';
import { defaults,ESCALA_DOS_PONTOS,loadProfile,loadRun,loadSettings,resetStorage,save,storageAvailable } from './lib/storage';
import type { Run,Settings } from './lib/storage';
import type { NovosNoLivro } from './components/CombosDoTrio';
import { PRIORIDADE } from './audio/cues';
import { battleAudio,faixaDaLuta } from './lib/audio';
import { createDirection,restoreDirection,checkpointDirection,advanceDirection,type Direction,type Beat,type BeatTrace } from './presentation/director';
import { PRESENTATION as P } from './presentation/config';
import { somDoCue,sonsDoQuadro } from './presentation/sons-da-luta';
import type { Battle } from './engine/types';
import { addSynergies,summarizeBattle } from './engine/run-summary';
import { acumularRaioX,ajudasDaLuta,raioXVazio } from './engine/raio-x';
import {emptyTally,tallyEvents} from './engine/progression';
import { pontosDaJornada } from './engine/pontos';
import {runDigest} from './engine/ranked';
import {PULOS_DO_DESAFIO,liberar} from './lib/conquistas';
import {ConquistasScreen} from './screens/ConquistasScreen';
import {carregarCliente,googleConfigured,haSessaoOuRetorno,onlineCall,onlineConfigured} from './lib/online';
import {criarAutenticacaoPreguicosa,validarHandle,type Conta} from './lib/auth';
import { dicasLiberadas,ehDono } from './lib/dicas-liberadas';
import { guardarEnvio,recusaDefinitiva,reenviarPendentes } from './lib/envios-pendentes';
import {AccountScreen} from './screens/AccountScreen';
import {PortaoDaConta,type EtapaDoPortao} from './screens/PortaoDaConta';
import {criarComunidade,type ServicoDaComunidade} from './lib/comunidade';
import {useComunidade} from './lib/useComunidade';
import {Avatar} from './components/AvatarDaComunidade';
const PvpScreen=lazy(()=>import('./screens/PvpScreen').then(m=>({default:m.PvpScreen})));
const ComunidadeScreen=lazy(()=>import('./screens/ComunidadeScreen').then(m=>({default:m.ComunidadeScreen})));
/* A prévia da Comunidade sem servidor (VITE_COMUNIDADE_DEMO=true): só para testar a tela; nunca no jogo publicado. */
const COMUNIDADE_DEMO=import.meta.env.VITE_COMUNIDADE_DEMO==='true';
const DebugScreen=lazy(()=>import('./screens/DebugScreen').then(m=>({default:m.DebugScreen})));
const VfxLabScreen=lazy(()=>import('./screens/VfxLabScreen').then(m=>({default:m.VfxLabScreen})));
type Screen='home'|'game'|'characters'|'conquistas'|'combos'|'ranking'|'conta'|'help'|'settings'|'debug'|'vfx'|'comunidade'|'pvp';
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
  const [paused,setPaused]=useState(false),[details,setDetails]=useState<string|null>(null),[menu,setMenu]=useState(false),[installHelp,setInstallHelp]=useState(false),[compartilhar,setCompartilhar]=useState(false),[convite,setConvite]=useState(()=>typeof location!=='undefined'&&new URLSearchParams(location.search).has('convite')&&!matchMedia('(display-mode: standalone)').matches),[confirmNew,setConfirmNew]=useState(false),[confirmAbandon,setConfirmAbandon]=useState(false);
  const [onlineNotice,setOnlineNotice]=useState(''),[acaoDoAviso,setAcaoDoAviso]=useState<'nome'|'atualizar'|'tentar'|null>(null),[nameDialog,setNameDialog]=useState(false),[draftHandle,setDraftHandle]=useState(''),[pendingStart,setPendingStart]=useState(false),[onlineBusy,setOnlineBusy]=useState(false);
  const submission=useRef(false);
  const [installEvent,setInstallEvent]=useState<InstallEvent|null>(null),[installed,setInstalled]=useState(()=>matchMedia('(display-mode: standalone)').matches);
  const runRef=useRef(run),lastSave=useRef(0);runRef.current=run;
  const direction=useRef<Direction|null>(null);
  const [presentation,setPresentation]=useState<{battle:Battle;beat:Beat|null}|null>(null);
  const lastAudio=useRef(0),lastDominionSound=useRef(0),passoTocado=useRef({beat:-1,passo:1}),unicaTocada=useRef<number|null>(null),apoioTocado=useRef<number|null>(null),pausasTocadas=useRef(new Set<string>()),divida=useRef(0);
  /* os sons da luta (src/presentation/sons-da-luta.ts), com o que já tocou guardado nestas refs */
  const sons=useMemo(()=>({lastAudio,lastDominionSound,passoTocado,unicaTocada,apoioTocado,pausasTocadas}),[]);
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
  /* A aba em que o Ranking abre: vindo das Conquistas, já na de conquistas. */
  const [rankingInicial,setRankingInicial]=useState<'daily'|'conquistas'>('daily');
  const navigate=(next:Screen)=>{if(next!=='game')setPaused(true);if(next!=='ranking')setRankingInicial('daily');setScreen(next);setMenu(false);window.scrollTo(0,0);};
  /*
   * Um jogo só, e ele é ranqueado (pedido do jogador: "não existe casual e
   * ranqueada, tudo é ranqueado"). Com a conta conectada, falta só o nome
   * público: na primeira jornada sem ele, o jogo pede o nome e segue.
   */
  const contaConectada=()=>onlineConfigured&&conta!==null&&conta.origem!=='convidado';
  const saveHandle=async()=>{
    setOnlineBusy(true);
    try{const response=await onlineCall<{profile:{handle:string}}> ('profile',{handle:draftHandle});setProfile(p=>{const n={...p,publicHandle:response.profile.handle};save('profile',n);return n;});setNameDialog(false);if(pendingStart){setPendingStart(false);abreJornada();}else tentarDeNovo();}
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
  /* O Desafio do Dia escolhido (src/lib/conquistas.ts): a próxima Jornada começa com ele no trio e mais trocas. */
  const desafioPendente=useRef<string|null>(null);
  /*
   * Desistir no meio conta como perder (pedido do dono: "se ela fez 700 pontos e desistiu com 700, conta que ela fez
   * 700"): a jornada de agora fecha com as lutas já terminadas e vai para o ranking.
   */
  const fechaDesistindo=(atual:Run|null)=>{
    if(!atual?.ranked?.id||!['playing','validating'].includes(atual.ranked.status))return;
    const terminou=atual.stage==='result'&&(atual.battle?.winner!=='player'||atual.index===9);if(terminou)return;
    const lista=atual.summaries??[],id=atual.ranked.id,envio={dicas:atual.dicas===true,vencidas:lista.filter(x=>x.won).length,desistiu:true,lutas:lista.length};
    void runDigest(id,atual.team,atual.seed,lista.map(x=>x.won)).then(digest=>onlineCall('submit',{runId:id,digest,...envio}).catch(e=>{
      if(!recusaDefinitiva(e instanceof Error?e.message:''))guardarEnvio({runId:id,digest,em:new Date().toISOString(),...envio});}));
  };
  const abreJornada=()=>{
    fechaDesistindo(runRef.current);
    const seed=crypto.getRandomValues(new Uint32Array(1))[0];
    const escolhido=desafioPendente.current;desafioPendente.current=null;
    let draft=newDraft(seed);
    if(escolhido){draft={...draft,team:[escolhido],skips:PULOS_DO_DESAFIO};draft={...draft,candidates:candidates(draft)};}
    changeRun({seed,team:[],encounters:generateCampaign(seed),index:0,stage:'draft',draft,battle:null,recorded:false,summaries:[],...(escolhido?{desafio:escolhido}:{})});setPaused(false);setConfirmNew(false);setConfirmAbandon(false);navigate('game');
  };
  const jogarDesafio=(id:string)=>{desafioPendente.current=id;if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else void startNew();};
  const requestNew=()=>{desafioPendente.current=null;if(run&&(run.stage!=='result'||run.battle?.winner==='player'&&run.index<9))setConfirmNew(true);else void startNew();};
  /*
   * Os rivais da jornada saem assim que o trio fica pronto, não ao entrar na
   * arena: assim a "Primeira luta" mostrada na escolha é exatamente a luta que
   * vem. Eles dependem do trio (ninguém repete) e, com a conta conectada, da
   * seed que o servidor do ranking sorteia — por isso a jornada é aberta no
   * servidor aqui. Antes, a prévia saía de um sorteio sem o trio e a arena
   * sorteava de novo: o jogador via um trio rival e enfrentava outro.
   */
  /*
   * Abre a jornada no servidor do ranking (pedido do jogador: "o meu amigo
   * consegue ver eu no ranking, mas eu não consigo ver ele"). Antes, qualquer
   * falha aqui deixava a jornada fora do ranking em silêncio: o servidor frio
   * que passava de 8 s, a conta sem nome público, o jogo numa versão velha
   * guardada no celular (o servidor refaz as lutas com a versão dele, e elas
   * não batem). Agora o servidor tem 20 s e uma segunda tentativa, e o motivo
   * aparece com o que fazer.
   *
   * O jogo numa versão velha não barra mais a jornada (pedido do dono do jogo:
   * "quero que ela entre direto, sem autorização"): o servidor refaz as lutas
   * com a versão dele e é esse resultado que entra no ranking.
   */
  const abrirNoRanking=async(team:string[])=>{
    const pede=()=>Promise.race([onlineCall<{run:{id:string;seed:number;engine_version?:string;roster_fingerprint?:string}}>('start',{mode:'free',team}),new Promise<never>((_,falha)=>setTimeout(()=>falha(new Error('O servidor demorou para responder.')),20000))]);
    let result;
    try{result=await pede();}
    catch(error){
      const msg=error instanceof Error?error.message:'';
      if(!/demorou|fetch|network|rede|indispon/i.test(msg))throw error;
      await new Promise(r=>setTimeout(r,1500));result=await pede();
    }
    return result.run;
  };
  const avisaForaDoRanking=(error:unknown)=>{
    const msg=error instanceof Error?error.message:'';
    if(/nome p[uú]blico/i.test(msg)){setAcaoDoAviso('nome');setOnlineNotice('Falta escolher o seu nome público: sem ele, as jornadas não entram no ranking.');}
    else{setAcaoDoAviso('tentar');setOnlineNotice(`Não deu para registrar esta jornada no ranking agora${msg?` (${msg})`:''}. Se começar assim, ela fica fora do ranking.`);}
  };
  const preparando=useRef<Run['draft']|null>(null);
  const preparaRivais=async(r:Run)=>{
    if(preparando.current===r.draft)return;preparando.current=r.draft;
    const team=r.draft.team;let seed=r.seed,ranked=r.ranked;
    if(!ranked&&contaConectada()){
      setOnlineBusy(true);
      try{
        const aberta=await abrirNoRanking(team);
        seed=aberta.seed;ranked={mode:'free',id:aberta.id,status:'playing'};
      }catch(error){console.warn('Jornada fora do ranking:',error instanceof Error?error.message:error);avisaForaDoRanking(error);}
      finally{setOnlineBusy(false);}
    }
    const atual=runRef.current;
    if(!atual||atual.stage!=='draft'||atual.draft.team.join()!==team.join())return;
    changeRun({...atual,seed,team,encounters:generateCampaign(seed,team),ranked,preparado:true});
  };
  const tentarDeNovo=()=>{const atual=runRef.current;if(!atual||atual.stage!=='draft'||atual.ranked)return;preparando.current=null;void preparaRivais({...atual,preparado:false});};
  useEffect(()=>{
    if(run?.stage==='draft'&&run.draft.team.length===3&&!run.preparado&&!(run.ranked&&run.ranked.mode!=='free'))void preparaRivais(run);
  });
  const startBattle=async(index:number)=>{
    const current=runRef.current;if(!current)return;
    // os rivais ainda estão sendo sorteados (a prévia mostra "Escolhendo rivais aleatórios…")
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
        const aberta=await abrirNoRanking(team);
        seed=aberta.seed;encounters=generateCampaign(seed,team);ranked={mode:'free',id:aberta.id,status:'playing'};
      }catch(error){console.warn('Jornada fora do ranking:',error instanceof Error?error.message:error);avisaForaDoRanking(error);}
      finally{setOnlineBusy(false);}
      if(runRef.current!==current)return;
    }
    const encounter=encounters[index];
    if(index===0&&ranked&&ranked.mode!=='free'){setOnlineBusy(true);try{const result=await onlineCall<{run:{id:string;seed:number}}> ('start',{mode:ranked.mode,team});if(result.run.seed!==current.seed)throw new Error('O desafio mudou; inicie outra Jornada Ranqueada.');ranked={...ranked,id:result.run.id,status:'playing'};}catch(error){setOnlineNotice(error instanceof Error?error.message:'Jornada Ranqueada indisponível.');return;}finally{setOnlineBusy(false);}}
    const next={...current,seed,team,encounters,index,stage:'battle' as const,recorded:false,presentation:undefined,battleSynergies:[],raioX:raioXVazio(),telemetry:emptyTally(),ranked,battle:createBattle(team,encounter.team,seed+index*7919,encounter.scale)};
    direction.current=null;setPresentation(null);changeRun(next);setPaused(false);navigate('game');
    if(index===0)setProfile(p=>{const n={...p,journeys:p.journeys+1};save('profile',n);return n;});
    /* Livro de Combos: um combo é descoberto quando o trio do jogador forma ele, ou quando ele vê o rival usar (pedido do jogador) */
    const meus=next.battle.combos?.player.map(c=>c.id)??[],deles=next.battle.combos?.enemy.map(c=>c.id)??[];
    const ja=profile.combosDescobertos??[],novos=[...new Set([...meus,...deles])].filter(id=>!ja.includes(id));
    setNovosNoLivro(novos.length?{chave:`${index}-${next.battle.seed}`,ids:novos,doRival:novos.filter(id=>!meus.includes(id))}:null);
    if(novos.length)setProfile(p=>{const antes=p.combosDescobertos??[],soma=novos.filter(id=>!antes.includes(id));if(!soma.length)return p;const n={...p,combosDescobertos:[...antes,...soma]};save('profile',n);return n;});
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
        somDoCue(d,cue);
      },settings.speed,import.meta.env.DEV?trace=>{
        const devWindow=window as Window & {__nexusBeatTrace?:BeatTrace[]};
        const history=devWindow.__nexusBeatTrace??=[];
        history.push(trace);if(history.length>2000)history.shift();
      }:undefined);
      if(recuperados.length)d.signals=[...recuperados,...d.signals];
      sonsDoQuadro(d,sons,mudo);
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
        const summary={...summarizeBattle(current.index,d.battle,battleSynergies,current.dicas===true),recordeAntes:current.recorded?undefined:loadProfile().recordePontos??0,ajudas:ajudasDaLuta(raioX,d.battle)};
        next={...next,stage:'result',recorded:true,summaries:current.recorded?current.summaries:[...(current.summaries??[]).filter(s=>s.index!==current.index),summary]};
        if(!current.recorded){
          /* conta ao servidor como a jornada está: se o envio do fim não chegar, o servidor a coloca no ranking sozinho */
          if(current.ranked?.id&&current.ranked.status==='playing'){const lista=next.summaries??[],perdeu=d.battle.winner!=='player';
            void onlineCall('progresso',{runId:current.ranked.id,lutas:lista.length,vencidas:lista.filter(x=>x.won).length,fim:perdeu||current.index===9,dicas:current.dicas===true}).catch(()=>{});}
          const won=d.battle.winner==='player',champion=won&&current.index===9;
          /* o objetivo do jogo: pontos. O recorde é o maior total de uma jornada. */
          const total=pontosDaJornada((next.summaries??[]).map(x=>({pontos:x.score,won:x.won})));
          /* Terminou as 10 lutas: o trio libera as Conquistas de quem ainda não tinha (só a primeira vez conta). */
          if(champion){const novas=liberar(loadProfile().conquistas??{},current.team).novas;if(novas.length)next={...next,conquistasNovas:novas};}
          setProfile(p=>{
            const n={...p,...(champion?{conquistas:liberar(p.conquistas??{},current.team).conquistas}:{}),best:Math.max(p.best,current.index+(won?1:0)),wins:p.wins+(won?1:0),victories:p.victories+Number(champion),champion:champion?[...current.team]:p.champion,recordePontos:Math.max(p.recordePontos??0,total)};
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
    const id=window.setTimeout(()=>{const current=runRef.current;if(!current)return;const index=current.index+1,encounter=current.encounters[index];const next={...current,index,stage:'battle' as const,recorded:false,presentation:undefined,battleSynergies:[],raioX:raioXVazio(),telemetry:emptyTally(),battle:createBattle(current.team,encounter.team,current.seed+index*7919,encounter.scale)};runRef.current=next;setRun(next);save('run',next);setPaused(false);},ESPERA_DA_PROXIMA_MS);
    return()=>clearTimeout(id);
  },[screen,settings.auto,run?.stage,run?.index,run?.battle?.winner]);
  useEffect(()=>{
    if(!run?.ranked?.id||run.stage!=='result'||run.battle?.winner==='player'&&run.index<9||!['playing','validating'].includes(run.ranked.status)||submission.current)return;
    submission.current=true;const id=run.ranked.id;
    if(run.ranked.status!=='validating')changeRun({...run,ranked:{...run.ranked,status:'validating'}});
    void (async()=>{
      try{const digest=await runDigest(id,run.team,run.seed,(run.summaries??[]).map(s=>s.won));const result=await onlineCall<{score:number;daily:number|null;weekly:number|null;season:number|null;top3?:{periodo?:ResultadoTop3;temporada?:ResultadoTop3}}>('submit',{runId:id,digest,dicas:run.dicas===true,vencidas:(run.summaries??[]).filter(s=>s.won).length});
        const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'verified',score:result.score,daily:result.daily,weekly:result.weekly,season:result.season,top3:result.top3,error:undefined}});
      }catch(error){const msg=error instanceof Error?error.message:'Falha na validação.';
        // falhou por rede ou servidor: fica guardada e é reenviada sozinha ao abrir o jogo (src/lib/envios-pendentes.ts)
        if(!recusaDefinitiva(msg))void runDigest(id,run.team,run.seed,(run.summaries??[]).map(s=>s.won)).then(digest=>guardarEnvio({runId:id,digest,dicas:run.dicas===true,em:new Date().toISOString(),vencidas:(run.summaries??[]).filter(s=>s.won).length}));
        const latest=runRef.current;if(latest?.ranked?.id===id)changeRun({...latest,ranked:{...latest.ranked,status:'failed',error:msg}});}
      finally{submission.current=false;}
    })();
  },[run?.stage,run?.index,run?.battle?.winner,run?.ranked?.status,run?.ranked?.id]);
  useEffect(()=>{battleAudio.configure(settings);},[settings]);
  /* versão nova publicada enquanto a aba estava aberta (src/main.tsx): oferece recarregar */
  const [versaoNova,setVersaoNova]=useState(false);
  /*
   * Fora de uma jornada em andamento, a versão nova entra sozinha (recarrega): o celular que deixou o
   * jogo aberto em segundo plano não fica jogando a versão velha, que o ranking recusa.
   */
  const telaAtual=useRef(screen);telaAtual.current=screen;
  useEffect(()=>{const ouve=()=>{const r=runRef.current,emJornada=telaAtual.current==='game'&&!!r&&r.stage!=='draft'&&!(r.stage==='result'&&(r.battle?.winner!=='player'||r.index>=9));if(emJornada)setVersaoNova(true);else location.reload();};window.addEventListener('nexus:versao-nova',ouve);return()=>window.removeEventListener('nexus:versao-nova',ouve);},[]);
  useEffect(()=>{battleAudio.setBattle(screen==='game'&&run?.stage==='battle'&&!paused&&!details&&!confirmNew&&!confirmAbandon,run?`${run.seed}-${run.index}`:undefined,faixaDaLuta(run?.index??0),run&&run.index<9?faixaDaLuta(run.index+1):undefined);return()=>battleAudio.setBattle(false);},[screen,run?.stage,run?.seed,run?.index,paused,details,confirmNew,confirmAbandon]);
  const install=async()=>{if(installEvent){await installEvent.prompt();const choice=await installEvent.userChoice;setInstallEvent(null);if(choice.outcome!=='accepted')setInstallHelp(true);}else setInstallHelp(true);};
  /* o convite (src/components/BoasVindasDoConvite.tsx): instala pelo pedido do próprio celular e diz se deu certo */
  const instalarDoConvite=async()=>{if(!installEvent)return false;await installEvent.prompt();const choice=await installEvent.userChoice;setInstallEvent(null);return choice.outcome==='accepted';};
  const fecharConvite=()=>{setConvite(false);const url=new URL(location.href);url.searchParams.delete('convite');history.replaceState(history.state,'',url);};
  /*
   * A conta vive fora do React: o Supabase mantém a sessão no armazenamento
   * dele e avisa por evento. Aqui só se espelha o que ele diz, incluindo a
   * sessão que expirou — nesse caso o jogador volta a ser convidado e o jogo
   * casual segue igual.
   */
  const autenticacao=useMemo(()=>criarAutenticacaoPreguicosa(carregarCliente),[]);
  const [conta,setConta]=useState<Conta|null>(null);
  /* Sem sessão guardada nem volta de link, não há conta a descobrir: a porta já abre no cadastro. */
  const [contaPronta,setContaPronta]=useState(()=>!haSessaoOuRetorno());
  useEffect(()=>{
    let vivo=true;
    if(haSessaoOuRetorno())void autenticacao.conta().then((c:Conta|null)=>{if(vivo){setConta(c);setContaPronta(true);}});
    const parar=autenticacao.observar((c:Conta|null)=>{setConta(c);setContaPronta(true);});
    return ()=>{vivo=false;parar();};
  },[autenticacao]);
  /*
   * O nome público da conta, no servidor (src/screens/PortaoDaConta.tsx). O nome escolhido no cadastro
   * vinha só nos dados de login, e o perfil público só nascia se o jogo pedisse — sem ele, o servidor
   * recusava as jornadas. Agora, ao entrar, o perfil é conferido e, se faltar, criado com esse nome.
   */
  const logado=conta!==null&&conta.origem!=='convidado';
  /* Acabou de entrar na conta (pela porta ou pela tela de Conta): o jogo vai para o início, não fica na tela de sair. */
  const estavaLogado=useRef<boolean|null>(null);
  useEffect(()=>{if(estavaLogado.current===false&&logado)navigate('home');if(contaPronta)estavaLogado.current=logado;},[logado,contaPronta]);
  const [nomeDaConta,setNomeDaConta]=useState<{id:string;handle:string|null}|null>(null);
  const [erroDaConta,setErroDaConta]=useState('');
  /** Os combos que a luta de agora acabou de pôr no Livro (o aviso na abertura da luta). */
  const [novosNoLivro,setNovosNoLivro]=useState<NovosNoLivro|null>(null);
  const buscaNome=async(c:Conta)=>{
    setErroDaConta('');
    try{
      const r=await onlineCall<{profile:{handle:string}|null}>('profile');
      let handle=r.profile?.handle??null;
      if(!handle&&c.handle&&!validarHandle(c.handle)){try{handle=(await onlineCall<{profile:{handle:string}}>('profile',{handle:c.handle})).profile.handle;}catch{/* o nome já tem dono: escolhe outro na porta */}}
      if(handle){const h=handle;setProfile(p=>{const n={...p,publicHandle:h};save('profile',n);return n;});}
      setNomeDaConta({id:c.id,handle});
    }catch(error){setErroDaConta(error instanceof Error?error.message:'Sem conexão com o servidor.');}
  };
  useEffect(()=>{if(onlineConfigured&&logado&&conta&&nomeDaConta?.id!==conta.id)void buscaNome(conta);},[logado,conta?.id]);
  /* jornadas terminadas que não chegaram ao servidor: reenviadas ao abrir o jogo com a conta (src/lib/envios-pendentes.ts) */
  useEffect(()=>{if(onlineConfigured&&logado&&conta)void reenviarPendentes(e=>onlineCall('submit',{runId:e.runId,digest:e.digest,dicas:e.dicas,vencidas:e.vencidas,desistiu:e.desistiu,lutas:e.lutas}));},[logado,conta?.id]);
  const escolheNome=async(handle:string):Promise<string|null>=>{
    if(!conta)return 'Entre na conta primeiro.';
    try{const r=await onlineCall<{profile:{handle:string}}>('profile',{handle});setProfile(p=>{const n={...p,publicHandle:r.profile.handle};save('profile',n);return n;});setNomeDaConta({id:conta.id,handle:r.profile.handle});return null;}
    catch(error){return error instanceof Error?error.message:'Não foi possível salvar o nome.';}
  };
  /* O botão das Dicas de trio: a conta do dono sempre; os outros depois de META_DAS_DICAS numa jornada (src/lib/dicas-liberadas.ts) */
  const [dono,setDono]=useState(false);
  useEffect(()=>{let vivo=true;void ehDono(conta?.email).then(d=>{if(vivo)setDono(d);});return ()=>{vivo=false;};},[conta?.email]);
  const podeDicas=dicasLiberadas(dono,profile.recordePontos??0);
  /* A Comunidade (src/screens/ComunidadeScreen.tsx): só com conta e nome público; a presença e os avisos valem em qualquer tela. */
  const contaRef=useRef(conta);contaRef.current=conta;
  const [comunidadeDemo,setComunidadeDemo]=useState<{servico:ServicoDaComunidade;eu:string}|null>(null);
  useEffect(()=>{if(COMUNIDADE_DEMO)void import('./lib/comunidade-demo').then(m=>setComunidadeDemo({servico:m.criarComunidadeDemo(),eu:m.EU_DEMO}));},[]);
  const servicoReal=useMemo(()=>onlineConfigured?criarComunidade(carregarCliente,()=>contaRef.current?.id??null):null,[]);
  const comunidadeLigada=COMUNIDADE_DEMO?!!comunidadeDemo:onlineConfigured&&logado&&!!conta&&nomeDaConta?.id===conta.id&&!!nomeDaConta.handle;
  const servicoDaComunidade=COMUNIDADE_DEMO?comunidadeDemo?.servico??null:servicoReal;
  const euNaComunidade=COMUNIDADE_DEMO?comunidadeDemo?.eu??null:conta?.id??null;
  const [abrirConversa,setAbrirConversa]=useState<string|null>(null);
  /* a luta do PvP ocupa a tela inteira, como a da jornada */
  const [pvpLutando,setPvpLutando]=useState(false);
  const comunidade=useComunidade({servico:servicoDaComunidade,ligado:comunidadeLigada,euId:euNaComunidade,naComunidade:screen==='comunidade',noInicio:screen==='home'});
  /* Dicas ligadas enquanto o trio é escolhido: a jornada inteira paga o custo, mesmo desligando depois (src/engine/pontos.ts) */
  useEffect(()=>{if(settings.dicasDoTrio&&podeDicas&&run?.stage==='draft'&&run.draft.team.length<3&&!run.dicas)changeRun({...run,dicas:true});},[settings.dicasDoTrio,podeDicas,run?.stage,run?.draft.team.length,run?.dicas]);

  /* A porta de entrada: sem conta e sem nome público, o jogo não abre (pedido do jogador). */
  const etapaDoPortao:EtapaDoPortao|null=!onlineConfigured?null:!contaPronta?'carregando':!logado?'entrar':nomeDaConta?.id!==conta!.id?(erroDaConta?'erro':'carregando'):!nomeDaConta.handle?'nome':null;
  // quem chega pelo convite vê as boas-vindas por cima da entrada da conta (instalar ou jogar no navegador)
  if(etapaDoPortao)return <><PortaoDaConta etapa={etapaDoPortao} autenticacao={autenticacao} conta={conta} profile={profile} conectado={onlineConfigured} google={googleConfigured} aoMudarPerfil={p=>{save('profile',p);setProfile(p);}} erro={erroDaConta} onTentar={()=>{if(conta)void buscaNome(conta);}} onNome={escolheNome}/>{convite&&<BoasVindasDoConvite podeInstalar={!!installEvent} onInstalar={instalarDoConvite} onClose={fecharConvite}/>}</>;
  const reset=()=>{resetStorage();setSettings(defaults);setProfile({journeys:0,victories:0,best:0,wins:0,recordePontos:0,escalaDosPontos:ESCALA_DOS_PONTOS});setRun(null);runRef.current=null;navigate('home');};
  return <div onPointerDownCapture={()=>void battleAudio.unlock()} onPointerUpCapture={()=>void battleAudio.unlock()} onTouchEndCapture={()=>void battleAudio.unlock()} onClickCapture={()=>void battleAudio.unlock()} onKeyDownCapture={e=>{if(e.key==='Enter'||e.key===' ')void battleAudio.unlock();}} className={`app ${settings.reducedMotion?'reduce-motion':''} ${screen==='game'&&run?.stage==='battle'||screen==='pvp'&&pvpLutando?'in-battle':''}`}>
    <ToqueGlobal/>
    <Cabecalho tela={screen} menu={menu} onMenu={setMenu} onNavigate={d=>{if(d==='comunidade')setAbrirConversa(null);navigate(d);}} recorde={profile.recordePontos??0} apelido={profile.publicHandle} online={onlineConfigured||COMUNIDADE_DEMO} total={characters.length} naoLidas={comunidade.naoLidas}/>
    <main key={`${screen}-${screen==='game'?run?.stage??'idle':'page'}`} className={screen==='game'&&run?.stage==='battle'||screen==='pvp'&&pvpLutando?'main battle-main screen-enter':'main screen-enter'}>
      {screen==='home'&&<Home comunidade={comunidadeLigada?{online:comunidade.online,naoLidas:comunidade.naoLidas}:null} profile={profile} run={run} conta={conta!==null&&conta.origem!=='convidado'} onPlay={requestNew} onContinue={()=>{if(run?.stage==='battle'&&run.battle){direction.current=directionFor(run);setPresentation({battle:direction.current.visible,beat:direction.current.active});}navigate('game');setPaused(run?.stage==='battle');}} onAbandon={()=>setConfirmAbandon(true)} onNavigate={navigate} onInstall={()=>void install()} onShare={()=>setCompartilhar(true)}/>}
      {screen==='characters'&&<CharactersScreen onDetails={setDetails}/>}
      {/* a Arena PvP (src/screens/PvpScreen.tsx): a coleção são os personagens liberados nas Conquistas (a conta do dono tem os 400, para testar) */}
      {screen==='pvp'&&<Suspense fallback={<p className="cm-carregando-tela">Abrindo a Arena…</p>}><PvpScreen colecao={dono?characters.map(c=>c.id):Object.keys(profile.conquistas??{}).filter(id=>!!byId[id])} settings={settings} onSettings={changeSettings} onDetails={setDetails} onJogar={requestNew} onLutando={setPvpLutando}/></Suspense>}
      {screen==='comunidade'&&(comunidadeLigada&&servicoDaComunidade&&euNaComunidade
        ?<Suspense fallback={<p className="cm-carregando-tela">Abrindo a Comunidade…</p>}><ComunidadeScreen servico={servicoDaComunidade} euId={euNaComunidade} euNome={profile.publicHandle??'Você'} naoLidas={comunidade.naoLidas} onLidas={()=>void comunidade.recontar()} abrirCom={abrirConversa} onDetails={setDetails}/></Suspense>
        :<div className="cm-sem-conta"><p>Entre na sua conta e escolha seu nome para conversar com a comunidade.</p><button className="primary" onClick={()=>navigate('conta')}>Ir para a Conta</button></div>)}
      {screen==='conquistas'&&<ConquistasScreen profile={profile} conta={conta!==null&&conta.origem!=='convidado'} onProfile={muda=>setProfile(p=>{const n=muda(p);if(n!==p)save('profile',n);return n;})} onRanking={()=>{setRankingInicial('conquistas');navigate('ranking');}} onDesafio={jogarDesafio}/>}
      {screen==='ranking'&&<RankingScreen dono={dono} inicial={rankingInicial} handle={profile.publicHandle} conta={conta!==null&&conta.origem!=='convidado'} onConta={()=>navigate('conta')} recorde={profile.recordePontos??0}/>}
      {screen==='conta'&&<AccountScreen autenticacao={autenticacao} conta={conta} profile={profile} conectado={onlineConfigured} google={googleConfigured} aoMudarPerfil={p=>{save('profile',p);setProfile(p);}}/>}
      {screen==='help'&&<HelpScreen onPlay={requestNew}/>}
      {screen==='combos'&&<LivroDeCombos descobertos={profile.combosDescobertos??[]} vistos={profile.combosVistos??[]} onVer={id=>setProfile(p=>{const ja=p.combosVistos??[];if(ja.includes(id))return p;const n={...p,combosVistos:[...ja,id]};save('profile',n);return n;})}/>}
      {screen==='settings'&&<SettingsScreen settings={settings} onChange={changeSettings} onReset={reset} onGaleria={()=>navigate('vfx')}/>}
      {screen==='game'&&run?.stage==='draft'&&<DraftScreen draft={run.draft} desafio={run.desafio} primeiroRival={run.preparado||run.ranked&&run.ranked.mode!=='free'?run.encounters[0]:undefined} dicas={settings.dicasDoTrio&&podeDicas} podeDicas={podeDicas} usouDicas={run.dicas===true} onDicas={ligar=>changeSettings({...settings,dicasDoTrio:ligar})} onPick={id=>changeRun({...run,draft:pickDraft(run.draft,id)})} onSkip={()=>changeRun({...run,draft:skipDraft(run.draft)})} onDetails={setDetails} onStart={()=>void startBattle(0)} onAbandon={()=>setConfirmAbandon(true)}/>}
      {screen==='game'&&run?.stage==='battle'&&run.battle&&<BattleScreen battle={presentation&&direction.current?.battle===run.battle?presentation.battle:run.battle} beat={presentation&&direction.current?.battle===run.battle?presentation.beat:null} index={run.index} name={run.encounters[run.index].name} settings={settings} paused={paused||!!details}  onPause={()=>setPaused(!paused)} onAbandon={()=>setConfirmAbandon(true)} onSettings={changeSettings} onExit={()=>{setPaused(true);navigate('home');}} novosNoLivro={novosNoLivro}/>}
      {screen==='game'&&run?.stage==='result'&&<ResultScreen run={run} onNext={()=>void startBattle(run.index+1)} onRestart={requestNew} onAbandon={()=>setConfirmAbandon(true)} onHome={()=>navigate('home')} onRanking={()=>navigate('ranking')} onRetry={()=>{if(run.ranked)changeRun({...run,ranked:{...run.ranked,status:'validating'}});}} auto={settings.auto} onAuto={auto=>changeSettings({...settings,auto})}/>}
      {screen==='debug'&&import.meta.env.DEV&&<Suspense fallback={<p>Carregando laboratório…</p>}><DebugScreen/></Suspense>}
      {screen==='vfx'&&<Suspense fallback={<p>Carregando galeria audiovisual…</p>}><VfxLabScreen/></Suspense>}
      {!storageAvailable&&<p role="alert" className="storage-warning">Não foi possível salvar neste navegador. Sua sessão continua, mas pode não ser recuperada ao fechar.</p>}
    </main>
    {details&&<CharacterModal character={byId[details]} onClose={()=>setDetails(null)}/>}
    {confirmNew&&<InfoDialog title="Começar uma nova jornada?" icone={<RotateCcw/>} cor="#ffb86b" onClose={()=>setConfirmNew(false)}><p>A jornada de agora some. <b>Seu recorde fica salvo.</b></p><div className="result-actions"><button className="danger" onClick={()=>void startNew()}>Descartar e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmNew(false)}>Continuar jornada</button></div></InfoDialog>}
    {nameDialog&&<InfoDialog title="Seu nome no ranking" icone={<UserPen/>} cor="#86e3a8" onClose={()=>{setNameDialog(false);/* sem nome, a jornada começa do mesmo jeito, só fora do ranking */if(pendingStart){setPendingStart(false);abreJornada();}}}><p>De 3 a 16 letras. Aparece junto do seu trio e dos seus pontos.</p><input className="handle-input" aria-label="Nome público" maxLength={16} value={draftHandle} onChange={e=>setDraftHandle(e.target.value)} placeholder="Seu nome no Nexus"/><p>Prévia: <strong>{draftHandle.trim()||'Seu nome'}</strong></p><button className="primary" disabled={onlineBusy} onClick={()=>void saveHandle()}>Confirmar nome</button></InfoDialog>}
    {versaoNova&&<div className="versao-nova" role="status"><span><b>Nova versão do jogo</b><small>Atualize para suas jornadas valerem no ranking.</small></span><button className="primary" onClick={()=>location.reload()}><RotateCcw size={16}/>Atualizar</button></div>}
    {onlineNotice&&<InfoDialog title="Conexão do ranking" icone={<WifiOff/>} cor="#ff9a8a" onClose={()=>{setOnlineNotice('');setAcaoDoAviso(null);}}><p role="alert">{onlineNotice}</p>
      {acaoDoAviso==='atualizar'&&<button className="primary" onClick={()=>location.reload()}><RotateCcw size={16}/>Atualizar o jogo</button>}
      {acaoDoAviso==='nome'&&<button className="primary" onClick={()=>{setOnlineNotice('');setAcaoDoAviso(null);setNameDialog(true);}}><UserPen size={16}/>Escolher nome</button>}
      {acaoDoAviso==='tentar'&&run?.stage==='draft'&&!run.ranked&&<button className="primary" onClick={()=>{setOnlineNotice('');setAcaoDoAviso(null);tentarDeNovo();}}><RotateCcw size={16}/>Tentar de novo</button>}
      <button className={acaoDoAviso?'secondary':'primary'} onClick={()=>{setOnlineNotice('');setAcaoDoAviso(null);}}>{acaoDoAviso?'Jogar assim mesmo':'Entendi'}</button></InfoDialog>}
    {confirmAbandon&&<InfoDialog title="Desistir desta jornada?" icone={<Flag/>} cor="#ff7a6b" onClose={()=>setConfirmAbandon(false)}><p>A jornada de agora termina aqui, como uma derrota: <b>os pontos que você já fez vão para o ranking</b>. Depois você monta um trio novo.</p><div className="result-actions"><button className="danger" onClick={startNew}>Desistir e começar outra <ArrowUpRight size={18}/></button><button className="secondary" onClick={()=>setConfirmAbandon(false)}>Continuar jornada</button></div></InfoDialog>}
    {comunidade.aviso&&<button className="cm-aviso" onClick={()=>{setAbrirConversa(comunidade.aviso!.de);comunidade.fecharAviso();navigate('comunidade');}} aria-label={`Mensagem nova de ${comunidade.aviso.nome}`}>
      <Avatar id={comunidade.aviso.de} nome={comunidade.aviso.nome} tamanho={40}/><span><b>{comunidade.aviso.nome}</b><small>{comunidade.aviso.texto}</small></span><em>RESPONDER</em></button>}
    {compartilhar&&<CompartilharJogo trio={profile.champion?.length?profile.champion:['goku','naruto','luffy']} onClose={()=>setCompartilhar(false)}/>}
    {convite&&<BoasVindasDoConvite podeInstalar={!!installEvent} onInstalar={instalarDoConvite} onClose={fecharConvite}/>}
    {installHelp&&<InfoDialog title={installed?'O NEXUS já está instalado':'Leve seu trio no bolso'} icone={<Download/>} cor="#8fd3ff" onClose={()=>setInstallHelp(false)}><p>{installed?'Abra o jogo pelo ícone na tela inicial do aparelho.':<><b>Android:</b> menu do navegador → “Instalar aplicativo”.<br/><b>iPhone:</b> Compartilhar → “Adicionar à Tela de Início”.</>}</p><p>O progresso fica neste aparelho e o jogo abre mesmo sem internet.</p><button className="primary" onClick={()=>setInstallHelp(false)}>Entendi</button></InfoDialog>}
  </div>;
}
