/*
 * FASE K ponta a ponta, contra o Supabase de verdade: uma conta joga quatro
 * trios diferentes e repete um, e o servidor tem de responder como o
 * documento manda — três entram, o quarto melhor tira o pior, o repetido só
 * mantém. Confere também que a pontuação do servidor é a mesma calculada aqui.
 *
 * Uso: npx tsx scripts/testar-top3.ts <email> <senha> <nome>
 */
import { readFileSync } from 'node:fs';
import { createClient } from '@supabase/supabase-js';

import { characters } from '../src/data/characters';
import { generateCampaign } from '../src/engine/campaign';
import { replayRanked, runDigest } from '../src/engine/ranked';

const env = Object.fromEntries(readFileSync('.env.production', 'utf8').split('\n').filter((l) => l.includes('=')).map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1).trim()]));
const [email, senha, nome] = process.argv.slice(2);
const sb = createClient(env.VITE_SUPABASE_URL, env.VITE_SUPABASE_PUBLISHABLE_KEY, { auth: { persistSession: false } });
let falhas = 0;
const confere = (ok: boolean, texto: string) => { console.log(`   ${ok ? '✓' : '✗'} ${texto}`); if (!ok) falhas++; };
const chamar = async (body: Record<string, unknown>): Promise<Record<string, any>> => {
  const { data: { session } } = await sb.auth.getSession();
  const r = await fetch(`${env.VITE_SUPABASE_URL}/functions/v1/ranked-api`, { method: 'POST',
    headers: { authorization: `Bearer ${session!.access_token}`, apikey: env.VITE_SUPABASE_PUBLISHABLE_KEY, 'content-type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(`${body.action}: ${j.error}`); return j;
};

let s = await sb.auth.signUp({ email, password: senha });
if (s.error?.message.includes('already')) s = await sb.auth.signInWithPassword({ email, password: senha }) as typeof s;
if (!s.data.session) throw new Error(s.error?.message ?? 'sem sessão');
await chamar({ action: 'profile', handle: nome });
const { challenge } = await chamar({ action: 'challenge', mode: 'daily' });
const banidos = new Set(generateCampaign(challenge.seed).flatMap((e) => e.team));
const livres = characters.filter((c) => !banidos.has(c.id)).map((c) => c.id);

/* Quatro trios com pontuações diferentes; o quarto é o melhor, para tirar o pior. */
const candidatos: { trio: string[]; score: number }[] = [];
const vistos = new Set<number>();
for (let i = 0; candidatos.length < 4 && i < 400; i++) {
  const trio = [...livres].sort(() => Math.random() - .5).slice(0, 3), score = replayRanked(trio, challenge.seed).score;
  if (score > 0 && !vistos.has(score)) { vistos.add(score); candidatos.push({ trio, score }); }
}
candidatos.sort((a, b) => a.score - b.score);
const ordem = [candidatos[1], candidatos[0], candidatos[2], candidatos[3], candidatos[2]];

const jogar = async ({ trio, score }: { trio: string[]; score: number }) => {
  const { run } = await chamar({ action: 'start', mode: 'daily', team: trio });
  const r = replayRanked(trio, run.seed);
  const digest = await runDigest(run.id, trio, run.seed, r.summaries.map((x) => x.won));
  const sub = await chamar({ action: 'submit', runId: run.id, digest });
  return { esperado: score, servidor: sub.score as number, top3: sub.top3?.periodo };
};

console.log('▶ três trios diferentes');
for (const [i, c] of ordem.slice(0, 3).entries()) {
  const r = await jogar(c);
  confere(r.servidor === r.esperado, `pontuação do servidor ${r.servidor} = calculada aqui ${r.esperado} (sem bônus escondido)`);
  confere(r.top3?.situacao === 'novo' && r.top3?.vagas === 2 - i, `trio ${i + 1}: "${r.top3?.situacao}", ${r.top3?.vagas} vaga(s)`);
}
console.log('▶ quarto trio, melhor que todos');
const q = await jogar(ordem[3]);
confere(q.top3?.situacao === 'entrou' && q.top3?.removido === candidatos[0].score, `"${q.top3?.situacao}", saiu ${q.top3?.removido} (o pior era ${candidatos[0].score})`);
console.log('▶ repetir um trio que já está no Top 3');
const rep = await jogar(ordem[4]);
confere(rep.top3?.situacao === 'manteve' && rep.top3?.recorde === candidatos[2].score, `"${rep.top3?.situacao}", recorde ${rep.top3?.recorde}`);

console.log('▶ ranking e histórico');
const lb = await chamar({ action: 'leaderboard', mode: 'daily' });
const minhas = lb.entries.filter((e: any) => e.handle === nome);
confere(minhas.length === 3, `${minhas.length} linhas desta conta no ranking de hoje`);
confere(lb.meus?.entries.length === 3 && lb.meus?.vagas === 0 && lb.meus?.precisaSuperar === candidatos[1].score, `caixa "Meus 3": vagas ${lb.meus?.vagas}, precisa superar ${lb.meus?.precisaSuperar}`);
const hist = await chamar({ action: 'historico' });
confere(hist.runs.length === 5, `histórico com ${hist.runs.length} jornadas`);
const temporada = await chamar({ action: 'leaderboard', mode: 'season' });
confere(temporada.meus?.entries.length === 3, `temporada também com ${temporada.meus?.entries.length} entradas`);
console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO CERTO');
process.exit(falhas ? 1 : 0);
