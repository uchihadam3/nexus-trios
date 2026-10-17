-- Ranking: uma linha por conta, a melhor (pedido do dono: "mostrar só o maior
-- recorde de cada pessoa"). Cada conta continua guardando até 3 trios em
-- `leaderboard_entries` (a regra da FASE K, que decide o "NOVO TOP 3" depois da
-- jornada), mas a lista mostra só o melhor deles: antes, quem tinha 3 trios
-- bons ocupava 3 lugares (1º, 2º e 3º da mesma pessoa).
--
-- O desempate é o mesmo de antes: maior pontuação; empatou, quem chegou antes;
-- e o id fecha a ordem. A própria conta continua se encontrando fora da página,
-- agora só com a sua melhor linha.
create or replace function public.ranking_pagina(
  p_scope text, p_period text, p_player uuid, p_offset integer default 0, p_limit integer default 50
) returns table (
  posicao bigint, total bigint, player_id uuid, run_id uuid, score integer,
  encounters_cleared smallint, team_ids text[], achieved_at timestamptz
)
language sql stable security definer set search_path = '' as $$
  with melhores as (
    select distinct on (e.player_id) e.*
      from public.leaderboard_entries e
     where e.scope = p_scope and e.period_key = p_period
     order by e.player_id, e.score desc, e.achieved_at asc, e.id
  ), ordenado as (
    select row_number() over (order by m.score desc, m.achieved_at asc, m.id) as posicao,
           count(*) over () as total, m.*
      from melhores m
  )
  select o.posicao, o.total, o.player_id, o.run_id, o.score, o.encounters_cleared, o.team_ids, o.achieved_at
    from ordenado o
   where (o.posicao > greatest(p_offset, 0) and o.posicao <= greatest(p_offset, 0) + least(greatest(p_limit, 1), 100))
      or o.player_id = p_player
   order by o.posicao
$$;

revoke all on function public.ranking_pagina(text, text, uuid, integer, integer) from public, anon, authenticated;
grant execute on function public.ranking_pagina(text, text, uuid, integer, integer) to service_role;
