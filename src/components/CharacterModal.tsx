import { useEffect,useRef,useState,type CSSProperties } from 'react';
import { SeloDeEstrela } from './SeloDeEstrela';
import { X, HeartPulse, Gauge, Brain, Info, Sparkles, Swords, TriangleAlert, Zap, Hourglass, Snowflake, Target, Scissors, Bomb, TrendingDown, Turtle, Sword, Skull, Clock, Shuffle, Heart, Shield, Lock, Timer, BatteryCharging, ShieldPlus, HandHeart, Mountain, Rocket, Award, CircleCheck, Flame, ChevronLeft, type LucideIcon } from 'lucide-react';
import type { Character } from '../engine/types';
import { characters } from '../data/characters';
import { Portrait } from './Portrait';
import { unicaDe } from '../engine/unicas';
import { SkillIcon } from './Icon';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { ativaQuando,presentEffect,presentSkill,presentTrait,targetNames,textoDaIsca,textoDaResistencia,textoDoDespercebido,textoDoJeito,textoDoRenascer } from '../engine/skill-descriptions';
import { identidadesDe } from '../presentation/identities';
import { IdentityChips } from './IdentityChips';
import { ComTermos,TermoBotao } from './Termos';
import { termoPorId } from '../presentation/glossario';
import { pontoFraco,type TipoDeFraqueza } from '../data/ponto-fraco';
import { pontoForte,type TipoDeForca } from '../data/ponto-forte';
import { universoDaFicha } from '../data/equipes';
import { nomeDe, numero, t } from '../i18n/idioma';

const ICONE_DA_FRAQUEZA:Record<TipoDeFraqueza,LucideIcon>={cai:TrendingDown,golpe:Skull,rara:Hourglass,espera:Clock,preparo:Scissors,demora:Timer,lento:Turtle,dano:Sword,espalha:Shuffle,apanhar:Bomb};
const ICONE_DA_FORCA:Record<TipoDeForca,LucideIcon>={dano:Swords,nocaute:Skull,cura:Heart,escudo:Shield,controle:Lock,ritmo:Gauge,carga:BatteryCharging,corte:Scissors,reforco:ShieldPlus,reviver:HandHeart,aguenta:Mountain,agil:Sparkles,cedo:Rocket,rapido:Zap,equilibrado:Award};

export function intelligenceLabel(value:number){
  return t(value>=95?'Excepcional':value>=80?'Muito inteligente':value>=60?'Esperto':value>=40?'Comum':'Impulsivo');
}

/* A régua dos atributos é o elenco inteiro: a barra cheia é o maior do jogo. */
const VIDA_MAX=Math.max(...characters.map(c=>c.hp));
const INTERVALO_MIN=Math.min(...characters.map(c=>c.interval)),INTERVALO_MAX=Math.max(...characters.map(c=>c.interval));
const pct=(x:number)=>Math.round(Math.max(.06,Math.min(1,x))*100);

/*
 * A ficha do lutador, no mesmo desenho da ficha da batalha (pedido do jogador:
 * "tem que deixar a ficha do personagem igual da batalha, que da batalha tá
 * bonita"). Mesmas peças de src/components/BattleInspector.tsx e
 * inspetor-v2.css: o retrato no anel, as barras, as três habilidades em botões
 * que abrem a ficha da habilidade (com a fileira para trocar e voltar), e os
 * cartões com selo colorido. Aqui não há luta: os anéis ficam cheios e as barras
 * medem o personagem contra o elenco inteiro.
 */
export function CharacterModal({character:c,onClose}:{character:Character;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null);
  const [hab,setHab]=useState(-1);
  useEffect(()=>{ref.current?.showModal();return()=>ref.current?.close();},[]);
  useEffect(()=>{ref.current?.scrollTo?.({top:0});},[hab]);
  return <dialog ref={ref} className="character-modal ficha-v3" onCancel={onClose} onClick={e=>{if(e.target===e.currentTarget)onClose();}}>
    <div key={hab} className="modal-inner bi2" style={{'--cor':c.color} as CSSProperties}>
      <button className="bi2-fechar" aria-label={t('Fechar detalhes')} onClick={onClose}><X size={18}/></button>
      {hab>=0?<FichaDaHabilidade c={c} i={hab} onSelect={setHab}/>:<FichaDoLutador c={c} onSelect={setHab}/>}
    </div>
  </dialog>;
}

