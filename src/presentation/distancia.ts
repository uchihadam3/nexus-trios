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
  // básicos que acertam de longe: a lança de corrente do Scorpion, a haste do Pain, o bastão que quica do Demolidor
  lanca_corrente_scorpion: 'longe', haste_negra_pain: 'longe', bastao_de_ricochete: 'longe', chicotes_de_carne_muzan: 'longe',
  // alcançam de longe: chicote, corrente, laço, braço que estica, tentáculo, rugido, onda de corte
  chicote: 'longe', vampire_killer: 'longe', laco: 'longe', esticar: 'longe', braco_namekiano: 'longe',
  tentaculos: 'longe', tentaculo_simbionte: 'longe', kagune: 'longe', corte_de_energia: 'longe',
  gadget_surpresa: 'longe', bigorna: 'longe', dedo_apontado: 'longe', punho_transmutado: 'longe', desmanche: 'longe',
  corte_dimensional: 'longe', inv_androide: 'longe',
  // de energia ou magia, mas na mão: vai até o alvo
  esfera_espiral: 'perto', kunai_de_hiraishin: 'perto', punho_fotonico: 'perto', toque_da_destruicao: 'perto',
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
  'goku:1': 'perto',          // o Kaioken: o Goku avança no rival com o rastro carmesim
  'sukuna:0': 'longe', 'sukuna:2': 'longe', // Desmantelar e o Santuário cortam à distância
  taz: 'perto',               // o redemoinho vai até o alvo e morde
  'cloud:1': 'perto',         // a guarda e o contra-ataque com a Buster Sword
};

/** Se o golpe vai até o alvo ou fica de longe; undefined = segue o ícone (apoio, especiais sem regra). */
export function distanciaDoGolpe(characterId: string, skillIndex: number | undefined, family: VfxFamily): Distancia | undefined {
  return DO_GOLPE[skillIndex === undefined ? characterId : `${characterId}:${skillIndex}`] ?? DO_EFEITO[family] ?? POR_GRUPO[familia(family).grupo];
}
