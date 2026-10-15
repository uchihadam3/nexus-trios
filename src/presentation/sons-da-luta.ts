import type { BattleEvent } from '../engine/types';
import { PRIORIDADE, type Sound } from '../audio/cues';
import { battleAudio } from '../lib/audio';
import { efeitoDaUnica } from './unicas-efeitos';
import { rajadaDaChave } from './rajada-da-unica';
import { ESFERA_QUE_CRESCE, estagiosDaEsfera } from './esfera-que-cresce';
import { entregasDeApoio } from './entrega-de-apoio';
import { duracaoBase, type Cue, type Direction } from './director';
import { fasesDoEvento } from './ativacao-da-unica';
import { preparoDaUnica } from './preparo-da-unica';
import { PRESENTATION as P } from './config';
import { FAMILIA_DA_INVOCACAO } from './vfx-atribuicao';
import { efeitosDoJeito, somDoJeito } from './jeito-efeito';
import { SOM_DA_ESPERA, SOM_DA_VOLTA, SOM_DO_REVIVER } from './renascer-proprio';

/*
 * Os sons de uma luta, quadro a quadro (tirado de dentro do laço da batalha em src/App.tsx para a arena do PvP tocar
 * exatamente o mesmo que a jornada): o som de cada golpe no impacto (somDoCue) e, depois de cada quadro, o clima da
 * música, os passos da cadeia, a Mecânica única, as entregas de apoio e o "pronto" (sonsDoQuadro).
 */
type Ref<T> = { current: T };
export interface EstadoDosSons {
  lastAudio: Ref<number>; lastDominionSound: Ref<number>; passoTocado: Ref<{ beat: number; passo: number }>;
  unicaTocada: Ref<number | null>; apoioTocado: Ref<number | null>; pausasTocadas: Ref<Set<string>>;
}
export const estadoDosSons = (): EstadoDosSons => ({ lastAudio: { current: 0 }, lastDominionSound: { current: 0 }, passoTocado: { current: { beat: -1, passo: 1 } }, unicaTocada: { current: null }, apoioTocado: { current: null }, pausasTocadas: { current: new Set() } });

