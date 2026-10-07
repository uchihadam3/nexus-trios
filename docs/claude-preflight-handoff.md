# Preflight do handoff Codex → Claude

Primeira ação obrigatória do handoff: auditar o estado local **antes** de
editar qualquer arquivo. Este documento registra o que foi encontrado.

Data da auditoria: 2026-10-07.

## 1 · HEAD local vs HEAD remoto

| | |
|---|---|
| HEAD local | `71a5e49a26567b0bc7f4b964ca5d77bc68c979e9` |
| HEAD remoto (`origin/main`) | `71a5e49a26567b0bc7f4b964ca5d77bc68c979e9` |
| Mensagem do commit | `Match home copy to completed journey outcome` |
| Branch | `main`, rastreando `origin/main` |

Os dois são **o mesmo commit** — exatamente o que a auditoria pública
anterior ao handoff havia previsto.

## 2 · Achado principal: não há trabalho do Codex neste container

O handoff parte da hipótese de que o repositório local recebido teria mais
coisas que a `main` remota, e que esse excedente seria trabalho não publicado
do Codex a preservar. **Essa hipótese não se confirma aqui.**

| | |
|---|---|
| Commits locais não publicados | **0** |
| Arquivos modificados (`git status`) | **0** |
| Arquivos untracked | **0** |
| Arquivos staged | **0** |

O repositório deste container é um clone raso (`--depth 1`) feito agora, a
partir do remoto. Não existe árvore de trabalho herdada, não existe stash, não
existe branch local além de `main`.

Consequência direta para o plano: a **FASE A** ("concluir exatamente o que o
Codex deixou pela metade") **não tem o que concluir**. Se existe trabalho do
Codex, ele está em outra máquina e não chegou até aqui. Tudo a partir da
expansão do roster precisa ser construído sobre a base de 100 personagens.

Nada foi descartado para chegar a esse estado: não houve `reset --hard`, nem
`checkout` descartando mudanças, nem `clean`, nem `rebase`.

## 3 · Roster atual

| | |
|---|---|
| Total de personagens | **100** |
| Definidos em `src/data/characters.ts` | 24 |
| Definidos em `src/data/expanded-roster.ts` | 76 |
| IDs únicos | 100 |
| Nomes únicos | 100 |
| IDs duplicados | nenhum |
| Nomes duplicados | nenhum |

A composição bate com a descrita no handoff. `characters.ts` declara os 24
primeiros em linha e espalha os 76 de `expanded-roster.ts` no mesmo array, e
só então aplica `intelligenceFor`. Quem importar `characters` recebe os 100
já montados — `expandedCharacters` **não** é uma lista adicional, é um
pedaço da mesma.

Faltam, portanto, **150 personagens** para fechar os 250 aprovados.

## 4 · O que já existe

Telas (`src/screens/`): `Home`, `DraftScreen`, `BattleScreen`,
`ResultScreen`, `Auxiliary`, `DebugScreen`, `VfxLabScreen`.

Componentes de batalha (`src/components/`): `BattleEffects`,
`BattleInspector`, `CombatConnections`, `FighterCard`, `Portrait`,
`StatusBadge`, `CharacterModal`, `Icon`.

Ferramentas de geração (`tools/`):

- `vfx/generate_vfx.py` — a base de VFX a preservar e expandir;
- `audio/generate_sfx.py` — a biblioteca de SFX a refazer;
- `audio/generate_battle_music.py`;
- `portraits/optimize_portraits.py`;
- `icons/generate-icons.ts`.

Publicação: GitHub Actions (`.github/workflows/pages.yml`) dispara em push
para `main` e publica no GitHub Pages.

## 5 · O que ainda não existe

Confirmado por busca no código — nenhuma ocorrência de `supabase` em `src/`
nem em `package.json`:

- roster com 250;
- Supabase (Auth, Postgres, RLS, Edge Functions);
- tela de Conta;
- login e-mail/senha;
- login Google;
- ranking online;
- Jornada Ranqueada validada no servidor;
- regra de até 3 trios por conta;
- Objetivos;
- Conquistas;
- Maestria;
- tela Progresso;
- Raio-X do Trio causal (existe o pós-batalha simples, com MVP, maior dano,
  maior apoio, melhor controle, momento decisivo e `topSynergy`).

## 6 · Baseline de qualidade

Medido neste commit, antes de qualquer alteração:

| Verificação | Resultado |
|---|---|
| `npm test` | **70 testes em 7 arquivos, todos passando** |
| `npm run typecheck` | limpo |
| `npm run lint` | limpo |

Arquivos de teste: `assets`, `audiovisual`, `battle`, `language`,
`presentation`, `roster`, `run-summary`.

Este é o piso. Nenhuma fase pode fechar abaixo dele.

## 7 · Uma limitação do ambiente, declarada antes de começar

O passo 15 do adendo pede, para cada parte: abrir a versão publicada e validar
visualmente. Neste container o proxy de saída **bloqueia** o domínio do
GitHub Pages (`CONNECT` recusado), então não é possível buscar a URL pública
daqui.

O que é possível, e será feito no lugar:

1. confirmar pela API do GitHub que o workflow de deploy concluiu com sucesso
   no commit publicado;
2. servir o `dist` real por um servidor local e validar visualmente ali, com
   capturas em 360 / 390 / 430 px e desktop.

É uma validação do mesmo artefato que o Pages serve, não do endpoint público.
A diferença está registrada aqui para não ser confundida com a outra.
