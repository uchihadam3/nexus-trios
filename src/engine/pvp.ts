/*
 * PvP: as regras da partida, o rating e a IA dos NPCs de treino.
 *
 * Pedido do jogador: cada um monta 3 times de 3 com a sua coleção (9 personagens diferentes); a cada rodada os dois
 * escolhem em segredo um dos seus times e eles lutam. O time que vence fica marcado e não pode ser escolhido de novo;
 * quem perdeu pode escolher qualquer um dos seus times. Vence a partida quem ganhar uma rodada com cada um dos 3 times
 * (no máximo 5 rodadas). O rating é o Elo: todo mundo começa igual e ganha ou perde mais ou menos conforme
 * a diferença para o adversário.
 *
 * Treino (pedido do jogador): 6 NPCs, do iniciante à lenda (o 6º com Aura). Quanto melhor o NPC, mais personagens ele tem
 * (75 → 400, dos mais fracos para os mais fortes, pela força medida em src/data/forca-dos-rivais.ts) e melhor ele
 * escolhe: o iniciante monta trios de qualquer jeito; o mestre procura os melhores trios entre os 400 (força, combos e
 * as duplas que rendem juntas: notaDoTrio) e escolhe cada rodada pensando nos times que você ainda tem. Treino não
 * mexe no rating nem no ranking.
 */
import { byId, characters } from '../data/characters';
import { FORCA } from '../data/forca-dos-rivais';
import { notaDoTrio } from '../presentation/dicas-do-trio';
import { TRIOS_DO_PVP } from '../data/trios-do-pvp';
import { META_DA_LENDA } from '../data/meta-da-lenda';

export type Times = [string[], string[], string[]];
export type Lado = 'eu' | 'rival';
/** `rendida`: quem perdeu desistiu da luta no meio (só daquela rodada; a partida segue). */
export interface RodadaPvp { meu: number; dele: number; seed: number; vencedor: Lado; rendida?: boolean }
export interface PartidaPvp { meus: Times; deles: Times; rodadas: RodadaPvp[]; seed: number }

/** Quantos personagens na coleção para entrar no PvP (3 times de 3, sem repetir). */
export const MINIMO_DA_COLECAO = 9;
/** Toda luta de PvP contra pessoas corre em 3× (pedido do dono: "deixa o pvp contra jogadores fixo na velocidade 3x"; antes 2×). */
export const VELOCIDADE_DO_PVP = 3;
/** Segundos de tela por segundo de luta do motor, com a encenação (nomes, efeitos, pausas). Medido ~5,5 em 2× (em 3× sobra mais folga). */
export const TELA_POR_SEGUNDO = 7;
/** Quanto a luta de uma rodada pode durar na tela (segundos): o prazo de segurança do online. */
export const duracaoNaTela = (duracaoDoMotor: number) => Math.min(TELA_POR_SEGUNDO * duracaoDoMotor + 15, 540);
export const RATING_INICIAL = 1000;
const K_DO_ELO = 32;

/* ---------------------------------------------------------------------------
 * Regras
 * ------------------------------------------------------------------------- */

/** Os 3 times estão certos? 3 trios de 3, 9 personagens diferentes, todos da coleção. */
export function problemaDosTimes(times: readonly (readonly string[])[], colecao?: ReadonlySet<string>): string | null {
  if (times.length !== 3 || times.some((t) => t.length !== 3)) return 'Monte 3 times de 3 personagens.';
  const todos = times.flat();
  if (todos.some((id) => !byId[id])) return 'Personagem inválido.';
  if (new Set(todos).size !== 9) return 'Cada personagem só pode estar em um time.';
  if (colecao && todos.some((id) => !colecao.has(id))) return 'Só vale personagem da sua coleção.';
  return null;
}

