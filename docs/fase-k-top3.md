# FASE K · Até 3 trios diferentes por conta, em cada ranking

A regra do documento: cada conta tem no máximo **3 entradas ativas** em cada
ranking (Hoje, Semana, Temporada), e as 3 precisam ser de **trios
diferentes**. Trio é o conjunto dos 3 ids, `sort(ids).join('|')`: a ordem não
cria trio novo. "Meus recordes" guarda o histórico completo.

Antes desta fase o ranking guardava só a melhor partida de cada conta.

## Onde a regra mora: no banco

`supabase/migrations/20261008000000_top3_por_conta.sql`

- `leaderboard_entries`, com `unique(player_id, scope, period_key,
  canonical_team)`, como o documento pede.
- `registrar_no_top3(...)` decide e grava, e devolve o que aconteceu:

  | situação | quando | o que a tela diz |
  | --- | --- | --- |
  | `novo` | trio novo, havia vaga | NOVO TRIO NO SEU TOP 3 · 1 vaga livre. |
  | `melhorou` | mesmo trio, pontuação maior | RECORDE DO TRIO · subiu de X para Y |
  | `manteve` | mesmo trio, igual ou menor | MESMO TRIO · o recorde continua X |
  | `entrou` | trio novo, sem vaga, superou o pior | NOVO TOP 3 · o resultado de X saiu |
  | `fora` | trio novo, sem vaga, não superou | Não entrou nos seus 3 melhores. Para entrar: supere X. |

  Empate com o pior não entra ("supere"). No empate entre os piores, sai o
  mais recente, porque quem chegou antes também fica na frente no ranking.

- **"Duas submissões simultâneas nunca podem criar 4 slots."** Cada (conta,
  ranking, período) tem uma trava transacional (`pg_advisory_xact_lock`). Quem
  chega em segundo espera o primeiro terminar antes de contar as vagas.
- O gatilho `top3_guarda` repete a trava e a contagem em **qualquer** INSERT.
  Nem um caminho futuro que esqueça a função consegue abrir uma quarta vaga.
- Só o servidor registra. O navegador não executa a função nem escreve na
  tabela.
- As partidas verificadas que já existiam entram pela mesma regra quando a
  migração roda.

## Testado num Postgres de verdade

`tests/top3.sql.test.ts` roda as migrações reais num banco descartável e
confere os exemplos do documento (mesmo trio, quarto trio que não entra,
quarto trio que entra, empate), a separação entre rankings, o INSERT direto
recusado, as permissões, a reconstrução a partir do histórico e a
concorrência: **20 partidas da mesma conta soltas ao mesmo tempo, cada uma
pela sua conexão, deixam exatamente as 3 maiores.**

Precisa de `NEXUS_PG_URL`. No GitHub, o workflow `banco.yml` sobe um Postgres
16 e roda esses testes a cada push. Ele também roda `deno check` na função do
servidor, que o typecheck do projeto não enxerga.

## Servidor e telas

- `ranked-api`: `submit` registra a partida no ranking do período e no da
  temporada **antes** de marcá-la como validada. Se a segunda escrita falhar,
  a partida fica aberta e pode ser reenviada, e reenviar é seguro. O
  `leaderboard` lê `leaderboard_entries` e devolve `meus` (as entradas da
  conta, vagas e o que é preciso superar). Há uma ação nova, `historico`.
- Tela de resultado: o aviso do Top 3 com as frases do documento
  (`src/lib/top3.ts`, testadas em `tests/top3.test.ts`).
- Ranking: a caixa "Meus 3 melhores trios" acima de cada período. As linhas
  da própria conta ficam marcadas, até 3. "Meus recordes" mostra todas as
  jornadas validadas.

**O jogo funciona com as duas versões da função.** Com a anterior (a
publicada antes desta fase), não aparece caixa nem aviso, e "Meus recordes"
mostra o que mostrava. Conferido no navegador simulando as duas respostas.

## Estado no Supabase (2026-10-07)

**Banco: aplicado.** A migração rodou primeiro como ensaio no banco de
produção (Postgres 17), dentro de uma transação desfeita no fim, e depois de
verdade, registrada em `supabase_migrations.schema_migrations` como
`20261008000000 top3_por_conta`. Conferido depois de aplicar: `anon` não tem
nada na tabela nova; `authenticated` só lê; só o `service_role` registra.

**As permissões padrão do Supabase.** Todo objeto novo em `public` nasce com
*todos* os privilégios para `anon` e `authenticated`, inclusive TRUNCATE, que
não passa por RLS. A primeira migração só revogou INSERT/UPDATE/DELETE, e as
tabelas dela ficaram com TRUNCATE, REFERENCES e TRIGGER. A API do navegador
não oferece nenhum dos três, então não havia como usar, mas a migração da
FASE K revoga tudo isso. O banco de teste (`tests/sql/supabase-stub.sql`)
agora imita essas permissões padrão, e um teste cobra que o TRUNCATE foi
fechado.

**Função: ainda é a anterior.** O empacotador do Supabase recusa a função,
porque o código do jogo importa sem extensão (`./expanded-roster`).
`scripts/publicar-funcao.sh` junta tudo com esbuild num arquivo só. Esse
pacote foi testado num Deno local: carrega, aceita o jogo publicado com o
cabeçalho `x-client-info`, exige login e recusa outras origens. A publicação
em si foi bloqueada pela proteção do ambiente de trabalho contra deploy em
produção e espera a autorização do dono do projeto.

Enquanto isso, tudo funciona como antes. A função anterior não usa a tabela
nova, e o jogo publicado entende as duas versões. O script, depois de
publicar, reaplica a regra às partidas validadas no meio-tempo.
