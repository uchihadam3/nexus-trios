import { byId } from '../data/characters';
import { CHOQUE_DO_ELETRIFICADO, RITMO_DA_INVOCACAO, statuses } from '../data/statuses';
import { random,shuffle } from './random';
import { DOMINION as D, fracaoPorAlvo} from './dominion-config';
import type { Battle, BattleEvent, Effect, Fighter, Side, Skill, StatusId, Target, Topic } from './types';
import { chooseTarget, inferTargetIntent } from './targeting';

export const STEP=.1;
const clamp=(n:number,lo=0,hi=1)=>Math.min(hi,Math.max(lo,n));
export const alive=(f:Fighter)=>f.hp>0;
export const intensity=(f:Fighter,id:StatusId)=>f.statuses.find(s=>s.id===id)?.intensity??0;
const friendly=(b:Battle,f:Fighter)=>b.fighters.filter(x=>x.side===f.side&&alive(x));
const hostile=(b:Battle,f:Fighter)=>b.fighters.filter(x=>x.side!==f.side&&alive(x));
/* Derivado de `statuses`, nunca repetido: ver a nota de tom em data/statuses.ts. */
export const negativeStatuses=new Set<StatusId>((Object.keys(statuses) as StatusId[]).filter(id=>statuses[id].tone==='negativo'));
const sign=(f:Fighter)=>f.side==='player'?1:-1;
const pressure=(b:Battle,side:Side,points:number)=>{b.momentum=clamp(b.momentum+(side==='player'?1:-1)*points,-D.maxScore,D.maxScore);};
export function emit(b:Battle,e:Omit<BattleEvent,'id'|'time'>){b.events.push({...e,id:b.nextEvent++,time:b.time});if(b.events.length>180)b.events.shift();}

export function createBattle(player:string[],enemy:string[],seed=Date.now(),enemyScale=1):Battle {
  if(player.length!==3||enemy.length!==3||new Set(player).size!==3||new Set(enemy).size!==3||[...player,...enemy].some(id=>!byId[id]))throw new Error('Cada equipe precisa de três personagens diferentes e válidos.');
  const b:Battle={version:1,seed,rng:seed>>>0,time:0,fighters:[],dominion:0,momentum:0,events:[],nextEvent:1,winner:null,reason:'',finished:false,turns:0,lastLead:null};
  for(const side of ['player','enemy'] as Side[]) (side==='player'?player:enemy).forEach((id,slot)=>{
    const c=byId[id], maxHp=Math.round(c.hp*(side==='enemy'?enemyScale:1));
    b.fighters.push({uid:`${side}-${slot}`,characterId:id,side,slot,hp:maxHp,maxHp,action:random(b)*.12,skills:c.skills.map(()=>({charge:0,cooldown:0,executing:0,uses:0})),statuses:[],shields:[],cast:null,investigation:{},discovered:{},traitTimer:0,storedEnergy:0,stats:{damage:0,healing:0,protection:0,interrupts:0,skills:0,kills:0}});
  });
  return b;
}
export function targets(b:Battle,actor:Fighter,rule:Target,effects:Effect[]=[],record=true):Fighter[] {
  const allies=friendly(b,actor).sort((a,z)=>a.characterId.localeCompare(z.characterId)),enemies=hostile(b,actor).sort((a,z)=>a.characterId.localeCompare(z.characterId));
  if(rule==='self')return alive(actor)?[actor]:[];
  // Reviver: o aliado caído mais forte que ainda pode voltar (cada lutador só volta uma vez)
  if(rule==='allyFallen')return caidos(b,actor).slice(0,1);
  if(rule==='allAllies')return allies;
  if(rule==='allEnemies')return enemies;
  if(actor.characterId==='light'&&rule==='enemyWeak'&&effects.some(effect=>effect.kind==='investigate')){
    const unknown=enemies.filter(x=>!actor.discovered?.[x.uid]);
    if(unknown.length)return chooseTarget(b,actor,unknown,rule,'investigate',effects,record);
  }
  if(actor.characterId==='light'&&rule==='investigated'){
    const isInvestigation=effects.some(effect=>effect.kind==='investigate');
    const isDeathNote=effects.some(effect=>effect.kind==='deathnote');
    if(isInvestigation){
      const unknown=enemies.filter(x=>!actor.discovered?.[x.uid]);
      if(unknown.length)return chooseTarget(b,actor,unknown,rule,'investigate',effects,record);
      return chooseTarget(b,actor,enemies,rule,'investigate',effects,record);
    }
    if(isDeathNote){
      const vulnerable=enemies.filter(x=>actor.discovered?.[x.uid]==='vulnerable'&&(actor.investigation[x.uid]??0)>=100);
      if(vulnerable.length)return chooseTarget(b,actor,vulnerable,rule,'finisher',effects,record);
      if(enemies.every(x=>actor.discovered?.[x.uid]==='immune'))return chooseTarget(b,actor,enemies.filter(x=>(actor.investigation[x.uid]??0)>=100),rule,'finisher',effects,record);
      return [];
    }
  }
  /*
   * Marcar com cabeça (pedido do jogador): a marca vai no rival que o trio
   * derruba mais rápido (menos Vida + Escudo), quem já está marcado fica por
   * último, e no empate vai no mais perigoso. Marcar o rival errado é jogar a
   * marca fora: o trio inteiro vai mirar nele.
   */
  const marcaComCabeca=rule!=='allyWeak'&&rule!=='enemyCast'&&rule!=='randomEnemy'&&effects.some(e=>e.kind==='status'&&e.status==='marked');
  if(marcaComCabeca){
    const vivos=enemies.filter(alive);
    if(vivos.length){
      const custo=(x:Fighter)=>x.hp+x.shields.reduce((n,s)=>n+s.amount,0)+(intensity(x,'marked')>0?10000:0)-byId[x.characterId].power*.01;
      return [vivos.reduce((a,z)=>custo(z)<custo(a)?z:a)];
    }
  }
  // Provocado: todo golpe de um alvo vai em quem provocou, enquanto ele estiver de pé
  const provocador=rule!=='allyWeak'&&rule!=='enemyCast'?quemProvocou(b,actor):undefined;
  if(provocador)return [provocador];
  const intent=inferTargetIntent(actor,rule,effects);
  if(rule==='enemyCast'){
    const casting=enemies.filter(interrompivel);
    if(casting.length)return chooseTarget(b,actor,casting,rule,intent,effects,record);
    if(intent==='interrupt')return [];
  }
  return chooseTarget(b,actor,rule==='allyWeak'?allies:enemies,rule,intent,effects,record);
}
/*
 * `gain` dá Carga. `trigger` dá Carga **e** dispara o traço.
 *
 * Quatro tópicos passavam só pelo `gain`: enemyHurt, winning, losing e
 * survived. O tipo `Topic` permite declarar um traço em qualquer um deles, e a
 * ficha mostrava o texto normalmente — mas o traço nunca acontecia. Catorze
 * personagens tinham traço morto por isso, entre eles o "Anjo sem coração" do
 * Sephiroth, o "Glory Kill" do Doom Slayer e o "Presença dominante" do
 * Aquaman, que é dos 100 originais.
 *
 * Agora os quatro passam pelo `trigger`. O `traitTimer` já limita a
 * frequência, e todos os traços afetados têm recarga de um segundo ou mais —
 * então `survived`, `winning` e `losing`, que ocorrem a cada passo, não viram
 * disparo a cada passo.
 */
