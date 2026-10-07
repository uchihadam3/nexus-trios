/*
 * FASE H · a Maestria dos 250.
 *
 * O documento pede três desafios por personagem — 250 × 3 = 750 — em três
 * degraus (I Aprender, II Especialista, III Mestre), com duas exigências que
 * andam juntas: **pelo menos 2 dos 3 ligados à mecânica real**, e *"não usar
 * só 'jogue 50 partidas'"*.
 *
 * Os desafios que existiam falhavam nas duas. Eram, para todo mundo:
 *
 *     I   · Ative <habilidade 1> em uma batalha
 *     II  · Use <habilidade 3> 2 vezes
 *     III · Vença uma Jornada e ative <habilidade 3> 3 vezes
 *
 * Os três medem a mesma coisa — quantas vezes um botão saiu — e nenhum olha
 * para o que o personagem **faz**. É o "jogue 50 partidas" com o nome da
 * habilidade colado em cima.
 *
 * Aqui cada desafio é um feito: curar o trio, travar Preparos, abrir inimigos
 * para o resto do time, aguentar a pressão, encher o próprio reforço até o
 * teto. A escolha de quais dois feitos cabem a cada personagem sai do mesmo
 * lugar que as identidades da FASE F — o que ele entregou em 10.000 lutas
 * medidas — então nenhum deles recebe um desafio que o kit não permite
 * cumprir, e a meta é proporcional ao que ele costuma alcançar.
 */
import { statuses } from '../data/statuses';
import { desafiosPorPersonagem } from '../data/maestria';
import type { Battle, BattleEvent, Character, Effect, StatusId, Target } from './types';

/* ---------------------------------------------------------------------------
 * Os feitos que o jogo sabe medir
 * ------------------------------------------------------------------------- */

export type Feito =
  | 'usou'        /* entrou em campo e agiu — o degrau de entrada */
  | 'curou'       /* devolveu Vida ao trio */
  | 'protegeu'    /* deu Escudo ou Protegido */
  | 'interrompeu' /* cortou Preparos inimigos */
  | 'controlou'   /* aplicou controle duro */
  | 'area'        /* acertou vários inimigos de uma vez */
  | 'continuo'    /* deixou inimigos perdendo Vida sozinhos */
  | 'abateu'      /* derrubou inimigos */
  | 'aguentou'    /* absorveu dano e continuou de pé */
  | 'sobreviveu'  /* terminou a luta vivo */
  | 'acumulou'    /* levou o próprio reforço ao teto */
  | 'explodiu'    /* concentrou muito dano num golpe */
  | 'carregou'    /* encheu a Carga dos aliados */
  | 'virou';      /* venceu uma luta estando atrás */

export interface Desafio { grau: 'I' | 'II' | 'III'; titulo: string; feito: Feito; meta: number; mecanico: boolean }

/** Quanto de cada feito um lutador acumulou. */
export type Feitos = Partial<Record<Feito, number>>;

/* ---------------------------------------------------------------------------
 * O que o kit permite — a mesma guarda dos Objetivos
 * ------------------------------------------------------------------------- */

const ALIADOS = new Set<Target>(['self', 'allyWeak', 'allAllies']);
const efeitosDe = (c: Character): { e: Effect; alvo: Target }[] => [
  ...c.trait.effects.map((e) => ({ e, alvo: e.target ?? c.trait.target })),
  ...c.basic.effects.map((e) => ({ e, alvo: e.target ?? c.basic.target })),
  ...c.skills.flatMap((s) => s.effects.map((e) => ({ e, alvo: e.target ?? s.target }))),
];

/**
 * Se o personagem **pode** cumprir aquele feito.
 *
 * É a guarda que o documento exige para os Objetivos — *"nunca gerar
 * impossível para o trio"* — aplicada aqui pelo mesmo motivo: um desafio que
 * o kit não alcança não é difícil, é quebrado.
 */
