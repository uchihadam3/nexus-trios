import { mkdirSync, writeFileSync } from 'node:fs';
import { createBattle, stepBattle } from '../src/engine/battle';
import { expandedCharacters, rosterIdentityReviewGroups } from '../src/data/expanded-roster';
import type { Battle, BattleEvent, Skill } from '../src/engine/types';

const SAMPLES=12;
type Context='enemyCast'|'incoming'|'vulnerable'|'threatened'|'injured'|'winning'|'losing'|'open';
type Probe={skill:number;sequence?:string;context?:Context;ready?:number[];natural?:boolean;maxSeconds?:number};
const adjustedSkill:Record<string,number>={frieza:1,kakashi:2,itachi:2,nezuko:1,ichigo:1,kenpachi:2,levi:2,gon:2,killua:1,alphonse:2,roy:0,guts:2,denji:1,yor:1,kaneki:2,scarletwitch:2,daredevil:0,punisher:2,blade:0,moonknight:2,storm:2,jeangrey:2,rogue:2,gambit:2,venom:1,carnage:0,loki:1,ultron:2,starlord:2,cyborg:2,shazam:2};
const redesignedProbe:Record<string,Probe>={
 piccolo:{skill:0,sequence:'cast inimigo → leitura marca e enfraquece a ameaça',context:'enemyCast'},sakura:{skill:2,sequence:'aliado ferido → Byakugou cura e regenera o trio',context:'injured'},inosuke:{skill:0,sequence:'cast inimigo → instinto atrasa e confunde a ameaça',context:'enemyCast'},muzan:{skill:0,sequence:'ação → chicotes atingem e marcam os três inimigos',context:'open'},yuji:{skill:1,sequence:'alvo vulnerável → Black Flash aplica a segunda onda',context:'vulnerable'},eren:{skill:1,sequence:'Condição baixa → endurecimento protege Eren',context:'injured'},griffith:{skill:1,sequence:'aliado ameaçado → comando acelera/reposiciona o trio',context:'threatened'},giorno:{skill:0,sequence:'aliado ferido → Vida criada cura e regenera',context:'injured'},power:{skill:2,sequence:'Domínio em desvantagem → Prêmio de sangue explode e confunde',context:'losing'},frieren:{skill:2,sequence:'preparação inimiga → magia carregada atrasa e atinge o conjurador',context:'enemyCast'},loid:{skill:1,sequence:'preparação inimiga → neutralização cancela o cast',context:'enemyCast'},yugi:{skill:2,sequence:'preparar duelo → Mago Negro → invocação final (ordem obrigatória)',natural:true,maxSeconds:120},kaiba:{skill:2,sequence:'pressão direta → Dragão Branco → Ultimate Burst (ordem obrigatória)',natural:true,maxSeconds:120},blackpanther:{skill:2,sequence:'recebe impacto → armazena energia cinética → descarrega e zera o estoque',context:'incoming'},vision:{skill:1,sequence:'faseia → reduz o impacto recebido → volta sólido e usa raio solar',context:'incoming'},antman:{skill:1,sequence:'inimigo ferido → formigas aceleram/reposicionam o trio',context:'open'},captainmarvel:{skill:2,sequence:'absorve impacto → armazena energia → explosão binária a libera',context:'incoming'},professorx:{skill:2,sequence:'coordena carga aliada → interrompe cast com controle mental',context:'enemyCast'},doctordoom:{skill:2,sequence:'armadura tecnológica → ritual místico → contingência (ordem obrigatória)',natural:true,maxSeconds:120},silversurfer:{skill:1,sequence:'impacto recebido → transmutação vira proteção e mobilidade',context:'incoming'},greenlantern:{skill:0,sequence:'escudo, prisão e arma adaptam-se a três ameaças/contextos',context:'threatened'},
};
const charById=new Map(expandedCharacters.map(c=>[c.id,c]));
function setup(id:string,seed:number,context:Context,ready:number[],natural=false):Battle{
  const supportPool=['superman','groot','captain','piccolo','strange','batman','pikachu','thor'];
  const player=[id,...supportPool.filter(x=>x!==id).slice(0,2)];
  const enemyPool=['goku','vegeta','naruto','sasuke','luffy','saitama','gojo','light'];
  const enemies=enemyPool.filter(x=>!player.includes(x)).slice(0,3);
  const b=createBattle(player,enemies,seed,1.5);
  for(const f of b.fighters){f.maxHp=100000;f.hp=100000;}
  const actor=b.fighters[0];
  if(context==='injured'){actor.hp=70000;for(const f of b.fighters.slice(3))f.hp=70000;}
  if(context==='threatened'||context==='incoming')b.fighters[1].hp=70000;
  if(context==='vulnerable')for(const f of b.fighters.slice(3))f.statuses.push({id:'exposed',remaining:30,intensity:.25,source:'player-1'});
  if(context==='enemyCast')b.fighters[3].cast={skill:2,elapsed:0,duration:100,targets:[actor.uid]};
  if(context==='incoming')b.fighters[3].cast={skill:0,elapsed:0,duration:.3,targets:[actor.uid]};
  if(context==='winning'){for(const f of b.fighters.slice(3))f.hp=85000;b.dominion=24;b.momentum=35;}
  if(context==='losing'){b.dominion=-24;b.momentum=-35;}
  if(natural){
    // Let a real opponent enter a telegraphed cast, so observers charge from the engine event.
    b.fighters[3].skills[2].charge=100;
    b.fighters.slice(0,3).forEach(f=>f.statuses.push({id:'exposed',remaining:50,intensity:.15,source:'enemy-0'}));
    b.fighters.slice(3).forEach(f=>f.statuses.push({id:'exposed',remaining:50,intensity:.15,source:'player-1'}));
    if(id==='kaiba'){for(const f of b.fighters.slice(3))f.hp=85000;b.dominion=24;b.momentum=35;}
  }else ready.forEach(index=>{actor.skills[index].charge=100;});
  return b;
}
function evidenceKinds(skill:Skill):Set<string>{
  const kinds=new Set<string>();
  for(const effect of skill.effects){
    if(effect.kind==='damage'||effect.kind==='release')kinds.add('damage');
    if(effect.kind==='heal')kinds.add('heal');
    if(effect.kind==='shield')kinds.add('shield');
    if(effect.kind==='status')kinds.add('status');
    if(effect.kind==='interrupt')kinds.add('interrupt');
    if(effect.kind==='store')kinds.add('stored');
    if(effect.kind==='charge')kinds.add('synergy');
  }
  return kinds;
}
function hasEvidence(skill:Skill,events:BattleEvent[],afterId:number):boolean{
  const expected=evidenceKinds(skill);
  return events.some(e=>e.id>afterId&&e.source==='player-0'&&(
    (expected.has('damage')&&e.kind==='damage')||
    (expected.has('heal')&&e.kind==='heal')||
    (expected.has('shield')&&['shield','block'].includes(e.kind))||
    (expected.has('status')&&e.kind==='status')||
    (expected.has('interrupt')&&e.kind==='interrupt')||
    (expected.has('stored')&&e.kind==='shield'&&e.label.includes('armazenada'))||
    (expected.has('synergy')&&['synergy','ready'].includes(e.kind))
  ));
}
function runProbe(id:string,probe:Probe,seed:number):{ok:boolean;events:BattleEvent[];battle:Battle}{
  const c=charById.get(id)!;const skill=c.skills[probe.skill];
  const context=probe.context??(skill.condition==='enemyCast'||skill.target==='enemyCast'?'enemyCast':skill.condition==='vulnerable'?'vulnerable':skill.condition==='threatened'?'threatened':skill.condition==='injured'?'injured':skill.condition==='storedEnergy'?'incoming':'open');
  const ready=probe.natural?(probe.ready??[]):(probe.ready??[probe.skill]);const b=setup(id,seed,context,ready,probe.natural);
  const events:BattleEvent[]=[];let last=0;const limit=Math.ceil((probe.maxSeconds??60)*10);
  for(let i=0;i<limit&&!b.finished;i++){
    stepBattle(b);
    for(const e of b.events)if(e.id>last){events.push(e);last=Math.max(last,e.id);}
    const used=events.find(e=>e.kind==='skill'&&e.source==='player-0'&&e.skill===probe.skill);
    if(used&&hasEvidence(skill,events,used.id))return {ok:true,events,battle:b};
  }
  return {ok:false,events,battle:b};
}
function observedCSequence(id:string,events:BattleEvent[],battle:Battle):boolean{
  const actor=battle.fighters[0];const skillEvents=events.filter(e=>e.kind==='skill'&&e.source==='player-0');
  if(id==='vision'){
    const phase=skillEvents.find(e=>e.skill===0),ray=skillEvents.find(e=>e.skill===1);
    const block=events.find(e=>e.kind==='block'&&e.source==='player-0'&&e.target==='player-0');
    return !!phase&&!!ray&&!!block&&phase.id<block.id&&block.id<ray.id;
  }
  if(id==='blackpanther'||id==='captainmarvel'){
    const store=events.find(e=>e.source==='player-0'&&e.kind==='shield'&&e.label.includes('armazenada'));
    const discharge=skillEvents.find(e=>e.skill===2);
    const hit=events.find(e=>e.source==='player-0'&&e.kind==='damage'&&e.id>(discharge?.id??Infinity));
    return !!store&&store.value!>0&&!!discharge&&!!hit&&hit.value!>0&&store.id<discharge.id&&actor.storedEnergy===0;
  }
  if(id==='doctordoom'||id==='yugi'){
    const seq=[0,1,2].map(i=>skillEvents.find(e=>e.skill===i)?.id??0);
    return seq.every((value,i)=>value>0&&(i===0||value>seq[i-1]));
  }
  if(id==='kaiba'){
    const summon=skillEvents.find(e=>e.skill===1),final=skillEvents.find(e=>e.skill===2);
    return !!summon&&!!final&&summon.id<final.id&&events.some(e=>e.kind==='damage'&&e.id<summon.id&&e.source==='player-0');
  }
  return skillEvents.some(e=>e.skill===redesignedProbe[id]?.skill)&&events.some(e=>e.source==='player-0'&&e.id>0&&['damage','heal','shield','status','interrupt','synergy'].includes(e.kind));
}

