/*
 * FASE F · as identidades públicas.
 *
 * O sistema antigo (`rolesFor`) marcava uma função se **existisse** um efeito
 * daquele tipo na ficha. A medição da FASE E mostrou o resultado: "Dano" em
 * 250 de 250 personagens, porque todo mundo tem ataque básico e ataque básico
 * machuca; 16 combinações distintas para 250 lutadores; e o corte em três
 * silenciando identidade em 114 deles, quase sempre a mais rara.
 *
 * Uma etiqueta que todo mundo tem não é identidade — é ruído ocupando espaço
 * numa tela onde o jogador precisa escolher entre três cartas.
 *
 * Aqui a regra é outra, e vem do documento da direção: **mecânica + simulação
 * + override manual**. Cada identidade é ganha por evidência, e a evidência é
 * comparada com o elenco inteiro: um personagem recebe "Área" porque está
 * entre os que mais acertam vários alvos ao mesmo tempo, não porque tem uma
 * habilidade que acerta dois.
 *
 * As medições estão em docs/identidades-medidas.json (10.000 lutas) e a
 * derivação em scripts/derivar-identidades.ts, que escreve o resultado em
 * src/data/identidades.ts. Este arquivo guarda só a taxonomia e o que cada
 * termo quer dizer para quem lê.
 */
import type { Character } from '../engine/types';
import { identidadesPorPersonagem } from '../data/identidades';

export type Identidade =
  | 'Pressão' | 'Explosão' | 'Finalização' | 'Área' | 'Dano contínuo'
  | 'Tanque' | 'Sobrevivência' | 'Proteção' | 'Cura' | 'Regeneração'
  | 'Controle' | 'Interrupção' | 'Ritmo' | 'Suporte' | 'Carga'
  | 'Buff' | 'Debuff' | 'Virada' | 'Preparação' | 'Transformação'
  | 'Contra-ataque' | 'Especialista' | 'Reviver' | 'Renascer';

/*
 * A taxonomia da direção tinha 23 termos. Este arquivo tem 22.
 *
 * "Invocação" ficou de fora porque o motor não tem invocação: nenhum efeito
 * cria um lutador novo no campo. Dar a etiqueta a quem aplica muitos Status,
 * ou a quem tem tema de invocar, seria exatamente a tag incidental enganosa
 * que a direção mandou não criar. Se a mecânica existir um dia, o termo entra
 * com ela.
 */

/** O que cada identidade significa, na voz do jogo. */
export const explicacaoDaIdentidade: Record<Identidade, string> = {
  'Pressão': 'Dano constante, luta inteira. Não depende de um momento certo.',
  'Explosão': 'Concentra muito dano num golpe só.',
  'Finalização': 'Converte inimigos feridos em inimigos fora da luta.',
  'Área': 'Boa parte do dano acerta vários inimigos de uma vez.',
  'Dano contínuo': 'Deixa o inimigo perdendo Vida sozinho, depois do golpe.',
  'Tanque': 'Absorve o ataque do trio rival e continua de pé.',
  'Sobrevivência': 'Termina a luta vivo com mais frequência que a maioria.',
  'Proteção': 'Dá Escudo e reduz o dano que o trio recebe.',
  'Cura': 'Devolve Vida aos aliados.',
  'Regeneração': 'Recupera a própria Vida ao longo da luta.',
  'Controle': 'Tira o turno do inimigo: prende, paralisa, silencia ou confunde.',
  'Interrupção': 'Corta habilidades inimigas durante o Preparo.',
  'Ritmo': 'Acelera o próprio trio ou atrasa o adversário.',
  'Suporte': 'Ajuda o trio de mais de uma maneira.',
  'Carga': 'Enche a Carga dos aliados e faz as habilidades deles saírem antes.',
  'Buff': 'Reforça os aliados com Status positivos.',
  'Debuff': 'Enfraquece o trio rival com Status negativos.',
  'Virada': 'Costuma vencer lutas em que o trio esteve atrás.',
  'Preparação': 'Golpes fortes que anunciam antes — e podem ser interrompidos.',
  'Transformação': 'Fica mais forte conforme a luta avança.',
  'Contra-ataque': 'Apanhar é o que carrega as habilidades dele.',
  'Especialista': 'Só age na situação certa, e aí resolve.',
  'Reviver': 'Levanta um aliado que caiu, uma vez por luta.',
  'Renascer': 'Quando cai, volta sozinho uma vez, com parte da Vida.',
};

