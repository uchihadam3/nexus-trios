import { characters, byId } from '../data/characters';
import { random, shuffle } from './random';
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { LIGACOES_DOS_COMBOS, idsDosCombos } from './combos';
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
 * A campanha por faixas fica logo abaixo, em FAIXAS.
 */
/* A sinergia do trio: os combos acesos (src/engine/combos.ts), cada um com o peso medido nas lutas. */
export function sinergiaDoTrio(team:readonly string[]):number{
  // o mesmo que somar ligacoesDosCombos × PESO_DA_LIGACAO, na mesma ordem (o resultado sai idêntico, bit a bit), sem montar o objeto de 56 chaves: a campanha avalia milhares de trios
  const conta=new Map<number,number>();
  for(const id of idsDosCombos(team)){const i=ORDEM_DA_LIGACAO.get(id.startsWith('lenda-')?'lenda':id)!;conta.set(i,Math.min(2,(conta.get(i)??0)+1));}
  let n=0;for(const i of [...conta.keys()].sort((a,b)=>a-b))n+=conta.get(i)!*(PESO_DA_LIGACAO[LIGACOES_DOS_COMBOS[i]!]??0);
  return n;
}
const ORDEM_DA_LIGACAO=new Map(LIGACOES_DOS_COMBOS.map((l,i)=>[l,i]));
export function forcaDoTrio(team:readonly string[]):number{return team.reduce((n,id)=>n+(FORCA[id]??0),0)+sinergiaDoTrio(team);}
/*
 * A campanha por faixas (pedido do jogador): os rivais possíveis são separados em cinco faixas de força —
 * muito fracos, fracos, médios, fortes e muito fortes — e de cada faixa saem dois trios sorteados. O mais
 * fraco dos dois vai para as lutas ímpares (1, 3, 5, 7, 9) e o mais forte para as pares (2, 4, 6, 8, 10):
 * a luta 10 é o mais forte dos dois sorteados entre os muito fortes, não o mais forte de todos.
 *
 * As faixas são as mesmas para todo trio (PUXA_DO_TRIO = 0): com a força medida em 2 milhões de lutas,
 * puxar as faixas com o trio apagava a vantagem de escolher bem. Só o trio que passa de todos os rivais
 * possíveis (cheio de combos) enfrenta rivais com mais Vida (VIDA_ACIMA_DO_TOPO). Medido em 40 personagens:
 * o trio sorteado vence ~5% das jornadas, o de quem escolhe bem ~12% e o melhor ~38%. Sem trio (a Diária e a Semanal, os
 * mesmos rivais para todos), as faixas ficam no meio. ESCALAS é a Vida dos rivais (×) em cada luta.
 */
/** O centro de cada faixa, em percentil da força dos rivais possíveis: muito fracos … muito fortes. */
export const FAIXAS=[0.03,0.17,0.37,0.57,0.77];
/** Meia largura de cada faixa (em percentil). */
export const LARGURA_DA_FAIXA=0.1;
/** Quanto as faixas sobem (ou descem) com a força do trio do jogador: 0 = nada, 1 = totalmente. */
export const PUXA_DO_TRIO=0;
/** Quanto a Vida dos rivais acompanha a força do trio do jogador: ×(1 + VIDA_PELO_TRIO·(percentil − 0,5)). */
export const VIDA_PELO_TRIO=0;
/*
 * Um trio cheio de combos pode ficar acima de todos os rivais possíveis: aí as faixas já estão no topo e não
 * sobem mais. Para ele, a Vida dos rivais cresce com o quanto ele passa do topo (força acima do percentil 97).
 */
export const VIDA_ACIMA_DO_TOPO=0.55;
/** Quantos trios rivais possíveis são sorteados para formar as faixas. */
const AMOSTRA=900;
export const ESCALAS=[.8,.82,.84,.84,.87,.9,.935,.945,.965,.965];
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
type Candidato={team:string[];forca:number};
/*
 * Em que percentil da força dos rivais possíveis o trio do jogador está (0,5 sem trio). Conta os personagens e
 * os combos (forcaDoTrio): com os combos de fora, um trio cheio deles vencia a jornada quase sempre (acima de 90%).
 */
function percentilDoTrio(amostra:Candidato[],playerTeam:string[]):number{
  if(playerTeam.length!==3)return .5;
  const f=forcaDoTrio(playerTeam);
  return amostra.filter(x=>x.forca<f).length/amostra.length;
}
export function generateCampaign(seed:number,playerTeam:string[]=[]):Encounter[]{
  const uniquePlayer=[...new Set(playerTeam)];
  if(uniquePlayer.length!==playerTeam.length||playerTeam.some(id=>!byId[id]))throw new Error('O trio do jogador contém IDs repetidos ou inválidos.');
  if(playerTeam.length!==0&&playerTeam.length!==3)throw new Error('A campanha só pode ser gerada após a escolha de exatamente três personagens.');
  const eligible=characters.map(c=>c.id).filter(id=>!uniquePlayer.includes(id));
  if(eligible.length<30)throw new Error('Elenco insuficiente: são necessários três personagens do jogador e trinta inimigos únicos.');
  const rng={rng:seed>>>0};
  // os rivais possíveis, do mais fraco ao mais forte
  const amostra=sampledTeams(eligible,rng,AMOSTRA).map(team=>({team,forca:forcaDoTrio(team)})).sort((a,b)=>a.forca-b.forca);
  const percentil=percentilDoTrio(amostra,uniquePlayer),desloca=PUXA_DO_TRIO*(percentil-.5);
  const acima=uniquePlayer.length===3?Math.max(0,forcaDoTrio(uniquePlayer)-amostra[Math.floor(.97*amostra.length)]!.forca):0;
  const vida=1+VIDA_PELO_TRIO*(percentil-.5)+VIDA_ACIMA_DO_TOPO*acima;
  const used=new Set(uniquePlayer),livre=(t:string[])=>t.every(id=>!used.has(id));
  const encounters:Encounter[]=new Array(10);
  FAIXAS.forEach((centro,f)=>{
    const c=Math.min(.97,Math.max(.03,centro+desloca));
    // os dois da faixa: sorteados entre os livres da faixa (se faltar, a faixa alarga até achar)
    const dois:Candidato[]=[];
    for(let largura=LARGURA_DA_FAIXA;dois.length<2;largura+=.05){
      const de=Math.floor(Math.max(0,c-largura)*amostra.length),ate=Math.ceil(Math.min(1,c+largura)*amostra.length);
      const faixa=amostra.slice(de,ate).filter(x=>livre(x.team));
      if(!faixa.length){if(largura>1)throw new Error('Elenco insuficiente para montar os rivais sem repetição.');continue;}
      const x=faixa[Math.floor(random(rng)*faixa.length)]!;
      dois.push(x);x.team.forEach(id=>used.add(id));
    }
    dois.sort((a,b)=>a.forca-b.forca).forEach((x,k)=>{
      const i=2*f+k;
      encounters[i]={team:[...x.team],name:names[i]!,power:Math.round(x.forca*100)/100,scale:Math.round(ESCALAS[i]!*vida*1000)/1000};
    });
  });
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
