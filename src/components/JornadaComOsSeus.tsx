import {useEffect,useMemo,useState,type CSSProperties} from 'react';
import {createPortal} from 'react-dom';
import {Award,Lock,Minus,Play,Search,StarOff,X} from 'lucide-react';
import {byId} from '../data/characters';
import type {Character} from '../engine/types';
import {CUSTO_DA_COLECAO,formatarPontos} from '../engine/pontos';
import {Portrait} from './Portrait';
import {ABAS,PERSONAGENS_DA_ABA,abaDo,type Aba,type Conquistas} from '../lib/conquistas';
import {Album} from './Album';
import {nomeDe,t} from '../i18n/idioma';

/*
 * A Jornada com os seus (pedido do jogador: "um botão lá nos seus personagens… fazer uma jornada com os personagens que
 * você tem"): o trio sai só dos personagens já liberados nas Conquistas (emprestado não vale), joga a Jornada normal e
 * cada luta custa CUSTO_DA_COLECAO (20 mil); o bônus das estrelas de pontos não vale e nada é liberado (nem Conquistas,
 * nem segredos: as lutas extras dos segredos não aparecem e nada abre no Livro).
 *
 * Na tela das Conquistas fica a faixa dourada; tocando nela, abre a escolha: só os seus, nas abas do álbum (Anime, Heróis…),
 * com busca, e o trio embaixo.
 */
const sem=(s:string)=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();

export function JornadaComOsSeus({conquistas,onJogar}:{conquistas:Conquistas;onJogar:(trio:string[])=>void}){
  /* os seus, do último liberado para o primeiro (o leque da faixa mostra os mais novos) */
  const meus=useMemo(()=>Object.entries(conquistas).sort((a,b)=>b[1].localeCompare(a[1])).map(([id])=>byId[id]).filter((c):c is Character=>!!c),[conquistas]);
  const [aberta,setAberta]=useState(false);
  const faltam=Math.max(0,3-meus.length),custo=formatarPontos(CUSTO_DA_COLECAO);
  return <>
    <div className={`cq-meus ${faltam?'trancada':''}`}>
      <div className="cq-meus-topo">
        <span className="cq-meus-rotulo"><Award size={15}/>{t('JORNADA COM OS SEUS')}</span>
        <span className="cq-meus-conta">{t(meus.length===1?'{n} seu':'{n} seus',{n:meus.length})}</span>
      </div>
      <div className="cq-meus-corpo">
        <span className="cq-meus-leque" aria-hidden="true">{[0,1,2].map(i=>{const c=meus[i];return <span key={i} style={{'--character':c?.color??'#3a3320','--i':i} as CSSProperties}>{c?<Portrait character={c}/>:<Lock size={16}/>}</span>;})}</span>
        <p>{t('Monte o trio só com os personagens que você já liberou e jogue a Jornada inteira com eles.')}</p>
      </div>
      <div className="cq-meus-regras">
        <span><Minus size={12}/>{custo} {t('por luta')}</span>
        <span><StarOff size={12}/>{t('sem bônus de estrela')}</span>
        <span><Lock size={12}/>{t('não libera conquistas nem segredos')}</span>
      </div>
      <button className="primary cq-meus-botao" disabled={!!faltam} onClick={()=>setAberta(true)}>
        {faltam?<><Lock size={16}/>{t('Libere mais {n} para usar',{n:faltam})}</>:<><Play size={17} fill="currentColor"/>{t('ESCOLHER MEU TRIO')}</>}
      </button>
    </div>
    {aberta&&<Escolha meus={meus} custo={custo} onFechar={()=>setAberta(false)} onJogar={trio=>{setAberta(false);onJogar(trio);}}/>}
  </>;
}

