import type { RealtimeChannel, SupabaseClient } from '@supabase/supabase-js';

/*
 * A Comunidade: quem está online, o chat global e as mensagens privadas com "visto".
 *
 * O banco (supabase/migrations/20261015000000_comunidade.sql) só deixa o navegador LER o que lhe cabe; toda escrita
 * vai pelas funções de lá (enviar, marcar como vista, reagir, presença), que conferem quem está mandando. Mensagens,
 * vistos e reações chegam na hora pelo Realtime, filtrados pelas mesmas regras. "Digitando…" é só um aviso de passagem
 * (broadcast), não fica guardado.
 *
 * As telas falam com `ServicoDaComunidade`, não com o Supabase: assim a tela roda nos testes e na prévia com uma
 * comunidade de mentira (src/lib/comunidade-demo.ts), sem servidor.
 */

export interface Jogador {
  id: string; nome: string; online: boolean;
  /** Desde quando está online (só vale com `online`). */
  onlineDesde: string | null;
  /** A última vez que o jogo dele marcou presença (ou a hora em que saiu). Null: nunca abriu o jogo desde a Comunidade. */
  vistoEm: string | null;
  recorde: number | null; trio: string[] | null; conquistas: number;
  /** Quando a conta nasceu. */
  desde: string;
  /** Quantas jornadas terminou (contadas no servidor). */
  jornadas: number;
}
export interface Mensagem { id: number; autorId: string; paraId: string | null; texto: string; respostaA: number | null; criadaEm: string; vistaEm: string | null }
export interface Reacao { mensagemId: number; playerId: string; emoji: string | null }
export interface Conversa { comId: string; comNome: string; ultimaId: number; ultimaTexto: string; ultimaEm: string; ultimaMinha: boolean; ultimaVista: boolean; naoLidas: number }
export interface Ouvintes {
  mensagem?: (m: Mensagem, tipo: 'nova' | 'mudou') => void;
  reacao?: (r: Reacao) => void;
  /** Alguém digitando: `onde` é null no global, ou o id de quem recebe na privada. */
  digitando?: (quem: string, onde: string | null) => void;
}
export interface ServicoDaComunidade {
  jogadores: () => Promise<Jogador[]>;
  /** As últimas mensagens do global (`com` null) ou da privada com `com`; `antesDe` busca as mais antigas. */
  historico: (com: string | null, antesDe?: number) => Promise<{ mensagens: Mensagem[]; reacoes: Reacao[]; temMais: boolean }>;
  enviar: (texto: string, para?: string | null, respostaA?: number | null) => Promise<Mensagem>;
  marcarVistas: (de: string) => Promise<void>;
  reagir: (mensagemId: number, emoji: string) => Promise<void>;
  conversas: () => Promise<Conversa[]>;
  ping: () => Promise<void>;
  sair: () => Promise<void>;
  ouvir: (o: Ouvintes) => () => void;
  avisarDigitando: (onde: string | null) => void;
}

export const EMOJIS_DAS_REACOES = ['🔥', '😂', '👏', '😮', '💀', '❤️'] as const;
export const LIMITE_DA_MENSAGEM = 500;
/** De quanto em quanto tempo o jogo aberto marca presença (o banco dá 75 s antes de considerar offline). */
export const PULSO_DA_PRESENCA_MS = 30_000;
const POR_PAGINA = 60;
const ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** As mensagens de erro do banco ("chat: devagar…") viram frase de gente. */
export function textoDoErro(e: unknown): string {
  const m = e instanceof Error ? e.message : typeof e === 'object' && e && 'message' in e ? String((e as { message: unknown }).message) : '';
  if (/devagar/.test(m)) return 'Calma! Espere uns segundos antes de mandar outra.';
  if (/repetida/.test(m)) return 'Você acabou de mandar essa mesma mensagem.';
  if (/escolha seu nome/.test(m)) return 'Escolha seu nome público para entrar na Comunidade.';
  if (/500/.test(m)) return `A mensagem pode ter até ${LIMITE_DA_MENSAGEM} letras.`;
  if (/vazia/.test(m)) return 'Escreva alguma coisa antes de mandar.';
  if (/destinat|resposta|não encontrada/.test(m)) return 'Essa conversa não está mais disponível.';
  if (/fetch|network|Failed/i.test(m)) return 'Sem conexão. Confira a internet e tente de novo.';
  return 'Não deu certo agora. Tente de novo em instantes.';
}

type LinhaMensagem = { id: number | string; autor_id: string; para_id: string | null; texto: string; resposta_a: number | string | null; criada_em: string; vista_em: string | null };
const mensagemDe = (r: LinhaMensagem): Mensagem => ({ id: Number(r.id), autorId: r.autor_id, paraId: r.para_id, texto: r.texto, respostaA: r.resposta_a === null ? null : Number(r.resposta_a), criadaEm: r.criada_em, vistaEm: r.vista_em });
type LinhaReacao = { mensagem_id: number | string; player_id: string; emoji: string | null };
const reacaoDe = (r: LinhaReacao): Reacao => ({ mensagemId: Number(r.mensagem_id), playerId: r.player_id, emoji: r.emoji });

