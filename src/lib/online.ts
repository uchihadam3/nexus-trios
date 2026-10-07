import {createClient} from '@supabase/supabase-js';

const url=import.meta.env.VITE_SUPABASE_URL as string|undefined,key=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string|undefined;
export const onlineConfigured=!!url&&!!key&&import.meta.env.VITE_RANKED_ENABLED==='true';
const client=onlineConfigured?createClient(url!,key!,{auth:{autoRefreshToken:true,persistSession:true,detectSessionInUrl:false}}):null;
async function session(){
  if(!client)throw new Error('Ranking online ainda não está conectado.');
  const current=await client.auth.getSession();if(current.error)throw new Error(current.error.message);
  if(current.data.session)return current.data.session;
  const signed=await client.auth.signInAnonymously();if(signed.error||!signed.data.session)throw new Error(signed.error?.message??'Não foi possível iniciar a sessão anônima.');
  return signed.data.session;
}
export async function onlineCall<T>(action:string,body:Record<string,unknown>={}):Promise<T>{
  await session();const {data,error}=await client!.functions.invoke('ranked-api',{body:{action,...body}});
  if(error){let message=error.message;try{const response=error.context as Response;const detail=await response.json() as {error?:string};message=detail.error??message;}catch{/* Network failures have no JSON body. */}throw new Error(message);}
  if(data?.error)throw new Error(data.error);return data as T;
}
export interface PublicRun {position:number;id:string;handle:string;score:number;progress:number;team:string[];date:string;seed:number;engineVersion:string;balanceVersion:string;highlights:{survivors?:number;turns?:number}}
export interface Leaderboard {mode:'daily'|'weekly'|'season';period:string;entries:PublicRun[];mine:PublicRun|null;details:PublicRun|null}
