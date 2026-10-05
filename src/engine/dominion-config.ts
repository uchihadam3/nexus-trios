// Every value is a signed-domain-point contribution. This model intentionally
// separates accumulated event pressure from the slower response to battle state.
export const DOMINION = {
  maxScore: 100,
  situationWeight: 0.58,
  eventMemoryWeight: 0.42,
  memoryHalfLifeSeconds: 32,
  responseSeconds: 2.6,
  situation: { condition: 38, activeFighter: 15, control: 8 },
  event: {
    damagePerFullCondition: 14,
    criticalThreshold: 25,
    criticalCrossing: 7,
    knockout: 34,
    successfulSkill: 2.2,
    grandSkill: 6.5,
    interruption: 20,
    statusApplied: 2.4,
    usefulHealingPerFullCondition: 8,
    usefulProtectionPerFullCondition: 12,
    clutchSave: 17,
    synergyCharge: 1.2,
    investigationQuarter: 1.8,
    investigationComplete: 5,
    deathNote: 40,
  },
  controlStatus: { paralyzed: 1, rooted: 0.65, slowed: 0.35, silenced: 0.55, exposed: 0.3, marked: 0.2 },
} as const;
