/*
 * Fábrica de simulação: lutas em lote, para medir força solo, de dupla e de
 * trio com milhões de lutas (.github/workflows/fabrica.yml roda 20 máquinas
 * × 4 processos em paralelo).
 *
 * É o motor do jogo, sem tirar nada: a CI empacota este arquivo com esbuild
 * (sem o ajudante __name do tsx, ~1,4× mais rápido) e o resultado de cada
 * luta é o mesmo de simulate().
 *
 * Uso: node lutas.mjs <plano> <parte> <partes> <lutas> <saida.txt> [semente]
 *   aleatorio  trio aleatório contra trio aleatório
 *   pares      cada dupla possível (79.800 com 400) com um terceiro aleatório,
 *              contra um trio aleatório; as duplas são divididas entre as partes
 *   jornada    trio aleatório jogando a jornada inteira (10 lutas, como o jogador)
 *   dificuldade  para cada personagem da parte, <lutas> jornadas com parceiros
 *              aleatórios, com o trio que um jogador bom montaria e com o melhor
 *              trio achado entre os mais fortes (as metas de equilíbrio)
 *
 *   pontos     trio sorteado jogando a jornada inteira, com os pontos da jornada (a conta do jogo, sem dicas e sem
 *              o bônus das estrelas: os pontos naturais do trio);
 *              com FORTES, o trio é sorteado só entre esses ids (para medir uma lista de candidatos)
 * Cada linha (lutas): a1 a2 a3 b1 b2 b3 v (índices do elenco; v = 1 se o trio a venceu).
 * Cada linha (pontos): a1 a2 a3 v pontos (v = lutas vencidas, 0 a 10).
 * Cada linha (jornada): a1 a2 a3 v (v = lutas vencidas, 0 a 10).
 *   trios        TODOS os trios do elenco, um lote de 1 milhão por rodada (semente = número do lote, 0 a 10):
 *              cada trio faz <lutas> lutas contra trios sorteados (pedido do jogador: "pega 1 milhão de
 *              trios e faz os testes com eles… até terminar")
 * Cada linha (dificuldade): JSON {id, aleatorio, bom, melhor, dupla}.
 * Cada linha (trios): i j k v (índices do trio; v = lutas vencidas de <lutas>).
 *   estrelas   PvP por estrela (pedido do dono: "um time 5 estrelas não pode perder para um 3 estrelas"): cada parte monta
 *              trios de 1 a 5 estrelas (a força do PvP, estrelasDoTime) e os põe para lutar em todas as combinações
 *              de estrelas, trocando o lado a cada luta
 * Cada linha (estrelas): ea eb a1 a2 a3 b1 b2 b3 v (estrelas dos dois trios; v = 1 se o trio a venceu).
 *   estrelas-jornada  um trio de cada estrela jogando a jornada inteira, com a regra "Vida acima do topo" em
 *              várias forças ao mesmo tempo (VIDAS), para escolher a que deixa mais estrelas = mais vitórias
 * Cada linha (estrelas-jornada): e acima v0 v1 v2 … a1 a2 a3 (v = lutas vencidas com cada força de VIDAS).
 * A primeira linha (# ...) diz o motor e o elenco, para não misturar medidas.
 */
import { writeFileSync, appendFileSync } from 'node:fs';
import { characters } from '../../src/data/characters';
import { createBattle, stepBattle } from '../../src/engine/battle';
import { ENGINE_VERSION, rosterFingerprint } from '../../src/engine/ranked';
import { ESCALAS, VIDA_ACIMA_DO_TOPO, forcaDoTrio, generateCampaign, newDraft, pickDraft, skipDraft } from '../../src/engine/campaign';
import { estrelasDoTime, notaDoTrio } from '../../src/presentation/dicas-do-trio';
import { combosDoTrio } from '../../src/engine/combos';
import { pontosDaLuta } from '../../src/engine/pontos';
import { FORCA } from '../../src/data/forca-dos-rivais';
import CANDIDATOS from './candidatos-do-melhor.json';

