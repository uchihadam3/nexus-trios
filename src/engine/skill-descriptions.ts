import { CHOQUE_DO_ELETRIFICADO, statuses } from '../data/statuses';
import { textoDoFerido } from './ferido';
import type { Effect, JeitoDeBater, Skill, Target, Topic, Trait, StatusId } from './types';
import { LOCALE, t, tx } from '../i18n/idioma';

const n=(v:number)=>Number(v.toFixed(1)).toLocaleString(LOCALE);
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
  enemyWeak:tx('no rival mais ferido'),enemyStrong:tx('no rival mais forte'),
  /*
   * "Preparo" é a palavra que o jogo já ensina — está na ficha de toda
   * habilidade, no anel dourado da batalha e no guia. Como cabeçalho, "no
   * inimigo que está preparando uma habilidade" quebrava em duas linhas no
   * celular para dizer a mesma coisa.
   */
  enemyCast:tx('no rival em Preparo'),
  investigated:tx('no rival mais investigado'),allyWeak:tx('no aliado mais ferido'),allyFallen:tx('no aliado caído'),
  self:tx('em si próprio'),allEnemies:tx('em todos os rivais'),allAllies:tx('em todo o trio'),
  randomEnemy:tx('em um rival aleatório'),leastInvestigated:tx('no rival menos investigado'),allyStrongest:tx('no aliado com mais Vida'),
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
  enemyWeak:tx('rival mais ferido'),enemyStrong:tx('rival mais forte'),
  enemyCast:tx('rival em Preparo'),
  investigated:tx('rival mais investigado'),allyWeak:tx('aliado mais ferido'),allyFallen:tx('aliado caído'),
  self:tx('o próprio personagem'),allEnemies:tx('todos os rivais'),allAllies:tx('todo o trio'),
  randomEnemy:tx('um rival aleatório'),leastInvestigated:tx('rival menos investigado'),allyStrongest:tx('aliado com mais Vida'),
};
export const topicNames:Record<Topic,string>={
  time:tx('por segundo'),action:tx('ao atacar'),dealt:tx('a cada 100 de dano causado'),received:tx('a cada 100 de dano recebido'),
  allyHurt:tx('a cada 100 de dano sofrido por um aliado'),enemyHurt:tx('a cada 100 de dano sofrido por um rival'),
  interrupt:tx('ao interromper um Preparo'),status:tx('quando seu trio aplica qualquer Status'),
  negativeStatus:tx('quando seu trio aplica um Status negativo em um rival'),
  protected:tx('a cada 100 de dano bloqueado'),enemyCast:tx('quando um rival começa o Preparo'),
  survived:tx('por segundo enquanto estiver na luta'),losing:tx('por segundo enquanto seu trio estiver atrás na Vantagem'),
  winning:tx('por segundo enquanto seu trio estiver à frente na Vantagem'),
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
  if(id==='regen'||id==='burning')return t('soma por aplicação até {n} de Vida por segundo',{n:n(def.cap)});
  return t('soma por aplicação até {n}',{n:pct(def.cap)});
};

/*
 * O valor de um Status agora, já somado — o que o jogador vê ao tocar nele na
 * batalha. "Aplicou 10% de Exposto, outro aplicou mais 20%: tocando, tem que
 * aparecer 30%." Paralisado, Silenciado e Confuso não têm intensidade que
 * importe: ou estão, ou não estão.
 */
