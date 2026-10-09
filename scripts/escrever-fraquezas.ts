/*
 * O ponto fraco de cada personagem: o que ELE não consegue fazer.
 *
 * Pedido do jogador: "o ponto fraco do Eren é Espinhos… todo mundo sofre com
 * Espinhos, todo mundo recebe dano em área — isso não é ponto fraco. Ponto
 * fraco tem a ver com as habilidades dele que ele não tá conseguindo fazer, ou
 * se ele tem pouca vida e morre rápido". A versão anterior comparava quanto
 * cada um vencia contra rivais de certa identidade ("contra Tanques",
 * "contra Área") — coisas que pesam em todo mundo. Agora o ponto fraco sai só
 * do próprio personagem, comparado com o resto do elenco:
 *
 * - Cai rápido: o primeiro do trio a cair bem mais que o normal, ou das menores
 *   Vidas do jogo — com o porquê (a Vida baixa, nenhuma cura ou proteção);
 * - Habilidade rara: uma habilidade dele quase não sai nas lutas (medido), e
 *   por quê — a regra de uso, o Preparo cortado ou a Carga que demora;
 * - Preparo longo: o golpe principal demora a sair e é cortado com frequência;
 * - Ataque lento: o ataque básico é dos mais lentos do jogo;
 * - Pouco dano: dos que menos causam dano por minuto de pé — depende do trio;
 * - Precisa apanhar: o traço só o fortalece quando ele recebe dano.
 *
 * Cada candidato ganha uma nota pelo tamanho do problema em relação ao elenco;
 * o maior sempre aparece, o segundo só quando também é forte.
 *
 * Uso: LUTAS=20000 npx tsx scripts/medir-fraquezas.ts && npx tsx scripts/escrever-fraquezas.ts
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import type { Character, Effect, Skill } from '../src/engine/types';
import type { TipoDeFraqueza } from '../src/data/ponto-fraco';

interface Medida {
  id: string; lutas: number; primeiroACair: number; cortados: number;
  usos: [number, number, number]; danoCausado: number; tempoDePe: number;
}
const dados = JSON.parse(readFileSync('docs/fraquezas-medidas.json', 'utf8')) as { lutas: number; medidas: Medida[] };
const porId = new Map(dados.medidas.map((m) => [m.id, m]));

const num = (v: number, casas = 0) => v.toLocaleString('pt-BR', { maximumFractionDigits: casas, minimumFractionDigits: 0 });
const pct = (v: number) => `${Math.round(v * 100)}%`;
/* Posição no elenco, de 0 (menor) a 1 (maior). */
const posicao = (valores: number[], v: number) => valores.filter((x) => x < v).length / Math.max(1, valores.length - 1);

const medidas = characters.map((c) => porId.get(c.id)).filter((m): m is Medida => !!m);
const vidas = characters.map((c) => c.hp), intervalos = characters.map((c) => c.interval);
const cortes = medidas.map((m) => m.cortados);
/* dano por minuto de pé: quem fica pouco tempo vivo não é "pouco dano", é "cai rápido" */
const ritmoDeDano = (m: Medida) => m.danoCausado / Math.max(5, m.tempoDePe) * 60;
const danos = medidas.map(ritmoDeDano);
/* usos por minuto de pé de cada habilidade do elenco */
const usoPorMinuto = (m: Medida, i: number) => (m.usos[i] ?? 0) / Math.max(5, m.tempoDePe) * 60;
const usos = medidas.flatMap((m) => [0, 1, 2].map((i) => usoPorMinuto(m, i)));

const SUSTENTO = (e: Effect) => e.kind === 'heal' || e.kind === 'shield' || (e.kind === 'status' && ['regen', 'protected', 'barrier', 'evasion'].includes(e.status));
const temSustento = (c: Character) => [...c.skills.flatMap((s) => s.effects), ...c.trait.effects].some(SUSTENTO);
const danoDe = (s: Skill) => s.effects.reduce((t, e) => t + (e.kind === 'damage' ? e.value * (s.target === 'allEnemies' || e.target === 'allEnemies' ? 2.2 : 1) : 0), 0);
const ALIADOS = ['allAllies', 'allyWeak', 'allyFallen'];
const apoia = (c: Character) => c.skills.filter((s) => s.effects.some((e) => (e.kind === 'heal' || e.kind === 'shield' || e.kind === 'charge' || e.kind === 'revive') && ALIADOS.includes(e.target ?? s.target))).length >= 2;