const [plano, parteTxt, partesTxt, lutasTxt, saida, sementeTxt = '0'] = process.argv.slice(2);
const parte = Number(parteTxt), partes = Number(partesTxt), lutas = Number(lutasTxt), semente = Number(sementeTxt), semente0 = semente;
if (!plano || !saida || !(partes > 0) || !(parte >= 0 && parte < partes) || !(lutas > 0)) {
  console.error('uso: lutas <aleatorio|pares|jornada|dificuldade|trios|pontos> <parte> <partes> <lutas> <saida.txt> [semente]');
  process.exit(1);
}
const N = characters.length;
let r = (Math.imul(parte + 1, 2654435761) ^ Math.imul(semente + 7, 40503) ^ (plano === 'pares' ? 0x9e3779b9 : 0)) >>> 0;
const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
const LOTE_DE_TRIOS = 1_000_000;
/* As forças da regra "Vida acima do topo" testadas juntas (a de agora é VIDA_ACIMA_DO_TOPO). */
const VIDAS = [0, 0.1, 0.2, 0.3, 0.4, VIDA_ACIMA_DO_TOPO];
const sorteia = (fora: Set<number>) => { let i: number; do i = Math.floor(rnd() * N); while (fora.has(i)); fora.add(i); return i; };

/* As duplas desta parte (pares): a k-ésima dupla da lista vai para a parte k % partes. */
const duplas: [number, number][] = [];
if (plano === 'pares') { let k = 0; for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++, k++) if (k % partes === parte) duplas.push([i, j]); }
else if (!['aleatorio', 'jornada', 'dificuldade', 'trios', 'pontos', 'estrelas', 'estrelas-jornada'].includes(plano)) { console.error(`plano desconhecido: ${plano}`); process.exit(1); }

