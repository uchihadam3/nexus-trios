-- A Jornada com os seus (pedido do jogador): o trio escolhido entre os personagens já liberados nas Conquistas, sem o
-- bônus das estrelas de pontos e com 30 mil a menos por luta. Fica marcado quando a jornada abre no servidor, para o
-- replay cobrar a regra mesmo que o aparelho não mande nada no fim.
alter table public.ranked_runs add column colecao boolean not null default false;
