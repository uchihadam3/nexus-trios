import { ArrowRight,RotateCcw,Shield,Swords,Zap,Home } from 'lucide-react';
import type { Run } from '../lib/storage';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { AuxIcon } from '../components/Icon';
export function ResultScreen({run,onNext,onRestart,onAbandon,onHome,auto,onAuto}:{run:Run;onNext:()=>void;onRestart:()=>void;onAbandon:()=>void;onHome:()=>void;auto:boolean;onAuto:(v:boolean)=>void}){
  const b=run.battle!,won=b.winner==='player',champion=won&&run.index===9;
  const players=b.fighters.filter(f=>f.side==='player');
  const damage=[...players].sort((a,z)=>z.stats.damage-a.stats.damage)[0],protection=[...players].sort((a,z)=>(z.stats.protection+z.stats.healing)-(a.stats.protection+a.stats.healing))[0],control=[...players].sort((a,z)=>z.stats.interrupts-a.stats.interrupts)[0];
  return <section className={`result-screen ${champion?'champion':''}`}><div className="result-medal"><AuxIcon id={won?'victory':'defeat'} size={52}/></div><span className="eyebrow">{champion?'DEZ CONFRONTOS. UMA EQUIPE CAMPEÃ.':`CONFRONTO ${String(run.index+1).padStart(2,'0')} / 10`}</span><h1>{champion?'A conexão perfeita.':won?'Vitória do seu trio.':'Toda conexão ensina.'}</h1><p>{champion?'Vocês atravessaram todos os desafios. Agora, quais lendas vão se encontrar?':won?`${run.encounters[run.index].name} concluído. Próximo desafio à frente.`:`A jornada terminou na batalha ${run.index+1}. Descubra outra combinação e tente de novo.`}</p><div className="result-reason">{b.reason} · {Math.round(b.time)} s</div>
    <div className="winning-trio">{run.team.map(id=><div key={id}><Portrait character={byId[id]}/><h3>{byId[id].name}</h3></div>)}</div>
    <div className="highlights"><article><Swords size={21}/><span>MAIOR IMPACTO</span><h3>{byId[damage.characterId].name}</h3><p>{Math.round(damage.stats.damage)} de dano efetivo</p></article><article><Shield size={21}/><span>APOIO AO TRIO</span><h3>{byId[protection.characterId].name}</h3><p>{Math.round(protection.stats.protection+protection.stats.healing)} de proteção e cura úteis</p></article><article><Zap size={21}/><span>{control.stats.interrupts?'PLANOS INTERROMPIDOS':'HABILIDADES EM AÇÃO'}</span><h3>{byId[control.characterId].name}</h3><p>{control.stats.interrupts?`${control.stats.interrupts} interrupções e atrasos`:`${players.reduce((n,f)=>n+f.stats.skills,0)} habilidades usadas pelo trio`}</p></article></div>
    {won&&<div className="defeated-line"><span>TRIO SUPERADO</span>{run.encounters[run.index].team.map(id=>byId[id].name).join(' · ')}</div>}
    <div className="result-actions">{won&&!champion?<><button className="primary" onClick={onNext}>Próxima batalha <ArrowRight size={19}/></button><button className="danger" onClick={onAbandon}>Desistir da campanha</button></>:<button className="primary" onClick={onRestart}>Montar outro trio <RotateCcw size={19}/></button>}<button className="secondary" onClick={onHome}><Home size={17}/>Início</button></div>
    {won&&!champion&&<label className="auto-label result-auto"><input type="checkbox" checked={auto} onChange={e=>onAuto(e.target.checked)}/>{auto?'Próxima batalha em instantes · desmarque para parar':'Avançar automaticamente entre batalhas'}</label>}
  </section>;
}