/** Quais times de cada lado já venceram uma rodada (e por isso não podem ser escolhidos de novo). */
export function vitoriasDosTimes(p: Pick<PartidaPvp, 'rodadas'>): Record<Lado, [boolean, boolean, boolean]> {
  const v: Record<Lado, [boolean, boolean, boolean]> = { eu: [false, false, false], rival: [false, false, false] };
  for (const r of p.rodadas) v[r.vencedor][r.vencedor === 'eu' ? r.meu : r.dele] = true;
  return v;
}
/** Os times que ainda podem ser escolhidos. */
export function timesLivres(p: Pick<PartidaPvp, 'rodadas'>, lado: Lado): number[] {
  const v = vitoriasDosTimes(p)[lado];
  return [0, 1, 2].filter((i) => !v[i]);
}
/** Quem já venceu com os 3 times (ou null). */
export function vencedorDaPartida(p: Pick<PartidaPvp, 'rodadas'>): Lado | null {
  const v = vitoriasDosTimes(p);
  return v.eu.every(Boolean) ? 'eu' : v.rival.every(Boolean) ? 'rival' : null;
}
/** A semente de cada rodada: a mesma para os dois jogadores, a partir da semente da partida. */
export const sementeDaRodada = (seedDaPartida: number, rodada: number) => ((seedDaPartida >>> 0) + Math.imul(rodada + 1, 0x9e3779b1)) >>> 0;

/* ---------------------------------------------------------------------------
 * Rating (Elo)
 * ------------------------------------------------------------------------- */

/** A chance esperada de A vencer B pelo rating. */
export const esperado = (a: number, b: number) => 1 / (1 + 10 ** ((b - a) / 400));
/**
 * Quem está 400 ou mais acima do rival não ganha nada vencendo (pedido do jogador: "você nem ganha mais pontos se
 * vencer uma pessoa mais baixa"). Vale contra pessoas e contra os rivais da campanha; quem perde perde o de sempre.
 */
export const DIFERENCA_SEM_GANHO = 400;
/** Quanto o rating de A muda: venceu (1) ou perdeu (0) contra B. */
export const variacaoDoElo = (a: number, b: number, venceu: boolean, k = K_DO_ELO) =>
  (venceu && a - b >= DIFERENCA_SEM_GANHO ? 0 : Math.round(k * ((venceu ? 1 : 0) - esperado(a, b))));
/*
 * Contra os rivais da campanha (pedido do jogador): sobe um pouco menos e cai um pouco mais que contra uma pessoa,
 * 80% do ganho e 120% da perda do Elo.
 */
export const GANHO_CONTRA_NPC = 0.8, PERDA_CONTRA_NPC = 1.2;
export const variacaoContraNpc = (a: number, b: number, venceu: boolean) =>
  (venceu && a - b >= DIFERENCA_SEM_GANHO ? 0 : Math.round(K_DO_ELO * ((venceu ? 1 : 0) - esperado(a, b)) * (venceu ? GANHO_CONTRA_NPC : PERDA_CONTRA_NPC)));

/* ---------------------------------------------------------------------------
 * Os NPCs de treino
 * ------------------------------------------------------------------------- */

