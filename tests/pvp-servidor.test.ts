/*
 * O juiz do PvP online (supabase/functions/ranked-api/pvp.ts) jogando uma partida inteira contra um Postgres de
 * verdade: desafio, aceite, os 3 times (segredo até os dois ficarem prontos), a escolha secreta de cada rodada, a
 * luta calculada pelo motor, o "começar duelo", o prazo que sorteia o time de quem sumiu e o rating no fim.
 *
 * O servidor fala com o banco pelo cliente do Supabase (PostgREST); aqui um adaptador pequeno faz as mesmas
 * consultas em SQL, como o serviço (service_role).
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';
import { acaoPvp } from '../supabase/functions/ranked-api/pvp';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_pvpsrv_${Date.now()}`;
const migracoes = readdirSync('supabase/migrations').filter((f) => f.endsWith('.sql')).sort();
const sql = (f: string) => readFileSync(f, 'utf8');
const urlDo = (banco: string) => { const u = new URL(ADMIN!); u.pathname = `/${banco}`; return u.toString(); };

/* ---------------------------------------------------------------------------
 * Um PostgREST de bolso: só o que o servidor do PvP usa
 * ------------------------------------------------------------------------- */
type Linha = Record<string, unknown>;
function cliente(db: pg.Pool) {
  class Consulta implements PromiseLike<{ data: unknown; error: { code?: string; message: string } | null }> {
    private onde: string[] = []; private args: unknown[] = []; private ordem = ''; private limite = ''; private um: 'single' | 'maybe' | null = null;
    private tipo: 'select' | 'insert' | 'update' | 'upsert' = 'select'; private dados: Linha | Linha[] | null = null; private colunas = '*';
    private conflito = ''; private ignorar = false;
    constructor(private tabela: string) {}
    private p(v: unknown) { this.args.push(v); return `$${this.args.length}`; }
    select(c = '*') { this.colunas = c; return this; }
    insert(d: Linha | Linha[]) { this.tipo = 'insert'; this.dados = d; return this; }
    upsert(d: Linha, o: { onConflict: string; ignoreDuplicates?: boolean }) { this.tipo = 'upsert'; this.dados = d; this.conflito = o.onConflict; this.ignorar = !!o.ignoreDuplicates; return this; }
    update(d: Linha) { this.tipo = 'update'; this.dados = d; return this; }
    eq(c: string, v: unknown) { this.onde.push(`${c} = ${this.p(v)}`); return this; }
    lt(c: string, v: unknown) { this.onde.push(`${c} < ${this.p(v)}`); return this; }
    is(c: string, v: null) { this.onde.push(`${c} is ${v === null ? 'null' : 'not null'}`); return this; }
    in(c: string, vs: unknown[]) { this.onde.push(`${c} = any(${this.p(vs)})`); return this; }
    like(c: string, v: string) { this.onde.push(`${c} like ${this.p(v)}`); return this; }
    or(expr: string) {
      // "a.eq.X,b.eq.X" ou "a.in.(x,y),b.in.(x,y)"
      const partes = expr.match(/[a-z_]+\.(?:eq\.[^,]+|in\.\([^)]*\))/g) ?? [];
      this.onde.push(`(${partes.map((t) => { const [c, op, ...r] = t.split('.'); const v = r.join('.'); return op === 'eq' ? `${c} = ${this.p(v)}` : `${c} = any(${this.p(v.slice(1, -1).split(','))})`; }).join(' or ')})`);
      return this;
    }
    order(c: string, o?: { ascending?: boolean }) { this.ordem = ` order by ${c} ${o?.ascending === false ? 'desc' : 'asc'}`; return this; }
    limit(n: number) { this.limite = ` limit ${n}`; return this; }
    single() { this.um = 'single'; return this; }
    maybeSingle() { this.um = 'maybe'; return this; }
    private sql() {
      const w = this.onde.length ? ` where ${this.onde.join(' and ')}` : '', t = `public.${this.tabela}`;
      const valores = (d: Linha) => { const ks = Object.keys(d); return { ks, vs: ks.map((k) => this.p(typeof d[k] === 'object' && d[k] !== null ? JSON.stringify(d[k]) : d[k])) }; };
      if (this.tipo === 'select') return `select ${this.colunas} from ${t}${w}${this.ordem}${this.limite}`;
      if (this.tipo === 'update') { const d = this.dados as Linha; return `update ${t} set ${Object.keys(d).map((k) => `${k} = ${this.p(d[k])}`).join(', ')}${w} returning *`; }
      const linhas = Array.isArray(this.dados) ? this.dados : [this.dados!];
      const ks = Object.keys(linhas[0]!), vals = linhas.map((d) => `(${valores(d).vs.join(', ')})`).join(', ');
      const fim = this.tipo === 'upsert' ? (this.ignorar ? ` on conflict (${this.conflito}) do nothing` : ` on conflict (${this.conflito}) do update set ${ks.map((k) => `${k} = excluded.${k}`).join(', ')}`) : '';
      return `insert into ${t} (${ks.join(', ')}) values ${vals}${fim} returning *`;
    }
    async rodar() {
      try {
        const r = await db.query(this.sql(), this.args);
        const linhas = r.rows.map((x) => ({ ...x, ...(x.seed !== undefined ? { seed: Number(x.seed) } : {}) }));
        if (this.um === 'single') return linhas.length === 1 ? { data: linhas[0], error: null } : { data: null, error: { message: 'não é uma linha' } };
        if (this.um === 'maybe') return { data: linhas[0] ?? null, error: null };
        return { data: linhas, error: null };
      } catch (e) { const x = e as { code?: string; message: string }; return { data: null, error: { code: x.code, message: x.message } }; }
    }
    then<A, B>(ok?: ((v: { data: unknown; error: { code?: string; message: string } | null }) => A | PromiseLike<A>) | null, falha?: ((e: unknown) => B | PromiseLike<B>) | null) { return this.rodar().then(ok, falha); }
  }
  return {
    from: (t: string) => new Consulta(t),
    rpc: async (fn: string, args: Record<string, unknown>) => {
      const ks = Object.keys(args);
      try { const r = await db.query(`select * from public.${fn}(${ks.map((k, i) => `${k} => $${i + 1}`).join(', ')})`, ks.map((k) => args[k])); return { data: r.rows, error: null }; }
      catch (e) { return { data: null, error: e as { message: string } }; }
    },
  };
}

