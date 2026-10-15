/*
 * Comunidade (presença, chat global, privadas com "visto"), num Postgres de verdade.
 *
 * Roda as migrações reais num banco descartável e confere, como cada jogador
 * logado (papel `authenticated` com o id dele), o que ele consegue ler e fazer:
 * a privada só para os dois, o visto só por quem recebeu, nada de escrever
 * direto nas tabelas, o ritmo do chat e a presença online/offline.
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_comunidade_${Date.now()}`;
const migracoes = readdirSync('supabase/migrations').filter((f) => f.endsWith('.sql')).sort();
const sql = (f: string) => readFileSync(f, 'utf8');
const urlDo = (banco: string) => { const u = new URL(ADMIN!); u.pathname = `/${banco}`; return u.toString(); };

describe.skipIf(!ADMIN)('Comunidade, no Postgres', () => {
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
  const conta = async (comNome = true) => {
    const id = randomUUID();
    await db.query('insert into auth.users(id) values ($1)', [id]);
    if (comNome) await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Chat_${++n}`]);
    return id;
  };
  /* Roda `q` como o jogador `quem`, do jeito que o navegador chega ao banco. */
  const como = async <T extends pg.QueryResultRow = pg.QueryResultRow>(quem: string | null, q: string, args: unknown[] = []) => {
    const c = await db.connect();
    try {
      await c.query('begin');
      await c.query(`set local role ${quem ? 'authenticated' : 'anon'}`);
      if (quem) await c.query(`select set_config('request.jwt.claim.sub', $1, true)`, [quem]);
      const r = await c.query<T>(q, args);
      await c.query('commit');
      return r;
    } catch (e) { await c.query('rollback'); throw e; } finally { c.release(); }
  };

  it('chat global: todo logado lê e escreve; sem login, nada', async () => {
    const ana = await conta(), beto = await conta();
    const m = (await como(ana, `select * from public.chat_enviar('  Bora jogar?  ')`)).rows[0];
    expect(m.texto).toBe('Bora jogar?');
    expect(m.para_id).toBeNull();
    const lidas = await como(beto, 'select texto from public.chat_mensagens where para_id is null');
    expect(lidas.rows.map((r) => r.texto)).toContain('Bora jogar?');
    await expect(como(null, 'select * from public.chat_mensagens')).rejects.toThrow(/permission denied/);
    await expect(como(null, `select public.chat_enviar('oi')`)).rejects.toThrow(/permission denied/);
  });

  it('ninguém escreve, muda ou apaga direto nas tabelas', async () => {
    const ana = await conta(), beto = await conta();
    const id = (await como(ana, `select id from public.chat_enviar('minha')`)).rows[0].id;
    await expect(como(beto, `insert into public.chat_mensagens(autor_id, texto) values ($1, 'falsa')`, [ana])).rejects.toThrow(/permission denied/);
    await expect(como(beto, `update public.chat_mensagens set texto = 'mudei' where id = $1`, [id])).rejects.toThrow(/permission denied/);
    await expect(como(beto, `delete from public.chat_mensagens where id = $1`, [id])).rejects.toThrow(/permission denied/);
    await expect(como(ana, 'truncate public.chat_mensagens')).rejects.toThrow(/permission denied/);
    await expect(como(beto, `update public.comunidade_presenca set online = true`)).rejects.toThrow(/permission denied/);
  });

  it('privada: só os dois leem; um terceiro não vê nem pela tabela nem pelas conversas', async () => {
    const ana = await conta(), beto = await conta(), caio = await conta();
    await como(ana, `select public.chat_enviar('segredo', $1)`, [beto]);
    const deBeto = await como(beto, `select texto from public.chat_mensagens where para_id is not null`);
    expect(deBeto.rows.map((r) => r.texto)).toEqual(['segredo']);
    const deCaio = await como(caio, `select texto from public.chat_mensagens where texto = 'segredo'`);
    expect(deCaio.rowCount).toBe(0);
    expect((await como(caio, 'select * from public.chat_conversas()')).rowCount).toBe(0);
    const conversa = (await como(beto, 'select * from public.chat_conversas()')).rows[0];
    expect(conversa).toMatchObject({ com_id: ana, ultima_texto: 'segredo', ultima_minha: false, ultima_vista: false, nao_lidas: 1 });
  });

  it('privada para quem está offline fica guardada, e o visto só vem quando ele abre', async () => {
    const ana = await conta(), beto = await conta();
    await como(beto, 'select public.comunidade_ping()');
    await como(beto, 'select public.comunidade_sair()');
    await como(ana, `select public.chat_enviar('quando voltar, me chama', $1)`, [beto]);
    let daAna = (await como(ana, 'select * from public.chat_conversas()')).rows[0];
    expect(daAna).toMatchObject({ ultima_minha: true, ultima_vista: false });
    // um terceiro (ou a própria Ana) não consegue marcar como vista
    expect((await como(ana, 'select public.chat_marcar_vistas($1) as n', [beto])).rows[0].n).toBe(0);
    const caio = await conta();
    expect((await como(caio, 'select public.chat_marcar_vistas($1) as n', [ana])).rows[0].n).toBe(0);
    // Beto entra e abre a conversa
    expect((await como(beto, 'select public.chat_marcar_vistas($1) as n', [ana])).rows[0].n).toBe(1);
    daAna = (await como(ana, 'select * from public.chat_conversas()')).rows[0];
    expect(daAna).toMatchObject({ ultima_vista: true });
    expect((await como(beto, 'select * from public.chat_conversas()')).rows[0].nao_lidas).toBe(0);
  });

  it('não manda para si, para quem não existe, nem resposta de outra conversa', async () => {
    const ana = await conta(), beto = await conta(), caio = await conta();
    await expect(como(ana, `select public.chat_enviar('eu', $1)`, [ana])).rejects.toThrow(/destinatário/);
    await expect(como(ana, `select public.chat_enviar('ninguém', $1)`, [randomUUID()])).rejects.toThrow(/destinatário/);
    const privada = (await como(beto, `select id from public.chat_enviar('entre nós', $1)`, [caio])).rows[0].id;
    await expect(como(ana, `select public.chat_enviar('respondo', null, $1)`, [privada])).rejects.toThrow(/resposta/);
    await expect(como(ana, `select public.chat_enviar('   ')`)).rejects.toThrow(/vazia/);
    await expect(como(ana, `select public.chat_enviar($1)`, ['x'.repeat(501)])).rejects.toThrow(/500/);
    const global = (await como(beto, `select id from public.chat_enviar('pergunta')`)).rows[0].id;
    const resposta = (await como(ana, `select * from public.chat_enviar('resposta', null, $1)`, [global])).rows[0];
    expect(Number(resposta.resposta_a)).toBe(Number(global));
  });

  it('sem nome público não entra na comunidade', async () => {
    const semNome = await conta(false);
    await expect(como(semNome, `select public.chat_enviar('oi')`)).rejects.toThrow(/escolha seu nome/);
    await expect(como(semNome, 'select * from public.comunidade_jogadores()')).rejects.toThrow(/escolha seu nome/);
  });

  it('ritmo: no máximo 6 a cada 15 s, e sem repetir a mesma frase', async () => {
    const ana = await conta();
    await como(ana, `select public.chat_enviar('igual')`);
    await expect(como(ana, `select public.chat_enviar('igual')`)).rejects.toThrow(/repetida/);
    for (let i = 0; i < 5; i++) await como(ana, `select public.chat_enviar($1)`, [`msg ${i}`]);
    await expect(como(ana, `select public.chat_enviar('a sétima')`)).rejects.toThrow(/devagar/);
  });

  it('reações: uma por pessoa, trocar substitui, o mesmo emoji tira; privada alheia, não', async () => {
    const ana = await conta(), beto = await conta(), caio = await conta();
    const id = (await como(ana, `select id from public.chat_enviar('reage aí')`)).rows[0].id;
    await como(beto, `select public.chat_reagir($1, '🔥')`, [id]);
    await como(beto, `select public.chat_reagir($1, '😂')`, [id]);
    let r = await como(caio, 'select emoji from public.chat_reacoes where mensagem_id = $1', [id]);
    expect(r.rows).toEqual([{ emoji: '😂' }]);
    await como(beto, `select public.chat_reagir($1, '😂')`, [id]);
    r = await como(caio, 'select emoji from public.chat_reacoes where mensagem_id = $1', [id]);
    expect(r.rows).toEqual([{ emoji: null }]);
    await expect(como(beto, `select public.chat_reagir($1, 'xx')`, [id])).rejects.toThrow(/reação inválida/);
    const privada = (await como(ana, `select id from public.chat_enviar('só nós', $1)`, [beto])).rows[0].id;
    await expect(como(caio, `select public.chat_reagir($1, '🔥')`, [privada])).rejects.toThrow(/não encontrada/);
  });

  it('presença: online ao marcar, offline ao sair, "online desde" só reinicia na volta', async () => {
    const ana = await conta(), beto = await conta();
    const dela = async () => (await como(beto, 'select * from public.comunidade_jogadores() where id = $1', [ana])).rows[0];
    let j = await dela();
    expect(j).toMatchObject({ online: false, online_desde: null, visto_em: null });
    await como(ana, 'select public.comunidade_ping()');
    j = await dela();
    expect(j.online).toBe(true);
    const desde = j.online_desde as Date;
    await db.query(`update public.comunidade_presenca set online_desde = online_desde - interval '10 minutes', visto_em = now() - interval '20 seconds' where player_id = $1`, [ana]);
    await como(ana, 'select public.comunidade_ping()');
    j = await dela();
    expect(j.online).toBe(true);
    expect((j.online_desde as Date).getTime()).toBeLessThan(desde.getTime() - 9 * 60_000);
    await como(ana, 'select public.comunidade_sair()');
    j = await dela();
    expect(j.online).toBe(false);
    // quem some sem avisar (bateria, sinal) cai para offline depois de 75 s
    await como(ana, 'select public.comunidade_ping()');
    await db.query(`update public.comunidade_presenca set visto_em = now() - interval '2 minutes' where player_id = $1`, [ana]);
    expect((await dela()).online).toBe(false);
    await como(ana, 'select public.comunidade_ping()');
    j = await dela();
    expect(j.online).toBe(true);
    expect(Date.now() - (j.online_desde as Date).getTime()).toBeLessThan(60_000);
  });

  it('lista da comunidade traz o recorde, o trio e as conquistas de cada um', async () => {
    const ana = await conta(), beto = await conta();
    const desafio = (await db.query(`insert into public.ranked_challenges(mode, period_key, seed, engine_version, balance_version, roster_fingerprint)
      values ('daily', '2026-10-15', 7, 'teste-com', 'season-1', 'x') returning id`)).rows[0].id;
    const run = (await db.query(`insert into public.ranked_runs(player_id, challenge_id, mode, period_key, seed, engine_version, balance_version,
        roster_fingerprint, team_ids, finished_at, encounters_cleared, score, verified)
      values ($1, $2, 'daily', '2026-10-15', 7, 'teste-com', 'season-1', 'x', array['goku','gojo','pikachu'], now(), 10, 1500000, true) returning id`, [ana, desafio])).rows[0].id;
    await db.query(`select public.registrar_no_top3($1, 'season', 'geral@t', array['goku','gojo','pikachu'], $2, 1500000, 10::smallint, now())`, [ana, run]);
    await db.query(`insert into public.player_achievements(player_id, achievement_id) values ($1, 'personagem:goku'), ($1, 'personagem:gojo')`, [ana]);
    const j = (await como(beto, 'select * from public.comunidade_jogadores() where id = $1', [ana])).rows[0];
    expect(j).toMatchObject({ recorde: 1500000, trio: ['goku', 'gojo', 'pikachu'], conquistas: 2 });
  });
});
