/* Tocar num personagem e num Status na batalha, no celular em pé: o valor acumulado tem que aparecer. */
import { chromium } from 'playwright';
const SAIDA = process.env.SAIDA ?? './prints';
const URL = process.env.URL ?? 'http://localhost:4334';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
await p.goto(`${URL}/visual-probe.html?scenario=acumulo&phase=impact`, { waitUntil: 'networkidle' });
await p.waitForTimeout(1200);
/* Primeiro o personagem: a lista de Status embaixo mostra os valores. */
await p.locator('.fighter-name', { hasText: /Goku/ }).first().click({ force: true });
await p.waitForTimeout(500);
await p.locator('.battle-inspector').screenshot({ path: `${SAIDA}/status-personagem.png` });
const lista = await p.locator('.inspector-status').allInnerTexts();
console.log('lista:', JSON.stringify(lista));
/* Depois o Status: o número grande aparece. */
await p.locator('.inspector-status', { hasText: 'Exposto' }).click();
await p.waitForTimeout(500);
await p.locator('.battle-inspector').screenshot({ path: `${SAIDA}/status-exposto.png` });
console.log('valor:', await p.locator('.inspector-valor').innerText().catch(() => 'sem valor'));
await p.screenshot({ path: `${SAIDA}/status-tela.png` });
console.log('erros:', erros.length ? erros : 'nenhum');
await b.close();
/* E direto no ícone de um personagem seu: Sakura com Acelerado. */
const b2 = await chromium.launch();
const p2 = await b2.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await p2.goto(`${URL}/visual-probe.html?scenario=acumulo&phase=impact`, { waitUntil: 'networkidle' });
await p2.waitForTimeout(1200);
const icone = p2.locator('.status-badge[aria-label^="Acelerado"]').first();
console.log('ícone diz:', await icone.getAttribute('aria-label'));
await icone.click({ force: true });
await p2.waitForTimeout(500);
await p2.locator('.battle-inspector').screenshot({ path: `${SAIDA}/status-acelerado.png` });
console.log('valor seu:', await p2.locator('.inspector-valor').innerText().catch(() => 'sem valor'));
await b2.close();
