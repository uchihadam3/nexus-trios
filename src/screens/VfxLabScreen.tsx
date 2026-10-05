import { useMemo,useState } from 'react';
import { Play,RotateCcw,Sparkles } from 'lucide-react';
import { VFX_PRESETS,type VfxProfile } from '../presentation/vfxProfiles';

const familyNames:Record<string,string>={physical:'Impacto físico',energy:'Energia',electric:'Eletricidade',fire:'Fogo',grand:'Grande impacto',slash:'Corte',magic:'Magia',dark:'Energia sombria',psychic:'Psíquico',shield:'Escudo',heal:'Cura',regen:'Regeneração',prison:'Prisão',interrupt:'Interrupção',ko:'Nocaute',buff:'Fortalecimento',debuff:'Enfraquecimento'};
const families=Object.keys(familyNames);
const profiles=Object.values(VFX_PRESETS);
const names:Record<string,string>={kamehameha:'Kamehameha', 'final-flash':'Final Flash',rasengan:'Rasengan',chidori:'Chidori','death-note':'Death Note','gear-fifth':'Gear Fifth','serious-punch':'Soco sério','heat-vision':'Visão de calor','web-cast':'Teia','impact-web':'Teia de impacto','mjolnir-storm':'Tempestade de Mjölnir','sling-ring-portal':'Portal do Doutor Estranho','thousand-blows':'Mil golpes do Flash','magnetic-prison':'Prisão magnética','azarath-shadow':'Magia sombria de Raven','titan-cosmic-wave':'Onda cósmica de Thanos'};
const palette:Record<string,string>={physical:'#ffe1a5',energy:'#90e4ff',electric:'#fff096',fire:'#ff814f',grand:'#ffe18a',slash:'#e9f5ff',magic:'#c49cff',dark:'#b47af4',psychic:'#ff9edb',shield:'#8ee1ff',heal:'#91ffc1',regen:'#a8f39d',prison:'#a3e5f2',interrupt:'#ffa783',ko:'#ff8d83',buff:'#eaf6a4',debuff:'#d895d9'};

function Preview({family,motif,phase,scale,color,playKey}:{family:string;motif:string;phase:'charge'|'travel'|'impact';scale:number;color:string;playKey:number}){
  const stage=phase==='charge'?'sprite-cast sprite-charge':phase==='travel'?'sprite-travel':'sprite-landed sprite-impact';
  return <div className={`vfx-lab-demo family-${family} motif-${motif}`} style={{'--fx-color':color,'--fx-scale':scale} as React.CSSProperties}>
    {phase==='travel'&&motif==='beam'&&<div className="beam-ribbon beam-beam" style={{'--beam-length':'78%','--beam-angle':'0deg','--beam-mid-x':'50%','--beam-mid-y':'50%'} as React.CSSProperties}/>}
    <div key={`${phase}-${playKey}-${family}`} className={`effect-sprite sprite-${family} ${stage} ${phase==='travel'?`motif-travel-${motif}`:''}`} style={{left:'50%',top:'50%','--sprite-image':`url(/assets/vfx/${family}.webp)`} as React.CSSProperties}/>
    <span className="vfx-lab-phase">{phase==='charge'?'PREPARAÇÃO':phase==='travel'?'TRAJETO':'IMPACTO'}</span>
  </div>;
}

