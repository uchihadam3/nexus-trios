import { ArrowUpRight,ArrowRight,Trophy,CircleHelp,Settings2,Download,ChevronRight,Users,Swords,Flag,Star } from 'lucide-react';
import { byId,characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import type { Profile, Run } from '../lib/storage';

interface Props {profile:Profile;run:Run|null;onPlay:()=>void;onContinue:()=>void;onAbandon:()=>void;onNavigate:(s:'characters'|'help'|'settings')=>void;onInstall:()=>void}
export function Home({profile,run,onPlay,onContinue,onAbandon,onNavigate,onInstall}:Props){
  const terminal=run?.stage==='result'&&(run.battle?.winner!=='player'||run.index===9);
  const wonCurrent=run?.stage==='result'&&run.battle?.winner==='player';
  const champion=terminal&&wonCurrent;
  const completed=run?run.index+(wonCurrent?1:0):0;
  const current=run?Math.min(9,completed):0;
  const enemies=run&&!terminal?run.encounters[current]?.team:undefined;
  const trio=run?.team.length?run.team:profile.champion?.length?profile.champion:['goku','pikachu','gojo'];
  return <section className="game-hub">
    <div className="hub-hero">
      <div className="hub-copy"><span className="eyebrow"><Star size={13}/> {terminal?champion?'TRIO CAMPEÃO':'JORNADA ENCERRADA':run?'JORNADA EM ANDAMENTO':'SUA PRÓXIMA JORNADA'}</span>
        <h1>{run?terminal?champion?'Dez vitórias. Seu trio é campeão.':`Sua jornada terminou no confronto ${run.index+1}.`:`Confronto ${current+1} de 10`:'Monte seu trio. Escreva a próxima vitória.'}</h1>
        <p>{run?run.stage==='draft'?'Escolha seus três personagens. Cada escolha muda a equipe.':terminal?champion?'Reviva o último duelo e veja como seu trio conquistou o título.':'Veja o resultado e monte um novo trio para tentar de novo.':`Próximo desafio: ${run.encounters[current]?.name}`:'Dez confrontos. Um trio. Cada ação mostra quem ajudou, quem atacou e quem virou a luta.'}</p>
        <button className="primary hero-cta" onClick={run?onContinue:onPlay}>{terminal?champion?'Ver título':'Ver resultado':run?'Continuar jornada':'Montar meu trio'}<ArrowUpRight size={20}/></button>
        {run&&!terminal&&<button className="abandon-campaign" onClick={onAbandon}>Desistir desta jornada</button>}
        <div className="hub-hero-stats"><span><b>{profile.best}<small>/10</small></b> recorde</span><span><b>{profile.victories}</b> trios campeões</span><span><b>{profile.journeys}</b> jornadas</span></div>
      </div>
      <div className="hub-team"><span className="eyebrow">{terminal?champion?'TRIO CAMPEÃO':'TRIO DA JORNADA':run?.team.length?'TRIO EM CAMPO':profile.champion?.length?'ÚLTIMO TRIO CAMPEÃO':'TRIO PARA COMEÇAR'}</span><div>{trio.map((id,i)=>{const c=byId[id];return <span key={id} className={`hub-unit hub-unit-${i}`} style={{'--character':c.color} as React.CSSProperties}><Portrait character={c}/><strong>{c.name}</strong></span>})}</div><small>{terminal?champion?'Dez confrontos vencidos juntos.':`Chegou ao confronto ${(run?.index??0)+1} desta jornada.`:run?.team.length?'Seu time segue junto até o fim da jornada.':'A escolha do seu trio começa no Draft.'}</small></div>
    </div>
    <div className="hub-progress"><div className="section-heading"><div><span className="eyebrow"><Flag size={13}/> TRILHA DA JORNADA</span><h2>{run?`${completed} de 10 confrontos vencidos`:'Dez passos até o título'}</h2></div><span className="record">RECORDE <strong>{profile.best}<small>/10</small></strong></span></div>
      <div className="milestones game-trail" aria-label="Progresso de dez confrontos">{Array.from({length:10},(_,i)=>{const done=run?i<completed:i<profile.best,active=i===current&&!terminal;return <div className={`${done?'complete':''} ${active?'next':''} ${i===9?'final':''}`} key={i} aria-label={`Confronto ${i+1}${done?', vencido':active?', próximo':''}`}><span>{i===9?<Trophy size={18}/>:String(i+1).padStart(2,'0')}</span></div>;})}</div>
      <div className="trail-callout"><span>{run?terminal?'JORNADA ENCERRADA':run.stage==='draft'?'PREPARE O TRIO':'PRÓXIMO NÓ DESBLOQUEADO':'PRIMEIRO PASSO'}</span><strong>{run&&!terminal?run.encounters[current]?.name:run&&terminal?`${completed} vitórias conquistadas`:'Monte seu trio para ativar a primeira luta'}</strong></div>
      <div className="journey-bottom"><span>{profile.journeys} jornadas · {profile.victories} trios campeões</span><button className="text-button" onClick={onPlay}>Nova jornada <ArrowRight size={15}/></button></div>
    </div>
    {enemies&&<div className="hub-encounter"><div><span className="eyebrow">RIVAIS DO PRÓXIMO CONFRONTO</span><h2>{run?.encounters[current].name}</h2><p>Entre na arena para descobrir como seu trio responde.</p></div><div className="hub-rivals">{enemies.map(id=><span key={id}><Portrait character={byId[id]}/><small>{byId[id].name}</small></span>)}</div></div>}
    <div className="hub-links"><button onClick={()=>onNavigate('characters')}><Users size={20}/><span><b>Personagens</b><small>Conheça os {characters.length} lutadores</small></span><ChevronRight size={17}/></button><button onClick={()=>onNavigate('help')}><CircleHelp size={20}/><span><b>Como jogar</b><small>Aprenda a ler a batalha</small></span><ChevronRight size={17}/></button><button onClick={()=>onNavigate('settings')}><Settings2 size={20}/><span><b>Configurações</b><small>Áudio, visual e jogo</small></span><ChevronRight size={17}/></button><button onClick={onInstall}><Download size={20}/><span><b>Instalar</b><small>Leve seu trio com você</small></span><ChevronRight size={17}/></button></div>
    <p className="hub-rule"><Swords size={17}/> A vitória acontece quando o trio rival inteiro sai da luta.</p>
  </section>;
}