export const podeCumprir = (c: Character, feito: Feito): boolean => {
  const efeitos = efeitosDe(c);
  const tem = (f: (x: { e: Effect; alvo: Target }) => boolean) => efeitos.some(f);
  switch (feito) {
    case 'curou': return tem(({ e, alvo }) => (e.kind === 'heal' || (e.kind === 'status' && e.status === 'regen')) && ALIADOS.has(alvo) && alvo !== 'self');
    case 'protegeu': return tem(({ e, alvo }) => (e.kind === 'shield' || (e.kind === 'status' && e.status === 'protected')) && ALIADOS.has(alvo));
    case 'interrompeu': return tem(({ e }) => e.kind === 'interrupt');
    case 'controlou': return tem(({ e }) => e.kind === 'status' && ['paralyzed', 'rooted', 'silenced', 'confused'].includes(e.status));
    case 'area': return c.skills.some((s) => s.target === 'allEnemies') || tem(({ e, alvo }) => e.kind === 'damage' && (e.target ?? alvo) === 'allEnemies');
    case 'continuo': return tem(({ e }) => e.kind === 'status' && ['burning', 'electric'].includes(e.status));
    case 'acumulou': return tem(({ e, alvo }) => e.kind === 'status' && statuses[e.status].stack === 'add'
      && statuses[e.status].tone === 'positivo' && ALIADOS.has(alvo));
    case 'carregou': return tem(({ e, alvo }) => e.kind === 'charge' && ALIADOS.has(alvo));
    /* Estes quatro qualquer personagem alcança: todo mundo bate, apanha e vive. */
    case 'usou': case 'abateu': case 'aguentou': case 'sobreviveu': case 'explodiu': case 'virou': return true;
  }
};

/* ---------------------------------------------------------------------------
 * Os 750 desafios
 * ------------------------------------------------------------------------- */

/*
 * O catálogo é gerado, não escrito à mão.
 *
 * As metas saem das 10.000 lutas medidas na FASE F, então elas precisam de um
 * passo offline: `scripts/gerar-maestria.ts` escreve `src/data/maestria.ts`,
 * que é o que o jogo carrega. O runtime não lê arquivo nenhum.
 */
export const desafiosDe = (id: string): readonly Desafio[] => desafiosPorPersonagem[id] ?? [];

/** Em que degrau o personagem está: 0 a III. */
export const grauAlcancado = (id: string, feitos: Feitos): 0 | 1 | 2 | 3 => {
  const desafios = desafiosDe(id);
  let grau = 0;
  for (const d of desafios) {
    if ((feitos[d.feito] ?? 0) >= d.meta) grau += 1;
    else break;
  }
  return grau as 0 | 1 | 2 | 3;
};

/* ---------------------------------------------------------------------------
 * Medir os feitos durante a luta
 * ------------------------------------------------------------------------- */

/*
 * O mesmo desenho do Raio-X, pelo mesmo motivo: `battle.events` guarda só os
 * 180 últimos, então contar no fim da batalha perderia o começo dela. O
 * acumulador recebe os eventos de cada quadro e é puro.
 */
const CONTROLE_DURO = new Set<StatusId>(['paralyzed', 'rooted', 'silenced', 'confused']);
const CONTINUOS = new Set<StatusId>(['burning', 'electric']);

export type FeitosPorPersonagem = Record<string, Feitos>;

export interface EstadoFeitos { porPersonagem: FeitosPorPersonagem; instante: number; alvosNoInstante: number }
export const feitosVazios = (): EstadoFeitos => ({ porPersonagem: {}, instante: -1, alvosNoInstante: 0 });

