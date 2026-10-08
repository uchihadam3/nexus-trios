/*
 * Os efeitos de círculo (mira, impacto, chegada do apoio) ficam centrados no
 * medalhão? Numa luta real, mede durante alguns segundos a distância entre o
 * centro de cada efeito e o centro do medalhão mais próximo (sem a animação).
 * Uso: node scripts/efeitos-centrados.mjs <url> [largura] [altura]
 */
import { createHash, X509Certificate } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { chromium } from 'playwright';
const [URL_JOGO = 'http://localhost:4335/', W = '390', H = '844'] = process.argv.slice(2);
/* site publicado atrás do proxy do ambiente: confia só nas autoridades do proxy (veja arena-batalha-real.mjs) */
const remoto = !/localhost|127\.0\.0\.1/.test(URL_JOGO);
const confiarNoProxy = () => {
  const PACOTE = '/root/.ccr/ca-bundle.crt';
  if (!existsSync(PACOTE)) return [];
  const pems = readFileSync(PACOTE, 'utf8').match(/-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----/g) ?? [];
  const chaves = pems.map((pem) => new X509Certificate(pem)).filter((c) => /Anthropic/.test(c.subject)).map((c) => createHash('sha256').update(c.publicKey.export({ type: 'spki', format: 'der' })).digest('base64'));
  return chaves.length ? [`--ignore-certificate-errors-spki-list=${chaves.join(',')}`] : [];
};
const b = await chromium.launch(remoto && process.env.HTTPS_PROXY ? { channel: 'chromium', proxy: { server: process.env.HTTPS_PROXY }, args: confiarNoProxy() } : {});
const p = await b.newPage({ viewport: { width: Number(W), height: Number(H) }, isMobile: Number(W) < 1000, hasTouch: Number(W) < 1000 });
await p.goto(URL_JOGO, { waitUntil: 'networkidle' });
await p.evaluate(() => { try { localStorage.clear(); localStorage.setItem('nexus-battle-guide-v1', '1'); } catch { /* */ } });
await p.reload({ waitUntil: 'networkidle' });
await p.getByRole('button', { name: /Montar meu trio|Nova jornada/ }).first().click();
for (let i = 0; i < 3; i += 1) { await p.locator('.choose-button').first().click(); await p.waitForTimeout(250); }
await p.getByRole('button', { name: /Entrar na arena/ }).click();
await p.waitForSelector('.arena-v2', { timeout: 30000 });
const r = await p.evaluate(async () => {
  const arena = document.querySelector('.arena');
  const centroSemAnim = (el) => { let x = 0, y = 0, n = el; while (n && n !== arena) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; } const a = arena.getBoundingClientRect(); return { x: a.x + x + el.offsetWidth / 2, y: a.y + y + el.offsetHeight / 2 }; };
  const desvios = { mira: [], impacto: [], chegada: [] }; const fim = performance.now() + 14000;
  while (performance.now() < fim) {
    const medalhoes = [...document.querySelectorAll('.fighter-portrait')].map(centroSemAnim);
    for (const [tipo, sel] of [['mira', '.link-mira'], ['impacto', '.fxl-impacto:not(.fxl-acento)'], ['chegada', '.link-chegada']]) {
      for (const e of document.querySelectorAll(sel)) {
        const st = getComputedStyle(e); const cx = parseFloat(st.left), cy = parseFloat(st.top); const pai = e.offsetParent.getBoundingClientRect();
        const c = { x: pai.x + cx, y: pai.y + cy };
        const d = Math.min(...medalhoes.map(m => Math.hypot(m.x - c.x, m.y - c.y)));
        desvios[tipo].push(Math.round(d));
      }
    }
    await new Promise(r => setTimeout(r, 90));
  }
  const resumo = (v) => v.length ? { amostras: v.length, max: Math.max(...v), mediana: v.sort((a, b) => a - b)[Math.floor(v.length / 2)] } : null;
  return { mira: resumo(desvios.mira), impacto: resumo(desvios.impacto), chegada: resumo(desvios.chegada) };
});
console.log('desvio do centro (px):', JSON.stringify(r));
await b.close();
