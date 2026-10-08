# NEXUS — Duelo de Trios

Jogo de batalhas automáticas em português, feito para celular e computador. Monte um trio, combine habilidades e enfrente dez confrontos em uma campanha.

**Jogar na web:** https://uchihadam3.github.io/nexus-trios/

## Conteúdo do jogo

- Elenco com 100 personagens e três habilidades por personagem.
- 300 ícones de habilidades, com folhas organizadas e manifesto de recorte.
- Ícones próprios para os 14 estados e 16 ações auxiliares da interface.
- Retratos e tela de inspeção visual dos assets.
- Campanha com opção de abandonar a jornada e começar outra.
- PWA instalável e suporte offline após o primeiro carregamento.

## Executar localmente

Requer Node.js 22 ou superior.

```sh
npm ci
npm run dev
```

Verificações e build de produção:

```sh
npm test
npm run lint
npm run typecheck
npm run build
npm run preview
```

## Assets

As folhas e os manifestos de recorte estão em `public/assets/sheets/`. Retratos, habilidades, estados e ícones de interface usados pelo jogo ficam em `public/assets/` e são carregados pela interface da batalha.

As origens dos retratos pesquisados estão em [docs/portrait-image-sources.md](docs/portrait-image-sources.md).

## Estrutura

- `src/data/`: elenco, habilidades e estados.
- `src/engine/`: campanha, regras e simulação da batalha.
- `src/components/` e `src/screens/`: interface do jogo e inspetor de assets.
- `public/assets/`: arte final usada pelo jogo.
- `scripts/`: geração de cache offline e ferramentas de auditoria.
