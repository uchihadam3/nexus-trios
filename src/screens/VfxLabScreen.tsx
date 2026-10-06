import { useEffect,useState,type CSSProperties } from 'react';
import { Play,Volume2 } from 'lucide-react';
import { VFX_FAMILIES,atlasFor,type VfxFamily } from '../presentation/vfxProfiles';
import { battleAudio } from '../lib/audio';
import type { Sound } from '../audio/cues';
interface VfxManifest {families:Record<string,{bytes:number}>}

type Phase='charge'|'travel'|'impact';
const families=Object.keys(VFX_FAMILIES) as VfxFamily[];
const soundFor:Record<VfxFamily,Sound>={physical_light:'action',physical_heavy:'physical',slash:'slash',projectile:'energy-shot',energy_orb:'energy',energy_beam:'energy',electric:'electric',fire:'fire',magic_psychic:'magic',dark:'dark',control:'prison',shield:'shield',heal_buff:'heal'};
const travelFor=new Set<VfxFamily>(['projectile','energy_orb','energy_beam','electric','fire','magic_psychic','dark','control']);
const kb=(bytes:number)=>(bytes/1024).toFixed(0);
export function VfxLabScreen(){
  const [manifest,setManifest]=useState<VfxManifest|null>(null);
  useEffect(()=>{const abort=new AbortController();fetch('/assets/vfx/manifest.json',{signal:abort.signal}).then(r=>r.json()).then(setManifest).catch(()=>undefined);return ()=>abort.abort()},[]);
  const [family,setFamily]=useState<VfxFamily>('energy_beam');
  const [phase,setPhase]=useState<Phase>('impact');
  const [scale,setScale]=useState(1.1),[area,setArea]=useState(false),[grand,setGrand]=useState(false),[playKey,setPlayKey]=useState(0);
  const replay=()=>setPlayKey(n=>n+1);
  const item=VFX_FAMILIES[family],atlas=manifest?.families[atlasFor(family)];
  const style={'--sprite-image':`url(/assets/vfx/${atlasFor(family)}.webp)`,'--fx-scale':scale} as CSSProperties;
  return <section className="vfx-lab">
    <header className="vfx-lab-heading"><span className="eyebrow">INSPEÇÃO AUDIOVISUAL</span><h1>Biblioteca de combate.</h1><p>Treze famílias em doze atlas originais compartilhados por ataques básicos e habilidades. Escolha uma fase, ajuste o tamanho e ouça o som associado.</p></header>
    <div className="vfx-lab-workbench"><div className="vfx-lab-controls">
      <label>Família<select value={family} onChange={e=>{setFamily(e.target.value as VfxFamily);setPhase('impact');replay()}}>{families.map(f=><option key={f} value={f}>{VFX_FAMILIES[f].name}</option>)}</select></label>
      <label>Escala <strong>{scale.toFixed(1)}×</strong><input type="range" min=".7" max="1.8" step=".1" value={scale} onChange={e=>{setScale(Number(e.target.value));replay()}}/></label>
      <fieldset><legend>Fase</legend>{(['charge','travel','impact'] as const).map(p=><button key={p} className={phase===p?'active':''} disabled={p==='travel'&&!travelFor.has(family)} onClick={()=>{setPhase(p);replay()}}>{p==='charge'?'Preparação':p==='travel'?'Trajeto':'Impacto'}</button>)}</fieldset>
      <fieldset><legend>Composição</legend><button className={area?'active':''} onClick={()=>{setArea(!area);replay()}}>Área</button><button className={grand?'active':''} onClick={()=>{setGrand(!grand);replay()}}>Grand</button></fieldset>
      <button className="primary vfx-replay" onClick={replay}><Play size={16}/>Reproduzir</button>
      <button className="primary vfx-replay" onClick={()=>void battleAudio.preview(soundFor[family])}><Volume2 size={16}/>Ouvir SFX</button>
      <p className="vfx-profile-note">{item.size} × {item.size} px por quadro · 12 quadros · {atlas?`${kb(atlas.bytes)} KB`:'carregando peso'} · {phase==='travel'&&family==='energy_beam'?'textura de feixe pré-renderizada':'WebP transparente'}</p>
    </div><div className="vfx-lab-demo" style={{'--fx-scale':scale} as CSSProperties}>
      <div key={`${family}-${phase}-${playKey}`} className={`effect-sprite sprite-${phase} ${area?'sprite-area-impact':''} ${grand?'sprite-grand-impact':''}`} style={style}/>
      {phase==='travel'&&family==='energy_beam'&&<div className="fx-beam" key={`beam-${playKey}`}/>}
      {phase==='impact'&&(area||grand)&&<div className="effect-sprite sprite-impact sprite-accent" style={{...style,left:'58%',top:'56%'}}/>}
      <span className="vfx-lab-phase">{phase==='charge'?'PREPARAÇÃO':phase==='travel'?'TRAJETO':'IMPACTO'} · {item.name.toUpperCase()}</span>
    </div></div>
    <h2 className="vfx-gallery-title">Famílias reutilizáveis <small>{families.length} famílias · {families.length-1} atlas · {manifest?`${kb(Object.values(manifest.families).reduce((sum,item)=>sum+item.bytes,0))} KB`:'carregando pesos'}</small></h2>
    <div className="vfx-family-gallery">{families.map(f=><button key={f} className={`vfx-family-card ${f===family?'active':''}`} onClick={()=>{setFamily(f);setPhase('impact');replay()}}><div><div className="effect-sprite" style={{'--sprite-image':`url(/assets/vfx/${atlasFor(f)}.webp)`} as CSSProperties}/></div><strong>{VFX_FAMILIES[f].name}</strong><small>12 quadros · {manifest?`${kb(manifest.families[atlasFor(f)].bytes)} KB`:'...'}</small></button>)}</div>
  </section>;
}
