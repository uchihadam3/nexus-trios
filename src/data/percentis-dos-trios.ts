/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.493, -1.27, -1.079, -0.962, -0.875, -0.806, -0.748, -0.697, -0.652, -0.61,
  -0.573, -0.538, -0.505, -0.474, -0.445, -0.418, -0.391, -0.366, -0.342, -0.318,
  -0.295, -0.273, -0.251, -0.23, -0.21, -0.19, -0.17, -0.15, -0.131, -0.112,
  -0.094, -0.075, -0.057, -0.039, -0.022, -0.004, 0.014, 0.031, 0.048, 0.065,
  0.082, 0.099, 0.116, 0.134, 0.151, 0.168, 0.185, 0.202, 0.219, 0.236,
  0.253, 0.271, 0.288, 0.306, 0.323, 0.341, 0.359, 0.378, 0.396, 0.415,
  0.433, 0.453, 0.472, 0.492, 0.512, 0.532, 0.553, 0.574, 0.596, 0.618,
  0.641, 0.664, 0.688, 0.712, 0.738, 0.764, 0.791, 0.819, 0.848, 0.878,
  0.91, 0.943, 0.977, 1.014, 1.052, 1.093, 1.136, 1.182, 1.232, 1.287,
  1.345, 1.411, 1.483, 1.565, 1.659, 1.77, 1.906, 2.082, 2.328, 2.747,
  7.785,
];
