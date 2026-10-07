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
  | 'Contra-ataque' | 'Especialista';

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
};

/** A ordem em que as identidades aparecem, quando o personagem tem várias. */
export const ordemDasIdentidades: readonly Identidade[] = [
  'Pressão', 'Explosão', 'Área', 'Dano contínuo', 'Finalização',
  'Controle', 'Interrupção', 'Debuff', 'Ritmo',
  'Cura', 'Proteção', 'Buff', 'Carga', 'Suporte',
  'Tanque', 'Regeneração', 'Sobrevivência',
  'Transformação', 'Contra-ataque', 'Preparação', 'Virada', 'Especialista',
];

/** Agrupamento usado pelos filtros e pelo Draft, para falar de lacunas. */
export const familiaDaIdentidade: Record<Identidade, 'ataque' | 'atrapalha' | 'ajuda' | 'aguenta' | 'jeito'> = {
  'Pressão': 'ataque', 'Explosão': 'ataque', 'Área': 'ataque', 'Dano contínuo': 'ataque', 'Finalização': 'ataque',
  'Controle': 'atrapalha', 'Interrupção': 'atrapalha', 'Debuff': 'atrapalha', 'Ritmo': 'atrapalha',
  'Cura': 'ajuda', 'Proteção': 'ajuda', 'Buff': 'ajuda', 'Carga': 'ajuda', 'Suporte': 'ajuda',
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
  { texto: 'Pouca recuperação', cobertaPor: ['Cura', 'Regeneração'] },
  { texto: 'Pouca interrupção', cobertaPor: ['Interrupção', 'Controle'] },
  { texto: 'Pouco dano concentrado', cobertaPor: ['Explosão', 'Finalização'] },
];

export const lacunasDoTrio = (trio: readonly (Character | string)[]): string[] => {
  if (trio.length === 0) return [];
  const tem = new Set(identidadesDoTrio(trio));
  return LACUNAS.filter((l) => !l.cobertaPor.some((x) => tem.has(x))).map((l) => l.texto);
};
