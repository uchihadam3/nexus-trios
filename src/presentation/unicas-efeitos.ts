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
  strange: { '*': { familia: 'mu_portal', som: 'mu-portal' } },
  flash: { '*': { familia: 'mu_rastro_flash', som: 'mu-rastro-flash' } },
  wonderwoman: { '*': { familia: 'mu_laco', som: 'mu-laco' } },
  ironman: { '*': { familia: 'mu_unibeam', som: 'mu-unibeam' } },
  captain: { '*': { familia: 'mu_lider', som: 'mu-lider' } },
  deadpool: { '*': { familia: 'mu_fator_cura', som: 'mu-fator-cura' } },
  thanos: { '*': { familia: 'mu_joia', som: 'mu-joia' }, Estalo: { familia: 'mu_estalo', som: 'mu-estalo' } },
  gohan: { '*': { familia: 'mu_potencial', som: 'mu-potencial' } },
  piccolo: { '*': { familia: 'mu_treino', som: 'mu-treino' } },
  frieza: { '*': { familia: 'mu_sofrimento', som: 'mu-sofrimento' } },
  kakashi: { '*': { familia: 'mu_copia', som: 'mu-copia' } },
  tanjiro: { '*': { familia: 'mu_fio', som: 'mu-fio' } },
  nezuko: { '*': { familia: 'mu_sangue', som: 'mu-sangue' } },
  zenitsu: { '*': { familia: 'mu_zzz', som: 'mu-zzz' } },
  inosuke: { '*': { familia: 'mu_juntas', som: 'mu-juntas' } },
  muzan: { '*': { familia: 'mu_bracos', som: 'mu-bracos' } },
  yuji: { '*': { familia: 'mu_black_flash', som: 'mu-black-flash' } },
  megumi: { '*': { familia: 'mu_mahoraga', som: 'mu-mahoraga' } },
  nobara: { '*': { familia: 'mu_boneca', som: 'mu-boneca' } },
  sukuna: { '*': { familia: 'mu_santuario', som: 'mu-santuario' } },
  frieren: { '*': { familia: 'mu_mana', som: 'mu-mana' } },
  anya: { '*': { familia: 'mu_waku', som: 'mu-waku' } },
  loid: { '*': { familia: 'mu_strix', som: 'mu-strix' } },
  yor: { '*': { familia: 'mu_espinho', som: 'mu-espinho' } },
  jinwoo: { '*': { familia: 'mu_nivel', som: 'mu-nivel' } },
  kaneki: { '*': { familia: 'mu_kakuja', som: 'mu-kakuja' } },
  yugi: { '*': { familia: 'mu_carta_yugi', som: 'mu-carta-yugi' } },
  kaiba: { '*': { familia: 'mu_olhos_azuis', som: 'mu-olhos-azuis' } },
  blackpanther: { '*': { familia: 'mu_cinetico', som: 'mu-cinetico' } },
  scarletwitch: { '*': { familia: 'mu_hex', som: 'mu-hex' } },
  vision: { '*': { familia: 'mu_joia_da_mente', som: 'mu-joia-da-mente' } },
  captainmarvel: { '*': { familia: 'mu_energia_absorvida', som: 'mu-energia-absorvida' } },
  punisher: { '*': { familia: 'mu_interrogatorio', som: 'mu-interrogatorio' } },
  ghostrider: { '*': { familia: 'mu_pecados', som: 'mu-pecados' } },
  blade: { '*': { familia: 'mu_cacador', som: 'mu-cacador' } },
  moonknight: { '*': { familia: 'mu_crescentes', som: 'mu-crescentes' } },
  cyclops: { '*': { familia: 'mu_raio_rubi', som: 'mu-raio-rubi' } },
  jeangrey: { '*': { familia: 'mu_elo_mental', som: 'mu-elo-mental' } },
  rogue: { '*': { familia: 'mu_toque', som: 'mu-toque' } },
  gambit: { '*': { familia: 'mu_carta_carregada', som: 'mu-carta-carregada' } },
  venom: { '*': { familia: 'mu_simbionte', som: 'mu-simbionte' } },
  carnage: { '*': { familia: 'mu_carnificina', som: 'mu-carnificina' } },
  doctordoom: { '*': { familia: 'mu_doombot', som: 'mu-doombot' } },
  loki: { '*': { familia: 'mu_ilusao', som: 'mu-ilusao' } },
  ultron: { '*': { familia: 'mu_corpo_novo', som: 'mu-corpo-novo' } },
  greengoblin: { '*': { familia: 'mu_abobora', som: 'mu-abobora' } },
  silversurfer: { '*': { familia: 'mu_planeta', som: 'mu-planeta' } },
  galactus: { '*': { familia: 'mu_devorador', som: 'mu-devorador' } },
  groot: { '*': { familia: 'mu_groot', som: 'mu-groot' } },
  rocket: { '*': { familia: 'mu_mina', som: 'mu-mina' } },
  greenlantern: { '*': { familia: 'mu_anel_lanterna', som: 'mu-anel-lanterna' } },
  cyborg: { '*': { familia: 'mu_hacker', som: 'mu-hacker' } },
  shazam: { '*': { familia: 'mu_shazam', som: 'mu-shazam' } },
  cloud: { '*': { familia: 'mu_buster', som: 'mu-buster' } },
  tifa: { '*': { familia: 'mu_combo_tifa', som: 'mu-combo-tifa' } },
  sephiroth: { '*': { familia: 'mu_asa_negra', som: 'mu-asa-negra' } },
  kratos: { '*': { familia: 'mu_furia_esparta', som: 'mu-furia-esparta' } },
  link: { '*': { familia: 'mu_espada_mestra', som: 'mu-espada-mestra' } },
  ganondorf: { '*': { familia: 'mu_poder_inabalavel', som: 'mu-poder-inabalavel' } },
  samus: { '*': { familia: 'mu_raio_de_gelo', som: 'mu-raio-de-gelo' } },
  dante: { '*': { familia: 'mu_estilo', som: 'mu-estilo' } },
  vergil: { '*': { familia: 'mu_concentracao', som: 'mu-concentracao' } },
  bayonetta: { '*': { familia: 'mu_witch_time', som: 'mu-witch-time' } },
  masterchief: { '*': { familia: 'mu_escudo_mjolnir', som: 'mu-escudo-mjolnir' } },
  doomslayer: { '*': { familia: 'mu_armadura_doom', som: 'mu-armadura-doom' } },
  snake: { '*': { familia: 'mu_tranquilizante', som: 'mu-tranquilizante' } },
  raidenmgr: { '*': { familia: 'mu_zandatsu', som: 'mu-zandatsu' } },
  leon: { '*': { familia: 'mu_faca', som: 'mu-faca' } },
  jill: { '*': { familia: 'mu_erva', som: 'mu-erva' } },
  wesker: { '*': { familia: 'mu_uroboros', som: 'mu-uroboros' } },
  lara: { '*': { familia: 'mu_terreno', som: 'mu-terreno' } },
  ezio: { '*': { familia: 'mu_proximo', som: 'mu-proximo' } },
  sonic: { '*': { familia: 'mu_aneis', som: 'mu-aneis' } },
  shadowhh: { '*': { familia: 'mu_inibidores', som: 'mu-inibidores' } },
};

/** O efeito de uma ativação: o próprio dela, ou o círculo de runas de quem ainda não tem. */
export function efeitoDaUnica(personagem: string, aviso: string): { familia: VfxFamily; som: string } {
  const dela = EFEITO_DA_UNICA[personagem];
  return dela?.[aviso] ?? dela?.['*'] ?? { familia: 'unica_ativa', som: 'unica-ativa' };
}
