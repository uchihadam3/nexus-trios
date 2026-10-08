-- FASE L · ranking paginado, com a posição calculada no banco.
--
-- A função `ranked-api` buscava até 1.000 entradas a cada consulta e numerava
-- as posições em JavaScript: caro com muitos jogadores, e quem estivesse
-- depois da milésima linha nunca aparecia — nem para si mesmo.
--
-- Esta função devolve só a página pedida mais as entradas da própria conta,
-- onde quer que estejam, cada uma com a posição exata e o total do ranking.
-- O desempate segue o resto do jogo: maior pontuação primeiro; empatou, quem
-- chegou antes; e o id fecha a ordem, para a posição nunca oscilar entre duas
-- consultas.
create function public.ranking_pagina(
  p_scope text, p_period text, p_player uuid, p_offset integer default 0, p_limit integer default 50
) returns table (
  posicao bigint, total bigint, player_id uuid, run_id uuid, score integer,
  encounters_cleared smallint, team_ids text[], achieved_at timestamptz
)
language sql stable security definer set search_path = '' as $$
  with ordenado as (
    select row_number() over (order by e.score desc, e.achieved_at asc, e.id) as posicao,
           count(*) over () as total, e.*
      from public.leaderboard_entries e
     where e.scope = p_scope and e.period_key = p_period
  )
  select o.posicao, o.total, o.player_id, o.run_id, o.score, o.encounters_cleared, o.team_ids, o.achieved_at
    from ordenado o
   where (o.posicao > greatest(p_offset, 0) and o.posicao <= greatest(p_offset, 0) + least(greatest(p_limit, 1), 100))
      or o.player_id = p_player
   order by o.posicao
$$;

revoke all on function public.ranking_pagina(text, text, uuid, integer, integer) from public, anon, authenticated;
grant execute on function public.ranking_pagina(text, text, uuid, integer, integer) to service_role;
