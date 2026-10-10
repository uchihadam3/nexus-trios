import { useLayoutEffect,useRef,useState,type CSSProperties,type ReactElement } from 'react';
import type { Battle } from '../engine/types';
import { ROTULO_DA_MECANICA,revelado,type Beat } from '../presentation/director';
import { PRESENTATION as P } from '../presentation/config';
import { byId } from '../data/characters';
import { SkillIcon } from './Icon';
import { ArrowDown,HeartPulse,ShieldCheck,Sparkles,Zap } from 'lucide-react';
import { statuses as statusCatalog } from '../data/statuses';
import { familia,folha,profileFor,type VfxFamily,type VfxProfile } from '../presentation/vfxProfiles';
import { RENASCER_PROPRIO } from '../presentation/renascer-proprio';
import { efeitosDoJeito,VOO_DO_QUIQUE } from '../presentation/jeito-efeito';
import { FAMILIA_DA_INVOCACAO } from '../presentation/vfx-atribuicao';

export interface Anchor {x:number;y:number}
export type Anchors=Record<string,Anchor>;
export function fallbackPoint(uid:string):Anchor{const [side,slot]=uid.split('-');return {x:17+Number(slot)*33,y:side==='enemy'?16:76};}
export function isAreaBeat(beat:Beat|null,battle:Battle):boolean {
  if(!beat||!['basic','skill'].includes(beat.event.kind))return false;
  const source=battle.fighters.find(f=>f.uid===beat.event.source);
  if(profileFor(source?.characterId??'',beat.event.skill)?.area)return true;
  // o que a mecânica faz depois do golpe (o quique, a cura do golpe, a guarda) não torna o golpe uma área
  const direct=beat.events.filter(e=>e.source===beat.event.source&&e.target&&e.target!==beat.event.source&&['damage','status','heal','shield'].includes(e.kind)&&!(e.label in ROTULO_DA_MECANICA));
  return new Set(direct.map(e=>e.target)).size>1;
}

/* Beats sem ficha de habilidade (interrupção) ganham uma família direta. */
const SEM_FICHA:Partial<Record<Beat['event']['kind'],VfxFamily>>={interrupt:'onda_de_choque',revive:'renascer',summon:'invocacao'};
/* Cada variante gira um pouco o impacto, para a mesma família não parecer carimbo. */
const GIRO_DA_VARIANTE=[0,16,-12,8];
/* Altura da faixa em relação ao medalhão. */
/* Os objetos arremessados (o escudo do Capitão, o batarangue…) voam grandes, para dar para ver o que é. */
const TAMANHO_DO_VOO:Record<string,number>={vermelho_bola:1.6,onda_choque_voo:1.9,laser_curto:1.7,portal_bala:1.9,teia_voando:2.0,teia_impacto_bola:2.1,burning_bola:2.3,kienzan_disco:2.4,saraivada:1.25,escudo_voando:2.6,batarangue_voando:2.5,batarangue_eletrico_voo:2.4,mjolnir_voando:2.4,laco_dourado_voo:2.4,bola_da_morte_voo:2.8,corvos_itachi_voo:2.4,repulsor_stark_voo:2.0,escudo_ricochete_voo:2.2,shuriken_voando:2.3,tiara_voando:2.5,dardo_voando:2.4,corvo_voando:2.6,reigun_bala:2.2,shotgun_rajada:2.2,barril_voando:2.4,fenix_voando:2.6,pedra_bloco:2.0,papel_bola:2.2,bola_do_charizard:2.4,buster_bala:2.2,raio_copiado:2.2,carga_maxima_bala:2.6,leao_dourado:2.6,bola_de_ar:2.4};
const ALTURA_DA_FAIXA:Record<string,number>={feixe:.36,feixe_pesado:.62,raio_faixa:.7,dreno:.42,dragao_faixa:.85,palma_faixa:.55,makanko_faixa:.5,chamas_faixa:.75,calor_faixa:.42,diamante_faixa:.6,aurora_faixa:.78,plasma_faixa:.7,feixe_ciclope:.6,unibeam_faixa:.8,raio_mortal_faixa:.25,kame_faixa_kuririn:.75,plano_b_faixa:.8,galick_faixa:.7,final_flash_faixa:1.0,trovao_faixa:.55};

