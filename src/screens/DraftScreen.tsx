import { useMemo,useState,type CSSProperties } from 'react';
import { SeloDeEstrela } from '../components/SeloDeEstrela';
import { createPortal } from 'react-dom';
import { ArrowRight,Award,Check,CircleCheck,Crown,Dices,Info,LogOut,Sparkles,Star,Swords,TriangleAlert,X,Zap } from 'lucide-react';
import type { Draft,Encounter } from '../engine/campaign';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { presentTrait,textoDaResistencia,textoDoRenascer } from '../engine/skill-descriptions';
import { identidadesDe,identidadesDoTrio,lacunasDoTrio,oQueAdiciona } from '../presentation/identities';
import { IdentityChips } from '../components/IdentityChips';
import { ComTermos } from '../components/Termos';
import { draftConnection } from '../presentation/draft-connections';
import { BotaoDicas } from '../components/BotaoDicas';
import { dicasDoDraft,estrelasDaPorcentagem,posicaoDoTrio,ESTRELAS_MAXIMAS,type DicaDoCandidato } from '../presentation/dicas-do-trio';
import { ESTRELAS_DOURADAS,douradasDaPosicao,textoDaPosicao,usePosicaoDoTrio } from '../presentation/posicao-do-trio';
import { universoDaFicha } from '../data/equipes';
import { CUSTO_DA_COLECAO,formatarPontos } from '../engine/pontos';
import { nomeDe, numero, ordinal, plural, t } from '../i18n/idioma';

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
const NIVEL=(n:number)=>n>=80?{rotulo:t('ÓTIMO'),cor:'#7dff9b'}:n>=55?{rotulo:t('BOM'),cor:'#c8f560'}:n>=35?{rotulo:t('OK'),cor:'#ffd166'}:{rotulo:t('FRACO'),cor:'#ff7a85'};
const primeiroNome=(id:string)=>nomeDe(byId[id]).split(/[ ,]/)[0];
export function DraftScreen({draft,desafio,colecao=false,primeiroRival,naColecao,dicas,podeDicas,usouDicas,onDicas,onPick,onSkip,onDetails,onStart,onAbandon}:{draft:Draft;/** a Jornada veio do Desafio do Dia, com este personagem já escolhido */desafio?:string;/** a Jornada com os seus: o trio veio das Conquistas */colecao?:boolean;primeiroRival?:Encounter;/** os personagens que o jogador já tem na coleção (ganham o selo na carta) */naColecao?:ReadonlySet<string>;dicas:boolean;/** o botão só liga para quem liberou as Dicas (src/lib/dicas-liberadas.ts) */podeDicas:boolean;usouDicas:boolean;onDicas:(ligar:boolean)=>void;onPick:(id:string)=>void;onSkip:()=>void;onDetails:(id:string)=>void;onStart:()=>void;onAbandon:()=>void}){
  const full=draft.team.length===3,team=draft.team.map(id=>byId[id]);
  const doTrio=identidadesDoTrio(team),lacunas=lacunasDoTrio(team);
  const vez=draft.team.length;
  const ligadas=dicas&&!full;
  const conselhos=useMemo(()=>ligadas?dicasDoDraft(draft.candidates,draft.team):[],[ligadas,draft.candidates,draft.team]);
  const [porque,setPorque]=useState<DicaDoCandidato|null>(null);
  const comQuem=draft.team.map(primeiroNome).join(' + ');

  return <section className={`draft-v2 ${full?'completo':''}`}>
    <header className="dv-topo">
      <span className="dv-rotulo">{full?t('TRIO COMPLETO'):t('ESCOLHA {n} DE 3',{n:vez+1})}</span>
      <h1>{full?t('Pronto para a arena'):t('Monte seu trio')}</h1>
      {desafio&&byId[desafio]&&<div className="dv-desafio" style={{'--character':byId[desafio].color} as CSSProperties}><Zap size={14}/><span><b>{t('DESAFIO DO DIA')}</b> · {t('{nome} já está no trio',{nome:nomeDe(byId[desafio])})}{!full&&<> · {plural(draft.skips,'{n} troca de opções','{n} trocas de opções')}</>}</span></div>}
      {colecao&&<div className="dv-desafio dv-com-os-seus"><Award size={14}/><span><b>{t('JORNADA COM OS SEUS')}</b> · {t('sem bônus de estrela nem segredos')} · <b>−{formatarPontos(CUSTO_DA_COLECAO)}</b> {t('por luta')}</span></div>}
      {/* quem já está no trio abre a ficha (pedido do jogador: "clicar ali em cima e ver o que ele faz, pra ver se combina") */}
      <div className="dv-espacos">{[0,1,2].map(i=>{const c=team[i];return c
        ?<button key={c.id} type="button" className="dv-espaco cheio" style={{'--character':c.color} as CSSProperties} onClick={()=>onDetails(c.id)} aria-label={t('Ver a ficha de {nome}',{nome:nomeDe(c)})}>
          <Portrait character={c}/><b>{nomeDe(c)}</b><small className="dv-espaco-ficha"><Info size={10}/>{t('ficha')}</small>
        </button>
        :<div key={`vazio-${i}`} className={`dv-espaco ${i===vez&&!full?'vez':''}`}><span>?</span><b>{i===vez?t('escolha agora'):t('espaço {n}',{n:i+1})}</b></div>;})}</div>
      {full&&<EstrelasDoTrio team={draft.team}/>}
      {team.length>0&&<div className="dv-trio-faz"><IdentityChips ids={doTrio} trio={doTrio}/>{ligadas&&lacunas.length>0&&<small><TriangleAlert size={13}/>{lacunas.map(x=>t(x)).join(' · ')}</small>}</div>}
      {(!full||usouDicas)&&<BotaoDicas ligado={dicas} liberado={podeDicas} usado={usouDicas} desativado={full} onMudar={onDicas}/>}
    </header>

    {!full&&<div className="dv-cartas" key={draft.candidates.join('-')}>{draft.candidates.map((id,i)=>{
      const c=byId[id],trait=presentTrait(c.trait),novas=oQueAdiciona(c,team),conexao=ligadas?draftConnection(c,team):null,dica=conselhos.find(x=>x.id===id),nivel=dica&&NIVEL(dica.encaixe);
      return <article key={id} className={`dv-carta candidate-card ${dica?.melhor?'melhor':''}`} style={{'--character':c.color,'--i':i} as CSSProperties}>
        <button className="dv-retrato" onClick={()=>onDetails(id)} aria-label={t('Ficha de {nome}',{nome:nomeDe(c)})}>
          <Portrait character={c}/><span className="dv-universo">{t(universoDaFicha(c))}</span><span className="dv-info"><Info size={16}/></span>
          <h2>{nomeDe(c)}</h2>
        </button>
        <SeloDeEstrela id={c.id}/>
        {/* pedido do jogador: "um selo bonito nos personagens que você já tem na coleção", no canto de cima da carta */}
        {naColecao?.has(id)&&<span className="dv-colecao" title={t('Já está na sua coleção')} aria-label={t('Já está na sua coleção')}><Check size={14} strokeWidth={3.6}/></span>}
        <div className="dv-corpo">
          {dica&&nivel&&<button className="dv-dica" style={{'--nivel':nivel.cor,'--encaixe':`${dica.encaixe}%`} as CSSProperties} onClick={()=>setPorque(dica)} aria-label={t('Por que {nome}? {n}% de encaixe',{nome:nomeDe(c),n:dica.encaixe})}>
            {dica.melhor&&<span className="dv-melhor"><Crown size={13}/>{t('MELHOR ESCOLHA')}</span>}
            <span className="dv-dica-topo"><b>{dica.encaixe}%</b><span><strong>{team.length?t('ENCAIXE'):t('FORÇA')} · {nivel.rotulo}</strong><small>{team.length?t('com {quem}',{quem:comQuem}):t('entre todo o elenco')}</small></span></span>
            <span className="dv-dica-barra"><i/></span>
            {dica.curtos.map(m=><span key={m.texto} className={`dv-dica-motivo ${m.tom}`}>{m.tom==='bom'?<CircleCheck size={13}/>:<TriangleAlert size={13}/>}{m.texto}</span>)}
            <span className="dv-dica-porque">{t('Por quê?')} <Info size={12}/></span>
          </button>}
          <IdentityChips ids={identidadesDe(c)} trio={team.length?doTrio:undefined} novas={ligadas&&team.length?novas:undefined}/>
          {conexao&&!dica&&<p className="dv-conexao"><Sparkles size={14}/>{conexao}</p>}
          <p className="dv-traco"><b>{t(c.trait.name)}</b> <ComTermos texto={trait.summary}/>{c.renascer&&<> · <ComTermos texto={textoDoRenascer(c.renascer)}/></>}{c.ultimaResistencia&&<> · <ComTermos texto={textoDaResistencia(c.ultimaResistencia)}/></>}</p>
          <div className="dv-habilidades">{c.skills.map(s=><span key={s.id} title={t(s.name)}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={30}/></span>)}<button className="text-button" onClick={()=>onDetails(id)}>{t('Ficha')}</button></div>
          <button className="dv-escolher choose-button" onClick={()=>onPick(id)} aria-label={t('Escolher')} title={t('Adicionar {nome} ao trio',{nome:nomeDe(c)})}>{t('ESCOLHER')}</button>
        </div>
      </article>;})}</div>}

    {full&&!primeiroRival&&<div className="dv-rival dv-rival-sorteando" role="status"><span><Swords size={15}/>{t('PRIMEIRA LUTA')}</span><b>{t('Escolhendo rivais aleatórios…')}</b></div>}
    {full&&primeiroRival&&<div className="dv-rival"><span><Swords size={15}/>{t('PRIMEIRA LUTA')}</span><b>{t(primeiroRival.name)}</b><div>{primeiroRival.team.map(id=><span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/><small>{nomeDe(byId[id])}</small></span>)}</div></div>}

    {porque&&createPortal(<div className="dv-porque-fundo" onClick={()=>setPorque(null)}><div className="dv-porque" role="dialog" aria-modal="true" aria-label={t('Por que {nome}',{nome:nomeDe(byId[porque.id])})} style={{'--character':byId[porque.id].color,'--nivel':NIVEL(porque.encaixe).cor} as CSSProperties} onClick={e=>e.stopPropagation()}>
      <button className="dv-porque-fechar" onClick={()=>setPorque(null)} aria-label={t('Fechar')}><X size={18}/></button>
      <div className="dv-porque-cabeca"><Portrait character={byId[porque.id]}/><div><span>{porque.melhor?<><Crown size={12}/>{t('MELHOR ESCOLHA')}</>:t('DICA DO TÉCNICO')}</span><h2>{nomeDe(byId[porque.id])}</h2></div></div>
      <div className="dv-porque-encaixe"><b>{porque.encaixe}%</b><p>{team.length?t('Combina com {quem} melhor do que {n}% dos personagens que poderiam entrar agora.',{quem:comQuem,n:porque.encaixe}):t('Mais forte, sozinho, do que {n}% do elenco.',{n:porque.encaixe})}</p></div>
      {/* o que é da combinação com o trio e o que é do próprio personagem (vale em qualquer trio), separados */}
      {(team.length?[['trio',t('Com {quem}',{quem:comQuem})],['dele',t('Do próprio {nome} · vale em qualquer trio',{nome:primeiroNome(porque.id)})]] as const:[['dele','']] as const).map(([g,titulo])=>{
        const itens=porque.detalhe.filter(m=>team.length?(m.grupo??'trio')===g:true);
        return itens.length?<div key={g} className={`dv-porque-grupo ${g}`}>{titulo&&<h3>{titulo}</h3>}
          <ul>{itens.map(m=><li key={m.texto} className={m.tom}>{m.tom==='bom'?<CircleCheck size={15}/>:<TriangleAlert size={15}/>}<span>{m.texto}{m.porque&&<small className="dv-porque-como">{m.porque}.</small>}</span></li>)}</ul></div>:null;})}
      <p className="dv-porque-licao">{team.length?t('Dica: o trio vence junto. Procure quem cura e protege os de pouca Vida e quem enche a Carga dos golpes grandes.'):t('Dica: comece por alguém forte. Depois, o técnico procura quem combina com ele.')}</p>
      <button className="dv-escolher" onClick={()=>{const id=porque.id;setPorque(null);onPick(id);}}>{t('ESCOLHER {nome}',{nome:primeiroNome(porque.id).toUpperCase()})}</button>
    </div></div>,document.body)}

    <footer className="dv-barra">
      {full?<button className="dv-arena" onClick={onStart} disabled={!primeiroRival} aria-label={t('Entrar na arena')}><span>{t('ENTRAR NA ARENA')}</span><ArrowRight size={22}/></button>
        :<button className="secondary dv-trocar" onClick={onSkip} disabled={draft.skips===0} aria-label={t('Trocar candidatos')}><Dices size={19}/><span>{t('Trocar opções')}</span><b>{draft.skips}</b></button>}
      <button className="secondary dv-sair" onClick={onAbandon} aria-label={t('Desistir da jornada')} title={t('Desistir da jornada')}><LogOut size={18}/></button>
    </footer>
  </section>;
}

