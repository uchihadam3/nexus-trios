#!/usr/bin/env bash
# Publica a função `ranked-api` no Supabase.
#
# Por que não `supabase functions deploy` direto: a função importa o motor do
# jogo (`src/...`), e o código do jogo importa sem extensão
# (`./expanded-roster`). O empacotador do Supabase não resolve isso e recusa
# a publicação ("Module not found"). Aqui o esbuild junta a função e todo o
# código do jogo num arquivo só, deixando de fora apenas `npm:` (a biblioteca
# do Supabase, que o Deno do servidor resolve), e é esse arquivo que sobe.
#
# Depois de publicar, reaplica a regra do Top 3 às partidas validadas: as que
# chegaram enquanto a função anterior estava no ar não passaram por ela.
# Reaplicar é seguro — o mesmo trio com a mesma pontuação só "mantém".
# A Jornada normal (seed própria, diferente da do desafio) só tem o ranking da
# Temporada.
#
# Uso:  SUPABASE_ACCESS_TOKEN=... scripts/publicar-funcao.sh [project-ref]
set -euo pipefail
: "${SUPABASE_ACCESS_TOKEN:?Defina SUPABASE_ACCESS_TOKEN (chave do painel do Supabase).}"
REF="${1:-hzfavpcchfzlggwdbiqd}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
B="$(mktemp -d)"
trap 'rm -rf "$B"' EXIT

mkdir -p "$B/supabase/functions/ranked-api"
npx esbuild "$RAIZ/supabase/functions/ranked-api/index.ts" --bundle --format=esm --platform=neutral \
  --target=es2022 --external:'npm:*' --outfile="$B/supabase/functions/ranked-api/index.ts" --log-level=warning
printf 'project_id = "nexus-trios"\n' > "$B/supabase/config.toml"
npx -y supabase@2 functions deploy ranked-api --project-ref "$REF" --use-api --workdir "$B"

curl -sS --fail -X POST "https://api.supabase.com/v1/projects/$REF/database/query" \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"do $$ declare r record; begin for r in select x.*, c.seed as seed_do_desafio from public.ranked_runs x join public.ranked_challenges c on c.id = x.challenge_id where x.verified order by x.finished_at loop if r.seed = r.seed_do_desafio then perform public.registrar_no_top3(r.player_id, r.mode, r.period_key::text, r.team_ids, r.id, r.score, r.encounters_cleared, r.finished_at); end if; perform public.registrar_no_top3(r.player_id, '\''season'\'', r.balance_version, r.team_ids, r.id, r.score, r.encounters_cleared, r.finished_at); end loop; end $$; select count(*) as entradas from public.leaderboard_entries;"}'
echo
