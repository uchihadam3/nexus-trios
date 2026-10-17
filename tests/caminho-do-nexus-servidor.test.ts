/*
 * O juiz do Caminho do Nexus (supabase/functions/ranked-api/campanha.ts) contra um Postgres de verdade: o rival
 * bloqueado, a partida inteira com as sementes escondidas até a rodada acontecer, a mesma luta que o aparelho desenha,
 * as estrelas, o rating (80%/120%, nada 400 acima), o rodízio dos dois lados, o abandono e a versão do jogo.
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';
import { acaoCampanha } from '../supabase/functions/ranked-api/campanha';
import { RIVAIS, escalaDoRival, estrelasDaPartida, lutaDaRodada } from '../src/engine/campanha';
import { variacaoContraNpc } from '../src/engine/pvp';
import { ENGINE_VERSION } from '../src/engine/ranked';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_campanha_${Date.now()}`;
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
      if (this.tipo === 'update') { const d = this.dados as Linha; return `update ${t} set ${Object.keys(d).map((k) => `${k} = ${this.p(typeof d[k] === 'object' && d[k] !== null ? JSON.stringify(d[k]) : d[k])}`).join(', ')}${w} returning *`; }
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

interface Vista { id: string; estado: string; rival: string; meus: string[][]; deles: string[][]; rodadas: { meu: number; dele: number; seed: number; vencedor: 'eu' | 'rival'; rendida?: boolean }[];
  vencedor: string | null; estrelas: number | null; delta: number | null; ratingAntes: number | null }
interface Resp { progresso: { estrelas: Record<string, number>; placar: Record<string, { v: number; d: number }>; descanso: Record<string, number>; descanso_rivais: Record<string, Record<string, number>>; partidas: number };
  rating: { rating: number }; colecao: string[]; partida: Vista | null; error?: string }

describe.skipIf(!ADMIN)('Caminho do Nexus: o juiz no servidor', () => {
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

  const COLECAO = ['goku', 'vegeta', 'gohan', 'naruto', 'sasuke', 'kakashi', 'luffy', 'zoro', 'sanji', 'gojo', 'itachi', 'light', 'pikachu', 'shaka'];
  let n = 0;
  const conta = async (colecao = COLECAO) => {
    const id = randomUUID();
    await db.query('insert into auth.users(id) values ($1)', [id]);
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Camp_${++n}`]);
    for (const c of colecao) await db.query(`insert into public.player_achievements(player_id, achievement_id) values ($1, $2)`, [id, `personagem:${c}`]);
    return id;
  };
  const pede = async (quem: string, input: Record<string, unknown>) => {
    const r = await acaoCampanha(servidor as never, quem, input);
    return { status: r.status, ...(r.body as Resp) };
  };
  /** Joga a partida até o fim escolhendo sempre o primeiro time livre. */
  const joga = async (quem: string, partida: Vista) => {
    let p = partida;
    while (p.estado === 'jogando') {
      const ganhos = new Set(p.rodadas.filter((x) => x.vencedor === 'eu').map((x) => x.meu));
      const time = [0, 1, 2].find((i) => !ganhos.has(i))!;
      const r = await pede(quem, { op: 'escolher', partida: p.id, n: p.rodadas.length, time });
      expect(r.status).toBe(200);
      expect(r.partida!.rodadas.length).toBe(p.rodadas.length + 1);
      p = r.partida!;
    }
    return p;
  };
  const TIMES = [['goku', 'vegeta', 'gohan'], ['naruto', 'sasuke', 'kakashi'], ['luffy', 'zoro', 'sanji']];

  it('começa só com o primeiro rival; a versão velha do jogo não entra; a coleção pequena não entra', async () => {
    const eu = await conta();
    const r0 = await pede(eu, { op: 'estado' });
    expect(r0.partida).toBeNull();
    expect(r0.progresso.estrelas).toEqual({});
    expect((await pede(eu, { op: 'comecar', rival: RIVAIS[1]!.id, times: TIMES, versao: ENGINE_VERSION })).status).toBe(403);
    expect((await pede(eu, { op: 'comecar', rival: RIVAIS[0]!.id, times: TIMES, versao: 'nexus-velha' })).status).toBe(409);
    const pouca = await conta(COLECAO.slice(0, 10));
    expect((await pede(pouca, { op: 'comecar', rival: RIVAIS[0]!.id, times: TIMES, versao: ENGINE_VERSION })).status).toBe(422);
    expect((await pede(eu, { op: 'comecar', rival: RIVAIS[0]!.id, times: [['goku', 'vegeta', 'superman'], TIMES[1], TIMES[2]], versao: ENGINE_VERSION })).status).toBe(422);
  });

  it('uma partida inteira: a mesma luta do aparelho, estrelas, rating e o rodízio dos dois lados', async () => {
    const eu = await conta();
    const c = await pede(eu, { op: 'comecar', rival: 'zepipoca', times: TIMES, versao: ENGINE_VERSION });
    expect(c.status).toBe(200);
    const p0 = c.partida!;
    expect(p0.rodadas).toEqual([]);
    expect(p0.deles.flat()).toHaveLength(9);
    expect(JSON.stringify(c)).not.toMatch(/sementes|sorteios/);
    // uma partida aberta de cada vez
    expect((await pede(eu, { op: 'comecar', rival: 'zepipoca', times: TIMES, versao: ENGINE_VERSION })).status).toBe(409);
    // a mesma rodada pedida duas vezes não é calculada duas vezes
    const r1 = await pede(eu, { op: 'escolher', partida: p0.id, n: 0, time: 0 });
    const r1b = await pede(eu, { op: 'escolher', partida: p0.id, n: 0, time: 1 });
    expect(r1b.partida!.rodadas).toEqual(r1.partida!.rodadas);
    const fim = await joga(eu, r1.partida!);
    const rival = RIVAIS[0]!;
    // cada rodada é a luta que o aparelho desenha com a semente que veio
    for (const x of fim.rodadas) expect(lutaDaRodada(fim.meus[x.meu]!, fim.deles[x.dele]!, x.seed, escalaDoRival(rival)).winner === 'player' ? 'eu' : 'rival').toBe(x.vencedor);
    const final = await pede(eu, { op: 'estado' });
    expect(final.partida).toBeNull();
    const ganhou = fim.vencedor === 'eu';
    expect(fim.estrelas).toBe(ganhou ? estrelasDaPartida(fim) : 0);
    expect(fim.delta).toBe(variacaoContraNpc(1000, rival.rating, ganhou));
    expect(final.rating.rating).toBe(1000 + fim.delta!);
    expect(final.progresso.estrelas.zepipoca ?? 0).toBe(fim.estrelas);
    expect(final.progresso.placar.zepipoca).toEqual(ganhou ? { v: 1, d: 0 } : { v: 0, d: 1 });
    // o rodízio: 2 seus (dormem 2 por partida) e 3 do rival descansam 3 partidas
    expect(Object.values(final.progresso.descanso)).toEqual([3, 3]);
    expect(Object.values(final.progresso.descanso_rivais.zepipoca!)).toEqual([3, 3, 3]);
    // quem descansa não entra no time
    const cansado = Object.keys(final.progresso.descanso)[0]!;
    const comCansado = [TIMES[0]!.includes(cansado) ? TIMES[0]! : TIMES.find((t) => t.includes(cansado))!, ...TIMES.filter((t) => !t.includes(cansado))];
    const r = await pede(eu, { op: 'comecar', rival: 'zepipoca', times: comCansado, versao: ENGINE_VERSION });
    expect(r.status).toBe(422);
    expect(r.error).toMatch(/descansando/);
  });

  it('abandonar conta como derrota e mexe no rating; vencer libera o próximo', async () => {
    const eu = await conta();
    const c = await pede(eu, { op: 'comecar', rival: 'zepipoca', times: TIMES, versao: ENGINE_VERSION });
    const a = await pede(eu, { op: 'abandonar', partida: c.partida!.id });
    expect(a.partida!.vencedor).toBe('rival');
    expect(a.partida!.delta).toBe(variacaoContraNpc(1000, 600, false));
    expect(a.progresso.placar.zepipoca).toEqual({ v: 0, d: 1 });
    // com a estrela do primeiro, o segundo abre
    await db.query(`update public.pvp_campanha set estrelas = '{"zepipoca": 2}'::jsonb, descanso = '{}'::jsonb where player_id = $1`, [eu]);
    const s = await pede(eu, { op: 'comecar', rival: RIVAIS[1]!.id, times: TIMES, versao: ENGINE_VERSION });
    expect(s.status).toBe(200);
    expect(s.partida!.rival).toBe(RIVAIS[1]!.id);
  });

  it('a melhor estrela fica: uma vitória pior não apaga o recorde', async () => {
    const eu = await conta();
    await db.query(`insert into public.pvp_campanha (player_id, estrelas) values ($1, '{"zepipoca": 3}'::jsonb)`, [eu]);
    const c = await pede(eu, { op: 'comecar', rival: 'zepipoca', times: TIMES, versao: ENGINE_VERSION });
    const fim = await joga(eu, c.partida!);
    const r = await pede(eu, { op: 'estado' });
    expect(r.progresso.estrelas.zepipoca).toBe(3);
    expect(fim.estado).toBe('terminada');
  });
});