export type NivelNpc = 1 | 2 | 3 | 4 | 5 | 6;
export interface Npc {
  nivel: NivelNpc; id: string; nome: string; titulo: string; rating: number; cor: string;
  /** O personagem que é a "cara" dele. */
  avatar: string;
  /** Quantos personagens ele tem (dos mais fracos para os mais fortes). */
  colecao: number;
  fala: string;
}
export const NPCS: readonly Npc[] = [
  { nivel: 1, id: 'novato', nome: 'Bento Novato', titulo: 'Iniciante', rating: 800, cor: '#9aa7b8', avatar: 'patrick', colecao: 75, fala: 'Peguei os que achei bonitos. Bora?' },
  { nivel: 2, id: 'mediano', nome: 'Lia Mediana', titulo: 'Mais ou menos', rating: 1000, cor: '#86e3a8', avatar: 'scooby', colecao: 130, fala: 'Já sei uns truques… alguns.' },
  { nivel: 3, id: 'estrategista', nome: 'Caio Estrategista', titulo: 'Intermediário', rating: 1250, cor: '#6fd0ff', avatar: 'naruto', colecao: 200, fala: 'Cada time meu tem um plano.' },
  { nivel: 4, id: 'profissional', nome: 'Vera Profissional', titulo: 'Profissional', rating: 1550, cor: '#c38aff', avatar: 'itachi', colecao: 300, fala: 'Combo, encaixe e força. Sem erro.' },
  { nivel: 5, id: 'mestre', nome: 'O Mestre do Nexus', titulo: 'Mestre', rating: 1900, cor: '#ffd36b', avatar: 'vegeta', colecao: 400, fala: 'Os 400 são meus. Mostre o que aprendeu.' },
  // pedido do dono: "um sexto oponente no treino ainda mais forte que o mestre" — sem Vida a mais ("é uma simulação de
  // PvP"): ele é mais forte por jogar melhor, com os melhores trios e a escolha pensada na partida inteira
  { nivel: 6, id: 'lenda', nome: 'A Lenda do Nexus', titulo: 'Lenda', rating: 2300, cor: '#ff5d7a', avatar: 'beerus', colecao: 400, fala: 'Só jogo com os melhores trios e penso a partida inteira antes de escolher.' },
];

/** Os personagens do NPC: os N mais fracos pela força medida (o mestre tem todos). */
export function colecaoDoNpc(npc: Pick<Npc, 'colecao'>): string[] {
  return characters.map((c) => c.id).sort((a, b) => (FORCA[a] ?? 0) - (FORCA[b] ?? 0) || a.localeCompare(b)).slice(0, npc.colecao);
}

/* um sorteio com semente, para cada partida ser diferente e ainda assim repetível nos testes */
export function sorteio(seed: number) {
  let s = seed >>> 0 || 1;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
}
export const gauss = (r: () => number) => Math.sqrt(-2 * Math.log(r() || 1e-9)) * Math.cos(2 * Math.PI * r());

/* Como cada nível monta e escolhe: quantos trios ele compara, quanto ele "erra" a conta, quanto ele melhora o trio. */
const JEITO: Record<NivelNpc, { amostras: number; erro: number; melhora: number; escolheAoAcaso: number }> = {
  1: { amostras: 1, erro: 0, melhora: 0, escolheAoAcaso: 1 },
  2: { amostras: 6, erro: 0.5, melhora: 3, escolheAoAcaso: 0.5 },
  3: { amostras: 25, erro: 0.3, melhora: 60, escolheAoAcaso: 0.25 },
  4: { amostras: 200, erro: 0.05, melhora: 1500, escolheAoAcaso: 0.08 },
  5: { amostras: 300, erro: 0.02, melhora: 2500, escolheAoAcaso: 0.03 },
  6: { amostras: 400, erro: 0, melhora: 4000, escolheAoAcaso: 0 },
};

/*
 * Profissional e Mestre montam a partir dos trios que mais vencem em luta de verdade (src/data/trios-do-pvp.ts):
 * dos que cabem na coleção dele, entre os `melhores` primeiros, com um pouco de sorte na ordem (`variacao`, em pontos
 * de taxa de vitória), sem repetir personagem.
 */
const DA_LISTA: Partial<Record<NivelNpc, ListaDeTrios>> = { 4: { melhores: 60, variacao: 10 }, 5: { melhores: 18, variacao: 4 },
  // a Lenda monta pelo meta: os trios que mais vencem dos trios fortes (src/data/meta-da-lenda.ts), não de trios sorteados.
  // Medido: vence ~63% das partidas inteiras contra o Mestre, sem Vida a mais
  6: { melhores: 6, variacao: 3, fonte: META_DA_LENDA } };
interface ListaDeTrios { melhores: number; variacao: number; fonte?: readonly (readonly [string, string, string, number, ...number[]])[] }

