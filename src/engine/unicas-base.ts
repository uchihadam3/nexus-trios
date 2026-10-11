/*
 * Mecânicas únicas — a base (tipos e funções que todos os lotes usam).
 *
 * Mecânicas únicas: uma regra que só aquele personagem tem, como a Death Note
 * do Light. Pedido do jogador: "tenta fazer alguns personagens serem muito
 * únicos" — cada um aqui joga de um jeito que nenhum outro joga.
 *
 * O motor (battle.ts) chama os ganchos nos momentos certos e passa o `Motor`
 * (as funções da luta), para este arquivo não importar battle.ts. O estado de
 * cada mecânica fica em `f.u` (números), e a luta continua salvável em JSON.
 *
 * Cada regra aparece na ficha ("Mecânica única") e, na luta, como um aviso
 * (`kind: 'unica'`) com o nome dela.
 */
import type { Battle, Effect, Fighter, StatusId, Target } from './types';

export interface Motor {
  dano(b: Battle, fonte: Fighter, alvo: Fighter, valor: number, direto?: boolean, label?: string): void;
  cura(b: Battle, fonte: Fighter, alvo: Fighter, valor: number, label?: string): void;
  efeitos(b: Battle, fonte: Fighter, alvos: Fighter[], efeitos: Effect[]): void;
  alvos(b: Battle, f: Fighter, regra: Target, efeitos?: Effect[]): Fighter[];
  /** Aliados vivos (inclui o próprio). */
  aliados(b: Battle, f: Fighter): Fighter[];
  /** Rivais vivos. */
  rivais(b: Battle, f: Fighter): Fighter[];
  intensidade(f: Fighter, s: StatusId): number;
  /** Mostra a mecânica na luta (texto curto em cima de quem age). */
  aviso(b: Battle, f: Fighter, texto: string, alvo?: Fighter, valor?: number): void;
  sorte(b: Battle): number;
  /** Põe de pé quem caiu, com `fracao` da Vida. */
  levanta(b: Battle, fonte: Fighter, alvo: Fighter, fracao: number): void;
}
/** De onde veio o golpe: `direto` = ataque ou habilidade (não Queimando, Veneno, devolvido…). */
export interface Golpe { direto: boolean; label: string; habilidade: boolean; /** Qual habilidade (0, 1 ou 2), quando o golpe é de uma. */ indice?: number }

