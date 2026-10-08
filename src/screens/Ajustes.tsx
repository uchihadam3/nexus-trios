import { useState,type CSSProperties,type ReactNode } from 'react';
import { Volume2,Volume1,Music2,Zap,Sparkles,Hash,Wind,Gauge,Repeat,CircleHelp,Eye,Clapperboard,UserPen,RotateCcw,Settings2,Check } from 'lucide-react';
import type { Settings } from '../lib/storage';
import { TelaTopo } from '../components/Casca';
import { battleAudio } from '../lib/audio';

/*
 * Ajustes (remake): um painel de jogo, sem parágrafo.
 *
 * Som em três barras grandes com o número ao lado; o visual e a sequência
 * automática como interruptores-cartão (tocar acende); velocidade e ajuda como
 * botões de escolha; e embaixo uma fileira de atalhos — rever o tutorial, a
 * galeria de efeitos, o nome no ranking e apagar os dados. Tudo cabe em pouco
 * mais de uma tela no celular.
 */
function Barra({icone,nome,valor,onChange,cor}:{icone:ReactNode;nome:string;valor:number;onChange:(v:number)=>void;cor:string}){
  return <label className="aj-barra" style={{'--aj':cor,'--v':`${valor}%`} as CSSProperties}>
    <span className="aj-barra-icone">{icone}</span>
    <span className="aj-barra-nome">{nome}</span>
    <input aria-label={nome} type="range" min="0" max="100" value={valor} onChange={e=>onChange(Number(e.target.value))}/>
    <b>{valor}</b>
  </label>;
}

function Chave({icone,nome,dica,ligado,onChange,cor}:{icone:ReactNode;nome:string;dica:string;ligado:boolean;onChange:(v:boolean)=>void;cor:string}){
  return <label className={`aj-chave ${ligado?'ligado':''}`} style={{'--aj':cor} as CSSProperties}>
    <input type="checkbox" className="aj-escondido" checked={ligado} onChange={e=>onChange(e.target.checked)} aria-label={nome}/>
    <span className="aj-chave-icone">{icone}</span>
    <b>{nome}</b><small>{dica}</small>
    <i aria-hidden className="aj-luz"/>
  </label>;
}

function Escolha<T extends string|number>({nome,icone,opcoes,valor,onChange,cor}:{nome:string;icone:ReactNode;opcoes:readonly (readonly [T,string])[];valor:T;onChange:(v:T)=>void;cor:string}){
  return <div className="aj-escolha" style={{'--aj':cor} as CSSProperties} role="group" aria-label={nome}>
    <span className="aj-escolha-nome">{icone}{nome}</span>
    <div>{opcoes.map(([v,rotulo])=><button key={String(v)} className={valor===v?'ativo':''} aria-pressed={valor===v} onClick={()=>onChange(v)}>{rotulo}</button>)}</div>
  </div>;
}

/* Toca um golpe e diz se o som está liberado: o jeito de conferir no próprio celular. */
function TestarSom({settings:s}:{settings:Settings}){
  const [aviso,setAviso]=useState('');
  const testar=async()=>{
    setAviso('Tocando…');
    await battleAudio.preview(['soco-pesado','bloqueio']);
    const estado=battleAudio.status.state;
    setAviso(s.volume===0?'O Volume está no zero: arraste a barra para a direita.'
      :estado!=='running'?'O navegador ainda não liberou o som. Toque no botão de novo.'
      :s.effectsVolume===0?'Os Efeitos sonoros estão no zero.'
      :'Som liberado. Se não ouviu nada, aumente o volume de mídia do celular (botão lateral) e tire o modo silencioso.');
  };
  return <div className="aj-testar"><button type="button" onClick={()=>void testar()}><Volume1 size={18}/>Testar som</button>{aviso&&<p role="status">{aviso}</p>}</div>;
}

