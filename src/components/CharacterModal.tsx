import { useEffect,useRef } from 'react';
import { X,Activity,Timer,Info,Brain } from 'lucide-react';
import type { Character } from '../engine/types';
import { Portrait } from './Portrait';
import { SkillIcon } from './Icon';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { presentEffect,presentSkill,presentTrait,targetNames } from '../engine/skill-descriptions';
import { explicacaoDaIdentidade,identidadesDe } from '../presentation/identities';

export function intelligenceLabel(value:number){
  return value>=95?'Excepcional':value>=80?'Muito inteligente':value>=60?'Esperto':value>=40?'Comum':'Impulsivo';
}
export function CharacterModal({character:c,onClose}:{character:Character;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null),trait=presentTrait(c.trait);
  useEffect(()=>{ref.current?.showModal();return()=>ref.current?.close();},[]);
  const intelligence=c.intelligence??50;
  return <dialog ref={ref} className="character-modal" onCancel={onClose} onClick={e=>{if(e.target===e.currentTarget)onClose();}}><div className="modal-inner character-sheet">
    <button className="icon-button modal-close" aria-label="Fechar detalhes" onClick={onClose}><X size={20}/></button>
    <div className="modal-character" style={{'--character':c.color} as React.CSSProperties}><Portrait character={c}/><div><span className="eyebrow">{c.universe}</span><h2>{c.name}</h2><p>{c.idea}</p></div></div>
    {/*
      * As identidades públicas, com o que cada uma quer dizer.
      *
      * A ficha era o único lugar do jogo que não as mostrava — o jogador via
      * as etiquetas no Draft e no catálogo, abria a ficha para entender, e não
      * encontrava nada. O `title` carrega a explicação para quem passa o mouse,
      * e ela está escrita por extenso no Como Jogar.
      */}
    <div className="identity-chips">{identidadesDe(c).map(x=><span key={x} title={explicacaoDaIdentidade[x]}>{x}</span>)}</div>
    <div className="character-stats"><span><Activity size={16}/> {c.hp} Vida</span><span><Timer size={16}/> Ataca a cada {c.interval.toLocaleString('pt-BR')} s</span><span><Brain size={16}/> Inteligência {intelligence}/100 · {intelligenceLabel(intelligence)}</span></div>
    {c.id==='light'&&<div className="vulnerability"><Info size={17}/><p><strong>Como funciona a investigação</strong><br/>Ao chegar a 100 Investigação em um inimigo, Light descobre se ele é vulnerável ou imune à Death Note. A descoberta fica visível na batalha.</p></div>}
    <div className="sheet-section trait"><span className="eyebrow">TRAÇO</span><h3>{c.trait.name}</h3><div className="effect-chips">{trait.effects.map((effect,i)=><span key={i}>{effect}</span>)}</div><small>{trait.quando}</small></div>
    <div className="sheet-section"><span className="eyebrow">ATAQUE BÁSICO · {targetNames[c.basic.target]}</span><div className="effect-chips">{c.basic.effects.map((effect,i)=><span key={i}>{presentEffect(effect,c.basic.target)}</span>)}</div></div>
    <div className="detail-skills">{c.skills.map((s,i)=>{const p=presentSkill(s);return <article key={s.id}><span className="skill-static"><SkillIcon type={s.icon} characterId={c.id} skillId={s.id}/></span><div><span className="eyebrow">HABILIDADE {i+1}</span><h3>{s.name}</h3><EfeitosAgrupados grupos={p.grupos}/>{p.mostrarAlvo&&<div className="sheet-detail"><b>Alvo</b> {p.target}</div>}<div className="sheet-detail"><b>Carga</b> {p.charge.join(' · ')}</div><div className="sheet-detail"><b>Usa quando</b> {p.useWhen}</div><div className="sheet-detail"><b>Preparo</b> {p.preparation} <b>Resfriamento</b> {p.cooldown}</div></div></article>;})}</div>
    <div className="vulnerability"><Info size={17}/><p><strong>Ponto de atenção</strong><br/>{c.vulnerability}</p></div>
  </div></dialog>;
}
