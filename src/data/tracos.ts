import type { Character, Effect, StatusId, Target, Topic } from '../engine/types';

/*
 * Traços próprios (pedido do jogador: "tem que ser mais criativo também nos
 * traços… o traço é muito importante… individualidade pros personagens").
 *
 * 114 personagens dividiam 33 traços genéricos ("Afinidade elemental" para
 * sete, "Ímpeto crescente" para sete…). Cada um ganha o seu, pela história do
 * personagem: o Charizard fica mais forte quando o trio está perdendo (Blaze),
 * a Jean Grey se cura ao apanhar (a Fênix), o Snake some na caixa de papelão,
 * o Iroh serve chá de jasmim para o trio, a Gaara tem a areia que defende
 * sozinha. A ficha monta o texto pelos efeitos (presentTrait), então o que
 * está aqui é o que acontece na luta.
 */
const ch = (value: number): Effect => ({ kind: 'charge', value });
const sh = (value: number, target?: Target): Effect => ({ kind: 'shift', value, ...(target ? { target } : {}) });
const cura = (value: number, target: Target = 'self'): Effect => ({ kind: 'heal', value, target });
const esc = (value: number, target: Target = 'self'): Effect => ({ kind: 'shield', value, target });
const dano = (value: number, target: Target): Effect => ({ kind: 'damage', value, target });
const st = (status: StatusId, value: number, duration: number, target?: Target): Effect => ({ kind: 'status', status, value, duration, ...(target ? { target } : {}) });