/*
 * O Preparo leve.
 *
 * Toda habilidade tem Preparo (pedido do jogador: o nome aparece antes do
 * golpe). As que eram instantâneas ganharam 0,5 s — e esse Preparo é leve: não
 * pode ser interrompido e não conta como "inimigo em Preparo", nem para a
 * condição nem para a Carga de quem vive de cortar golpes. Só os Preparos de
 * verdade (todos acima de 0,5 s, como antes) são alvo de interrupção.
 */
export const PREPARO_LEVE=.5;
const interrompivel=(x:Fighter)=>!!x.cast&&x.cast.duration>PREPARO_LEVE+1e-6;

/*
 * Reviver e Renascer (pedido do jogador: "levantar personagem caído").
 *
 * Reviver é um efeito de habilidade: levanta o aliado caído mais forte com
 * uma fração da Vida. Quem levanta faz isso uma vez por luta, e cada lutador
 * só volta uma vez (`voltou`). Renascer é de quem tem `renascer` na ficha: ao
 * cair, fica em brasas por `atraso` segundos e volta sozinho. A Death Note
 * impede (execução não tem volta). Enquanto alguém vai renascer, o trio dele
 * ainda não perdeu.
 */
/*
 * Provocar: um tanque grita, e os rivais atingidos ficam Provocados — o
 * ataque básico e as habilidades de um alvo só vão nele. Golpes em todos,
 * interrupções e Death Note seguem as próprias regras. Se quem provocou cai,
 * a provocação acaba na hora.
 */
function quemProvocou(b:Battle,actor:Fighter):Fighter|undefined{
  const s=actor.statuses.find(x=>x.id==='provoked');if(!s)return undefined;
  const f=b.fighters.find(x=>x.uid===s.source);
  return f&&f.side!==actor.side&&alive(f)?f:undefined;
}
const caidos=(b:Battle,actor:Fighter)=>b.fighters.filter(x=>x.side===actor.side&&!alive(x)&&!x.voltou&&!((x.renascendo??0)>0))
  .sort((a,z)=>byId[z.characterId].power-byId[a.characterId].power||a.uid.localeCompare(z.uid));
const podeReviver=(b:Battle,f:Fighter)=>!f.reviveu&&caidos(b,f).length>0;
const temReviver=(s:Skill)=>s.effects.some(e=>e.kind==='revive');
const voltando=(f:Fighter)=>(f.renascendo??0)>0;
function levanta(b:Battle,source:Fighter,target:Fighter,fracao:number){
  target.hp=Math.max(1,Math.round(target.maxHp*fracao));target.voltou=true;target.renascendo=0;
  target.statuses=[];target.shields=[];target.cast=null;target.action=0;
  target.skills.forEach(s=>{s.charge=0;s.cooldown=0;s.executing=0;});
  if(source.uid!==target.uid){source.stats.healing+=target.hp;source.stats.revives=(source.stats.revives??0)+1;}
  // voltar à luta pesa como um nocaute ao contrário
  pressure(b,target.side,D.event.knockout);
  emit(b,{kind:'revive',source:source.uid,target:target.uid,label:source.uid===target.uid?'Renasceu':'De pé!',value:target.hp});
}

function gain(b:Battle,f:Fighter,topic:Topic,amount:number,source?:Fighter){
  if(!alive(f))return;
  byId[f.characterId].skills.forEach((s,i)=>{
    const state=f.skills[i];
    if(state.cooldown>0||f.cast?.skill===i)return;
    const delta=s.charge.filter(c=>c.on===topic).reduce((sum,c)=>sum+c.amount*amount,0);
    const before=state.charge;state.charge=clamp(state.charge+delta,0,100);
    if(before<100&&state.charge>=100)emit(b,{kind:'ready',source:f.uid,skill:i,label:s.name,visual:s.icon});
    if(delta>0&&state.charge>before&&topic!=='time'){
      const gained=state.charge-before,actor=source??f;
      emit(b,{kind:'charge',source:actor.uid,target:f.uid,skill:i,label:topic,value:gained});
      if(source&&source.uid!==f.uid&&source.side===f.side){pressure(b,f.side,D.event.synergyCharge*clamp(gained/25));emit(b,{kind:'synergy',source:source.uid,target:f.uid,skill:i,label:s.name,value:gained});source.stats.carga=(source.stats.carga??0)+gained;}
    }
  });
}
function trigger(b:Battle,f:Fighter,topic:Topic,source?:Fighter,amount=1){
  if(!alive(f))return;
  gain(b,f,topic,amount,source);
  const t=byId[f.characterId].trait;
  if(t.on===topic&&f.traitTimer<=0){
    f.traitTimer=Math.max(t.cooldown,STEP);
    applyEffects(b,f,targets(b,f,t.target,t.effects),t.effects,amount);
  }
}
/*
 * Cada Status de "apanhar mais" faz uma coisa diferente (pedido do jogador:
 * três Status que só davam dano extra não faziam sentido):
 *   Exposto      — recebe mais dano (o único que aumenta o dano);
 *   Marcado      — só marca: os rivais miram nele (targeting.ts); quem marca escolhe o alvo (marcaComCabeca);
 *   Eletrificado — choque: cada golpe recebido atrasa a próxima ação dele.
 */
/*
 * Roubo de vida, Vampirismo, Refletir e Espinhos.
 *
 * `direto`: o golpe veio de um ataque ou habilidade. Queimadura e o próprio
 * dano devolvido não são diretos — senão dois lutadores com Refletir
 * devolveriam o golpe um para o outro para sempre.
 *   Vampirismo (Status em quem bate): cura parte do dano que causa.
 *   Refletir (em quem apanha): devolve parte do golpe, antes do Escudo.
 *   Espinhos (em quem apanha): quem bate leva um dano fixo por golpe.
 * O Roubo de vida é da habilidade (`lifesteal`, em applyEffects).
 */
