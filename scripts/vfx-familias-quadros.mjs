/*
 * Prova em movimento das famílias de efeito (adendo, parte 3): toca a
 * habilidade real de cada personagem em laço (visual-probe ?hab=id:i&play=1)
 * e fotografa a trajetória e o impacto.
 *
 * Uso: node scripts/vfx-familias-quadros.mjs <porta> [largura] [altura]
 *   HABS="goku:0,superman:0,..."  QUADROS=6  SAIDA=./prints
 */
import { chromium } from 'playwright';
const [porta = '4335', W = '390', H = '844'] = process.argv.slice(2);
const SAIDA = process.env.SAIDA ?? './prints';
const HABS = (process.env.HABS ?? 'goku:0').split(',');
const QUADROS = Number(process.env.QUADROS ?? 6);
const b = await chromium.launch();
for (const h of HABS) {
  const p = await b.newPage({ viewport: { width: Number(W), height: Number(H) }, deviceScaleFactor: Number(process.env.DPR ?? 1), isMobile: Number(W) < 1000, hasTouch: Number(W) < 1000 });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  await p.goto(`http://localhost:${porta}/visual-probe.html?hab=${h}&play=1`, { waitUntil: 'networkidle' });
  await p.waitForFunction(() => document.querySelector('.battle-screen')?.getAttribute('data-beat-id') === '1001', null, { timeout: 15000 });
  const basico = h.endsWith(':b');
  const dur = (basico ? 2.0 : 3.0) * 1000;
  /* quadros entre 25% e 85% do beat: a viagem, o impacto e o fim do impacto */
  const t0 = Date.now(); const familias = new Set();
  for (let i = 0; i < QUADROS; i += 1) {
    const alvo = dur * (0.25 + 0.6 * i / (QUADROS - 1));
    const espera = alvo - (Date.now() - t0); if (espera > 0) await p.waitForTimeout(espera);
    familias.add(await p.evaluate(() => document.querySelector('.battle-effects')?.getAttribute('data-familia')));
    await p.screenshot({ path: `${SAIDA}/vf-${h.replace(':', '_')}-${String(i).padStart(2, '0')}.png` });
  }
  console.log(h, [...familias].join(','), erros.length ? erros : 'ok');
  await p.close();
}
await b.close();
