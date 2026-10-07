# FASE E · auditoria de clareza

A regra é **"BATEU O OLHO = ENTENDEU"**. A ficha de um lutador tem que ser
compreensível na primeira leitura, sem glossário e sem adivinhação.

Auditei a ficha completa dos 250 — traço, ataque básico, as três habilidades,
efeitos e fontes de Carga — e achei quatro defeitos. Nenhum deles era bug de
lógica: o jogo fazia a coisa certa e **contava errado**. Esse tipo de defeito é
o mais fácil de não ver, porque os testes passam.

## 1 · Status aplicado sem dizer que é aplicado

A ficha mostrava:

```
Lento · Ataca e prepara habilidades 20% mais devagar · 6 s
```

Lido rápido, isso parece uma descrição do personagem — "este lutador é lento".
É o contrário: ele **deixa o alvo** lento. Sem o verbo, a linha pode ser lida
como defeito próprio em vez de ataque.

Agora:

```
Aplica Lento · Ataca e prepara habilidades 16% mais devagar · 7 s
```

## 2 · Status que soma, sem dizer até quanto

Este foi encontrado pelo jogador, não por mim. A pergunta foi:

> "O buff fortalecido me parece fraco, só 3% de dano a mais. Você acha que está
> bom assim ou dá pra melhorar?"

O buff não estava fraco. A ficha estava mentindo por omissão. Fortalecido
**soma a cada aplicação**, até 80% — e a ficha mostrava só os 3% da primeira
aplicação, que lê como o efeito inteiro.

Cinco dos quatorze Status somam em vez de renovar: Exposto, Regeneração,
Queimadura, Elétrico e Fortalecido. Nenhum dos cinco dizia isso. Agora todos
dizem, com o teto em número:

```
Aplica Fortalecido · Causa +8% de dano · soma a cada aplicação, até 80% · 8 s
```

## 3 · Duas fontes de Carga que são a mesma fonte

Seis habilidades mostravam:

```
+3% por segundo enquanto estiver na luta; +2,5% por segundo
```

Duas linhas para uma coisa. O motor dispara `time` e `survived` no mesmo passo,
sem condição nenhuma, então são idênticas — e pior, a primeira sugeria uma
condição que não existe: estar na luta é o estado normal, não um requisito.

Agora: `+5,5% por segundo`.

## 4 · O gotejamento passivo vinha antes do que importa

Em 166 habilidades, o `+2% por segundo` aparecia antes da fonte que caracteriza
a habilidade:

```
antes:  +3% por segundo; +10% ao atacar
agora:  +10% ao atacar; +3% por segundo
```

Quase toda habilidade do jogo tem um gotejamento por segundo, então ele não
diferencia nada. Quem compara duas fichas lia a linha irrelevante primeiro, nas
duas. O que define a habilidade vem na frente; o gotejamento vai para o fim.

## 5 · A tela inicial dizia "100 lutadores" com 250 no jogo

Este não saiu da auditoria de texto — saiu de um print do celular. A auditoria
cobria a ficha do lutador, e esta mentira estava na tela inicial:

```
Personagens
Conheça os 100 lutadores
```

Mais duas na tela de diagnóstico: "300 habilidades" com 750 no jogo, e
"estados: 14" usando justamente a palavra que a direção proibiu — o jogo chama
de **Status**, não de estado.

Número de roster escrito à mão envelhece calado. O roster cresce, ninguém
lembra da string, e o jogo passa a mentir sem nenhum teste reclamar. Os três
agora vêm dos dados: `characters.length`, `characters.length*3`,
`Object.keys(statuses).length`.

## O que a auditoria **não** achou

As strings proibidas — "alvo válido", "efeito aplicado", "recarga interna",
nomes internos de alvo e de gatilho, `undefined`, `[object Object]` — não
aparecem em nenhuma das 250 fichas. Zero achados. Isso foi conferido, não
presumido: `scripts/auditar-clareza.ts` renderiza tudo e procura.

## Como isso fica travado

Auditar uma vez não serve de nada: o roster cresce, alguém escreve uma
habilidade nova, e a string técnica volta. Então a auditoria virou teste —
`tests/clareza.test.ts`, 14 testes sobre a ficha dos 250.

E o contrato passou a ler também o código das telas, porque foi lá que o "100
lutadores" se escondeu: um teste procura contagem de roster escrita à mão em
`src/screens` e `src/components`, nas duas formas ("300 habilidades" e
"habilidades: 300"), e outro proíbe a palavra "estado" em texto de tela. O
segundo achou um terceiro caso que eu tinha deixado passar na mesma rodada.

Um deles merece nota. Agregar fontes de Carga podia esconder Carga sem ninguém
perceber, então o teste não confere o texto: ele **soma as porcentagens que a
ficha mostra e compara com a soma nos dados**. Se a agregação perder qualquer
coisa, em qualquer um dos 250, o teste cai.

```
npx tsx scripts/auditar-clareza.ts   # a auditoria, sobre os 250
npx vitest run tests/clareza.test.ts # o contrato, no CI
```