/** O som de um momento do golpe (início, golpe, impacto). */
export function somDoCue(d: Direction, cue: Cue): void {
  if(cue.phase==='impact'&&d.active){
    // levantar/renascer: o som próprio por cima do golpe do beat
    const volta=d.active.events.find(e=>e.kind==='revive');
    const quemVolta=volta?d.active.after.fighters.find(f=>f.uid===volta.source)?.characterId??'':'';
    if(volta)battleAudio.sound(volta.source===volta.target?SOM_DA_VOLTA(quemVolta):SOM_DO_REVIVER(quemVolta) as Sound,PRIORIDADE.importante,0,volta.id,volta.source===volta.target?0:.12);
    if(volta&&d.active.event.kind==='revive')return;
    // caiu, mas vai renascer: as brasas começam a crepitar logo depois do nocaute
    const brasa=d.active.events.find(e=>e.kind==='ko'&&(d.active!.after.fighters.find(f=>f.uid===e.target)?.renascendo??0)>0);
    if(brasa)battleAudio.sound(SOM_DA_ESPERA(d.active.after.fighters.find(f=>f.uid===brasa.target)?.characterId??''),PRIORIDADE.apoio,0,brasa.id,.45);
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
}

/** Os sons depois de cada quadro: o clima da música e tudo que soa fora do impacto. */
export function sonsDoQuadro(d: Direction, s: EstadoDosSons, mudo: boolean): void {
  const { lastAudio, lastDominionSound, passoTocado, unicaTocada, apoioTocado, pausasTocadas } = s;
  const fighters=d.visible.fighters,critical=fighters.filter(f=>f.hp>0&&f.hp/f.maxHp<.34).length,casts=fighters.filter(f=>f.hp>0&&f.cast).length;
  battleAudio.setMood({heat:Math.min(1,.15+critical*.13+casts*.17+Math.abs(d.visible.dominion)/150),pressure:d.visible.dominion/100,time:Math.min(1,d.visible.time/120)});
  if(Math.abs(d.visible.dominion-lastDominionSound.current)>=20){if(!mudo)battleAudio.sound('toque',PRIORIDADE.interface);lastDominionSound.current=d.visible.dominion;}
  // cada passo da cadeia (depois do golpe) tem o seu som: reação, debuff, buff, cura, escudo
  const ativo=d.active;
  // a Mecânica única ativando sozinha: o som dela sai junto do efeito, logo depois do nome (não espera o impacto)
  if(ativo?.traco&&ativo.passos?.[0]?.classe==='unica'&&unicaTocada.current!==ativo.event.id&&!mudo){
    unicaTocada.current=ativo.event.id;
    const dono=ativo.after.fighters.find(f=>f.uid===ativo.event.source);
    // o preparo soa como o de uma habilidade (o som de carregar do personagem) e o efeito dela sai no fim dele
    const fases=fasesDoEvento(ativo.event,ativo.after,ativo),esfera=dono?ESFERA_QUE_CRESCE[dono.characterId]:undefined;
    // a esfera que cresce (a Genki Dama): um som por estágio e o do arremesso, no lugar do som de carregar
    if(esfera){estagiosDaEsfera(esfera,fases).forEach((t,k)=>battleAudio.sound(esfera.sons[k] as Sound,PRIORIDADE.habilidade,0,ativo.event.id*10+6+k*1000,t));battleAudio.sound(esfera.lanca as Sound,PRIORIDADE.habilidade,0,ativo.event.id*10+5,fases.soltaEm);}
    else if(dono)battleAudio.sound(preparoDaUnica(dono.characterId).som,PRIORIDADE.habilidade,0,ativo.event.id*10+6);
    // a explosão da Genki Dama tem 0,85 s de ronco antes do estrondo: o estrondo cai na chegada da esfera
    if(dono)battleAudio.sound(efeitoDaUnica(dono.characterId,ativo.event.label).som as Sound,PRIORIDADE.habilidade,0,ativo.event.id*10+7,esfera?Math.max(0,fases.efeitoEm-.85):fases.soltaEm);
  }
  // a esfera do apoio saindo para o aliado (src/presentation/entrega-de-apoio.ts): o som sai junto com ela
  if(ativo&&apoioTocado.current!==ativo.event.id&&!mudo){
    const entregas=entregasDeApoio(ativo);
    if(entregas.length){
      apoioTocado.current=ativo.event.id;
      const agora=ativo.elapsed-duracaoBase(ativo)*P.impactAt;
      entregas.forEach((x,k)=>battleAudio.sound('apoio-sai',PRIORIDADE.apoio,0,ativo.event.id*10+3+k*1000,Math.max(0,x.sai-agora)));
    }
  }
  // cada pausa do golpe (alguém ativando antes de ele cair): o som de carregar quando ela começa e o efeito dela quando solta
  for(const pausa of ativo?.pausas??[]){
    const chave=`${ativo!.event.id}-${pausa.evento.id}`;
    if(pausa.t<=0||pausasTocadas.current.has(chave)||mudo)continue;
    pausasTocadas.current.add(chave);if(pausasTocadas.current.size>40)pausasTocadas.current.delete(pausasTocadas.current.values().next().value!);
    const dono=ativo!.after.fighters.find(f=>f.uid===pausa.quem);
    if(dono&&pausa.fases.preparo>0)battleAudio.sound(preparoDaUnica(dono.characterId).som,PRIORIDADE.habilidade,0,ativo!.event.id*10+6);
    if(dono)battleAudio.sound(efeitoDaUnica(dono.characterId,pausa.evento.label).som as Sound,PRIORIDADE.habilidade,0,ativo!.event.id*10+7,Math.max(0,pausa.fases.soltaEm-pausa.t));
  }
  if(ativo?.impacted&&ativo.passos&&ativo.etapa&&!mudo){
    const visto=passoTocado.current.beat===ativo.event.id?passoTocado.current.passo:0;
    // o primeiro passo já tem o som do golpe; um traço sozinho começa direto na reação
    for(let k=Math.max(ativo.passos[0]?.classe==='reacao'||ativo.passos[0]?.classe==='unica'?1:2,visto+1);k<=ativo.etapa;k++){
      const passo=ativo.passos[k-1];if(!passo)continue;
      // a ativação completa da Mecânica única toca o som próprio dela (a sozinha já tocou acima)
      if(passo.classe==='unica'){
        if(ativo.traco||passo.antecipada)continue;
        // no meio da cadeia: as mesmas fases da sozinha (carrega e solta)
        const ev=ativo.events.find(e=>e.kind==='unica'&&passo.eventos.includes(e.id)),dono=ativo.after.fighters.find(f=>f.uid===passo.quem);
        if(ev&&dono){
          const fases=fasesDoEvento(ev,ativo.after,ativo);
          if(fases.preparo>0)battleAudio.sound(preparoDaUnica(dono.characterId).som,PRIORIDADE.habilidade,0,ativo.event.id*10+k);
          battleAudio.sound(efeitoDaUnica(dono.characterId,ev.label).som as Sound,PRIORIDADE.habilidade,0,ativo.event.id*10+k+5,fases.soltaEm);
        }
        continue;
      }
      // cada golpe da rajada soa quando chega (src/presentation/rajada-da-unica.ts)
      if(passo.rajada){const r=rajadaDaChave(passo.rajada.chave);if(r)battleAudio.sound(r.som as Sound,PRIORIDADE.habilidade,0,ativo.event.id*10+k);continue;}
      // o resultado da Mecânica única já soou com ela
      if(passo.resultado)continue;
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
}
