/*
 * Efeitos visuais por família (adendo, parte 3).
 *
 * 250 lutadores não cabem em treze desenhos, e uma animação por habilidade
 * seria mil desenhos. A estratégia é a do adendo:
 *
 *   FAMÍLIA + VARIANTE + COR + ESCALA + DIREÇÃO + INTENSIDADE + TEMPO + CAMADAS
 *
 * - 163 famílias (41 originais + 122 novas), cada uma montada a partir das folhas desenhadas em Python
 *   (tools/vfx/generate_families.py → public/assets/vfx/familias);
 * - cada família diz que CAMADAS usa: preparo em quem age, viagem (um
 *   projétil que voa) ou faixa (um feixe esticado de quem age até o alvo),
 *   e o impacto em cada alvo;
 * - a COR vem do personagem (ou de uma cor marcante da habilidade: o
 *   Kamehameha é azul, a Visão de calor é vermelha), misturada com a cor do
 *   elemento quando o elemento precisa ser reconhecido (fogo continua
 *   parecendo fogo, cura continua verde);
 * - VARIANTE, ESCALA e INTENSIDADE saem da habilidade (qual das três, quanto
 *   tempo de preparo), e a DIREÇÃO do vetor real entre quem age e o alvo.
 *
 * Nada aqui decide combate: só lê a ficha do personagem.
 */
import { byId } from '../data/characters';
import type { Character, Effect, Skill, Target, Visual } from '../engine/types';
import { FAMILIAS_NOVAS, NOVAS_DE_BASICO, NOVAS_NO_ALVO, type FamiliaNova } from './vfx-familias-novas';
import { FAMILIA_DA_HABILIDADE, FAMILIA_DO_BASICO } from './vfx-atribuicao';

export type Grupo = 'físico' | 'corte' | 'projétil' | 'energia' | 'elemento' | 'magia' | 'apoio' | 'especial';

/** Como a cor do personagem entra: inteira, misturada com o elemento, ou quase fixa. */
type Tinta = 'personagem' | 'elemento' | 'fixa';

export interface Familia {
  nome: string;
  grupo: Grupo;
  /** Folha do impacto, desenhada no alvo. */
  impacto: string;
  /** Folha que voa de quem age até o alvo (laço, aponta para +x). */
  viagem?: string;
  /** Folha esticada de quem age até o alvo (feixe, raio, dreno). */
  faixa?: string;
  /** Folha em laço sobre quem age enquanto prepara. */
  preparo?: string;
  /** O impacto gira para a direção do golpe (perfuração, lâmina). */
  aponta?: boolean;
  /** Segunda folha de impacto, menor, por baixo da principal (o clarão do contato num corte). */
  acento?: string;
  /** Rotação base do impacto, em graus (cortes diagonais). */
  giro?: number;
  /** Tamanho do impacto em relação ao medalhão. */
  escala: number;
  /** Fração do resto do beat que o impacto dura. */
  tempo: number;
  cor: string;
  tinta: Tinta;
  /** Som da biblioteca que acompanha (a parte 6 refaz a biblioteca inteira). */
}

const f = (x: Familia) => x;

