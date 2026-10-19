/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.493, -1.282, -1.091, -0.974, -0.887, -0.818, -0.759, -0.708, -0.662, -0.621,
  -0.583, -0.548, -0.515, -0.484, -0.455, -0.428, -0.401, -0.376, -0.351, -0.328,
  -0.305, -0.283, -0.261, -0.24, -0.219, -0.199, -0.179, -0.16, -0.141, -0.122,
  -0.103, -0.085, -0.067, -0.049, -0.031, -0.013, 0.004, 0.022, 0.039, 0.056,
  0.073, 0.09, 0.108, 0.124, 0.142, 0.159, 0.176, 0.193, 0.21, 0.227,
  0.244, 0.262, 0.279, 0.297, 0.314, 0.332, 0.35, 0.369, 0.387, 0.406,
  0.425, 0.444, 0.463, 0.483, 0.503, 0.524, 0.544, 0.566, 0.587, 0.609,
  0.632, 0.655, 0.679, 0.704, 0.729, 0.755, 0.783, 0.811, 0.84, 0.87,
  0.901, 0.934, 0.969, 1.005, 1.043, 1.084, 1.128, 1.174, 1.224, 1.278,
  1.337, 1.402, 1.475, 1.557, 1.651, 1.762, 1.898, 2.073, 2.319, 2.739,
  7.785,
];
