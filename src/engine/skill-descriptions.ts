import { CHOQUE_DO_ELETRIFICADO, statuses } from '../data/statuses';
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
  /*
   * "Preparo" é a palavra que o jogo já ensina — está na ficha de toda
   * habilidade, no anel dourado da batalha e no guia. Como cabeçalho, "no
   * inimigo que está preparando uma habilidade" quebrava em duas linhas no
   * celular para dizer a mesma coisa.
   */
  enemyCast:'no inimigo em Preparo',
  investigated:'no inimigo mais investigado',allyWeak:'no aliado mais ferido',allyFallen:'no aliado caído',
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
  enemyCast:'inimigo em Preparo',
  investigated:'inimigo mais investigado',allyWeak:'aliado mais ferido',allyFallen:'aliado caído',
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
  /*
   * "por aplicação" é a parte que não pode cair.
   *
   * "soma até 80%" lê como se o Status fosse até 80% e pronto. O que acontece
   * é que **cada** aplicação soma, e 80% é onde a soma para.
   */
  if(id==='regen'||id==='burning')return `soma por aplicação até ${n(def.cap)} de Vida por segundo`;
  return `soma por aplicação até ${pct(def.cap)}`;
};

/*
 * O valor de um Status agora, já somado — o que o jogador vê ao tocar nele na
 * batalha. "Aplicou 10% de Exposto, outro aplicou mais 20%: tocando, tem que
 * aparecer 30%." Paralisado, Silenciado e Confuso não têm intensidade que
 * importe: ou estão, ou não estão.
 */
const SEM_VALOR=new Set<StatusId>(['paralyzed','confused','silenced','marked','provoked']);
const deVida=(id:StatusId)=>id==='regen'||id==='burning';
/* Espinhos é um número fixo por golpe, não %. */
const porGolpe=(id:StatusId)=>id==='thorns';
export function valorAtualDoStatus(id:StatusId,intensidade:number):string|null{
  if(SEM_VALOR.has(id))return null;
  const v=Math.min(intensidade,statuses[id].cap);
  if(id==='electric')return `−${Math.round(v*CHOQUE_DO_ELETRIFICADO*100)}%`; // o choque na barra de ação, não dano
  return deVida(id)?`${n(v)} de Vida/s`:porGolpe(id)?`${n(v)} por golpe`:pct(v);
}
/* Até onde as aplicações somam — só para os Status que somam. */
export function tetoDoStatus(id:StatusId):string|null{
  const def=statuses[id];
  if(def.stack!=='add')return null;
  if(id==='electric')return `−${Math.round(def.cap*CHOQUE_DO_ELETRIFICADO*100)}%`;
  return deVida(id)?`${n(def.cap)} de Vida/s`:porGolpe(id)?`${n(def.cap)} por golpe`:pct(def.cap);
}

