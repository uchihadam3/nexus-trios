import { useEffect,type CSSProperties,type ReactNode } from 'react';
import { ArrowLeft,Award,CircleHelp,Crown,Home as HomeIcon,Menu,Settings2,ShieldCheck,Trophy,Users,X } from 'lucide-react';
import { battleAudio } from '../lib/audio';
import { PRIORIDADE,type Sound } from '../audio/cues';
import { formatarPontos } from '../engine/pontos';

/*
 * A casca do jogo (remake): a barra de cima, o menu e o que vale para todo
 * botão.
 *
 * A barra é a de um jogo: fora do início, um botão redondo de voltar; o logo;
 * o recorde de pontos sempre à vista; e o menu, que no celular abre um painel
 * de botões grandes com ícone. Todo toque num botão solta um estouro de luz
 * desenhado em Python (folha "toque") no ponto do dedo e um som de interface
 * também feito em Python — o de confirmar nos botões principais, o de abrir
 * nos que abrem um cartão, o de fechar nos que fecham.
 */

export type Destino='home'|'characters'|'conquistas'|'ranking'|'help'|'settings'|'conta';

const Fx=({nome,cor,ms,className,laco=true}:{nome:string;cor:string;ms:number;className:string;laco?:boolean})=>
  <span aria-hidden className={`uifx ${laco?'uifx-laco':''} ${className}`} style={{'--uifx-img':`url(/assets/ui/fx/${nome}.webp)`,'--uifx-cor':cor,'--uifx-dur':`${ms}ms`} as CSSProperties}/>;

const ITENS:{id:Destino;nome:string;icone:typeof HomeIcon;cor:string;online?:boolean}[]=[
  {id:'home',nome:'Início',icone:HomeIcon,cor:'#c8f560'},
  {id:'characters',nome:'Personagens',icone:Users,cor:'#ffb86b'},
  {id:'conquistas',nome:'Conquistas',icone:Award,cor:'#ffc65a'},
  {id:'ranking',nome:'Ranking',icone:Trophy,cor:'#ffd36b'},
  {id:'help',nome:'Como jogar',icone:CircleHelp,cor:'#8fd3ff'},
  {id:'settings',nome:'Configurações',icone:Settings2,cor:'#c3a2ff'},
  {id:'conta',nome:'Conta',icone:ShieldCheck,cor:'#86e3a8'},
];

export function Cabecalho({tela,menu,onMenu,onNavigate,recorde,apelido,online,total}:{tela:string;menu:boolean;onMenu:(aberto:boolean)=>void;onNavigate:(d:Destino)=>void;recorde:number;apelido?:string;online:boolean;total:number}){
  const itens=ITENS.filter(i=>!i.online||online);
  useEffect(()=>{if(!menu)return;const fecha=(e:KeyboardEvent)=>{if(e.key==='Escape')onMenu(false);};addEventListener('keydown',fecha);return()=>removeEventListener('keydown',fecha);},[menu,onMenu]);
  return <header className="gs-barra">
    {tela!=='home'&&<button className="gs-voltar" onClick={()=>onNavigate('home')} aria-label="Voltar ao início" title="Voltar ao início"><ArrowLeft size={20}/></button>}
    <button className="gs-marca" onClick={()=>onNavigate('home')} aria-label="Nexus início"><b>N</b><span>NEXUS<small>DUELO DE TRIOS</small></span></button>
    <nav aria-label="Navegação principal" className={`gs-nav ${menu?'aberto':''}`}>
      <div className="gs-nav-grade">{itens.map((i,k)=><button key={i.id} className={tela===i.id?'ativo':''} onClick={()=>onNavigate(i.id)} aria-label={i.nome} style={{'--tile':i.cor,'--k':k} as CSSProperties}>
        <i.icone size={22}/><b>{i.nome}</b>{i.id==='characters'&&<small>{total}</small>}
      </button>)}</div>
    </nav>
    <span className="gs-recorde" title="Seu recorde de pontos"><Crown size={14}/><b>{formatarPontos(recorde)}</b>{apelido&&<small>{apelido}</small>}</span>
    <button className="gs-menu menu-toggle" aria-label="Abrir menu" aria-expanded={menu} onClick={()=>onMenu(!menu)}>{menu?<X size={22}/>:<Menu size={22}/>}</button>
    {menu&&<button className="gs-veu" aria-label="Fechar menu" tabIndex={-1} onClick={()=>onMenu(false)}/>}
  </header>;
}

