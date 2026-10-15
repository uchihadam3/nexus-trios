-- PvP online: desafio, 3 times de 3, escolha secreta a cada rodada, rating (Elo) e ranking.
--
-- Quem joga só LÊ a partida em que está (RLS) e só o que não é segredo: em que etapa ela está, quem já marcou
-- "pronto", quem já escolheu, quando a luta começa. Os times (até os dois ficarem prontos) e a escolha de cada
-- rodada (até os dois escolherem) ficam em tabelas que ninguém lê pelo navegador; quem mostra é a função do
-- servidor (ranked-api, ação "pvp"), que também calcula a luta (o motor do jogo) e o resultado. O rating só muda
-- por pvp_aplicar_resultado, numa transação só.

create table public.pvp_ratings (
  player_id uuid primary key references public.players(id) on delete cascade,
  rating integer not null default 1000 check (rating between 0 and 5000),
  vitorias integer not null default 0 check (vitorias >= 0),
  derrotas integer not null default 0 check (derrotas >= 0),
  atualizado_em timestamptz not null default now()
);

create table public.pvp_partidas (
  id uuid primary key default gen_random_uuid(),
  desafiante uuid not null references public.players(id) on delete cascade,
  desafiado uuid not null references public.players(id) on delete cascade,
  estado text not null default 'convite' check (estado in ('convite', 'montando', 'jogando', 'terminada', 'recusada', 'cancelada', 'expirada')),
  seed bigint not null,
  versao_do_motor text not null,
  pronto_a boolean not null default false,
  pronto_b boolean not null default false,
  -- a rodada da vez (0, 1, 2…) e quem já escolheu o time dela
  rodada smallint not null default 0 check (rodada between 0 and 5),
  escolheu_a boolean not null default false,
  escolheu_b boolean not null default false,
  -- a rodada já resolvida mais recente (trava para só um calcular a luta)
  resolvida smallint not null default -1,
  -- "começar duelo" de cada um, e quando a luta da rodada começa nos dois aparelhos
  lutar_a boolean not null default false,
  lutar_b boolean not null default false,
  inicio_em timestamptz,
  -- cada um terminou de assistir a luta da rodada (o tempo de escolher a próxima só corre depois disso)
  assistiu_a boolean not null default false,
  assistiu_b boolean not null default false,
  -- até quando a etapa de agora espera (convite, montar, escolher, começar)
  prazo timestamptz not null default now() + interval '2 minutes',
  vencedor uuid references public.players(id) on delete set null,
  motivo text,
  rating_a integer, rating_b integer, delta_a integer, delta_b integer,
  criada_em timestamptz not null default now(),
  atualizada_em timestamptz not null default now(),
  constraint pvp_nao_contra_si check (desafiante <> desafiado)
);
create index pvp_partidas_a_idx on public.pvp_partidas(desafiante, criada_em desc);
create index pvp_partidas_b_idx on public.pvp_partidas(desafiado, criada_em desc);
-- uma partida aberta por pessoa de cada vez
create unique index pvp_uma_aberta_a on public.pvp_partidas(desafiante) where estado in ('convite', 'montando', 'jogando');
create unique index pvp_uma_aberta_b on public.pvp_partidas(desafiado) where estado in ('convite', 'montando', 'jogando');

-- os 3 times de cada um (segredo até os dois ficarem prontos)
create table public.pvp_times (
  partida_id uuid not null references public.pvp_partidas(id) on delete cascade,
  jogador uuid not null references public.players(id) on delete cascade,
  times jsonb not null,
  primary key (partida_id, jogador)
);
-- a escolha de cada um em cada rodada (segredo até os dois escolherem)
create table public.pvp_escolhas (
  partida_id uuid not null references public.pvp_partidas(id) on delete cascade,
  n smallint not null,
  jogador uuid not null references public.players(id) on delete cascade,
  time smallint not null check (time between 0 and 2),
  automatica boolean not null default false,
  primary key (partida_id, n, jogador)
);
-- as rodadas resolvidas: os dois times, a semente e quem venceu
create table public.pvp_rodadas (
  partida_id uuid not null references public.pvp_partidas(id) on delete cascade,
  n smallint not null,
  time_a smallint not null check (time_a between 0 and 2),
  time_b smallint not null check (time_b between 0 and 2),
  seed bigint not null,
  vencedor char(1) not null check (vencedor in ('a', 'b')),
  duracao real not null default 0,
  primary key (partida_id, n)
);