const s=(x:number)=>`${x.toFixed(3)}s`;

/**
 * Os efeitos das famílias (adendo, parte 3), em até cinco camadas por ação:
 * preparo em quem age, o projétil que voa ou o feixe esticado até o alvo, e o
 * impacto em cada alvo atingido. Cada camada é uma folha neutra tingida com a
 * cor do efeito (máscara) e com o núcleo claro por cima; o navegador só
 * posiciona, gira e troca o quadro — transform, opacity e mask-position.
 */
export function BattleEffects({battle,beat,anchors,enabled,reduced,medal=80}:{battle:Battle;beat:Beat|null;anchors:Anchors;enabled:boolean;reduced:boolean;medal?:number}){
  const root=useRef<HTMLDivElement>(null),[size,setSize]=useState({w:0,h:0});
  useLayoutEffect(()=>{const element=root.current;if(!element)return;const observer=new ResizeObserver(([entry])=>setSize({w:entry.contentRect.width,h:entry.contentRect.height}));observer.observe(element);return ()=>observer.disconnect();},[]);
  const point=(uid:string)=>anchors[uid]??fallbackPoint(uid);
  const px=(a:Anchor)=>({x:a.x*size.w/100,y:a.y*size.h/100});
  const source=beat?battle.fighters.find(f=>f.uid===beat.event.source):null;
  const character=source?byId[source.characterId]:null;
  const kind=beat?.event.kind;
  const perfil:VfxProfile|undefined=beat&&(kind==='basic'||kind==='skill'||kind==='cast')?profileFor(source?.characterId??'',beat.event.skill):undefined;
  // quem renasce sozinho volta do jeito dele (a Fênix do Ikki, a gosma do Majin Boo, o cogumelo do Mario…)
  const volta=kind==='revive'&&beat?.event.source===beat?.event.target&&character?RENASCER_PROPRIO[character.id]?.volta:undefined;
  const chave:VfxFamily|undefined=perfil?.family??(kind==='summon'&&character?FAMILIA_DA_INVOCACAO[character.id]:undefined)??(volta as VfxFamily|undefined)??(kind?SEM_FICHA[kind]:undefined);
  const fam=chave?familia(chave):undefined;
  const cor=perfil?.color??character?.color??'#cfe6ff';
  const landed=beat?.impacted??false;
  const area=isAreaBeat(beat,battle);
  const D=beat?.duration??2,I=P.impactAt;
  const p1=beat?point(beat.event.source):{x:50,y:50};
  // o golpe vai até quem ele acerta: numa habilidade que bate no rival e cura o aliado (o Cólera do
  // Dragão), o dragão vai até o rival, mesmo que o alvo da habilidade seja o aliado
  const ladoDoAtor=beat?battle.fighters.find(f=>f.uid===beat.event.source)?.side:undefined;
  const golpeNoRival=beat?.events.find(e=>e.source===beat.event.source&&e.kind==='damage'&&!!e.target&&battle.fighters.find(f=>f.uid===e.target)?.side!==ladoDoAtor)?.target;
  const alvoPrincipal=beat?.event.target&&battle.fighters.find(f=>f.uid===beat.event.target)?.side!==ladoDoAtor?beat.event.target:golpeNoRival??beat?.event.target;
  const p2=alvoPrincipal?point(alvoPrincipal):p1;
  const a=px(p1),b=px(p2),dx=b.x-a.x,dy=b.y-a.y,dist=Math.hypot(dx,dy),ang=Math.atan2(dy,dx)*180/Math.PI;
  const intensidade=(perfil?.intensity??1)*(beat?.grand?1.22:1);
  const vai=!!beat&&!reduced&&kind!=='cast'&&!!alvoPrincipal&&alvoPrincipal!==beat.event.source&&!!perfil?.travel&&dist>medal*.6;

  /* Alvos que recebem impacto: quem levou dano, cura, Escudo ou Status deste beat (até três). */
  // a criatura invocada ataca os rivais; o Status de invocação em quem invocou não ganha a criatura em cima dele
  const criatura=!!chave&&chave.startsWith('inv_');
  const alvos=beat?[...new Set(beat.events.filter(e=>e.target&&['damage','status','interrupt','shield','heal','ko','block','revive','cleanse','dispel'].includes(e.kind)&&!(criatura&&e.target===beat.event.source&&e.kind==='status')).map(e=>e.target!))].slice(0,3):[];
  if(beat&&landed&&!alvos.length&&kind!=='turn'&&kind!=='cast')alvos.push(alvoPrincipal??beat.event.source);

  /*
   * Varredura (pedido do jogador: "a rajada do Ciclope tá saindo do lado, tinha que sair dele e cortar
   * os três"): o feixe sai de quem age, mira no primeiro rival e gira até o último; cada rival é
   * atingido quando o feixe passa por ele. O feixe passa de 22% a 62% da faixa (veja fx-varre).
   */
  const varredura=(()=>{
    if(!beat||!fam?.varre||!fam.faixa)return null;
    const lado=battle.fighters.find(f=>f.uid===beat.event.source)?.side;
    const rivais=alvos.filter(uid=>battle.fighters.find(f=>f.uid===uid)?.side!==lado);
    if(rivais.length<2)return null;
    const mira=rivais.map(uid=>{const q=px(point(uid)),vx=q.x-a.x,vy=q.y-a.y;return{uid,ang:Math.atan2(vy,vx)*180/Math.PI,dist:Math.hypot(vx,vy)};}).sort((m,n)=>m.ang-n.ang);
    const de=mira[0].ang,ate=mira[mira.length-1].ang,abre=Math.max(1e-3,ate-de);
    const passa:Record<string,number>={};
    for(const m of mira)passa[m.uid]=Math.max(0,D*I*.55+D*.78*(.22+.4*(m.ang-de)/abre)-D*I);
    return{de,ate,largura:Math.max(...mira.map(m=>m.dist))+medal*.25,passa};
  })();
  /*
   * Encadeia: o golpe sai de quem age até o primeiro rival e quica para o próximo e para o próximo;
   * cada rival é atingido quando o golpe chega nele. Com `viagem` é um tiro curto que voa e quica
   * (o Ricochete do Ciclope — pedido do jogador: "sai um laser curto bem no personagem do meio e
   * fica ricocheteando nos personagens"); com `faixa`, cada trecho é um feixe que acende na sua vez.
   */
  const cadeia=(()=>{
    if(!beat||!fam?.encadeia||!(fam.faixa||fam.viagem))return null;
    const lado=battle.fighters.find(f=>f.uid===beat.event.source)?.side;
    const rivais=alvos.filter(uid=>battle.fighters.find(f=>f.uid===uid)?.side!==lado);
    if(rivais.length<2)return null;
    // o primeiro é o do meio da fileira (na tela); depois quica no mais perto e no outro
    const porX=[...rivais].sort((m,n)=>px(point(m)).x-px(point(n)).x);
    const primeiro=porX[Math.floor((porX.length-1)/2)];
    const ordem=[primeiro],resto=rivais.filter(u=>u!==primeiro);
    while(resto.length){const ult=px(point(ordem[ordem.length-1]));resto.sort((m,n)=>{const qm=px(point(m)),qn=px(point(n));return Math.hypot(qm.x-ult.x,qm.y-ult.y)-Math.hypot(qn.x-ult.x,qn.y-ult.y);});ordem.push(resto.shift()!);}
    const voa=!!fam.viagem;
    // tiro: o primeiro voo chega no impacto; cada quique depois leva `passo`
    const trecho=voa?D*.13:D*.42,passo=D*.13,inicio=voa?D*I*.35:D*I*.55,primeiroVoo=D*I*.65;
    const passa:Record<string,number>={};
    const trechos=ordem.map((uid,k)=>{
      const de=k===0?p1:point(ordem[k-1]),qa=px(de),qb=px(point(uid)),vx=qb.x-qa.x,vy=qb.y-qa.y;
      const atraso=voa?(k===0?inicio:inicio+primeiroVoo+(k-1)*passo):inicio+k*passo;
      const dura=voa?(k===0?primeiroVoo:trecho):trecho;
      passa[uid]=Math.max(0,voa?atraso+dura-D*I:atraso+trecho*.22-D*I);
      return{uid,de,vx,vy,largura:Math.hypot(vx,vy),ang:Math.atan2(vy,vx)*180/Math.PI,atraso,dura};
    });
    return{trechos,trecho,passa};
  })();

  const camada=(nome:string,estilo:Record<string,string|number>,classe:string,key:string)=><span key={key} className={`fxl ${classe}`} style={{'--fx-img':`url(${folha(nome)})`,...estilo} as CSSProperties}/>;
  const nodes:ReactElement[]=[];
  if(enabled&&beat&&fam&&kind!=='turn'&&size.w>0){
    const id=beat.event.id;
    // preparo: a folha da família em laço sobre quem prepara
    if(kind==='cast'&&!landed&&fam.preparo){
      const t=medal*1.9*intensidade;
      nodes.push(camada(fam.preparo,{left:`${p1.x}%`,top:`${p1.y}%`,width:t,height:t},'fxl-laco',`prep-${id}`));
    }
    // viagem: o projétil sai depois da preparação do golpe e chega no impacto
    // ergue: antes do objeto sair, ele se forma em cima de quem age (o Kienzan na mão erguida)
    if(vai&&!landed&&fam.ergue){
      const t=medal*1.9*intensidade;
      nodes.push(camada(fam.ergue,{left:`${p1.x}%`,top:`calc(${p1.y}% - ${Math.round(medal*.45)}px)`,width:t,height:t,'--fx-cor':cor,'--ang':'0deg','--flip':1,'--dur':s(D*I*.4),'--delay':'0s'},'fxl-impacto fxl-sobre',`ergue-${id}`));
    }
    if(vai&&fam.viagem&&cadeia){
      const t=medal*(TAMANHO_DO_VOO[fam.viagem]??1.05)*Math.min(1.25,intensidade);
      for(const v of cadeia.trechos)nodes.push(camada(fam.viagem,{left:`${v.de.x}%`,top:`${v.de.y}%`,width:t,height:t,'--dx':`${v.vx}px`,'--dy':`${v.vy}px`,'--ang':`${v.ang}deg`,'--voo':s(v.dura),'--voo-delay':s(v.atraso)},'fxl-laco fxl-voo fxl-quica',`voo-${id}-${v.uid}`));
    }else if(vai&&!landed&&fam.viagem){
      const t=medal*(TAMANHO_DO_VOO[fam.viagem]??1.05)*Math.min(1.25,intensidade);
      nodes.push(camada(fam.viagem,{left:`${p1.x}%`,top:`${p1.y}%`,width:t,height:t,'--dx':`${dx}px`,'--dy':`${dy}px`,'--ang':`${ang}deg`,'--voo':s(D*I*.65),'--voo-delay':s(D*I*.35)},'fxl-laco fxl-voo',`voo-${id}`));
    }
    // atravessa: o corpo inteiro (o dragão do Shiryu) sai de quem age, anda até o alvo, entra nele e
    // some lá dentro — a cabeça chega no alvo no momento do impacto
    if(vai&&fam.atravessa){
      const h=medal*(ALTURA_DA_FAIXA[fam.atravessa]??.6)*Math.min(1.3,intensidade);
      const largura=dist+medal*.35,corpo=Math.min(dist*.85,h*4.6);
      const t0=D*I*.2,ate=Math.max(.15,D*I-t0),v=dist/ate,anda=(largura+corpo)/v;
      nodes.push(<span key={`atravessa-${id}`} className="fxl-trilho" style={{left:`${p1.x}%`,top:`${p1.y}%`,width:largura,height:h,'--ang':`${ang}deg`,'--some':`${Math.round(medal*.75)}px`} as CSSProperties}>
        <span className="fxl fxl-laco fxl-atravessa" style={{'--fx-img':`url(${folha(fam.atravessa)})`,'--corpo':`${corpo}px`,'--percurso':`${largura+corpo}px`,'--anda':s(anda),'--anda-delay':s(t0)} as CSSProperties}/>
      </span>);
    }
    // faixa: o feixe cresce de quem age até o alvo, segura o impacto e some
    if(vai&&fam.faixa&&!fam.viagem&&cadeia){
      const h=medal*(ALTURA_DA_FAIXA[fam.faixa]??.4)*Math.min(1.3,intensidade);
      for(const t of cadeia.trechos)nodes.push(camada(fam.faixa,{left:`${t.de.x}%`,top:`${t.de.y}%`,width:t.largura,height:h,'--ang':`${t.ang}deg`,'--faixa':s(cadeia.trecho),'--faixa-delay':s(t.atraso)},'fxl-laco fxl-faixa',`faixa-${id}-${t.uid}`));
    }else if(vai&&fam.faixa&&varredura){
      const h=medal*(ALTURA_DA_FAIXA[fam.faixa]??.4)*Math.min(1.3,intensidade);
      nodes.push(camada(fam.faixa,{left:`${p1.x}%`,top:`${p1.y}%`,width:varredura.largura,height:h,'--ang0':`${varredura.de}deg`,'--ang1':`${varredura.ate}deg`,'--faixa':s(D*.78),'--faixa-delay':s(D*I*.55)},'fxl-laco fxl-faixa fxl-varre',`faixa-${id}`));
    }else if(vai&&fam.faixa){
      const h=medal*(ALTURA_DA_FAIXA[fam.faixa]??.4)*Math.min(1.3,intensidade);
      nodes.push(camada(fam.faixa,{left:`${p1.x}%`,top:`${p1.y}%`,width:dist,height:h,'--ang':`${ang}deg`,'--faixa':s(D*.78),'--faixa-delay':s(D*I*.55)},'fxl-laco fxl-faixa',`faixa-${id}`));
    }
    // impacto: em cada alvo, depois do contato
    if(landed){
      const dur=reduced?.35:Math.max(.42,D*(1-I)*fam.tempo);
      const giroBase=(fam.giro??0)+GIRO_DA_VARIANTE[perfil?.variant??0];
      // efeitos que contam a mecânica por cima da família do golpe: quem foi levantado por um
      // aliado (a do renascer já é o próprio beat) e quem foi Provocado
      const sobre=(alvo:string,nome:VfxFamily,chaveDoNo:string,atraso:number)=>{
        const p=point(alvo),f=familia(nome),t=Math.min(medal*f.escala,Math.min(size.w,size.h)*.92);
        nodes.push(camada(f.impacto,{left:`${p.x}%`,top:`${p.y}%`,width:t,height:t,'--fx-cor':f.cor,'--ang':'0deg','--flip':1,'--dur':s(Math.max(.6,dur*1.1)),'--delay':s(atraso)},`fxl-impacto fxl-sobre ${reduced?'fxl-parado':''}`,chaveDoNo));
      };
      // um golpe que ataca o rival e também cura ou reforça alguém do próprio trio (o soco da Sakura
      // que cura, o golpe do Gohan que fortalece ele mesmo): o aliado ganha o efeito do que recebeu,
      // nunca o desenho do ataque — senão parece que ele também apanhou
      const ladoDe=(uid?:string)=>battle.fighters.find(f=>f.uid===uid)?.side;
      const lado=ladoDe(beat.event.source);
      const ataca=beat.events.some(e=>e.source===beat.event.source&&e.kind==='damage'&&!!e.target&&ladoDe(e.target)!==lado);
      const apoioPara=(uid:string):VfxFamily|null=>{
        const meus=beat.events.filter(e=>e.target===uid&&e.source===beat.event.source&&revelado(beat,e)&&!(e.label in ROTULO_DA_MECANICA)&&e.label!=='Guarda do golpe');
        return meus.some(e=>e.kind==='heal')?'cura':meus.some(e=>e.kind==='shield')?'escudo':meus.some(e=>e.kind==='status')?'reforco':null;
      };
      // o meteoro que cai no meio: numa área, uma folha só, grande, no centro dos rivais atingidos
      const rivais=alvos.filter(uid=>ladoDe(uid)!==lado);
      const noCentro=!!fam.noCentro&&rivais.length>1;
      if(noCentro){
        const pts=rivais.map(point),cx=pts.reduce((a,p)=>a+p.x,0)/pts.length,cy=pts.reduce((a,p)=>a+p.y,0)/pts.length;
        const t=Math.min(medal*(perfil?.scale??fam.escala)*1.9*(beat.grand?1.1:1),Math.min(size.w,size.h)*.98);
        nodes.push(camada(fam.impacto,{left:`${cx}%`,top:`${cy}%`,width:t,height:t,'--ang':'0deg','--flip':1,'--dur':s(dur*1.15)},`fxl-impacto ${reduced?'fxl-parado':''}`,`centro-${id}`));
      }
      // o que aparece em quem age quando o golpe sai (o Susanoo em volta do Madara)
      if(fam.noAtor){
        const t=Math.min(medal*2.3,Math.min(size.w,size.h)*.8);
        nodes.push(camada(fam.noAtor,{left:`${p1.x}%`,top:`${p1.y}%`,width:t,height:t,'--fx-cor':cor,'--ang':'0deg','--flip':1,'--dur':s(Math.max(.8,dur*1.3))},`fxl-impacto fxl-sobre ${reduced?'fxl-parado':''}`,`ator-${id}`));
      }
      /*
       * O ricochete é um objeto só (pedido do jogador: "o escudo do Capitão tá virando dois escudos…
       * tem que bater em um e depois ricochetear e bater no outro"): quem só levou o quique não ganha o
       * impacto junto com o primeiro; quando o passo do Ricochete chega, o objeto voa do primeiro alvo
       * até ele e bate lá.
       */
      const doQuique=new Set(beat.events.filter(e=>e.kind==='damage'&&e.label==='Ricochete'&&!!e.target).map(e=>e.target!));
      const soQuique=new Set([...doQuique].filter(uid=>!beat.events.some(e=>e.target===uid&&e.kind==='damage'&&e.label!=='Ricochete'&&e.source===beat.event.source)));
      for(const e of beat.events)if(e.kind==='damage'&&e.label==='Ricochete'&&e.target&&soQuique.has(e.target)&&revelado(beat,e)&&alvoPrincipal&&!reduced){
        const de=point(alvoPrincipal),para=point(e.target),qa=px(de),qb=px(para);
        const vx=qb.x-qa.x,vy=qb.y-qa.y,ang2=Math.atan2(vy,vx)*180/Math.PI;
        if(fam.viagem){
          const tv=medal*(TAMANHO_DO_VOO[fam.viagem]??1.05)*Math.min(1.25,intensidade);
          nodes.push(camada(fam.viagem,{left:`${de.x}%`,top:`${de.y}%`,width:tv,height:tv,'--dx':`${vx}px`,'--dy':`${vy}px`,'--ang':`${ang2}deg`,'--voo':s(VOO_DO_QUIQUE),'--voo-delay':s(0)},'fxl-laco fxl-voo',`quique-voo-${id}-${e.id}`));
        }
        const t=Math.min(medal*(perfil?.scale??fam.escala),Math.min(size.w,size.h)*.92);
        const pula=fam.viagem&&fam.pula?fam.pula:0,durDaFolha=dur/(1-pula);
        nodes.push(camada(fam.impacto,{left:`${para.x}%`,top:`${para.y}%`,width:t,height:t,'--ang':`${fam.aponta?ang2:0}deg`,'--flip':1,'--dur':s(durDaFolha),'--delay':s(VOO_DO_QUIQUE-pula*durDaFolha)},`fxl-impacto`,`quique-imp-${id}-${e.id}`));
      }
      alvos.forEach((uid,i)=>{
        if(noCentro&&rivais.includes(uid))return;
        if(soQuique.has(uid))return;
        if(ataca&&ladoDe(uid)===lado){
          // a família tem o desenho próprio do que ela faz no trio (a muralha da Toph na frente de cada aliado)
          if(fam.noAliado){
            const p=point(uid),t=Math.min(medal*fam.escala,Math.min(size.w,size.h)*.92);
            nodes.push(camada(fam.noAliado,{left:`${p.x}%`,top:`${p.y}%`,width:t,height:t,'--fx-cor':cor,'--ang':'0deg','--flip':1,'--dur':s(Math.max(.6,dur*1.1)),'--delay':s(.12+i*.06)},`fxl-impacto fxl-sobre ${reduced?'fxl-parado':''}`,`aliado-${id}-${uid}`));
            return;
          }
          const apoio=apoioPara(uid);
          if(apoio)sobre(uid,apoio,`apoio-${id}-${uid}`,.12);
          return;
        }
        const p=point(uid),q=px(p),vx=q.x-a.x,vy=q.y-a.y;
        const direcao=Math.atan2(vy,vx)*180/Math.PI;
        const espelho=!fam.aponta&&vx<-1?-1:1;
        const giro=fam.aponta?direcao:giroBase*espelho;
        const t=Math.min(medal*(perfil?.scale??fam.escala)*(beat.grand?1.25:1)*(area&&i>0?.9:1),Math.min(size.w,size.h)*.92);
        // o clarão do contato vem por baixo, no alvo principal
        if(fam.acento&&i===0&&!reduced)nodes.push(camada(fam.acento,{left:`${p.x}%`,top:`${p.y}%`,width:t*.62,height:t*.62,'--ang':`${direcao}deg`,'--dur':s(Math.max(.35,dur*.6))},'fxl-impacto fxl-acento',`ac-${id}-${uid}`));
        // o objeto já voou até aqui: pula o começo da folha, que mostrava ele chegando
        const pula=vai&&fam.pula?fam.pula:0,durDaFolha=dur/(1-pula);
        nodes.push(camada(fam.impacto,{left:`${p.x}%`,top:`${p.y}%`,width:t,height:t,'--ang':`${giro}deg`,'--flip':espelho,'--dur':s(durDaFolha),'--delay':s(((varredura??cadeia)?.passa[uid]??(area?i*.07:0))-pula*durDaFolha)},`fxl-impacto ${reduced?'fxl-parado':''}`,`imp-${id}-${uid}`));
      });
      // cada uma aparece no passo da cadeia em que acontece (a reação depois do golpe)
      for(const e of beat.events){
        if(!revelado(beat,e))continue;
        if(e.kind==='revive'&&e.target&&e.source!==e.target)sobre(e.target,'ressurreicao',`rev-${id}-${e.target}`,.12);
        if(e.kind==='cleanse'&&e.target)sobre(e.target,'purificacao',`pur-${id}-${e.id}`,.06);
        if(e.kind==='dispel'&&e.target)sobre(e.target,'dissipar',`dis-${id}-${e.id}`,.06);
        // os Status da parte 5 ganham o efeito deles ao entrar
        const DO_STATUS:Partial<Record<string,VfxFamily>>={poison:'acido',bleed:'sangue',cursed:'maldicao',frozen:'bloco_de_gelo',sleep:'sono',blind:'cegueira',barrier:'barreira_magica'};
        if(e.kind==='status'&&e.status&&DO_STATUS[e.status]&&e.target)sobre(e.target,DO_STATUS[e.status]!,`st-${id}-${e.id}`,.06);
        if(e.kind==='resist'&&e.target)sobre(e.target,e.label==='Última resistência'?'ultima_resistencia':'barreira_magica',`res-${id}-${e.id}`,0);
        if(e.kind==='copy')sobre(e.source,'copia',`cop-${id}-${e.id}`,0);
        if(e.kind==='damage'&&e.label==='Explosão'&&e.target)sobre(e.target,'explosao',`bum-${id}-${e.id}`,0);
        if(e.kind==='miss'&&e.label==='Esquivou'&&e.target)sobre(e.target,'esquiva',`esq-${id}-${e.id}`,0);
        if(e.kind==='status'&&e.status==='provoked'&&e.target)sobre(e.target,'provocar',`prov-${id}-${e.target}`,.08);
        // o golpe devolvido: o espelho ou os espinhos aparecem em quem devolveu
        if(e.kind==='damage'&&e.label==='Refletido')sobre(e.source,'reflexo',`refl-${id}-${e.id}`,0);
        if(e.kind==='damage'&&e.label==='Espinhos')sobre(e.source,'espinhos',`esp-${id}-${e.id}`,0);
        if(e.kind==='heal'&&(e.label==='Vampirismo'||e.label==='Roubo de vida')&&e.target)sobre(e.target,'vampirismo',`vamp-${id}-${e.id}`,.1);
      }
      // os jeitos de bater: o quique, a varrida, o fim da série, a cura, a Carga roubada, a guarda e o relógio
      for(const x of efeitosDoJeito(beat.event,beat.events,beat.after.fighters))if(x.evento===beat.event||revelado(beat,x.evento))sobre(x.alvo,x.familia,`jeito-${id}-${x.familia}-${x.evento.id}`,x.atraso);
    }
  }

  const outcomes=(beat?.impacted?beat.events:[]).filter(e=>e.target===beat?.event.target&&['damage','status','interrupt','shield','block','heal'].includes(e.kind)).slice(0,3);
  const outcome=(event:typeof outcomes[number])=>event.kind==='damage'?{label:'Dano',icon:Zap}:event.kind==='interrupt'?{label:'Interrompido',icon:ArrowDown}:event.kind==='status'?{label:event.status?statusCatalog[event.status].name:'Efeito',icon:Sparkles}:event.kind==='heal'?{label:'Recuperação',icon:HeartPulse}:{label:'Protegido',icon:ShieldCheck};
  const style={'--fx-cor':cor,'--fx-color':character?.color??'#d2f276'} as CSSProperties;
  return <div ref={root} className={`battle-effects directed-effects ${beat?.grand?'grand-event':''} ${reduced?'reduced':''}`} aria-hidden="true" style={style} data-familia={chave}>
    {nodes}
    {beat&&!beat.periodic&&beat.event.kind==='turn'&&<div className={`action-title ${landed?'landed':''} ${beat.grand?'title-grand':''}`} key={beat.event.id}><SkillIcon type={beat.event.visual??'impact'} size={20} characterId={source?.characterId} skillId={source&&beat.event.skill!==undefined?character?.skills[beat.event.skill]?.id:undefined}/><div><small>{beat.event.kind==='turn'?(beat.event.source.startsWith('player')?'SEU TRIO':'RIVAIS'):character?.name??'NEXUS'}</small><strong>{beat.event.kind==='turn'?'VIRADA!':beat.event.label}</strong>{outcomes.length>0&&<span className="action-outcomes">{outcomes.slice(0,2).map(e=>{const x=outcome(e),Icon=x.icon;return <i key={e.id}><Icon size={12}/>{x.label}</i>;})}</span>}</div></div>}
  </div>;
}