/** O topo de cada tela: medalhão com o anel de runas girando, rótulo e título. */
export function TelaTopo({icone,cor,rotulo,titulo,children}:{icone:ReactNode;cor:string;rotulo:string;titulo:string;children?:ReactNode}){
  return <header className="gs-topo" style={{'--tela':cor} as CSSProperties}>
    <span className="gs-medalhao"><Fx nome="anel" cor={cor} ms={4800} className="gs-anel"/>{icone}</span>
    <div><span className="gs-rotulo">{rotulo}</span><h1>{titulo}</h1>{children}</div>
  </header>;
}

/* Qual som cada botão faz. */
function somDoBotao(el:HTMLElement):Sound|null{
  if(el.closest('.battle-main .arena, [data-sem-som]'))return null;
  if(el instanceof HTMLInputElement)return el.type==='checkbox'?'ui-alternar':null;
  const nome=el.getAttribute('aria-label')??'';
  if(/^Fechar/.test(nome)||el.matches('.modal-close,.id-card-close,.id-card-ok,.gs-veu'))return 'ui-fechar';
  // os dois momentos que mais importam na escolha do trio têm som próprio
  if(el.matches('.dv-arena'))return 'ui-arena';
  if(el.matches('.dv-escolher'))return 'ui-escolher';
  if(el.matches('.primary,.hv-cta,.rs-cta,.gs-cta'))return 'ui-confirma';
  if(el.matches('.termo,.id-chip,.gs-menu,.rv-carta,.dv-retrato,[aria-haspopup]'))return 'ui-abrir';
  return 'ui-clique';
}

/** Estouro de luz no ponto do toque e som de interface em todo botão do jogo. */
export function ToqueGlobal(){
  useEffect(()=>{
    const reduzido=()=>matchMedia('(prefers-reduced-motion: reduce)').matches||!!document.querySelector('.app.reduce-motion');
    const toque=(e:PointerEvent)=>{
      const alvo=(e.target as HTMLElement|null)?.closest<HTMLElement>('button,[role="button"],a[href]');
      if(!alvo||alvo.matches(':disabled')||reduzido()||alvo.closest('.battle-main .arena'))return;
      const fx=document.createElement('span');
      fx.className='uifx gs-toque';fx.setAttribute('aria-hidden','true');
      const cor=getComputedStyle(alvo).getPropertyValue('--tile')||getComputedStyle(alvo).getPropertyValue('--character')||'#d8ff7a';
      fx.style.cssText=`left:${e.clientX}px;top:${e.clientY}px;--uifx-img:url(/assets/ui/fx/toque.webp);--uifx-cor:${cor.trim()||'#d8ff7a'};--uifx-dur:420ms`;
      document.body.appendChild(fx);setTimeout(()=>fx.remove(),460);
    };
    const clique=(e:MouseEvent)=>{
      const alvo=(e.target as HTMLElement|null)?.closest<HTMLElement>('button,[role="button"],a[href],input[type="checkbox"]');
      if(!alvo||alvo.matches(':disabled'))return;
      const som=somDoBotao(alvo);if(som)battleAudio.sound(som,PRIORIDADE.interface,0,Math.floor(performance.now()));
    };
    addEventListener('pointerdown',toque,{capture:true,passive:true});
    addEventListener('click',clique,{capture:true});
    return()=>{removeEventListener('pointerdown',toque,{capture:true});removeEventListener('click',clique,{capture:true});};
  },[]);
  return null;
}