export function SettingsScreen({settings:s,onChange,onReset,onGaleria,ranking}:{settings:Settings;onChange:(s:Settings)=>void;onReset:()=>void;onGaleria:()=>void;ranking?:{nome?:string;onEditar:()=>void}}){
  const [confirm,setConfirm]=useState(false),[revisto,setRevisto]=useState(false);
  const muda=<K extends keyof Settings>(k:K,v:Settings[K])=>onChange({...s,[k]:v});
  return <section className="ajustes-v2">
    <TelaTopo icone={<Settings2/>} cor="#c3a2ff" rotulo="AJUSTES" titulo="Do seu jeito"><p>Fica salvo neste aparelho.</p></TelaTopo>

    <div className="aj-painel">
      <h2><Volume2 size={16}/>SOM</h2>
      <Barra icone={<Volume2 size={18}/>} nome="Volume" valor={s.volume} onChange={v=>muda('volume',v)} cor="#c8f560"/>
      <Barra icone={<Music2 size={18}/>} nome="Música de batalha" valor={s.musicVolume} onChange={v=>muda('musicVolume',v)} cor="#8fd3ff"/>
      <Barra icone={<Zap size={18}/>} nome="Efeitos sonoros" valor={s.effectsVolume} onChange={v=>muda('effectsVolume',v)} cor="#ffb86b"/>
      <TestarSom settings={s}/>
    </div>

    <div className="aj-painel">
      <h2><Sparkles size={16}/>VISUAL</h2>
      <div className="aj-chaves">
        <Chave icone={<Sparkles size={22}/>} nome="Efeitos visuais" dica="raios e explosões" ligado={s.effects} onChange={v=>muda('effects',v)} cor="#ffd36b"/>
        <Chave icone={<Hash size={22}/>} nome="Números de combate" dica="dano e cura na tela" ligado={s.numbers} onChange={v=>muda('numbers',v)} cor="#ff8a7a"/>
        <Chave icone={<Wind size={22}/>} nome="Reduzir movimento" dica="menos tremor" ligado={s.reducedMotion} onChange={v=>muda('reducedMotion',v)} cor="#8fd3ff"/>
      </div>
    </div>

    <div className="aj-painel">
      <h2><Gauge size={16}/>JOGO</h2>
      <Escolha nome="Velocidade padrão" icone={<Gauge size={16}/>} opcoes={[[1,'1×'],[2,'2×']] as const} valor={s.speed} onChange={v=>muda('speed',v)} cor="#c8f560"/>
      <Escolha nome="Ajuda na batalha" icone={<CircleHelp size={16}/>} opcoes={[['normal','Normal'],['detailed','Detalhada'],['off','Desligada']] as const} valor={s.explanations} onChange={v=>muda('explanations',v)} cor="#8fd3ff"/>
      <div className="aj-chaves um"><Chave icone={<Repeat size={22}/>} nome="Sequência automática" dica="a próxima luta começa sozinha após vencer" ligado={s.auto} onChange={v=>muda('auto',v)} cor="#86e3a8"/></div>
    </div>

    <div className="aj-atalhos">
      <button onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1');setRevisto(true);}catch{return}}} style={{'--tile':'#8fd3ff'} as CSSProperties}>{revisto?<Check size={22}/>:<Eye size={22}/>}<b>{revisto?'Guia volta na próxima luta':'Rever tutorial'}</b></button>
      <button onClick={onGaleria} style={{'--tile':'#ffd36b'} as CSSProperties}><Clapperboard size={22}/><b>Galeria de efeitos</b></button>
      {ranking&&<button onClick={ranking.onEditar} style={{'--tile':'#86e3a8'} as CSSProperties}><UserPen size={22}/><b>Nome no ranking</b><small>{ranking.nome??'ainda não escolhido'}</small></button>}
      <button className="aj-perigo" onClick={()=>setConfirm(true)} style={{'--tile':'#ff7a6b'} as CSSProperties}><RotateCcw size={22}/><b>Resetar dados</b></button>
    </div>
    {confirm&&<div className="aj-confirma" role="alertdialog" aria-label="Apagar dados locais?">
      <p><b>Apagar tudo deste aparelho?</b> Jornada, recorde e ajustes somem.</p>
      <div><button className="danger" onClick={onReset}>Apagar dados locais</button><button className="secondary" onClick={()=>setConfirm(false)}>Cancelar</button></div>
    </div>}
  </section>;
}
