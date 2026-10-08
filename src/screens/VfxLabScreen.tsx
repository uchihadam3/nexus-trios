import { useEffect,useState,type CSSProperties } from 'react';
import { Play,Volume2 } from 'lucide-react';
import { FAMILIAS,familia,folha,legivel,type Grupo,type VfxFamily } from '../presentation/vfxProfiles';
import { SOM_DA_FAMILIA,type Sound } from '../audio/cues';
import { battleAudio } from '../lib/audio';
interface Manifest {[folha:string]:{bytes:number;tamanho:[number,number]}}

type Fase='preparo'|'viagem'|'faixa'|'impacto';
const GRUPOS:Grupo[]=['físico','corte','projétil','energia','elemento','magia','apoio','especial'];
const kb=(bytes:number)=>(bytes/1024).toFixed(0);
const CORES=['#5ec8ff','#ff4a3a','#ffe66b','#b77cff','#5fe36b','#ff7ad1','#ffffff'];

/** Galeria das famílias de efeito (adendo, parte 3): cada família, cada camada, em qualquer cor. */
export function VfxLabScreen(){
  const [manifest,setManifest]=useState<Manifest|null>(null);
  useEffect(()=>{const abort=new AbortController();fetch(`/assets/vfx/familias/manifest.json`,{signal:abort.signal}).then(r=>r.json()).then(setManifest).catch(()=>undefined);return ()=>abort.abort()},[]);
  const [chave,setChave]=useState<VfxFamily>('feixe_pesado');
  const [fase,setFase]=useState<Fase>('impacto');
  const [cor,setCor]=useState<string|null>(null),[escala,setEscala]=useState(1),[toca,setToca]=useState(0);
  const fam=familia(chave);
  const tinta=legivel(cor??fam.cor,chave==='sombra'||chave==='execucao');
  const replay=()=>setToca(n=>n+1);
  const escolhe=(k:VfxFamily)=>{setChave(k);setFase('impacto');replay();};
  const temFase=(f:Fase)=>f==='impacto'||(f==='preparo'?!!fam.preparo:f==='viagem'?!!fam.viagem:!!fam.faixa);
  const nomeDaFolha=fase==='preparo'?fam.preparo:fase==='viagem'?fam.viagem:fase==='faixa'?fam.faixa:fam.impacto;
  const total=manifest?Object.values(manifest).reduce((s,x)=>s+x.bytes,0):0;
  const demo:CSSProperties=fase==='faixa'
    ?{left:'12%',top:'50%',width:'76%',height:70*escala,'--ang':'0deg','--faixa':'1.6s','--faixa-delay':'0s'} as CSSProperties
    :fase==='viagem'
      ?{left:'18%',top:'50%',width:120*escala,height:120*escala,'--dx':'260px','--dy':'0px','--ang':'0deg','--voo':'1s','--voo-delay':'0s'} as CSSProperties
      :{left:'50%',top:'50%',width:240*escala,height:240*escala,'--ang':`${fam.giro??0}deg`,'--dur':`${1.1*fam.tempo/0.7}s`} as CSSProperties;
  const classe=fase==='impacto'?'fxl-impacto':fase==='viagem'?'fxl-laco fxl-voo':fase==='faixa'?'fxl-laco fxl-faixa':'fxl-laco';
  return <section className="vfx-lab">
    <header className="vfx-lab-heading"><span className="eyebrow">INSPEÇÃO AUDIOVISUAL</span><h1>Biblioteca de efeitos.</h1><p>{FAMILIAS.length} famílias montadas a partir de {manifest?Object.keys(manifest).length:'…'} folhas desenhadas em Python. Cada efeito é neutro e ganha a cor do personagem na luta: o mesmo feixe é o Kamehameha azul e a Visão de calor vermelha.</p></header>
    <div className="vfx-lab-workbench"><div className="vfx-lab-controls">
      <label>Família<select value={chave} onChange={e=>escolhe(e.target.value as VfxFamily)}>{GRUPOS.map(g=><optgroup key={g} label={g}>{FAMILIAS.filter(k=>familia(k).grupo===g).map(k=><option key={k} value={k}>{familia(k).nome}</option>)}</optgroup>)}</select></label>
      <fieldset><legend>Camada</legend>{(['preparo','viagem','faixa','impacto'] as const).map(f=><button key={f} className={fase===f?'active':''} disabled={!temFase(f)} onClick={()=>{setFase(f);replay()}}>{f==='preparo'?'Preparo':f==='viagem'?'Viagem':f==='faixa'?'Feixe':'Impacto'}</button>)}</fieldset>
      <fieldset><legend>Cor</legend><button className={cor===null?'active':''} onClick={()=>{setCor(null);replay()}}>Da família</button>{CORES.map(c=><button key={c} aria-label={`Cor ${c}`} className={`vfx-swatch ${cor===c?'active':''}`} style={{background:c}} onClick={()=>{setCor(c);replay()}}/>)}</fieldset>
      <label>Escala <strong>{escala.toFixed(1)}×</strong><input type="range" min=".6" max="1.6" step=".1" value={escala} onChange={e=>{setEscala(Number(e.target.value));replay()}}/></label>
      <button className="primary vfx-replay" onClick={replay}><Play size={16}/>Reproduzir</button>
      <button className="primary vfx-replay" onClick={()=>void battleAudio.preview([SOM_DA_FAMILIA[chave].antes,SOM_DA_FAMILIA[chave].saida,SOM_DA_FAMILIA[chave].impacto].filter((x):x is Sound=>!!x))}><Volume2 size={16}/>Ouvir SFX</button>
      <p className="vfx-profile-note">{nomeDaFolha} · 12 quadros · {manifest&&nomeDaFolha&&manifest[nomeDaFolha]?`${manifest[nomeDaFolha].tamanho.join(' × ')} px · ${kb(manifest[nomeDaFolha].bytes)} KB`:'…'}</p>
    </div><div className="vfx-lab-demo battle-effects" style={{'--fx-cor':tinta} as CSSProperties}>
      {nomeDaFolha&&<span key={`${chave}-${fase}-${toca}-${tinta}`} className={`fxl ${classe}`} style={{'--fx-img':`url(${folha(nomeDaFolha)})`,...demo} as CSSProperties}/>}
      <span className="vfx-lab-phase">{fam.grupo.toUpperCase()} · {fam.nome.toUpperCase()}</span>
    </div></div>
    <h2 className="vfx-gallery-title">Famílias reutilizáveis <small>{FAMILIAS.length} famílias · {manifest?`${Object.keys(manifest).length} folhas · ${kb(total)} KB, carregadas só quando usadas`:'carregando pesos'}</small></h2>
    {GRUPOS.map(g=><div key={g}><h3 className="vfx-group-title">{g}</h3><div className="vfx-family-gallery">{FAMILIAS.filter(k=>familia(k).grupo===g).map(k=>{const x=familia(k);return <button key={k} className={`vfx-family-card ${k===chave?'active':''}`} onClick={()=>escolhe(k)}><div className="battle-effects" style={{'--fx-cor':legivel(x.cor,k==='sombra'||k==='execucao')} as CSSProperties}><span className="fxl fxl-galeria" style={{'--fx-img':`url(${folha(x.impacto)})`,'--ang':`${x.giro??0}deg`} as CSSProperties}/></div><strong>{x.nome}</strong><small>{[x.preparo&&'preparo',x.viagem&&'viagem',x.faixa&&'feixe','impacto'].filter(Boolean).join(' · ')}</small></button>;})}</div></div>)}
  </section>;
}
