/*
 * FASE G · o Raio-X do Trio.
 *
 * Depois de toda batalha, ganhando ou perdendo, o jogador precisa aprender
 * alguma coisa sobre a combinação que montou. O que existia antes media uma
 * coisa só — Carga passada entre aliados — e chamava isso de "a ligação mais
 * frequente".
 *
 * A regra que governa este arquivo está escrita no documento da direção em
 * cinco palavras: **não inventar causalidade que não aconteceu**. Então nada
 * aqui é inferido do desenho dos personagens. Todo elo nasce de eventos que o
 * motor de fato emitiu, e os que dependem de um Status estar ativo conferem a
 * duração real que o motor registra no evento, em vez de supor uma janela.
 *
 * O acumulador roda junto da batalha, alimentado com os eventos de cada quadro.
 * Isso é necessário, não preferência: `battle.events` guarda só os 180 últimos,
 * então uma leitura feita no fim da luta já teria perdido o começo dela.
 */
import { byId } from '../data/characters';
import { statuses } from '../data/statuses';
import type { Battle, BattleEvent, StatusId } from './types';

/* ---------------------------------------------------------------------------
 * Os tipos de elo, e o que prova cada um
 * ------------------------------------------------------------------------- */

export type TipoDeElo =
  | 'carga'            /* A fez a Carga de B subir */
  | 'cura'             /* A devolveu Vida a B */
  | 'escudo'           /* A deu Escudo a B */
  | 'aceleracao'       /* A deixou B mais rápido */
  | 'reforco'          /* A pôs um Status positivo em B */
  | 'preparo-protegido'/* A protegeu B enquanto B preparava uma habilidade */
  | 'alvo-preparado'   /* A deixou um inimigo vulnerável e B aproveitou */
  | 'finalizacao'      /* A deixou um inimigo vulnerável e B o derrubou */
  | 'controle'         /* A travou um inimigo que estava preparando algo */
  | 'conflito';        /* A prejudicou B — ver a nota no fim do arquivo */

export interface Elo { de: string; para: string; tipo: TipoDeElo; vezes: number; valor: number }

/** O estado que o acumulador carrega entre os quadros da batalha. */
export interface EstadoRaioX {
  elos: Elo[];
  /** Status negativos vivos em inimigos: quem aplicou e até quando vale. */
  marcas: { alvo: string; status: StatusId; de: string; ate: number }[];
  /** Quem está preparando uma habilidade agora, e desde quando. */
  preparando: { uid: string; desde: number }[];
  /** Dano que cada lutador do trio absorveu. */
  absorvido: Record<string, number>;
  /** Último instante visto, para expirar marcas. */
  tempo: number;
}

export const raioXVazio = (): EstadoRaioX =>
  ({ elos: [], marcas: [], preparando: [], absorvido: {}, tempo: 0 });

/* Os que abrem o inimigo para o golpe de outro. */
const VULNERABILIZA = new Set<StatusId>(['exposed', 'marked', 'electric', 'weakened']);
/* Os que tiram o turno do inimigo. */
const TRAVA = new Set<StatusId>(['paralyzed', 'frozen', 'sleep', 'rooted', 'silenced', 'confused', 'blind']);

const doTrio = (uid: string) => uid.startsWith('player-');

/* ---------------------------------------------------------------------------
 * O acumulador
 * ------------------------------------------------------------------------- */

/**
 * Lê os eventos novos de um quadro e devolve o estado atualizado.
 *
 * Puro: não altera o estado recebido, e o mesmo par (estado, eventos) sempre
 * produz o mesmo resultado.
 */
