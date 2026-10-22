import { useEffect,useState,type CSSProperties,type ReactNode } from 'react';
import { ConquistasLiberadas } from './ConquistasScreen';
import { ArrowRight,RotateCcw,Home,Trophy,HeartPulse,TrendingUp,Shield,Crown,Sparkles,Medal,LogOut,Swords,Skull,Zap,Lightbulb,ThumbsDown,ThumbsUp,ArrowDown,Minus,Flame,Star,Lock,Award,type LucideIcon } from 'lucide-react';
import { loadProfile,proximaDaJornada,rivalAtual,type Run } from '../lib/storage';
import { LUTA_ESTRELA,LUTA_ONZE,PULOS_COM_O_LIVRO_COMPLETO,PULOS_DA_JORNADA,SEGREDO,ehLutaExtra,livroCompleto,segredosCumpridos,segredosDaLuta,type SegredoId } from '../engine/segredos';
import { ICONE_DO_SEGREDO } from '../components/SeloDoSegredo';
import '../presentation/segredos.css';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { summarizeBattle } from '../engine/run-summary';
import { formatarPontos,pontosDaJornada,pontosDaLuta } from '../engine/pontos';
import { ajudasDaLuta,type AjudasDaLuta } from '../engine/raio-x';
import { avaliarAjuda,avaliarDirecao,NOMES_DAS_NOTAS,type AvaliacaoDaAjuda } from '../engine/nota-da-ajuda';
import { mensagemDoTop3,type ResultadoTop3 } from '../lib/top3';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE } from '../audio/cues';
import { ChaveDoAuto,ESPERA_DA_PROXIMA_MS } from '../components/ChaveDoAuto';
import { nomeDe, numero, plural, t } from '../i18n/idioma';

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

/*
 * A nota da ajuda (pedido do jogador: "foi boa essa ajuda? … bater o olho e entender na hora"): uma régua de seis
 * gomos, do vermelho ao dourado, que enche até a nota; o selo com o nome e o ícone; e quanto ela ficou acima das
 * ajudas iguais em outras lutas (src/engine/nota-da-ajuda.ts).
 */
const ICONE_DA_NOTA:LucideIcon[]=[ThumbsDown,ArrowDown,Minus,ThumbsUp,Flame,Crown];
function NotaDaAjuda({av,i}:{av:AvaliacaoDaAjuda;i:number}){
  const Ic=ICONE_DA_NOTA[av.nota]!;
  return <div className={`rs-nota nota-${av.nota}`} style={{'--i':i} as CSSProperties}>
    <span className="rs-nota-regua" aria-hidden="true">{NOMES_DAS_NOTAS.map((_,k)=><i key={k} className={k<=av.nota?'acesa':''} style={{'--k':k} as CSSProperties}/>)}</span>
    <span className="rs-nota-selo"><Ic size={13} strokeWidth={2.6}/>{t(NOMES_DAS_NOTAS[av.nota]!)}</span>
    <small className="rs-nota-compara">{av.melhorQue>=50?t('Melhor que {n}% das ajudas desse tipo',{n:av.melhorQue}):av.melhorQue>0?t('Só melhor que {n}% das ajudas desse tipo',{n:av.melhorQue}):t('Das menores ajudas desse tipo')}</small>
  </div>;
}

