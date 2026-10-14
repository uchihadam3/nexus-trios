import type { CSSProperties } from 'react';
import { X,HeartPulse,Clock3,Sparkles,Swords,Flame,Hourglass,Snowflake,Zap,ChevronLeft,ShieldHalf,Info } from 'lucide-react';
import { condicaoAtendida } from '../engine/battle';
import { unicaDe } from '../engine/unicas';
import type { Battle,Fighter,Status } from '../engine/types';
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import { SkillIcon } from './Icon';
import { Portrait } from './Portrait';
import { naFormaDeAgora } from '../presentation/formas';
import { EfeitosAgrupados } from './EfeitosAgrupados';
import { ComTermos,TermoBotao } from './Termos';
import { termoPorId } from '../presentation/glossario';
import { StatusBadge } from './StatusBadge';
import { ativaQuando,presentEffect,presentSkill,presentStatus,presentTrait,tetoDoStatus,textoDaIsca,textoDaResistencia,textoDoDespercebido,textoDoJeito,textoDoRenascer,valorAtualDoStatus } from '../engine/skill-descriptions';
import { universoDaFicha } from '../data/equipes';
import { bolinhaNaTela,type LuzDaBolinha } from '../presentation/bolinha-da-unica';
import { bolinhaDe,corDaBolinha } from '../presentation/bolinhas';

/*
 * O detalhe rápido da batalha (pedido do jogador: "deixa muito bonito, bem
 * gamificado, padronizado; encurta onde der e põe coisa clicável").
 *
 * Três telas com o mesmo desenho: um topo com o retrato (ou o ícone) dentro de
 * um anel que mostra o estado de agora — a Vida do lutador, a Carga da
 * habilidade, o tempo que falta do Status —, e embaixo cartões curtos, cada um
 * com o selo do que ele é (Mecânica única, Traço, Ataque básico). Os selos e os
 * rótulos abrem a explicação do glossário. Na ficha da habilidade e na do
 * Status, a fileira de baixo troca de ficha sem fechar.
 */
export type InspectTarget={kind:'fighter';fighter:Fighter}|{kind:'unica';fighter:Fighter}|{kind:'skill';fighter:Fighter;index:number}|{kind:'status';fighter:Fighter;status:Status};

const fmt=(x:number)=>x.toLocaleString('pt-BR',{maximumFractionDigits:1});

/** O estado de agora de uma habilidade: o rótulo curto, o ícone e quanto do anel está cheio. */
function estadoDa(battle:Battle,f:Fighter,i:number){
  const s=f.skills[i],skill=byId[f.characterId].skills[i];
  if(s.cooldown>0)return {classe:'descansa',rotulo:`Resfriamento ${fmt(s.cooldown)} s`,icone:Snowflake,p:0};
  if(f.cast?.skill===i)return {classe:'prepara',rotulo:'Em Preparo',icone:Hourglass,p:100};
  if(s.charge>=100)return condicaoAtendida(battle,f,skill)?{classe:'pronta',rotulo:'Pronta',icone:Zap,p:100}:{classe:'espera',rotulo:'Pronta · esperando',icone:Hourglass,p:100};
  return {classe:'enche',rotulo:`${Math.round(s.charge)}% · Carregando`,icone:Flame,p:s.charge};
}

export function BattleInspector({target,battle,onClose,onSelect}:{target:InspectTarget;battle:Battle;onClose:()=>void;onSelect:(target:InspectTarget)=>void}){
  const f=battle.fighters.find(fighter=>fighter.uid===target.fighter.uid)??target.fighter,c=byId[f.characterId];
  const skillIndex=target.kind==='skill'?target.index:-1,unicaAberta=target.kind==='unica';
  const liveStatus=target.kind==='status'?f.statuses.find(status=>status.id===target.status.id)??target.status:undefined;
  // a chave muda com a ficha: trocar de ficha toca a entrada de novo
  return <aside key={`${f.uid}-${target.kind}-${skillIndex}-${liveStatus?.id??''}${unicaAberta?'-u':''}`} className={`battle-inspector bi2 ${f.side==='player'?'aliado':'rival'}`} style={{'--cor':c.color} as CSSProperties} role="dialog" aria-modal="false" aria-label="Detalhes rápidos de batalha">
    <button className="inspector-close bi2-fechar" onClick={onClose} aria-label="Fechar detalhes"><X size={18}/></button>
    {target.kind==='unica'&&unicaDe(c.id)?<FichaDaUnica battle={battle} f={f} onSelect={onSelect}/>
      :liveStatus?<FichaDoStatus battle={battle} f={f} s={liveStatus} onSelect={onSelect}/>
      :skillIndex>=0?<FichaDaHabilidade battle={battle} f={f} i={skillIndex} onSelect={onSelect}/>
      :<FichaDoLutador battle={battle} f={f} onSelect={onSelect}/>}
  </aside>;
}

