# FASE F · as identidades públicas, refeitas

O documento da direção pedia **2 a 4 identidades públicas realmente relevantes**
por personagem, de uma taxonomia de cerca de 23 termos, derivadas por
**mecânica + simulação + override manual** — e proibia duas coisas por escrito:
*"Cura por cura incidental"* e *"Dano só porque ataque básico machuca"*.

## O que havia antes

`rolesFor` marcava uma função se **existisse** um efeito daquele tipo na ficha,
e mostrava as três primeiras numa ordem fixa. A medição, registrada em
`fase-f-brief.md`:

| | antes | agora |
|---|---|---|
| termo mais comum | **Dano, 250 de 250 (100%)** | Especialista, 54 (22%) |
| combinações distintas | **16** para 250 lutadores | **216** |
| combinação mais repetida | 64× | 4× |
| personagens com identidade cortada | **114** | 0 |
| identidades por personagem | até 3 | 2 a 4, média 3,8 |

## O método

### A simulação

`scripts/medir-identidades.ts` põe cada personagem em 40 lutas 3 contra 3 —
10.000 lutas no total — e observa os eventos do combate, não a ficha: quanto
dano saiu e de que tamanho foi o maior golpe, quanto acertou vários alvos ao
mesmo tempo, quantos segundos de controle duro aplicou, quanto curou nos outros
e em si, quanto apanhou e por quanto tempo continuou de pé, e se venceu lutas
em que o trio esteve atrás.

### A comparação

`scripts/derivar-identidades.ts` transforma cada medida num **percentil dentro
do elenco inteiro**. É isso que resolve as duas proibições de uma vez: como
todo mundo causa dano, causar dano não rende etiqueta nenhuma — rende "Pressão"
quem causa muito **e** de forma constante, e "Explosão" quem concentra num
golpe só.

Dois erros ao longo do caminho, que vale registrar porque ambos eram o mesmo
erro visto de ângulos diferentes:

1. **Comparar com o grupo errado.** A primeira versão comparava cada um só com
   quem tinha a mesma capacidade: a fila dos curandeiros entre curandeiros.
   Treze personagens curam aliados; exigir que estivessem entre os 28% melhores
   **desses treze** deixou "Cura" com dois donos em 250. Mas curar aliado já é
   raro — uma capacidade que 13 de 250 têm é um ótimo distintivo por si só.
   Comparando contra o elenco inteiro, os treze passam, e uma capacidade comum
   continua exigindo destaque.
2. **Cortar pela nota, não pela informação.** A segunda versão ordenava por
   evidência bruta e cortava em quatro — e repetiu exatamente o defeito que
   esta fase existia para consertar: a Sailor Moon tinha "Cura" com evidência
   0,85 e perdia a vaga para termos comuns com nota um pouco maior. Evidência
   alta não é a mesma coisa que informação: um termo que 96 personagens têm diz
   pouco sobre qualquer um deles. Agora a ordem é **evidência × raridade**.

### Os overrides

Quatro personagens vieram com identidade escrita no documento, e os quatro
estão aplicados. Onde a simulação discorda, a divergência fica registrada,
porque uma delas é informação sobre o jogo e não sobre o texto:

| personagem | o documento diz | a simulação mediu |
|---|---|---|
| Saitama | Explosão · Finalização · Sobrevivência | Preparação, Virada, Proteção |
| Tempestade | Área · Controle · Debuff · Ritmo | Dano contínuo, Ritmo, Área, Debuff |
| Wolverine | Pressão · Regeneração · Sobrevivência | Regeneração, Tanque, Sobrevivência, Buff |
| Professor Xavier | Suporte · Controle · Ritmo | Interrupção, Carga, Suporte, Buff |

A do Saitama merece atenção na calibragem: ele recebe "Sobrevivência" por ser
quem é, e a simulação diz que ele **morre em 77% das lutas**. Isso não é um erro
de etiqueta, é um personagem que não está fazendo o que deveria.

A da Tempestade é mais branda: o que a ficha dela chama de controle é Lento e
Enfraquecido, que o sistema classifica como Ritmo e Debuff. Controle duro —
prender, paralisar, silenciar, confundir — ela não tem.

## Um termo a menos

A taxonomia proposta tinha 23 termos; este sistema usa 22. **"Invocação" ficou
de fora porque o motor não tem invocação**: nenhum efeito cria um lutador novo
no campo. Dar a etiqueta a quem aplica muitos Status, ou a quem tem tema de
invocar, seria exatamente a tag incidental enganosa que a direção mandou não
criar. Se a mecânica existir um dia, o termo entra com ela.

## Onde aparecem

Como o documento pede, as mesmas identidades em todo lugar:

- **Draft** — nas três cartas, no destaque, e em "Seu trio ganha + Interrupção
  + Virada", que é o que aquele candidato acrescenta ao que o trio já tem;
- **Lacunas do trio** — "Pouca proteção", "Pouca recuperação", "Pouca
  interrupção", "Pouco dano concentrado", cada uma dita **só quando nenhum dos
  três cobre aquilo**. Um trio com curandeiro não ouve que lhe falta
  recuperação;
- **Personagens** — nas cartas e no filtro, que agora filtra por identidade;
- **Ficha** — sob o nome, com a explicação de cada termo ao passar o mouse. A
  ficha era o único lugar que não as mostrava: o jogador via a etiqueta no
  Draft, abria a ficha para entender, e não encontrava nada.

## O contrato

`tests/identidades.test.ts`, 15 testes:

- 2 a 4 por personagem, sem repetição, cobrindo os 250;
- só termos da taxonomia, cada um com explicação e família;
- **nenhum termo em mais de 35% do elenco** — o teste que o sistema antigo
  falharia com 100%;
- mais de 150 combinações distintas, nenhuma repetida mais de 8 vezes;
- quem tem "Cura" cura aliado de verdade; quem tem "Interrupção" interrompe;
  quem tem "Carga" enche Carga do trio;
- as quatro âncoras do documento;
- as lacunas do Draft só aparecem quando são verdade.

```
npx tsx scripts/medir-identidades.ts    # 10.000 lutas  (alguns minutos)
npx tsx scripts/derivar-identidades.ts  # gera src/data/identidades.ts
npx vitest run tests/identidades.test.ts
```
