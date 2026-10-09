import { byId } from '../data/characters';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';

export type Family='physical'|'energy'|'electric'|'fire'|'magic'|'dark'|'psychic'|'slash'|'prison'|'shield'|'heal'|'regen'|'buff'|'debuff'|'interrupt'|'ko'|'turn'|'grand';
export interface Beat {event:BattleEvent;events:BattleEvent[];before:Battle;after:Battle;duration:number;family:Family;grand:boolean;elapsed:number;impacted:boolean;periodic?:boolean;trace?:BeatTrace;
  /** Passo da cadeia já mostrado (1, 2, 3…; 0 = antes do impacto). Ver `etapaDoEvento`. */
  etapa?:number;
  /** Os números dos passos deste beat (1…n). */
  etapas?:number[];
  /** A cadeia de efeitos deste beat, na ordem em que aparece. */
  passos?:Passo[];
  /** Um traço disparou sozinho, fora da ação de alguém (fica com um passo de reação). */
  traco?:boolean;
  /** Duração sem as etapas (o ritmo fixo da ação). */
  base?:number}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[]}
export interface PresentationCheckpoint {version?:2;battleTime:number;nextEvent:number;rng:number;visibleNextEvent:number;activeEventId:number|null;activeElapsed:number;impacted:boolean;serial:number;simIdle?:number}
export interface Cue {event:BattleEvent;family:Family;phase:'start'|'impact';grand:boolean}
export interface BeatTrace {eventId:number;kind:BattleEvent['kind'];duration:number;realStart:number;realImpact:number|null;realFinish:number|null;speed:number;queueLength:number;battleTime:number;source:string;haste:number;slow:number;rooted:number;shifts:{target:string;value:number}[]}
export function familyOf(event:BattleEvent,battle:Battle):Family {
  if(event.kind==='ko'||event.kind==='turn'||event.kind==='interrupt')return event.kind;
  if(event.kind==='heal'||event.kind==='revive')return 'heal';
  if(event.kind==='shield'||event.kind==='block')return 'shield';
  if(event.status){if(event.status==='regen')return 'regen';if(event.status==='burning')return 'fire';if(['haste','strengthened','protected'].includes(event.status))return 'buff';if(['rooted','paralyzed'].includes(event.status))return 'prison';return 'debuff';}
  const f=battle.fighters.find(f=>f.uid===event.source),c=f?byId[f.characterId]:null;
  const effects=event.skill!==undefined?c?.skills[event.skill].effects:[];
  if(effects?.some(e=>e.kind==='status'&&e.status==='burning'))return 'fire';
  if(effects?.length&&!effects.some(e=>e.kind==='damage'||e.kind==='deathnote')){
    if(effects.some(e=>e.kind==='heal'))return 'heal';
    if(effects.some(e=>e.kind==='shield'))return 'shield';
    const status=effects.find(e=>e.kind==='status');
    if(status?.kind==='status'){if(status.status==='regen')return 'regen';if(status.status==='burning')return 'fire';if(['strengthened','haste','protected'].includes(status.status))return 'buff';if(['rooted','paralyzed'].includes(status.status))return 'prison';return 'debuff';}
  }
  if(c?.id==='raven'&&event.visual==='psychic')return 'dark';
  return ({impact:'physical',beam:'energy',bolt:'electric',wave:'magic',psychic:'psychic',slash:'slash',web:'prison',shield:'shield'} as const)[event.visual??'impact'];
}
function focus(events:BattleEvent[]):BattleEvent|undefined {
  return events.find(e=>e.kind==='basic'||e.kind==='skill'||e.kind==='cast')
    ??events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='revive'||e.kind==='turn');
}
function duration(event:BattleEvent,grand:boolean){
  if(event.kind==='cast')return P.preparationSeconds;
  if(event.kind==='ko'||event.kind==='revive')return P.knockoutSeconds;
  if(event.kind==='turn')return P.turnaroundSeconds;
  if(event.kind==='interrupt')return P.interruptSeconds;
  if(event.kind==='tempo')return P.tempoSeconds;
  return grand?P.grandSeconds:event.kind==='skill'?P.skillSeconds:P.normalSeconds;
}
/*
 * A cadeia de efeitos, um passo por vez.
 *
 * Pedido do jogador: quando um golpe acontece, cada coisa tem que aparecer na
 * hora certa — o dano; se o alvo tem uma reação ao sofrer dano, ela dispara e
 * mostra o efeito dela; depois o debuff no rival; depois o buff no próprio
 * trio; e se isso faz um aliado reagir, a reação dele vem em seguida. Nada ao
 * mesmo tempo.
 *
 * O motor já registra os eventos na ordem em que as coisas acontecem (a reação
 * de quem sofre dano é emitida logo depois do dano). Aqui essa lista vira
 * passos:
 *   golpe   · dano, bloqueio, interrupção e nocaute de quem age (em todos os
 *             alvos de uma vez — um golpe em área cai junto);
 *   reacao  · tudo o que outro lutador causa no meio da ação é o traço dele
 *             disparando (um passo por reação, com o nome do traço);
 *   rival   · Status negativo e atraso que quem age põe no rival;
 *   aliado  · cura, Escudo, Status positivo e Carga de quem age no próprio trio.
 * O golpe vem sempre primeiro; o resto segue a ordem real do motor. Carga,
 * sinergia e "pronto" vão no passo que os causou. O motor não muda nada (nem
 * um evento a mais: a mira da IA usa o contador de eventos como semente) — é
 * só a ordem e o tempo em que a tela revela o que já aconteceu.
 */
