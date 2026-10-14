import { byId } from '../data/characters';
import { UNICAS } from '../engine/unicas';
import { STEP, stepBattle } from '../engine/battle';
import type { Battle, BattleEvent } from '../engine/types';
import { PRESENTATION as P } from './config';
import { QUADRO_DO_GOLPE } from './golpe-das-folhas';
import { familia, profileFor } from './vfxProfiles';
import { INTERVALO_DA_UNICA, JEITO_DA_UNICA } from './unicas-efeitos';
import { fasesDoEvento, golpeParado, pausasDoGolpe, soONome, type PausaDaUnica } from './ativacao-da-unica';
import { ehDaRajada, rajadaDaChave } from './rajada-da-unica';
export { ladoDaUnica, vooDaUnica } from './ativacao-da-unica';

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
  base?:number;
  /** Quanto antes do impacto a folha do golpe (e o som dela) começa, para o golpe desenhado cair junto do número. */
  antecipa?:number;
  /** A folha do golpe já começou (a deixa 'golpe' já saiu). */
  golpeou?:boolean;
  /** O golpe para e alguém ativa a Mecânica única antes de ele cair (src/presentation/ativacao-da-unica.ts). */
  pausas?:PausaDaUnica[]}
export interface Direction {battle:Battle;visible:Battle;queue:Beat[];active:Beat|null;simIdle:number;complete:boolean;serial:number;signals:BattleEvent[];/** quando cada lutador teve a última ativação completa da Mecânica única */unicaCheia?:Record<string,number>}
export interface PresentationCheckpoint {version?:2;battleTime:number;nextEvent:number;rng:number;visibleNextEvent:number;activeEventId:number|null;activeElapsed:number;impacted:boolean;serial:number;simIdle?:number}
/** 'golpe': a folha do golpe (e o som dela) começa antes do impacto; o impacto que vem depois traz `antecipado`. */
export interface Cue {event:BattleEvent;family:Family;phase:'start'|'golpe'|'impact';grand:boolean;antecipado?:boolean}
export interface BeatTrace {eventId:number;kind:BattleEvent['kind'];duration:number;realStart:number;realImpact:number|null;realFinish:number|null;speed:number;queueLength:number;battleTime:number;source:string;haste:number;slow:number;rooted:number;shifts:{target:string;value:number}[]}
export function familyOf(event:BattleEvent,battle:Battle):Family {
  if(event.kind==='ko'||event.kind==='turn'||event.kind==='interrupt')return event.kind;
  if(event.kind==='heal'||event.kind==='revive')return 'heal';
  if(event.kind==='cleanse')return 'buff';
  if(event.kind==='dispel')return 'debuff';
  if(event.kind==='shield'||event.kind==='block')return 'shield';
  if(event.kind==='miss'||event.kind==='summon')return 'physical';
  if(event.kind==='resist')return 'shield';
  if(event.kind==='unica'||event.kind==='pulso')return 'buff';
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
    ??events.find(e=>e.kind==='interrupt'||e.kind==='ko'||e.kind==='revive'||e.kind==='summon'||e.kind==='turn');
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
export type ClasseDoPasso='golpe'|'reacao'|'rival'|'aliado'|'unica';
export interface Passo {classe:ClasseDoPasso;/** quem age neste passo */quem:string;/** nome do traço, numa reação */rotulo?:string;eventos:number[];/** segundos depois do impacto */em:number;/** a Mecânica única já ativou na pausa do golpe: aqui só cai o resultado, sem o nome de novo */antecipada?:boolean;/** o efeito da Mecânica única do passo anterior (o dano, a cura, o Status que ela causou), sem selo de traço */resultado?:boolean;/** um golpe de uma rajada (src/presentation/rajada-da-unica.ts): o i-ésimo de n, e de qual rajada (rajadaDaChave) */rajada?:{i:number;n:number;chave:string}}
/** Quanto cada passo fica na tela antes do próximo (o tempo de ler o que aconteceu). */
export const TEMPO_DO_PASSO:Record<ClasseDoPasso,number>={golpe:.42,reacao:.58,rival:.4,aliado:.4,unica:1.85};
/**
 * A mini preparação da Mecânica única no meio da cadeia de um golpe. Sozinha ou na pausa do golpe, ela tem as fases
 * de uma habilidade e o Preparo de cada personagem (src/presentation/ativacao-da-unica.ts).
 */
export const PREPARO_DA_UNICA=.5;
/** Fração do golpe em que quem foi até o alvo já está de volta no lugar (acting-motion.css). */
export const VOLTA_DO_GOLPE=.9;
/** O máximo que a cadeia inteira pode alongar um golpe (lutas com muitas reações não arrastam). */
const CADEIA_MAXIMA=2.6;
/** Quanto dura um traço que dispara sozinho (o nome aparece, o efeito entra, a luta segue). */
const TEMPO_DO_TRACO=1.3;
/** A Mecânica única ativando sozinha: depois do impacto, o efeito dela fica à vista este tanto. */
const DEPOIS_DA_UNICA=2.2;
/** Mantido para quem ainda mede pelo intervalo antigo. */
export const INTERVALO_DA_ETAPA=TEMPO_DO_PASSO.rival;
const CONTABIL=new Set<BattleEvent['kind']>(['charge','synergy','ready','discovery','basic','skill','cast','turn']);
const DO_GOLPE=new Set<BattleEvent['kind']>(['damage','block','interrupt','ko']);
/* Reações que vêm de uma mecânica, não do traço: o passo leva o nome dela. */
export const ROTULO_DA_MECANICA:Record<string,string>={Refletido:'Refletir',Espinhos:'Espinhos',Vampirismo:'Vampirismo',Sangramento:'Sangramento',Barreira:'Barreira','Última resistência':'Última resistência',Ricochete:'Ricochete','Golpe largo':'Golpe largo','Golpe que cura':'Golpe que cura','Guarda do golpe':'Guarda do golpe','Roubou Carga':'Roubou Carga',Acelerou:'Acelerou'};
const ehDaMecanica=(e:BattleEvent)=>['damage','heal','resist','shield','charge','tempo'].includes(e.kind)&&e.label in ROTULO_DA_MECANICA;
export function montaPassos(beat:Pick<Beat,'event'|'events'|'after'|'traco'|'base'>,cheias?:ReadonlySet<string>):Passo[]{
  const ator=beat.event.source,lado=beat.after.fighters.find(f=>f.uid===ator)?.side;
  const ladoDe=(uid?:string)=>beat.after.fighters.find(f=>f.uid===uid)?.side;
  if(beat.traco){
    const f=beat.after.fighters.find(x=>x.uid===ator);
    const so:Passo[]=[{classe:beat.event.kind==='unica'&&cheias?.has(ator)?'unica':'reacao',quem:ator,rotulo:f?(beat.event.kind==='unica'?UNICAS[f.characterId]?.nome:beat.event.kind==='pulso'?'':byId[f.characterId].trait.name):undefined,eventos:beat.events.map(e=>e.id),em:0}];
    // sozinha, o impacto do beat é a chegada do efeito: os golpes da rajada saem dali, um a cada intervalo
    separaRajadas(so,beat);
    for(const x of so)if(x.rajada)x.em=x.rajada.i*(rajadaDaChave(x.rajada.chave)?.intervalo??.3);
    return so;
  }
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
  // a ativação completa aberta agora e o passo com o resultado dela
  let unicaAberta:Passo|null=null,resultado:Passo|null=null;
  for(const e of beat.events){
    // contabilidade (Carga, "pronto", sinergia) e ajustes nulos vão no passo que os causou
    const dono=e.kind==='block'?(e.attacker??ator):e.source;
    // Mecânica única: um passo com o nome dela. Combo de tempo em tempo: um passo sem nome — só o efeito
    // aparece, como numa habilidade (pedido do jogador: o nome do combo em cima do personagem atrapalhava;
    // quem quiser ler toca na etiqueta de combos)
    if(e.kind==='unica'||e.kind==='pulso'){
      const f=beat.after.fighters.find(x=>x.uid===e.source),rotulo=e.kind==='pulso'?'':f?UNICAS[f.characterId]?.nome:undefined;
      // a ativação completa (src/presentation/unicas-efeitos.ts): um passo longo, como uma habilidade
      const classe:ClasseDoPasso=e.kind==='unica'&&cheias?.has(e.source)?'unica':'reacao';
      const ultimo=atual as Passo|null;
      if(ultimo&&ultimo.classe===classe&&ultimo.quem===e.source&&ultimo.rotulo===rotulo)ultimo.eventos.push(e.id);
      else{atual={classe,quem:e.source,rotulo,eventos:[e.id],em:0};passos.push(atual);}
      unicaAberta=classe==='unica'?atual:null;resultado=null;
      continue;
    }
    // o que a Mecânica única causa logo depois do aviso (o dano, a cura, o Status) é o resultado dela: aparece quando
    // o efeito dela chega, sem o selo do traço (antes, o nome do traço aparecia em cima do efeito da mecânica)
    if(unicaAberta&&(atual===unicaAberta||atual===resultado)&&dono===unicaAberta.quem&&!CONTABIL.has(e.kind)&&!ehDaMecanica(e)&&!(dono===ator&&DO_GOLPE.has(e.kind))){
      if(!resultado){resultado={classe:'reacao',quem:dono,rotulo:'',eventos:[],em:0,resultado:true};passos.push(resultado);}
      resultado.eventos.push(e.id);atual=resultado;continue;
    }
    if(!CONTABIL.has(e.kind)||ehDaMecanica(e)){unicaAberta=null;resultado=null;}
    // Refletir, Espinhos, Vampirismo e os jeitos de bater (Ricochete, Roubou Carga…): um passo com o nome da mecânica
    if(!ehDaMecanica(e)&&(CONTABIL.has(e.kind)||(e.kind==='tempo'&&Math.abs(e.value??0)<.005))){if(atual)atual.eventos.push(e.id);else soltos.push(e.id);continue;}
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
  const ORDEM:Record<ClasseDoPasso,number>={golpe:0,rival:1,aliado:2,reacao:9,unica:9};
  const blocos:Passo[][]=[];let antes:Passo[]=[];
  for(const x of passos){
    if(x.classe==='reacao'||x.classe==='unica'){if(blocos.length)blocos.at(-1)!.push(x);else antes.push(x);}
    else blocos.push([x]);
  }
  blocos.sort((a,b)=>ORDEM[a[0]!.classe]-ORDEM[b[0]!.classe]);
  if(blocos.length){blocos[0]!.splice(1,0,...antes);antes=[];}
  passos.length=0;passos.push(...blocos.flat(),...antes);
  if(!passos.length)passos.push({classe:'golpe',quem:ator,eventos:[],em:0});
  passos[0]!.eventos.unshift(...soltos);
  separaRajadas(passos,beat);
  separaGolpes(passos,beat);
  tempoDosPassos(passos,beat);
  return passos;
}
/*
 * Os golpes da rajada da Mecânica única (src/presentation/rajada-da-unica.ts): cada um sai do passo em que caiu (o
 * golpe da habilidade, a ativação) e vira um passo próprio logo depois da ativação, para o número, o tremor e o som
 * saírem um por um, na hora em que cada projétil chega. O nocaute que um golpe causa vai junto dele.
 */
function separaRajadas(passos:Passo[],beat:Pick<Beat,'events'|'after'>):void{
  const personagem=(uid:string)=>beat.after.fighters.find(f=>f.uid===uid)?.characterId;
  const donoDe=(e:BattleEvent)=>e.kind==='block'?(e.attacker??e.source):e.source;
  const grupos=new Map<string,number[][]>();
  beat.events.forEach((e,k)=>{
    const dono=donoDe(e);
    if(!ehDaRajada(e,personagem(dono)))return;
    const golpe=[e.id];
    // o nocaute logo depois do golpe que derrubou
    for(let j=k+1;j<beat.events.length;j++){const x=beat.events[j]!;if(x.kind==='ko'&&x.target===e.target){golpe.push(x.id);break;}if(x.kind!=='charge'&&x.kind!=='synergy')break;}
    (grupos.get(dono)??grupos.set(dono,[]).get(dono)!).push(golpe);
  });
  for(const [dono,golpes] of grupos){
    if(golpes.length<2)continue;
    const ids=new Set(golpes.flat());
    for(const x of passos)x.eventos=x.eventos.filter(id=>!ids.has(id));
    // logo depois da ativação dela (o passo com o aviso da Mecânica única de quem soltou)
    let k=passos.findIndex(x=>x.quem===dono&&x.eventos.some(id=>beat.events.find(e=>e.id===id)?.kind==='unica'));
    if(k<0)k=passos.length-1;
    const novos:Passo[]=golpes.map((eventos,i)=>({classe:'reacao',quem:dono,rotulo:'',eventos,em:0,resultado:true,rajada:{i,n:golpes.length,chave:`u:${personagem(dono)}`}}));
    passos.splice(k+1,0,...novos);
  }
  // um passo que ficou vazio (o golpe da habilidade era só a rajada) sai da cadeia, menos o primeiro
  for(let i=passos.length-1;i>0;i--)if(!passos[i]!.eventos.length&&!passos[i]!.rajada)passos.splice(i,1);
}
/*
 * Os golpes da habilidade de vários golpes (src/engine/golpes.ts): o motor já dividiu o dano em partes; a primeira
 * parte de cada alvo cai no impacto, e as outras vêm em sequência, um golpe por passo (alvo por alvo), cada uma com o
 * seu número. O nocaute fica com a última parte do alvo que caiu.
 */
function separaGolpes(passos:Passo[],beat:Pick<Beat,'event'|'events'|'after'>):void{
  const e0=beat.event;
  if(e0.kind!=='skill'||e0.skill===undefined)return;
  const personagem=beat.after.fighters.find(f=>f.uid===e0.source)?.characterId;
  const chave=`h:${personagem}:${e0.skill}`;
  if(!rajadaDaChave(chave))return;
  const donoDe=(e:BattleEvent)=>e.kind==='block'?(e.attacker??e.source):e.source;
  // as partes por (golpe, alvo): bloqueio e dano da mesma parte andam juntos
  const porParte=new Map<string,number[]>(),ordem:string[]=[];
  for(const e of beat.events){
    if((e.parte??0)<1||!e.partes||donoDe(e)!==e0.source||!e.target)continue;
    const k=`${e.parte}|${e.target}`;
    if(!porParte.has(k)){porParte.set(k,[]);ordem.push(k);}
    porParte.get(k)!.push(e.id);
  }
  if(!ordem.length)return;
  ordem.sort((a,b)=>Number(a.split('|')[0])-Number(b.split('|')[0]));
  const ids=new Set([...porParte.values()].flat());
  // o nocaute vai com a última parte do alvo
  for(const e of beat.events)if(e.kind==='ko'&&e.target){const ult=[...ordem].reverse().find(k=>k.endsWith(`|${e.target}`));if(ult){porParte.get(ult)!.push(e.id);ids.add(e.id);}}
  for(const x of passos)x.eventos=x.eventos.filter(id=>!ids.has(id));
  const k=Math.max(0,passos.findIndex(x=>x.classe==='golpe'));
  const novos:Passo[]=ordem.map((key,i)=>({classe:'reacao',quem:e0.source,rotulo:'',eventos:porParte.get(key)!,em:0,resultado:true,rajada:{i,n:ordem.length,chave}}));
  passos.splice(k+1,0,...novos);
}
/** Depois de o efeito da Mecânica única chegar (no meio da cadeia), quanto ele fica à vista. */
const DEPOIS_NA_CADEIA=1.0;
/**
 * O tempo de cada passo depois do impacto, comprimido se a cadeia ficar longa. A Mecânica única no meio da cadeia
 * tem as fases dela (concentra, nome, carga, solta) e o resultado aparece quando o efeito chega; ela não encurta.
 * Devolve quanto o beat ainda precisa depois do último passo.
 */
export function tempoDosPassos(passos:Passo[],beat:Pick<Beat,'event'|'events'|'after'|'base'>):number{
  const ator=beat.event.source,lado=beat.after.fighters.find(f=>f.uid===ator)?.side;
  const ladoDe=(uid?:string)=>beat.after.fighters.find(f=>f.uid===uid)?.side;
  const fasesDe=(x:Passo)=>{const e=beat.events.find(y=>y.kind==='unica'&&x.eventos.includes(y.id));return e?fasesDoEvento(e,beat.after,{events:beat.events,after:beat.after,passos,traco:false}):undefined;};
  const daUnica=(k:number)=>{const x=passos[k]!;return x.classe==='unica'&&!x.antecipada||!!x.rajada||!!x.resultado&&passos[k-1]?.classe==='unica'&&!passos[k-1]!.antecipada;};
  const intervalo=(k:number)=>{
    const x=passos[k]!;
    // a rajada: um golpe a cada intervalo dela; depois do último, o tempo de ver o resultado
    if(x.rajada){const r=rajadaDaChave(x.rajada.chave);return passos[k+1]?.rajada?(r?.intervalo??.3):x.rajada.chave.startsWith('h:')?TEMPO_DO_PASSO.golpe:DEPOIS_NA_CADEIA;}
    // o golpe de uma habilidade de vários golpes: o segundo golpe vem logo, no ritmo da rajada
    if(x.classe==='golpe'&&passos[k+1]?.rajada?.chave.startsWith('h:'))return rajadaDaChave(passos[k+1]!.rajada!.chave)?.intervalo??.2;
    if(x.classe==='unica'){if(x.antecipada)return .05;const f=fasesDe(x);return (f?.impactoEm??PREPARO_DA_UNICA)+(passos[k+1]?.resultado?0:DEPOIS_NA_CADEIA);}
    if(x.resultado&&daUnica(k))return DEPOIS_NA_CADEIA;
    return TEMPO_DO_PASSO[x.resultado?'reacao':x.classe];
  };
  const intervalos=passos.slice(0,-1).map((_,k)=>intervalo(k));
  // a ativação da Mecânica única não encurta: é o momento dela (a cadeia comprime só o resto)
  const total=intervalos.reduce((a,b,k)=>a+(daUnica(k)?0:b),0),escala=total>CADEIA_MAXIMA?CADEIA_MAXIMA/total:1;
  let t=0;passos.forEach((x,k)=>{x.em=t;t+=(intervalos[k]??0)*(daUnica(k)?1:escala);});
  // depois de um golpe, o que cai no próprio trio (cura, Escudo, reforço, o traço em quem agiu) espera
  // quem bateu voltar para o lugar: antes, o efeito saía com o personagem ainda no caminho de volta
  const bateu=passos[0]?.classe==='golpe'&&beat.events.some(e=>e.kind==='damage'&&e.source===ator&&ladoDe(e.target)!==lado);
  // o que alguém do meu trio (quem bateu ou um aliado) faz em alguém do meu trio: sem alvo, é nele mesmo
  const noMeuTrio=(x:Passo)=>ladoDe(x.quem)===lado&&x.eventos.some(id=>{const e=beat.events.find(y=>y.id===id);return !!e&&ladoDe(e.target??e.source)===lado&&(ehDaMecanica(e)||!CONTABIL.has(e.kind));});
  const k=bateu?passos.findIndex((x,i)=>i>0&&(x.classe==='aliado'||((x.classe==='reacao'||x.classe==='unica')&&noMeuTrio(x)))):-1;
  const volta=(VOLTA_DO_GOLPE-P.impactAt)*(beat.base??0);
  if(k>0&&passos[k]!.em<volta){const atraso=volta-passos[k]!.em;for(let i=k;i<passos.length;i++)passos[i]!.em+=atraso;}
  // a última ainda precisa do tempo dela
  const n=passos.length-1,ultimo=passos[n];
  if(!ultimo)return 0;
  if(ultimo.classe==='unica'&&!ultimo.antecipada)return (fasesDe(ultimo)?.impactoEm??0)+DEPOIS_NA_CADEIA;
  if(daUnica(n))return DEPOIS_NA_CADEIA;
  return 0;
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
    let vistos2=statuses;
    for(const e of meus){
      if(e.kind==='status'&&e.status){
        const novo=f.statuses.find(s=>s.id===e.status);const k=vistos2.findIndex(s=>s.id===e.status);
        if(novo){if(k>=0)vistos2[k]=structuredClone(novo);else vistos2.push(structuredClone(novo));}
      }
      // Purificar/Dissipar: os Status somem no passo em que saíram
      if((e.kind==='cleanse'||e.kind==='dispel')&&e.removidos)vistos2=vistos2.filter(s=>!e.removidos!.includes(s.id));
    }
    f.statuses=vistos2;
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
  const d:Direction={battle,visible:structuredClone(battle),queue:[],active:null,simIdle:0,complete:false,serial:0,signals:[],unicaCheia:{}};
  /*
   * As Mecânicas únicas que ficam sempre ativas ativam no começo da luta, como uma habilidade (pedido do
   * jogador: "se já começa ativa, no começo da batalha já mostra ele ativando… aparecendo o nome dele"). O aviso
   * é só da apresentação: não entra na luta (a numeração dos eventos da luta escolhe alvos), e o número dele fica
   * entre 0 e 1, antes do primeiro evento de verdade.
   */
  if(battle.time===0&&battle.nextEvent<=1)battle.fighters.forEach((f,i)=>{
    const u=UNICAS[f.characterId];if(!u||JEITO_DA_UNICA[f.characterId]!=='sempre')return;
    const aviso:BattleEvent={id:(i+1)/10,time:0,kind:'unica',source:f.uid,target:f.uid,label:u.nome};
    const antes=structuredClone(battle);
    d.unicaCheia![f.uid]=0;
    d.queue.push(makeBeat(aviso,[aviso],antes,antes,false,false,true,new Set([f.uid])));
  });
  return d;
}
/** Quem tem a ativação completa da Mecânica única neste momento (a regra está em unicas-efeitos.ts). */
function ativacoesCheias(d:Direction,events:BattleEvent[],after:Battle):Set<string>{
  const cheias=new Set<string>();
  for(const e of events){
    if(e.kind!=='unica'||cheias.has(e.source))continue;
    const f=after.fighters.find(x=>x.uid===e.source);if(!f||e.leve||soONome(f.characterId,e.label))continue;
    const vista=(d.unicaCheia??={})[e.source];
    if(vista!==undefined&&after.time-vista<INTERVALO_DA_UNICA)continue;
    d.unicaCheia[e.source]=after.time;cheias.add(e.source);
  }
  return cheias;
}
function makeBeat(event:BattleEvent,events:BattleEvent[],before:Battle,after:Battle,periodic=false,previous=false,traco=false,cheias?:ReadonlySet<string>):Beat {
  const actor=after.fighters.find(f=>f.uid===event.source);
  const prep=actor&&event.skill!==undefined?byId[actor.characterId].skills[event.skill].preparation:0;
  const grand=event.kind==='skill'&&prep>=P.grandPreparation;
  const auxiliary=event.kind==='ready'||event.kind==='status';
  const unicaSozinha=traco&&event.kind==='unica'&&!!cheias?.has(event.source);
  // sozinha, o impacto espera as fases dela (concentra, nome, carga, solta) e a viagem até o alvo: o número aparece quando o golpe chega
  const fases=unicaSozinha?fasesDoEvento(event,after,{events,after,traco:true}):undefined;
  const seconds=traco?(fases?fases.impactoEm/P.impactAt:TEMPO_DO_TRACO):previous?(periodic?.55:auxiliary?.5:duration(event,grand)):periodic?P.periodicSeconds:duration(event,grand);
  const beat:Beat={event,events,before,after,duration:seconds,family:familyOf(event,after),grand,elapsed:0,impacted:false,periodic,etapa:0,base:seconds,traco};
  beat.passos=montaPassos(beat,cheias);
  beat.etapas=beat.passos.map((_,k)=>k+1);
  beat.antecipa=antecipaDoGolpe(beat);
  // quem ativa antes de o golpe cair (o atacante antes de partir, quem é atingido no meio do caminho): na cadeia
  // fica só o resultado
  const pausas=cheias&&!traco?pausasDoGolpe(beat,seconds*P.impactAt,beat.antecipa):[];
  let cauda=traco?0:-1;
  if(pausas.length){beat.pausas=pausas;for(const p of pausas)beat.passos[p.passo]!.antecipada=true;cauda=tempoDosPassos(beat.passos,beat);}
  else if(!traco)cauda=tempoDosPassos(beat.passos,beat);
  const ultimo=beat.passos.at(-1)!;
  beat.duration+=ultimo.em+Math.max(0,cauda)+(fases?Math.max(0,DEPOIS_DA_UNICA-(seconds-fases.impactoEm)):0);
  return beat;
}
/*
 * O golpe desenhado cai junto do número (pedido do jogador: "o dano tá aparecendo antes da animação … tem que ser
 * no impacto da animação o dano aparecer"). Muitas folhas contam o golpe inteiro — a onda sobe e só quebra no
 * quadro 6, o punho desce e só bate no quadro 3 —, então a folha e o som dela começam antes do impacto, o bastante
 * para o quadro do golpe (QUADRO_DO_GOLPE) chegar no instante em que o número sai. As contas da duração da folha
 * são as mesmas do BattleEffects.
 */
export function antecipaDoGolpe(beat:Beat):number{
  if((beat.event.kind!=='basic'&&beat.event.kind!=='skill')||beat.periodic||beat.traco)return 0;
  const ator=beat.after.fighters.find(f=>f.uid===beat.event.source);
  const perfil=ator?profileFor(ator.characterId,beat.event.skill):undefined;
  if(!perfil)return 0;
  const fam=familia(perfil.family),quadro=QUADRO_DO_GOLPE[fam.impacto]??0;
  // a varredura e o golpe que quica já têm a hora certa de bater em cada alvo
  if(!quadro||fam.varre||fam.encadeia)return 0;
  const viaja=!!perfil.travel&&!!beat.event.target&&beat.event.target!==beat.event.source;
  const dur=Math.max(.42,beat.duration*(1-P.impactAt)*fam.tempo),pula=viaja&&fam.pula?fam.pula:0,folha=dur/(1-pula);
  let antes=Math.max(0,quadro/12*folha-pula*folha);
  // o objeto que voa chega no impacto: a folha só pode começar um instante antes de ele chegar
  if(viaja)antes=Math.min(antes,.2);
  antes=Math.min(antes,duracaoBase(beat)*P.impactAt*.9);
  // menos que dois quadros não se vê: a folha sai junto do impacto
  return antes>=.1?antes:0;
}
function collect(d:Direction,events:BattleEvent[],before:Battle,after:Battle,legacy=false,previous=false){
  if(!events.length)return;
  // Every observer callback is a chronological boundary: one action and its
  // consequences, or periodic effects. Never merge across an action boundary.
  const principal=focus(events);
  const cheias=!previous&&!legacy?ativacoesCheias(d,events,after):undefined;
  if(principal&&['basic','skill','cast'].includes(principal.kind)){
    d.queue.push(makeBeat(principal,events,before,after,false,false,false,cheias));
    return;
  }
  if(principal&&!previous){d.queue.push(makeBeat(principal,events,before,after,false,false,false,cheias));return;}
  // a Mecânica única disparando sozinha (relógio, reação) ganha um momento com o nome dela
  const unica=!previous&&!legacy?events.find(e=>(e.kind==='unica'&&e.label!=='Imune')||e.kind==='pulso'):undefined;
  if(unica){d.queue.push(makeBeat(unica,events,before,after,false,false,true,cheias));return;}
  // fora de uma ação, Status e Escudo só nascem de um traço disparando sozinho: ganha um momento próprio
  const traco=!previous&&!legacy?events.find(e=>e.kind==='status'||(e.kind==='shield'&&e.label==='Escudo')):undefined;
  if(traco){d.queue.push(makeBeat(traco,events,before,after,false,false,true));return;}
  // a Marca explosiva estourando é um momento próprio, não um "efeito contínuo"
  const bum=events.find(e=>e.kind==='damage'&&e.label==='Explosão');
  if(bum&&!previous&&!legacy){d.queue.push(makeBeat(bum,events,before,after));return;}
  const change=events.find(e=>e.kind==='damage'||e.kind==='heal');
  if(change){
    const burning=change.kind==='damage'&&change.label!=='Veneno'&&before.fighters.find(f=>f.uid===change.target)?.statuses.some(s=>s.id==='burning');
    const veneno=change.kind==='damage'&&change.label==='Veneno';
    const event={...change,label:veneno?'Veneno':burning?'Queimadura':change.kind==='heal'?'Regeneração':'Efeito contínuo',status:veneno?'poison' as const:burning?'burning' as const:change.kind==='heal'?'regen' as const:undefined};
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
    d.active.golpeou=checkpoint.impacted;
    // voltando no meio de um golpe que já passou do ponto da pausa: a resposta já foi vista
    for(const p of d.active.pausas??[])if(d.active.elapsed>=p.em-1e-8&&(d.active.elapsed>p.em+1e-8||d.active.impacted))p.t=p.dura;
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
    /*
     * A pausa do golpe: chegando no ponto dela, o golpe fica parado e só o tempo da ativação de quem foi atacado
     * corre (concentra, nome, carga, a defesa aparecendo). Depois o golpe continua de onde parou.
     */
    const parada=golpeParado(beat);
    if(parada){parada.t=Math.min(parada.dura,parada.t+elapsed);return;}
    const proxima=!beat.impacted?beat.pausas?.find(x=>x.t<x.dura):undefined;
    beat.elapsed=Math.min(limit,beat.elapsed+elapsed,proxima?proxima.em:Infinity);
    const etapas=beat.etapas??[1];
    // a folha do golpe começa antes, para o golpe desenhado cair no impacto (sempre sai antes da deixa do impacto)
    if(!beat.golpeou&&beat.antecipa&&beat.elapsed>=impacto-beat.antecipa-1e-8){
      beat.golpeou=true;
      onCue?.({event:beat.event,family:beat.family,phase:'golpe',grand:beat.grand});
      return;
    }
    if(!beat.impacted&&beat.elapsed>=limit-1e-8){
      beat.impacted=true;beat.etapa=etapas[0];
      if(beat.trace)beat.trace.realImpact=performance.now();
      d.visible=visivelNaEtapa(beat,beat.etapa!);
      d.signals.push(...beat.events.filter(e=>etapaDoEvento(beat,e)<=beat.etapa!));
      beat.golpeou=true;
      onCue?.({event:beat.event,family:beat.family,phase:'impact',grand:beat.grand,antecipado:!!beat.antecipa});
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