const SEM_VALOR=new Set<StatusId>(['paralyzed','confused','silenced','marked','provoked','sleep']);
const deVida=(id:StatusId)=>id==='regen'||id==='burning'||id==='poison';
/* Espinhos é um número fixo por golpe, não %. */
const porGolpe=(id:StatusId)=>id==='thorns';
/* Sangramento é Vida por ação; Barreira é quantos debuffs ela ainda anula. */
const porAcao=(id:StatusId)=>id==='bleed';
const deDano=(id:StatusId)=>id==='bomb'||id==='summon';
export function valorAtualDoStatus(id:StatusId,intensidade:number):string|null{
  if(SEM_VALOR.has(id))return null;
  const v=Math.min(intensidade,statuses[id].cap);
  if(id==='electric')return `−${Math.round(v*CHOQUE_DO_ELETRIFICADO*100)}%`; // o choque na barra de ação, não dano
  if(id==='barrier')return `${n(Math.round(v))}`;
  return deVida(id)?t('{n} de Vida/s',{n:n(v)}):porGolpe(id)?t('{n} por golpe',{n:n(v)}):porAcao(id)?t('{n} por ação',{n:n(v)}):deDano(id)?t('{n} de dano',{n:n(v)}):pct(v);
}
/* Até onde as aplicações somam — só para os Status que somam. */
export function tetoDoStatus(id:StatusId):string|null{
  const def=statuses[id];
  if(def.stack!=='add')return null;
  if(id==='electric')return `−${Math.round(def.cap*CHOQUE_DO_ELETRIFICADO*100)}%`;
  if(id==='barrier')return `${n(def.cap)}`;
  return deVida(id)?t('{n} de Vida/s',{n:n(def.cap)}):porGolpe(id)?t('{n} por golpe',{n:n(def.cap)}):porAcao(id)?t('{n} por ação',{n:n(def.cap)}):deDano(id)?t('{n} de dano',{n:n(def.cap)}):pct(def.cap);
}