function FichaDoLutador({c,onSelect}:{c:Character;onSelect:(i:number)=>void}){
  const traco=presentTrait(c.trait),unica=unicaDe(c.id),intelligence=c.intelligence??50,quando=ativaQuando(c.trait,c.name);
  const extras=[c.renascer&&textoDoRenascer(c.renascer),c.ultimaResistencia&&textoDaResistencia(c.ultimaResistencia),c.despercebido&&textoDoDespercebido(),c.isca&&textoDaIsca(c.isca)].filter((x):x is string=>!!x);
  const basico=c.basic.effects.map(effect=>presentEffect(effect,c.basic.target)).join(' · ');
  const fracaoDoRitmo=1-(c.interval-INTERVALO_MIN)/(INTERVALO_MAX-INTERVALO_MIN)*.9;
  return <>
    <header className="bi2-topo">
      <div className="bi2-retrato" style={{'--p':100} as CSSProperties}><Portrait character={c}/></div>
      <div className="bi2-nome">
        <small>{t(universoDaFicha(c))}</small>
        <h2>{nomeDe(c)}</h2>
        <SeloDeEstrela id={c.id} naFicha/>
        <p className="fv3-ideia">{t(c.idea)}</p>
      </div>
    </header>
    <IdentityChips ids={identidadesDe(c)}/>
    <div className="fv3-barras">
      <div className="bi2-barra vida" style={{'--p':pct(c.hp/VIDA_MAX)} as CSSProperties}><i/><span><HeartPulse size={13}/>{t('Vida')}<b>{numero(c.hp)}</b></span></div>
      <div className="bi2-barra ritmo" style={{'--p':pct(fracaoDoRitmo)} as CSSProperties}><i/><span><Gauge size={13}/>{t('Ataca a cada')}<b>{numero(c.interval)} s</b></span></div>
      <div className="bi2-barra mente" style={{'--p':pct(intelligence/100)} as CSSProperties}><i/><span><Brain size={13}/>{t('Inteligência')}<b>{intelligence}</b>{intelligenceLabel(intelligence)}</span></div>
    </div>
    <div className="bi2-habs">{c.skills.map((s,i)=><button key={s.id} className="bi2-hab" style={{'--i':i} as CSSProperties} onClick={()=>onSelect(i)}>
      <span className="bi2-anel" style={{'--p':100} as CSSProperties}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={24}/></span>
      <b>{t(s.name)}</b><small>{t('HABILIDADE {n}',{n:i+1})}</small>
    </button>)}</div>
    <div className="bi2-cartoes">
      {c.id==='light'&&<section className="bi2-cartao aviso" style={{'--i':3} as CSSProperties}>
        <span className="bi2-selo"><Info size={12}/>{t('Como funciona a investigação')}</span>
        <p>{t('Ao chegar a 100 Investigação em um rival, Light descobre se o rival é vulnerável ou imune à Death Note. A descoberta fica visível na batalha.')}</p>
      </section>}
      {unica&&<section className="bi2-cartao unica" style={{'--i':3} as CSSProperties}>
        <span className="bi2-selo"><Sparkles size={12}/><TermoBotao termo={termoPorId['mecanica-unica']!}>{t('Mecânica única')}</TermoBotao> · {t('só {nome} tem',{nome:nomeDe(c)})}</span>
        <b>{t(unica.nome)}</b><p><ComTermos texto={t(unica.texto)}/></p>
      </section>}
      <section className="bi2-cartao traco" style={{'--i':4} as CSSProperties}>
        <span className="bi2-selo"><Flame size={12}/><TermoBotao termo={termoPorId.traco!}>{t('Traço')}</TermoBotao></span>
        <b>{t(c.trait.name)}</b><p><ComTermos texto={`${traco.effects.join(' · ')}.`}/></p><p className="ativa-quando"><u>{quando.rotulo}</u> <ComTermos texto={`${quando.resto}.`}/></p>
        {extras.length>0&&<ul className="bi2-extras">{extras.map((x,i)=><li key={i}><ComTermos texto={x+'.'}/></li>)}</ul>}
      </section>
      <section className="bi2-cartao basico" style={{'--i':5} as CSSProperties}>
        <span className="bi2-selo"><Swords size={12}/><TermoBotao termo={termoPorId['ataque-basico']!}>{t('Ataque básico')}</TermoBotao> · {t(targetNames[c.basic.target])}</span>
        <b>{t(c.basic.name)}</b><p><ComTermos texto={basico+'.'}/>{c.basic.jeito&&<> <ComTermos texto={textoDoJeito(c.basic.jeito)+'.'}/></>}</p>
      </section>
      {/* o que ele faz melhor que o elenco, e com qual habilidade */}
      <section className="bi2-cartao forte" style={{'--i':6} as CSSProperties} aria-label={t('Ponto forte')}>
        <span className="bi2-selo"><CircleCheck size={12}/>{t('Ponto forte')}</span>
        <ul className="fv3-pontos">{pontoForte(c).map(x=>{const Icone=ICONE_DA_FORCA[x.tipo];return <li key={x.tipo}><span><Icone size={14} strokeWidth={2.4}/>{t(x.rotulo)}</span><small>{t(x.motivo)}</small></li>;})}</ul>
      </section>
      {/* curto: o que ele não consegue fazer, e por quê em poucas palavras */}
      <section className="bi2-cartao fraco" style={{'--i':7} as CSSProperties} aria-label={t('Ponto fraco')}>
        <span className="bi2-selo"><TriangleAlert size={12}/>{t('Ponto fraco')}</span>
        <ul className="fv3-pontos">{pontoFraco(c).map(x=>{const Icone=ICONE_DA_FRAQUEZA[x.tipo];return <li key={x.tipo}><span><Icone size={14} strokeWidth={2.4}/>{t(x.rotulo)}</span><small>{t(x.motivo)}</small></li>;})}</ul>
      </section>
    </div>
  </>;
}

