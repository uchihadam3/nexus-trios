import { useEffect,useState,type CSSProperties,type ReactNode } from 'react';
import { ArrowRight,RotateCcw,Home,Trophy,HeartPulse,TrendingUp,Shield,Crown,Sparkles,Medal,LogOut,Swords,Skull,Zap,Lightbulb } from 'lucide-react';
import type { Run } from '../lib/storage';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { summarizeBattle } from '../engine/run-summary';
import { formatarPontos,pontosDaJornada,pontosDaLuta } from '../engine/pontos';
import { lerRaioX,quemAbsorveu,type Direcao } from '../engine/raio-x';
import { mensagemDoTop3,type ResultadoTop3 } from '../lib/top3';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';

/*
 * A tela depois de cada luta (remake).
 *
 * O objetivo do jogo é fazer pontos: ir o mais longe possível nas 10 lutas e
 * subir no ranking. Então o centro da tela é o placar — os pontos desta luta
 * sobem contando, as parcelas aparecem uma a uma (vitória, Vida, de pé,
 * viradas), e depois o total da jornada sobe do que era para o que ficou.
 * Passou o recorde, a tela comemora.
 *
 * Embaixo, sem parede de texto: a trilha das 10 lutas, quem ajudou quem (em
 * números de jogo — "1,5 habilidade a mais", não "233 vezes") e o botão
 * grande para a próxima luta.
 */
const reduzido=()=>typeof matchMedia!=='undefined'&&matchMedia('(prefers-reduced-motion: reduce)').matches;

/** Um número que sobe contando. */
function Contador({de,para,ms=1100}:{de:number;para:number;ms?:number}){
  const [v,setV]=useState(reduzido()?para:de);
  useEffect(()=>{
    if(reduzido()){setV(para);return;}
    let raf=0;const t0=performance.now();
    const passo=(agora:number)=>{
      const t=Math.max(0,Math.min(1,(agora-t0)/ms)),e=1-Math.pow(1-t,3);
      setV(de+(para-de)*e);
      if(t<1)raf=requestAnimationFrame(passo);
    };
    raf=requestAnimationFrame(passo);
    return()=>cancelAnimationFrame(raf);
  },[de,para,ms]);
  return <>{formatarPontos(v)}</>;
}

/** Uma animação desenhada em Python (public/assets/ui/fx), tingida com a cor do momento. */
function Fx({nome,cor,ms=900,laco=false,className=''}:{nome:string;cor:string;ms?:number;laco?:boolean;className?:string}){
  return <span aria-hidden className={`uifx ${laco?'uifx-laco':''} ${className}`} style={{'--uifx-img':`url(/assets/ui/fx/${nome}.webp)`,'--uifx-cor':cor,'--uifx-dur':`${ms}ms`} as CSSProperties}/>;
}

interface Parcela {rotulo:string;valor:number;icone:ReactNode}

