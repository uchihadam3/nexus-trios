import type { CSSProperties } from 'react';
import { ArrowRight,MessagesSquare,Swords,Award,BookOpen,ChevronRight,Zap,Trophy,CircleHelp,Settings2,Download,Users,Crown,ShieldCheck,Play,LogOut,Share2,MessageCircle,Instagram,Facebook,KeyRound,Lock,Sparkles } from 'lucide-react';
import '../presentation/compartilhar.css';
import '../presentation/segredos.css';
import { byId,characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { jornadaAcabou,type Profile,type Run } from '../lib/storage';
import { LUTA_ESTRELA,SEGREDOS,ehLutaExtra,normaisVencidas } from '../engine/segredos';
import {onlineConfigured} from '../lib/online';
import { formatarPontos,pontosDaJornada } from '../engine/pontos';
import { TOTAL_DE_CONQUISTAS,desafioDoDia,tituloDe } from '../lib/conquistas';
import { TODOS_OS_COMBOS } from '../components/CombosDoTrio';
import { Avatar } from '../components/AvatarDaComunidade';
import type { Jogador } from '../lib/comunidade';
import { NPCS } from '../engine/pvp';
import '../presentation/pvp.css';

/*
 * A tela inicial (remake).
 *
 * Tela de jogo, não página: o logo vivo, o trio em medalhões, o recorde de
 * pontos grande — o objetivo do jogo — e um botão JOGAR que não tem como
 * passar despercebido. Com uma jornada em andamento, o botão vira "Continuar"
 * e mostra a luta e os pontos de agora. O resto do jogo fica num painel de
 * botões-ícone, como o menu de um jogo.
 */
interface Props {comunidade:{online:Jogador[]|null;naoLidas:number}|null;profile:Profile;run:Run|null;conta:boolean;onPlay:()=>void;onContinue:()=>void;onAbandon:()=>void;onNavigate:(s:'characters'|'conquistas'|'combos'|'segredos'|'ranking'|'conta'|'help'|'settings'|'comunidade'|'pvp')=>void;onInstall:()=>void;onShare:()=>void}

const Fx=({nome,cor,ms,className}:{nome:string;cor:string;ms:number;className:string})=>
  <span aria-hidden className={`uifx uifx-laco ${className}`} style={{'--uifx-img':`url(/assets/ui/fx/${nome}.webp)`,'--uifx-cor':cor,'--uifx-dur':`${ms}ms`} as CSSProperties}/>;

export function Home({comunidade,profile,run,conta,onPlay,onContinue,onAbandon,onNavigate,onInstall,onShare}:Props){
  const terminal=!!run&&jornadaAcabou(run);
  const wonCurrent=run?.stage==='result'&&run.battle?.winner==='player';
  const completed=run?normaisVencidas(run.summaries??[]):0,naExtra=!!run&&ehLutaExtra(run.index)&&run.stage==='battle';
  void wonCurrent;
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
          <Play size={26} fill="currentColor"/><span><b>CONTINUAR</b><small>{run!.stage==='draft'?'Escolha seu trio':`${naExtra?(run!.index===LUTA_ESTRELA?'Luta secreta ★':'Luta 11 · secreta'):`Luta ${Math.min(10,completed+1)} de 10`} · ${formatarPontos(pontosAgora)} pontos`}</small></span><ArrowRight size={22}/>
        </button>
        :<button className="hv-cta" onClick={run?onContinue:onPlay} aria-label={run?'Ver resultado':'Montar meu trio'}>
          <Fx nome="brilho" cor="#ffffff" ms={2600} className="hv-brilho"/>
          <Play size={26} fill="currentColor"/><span><b>{run?'VER RESULTADO':'JOGAR'}</b><small>{run?`${formatarPontos(pontosAgora)} pontos nesta jornada`:onlineConfigured&&conta?'10 lutas · vale o ranking':'10 lutas · máximo de pontos'}</small></span><ArrowRight size={22}/>
        </button>}
      {emAndamento&&<div className="hv-trilha" aria-label={`${completed} de 10 lutas vencidas`}>{Array.from({length:10},(_,i)=><i key={i} className={i<completed?'ok':i===completed?'agora':''}/>)}</div>}
      {(emAndamento||terminal)&&<div className="hv-secundarias">
        {terminal&&<button className="secondary" onClick={onPlay}><Play size={15}/>Nova jornada</button>}
        {emAndamento&&<button className="text-button hv-desistir" onClick={onAbandon}><LogOut size={14}/>Desistir desta jornada</button>}
      </div>}
    </div>

    <div className="hv-faixas">
    {/* A Arena PvP (src/screens/PvpScreen.tsx): treino contra os 6 NPCs; o desafio online vem depois */}
    <button className="hv-conquistas-faixa hv-pvp-faixa" onClick={()=>onNavigate('pvp')} aria-label={`Arena PvP: treine contra ${NPCS.length} NPCs`}>
      <span className="hv-cq-icone"><Swords size={22}/></span>
      <span className="hv-cq-texto"><b>ARENA PvP</b><small>3 times de 3 · treine contra {NPCS.length} NPCs, do Novato à Lenda</small></span>
      <span className="hv-cq-ultimos" aria-hidden="true">{NPCS.slice(3).map(n=><span key={n.id} className="pv-npc-avatar" style={{'--npc':n.cor,'--t':'30px'} as CSSProperties}><Portrait character={byId[n.avatar]}/><i/></span>)}</span>
      <ChevronRight size={20}/>
    </button>
    {/* A Comunidade (src/screens/ComunidadeScreen.tsx): quem está online agora, e as privadas não lidas. */}
    {comunidade&&<button className="hv-conquistas-faixa hv-comunidade-faixa" onClick={()=>onNavigate('comunidade')} aria-label={`Comunidade: ${comunidade.online?.length??0} online${comunidade.naoLidas?`, ${comunidade.naoLidas} mensagens novas`:''}`}>
      <span className="hv-cq-icone"><MessagesSquare size={22}/>{comunidade.naoLidas>0&&<em>{comunidade.naoLidas}</em>}</span>
      <span className="hv-cq-texto"><b>COMUNIDADE</b><small>{comunidade.naoLidas>0?<strong>{comunidade.naoLidas} {comunidade.naoLidas===1?'mensagem nova':'mensagens novas'}</strong>:<span className="hv-cm-online"><span className="cm-ponto vivo"/>{comunidade.online===null?'chat e jogadores':`${comunidade.online.length+1} online agora`}</span>}</small></span>
      <span className="hv-cq-ultimos" aria-hidden="true">{(comunidade.online??[]).slice(0,3).map(j=><Avatar key={j.id} jogador={j} id={j.id} nome={j.nome} tamanho={30}/>)}</span>
      <ChevronRight size={20}/>
    </button>}
    {/* As Conquistas: quantos já foram liberados, o título e os últimos liberados. */}
    {(()=>{const lista=Object.entries(profile.conquistas??{}).sort((a,b)=>b[1].localeCompare(a[1])),n=lista.length,t=tituloDe(n),novas=lista.filter(([id])=>!(profile.conquistasVistas??[]).includes(id)).length,desafios=desafioDoDia(profile.desafio,profile.conquistas??{}).ids.filter(id=>!profile.conquistas?.[id]).length;
      return <button className="hv-conquistas-faixa" onClick={()=>onNavigate('conquistas')} style={{'--titulo':t.atual.cor} as CSSProperties} aria-label={`Conquistas: ${n} de ${TOTAL_DE_CONQUISTAS}`}>
        <span className="hv-cq-icone"><Award size={24}/>{novas>0&&<em>{novas}</em>}</span>
        <span className="hv-cq-texto"><b>CONQUISTAS</b><small>{t.atual.nome} · <strong>{n}</strong>/{TOTAL_DE_CONQUISTAS}{desafios>0&&<em className="hv-cq-desafio"><Zap size={10}/>{desafios} {desafios===1?'desafio':'desafios'} hoje</em>}</small><span className="hv-cq-barra"><i style={{width:`${(n/TOTAL_DE_CONQUISTAS)*100}%`}}/></span></span>
        <span className="hv-cq-ultimos">{lista.slice(0,3).map(([id])=>byId[id]&&<span key={id} style={{'--character':byId[id].color} as CSSProperties}><Portrait character={byId[id]}/></span>)}</span>
        <ChevronRight size={20}/>
      </button>;})()}
    {/* O Livro de Combos (src/screens/LivroDeCombos.tsx): quantos já foram descobertos, e os novos ainda não abertos. */}
    {(()=>{const achados=TODOS_OS_COMBOS.filter(c=>(profile.combosDescobertos??[]).includes(c.id)),novos=achados.filter(c=>!(profile.combosVistos??[]).includes(c.id)).length;
      return <button className="hv-conquistas-faixa hv-livro-faixa" onClick={()=>onNavigate('combos')} aria-label={`Livro de Combos: ${achados.length} de ${TODOS_OS_COMBOS.length}`}>
        <span className="hv-cq-icone"><BookOpen size={22}/>{novos>0&&<em>{novos}</em>}</span>
        <span className="hv-cq-texto"><b>LIVRO DE COMBOS</b><small><strong>{achados.length}</strong>/{TODOS_OS_COMBOS.length} descobertos</small><span className="hv-cq-barra"><i style={{width:`${100*achados.length/TODOS_OS_COMBOS.length}%`}}/></span></span>
      </button>;})()}
    {/* O Livro de Segredos (src/screens/LivroDeSegredos.tsx): os seis segredos, trancados até cumprir. */}
    {(()=>{const achados=SEGREDOS.filter(x=>(profile.segredosDescobertos??[]).includes(x.id)),novos=achados.filter(x=>!(profile.segredosVistos??[]).includes(x.id)).length;
      return <button className="hv-conquistas-faixa hv-segredos-faixa" onClick={()=>onNavigate('segredos')} aria-label={`Livro de Segredos: ${achados.length} de ${SEGREDOS.length}`}>
        <span className="hv-cq-icone"><KeyRound size={22}/>{novos>0&&<em>{novos}</em>}</span>
        <span className="hv-cq-texto"><b>LIVRO DE SEGREDOS</b><small><strong>{achados.length}</strong>/{SEGREDOS.length} descobertos</small></span>
        <span className="hv-sg-selos" aria-hidden="true">{SEGREDOS.map(x=>{const ok=achados.includes(x);return <i key={x.id} className={ok?'ok':''} style={{'--cor':x.cor} as CSSProperties}>{ok?<Sparkles size={10}/>:<Lock size={9}/>}</i>;})}</span>
        <ChevronRight size={20}/>
      </button>;})()}
    {/* Chamar amigos (src/components/CompartilharJogo.tsx): manda o convite pelo WhatsApp, Instagram, Facebook… */}
    <button className="hv-conquistas-faixa hv-convite-faixa" onClick={onShare} aria-label="Chamar amigos para jogar">
      <span className="hv-cq-icone"><Share2 size={22}/></span>
      <span className="hv-cq-texto"><b>CHAMAR AMIGOS</b><small>Mande o jogo pelo WhatsApp, Instagram, Facebook…</small></span>
      <span className="hv-cq-ultimos" aria-hidden="true"><span style={{'--cor':'#25d366'} as CSSProperties}><MessageCircle size={15}/></span><span className="ig"><Instagram size={15}/></span><span style={{'--cor':'#1877f2'} as CSSProperties}><Facebook size={15}/></span></span>
      <ChevronRight size={20}/>
    </button>
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
