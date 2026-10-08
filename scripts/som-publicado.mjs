/*
 * O som no site publicado: entra numa luta de verdade e confere que a música
 * (3 camadas) e os efeitos sonoros chegaram, sem erro. Mede pela rede, porque
 * o build publicado não expõe o mixer.
 * Uso: node scripts/som-publicado.mjs [url]
 */
import { createHash, X509Certificate } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { chromium } from 'playwright';
const PACOTE = '/root/.ccr/ca-bundle.crt';
const [URL_JOGO = 'http://localhost:4335/'] = process.argv.slice(2);
const remoto = !/localhost|127\.0\.0\.1/.test(URL_JOGO);
/* O proxy do ambiente reassina o TLS: o Chromium confia só nas autoridades dele (nunca desliga a verificação). */
const confiarNoProxy = () => {
  if (!existsSync(PACOTE)) return [];
  const pems = readFileSync(PACOTE, 'utf8').match(/-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----/g) ?? [];
  const chaves = pems.map((pem) => new X509Certificate(pem)).filter((c) => /Anthropic/.test(c.subject))
    .map((c) => createHash('sha256').update(c.publicKey.export({ type: 'spki', format: 'der' })).digest('base64'));
  return chaves.length ? [`--ignore-certificate-errors-spki-list=${chaves.join(',')}`] : [];
};
const b = await chromium.launch(remoto && process.env.HTTPS_PROXY ? { channel: 'chromium', proxy: { server: process.env.HTTPS_PROXY }, args: [...confiarNoProxy(), '--autoplay-policy=no-user-gesture-required'] } : { args: ['--autoplay-policy=no-user-gesture-required'] });
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = [], audio = new Map();
p.on('pageerror', (e) => erros.push(String(e).slice(0, 160)));
p.on('response', (r) => { const u = new URL(r.url()); if (u.pathname.includes('/assets/audio/')) audio.set(u.pathname.replace(/.*\/assets\/audio\//, ''), r.status()); });
await p.goto(URL_JOGO, { waitUntil: 'networkidle' });
await p.evaluate(() => { try { localStorage.clear(); localStorage.setItem('nexus-battle-guide-v1', '1'); } catch { /* */ } });
await p.reload({ waitUntil: 'networkidle' });
await p.getByRole('button', { name: /Montar meu trio|Nova jornada/ }).first().click();
for (let i = 0; i < 3; i += 1) { await p.locator('.choose-button').first().click(); await p.waitForTimeout(250); }
await p.getByRole('button', { name: /Entrar na arena/ }).click();
await p.waitForSelector('.arena-v2', { timeout: 15000 });
await p.locator('.arena-v2').click({ position: { x: 20, y: 300 } }).catch(() => {});
await p.waitForTimeout(14000);
const todos = [...audio.entries()];
const musica = todos.filter(([k]) => k.startsWith('musica-')), sfx = todos.filter(([k]) => k.startsWith('sfx/') && k.endsWith('.mp3'));
console.log(JSON.stringify({ musica, manifesto: audio.get('sfx/manifest.json'), sfxCarregados: sfx.length, sfxFalhas: sfx.filter(([, s]) => s !== 200), antigos: todos.filter(([k]) => /\.wav$|harmony|rhythm|pulse\.ogg|lead\.ogg/.test(k)), erros }, null, 1));
await b.close();
