import { characters } from '../data/characters';
import type { Character } from '../engine/types';

/*
 * Conquistas (pedido do jogador): uma para cada personagem, 250 no total.
 *
 * Libera quando você termina as 10 lutas de uma Jornada com o personagem no
 * trio. Só a primeira vez conta: jogar de novo com quem já está liberado não
 * muda nada, e só os outros do trio são liberados. A ideia é incentivar a
 * jogar com personagens diferentes.
 *
 * O aparelho guarda as suas (`Profile.conquistas`, com a data). Com conta, o
 * servidor guarda as que ele mesmo validou, e são essas que valem no ranking
 * de conquistas; ao abrir a tela, as do servidor entram também no aparelho.
 */
export type Conquistas = Record<string, string>;

/* As abas da tela: cada universo cai em uma. */
export type Aba = 'anime' | 'herois' | 'games' | 'desenhos';
export const ABAS: readonly { id: Aba; nome: string; cor: string }[] = [
  { id: 'anime', nome: 'Anime', cor: '#ff7a8a' },
  { id: 'herois', nome: 'Heróis', cor: '#6fb4ff' },
  { id: 'games', nome: 'Games', cor: '#8de06a' },
  { id: 'desenhos', nome: 'Desenhos', cor: '#ffc65a' },
];
const ANIME = new Set(['Dragon Ball', 'Naruto', 'One Piece', 'Jujutsu Kaisen', 'Death Note', 'Pokémon', 'One Punch Man', 'Demon Slayer', 'Bleach',
  'Attack on Titan', 'Hunter x Hunter', 'Fullmetal Alchemist', 'Berserk', 'JoJo', 'Chainsaw Man', 'Frieren', 'Spy x Family', 'Solo Leveling',
  'Tokyo Ghoul', 'Yu-Gi-Oh!', 'Cavaleiros do Zodíaco', 'Yu Yu Hakusho', 'Sailor Moon']);
const HEROIS = new Set(['Marvel', 'DC', 'Image', 'Dark Horse']);
const GAMES = new Set(['Final Fantasy VII', 'God of War', 'The Legend of Zelda', 'Metroid', 'Devil May Cry', 'Bayonetta', 'Halo', 'DOOM', 'Metal Gear',
  'Metal Gear Rising', 'Resident Evil', 'Tomb Raider', "Assassin's Creed", 'Sonic the Hedgehog', 'Mega Man', 'Mega Man X', 'Super Mario',
  'Street Fighter', 'Mortal Kombat', 'Tekken', 'Kingdom Hearts', 'NieR: Automata', 'Sekiro', 'Elden Ring', 'Hitman', 'Warcraft', 'The Witcher',
  'Dead Space', 'Half-Life', 'Ninja Gaiden', 'Silent Hill', 'Kirby', 'Donkey Kong', 'Castlevania', 'Prince of Persia']);
export const abaDo = (c: Character): Aba => (ANIME.has(c.universe) ? 'anime' : HEROIS.has(c.universe) ? 'herois' : GAMES.has(c.universe) ? 'games' : 'desenhos');

/* Os personagens de cada aba, agrupados por universo (os maiores primeiro) e, dentro dele, por nome. */
export const PERSONAGENS_DA_ABA: Record<Aba, Character[]> = (() => {
  const tamanho = new Map<string, number>();
  for (const c of characters) tamanho.set(c.universe, (tamanho.get(c.universe) ?? 0) + 1);
  const r = { anime: [], herois: [], games: [], desenhos: [] } as Record<Aba, Character[]>;
  for (const c of characters) r[abaDo(c)].push(c);
  for (const lista of Object.values(r)) lista.sort((a, b) => tamanho.get(b.universe)! - tamanho.get(a.universe)! || a.universe.localeCompare(b.universe, 'pt-BR') || a.name.localeCompare(b.name, 'pt-BR'));
  return r;
})();

export const TOTAL_DE_CONQUISTAS = characters.length;

/*
 * Os títulos do colecionador: cada marco de personagens liberados dá um nome
 * novo. O próximo marco aparece na tela, com a barra do quanto falta.
 */
export const TITULOS: readonly { minimo: number; nome: string; cor: string }[] = [
  { minimo: 0, nome: 'Recruta', cor: '#9aa7b8' },
  { minimo: 3, nome: 'Aventureiro', cor: '#86e3a8' },
  { minimo: 10, nome: 'Colecionador', cor: '#6fd0ff' },
  { minimo: 25, nome: 'Veterano', cor: '#8a9cff' },
  { minimo: 50, nome: 'Mestre dos Trios', cor: '#c38aff' },
  { minimo: 100, nome: 'Lenda', cor: '#ff8ad0' },
  { minimo: 150, nome: 'Mito', cor: '#ff9a5a' },
  { minimo: 200, nome: 'Imortal', cor: '#ffd36b' },
  { minimo: TOTAL_DE_CONQUISTAS, nome: 'Senhor do Nexus', cor: '#fff3b0' },
];
export function tituloDe(liberadas: number) {
  let i = 0;
  while (i + 1 < TITULOS.length && liberadas >= TITULOS[i + 1]!.minimo) i++;
  const atual = TITULOS[i]!, proximo = TITULOS[i + 1] ?? null;
  const progresso = proximo ? (liberadas - atual.minimo) / (proximo.minimo - atual.minimo) : 1;
  return { atual, proximo, progresso, nivel: i + 1 };
}

/* Só ids que existem no elenco, com data válida. */
export function limpar(x: unknown): Conquistas {
  if (!x || typeof x !== 'object' || Array.isArray(x)) return {};
  const ids = new Set(characters.map((c) => c.id)), r: Conquistas = {};
  for (const [id, data] of Object.entries(x as Record<string, unknown>)) if (ids.has(id) && typeof data === 'string' && !Number.isNaN(Date.parse(data))) r[id] = data;
  return r;
}

/* Terminou as 10 lutas com este trio: libera quem ainda não estava liberado. */
export function liberar(atual: Conquistas, trio: readonly string[], quando = new Date().toISOString()) {
  const conquistas = { ...atual }, novas: string[] = [];
  for (const id of trio) if (!conquistas[id] && characters.some((c) => c.id === id)) { conquistas[id] = quando; novas.push(id); }
  return { conquistas, novas };
}

/* As do servidor entram no aparelho; fica a data mais antiga de cada uma. */
export function juntar(local: Conquistas, doServidor: readonly { id: string; data: string }[]): Conquistas {
  const r = { ...local };
  for (const { id, data } of doServidor) if (characters.some((c) => c.id === id) && !Number.isNaN(Date.parse(data)) && (!r[id] || Date.parse(data) < Date.parse(r[id]!))) r[id] = data;
  return r;
}

/* Três personagens ainda bloqueados, para a sugestão "jogue com eles" (muda a cada dia, igual para o dia todo). */
export function sugestao(conquistas: Conquistas, dia = new Date().toISOString().slice(0, 10)): Character[] {
  const faltam = characters.filter((c) => !conquistas[c.id]);
  if (faltam.length <= 3) return faltam;
  let h = 0;
  for (const ch of dia) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const r: Character[] = [];
  const usados = new Set<number>();
  while (r.length < 3) { h = (h * 1103515245 + 12345) >>> 0; const i = h % faltam.length; if (!usados.has(i)) { usados.add(i); r.push(faltam[i]!); } }
  return r;
}
