import type { FamiliaNova } from './vfx-familias-novas';

/*
 * O Renascer de cada um (pedido do jogador: "os personagens que têm renascer,
 * todos usam a mesma coisa… de Fênix… cada um renasce de uma forma diferente").
 *
 * Para quem tem Renascer (src/data/mecanicas.ts): a cor, o rótulo e o ícone da
 * bolinha no medalhão caído, a animação em laço enquanto a barrinha enche
 * (`espera`), a animação da volta (`volta`) e os dois sons (os nomes das
 * famílias com hífen: espera-ikki, volta-ikki…). Quem não está aqui usa as
 * brasas e as asas de fogo de sempre.
 */
export interface RenascerProprio {
  /** a cor do anel, do brilho e do rótulo */
  cor: string;
  /** o fundo escuro da bolinha */
  fundo: string;
  /** a palavra na bolinha (no lugar de RENASCE) */
  rotulo: string;
  espera: FamiliaNova;
  volta: FamiliaNova;
}

const r = (id: string, cor: string, fundo: string, rotulo: string): RenascerProprio =>
  ({ cor, fundo, rotulo, espera: `espera_${id}` as FamiliaNova, volta: `volta_${id}` as FamiliaNova });

export const RENASCER_PROPRIO: Record<string, RenascerProprio> = {
  ikki: r('ikki', '#ff8a3a', '#3a1606', 'FÊNIX'),
  jeangrey: r('jeangrey', '#ffc24a', '#3a2606', 'FORÇA FÊNIX'),
  deadpool: r('deadpool', '#ff4a5a', '#3a0810', 'REGENERA'),
  majinbuu: r('majinbuu', '#ff8ad0', '#3a1030', 'SE REFAZ'),
  mummra: r('mummra', '#c58aff', '#24103a', 'SARCÓFAGO'),
  cell: r('cell', '#8ee86a', '#0e2a0a', 'CÉLULA'),
  mario: r('mario', '#5adf6a', '#0a2a10', '1-UP'),
  wolverine: r('wolverine', '#ffd84a', '#2e2406', 'CURANDO'),
  alucardcv: r('alucardcv', '#ff4a66', '#300610', 'NÉVOA'),
  muzan: r('muzan', '#ff4a86', '#300618', 'SE REMONTA'),
  pain: r('pain', '#b8a2ff', '#1a1236', 'RINNEGAN'),
};

export const SOM_DA_ESPERA = (id: string) => (RENASCER_PROPRIO[id] ? `espera-${id}` : 'brasas-renascendo');
export const SOM_DA_VOLTA = (id: string) => (RENASCER_PROPRIO[id] ? `volta-${id}` : 'renascer');
