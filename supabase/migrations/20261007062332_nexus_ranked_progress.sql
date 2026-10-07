-- Ranked results are written only by the verifying Edge Function. There are
-- deliberately no INSERT/UPDATE policies for authenticated browser clients.
create table public.players (
  id uuid primary key references auth.users(id) on delete cascade,
  handle text not null check (handle ~ '^[A-Za-z0-9_ ]{3,16}$' and handle = btrim(handle)),
  handle_normalized text generated always as (lower(btrim(handle))) stored unique,
  nexus_level integer not null default 1 check (nexus_level between 1 and 10000),
  xp integer not null default 0 check (xp >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  renamed_at timestamptz
);

create table public.ranked_challenges (
  id uuid primary key default gen_random_uuid(),
  mode text not null check (mode in ('daily','weekly')),
  period_key date not null,
  seed integer not null,
  engine_version text not null,
  balance_version text not null,
  roster_fingerprint text not null,
  created_at timestamptz not null default now(),
  unique (mode,period_key,engine_version)
);

create table public.ranked_runs (
  id uuid primary key default gen_random_uuid(),
  player_id uuid not null references public.players(id) on delete cascade,
  challenge_id uuid not null references public.ranked_challenges(id),
  mode text not null check (mode in ('daily','weekly')),
  period_key date not null,
  seed integer not null,
  engine_version text not null,
  balance_version text not null,
  roster_fingerprint text not null,
  team_ids text[] not null check (cardinality(team_ids)=3),
  started_at timestamptz not null default now(),
  expires_at timestamptz not null default (now()+interval '24 hours'),
  finished_at timestamptz,
  encounters_cleared smallint check (encounters_cleared between 0 and 10),
  score integer check (score between 0 and 10999999),
  objectives_completed smallint check (objectives_completed between 0 and 3),
  verified boolean not null default false,
  summary jsonb,
  digest text,
  constraint finish_verified check ((not verified and finished_at is null and score is null) or (verified and finished_at is not null and score is not null))
);
create index ranked_runs_player_started_idx on public.ranked_runs(player_id,started_at desc);
create index ranked_runs_board_idx on public.ranked_runs(mode,period_key,score desc,finished_at asc) where verified;
create index ranked_runs_world_idx on public.ranked_runs(score desc,finished_at asc) where verified;

create table public.player_achievements (
  player_id uuid not null references public.players(id) on delete cascade,
  achievement_id text not null,
  unlocked_at timestamptz not null default now(),
  progress integer not null default 0 check (progress>=0),
  primary key (player_id,achievement_id)
);
create table public.character_mastery (
  player_id uuid not null references public.players(id) on delete cascade,
  character_id text not null,
  level smallint not null default 0 check (level between 0 and 3),
  objective_1 integer not null default 0,
  objective_2 integer not null default 0,
  objective_3 integer not null default 0,
  updated_at timestamptz not null default now(),
  primary key (player_id,character_id)
);
create table public.daily_weekly_progress (
  player_id uuid not null references public.players(id) on delete cascade,
  objective_id text not null,
  period_key date not null,
  progress integer not null default 0 check (progress>=0),
  completed_at timestamptz,
  primary key (player_id,objective_id,period_key)
);

alter table public.players enable row level security;
alter table public.ranked_challenges enable row level security;
alter table public.ranked_runs enable row level security;
alter table public.player_achievements enable row level security;
alter table public.character_mastery enable row level security;
alter table public.daily_weekly_progress enable row level security;

create policy players_read_self on public.players for select to authenticated using ((select auth.uid())=id);
create policy challenges_read on public.ranked_challenges for select to authenticated using (true);
create policy runs_read_self on public.ranked_runs for select to authenticated using ((select auth.uid())=player_id);
create policy achievements_read_self on public.player_achievements for select to authenticated using ((select auth.uid())=player_id);
create policy mastery_read_self on public.character_mastery for select to authenticated using ((select auth.uid())=player_id);
create policy objectives_read_self on public.daily_weekly_progress for select to authenticated using ((select auth.uid())=player_id);

-- Even when Data API exposes public tables, ordinary users cannot write
-- verified scores or another user's profile. Only server-side service role
-- code performs validated writes.
grant select on public.players,public.ranked_challenges,public.ranked_runs,public.player_achievements,public.character_mastery,public.daily_weekly_progress to authenticated;
revoke insert,update,delete on public.players,public.ranked_challenges,public.ranked_runs,public.player_achievements,public.character_mastery,public.daily_weekly_progress from anon,authenticated;