/*
 * As estrelas do trio (pedido do dono: "depois que escolher os três, aparece quantas estrelas o time tem… mais
 * sutil, pequenininhas, não tão destacado"; e depois: "deixa as estrelinhas só na minha conta"; depois liberou para todas as contas): só as estrelinhas (1 a 7) embaixo do trio, acendendo uma a uma. A força é
 * a mesma do PvP (src/presentation/dicas-do-trio.ts, estrelasDoTime).
 */
function EstrelasDoTrio({team}:{team:string[]}){
  const {pct}=posicaoDoTrio(team),n=estrelasDaPorcentagem(pct),lugar=usePosicaoDoTrio(team);
  // as 7 de prata e, no 1% do topo, de 1 a 7 douradas (src/presentation/posicao-do-trio.ts)
  const ouro=lugar?douradasDaPosicao(lugar.posicao,lugar.total):0;
  // e a posição entre todos os trios; a porcentagem saiu (pedido do dono: "deixar só as estrelas e a posição")
  return <div className="dv-estrelas" role="img" aria-label={`${plural(n,'Trio de {n} estrela','Trio de {n} estrelas')}${ouro?` ${plural(ouro,'e {n} dourada','e {n} douradas')}`:''}, ${lugar?`, ${t('{posicao} de {total}',{posicao:ordinal(lugar.posicao),total:numero(lugar.total)})}`:''}`}>
    {Array.from({length:ESTRELAS_MAXIMAS},(_,k)=><i key={k} className={k<n?'acesa':''} style={{'--k':k} as CSSProperties}><Star size={13} fill="currentColor" strokeWidth={1.5}/></i>)}
    {ouro>0&&<span className="dv-ouro">{Array.from({length:ESTRELAS_DOURADAS},(_,k)=><i key={k} className={k<ouro?'acesa':''} style={{'--k':ESTRELAS_MAXIMAS+k} as CSSProperties}><Star size={13} fill="currentColor" strokeWidth={1.5}/></i>)}</span>}
    {lugar&&<small><span className="dv-lugar" title={t('{posicao} lugar entre {total} trios possíveis',{posicao:ordinal(lugar.posicao),total:numero(lugar.total)})}>{textoDaPosicao(lugar.posicao)}</span></small>}
  </div>;
}
