# Adendo · Parte 3 — famílias de efeitos visuais

Antes: 13 atlas coloridos para 250 lutadores. Todo soco era o mesmo soco,
todo feixe tinha a mesma cor, e a maior parte das habilidades caía em "impacto
leve" ou "magia". Agora: **42 famílias** montadas a partir de **46 folhas**
desenhadas em Python, com a cor de cada personagem.

## A estratégia do adendo

FAMÍLIA + VARIANTE + COR + ESCALA + DIREÇÃO + INTENSIDADE + TEMPO + CAMADAS.

| peça | onde | como |
|---|---|---|
| família | `src/presentation/vfxProfiles.ts` | 42 famílias em 8 grupos (físico, corte, projétil, energia, elemento, magia, apoio, especial). Cada uma diz quais folhas usa. |
| camadas | idem | **preparo** em quem age, **viagem** (projétil que voa) ou **faixa** (feixe esticado de quem age até o alvo), e **impacto** em cada alvo. |
| cor | `corDoEfeito` | cor do personagem; a cor marcante da habilidade quando ela tem uma (Kamehameha azul, Visão de calor vermelha, Final Flash amarelo, Amaterasu negro-roxo); misturada com a cor do elemento quando ele precisa ser reconhecido (fogo continua fogo, cura continua verde). Toda cor passa por `legivel`: saturação e luminosidade numa faixa que aparece sobre a arena escura. |
| variante | `profileFor` | 0–3, tirada do id (sem sorteio): gira o corte, muda o lado. |
| escala e intensidade | idem | básico 0,82; habilidades sobem; preparo longo (2,5 s ou mais) chega a 1,4. |
| direção | `BattleEffects` | o vetor real, em pixels, entre quem age e cada alvo: o projétil aponta, o feixe gira, a perfuração aponta, o corte espelha. |
| tempo | idem | o projétil sai e chega exatamente no impacto; o feixe cresce, segura o impacto e some; o impacto dura uma fração do resto do beat. |

## As folhas (Python + NumPy + SciPy + Pillow)

`tools/vfx/generate_families.py`, com as ferramentas de luz em
`tools/vfx/luz.py`. Cada folha tem 12 quadros (3 × 4) e é desenhada como luz
em dois campos — **brilho** (vira transparência) e **calor** (vira o tom de
cinza do núcleo). No jogo a folha é usada duas vezes: como máscara de um fundo
na cor do efeito, e por cima, em "screen", o próprio cinza. Resultado: borda
na cor do personagem e núcleo que estoura para claro, a partir de uma folha só.

A física vem de contas:
- faíscas balísticas com gravidade e borrão de movimento proporcional à velocidade;
- fogo, fumaça, veneno e névoa em ruído suavizado (`gaussian_filter`) que sobe com o tempo;
- raios e rachaduras por deslocamento de ponto médio, trocando a cada quadro;
- cortes varrendo um arco em meia-lua, com a cauda que persegue a cabeça e fecha o corte;
- feixes com turbulência que corre para o alvo e fios em espiral;
- escudo em grade hexagonal real, selo com estrela traçada aos poucos.

Tamanhos: impactos 192 px por quadro, projéteis 160 px, faixas 512 × 96. São
46 arquivos WebP com alfa, 3 MB no total, nenhum acima de 160 KB. Cada folha só
é baixada quando uma luta usa aquela família; o service worker guarda cada uma
na primeira vez (não entram mais na instalação).

As 13 folhas antigas saíram; `tools/vfx/generate_vfx.py` agora só gera a
textura neutra da arena.

## Quem usa o quê

`scripts/relatorio-vfx.ts` mostra a distribuição nas 1.000 ações do elenco
(250 básicos + 750 habilidades). As 42 famílias são usadas; a mais comum
(soco) fica em 13,6% e o teste garante que nenhuma passa de 16%.

A escolha segue, nesta ordem: o efeito sem dano manda (cura, Escudo, reforço,
prisão, confusão, debuff — com o nome dando o tema, como prisão de gelo); o
nome da habilidade (Kamehameha, Rasengan, Getsuga, "fogo", "gelo", "garras",
"lança"…); o ícone. Golpes físicos em área viram terremoto; projéteis em área,
explosão. O ataque básico bate do jeito das próprias habilidades: quem tem
elemento bate com ele, quem corta corta, quem só soca varia entre soco, gancho,
rajada e golpe pesado.

## Na arena

`src/components/BattleEffects.tsx` e `src/presentation/vfx-families.css`.
Até cinco camadas por ação (preparo, viagem ou faixa, e até três impactos), só
`transform`, `opacity` e `mask-position` animados. Com as famílias ligadas, a
folha genérica da reação da parte 2 deixa de ser desenhada nos alvos (o
impacto colorido já mostra o golpe); ficam o tremor, o empurrão, o clarão do
retrato, o preparo quebrado e o nocaute.

Com "menos movimento", nada voa nem cresce; o impacto aparece num quadro só e
some — a origem, o alvo e o resultado continuam claros.

## Como conferir

- **Galeria de efeitos** (rodapé do jogo): as 42 famílias em laço, por grupo,
  e uma bancada para tocar cada camada em qualquer cor.
- `visual-probe.html?hab=goku:0&play=1` toca a habilidade real de qualquer
  personagem em laço; `scripts/vfx-familias-quadros.mjs` fotografa a trajetória
  e o impacto de uma lista delas.
- `tests/audiovisual.test.ts`: folhas 3 × 4 com alfa, todas usadas, peso; 30–45
  famílias, todas usadas, nenhuma dominando; cor legível; as habilidades
  famosas com o efeito e a cor certos.
