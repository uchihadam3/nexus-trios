/*
 * PvP online: a sincronia das lutas, rodada após rodada (pedido do jogador: "só funcionou o primeiro duelo; a partir
 * do segundo a luta já começou e já acabou"). Partidas inteiras entre dois jogadores, com consultas de estado
 * disparadas ao mesmo tempo que cada escolha (como os aparelhos perguntam a cada 3 s e a cada aviso do Realtime).
 * Em toda resposta, o começo da luta (inicioEm) tem de ser da rodada que acabou de ser resolvida, e cada luta só
 * começa depois que os dois estão vendo a tela, com a contagem inteira pela frente.
 *
 * Precisa de um Postgres: NEXUS_PG_URL=postgres://usuario@host:porta/postgres. PVP_ESTRESSE=n joga n partidas
 * (padrão 12).
 */
import { readFileSync, readdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import pg from 'pg';
import { acaoPvp } from '../supabase/functions/ranked-api/pvp';

const ADMIN = process.env.NEXUS_PG_URL;
const BANCO = `nexus_pvpsinc_${Date.now()}`;
const PARTIDAS = Number(process.env.PVP_ESTRESSE ?? 12);
/* atraso de cada consulta (ms, sorteado): como a rede e o banco de verdade, para as perguntas caírem no meio do cálculo */
const JITTER = 12;
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
        await new Promise((ok) => setTimeout(ok, Math.random() * JITTER));
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

interface Vista { id: string; fase: string; rodada: number; resolvida: number; inicioEm: string | null; rodadas: { n: number; meu: number; vencedor: 'eu' | 'rival' }[]; vencedor: string | null }

describe.skipIf(!ADMIN)('PvP online: a luta de cada rodada começa junto nos dois aparelhos', () => {
  let admin: pg.Client, db: pg.Pool, servidor: ReturnType<typeof cliente>;
  beforeAll(async () => {
    admin = new pg.Client({ connectionString: ADMIN }); await admin.connect();
    await admin.query(`create database ${BANCO}`);
    db = new pg.Pool({ connectionString: urlDo(BANCO), max: 16 });
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

  const COLECAO_A = ['goku', 'vegeta', 'gohan', 'naruto', 'sasuke', 'kakashi', 'luffy', 'zoro', 'sanji'];
  const COLECAO_B = ['itachi', 'light', 'pikachu', 'shaka', 'batman', 'superman', 'wonderwoman', 'thor', 'magneto'];
  let k = 0;
  const conta = async (colecao: string[]) => {
    const id = randomUUID();
    await db.query('insert into auth.users(id) values ($1)', [id]);
    await db.query('insert into public.players(id, handle) values ($1, $2)', [id, `Sinc_${++k}`]);
    for (const c of colecao) await db.query(`insert into public.player_achievements(player_id, achievement_id) values ($1, $2)`, [id, `personagem:${c}`]);
    return id;
  };
  const pede = async (quem: string, input: Record<string, unknown>) => {
    const r = await acaoPvp(servidor as never, quem, input);
    return r.body as { partida?: Vista; error?: string };
  };
  const livres = (v: Vista) => [0, 1, 2].filter((i) => !v.rodadas.some((r) => r.vencedor === 'eu' && r.meu === i));

  it(`${PARTIDAS} partidas inteiras, com perguntas no meio de cada escolha`, async () => {
    const problemas: string[] = [];
    let rodadasJogadas = 0;
    for (let jogo = 0; jogo < PARTIDAS; jogo++) {
      const a = await conta(COLECAO_A), b = await conta(COLECAO_B);
      const id = (await pede(a, { op: 'desafiar', alvo: b })).partida!.id;
      await pede(b, { op: 'responder', partida: id, aceitar: true });
      await pede(a, { op: 'times', partida: id, times: [COLECAO_A.slice(0, 3), COLECAO_A.slice(3, 6), COLECAO_A.slice(6, 9)] });
      await pede(b, { op: 'times', partida: id, times: [COLECAO_B.slice(0, 3), COLECAO_B.slice(3, 6), COLECAO_B.slice(6, 9)] });
      const resolvidaEm: number[] = [];
      let inicioAnterior: string | null = null;
      for (let n = 0; n < 6; n++) {
        const va = (await pede(a, { op: 'estado', partida: id })).partida!, vb = (await pede(b, { op: 'estado', partida: id })).partida!;
        if (va.fase !== 'jogando') break;
        // os dois escolhem em ordem sorteada; a segunda escolha resolve a rodada enquanto os dois aparelhos perguntam
        const [primeiro, segundo] = Math.random() < 0.5 ? [[a, va], [b, vb]] as const : [[b, vb], [a, va]] as const;
        await pede(primeiro[0], { op: 'escolher', partida: id, n, time: livres(primeiro[1])[0] });
        resolvidaEm[n] = Date.now();
        // enquanto a segunda escolha é calculada, os dois aparelhos não param de perguntar (o aviso do Realtime chega
        // no meio do cálculo e cada aparelho pergunta na hora)
        let calculando = true;
        const vistas: { partida?: Vista }[] = [];
        const escolha = pede(segundo[0], { op: 'escolher', partida: id, n, time: livres(segundo[1])[0] }).then((r) => { calculando = false; vistas.push(r); });
        const perguntam = async (quem: string) => { while (calculando) vistas.push(await pede(quem, { op: 'estado', partida: id })); };
        await Promise.all([escolha, perguntam(a), perguntam(b), perguntam(a), perguntam(b)]);
        for (const r of vistas) {
          const v = r.partida;
          if (!v?.inicioEm) continue;
          // o começo mostrado tem de ser da rodada resolvida que ele acompanha (nunca o da luta anterior)
          const desde = resolvidaEm[v.resolvida];
          if (desde === undefined || Date.parse(v.inicioEm) < desde || (v.resolvida === n && inicioAnterior !== null && String(v.inicioEm) === String(inicioAnterior))) problemas.push(`partida ${jogo} rodada ${n}: inicioEm ${v.inicioEm} velho para a rodada ${v.resolvida}`);
        }
        // antes dos dois estarem vendo a tela, a luta não começa
        const antes = (await pede(a, { op: 'estado', partida: id })).partida!;
        if (antes.resolvida === n && antes.inicioEm) problemas.push(`partida ${jogo} rodada ${n}: começou sem os dois vendo`);
        await pede(a, { op: 'lutar', partida: id });
        const meio = (await pede(b, { op: 'estado', partida: id })).partida!;
        if (meio.inicioEm) problemas.push(`partida ${jogo} rodada ${n}: começou com um só vendo`);
        const [, depois] = await Promise.all([pede(b, { op: 'lutar', partida: id }), pede(a, { op: 'estado', partida: id })]);
        const ja = (await pede(b, { op: 'estado', partida: id })).partida!;
        if (!ja.inicioEm) problemas.push(`partida ${jogo} rodada ${n}: não começou com os dois vendo`);
        else if (Date.parse(ja.inicioEm) - Date.now() < 3000) problemas.push(`partida ${jogo} rodada ${n}: a contagem já tinha passado (${Date.parse(ja.inicioEm) - Date.now()} ms)`);
        if (depois.partida?.inicioEm && Date.parse(depois.partida.inicioEm) < resolvidaEm[n]!) problemas.push(`partida ${jogo} rodada ${n}: começo velho logo depois do lutar`);
        inicioAnterior = ja.inicioEm;
        rodadasJogadas++;
        // os dois assistem a luta inteira (no teste, sem esperar: o servidor só registra)
        await Promise.all([pede(a, { op: 'assisti', partida: id, n }), pede(b, { op: 'assisti', partida: id, n })]);
      }
      const fim = (await pede(a, { op: 'estado', partida: id })).partida!;
      if (fim.fase !== 'terminada') problemas.push(`partida ${jogo}: não terminou (${fim.fase}, rodada ${fim.rodada})`);
    }
    expect(problemas).toEqual([]);
    expect(rodadasJogadas).toBeGreaterThanOrEqual(PARTIDAS * 3);
  }, Math.max(600000, PARTIDAS * 5000));
});
