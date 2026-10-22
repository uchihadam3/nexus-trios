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
import { t, tx } from '../i18n/idioma';

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
  {titulo:tx('Ataque básico'),texto:tx('O círculo do retrato enche. Cheio, o lutador ataca sozinho.'),icone:Swords,cor:'#ff9a76'},
  {titulo:tx('Carga'),texto:tx('Cada habilidade enche de 0% a 100%. Cheia, o ícone acende e ela sai.'),icone:Zap,cor:'#c8f560'},
  {titulo:tx('Preparo'),texto:tx('Habilidade grande demora para sair. Nesse tempo, pode ser cortada.'),icone:Orbit,cor:'#f4d47e'},
  {titulo:tx('Escudo'),texto:tx('A barreira azul segura o golpe antes da Vida.'),icone:Shield,cor:'#8fd3ff'},
  {titulo:tx('Status'),texto:tx('Ícones sobre o retrato: efeitos bons ou ruins enquanto durarem.'),icone:HeartPulse,cor:'#c3a2ff'},
  {titulo:tx('Pontos'),texto:tx('Vença as 10 lutas. Terminar com mais Vida e mais gente de pé dá mais pontos.'),icone:Trophy,cor:'#ffd36b'},
] as const;

function Cena({i}:{i:number}){
  if(i===0)return <div className="demo-art demo-attack"><div className="demo-actor"><Portrait character={byId.goku}/><i/></div><span className="demo-travel">→</span><div className="demo-victim"><Portrait character={byId.vegeta}/><b>−66</b></div></div>;
  if(i===1)return <div className="demo-art demo-charge"><SkillIcon type={byId.goku.skills[0].icon} characterId="goku" skillId={byId.goku.skills[0].id} size={51}/><div><span>{t('CARGA DA HABILIDADE')}</span><i/><strong>{t('100% · PRONTA')}</strong></div></div>;
  if(i===2)return <div className="demo-art demo-prep"><div className="prep-portrait"><Portrait character={byId.goku}/><i/></div><div><strong>{t('PREPARANDO')}</strong><span>Kamehameha</span><small>{t('Pode ser interrompido')}</small></div></div>;
  if(i===3)return <div className="demo-art demo-shield"><Shield size={58}/><div><span>{t('ESCUDO')}</span><strong>{t('{n} bloqueado',{n:180})}</strong><i/></div></div>;
  if(i===4)return <div className="demo-art demo-status"><Portrait character={byId.vegeta}/><span>→</span><StatusBadge status={{id:'exposed',remaining:8,duration:8,intensity:.22,source:''}}/><strong>{t('EXPOSTO')}</strong></div>;
  // a escala de uma luta (src/engine/pontos.ts): o que o trio fez vale, até na derrota
  return <div className="cj-pontos"><span><b>{t('~10 mil')}</b><small>{t('derrota feia')}</small></span><span><b>{t('~100 mil')}</b><small>{t('vitória boa')}</small></span><span><b>{t('150 mil+')}</b><small>{t('luta incrível')}</small></span></div>;
}

/* Regras do jogo que não estão no glossário da ficha. */
const BASE:Termo[]=[
  {id:'trio',nome:tx('Trio'),cor:'#c8f560',rotulo:tx('COMEÇO'),texto:tx('Você escolhe 3 lutadores. Eles lutam sozinhos: seu trabalho é montar um trio que funcione junto.')},
  {id:'jornada',nome:tx('Jornada'),cor:'#ffd36b',rotulo:tx('OBJETIVO'),texto:tx('10 lutas seguidas. Cada luta soma pontos pelo que o trio fez: dano, nocautes, cura e proteção, habilidades, Status, ritmo, Carga e manter o trio vivo — com o peso certo para cada personagem, para todo estilo de jogo pontuar parecido. A vitória vale 25 mil a mais. Uma derrota encerra a jornada, mas os pontos dela ficam.')},
  {id:'vida',nome:tx('Vida'),cor:'#86e3a8',rotulo:tx('SOBREVIVER'),texto:tx('Quando chega a zero, o lutador sai da luta. A Vida que sobra no fim vale pontos.')},
  {id:'basico',nome:tx('Ataque básico'),cor:'#ff9a76',rotulo:tx('RITMO'),texto:tx('O golpe de sempre, com o nome e o jeito de cada lutador: uns quicam no segundo rival, uns pegam dois, uns curam o aliado, roubam Carga ou fecham um combo no 3º golpe. O círculo em volta do retrato mostra quanto falta para o próximo.')},
  {id:'vantagem',nome:tx('Vantagem'),cor:'#8fd3ff',rotulo:tx('QUEM DOMINA'),texto:tx('A barra do topo mostra quem está controlando a luta. Algumas habilidades reagem a ela; virar o jogo dá pontos.')},
  {id:'investigacao',nome:tx('Investigação'),cor:'#f4d47e',rotulo:tx('ESTUDAR O RIVAL'),texto:tx('Alguns lutadores estudam um rival por vez. Ao chegar a 100, abrem uma habilidade que só funciona contra quem foi estudado.')},
  {id:'inteligencia',nome:tx('Inteligência'),cor:'#c3a2ff',rotulo:tx('DECISÕES'),texto:tx('De 0 a 100: quanto melhor, mais o lutador escolhe o alvo e a hora certa sozinho.')},
];

