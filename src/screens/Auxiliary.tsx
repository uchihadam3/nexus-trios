import { useEffect,useRef,useState } from 'react';
import { Search,ArrowUpRight,Users,Zap,Swords,Orbit,RotateCcw,Eye,Shield,HeartPulse,Volume2,SlidersHorizontal,Gamepad2,CircleHelp } from 'lucide-react';
import { characters,byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { StatusBadge } from '../components/StatusBadge';
import { statuses } from '../data/statuses';
import { presentStatus,positiveStatuses } from '../engine/skill-descriptions';
import { corDaIdentidade } from '../components/IdentityChips';
import { identidadesDe,ordemDasIdentidades,type Identidade } from '../presentation/identities';
import type { Settings } from '../lib/storage';

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
  const universos=['Todos',...[...new Set(characters.map(c=>c.universe))].sort((a,b)=>characters.filter(c=>c.universe===b).length-characters.filter(c=>c.universe===a).length)];
  const fim=useRef<HTMLDivElement>(null);
  useEffect(()=>{const el=fim.current;if(!el||typeof IntersectionObserver==='undefined')return;const o=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting))setVisibleCount(n=>n+30);},{rootMargin:'400px'});o.observe(el);return()=>o.disconnect();},[filtered.length]);
  const muda=(f:()=>void)=>{f();setVisibleCount(30);};
  return <section className="roster-v2">
    <header className="rv-topo"><span className="rv-rotulo">COLEÇÃO</span><h1>{characters.length} lutadores</h1></header>
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

