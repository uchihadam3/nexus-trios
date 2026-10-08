/*
 * Prova em movimento: toca cada tipo de ação em laço (visual-probe ?play=1) e
 * tira uma sequência de quadros, montada depois numa tira por ação.
 * Uso: node scripts/atuacao-quadros.mjs <porta> [largura] [altura]
 */
import { chromium } from 'playwright';
const [porta = '4335', W = '390', H = '844'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const CENARIOS = (process.env.CENARIOS ?? 'basic,energy,heal,buff,debuff,interrupt,aoe,ko').split(',');
const QUADROS = Number(process.env.QUADROS ?? 8);
const b = await chromium.launch();
for (const c of CENARIOS) {
  const p = await b.newPage({ viewport: { width: Number(W), height: Number(H) }, deviceScaleFactor: 1, isMobile: Number(W) < 1000, hasTouch: Number(W) < 1000 });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  await p.goto(`http://localhost:${porta}/visual-probe.html?scenario=${c}&play=1`, { waitUntil: 'networkidle' });
  /* espera o laço recomeçar, para pegar a ação desde o início */
  await p.waitForFunction(() => document.querySelector('.battle-screen')?.getAttribute('data-beat-id') === '1001', null, { timeout: 15000 });
  const dur = c === 'basic' || c === 'energy' ? 2.0 : 3.0;
  const t0 = Date.now();
  for (let i = 0; i < QUADROS; i += 1) {
    const alvo = (i / (QUADROS - 1)) * dur * 1000 * 0.92;
    const espera = alvo - (Date.now() - t0); if (espera > 0) await p.waitForTimeout(espera);
    await p.screenshot({ path: `${SAIDA}/q-${c}-${String(i).padStart(2, '0')}.png` });
  }
  console.log(c, erros.length ? erros : 'ok');
  await p.close();
}
await b.close();