export function ResultScreen({run,onNext,onRestart,onAbandon,onHome,onRanking,onRetry,auto,onAuto}:{run:Run;onNext:()=>void;onRestart:()=>void;onAbandon:()=>void;onHome:()=>void;onRanking?:()=>void;onRetry?:()=>void;auto:boolean;onAuto:(v:boolean)=>void}){
  const b=run.battle!,won=b.winner==='player',champion=won&&run.index===9,fimDaJornada=champion||!won;
  const resumos=run.summaries?.length?run.summaries:[summarizeBattle(run.index,b,[],run.dicas===true)];
  const atual=resumos.find(s=>s.index===run.index)??summarizeBattle(run.index,b,[],run.dicas===true);
  // resumos salvos antes da conta nova não têm as parcelas: refaz pela luta
  const p=atual.pontos?.parcelas?atual.pontos:pontosDaLuta(b,run.index,run.dicas===true);
  const jornada=(ate:number)=>pontosDaJornada(resumos.filter(s=>s.index<=ate).map(s=>({pontos:s.score,won:s.won})));
  const antes=jornada(run.index-1),total=jornada(run.index);
  const recordeAntes=atual.recordeAntes??0,novoRecorde=total>0&&total>recordeAntes;
  const vitorias=resumos.filter(s=>s.won).length;

  // cada parcela da luta com o seu ícone (a conta vem de src/engine/pontos.ts, a mesma do ranking)
  const ICONE:Record<string,ReactNode>={dano:<Swords size={15}/>,nocautes:<Skull size={15}/>,apoio:<Shield size={15}/>,jogadas:<Zap size={15}/>,viradas:<TrendingUp size={15}/>,vitoria:<Trophy size={15}/>,efeitos:<Sparkles size={15}/>,vida:<HeartPulse size={15}/>,ajuda:<Lightbulb size={15}/>};
  const parcelas:Parcela[]=p.parcelas.map(x=>({rotulo:x.rotulo,valor:x.valor,icone:ICONE[x.id]}));

  /* A sequência do placar: parcelas uma a uma, depois o total sobe, depois o recorde. */
  const [fase,setFase]=useState(reduzido()?3:0);
  useEffect(()=>{
    if(reduzido())return;
    const tempos=[350,350+parcelas.length*260+400,350+parcelas.length*260+400+1300];
    const ids=tempos.map((t,i)=>window.setTimeout(()=>{setFase(i+1);battleAudio.sound(i===2&&novoRecorde?'pronto':'toque',PRIORIDADE.interface);},t));
    return()=>ids.forEach(clearTimeout);
    // a sequência roda uma vez por luta
  },[run.index]);

  const trio=b.fighters.filter(f=>f.side==='player');
  const pesoDoMvp=(f:typeof trio[number])=>f.stats.damage+f.stats.healing+f.stats.protection+f.stats.interrupts*100+f.stats.kills*150;
  const mvp=[...trio].sort((a,z)=>pesoDoMvp(z)-pesoDoMvp(a))[0];

  const ajudas:Direcao[]=run.raioX?lerRaioX(run.raioX,b).flatMap(par=>[par.aParaB,par.bParaA]).filter(d=>d.destaque&&d.tipo!=='conflito').slice(0,4):[];
  const pressao=run.raioX?quemAbsorveu(run.raioX,b):null;
  const lutador=(uid:string)=>byId[b.fighters.find(f=>f.uid===uid)?.characterId??''];

  const cor=won?(champion?'#ffd36b':'#b8f07a'):'#ff8a7a';
  const proximo=won&&!champion?run.encounters[run.index+1]:null;

  return <section className={`result-v2 ${won?'vitoria':'derrota'} ${champion?'campeao':''}`} style={{'--res-cor':cor} as CSSProperties}>
    <header className="rs-topo">
      <div className="rs-medalha">
        {won&&<Fx nome="raios" cor={cor} ms={2400} laco className="rs-raios"/>}
        <Fx nome="faiscas" cor={cor} ms={3600} laco className="rs-faiscas"/>
        <span className="rs-icone">{champion?<Crown size={40}/>:won?<Trophy size={38}/>:<Shield size={36}/>}</span>
      </div>
      <div className="rs-titulo">
        <span className="rs-confronto">{champion?'DEZ DE DEZ':`LUTA ${run.index+1} DE 10`}</span>
        <h1>{champion?'TRIO CAMPEÃO':won?'VITÓRIA':'DERROTA'}</h1>
      </div>
      <div className="rs-trio">{run.team.map((id,i)=>{const f=trio[i];const caiu=!!f&&f.hp<=0;return <span key={id} className={`${caiu?'caiu':''} ${f?.uid===mvp?.uid?'mvp':''}`} style={{'--character':byId[id].color,'--i':i} as CSSProperties}>
        <Portrait character={byId[id]} className="tiny"/>{f?.uid===mvp?.uid&&<b className="rs-mvp"><Medal size={11}/>MVP</b>}</span>;})}</div>
    </header>

    <div className="rs-placar">
      {/* na derrota também: os pontos do que o trio fez nesta luta ficam */}
      {p.total>0?<>
        <span className="rs-rotulo">PONTOS DESTA LUTA{p.multiplicador>1?` · ×${p.multiplicador.toFixed(2).replace('.',',')}`:''}</span>
        <strong className="rs-desta">+{fase>=1?<Contador de={0} para={p.total} ms={900}/>:'0'}</strong>
        <ul className="rs-parcelas">{parcelas.map((x,i)=><li key={x.rotulo} className={`${fase>=1?'entra':''} ${x.valor<0?'custo':''}`} style={{'--i':i} as CSSProperties}>{x.icone}<span>{x.rotulo}</span><b>{x.valor<0?'−':'+'}{formatarPontos(Math.abs(x.valor))}</b></li>)}</ul>
      </>:<p className="rs-sem">Nenhum ponto nesta luta: a jornada termina aqui com o que você já fez.</p>}
      <div className={`rs-total ${fase>=2?'subiu':''}`}>
        {fase>=2&&p.total>0&&<Fx nome="pontos" cor={cor} ms={900} className="rs-estouro"/>}
        <span className="rs-rotulo">{fimDaJornada?'PONTUAÇÃO FINAL':'TOTAL DA JORNADA'}</span>
        <strong>{fase>=2?<Contador de={antes} para={total} ms={1200}/>:formatarPontos(antes)}</strong>
        <small>{vitorias} {vitorias===1?'vitória':'vitórias'} · {formatarPontos(total)} pontos para o ranking</small>
      </div>
      <div className={`rs-recorde ${fase>=3&&novoRecorde?'novo':''}`}>
        {fase>=3&&novoRecorde&&<Fx nome="recorde" cor="#ffd36b" ms={1100} className="rs-estouro-recorde"/>}
        {fase>=3&&novoRecorde?<><Sparkles size={16}/><b>NOVO RECORDE!</b>{recordeAntes>0&&<span>antes: {formatarPontos(recordeAntes)}</span>}</>
          :<><span>Seu recorde</span><b>{formatarPontos(Math.max(recordeAntes,total))}</b>{recordeAntes>total&&<span>faltam {formatarPontos(recordeAntes-total)}</span>}</>}
      </div>
    </div>

    <ol className="rs-trilha" aria-label="As 10 lutas da jornada">{Array.from({length:10},(_,i)=>{const r=resumos.find(s=>s.index===i);const marca=r?(r.won?'ganhou':'perdeu'):i===run.index+1&&won?'proxima':'';
      return <li key={i} className={`${marca} ${i===run.index?'agora':''}`} title={r?`Luta ${i+1}: ${r.won?'+'+formatarPontos(r.score):'derrota'}`:`Luta ${i+1}`}>{i===9?<Crown size={12}/>:i+1}</li>;})}</ol>

    {(ajudas.length>0||pressao)&&<section className="rs-ajudas" aria-label="Quem ajudou quem">
      <h2>Quem ajudou quem</h2>
      <div>{ajudas.map(d=>{const de=lutador(d.de),para=lutador(d.para);if(!de||!para)return null;return <article key={`${d.de}-${d.para}`} className={`rs-ajuda tipo-${d.tipo}`}>
        <div className="rs-dupla"><span style={{'--character':de.color} as CSSProperties}><Portrait character={de} className="tiny"/></span><ArrowRight size={14}/><span style={{'--character':para.color} as CSSProperties}><Portrait character={para} className="tiny"/></span></div>
        <div className="rs-ajuda-numero"><b>{d.destaque!.numero}</b><small>{d.destaque!.rotulo}</small></div>
        <p><b>{de.name.split(/[ ,]/)[0]}</b> {d.frase}</p>
      </article>;})}
      {pressao&&(()=>{const quem=lutador(pressao.uid);return quem?<article className="rs-ajuda tipo-pressao">
        <div className="rs-dupla"><span style={{'--character':quem.color} as CSSProperties}><Portrait character={quem} className="tiny"/></span><Shield size={16}/></div>
        <div className="rs-ajuda-numero"><b>{Math.round(pressao.parte*100)}%</b><small>do dano levado</small></div>
        <p><b>{quem.name.split(/[ ,]/)[0]}</b> segurou a pressão pelo trio</p>
      </article>:null;})()}
      </div>
    </section>}

    {run.ranked&&fimDaJornada&&<div className="rs-ranqueada" role="status"><strong>RANKING</strong>
      {run.ranked.status==='verified'?<><span>Pontuação validada: <b>{formatarPontos(run.ranked.score??0)}</b></span><span>Posição: hoje #{run.ranked.daily??'—'} · semana #{run.ranked.weekly??'—'} · geral #{run.ranked.season??'—'}</span>{(run.ranked.top3?.temporada??run.ranked.top3?.periodo)&&<AvisoTop3 resultado={(run.ranked.top3?.temporada??run.ranked.top3?.periodo)!}/>}</>
        :run.ranked.status==='failed'?<><span>{/vers[aã]o/i.test(run.ranked.error??'')?'Esta jornada começou numa versão antiga do jogo e não pode entrar no ranking. Atualize o jogo e jogue de novo.':`Validação pendente: ${run.ranked.error}`}</span>{onRetry&&<button className="secondary" onClick={onRetry}>Tentar validar de novo</button>}</>
        :<span>Validando no servidor…</span>}
      {onRanking&&<button className="text-button" onClick={onRanking}>Ver ranking →</button>}</div>}

    {proximo&&<div className="rs-proximo"><span>PRÓXIMA LUTA<b>{proximo.name}</b></span><div>{proximo.team.map(id=><Portrait key={id} character={byId[id]} className="tiny"/>)}</div></div>}
    {won&&!champion&&<label className="auto-label rs-auto"><input type="checkbox" checked={auto} onChange={e=>onAuto(e.target.checked)}/>{auto?'Próxima luta em instantes':'Avançar sozinho entre as lutas'}</label>}
    {fimDaJornada&&!run.ranked&&<div className="rs-ranqueada fora" role="status"><strong>FORA DO RANKING</strong><span>Esta jornada foi jogada sem a conta conectada (ou sem internet ao começar), então não foi para o ranking. Entre na sua conta antes de jogar para as próximas valerem.</span>{onRanking&&<button className="text-button" onClick={onRanking}>Ver o ranking →</button>}</div>}

    <footer className="rs-acoes">
      {won&&!champion?<button className="rs-cta" onClick={onNext}><Fx nome="brilho" cor="#ffffff" ms={2600} laco className="rs-brilho"/><span>Próxima luta</span><ArrowRight size={20}/></button>
        :<button className="rs-cta" onClick={onRestart}><Fx nome="brilho" cor="#ffffff" ms={2600} laco className="rs-brilho"/><span>Jogar de novo</span><RotateCcw size={19}/></button>}
      <button className="secondary rs-icone-botao" onClick={onHome} aria-label="Início" title="Início"><Home size={19}/></button>
      {won&&!champion&&<button className="secondary rs-icone-botao rs-desistir" onClick={onAbandon} aria-label="Desistir da jornada" title="Desistir da jornada"><LogOut size={18}/></button>}
    </footer>
  </section>;
}

/*
 * O que esta partida fez com os seus 3 melhores trios do período — "NOVO TOP
 * 3", "Para entrar: supere 1.300". Só aparece quando o servidor já manda a
 * resposta da FASE K.
 */
function AvisoTop3({resultado}:{resultado:ResultadoTop3}){
  const m=mensagemDoTop3(resultado);
  return <div className={`top3-aviso${m.destaque?' destaque':''}`}><b>{m.titulo}</b>{m.linhas.map(l=><span key={l}>{l}</span>)}</div>;
}
