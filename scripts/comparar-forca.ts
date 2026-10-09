/*
 * A posição de força de cada personagem, antes e depois de uma mudança.
 *
 * Pedido do jogador: "sempre que mudar um personagem, me fala em que posição
 * de força ele estava e para qual posição passou". A posição vem da força
 * medida (src/data/forca-dos-rivais.ts, scripts/medir-forca.ts): 1º é o mais
 * forte dos 250.
 *
 * Uso:
 *   git show HEAD:src/data/forca-dos-rivais.ts > /tmp/forca-antes.ts   (antes de medir de novo)
 *   npx tsx scripts/comparar-forca.ts /tmp/forca-antes.ts [id …]       (sem ids: os que mais mudaram)
 */
import { readFileSync } from 'node:fs';
import { byId } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';

const [arquivo, ...ids] = process.argv.slice(2);
if (!arquivo) { console.error('uso: comparar-forca.ts <forca-antes.ts> [id …]'); process.exit(1); }
const texto = readFileSync(arquivo, 'utf8').split('PESO_DA_LIGACAO')[0]!;
const ANTES: Record<string, number> = Object.fromEntries([...texto.matchAll(/"([^"]+)": (-?[\d.]+),/g)].map((m) => [m[1]!, Number(m[2])]));
const posicoes = (f: Record<string, number>) => new Map(Object.entries(f).sort((a, b) => b[1] - a[1]).map(([id], i) => [id, i + 1]));
const antes = posicoes(ANTES), depois = posicoes(FORCA), total = depois.size;
const lista = ids.length ? ids : [...depois.keys()].sort((a, b) => Math.abs((antes.get(b) ?? 0) - (depois.get(b) ?? 0)) - Math.abs((antes.get(a) ?? 0) - (depois.get(a) ?? 0))).slice(0, 15);
for (const id of lista) {
  const a = antes.get(id), d = depois.get(id);
  const seta = a === undefined || d === undefined ? '' : d < a ? `subiu ${a - d}` : d > a ? `caiu ${d - a}` : 'igual';
  console.log(`${(byId[id]?.name ?? id).padEnd(24)} ${a ?? '—'}º → ${d ?? '—'}º de ${total}  (${seta})`);
}
