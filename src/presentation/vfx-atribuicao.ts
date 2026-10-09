/*
 * Que efeito cada habilidade usa, escolhido uma a uma.
 *
 * As regras por palavra (vfxProfiles.ts) acertam o tema, mas com 250 lutadores
 * metade das habilidades caía em "corte", "soco" ou "escudo". Aqui cada
 * habilidade marcante ganha a família que conta a história dela: o Azul do
 * Gojo puxa, o Vermelho empurra, o Vazio Infinito abre um domínio; o Hakai
 * desintegra; o Chidori canta; a Galick Gun é uma onda de ki. O que não está
 * aqui (marcado com "-") continua com a regra por palavra.
 *
 * Cada linha: as famílias das habilidades 0, 1 e 2 do personagem.
 */
import type { VfxFamily } from './vfxProfiles';

const T: Record<string, string> = {
  goku: 'kamehameha transformacao transformacao', vegeta: 'kamehameha transformacao -', naruto: 'clones esfera_espiral transformacao',
  sasuke: 'chidori chama_negra hipnose', luffy: '- esticar transformacao', gojo: 'atracao repulsao dominio',
  light: 'olho marca -', pikachu: '- raio_em_cadeia velocidade', saitama: '- resgate soco_serio',
  wolverine: 'garras armadura regeneracao', batman: 'marca disco escudo_tech', superman: 'laser resgate -',
  spiderman: 'teia resgate teia', hulk: '- rugido punho_gigante', thor: 'martelo tempestade raio_em_cadeia',
  strange: 'barreira_magica relogio portal', flash: '- resgate velocidade', wonderwoman: 'chicote escudo_fisico investida',
  ironman: 'feixe escudo_tech canhao_de_energia', captain: 'disco escudo_fisico grito_de_guerra', magneto: 'metal - gravidade',
  deadpool: 'pow_cartoon confusao regeneracao', raven: 'runas - asa_negra', thanos: 'plasma relogio desintegrar',
  gohan: 'pilar grito_de_guerra kamehameha', piccolo: 'marca esticar regeneracao', frieza: 'disco laser transformacao',
  kakashi: 'olho chidori clones', itachi: 'lua_vermelha - susanoo', sakura: 'pisao punho_gigante cura_em_area',
  tanjiro: 'marca lamina_de_agua lamina_de_fogo', nezuko: 'sangue labareda transformacao', zenitsu: 'iaido velocidade lamina_eletrica',
  inosuke: 'olho garras investida', muzan: 'tentaculos acido regeneracao', yuji: '- faisca_negra -',
  megumi: 'inv_cao tempestade -', nobara: 'facas maldicao explosao', sukuna: 'mil_cortes corte_vertical mil_cortes',
  ichigo: '- transformacao lamina_sombria', rukia: 'espinho_de_gelo nevasca bloco_de_gelo', aizen: 'hipnose sarcofago olho',
  kenpachi: 'espadao corte_vertical transformacao', eren: 'punho_gigante armadura rugido', mikasa: 'investida - iaido',
  levi: 'marca - -', gon: 'punho_gigante corte_vertical hadouken', killua: 'clones raio raio_em_cadeia',
  hisoka: 'esticar cartas teia', kurapika: 'corrente corrente olho', edward: 'espinhos_de_terra runas metal',
  alphonse: 'armadura cura_em_area barreira_magica', roy: 'sopro_de_fogo chuva_de_meteoros labareda', guts: 'espadao armadura -',
  griffith: 'marca grito_de_guerra asa_negra', jotaro: 'inv_ora rajada_de_golpes relogio', dio: '- facas relogio',
  giorno: 'vinhas barreira_magica cura_em_area', denji: 'motosserra sangue mil_cortes', power: '- martelo sangue',
  makima: 'olho - hipnose', frieren: 'runas laser encanto', anya: 'olho resgate -',
  loid: 'clones silencio velocidade', yor: 'facas chute_voador petalas', jinwoo: 'invocacao grito_de_guerra inv_sombras',
  kaneki: 'tentaculos mordida tentaculos', yugi: 'cartas inv_mago runas', kaiba: 'canhao_de_energia inv_dragao supernova',
  blackpanther: 'armadura garras repulsao', scarletwitch: 'sorte - fenda', vision: 'teleporte laser pulso_emp',
  antman: 'atracao enxame punho_gigante', captainmarvel: 'cosmico hadouken supernova', daredevil: 'marca bastao bastao',
  punisher: 'marca espingarda tiro_preciso', ghostrider: 'corrente olho labareda', blade: 'marca iaido -',
  moonknight: 'lua disco raio_divino', storm: 'tornado raio_em_cadeia tempestade', cyclops: 'canhao_de_energia laser -',
  jeangrey: '- - fenix', rogue: '- - clones', gambit: 'cartas cartas bastao',
  professorx: 'olho hipnose silencio', venom: 'tentaculos mordida tentaculos', carnage: 'garras sangue mil_cortes',
  doctordoom: 'laser pentagrama canhao_de_energia', loki: 'clones teleporte hipnose', ultron: 'pulso_emp escudo_tech laser',
  greengoblin: 'bomba gas foguete', silversurfer: 'cosmico velocidade fenda', galactus: '- cosmico buraco_negro',
  starlord: 'espingarda grito_de_guerra confete', groot: '- regeneracao vinhas', rocket: 'bomba foguete espingarda',
  aquaman: 'jato_dagua bolhas tsunami', greenlantern: 'escudo_fisico punho_gigante martelo', cyborg: 'pulso_emp canhao_de_energia laser',
  shazam: 'raio_divino grito_de_guerra encanto', cloud: 'corte_vertical escudo_fisico mil_cortes', tifa: 'exposto - -',
  sephiroth: 'iaido lamina_sombria asa_negra', kratos: 'lamina_de_fogo rugido labareda', link: '- escudo_fisico -',
  zelda: 'selo barreira_magica flecha', ganondorf: 'faisca_negra runas raio_divino', samus: 'marca missil esfera_carregada',
  dante: 'espadao saraivada transformacao', vergil: 'iaido fenda mil_cortes', bayonetta: 'chute_giratorio relogio inv_gomorrah',
  masterchief: 'escudo_tech saraivada pisao', doomslayer: 'investida armadura espinhos_de_terra', snake: 'teleporte tiro_preciso silencio',
  raidenmgr: 'lamina_eletrica mil_cortes iaido', leon: '- tiro_preciso corte_vertical', jill: 'cura grito_de_guerra armadura',
  wesker: 'teleporte rajada_de_golpes olho', lara: 'flecha - tiro_preciso', ezio: 'clones florete -',
  sonic: 'investida resgate transformacao', shadowhh: 'flecha relogio chuva_de_meteoros', megaman: 'hadouken plasma esfera_carregada',
  zeromm: 'lamina_eletrica iaido mil_cortes', mario: 'bonk - estrela_invencivel', bowser: 'investida sopro_de_fogo pisao',
  ryu: 'hadouken - canhao_de_energia', chunli: '- chute_giratorio repulsao', akuma: 'hadouken teleporte execucao',
  scorpion: 'chicote teleporte sopro_de_fogo', subzero: '- bloco_de_gelo nevasca', liukang: 'chute_voador - dragao',
  raidenmk: 'tempestade - raio_divino', jin: '- chute_voador asa_negra', kazuya: 'pisao laser transformacao',
  sora: '- - grito_de_guerra', tuob: 'corte_giratorio laser espadao', sekiro: 'escudo_fisico iaido execucao',
  malenia: '- mil_cortes petalas', agent47: 'clones chicote tiro_preciso', arthas: 'foice invocacao -',
  geralt: 'barreira_magica sopro_de_fogo hipnose', isaac: 'laser lentidao corte_vertical', gordon: 'bastao telecinese repulsao',
  hayabusa: 'iaido tornado esmagar', pyramidhead: 'espadao medo -', kirby: 'atracao encanto tornado',
  donkeykong: 'punho_gigante canhao -', simonbelmont: 'chicote - disco', princeofpersia: 'florete relogio areia',
  alucardcv: '- teleporte caveira', seiya: 'rajada_de_golpes cosmico investida', majinbuu: 'laser regeneracao pow_cartoon',
  kuririn: 'disco clarao_solar kamehameha', shiryu: 'escudo_fisico dragao pilar', hyoga: 'nevasca bloco_de_gelo bloco_de_gelo',
  shun: 'corrente tornado -', ikki: 'fenix hipnose renascer', saga: 'cosmico fenda hipnose',
  shaka: 'olho barreira_magica dominio', aiolia: 'plasma raio_em_cadeia rugido', camus: 'nevasca bloco_de_gelo espinho_de_gelo',
  hadescz: 'dominio medo caveira', madara: 'susanoo chuva_de_meteoros lua_vermelha', pain: 'gravidade repulsao buraco_negro',
  minato: 'teleporte esfera_espiral marca', gaara: '- areia areia', trunks: 'mil_cortes hadouken corte_vertical',
  cell: '- transformacao supernova', broly: 'esfera_carregada transformacao rugido', beerus: 'desintegrar - repulsao',
  mewtwo: '- barreira_magica hipnose', charizard: 'sopro_de_fogo garras labareda', garou: 'lamina_de_agua chute_giratorio garras',
  genos: 'canhao_de_energia foguete pulso_emp', yusuke: 'punho_gigante hadouken espingarda', hiei: 'lamina_de_fogo olho dragao',
  sailormoon: 'disco purificacao ressurreicao', coringa: 'gas cartas bomba', arlequina: 'marretada chute_giratorio bomba',
  darkseid: 'laser punho_gigante hipnose', lexluthor: 'canhao radiacao enfraquecimento', spawn: 'corrente tentaculos labareda',
  invencivel: '- velocidade pow_cartoon', omniman: 'punho_gigante investida sangue', leonardo: '- grito_de_guerra investida',
  raphael: 'florete investida pow_cartoon', donatello: 'bastao pulso_emp escudo_tech', michelangelo: '- chute_giratorio confete',
  constantine: 'pentagrama raio_divino caveira', hellboy: 'punho_gigante armadura martelo', picapau: 'confusao florete confusao',
  pernalonga: 'teleporte clones bonk', ben10: '- labareda investida', aang: 'rajada_de_ar lamina_de_agua transformacao',
  samuraijack: 'iaido purificacao corte_vertical', heman: 'espadao transformacao espadao', popeye: 'pow_cartoon lanche rajada_de_golpes',
  optimus: 'escudo_tech laser grito_de_guerra', salsicha: 'velocidade lanche bonk', bobesponja: 'bolhas esticar chute_voador',
  scooby: 'bonk lanche sorte', rick: 'portal pulso_emp radiacao', finn: '- investida confete',
  megatron: 'canhao_de_energia punho_gigante medo', docinho: 'investida - supernova', mickey: 'encanto inv_vassouras confete',
  donald: 'pow_cartoon rugido -', pateta: 'bonk confusao sorte', stitch: '- mordida pow_cartoon',
  buzz: 'laser pulso_emp foguete', woody: 'chicote grito_de_guerra confete', srincrivel: 'investida escudo_fisico punho_gigante',
  mulherelastica: 'esticar escudo_fisico resgate', frozone: '- bloco_de_gelo nevasca', korra: 'sopro_de_fogo espinhos_de_terra transformacao',
  zuko: 'lamina_de_fogo raio_em_cadeia corte_cruzado', azula: 'labareda - florete', toph: '- espinhos_de_terra metal',
  iroh: 'lanche raio_em_cadeia sopro_de_fogo', patolino: 'confusao mordida bomba', taz: 'tornado mordida atracao',
  coiote: 'bomba bonk foguete', papaleguas: 'investida areia velocidade', marvin: 'bomba laser desintegrar',
  tom: 'pow_cartoon investida garras', jerry: 'bonk teleporte marretada', pantera: 'silencio clones teleporte',
  shredder: 'garras investida mil_cortes', splinter: '- bastao bonk', krang: 'inv_androide escudo_tech -',
  caseyjones: 'bastao - pow_cartoon', bebop: 'investida armadura pisao', skeletor: 'caveira - dominio',
  shera: 'raio_divino grito_de_guerra chute_voador', liono: 'espadao olho tempestade', cheetara: 'bastao investida florete',
  mummra: 'invocacao transformacao sarcofago', homer: 'bonk lanche pow_cartoon', bart: 'tiro confusao bomba',
  peter: 'pow_cartoon bomba confusao', stewie: 'laser escudo_tech dominio', cartman: 'rugido enfraquecimento gas',
  billcipher: 'runas fenda olho', plankton: 'inv_clones pulso_emp -', mojojojo: 'punho_gigante laser rugido',
  capitaoplaneta: 'barreira_magica vinhas grito_de_guerra', bugiganga: 'esticar rajada_de_ar confusao', dannyphantom: 'laser teleporte rugido',
  coragem: 'medo resgate bencao',
};

