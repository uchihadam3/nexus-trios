// Every value is a signed-domain-point contribution. This model intentionally
// separates accumulated event pressure from the slower response to battle state.
export const DOMINION = {
  maxScore: 100,
  situationWeight: 0.3,
  eventMemoryWeight: 0.7,
  memoryHalfLifeSeconds: 32,
  responseSeconds: 2.6,
  situation: { condition: 25, activeFighter: 8, control: 4 },
  event: {
    damagePerFullCondition: 9,
    criticalThreshold: 25,
    criticalCrossing: 7,
    knockout: 24,
    successfulSkill: 1.5,
    grandSkill: 4.5,
    interruption: 14,
    statusApplied: 1.5,
    usefulHealingPerFullCondition: 6,
    usefulProtectionPerFullCondition: 8,
    clutchSave: 17,
    synergyCharge: 1.2,
    investigationQuarter: 1.8,
    investigationComplete: 5,
    deathNote: 40,
  },
  controlStatus: { paralyzed: 1, rooted: 0.65, slowed: 0.35, silenced: 0.55, exposed: 0.3, marked: 0.2 },
} as const;

/*
 * Retorno decrescente por alvo atingido.
 *
 * A direção pediu a métrica explícita: "AOE tem valor diferente de
 * single-target. Criar métrica explícita com retorno decrescente por alvo e
 * validar por simulação."
 *
 * Até aqui não havia nenhuma. Um dano de 300 em `allEnemies` entregava 300 a
 * cada um dos três — 900 no total, contra 300 de um golpe focado. Como a luta
 * termina quando um lado cai inteiro, espalhar dano não era só mais eficiente:
 * era estritamente melhor. A calibragem dos 250 mostrou o efeito disso em
 * ordem: as famílias de área (tempest 76,7%, swarm 66,7%, siege 64,6%) no topo,
 * as de controle e apoio (evader 15,3%, chronos 29,2%, saboteur 30,8%) no fundo.
 *
 * A curva abaixo é o total entregue quando o golpe alcança N alvos vivos. Um
 * alvo entrega o valor inteiro; três entregam 2,2 vezes, não 3. O efeito em
 * área continua valendo mais que o focado — ele só deixa de ser gratuito.
 *
 * Vale para dano. Cura e Escudo não entram: sustentar três aliados feridos é o
 * trabalho de quem escolheu sustentar, e não havia distorção medida ali.
 */
export const RETORNO_POR_ALVO = [0, 1, 1.7, 2.2] as const;

/** O multiplicador de cada acerto quando o golpe alcança `vivos` alvos. */
export const fracaoPorAlvo = (vivos: number): number => {
  if (vivos <= 1) return 1;
  const total = RETORNO_POR_ALVO[Math.min(vivos, RETORNO_POR_ALVO.length - 1)] ?? vivos;
  return total / vivos;
};