/** A ordem em que as identidades aparecem, quando o personagem tem várias. */
export const ordemDasIdentidades: readonly Identidade[] = [
  'Pressão', 'Explosão', 'Área', 'Dano contínuo', 'Finalização',
  'Controle', 'Interrupção', 'Debuff', 'Ritmo',
  'Reviver', 'Cura', 'Proteção', 'Buff', 'Carga', 'Suporte',
  'Renascer', 'Tanque', 'Regeneração', 'Sobrevivência',
  'Transformação', 'Contra-ataque', 'Preparação', 'Virada', 'Especialista',
];

/** Agrupamento usado pelos filtros e pelo Draft, para falar de lacunas. */
export const familiaDaIdentidade: Record<Identidade, 'ataque' | 'atrapalha' | 'ajuda' | 'aguenta' | 'jeito'> = {
  'Pressão': 'ataque', 'Explosão': 'ataque', 'Área': 'ataque', 'Dano contínuo': 'ataque', 'Finalização': 'ataque',
  'Controle': 'atrapalha', 'Interrupção': 'atrapalha', 'Debuff': 'atrapalha', 'Ritmo': 'atrapalha',
  'Reviver': 'ajuda', 'Renascer': 'aguenta', 'Cura': 'ajuda', 'Proteção': 'ajuda', 'Buff': 'ajuda', 'Carga': 'ajuda', 'Suporte': 'ajuda',
  'Tanque': 'aguenta', 'Regeneração': 'aguenta', 'Sobrevivência': 'aguenta',
  'Transformação': 'jeito', 'Contra-ataque': 'jeito', 'Preparação': 'jeito', 'Virada': 'jeito', 'Especialista': 'jeito',
};

/* ---------------------------------------------------------------------------
 * Acesso
 * ------------------------------------------------------------------------- */

/** As identidades públicas de um lutador. */
export const identidadesDe = (c: Character | string): readonly Identidade[] =>
  identidadesPorPersonagem[typeof c === 'string' ? c : c.id] ?? [];

/** Tudo que o trio reúne, sem repetir, na ordem da taxonomia. */
export const identidadesDoTrio = (trio: readonly (Character | string)[]): Identidade[] => {
  const juntas = new Set(trio.flatMap((c) => identidadesDe(c)));
  return ordemDasIdentidades.filter((x) => juntas.has(x));
};

/** O que este candidato traz que o trio ainda não tem. */
export const oQueAdiciona = (candidato: Character | string, trio: readonly (Character | string)[]): Identidade[] => {
  const jaTem = new Set(identidadesDoTrio(trio));
  return identidadesDe(candidato).filter((x) => !jaTem.has(x));
};

/*
 * As lacunas, ditas só quando são verdade.
 *
 * O documento da direção pede "Pouca proteção", "Pouca recuperação", "Pouca
 * interrupção" — e acrescenta: *"Somente se calculado honestamente."* Então
 * cada lacuna aqui corresponde a um conjunto de identidades, e só aparece
 * quando nenhum dos três personagens tem nenhuma delas. Um trio com um
 * curandeiro não ouve que lhe falta recuperação.
 */
const LACUNAS: readonly { texto: string; cobertaPor: readonly Identidade[] }[] = [
  { texto: 'Pouca proteção', cobertaPor: ['Proteção', 'Tanque'] },
  { texto: 'Pouca recuperação', cobertaPor: ['Cura', 'Regeneração', 'Reviver', 'Renascer'] },
  { texto: 'Pouca interrupção', cobertaPor: ['Interrupção', 'Controle'] },
  { texto: 'Pouco dano concentrado', cobertaPor: ['Explosão', 'Finalização'] },
];

export const lacunasDoTrio = (trio: readonly (Character | string)[]): string[] => {
  if (trio.length === 0) return [];
  const tem = new Set(identidadesDoTrio(trio));
  return LACUNAS.filter((l) => !l.cobertaPor.some((x) => tem.has(x))).map((l) => l.texto);
};