export function acumularRaioX(estado: EstadoRaioX, eventos: readonly BattleEvent[], battle: Battle): EstadoRaioX {
  if (eventos.length === 0) return estado;

  const elos = estado.elos.map((e) => ({ ...e }));
  let marcas = estado.marcas.map((m) => ({ ...m }));
  let preparando = estado.preparando.map((p) => ({ ...p }));
  const absorvido = { ...estado.absorvido };
  let tempo = estado.tempo;

  const lado = (uid: string) => battle.fighters.find((f) => f.uid === uid)?.side;
  const ligar = (de: string, para: string, tipo: TipoDeElo, valor = 0) => {
    if (!de || !para || de === para || !doTrio(de) || !doTrio(para)) return;
    const existente = elos.find((e) => e.de === de && e.para === para && e.tipo === tipo);
    if (existente) { existente.vezes += 1; existente.valor += valor; }
    else elos.push({ de, para, tipo, vezes: 1, valor });
  };

  for (const ev of eventos) {
    tempo = Math.max(tempo, ev.time);
    /* Marcas vencidas saem antes de qualquer pergunta sobre elas. */
    marcas = marcas.filter((m) => m.ate > ev.time);

    switch (ev.kind) {
      /* A Carga que um aliado fez subir: o motor já identifica a fonte. */
      case 'synergy': if (ev.target) ligar(ev.source, ev.target, 'carga', ev.value ?? 0); break;

      case 'heal': if (ev.target && doTrio(ev.target)) ligar(ev.source, ev.target, 'cura', ev.value ?? 0); break;
      case 'shield': if (ev.target && doTrio(ev.target)) ligar(ev.source, ev.target, 'escudo', ev.value ?? 0); break;

      case 'cast': preparando = [...preparando.filter((p) => p.uid !== ev.source), { uid: ev.source, desde: ev.time }]; break;
      case 'skill': preparando = preparando.filter((p) => p.uid !== ev.source); break;

      case 'status': {
        const alvo = ev.target, id = ev.status;
        if (!alvo || !id) break;
        const duracao = ev.value ?? 0;
        if (lado(ev.source) === lado(alvo)) {
          /* Apoio: só conta quando sai de um aliado para outro. */
          if (statuses[id].tone !== 'positivo') { ligar(ev.source, alvo, 'conflito', duracao); break; }
          if (id === 'haste') ligar(ev.source, alvo, 'aceleracao', duracao);
          else if (id === 'protected' && preparando.some((p) => p.uid === alvo)) {
            /*
             * Protegido resiste a interrupções, então pôr Protegido em alguém
             * que está no meio do Preparo é defender aquela habilidade — e
             * esta é a única leitura em que isso é afirmado, porque é a única
             * em que o Preparo estava de fato em andamento.
             */
            ligar(ev.source, alvo, 'preparo-protegido', duracao);
          } else ligar(ev.source, alvo, 'reforco', duracao);
        } else {
          /* Debuff em inimigo: vira marca, para responder a quem aproveitou. */
          if (VULNERABILIZA.has(id) || TRAVA.has(id)) {
            marcas = [...marcas.filter((m) => !(m.alvo === alvo && m.status === id)),
              { alvo, status: id, de: ev.source, ate: ev.time + duracao }];
          }
          if (TRAVA.has(id)) {
            /* Travar quem estava preparando algo compra tempo para o trio. */
            const vitima = preparando.find((p) => p.uid === alvo);
            if (vitima) for (const f of battle.fighters) {
              if (f.side === lado(ev.source) && f.uid !== ev.source) ligar(ev.source, f.uid, 'controle', duracao);
            }
          }
        }
        break;
      }

      case 'damage': {
        const alvo = ev.target;
        if (!alvo) break;
        if (doTrio(alvo) && lado(ev.source) !== 'player') absorvido[alvo] = (absorvido[alvo] ?? 0) + (ev.value ?? 0);
        if (!doTrio(ev.source) || doTrio(alvo)) break;
        /* Quem abriu este inimigo antes deste golpe leva o crédito do elo. */
        for (const m of marcas) {
          if (m.alvo !== alvo || !VULNERABILIZA.has(m.status)) continue;
          ligar(m.de, ev.source, 'alvo-preparado', ev.value ?? 0);
        }
        break;
      }

      case 'ko': {
        const alvo = ev.target;
        if (!alvo || doTrio(alvo) || !doTrio(ev.source)) break;
        for (const m of marcas) {
          if (m.alvo !== alvo) continue;
          ligar(m.de, ev.source, 'finalizacao', 1);
        }
        break;
      }
      default: break;
    }
  }

  return { elos, marcas, preparando, absorvido, tempo };
}

/* ---------------------------------------------------------------------------
 * A leitura: de elos para o que o jogador vê
 * ------------------------------------------------------------------------- */

export type Classificacao = 'ÓTIMA CONEXÃO' | 'BOA CONEXÃO' | 'POUCA CONEXÃO' | 'INDEPENDENTES' | 'CONFLITO';

