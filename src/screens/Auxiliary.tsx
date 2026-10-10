import { useEffect,useMemo,useState } from 'react';
import { Search,Users } from 'lucide-react';
import { TelaTopo } from '../components/Casca';
import { characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { Album } from '../components/Album';
import { ABAS,PERSONAGENS_DA_ABA,type Aba } from '../lib/conquistas';
import type { Character } from '../engine/types';
import { corDaIdentidade } from '../components/IdentityChips';
import { identidadesDe,ordemDasIdentidades,type Identidade } from '../presentation/identities';

/*
 * Personagens (pedido do jogador): o mesmo álbum das Conquistas — as abas
 * Anime, Heróis, Games e Desenhos e as páginas de 6 × 5 retratos que passam de
 * lado —, em vez da lista comprida. A busca e o filtro de função continuam:
 * filtram dentro das abas, e cada aba mostra quantos sobraram. Se a busca não
 * acha ninguém na aba aberta, o álbum pula para a primeira que tem.
 */
export function CharactersScreen({onDetails}:{onDetails:(id:string)=>void}){
  const [query,setQuery]=useState(''),[role,setRole]=useState<Identidade|'Todas'>('Todas'),[aba,setAba]=useState<Aba>('anime');
  const listas=useMemo(()=>{
    const sem=(t:string)=>t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const passa=(c:Character)=>(role==='Todas'||identidadesDe(c).includes(role))&&sem(`${c.name} ${c.universe}`).includes(sem(query));
    return Object.fromEntries(ABAS.map(a=>[a.id,PERSONAGENS_DA_ABA[a.id].filter(passa)])) as Record<Aba,Character[]>;
  },[query,role]);
  const total=ABAS.reduce((n,a)=>n+listas[a.id].length,0);
  useEffect(()=>{if(!listas[aba].length){const outra=ABAS.find(a=>listas[a.id].length);if(outra)setAba(outra.id);}},[listas,aba]);
  return <section className="roster-v2">
    <TelaTopo icone={<Users/>} cor="#ffb86b" rotulo="COLEÇÃO" titulo={`${characters.length} lutadores`}/>
    <label className="rv-busca"><Search size={18}/><input aria-label="Buscar personagem" placeholder="Buscar por nome ou universo…" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button aria-label="Limpar busca" onClick={()=>setQuery('')}>×</button>}</label>
    <div className="rv-filtro" aria-label="Filtrar por função">{(['Todas',...ordemDasIdentidades] as const).map(x=><button key={x} className={role===x?'ativo':''} style={x==='Todas'?undefined:{'--id-cor':corDaIdentidade(x)} as React.CSSProperties} onClick={()=>setRole(x)}>{x}</button>)}</div>
    {(role!=='Todas'||query)&&<p className="rv-conta"><b>{total}</b> {total===1?'lutador':'lutadores'}<button className="text-button" onClick={()=>{setRole('Todas');setQuery('');}}>limpar filtros</button></p>}
    <Album aba={aba} onAba={setAba} listas={listas} rotulo={a=>`${listas[a].length}${role!=='Todas'||query?` de ${PERSONAGENS_DA_ABA[a].length}`:''}`}
      vazio={<p className="empty-state">Nenhum lutador com esse nome, universo ou função.</p>}
      carta={(c,i)=><button key={c.id} className="cq-carta liberada rv-album-carta" style={{'--character':c.color,'--i':i} as React.CSSProperties} onClick={()=>onDetails(c.id)} aria-label={`${c.name}, ${c.universe}`}>
        <span className="cq-retrato"><Portrait character={c}/></span>
        <small>{c.name}</small>
        <span className="rv-album-funcoes">{identidadesDe(c).map(x=><i key={x} title={x} style={{'--id-cor':corDaIdentidade(x)} as React.CSSProperties}/>)}</span>
      </button>}/>
  </section>;
}
