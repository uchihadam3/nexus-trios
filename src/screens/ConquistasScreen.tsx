import {useEffect,useState,type CSSProperties} from 'react';
import {Award,ChevronRight,Clock3,Lock,Play,Trophy,X,Zap} from 'lucide-react';
import {byId} from '../data/characters';
import type {Character} from '../engine/types';
import {Portrait} from '../components/Portrait';
import {TelaTopo} from '../components/Casca';
import {PERSONAGENS_DA_ABA,PULOS_DO_DESAFIO,TOTAL_DE_CONQUISTAS,ateMeiaNoite,desafioDoDia,juntar,tituloDe} from '../lib/conquistas';
import {Album} from '../components/Album';
import {onlineCall,onlineConfigured,type RankingDeConquistas} from '../lib/online';
import type {Profile} from '../lib/storage';

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
 * Embaixo, três sugestões do dia de quem ainda falta.
 */
const data=(iso:string)=>new Date(iso).toLocaleDateString('pt-BR');

export function ConquistasScreen({profile,conta,onProfile,onRanking,onDesafio}:{profile:Profile;conta:boolean;/** recebe uma atualização (do perfil mais novo), para duas mudanças seguidas não se apagarem */onProfile:(muda:(p:Profile)=>Profile)=>void;onRanking:()=>void;onDesafio:(id:string)=>void}){
  const conquistas=profile.conquistas??{};
  const [noRanking,setNoRanking]=useState<{total:number;posicao:number|null}|null>(null);
  /* As do servidor entram no aparelho; e a posição no ranking de conquistas. */
  useEffect(()=>{if(!onlineConfigured||!conta)return;let ativo=true;
    void onlineCall<{conquistas:{id:string;data:string}[]}>('conquistas').then(r=>{if(!ativo)return;onProfile(p=>{const juntas=juntar(p.conquistas??{},r.conquistas);return Object.keys(juntas).length!==Object.keys(p.conquistas??{}).length||Object.entries(juntas).some(([k,v])=>p.conquistas?.[k]!==v)?{...p,conquistas:juntas}:p;});setNoRanking(n=>({total:r.conquistas.length,posicao:n?.posicao??null}));}).catch(()=>{});
    void onlineCall<RankingDeConquistas>('leaderboard',{mode:'conquistas'}).then(r=>{if(ativo&&r.mine)setNoRanking(n=>({total:r.mine!.total,posicao:r.mine!.position??n?.posicao??null}));}).catch(()=>{});
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
    <TelaTopo icone={<Award/>} cor="#ffd36b" rotulo="CONQUISTAS" titulo={`Libere os ${TOTAL_DE_CONQUISTAS}`}><p>Termine as 10 lutas com um personagem no trio para liberar a conquista dele.</p></TelaTopo>

    <div className="cq-heroi" style={{'--titulo':titulo.atual.cor} as CSSProperties}>
      <div className="cq-anel" aria-label={`${liberadas} de ${TOTAL_DE_CONQUISTAS} liberados`}>
        <svg viewBox="0 0 100 100"><circle className="cq-anel-fundo" cx="50" cy="50" r={R}/><circle className="cq-anel-cheio" cx="50" cy="50" r={R} style={{strokeDasharray:`${C*fracao} ${C}`}}/></svg>
        <span><b>{liberadas}</b><small>de {TOTAL_DE_CONQUISTAS}</small><em>{Math.floor(fracao*100)}%</em></span>
      </div>
      <div className="cq-titulo">
        <span className="cq-nivel">NÍVEL {titulo.nivel}</span>
        <strong>{titulo.atual.nome}</strong>
        {titulo.proximo?<><div className="cq-barra"><i style={{width:`${Math.round(titulo.progresso*100)}%`}}/></div>
          <small>Faltam <b>{titulo.proximo.minimo-liberadas}</b> para <b style={{color:titulo.proximo.cor}}>{titulo.proximo.nome}</b></small></>
          :<small>Você liberou todos os personagens!</small>}
        {conta&&onlineConfigured&&<button className="cq-no-ranking" onClick={onRanking}><Trophy size={14}/>{noRanking?.posicao?<><b>#{noRanking.posicao}</b> no ranking · {noRanking.total} valendo</>:<>Ranking de conquistas</>}<ChevronRight size={14}/></button>}
      </div>
    </div>

    <div className={`cq-desafio ${faltam.length?'':'completo'}`}>
      <div className="cq-desafio-topo">
        <span className="cq-desafio-rotulo"><Zap size={15}/>DESAFIO DO DIA</span>
        <span className="cq-desafio-pips" aria-label={`${desafio.ids.length-faltam.length} de ${desafio.ids.length} feitos hoje`}>{desafio.ids.map(id=><i key={id} className={conquistas[id]?'feito':''}/>)}</span>
      </div>
      {faltam.length?<>
        <div className="cq-desafio-trio">{faltam.map((c,i)=><button key={c.id} onClick={()=>setAberto(c)} style={{'--character':c.color,'--i':i} as CSSProperties} aria-label={`Desafio: jogar com ${c.name}`}>
          <span className="cq-desafio-retrato"><Portrait character={c}/></span><b>{c.name}</b><em><Play size={10} fill="currentColor"/>JOGAR</em></button>)}</div>
        <p>Toque num deles: a Jornada já começa com ele no trio e <b>{PULOS_DO_DESAFIO} trocas</b> de opções (em vez de 3). Termine as 10 lutas para liberar.</p>
        <small className="cq-desafio-relogio"><Clock3 size={12}/>Novos desafios em {ateMeiaNoite()}</small>
      </>:<div className="cq-desafio-fim"><Trophy size={30}/><b>Desafio de hoje completo!</b><small><Clock3 size={12}/>Novos desafios em {ateMeiaNoite()}</small></div>}
    </div>

    <Album listas={PERSONAGENS_DA_ABA} rotulo={a=>`${PERSONAGENS_DA_ABA[a].filter(c=>conquistas[c.id]).length}/${PERSONAGENS_DA_ABA[a].length}`}
      barra={a=>PERSONAGENS_DA_ABA[a].filter(c=>conquistas[c.id]).length/PERSONAGENS_DA_ABA[a].length}
      carta={(c,i)=>{const quando=conquistas[c.id],novo=!!quando&&!vistasAoAbrir.has(c.id);
        return <button key={c.id} className={`cq-carta ${quando?'liberada':'bloqueada'} ${novo?'novo':''}`} style={{'--character':c.color,'--i':i} as CSSProperties} onClick={()=>setAberto(c)} aria-label={`${c.name}: ${quando?`liberado em ${data(quando)}`:'bloqueado'}`}>
          <span className="cq-retrato"><Portrait character={c}/>{!quando&&<Lock className="cq-cadeado" size={14}/>}</span>
          <small>{c.name}</small>
          {novo&&<em className="cq-novo">NOVO</em>}
        </button>;}}/>

    {aberto&&<div className="cq-veu" role="dialog" aria-label={aberto.name} onClick={e=>{if(e.target===e.currentTarget)setAberto(null);}}>
      <div className={`cq-ficha ${conquistas[aberto.id]?'liberada':'bloqueada'}`} style={{'--character':aberto.color} as CSSProperties}>
        <button className="cq-fechar" onClick={()=>setAberto(null)} aria-label="Fechar"><X size={18}/></button>
        <span className="cq-ficha-retrato"><Portrait character={aberto}/>{!conquistas[aberto.id]&&<Lock size={26}/>}</span>
        <small className="cq-ficha-universo">{aberto.universe}</small>
        <h2>{aberto.name}</h2>
        {conquistas[aberto.id]
          ?<p className="cq-ficha-ok"><Award size={16}/>Conquista liberada em <b>{data(conquistas[aberto.id]!)}</b></p>
          :<p className="cq-ficha-falta">Termine as <b>10 lutas</b> de uma Jornada com {aberto.name} no trio para liberar.</p>}
        {noDesafio(aberto.id)&&<button className="primary cq-ficha-jogar" onClick={()=>{setAberto(null);onDesafio(aberto.id);}}><Play size={18} fill="currentColor"/>Jogar com {aberto.name}<small>já no trio · {PULOS_DO_DESAFIO} trocas</small></button>}
      </div>
    </div>}
  </section>;
}

/* Os personagens que esta jornada liberou: a tela de resultado mostra. */
export function ConquistasLiberadas({ids}:{ids:string[]}){
  const lista=ids.map(id=>byId[id]).filter((c):c is Character=>!!c);
  if(!lista.length)return null;
  return <div className="cq-liberadas" role="status">
    <span className="cq-liberadas-rotulo"><Award size={15}/>{lista.length===1?'CONQUISTA LIBERADA':`${lista.length} CONQUISTAS LIBERADAS`}</span>
    <div>{lista.map((c,i)=><span key={c.id} className="cq-liberada" style={{'--character':c.color,'--i':i} as CSSProperties}><Portrait character={c}/><small>{c.name}</small></span>)}</div>
  </div>;
}

