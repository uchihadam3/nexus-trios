# FASE H · conquistas, Maestria e Progresso

O documento pedia quatro coisas: Objetivos, Conquistas, Maestria e a tela de
Progresso. Durante a fase a direção mudou uma delas:

> "Esses objetivos são ruins, tira isso, deixa só as conquistas e deixe
> interessante e divertido de conseguir."

Este documento registra o que foi feito e por quê, incluindo a parte removida.

## Por que os Objetivos saíram

Eram três grupos — da jornada, diários e semanais — e cada um tinha um
problema diferente:

- **Diários e semanais são um calendário.** Expiram se você não jogar hoje.
  Isso funciona num jogo de serviço com servidor; aqui é um jogo que se abre
  quando dá vontade, e um calendário vira cobrança.
- **Os da jornada somem com a jornada.** Você cumpre "interrompa 2
  preparações", ganha 110 XP, e não fica registro nenhum. Não vira história.
- **Os três pediam o que as conquistas pedem, só que pior.** Vencer com os três
  de pé, interromper Preparos, aplicar Status, curar, bloquear — tudo isso
  virou conquista, e conquista fica.

Havia uma guarda decente: `capable()` impedia objetivo impossível, então um
trio sem curandeiro nunca recebia "cure 500". O problema não era descontrole;
era que mesmo controlados eles eram contadores.

**O que a remoção mexeu no ranqueado:** a qualidade de uma jornada ranqueada
somava 12.000 pontos por objetivo cumprido, até 36.000. Esse componente saiu.
A pontuação agora é o que a jornada mostrou: confrontos vencidos, Vida restante
e lutadores de pé. A coluna `objectives_completed` ficou sem uso e sai na
migração `20261009000000_limpeza_objetivos.sql`, junto com a tabela
`daily_weekly_progress`.

## As conquistas, refeitas

As cinquenta antigas eram degraus de contador: vença 1, 10, 30, 100, 250;
bloqueie 100, 1.000, 5.000, 20.000, 60.000. Nada ali pede que você jogue
melhor, só que jogue mais.

As 52 novas são de **momento**:

| antes | agora |
|---|---|
| `protection >= 60000` | **Um golpe só** — acerte 600 num golpe |
| `wins >= 250` | **No fio da navalha** — vença com alguém abaixo de 5% de Vida |
| `journeys >= 75` | **Serviu na bandeja** — abra o inimigo e deixe o aliado derrubar |
| `healing >= 60000` | **Carregou nas costas** — vença com um causando mais dano que os outros dois juntos |

Dez categorias, como o documento lista, e seis secretas que só revelam a dica
depois de conquistadas.

### Três eram impossíveis, e a simulação provou

Escrever conquista de momento é fácil; escrever uma que **acontece** não é.
Rodei 191 lutas e 10 nunca dispararam. Medindo as faixas reais:

| conquista | pedia | o que o jogo permite |
|---|---|---|
| Sem chance | Vantagem ≥ 80 no fim | máximo observado: **72** |
| Ninguém dava nada | 60 pontos atrás | atraso máximo numa vitória: **56** |
| Só na mão | vencer sem habilidade sair | **0 em 211 vitórias** — elas saem sozinhas |
| Pelas beiradas | maior golpe ≤ 150 | o trio mais fraco ainda bate **312** |

As duas primeiras viraram 65 e 45. As duas últimas foram substituídas por
"Carregou nas costas" e "Sem pressa".

"Trio afinado" tinha o problema oposto: disparava em 96% das lutas. Agora exige
mão dupla nos três pares.

As sete restantes que não dispararam eram artefato de sorteio, não
impossibilidade — um trio sorteado quase nunca é do mesmo universo nem tem três
curandeiros. `scripts/provar-conquistas.ts` as verifica com cenários
construídos, e **as 52 estão provadas alcançáveis**.

## A Maestria dos 250

O documento pede três desafios por personagem, "pelo menos 2 dos 3 ligados à
mecânica real", e proíbe "jogue 50 partidas". Os que existiam eram, para todo
mundo:

```
I   · Ative <habilidade 1> em uma batalha
II  · Use <habilidade 3> 2 vezes
III · Vença uma Jornada e ative <habilidade 3> 3 vezes
```

Os três medem a mesma coisa — quantas vezes um botão saiu. É o "jogue 50
partidas" com o nome da habilidade colado em cima.

Agora cada um é um feito, escolhido pelo que o kit permite e **dimensionado
pelas 10.000 lutas que a FASE F mediu**:

```
Sakura Haruno   II  Devolva 760 de Vida ao trio
                III Encha 230% de Carga dos seus aliados
Saitama         II  Absorva 320 de dano com Escudo
                III Acerte um único golpe de 1.400 de dano
Pikachu         II  Corte 4 Preparos inimigos
                III Mantenha inimigos travados por 16 segundos no total
```

500 dos 750 desafios são mecânicos — exatamente 2 de 3. Um personagem que
nunca curou não recebe desafio de cura: a mesma guarda que o documento exigia
dos Objetivos, pelo mesmo motivo.

## A tela

Três abas em vez de quatro: Conquistas, Maestria, Estatísticas. O topo mostra
Nível Nexus, XP, % do elenco experimentado e lutadores dominados.

XP continua sendo prestígio — nível e título. Nenhum ponto altera atributo de
personagem, e um teste cobra isso.

## O contrato

`tests/progression.test.ts`, 14 testes:

- 750 desafios, três por personagem, nos três degraus;
- **2 de 3 mecânicos**, e os dois mecânicos pedem feitos diferentes;
- nenhum desafio pede o que o kit não alcança;
- o grau para no primeiro degrau não cumprido;
- **as 52 conquistas são alcançáveis jogando** — o teste joga, não lê;
- nenhuma conquista é entregue duas vezes;
- XP não mexe em atributo;
- o perfil antigo migra sem perder recordes, e os objetivos não voltam
  disfarçados.

```
npx tsx scripts/gerar-maestria.ts      # regenera os 750 desafios
npx tsx scripts/provar-conquistas.ts   # a varredura + os cenários construídos
npx vitest run tests/progression.test.ts
```
