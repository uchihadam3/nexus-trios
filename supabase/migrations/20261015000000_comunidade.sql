-- Comunidade: quem está online, chat global e mensagens privadas com "visto".
--
-- O navegador só LÊ estas tabelas, e só o que lhe cabe (RLS): o chat global é
-- de todos os logados; uma conversa privada, só dos dois. Toda escrita passa
-- pelas funções abaixo (security definer), que conferem quem está mandando,
-- o tamanho do texto e o ritmo — ninguém escreve em nome de outro, apaga
-- mensagem alheia ou marca como vista uma conversa que não é sua.
--
-- Presença: o jogo aberto com a conta chama `comunidade_ping()` a cada ~30 s e
-- `comunidade_sair()` ao fechar. Online = marcou presença há menos de 75 s.
-- `online_desde` só reinicia quando a pessoa volta depois de ter saído.

create table public.comunidade_presenca (
  player_id uuid primary key references public.players(id) on delete cascade,
  online boolean not null default true,
  online_desde timestamptz not null default now(),
  visto_em timestamptz not null default now()
);

create table public.chat_mensagens (
  id bigint generated always as identity primary key,
  autor_id uuid not null references public.players(id) on delete cascade,
  -- null = chat global; senão, a conversa privada com esta conta
  para_id uuid references public.players(id) on delete cascade,
  texto text not null check (char_length(texto) between 1 and 500 and texto = btrim(texto)),
  resposta_a bigint references public.chat_mensagens(id) on delete set null,
  criada_em timestamptz not null default now(),
  -- "visto" (✓✓): só nas privadas, quando quem recebeu abriu a conversa
  vista_em timestamptz,
  constraint chat_nao_para_si check (para_id is null or para_id <> autor_id),
  constraint chat_visto_so_privada check (para_id is not null or vista_em is null)
);
create index chat_global_idx on public.chat_mensagens(id desc) where para_id is null;
create index chat_privada_idx on public.chat_mensagens(autor_id, para_id, id desc) where para_id is not null;
create index chat_recebidas_idx on public.chat_mensagens(para_id, autor_id, id desc) where para_id is not null and vista_em is null;

create table public.chat_reacoes (
  mensagem_id bigint not null references public.chat_mensagens(id) on delete cascade,
  player_id uuid not null references public.players(id) on delete cascade,
  -- null = tirou a reação (fica a linha: o Realtime entrega a mudança pela RLS, coisa que não faz com DELETE)
  emoji text check (emoji is null or emoji in ('🔥','😂','👏','😮','💀','❤️')),
  criada_em timestamptz not null default now(),
  -- uma reação por pessoa em cada mensagem (trocar substitui)
  primary key (mensagem_id, player_id)
);

alter table public.comunidade_presenca enable row level security;
alter table public.chat_mensagens enable row level security;
alter table public.chat_reacoes enable row level security;

-- Quem pode ler cada mensagem. A mesma regra decide o que o Realtime entrega.
create function public.chat_pode_ler(p_autor uuid, p_para uuid) returns boolean
language sql stable set search_path = '' as
$$ select p_para is null or (select auth.uid()) in (p_autor, p_para) $$;

create policy chat_ler on public.chat_mensagens for select to authenticated
  using (public.chat_pode_ler(autor_id, para_id));
create policy reacoes_ler on public.chat_reacoes for select to authenticated
  using (exists (select 1 from public.chat_mensagens m where m.id = mensagem_id and public.chat_pode_ler(m.autor_id, m.para_id)));
create policy presenca_ler on public.comunidade_presenca for select to authenticated using (true);

-- O Supabase dá tudo em `public` para anon e authenticated; aqui começa do zero.
revoke all on public.comunidade_presenca, public.chat_mensagens, public.chat_reacoes from anon, authenticated;
grant select on public.comunidade_presenca, public.chat_mensagens, public.chat_reacoes to authenticated;

-- Quem chama precisa ter perfil público (nome). Devolve o id.
create function public.comunidade_eu() returns uuid
language plpgsql stable security definer set search_path = '' as $$
declare eu uuid := (select auth.uid());
begin
  if eu is null or not exists (select 1 from public.players where id = eu) then
    raise exception 'comunidade: escolha seu nome antes' using errcode = '42501';
  end if;
  return eu;
end $$;

create function public.comunidade_ping() returns void
language plpgsql volatile security definer set search_path = '' as $$
declare eu uuid := public.comunidade_eu();
begin
  insert into public.comunidade_presenca as p (player_id) values (eu)
  on conflict (player_id) do update set
    online = true,
    visto_em = now(),
    -- voltou depois de ter saído (ou de sumir por mais de 75 s): online de novo, a partir de agora
    online_desde = case when not p.online or p.visto_em < now() - interval '75 seconds' then now() else p.online_desde end;
end $$;

create function public.comunidade_sair() returns void
language plpgsql volatile security definer set search_path = '' as $$
declare eu uuid := public.comunidade_eu();
begin
  update public.comunidade_presenca set online = false, visto_em = now() where player_id = eu;
end $$;

-- Todos os jogadores com nome, para a lista da comunidade: online agora,
-- desde quando, quando saiu, e um pouco de cada um (melhor pontuação geral,
-- o trio dela e quantos personagens já liberou).
create function public.comunidade_jogadores() returns table (
  id uuid, nome text, online boolean, online_desde timestamptz, visto_em timestamptz,
  recorde integer, trio text[], conquistas integer, desde timestamptz
)
language sql stable security definer set search_path = '' as $$
  select p.id, p.handle,
    coalesce(c.online and c.visto_em > now() - interval '75 seconds', false),
    c.online_desde, c.visto_em,
    r.score, r.team_ids,
    (select count(*)::int from public.player_achievements a where a.player_id = p.id and a.achievement_id like 'personagem:%'),
    p.created_at
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

