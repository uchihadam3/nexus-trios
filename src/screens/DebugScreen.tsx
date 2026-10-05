import { useState } from 'react';
import { byId,characters } from '../data/characters';
import { createBattle,simulate,stepBattle } from '../engine/battle';
import type { Battle } from '../engine/types';
import { AuxIcon,SkillIcon } from '../components/Icon';
import { StatusBadge } from '../components/StatusBadge';
import { statuses } from '../data/statuses';

type AtlasTab='skills'|'statuses'|'ui'|'portraits';
const uiNames:Record<string,string>={ready:'Pronta',cooldown:'Cooldown',charging:'Carregando',preparing:'Preparando',executing:'Executando',buff:'Buff',debuff:'Debuff','tempo-up':'Ação acelerada','tempo-down':'Ação atrasada',interrupt:'Interrupção',history:'Histórico',inspect:'Inspeção',help:'Ajuda',domain:'Domínio',victory:'Vitória',defeat:'Derrota'};
const statusNames:Record<string,string>={exposed:'Exposto',paralyzed:'Paralisado',protected:'Protegido',marked:'Marcado',slow:'Lento',haste:'Acelerado',confused:'Confuso',rooted:'Preso',regen:'Regeneração',burning:'Queimando',electric:'Eletrificado',silenced:'Silenciado',strengthened:'Fortalecido',weakened:'Enfraquecido'};
export function DebugScreen(){
  const [left,setLeft]=useState(['light','pikachu','wolverine']);
  const [right,setRight]=useState(['thanos','gojo','superman']);
  const [result,setResult]=useState<Battle|null>(null);
  const [seed,setSeed]=useState(1);
  const [error,setError]=useState('');
  const [atlas,setAtlas]=useState(false);
  const [tab,setTab]=useState<AtlasTab>('skills');
  const run=(full:boolean)=>{try{const b=full?simulate(left,right,seed):createBattle(left,right,seed);setResult(b);setError('');}catch(e){setError(String(e));}};
  const log=result?[...(result.targetLog??[]).map(d=>({time:d.time,line:`ALVO ${d.time.toFixed(1)} ${byId[result.fighters.find(f=>f.uid===d.actor)?.characterId??'']?.name??d.actor} → ${byId[result.fighters.find(f=>f.uid===d.target)?.characterId??'']?.name??d.target} [${d.intent}] ${d.reasons.join(' · ')}`})),...result.events.filter(e=>!['damage','heal','synergy'].includes(e.kind)).map(e=>({time:e.time,line:`${e.time.toFixed(1)} ${e.kind} ${e.source} → ${e.target??''} ${e.label}`}))].sort((a,z)=>a.time-z.time).slice(-80).map(x=>x.line).join('\n'):'';
  return <section className="debug-screen">
    <span className="eyebrow">DESENVOLVIMENTO · NÃO ALTERA A JORNADA</span><h1>Laboratório headless</h1>
    <button className="secondary atlas-toggle" onClick={()=>setAtlas(!atlas)}>{atlas?'Fechar inspeção visual':'Abrir inspeção visual de assets · 100 lutadores'}</button>
    {atlas&&<section className="asset-inspector" aria-label="Inspeção visual dos assets">
      <p>Prévia dos PNGs realmente usados pelo jogo. O quadriculado mostra a transparência; habilidades: 300 · estados: 14 · interface: 16 · retratos: {characters.length}.</p>
      <nav className="asset-inspector-tabs" aria-label="Conjuntos de assets">{([['skills','300 habilidades'],['statuses','14 estados'],['ui','16 auxiliares'],['portraits',`${characters.length} retratos`]] as const).map(([id,label])=><button key={id} className={tab===id?'selected':''} onClick={()=>setTab(id)}>{label}</button>)}</nav>
      {tab==='skills'&&<div className="skill-atlas">{characters.map(c=><article key={c.id}><strong>{c.name}</strong><div>{c.skills.map(skill=><figure key={skill.id}><SkillIcon type={skill.icon} characterId={c.id} skillId={skill.id} size={42}/><figcaption>{skill.name}</figcaption></figure>)}</div></article>)}</div>}
      {tab==='statuses'&&<div className="asset-icon-grid">{Object.entries(statusNames).map(([id,name])=><figure key={id}><StatusBadge status={{id:id as keyof typeof statuses,remaining:8,duration:10,intensity:0,source:'preview'}}/><figcaption>{name}</figcaption></figure>)}</div>}
      {tab==='ui'&&<div className="asset-icon-grid">{Object.entries(uiNames).map(([id,name])=><figure key={id}><AuxIcon id={id as 'ready'} size={56}/><figcaption>{name}</figcaption></figure>)}</div>}
      {tab==='portraits'&&<div className="portrait-atlas">{characters.map(c=><figure key={c.id}><img src={c.portrait} alt={c.name}/><figcaption>{c.name}</figcaption></figure>)}</div>}
    </section>}
    <div className="debug-teams">{([left,right] as string[][]).map((team,side)=><div key={side}><h3>{side?'Rivais':'Seu trio'}</h3>{team.map((id,i)=><select aria-label={`Equipe ${side} posição ${i}`} key={i} value={id} onChange={e=>{const next=[...team];next[i]=e.target.value;(side?setRight:setLeft)(next);}}>{characters.map(c=><option value={c.id} key={c.id}>{c.name}</option>)}</select>)}</div>)}</div>
    <label>Semente <input type="number" value={seed} onChange={e=>setSeed(Number(e.target.value))}/></label>
    <div className="debug-actions"><button className="primary" onClick={()=>run(true)}>Simular 120 s instantaneamente</button><button className="secondary" onClick={()=>run(false)}>Iniciar / reiniciar</button><button className="secondary" disabled={!result||result.finished} onClick={()=>{if(result){const b=structuredClone(result);for(let i=0;i<100;i++)stepBattle(b);setResult(b);}}}>Avançar 10 s</button></div>
    {error&&<p role="alert">{error}</p>}
    {result&&<><h2>{result.finished?`${result.winner}: ${result.reason}`:`${result.time.toFixed(1)} s · em andamento`}</h2><p>Domínio: {result.dominion.toFixed(2)} · Eventos: {result.nextEvent-1}</p><pre>{log}</pre></>}
  </section>;
}
