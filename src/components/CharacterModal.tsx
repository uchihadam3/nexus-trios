import { useEffect,useRef } from 'react';
import { X,Activity,Timer,Info,Brain } from 'lucide-react';
import type { Character } from '../engine/types';
import { Portrait } from './Portrait';
import { SkillIcon } from './Icon';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { presentEffect,presentSkill,presentTrait,targetNames } from '../engine/skill-descriptions';
import { identidadesDe } from '../presentation/identities';
import { IdentityChips } from './IdentityChips';

export function intelligenceLabel(value:number){
  return value>=95?'Excepcional':value>=80?'Muito inteligente':value>=60?'Esperto':value>=40?'Comum':'Impulsivo';
}
function EnergiaGuardada({c}:{c:Character}){
  const solta=c.skills.find(s=>s.effects.some(e=>e.kind==='release'));
  const guardas=[{nome:'o traço',efeitos:c.trait.effects},{nome:'o ataque básico',efeitos:c.basic.effects},...c.skills.map(s=>({nome:s.name,efeitos:s.effects}))].filter(x=>x.efeitos.some(e=>e.kind==='store'));
  if(!solta||!guardas.length)return null;
  const release=solta.effects.find(e=>e.kind==='release'),teto=Math.max(...guardas.flatMap(g=>g.efeitos.map(e=>e.kind==='store'?e.cap:0)));
  if(!release||release.kind!=='release')return null;
  const n=(x:number)=>x.toLocaleString('pt-BR');
  return <div className="vulnerability energia-guardada"><Info size={17}/><p><strong>Como funciona a energia guardada</strong><br/>
    {c.name} enche um estoque de energia com {guardas.map(g=>g.nome).join(', ').replace(/, ([^,]*)$/,' e $1')} (máximo {n(teto)}). Ela não faz nada sozinha: quando usa <b>{solta.name}</b>, solta tudo de uma vez — a energia ×{n(release.multiplier)} vira dano, dividido entre os inimigos vivos — e o estoque volta a zero.
    <br/><small>Exemplo: com {n(teto)} guardados, {solta.name} causa {n(Math.round(teto*release.multiplier))} de dano.</small></p></div>;
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
      * encontrava nada. Cada etiqueta é tocável e abre o cartão que explica o que ela faz.
      */}
    <IdentityChips ids={identidadesDe(c)}/>
    <div className="character-stats"><span><Activity size={16}/> {c.hp} Vida</span><span><Timer size={16}/> Ataca a cada {c.interval.toLocaleString('pt-BR')} s</span><span><Brain size={16}/> Inteligência {intelligence}/100 · {intelligenceLabel(intelligence)}</span></div>
    {c.id==='light'&&<div className="vulnerability"><Info size={17}/><p><strong>Como funciona a investigação</strong><br/>Ao chegar a 100 Investigação em um inimigo, Light descobre se ele é vulnerável ou imune à Death Note. A descoberta fica visível na batalha.</p></div>}
    {/*
      * "Guarda 34 de energia" não diz nada sozinho: para quê? A energia é um
      * estoque escondido que só vira dano quando a habilidade de soltar sai.
      */}
    <EnergiaGuardada c={c}/>
    <div className="sheet-section trait"><span className="eyebrow">TRAÇO</span><h3>{c.trait.name}</h3><div className="effect-chips">{trait.effects.map((effect,i)=><span key={i}>{effect}</span>)}</div><small>{trait.quando}</small></div>
    <div className="sheet-section"><span className="eyebrow">ATAQUE BÁSICO · {targetNames[c.basic.target]}</span><div className="effect-chips">{c.basic.effects.map((effect,i)=><span key={i}>{presentEffect(effect,c.basic.target)}</span>)}</div></div>
    <div className="detail-skills">{c.skills.map((s,i)=>{const p=presentSkill(s);return <article key={s.id}><span className="skill-static"><SkillIcon type={s.icon} characterId={c.id} skillId={s.id}/></span><div><span className="eyebrow">HABILIDADE {i+1}</span><h3>{s.name}</h3><EfeitosAgrupados grupos={p.grupos}/>{p.mostrarAlvo&&<div className="sheet-detail"><b>Alvo</b> {p.target}</div>}<div className="sheet-detail"><b>Carga</b> {p.charge.join(' · ')}</div><div className="sheet-detail"><b>Usa quando</b> {p.useWhen}</div><div className="sheet-detail"><b>Preparo</b> {p.preparation} <b>Resfriamento</b> {p.cooldown}</div></div></article>;})}</div>
    <div className="vulnerability"><Info size={17}/><p><strong>Ponto fraco</strong><br/>{c.vulnerability}</p></div>
  </div></dialog>;
}
