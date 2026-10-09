/*
 * Calibra a dificuldade da campanha (src/engine/campaign.ts) para quem escolhe
 * bem: a chance de o "jogador bom" vencer cada luta segue ALVO (92% na
 * primeira, 55% no chefe), e ~10% das jornadas bem jogadas terminam campeãs.
 *
 * O jogador bom faz o draft de verdade (newDraft/pickDraft/skipDraft): pega o
 * candidato mais forte que combina com o trio (força medida + sinergia,
 * src/data/forca-dos-rivais.ts) e usa as trocas quando os candidatos são
 * fracos (o melhor fora dos 30% mais fortes). Cada luta é jogada por conta própria (não depende de ter vencido
 * a anterior).
 *
 * Para cada luta, procura por bissecção quantos trios sortear (o rival é o
 * mais forte deles: TRIOS_DA_LUTA / DIFICULDADE.triosDoChefe); se nem o
 * máximo basta, procura a Vida extra (ESCALAS); se até um trio sorteado ao
 * acaso é forte demais (começo da jornada), procura uma Vida menor que 1.
 *
 * Uso:
 *   npx tsx scripts/calibrar-dificuldade.ts luta <0-9> <jornadas>   (rode várias lutas em paralelo)
 *   npx tsx scripts/calibrar-dificuldade.ts medir <bom|aleatorio> <jornadas>
 */
import { characters } from '../src/data/characters';
import { FORCA } from '../src/data/forca-dos-rivais';
import { createBattle, stepBattle } from '../src/engine/battle';
import { DIFICULDADE, ESCALAS, TRIOS_DA_LUTA, forcaDoTrio, generateCampaign, newDraft, pickDraft, skipDraft } from '../src/engine/campaign';

/*
 * Chance de o jogador bom vencer cada luta. Pedido do jogador: ~10% das
 * jornadas bem jogadas terminam com as 10 vitórias — o produto das chances
 * (com quem chega longe sendo, em média, quem tem o trio melhor) dá isso.
 */
const ALVO = [0.92, 0.90, 0.88, 0.85, 0.82, 0.78, 0.72, 0.65, 0.57, 0.45];
const MAXIMO = 600;
const ids = characters.map((c) => c.id);
/* troca os candidatos quando o melhor deles não está entre os 30% mais fortes do elenco */
const CORTE = [...Object.values(FORCA)].sort((a, b) => a - b)[Math.floor(0.7 * Object.values(FORCA).length)] ?? 0;

export function trioDoJogadorBom(seed: number): string[] {
  let d = newDraft(seed);
  while (d.team.length < 3) {
    const nota = (id: string) => forcaDoTrio([...d.team, id]);
    const melhor = [...d.candidates].sort((a, b) => nota(b) - nota(a))[0]!;
    if ((FORCA[melhor] ?? 0) < CORTE && d.skips > 0) { d = skipDraft(d); continue; }
    d = pickDraft(d, melhor);
  }
  return d.team;
}
function jornadas(n: number, base: number, perfil: 'bom' | 'aleatorio') {
  let r = base >>> 0;
  const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
  return Array.from({ length: n }, () => {
    const seed = Math.floor(rnd() * 2 ** 31);
    if (perfil === 'bom') return { team: trioDoJogadorBom(seed), seed };
    const t = new Set<string>();
    while (t.size < 3) t.add(ids[Math.floor(rnd() * ids.length)]!);
    return { team: [...t], seed };
  });
}
function chance(lista: ReturnType<typeof jornadas>, luta: number) {
  let v = 0;
  for (const j of lista) {
    const e = generateCampaign(j.seed, j.team)[luta]!;
    const b = createBattle(j.team, e.team, j.seed + luta * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner === 'player') v++;
  }
  return v / lista.length;
}
const poe = (luta: number, k: number) => { if (luta < 9) TRIOS_DA_LUTA[luta] = k; else DIFICULDADE.triosDoChefe = k; };

const [modo, a, b] = process.argv.slice(2);
if (modo === 'luta') {
  const luta = Number(a), lista = jornadas(Number(b), 777 + luta * 31, 'bom');
  ESCALAS[luta] = 1; poe(luta, MAXIMO);
  if (chance(lista, luta) > ALVO[luta]!) {
    // nem o mais forte entre muitos basta: sobe a Vida
    let lo = 1, hi = 4;
    for (let passo = 0; passo < 8; passo++) { const m = (lo + hi) / 2; ESCALAS[luta] = m; if (chance(lista, luta) > ALVO[luta]!) lo = m; else hi = m; }
    ESCALAS[luta] = Math.round(((lo + hi) / 2) * 100) / 100;
  } else if ((poe(luta, 1), chance(lista, luta)) < ALVO[luta]!) {
    // até um trio sorteado ao acaso é forte demais para o começo: rivais com menos Vida
    let lo = 0.3, hi = 1;
    for (let passo = 0; passo < 8; passo++) { const m = (lo + hi) / 2; ESCALAS[luta] = m; if (chance(lista, luta) > ALVO[luta]!) lo = m; else hi = m; }
    ESCALAS[luta] = Math.round(((lo + hi) / 2) * 100) / 100;
  } else {
    let lo = 0, hi = Math.log(MAXIMO);
    for (let passo = 0; passo < 9; passo++) { const m = (lo + hi) / 2; poe(luta, Math.max(1, Math.round(Math.exp(m)))); if (chance(lista, luta) > ALVO[luta]!) lo = m; else hi = m; }
    poe(luta, Math.max(1, Math.round(Math.exp((lo + hi) / 2))));
  }
  const k = luta < 9 ? TRIOS_DA_LUTA[luta] : DIFICULDADE.triosDoChefe;
  console.log(JSON.stringify({ luta, trios: k, escala: ESCALAS[luta], chance: chance(lista, luta), alvo: ALVO[luta] }));
} else if (modo === 'medir') {
  const lista = jornadas(Number(b), 4242, a as 'bom' | 'aleatorio');
  console.log(a, ESCALAS.map((_, i) => Math.round(100 * chance(lista, i))).join(' '));
} else {
  console.error('uso: luta <0-9> <jornadas> | medir <bom|aleatorio> <jornadas>');
  process.exit(1);
}
