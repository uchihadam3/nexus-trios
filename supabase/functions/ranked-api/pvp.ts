/*
 * PvP online no servidor (ação "pvp" da ranked-api): o juiz da partida.
 *
 * O navegador só lê a partida em que está (sem segredos, RLS) e pede tudo aqui: desafiar, aceitar, mandar os 3
 * times, escolher o time da rodada, "começar duelo", desistir. É aqui que os times ficam guardados até os dois
 * ficarem prontos, que a escolha de cada um fica escondida até os dois escolherem, que a luta de cada rodada é
 * calculada (o mesmo motor do jogo, com a semente da rodada: os dois aparelhos desenham exatamente esta luta) e que o
 * rating muda (pvp_aplicar_resultado, no banco). Quem some não trava a partida: cada etapa tem prazo, e quem passa
 * dele tem o time sorteado (ou a partida cancelada, antes de começar).
 */
import type { SupabaseClient } from 'npm:@supabase/supabase-js@2.117.2';
import { createBattle, stepBattle } from '../../../src/engine/battle.ts';
import { MINIMO_DA_COLECAO, duracaoNaTela, problemaDosTimes, sementeDaRodada, timesLivres, vencedorDaPartida, type Lado, type RodadaPvp } from '../../../src/engine/pvp.ts';
import { ENGINE_VERSION } from '../../../src/engine/ranked.ts';
import { comEmprestados, diaDoEmprestimo } from '../../../src/engine/emprestimo.ts';
import { characters } from '../../../src/data/characters.ts';

type Db = SupabaseClient;
type Resposta = { status: number; body: unknown };
const ok = (body: unknown): Resposta => ({ status: 200, body });
const erro = (mensagem: string, status = 422): Resposta => ({ status, body: { error: mensagem } });

/** Quanto cada etapa espera (segundos). */
/*
 * `lutar`: a luta da rodada só começa com os dois vendo a tela do VS (pedido do jogador: "a luta não pode começar até
 * os dois estarem vendo a tela"); o aparelho avisa sozinho quando a tela está aberta. Este prazo é só a rede de
 * segurança para um aparelho antigo que não avisa (quem some de verdade perde pela ausência, AUSENCIA_MAXIMA).
 */
export const PRAZO = { convite: 120, montar: 300, escolher: 75, lutar: 90 } as const;
/** A contagem nos dois aparelhos entre os dois ficarem prontos e a luta começar (ms). */
const CONTAGEM_DA_LUTA = 5000;
/** Quem some da partida (app fechado, sem internet) por mais que isso perde (pedido do jogador: 45 s para voltar). */
export const AUSENCIA_MAXIMA = 45;
/** A partir de quanto tempo sem notícia o rival aparece como desconectado (o aparelho pergunta a cada 3 s). */
const SINAL_DE_QUEDA = 9;
const ABERTAS = ['convite', 'montando', 'jogando'];
const ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const PREFIXO = 'personagem:';
const daqui = (s: number) => new Date(Date.now() + s * 1000).toISOString();

interface Partida {
  id: string; desafiante: string; desafiado: string; estado: string; seed: number; versao_do_motor: string;
  pronto_a: boolean; pronto_b: boolean; rodada: number; escolheu_a: boolean; escolheu_b: boolean; resolvida: number;
  lutar_a: boolean; lutar_b: boolean; assistiu_a: boolean; assistiu_b: boolean; inicio_em: string | null; prazo: string; vencedor: string | null; motivo: string | null;
  rating_a: number | null; rating_b: number | null; delta_a: number | null; delta_b: number | null; criada_em: string;
}
interface Rodada { n: number; time_a: number; time_b: number; seed: number; vencedor: 'a' | 'b'; duracao: number; rendida?: boolean }

/**
 * A coleção de quem joga, no servidor: os personagens liberados nas Conquistas e os 9 emprestados do dia
 * (src/engine/emprestimo.ts, os mesmos para todo mundo). `desde`: o dia em que a partida nasceu também vale (quem
 * montou os times antes da meia-noite não perde os emprestados dela).
 */
