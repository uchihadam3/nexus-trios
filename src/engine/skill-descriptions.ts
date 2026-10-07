import { statuses } from '../data/statuses';
import type { Effect, Skill, Target, Topic, Trait, StatusId } from './types';

const n=(v:number)=>Number(v.toFixed(1)).toLocaleString('pt-BR');
const pct=(v:number)=>`${Math.round(v*100)}%`;
const secs=(v:number)=>`${n(v)} s`;
/*
 * Em quem o Status cai, dito junto com o verbo.
 *
 * `targetNames` é substantivo solto, para a linha "Alvo: ...". Colado num
 * "em", viraria "em o próprio personagem". Esta é a forma preposicionada, para
 * a frase ficar inteira: "Aplica Fortalecido em si próprio".
 */
export const targetNamesEm:Record<Target,string>={
  enemyWeak:'no inimigo mais ferido',enemyStrong:'no inimigo mais forte',
  enemyCast:'no inimigo que está preparando uma habilidade',
  investigated:'no inimigo mais investigado',allyWeak:'no aliado mais ferido',
  self:'em si próprio',allEnemies:'em todos os inimigos',allAllies:'em todo o trio',
  randomEnemy:'em um inimigo sorteado',
};
/*
 * O alvo dito pelo que ele é, não por uma metáfora.
 *
 * "inimigo mais fácil de derrubar" soa a julgamento e não explica nada: fácil
 * por quê? Pouca Vida? Pouca Armadura? Pouco poder? A regra do motor é uma só
 * — `enemyWeak` pontua `(1 - Vida restante / Vida máxima)`, quer dizer, prefere
 * quem está mais ferido. Então é isso que a ficha diz.
 *
 * "maior ameaça" era pior, porque estava errado. O motor soma ameaça em
 * **todo** alvo inimigo; o que distingue `enemyStrong` é o poder do
 * personagem. Quem lia "maior ameaça" esperava que a habilidade perseguisse
 * quem estivesse prestes a agir, e ela persegue o mais forte.
 */
export const targetNames:Record<Target,string>={
  enemyWeak:'inimigo mais ferido',enemyStrong:'inimigo mais forte',
  enemyCast:'inimigo preparando uma habilidade',
  investigated:'inimigo mais investigado',allyWeak:'aliado mais ferido',
  self:'o próprio personagem',allEnemies:'todos os inimigos',allAllies:'todo o trio',
  randomEnemy:'um inimigo sorteado',
};
export const topicNames:Record<Topic,string>={
  time:'por segundo',action:'ao atacar',dealt:'a cada 100 de dano causado',received:'a cada 100 de dano recebido',
  allyHurt:'a cada 100 de dano sofrido por um aliado',enemyHurt:'a cada 100 de dano sofrido por um inimigo',
  interrupt:'ao interromper um Preparo',status:'quando seu trio aplica qualquer Status',
  negativeStatus:'quando seu trio aplica um Status negativo em um inimigo',
  protected:'a cada 100 de dano bloqueado',enemyCast:'quando um inimigo começa o Preparo',
  survived:'por segundo enquanto estiver na luta',losing:'por segundo enquanto seu trio estiver atrás na Vantagem',
  winning:'por segundo enquanto seu trio estiver à frente na Vantagem',
};
/* Derivado de `statuses`, nunca repetido: ver a nota de tom em data/statuses.ts. */
export const positiveStatuses=new Set<StatusId>((Object.keys(statuses) as StatusId[]).filter(id=>statuses[id].tone==='positivo'));
export interface StatusPresentation {name:string;tone:'positivo'|'negativo';summary:string;value:string;
  /** Vazio quando o Status apenas renova; descreve o acúmulo quando ele soma. */
  accumulation:string}