export interface Direcao { de: string; para: string; elos: Elo[]; frase: string | null; destaque: Destaque | null; tipo: TipoDeElo | null }
export interface Par { a: string; b: string; classificacao: Classificacao; aParaB: Direcao; bParaA: Direcao; total: number }

/*
 * Como cada ajuda se conta para o jogador.
 *
 * A primeira versão contava eventos: "encheu a Carga de Coragem 233 vezes
 * (148% no total)". Os 233 eram pedacinhos de Carga de um traço que dispara a
 * cada poucos décimos de segundo — um número que não diz nada a quem joga. O
 * que importa é o efeito: 148% de Carga são uma habilidade e meia a mais.
 * Cada ajuda tem agora um número em destaque e uma frase curta.
 */
export interface Destaque { numero: string; rotulo: string }
const n0 = (x: number) => Math.round(x).toLocaleString('pt-BR');
const habilidades = (pct: number) => {
  const h = pct / 100;
  const arred = Math.round(h * 2) / 2;
  return `${arred.toLocaleString('pt-BR')} ${arred === 1 ? 'habilidade' : 'habilidades'} a mais`;
};
const FRASES: Record<TipoDeElo, (n: number, v: number, o: string) => { frase: string; destaque: Destaque }> = {
  'carga': (_n, v, o) => ({ frase: v < 95 ? `encheu ${Math.round(v)}% de uma habilidade de ${o}` : `fez ${o} usar ${habilidades(v)}`, destaque: { numero: `+${n0(v)}%`, rotulo: 'de Carga' } }),
  'cura': (_n, v, o) => ({ frase: `curou ${o}`, destaque: { numero: `+${n0(v)}`, rotulo: 'de Vida' } }),
  'escudo': (_n, v, o) => ({ frase: `protegeu ${o} com Escudo`, destaque: { numero: n0(v), rotulo: 'de Escudo' } }),
  'aceleracao': (n, _v, o) => ({ frase: `deixou ${o} mais rápido`, destaque: { numero: `${n}×`, rotulo: 'Acelerado' } }),
  'reforco': (n, _v, o) => ({ frase: `deixou ${o} mais forte`, destaque: { numero: `${n}×`, rotulo: 'reforçado' } }),
  'preparo-protegido': (n, _v, o) => ({ frase: `segurou o rival enquanto ${o} preparava`, destaque: { numero: `${n}`, rotulo: n === 1 ? 'Preparo salvo' : 'Preparos salvos' } }),
  'alvo-preparado': (n, _v, o) => ({ frase: `deixou o alvo vulnerável para ${o}`, destaque: { numero: `${n}`, rotulo: n === 1 ? 'golpe a mais forte' : 'golpes mais fortes' } }),
  'finalizacao': (n, _v, o) => ({ frase: `deixou o alvo vulnerável e ${o} derrubou`, destaque: { numero: `${n}`, rotulo: n === 1 ? 'rival derrubado' : 'rivais derrubados' } }),
  'controle': (n, _v, o) => ({ frase: `travou golpes rivais e deu tempo a ${o}`, destaque: { numero: `${n}`, rotulo: n === 1 ? 'golpe travado' : 'golpes travados' } }),
  'conflito': (n, _v, o) => ({ frase: `atrapalhou ${o}`, destaque: { numero: `${n}×`, rotulo: 'atrapalhou' } }),
};

/* Quanto cada elo pesa na classificação: ajudar a derrubar vale mais que um empurrão. */
const PESO: Record<TipoDeElo, number> = {
  'finalizacao': 3, 'preparo-protegido': 2.5, 'controle': 2, 'alvo-preparado': 1.4,
  'cura': 1.2, 'escudo': 1.2, 'aceleracao': 1, 'reforco': 1, 'carga': 0.8, 'conflito': 0,
};

/*
 * Os cortes, tirados da distribuição real.
 *
 * A primeira versão usava números escolhidos a dedo e 56% dos pares saíam como
 * "ÓTIMA CONEXÃO" — o mesmo defeito do "Dano" que valia para 250 de 250: um
 * rótulo que descreve a maioria não separa ninguém.
 *
 * Medindo 360 pares em 120 lutas (`scripts/medir-raiox.ts`), a força do par
 * ficou assim: p10 = 4, mediana = 16, p75 = 41, p90 = 84. Os cortes seguem
 * essa régua — "ótima" é o topo, "boa" é da mediana para cima, e o resto é
 * pouca conexão em vez de problema.
 */
