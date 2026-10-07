# FASE F · o que medir antes de reconstruir as identidades

A FASE E auditou a escrita. Ao chegar no Draft, ela esbarrou num problema que
não é de redação e sim de desenho: as etiquetas de função. Este documento é a
medição, para a FASE F começar de números e não de impressão.

## O que as etiquetas dizem hoje

`src/presentation/roles.ts` deriva até três funções por personagem olhando
apenas se **existe** um efeito de cada tipo. Nos 250:

| função | quantos têm | % |
|---|---|---|
| Dano | 250 | **100%** |
| Controle | 150 | 60% |
| Proteção | 106 | 42% |
| Ritmo | 104 | 42% |
| Cura | 56 | 22% |
| Finalização | 44 | 18% |

**"Dano" está em todos os 250.** Toda carta do Draft gasta uma das três vagas
com uma etiqueta que é verdade para qualquer escolha — ou seja, que não ajuda a
escolher. A causa é simples: todo personagem tem ataque básico, e o ataque
básico causa dano.

## Só 16 combinações para 250 personagens

| aparece | combinação |
|---|---|
| 64× | Dano + Controle + Ritmo |
| 51× | Dano + Proteção + Controle |
| 32× | Dano + Proteção + Cura |
| 17× | Dano + Proteção + Ritmo |
| 15× | Dano + Controle + Finalização |
| 12× | Dano + Ritmo + Finalização |

O Draft mostra três cartas e pede uma escolha. Com 16 rótulos possíveis, duas
das três frequentemente aparecem idênticas — e o jogador escolhe no retrato,
não na função.

## O corte em três silencia justamente o que distingue

`roles.slice(0,3)` corta numa ordem fixa, e a ordem põe "Dano" em primeiro.
**114 dos 250 perdem pelo menos uma função** por esse corte:

| função silenciada | vezes |
|---|---|
| Finalização | 71 |
| Ritmo | 54 |
| Controle | 13 |

"Finalização" é a função mais rara do jogo (18%) e portanto a que mais
distingue — e é a mais silenciada. Quem é finalizador quase nunca mostra isso.

## O cálculo ignora o alvo e a quantidade

Duas falhas no critério, além do corte:

1. **Ignora o alvo.** `has(e => e.kind === 'damage')` conta dano em si próprio.
   A Sailor Moon, cuja ideia escrita é "levanta o trio e limpa o que gruda
   nele", é rotulada "Dano + Proteção + Cura" — e o dano dela é o custo que
   ela paga, não o que ela entrega.
2. **Ignora a quantidade.** Um personagem com um único Lento de 5% por 4 s
   recebe "Ritmo" igual a quem para a luta inteira. Presença não é relevância.

## O que a FASE F precisa produzir

O handoff pede **2 a 4 identidades honestas por personagem**, de uma taxonomia
de cerca de 23 termos. Pelos números acima, "honesta" precisa significar três
coisas ao mesmo tempo:

- **Discriminante** — uma identidade que 100% dos personagens têm não é
  identidade. Nenhum termo deve passar de uns 60% do elenco.
- **Medida, não presumida** — derivada do que o personagem entrega numa luta
  (dano por segundo, cura, proteção, tempo de controle), comparada com a
  mediana do elenco, e não da mera existência de um efeito.
- **Com alvo** — o que ele faz ao inimigo, o que faz pelo trio e o que custa a
  ele próprio são três coisas diferentes.

E o critério de aceitação deve ser verificável, como foi nesta fase: nenhum
termo acima de X% do elenco, nenhuma combinação repetida mais de Y vezes,
nenhum personagem com identidade silenciada por corte.

## O que não é problema

`draftConnection` é honesto. Ele só afirma "BOA CONEXÃO" quando existe um
efeito de apoio mirando `allAllies` ou `allyWeak`, e nomeia quem ajuda quem com
o quê. Nesta auditoria ele só ganhou precisão: um efeito que alcança o trio
inteiro dizia o nome de um aliado só, e agora diz "o trio todo".
