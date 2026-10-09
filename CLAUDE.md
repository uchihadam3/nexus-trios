# NEXUS DUEL — regras para quem mexe no código

- Respostas ao dono do projeto: em português, simples.
- Publicação só pelo GitHub Pages (workflow "Build and deploy"). Nada de Vercel.

## Mudou um personagem ou o motor da luta? Meça a força de novo

As Dicas de trio (`src/presentation/dicas-do-trio.ts`) e a campanha usam a
força medida de cada personagem (`src/data/forca-dos-rivais.ts`). Qualquer
mudança em Vida, ritmo, ataque, traço, habilidade, Status ou regra da luta
deixa essa medida velha, e as dicas passam a errar.

1. Suba `ENGINE_VERSION` em `src/engine/ranked.ts` se a regra da luta mudou.
2. Meça de novo (uns minutos):
   ```
   for p in 1 2 3 4; do npx tsx scripts/medir-forca.ts simular $p 30000 /tmp/forca-$p.jsonl & done; wait
   npx tsx scripts/medir-forca.ts ajustar /tmp/forca-*.jsonl
   ```
3. Confira a dificuldade: `npx tsx scripts/medir-perfis.ts bom 700` (~10–13% de campeões).

`tests/forca-atualizada.test.ts` falha enquanto a medida não for refeita.

4. Conte ao jogador a posição de força de quem mudou, antes e depois (pedido
   dele): guarde a medida antiga antes de medir
   (`git show HEAD:src/data/forca-dos-rivais.ts > /tmp/forca-antes.ts`) e rode
   `npx tsx scripts/comparar-forca.ts /tmp/forca-antes.ts <ids>`.

Vida no equilíbrio: pode mudar em todos, mas pouco, sem o personagem virar
outra coisa (`partesDoAjuste` em src/data/characters.ts): tanque sobe até 20% e
desce no máximo 15% (continua tanque); os outros sobem no máximo 10%, descem no
máximo 15% e nunca chegam à Vida de tanque. O resto vai para dano/cura/escudo
ou para o próprio kit.

## Antes de publicar

```
npx tsc --noEmit -p . && npx eslint . && npx vitest run && npm run build
npx -y deno@2 check supabase/functions/ranked-api/index.ts
```