async function colecaoDe(db: Db, quem: string, desde?: string): Promise<string[]> {
  const { data, error } = await db.from('player_achievements').select('achievement_id').eq('player_id', quem).like('achievement_id', `${PREFIXO}%`);
  if (error) throw error;
  const ids = new Set(characters.map((c) => c.id));
  const minha = (data ?? []).map((x) => String(x.achievement_id).slice(PREFIXO.length)).filter((id) => ids.has(id));
  const hoje = comEmprestados(minha);
  return desde && desde !== diaDoEmprestimo() ? comEmprestados(hoje, desde) : hoje;
}
async function partidaDe(db: Db, id: string): Promise<Partida | null> {
  const { data, error } = await db.from('pvp_partidas').select('*').eq('id', id).maybeSingle();
  if (error) throw error;
  return data as Partida | null;
}
async function rodadasDe(db: Db, id: string): Promise<Rodada[]> {
  const { data, error } = await db.from('pvp_rodadas').select('n,time_a,time_b,seed,vencedor,duracao,rendida').eq('partida_id', id).order('n');
  if (error) throw error;
  return (data ?? []) as Rodada[];
}
async function timesDe(db: Db, id: string): Promise<Record<string, string[][]>> {
  const { data, error } = await db.from('pvp_times').select('jogador,times').eq('partida_id', id);
  if (error) throw error;
  return Object.fromEntries((data ?? []).map((x) => [x.jogador as string, x.times as string[][]]));
}
/** As rodadas do ponto de vista de A ('eu') — para as regras de src/engine/pvp.ts. */
const comoA = (rs: Rodada[]): RodadaPvp[] => rs.map((r) => ({ meu: r.time_a, dele: r.time_b, seed: Number(r.seed), vencedor: r.vencedor === 'a' ? 'eu' : 'rival' }));
const ladoDe = (p: Partida, quem: string): 'a' | 'b' => (p.desafiante === quem ? 'a' : 'b');
const atualiza = async (db: Db, id: string, campos: Record<string, unknown>, filtro?: (q: ReturnType<ReturnType<Db['from']>['update']>) => unknown) => {
  let q = db.from('pvp_partidas').update({ ...campos, atualizada_em: new Date().toISOString() }).eq('id', id);
  if (filtro) q = filtro(q) as typeof q;
  const { data, error } = await q.select('*');
  if (error) throw error;
  return (data ?? []) as Partida[];
};

/** Calcula a luta da rodada n (quando os dois já escolheram) e, se alguém venceu com os 3 times, o fim da partida. */
async function resolver(db: Db, p: Partida, n: number) {
  const [{ data: escolhas, error }, times] = await Promise.all([db.from('pvp_escolhas').select('jogador,time').eq('partida_id', p.id).eq('n', n), timesDe(db, p.id)]);
  if (error) throw error;
  const ta = escolhas?.find((e) => e.jogador === p.desafiante)?.time, tb = escolhas?.find((e) => e.jogador === p.desafiado)?.time;
  if (ta === undefined || tb === undefined) return;
  // só um calcula: quem conseguir marcar a rodada como resolvida. No mesmo passo some o começo da luta anterior: se
  // um aparelho perguntar no meio do cálculo, ele não pode ver a rodada nova com o horário da luta velha (pegava a
  // luta 2 "começada" lá atrás, já no fim, e a partida travava).
  const marcou = await atualiza(db, p.id, { resolvida: n, inicio_em: null, lutar_a: false, lutar_b: false, assistiu_a: false, assistiu_b: false },
    (q) => q.lt('resolvida', n).eq('estado', 'jogando'));
  if (!marcou.length) return;
  const seed = sementeDaRodada(Number(p.seed), n);
  const luta = createBattle(times[p.desafiante]![ta]!, times[p.desafiado]![tb]!, seed);
  for (let i = 0; i < 60000 && !luta.finished; i++) stepBattle(luta);
  const vencedor: 'a' | 'b' = luta.winner === 'player' ? 'a' : 'b';
  const { error: e2 } = await db.from('pvp_rodadas').insert({ partida_id: p.id, n, time_a: ta, time_b: tb, seed, vencedor, duracao: luta.time });
  if (e2) throw e2;
  const rodadas = await rodadasDe(db, p.id);
  const fim = vencedorDaPartida({ rodadas: comoA(rodadas) });
  if (fim) {
    const { error: e3 } = await db.rpc('pvp_aplicar_resultado', { p_partida: p.id, p_vencedor: fim === 'eu' ? p.desafiante : p.desafiado, p_motivo: 'venceu com os 3 times' });
    if (e3) throw e3;
  }
  await atualiza(db, p.id, { rodada: n + 1, escolheu_a: false, escolheu_b: false, lutar_a: false, lutar_b: false, assistiu_a: false, assistiu_b: false, inicio_em: null, prazo: daqui(PRAZO.lutar) });
}

