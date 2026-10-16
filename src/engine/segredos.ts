import { byId, characters } from '../data/characters';
import { estrelasDoTime } from '../presentation/dicas-do-trio';
import { forcaDoTrio, sampledTeams, type Encounter } from './campaign';
import { random, shuffle } from './random';

/*
 * Os seis segredos da jornada (pedido do jogador: "seis segredos… dois dão uma luta extra entre a 5 e a 6, dois depois
 * da 10 e dois as duas, até 12 lutas… a maioria dos personagens tem que conseguir").
 *
 * A jornada continua com as 10 lutas de sempre. Cumprir um segredo libera uma luta a mais:
 *  - a luta ★, entre a 5 e a 6 (LUTA_ESTRELA): vem logo depois de vencer a luta 5;
 *  - a luta 11 (LUTA_ONZE): vem depois de vencer a luta 10.
 * São no máximo duas lutas extras (12 ao todo), por mais segredos que a jornada cumpra.
 *
 * A luta extra vale pontos só se o trio vencer. Perder a luta ★ não acaba a jornada: ela segue para a luta 6.
 *
 * Tudo sai das lutas normais (vitória, tempo, quem ficou de pé, a virada de 1 contra 3) e do trio, então o servidor
 * refaz a mesma conta no replay (src/engine/ranked.ts): ninguém inventa um segredo.
 *
 * Chances medidas com o motor atual (jornadas de trios sorteados): Sem Baixas 7%, Relâmpago 6%, Virada 3%,
 * Trio Intacto 1,3%; Clássico do Universo 54% de quem monta um trio de um universo só; Davi contra Golias 19% dos
 * trios de 1 estrela.
 */
export type SegredoId = 'sem-baixas' | 'classico' | 'intacto' | 'virada' | 'relampago' | 'davi';
export type QualLuta = 'estrela' | 'onze';
export interface Segredo {
  id: SegredoId;
  nome: string;
  /** A charada do Livro de Segredos antes de descobrir. */
  charada: string;
  /** A regra, mostrada depois de descobrir. */
  regra: string;
  libera: QualLuta[];
  /** Cor do selo. */
  cor: string;
}
export const SEGREDOS: readonly Segredo[] = [
  { id: 'sem-baixas', nome: 'Sem Baixas', charada: 'Três lutas, três de pé. Ninguém fica pelo caminho.', regra: 'Vença as lutas 1, 2 e 3 terminando cada uma com os três do trio de pé.', libera: ['estrela'], cor: '#7fe0a8' },
  { id: 'classico', nome: 'Clássico do Universo', charada: 'Quem vem do mesmo mundo luta melhor junto… e atrai velhos conhecidos.', regra: 'Monte o trio com três personagens do mesmo universo e vença as 5 primeiras lutas. A luta extra é contra outros do mesmo universo.', libera: ['estrela'], cor: '#8fb4ff' },
  { id: 'intacto', nome: 'Trio Intacto', charada: 'Chegar ao fim é bom. Chegar inteiro é lenda.', regra: 'Vença a luta 10 com os três do trio de pé.', libera: ['onze'], cor: '#ffd36b' },
  { id: 'virada', nome: 'A Virada', charada: 'Sozinho contra três. Quem não desiste…', regra: 'Em qualquer luta, fique com só um do trio de pé contra os três rivais e vença assim mesmo. Depois, vença as 10.', libera: ['onze'], cor: '#ff8a5c' },
  { id: 'relampago', nome: 'Relâmpago', charada: 'Rápido demais para o rival entender o que aconteceu.', regra: 'Vença 4 das 5 primeiras lutas em menos de 25 segundos cada.', libera: ['estrela', 'onze'], cor: '#7fe8ff' },
  { id: 'davi', nome: 'Davi contra Golias', charada: 'Ninguém aposta nos pequenos. Prove que estão errados.', regra: 'Com um trio de 1 estrela, vença as 5 primeiras lutas.', libera: ['estrela', 'onze'], cor: '#d59cff' },
];
export const SEGREDO = Object.fromEntries(SEGREDOS.map((s) => [s.id, s])) as Record<SegredoId, Segredo>;

