/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.675, -1.466, -1.264, -1.14, -1.048, -0.975, -0.912, -0.859, -0.81, -0.767,
  -0.727, -0.689, -0.655, -0.622, -0.591, -0.562, -0.534, -0.507, -0.48, -0.455,
  -0.431, -0.407, -0.384, -0.362, -0.34, -0.318, -0.297, -0.277, -0.256, -0.236,
  -0.216, -0.197, -0.178, -0.159, -0.14, -0.121, -0.103, -0.084, -0.066, -0.048,
  -0.03, -0.012, 0.006, 0.024, 0.042, 0.06, 0.078, 0.096, 0.114, 0.132,
  0.15, 0.168, 0.186, 0.204, 0.223, 0.241, 0.26, 0.279, 0.298, 0.317,
  0.336, 0.356, 0.375, 0.395, 0.416, 0.436, 0.457, 0.479, 0.5, 0.523,
  0.545, 0.568, 0.591, 0.615, 0.64, 0.665, 0.691, 0.718, 0.746, 0.775,
  0.804, 0.835, 0.867, 0.901, 0.936, 0.973, 1.013, 1.054, 1.099, 1.147,
  1.199, 1.255, 1.318, 1.388, 1.468, 1.562, 1.674, 1.819, 2.019, 2.353,
  6.909,
];