export function ResultScreen({run,onNext,onRestart,onAbandon,onHome,onRanking,onRetry,auto,onAuto}:{run:Run;onNext:()=>void;onRestart:()=>void;onAbandon:()=>void;onHome:()=>void;onRanking?:()=>void;onRetry?:()=>void;auto:boolean;onAuto:(v:boolean)=>void}){
  const b=run.battle!,won=b.winner==='player',champion=won&&run.index===9,extra=ehLutaExtra(run.index);
  const resumos=run.summaries?.length?run.summaries:[summarizeBattle(run.index,b,[],run.dicas===true,run.colecao===true)];
  const atual=resumos.find(s=>s.index===run.index)??summarizeBattle(run.index,b,[],run.dicas===true,run.colecao===true);
  /* a próxima luta (a normal, ou uma luta extra liberada por um segredo: src/engine/segredos.ts) */
  const proxima=proximaDaJornada(run),fimDaJornada=proxima===null,segue=!fimDaJornada;
  // resumos salvos antes da conta nova não têm as parcelas: refaz pela luta
  const p=atual.pontos?.parcelas?atual.pontos:pontosDaLuta(b,run.index,run.dicas===true,run.colecao===true);
  /* os pontos somam na ordem em que as lutas foram jogadas (a ★ entre a 5 e a 6) */
  const posicao=Math.max(0,resumos.findIndex(s=>s.index===run.index));
  const jornada=(n:number)=>pontosDaJornada(resumos.slice(0,n).map(s=>({pontos:s.score,won:s.won})));
  const antes=jornada(posicao),total=jornada(posicao+1);
  /* os segredos cumpridos nesta luta: o aviso grande de SEGREDO DESCOBERTO */
  // (na Jornada com os seus os segredos não valem: nem o aviso, nem as lutas extras na trilha)
  const comSegredos=run.colecao!==true;
  const segredosAgora=comSegredos?segredosCumpridos(run.team,resumos.slice(0,posicao+1)):[],segredosAntes=comSegredos?segredosCumpridos(run.team,resumos.slice(0,posicao)):[];
  const descobertos=segredosAgora.filter(x=>!segredosAntes.includes(x));
  const estrelaLiberada=comSegredos&&segredosDaLuta(run.team,resumos.slice(0,posicao+1),'estrela').length>0,onzeLiberada=comSegredos&&segredosDaLuta(run.team,resumos.slice(0,posicao+1),'onze').length>0;
  const recordeAntes=atual.recordeAntes??0,novoRecorde=total>0&&total>recordeAntes;
  const vitorias=resumos.filter(s=>s.won).length;

  /* Lutas seguidas ligada: "Próxima luta" conta os segundos até a próxima começar sozinha (o tempo é o do App). */
  const vaiSozinha=auto&&segue;
  const [contando,setContando]=useState<{desde:number;faltam:number}|null>(null);
  useEffect(()=>{
    if(!vaiSozinha){setContando(null);return;}
    const desde=performance.now(),conta=()=>setContando({desde,faltam:Math.max(1,Math.ceil((ESPERA_DA_PROXIMA_MS-(performance.now()-desde))/1000))});
    conta();const id=window.setInterval(conta,250);
    return()=>clearInterval(id);
  },[vaiSozinha]);

  // cada parcela da luta com o seu ícone (a conta vem de src/engine/pontos.ts, a mesma do ranking)
  const ICONE:Record<string,ReactNode>={dano:<Swords size={15}/>,nocautes:<Skull size={15}/>,apoio:<Shield size={15}/>,jogadas:<Zap size={15}/>,viradas:<TrendingUp size={15}/>,vitoria:<Trophy size={15}/>,efeitos:<Sparkles size={15}/>,vida:<HeartPulse size={15}/>,estrela:<Star size={15}/>,ajuda:<Lightbulb size={15}/>,colecao:<Award size={15}/>};
  const parcelas:Parcela[]=p.parcelas.map(x=>({rotulo:t(x.rotulo),valor:x.valor,icone:ICONE[x.id]}));

  /* A sequência do placar: parcelas uma a uma, depois o total sobe, depois o recorde. */
  const [fase,setFase]=useState(reduzido()?3:0);
  useEffect(()=>{
    if(reduzido())return;
    const tempos=[350,350+parcelas.length*260+400,350+parcelas.length*260+400+1300];
    const ids=tempos.map((t,i)=>window.setTimeout(()=>{setFase(i+1);battleAudio.sound(i===2&&novoRecorde?'pronto':'toque',PRIORIDADE.interface);},t));
    // segredo descoberto: o som de conquista junto com o aviso
    if(descobertos.length)ids.push(window.setTimeout(()=>battleAudio.sound('pronto',PRIORIDADE.grand),tempos[2]!+500));
    return()=>ids.forEach(clearTimeout);
    // a sequência roda uma vez por luta
  },[run.index]);

  const trio=b.fighters.filter(f=>f.side==='player');
  const pesoDoMvp=(f:typeof trio[number])=>f.stats.damage+f.stats.healing+f.stats.protection+f.stats.interrupts*100+f.stats.kills*150;
  const mvp=[...trio].sort((a,z)=>pesoDoMvp(z)-pesoDoMvp(a))[0];

  /*
   * Quem ajudou quem, luta por luta (pedido do jogador: "clicar na bolinha… na terceira, na segunda, na primeira e ver
   * como é que foi, quem ajudou quem"): cada bolinha jogada da trilha abre o dela. A luta de agora sai do Raio-X ao
   * vivo; as outras, do que ficou guardado no resumo de cada uma.
   */
  const [vista,setVista]=useState(run.index);
  useEffect(()=>setVista(run.index),[run.index]);
  const resumoVisto=resumos.find(s=>s.index===vista);
  const dados:AjudasDaLuta|null=vista===run.index?(run.raioX?ajudasDaLuta(run.raioX,b):resumoVisto?.ajudas??null):resumoVisto?.ajudas??null;
  const ajudas=dados?.direcoes??[],pressao=dados?.pressao??null;
  const lutador=(uid:string)=>byId[dados?.quem[uid]??''];

  const cor=won?(champion||extra?'#ffd36b':'#b8f07a'):extra?'#b7a6d9':'#ff8a7a';
  const proximo=proxima!==null?rivalAtual(run,proxima):null;
  const rotuloDaLuta=(i:number)=>i===LUTA_ESTRELA?t('Luta ★'):i===LUTA_ONZE?t('Luta 11'):t('Luta {n}',{n:i+1});

  return <section className={`result-v2 ${won?'vitoria':'derrota'} ${champion||extra&&won?'campeao':''} ${extra?'luta-secreta':''}`} style={{'--res-cor':cor} as CSSProperties}>
    <header className="rs-topo">
      <div className="rs-medalha">
        {won&&<Fx nome="raios" cor={cor} ms={2400} laco className="rs-raios"/>}
        <Fx nome="faiscas" cor={cor} ms={3600} laco className="rs-faiscas"/>
        <span className="rs-icone">{extra?<Star size={38} fill={won?'currentColor':'none'}/>:champion?<Crown size={40}/>:won?<Trophy size={38}/>:<Shield size={36}/>}</span>
      </div>
      <div className="rs-titulo">
        <span className="rs-confronto">{run.index===LUTA_ESTRELA?t('LUTA SECRETA ★'):run.index===LUTA_ONZE?t('LUTA 11 · SECRETA'):champion?t('DEZ DE DEZ'):t('LUTA {n} DE 10',{n:run.index+1})}</span>
        <h1>{extra?(won?(run.index===LUTA_ONZE?t('LENDA SECRETA'):t('VITÓRIA SECRETA')):t('QUASE!')):champion?t('TRIO CAMPEÃO'):won?t('VITÓRIA'):t('DERROTA')}</h1>
      </div>
      <div className="rs-trio">{run.team.map((id,i)=>{const f=trio[i];const caiu=!!f&&f.hp<=0;return <span key={id} className={`${caiu?'caiu':''} ${f?.uid===mvp?.uid?'mvp':''}`} style={{'--character':byId[id].color,'--i':i} as CSSProperties}>
        <Portrait character={byId[id]} className="tiny"/>{f?.uid===mvp?.uid&&<b className="rs-mvp"><Medal size={11}/>{t('MVP')}</b>}</span>;})}</div>
    </header>

    <div className="rs-placar">
      {/* na derrota também: os pontos do que o trio fez nesta luta ficam */}
      {extra&&!won?<p className="rs-sem">{t('A luta secreta só vale pontos com vitória.')} {segue?t('A jornada segue para a luta 6, com tudo o que você já fez.'):t('A jornada termina aqui, com tudo o que você já fez.')}</p>:p.total>0?<>
        <span className="rs-rotulo">{t('PONTOS DESTA LUTA')}{p.multiplicador>1?` · ×${numero(p.multiplicador,{minimumFractionDigits:2,maximumFractionDigits:2})}`:''}</span>
        <strong className="rs-desta">+{fase>=1?<Contador de={0} para={p.total} ms={900}/>:'0'}</strong>
        <ul className="rs-parcelas">{parcelas.map((x,i)=><li key={x.rotulo} className={`${fase>=1?'entra':''} ${x.valor<0?'custo':''}`} style={{'--i':i} as CSSProperties}>{x.icone}<span>{x.rotulo}</span><b>{x.valor<0?'−':'+'}{formatarPontos(Math.abs(x.valor))}</b></li>)}</ul>
      </>:<p className="rs-sem">{t('Nenhum ponto nesta luta: a jornada termina aqui com o que você já fez.')}</p>}
      <div className={`rs-total ${fase>=2?'subiu':''}`}>
        {fase>=2&&p.total>0&&<Fx nome="pontos" cor={cor} ms={900} className="rs-estouro"/>}
        <span className="rs-rotulo">{fimDaJornada?'PONTUAÇÃO FINAL':'TOTAL DA JORNADA'}</span>
        <strong>{fase>=2?<Contador de={antes} para={total} ms={1200}/>:formatarPontos(antes)}</strong>
        <small>{plural(vitorias,'{n} vitória','{n} vitórias')} · {t('{pontos} pontos para o ranking',{pontos:formatarPontos(total)})}</small>
      </div>
      <div className={`rs-recorde ${fase>=3&&novoRecorde?'novo':''}`}>
        {fase>=3&&novoRecorde&&<Fx nome="recorde" cor="#ffd36b" ms={1100} className="rs-estouro-recorde"/>}
        {fase>=3&&novoRecorde?<><Sparkles size={16}/><b>{t('NOVO RECORDE!')}</b>{recordeAntes>0&&<span>{t('antes: {pontos}',{pontos:formatarPontos(recordeAntes)})}</span>}</>
          :<><span>{t('Seu recorde')}</span><b>{formatarPontos(Math.max(recordeAntes,total))}</b>{recordeAntes>total&&<span>{t('faltam {pontos}',{pontos:formatarPontos(recordeAntes-total)})}</span>}</>}
      </div>
    </div>

    {descobertos.map((id,k)=><AvisoDeSegredo key={id} id={id} k={k} proxima={proxima} index={run.index} noLivro={run.livroNovo?.includes(id)===true}/>)}
    {/* o sexto segredo saiu nesta jornada: o prêmio do Livro (um pulo a mais, para sempre) */}
    {descobertos.some(id=>run.livroNovo?.includes(id))&&livroCompleto([...(loadProfile().segredosDescobertos??[]),...(run.livroNovo??[])])&&<div className="rs-segredo rs-premio-livro" role="status" style={{'--cor':'#ffd36b',animationDelay:`${.6+descobertos.length*.35}s`} as CSSProperties}>
      <span className="rs-segredo-selo"><Sparkles size={28}/></span>
      <div className="rs-segredo-texto"><small>{t('LIVRO DE SEGREDOS COMPLETO')}</small><strong>{t('+1 pulo para sempre!')}</strong><span>{t('Prêmio dos 6 segredos: a escolha do trio agora tem {n} pulos em vez de {antes}.',{n:PULOS_COM_O_LIVRO_COMPLETO,antes:PULOS_DA_JORNADA})}</span></div>
    </div>}

    {champion&&run.conquistasNovas?.length?<ConquistasLiberadas ids={run.conquistasNovas}/>:null}

    {/* as 10 lutas e, no lugar delas, a ★ (entre a 5 e a 6) e a 11: trancadas até um segredo abrir */}
    <ol className={`rs-trilha ${comSegredos?'com-extras':''}`} aria-label={t('As lutas da jornada')}>{(comSegredos?[0,1,2,3,4,LUTA_ESTRELA,5,6,7,8,9,LUTA_ONZE]:[0,1,2,3,4,5,6,7,8,9]).map(i=>{const r=resumos.find(s=>s.index===i),ex=ehLutaExtra(i);
      const liberada=i===LUTA_ESTRELA?estrelaLiberada:i===LUTA_ONZE?onzeLiberada:true;
      const marca=r?(r.won?'ganhou':'perdeu'):i===proxima?'proxima':'';
      const rotulo=r?`${rotuloDaLuta(i)}: ${r.won?'+'+formatarPontos(r.score):ex?t('sem pontos'):t('derrota')}`:ex&&!liberada?`${rotuloDaLuta(i)}: ${t('trancada, abre com um segredo')}`:rotuloDaLuta(i);
      const conteudo=i===LUTA_ESTRELA?(liberada||r?<Star size={11} fill="currentColor"/>:<Lock size={9}/>):i===LUTA_ONZE?(liberada||r?11:<Lock size={9}/>):i===9?<Crown size={12}/>:i+1;
      return <li key={i} className={`${marca} ${ex?`secreta ${liberada||r?'':'trancada'}`:''} ${i===run.index?'agora':''} ${r&&i===vista?'vendo':''}`} title={rotulo}>
        {r?<button type="button" onClick={()=>{if(i!==vista){setVista(i);battleAudio.sound('toque',PRIORIDADE.interface);}}} aria-pressed={i===vista} aria-label={`${rotulo}. ${t('Ver quem ajudou quem nesta luta')}`}>{conteudo}</button>:conteudo}</li>;})}</ol>
    {resumos.length>1&&<p className="rs-trilha-dica">{t('Toque numa luta para ver quem ajudou quem nela')}</p>}

    {(ajudas.length>0||pressao||vista!==run.index)&&<section key={vista} className="rs-ajudas" aria-label={t('Quem ajudou quem')}>
      <h2>{t('Quem ajudou quem')}{vista!==run.index&&<span className={`rs-ajudas-luta ${resumoVisto?.won?'ganhou':'perdeu'}`}>{rotuloDaLuta(vista)} · {resumoVisto?.won?`+${formatarPontos(resumoVisto.score)}`:t('derrota')}</span>}</h2>
      {vista!==run.index&&!dados&&<p className="rs-ajudas-vazio">{t('Esta luta foi jogada antes desta novidade, então o quem ajudou quem dela não ficou guardado. As próximas ficam.')}</p>}
      {dados&&ajudas.length===0&&!pressao&&<p className="rs-ajudas-vazio">{t('Nesta luta ninguém do trio ativou a mecânica de outro.')}</p>}
      <div>{ajudas.map((d,i)=>{const de=lutador(d.de),para=lutador(d.para);if(!de||!para)return null;const av=avaliarDirecao(d);return <article key={`${d.de}-${d.para}`} className={`rs-ajuda tipo-${d.tipo} ${av?`com-nota nota-${av.nota}`:''}`}>
        <div className="rs-dupla"><span style={{'--character':de.color} as CSSProperties}><Portrait character={de} className="tiny"/></span><ArrowRight size={14}/><span style={{'--character':para.color} as CSSProperties}><Portrait character={para} className="tiny"/></span></div>
        <div className="rs-ajuda-numero"><b>{d.destaque!.numero}</b><small>{t(d.destaque!.rotulo)}</small></div>
        <p><b>{nomeDe(de).split(/[ ,]/)[0]}</b> {d.frase&&t(d.frase)}</p>
        {av&&<NotaDaAjuda av={av} i={i}/>}
      </article>;})}
      {pressao&&(()=>{const quem=lutador(pressao.uid),av=avaliarAjuda('pressao',pressao.dano);return quem?<article className={`rs-ajuda tipo-pressao ${av?`com-nota nota-${av.nota}`:''}`}>
        <div className="rs-dupla"><span style={{'--character':quem.color} as CSSProperties}><Portrait character={quem} className="tiny"/></span><Shield size={16}/></div>
        <div className="rs-ajuda-numero"><b>{Math.round(pressao.parte*100)}%</b><small>{t('do dano levado')}</small></div>
        <p><b>{nomeDe(quem).split(/[ ,]/)[0]}</b> {t('segurou a pressão pelo trio · {v} de dano',{v:pressao.dano})}</p>
        {av&&<NotaDaAjuda av={av} i={ajudas.length}/>}
      </article>:null;})()}
      </div>
    </section>}

    {run.ranked&&fimDaJornada&&<div className="rs-ranqueada" role="status"><strong>{t('RANKING')}</strong>
      {run.ranked.status==='verified'?<><span>{t('Pontuação validada:')} <b>{formatarPontos(run.ranked.score??0)}</b></span><span>{t('Posição: hoje #{hoje} · semana #{semana} · geral #{geral}',{hoje:run.ranked.daily??'—',semana:run.ranked.weekly??'—',geral:run.ranked.season??'—'})}</span>{(run.ranked.top3?.temporada??run.ranked.top3?.periodo)&&<AvisoTop3 resultado={(run.ranked.top3?.temporada??run.ranked.top3?.periodo)!}/>}</>
        :run.ranked.status==='failed'?<><span>{/vers[aã]o/i.test(run.ranked.error??'')?t('Esta jornada começou numa versão antiga do jogo e não pode entrar no ranking. Atualize o jogo e jogue de novo.'):`${t('Validação pendente:')} ${t(run.ranked.error??'')}`}</span>{onRetry&&<button className="secondary" onClick={onRetry}>{t('Tentar validar de novo')}</button>}</>
        :<span>{t('Validando no servidor…')}</span>}
      {onRanking&&<button className="text-button" onClick={onRanking}>{t('Ver ranking →')}</button>}</div>}

    {proximo&&<div className={`rs-proximo ${proxima!==null&&ehLutaExtra(proxima)?'secreta':''}`}><span>{proxima===LUTA_ESTRELA?t('PRÓXIMA: SECRETA ★'):proxima===LUTA_ONZE?t('PRÓXIMA: SECRETA 11'):t('PRÓXIMA LUTA')}<b>{t(proximo.name)}</b></span><div>{proximo.team.map(id=><Portrait key={id} character={byId[id]} className="tiny"/>)}</div></div>}
    {fimDaJornada&&!run.ranked&&<div className="rs-ranqueada fora" role="status"><strong>{t('FORA DO RANKING')}</strong><span>{t('Esta jornada foi jogada sem a conta conectada (ou sem internet ao começar), então não foi para o ranking. Entre na sua conta antes de jogar para as próximas valerem.')}</span>{onRanking&&<button className="text-button" onClick={onRanking}>{t('Ver o ranking →')}</button>}</div>}

    {/* a chave fica no fim da tela, sem acompanhar a rolagem: a batalha também tem o botão AUTO à vista */}
    {segue&&<ChaveDoAuto ligado={auto} onChange={onAuto}/>}
    <footer className="rs-acoes">
      {segue?<button className={`rs-cta ${proxima!==null&&ehLutaExtra(proxima)?'rs-cta-secreta':''}`} onClick={onNext}><Fx nome="brilho" cor="#ffffff" ms={2600} laco className="rs-brilho"/>{contando&&<i key={contando.desde} className="rs-contagem" style={{'--espera':`${ESPERA_DA_PROXIMA_MS}ms`} as CSSProperties}/>}<span>{proxima===LUTA_ESTRELA?t('Luta secreta ★'):proxima===LUTA_ONZE?t('Luta 11 secreta'):t('Próxima luta')}</span>{contando?<b className="rs-segundos">{contando.faltam}</b>:<ArrowRight size={20}/>}</button>
        :<button className="rs-cta" onClick={onRestart}><Fx nome="brilho" cor="#ffffff" ms={2600} laco className="rs-brilho"/><span>{t('Jogar de novo')}</span><RotateCcw size={19}/></button>}
      <button className="secondary rs-icone-botao" onClick={onHome} aria-label={t('Início')} title={t('Início')}><Home size={19}/></button>
      {segue&&<button className="secondary rs-icone-botao rs-desistir" onClick={onAbandon} aria-label={t('Desistir da jornada')} title={t('Desistir da jornada')}><LogOut size={18}/></button>}
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
  return <div className={`top3-aviso${m.destaque?' destaque':''}`}><b>{t(m.titulo)}</b>{m.linhas.map(l=><span key={l}>{t(l)}</span>)}</div>;
}

