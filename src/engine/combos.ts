/*
 * Combos do trio e bônus de universo (pedido do jogador: o trio bom tem que
 * valer bem mais que o aleatório — "bom entre 5 e 30, perto de 15–20; o muito
 * bom entre 20 e 70, por volta de 45" — escolhido: combos + universo).
 *
 * Antes, a sinergia era só o que as habilidades já faziam umas pelas outras, e
 * na luta ela quase não pesava: com o elenco equilibrado, escolher bem o trio
 * mudava pouco. Agora cada ligação entre dois do trio (src/engine/sinergia.ts,
 * lida dos kits) acende um combo com nome, que dá um bônus de verdade a quem é
 * ajudado — "Carga para o golpe": o aliado que dá Carga faz o golpe grande do
 * outro carregar mais depressa. E dois ou três do mesmo universo lutam melhor
 * juntos.
 *
 * Vale para os dois lados: os rivais também ganham os combos deles (o rival
 * da campanha é escolhido mais entrosado a cada luta — campaign.ts).
 */
import { byId } from '../data/characters';
import { grupoDoUniverso } from '../data/equipes';
import { papelDe, type Ligacao } from './sinergia';
import type { Bonus, ComboAtivo, Effect, Pulso, StatusId, Target } from './types';

export type { Bonus, ComboAtivo } from './types';
export const SEM_BONUS: Bonus = { dano: 0, defesa: 0, cura: 0, carga: 0, ritmo: 0, vida: 0, escudo: 0, preparo: 0, traco: 0, basico: 0, duracao: 0, resiste: 0, segura: 0 };

/*
 * O que cada um precisa ter para entrar num combo. Pedido do jogador: "coisa
 * que um ser humano entende" — nada de "golpe grande" ou "o forte": cada
 * condição é algo que o jogador confere lendo a ficha (a Vida, o dano de uma
 * habilidade, o Preparo, o Status que ela põe). E o jogo não aponta quem
 * combina com quem na escolha do trio: o jogador lê as regras no Livro de
 * Combos, lê as fichas e descobre; os combos aparecem na abertura da luta.
 */
export interface Feitio {
  /* Status que põe nos rivais */
  congela: boolean; queima: boolean; envenena: boolean; sangra: boolean; adormece: boolean; cega: boolean; eletriza: boolean;
  bomba: boolean; amaldicoa: boolean; marca: boolean; provoca: boolean; controlePesado: boolean;
  /* em todos os rivais de uma vez */
  silenciaTodos: boolean; expoeTodos: boolean; confundeTodos: boolean; retardaTodos: boolean; paralisaTodos: boolean; enraizaTodos: boolean;
  /* o que faz pelos aliados */
  daCarga: boolean; curaAliado: boolean; levanta: boolean; purifica: boolean; barreira: boolean; regenAliados: boolean;
  fortalece: boolean; aceleraAliados: boolean; adiantaAliados: boolean; escudoAliado: boolean; dissipa: boolean; invoca: boolean; copia: boolean;
  /* o que ele mesmo tem */
  golpe500: boolean; golpe550: boolean; golpe600: boolean; area350: boolean; preparo3: boolean; vida900: boolean; vida1400: boolean;
  vampiro: boolean; espinhos: boolean; esquiva: boolean; acumula: boolean; precisaFerido: boolean;
  reageAStatus: boolean; tracoPerdendo: boolean; tracoRivalFerido: boolean;
}
/*
 * Os combos são específicos de propósito (pedido do jogador: "a chance de você fazer uma coisa aleatória tem
 * que ser pequena… mais tipos de combo, onde o personagem encaixa com alguns, não com 100"): cada peça é uma
 * coisa que poucos têm (Congelar, Bomba, Barreira nos aliados, um golpe de 550…), e cada personagem forma
 * combo com uns 10 a 20 do elenco. Um trio aleatório quase nunca forma; quem lê as fichas e procura, forma.
 */
