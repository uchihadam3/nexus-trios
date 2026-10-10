import { useMemo,useState,type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight,CircleCheck,Crown,Dices,Info,Lightbulb,LogOut,Sparkles,Swords,TriangleAlert,X } from 'lucide-react';
import type { Draft,Encounter } from '../engine/campaign';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { presentTrait,textoDaResistencia,textoDoRenascer } from '../engine/skill-descriptions';
import { identidadesDe,identidadesDoTrio,lacunasDoTrio,oQueAdiciona } from '../presentation/identities';
import { IdentityChips } from '../components/IdentityChips';
import { ComTermos } from '../components/Termos';
import { draftConnection } from '../presentation/draft-connections';
import { dicasDoDraft,type DicaDoCandidato } from '../presentation/dicas-do-trio';
import { CUSTO_DAS_DICAS,formatarPontos } from '../engine/pontos';

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
 *
 * Dicas de trio: o botão no topo liga um "técnico" (src/presentation/
 * dicas-do-trio.ts) que marca a melhor escolha, mostra quanto cada candidato
 * encaixa no trio de agora e diz por quê — e cada luta da jornada passa a
 * custar CUSTO_DAS_DICAS. Desligado, a escolha fica por conta do jogador:
 * sem dicas, sem conexões, sem avisos.
 */