const demos=[
  {title:'Ataque básico',detail:'O círculo enche. O lutador age e o alvo recebe o impacto.',icon:Swords},
  {title:'Carga',detail:'A habilidade enche de 0% a 100%. Quando fica pronta, o ícone acende.',icon:Zap},
  {title:'Preparo',detail:'Uma habilidade começou, mas ainda pode ser interrompida.',icon:Orbit},
  {title:'Escudo',detail:'A barreira absorve o impacto antes da Vida.',icon:Shield},
  {title:'Status',detail:'O efeito chega ao alvo e seu ícone permanece enquanto durar.',icon:HeartPulse},
  {title:'Vantagem',detail:'O medidor reage à luta. Algumas habilidades dependem dele; a vitória não.',icon:Users},
] as const;
function DemoArt({index}:{index:number}){
  if(index===0)return <div className="demo-art demo-attack"><div className="demo-actor"><Portrait character={byId.goku}/><i/></div><span className="demo-travel">→</span><div className="demo-victim"><Portrait character={byId.vegeta}/><b>−66</b></div></div>;
  if(index===1)return <div className="demo-art demo-charge"><SkillIcon type={byId.goku.skills[0].icon} characterId="goku" skillId={byId.goku.skills[0].id} size={51}/><div><span>CARGA DA HABILIDADE</span><i/><strong>100% · PRONTA</strong></div></div>;
  if(index===2)return <div className="demo-art demo-prep"><div className="prep-portrait"><Portrait character={byId.goku}/><i/></div><div><strong>PREPARANDO</strong><span>Kamehameha</span><small>Pode ser interrompido</small></div></div>;
  if(index===3)return <div className="demo-art demo-shield"><Shield size={58}/><div><span>ESCUDO</span><strong>180 bloqueado</strong><i/></div></div>;
  if(index===4)return <div className="demo-art demo-status"><Portrait character={byId.vegeta}/><span>→</span><StatusBadge status={{id:'exposed',remaining:8,duration:8,intensity:.22,source:''}}/><strong>EXPOSTO</strong></div>;
  return <div className="demo-art demo-advantage"><span>RIVAIS</span><div><i/></div><span>SEU TRIO</span><strong>VIRADA!</strong></div>;
}
export function HelpScreen({onPlay}:{onPlay:()=>void}){
  const [active,setActive]=useState(0);
  const example=(id:keyof typeof statuses)=>characters.flatMap(c=>[...c.basic.effects,...c.trait.effects,...c.skills.flatMap(s=>s.effects)]).find(e=>e.kind==='status'&&e.status===id);
  const groups=[{title:'Começar',icon:Users,items:[['Trio','Escolha 3 personagens. Eles lutam automaticamente.'],['Jornada','Vença 10 confrontos. Uma derrota encerra a jornada.']]},{title:'Batalha',icon:Swords,items:[['Vida','Quando chega a zero, o personagem sai da luta.'],['Ataque básico','O círculo do retrato mostra quando será o próximo ataque.'],['Escudo','Absorve dano antes da Vida.'],['Interrupção','Cancela ou atrasa uma habilidade durante o Preparo.']]},{title:'Habilidades',icon:Zap,items:[['Carga','Cada habilidade vai de 0% a 100%. Com 100%, fica pronta.'],['Preparo','Tempo entre começar a habilidade e ela acontecer. Pode ser interrompido.'],['Resfriamento','Depois que a habilidade sai, ela espera este tempo antes de poder sair de novo.'],['Energia guardada','Alguns personagens acumulam energia durante a luta. Uma habilidade solta tudo de uma vez, como dano dividido entre os inimigos vivos.'],['Investigação','Alguns personagens estudam um inimigo por vez. Ao chegar a 100, abrem uma habilidade que só funciona contra quem foi estudado.']]},{title:'Vantagem',icon:Orbit,items:[['Vantagem','Mostra quem controla a luta. Algumas habilidades reagem quando o trio está à frente ou atrás. Não decide a vitória.'],['Sinergia','Quando a ação de um aliado ajuda outro personagem.'],['Inteligência','Mostra a qualidade das decisões automáticas, de 0 a 100.']]}];
  return <section className="help-screen"><div className="screen-title"><span className="eyebrow">GUIA VISUAL</span><h1>Aprenda vendo a luta.</h1><p>Escolha uma mecânica. A demonstração mostra onde olhar durante a batalha.</p></div>
    <div className="help-demo-shell"><div className="help-demo-tabs">{demos.map((demo,i)=><button key={demo.title} className={active===i?'active':''} onClick={()=>setActive(i)}><demo.icon size={16}/>{demo.title}</button>)}</div><div className="help-demo-stage" key={active}><DemoArt index={active}/><div className="demo-explanation"><span>0{active+1} / 06</span><h2>{demos[active].title}</h2><p>{demos[active].detail}</p></div></div></div>
    <div className="help-sections">{groups.map(group=><section className="help-group" key={group.title}><h2><group.icon size={22}/>{group.title}</h2><div className="help-items">{group.items.map(([name,description])=><article key={name}><strong>{name}</strong><p>{description}</p>{name==='Carga'&&<div className="charge-demo"><span>0%</span><i/><b>100% · PRONTA</b></div>}</article>)}</div></section>)}{(['positivo','negativo'] as const).map(tone=><section className="help-group" key={tone}><h2>Status {tone==='positivo'?'positivos':'negativos'}</h2><div className="status-legend"><div>{Object.keys(statuses).filter(id=>positiveStatuses.has(id as keyof typeof statuses)===(tone==='positivo')).map(id=>{const key=id as keyof typeof statuses,raw=example(key),value=raw?.kind==='status'?raw.value:0;return <span key={id}><StatusBadge status={{id:key,remaining:10,duration:10,intensity:value,source:''}}/><strong>{statuses[key].name}</strong><small>{presentStatus(key,value).summary}</small></span>})}</div></div></section>)}</div>
    <button className="secondary review-tutorial" onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1')}catch{return}}}><Eye size={16}/> Rever guia na próxima batalha</button><button className="primary" onClick={onPlay}>Montar meu trio <ArrowUpRight size={19}/></button>
  </section>;
}

