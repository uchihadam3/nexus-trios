import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
const habs=(process.env.HABS??'goku:0').split(',');
for (const hab of habs) {
  await p.goto(`http://localhost:4335/visual-probe.html?hab=${hab}&play=1`, { waitUntil: 'networkidle' });
  await p.waitForFunction(() => document.querySelector('.battle-screen')?.getAttribute('data-beat-id') === '1001');
  const t0=Date.now();
  for (const [i,t] of [[0,250],[1,550],[2,850],[3,1150],[4,1650],[5,2100]]) { const w=t-(Date.now()-t0); if(w>0) await p.waitForTimeout(w); await p.screenshot({ path: `prints/lin-${hab.replace(':','_')}-${i}.png` }); }
}
await b.close();
