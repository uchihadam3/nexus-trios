import {createClient} from 'npm:@supabase/supabase-js@2.117.2';
import {characters} from '../../../src/data/characters.ts';
import {generateCampaign} from '../../../src/engine/campaign.ts';
import {BALANCE_VERSION,ENGINE_VERSION,replayRanked,rosterFingerprint,runDigest} from '../../../src/engine/ranked.ts';

declare const Deno:{env:{get:(name:string)=>string|undefined};serve:(handler:(request:Request)=>Response|Promise<Response>)=>unknown};
type Mode='daily'|'weekly';
const url=Deno.env.get('SUPABASE_URL')!,secret=Deno.env.get('SUPABASE_SECRET_KEY')??Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,publishable=Deno.env.get('SUPABASE_PUBLISHABLE_KEY')??Deno.env.get('SUPABASE_ANON_KEY')!;
const admin=createClient(url,secret,{auth:{persistSession:false,autoRefreshToken:false}});
const authClient=createClient(url,publishable,{auth:{persistSession:false,autoRefreshToken:false}});
const allowed=new Set(['https://uchihadam3.github.io','http://localhost:5173','http://127.0.0.1:5173']);
const json=(data:unknown,status=200,origin='')=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json','cache-control':'no-store','access-control-allow-origin':allowed.has(origin)?origin:'https://uchihadam3.github.io','access-control-allow-headers':'authorization, apikey, content-type, x-client-info','access-control-allow-methods':'POST, OPTIONS'}});
const fail=(message:string,status=400,origin='')=>json({error:message},status,origin);
const iso=(date:Date)=>date.toISOString().slice(0,10);
const period=(mode:Mode)=>{const date=new Date();if(mode==='weekly')date.setUTCDate(date.getUTCDate()-(date.getUTCDay()+6)%7);return iso(date)};
async function seedFor(mode:Mode,key:string){const bytes=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(`nexus:${BALANCE_VERSION}:${mode}:${key}`)));return new DataView(bytes.buffer).getUint32(0,false)&0x7fffffff;}
async function challenge(mode:Mode){
  const key=period(mode),seed=await seedFor(mode,key),fingerprint=rosterFingerprint();
  const payload={mode,period_key:key,seed,engine_version:ENGINE_VERSION,balance_version:BALANCE_VERSION,roster_fingerprint:fingerprint};
  const {data,error}=await admin.from('ranked_challenges').upsert(payload,{onConflict:'mode,period_key,engine_version'}).select('id,mode,period_key,seed,engine_version,balance_version,roster_fingerprint').single();
  if(error||!data)throw new Error(`Desafio indisponível: ${error?.message??'sem resposta'}`);
  return data;
}
function validHandle(value:unknown){if(typeof value!=='string')return null;const handle=value.trim().replace(/\s+/g,' ');
  if(!/^[A-Za-z0-9_ ]{3,16}$/.test(handle)||/@/.test(handle)||/\d{7}/.test(handle)||/(?:fuck|shit|puta|merda|porra|nazi|hitler)/i.test(handle.replace(/[ _]/g,'')))return null;return handle;
}
async function profile(userId:string){const {data,error}=await admin.from('players').select('id,handle,nexus_level,xp,renamed_at').eq('id',userId).maybeSingle();if(error)throw error;return data;}
/*
 * O ranking vem de `leaderboard_entries`, onde cada conta tem até 3 trios
 * diferentes por ranking — a regra da FASE K, garantida pelo banco. Antes, o
 * ranking pegava só a melhor partida de cada conta.
 *
 * `meus` é a caixa "Meus 3 melhores trios": as entradas da própria conta,
 * quantas vagas sobram e o que a próxima entrada precisa superar.
 */
type Escopo='daily'|'weekly'|'season';
const chaveDo=(escopo:Escopo)=>escopo==='season'?BALANCE_VERSION:period(escopo);
async function board(userId:string,mode:Escopo,detailId?:string){
  const key=chaveDo(mode);
  const {data,error}=await admin.from('leaderboard_entries').select('player_id,run_id,score,encounters_cleared,team_ids,achieved_at').eq('scope',mode).eq('period_key',key).order('score',{ascending:false}).order('achieved_at',{ascending:true}).limit(1000);
  if(error)throw error;
  const rows=data??[];
  const ids=[...new Set(rows.map(r=>r.player_id))],names=ids.length?(await admin.from('players').select('id,handle').in('id',ids)).data??[]:[];
  const handleOf=new Map(names.map(x=>[x.id,x.handle]));
  const visiveis=rows.filter((r,i)=>i<50||r.player_id===userId||r.run_id===detailId);
  const runIds=[...new Set(visiveis.map(r=>r.run_id))];
  const runs=runIds.length?(await admin.from('ranked_runs').select('id,seed,summary,engine_version,balance_version').in('id',runIds)).data??[]:[];
  const runOf=new Map(runs.map(r=>[r.id,r]));
  const publico=(r:typeof rows[number],index:number)=>{const run=runOf.get(r.run_id);return {position:index+1,id:r.run_id,handle:handleOf.get(r.player_id)??'Jogador',score:r.score,progress:r.encounters_cleared,team:r.team_ids,date:r.achieved_at,seed:run?.seed??0,engineVersion:run?.engine_version??ENGINE_VERSION,balanceVersion:run?.balance_version??BALANCE_VERSION,highlights:run?.summary?.highlights??{}};};
  const todos=rows.map(publico),meus=todos.filter((_,i)=>rows[i].player_id===userId);
  return {mode,period:key,entries:todos.slice(0,50),mine:meus[0]??null,
    meus:{entries:meus,vagas:Math.max(0,3-meus.length),precisaSuperar:meus.length>=3?Math.min(...meus.map(m=>m.score)):null},
    details:detailId?(todos.find(x=>x.id===detailId)??null):null};
}