-- Manda uma mensagem (global sem `p_para`). No máximo 6 a cada 15 s, e a
-- mesma frase seguida no mesmo lugar não repete em menos de 30 s.
create function public.chat_enviar(p_texto text, p_para uuid default null, p_resposta bigint default null)
returns public.chat_mensagens
language plpgsql volatile security definer set search_path = '' as $$
declare eu uuid := public.comunidade_eu(); t text := btrim(coalesce(p_texto, '')); nova public.chat_mensagens;
begin
  if char_length(t) = 0 then raise exception 'chat: mensagem vazia' using errcode = '22023'; end if;
  if char_length(t) > 500 then raise exception 'chat: até 500 letras' using errcode = '22023'; end if;
  if p_para is not null and (p_para = eu or not exists (select 1 from public.players where id = p_para)) then
    raise exception 'chat: destinatário inválido' using errcode = '22023';
  end if;
  if p_resposta is not null and not exists (
    select 1 from public.chat_mensagens m where m.id = p_resposta
      and (case when p_para is null then m.para_id is null
                else (m.autor_id, m.para_id) in ((eu, p_para), (p_para, eu)) end)) then
    raise exception 'chat: resposta inválida' using errcode = '22023';
  end if;
  perform pg_advisory_xact_lock(hashtextextended('chat:' || eu::text, 0));
  if (select count(*) from public.chat_mensagens where autor_id = eu and criada_em > now() - interval '15 seconds') >= 6 then
    raise exception 'chat: devagar, espere uns segundos' using errcode = '53400';
  end if;
  if exists (select 1 from public.chat_mensagens where autor_id = eu and para_id is not distinct from p_para
             and texto = t and criada_em > now() - interval '30 seconds') then
    raise exception 'chat: mensagem repetida' using errcode = '53400';
  end if;
  insert into public.chat_mensagens (autor_id, para_id, texto, resposta_a) values (eu, p_para, t, p_resposta) returning * into nova;
  perform public.comunidade_ping();
  return nova;
end $$;

-- Marca como vistas as mensagens que `p_de` mandou para mim (abri a conversa).
create function public.chat_marcar_vistas(p_de uuid) returns integer
language plpgsql volatile security definer set search_path = '' as $$
declare eu uuid := public.comunidade_eu(); n integer;
begin
  update public.chat_mensagens set vista_em = now()
  where para_id = eu and autor_id = p_de and vista_em is null;
  get diagnostics n = row_count;
  return n;
end $$;

-- Reage a uma mensagem que eu posso ler; o mesmo emoji de novo tira a reação.
create function public.chat_reagir(p_mensagem bigint, p_emoji text) returns void
language plpgsql volatile security definer set search_path = '' as $$
declare eu uuid := public.comunidade_eu();
begin
  if not exists (select 1 from public.chat_mensagens m where m.id = p_mensagem
                 and (m.para_id is null or eu in (m.autor_id, m.para_id))) then
    raise exception 'chat: mensagem não encontrada' using errcode = '22023';
  end if;
  if p_emoji is null or p_emoji not in ('🔥','😂','👏','😮','💀','❤️') then
    raise exception 'chat: reação inválida' using errcode = '22023';
  end if;
  insert into public.chat_reacoes as r (mensagem_id, player_id, emoji) values (p_mensagem, eu, p_emoji)
  on conflict (mensagem_id, player_id) do update
    set emoji = case when r.emoji = excluded.emoji then null else excluded.emoji end, criada_em = now();
end $$;

-- As conversas privadas: com quem, a última mensagem e quantas não li.
create function public.chat_conversas() returns table (
  com_id uuid, com_nome text, ultima_id bigint, ultima_texto text, ultima_em timestamptz,
  ultima_minha boolean, ultima_vista boolean, nao_lidas integer
)
language sql stable security definer set search_path = '' as $$
  with eu as (select public.comunidade_eu() as id),
  minhas as (
    select m.*, case when m.autor_id = (select id from eu) then m.para_id else m.autor_id end as outro
    from public.chat_mensagens m
    where m.para_id is not null and (select id from eu) in (m.autor_id, m.para_id)
  ),
  ultimas as (select distinct on (outro) * from minhas order by outro, id desc)
  select u.outro, p.handle, u.id, u.texto, u.criada_em, u.autor_id = (select id from eu), u.vista_em is not null,
    (select count(*)::int from minhas x where x.outro = u.outro and x.para_id = (select id from eu) and x.vista_em is null)
  from ultimas u join public.players p on p.id = u.outro
  order by u.id desc
$$;

-- Só os logados chamam as funções; ninguém escreve direto nas tabelas.
revoke all on function public.chat_pode_ler(uuid, uuid), public.comunidade_eu(), public.comunidade_ping(), public.comunidade_sair(),
  public.comunidade_jogadores(), public.chat_enviar(text, uuid, bigint), public.chat_marcar_vistas(uuid),
  public.chat_reagir(bigint, text), public.chat_conversas() from public, anon;
grant execute on function public.chat_pode_ler(uuid, uuid), public.comunidade_ping(), public.comunidade_sair(),
  public.comunidade_jogadores(), public.chat_enviar(text, uuid, bigint), public.chat_marcar_vistas(uuid),
  public.chat_reagir(bigint, text), public.chat_conversas() to authenticated;

-- Mensagens, vistos e reações chegam na hora (Realtime), filtrados pela RLS acima.
do $$ begin
  if exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    alter publication supabase_realtime add table public.chat_mensagens, public.chat_reacoes;
  end if;
end $$;