export function criarComunidade(carregar: () => Promise<SupabaseClient | null>, eu: () => string | null): ServicoDaComunidade {
  const cliente = async () => { const c = await carregar(); if (!c) throw new Error('offline'); return c; };
  const rpc = async <T,>(nome: string, args: Record<string, unknown> = {}): Promise<T> => {
    const { data, error } = await (await cliente()).rpc(nome, args);
    if (error) throw new Error(error.message);
    return data as T;
  };
  /* Um canal só de "digitando…" para o jogo inteiro; cada tela aberta só se inscreve para ouvir. */
  const quemOuveDigitar = new Set<NonNullable<Ouvintes['digitando']>>();
  let digitar: Promise<RealtimeChannel> | null = null;
  const canalDeDigitar = () => digitar ??= cliente().then((c) => c.channel('comunidade-digitando', { config: { broadcast: { self: false } } })
    .on('broadcast', { event: 'digitando' }, ({ payload }) => {
      const p = payload as { de?: unknown; para?: unknown };
      if (typeof p.de !== 'string') return;
      const para = typeof p.para === 'string' ? p.para : null;
      // privada: só interessa a quem recebe, e aparece na conversa com quem está digitando
      if (para !== null && para !== eu()) return;
      for (const f of quemOuveDigitar) f(p.de, para === null ? null : p.de);
    })
    .subscribe()).catch((e: unknown) => { digitar = null; throw e; });

  return {
    jogadores: async () => (await rpc<{ id: string; nome: string; online: boolean; online_desde: string | null; visto_em: string | null; recorde: number | null; trio: string[] | null; conquistas: number; desde: string; jornadas?: number }[]>('comunidade_jogadores'))
      .map((j) => ({ id: j.id, nome: j.nome, online: j.online, onlineDesde: j.online_desde, vistoEm: j.visto_em, recorde: j.recorde, trio: j.trio, conquistas: j.conquistas, desde: j.desde, jornadas: j.jornadas ?? 0 })),

    historico: async (com, antesDe) => {
      const c = await cliente(), meu = eu();
      // os ids entram no filtro do PostgREST: só passam se forem ids mesmo
      if (com !== null && (!ID.test(com) || !meu || !ID.test(meu))) throw new Error('destinatário inválido');
      let q = c.from('chat_mensagens').select('*').order('id', { ascending: false }).limit(POR_PAGINA + 1);
      q = com === null ? q.is('para_id', null) : q.or(`and(autor_id.eq.${meu},para_id.eq.${com}),and(autor_id.eq.${com},para_id.eq.${meu})`);
      if (antesDe) q = q.lt('id', antesDe);
      const { data, error } = await q;
      if (error) throw new Error(error.message);
      const linhas = (data ?? []) as LinhaMensagem[], temMais = linhas.length > POR_PAGINA;
      const mensagens = linhas.slice(0, POR_PAGINA).map(mensagemDe).reverse();
      if (!mensagens.length) return { mensagens, reacoes: [], temMais };
      const r = await c.from('chat_reacoes').select('mensagem_id,player_id,emoji').in('mensagem_id', mensagens.map((m) => m.id)).not('emoji', 'is', null);
      if (r.error) throw new Error(r.error.message);
      return { mensagens, reacoes: ((r.data ?? []) as LinhaReacao[]).map(reacaoDe), temMais };
    },

    enviar: async (texto, para = null, respostaA = null) => mensagemDe(await rpc<LinhaMensagem>('chat_enviar', { p_texto: texto, p_para: para, p_resposta: respostaA })),
    marcarVistas: async (de) => { await rpc('chat_marcar_vistas', { p_de: de }); },
    reagir: async (mensagemId, emoji) => { await rpc('chat_reagir', { p_mensagem: mensagemId, p_emoji: emoji }); },
    conversas: async () => (await rpc<{ com_id: string; com_nome: string; ultima_id: number; ultima_texto: string; ultima_em: string; ultima_minha: boolean; ultima_vista: boolean; nao_lidas: number }[]>('chat_conversas'))
      .map((c) => ({ comId: c.com_id, comNome: c.com_nome, ultimaId: Number(c.ultima_id), ultimaTexto: c.ultima_texto, ultimaEm: c.ultima_em, ultimaMinha: c.ultima_minha, ultimaVista: c.ultima_vista, naoLidas: c.nao_lidas })),
    ping: async () => { await rpc('comunidade_ping'); },
    sair: async () => { await rpc('comunidade_sair'); },

    ouvir: (o) => {
      let canal: RealtimeChannel | null = null, parado = false;
      void cliente().then((c) => {
        if (parado) return;
        canal = c.channel(`comunidade-${Math.random().toString(36).slice(2)}`)
          .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'chat_mensagens' }, (p) => o.mensagem?.(mensagemDe(p.new as LinhaMensagem), 'nova'))
          .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'chat_mensagens' }, (p) => o.mensagem?.(mensagemDe(p.new as LinhaMensagem), 'mudou'))
          .on('postgres_changes', { event: '*', schema: 'public', table: 'chat_reacoes' }, (p) => { if (p.new && 'mensagem_id' in p.new) o.reacao?.(reacaoDe(p.new as LinhaReacao)); })
          .subscribe();
      }).catch(() => undefined);
      const digitando = o.digitando;
      if (digitando) { quemOuveDigitar.add(digitando); void canalDeDigitar().catch(() => undefined); }
      return () => { parado = true; if (canal) void canal.unsubscribe(); if (digitando) quemOuveDigitar.delete(digitando); };
    },

    avisarDigitando: (onde) => {
      const meu = eu();
      if (!meu) return;
      void canalDeDigitar().then((c) => c.send({ type: 'broadcast', event: 'digitando', payload: { de: meu, para: onde } })).catch(() => undefined);
    },
  };
}

