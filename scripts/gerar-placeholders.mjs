/*
 * Gera o retrato placeholder de cada personagem que ainda não tem arte final.
 *
 * O desenho é o mesmo que a expansão anterior já usava: um cartão com a cor do
 * personagem, uma silhueta neutra, a inicial e o nome. Não é arte final e não
 * pretende ser — é o que permite o catálogo crescer sem que a tela de
 * Personagens fique com buracos, e é substituído arquivo a arquivo conforme a
 * arte real chega.
 */
import { writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const destino = resolve(raiz, 'public/assets/portraits');
if (!existsSync(destino)) mkdirSync(destino, { recursive: true });

const { characters } = await import('../src/data/characters.ts');

const svg = (cor, inicial, nome) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="${cor}" stop-opacity=".42"/><stop offset="1" stop-color="#11131b"/></linearGradient></defs><rect width="240" height="300" rx="32" fill="url(#g)"/><circle cx="120" cy="112" r="76" fill="none" stroke="${cor}" stroke-opacity=".5" stroke-width="2"/><path d="M35 300l18-70 41-24 7-23h38l7 23 41 24 18 70" fill="${cor}" fill-opacity=".22"/><circle cx="120" cy="112" r="53" fill="${cor}" fill-opacity=".14"/><text x="120" y="137" text-anchor="middle" fill="${cor}" font-family="system-ui,sans-serif" font-weight="800" font-size="72">${inicial}</text><text x="120" y="276" text-anchor="middle" fill="#fff" fill-opacity=".88" font-family="system-ui,sans-serif" font-weight="700" font-size="17">${nome.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text></svg>`;

let criados = 0;
for (const c of characters) {
  if (!c.portrait.startsWith('/assets/portraits/placeholder-')) continue;
  const arquivo = resolve(raiz, 'public', c.portrait.slice(1));
  if (existsSync(arquivo)) continue;
  writeFileSync(arquivo, svg(c.color, c.symbol, c.name), 'utf8');
  criados += 1;
}
console.log(`retratos placeholder criados: ${criados}`);