export type ClasseDoPasso='golpe'|'reacao'|'rival'|'aliado';
export interface Passo {classe:ClasseDoPasso;/** quem age neste passo */quem:string;/** nome do traço, numa reação */rotulo?:string;eventos:number[];/** segundos depois do impacto */em:number}
/** Quanto cada passo fica na tela antes do próximo (o tempo de ler o que aconteceu). */
export const TEMPO_DO_PASSO:Record<ClasseDoPasso,number>={golpe:.42,reacao:.58,rival:.4,aliado:.4};
/** O máximo que a cadeia inteira pode alongar um golpe (lutas com muitas reações não arrastam). */
const CADEIA_MAXIMA=2.6;
/** Quanto dura um traço que dispara sozinho (o nome aparece, o efeito entra, a luta segue). */
const TEMPO_DO_TRACO=1.3;
/** Mantido para quem ainda mede pelo intervalo antigo. */
export const INTERVALO_DA_ETAPA=TEMPO_DO_PASSO.rival;
const CONTABIL=new Set<BattleEvent['kind']>(['charge','synergy','ready','discovery','basic','skill','cast','turn']);
const DO_GOLPE=new Set<BattleEvent['kind']>(['damage','block','interrupt','ko']);
/* Reações que vêm de uma mecânica, não do traço: o passo leva o nome dela. */
export const ROTULO_DA_MECANICA:Record<string,string>={Refletido:'Refletir',Espinhos:'Espinhos',Vampirismo:'Vampirismo'};
const ehDaMecanica=(e:BattleEvent)=>(e.kind==='damage'||e.kind==='heal')&&e.label in ROTULO_DA_MECANICA;
function montaPassos(beat:Pick<Beat,'event'|'events'|'after'|'traco'>):Passo[]{
  const ator=beat.event.source,lado=beat.after.fighters.find(f=>f.uid===ator)?.side;
  const ladoDe=(uid?:string)=>beat.after.fighters.find(f=>f.uid===uid)?.side;
  if(beat.traco){const f=beat.after.fighters.find(x=>x.uid===ator);return [{classe:'reacao',quem:ator,rotulo:f?byId[f.characterId].trait.name:undefined,eventos:beat.events.map(e=>e.id),em:0}];}
  if(!['basic','skill'].includes(beat.event.kind)||!lado)return [{classe:'golpe',quem:ator,eventos:beat.events.map(e=>e.id),em:0}];
  const tracoDe=(uid:string)=>{const f=beat.after.fighters.find(x=>x.uid===uid);return f?byId[f.characterId].trait.name:undefined;};
  // o que a própria ação (habilidade ou básico) faz: o resto que sai de quem age é o traço dele
  const lutador=beat.after.fighters.find(f=>f.uid===ator),ficha=lutador?byId[lutador.characterId]:undefined;
  const efeitos=beat.event.kind==='skill'&&beat.event.skill!==undefined?ficha?.skills[beat.event.skill]?.effects??[]:ficha?.basic.effects??[];
  const explicado=(e:BattleEvent)=>e.kind==='status'?efeitos.some(x=>x.kind==='status'&&x.status===e.status)||efeitos.some(x=>x.kind==='deathnote')
    :e.kind==='heal'?efeitos.some(x=>x.kind==='heal'||x.kind==='release')||(e.label==='Roubo de vida'&&efeitos.some(x=>x.kind==='lifesteal'))
    :e.kind==='shield'?efeitos.some(x=>x.kind==='shield')||e.label!=='Escudo'
    :e.kind==='tempo'?efeitos.some(x=>x.kind==='shift'):true;
  const passos:Passo[]=[],doAtor=new Map<ClasseDoPasso,Passo>(),soltos:number[]=[];
  let atual:Passo|null=null;
  for(const e of beat.events){
    // contabilidade (Carga, "pronto", sinergia) e ajustes nulos vão no passo que os causou
    if(CONTABIL.has(e.kind)||(e.kind==='tempo'&&Math.abs(e.value??0)<.005)){if(atual)atual.eventos.push(e.id);else soltos.push(e.id);continue;}
    const dono=e.kind==='block'?(e.attacker??ator):e.source;
    // Refletir, Espinhos e Vampirismo: um passo de reação com o nome da mecânica
    if(ehDaMecanica(e)){
      const rotulo=ROTULO_DA_MECANICA[e.label]!;
      if(!(atual?.classe==='reacao'&&atual.quem===dono&&atual.rotulo===rotulo)){atual={classe:'reacao',quem:dono,rotulo,eventos:[],em:0};passos.push(atual);}
      atual.eventos.push(e.id);continue;
    }
    if(dono===ator&&!DO_GOLPE.has(e.kind)&&!explicado(e)){
      // o próprio traço de quem age disparou (ao agir, ao causar dano…): vira um passo com o nome dele
      if(!(atual?.classe==='reacao'&&atual.quem===ator)){atual={classe:'reacao',quem:ator,rotulo:tracoDe(ator),eventos:[],em:0};passos.push(atual);}
      atual.eventos.push(e.id);continue;
    }
    if(dono===ator){
      const classe:ClasseDoPasso=DO_GOLPE.has(e.kind)?'golpe':ladoDe(e.target??e.source)!==lado?'rival':'aliado';
      let passo=doAtor.get(classe);
      if(!passo){passo={classe,quem:ator,eventos:[],em:0};doAtor.set(classe,passo);passos.push(passo);}
      passo.eventos.push(e.id);atual=passo;
    }else{
      if(!(atual?.classe==='reacao'&&atual.quem===dono)){atual={classe:'reacao',quem:dono,rotulo:tracoDe(dono),eventos:[],em:0};passos.push(atual);}
      atual.eventos.push(e.id);
    }
  }
  /*
   * A ordem de quem age é sempre golpe → rival → aliado (o pedido: dano,
   * depois o debuff, depois o buff). Cada reação anda junto do passo que a
   * causou, logo depois dele; reações de antes do primeiro passo de quem age
   * (um traço que dispara ao agir) vêm logo depois do golpe.
   */
  const ORDEM:Record<ClasseDoPasso,number>={golpe:0,rival:1,aliado:2,reacao:9};
  const blocos:Passo[][]=[];let antes:Passo[]=[];
  for(const x of passos){
    if(x.classe==='reacao'){if(blocos.length)blocos.at(-1)!.push(x);else antes.push(x);}
    else blocos.push([x]);
  }
  blocos.sort((a,b)=>ORDEM[a[0]!.classe]-ORDEM[b[0]!.classe]);
  if(blocos.length){blocos[0]!.splice(1,0,...antes);antes=[];}
  passos.length=0;passos.push(...blocos.flat(),...antes);
  if(!passos.length)passos.push({classe:'golpe',quem:ator,eventos:[],em:0});
  passos[0]!.eventos.unshift(...soltos);
  // o tempo de cada passo depois do impacto, comprimido se a cadeia ficar longa
  const intervalos=passos.slice(0,-1).map(x=>TEMPO_DO_PASSO[x.classe]);
  const total=intervalos.reduce((a,b)=>a+b,0),escala=total>CADEIA_MAXIMA?CADEIA_MAXIMA/total:1;
  let t=0;passos.forEach((x,k)=>{x.em=t;t+=(intervalos[k]??0)*escala;});
  return passos;
}
/** Em que passo (1, 2, 3…) o evento aparece. Eventos fora da lista do beat aparecem no primeiro. */
export function etapaDoEvento(beat:Pick<Beat,'event'|'after'>&{passos?:Passo[]},e:BattleEvent):number{
  const k=beat.passos?.findIndex(x=>x.eventos.includes(e.id))??-1;
  return k<0?1:k+1;
}
/** O passo que está na tela agora. */
export const passoAtual=(beat:Beat|null|undefined):Passo|undefined=>beat?.impacted&&beat.etapa?beat.passos?.[beat.etapa-1]:undefined;
/** O evento já pode aparecer na tela? */
export function revelado(beat:Beat|null|undefined,e:BattleEvent):boolean{
  if(!beat?.impacted)return false;
  return etapaDoEvento(beat,e)<=(beat.etapa??99);
}
/*
 * O que a tela mostra num passo: o estado de antes com só o que já foi
 * revelado aplicado por cima — a Vida desce no dano, sobe na cura da reação,
 * o Escudo entra e é gasto, cada Status aparece no seu passo. No último passo
 * é exatamente o estado de depois.
 */