const rows:Record<string,{sequence:string;trials:number;passes:number;status:string;note?:string}>={};
for(const c of expandedCharacters){
  const id=c.id;
  if(id==='vision'||id==='blackpanther'||id==='captainmarvel'||id==='doctordoom'||id==='yugi'||id==='kaiba'){
    let passes=0;
    for(let seed=1;seed<=SAMPLES;seed++){
      const p=redesignedProbe[id];const ready=id==='vision'?[0]:id==='blackpanther'||id==='captainmarvel'?[2]:id==='doctordoom'||id==='yugi'||id==='kaiba'?[]:[0,1];
      const context=id==='vision'||id==='blackpanther'||id==='captainmarvel'?'incoming':id==='kaiba'?'winning':'vulnerable';
      const result=runProbe(id,{...p,context,ready,natural:['doctordoom','yugi','kaiba'].includes(id),maxSeconds:120},seed+12000);
      if(observedCSequence(id,result.events,result.battle))passes++;
    }
    const sequence=redesignedProbe[id].sequence!;
    rows[id]={sequence,trials:SAMPLES,passes,status:passes===SAMPLES?'comprovada':'falha',note:passes<SAMPLES?'A cadeia não completou naturalmente em todas as lutas.':''};
    continue;
  }
  if(id==='greenlantern'){
    const branches=[{skill:0,context:'threatened' as Context,label:'escudo do aliado ameaçado'},{skill:1,context:'enemyCast' as Context,label:'prisão que cancela preparação'},{skill:2,context:'vulnerable' as Context,label:'arma ofensiva contra abertura'}];
    const branchResults=branches.map((branch)=>{let passes=0;for(let n=0;n<4;n++){const r=runProbe(id,{...branch,ready:[branch.skill]},13000+n);if(r.ok)passes++;}return `${branch.label}: ${passes}/4`;});
    const passes=branchResults.every(x=>x.endsWith('4/4'))?SAMPLES:0;
    rows[id]={sequence:branchResults.join('; '),trials:SAMPLES,passes,status:passes===SAMPLES?'comprovada':'falha'};
    continue;
  }
  if(id==='professorx'){
    let coord=0,control=0;
    for(let n=0;n<6;n++){
      const a=runProbe(id,{skill:0,context:'open'},14000+n);if(a.events.some(e=>e.kind==='synergy'&&e.source==='player-0'))coord++;
      const b=runProbe(id,{skill:2,context:'enemyCast'},15000+n);if(b.events.some(e=>e.kind==='interrupt'&&e.source==='player-0'))control++;
    }
    const passes=coord===6&&control===6?12:0;
    rows[id]={sequence:`coordenação do trio: ${coord}/6; interrupção mental: ${control}/6; dano básico configurado em 20`,trials:12,passes,status:passes===12?'comprovada':'falha'};
    continue;
  }
  const cGroup=(rosterIdentityReviewGroups.redesigned as readonly string[]).includes(id);
  const probe=cGroup?redesignedProbe[id]:{skill:adjustedSkill[id]??2};let passes=0;
  for(let seed=1;seed<=SAMPLES;seed++){
    const result=runProbe(id,probe,seed+(cGroup?16000:20000));
    const event=result.events.find(e=>e.kind==='skill'&&e.source==='player-0'&&e.skill===probe.skill);
    const skill=charById.get(id)!.skills[probe.skill];
    if(event&&hasEvidence(skill,result.events,event.id))passes++;
  }
  rows[id]={sequence:cGroup?(probe.sequence??`habilidade ${probe.skill+1}`):`habilidade ${probe.skill+1} (${c.skills[probe.skill].name}) emitiu efeito de ${[...evidenceKinds(c.skills[probe.skill])].join('/')}`,trials:SAMPLES,passes,status:passes===SAMPLES?'comprovada':'falha'};
}

