import type { Character } from '../engine/types';

/*
 * Os universos grandes divididos em equipes (pedido do jogador: "a dupla de universo que acontece muito é a da
 * Marvel, porque tem 37 personagens… separa: X-Men é um universo, não a Marvel como um todo"). O combo de
 * universo olha a equipe; a ficha mostra "Marvel · X-Men". Universo sem divisão continua sendo um só.
 */
const EQUIPES: Record<string, readonly string[]> = {
  'X-Men': ['iceman', 'wolverine', 'magneto', 'storm', 'cyclops', 'jeangrey', 'rogue', 'gambit', 'professorx', 'deadpool'],
  Vingadores: ['blackwidow', 'hawkeye', 'hulk', 'thor', 'ironman', 'captain', 'blackpanther', 'scarletwitch', 'vision', 'antman', 'captainmarvel', 'loki', 'ultron', 'strange'],
  'Cósmicos': ['gamora', 'drax', 'thanos', 'silversurfer', 'galactus', 'starlord', 'groot', 'rocket', 'doctordoom'],
  'Ruas de Nova York': ['spiderwoman', 'spiderman', 'daredevil', 'punisher', 'ghostrider', 'blade', 'moonknight', 'venom', 'carnage', 'greengoblin'],
  'Liga da Justiça': ['superman', 'flash', 'wonderwoman', 'aquaman', 'greenlantern', 'cyborg', 'shazam', 'darkseid', 'lexluthor'],
  Gotham: ['batman', 'coringa', 'arlequina', 'robin', 'nightwing', 'catwoman', 'scarecrow', 'mrfreeze', 'poisonivy'],
  'Sombras da DC': ['raven', 'constantine'],
};
const EQUIPE_DE: Record<string, string> = Object.fromEntries(Object.entries(EQUIPES).flatMap(([e, ids]) => ids.map((id) => [id, e])));
/** O grupo que conta para o combo de universo: a equipe, se o universo é dividido; senão, o próprio universo. */
export const grupoDoUniverso = (c: Pick<Character, 'id' | 'universe'>): string => EQUIPE_DE[c.id] ?? c.universe;
/** O que a ficha mostra: "Marvel · X-Men", ou só o universo. */
export const universoDaFicha = (c: Pick<Character, 'id' | 'universe'>): string => (EQUIPE_DE[c.id] ? `${c.universe} · ${EQUIPE_DE[c.id]}` : c.universe);
