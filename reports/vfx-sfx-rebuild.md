# NEXUS DUEL — reconstrução audiovisual da batalha

## Método

Chromium headless local, seed 451. A/B com a mesma composição e habilidades carregadas, 20 s em cada largura, `requestAnimationFrame`, PerformanceObserver de long tasks, contagem de nós e filtros computados. A medição com CPU mobile 4× limitada também durou 25 s. Esses perfis de 20–25 s cobrem principalmente a abertura carregada da batalha; uma segunda regressão de 75 s em 2× percorre 16,5 s do relógio mecânico e ataques básicos, skills, cast, cura, escudo, eletricidade, magia e feixe. FPS e percentis dependem da carga do host e a comparação A/B inclui trabalho não relacionado aos VFX.

## Antes e depois — execução sem limitação artificial de CPU, VFX ligados

| Largura | Antes FPS | Antes p95 / p99 ms | Antes >33 ms | Depois FPS | Depois p95 / p99 ms | Depois >33 ms |
|---:|---:|---:|---:|---:|---:|---:|
| 1280 | 51,4 | 33,4 / 50,0 | 133 | 53,2 | 33,4 / 50,1 | 96 |
| 360 | 57,5 | 16,8 / 33,4 | 37 | 58,2 | 16,8 / 33,3 | 23 |
| 390 | 48,4 | 33,4 / 100,0 | 101 | 51,0 | 33,3 / 83,3 | 79 |
| 430 | 39,7 | 66,7 / 116,7 | 152 | 57,8 | 16,8 / 33,4 | 26 |

A mediana ficou em ~16,7 ms em todos esses casos. Em cada largura, há resultados com VFX desligados nos JSON brutos `vfx-benchmark-before-native.json` e `vfx-benchmark-after-final.json`. O custo ligado/desligado da rodada final, em FPS, foi 55,7→53,2 no desktop, 48,4→58,2 em 360, 58,3→51,0 em 390 e 56,8→57,8 em 430. A inversão em 360 e 430 deixa clara a variação do host; não representa ganho causado por ativar efeitos. Na primeira rodada após a implementação, 430 com VFX ficou em 54,3 FPS. O caso 390 ainda mostra p95 de ~33 ms em duas rodadas de 20 s.

Na simulação com CPU limitada 4×, a batalha quase não avançou (0,2–1,1 s mecânicos em 25 s reais), inclusive com VFX desligados. Os FPS com efeitos foram 18,8→19,2 em 360, 14,8→18,2 em 390 e 15,2→19,8 em 430; o p95 permaneceu acima de 100 ms. Esta condição não sustenta uma afirmação de 60 FPS em aparelho físico. JSONs brutos: `vfx-benchmark-before.json` e `vfx-benchmark-after.json`.

| Recurso | Antes | Depois final | Redução |
|---|---:|---:|---:|
| Atlas de combate comprimidos | 4.677.784 bytes / 17 | 1.040.914 bytes / 12 | 77,7% |
| Atlas decodificados, estimativa RGBA | 45.088.768 bytes | 8.749.056 bytes | 80,6% |
| SFX WAV mono | 4.139.180 bytes / 25 | 1.343.634 bytes / 18 | 67,5% |
| Nós máximos sob `.battle-effects` | 37 | 24 | 35,1% |
| Elementos com `filter` sob `.battle-effects` | 9 | 2 | 77,8% |

Os 24 nós incluem o título e seus ícones; o teto de objetos de efeito (`.effect-sprite` e `.fx-beam`) na regressão longa foi 2, abaixo do teto de 3 previsto pelo renderer. A textura do feixe e o cenário somam cerca de 13 KB além dos atlas. O FPS de um cenário específico não mede a memória da GPU diretamente; a estimativa RGBA supõe um atlas inteiro decodificado por arquivo.

## Biblioteca visual

Cada atlas é WebP transparente, 12 quadros em grade 3×4, 20 FPS, com brilho e textura gerados offline por Python determinístico. Nenhum quadro excede 128×128 px.

| Família | Atlas | Quadro | Bytes |
|---|---|---:|---:|
| Impacto leve | physical_light | 96² | 62.716 |
| Impacto forte | physical_heavy | 128² | 115.662 |
| Corte | slash | 128² | 46.450 |
| Projétil | projectile | 96² | 56.794 |
| Esfera de energia | energy_orb | 128² | 97.514 |
| Feixe de energia | energy_orb + beam.webp | 128² + 256×32 | atlas compartilhado |
| Eletricidade | electric | 128² | 83.078 |
| Fogo | fire | 128² | 100.534 |
| Magia e psíquico | magic_psychic | 128² | 85.436 |
| Sombras | dark | 128² | 120.722 |
| Controle | control | 128² | 89.374 |
| Escudo | shield | 128² | 85.548 |
| Cura e bônus | heal_buff | 128² | 97.086 |