function FichaDoLutador({battle,f,onSelect}:{battle:Battle;f:Fighter;onSelect:(t:InspectTarget)=>void}){
  const c=naFormaDeAgora(byId[f.characterId],f),vida=Math.max(0,Math.min(Math.round(f.hp),Math.round(f.maxHp))),fracao=Math.max(0,f.hp)/f.maxHp,escudo=Math.round(f.shields.reduce((t,s)=>t+s.amount,0));
  const traco=presentTrait(c.trait),unica=unicaDe(c.id);
  const extras=[c.renascer&&(f.voltou?'Já renasceu nesta luta. ':'')+textoDoRenascer(c.renascer),c.ultimaResistencia&&(f.resistiu?'Já usou nesta luta. ':'')+textoDaResistencia(c.ultimaResistencia),c.despercebido&&textoDoDespercebido(),c.isca&&textoDaIsca(c.isca)].filter((x):x is string=>!!x);
  const basico=c.basic.effects.map(effect=>presentEffect(effect,c.basic.target)).join(' · ');
  return <>
    <header className="bi2-topo">
      <div className={`bi2-retrato ${fracao<.3?'perigo':''}`} style={{'--p':fracao*100} as CSSProperties}><Portrait character={c}/></div>
      <div className="bi2-nome">
        <small>{universoDaFicha(c)}</small>
        <h3>{c.name}</h3>
        <div className="bi2-barra vida" style={{'--p':fracao*100} as CSSProperties}><i/><span><HeartPulse size={13}/><b>{vida}</b>/{Math.round(f.maxHp)}{escudo>0&&<em><ShieldHalf size={12}/><TermoBotao termo={termoPorId.escudo!}>{escudo}</TermoBotao></em>}</span></div>
        <div className="bi2-barra ritmo" style={{'--p':Math.min(1,Math.max(0,f.action))*100} as CSSProperties}><i/><span><Clock3 size={13}/><TermoBotao termo={termoPorId['ataque-basico']!}>Próximo ataque</TermoBotao></span></div>
      </div>
    </header>
    <div className="bi2-habs">{c.skills.map((s,i)=>{const e=estadoDa(battle,f,i);return <button key={s.id} className={`bi2-hab ${e.classe}`} style={{'--i':i} as CSSProperties} onClick={()=>onSelect({kind:'skill',fighter:f,index:i})}>
      <span className="bi2-anel" style={{'--p':e.p} as CSSProperties}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={24}/></span>
      <b>{s.name}</b><small>{e.classe==='enche'?`${Math.round(f.skills[i].charge)}%`:e.rotulo}</small>
    </button>;})}</div>
    <div className="bi2-cartoes">
      {unica&&<section className="bi2-cartao unica" style={{'--i':3} as CSSProperties}>
        <span className="bi2-selo"><Sparkles size={12}/><TermoBotao termo={termoPorId['mecanica-unica']!}>Mecânica única</TermoBotao></span>
        <b>{unica.nome}</b><p><ComTermos texto={unica.texto}/></p>
        <button className="bi2-abre-unica" onClick={()=>onSelect({kind:'unica',fighter:f})}>Ver agora</button>
      </section>}
      <section className="bi2-cartao traco" style={{'--i':4} as CSSProperties}>
        <span className="bi2-selo"><Flame size={12}/><TermoBotao termo={termoPorId.traco!}>Traço</TermoBotao></span>
        <b>{c.trait.name}</b><p><ComTermos texto={`${traco.effects.join(' · ')}.`}/></p><p className="ativa-quando"><u>{ativaQuando(c.trait,c.name).rotulo}</u> <ComTermos texto={`${ativaQuando(c.trait,c.name).resto}.`}/></p>
        {extras.length>0&&<ul className="bi2-extras">{extras.map((x,i)=><li key={i}><ComTermos texto={x+'.'}/></li>)}</ul>}
      </section>
      <section className="bi2-cartao basico" style={{'--i':5} as CSSProperties}>
        <span className="bi2-selo"><Swords size={12}/><TermoBotao termo={termoPorId['ataque-basico']!}>Ataque básico</TermoBotao></span>
        <b>{c.basic.name}</b><p><ComTermos texto={basico+'.'}/>{c.basic.jeito&&<> <ComTermos texto={textoDoJeito(c.basic.jeito)+'.'}/></>}</p>
      </section>
    </div>
    {/* Os Status do lutador, com o valor de agora e o tempo que falta; cada um abre o detalhe. */}
    {f.statuses.length>0&&<div className="bi2-status-lista">{f.statuses.map(s=>{const v=valorAtualDoStatus(s.id,s.intensity);return <button key={s.id} className={`bi2-status ${statuses[s.id].tone==='positivo'?'bom':'ruim'}`} onClick={()=>onSelect({kind:'status',fighter:f,status:s})}>
      <StatusBadge status={s}/><span>{statuses[s.id].name}</span>{v&&<b>{v}</b>}<small>{fmt(s.remaining)} s</small>
    </button>;})}</div>}
  </>;
}

