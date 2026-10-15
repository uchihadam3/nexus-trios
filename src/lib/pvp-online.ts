import type { RealtimeChannel, SupabaseClient } from '@supabase/supabase-js';

/*
 * O PvP online no aparelho: os pedidos ao juiz (ranked-api, ação "pvp": supabase/functions/ranked-api/pvp.ts) e o
 * aviso na hora quando a partida muda (Realtime na tabela pvp_partidas, que só mostra aos dois da partida o que não é
 * segredo). O que cada um vê da partida (VistaPvp) vem sempre do servidor: os times do rival só depois dos dois
 * prontos, a escolha dele só depois dos dois escolherem.
 */
export interface JogadorPvp { id: string; nome: string; rating: number; vitorias: number; derrotas: number }
export interface RodadaVista { n: number; meu: number; dele: number; seed: number; vencedor: 'eu' | 'rival'; duracao: number }
export interface VistaPvp {
  id: string; fase: 'convite' | 'montando' | 'jogando' | 'terminada' | 'recusada' | 'cancelada' | 'expirada';
  eu: 'a' | 'b'; desafiante: boolean; seed: number; versao: string; agora: string; prazo: string; criada: string;
  voce: JogadorPvp; rival: JogadorPvp;
  pronto: { eu: boolean; rival: boolean }; escolheu: { eu: boolean; rival: boolean }; lutar: { eu: boolean; rival: boolean }; assistiu: { eu: boolean; rival: boolean };
  rodada: number; resolvida: number; inicioEm: string | null;
  meusTimes: string[][] | null; timesDele: string[][] | null; minhaEscolha: number | null;
  rodadas: RodadaVista[];
  vencedor: 'eu' | 'rival' | null; motivo: string | null; delta: number | null;
}
export interface RespostaPvp { partida: VistaPvp | null; colecao: string[] }
export interface RankingPvp { ranking: { posicao: number; id: string; nome: string; rating: number; vitorias: number; derrotas: number }[]; eu: { rating: number; vitorias: number; derrotas: number }; colecao: number }

export interface ServicoPvp {
  /** A partida (a pedida, ou a aberta de agora). */
  consultar: (partida?: string | null) => Promise<RespostaPvp>;
  desafiar: (alvo: string) => Promise<RespostaPvp>;
  responder: (partida: string, aceitar: boolean) => Promise<RespostaPvp>;
  times: (partida: string, times: string[][]) => Promise<RespostaPvp>;
  escolher: (partida: string, n: number, time: number) => Promise<RespostaPvp>;
  lutar: (partida: string) => Promise<RespostaPvp>;
  /** Terminei de assistir a luta da rodada n (o tempo de escolher a próxima começa quando os dois terminam). */
  assisti: (partida: string, n: number) => Promise<RespostaPvp>;
  desistir: (partida: string) => Promise<RespostaPvp>;
  ranking: () => Promise<RankingPvp>;
  /** Avisa quando uma partida minha muda (ou nasce: um convite). */
  ouvir: (aviso: (linha: { id: string; desafiante: string; desafiado: string; fase: string }) => void) => () => void;
}

export function criarPvpOnline(chamar: <T>(acao: string, corpo: Record<string, unknown>) => Promise<T>, carregar: () => Promise<SupabaseClient | null>): ServicoPvp {
  const pvp = <T,>(op: string, corpo: Record<string, unknown> = {}) => chamar<T>('pvp', { op, ...corpo });
  return {
    consultar: (partida) => pvp('estado', partida ? { partida } : {}),
    desafiar: (alvo) => pvp('desafiar', { alvo }),
    responder: (partida, aceitar) => pvp('responder', { partida, aceitar }),
    times: (partida, times) => pvp('times', { partida, times }),
    escolher: (partida, n, time) => pvp('escolher', { partida, n, time }),
    lutar: (partida) => pvp('lutar', { partida }),
    assisti: (partida, n) => pvp('assisti', { partida, n }),
    desistir: (partida) => pvp('desistir', { partida }),
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
