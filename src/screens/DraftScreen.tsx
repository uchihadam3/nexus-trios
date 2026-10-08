import { useState } from 'react';
import { ArrowRight,Shuffle,Plus,Check,Info,LogOut,Sparkles } from 'lucide-react';
import type { Draft } from '../engine/campaign';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { presentTrait } from '../engine/skill-descriptions';
import { identidadesDe,identidadesDoTrio,lacunasDoTrio,oQueAdiciona } from '../presentation/identities';
import { draftConnection } from '../presentation/draft-connections';

export function DraftScreen({draft,onPick,onSkip,onDetails,onStart,onAbandon}:{draft:Draft;onPick:(id:string)=>void;onSkip:()=>void;onDetails:(id:string)=>void;onStart:()=>void;onAbandon:()=>void}){
  const [focused,setFocused]=useState('');
  const full=draft.team.length===3,team=draft.team.map(id=>byId[id]);
  const identidadesDoMeuTrio=identidadesDoTrio(team),lacunas=lacunasDoTrio(team),candidates=full?draft.team:draft.candidates;
  const spotlight=byId[candidates.includes(focused)?focused:candidates[0]];
  const connection=spotlight&&!full?draftConnection(spotlight,team):null;
  const novidades=spotlight&&!full?oQueAdiciona(spotlight,team):[];
  return <section className="draft-screen">
    <div className="screen-title draft-intro"><span className="eyebrow">DRAFT · FORME SEU TRIO</span><h1>{full?'Trio completo. Arena liberada.':'Cada escolha muda a luta.'}</h1><p>{full?'Veja a combinação que você construiu e entre no primeiro confronto.':`Escolha ${draft.team.length+1} de 3. Compare funções, veja conexões reais e monte sua equipe.`}</p></div>
    <div className="draft-progress" aria-label={`Escolha ${Math.min(3,draft.team.length+1)} de 3`}>{Array.from({length:3},(_,i)=><div key={i} className={i<draft.team.length?'done':i===draft.team.length&&!full?'active':''}><span>{i<draft.team.length?<Check size={13}/>:i+1}</span><small>{i<draft.team.length?'ESCOLHIDO':i===draft.team.length&&!full?'ESCOLHA AGORA':'EM SEGUIDA'}</small></div>)}</div>
    <div className="team-slots draft-team">{Array.from({length:3},(_,i)=>{const c=team[i];return <div className={`team-slot ${c?'filled':''}`} key={i} style={c?{'--character':c.color} as React.CSSProperties:undefined}>{c?<><Portrait character={c} className="tiny"/><span>{c.name}</span><Check size={16}/></>:<><Plus size={20}/><span>Espaço {i+1}</span></>}</div>;})}</div>
    {spotlight&&!full&&<div className="draft-spotlight" style={{'--character':spotlight.color} as React.CSSProperties}><div className="draft-spotlight-art"><Portrait character={spotlight}/></div><div><span className="eyebrow">SE ENTRAR NO TRIO</span><h2>{spotlight.name}</h2><div className="role-chips">{identidadesDe(spotlight).map(x=><span key={x}>{x}</span>)}</div><p>{connection?<><Sparkles size={15}/> <b>BOA CONEXÃO</b> · {connection}</>:<>{novidades.length>0?<>Seu trio ganha {novidades.map(x=>`+ ${x}`).join(' ')}. </>:<>Reforça o que o trio já faz. </>}{spotlight.vulnerability}</>}</p></div></div>}
    {team.length>0&&<div className="team-kit"><strong>Seu trio já consegue</strong><div className="role-chips">{identidadesDoMeuTrio.map(x=><span key={x}>✓ {x}</span>)}</div>{lacunas.length>0&&<small>{lacunas.join(' · ')}.</small>}</div>}
    <div className="candidate-grid">{candidates.map((id,i)=>{const c=byId[id],trait=presentTrait(c.trait);return <article className={`candidate-card ${spotlight.id===id?'spotlighted':''}`} key={id} onPointerEnter={()=>setFocused(id)} onFocusCapture={()=>setFocused(id)} onPointerDown={()=>setFocused(id)} style={{'--character':c.color,'--candidate-order':i} as React.CSSProperties}>
      <button className="candidate-art" onClick={()=>onDetails(id)} aria-label={`Detalhes de ${c.name}`}><Portrait character={c}/><span className="candidate-universe">{c.universe}</span><span className="detail-dot"><Info size={17}/></span></button>
      <div className="candidate-body"><span className="candidate-index">OPÇÃO {i+1}</span><h2>{c.name}</h2><div className="role-chips">{identidadesDe(c).map(x=><span key={x}>{x}</span>)}</div><p>{c.idea}</p><small className="candidate-trait"><b>{c.trait.name}</b> · {trait.summary} · {trait.trigger}</small><small className="candidate-warning">{c.vulnerability}</small><div className="candidate-skills">{c.skills.map(s=><span title={s.name} key={s.id}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id}/></span>)}<button className="text-button" onClick={()=>onDetails(id)}>Ver ficha <ArrowRight size={14}/></button></div>{!full&&<button className="choose-button" onClick={()=>onPick(id)}>Adicionar ao trio <Plus size={17}/></button>}</div>
    </article>;})}</div>
    <div className="draft-actions">{full?<button className="primary" onClick={onStart}>Entrar na arena <ArrowRight size={20}/></button>:<><button className="secondary" onClick={onSkip} disabled={draft.skips===0}><Shuffle size={17}/> Trocar candidatos <span className="count-badge">{draft.skips} pulos</span></button><p>Os três pulos são compartilhados entre todas as escolhas.</p></>}<button className="draft-abandon" onClick={onAbandon}><LogOut size={15}/>Desistir da jornada</button></div>
  </section>;
}
