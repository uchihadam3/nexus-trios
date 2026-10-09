/*
 * Mede quantos pontos de feitos cada personagem faz numa luta vencida típica
 * (sem fator) e grava o fator que traz todos para a mesma média.
 *
 * Pedido do jogador: "os pontos têm que ser balanceados para que todos os
 * personagens que jogarem bem possam pontuar parecido". Um kit de controle,
 * investigação ou apoio gera menos número visível que um de dano puro; o
 * fator corrige isso (entre ×0,5 e ×2), e o personagem que joga acima do seu
 * normal continua pontuando mais.
 *
 * Uso: npx tsx scripts/equilibrar-pontos.ts   (escreve src/data/pontos-por-personagem.ts)
 */
import { writeFileSync } from 'node:fs';
import { characters } from '../src/data/characters';
import { generateCampaign } from '../src/engine/campaign';
import { createBattle, stepBattle } from '../src/engine/battle';
import { feitosDoLutador } from '../src/engine/pontos';

const MIN = 0.5, MAX = 2, AMOSTRAS = 12;
const soma: Record<string, { n: number; p: number }> = {};
const ids = characters.map((c) => c.id);
const conta = (id: string) => soma[id]?.n ?? 0;
function joga(trio: string[], seed: number) {
  for (const [i, e] of generateCampaign(seed, trio).entries()) {
    if (i > 4) break;
    const b = createBattle(trio, e.team, seed + i * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner !== 'player') break;
    for (const f of b.fighters.filter((x) => x.side === 'player')) {
      const x = feitosDoLutador(f), a = (soma[f.characterId] ??= { n: 0, p: 0 });
      a.n++; a.p += Object.values(x).reduce((n, v) => n + v, 0);
    }
  }
}
// trios variados; depois, quem ainda tem poucas lutas vencidas joga mais
for (let seed = 1; seed <= 700; seed++) {
  const rivais = new Set(generateCampaign(seed).flatMap((e) => e.team)), l = ids.filter((i) => !rivais.has(i));
  const trio = [l[(seed * 7) % l.length]!, l[(seed * 13 + 5) % l.length]!, l[(seed * 29 + 11) % l.length]!];
  if (new Set(trio).size === 3) joga(trio, seed);
}
for (let rodada = 0; rodada < 16; rodada++) for (const [k, id] of ids.entries()) {
  if (conta(id) >= AMOSTRAS) continue;
  const seed = 9000 + rodada * 997 + k, rivais = new Set(generateCampaign(seed).flatMap((e) => e.team));
  if (rivais.has(id)) continue;
  const l = ids.filter((i) => !rivais.has(i) && i !== id);
  joga([id, l[(seed * 7) % l.length]!, l[(seed * 13 + 5) % l.length]!].filter((x, i, a) => a.indexOf(x) === i), seed);
}
const medias = Object.fromEntries(Object.entries(soma).filter(([, a]) => a.n >= 4).map(([k, a]) => [k, a.p / a.n]));
const valores = Object.values(medias), alvo = valores.reduce((a, b) => a + b, 0) / valores.length;
const fator = Object.fromEntries(Object.entries(medias).sort(([a], [b]) => a.localeCompare(b))
  .map(([k, m]) => [k, Math.round(Math.max(MIN, Math.min(MAX, alvo / m)) * 100) / 100]));
const corpo = Object.entries(fator).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n');
writeFileSync(new URL('../src/data/pontos-por-personagem.ts', import.meta.url), `/*
 * O fator de pontos de cada personagem — gerado por scripts/equilibrar-pontos.ts
 * (média de ${Math.round(alvo)} pontos de feitos por luta vencida, fator entre ×${MIN} e ×${MAX}).
 * Não editar à mão: rode o script de novo depois de mudar o elenco ou os pesos.
 * Quem não aparece aqui (poucas lutas medidas) usa ×1.
 */
export const FATOR_DE_PONTOS: Record<string, number> = {
${corpo}
};
`);
const semMedida = ids.filter((i) => !(i in fator));
console.log(`fatores: ${Object.keys(fator).length} · sem medida: ${semMedida.join(', ') || 'nenhum'} · alvo ${Math.round(alvo)}`);