export const FAMILIA_DA_HABILIDADE: Record<string, VfxFamily> = Object.fromEntries(
  Object.entries(T).flatMap(([id, linha]) => linha.split(' ').flatMap((f, i) => (f === '-' ? [] : [[`${id}:${i}`, f as VfxFamily]]))),
);

/*
 * A criatura de cada invocador (parte 8): a mesma animação e o mesmo som quando
 * ela chega (a habilidade) e a cada ataque dela. O Caminho Deva do Pain segue
 * com a gravidade; o Caminho Animal aparece nos ataques da invocação.
 */
export const FAMILIA_DA_INVOCACAO: Record<string, VfxFamily> = {
  megumi: 'inv_cao', jinwoo: 'inv_sombras', yugi: 'inv_mago', kaiba: 'inv_dragao', bayonetta: 'inv_gomorrah',
  jotaro: 'inv_ora', pain: 'inv_feras', mickey: 'inv_vassouras', plankton: 'inv_clones', krang: 'inv_androide',
};

/*
 * O ataque básico de quem tem um jeito próprio de bater: o espadachim corta, o
 * atirador atira, o telepata empurra com a mente. Os outros seguem a regra
 * (as próprias habilidades e o visual do personagem).
 */
export const FAMILIA_DO_BASICO: Record<string, VfxFamily> = {
  akuma: 'soco',
  agent47: 'tiro',
  arthas: 'corte_diagonal',
  geralt: 'corte_diagonal',
  donkeykong: 'golpe_pesado',
  beerus: 'soco',
  yusuke: 'soco',
  constantine: 'soco',
  aang: 'vento',
  rick: 'laser',
  azula: 'fogo',
  iroh: 'fogo',
  papaleguas: 'investida',
  marvin: 'laser',
  pantera: 'bonk',
  skeletor: 'bastao',
  shera: 'corte_diagonal',
  billcipher: 'fogo',
  dannyphantom: 'laser',
  naruto: 'rajada_de_golpes',
  batman: 'gancho',
  spiderman: 'soco',
  deadpool: 'corte_cruzado',
  frieza: 'esfera',
  inosuke: 'corte_cruzado',
  aizen: 'corte',
  hisoka: 'cartas',
  kurapika: 'corrente',
  griffith: 'florete',
  jotaro: 'soco',
  makima: 'tiro',
  frieren: 'esfera',
  jinwoo: 'corte_cruzado',
  scarletwitch: 'distorcao',
  storm: 'raio',
  cyclops: 'feixe',
  jeangrey: 'telecinese',
  professorx: 'telecinese',
  loki: 'facas',
  aquaman: 'estocada',
  cloud: 'espadao',
  samus: 'tiro',
  bayonetta: 'saraivada',
  wesker: 'soco',
  sonic: 'chute_voador',
  shadowhh: 'chute_voador',
  megaman: 'tiro',
};
