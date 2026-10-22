import { useState,type CSSProperties,type ReactNode } from 'react';
import { Volume2,Volume1,Music2,Zap,Sparkles,Hash,Wind,Gauge,Repeat,CircleHelp,Eye,Clapperboard,RotateCcw,Settings2,Check } from 'lucide-react';
import { VELOCIDADES, type Settings } from '../lib/storage';
import { TelaTopo } from '../components/Casca';
import { battleAudio } from '../lib/audio';
import { TrocaDeIdioma } from '../components/TrocaDeIdioma';
import { t } from '../i18n/idioma';

/*
 * Ajustes (remake): um painel de jogo, sem parágrafo.
 *
 * Som em três barras grandes com o número ao lado; o visual e a sequência
 * automática como interruptores-cartão (tocar acende); velocidade e ajuda como
 * botões de escolha; e embaixo uma fileira de atalhos — rever o tutorial, a
 * galeria de efeitos e apagar os dados. Tudo cabe em pouco
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
    setAviso(t('Tocando…'));
    await battleAudio.preview(['soco-pesado','bloqueio']);
    const estado=battleAudio.status.state;
    setAviso(s.volume===0?t('O Volume está no zero: arraste a barra para a direita.')
      :estado!=='running'?t('O navegador ainda não liberou o som. Toque no botão de novo.')
      :s.effectsVolume===0?t('Os Efeitos sonoros estão no zero.')
      :t('Som liberado. Se não ouviu nada, aumente o volume de mídia do celular (botão lateral) e tire o modo silencioso.'));
  };
  return <div className="aj-testar"><button type="button" onClick={()=>void testar()}><Volume1 size={18}/>{t('Testar som')}</button>{aviso&&<p role="status">{aviso}</p>}</div>;
}

export function SettingsScreen({settings:s,onChange,onReset,onGaleria}:{settings:Settings;onChange:(s:Settings)=>void;onReset:()=>void;onGaleria:()=>void}){
  const [confirm,setConfirm]=useState(false),[revisto,setRevisto]=useState(false);
  const muda=<K extends keyof Settings>(k:K,v:Settings[K])=>onChange({...s,[k]:v});
  return <section className="ajustes-v2">
    <TelaTopo icone={<Settings2/>} cor="#c3a2ff" rotulo={t('AJUSTES')} titulo={t('Do seu jeito')}><p>{t('Fica salvo neste aparelho.')}</p></TelaTopo>
    <TrocaDeIdioma/>

    <div className="aj-painel">
      <h2><Volume2 size={16}/>{t('SOM')}</h2>
      <Barra icone={<Volume2 size={18}/>} nome={t('Volume')} valor={s.volume} onChange={v=>muda('volume',v)} cor="#c8f560"/>
      <Barra icone={<Music2 size={18}/>} nome={t('Música de batalha')} valor={s.musicVolume} onChange={v=>muda('musicVolume',v)} cor="#8fd3ff"/>
      <Barra icone={<Zap size={18}/>} nome={t('Efeitos sonoros')} valor={s.effectsVolume} onChange={v=>muda('effectsVolume',v)} cor="#ffb86b"/>
      <TestarSom settings={s}/>
    </div>

    <div className="aj-painel">
      <h2><Sparkles size={16}/>{t('VISUAL')}</h2>
      <div className="aj-chaves">
        <Chave icone={<Sparkles size={22}/>} nome={t('Efeitos visuais')} dica={t('raios e explosões')} ligado={s.effects} onChange={v=>muda('effects',v)} cor="#ffd36b"/>
        <Chave icone={<Hash size={22}/>} nome={t('Números de combate')} dica={t('dano e cura na tela')} ligado={s.numbers} onChange={v=>muda('numbers',v)} cor="#ff8a7a"/>
        <Chave icone={<Wind size={22}/>} nome={t('Reduzir movimento')} dica={t('menos tremor')} ligado={s.reducedMotion} onChange={v=>muda('reducedMotion',v)} cor="#8fd3ff"/>
      </div>
    </div>

    <div className="aj-painel">
      <h2><Gauge size={16}/>{t('JOGO')}</h2>
      <Escolha nome={t('Velocidade padrão')} icone={<Gauge size={16}/>} opcoes={VELOCIDADES.map((v)=>[v,`${v}×`] as const)} valor={s.speed} onChange={v=>muda('speed',v)} cor="#c8f560"/>
      <Escolha nome={t('Ajuda na batalha')} icone={<CircleHelp size={16}/>} opcoes={[['normal',t('Normal')],['detailed',t('Detalhada')],['off',t('Desligada')]] as const} valor={s.explanations} onChange={v=>muda('explanations',v)} cor="#8fd3ff"/>
      <div className="aj-chaves um"><Chave icone={<Repeat size={22}/>} nome={t('Sequência automática')} dica={t('a próxima luta começa sozinha após vencer')} ligado={s.auto} onChange={v=>muda('auto',v)} cor="#86e3a8"/></div>
    </div>

    <div className="aj-atalhos">
      <button onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1');setRevisto(true);}catch{return}}} style={{'--tile':'#8fd3ff'} as CSSProperties}>{revisto?<Check size={22}/>:<Eye size={22}/>}<b>{revisto?t('Guia volta na próxima luta'):t('Rever tutorial')}</b></button>
      <button onClick={onGaleria} style={{'--tile':'#ffd36b'} as CSSProperties}><Clapperboard size={22}/><b>{t('Galeria de efeitos')}</b></button>
      <button className="aj-perigo" onClick={()=>setConfirm(true)} style={{'--tile':'#ff7a6b'} as CSSProperties}><RotateCcw size={22}/><b>{t('Resetar dados')}</b></button>
    </div>
    {confirm&&<div className="aj-confirma" role="alertdialog" aria-label={t('Apagar dados locais?')}>
      <p><b>{t('Apagar tudo deste aparelho?')}</b> {t('Jornada, recorde e ajustes somem.')}</p>
      <div><button className="danger" onClick={onReset}>{t('Apagar dados locais')}</button><button className="secondary" onClick={()=>setConfirm(false)}>{t('Cancelar')}</button></div>
    </div>}
  </section>;
}