/*
 * Purificar e Dissipar.
 *
 * Purificar tira dos aliados os debuffs que mais atrapalham primeiro (quem
 * está travado volta a agir antes de quem só está mais lento). Dissipar tira
 * dos rivais os buffs que mais ajudam primeiro. `value` é quantos Status saem.
 */
export const ORDEM_DA_PURIFICACAO:StatusId[]=['paralyzed','frozen','sleep','bomb','silenced','rooted','provoked','confused','blind','poison','bleed','cursed','slow','burning','exposed','marked','electric','weakened'];
export const ORDEM_DA_DISSIPACAO:StatusId[]=['summon','evasion','barrier','protected','reflect','vampirism','strengthened','haste','thorns','regen'];
const PESO_DO_DEBUFF:Partial<Record<StatusId,number>>={bomb:.8,paralyzed:1,frozen:.9,sleep:.8,silenced:.65,rooted:.7,provoked:.5,confused:.45,blind:.45,poison:.4,bleed:.4,cursed:.4,slow:.4};
const PESO_DO_BUFF:Partial<Record<StatusId,number>>={summon:.6,evasion:.5,barrier:.5,protected:.5,reflect:.45,vampirism:.45,strengthened:.4,haste:.4,thorns:.3,regen:.3};
function quaisSaem(alvo:Fighter,ordem:StatusId[],n:number):StatusId[]{
  const tem=new Set(alvo.statuses.map(s=>s.id));
  return [...ordem.filter(id=>tem.has(id)),...[...tem].filter(id=>!ordem.includes(id)&&ordem!==ORDEM_DA_DISSIPACAO&&negativeStatuses.has(id))].slice(0,Math.max(0,Math.round(n)));
}
function tiraStatus(b:Battle,source:Fighter,alvo:Fighter,kind:'cleanse'|'dispel',n:number){
  const ordem=kind==='cleanse'?ORDEM_DA_PURIFICACAO:ORDEM_DA_DISSIPACAO;
  const saem=quaisSaem(alvo,ordem,n);if(!saem.length)return;
  alvo.statuses=alvo.statuses.filter(s=>!saem.includes(s.id));
  if(kind==='cleanse')source.stats.buffs=(source.stats.buffs??0)+saem.length*3;else source.stats.debuffs=(source.stats.debuffs??0)+saem.length*3;
  pressure(b,source.side,D.event.statusApplied*.4*saem.length);
  emit(b,{kind,source:source.uid,target:alvo.uid,label:kind==='cleanse'?'Purificado':'Dissipado',value:saem.length,removidos:saem});
}
/*
 * Copiar habilidade: pega a última habilidade que um rival usou e a usa do
 * lado de quem copiou, com `fracao` da força (dano, cura e Escudo; os Status
 * vêm iguais). Execução, reviver, investigação, guardar energia e a própria
 * cópia não se copiam.
 */
const NAO_SE_COPIA=new Set<Effect['kind']>(['deathnote','investigate','revive','copy','store','release','lifesteal']);
export function ultimaHabilidadeRival(b:Battle,f:Fighter):{quem:Fighter;skill:Skill}|undefined{
  for(let i=b.events.length-1;i>=0;i--){
    const e=b.events[i]!;
    if(e.kind!=='skill'||e.skill===undefined)continue;
    const quem=b.fighters.find(x=>x.uid===e.source);
    if(!quem||quem.side===f.side)continue;
    const skill=byId[quem.characterId].skills[e.skill];
    if(skill&&!skill.effects.some(x=>x.kind==='copy'))return {quem,skill};
  }
  return undefined;
}
function copia(b:Battle,f:Fighter,fracao:number){
  const achou=ultimaHabilidadeRival(b,f);if(!achou)return;
  const effs=achou.skill.effects.filter(e=>!NAO_SE_COPIA.has(e.kind)).map(e=>(e.kind==='damage'||e.kind==='heal'||e.kind==='shield')?{...e,value:e.value*fracao}:e) as Effect[];
  if(!effs.length)return;
  emit(b,{kind:'copy',source:f.uid,target:achou.quem.uid,label:`Copiou ${achou.skill.name}`,visual:achou.skill.icon});
  applyEffects(b,f,targets(b,f,achou.skill.target,effs),effs);
}
/*
 * Invocação: uma criatura (o nome vem da ficha: Cão divino, Mago Negro…) luta
 * ao lado de quem invocou. Ela não é um lutador: não tem Vida, não é alvo e
 * some quando o tempo acaba, quando quem invocou cai ou com Dissipar. Ataca o
 * rival mais ferido (ou quem provocou), e os golpes dela são diretos: Esquiva,
 * Refletir e Espinhos valem.
 */