export function visivelNaEtapa(beat:Beat,etapa:number):Battle{
  const ultima=beat.etapas?.at(-1)??1;
  if(etapa>=ultima)return beat.after;
  const v=structuredClone(beat.after);
  const vistos=beat.events.filter(e=>etapaDoEvento(beat,e)<=etapa);
  v.fighters.forEach((f,i)=>{
    const antes=beat.before.fighters[i];if(!antes)return;
    const meus=vistos.filter(e=>e.target===f.uid);
    // na ordem: cair zera, levantar volta com a Vida prometida, e o resto soma por cima
    let hp=antes.hp;
    for(const e of meus){
      if(e.kind==='ko')hp=0;
      else if(e.kind==='revive')hp=e.value??1;
      else if(e.kind==='heal'&&hp>0)hp+=e.value??0;
      else if(e.kind==='damage')hp-=e.value??0;
    }
    f.hp=Math.max(0,Math.min(f.maxHp,hp));
    const escudos=structuredClone(antes.shields);
    for(const e of meus){
      if(e.kind==='shield'&&e.label==='Escudo')escudos.push({amount:e.value??0,remaining:10,source:e.source});
      if(e.kind==='block'&&e.label==='Bloqueio'){let resta=e.value??0;for(const s of escudos){if(s.source!==e.source)continue;const usado=Math.min(s.amount,resta);s.amount-=usado;resta-=usado;}}
    }
    f.shields=escudos.filter(s=>s.amount>.01);
    const statuses=structuredClone(antes.statuses);
    for(const e of meus)if(e.kind==='status'&&e.status){
      const novo=f.statuses.find(s=>s.id===e.status);const k=statuses.findIndex(s=>s.id===e.status);
      if(novo){if(k>=0)statuses[k]=structuredClone(novo);else statuses.push(structuredClone(novo));}
    }
    f.statuses=statuses;
    const cargaVista=vistos.some(e=>(e.kind==='charge'&&e.target===f.uid)||(e.kind==='ready'&&e.source===f.uid));
    if(!cargaVista)f.skills=f.skills.map((s,k)=>({...s,charge:antes.skills[k]?.charge??s.charge}));
    if(!meus.some(e=>e.kind==='interrupt'||e.kind==='ko'))f.cast=structuredClone(antes.cast);
  });
  return v;
}
/** A duração do golpe sem o tempo da cadeia: o ritmo de cada ação continua fixo. */
export const duracaoBase=(beat:Beat)=>beat.base??beat.duration;
/** Em que passo o impacto está, pelo tempo já passado do beat. */
function etapaNoTempo(beat:Beat):number{
  const passos=beat.passos??[],impacto=duracaoBase(beat)*P.impactAt;
  let i=0;while(i<passos.length-1&&beat.elapsed>=impacto+passos[i+1]!.em-1e-8)i++;
  return i+1;
}

