import { Fragment,useEffect,useRef,useState,type CSSProperties,type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import { statuses } from '../data/statuses';
import { acharTermos,type Termo } from '../presentation/glossario';

/*
 * Termos tocáveis: o nome de um Status ou de uma mecânica (Escudo, Carga,
 * Preparo, energia…) aparece sublinhado de leve; tocar abre um cartão curto
 * com o que ele faz. Assim a ficha mostra só o termo e o número, sem a frase
 * de explicação na frente de cada efeito.
 */
function CartaoDoTermo({termo,onClose}:{termo:Termo;onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null);
  useEffect(()=>{const d=ref.current;d?.showModal();return()=>d?.close();},[]);
  const ehStatus=termo.id in statuses;
  return <dialog ref={ref} className="id-card-dialog termo-dialog" aria-label={termo.nome} onCancel={e=>{e.preventDefault();e.stopPropagation();onClose();}} onClick={e=>{e.stopPropagation();if(e.target===e.currentTarget)onClose();}}>
    <div className="id-card termo-card" style={{'--id-cor':termo.cor} as CSSProperties}>
      <button className="icon-button id-card-close" aria-label="Fechar" onClick={onClose}><X size={18}/></button>
      <div className="id-card-top">
        <span className="id-card-medal termo-medal" aria-hidden>{ehStatus?<img src={`/assets/statuses/${termo.id}.png`} width={30} height={30} alt=""/>:<b>{termo.nome.slice(0,1).toUpperCase()}</b>}</span>
        <div><span className="id-card-family">{termo.rotulo}</span><h2>{termo.nome}</h2></div>
      </div>
      <p className="id-card-lead">{termo.texto}</p>
      {termo.extra&&<p className="termo-extra">{termo.extra}</p>}
      <button className="primary id-card-ok" onClick={onClose}>Entendi</button>
    </div>
  </dialog>;
}

/** Um termo do glossário, tocável. */
export function TermoBotao({termo,children}:{termo:Termo;children?:ReactNode}){
  const [aberto,setAberto]=useState(false);
  return <>
    <button type="button" className="termo" style={{'--termo-cor':termo.cor} as CSSProperties} onClick={e=>{e.stopPropagation();setAberto(true);}} aria-label={`${termo.nome}: o que é?`}>{children??termo.nome}</button>
    {aberto&&createPortal(<CartaoDoTermo termo={termo} onClose={()=>setAberto(false)}/>,document.body)}
  </>;
}

/** Um texto qualquer, com os termos do glossário tocáveis. */
export function ComTermos({texto}:{texto:string}){
  return <>{acharTermos(texto).map((x,i)=>typeof x==='string'?<Fragment key={i}>{x}</Fragment>:<TermoBotao key={i} termo={x.termo}>{x.texto}</TermoBotao>)}</>;
}