/** O NPC monta os 3 times dele. */
export function timesDoNpc(nivel: NivelNpc, seed: number, objetivo: (t: readonly string[]) => number = notaDoTrio): Times {
  return montarTimes(colecaoDoNpc(NPCS[nivel - 1]!), JEITO[nivel], objetivo === notaDoTrio ? DA_LISTA[nivel] : undefined, seed, objetivo);
}
/** "Montar sozinho" (o botão da montagem): os melhores 3 times que cabem na sua coleção, do jeito da Profissional. */
export function sugerirTimes(colecao: readonly string[], seed: number): Times | null {
  if (colecao.length < MINIMO_DA_COLECAO) return null;
  return montarTimes([...colecao], JEITO[4], { melhores: 400, variacao: 3 }, seed, notaDoTrio);
}

export interface JeitoDeMontar { amostras: number; erro: number; melhora: number }
/** `aceita`: um limite para os trios (a campanha: o teto de estrelas de cada rival); só se nenhum passar, sai um que não passa. */
export function montarTimes(colecao: string[], jeito: JeitoDeMontar, lista: ListaDeTrios | undefined, seed: number, objetivo: (t: readonly string[]) => number,
  aceita?: (t: readonly string[]) => boolean): Times {
  const r = sorteio(seed ^ 0x5bd1e995);
  let livres = [...colecao];
  const times: string[][] = [];
  if (lista) {
    const dele = new Set(livres);
    const opcoes = (lista.fonte ?? TRIOS_DO_PVP).filter((t) => t.slice(0, 3).every((id) => dele.has(id as string)) && (!aceita || aceita(t.slice(0, 3) as string[]))).slice(0, lista.melhores)
      .map((t) => ({ trio: t.slice(0, 3) as string[], valor: t[3] + gauss(r) * lista.variacao })).sort((a, b) => b.valor - a.valor);
    for (const o of opcoes) if (times.length < 3 && !o.trio.some((id) => times.flat().includes(id))) times.push(o.trio);
    livres = livres.filter((id) => !times.flat().includes(id));
  }
  const nota = (t: string[]) => objetivo(t) + (jeito.erro ? gauss(r) * jeito.erro : 0) - (aceita && !aceita(t) ? 1000 : 0);
  const trioAoAcaso = () => { const p = [...livres]; const t: string[] = []; while (t.length < 3) t.push(p.splice(Math.floor(r() * p.length), 1)[0]!); return t; };
  for (let k = times.length; k < 3; k++) {
    let melhor = trioAoAcaso();
    for (let i = 0; aceita && i < 60 && !aceita(melhor); i++) melhor = trioAoAcaso();
    let nm = nota(melhor);
    for (let i = 1; i < jeito.amostras; i++) { const t = trioAoAcaso(), n = nota(t); if (n > nm) { melhor = t; nm = n; } }
    // melhora o trio trocando um de cada vez pelo melhor que achar (o mestre faz isso muitas vezes)
    for (let i = 0; i < jeito.melhora; i++) {
      const pos = Math.floor(r() * 3), c = livres[Math.floor(r() * livres.length)]!;
      if (melhor.includes(c)) continue;
      const t = melhor.map((x, j) => (j === pos ? c : x)), n = nota(t);
      if (n > nm) { melhor = t; nm = n; }
    }
    times.push(melhor);
    livres = livres.filter((id) => !melhor.includes(id));
  }
  // o mais forte primeiro, como um jogador mostraria
  return times.sort((a, b) => notaDoTrio(b) - notaDoTrio(a)) as Times;
}

/*
 * A Lenda escolhe como um jogador de alto nível: pensa na partida inteira, não só na rodada. Em cada placar possível
 * (quais times de cada lado já venceram), a chance dela vencer a partida sai das chances de cada time contra cada time e
 * do placar que cada resultado deixa; a escolha da rodada é a melhor mistura (o jeito de escolher que mais garante,
 * contra qualquer resposta sua). Ela sorteia dentro dessa mistura: não fica previsível e não vê o time que você escolheu.
 */
