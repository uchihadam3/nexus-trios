import {byId,characters} from '../data/characters';
import type {Battle,BattleEvent} from './types';
import type {RunBattleSummary} from './run-summary';
import {statuses} from '../data/statuses';

export type Metric='battles'|'wins'|'journeys'|'champions'|'perfect'|'damage'|'healing'|'protection'|'interrupts'|'statuses'|'turns'|'synergies'|'unique'|'universes'|'trios'|'skills'|'kos';
export type Counters=Record<Metric,number>;
export const emptyCounters=():Counters=>({battles:0,wins:0,journeys:0,champions:0,perfect:0,damage:0,healing:0,protection:0,interrupts:0,statuses:0,turns:0,synergies:0,unique:0,universes:0,trios:0,skills:0,kos:0});
export interface Objective {id:string;label:string;metric:Metric;target:number;progress:number;reward:number;difficulty:'Fácil'|'Médio'|'Difícil'}
export interface Mastery {skills:[number,number,number];journeys:number;level:0|1|2|3}
export interface ProgressState {xp:number;title:string;seen:string[];unlocked:string[];stats:Counters;mastery:Record<string,Mastery>;daily:{key:string;items:Objective[]};weekly:{key:string;items:Objective[]}}
export interface Achievement {id:string;name:string;category:string;metric:Metric;target:number;secret?:boolean}
type EventTally={lastId:number;statuses:number;interrupts:number;turns:number;synergies:number};
export const emptyTally=():EventTally=>({lastId:0,statuses:0,interrupts:0,turns:0,synergies:0});

