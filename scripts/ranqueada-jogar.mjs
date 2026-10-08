/*
 * Uma Jornada Ranqueada inteira pela tela do jogo, contra o Supabase de
 * verdade: entra na conta, escolhe o trio, deixa as lutas correrem no
 * automático e espera o servidor validar.
 * Uso: node scripts/ranqueada-jogar.mjs <email> <senha>
 */
import { chromium } from 'playwright';
import { execSync } from 'node:child_process';
const [email, senha] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const proxy = (process.env.HTTPS_PROXY ?? '').replace(/^http:\/\//, '').replace(/\/$/, '');
const spki = proxy && execSync("openssl x509 -in /root/.ccr/agent-proxy-ca.crt -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64").toString().trim();
const b = await chromium.launch(proxy ? { args: [`--proxy-server=https=${proxy}`, `--ignore-certificate-errors-spki-list=${spki}`] } : {});
const p = await b.newPage({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
p.on('response', async (r) => {
  if (!r.url().includes('/functions/v1/ranked-api') || r.request().method() !== 'POST') return;
  const corpo = r.request().postDataJSON?.() ?? {};
  let resp = ''; try { resp = JSON.stringify(await r.json()).slice(0, 160); } catch { /* */ }
  console.log(`   [servidor] ${corpo.action} → ${r.status()} ${resp}`);
});
const botoes = async () => (await p.locator('button:visible').allInnerTexts()).map((t) => t.replace(/\s+/g, ' ').trim()).filter(Boolean).slice(0, 14).join(' | ');

await p.goto('http://localhost:5173/nexus-trios/', { waitUntil: 'networkidle' });
await p.evaluate(() => { localStorage.clear(); localStorage.setItem('nexus-battle-guide-v1', '1'); });
await p.reload({ waitUntil: 'networkidle' });

console.log('▶ entrar');
await p.getByRole('button', { name: /conta/i }).first().click(); await p.waitForTimeout(500);
await p.getByPlaceholder('voce@exemplo.com').fill(email);
await p.getByPlaceholder('pelo menos 8 caracteres').fill(senha);
await p.locator('.account-formulario button.primary').click();
await p.waitForSelector('.account-cartao', { timeout: 20000 });
await p.getByRole('button', { name: /Voltar|Início/ }).first().click().catch(() => {}); await p.waitForTimeout(600);

console.log('▶ início · botões:', await botoes());
await p.getByRole('button', { name: /Desafio diário/ }).first().click(); await p.waitForTimeout(3500);
console.log('▶ montar o trio');
for (let i = 0; i < 3; i++) {
  await p.getByRole('button', { name: 'Escolher', exact: true }).first().click(); await p.waitForTimeout(700);
}
await p.screenshot({ path: `${SAIDA}/rank-1.png` });
console.log('   botões:', await botoes());
let validado = null;
p.on('response', async (r) => {
  if (!r.url().includes('/functions/v1/ranked-api')) return;
  try { const j = await r.json(); if (j.verified || (r.request().postDataJSON?.()?.action === 'submit')) validado = { status: r.status(), ...j }; } catch { /* */ }
});
console.log('▶ entrar na arena e deixar correr');
await p.getByRole('button', { name: /Entrar na arena/ }).click();
const inicio = Date.now(); let ultimo = '';
const AVANCAR = /Próximo confronto|Continuar|Seguir|Próxima luta|Ver resultado|Avançar|Entrar na arena|Enviar|Finalizar/;
while (!validado && Date.now() - inicio < 15 * 60 * 1000) {
  await p.waitForTimeout(2500);
  /* Automático e 2x, sempre que a batalha os oferecer desligados. */
  const auto = p.locator('.auto-label input[type=checkbox]');
  if (await auto.count() && !(await auto.first().isChecked())) await auto.first().check().catch(() => {});
  const x2 = p.getByRole('button', { name: /^2x$|^2×$/ });
  if (await x2.count()) await x2.first().click().catch(() => {});
  const avancar = p.getByRole('button', { name: AVANCAR });
  if (await avancar.count()) { const t = (await avancar.first().innerText()).trim(); await avancar.first().click().catch(() => {}); console.log(`   ${Math.round((Date.now() - inicio) / 1000)}s · cliquei "${t}"`); }
  const tela = (await p.locator('h1:visible, h2:visible').first().innerText().catch(() => '')).trim();
  if (tela && tela !== ultimo) { ultimo = tela; console.log(`   ${Math.round((Date.now() - inicio) / 1000)}s · tela: ${tela.slice(0, 50)}`); }
}
await p.waitForTimeout(2000);
await p.screenshot({ path: `${SAIDA}/rank-fim.png` });
console.log('\n▶ resultado do servidor:', validado ? JSON.stringify(validado) : 'nenhum envio em 15 min');
console.log('   tela final · botões:', await botoes());
console.log('erros:', erros.length ? erros : 'nenhum');
await b.close();
