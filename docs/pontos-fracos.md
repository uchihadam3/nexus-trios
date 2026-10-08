# Pontos fracos

Pedido do jogador: o ponto fraco tem que dizer de verdade contra o que o
personagem é ruim e por que ele perde — não uma frase vaga como "perde o
controle e perde a luta".

Agora cada ponto fraco sai de evidência:

- **A ficha**: pouca Vida em relação ao elenco, ataque lento, golpe principal
  com Preparo longo, habilidade que só sai em certa condição, kit sem cura
  nem Escudo, dano só em um alvo, traço que só fortalece ao apanhar.
- **A simulação** (`scripts/medir-fraquezas.ts`, 20 mil lutas 3×3 com trios
  sorteados, resultado em `docs/fraquezas-medidas.json`): quantos Preparos
  são cortados, quantos segundos passa preso, quanto queima, de quantos
  golpes cai, e quanto vence a menos contra trios rivais com Interrupção,
  Controle, Explosão, Área, Cura/Proteção, Dano contínuo ou Tanque.

`scripts/escrever-fraquezas.ts` dá uma nota a cada fraqueza pelo tamanho da
prova em relação ao elenco e escreve `src/data/fraquezas.ts`: a mais forte,
inteira e com o número que a prova; a segunda só quando também é forte e
cabe. Sempre no formato "contra o quê: por quê", com algo do próprio
personagem (Vida, nome do golpe, nome do traço).

Exemplos:

- **Pato Donald** — Precisa apanhar para crescer: Ímpeto crescente só o
  fortalece quando ele recebe dano — contra Explosão, cai antes de crescer o
  bastante. Contra esses trios, ganha 4 de cada 100 lutas a menos.
- **Saitama** — Contra trios rápidos: ataca só a cada 8,5 s — no tempo de um
  golpe dele, o rival comum ataca 2 vezes.
- **Light** — Contra Interrupção: Death Note leva 5,5 s de Preparo (é cortado
  em 12% das vezes) — se for cortado, perde a jogada principal.

Mudou o elenco ou o balanceamento? Rode os dois scripts de novo.