export function presentStatus(id:StatusId,value:number):StatusPresentation {
  const amount=Math.min(value,statuses[id].cap),percent=pct(amount),number=n(amount);
  const summary:Record<StatusId,string>={
    exposed:`Recebe +${percent} de dano`,
    /* Marcado não aumenta dano (isso é o Exposto): os rivais miram nele e os golpes atravessam o Escudo. */
    marked:'Vira alvo preferencial dos rivais, e os golpes nele atravessam o Escudo',
    /*
     * Lento, Preso e Acelerado: "7% mais lento para agir" — agir é dar o
     * próximo golpe e preparar habilidades, sem usar a palavra "ataque". Na ficha a
     * linha começa com "Aplica Lento", que já diz que a habilidade põe um
     * efeito no alvo — e não que ela própria ataca ou age.
     *
     * Duas redações caíram antes desta. "Ataca e prepara habilidades 7% mais
     * devagar", sem sujeito, lia como se a habilidade atacasse. "Ataque básico
     * e Preparo ficam 7% mais lentos" ainda tinha "ataque" e fazia a mesma
     * confusão numa habilidade sem dano nenhum. O que "mais lento" quer dizer
     * — o próximo golpe e o Preparo demoram mais — fica na legenda do Status.
     */
    slow:`${percent} mais lento para agir`,rooted:`${percent} mais lento para agir · vale junto com Lento`,
    /* Eletrificado não aumenta dano (isso é o Exposto): é o choque que atrasa a ação a cada golpe. */
    electric:`Cada golpe recebido atrasa ${Math.round(amount*CHOQUE_DO_ELETRIFICADO*100)}% da próxima ação`,paralyzed:'Não ataca nem avança o Preparo',
    protected:`Recebe ${percent} menos dano${amount>=.3?'; Preparo não pode ser interrompido':''}`,
    haste:`${percent} mais rápido para agir`,confused:'25% de chance do ataque básico atingir a si mesmo',
    regen:`Recupera ${number} de Vida por segundo`,burning:`Perde ${number} de Vida por segundo`,
    silenced:'Não começa novas habilidades',strengthened:`+${percent} de dano`,weakened:`−${percent} de dano`,
    provoked:'Só mira em quem provocou',
    vampirism:`Cura ${percent} do dano que causa`,reflect:`Devolve ${percent} do dano recebido a quem bateu`,
    thorns:`Quem bate leva ${number} de dano por golpe`,
  };
  return {name:statuses[id].name,tone:positiveStatuses.has(id)?'positivo':'negativo',summary:summary[id],
    value:['regen','burning','thorns'].includes(id)?number:percent,accumulation:acumulacaoDe(id)};
}
/*
 * Os efeitos de uma habilidade, reunidos por em quem caem.
 *
 * O que motivou isto foi medido, não achado: nos 250 personagens, 357 das 750
 * habilidades mostram 3 linhas ou mais, e **220 linhas repetem um alvo que a
 * própria ficha já tinha dito**. O Manto da Kurama dizia "em si próprio" duas
 * vezes e "Alvo: o próprio personagem" numa terceira, na mesma caixa.
 *
 * Dizer o alvo uma vez, como cabeçalho, resolve a repetição sem esconder nada
 * — e o que some é só o que estava sobrando.
 *
 * `titulo` vazio marca o grupo dos efeitos que se explicam sozinhos; ver
 * `agruparEfeitos`.
 */
export interface GrupoDeEfeitos {titulo:string;linhas:LinhaDeEfeito[]}

/*
 * Guardar energia, liberá-la e o Death Note não entram em grupo nenhum.
 *
 * Eles descrevem o alvo dentro da própria frase ("dividido entre inimigos
 * vivos", "elimina o alvo vulnerável"). Pior: `store` normalmente não declara
 * alvo, então herdaria o da habilidade — e um "Guarda 40 de energia" sob o
 * cabeçalho "No inimigo mais ferido" estaria simplesmente mentindo.
 */
const seExplicaSozinho=new Set<Effect['kind']>(['store','release','deathnote','revive','lifesteal']);
const maiuscula=(t:string):string=>t.charAt(0).toUpperCase()+t.slice(1);

/*
 * As peças de uma linha agrupada.
 *
 * Só o Status tem mais de uma: nome, o que faz, como acumula, quanto dura. O
 * resto é uma frase só, e fica assim.
 */
/*
 * Na ficha a linha do Status fica só com o nome, o número e o tempo:
 * "Aplica Fortalecido · +18% de dano · 7 s". O que o Status faz e como ele
 * soma estão no cartão que abre ao tocar no nome (src/presentation/glossario.ts).
 * Confuso, Paralisado e Silenciado não têm número: a linha é só o nome.
 */
