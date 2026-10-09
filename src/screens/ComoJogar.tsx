import { useState,type CSSProperties } from 'react';
import { ArrowLeft,ArrowRight,CircleHelp,HeartPulse,Orbit,Play,Shield,Swords,Trophy,Users,Zap,Eye,Check } from 'lucide-react';
import { byId } from '../data/characters';
import { Portrait } from '../components/Portrait';
import { SkillIcon } from '../components/Icon';
import { StatusBadge } from '../components/StatusBadge';
import { TelaTopo } from '../components/Casca';
import { TermoBotao } from '../components/Termos';
import { GLOSSARIO,type Termo } from '../presentation/glossario';
import { statuses } from '../data/statuses';

/*
 * Como jogar (remake): aprender jogando o olho, não lendo.
 *
 * Três abas no topo, uma tela cada — sem rolar meia hora:
 *   Passo a passo  seis cartas com a cena animada (ataque, Carga, Preparo,
 *                  Escudo, Status, Vantagem), uma por vez, com avançar/voltar;
 *   Regras         as mecânicas como peças tocáveis: tocar abre o cartão;
 *   Status         todos os Status com o ícone novo, bons em cima e ruins
 *                  embaixo, tocar explica.
 */
const PASSOS=[
  {titulo:'Ataque básico',texto:'O círculo do retrato enche. Cheio, o lutador ataca sozinho.',icone:Swords,cor:'#ff9a76'},
  {titulo:'Carga',texto:'Cada habilidade enche de 0% a 100%. Cheia, o ícone acende e ela sai.',icone:Zap,cor:'#c8f560'},
  {titulo:'Preparo',texto:'Habilidade grande demora para sair. Nesse tempo, pode ser cortada.',icone:Orbit,cor:'#f4d47e'},
  {titulo:'Escudo',texto:'A barreira azul segura o golpe antes da Vida.',icone:Shield,cor:'#8fd3ff'},
  {titulo:'Status',texto:'Ícones sobre o retrato: efeitos bons ou ruins enquanto durarem.',icone:HeartPulse,cor:'#c3a2ff'},
  {titulo:'Pontos',texto:'Vença as 10 lutas. Terminar com mais Vida e mais gente de pé dá mais pontos.',icone:Trophy,cor:'#ffd36b'},
] as const;

function Cena({i}:{i:number}){
  if(i===0)return <div className="demo-art demo-attack"><div className="demo-actor"><Portrait character={byId.goku}/><i/></div><span className="demo-travel">→</span><div className="demo-victim"><Portrait character={byId.vegeta}/><b>−66</b></div></div>;
  if(i===1)return <div className="demo-art demo-charge"><SkillIcon type={byId.goku.skills[0].icon} characterId="goku" skillId={byId.goku.skills[0].id} size={51}/><div><span>CARGA DA HABILIDADE</span><i/><strong>100% · PRONTA</strong></div></div>;
  if(i===2)return <div className="demo-art demo-prep"><div className="prep-portrait"><Portrait character={byId.goku}/><i/></div><div><strong>PREPARANDO</strong><span>Kamehameha</span><small>Pode ser interrompido</small></div></div>;
  if(i===3)return <div className="demo-art demo-shield"><Shield size={58}/><div><span>ESCUDO</span><strong>180 bloqueado</strong><i/></div></div>;
  if(i===4)return <div className="demo-art demo-status"><Portrait character={byId.vegeta}/><span>→</span><StatusBadge status={{id:'exposed',remaining:8,duration:8,intensity:.22,source:''}}/><strong>EXPOSTO</strong></div>;
  // a escala de uma luta (src/engine/pontos.ts): o que o trio fez vale, até na derrota
  return <div className="cj-pontos"><span><b>~10 mil</b><small>derrota feia</small></span><span><b>~100 mil</b><small>vitória boa</small></span><span><b>150 mil+</b><small>luta incrível</small></span></div>;
}

