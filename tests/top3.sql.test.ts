/*
 * FASE K · a regra "até 3 trios diferentes por conta", num Postgres de verdade.
 *
 * Roda as migrações reais do projeto num banco descartável e confere a regra
 * com os exemplos do próprio documento — mesmo trio, quarto trio, empate — e
 * com o caso que nenhum teste de unidade alcança: partidas chegando ao mesmo
 * tempo, por conexões diferentes, disputando a última vaga.
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 * Sem a variável, os testes são pulados (e dizem isso), em vez de passarem.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_top3_${Date.now()}`;
const migracoes = readdirSync('supabase/migrations').filter((f) => f.endsWith('.sql')).sort();
const sql = (f: string) => readFileSync(f, 'utf8');
const urlDo = (banco: string) => { const u = new URL(ADMIN!); u.pathname = `/${banco}`; return u.toString(); };

type Resultado = { situacao: string; score: number; vagas: number; precisa_superar: number | null; anterior?: number; recorde?: number; removido?: number };

describe.skipIf(!ADMIN)('Top 3 por conta, no Postgres', () => {
  let admin: pg.Client, db: pg.Pool, desafio: string;

  beforeAll(async () => {
    admin = new pg.Client({ connectionString: ADMIN }); await admin.connect();
    await admin.query(`create database ${BANCO}`);
    db = new pg.Pool({ connectionString: urlDo(BANCO), max: 25 });
    /*
     * Na faxina, o banco descartável é apagado com as conexões ainda fechando,
     * e o servidor as encerra. É esperado; sem este ouvinte, o aviso vira
     * exceção solta e mancha uma execução que passou.
     */
    db.on('error', () => undefined);
    await db.query(sql('tests/sql/supabase-stub.sql'));
    for (const m of migracoes) await db.query(sql(`supabase/migrations/${m}`));
    desafio = (await db.query(`insert into public.ranked_challenges(mode, period_key, seed, engine_version, balance_version, roster_fingerprint)
      values ('daily', '2026-10-07', 1, 'teste', 'season-1', 'x') returning id`)).rows[0].id;
  }, 60000);

  afterAll(async () => {
    await db?.end();
    await admin?.query(`drop database if exists ${BANCO} with (force)`);
    await admin?.end();
  });

  let n = 0;
  const conta = async () => {
    const id = randomUUID();
    await db.query('insert into auth.users(id) values ($1)', [id]);
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Jogador_${++n}`]);
    return id;
  };
  /* Uma partida verificada: a tabela de entradas aponta para ela. */
  const partida = async (jogador: string, trio: string[], score: number) =>
    (await db.query(`insert into public.ranked_runs(player_id, challenge_id, mode, period_key, seed, engine_version, balance_version,
        roster_fingerprint, team_ids, finished_at, encounters_cleared, score, verified)
      values ($1, $2, 'daily', '2026-10-07', 1, 'teste', 'season-1', 'x', $3, now(), 3, $4, true) returning id`,
      [jogador, desafio, trio, score])).rows[0].id as string;
  const registrar = async (jogador: string, trio: string[], score: number, escopo = 'daily', periodo = '2026-10-07', cliente: pg.Pool | pg.PoolClient = db) => {
    const run = await partida(jogador, trio, score);
    const r = await cliente.query('select public.registrar_no_top3($1, $2, $3, $4, $5, $6, 3::smallint) as r', [jogador, escopo, periodo, trio, run, score]);
    return r.rows[0].r as Resultado;
  };
  const ativas = async (jogador: string, escopo = 'daily', periodo = '2026-10-07') =>
    (await db.query(`select canonical_team, score from public.leaderboard_entries
      where player_id = $1 and scope = $2 and period_key = $3 order by score desc`, [jogador, escopo, periodo])).rows as { canonical_team: string; score: number }[];

  const A = ['goku', 'storm', 'pikachu'], B = ['naruto', 'sasuke', 'sakura'], C = ['thor', 'loki', 'hulk'], D = ['batman', 'robin', 'alfred'];

  it('mesmo trio: pontuação menor mantém o recorde, maior atualiza a mesma entrada', async () => {
    const j = await conta();
    expect((await registrar(j, A, 1500)).situacao).toBe('novo');
    /* A ordem dos ids não cria trio novo. */
    expect(await registrar(j, ['pikachu', 'goku', 'storm'], 1300)).toMatchObject({ situacao: 'manteve', recorde: 1500 });
    expect(await registrar(j, ['storm', 'pikachu', 'goku'], 1550)).toMatchObject({ situacao: 'melhorou', anterior: 1500 });
    expect(await ativas(j)).toEqual([{ canonical_team: 'goku|pikachu|storm', score: 1550 }]);
  });

  it('quarto trio, exatamente o exemplo do documento', async () => {
    const j = await conta();
    await registrar(j, A, 1500); await registrar(j, B, 1400);
    expect(await registrar(j, C, 1300)).toMatchObject({ situacao: 'novo', vagas: 0, precisa_superar: 1300 });
    /* "1.200 pontos. Não entrou nos seus 3 melhores. Para entrar: supere 1.300." */
    expect(await registrar(j, D, 1200)).toMatchObject({ situacao: 'fora', precisa_superar: 1300 });
    /* "NOVO TOP 3. 1.550 entrou no ranking. O resultado de 1.300 saiu dos seus 3 melhores." */
    expect(await registrar(j, D, 1550)).toMatchObject({ situacao: 'entrou', removido: 1300, precisa_superar: 1400 });
    expect((await ativas(j)).map((e) => e.score)).toEqual([1550, 1500, 1400]);
  });

  it('empate com o pior não entra: é preciso superar', async () => {
    const j = await conta();
    await registrar(j, A, 1500); await registrar(j, B, 1400); await registrar(j, C, 1300);
    expect(await registrar(j, D, 1300)).toMatchObject({ situacao: 'fora', precisa_superar: 1300 });
  });

  it('conta as vagas livres', async () => {
    const j = await conta();
    expect(await registrar(j, A, 900)).toMatchObject({ vagas: 2, precisa_superar: null });
    expect(await registrar(j, B, 800)).toMatchObject({ vagas: 1, precisa_superar: null });
  });

  it('cada ranking tem os seus 3: Hoje cheio não ocupa a Temporada', async () => {
    const j = await conta();
    for (const [t, s] of [[A, 10], [B, 20], [C, 30]] as const) await registrar(j, t, s);
    expect(await registrar(j, D, 5, 'season', 'season-1')).toMatchObject({ situacao: 'novo', vagas: 2 });
    expect(await registrar(j, D, 5, 'daily', '2026-10-08')).toMatchObject({ situacao: 'novo' });
  });

  it('o ranking pode mostrar a mesma conta 3 vezes, nunca 4', async () => {
    const j = await conta();
    for (const [t, s] of [[A, 100], [B, 200], [C, 300], [D, 400]] as const) await registrar(j, t, s, 'daily', '2026-10-09');
    const linhas = (await db.query(`select player_id from public.leaderboard_entries where scope = 'daily' and period_key = '2026-10-09'`)).rows;
    expect(linhas).toHaveLength(3);
  });

  it('nem um INSERT direto abre a quarta vaga', async () => {
    const j = await conta();
    for (const [t, s] of [[A, 1], [B, 2], [C, 3]] as const) await registrar(j, t, s);
    const run = await partida(j, D, 4);
    await expect(db.query(`insert into public.leaderboard_entries(player_id, scope, period_key, canonical_team, team_ids, run_id, score, encounters_cleared)
      values ($1, 'daily', '2026-10-07', public.trio_canonico($2), $2, $3, 4, 1)`, [j, D, run])).rejects.toMatchObject({ code: '23514' });
  });

  it('recusa trio com integrante repetido', async () => {
    const j = await conta();
    await expect(registrar(j, ['goku', 'goku', 'storm'], 10)).rejects.toMatchObject({ code: '22023' });
  });

  /*
   * "Duas submissões simultâneas nunca podem criar 4 slots."
   *
   * Vinte trios diferentes da mesma conta, cada um pela sua conexão, todos
   * soltos ao mesmo tempo. Sem a trava, várias conexões contariam "2 ativas"
   * juntas e inseririam juntas. Com ela, sobram exatamente as 3 maiores.
   */
  it('vinte partidas simultâneas da mesma conta deixam exatamente as 3 melhores', async () => {
    const j = await conta();
    const trios = Array.from({ length: 20 }, (_, i) => [`a${i}`, `b${i}`, `c${i}`]);
    const scores = trios.map((_, i) => 1000 + ((i * 37) % 20) * 10);
    const runs = await Promise.all(trios.map((t, i) => partida(j, t, scores[i])));
    const clientes = await Promise.all(trios.map(() => db.connect()));
    try {
      await Promise.all(clientes.map(async (c, i) => {
        await c.query('begin');
        await c.query('select public.registrar_no_top3($1, $2, $3, $4, $5, $6, 3::smallint)', [j, 'daily', '2026-10-10', trios[i], runs[i], scores[i]]);
        await c.query('commit');
      }));
    } finally { clientes.forEach((c) => c.release()); }
    const fim = await ativas(j, 'daily', '2026-10-10');
    expect(fim).toHaveLength(3);
    expect(fim.map((e) => e.score)).toEqual([...scores].sort((a, b) => b - a).slice(0, 3));
  });

  it('o mesmo trio enviado várias vezes ao mesmo tempo vira uma entrada, com a maior pontuação', async () => {
    const j = await conta();
    const scores = [700, 950, 800, 900, 650, 990, 720];
    const runs = await Promise.all(scores.map((s) => partida(j, A, s)));
    await Promise.all(scores.map((s, i) => db.query('select public.registrar_no_top3($1, $2, $3, $4, $5, $6, 3::smallint)',
      [j, 'daily', '2026-10-11', i % 2 ? [...A].reverse() : A, runs[i], s])));
    expect(await ativas(j, 'daily', '2026-10-11')).toEqual([{ canonical_team: 'goku|pikachu|storm', score: 990 }]);
  });

  /*
   * O Supabase concede tudo a `anon` e `authenticated` em tabela nova —
   * inclusive TRUNCATE, que passa por cima de RLS. O stub imita isso; este
   * teste garante que a migração tira.
   */
  it('nem visitante nem jogador apagam a tabela inteira', async () => {
    for (const papel of ['anon', 'authenticated']) {
      const c = await db.connect();
      try {
        await c.query('begin'); await c.query(`set local role ${papel}`);
        await expect(c.query('truncate public.leaderboard_entries')).rejects.toMatchObject({ code: '42501' });
        await c.query('rollback');
        await c.query('begin'); await c.query(`set local role ${papel}`);
        await expect(c.query('truncate public.ranked_runs cascade')).rejects.toMatchObject({ code: '42501' });
        await c.query('rollback');
      } finally { c.release(); }
    }
  });

  /* "service_role fora do frontend": o navegador não consegue nem chamar. */
  it('um jogador logado não registra nem escreve direto', async () => {
    const j = await conta(), run = await partida(j, A, 1);
    const c = await db.connect();
    try {
      await c.query('begin'); await c.query('set local role authenticated');
      await expect(c.query('select public.registrar_no_top3($1, $2, $3, $4, $5, 99, 3::smallint)', [j, 'daily', '2026-10-12', A, run]))
        .rejects.toMatchObject({ code: '42501' });
      await c.query('rollback');
      await c.query('begin'); await c.query('set local role authenticated');
      await expect(c.query(`insert into public.leaderboard_entries(player_id, scope, period_key, canonical_team, team_ids, run_id, score, encounters_cleared)
        values ($1, 'daily', '2026-10-12', 'goku|pikachu|storm', $2, $3, 99, 1)`, [j, A, run])).rejects.toMatchObject({ code: '42501' });
      await c.query('rollback');
    } finally { c.release(); }
  });
});

/*
 * As partidas verificadas antes desta migração entram pela mesma regra. Num
 * banco à parte, porque precisa das partidas existirem *antes* da migração.
 */
describe.skipIf(!ADMIN)('Top 3 · partidas que já existiam', () => {
  it('a migração reconstrói o Top 3 de cada conta a partir do histórico', async () => {
    const banco = `${BANCO}_hist`, adm = new pg.Client({ connectionString: ADMIN });
    await adm.connect(); await adm.query(`create database ${banco}`);
    const c = new pg.Client({ connectionString: urlDo(banco) }); await c.connect();
    try {
      await c.query(sql('tests/sql/supabase-stub.sql'));
      for (const m of migracoes.filter((x) => !x.includes('top3'))) await c.query(sql(`supabase/migrations/${m}`));
      const j = randomUUID();
      await c.query('insert into auth.users(id) values ($1)', [j]);
      await c.query(`insert into public.players(id, handle) values ($1, 'Antigo')`, [j]);
      const ch = (await c.query(`insert into public.ranked_challenges(mode, period_key, seed, engine_version, balance_version, roster_fingerprint)
        values ('daily', '2026-10-07', 1, 't', 'season-1', 'x') returning id`)).rows[0].id;
      const historico: [string[], number][] = [[['a', 'b', 'c'], 500], [['d', 'e', 'f'], 900], [['c', 'b', 'a'], 700], [['g', 'h', 'i'], 300], [['j', 'k', 'l'], 800]];
      for (const [i, [t, s]] of historico.entries()) await c.query(`insert into public.ranked_runs(player_id, challenge_id, mode, period_key, seed, engine_version,
          balance_version, roster_fingerprint, team_ids, finished_at, encounters_cleared, score, verified)
        values ($1, $2, 'daily', '2026-10-07', 1, 't', 'season-1', 'x', $3, now() + make_interval(secs => $4), 2, $5, true)`, [j, ch, t, i, s]);
      await c.query(sql(`supabase/migrations/${migracoes.find((x) => x.includes('top3'))}`));
      for (const escopo of ['daily', 'season']) {
        const r = (await c.query(`select canonical_team, score from public.leaderboard_entries where scope = $1 order by score desc`, [escopo])).rows;
        /* a|b|c aparece uma vez só, com 700 (o melhor dos dois); g|h|i (300) ficou de fora. */
        expect(r).toEqual([{ canonical_team: 'd|e|f', score: 900 }, { canonical_team: 'j|k|l', score: 800 }, { canonical_team: 'a|b|c', score: 700 }]);
      }
    } finally {
      await c.end(); await adm.query(`drop database if exists ${banco} with (force)`); await adm.end();
    }
  }, 60000);
});
