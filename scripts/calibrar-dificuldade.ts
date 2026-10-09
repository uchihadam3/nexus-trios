/*
 * Calibra a dificuldade da campanha (src/engine/campaign.ts) para a chance de
 * vencer cada luta seguir a curva pedida pelo jogador: ~70% na primeira,
 * caindo até ~15% na décima.
 *
 * A Vida extra dos rivais (ESCALAS) é fixa e sobe devagar; o que se calibra
 * é a força do trio escolhido para cada luta (FORCA_DA_LUTA, lutas 1–9) e quantos
 * trios são sorteados para achar o chefe (DIFICULDADE.triosDoChefe).
 *
 * A chance é medida com trios do jogador sorteados, cada luta jogada por conta
 * própria (não depende de ter vencido a anterior), por bissecção, com as
 * mesmas jornadas em todos os passos.
 *
 * Uso:
 *   npx tsx scripts/calibrar-dificuldade.ts luta <0-8> <jornadas>   (imprime a força da luta; rode várias em paralelo)
 *   npx tsx scripts/calibrar-dificuldade.ts chefe <jornadas>        (imprime quantos trios sortear para o chefe)
 *   npx tsx scripts/calibrar-dificuldade.ts medir <jornadas>        (a chance de vencer cada luta com os valores atuais)
 */
import { characters } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { DIFICULDADE, ESCALAS, FORCA_DA_LUTA, generateCampaign } from '../src/engine/campaign';

const ALVO = [0.70, 0.64, 0.58, 0.52, 0.46, 0.40, 0.33, 0.27, 0.21, 0.12];
const ids = characters.map((c) => c.id);

function jornadas(n: number, base: number) {
  let r = base >>> 0;
  const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
  return Array.from({ length: n }, () => {
    const t = new Set<string>();
    while (t.size < 3) t.add(ids[Math.floor(rnd() * ids.length)]!);
    return { team: [...t], seed: Math.floor(rnd() * 2 ** 31) };
  });
}
function chance(lista: ReturnType<typeof jornadas>, luta: number) {
  let v = 0;
  for (const j of lista) {
    const e = generateCampaign(j.seed, j.team)[luta]!;
    const b = createBattle(j.team, e.team, j.seed + luta * 7919, ESCALAS[luta]);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner === 'player') v++;
  }
  return v / lista.length;
}

const [modo, a, b] = process.argv.slice(2);
if (modo === 'luta') {
  const luta = Number(a), lista = jornadas(Number(b), 777 + luta * 31);
  let lo = 0, hi = 1;
  for (let passo = 0; passo < 7; passo++) {
    const meio = (lo + hi) / 2; FORCA_DA_LUTA[luta] = meio;
    if (chance(lista, luta) > ALVO[luta]!) lo = meio; else hi = meio;
  }
  FORCA_DA_LUTA[luta] = Math.round(((lo + hi) / 2) * 100) / 100;
  console.log(JSON.stringify({ luta, forca: FORCA_DA_LUTA[luta], chance: chance(lista, luta), alvo: ALVO[luta] }));
} else if (modo === 'chefe') {
  const lista = jornadas(Number(a), 999);
  // em escala de log: 2, 4, 8… trios
  let lo = Math.log(2), hi = Math.log(3000);
  for (let passo = 0; passo < 8; passo++) {
    const meio = (lo + hi) / 2; DIFICULDADE.triosDoChefe = Math.round(Math.exp(meio));
    if (chance(lista, 9) > ALVO[9]!) lo = meio; else hi = meio;
  }
  DIFICULDADE.triosDoChefe = Math.round(Math.exp((lo + hi) / 2));
  console.log(JSON.stringify({ triosDoChefe: DIFICULDADE.triosDoChefe, chance: chance(lista, 9), alvo: ALVO[9] }));
} else if (modo === 'medir') {
  const lista = jornadas(Number(a), 4242);
  console.log(ESCALAS.map((_, i) => Math.round(100 * chance(lista, i))).join(' '));
} else {
  console.error('uso: luta <0-8> <jornadas> | chefe <jornadas> | medir <jornadas>');
  process.exit(1);
}
