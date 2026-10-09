import { useEffect,useRef,type CSSProperties } from 'react';
import { X,HeartPulse,Gauge,Brain,Info,Sparkles,Swords,TriangleAlert,Zap,Hourglass,Snowflake,Target,Scissors,Bomb,Users,ShieldPlus,FastForward,Flame,Lock,Mountain,Clock,type LucideIcon } from 'lucide-react';
import type { Character } from '../engine/types';
import { characters } from '../data/characters';
import { Portrait } from './Portrait';
import { SkillIcon } from './Icon';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { presentEffect,presentSkill,presentTrait,targetNames,textoDaResistencia,textoDoRenascer } from '../engine/skill-descriptions';
import { identidadesDe } from '../presentation/identities';
import { IdentityChips } from './IdentityChips';
import { ComTermos,TermoBotao } from './Termos';
import { termoPorId } from '../presentation/glossario';
import { pontoFraco,type TipoDeFraqueza } from '../data/ponto-fraco';

const ICONE_DA_FRAQUEZA:Record<TipoDeFraqueza,LucideIcon>={interrupcao:Scissors,explosao:Bomb,area:Users,cura:ShieldPlus,rapidos:FastForward,continuo:Flame,controle:Lock,tanques:Mountain,longa:Hourglass,momento:Clock,apanhar:Bomb};

export function intelligenceLabel(value:number){
  return value>=95?'Excepcional':value>=80?'Muito inteligente':value>=60?'Esperto':value>=40?'Comum':'Impulsivo';
}

/* A régua dos atributos é o elenco inteiro: a barra cheia é o maior do jogo. */
const VIDA_MAX=Math.max(...characters.map(c=>c.hp));
const INTERVALO_MIN=Math.min(...characters.map(c=>c.interval)),INTERVALO_MAX=Math.max(...characters.map(c=>c.interval));

function Atributo({icone,nome,valor,fracao,cor}:{icone:React.ReactNode;nome:string;valor:string;fracao:number;cor:string}){
  return <div className="fv-atributo" style={{'--attr':cor,'--fill':`${Math.round(Math.max(.06,Math.min(1,fracao))*100)}%`} as CSSProperties}>
    <span className="fv-attr-icone">{icone}</span><span className="fv-attr-nome">{nome}</span><b>{valor}</b><i aria-hidden><em/></i>
  </div>;
}

/*
 * A ficha do lutador (remake).
 *
 * Topo com retrato grande e brilho na cor do personagem, as etiquetas, três
 * barras de atributo medidas contra o elenco inteiro, o traço num cartão
 * dourado ("sempre ativo"), o básico numa linha, as habilidades em cartões
 * com ícone grande e selos de Carga, Preparo e Resfriamento, e o ponto fraco
 * num cartão vermelho. Os termos do jogo continuam tocáveis.
 */
export function CharacterModal({character:c,onClose}:{character:Character;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null),trait=presentTrait(c.trait);
  useEffect(()=>{ref.current?.showModal();return()=>ref.current?.close();},[]);
  const intelligence=c.intelligence??50;
  return <dialog ref={ref} className="character-modal ficha-v2" onCancel={onClose} onClick={e=>{if(e.target===e.currentTarget)onClose();}}><div className="modal-inner character-sheet" style={{'--character':c.color} as CSSProperties}>
    <button className="icon-button modal-close" aria-label="Fechar detalhes" onClick={onClose}><X size={20}/></button>
    <header className="fv-hero">
      <div className="fv-retrato"><Portrait character={c}/></div>
      <div className="fv-titulo"><span className="fv-universo">{c.universe}</span><h2>{c.name}</h2><p>{c.idea}</p></div>
    </header>
    <IdentityChips ids={identidadesDe(c)}/>
    <div className="fv-atributos">
      <Atributo icone={<HeartPulse size={15}/>} nome="Vida" valor={c.hp.toLocaleString('pt-BR')} fracao={c.hp/VIDA_MAX} cor="#86e3a8"/>
      <Atributo icone={<Gauge size={15}/>} nome="Velocidade" valor={`ataca a cada ${c.interval.toLocaleString('pt-BR')} s`} fracao={1-(c.interval-INTERVALO_MIN)/(INTERVALO_MAX-INTERVALO_MIN)*.9} cor="#ffd36b"/>
      <Atributo icone={<Brain size={15}/>} nome="Inteligência" valor={`${intelligence} · ${intelligenceLabel(intelligence)}`} fracao={intelligence/100} cor="#8fd3ff"/>
    </div>
    {c.id==='light'&&<div className="fv-aviso"><Info size={17}/><p><strong>Como funciona a investigação</strong><br/>Ao chegar a 100 Investigação em um inimigo, Light descobre se ele é vulnerável ou imune à Death Note. A descoberta fica visível na batalha.</p></div>}

    <section className="fv-traco">
      <span className="fv-selo"><Sparkles size={13}/>TRAÇO · SEMPRE ATIVO</span>
      <h3>{c.trait.name}</h3>
      <div className="fv-chips">{trait.effects.map((effect,i)=><span key={i}><ComTermos texto={effect}/></span>)}{c.renascer&&<span className="fv-renasce"><ComTermos texto={textoDoRenascer(c.renascer)}/></span>}{c.ultimaResistencia&&<span className="fv-renasce"><ComTermos texto={textoDaResistencia(c.ultimaResistencia)}/></span>}</div>
      <small>{trait.quando}</small>
    </section>

    <section className="fv-basico">
      <span className="fv-selo"><Swords size={13}/>ATAQUE BÁSICO · {targetNames[c.basic.target]}</span>
      <div className="fv-chips">{c.basic.effects.map((effect,i)=><span key={i}><ComTermos texto={presentEffect(effect,c.basic.target)}/></span>)}</div>
    </section>

    <div className="fv-habilidades">{c.skills.map((s,i)=>{const p=presentSkill(s);return <article key={s.id} className="fv-habilidade">
      <header><span className="fv-icone"><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={52}/></span><div><span className="fv-selo">HABILIDADE {i+1}</span><h3>{s.name}</h3></div></header>
      <EfeitosAgrupados grupos={p.grupos}/>
      {p.mostrarAlvo&&<div className="fv-regra"><Target size={13}/><b>Alvo</b> {p.target}</div>}
      <div className="fv-regras">
        <div className="fv-regra"><Zap size={14}/><b><TermoBotao termo={termoPorId.carga!}/></b><span>{p.charge.join(' · ')}</span></div>
        <div className="fv-regra"><Target size={14}/><b><TermoBotao termo={termoPorId['usa-quando']!}/></b><span>{p.useWhen}</span></div>
        <div className="fv-pilulas"><span><Hourglass size={13}/><TermoBotao termo={termoPorId.preparo!}/> <b>{p.preparation}</b></span><span><Snowflake size={13}/><TermoBotao termo={termoPorId.resfriamento!}/> <b>{p.cooldown}</b></span></div>
      </div>
    </article>;})}</div>

    {/* curto: contra o quê ele perde, e por quê em poucas palavras */}
    <section className="fv-fraco" aria-label="Ponto fraco">
      <span className="fv-selo"><TriangleAlert size={13}/>PONTO FRACO</span>
      <ul>{pontoFraco(c.vulnerability,c).map(x=>{const Icone=ICONE_DA_FRAQUEZA[x.tipo];return <li key={x.contra}>
        <span className="fv-fraco-contra"><Icone size={15} strokeWidth={2.4}/>{x.contra}</span>
        <span className="fv-fraco-motivo">{x.motivo}</span>
      </li>;})}</ul>
    </section>
  </div></dialog>;
}