/*
 * Cinco dos quatorze Status **somam** em vez de renovar, e a ficha não dizia.
 *
 * O caso que denunciou foi o Fortalecido. A ficha mostrava "Causa +3% de dano",
 * que lê como o efeito inteiro — e a conclusão natural de quem lê é que o buff
 * é fraco. Medido no combate, o He-Man chega a +68% de dano numa luta, porque
 * cada aplicação soma até o teto de +80%.
 *
 * O número nunca esteve errado. O que faltava era dizer que ele é **por
 * aplicação** e até onde vai.
 */
const acumulacaoDe=(id:StatusId):string=>{
  const def=statuses[id];
  if(def.stack!=='add')return '';
  if(id==='regen')return `soma a cada aplicação, até ${n(def.cap)} de Vida por segundo`;
  if(id==='burning')return `soma a cada aplicação, até ${n(def.cap)} de Vida por segundo`;
  return `soma a cada aplicação, até ${pct(def.cap)}`;
};

export function presentStatus(id:StatusId,value:number):StatusPresentation {
  const amount=Math.min(value,statuses[id].cap),percent=pct(amount),number=n(amount);
  const summary:Record<StatusId,string>={
    exposed:`Recebe +${percent} de dano`,marked:`Recebe +${percent} de dano e vira alvo preferencial`,
    slow:`Ataca e prepara habilidades ${percent} mais devagar`,rooted:`Ataca e prepara habilidades ${percent} mais devagar; acumula separadamente com Lento`,
    electric:`Recebe +${percent} de dano`,paralyzed:'Não ataca nem avança o Preparo',
    protected:`Recebe ${percent} menos dano${amount>=.3?'; Preparo não pode ser interrompido':''}`,
    haste:`Ataca e prepara habilidades ${percent} mais rápido`,confused:'25% de chance do ataque básico atingir a si mesmo',
    regen:`Recupera ${number} de Vida por segundo`,burning:`Perde ${number} de Vida por segundo`,
    silenced:'Não começa novas habilidades',strengthened:`Causa +${percent} de dano`,weakened:`Causa ${percent} menos dano`,
  };
  return {name:statuses[id].name,tone:positiveStatuses.has(id)?'positivo':'negativo',summary:summary[id],
    value:['regen','burning'].includes(id)?number:percent,accumulation:acumulacaoDe(id)};
}
export interface SkillPresentation {summary:string;target:string;effects:string[];charge:string[];useWhen:string;preparation:string;cooldown:string;
  /*
   * Se a linha "Alvo" ainda tem o que dizer.
   *
   * Quando toda linha de efeito já nomeia em quem ela cai — "181 de dano → o
   * inimigo mais ferido", "Aplica Fortalecido em si próprio" — a linha "Alvo"
   * logo abaixo repete, e numa habilidade de alvos mistos chega a contradizer:
   * a ficha da Sakura mostrava dano num inimigo e, embaixo, "Alvo: o próprio
   * personagem". Quem lê rápido conclui que a habilidade inteira é nela.
   */
  mostrarAlvo:boolean}
export interface TraitPresentation {summary:string;trigger:string;frequency:string;effects:string[]}
/*
 * `sempre` liga quando a habilidade tem alvos misturados.
 *
 * Normalmente uma linha só nomeia o alvo quando ele difere do alvo da
 * habilidade — o resto fica para a linha "Alvo", embaixo. Isso quebra quando a
 * mesma habilidade acerta lados diferentes: o Byakugou da Sakura dava
 * "306 de dano → inimigo mais ferido" e "+130 de Vida" sem alvo, com "Alvo:
 * todo o trio" no rodapé, e cabia ao jogador deduzir que o rodapé valia para a
 * cura e não para o dano. Com alvos misturados, cada linha diz o seu.
 */
