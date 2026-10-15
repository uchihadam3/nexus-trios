import type { Character } from '../engine/types';

/*
 * Os universos grandes divididos em equipes (pedido do jogador: "a dupla de universo que acontece muito é a da
 * Marvel, porque tem 37 personagens… separa: X-Men é um universo, não a Marvel como um todo"). O combo de
 * universo olha a equipe. Universo sem divisão continua sendo um só.
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
/*
 * O universo que a ficha mostra (pedido do jogador: "em vez de colocar sexta-feira 13, coloca o nome do universo
 * dele… esse mesmo nome no Pinhead, no Ghostface… dos X-Men, você põe X-Men, em vez de colocar Marvel"). Os
 * universos grandes ficam com o nome deles (Naruto, Dragon Ball…), a Marvel e a DC pelas equipes de cima, e os
 * pequenos se juntam com os parecidos ("Lendas do Terror", "Nintendo", "Cartoon Network"…): 45 universos, cada um
 * com 5 personagens ou mais. Só a ficha muda: os combos de universo continuam olhando grupoDoUniverso.
 */
const UNIVERSOS_JUNTOS: Record<string, readonly string[]> = {
  "Avatar": ["Avatar", "A Lenda de Korra"],
  "Disney": ["Disney", "Lilo & Stitch"],
  "Pixar & DreamWorks": ["Toy Story", "Os Incríveis", "Shrek", "Megamente"],
  "Cartoon Network": ["Ben 10", "Hora de Aventura", "As Meninas Superpoderosas", "Johnny Bravo", "O Laboratório de Dexter", "Coragem", "Samurai Jack", "Steven Universo"],
  "Desenhos da TV": ["Bob Esponja", "Danny Phantom", "Padrinhos Mágicos", "Gravity Falls"],
  "Desenhos Clássicos": ["Tom e Jerry", "Pantera Cor-de-Rosa", "Popeye", "Scooby-Doo", "Inspetor Bugiganga", "Capitão Planeta"],
  "Heróis dos Anos 80": ["ThunderCats", "Masters of the Universe", "Transformers"],
  "Animação Adulta": ["Os Simpsons", "Family Guy", "Rick and Morty", "South Park"],
  "Nintendo": ["Super Mario", "The Legend of Zelda", "Kirby", "Donkey Kong", "Metroid", "Pokémon"],
  "Clássicos dos Games": ["Sonic the Hedgehog", "Crash Bandicoot", "Pac-Man", "Mega Man", "Mega Man X", "Cuphead", "Undertale", "Minecraft"],
  "Torneio de Luta": ["Street Fighter", "Tekken"],
  "Square Enix": ["Final Fantasy VII", "Kingdom Hearts", "NieR: Automata"],
  "Survival Horror": ["Resident Evil", "Dead Space", "The Last of Us"],
  "Caçadores de Demônios": ["Castlevania", "Devil May Cry", "Bayonetta"],
  "Fantasia Sombria": ["Sekiro", "Elden Ring", "Hollow Knight", "The Witcher", "Berserk"],
  "Lendas dos Games": ["God of War", "Halo", "DOOM", "Warcraft", "Half-Life", "Metal Gear", "Metal Gear Rising", "Hitman", "Assassin's Creed", "Ninja Gaiden", "Tomb Raider", "Prince of Persia", "Red Dead Redemption"],
  "Mitologia Nórdica": ["Skyrim", "Mitologia Nórdica"],
  "Lendas do Terror": ["Sexta-Feira 13", "A Hora do Pesadelo", "Halloween", "Brinquedo Assassino", "It", "Pânico", "O Massacre da Serra Elétrica", "Hellraiser", "O Chamado", "Invocação do Mal", "Silent Hill", "Alien"],
  "Cinema de Ação": ["John Wick", "O Exterminador do Futuro", "RoboCop", "Rambo", "Indiana Jones", "Piratas do Caribe", "Predador", "Matrix", "Monsterverse"],
  "Sagas do Cinema": ["Star Wars", "Harry Potter", "O Senhor dos Anéis"],
  "Quadrinhos Rebeldes": ["Image", "Dark Horse"],
  "Shonen": ["My Hero Academia", "One Punch Man", "Black Clover", "Fairy Tail", "Mob Psycho 100"],
  "Anime Sombrio": ["Attack on Titan", "Chainsaw Man", "Tokyo Ghoul", "Death Note", "Code Geass"],
  "Anime Clássico": ["Yu Yu Hakusho", "Sailor Moon", "Samurai X", "Cowboy Bebop", "Trigun", "Yu-Gi-Oh!", "Inuyasha"],
  "Isekai e Fantasia": ["Slime", "Overlord", "Re:Zero", "Sword Art Online", "Frieren", "Solo Leveling"],
  "Anime de Aventura": ["Fullmetal Alchemist", "JoJo", "Spy x Family", "Dr. Stone"],
};
const UNIVERSO_JUNTO: Record<string, string> = Object.fromEntries(Object.entries(UNIVERSOS_JUNTOS).flatMap(([u, de]) => de.map((x) => [x, u])));
/** Quem fica num universo que não é o da série dele (Kratos vai para a Mitologia Nórdica; a Ravena e o Constantine, para os Quadrinhos Rebeldes). */
const UNIVERSO_POR_ID: Record<string, string> = { raven: 'Quadrinhos Rebeldes', constantine: 'Quadrinhos Rebeldes', kratos: 'Mitologia Nórdica' };
/** O universo do personagem: o que a ficha mostra e o que agrupa os parecidos. */
export const universoDe = (c: Pick<Character, 'id' | 'universe'>): string => UNIVERSO_POR_ID[c.id] ?? EQUIPE_DE[c.id] ?? UNIVERSO_JUNTO[c.universe] ?? c.universe;
/** O que a ficha mostra: "X-Men", "Lendas do Terror", "Naruto"… */
export const universoDaFicha = universoDe;
