import type { Character, ChargeRule } from '../engine/types';

/*
 * O ritmo da Carga das habilidades que quase nunca saíam (pedido do dono: "verifica se tem algo que nunca tá ativando
 * ou ativa muito raramente… melhorar um pouquinho pra ela ativar"). Medido em 14.000 lutas sorteadas: as que saíam menos
 * de 0,3 vez por luta (a luta média dura 35 s) têm toda a Carga multiplicada por RITMO, até saírem ~0,4 vez por luta.
 * A Fênix desperta (Jean Grey) fica de fora: é rara de propósito. Chave: "<id do personagem>:<habilidade 0, 1 ou 2>".
 */
export const RITMO: Record<string, number> = {
  "billcipher:0": 2.25,
  "scorpion:0": 2.15,
  "asta:0": 2.08,
  "lelouch:1": 2.07,
  "carnage:0": 1.9,
  "palpatine:0": 1.76,
  "liono:0": 1.97,
  "pain:0": 1.77,
  "frieza:1": 2.07,
  "agent47:0": 1.72,
  "frieza:0": 1.83,
  "hulk:1": 1.55,
  "scarletwitch:2": 2.01,
  "shaka:0": 1.74,
  "darkseid:0": 1.66,
  "hadescz:2": 2.19,
  "deidara:0": 1.62,
  "daredevil:0": 1.56,
  "mewtwo:0": 1.63,
  "thor:1": 1.66,
  "nobara:0": 1.51,
  "dipper:0": 1.45,
  "camus:0": 1.51,
  "deidara:1": 1.47,
  "minato:2": 1.62,
  "hadescz:0": 1.49,
  "jackskellington:0": 1.4,
  "omniman:2": 1.61,
  "giorno:1": 1.57,
  "leonardo:0": 1.45,
  "darkseid:1": 2.19,
  "samus:1": 1.43,
  "cyclops:0": 1.54,
  "malenia:2": 1.61,
  "saitama:2": 1.53,
  "anubis:1": 1.42,
  "megatron:2": 2.02,
  "samara:0": 1.41,
  "aang:2": 1.37,
  "blackwidow:0": 1.24,
  "allmight:2": 1.46,
  "scar:0": 1.32,
  "zeus:0": 1.32,
  "gohan:2": 1.37,
  "zelda:2": 1.27,
};
/* Gatilhos novos: o Acordo do Bill Cipher só carregava com o tempo (40 s) e nunca saía; agora carrega também com o Preparo inimigo. */
const GATILHOS_A_MAIS: Record<string, { regras: ChargeRule[]; texto: string }> = {
  'billcipher:0': { regras: [{ on: 'enemyCast', amount: 9 }], texto: 'Preparo inimigo + tempo' },
};

export function aplicaRitmo(c: Character): Character {
  if (![0, 1, 2].some((i) => RITMO[`${c.id}:${i}`] || GATILHOS_A_MAIS[`${c.id}:${i}`])) return c;
  const skills = c.skills.map((s, i) => {
    const chave = `${c.id}:${i}`, f = RITMO[chave] ?? 1, mais = GATILHOS_A_MAIS[chave];
    if (f === 1 && !mais) return s;
    const charge = [...s.charge, ...(mais?.regras ?? [])].map((r) => ({ ...r, amount: Math.round(r.amount * f * 100) / 100 }));
    return { ...s, charge, ...(mais ? { chargeText: mais.texto } : {}) };
  }) as Character['skills'];
  return { ...c, skills };
}