export function valorCurto(id:StatusId,value:number):string[]{
  const v=presentStatus(id,value).value;
  const curto:Partial<Record<StatusId,string>>={
    exposed:`+${v} de dano recebido`,marked:'na mira · atravessa escudo',electric:`choque: −${Math.round(value*CHOQUE_DO_ELETRIFICADO*100)}% da barra por golpe`,
    protected:`−${v} de dano recebido`,slow:`${v} mais lento`,rooted:`${v} mais lento`,haste:`${v} mais rápido`,
    regen:`+${v} Vida/s`,burning:`−${v} Vida/s`,strengthened:`+${v} de dano`,weakened:`−${v} de dano`,
    vampirism:`cura ${v} do dano causado`,reflect:`devolve ${v} do dano`,thorns:`${v} de dano em quem bate`,
  };
  return curto[id]?[curto[id]!]:[];
}
export function partesDoEfeito(effect:Effect,defaultTarget:Target):string[]{
  if(effect.kind!=='status')return [presentEffect(effect,defaultTarget,'agrupado')];
  /*
   * "Aplica <Status>", como pediu o jogador e como o documento da direção
   * manda: sem o verbo, "Lento · 7% mais lento" lia como se a habilidade
   * fosse lenta. O alvo continua no cabeçalho do grupo, então não se repete.
   */
  return [`Aplica ${statuses[effect.status].name}`,...valorCurto(effect.status,effect.value),secs(effect.duration)];
}
const linhaDe=(effect:Effect,defaultTarget:Target):LinhaDeEfeito=>{
  const partes=partesDoEfeito(effect,defaultTarget);
  return {texto:partes.join(' · '),partes};
};

export function agruparEfeitos(effects:Effect[],defaultTarget:Target):GrupoDeEfeitos[]{
  const ordem:Target[]=[],porAlvo=new Map<Target,LinhaDeEfeito[]>(),sozinhos:LinhaDeEfeito[]=[];
  for(const effect of effects){
    if(seExplicaSozinho.has(effect.kind)){sozinhos.push(linhaDe(effect,defaultTarget));continue;}
    const alvo=effect.target??defaultTarget;
    if(!porAlvo.has(alvo)){porAlvo.set(alvo,[]);ordem.push(alvo);}
    porAlvo.get(alvo)!.push(linhaDe(effect,defaultTarget));
  }
  const grupos=ordem.map(alvo=>({titulo:maiuscula(targetNamesEm[alvo]),linhas:porAlvo.get(alvo)!}));
  return sozinhos.length>0?[...grupos,{titulo:'',linhas:sozinhos}]:grupos;
}

/*
 * Uma linha da ficha, quebrada nas suas peças.
 *
 * `texto` é a frase inteira — é o que os testes leem e o que serve a qualquer
 * lugar que só queira texto. `partes` é a mesma coisa separada, para a tela
 * poder dar peso diferente a cada pedaço: o nome do Status forte, o detalhe
 * normal, a duração discreta. Uma frase de 150 caracteres toda no mesmo tom é
 * o que fazia a ficha parecer um parágrafo de contrato.
 *
 * As duas nascem da mesma lista, então não existe o risco clássico de uma
 * concordar e a outra não.
 */
export interface LinhaDeEfeito {texto:string;partes:string[]}

