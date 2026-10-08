/*
 * A biblioteca de efeitos sonoros (adendo, parte 6).
 *
 * Os sons são gerados em Python (tools/audio/generate_sfx_v2.py): cada arquivo
 * MP3 guarda 4 versões do mesmo som; public/assets/audio/sfx/manifest.json diz
 * onde cada versão começa e quanto dura. Aqui ficam só os nomes e a ligação de
 * cada família de efeito visual (src/presentation/vfxProfiles.ts) com o som que
 * combina com ela: o que toca na saída (o disparo, o feixe, a carga) e o que
 * toca no impacto.
 */
import type { VfxFamily } from '../presentation/vfxProfiles';

export const SONS = [
  'soco-leve', 'soco-pesado', 'esmagar', 'gancho', 'multi-golpe', 'terremoto', 'onda-choque',
  'corte', 'corte-pesado', 'estocada', 'corte-giratorio', 'lamina-energia',
  'disparo', 'tiro', 'saraivada', 'missil', 'explosao', 'carga-pequena', 'carga-grande', 'feixe', 'impacto-energia',
  'raio', 'fogo', 'gelo', 'vento', 'agua', 'terra', 'veneno',
  'psiquico', 'sombra', 'luz', 'portal', 'maldicao', 'prisao', 'selo', 'distorcao',
  'cura', 'escudo', 'bloqueio', 'reforco', 'enfraquecer', 'purificar', 'dreno',
  'interrupcao', 'pronto', 'preparo', 'grand-carga', 'grand-impacto', 'nocaute', 'vitoria', 'derrota', 'virada',
  'transformacao', 'toque',
  'ui-clique', 'ui-confirma', 'ui-abrir', 'ui-fechar', 'ui-alternar',
] as const;
export type Sound = typeof SONS[number];

/*
 * Prioridade da mixagem, do adendo: grand > impacto importante > interrupção >
 * ataque básico > buff/debuff > interface. Quando há som demais ao mesmo tempo,
 * o de prioridade menor é o que sai.
 */
export const PRIORIDADE = { grand: 5, importante: 4, habilidade: 3, basico: 2, apoio: 1.5, interface: 1 } as const;

interface SomDaFamilia {
  /** Toca quando o golpe sai (disparo, feixe, lâmina), sincronizado com a viagem. */
  saida?: Sound;
  /** Toca no começo do Preparo de uma habilidade desta família. */
  preparo?: Sound;
  impacto: Sound;
}

export const SOM_DA_FAMILIA: Record<VfxFamily, SomDaFamilia> = {
  soco: { impacto: 'soco-leve' }, golpe_pesado: { impacto: 'soco-pesado' }, esmagar: { impacto: 'esmagar' },
  gancho: { impacto: 'gancho' }, terremoto: { impacto: 'terremoto' }, onda_de_choque: { impacto: 'onda-choque' },
  rajada_de_golpes: { impacto: 'multi-golpe' },
  corte: { impacto: 'corte' }, corte_diagonal: { impacto: 'corte' }, corte_cruzado: { impacto: 'corte-pesado' },
  estocada: { impacto: 'estocada' }, corte_giratorio: { impacto: 'corte-giratorio' },
  corte_de_energia: { saida: 'lamina-energia', impacto: 'corte-pesado' },
  tiro: { saida: 'tiro', impacto: 'soco-leve' }, saraivada: { saida: 'saraivada', impacto: 'multi-golpe' },
  missil: { saida: 'missil', impacto: 'explosao' }, esfera: { saida: 'disparo', impacto: 'impacto-energia' },
  esfera_carregada: { preparo: 'carga-grande', saida: 'disparo', impacto: 'explosao' },
  feixe: { saida: 'feixe', impacto: 'impacto-energia' }, feixe_pesado: { preparo: 'carga-grande', saida: 'feixe', impacto: 'explosao' },
  explosao: { impacto: 'explosao' }, onda_de_energia: { saida: 'lamina-energia', impacto: 'onda-choque' },
  fogo: { impacto: 'fogo' }, gelo: { impacto: 'gelo' }, raio: { impacto: 'raio' }, vento: { impacto: 'vento' },
  agua: { impacto: 'agua' }, terra: { impacto: 'terra' }, veneno: { impacto: 'veneno' }, sombra: { impacto: 'sombra' },
  luz: { impacto: 'luz' }, selo: { impacto: 'selo' }, prisao: { impacto: 'prisao' }, distorcao: { impacto: 'distorcao' },
  portal: { impacto: 'portal' }, telecinese: { impacto: 'psiquico' }, maldicao: { impacto: 'maldicao' },
  cura: { impacto: 'cura' }, escudo: { impacto: 'escudo' }, reforco: { impacto: 'reforco' }, dreno: { saida: 'dreno', impacto: 'enfraquecer' },
  execucao: { preparo: 'grand-carga', impacto: 'grand-impacto' },
};

/* Famílias de apoio entram com prioridade de apoio na mixagem. */
export const FAMILIAS_DE_APOIO = new Set<VfxFamily>(['cura', 'escudo', 'reforco', 'selo', 'maldicao', 'distorcao', 'portal']);

export interface SomManifesto { arquivo: string; versoes: number[]; duracoes: number[]; bytes: number; descricao: string }
export interface Manifesto { taxa: number; versoes: number; sons: Record<Sound, SomManifesto> }
