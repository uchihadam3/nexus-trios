/* O inspetor de habilidade dentro da batalha, no celular deitado e em pé. */
import { chromium } from 'playwright';
const SAIDA = process.env.SAIDA ?? './prints';
const b = await chromium.launch();
for (const [nome, w, h] of [['deitado', 844, 390], ['em-pe', 390, 844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  await p.goto('http://localhost:4334/visual-probe.html?scenario=basic', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  /* A terceira habilidade da Sakura tem efeitos em mais de um alvo. */
  await p.locator('.ability').nth(2).click({ force: true });
  await p.waitForTimeout(600);
  const insp = p.locator('.battle-inspector');
  const aberto = await insp.count() > 0;
  if (aberto) await insp.screenshot({ path: `${SAIDA}/inspetor-${nome}.png` });
  await p.screenshot({ path: `${SAIDA}/inspetor-${nome}-tela.png` });
  const m = await p.evaluate(() => {
    const i = document.querySelector('.battle-inspector'); if (!i) return null;
    const r = i.getBoundingClientRect();
    return { dentro: r.left >= 0 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1, grupos: i.querySelectorAll('.grupo-efeitos').length,
      rolaPorDentro: i.scrollHeight > i.clientHeight };
  });
  console.log(nome, aberto ? JSON.stringify(m) : 'inspetor não abriu', '· erros:', erros.length ? erros : 'nenhum');
  await p.close();
}
await b.close();
