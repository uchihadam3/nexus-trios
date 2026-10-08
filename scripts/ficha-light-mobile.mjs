/* A ficha do Light no celular: o quadro da investigação e a Death Note. Uso: node scripts/ficha-light-mobile.mjs <porta> */
import { chromium } from 'playwright';
const [porta = '4334'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
await p.goto(`http://localhost:${porta}/nexus-trios/`, { waitUntil: 'networkidle' });
await p.getByRole('button', { name: /^Personagens/ }).first().click().catch(async () => {
  await p.getByRole('button', { name: /Abrir menu/i }).click();
  await p.getByRole('button', { name: /^Personagens/ }).first().click();
});
await p.waitForTimeout(500);
await p.getByPlaceholder('Buscar personagem…').fill('Light'); await p.waitForTimeout(400);
await p.locator('.roster-card').first().click(); await p.waitForTimeout(700);
const quadro = p.locator('.vulnerability', { hasText: 'Como funciona a investigação' });
await quadro.scrollIntoViewIfNeeded(); await quadro.screenshot({ path: `${SAIDA}/light-investigacao.png` });
const artigos = p.locator('.detail-skills article');
for (let i = 0; i < await artigos.count(); i++) {
  await artigos.nth(i).scrollIntoViewIfNeeded(); await p.waitForTimeout(150);
  await artigos.nth(i).screenshot({ path: `${SAIDA}/light-habilidade-${i}.png` });
}
console.log((await quadro.innerText()).replace(/\n/g, ' '));
console.log((await artigos.nth(2).innerText()).replace(/\n+/g, ' · '));
console.log('rola lateral:', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), '· erros:', erros.length ? erros : 'nenhum');
await b.close();
