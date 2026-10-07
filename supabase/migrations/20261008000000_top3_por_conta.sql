-- FASE K · até 3 trios diferentes por conta, em cada ranking.
--
-- Antes, o ranking guardava só a melhor partida de cada conta. A regra do
-- documento é outra: cada conta pode ter até 3 entradas ativas em cada ranking
-- (Hoje, Semana, Temporada), e as 3 precisam ser de trios diferentes. Trio é o
-- conjunto dos 3 ids — a ordem não cria trio novo.
--
-- Toda escrita passa por `registrar_no_top3`, que roda dentro da transação da
-- Edge Function. "Duas submissões simultâneas nunca podem criar 4 slots": cada
-- (conta, ranking, período) tem uma trava própria, e quem chega segundo espera
-- o primeiro terminar antes de contar quantas vagas restam. O gatilho
-- `top3_guarda` repete a trava e a contagem em qualquer INSERT, para que nem um
-- caminho futuro que esqueça a função consiga abrir uma quarta vaga.

create function public.trio_canonico(ids text[]) returns text
language sql immutable strict set search_path = '' as
$$ select string_agg(x, '|' order by x) from unnest(ids) as x $$;

create table public.leaderboard_entries (
  id uuid primary key default gen_random_uuid(),
  player_id uuid not null references public.players(id) on delete cascade,
  scope text not null check (scope in ('daily','weekly','season')),
  period_key text not null check (char_length(period_key) between 1 and 32),
  canonical_team text not null,
  team_ids text[] not null check (cardinality(team_ids) = 3),
  run_id uuid not null references public.ranked_runs(id) on delete cascade,
  score integer not null check (score between 0 and 10999999),
  encounters_cleared smallint not null check (encounters_cleared between 0 and 10),
  achieved_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint trio_coerente check (canonical_team = public.trio_canonico(team_ids)),
  unique (player_id, scope, period_key, canonical_team)
);
create index leaderboard_entries_board_idx on public.leaderboard_entries(scope, period_key, score desc, achieved_at asc);
create index leaderboard_entries_player_idx on public.leaderboard_entries(player_id, scope, period_key);

-- A trava de uma conta num ranking. Transacional: solta sozinha no fim.
create function public.top3_travar(p_player uuid, p_scope text, p_period text) returns void
language sql volatile set search_path = '' as
$$ select pg_advisory_xact_lock(hashtextextended(p_player::text || ':' || p_scope || ':' || p_period, 0)) $$;

create function public.top3_guarda() returns trigger
language plpgsql set search_path = '' as $$
begin
  perform public.top3_travar(new.player_id, new.scope, new.period_key);
  if (select count(*) from public.leaderboard_entries
      where player_id = new.player_id and scope = new.scope and period_key = new.period_key) >= 3 then
    raise exception 'top3: esta conta já tem 3 trios neste ranking' using errcode = '23514';
  end if;
  return new;
end $$;
create trigger top3_guarda before insert on public.leaderboard_entries
  for each row execute function public.top3_guarda();

-- Registra uma partida verificada num ranking e devolve o que aconteceu,
-- nas palavras que a tela precisa:
--   novo      — trio novo, havia vaga;
--   melhorou  — mesmo trio, pontuação maior: a mesma entrada sobe;
--   manteve   — mesmo trio, pontuação igual ou menor: o recorde fica;
--   entrou    — trio novo, sem vaga, superou o pior: o pior sai;
--   fora      — trio novo, sem vaga, não superou o pior.
-- `precisa_superar` é o que a próxima entrada precisa bater; `vagas`, quantas
-- sobram. Empate não entra: "Para entrar: supere 1.300".
create function public.registrar_no_top3(
  p_player uuid, p_scope text, p_period text, p_team text[],
  p_run uuid, p_score integer, p_cleared smallint, p_quando timestamptz default now()
) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare
  v_trio text;
  v_mesmo public.leaderboard_entries;
  v_pior public.leaderboard_entries;
  v_ativas integer;
  v_situacao text;
  v_extra jsonb := '{}'::jsonb;
