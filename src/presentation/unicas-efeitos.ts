import type { VfxFamily } from './vfxProfiles';

/*
 * A Mecânica única ativando como uma habilidade (pedido do jogador: "a mecânica única a gente tem que tratar
 * como se fosse realmente uma habilidade… mostra o nome, para… faz o efeito").
 *
 * - rara: dispara de vez em quando (1 vez por luta, a cada 15–20 s): toda ativação vira um momento próprio — a
 *   luta espera, o nome aparece na cabeça e o efeito dela toca.
 * - sempre: age o tempo todo (a cada golpe): ativa uma vez no começo da luta, com o mesmo destaque; depois só o
 *   nome aparece na cabeça, sem travar a luta.
 * - condicional: liga quando algo acontece (Vida baixa, aliado ferido…): ativa quando dispara, como a rara.
 *
 * Em todas, se a mesma mecânica disparar de novo em menos de INTERVALO_DA_UNICA, só o nome aparece.
 */
import { INTERVALO_DA_UNICA, JEITO_DA_UNICA, type JeitoDaUnica } from '../data/unicas-jeito';
export { INTERVALO_DA_UNICA, JEITO_DA_UNICA, type JeitoDaUnica };

/** O efeito e o som próprios de cada ativação (pelo texto do aviso; '*' vale para qualquer aviso dela). */
export const EFEITO_DA_UNICA: Record<string, Record<string, { familia: VfxFamily; som: string }>> = {
  cell: { 'Vai explodir!': { familia: 'cell_contagem', som: 'cell-contagem' }, Autodestruição: { familia: 'cell_autodestruicao', som: 'cell-autodestruicao' } },
  hinata: { '*': { familia: 'pontos_de_chakra', som: 'pontos-de-chakra' } },
};

/** O efeito de uma ativação: o próprio dela, ou o círculo de runas de quem ainda não tem. */
export function efeitoDaUnica(personagem: string, aviso: string): { familia: VfxFamily; som: string } {
  const dela = EFEITO_DA_UNICA[personagem];
  return dela?.[aviso] ?? dela?.['*'] ?? { familia: 'unica_ativa', som: 'unica-ativa' };
}