const ALIADOS = ['allAllies', 'allyWeak', 'allyFallen', 'allyStrongest'];
const feitios = new Map<string, Feitio>();
export function feitioDe(id: string): Feitio {
  const pronto = feitios.get(id);
  if (pronto) return pronto;
  const c = byId[id]!, p = papelDe(id);
  const todos = [...c.skills.flatMap((s) => s.effects.map((e) => ({ e, alvo: e.target ?? s.target }))), ...c.trait.effects.map((e) => ({ e, alvo: e.target ?? c.trait.target })), ...c.basic.effects.map((e) => ({ e, alvo: e.target ?? c.basic.target }))];
  const noRival = (alvo: string) => alvo !== 'self' && !ALIADOS.includes(alvo);
  const poe = (lista: string[], duracao = 0) => todos.some(({ e, alvo }) => e.kind === 'status' && lista.includes(e.status) && (e.duration ?? 0) >= duracao && noRival(alvo));
  const poeEmTodos = (st: string) => todos.some(({ e, alvo }) => e.kind === 'status' && e.status === st && alvo === 'allEnemies');
  const nosAliados = (st: string) => todos.some(({ e, alvo }) => e.kind === 'status' && e.status === st && ALIADOS.includes(alvo));
  const tipoNosAliados = (k: string) => todos.some(({ e, alvo }) => e.kind === k && ALIADOS.includes(alvo));
  const golpe = (n: number) => c.skills.some((s) => s.effects.some((e) => e.kind === 'damage' && e.value >= n && noRival(e.target ?? s.target)));
  const f: Feitio = {
    congela: poe(['frozen']), queima: poe(['burning']), envenena: poe(['poison']), sangra: poe(['bleed']), adormece: poe(['sleep']), cega: poe(['blind']),
    eletriza: poe(['electric']), bomba: poe(['bomb']), amaldicoa: poe(['cursed']), marca: poe(['marked']), provoca: poe(['provoked']),
    controlePesado: poe(['paralyzed', 'frozen', 'sleep'], 1.5),
    silenciaTodos: poeEmTodos('silenced'), expoeTodos: poeEmTodos('exposed'), confundeTodos: poeEmTodos('confused'), retardaTodos: poeEmTodos('slow'),
    paralisaTodos: poeEmTodos('paralyzed'), enraizaTodos: poeEmTodos('rooted'), copia: todos.some(({ e }) => e.kind === 'copy'),
    daCarga: tipoNosAliados('charge'), curaAliado: tipoNosAliados('heal'), levanta: tipoNosAliados('revive'), purifica: tipoNosAliados('cleanse'),
    barreira: nosAliados('barrier'), regenAliados: nosAliados('regen'), fortalece: nosAliados('strengthened'), aceleraAliados: nosAliados('haste'),
    adiantaAliados: tipoNosAliados('shift'), escudoAliado: tipoNosAliados('shield'), dissipa: todos.some(({ e }) => e.kind === 'dispel'),
    invoca: todos.some(({ e }) => e.kind === 'status' && e.status === 'summon'),
    golpe500: golpe(500), golpe550: golpe(550), golpe600: golpe(600),
    area350: c.skills.some((s) => s.effects.some((e) => e.kind === 'damage' && e.value >= 350 && (e.target ?? s.target) === 'allEnemies')),
    preparo3: c.skills.some((s) => s.preparation >= 3), vida900: c.hp <= 900, vida1400: c.hp >= 1400,
    vampiro: todos.some(({ e }) => e.kind === 'lifesteal' || (e.kind === 'status' && e.status === 'vampirism')),
    espinhos: todos.some(({ e }) => e.kind === 'status' && (e.status === 'thorns' || e.status === 'reflect')),
    esquiva: todos.some(({ e, alvo }) => e.kind === 'status' && e.status === 'evasion' && alvo === 'self'),
    acumula: todos.some(({ e }) => e.kind === 'store' || e.kind === 'release'),
    precisaFerido: p.precisaFerido,
    reageAStatus: ['status', 'negativeStatus'].includes(c.trait.on), tracoPerdendo: c.trait.on === 'losing', tracoRivalFerido: c.trait.on === 'enemyHurt',
  };
  feitios.set(id, f);
  return f;
}

/* Cada peça, do jeito que o jogador confere na ficha ("Alguém que …"). */
export const PECAS: Record<keyof Feitio, string> = {
  congela: 'Congela um rival', queima: 'deixa um rival Queimando', envenena: 'Envenena um rival', sangra: 'faz um rival Sangrar',
  adormece: 'faz um rival Dormir', cega: 'deixa um rival Cego', eletriza: 'deixa um rival Eletrizado', bomba: 'põe uma Bomba num rival',
  amaldicoa: 'deixa um rival Amaldiçoado', marca: 'deixa um rival Marcado', provoca: 'Provoca os rivais (eles só batem nele)',
  controlePesado: 'Paralisa, Congela ou faz Dormir um rival por 1,5 s ou mais',
  silenciaTodos: 'Silencia todos os rivais de uma vez', expoeTodos: 'deixa todos os rivais Expostos de uma vez',
  confundeTodos: 'deixa todos os rivais Confusos de uma vez', retardaTodos: 'deixa todos os rivais Lentos de uma vez',
  paralisaTodos: 'Paralisa todos os rivais de uma vez', enraizaTodos: 'Enraíza todos os rivais de uma vez', copia: 'copia a habilidade de um rival',
  daCarga: 'enche a Carga de um aliado', curaAliado: 'cura um aliado', levanta: 'revive um aliado caído', purifica: 'tira os Status ruins dos aliados',
  barreira: 'dá Barreira aos aliados', regenAliados: 'dá Regeneração aos aliados', fortalece: 'deixa os aliados Fortalecidos',
  aceleraAliados: 'deixa os aliados Acelerados', adiantaAliados: 'adianta a vez dos aliados', escudoAliado: 'dá Escudo a um aliado',
  dissipa: 'tira os buffs dos rivais (Dissipar)', invoca: 'invoca uma criatura',
  golpe500: 'tem uma habilidade que tira 500 de dano ou mais', golpe550: 'tem uma habilidade que tira 550 de dano ou mais',
  golpe600: 'tem uma habilidade que tira 600 de dano ou mais', area350: 'acerta todos os rivais de uma vez com 350 de dano ou mais',
  preparo3: 'tem uma habilidade com Preparo de 3 s ou mais', vida900: 'tem 900 de Vida ou menos', vida1400: 'tem 1400 de Vida ou mais',
  vampiro: 'tem Vampirismo ou rouba Vida', espinhos: 'tem Espinhos ou Refletir', esquiva: 'ganha Esquiva', acumula: 'guarda energia e depois libera',
  precisaFerido: 'tem uma habilidade que só é usada quando o rival já está machucado',
  reageAStatus: 'tem um Traço que dispara quando alguém ganha Status', tracoPerdendo: 'tem um Traço que funciona quando o trio está atrás na Vantagem',
  tracoRivalFerido: 'tem um Traço que dispara quando um rival se machuca',
};

