/*
 * Quantas imagens (e quantos bytes) o celular baixa ao abrir "Personagens",
 * sem rolar a tela. Com carregamento preguiçoso, só o que aparece deveria vir.
 */
import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
await p.goto('http://localhost:5173/nexus-trios/', { waitUntil: 'networkidle' });
let n = 0, bytes = 0;
p.on('response', async (r) => { if (/\.(png|jpe?g|webp)$/.test(r.url())) { n++; try { bytes += (await r.body()).length; } catch { /* */ } } });
await p.getByRole('button', { name: /Abrir menu/i }).click().catch(() => {});
await p.getByRole('button', { name: /^Personagens/ }).first().click();
await p.waitForLoadState('networkidle'); await p.waitForTimeout(1500);
console.log(`ao abrir "Personagens", sem rolar: ${n} imagens, ${(bytes / 1024 / 1024).toFixed(2)} MB`);
await b.close();
