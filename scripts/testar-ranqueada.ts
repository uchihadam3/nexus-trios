/*
 * Ponta a ponta contra o Supabase de verdade: cria conta, escolhe nome,
 * pede o desafio, abre a Jornada, refaz as 10 lutas aqui e envia o resumo.
 *
 * A pontuação nunca vai do cliente — quem calcula é o servidor, refazendo as
 * lutas com a cópia dele do motor. Se a cópia dele for diferente desta, é aqui
 * que aparece.
 *
 * Uso: npx tsx scripts/testar-ranqueada.ts <email> <senha> <nome>
 */
import { readFileSync } from 'node:fs';
import { createClient } from '@supabase/supabase-js';

import { characters } from '../src/data/characters';
import { ENGINE_VERSION, BALANCE_VERSION, replayRanked, rosterFingerprint, runDigest } from '../src/engine/ranked';
import { generateCampaign } from '../src/engine/campaign';

const env = Object.fromEntries(readFileSync('.env.production', 'utf8').split('\n').filter((l) => l.includes('=')).map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1).trim()]));
const [email, senha, nome] = process.argv.slice(2);
const sb = createClient(env.VITE_SUPABASE_URL, env.VITE_SUPABASE_PUBLISHABLE_KEY, { auth: { persistSession: false } });
const passo = (t: string) => console.log(`\n▶ ${t}`);
const chamar = async (body: Record<string, unknown>) => {
  const { data, error } = await sb.functions.invoke('ranked-api', { body });
  if (error) { let msg = error.message; try { msg = ((await (error.context as Response).json()) as { error?: string }).error ?? msg; } catch { /* sem corpo */ } return { erro: msg }; }
  return data as Record<string, unknown>;
};

passo('1. criar conta (ou entrar, se já existir)');
let s = await sb.auth.signUp({ email, password: senha, options: { data: { handle: nome } } });
if (s.error?.message.includes('already')) s = await sb.auth.signInWithPassword({ email, password: senha }) as typeof s;
if (s.error) { console.log('   ✗', s.error.message); process.exit(1); }
console.log('   ✓ sessão aberta na hora:', !!s.data.session, '· e-mail confirmado:', !!s.data.user?.email_confirmed_at);
if (!s.data.session) process.exit(1);

passo('2. nome público');
console.log('  ', JSON.stringify(await chamar({ action: 'profile', handle: nome })));

passo('3. desafio do dia');
const ch = await chamar({ action: 'challenge', mode: 'daily' }) as { challenge?: { seed: number; engine_version: string; roster_fingerprint: string }; banned?: string[]; erro?: string };
if (!ch.challenge) { console.log('   ✗', ch.erro); process.exit(1); }
console.log(`   servidor: motor ${ch.challenge.engine_version} · elenco ${ch.challenge.roster_fingerprint}`);
console.log(`   este jogo: motor ${ENGINE_VERSION} · elenco ${rosterFingerprint()} · temporada ${BALANCE_VERSION}`);
console.log('   elenco igual?', ch.challenge.roster_fingerprint === rosterFingerprint() ? 'SIM' : 'NÃO — o servidor está com outra versão dos personagens');

passo('4. abrir a Jornada');
/*
 * Um trio que vence várias lutas. Com uma derrota logo na primeira, o resumo
 * enviado é quase vazio, e servidor e cliente concordarem não prova que o
 * motor deles é o mesmo. Quanto mais lutas, mais forte a prova.
 */
const banidos = new Set(ch.banned ?? generateCampaign(ch.challenge.seed).flatMap((e) => e.team));
const livres = characters.filter((c) => !banidos.has(c.id)).map((c) => c.id);
let trio = livres.slice(0, 3), vitorias = -1;
for (let i = 0; i < 300 && vitorias < 6; i++) {
  const t = [...livres].sort(() => Math.random() - .5).slice(0, 3);
  const v = replayRanked(t, ch.challenge.seed).encountersCleared;
  if (v > vitorias) { trio = t; vitorias = v; }
}
console.log(`   trio escolhido aqui: ${trio.join(', ')} (vence ${vitorias} lutas)`);
const st = await chamar({ action: 'start', mode: 'daily', team: trio }) as { run?: { id: string; seed: number }; erro?: string };
if (!st.run) { console.log('   ✗', st.erro); process.exit(1); }
console.log(`   ✓ Jornada ${st.run.id.slice(0, 8)}… · trio ${trio.join(', ')}`);

passo('5. jogar as 10 lutas aqui e enviar só o resumo');
const r = replayRanked(trio, st.run.seed);
console.log(`   aqui: ${r.encountersCleared}/10 vencidas · pontuação calculada aqui ${r.score} (não é enviada)`);
const digest = await runDigest(st.run.id, trio, st.run.seed, r.summaries.map((x) => x.won));
const sub = await chamar({ action: 'submit', runId: st.run.id, digest });
console.log('  ', JSON.stringify(sub));

passo('6. ranking do dia');
const lb = await chamar({ action: 'leaderboard', mode: 'daily' }) as { entries?: { position: number; handle: string; score: number }[]; erro?: string };
console.log('  ', lb.entries ? lb.entries.slice(0, 5).map((e) => `${e.position}º ${e.handle} ${e.score}`).join(' · ') || '(vazio)' : lb.erro);
