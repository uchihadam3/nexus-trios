// Presentation seconds at 1×. Combat always retains its fixed 100 ms simulation step.
export const PRESENTATION = {
  gameRate: 1,
  normalSeconds: 2.0,
  // A crowded six-fighter exchange uses a readable strike-and-impact gesture.
  // Isolated basics still receive the full normal presentation.
  exchangeSeconds: 0.28,
  isolatedActionGap: 1.4,
  skillSeconds: 2.0,
  grandSeconds: 3.0,
  preparationSeconds: 0.48,
  periodicSeconds: 0.09,
  auxiliarySeconds: 0.09,
  interruptSeconds: 2.35,
  knockoutSeconds: 2.45,
  turnaroundSeconds: 1.6,
  impactAt: 0.48,
  criticalCondition: 0.25,
  nearAction: 0.82,
  grandPreparation: 2.5,
  ambientParticles: 9,
  impactParticles: 7,
  particleLimit: 16,
  maxConnections: 3,
  vfxIntensity: 0.8,
  renderIntervalMs: 24,
  audio: { master: 65, music: 45, effects: 70, bpm: 108, bars: 64, musicSeconds: 142.2, duck: 0.32, maxActiveCues: 12, minorGap: 0.16, majorGap: 0.08 },
} as const;