writeFileSync(saida, `# motor ${ENGINE_VERSION} elenco ${rosterFingerprint()} plano ${plano} parte ${parte}/${partes} semente ${semente}\n`);
if (plano === 'jornada' || plano === 'dificuldade' || plano === 'trios' || plano === 'pontos' || plano === 'estrelas' || plano === 'estrelas-jornada') { ({ jornada: jornadas, dificuldade, trios, pontos, estrelas, 'estrelas-jornada': estrelasJornada })[plano](); process.exit(0); }
let buffer = '', feitas = 0;
const inicio = Date.now();
for (let n = 0; n < lutas; n++) {
  const usados = new Set<number>();
  let a: number[];
  if (plano === 'pares') { const [x, y] = duplas[n % duplas.length]!; usados.add(x); usados.add(y); a = [x, y, sorteia(usados)]; }
  else a = [sorteia(usados), sorteia(usados), sorteia(usados)];
  const b = [sorteia(usados), sorteia(usados), sorteia(usados)];
  const batalha = createBattle(a.map((i) => characters[i]!.id), b.map((i) => characters[i]!.id), Math.floor(rnd() * 2 ** 31), 1);
  for (let t = 0; t < 9000 && !batalha.finished; t++) stepBattle(batalha);
  if (!batalha.finished) continue;
  buffer += `${a.join(' ')} ${b.join(' ')} ${batalha.winner === 'player' ? 1 : 0}\n`;
  if (++feitas % 1000 === 0) { appendFileSync(saida, buffer); buffer = ''; }
  if (n % 5000 === 4999) console.log(`parte ${parte}: ${n + 1}/${lutas} lutas · ${((n + 1) / ((Date.now() - inicio) / 1000)).toFixed(0)}/s`);
}
appendFileSync(saida, buffer);
console.log(`parte ${parte}: pronto, ${feitas} lutas em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);

/* Os trios do lote `semente` (o g-ésimo trio na ordem i < j < k), divididos entre as partes; cada um faz `lutas` lutas. */
function trios() {
  const de = semente * LOTE_DE_TRIOS, ate = de + LOTE_DE_TRIOS;
  let g = 0, buf = '', feitos = 0;
  const inicio = Date.now();
  for (let i = 0; i < N && g < ate; i++) for (let j = i + 1; j < N && g < ate; j++) {
    const nk = N - j - 1;
    if (g + nk <= de) { g += nk; continue; }
    for (let k = j + 1; k < N; k++, g++) {
      if (g < de || g >= ate || g % partes !== parte) continue;
      let v = 0;
      for (let n = 0; n < lutas; n++) {
        const fora = new Set([i, j, k]), b = [sorteia(fora), sorteia(fora), sorteia(fora)];
        const luta = createBattle([i, j, k].map((x) => characters[x]!.id), b.map((x) => characters[x]!.id), Math.floor(rnd() * 2 ** 31), 1);
        for (let t = 0; t < 9000 && !luta.finished; t++) stepBattle(luta);
        if (luta.winner === 'player') v++;
      }
      buf += `${i} ${j} ${k} ${v}\n`;
      if (++feitos % 500 === 0) { appendFileSync(saida, buf); buf = ''; }
      if (feitos % 2500 === 0) console.log(`parte ${parte}: ${feitos} trios · ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
    }
  }
  appendFileSync(saida, buf);
  console.log(`parte ${parte}: pronto, ${feitos} trios do lote ${semente}`);
}
/* A jornada inteira, como o jogador joga: quantas das 10 lutas o trio vence. */
function jornada(team: string[], seed: number) {
  for (const [i, e] of generateCampaign(seed, team).entries()) {
    const b = createBattle(team, e.team, seed + i * 7919, e.scale);
    for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
    if (b.winner !== 'player') return i;
  }
  return 10;
}
/* A jornada com os pontos dela: soma os pontos de cada luta jogada (também a da derrota), como o jogo. */
function pontos() {
  const ids = characters.map((c) => c.id);
  const pool = process.env.FORTES ? process.env.FORTES.split(',').filter((x) => ids.includes(x)) : ids;
  let buf = '';
  for (let n = 0; n < lutas; n++) {
    const team: string[] = [];
    while (team.length < 3) { const id = pool[Math.floor(rnd() * pool.length)]!; if (!team.includes(id)) team.push(id); }
    const seed = Math.floor(rnd() * 2 ** 31);
    let soma = 0, v = 0;
    for (const [i, e] of generateCampaign(seed, team).entries()) {
      const b = createBattle(team, e.team, seed + i * 7919, e.scale);
      for (let t = 0; t < 9000 && !b.finished; t++) stepBattle(b);
      // os pontos naturais do trio: sem o bônus das estrelas (src/data/estrelas-de-pontos.ts), que é o que se mede
      const luta = pontosDaLuta(b, i, false);
      soma += Math.max(0, luta.total - (luta.parcelas.find((p) => p.id === 'estrela')?.valor ?? 0));
      if (b.winner !== 'player') break;
      v++;
    }
    buf += `${team.map((id) => ids.indexOf(id)).join(' ')} ${v} ${Math.round(soma)}\n`;
    if (n % 200 === 199) { appendFileSync(saida, buf); buf = ''; console.log(`parte ${parte}: ${n + 1}/${lutas} jornadas`); }
  }
  appendFileSync(saida, buf);
}
function jornadas() {
  let buf = '';
  for (let n = 0; n < lutas; n++) {
    const usados = new Set<number>(), a = [sorteia(usados), sorteia(usados), sorteia(usados)];
    buf += `${a.join(' ')} ${jornada(a.map((i) => characters[i]!.id), Math.floor(rnd() * 2 ** 31))}\n`;
    if (n % 200 === 199) { appendFileSync(saida, buf); buf = ''; console.log(`parte ${parte}: ${n + 1}/${lutas} jornadas`); }
  }
  appendFileSync(saida, buf);
}
/*
 * As metas de equilíbrio por personagem (pedido do jogador: aleatório 0,5–9,9%, bom 10–35%, melhor 15–70%):
 *   aleatório — X com dois parceiros sorteados;
 *   bom — o trio que um jogador bom montaria em volta de X na escolha (pela nota, procurando combo);
 *   melhor — os 20 trios com X que mais venceram de verdade no plano trios (candidatos-do-melhor.json: todos os
 *   10,6 milhões de trios, a sorte de 10 lutas descontada) e mais os 20 da busca pela nota (as 10 duplas de nota mais
 *   alta entre os mais fortes — FORTES — e os do mesmo universo, e 10 sorteadas um pouco abaixo), peneirados em
 *   jornadas, e o vencedor medido em jornadas novas.
 */
