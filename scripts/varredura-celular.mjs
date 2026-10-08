/*
 * FASE L · todas as telas do jogo no celular, em 360, 390 e 430 px.
 *
 * Em cada tela procura o que estraga o uso com o dedo: a página rolando para
 * o lado, elementos saindo da tela, e alvos de toque menores que 44 px (o
 * mínimo que um dedo acerta sem pegar o vizinho). Fotografa cada uma.
 *
 * Uso: node scripts/varredura-celular.mjs [url]   (SAIDA=pasta dos prints)
 * Sai com código 1 se encontrar rolagem lateral ou algo vazando.
 */
import { chromium } from 'playwright';
const URL_JOGO = process.argv[2] ?? 'http://localhost:5173/nexus-trios/';
const SAIDA = process.env.SAIDA ?? './prints/varredura';
const LARGURAS = (process.env.LARGURAS ?? "360,390,430").split(",").map(Number);

const irPeloMenu = (nome) => async (p) => {
  await p.getByRole('button', { name: /Abrir menu/i }).click().catch(() => {});
  await p.getByRole('button', { name: nome }).first().click();
};
const TELAS = [
  ['inicio', async () => {}],
  ['personagens', irPeloMenu(/^Personagens/)],
  ['ficha', async (p) => { await irPeloMenu(/^Personagens/)(p); await p.locator('.roster-card').first().click(); }],
  ['progresso', irPeloMenu(/^Progresso$/)],
  ['ranking', irPeloMenu(/^Ranking$/)],
  ['como-jogar', irPeloMenu(/^Como jogar$/)],
  ['configuracoes', irPeloMenu(/^Configurações$/)],
  ['conta', async (p) => { await p.getByRole('button', { name: /conta/i }).first().click(); }],
  ['montar-trio', async (p) => { await p.getByRole('button', { name: /Montar meu trio|Nova jornada/ }).first().click(); }],
];

const medir = (p) => p.evaluate(() => {
  const W = innerWidth, visivel = (e) => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  /* Dentro de algo que rola de lado de propósito (carrossel, abas), sair da tela é esperado. */
  const dentroDeRolagem = (e) => { for (let a = e.parentElement; a; a = a.parentElement) { const s = getComputedStyle(a); if (/(auto|scroll)/.test(s.overflowX) && a.scrollWidth > a.clientWidth) return true; } return false; };
  const classe = (e) => (e && typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const nome = (e) => `${e.parentElement ? classe(e.parentElement) + ' > ' : ''}${e.tagName.toLowerCase()}${classe(e)}${e.textContent?.trim() ? ` "${e.textContent.trim().slice(0, 22)}"` : ''}`;
  /* Recortado por um ancestral (moldura de retrato, carrossel): não aparece, não vaza. */
  const recortado = (e) => { for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const s = getComputedStyle(a); if (s.overflowX !== 'visible') { const r = a.getBoundingClientRect(); if (r.right <= W + 1 && r.left >= -1) return true; } } return false; };
  const vazando = [...document.querySelectorAll('body *')].filter((e) => visivel(e) && !dentroDeRolagem(e) && !recortado(e) && (e.getBoundingClientRect().right > W + 1 || e.getBoundingClientRect().left < -1))
    .filter((e) => !e.closest('[aria-hidden="true"]')).map(nome);
  const pequenos = [...document.querySelectorAll('button, a[href], input, select, textarea, [role="button"]')].filter(visivel)
    /* Dentro de um <label>, o alvo de toque é o label inteiro (a linha de um interruptor). */
    .filter((e) => { const r = (e.closest('label') ?? e).getBoundingClientRect(); return Math.min(r.width, r.height) < 44; })
    .map((e) => { const r = e.getBoundingClientRect(); return `${nome(e)} ${Math.round(r.width)}×${Math.round(r.height)}`; });
  return { rolaLateral: document.documentElement.scrollWidth > W + 1, vazando: [...new Set(vazando)], pequenos: [...new Set(pequenos)] };
});

const b = await chromium.launch();
let problemas = 0;
const resumo = [];
for (const largura of LARGURAS) {
  for (const [tela, ir] of TELAS) {
    const p = await b.newPage({ viewport: { width: largura, height: 800 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const erros = []; p.on('pageerror', (e) => erros.push(String(e).slice(0, 120)));
    await p.goto(URL_JOGO, { waitUntil: 'networkidle' });
    await p.evaluate(() => { try { localStorage.setItem('nexus-battle-guide-v1', '1'); } catch { /* */ } });
    try { await ir(p); } catch (e) { resumo.push(`${largura} ${tela}: NÃO CHEGOU (${String(e).split('\n')[0].slice(0, 80)})`); await p.close(); problemas++; continue; }
    await p.waitForTimeout(900);
    const m = await medir(p);
    await p.screenshot({ path: `${SAIDA}/${largura}-${tela}.png`, fullPage: true });
    const grave = m.rolaLateral || m.vazando.length || erros.length;
    if (grave) problemas++;
    resumo.push(`${largura} ${tela.padEnd(13)} ${grave ? '✗' : '✓'} lateral:${m.rolaLateral ? 'SIM' : 'não'} vazando:${m.vazando.length} toque<44:${m.pequenos.length}${erros.length ? ' ERROS:' + erros.join(';') : ''}`);
    for (const v of m.vazando.slice(0, 4)) resumo.push(`      vaza: ${v}`);
    for (const s of m.pequenos.slice(0, 6)) resumo.push(`      pequeno: ${s}`);
    await p.close();
  }
}
console.log(resumo.join('\n'));
console.log(problemas ? `\n${problemas} tela(s) com problema grave` : '\nnenhuma rolagem lateral, nada vazando, nenhum erro');
await b.close();
process.exit(problemas ? 1 : 0);
