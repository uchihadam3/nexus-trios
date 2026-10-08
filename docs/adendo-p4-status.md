# Adendo · Parte 4 — Buffs, debuffs e Status

## Na arena

- **Linhas separadas.** Buffs (▲) e debuffs (▼) têm uma linha própria cada, sob o medalhão, com até 4 ícones e "+N" para o resto. Cada ícone mostra a duração num anel e abre os detalhes ao tocar.
- **Entrada.** O nome curto aparece no medalhão no impacto. O ícone chega à linha crescendo com um brilho na cor do lado (verde para ajuda, vermelho para atrapalho) e depois fica parado.
- **Renovação.** Reaplicar um Status que já está lá não cria um ícone novo: o anel dá um pulso discreto, no máximo um a cada 1,5 s.
- **Saída.**
  - Quando o tempo acaba, o ícone encolhe e some (fade).
  - Quando sai antes da hora (dissipado), o ícone se parte num anel branco.
  - O ícone que sai fica 0,6 s na tela para o efeito ser visto.
- **Purificação.** O motor ainda não tem efeito que remova Status. O visual de "dissipado" já cobre qualquer remoção antecipada, então uma purificação futura aparece sem trabalho novo.
- **Movimento reduzido.** Sem o crescimento, o pulso e o anel: só o fade.

## Na ficha

- A linha do Status mostra só o nome, o número e o tempo: "Aplica Fortalecido · +18% de dano · 7 s".
- O que o Status faz e como ele soma estão no cartão que abre ao tocar no nome (`src/presentation/glossario.ts`).

## Preparo mínimo e Preparo leve

- Toda habilidade tem Preparo, para o nome aparecer antes do golpe. As 481 que eram instantâneas ganharam **0,5 s**.
- Esse Preparo é **leve**: não pode ser interrompido e não conta como "inimigo em Preparo", nem para a condição de habilidades nem para a Carga de quem vive de interromper. Os Preparos que já existiam (todos de 0,6 s ou mais) continuam interrompíveis como antes (`PREPARO_LEVE` em `src/engine/battle.ts`).
- Medido em 8.000 lutas com o elenco inteiro, antes e depois:
  - a vitória de cada personagem mudou em média 2,1 pontos, perto do ruído da simulação;
  - o desvio do elenco ficou igual (13,7 pontos);
  - a duração média ficou em ~35 s.
