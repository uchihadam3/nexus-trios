-- Conquistas: refaz as linhas de player_achievements a partir das jornadas validadas.
-- Cada jornada validada com as 10 lutas terminadas libera os três do trio
-- (`personagem:<id>`, com a data da primeira vez); depois, a linha
-- `conquistas:total` de cada conta guarda quantos ela liberou e quando chegou
-- a esse número, que é o que o ranking de conquistas ordena. Rodar de novo não
-- muda nada: o que já está liberado fica com a data dele.
insert into public.player_achievements(player_id, achievement_id, unlocked_at, progress)
select r.player_id, 'personagem:' || t.id, min(r.finished_at), 1
  from public.ranked_runs r cross join lateral unnest(r.team_ids) as t(id)
 where r.verified and r.encounters_cleared = 10
 group by r.player_id, t.id
on conflict (player_id, achievement_id) do nothing;
insert into public.player_achievements(player_id, achievement_id, unlocked_at, progress)
select player_id, 'conquistas:total', max(unlocked_at), count(*)
  from public.player_achievements where achievement_id like 'personagem:%'
 group by player_id
on conflict (player_id, achievement_id) do update
  set unlocked_at = case when public.player_achievements.progress = excluded.progress then public.player_achievements.unlocked_at else excluded.unlocked_at end,
      progress = excluded.progress;
