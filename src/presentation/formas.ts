import type { Battle, Character, Fighter } from '../engine/types';

/**
 * Formas que trocam o retrato no meio da luta. O medalhão e a ficha mostram a forma de agora, e cada troca nasce de
 * um clarão na cor da forma:
 * - Gandalf volta pela mecânica "O Branco" como Gandalf, o Branco;
 * - Ben 10 vira o alien que o Omnitrix sorteou (se o Omnitrix falha, segue o Ben);
 * - Mario fica pequeno até o Super Cogumelo;
 * - Korra entra no Estado Avatar;
 * - Hércules vira Semideus;
 * - Griffith vira Femto no Eclipse;
 * - Kenpachi tira o tapa-olho;
 * - Sephiroth abre a asa negra;
 * - Steve veste a armadura de diamante;
 * - Macaco Louco começa no robô e sai dele quando o robô quebra;
 * - Ikki renasce das cinzas com a Fênix;
 * - Fenrir começa acorrentado e se solta aos 12 s;
 * - Saitama fica sério depois de 4 golpes;
 * - Shadow tira os inibidores;
 * - Drácula vira névoa por 4 s;
 * - Guts veste a Armadura do Berserker nos 6 s finais.
 */
interface Forma { retrato: string; nome: string; cor: string }
const DIR = '/assets/portraits/formas/';
/** Os aliens na ordem do Omnitrix (src/engine/unicas-lote9.ts: 0 Quatro Braços, 1 Chama, 2 XLR8, 3 Diamante, 4 falhou). */
const ALIENS: Forma[] = [
  { retrato: `${DIR}ben10-quatro-bracos.webp`, nome: 'Quatro Braços', cor: '#ff5a4a' },
  { retrato: `${DIR}ben10-chama.webp`, nome: 'Chama', cor: '#ffb43a' },
  { retrato: `${DIR}ben10-xlr8.webp`, nome: 'XLR8', cor: '#3fd8e8' },
  { retrato: `${DIR}ben10-diamante.webp`, nome: 'Diamante', cor: '#8dffb8' },
];
const MARIO_PEQUENO: Forma = { retrato: `${DIR}mario-pequeno.webp`, nome: 'Mario pequeno', cor: '#ff4a3a' };
const KORRA_AVATAR: Forma = { retrato: `${DIR}korra-avatar.webp`, nome: 'Korra, Estado Avatar', cor: '#bfeaff' };
const HERCULES_SEMIDEUS: Forma = { retrato: `${DIR}hercules-semideus.webp`, nome: 'Hércules, Semideus', cor: '#ffd36b' };
const GRIFFITH_FEMTO: Forma = { retrato: `${DIR}griffith-femto.webp`, nome: 'Femto', cor: '#b56cff' };
const KENPACHI_SEM_TAPA_OLHO: Forma = { retrato: `${DIR}kenpachi-sem-tapa-olho.webp`, nome: 'Kenpachi sem o tapa-olho', cor: '#ff5a6a' };
const SEPHIROTH_UMA_ASA: Forma = { retrato: `${DIR}sephiroth-uma-asa.webp`, nome: 'Sephiroth, uma asa', cor: '#7dffcf' };
const STEVE_DIAMANTE: Forma = { retrato: `${DIR}steve-diamante.webp`, nome: 'Steve de diamante', cor: '#5ff0ff' };
const MOJO_ROBO: Forma = { retrato: `${DIR}mojo-robo.webp`, nome: 'Macaco Louco no robô', cor: '#ffd23a' };
const IKKI_RENASCIDO: Forma = { retrato: `${DIR}ikki-renascido.webp`, nome: 'Ikki, a Fênix renascida', cor: '#ff8a2a' };
const FENRIR_PRESO: Forma = { retrato: `${DIR}fenrir-preso.webp`, nome: 'Fenrir acorrentado', cor: '#ff6a3a' };
const SAITAMA_SERIO: Forma = { retrato: `${DIR}saitama-serio.webp`, nome: 'Saitama, modo sério', cor: '#ffd23a' };
const SHADOW_SEM_INIBIDORES: Forma = { retrato: `${DIR}shadow-sem-inibidores.webp`, nome: 'Shadow sem inibidores', cor: '#ff3a4a' };
const DRACULA_NEVOA: Forma = { retrato: `${DIR}dracula-nevoa.webp`, nome: 'Drácula em névoa', cor: '#c84a6a' };
const GUTS_BERSERKER: Forma = { retrato: `${DIR}guts-berserker.webp`, nome: 'Guts, Armadura do Berserker', cor: '#ff2a2a' };
const FORMAS: Record<string, { de: (f: Fighter, agora: number) => Forma | null; todas: Forma[] }> = {
  gandalf: {
    de: (f) => (f.voltou && (f.u?.branco ?? 0) >= 1 ? FORMAS.gandalf!.todas[0]! : null),
    todas: [{ retrato: `${DIR}gandalf-branco.webp`, nome: 'Gandalf, o Branco', cor: '#fffbe8' }],
  },
  ben10: { de: (f) => ALIENS[f.u?.alien ?? -1] ?? null, todas: ALIENS },
  /* Mario começa pequeno e só vira o Mario de sempre (o retrato normal) depois do Super Cogumelo (src/engine/unicas-lote9.ts) */
  mario: { de: (f) => (f.u?.grande ? null : MARIO_PEQUENO), todas: [MARIO_PEQUENO] },
  /* Korra no Estado Avatar: os 6 s de olhos brilhando (src/engine/unicas-lote7.ts) */
  korra: { de: (f, agora) => ((f.u?.avatar ?? 0) > agora ? KORRA_AVATAR : null), todas: [KORRA_AVATAR] },
  /* Hércules vira Semideus com 12 Trabalhos, até o fim da luta (src/engine/unicas.ts) */
  hercules: { de: (f) => (f.u?.deus ? HERCULES_SEMIDEUS : null), todas: [HERCULES_SEMIDEUS] },
  /* Griffith vira Femto no Eclipse (menos de 25% da Vida), até o fim da luta (src/engine/unicas-lote8.ts) */
  griffith: { de: (f) => (f.u?.femto ? GRIFFITH_FEMTO : null), todas: [GRIFFITH_FEMTO] },
  /* Kenpachi tira o tapa-olho com menos de 50% da Vida, até o fim da luta (src/engine/unicas-lote6.ts) */
  kenpachi: { de: (f) => (f.u?.olho ? KENPACHI_SEM_TAPA_OLHO : null), todas: [KENPACHI_SEM_TAPA_OLHO] },
  /* Sephiroth abre a asa negra com menos de 50% da Vida, até o fim da luta (src/engine/unicas-lote7.ts) */
  sephiroth: { de: (f) => (f.u?.asa ? SEPHIROTH_UMA_ASA : null), todas: [SEPHIROTH_UMA_ASA] },
  /* Steve fabrica a armadura de diamante na primeira peça e fica com ela até o fim da luta (src/engine/unicas-lote4.ts) */
  steve: { de: (f) => ((f.u?.pecas ?? 0) >= 1 ? STEVE_DIAMANTE : null), todas: [STEVE_DIAMANTE] },
  /* Macaco Louco começa dentro do robô e sai quando o Escudo do robô quebra (src/engine/unicas-lote7.ts) */
  mojojojo: { de: (f) => (f.u?.robo === 1 ? MOJO_ROBO : null), todas: [MOJO_ROBO] },
  /* Ikki renasce das cinzas e fica com a Fênix em chamas até o fim da luta (src/engine/unicas-lote6.ts) */
  ikki: { de: (f) => (f.u?.fenix ? IKKI_RENASCIDO : null), todas: [IKKI_RENASCIDO] },
  /* Fenrir começa acorrentado na Gleipnir e, solto aos 12 s, volta ao retrato de sempre (src/engine/unicas-lote3.ts) */
  fenrir: { de: (f) => (f.u?.solto ? null : FENRIR_PRESO), todas: [FENRIR_PRESO] },
  /* Saitama fica sério depois de levar 4 golpes, até o fim da luta (src/engine/unicas-lote8.ts) */
  saitama: { de: (f) => ((f.u?.serio ?? 0) >= 4 ? SAITAMA_SERIO : null), todas: [SAITAMA_SERIO] },
  /* Shadow tira os inibidores com menos de 40% da Vida, até o fim da luta (src/engine/unicas-lote6.ts) */
  shadowhh: { de: (f) => (f.u?.aneis ? SHADOW_SEM_INIBIDORES : null), todas: [SHADOW_SEM_INIBIDORES] },
  /* Drácula vira névoa por 4 s com menos de 30% da Vida, e depois volta (src/engine/unicas-lote3.ts) */
  dracula: { de: (f, agora) => ((f.u?.nevoa ?? 0) > agora ? DRACULA_NEVOA : null), todas: [DRACULA_NEVOA] },
  /* Guts veste a Armadura do Berserker nos 6 s em que fica de pé com 1 de Vida (src/engine/unicas.ts) */
  guts: { de: (f, agora) => ((f.u?.berserk ?? 0) > agora ? GUTS_BERSERKER : null), todas: [GUTS_BERSERKER] },
};

/** A forma de agora do lutador, se ele trocou de forma. */
export const formaDe = (f: Fighter, b?: Battle): Forma | null => FORMAS[f.characterId]?.de(f, b?.time ?? 0) ?? null;

/** O personagem como ele aparece agora: com o retrato (e o nome) da forma nova, se trocou. */
export function naFormaDeAgora(c: Character, f: Fighter, b?: Battle): Character {
  const forma = formaDe(f, b);
  return forma ? { ...c, portrait: forma.retrato, name: forma.nome } : c;
}

/** Baixa antes os retratos das formas, para a troca não piscar vazia no meio da luta. */
export function preCarregaFormas(ids: readonly string[]): void {
  if (typeof Image === 'undefined') return;
  for (const id of ids) for (const forma of FORMAS[id]?.todas ?? []) new Image().src = forma.retrato;
}