/** Faz a luta da rodada resolvida começar nos dois aparelhos ao mesmo tempo, depois da contagem. */
async function comecarLuta(db: Db, p: Partida) {
  const n = p.resolvida, rodadas = await rodadasDe(db, p.id), r = rodadas.find((x) => x.n === n);
  if (!r) return;
  // a próxima escolha espera a luta acabar na tela e mais um tempo para escolher. A encenação (nomes, efeitos, pausas)
  // leva bem mais que o relógio do motor: este prazo é só a rede de segurança para quem sumiu; quando os dois avisam
  // que terminaram de assistir (op "assisti"), o tempo de escolher começa a contar dali.
  const inicio = Date.now() + CONTAGEM_DA_LUTA, fimDaLuta = inicio + duracaoNaTela(r.duracao) * 1000;
  await atualiza(db, p.id, { inicio_em: new Date(inicio).toISOString(), prazo: new Date(fimDaLuta + PRAZO.escolher * 1000).toISOString() }, (q) => q.is('inicio_em', null).eq('resolvida', n));
}

/** Os prazos: convite e montagem expiram; quem não escolhe tem o time sorteado; o duelo começa sozinho. */
async function avancar(db: Db, p: Partida): Promise<Partida> {
  const venceu = Date.parse(p.prazo) < Date.now();
  if (!venceu) return p;
  if (p.estado === 'convite') { await atualiza(db, p.id, { estado: 'expirada', motivo: 'O convite expirou' }, (q) => q.eq('estado', 'convite')); }
  else if (p.estado === 'montando') { await atualiza(db, p.id, { estado: 'cancelada', motivo: 'O tempo para montar os times acabou' }, (q) => q.eq('estado', 'montando')); }
  else if (['jogando', 'terminada'].includes(p.estado) && p.resolvida >= 0 && p.resolvida === p.rodada - 1 && !p.inicio_em) { await comecarLuta(db, p); }
  else if (p.estado === 'jogando' && (p.rodada === 0 || p.inicio_em)) {
    // a escolha da rodada: quem não escolheu a tempo joga com um time sorteado entre os que ainda pode usar
    const rodadas = comoA(await rodadasDe(db, p.id));
    for (const [lado, quem, ja] of [['eu', p.desafiante, p.escolheu_a], ['rival', p.desafiado, p.escolheu_b]] as [Lado, string, boolean][]) {
      if (ja) continue;
      const livres = timesLivres({ rodadas }, lado), time = livres[Math.floor(Math.random() * livres.length)]!;
      await db.from('pvp_escolhas').upsert({ partida_id: p.id, n: p.rodada, jogador: quem, time, automatica: true }, { onConflict: 'partida_id,n,jogador', ignoreDuplicates: true });
    }
    await atualiza(db, p.id, { escolheu_a: true, escolheu_b: true });
    await resolver(db, (await partidaDe(db, p.id))!, p.rodada);
  }
  return (await partidaDe(db, p.id))!;
}