/** O número (índice) da luta ★ e da luta 11 nos resumos da jornada; as normais são 0 a 9. */
export const LUTA_ESTRELA = 10;
export const LUTA_ONZE = 11;
export const ehLutaExtra = (indice: number) => indice === LUTA_ESTRELA || indice === LUTA_ONZE;
/** A seed de cada luta da jornada (a mesma conta das lutas normais: seed + índice × 7919). */
export const seedDaLuta = (seed: number, indice: number) => seed + indice * 7919;
/**
 * O multiplicador de pontos da luta extra: a ★ vale como a luta 6 (×1,25); a 11 é o maior da jornada, ×1,8 (pedido do
 * dono: "é difícil de liberar, tem que ser o maior de todos"), o mesmo que o índice 16 em multiplicadorDaLuta.
 */
export const indiceDosPontos = (indice: number) => (indice === LUTA_ESTRELA ? 5 : indice === LUTA_ONZE ? 16 : indice);
/** Menos de RELAMPAGO segundos de luta (tempo de jogo, não de tela)… */
export const RELAMPAGO = 25;
/** …em LUTAS_DO_RELAMPAGO das 5 primeiras (era 3: 12% das jornadas fazia; com 4, 6%, como os outros segredos). */
export const LUTAS_DO_RELAMPAGO = 4;

/** O que cada luta normal precisa guardar para os segredos (o RunBattleSummary tem tudo). */
export interface LutaDoSegredo { index: number; won: boolean; time: number; survivors: number; virada?: boolean }

/** O universo do trio, se os três forem do mesmo (e ele tiver ao menos 3 personagens, o que é sempre verdade aí). */
export function universoDoTrio(team: readonly string[]): string | null {
  if (team.length !== 3) return null;
  const u = byId[team[0]!]?.universe;
  return u && team.every((id) => byId[id]?.universe === u) ? u : null;
}

/** Os segredos cumpridos até aqui, na ordem em que aparecem, olhando só as lutas normais. */
export function segredosCumpridos(team: readonly string[], lutas: readonly LutaDoSegredo[]): SegredoId[] {
  const normais = lutas.filter((l) => !ehLutaExtra(l.index)).sort((a, b) => a.index - b.index);
  const da = (i: number) => normais.find((l) => l.index === i);
  const venceuAte = (n: number) => Array.from({ length: n }, (_, i) => da(i)).every((l) => l?.won);
  const out: SegredoId[] = [];
  if (venceuAte(3) && [0, 1, 2].every((i) => da(i)!.survivors === 3)) out.push('sem-baixas');
  if (normais.filter((l) => l.index < 5 && l.won && l.time < RELAMPAGO).length >= LUTAS_DO_RELAMPAGO) out.push('relampago');
  if (venceuAte(5) && universoDoTrio(team)) out.push('classico');
  if (venceuAte(5) && estrelasDoTime(team) === 1) out.push('davi');
  if (normais.some((l) => l.won && l.virada)) out.push('virada');
  if (da(9)?.won && da(9)!.survivors === 3) out.push('intacto');
  return out;
}

/** Os segredos que abrem cada luta extra (a ★ só conta o que foi feito até a luta 5). */
export function segredosDaLuta(team: readonly string[], lutas: readonly LutaDoSegredo[], qual: QualLuta): SegredoId[] {
  const olhar = qual === 'estrela' ? lutas.filter((l) => !ehLutaExtra(l.index) && l.index < 5) : lutas;
  return segredosCumpridos(team, olhar).filter((id) => SEGREDO[id].libera.includes(qual));
}

/**
 * A próxima luta da jornada (0–9, LUTA_ESTRELA ou LUTA_ONZE), ou null se a jornada acabou. `lutas` na ordem em que
 * foram jogadas: 1…5, ★ (se liberada), 6…10, 11 (se liberada).
 */
