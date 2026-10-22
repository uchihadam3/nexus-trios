/*
 * Os textos do jogo sem tradução para o inglês: procura t('…'), tx('…') e plural(n, '…', '…') no código e confere o
 * dicionário (src/i18n/en.ts). Uso: npx tsx scripts/i18n-faltando.ts [--todos]   (com --todos, lista as chaves)
 * Também avisa traduções com {variáveis} diferentes das do português.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { EN } from '../src/i18n/en';

const arquivos: string[] = [];
const anda = (d: string) => { for (const n of readdirSync(d)) { const p = join(d, n); if (statSync(p).isDirectory()) anda(p); else if (/\.tsx?$/.test(n) && !p.includes('/i18n/')) arquivos.push(p); } };
anda('src');
const literal = String.raw`'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)"|` + '`((?:[^`\\\\$]|\\\\.)*)`';
const reT = new RegExp(String.raw`\btx?\(\s*(?:${literal})`, 'g');
const rePlural = new RegExp(String.raw`\bplural\([^,]+,\s*(?:${literal})\s*,\s*(?:${literal})`, 'g');
const desfaz = (s: string) => s.replace(/\\(['"`\\])/g, '$1').replace(/\\n/g, '\n');
const chaves = new Map<string, string>();
for (const f of arquivos) {
  const s = readFileSync(f, 'utf8');
  for (const m of s.matchAll(reT)) { const k = m[1] ?? m[2] ?? m[3]; if (k !== undefined) chaves.set(desfaz(k), f); }
  for (const m of s.matchAll(rePlural)) for (const k of [m[1] ?? m[2] ?? m[3], m[4] ?? m[5] ?? m[6]]) if (k !== undefined) chaves.set(desfaz(k), f);
}
const faltam = [...chaves].filter(([k]) => !(k in EN));
const vars = (s: string) => [...s.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort().join(',');
const erradas = Object.entries(EN).filter(([pt, en]) => vars(pt) !== vars(en));
console.log(`${chaves.size} textos com t(); ${faltam.length} sem tradução; ${Object.keys(EN).length} no dicionário; ${erradas.length} com variáveis diferentes`);
for (const [k, f] of faltam.slice(0, process.argv.includes('--todos') ? Infinity : 40)) console.log(`  ${f.replace('src/', '')}: ${JSON.stringify(k)}`);
for (const [pt, en] of erradas) console.log(`  variáveis: ${JSON.stringify(pt)} → ${JSON.stringify(en)}`);
if (faltam.length || erradas.length) process.exitCode = 1;
