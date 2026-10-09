import { useEffect,useRef,useState } from 'react';
import { Search,Users } from 'lucide-react';
import { TelaTopo } from '../components/Casca';
import { characters } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { corDaIdentidade } from '../components/IdentityChips';
import { identidadesDe,ordemDasIdentidades,type Identidade } from '../presentation/identities';

/*
 * Os lutadores (remake): uma coleção de cartas.
 *
 * Busca no topo, filtros como fileiras de chips que deslizam (universo e
 * função), e a grade de cartas: retrato, nome, universo e as etiquetas em
 * cor. Mais cartas entram sozinhas conforme a rolagem chega ao fim — sem
 * botão de "ver mais". Tocar numa carta abre a ficha.
 */
export function CharactersScreen({onDetails}:{onDetails:(id:string)=>void}){
  const [query,setQuery]=useState(''),[universe,setUniverse]=useState('Todos'),[role,setRole]=useState<Identidade|'Todas'>('Todas'),[visibleCount,setVisibleCount]=useState(30);
  const sem=(t:string)=>t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const filtered=characters.filter(c=>(universe==='Todos'||c.universe===universe)&&(role==='Todas'||identidadesDe(c).includes(role))&&sem(`${c.name} ${c.universe}`).includes(sem(query)));
  // em ordem alfabética (pedido do jogador: "fica mais fácil de achar"), e não pela quantidade de personagens
  const universos=['Todos',...[...new Set(characters.map(c=>c.universe))].sort((a,b)=>a.localeCompare(b,'pt-BR',{sensitivity:'base'}))];
  const fim=useRef<HTMLDivElement>(null);
  useEffect(()=>{const el=fim.current;if(!el||typeof IntersectionObserver==='undefined')return;const o=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting))setVisibleCount(n=>n+30);},{rootMargin:'400px'});o.observe(el);return()=>o.disconnect();},[filtered.length]);
  const muda=(f:()=>void)=>{f();setVisibleCount(30);};
  return <section className="roster-v2">
    <TelaTopo icone={<Users/>} cor="#ffb86b" rotulo="COLEÇÃO" titulo={`${characters.length} lutadores`}/>
    <label className="rv-busca"><Search size={18}/><input aria-label="Buscar personagem" placeholder="Buscar por nome ou universo…" value={query} onChange={e=>muda(()=>setQuery(e.target.value))}/>{query&&<button aria-label="Limpar busca" onClick={()=>muda(()=>setQuery(''))}>×</button>}</label>
    <div className="rv-filtro" aria-label="Filtrar por função">{(['Todas',...ordemDasIdentidades] as const).map(x=><button key={x} className={role===x?'ativo':''} style={x==='Todas'?undefined:{'--id-cor':corDaIdentidade(x)} as React.CSSProperties} onClick={()=>muda(()=>setRole(x))}>{x}</button>)}</div>
    <div className="rv-filtro rv-universos" aria-label="Filtrar por universo">{universos.map(u=><button key={u} className={universe===u?'ativo':''} onClick={()=>muda(()=>setUniverse(u))}>{u}</button>)}</div>
    <p className="rv-conta"><b>{filtered.length}</b> {filtered.length===1?'lutador':'lutadores'}{(role!=='Todas'||universe!=='Todos'||query)&&<button className="text-button" onClick={()=>muda(()=>{setRole('Todas');setUniverse('Todos');setQuery('');})}>limpar filtros</button>}</p>
    <div className="rv-grade">{filtered.slice(0,visibleCount).map((c,i)=><button className="rv-carta roster-card" key={c.id} onClick={()=>onDetails(c.id)} style={{'--character':c.color,'--i':i%30} as React.CSSProperties}>
      <Portrait character={c}/>
      <span className="rv-universo">{c.universe}</span>
      <span className="rv-nome"><b>{c.name}</b><span className="rv-tags">{identidadesDe(c).map(x=><i key={x} style={{'--id-cor':corDaIdentidade(x)} as React.CSSProperties}>{x}</i>)}</span></span>
    </button>)}</div>
    <div ref={fim} aria-hidden/>
    {!filtered.length&&<p className="empty-state">Nenhum lutador com esse nome, universo ou função.</p>}
  </section>;
}
