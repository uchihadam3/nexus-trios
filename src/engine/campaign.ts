import { characters, byId } from '../data/characters';
import { random, shuffle } from './random';
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { LIGACOES, ligacoesDoTrio } from './sinergia';
export interface Encounter {team:string[];name:string;power:number;scale:number}
export interface Draft {team:string[];candidates:string[];skips:number;rng:number;banned?:string[]}
export function candidates(draft:Draft,exclude:string[]=[]):string[]{return shuffle(characters.filter(c=>!draft.team.includes(c.id)&&!draft.banned?.includes(c.id)&&!exclude.includes(c.id)).map(c=>c.id),draft).slice(0,3);}
/*
 * O sorteio dos candidatos avança o estado do draft (`rng`). Antes, o
 * `{...d, candidates: candidates(d)}` copiava o estado *antes* do sorteio, e
 * a primeira troca sorteava de novo a partir da mesma semente: a segunda tela
 * saía amarrada à primeira, e alguns personagens apareciam bem menos (Goku
 * −13% em 200 mil jornadas). tests/sorteio.test.ts confere que todos têm a
 * mesma chance.
 */
export function newDraft(seed:number,banned:string[]=[]):Draft{const d:Draft={team:[],candidates:[],skips:3,rng:seed>>>0,banned};d.candidates=candidates(d);return d;}
export function skipDraft(d:Draft):Draft{if(d.skips<=0)return d;const next={...d,skips:d.skips-1};next.candidates=candidates(next,d.candidates);return next;}
export function pickDraft(d:Draft,id:string):Draft{if(d.team.length>=3||!d.candidates.includes(id)||d.team.includes(id))return d;const next={...d,team:[...d.team,id]};next.candidates=next.team.length<3?candidates(next):[];return next;}
/*
 * A campanha: 10 lutas, 30 rivais diferentes, cada luta mais difícil e mais
 * entrosada que a anterior (pedido do jogador: "começando ~70% de chance de
 * vencer e chegando a ~15% na última; sem trio fixo no final — tem que ser o
 * trio mais forte daquela rodada; e a cada luta os rivais têm mais sinergia").
 *
 * A força de um trio é medida, não chutada: a força de cada personagem e o
 * peso de cada ligação de sinergia (src/engine/sinergia.ts) vêm de lutas
 * simuladas (scripts/medir-forca.ts → src/data/forca-dos-rivais.ts).
 *
 * Detalhes da calibração logo abaixo, em TRIOS_DA_LUTA.
 */
export function sinergiaDoTrio(team:readonly string[]):number{const l=ligacoesDoTrio(team);return LIGACOES.reduce((n,k)=>n+l[k]*(PESO_DA_LIGACAO[k]??0),0);}
export function forcaDoTrio(team:readonly string[]):number{return team.reduce((n,id)=>n+(FORCA[id]??0),0)+sinergiaDoTrio(team);}
/*
 * A dificuldade é calibrada para quem escolhe bem (pedidos do jogador: a curva
 * vale para quem escolhe bem; ~10% das jornadas bem jogadas terminam com as 10
 * vitórias; e escolher bem tem que pesar). O "jogador bom" de referência escolhe no draft o
 * candidato mais forte que combina com o trio e usa as trocas quando os
 * candidatos são fracos (scripts/calibrar-dificuldade.ts).
 *
 * Cada luta sorteia TRIOS_DA_LUTA[i] trios com os personagens que sobraram e
 * pega o mais forte entre os que não têm menos sinergia que o da luta
 * anterior: quanto mais trios sorteados, mais forte o rival. O chefe é o mais
 * forte entre DIFICULDADE.triosDoChefe trios — nunca um trio fixo. ESCALAS é
 * a Vida dos rivais (×), que só sobe quando o trio mais forte não basta.
 */
export const TRIOS_DA_LUTA=[1,1,1,1,1,1,1,2,3];
export const DIFICULDADE={triosDoChefe:400};
/** Sinergia máxima do rival da luta i: SINERGIA_MAXIMA × (i+1)/10 (o chefe não tem teto). */
export const SINERGIA_MAXIMA=0.4;
export const ESCALAS=[.82,.84,.86,.86,.9,.93,.97,.98,1,1];
const names=['Primeiro encontro','Novos rivais','O ritmo aumenta','Entre universos','Ponto de ruptura','Pressão crescente','Sem recuar','A última barreira','À altura das lendas','O confronto final'];
const chave=(t:readonly string[])=>[...t].sort().join('|');
/* `count` trios diferentes sorteados de `ids` (três índices ao acaso; rápido mesmo para milhares de trios). */
function sampledTeams(ids:string[],rng:{rng:number},count:number):string[][]{
  const found=new Map<string,string[]>(),n=ids.length;
  if(n<3)return [];
  for(let i=0;i<count*5&&found.size<count;i++){
    const a=Math.floor(random(rng)*n),b=Math.floor(random(rng)*n),c=Math.floor(random(rng)*n);
    if(a===b||a===c||b===c)continue;
    const team=[ids[a]!,ids[b]!,ids[c]!],k=chave(team);
    if(!found.has(k))found.set(k,team);
  }
  return [...found.values()];
}
type Candidato={team:string[];forca:number;sinergia:number};
const avalia=(team:string[]):Candidato=>({team,forca:forcaDoTrio(team),sinergia:sinergiaDoTrio(team)});
/*
 * O rival de uma luta: o mais forte entre `quantos` trios sorteados que não
 * têm menos sinergia que o anterior. Se nenhum dos sorteados é tão entrosado,
 * sorteia mais antes de desistir (e aí fica com o mais entrosado).
 */
