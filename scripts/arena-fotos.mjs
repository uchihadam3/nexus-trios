/*
 * Fotos da arena de batalha em todos os tamanhos que importam, para comparar
 * antes e depois. Uso: node scripts/arena-fotos.mjs <porta> <prefixo>
 */
import { chromium } from 'playwright';
const [porta = '4335', prefixo = 'antes'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const TELAS = [['360', 360, 780, true], ['390', 390, 844, true], ['430', 430, 932, true], ['deitado', 844, 390, true], ['desktop', 1280, 800, false]];
const CENARIOS = (process.env.CENARIOS ?? 'acumulo,basic').split(',');
const b = await chromium.launch();
for (const cenario of CENARIOS) for (const [nome, w, h, mobile] of TELAS) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: mobile, hasTouch: mobile });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  await p.goto(`http://localhost:${porta}/visual-probe.html?scenario=${cenario}&phase=impact`, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  await p.screenshot({ path: `${SAIDA}/${prefixo}-${cenario}-${nome}.png` });
  const m = await p.evaluate(() => ({
    rolaLateral: document.documentElement.scrollWidth > innerWidth + 1,
    alturaTotal: document.documentElement.scrollHeight,
    alvosPequenos: [...document.querySelectorAll('button')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.width < 44 || r.height < 44) && !e.closest('[hidden]'); }).length,
  }));
  console.log(`${cenario} ${nome}: ${JSON.stringify(m)} erros: ${erros.length}`);
  await p.close();
}
await b.close();