type Extra = { nosRivais?: Partial<Bonus>; pulso?: Pulso };
type Regra = { id: Ligacao | string; nome: string; ajuda: keyof Feitio; ganha: keyof Feitio; bonus: Partial<Bonus>; texto: string } & Extra;
/*
 * As duplas: quem tem a peça `ajuda` dá o bônus a quem tem a peça `ganha`.
 * Os números são calibrados pelas medições de dificuldade (scripts/_dificuldade.ts); FORCA_DOS_COMBOS escala todos juntos.
 */
const r = (id: string, nome: string, ajuda: keyof Feitio, ganha: keyof Feitio, bonus: Partial<Bonus>, texto: string, extra: Extra = {}): Regra => ({ id, nome, ajuda, ganha, bonus, texto, ...extra });
/* os efeitos dos combos de tempo em tempo */
const st = (status: StatusId, value: number, duration: number, target?: Target): Effect => ({ kind: 'status', status, value, duration, ...(target ? { target } : {}) });
const pulso = (cada: number, alvo: Target, efeitos: Effect[], texto: string): Pulso => ({ cada, alvo, efeitos, texto });
export const REGRAS: readonly Regra[] = [
  // o que cada combo dá combina com a dupla: quem congela quebra o gelo com o golpe, quem cega deixa o outro
  // escapar, quem tira os buffs abre a defesa dos rivais
  r('gelo-fogo', 'Choque térmico', 'congela', 'queima', { dano: 0.12, duracao: 0.2 }, 'mais dano, e a queimadura dura mais'),
  r('gelo-quebra', 'Quebra-gelo', 'congela', 'golpe500', { preparo: 0.2 }, 'prepara o golpe mais rápido'),
  r('veneno-sangue', 'Ferida aberta', 'envenena', 'sangra', { dano: 0.06 }, 'bate mais, e os rivais curam menos', { nosRivais: { cura: 0.25 } }),
  r('sangue-vampiro', 'Sede de sangue', 'sangra', 'vampiro', { cura: 0.3, vida: 0.06 }, 'cura mais e tem mais Vida'),
  r('maldicao-vampiro', 'Sem cura para eles', 'amaldicoa', 'vampiro', { cura: 0.2 }, 'cura mais, e os rivais curam menos', { nosRivais: { cura: 0.15 } }),
  r('sono-golpe', 'Golpe no sono', 'adormece', 'golpe500', { duracao: 0.3 }, 'os Status dele duram mais', { pulso: pulso(12, 'enemyCast', [{ kind: 'interrupt', mode: 'delay', value: 1 }], 'quem recebe atrasa em 1 s o Preparo do rival que estiver preparando') }),
  r('controla-dano', 'Prende e bate', 'controlePesado', 'golpe550', { preparo: 0.15, dano: 0.06 }, 'prepara mais rápido e bate mais'),
  r('dissipa-golpe', 'Sem defesa', 'dissipa', 'golpe500', { dano: 0.06 }, 'mais dano, e os rivais recebem mais dano', { nosRivais: { defesa: 0.07 } }),
  r('reforca-forte', 'Força extra', 'fortalece', 'golpe600', { basico: 0.35 }, 'o ataque básico fica bem mais forte'),
  r('carga-golpe', 'Golpe carregado', 'daCarga', 'golpe550', { carga: 0.15 }, 'a Carga enche mais depressa', { pulso: pulso(10, 'self', [{ kind: 'charge', value: 12 }], 'quem recebe ganha 12 de Carga nas habilidades') }),
  r('bomba-area', 'Fogos', 'bomba', 'area350', { preparo: 0.15 }, 'prepara mais rápido, e de tempo em tempo põe Bomba', { pulso: pulso(12, 'enemyStrong', [st('bomb', 80, 3)], 'quem recebe põe uma Bomba de 80 no rival mais forte (explode em 3 s)') }),
  r('expostos-ferido', 'Cheiro de sangue', 'expoeTodos', 'tracoRivalFerido', { traco: 0.3 }, 'o Traço volta mais rápido'),
  r('silencio-preparo', 'Silêncio', 'silenciaTodos', 'preparo3', { preparo: 0.25 }, 'prepara as habilidades mais rápido'),
  r('pressa-acumula', 'Acúmulo rápido', 'aceleraAliados', 'acumula', { ritmo: 0.06 }, 'ataca mais rápido e guarda energia', { pulso: pulso(8, 'self', [{ kind: 'store', value: 40, cap: 420 }], 'quem recebe guarda 40 de energia para soltar depois') }),
  r('status-gatilho', 'Reação em cadeia', 'eletriza', 'reageAStatus', { traco: 0.35 }, 'o Traço volta mais rápido'),
  r('cego-esquiva', 'Ninguém acerta', 'cega', 'esquiva', { escudo: 0.12 }, 'começa a luta com Escudo'),
  r('escudo-espinhos', 'Muralha de espinhos', 'barreira', 'espinhos', { escudo: 0.12, resiste: 0.2 }, 'começa com Escudo e Status ruins duram menos nele'),
  r('provoca-espinhos', 'Venha me bater', 'provoca', 'espinhos', { resiste: 0.3 }, 'Status ruins duram menos nele', { pulso: pulso(10, 'self', [st('thorns', 20, 4)], 'quem recebe ganha Espinhos: quem bater nele leva 20 de dano por golpe, por 4 s') }),
  r('provoca-golpe', 'Escudo humano', 'provoca', 'golpe550', { escudo: 0.12 }, 'começa a luta com Escudo'),
  r('cura-tanque', 'Tanque com médico', 'curaAliado', 'provoca', { vida: 0.1 }, 'mais Vida e Provoca de novo', { pulso: pulso(14, 'allEnemies', [st('provoked', 1, 2.5)], 'quem recebe Provoca todos os rivais de novo por 2,5 s') }),
  r('regen-tanque', 'Muralha viva', 'regenAliados', 'vida1400', { defesa: 0.08 }, 'recebe menos dano e se regenera', { pulso: pulso(10, 'self', [st('regen', 12, 4)], 'quem recebe ganha Regeneração: +12 de Vida por segundo, por 4 s') }),
  r('limpa-fragil', 'Sempre limpo', 'purifica', 'vida900', { segura: 1 }, 'aguenta o golpe que o derrubaria', { pulso: pulso(10, 'self', [{ kind: 'cleanse', value: 1 }], 'quem recebe tira 1 Status ruim de si') }),
  r('revive-virada', 'Virada', 'levanta', 'tracoPerdendo', { traco: 0.3, vida: 0.06 }, 'o Traço volta mais rápido e tem mais Vida'),
  r('duas-invocacoes', 'Exército', 'invoca', 'invoca', { duracao: 0.3 }, 'as criaturas e os Status duram mais'),
  // os que agem de tempo em tempo na luta (pedido do jogador: "aplica, depois de um tempo tem um cooldown, aplica de novo")
  r('veneno-maldicao', 'Praga lenta', 'envenena', 'amaldicoa', {}, 'Envenena os rivais de tempo em tempo', { pulso: pulso(10, 'allEnemies', [st('poison', 6, 5)], 'quem recebe Envenena todos os rivais: −6 de Vida por segundo, por 5 s') }),
  r('gelo-sono', 'Sono gelado', 'congela', 'adormece', { carga: 0.15 }, 'a Carga enche mais depressa', { pulso: pulso(14, 'enemyStrong', [st('slow', 0.25, 6)], 'quem recebe deixa o rival mais forte Lento (25% mais devagar) por 6 s') }),
  r('barreira-purifica', 'Santuário', 'barreira', 'purifica', { cura: 0.15 }, 'cura mais', { pulso: pulso(10, 'allAllies', [st('protected', 0.12, 5)], 'o trio todo fica Protegido (recebe 12% menos dano) por 5 s') }),
  r('regen-cura', 'Fonte de vida', 'regenAliados', 'curaAliado', { cura: 0.2 }, 'cura mais', { pulso: pulso(8, 'allyWeak', [{ kind: 'heal', value: 60 }], 'quem recebe cura 60 de Vida no aliado mais ferido') }),
  r('invoca-carga', 'Domador', 'daCarga', 'invoca', { carga: 0.15 }, 'a Carga enche mais depressa', { pulso: pulso(9, 'self', [st('haste', 0.15, 4)], 'quem recebe fica Acelerado (15% mais rápido) por 4 s') }),
  r('bomba-fogo', 'Pavio aceso', 'queima', 'bomba', { basico: 0.2 }, 'ataque básico mais forte e Queima de tempo em tempo', { pulso: pulso(12, 'enemyWeak', [st('burning', 10, 4)], 'quem recebe deixa o rival mais fraco Queimando: −10 de Vida por segundo, por 4 s') }),
  r('eletrico-golpe', 'Descarga', 'eletriza', 'golpe550', { preparo: 0.2 }, 'prepara o golpe mais rápido'),
  r('cego-golpe', 'Golpe no escuro', 'cega', 'golpe500', { basico: 0.15 }, 'ataque básico mais forte e Expõe de tempo em tempo', { pulso: pulso(12, 'enemyStrong', [st('exposed', 0.15, 5)], 'quem recebe deixa o rival mais forte Exposto (recebe 15% mais dano) por 5 s') }),
  r('dissipa-maldicao', 'Sem proteção', 'dissipa', 'amaldicoa', {}, 'os rivais curam menos', { nosRivais: { cura: 0.1 }, pulso: pulso(12, 'enemyStrong', [{ kind: 'dispel', value: 1 }], 'quem recebe tira 1 buff do rival mais forte') }),
  r('copia-golpe', 'Cópia perfeita', 'copia', 'golpe600', { carga: 0.3 }, 'a Carga enche mais depressa'),
  r('acumula-barreira', 'Bateria', 'barreira', 'acumula', {}, 'ganha Escudo de tempo em tempo', { pulso: pulso(10, 'self', [{ kind: 'shield', value: 80 }], 'quem recebe ganha Escudo de 80') }),
  r('paralisa-golpe', 'Tempestade parada', 'paralisaTodos', 'golpe600', { preparo: 0.25 }, 'prepara o golpe mais rápido'),
  r('provoca-regen', 'Tanque eterno', 'regenAliados', 'provoca', {}, 'se regenera de tempo em tempo', { pulso: pulso(8, 'self', [st('regen', 15, 4)], 'quem recebe ganha Regeneração: +15 de Vida por segundo, por 4 s') }),
];
/*
 * Os combos de trio (pedido do jogador: "bastante camadas… pra pessoa aprender"; escolhido: combos de 3
 * peças). Só acendem quando os três do trio se completam, cada um numa peça diferente; o bônus vai para o
 * trio todo. Um trio aleatório forma algum deles em ~2,5% das vezes; não contam no limite de COMBOS_POR_TRIO.
 */
