# Relatório final · NEXUS DUEL

O relatório da seção 39 do handoff, item por item. Onde algo ficou pela metade
ou mudou por decisão do dono do projeto, o item diz isso, e diz por quê. Cada
fase tem seu documento em `docs/`, com a medição que sustenta o que está aqui.

## Estado de partida

1. **Estado encontrado do trabalho do Codex.** Não havia trabalho do Codex
   neste container: HEAD local e remoto eram o mesmo commit (`71a5e49`), sem
   commits locais, sem arquivos modificados, sem stash. O roster tinha 100
   personagens. Registrado em `docs/claude-preflight-handoff.md`.
2. **Commits locais preservados.** Não havia nenhum para preservar. Nada foi
   descartado: sem `reset --hard`, sem `clean`, sem `force push`.
3. **Fases que já estavam feitas.** Nenhuma das fases A–L. A FASE A
   ("concluir o que o Codex deixou") não tinha o que concluir.
4. **Fases completadas.** B, C, D, E, F, G, H, I, J, K e L, com as ressalvas
   dos itens 15, 19 e 26–27.

## Roster e combate

5. **Contagem final: 250 personagens**, conferida pelo próprio código
   (`characters.length`), todos com ids e nomes únicos.
6. **Novas mecânicas.** A auditoria da FASE C achou catorze traços que nunca
   disparavam (defeito de motor, não de dados) e quatro habilidades com trava
   estrutural. Os traços passaram a disparar e as travas caíram de 29 para 0.
   Depois, na FASE E, apareceram 80 efeitos ofensivos que caíam no próprio
   trio (a Sakura causava 306 de dano em si mesma a cada uso). Corrigidos e
   remedidos: 16.158 de dano autoinfligido em 30 lutas antes, 0 depois.
7. **Auditoria de clones.** Dezesseis pares de personagens parecidos demais
   foram afastados. O par mais próximo depois disso (Aquaman ~ Eric Cartman,
   distância 0,0822) fica acima do limite. `docs/fase-c-diversidade.md`.
8. **Calibração global.** Os 250 foram calibrados juntos, por arquétipo, e o
   achado principal foi sobre a medição: com 24 lutas, o ruído é de ±25
   pontos e não serve para julgar personagem individual; com 300, cai para
   ±5,6. Correções medidas: `tempest` de 76,7% para 66,2% de vitórias,
   `evader` de 15,3% para 21,7%. `docs/fase-d-calibragem.md`.
9. **Tempestade antes/depois.** Com 24 lutas parecia abaixo da média (37,5%).
   Com 300 lutas ficou dentro de ±5,6 pontos da média do elenco. **A
   simulação não confirmou o nerf pedido**, e ele não foi aplicado.
10. **Saitama validado.** Dentro da faixa com 300 lutas, e **não foi
    nerfado**. Nota aberta: ele morre em 77% das lutas apesar de ser a âncora
    de sobrevivência do trio, e isso merece um olhar próprio.

## Clareza e identidade

11. **Clareza.** Toda ficha diz em quem cada efeito cai, sem jargão ("inimigo
    mais ferido", não "mais fácil de derrubar"; "inimigo mais forte", não
    "maior ameaça", que estava errado). Os efeitos são agrupados por alvo:
    alvo repetido na mesma ficha caiu de 213 para 0, e o texto total, 22%.
    `docs/fase-e-clareza.md`.
