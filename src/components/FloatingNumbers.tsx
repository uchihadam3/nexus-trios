import { useEffect,useRef,useState } from 'react';
import { HeartPulse,Shield } from 'lucide-react';
import type { Battle } from '../engine/types';
import { etapaDoEvento,type Beat } from '../presentation/director';
import { fallbackPoint,type Anchors } from './BattleEffects';

/*
 * Números flutuantes com vida própria, numa camada acima dos efeitos (o
 * clarão do impacto não os cobre). Não somem quando a próxima ação começa:
 * cada número fica uns 1,8 s — no ritmo da velocidade da luta e parado na
 * pausa, porque sai no fim da própria animação — e vários seguidos se
 * empilham. Dano em vermelho, cura em verde, Escudo em azul-claro; um golpe
 * que tira 16% da Vida ou mais aparece maior.
 *
 * Regeneração e Queimadura contam por segundo inteiro: o tique é a cada
 * 0,1 s (src/engine/battle.ts) e as ações dos outros cortam a cena contínua
 * em pedaços, então o número junta 10 tiques — 1 s de luta — antes de
 * aparecer (ou o que houver, quando o efeito acaba). "+12 Vida/s" aparece
 * +12; menos só quando falta menos que isso para a Vida cheia.
 */
interface Numero {id:string;uid:string;tipo:'dano'|'cura'|'escudo'|'bloqueio';valor:number;forte:boolean}

export function FloatingNumbers({battle,beat,anchors,medal,enabled}:{battle:Battle;beat:Beat|null;anchors:Anchors;medal:number;enabled:boolean}){
  const [numeros,setNumeros]=useState<Numero[]>([]);
  const continuo=useRef(new Map<string,{valor:number;tiques:number}>()),ultimo=useRef(0);
  /* um efeito por vez: os números de cada etapa do impacto nascem na etapa deles */
  const etapa=beat?.impacted?(beat.etapa??3):0;
  const chave=beat?.impacted?`${beat.event.id}-${etapa}`:null;
  useEffect(()=>{
    if(chave===null||!beat||!enabled)return;
    const desta=beat.events.filter(e=>etapaDoEvento(beat,e)===etapa);
    const soma=(uid:string,kind:string)=>desta.filter(e=>e.kind===kind&&e.target===uid).reduce((t,e)=>t+(e.value??0),0);
    const novos:Numero[]=[];
    // uma luta nova recomeça o tempo: o que estava juntando fica para trás
    if(beat.after.time<ultimo.current)continuo.current.clear();
    ultimo.current=beat.after.time;
    for(const f of battle.fighters){
      let dano=soma(f.uid,'damage'),cura=soma(f.uid,'heal');const bloqueio=soma(f.uid,'block');
      if(beat.periodic){
        const porSegundo=(kind:'heal'|'damage')=>{
          const chaveDoTipo=`${f.uid}-${kind}`,tiques=desta.filter(e=>e.kind===kind&&e.target===f.uid);
          let junta=continuo.current.get(chaveDoTipo),total=0;
          for(const e of tiques){junta??={valor:0,tiques:0};junta.valor+=e.value??0;junta.tiques++;
            // fechou 1 s de luta
            if(junta.tiques>=10){total+=junta.valor;junta=undefined;}}
          // o efeito parou de tiquetaquear (acabou, ou a Vida encheu): mostra o que juntou
          if(junta&&!tiques.length){total+=junta.valor;junta=undefined;}
          if(junta)continuo.current.set(chaveDoTipo,junta);else continuo.current.delete(chaveDoTipo);
          return total;
        };
        cura=porSegundo('heal');dano=porSegundo('damage');
      }
      const escudo=desta.find(e=>e.target===f.uid&&e.kind==='shield'&&e.label==='Escudo');
      if(dano>0)novos.push({id:`${chave}-${f.uid}-d`,uid:f.uid,tipo:'dano',valor:dano,forte:dano>=f.maxHp*.16});
      if(cura>0)novos.push({id:`${chave}-${f.uid}-c`,uid:f.uid,tipo:'cura',valor:cura,forte:cura>=f.maxHp*.16});
      if(escudo)novos.push({id:`${chave}-${f.uid}-e`,uid:f.uid,tipo:'escudo',valor:escudo.value??0,forte:false});
      if(bloqueio>0)novos.push({id:`${chave}-${f.uid}-b`,uid:f.uid,tipo:'bloqueio',valor:bloqueio,forte:false});
    }
    if(novos.length)setNumeros(lista=>[...lista.filter(n=>!novos.some(x=>x.id===n.id)),...novos].slice(-12));
  },[chave]);
  const porLutador=new Map<string,Numero[]>();
  for(const n of numeros)porLutador.set(n.uid,[...(porLutador.get(n.uid)??[]),n].slice(-3));
  return <div className="floating-layer" aria-hidden="true">
    {[...porLutador].map(([uid,lista])=>{const p=anchors[uid]??fallbackPoint(uid);
      return <span key={uid} className="floating-numbers" style={{left:`${p.x}%`,top:`calc(${p.y}% - ${Math.round(medal*.08)}px)`}}>
        {lista.map(n=><span key={n.id} className={`float-number float-${n.tipo} ${n.forte?'float-strong':''}`} onAnimationEnd={()=>setNumeros(l=>l.filter(x=>x.id!==n.id))}>
          {n.tipo==='cura'&&<HeartPulse size={14}/>}{(n.tipo==='escudo'||n.tipo==='bloqueio')&&<Shield size={13}/>}
          {n.tipo==='dano'?'−':n.tipo==='bloqueio'?'':'+'}{Math.round(n.valor)}{n.tipo==='bloqueio'?' bloqueado':''}
        </span>)}
      </span>;})}
  </div>;
}