export function presentStatus(id:StatusId,value:number):StatusPresentation {
  const amount=Math.min(value,statuses[id].cap),percent=pct(amount),number=n(amount);
  const summary:Record<StatusId,string>={
    exposed:t('Recebe +{p} de dano',{p:percent}),
    /* Marcado não aumenta dano (isso é o Exposto): os rivais miram nele e os golpes atravessam o Escudo. */
    marked:t('Vira alvo preferencial dos rivais: o trio inteiro foca nele'),
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
    slow:t('{p} mais lento para agir',{p:percent}),rooted:t('{p} mais lento para agir · vale junto com Lento',{p:percent}),
    /* Eletrificado não aumenta dano (isso é o Exposto): é o choque que atrasa a ação a cada golpe. */
    electric:t('Cada golpe recebido atrasa {p} da próxima ação',{p:`${Math.round(amount*CHOQUE_DO_ELETRIFICADO*100)}%`}),paralyzed:t('Não ataca nem avança o Preparo'),
    protected:t('Recebe {p} menos dano',{p:percent})+(amount>=.3?t('; Preparo não pode ser interrompido'):''),
    haste:t('{p} mais rápido para agir',{p:percent}),confused:t('25% de chance do ataque básico atingir a si mesmo'),
    regen:t('Recupera {n} de Vida por segundo',{n:number}),burning:t('Perde {n} de Vida por segundo',{n:number}),
    silenced:t('Não começa novas habilidades'),strengthened:t('+{p} de dano',{p:percent}),weakened:t('−{p} de dano',{p:percent}),
    provoked:t('Só mira em quem provocou'),
    vampirism:t('Cura {p} do dano que causa',{p:percent}),reflect:t('Devolve {p} do dano recebido a quem bateu',{p:percent}),
    thorns:t('Quem bate leva {n} de dano por golpe',{n:number}),
    poison:t('Perde {n} de Vida por segundo, passando por Escudo e Protegido',{n:number}),bleed:t('Perde {n} de Vida a cada ação',{n:number}),
    cursed:t('Recebe {p} menos cura e Escudo',{p:percent}),frozen:t('Não age; o próximo golpe quebra o gelo com +{p} de dano',{p:percent}),
    sleep:t('Não age até acordar; qualquer golpe acorda'),blind:t('{p} de chance de errar o ataque básico',{p:percent}),
    barrier:amount>=2?t('Anula os próximos {n} debuffs',{n:number}):t('Anula o próximo debuff'),
    evasion:t('{p} de chance de escapar de cada golpe de rival',{p:percent}),
    bomb:t('Explode quando o tempo acaba: {n} de dano',{n:number}),
    summon:t('Uma criatura ataca um rival a cada 1,5 s: {n} de dano por ataque',{n:number}),
  };
  return {name:t(statuses[id].name),tone:positiveStatuses.has(id)?'positivo':'negativo',summary:summary[id],
    value:['regen','burning','thorns','poison','bleed','barrier','bomb','summon'].includes(id)?number:percent,accumulation:acumulacaoDe(id)};
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
const seExplicaSozinho=new Set<Effect['kind']>(['store','release','deathnote','revive','lifesteal','copy']);
const maiuscula=(x:string):string=>x.charAt(0).toUpperCase()+x.slice(1);

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
    exposed:t('+{v} de dano recebido',{v}),electric:t('−{v} da barra por golpe',{v:`${Math.round(value*CHOQUE_DO_ELETRIFICADO*100)}%`}),
    protected:t('−{v} de dano recebido',{v}),slow:t('{v} mais lento',{v}),rooted:t('{v} mais lento',{v}),haste:t('{v} mais rápido',{v}),
    regen:t('+{v} Vida/s',{v}),burning:t('−{v} Vida/s',{v}),strengthened:t('+{v} de dano',{v}),weakened:t('−{v} de dano',{v}),
    vampirism:t('{v} do dano',{v}),reflect:t('{v} do dano',{v}),thorns:t('{v} de dano por golpe',{v}),
    poison:t('−{v} Vida/s',{v}),bleed:t('−{v} Vida por ação',{v}),cursed:t('−{v} de cura recebida',{v}),frozen:t('+{v} no golpe que quebra',{v}),
    blind:t('{v} de chance',{v}),bomb:t('{v} de dano',{v}),summon:t('{v} de dano por ataque',{v}),evasion:t('{v} de chance',{v}),barrier:value>=2?t('anula {v} debuffs',{v}):t('anula {v} debuff',{v}),
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
  return [t('Aplica {status}',{status:t(statuses[effect.status].name)}),...valorCurto(effect.status,effect.value),secs(effect.duration)];
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
  const grupos=ordem.map(alvo=>({titulo:maiuscula(t(targetNamesEm[alvo])),linhas:porAlvo.get(alvo)!}));
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
  const target=modo==='agrupado'?'':modo==='sempre'||(effect.target&&effect.target!==defaultTarget)?` → ${t(targetNames[alvoReal])}`:'';
  switch(effect.kind){
    case 'damage':return t('{n} de dano',{n:n(effect.value)})+target;
    case 'heal':return t('+{n} de Vida',{n:n(effect.value)})+target;
    case 'shield':return t('+{n} Escudo',{n:n(effect.value)})+target;
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
      // Invocação não é algo que "se aplica": a criatura chega e luta junto
      if(effect.status==='summon')return [t('Invoca {quem}',{quem:effect.rotulo?t(effect.rotulo):t('uma criatura')}),...valorCurto(effect.status,effect.value),secs(effect.duration)].join(' · ');
      if(modo==='agrupado')return [t('Aplica {status}',{status:t(statuses[effect.status].name)}),...valorCurto(effect.status,effect.value),secs(effect.duration)].join(' · ');
      const emQuem=t(targetNamesEm[effect.target??defaultTarget]);
      return [t('Aplica {status} {emQuem}',{status:t(statuses[effect.status].name),emQuem}),...valorCurto(effect.status,effect.value),secs(effect.duration)].join(' · ');
    }
    case 'interrupt':return (effect.mode==='cancel'?t('Interrompe o Preparo'):effect.mode==='delay'?t('Atrasa o Preparo em {s}',{s:secs(effect.value)}):t('Reduz {p} do Preparo',{p:pct(effect.value)}))+target;
    case 'shift':return (effect.value>=0?t('Adianta {p} do próximo ataque',{p:pct(Math.abs(effect.value))}):t('Atrasa {p} do próximo ataque',{p:pct(Math.abs(effect.value))}))+target;
    case 'investigate':return t('+{n} Investigação',{n:n(effect.value)})+target;
    case 'revive':return t('Levanta um aliado caído com {p} da Vida máxima',{p:pct(effect.value)});
    case 'lifesteal':return t('Roubo de vida · {p} do dano',{p:pct(effect.value)});
    case 'cleanse':return (effect.value>1?t('Purifica até {n} debuffs',{n:n(effect.value)}):t('Purifica 1 debuff'))+target;
    case 'copy':return t('Na mesma hora, usa a última habilidade de um rival · {p} da força',{p:pct(effect.value)});
    case 'dispel':return (effect.value>1?t('Dissipa até {n} buffs',{n:n(effect.value)}):t('Dissipa 1 buff'))+target;
    case 'deathnote':return t('Com 100 Investigação: elimina o alvo; contra imune, 230 de dano, Exposto +55% por 14 s e recarga pela metade');
    case 'charge':return t('+{n}% de Carga para habilidades',{n:n(effect.value)})+target;
    case 'store':return t('Guarda {n} de energia (até {max})',{n:n(effect.value),max:n(effect.cap)});
    /*
     * A energia vai para os alvos da habilidade: num alvo só, inteira nele; em área, dividida entre os vivos
     * (pedido do jogador: "ela não divide, né? Ela só vai no inimigo mais forte. Por que tá escrito isso?").
     */
    case 'release':{
      const alvo=effect.target??defaultTarget;
      const area=alvo==='allEnemies';
      return t('Libera a energia guardada ×{m} como dano {onde}',{m:n(effect.multiplier),onde:area?t('dividido entre todos os rivais vivos'):t(targetNamesEm[alvo])});
    }
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
    always:tx('ficar pronta'),
    injured:tx('o alvo estiver com menos de 78% de Vida'), // a ficha usa textoDoFerido (de quem é a Vida)
    enemyCast:tx('um rival estiver preparando uma habilidade'),
    threatened:tx('um aliado tiver menos de 85% de Vida ou um rival começar o Preparo'),
    investigated:tx('houver um alvo conhecido com 100 Investigação'),
    // a lista dos Status que contam fica no termo clicável "vulnerável", não na ficha
    vulnerable:tx('um rival estiver vulnerável'),
    storedEnergy:tx('houver energia guardada'),
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
  // "alvo ferido" diz de quem é a Vida: o aliado que recebe a cura, ele mesmo ou o inimigo (engine/ferido.ts)
  // só levantar caídos (o Guia das almas do Anúbis): o motor espera alguém cair, então a ficha diz
  const soLevanta=skill.condition==='always'&&skill.effects.length>0&&skill.effects.every(e=>e.kind==='revive');
  const quando=soLevanta?t('um aliado tiver caído'):skill.condition==='injured'?textoDoFerido(skill):t(use[skill.condition]);
  return {summary:effects[0]??t('Sem efeito'),target:t(targetNames[skill.target]),effects,grupos,
    mostrarAlvo:!temCabecalho&&(skill.effects.length===0||!skill.effects.every(seApresenta)),
    charge:cargasLegiveis(skill.charge),useWhen:quando,
    ...(skill.condition!=='always'||soLevanta?{requisito:t('Só usa quando {quando}',{quando})}:{}),
    preparation:skill.preparation>0?secs(skill.preparation):t('instantâneo'),cooldown:secs(skill.cooldown)};
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
  action:tx('Ao atacar'),dealt:tx('Ao causar dano'),received:tx('Ao receber dano'),
  allyHurt:tx('Quando um aliado recebe dano'),enemyHurt:tx('Quando um rival recebe dano'),
  interrupt:tx('Ao interromper um Preparo'),status:tx('Quando seu trio aplica um Status'),
  negativeStatus:tx('Quando seu trio aplica um Status negativo em um rival'),
  protected:tx('Ao bloquear dano com Escudo ou Protegido'),enemyCast:tx('Quando um rival começa um Preparo'),
};
const PASSO_DO_MOTOR=.1;
const DANO_PROPORCIONAL=new Set<Topic>(['dealt','received','allyHurt','enemyHurt','protected']);
export function quandoAtiva(trait:Trait):{quando:string;limite:string}{
  const intervalo=secs(Math.max(trait.cooldown,PASSO_DO_MOTOR));
  if(trait.on==='time'||trait.on==='survived')return {quando:t('A cada {s}',{s:intervalo}),limite:''};
  if(trait.on==='winning')return {quando:t('A cada {s} enquanto seu trio está à frente na Vantagem',{s:intervalo}),limite:''};
  if(trait.on==='losing')return {quando:t('A cada {s} enquanto seu trio está atrás na Vantagem',{s:intervalo}),limite:''};
  const limite=trait.cooldown>=.5?t('no máximo 1 vez a cada {s}',{s:secs(trait.cooldown)}):'';
  const evento=QUANDO_EVENTO[trait.on],base=evento?t(evento):t('Ao {quando}',{quando:t(topicNames[trait.on])});
  return {quando:limite?`${base} · ${limite}`:base,limite};
}
/*
 * A condição do traço como condição de verdade (pedido do jogador: "coloca ativa quando, sublinhado, pra pessoa
 * entender"): o rótulo "Ativa quando" (ou "Ativa", nos de tempo) e o resto da frase, em minúscula.
 */
