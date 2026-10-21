/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.493, -1.279, -1.088, -0.971, -0.884, -0.815, -0.756, -0.705, -0.659, -0.618,
  -0.58, -0.545, -0.512, -0.481, -0.452, -0.424, -0.398, -0.372, -0.348, -0.324,
  -0.301, -0.279, -0.257, -0.236, -0.215, -0.195, -0.175, -0.156, -0.136, -0.117,
  -0.099, -0.08, -0.062, -0.044, -0.026, -0.009, 0.009, 0.026, 0.044, 0.061,
  0.078, 0.095, 0.112, 0.129, 0.146, 0.164, 0.181, 0.198, 0.215, 0.232,
  0.249, 0.267, 0.284, 0.302, 0.32, 0.338, 0.356, 0.374, 0.392, 0.411,
  0.43, 0.449, 0.469, 0.488, 0.508, 0.529, 0.55, 0.571, 0.592, 0.615,
  0.637, 0.661, 0.684, 0.709, 0.734, 0.76, 0.787, 0.816, 0.845, 0.875,
  0.906, 0.939, 0.974, 1.01, 1.048, 1.089, 1.132, 1.179, 1.228, 1.283,
  1.341, 1.407, 1.479, 1.561, 1.655, 1.766, 1.902, 2.077, 2.323, 2.742,
  7.785,
];
