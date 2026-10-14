/*
 * A rajada (pedido do jogador: "o Byakuya… manda 10 pétalas… aparece as 10 pétalas na frente dele, tipo um leque…
 * e elas vão nos inimigos: vai, vai, vai… o tempo tá parado"; "se a habilidade dava cinco golpes e 100 de dano,
 * cada golpe dá 20").
 *
 * Duas fontes de vários golpes viram rajada:
 *  - a Mecânica única que solta vários golpes de uma vez (as pétalas do Byakuya, os tiros do Dead Eye, as cartas do
 *    Gambit…): reconhecida pelo rótulo do dano no motor; a luta para enquanto ela corre;
 *  - a habilidade de vários golpes (src/engine/golpes.ts): o motor divide o dano em partes iguais (cada parte com o
 *    seu número), a primeira cai no impacto da habilidade e as outras vêm em sequência.
 * O diretor (src/presentation/director.ts: separaRajadas) põe cada golpe num passo próprio da cadeia; o desenho está
 * em src/components/RajadaDaUnica.tsx.
 */
import type { BattleEvent } from '../engine/types';

export type FormaDaRajada =
  | 'golpe' | 'petala' | 'bala' | 'garra' | 'punho' | 'faca' | 'agulha' | 'carta' | 'energia' | 'fogo' | 'meteoro'
  | 'flecha' | 'missil' | 'espada' | 'osso' | 'bolha' | 'cristal' | 'lamina' | 'raio';
export interface Rajada {
  forma: FormaDaRajada;
  /** entre um golpe e o próximo (s a 1×) */
  intervalo: number;
  /** quanto cada projétil voa até o alvo ('golpe': de perto, sem voo) */
  voo: number;
  /** os projéteis aparecem antes, em leque na frente de quem solta, e saem dali */
  leque: boolean;
  cor: string;
  /** o som de cada golpe que acerta */
  som: string;
  /** a luta para enquanto a rajada corre (a Mecânica única); a habilidade segue o ritmo dela */
  para?: boolean;
}
type Mecanica = Rajada & { rotulo: string };
const r = (forma: FormaDaRajada, cor: string, som: string, x: Partial<Rajada> = {}): Rajada => {
  const perto = forma === 'golpe';
  return { forma, cor, som, intervalo: perto ? 0.15 : 0.2, voo: perto ? 0 : forma === 'bala' ? 0.14 : 0.32, leque: false, ...x };
};
const u = (rotulo: string, forma: FormaDaRajada, cor: string, som: string, x: Partial<Rajada> = {}): Mecanica => ({ ...r(forma, cor, som, x), rotulo, para: true });

