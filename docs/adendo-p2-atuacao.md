# Adendo · Parte 2 — movimento e atuação dos personagens

O critério do adendo: assistindo sem ler nada, tem que ser óbvio quem fez o
quê. Antes desta parte, só o ataque básico físico dava um pequeno tranco no
lugar; quem curava, protegia, lançava maldição ou disparava não se mexia, e
quem era atingido só tremia.

## Como funciona

Três peças, cada uma no lugar onde faz sentido:

1. **Quem faz o quê** — `src/presentation/acting.ts`. Lê o beat que o motor já
   calculou e decide o estilo de quem age (corpo a corpo, à distância, área,
   apoio, maldição, preparo, interrupção) e a reação de cada alvo (golpe,
   golpe pesado, cura, Escudo, buff, debuff, preparo quebrado, queda). Calcula
   a direção real, em pixels, entre o medalhão de quem age e o do alvo — o
   avanço vai até encostar, em qualquer tamanho de tela, em pé ou deitado.
2. **Como se move** — curvas simuladas, não desenhadas à mão
   (`tools/vfx/generate_motion.py`). Cada estilo tem um roteiro de para onde o
   medalhão "quer ir"; uma mola amortecida o persegue, resolvida com
   `scipy.integrate.solve_ivp`. A física dá a antecipação, a aceleração, a
   ultrapassagem no contato e o assentamento. Conferido: no corpo a corpo o
   medalhão recua 15%, chega ao alvo exatamente no impacto (1,01) e passa 4%
   do ponto. Saída: `src/presentation/acting-motion.css`.
3. **O que se vê** — efeitos desenhados em Python com NumPy, SciPy e Pillow
   (`tools/vfx/generate_acting.py`), 13 folhas de 12 quadros: faísca e golpe
   pesado (com estrela de clarão), cura subindo em colunas de luz, bolha de
   Escudo com grade de energia, buff subindo, névoa de maldição torcida a
   cada quadro, preparo estilhaçado, poeira de nocaute; e, para quem age,
   rastro do avanço, clarão do disparo, aura do preparo, onda de choque no
   chão e pulso de apoio. Desenhados como luz que se soma e só no fim
   convertidos em cor e transparência. Os de quem age são máscaras brancas
   tingidas com a cor do personagem no jogo.

## Os estilos

| quem age | movimento | efeito |
|---|---|---|
| corpo a corpo | recua, avança até o alvo, encosta no impacto, volta | rastro na direção do avanço |
| à distância | inclina carregando, tranco para trás no disparo | clarão do disparo, na direção do alvo |
| área | sobe, desce batendo no chão | onda de choque no chão |
| apoio (cura, Escudo, buff) | pulsa e se inclina para o aliado | pulso na cor do personagem |
| maldição (debuff sem dano) | inclina e treme de leve | pulso |
| preparo | ergue-se e segura, respirando | aura em laço |
| interrupção | o avanço rápido | rastro |

| quem recebe | movimento | efeito |
|---|---|---|
| golpe / golpe pesado | empurrado para longe de quem bateu, tremor perpendicular, clarão branco | faísca / impacto pesado |
| cura | sobe de leve | colunas verdes |
| Escudo | pulso | bolha azul |
| buff | sobe | chama dourada com setas |
| debuff | estremece | névoa roxa |
| preparo quebrado | treme | estilhaços dourados |
| nocaute | cai, inclina, encolhe | poeira |

Com "menos movimento" (do sistema ou das configurações), nada viaja nem
treme; a origem e o alvo continuam marcados e as reações de cura, Escudo e
debuff continuam aparecendo.

## Como foi conferido

- `scripts/atuacao-quadros.mjs` toca cada ação em laço
  (`visual-probe.html?play=1`) e fotografa a sequência: corpo a corpo,
  energia, cura, buff, debuff, interrupção, área e nocaute, em pé e deitado.
- `tests/atuacao.test.ts`: o avanço para a 0,82 medalhão do alvo, o alvo só
  reage no impacto e é empurrado para longe de quem bateu, cada tipo de ação
  dá o estilo certo, e a animação recomeça a cada beat.
- Regressão de batalha completa, testes, lint, tipos e build.
