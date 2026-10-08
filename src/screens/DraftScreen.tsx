import type { CSSProperties } from 'react';
import { ArrowRight,Dices,Info,LogOut,Sparkles,Swords,TriangleAlert } from 'lucide-react';
import type { Draft,Encounter } from '../engine/campaign';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { presentTrait } from '../engine/skill-descriptions';
import { identidadesDe,identidadesDoTrio,lacunasDoTrio,oQueAdiciona } from '../presentation/identities';
import { IdentityChips } from '../components/IdentityChips';
import { ComTermos } from '../components/Termos';
import { draftConnection } from '../presentation/draft-connections';

/*
 * A escolha do trio (remake).
 *
 * No topo, os três espaços do trio como medalhões: o da vez pulsa, e o
 * retrato entra com um estouro quando a escolha acontece. Embaixo, três
 * cartas de candidato — retrato grande, as etiquetas (as que trazem algo novo
 * para o trio brilham), a conexão com quem já foi escolhido, o traço numa
 * linha, as habilidades e um botão ESCOLHER na cor do personagem. A barra de
 * baixo fica sempre à mão: trocar as opções, ou, com o trio completo, entrar
 * na arena.
 */
export function DraftScreen({draft,primeiroRival,onPick,onSkip,onDetails,onStart,onAbandon}:{draft:Draft;primeiroRival?:Encounter;onPick:(id:string)=>void;onSkip:()=>void;onDetails:(id:string)=>void;onStart:()=>void;onAbandon:()=>void}){
  const full=draft.team.length===3,team=draft.team.map(id=>byId[id]);
  const doTrio=identidadesDoTrio(team),lacunas=lacunasDoTrio(team);
  const vez=draft.team.length;

  return <section className={`draft-v2 ${full?'completo':''}`}>
    <header className="dv-topo">
      <span className="dv-rotulo">{full?'TRIO COMPLETO':`ESCOLHA ${vez+1} DE 3`}</span>
      <h1>{full?'Pronto para a arena':'Monte seu trio'}</h1>
      <div className="dv-espacos">{[0,1,2].map(i=>{const c=team[i];return <div key={c?.id??`vazio-${i}`} className={`dv-espaco ${c?'cheio':''} ${i===vez&&!full?'vez':''}`} style={c?{'--character':c.color} as CSSProperties:undefined}>
        {c?<><Portrait character={c}/><b>{c.name}</b></>:<><span>?</span><b>{i===vez?'escolha agora':`espaço ${i+1}`}</b></>}
      </div>;})}</div>
      {team.length>0&&<div className="dv-trio-faz"><IdentityChips ids={doTrio} trio={doTrio}/>{lacunas.length>0&&!full&&<small><TriangleAlert size={13}/>{lacunas.join(' · ')}</small>}</div>}
    </header>

    {!full&&<div className="dv-cartas" key={draft.candidates.join('-')}>{draft.candidates.map((id,i)=>{
      const c=byId[id],trait=presentTrait(c.trait),novas=oQueAdiciona(c,team),conexao=draftConnection(c,team);
      return <article key={id} className="dv-carta candidate-card" style={{'--character':c.color,'--i':i} as CSSProperties}>
        <button className="dv-retrato" onClick={()=>onDetails(id)} aria-label={`Ficha de ${c.name}`}>
          <Portrait character={c}/><span className="dv-universo">{c.universe}</span><span className="dv-info"><Info size={16}/></span>
          <h2>{c.name}</h2>
        </button>
        <div className="dv-corpo">
          <IdentityChips ids={identidadesDe(c)} trio={team.length?doTrio:undefined} novas={team.length?novas:undefined}/>
          {conexao&&<p className="dv-conexao"><Sparkles size={14}/>{conexao}</p>}
          <p className="dv-traco"><b>{c.trait.name}</b> <ComTermos texto={trait.summary}/></p>
          <div className="dv-habilidades">{c.skills.map(s=><span key={s.id} title={s.name}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={30}/></span>)}<button className="text-button" onClick={()=>onDetails(id)}>Ficha</button></div>
          <button className="dv-escolher choose-button" onClick={()=>onPick(id)} aria-label="Escolher" title={`Adicionar ${c.name} ao trio`}>ESCOLHER</button>
        </div>
      </article>;})}</div>}

    {full&&primeiroRival&&<div className="dv-rival"><span><Swords size={15}/>PRIMEIRA LUTA</span><b>{primeiroRival.name}</b><div>{primeiroRival.team.map(id=><span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/><small>{byId[id].name}</small></span>)}</div></div>}

    <footer className="dv-barra">
      {full?<button className="dv-arena" onClick={onStart} aria-label="Entrar na arena"><span>ENTRAR NA ARENA</span><ArrowRight size={22}/></button>
        :<button className="secondary dv-trocar" onClick={onSkip} disabled={draft.skips===0} aria-label="Trocar candidatos"><Dices size={19}/><span>Trocar opções</span><b>{draft.skips}</b></button>}
      <button className="secondary dv-sair" onClick={onAbandon} aria-label="Desistir da jornada" title="Desistir da jornada"><LogOut size={18}/></button>
    </footer>
  </section>;
}
