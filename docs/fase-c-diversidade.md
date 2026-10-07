# FASE C · auditoria de diversidade mecânica dos 250

A direção escreveu a regra por extenso: *"250 personagens não podem ser 250
skins. Se remover nome e retrato de dois personagens e os kits parecerem iguais
com números diferentes, um deles precisa ser diferenciado."*

O teste de assinatura que já existia garante que nenhum par é **idêntico**.
Isso é o piso, e não é o que a regra pede. Identidade exata é fácil de evitar;
semelhança não. Esta fase mediu a semelhança.

Instrumento: `scripts/auditar-diversidade.ts`. Ele mede, não conserta, e sai
com código 1 quando acha algo que precisa de decisão humana.

## O que foi medido, e o resultado

| | antes | depois |
|---|---:|---:|
| Pares mecanicamente parecidos demais (31.125 comparados) | **16** | **0** |
| Habilidades que nunca saem | **7** | **0** |
| Traços que nunca disparam | **14** | **0** |
| Controle perpétuo | 0 | 0 |

Vitórias do lado do jogador: 48,1% antes, 48,5% depois. Duração média da luta:
376 passos antes, 353 depois. As correções não desestabilizaram o combate.

## 1 · O defeito de motor: catorze traços que nunca aconteciam

O motor tem duas funções. `gain()` dá Carga. `trigger()` dá Carga **e** dispara
o traço. Quatro tópicos passavam só pelo `gain()`: `enemyHurt`, `winning`,
`losing` e `survived`.

O tipo `Topic` permite declarar um traço em qualquer um deles, e a ficha
mostrava o texto normalmente. O traço simplesmente não acontecia.

Catorze personagens tinham traço morto por isso, e não eram só os novos:

- **Aquaman**, **Galactus**, **Ganondorf**, **Eric Cartman** — `winning`
- **Megumi**, **Sung Jinwoo**, **Sephiroth**, **Doom Slayer**, **Akuma**,
  **Arthas**, **Beerus**, **Omni-Man**, **Azula** — `enemyHurt`
- **Eren Yeager** — `losing`

Correção: os quatro tópicos passam pelo `trigger()`. O `traitTimer` já limita a
frequência, e todos os traços afetados têm recarga de um segundo ou mais, então
`survived`, `winning` e `losing` — que ocorrem a cada passo — não viram disparo
a cada passo.

## 2 · Quatro habilidades com trava estrutural

Não era custo alto. Era desenho que se mordia.

**Geralt de Rívia — Sinal de Quen.** Dependência circular, e introduzida por
mim. O Quen carregava com `protected`, que é dano **bloqueado**, e é o Quen que
dá o escudo. Sem escudo não há bloqueio, sem bloqueio não há Carga, sem Carga
não há Quen. O traço "Sinais" morria pelo mesmo motivo. Agora o Quen carrega
com o dano **recebido**, que é quando um bruxo de verdade o levanta.

**Pica-Pau — Risada irritante.** A primeira habilidade mirava `enemyCast` e
carregava do mesmo evento: duas travas no mesmo gatilho, na habilidade que
deveria ser a mais acessível das três. Passou a mirar a maior ameaça.

**Seto Kaiba — Ultimate Burst.** Três travas: exigia a habilidade anterior,
exigia alvo vulnerável, e carregava só de `winning`. A carga passou a vir do
dano causado, com `winning` como reforço.

**Mewtwo — Tempestade mental.** Pedia Preparo inimigo na carga, na condição e
no alvo — o mesmo gatilho três vezes. Passou a alcançar o campo inteiro.

## 3 · Dezesseis pares parecidos demais

O padrão era sempre o mesmo: personagens que dividem estilo e cujo ajuste mexia
só no ultimate. Traço e primeiras habilidades continuavam idênticos — e é ali
que a luta passa a maior parte do tempo.

Os agrupamentos encontrados, por estilo: precisão (Tanjiro, Ciclope, Samurai
Jack, Leon — seis pares sozinhos), velocidade (Mikasa, Wesker), invocação
(Megumi, Jinwoo), trapaça (Loki, Bart, Aizen), aposta (Arlequina, Peter),
armadilha (Nobara, Duende Verde), mira (Samus, Buzz), cerco (Hades, Megatron),
guarda (Groot, Gaara) e limite (Popeye, Homer).

A correção mudou o **traço** e uma habilidade de entrada de cada um, porque é o
traço que diz quem o personagem é quando nada de especial está acontecendo.

Par mais próximo depois da correção: Aquaman ~ Eric Cartman, a 0,0822 — acima
do limite de 0,08.

## 4 · Duas medições minhas que estavam erradas

Registradas porque uma auditoria que publica achado falso é pior que nenhuma.

**"220 traços mortos" (88% do elenco).** Implausível demais para publicar. Eu
procurava um evento com o nome do traço, e o motor nunca emite isso — quando um
traço dispara ele chama `applyEffects` direto. Trocado por observar o
`traitTimer`: 220 → 14 reais.

**"29 controles perpétuos".** Eu comparava a duração do Status com a recarga da
habilidade. Mas quem limita uma habilidade é a **Carga**, não a recarga: uma
skill com recarga de 3 s que precisa de 100 de Carga pode sair uma vez a cada
vinte segundos. Trocado por medir quanto tempo o inimigo passa de fato travado:
29 → 0, com trava média de 8% no catálogo.

**"Vazio Infinito do Gojo nunca sai".** Medido à parte em quarenta lutas, ele
chega a 100 de Carga em seis e é lançado em cinco. Raro, não morto. O
instrumento passou a usar vinte sementes e a separar *morto* de *raro*.

## O que fica para a FASE D

- **Fortalecido acumula até +80%, e a ficha não diz.** O texto mostra "+3% de
  dano", que lê como o efeito inteiro. Medido: Goku chega a +18% de pico na
  luta, He-Man a +68%. A mecânica está boa; o texto é que engana, e isso é
  clareza (FASE E).
- **O mesmo arquétipo rende muito diferente.** Goku e Vegeta param em +18% de
  Fortalecido; Kratos chega a +59% e He-Man a +68%. É desequilíbrio real entre
  personagens que deveriam ocupar o mesmo espaço.
- **Vinte e três habilidades raras** (menos de 0,2 uso por luta). Saem, mas
  quase nunca. São os ultimates mais caros do jogo, e vale decidir se o preço
  está certo. Lista completa em `docs/auditoria-diversidade.json`.