function invocacaoAtaca(b:Battle,f:Fighter,dano:number){
  const alvo=targets(b,f,'enemyWeak',[{kind:'damage',value:dano}])[0];if(!alvo)return;
  emit(b,{kind:'summon',source:f.uid,target:alvo.uid,label:byId[f.characterId].invocacao??'Invocação',value:dano});
  applyEffects(b,f,[alvo],[{kind:'damage',value:dano}]);
}
/* Sangramento: agir abre a ferida — cada ataque básico ou habilidade custa Vida. */
function sangra(b:Battle,f:Fighter){
  const s=f.statuses.find(x=>x.id==='bleed');if(!s||!alive(f))return;
  const origem=b.fighters.find(x=>x.uid===s.source)??f;
  damage(b,origem,f,Math.min(s.intensity,statuses.bleed.cap),false,'Sangramento');
}
function devolve(b:Battle,dono:Fighter,agressor:Fighter,valor:number,label:'Refletido'|'Espinhos'){
  if(valor<=.01||!alive(agressor))return;
  damage(b,dono,agressor,valor,false,label);
}
function damage(b:Battle,source:Fighter,target:Fighter,raw:number,direto=true,label='Impacto'){
  if(!alive(target))return;
  // o golpe devolvido é o próprio golpe (ou o espinho fixo): Fortalecido e Enfraquecido de quem devolve não mexem nele
  const devolvido=label==='Refletido'||label==='Espinhos';
  // Veneno e Sangramento são por dentro: passam por Exposto, Protegido e Escudo
  const interno=label==='Veneno'||label==='Sangramento';
  const outgoing=devolvido||interno?raw:raw*(1+intensity(source,'strengthened'))*(1-intensity(source,'weakened'));
  // Congelado: o golpe direto quebra o gelo e entra mais forte
  const gelo=direto?intensity(target,'frozen'):0;
  if(gelo>0){target.statuses=target.statuses.filter(s=>s.id!=='frozen');label='Quebrou o gelo';}
  const beforeProtection=interno?outgoing:outgoing*(1+intensity(target,'exposed'))*(1+gelo);
  const protection=interno?0:intensity(target,'protected');
  let amount=beforeProtection*(1-protection),blocked=beforeProtection-amount;
  // só o que é por dentro (Veneno, Sangramento) passa pelo Escudo; Marcado não atravessa mais (pedido do jogador)
  const atravessaEscudo=interno;
  if(!atravessaEscudo)for(const s of target.shields){const used=Math.min(s.amount,amount);s.amount-=used;amount-=used;blocked+=used;const owner=b.fighters.find(f=>f.uid===s.source);if(owner&&used>0){owner.stats.protection+=used;pressure(b,owner.side,D.event.usefulProtectionPerFullCondition*clamp(used/target.maxHp));emit(b,{kind:'block',source:owner.uid,target:target.uid,attacker:source.uid,label:'Bloqueio',value:used,visual:'shield'});trigger(b,owner,'protected',owner,used/100);}}
  target.shields=target.shields.filter(s=>s.amount>.01);
  if(protection>0){const owner=b.fighters.find(f=>f.uid===target.statuses.find(s=>s.id==='protected')?.source);if(owner){owner.stats.protection+=beforeProtection*protection;pressure(b,owner.side,D.event.usefulProtectionPerFullCondition*clamp(beforeProtection*protection/target.maxHp));emit(b,{kind:'block',source:owner.uid,target:target.uid,attacker:source.uid,label:'Proteção',value:beforeProtection*protection,visual:'shield'});trigger(b,owner,'protected',owner,beforeProtection*protection/100);}}
  const hpBefore=target.hp;
  // Última resistência: o golpe que derrubaria deixa com 1 de Vida, uma vez por luta
  const resiste=byId[target.characterId].ultimaResistencia;
  let resistiu=false;
  if(resiste&&!target.resistiu&&amount>=hpBefore&&hpBefore>1){amount=hpBefore-1;target.resistiu=true;resistiu=true;}
  const dealt=Math.min(hpBefore,amount);target.hp=Math.max(0,hpBefore-dealt);source.stats.damage+=dealt;
  if(dealt>.01){
    // Dormindo: o golpe direto acorda
    if(direto&&target.hp>0&&intensity(target,'sleep')>0){target.statuses=target.statuses.filter(s=>s.id!=='sleep');if(label==='Impacto')label='Acordou';}
    emit(b,{kind:'damage',source:source.uid,target:target.uid,label,value:dealt});
    const choque=intensity(target,'electric');if(choque>0&&target.hp>0)target.action=Math.max(0,target.action-choque*CHOQUE_DO_ELETRIFICADO);
    pressure(b,source.side,D.event.damagePerFullCondition*clamp(dealt/target.maxHp));
    if(beforeProtection>=hpBefore&&target.hp>0&&blocked>0)pressure(b,target.side,D.event.clutchSave);
    trigger(b,source,'dealt',source,dealt/100);
    trigger(b,target,'received',source,dealt/100);
    for(const f of b.fighters){if(f.side===target.side&&f.uid!==target.uid)trigger(b,f,'allyHurt',target,dealt/100);if(f.side!==target.side)trigger(b,f,'enemyHurt',source,dealt/100);}
    const vampiro=direto&&source.side!==target.side?intensity(source,'vampirism'):0;
    if(vampiro>0&&alive(source))healing(b,source,source,dealt*Math.min(vampiro,statuses.vampirism.cap),'Vampirismo');
  }
  if(direto&&source.side!==target.side){
    devolve(b,target,source,beforeProtection*Math.min(intensity(target,'reflect'),statuses.reflect.cap),'Refletido');
    devolve(b,target,source,Math.min(intensity(target,'thorns'),statuses.thorns.cap),'Espinhos');
  }
  if(resistiu&&resiste){
    const atual=target.statuses.find(s=>s.id==='protected');
    if(atual){atual.intensity=Math.max(atual.intensity,resiste.protegido);atual.remaining=Math.max(atual.remaining,resiste.duracao);}
    else target.statuses.push({id:'protected',remaining:resiste.duracao,duration:resiste.duracao,intensity:resiste.protegido,source:target.uid});
    pressure(b,target.side,D.event.clutchSave);
    emit(b,{kind:'resist',source:target.uid,target:target.uid,label:'Última resistência',value:1});
  }
  if(beforeProtection>target.maxHp*D.event.criticalThreshold/100&&alive(target)&&target.hp/target.maxHp<=D.event.criticalThreshold/100)pressure(b,source.side,D.event.criticalCrossing);
  if(!alive(target)){
    pressure(b,source.side,D.event.knockout);target.cast=null;target.action=0;target.statuses=[];target.shields=[];source.stats.kills++;
    emit(b,{kind:'ko',source:source.uid,target:target.uid,label:`${byId[target.characterId].name} incapacitado`});
    const renascer=byId[target.characterId].renascer;
    if(renascer&&!target.voltou)target.renascendo=renascer.atraso;
  }
}
function healing(b:Battle,source:Fighter,target:Fighter,value:number,label='Recuperação'){
  if(!alive(target))return;
  value*=1-Math.min(intensity(target,'cursed'),statuses.cursed.cap);
  const used=Math.min(target.maxHp-target.hp,value);target.hp+=used;source.stats.healing+=used;
  if(used>.01){pressure(b,source.side,D.event.usefulHealingPerFullCondition*clamp(used/target.maxHp));emit(b,{kind:'heal',source:source.uid,target:target.uid,label,value:used});}
}
export function applyEffects(b:Battle,source:Fighter,selected:Fighter[],effects:Effect[],scale=1){
  const danoAntes=source.stats.damage;
  /*
   * Esquiva: o rival com Esquiva rola uma vez por golpe; se escapou, nada do
   * que é contra ele entra (dano, debuff, interrupção) — o golpe passou longe.
   */
  const decidido=new Map<string,boolean>();
  const escapou=(alvo:Fighter)=>{
    if(alvo.side===source.side||!alive(alvo))return false;
    if(!decidido.has(alvo.uid)){
      const chance=Math.min(intensity(alvo,'evasion'),statuses.evasion.cap);
      const sim=chance>0&&random(b)<chance;
      decidido.set(alvo.uid,sim);
      if(sim)emit(b,{kind:'miss',source:source.uid,target:alvo.uid,label:'Esquivou'});
    }
    return decidido.get(alvo.uid)!;
  };
  for(const effect of effects){
    // Roubo de vida: cura quem age em parte do dano que esta habilidade causou
    if(effect.kind==='copy'){copia(b,source,effect.value);continue;}
    if(effect.kind==='lifesteal'){healing(b,source,source,(source.stats.damage-danoAntes)*effect.value,'Roubo de vida');continue;}
    const list=effect.target?targets(b,source,effect.target,[effect]):selected;
    if(effect.kind==='release'){
      const total=(source.storedEnergy??0)*effect.multiplier;
      source.storedEnergy=0;
      const targetsAlive=list.filter(alive),share=targetsAlive.length?total/targetsAlive.length:0;
      for(const target of targetsAlive)damage(b,source,target,share);
      continue;
    }
    /*
     * Quantos alvos vivos este efeito vai alcançar.
     *
     * Precisa ser contado **antes** do laço: se o primeiro alvo cair no
     * próprio golpe, os seguintes não podem receber uma fração diferente.
     */
    const vivosNoAlvo=list.filter(alive).length;
    const fracao=fracaoPorAlvo(vivosNoAlvo);
    for(const target of list){
      if(effect.kind==='revive'){
        if(!source.reviveu&&!alive(target)&&!target.voltou&&!voltando(target)&&target.side===source.side){source.reviveu=true;levanta(b,source,target,effect.value);}
        continue;
      }
      if(!alive(target))continue;
      if(['damage','status','interrupt','dispel','shift','release'].includes(effect.kind)&&target.side!==source.side&&escapou(target))continue;
      switch(effect.kind){
        case 'damage':damage(b,source,target,effect.value*fracao);break;
        case 'cleanse':if(target.side===source.side)tiraStatus(b,source,target,'cleanse',effect.value);break;
        case 'dispel':if(target.side!==source.side)tiraStatus(b,source,target,'dispel',effect.value);break;
        case 'heal':healing(b,source,target,effect.value);break;
        case 'shield':{
          const existing=target.shields.reduce((n,s)=>n+s.amount,0);
          const added=Math.max(0,Math.min(effect.value*(1-Math.min(intensity(target,'cursed'),statuses.cursed.cap)),target.maxHp*.55-existing));
          if(added>0){target.shields.push({amount:added,remaining:10,source:source.uid});emit(b,{kind:'shield',source:source.uid,target:target.uid,label:'Escudo',value:added,visual:'shield'});}break;
        }
        case 'status':{
          // Barreira: o próximo debuff de um rival não entra
          const barreira=target.side!==source.side&&negativeStatuses.has(effect.status)?target.statuses.find(s=>s.id==='barrier'):undefined;
          if(barreira){barreira.intensity-=1;if(barreira.intensity<.5)target.statuses=target.statuses.filter(s=>s!==barreira);emit(b,{kind:'resist',source:target.uid,target:target.uid,label:'Barreira',status:effect.status});break;}
          const def=statuses[effect.status],existing=target.statuses.find(s=>s.id===effect.status);
          if(existing){existing.remaining=Math.max(existing.remaining,effect.duration);existing.duration=Math.max(existing.duration??0,effect.duration);existing.intensity=Math.min(def.cap,def.stack==='add'?existing.intensity+effect.value:Math.max(existing.intensity,effect.value));existing.source=source.uid;}
          else target.statuses.push({id:effect.status,remaining:effect.duration,duration:effect.duration,intensity:Math.min(def.cap,effect.value),source:source.uid});
          /*
           * A duração vai no evento para o Raio-X não precisar adivinhá-la.
           *
           * A análise causal do pós-batalha pergunta coisas como "o Exposto que
           * A aplicou ainda estava de pé quando B bateu?". Sem a duração no
           * evento, a única saída seria uma janela de tempo arbitrária — ou
           * seja, inventar causalidade, que é exatamente o que a direção
           * proibiu. Com ela, a resposta é exata.
           */
          emit(b,{kind:'status',source:source.uid,target:target.uid,label:def.name,status:effect.status,value:effect.duration});
          if(target.side!==source.side)source.stats.debuffs=(source.stats.debuffs??0)+effect.duration;else source.stats.buffs=(source.stats.buffs??0)+effect.duration;
          if(target.side!==source.side){const weight=effect.status==='paralyzed'?1:effect.status==='rooted'?.65:effect.status==='slow'?.35:effect.status==='silenced'?.55:effect.status==='provoked'?.4:effect.status==='frozen'?.9:effect.status==='sleep'?.7:['blind','poison','bleed','cursed'].includes(effect.status)?.35:['exposed','marked','electric','burning'].includes(effect.status)?.3:0;if(weight)pressure(b,source.side,D.event.statusApplied*weight);}
          // Status events only charge observers; they cannot recursively execute other traits.
          const negative=target.side!==source.side&&negativeStatuses.has(effect.status);
          for(const f of friendly(b,source)){gain(b,f,'status',1,source);if(negative)gain(b,f,'negativeStatus',1,source);}
          if(target.side!==source.side){for(const f of friendly(b,source)){const t=byId[f.characterId].trait;if((t.on==='status'||negative&&t.on==='negativeStatus')&&f.traitTimer<=0){f.traitTimer=Math.max(t.cooldown,STEP);applyEffects(b,f,targets(b,f,t.target),t.effects);}}}
          break;
        }
        case 'interrupt':{
          if(!target.cast||!interrompivel(target))break;
          if(intensity(target,'protected')>=.3){emit(b,{kind:'shield',source:target.uid,target:target.uid,label:'Preparação protegida',visual:'shield'});break;}
          if(effect.mode==='cancel'){const i=target.cast.skill;target.cast=null;target.skills[i].charge=25;target.skills[i].cooldown=2;}
          else if(effect.mode==='delay')target.cast.elapsed=Math.max(-2,target.cast.elapsed-effect.value);
          else target.cast.elapsed=Math.max(0,target.cast.elapsed*(1-effect.value));
          source.stats.interrupts++;pressure(b,source.side,D.event.interruption);
          emit(b,{kind:'interrupt',source:source.uid,target:target.uid,label:effect.mode==='cancel'?'Interrompido!':'Preparação atrasada',visual:'bolt'});
          trigger(b,source,'interrupt',source);break;
        }
        case 'investigate':{const before=source.investigation[target.uid]??0,after=Math.min(100,before+effect.value);source.investigation[target.uid]=after;const quarters=Math.floor(after/25)-Math.floor(before/25);if(quarters>0)pressure(b,source.side,quarters*D.event.investigationQuarter+(after===100?D.event.investigationComplete:0));if(after===100&&!source.discovered?.[target.uid]){source.discovered??={};source.discovered[target.uid]=byId[target.characterId].deathNoteCompatible?'vulnerable':'immune';emit(b,{kind:'discovery',source:source.uid,target:target.uid,label:source.discovered[target.uid]==='vulnerable'?'Vulnerável à Death Note':'Imune à execução'});}break;}
        case 'deathnote':{
          if((source.investigation[target.uid]??0)<100)break;
          if(byId[target.characterId].deathNoteCompatible){const value=target.hp;target.hp=0;target.cast=null;target.shields=[];target.statuses=[];target.voltou=true;target.renascendo=0;source.stats.damage+=value;source.stats.kills++;pressure(b,source.side,D.event.deathNote);emit(b,{kind:'ko',source:source.uid,target:target.uid,label:'Sentença concluída',value});}
          else applyEffects(b,source,[target],[{kind:'status',status:'exposed',value:.55,duration:14},{kind:'damage',value:110}]);
          break;
        }
        case 'charge':target.skills.forEach((s,i)=>{if(s.cooldown<=0&&target.cast?.skill!==i){const before=s.charge;s.charge=Math.min(100,s.charge+effect.value);if(before<100&&s.charge>=100)emit(b,{kind:'ready',source:target.uid,skill:i,label:byId[target.characterId].skills[i].name,visual:byId[target.characterId].skills[i].icon});if(s.charge>before){emit(b,{kind:'charge',source:source.uid,target:target.uid,skill:i,label:source.uid===target.uid?'trait':'synergy',value:s.charge-before});if(source.uid!==target.uid){pressure(b,source.side,D.event.synergyCharge*clamp((s.charge-before)/25));emit(b,{kind:'synergy',source:source.uid,target:target.uid,skill:i,label:'Carga recebida',value:s.charge-before});source.stats.carga=(source.stats.carga??0)+(s.charge-before);}}}});break;
        case 'shift':{
          const before=target.action;target.action=clamp(target.action+effect.value);
          const delta=target.action-before;
          if(Math.abs(delta)>.005){emit(b,{kind:'tempo',source:source.uid,target:target.uid,label:delta>0?'Ação adiantada':'Ação atrasada',value:delta});source.stats.tempo=(source.stats.tempo??0)+Math.abs(delta);}
          break;
        }
        case 'store':source.storedEnergy=Math.min(effect.cap,(source.storedEnergy??0)+effect.value*scale);emit(b,{kind:'shield',source:source.uid,target:source.uid,label:'Energia cinética armazenada',value:source.storedEnergy,visual:'bolt'});break;
      }
    }
  }
}
/**
 * A regra de uso da habilidade está cumprida agora? Para a tela mostrar
 * "pronta, esperando a regra de uso". Roda numa cópia: a escolha de alvo grava
 * memória na luta, e olhar não pode mudar a luta.
 */