const ORIGINAIS = {
  // ---------------------------------------------------------------- físico
  soco: f({ nome: 'Soco', grupo: 'físico', impacto: 'soco', escala: 1.5, tempo: 0.55, cor: '#ffd9a8', tinta: 'personagem' }),
  golpe_pesado: f({ nome: 'Golpe pesado', grupo: 'físico', impacto: 'golpe_pesado', escala: 1.9, tempo: 0.7, cor: '#ffc28a', tinta: 'personagem' }),
  esmagar: f({ nome: 'Esmagar', grupo: 'físico', impacto: 'esmagar', escala: 2.0, tempo: 0.75, cor: '#ffc28a', tinta: 'personagem' }),
  gancho: f({ nome: 'Gancho', grupo: 'físico', impacto: 'gancho', escala: 1.8, tempo: 0.65, cor: '#ffd9a8', tinta: 'personagem' }),
  terremoto: f({ nome: 'Terremoto', grupo: 'físico', impacto: 'terremoto', escala: 2.3, tempo: 0.8, cor: '#e8b77c', tinta: 'personagem' }),
  onda_de_choque: f({ nome: 'Onda de choque', grupo: 'físico', impacto: 'onda_de_choque', escala: 2.1, tempo: 0.7, cor: '#cfe6ff', tinta: 'personagem' }),
  rajada_de_golpes: f({ nome: 'Rajada de golpes', grupo: 'físico', impacto: 'rajada_de_golpes', escala: 1.8, tempo: 0.85, cor: '#ffd9a8', tinta: 'personagem' }),
  // ---------------------------------------------------------------- cortes
  corte: f({ nome: 'Corte', grupo: 'corte', acento: 'soco', impacto: 'corte', escala: 2.25, tempo: 0.75, giro: -10, cor: '#dff1ff', tinta: 'personagem' }),
  corte_diagonal: f({ nome: 'Corte diagonal', grupo: 'corte', acento: 'soco', impacto: 'corte', escala: 2.25, tempo: 0.75, giro: -42, cor: '#dff1ff', tinta: 'personagem' }),
  corte_cruzado: f({ nome: 'Corte cruzado', grupo: 'corte', acento: 'soco', impacto: 'corte_cruzado', escala: 2.25, tempo: 0.75, cor: '#dff1ff', tinta: 'personagem' }),
  estocada: f({ nome: 'Perfuração', grupo: 'corte', acento: 'soco', impacto: 'estocada', aponta: true, escala: 2.25, tempo: 0.75, cor: '#e6f4ff', tinta: 'personagem' }),
  corte_giratorio: f({ nome: 'Corte giratório', grupo: 'corte', acento: 'soco', impacto: 'corte_giratorio', escala: 2.35, tempo: 0.75, cor: '#dff1ff', tinta: 'personagem' }),
  corte_de_energia: f({ nome: 'Lâmina de energia', grupo: 'corte', viagem: 'crescente', impacto: 'corte_de_energia', aponta: true, escala: 2.0, tempo: 0.6, cor: '#9fe0ff', tinta: 'personagem' }),
  // ---------------------------------------------------------------- projéteis
  tiro: f({ nome: 'Tiro', grupo: 'projétil', viagem: 'tiro', impacto: 'soco', escala: 1.2, tempo: 0.45, cor: '#ffe0a0', tinta: 'personagem' }),
  saraivada: f({ nome: 'Rajada de tiros', grupo: 'projétil', viagem: 'saraivada', impacto: 'rajada_de_golpes', escala: 1.6, tempo: 0.75, cor: '#ffe0a0', tinta: 'personagem' }),
  missil: f({ nome: 'Míssil', grupo: 'projétil', viagem: 'missil', impacto: 'explosao', escala: 2.1, tempo: 0.75, cor: '#ffb070', tinta: 'personagem' }),
  esfera: f({ nome: 'Esfera de energia', grupo: 'projétil', viagem: 'orbe', impacto: 'pulso_de_energia', escala: 1.8, tempo: 0.65, cor: '#8fd8ff', tinta: 'personagem' }),
  esfera_carregada: f({ nome: 'Esfera carregada', grupo: 'projétil', preparo: 'carga', viagem: 'orbe', impacto: 'explosao', escala: 2.2, tempo: 0.8, cor: '#8fd8ff', tinta: 'personagem' }),
  // ---------------------------------------------------------------- energia
  feixe: f({ nome: 'Feixe', grupo: 'energia', faixa: 'feixe', impacto: 'soco', escala: 1.8, tempo: 0.55, cor: '#8fd8ff', tinta: 'personagem' }),
  feixe_pesado: f({ nome: 'Feixe pesado', grupo: 'energia', preparo: 'carga', faixa: 'feixe_pesado', impacto: 'explosao', escala: 2.2, tempo: 0.8, cor: '#8fd8ff', tinta: 'personagem' }),
  explosao: f({ nome: 'Explosão', grupo: 'energia', impacto: 'explosao', escala: 2.2, tempo: 0.8, cor: '#ffb070', tinta: 'personagem' }),
  onda_de_energia: f({ nome: 'Onda de energia', grupo: 'energia', viagem: 'crescente', impacto: 'onda_de_choque', escala: 2.0, tempo: 0.65, cor: '#a8e6ff', tinta: 'personagem' }),
  // ---------------------------------------------------------------- elementos
  fogo: f({ nome: 'Fogo', grupo: 'elemento', viagem: 'bola_de_fogo', impacto: 'fogo', escala: 2.0, tempo: 0.85, cor: '#ff7a2e', tinta: 'elemento' }),
  gelo: f({ nome: 'Gelo', grupo: 'elemento', viagem: 'estilhaco', impacto: 'gelo', escala: 1.9, tempo: 0.8, cor: '#8fe6ff', tinta: 'elemento' }),
  raio: f({ nome: 'Raio', grupo: 'elemento', faixa: 'raio_faixa', impacto: 'raio', acento: 'soco', escala: 1.9, tempo: 0.65, cor: '#ffe76a', tinta: 'elemento' }),
  vento: f({ nome: 'Vento', grupo: 'elemento', viagem: 'crescente', impacto: 'vento', escala: 2.0, tempo: 0.8, cor: '#bff5e4', tinta: 'elemento' }),
  agua: f({ nome: 'Água', grupo: 'elemento', viagem: 'orbe', impacto: 'agua', escala: 2.0, tempo: 0.8, cor: '#4fb4ff', tinta: 'elemento' }),
  terra: f({ nome: 'Terra', grupo: 'elemento', viagem: 'rocha', impacto: 'terra', escala: 2.0, tempo: 0.85, cor: '#d6a86a', tinta: 'elemento' }),
  veneno: f({ nome: 'Veneno', grupo: 'elemento', viagem: 'orbe', impacto: 'veneno', escala: 1.9, tempo: 0.85, cor: '#9be84a', tinta: 'elemento' }),
  sombra: f({ nome: 'Sombra', grupo: 'elemento', viagem: 'orbe', impacto: 'sombra', escala: 2.0, tempo: 0.85, cor: '#9a5cff', tinta: 'elemento' }),
  luz: f({ nome: 'Luz', grupo: 'elemento', impacto: 'luz', escala: 2.0, tempo: 0.85, cor: '#ffe9a3', tinta: 'elemento' }),
  // ---------------------------------------------------------------- magia e psíquico
  selo: f({ nome: 'Selo', grupo: 'magia', impacto: 'selo', escala: 2.0, tempo: 0.85, cor: '#c7a2ff', tinta: 'personagem' }),
  prisao: f({ nome: 'Prisão', grupo: 'magia', impacto: 'prisao', escala: 1.8, tempo: 0.9, cor: '#9fe1f3', tinta: 'personagem' }),
  distorcao: f({ nome: 'Distorção', grupo: 'magia', impacto: 'distorcao', escala: 1.9, tempo: 0.8, cor: '#d18cff', tinta: 'personagem' }),
  portal: f({ nome: 'Portal', grupo: 'magia', preparo: 'portal', impacto: 'portal', escala: 1.8, tempo: 0.8, cor: '#8f9dff', tinta: 'personagem' }),
  telecinese: f({ nome: 'Telecinese', grupo: 'magia', impacto: 'telecinese', escala: 2.0, tempo: 0.85, cor: '#d6a2ff', tinta: 'personagem' }),
  maldicao: f({ nome: 'Maldição', grupo: 'magia', impacto: 'maldicao', escala: 1.9, tempo: 0.9, cor: '#b45cff', tinta: 'elemento' }),
  // ---------------------------------------------------------------- apoio
  cura: f({ nome: 'Cura', grupo: 'apoio', impacto: 'cura', escala: 1.8, tempo: 0.9, cor: '#7dffb0', tinta: 'fixa' }),
  escudo: f({ nome: 'Escudo', grupo: 'apoio', impacto: 'escudo', escala: 1.7, tempo: 0.9, cor: '#8edeff', tinta: 'fixa' }),
  reforco: f({ nome: 'Reforço', grupo: 'apoio', impacto: 'reforco', escala: 1.8, tempo: 0.9, cor: '#ffd36b', tinta: 'elemento' }),
  dreno: f({ nome: 'Dreno', grupo: 'apoio', faixa: 'dreno', impacto: 'maldicao', escala: 1.6, tempo: 0.8, cor: '#ff6d8a', tinta: 'elemento' }),
  // ---------------------------------------------------------------- especial
  execucao: f({ nome: 'Execução', grupo: 'especial', impacto: 'execucao', escala: 2.3, tempo: 0.9, cor: '#e24a5a', tinta: 'fixa' }),
} as const satisfies Record<string, Familia>;

