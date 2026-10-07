# NEXUS — prova visual da jornada e da batalha

Capturas em viewport de **390 × 844 px**, feitas no navegador Chromium com o mesmo trio e encontro. As páginas longas foram capturadas por inteiro. O estado de resultado foi produzido pelo motor real, com a escala reduzida na fixture para garantir vitória reproduzível.

| Tela | Antes | Depois |
| --- | --- | --- |
| Início | [Ver](visual-proof/before/home.jpg) | [Ver](visual-proof/after/home.jpg) |
| Draft | [Ver](visual-proof/before/draft.jpg) | [Ver](visual-proof/after/draft.jpg) |
| Personagens | [Ver](visual-proof/before/characters.jpg) | [Ver](visual-proof/after/characters.jpg) |
| Como jogar | [Ver](visual-proof/before/help.jpg) | [Ver](visual-proof/after/help.jpg) |
| Batalha, em repouso | [Ver](visual-proof/before/battle.jpg) | [Ver](visual-proof/after/battle.jpg) |
| Resultado | [Ver](visual-proof/before/result.jpg) | [Ver](visual-proof/after/result.jpg) |
| Conclusão da jornada | [Ver](visual-proof/before/conclusion.jpg) | [Ver](visual-proof/after/conclusion.jpg) |
| Configurações | [Ver](visual-proof/before/settings.jpg) | [Ver](visual-proof/after/settings.jpg) |

## Uma ação em seis quadros

1. [Origem](visual-proof/action/01-source.jpg)
2. [Alvo](visual-proof/action/02-target.jpg)
3. [Trajeto](visual-proof/action/03-travel.jpg)
4. [Impacto](visual-proof/action/04-impact.jpg)
5. [Número](visual-proof/action/05-number.jpg)
6. [Consequência](visual-proof/action/06-consequence.jpg)

O teste de navegador em `scripts/combat-visual-browser.mjs` também verifica ataque físico, energia, cura, escudo, buff, debuff, interrupção, área, assistência de sinergia e KO. A origem, o alvo, o vínculo visual e a consequência são derivados dos eventos da batalha, sem alterar o motor.

## Verificação

- `npm test -- --run`: 70 testes aprovados.
- `npm run lint`, `npm run typecheck`, `npm run build`: aprovados.
- `node scripts/ux-mobile-browser.mjs`: Início, Ajuda, Luz, Draft e Batalha em 360, 390 e 430 px, sem rolagem horizontal.
- `node scripts/combat-visual-browser.mjs`: 10 cenários aprovados.

As imagens do estado de repouso não substituem a sequência de ação: o traço causal só aparece durante a execução do golpe.