function FichaDaHabilidade({c,i,onSelect}:{c:Character;i:number;onSelect:(i:number)=>void}){
  const skill=c.skills[i],p=presentSkill(skill);
  return <>
    <header className="bi2-topo hab">
      <span className="bi2-anel grande" style={{'--p':100} as CSSProperties}><SkillIcon type={skill.icon} characterId={c.id} skillId={skill.id} size={40}/></span>
      <div className="bi2-nome">
        <small>{nomeDe(c)} · {t('Habilidade {n}',{n:i+1})}</small>
        <h2>{t(skill.name)}</h2>
        {p.mostrarAlvo&&<span className="bi2-situacao"><Target size={13}/>{p.target}</span>}
      </div>
    </header>
    <section className="bi2-cartao faz" style={{'--i':0} as CSSProperties}>
      <span className="bi2-selo"><Zap size={12}/>{t('O que faz')}</span>
      <EfeitosAgrupados grupos={p.grupos}/>
    </section>
    <div className="bi2-numeros">
      <span style={{'--i':1} as CSSProperties}><Hourglass size={15}/><TermoBotao termo={termoPorId.preparo!}/><b>{p.preparation}</b></span>
      <span style={{'--i':2} as CSSProperties}><Snowflake size={15}/><TermoBotao termo={termoPorId.resfriamento!}/><b>{p.cooldown}</b></span>
    </div>
    <section className="bi2-cartao carga" style={{'--i':3} as CSSProperties}>
      <span className="bi2-selo"><Flame size={12}/><TermoBotao termo={termoPorId.carga!}>{t('Como enche')}</TermoBotao></span>
      <div className="bi2-fontes">{p.charge.map((x,k)=><span key={k}><ComTermos texto={x}/></span>)}</div>
      {p.useWhen&&!/^ficar pronta$/i.test(p.useWhen)&&<p className="bi2-quando"><TermoBotao termo={termoPorId['usa-quando']!}/> <ComTermos texto={p.useWhen}/></p>}
    </section>
    <nav className="bi2-trilha" aria-label={t('Trocar de ficha')}>
      <button className="bi2-voltar" onClick={()=>onSelect(-1)} aria-label={t('Voltar para {nome}',{nome:nomeDe(c)})}><ChevronLeft size={16}/><span className="bi2-mini"><Portrait character={c}/></span></button>
      {c.skills.map((s,k)=><button key={s.id} className={`bi2-aba ${k===i?'ativa':''}`} onClick={()=>onSelect(k)} aria-label={t(s.name)} aria-current={k===i}>
        <span className="bi2-anel" style={{'--p':100} as CSSProperties}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={20}/></span>
      </button>)}
    </nav>
  </>;
}
