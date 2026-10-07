/*
 * Prints da ficha de habilidade no celular, para comparar antes e depois.
 * Uso: node scripts/ficha-mobile.mjs <porta> <prefixo-dos-arquivos>
 *
 * Cada habilidade é fotografada sozinha e as fotos são empilhadas depois:
 * fotografar a ficha inteira de uma vez pega o que estiver atrás do modal
 * quando ela é mais alta que a tela.
 */
import { chromium } from 'playwright';
const [porta = '4331', prefixo = 'depois'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
await p.goto(`http://localhost:${porta}/nexus-trios/`, { waitUntil: 'networkidle' });
for (const nome of ['Naruto', 'Mulher-Maravilha', 'Ciclope', 'Shazam']) {
  await p.getByRole('button', { name: /^Personagens/ }).first().click().catch(async () => {
    await p.getByRole('button', { name: /Abrir menu/i }).click();
    await p.getByRole('button', { name: /^Personagens/ }).first().click();
  });
  await p.waitForTimeout(500);
  await p.getByPlaceholder('Buscar personagem…').fill(nome); await p.waitForTimeout(400);
  await p.locator('.roster-card').first().click(); await p.waitForTimeout(700);
  const artigos = p.locator('.detail-skills article');
  const n = await artigos.count();
  const slug = nome.toLowerCase().replace(/[^a-z]/g, '');
  for (let i = 0; i < n; i++) {
    await artigos.nth(i).scrollIntoViewIfNeeded(); await p.waitForTimeout(150);
    await artigos.nth(i).screenshot({ path: `${SAIDA}/${prefixo}-${slug}-${i}.png` });
  }
  const m = await p.evaluate(() => ({
    altura: Math.round([...document.querySelectorAll('.detail-skills article')].reduce((s, a) => s + a.getBoundingClientRect().height, 0)),
    rolaLateral: document.documentElement.scrollWidth > innerWidth + 1,
    vazando: [...document.querySelectorAll('.detail-skills *')].filter((e) => e.getBoundingClientRect().right > innerWidth + 1).length,
  }));
  console.log(`${nome.padEnd(17)} altura das 3 habilidades: ${m.altura}px · rola lateral: ${m.rolaLateral} · vazando: ${m.vazando}`);
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);
}
console.log('erros:', erros.length ? erros : 'nenhum');
await b.close();
