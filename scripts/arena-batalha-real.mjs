/*
 * A arena numa batalha de verdade, no celular: monta um trio, entra na luta e
 * fotografa vários momentos; abre o inspetor, o histórico e os ajustes; volta
 * ao início e continua. Mede se algo rola, vaza ou fica pequeno demais.
 * Uso: node scripts/arena-batalha-real.mjs <url> [largura] [altura] [prefixo]
 */
import { chromium } from 'playwright';
const [URL_JOGO = 'http://localhost:4335/', W = '390', H = '844', prefixo = 'real'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: Number(W), height: Number(H) }, deviceScaleFactor: 2, isMobile: Number(W) < 1000, hasTouch: Number(W) < 1000 });
const erros = []; p.on('pageerror', (e) => erros.push(String(e).slice(0, 160)));
await p.goto(URL_JOGO, { waitUntil: 'networkidle' });
await p.evaluate(() => { try { localStorage.clear(); localStorage.setItem('nexus-battle-guide-v1', '1'); } catch { /* */ } });
await p.reload({ waitUntil: 'networkidle' });
await p.getByRole('button', { name: /Montar meu trio|Nova jornada/ }).first().click();
for (let i = 0; i < 3; i += 1) { await p.locator('.choose-button').first().click(); await p.waitForTimeout(250); }
await p.getByRole('button', { name: /Entrar na arena/ }).click();
await p.waitForSelector('.arena-v2', { timeout: 15000 });
const medir = () => p.evaluate(() => {
  const vis = (e) => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const root = document.querySelector('.arena-v2'), r = root.getBoundingClientRect();
  const fora = [...document.querySelectorAll('.arena-v2 .unit, .arena-v2 .arena-controls button, .arena-v2 .arena-hud > *')].filter(vis).filter((e) => { const q = e.getBoundingClientRect(); return q.left < -1 || q.right > innerWidth + 1 || q.top < -1 || q.bottom > innerHeight + 1; }).map((e) => e.className);
  return { rola: document.documentElement.scrollHeight > innerHeight + 1 || document.documentElement.scrollWidth > innerWidth + 1, arena: `${Math.round(r.width)}×${Math.round(r.height)}`, fora, medalhoes: [...document.querySelectorAll('.fighter-portrait')].map((e) => Math.round(e.getBoundingClientRect().width)) };
});
for (const [n, espera] of [['inicio', 600], ['meio', 9000], ['depois', 9000]]) {
  await p.waitForTimeout(espera);
  await p.screenshot({ path: `${SAIDA}/${prefixo}-${n}.png` });
  console.log(n, JSON.stringify(await medir()));
}
await p.locator('.arena-controls .control-main').click();
const hab = p.locator('.unit .ability').first();
await hab.click(); await p.waitForTimeout(400);
console.log('inspetor:', await p.locator('.battle-inspector').count(), '· pausado:', await p.locator('.paused-banner').count());
console.log('caixa do inspetor:', JSON.stringify(await p.evaluate(() => { const e = document.querySelector('.battle-inspector'); if (!e) return null; const r = e.getBoundingClientRect(), s = getComputedStyle(e); const no = document.elementFromPoint(r.left + r.width / 2, r.top + Math.min(20, r.height / 2)); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), opacity: s.opacity, vis: s.visibility, z: s.zIndex, topo: no?.className?.baseVal ?? no?.className }; })));
await p.screenshot({ path: `${SAIDA}/${prefixo}-inspetor.png` });
await p.keyboard.press('Escape'); await p.locator('.inspector-close').click().catch(() => {}); await p.waitForTimeout(300);
await p.locator('.history-button').click(); await p.waitForTimeout(300);
await p.screenshot({ path: `${SAIDA}/${prefixo}-historico.png` });
await p.locator('.history-button').click();
await p.locator('.mixer-button').click(); await p.waitForTimeout(300);
await p.screenshot({ path: `${SAIDA}/${prefixo}-ajustes.png` });
await p.locator('.mixer-button').click();
const voltar = p.locator('.hud-exit');
if (await voltar.count()) {
  await voltar.click(); await p.waitForTimeout(500);
  const naHome = await p.getByRole('button', { name: /Continuar jornada/ }).count();
  await p.getByRole('button', { name: /Continuar jornada/ }).first().click().catch(() => {});
  await p.waitForTimeout(800);
  console.log('voltar e continuar:', naHome ? 'ok' : 'botão de continuar não apareceu', '· arena de volta:', await p.locator('.arena-v2').count() ? 'sim' : 'não');
}
console.log('erros:', erros.length ? erros : 'nenhum');
await b.close();
