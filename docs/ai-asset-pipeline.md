# Assets visuais gerados por IA

## Exportação

Execute `npm run assets:expanded` para reconstruir as 450 imagens dos 150 personagens adicionados. Cada um dos 149 personagens com fonte de IA tem uma folha transparente exclusiva em `assets/ai-source/skills/<personagem>.png`, com três ilustrações próprias; as três habilidades de Mario usam ilustrações originais de objetos feitas no script. Se faltar uma folha, o build falha em vez de reaproveitar imagens de outro personagem. As 300 imagens dos personagens originais ficam intactas. O resultado inclui ícones PNG RGBA de 128 × 128, folhas e manifestos atualizados. Pillow é necessário.

`scripts/split-skill-grid.py <imagem> <personagem-1> ...` recorta uma folha gerada com três colunas e uma linha por personagem em fontes separadas de 768 × 256 pixels.

`npm run assets:pack` é o empacotador integral para quando as 250 folhas fonte de IA estiverem disponíveis; ele exige uma folha fonte para cada personagem. As fontes já recebidas dos personagens novos são mantidas fora de `public/`.

As páginas finais ficam em `public/assets/sheets/`; os PNGs individuais usados pela interface ficam em `public/assets/skills/`, `public/assets/statuses/` e `public/assets/ui/`. Os arquivos mestres permanecem fora de `public/`, então o jogo não os baixa.

## Geometria das folhas

| Conjunto | Quantidade | Folha final | Grade | Célula | Espaço | Margem | Ícone individual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Habilidades | 750, em 250 páginas por personagem | 512 × 176 px por página | 3 colunas × 1 linha | 160 × 160 px | 8 px | 8 px | 128 × 128 px |
| Estados | 14 | 680 × 680 px | 4 × 4, 2 células vazias | 160 × 160 px | 8 px | 8 px | 128 × 128 px |
| Interface | 16 | 680 × 680 px | 4 × 4 | 160 × 160 px | 8 px | 8 px | 128 × 128 px |

Todas as folhas e ícones são PNG RGBA com fundo transparente. Linha e coluna nos manifestos começam em zero. `cell` identifica a célula dentro da folha final; `crop` é o retângulo do ícone de 128 × 128; `sourceCrop` registra o retângulo usado no mestre de IA. Cada manifesto também registra resolução, grade, formato, origem, personagem e habilidade/estado.

## Manifestos

- `public/assets/sheets/skills/manifest.json`: os 750 ícones, seus personagens, habilidades, páginas e recortes.
- `public/assets/sheets/statuses/manifest.json`: os 14 estados universais e seus recortes.
- `public/assets/sheets/ui/manifest.json`: os 16 ícones auxiliares e seus recortes.
- `public/assets/skills/manifest.json`: mapa que a interface consulta para as habilidades.

## Conferência visual

Em desenvolvimento, abra `/#debug` e selecione **Abrir inspeção visual de assets**. As abas mostram as 750 habilidades, os 14 estados, os 16 auxiliares e os retratos dos 250 personagens sobre um quadriculado de transparência. Os ícones de habilidades e estados continuam clicáveis na batalha para abrir suas explicações.

Há 31 retratos placeholder restantes: Black Panther, Feiticeira Escarlate, Vision, Ant-Man, Capitã Marvel, Demolidor, Justiceiro, Motoqueiro Fantasma, Blade, Cavaleiro da Lua, Tempestade, Ciclope, Jean Grey, Vampira, Gambit, Professor X, Venom, Carnage, Doutor Destino, Loki, Ultron, Duende Verde, Surfista Prateado, Galactus, Senhor das Estrelas, Groot, Rocket, Aquaman, Lanterna Verde, Ciborgue e Shazam. As gerações desses retratos tentadas nesta etapa foram recusadas pelo gerador de imagem; os retratos aprovados não foram alterados.