const OTIMA = 60;
const BOA = 16;

const nomeDe = (uid: string, battle: Battle) => {
  const f = battle.fighters.find((x) => x.uid === uid);
  return f ? byId[f.characterId]?.name ?? f.characterId : uid;
};

const direcao = (elos: Elo[], de: string, para: string, battle: Battle): Direcao => {
  const meus = elos.filter((e) => e.de === de && e.para === para && e.tipo !== 'conflito')
    .sort((a, b) => b.vezes * PESO[b.tipo] - a.vezes * PESO[a.tipo]);
  const principal = meus[0];
  const lido = principal ? FRASES[principal.tipo](principal.vezes, principal.valor, nomeDe(para, battle)) : null;
  return { de, para, elos: meus, frase: lido?.frase ?? null, destaque: lido?.destaque ?? null, tipo: principal?.tipo ?? null };
};

/**
 * As seis direções do trio, agrupadas nos três pares.
 *
 * A classificação segue a escala do documento, com uma regra que ele deixou
 * explícita: *"Não chamar dupla neutra de ruim."* Duas pessoas que lutaram bem
 * sem ativar mecânica uma da outra são **INDEPENDENTES**, não um problema.
 */
export function lerRaioX(estado: EstadoRaioX, battle: Battle): Par[] {
  const trio = battle.fighters.filter((f) => f.side === 'player').map((f) => f.uid);
  const pares: Par[] = [];
  for (let i = 0; i < trio.length; i += 1) {
    for (let j = i + 1; j < trio.length; j += 1) {
      const a = trio[i]!, b = trio[j]!;
      const aParaB = direcao(estado.elos, a, b, battle), bParaA = direcao(estado.elos, b, a, battle);
      const conflito = estado.elos.some((e) => e.tipo === 'conflito'
        && ((e.de === a && e.para === b) || (e.de === b && e.para === a)));
      const força = [...aParaB.elos, ...bParaA.elos].reduce((n, e) => n + e.vezes * PESO[e.tipo], 0);
      const mãoDupla = aParaB.elos.length > 0 && bParaA.elos.length > 0;
      const classificacao: Classificacao = conflito ? 'CONFLITO'
        : força >= OTIMA && mãoDupla ? 'ÓTIMA CONEXÃO'
          : força >= BOA ? 'BOA CONEXÃO'
            : força > 0 ? 'POUCA CONEXÃO'
              : 'INDEPENDENTES';
      pares.push({ a, b, classificacao, aParaB, bParaA, total: Math.round(força) });
    }
  }
  return pares.sort((x, y) => y.total - x.total);
}

/** Quem segurou a pressão: o lutador do trio que mais apanhou. */
export function quemAbsorveu(estado: EstadoRaioX, battle: Battle): { uid: string; dano: number; parte: number } | null {
  const total = Object.values(estado.absorvido).reduce((a, b) => a + b, 0);
  if (total <= 0) return null;
  const [uid, dano] = Object.entries(estado.absorvido).sort((a, b) => b[1] - a[1])[0]!;
  void battle;
  return { uid, dano: Math.round(dano), parte: dano / total };
}

/*
 * Sobre "CONFLITO".
 *
 * O documento pede a classificação e acrescenta: *"somente quando houver
 * conflito mecânico real"*. A detecção está implementada acima — um Status
 * negativo saindo de um aliado para outro — e, hoje, ela não encontra nada.
 *
 * Não é descuido: depois que a FASE E corrigiu os 80 efeitos ofensivos que
 * herdavam alvo aliado, nenhum personagem prejudica um companheiro. O único
 * jeito de um lutador atingir o próprio lado é a Confusão, e o motor a
 * resolve mandando o golpe nele mesmo, nunca num aliado. Os quinze custos
 * declarados também são sempre `self`.
 *
 * A detecção fica porque é barata e porque o dia em que alguém escrever uma
 * mecânica de fogo amigo, o Raio-X vai contar em vez de ficar calado.
 */
