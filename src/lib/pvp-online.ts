import type { RealtimeChannel, SupabaseClient } from '@supabase/supabase-js';

/*
 * O PvP online no aparelho: os pedidos ao juiz (ranked-api, ação "pvp": supabase/functions/ranked-api/pvp.ts) e o
 * aviso na hora quando a partida muda (Realtime na tabela pvp_partidas, que só mostra aos dois da partida o que não é
 * segredo). O que cada um vê da partida (VistaPvp) vem sempre do servidor: os times do rival só depois dos dois
 * prontos, a escolha dele só depois dos dois escolherem.
 */
export interface JogadorPvp { id: string; nome: string; rating: number; vitorias: number; derrotas: number }
export interface RodadaVista { n: number; meu: number; dele: number; seed: number; vencedor: 'eu' | 'rival'; duracao: number; rendida?: boolean }
export interface VistaPvp {
  id: string; fase: 'convite' | 'montando' | 'jogando' | 'terminada' | 'recusada' | 'cancelada' | 'expirada';
  eu: 'a' | 'b'; desafiante: boolean; seed: number; versao: string; agora: string; prazo: string; criada: string;
  voce: JogadorPvp; rival: JogadorPvp;
  pronto: { eu: boolean; rival: boolean }; escolheu: { eu: boolean; rival: boolean }; lutar: { eu: boolean; rival: boolean }; assistiu: { eu: boolean; rival: boolean };
  rodada: number; resolvida: number; inicioEm: string | null;
  meusTimes: string[][] | null; timesDele: string[][] | null; minhaEscolha: number | null;
  rodadas: RodadaVista[];
  vencedor: 'eu' | 'rival' | null; motivo: string | null; delta: number | null;
  /** Há quantos segundos o rival não dá notícia (null: está na partida) e o máximo antes de perder. */
  ausencia: number | null; ausenciaMaxima: number;
}
export interface RespostaPvp { partida: VistaPvp | null; colecao: string[] }
export interface RankingPvp { ranking: { posicao: number; id: string; nome: string; rating: number; vitorias: number; derrotas: number }[]; eu: { rating: number; vitorias: number; derrotas: number }; colecao: number }

/* O Caminho do Nexus (a campanha contra os 40 rivais, src/engine/campanha.ts): o juiz é o servidor (ação "campanha"). */
export interface ProgressoDaCampanha {
  estrelas: Record<string, number>; placar: Record<string, { v: number; d: number }>;
  /** Quem descansa (id → partidas que faltam): os seus e os de cada rival. */
  descanso: Record<string, number>; descanso_rivais: Record<string, Record<string, number>>; partidas: number;
}
export interface PartidaDaCampanha {
  id: string; rival: string; estado: 'jogando' | 'terminada'; versao: string; meus: string[][]; deles: string[][];
  rodadas: { meu: number; dele: number; seed: number; vencedor: 'eu' | 'rival'; rendida?: boolean }[];
  vencedor: 'eu' | 'rival' | null; motivo: string | null; estrelas: number | null; ratingAntes: number | null; delta: number | null; rating?: number;
}
export interface RespostaDaCampanha { progresso: ProgressoDaCampanha; rating: { rating: number; vitorias: number; derrotas: number }; colecao: string[]; partida: PartidaDaCampanha | null }
export interface ServicoDaCampanha {
  estado: () => Promise<RespostaDaCampanha>;
  comecar: (rival: string, times: string[][], versao: string) => Promise<RespostaDaCampanha>;
  escolher: (partida: string, n: number, time: number) => Promise<RespostaDaCampanha>;
  render: (partida: string, n: number) => Promise<RespostaDaCampanha>;
  abandonar: (partida: string) => Promise<RespostaDaCampanha>;
}

