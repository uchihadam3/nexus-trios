import type { Character, Effect, StatusId, Target } from '../engine/types';

/*
 * Mecânicas novas, por personagem (pedido do jogador: "levantar personagem
 * caído" e o resto da lista). Cada uma entra só em quem tem isso na história,
 * e o equilíbrio de força (src/data/ajuste-de-forca.ts) mede o personagem já
 * com ela.
 */

/** Reviver: a habilidade (índice) levanta o aliado caído mais forte com esta fração da Vida. */
export const REVIVER: Record<string, { habilidade: number; vida: number }> = {
  sailormoon: { habilidade: 2, vida: 0.4 }, // o Cristal de Prata devolve o trio à luta
  sora: { habilidade: 1, vida: 0.35 }, // Cura (Vida+): levanta quem caiu
  arthas: { habilidade: 1, vida: 0.3 }, // Erguer os mortos
  jinwoo: { habilidade: 0, vida: 0.3 }, // Extração de sombra: "Levante-se"
  giorno: { habilidade: 0, vida: 0.35 }, // Gold Experience cria vida
  jill: { habilidade: 0, vida: 0.3 }, // o kit de primeiros socorros põe o parceiro de pé
};

/** Renascer: ao cair, volta sozinho depois de `atraso` segundos com esta fração da Vida. */
export const RENASCER: Record<string, { vida: number; atraso: number }> = {
  ikki: { vida: 0.5, atraso: 1.5 }, // a Fênix sempre volta das cinzas
  jeangrey: { vida: 0.4, atraso: 2 }, // a Força Fênix
  deadpool: { vida: 0.35, atraso: 2 }, // o fator de cura não deixa ele morrer
  majinbuu: { vida: 0.35, atraso: 2.5 }, // se refaz de qualquer pedaço
  mummra: { vida: 0.4, atraso: 2.5 }, // "Antigos Espíritos do Mal…": volta do sarcófago
  cell: { vida: 0.3, atraso: 2.5 }, // volta inteiro de uma célula só
  mario: { vida: 0.35, atraso: 1.5 }, // o cogumelo 1-Up: uma vida extra
  wolverine: { vida: 0.3, atraso: 3 }, // o fator de cura não deixa ele ficar no chão
  alucardcv: { vida: 0.35, atraso: 2 }, // vira névoa e se refaz
  muzan: { vida: 0.3, atraso: 2.5 }, // o corpo se remonta de qualquer pedaço
};

/**
 * Provocar: a habilidade deixa os rivais Provocados por `duracao` segundos (só
 * miram em quem provocou). `troca`: o Status que sai para dar lugar — o
 * personagem não ganha mais um efeito, ganha um diferente.
 */
export const PROVOCAR: Record<string, { habilidade: number; duracao: number; troca?: StatusId }> = {
  captain: { habilidade: 1, duracao: 4 }, // "Eu posso o dia todo"
  hulk: { habilidade: 1, duracao: 4, troca: 'slow' }, // o Rugido chama a briga para ele
  bowser: { habilidade: 1, duracao: 3.5 }, // o rei Koopa ruge e fica mais pesado
  eren: { habilidade: 1, duracao: 4 }, // endurece e atrai o golpe para o titã
  majinbuu: { habilidade: 1, duracao: 3.5 }, // debocha e chama para a briga: ele se refaz de tudo
  bart: { habilidade: 1, duracao: 3, troca: 'confused' }, // "Provocação": agora literal
  patolino: { habilidade: 0, duracao: 3, troca: 'weakened' }, // "Exijo atenção"
  cartman: { habilidade: 0, duracao: 3.5, troca: 'slow' }, // "Respeitem minha autoridade!"
  srincrivel: { habilidade: 1, duracao: 4 }, // se põe na frente do trio inteiro
  alphonse: { habilidade: 1, duracao: 4, troca: 'weakened' }, // a armadura chama o golpe para si
};

/** Roubo de vida: a habilidade cura quem age em `fracao` do dano que ela mesma causou. */
export const ROUBO_DE_VIDA: Record<string, { habilidade: number; fracao: number; troca?: StatusId }> = {
  rogue: { habilidade: 0, fracao: 0.5 }, // Vampira: o toque absorve
  blade: { habilidade: 1, fracao: 0.3, troca: 'weakened' }, // meio-vampiro: a lâmina de prata bebe
  dio: { habilidade: 0, fracao: 0.25 }, // "Muda": o vampiro se alimenta no golpe
  galactus: { habilidade: 0, fracao: 0.4, troca: 'slow' }, // Dreno planetário
  malenia: { habilidade: 0, fracao: 0.35 }, // cada acerto a cura
  arthas: { habilidade: 0, fracao: 0.3 }, // a Ceifadora de Almas come almas
  cell: { habilidade: 0, fracao: 0.3 }, // Absorção
};

