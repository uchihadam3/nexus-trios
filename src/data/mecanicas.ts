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
  gaara: [{ habilidade: 0, status: 'thorns', valor: 18, duracao: 6, alvo: 'allyWeak' }], // a areia responde sozinha
  sonic: [{ habilidade: 0, status: 'thorns', valor: 12, duracao: 5, alvo: 'self' }], // o Spin Dash vira uma bola de espinhos

  /* ---- Status-assinatura (parte 5): cada um com o que tem na história ---- */
  // Envenenado: perde Vida por segundo, por dentro do Escudo
  coringa: [{ habilidade: 0, status: 'poison', valor: 8, duracao: 6, troca: 'weakened' }], // o gás do riso é veneno
  malenia: [{ habilidade: 1, status: 'poison', valor: 8, duracao: 6, alvo: 'allEnemies', troca: 'burning' }], // a podridão escarlate
  wesker: [{ habilidade: 1, status: 'poison', valor: 7, duracao: 6 }], // o vírus Uroboros
  agent47: [{ habilidade: 0, status: 'poison', valor: 7, duracao: 7, troca: 'weakened' }], // a bebida batizada
  greengoblin: [{ habilidade: 1, status: 'poison', valor: 6, duracao: 6, alvo: 'allEnemies' }, // o gás
    { habilidade: 0, status: 'blind', valor: 0.3, duracao: 5, troca: 'marked' }], // a fumaça da bomba abóbora
  // Sangrando: cada ação custa Vida
  wolverine: [{ habilidade: 0, status: 'bleed', valor: 25, duracao: 8, troca: 'exposed' }], // garras de adamantium
  sukuna: [{ habilidade: 0, status: 'bleed', valor: 22, duracao: 8, troca: 'exposed' }], // Desmantelar corta
  guts: [{ habilidade: 0, status: 'bleed', valor: 20, duracao: 8 }], // a Matadora de Dragões
  kenpachi: [{ habilidade: 1, status: 'bleed', valor: 18, duracao: 8 }], // corte selvagem
  carnage: [{ habilidade: 0, status: 'bleed', valor: 20, duracao: 8, troca: 'burning' }, { habilidade: 1, status: 'vampirism', valor: 0.3, duracao: 7, alvo: 'self', troca: 'regen' }],
  shredder: [{ habilidade: 0, status: 'bleed', valor: 20, duracao: 8 }], // garras de aço
  kratos: [{ habilidade: 0, status: 'bleed', valor: 18, duracao: 8 }], // as Lâminas do Caos
  // Amaldiçoado: menos cura e Escudo
  nobara: [{ habilidade: 0, status: 'cursed', valor: 0.4, duracao: 8, troca: 'marked' }], // pregos amaldiçoados
  skeletor: [{ habilidade: 1, status: 'cursed', valor: 0.4, duracao: 8, troca: 'burning' }], // Maldição
  hadescz: [{ habilidade: 0, status: 'cursed', valor: 0.3, duracao: 8, alvo: 'allEnemies', troca: 'exposed' }, // Elísios
    { habilidade: 1, status: 'sleep', valor: 1, duracao: 4, troca: 'silenced' }], // Sono eterno
  ghostrider: [{ habilidade: 1, status: 'cursed', valor: 0.35, duracao: 7, alvo: 'allEnemies', troca: 'slow' }], // olhar de penitência
  // Congelado: não age; o próximo golpe quebra o gelo (e gelo não queima: Lento no golpe rápido)
  subzero: [{ habilidade: 0, status: 'slow', valor: 0.2, duracao: 5, troca: 'burning' }, { habilidade: 1, status: 'frozen', valor: 0.3, duracao: 2.5, troca: 'paralyzed' }],
  hyoga: [{ habilidade: 0, status: 'slow', valor: 0.2, duracao: 5, troca: 'burning' }, { habilidade: 2, status: 'frozen', valor: 0.3, duracao: 2, alvo: 'allEnemies', troca: 'paralyzed' }],
  camus: [{ habilidade: 2, status: 'frozen', valor: 0.35, duracao: 2, alvo: 'allEnemies', troca: 'paralyzed' }], // o esquife de gelo
  rukia: [{ habilidade: 0, status: 'slow', valor: 0.2, duracao: 5, troca: 'burning' }, { habilidade: 2, status: 'frozen', valor: 0.35, duracao: 2.5, troca: 'paralyzed' }],
  frozone: [{ habilidade: 0, status: 'slow', valor: 0.2, duracao: 5, troca: 'burning' }, { habilidade: 1, status: 'thorns', valor: 14, duracao: 6, alvo: 'allAllies' }, { habilidade: 2, status: 'frozen', valor: 0.3, duracao: 2, alvo: 'allEnemies', troca: 'rooted' }],
  // Dormindo: não age até acordar
  madara: [{ habilidade: 2, status: 'sleep', valor: 1, duracao: 4, alvo: 'allEnemies', troca: 'confused' }], // o Tsukuyomi Infinito
  itachi: [{ habilidade: 0, status: 'sleep', valor: 1, duracao: 3, troca: 'confused' }], // Tsukuyomi
  aizen: [{ habilidade: 0, status: 'sleep', valor: 1, duracao: 3, alvo: 'allEnemies', troca: 'confused' }], // a hipnose completa
  // Cego: pode errar o ataque básico
  kuririn: [{ habilidade: 1, status: 'blind', valor: 0.4, duracao: 5, alvo: 'allEnemies', troca: 'confused' }], // Taiyoken
  shaka: [{ habilidade: 0, status: 'blind', valor: 0.45, duracao: 6, troca: 'confused' }, // tira os sentidos
    { habilidade: 1, status: 'barrier', valor: 2, duracao: 8, alvo: 'allyWeak' }], // o Kaan
  zelda: [{ habilidade: 0, status: 'blind', valor: 0.3, duracao: 5, troca: 'slow' }], // o Selo da Luz ofusca
  // Barreira: anula os próximos debuffs
  strange: [{ habilidade: 0, status: 'barrier', valor: 1, duracao: 8, alvo: 'allAllies' }], // Escudo de Serafim
  jeangrey: [{ habilidade: 1, status: 'barrier', valor: 1, duracao: 8, alvo: 'allAllies' }], // escudo mental
  greenlantern: [{ habilidade: 0, status: 'barrier', valor: 1, duracao: 8, alvo: 'allyWeak' }], // escudo de vontade
  raidenmk: [{ habilidade: 1, status: 'barrier', valor: 1, duracao: 8, alvo: 'allAllies', troca: 'electric' }], // barreira elétrica
  // Esquiva: chance de escapar do golpe inteiro (parte 6) — onde havia Protegido de "fugir", a Esquiva entra no lugar
  pikachu: [{ habilidade: 2, status: 'evasion', valor: 0.35, duracao: 6, alvo: 'self' }], // Agilidade
  killua: [{ habilidade: 0, status: 'evasion', valor: 0.3, duracao: 5, alvo: 'self' }], // o ritmo elétrico deixa rastro
  flash: [{ habilidade: 0, status: 'evasion', valor: 0.35, duracao: 5, alvo: 'self' }], // rápido demais para acertar
  papaleguas: [{ habilidade: 2, status: 'evasion', valor: 0.45, duracao: 6, alvo: 'self', troca: 'protected' }], // bip-bip
  jerry: [{ habilidade: 0, status: 'evasion', valor: 0.4, duracao: 6, alvo: 'self', troca: 'protected' }], // nunca onde deveria
  pernalonga: [{ habilidade: 0, status: 'evasion', valor: 0.4, duracao: 6, alvo: 'self', troca: 'protected' }], // o buraco de coelho
  loki: [{ habilidade: 0, status: 'evasion', valor: 0.35, duracao: 6, alvo: 'self', troca: 'weakened' }], // a duplicata leva o golpe
  sekiro: [{ habilidade: 0, status: 'evasion', valor: 0.4, duracao: 5, alvo: 'self', troca: 'protected' }], // Deflexão
  minato: [{ habilidade: 0, status: 'evasion', valor: 0.3, duracao: 5, alvo: 'self' }], // o Hiraishin já está em outro lugar
  // Marca explosiva (parte 7): bomba-relógio que explode no fim do tempo
  gambit: [{ habilidade: 0, status: 'bomb', valor: 110, duracao: 3, troca: 'burning' }], // a carta carregada de energia cinética
  rocket: [{ habilidade: 0, status: 'bomb', valor: 130, duracao: 3, troca: 'marked' }], // armadilha explosiva
  coiote: [{ habilidade: 0, status: 'bomb', valor: 150, duracao: 4, troca: 'marked' }], // a encomenda ACME tinha uma bomba
  arlequina: [{ habilidade: 2, status: 'bomb', valor: 90, duracao: 3, alvo: 'allEnemies', troca: 'exposed' }], // surpresa explosiva
  donatello: [{ habilidade: 1, status: 'bomb', valor: 100, duracao: 3 }], // o dispositivo tático é uma bomba
  alphonse: [{ habilidade: 2, status: 'barrier', valor: 1, duracao: 8, alvo: 'allAllies' }], // barreira transmutada
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

