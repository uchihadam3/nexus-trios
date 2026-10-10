/*
 * De perto ou de longe: quem age vai até o alvo ou fica no lugar.
 *
 * Pedido do jogador: "ataques que são de perto, o personagem deveria ir até lá
 * pra poder aparecer a animação. Ataques de longe, que nem o do Coiote [a
 * bigorna]… ele não precisa estar lá". Antes isso saía do ícone antigo do golpe
 * (um corte com ícone de energia ficava de longe; a bigorna, sem nada voando,
 * fazia o Coiote correr até o alvo). Agora sai do próprio efeito que aparece:
 * golpe de corpo e de lâmina vai até o alvo; tiro, energia, elemento e magia
 * ficam de longe — com as exceções de cada golpe que foge da regra.
 */
import { familia, type VfxFamily } from './vfxProfiles';

export type Distancia = 'perto' | 'longe';

const POR_GRUPO: Partial<Record<string, Distancia>> = { 'físico': 'perto', corte: 'perto', 'projétil': 'longe', energia: 'longe', elemento: 'longe', magia: 'longe' };

/* Efeitos que fogem da regra do grupo. */
const DO_EFEITO: Partial<Record<VfxFamily, Distancia>> = {
  // alcançam de longe: chicote, corrente, laço, braço que estica, tentáculo, rugido, onda de corte
  chicote: 'longe', corrente: 'longe', laco: 'longe', esticar: 'longe', braco_namekiano: 'longe',
  tentaculos: 'longe', tentaculo_simbionte: 'longe', kagune: 'longe', rugido: 'longe', corte_de_energia: 'longe',
  gadget_surpresa: 'longe', bigorna: 'longe', dedo_apontado: 'longe', punho_transmutado: 'longe', desmanche: 'longe',
  corte_dimensional: 'longe', inv_androide: 'longe',
  // de energia ou magia, mas na mão: vai até o alvo
  chidori: 'perto', esfera_espiral: 'perto', kunai_de_hiraishin: 'perto', punho_fotonico: 'perto', toque_da_destruicao: 'perto',
  cajado_da_caveira: 'perto', toque_absorvente: 'perto', soco_da_vida: 'perto',
  raikiri: 'perto', // o Kakashi corre até o rival com o raio na mão
  rasengan: 'perto', // o Naruto leva a esfera na mão até o rival
  gomu_gatling: 'longe', // os braços de borracha esticam até o rival
};

/* Golpes de um personagem só (id ou id:habilidade) que fogem da regra do efeito. */
const DO_GOLPE: Record<string, Distancia> = {
  thor: 'longe',              // a Martelada trovejante é o Mjolnir arremessado
  'greenlantern:1': 'longe', // o punho de construto do anel
  'coiote:1': 'longe',        // a armadilha já estava montada
  'sukuna:0': 'longe', 'sukuna:2': 'longe', // Desmantelar e o Santuário cortam à distância
  taz: 'perto',               // o redemoinho vai até o alvo e morde
  'cloud:1': 'perto',         // a guarda e o contra-ataque com a Buster Sword
};

/** Se o golpe vai até o alvo ou fica de longe; undefined = segue o ícone (apoio, especiais sem regra). */
export function distanciaDoGolpe(characterId: string, skillIndex: number | undefined, family: VfxFamily): Distancia | undefined {
  return DO_GOLPE[skillIndex === undefined ? characterId : `${characterId}:${skillIndex}`] ?? DO_EFEITO[family] ?? POR_GRUPO[familia(family).grupo];
}
