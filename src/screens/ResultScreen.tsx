import { ArrowRight,RotateCcw,Shield,Swords,Zap,Home } from 'lucide-react';
import type { Run } from '../lib/storage';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { AuxIcon } from '../components/Icon';
import { summarizeBattle,summarizeRun } from '../engine/run-summary';
export function ResultScreen({run,onNext,onRestart,onAbandon,onHome,auto,onAuto}:{run:Run;onNext:()=>void;onRestart:()=>void;onAbandon:()=>void;onHome:()=>void;auto:boolean;onAuto:(v:boolean)=>void}){
  const b=run.battle!,won=b.winner==='player',champion=won&&run.index===9;
  const journey=champion||!won?summarizeRun(run.summaries?.length?run.summaries:[summarizeBattle(run.index,b)]):null;
  const fmt=(value:number)=>Math.round(value).toLocaleString('pt-BR');
  const fighterTotals=run.team.map(id=>({id,stats:journey?.battles.flatMap(battle=>battle.fighters).filter(f=>f.characterId===id).reduce((sum,f)=>({damage:sum.damage+f.damage,healing:sum.healing+f.healing,protection:sum.protection+f.protection,interrupts:sum.interrupts+f.interrupts,kills:sum.kills+f.kills}),{damage:0,healing:0,protection:0,interrupts:0,kills:0})}));
  const nameFor=(uid:string)=>byId[run.team[Number(uid.split('-')[1])]]?.name??'Aliado';
  const players=b.fighters.filter(f=>f.side==='player');
  const damage=[...players].sort((a,z)=>z.stats.damage-a.stats.damage)[0],protection=[...players].sort((a,z)=>(z.stats.protection+z.stats.healing)-(a.stats.protection+a.stats.healing))[0],control=[...players].sort((a,z)=>z.stats.interrupts-a.stats.interrupts)[0];
  return <section className={`result-screen ${champion?'champion':''}`}><div className="result-medal"><AuxIcon id={won?'victory':'defeat'} size={52}/></div><span className="eyebrow">{champion?'DEZ CONFRONTOS. UM TRIO CAMPEÃO.':`CONFRONTO ${String(run.index+1).padStart(2,'0')} / 10`}</span><h1>{champion?'Trio campeão!':won?'VITÓRIA':'DERROTA'}</h1><p>{champion?'Vocês venceram os dez confrontos.':won?`${run.encounters[run.index].name} superado. Próximo desafio à frente.`:`Seu trio saiu da luta no confronto ${run.index+1}. Tente uma combinação diferente.`}</p><div className="result-reason">A luta terminou quando um trio inteiro ficou fora de combate.</div>
    <div className="winning-trio">{run.team.map(id=><div key={id}><Portrait character={byId[id]}/><h3>{byId[id].name}</h3></div>)}</div>
    <div className="highlights"><article><Swords size={21}/><span>MAIOR DANO</span><h3>{byId[damage.characterId].name}</h3><p>{fmt(damage.stats.damage)} de dano</p></article>{protection.stats.protection+protection.stats.healing>0&&<article><Shield size={21}/><span>MAIOR APOIO</span><h3>{byId[protection.characterId].name}</h3><p>{fmt(protection.stats.protection)} de dano bloqueado · {fmt(protection.stats.healing)} de cura</p></article>}{control.stats.interrupts>0&&<article><Zap size={21}/><span>PREPAROS INTERROMPIDOS</span><h3>{byId[control.characterId].name}</h3><p>{control.stats.interrupts} interrupções ou atrasos</p></article>}</div>
    {won&&<div className="defeated-line"><span>TRIO SUPERADO</span>{run.encounters[run.index].team.map(id=>byId[id].name).join(' · ')}</div>}
    {journey&&<section className="journey-summary" aria-label="Resumo da jornada">
      <div className="journey-score"><div><small>JORNADA {champion?'CONCLUÍDA':'ENCERRADA'}</small><strong>{journey.won} de 10 vitórias</strong></div><div><small>PONTUAÇÃO</small><strong>{fmt(journey.score)}</strong></div><div className="journey-rank"><small>DESEMPENHO</small><strong>{journey.rank}</strong></div></div>
      <div className="journey-metrics"><span><b>{fmt(journey.damage)}</b> dano</span><span><b>{fmt(journey.healing)}</b> cura</span><span><b>{fmt(journey.protection)}</b> dano bloqueado</span><span><b>{journey.interrupts}</b> interrupções</span><span><b>{journey.kills}</b> eliminações</span></div>
      <h2>O que cada um trouxe</h2><div className="journey-contributors">{fighterTotals.map(({id,stats})=><article key={id}><strong>{byId[id].name}</strong><span>{fmt(stats?.damage??0)} dano · {fmt((stats?.healing??0)+(stats?.protection??0))} apoio</span><small>{stats?.interrupts??0} interrupções · {stats?.kills??0} eliminações</small></article>)}</div>
      <h2>Conexões e aprendizados</h2><div className="journey-lessons">{journey.topSynergy&&<p><b>{nameFor(journey.topSynergy.source)} ajudou {nameFor(journey.topSynergy.target)}</b> a deixar habilidades prontas {journey.topSynergy.count} vezes.</p>}{journey.lessons.filter(line=>!journey.topSynergy||!line.startsWith('A ligação mais frequente')).slice(0,2).map(line=><p key={line}>{line}</p>)}</div>
      <h2>Os encontros</h2><ol className="journey-battles">{journey.battles.map(battle=><li key={battle.index} className={battle.won?'won':'lost'}><span>{String(battle.index+1).padStart(2,'0')}</span><strong>{battle.won?'Vitória':'Derrota'} · {battle.enemies.map(id=>byId[id].name).join(', ')}</strong><small>{battle.survivors} do seu trio permaneceram na luta</small></li>)}</ol>
    </section>}
    <div className="result-actions">{won&&!champion?<><button className="primary" onClick={onNext}>Próxima batalha <ArrowRight size={19}/></button><button className="danger" onClick={onAbandon}>Desistir da jornada</button></>:<button className="primary" onClick={onRestart}>Montar outro trio <RotateCcw size={19}/></button>}<button className="secondary" onClick={onHome}><Home size={17}/>Início</button></div>
    {won&&!champion&&<label className="auto-label result-auto"><input type="checkbox" checked={auto} onChange={e=>onAuto(e.target.checked)}/>{auto?'Próxima batalha em instantes · desmarque para parar':'Avançar automaticamente entre batalhas'}</label>}
  </section>;
}
