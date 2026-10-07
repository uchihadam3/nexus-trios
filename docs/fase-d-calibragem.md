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
