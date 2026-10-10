import type { CSSProperties } from 'react';
import { ArrowRight,Trophy,CircleHelp,Settings2,Download,Users,Crown,ShieldCheck,Play,LogOut } from 'lucide-react';
import { byId,characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { BotaoDicas } from '../components/BotaoDicas';
import type { Profile, Run } from '../lib/storage';
import {onlineConfigured} from '../lib/online';
import { formatarPontos,pontosDaJornada } from '../engine/pontos';

/*
 * A tela inicial (remake).
 *
 * Tela de jogo, não página: o logo vivo, o trio em medalhões, o recorde de
 * pontos grande — o objetivo do jogo — e um botão JOGAR que não tem como
 * passar despercebido. Com uma jornada em andamento, o botão vira "Continuar"
 * e mostra a luta e os pontos de agora. O resto do jogo fica num painel de
 * botões-ícone, como o menu de um jogo.
 */
interface Props {profile:Profile;run:Run|null;conta:boolean;/** Dicas de trio: decididas aqui, antes da jornada */dicas:boolean;podeDicas:boolean;onDicas:(ligar:boolean)=>void;onPlay:()=>void;onContinue:()=>void;onAbandon:()=>void;onNavigate:(s:'characters'|'ranking'|'conta'|'help'|'settings')=>void;onInstall:()=>void}

const Fx=({nome,cor,ms,className}:{nome:string;cor:string;ms:number;className:string})=>
  <span aria-hidden className={`uifx uifx-laco ${className}`} style={{'--uifx-img':`url(/assets/ui/fx/${nome}.webp)`,'--uifx-cor':cor,'--uifx-dur':`${ms}ms`} as CSSProperties}/>;

export function Home({profile,run,conta,dicas,podeDicas,onDicas,onPlay,onContinue,onAbandon,onNavigate,onInstall}:Props){
  const terminal=run?.stage==='result'&&(run.battle?.winner!=='player'||run.index===9);
  const wonCurrent=run?.stage==='result'&&run.battle?.winner==='player';
  const completed=run?run.index+(wonCurrent?1:0):0;
  const emAndamento=!!run&&!terminal;
  const trio=run?.team.length?run.team:profile.champion?.length?profile.champion:['goku','pikachu','gojo'];
  const pontosAgora=run?pontosDaJornada((run.summaries??[]).map(s=>({pontos:s.score,won:s.won}))):0;
  const recorde=profile.recordePontos??0;
  const rotuloDoTrio=emAndamento&&run?.team.length?'SEU TRIO EM CAMPO':profile.champion?.length?'ÚLTIMO TRIO CAMPEÃO':'MONTE UM TRIO COMO ESTE';

  return <section className="home-v2">
    <header className="hv-logo">
      <Fx nome="raios" cor="#c8f560" ms={5200} className="hv-raios"/>
      <Fx nome="faiscas" cor="#c8f560" ms={4200} className="hv-faiscas"/>
      <h1><span>NEXUS</span><small>DUELO DE TRIOS</small></h1>
    </header>

    <div className="hv-trio" aria-label={rotuloDoTrio}>
      {trio.map((id,i)=>{const c=byId[id];return <span key={id} className={`hv-medalhao m${i}`} style={{'--character':c.color,'--i':i} as CSSProperties}>
        <Portrait character={c}/><b>{c.name}</b></span>;})}
      <small>{rotuloDoTrio}</small>
    </div>

    <div className="hv-recorde">
      <Crown size={18}/><span>SEU RECORDE</span><strong>{formatarPontos(recorde)}</strong><em>pontos</em>
    </div>

    <div className="hv-jogar">
      {emAndamento?<button className="hv-cta" onClick={onContinue} aria-label="Continuar jornada">
          <Fx nome="brilho" cor="#ffffff" ms={2600} className="hv-brilho"/>
          <Play size={26} fill="currentColor"/><span><b>CONTINUAR</b><small>{run!.stage==='draft'?'Escolha seu trio':`Luta ${Math.min(10,completed+1)} de 10 · ${formatarPontos(pontosAgora)} pontos`}</small></span><ArrowRight size={22}/>
        </button>
        :<button className="hv-cta" onClick={run?onContinue:onPlay} aria-label={run?'Ver resultado':'Montar meu trio'}>
          <Fx nome="brilho" cor="#ffffff" ms={2600} className="hv-brilho"/>
          <Play size={26} fill="currentColor"/><span><b>{run?'VER RESULTADO':'JOGAR'}</b><small>{run?`${formatarPontos(pontosAgora)} pontos nesta jornada`:onlineConfigured&&conta?'10 lutas · vale o ranking':'10 lutas · máximo de pontos'}</small></span><ArrowRight size={22}/>
        </button>}
      {!emAndamento&&<div className="hv-dicas"><BotaoDicas ligado={dicas} liberado={podeDicas} onMudar={onDicas}/></div>}
      {emAndamento&&<div className="hv-trilha" aria-label={`${completed} de 10 lutas vencidas`}>{Array.from({length:10},(_,i)=><i key={i} className={i<completed?'ok':i===completed?'agora':''}/>)}</div>}
      {(emAndamento||terminal)&&<div className="hv-secundarias">
        {terminal&&<button className="secondary" onClick={onPlay}><Play size={15}/>Nova jornada</button>}
        {emAndamento&&<button className="text-button hv-desistir" onClick={onAbandon}><LogOut size={14}/>Desistir desta jornada</button>}
      </div>}
    </div>

    <nav className="hv-menu" aria-label="Menu do jogo">
      <button onClick={()=>onNavigate('characters')} style={{'--tile':'#ffb86b'} as CSSProperties}><Users size={22}/><b>Personagens</b><small>{characters.length} lutadores</small></button>
      <button onClick={()=>onNavigate('ranking')} style={{'--tile':'#ffd36b'} as CSSProperties}><Trophy size={22}/><b>Ranking</b><small>os melhores</small></button>
      <button onClick={()=>onNavigate('help')} style={{'--tile':'#8fd3ff'} as CSSProperties}><CircleHelp size={22}/><b>Como jogar</b><small>em 1 minuto</small></button>
      <button onClick={()=>onNavigate('settings')} style={{'--tile':'#c3a2ff'} as CSSProperties}><Settings2 size={22}/><b>Ajustes</b><small>som e visual</small></button>
      <button onClick={()=>onNavigate('conta')} style={{'--tile':'#86e3a8'} as CSSProperties}><ShieldCheck size={22}/><b>Conta</b><small>{conta?'conectada':'para o ranking'}</small></button>
      <button onClick={onInstall} style={{'--tile':'#ff9a8a'} as CSSProperties}><Download size={22}/><b>Instalar</b><small>no celular</small></button>
    </nav>

    <p className="hv-numeros"><span><b>{profile.journeys}</b> jornadas</span><span><b>{profile.victories}</b> {profile.victories===1?'trio campeão':'trios campeões'}</span><span><b>{profile.best}</b>/10 melhor campanha</span></p>
  </section>;
}