export interface SkillPresentation {summary:string;target:string;effects:string[];grupos:GrupoDeEfeitos[];charge:string[];useWhen:string;
  /** A regra que a habilidade espera para sair, quando tem uma ("Só usa quando…"). */
  requisito?:string;preparation:string;cooldown:string;
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
export interface TraitPresentation {summary:string;
  /** A frase inteira de quando ativa: "A cada 2 s", "Ao receber dano · no máximo 1 vez a cada 3 s". */
  quando:string;
  /** A mesma frase, começando em minúscula (para "… · ativa …"). */
  trigger:string;
  /** O limite de frequência, quando existe (eventos); vazio nos traços de tempo. */
  frequency:string;effects:string[]}
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
/*
 * `modo` decide quem carrega o alvo: a linha ou o cabeçalho.
 *
 * - `auto`: a linha nomeia o alvo só quando ele difere do alvo da habilidade.
 * - `sempre`: a linha nomeia sempre (habilidade de alvos misturados, numa
 *   lista plana, onde o rodapé não dá conta).
 * - `agrupado`: a linha **nunca** nomeia, porque o cabeçalho do grupo já diz.
 */
export type ModoDeAlvo='auto'|'sempre'|'agrupado';
export function presentEffect(effect:Effect,defaultTarget:Target,modo:ModoDeAlvo='auto'):string {
  const alvoReal=effect.target??defaultTarget;
  const target=modo==='agrupado'?'':modo==='sempre'||(effect.target&&effect.target!==defaultTarget)?` → ${targetNames[alvoReal]}`:'';
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
      /*
       * Agrupada, a linha perde o verbo e o alvo e fica com o essencial:
       * "Exposto · Recebe +12% de dano · soma por aplicação até 65% · 5 s".
       *
       * Isso responde de lado uma dúvida que a forma antiga criava. Lendo
       * "Aplica Exposto ... Causa +5% de dano" numa habilidade e "+12%" em
       * outra, a leitura natural é que o Status tem um valor fixo e aquele
       * número é outra coisa. Com o número colado no nome do Status, fica
       * claro que **cada habilidade aplica a sua própria dose** — e o teto diz
       * até onde as doses somam.
       */
      /*
       * Na ficha agrupada a linha fica só com o nome, o número e o tempo:
       * "Aplica Fortalecido · +18% de dano · 7 s". O que o Status faz e como
       * ele soma estão no cartão que abre ao tocar no nome (glossário).
       */
      if(modo==='agrupado')return [`Aplica ${statuses[effect.status].name}`,...valorCurto(effect.status,effect.value),secs(effect.duration)].join(' · ');
      const emQuem=targetNamesEm[effect.target??defaultTarget];
      return [`Aplica ${statuses[effect.status].name} ${emQuem}`,...valorCurto(effect.status,effect.value),secs(effect.duration)].join(' · ');
    }
    case 'interrupt':return effect.mode==='cancel'?`Interrompe o Preparo${target}`:effect.mode==='delay'?`Atrasa o Preparo em ${secs(effect.value)}${target}`:`Reduz ${pct(effect.value)} do Preparo${target}`;
    case 'shift':return `${effect.value>=0?'Adianta':'Atrasa'} ${pct(Math.abs(effect.value))} do próximo ataque${target}`;
    case 'investigate':return `+${n(effect.value)} Investigação${target}`;
    case 'revive':return `Levanta um aliado caído com ${pct(effect.value)} da Vida · 1 vez por luta`;
    case 'lifesteal':return `Roubo de vida: recupera ${pct(effect.value)} do dano causado`;
    case 'cleanse':return `Purifica: tira ${effect.value>1?`até ${n(effect.value)} debuffs`:'1 debuff'}${target}`;
    case 'dispel':return `Dissipa: tira ${effect.value>1?`até ${n(effect.value)} buffs`:'1 buff'}${target}`;
    case 'deathnote':return 'Com 100 Investigação: elimina o alvo vulnerável; contra imune, 110 de dano e Exposto +55% por 14 s';
    case 'charge':return `+${n(effect.value)}% de Carga para habilidades${target}`;
    case 'store':return `Guarda ${n(effect.value)} de energia (até ${n(effect.cap)})`;
    case 'release':return `Libera energia guardada ×${n(effect.multiplier)} como dano, dividido entre inimigos vivos`;
  }
}
export function presentSkill(skill:Skill):SkillPresentation {
  /* Alvos misturados: mais de um destino entre os efeitos da mesma habilidade. */
  const misto=new Set(skill.effects.map(e=>e.target??skill.target)).size>1;
  const effects=skill.effects.map(effect=>presentEffect(effect,skill.target,
    misto&&effect.kind!=='status'&&!seExplicaSozinho.has(effect.kind)?'sempre':'auto'));
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
    vulnerable:'um inimigo estiver Exposto, Marcado, Paralisado, Eletrificado ou Queimando',
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
  const seApresenta=(e:Effect)=>e.kind==='status'||seExplicaSozinho.has(e.kind)||misto||(e.target!==undefined&&e.target!==skill.target);
  const grupos=agruparEfeitos(skill.effects,skill.target);
  /*
   * Com os grupos na tela, "Alvo" só tem o que dizer quando nenhum cabeçalho
   * apareceu: habilidade sem efeito, ou feita apenas de efeitos que se
   * explicam sozinhos. Fora disso, repetiria o primeiro cabeçalho.
   */
  const temCabecalho=grupos.some(g=>g.titulo!=='');
  return {summary:effects[0]??'Sem efeito',target:targetNames[skill.target],effects,grupos,
    mostrarAlvo:!temCabecalho&&(skill.effects.length===0||!skill.effects.every(seApresenta)),
    charge:cargasLegiveis(skill.charge),useWhen:use[skill.condition],
    ...(skill.condition!=='always'?{requisito:`Só usa quando ${use[skill.condition]}`}:{}),
    preparation:skill.preparation>0?secs(skill.preparation):'instantâneo',cooldown:secs(skill.cooldown)};
}
/*
 * Quando um traço ativa, dito do jeito que acontece no motor.
 *
 * O texto antigo juntava "Ativa por segundo · Resfriamento 2 s" — duas
 * informações para uma coisa só: um traço de tempo dispara e espera o
 * resfriamento, então ele simplesmente ativa a cada 2 s. E dizia "a cada 100 de
 * dano recebido" para traços que, no motor, ativam a cada golpe recebido de
 * qualquer tamanho (o valor do dano só pesa na energia armazenada). Agora:
 *
 * - tempo: "A cada 2 s" — o resfriamento é o próprio intervalo;
 * - à frente/atrás na Vantagem: "A cada 1 s enquanto seu trio está à frente";
 * - evento (golpe, Preparo, Status…): "Ao receber dano", e o resfriamento vira
 *   o limite que de fato importa — "no máximo 1 vez a cada 3 s" —, porque sem
 *   ele o traço ativaria a cada golpe.
 */
