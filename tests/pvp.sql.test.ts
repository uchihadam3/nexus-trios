/*
 * PvP online, no Postgres: quem lê o quê, o segredo dos times e das escolhas, uma partida aberta por pessoa e o
 * rating (Elo) aplicado numa transação só. As escritas da partida são da função do servidor (service_role).
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';
import { variacaoDoElo } from '../src/engine/pvp';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_pvp_${Date.now()}`;
const migracoes = readdirSync('supabase/migrations').filter((f) => f.endsWith('.sql')).sort();
const sql = (f: string) => readFileSync(f, 'utf8');
const urlDo = (banco: string) => { const u = new URL(ADMIN!); u.pathname = `/${banco}`; return u.toString(); };

describe.skipIf(!ADMIN)('PvP online, no Postgres', () => {
  let admin: pg.Client, db: pg.Pool;
  beforeAll(async () => {
    admin = new pg.Client({ connectionString: ADMIN }); await admin.connect();
    await admin.query(`create database ${BANCO}`);
    db = new pg.Pool({ connectionString: urlDo(BANCO), max: 10 });
    db.on('error', () => undefined);
    await db.query(sql('tests/sql/supabase-stub.sql'));
    for (const m of migracoes) await db.query(sql(`supabase/migrations/${m}`));
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
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Pvp_${++n}`]);
    return id;
  };
  const como = async (papel: 'authenticated' | 'service_role', quem: string | null, q: string, args: unknown[] = []) => {
    const c = await db.connect();
    try {
      await c.query('begin'); await c.query(`set local role ${papel}`);
      if (quem) await c.query(`select set_config('request.jwt.claim.sub', $1, true)`, [quem]);
      const r = await c.query(q, args); await c.query('commit'); return r;
    } catch (e) { await c.query('rollback'); throw e; } finally { c.release(); }
  };
  const partida = async (a: string, b: string, estado = 'jogando') =>
    (await db.query(`insert into public.pvp_partidas(desafiante, desafiado, estado, seed, versao_do_motor) values ($1, $2, $3, 42, 'teste') returning id`, [a, b, estado])).rows[0].id as string;

  it('só os dois da partida a leem; ninguém escreve nela pelo navegador', async () => {
    const a = await conta(), b = await conta(), c = await conta();
    const id = await partida(a, b);
    expect((await como('authenticated', a, 'select id from public.pvp_partidas where id = $1', [id])).rowCount).toBe(1);
    expect((await como('authenticated', b, 'select id from public.pvp_partidas where id = $1', [id])).rowCount).toBe(1);
    expect((await como('authenticated', c, 'select id from public.pvp_partidas where id = $1', [id])).rowCount).toBe(0);
    await expect(como('authenticated', a, `update public.pvp_partidas set vencedor = $2 where id = $1`, [id, a])).rejects.toThrow(/permission denied/);
    await expect(como('authenticated', a, `insert into public.pvp_partidas(desafiante, desafiado, seed, versao_do_motor) values ($1, $2, 1, 'x')`, [a, c])).rejects.toThrow(/permission denied/);
    await expect(como('authenticated', a, `update public.pvp_ratings set rating = 3000`)).rejects.toThrow(/permission denied/);
  });

  it('os times e as escolhas são segredo: ninguém lê pelo navegador', async () => {
    const a = await conta(), b = await conta();
    const id = await partida(a, b);
    await db.query(`insert into public.pvp_times(partida_id, jogador, times) values ($1, $2, '[["goku","vegeta","gohan"]]')`, [id, a]);
    await db.query(`insert into public.pvp_escolhas(partida_id, n, jogador, time) values ($1, 0, $2, 1)`, [id, a]);
    await expect(como('authenticated', b, 'select * from public.pvp_times')).rejects.toThrow(/permission denied/);
    await expect(como('authenticated', b, 'select * from public.pvp_escolhas')).rejects.toThrow(/permission denied/);
    await expect(como('authenticated', a, 'select * from public.pvp_rodadas')).rejects.toThrow(/permission denied/);
  });

  it('uma partida aberta por pessoa de cada vez', async () => {
    const a = await conta(), b = await conta(), c = await conta();
    await partida(a, b, 'convite');
    await expect(partida(a, c, 'convite')).rejects.toThrow(/pvp_uma_aberta_a/);
    await expect(partida(c, b, 'montando')).rejects.toThrow(/pvp_uma_aberta_b/);
  });

  it('Elo: rating igual dá +16/−16, e o mesmo resultado não conta duas vezes', async () => {
    const a = await conta(), b = await conta();
    const id = await partida(a, b);
    const r = (await como('service_role', null, 'select * from public.pvp_aplicar_resultado($1, $2, $3)', [id, b, 'venceu com os 3 times'])).rows[0];
    expect(r).toMatchObject({ delta_a: -16, delta_b: 16, rating_a: 1000, rating_b: 1000 });
    const de = async (id_: string) => (await db.query('select rating, vitorias, derrotas from public.pvp_ratings where player_id = $1', [id_])).rows[0];
    expect(await de(a)).toEqual({ rating: 984, vitorias: 0, derrotas: 1 });
    expect(await de(b)).toEqual({ rating: 1016, vitorias: 1, derrotas: 0 });
    await como('service_role', null, 'select * from public.pvp_aplicar_resultado($1, $2, $3)', [id, b, 'de novo']);
    expect(await de(b)).toEqual({ rating: 1016, vitorias: 1, derrotas: 0 });
    const p = (await db.query('select estado, vencedor from public.pvp_partidas where id = $1', [id])).rows[0];
    expect(p).toEqual({ estado: 'terminada', vencedor: b });
  });

  it('o Elo do banco é o mesmo do jogo (src/engine/pvp.ts)', async () => {
    const a = await conta(), b = await conta();
    await db.query(`insert into public.pvp_ratings(player_id, rating) values ($1, 1180), ($2, 940)`, [a, b]);
    const id = await partida(a, b);
    const r = (await como('service_role', null, 'select * from public.pvp_aplicar_resultado($1, $2, $3)', [id, b, 'x'])).rows[0];
    expect(r.delta_b).toBe(variacaoDoElo(940, 1180, true));
    expect(r.delta_a).toBe(-variacaoDoElo(940, 1180, true));
  });

  it('o navegador não aplica resultado; o ranking ele lê', async () => {
    const a = await conta(), b = await conta();
    const id = await partida(a, b);
    await expect(como('authenticated', a, 'select * from public.pvp_aplicar_resultado($1, $2, $3)', [id, a, 'x'])).rejects.toThrow(/permission denied/);
    const r = await como('authenticated', a, 'select * from public.pvp_ranking(10)');
    expect(r.rows.length).toBeGreaterThan(0);
    expect(r.rows[0]).toHaveProperty('rating');
  });
});