export function proximaLuta(team: readonly string[], lutas: readonly LutaDoSegredo[]): number | null {
  if (!lutas.length) return 0;
  const ultima = lutas[lutas.length - 1]!;
  if (ultima.index === LUTA_ONZE) return null;
  if (ultima.index === LUTA_ESTRELA) return 5;
  if (!ultima.won) return null;
  if (ultima.index === 4 && !lutas.some((l) => l.index === LUTA_ESTRELA) && segredosDaLuta(team, lutas, 'estrela').length) return LUTA_ESTRELA;
  if (ultima.index === 9) return segredosDaLuta(team, lutas, 'onze').length ? LUTA_ONZE : null;
  return ultima.index + 1;
}

/** As 10 lutas normais foram vencidas (as Conquistas e o "trio campeão" contam só elas). */
export const venceuAsDez = (lutas: readonly LutaDoSegredo[]) => lutas.some((l) => l.index === 9 && l.won);
/** Quantas lutas normais foram vencidas (o progresso de 0 a 10 do ranking). */
export const normaisVencidas = (lutas: readonly LutaDoSegredo[]) => lutas.filter((l) => !ehLutaExtra(l.index) && l.won).length;

/*
 * O rival da luta extra. Sai da seed e do trio, então o servidor sorteia o mesmo.
 *  - Clássico do Universo (só na ★): outros personagens do mesmo universo; se o universo tiver menos de seis, o rival
 *    se completa com versões sombrias do seu próprio trio.
 *  - Luta ★: um trio forte (entre os 25% mais fortes), novo na jornada.
 *  - Luta 11: um dos trios mais fortes de todos (5% do topo), novo na jornada, com um pouco mais de Vida que a luta 10.
 */
export function rivalSecreto(seed: number, team: readonly string[], encounters: readonly Encounter[], qual: QualLuta, classico: boolean): Encounter {
  const rng = { rng: (seed ^ (qual === 'estrela' ? 0x5e57e1a : 0x0b5e11e)) >>> 0 };
  const u = qual === 'estrela' && classico ? universoDoTrio(team) : null;
  if (u) {
    const doMundo = shuffle(characters.filter((c) => c.universe === u && !team.includes(c.id)).map((c) => c.id), rng);
    const rival = [...doMundo.slice(0, 3), ...shuffle([...team], rng)].slice(0, 3);
    return { team: rival, name: `Clássico · ${u}`, power: Math.round(forcaDoTrio(rival) * 100) / 100, scale: encounters[5]!.scale };
  }
  const usados = new Set([...team, ...encounters.flatMap((e) => e.team)]);
  const livres = characters.map((c) => c.id).filter((id) => !usados.has(id));
  const amostra = sampledTeams(livres, rng, 400).map((t) => ({ t, f: forcaDoTrio(t) })).sort((a, b) => a.f - b.f);
  const [de, ate] = qual === 'estrela' ? [0.75, 0.92] : [0.95, 1];
  const faixa = amostra.slice(Math.floor(de * amostra.length), Math.max(Math.floor(de * amostra.length) + 1, Math.ceil(ate * amostra.length)));
  const x = faixa[Math.floor(random(rng) * faixa.length)]!;
  return qual === 'estrela'
    ? { team: [...x.t], name: 'Luta Secreta', power: Math.round(x.f * 100) / 100, scale: encounters[5]!.scale }
    : { team: [...x.t], name: 'O Desafio Secreto', power: Math.round(x.f * 100) / 100, scale: Math.round(encounters[9]!.scale * 1.05 * 1000) / 1000 };
}

/** O rival de qualquer luta da jornada: as normais vêm da campanha, as extras do rivalSecreto. */
export function rivalDaLuta(seed: number, team: readonly string[], encounters: readonly Encounter[], indice: number, lutas: readonly LutaDoSegredo[]): Encounter {
  if (indice === LUTA_ESTRELA) return rivalSecreto(seed, team, encounters, 'estrela', segredosDaLuta(team, lutas, 'estrela').includes('classico'));
  if (indice === LUTA_ONZE) return rivalSecreto(seed, team, encounters, 'onze', false);
  return encounters[indice]!;
}