export function VfxLabScreen(){
  const [family,setFamily]=useState('energy'),[profileId,setProfileId]=useState('kamehameha'),[phase,setPhase]=useState<'charge'|'travel'|'impact'>('impact');
  const [scale,setScale]=useState(1.15),[color,setColor]=useState('#90e4ff'),[playKey,setPlayKey]=useState(0);
  const selected=useMemo(()=>profiles.find(p=>p.id===profileId),[profileId]);
  const chooseProfile=(p:VfxProfile)=>{setProfileId(p.id);setFamily(p.family??'energy');setColor(palette[p.family??'energy']??'#9be7ff');setScale(p.scale);setPlayKey(n=>n+1);};
  const replay=()=>setPlayKey(n=>n+1);
  return <section className="vfx-lab">
    <header className="vfx-lab-heading"><span className="eyebrow">INSPEÇÃO AUDIOVISUAL</span><h1>Galeria de combate.</h1><p>Os atlas que aparecem na arena, organizados por família. Selecione uma habilidade, ajuste a leitura e repita o efeito.</p></header>
    <div className="vfx-lab-workbench"><div className="vfx-lab-controls">
      <label>Família<select value={family} onChange={e=>{setFamily(e.target.value);setProfileId('');setColor(palette[e.target.value]??'#9be7ff');setPlayKey(n=>n+1)}}>{families.map(f=><option key={f} value={f}>{familyNames[f]}</option>)}</select></label>
      <label>Preset icônico<select value={profileId} onChange={e=>{const p=profiles.find(x=>x.id===e.target.value);if(p)chooseProfile(p);else setProfileId('')}}><option value="">Família sem preset</option>{profiles.map(p=><option key={p.id} value={p.id}>{names[p.id]??p.id}</option>)}</select></label>
      <label className="vfx-color-control">Cor do brilho<input type="color" value={color} onChange={e=>setColor(e.target.value)}/></label>
      <label>Escala <strong>{scale.toFixed(1)}×</strong><input type="range" min=".7" max="1.8" step=".1" value={scale} onChange={e=>setScale(Number(e.target.value))}/></label>
      <fieldset><legend>Fase</legend>{(['charge','travel','impact'] as const).map(p=><button key={p} className={phase===p?'active':''} onClick={()=>{setPhase(p);replay()}}>{p==='charge'?'Preparação':p==='travel'?'Trajeto':'Impacto'}</button>)}</fieldset>
      <button className="primary vfx-replay" onClick={replay}><Play size={16}/>Reproduzir novamente</button>
      {selected&&<p className="vfx-profile-note"><Sparkles size={15}/>{names[selected.id]??selected.id}: preset de apresentação declarado em dados.</p>}
    </div><Preview family={family} motif={selected?.motif??'default'} phase={phase} scale={scale} color={color} playKey={playKey}/></div>
    <h2 className="vfx-gallery-title">Famílias geradas <small>{families.length} atlas · 16 quadros por atlas</small></h2>
    <div className="vfx-family-gallery">{families.map(f=><button key={f} className={`vfx-family-card family-${f}`} onClick={()=>{setFamily(f);setProfileId('');setColor(palette[f]??'#9be7ff');setPhase('impact');replay()}}><div><div key={`${f}-${playKey}`} className={`effect-sprite sprite-${f} sprite-landed`} style={{left:'50%',top:'50%','--fx-color':palette[f],'--sprite-image':`url(/assets/vfx/${f}.webp)`} as React.CSSProperties}/></div><strong>{familyNames[f]}</strong><small>128–384 px · RGBA</small></button>)}</div>
    <h2 className="vfx-gallery-title">Habilidades icônicas <small>{profiles.length} presets com silhueta/estágio próprios</small></h2>
    <div className="vfx-profile-gallery">{profiles.map(p=><button key={p.id} onClick={()=>{chooseProfile(p);setPhase('impact')}}><span className={`mini-vfx family-${p.family}`}><span className={`effect-sprite sprite-${p.family} sprite-landed motif-${p.motif}`} style={{left:'50%',top:'50%','--fx-color':palette[p.family??'energy'],'--sprite-image':`url(/assets/vfx/${p.family??'energy'}.webp)`} as React.CSSProperties}/></span><strong>{names[p.id]??p.id}</strong><small>{familyNames[p.family??'energy']} · {p.scale.toFixed(1)}×</small></button>)}</div>
    <div className="vfx-lab-footer"><RotateCcw size={14}/> A fase e a escala aqui reproduzem a mesma família de atlas usada durante a batalha.</div>
  </section>;
}
