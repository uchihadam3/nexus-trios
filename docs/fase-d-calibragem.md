# FASE D · calibrar os 250 juntos

A direção foi explícita sobre o método: não vale comparar "dano 300 contra dano
700". Um número alto preso atrás de Preparo longo, Carga cara e condição
estreita vale menos que um número médio que sai sempre.

Então a medida aqui é a única que responde à pergunta de verdade: **com este
personagem no trio, com que frequência o trio ganha?** Instrumento:
`scripts/calibrar.ts`.

## O achado mais importante é sobre a própria medição

A primeira rodada usou 24 sementes por personagem e produziu uma lista
arrumada de "fora da curva" — três acima, seis abaixo. Eu estava a um passo de
nerfar e buffar com base nela.

Antes disso, medi o **mesmo personagem** com três conjuntos diferentes de 24
sementes:

| | amostra 1 | amostra 2 | amostra 3 | variação |
|---|---:|---:|---:|---:|
| Saitama | 50,0% | 29,2% | 54,2% | **25 pontos** |
| Tempestade | 50,0% | 33,3% | 37,5% | 17 pontos |
| Goku | 41,7% | 29,2% | 29,2% | 13 pontos |

Vinte e cinco pontos de variação sem nada ter mudado. **Com 24 sementes,
qualquer conclusão sobre um personagem isolado é sorteio.** A lista de "fora da
curva" da primeira rodada era ruído bem formatado.

O que sobrevive é o agregado por família, que junta vários personagens e
centenas de lutas. Medido a 100 sementes:

| família | vitória | lutas | intervalo |
|---|---:|---:|---:|
| evader | 21,7% | 300 | ±4,7 |
| controller | 45,2% | 500 | ±4,4 |
| predator | 57,2% | 500 | ±4,3 |
| siege | 65,0% | 400 | ±4,7 |
| tempest | 66,2% | 500 | ±4,1 |

Intervalos que não se tocam. A diferença entre famílias é real.

O instrumento agora declara o próprio erro em toda execução, e aceita
`SEMENTES=100` para quando a decisão for sobre um personagem específico.

## O que foi diagnosticado

O desequilíbrio **não é de personagem, é de arquétipo**. A correlação entre
dano médio entregue e vitória, por família, é de **0,62**.

A causa, medida: numa luta que termina quando um lado perde a Vida, só dano,
cura e Escudo convertem em vitória. Controle, engano e proteção própria não.
E as famílias de utilidade tinham **habilidades com dano zero** — o `evader`
só causava dano em uma das três. Multiplicar o dano delas por 1,9 moveu quase
nada, porque multiplicar zero continua zero. O trio virava, na prática, dois
contra três.

## O que foi corrigido, e quanto mediu

**1 · Retorno decrescente por alvo.** O handoff pediu explicitamente: *"AOE tem
valor diferente de single-target. Criar métrica explícita com retorno
decrescente por alvo e validar por simulação."* Não havia nenhuma: um dano de
300 em `allEnemies` entregava 300 a cada um dos três. Como a luta termina
quando um lado cai inteiro, espalhar dano não era só mais eficiente — era
estritamente melhor. A curva está em `RETORNO_POR_ALVO`: um alvo entrega o
valor inteiro, três entregam 2,2 vezes, não 3.

**2 · Piso de dano nas famílias de utilidade.** A habilidade continua
protegendo, prendendo ou confundindo; ela só passa a doer um pouco também. O
valor acompanha o ataque do personagem, então um rato pequeno continua batendo
como rato pequeno.

**3 · Calibragem de dano por família**, nas duas pontas.

Resultado medido: `tempest` de 76,7% para 66,2%; `evader` de 15,3% para 21,7%;
amplitude entre famílias de 65,6 para 63,9 pontos.

**Isso é um começo, não um fim.** A amplitude continua grande demais, e eu
prefiro dizer isso a apresentar três ajustes como se tivessem resolvido.

## As duas âncoras que a direção nomeou

