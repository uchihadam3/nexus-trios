/*
 * O Caminho do Nexus no servidor (ação "campanha" da ranked-api): o juiz da campanha do PvP contra os 40 rivais
 * (src/engine/campanha.ts).
 *
 * O aparelho manda os 3 times e, a cada rodada, o time escolhido. Aqui ficam o progresso (estrelas, placar contra
 * cada rival) e o rodízio (quem descansa, de você e de cada rival); aqui o rival monta os times dele (depois de ver os
 * seus, como o Espelho precisa), escolhe o time da rodada e a luta é calculada com o mesmo motor do jogo. As sementes
 * das lutas e da escolha do rival são sorteadas no começo e só saem daqui depois que a rodada acontece: quem soubesse
 * a semente saberia o resultado antes de escolher. No fim, o progresso muda numa transação (pvp_campanha_terminar).
 * O Nexus não mexe no rating do PvP (pedido do dono: os rankings separados); o dele é o das estrelas (op "ranking").
 */
import type { SupabaseClient } from 'npm:@supabase/supabase-js@2.117.2';
import { DESCANSO, MINIMO_DA_CAMPANHA, contaParaODescanso, depoisDaPartida, seuDescanso, escalaDoRival, escolhaDoRival, estrelasDaPartida, liberado, livresParaJogar, lutaDaRodada, quemLutou,
  rivalPorId, timesDoRival, tituloDas, type Descanso, type Estrelas, type Rival } from '../../../src/engine/campanha.ts';
import { RATING_INICIAL, problemaDosTimes, timesLivres, vencedorDaPartida, type PartidaPvp, type RodadaPvp, type Times } from '../../../src/engine/pvp.ts';
import { ENGINE_VERSION } from '../../../src/engine/ranked.ts';
import { characters } from '../../../src/data/characters.ts';

type Db = SupabaseClient;
type Resposta = { status: number; body: unknown };
const ok = (body: unknown): Resposta => ({ status: 200, body });
const erro = (mensagem: string, status = 422): Resposta => ({ status, body: { error: mensagem } });
const ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const PREFIXO = 'personagem:';

interface Progresso { estrelas: Estrelas; placar: Record<string, { v: number; d: number }>; descanso: Descanso; descanso_rivais: Record<string, Descanso>; partidas: number }
interface Partida {
  id: string; player_id: string; rival: string; rival_rating: number; estado: 'jogando' | 'terminada'; versao_do_motor: string;
  sementes: number[]; sorteios: number[]; meus: Times; deles: Times; rodadas: RodadaPvp[]; n_rodadas: number;
  vencedor: 'eu' | 'rival' | null; motivo: string | null; estrelas: number | null; rating_antes: number | null; delta: number | null; criada_em: string;
}

const sorteia = () => crypto.getRandomValues(new Uint32Array(1))[0]!;
const lista = (x: unknown) => (Array.isArray(x) ? x : typeof x === 'string' ? JSON.parse(x) : []) as RodadaPvp[];

async function colecaoDe(db: Db, quem: string): Promise<string[]> {
  const { data, error } = await db.from('player_achievements').select('achievement_id').eq('player_id', quem).like('achievement_id', `${PREFIXO}%`);
  if (error) throw error;
  const ids = new Set(characters.map((c) => c.id));
  return (data ?? []).map((x) => String(x.achievement_id).slice(PREFIXO.length)).filter((id) => ids.has(id));
}
async function progressoDe(db: Db, quem: string): Promise<Progresso> {
  const { data, error } = await db.from('pvp_campanha').select('estrelas,placar,descanso,descanso_rivais,partidas').eq('player_id', quem).maybeSingle();
  if (error) throw error;
  const j = (x: unknown) => (x && typeof x === 'object' ? x : typeof x === 'string' ? JSON.parse(x) : {});
  return { estrelas: j(data?.estrelas), placar: j(data?.placar), descanso: j(data?.descanso), descanso_rivais: j(data?.descanso_rivais), partidas: Number(data?.partidas ?? 0) };
}
async function ratingDe(db: Db, quem: string) {
  const { data, error } = await db.from('pvp_ratings').select('rating,vitorias,derrotas').eq('player_id', quem).maybeSingle();
  if (error) throw error;
  return data ?? { rating: RATING_INICIAL, vitorias: 0, derrotas: 0 };
}
const json = <T,>(x: unknown) => (typeof x === 'string' ? JSON.parse(x) : x) as T;
const ler = (x: Record<string, unknown>): Partida => ({ ...(x as unknown as Partida), meus: json<Times>(x.meus), deles: json<Times>(x.deles), rodadas: lista(x.rodadas),
  sementes: json<number[]>(x.sementes ?? []), sorteios: json<number[]>(x.sorteios ?? []) });