const tempoDe = (x: unknown) => new Date(x as string).getTime();
/**
 * Marca que quem pergunta está na partida. No meio do jogo, se o outro sumiu há mais de AUSENCIA_MAXIMA, quem ficou
 * vence (a luta na tela segue até lá; a vitória vale como as 3 rodadas). Devolve a partida e há quanto tempo o rival
 * não dá notícia (para a tela mostrar "desconectou, X s para voltar").
 */
async function presenca(db: Db, p: Partida, quem: string): Promise<{ p: Partida; ausencia: number | null }> {
  if (!['montando', 'jogando'].includes(p.estado)) return { p, ausencia: null };
  const { error } = await db.from('pvp_presenca').upsert({ partida_id: p.id, jogador: quem, visto_em: new Date().toISOString() }, { onConflict: 'partida_id,jogador' });
  if (error) throw error;
  const outro = p.desafiante === quem ? p.desafiado : p.desafiante;
  const { data } = await db.from('pvp_presenca').select('visto_em').eq('partida_id', p.id).eq('jogador', outro).maybeSingle();
  if (!data) return { p, ausencia: null };
  const ha = Math.max(0, (Date.now() - tempoDe(data.visto_em)) / 1000);
  if (p.estado === 'jogando' && ha > AUSENCIA_MAXIMA) {
    const { error: e } = await db.rpc('pvp_aplicar_resultado', { p_partida: p.id, p_vencedor: quem, p_motivo: 'desconectou' });
    if (e) throw e;
    return { p: (await partidaDe(db, p.id))!, ausencia: null };
  }
  return { p, ausencia: ha >= SINAL_DE_QUEDA ? Math.floor(ha) : null };
}

/** O que cada um pode ver da partida (do ponto de vista de quem pergunta). */
async function vista(db: Db, p: Partida, quem: string, ausencia: number | null = null) {
  const eu = ladoDe(p, quem), outro = eu === 'a' ? p.desafiado : p.desafiante;
  const [{ data: nomes }, { data: ratings }, rodadas, times, { data: minha }] = await Promise.all([
    db.from('players').select('id,handle').in('id', [p.desafiante, p.desafiado]),
    db.from('pvp_ratings').select('player_id,rating,vitorias,derrotas').in('player_id', [p.desafiante, p.desafiado]),
    rodadasDe(db, p.id), timesDe(db, p.id),
    db.from('pvp_escolhas').select('time').eq('partida_id', p.id).eq('n', p.rodada).eq('jogador', quem).maybeSingle(),
  ]);
  const nome = (id: string) => nomes?.find((x) => x.id === id)?.handle ?? 'Jogador';
  const rating = (id: string) => ratings?.find((x) => x.player_id === id) ?? { rating: 1000, vitorias: 0, derrotas: 0 };
  const prontos = p.pronto_a && p.pronto_b;
  const meu = (r: Rodada) => (eu === 'a' ? r.time_a : r.time_b), dele = (r: Rodada) => (eu === 'a' ? r.time_b : r.time_a);
  // a linha da partida é lida antes das rodadas: se a rodada nova entrou no meio, a resolvida acompanha (a rodada só existe
  // depois de marcada como resolvida) e o começo velho não vale para ela; senão o aparelho via o resultado como se a luta
  // já tivesse passado na tela (pedido do dono: "o jogador não pode saber se ganhou ou perdeu antes da luta")
  const resolvida = Math.max(p.resolvida, ...rodadas.map((r) => r.n));
  return {
    id: p.id, fase: p.estado, eu, seed: Number(p.seed), versao: p.versao_do_motor, agora: new Date().toISOString(), prazo: p.prazo, criada: p.criada_em,
    voce: { id: quem, nome: nome(quem), ...rating(quem) }, rival: { id: outro, nome: nome(outro), ...rating(outro) },
    desafiante: eu === 'a',
    pronto: { eu: eu === 'a' ? p.pronto_a : p.pronto_b, rival: eu === 'a' ? p.pronto_b : p.pronto_a },
    escolheu: { eu: eu === 'a' ? p.escolheu_a : p.escolheu_b, rival: eu === 'a' ? p.escolheu_b : p.escolheu_a },
    lutar: { eu: eu === 'a' ? p.lutar_a : p.lutar_b, rival: eu === 'a' ? p.lutar_b : p.lutar_a },
    assistiu: { eu: eu === 'a' ? p.assistiu_a : p.assistiu_b, rival: eu === 'a' ? p.assistiu_b : p.assistiu_a },
    // o começo da luta só vale para a rodada que acabou de ser resolvida (a próxima a passar na tela)
    rodada: p.rodada, resolvida,
    inicioEm: resolvida === p.resolvida && p.resolvida >= 0 && p.resolvida === p.rodada - 1 ? p.inicio_em : null,
    meusTimes: times[quem] ?? null, timesDele: prontos ? times[outro] ?? null : null,
    minhaEscolha: minha?.time ?? null,
    rodadas: rodadas.map((r) => ({ n: r.n, meu: meu(r), dele: dele(r), seed: Number(r.seed), vencedor: r.vencedor === eu ? 'eu' : 'rival', duracao: r.duracao, rendida: r.rendida === true })),
    vencedor: p.vencedor ? (p.vencedor === quem ? 'eu' : 'rival') : null, motivo: p.motivo,
    delta: p.delta_a === null ? null : eu === 'a' ? p.delta_a : p.delta_b,
    // há quantos segundos o rival não dá notícia (null: está aqui) e quanto ele tem para voltar
    ausencia, ausenciaMaxima: AUSENCIA_MAXIMA,
  };
}