export function presentEffect(effect:Effect,defaultTarget:Target,sempre=false):string {
  const alvoReal=effect.target??defaultTarget;
  const target=sempre||(effect.target&&effect.target!==defaultTarget)?` → ${targetNames[alvoReal]}`:'';
  switch(effect.kind){
    case 'damage':return `${n(effect.value)} de dano${target}`;
    case 'heal':return `+${n(effect.value)} de Vida${target}`;
    case 'shield':return `+${n(effect.value)} Escudo por até 10 s${target}`;
    /*
     * "Aplica <Status>", sempre.
     *
     * A regra está escrita por extenso no documento da direção: *"Não deixar
     * 'Lento' solto como se fosse ataque."* Era exatamente o que acontecia — a
     * ficha abria com o nome do Status, e quem lê rápido entende que a
     * habilidade **é** aquilo, não que ela aplica aquilo.
     *
     * A ordem segue a regra: ação → resultado → acúmulo → duração → alvo.
     */
    case 'status':{
      const p=presentStatus(effect.status,effect.value);
      const acumula=p.accumulation?` · ${p.accumulation}`:'';
      /*
       * Em quem, sempre — e junto do verbo.
       *
       * O alvo só aparecia quando era **diferente** do alvo da habilidade, o
       * que significa que ele sumia justamente nos casos mais comuns: um buff
       * que o personagem põe em si mesmo não dizia em quem. E quando aparecia,
       * vinha no fim da linha, depois da duração, longe do verbo que o rege.
       *
       * Um buff e um debuff só se distinguem por em quem caem. Essa é a
       * informação que não pode faltar.
       */
      const emQuem=targetNamesEm[effect.target??defaultTarget];
      return `Aplica ${statuses[effect.status].name} ${emQuem} · ${p.summary}${acumula} · ${secs(effect.duration)}`;
    }
    case 'interrupt':return effect.mode==='cancel'?`Interrompe o Preparo${target}`:effect.mode==='delay'?`Atrasa o Preparo em ${secs(effect.value)}${target}`:`Reduz ${pct(effect.value)} do Preparo${target}`;
    case 'shift':return `${effect.value>=0?'Adianta':'Atrasa'} ${pct(Math.abs(effect.value))} do próximo ataque${target}`;
    case 'investigate':return `+${n(effect.value)} Investigação${target}`;
    case 'deathnote':return 'Com 100 Investigação: elimina o alvo vulnerável; contra imune, 110 de dano e Exposto +55% por 14 s';
    case 'charge':return `+${n(effect.value)}% de Carga para habilidades${target}`;
    case 'store':return `Guarda ${n(effect.value)} de energia (até ${n(effect.cap)})`;
    case 'release':return `Libera energia guardada ×${n(effect.multiplier)} como dano, dividido entre inimigos vivos`;
  }
}
export function presentSkill(skill:Skill):SkillPresentation {
  const seExplicaSozinho=new Set<Effect['kind']>(['store','release','deathnote']);
  /* Alvos misturados: mais de um destino entre os efeitos da mesma habilidade. */
  const misto=new Set(skill.effects.map(e=>e.target??skill.target)).size>1;
  const effects=skill.effects.map(effect=>presentEffect(effect,skill.target,misto&&effect.kind!=='status'&&!seExplicaSozinho.has(effect.kind)));
  const use:Record<Skill['condition'],string>={
    /*
     * Sem repetir o alvo.
     *
     * A ficha mostra "Alvo" e "Usa quando" uma embaixo da outra, e isto dizia
     * "Alvo: inimigo mais ferido · Usa quando: ficar pronta, contra inimigo
     * mais ferido". A mesma informação, duas vezes, em duas linhas vizinhas. A
     * linha do Alvo já respondeu contra quem.
     */
    always:'ficar pronta',
    injured:'o alvo estiver com menos de 78% de Vida',
    enemyCast:'um inimigo estiver preparando uma habilidade',
    threatened:'um aliado tiver menos de 85% de Vida ou um inimigo começar o Preparo',
    investigated:'houver um alvo conhecido com 100 Investigação',
    vulnerable:'um inimigo estiver vulnerável ou sob controle',
    storedEnergy:'houver energia guardada',
  };
  /*
   * Um efeito "se apresenta" quando a própria linha dele já diz o alvo: todo
   * Status diz desde a FASE E, e os demais dizem quando miram algo diferente
   * do alvo da habilidade. Se todos se apresentam, "Alvo" vira eco.
   */
  /*
   * `store`, `release` e `deathnote` nunca precisam da linha "Alvo": guardar
   * energia só pode ser consigo mesmo, e as outras duas já nomeiam quem recebe
   * dentro da própria frase ("dividido entre inimigos vivos", "o alvo
   * vulnerável").
   */
  const seExplica=seExplicaSozinho;
  const seApresenta=(e:Effect)=>e.kind==='status'||seExplica.has(e.kind)||misto||(e.target!==undefined&&e.target!==skill.target);
  return {summary:effects[0]??'Sem efeito',target:targetNames[skill.target],effects,
    mostrarAlvo:skill.effects.length===0||!skill.effects.every(seApresenta),
    charge:cargasLegiveis(skill.charge),useWhen:use[skill.condition],
    preparation:skill.preparation>0?secs(skill.preparation):'instantâneo',cooldown:secs(skill.cooldown)};
}
export function presentTrait(trait:Trait):TraitPresentation {
  const effects=trait.effects.map(effect=>presentEffect(effect,trait.target));
  return {summary:effects[0]??'Sem efeito',trigger:topicNames[trait.on],frequency:trait.cooldown>0?`Resfriamento ${secs(trait.cooldown)}`:'Sem resfriamento',effects};
}
/*
 * Agregar fontes iguais de Carga, e pôr o gotejamento por último.
 *
 * Dois defeitos de leitura. O primeiro: o motor dispara `time` e `survived` no
 * mesmo passo, sem condição nenhuma — são a mesma fonte. Mas a ficha mostrava
 * "+3% por segundo enquanto estiver na luta; +2,5% por segundo": duas linhas
 * para uma coisa, e a primeira sugerindo uma condição que não existe (estar na
 * luta não é condição, é o estado normal). Agora soma: "+5,5% por segundo".
 *
 * O segundo: em 166 habilidades o "+2% por segundo" vinha antes da fonte que
 * caracteriza a habilidade. Quem compara duas fichas lia o gotejamento primeiro
 * toda vez. Ele vai para o fim; o que define a habilidade vem na frente.
 */
