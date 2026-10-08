/*
 * Quanto o jogo demora para abrir num celular comum: processador 4× mais
 * lento que o desta máquina e uma rede 4G razoável (9 Mbps, 120 ms). Mede três
 * vezes, sem cache, e fica com a mediana.
 *
 * Uso: node scripts/medir-carga-celular.mjs [url]
 */
import { chromium } from 'playwright';
const url = process.argv[2] ?? 'http://localhost:5173/nexus-trios/';
const b = await chromium.launch();
const medidas = [];
for (let i = 0; i < 3; i++) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
  const p = await ctx.newPage();
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 120, downloadThroughput: 9e6 / 8, uploadThroughput: 3e6 / 8 });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  let js = 0; p.on('response', async (r) => { if (r.url().endsWith('.js')) { try { js += (await r.body()).length; } catch { /* */ } } });
  const t0 = Date.now();
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  await p.getByRole('button', { name: /Montar meu trio|Nova jornada/ }).first().waitFor({ timeout: 60000 });
  const pronto = Date.now() - t0;
  const longas = await p.evaluate(() => new Promise((ok) => { let total = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) total += e.duration; }).observe({ type: 'longtask', buffered: true }); setTimeout(() => ok(total), 500); }));
  /* A tela dos 250: do toque até os cartões aparecerem. */
  const t1 = Date.now();
  await p.getByRole('button', { name: /^Personagens/ }).first().click().catch(async () => { await p.getByRole('button', { name: /Abrir menu/i }).click(); await p.getByRole('button', { name: /^Personagens/ }).first().click(); });
  await p.locator('.roster-card').first().waitFor();
  const roster = Date.now() - t1;
  const cartoes = await p.locator('.roster-card').count();
  medidas.push({ pronto, longas: Math.round(longas), roster, cartoes, js: Math.round(js / 1024) });
  await ctx.close();
}
const med = (k) => medidas.map((m) => m[k]).sort((a, b) => a - b)[1];
console.log(`jogo pronto para tocar: ${med('pronto')} ms (mediana de 3)`);
console.log(`travadas do processador na abertura: ${med('longas')} ms`);
console.log(`abrir "Personagens": ${med('roster')} ms · cartões montados de cara: ${medidas[0].cartoes}`);
console.log(`JavaScript baixado na abertura: ${medidas[0].js} KB (sem compressão)`);
await b.close();
