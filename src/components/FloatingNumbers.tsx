import { useEffect,useState } from 'react';
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
 */
interface Numero {id:string;uid:string;tipo:'dano'|'cura'|'escudo'|'bloqueio';valor:number;forte:boolean}

export function FloatingNumbers({battle,beat,anchors,medal,enabled}:{battle:Battle;beat:Beat|null;anchors:Anchors;medal:number;enabled:boolean}){
  const [numeros,setNumeros]=useState<Numero[]>([]);
  /* um efeito por vez: os números de cada etapa do impacto nascem na etapa deles */
  const etapa=beat?.impacted?(beat.etapa??3):0;
  const chave=beat?.impacted?`${beat.event.id}-${etapa}`:null;
  useEffect(()=>{
    if(chave===null||!beat||!enabled)return;
    const desta=beat.events.filter(e=>etapaDoEvento(beat,e)===etapa);
    const soma=(uid:string,kind:string)=>desta.filter(e=>e.kind===kind&&e.target===uid).reduce((t,e)=>t+(e.value??0),0);
    const novos:Numero[]=[];
    for(const f of battle.fighters){
      const dano=soma(f.uid,'damage'),cura=soma(f.uid,'heal'),bloqueio=soma(f.uid,'block');
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
