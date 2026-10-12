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
  goku: { '*': { familia: 'mu_genki_dama', som: 'mu-genki-dama' } },
  vegeta: { '*': { familia: 'mu_zenkai', som: 'mu-zenkai' } },
  naruto: { '*': { familia: 'mu_kage_bunshin', som: 'mu-kage-bunshin' } },
  sasuke: { '*': { familia: 'mu_sharingan', som: 'mu-sharingan' } },
  luffy: { '*': { familia: 'mu_borracha', som: 'mu-borracha' } },
  gojo: { '*': { familia: 'mu_vazio_infinito', som: 'mu-vazio-infinito' } },
  pikachu: { '*': { familia: 'mu_bochechas', som: 'mu-bochechas' } },
  saitama: { 'Tédio do herói': { familia: 'mu_tedio', som: 'mu-tedio' }, 'Modo sério': { familia: 'mu_modo_serio', som: 'mu-modo-serio' } },
  wolverine: { '*': { familia: 'mu_garras_regeneram', som: 'mu-garras-regeneram' } },
  batman: { Gancho: { familia: 'mu_gancho', som: 'mu-gancho' }, 'Bomba de fumaça': { familia: 'mu_bomba_de_fumaca', som: 'mu-bomba-de-fumaca' }, Batarangue: { familia: 'mu_batarangue', som: 'mu-batarangue' }, '*': { familia: 'mu_batarangue', som: 'mu-batarangue' } },
  superman: { '*': { familia: 'mu_sopro_congelante', som: 'mu-sopro-congelante' } },
  spiderman: { '*': { familia: 'mu_teia', som: 'mu-teia' } },
  hulk: { '*': { familia: 'mu_cada_vez_maior', som: 'mu-cada-vez-maior' } },
};

/** O efeito de uma ativação: o próprio dela, ou o círculo de runas de quem ainda não tem. */
export function efeitoDaUnica(personagem: string, aviso: string): { familia: VfxFamily; som: string } {
  const dela = EFEITO_DA_UNICA[personagem];
  return dela?.[aviso] ?? dela?.['*'] ?? { familia: 'unica_ativa', som: 'unica-ativa' };
}