**Saitama: validado, e não deve ser nerfado.** A direção disse que o Soco Sério
tem número alto mas não parece quebrado, porque o custo de acesso funciona. A
medição concorda: ele ficou na posição 95 de 250 na primeira rodada, dentro de
0,25 desvios da média. O número nominal não vira domínio.

**Tempestade: a simulação NÃO confirma o nerf pedido.** A direção pediu nerf
leve e cirúrgico *se a simulação confirmasse*. Ela mediu 37,5%, na posição 196
de 250 — **abaixo** da média, não acima. Repetido com sementes diferentes:
50,0%, 33,3%, 37,5%.

Não a nerfei. A percepção de que ela está acima da curva é legítima e pode
estar medindo o que a medição não pega: Lento e Enfraquecido em área são
desagradáveis de **enfrentar** mesmo quando não aumentam a chance de vitória do
time dela. Se o incômodo for o problema, o ajuste é na leitura e na duração dos
Status, não na força — mas isso precisa da sua decisão, não da minha.

## O que fica aberto

- **A amplitude entre famílias ainda é de 63,9 pontos.** Fechar isso de verdade
  exige uma das duas: o motor deixar o controle contribuir para vencer, ou as
  famílias de utilidade ganharem dano a ponto de deixarem de ser famílias de
  utilidade. É decisão de design.
- **Fortalecido acumula até +80% e a ficha diz "+3%."** Goku chega a +18% de
  pico na luta, He-Man a +68%. A mecânica está boa; o texto engana. FASE E.
- **O mesmo arquétipo rende muito diferente**: Goku e Vegeta param em +18% de
  Fortalecido, Kratos e He-Man passam de +50%.
- **Nenhum personagem foi nerfado ou buffado individualmente nesta fase**,
  porque os dados não sustentam decisão individual. Para isso, rode
  `SEMENTES=100 npx tsx scripts/calibrar.ts`.

## Segunda rodada · fechar as pontas

Medição de partida (25.000 lutas, 100 por personagem): média 50,5%, desvio de
13,7 pontos entre personagens, amplitude de 51,3 pontos entre famílias. Oito
personagens acima de dois desvios (Azula, Toph, Jill, Garou e Sr. Incrível
passavam de 80%) e oito abaixo (Xavier e Light em 17%).

**1 · Família, de novo, onde o intervalo não deixa dúvida.** counter, reaper,
tempest e siege desceram; evader, chronos, limit, saboteur, controller e
tactician subiram. O efeito foi pequeno — counter de 67,0% para 65,4% — e a
razão é instrutiva: o fator da família só toca as habilidades, e boa parte do
dano dessas famílias vem do ataque básico e da Passiva.

**2 · O piso do piso.** O piso de dano das famílias de utilidade era calculado
pelo ataque do personagem, e some em quem quase não ataca: o Xavier tem ataque
8 e causava 25, 31 e 42 de dano nas habilidades. Agora o piso usa pelo menos
40 de referência e também sobe o dano que já existe abaixo dele.

**3 · Calibragem individual por medição repetida** (`scripts/calibrar-individual.ts`,
tabela em `src/data/calibragem-individual.ts`). Um fator por personagem que
multiplica dano (básico, habilidades e Passiva), cura e Escudo, e a Vida pela
raiz. O ritmo — intervalo do básico, Carga, Preparo, Recarga — não muda. O
script mede os 250 com 200 lutas cada, mexe só em quem está fora de 38% a 62%,
empurra para dentro da faixa e não para o meio, e repete quatro vezes. Mede
todos a cada rodada, porque mexer num muda as lutas dos outros.

| | antes | depois |
|---|---:|---:|
| desvio entre personagens | 13,7 | **8,8** (8,8 com sementes novas) |
| amplitude entre famílias | 51,3 | **24,8** |
| mais forte | 85% | 70% |
| mais fraco | 14% | 23% (Xavier) |

A conferência com sementes que não serviram para escolher nada dá o mesmo
quadro: o ajuste não decorou as lutas em que foi medido.