const NIVEL=(n:number)=>n>=80?{rotulo:'ÓTIMO',cor:'#7dff9b'}:n>=55?{rotulo:'BOM',cor:'#c8f560'}:n>=35?{rotulo:'OK',cor:'#ffd166'}:{rotulo:'FRACO',cor:'#ff7a85'};
const primeiroNome=(id:string)=>byId[id].name.split(/[ ,]/)[0];
export function DraftScreen({draft,primeiroRival,dicas,podeDicas=true,usouDicas,onDicas,onPick,onSkip,onDetails,onStart,onAbandon}:{draft:Draft;primeiroRival?:Encounter;dicas:boolean;/** o botão só aparece para quem liberou as Dicas (src/lib/dicas-liberadas.ts) */podeDicas?:boolean;usouDicas:boolean;onDicas:(ligar:boolean)=>void;onPick:(id:string)=>void;onSkip:()=>void;onDetails:(id:string)=>void;onStart:()=>void;onAbandon:()=>void}){
  const full=draft.team.length===3,team=draft.team.map(id=>byId[id]);
  const doTrio=identidadesDoTrio(team),lacunas=lacunasDoTrio(team);
  const vez=draft.team.length;
  const ligadas=dicas&&!full;
  const conselhos=useMemo(()=>ligadas?dicasDoDraft(draft.candidates,draft.team):[],[ligadas,draft.candidates,draft.team]);
  const [porque,setPorque]=useState<DicaDoCandidato|null>(null);
  const comQuem=draft.team.map(primeiroNome).join(' + ');

  return <section className={`draft-v2 ${full?'completo':''}`}>
    <header className="dv-topo">
      <span className="dv-rotulo">{full?'TRIO COMPLETO':`ESCOLHA ${vez+1} DE 3`}</span>
      <h1>{full?'Pronto para a arena':'Monte seu trio'}</h1>
      <div className="dv-espacos">{[0,1,2].map(i=>{const c=team[i];return <div key={c?.id??`vazio-${i}`} className={`dv-espaco ${c?'cheio':''} ${i===vez&&!full?'vez':''}`} style={c?{'--character':c.color} as CSSProperties:undefined}>
        {c?<><Portrait character={c}/><b>{c.name}</b></>:<><span>?</span><b>{i===vez?'escolha agora':`espaço ${i+1}`}</b></>}
      </div>;})}</div>
      {team.length>0&&<div className="dv-trio-faz"><IdentityChips ids={doTrio} trio={doTrio}/>{ligadas&&lacunas.length>0&&<small><TriangleAlert size={13}/>{lacunas.join(' · ')}</small>}</div>}
      {(podeDicas&&!full||usouDicas)&&<button className={`dv-dicas ${dicas?'ligado':''}`} role="switch" aria-checked={dicas} onClick={()=>onDicas(!dicas)} disabled={full}>
        <span className="dv-dicas-lampada"><Lightbulb size={20}/></span>
        <span className="dv-dicas-texto"><b>DICAS DE TRIO</b><small>{dicas?<>ligadas · <em>−{formatarPontos(CUSTO_DAS_DICAS)} por luta</em></>:usouDicas?<>esta jornada já usou · <em>−{formatarPontos(CUSTO_DAS_DICAS)} por luta</em></>:'desligadas · pontos cheios'}</small></span>
        <span className="dv-dicas-chave" aria-hidden><i/></span>
      </button>}
    </header>

    {!full&&<div className="dv-cartas" key={draft.candidates.join('-')}>{draft.candidates.map((id,i)=>{
      const c=byId[id],trait=presentTrait(c.trait),novas=oQueAdiciona(c,team),conexao=ligadas?draftConnection(c,team):null,dica=conselhos.find(x=>x.id===id),nivel=dica&&NIVEL(dica.encaixe);
      return <article key={id} className={`dv-carta candidate-card ${dica?.melhor?'melhor':''}`} style={{'--character':c.color,'--i':i} as CSSProperties}>
        <button className="dv-retrato" onClick={()=>onDetails(id)} aria-label={`Ficha de ${c.name}`}>
          <Portrait character={c}/><span className="dv-universo">{c.universe}</span><span className="dv-info"><Info size={16}/></span>
          <h2>{c.name}</h2>
        </button>
        <div className="dv-corpo">
          {dica&&nivel&&<button className="dv-dica" style={{'--nivel':nivel.cor,'--encaixe':`${dica.encaixe}%`} as CSSProperties} onClick={()=>setPorque(dica)} aria-label={`Por que ${c.name}? ${dica.encaixe}% de encaixe`}>
            {dica.melhor&&<span className="dv-melhor"><Crown size={13}/>MELHOR ESCOLHA</span>}
            <span className="dv-dica-topo"><b>{dica.encaixe}%</b><span><strong>{team.length?'ENCAIXE':'FORÇA'} · {nivel.rotulo}</strong><small>{team.length?`com ${comQuem}`:'entre todo o elenco'}</small></span></span>
            <span className="dv-dica-barra"><i/></span>
            {dica.curtos.map(m=><span key={m.texto} className={`dv-dica-motivo ${m.tom}`}>{m.tom==='bom'?<CircleCheck size={13}/>:<TriangleAlert size={13}/>}{m.texto}</span>)}
            <span className="dv-dica-porque">Por quê? <Info size={12}/></span>
          </button>}
          <IdentityChips ids={identidadesDe(c)} trio={team.length?doTrio:undefined} novas={ligadas&&team.length?novas:undefined}/>
          {conexao&&!dica&&<p className="dv-conexao"><Sparkles size={14}/>{conexao}</p>}
          <p className="dv-traco"><b>{c.trait.name}</b> <ComTermos texto={trait.summary}/>{c.renascer&&<> · <ComTermos texto={textoDoRenascer(c.renascer)}/></>}{c.ultimaResistencia&&<> · <ComTermos texto={textoDaResistencia(c.ultimaResistencia)}/></>}</p>
          <div className="dv-habilidades">{c.skills.map(s=><span key={s.id} title={s.name}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={30}/></span>)}<button className="text-button" onClick={()=>onDetails(id)}>Ficha</button></div>
          <button className="dv-escolher choose-button" onClick={()=>onPick(id)} aria-label="Escolher" title={`Adicionar ${c.name} ao trio`}>ESCOLHER</button>
        </div>
      </article>;})}</div>}

    {full&&!primeiroRival&&<div className="dv-rival dv-rival-sorteando" role="status"><span><Swords size={15}/>PRIMEIRA LUTA</span><b>Sorteando os rivais…</b></div>}
    {full&&primeiroRival&&<div className="dv-rival"><span><Swords size={15}/>PRIMEIRA LUTA</span><b>{primeiroRival.name}</b><div>{primeiroRival.team.map(id=><span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/><small>{byId[id].name}</small></span>)}</div></div>}

    {porque&&createPortal(<div className="dv-porque-fundo" onClick={()=>setPorque(null)}><div className="dv-porque" role="dialog" aria-modal="true" aria-label={`Por que ${byId[porque.id].name}`} style={{'--character':byId[porque.id].color,'--nivel':NIVEL(porque.encaixe).cor} as CSSProperties} onClick={e=>e.stopPropagation()}>
      <button className="dv-porque-fechar" onClick={()=>setPorque(null)} aria-label="Fechar"><X size={18}/></button>
      <div className="dv-porque-cabeca"><Portrait character={byId[porque.id]}/><div><span>{porque.melhor?<><Crown size={12}/>MELHOR ESCOLHA</>:'DICA DO TÉCNICO'}</span><h2>{byId[porque.id].name}</h2></div></div>
      <div className="dv-porque-encaixe"><b>{porque.encaixe}%</b><p>{team.length?<>Combina com <strong>{comQuem}</strong> melhor do que {porque.encaixe}% dos personagens que poderiam entrar agora.</>:<>Mais forte, sozinho, do que {porque.encaixe}% do elenco — medido em milhares de lutas simuladas.</>}</p></div>
      <ul>{porque.detalhe.map(m=><li key={m.texto} className={m.tom}>{m.tom==='bom'?<CircleCheck size={15}/>:<TriangleAlert size={15}/>}<span>{m.texto}{m.porque&&<small className="dv-porque-como">{m.porque}.</small>}</span></li>)}</ul>
      <p className="dv-porque-licao">{team.length?'Dica: o trio vence junto. Procure quem cura e protege os de pouca Vida e quem enche a Carga dos golpes grandes.':'Dica: comece por alguém forte. Depois, o técnico procura quem combina com ele.'}</p>
      <button className="dv-escolher" onClick={()=>{const id=porque.id;setPorque(null);onPick(id);}}>ESCOLHER {primeiroNome(porque.id).toUpperCase()}</button>
    </div></div>,document.body)}

    <footer className="dv-barra">
      {full?<button className="dv-arena" onClick={onStart} disabled={!primeiroRival} aria-label="Entrar na arena"><span>ENTRAR NA ARENA</span><ArrowRight size={22}/></button>
        :<button className="secondary dv-trocar" onClick={onSkip} disabled={draft.skips===0} aria-label="Trocar candidatos"><Dices size={19}/><span>Trocar opções</span><b>{draft.skips}</b></button>}
      <button className="secondary dv-sair" onClick={onAbandon} aria-label="Desistir da jornada" title="Desistir da jornada"><LogOut size={18}/></button>
    </footer>
  </section>;
}