export interface ServicoPvp {
  campanha: ServicoDaCampanha;
  /** A partida (a pedida, ou a aberta de agora). */
  consultar: (partida?: string | null) => Promise<RespostaPvp>;
  desafiar: (alvo: string) => Promise<RespostaPvp>;
  responder: (partida: string, aceitar: boolean) => Promise<RespostaPvp>;
  times: (partida: string, times: string[][]) => Promise<RespostaPvp>;
  escolher: (partida: string, n: number, time: number) => Promise<RespostaPvp>;
  lutar: (partida: string) => Promise<RespostaPvp>;
  /** Terminei de assistir a luta da rodada n (o tempo de escolher a próxima começa quando os dois terminam). */
  assisti: (partida: string, n: number) => Promise<RespostaPvp>;
  /** Desiste da partida inteira. */
  desistir: (partida: string) => Promise<RespostaPvp>;
  /** Desiste só da luta da rodada n (perde a rodada; a partida segue). */
  render: (partida: string, n: number) => Promise<RespostaPvp>;
  ranking: () => Promise<RankingPvp>;
  /** Avisa quando uma partida minha muda (ou nasce: um convite). */
  ouvir: (aviso: (linha: { id: string; desafiante: string; desafiado: string; fase: string }) => void) => () => void;
}

export function criarPvpOnline(chamar: <T>(acao: string, corpo: Record<string, unknown>) => Promise<T>, carregar: () => Promise<SupabaseClient | null>): ServicoPvp {
  const pvp = <T,>(op: string, corpo: Record<string, unknown> = {}) => chamar<T>('pvp', { op, ...corpo });
  const campanha = (op: string, corpo: Record<string, unknown> = {}) => chamar<RespostaDaCampanha>('campanha', { op, ...corpo });
  return {
    campanha: {
      estado: () => campanha('estado'),
      comecar: (rival, times, versao) => campanha('comecar', { rival, times, versao }),
      escolher: (partida, n, time) => campanha('escolher', { partida, n, time }),
      render: (partida, n) => campanha('render', { partida, n }),
      abandonar: (partida) => campanha('abandonar', { partida }),
    },
    consultar: (partida) => pvp('estado', partida ? { partida } : {}),
    desafiar: (alvo) => pvp('desafiar', { alvo }),
    responder: (partida, aceitar) => pvp('responder', { partida, aceitar }),
    times: (partida, times) => pvp('times', { partida, times }),
    escolher: (partida, n, time) => pvp('escolher', { partida, n, time }),
    lutar: (partida) => pvp('lutar', { partida }),
    assisti: (partida, n) => pvp('assisti', { partida, n }),
    desistir: (partida) => pvp('desistir', { partida }),
    render: (partida, n) => pvp('render', { partida, n }),
    ranking: () => pvp('ranking'),
    ouvir: (aviso) => {
      let canal: RealtimeChannel | null = null, parado = false;
      void carregar().then((c) => {
        if (!c || parado) return;
        canal = c.channel(`pvp-${Math.random().toString(36).slice(2)}`)
          .on('postgres_changes', { event: '*', schema: 'public', table: 'pvp_partidas' }, (p) => {
            const l = (p.new ?? {}) as { id?: string; desafiante?: string; desafiado?: string; estado?: string };
            if (l.id && l.desafiante && l.desafiado && l.estado) aviso({ id: l.id, desafiante: l.desafiante, desafiado: l.desafiado, fase: l.estado });
          })
          .subscribe();
      }).catch(() => undefined);
      return () => { parado = true; if (canal) void canal.unsubscribe(); };
    },
  };
}

/** O relógio do servidor (para os dois aparelhos começarem a luta juntos). */
export const diferencaDoRelogio = (agoraNoServidor: string) => Date.parse(agoraNoServidor) - Date.now();

/** Os erros do juiz já vêm em frase de gente; só a falta de rede ganha uma. */
export const textoDoErroPvp = (e: unknown) => {
  const m = e instanceof Error ? e.message : '';
  return /fetch|network|Failed|conexão/i.test(m) ? 'Sem conexão com o servidor. Confira a internet.' : m || 'Não deu certo agora. Tente de novo.';
};
