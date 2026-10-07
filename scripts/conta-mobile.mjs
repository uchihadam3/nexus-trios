import { chromium } from 'playwright';
const SAIDA = './prints';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const erros = [];
p.on('pageerror', e => erros.push(String(e)));

await p.goto('http://localhost:4319/nexus-trios/', { waitUntil: 'networkidle' });

/* Entrar pelo menu, como o jogador entra. */
const link = p.getByRole('button', { name: /conta/i }).first();
await link.click();
await p.waitForTimeout(900);

const medir = async (nome) => {
  await p.screenshot({ path: `${SAIDA}/${nome}.png`, fullPage: true });
  const m = await p.evaluate(() => ({
    rolaLateral: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    altura: document.documentElement.scrollHeight,
    vazando: [...document.querySelectorAll('.account-screen *')]
      .filter(e => e.getBoundingClientRect().right > innerWidth + 1 || e.getBoundingClientRect().left < -1)
      .map(e => e.className).slice(0, 4),
    alvosPequenos: [...document.querySelectorAll('.account-screen button, .account-screen input')]
      .filter(e => e.getBoundingClientRect().height < 44)
      .map(e => `${e.tagName}.${e.className}:${Math.round(e.getBoundingClientRect().height)}px`),
  }));
  console.log(`\n=== ${nome} ===`);
  console.log(`  rola lateral: ${m.rolaLateral} · altura: ${m.altura}px · vazando: ${m.vazando.length ? m.vazando.join(', ') : 'nada'}`);
  console.log(`  toque < 44px: ${m.alvosPequenos.length ? m.alvosPequenos.join(', ') : 'nenhum'}`);
};

await medir('conta-entrar');
await p.getByRole('button', { name: 'Criar conta', exact: true }).first().click();
await p.waitForTimeout(400);
await medir('conta-criar');
await p.getByRole('button', { name: /Esqueci a senha/i }).first().click();
await p.waitForTimeout(400);
await medir('conta-recuperar');

console.log('\nerros de página:', erros.length ? erros : 'nenhum');
await b.close();
