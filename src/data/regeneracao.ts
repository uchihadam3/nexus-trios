/*
 * Fator da Regeneração de cada personagem, para que a Regeneração que não
 * soma (src/data/statuses.ts) cure o mesmo que curava quando somava — e o
 * número escrito seja o que cura. Gerado por scripts/equilibrar-regeneracao.ts.
 * Mínimo de 4 de Vida por segundo; teto de 25.
 */
export const MINIMO_DA_REGENERACAO = 4;
export const valorDaRegeneracao = (valor: number, fator = 1) => Math.max(MINIMO_DA_REGENERACAO, Math.min(25, Math.round(valor * fator)));
export const FATOR_DA_REGENERACAO: Record<string, number> = {
  "capitaoplaneta": 3.75,
  "carnage": 2.199,
  "coragem": 1.015,
  "denji": 4.117,
  "ghostrider": 1.653,
  "giorno": 1.134,
  "groot": 0.999,
  "guts": 1.005,
  "ikki": 3.212,
  "jill": 2.549,
  "kaneki": 1.295,
  "majinbuu": 2.958,
  "mummra": 2.333,
  "muzan": 0.969,
  "naruto": 1.041,
  "piccolo": 0.992,
  "raven": 1.077,
  "sailormoon": 1.011,
  "sakura": 1.035,
  "sora": 1.072,
  "venom": 1.247,
};
