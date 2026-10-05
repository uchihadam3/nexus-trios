# Assets visuais gerados por IA

## Exportação

Execute `npm run assets:pack` na raiz do projeto. O script `scripts/pack-ai-assets.py` recorta os mestres em `assets/ai-source/`, limpa pixels quase transparentes, normaliza cada imagem para PNG RGBA de 128 × 128 e valida o canal alfa e os cantos transparentes. Pillow é necessário para executar o recorte.

As páginas finais ficam em `public/assets/sheets/`; os PNGs individuais usados pela interface ficam em `public/assets/skills/`, `public/assets/statuses/` e `public/assets/ui/`. Os arquivos mestres permanecem fora de `public/`, então o jogo não os baixa.

## Geometria das folhas

| Conjunto | Quantidade | Folha final | Grade | Célula | Espaço | Margem | Ícone individual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Habilidades | 300, em 100 páginas por personagem | 512 × 176 px por página | 3 colunas × 1 linha | 160 × 160 px | 8 px | 8 px | 128 × 128 px |
| Estados | 14 | 680 × 680 px | 4 × 4, 2 células vazias | 160 × 160 px | 8 px | 8 px | 128 × 128 px |
| Interface | 16 | 680 × 680 px | 4 × 4 | 160 × 160 px | 8 px | 8 px | 128 × 128 px |

Todas as folhas e ícones são PNG RGBA com fundo transparente. Linha e coluna nos manifestos começam em zero. `cell` identifica a célula dentro da folha final; `crop` é o retângulo do ícone de 128 × 128; `sourceCrop` registra o retângulo usado no mestre de IA. Cada manifesto também registra resolução, grade, formato, origem, personagem e habilidade/estado.

## Manifestos

- `public/assets/sheets/skills/manifest.json`: os 300 ícones, seus personagens, habilidades, páginas e recortes.
- `public/assets/sheets/statuses/manifest.json`: os 14 estados universais e seus recortes.
- `public/assets/sheets/ui/manifest.json`: os 16 ícones auxiliares e seus recortes.
- `public/assets/skills/manifest.json`: mapa que a interface consulta para as habilidades.

## Conferência visual

Em desenvolvimento, abra `/#debug` e selecione **Abrir inspeção visual de assets**. As abas mostram as 300 habilidades, os 14 estados, os 16 auxiliares e os retratos dos 100 personagens sobre um quadriculado de transparência. Os ícones de habilidades e estados continuam clicáveis na batalha para abrir suas explicações.

Há 31 retratos placeholder restantes: Black Panther, Feiticeira Escarlate, Vision, Ant-Man, Capitã Marvel, Demolidor, Justiceiro, Motoqueiro Fantasma, Blade, Cavaleiro da Lua, Tempestade, Ciclope, Jean Grey, Vampira, Gambit, Professor X, Venom, Carnage, Doutor Destino, Loki, Ultron, Duende Verde, Surfista Prateado, Galactus, Senhor das Estrelas, Groot, Rocket, Aquaman, Lanterna Verde, Ciborgue e Shazam. As gerações desses retratos tentadas nesta etapa foram recusadas pelo gerador de imagem; os retratos aprovados não foram alterados.
