/*
 * A conta e o ranking pela tela do jogo, contra o Supabase de verdade.
 * Uso: node scripts/ranqueada-navegador.mjs <email> <senha>
 * Precisa do build servido em http://localhost:5173 (origem que a função aceita).
 */
import { chromium } from 'playwright';
const [email, senha] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
/*
 * Neste ambiente a internet passa por um proxy que reassina o HTTPS, e o
 * Chromium de teste não lê HTTPS_PROXY nem confia sozinho no certificado dele.
 * Só o tráfego https vai pelo proxy — o jogo em localhost segue direto — e o
 * Chromium passa a confiar na chave desse proxy, informada em PROXY_SPKI. A
 * verificação de certificado continua ligada para todo o resto.
 *
 * Fora deste ambiente, sem as duas variáveis, nada disso é usado.
 */
import { execSync } from 'node:child_process';
const proxy = (process.env.HTTPS_PROXY ?? '').replace(/^http:\/\//, '').replace(/\/$/, '');
const spki = proxy && execSync("openssl x509 -in /root/.ccr/agent-proxy-ca.crt -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64").toString().trim();
const b = await chromium.launch(proxy ? { args: [`--proxy-server=https=${proxy}`, `--ignore-certificate-errors-spki-list=${spki}`] } : {});
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
const falhas = []; p.on('response', (r) => { if (r.url().includes('supabase') && r.status() >= 400) falhas.push(`${r.status()} ${r.url().split('/').slice(-2).join('/')}`); });
const passo = (t) => console.log(`▶ ${t}`);

await p.goto('http://localhost:5173/nexus-trios/', { waitUntil: 'networkidle' });
passo('abrir a tela de Conta');
await p.getByRole('button', { name: /conta/i }).first().click(); await p.waitForTimeout(800);
console.log('   aviso "não conectada" sumiu:', await p.getByText('ainda não foi conectada').count() === 0);
console.log('   botão do Google escondido:', await p.getByRole('button', { name: /Google/ }).count() === 0);

passo('entrar com e-mail e senha');
await p.getByPlaceholder('voce@exemplo.com').fill(email);
await p.getByPlaceholder('pelo menos 8 caracteres').fill(senha);
await p.locator('.account-formulario button.primary').click();
await p.waitForSelector('.account-cartao', { timeout: 20000 }).catch(() => {});
const logado = await p.locator('.account-cartao').count() > 0;
console.log('   entrou:', logado, '· nome na tela:', logado ? await p.locator('.account-identidade strong').innerText() : '—');
await p.screenshot({ path: `${SAIDA}/online-conta.png`, fullPage: true });

passo('senha errada mostra erro em português');
const p2 = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
await p2.goto('http://localhost:5173/nexus-trios/', { waitUntil: 'networkidle' });
await p2.getByRole('button', { name: /conta/i }).first().click(); await p2.waitForTimeout(600);
await p2.getByPlaceholder('voce@exemplo.com').fill(email);
await p2.getByPlaceholder('pelo menos 8 caracteres').fill('senhaerrada123');
await p2.locator('.account-formulario button.primary').click();
await p2.waitForSelector('.account-aviso.erro', { timeout: 20000 }).catch(() => {});
console.log('   mensagem:', await p2.locator('.account-aviso.erro').last().innerText().catch(() => '—'));
await p2.close();

passo('abrir o Ranking');
await p.getByRole('button', { name: /Abrir menu/i }).click().catch(() => {});
await p.getByRole('button', { name: /^Ranking$/ }).first().click(); await p.waitForTimeout(3500);
const linhas = await p.locator('.ranking-screen li, .ranking-screen tr, .leaderboard li, .leaderboard-row').allInnerTexts().catch(() => []);
console.log('   linhas do ranking:', linhas.slice(0, 3).map((l) => l.replace(/\s+/g, ' ').slice(0, 70)));
await p.screenshot({ path: `${SAIDA}/online-ranking.png`, fullPage: true });

console.log('\nfalhas de rede no Supabase:', falhas.length ? falhas : 'nenhuma');
console.log('erros de página:', erros.length ? erros : 'nenhum');
await b.close();