function escolhaDaLenda(p: PartidaPvp, r: () => number): number {
  const chance = [0, 1, 2].map((i) => [0, 1, 2].map((j) => chanceDoTrio(p.deles[i]!, p.meus[j]!)));
  const v = vitoriasDosTimes(p), mascara = (x: boolean[]) => x.reduce((m, b, i) => m | (b ? 1 << i : 0), 0);
  const memo = new Map<number, { valor: number; mista: number[] }>();
  const resolve = (minhas: number, suas: number): { valor: number; mista: number[] } => {
    if (minhas === 7) return { valor: 1, mista: [] };
    if (suas === 7) return { valor: 0, mista: [] };
    const chave = minhas * 8 + suas, pronto = memo.get(chave);
    if (pronto) return pronto;
    const linhas = [0, 1, 2].filter((i) => !(minhas & (1 << i))), colunas = [0, 1, 2].filter((j) => !(suas & (1 << j)));
    const a = linhas.map((i) => colunas.map((j) => chance[i]![j]! * resolve(minhas | (1 << i), suas).valor + (1 - chance[i]![j]!) * resolve(minhas, suas | (1 << j)).valor));
    // a melhor mistura das linhas (passos de 2%): a que deixa a pior resposta sua com a maior chance para ela
    let melhor = { valor: -1, mista: linhas.map(() => 0) };
    const passo = 50;
    for (let x = 0; x <= passo; x++) for (let y = 0; y <= (linhas.length > 1 ? passo - x : 0); y++) {
      const pesos = linhas.length === 1 ? [1] : linhas.length === 2 ? [x / passo, 1 - x / passo] : [x / passo, y / passo, (passo - x - y) / passo];
      if (linhas.length === 2 && y > 0) break;
      const pior = Math.min(...colunas.map((_, c) => pesos.reduce((s, w, l) => s + w * a[l]![c]!, 0)));
      if (pior > melhor.valor + 1e-12) melhor = { valor: pior, mista: pesos };
    }
    const mista = [0, 0, 0]; linhas.forEach((i, l) => { mista[i] = melhor.mista[l]!; });
    const res = { valor: melhor.valor, mista };
    memo.set(chave, res);
    return res;
  };
  const { mista } = resolve(mascara(v.rival), mascara(v.eu));
  let sorte = r();
  for (const i of [0, 1, 2]) { sorte -= mista[i]!; if (sorte <= 0 && mista[i]! > 0) return i; }
  return timesLivres(p, 'rival').at(-1)!;
}

/** A chance de um trio vencer o outro pela nota (força, combos e duplas, medidas em lutas simuladas). */
export const chanceDoTrio = (a: readonly string[], b: readonly string[]) => 1 / (1 + Math.exp(-(notaDoTrio(a) - notaDoTrio(b))));

/** O NPC escolhe o time da rodada (sem saber qual você escolheu, só os que você ainda tem). */
export function escolhaDoNpc(nivel: NivelNpc, p: PartidaPvp, seed: number): number {
  const jeito = JEITO[nivel], r = sorteio(seed ^ 0x27d4eb2f);
  const meus = timesLivres(p, 'rival'), seus = timesLivres(p, 'eu');
  if (meus.length === 1 || r() < jeito.escolheAoAcaso) return meus[Math.floor(r() * meus.length)]!;
  if (nivel === 6) return escolhaDaLenda(p, r);
  if (nivel === 2) return meus.reduce((a, b) => (notaDoTrio(p.deles[b]!) > notaDoTrio(p.deles[a]!) ? b : a));
  // do intermediário para cima: o time com mais chance contra os times que você ainda pode escolher; o mestre (e a lenda) pesa
  // mais os seus times fortes (é com eles que um bom jogador vem) e guarda o time mais forte quando já está na frente
  const peso = (j: number) => (nivel >= 5 ? 1 + notaDoTrio(p.meus[j]!) - Math.min(...seus.map((x) => notaDoTrio(p.meus[x]!))) : 1);
  const valor = (i: number) => seus.reduce((s, j) => s + peso(j) * chanceDoTrio(p.deles[i]!, p.meus[j]!), 0) / seus.reduce((s, j) => s + peso(j), 0);
  return meus.reduce((a, b) => (valor(b) > valor(a) ? b : a));
}