/* ---------------------------------------------------------------------------
 * Tempo, do jeito que a gente fala
 * ------------------------------------------------------------------------- */

const doisDigitos = (n: number) => String(n).padStart(2, '0');
export const hora = (iso: string) => { const d = new Date(iso); return `${doisDigitos(d.getHours())}:${doisDigitos(d.getMinutes())}`; };
const mesmoDia = (a: Date, b: Date) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

/** "agora", "há 5 min", "há 2 h", "há 3 dias"… */
export function haQuanto(iso: string, agora = Date.now()): string {
  const s = Math.max(0, (agora - new Date(iso).getTime()) / 1000);
  if (s < 45) return 'agora';
  if (s < 3600) return `há ${Math.max(1, Math.round(s / 60))} min`;
  if (s < 86400) return `há ${Math.floor(s / 3600)} h`;
  const d = Math.floor(s / 86400);
  if (d < 30) return `há ${d} ${d === 1 ? 'dia' : 'dias'}`;
  const m = Math.floor(d / 30);
  return m < 12 ? `há ${m} ${m === 1 ? 'mês' : 'meses'}` : `há ${Math.floor(m / 12)} ${Math.floor(m / 12) === 1 ? 'ano' : 'anos'}`;
}

/** "hoje às 14:05", "ontem às 09:30", "12/10 às 18:00". */
export function quando(iso: string, agora = Date.now()): string {
  const d = new Date(iso), hoje = new Date(agora), ontem = new Date(agora - 86400000);
  if (mesmoDia(d, hoje)) return `hoje às ${hora(iso)}`;
  if (mesmoDia(d, ontem)) return `ontem às ${hora(iso)}`;
  return `${doisDigitos(d.getDate())}/${doisDigitos(d.getMonth() + 1)} às ${hora(iso)}`;
}

/** O separador de dia no meio da conversa: "Hoje", "Ontem", "Segunda, 12/10". */
export function rotuloDoDia(iso: string, agora = Date.now()): string {
  const d = new Date(iso), hoje = new Date(agora), ontem = new Date(agora - 86400000);
  if (mesmoDia(d, hoje)) return 'Hoje';
  if (mesmoDia(d, ontem)) return 'Ontem';
  const dia = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'][d.getDay()];
  return `${dia}, ${doisDigitos(d.getDate())}/${doisDigitos(d.getMonth() + 1)}`;
}

/** A linha de status de um jogador: "Online há 12 min", "Saiu há 3 h", "Ainda não apareceu". */
export function statusDe(j: Pick<Jogador, 'online' | 'onlineDesde' | 'vistoEm'>, agora = Date.now()): { curto: string; longo: string } {
  if (j.online && j.onlineDesde) {
    const ha = haQuanto(j.onlineDesde, agora);
    return { curto: ha === 'agora' ? 'Online agora' : `Online ${ha}`, longo: `Online desde ${quando(j.onlineDesde, agora)}` };
  }
  if (j.vistoEm) return { curto: `Saiu ${haQuanto(j.vistoEm, agora)}`, longo: `Visto por último ${quando(j.vistoEm, agora)}` };
  return { curto: 'Ainda não apareceu', longo: 'Ainda não abriu o jogo desde que a Comunidade chegou' };
}

/** A cor de cada nome no chat: sempre a mesma para a mesma conta. */
export function corDoNome(id: string): string {
  let h = 0;
  for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) >>> 0;
  return `hsl(${h % 360} 85% 70%)`;
}