async function aberta(db: Db, quem: string): Promise<Partida | null> {
  const { data, error } = await db.from('pvp_campanha_partidas').select('*').eq('player_id', quem).eq('estado', 'jogando').maybeSingle();
  if (error) throw error;
  return data ? ler(data) : null;
}
async function partidaDe(db: Db, quem: string, id: string): Promise<Partida | null> {
  const { data, error } = await db.from('pvp_campanha_partidas').select('*').eq('id', id).eq('player_id', quem).maybeSingle();
  if (error) throw error;
  return data ? ler(data) : null;
}
/** As últimas partidas terminadas (de todas, ou só contra um rival), da mais antiga para a mais nova. */
async function ultimas(db: Db, quem: string, rival?: string): Promise<Partida[]> {
  let q = db.from('pvp_campanha_partidas').select('meus,deles,rodadas,rival,criada_em').eq('player_id', quem).eq('estado', 'terminada');
  if (rival) q = q.eq('rival', rival);
  const { data, error } = await q.order('criada_em', { ascending: false }).limit(DESCANSO.janela - 1);
  if (error) throw error;
  return (data ?? []).map((x) => ler(x)).reverse();
}

/** O que o aparelho vê da partida: sem as sementes das rodadas que ainda não aconteceram. */
function vista(p: Partida, rating?: number) {
  return {
    id: p.id, rival: p.rival, estado: p.estado, versao: p.versao_do_motor, meus: p.meus, deles: p.deles,
    rodadas: p.rodadas.map((r) => ({ meu: r.meu, dele: r.dele, seed: Number(r.seed), vencedor: r.vencedor, ...(r.rendida ? { rendida: true } : {}) })),
    vencedor: p.vencedor, motivo: p.motivo, estrelas: p.estrelas, ratingAntes: p.rating_antes, delta: p.delta,
    ...(rating !== undefined ? { rating } : {}),
  };
}
async function resposta(db: Db, quem: string, partida: Partida | null) {
  const [progresso, rating, colecao] = await Promise.all([progressoDe(db, quem), ratingDe(db, quem), colecaoDe(db, quem)]);
  return ok({ progresso, rating, colecao, partida: partida ? vista(partida, rating.rating) : null });
}

/** O fim da partida: estrelas e o rodízio dos dois lados, numa transação (o Nexus não mexe mais no rating do PvP). */
async function terminar(db: Db, p: Partida, rival: Rival, vencedor: 'eu' | 'rival', motivo: string) {
  const [progresso, minhas, contraEle, colecao] = await Promise.all([progressoDe(db, p.player_id), ultimas(db, p.player_id), ultimas(db, p.player_id, rival.id), colecaoDe(db, p.player_id)]);
  const usoMeu = (x: Partida) => quemLutou(x.meus, x.rodadas.map((r) => ({ time: r.meu })));
  const usoDele = (x: Partida) => quemLutou(x.deles, x.rodadas.map((r) => ({ time: r.dele })));
  // o seu rodízio pesa mais a cada duas regiões; contra rival que você já tinha gabaritado (3★), nada muda
  const descanso = contaParaODescanso(progresso.estrelas, rival)
    ? depoisDaPartida(progresso.descanso, [...minhas, p].map(usoMeu), seuDescanso(rival.regiao, colecao.length)) : progresso.descanso;
  const descansoDele = depoisDaPartida(progresso.descanso_rivais[rival.id] ?? {}, [...contraEle, p].map(usoDele));
  const estrelas = vencedor === 'eu' ? estrelasDaPartida(p) : 0;
  const { error } = await db.rpc('pvp_campanha_terminar', { p_partida: p.id, p_vencedor: vencedor, p_motivo: motivo, p_estrelas: estrelas, p_delta: 0, p_descanso: descanso, p_descanso_rival: descansoDele });
  if (error) throw error;
}