**As âncoras.** Na primeira tentativa deixei Saitama e Tempestade de fora, e
os dois caíram para 36% e 37% — os vizinhos subiram e eles ficaram. É nerf por
tabela, que a direção proibiu para o Saitama. Agora os dois só podem subir.
Medidos com 400 lutas: **Saitama 52,3%** (fator 1,12) e **Tempestade 41,0%**,
sem ajuste. Ela media 45% antes; os intervalos se sobrepõem, então nada
confirma que ela tenha caído, e nada pede nerf.

**Anya Forger** causava 82 de dano numa luta inteira e ganhava 7%. Recebeu o
mesmo piso de dano das famílias de utilidade (`pisosIndividuais`) e o fator
por cima: 44%.

**Light Yagami: a regra, decidida pelo dono do jogo.** Ele ganhava 8%. A
causa não era número: o Light investigava primeiro os inimigos que ainda não
conhecia, espalhava a investigação pelos três, e a primeira descoberta só
saía aos 17 s — ele morria aos 20. Nenhuma combinação de Carga, Preparo e
Vida passava de 19%. A regra agora (`battle.ts`, `death-note.ts`):

- investiga **um inimigo de cada vez**, até o fim;
- com **70 de Investigação** descobre se o alvo é vulnerável ou imune (era 100);
- no **vulnerável**, a Death Note elimina;
- no **imune**, causa dano e deixa Exposto **uma vez só**; ele passa a saber,
  não usa mais nele, e começa a investigar outro.

A Vida continua 700 — "Pouca Vida" é o personagem. O fator da calibragem não
entra nele, porque levava a Vida a 1.240 e a medição passava a chamá-lo de
"Tanque". Além da regra: Investigação 40 (era 32) com Carga 8%/s, e a Death
Note com Preparo 3 s (era 5,5) e Carga 7%/s (era 4). Medido com 400 lutas:
**28,2%**. Carga mais rápida não sobe mais: com 700 de Vida ele cai por volta
dos 20 s, e esse é o preço que a direção escolheu.

**Quem é imune à Death Note.** A regra do caderno: só mata **humano** de quem
se sabe o **nome verdadeiro**. Revisada com o dono do jogo, personagem por
personagem. Imunes: deuses, demônios, mortos-vivos, alienígenas, máquinas,
brinquedos, animais, e quem não tem nome próprio (Pikachu, Agente 47, Cabeça
de Pirâmide, Doom Slayer). Metade humano conta como humano — tem nome humano
de verdade (Ravena é Rachel Roth, Invencível é Mark Grayson). Entraram como
imunes os shinigamis de Bleach, Nezuko, Muzan, Sukuna, Hiei, Power, Dio,
Freeza, Piccolo, Surfista Prateado, Lion-O, Cheetara, Loki, Frieren, Rocket,
Splinter, Mojo Jojo, Coragem e as quatro Tartarugas; passaram a vulneráveis
Mario, Genos e Ciborgue (humanos, cérebro humano), Ravena e Invencível.
Ficou **89 imunes e 161 vulneráveis** (eram 69 e 181). Com mais imunes, o
Light mediu **25,3%**.

**O Professor Xavier** está no fator máximo e ficou em 23% a 28%. Subiu de
17%, mas segue embaixo: o kit dele é coordenar o trio, e a medição não vê esse
valor. Também é decisão de design.

**Efeitos colaterais medidos e tratados.** As identidades e as metas de
Maestria saem de lutas medidas, então foram geradas de novo
(`medir-identidades`, `derivar-identidades`, `gerar-maestria`). A conquista
"Sem pressa" pedia 60 segundos com os três vivos — em 4.000 lutas sorteadas a
vitória mais longa com os três vivos durou 55, antes e depois desta rodada;
ela só acontecia num trio escolhido a dedo. Passou a pedir 45, o percentil 97
dessas vitórias. As vitórias atropeladas (três vivos) caíram de 854 para 540
em 4.000 lutas, e as viradas de 30 pontos subiram de 4,4% para 6,8% das
vitórias: as lutas ficaram mais disputadas.