export function acumularFeitos(estado: EstadoFeitos, eventos: readonly BattleEvent[], battle: Battle): EstadoFeitos {
  if (eventos.length === 0) return estado;
  const porPersonagem: FeitosPorPersonagem = {};
  for (const [id, f] of Object.entries(estado.porPersonagem)) porPersonagem[id] = { ...f };
  let instante = estado.instante, alvosNoInstante = estado.alvosNoInstante;

  const quem = (uid: string) => battle.fighters.find((f) => f.uid === uid);
  const somar = (uid: string, feito: Feito, valor: number) => {
    const f = quem(uid);
    if (!f || f.side !== 'player' || valor <= 0) return;
    const atual = porPersonagem[f.characterId] ?? {};
    atual[feito] = (atual[feito] ?? 0) + valor;
    porPersonagem[f.characterId] = atual;
  };

  for (const ev of eventos) {
    const alvo = ev.target ? quem(ev.target) : undefined;
    const fonte = quem(ev.source);
    if (ev.kind === 'damage' && alvo?.side === 'player' && fonte?.side !== 'player') somar(alvo.uid, 'aguentou', ev.value ?? 0);
    if (!fonte || fonte.side !== 'player') continue;

    switch (ev.kind) {
      case 'damage': {
        const v = ev.value ?? 0;
        /* O maior golpe é um recorde, não uma soma. */
        const atual = porPersonagem[fonte.characterId] ?? {};
        atual.explodiu = Math.max(atual.explodiu ?? 0, v);
        porPersonagem[fonte.characterId] = atual;
        /* Golpes no mesmo instante são o mesmo ataque alcançando vários alvos. */
        if (Math.abs(ev.time - instante) < 1e-6) { alvosNoInstante += 1; if (alvosNoInstante >= 2) somar(fonte.uid, 'area', v); }
        else { instante = ev.time; alvosNoInstante = 1; }
        break;
      }
      /* Cura em si mesmo não é cuidar do trio: o desafio pede o trio. */
      case 'heal': if (alvo && alvo.uid !== fonte.uid && alvo.side === 'player') somar(fonte.uid, 'curou', ev.value ?? 0); break;
      case 'shield': somar(fonte.uid, 'protegeu', ev.value ?? 0); break;
      case 'interrupt': somar(fonte.uid, 'interrompeu', 1); break;
      case 'ko': if (alvo && alvo.side !== 'player') somar(fonte.uid, 'abateu', 1); break;
      case 'synergy': if (alvo?.side === 'player') somar(fonte.uid, 'carregou', ev.value ?? 0); break;
      case 'status': {
        const id = ev.status, dur = ev.value ?? 0;
        if (!id || !alvo) break;
        if (alvo.side !== 'player') {
          if (CONTROLE_DURO.has(id)) somar(fonte.uid, 'controlou', dur);
          if (CONTINUOS.has(id)) somar(fonte.uid, 'continuo', dur);
        } else if (alvo.uid === fonte.uid && statuses[id].stack === 'add' && statuses[id].tone === 'positivo') {
          somar(fonte.uid, 'acumulou', dur);
        } else if (id === 'protected') somar(fonte.uid, 'protegeu', dur * 60);
        break;
      }
      default: break;
    }
  }
  return { porPersonagem, instante, alvosNoInstante };
}

/**
 * Os feitos que só se sabem no fim: estar vivo, ter participado, ter virado.
 *
 * `atrasou` diz se o trio esteve atrás na Vantagem em algum momento — quem
 * chama precisa ter observado isso durante a luta, porque no fim a informação
 * já não está em lugar nenhum.
 */
export function fecharFeitos(estado: EstadoFeitos, battle: Battle, atrasou: boolean): FeitosPorPersonagem {
  const saida: FeitosPorPersonagem = {};
  for (const [id, f] of Object.entries(estado.porPersonagem)) saida[id] = { ...f };
  for (const f of battle.fighters) {
    if (f.side !== 'player') continue;
    const atual = saida[f.characterId] ?? {};
    atual.usou = (atual.usou ?? 0) + 1;
    if (f.hp > 0) atual.sobreviveu = (atual.sobreviveu ?? 0) + 1;
    if (battle.winner === 'player' && atrasou) atual.virou = (atual.virou ?? 0) + 1;
    saida[f.characterId] = atual;
  }
  return saida;
}

/** Junta os feitos de uma batalha ao que o personagem já tinha. */
export function somarFeitos(antes: Feitos, novos: Feitos): Feitos {
  const saida: Feitos = { ...antes };
  for (const [chave, valor] of Object.entries(novos) as [Feito, number][]) {
    /* O maior golpe é recorde; o resto soma. */
    saida[chave] = chave === 'explodiu' ? Math.max(saida[chave] ?? 0, valor) : (saida[chave] ?? 0) + valor;
  }
  return saida;
}
