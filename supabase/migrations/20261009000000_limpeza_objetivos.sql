-- Limpeza: o que os Objetivos diários e semanais deixaram no banco.
--
-- Os Objetivos saíram do ranqueado na FASE H (docs/fase-h-conquistas.md): a
-- pontuação deixou de somar 12.000 por objetivo cumprido. Desde então
-- `ranked_runs.objectives_completed` só recebe nulo e `daily_weekly_progress`
-- nunca é lida nem escrita — nem pelo jogo, nem pela função `ranked-api`, nem
-- por função do banco. Ficaram só ocupando espaço e privilégio.
alter table public.ranked_runs drop column if exists objectives_completed;
drop table if exists public.daily_weekly_progress;
