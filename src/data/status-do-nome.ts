import type { Character, Effect, StatusId } from '../engine/types';

/*
 * O Status tem que combinar com o nome do golpe.
 *
 * Pedido do jogador: "a Dobra de fogo tá aplicando Eletrificado, deveria
 * aplicar Queimando… verifique outro personagem, se tá incondizente com o nome
 * do poder". Os Status saíam dos modelos de cada estilo (o "tempestade"
 * eletrifica, o reforço do traço queima), sem olhar o nome. A varredura
 * (cada golpe que aplica Queimando, Eletrificado, Congelado, Envenenado ou
 * Dormindo, comparado com o nome) achou estes, e cada um troca para o Status
 * que o poder tem na obra. A força volta para a medição depois
 * (scripts/medir-forca.ts e equilibrar-personagens.ts).
 *
 * Chave: id:habilidade (0 a 2), id:b (ataque básico), id:t (traço).
 */
interface Troca { de: StatusId; para: StatusId; valor: number }

const TROCAS: Record<string, Troca> = {
  // a Dobra de fogo queima; o Estado Avatar, que junta todos os elementos, fica com o choque
  'korra:0': { de: 'electric', para: 'burning', valor: 6 },
  'korra:2': { de: 'burning', para: 'electric', valor: 0.16 },
  // o Canhão incinerador queima, não dá choque
  'genos:0': { de: 'electric', para: 'burning', valor: 6 },
  // o sangue do Muzan e a podridão escarlate da Malenia envenenam
  'muzan:t': { de: 'burning', para: 'poison', valor: 2 },
  'malenia:t': { de: 'burning', para: 'poison', valor: 4 },
  // a Ressonância é o prego no boneco: a ferida sangra
  'nobara:t': { de: 'burning', para: 'bleed', valor: 8 },
  // golpes de lâmina e de corrente fazem sangrar
  'wesker:1': { de: 'poison', para: 'bleed', valor: 14 },
  'pyramidhead:b': { de: 'burning', para: 'bleed', valor: 6 },
  'spawn:1': { de: 'burning', para: 'bleed', valor: 6 },
  // a Frostmourne é gelo; o fantasma do Danny também gela
  'arthas:b': { de: 'burning', para: 'slow', valor: 0.1 },
  'dannyphantom:b': { de: 'burning', para: 'slow', valor: 0.1 },
  'dannyphantom:1': { de: 'burning', para: 'slow', valor: 0.1 },
  // magia das trevas e morto-vivo amaldiçoam
  'arthas:1': { de: 'burning', para: 'cursed', valor: 0.15 },
  'skeletor:b': { de: 'burning', para: 'cursed', valor: 0.12 },
  'mummra:b': { de: 'burning', para: 'cursed', valor: 0.12 },
  'mummra:1': { de: 'burning', para: 'cursed', valor: 0.12 },
  // a presença do Cabeça de Pirâmide enfraquece
  'pyramidhead:1': { de: 'burning', para: 'weakened', valor: 0.08 },
  // o discurso do Mojo Jojo prende todo mundo ouvindo; o chapéu-helicóptero confunde
  'mojojojo:2': { de: 'electric', para: 'slow', valor: 0.16 },
  'bugiganga:1': { de: 'electric', para: 'confused', valor: 1 },
};

/* A série do básico com nome de fogo que dava choque: a Azula solta o relâmpago dela. */
const NOME_DA_SERIE: Record<string, string> = { azula: 'Faísca de relâmpago' };

export const GOLPES_COM_STATUS_TROCADO = Object.keys(TROCAS);

const troca = (chave: string, effects: readonly Effect[]): Effect[] => {
  const t = TROCAS[chave];
  if (!t) return [...effects];
  return effects.map((e) => (e.kind === 'status' && e.status === t.de ? { ...e, status: t.para, value: t.valor } : e));
};

export function aplicaStatusDoNome(c: Character): Character {
  const tem = Object.keys(TROCAS).some((k) => k.startsWith(`${c.id}:`)) || NOME_DA_SERIE[c.id];
  if (!tem) return c;
  const skills = c.skills.map((s, i) => ({ ...s, effects: troca(`${c.id}:${i}`, s.effects) })) as Character['skills'];
  const jeito = c.basic.jeito && NOME_DA_SERIE[c.id] ? { ...c.basic.jeito, nome: NOME_DA_SERIE[c.id]! } : c.basic.jeito;
  return {
    ...c, skills,
    basic: { ...c.basic, effects: troca(`${c.id}:b`, c.basic.effects), ...(jeito ? { jeito } : {}) },
    trait: { ...c.trait, effects: troca(`${c.id}:t`, c.trait.effects) },
  };
}