Deno.serve(async (request:Request)=>{
  const origin=request.headers.get('origin')??'';
  if(origin&&!allowed.has(origin))return fail('Origem não permitida.',403,origin);
  if(request.method==='OPTIONS')return new Response(null,{status:204,headers:{'access-control-allow-origin':allowed.has(origin)?origin:'https://uchihadam3.github.io','access-control-allow-headers':'authorization, apikey, content-type, x-client-info','access-control-allow-methods':'POST, OPTIONS'}});
  if(request.method!=='POST')return fail('Método inválido.',405,origin);
  const bearer=request.headers.get('authorization')??'',token=bearer.startsWith('Bearer ')?bearer.slice(7):'';
  if(!token)return fail('Autenticação necessária.',401,origin);
  const {data:{user},error:authError}=await authClient.auth.getUser(token);
  if(authError||!user)return fail('Sessão inválida.',401,origin);
  if(Number(request.headers.get('content-length')??0)>8192)return fail('Pedido muito grande.',413,origin);
  const raw=await request.text();if(raw.length>8192)return fail('Pedido muito grande.',413,origin);
  let input:Record<string,unknown>;try{input=JSON.parse(raw) as Record<string,unknown>;}catch{return fail('JSON inválido.',400,origin)}
  try{
    if(input.action==='profile'){
      if(input.handle===undefined){const existing=await profile(user.id);return json({profile:existing&&{handle:existing.handle,xp:existing.xp,level:existing.nexus_level}},200,origin);}
      const handle=validHandle(input.handle);if(!handle)return fail('Use 3–16 letras, números, espaços ou _. Sem contato pessoal ou ofensa.',422,origin);
      const existing=await profile(user.id);
      if(existing&&existing.handle.toLowerCase()===handle.toLowerCase())return json({profile:{handle:existing.handle,xp:existing.xp,level:existing.nexus_level}},200,origin);
      if(existing?.renamed_at&&Date.now()-new Date(existing.renamed_at).getTime()<30*86400000)return fail('Nome pode mudar uma vez a cada 30 dias.',429,origin);
      const agora=new Date().toISOString();
      const result=existing?await admin.from('players').update({handle,renamed_at:agora,updated_at:agora}).eq('id',user.id).select('handle,xp,nexus_level').single():await admin.from('players').insert({id:user.id,handle}).select('handle,xp,nexus_level').single();
      if(result.error){if(result.error.code==='23505')return fail('Este nome já está em uso.',409,origin);throw result.error;}
      return json({profile:{handle:result.data.handle,xp:result.data.xp,level:result.data.nexus_level}},200,origin);
    }
    if(input.action==='challenge'){
      const mode=input.mode==='weekly'?'weekly':'daily',data=await challenge(mode);
      return json({challenge:data,banned:generateCampaign(data.seed).flatMap(e=>e.team)},200,origin);
    }
    if(input.action==='start'){
      const player=await profile(user.id);if(!player)return fail('Escolha seu nome público antes da Ranqueada.',409,origin);
      const mode=input.mode==='weekly'?'weekly':'daily',data=await challenge(mode);
      const team=input.team;
      if(!Array.isArray(team)||team.length!==3||team.some(id=>typeof id!=='string'||id.length>80)||new Set(team).size!==3||team.some(id=>!characters.some(c=>c.id===id)))return fail('Trio inválido.',422,origin);
      const banned=new Set(generateCampaign(data.seed).flatMap(e=>e.team));if(team.some(id=>banned.has(id)))return fail('Um integrante faz parte dos rivais deste desafio.',422,origin);
      const {count,error:rateError}=await admin.from('ranked_runs').select('id',{count:'exact',head:true}).eq('player_id',user.id).gte('started_at',new Date(Date.now()-3600000).toISOString());
      if(rateError)throw rateError;if((count??0)>=12)return fail('Limite de 12 tentativas por hora. Volte mais tarde.',429,origin);
      const {data:run,error}=await admin.from('ranked_runs').insert({player_id:user.id,challenge_id:data.id,mode,period_key:data.period_key,seed:data.seed,engine_version:ENGINE_VERSION,balance_version:BALANCE_VERSION,roster_fingerprint:data.roster_fingerprint,team_ids:team}).select('id,seed,mode,period_key,engine_version,roster_fingerprint').single();
      if(error||!run)throw error??new Error('Não foi possível abrir a Jornada.');
      return json({run},200,origin);
    }
    if(input.action==='submit'){
      if(typeof input.runId!=='string'||!/^[0-9a-f-]{36}$/i.test(input.runId)||typeof input.digest!=='string'||!/^[0-9a-f]{64}$/i.test(input.digest))return fail('Envio inválido.',422,origin);
      if('score' in input)return fail('O servidor calcula a pontuação.',422,origin);
      const {data:run,error}=await admin.from('ranked_runs').select('*').eq('id',input.runId).eq('player_id',user.id).maybeSingle();if(error)throw error;
      if(!run)return fail('Jornada inexistente.',404,origin);if(run.verified)return fail('Jornada já validada.',409,origin);
      if(new Date(run.expires_at).getTime()<Date.now())return fail('Jornada expirada.',410,origin);
      if(run.engine_version!==ENGINE_VERSION||run.roster_fingerprint!==rosterFingerprint()||run.balance_version!==BALANCE_VERSION)return fail('Versão do motor não reconhecida.',409,origin);
      const verified=replayRanked(run.team_ids,run.seed),digest=await runDigest(run.id,run.team_ids,run.seed,verified.summaries.map(s=>s.won));
      if(digest!==input.digest)return fail('Replay não corresponde ao desafio registrado.',422,origin);
      /*
       * O Top 3 é registrado *antes* de a partida ser marcada como validada.
       *
       * São duas escritas, e se a segunda falhasse depois da primeira, a
       * partida ficaria validada e fora do ranking, sem volta: um novo envio
       * esbarraria em "Jornada já validada". Nesta ordem, uma falha deixa a
       * partida aberta e o jogador pode reenviar; e reenviar é seguro, porque
       * o mesmo trio com a mesma pontuação só "mantém" a entrada.
       */
      const registrar=async(escopo:Escopo,chave:string)=>{const {data,error}=await admin.rpc('registrar_no_top3',{p_player:user.id,p_scope:escopo,p_period:chave,p_team:run.team_ids,p_run:run.id,p_score:verified.score,p_cleared:verified.encountersCleared});if(error)throw error;return data;};
      const top3={periodo:await registrar(run.mode,String(run.period_key)),temporada:await registrar('season',BALANCE_VERSION)};
      const {data:saved,error:saveError}=await admin.from('ranked_runs').update({verified:true,finished_at:new Date().toISOString(),encounters_cleared:verified.encountersCleared,score:verified.score,summary:{highlights:verified.highlights,outcomes:verified.summaries.map(s=>s.won)},digest}).eq('id',run.id).eq('verified',false).select('id').maybeSingle();
      if(saveError)throw saveError;if(!saved)return fail('Jornada já enviada.',409,origin);
      const player=await profile(user.id),xp=(player?.xp??0)+30+verified.encountersCleared*30+(verified.encountersCleared===10?250:0);
      await admin.from('players').update({xp,nexus_level:Math.floor(Math.sqrt(xp/100))+1,updated_at:new Date().toISOString()}).eq('id',user.id);
      const daily=await board(user.id,'daily'),weekly=await board(user.id,'weekly'),season=await board(user.id,'season');
      return json({verified:true,score:verified.score,progress:verified.encountersCleared,daily:daily.mine?.position??null,weekly:weekly.mine?.position??null,season:season.mine?.position??null,top3},200,origin);
    }
    /* "MEUS RECORDES: histórico completo." Todas as partidas validadas da conta. */
    if(input.action==='historico'){
      const {data,error}=await admin.from('ranked_runs').select('id,mode,period_key,score,encounters_cleared,team_ids,finished_at').eq('player_id',user.id).eq('verified',true).order('finished_at',{ascending:false}).limit(100);
      if(error)throw error;
      return json({runs:(data??[]).map(r=>({id:r.id,mode:r.mode,period:r.period_key,score:r.score,progress:r.encounters_cleared,team:r.team_ids,date:r.finished_at}))},200,origin);
    }
    if(input.action==='leaderboard'){
      const mode=input.mode==='weekly'?'weekly':input.mode==='season'?'season':'daily';
      return json(await board(user.id,mode,typeof input.detailId==='string'?input.detailId:undefined),200,origin);
    }
    return fail('Ação desconhecida.',404,origin);
  }catch(error){console.error('ranked-api',input.action,error instanceof Error?error.message:String(error));return fail('Serviço temporariamente indisponível.',503,origin);}
});
