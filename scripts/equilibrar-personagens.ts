/*
 * Aproxima a força dos 250 personagens (pedido do jogador: "nenhum personagem
 * tão ruim que com ele você nunca vence as 10, e nenhum tão forte que com ele
 * qualquer dupla vence").
 *
 * Lê a força medida (src/data/forca-dos-rivais.ts, de scripts/medir-forca.ts,
 * medida já com os ajustes atuais) e corrige o multiplicador de cada um
 * (src/data/ajuste-de-forca.ts, que escala Vida, dano, cura e escudo) para a
 * força cair perto de ALVO × força original (sem ajuste) — os fortes descem,
 * os fracos sobem, a ordem entre eles se mantém. Rode em rodadas: medir → equilibrar → medir…
 *
 * Uso: npx tsx scripts/equilibrar-personagens.ts
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';
import { AJUSTE_DE_FORCA, AJUSTE_DE_RITMO } from '../src/data/ajuste-de-forca';

/** quanto da distância para a média sobra (0,5 = cada um fica com metade da diferença que tinha sem ajuste) */
const ALVO = Number(process.env.ALVO ?? 0.5);
/*
 * A força de cada um SEM ajuste (a primeira medição), para o alvo não andar a
 * cada rodada: alvo = ALVO × força original. Pedido do jogador: escolher bem
 * tem que pesar — os fortes continuam mais fortes, só que ninguém quebrado.
 */
const ORIGINAL: Record<string, number> = Object.fromEntries([...readFileSync(new URL('./forca-original.txt', import.meta.url), 'utf8').matchAll(/"([^"]+)": (-?[\d.]+),/g)].map((m) => [m[1]!, Number(m[2])]));
/** força ganha por personagem a cada ×e no multiplicador (medida entre rodadas) */
const BETA = Number(process.env.BETA ?? 0.9);
const PASSO = Number(process.env.PASSO ?? 0.85), MIN = 0.5, MAX = 3;

const novo: Record<string, number> = {};
let maior = 0;
for (const c of characters) {
  const f = FORCA[c.id] ?? 0, alvo = ALVO * (ORIGINAL[c.id] ?? 0), m = AJUSTE_DE_FORCA[c.id] ?? 1;
  const ln = Math.log(m) + PASSO * (alvo - f) / BETA;
  const v = Math.round(Math.max(MIN, Math.min(MAX, Math.exp(ln))) * 100) / 100;
  novo[c.id] = v; maior = Math.max(maior, Math.abs(alvo - f));
}
const linhas = Object.entries(novo).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
writeFileSync(new URL('../src/data/ajuste-de-forca.ts', import.meta.url), `/*
 * Ajuste de força de cada personagem — gerado por scripts/equilibrar-personagens.ts.
 * Multiplica a Vida e o que ele produz (dano, cura, escudo, energia guardada).
 * 1 = sem ajuste. Não editar à mão.
 */
export const AJUSTE_DE_FORCA: Record<string, number> = {
${linhas}
};

/**
 * Ritmo (× no intervalo entre ações; < 1 = mais rápido), só para quem tem a força
 * no controle e na investigação e não sobe o bastante só com Vida e dano. Ajustado à mão.
 */
export const AJUSTE_DE_RITMO: Record<string, number> = ${JSON.stringify(AJUSTE_DE_RITMO, null, 2).replace(/\n}$/, ',\n}')};
`);
const vs = Object.values(novo).sort((a, b) => a - b);
console.log('maior distância do alvo', maior.toFixed(2), 'multiplicadores min/med/max', vs[0], vs[125], vs[249]);