/* Quando a regra de uso segura a habilidade, dito curto. */
const QUANDO: Partial<Record<Skill['condition'], string>> = {
  injured: 'com o alvo ferido', enemyCast: 'com um rival em Preparo', threatened: 'com o trio em perigo',
  investigated: 'com um alvo investigado', vulnerable: 'com o rival vulnerável', storedEnergy: 'com energia guardada',
};

interface Candidata { nota: number; tipo: TipoDeFraqueza; rotulo: string; motivo: string; golpe?: string }

function candidatas(c: Character, m: Medida): Candidata[] {
  const out: Candidata[] = [];
  const pVida = posicao(vidas, c.hp), pIntervalo = posicao(intervalos, c.interval);
  const pDano = posicao(danos, ritmoDeDano(m));
  const forte = [...c.skills].sort((a, b) => danoDe(b) - danoDe(a))[0]!;

  /*
   * Cai rápido (pedido do jogador: "não coloca pouca Vida, coloca cai rápido ou é frágil… talvez o
   * personagem tenha mil de Vida mas tá caindo que nem um de 700, porque não tem nenhuma proteção").
   * Vale quem é o primeiro do trio a cair bem acima do normal (num trio, o normal é 1 em 6, uns 17%)
   * ou quem tem das menores Vidas do jogo; o porquê vem junto: a Vida baixa, a falta de cura e proteção.
   */
  const caiMuito = m.primeiroACair >= 0.25, semDefesa = !temSustento(c);
  const porQueda = caiMuito ? (m.primeiroACair - 0.25) * 12 + 0.6 : -9, porVida = pVida <= 0.2 ? (0.2 - pVida) * 8 + 0.4 : -9;
  const causas = [pVida <= 0.35 ? `só ${num(c.hp)} de Vida` : '', semDefesa ? 'sem cura nem proteção' : ''].filter(Boolean);
  out.push({ tipo: 'cai', rotulo: 'Cai rápido', nota: Math.max(porQueda, porVida) + (semDefesa ? 0.3 : 0),
    motivo: caiMuito ? `É o primeiro a cair em ${pct(m.primeiroACair)} das lutas${causas.length ? ` (${causas.join(', ')})` : ''}`
      : `Só ${num(c.hp)} de Vida, das menores do jogo${semDefesa ? ', e sem cura nem proteção' : ''}` });
  // A habilidade que quase não sai
  c.skills.forEach((s, i) => {
    const p = posicao(usos, usoPorMinuto(m, i)), porLuta = m.usos[i] ?? 0;
    const quando = s.condition !== 'always' ? QUANDO[s.condition] : undefined;
    const cortada = s.preparation >= 2 && m.cortados >= 0.15;
    const porque = quando ? `só ${quando}` : cortada ? `é cortada no Preparo (${num(s.preparation, 1)} s)` : 'a Carga demora a encher';
    const vezes = porLuta < 0.95 ? 'menos de 1 vez por luta' : `só ${num(porLuta, 1)} vezes por luta`;
    // um golpe que não sai pesa mais que uma defesa que espera o perigo (essa é feita para sair pouco)
    out.push({ tipo: 'rara', rotulo: 'Habilidade rara', nota: (0.15 - p) * 10 + (s === forte ? 0.6 : 0) + (danoDe(s) > 0 ? 0.6 : 0) - (s.condition === 'threatened' ? 0.5 : 0), motivo: `${s.name} sai ${vezes} (${porque})`, golpe: s.name });
  });
  // O golpe que mais demora e é cortado
  const longo = [...c.skills].sort((a, b) => b.preparation - a.preparation)[0]!;
  if (longo.preparation >= 3 || (longo.preparation >= 2.4 && m.cortados >= 0.1)) out.push({ tipo: 'preparo', rotulo: 'Preparo longo', golpe: longo.name, nota: (longo.preparation - 2.4) * 0.5 + (posicao(cortes, m.cortados) - 0.7) * 5 + 0.3,
    motivo: `${longo.name} leva ${num(longo.preparation, 1)} s para sair${m.cortados >= 0.1 ? ` e é cortada em ${pct(m.cortados)} das vezes` : ''}` });
  // Ataque lento
  out.push({ tipo: 'lento', rotulo: 'Ataque lento', nota: (pIntervalo - 0.8) * 7 + 0.4, motivo: `Ataca só a cada ${num(c.interval, 2)} s` });
  // Pouco dano por minuto de pé (quem cuida do trio não precisa bater forte: vale menos)
  out.push({ tipo: 'dano', rotulo: 'Pouco dano', nota: (0.15 - pDano) * 8 + (apoia(c) ? -0.6 : 0.3),
    motivo: apoia(c) ? 'Bate pouco; o forte dele é cuidar do trio' : 'Bate pouco e precisa do trio para derrubar alguém' });
  // Só cresce apanhando
  const cresceApanhando = c.trait.on === 'received' && c.trait.effects.some((e) => e.kind === 'status' && ['strengthened', 'haste'].includes(e.status));
  if (cresceApanhando) out.push({ tipo: 'apanhar', rotulo: 'Precisa apanhar', nota: 0.9 + (pVida <= 0.4 ? 0.4 : 0), motivo: `${c.trait.name} só o fortalece quando ele recebe dano` });
  return out;
}

