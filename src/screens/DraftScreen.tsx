import { ArrowRight, Shuffle, Plus, Check, Info, LogOut } from 'lucide-react';
import type { Draft } from '../engine/campaign';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { presentTrait } from '../engine/skill-descriptions';
import { rolesFor,roleOrder } from '../presentation/roles';
export function DraftScreen({draft,onPick,onSkip,onDetails,onStart,onAbandon}:{draft:Draft;onPick:(id:string)=>void;onSkip:()=>void;onDetails:(id:string)=>void;onStart:()=>void;onAbandon:()=>void}){
 const full=draft.team.length===3;
 const teamRoles=draft.team.flatMap(id=>rolesFor(byId[id]));
 return <section className="draft-screen"><div className="screen-title"><span className="eyebrow">MONTE SUA CONEXÃO</span><h1>{full?'Seu trio está pronto.':`Quem entra na equipe?`}</h1><p>{full?'As combinações estão feitas. Agora deixe o trio mostrar seu poder.':`Escolha ${draft.team.length+1} de 3. Pense em como as habilidades podem trabalhar juntas.`}</p></div>
  <div className="team-slots">{Array.from({length:3},(_,i)=>{const c=byId[draft.team[i]];return <div className={`team-slot ${c?'filled':''}`} key={i}>{c?<><Portrait character={c} className="tiny"/><span>{c.name}</span><Check size={16}/></>:<><Plus size={20}/><span>Integrante {i+1}</span></>}</div>;})}</div>
  {draft.team.length>0&&<div className="team-kit"><strong>Seu trio já tem</strong><div className="role-chips">{roleOrder.filter(role=>teamRoles.includes(role)).map(role=><span key={role}>✓ {role}</span>)}</div>{!teamRoles.includes('Cura')&&<small>Pouca recuperação até agora</small>}</div>}
  <div className="candidate-grid">{(full?draft.team:draft.candidates).map(id=>{const c=byId[id],trait=presentTrait(c.trait);return <article className="candidate-card" key={id} style={{'--character':c.color} as React.CSSProperties}><button className="candidate-art" onClick={()=>onDetails(id)} aria-label={`Detalhes de ${c.name}`}><Portrait character={c}/><span className="candidate-universe">{c.universe}</span><span className="detail-dot"><Info size={17}/></span></button><div className="candidate-body"><h2>{c.name}</h2><div className="role-chips">{rolesFor(c).map(role=><span key={role}>{role}</span>)}</div><p>{c.idea}</p><small className="candidate-trait"><b>{c.trait.name}</b> · {trait.summary} · ativa {trait.trigger}</small><small className="candidate-warning">{c.vulnerability}</small><div className="candidate-skills">{c.skills.map(s=><span title={s.name} key={s.id}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id}/></span>)}<button className="text-button" onClick={()=>onDetails(id)}>Ver ficha <ArrowRight size={14}/></button></div>{!full&&<button className="choose-button" onClick={()=>onPick(id)}>Escolher <Plus size={17}/></button>}</div></article>;})}</div>
  <div className="draft-actions">{full?<button className="primary" onClick={onStart}>Entrar na arena <ArrowRight size={20}/></button>:<><button className="secondary" onClick={onSkip} disabled={draft.skips===0}><Shuffle size={17}/> Trocar candidatos <span className="count-badge">{draft.skips}/3</span></button><p>Os pulos são compartilhados entre as três escolhas.</p></>}<button className="draft-abandon" onClick={onAbandon}><LogOut size={15}/>Desistir da campanha</button></div>
 </section>;
}
