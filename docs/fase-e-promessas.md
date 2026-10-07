# Quando a ficha promete uma coisa e o combate faz outra

Esta investigação começou com uma pergunta sobre duas linhas repetidas na ficha
da Tempestade e terminou num defeito que custava uma luta inteira.

## O fio

Depois que a ficha passou a dizer **em quem** cada Status cai, a habilidade
"Relâmpago em cadeia" ficou assim:

```
Aplica Lento em todos os inimigos · 20% mais devagar · 6 s
Aplica Lento em todos os inimigos · 5%  mais devagar · 4 s
```

O mesmo Status, no mesmo alvo, duas vezes. O motor resolve Status de renovação
por `Math.max` nos dois campos, então a segunda aplicação não mudava nada: uma
linha que o jogador lê e o combate ignora.

`fundirEfeitos` existia justamente para impedir isso, e falhava por um detalhe:
comparava o alvo **cru**. Um efeito dizia `allEnemies`; o outro não dizia nada e
herdava `allEnemies` da habilidade. Como `'' !== 'allEnemies'`, os dois não
fundiam — embora em combate acertassem exatamente as mesmas pessoas. Quatro
habilidades escapavam assim.

## O que estava embaixo

Resolver o alvo antes de comparar consertou as quatro. Mas a mesma pergunta —
*em quem este efeito cai de verdade?* — aplicada aos 250 encontrou algo bem
maior.

`applyEffects` faz `effect.target ? targets(...) : selected`. Um efeito sem alvo
próprio cai em quem a **habilidade** mirou. Para uma habilidade de ataque, é o
certo. Para uma de apoio, é o contrário:

```
Sakura · "Byakugou"  (alvo da habilidade: allAllies)
   heal   130  → allAllies
   regen   12  → allAllies
   strengthened .1 → allAllies
   damage 306        ← sem alvo próprio: herda allAllies
```

**306 de dano no próprio trio**, toda vez. O Piccolo marcava e enfraquecia o
aliado que a habilidade estava tentando proteger. São 80 efeitos em 250
personagens, todos no mesmo sentido, porque o descuido é sempre o mesmo:
habilidade de apoio com um efeito ofensivo junto.

Medido em 30 lutas com Sakura, Piccolo e Ichigo no mesmo trio:

```
antes:  71 golpes no próprio time · 16.158 de dano · 46 debuffs em aliado
depois:  0 golpes                 ·      0 de dano ·  0 debuffs em aliado
```

A ficha nunca prometeu isso. Ela diz "306 de dano", e ninguém lê isso como "no
meu próprio trio".

## O que não foi tocado

Quinze efeitos ofensivos miram `self` **explicitamente**, e os quinze combinam
com a ideia escrita do personagem: o traço da Sailor Moon se chama "Preço do
cuidado" e cura o aliado ferindo ela; o Akuma "mata rápido porque não sobrevive
a uma luta longa" e fica Exposto ao soltar o Shun Goku Satsu.

A distinção que o auditor aprendeu é entre **escolher** e **herdar**. Mirar
`self` é decisão de quem escreveu. Cair num aliado por falta de alvo próprio é
descuido. Ferir o trio inteiro de propósito nunca é custo.

## O efeito no equilíbrio

Isto é correção de defeito, não balanceamento — mas quem parou de se derrotar
sozinho ficou mais forte, e o número importa. Medido a 200 lutas por
personagem, com a mesma regra de sorteio antes e depois:

| | antes | depois | mudança |
|---|---|---|---|
| Sakura Haruno | 29,5% | 61,5% | **+32,0** |
| Edward Elric | 38,0% | 57,5% | **+19,5** |
| Piccolo | 28,0% | 26,0% | −2,0 |
| Ichigo Kurosaki | 42,5% | 43,5% | +1,0 |
| Itachi Uchiha | 35,5% | 36,0% | +0,5 |
| Zenitsu Agatsuma | 57,5% | 59,0% | +1,5 |

A margem de uma medida individual a 200 lutas é de ±7 pontos, então só as duas
primeiras mudaram de verdade; as outras quatro estão dentro do ruído. Piccolo
continua fraco — ele já era antes da correção, e isso é assunto da calibragem,
não deste conserto.

Sakura a 61,5% e Edward a 57,5% agora estão **acima** da curva. Entram na lista
da próxima rodada de balanceamento, do lado oposto ao que estavam.

## As outras formas do mesmo defeito

Ao abrir a auditoria, procurei toda divergência entre o que a ficha mostra e o
que o motor executa, não só esta:

- **linha morta** — Status de renovação dominado por outro na mesma habilidade
- **passa do teto** — intensidade escrita acima do `cap`, que o motor corta
  (Muzan anunciava Regeneração 28 com teto 25)
- **lado errado** — ofensivo em aliado, apoio em inimigo
- **valor zero**, **duração zero** — efeito que não faz nada
- **nunca fica pronta** — habilidade sem nenhuma fonte de Carga
- **corrente quebrada** — `requiresSkills` apontando para fora, ou para si mesma

Hoje: **zero achados em todas**.

Duas dessas checagens acusaram errado na primeira versão e precisaram ser
corrigidas, não os dados. `requiresSkills` guarda **índices**, não ids — o motor
faz `f.skills[index]` — e minha comparação com `skill.id` acusou dez
personagens inocentes. Vale repetir porque é o mesmo erro de sempre: antes de
chamar algo de bug, confirmar o que o motor faz.

## O que ficou travado

`tests/promessas.test.ts` — oito testes, o último deles jogando 30 lutas de
verdade e cobrando zero dano e zero debuff no próprio time. Os sete anteriores
leem os dados; esse não depende da minha leitura estar certa.

E uma duplicação virou fonte única. "O que é Status positivo" existia em duas
listas, em arquivos diferentes, nenhuma derivada da outra: `positiveStatuses` na
apresentação e `negativeStatuses` no motor. Enquanto as duas estiverem certas
ninguém percebe; no dia em que um Status novo entrar numa e não na outra, elas
discordam em silêncio — e esta correção depende exatamente disso para decidir
em quem um efeito cai. Agora o tom mora em `data/statuses.ts`, junto do Status,
e as duas listas derivam dele.

```
npx tsx scripts/auditar-promessas.ts   # a auditoria sobre os 250
npx vitest run tests/promessas.test.ts # o contrato, no CI
```
