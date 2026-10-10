import { describe, expect, it } from 'vitest';
import { META_DAS_DICAS, dicasLiberadas, ehDono, sha256 } from '../src/lib/dicas-liberadas';

describe('botão das Dicas de trio', () => {
  it('fica escondido até a meta, e aparece depois dela', () => {
    expect(META_DAS_DICAS).toBe(1_400_000);
    expect(dicasLiberadas(false, 0)).toBe(false);
    expect(dicasLiberadas(false, META_DAS_DICAS - 1)).toBe(false);
    expect(dicasLiberadas(false, META_DAS_DICAS)).toBe(true);
  });
  it('a conta do dono vê sempre; outras contas e quem não entrou, não', async () => {
    // o e-mail do dono não fica escrito nem aqui: só o resumo SHA-256 dele, em src/lib/dicas-liberadas.ts
    expect(dicasLiberadas(true, 0)).toBe(true);
    expect(await sha256('abc')).toBe('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
    expect(await ehDono('outra.pessoa@gmail.com')).toBe(false);
    expect(await ehDono(null)).toBe(false);
  });
});
