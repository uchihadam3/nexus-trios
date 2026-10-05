import { ArrowUpRight, ArrowRight, Layers, Zap, Trophy, CircleHelp, Settings2, Download, ChevronRight } from 'lucide-react';
import { byId,characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import type { Profile, Run } from '../lib/storage';
interface Props {profile:Profile;run:Run|null;onPlay:()=>void;onContinue:()=>void;onAbandon:()=>void;onNavigate:(s:'characters'|'help'|'settings')=>void;onInstall:()=>void}
export function Home({profile,run,onPlay,onContinue,onAbandon,onNavigate,onInstall}:Props){
  const hasRun=run&&(run.stage==='draft'||run.stage==='battle'||(run.battle?.winner==='player'&&run.index<9));
  return <>
    <section className="home-hero">
      <div className="hero-copy"><div className="hero-kicker"><span className="live-dot"/> UNIVERSOS DIFERENTES. UM SÓ DESTINO.</div><h1>TRÊS LENDAS.<br/><span>UMA CONEXÃO.</span></h1><p>O poder está na combinação.<br/>Monte seu trio e conquiste dez confrontos<br className="desktop-break"/> em batalhas totalmente automáticas.</p>
        <button className="primary hero-cta" onClick={hasRun?onContinue:onPlay}>{hasRun?'Continuar jornada':'Montar meu trio'}<ArrowUpRight size={22}/></button>
        {hasRun&&<button className="abandon-campaign" onClick={onAbandon}>Desistir desta campanha e começar outra</button>}
        <div className="hero-footnote"><span>3 escolhas</span><i/> <span>10 confrontos</span><i/><span>Infinitas combinações</span></div>
      </div>
      <div className="hero-art" aria-label="Goku, Pikachu e Gojo: descubra sua combinação"><div className="orbital orbital-one"/><div className="orbital orbital-two"/><span className="art-coordinate">NXS / CONEXÃO 001</span>
        {['goku','pikachu','gojo'].map((id,i)=>{const c=byId[id];return <div className={`hero-card hero-card-${i}`} key={id} style={{'--character':c.color} as React.CSSProperties}><div className="hero-card-top"><span>0{i+1}</span><span>✦</span></div><Portrait character={c} className="hero-portrait"/><div className="hero-card-bottom"><span className="mini-label">{c.universe}</span><h3>{c.name}</h3><div>{c.skills.map(s=><span key={s.id}><SkillIcon type={s.icon} size={15} characterId={c.id} skillId={s.id}/></span>)}</div></div></div>;})}
        <div className="synergy-badge"><span className="live-dot"/> MELHORES JUNTOS <Zap size={13}/></div><span className="art-caption">ENCONTRE A SUA SINERGIA</span>
      </div>
    </section>
    <section className="game-principles" aria-label="A experiência"><article><span className="principle-number">01</span><Layers/><div><h3>Escolha com intenção</h3><p>{characters.length} personagens. Três oportunidades por escolha.</p></div></article><article><span className="principle-number">02</span><Zap/><div><h3>Veja a sinergia acontecer</h3><p>Habilidades conectadas mudam o rumo da luta.</p></div></article><article><span className="principle-number">03</span><Trophy/><div><h3>Chegue ao décimo confronto</h3><p>Seu trio contra desafios cada vez maiores.</p></div></article></section>
    <section className="home-bottom"><div className="journey-preview"><div className="section-heading"><div><span className="eyebrow">A JORNADA</span><h2>Do primeiro encontro à glória.</h2></div><span className="record">RECORDE <strong>{profile.best}<small>/10</small></strong></span></div><div className="milestones">{Array.from({length:10},(_,i)=><div className={i<profile.best?'complete':''} key={i}>{i===9?<Trophy size={17}/>:String(i+1).padStart(2,'0')}</div>)}</div><div className="journey-bottom"><span>{profile.journeys} jornadas · {profile.victories} equipes campeãs</span><button className="text-button" onClick={onPlay}>{hasRun?'Nova jornada':'Começar jornada'} <ArrowRight size={15}/></button></div></div>
      <div className="quick-links"><button onClick={()=>onNavigate('characters')}><span><Layers size={19}/>Conheça os personagens</span><ChevronRight size={16}/></button><button onClick={()=>onNavigate('help')}><span><CircleHelp size={19}/>Como jogar</span><ChevronRight size={16}/></button><button onClick={()=>onNavigate('settings')}><span><Settings2 size={19}/>Configurações</span><ChevronRight size={16}/></button><button onClick={onInstall}><span><Download size={19}/>Instalar o jogo</span><ChevronRight size={16}/></button></div>
    </section>
  </>;
}
