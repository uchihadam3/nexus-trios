# Validação — apresentação de batalha

## Regressão e build

- Typecheck (`npm run typecheck`), ESLint, build de produção e 23 testes aprovados.
- Três estados completos capturados antes da alteração reproduzidos integralmente; nenhum valor de ficha, dano, carga, cooldown, dificuldade ou Domínio foi rebalanceado.
- Direção em 1×, 2× e alternando velocidades: mesmo estado final, eventos e resultado. Duração de apresentação em 2× equivale à metade, com tolerância de um frame.
- Condição só muda no impacto; a fila contém no máximo um passo de simulação e é esvaziada antes do resultado.
- Preparação, cancelamento, atraso, redução, proteção, carga por evento, cooldown, Death Note, 100 confrontos e as 24 fichas continuam cobertos pelos testes existentes.
- Limite de 120 segundos e vitória por Domínio confirmados com fixture resistente. Encerramento antecipado por incapacitação também confirmado.

## Navegador

- Chromium, larguras 320, 360, 390 e 1280: seis retratos com pelo menos 76 px, sem overflow horizontal, barra única de Domínio.
- Duas batalhas completas pelo fluxo real da interface, Light/Pikachu/Wolverine contra Gojo/Goku/Raven, semente 42: vitória por incapacitação aos 55,9 segundos de jogo, exatamente o mesmo resultado em 1× e 2×.
- Apresentação dessa luta: ~204,48 s em 1×, ~102,24 s em 2× (teste determinístico do diretor). No navegador, amostras a cada dez segundos observaram conclusão aos 210/110 s. Momentos de foco estendem o tempo real sem mudar o relógio do motor.
- Estados observados em ambas as velocidades: vazia, carregando, pronta, preparando, executando e cooldown.
- Capturas inspecionadas de arena, preparação, grande habilidade, interrupção, ligação de sinergia, bloqueio e incapacitação.
- Nenhum erro JavaScript nos testes de apresentação.
- Campanha automática completa: dez vitórias, campeão, contadores corretos, nova seleção, derrota e reinício.
- Oito tipos de momentos visuais capturados; máximo de 400 elementos na arena durante a luta amostrada.

## Áudio

- AudioContext inexistente antes de gesto; estado `running` e trilha agendada após clicar. Pausa interrompe a música.
- Música e efeitos configurados separadamente, salvos e recuperados após recarregamento.
- Composição original de 16 compassos (~35,56 s) e 25 cues renderizados pelo OfflineAudioContext do navegador, todos não silenciosos e sem clipping individual.
- Pico da trilha no ganho de teste: 0,253; RMS 0,024. Isso valida a síntese, não substitui avaliação auditiva em aparelhos reais.
- Sem assets musicais externos; nenhum download de música.

## PWA

- Build de produção: manifesto standalone, ícones PNG, service worker ativo e 32 arquivos em cache.
- Recarregamento, seleção de trio e batalha funcionaram com rede desconectada.
- Instalação física em Android/iOS não foi executada no dispositivo do usuário; disponibilidade depende do navegador.

## Reproduzir

- `npm test`, `npm run typecheck`, `npm run lint`, `npm run build`.
- `node scripts/presentation-browser.mjs` — UI, áudio, velocidades e quatro larguras.
- `node scripts/visual-moments.mjs` — capturas das ações e contagem de elementos da arena.
- `node scripts/campaign-browser.mjs` — dez confrontos automáticos, campeão, derrota e reinício.
- `node scripts/pwa-browser.mjs` — build offline.

Relatórios e capturas são temporários em `test-results/`. Parâmetros iniciais de apresentação estão documentados no README e centralizados em `src/presentation/config.ts`. As regras e os valores de balanceamento do MVP permanecem os mesmos.