/*
 * Quem faz, sempre pelo nome (pedido do jogador: "Ativa quando ele recebe dano. Ele quem? … quando você recebe
 * dano? Não dá pra entender de quem é").
 */
const ATIVA_QUANDO=(nome:string):Partial<Record<Topic,string>>=>({
  action:t('{nome} ataca',{nome}),dealt:t('{nome} causa dano',{nome}),received:t('{nome} recebe dano',{nome}),
  allyHurt:t('um aliado de {nome} recebe dano',{nome}),enemyHurt:t('um rival recebe dano'),
  interrupt:t('{nome} interrompe um Preparo',{nome}),status:t('o trio de {nome} aplica um Status',{nome}),
  negativeStatus:t('o trio de {nome} aplica um Status negativo em um rival',{nome}),
  protected:t('{nome} bloqueia dano com Escudo ou Protegido',{nome}),enemyCast:t('um rival começa um Preparo'),
});
export function ativaQuando(trait:Trait,nome=t('o personagem')):{rotulo:string;resto:string}{
  const intervalo=secs(Math.max(trait.cooldown,PASSO_DO_MOTOR));
  if(trait.on==='time'||trait.on==='survived')return {rotulo:t('Ativa'),resto:t('a cada {s}',{s:intervalo})};
  if(trait.on==='winning')return {rotulo:t('Ativa quando'),resto:t('o trio de {nome} está à frente na Vantagem · a cada {s}',{nome,s:intervalo})};
  if(trait.on==='losing')return {rotulo:t('Ativa quando'),resto:t('o trio de {nome} está atrás na Vantagem · a cada {s}',{nome,s:intervalo})};
  const {limite}=quandoAtiva(trait);
  const base=ATIVA_QUANDO(nome)[trait.on]??t(topicNames[trait.on]).replace(/^(ao|quando|when|on) /i,'');
  return {rotulo:t('Ativa quando'),resto:limite?`${base} · ${limite}`:base};
}
/** Última resistência (na ficha, fora do traço): o golpe fatal o deixa de pé uma vez. */
export function textoDaResistencia(r:{protegido:number;duracao:number}):string{
  return t('Última resistência · Protegido {p} por {s} s',{p:pct(r.protegido),s:r.duracao});
}
/** Ninguém suspeita dele (na ficha, junto do traço): os rivais preferem outros alvos. */
export function textoDoDespercebido():string{
  return t('Ninguém suspeita dele · os rivais preferem outros alvos, menos quando ele está em Preparo');
}
/** Isca (na ficha, junto do traço): quem bate no aliado marcado por ele se entrega. */
export function textoDaIsca(i:{investiga:number}):string{
  return t('Isca · quem bate no aliado que ele marcou dá {n} de Investigação sobre si',{n:i.investiga});
}
/** O jeito de bater: o que o ataque básico faz além do golpe. */
export function textoDoJeito(j:JeitoDeBater):string{
  const x=(v:number)=>v.toLocaleString(LOCALE,{maximumFractionDigits:1});
  switch(j.tipo){
    case 'serie':{
      const partes=[(j.mult??1)>1?t('dano ×{m}',{m:x(j.mult!)}):'',j.status?presentEffect({kind:'status',status:j.status.status,value:j.status.value,duration:j.status.duration},'enemyWeak').replace(/^./,c=>c.toLowerCase()):''].filter(Boolean);
      return t('A cada {n} golpes: {nome}',{n:j.cada,nome:t(j.nome)})+(partes.length?` (${partes.join(t(' e '))})`:'');
    }
    case 'ricochete':return t('Quica no outro rival · {p} do dano',{p:pct(j.fracao)});
    case 'largo':return t('Pega também um segundo rival · {p} do dano',{p:pct(j.fracao)});
    case 'cura':return t('{p} do dano vira cura no aliado mais ferido',{p:pct(j.fracao)});
    case 'escudo':return t('{p} do dano vira Escudo em si',{p:pct(j.fracao)});
    case 'dreno':return t('Roubo de vida: {p} do dano volta como Vida',{p:pct(j.fracao)});
    case 'rouba':return t('Rouba {n} de Carga',{n:j.valor});
    case 'acelera':return t('Cada golpe adianta a próxima ação em {p}',{p:pct(j.valor)});
  }
}
/** Renascer (na ficha do personagem, fora do traço): o que acontece quando ele cai. */
export function textoDoRenascer(r:{vida:number;atraso:number}):string{
  return t('Renasce em {s} s com {p} da Vida',{s:r.atraso,p:pct(r.vida)});
}
export function presentTrait(trait:Trait):TraitPresentation {
  const effects=trait.effects.map(effect=>{
    const texto=presentEffect(effect,trait.target);
    // só a energia armazenada cresce com o tamanho do golpe; e diz de qual dano ("a cada 100 de dano recebido")
    return effect.kind==='store'&&DANO_PROPORCIONAL.has(trait.on)?`${texto}, ${t(topicNames[trait.on])}`:texto;
  });
  const {quando,limite}=quandoAtiva(trait);
  return {summary:effects[0]??t('Sem efeito'),quando,trigger:quando.charAt(0).toLowerCase()+quando.slice(1),frequency:limite,effects};
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
  return [...somadas].sort((a,b)=>ordemDaFonte(a[0])-ordemDaFonte(b[0])).map(([tp,soma])=>`+${n(soma)}% ${t(topicNames[tp])}`);
}
export function describeCharge(rules:Skill['charge']):string{return cargasLegiveis(rules).join('; ')||t('Sem Carga');}
export function describeEffects(effects:Effect[],target:Target):string[]{return effects.map(effect=>presentEffect(effect,target));}
export function describeSkill(skill:Skill):string{return `${targetNames[skill.target]}: ${presentSkill(skill).effects.join('; ')}`;}
export function describeSkillUse(skill:Skill):string{const p=presentSkill(skill);return `Carga: ${p.charge.join('; ')}. Usa quando: ${p.useWhen}. Preparo: ${p.preparation}. Resfriamento: ${p.cooldown}.`;}
export function describeTrait(trait:Trait):string{const p=presentTrait(trait);return `${p.effects.join('; ')}. ${p.quando}.`;}