/**
 * Status novos dados por uma habilidade (Vampirismo, Refletir, Espinhos), com
 * `troca`: o Status que sai para dar lugar, para o personagem ficar diferente
 * em vez de só ganhar mais um efeito.
 */
export interface GanhaStatus { habilidade: number; status: StatusId; valor: number; duracao: number; alvo?: Target; troca?: StatusId }
export const GANHA_STATUS: Record<string, GanhaStatus[]> = {
  // Vampirismo: por um tempo, todo golpe cura
  alucardcv: [{ habilidade: 1, status: 'vampirism', valor: 0.3, duracao: 8, alvo: 'self' }],
  nezuko: [{ habilidade: 2, status: 'vampirism', valor: 0.25, duracao: 8, alvo: 'self' }],
  kaneki: [{ habilidade: 2, status: 'vampirism', valor: 0.3, duracao: 7, alvo: 'self', troca: 'regen' }],
  carnage: [{ habilidade: 1, status: 'vampirism', valor: 0.3, duracao: 7, alvo: 'self', troca: 'regen' }],
  venom: [{ habilidade: 2, status: 'vampirism', valor: 0.3, duracao: 8, alvo: 'self' }],
  muzan: [{ habilidade: 2, status: 'vampirism', valor: 0.25, duracao: 9, alvo: 'self' }],
  // Refletir: devolve parte do golpe recebido
  giorno: [{ habilidade: 1, status: 'reflect', valor: 0.35, duracao: 6, alvo: 'allyWeak', troca: 'protected' }], // Reflexo de dano
  link: [{ habilidade: 1, status: 'reflect', valor: 0.35, duracao: 6, alvo: 'self', troca: 'exposed' }], // o Escudo Hyliano rebate
  iroh: [{ habilidade: 1, status: 'reflect', valor: 0.4, duracao: 5, alvo: 'self', troca: 'exposed' }], // Redirecionar
  zuko: [{ habilidade: 1, status: 'reflect', valor: 0.35, duracao: 5, alvo: 'self' }], // Redirecionar relâmpago
  splinter: [{ habilidade: 1, status: 'reflect', valor: 0.35, duracao: 5, alvo: 'self' }], // Redirecionar
  shiryu: [{ habilidade: 0, status: 'reflect', valor: 0.3, duracao: 6, alvo: 'allyWeak' }], // o Escudo do Dragão devolve o golpe
  mewtwo: [{ habilidade: 1, status: 'reflect', valor: 0.25, duracao: 6, alvo: 'allAllies', troca: 'confused' }], // Barreira (Reflect)
  // Espinhos: quem bate se machuca a cada golpe
  groot: [{ habilidade: 0, status: 'thorns', valor: 18, duracao: 6, alvo: 'allyWeak' }], // galhos com espinhos
  bowser: [{ habilidade: 1, status: 'thorns', valor: 16, duracao: 8, alvo: 'self' }], // o casco cheio de pontas
  edward: [{ habilidade: 1, status: 'thorns', valor: 15, duracao: 6, alvo: 'allyWeak' }], // a muralha sai com estacas
  toph: [{ habilidade: 1, status: 'thorns', valor: 12, duracao: 6, alvo: 'allAllies', troca: 'marked' }], // pontas de pedra
  frozone: [{ habilidade: 1, status: 'thorns', valor: 14, duracao: 6, alvo: 'allAllies' }], // a parede vira estalactites
  gaara: [{ habilidade: 0, status: 'thorns', valor: 18, duracao: 6, alvo: 'allyWeak' }], // a areia responde sozinha
  sonic: [{ habilidade: 0, status: 'thorns', valor: 12, duracao: 5, alvo: 'self' }], // o Spin Dash vira uma bola de espinhos
};

/**
 * Purificar (tira debuffs dos aliados) e Dissipar (tira buffs dos rivais):
 * `quantos` Status saem, os que mais pesam primeiro.
 */
