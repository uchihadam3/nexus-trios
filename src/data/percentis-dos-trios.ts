/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.621, -1.188, -1.001, -0.887, -0.803, -0.736, -0.68, -0.631, -0.588, -0.549,
  -0.513, -0.48, -0.449, -0.419, -0.392, -0.366, -0.341, -0.317, -0.294, -0.272,
  -0.25, -0.229, -0.209, -0.189, -0.17, -0.151, -0.133, -0.115, -0.097, -0.079,
  -0.062, -0.045, -0.028, -0.012, 0.005, 0.021, 0.037, 0.053, 0.069, 0.085,
  0.101, 0.117, 0.132, 0.148, 0.164, 0.179, 0.195, 0.211, 0.226, 0.242,
  0.258, 0.274, 0.29, 0.306, 0.322, 0.339, 0.355, 0.372, 0.389, 0.406,
  0.423, 0.441, 0.458, 0.476, 0.495, 0.513, 0.532, 0.552, 0.571, 0.592,
  0.612, 0.634, 0.655, 0.678, 0.701, 0.725, 0.749, 0.775, 0.801, 0.829,
  0.858, 0.888, 0.92, 0.953, 0.989, 1.026, 1.066, 1.108, 1.154, 1.204,
  1.258, 1.318, 1.385, 1.462, 1.549, 1.652, 1.779, 1.941, 2.17, 2.561,
  7.922,
];