/* Regras do jogo que não estão no glossário da ficha. */
const BASE:Termo[]=[
  {id:'trio',nome:'Trio',cor:'#c8f560',rotulo:'COMEÇO',texto:'Você escolhe 3 lutadores. Eles lutam sozinhos: seu trabalho é montar um trio que funcione junto.'},
  {id:'jornada',nome:'Jornada',cor:'#ffd36b',rotulo:'OBJETIVO',texto:'10 lutas seguidas. Cada luta soma pontos pelo que o trio fez: dano, nocautes, cura e proteção, habilidades, Status, ritmo, Carga e manter o trio vivo — com o peso certo para cada personagem, para todo estilo de jogo pontuar parecido. A vitória vale 25 mil a mais. Uma derrota encerra a jornada, mas os pontos dela ficam.'},
  {id:'vida',nome:'Vida',cor:'#86e3a8',rotulo:'SOBREVIVER',texto:'Quando chega a zero, o lutador sai da luta. A Vida que sobra no fim vale pontos.'},
  {id:'basico',nome:'Ataque básico',cor:'#ff9a76',rotulo:'RITMO',texto:'O golpe de sempre, com o nome e o jeito de cada lutador: uns quicam no segundo rival, uns pegam dois, uns curam o aliado, roubam Carga ou fecham um combo no 3º golpe. O círculo em volta do retrato mostra quanto falta para o próximo.'},
  {id:'vantagem',nome:'Vantagem',cor:'#8fd3ff',rotulo:'QUEM DOMINA',texto:'A barra do topo mostra quem está controlando a luta. Algumas habilidades reagem a ela; virar o jogo dá pontos.'},
  {id:'investigacao',nome:'Investigação',cor:'#f4d47e',rotulo:'ESTUDAR O RIVAL',texto:'Alguns lutadores estudam um inimigo por vez. Ao chegar a 100, abrem uma habilidade que só funciona contra quem foi estudado.'},
  {id:'inteligencia',nome:'Inteligência',cor:'#c3a2ff',rotulo:'DECISÕES',texto:'De 0 a 100: quanto melhor, mais o lutador escolhe o alvo e a hora certa sozinho.'},
];

export function HelpScreen({onPlay}:{onPlay:()=>void}){
  const [aba,setAba]=useState<'passos'|'regras'|'status'>('passos'),[passo,setPasso]=useState(0),[revisto,setRevisto]=useState(false);
  const mecanicas=[...BASE,...GLOSSARIO.filter(t=>!(t.id in statuses))];
  const doStatus=GLOSSARIO.filter(t=>t.id in statuses);
  const p=PASSOS[passo],ultimo=passo===PASSOS.length-1;
  return <section className="comojogar-v2">
    <TelaTopo icone={<CircleHelp/>} cor="#8fd3ff" rotulo="COMO JOGAR" titulo="Aprenda em 1 minuto"/>
    <div className="cj-abas" role="tablist">{([['passos','Passo a passo'],['regras','Regras'],['status','Status']] as const).map(([id,nome])=><button key={id} role="tab" aria-selected={aba===id} className={aba===id?'ativo':''} onClick={()=>setAba(id)}>{nome}</button>)}</div>

    {aba==='passos'&&<div className="cj-passo" style={{'--cj':p.cor} as CSSProperties}>
      <div className="cj-cena" key={passo}><Cena i={passo}/></div>
      <div className="cj-texto" key={`t${passo}`}><span className="cj-num"><p.icone size={15}/>{passo+1} / {PASSOS.length}</span><h2>{p.titulo}</h2><p>{p.texto}</p></div>
      <div className="cj-pontinhos">{PASSOS.map((x,i)=><button key={x.titulo} aria-label={`Passo ${i+1}: ${x.titulo}`} className={i===passo?'ativo':i<passo?'visto':''} onClick={()=>setPasso(i)}/>)}</div>
      <div className="cj-nav">
        <button className="secondary" disabled={passo===0} onClick={()=>setPasso(passo-1)} aria-label="Passo anterior"><ArrowLeft size={18}/></button>
        {ultimo?<button className="primary gs-cta" onClick={onPlay}><Play size={18} fill="currentColor"/>Montar meu trio</button>
          :<button className="primary cj-proximo" onClick={()=>setPasso(passo+1)}>Próximo<ArrowRight size={18}/></button>}
      </div>
    </div>}

    {aba==='regras'&&<div className="cj-pecas">{mecanicas.map((t,i)=><TermoBotao key={t.id} termo={t} className="cj-peca"><span style={{'--i':i} as CSSProperties}><b>{t.nome}</b><small>{t.rotulo}</small></span></TermoBotao>)}</div>}

    {aba==='status'&&<div className="cj-status">{(['positivo','negativo'] as const).map(tom=><div key={tom}>
      <h2 className={tom}>{tom==='positivo'?'BONS · ajudam quem recebe':'RUINS · atrapalham quem recebe'}</h2>
      <div className="cj-status-grade">{doStatus.filter(t=>statuses[t.id as keyof typeof statuses].tone===tom).map(t=><TermoBotao key={t.id} termo={t} className="cj-status-peca"><img src={`/assets/statuses/${t.id}.png`} alt="" width={40} height={40}/><b>{t.nome}</b></TermoBotao>)}</div>
    </div>)}</div>}

    <div className="cj-rodape">
      <button className="secondary" onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1');setRevisto(true);}catch{return}}}>{revisto?<Check size={16}/>:<Eye size={16}/>}{revisto?'O guia volta na próxima luta':'Rever guia na próxima batalha'}</button>
      {!(aba==='passos'&&ultimo)&&<button className="primary gs-cta" onClick={onPlay}><Users size={17}/>Montar meu trio</button>}
    </div>
  </section>;
}