/*
 * O aviso de segredo descoberto (src/engine/segredos.ts): o selo do segredo girando para dentro, o nome, e o que ele
 * libera — "a luta secreta ★ é a próxima!" ou "vença até a luta 5 e ela aparece".
 */
function AvisoDeSegredo({id,k,proxima,index,noLivro}:{id:SegredoId;k:number;proxima:number|null;index:number;noLivro:boolean}){
  const s=SEGREDO[id],Ic=ICONE_DO_SEGREDO[id];
  const frases=s.libera.map(q=>q==='estrela'
    ?(proxima===LUTA_ESTRELA?t('A luta secreta ★ é a próxima!'):index<4?t('Vença até a luta 5 e a luta secreta ★ aparece.'):null)
    :(proxima===LUTA_ONZE?t('A luta 11 é a próxima!'):index<9||index===LUTA_ESTRELA?t('Vença as 10 lutas e a luta 11 te espera.'):null)).filter(Boolean);
  return <div className="rs-segredo" role="status" style={{'--cor':s.cor,animationDelay:`${.6+k*.35}s`} as CSSProperties}>
    <span className="rs-segredo-selo" style={{animationDelay:`${.9+k*.35}s`}}><Ic size={28}/></span>
    <div className="rs-segredo-texto">
      <small>{t('SEGREDO DESCOBERTO')}</small>
      <strong>{t(s.nome)}!</strong>
      {frases.map((f,i)=><span key={i}>{f}</span>)}
      {noLivro&&<em className="rs-segredo-livro">{t('NOVO NO LIVRO DE SEGREDOS')}</em>}
    </div>
  </div>;
}
