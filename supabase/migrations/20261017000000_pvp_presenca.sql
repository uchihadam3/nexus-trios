-- PvP online: quem ainda está na partida (pedido do jogador: quem cai tem 45 s para voltar; depois disso perde).
-- Cada pedido do aparelho à função marca "estou aqui". Fica fora do Realtime de propósito: é escrito a cada poucos
-- segundos e não pode virar aviso para o outro aparelho (um aviso faria o outro pedir, que avisaria de volta…).
create table if not exists public.pvp_presenca (
  partida_id uuid not null references public.pvp_partidas(id) on delete cascade,
  jogador uuid not null references public.players(id) on delete cascade,
  visto_em timestamptz not null default now(),
  primary key (partida_id, jogador)
);
alter table public.pvp_presenca enable row level security;
revoke all on public.pvp_presenca from anon, authenticated;
grant all on public.pvp_presenca to service_role;

-- "Desistir" dentro da luta vale só para aquela rodada (pedido do jogador): quem desiste perde a rodada, a partida segue.
alter table public.pvp_rodadas add column if not exists rendida boolean not null default false;