export async function acaoCampanha(db: Db, quem: string, input: Record<string, unknown>): Promise<Resposta> {
  const op = String(input.op ?? '');
  const id = typeof input.partida === 'string' && ID.test(input.partida) ? input.partida : null;

  if (op === 'estado') return resposta(db, quem, await aberta(db, quem));

  // o ranking do Nexus (separado do PvP): mais estrelas; empate, menos partidas
  if (op === 'ranking') {
    const { data, error } = await db.rpc('pvp_campanha_ranking', { p_player: quem, p_limite: 50 });
    if (error) throw error;
    type Linha = { posicao: number; total: number; id: string; nome: string; estrelas: number; partidas: number };
    const linhas = ((data ?? []) as Linha[]).map((l) => ({ posicao: Number(l.posicao), id: l.id, nome: l.nome, estrelas: l.estrelas, partidas: l.partidas, titulo: tituloDas(l.estrelas).nome }));
    return ok({ ranking: linhas.filter((l) => l.posicao <= 50), eu: linhas.find((l) => l.id === quem) ?? null, total: Number(((data ?? []) as Linha[])[0]?.total ?? 0) });
  }

  if (op === 'comecar') {
    const rival = typeof input.rival === 'string' ? rivalPorId(input.rival) : null;
    if (!rival) return erro('Rival não encontrado.', 404);
    if (input.versao !== ENGINE_VERSION) return erro('O jogo foi atualizado. Feche e abra o jogo para jogar a campanha.', 409);
    if (await aberta(db, quem)) return erro('Você já tem uma partida da campanha aberta: termine ou abandone ela primeiro.', 409);
    const [progresso, colecao] = await Promise.all([progressoDe(db, quem), colecaoDe(db, quem)]);
    if (!liberado(progresso.estrelas, rival)) return erro(`${rival.nome} ainda está bloqueado: vença o rival anterior.`, 403);
    if (colecao.length < MINIMO_DA_CAMPANHA) return erro(`A campanha pede ${MINIMO_DA_CAMPANHA} personagens na coleção (você tem ${colecao.length}).`);
    const times = input.times;
    if (!Array.isArray(times) || times.length !== 3 || times.some((t) => !Array.isArray(t) || t.length !== 3 || t.some((x) => typeof x !== 'string'))) return erro('Monte 3 times de 3.');
    const problema = problemaDosTimes(times as string[][], new Set(livresParaJogar(colecao, progresso.descanso)));
    if (problema) return erro(Object.keys(progresso.descanso).some((x) => (times as string[][]).flat().includes(x)) ? 'Tem personagem descansando no seu time.' : problema);
    const meus = times as Times;
    const descansaDele = Object.keys(progresso.descanso_rivais[rival.id] ?? {});
    const deles = timesDoRival(rival, sorteia(), descansaDele, meus.flat());
    const sementes = Array.from({ length: 5 }, () => sorteia() & 0x7fffffff), sorteios = Array.from({ length: 5 }, () => sorteia() & 0x7fffffff);
    const { data, error } = await db.from('pvp_campanha_partidas').insert({
      player_id: quem, rival: rival.id, rival_rating: rival.rating, versao_do_motor: ENGINE_VERSION, sementes, sorteios, meus, deles,
    }).select('*').single();
    if (error) {
      if (error.code === '23505') return erro('Você já tem uma partida da campanha aberta.', 409);
      throw error;
    }
    return resposta(db, quem, ler(data));
  }

  const p = id ? await partidaDe(db, quem, id) : null;
  if (!p) return erro('Partida não encontrada.', 404);
  const rival = rivalPorId(p.rival)!;
  const devolve = async () => resposta(db, quem, await partidaDe(db, quem, p.id));

  if (op === 'escolher') {
    const n = Number(input.n), time = Number(input.time);
    if (p.estado !== 'jogando' || n !== p.rodadas.length) return devolve();
    if (!timesLivres(p, 'eu').includes(time)) return erro('Este time já venceu: escolha outro.');
    const partida: PartidaPvp = { meus: p.meus, deles: p.deles, rodadas: p.rodadas, seed: 0 };
    const seed = Number(p.sementes[n]), dele = escolhaDoRival(rival, partida, Number(p.sorteios[n]), seed);
    const luta = lutaDaRodada(p.meus[time]!, p.deles[dele]!, seed, escalaDoRival(rival));
    const rodadas: RodadaPvp[] = [...p.rodadas, { meu: time, dele, seed, vencedor: luta.winner === 'player' ? 'eu' : 'rival' }];
    // só um calcula: quem conseguir gravar a rodada n
    const { data, error } = await db.from('pvp_campanha_partidas').update({ rodadas, n_rodadas: n + 1, atualizada_em: new Date().toISOString() })
      .eq('id', p.id).eq('estado', 'jogando').eq('n_rodadas', n).select('id');
    if (error) throw error;
    if (data?.length) {
      const fim = vencedorDaPartida({ rodadas });
      if (fim) await terminar(db, { ...p, rodadas }, rival, fim, 'venceu com os 3 times');
    }
    return devolve();
  }

  /* Desistir da luta que está passando: a rodada vai para o rival e a partida segue (se não acabou com ela). */
  if (op === 'render') {
    const n = Number(input.n), r = p.rodadas[n];
    if (p.estado !== 'jogando' || n !== p.rodadas.length - 1 || !r || r.rendida || r.vencedor === 'rival') return devolve();
    const rodadas = p.rodadas.map((x, i) => (i === n ? { ...x, vencedor: 'rival' as const, rendida: true } : x));
    const { data, error } = await db.from('pvp_campanha_partidas').update({ rodadas, atualizada_em: new Date().toISOString() })
      .eq('id', p.id).eq('estado', 'jogando').eq('n_rodadas', n + 1).select('id');
    if (error) throw error;
    if (data?.length && vencedorDaPartida({ rodadas })) await terminar(db, { ...p, rodadas }, rival, 'rival', 'venceu com os 3 times');
    return devolve();
  }

  if (op === 'abandonar') {
    if (p.estado === 'jogando') await terminar(db, p, rival, 'rival', 'abandonou');
    return devolve();
  }

  return erro('Ação da campanha desconhecida.', 404);
}