function Escolha({meus,custo,onFechar,onJogar}:{meus:Character[];custo:string;onFechar:()=>void;onJogar:(trio:string[])=>void}){
  const [trio,setTrio]=useState<string[]>([]);
  const [busca,setBusca]=useState('');
  const [aba,setAba]=useState<Aba>(()=>ABAS.find(x=>meus.some(c=>abaDo(c)===x.id))?.id??'anime');
  // separados pelas abas das Conquistas (pedido do dono: "ficar separadinho igual"), na mesma ordem do álbum
  const listas=useMemo(()=>{
    const q=sem(busca.trim()),seus=new Set(meus.map(c=>c.id));
    return Object.fromEntries(ABAS.map(x=>[x.id,PERSONAGENS_DA_ABA[x.id].filter(c=>seus.has(c.id)&&(!q||sem(`${c.name} ${nomeDe(c)}`).includes(q)))])) as Record<Aba,Character[]>;
  },[meus,busca]);
  // buscando, vai para a aba que tem o nome
  useEffect(()=>{if(busca.trim()&&!listas[aba].length){const outra=ABAS.find(x=>listas[x.id].length);if(outra)setAba(outra.id);}},[busca,listas,aba]);
  const troca=(id:string)=>setTrio(t=>t.includes(id)?t.filter(x=>x!==id):t.length<3?[...t,id]:t);
  const pronto=trio.length===3;
  return createPortal(<div className="cq-meus-veu" role="dialog" aria-label={t('Jornada com os seus: escolha o trio')} onClick={e=>{if(e.target===e.currentTarget)onFechar();}}>
    <div className="cq-meus-folha">
      <header>
        <span className="cq-meus-rotulo"><Award size={15}/>{t('MONTE SEU TRIO')}</span>
        <button className="cq-fechar" onClick={onFechar} aria-label={t('Fechar')}><X size={18}/></button>
        <small>{t('Só os seus liberados · {n} na coleção',{n:meus.length})}</small>
        {meus.length>12&&<label className="cq-meus-busca"><Search size={15}/><input value={busca} onChange={e=>setBusca(e.target.value)} placeholder={t('Buscar nos seus')} aria-label={t('Buscar nos seus personagens')}/></label>}
      </header>
      <div className="cq-meus-grade">
        <Album listas={listas} aba={aba} onAba={setAba} rotulo={x=>`${listas[x].length}`}
          vazio={<p className="cq-meus-nada">{busca.trim()?t('Nenhum dos seus com esse nome.'):t('Nenhum liberado aqui ainda.')}</p>}
          carta={(c,i)=>{const n=trio.indexOf(c.id),cheio=n<0&&trio.length===3;
            return <button key={c.id} className={`cq-carta liberada ${n>=0?'no-trio':''} ${cheio?'apagada':''}`} style={{'--character':c.color,'--i':Math.min(i,40)} as CSSProperties} onClick={()=>troca(c.id)} aria-pressed={n>=0} aria-label={n>=0?t('{nome}: no trio (toque para tirar)',{nome:nomeDe(c)}):t('Pôr {nome} no trio',{nome:nomeDe(c)})}>
              <span className="cq-retrato"><Portrait character={c}/>{n>=0&&<em className="cq-meus-numero">{n+1}</em>}</span>
              <small>{nomeDe(c)}</small>
            </button>;}}/>
      </div>
      <footer>
        <div className="cq-meus-trio">{[0,1,2].map(i=>{const c=trio[i]?byId[trio[i]!]:undefined;return c
          ?<button key={c.id} className="cheio" style={{'--character':c.color} as CSSProperties} onClick={()=>troca(c.id)} aria-label={t('Tirar {nome} do trio',{nome:nomeDe(c)})}><Portrait character={c}/><b>{nomeDe(c)}</b></button>
          :<span key={`v${i}`} className={i===trio.length?'vez':''}><i>?</i><b>{i===trio.length?t('escolha'):t('espaço {n}',{n:i+1})}</b></span>;})}</div>
        <p className="cq-meus-lembrete"><b>−{custo}</b> {t('por luta')} · {t('sem bônus de estrela')} · {t('não libera conquistas nem segredos')}</p>
        <button className="primary cq-meus-jogar" disabled={!pronto} onClick={()=>onJogar(trio)}>
          {pronto?<><Play size={18} fill="currentColor"/>{t('JOGAR COM OS MEUS')}</>:<>{t(3-trio.length===1?'Escolha {n} personagem':'Escolha {n} personagens',{n:3-trio.length})}</>}
        </button>
      </footer>
    </div>
  </div>,document.body);
}
