import {useEffect,useState,type CSSProperties} from 'react';
import {Award,ChevronRight,Clock3,Lock,Play,Trophy,X,Zap} from 'lucide-react';
import {byId} from '../data/characters';
import type {Character} from '../engine/types';
import {Portrait} from '../components/Portrait';
import {TelaTopo} from '../components/Casca';
import {PERSONAGENS_DA_ABA,PULOS_DO_DESAFIO,TOTAL_DE_CONQUISTAS,ateMeiaNoite,desafioDoDia,juntar,tituloDe} from '../lib/conquistas';
import {Album} from '../components/Album';
import {JornadaComOsSeus} from '../components/JornadaComOsSeus';
import {onlineCall,onlineConfigured,type RankingDeConquistas} from '../lib/online';
import type {Profile} from '../lib/storage';
import { universoDaFicha } from '../data/equipes';
import {LOCALE,nomeDe,t} from '../i18n/idioma';

/*
 * As Conquistas (pedido do jogador): todos os personagens, um por conquista.
 *
 * Sem lista infinita: o álbum (components/Album.tsx), com as quatro abas e as
 * páginas que passam de lado. O bloqueado fica cinza com cadeado; o liberado fica
 * colorido, com o anel dourado e o brilho passando, e o recém-liberado ganha
 * o selo NOVO até a tela ser vista.
 *
 * No topo, o anel com quantos já foram liberados, o título do colecionador e
 * quanto falta para o próximo; com conta, a posição no ranking de conquistas.
 * Embaixo, a Jornada com os seus (o trio dos já liberados) e três sugestões do dia de quem ainda falta.
 */
const data=(iso:string)=>new Date(iso).toLocaleDateString(LOCALE);