function FichaDaHabilidade({battle,f,i,onSelect}:{battle:Battle;f:Fighter;i:number;onSelect:(t:InspectTarget)=>void}){
  const c=byId[f.characterId],skill=c.skills[i],p=presentSkill(skill),e=estadoDa(battle,f,i),Ic=e.icone;
  return <>
    <header className="bi2-topo hab">
      <span className={`bi2-anel grande ${e.classe}`} style={{'--p':e.p} as CSSProperties}><SkillIcon type={skill.icon} characterId={c.id} skillId={skill.id} size={40}/></span>
      <div className="bi2-nome">
        <small>{c.name} · Habilidade {i+1}</small>
        <h3>{skill.name}</h3>
        <span className={`bi2-situacao ${e.classe}`}><Ic size={13}/><ComTermos texto={e.rotulo}/></span>
      </div>
    </header>
    <section className="bi2-cartao faz" style={{'--i':0} as CSSProperties}>
      <span className="bi2-selo"><Zap size={12}/>O que faz</span>
      <EfeitosAgrupados grupos={p.grupos}/>
      {/* quanto a habilidade soltaria agora (pedido do jogador: "podia mostrar quanta energia tá guardada") */}
      {skill.effects.map((ef,k)=>ef.kind==='release'&&<p key={k} className="bi2-energia"><ComTermos texto={`Energia guardada agora: ${Math.round(f.storedEnergy??0)}`}/><b>{Math.round((f.storedEnergy??0)*ef.multiplier)} de dano</b></p>)}
    </section>
    <div className="bi2-numeros">
      <span style={{'--i':1} as CSSProperties}><Hourglass size={15}/><TermoBotao termo={termoPorId.preparo!}/><b>{p.preparation}</b></span>
      <span style={{'--i':2} as CSSProperties}><Snowflake size={15}/><TermoBotao termo={termoPorId.resfriamento!}/><b>{p.cooldown}</b></span>
    </div>
    <section className="bi2-cartao carga" style={{'--i':3} as CSSProperties}>
      <span className="bi2-selo"><Flame size={12}/><TermoBotao termo={termoPorId.carga!}>Como enche</TermoBotao></span>
      <div className="bi2-fontes">{p.charge.map((x,k)=><span key={k}><ComTermos texto={x}/></span>)}</div>
      {p.useWhen&&!/^ficar pronta$/i.test(p.useWhen)&&<p className="bi2-quando"><TermoBotao termo={termoPorId['usa-quando']!}/> <ComTermos texto={p.useWhen}/></p>}
    </section>
    <nav className="bi2-trilha" aria-label="Trocar de ficha">
      <button className="bi2-voltar" onClick={()=>onSelect({kind:'fighter',fighter:f})} aria-label={`Voltar para ${c.name}`}><ChevronLeft size={16}/><span className="bi2-mini"><Portrait character={c}/></span></button>
      {c.skills.map((s,k)=>{const ek=estadoDa(battle,f,k);return <button key={s.id} className={`bi2-aba ${k===i?'ativa':''} ${ek.classe}`} onClick={()=>onSelect({kind:'skill',fighter:f,index:k})} aria-label={s.name} aria-current={k===i}>
        <span className="bi2-anel" style={{'--p':ek.p} as CSSProperties}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={20}/></span>
      </button>;})}
      <AbaDaUnica battle={battle} f={f} ativa={false} onSelect={onSelect}/>
    </nav>
  </>;
}

