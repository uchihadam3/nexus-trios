/*
 * A régua da força dos trios (gerado com os 10.586.800 trios do elenco por scripts/regua-dos-trios.ts).
 * PERCENTIS[p] é a nota das Dicas (notaDoTrio) que fica acima de p% de todos os trios possíveis. Daqui saem o "melhor que
 * X% dos trios" e as estrelas do time (src/presentation/dicas-do-trio.ts). Refazer quando os personagens ou as Dicas
 * mudarem bastante (junto com src/data/percentis-finos.ts).
 */
export const PERCENTIS: readonly number[] = [
  -3.493, -1.279, -1.088, -0.971, -0.885, -0.816, -0.757, -0.706, -0.66, -0.619,
  -0.581, -0.546, -0.513, -0.482, -0.453, -0.425, -0.399, -0.373, -0.349, -0.325,
  -0.302, -0.28, -0.258, -0.237, -0.217, -0.197, -0.177, -0.157, -0.138, -0.119,
  -0.101, -0.082, -0.064, -0.046, -0.028, -0.011, 0.007, 0.024, 0.042, 0.059,
  0.076, 0.093, 0.11, 0.127, 0.144, 0.161, 0.178, 0.195, 0.213, 0.23,
  0.247, 0.265, 0.282, 0.3, 0.317, 0.335, 0.353, 0.372, 0.39, 0.409,
  0.427, 0.447, 0.466, 0.486, 0.506, 0.527, 0.547, 0.569, 0.59, 0.612,
  0.635, 0.658, 0.682, 0.707, 0.733, 0.759, 0.786, 0.814, 0.843, 0.873,
  0.905, 0.937, 0.972, 1.008, 1.047, 1.087, 1.131, 1.177, 1.227, 1.281,
  1.34, 1.405, 1.478, 1.56, 1.654, 1.765, 1.901, 2.075, 2.322, 2.741,
  7.785,
];