export interface ComboDeTrio extends Extra { id: string; nome: string; pecas: readonly [keyof Feitio, keyof Feitio, keyof Feitio]; bonus: Partial<Bonus>; texto: string }
export const TRIOS: readonly ComboDeTrio[] = [
  { id: 'trio-armadilha', nome: 'Armadilha', pecas: ['controlePesado', 'marca', 'golpe500'], bonus: { dano: 0.06 }, nosRivais: { preparo: 0.12 }, texto: 'o trio todo causa mais dano, e os rivais preparam mais devagar' },
  { id: 'trio-execucao', nome: 'Execução', pecas: ['area350', 'expoeTodos', 'precisaFerido'], bonus: { dano: 0.1 }, texto: 'o trio todo causa mais dano' },
  { id: 'trio-elementos', nome: 'Fúria dos elementos', pecas: ['eletriza', 'queima', 'congela'], bonus: { dano: 0.15 }, texto: 'o trio todo causa mais dano' },
  { id: 'trio-pragas', nome: 'Pragas', pecas: ['envenena', 'amaldicoa', 'sangra'], bonus: {}, nosRivais: { dano: 0.1, cura: 0.2 }, texto: 'os rivais causam menos dano e curam menos' },
  { id: 'trio-caos', nome: 'Caos', pecas: ['confundeTodos', 'silenciaTodos', 'retardaTodos'], bonus: {}, nosRivais: { ritmo: 0.06, preparo: 0.12 }, texto: 'os rivais atacam e preparam mais devagar' },
  { id: 'trio-turbo', nome: 'Turbo', pecas: ['daCarga', 'adiantaAliados', 'preparo3'], bonus: { preparo: 0.15, carga: 0.1 }, texto: 'o trio todo prepara e carrega mais rápido' },
  { id: 'trio-ataque-total', nome: 'Ataque total', pecas: ['fortalece', 'aceleraAliados', 'golpe500'], bonus: { ritmo: 0.08 }, texto: 'o trio todo ataca mais rápido' },
  { id: 'trio-muralha', nome: 'Muralha', pecas: ['provoca', 'curaAliado', 'escudoAliado'], bonus: { escudo: 0.1 }, texto: 'o trio todo começa a luta com Escudo' },
  { id: 'trio-imortais', nome: 'Imortais', pecas: ['levanta', 'purifica', 'regenAliados'], bonus: { vida: 0.12 }, texto: 'o trio todo ganha mais Vida' },
  { id: 'trio-banquete', nome: 'Banquete', pecas: ['sangra', 'vampiro', 'amaldicoa'], bonus: { cura: 0.2, dano: 0.08 }, texto: 'o trio todo cura mais e causa mais dano' },
  { id: 'trio-era-do-gelo', nome: 'Era do gelo', pecas: ['congela', 'retardaTodos', 'golpe500'], bonus: {}, nosRivais: { ritmo: 0.06 }, pulso: pulso(12, 'allEnemies', [st('slow', 0.15, 4)], 'todos os rivais ficam Lentos (15% mais devagar) por 4 s'), texto: 'os rivais atacam mais devagar' },
  { id: 'trio-templo', nome: 'Templo', pecas: ['barreira', 'purifica', 'curaAliado'], bonus: { cura: 0.1 }, pulso: pulso(9, 'allAllies', [st('protected', 0.15, 4)], 'o trio todo fica Protegido (recebe 15% menos dano) por 4 s'), texto: 'o trio todo cura mais' },
  { id: 'trio-explosao', nome: 'Explosão em cadeia', pecas: ['bomba', 'queima', 'area350'], bonus: { dano: 0.15 }, texto: 'o trio todo causa mais dano' },
  { id: 'trio-relogio', nome: 'Controle do tempo', pecas: ['adiantaAliados', 'aceleraAliados', 'daCarga'], bonus: { traco: 0.25, ritmo: 0.06 }, texto: 'o Traço do trio todo volta mais rápido, e o trio ataca mais rápido' },
];
/*
 * As duplas lendárias (pedido do jogador: "alguns personagens que são fracos… colocar algum combo dele com algum
 * personagem específico que faça sentido pra aquele personagem… a dupla dele"): pares da história, de nome. Um
 * trio aleatório quase nunca junta os dois, então elas servem para levantar quem está fraco sem facilitar o aleatório.
 * Só entra aqui quem a medição mostrou fraco (pedido do jogador: "não precisa colocar muitos… pra equilibrar se precisar").
 * `so`: só um dos dois recebe (o outro já é forte).
 */