begin
  if p_team is null or cardinality(p_team) <> 3
     or (select count(distinct x) from unnest(p_team) as x) <> 3 then
    raise exception 'top3: trio inválido' using errcode = '22023';
  end if;
  v_trio := public.trio_canonico(p_team);
  perform public.top3_travar(p_player, p_scope, p_period);

  select * into v_mesmo from public.leaderboard_entries
   where player_id = p_player and scope = p_scope and period_key = p_period and canonical_team = v_trio;

  if found then
    if p_score > v_mesmo.score then
      update public.leaderboard_entries
         set score = p_score, run_id = p_run, encounters_cleared = p_cleared, team_ids = p_team,
             achieved_at = p_quando, updated_at = now()
       where id = v_mesmo.id;
      v_situacao := 'melhorou'; v_extra := jsonb_build_object('anterior', v_mesmo.score);
    else
      v_situacao := 'manteve'; v_extra := jsonb_build_object('recorde', v_mesmo.score);
    end if;
  else
    select count(*) into v_ativas from public.leaderboard_entries
     where player_id = p_player and scope = p_scope and period_key = p_period;
    if v_ativas < 3 then
      insert into public.leaderboard_entries(player_id, scope, period_key, canonical_team, team_ids, run_id, score, encounters_cleared, achieved_at)
      values (p_player, p_scope, p_period, v_trio, p_team, p_run, p_score, p_cleared, p_quando);
      v_situacao := 'novo';
    else
      -- O pior: menor pontuação; no empate, o mais recente sai — quem chegou
      -- antes fica na frente no ranking, e fica também aqui.
      select * into v_pior from public.leaderboard_entries
       where player_id = p_player and scope = p_scope and period_key = p_period
       order by score asc, achieved_at desc limit 1;
      if p_score > v_pior.score then
        delete from public.leaderboard_entries where id = v_pior.id;
        insert into public.leaderboard_entries(player_id, scope, period_key, canonical_team, team_ids, run_id, score, encounters_cleared, achieved_at)
        values (p_player, p_scope, p_period, v_trio, p_team, p_run, p_score, p_cleared, p_quando);
        v_situacao := 'entrou';
        v_extra := jsonb_build_object('removido', v_pior.score, 'removido_trio', v_pior.team_ids);
      else
        v_situacao := 'fora';
      end if;
    end if;
  end if;

  select count(*) into v_ativas from public.leaderboard_entries
   where player_id = p_player and scope = p_scope and period_key = p_period;
  return jsonb_build_object(
    'situacao', v_situacao, 'score', p_score, 'vagas', 3 - v_ativas,
    'precisa_superar', case when v_ativas >= 3 then
      (select min(score) from public.leaderboard_entries
        where player_id = p_player and scope = p_scope and period_key = p_period) end
  ) || v_extra;
end $$;

alter table public.leaderboard_entries enable row level security;
create policy leaderboard_read_self on public.leaderboard_entries
  for select to authenticated using ((select auth.uid()) = player_id);
-- O Supabase dá a `anon` e `authenticated` *todos* os privilégios em toda
-- tabela nova de `public` — inclusive TRUNCATE, que não passa por RLS. Revogar
-- só INSERT/UPDATE/DELETE, como a primeira migração fez, deixa o resto.
-- Aqui começa do zero e devolve só a leitura da própria linha.
revoke all on public.leaderboard_entries from anon, authenticated;
grant select on public.leaderboard_entries to authenticated;

-- E fecha a mesma porta nas tabelas da primeira migração: lá, `anon` e
-- `authenticated` ficaram com TRUNCATE, REFERENCES e TRIGGER. A API do
-- navegador não oferece nenhum dos três, então não havia como usar; mas
-- privilégio que ninguém precisa não fica concedido.
revoke truncate, references, trigger on
  public.players, public.ranked_challenges, public.ranked_runs,
  public.player_achievements, public.character_mastery, public.daily_weekly_progress
  from anon, authenticated;

-- Só o servidor registra. Ninguém de fora chama estas funções.
revoke all on function public.registrar_no_top3(uuid, text, text, text[], uuid, integer, smallint, timestamptz) from public, anon, authenticated;
revoke all on function public.top3_travar(uuid, text, text) from public, anon, authenticated;
grant execute on function public.registrar_no_top3(uuid, text, text, text[], uuid, integer, smallint, timestamptz) to service_role;

-- As partidas já verificadas entram pela mesma regra, na ordem em que
-- terminaram, como se tivessem chegado agora.
do $$
declare r record;
begin
  for r in select * from public.ranked_runs where verified order by finished_at asc loop
    perform public.registrar_no_top3(r.player_id, r.mode, r.period_key::text, r.team_ids, r.id, r.score, r.encounters_cleared, r.finished_at);
    perform public.registrar_no_top3(r.player_id, 'season', r.balance_version, r.team_ids, r.id, r.score, r.encounters_cleared, r.finished_at);
  end loop;
end $$;
