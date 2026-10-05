import { useEffect,useRef } from 'react';
import { X, Activity, Timer, Info } from 'lucide-react';
import type { Character } from '../engine/types';
import { Portrait } from './Portrait';
import { SkillIcon } from './Icon';
export function CharacterModal({character:c,onClose}:{character:Character;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null);
  useEffect(()=>{ref.current?.showModal();return()=>ref.current?.close();},[]);
  return <dialog ref={ref} className="character-modal" onCancel={onClose} onClick={e=>{if(e.target===e.currentTarget)onClose();}}><div className="modal-inner">
    <button className="icon-button modal-close" aria-label="Fechar detalhes" onClick={onClose}><X size={20}/></button>
    <div className="modal-character" style={{'--character':c.color} as React.CSSProperties}><Portrait character={c}/><div><span className="eyebrow">{c.universe}</span><h2>{c.name}</h2><p>{c.idea}</p><span className="mini-label">RETRATO PROVISÓRIO</span></div></div>
    <div className="character-stats"><span><Activity size={16}/> {c.hp} Condição</span><span><Timer size={16}/> Ação a cada {c.interval.toLocaleString('pt-BR')} s</span></div>
    <div className="trait"><span className="eyebrow">TRAÇO PERMANENTE</span><h3>{c.trait.name}</h3><p>{c.trait.description}</p></div>
    <div className="detail-skills">{c.skills.map(s=><article key={s.id}><span className="skill-static"><SkillIcon type={s.icon} characterId={c.id} skillId={s.id}/></span><div><h3>{s.name}</h3><p>{s.description}</p><small>Carga: {s.chargeText} · {s.preparation>0?`${s.preparation.toLocaleString('pt-BR')} s de preparação`:'Uso instantâneo'} · {s.cooldown} s de recarga</small></div></article>)}</div>
    <div className="vulnerability"><Info size={17}/><p><strong>Ponto de atenção</strong><br/>{c.vulnerability}</p></div>
    <small className="compatibility">Death Note: {c.deathNoteCompatible?'compatível com a sentença':'investigação se converte em Exposto'}. Regra ficcional deste jogo.</small>
  </div></dialog>;
}