export interface DuplaLendaria { id: string; nome: string; a: string; b: string; bonus: Partial<Bonus>; texto: string; so?: string; pulso?: Pulso }
const lenda = (a: string, b: string, nome: string, bonus: Partial<Bonus>, texto: string, extra: { so?: string; pulso?: Pulso } = {}): DuplaLendaria => ({ id: `lenda-${a}-${b}`, nome, a, b, bonus, texto, ...extra });
export const DUPLAS_LENDARIAS: readonly DuplaLendaria[] = [
  lenda('tom', 'jerry', 'Gato e rato', { ritmo: 0.08, basico: 0.15 }, 'os dois atacam mais rápido, com o ataque básico mais forte', { pulso: pulso(12, 'enemyStrong', [st('confused', 0.2, 4)], 'uma armadilha deixa o rival mais forte Confuso (pode errar e se acertar) por 4 s') }),
  lenda('dante', 'vergil', 'Filhos de Sparda', { basico: 0.2, preparo: 0.1 }, 'ataque básico mais forte e Preparo mais curto', { pulso: pulso(15, 'self', [st('strengthened', 0.15, 6)], 'Dante entra em Devil Trigger: fica Fortalecido (+15% de dano) por 6 s') }),
  lenda('jin', 'kazuya', 'Sangue Mishima', { traco: 0.25, vida: 0.08 }, 'o Traço volta mais rápido e os dois têm mais Vida'),
  lenda('power', 'denji', 'Caçadores de demônios', { vida: 0.1, cura: 0.2 }, 'os dois têm mais Vida e curam mais'),
  lenda('nezuko', 'tanjiro', 'Irmãos Kamado', { defesa: 0.1, dano: 0.08 }, 'os dois recebem menos dano e batem mais', { pulso: pulso(12, 'allyWeak', [{ kind: 'shield', value: 70 }], 'Nezuko dá Escudo de 70 ao aliado mais ferido') }),
  lenda('inosuke', 'zenitsu', 'Parceiros de missão', { ritmo: 0.1 }, 'os dois atacam mais rápido'),
  lenda('ryu', 'ken', 'Irmãos Shotokan', { preparo: 0.15, basico: 0.12 }, 'Preparo mais curto e ataque básico mais forte'),
  lenda('finn', 'jake', 'Hora de Aventura!', { vida: 0.1, ritmo: 0.06 }, 'os dois têm mais Vida e atacam mais rápido'),
  lenda('robin', 'batman', 'Dupla Dinâmica', { traco: 0.2, defesa: 0.06 }, 'Robin: o Traço volta mais rápido e recebe menos dano', { so: 'robin' }),
  lenda('luigi', 'mario', 'Irmãos Mario', { basico: 0.15, vida: 0.08 }, 'os dois: ataque básico mais forte e mais Vida'),
  lenda('zoro', 'luffy', 'Bando do Chapéu de Palha', { preparo: 0.12, carga: 0.1 }, 'os dois preparam e carregam mais rápido'),
  lenda('lawliet', 'light', 'Kira e L', { duracao: 0.25 }, 'os Status dos dois duram mais', { pulso: pulso(14, 'enemyStrong', [st('exposed', 0.15, 5)], 'L expõe o rival mais forte (recebe 15% mais dano) por 5 s') }),
  lenda('morty', 'rick', 'Rick e Morty', { escudo: 0.1, carga: 0.1 }, 'os dois começam com Escudo e carregam mais rápido'),
  lenda('peter', 'stewie', 'Família Griffin', { vida: 0.12, defesa: 0.08 }, 'os dois têm mais Vida e recebem menos dano'),
  lenda('azula', 'zuko', 'Herdeiros do fogo', { preparo: 0.12 }, 'os dois preparam mais rápido', { pulso: pulso(10, 'enemyWeak', [st('burning', 10, 4)], 'Azula deixa o rival mais fraco Queimando: −10 de Vida por segundo, por 4 s') }),
  lenda('raidenmgr', 'snake', 'Shadow Moses', { escudo: 0.1, ritmo: 0.06 }, 'os dois começam com Escudo e atacam mais rápido'),
];
/*
 * A raridade (pedido do jogador: "quanto mais poderoso é o combo, mais difícil é de fazer"): conta quantas duplas do
 * elenco formam cada combo. O que quase ninguém forma vale mais; o que muita gente forma vale menos. Os de trio e as
 * duplas lendárias são os mais raros de todos.
 */