function dificuldade() {
  const ids = characters.map((c) => c.id), NJ = lutas;
  const fortes = process.env.FORTES ? process.env.FORTES.split(',').filter((x) => ids.includes(x))
    : [...ids].sort((a, b) => (FORCA[b] ?? 0) - (FORCA[a] ?? 0)).slice(0, 40);
  const semente = (j: number) => (Math.imul(j + 1 + semente0 * 100003, 2654435761) >>> 1) & 0x7fffffff;
  const corte = [...Object.values(FORCA)].sort((a, b) => a - b)[Math.floor(0.6 * Object.values(FORCA).length)] ?? 0;
  const combos = (t: string[]) => (t.length < 2 ? 0 : combosDoTrio(t).combos.length);
  const trioBom = (x: string, seed: number) => {
    let d = newDraft(seed); d = { ...d, team: [x] }; d.candidates = d.candidates.filter((c) => c !== x);
    if (d.candidates.length < 3) d = skipDraft(d);
    while (d.team.length < 3) {
      const nota = (id: string) => forcaDoTrio([...d.team, id]);
      const melhor = [...d.candidates].filter((c) => c !== x).sort((a, b) => nota(b) - nota(a))[0];
      if (!melhor) { if (d.skips <= 0) break; d = skipDraft(d); continue; }
      const formaCombo = d.team.length > 0 && combos([...d.team, melhor]) > combos(d.team);
      if (d.team.length > 0 && !formaCombo && d.skips > 3 - d.team.length) { d = skipDraft(d); continue; }
      if (d.team.length === 0 && (FORCA[melhor] ?? 0) < corte && d.skips > 0) { d = skipDraft(d); continue; }
      d = pickDraft(d, melhor);
    }
    return d.team;
  };
  for (const [k, x] of ids.entries()) {
    if (k % partes !== parte) continue;
    let vAle = 0, vBom = 0;
    for (let j = 0; j < NJ; j++) {
      const s = semente(j), par = new Set<string>();
      while (par.size < 2) { const c = ids[Math.floor(rnd() * ids.length)]!; if (c !== x) par.add(c); }
      if (jornada([x, ...par], s) === 10) vAle++;
      const bom = trioBom(x, s);
      if (bom.length === 3 && jornada(bom, s) === 10) vBom++;
    }
    const conta = (t: string[], de: number, ate: number) => { let v = 0; for (let j = de; j < ate; j++) if (jornada(t, semente(j)) === 10) v++; return v; };
    // os 20 trios com X que mais venceram nas lutas de verdade (plano trios); só sem a lista, a busca antiga pela nota
    const medidos = ((CANDIDATOS as Record<string, [string, string][]>)[x] ?? []).filter(([a, b]) => ids.includes(a) && ids.includes(b));
    const uni = characters.find((c) => c.id === x)?.universe;
    const ps = [...new Set([...fortes, ...ids.filter((c) => uni && characters.find((z) => z.id === c)?.universe === uni)])].filter((c) => c !== x);
    const pares: [string, string, number][] = [];
    for (let a = 0; a < ps.length; a++) for (let b = a + 1; b < ps.length; b++) pares.push([ps[a]!, ps[b]!, forcaDoTrio([x, ps[a]!, ps[b]!])]);
    pares.sort((p, q) => q[2] - p[2]);
    // da nota: os 10 de nota mais alta e 10 sorteados entre o 11º e o 150º — a campanha põe mais Vida nos rivais do trio
    // que passa do topo, e o trio que mais vence luta avulsa pode ser justamente o que mais sofre com isso
    const pelaNota: [string, string][] = [...pares.slice(0, 10), ...pares.slice(10, 150).sort(() => rnd() - 0.5).slice(0, 10)].map(([a, b]) => [a, b]);
    const vistos = new Set<string>();
    const candidatos = [...medidos.slice(0, 20), ...pelaNota].filter(([a, b]) => { const k = [a, b].sort().join('|'); if (vistos.has(k)) return false; vistos.add(k); return true; });
    const peneira = candidatos.map(([a, b]) => ({ d: [a, b], v: conta([x, a, b], NJ, NJ + 8) })).sort((p, q) => q.v - p.v).slice(0, 3)
      .map((p) => ({ ...p, v: p.v + conta([x, ...p.d], NJ + 8, NJ + 24) })).sort((p, q) => q.v - p.v);
    const melhor = peneira[0]!.d, NM = Math.max(48, Math.round(NJ / 2));
    const vMel = conta([x, ...melhor], NJ + 24, NJ + 24 + NM);
    appendFileSync(saida, JSON.stringify({ id: x, aleatorio: vAle / NJ, bom: vBom / NJ, melhor: vMel / NM, dupla: melhor }) + '\n');
    console.log(`parte ${parte}: ${x} pronto`);
  }
}

/*
 * Os trios de cada estrela (1 a 5): sorteados e, para chegar às estrelas altas, melhorados trocando um personagem de
 * cada vez (só aceita a troca que não piora a nota) até cair na estrela pedida. Cada parte tem os seus.
 */