/*
 * Ajustes pedidos pelo jogador, número a número. Ficam aqui (e não nas regras
 * de estilo de expanded-roster.ts) para ninguém mais ser mexido junto.
 */
type Ajuste = { habilidade: number; muda?: (e: Effect) => Effect; soma?: Effect[] };
const valor = (kind: Effect['kind'], status: StatusId | undefined, f: (e: Effect) => Effect) => (e: Effect) =>
  e.kind === kind && (!status || (e.kind === 'status' && e.status === status)) ? f(e) : e;
export const PEDIDOS_DO_JOGADOR: Record<string, Ajuste[]> = {
  goku: [
    // Kaioken: além do Acelerado 35% por 9 s, Fortalecido 20% por 9 s
    { habilidade: 1, soma: [{ kind: 'status', status: 'strengthened', value: 0.2, duration: 9, target: 'self' }] },
  ],
  professorx: [
    { habilidade: 0, muda: valor('charge', undefined, (e) => ({ ...e, value: 10 } as Effect)) }, // Coordenação mental: Carga 5 → 10
    { habilidade: 0, muda: valor('status', 'haste', (e) => ({ ...e, value: 0.1 } as Effect)) }, // Acelerado 8% → 10%
    { habilidade: 1, muda: (e) => (e.kind === 'interrupt' && e.mode === 'delay' ? { ...e, value: 3 } : e) }, // Bloqueio mental: atraso 1,7 s → 3 s
    { habilidade: 1, muda: valor('status', 'confused', (e) => ({ ...e, duration: 7 } as Effect)) }, // Confuso 5 s → 7 s
    { habilidade: 2, muda: valor('status', 'silenced', (e) => ({ ...e, duration: 5 } as Effect)) }, // Paralisia mental: Silenciado 3 s → 5 s
  ],
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
  for (const a of PEDIDOS_DO_JOGADOR[id] ?? []) poe(a.habilidade, (e) => [...(a.muda ? e.map(a.muda) : e), ...(a.soma ?? [])]);
  const inv = INVOCACAO[id];
  if (inv) poe(inv.habilidade, (e) => [...e.filter(semStatus(inv.troca)), { kind: 'status', status: 'summon', value: inv.dano, duration: inv.duracao, target: 'self', rotulo: inv.nome }]);
  const copiar = COPIAR[id];
  if (copiar) poe(copiar.habilidade, (e) => [...e.filter(semStatus(copiar.troca)), { kind: 'copy', value: copiar.fracao }]);
  const tira = TIRA_STATUS[id];
  if (tira) poe(tira.habilidade, (e) => [...e.filter(semStatus(tira.troca)), { kind: tira.tipo, value: tira.quantos, target: tira.alvo }]);
  for (const g of GANHA_STATUS[id] ?? []) poe(g.habilidade, (e) => [
    ...e.filter(semStatus(g.troca)),
    { kind: 'status', status: g.status, value: g.valor, duration: g.duracao, ...(g.alvo ? { target: g.alvo } : {}) },
  ]);
  return m;
};