export type Raridade = 'comum' | 'raro' | 'epico' | 'lendario';
export const FORCA_DA_RARIDADE: Record<Raridade, number> = { comum: 0.8, raro: 1, epico: 1.25, lendario: 1 };
let raridades: Map<string, Raridade> | null = null;
export function raridadeDe(id: string): Raridade {
  if (!raridades) {
    raridades = new Map();
    const ids = Object.keys(byId);
    for (const r of REGRAS) {
      const quem = ids.filter((x) => feitioDe(x)[r.ajuda]), recebem = ids.filter((x) => feitioDe(x)[r.ganha]);
      const duplas = new Set(quem.flatMap((a) => recebem.filter((b) => b !== a).map((b) => (a < b ? `${a}|${b}` : `${b}|${a}`)))).size;
      raridades.set(r.id, duplas >= 150 ? 'comum' : duplas >= 60 ? 'raro' : 'epico');
    }
  }
  if (id.startsWith('trio-') || id.startsWith('lenda-') || id === 'universo-3') return 'lendario';
  if (id === 'universo-2') return 'comum';
  return raridades.get(id) ?? 'raro';
}
const ORDENS = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]] as const;
/** Os três do trio, na ordem das peças, se eles formam o combo de trio. */
export function quemFormaOTrio(trio: readonly string[], c: ComboDeTrio): string[] | null {
  if (trio.length !== 3) return null;
  for (const o of ORDENS) { const ids = o.map((i) => trio[i]!); if (c.pecas.every((k, i) => feitioDe(ids[i]!)[k])) return ids; }
  return null;
}

