import { describe, expect, it } from 'vitest';
import { MEDIDA_COM } from '../src/data/forca-dos-rivais';
import { ENGINE_VERSION, rosterFingerprint } from '../src/engine/ranked';

/*
 * Pedido do jogador: "quando a gente mexer com um personagem, sempre
 * atualizar lá também", para as Dicas de trio (e a campanha) darem a
 * resposta certa. A força de cada personagem é medida em lutas simuladas;
 * se um personagem (Vida, ritmo, ataque, traço, habilidades) ou o motor da
 * luta muda, a medida antiga fica errada. Para medir de novo:
 *
 *   for p in 1 2 3 4; do npx tsx scripts/medir-forca.ts simular $p 30000 /tmp/forca-$p.jsonl & done; wait
 *   npx tsx scripts/medir-forca.ts ajustar /tmp/forca-*.jsonl
 */
describe('força medida dos personagens', () => {
  it('foi medida com o elenco e o motor de agora', () => {
    expect(MEDIDA_COM.elenco, 'um personagem mudou: meça a força de novo (scripts/medir-forca.ts)').toBe(rosterFingerprint());
    expect(MEDIDA_COM.motor, 'o motor da luta mudou: meça a força de novo (scripts/medir-forca.ts)').toBe(ENGINE_VERSION);
  });
});