const tiers=(category:string,metric:Metric,names:string[],targets:number[]):Achievement[]=>names.map((name,i)=>({id:`${metric}-${category}-${i+1}`,name,category,metric,target:targets[i]}));
export const achievements:Achievement[]=[
  ...tiers('Jornada','journeys',['Primeira trilha','Rota conhecida','Pés na estrada','Viajante Nexus','Horizonte sem fim'],[1,5,15,35,75]),
  ...tiers('Combate','wins',['Primeira vitória','Sequência de dez','Veterano da arena','Centurião','Lenda de trios'],[1,10,30,100,250]),
  ...tiers('Sinergia','synergies',['Primeira conexão','Aliados em sintonia','Rede de apoio','Trio afinado','Orquestra Nexus'],[1,15,50,150,400]),
  ...tiers('Coleção','unique',['Primeiro encontro','Elenco curioso','Cinquenta vozes','Cem estilos','Duzentas histórias'],[1,10,50,100,200]),
  ...tiers('Vantagem','turns',['Primeira virada','Luta disputada','Vento mudou','Especialista em viradas','Mestre da recuperação'],[1,5,20,60,150]),
  ...tiers('Controle','interrupts',['Quebra de ritmo','Corta o Preparo','Sem tempo para reagir','Guarda aberta','Silêncio na arena'],[1,10,30,100,250]),
  ...tiers('Proteção','protection',['Primeiro bloqueio','Escudo do trio','Muralha amiga','Defesa heroica','Guardião absoluto'],[100,1000,5000,20000,60000]),
  ...tiers('Cura','healing',['Primeiro resgate','Cuidado constante','Trio recuperado','Mãos de esperança','Fonte inesgotável'],[100,1000,5000,20000,60000]),
  ...tiers('Personagens','skills',['Primeira técnica','Ferramentas novas','Arsenal testado','Grande repertório','Mil escolhas'],[1,25,100,400,1000]),
  ...tiers('Segredos','perfect',['Todos de pé','Outra vez juntos','Impecável','Trio intacto','Companheiros inseparáveis'],[1,5,15,40,100]),
];
export function nexusLevel(xp:number){return Math.max(1,Math.floor(Math.sqrt(Math.max(0,xp)/100))+1)}
export function emptyProgress():ProgressState{return {xp:0,title:'Explorador Nexus',seen:[],unlocked:[],stats:emptyCounters(),mastery:{},daily:{key:'',items:[]},weekly:{key:'',items:[]}};}
const objectives:Omit<Objective,'progress'>[]=[
  {id:'journey-wins',label:'Vença 3 confrontos',metric:'wins',target:3,reward:100,difficulty:'Médio'},
  {id:'journey-survive',label:'Vença com os três de pé 2 vezes',metric:'perfect',target:2,reward:90,difficulty:'Médio'},
  {id:'journey-skills',label:'Veja 12 habilidades do seu trio',metric:'skills',target:12,reward:70,difficulty:'Fácil'},
  {id:'journey-interrupt',label:'Interrompa 2 preparações',metric:'interrupts',target:2,reward:110,difficulty:'Médio'},
  {id:'journey-status',label:'Aplique 6 Status negativos',metric:'statuses',target:6,reward:80,difficulty:'Fácil'},
  {id:'journey-heal',label:'Recupere 500 de Vida',metric:'healing',target:500,reward:90,difficulty:'Médio'},
  {id:'journey-protect',label:'Bloqueie 500 de dano',metric:'protection',target:500,reward:90,difficulty:'Médio'},
  {id:'journey-turn',label:'Faça a Vantagem virar',metric:'turns',target:1,reward:110,difficulty:'Difícil'},
  {id:'journey-synergy',label:'Crie 5 conexões de Carga',metric:'synergies',target:5,reward:100,difficulty:'Médio'},
];
const capable=(team:string[],metric:Metric)=>{
  const cards=team.map(id=>byId[id]);
  const effects=cards.flatMap(c=>[...c.trait.effects,...c.skills.flatMap(s=>s.effects)]);
  if(metric==='healing')return effects.some(e=>e.kind==='heal'||e.kind==='status'&&e.status==='regen');
  if(metric==='protection')return effects.some(e=>e.kind==='shield'||e.kind==='status'&&e.status==='protected');
  if(metric==='interrupts')return effects.some(e=>e.kind==='interrupt');
  if(metric==='statuses')return effects.some(e=>e.kind==='status'&&statuses[e.status].tone==='negativo');
  if(metric==='synergies')return effects.some(e=>e.kind==='charge'&&e.target==='allAllies')||cards.some(c=>c.skills.some(s=>s.charge.some(rule=>['status','negativeStatus','allyHurt','protected'].includes(rule.on))));
  return true;
};
export function journeyObjectives(team:string[],seed:number):Objective[]{
  const eligible=objectives.filter(o=>capable(team,o.metric));
  const base=[eligible[seed%eligible.length],eligible[(seed+3)%eligible.length],eligible[(seed+5)%eligible.length]];
  const unique=[...new Map(base.map(o=>[o.id,o])).values()];
  for(const o of eligible)if(unique.length<3&&!unique.includes(o))unique.push(o);
  return unique.slice(0,3).map(o=>({...o,progress:0}));
}
const dailyTemplates:Omit<Objective,'progress'>[]=[
  {id:'daily-play',label:'Entre em 2 confrontos',metric:'battles',target:2,reward:50,difficulty:'Fácil'},
  {id:'daily-win',label:'Vença um confronto',metric:'wins',target:1,reward:60,difficulty:'Fácil'},
  {id:'daily-skills',label:'Veja 5 habilidades acontecerem',metric:'skills',target:5,reward:60,difficulty:'Fácil'},
];
const weeklyTemplates:Omit<Objective,'progress'>[]=[
  {id:'weekly-journey',label:'Conclua 2 Jornadas',metric:'journeys',target:2,reward:120,difficulty:'Médio'},
  {id:'weekly-win',label:'Vença 6 confrontos',metric:'wins',target:6,reward:160,difficulty:'Médio'},
  {id:'weekly-status',label:'Aplique 12 Status negativos',metric:'statuses',target:12,reward:140,difficulty:'Médio'},
  {id:'weekly-help',label:'Ajude o trio com 10 conexões',metric:'synergies',target:10,reward:160,difficulty:'Médio'},
];
const periodKey=(date:Date,weekly=false)=>{const d=new Date(Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate()));if(weekly)d.setUTCDate(d.getUTCDate()-(d.getUTCDay()+6)%7);return d.toISOString().slice(0,10)};
export function refreshPeriods(p:ProgressState,date=new Date()):ProgressState{
  const daily=periodKey(date),weekly=periodKey(date,true);
  return {...p,daily:p.daily.key===daily?p.daily:{key:daily,items:dailyTemplates.map(o=>({...o,progress:0}))},weekly:p.weekly.key===weekly?p.weekly:{key:weekly,items:weeklyTemplates.map(o=>({...o,progress:0}))}};
}
export function tallyEvents(tally:EventTally,events:BattleEvent[]):EventTally{
  const next={...tally};for(const e of events){if(e.id<=next.lastId)continue;next.lastId=e.id;if(e.source.startsWith('player-')){
    if(e.kind==='status'&&e.status&&statuses[e.status].tone==='negativo'&&e.target?.startsWith('enemy-'))next.statuses++;
    if(e.kind==='interrupt')next.interrupts++;
    if(e.kind==='turn')next.turns++;
    if(e.kind==='synergy'&&e.target?.startsWith('player-'))next.synergies++;
  }}return next;
}
const advance=(items:Objective[],delta:Counters)=>items.map(o=>({...o,progress:Math.min(o.target,o.progress+delta[o.metric])}));
export function advanceObjectives(items:Objective[],delta:Counters){return advance(items,delta)}
export function liveObjectives(items:Objective[],battle:Battle,tally:EventTally):Objective[]{
  const delta=emptyCounters(),players=battle.fighters.filter(f=>f.side==='player');
  delta.damage=players.reduce((n,f)=>n+f.stats.damage,0);delta.healing=players.reduce((n,f)=>n+f.stats.healing,0);delta.protection=players.reduce((n,f)=>n+f.stats.protection,0);
  delta.interrupts=tally.interrupts;delta.statuses=tally.statuses;delta.turns=tally.turns;delta.synergies=tally.synergies;
  delta.skills=players.reduce((n,f)=>n+f.skills.reduce((m,s)=>m+s.uses,0),0);
  return advance(items,delta);
}
export function battleDelta(summary:RunBattleSummary,battle:Battle,tally:EventTally,seen:string[],team:string[]):Counters{
  const next=emptyCounters();next.battles=1;next.wins=Number(summary.won);next.perfect=Number(summary.won&&summary.survivors===3);
  next.damage=summary.fighters.reduce((n,f)=>n+f.damage,0);next.healing=summary.fighters.reduce((n,f)=>n+f.healing,0);next.protection=summary.fighters.reduce((n,f)=>n+f.protection,0);
  next.interrupts=Math.max(tally.interrupts,summary.fighters.reduce((n,f)=>n+f.interrupts,0));next.statuses=tally.statuses;next.turns=tally.turns;next.synergies=tally.synergies;
  next.skills=battle.fighters.filter(f=>f.side==='player').reduce((n,f)=>n+f.skills.reduce((a,s)=>a+s.uses,0),0);
  next.kos=summary.fighters.reduce((n,f)=>n+f.kills,0);next.unique=team.filter(id=>!seen.includes(id)).length;
  next.universes=new Set(team.map(id=>byId[id].universe)).size===3&&summary.won?1:0;next.trios=summary.won?1:0;return next;
}
export function recordProgress(state:ProgressState,delta:Counters,battle:Battle,team:string[],journeyEnded=false,champion=false,date=new Date()):ProgressState{
  const p=refreshPeriods(state,date),stats={...p.stats};for(const key of Object.keys(stats) as Metric[])stats[key]+=delta[key];
  if(journeyEnded){stats.journeys++;delta={...delta,journeys:1};if(champion){stats.champions++;delta.champions=1;}}
  const seen=[...new Set([...p.seen,...team])],mastery={...p.mastery};
  for(const f of battle.fighters.filter(x=>x.side==='player')){
    const old=mastery[f.characterId]??{skills:[0,0,0] as [number,number,number],journeys:0,level:0 as const};
    const skills=old.skills.map((n,i)=>n+f.skills[i].uses) as [number,number,number];
    const journeys=old.journeys+(champion?1:0),level=(journeys>=1&&skills[2]>=3?3:skills[2]>=2?2:skills[0]>=1?1:0) as Mastery['level'];
    mastery[f.characterId]={skills,journeys,level};
  }
  const unlocked=[...p.unlocked];for(const a of achievements)if(stats[a.metric]>=a.target&&!unlocked.includes(a.id))unlocked.push(a.id);
  const completedBefore=(items:Objective[])=>items.filter(o=>o.progress>=o.target).length;
  const daily=advance(p.daily.items,delta),weekly=advance(p.weekly.items,delta);
  const objectiveXp=(completedBefore(daily)-completedBefore(p.daily.items))*60+(completedBefore(weekly)-completedBefore(p.weekly.items))*140;
  const xp=p.xp+20+Number(delta.wins)*30+Number(champion)*250+(unlocked.length-p.unlocked.length)*75+objectiveXp;
  return {...p,xp,seen,stats,mastery,unlocked,daily:{...p.daily,items:daily},weekly:{...p.weekly,items:weekly}};
}
export const masteryChallenges=(id:string)=>{
  const c=characters.find(x=>x.id===id)!;
  return [`I · Ative ${c.skills[0].name} em uma batalha.`,`II · Use ${c.skills[2].name} 2 vezes.`,`III · Vença uma Jornada com ${c.name} e ative ${c.skills[2].name} 3 vezes no total.`];
};
