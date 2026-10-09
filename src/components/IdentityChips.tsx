import { useEffect,useRef,useState,type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import { BatteryCharging,Bomb,Castle,Droplet,Flame,Megaphone,Hexagon,Asterisk,CircleArrowDown,CircleArrowUp,Crosshair,Droplets,Gauge,HandHelping,HandHeart,Heart,HeartPulse,Hourglass,Lock,Radar,RotateCcw,Scissors,ShieldPlus,Skull,Sparkles,Sprout,Swords,Timer,TriangleAlert,X,type LucideIcon } from 'lucide-react';
import { byId } from '../data/characters';
import { Portrait } from './Portrait';
import { exemplosDe,explicacaoDaIdentidade,familiaDaIdentidade,guiaDaIdentidade,quantosTem,type Identidade } from '../presentation/identities';

/*
 * As etiquetas de identidade (Pressão, Área, Controle…) são botões: tocar numa
 * abre um cartão curto que explica o que ela faz, em linguagem de jogo. Serve
 * para quem está montando o trio e não sabe o que "Especialista" quer dizer.
 */
const ICONE:Record<Identidade,LucideIcon>={
  'Pressão':Gauge,'Explosão':Bomb,'Finalização':Skull,'Área':Radar,'Dano contínuo':Droplets,
  'Tanque':Castle,'Sobrevivência':HeartPulse,'Proteção':ShieldPlus,'Cura':Heart,'Regeneração':Sprout,
  'Controle':Lock,'Interrupção':Scissors,'Ritmo':Timer,'Suporte':HandHelping,'Carga':BatteryCharging,
  'Buff':CircleArrowUp,'Debuff':CircleArrowDown,'Virada':RotateCcw,'Preparação':Hourglass,'Transformação':Sparkles,
  'Contra-ataque':Swords,'Especialista':Crosshair,'Reviver':HandHeart,'Renascer':Flame,'Provocar':Megaphone,'Roubo de vida':Droplet,'Refletir':Hexagon,'Espinhos':Asterisk,
};
const FAMILIA={
  ataque:{nome:'ATAQUE',cor:'#ff9a76'},atrapalha:{nome:'ATRAPALHA O RIVAL',cor:'#c3a2ff'},ajuda:{nome:'AJUDA O TRIO',cor:'#86e3a8'},
  aguenta:{nome:'AGUENTA PANCADA',cor:'#8cc4ff'},jeito:{nome:'JEITO DE LUTAR',cor:'#ffd66e'},
} as const;
export const corDaIdentidade=(x:Identidade)=>FAMILIA[familiaDaIdentidade[x]].cor;

function CartaoDaIdentidade({inicial,trio,onClose}:{inicial:Identidade;trio?:readonly Identidade[];onClose:()=>void}){
  const ref=useRef<HTMLDialogElement>(null);
  const [x,setX]=useState(inicial);
  useEffect(()=>{const d=ref.current;d?.showModal();return()=>d?.close();},[]);
  const guia=guiaDaIdentidade[x],familia=FAMILIA[familiaDaIdentidade[x]],Icone=ICONE[x];
  const total=quantosTem(x),exemplos=exemplosDe(x).map(id=>byId[id]).filter(Boolean);
  const temNoTrio=trio?.includes(x);
  return <dialog ref={ref} className="id-card-dialog" aria-label={`O que é ${x}`} onCancel={e=>{e.preventDefault();e.stopPropagation();onClose();}} onClick={e=>{e.stopPropagation();if(e.target===e.currentTarget)onClose();}}>
    <div key={x} className="id-card" style={{'--id-cor':familia.cor} as CSSProperties}>
      <button className="icon-button id-card-close" aria-label="Fechar" onClick={onClose}><X size={18}/></button>
      <div className="id-card-top">
        <span className="id-card-medal" aria-hidden><Icone size={30} strokeWidth={2.2}/></span>
        <div><span className="id-card-family">{familia.nome}</span><h2>{x}</h2></div>
      </div>
      <p className="id-card-lead">{explicacaoDaIdentidade[x]}</p>
      {trio&&<p className={`id-card-trio ${temNoTrio?'tem':''}`}>{temNoTrio?'✓ Seu trio já tem':'Seu trio ainda não tem'}</p>}
      <h3>Na luta</h3>
      <ol className="id-card-steps">{guia.naLuta.map((t,i)=><li key={i}><span>{i+1}</span>{t}</li>)}</ol>
      <h3>Combina com</h3>
      <div className="id-card-combos">{guia.combina.map(c=>{const I=ICONE[c];return <button key={c} style={{'--id-cor':corDaIdentidade(c)} as CSSProperties} onClick={()=>setX(c)}><I size={14}/>{c}</button>;})}</div>
      <p className="id-card-warn"><TriangleAlert size={16}/><span><b>Cuidado com</b>{guia.cuidado}</span></p>
      <div className="id-card-who"><small>{total} {total===1?'lutador tem':'lutadores têm'}</small><div>{exemplos.map(c=><span key={c.id} style={{'--character':c.color} as CSSProperties}><Portrait character={c} className="tiny"/><em>{c.name}</em></span>)}</div></div>
      <button className="primary id-card-ok" onClick={onClose}>Entendi</button>
    </div>
  </dialog>;
}

/** Linha de etiquetas tocáveis. `trio` mostra no cartão se o trio já tem aquela identidade. */
/** `novas`: identidades que o trio ainda não tem — brilham, porque são o que este lutador acrescenta. */
export function IdentityChips({ids,trio,marca,novas}:{ids:readonly Identidade[];trio?:readonly Identidade[];marca?:string;novas?:readonly Identidade[]}){
  const [aberta,setAberta]=useState<Identidade|null>(null);
  return <div className="role-chips id-chips">
    {ids.map(x=><button type="button" key={x} className={`id-chip ${novas?.includes(x)?'novo':''}`} style={{'--id-cor':corDaIdentidade(x)} as CSSProperties} aria-label={`${x}: o que é?`}
      onClick={e=>{e.stopPropagation();setAberta(x);}}>{marca}{x}<i aria-hidden>?</i></button>)}
    {aberta&&createPortal(<CartaoDaIdentidade inicial={aberta} trio={trio} onClose={()=>setAberta(null)}/>,document.body)}
  </div>;
}
