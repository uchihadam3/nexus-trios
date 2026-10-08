/*
 * As famílias novas de efeito (122), desenhadas em Python em
 * tools/vfx/familias_v2 e com um som próprio cada uma (tools/audio/sfx_familias.py).
 *
 * Cada uma diz as folhas que usa (impacto, e às vezes viagem, faixa ou preparo),
 * o tamanho, quanto tempo dura, a cor de base e como a cor do personagem
 * entra; e o som: o impacto é sempre o som da própria família.
 */
import type { Familia } from './vfxProfiles';

type F = Omit<Familia, 'cor' | 'tinta' | 'escala' | 'tempo'> & Partial<Pick<Familia, 'cor' | 'tinta' | 'escala' | 'tempo'>>;
const n = (x: F): Familia => ({ escala: 1.9, tempo: 0.75, cor: '#dff1ff', tinta: 'personagem', ...x });

export const FAMILIAS_NOVAS = {
  // ------------------------------------------------------------ corpo
  chute_voador: n({ nome: 'Chute voador', grupo: 'físico', impacto: 'chute_voador', escala: 2.0, tempo: 0.65, cor: '#ffd9a8' }),
  chute_giratorio: n({ nome: 'Chute giratório', grupo: 'físico', impacto: 'chute_giratorio', escala: 2.1, cor: '#ffd9a8' }),
  bonk: n({ nome: 'Pancada de desenho', grupo: 'físico', impacto: 'bonk', escala: 1.9, tempo: 0.85, cor: '#ffe28a', tinta: 'elemento' }),
  pow_cartoon: n({ nome: 'POW!', grupo: 'físico', impacto: 'pow_cartoon', escala: 1.8, tempo: 0.7, cor: '#ffe066', tinta: 'elemento' }),
  martelo: n({ nome: 'Martelada', grupo: 'físico', impacto: 'martelo', escala: 2.2, tempo: 0.8, cor: '#ffd9a8' }),
  corrente: n({ nome: 'Corrente', grupo: 'físico', impacto: 'corrente', escala: 2.1, tempo: 0.9, cor: '#d8e4f0' }),
  marretada: n({ nome: 'Marretada de desenho', grupo: 'físico', impacto: 'marretada', escala: 2.2, tempo: 0.9, cor: '#ffcf8a', tinta: 'elemento' }),
  investida: n({ nome: 'Investida', grupo: 'físico', impacto: 'investida', escala: 2.1, tempo: 0.7, cor: '#ffc28a' }),
  punho_gigante: n({ nome: 'Punho gigante', grupo: 'físico', impacto: 'punho_gigante', escala: 2.2, tempo: 0.8, cor: '#ffc28a' }),
  soco_serio: n({ nome: 'Soco sério', grupo: 'físico', impacto: 'soco_serio', escala: 2.5, tempo: 0.9, cor: '#fff3d6', tinta: 'fixa' }),
  faisca_negra: n({ nome: 'Faísca negra', grupo: 'físico', impacto: 'faisca_negra', escala: 2.1, tempo: 0.7, cor: '#ff3355', tinta: 'fixa' }),
  chicote: n({ nome: 'Chicote', grupo: 'físico', impacto: 'chicote', escala: 2.1, tempo: 0.7 }),
  garras: n({ nome: 'Garras', grupo: 'corte', impacto: 'garras', escala: 2.1, tempo: 0.75, cor: '#e6f4ff' }),
  mordida: n({ nome: 'Mordida', grupo: 'físico', impacto: 'mordida', escala: 1.9, tempo: 0.7, cor: '#ffd9d9' }),
  bastao: n({ nome: 'Bastão', grupo: 'físico', impacto: 'bastao', escala: 2.0, tempo: 0.75, cor: '#ffd9a8' }),
  tentaculos: n({ nome: 'Tentáculos', grupo: 'físico', impacto: 'tentaculos', escala: 2.2, tempo: 0.85, cor: '#d04a6a' }),
  pisao: n({ nome: 'Pisão', grupo: 'físico', impacto: 'pisao', escala: 2.3, tempo: 0.85, cor: '#e8b77c' }),
  esticar: n({ nome: 'Braço elástico', grupo: 'físico', impacto: 'esticar', escala: 2.1, tempo: 0.8, cor: '#ffd9a8' }),
  // ------------------------------------------------------------ cortes
  corte_vertical: n({ nome: 'Corte vertical', grupo: 'corte', acento: 'soco', impacto: 'corte_vertical', escala: 2.2 }),
  iaido: n({ nome: 'Saque rápido', grupo: 'corte', impacto: 'iaido', escala: 2.3, tempo: 0.85 }),
  mil_cortes: n({ nome: 'Mil cortes', grupo: 'corte', impacto: 'mil_cortes', escala: 2.3, tempo: 0.9 }),
  foice: n({ nome: 'Foice', grupo: 'corte', impacto: 'foice', escala: 2.3, tempo: 0.85, cor: '#b49cff' }),
  espadao: n({ nome: 'Espadão', grupo: 'corte', impacto: 'espadao', escala: 2.4, tempo: 0.85 }),
  lamina_de_fogo: n({ nome: 'Lâmina de fogo', grupo: 'corte', impacto: 'lamina_de_fogo', escala: 2.3, cor: '#ff7a2e', tinta: 'elemento' }),
  lamina_eletrica: n({ nome: 'Lâmina elétrica', grupo: 'corte', impacto: 'lamina_eletrica', escala: 2.3, cor: '#ffe76a', tinta: 'elemento' }),
  lamina_sombria: n({ nome: 'Lâmina sombria', grupo: 'corte', impacto: 'lamina_sombria', escala: 2.3, cor: '#9a5cff', tinta: 'elemento' }),
  motosserra: n({ nome: 'Motosserra', grupo: 'corte', impacto: 'motosserra', escala: 2.0, tempo: 0.85, cor: '#ffb070' }),
  lamina_de_agua: n({ nome: 'Lâmina de água', grupo: 'corte', impacto: 'lamina_de_agua', escala: 2.3, tempo: 0.85, cor: '#4fb4ff', tinta: 'elemento' }),
  disco: n({ nome: 'Disco arremessado', grupo: 'projétil', viagem: 'disco', impacto: 'ricochete', escala: 1.9, tempo: 0.65 }),
  florete: n({ nome: 'Estocadas finas', grupo: 'corte', impacto: 'florete', escala: 2.1, tempo: 0.8 }),
  // ------------------------------------------------------------ projéteis
  flecha: n({ nome: 'Flecha', grupo: 'projétil', viagem: 'flecha', impacto: 'cravar', aponta: true, escala: 1.6, tempo: 0.6 }),
  tiro_preciso: n({ nome: 'Tiro de precisão', grupo: 'projétil', viagem: 'tiro', impacto: 'tiro_preciso', escala: 1.8, tempo: 0.7, cor: '#ffe0a0' }),
  espingarda: n({ nome: 'Espingarda', grupo: 'projétil', viagem: 'saraivada', impacto: 'espingarda', escala: 1.9, tempo: 0.7, cor: '#ffe0a0' }),
  teia: n({ nome: 'Teia', grupo: 'projétil', viagem: 'teia_bola', impacto: 'teia_rede', escala: 1.9, tempo: 0.9, cor: '#f2f7ff', tinta: 'fixa' }),
  bolhas: n({ nome: 'Bolhas', grupo: 'elemento', impacto: 'bolhas', escala: 1.9, tempo: 0.9, cor: '#7fd6ff', tinta: 'elemento' }),
  cartas: n({ nome: 'Cartas', grupo: 'projétil', viagem: 'cartas_voando', impacto: 'cartas_explosivas', escala: 2.0, tempo: 0.85, cor: '#ff7ad1' }),
  facas: n({ nome: 'Facas', grupo: 'projétil', viagem: 'facas_voando', impacto: 'cravar', escala: 1.7, tempo: 0.6, cor: '#e6f4ff' }),
  foguete: n({ nome: 'Foguete', grupo: 'projétil', viagem: 'foguete', impacto: 'explosao_grande', escala: 2.3, tempo: 0.85, cor: '#ffb070' }),
  bomba: n({ nome: 'Bomba', grupo: 'projétil', viagem: 'bomba', impacto: 'explosao_cartoon', escala: 2.1, tempo: 0.85, cor: '#ffb070' }),
  canhao: n({ nome: 'Bala de canhão', grupo: 'projétil', viagem: 'bala_de_canhao', impacto: 'explosao_grande', escala: 2.2, tempo: 0.85, cor: '#ffb070' }),
  gas: n({ nome: 'Gás', grupo: 'elemento', impacto: 'gas', escala: 2.1, tempo: 0.95, cor: '#9be84a', tinta: 'elemento' }),
  laser: n({ nome: 'Laser', grupo: 'energia', faixa: 'laser', impacto: 'queimadura', escala: 1.6, tempo: 0.6, cor: '#ff4a4a' }),
  // ------------------------------------------------------------ energia
  hadouken: n({ nome: 'Bola de ki', grupo: 'energia', viagem: 'bola_ki', impacto: 'explosao_ki', escala: 1.9, tempo: 0.7, cor: '#8fd8ff' }),
  kamehameha: n({ nome: 'Onda de ki', grupo: 'energia', preparo: 'carga_ki', faixa: 'feixe_ki', impacto: 'explosao_ki', escala: 2.3, tempo: 0.85, cor: '#5ec8ff' }),
  canhao_de_energia: n({ nome: 'Canhão de energia', grupo: 'energia', preparo: 'carga', faixa: 'canhao_de_energia', impacto: 'explosao_ki', escala: 2.3, tempo: 0.85, cor: '#9fe6ff' }),
  esfera_espiral: n({ nome: 'Esfera espiral', grupo: 'energia', preparo: 'carga_ki', impacto: 'esfera_espiral', escala: 2.0, tempo: 0.9, cor: '#7fd8ff' }),
  buraco_negro: n({ nome: 'Buraco negro', grupo: 'energia', impacto: 'buraco_negro', escala: 2.2, tempo: 0.95, cor: '#a07cff' }),
  gravidade: n({ nome: 'Gravidade', grupo: 'energia', impacto: 'gravidade', escala: 2.2, tempo: 0.9, cor: '#b48cff' }),
  cosmico: n({ nome: 'Cosmos', grupo: 'energia', impacto: 'cosmico', escala: 2.2, tempo: 0.9, cor: '#c7a2ff' }),
  chuva_de_meteoros: n({ nome: 'Chuva de meteoros', grupo: 'energia', impacto: 'chuva_de_meteoros', escala: 2.3, tempo: 0.95, cor: '#ffd08a' }),
  supernova: n({ nome: 'Supernova', grupo: 'energia', impacto: 'supernova', escala: 2.4, tempo: 0.9, cor: '#fff0b0' }),
  pulso_emp: n({ nome: 'Pulso eletromagnético', grupo: 'energia', impacto: 'pulso_emp', escala: 2.0, tempo: 0.8, cor: '#7fe7ff', tinta: 'elemento' }),
  pilar: n({ nome: 'Pilar de energia', grupo: 'energia', impacto: 'pilar', escala: 2.2, tempo: 0.9 }),
  transformacao: n({ nome: 'Transformação', grupo: 'energia', impacto: 'transformacao', escala: 2.2, tempo: 0.95, cor: '#ffe66b' }),
  atracao: n({ nome: 'Atração', grupo: 'energia', impacto: 'atracao', escala: 2.1, tempo: 0.9, cor: '#4aa8ff' }),
  repulsao: n({ nome: 'Repulsão', grupo: 'energia', impacto: 'repulsao', escala: 2.2, tempo: 0.8, cor: '#ff4a4a' }),
  dominio: n({ nome: 'Domínio', grupo: 'especial', impacto: 'dominio', escala: 2.4, tempo: 0.95, cor: '#b48cff' }),
  plasma: n({ nome: 'Plasma', grupo: 'energia', impacto: 'plasma', escala: 1.9, tempo: 0.85, cor: '#ff6bd5', tinta: 'elemento' }),
  desintegrar: n({ nome: 'Desintegrar', grupo: 'especial', impacto: 'desintegrar', escala: 2.1, tempo: 0.95, cor: '#c7a2ff', tinta: 'fixa' }),
  // ------------------------------------------------------------ elementos
  labareda: n({ nome: 'Labareda', grupo: 'elemento', impacto: 'labareda', escala: 2.2, tempo: 0.9, cor: '#ff7a2e', tinta: 'elemento' }),
  sopro_de_fogo: n({ nome: 'Sopro de fogo', grupo: 'elemento', impacto: 'sopro_de_fogo', escala: 2.2, tempo: 0.9, cor: '#ff8a3a', tinta: 'elemento' }),
  fenix: n({ nome: 'Fênix', grupo: 'elemento', impacto: 'fenix', escala: 2.3, tempo: 0.9, cor: '#ff9a3a', tinta: 'elemento' }),
  chama_negra: n({ nome: 'Chama negra', grupo: 'elemento', impacto: 'chama_negra', escala: 2.1, tempo: 0.95, cor: '#6a3cff', tinta: 'fixa' }),
  dragao: n({ nome: 'Dragão', grupo: 'elemento', impacto: 'dragao', escala: 2.3, tempo: 0.9, cor: '#ff8a3a' }),
  nevasca: n({ nome: 'Nevasca', grupo: 'elemento', impacto: 'nevasca', escala: 2.2, tempo: 0.95, cor: '#bfefff', tinta: 'elemento' }),
  bloco_de_gelo: n({ nome: 'Bloco de gelo', grupo: 'elemento', impacto: 'bloco_de_gelo', escala: 1.9, tempo: 0.95, cor: '#8fe6ff', tinta: 'elemento' }),
  espinho_de_gelo: n({ nome: 'Espinho de gelo', grupo: 'elemento', impacto: 'espinho_de_gelo', escala: 2.1, tempo: 0.85, cor: '#8fe6ff', tinta: 'elemento' }),
  tempestade: n({ nome: 'Tempestade', grupo: 'elemento', impacto: 'tempestade', escala: 2.3, tempo: 0.95, cor: '#ffe76a', tinta: 'elemento' }),
  raio_em_cadeia: n({ nome: 'Raio em cadeia', grupo: 'elemento', impacto: 'raio_em_cadeia', escala: 2.2, tempo: 0.8, cor: '#ffe76a', tinta: 'elemento' }),
  chidori: n({ nome: 'Mil pássaros', grupo: 'elemento', impacto: 'chidori', escala: 2.1, tempo: 0.85, cor: '#9fd8ff' }),
  tsunami: n({ nome: 'Tsunami', grupo: 'elemento', impacto: 'tsunami', escala: 2.4, tempo: 0.95, cor: '#4fb4ff', tinta: 'elemento' }),
  jato_dagua: n({ nome: 'Jato d’água', grupo: 'elemento', faixa: 'jato_dagua', impacto: 'agua', escala: 1.9, tempo: 0.8, cor: '#4fb4ff', tinta: 'elemento' }),
  areia: n({ nome: 'Areia', grupo: 'elemento', impacto: 'areia', escala: 2.1, tempo: 0.95, cor: '#e8c47c', tinta: 'elemento' }),
  espinhos_de_terra: n({ nome: 'Espinhos de terra', grupo: 'elemento', impacto: 'espinhos_de_terra', escala: 2.3, tempo: 0.85, cor: '#d6a86a', tinta: 'elemento' }),
  metal: n({ nome: 'Metal', grupo: 'elemento', impacto: 'metal', escala: 2.0, tempo: 0.9, cor: '#c9d6e3', tinta: 'elemento' }),
  tornado: n({ nome: 'Tornado', grupo: 'elemento', impacto: 'tornado', escala: 2.3, tempo: 0.95, cor: '#bff5e4', tinta: 'elemento' }),
  rajada_de_ar: n({ nome: 'Rajada de ar', grupo: 'elemento', impacto: 'rajada_de_ar', escala: 2.1, tempo: 0.8, cor: '#bff5e4', tinta: 'elemento' }),
  vinhas: n({ nome: 'Vinhas', grupo: 'elemento', impacto: 'vinhas', escala: 2.0, tempo: 0.95, cor: '#7ed957', tinta: 'elemento' }),
  petalas: n({ nome: 'Pétalas', grupo: 'elemento', impacto: 'petalas', escala: 2.1, tempo: 0.95, cor: '#ff7aa8', tinta: 'elemento' }),
  enxame: n({ nome: 'Enxame', grupo: 'elemento', impacto: 'enxame', escala: 2.0, tempo: 0.95, cor: '#ffcf5a' }),
  acido: n({ nome: 'Ácido', grupo: 'elemento', impacto: 'acido', escala: 1.9, tempo: 0.95, cor: '#b6f04a', tinta: 'elemento' }),
  sangue: n({ nome: 'Sangue', grupo: 'elemento', impacto: 'sangue', escala: 2.0, tempo: 0.85, cor: '#e2334a', tinta: 'fixa' }),
  radiacao: n({ nome: 'Radiação', grupo: 'elemento', impacto: 'radiacao', escala: 2.0, tempo: 0.95, cor: '#7dff6a', tinta: 'fixa' }),
  lua: n({ nome: 'Lua', grupo: 'elemento', impacto: 'lua', escala: 2.1, tempo: 0.95, cor: '#dfe8ff', tinta: 'elemento' }),
  raio_divino: n({ nome: 'Raio divino', grupo: 'elemento', impacto: 'raio_divino', escala: 2.3, tempo: 0.9, cor: '#ffe9a3', tinta: 'elemento' }),
  rugido: n({ nome: 'Rugido', grupo: 'físico', impacto: 'rugido', escala: 2.2, tempo: 0.85 }),
  // ------------------------------------------------------------ magia
  olho: n({ nome: 'Olho', grupo: 'magia', impacto: 'olho', escala: 2.1, tempo: 0.95, cor: '#ff5a5a' }),
  hipnose: n({ nome: 'Hipnose', grupo: 'magia', impacto: 'hipnose', escala: 2.0, tempo: 0.95, cor: '#d18cff' }),
  relogio: n({ nome: 'Tempo', grupo: 'magia', impacto: 'relogio', escala: 2.1, tempo: 0.95, cor: '#ffe9a3' }),
  runas: n({ nome: 'Runas', grupo: 'magia', impacto: 'runas', escala: 2.1, tempo: 0.95, cor: '#c7a2ff' }),
  sarcofago: n({ nome: 'Sarcófago', grupo: 'magia', impacto: 'sarcofago', escala: 2.0, tempo: 0.95, cor: '#9a7cff' }),
  encanto: n({ nome: 'Encanto', grupo: 'magia', impacto: 'encanto', escala: 2.0, tempo: 0.9, cor: '#ffe9a3' }),
  caveira: n({ nome: 'Caveira', grupo: 'magia', impacto: 'caveira', escala: 2.0, tempo: 0.95, cor: '#b6ffcf' }),
  clones: n({ nome: 'Clones', grupo: 'magia', impacto: 'clones', escala: 2.1, tempo: 0.95 }),
  teleporte: n({ nome: 'Teleporte', grupo: 'magia', impacto: 'teleporte', escala: 2.0, tempo: 0.8 }),
  fenda: n({ nome: 'Fenda dimensional', grupo: 'magia', impacto: 'fenda', escala: 2.2, tempo: 0.95, cor: '#8f9dff' }),
  sorte: n({ nome: 'Sorte', grupo: 'magia', impacto: 'sorte', escala: 2.0, tempo: 0.95, cor: '#ffe066', tinta: 'elemento' }),
  confete: n({ nome: 'Confete', grupo: 'especial', impacto: 'confete', escala: 2.1, tempo: 0.95, cor: '#ffd36b' }),
  confusao: n({ nome: 'Confusão', grupo: 'magia', impacto: 'confusao', escala: 2.0, tempo: 0.95, cor: '#ffe066', tinta: 'elemento' }),
  clarao_solar: n({ nome: 'Clarão solar', grupo: 'especial', impacto: 'clarao_solar', escala: 2.2, tempo: 0.8, cor: '#fff6c8', tinta: 'fixa' }),
  pentagrama: n({ nome: 'Pentagrama', grupo: 'magia', impacto: 'pentagrama', escala: 2.2, tempo: 0.95, cor: '#ff4a3a', tinta: 'elemento' }),
  invocacao: n({ nome: 'Invocação', grupo: 'magia', impacto: 'invocacao', escala: 2.1, tempo: 0.95 }),
  lua_vermelha: n({ nome: 'Lua vermelha', grupo: 'especial', impacto: 'lua_vermelha', escala: 2.3, tempo: 0.95, cor: '#ff3a3a', tinta: 'fixa' }),
  susanoo: n({ nome: 'Guerreiro espectral', grupo: 'especial', impacto: 'susanoo', escala: 2.4, tempo: 0.95, cor: '#a07cff' }),
  asa_negra: n({ nome: 'Asa negra', grupo: 'magia', impacto: 'asa_negra', escala: 2.2, tempo: 0.95, cor: '#8a7cff' }),
  // ------------------------------------------------------------ apoio e Status
  cura_em_area: n({ nome: 'Cura em área', grupo: 'apoio', impacto: 'cura_em_area', escala: 2.0, tempo: 0.95, cor: '#7dffb0', tinta: 'fixa' }),
  regeneracao: n({ nome: 'Regeneração', grupo: 'apoio', impacto: 'regeneracao', escala: 1.9, tempo: 0.95, cor: '#7dffb0', tinta: 'fixa' }),
  grito_de_guerra: n({ nome: 'Grito de guerra', grupo: 'apoio', impacto: 'grito_de_guerra', escala: 2.0, tempo: 0.9, cor: '#ffd36b', tinta: 'elemento' }),
  velocidade: n({ nome: 'Velocidade', grupo: 'apoio', impacto: 'velocidade', escala: 1.9, tempo: 0.9, cor: '#bff5e4', tinta: 'elemento' }),
  escudo_tech: n({ nome: 'Escudo tecnológico', grupo: 'apoio', impacto: 'escudo_tech', escala: 1.8, tempo: 0.95, cor: '#7fe7ff', tinta: 'elemento' }),
  barreira_magica: n({ nome: 'Barreira mágica', grupo: 'apoio', impacto: 'barreira_magica', escala: 1.9, tempo: 0.95, cor: '#c7a2ff', tinta: 'elemento' }),
  escudo_fisico: n({ nome: 'Escudo de mão', grupo: 'apoio', impacto: 'escudo_fisico', escala: 1.8, tempo: 0.85, cor: '#8edeff', tinta: 'elemento' }),
  armadura: n({ nome: 'Armadura', grupo: 'apoio', impacto: 'armadura', escala: 1.8, tempo: 0.95, cor: '#c9d6e3', tinta: 'elemento' }),
  resgate: n({ nome: 'Resgate', grupo: 'apoio', impacto: 'resgate', escala: 1.9, tempo: 0.9, cor: '#8edeff', tinta: 'elemento' }),
  bencao: n({ nome: 'Bênção', grupo: 'apoio', impacto: 'bencao', escala: 2.0, tempo: 0.95, cor: '#ffe9a3', tinta: 'fixa' }),
  lanche: n({ nome: 'Lanche', grupo: 'apoio', impacto: 'lanche', escala: 1.8, tempo: 0.95, cor: '#ffcf8a', tinta: 'fixa' }),
  purificacao: n({ nome: 'Purificação', grupo: 'apoio', impacto: 'purificar_onda', escala: 1.9, tempo: 0.95, cor: '#e8fbff', tinta: 'fixa' }),
  enfraquecimento: n({ nome: 'Enfraquecimento', grupo: 'apoio', impacto: 'enfraquecer', escala: 1.9, tempo: 0.95, cor: '#b3a2c9', tinta: 'fixa' }),
  lentidao: n({ nome: 'Lentidão', grupo: 'apoio', impacto: 'lentidao', escala: 1.9, tempo: 0.95, cor: '#9fc3e0', tinta: 'fixa' }),
  marca: n({ nome: 'Marca', grupo: 'apoio', impacto: 'marca', escala: 1.9, tempo: 0.9, cor: '#ff5a5a', tinta: 'fixa' }),
  silencio: n({ nome: 'Silêncio', grupo: 'apoio', impacto: 'silencio', escala: 1.9, tempo: 0.95, cor: '#c3a2ff', tinta: 'fixa' }),
  medo: n({ nome: 'Medo', grupo: 'apoio', impacto: 'medo', escala: 2.0, tempo: 0.95, cor: '#c84aff', tinta: 'fixa' }),
  exposto: n({ nome: 'Guarda quebrada', grupo: 'apoio', impacto: 'exposto', escala: 1.9, tempo: 0.9, cor: '#ff9475', tinta: 'fixa' }),
  estrela_invencivel: n({ nome: 'Estrela invencível', grupo: 'especial', impacto: 'estrela_invencivel', escala: 2.0, tempo: 0.95, cor: '#ffe066', tinta: 'fixa' }),
} as const satisfies Record<string, Familia>;