export function condicaoAtendida(b:Battle,f:Fighter,s:Skill):boolean{
  if(s.condition==='always'&&!s.requiresSkills?.length&&!temReviver(s))return true;
  const copia=structuredClone(b),eu=copia.fighters.find(x=>x.uid===f.uid);
  return !!eu&&appropriate(copia,eu,s);
}
function appropriate(b:Battle,f:Fighter,s:Skill){
  if(s.requiresSkills?.some(index=>(f.skills[index]?.uses??0)<1))return false;
  if(temReviver(s)&&podeReviver(b,f))return true;
  if(s.condition==='injured')return targets(b,f,s.target,s.effects).some(x=>x.hp/x.maxHp<.78);
  if(s.condition==='enemyCast')return hostile(b,f).some(interrompivel);
  if(s.condition==='threatened')return friendly(b,f).some(x=>x.hp/x.maxHp<.85)||hostile(b,f).some(interrompivel);
  if(s.condition==='investigated')return targets(b,f,s.target,s.effects,false).some(x=>(f.investigation[x.uid]??0)>=100);
  if(s.condition==='vulnerable')return hostile(b,f).some(x=>x.statuses.some(z=>['exposed','marked','paralyzed','electric','burning'].includes(z.id)));
  if(s.condition==='storedEnergy')return (f.storedEnergy??0)>0;
  return true;
}
function skillValue(b:Battle,f:Fighter,s:Skill,selected:Fighter[],intelligence:number):{score:number;reasons:string[]} {
  let value=0;const reasons:string[]=[],tacticalFactor=.65+intelligence/120;
  const add=(label:string,n:number)=>{if(n>0.05){value+=n;reasons.push(`${label} +${n.toFixed(1)}`);}};
  for(const effect of s.effects){
    if(effect.kind==='revive'){if(podeReviver(b,f))add('levantar aliado caído',70*effect.value*tacticalFactor);continue;}
    const list=(effect.target?targets(b,f,effect.target,[effect],false):selected).filter(alive);
    if(effect.kind==='damage'||effect.kind==='deathnote'||effect.kind==='release'){
      const raw=effect.kind==='release'?(f.storedEnergy??0)*effect.multiplier:effect.value;
      for(const target of list){
        const ready=effect.kind!=='deathnote'||(f.investigation[target.uid]??0)>=100;
        const shields=target.shields.reduce((n,x)=>n+x.amount,0),amount=ready?Math.min(target.hp+shields,raw):0;
        add('dano útil',amount/target.maxHp*65);
        if(amount>=target.hp+shields&&amount>0)add('incapacitação provável',18);
        if(effect.kind==='deathnote'&&ready)add('sentença preparada',f.discovered?.[target.uid]==='vulnerable'?40:10);
      }
    }else if(effect.kind==='heal'){
      for(const target of list){const used=Math.min(target.maxHp-target.hp,effect.value);add('cura necessária',used/target.maxHp*48*tacticalFactor);if(target.hp/target.maxHp<.3&&used>0)add('aliado crítico',8*tacticalFactor);}
    }else if(effect.kind==='shield'){
      for(const target of list){const existing=target.shields.reduce((n,x)=>n+x.amount,0);const need=target.maxHp*(1-target.hp/target.maxHp)+target.maxHp*.12-existing;const used=Math.max(0,Math.min(effect.value,need));add('proteção preventiva',used/target.maxHp*26*tacticalFactor);}
    }else if(effect.kind==='interrupt'){
      for(const target of list)if(target.cast&&interrompivel(target))add('interromper preparação',(22+Math.max(0,target.cast.elapsed/target.cast.duration)*12)*tacticalFactor);
    }else if(effect.kind==='status'&&effect.status==='provoked'){
      const aliados=friendly(b,f).filter(x=>x.uid!==f.uid);
      const fragil=aliados.length?Math.max(0,...aliados.map(x=>1-x.hp/x.maxHp)):0;
      const folego=f.hp/f.maxHp;
      for(const target of list){if(quemProvocou(b,target)?.uid===f.uid)continue;add('provocar',(6+fragil*18)*folego*tacticalFactor);}
    }else if(effect.kind==='status'){
      for(const target of list){const existing=target.statuses.find(x=>x.id===effect.status)?.intensity??0;const weight=effect.status==='paralyzed'?1:effect.status==='rooted'?.7:effect.status==='silenced'?.65:effect.status==='slow'?.4:['exposed','marked','electric','burning'].includes(effect.status)?.35:effect.status==='protected'?.5:effect.status==='vampirism'||effect.status==='reflect'?.45:effect.status==='frozen'?.9:effect.status==='sleep'?.75:effect.status==='barrier'?.5:effect.status==='evasion'?.45:['blind','cursed'].includes(effect.status)?.4:effect.status==='poison'||effect.status==='bleed'?.012:effect.status==='bomb'?.0025:effect.status==='summon'?.012:effect.status==='thorns'?.02:0;add('efeito de estado',Math.max(0,effect.value-existing)*weight*24*tacticalFactor);}
    }else if(effect.kind==='cleanse'||effect.kind==='dispel'){
      // vale o quanto atrapalhava (ou ajudava) o que vai sair
      const ordem=effect.kind==='cleanse'?ORDEM_DA_PURIFICACAO:ORDEM_DA_DISSIPACAO,peso=effect.kind==='cleanse'?PESO_DO_DEBUFF:PESO_DO_BUFF;
      for(const target of list){
        if((effect.kind==='cleanse')!==(target.side===f.side))continue;
        add(effect.kind==='cleanse'?'purificar':'dissipar',quaisSaem(target,ordem,effect.value).reduce((n,id)=>n+(peso[id]??.3),0)*24*tacticalFactor);
      }
    }else if(effect.kind==='copy'){
      if(ultimaHabilidadeRival(b,f))add('copiar habilidade',30*effect.value*tacticalFactor);
    }else if(effect.kind==='lifesteal'){
      // vale mais quanto mais ferido quem rouba está
      add('roubo de vida',effect.value*(1-f.hp/f.maxHp)*40*tacticalFactor);
    }else if(effect.kind==='investigate'){
      for(const target of list){const progress=f.investigation[target.uid]??0;add('investigação',effect.value/100*14*(1-progress/100)*tacticalFactor);}
    }else if(effect.kind==='charge'){
      add('carga de habilidades',Math.max(0,100-f.skills.reduce((n,x)=>n+x.charge,0))/300*12);
    }else if(effect.kind==='shift'){
      add('controle de ritmo',Math.abs(effect.value)*12);
    }else if(effect.kind==='store'){
      add('energia armazenada',Math.max(0,effect.cap-f.storedEnergy)/Math.max(1,effect.cap)*Math.min(18,effect.value/8));
    }
  }
  const cost=s.preparation*3+s.cooldown*.08;
  value=Math.max(0,value-cost)+s.priority*.08;
  if(cost>0)reasons.push(`custo tático -${cost.toFixed(1)}`);
  return {score:value,reasons};
}
function decideSkill(b:Battle,f:Fighter):number|null {
  const c=byId[f.characterId],intelligence=c.intelligence??50;
  const candidates=c.skills.map((s,i)=>({s,i,state:f.skills[i]}))
    .filter(({s,state})=>state.charge>=100&&state.cooldown<=0&&appropriate(b,f,s))
    .map(({s,i,state})=>{const selected=targets(b,f,s.target,s.effects,false);const result=skillValue(b,f,s,selected,intelligence);return {s,i,state,selected,...result};})
    .sort((a,z)=>z.score-a.score||a.i-z.i);
  if(!candidates.length)return null;
  const best=candidates[0];
  b.decisionLog??=[];
  b.decisionLog.push({time:b.time,actor:f.uid,intelligence,candidates:candidates.map(x=>({skill:x.s.name,score:x.score,target:x.selected[0]?.uid,reasons:x.reasons})),chosen:best.s.name});
  if(b.decisionLog.length>120)b.decisionLog.shift();
  return best.i;
}
function execute(b:Battle,f:Fighter,index:number,selected:Fighter[]){
  const s=byId[f.characterId].skills[index],eventStart=b.nextEvent;
  emit(b,{kind:'skill',source:f.uid,target:selected[0]?.uid,skill:index,label:s.name,visual:s.icon});
  applyEffects(b,f,selected,s.effects);
  sangra(b,f);
  const effective=b.events.some(e=>e.id>=eventStart&&(['damage','heal','block','interrupt','ko','synergy','revive','cleanse','dispel','copy'].includes(e.kind)||e.kind==='status'&&e.target!==f.uid));
  if(effective)pressure(b,f.side,s.preparation>=2.5?D.event.grandSkill:D.event.successfulSkill);
  f.stats.skills++;
  f.skills[index].uses=(f.skills[index].uses??0)+1;
  f.skills[index].charge=0;f.skills[index].cooldown=s.cooldown;f.skills[index].executing=.7;
}
export function updateDominion(b:Battle){
  const group=(side:Side)=>b.fighters.filter(f=>f.side===side);
  const health=(side:Side)=>group(side).reduce((n,f)=>n+f.hp/f.maxHp,0)/3;
  const count=(side:Side)=>group(side).filter(alive).length;
  const controlled=(side:Side)=>group(side).filter(alive).reduce((n,f)=>n+(Math.max(intensity(f,'paralyzed'),intensity(f,'frozen')>0?1:0,intensity(f,'sleep'))*D.controlStatus.paralyzed)+(intensity(f,'slow')*D.controlStatus.slowed)+(intensity(f,'rooted')*D.controlStatus.rooted)+(intensity(f,'silenced')*D.controlStatus.silenced)+(intensity(f,'exposed')*D.controlStatus.exposed)+(intensity(f,'marked')*D.controlStatus.marked),0);
  const situation=clamp((health('player')-health('enemy'))*D.situation.condition+(count('player')-count('enemy'))*D.situation.activeFighter+(controlled('enemy')-controlled('player'))*D.situation.control,-D.maxScore,D.maxScore);
  const target=clamp(situation*D.situationWeight+b.momentum*D.eventMemoryWeight,-D.maxScore,D.maxScore);
  const approach=1-Math.exp(-STEP/D.responseSeconds);
  b.dominion=clamp(b.dominion+(target-b.dominion)*approach,-D.maxScore,D.maxScore);
  const leader=b.dominion>5?'player':b.dominion< -5?'enemy':null;
  if(leader&&b.lastLead&&leader!==b.lastLead){b.turns++;if(leader==='player')b.viradasDoTrio=(b.viradasDoTrio??0)+1;emit(b,{kind:'turn',source:`${leader}-0`,label:'O Domínio virou'});}
  if(leader)b.lastLead=leader;
}
/*
 * Uma luta normal dura de 20 s a ~1,5 min. Raramente os dois lados se curam e
 * se protegem mais rápido do que se ferem, e a luta não acabava nunca: na tela
 * ficava rodando para sempre e o servidor recusava a jornada ("replay sem
 * conclusão"). Passado o limite, vence quem tem mais Vida (proporcional).
 * Só muda lutas que antes não terminavam.
 */