/* As 41 originais e as 122 novas (vfx-familias-novas.ts). */
export const VFX_FAMILIES = { ...ORIGINAIS, ...FAMILIAS_NOVAS };

export type VfxFamily = keyof typeof VFX_FAMILIES;
export const FAMILIAS = Object.keys(VFX_FAMILIES) as VfxFamily[];
export const familia = (k: VfxFamily): Familia => VFX_FAMILIES[k];

/** Folhas da linha de ação (quem vai atacar quem): a luz que corre, a mira no alvo, o apoio chegando. */
export const FOLHAS_DA_LINHA = ['cometa', 'mira', 'chegada'] as const;

/** Todas as folhas que o jogo usa. */
export const folhasUsadas = (): string[] => [...new Set([...FAMILIAS.flatMap((k) => {
  const x = familia(k);
  return [x.impacto, x.viagem, x.faixa, x.preparo, x.acento].filter((s): s is string => !!s);
}), ...FOLHAS_DA_LINHA])].sort();

export const folha = (nome: string) => `/assets/vfx/familias/${nome}.webp`;

export interface VfxProfile {
  family: VfxFamily;
  /** 0–3: muda giro, espelho e ritmo, para a mesma família não parecer carimbo. */
  variant: number;
  scale: number;
  travel: boolean;
  area: boolean;
  /** 0,82 (básico) a 1,4 (grande habilidade). */
  intensity: number;
  /** Cor final do efeito (já legível sobre a arena escura). */
  color: string;
}