type T = [nome: string, on: Topic, cooldown: number, target: Target, effects: Effect[]];
export const TRACOS: Record<string, T> = {
  // ---------------------------------------------------------------- anime
  gohan: ['Potencial despertado', 'allyHurt', 4, 'self', [st('strengthened', 0.08, 5)]],
  ichigo: ['Instinto Hollow', 'received', 3, 'self', [sh(0.1), st('strengthened', 0.05, 5)]],
  frieza: ['Crueldade', 'enemyHurt', 2.5, 'enemyWeak', [st('exposed', 0.06, 5)]],
  levi: ['Reflexo Ackerman', 'dealt', 1.5, 'self', [sh(0.06)]],
  kakashi: ['Sharingan observador', 'enemyCast', 1, 'self', [ch(7)]],
  itachi: ['Olhos que veem tudo', 'enemyCast', 2.5, 'enemyCast', [st('confused', 0.1, 3)]],
  nezuko: ['Regeneração demoníaca', 'time', 2, 'self', [cura(9)]],
  zenitsu: ['Dormindo de pé', 'losing', 2, 'self', [sh(0.1)]],
  killua: ['Godspeed', 'action', 2.5, 'enemyWeak', [st('electric', 0.06, 3)]],
  sukuna: ['Rei das Maldições', 'dealt', 3, 'enemyWeak', [st('cursed', 0.12, 6)]],
  rukia: ['Ar gelado da Sode no Shirayuki', 'action', 3, 'enemyWeak', [st('slow', 0.08, 4)]],
  kenpachi: ['Sede de batalha', 'received', 3, 'self', [st('strengthened', 0.035, 35)]],
  kurapika: ['Juramento da corrente', 'interrupt', 1, 'self', [ch(10)]],
  edward: ['Troca equivalente', 'received', 2, 'self', [esc(35)]],
  alphonse: ['Proteger o irmão', 'allyHurt', 4, 'allyWeak', [esc(61, 'allyWeak')]],
  roy: ['Faísca de oxigênio', 'dealt', 3, 'enemyWeak', [st('burning', 8, 4)]],
  jotaro: ['Yare yare daze', 'received', 3, 'enemyStrong', [dano(40, 'enemyStrong')]],
  dio: ['Tempo parado', 'enemyCast', 2, 'enemyCast', [sh(-0.08, 'enemyCast')]],
  makima: ['Contrato de transferência', 'allyHurt', 3, 'self', [cura(15)]],
  anya: ['Telepatia de alerta', 'allyHurt', 2, 'allyWeak', [sh(0.06, 'allyWeak')]],
  yor: ['Golpe na veia', 'dealt', 3, 'enemyWeak', [st('bleed', 8, 5)]],
  cloud: ['Barra de Limite', 'received', 1.4, 'self', [{ kind: 'store', value: 27, cap: 433, target: 'self' }]],
  tifa: ['Combo crescente', 'dealt', 1.2, 'self', [sh(0.06, 'self')]],
  yusuke: ['Reiki acumulado', 'received', 1.4, 'self', [{ kind: 'store', value: 27, cap: 441, target: 'self' }]],
  trunks: ['Esperança do futuro', 'allyHurt', 2, 'self', [ch(6)]],
  cell: ['Absorção perfeita', 'dealt', 1.8, 'self', [ch(5), cura(12)]],
  beerus: ['Deus da Destruição', 'enemyHurt', 2.5, 'enemyWeak', [st('marked', 0.12, 8)]],
  seiya: ['Cosmo que não se apaga', 'losing', 4, 'self', [cura(20)]],
  shiryu: ['Defesa do Dragão', 'allyHurt', 4, 'allyWeak', [esc(53, 'allyWeak')]],
  shun: ['Rede de Andrômeda', 'negativeStatus', 3, 'enemyStrong', [st('rooted', 0.1, 4)]],
  camus: ['Rumo ao Zero Absoluto', 'time', 5, 'enemyStrong', [st('slow', 0.08, 5)]],
  hadescz: ['Domínio do submundo', 'time', 5, 'allEnemies', [st('cursed', 0.06, 6, 'allEnemies')]],
  madara: ['Olhar do Rinnegan', 'time', 5, 'allEnemies', [st('slow', 0.06, 7, 'allEnemies'), st('weakened', 0.04, 7, 'allEnemies')]],
  gaara: ['Areia que defende sozinha', 'received', 2, 'self', [esc(40)]],
  ben10: ['Omnitrix recarregando', 'time', 6, 'self', [ch(12)]],
  mewtwo: ['Mente superior', 'enemyCast', 2, 'enemyCast', [sh(-0.08, 'enemyCast')]],
  charizard: ['Blaze', 'losing', 2, 'self', [st('strengthened', 0.08, 5)]],
  omniman: ['Sangue viltrumita', 'enemyHurt', 2.5, 'enemyWeak', [st('exposed', 0.08, 5)]],
  // ---------------------------------------------------------------- quadrinhos
  scarletwitch: ['Magia do caos', 'action', 3, 'randomEnemy', [st('confused', 0.1, 3)]],
  daredevil: ['Sentido de radar', 'enemyCast', 2, 'self', [sh(0.08)]],
  punisher: ['Arsenal sem fim', 'time', 5, 'self', [ch(10)]],
  ghostrider: ['Fogo do inferno', 'received', 2, 'enemyStrong', [st('burning', 10, 4, 'enemyStrong')]],
  blade: ['Sangue de Daywalker', 'dealt', 2, 'self', [cura(14)]],
  storm: ['Clima instável', 'time', 6, 'allEnemies', [st('electric', 0.05, 4, 'allEnemies')]],
  jeangrey: ['Força Fênix', 'received', 3, 'self', [cura(20)]],
  gambit: ['Energia cinética', 'action', 2, 'self', [ch(5)]],
  venom: ['Simbionte que fecha feridas', 'received', 1.5, 'self', [cura(14)]],
  carnage: ['Frenesi vermelho', 'dealt', 3, 'enemyWeak', [st('bleed', 10, 6)]],
  galactus: ['Fome cósmica', 'enemyHurt', 2, 'self', [cura(15)]],
  starlord: ['Awesome Mix', 'time', 6, 'allAllies', [st('haste', 0.05, 4, 'allAllies')]],
  rocket: ['Engenhoca improvisada', 'time', 5, 'enemyStrong', [dano(30, 'enemyStrong')]],
  aquaman: ['Chamado do mar', 'time', 6, 'enemyStrong', [st('slow', 0.08, 4, 'enemyStrong')]],
  cyborg: ['Dados da Torre', 'enemyCast', 1, 'self', [ch(5)]],
  shazam: ['Sabedoria de Salomão', 'time', 6, 'self', [ch(10)]],
  darkseid: ['Olhar Ômega', 'time', 5, 'enemyStrong', [st('exposed', 0.08, 6, 'enemyStrong')]],
  lexluthor: ['Gênio estrategista', 'enemyCast', 2, 'self', [esc(40)]],
  arlequina: ['Loucura imprevisível', 'received', 2, 'self', [sh(0.12)]],
  constantine: ['Pacto sujo', 'enemyCast', 2, 'enemyCast', [sh(-0.1, 'enemyCast')]],
  // ---------------------------------------------------------------- games
  zelda: ['Sabedoria da Triforce', 'negativeStatus', 3, 'enemyStrong', [st('rooted', 0.1, 4)]],
  ganondorf: ['Triforce do Poder', 'winning', 1, 'self', [ch(4)]],
  samus: ['Varredura do visor', 'time', 5, 'enemyStrong', [st('marked', 0.09, 9)]],
  vergil: ['Busca pelo poder', 'dealt', 1, 'self', [ch(4)]],
  masterchief: ['Escudo recarregável', 'received', 4, 'self', [esc(45)]],
  snake: ['Caixa de papelão', 'received', 4, 'self', [st('evasion', 0.15, 3)]],
  raidenmgr: ['Lâmina eletromagnética', 'action', 2.5, 'allEnemies', [st('electric', 0.06, 4, 'allEnemies')]],
  lara: ['Instinto de sobrevivente', 'losing', 3, 'self', [st('evasion', 0.15, 4)]],
  sonic: ['Velocidade do som', 'action', 1.2, 'self', [sh(0.08, 'self'), st('haste', 0.05, 30, 'self')]],
  shadowhh: ['Controle do Caos', 'time', 6, 'self', [sh(0.15)]],
  zeromm: ['Sabre carregado', 'dealt', 3, 'enemyWeak', [st('electric', 0.06, 4)]],
  bowser: ['Casco do rei', 'received', 2, 'self', [esc(38)]],
  ryu: ['Caminho do guerreiro', 'dealt', 1, 'self', [ch(3)]],
  chunli: ['Pernas relâmpago', 'dealt', 1.2, 'self', [sh(0.06, 'self')]],
  subzero: ['Frio Lin Kuei', 'received', 3, 'enemyStrong', [st('slow', 0.1, 4, 'enemyStrong')]],
  liukang: ['Chama do Shaolin', 'dealt', 3, 'enemyWeak', [st('burning', 8, 4)]],
  jin: ['Karatê Kazama', 'received', 2, 'enemyStrong', [dano(48, 'enemyStrong'), st('exposed', 0.08, 5, 'enemyStrong')]],
  kazuya: ['Gene do Diabo', 'losing', 3, 'self', [st('strengthened', 0.07, 6)]],
  tuob: ['Pod de apoio', 'time', 4, 'enemyStrong', [dano(30, 'enemyStrong')]],
  agent47: ['Na multidão', 'enemyCast', 2, 'enemyCast', [sh(-0.1, 'enemyCast')]],
  kirby: ['Barriga sem fundo', 'dealt', 1.8, 'self', [ch(5), cura(17)]],
  donkeykong: ['Batida no peito', 'received', 3, 'self', [st('strengthened', 0.06, 5)]],
  simonbelmont: ['Água benta no bolso', 'time', 5, 'enemyStrong', [st('burning', 8, 4, 'enemyStrong')]],
  // ---------------------------------------------------------------- desenhos e outros
  heman: ['Pelo poder de Grayskull', 'received', 3, 'self', [st('strengthened', 0.035, 35)]],
  shera: ['Honra de Grayskull', 'allyHurt', 4, 'allyWeak', [esc(50, 'allyWeak')]],
  skeletor: ['Montanha da Serpente', 'time', 5, 'allEnemies', [st('weakened', 0.06, 6, 'allEnemies')]],
  cheetara: ['Sexto sentido', 'received', 2, 'self', [sh(0.1)]],
  leonardo: ['Formação!', 'allyHurt', 3, 'allAllies', [sh(0.04, 'allAllies')]],
  raphael: ['Cabeça quente', 'received', 2, 'self', [st('strengthened', 0.05, 5)]],
  shredder: ['Mestre do Clã do Pé', 'dealt', 1, 'self', [ch(3)]],
  splinter: ['Sabedoria do mestre', 'received', 2, 'enemyStrong', [dano(53, 'enemyStrong'), st('exposed', 0.08, 5, 'enemyStrong')]],
  bebop: ['Couro grosso', 'received', 2, 'self', [esc(44)]],
  aang: ['Último dobrador de ar', 'time', 8, 'self', [st('evasion', 0.1, 4)]],
  korra: ['Conexão com Raava', 'time', 6, 'self', [ch(10)]],
  zuko: ['Honra restaurada', 'losing', 3, 'self', [ch(10)]],
  azula: ['Perfeição', 'dealt', 2, 'self', [sh(0.06)]],
  iroh: ['Chá de jasmim', 'time', 6, 'allAllies', [cura(12, 'allAllies')]],
  frozone: ['Gelo instantâneo', 'allyHurt', 4, 'allyWeak', [esc(50, 'allyWeak')]],
  mulherelastica: ['Abraço elástico', 'allyHurt', 4, 'allyWeak', [esc(59, 'allyWeak')]],
  optimus: ['Proteger os humanos', 'allyHurt', 4, 'allyWeak', [esc(45, 'allyWeak')]],
  popeye: ['Vontade de espinafre', 'received', 1.4, 'self', [{ kind: 'store', value: 28, cap: 458, target: 'self' }]],
  bobesponja: ['Esponja que absorve', 'received', 2, 'self', [cura(16)]],
  scooby: ['Scooby-lanche', 'losing', 3, 'self', [cura(18)]],
  mickey: ['Chapéu de feiticeiro', 'action', 3, 'self', [ch(5)]],
  donald: ['Ataque de fúria', 'received', 2, 'self', [sh(0.1)]],
  woody: ['Amigo de verdade', 'allyHurt', 2, 'allyWeak', [cura(15, 'allyWeak')]],
  rick: ['Portal de fuga', 'received', 4, 'self', [st('evasion', 0.12, 3)]],
  picapau: ['Ha-ha-ha-HA-ha!', 'enemyCast', 1.8, 'enemyCast', [st('confused', 0.1, 5), ch(5)]],
  patolino: ['Desprezível!', 'received', 3, 'self', [ch(8)]],
  pernalonga: ['Buraco de coelho', 'received', 1.6, 'self', [sh(0.12, 'self'), cura(23)]],
  tom: ['Perseguição sem fim', 'dealt', 3, 'enemyWeak', [st('marked', 0.08, 7)]],
  jerry: ['Esconderijo na parede', 'received', 1.6, 'self', [sh(0.12, 'self'), cura(21)]],
  pantera: ['Passo de veludo', 'enemyCast', 2, 'enemyCast', [sh(-0.1, 'enemyCast')]],
  marvin: ['Mira marciana', 'time', 5, 'enemyStrong', [st('marked', 0.09, 9)]],
  cartman: ['Respeitem minha autoridade', 'losing', 2, 'enemyStrong', [st('weakened', 0.06, 5, 'enemyStrong')]],
  mojojojo: ['Plano maligno', 'enemyCast', 2, 'self', [ch(6)]],
};

/** Põe o traço próprio na ficha (o texto da ficha sai dos efeitos). */
export const aplicaTraco = (c: Character): Character => {
  const t = TRACOS[c.id];
  if (!t) return c;
  const [name, on, cooldown, target, effects] = t;
  // quando todo efeito diz o próprio alvo, o traço fica em "si" e a ficha escreve o alvo de cada um ("em todo o trio")
  const alvo: Target = effects.every((e) => e.target) ? 'self' : target;
  return { ...c, trait: { name, description: name, on, cooldown, target: alvo, effects } };
};
