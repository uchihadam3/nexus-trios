# FASE G · o Raio-X do Trio

O documento da direção pede que, **depois de toda batalha, ganhando ou
perdendo**, o jogador aprenda alguma coisa sobre a combinação que montou. Sem
parede de texto: três retratos e as conexões, nas seis direções (A→B, A→C,
B→A, B→C, C→A, C→B).

E põe o limite em cinco palavras: **não inventar causalidade que não
aconteceu**.

## O que existia

`RunSynergyEvent` media uma coisa só — Carga passada entre aliados — e a tela
de resultado dizia "a ligação mais frequente ajudou um aliado N vezes". É
verdade, mas é um canal de doze.

## O que o Raio-X sabe agora

Cada elo nasce de eventos que o motor de fato emitiu. Nenhum é inferido do
desenho dos personagens:

| elo | o que o prova |
|---|---|
| **carga** | evento `synergy`, que o motor emite nomeando o aliado que causou o ganho |
| **cura** | evento `heal` de A para B, os dois do trio |
| **escudo** | evento `shield` de A para B |
| **aceleração** | Status `haste` aplicado por A em B |
| **reforço** | qualquer Status positivo de A em B |
| **preparo protegido** | `protected` que A pôs em B **enquanto B estava no Preparo** |
| **alvo preparado** | A deixou o inimigo Exposto/Marcado/Eletrificado/Enfraquecido, e B bateu nele **com o Status ainda vivo** |
| **finalização** | o mesmo, e o golpe de B derrubou o inimigo |
| **controle** | A travou um inimigo **que estava preparando uma habilidade** |

Os três últimos dependem de o Status estar ativo na hora do golpe. A única
forma honesta de responder isso era saber a duração real, então o motor passou
a registrá-la no próprio evento — a alternativa seria uma janela de tempo
arbitrária, que é inventar causalidade com outro nome.

O acumulador roda **durante** a luta, alimentado com os eventos de cada quadro.
Isso não é preferência: `battle.events` guarda só os 180 últimos, e uma leitura
feita no fim já teria perdido o começo da batalha.

## A classificação, calibrada

A escala é a do documento: ÓTIMA CONEXÃO, BOA CONEXÃO, POUCA CONEXÃO,
INDEPENDENTES, CONFLITO.

A primeira versão usou cortes escolhidos a dedo, e 360 pares medidos em 120
lutas saíram assim: **56% "ÓTIMA CONEXÃO"**. É o mesmo defeito que a FASE F
achou nas etiquetas — um rótulo que descreve a maioria não separa ninguém.

Medida a distribuição real da força de um par (p10 = 4, mediana = 16, p75 = 41,
p90 = 84), os cortes passaram a seguir essa régua:

| | antes | agora |
|---|---|---|
| ÓTIMA CONEXÃO | 56% | **12%** |
| BOA CONEXÃO | 28% | 37% |
| POUCA CONEXÃO | 12% | 48% |
| INDEPENDENTES | 3% | 3% |
| CONFLITO | 0% | 0% |

E a regra que o documento deixou escrita — *"não chamar dupla neutra de ruim"* —
está na escrita: um par sem elos é **INDEPENDENTES**, com a legenda "lutaram
bem, cada um por si. Não é problema."

## Sobre o CONFLITO: zero, e por um bom motivo

A detecção está implementada — Status negativo saindo de um aliado para outro —
e não encontra nada em 120 lutas.

Não é omissão. Depois que a FASE E corrigiu os 80 efeitos ofensivos que
herdavam alvo aliado, **nenhum personagem prejudica um companheiro**. O único
jeito de um lutador atingir o próprio lado é a Confusão, e o motor a resolve
mandando o golpe nele mesmo, nunca num aliado; os quinze custos declarados
também miram sempre `self`.

A detecção fica porque é barata, e porque no dia em que alguém escrever uma
mecânica de fogo amigo o Raio-X vai contar em vez de ficar calado. O teste
cobra zero hoje — se virar um, é notícia.

## O que a tela mostra

Três linhas, uma por par. Em cada uma: os dois retratos, o selo da
classificação, e no máximo uma frase por direção — a conexão mais forte que
aconteceu de verdade.

```
Pikachu  ↔  Tempestade          [ÓTIMA CONEXÃO]
   Pikachu    → travou 3 Preparos inimigos e deu tempo a Tempestade
   Tempestade → abriu o alvo e Pikachu bateu 6 vezes
   Um ativou o outro o tempo todo.

Tempestade segurou a pressão: 1.207 de dano recebido, 39% de tudo que o trio levou.
```

Quando uma direção não tem elo nenhum, a linha simplesmente não aparece. Dizer
"não ajudou" seria transformar ausência em julgamento.

## O contrato

`tests/raio-x.test.ts`, 17 testes. Os que importam:

- todo elo liga dois lutadores **diferentes** do **próprio** trio;
- elo de cura exige evento de cura, de escudo exige escudo, de carga exige
  sinergia, de finalização exige abate;
- a contagem **bate exatamente** com o número de eventos — nem um a mais;
- o acumulador é puro e determinístico: não altera o que recebe, e a mesma
  entrada dá sempre a mesma saída;
- a frase de cada direção vem de um elo daquela direção;
- sem elo nenhum, o par é INDEPENDENTES e nenhuma frase é inventada;
- "ÓTIMA CONEXÃO" fica abaixo de 30% dos pares, e acima de zero;
- CONFLITO é zero enquanto não houver fogo amigo.

```
npx tsx scripts/medir-raiox.ts     # a distribuição das cinco classes
npx vitest run tests/raio-x.test.ts
```