/* =====================================================================
 * Cor
 * =================================================================== */

const hexRgb = (hex: string): [number, number, number] => {
  const h = hex.replace('#', '');
  const n = parseInt(h.length === 3 ? h.split('').map((c) => c + c).join('') : h.slice(0, 6), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
const rgbHex = (r: number, g: number, b: number) => '#' + [r, g, b].map((v) => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('');

export function rgbHsl([r, g, b]: [number, number, number]): [number, number, number] {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
  if (max === min) return [0, 0, l];
  const d = max - min, s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  const h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function hslHex(h: number, s: number, l: number): string {
  const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs(((h / 60) % 2) - 1)), m = l - c / 2;
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return rgbHex((r + m) * 255, (g + m) * 255, (b + m) * 255);
}
export const hsl = (hex: string) => rgbHsl(hexRgb(hex));

/** Mistura com gama 2: não escurece no meio. */
export function misturar(a: string, b: string, peso: number): string {
  const x = hexRgb(a), y = hexRgb(b);
  return rgbHex(...(x.map((v, i) => Math.sqrt(v * v * (1 - peso) + y[i] * y[i] * peso)) as [number, number, number]));
}

/**
 * Legível sobre a arena escura: saturação e luminosidade dentro de uma faixa.
 * Um personagem de cor quase preta ou acinzentada ainda produz um efeito que
 * se enxerga; a sombra pode ser um pouco mais escura que o resto.
 */
export function legivel(hex: string, escura = false): string {
  const [h, s, l] = hsl(hex);
  const sat = s < 0.08 ? s : Math.min(1, Math.max(s, 0.62));
  const lum = Math.min(escura ? 0.66 : 0.72, Math.max(escura ? 0.5 : 0.58, l));
  return hslHex(h, sat, lum);
}

export const normaliza = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

/* Cores que a habilidade tem no nome, mais fortes que a cor do personagem. */
const COR_DO_NOME: [RegExp, string][] = [
  [/azul|blue/, '#4aa8ff'],
  [/vermelh|\bred\b|sangue|blood|carmesim/, '#ff4a4a'],
  [/roxo|purple|violeta/, '#a76bff'],
  [/dourad|\bouro\b|golden/, '#ffd35a'],
  [/verde|green/, '#5fe36b'],
  [/negr|black|escurid/, '#8a5cff'],
  [/rosa\b|pink/, '#ff7ad1'],
];

/* As habilidades mais famosas, com a cor que todo mundo reconhece. */
const COR_ICONICA: Record<string, string> = {
  'goku:0': '#5ec8ff', 'goku:basic': '#7fd2ff',
  'vegeta:0': '#b77cff', 'vegeta:2': '#ffe66b', 'vegeta:basic': '#ffe66b',
  'superman:0': '#ff4a3a',
  'sasuke:0': '#8fd8ff', 'sasuke:1': '#8a5cff',
  'gojo:0': '#4aa8ff', 'gojo:1': '#ff4a4a', 'gojo:2': '#b48cff', 'gojo:basic': '#9fc4ff',
  'frieza:1': '#ff6bd5',
  'ichigo:0': '#7fd3ff',
  'naruto:1': '#7fd8ff',
  'kakashi:1': '#8fd8ff',
  'itachi:1': '#8a5cff', 'itachi:2': '#ff5a5a',
  'cyclops:0': '#ff4a4a',
  'ironman:0': '#9fe6ff', 'ironman:2': '#9fe6ff',
  'thanos:0': '#c77dff',
  'darkseid:0': '#ff4a3a',
  'greenlantern:0': '#5fe36b',
  'azula:0': '#4aa8ff',
  'subzero:0': '#8fe6ff',
  'hyoga:0': '#8fe6ff', 'camus:0': '#8fe6ff',
  'pikachu:0': '#ffe76a',
  'broly:0': '#7dff8a',
  'zenitsu:2': '#ffe76a',
  'ryu:0': '#7fd2ff', 'akuma:0': '#ff4a6a',
  'kuririn:0': '#ffe9a3',
  'raven:0': '#8a5cff', 'raven:2': '#8a5cff',
  'mewtwo:0': '#d18cff',
  'charizard:0': '#ff7a2e',
  'ghostrider:0': '#ff7a2e',
  'beerus:0': '#b48cff',
  'light:2': '#e24a5a',
};

export function corDoEfeito(k: VfxFamily, personagem: Character, chave: string, nome: string): string {
  const fam = familia(k);
  const escura = ['sombra', 'execucao', 'lamina_sombria', 'chama_negra', 'foice', 'asa_negra', 'buraco_negro', 'caveira', 'medo'].includes(k);
  const iconica = COR_ICONICA[`${personagem.id}:${chave}`];
  if (iconica) return legivel(iconica, escura);
  const doNome = COR_DO_NOME.find(([re]) => re.test(normaliza(nome)))?.[1];
  if (fam.tinta === 'fixa') return legivel(doNome ? misturar(fam.cor, doNome, 0.35) : misturar(fam.cor, personagem.color, 0.12), escura);
  if (fam.tinta === 'elemento') return legivel(doNome ?? misturar(fam.cor, personagem.color, 0.3), escura);
  return legivel(doNome ?? misturar(personagem.color, fam.cor, 0.15), escura);
}

/* =====================================================================
 * Qual família cada habilidade usa
 * =================================================================== */

/* Palavras do nome → família. A ordem importa: o primeiro que casar vence. */
const POR_NOME: [RegExp, VfxFamily][] = [
  [/death note|hakai|execu|sentenca|julgamento final/, 'execucao'],
  [/visao de calor|raio mortal|raio laser/, 'feixe'],
  [/kamehameha|final flash|galick|unibeam|feixe omega|big bang|canhao|cannon|eraser|masenko|makankosappo|hadouken/, 'feixe_pesado'],
  [/rasengan|genki|esfera|orbe|spirit bomb|bola de energia/, 'esfera_carregada'],
  [/getsuga|kienzan|disco|lamina de vento|crescente|cleave/, 'corte_de_energia'],
  [/fogo|chama|flame|fire|inferno|fenix|phoenix|incinera|igni|queim|amaterasu|lava|magma|brasa|calor|katon|incend/, 'fogo'],
  [/gelo|\bice\b|frio|congel|neve|diamante|frost|shirayuki|glacia/, 'gelo'],
  [/trov|eletri|chidori|raikiri|thunder|choque|relampago|tempestade|plasma|lightning|faisca|volt|raio celeste|raio magico|seis dobras/, 'raio'],
  [/vento|rajada de ar|tornado|furacao|redemoinho|ciclone|wind|dobra de ar/, 'vento'],
  [/agua|tsunami|tridente|water|aqua|hidro|oceano|\bmar\b|bolha/, 'agua'],
  [/pedra|rocha|sismic|\bterra\b|areia|\bsand\b|stone|earth|terremoto|avalanche|defesa absoluta/, 'terra'],
  [/veneno|toxic|acido|\bgas\b|poison|pestil|praga/, 'veneno'],
  [/dreno|absor|drain|sugar|vampir|inalar|roub/, 'dreno'],
  [/sombra|shadow|trevas|escur|noite|necro|\balma\b|abismo|ceifa|demon|infern|morte|tsukuyomi|genjutsu|caveira|fantasma|espiritos/, 'sombra'],
  [/\bluz\b|sagrad|holy|celest|\bsol\b|lunar|estrela|anjo|luminos|tesouro do ceu|aurora|tiara/, 'luz'],
  [/missil|missel|foguete|rocket|bomba|granada|explosiv|dinamite|acme/, 'missil'],
  [/explos|detona|colapso|supernova|galactica|nuclear|aniquila/, 'explosao'],
  [/gatling|star platinum|mil golpes|hyakuretsu|\bmuda\b|\bora\b|socos|combo|sequencia|nunchaku|bastao giratorio|quatro bracos|chicotes/, 'rajada_de_golpes'],
  [/metralh|saraivada|chuva de|facas voadoras|\bcarta|shuriken|kunai|agulhas|pregos|estilhac/, 'saraivada'],
  [/tiro|\bbala\b|pistola|disparo|revolver|rifle|\barco\b|flecha|estilingue|repulsor|buster|blaster|laser|\bmira\b|teia de impacto|lancar teia/, 'tiro'],
  [/feixe|\bbeam\b|visao de calor|raio mortal|rajada cosmica|rajada de contencao|rajada|\braio\b|joia do poder/, 'feixe'],
  [/portal|teleport|dimens|buraco|warp|hiraishin|deslocamento|faseamento|\bfase\b|clones|duplicata|multidao/, 'portal'],
  [/telecin|psiquico|magnet|gravidade|levita|empurr|\bmetal\b|corda puxada|muralha/, 'telecinese'],
  [/prisao|corrente|teia|\blaco\b|corda|amarr|chain|\bweb\b|algema|captura|raiz|bungee|armadilha|ratoeira|caixao/, 'prisao'],
  [/maldi|curse|\bhex\b|vodu|amaldi|azar|sangue corruptor|acordo|pacto|feitic/, 'maldicao'],
  [/selo|\bseal\b|ritual|runa|circulo|magia|encant|sharingan|byakugan|analise|leitura|investig|olfato|radar|percepcao|rastreio|varredura/, 'selo'],
  [/the world|o mundo|za warudo|ilus|hipnose|mental|mente|confus|\btempo\b|temporal|realidade|probabilidade|quarta parede|grito de pavor|risada|exijo|tropec/, 'distorcao'],
  [/rugido|grito|onda de choque|sonic|sonico|impacto|estrondo|kiai/, 'onda_de_choque'],
  [/onda|\bwave\b|pulso/, 'onda_de_energia'],
  [/garras|cruz|dupla|gemeas|duas espadas|desmantelar|laminas vivas/, 'corte_cruzado'],
  [/\bgir|spin|turbilhao|danca/, 'corte_giratorio'],
  [/estoc|lanca|perfur|espinho|\bponta\b|rapieira|chifre|ferrao|presas|chute voador/, 'estocada'],
  [/espada|lamina|corte|katana|machado|foice|adaga|faca|sabre|saber|serra|masamune|yamato|rebellion|bankai|alabarda/, 'corte'],
  [/esmag|smash|pisao|martelo|marreta|hammer|mjolnir|pulo|salto|queda|meteoro|bigorna/, 'esmagar'],
  [/uppercut|gancho|ascendente|shoryuken/, 'gancho'],
  [/investida|avanco|tackle|casco|forca bruta|titan|serio|monstruos|soco giratorio|mao da perdicao|punho sombrio|black flash|golpe/, 'golpe_pesado'],
  [/soco|punho|chute|murro|cabecada|tapa|joelh|cotovel|pisada/, 'soco'],
];

/* Hash estável do id: a variante sai sem sorteio, igual em toda luta. */
const hash = (s: string) => [...s].reduce((h, ch) => (Math.imul(h, 31) + ch.charCodeAt(0)) | 0, 7) >>> 0;

const ELEMENTOS: VfxFamily[] = ['fogo', 'gelo', 'raio', 'vento', 'agua', 'terra', 'veneno', 'sombra', 'luz'];
const TEMAS_SEM_DANO: VfxFamily[] = [...ELEMENTOS, 'prisao', 'distorcao', 'maldicao', 'portal', 'telecinese', 'selo'];
const BUFFS = new Set(['haste', 'strengthened', 'protected', 'regen']);

const temDano = (effects: Effect[]) => effects.some((e) => e.kind === 'damage' || e.kind === 'release' || e.kind === 'deathnote');
const statusDe = (effects: Effect[]) => effects.flatMap((e) => (e.kind === 'status' ? [e.status] : []));
const pelaPalavra = (nome: string) => POR_NOME.find(([re]) => re.test(normaliza(nome)))?.[1];

interface Ficha { icon: Visual; effects: Effect[]; target: Target; name: string; preparation: number }

/* Sem dano, o efeito manda: cura, Escudo, reforço, prisão, confusão, debuff. */
function porEfeito(s: Ficha): VfxFamily | undefined {
  const { effects } = s;
  if (effects.some((e) => e.kind === 'deathnote')) return 'execucao';
  if (effects.some((e) => e.kind === 'investigate')) return 'selo';
  if (temDano(effects)) return undefined;
  if (effects.some((e) => e.kind === 'heal')) return 'cura';
  if (effects.some((e) => e.kind === 'shield')) return 'escudo';
  const st = statusDe(effects);
  if (st.includes('regen')) return 'cura';
  if (st.length && st.every((x) => BUFFS.has(x))) return 'reforco';
  if (st.includes('paralyzed')) return 'raio';
  if (st.includes('rooted')) return 'prisao';
  if (st.some((x) => x === 'confused' || x === 'silenced')) return 'distorcao';
  if (st.length) return 'maldicao';
  return undefined;
}

function porIcone(s: Ficha): VfxFamily {
  switch (s.icon) {
    case 'beam': return s.preparation >= 1.5 ? 'feixe_pesado' : 'feixe';
    case 'bolt': return 'raio';
    case 'slash': return s.preparation >= 2 ? 'corte_giratorio' : 'corte';
    case 'web': return 'prisao';
    case 'shield': return temDano(s.effects) ? 'onda_de_choque' : 'escudo';
    case 'wave': return 'onda_de_energia';
    case 'psychic': return temDano(s.effects) ? 'telecinese' : 'distorcao';
    default: return s.preparation >= 2 ? 'golpe_pesado' : 'soco';
  }
}

/* O ataque básico é o "jeito de bater" do personagem, com o elemento dele se tiver um. */
const FISICOS: VfxFamily[] = ['soco', 'golpe_pesado', 'esmagar', 'gancho', 'rajada_de_golpes', 'estocada', 'corte', 'corte_diagonal', 'corte_cruzado', 'corte_giratorio'];
const JEITOS_DE_BATER: VfxFamily[] = ['soco', 'gancho', 'rajada_de_golpes', 'soco', 'golpe_pesado'];

function basicoDe(c: Character, familias: VfxFamily[], escolhidas: VfxFamily[] = []): VfxFamily {
  // quem tem uma família de identidade (garras, chicote, lâmina de fogo…) bate com ela também
  const propria = escolhidas.find((x) => NOVAS_DE_BASICO.has(x as FamiliaNova));
  if (propria) return propria;
  const v = c.basic.visual;
  const elemento = familias.find((x) => ELEMENTOS.includes(x));
  // quem tem um elemento de verdade (duas habilidades ou mais) bate com ele
  const marcado = elemento && familias.filter((x) => x === elemento).length >= 2 && v !== 'slash';
  if (elemento && (marcado || ['beam', 'bolt', 'wave', 'psychic'].includes(v))) return elemento;
  if (v === 'impact' || v === 'slash') {
    // bate do jeito das próprias habilidades: quem corta, corta; quem esmaga, esmaga
    const fisico = familias.find((x) => FISICOS.includes(x));
    if (fisico) return fisico.startsWith('corte') ? (fisico === 'corte_cruzado' ? 'corte_cruzado' : 'corte_diagonal') : fisico;
    if (v === 'impact') return JEITOS_DE_BATER[hash(c.id) % JEITOS_DE_BATER.length];
  }
  switch (v) {
    case 'beam': return 'esfera';
    case 'bolt': return 'raio';
    case 'slash': return 'corte_diagonal';
    case 'web': return 'tiro';
    case 'shield': return 'golpe_pesado';
    case 'wave': return 'onda_de_energia';
    case 'psychic': return 'distorcao';
    default: return 'soco';
  }
}

const ehArea = (target: Target, effects: Effect[]) => target === 'allEnemies' || target === 'allAllies' || effects.some((e) => e.target === 'allEnemies' || e.target === 'allAllies');

/** Família de uma habilidade (ou do básico, sem índice). */
export function familiaDe(c: Character, skillIndex?: number): VfxFamily {
  if (skillIndex === undefined) {
    const proprio = FAMILIA_DO_BASICO[c.id];
    if (proprio) return proprio;
    return basicoDe(c, c.skills.map((_, i) => familiaPelaRegra(c, i)), c.skills.map((_, i) => familiaDe(c, i)));
  }
  return FAMILIA_DA_HABILIDADE[`${c.id}:${skillIndex}`] ?? familiaPelaRegra(c, skillIndex);
}

/** A família pela regra (palavra do nome, efeito, ícone), sem a escolha da tabela. */
function familiaPelaRegra(c: Character, skillIndex: number): VfxFamily {
  const s = c.skills[skillIndex];
  const efeito = porEfeito(s);
  const palavra = pelaPalavra(s.name);
  if (efeito) {
    if (['reforco', 'cura', 'escudo', 'execucao', 'selo'].includes(efeito)) return efeito;
    // sem dano o efeito manda, mas o nome ainda dá o tema (prisão de gelo, confusão sombria…)
    return palavra && TEMAS_SEM_DANO.includes(palavra) ? palavra : efeito;
  }
  let fam = palavra ?? porIcone(s);
  const area = ehArea(s.target, s.effects);
  // golpes físicos em área viram tremor no chão; projéteis em área explodem
  if (area && ['soco', 'golpe_pesado', 'esmagar', 'gancho'].includes(fam)) fam = 'terremoto';
  if (area && ['esfera', 'tiro', 'feixe'].includes(fam)) fam = 'explosao';
  // dano com preparo longo pesa mais
  if (s.preparation >= 2.5 && fam === 'soco') fam = 'golpe_pesado';
  if (s.preparation >= 2.5 && fam === 'esfera') fam = 'esfera_carregada';
  return fam;
}

/* Estas acontecem no alvo, sem nada voando até ele. */
const NO_ALVO = new Set<VfxFamily>(['distorcao', 'maldicao', 'selo', 'telecinese', 'prisao', 'portal', 'luz', ...NOVAS_NO_ALVO]);

export function profileFor(characterId: string, skillIndex?: number): VfxProfile | undefined {
  const c = byId[characterId];
  if (!c) return undefined;
  const ficha: Ficha | undefined = skillIndex === undefined
    ? { icon: c.basic.visual, effects: c.basic.effects, target: c.basic.target, name: c.basic.name, preparation: 0 }
    : (c.skills[skillIndex] as Skill | undefined);
  if (!ficha) return undefined;
  const family = familiaDe(c, skillIndex);
  const fam = familia(family);
  const area = ehArea(ficha.target, ficha.effects);
  const proprio = ficha.target === 'self' || ficha.target === 'allAllies' || ficha.target === 'allyWeak';
  const travel = !proprio && !!(fam.viagem || fam.faixa) && !NO_ALVO.has(family);
  const intensity = skillIndex === undefined ? 0.82 : Math.min(1.4, 1 + skillIndex * 0.06 + (ficha.preparation >= 2.5 ? 0.22 : ficha.preparation >= 1.2 ? 0.1 : 0));
  const chave = skillIndex === undefined ? 'basic' : String(skillIndex);
  return {
    family,
    variant: hash(`${c.id}:${chave}`) % 4,
    scale: fam.escala * (0.86 + 0.14 * intensity),
    travel,
    area,
    intensity,
    color: corDoEfeito(family, c, chave, ficha.name),
  };
}
