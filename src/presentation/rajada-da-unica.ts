/*
 * A rajada da Mecânica única (pedido do jogador: "o Byakuya… manda 10 pétalas… só que não tem animação das pétalas
 * indo… aparece as 10 pétalas na frente dele, tipo um leque… e elas vão nos inimigos: vai, vai, vai… o tempo tá
 * parado nesse tempo… uns 2, 3 segundos… depois o tempo volta").
 *
 * As mecânicas que soltam vários golpes de uma vez (as pétalas do Byakuya, as hienas do Scar, os tiros do Dead Eye,
 * os socos do Pato Donald) não aparecem mais como um número só: cada golpe vira um projétil que sai de quem ativou e
 * acerta o alvo dele, um depois do outro, com o número, o tremor e o som na hora em que chega. O diretor
 * (src/presentation/director.ts: separaRajadas) põe cada golpe num passo próprio da cadeia; a luta fica parada enquanto
 * a rajada corre, como em qualquer ativação. O desenho está em src/components/RajadaDaUnica.tsx.
 */
import type { BattleEvent } from '../engine/types';

export type FormaDaRajada = 'petala' | 'bala' | 'garra' | 'punho';
export interface Rajada {
  /** o rótulo do dano no motor (m.dano(…, 'Pétalas')): é assim que o golpe da rajada é reconhecido */
  rotulo: string;
  forma: FormaDaRajada;
  /** entre um golpe e o próximo (s a 1×) */
  intervalo: number;
  /** quanto cada projétil voa até o alvo */
  voo: number;
  /** os projéteis aparecem antes, em leque na frente de quem ativou, e saem dali */
  leque: boolean;
  cor: string;
  /** o som de cada golpe que acerta */
  som: string;
}
export const RAJADA_DA_UNICA: Record<string, Rajada> = {
  byakuya: { rotulo: 'Pétalas', forma: 'petala', intervalo: 0.24, voo: 0.42, leque: true, cor: '#ff9ec4', som: 'corte' },
  scar: { rotulo: 'Hienas', forma: 'garra', intervalo: 0.36, voo: 0.34, leque: false, cor: '#f0b24a', som: 'corte-pesado' },
  arthurmorgan: { rotulo: 'Dead Eye', forma: 'bala', intervalo: 0.46, voo: 0.14, leque: false, cor: '#ffd27a', som: 'tiro' },
  donald: { rotulo: 'Ataque de nervos', forma: 'punho', intervalo: 0.3, voo: 0.28, leque: false, cor: '#7ac8ff', som: 'soco-pesado' },
};
/** O golpe da rajada de quem o causou (pelo rótulo que o motor deu ao dano). */
export function ehDaRajada(e: BattleEvent, personagem: string | undefined): boolean {
  const r = personagem ? RAJADA_DA_UNICA[personagem] : undefined;
  return !!r && (e.kind === 'damage' || e.kind === 'block') && e.label === r.rotulo;
}
/** Quanto tempo o leque leva para se abrir antes do primeiro golpe sair. */
export const ABRE_O_LEQUE = 0.6;