export function HelpScreen({onPlay}:{onPlay:()=>void}){
  const [aba,setAba]=useState<'passos'|'regras'|'status'>('passos'),[passo,setPasso]=useState(0),[revisto,setRevisto]=useState(false);
  const mecanicas=[...BASE,...GLOSSARIO.filter(tm=>!(tm.id in statuses))];
  const doStatus=GLOSSARIO.filter(tm=>tm.id in statuses);
  const p=PASSOS[passo],ultimo=passo===PASSOS.length-1;
  return <section className="comojogar-v2">
    <TelaTopo icone={<CircleHelp/>} cor="#8fd3ff" rotulo={t('COMO JOGAR')} titulo={t('Aprenda em 1 minuto')}/>
    <div className="cj-abas" role="tablist">{([['passos',tx('Passo a passo')],['regras',tx('Regras')],['status',tx('Status')]] as const).map(([id,nome])=><button key={id} role="tab" aria-selected={aba===id} className={aba===id?'ativo':''} onClick={()=>setAba(id)}>{t(nome)}</button>)}</div>

    {aba==='passos'&&<div className="cj-passo" style={{'--cj':p.cor} as CSSProperties}>
      <div className="cj-cena" key={passo}><Cena i={passo}/></div>
      <div className="cj-texto" key={`t${passo}`}><span className="cj-num"><p.icone size={15}/>{passo+1} / {PASSOS.length}</span><h2>{t(p.titulo)}</h2><p>{t(p.texto)}</p></div>
      <div className="cj-pontinhos">{PASSOS.map((x,i)=><button key={x.titulo} aria-label={t('Passo {n}: {titulo}',{n:i+1,titulo:t(x.titulo)})} className={i===passo?'ativo':i<passo?'visto':''} onClick={()=>setPasso(i)}/>)}</div>
      <div className="cj-nav">
        <button className="secondary" disabled={passo===0} onClick={()=>setPasso(passo-1)} aria-label={t('Passo anterior')}><ArrowLeft size={18}/></button>
        {ultimo?<button className="primary gs-cta" onClick={onPlay}><Play size={18} fill="currentColor"/>{t('Montar meu trio')}</button>
          :<button className="primary cj-proximo" onClick={()=>setPasso(passo+1)}>{t('Próximo')}<ArrowRight size={18}/></button>}
      </div>
    </div>}

    {aba==='regras'&&<div className="cj-pecas">{mecanicas.map((tm,i)=><TermoBotao key={tm.id} termo={tm} className="cj-peca"><span style={{'--i':i} as CSSProperties}><b>{t(tm.nome)}</b><small>{t(tm.rotulo)}</small></span></TermoBotao>)}</div>}

    {aba==='status'&&<div className="cj-status">{(['positivo','negativo'] as const).map(tom=><div key={tom}>
      <h2 className={tom}>{tom==='positivo'?t('BONS · ajudam quem recebe'):t('RUINS · atrapalham quem recebe')}</h2>
      <div className="cj-status-grade">{doStatus.filter(tm=>statuses[tm.id as keyof typeof statuses].tone===tom).map(tm=><TermoBotao key={tm.id} termo={tm} className="cj-status-peca"><img src={`/assets/statuses/${tm.id}.png`} alt="" width={40} height={40}/><b>{t(tm.nome)}</b></TermoBotao>)}</div>
    </div>)}</div>}

    <div className="cj-rodape">
      <button className="secondary" onClick={()=>{try{localStorage.removeItem('nexus-battle-guide-v1');setRevisto(true);}catch{return}}}>{revisto?<Check size={16}/>:<Eye size={16}/>}{revisto?t('O guia volta na próxima luta'):t('Rever guia na próxima batalha')}</button>
      {!(aba==='passos'&&ultimo)&&<button className="primary gs-cta" onClick={onPlay}><Users size={17}/>{t('Montar meu trio')}</button>}
    </div>
  </section>;
}