function FichaDoStatus({battle,f,s,onSelect}:{battle:Battle;f:Fighter;s:Status;onSelect:(t:InspectTarget)=>void}){
  const c=byId[f.characterId],info=statuses[s.id],bom=info.tone==='positivo',v=valorAtualDoStatus(s.id,s.intensity),teto=tetoDoStatus(s.id);
  const quem=battle.fighters.find(x=>x.uid===s.source),deQuem=quem?byId[quem.characterId]:undefined;
  const resto=s.duration?Math.min(100,s.remaining/s.duration*100):100;
  return <>
    <header className={`bi2-topo status ${bom?'bom':'ruim'}`} style={{'--st':info.color} as CSSProperties}>
      <span className="bi2-anel grande" style={{'--p':resto} as CSSProperties}><StatusBadge status={s}/></span>
      <div className="bi2-nome">
        <small>{bom?'Status bom':'Status ruim'} · {c.name}</small>
        <h3>{info.name}</h3>
        <span className="bi2-situacao"><Clock3 size={13}/>{fmt(s.remaining)} s restantes</span>
      </div>
    </header>
    {v&&<div className="bi2-valor" style={{'--i':0} as CSSProperties}><b>{v}</b><span>{teto?`agora · soma até ${teto}`:'agora'}</span></div>}
    <section className="bi2-cartao" style={{'--i':1} as CSSProperties}>
      <span className="bi2-selo"><Info size={12}/><TermoBotao termo={termoPorId[s.id]!}>O que faz</TermoBotao></span>
      <p><ComTermos texto={presentStatus(s.id,s.intensity).summary+'.'}/></p>
    </section>
    <nav className="bi2-trilha" aria-label="Trocar de ficha">
      <button className="bi2-voltar" onClick={()=>onSelect({kind:'fighter',fighter:f})} aria-label={`Voltar para ${c.name}`}><ChevronLeft size={16}/><span className="bi2-mini"><Portrait character={c}/></span></button>
      {deQuem&&quem&&quem.uid!==f.uid&&<button className="bi2-de-quem" onClick={()=>onSelect({kind:'fighter',fighter:quem})}><span className="bi2-mini"><Portrait character={deQuem}/></span><span><small>Aplicado por</small><b>{deQuem.name}</b></span></button>}
    </nav>
  </>;
}