12. **"Aplica Status".** Todo Status aparece como aplicação explícita, com
    alvo, valor, quanto acumula e duração ("Exposto · Recebe +12% de dano ·
    soma por aplicação até 65% · 5 s"). Coberto por testes.
13. **Sistema de 2–4 identidades.** Refeito na FASE F: antes, "Dano" aparecia
    em 250 de 250 personagens e 114 tinham identidade cortada; depois, o termo
    mais comum cobre 22% e ninguém fica cortado. O Draft usa essas
    identidades. `docs/fase-f-identidades.md`.
14. **Raio-X do trio.** O pós-batalha mostra conexões causais reais entre os
    três (carga, cura, escudo, aceleração, preparo protegido, finalização,
    controle...). A escala foi recalibrada pelo que se mede: "ÓTIMA CONEXÃO"
    saía em 56% das lutas, agora em 12%. `docs/fase-g-raio-x.md`.

## Progressão

15. **Objetivos.** Construídos e depois **removidos a pedido do dono do
    projeto** ("esses objetivos são ruins, tira isso, deixa só as conquistas").
    A pontuação ranqueada também deixou de somá-los.
16. **Conquistas.** 52 conquistas de momento, em 10 categorias, 6 secretas.
    Quatro eram impossíveis e foram achadas por simulação, antes de chegarem
    ao jogador. `docs/fase-h-conquistas.md`.
17. **Maestria.** Por personagem, com 14 tipos de feito rastreados durante a
    luta.

## Conta e online

18. **Conta e-mail/senha: funcionando.** Testado contra o Supabase de verdade,
    pela tela do jogo: criar conta (entra na hora), entrar, senha errada em
    português, sair e recuperar senha. `docs/fase-i-contas.md`.
19. **Google Login: código pronto, ainda não ligado.** Exige um Client ID e um
    Client Secret criados no Google Cloud pelo dono do projeto. Até lá, o botão
    fica escondido (`VITE_GOOGLE_ENABLED=false`) em vez de aparecer quebrado.
    Para ligar: criar as credenciais, colar em Authentication → Providers →
    Google, e trocar a chave para `true`.
20. **Convidado → conta.** O progresso local nunca é apagado. Quem já jogou
    como convidado vê, uma vez por conta, o que está em jogo e escolhe se o
    progresso passa a ser da conta. As duas respostas preservam tudo.
21. **Supabase/RLS.** RLS ligada em todas as tabelas. Só o servidor escreve
    pontuação. A FASE K achou e fechou uma brecha: o Supabase dá TRUNCATE em
    toda tabela nova a visitantes e jogadores, e as tabelas da primeira
    migração tinham ficado assim.
22. **Ranqueada verificada no servidor.** O servidor refaz as dez lutas a
    partir do trio e da semente, compara o resultado e calcula a pontuação
    sozinho. O cliente não envia pontuação, e um envio que tente é recusado.
    Testado de ponta a ponta pela tela. No caminho, apareceu e foi corrigido um
    defeito de CORS que teria bloqueado toda ranqueada no site publicado.
23. **Top 3 por conta.** No máximo 3 entradas por conta em cada ranking, de
    trios diferentes (a ordem dos ids não cria trio novo), garantido no banco
    com trava transacional e um gatilho de defesa. `docs/fase-k-top3.md`.
24. **Testes do Top 3.** 18 testes num Postgres de verdade, que rodam no CI a
    cada push: 1ª, 2ª e 3ª entradas; 4ª pior fica fora; 4ª melhor substitui a
    pior; mesmo trio pior não altera; mesmo trio melhor atualiza; ordem
    diferente é o mesmo trio; empate não entra; **20 envios simultâneos nunca
    passam de 3**; a mesma conta pode aparecer 3 vezes, nunca 4; histórico
    preservado; rankings independentes. Também verificado em produção com uma
    conta de teste, apagada no fim.
25. **Hoje/Semana/Temporada.** Os três rankings, cada um com o seu Top 3, mais
    "Meus recordes" com o histórico completo.

## Qualidade

26. **Celular.** Todas as telas varridas em 360, 390 e 430 px: nenhuma rola
    para o lado, nada vaza, e **nenhum alvo de toque abaixo de 44 px**
    ("Adicionar ao trio" tinha 33; "Ver ficha", 14). Texto que é informação
    não fica abaixo de 11 px. A varredura roda no CI. Ressalva: na batalha, as
    bolinhas de Status continuam com 18 px. Coladas umas nas outras, aumentar
    o toque de uma tomaria o da vizinha, e o mesmo detalhe abre tocando no
    lutador. O visual aprovado da batalha não mudou.
27. **Desempenho.** O Supabase passou a carregar só quando alguém usa conta ou
    ranking: o pacote principal caiu de 983 para 783 KB (261 → 209 KB
    comprimido), e o tempo até o jogo ficar tocável num celular simulado foi
    de 1,55 s para 1,37 s. Abrir "Personagens" baixava 0,72 MB de imagens e
    agora baixa 0,10 MB. O ranking é paginado no banco: 51 mil entradas,
    ~100 ms por consulta. Ressalva: o pacote ainda tem 783 KB, porque
    dividi-lo por tela seria uma mudança grande para um ganho pequeno.
28. **Lint:** limpo (`eslint .`, o mesmo que o CI roda).
29. **Typecheck:** limpo (`tsc`), e a função do servidor passa no `deno check`.
30. **Testes unitários:** 231 passando (dos quais 18 no Postgres).
31. **E2E:** regressão de batalha em 360, 390, 430 e 1280 px; varredura de
    todas as telas em 360, 390 e 430 px; jornada ranqueada completa contra o
    servidor de verdade.
32. **Build:** passa, no CI, a cada push.
33. **Commits:** em `main` desde o início do handoff, um assunto por commit.
    Os de arte (ícones de habilidade, retratos) foram feitos em paralelo e
    integrados sem perder nada: cada vez que chegaram, a versão local foi
    reaplicada por cima e toda a verificação rodou de novo.
34. **HEAD final:** ver o fim deste documento.
35. **Deploy/status:** GitHub Pages publica a cada push, com o registro de
    deploy conferido. No Supabase estão aplicadas as quatro migrações, todas
    registradas no histórico (as duas da FASE K/L passaram antes por um
    ensaio no banco de produção, numa transação desfeita), e a função
    `ranked-api` está publicada com o Top 3 e a paginação. As duas coisas
    foram verificadas em produção com contas de teste, apagadas no fim: o
    banco está limpo, sem jogadores, partidas ou entradas de teste.

## O que fica aberto

- **Google Login** (item 19): falta a credencial do Google, que só o dono do
  projeto cria.
- **Balanceamento**: a segunda rodada (`docs/fase-d-calibragem.md`) levou o
  desvio entre personagens de 13,7 para 8,6 pontos e a amplitude entre
  famílias de 51,3 para 24,8. O Light ganhou a regra decidida pelo dono do
  jogo (um alvo de cada vez, Death Note com 70 de Investigação, imune uma vez
  só) e foi de 8% para 28%, com a Vida de 700 mantida. Fica aberto o
  **Professor Xavier** (23% a 28%): o valor dele é coordenar, e a medição não
  vê isso.
- **Limpeza do banco**: a coluna `objectives_completed` e a tabela
  `daily_weekly_progress` não são mais usadas e podem sair numa migração
  futura.
- **Arte dos personagens**: o dono do projeto está fornecendo. Em paralelo a
  esta fase entraram 110 retratos originais revisados (`27d1cbb`), gerados a
  partir de folhas de arte por `npm run assets:portraits`. Os outros 40
  personagens seguem com o retrato provisório até a semelhança ser corrigida.