/*
 * Debuff miúdo (pedido do jogador: "quase todos os personagens causam
 * debuff"): 137 ataques básicos punham um Status de 3–8% em todo golpe, e 77
 * habilidades um de 5–6%. Não mudava a luta e enchia a tela de ícones. O
 * ataque básico volta a ser só dano (queimar e envenenar por segundo ficam),
 * e a habilidade perde o debuff miúdo — no lugar, quem tem uma marca própria
 * ganhou o Status dela (acima).
 */
const POR_SEGUNDO = new Set<StatusId>(['burning', 'poison', 'bleed']);
const miudo = (limite: number) => (e: Effect) => e.kind === 'status' && !POR_SEGUNDO.has(e.status) && negativo(e.status) && e.value <= limite;
const negativo = (s: StatusId) => !['protected', 'haste', 'regen', 'strengthened', 'vampirism', 'reflect', 'thorns', 'barrier'].includes(s);
export const LIMITE_DO_MIUDO = { basico: 0.08, habilidade: 0.065 };

/** Copiar habilidade (parte 7): a habilidade também usa a última habilidade de um rival, com esta fração da força. */
export const COPIAR: Record<string, { habilidade: number; fracao: number; troca?: StatusId }> = {
  kakashi: { habilidade: 2, fracao: 0.8, troca: 'marked' }, // o Sharingan copia a técnica
  kirby: { habilidade: 1, fracao: 0.7 }, // Cópia de poder
  rogue: { habilidade: 2, fracao: 0.7 }, // Memória emprestada: usa o poder de quem tocou
  megaman: { habilidade: 1, fracao: 0.6 }, // Arma adquirida do chefe
};

