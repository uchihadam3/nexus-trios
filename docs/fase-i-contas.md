# FASE I · Contas reais (e-mail + Google)

O jogo casual nunca pediu conta e continua não pedindo. A conta serve para
duas coisas: **jogar a Jornada Ranqueada** e **aparecer no ranking**. Tudo o
mais — montar trio, colecionar lutadores, conquistas, Maestria, recordes —
funciona do mesmo jeito sem nunca digitar um e-mail.

## O que foi construído

| Arquivo | O que é |
| --- | --- |
| `src/lib/auth.ts` | A camada de conta: criar, entrar, Google, sair, recuperar e trocar senha. Recebe o cliente Supabase por parâmetro, então dá para testar sem servidor. |
| `src/lib/migracao.ts` | A oferta de levar o progresso do convidado para a conta. Nunca apaga nada. |
| `src/screens/AccountScreen.tsx` | A tela de Conta. |
| `src/conta-probe.tsx` + `conta-probe.html` | Banco de provas: desenha a tela no estado "logado" sem servidor nenhum. |
| `tests/conta.test.ts` | 18 testes da camada de conta, contra um Supabase de mentira. |
| `tests/migracao.test.ts` | 12 testes de que o progresso sobrevive. |

## As três regras do documento, e onde cada uma virou código

**"Casual pode ser guest. Online/Ranqueado exige conta."**
`src/lib/online.ts` tinha `signInAnonymously()`: qualquer visitante publicava
no ranking sem conta nenhuma. Saiu. Agora uma sessão anônima é recusada com
*"Entre na sua conta para jogar a Jornada Ranqueada."* — e jogar continua
livre.

**"Privado: e-mail, auth id, tokens, provider metadata."**
`auth.ts` devolve um objeto com exatamente quatro campos — `id`, `email`,
`handle`, `origem` — e nada mais sai de lá. Há um teste que falha se algum dia
sair. O e-mail aparece numa única linha da tela, para o próprio dono; o
ranking mostra só nome público, trio e pontuação.

**"Preservar progresso local. Ao criar conta: oferecer sincronizar/migrar.
Nunca apagar progresso silenciosamente."**
O progresso vive no aparelho e entrar numa conta não encosta nele. Quando
alguém que já jogou como convidado entra numa conta, aparece **uma vez** um
cartão dizendo o que está em jogo ("12 jornadas, 5 conquistas e Maestria em 2
lutadores") com duas saídas. As duas preservam tudo: a diferença entre elas é
de quem é o nome público daqui para a frente. Não existe caminho de
`migracao.ts` para `removeItem`.

## O que ainda não é

Subir o progresso para o servidor é da **FASE J**, quando a Edge Function
guardar perfil. Até lá "levar para a conta" significa marcar de quem é este
aparelho e carimbar o nome público — que é o que muda na tela do jogador.
Trocar de celular ainda começa do zero, e a tela não promete o contrário.

## Medido no celular (390 × 844)

| Tela | Rolagem lateral | Vazando | Alvo de toque < 44px |
| --- | --- | --- | --- |
| Entrar | não | nada | nenhum |
| Criar conta | não | nada | nenhum |
| Esqueci a senha | não | nada | nenhum |
| Cartão da migração | não | nada | nenhum |

Duas correções saíram dessa medição: as abas e os campos estavam com 42px e
39px de altura, abaixo do mínimo que um dedo acerta; e os campos estavam com
fonte de 13px, abaixo dos 16px em que o iPhone dá zoom sozinho ao focar e
joga o formulário para fora da tela.

---

## Duas chaves separadas, de propósito

`VITE_RANKED_ENABLED` liga a conta por **e-mail**. `VITE_GOOGLE_ENABLED` liga
o botão do **Google**. Elas são separadas porque não ficam prontas juntas: o
Supabase já nasce aceitando e-mail e senha, enquanto o Google depende de
credenciais emitidas no Google Cloud pelo dono do projeto. Sem a separação,
ligar o ranqueado colocava na tela um botão do Google que leva a erro — e um
botão que falha é pior do que um botão que não existe.

Quem não quiser mexer no Google nunca precisa: entrar por e-mail é um caminho
completo, com recuperação de senha, e o jogador nem vê que o Google existia.

## O que só você pode fazer (eu não tenho acesso)

Enquanto nada disto for feito, a tela de Conta mostra *"A conta online ainda
não foi conectada neste build"* e o jogo casual segue normal.

**Nenhum dos passos do Google (1) é obrigatório.** O mínimo para ter conta e
ranking online são os passos 3 e 4.

**1. Ligar o provedor Google no Supabase.** *Opcional.*
Painel do projeto → *Authentication* → *Providers* → *Google* → ligar, e colar
o Client ID e o Client Secret de um projeto do Google Cloud (*APIs & Services*
→ *Credentials* → *OAuth client ID* → tipo *Web application*). No Google
Cloud, o *Authorized redirect URI* é o que o Supabase mostra nessa mesma tela,
no formato o endereço que o Supabase mostra nessa mesma tela (termina em `/auth/v1/callback`).

**2. Cadastrar os endereços de volta no Supabase.**
*Authentication* → *URL Configuration* → *Redirect URLs*, os dois:

- `https://uchihadam3.github.io/nexus-trios/` — o jogo publicado
- `http://localhost:5173/` — para testar na sua máquina

Sem isso o Google devolve o jogador para uma página que não existe. O endereço
de volta é montado por `enderecoDeVolta()`, que já inclui o `/nexus-trios/`;
há teste para isso.

**3. Decidir se o e-mail precisa ser confirmado.**
*Authentication* → *Sign In / Providers* → *Confirm email*. Ligado é mais
seguro e mais chato (o jogador só entra depois de abrir o e-mail); a tela já
avisa quando é o caso. Desligado, entra na hora.

**4. Ligar a conta online no build.**
Trocar `VITE_RANKED_ENABLED=false` para `true` em `.env.production`. Se tiver
feito o passo 1, trocar também `VITE_GOOGLE_ENABLED` para `true`; se não
tiver, deixar `false` e o botão do Google simplesmente não aparece.

**5. Testar o caminho do Google uma vez**, no celular, pelo endereço
publicado. É o único pedaço que não consigo verificar daqui: a rede deste
ambiente recusa a conexão com o host do seu projeto Supabase, então tudo
que depende de falar com o servidor de verdade está testado contra um
Supabase de mentira, não contra o seu.