/** A Mecânica única: pelo rótulo que o motor dá ao dano (m.dano(…, 'Pétalas')). */
export const RAJADA_DA_UNICA: Record<string, Mecanica> = {
  byakuya: u('Pétalas', 'petala', '#ff9ec4', 'corte', { intervalo: 0.24, voo: 0.42, leque: true }),
  scar: u('Hienas', 'garra', '#f0b24a', 'corte-pesado', { intervalo: 0.36, voo: 0.34 }),
  arthurmorgan: u('Dead Eye', 'bala', '#ffd27a', 'tiro', { intervalo: 0.46 }),
  donald: u('Ataque de nervos', 'punho', '#7ac8ff', 'soco-pesado', { intervalo: 0.3, voo: 0.28 }),
  gambit: u('Carta', 'carta', '#ff5ac8', 'explosao', { intervalo: 0.3, leque: true }),
  madara: u('Meteoro', 'meteoro', '#ff7a2e', 'explosao', { intervalo: 0.4, voo: 0.55 }),
  megatron: u('Tiro devastador', 'energia', '#b06bff', 'disparo', { intervalo: 0.3 }),
  moonknight: u('Crescentes', 'lamina', '#e8eeff', 'corte', { intervalo: 0.28 }),
  carnage: u('Lâminas', 'lamina', '#ff3355', 'corte', { intervalo: 0.28 }),
  kaiba: u('Luz Branca', 'energia', '#bfe6ff', 'feixe', { intervalo: 0.3 }),
  storm: u('Tempestade', 'raio', '#cfe6ff', 'raio', { intervalo: 0.3, voo: 0.18 }),
  rocket: u('Mina', 'missil', '#ffb24a', 'explosao', { intervalo: 0.32 }),
  bowser: u('Rei furioso', 'fogo', '#ff7a2e', 'fogo', { intervalo: 0.3 }),
  coiote: u('Dinamite', 'missil', '#ff5a3a', 'explosao', { intervalo: 0.32 }),
};
/** A habilidade de vários golpes (src/engine/golpes.ts), por personagem:habilidade. */
export const RAJADA_DA_HABILIDADE: Record<string, Rajada> = {
  // de perto
  'luffy:0': r('golpe', '#ff6a3a', 'soco-pesado'), 'flash:0': r('golpe', '#ffd24a', 'soco-leve', { intervalo: 0.1 }),
  'dio:0': r('golpe', '#ffd24a', 'soco-pesado'), 'jotaro:0': r('golpe', '#9a7aff', 'soco-pesado'),
  'tifa:1': r('golpe', '#ff9a7a', 'soco-leve'), 'chunli:0': r('golpe', '#7ac8ff', 'soco-leve', { intervalo: 0.12 }),
  'hinata:2': r('golpe', '#b8c8ff', 'soco-leve'), 'kirito:2': r('golpe', '#7af0ff', 'corte'),
  'raidenmgr:1': r('golpe', '#ff5a5a', 'corte'), 'docinho:1': r('golpe', '#7aff9a', 'soco-leve'),
  'caseyjones:1': r('golpe', '#d8d8d8', 'soco-pesado', { intervalo: 0.2 }), 'nightwing:2': r('golpe', '#5aa0ff', 'soco-leve'),
  'goro:0': r('golpe', '#ffb24a', 'soco-pesado', { intervalo: 0.2 }), 'tenshinhan:1': r('golpe', '#ffd8a8', 'soco-leve'),
  'zoro:2': r('golpe', '#7aff8a', 'corte', { intervalo: 0.13 }), 'akuma:2': r('golpe', '#ff3355', 'soco-pesado', { intervalo: 0.12 }),
  'ken:1': r('golpe', '#ff9a3a', 'soco-pesado', { intervalo: 0.2 }), 'leatherface:1': r('golpe', '#c8a070', 'corte'),
  'dash:0': r('golpe', '#ff8a3a', 'soco-leve', { intervalo: 0.1 }), 'neo:0': r('golpe', '#7aff7a', 'soco-leve'),
  'leonardo:0': r('golpe', '#5a9aff', 'corte', { intervalo: 0.22 }), 'raphael:0': r('golpe', '#ff5a5a', 'corte', { intervalo: 0.22 }),
  // de longe
  'dio:1': r('faca', '#e8e8ff', 'corte', { leque: true }), 'nobara:0': r('agulha', '#ff7a9a', 'estocada'),
  'yor:0': r('agulha', '#ffd24a', 'estocada'), 'gambit:1': r('carta', '#ff5ac8', 'explosao', { leque: true }),
  'masterchief:1': r('bala', '#ffd27a', 'tiro', { intervalo: 0.1 }), 'punisher:1': r('bala', '#ffd27a', 'tiro', { intervalo: 0.12 }),
  'robocop:0': r('bala', '#ffe08a', 'tiro', { intervalo: 0.12 }), 'dante:1': r('bala', '#ff5a5a', 'tiro', { intervalo: 0.1 }),
  'cuphead:0': r('energia', '#7ac8ff', 'disparo', { intervalo: 0.14 }), 'megaman:0': r('energia', '#7ae0ff', 'disparo'),
  'starlord:0': r('energia', '#ff9a4a', 'disparo', { intervalo: 0.14 }), 'kitana:1': r('faca', '#7ab0ff', 'corte'),
  'shadowhh:0': r('flecha', '#ffe24a', 'lamina-energia'), 'sans:0': r('osso', '#ffffff', 'impacto-energia', { leque: true }),
  'sailormercury:1': r('bolha', '#7ad8ff', 'agua'), 'elsa:0': r('cristal', '#bfeaff', 'gelo'),
  'mario:1': r('fogo', '#ff7a2e', 'fogo', { intervalo: 0.24 }), 'seiya:0': r('golpe', '#9ad8ff', 'impacto-energia', { intervalo: 0.12 }),
  'drax:0': r('faca', '#c8c8c8', 'corte'), 'gwen:0': r('energia', '#ff7ad8', 'psiquico'),
  // em área
  'hawkeye:2': r('flecha', '#c8a0ff', 'disparo', { leque: true }), 'roy:1': r('fogo', '#ff7a2e', 'fogo'),
  'genos:1': r('missil', '#ffb24a', 'missil', { leque: true }), 'erza:0': r('espada', '#d8e8ff', 'corte', { leque: true }),
  'byakuya:0': r('petala', '#ff9ec4', 'corte', { leque: true, intervalo: 0.16, voo: 0.38 }), 'zeromm:2': r('lamina', '#ff5a5a', 'lamina-energia'),
};
/** A chave da rajada de um passo: 'u:personagem' (Mecânica única) ou 'h:personagem:habilidade'. */
export function rajadaDaChave(chave: string): Rajada | undefined {
  const [tipo, id, i] = chave.split(':');
  return tipo === 'u' ? RAJADA_DA_UNICA[id!] : RAJADA_DA_HABILIDADE[`${id}:${i}`];
}
/** O golpe da rajada da Mecânica única de quem o causou (pelo rótulo que o motor deu ao dano). */
export function ehDaRajada(e: BattleEvent, personagem: string | undefined): boolean {
  const m = personagem ? RAJADA_DA_UNICA[personagem] : undefined;
  return !!m && (e.kind === 'damage' || e.kind === 'block') && e.label === m.rotulo;
}
/** Quanto tempo o leque leva para se abrir antes do primeiro golpe sair. */
export const ABRE_O_LEQUE = 0.6;
