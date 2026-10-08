import { ArrowUpRight,ArrowDownRight } from 'lucide-react';
import type { Status } from '../engine/types';
import { statuses } from '../data/statuses';
import { valorAtualDoStatus } from '../engine/skill-descriptions';
const positive=new Set(['protected','haste','regen','strengthened']);
export function StatusBadge({status,onClick}:{status:Status;onClick?:()=>void}){
  const item=statuses[status.id],valor=valorAtualDoStatus(status.id,status.intensity),nome=valor?`${item.name} ${valor}`:item.name,good=positive.has(status.id),progress=Math.max(0,Math.min(100,100*status.remaining/Math.max(1,status.duration??status.remaining)));
  const content=<><img className="status-icon-art" src={`/assets/statuses/${status.id}.png`} width={14} height={14} alt="" aria-hidden="true"/><svg viewBox="0 0 24 24" className="status-duration" aria-hidden="true"><circle cx="12" cy="12" r="10" pathLength="100" strokeDasharray={`${progress} 100`}/></svg>{good?<ArrowUpRight className="status-tone" size={7}/>:<ArrowDownRight className="status-tone" size={7}/>}</>;
  const className=`status-badge ${good?'positive':'negative'}`;
  return onClick?<button className={className} onClick={onClick} aria-label={`${nome}, ${status.remaining.toLocaleString('pt-BR',{maximumFractionDigits:1})} segundos restantes`} title={nome}>{content}</button>:<span className={className} title={nome}>{content}</span>;
}