/* O mesmo universo: dois juntos e o trio inteiro. */
// a dupla do mesmo universo vale pouco (um trio aleatório forma em ~9% das vezes); o trio inteiro vale muito
export const UNIVERSO = { dois: { dano: 0.04, vida: 0.04 } as Partial<Bonus>, tres: { dano: 0.08, vida: 0.08 } as Partial<Bonus> };
export const COMBOS_POR_LUTADOR = 2, COMBOS_POR_TRIO = 4;
/** Escala de todos os combos (a alavanca da calibragem). */
export const FORCA_DOS_COMBOS = 3.0;
/*
 * Os combos que um trio aleatório quase nunca forma (os de trio e os de universo) valem mais que os de dupla
 * (pedido do jogador: "quanto mais longe o bom ficar do aleatório, é a melhor coisa").
 */
export const FORCA_DOS_TRIOS = 1, FORCA_DO_UNIVERSO = 1, FORCA_DAS_LENDARIAS = 0.5;
/** Quanto dos combos o trio rival recebe (1 = igual ao jogador; 0 = os rivais não formam combos). */
export const COMBOS_DOS_RIVAIS = 1;
/** Teto de cada bônus somado num lutador. */
export const TETO: Bonus = { dano: 0.35, defesa: 0.3, cura: 0.4, carga: 0.45, ritmo: 0.16, vida: 0.3, escudo: 0.3, preparo: 0.35, traco: 0.45, basico: 0.6, duracao: 0.6, resiste: 0.5, segura: 1 };
/** Quantos segundos dura o Escudo que o combo dá no começo da luta. */
export const ESCUDO_DO_COMBO = 15;
/** O quanto os combos podem enfraquecer o trio rival, somados (o piso de cada um, em negativo). */
export const PISO: Bonus = { dano: 0.2, defesa: 0.2, cura: 0.4, carga: 0.25, ritmo: 0.12, vida: 0, escudo: 0, preparo: 0.25, traco: 0.3, basico: 0.25, duracao: 0.3, resiste: 0, segura: 0 };

/** Quanto vale cada combo: a força geral, vezes a do tipo (trio, universo, lendária) e a da raridade. */
export function forcaDoCombo(id: string, forca = FORCA_DOS_COMBOS): number {
  const tipo = id.startsWith('trio-') ? FORCA_DOS_TRIOS : id.startsWith('universo') ? FORCA_DO_UNIVERSO : id.startsWith('lenda-') ? FORCA_DAS_LENDARIAS : 1;
  return forca * tipo * FORCA_DA_RARIDADE[raridadeDe(id)];
}
/** O bônus de verdade de um combo na luta (o da tabela vezes a força do combo, no teto) — o que a tela mostra. */
export function bonusEfetivo(b: Partial<Bonus>, id: string, limite: Bonus = TETO): Partial<Bonus> {
  const k = forcaDoCombo(id);
  return Object.fromEntries((Object.keys(b) as (keyof Bonus)[]).map((c) => [c, Math.min(limite[c], (b[c] ?? 0) * k)]));
}
const soma = (a: Bonus, b: Partial<Bonus>, k = 1): Bonus => {
  const r = { ...a };
  for (const chave of Object.keys(b) as (keyof Bonus)[]) r[chave] = Math.min(TETO[chave], r[chave] + (b[chave] ?? 0) * k);
  return r;
};