export interface TiraStatus { habilidade: number; tipo: 'cleanse' | 'dispel'; quantos: number; alvo: Target; troca?: StatusId }
export const TIRA_STATUS: Record<string, TiraStatus> = {
  sailormoon: { habilidade: 1, tipo: 'cleanse', quantos: 2, alvo: 'allAllies', troca: 'slow' }, // "limpa o que gruda" no trio
  iroh: { habilidade: 0, tipo: 'cleanse', quantos: 2, alvo: 'self' }, // o chá de jasmim acalma tudo
  samuraijack: { habilidade: 1, tipo: 'cleanse', quantos: 2, alvo: 'self', troca: 'exposed' }, // a postura serena limpa a mente
  zelda: { habilidade: 1, tipo: 'cleanse', quantos: 1, alvo: 'allAllies', troca: 'slow' }, // a barreira sagrada purifica
  professorx: { habilidade: 0, tipo: 'cleanse', quantos: 1, alvo: 'allAllies' }, // tira a interferência da mente do trio
  aang: { habilidade: 1, tipo: 'cleanse', quantos: 2, alvo: 'allyWeak' }, // a água que cura também lava
  constantine: { habilidade: 1, tipo: 'dispel', quantos: 2, alvo: 'enemyWeak', troca: 'slow' }, // Exorcismo
  scarletwitch: { habilidade: 1, tipo: 'dispel', quantos: 1, alvo: 'enemyCast', troca: 'slow' }, // desfaz o feitiço de quem prepara
  rogue: { habilidade: 1, tipo: 'dispel', quantos: 2, alvo: 'enemyCast' }, // "Força roubada": toma o que o rival tinha
  frieren: { habilidade: 0, tipo: 'dispel', quantos: 2, alvo: 'enemyStrong' }, // lê a mana e desmonta a defesa
  billcipher: { habilidade: 1, tipo: 'dispel', quantos: 1, alvo: 'enemyWeak', troca: 'confused' }, // realidade invertida
  darkseid: { habilidade: 1, tipo: 'dispel', quantos: 1, alvo: 'enemyStrong', troca: 'weakened' }, // o tirano arranca a proteção
};

type Mudanca = (effects: Effect[]) => Effect[];
const semStatus = (troca?: StatusId) => (x: Effect) => !(troca && x.kind === 'status' && x.status === troca);
const mudancasDe = (id: string): Map<number, Mudanca[]> => {
  const m = new Map<number, Mudanca[]>();
  const poe = (i: number, f: Mudanca) => m.set(i, [...(m.get(i) ?? []), f]);
  const reviver = REVIVER[id], provocar = PROVOCAR[id], roubo = ROUBO_DE_VIDA[id];
  if (reviver) poe(reviver.habilidade, (e) => [...e, { kind: 'revive', value: reviver.vida, target: 'allyFallen' }]);
  if (provocar) poe(provocar.habilidade, (e) => [
    ...e.filter(semStatus(provocar.troca)),
    { kind: 'status', status: 'provoked', value: 1, duration: provocar.duracao, target: 'allEnemies' },
  ]);
  // o roubo de vida vem depois do dano: cura pelo que a habilidade causou
  if (roubo) poe(roubo.habilidade, (e) => [...e.filter(semStatus(roubo.troca)), { kind: 'lifesteal', value: roubo.fracao }]);
  const tira = TIRA_STATUS[id];
  if (tira) poe(tira.habilidade, (e) => [...e.filter(semStatus(tira.troca)), { kind: tira.tipo, value: tira.quantos, target: tira.alvo }]);
  for (const g of GANHA_STATUS[id] ?? []) poe(g.habilidade, (e) => [
    ...e.filter(semStatus(g.troca)),
    { kind: 'status', status: g.status, value: g.valor, duration: g.duracao, ...(g.alvo ? { target: g.alvo } : {}) },
  ]);
  return m;
};

export function aplicaMecanicas(c: Character): Character {
  const renascer = RENASCER[c.id], mudancas = mudancasDe(c.id);
  if (!renascer && !mudancas.size) return c;
  return {
    ...c,
    ...(renascer ? { renascer } : {}),
    skills: c.skills.map((s, i) => {
      const fs = mudancas.get(i);
      return fs ? { ...s, effects: fs.reduce((e, f) => f(e), [...s.effects]) } : s;
    }) as Character['skills'],
  };
}
