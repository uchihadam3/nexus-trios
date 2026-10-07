import {createClient} from '@supabase/supabase-js';

const url=import.meta.env.VITE_SUPABASE_URL as string|undefined,key=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string|undefined;
export const onlineConfigured=!!url&&!!key&&import.meta.env.VITE_RANKED_ENABLED==='true';
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
export async function onlineCall<T>(action:string,body:Record<string,unknown>={}):Promise<T>{
  await session();const {data,error}=await client!.functions.invoke('ranked-api',{body:{action,...body}});
  if(error){let message=error.message;try{const response=error.context as Response;const detail=await response.json() as {error?:string};message=detail.error??message;}catch{/* Network failures have no JSON body. */}throw new Error(message);}
  if(data?.error)throw new Error(data.error);return data as T;
}
export interface PublicRun {position:number;id:string;handle:string;score:number;progress:number;team:string[];date:string;seed:number;engineVersion:string;balanceVersion:string;highlights:{survivors?:number;turns?:number}}
export interface Leaderboard {mode:'daily'|'weekly'|'season';period:string;entries:PublicRun[];mine:PublicRun|null;details:PublicRun|null}