const QUANDO_EVENTO:Partial<Record<Topic,string>>={
  action:'Ao atacar',dealt:'Ao causar dano',received:'Ao receber dano',
  allyHurt:'Quando um aliado recebe dano',enemyHurt:'Quando um inimigo recebe dano',
  interrupt:'Ao interromper um Preparo',status:'Quando seu trio aplica um Status',
  negativeStatus:'Quando seu trio aplica um Status negativo em um inimigo',
  protected:'Quando o Escudo ou a Proteção dele bloqueia dano',enemyCast:'Quando um inimigo começa um Preparo',
};
const PASSO_DO_MOTOR=.1;
const DANO_PROPORCIONAL=new Set<Topic>(['dealt','received','allyHurt','enemyHurt','protected']);
export function quandoAtiva(trait:Trait):{quando:string;limite:string}{
  const intervalo=secs(Math.max(trait.cooldown,PASSO_DO_MOTOR));
  if(trait.on==='time'||trait.on==='survived')return {quando:`A cada ${intervalo}`,limite:''};
  if(trait.on==='winning')return {quando:`A cada ${intervalo} enquanto seu trio está à frente na Vantagem`,limite:''};
  if(trait.on==='losing')return {quando:`A cada ${intervalo} enquanto seu trio está atrás na Vantagem`,limite:''};
  const limite=trait.cooldown>=.5?`no máximo 1 vez a cada ${secs(trait.cooldown)}`:'';
  const base=QUANDO_EVENTO[trait.on]??`Ao ${topicNames[trait.on]}`;
  return {quando:limite?`${base} · ${limite}`:base,limite};
}
/** Renascer (na ficha do personagem, fora do traço): o que acontece quando ele cai. */
export function textoDoRenascer(r:{vida:number;atraso:number}):string{
  return `Renasce: ao cair, volta em ${r.atraso.toLocaleString('pt-BR')} s com ${pct(r.vida)} da Vida · 1 vez por luta`;
}
export function presentTrait(trait:Trait):TraitPresentation {
  const effects=trait.effects.map(effect=>{
    const texto=presentEffect(effect,trait.target);
    // só a energia armazenada cresce com o tamanho do golpe
    return effect.kind==='store'&&DANO_PROPORCIONAL.has(trait.on)?`${texto}, a cada 100 de dano`:texto;
  });
  const {quando,limite}=quandoAtiva(trait);
  return {summary:effects[0]??'Sem efeito',quando,trigger:quando.charAt(0).toLowerCase()+quando.slice(1),frequency:limite,effects};
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
export function describeTrait(trait:Trait):string{const p=presentTrait(trait);return `${p.effects.join('; ')}. ${p.quando}.`;}
