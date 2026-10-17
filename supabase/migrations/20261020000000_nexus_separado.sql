-- O Caminho do Nexus deixa de mexer no rating do PvP, e ganha o seu próprio ranking (pedido do dono: "separar o rank
-- do Nexus do PvP"). O rating do PvP fica só com as partidas contra pessoas; o Nexus se mede pelas estrelas (0 a 120).

-- 1. Limpa o rating do PvP: tira o que veio das partidas da campanha (a soma das variações e as vitórias e derrotas).
--    Quem só jogou a campanha volta a 1000 com 0V 0D e sai do ranking do PvP (que só mostra quem jogou).
with da_campanha as (
  select player_id, sum(coalesce(delta, 0)) as delta,
         count(*) filter (where vencedor = 'eu') as vitorias, count(*) filter (where vencedor = 'rival') as derrotas
    from public.pvp_campanha_partidas
   where estado = 'terminada'
   group by player_id
)
update public.pvp_ratings r
   set rating = greatest(0, least(5000, r.rating - c.delta)),
       vitorias = greatest(0, r.vitorias - c.vitorias::integer),
       derrotas = greatest(0, r.derrotas - c.derrotas::integer),
       atualizado_em = now()
  from da_campanha c
 where r.player_id = c.player_id;

-- 2. O fim de uma partida da campanha, sem o rating: a partida, as estrelas, o placar e o descanso (o p_delta fica na
--    assinatura para o servidor antigo não quebrar, mas não é usado).
create or replace function public.pvp_campanha_terminar(
  p_partida uuid, p_vencedor text, p_motivo text, p_estrelas smallint, p_delta integer,
  p_descanso jsonb, p_descanso_rival jsonb
) returns table (delta integer, rating integer)
language plpgsql volatile security definer set search_path = '' as $$
declare
  p public.pvp_campanha_partidas;
begin
  select * into p from public.pvp_campanha_partidas where id = p_partida for update;
  if not found then raise exception 'campanha: partida não encontrada' using errcode = '22023'; end if;
  if p.estado = 'terminada' then
    return query select null::integer, null::integer;
    return;
  end if;
  if p_vencedor not in ('eu', 'rival') then raise exception 'campanha: vencedor inválido' using errcode = '22023'; end if;
  update public.pvp_campanha_partidas set estado = 'terminada', vencedor = p_vencedor, motivo = p_motivo,
    estrelas = p_estrelas, rating_antes = null, delta = null, atualizada_em = now() where id = p_partida;
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
  return query select null::integer, null::integer;
end $$;

revoke all on function public.pvp_campanha_terminar(uuid, text, text, smallint, integer, jsonb, jsonb) from public, anon, authenticated;
grant execute on function public.pvp_campanha_terminar(uuid, text, text, smallint, integer, jsonb, jsonb) to service_role;

-- 3. O ranking do Nexus: mais estrelas (cada rival vale até 3); empate, quem jogou menos partidas; depois quem chegou
--    antes. Os primeiros `p_limite` e, onde estiver, a linha de quem pergunta. Só quem já jogou alguma partida.
create function public.pvp_campanha_ranking(p_player uuid, p_limite integer default 50) returns table (
  posicao bigint, total bigint, id uuid, nome text, estrelas integer, partidas integer
)
language sql stable security definer set search_path = '' as $$
  with somadas as (
    select c.player_id, c.partidas, c.atualizado_em,
           (select coalesce(sum(least(3, greatest(0, e.value::int))), 0) from jsonb_each_text(c.estrelas) e)::integer as estrelas
      from public.pvp_campanha c
     where c.partidas > 0
  ), ordenado as (
    select row_number() over (order by s.estrelas desc, s.partidas asc, s.atualizado_em asc, s.player_id) as posicao,
           count(*) over () as total, s.*
      from somadas s
  )
  select o.posicao, o.total, o.player_id, p.handle, o.estrelas, o.partidas
    from ordenado o join public.players p on p.id = o.player_id
   where o.posicao <= least(greatest(p_limite, 1), 200) or o.player_id = p_player
   order by o.posicao
$$;

revoke all on function public.pvp_campanha_ranking(uuid, integer) from public, anon, authenticated;
grant execute on function public.pvp_campanha_ranking(uuid, integer) to service_role;