/*
 * O guia de cada identidade, para quem toca na etiqueta.
 *
 * O jogador vê "Especialista" ou "Controle" no Draft e nem sempre sabe o que
 * aquilo faz. Tocar na etiqueta abre um cartão curto: o que é, o que você vê
 * acontecer na luta, com o que combina no trio e o que atrapalha.
 */
export interface GuiaDaIdentidade {
  /** O que você vê acontecer na luta, em duas frases curtas. */
  naLuta: readonly [string, string];
  /** Identidades que, no mesmo trio, deixam esta mais forte. */
  combina: readonly Identidade[];
  /** O que atrapalha quem tem esta identidade. */
  cuidado: string;
}

export const guiaDaIdentidade: Record<Identidade, GuiaDaIdentidade> = {
  'Pressão': { naLuta: ['Ataca o tempo todo, sem esperar Carga encher.', 'O dano dele soma devagar e não para.'], combina: ['Buff', 'Ritmo'], cuidado: 'Tanques e Escudos seguram esse dano constante.' },
  'Explosão': { naLuta: ['Junta força e solta um golpe enorme de uma vez.', 'Um acerto bem dado tira boa parte da Vida do alvo.'], combina: ['Carga', 'Debuff'], cuidado: 'Se o golpe grande for cortado ou bater num Escudo, perde a vez.' },
  'Finalização': { naLuta: ['Fica mais perigoso quando o inimigo está ferido.', 'Tira da luta quem já está com pouca Vida.'], combina: ['Pressão', 'Área'], cuidado: 'Cura e Regeneração tiram os inimigos da zona de perigo.' },
  'Área': { naLuta: ['Um golpe acerta vários inimigos ao mesmo tempo.', 'Machuca o trio rival inteiro de uma vez.'], combina: ['Finalização', 'Dano contínuo'], cuidado: 'Contra um Tanque só, o dano espalhado rende menos.' },
  'Dano contínuo': { naLuta: ['Deixa o inimigo Queimando ou envenenado.', 'O alvo continua perdendo Vida depois do golpe.'], combina: ['Área', 'Controle'], cuidado: 'Cura e Regeneração compensam esse dano que vem aos poucos.' },
  'Tanque': { naLuta: ['Tem muita Vida ou se protege muito bem.', 'Fica de pé enquanto os aliados atacam.'], combina: ['Cura', 'Contra-ataque'], cuidado: 'Dano contínuo e Exposto fazem ele cair aos poucos.' },
  'Sobrevivência': { naLuta: ['Costuma terminar a luta ainda de pé.', 'Escapa de quedas que derrubariam outros.'], combina: ['Virada', 'Pressão'], cuidado: 'Explosões rápidas no começo pegam antes dele se firmar.' },
  'Proteção': { naLuta: ['Coloca Escudo nos aliados.', 'O trio recebe menos dano enquanto ele estiver na luta.'], combina: ['Preparação', 'Explosão'], cuidado: 'Se ele cair primeiro, o trio fica sem defesa.' },
  'Cura': { naLuta: ['Devolve Vida a quem está ferido.', 'Mantém os aliados de pé por mais tempo.'], combina: ['Tanque', 'Pressão'], cuidado: 'Explosão e Finalização derrubam antes da cura chegar.' },
  'Regeneração': { naLuta: ['Recupera a própria Vida aos poucos, sozinho.', 'Quanto mais longa a luta, mais isso rende.'], combina: ['Tanque', 'Contra-ataque'], cuidado: 'Controle e golpes grandes derrubam antes da recuperação somar.' },
  'Controle': { naLuta: ['Prende, paralisa, silencia ou confunde o inimigo.', 'Quem está controlado perde a vez de agir.'], combina: ['Explosão', 'Dano contínuo'], cuidado: 'O controle dura poucos segundos: sem aliados que causem dano, o inimigo volta inteiro.' },
  'Interrupção': { naLuta: ['Corta a habilidade inimiga enquanto ela é preparada.', 'O golpe grande do rival não sai.'], combina: ['Pressão', 'Controle'], cuidado: 'Contra quem ataca rápido, sem Preparo, não tem o que cortar.' },
  'Ritmo': { naLuta: ['Deixa o próprio trio mais rápido ou o rival mais lento.', 'Seu lado age mais vezes no mesmo tempo.'], combina: ['Pressão', 'Área'], cuidado: 'Agir mais vezes rende pouco se o trio não tiver quem cause dano; Controle para tudo.' },
  'Suporte': { naLuta: ['Ajuda o trio de várias formas ao mesmo tempo.', 'Cura, protege ou reforça conforme a luta pede.'], combina: ['Explosão', 'Pressão'], cuidado: 'Bate pouco: precisa de aliados que causem o dano.' },
  'Carga': { naLuta: ['Enche a Carga dos aliados.', 'As habilidades do trio saem antes e mais vezes.'], combina: ['Explosão', 'Preparação'], cuidado: 'Se o trio não tiver habilidades fortes, a Carga extra rende pouco.' },
  'Buff': { naLuta: ['Dá Status bons aos aliados: Fortalecido, Acelerado…', 'Os aliados batem mais forte ou mais rápido.'], combina: ['Pressão', 'Área'], cuidado: 'Se o aliado reforçado cair, o reforço cai junto; Enfraquecido do rival anula parte dele.' },
  'Debuff': { naLuta: ['Deixa o inimigo Exposto, Enfraquecido ou Lento.', 'O rival bate menos e apanha mais.'], combina: ['Explosão', 'Finalização'], cuidado: 'Os Status duram poucos segundos: o trio precisa bater enquanto eles valem.' },
  'Virada': { naLuta: ['Fica mais forte quando o trio está perdendo.', 'Costuma vencer lutas que pareciam perdidas.'], combina: ['Tanque', 'Sobrevivência'], cuidado: 'Se cair cedo, não sobra tempo para a virada.' },
  'Preparação': { naLuta: ['Anuncia o golpe antes: aparece o Preparo.', 'Quando sai, o golpe é muito forte.'], combina: ['Proteção', 'Controle'], cuidado: 'Interrupção corta o golpe no meio do Preparo.' },
  'Transformação': { naLuta: ['Muda de forma ou fica mais forte no meio da luta.', 'O começo é mais fraco; o final é o melhor momento.'], combina: ['Tanque', 'Proteção'], cuidado: 'Explosão no começo derruba antes da transformação.' },
  'Contra-ataque': { naLuta: ['Cada golpe que recebe carrega as habilidades dele.', 'Quanto mais apanha, mais rápido revida.'], combina: ['Tanque', 'Regeneração'], cuidado: 'Controle e dano contínuo machucam sem dar Carga a ele.' },
  'Especialista': { naLuta: ['Espera a situação certa para agir.', 'Quando ela aparece, decide a luta.'], combina: ['Suporte', 'Carga'], cuidado: 'Se a situação não aparecer, ele faz pouco.' },
  'Reviver': { naLuta: ['Quando um aliado cai, a habilidade dele o levanta com parte da Vida.', 'Uma vez por luta — e cada lutador só volta uma vez.'], combina: ['Explosão', 'Pressão'], cuidado: 'Leva um tempo de Preparo: se for interrompido ou cair antes, o aliado fica no chão.' },
  'Renascer': { naLuta: ['Quando cai, fica em brasas por um instante e volta sozinho.', 'Volta com parte da Vida, uma vez por luta.'], combina: ['Tanque', 'Virada'], cuidado: 'A Death Note impede: quem é executado não renasce.' },
};

/** Quantos lutadores têm cada identidade. */
export const quantosTem = (x: Identidade) => Object.values(identidadesPorPersonagem).filter((ids) => ids.includes(x)).length;
/** Alguns lutadores com a identidade, para o cartão. */
export const exemplosDe = (x: Identidade, n = 4) => {
  // espalhados pela lista, para mostrar universos diferentes
  const todos = Object.entries(identidadesPorPersonagem).filter(([, ids]) => ids.includes(x)).map(([id]) => id);
  return todos.length <= n ? todos : Array.from({ length: n }, (_, i) => todos[Math.floor((i * todos.length) / n)]!);
};