export async function acaoPvp(db: Db, quem: string, input: Record<string, unknown>): Promise<Resposta> {
  const op = String(input.op ?? '');
  const id = typeof input.partida === 'string' && ID.test(input.partida) ? input.partida : null;
  const minha = async () => {
    if (!id) return null;
    const p = await partidaDe(db, id);
    return p && (p.desafiante === quem || p.desafiado === quem) ? p : null;
  };

  if (op === 'ranking') {
    const { data, error } = await db.rpc('pvp_ranking', { p_limite: 50 });
    if (error) throw error;
    const { data: eu } = await db.from('pvp_ratings').select('rating,vitorias,derrotas').eq('player_id', quem).maybeSingle();
    // a sua linha (o id e a posição, se estiver entre os 50) para a tela marcar você
    const posicao = ((data ?? []) as { id: string; posicao: number }[]).find((r) => r.id === quem)?.posicao ?? null;
    return ok({ ranking: data ?? [], eu: { ...(eu ?? { rating: 1000, vitorias: 0, derrotas: 0 }), id: quem, posicao: posicao === null ? null : Number(posicao) }, colecao: (await colecaoDe(db, quem)).length });
  }

  if (op === 'estado') {
    let p = await minha();
    if (!p) {
      const { data, error } = await db.from('pvp_partidas').select('*').or(`desafiante.eq.${quem},desafiado.eq.${quem}`).in('estado', ABERTAS).order('criada_em', { ascending: false }).limit(1);
      if (error) throw error;
      p = (data?.[0] as Partida | undefined) ?? null;
    }
    if (!p) return ok({ partida: null, colecao: await colecaoDe(db, quem) });
    const aqui = await presenca(db, await avancar(db, p), quem);
    return ok({ partida: await vista(db, aqui.p, quem, aqui.ausencia), colecao: await colecaoDe(db, quem) });
  }

  if (op === 'desafiar') {
    const alvo = typeof input.alvo === 'string' && ID.test(input.alvo) ? input.alvo : null;
    if (!alvo || alvo === quem) return erro('Escolha quem desafiar.');
    const { data: existe } = await db.from('players').select('id,handle').eq('id', alvo).maybeSingle();
    if (!existe) return erro('Jogador não encontrado.', 404);
    const [minhaColecao, dele] = await Promise.all([colecaoDe(db, quem), colecaoDe(db, alvo)]);
    if (minhaColecao.length < MINIMO_DA_COLECAO) return erro(`Você precisa de ${MINIMO_DA_COLECAO} personagens na coleção para o PvP (tem ${minhaColecao.length}).`);
    if (dele.length < MINIMO_DA_COLECAO) return erro(`${existe.handle} ainda não tem ${MINIMO_DA_COLECAO} personagens na coleção.`);
    // partidas abertas que já passaram do prazo deixam de travar
    const { data: abertas } = await db.from('pvp_partidas').select('*').or(`desafiante.in.(${quem},${alvo}),desafiado.in.(${quem},${alvo})`).in('estado', ABERTAS);
    for (const a of (abertas ?? []) as Partida[]) await avancar(db, a);
    const seed = crypto.getRandomValues(new Uint32Array(1))[0]! & 0x7fffffff;
    const { data, error } = await db.from('pvp_partidas').insert({ desafiante: quem, desafiado: alvo, estado: 'convite', seed, versao_do_motor: ENGINE_VERSION, prazo: daqui(PRAZO.convite) }).select('*').single();
    if (error) {
      if (error.code === '23505') return erro(`Você ou ${existe.handle} já está numa partida de PvP.`, 409);
      throw error;
    }
    return ok({ partida: await vista(db, data as Partida, quem), colecao: minhaColecao });
  }

  const p0 = await minha();
  if (!p0) return erro('Partida não encontrada.', 404);
  const aqui = await presenca(db, await avancar(db, p0), quem), p = aqui.p, eu = ladoDe(p, quem);
  const devolve = async () => ok({ partida: await vista(db, (await partidaDe(db, p.id))!, quem, aqui.ausencia), colecao: await colecaoDe(db, quem) });

  if (op === 'responder') {
    if (eu !== 'b' || p.estado !== 'convite') return erro('Este convite não está mais aberto.', 409);
    if (input.aceitar === true) await atualiza(db, p.id, { estado: 'montando', prazo: daqui(PRAZO.montar) }, (q) => q.eq('estado', 'convite'));
    else await atualiza(db, p.id, { estado: 'recusada', motivo: 'Recusou o desafio' }, (q) => q.eq('estado', 'convite'));
    return devolve();
  }

  if (op === 'times') {
    if (p.estado !== 'montando') return erro('A montagem dos times já acabou.', 409);
    if ((eu === 'a' ? p.pronto_a : p.pronto_b)) return devolve();
    const times = input.times;
    if (!Array.isArray(times) || times.length !== 3 || times.some((t) => !Array.isArray(t) || t.length !== 3 || t.some((x) => typeof x !== 'string'))) return erro('Monte 3 times de 3.');
    const problema = problemaDosTimes(times as string[][], new Set(await colecaoDe(db, quem, diaDoEmprestimo(Date.parse(p.criada_em)))));
    if (problema) return erro(problema);
    const { error } = await db.from('pvp_times').upsert({ partida_id: p.id, jogador: quem, times }, { onConflict: 'partida_id,jogador' });
    if (error) throw error;
    await atualiza(db, p.id, eu === 'a' ? { pronto_a: true } : { pronto_b: true });
    // os dois prontos: começa (só um consegue)
    await atualiza(db, p.id, { estado: 'jogando', rodada: 0, prazo: daqui(PRAZO.escolher) }, (q) => q.eq('estado', 'montando').eq('pronto_a', true).eq('pronto_b', true));
    return devolve();
  }

  if (op === 'escolher') {
    const n = Number(input.n), time = Number(input.time);
    if (p.estado !== 'jogando' || n !== p.rodada) return erro('Esta rodada já foi.', 409);
    if (p.rodada > 0 && !p.inicio_em) return erro('Espere a luta começar.', 409);
    if ((eu === 'a' ? p.escolheu_a : p.escolheu_b)) return devolve();
    const livres = timesLivres({ rodadas: comoA(await rodadasDe(db, p.id)) }, eu === 'a' ? 'eu' : 'rival');
    if (!livres.includes(time)) return erro('Este time já venceu: escolha outro.');
    const { error } = await db.from('pvp_escolhas').insert({ partida_id: p.id, n, jogador: quem, time });
    if (error && error.code !== '23505') throw error;
    await atualiza(db, p.id, eu === 'a' ? { escolheu_a: true } : { escolheu_b: true });
    const agora = (await partidaDe(db, p.id))!;
    if (agora.escolheu_a && agora.escolheu_b) await resolver(db, agora, n);
    return devolve();
  }

  /*
   * Estou vendo a tela do VS (pronto) ou saí dela (pronto: false, o app foi para segundo plano antes da luta começar).
   * Quando os dois estão vendo, a luta começa nos dois aparelhos depois da contagem.
   */
  if (op === 'lutar') {
    if (!['jogando', 'terminada'].includes(p.estado) || p.resolvida < 0 || p.resolvida !== p.rodada - 1 || p.inicio_em) return devolve();
    const pronto = input.pronto !== false;
    await atualiza(db, p.id, eu === 'a' ? { lutar_a: pronto } : { lutar_b: pronto });
    if (!pronto) return devolve();
    const agora = (await partidaDe(db, p.id))!;
    if (agora.lutar_a && agora.lutar_b) await comecarLuta(db, agora);
    return devolve();
  }

  if (op === 'assisti') {
    const n = Number(input.n);
    if (p.estado !== 'jogando' || n !== p.resolvida || !p.inicio_em || (eu === 'a' ? p.assistiu_a : p.assistiu_b)) return devolve();
    await atualiza(db, p.id, eu === 'a' ? { assistiu_a: true } : { assistiu_b: true });
    const agora = (await partidaDe(db, p.id))!;
    if (agora.assistiu_a && agora.assistiu_b && Date.parse(agora.prazo) > Date.now() + PRAZO.escolher * 1000)
      await atualiza(db, p.id, { prazo: daqui(PRAZO.escolher) }, (q) => q.eq('resolvida', n));
    return devolve();
  }

  /*
   * Desistir da luta que está passando (pedido do jogador: "o desistir dentro da luta é só daquela luta"): a rodada
   * vai para o outro e a partida segue. Se com isso o outro completou os 3 times, a partida acaba para ele.
   * (Se a rodada já era do outro, nada muda; se ela tinha encerrado a partida, já não há o que render.)
   */
  if (op === 'render') {
    const n = Number(input.n);
    if (p.estado !== 'jogando' || n !== p.resolvida || !p.inicio_em) return devolve();
    const rodadas = await rodadasDe(db, p.id), r = rodadas.find((x) => x.n === n);
    if (!r || r.rendida) return devolve();
    const outro: 'a' | 'b' = eu === 'a' ? 'b' : 'a';
    const { error } = await db.from('pvp_rodadas').update({ vencedor: outro, rendida: true }).eq('partida_id', p.id).eq('n', n);
    if (error) throw error;
    const fim = vencedorDaPartida({ rodadas: comoA(await rodadasDe(db, p.id)) });
    if (fim) {
      const { error: e } = await db.rpc('pvp_aplicar_resultado', { p_partida: p.id, p_vencedor: fim === 'eu' ? p.desafiante : p.desafiado, p_motivo: 'venceu com os 3 times' });
      if (e) throw e;
    }
    return devolve();
  }

  if (op === 'cancelar' || op === 'desistir') {
    if (p.estado === 'convite' || p.estado === 'montando') await atualiza(db, p.id, { estado: 'cancelada', motivo: eu === 'a' ? 'O desafiante cancelou' : 'O desafiado saiu' }, (q) => q.in('estado', ['convite', 'montando']));
    else if (p.estado === 'jogando') {
      const { error } = await db.rpc('pvp_aplicar_resultado', { p_partida: p.id, p_vencedor: eu === 'a' ? p.desafiado : p.desafiante, p_motivo: 'desistiu' });
      if (error) throw error;
    }
    return devolve();
  }

  return erro('Ação de PvP desconhecida.', 404);
}