const escolhidas: Record<string, Candidata[]> = {};
const resumo: Record<string, number> = {};
for (const c of characters) {
  const m = porId.get(c.id);
  if (!m) throw new Error(`sem medida para ${c.id}: rode scripts/medir-fraquezas.ts`);
  const lista = candidatas(c, m).sort((a, b) => b.nota - a.nota);
  const unicas = lista.filter((x, i) => lista.findIndex((y) => y.tipo === x.tipo) === i);
  // o segundo não repete o golpe do primeiro (o Discurso que demora e que quase não sai é uma coisa só)
  const [primeira] = unicas;
  const segunda = unicas.slice(1).find((x) => !x.golpe || x.golpe !== primeira!.golpe);
  const fica = [primeira!, ...(segunda && segunda.nota >= 0.9 ? [segunda] : [])];
  escolhidas[c.id] = fica;
  for (const x of fica) resumo[x.tipo] = (resumo[x.tipo] ?? 0) + 1;
}

const minuscula = (t: string) => (/^(É|Só|Ataca|Bate|Não) /.test(t) ? t.charAt(0).toLowerCase() + t.slice(1) : t);
const frase = (l: Candidata[]) => l.map((x) => `${x.rotulo}: ${minuscula(x.motivo)}.`).join(' ');
const linhas = Object.entries(escolhidas).map(([id, l]) => `  ${JSON.stringify(id)}: ${JSON.stringify(l.map(({ tipo, rotulo, motivo }) => ({ tipo, rotulo, motivo })))},`).join('\n');
const textos = Object.entries(escolhidas).map(([id, l]) => `  ${JSON.stringify(id)}: ${JSON.stringify(frase(l))},`).join('\n');
writeFileSync('src/data/fraquezas.ts', `/*
 * Ponto fraco de cada personagem: o que ele mesmo não consegue fazer (pouca
 * Vida, cai rápido, habilidade que quase não sai, Preparo longo…). Gerado por
 * scripts/escrever-fraquezas.ts a partir da ficha e de ${num(dados.lutas)} lutas simuladas
 * (docs/fraquezas-medidas.json). Não editar à mão: rode os scripts de novo
 * depois de mudar o elenco.
 */
import type { TipoDeFraqueza } from './ponto-fraco';

export interface PontoFracoMedido { tipo: TipoDeFraqueza; rotulo: string; motivo: string }

export const pontosFracos: Record<string, PontoFracoMedido[]> = {
${linhas}
};

/** O mesmo, em uma frase (o texto do personagem). */
export const fraquezas: Record<string, string> = {
${textos}
};
`);
console.log('escolhas por tipo:', resumo);
for (const id of ['eren', 'goku', 'korra', 'light', 'saitama', 'pikachu', 'batman', 'hulk', 'mojojojo', 'shiryu']) console.log(`${id}: ${frase(escolhidas[id] ?? [])}`);