describe.skipIf(!ADMIN)('PvP online: o juiz no servidor, partida inteira', () => {
  let admin: pg.Client, db: pg.Pool, servidor: ReturnType<typeof cliente>;
  beforeAll(async () => {
    admin = new pg.Client({ connectionString: ADMIN }); await admin.connect();
    await admin.query(`create database ${BANCO}`);
    db = new pg.Pool({ connectionString: urlDo(BANCO), max: 8 });
    db.on('error', () => undefined);
    await db.query(sql('tests/sql/supabase-stub.sql'));
    for (const m of migracoes) await db.query(sql(`supabase/migrations/${m}`));
    servidor = cliente(db);
  }, 60000);
  afterAll(async () => {
    await db?.end();
    await admin?.query(`drop database if exists ${BANCO} with (force)`);
    await admin?.end();
  });

  const COLECAO_A = ['goku', 'vegeta', 'gohan', 'naruto', 'sasuke', 'kakashi', 'luffy', 'zoro', 'sanji', 'gojo'];
  const COLECAO_B = ['itachi', 'light', 'pikachu', 'shaka', 'batman', 'superman', 'wonderwoman', 'thor', 'magneto', 'deadpool'];
  let n = 0;
  const conta = async (colecao: string[]) => {
    const id = randomUUID();
    await db.query('insert into auth.users(id) values ($1)', [id]);
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Duelo_${++n}`]);
    for (const c of colecao) await db.query(`insert into public.player_achievements(player_id, achievement_id) values ($1, $2)`, [id, `personagem:${c}`]);
    return id;
  };
  type Vista = { id: string; fase: string; prazo: string; ausencia: number | null; motivo: string | null; rodada: number; resolvida: number; inicioEm: string | null; timesDele: string[][] | null; meusTimes: string[][] | null; minhaEscolha: number | null;
    rodadas: { n: number; meu: number; dele: number; vencedor: 'eu' | 'rival'; rendida?: boolean }[]; vencedor: 'eu' | 'rival' | null; delta: number | null; escolheu: { eu: boolean; rival: boolean } };
  const pede = async (quem: string, input: Record<string, unknown>) => {
    const r = await acaoPvp(servidor as never, quem, input);
    return r as { status: number; body: { partida?: Vista; error?: string; colecao?: string[] } };
  };
  const livres = (v: Vista) => [0, 1, 2].filter((i) => !v.rodadas.some((r) => r.vencedor === 'eu' && r.meu === i));

  it('desafio → aceite → times → rodadas secretas → luta → rating', async () => {
    const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
    const d = await pede(a, { op: 'desafiar', alvo: b });
    expect(d.status).toBe(200);
    const id = d.body.partida!.id;
    expect(d.body.partida!.fase).toBe('convite');
    // um segundo desafio enquanto o primeiro está aberto é recusado
    const c = await conta(COLECAO_A);
    expect((await pede(c, { op: 'desafiar', alvo: b })).status).toBe(409);
    // só o desafiado responde
    expect((await pede(a, { op: 'responder', partida: id, aceitar: true })).status).toBe(409);
    expect((await pede(b, { op: 'responder', partida: id, aceitar: true })).body.partida!.fase).toBe('montando');
    // time com personagem fora da coleção é recusado
    expect((await pede(a, { op: 'times', partida: id, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'itachi']] })).body.error).toMatch(/coleção/);
    const ta = await pede(a, { op: 'times', partida: id, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] });
    // pronto sozinho: os times do outro ainda são segredo
    expect(ta.body.partida!.fase).toBe('montando');
    expect((await pede(b, { op: 'estado', partida: id })).body.partida!.timesDele).toBeNull();
    const tb = await pede(b, { op: 'times', partida: id, times: [['itachi', 'light', 'pikachu'], ['shaka', 'batman', 'superman'], ['wonderwoman', 'thor', 'magneto']] });
    expect(tb.body.partida!.fase).toBe('jogando');
    expect(tb.body.partida!.timesDele).toHaveLength(3);

    // as rodadas, até alguém vencer com os 3 times
    let va = (await pede(a, { op: 'estado', partida: id })).body.partida!;
    for (let rodada = 0; rodada < 5 && va.fase === 'jogando'; rodada++) {
      const vb = (await pede(b, { op: 'estado', partida: id })).body.partida!;
      const escolheuA = await pede(a, { op: 'escolher', partida: id, n: rodada, time: livres(va)[0] });
      // escolheu sozinho: o outro só sabe que ele escolheu, não qual
      if (rodada === 0) { const visto = (await pede(b, { op: 'estado', partida: id })).body.partida!; expect(visto.escolheu.rival).toBe(true); expect(visto.rodadas).toHaveLength(0); }
      expect(escolheuA.status).toBe(200);
      await pede(b, { op: 'escolher', partida: id, n: rodada, time: livres(vb)[livres(vb).length - 1] });
      va = (await pede(a, { op: 'estado', partida: id })).body.partida!;
      expect(va.rodadas).toHaveLength(rodada + 1);
      expect(va.resolvida).toBe(rodada);
      // escolher a próxima antes da luta começar não vale
      if (va.fase === 'jogando') expect((await pede(a, { op: 'escolher', partida: id, n: rodada + 1, time: livres(va)[0] })).status).toBe(409);
      await pede(a, { op: 'lutar', partida: id });
      va = (await pede(b, { op: 'lutar', partida: id })).body.partida! && (await pede(a, { op: 'estado', partida: id })).body.partida!;
      expect(va.inicioEm).not.toBeNull();
      if (va.fase === 'jogando') {
        // o tempo de escolher a próxima só começa quando os dois terminam de assistir a luta (op "assisti")
        expect(new Date(va.prazo).getTime() - Date.now()).toBeGreaterThan(80_000);
        await pede(a, { op: 'assisti', partida: id, n: rodada });
        expect(new Date((await pede(a, { op: 'estado', partida: id })).body.partida!.prazo).getTime()).toBe(new Date(va.prazo).getTime());
        await pede(b, { op: 'assisti', partida: id, n: rodada });
        const falta = new Date((await pede(a, { op: 'estado', partida: id })).body.partida!.prazo).getTime() - Date.now();
        expect(falta).toBeLessThanOrEqual(75_000); expect(falta).toBeGreaterThan(60_000);
      }
    }
    expect(va.fase).toBe('terminada');
    const vb = (await pede(b, { op: 'estado', partida: id })).body.partida!;
    expect([va.vencedor, vb.vencedor].sort()).toEqual(['eu', 'rival']);
    expect(va.delta! + vb.delta!).toBe(0);
    expect(Math.abs(va.delta!)).toBe(16);
    // a luta de cada rodada foi a do motor, com a semente da rodada: a mesma que os dois aparelhos desenham
    const r = await db.query(`select vitorias, derrotas, rating from public.pvp_ratings where player_id = any($1) order by rating desc`, [[a, b]]);
    expect(r.rows.map((x) => x.vitorias + x.derrotas)).toEqual([1, 1]);
    expect(r.rows.map((x) => x.rating)).toEqual([1016, 984]);
    const rk = await pede(a, { op: 'ranking' });
    expect((rk.body as unknown as { ranking: unknown[] }).ranking.length).toBe(2);
  });

  it('quem não escolhe a tempo joga com um time sorteado', async () => {
    const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
    const id = (await pede(a, { op: 'desafiar', alvo: b })).body.partida!.id;
    await pede(b, { op: 'responder', partida: id, aceitar: true });
    await pede(a, { op: 'times', partida: id, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] });
    await pede(b, { op: 'times', partida: id, times: [['itachi', 'light', 'pikachu'], ['shaka', 'batman', 'superman'], ['wonderwoman', 'thor', 'magneto']] });
    await pede(a, { op: 'escolher', partida: id, n: 0, time: 1 });
    await db.query(`update public.pvp_partidas set prazo = now() - interval '1 second' where id = $1`, [id]);
    const v = (await pede(a, { op: 'estado', partida: id })).body.partida!;
    expect(v.rodadas).toHaveLength(1);
    expect(v.rodadas[0]!.meu).toBe(1);
    const auto = await db.query(`select automatica from public.pvp_escolhas where partida_id = $1 and jogador = $2`, [id, b]);
    expect(auto.rows[0].automatica).toBe(true);
  });

  it('desistir dentro da luta perde só aquela rodada; a partida segue', async () => {
    const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
    const id = (await pede(a, { op: 'desafiar', alvo: b })).body.partida!.id;
    await pede(b, { op: 'responder', partida: id, aceitar: true });
    await pede(a, { op: 'times', partida: id, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] });
    await pede(b, { op: 'times', partida: id, times: [['itachi', 'light', 'pikachu'], ['shaka', 'batman', 'superman'], ['wonderwoman', 'thor', 'magneto']] });
    await pede(a, { op: 'escolher', partida: id, n: 0, time: 0 });
    await pede(b, { op: 'escolher', partida: id, n: 0, time: 0 });
    // antes da luta começar não dá para desistir dela
    await pede(a, { op: 'render', partida: id, n: 0 });
    expect((await pede(a, { op: 'estado', partida: id })).body.partida!.rodadas[0]!.rendida).toBe(false);
    await pede(a, { op: 'lutar', partida: id }); await pede(b, { op: 'lutar', partida: id });
    const rendeu = (await pede(a, { op: 'render', partida: id, n: 0 })).body.partida!;
    expect(rendeu.fase).toBe('jogando');
    expect(rendeu.rodadas[0]).toMatchObject({ vencedor: 'rival', rendida: true });
    expect((await pede(b, { op: 'estado', partida: id })).body.partida!.rodadas[0]).toMatchObject({ vencedor: 'eu', rendida: true });
    // a próxima rodada segue normal
    expect((await pede(a, { op: 'escolher', partida: id, n: 1, time: 0 })).status).toBe(200);
  });

  it('quem some da partida: o rival vê há quanto tempo; passou de 45 s, perde', async () => {
    const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
    const id = (await pede(a, { op: 'desafiar', alvo: b })).body.partida!.id;
    await pede(b, { op: 'responder', partida: id, aceitar: true });
    await pede(a, { op: 'times', partida: id, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] });
    await pede(b, { op: 'times', partida: id, times: [['itachi', 'light', 'pikachu'], ['shaka', 'batman', 'superman'], ['wonderwoman', 'thor', 'magneto']] });
    // presente há pouco: não aparece como desconectado
    expect((await pede(a, { op: 'estado', partida: id })).body.partida!.ausencia).toBeNull();
    // b caiu há 20 s: a vê a contagem, a partida segue
    await db.query(`update public.pvp_presenca set visto_em = now() - interval '20 seconds' where partida_id = $1 and jogador = $2`, [id, b]);
    const caiu = (await pede(a, { op: 'estado', partida: id })).body.partida!;
    expect(caiu.fase).toBe('jogando');
    expect(caiu.ausencia).toBeGreaterThanOrEqual(19);
    // voltou: zera
    await pede(b, { op: 'estado', partida: id });
    expect((await pede(a, { op: 'estado', partida: id })).body.partida!.ausencia).toBeNull();
    // sumiu de novo por mais de 45 s: a vence, b perde no rating
    await db.query(`update public.pvp_presenca set visto_em = now() - interval '50 seconds' where partida_id = $1 and jogador = $2`, [id, b]);
    const fim = (await pede(a, { op: 'estado', partida: id })).body.partida!;
    expect(fim).toMatchObject({ fase: 'terminada', vencedor: 'eu', motivo: 'desconectou' });
    expect((await pede(b, { op: 'estado', partida: id })).body.partida!.vencedor).toBe('rival');
  });

  it('convite que ninguém responde expira; desistir no meio dá a vitória ao outro', async () => {
    const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
    const id = (await pede(a, { op: 'desafiar', alvo: b })).body.partida!.id;
    await db.query(`update public.pvp_partidas set prazo = now() - interval '1 second' where id = $1`, [id]);
    expect((await pede(b, { op: 'estado', partida: id })).body.partida!.fase).toBe('expirada');
    const id2 = (await pede(a, { op: 'desafiar', alvo: b })).body.partida!.id;
    await pede(b, { op: 'responder', partida: id2, aceitar: true });
    await pede(a, { op: 'times', partida: id2, times: [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']] });
    await pede(b, { op: 'times', partida: id2, times: [['itachi', 'light', 'pikachu'], ['shaka', 'batman', 'superman'], ['wonderwoman', 'thor', 'magneto']] });
    const fim = (await pede(b, { op: 'desistir', partida: id2 })).body.partida!;
    expect(fim).toMatchObject({ fase: 'terminada', vencedor: 'rival' });
    expect((await pede(a, { op: 'estado', partida: id2 })).body.partida!.vencedor).toBe('eu');
  });

  it('não desafia sem 9 personagens na coleção', async () => {
    const a = await conta(COLECAO_A.slice(0, 5)), b = await conta(COLECAO_B);
    expect((await pede(a, { op: 'desafiar', alvo: b })).body.error).toMatch(/9 personagens/);
  });
});