/* ---------- a ficha da Mecânica única (pedido do jogador: "clicar em cima da bolinha… abrir… pra poder ler") ---------- */
const SITUACAO:Record<LuzDaBolinha,string>={carregando:'Carregando',quase:'Quase pronta!',pronta:'Pronta para ativar',usada:'Já usada nesta luta',apagada:'Esperando acontecer',acesa:'Ativa'};
/** A legenda do número grande, pelo jeito que a bolinha enche. */
function legendaDaBolinha(modo:string|undefined,texto:string):{valor:string;legenda:string}{
  switch(modo){
    case 'relogio':case 'tempo':return texto==='!'?{valor:'Agora',legenda:'ativa neste instante'}:{valor:texto,legenda:'até ativar'};
    case 'barra':return {valor:texto,legenda:'carregada'};
    case 'ciclo':case 'conta':return {valor:texto,legenda:texto==='1'?'falta 1 para ativar':'faltam para ativar'};
    case 'pilhas':return {valor:texto,legenda:'acumuladas'};
    case 'vida':return {valor:`${texto}%`,legenda:'ativa com essa Vida ou menos'};
    case 'chance':return {valor:texto,legenda:'de chance cada vez'};
    default:return {valor:texto,legenda:'agora'};
  }
}
function AbaDaUnica({battle,f,ativa,onSelect}:{battle:Battle;f:Fighter;ativa:boolean;onSelect:(t:InspectTarget)=>void}){
  const c=byId[f.characterId];
  if(!unicaDe(c.id))return null;
  const spec=bolinhaDe(c.id),b=bolinhaNaTela(spec,f,battle),Ic=spec.ic;
  return <button className={`bi2-aba unica ${ativa?'ativa':''}`} style={{'--u':corDaBolinha(c.id)} as CSSProperties} onClick={()=>onSelect({kind:'unica',fighter:f})} aria-label={unicaDe(c.id)!.nome} aria-current={ativa}>
    <span className="bi2-anel" style={{'--p':b.carga*100} as CSSProperties}><Ic size={18}/></span>
  </button>;
}
function FichaDaUnica({battle,f,onSelect}:{battle:Battle;f:Fighter;onSelect:(t:InspectTarget)=>void}){
  const c=byId[f.characterId],unica=unicaDe(c.id)!,spec=bolinhaDe(c.id),b=bolinhaNaTela(spec,f,battle),Ic=spec.ic,cor=corDaBolinha(c.id)??'#c58bff';
  const num=b.texto?legendaDaBolinha(spec.modo,b.texto):undefined,situacao=SITUACAO[b.luz];
  return <>
    <header className={`bi2-topo unica luz-${b.luz}`} style={{'--u':cor} as CSSProperties}>
      <span className={`bi2-anel grande ${b.luz==='pronta'||b.luz==='quase'?'pronta':''}`} style={{'--p':b.carga*100} as CSSProperties}><Ic size={36}/></span>
      <div className="bi2-nome">
        <small><Sparkles size={11}/> Mecânica única · {c.name}</small>
        <h3>{unica.nome}</h3>
        <span className={`bi2-situacao ${b.luz==='pronta'||b.luz==='quase'?'pronta':''}`}><Ic size={13}/>{situacao}</span>
      </div>
    </header>
    {num&&b.luz!=='usada'&&<div className="bi2-valor" style={{'--i':0} as CSSProperties}><b>{num.valor}</b><span>{num.legenda}</span></div>}
    {b.pontos&&<div className="bi2-gomos" style={{'--i':1,'--u':cor} as CSSProperties} aria-label={`${b.pontos.tem} de ${b.pontos.max}`}>
      {Array.from({length:b.pontos.max},(_,k)=><span key={k} className={k<b.pontos!.tem?'cheio':''}><Ic size={16}/></span>)}
      <small>{b.pontos.tem} de {b.pontos.max}</small>
    </div>}
    <section className="bi2-cartao unica" style={{'--i':2} as CSSProperties}>
      <span className="bi2-selo"><Info size={12}/><TermoBotao termo={termoPorId['mecanica-unica']!}>O que faz</TermoBotao></span>
      <p><ComTermos texto={unica.texto}/></p>
    </section>
    <nav className="bi2-trilha" aria-label="Trocar de ficha">
      <button className="bi2-voltar" onClick={()=>onSelect({kind:'fighter',fighter:f})} aria-label={`Voltar para ${c.name}`}><ChevronLeft size={16}/><span className="bi2-mini"><Portrait character={c}/></span></button>
      {c.skills.map((s,k)=>{const ek=estadoDa(battle,f,k);return <button key={s.id} className={`bi2-aba ${ek.classe}`} onClick={()=>onSelect({kind:'skill',fighter:f,index:k})} aria-label={s.name}>
        <span className="bi2-anel" style={{'--p':ek.p} as CSSProperties}><SkillIcon type={s.icon} characterId={c.id} skillId={s.id} size={20}/></span>
      </button>;})}
      <AbaDaUnica battle={battle} f={f} ativa onSelect={onSelect}/>
    </nav>
  </>;
}