const topicoVisivel=(t:Topic):Topic=>t==='survived'?'time':t;
const ordemDaFonte=(t:Topic):number=>t==='time'||t==='survived'?2:t==='losing'||t==='winning'?1:0;
export function cargasLegiveis(rules:Skill['charge']):string[]{
  const somadas=new Map<Topic,number>();
  for(const r of rules){const chave=topicoVisivel(r.on);somadas.set(chave,(somadas.get(chave)??0)+r.amount);}
  return [...somadas].sort((a,b)=>ordemDaFonte(a[0])-ordemDaFonte(b[0])).map(([t,soma])=>`+${n(soma)}% ${topicNames[t]}`);
}
export function describeCharge(rules:Skill['charge']):string{return cargasLegiveis(rules).join('; ')||'Sem Carga';}
export function describeEffects(effects:Effect[],target:Target):string[]{return effects.map(effect=>presentEffect(effect,target));}
export function describeSkill(skill:Skill):string{return `${targetNames[skill.target]}: ${presentSkill(skill).effects.join('; ')}`;}
export function describeSkillUse(skill:Skill):string{const p=presentSkill(skill);return `Carga: ${p.charge.join('; ')}. Usa quando: ${p.useWhen}. Preparo: ${p.preparation}. Resfriamento: ${p.cooldown}.`;}
export function describeTrait(trait:Trait):string{const p=presentTrait(trait);return `${p.effects.join('; ')}. Ativa ${p.trigger}. ${p.frequency}.`;}