const groups={redesigned:rosterIdentityReviewGroups.redesigned as readonly string[],adjusted:rosterIdentityReviewGroups.smallAdjustments as readonly string[],excellent:rosterIdentityReviewGroups.excellent as readonly string[]};
const groupSummary=Object.fromEntries(Object.entries(groups).map(([group,ids])=>[group,{count:ids.length,passed:ids.filter(id=>rows[id].status==='comprovada').length,failed:ids.filter(id=>rows[id].status!=='comprovada').map(id=>({id,...rows[id]}))}]));
const redesigned=groups.redesigned.map(id=>({id,name:charById.get(id)!.name,...rows[id]}));
const report=`# Validação comportamental do elenco — ${new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date())}\n\nAs provas executam stepBattle em contextos preparados e registram eventos/efeitos reais. Para Yugi, Kaiba e Doctor Doom, as cargas dos personagens evoluem durante até 120 s; os demais começam com a habilidade testada pronta para isolar sua consequência. As sequências só contam quando a ação e pelo menos um efeito observável aparecem, nunca apenas pelo uso do botão/skill.\n\n- Novos personagens: ${expandedCharacters.length}/76 avaliados; 12 sementes por contrato.\n- Resultado por grupo: ${JSON.stringify(groupSummary)}\n- Campeonatos de jornada não são alvo desta validação.\n\n## Vinte e um redesenhados\n\n| Personagem | Sequência característica observada | Simulações | Identidade | Nota |\n|---|---|---:|---|---|\n${redesigned.map(x=>`| ${x.name} | ${x.sequence} | ${x.passes}/${x.trials} | ${x.status==='comprovada'?'comprovada':'não comprovada'} | ${x.note??''} |`).join('\n')}\n\n## Cobertura dos outros grupos\n\n${groups.adjusted.map(id=>`- ${charById.get(id)!.name}: ${rows[id].passes}/${rows[id].trials} probes do ajuste — ${rows[id].status}. ${rows[id].sequence}.`).join('\n')}\n\n${groups.excellent.map(id=>`- ${charById.get(id)!.name}: ${rows[id].passes}/${rows[id].trials} probes da ação característica — ${rows[id].status}.`).join('\n')}\n`;
mkdirSync('docs',{recursive:true});writeFileSync('docs/roster-behavior-validation.md',report);
writeFileSync('docs/roster-behavior-validation.json',JSON.stringify({samplesPerCharacter:SAMPLES,groupSummary,characters:rows},null,2));
console.log(JSON.stringify({groupSummary,redesigned:redesigned.map(({id,name,...x})=>({id,name,...x})),total:expandedCharacters.length,failed:Object.entries(rows).filter(([,r])=>r.status!=='comprovada').map(([id,r])=>({id,...r}))},null,2));
if(Object.values(rows).some(row=>row.status!=='comprovada'))throw new Error('Falha na validação comportamental; consulte docs/roster-behavior-validation.md.');
