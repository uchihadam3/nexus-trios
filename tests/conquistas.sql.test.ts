/*
 * Conquistas no Postgres: o SQL que refaz as conquistas a partir das jornadas
 * validadas (scripts/conquistas.sql, rodado por scripts/publicar-funcao.sh).
 *
 * Só jornada validada com as 10 lutas terminadas libera; cada personagem conta
 * uma vez, com a data da primeira; o total de cada conta é o que o ranking
 * ordena; e rodar de novo não muda nada.
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_conquistas_${Date.now()}`;
const migracoes = readdirSync('supabase/migrations').filter((f) => f.endsWith('.sql')).sort();
const sql = (f: string) => readFileSync(f, 'utf8');
const urlDo = (banco: string) => { const u = new URL(ADMIN!); u.pathname = `/${banco}`; return u.toString(); };

describe.skipIf(!ADMIN)('Conquistas, no Postgres', () => {
  let admin: pg.Client, db: pg.Pool, desafio: string;
  beforeAll(async () => {
    admin = new pg.Client({ connectionString: ADMIN }); await admin.connect();
    await admin.query(`create database ${BANCO}`);
    db = new pg.Pool({ connectionString: urlDo(BANCO), max: 5 });
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
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Colecionador_${++n}`]);
    return id;
  };
  const jornada = (jogador: string, trio: string[], lutas: number, quando: string, validada = true) => db.query(
    `insert into public.ranked_runs(player_id, challenge_id, mode, period_key, seed, engine_version, balance_version, roster_fingerprint, team_ids, finished_at, encounters_cleared, score, verified)
     values ($1, $2, 'daily', '2026-10-07', 1, 'teste', 'season-1', 'x', $3, $4, $5, $6, $7)`,
    [jogador, desafio, trio, validada ? quando : null, validada ? lutas : null, validada ? 1000 : null, validada]);
  const liberadas = async (jogador: string) => (await db.query(`select achievement_id, unlocked_at from public.player_achievements
    where player_id = $1 and achievement_id like 'personagem:%' order by achievement_id`, [jogador])).rows as { achievement_id: string; unlocked_at: Date }[];
  const total = async (jogador: string) => (await db.query(`select progress, unlocked_at from public.player_achievements where player_id = $1 and achievement_id = 'conquistas:total'`, [jogador])).rows[0] as { progress: number; unlocked_at: Date } | undefined;

  it('só as 10 lutas terminadas liberam, cada personagem uma vez, com a data da primeira', async () => {
    const j = await conta();
    await jornada(j, ['jill', 'vegeta', 'goku'], 10, '2026-10-01T10:00:00Z');
    await jornada(j, ['jill', 'light', 'xavier'], 10, '2026-10-02T10:00:00Z');
    await jornada(j, ['naruto', 'sasuke', 'sakura'], 9, '2026-10-03T10:00:00Z');
    await jornada(j, ['thor', 'loki', 'hulk'], 10, '2026-10-04T10:00:00Z', false);
    await db.query(sql('scripts/conquistas.sql'));
    const l = await liberadas(j);
    expect(l.map((x) => x.achievement_id)).toEqual(['personagem:goku', 'personagem:jill', 'personagem:light', 'personagem:vegeta', 'personagem:xavier']);
    expect(l.find((x) => x.achievement_id === 'personagem:jill')!.unlocked_at.toISOString()).toBe('2026-10-01T10:00:00.000Z');
    const t = await total(j);
    expect(t?.progress).toBe(5);
    expect(t?.unlocked_at.toISOString()).toBe('2026-10-02T10:00:00.000Z');
  });

  it('rodar de novo não muda nada, e uma jornada nova sobe o total', async () => {
    const j = await conta();
    await jornada(j, ['goku', 'pikachu', 'gojo'], 10, '2026-10-05T10:00:00Z');
    await db.query(sql('scripts/conquistas.sql'));
    const antes = await total(j);
    await db.query(sql('scripts/conquistas.sql'));
    expect(await total(j)).toEqual(antes);
    await jornada(j, ['goku', 'luffy', 'zoro'], 10, '2026-10-06T10:00:00Z');
    await db.query(sql('scripts/conquistas.sql'));
    expect((await total(j))?.progress).toBe(5);
  });

  it('o navegador só lê as próprias conquistas e não escreve', async () => {
    const r = await db.query(`select has_table_privilege('authenticated', 'public.player_achievements', 'insert') as escreve,
      has_table_privilege('authenticated', 'public.player_achievements', 'select') as le,
      has_table_privilege('anon', 'public.player_achievements', 'insert') as anon_escreve`);
    expect(r.rows[0]).toEqual({ escreve: false, le: true, anon_escreve: false });
  });
});