export interface Ganchos {
  inicio?(m: Motor, b: Battle, f: Fighter): void;
  /** A cada passo da luta, enquanto está de pé. */
  passo?(m: Motor, b: Battle, f: Fighter, dt: number): void;
  /** Multiplica o dano que ele causa. */
  causa?(m: Motor, b: Battle, f: Fighter, alvo: Fighter, g: Golpe): number;
  /** Multiplica o dano que um aliado dele causa (aura). */
  causaAliado?(m: Motor, b: Battle, f: Fighter, aliado: Fighter, alvo: Fighter, g: Golpe): number;
  /** Multiplica o dano que ele recebe (0 = não pega). */
  recebe?(m: Motor, b: Battle, f: Fighter, fonte: Fighter, g: Golpe): number;
  /** Multiplica o dano que um aliado dele recebe (aura). */
  recebeAliado?(m: Motor, b: Battle, f: Fighter, aliado: Fighter, fonte: Fighter, g: Golpe): number;
  /** Multiplica a cura que ele recebe. */
  curaRecebida?(m: Motor, b: Battle, f: Fighter, fonte: Fighter): number;
  /** Multiplica a cura que um rival dele recebe (ex.: impedir rivais de curar). */
  curaNoRival?(m: Motor, b: Battle, f: Fighter, alvo: Fighter): number;
  /** Ele desviou de um golpe com Esquiva. */
  desviou?(m: Motor, b: Battle, f: Fighter, fonte: Fighter): void;
  /** Multiplica a cura que ele faz em `alvo`. */
  curaFeita?(m: Motor, b: Battle, f: Fighter, alvo: Fighter): number;
  /** Multiplica a velocidade com que a próxima ação enche. */
  ritmo?(m: Motor, b: Battle, f: Fighter): number;
  /** Depois de causar dano (já descontado). */
  bateu?(m: Motor, b: Battle, f: Fighter, alvo: Fighter, dano: number, g: Golpe): void;
  /** Depois de levar dano. */
  apanhou?(m: Motor, b: Battle, f: Fighter, fonte: Fighter, dano: number, g: Golpe): void;
  /** Qualquer dano na luta (para quem reage ao que acontece com os outros). */
  viu?(m: Motor, b: Battle, f: Fighter, fonte: Fighter, alvo: Fighter, dano: number, g: Golpe): void;
  /** Logo antes de a habilidade (0, 1 ou 2) fazer efeito. */
  antes?(m: Motor, b: Battle, f: Fighter, indice: number): void;
  /** Depois de usar uma habilidade (0, 1 ou 2). */
  usou?(m: Motor, b: Battle, f: Fighter, indice: number): void;
  /** Um rival começou a preparar uma habilidade. */
  viuPreparo?(m: Motor, b: Battle, f: Fighter, quem: Fighter, preparo: number): void;
  /** Ele mesmo caiu. */
  morreu?(m: Motor, b: Battle, f: Fighter, quemDerrubou: Fighter): void;
  /** Alguém caiu (de qualquer lado); `f` está de pé. */
  caiu?(m: Motor, b: Battle, f: Fighter, quem: Fighter, quemDerrubou: Fighter): void;
  /**
   * O golpe ia derrubar `alvo` (ele mesmo ou um aliado). Devolve com quanta
   * Vida o alvo fica (≥ 1), ou null para deixar cair.
   */
  salva?(m: Motor, b: Battle, f: Fighter, alvo: Fighter, dano: number, fonte: Fighter, g: Golpe): number | null;
  /** Limita o dano final de um golpe em `alvo` (ele mesmo ou um aliado), depois da defesa e antes do Escudo. */
  limita?(m: Motor, b: Battle, f: Fighter, alvo: Fighter, valor: number): number;
  /** Não pega este Status. */
  imune?(f: Fighter, s: StatusId, duracao: number): boolean;
  /** Um Status ruim de um rival acabou de pegar nele. */
  pegouStatus?(m: Motor, b: Battle, f: Fighter, s: StatusId, fonte: Fighter): void;
  /** Fica parado neste passo (canalizando, dormindo…). */
  parado?(f: Fighter, b: Battle): boolean;
  /** Os golpes dele nunca erram (passam por Esquiva e Cego). */
  nuncaErra?: boolean;
  /** Os golpes de todo o trio dele nunca erram (enquanto ele está de pé). */
  trioNuncaErra?: boolean;
  /** Multiplica o Preparo das habilidades dele (0 = sai na hora). */
  preparo?(f: Fighter, indice: number): number;
  /** Escolhe o alvo do ataque básico dele (undefined = o de sempre). */
  alvoDoBasico?(m: Motor, b: Battle, f: Fighter): Fighter | undefined;
  /** Os golpes diretos dele passam pelo Escudo e vão direto na Vida. */
  atravessaEscudo?: boolean;
  /** Os golpes dele não acordam quem está Dormindo. */
  naoAcorda?: boolean;
  /** Os golpes dele nunca derrubam (deixam com 1 de Vida). */
  poupa?: boolean;
}
export interface Unica { nome: string; texto: string; ganchos: Ganchos }

export const u = (f: Fighter) => (f.u ??= {});
export const vivo = (f: Fighter) => f.hp > 0;
export const fracao = (f: Fighter) => f.hp / f.maxHp;
export function trabalho(m: Motor, b: Battle, f: Fighter, n: number) {
  const s = u(f);
  if (s.deus) return;
  s.trabalhos = Math.min(12, (s.trabalhos ?? 0) + n);
  if (s.trabalhos >= 12) { s.deus = 1; m.aviso(b, f, 'Semideus!', f); }
  else m.aviso(b, f, `Trabalhos ${s.trabalhos}/12`, f, s.trabalhos);
}
export const st = (status: StatusId, value: number, duration: number, target?: Target): Effect => ({ kind: 'status', status, value, duration, target });
export const CONTROLES: StatusId[] = ['paralyzed', 'frozen', 'sleep', 'confused', 'silenced', 'slow', 'rooted'];
export const BUFFS: StatusId[] = ['barrier', 'evasion', 'protected', 'reflect', 'vampirism', 'strengthened', 'haste', 'thorns', 'regen'];
/** O rival com mais Vida agora (o "mais forte" das mecânicas). */
export const maisForte = (m: Motor, b: Battle, f: Fighter) => m.rivais(b, f).sort((x, y) => y.hp - x.hp)[0];
/** O aliado mais ferido (em fração da Vida). */
export const maisFerido = (m: Motor, b: Battle, f: Fighter) => m.aliados(b, f).sort((x, y) => fracao(x) - fracao(y))[0];
/** Um relógio que dispara a cada `cada` segundos (o primeiro depois de `primeiro`). */
export function relogio(f: Fighter, chave: string, dt: number, cada: number, primeiro = cada): boolean {
  // a chave do relógio tem prefixo próprio: não pode colidir com um contador da mecânica de mesmo nome
  const s = u(f), k = `relogio_${chave}`;
  s[k] = (s[k] ?? primeiro) - dt;
  if (s[k]! > 1e-6) return false;
  s[k] = s[k]! + cada;
  return true;
}

