import {createClient} from '@supabase/supabase-js';

const url=import.meta.env.VITE_SUPABASE_URL as string|undefined,key=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string|undefined;
export const onlineConfigured=!!url&&!!key&&import.meta.env.VITE_RANKED_ENABLED==='true';
/*
 * Entrar com e-mail e entrar com Google não ficam prontos juntos.
 *
 * O Supabase já nasce aceitando e-mail e senha; o Google não, porque depende
 * de credenciais emitidas pelo dono do projeto no Google Cloud. Sem esta
 * separação, ligar o ranqueado colocava na tela um botão do Google que leva a
 * um erro — e um botão que falha é pior do que um botão que não existe.
 */
export const googleConfigured=onlineConfigured&&import.meta.env.VITE_GOOGLE_ENABLED==='true';
/*
 * `detectSessionInUrl` ligado, porque agora existe volta do Google.
 *
 * O OAuth devolve o jogador com o token no fragmento da URL. Com a detecção
 * desligada — como estava — esse fragmento era ignorado e a volta do Google
 * simplesmente não logava ninguém.
 */
export const client=onlineConfigured?createClient(url!,key!,{auth:{autoRefreshToken:true,persistSession:true,detectSessionInUrl:true}}):null;

/*
 * Ranqueado exige conta.
 *
 * Isto era `signInAnonymously()`: qualquer visitante publicava no ranking sem
 * conta nenhuma, e o documento é explícito no contrário — *"Casual pode ser
 * guest. Online/Ranqueado exige conta."* Jogar continua livre; publicar, não.
 */
async function session(){
  if(!client)throw new Error('Ranking online ainda não está conectado.');
  const current=await client.auth.getSession();if(current.error)throw new Error(current.error.message);
  const sessao=current.data.session;
  if(!sessao||sessao.user.is_anonymous===true)throw new Error('Entre na sua conta para jogar a Jornada Ranqueada.');
  return sessao;
}
/*
 * A chamada vai por `fetch`, e não por `client.functions.invoke`, de propósito.
 *
 * `invoke` acrescenta o cabeçalho `x-client-info`, e a função publicada só
 * autoriza `authorization`, `apikey` e `content-type`. O navegador pergunta
 * antes (o pré-voo do CORS), recebe "não", e a chamada nem sai: o jogador via
 * "Failed to send a request to the Edge Function", em inglês, em toda
 * ranqueada e em todo ranking. Pela linha de comando funcionava, porque lá não
 * existe CORS — só apareceu testando no navegador.
 *
 * Mandar exatamente os três cabeçalhos autorizados funciona com a função que
 * está no ar hoje e com qualquer versão futura dela.
 */
export async function onlineCall<T>(action:string,body:Record<string,unknown>={}):Promise<T>{
  const sessao=await session();
  let resposta:Response;
  try{
    resposta=await fetch(`${url}/functions/v1/ranked-api`,{method:'POST',
      headers:{authorization:`Bearer ${sessao.access_token}`,apikey:key!,'content-type':'application/json'},
      body:JSON.stringify({action,...body})});
  }catch{throw new Error('Sem conexão com o servidor. Confira a internet e tente de novo.');}
  let dados:unknown=null;try{dados=await resposta.json();}catch{/* Corpo vazio ou não-JSON. */}
  const erro=(dados as {error?:unknown}|null)?.error;
  if(!resposta.ok||typeof erro==='string')throw new Error(typeof erro==='string'?erro:'O servidor não respondeu como esperado. Tente de novo em instantes.');
  return dados as T;
}

export interface PublicRun {position:number;id:string;handle:string;score:number;progress:number;team:string[];date:string;seed:number;engineVersion:string;balanceVersion:string;highlights:{survivors?:number;turns?:number}}
/*
 * `meus` só vem da função publicada com a FASE K. A versão anterior não manda,
 * e a tela precisa funcionar com as duas: o jogo vai ao ar antes da função.
 */
export interface MeusTop3 {entries:PublicRun[];vagas:number;precisaSuperar:number|null}
export interface Leaderboard {mode:'daily'|'weekly'|'season';period:string;entries:PublicRun[];mine:PublicRun|null;details:PublicRun|null;meus?:MeusTop3}
export interface PartidaDoHistorico {id:string;mode:'daily'|'weekly';period:string;score:number;progress:number;team:string[];date:string}
