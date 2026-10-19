import {useMemo,useState,type CSSProperties} from 'react';
import {createPortal} from 'react-dom';
import {Award,Lock,Minus,Play,Search,StarOff,X} from 'lucide-react';
import {byId} from '../data/characters';
import type {Character} from '../engine/types';
import {CUSTO_DA_COLECAO,formatarPontos} from '../engine/pontos';
import {Portrait} from './Portrait';
import type {Conquistas} from '../lib/conquistas';

/*
 * A Jornada com os seus (pedido do jogador: "um botão lá nos seus personagens… fazer uma jornada com os personagens que
 * você tem"): o trio sai só dos personagens já liberados nas Conquistas (emprestado não vale), joga a Jornada normal e
 * cada luta custa CUSTO_DA_COLECAO (30 mil); o bônus das estrelas de pontos não vale e nada é liberado.
 *
 * Na tela das Conquistas fica a faixa dourada; tocando nela, abre a escolha: só os seus, com busca, e o trio embaixo.
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
        <span className="cq-meus-rotulo"><Award size={15}/>JORNADA COM OS SEUS</span>
        <span className="cq-meus-conta">{meus.length} {meus.length===1?'seu':'seus'}</span>
      </div>
      <div className="cq-meus-corpo">
        <span className="cq-meus-leque" aria-hidden="true">{[0,1,2].map(i=>{const c=meus[i];return <span key={i} style={{'--character':c?.color??'#3a3320','--i':i} as CSSProperties}>{c?<Portrait character={c}/>:<Lock size={16}/>}</span>;})}</span>
        <p>Monte o trio só com <b>os personagens que você já liberou</b> e jogue a Jornada inteira com eles.</p>
      </div>
      <div className="cq-meus-regras">
        <span><Minus size={12}/>{custo} por luta</span>
        <span><StarOff size={12}/>sem bônus de estrela</span>
        <span><Lock size={12}/>não libera conquistas</span>
      </div>
      <button className="primary cq-meus-botao" disabled={!!faltam} onClick={()=>setAberta(true)}>
        {faltam?<><Lock size={16}/>Libere mais {faltam} para usar</>:<><Play size={17} fill="currentColor"/>ESCOLHER MEU TRIO</>}
      </button>
    </div>
    {aberta&&<Escolha meus={meus} custo={custo} onFechar={()=>setAberta(false)} onJogar={trio=>{setAberta(false);onJogar(trio);}}/>}
  </>;
}

function Escolha({meus,custo,onFechar,onJogar}:{meus:Character[];custo:string;onFechar:()=>void;onJogar:(trio:string[])=>void}){
  const [trio,setTrio]=useState<string[]>([]);
  const [busca,setBusca]=useState('');
  const lista=useMemo(()=>{const q=sem(busca.trim());return [...meus].sort((a,b)=>a.name.localeCompare(b.name,'pt-BR')).filter(c=>!q||sem(c.name).includes(q));},[meus,busca]);
  const troca=(id:string)=>setTrio(t=>t.includes(id)?t.filter(x=>x!==id):t.length<3?[...t,id]:t);
  const pronto=trio.length===3;
  return createPortal(<div className="cq-meus-veu" role="dialog" aria-label="Jornada com os seus: escolha o trio" onClick={e=>{if(e.target===e.currentTarget)onFechar();}}>
    <div className="cq-meus-folha">
      <header>
        <span className="cq-meus-rotulo"><Award size={15}/>MONTE SEU TRIO</span>
        <button className="cq-fechar" onClick={onFechar} aria-label="Fechar"><X size={18}/></button>
        <small>Só os seus liberados · {meus.length} na coleção</small>
        {meus.length>12&&<label className="cq-meus-busca"><Search size={15}/><input value={busca} onChange={e=>setBusca(e.target.value)} placeholder="Buscar nos seus" aria-label="Buscar nos seus personagens"/></label>}
      </header>
      <div className="cq-meus-grade">
        {lista.map((c,i)=>{const n=trio.indexOf(c.id),cheio=n<0&&trio.length===3;
          return <button key={c.id} className={`cq-carta liberada ${n>=0?'no-trio':''} ${cheio?'apagada':''}`} style={{'--character':c.color,'--i':Math.min(i,40)} as CSSProperties} onClick={()=>troca(c.id)} aria-pressed={n>=0} aria-label={n>=0?`${c.name}: no trio (toque para tirar)`:`Pôr ${c.name} no trio`}>
            <span className="cq-retrato"><Portrait character={c}/>{n>=0&&<em className="cq-meus-numero">{n+1}</em>}</span>
            <small>{c.name}</small>
          </button>;})}
        {!lista.length&&<p className="cq-meus-nada">Nenhum dos seus com esse nome.</p>}
      </div>
      <footer>
        <div className="cq-meus-trio">{[0,1,2].map(i=>{const c=trio[i]?byId[trio[i]!]:undefined;return c
          ?<button key={c.id} className="cheio" style={{'--character':c.color} as CSSProperties} onClick={()=>troca(c.id)} aria-label={`Tirar ${c.name} do trio`}><Portrait character={c}/><b>{c.name}</b></button>
          :<span key={`v${i}`} className={i===trio.length?'vez':''}><i>?</i><b>{i===trio.length?'escolha':`espaço ${i+1}`}</b></span>;})}</div>
        <p className="cq-meus-lembrete"><b>−{custo}</b> por luta · sem bônus de estrela · não libera conquistas</p>
        <button className="primary cq-meus-jogar" disabled={!pronto} onClick={()=>onJogar(trio)}>
          {pronto?<><Play size={18} fill="currentColor"/>JOGAR COM OS MEUS</>:<>Escolha {3-trio.length} {3-trio.length===1?'personagem':'personagens'}</>}
        </button>
      </footer>
    </div>
  </div>,document.body);
}
