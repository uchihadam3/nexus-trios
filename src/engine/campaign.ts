import { characters, byId } from '../data/characters';
import { shuffle } from './random';
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { LIGACOES, ligacoesDoTrio } from './sinergia';
export interface Encounter {team:string[];name:string;power:number;scale:number}
export interface Draft {team:string[];candidates:string[];skips:number;rng:number;banned?:string[]}
export function candidates(draft:Draft,exclude:string[]=[]):string[]{return shuffle(characters.filter(c=>!draft.team.includes(c.id)&&!draft.banned?.includes(c.id)&&!exclude.includes(c.id)).map(c=>c.id),draft).slice(0,3);}
export function newDraft(seed:number,banned:string[]=[]):Draft{const d={team:[],candidates:[],skips:3,rng:seed>>>0,banned};return {...d,candidates:candidates(d)};}
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
 * Cada jornada sorteia uma rodada de personagens (DIFICULDADE.rodada) e,
 * dentro dela, dezenas de trios. O chefe da luta 10 é o mais forte desses
 * trios — muda a cada jornada, porque a rodada muda. As lutas 1 a 9 sobem de força e de sinergia
 * a cada luta, e a Vida extra dos rivais (ESCALAS) fecha a curva: a chance de
 * vencer cada luta foi calibrada em lutas simuladas (scripts/calibrar-dificuldade.ts).
 */
export function sinergiaDoTrio(team:readonly string[]):number{const l=ligacoesDoTrio(team);return LIGACOES.reduce((n,k)=>n+l[k]*(PESO_DA_LIGACAO[k]??0),0);}
export function forcaDoTrio(team:readonly string[]):number{return team.reduce((n,id)=>n+(FORCA[id]??0),0)+sinergiaDoTrio(team);}
/** Vida dos rivais em cada luta (×): sobe devagar; quem faz a dificuldade é a força do trio escolhido. */
export const ESCALAS=[.9,.92,.94,.96,.98,1,1.02,1.04,1.06,1.08];
/*
 * Quão forte é o trio das lutas 1 a 9, como posição entre os trios possíveis
 * da rodada (0 = o mais fraco, 1 = o mais forte), e quantos trios são
 * sorteados para achar o chefe (o mais forte entre mais trios é mais forte). Calibrados por scripts/calibrar-dificuldade.ts para a chance de
 * vencer seguir ~70%, 64%, 58% … 21% e ~12% no chefe (o jogador aceitou até 10%).
 */
export const FORCA_DA_LUTA=[.32,.39,.47,.53,.61,.63,.69,.79,.85];
export const DIFICULDADE={rodada:72,triosDoChefe:13};
const names=['Primeiro encontro','Novos rivais','O ritmo aumenta','Entre universos','Ponto de ruptura','Pressão crescente','Sem recuar','A última barreira','À altura das lendas','O confronto final'];
const CANDIDATOS=100;
const chave=(t:readonly string[])=>[...t].sort().join('|');
function sampledTeams(ids:string[],rng:{rng:number},count:number):string[][]{
  const found=new Map<string,string[]>();
  for(let i=0;i<count*5&&found.size<count;i++){const team=shuffle(ids,rng).slice(0,3);if(team.length===3&&!found.has(chave(team)))found.set(chave(team),team);}
  return [...found.values()];
}
/*
 * O chefe: entre os trios sorteados com quem sobrou da rodada e entrosados
 * pelo menos como o da luta 9, o mais forte. Quanto mais trios sorteados,
 * mais forte ele sai.
 */
function trioMaisForte(sobra:string[],rng:{rng:number},sinergiaMinima:number):string[]{
  const todos=sampledTeams(sobra,rng,DIFICULDADE.triosDoChefe*20).map(team=>({team,forca:forcaDoTrio(team),sinergia:sinergiaDoTrio(team)}));
  const entrosados=todos.filter(x=>x.sinergia>=sinergiaMinima-1e-9);
  const lista=(entrosados.length?entrosados:todos).slice(0,DIFICULDADE.triosDoChefe);
  return lista.reduce((a,b)=>b.forca>a.forca?b:a).team;
}
const quantil=(xs:number[],x:number)=>xs.filter(v=>v<x).length/Math.max(1,xs.length-1);
export function generateCampaign(seed:number,playerTeam:string[]=[]):Encounter[]{
  const uniquePlayer=[...new Set(playerTeam)];
  if(uniquePlayer.length!==playerTeam.length||playerTeam.some(id=>!byId[id]))throw new Error('O trio do jogador contém IDs repetidos ou inválidos.');
  if(playerTeam.length!==0&&playerTeam.length!==3)throw new Error('A campanha só pode ser gerada após a escolha de exatamente três personagens.');
  const eligible=characters.map(c=>c.id).filter(id=>!uniquePlayer.includes(id));
  if(eligible.length<30)throw new Error('Elenco insuficiente: são necessários três personagens do jogador e trinta inimigos únicos.');
  const rng={rng:seed>>>0};
  const rodada=shuffle(eligible,rng).slice(0,Math.max(33,Math.min(DIFICULDADE.rodada,eligible.length)));
  const used=new Set(uniquePlayer);
  const encounters:Encounter[]=[];
  let sinergiaAnterior=-Infinity;
  for(let i=0;i<9;i++){
    const remaining=rodada.filter(id=>!used.has(id));
    const lista=sampledTeams(remaining,rng,CANDIDATOS).map(team=>({team,forca:forcaDoTrio(team),sinergia:sinergiaDoTrio(team)}));
    if(!lista.length)throw new Error(`Elenco insuficiente para criar o encontro ${i+1} sem repetição.`);
    const forcas=lista.map(x=>x.forca),sinergias=lista.map(x=>x.sinergia);
    // a força sobe dos mais fracos (luta 1) aos mais fortes (luta 9); a sinergia sobe junto e nunca cai de uma luta para a outra
    const alvoForca=FORCA_DA_LUTA[i]!,alvoSinergia=.05+.6*(i/8);
    const nota=(x:typeof lista[number])=>Math.abs(quantil(forcas,x.forca)-alvoForca)*2+Math.abs(quantil(sinergias,x.sinergia)-alvoSinergia);
    let semCair=lista.filter(x=>x.sinergia>=sinergiaAnterior-1e-9);
    // nenhum dos sorteados é tão entrosado quanto o da luta anterior: procura mais trios antes de desistir
    if(!semCair.length)semCair=sampledTeams(remaining,rng,CANDIDATOS*6).map(team=>({team,forca:forcaDoTrio(team),sinergia:sinergiaDoTrio(team)})).filter(x=>x.sinergia>=sinergiaAnterior-1e-9);
    const escolhido=semCair.length?semCair.reduce((a,b)=>nota(b)<nota(a)?b:a):lista.reduce((a,b)=>b.sinergia>a.sinergia?b:a);
    sinergiaAnterior=escolhido.sinergia;
    const team=[...escolhido.team];
    encounters.push({team,name:names[i]!,power:Math.round(escolhido.forca*100)/100,scale:ESCALAS[i]!});
    team.forEach(id=>used.add(id));
  }
  const boss=trioMaisForte(rodada.filter(id=>!used.has(id)),rng,sinergiaAnterior);
  encounters.push({team:boss,name:names[9]!,power:Math.round(forcaDoTrio(boss)*100)/100,scale:ESCALAS[9]!});
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