alter table public.pvp_ratings enable row level security;
alter table public.pvp_partidas enable row level security;
alter table public.pvp_times enable row level security;
alter table public.pvp_escolhas enable row level security;
alter table public.pvp_rodadas enable row level security;

create policy pvp_ratings_ler on public.pvp_ratings for select to authenticated using (true);
create policy pvp_partidas_ler on public.pvp_partidas for select to authenticated
  using ((select auth.uid()) in (desafiante, desafiado));

revoke all on public.pvp_ratings, public.pvp_partidas, public.pvp_times, public.pvp_escolhas, public.pvp_rodadas from anon, authenticated;
grant select on public.pvp_ratings, public.pvp_partidas to authenticated;

-- O fim da partida: quem venceu, o motivo, e o rating dos dois (Elo, K = 32), numa transação.
-- Devolve a variação de cada um. Só o servidor chama (service_role).
create function public.pvp_aplicar_resultado(p_partida uuid, p_vencedor uuid, p_motivo text)
returns table (delta_a integer, delta_b integer, rating_a integer, rating_b integer)
language plpgsql volatile security definer set search_path = '' as $$
declare
  p public.pvp_partidas;
  ra integer; rb integer; ea double precision; da integer; db integer; venceu_a boolean;
begin
  select * into p from public.pvp_partidas where id = p_partida for update;
  if not found then raise exception 'pvp: partida não encontrada' using errcode = '22023'; end if;
  if p.estado = 'terminada' then
    return query select p.delta_a, p.delta_b, p.rating_a, p.rating_b;
    return;
  end if;
  if p.estado <> 'jogando' or p_vencedor not in (p.desafiante, p.desafiado) then
    raise exception 'pvp: partida não está em jogo' using errcode = '22023';
  end if;
  insert into public.pvp_ratings (player_id) values (p.desafiante), (p.desafiado) on conflict (player_id) do nothing;
  -- trava os dois ratings sempre na mesma ordem (duas partidas terminando juntas não se cruzam)
  perform 1 from public.pvp_ratings where player_id in (p.desafiante, p.desafiado) order by player_id for update;
  select rating into ra from public.pvp_ratings where player_id = p.desafiante;
  select rating into rb from public.pvp_ratings where player_id = p.desafiado;
  venceu_a := p_vencedor = p.desafiante;
  ea := 1 / (1 + power(10, (rb - ra) / 400.0));
  da := round(32 * ((case when venceu_a then 1 else 0 end) - ea));
  db := -da;
  update public.pvp_ratings set rating = greatest(0, rating + da), vitorias = vitorias + (case when venceu_a then 1 else 0 end),
    derrotas = derrotas + (case when venceu_a then 0 else 1 end), atualizado_em = now() where player_id = p.desafiante;
  update public.pvp_ratings set rating = greatest(0, rating + db), vitorias = vitorias + (case when venceu_a then 0 else 1 end),
    derrotas = derrotas + (case when venceu_a then 1 else 0 end), atualizado_em = now() where player_id = p.desafiado;
  update public.pvp_partidas set estado = 'terminada', vencedor = p_vencedor, motivo = p_motivo,
    rating_a = ra, rating_b = rb, delta_a = da, delta_b = db, atualizada_em = now() where id = p_partida;
  return query select da, db, ra, rb;
end $$;

-- O ranking do PvP: maior rating; empate, mais vitórias.
create function public.pvp_ranking(p_limite integer default 50) returns table (
  posicao bigint, id uuid, nome text, rating integer, vitorias integer, derrotas integer
)
language sql stable security definer set search_path = '' as $$
  select row_number() over (order by r.rating desc, r.vitorias desc, p.handle), p.id, p.handle, r.rating, r.vitorias, r.derrotas
  from public.pvp_ratings r join public.players p on p.id = r.player_id
  where r.vitorias + r.derrotas > 0
  order by r.rating desc, r.vitorias desc, p.handle
  limit least(greatest(p_limite, 1), 200)
$$;

revoke all on function public.pvp_aplicar_resultado(uuid, uuid, text), public.pvp_ranking(integer) from public, anon, authenticated;
grant execute on function public.pvp_aplicar_resultado(uuid, uuid, text) to service_role;
grant execute on function public.pvp_ranking(integer) to authenticated, service_role;

-- O convite, a etapa e o "pronto" de cada um chegam na hora (Realtime), só para os dois da partida (RLS acima).
do $$ begin
  if exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    alter publication supabase_realtime add table public.pvp_partidas;
  end if;
end $$;
