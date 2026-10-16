-- O Caminho do Nexus (a campanha do PvP contra 40 rivais) e duas regras novas do rating.
--
-- Tudo da campanha é da função do servidor (ranked-api, ação "campanha"): ninguém lê nem escreve pelo navegador.
-- As sementes das lutas e da escolha do rival são sorteadas no começo da partida e ficam só aqui (quem sabe a
-- semente sabe o resultado). O rating muda por pvp_campanha_terminar, numa transação só com o progresso.

-- o progresso de cada jogador: as melhores estrelas contra cada rival e quem está descansando (o rodízio)
create table public.pvp_campanha (
  player_id uuid primary key references public.players(id) on delete cascade,
  estrelas jsonb not null default '{}'::jsonb,
  placar jsonb not null default '{}'::jsonb,
  descanso jsonb not null default '{}'::jsonb,
  descanso_rivais jsonb not null default '{}'::jsonb,
  partidas integer not null default 0 check (partidas >= 0),
  atualizado_em timestamptz not null default now()
);

create table public.pvp_campanha_partidas (
  id uuid primary key default gen_random_uuid(),
  player_id uuid not null references public.players(id) on delete cascade,
  rival text not null,
  rival_rating integer not null,
  estado text not null default 'jogando' check (estado in ('jogando', 'terminada')),
  versao_do_motor text not null,
  -- segredo: a semente de cada luta e o sorteio da escolha do rival em cada rodada
  sementes jsonb not null,
  sorteios jsonb not null,
  meus jsonb not null,
  deles jsonb not null,
  rodadas jsonb not null default '[]'::jsonb,
  -- quantas rodadas já foram (trava para a mesma rodada não ser calculada duas vezes)
  n_rodadas smallint not null default 0 check (n_rodadas between 0 and 5),
  vencedor text check (vencedor in ('eu', 'rival')),
  motivo text,
  estrelas smallint,
  rating_antes integer,
  delta integer,
  criada_em timestamptz not null default now(),
  atualizada_em timestamptz not null default now()
);
create index pvp_campanha_partidas_idx on public.pvp_campanha_partidas(player_id, criada_em desc);
create index pvp_campanha_partidas_rival_idx on public.pvp_campanha_partidas(player_id, rival, criada_em desc);
-- uma partida aberta da campanha por pessoa de cada vez
create unique index pvp_campanha_uma_aberta on public.pvp_campanha_partidas(player_id) where estado = 'jogando';

alter table public.pvp_campanha enable row level security;
alter table public.pvp_campanha_partidas enable row level security;
revoke all on public.pvp_campanha, public.pvp_campanha_partidas from anon, authenticated;
grant all on public.pvp_campanha, public.pvp_campanha_partidas to service_role;

-- O fim de uma partida da campanha, numa transação: a partida, o rating (a variação já vem calculada pelo servidor:
-- 80% do ganho e 120% da perda do Elo, nada para quem está 400 acima) e o progresso (estrelas, placar e descanso).
create function public.pvp_campanha_terminar(
  p_partida uuid, p_vencedor text, p_motivo text, p_estrelas smallint, p_delta integer,
  p_descanso jsonb, p_descanso_rival jsonb
) returns table (delta integer, rating integer)
language plpgsql volatile security definer set search_path = '' as $$
declare
  p public.pvp_campanha_partidas;
  r integer;