function rival(sobra:string[],rng:{rng:number},quantos:number,sinergiaMinima:number,teto:number):Candidato{
  const lista=sampledTeams(sobra,rng,quantos).map(avalia);
  if(!lista.length)throw new Error('Elenco insuficiente para montar um rival sem repetição.');
  // entre a sinergia da luta anterior e o teto desta luta (o teto sobe a cada luta: a sinergia cresce aos poucos e não acaba antes do chefe)
  const naFaixa=(x:Candidato)=>x.sinergia>=sinergiaMinima-1e-9&&x.sinergia<=Math.max(teto,sinergiaMinima)+1e-9;
  let ok=lista.filter(naFaixa);
  if(!ok.length)ok=sampledTeams(sobra,rng,Math.max(400,quantos*6)).map(avalia).filter(naFaixa).slice(0,quantos);
  // nenhum tão entrosado quanto o anterior: sorteia mais e fica com os que sobem menos (a sinergia sobe aos poucos e sobra entrosamento para as próximas lutas)
  if(!ok.length)ok=sampledTeams(sobra,rng,Math.max(400,quantos*6)).map(avalia).filter(x=>x.sinergia>=sinergiaMinima-1e-9).sort((a,b)=>a.sinergia-b.sinergia).slice(0,quantos);
  return ok.length?ok.reduce((a,b)=>b.forca>a.forca?b:a):lista.reduce((a,b)=>b.sinergia>a.sinergia||b.sinergia===a.sinergia&&b.forca>a.forca?b:a);
}
export function generateCampaign(seed:number,playerTeam:string[]=[]):Encounter[]{
  const uniquePlayer=[...new Set(playerTeam)];
  if(uniquePlayer.length!==playerTeam.length||playerTeam.some(id=>!byId[id]))throw new Error('O trio do jogador contém IDs repetidos ou inválidos.');
  if(playerTeam.length!==0&&playerTeam.length!==3)throw new Error('A campanha só pode ser gerada após a escolha de exatamente três personagens.');
  const eligible=characters.map(c=>c.id).filter(id=>!uniquePlayer.includes(id));
  if(eligible.length<30)throw new Error('Elenco insuficiente: são necessários três personagens do jogador e trinta inimigos únicos.');
  const rng={rng:seed>>>0};
  const used=new Set(uniquePlayer);
  const encounters:Encounter[]=[];
  let sinergiaAnterior=-Infinity;
  for(let i=0;i<10;i++){
    const escolhido=rival(eligible.filter(id=>!used.has(id)),rng,i<9?TRIOS_DA_LUTA[i]!:DIFICULDADE.triosDoChefe,sinergiaAnterior,i<9?SINERGIA_MAXIMA*(i+1)/10:Infinity);
    sinergiaAnterior=escolhido.sinergia;
    const team=[...escolhido.team];
    encounters.push({team,name:names[i]!,power:Math.round(escolhido.forca*100)/100,scale:ESCALAS[i]!});
    team.forEach(id=>used.add(id));
  }
  if(uniquePlayer.length===3){
    const result=validateCampaignUniqueness({team:uniquePlayer,encounters});
    if(!result.valid)throw new Error(`Campanha gerada com violações: ${result.errors.join('; ')}`);
  }else if(new Set(encounters.flatMap(encounter=>encounter.team)).size!==30)throw new Error('Campanha provisória gerada com personagens repetidos.');
  return encounters;
}
export function validateCampaignUniqueness(run:{team:string[];encounters:Encounter[]}):{valid:boolean;errors:string[]}{
  const errors:string[]=[];
  if(run.team.length!==3||new Set(run.team).size!==3||run.team.some(id=>!byId[id]))errors.push('O trio do jogador precisa conter três personagens válidos e distintos.');
  if(run.encounters.length!==10)errors.push('A campanha precisa conter dez encontros.');
  const used=new Set<string>(),enemyIds:string[]=[];
  run.encounters.forEach((encounter,index)=>{
    if(encounter.team.length!==3||new Set(encounter.team).size!==3)errors.push(`Encontro ${index+1}: trio inválido ou com IDs repetidos.`);
    for(const id of encounter.team){
      if(!byId[id])errors.push(`Encontro ${index+1}: personagem desconhecido (${id}).`);
      if(run.team.includes(id))errors.push(`Encontro ${index+1}: personagem do jogador usado como inimigo (${id}).`);
      if(used.has(id))errors.push(`Encontro ${index+1}: personagem inimigo repetido na jornada (${id}).`);
      used.add(id);enemyIds.push(id);
    }
  });
  if(run.encounters.length===10&&enemyIds.length!==30)errors.push('A campanha completa precisa ter trinta inimigos.');
  if(run.encounters.length===10&&new Set(enemyIds).size!==30)errors.push('Os trinta inimigos precisam ser únicos.');
  return {valid:errors.length===0,errors};
}