export type FamiliaNova = keyof typeof FAMILIAS_NOVAS;

/** O som próprio de cada família nova (nome do arquivo em public/assets/audio/sfx). */
export const SOM_DA_NOVA = (k: FamiliaNova): string => (k === 'transformacao' ? 'transformacao-v2' : k.replace(/_/g, '-'));

/** Estas acontecem no alvo, sem nada voando até ele. */
export const NOVAS_NO_ALVO = new Set<FamiliaNova>(['olho', 'hipnose', 'relogio', 'runas', 'sarcofago', 'encanto', 'caveira', 'clones',
  'teleporte', 'fenda', 'sorte', 'confusao', 'pentagrama', 'invocacao', 'lua_vermelha', 'susanoo', 'dominio', 'desintegrar', 'buraco_negro',
  'gravidade', 'cosmico', 'tempestade', 'raio_divino', 'chuva_de_meteoros', 'lua', 'marca', 'silencio', 'medo', 'exposto', 'lentidao', 'enfraquecimento']);

/** Bons para o ataque básico do personagem (quando ele já usa a família numa habilidade). */
export const NOVAS_DE_BASICO = new Set<FamiliaNova>(['garras', 'chicote', 'corrente', 'bastao', 'mordida', 'tentaculos', 'florete', 'lamina_de_fogo',
  'lamina_eletrica', 'lamina_sombria', 'lamina_de_agua', 'motosserra', 'espadao', 'foice', 'iaido', 'chute_voador', 'bonk', 'pow_cartoon',
  'flecha', 'facas', 'espingarda']);