`profileFor` resolve ataque básico e skill pelos dados de `icon`, efeitos, status, alvo e algumas palavras do nome. Em uma ação, o renderer monta uma carga curta na origem, um atlas viajando por `translate3d` ao alvo quando aplicável, textura de feixe pré-renderizada para beams, e impacto após a fronteira causal do diretor. Melee recebe o impacto junto ao alvo; área/grand compõem no máximo um acento adicional com o mesmo atlas. `reducedMotion` elimina trajetória e feixe e deixa impacto estático. A cor do personagem identifica o título; a família mantém paleta própria pré-renderizada.

As animações do retrato atingido e da habilidade pronta também deixaram de animar `filter`/`box-shadow`, e o blur da barra de domínio foi removido. Foram removidos SVGs de trajetória/conexão, áreas com gradientes animados, auras, partículas DOM, `mix-blend-mode`/`plus-lighter`, blur e `drop-shadow` nos objetos VFX, além dos presets por personagem e atlas antigos. Cenário e tipografia permanecem estáticos. O diretor, a simulação, STEP e durações não foram alterados.

## Biblioteca sonora

18 bancos: physical-light, physical-heavy, slash, projectile, energy-charge, energy-shot, energy-impact, electric, fire, magic, dark-control, shield, heal-buff, interrupt, ko, grand, victory e defeat. PCM WAV mono a 22.050 Hz, três tomadas determinísticas por banco; picos normalizados a 0,78. O mixer pré-carrega/decodifica os 18 bancos ao desbloquear áudio. No frame do impacto, `sound()` apenas lê `AudioBuffer` em cache, configura ganho/pan e dispara o buffer; se ainda não estiver disponível, omite o cue sem fetch/decode naquele frame. Máximo de sete SFX simultâneos, preempção por prioridade, ducking apenas para grand/KO. O diretor mantém os cues de início e impacto alinhados à troca `before`→`after`.

## Verificação

- Lint, typecheck, 64 testes em 6 arquivos e build passaram.
- Regressão de interface: batalhas completas em 1× e 2× produziram o mesmo vencedor, motivo e tempo mecânico (52,8 s); pausa/retomada, mixer, layout 320/360/390/1280 e 18 WAV decodificados sem clipping passaram.
- VFX Lab: 13 famílias, 3 fases, área/grand, peso por atlas, preview e botão SFX; sem overflow em 390 px.
- Regressão mobile final em `reports/vfx-mobile-final.json`: 75 s reais por largura, 63 impactos amostrados em cada execução, 17,2 s de tempo mecânico, 18 bancos de áudio em cache, nenhum erro de página ou overflow. O máximo observado foi de 2 objetos VFX simultâneos. A galeria em 390 px mostrou as 13 famílias sem erro. Capturas em `reports/vfx-lab-390.png` e `reports/vfx-battle-390.png` (esta após a última remoção de filtros).

| Largura, VFX ligados | FPS | p95 / p99 | Frames >33 ms | Long tasks | Quadros de entrada de impacto >33 ms |
|---:|---:|---:|---:|---:|---:|
| 360 | 59,8 | 16,7 / 16,8 ms | 5 | 1 | 0 de 63 |
| 390 | 59,9 | 16,8 / 16,8 ms | 6 | 0 | 0 de 63 |
| 430 | 60,0 | 16,7 / 16,8 ms | 1 | 0 | 0 de 63 |

Na medição pareada de 360 px sem VFX: 59,9 FPS, p95 16,7 ms, 7 frames >33 ms, 1 long task. Rodadas anteriores dos mesmos 75 s no outro ambiente ficaram em 48,2–55,7 FPS em 360 px e 53,1–55,2 FPS em 390/430 px, com p95 entre 16,8 e 49,9 ms. Por isso, o último resultado comprova uma execução fluida no Chromium usado, mas não estabilidade garantida em todo dispositivo.

A meta p95 <25 ms foi atingida nas três larguras em uma regressão longa após a reconstrução e a checagem visual de 390 px após a última limpeza de filtros ficou em 59,9 FPS/p95 16,7 ms, mas não em todas as rodadas: o trecho curto em 390 px ficou em ~33 ms e uma rodada longa anterior chegou a 49,9 ms em 360 px. O teste com CPU 4× limitada permaneceu lento mesmo sem VFX. Não foi feita medição em hardware mobile real; a evidência é Chromium headless em viewports mobile. Não há decode síncrono no impacto por construção, e nenhum dos 63 quadros de entrada de impacto por largura ultrapassou 33 ms na última rodada. A causa completa da variabilidade entre ambientes não foi isolada.