function triosPorEstrela(quantos: number): number[][][] {
  const pools: number[][][] = [[], [], [], [], [], []];
  const ids = (t: number[]) => t.map((i) => characters[i]!.id);
  for (let alvo = 1; alvo <= 5; alvo++) {
    let tentativas = 0;
    while (pools[alvo]!.length < quantos && tentativas++ < quantos * 60) {
      const u = new Set<number>(); let t = [sorteia(u), sorteia(u), sorteia(u)], nota = notaDoTrio(ids(t));
      for (let passo = 0; passo < 4000; passo++) {
        const e = estrelasDoTime(ids(t));
        if (e === alvo) { pools[alvo]!.push(t); break; }
        if (e > alvo) break;
        const pos = Math.floor(rnd() * 3), c = Math.floor(rnd() * N);
        if (t.includes(c)) continue;
        const novo = t.map((x, j) => (j === pos ? c : x)), n2 = notaDoTrio(ids(novo));
        if (n2 >= nota) { t = novo; nota = n2; }
      }
    }
  }
  return pools;
}
function estrelas() {
  const inicio = Date.now(), pools = triosPorEstrela(150);
  console.log(`parte ${parte}: trios por estrela ${pools.slice(1).map((p) => p.length).join('/')} em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
  let buffer = '', feitas = 0;
  for (let n = 0; n < lutas; n++) {
    // todas as combinações de estrelas, por igual (5 × 5)
    const ea = 1 + (n % 5), eb = 1 + (Math.floor(n / 5) % 5);
    const pa = pools[ea]!, pb = pools[eb]!;
    if (!pa.length || !pb.length) continue;
    const a = pa[Math.floor(rnd() * pa.length)]!, b = pb[Math.floor(rnd() * pb.length)]!;
    if (a.some((x) => b.includes(x))) { n--; continue; }
    // troca o lado a cada luta: o trio a ora é o jogador, ora o rival
    const ladoA = n % 2 === 0, x = ladoA ? a : b, y = ladoA ? b : a;
    const batalha = createBattle(x.map((i) => characters[i]!.id), y.map((i) => characters[i]!.id), Math.floor(rnd() * 2 ** 31), 1);
    for (let t = 0; t < 9000 && !batalha.finished; t++) stepBattle(batalha);
    if (!batalha.finished) continue;
    const venceuA = (batalha.winner === 'player') === ladoA;
    buffer += `${ea} ${eb} ${a.join(' ')} ${b.join(' ')} ${venceuA ? 1 : 0}\n`;
    if (++feitas % 1000 === 0) { appendFileSync(saida, buffer); buffer = ''; }
    if (n % 5000 === 4999) console.log(`parte ${parte}: ${n + 1}/${lutas} lutas · ${((n + 1) / ((Date.now() - inicio) / 1000)).toFixed(0)}/s`);
  }
  appendFileSync(saida, buffer);
  console.log(`parte ${parte}: pronto, ${feitas} lutas em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
}
function estrelasJornada() {
  const inicio = Date.now(), pools = triosPorEstrela(60);
  let buffer = '';
  for (let n = 0; n < lutas; n++) {
    const e = 1 + (n % 5), p = pools[e]!;
    if (!p.length) continue;
    const t = p[Math.floor(rnd() * p.length)]!, team = t.map((i) => characters[i]!.id), seed = Math.floor(rnd() * 2 ** 31);
    const enc = generateCampaign(seed, team);
    // quanto o trio passa do topo (o que a regra usa): a Vida extra de agora dividida pela força da regra
    const acima = Math.max(0, (enc[0]!.scale / ESCALAS[0]! - 1) / VIDA_ACIMA_DO_TOPO);
    const vencidas = VIDAS.map((v) => {
      let k = 0;
      for (; k < 10; k++) {
        const b = createBattle(team, enc[k]!.team, seed + k * 7919, ESCALAS[k]! * (1 + v * acima));
        for (let x = 0; x < 9000 && !b.finished; x++) stepBattle(b);
        if (b.winner !== 'player') break;
      }
      return k;
    });
    buffer += `${e} ${acima.toFixed(3)} ${vencidas.join(' ')} ${t.join(' ')}\n`;
    if (n % 50 === 49) { appendFileSync(saida, buffer); buffer = ''; console.log(`parte ${parte}: ${n + 1}/${lutas} jornadas · ${((Date.now() - inicio) / 1000).toFixed(0)} s`); }
  }
  appendFileSync(saida, buffer);
  console.log(`parte ${parte}: pronto em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
}
