/*
 * As telas da FASE K no navegador, com o servidor simulado em dois formatos:
 *
 *   antigo — o que a função publicada antes da FASK K responde: sem `meus`, e
 *            "Ação desconhecida." para o histórico. Nada pode quebrar: sem
 *            caixa "Meus 3", sem erro, e "Meus recordes" como era.
 *   novo   — a resposta da função da FASE K: caixa "Meus 3", a mesma conta
 *            até 3 vezes no ranking, e o histórico completo.
 *
 * O login também é simulado: o teste não cria conta nenhuma no projeto real.
 * Uso: node scripts/top3-navegador.mjs
 */
import { chromium } from 'playwright';
import { execSync } from 'node:child_process';
const SAIDA = process.env.SAIDA ?? './prints';
const proxy = (process.env.HTTPS_PROXY ?? '').replace(/^http:\/\//, '').replace(/\/$/, '');
const spki = proxy && execSync("openssl x509 -in /root/.ccr/agent-proxy-ca.crt -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64").toString().trim();
const b = await chromium.launch(proxy ? { args: [`--proxy-server=https=${proxy}`, `--ignore-certificate-errors-spki-list=${spki}`] } : {});

const trio = (a, c, d) => [a, c, d];
const linha = (position, handle, score, team, id) => ({ position, id, handle, score, progress: Math.floor(score / 1e6), team, date: '2026-10-07T20:00:00Z', seed: 1, engineVersion: 'nexus-250.3', balanceVersion: 'season-1', highlights: { survivors: 2 } });
const meus = [linha(2, 'Uchihadam', 7210400, trio('goku', 'storm', 'pikachu'), 'r1'), linha(4, 'Uchihadam', 6880100, trio('naruto', 'sasuke', 'sakura'), 'r2'), linha(7, 'Uchihadam', 5120900, trio('thor', 'loki', 'hulk'), 'r3')];
const simulado = {
  leaderboard: { mode: 'daily', period: '2026-10-07', entries: [linha(1, 'Diego', 8100200, trio('batman', 'superman', 'flash'), 'x1'), meus[0], linha(3, 'Ana', 7001000, trio('ichigo', 'rukia', 'renji'), 'x2'), meus[1], linha(5, 'Diego', 6500000, trio('luffy', 'zoro', 'nami'), 'x3'), linha(6, 'Teste_Claude', 6103652, trio('kazuya', 'kirby', 'jin'), 'x4'), meus[2]], mine: meus[0], details: null, meus: { entries: meus, vagas: 0, precisaSuperar: 5120900 } },
  historico: { runs: [7210400, 6880100, 3078971, 5120900, 1200000].map((s, i) => ({ id: `h${i}`, mode: i % 3 ? 'daily' : 'weekly', period: '2026-10-07', score: s, progress: Math.floor(s / 1e6), team: [meus[0].team, meus[1].team, ['kazuya', 'kirby', 'jin'], meus[2].team, ['batman', 'robin', 'alfred']][i], date: `2026-10-0${7 - i}T20:00:00Z` })) },
};

/* Uma sessão de mentira, no formato que o supabase-js guarda. */
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
const agora = Math.floor(Date.now() / 1000);
const usuario = { id: '00000000-0000-4000-8000-000000000001', aud: 'authenticated', role: 'authenticated', email: 'voce@exemplo.com', app_metadata: { provider: 'email' }, user_metadata: { handle: 'Uchihadam' }, created_at: '2026-10-07T00:00:00Z' };
const sessao = { access_token: `${b64({ alg: 'HS256', typ: 'JWT' })}.${b64({ sub: usuario.id, exp: agora + 3600, role: 'authenticated', aud: 'authenticated' })}.assinatura`, token_type: 'bearer', expires_in: 3600, expires_at: agora + 3600, refresh_token: 'falso', user: usuario };
const antigo = { leaderboard: { ...simulado.leaderboard, meus: undefined, entries: simulado.leaderboard.entries.filter((e, i, a) => a.findIndex((x) => x.handle === e.handle) === i) } };

for (const modo of ['antigo', 'novo']) {
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  const cors = { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*' };
  await p.route('**/auth/v1/token**', (r) => r.fulfill({ status: 200, contentType: 'application/json', headers: cors, body: JSON.stringify(sessao) }));
  await p.route('**/auth/v1/user**', (r) => r.fulfill({ status: 200, contentType: 'application/json', headers: cors, body: JSON.stringify(usuario) }));
  await p.route('**/functions/v1/ranked-api', async (r) => {
    const acao = r.request().postDataJSON()?.action, fonte = modo === 'novo' ? simulado : antigo;
    if (!(acao in fonte)) return r.fulfill({ status: 404, contentType: 'application/json', headers: cors, body: JSON.stringify({ error: 'Ação desconhecida.' }) });
    await r.fulfill({ status: 200, contentType: 'application/json', headers: cors, body: JSON.stringify(fonte[acao]) });
  });
  await p.goto('http://localhost:5173/nexus-trios/', { waitUntil: 'networkidle' });
  await p.getByRole('button', { name: /conta/i }).first().click(); await p.waitForTimeout(500);
  await p.getByPlaceholder('voce@exemplo.com').fill('voce@exemplo.com');
  await p.getByPlaceholder('pelo menos 8 caracteres').fill('qualquercoisa');
  await p.locator('.account-formulario button.primary').click(); await p.waitForSelector('.account-cartao', { timeout: 20000 });
  await p.getByRole('button', { name: /Abrir menu/i }).click().catch(() => {});
  await p.getByRole('button', { name: /^Ranking$/ }).first().click(); await p.waitForTimeout(3000);
  const caixa = await p.locator('.meus-tres').count();
  console.log(`\n=== ${modo} ===`);
  console.log('  caixa "Meus 3":', caixa ? (await p.locator('.meus-tres').innerText()).replace(/\s+/g, ' ').slice(0, 140) : 'não aparece');
  console.log('  linhas no ranking:', await p.locator('.ranking-list > button').count(), '· marcadas como minhas:', await p.locator('.ranking-list > button.mine').count());
  console.log('  aviso de erro:', await p.locator('[role=alert]').count() ? await p.locator('[role=alert]').innerText() : 'nenhum');
  await p.screenshot({ path: `${SAIDA}/top3-${modo}-hoje.png`, fullPage: true });
  await p.getByRole('button', { name: 'MEUS RECORDES' }).click(); await p.waitForTimeout(3000);
  console.log('  Meus recordes:', (await p.locator('.ranking-screen').innerText()).split('\n').filter((l) => /jornada|validad|melhor resultado|#/i.test(l)).slice(0, 2).join(' | '));
  await p.screenshot({ path: `${SAIDA}/top3-${modo}-recordes.png`, fullPage: true });
  console.log('  rola para o lado:', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), '· erros de página:', erros.length ? erros : 'nenhum');
  await p.close();
}
await b.close();