export function ConquistasScreen({profile,conta,onProfile,onRanking,onDesafio,onComOsMeus}:{profile:Profile;conta:boolean;/** recebe uma atualização (do perfil mais novo), para duas mudanças seguidas não se apagarem */onProfile:(muda:(p:Profile)=>Profile)=>void;onRanking:()=>void;onDesafio:(id:string)=>void;/** a Jornada com os seus: o trio escolhido entre os liberados */onComOsMeus:(trio:string[])=>void}){
  const conquistas=profile.conquistas??{};
  const [noRanking,setNoRanking]=useState<{total:number;posicao:number|null}|null>(null);
  /* As do servidor entram no aparelho; e a posição no ranking de conquistas. */
  useEffect(()=>{if(!onlineConfigured||!conta)return;let ativo=true;
    /* manda as do aparelho junto: as que o servidor ainda não tinha entram no ranking na hora; só depois pede a posição */
    void onlineCall<{conquistas:{id:string;data:string}[]}>('conquistas-sync',{ids:Object.keys(profile.conquistas??{})}).then(r=>{if(!ativo)return;onProfile(p=>{const juntas=juntar(p.conquistas??{},r.conquistas);return Object.keys(juntas).length!==Object.keys(p.conquistas??{}).length||Object.entries(juntas).some(([k,v])=>p.conquistas?.[k]!==v)?{...p,conquistas:juntas}:p;});setNoRanking(n=>({total:r.conquistas.length,posicao:n?.posicao??null}));}).catch(()=>{})
      .finally(()=>{if(ativo)void onlineCall<RankingDeConquistas>('leaderboard',{mode:'conquistas'}).then(r=>{if(ativo&&r.mine)setNoRanking(n=>({total:r.mine!.total,posicao:r.mine!.position??n?.posicao??null}));}).catch(()=>{});});
    return()=>{ativo=false};
  },[conta]);
  /* O que estava NOVO fica visto depois de a tela ficar aberta um pouco (o selo aparece na primeira vez). */
  const [vistasAoAbrir]=useState(()=>new Set(profile.conquistasVistas??[]));
  useEffect(()=>{const id=window.setTimeout(()=>{const todas=Object.keys(profile.conquistas??{});if(todas.some(k=>!vistasAoAbrir.has(k)))onProfile(p=>({...p,conquistasVistas:Object.keys(p.conquistas??{})}));},1500);return()=>window.clearTimeout(id);
  },[profile.conquistas]);

  const liberadas=Object.keys(conquistas).length,titulo=tituloDe(liberadas);
  const [aberto,setAberto]=useState<Character|null>(null);
  /* O Desafio do Dia: os três de hoje ficam guardados; quem foi liberado sai; feitos os três, outros chegam à meia-noite. */
  const desafio=desafioDoDia(profile.desafio,conquistas),faltam=desafio.ids.filter(id=>!conquistas[id]).map(id=>byId[id]).filter((c):c is Character=>!!c);
  useEffect(()=>{if(profile.desafio?.dia!==desafio.dia||profile.desafio.ids.join()!==desafio.ids.join())onProfile(p=>({...p,desafio}));},[desafio.dia,desafio.ids.join()]);
  const [,setRelogio]=useState(0);
  useEffect(()=>{const id=window.setInterval(()=>setRelogio(n=>n+1),30000);return()=>window.clearInterval(id);},[]);
  const noDesafio=(id:string)=>desafio.ids.includes(id)&&!conquistas[id];
  const R=44,C=2*Math.PI*R,fracao=liberadas/TOTAL_DE_CONQUISTAS;

  return <section className="conquistas-tela">
    <TelaTopo icone={<Award/>} cor="#ffd36b" rotulo={t('CONQUISTAS')} titulo={t('Libere os {n}',{n:TOTAL_DE_CONQUISTAS})}><p>{t('Termine as 10 lutas com um personagem no trio para liberar a conquista dele.')}</p></TelaTopo>

    <div className="cq-heroi" style={{'--titulo':titulo.atual.cor} as CSSProperties}>
      <div className="cq-anel" aria-label={t('{n} de {total} liberados',{n:liberadas,total:TOTAL_DE_CONQUISTAS})}>
        <svg viewBox="0 0 100 100"><circle className="cq-anel-fundo" cx="50" cy="50" r={R}/><circle className="cq-anel-cheio" cx="50" cy="50" r={R} style={{strokeDasharray:`${C*fracao} ${C}`}}/></svg>
        <span><b>{liberadas}</b><small>{t('de')} {TOTAL_DE_CONQUISTAS}</small><em>{Math.floor(fracao*100)}%</em></span>
      </div>
      <div className="cq-titulo">
        <span className="cq-nivel">{t('NÍVEL {n}',{n:titulo.nivel})}</span>
        <strong>{t(titulo.atual.nome)}</strong>
        {titulo.proximo?<><div className="cq-barra"><i style={{width:`${Math.round(titulo.progresso*100)}%`}}/></div>
          <small>{t('Faltam {n} para',{n:titulo.proximo.minimo-liberadas})} <b style={{color:titulo.proximo.cor}}>{t(titulo.proximo.nome)}</b></small></>
          :<small>{t('Você liberou todos os personagens!')}</small>}
        {conta&&onlineConfigured&&<button className="cq-no-ranking" onClick={onRanking}><Trophy size={14}/>{noRanking?.posicao?<><b>#{noRanking.posicao}</b> {t('no ranking · {n} valendo',{n:noRanking.total})}</>:<>{t('Ranking de conquistas')}</>}<ChevronRight size={14}/></button>}
      </div>
    </div>

    <JornadaComOsSeus conquistas={conquistas} onJogar={onComOsMeus}/>

    <div className={`cq-desafio ${faltam.length?'':'completo'}`}>
      <div className="cq-desafio-topo">
        <span className="cq-desafio-rotulo"><Zap size={15}/>{t('DESAFIO DO DIA')}</span>
        <span className="cq-desafio-pips" aria-label={t('{n} de {total} feitos hoje',{n:desafio.ids.length-faltam.length,total:desafio.ids.length})}>{desafio.ids.map(id=><i key={id} className={conquistas[id]?'feito':''}/>)}</span>
      </div>
      {faltam.length?<>
        <div className="cq-desafio-trio">{faltam.map((c,i)=><button key={c.id} onClick={()=>setAberto(c)} style={{'--character':c.color,'--i':i} as CSSProperties} aria-label={t('Desafio: jogar com {nome}',{nome:nomeDe(c)})}>
          <span className="cq-desafio-retrato"><Portrait character={c}/></span><b>{nomeDe(c)}</b><em><Play size={10} fill="currentColor"/>{t('JOGAR')}</em></button>)}</div>
        <p>{t('Toque num deles: a Jornada já começa com ele no trio e {n} trocas de opções (em vez de 3). Termine as 10 lutas para liberar.',{n:PULOS_DO_DESAFIO})}</p>
        <small className="cq-desafio-relogio"><Clock3 size={12}/>{t('Novos desafios em {tempo}',{tempo:ateMeiaNoite()})}</small>
      </>:<div className="cq-desafio-fim"><Trophy size={30}/><b>{t('Desafio de hoje completo!')}</b><small><Clock3 size={12}/>{t('Novos desafios em {tempo}',{tempo:ateMeiaNoite()})}</small></div>}
    </div>

    <Album listas={PERSONAGENS_DA_ABA} rotulo={a=>`${PERSONAGENS_DA_ABA[a].filter(c=>conquistas[c.id]).length}/${PERSONAGENS_DA_ABA[a].length}`}
      barra={a=>PERSONAGENS_DA_ABA[a].filter(c=>conquistas[c.id]).length/PERSONAGENS_DA_ABA[a].length}
      carta={(c,i)=>{const quando=conquistas[c.id],novo=!!quando&&!vistasAoAbrir.has(c.id);
        return <button key={c.id} className={`cq-carta ${quando?'liberada':'bloqueada'} ${novo?'novo':''}`} style={{'--character':c.color,'--i':i} as CSSProperties} onClick={()=>setAberto(c)} aria-label={`${nomeDe(c)}: ${quando?t('liberado em {data}',{data:data(quando)}):t('bloqueado')}`}>
          <span className="cq-retrato"><Portrait character={c}/>{!quando&&<Lock className="cq-cadeado" size={14}/>}</span>
          <small>{nomeDe(c)}</small>
          {novo&&<em className="cq-novo">{t('NOVO')}</em>}
        </button>;}}/>

    {aberto&&<div className="cq-veu" role="dialog" aria-label={nomeDe(aberto)} onClick={e=>{if(e.target===e.currentTarget)setAberto(null);}}>
      <div className={`cq-ficha ${conquistas[aberto.id]?'liberada':'bloqueada'}`} style={{'--character':aberto.color} as CSSProperties}>
        <button className="cq-fechar" onClick={()=>setAberto(null)} aria-label={t('Fechar')}><X size={18}/></button>
        <span className="cq-ficha-retrato"><Portrait character={aberto}/>{!conquistas[aberto.id]&&<Lock size={26}/>}</span>
        <small className="cq-ficha-universo">{t(universoDaFicha(aberto))}</small>
        <h2>{nomeDe(aberto)}</h2>
        {conquistas[aberto.id]
          ?<p className="cq-ficha-ok"><Award size={16}/>{t('Conquista liberada em {data}',{data:data(conquistas[aberto.id]!)})}</p>
          :<p className="cq-ficha-falta">{t('Termine as 10 lutas de uma Jornada com {nome} no trio para liberar.',{nome:nomeDe(aberto)})}</p>}
        {noDesafio(aberto.id)&&<button className="primary cq-ficha-jogar" onClick={()=>{setAberto(null);onDesafio(aberto.id);}}><Play size={18} fill="currentColor"/>{t('Jogar com {nome}',{nome:nomeDe(aberto)})}<small>{t('já no trio · {n} trocas',{n:PULOS_DO_DESAFIO})}</small></button>}
      </div>
    </div>}
  </section>;
}

/* Os personagens que esta jornada liberou: a tela de resultado mostra. */
export function ConquistasLiberadas({ids}:{ids:string[]}){
  const lista=ids.map(id=>byId[id]).filter((c):c is Character=>!!c);
  if(!lista.length)return null;
  return <div className="cq-liberadas" role="status">
    <span className="cq-liberadas-rotulo"><Award size={15}/>{lista.length===1?t('CONQUISTA LIBERADA'):t('{n} CONQUISTAS LIBERADAS',{n:lista.length})}</span>
    <div>{lista.map((c,i)=><span key={c.id} className="cq-liberada" style={{'--character':c.color,'--i':i} as CSSProperties}><Portrait character={c}/><small>{nomeDe(c)}</small></span>)}</div>
  </div>;
}

