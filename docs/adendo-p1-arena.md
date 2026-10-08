# Adendo · Parte 1 — arena, layout e posicionamento

O adendo pediu que a batalha deixasse de ser "seis cards numa grade". Esta
parte mexe só na estrutura visual da batalha; movimento, efeitos, Status
animados, grands, som e cenário são as partes seguintes.

## O que estava errado (medido antes)

- **Seis cartões numa grade**, sem chão, sem palco, sem dois times se
  encarando.
- **Não cabia na tela** com o celular deitado (940 px de conteúdo para 390 de
  tela) nem no computador (976 para 800): era preciso rolar para ver o próprio
  time durante a luta.
- **Buffs e debuffs** misturados num canto do cartão, ícones de 17 px.
- **Escudo** invisível na barra de Vida.
- Título e painel de Vantagem ocupando quase um terço da tela em pé.

## O que mudou

- **A batalha ocupa a tela inteira e nunca rola**, em qualquer tamanho. O
  cabeçalho e o rodapé do site somem durante a luta; um botão no canto volta
  ao início com a luta pausada.
- **Dois times frente a frente.** Em pé: rivais em cima, seu trio embaixo,
  medalhões virados para o centro e informação para as bordas — o palco do
  meio fica livre para as trajetórias. Deitado e no computador: seu trio à
  esquerda, rivais à direita. O do meio de cada time dá um passo à frente, e
  os times formam um arco.
- **Cada lutador é uma unidade de pé no chão:** medalhão com moldura na cor do
  time, base de luz, e o círculo do ataque básico em volta, que brilha quando o
  golpe está para sair.
- **Vida com Escudo visível** (listras azuis depois da Vida), "VIDA BAIXA" em
  vermelho pulsando.
- **Habilidades maiores** (34–46 px, conforme a tela), com estado legível de
  longe: carregando (preenche), pronta (dourada), preparando (pulsa), em
  recarga (cinza com cadeado).
- **Buffs numa linha (▲, verde) e debuffs em outra (▼, vermelho)**, com
  duração em volta de cada ícone e "+N" quando não cabe; tocar abre o valor
  atual. Linha vazia não aparece.
- **Preparo e interrupção** aparecem do lado do centro, onde o olho está.
- **Barra de cima única**: confronto, Vantagem e histórico. **Controles
  embaixo**, grandes para o polegar; "próximo confronto automático" foi para o
  painel de ajustes, junto de música e efeitos.
- Nomes longos ("Coragem, o Cão Covarde") usam duas linhas em vez de serem
  cortados.

## Um defeito antigo encontrado no caminho

Com a batalha **pausada**, tocar numa habilidade abria o inspetor com
opacidade zero: a regra que congela as animações da luta congelava também a
entrada do inspetor. Ele existia, mas não aparecia. Agora só a luta congela.

## Como foi conferido

- `scripts/arena-fotos.mjs`: cenários de prova (incluindo `estados` — Preparo,
  fora da luta, Vida baixa com Escudo, muitos Status, pronta, recarga — e
  `nomes`, com os nomes mais longos do elenco) em 360, 390, 430, deitado e
  computador.
- `scripts/arena-batalha-real.mjs`: uma jornada de verdade em 360×640,
  375×667, 390×844, 430×932, 844×390 e 1280×800 — nada rola, nada sai da
  tela, medalhões de 74 a 141 px, inspetor, histórico, ajustes, voltar e
  continuar funcionando, nenhum erro de página.
- Regressão de batalha completa, testes, lint, tipos e build.