/** Os combos acesos no trio, o bônus de cada um dos três e o que eles tiram do trio rival. */
export function combosDoTrio(trio: readonly string[], forca = FORCA_DOS_COMBOS): { combos: ComboAtivo[]; bonus: Record<string, Bonus>; nosRivais: Bonus } {
  const bonus: Record<string, Bonus> = Object.fromEntries(trio.map((id) => [id, { ...SEM_BONUS }]));
  const combos: ComboAtivo[] = [];
  // o que os combos tiram do trio rival (em positivo; a luta subtrai do bônus de cada rival), até o PISO
  let nosRivais: Bonus = { ...SEM_BONUS };
  const enfraquece = (b: Partial<Bonus> | undefined, k: number) => {
    if (!b) return;
    const r = { ...nosRivais };
    for (const chave of Object.keys(b) as (keyof Bonus)[]) r[chave] = Math.min(PISO[chave], r[chave] + (b[chave] ?? 0) * k);
    nosRivais = r;
  };
  /*
   * O teto: um apoio que faz tudo (Carga, cura, reviver, limpar) acendia nove
   * combos sozinho, e o trio com ele vencia quase sempre. Cada um recebe no
   * máximo COMBOS_POR_LUTADOR combos e o trio tem no máximo COMBOS_POR_TRIO
   * combos de dupla — na ordem de REGRAS. Universo, trio e duplas lendárias ficam fora do limite.
   */
  const recebidos = new Map<string, number>();
  for (const r of REGRAS) {
    // cada combo acende uma vez por quem ganha (dois ajudando o mesmo não somam)
    for (const b of trio) {
      if (combos.length >= COMBOS_POR_TRIO) break;
      if ((recebidos.get(b) ?? 0) >= COMBOS_POR_LUTADOR) continue;
      if (!feitioDe(b)[r.ganha]) continue;
      const ajudantes = trio.filter((a) => a !== b && feitioDe(a)[r.ajuda]);
      if (!ajudantes.length) continue;
      const k = forcaDoCombo(r.id, forca);
      bonus[b] = soma(bonus[b]!, r.bonus, k);
      enfraquece(r.nosRivais, k);
      recebidos.set(b, (recebidos.get(b) ?? 0) + 1);
      combos.push({ id: r.id, nome: r.nome, texto: r.texto, de: ajudantes, para: [b], bonus: r.bonus, ...(r.nosRivais ? { nosRivais: r.nosRivais } : {}), ...(r.pulso ? { pulso: r.pulso, dono: b } : {}) });
    }
  }
  const porUniverso = new Map<string, string[]>();
  for (const id of trio) { const c = byId[id], u = c ? grupoDoUniverso(c) : ''; porUniverso.set(u, [...(porUniverso.get(u) ?? []), id]); }
  for (const [u, ids] of porUniverso) {
    if (ids.length < 2) continue;
    const id = ids.length === 3 ? 'universo-3' : 'universo-2', b = ids.length === 3 ? UNIVERSO.tres : UNIVERSO.dois;
    for (const x of ids) bonus[x] = soma(bonus[x]!, b, forcaDoCombo(id, forca));
    combos.push({ id, nome: ids.length === 3 ? `Trio de ${u}` : `Dupla de ${u}`, texto: 'mais dano e mais Vida', de: ids, para: ids, bonus: b });
  }
  for (const t of TRIOS) {
    const ids = quemFormaOTrio(trio, t);
    if (!ids) continue;
    const k = forcaDoCombo(t.id, forca);
    for (const id of trio) bonus[id] = soma(bonus[id]!, t.bonus, k);
    enfraquece(t.nosRivais, k);
    combos.push({ id: t.id, nome: t.nome, texto: t.texto, de: ids, para: [...trio], bonus: t.bonus, ...(t.nosRivais ? { nosRivais: t.nosRivais } : {}), ...(t.pulso ? { pulso: t.pulso, dono: ids[0] } : {}) });
  }
  for (const l of DUPLAS_LENDARIAS) {
    if (!trio.includes(l.a) || !trio.includes(l.b)) continue;
    const para = l.so ? [l.so] : [l.a, l.b], k = forcaDoCombo(l.id, forca);
    for (const id of para) bonus[id] = soma(bonus[id]!, l.bonus, k);
    combos.push({ id: l.id, nome: l.nome, texto: l.texto, de: [l.a, l.b], para, bonus: l.bonus, ...(l.pulso ? { pulso: l.pulso, dono: l.a } : {}) });
  }
  return { combos, bonus, nosRivais };
}

/*
 * As ligações para a força do trio (campaign.ts) e para a medição
 * (scripts/medir-forca.ts): quantas vezes cada combo acende no trio. O peso de
 * cada uma sai das lutas simuladas, como a força de cada personagem.
 */
export const LIGACOES_DOS_COMBOS: readonly string[] = [...REGRAS.map((r) => r.id), 'universo-2', 'universo-3', ...TRIOS.map((t) => t.id), 'lenda'];
export function ligacoesDosCombos(trio: readonly string[]): Record<string, number> {
  const n: Record<string, number> = Object.fromEntries(LIGACOES_DOS_COMBOS.map((l) => [l, 0]));
  // as duplas lendárias contam juntas (são muitas e cada uma aparece pouco)
  for (const c of combosDoTrio(trio).combos) { const id = c.id.startsWith('lenda-') ? 'lenda' : c.id; n[id] = Math.min(2, (n[id] ?? 0) + 1); }
  return n;
}