export const TEMPO_MAXIMO=300;
export function resolve(b:Battle){
  const naLuta=(f:Fighter)=>alive(f)||voltando(f);
  const p=b.fighters.some(f=>f.side==='player'&&naLuta(f)),e=b.fighters.some(f=>f.side==='enemy'&&naLuta(f));
  if(!p||!e){b.finished=true;b.winner=p?'player':e?'enemy':null;b.reason='Incapacitação da equipe';return;}
  if(b.time>=TEMPO_MAXIMO){
    const vida=(lado:string)=>{const t=b.fighters.filter(f=>f.side===lado);return t.reduce((n,f)=>n+Math.max(0,f.hp)/f.maxHp,0)/t.length;};
    b.finished=true;b.winner=vida('player')>=vida('enemy')?'player':'enemy';b.reason='Tempo esgotado · decidida pela Vida';
  }
}
export function stepBattle(b:Battle,observe?:(snapshot:Battle)=>void):Battle {
  if(b.finished)return b;
  b.time+=STEP;b.momentum*=Math.exp(-Math.LN2*STEP/D.memoryHalfLifeSeconds);
  for(const f of b.fighters){
    if(!alive(f)){
      if(voltando(f)){f.renascendo=Math.max(0,(f.renascendo??0)-STEP);if(f.renascendo<=1e-6)levanta(b,f,f,byId[f.characterId].renascer?.vida??.3);}
      continue;
    }
    f.traitTimer=Math.max(0,f.traitTimer-STEP);
    for(const s of [...f.statuses]){
      const origin=b.fighters.find(x=>x.uid===s.source)??f;
      if(s.id==='burning')damage(b,origin,f,s.intensity*STEP,false);
      if(s.id==='poison')damage(b,origin,f,s.intensity*STEP,false,'Veneno');
      // Invocação: a criatura ataca sozinha a cada RITMO_DA_INVOCACAO segundos, mesmo com quem invocou travado
      if(s.id==='summon'){const ja=(s.duration??s.remaining)-s.remaining;if(Math.floor((ja+STEP+1e-6)/RITMO_DA_INVOCACAO)>Math.floor((ja+1e-6)/RITMO_DA_INVOCACAO))invocacaoAtaca(b,f,Math.min(s.intensity,statuses.summon.cap));}
      // Marca explosiva: quando o tempo acaba, explode com o dano guardado
      if(s.id==='bomb'&&s.remaining-STEP<=1e-6){s.remaining=0;damage(b,origin,f,Math.min(s.intensity,statuses.bomb.cap),false,'Explosão');if(!alive(f))break;}
      if(s.id==='regen')healing(b,origin,f,s.intensity*STEP);
      s.remaining-=STEP;
    }
    resolve(b);if(b.finished){observe?.(b);return b;}
    f.statuses=f.statuses.filter(s=>s.remaining>0);f.shields.forEach(s=>s.remaining-=STEP);f.shields=f.shields.filter(s=>s.remaining>0&&s.amount>0);
    f.skills.forEach(s=>{s.cooldown=Math.max(0,s.cooldown-STEP);s.executing=Math.max(0,s.executing-STEP);});
    trigger(b,f,'time',undefined,STEP);trigger(b,f,'survived',undefined,STEP);
    if(b.dominion*sign(f)<-3)trigger(b,f,'losing',undefined,STEP);else if(b.dominion*sign(f)>3)trigger(b,f,'winning',undefined,STEP);
  }
  observe?.(b);
  for(const f of shuffle(b.fighters,b)){
    if(!alive(f))continue;
    const c=byId[f.characterId];
    const rate=(1+intensity(f,'haste'))*(1-intensity(f,'slow'))*(1-intensity(f,'rooted'));
    if(intensity(f,'paralyzed')||intensity(f,'frozen')||intensity(f,'sleep'))continue;
    if(f.cast){
      f.cast.elapsed+=STEP*rate;
      if(f.cast.elapsed>=f.cast.duration){const cast=f.cast;f.cast=null;let list=cast.targets.map(id=>b.fighters.find(x=>x.uid===id)).filter((x):x is Fighter=>!!x&&alive(x));if(!list.length&&c.skills[cast.skill].condition!=='investigated')list=targets(b,f,c.skills[cast.skill].target,c.skills[cast.skill].effects);execute(b,f,cast.skill,list);resolve(b);observe?.(b);if(b.finished)break;}
      continue;
    }
    if(!intensity(f,'silenced')){
      const selectedSkill=decideSkill(b,f);
      if(selectedSkill!==null){
        const i=selectedSkill,s=c.skills[i],list=targets(b,f,s.target,s.effects);
        if(s.preparation>0){f.cast={skill:i,elapsed:0,duration:s.preparation,targets:list.map(x=>x.uid)};emit(b,{kind:'cast',source:f.uid,target:list[0]?.uid,skill:i,label:s.name,visual:s.icon});if(s.preparation>PREPARO_LEVE)for(const opponent of hostile(b,f))trigger(b,opponent,'enemyCast',f);}
        else execute(b,f,i,list);
        resolve(b);observe?.(b);if(b.finished)break;
        continue;
      }
    }
    f.action+=STEP*rate/c.interval;
    if(f.action>=1){
      f.action-=1;
      const selected=intensity(f,'confused')&&random(b)<.25?[f]:targets(b,f,c.basic.target,c.basic.effects);
      emit(b,{kind:'basic',source:f.uid,target:selected[0]?.uid,label:c.basic.name,visual:c.basic.visual});
      // Cego: o golpe pode passar longe
      const cego=intensity(f,'blind');
      if(cego>0&&selected[0]&&selected[0].side!==f.side&&random(b)<Math.min(cego,statuses.blind.cap))emit(b,{kind:'miss',source:f.uid,target:selected[0].uid,label:'Errou'});
      else applyEffects(b,f,selected,c.basic.effects);
      sangra(b,f);
      trigger(b,f,'action',f);resolve(b);observe?.(b);if(b.finished)break;
    }
  }
  updateDominion(b);resolve(b);observe?.(b);return b;
}
export function simulate(player:string[],enemy:string[],seed=1,enemyScale=1):Battle {
  const b=createBattle(player,enemy,seed,enemyScale);while(!b.finished)stepBattle(b);return b;
}
