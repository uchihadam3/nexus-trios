# Nexus Duel — revisão de linguagem e gamificação

## A. Vocabulário

| Anterior | Interface atual |
| --- | --- |
| Condição/HP | Vida |
| Domínio | Vantagem |
| campanha | jornada |
| cooldown | Recarga |
| cast | Preparo |
| alvo válido, condição de uso | Alvo, Usa quando |
| efeito aplicado, texto flutuante de carga | consequência no alvo e medidor de Carga |

O motor preserva identificadores internos (`dominion`, `winning`, `losing`, `hp`) para manter os saves e a simulação. A interface explica que Vantagem altera algumas fontes de Carga, mas não decide a vitória.

## B. Status

| Status | Sinal | Efeito exibido |
| --- | --- | --- |
| Protegido | Positivo | Reduz dano; a partir de 30%, impede interrupção do Preparo |
| Acelerado | Positivo | Acelera ataque e Preparo |
| Regeneração | Positivo | Recupera Vida por segundo |
| Fortalecido | Positivo | Aumenta dano causado |
| Exposto | Negativo | Aumenta dano recebido |
| Marcado | Negativo | Aumenta dano recebido e favorece a escolha como alvo |
| Lento | Negativo | Retarda ataque e Preparo |
| Preso | Negativo | Retarda ataque e Preparo em uma camada separada de Lento |
| Eletrificado | Negativo | Aumenta dano recebido |
| Paralisado | Negativo | Impede ataques e avanço do Preparo |
| Confuso | Negativo | 25% de chance de o ataque básico atingir o próprio lutador |
| Queimando | Negativo | Perde Vida por segundo |
| Silenciado | Negativo | Impede iniciar novas habilidades |
| Enfraquecido | Negativo | Reduz dano causado |

Os números e durações vêm de cada kit. Exposto e Eletrificado têm o mesmo tipo de multiplicador de dano recebido, com limites de intensidade diferentes. Preso e Lento usam camadas separadas que se acumulam. Esses nomes continuam distintos porque os kits, durações e limites são distintos; não houve rebalanceamento.

## C. Cem personagens

O catálogo tem 100 IDs únicos, cada um com ataque básico, Traço e três habilidades. A ficha agora deriva efeitos, alvos, fontes de Carga, condição de uso, Preparo, Recarga, Vida, intervalo e Inteligência diretamente dos objetos do motor. As 100 fichas são renderizadas em teste e verificadas contra a quantidade de efeitos/regras dos próprios kits; a apresentação não depende dos antigos parágrafos livres de habilidade. Pontos de atenção continuam editados individualmente no catálogo. Corrigidos termos públicos desatualizados, inclusive a frase de Gojo sobre seu Preparo. Não foi necessário mudar o dano ou a duração dos outros kits.

## D. Light

Cada adversário começa desconhecido. Ao atingir 100 Investigação, a batalha registra e mostra Vulnerável à Death Note ou Imune à execução; o conhecimento permanece até o fim. A IA prefere investigar desconhecidos, prepara a execução contra um vulnerável conhecido e usa a alternativa apenas se todos os adversários vivos forem conhecidos como imunes. A Death Note ainda exige 100 Investigação, 100% de Carga e 5,5 s de Preparo. Contra imune, causa 110 de dano e Exposto 55% por 14 s. A ficha geral não revela compatibilidade. Testes cobrem revelação, memória, alvos, alternativa e Carga por Status negativo no inimigo.

## E. Batalha

A carga deixou de gerar frases flutuantes. Dano, cura, Escudo, Status, habilidade pronta, descoberta e saída da luta aparecem associados ao lutador ou ao histórico compacto. O painel rápido explica fonte, duração e valores. O guia inicial pode ser percorrido ou pulado; as seis fichas cabem na largura de 360, 390 e 430 px.

## F. Vantagem

Substitui Domínio no HUD, guia, fichas, descrição de Carga e resultado. Regras `winning` e `losing` continuam ligadas à posição real do medidor. Vantagem não encerra a batalha: a vitória vem da eliminação do trio rival. Testes do motor cobrem as fontes e a ausência de vitória por tempo/medidor.

## G. Jornada

Home mostra trio, progresso e acesso às áreas. Personagens traz filtros e papéis derivados dos efeitos. Draft mostra papel, Traço, ponto de atenção e composição do trio. Batalha tem tutorial, histórico legível e painel contextual. Resultado mostra destaques condicionais, métricas e trajetória. Como Jogar ensina mecânicas e todos os Status com exemplos. Configurações agrupa áudio, visual, jogo e ajuda, inclusive reinício do guia.

## H. Verificação

`npm run lint`, `npm run typecheck`, `npm test -- --run` (70 testes em 7 arquivos) e `npm run build` passaram. O roteiro Playwright abriu Home, guia, ficha do Light, Draft e Batalha em 360/390/430 px sem erros de página ou rolagem horizontal. Testes cobrem renderização das 100 fichas, 14 Status, motor do Light e ausência da caixa flutuante de Carga. A regressão de batalha e o deploy serão anotados na publicação.

## I. SFX/VFX

A reconstrução profunda de SFX/VFX foi deixada para outra rodada, conforme pedido. A simplificação desta etapa remove somente a frase de Carga e reduz chamadas repetitivas de ação básica para melhorar a leitura.

## J. Publicação

Preencher com o commit e a execução do GitHub Pages após a publicação.
