import type { Character, Effect, StatusId } from '../engine/types';

/*
 * Ajuste do kit de cada personagem (pedido do jogador: "nos mais fortes… reduzir a porcentagem do
 * que eles dão e o tempo do traço… isso ajudou bastante… e os que estão fracos, faz isso pra
 * aumentar").
 *
 * De −1 a 1, gerado por scripts/equilibrar-tempo.ts junto com o ajuste de tempo. Mexe em duas coisas,
 * nunca mais que 30%:
 *   - a porcentagem dos Status que o personagem põe (Fortalecido, Protegido, Exposto, Lento,
 *     Veneno…): ×(1 + 0,3·k);
 *   - o intervalo do traço: ×(1 − 0,3·k) (forte: dispara menos; fraco: mais).
 * Os Status que são "liga/desliga" (Dormindo, Provocado, Paralisado, Silenciado, Barreira,
 * Invocação, Marca explosiva) não mudam. Não editar à mão.
 */
export const AJUSTE_DE_KIT: Record<string, number> = {
  "agent47": -0.4,
  "akuma": -0.2,
  "billcipher": -0.55,
  "coringa": -0.2,
  "darkseid": -0.2,
  "flash": -0.2,
  "gambit": -0.2,
  "geralt": 0.2,
  "greengoblin": -0.2,
  "heman": 0.2,
  "ikki": -0.2,
  "jill": -0.2,
  "kaiba": -0.2,
  "light": -0.2,
  "liono": -0.2,
  "magneto": -0.2,
  "rukia": -0.2,
  "sephiroth": -0.2,
  "shaka": -0.55,
  "sonic": -0.2,
  "stewie": -0.2,
  "yugi": -0.4,
};

const FIXOS = new Set<StatusId>(['sleep', 'provoked', 'paralyzed', 'silenced', 'barrier', 'summon', 'bomb']);
export const PASSO_DO_KIT = 0.3;
const muda = (f: number) => (e: Effect): Effect =>
  e.kind === 'status' && !FIXOS.has(e.status) ? { ...e, value: Math.round(e.value * f * 1000) / 1000 } : e;

export function aplicaAjusteDeKit(c: Character): Character {
  const k = Math.max(-1, Math.min(1, AJUSTE_DE_KIT[c.id] ?? 0));
  if (!k) return c;
  const f = 1 + PASSO_DO_KIT * k;
  return {
    ...c,
    basic: { ...c.basic, effects: c.basic.effects.map(muda(f)) },
    trait: { ...c.trait, cooldown: Math.round(c.trait.cooldown * (1 - PASSO_DO_KIT * k) * 100) / 100, effects: c.trait.effects.map(muda(f)) },
    skills: c.skills.map((s) => ({ ...s, effects: s.effects.map(muda(f)) })) as Character['skills'],
  };
}
