#!/usr/bin/env bash
# Aplica no Supabase as migrações novas de supabase/migrations.
#
# Só as de versão >= PRIMEIRA (as anteriores já foram aplicadas à mão e estão
# registradas). Cada uma roda dentro de um bloco só — entra inteira ou não
# entra — e é registrada em supabase_migrations.schema_migrations, como faz o
# `supabase db push`; uma migração já registrada é pulada, então rodar de novo
# a cada publicação é seguro.
#
# Uso:  SUPABASE_ACCESS_TOKEN=... scripts/aplicar-migracoes.sh [project-ref]
#       scripts/aplicar-migracoes.sh --sql     (só imprime o SQL, para teste)
set -euo pipefail
PRIMEIRA=20261015000000
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

sql_das_migracoes() {
  local f base v nome tag
  for f in "$RAIZ"/supabase/migrations/*.sql; do
    base="$(basename "$f" .sql)"; v="${base%%_*}"; nome="${base#*_}"
    [[ "$v" =~ ^[0-9]{14}$ ]] || { echo "Nome de migração inválido: $base" >&2; exit 1; }
    (( v >= PRIMEIRA )) || continue
    tag="\$migracao_$v\$"
    grep -qF "$tag" "$f" && { echo "A migração $base contém $tag" >&2; exit 1; }
    printf 'do $aplicar$ begin\n  if not exists (select 1 from supabase_migrations.schema_migrations where version = %s) then\n    execute %s\n%s\n%s;\n    insert into supabase_migrations.schema_migrations(version, name) values (%s, %s);\n    raise notice %s;\n  end if;\nend $aplicar$;\n' \
      "'$v'" "$tag" "$(cat "$f")" "$tag" "'$v'" "'$nome'" "'aplicada: $base'"
  done
}

if [[ "${1:-}" == "--sql" ]]; then sql_das_migracoes; exit 0; fi
: "${SUPABASE_ACCESS_TOKEN:?Defina SUPABASE_ACCESS_TOKEN (chave do painel do Supabase).}"
REF="${1:-hzfavpcchfzlggwdbiqd}"
SQL="$(sql_das_migracoes)"
[[ -n "$SQL" ]] || { echo "Nenhuma migração nova."; exit 0; }
SQL="$SQL select version, name from supabase_migrations.schema_migrations where version >= '$PRIMEIRA' order by version;"
jq -n --arg q "$SQL" '{query: $q}' | curl -sS --fail -X POST "https://api.supabase.com/v1/projects/$REF/database/query" \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" -H "Content-Type: application/json" --data-binary @-
echo