begin
  select * into p from public.pvp_campanha_partidas where id = p_partida for update;
  if not found then raise exception 'campanha: partida não encontrada' using errcode = '22023'; end if;
  if p.estado = 'terminada' then
    return query select p.delta, (select x.rating from public.pvp_ratings x where x.player_id = p.player_id);
    return;
  end if;
  if p_vencedor not in ('eu', 'rival') then raise exception 'campanha: vencedor inválido' using errcode = '22023'; end if;
  insert into public.pvp_ratings (player_id) values (p.player_id) on conflict (player_id) do nothing;
  select x.rating into r from public.pvp_ratings x where x.player_id = p.player_id for update;
  update public.pvp_ratings set rating = greatest(0, least(5000, public.pvp_ratings.rating + p_delta)),
    vitorias = vitorias + (case when p_vencedor = 'eu' then 1 else 0 end),
    derrotas = derrotas + (case when p_vencedor = 'eu' then 0 else 1 end), atualizado_em = now()
    where player_id = p.player_id;
  update public.pvp_campanha_partidas set estado = 'terminada', vencedor = p_vencedor, motivo = p_motivo,
    estrelas = p_estrelas, rating_antes = r, delta = p_delta, atualizada_em = now() where id = p_partida;
  insert into public.pvp_campanha (player_id) values (p.player_id) on conflict (player_id) do nothing;
  update public.pvp_campanha c set
    estrelas = case when p_estrelas > coalesce((c.estrelas ->> p.rival)::int, 0)
      then c.estrelas || jsonb_build_object(p.rival, p_estrelas) else c.estrelas end,
    placar = c.placar || jsonb_build_object(p.rival, jsonb_build_object(
      'v', coalesce((c.placar -> p.rival ->> 'v')::int, 0) + (case when p_vencedor = 'eu' then 1 else 0 end),
      'd', coalesce((c.placar -> p.rival ->> 'd')::int, 0) + (case when p_vencedor = 'eu' then 0 else 1 end))),
    descanso = coalesce(p_descanso, '{}'::jsonb),
    descanso_rivais = c.descanso_rivais || jsonb_build_object(p.rival, coalesce(p_descanso_rival, '{}'::jsonb)),
    partidas = c.partidas + 1, atualizado_em = now()
    where c.player_id = p.player_id;
  return query select p_delta, greatest(0, least(5000, r + p_delta));
end $$;

revoke all on function public.pvp_campanha_terminar(uuid, text, text, smallint, integer, jsonb, jsonb) from public, anon, authenticated;
grant execute on function public.pvp_campanha_terminar(uuid, text, text, smallint, integer, jsonb, jsonb) to service_role;

-- Contra pessoas também (pedido do jogador): quem está 400 ou mais acima não ganha nada vencendo; quem perde perde
-- o de sempre. O resto da função é o mesmo de 20261016000000_pvp.sql.
create or replace function public.pvp_aplicar_resultado(p_partida uuid, p_vencedor uuid, p_motivo text)
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
  perform 1 from public.pvp_ratings where player_id in (p.desafiante, p.desafiado) order by player_id for update;
  select rating into ra from public.pvp_ratings where player_id = p.desafiante;
  select rating into rb from public.pvp_ratings where player_id = p.desafiado;
  venceu_a := p_vencedor = p.desafiante;
  ea := 1 / (1 + power(10, (rb - ra) / 400.0));
  da := round(32 * ((case when venceu_a then 1 else 0 end) - ea));
  db := -da;
  -- 400 ou mais acima: o vencedor não ganha nada
  if venceu_a and ra - rb >= 400 then da := 0; end if;
  if not venceu_a and rb - ra >= 400 then db := 0; end if;
  update public.pvp_ratings set rating = greatest(0, rating + da), vitorias = vitorias + (case when venceu_a then 1 else 0 end),
    derrotas = derrotas + (case when venceu_a then 0 else 1 end), atualizado_em = now() where player_id = p.desafiante;
  update public.pvp_ratings set rating = greatest(0, rating + db), vitorias = vitorias + (case when venceu_a then 0 else 1 end),
    derrotas = derrotas + (case when venceu_a then 1 else 0 end), atualizado_em = now() where player_id = p.desafiado;
  update public.pvp_partidas set estado = 'terminada', vencedor = p_vencedor, motivo = p_motivo,
    rating_a = ra, rating_b = rb, delta_a = da, delta_b = db, atualizada_em = now() where id = p_partida;
  return query select da, db, ra, rb;
end $$;
