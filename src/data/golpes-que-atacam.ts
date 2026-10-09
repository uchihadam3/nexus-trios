import type { Character, Effect, Target } from '../engine/types';

/*
 * Habilidades com nome de ataque que não atacavam.
 *
 * Pedido do jogador: "o Shiryu tem o Cólera do Dragão, e ele tá curando, dando
 * buff pro aliado. Não faz sentido… ele pode até dar um buff pra alguém, mas
 * ele tem que atacar o oponente". As habilidades saíam dos modelos de cada
 * estilo (o guardião protege, o estrategista marca), e algumas ficaram só com
 * o efeito de apoio. Aqui elas passam a bater no rival — continuam com o que
 * já faziam (o Escudo, a marca, o reforço) depois do golpe.
 *
 * O dano é uma fração do dano das outras habilidades do próprio personagem:
 * 0,8 nas que eram só apoio (a Masenko, o Sopro flamejante), 0,6 nos golpes
 * de arma que só marcavam (a Yamato, o Bastão bo). O equilíbrio de força mede
 * tudo de novo depois (scripts/medir-forca.ts e equilibrar-personagens.ts).
 */
const GOLPES: Record<string, number> = {
  // eram só apoio ou controle
  'shiryu:1': 0.8, 'gohan:1': 0.8, 'galactus:1': 0.8, 'bowser:1': 0.8, 'sonic:1': 0.8, 'invencivel:1': 0.8, 'bebop:1': 0.8, 'venom:1': 0.8,
  'greengoblin:0': 0.8, 'darkseid:0': 0.8, 'megatron:0': 0.8, 'buzz:0': 0.8, 'lara:0': 0.8,
  // golpes de arma ou de poder que só marcavam, prendiam ou confundiam
  'trunks:0': 0.6, 'samuraijack:0': 0.6, 'vergil:0': 0.6, 'tuob:0': 0.6, 'donatello:0': 0.6, 'cheetara:0': 0.6, 'gordon:0': 0.6,
  'skeletor:0': 0.6, 'yor:0': 0.6, 'greenlantern:1': 0.6, 'mewtwo:0': 0.6, 'madara:0': 0.6, 'nobara:0': 0.6, 'scorpion:0': 0.6, 'ikki:1': 0.6,
};
const RIVAL: Target[] = ['enemyWeak', 'enemyStrong', 'enemyCast', 'investigated', 'leastInvestigated', 'allEnemies', 'randomEnemy'];

export const HABILIDADES_QUE_PASSAM_A_ATACAR = Object.keys(GOLPES);

/*
 * Golpes que passam a pegar todos os rivais (pedido do jogador: "faz o meteoro
 * do Madara pegar em todos os inimigos, não só no mais forte"). O dano em cada
 * um é a fração indicada do dano no alvo único; os Status ficam no alvo de antes.
 */
const EM_AREA: Record<string, number> = { 'madara:1': 0.6 };
export const HABILIDADES_EM_AREA = Object.keys(EM_AREA);

function emArea(c: Character): Character {
  if (!c.skills.some((_, i) => EM_AREA[`${c.id}:${i}`])) return c;
  const skills = c.skills.map((s, i) => {
    const fator = EM_AREA[`${c.id}:${i}`];
    if (!fator) return s;
    const effects = s.effects.map((e): Effect => {
      if (e.kind === 'damage' && (!e.target || RIVAL.includes(e.target))) return { ...e, value: Math.round(e.value * fator), target: 'allEnemies' };
      return e.target ? e : { ...e, target: s.target };
    });
    return { ...s, target: 'allEnemies' as Target, effects };
  }) as Character['skills'];
  return { ...c, skills };
}

export function aplicaGolpesQueAtacam(entrada: Character): Character {
  const c = emArea(entrada);
  if (!c.skills.some((_, i) => GOLPES[`${c.id}:${i}`])) return c;
  // a referência: a mediana do dano das habilidades que já batem (ou o básico × 2,5)
  const dano = (e: Effect) => (e.kind === 'damage' ? e.value : 0);
  const danos = c.skills.flatMap((s) => s.effects.filter((e) => e.kind === 'damage' && RIVAL.includes(e.target ?? s.target)).map(dano)).sort((a, b) => a - b);
  const basico = dano(c.basic.effects.find((e) => e.kind === 'damage') ?? { kind: 'damage', value: 40 });
  const referencia = danos.length ? danos[Math.floor(danos.length / 2)]! : basico * 2.5;
  const skills = c.skills.map((s, i) => {
    const fracao = GOLPES[`${c.id}:${i}`];
    if (!fracao) return s;
    // o golpe no rival vem primeiro; o que a habilidade já fazia continua depois. O alvo da habilidade
    // fica o de antes (a regra de uso — "só sai com alguém ferido" — olha para ele); a luta mostra o
    // golpe indo até o rival atingido
    const alvo: Target = RIVAL.includes(s.target) ? s.target : 'enemyWeak';
    const golpe: Effect = { kind: 'damage', value: Math.round(referencia * fracao), ...(alvo !== s.target ? { target: alvo } : {}) };
    return { ...s, effects: [golpe, ...s.effects] };
  }) as Character['skills'];
  return { ...c, skills };
}
