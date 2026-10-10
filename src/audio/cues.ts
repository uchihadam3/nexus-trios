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
import { FAMILIAS_NOVAS, SOM_DA_NOVA, type FamiliaNova } from '../presentation/vfx-familias-novas';

export const SONS = [
  'soco-leve', 'soco-pesado', 'esmagar', 'gancho', 'multi-golpe', 'terremoto', 'onda-choque',
  'corte', 'corte-pesado', 'estocada', 'corte-giratorio', 'lamina-energia',
  'disparo', 'tiro', 'saraivada', 'missil', 'explosao', 'carga-pequena', 'carga-grande', 'feixe', 'impacto-energia',
  'raio', 'fogo', 'gelo', 'vento', 'agua', 'terra', 'veneno',
  'psiquico', 'sombra', 'luz', 'portal', 'maldicao', 'prisao', 'selo', 'distorcao',
  'cura', 'escudo', 'bloqueio', 'reforco', 'enfraquecer', 'renova-buff', 'renova-debuff', 'purificar', 'dreno',
  'interrupcao', 'pronto', 'preparo', 'grand-carga', 'grand-impacto', 'nocaute', 'vitoria', 'derrota', 'virada',
  'transformacao', 'toque', 'errou', 'barreira-anula',
  'ui-clique', 'ui-confirma', 'ui-abrir', 'ui-fechar', 'ui-alternar', 'ui-escolher', 'ui-arena', 'reacao',
] as const;

/* Um som próprio para cada família nova de efeito (tools/audio/sfx_familias.py). */
const NOVAS = Object.keys(FAMILIAS_NOVAS) as FamiliaNova[];
export const SONS_DAS_NOVAS = NOVAS.map(SOM_DA_NOVA);
export type Sound = typeof SONS[number] | (string & { readonly __somNovo?: never });
/*
 * Os golpes famosos têm um som que vem ANTES do contato: a mão do Chidori
 * acendendo, o Rasengan girando, o "ka-me-ha-me" juntando energia, a marreta
 * subindo. Ele começa com o golpe e termina quando o golpe sai (se voa) ou
 * chega (se é corpo a corpo); o impacto fica só com o estouro.
 */
const ANTES_DA_NOVA: Partial<Record<FamiliaNova, { antes: Sound; saida?: Sound }>> = {
  esfera_espiral: { antes: 'esfera-espiral-carga' },
  kamehameha: { antes: 'kamehameha-carga', saida: 'kamehameha-feixe' },
  marretada: { antes: 'marretada-giro' },
  susanoo_perfeito: { antes: 'susanoo-manto' },
  raikiri: { antes: 'raikiri-mao' },
  reigun: { antes: 'reigun-carga' },
  omnislash: { antes: 'limite-cloud' },
  rasengan: { antes: 'rasengan-mao' },
  renascimento: { antes: 'fenix-asas' },
  metal_dobrado: { antes: 'metal-preparo' },
  makankosappo: { antes: 'makanko-carga' },
  explosao_de_fogo: { antes: 'fogo-no-peito' },
  arma_adquirida: { antes: 'troca-de-arma' },
  carga_maxima: { antes: 'buster-carga' },
  visao_de_calor: { antes: 'olhos-brilhando' },
  ultimo_filho_de_krypton: { antes: 'krypton-carga' },
  execucao_aurora: { antes: 'aurora-preparo' },
  zero_absoluto: { antes: 'zero-preparo' },
  mais_forte_ainda: { antes: 'furia-hulk' },
  rugido_do_leao: { antes: 'cosmo-leao' },
  praga_da_carne: { antes: 'runa-lich' },
  estado_avatar_aang: { antes: 'avatar-brilho' },
  byakugou: { antes: 'byakugou-selo' },
  feixe_concentrado: { antes: 'visor-carregando' },
  seis_mundos: { antes: 'lotus-shaka' },
  retorno_ao_sarcofago: { antes: 'sarcofago-preparo' },
  jajanken_pedra: { antes: 'nen-gon' },
  jajanken_papel: { antes: 'nen-gon' },
  batida_do_gorila: { antes: 'batida-preparo' },
  chidori_sasuke: { antes: 'chidori-sasuke-mao' },
  amaterasu: { antes: 'mangekyo-sasuke' },
  genjutsu_sasuke: { antes: 'mangekyo-sasuke' },
  burning_attack: { antes: 'selo-burning' },
  corte_final: { antes: 'aura-trunks' },
  taiyoken: { antes: 'taiyoken-flash' },
  kame_kuririn: { antes: 'kame-kuririn-carga' },
  furia_espartana: { antes: 'furia-kratos' },
  ira_dos_deuses: { antes: 'ira-kratos' },
};
const SONS_DE_ANTES = [...new Set(Object.values(ANTES_DA_NOVA).flatMap((x) => [x!.antes, ...(x!.saida ? [x!.saida] : [])]))];

export const TODOS_OS_SONS: Sound[] = [...SONS, ...SONS_DAS_NOVAS, ...SONS_DE_ANTES, 'cravar', 'ricochete'];

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
  /** Toca antes do contato e termina quando o golpe sai (ou chega, se não voa). */
  antes?: Sound;
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
  ...Object.fromEntries(NOVAS.map((k) => {
    const x = FAMILIAS_NOVAS[k] as { viagem?: string; faixa?: string; preparo?: string };
    // a saída (o que voa ou o feixe) usa a biblioteca; o impacto é o som da própria família
    const saida: Sound | undefined = x.faixa === 'laser' ? 'feixe' : x.faixa ? 'feixe' : x.viagem === 'flecha' ? SOM_DA_NOVA('flecha')
      : x.viagem === 'disco' ? SOM_DA_NOVA('disco') : x.viagem === 'bola_ki' ? 'disparo' : x.viagem ? 'disparo' : undefined;
    const extra = ANTES_DA_NOVA[k];
    const preparo: Sound | undefined = extra?.antes ?? (x.preparo ? 'carga-grande' : undefined);
    const impacto = k === 'flecha' ? 'cravar' : k === 'disco' ? 'ricochete' : SOM_DA_NOVA(k);
    return [k, { saida: extra?.saida ?? saida, preparo, impacto, antes: extra?.antes }];
  })) as Record<FamiliaNova, SomDaFamilia>,
};

/* Famílias de apoio entram com prioridade de apoio na mixagem. */
export const FAMILIAS_DE_APOIO = new Set<VfxFamily>(['cura', 'escudo', 'reforco', 'selo', 'maldicao', 'distorcao', 'portal',
  ...NOVAS.filter((k) => FAMILIAS_NOVAS[k].grupo === 'apoio')]);

export interface SomManifesto { arquivo: string; versoes: number[]; duracoes: number[]; bytes: number; descricao: string }
export interface Manifesto { taxa: number; versoes: number; sons: Record<Sound, SomManifesto> }
