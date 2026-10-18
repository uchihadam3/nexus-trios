/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.468, -1.269, -1.08, -0.962, -0.876, -0.807, -0.749, -0.698, -0.652, -0.611,
  -0.574, -0.539, -0.506, -0.475, -0.446, -0.419, -0.392, -0.367, -0.343, -0.319,
  -0.296, -0.274, -0.252, -0.231, -0.211, -0.191, -0.171, -0.152, -0.133, -0.114,
  -0.096, -0.077, -0.059, -0.041, -0.024, -0.006, 0.011, 0.029, 0.046, 0.063,
  0.08, 0.097, 0.114, 0.131, 0.148, 0.165, 0.182, 0.199, 0.216, 0.233,
  0.25, 0.267, 0.285, 0.302, 0.32, 0.337, 0.355, 0.373, 0.392, 0.41,
  0.429, 0.448, 0.467, 0.487, 0.507, 0.527, 0.547, 0.568, 0.59, 0.612,
  0.634, 0.657, 0.681, 0.705, 0.73, 0.756, 0.783, 0.81, 0.839, 0.869,
  0.9, 0.932, 0.966, 1.002, 1.039, 1.079, 1.122, 1.167, 1.216, 1.269,
  1.327, 1.391, 1.461, 1.542, 1.634, 1.742, 1.874, 2.044, 2.284, 2.693,
  7.868,
];