export function createDirection(battle:Battle):Direction {
  return {battle,visible:structuredClone(battle),queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[]};
}
function makeBeat(event:BattleEvent,events:BattleEvent[],before:Battle,after:Battle,periodic=false,previous=false,traco=false):Beat {
  const actor=after.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  const auxiliary=event.kind==='ready'||event.kind==='status';
  const seconds=traco?TEMPO_DO_TRACO:previous?(periodic?.55:auxiliary?.5:duration(event,grand)):periodic?P.periodicSeconds:duration(event,grand);
  const beat:Beat={event,events,before,after,duration:seconds,family:familyOf(event,after),grand,elapsed:0,impacted:false,periodic,etapa:0,base:seconds,traco};
  beat.passos=montaPassos(beat);
  beat.etapas=beat.passos.map((_,k)=>k+1);
  const ultimo=beat.passos.at(-1)!;
  beat.duration+=ultimo.em;
  return beat;
}
function collect(d:Direction,events:BattleEvent[],before:Battle,after:Battle,legacy=false,previous=false){
  if(!events.length)return;
  // Every observer callback is a chronological boundary: one action and its
  // consequences, or periodic effects. Never merge across an action boundary.
  const principal=focus(events);
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    d.queue.push(makeBeat(principal,events,before,after));
    return;
  }
  if(principal&&!previous){d.queue.push(makeBeat(principal,events,before,after));return;}
  // fora de uma ação, Status e Escudo só nascem de um traço disparando sozinho: ganha um momento próprio
  const traco=!previous&&!legacy?events.find(e=>e.kind==='status'||(e.kind==='shield'&&e.label==='Escudo')):undefined;
  if(traco){d.queue.push(makeBeat(traco,events,before,after,false,false,true));return;}
  const change=events.find(e=>e.kind==='damage'||e.kind==='heal');
  if(change){
    const burning=change.kind==='damage'&&before.fighters.find(f=>f.uid===change.target)?.statuses.some(s=>s.id==='burning');
    const event={...change,label:burning?'Queimadura':change.kind==='heal'?'Regeneração':'Efeito contínuo',status:burning?'burning' as const:change.kind==='heal'?'regen' as const:undefined};
    const last=d.queue[d.queue.length-1];
    // One fixed window covers every affected fighter, without crossing an action.
    if(last?.periodic&&(previous?(last.event.source===event.source&&last.event.target===event.target&&last.event.kind===event.kind):true)&&
       !events.some(e=>e.kind==='ko'||e.kind==='revive'||e.kind==='interrupt'||e.kind==='turn')&&after.time-last.before.time<=(legacy?1.01:previous?.51:P.periodicWindowSeconds+.01)){
      last.events.push(...events);last.after=after;
      if(previous)last.event.value=(last.event.value??0)+(event.value??0);
    }else d.queue.push(makeBeat(event,events,before,after,true,previous));
    return;
  }
  if(previous){
    const important=events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='revive'||e.kind==='turn'||e.kind==='ready'||e.kind==='status'||e.kind==='shield');
    if(important)d.queue.push(makeBeat(important,events,before,after,legacy&&(important.kind==='ready'||important.kind==='status'),true));
    return;
  }
  // Charge, ready, and status feedback rides on the visible idle simulation.
  // A standalone tempo adjustment gets its own clear target indication.
  const tempo=events.find(e=>e.kind==='tempo');
  if(tempo)d.queue.push(makeBeat(tempo,events,before,after));
  else if(d.queue.at(-1)?.periodic){d.queue.at(-1)!.events.push(...events);d.queue.at(-1)!.after=after;}
  else d.signals.push(...events);
}
function simulateStep(d:Direction,legacy=false,previousMode=false){
  let previous=structuredClone(d.battle),lastId=d.battle.nextEvent-1;
  stepBattle(d.battle,current=>{
    const events=current.events.filter(e=>e.id>lastId);
    lastId=current.nextEvent-1;
    const after=structuredClone(current);
    collect(d,events,previous,after,legacy,previousMode);
    previous=after;
  });
  const last=d.queue[d.queue.length-1];
  if(!legacy&&last?.periodic&&d.battle.time-last.before.time<=(previousMode?.51:P.periodicWindowSeconds+.01))last.after=structuredClone(d.battle);
}
export function checkpointDirection(d:Direction):PresentationCheckpoint {
  return {version:2,battleTime:d.battle.time,nextEvent:d.battle.nextEvent,rng:d.battle.rng,visibleNextEvent:d.visible.nextEvent,activeEventId:d.active?.event.id??null,activeElapsed:d.active?.elapsed??0,impacted:d.active?.impacted??false,serial:d.serial,simIdle:d.simIdle};
}
/** Rebuilds the unseen visual timeline from deterministic combat after a reload. */
export function restoreDirection(initial:Battle,saved:Battle,checkpoint:PresentationCheckpoint):Direction|null {
  if(!checkpoint||checkpoint.battleTime!==saved.time||checkpoint.nextEvent!==saved.nextEvent||checkpoint.rng!==saved.rng)return null;
  const d=createDirection(initial);
  const legacy=checkpoint.simIdle===undefined;
  const previous=checkpoint.version!==2&&!legacy;
  while(!d.battle.finished&&d.battle.time+STEP/2<saved.time)simulateStep(d,legacy,previous);
  if(d.battle.time!==saved.time||d.battle.nextEvent!==saved.nextEvent||d.battle.rng!==saved.rng)return null;
  const index=checkpoint.activeEventId===null?-1:d.queue.findIndex(beat=>beat.event.id===checkpoint.activeEventId);
  if(checkpoint.activeEventId!==null&&index<0)return null;
  if(index>=0){
    d.active=d.queue[index];d.queue=d.queue.slice(index+1);
    d.active.elapsed=Math.min(d.active.duration,Math.max(0,checkpoint.activeElapsed));
    d.active.impacted=checkpoint.impacted;
    if(d.active.impacted)d.active.etapa=etapaNoTempo(d.active);
    d.visible=d.active.impacted?visivelNaEtapa(d.active,d.active.etapa!):d.active.before;
  }else{
    const pending=d.queue.findIndex(beat=>beat.after.nextEvent>checkpoint.visibleNextEvent);
    const completed=pending<0?d.queue.length:pending;
    d.visible=pending<0?structuredClone(saved):completed?d.queue[completed-1].after:structuredClone(initial);
    d.queue=d.queue.slice(completed);
  }
  if(d.visible.nextEvent!==checkpoint.visibleNextEvent)return null;
  d.battle=saved;d.serial=checkpoint.serial;d.simIdle=checkpoint.simIdle??0;d.complete=saved.finished&&!d.active&&!d.queue.length;
  return d;
}
/** Consume combat only between beats. One render advances at most one visual boundary. */
export function advanceDirection(d:Direction,seconds:number,onCue?:(cue:Cue)=>void,visualSpeed=1,onTrace?:(trace:BeatTrace)=>void):void {
  // A delayed frame may not accumulate time to rush through unseen actions.
  const speed=visualSpeed===2?2:1;
  const elapsed=Math.min(P.renderIntervalMs/1000,Math.max(0,seconds))*speed;d.signals=[];
  if(d.complete||elapsed===0)return;
  if(d.active){
    const beat=d.active;
    const impacto=duracaoBase(beat)*P.impactAt;
    const limit=beat.impacted?beat.duration:impacto;
    beat.elapsed=Math.min(limit,beat.elapsed+elapsed);
    const etapas=beat.etapas??[1];
    if(!beat.impacted&&beat.elapsed>=limit-1e-8){
      beat.impacted=true;beat.etapa=etapas[0];
      if(beat.trace)beat.trace.realImpact=performance.now();
      d.visible=visivelNaEtapa(beat,beat.etapa!);
      d.signals.push(...beat.events.filter(e=>etapaDoEvento(beat,e)<=beat.etapa!));
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand});
    }else if(beat.impacted&&(beat.etapa??1)<etapas.at(-1)!&&beat.elapsed>=impacto+(beat.passos?.[beat.etapa!]?.em??0)-1e-8){
      /* o próximo passo da cadeia: um efeito por vez, cada um na sua hora */
      const anterior=beat.etapa!;beat.etapa=anterior+1;
      d.visible=visivelNaEtapa(beat,beat.etapa!);
      d.signals.push(...beat.events.filter(e=>{const x=etapaDoEvento(beat,e);return x>anterior&&x<=beat.etapa!;}));
    }else if(beat.impacted&&beat.elapsed>=beat.duration-1e-8){
      if(beat.trace){beat.trace.realFinish=performance.now();onTrace?.(beat.trace);}
      d.active=null;
      return;
    }
  }else if(!d.battle.finished&&(d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
    d.simIdle+=elapsed*P.gameRate;
    while(d.simIdle>=STEP-1e-8&&!d.battle.finished&&
      (d.queue.length===0||d.queue.length===1&&d.queue[0].periodic&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
      d.simIdle=Math.max(0,d.simIdle-STEP);
      simulateStep(d);
      if(!d.queue.length)d.visible=structuredClone(d.battle);
    }
  }
  // Start, impact, and finish each get their own paint. The motor stays parked
  // while an active beat or its consequences are waiting to be displayed.
  if(!d.active&&d.queue.length&&!(d.queue.length===1&&d.queue[0].periodic&&!d.battle.finished&&d.battle.time-d.queue[0].before.time<P.periodicWindowSeconds-.01)){
    d.active=d.queue.shift()!;d.serial++;
    if(onTrace){
      const fighter=d.active.before.fighters.find(f=>f.uid===d.active!.event.source);
      const intensity=(id:string)=>fighter?.statuses.find(s=>s.id===id)?.intensity??0;
      d.active.trace={eventId:d.active.event.id,kind:d.active.event.kind,duration:duracaoBase(d.active),realStart:performance.now(),realImpact:null,realFinish:null,speed,queueLength:d.queue.length,battleTime:d.active.before.time,source:d.active.event.source,haste:intensity('haste'),slow:intensity('slow'),rooted:intensity('rooted'),shifts:d.active.events.filter(e=>e.kind==='tempo').map(e=>({target:e.target??'',value:e.value??0}))};
    }
    d.visible=d.active.before;
    onCue?.({event:d.active.event,family:d.active.family,phase:'start',grand:d.active.grand});
    return;
  }
  if(d.battle.finished&&!d.active&&!d.queue.length){d.visible=structuredClone(d.battle);d.complete=true;}
}
