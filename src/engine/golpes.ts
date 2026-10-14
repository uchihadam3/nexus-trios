/*
 * As habilidades de vários golpes (pedido do jogador: "se a habilidade dava cinco golpes e 100 de dano, cada golpe
 * dá 20… não faz sentido só o último dar o dano"). O dano é calculado uma vez, com todos os modificadores, e sai em
 * partes iguais — cada parte é um golpe com o seu número na tela (src/engine/battle.ts: damage, `partes`). O total
 * não muda, e o que reage "ao acertar" (traços, Roubo de vida, Espinhos, Refletir, mecânicas únicas) conta uma vez
 * por habilidade, com o dano inteiro: o equilíbrio fica igual.
 *
 * O número é quantos golpes a habilidade dá ao todo; numa habilidade em área eles se dividem entre os alvos vivos.
 */
export const GOLPES_DA_HABILIDADE: Record<string, number> = {
  // de perto: a sequência de golpes no alvo
  'luffy:0': 8, 'flash:0': 10, 'dio:0': 8, 'jotaro:0': 8, 'tifa:1': 6, 'chunli:0': 8, 'hinata:2': 8,
  'kirito:2': 8, 'raidenmgr:1': 5, 'docinho:1': 5, 'caseyjones:1': 4, 'nightwing:2': 5, 'goro:0': 4,
  'tenshinhan:1': 4, 'zoro:2': 9, 'akuma:2': 10, 'ken:1': 3, 'leatherface:1': 4, 'dash:0': 6, 'neo:0': 6,
  'leonardo:0': 2, 'raphael:0': 2,
  // de longe: os projéteis um por um
  'dio:1': 6, 'nobara:0': 4, 'yor:0': 3, 'gambit:1': 5, 'masterchief:1': 8, 'punisher:1': 5, 'robocop:0': 3,
  'dante:1': 8, 'cuphead:0': 6, 'megaman:0': 3, 'starlord:0': 6, 'kitana:1': 3, 'shadowhh:0': 3, 'sans:0': 6,
  'sailormercury:1': 6, 'elsa:0': 5, 'mario:1': 3, 'seiya:0': 10, 'drax:0': 2, 'gwen:0': 3,
  // em área: a chuva espalhada entre os rivais
  'hawkeye:2': 9, 'roy:1': 9, 'genos:1': 6, 'erza:0': 9, 'byakuya:0': 12, 'zeromm:2': 6,
};
export const golpesDe = (personagem: string, habilidade: number): number => GOLPES_DA_HABILIDADE[`${personagem}:${habilidade}`] ?? 1;
