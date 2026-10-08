# Adendo · Parte 6 — Som e música

## O que mudou

**Efeitos sonoros em famílias, casados com os efeitos visuais.** São 54 sons, gerados em Python (`tools/audio/som.py` e `tools/audio/generate_sfx_v2.py`). Cada uma das 42 famílias de efeito visual (`src/presentation/vfxProfiles.ts`) tem o seu som (`SOM_DA_FAMILIA` em `src/audio/cues.ts`):

- **saída**: o disparo, o feixe, a lâmina de energia. Toca no instante em que o golpe deixa quem age.
- **preparo**: a carga dos golpes grandes (feixe pesado, esfera carregada, execução).
- **impacto**: o contato, com o caráter da família. Um soco é seco e grave, um corte é um chiado metálico, o gelo é cristalino, o fogo crepita e a cura é um brilho suave.

Grupos: físico, cortes, projéteis e energia, elementos, magia, apoio e eventos (pronto, interrupção, nocaute, virada, vitória, derrota, grand).

**Variação sem repetição.** Cada arquivo MP3 guarda 4 versões do mesmo som, feitas de tamanhos levemente diferentes. Na luta, a versão e uma variação pequena de tom (±1,5%) e volume (±1,5 dB) são escolhidas pelo número do evento, então o replay soa igual.

**Feitos para celular.** O alto-falante de celular quase não toca graves abaixo de ~150 Hz. Por isso os golpes têm harmônicos e um "toc" de médios que carregam o peso, e o volume de cada som é ajustado pelo que se ouve acima de 250 Hz, não pelo grave. Os picos ficam abaixo de −0,8 dB.

**Mixagem.**
- No máximo 5 sons ao mesmo tempo. Quando passa disso, sai o de menor prioridade: grand > nocaute/interrupção > habilidade > básico > apoio > interface.
- O mesmo som repetido em menos de 70 ms toca uma vez só.
- Estéreo leve, do lado de quem age (nunca mais que 45% para um lado).
- A música abaixa nos momentos grandes (grand, nocaute) e volta devagar.
- Um compressor no fim segura os picos quando vários sons se juntam.

**Música de fundo.** É uma peça original de ~3 min (84 BPM, 64 compassos, seções A–B–C–A2), em 3 camadas do mesmo trecho:
- **base**: pad e baixo, sempre tocando;
- **pulso**: percussão suave e arpejo, que sobe com a intensidade da luta;
- **tema**: a melodia, que só entra quando a luta esquenta ou se arrasta.

Cada luta começa numa seção sorteada. Depois de uma pausa, a música continua de onde parou. O volume da música fica um degrau abaixo dos efeitos para nunca atrapalhar. O laço fecha sem emenda audível.

## Tamanho

| | |
|---|---|
| 54 efeitos (MP3, 4 versões cada) | 1,9 MB |
| Música: base / pulso / tema (Ogg) | 1,5 MB / 1,5 MB / 0,7 MB |

Nada disso entra na instalação do app. O service worker guarda cada arquivo quando a luta usa (`scripts/build-sw.mjs`, `SOB_DEMANDA`). A base da música carrega primeiro e toca assim que chega; as outras camadas entram depois.

## Como regenerar

```
python3 tools/audio/generate_sfx_v2.py      # public/assets/audio/sfx/*.mp3 + manifest.json
python3 tools/audio/generate_music_v2.py    # public/assets/audio/musica-*.ogg + musica.json
```

## Verificação

- `tests/audiovisual.test.ts`: toda família visual tem som existente; 54 sons com 4 versões que não se sobrepõem; MP3 válidos; orçamento de bytes; música com 3 camadas e duração = compassos × 4 × 60 / BPM.
- No Chromium, o início de cada versão decodificada bate com o manifesto (0–5 ms). O navegador já remove o atraso do codificador MP3.
- `scripts/presentation-browser.mjs`: depois do toque, a música toca em 3 camadas, pausa e retoma do mesmo ponto.
