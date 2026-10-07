-- O mínimo do Supabase para as migrações rodarem num Postgres comum:
-- os papéis, o esquema auth e auth.uid(). Só para teste local.
do $$ begin
  if not exists (select from pg_roles where rolname = 'anon') then create role anon; end if;
  if not exists (select from pg_roles where rolname = 'authenticated') then create role authenticated; end if;
  if not exists (select from pg_roles where rolname = 'service_role') then create role service_role; end if;
end $$;
create schema if not exists auth;
create table if not exists auth.users (id uuid primary key default gen_random_uuid());
create or replace function auth.uid() returns uuid language sql stable as
$$ select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;

-- O que o Supabase faz e um Postgres comum não: todo objeto novo em `public`
-- nasce com todos os privilégios para `anon`, `authenticated` e
-- `service_role`. Sem imitar isto, um teste de permissão passaria aqui e o
-- buraco existiria lá.
alter default privileges in schema public grant all on tables to anon, authenticated, service_role;
alter default privileges in schema public grant all on functions to anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to anon, authenticated, service_role;
grant usage on schema public to anon, authenticated, service_role;