/** Invocação (parte 8): a habilidade chama uma criatura que ataca sozinha (dano por ataque, duração). */
export const INVOCACAO: Record<string, { habilidade: number; nome: string; dano: number; duracao: number; troca?: StatusId }> = {
  megumi: { habilidade: 0, nome: 'Cão divino', dano: 40, duracao: 8, troca: 'marked' },
  jinwoo: { habilidade: 2, nome: 'Soldados das sombras', dano: 45, duracao: 9, troca: 'slow' },
  yugi: { habilidade: 1, nome: 'Mago Negro', dano: 50, duracao: 8 },
  kaiba: { habilidade: 1, nome: 'Dragão Branco de Olhos Azuis', dano: 60, duracao: 7, troca: 'exposed' },
  bayonetta: { habilidade: 2, nome: 'Gomorrah', dano: 55, duracao: 7 },
  jotaro: { habilidade: 0, nome: 'Star Platinum', dano: 40, duracao: 6 },
  pain: { habilidade: 0, nome: 'Caminho Animal', dano: 35, duracao: 8, troca: 'exposed' },
  mickey: { habilidade: 1, nome: 'Vassouras encantadas', dano: 35, duracao: 8, troca: 'confused' },
  plankton: { habilidade: 0, nome: 'Exército de clones', dano: 30, duracao: 8, troca: 'exposed' },
  krang: { habilidade: 0, nome: 'Androide de combate', dano: 50, duracao: 8, troca: 'rooted' },
};

/** Última resistência: uma vez por luta, o golpe fatal deixa com 1 de Vida e Protegido por um instante. */
export const ULTIMA_RESISTENCIA: Record<string, { protegido: number; duracao: number }> = {
  naruto: { protegido: 0.5, duracao: 2.5 }, // "Nunca desistir"
  vegeta: { protegido: 0.5, duracao: 2.5 }, // "Não vou cair"
  guts: { protegido: 0.5, duracao: 3 }, // sobrevive ao impossível
  saitama: { protegido: 0.5, duracao: 2 }, // "Ainda aqui"
  invencivel: { protegido: 0.5, duracao: 2.5 }, // "Levantar de novo"
  coragem: { protegido: 0.6, duracao: 2.5 }, // morre de medo, mas não cai
};

export function aplicaMecanicas(c0: Character): Character {
  const c: Character = {
    ...c0,
    basic: { ...c0.basic, effects: c0.basic.effects.filter((e) => !miudo(LIMITE_DO_MIUDO.basico)(e)) },
    skills: c0.skills.map((s) => {
      const effects = s.effects.filter((e) => !miudo(LIMITE_DO_MIUDO.habilidade)(e));
      return effects.length ? { ...s, effects } : s;
    }) as Character['skills'],
  };
  const renascer = RENASCER[c.id], mudancas = mudancasDe(c.id), ultimaResistencia = ULTIMA_RESISTENCIA[c.id], invocacao = INVOCACAO[c.id]?.nome;
  if (!renascer && !ultimaResistencia && !mudancas.size) return c;
  return {
    ...c,
    ...(invocacao ? { invocacao } : {}),
    ...(renascer ? { renascer } : {}),
    ...(ultimaResistencia ? { ultimaResistencia } : {}),
    skills: c.skills.map((s, i) => {
      const fs = mudancas.get(i);
      return fs ? { ...s, effects: fs.reduce((e, f) => f(e), [...s.effects]) } : s;
    }) as Character['skills'],
  };
}