export function SettingsScreen({settings:s,onChange,onReset}:{settings:Settings;onChange:(s:Settings)=>void;onReset:()=>void}){
  const [confirm,setConfirm]=useState(false);
  return <section className="settings-screen"><div className="screen-title"><span className="eyebrow">DO SEU JEITO</span><h1>Prepare sua experiência.</h1><p>Suas preferências ficam salvas neste dispositivo.</p></div>
    <div className="settings-list">
      <section className="settings-panel"><h2 className="settings-group"><Volume2 size={20}/> Áudio</h2><div className="setting-row"><div><h3>Volume</h3><p>Volume geral da trilha e dos efeitos de batalha.</p></div><input aria-label="Volume" type="range" min="0" max="100" value={s.volume} onChange={e=>onChange({...s,volume:Number(e.target.value)})}/></div>{([{key:'musicVolume',title:'Música de batalha',text:'Trilha original procedural. Baixo, percussão e sintetizadores.'},{key:'effectsVolume',title:'Efeitos sonoros',text:'Ações, proteção, interrupções e grandes viradas.'}] as const).map(x=><label className="setting-row" key={x.key}><div><h3>{x.title}</h3><p>{x.text}</p></div><input aria-label={x.title} type="range" min="0" max="100" value={s[x.key]} onChange={e=>onChange({...s,[x.key]:Number(e.target.value)})}/></label>)}</section>
      <section className="settings-panel"><h2 className="settings-group"><SlidersHorizontal size={20}/> Visual</h2>{([{key:'effects',title:'Efeitos visuais',text:'Raios, ondas e efeitos das habilidades.'},{key:'numbers',title:'Números de combate',text:'Dano, cura, Escudo e bloqueio aparecem sobre os alvos.'},{key:'reducedMotion',title:'Reduzir movimento',text:'Mantém fonte e alvo destacados, sem deslocamentos rápidos.'}] as const).map(x=><label className="setting-row" key={x.key}><div><h3>{x.title}</h3><p>{x.text}</p></div><input className="toggle" type="checkbox" checked={s[x.key]} onChange={e=>onChange({...s,[x.key]:e.target.checked})}/></label>)}</section>
      <section className="settings-panel"><h2 className="settings-group"><Gamepad2 size={20}/> Jogo</h2><div className="setting-row"><div><h3>Velocidade padrão</h3><p>A mesma simulação, no seu ritmo.</p></div><div className="segmented">{([1,2] as const).map(n=><button key={n} className={s.speed===n?'active':''} onClick={()=>onChange({...s,speed:n})}>{n}×</button>)}</div></div><label className="setting-row"><div><h3>Sequência automática</h3><p>Começa o próximo confronto após uma vitória.</p></div><input className="toggle" type="checkbox" checked={s.auto} onChange={e=>onChange({...s,auto:e.target.checked})}/></label></section>
      <section className="settings-panel"><h2 className="settings-group"><CircleHelp size={20}/> Ajuda</h2><div className="setting-row"><div><h3>Ajuda na batalha</h3><p>Mostra a legenda e dicas para entender habilidades e Status.</p></div><div className="segmented">{(['normal','detailed','off'] as const).map(mode=><button key={mode} className={s.explanations===mode?'active':''} onClick={()=>onChange({...s,explanations:mode})}>{mode==='normal'?'Normal':mode==='detailed'?'Detalhada':'Desligada'}</button>)}</div></div><button className="secondary review-tutorial" onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1')}catch{return}}}><Eye size={16}/> Rever tutorial na próxima batalha</button></section>
    </div>
    <div className="reset-box"><div><h3>Recomeçar do zero</h3><p>Apaga jornada, recordes e preferências deste dispositivo.</p></div>{confirm?<div className="reset-confirm"><button className="danger" onClick={onReset}>Apagar dados locais</button><button className="secondary" onClick={()=>setConfirm(false)}>Cancelar</button></div>:<button className="secondary" onClick={()=>setConfirm(true)}><RotateCcw size={16}/>Resetar dados</button>}</div>
  </section>;
}
