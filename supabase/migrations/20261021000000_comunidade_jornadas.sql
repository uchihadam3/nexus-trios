-- O cartão do jogador na Comunidade mostra quantas jornadas a pessoa já fez
-- (pedido do dono: "pra você saber quanto que a pessoa jogou"). Conta as
-- jornadas que chegaram ao fim no servidor, desistências incluídas; as
-- abertas e abandonadas sem fim não contam.
drop function public.comunidade_jogadores();
create function public.comunidade_jogadores() returns table (
  id uuid, nome text, online boolean, online_desde timestamptz, visto_em timestamptz,
  recorde integer, trio text[], conquistas integer, desde timestamptz, jornadas integer
)
language sql stable security definer set search_path = '' as $$
  select p.id, p.handle,
    coalesce(c.online and c.visto_em > now() - interval '75 seconds', false),
    c.online_desde, c.visto_em,
    r.score, r.team_ids,
    (select count(*)::int from public.player_achievements a where a.player_id = p.id and a.achievement_id like 'personagem:%'),
    p.created_at,
    (select count(*)::int from public.ranked_runs j where j.player_id = p.id and j.verified)
  from public.players p
  left join public.comunidade_presenca c on c.player_id = p.id
  left join lateral (
    select e.score, e.team_ids from public.leaderboard_entries e
    where e.player_id = p.id and e.scope = 'season'
    order by e.score desc, e.achieved_at asc limit 1
  ) r on true
  where public.comunidade_eu() is not null
  order by 3 desc, c.visto_em desc nulls last, p.handle
$$;
revoke all on function public.comunidade_jogadores() from public, anon;
grant execute on function public.comunidade_jogadores() to authenticated;
