/*
 * O ponto forte e o ponto fraco de cada personagem — medidos, variados e com o porquê.
 *
 * Pedidos do jogador:
 * - "ponto fraco tem a ver com as habilidades dele que ele não tá conseguindo
 *   fazer, ou se ele tem pouca vida e morre rápido" (nunca "contra Espinhos":
 *   o que pesa em todo mundo não é ponto fraco);
 * - "quase todos os personagens é cai rápido ou habilidade rara… tem que fazer
 *   outra forma de medir, especificar melhor";
 * - na dica: "você fala por que que é fraco, mas não fala por que que é forte".
 *
 * Então cada personagem é comparado com o elenco inteiro em muitas medidas
 * (docs/fraquezas-medidas.json, scripts/medir-fraquezas.ts): o que ele faz
 * muito mais que os outros vira ponto forte, e o que ele faz muito menos (ou
 * sofre muito mais) vira ponto fraco — sempre com a habilidade que explica.
 *
 * Para nenhum tipo engolir o elenco, a escolha é feita para todos de uma vez:
 * os casos mais extremos de cada tipo entram primeiro, e cada tipo tem um teto
 * (TETO) — quem passaria do teto fica com o seu segundo traço mais marcante,
 * que também é verdade medida, só um pouco menos extremo.
 *
 * Uso: LUTAS=20000 npx tsx scripts/medir-fraquezas.ts && npx tsx scripts/escrever-fraquezas.ts
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import type { Character, Effect, Skill, StatusId } from '../src/engine/types';
import type { TipoDeFraqueza } from '../src/data/ponto-fraco';
import type { TipoDeForca } from '../src/data/ponto-forte';

interface Medida {
  id: string; lutas: number; primeiroACair: number; cortados: number; quedaPorGolpeGrande: number;
  usos: [number, number, number]; danoCausado: number; tempoDePe: number; duracaoMedia: number;
  feitos: { kills: number; healing: number; protection: number; skills: number; interrupts: number; debuffs: number; buffs: number; tempo: number; carga: number; revives: number };
  danoPorAcao: number[]; curaPorAcao: number[]; escudoPorAcao: number[]; statusPorAcao: Record<string, number>[];
  primeiraHabilidade: number | null; semHabilidade: number;
}
const dados = JSON.parse(readFileSync('docs/fraquezas-medidas.json', 'utf8')) as { lutas: number; medidas: Medida[] };
const porId = new Map(dados.medidas.map((m) => [m.id, m]));
const medidas = characters.map((c) => porId.get(c.id)).filter((m): m is Medida => !!m);
if (medidas.length !== characters.length || !medidas[0]!.feitos) throw new Error('rode scripts/medir-fraquezas.ts de novo (faltam medidas)');

const num = (v: number, casas = 0) => v.toLocaleString('pt-BR', { maximumFractionDigits: casas, minimumFractionDigits: 0 });
const redondo = (v: number) => num(v >= 1000 ? Math.round(v / 50) * 50 : Math.round(v / 10) * 10);
const pct = (v: number) => `${Math.round(v * 100)}%`;
/* "0,5 por luta" não se lê bem: vira "1 a cada 2 lutas" */
const porLuta = (v: number, um: string, varios: string) => (v >= 0.95 ? `${num(v, 1)} ${v >= 1.5 ? varios : um} por luta` : `1 ${um} a cada ${num(1 / Math.max(0.05, v), 0)} lutas`);
/* Posição no elenco, de 0 (o menor) a 1 (o maior). */
const posicao = (valores: number[], v: number) => valores.filter((x) => x < v).length / Math.max(1, valores.length - 1);
const coluna = (f: (m: Medida) => number) => characters.map((c) => f(porId.get(c.id)!));

/* ------------------------------------------------------------------ as medidas comparadas */
const minutos = (m: Medida) => Math.max(5, m.tempoDePe) / 60;
const M = {
  danoPorMinuto: (m: Medida) => m.danoCausado / minutos(m),
  nocautes: (m: Medida) => m.feitos.kills,
  cura: (m: Medida) => m.feitos.healing,
  escudo: (m: Medida) => m.feitos.protection,
  controle: (m: Medida) => m.feitos.debuffs,
  ritmo: (m: Medida) => m.feitos.tempo,
  carga: (m: Medida) => m.feitos.carga,
  cortes: (m: Medida) => m.feitos.interrupts,
  reforco: (m: Medida) => m.feitos.buffs,
  habilidades: (m: Medida) => m.feitos.skills / minutos(m),
  dePe: (m: Medida) => m.tempoDePe / Math.max(1, m.duracaoMedia),
  primeira: (m: Medida) => m.primeiraHabilidade ?? 99,
  golpeGrande: (m: Medida) => m.quedaPorGolpeGrande,
  /* nocautes por mil de dano: quem bate muito e derruba pouco espalha o dano */
  finaliza: (m: Medida) => m.feitos.kills / Math.max(1, m.danoCausado / 1000),
};
const C = Object.fromEntries(Object.entries(M).map(([k, f]) => [k, coluna(f)])) as Record<keyof typeof M, number[]>;
const vidas = characters.map((c) => c.hp), intervalos = characters.map((c) => c.interval);
const VIDA_ALTA = [...vidas].sort((a, b) => a - b)[Math.floor(vidas.length * 0.7)]!;
const p = (k: keyof typeof M, m: Medida) => posicao(C[k], M[k](m));

/* ------------------------------------------------------------------ as ações de cada um */
/*
 * O 5º "lugar" (índice 4) é o que não sai junto com uma ação: o traço e o que continua depois. Se o traço
 * faz aquilo (cura, bate, põe Status), é ele; senão é o Status que fica (Regeneração, Queimadura…).
 */
const CONTINUA: Record<string, string> = { regen: 'a Regeneração que fica no aliado', burning: 'a Queimadura que fica no rival', poison: 'o Veneno que fica no rival', bleed: 'o Sangramento que fica no rival' };
type Tipo = 'dano' | 'cura' | 'escudo' | 'status';
const traçoFaz = (c: Character, tipo: Tipo) => c.trait.effects.some((e) =>
  tipo === 'dano' ? e.kind === 'damage' || (e.kind === 'status' && ['burning', 'poison', 'bleed'].includes(e.status))
    : tipo === 'cura' ? e.kind === 'heal' || (e.kind === 'status' && e.status === 'regen') : tipo === 'escudo' ? e.kind === 'shield' : e.kind === 'status');
const continuaDe = (c: Character, tipo: Tipo) => {
  const ids = c.skills.flatMap((s) => s.effects).filter((e) => e.kind === 'status').map((e) => (e as { status: string }).status);
  const achado = (tipo === 'cura' ? ['regen'] : tipo === 'dano' ? ['burning', 'poison', 'bleed'] : []).find((id) => ids.includes(id));
  return achado ? CONTINUA[achado]! : 'o que fica no alvo';
};
const nomeDaAcao = (c: Character, i: number, tipo: Tipo = 'dano') => {
  if (i === 0) return c.basic.name;
  if (i <= 3) return c.skills[i - 1]!.name;
  return traçoFaz(c, tipo) ? `o traço ${c.trait.name}` : continuaDe(c, tipo);
};
/* o começo da frase em maiúscula ("o traço X devolve…" → "O traço X devolve…") */
const maiuscula = (t: string) => t.charAt(0).toUpperCase() + t.slice(1);
/* o golpe que a ficha destaca: só ações de verdade (o básico ou uma habilidade) */
const golpeDe = (c: Character, i: number) => (i <= 3 ? nomeDaAcao(c, i) : undefined);
const maiorAcao = (lista: number[]) => lista.reduce((best, v, i) => (v > lista[best]! ? i : best), 0);
const nomeDoStatus = (s: string) => statuses[s as StatusId]?.name ?? s;
const ALIADOS = ['allAllies', 'allyWeak', 'allyFallen'];
const SUSTENTO = (e: Effect) => e.kind === 'heal' || e.kind === 'shield' || (e.kind === 'status' && ['regen', 'protected', 'barrier', 'evasion'].includes(e.status));
const temSustento = (c: Character) => [...c.skills.flatMap((s) => s.effects), ...c.trait.effects].some(SUSTENTO);
const danoDe = (s: Skill) => s.effects.reduce((t, e) => t + (e.kind === 'damage' ? e.value * (s.target === 'allEnemies' || e.target === 'allEnemies' ? 2.2 : 1) : 0), 0);
const apoia = (c: Character) => c.skills.filter((s) => s.effects.some((e) => (e.kind === 'heal' || e.kind === 'shield' || e.kind === 'charge' || e.kind === 'revive') && ALIADOS.includes(e.target ?? s.target))).length >= 2;
const QUANDO: Partial<Record<Skill['condition'], string>> = {
  injured: 'com o alvo ferido', enemyCast: 'com um rival em Preparo', threatened: 'com o trio em perigo',
  investigated: 'com um alvo investigado', vulnerable: 'com o rival vulnerável', storedEnergy: 'com energia guardada',
};
const usoPorMinuto = (m: Medida, i: number) => (m.usos[i] ?? 0) / minutos(m);
const usos = medidas.flatMap((m) => [0, 1, 2].map((i) => usoPorMinuto(m, i)));

interface Candidata { nota: number; tipo: string; rotulo: string; motivo: string; golpe?: string }

/* ------------------------------------------------------------------ pontos fortes */
function fortes(c: Character, m: Medida): Candidata[] {
  const out: Candidata[] = [];
  const acaoDano = maiorAcao(m.danoPorAcao), acaoCura = maiorAcao(m.curaPorAcao), acaoEscudo = maiorAcao(m.escudoPorAcao);
  const totalStatus = m.statusPorAcao.map((o) => Object.values(o).reduce((t, v) => t + v, 0));
  const acaoStatus = maiorAcao(totalStatus);
  const statusDe = (i: number) => Object.entries(m.statusPorAcao[i] ?? {}).sort((a, b) => b[1] - a[1]).slice(0, 2).map(([s]) => nomeDoStatus(s));
  const forte = (tipo: TipoDeForca, rotulo: string, posi: number, motivo: string, extra = 0, golpe?: string) =>
    out.push({ tipo, rotulo, nota: (posi - 0.8) * 6 + extra, motivo, ...(golpe ? { golpe } : {}) });

  forte('dano', 'Bate muito forte', p('danoPorMinuto', m), maiuscula(`${nomeDaAcao(c, acaoDano, 'dano')} tira uns ${redondo(m.danoPorAcao[acaoDano]!)} de Vida por luta`), 0, golpeDe(c, acaoDano));
  if (m.feitos.kills > 0) forte('nocaute', 'Finalizador', p('nocautes', m), `Derruba ${porLuta(m.feitos.kills, 'rival', 'rivais')}, mais que quase todo o elenco`, m.feitos.kills >= 0.9 ? 0 : -0.3);
  if (m.feitos.healing > 0) forte('cura', 'Cura forte', p('cura', m), maiuscula(`${nomeDaAcao(c, acaoCura, 'cura')} devolve uns ${redondo(m.feitos.healing)} de Vida por luta`), 0.15, golpeDe(c, acaoCura));
  if (m.feitos.protection > 0) forte('escudo', 'Escudo forte', p('escudo', m), maiuscula(`${nomeDaAcao(c, acaoEscudo, 'escudo')} segura uns ${redondo(m.feitos.protection)} de dano por luta com Escudo`), 0.1, golpeDe(c, acaoEscudo));
  if (m.feitos.debuffs > 0 && totalStatus[acaoStatus]! > 0) {
    const st = statusDe(acaoStatus);
    forte('controle', 'Atrapalha os rivais', p('controle', m), maiuscula(`${nomeDaAcao(c, acaoStatus, 'status')} deixa os rivais ${st.join(' e ')}`), 0, golpeDe(c, acaoStatus));
  }
  if (m.feitos.tempo > 0) forte('ritmo', 'Dita o ritmo', p('ritmo', m), 'Adianta a vez do trio e atrasa a dos rivais', 0.05);
  if (m.feitos.carga > 0) forte('carga', 'Enche a Carga do trio', p('carga', m), 'As habilidades dos aliados saem antes quando está no trio');
  if (m.feitos.interrupts > 0) forte('corte', 'Corta Preparos', p('cortes', m), `Corta ${porLuta(m.feitos.interrupts, 'golpe em Preparo', 'golpes em Preparo')}`, m.feitos.interrupts >= 0.9 ? 0.1 : -1);
  if (m.feitos.buffs > 0) forte('reforco', 'Sempre reforçado', p('reforco', m), 'Mantém Status bons em si e no trio quase a luta toda');
  if (m.feitos.revives > 0.05) forte('reviver', 'Levanta aliados', 0.8 + Math.min(0.2, m.feitos.revives), `Põe de pé ${porLuta(m.feitos.revives, 'aliado caído', 'aliados caídos')}`, 0.6);
  const porque = [c.hp >= VIDA_ALTA ? `${num(c.hp)} de Vida` : '', temSustento(c) ? 'se cura ou se protege' : ''].filter(Boolean);
  forte('aguenta', 'Difícil de derrubar', p('dePe', m), `Fica de pé ${pct(Math.min(1, M.dePe(m)))} da luta${porque.length ? ` (${porque.join(', ')})` : ''}`);
  forte('agil', 'Habilidades sem parar', p('habilidades', m), `Solta ${num(m.feitos.skills, 1)} habilidades por luta`);
  if (m.primeiraHabilidade !== null) forte('cedo', 'Começa rápido', 1 - p('primeira', m), `A primeira habilidade já sai aos ${num(m.primeiraHabilidade, 0)} s de luta`, -0.1);
  forte('rapido', 'Ataque rápido', 1 - posicao(intervalos, c.interval), `${c.basic.name} sai a cada ${num(c.interval, 2)} s`, -0.15, c.basic.name);
  /*
   * Quem não se destaca muito em nada (nenhuma medida entre as maiores do elenco) ganha o retrato do
   * que ele faz melhor, em duas partes: "faz um pouco de tudo: bate bem e corta Preparos".
   */
  const FAZ: Record<string, string> = { dano: 'bate bem', nocaute: 'derruba rivais', cura: 'cura', escudo: 'dá Escudo', controle: 'atrapalha os rivais',
    ritmo: 'mexe no ritmo', carga: 'enche a Carga do trio', corte: 'corta Preparos', reforco: 'se reforça', aguenta: 'aguenta bem', agil: 'usa muitas habilidades',
    cedo: 'começa rápido', rapido: 'ataca rápido', reviver: 'levanta aliados' };
  const melhores = [...out].sort((a, b) => b.nota - a.nota).slice(0, 2).map((x) => FAZ[x.tipo]).filter(Boolean);
  if (melhores.length === 2) out.push({ tipo: 'equilibrado', rotulo: 'Faz de tudo', nota: -0.05, motivo: `Nenhum número sozinho se destaca, mas ${melhores[0]} e ${melhores[1]}` });
  return out;
}

/* ------------------------------------------------------------------ pontos fracos */
function fracos(c: Character, m: Medida): Candidata[] {
  const out: Candidata[] = [];
  const pVida = posicao(vidas, c.hp), pIntervalo = posicao(intervalos, c.interval);
  const golpeForte = [...c.skills].sort((a, b) => danoDe(b) - danoDe(a))[0]!;
  const fraco = (tipo: TipoDeFraqueza, rotulo: string, nota: number, motivo: string, golpe?: string) => out.push({ tipo, rotulo, nota, motivo, ...(golpe ? { golpe } : {}) });

  // Cai rápido: o primeiro do trio a cair bem acima do normal (num trio, o normal é ~17%)
  const causas = [pVida <= 0.35 ? `só ${num(c.hp)} de Vida` : '', !temSustento(c) ? 'sem cura nem proteção' : ''].filter(Boolean);
  fraco('cai', 'Cai rápido', (m.primeiroACair - 0.24) * 12 + 0.5, `É o primeiro a cair em ${pct(m.primeiroACair)} das lutas${causas.length ? ` (${causas.join(', ')})` : ''}`);
  // Cai de um golpe: boa parte das quedas vem de um golpe grande só
  if (m.quedaPorGolpeGrande >= 0.25) fraco('golpe', 'Cai de um golpe', (p('golpeGrande', m) - 0.85) * 7 + 0.4,
    `${pct(m.quedaPorGolpeGrande)} das vezes que cai, cai de um golpe grande só${pVida <= 0.35 ? ` (só ${num(c.hp)} de Vida)` : ''}`);
  // A habilidade que quase não sai: a Carga que demora, a regra de uso ou o Preparo cortado
  c.skills.forEach((s, i) => {
    const pos = posicao(usos, usoPorMinuto(m, i)), porLuta = m.usos[i] ?? 0;
    const vezes = porLuta < 0.95 ? 'menos de 1 vez por luta' : `só ${num(porLuta, 1)} vezes por luta`;
    const peso = (s === golpeForte ? 0.4 : 0) + (danoDe(s) > 0 ? 0.4 : 0);
    const quando = s.condition !== 'always' ? QUANDO[s.condition] : undefined;
    // uma defesa que espera o perigo é feita para sair pouco: não é ponto fraco
    if (quando) { if (s.condition !== 'threatened') fraco('espera', 'Espera a hora certa', (0.12 - pos) * 10 + peso, `${s.name} só sai ${quando}: ${vezes}`, s.name); }
    else if (s.preparation >= 2 && m.cortados >= 0.12) fraco('preparo', 'Preparo cortado', (0.15 - pos) * 8 + (m.cortados - 0.12) * 6 + peso, `${s.name} leva ${num(s.preparation, 1)} s e é cortada em ${pct(m.cortados)} das vezes`, s.name);
    else fraco('rara', 'Habilidade rara', (0.1 - pos) * 10 + peso, `${s.name} sai ${vezes} (a Carga demora a encher)`, s.name);
  });
  // Demora a agir: a primeira habilidade sai tarde, ou nem sai
  if (m.primeiraHabilidade !== null) fraco('demora', 'Demora a agir', (p('primeira', m) - 0.85) * 7 + m.semHabilidade * 2,
    m.semHabilidade >= 0.25 ? `Em ${pct(m.semHabilidade)} das lutas não usa nenhuma habilidade` : `A primeira habilidade só sai aos ${num(m.primeiraHabilidade, 0)} s de luta`);
  // Ataque lento
  fraco('lento', 'Ataque lento', (pIntervalo - 0.85) * 7 + 0.3, `${c.basic.name} sai só a cada ${num(c.interval, 2)} s`, c.basic.name);
  // Pouco dano (quem cuida do trio não precisa bater forte: vale menos)
  fraco('dano', 'Pouco dano', (0.12 - p('danoPorMinuto', m)) * 8 + (apoia(c) ? -0.6 : 0.3),
    apoia(c) ? 'Bate pouco; o forte é cuidar do trio' : 'Bate pouco e precisa do trio para derrubar alguém');
  // Não finaliza: bate bastante, mas o dano se espalha e quase não derruba ninguém
  if (p('danoPorMinuto', m) >= 0.4) fraco('espalha', 'Não finaliza', (0.12 - p('finaliza', m)) * 8 + 0.2, 'Bate bastante, mas espalha o dano e quase não derruba ninguém');
  // Só cresce apanhando
  const cresceApanhando = c.trait.on === 'received' && c.trait.effects.some((e) => e.kind === 'status' && ['strengthened', 'haste'].includes(e.status));
  if (cresceApanhando) fraco('apanhar', 'Precisa apanhar', 0.7 + (pVida <= 0.4 ? 0.3 : 0), `${c.trait.name} só fortalece quando recebe dano`);
  return out;
}

/* ------------------------------------------------------------------ a escolha, para todos de uma vez */
const TETO = Math.ceil(characters.length * 0.17);
function escolher(listas: Map<string, Candidata[]>, segundaMinima: number) {
  const uso = new Map<string, number>(), primeira = new Map<string, Candidata>();
  const todas = [...listas].flatMap(([id, l]) => l.map((x) => ({ id, x }))).sort((a, b) => b.x.nota - a.x.nota);
  for (const { id, x } of todas) {
    if (primeira.has(id) || (uso.get(x.tipo) ?? 0) >= TETO) continue;
    primeira.set(id, x); uso.set(x.tipo, (uso.get(x.tipo) ?? 0) + 1);
  }
  const fim: Record<string, Candidata[]> = {};
  for (const [id, l] of listas) {
    const ordem = [...l].sort((u, v) => v.nota - u.nota);
    const a = primeira.get(id) ?? ordem[0]!;
    // a segunda só quando é tão marcante quanto, de outro tipo e de outra habilidade
    const b = ordem.find((x) => x.tipo !== a.tipo && (!x.golpe || x.golpe !== a.golpe) && x.nota >= segundaMinima && (uso.get(x.tipo) ?? 0) < TETO);
    if (b) uso.set(b.tipo, (uso.get(b.tipo) ?? 0) + 1);
    fim[id] = b ? [a, b] : [a];
  }
  return { fim, uso };
}

const F = escolher(new Map(characters.map((c) => [c.id, fracos(c, porId.get(c.id)!)])), 1.0);
const S = escolher(new Map(characters.map((c) => [c.id, fortes(c, porId.get(c.id)!)])), 0.9);

const minuscula = (t: string) => (/^(É|Só|Bate|Em|A|O|Fica|Derruba|Corta|Põe|Solta|Adianta|As|Mantém|Segura|Nenhum) /.test(t) ? t.charAt(0).toLowerCase() + t.slice(1) : t);
const frase = (l: Candidata[]) => l.map((x) => `${x.rotulo}: ${minuscula(x.motivo)}.`).join(' ');
const json = (l: Candidata[]) => JSON.stringify(l.map(({ tipo, rotulo, motivo }) => ({ tipo, rotulo, motivo })));
writeFileSync('src/data/fraquezas.ts', `/*
 * Ponto fraco e ponto forte de cada personagem, medidos: comparado com o
 * elenco inteiro, o que ele faz muito pior (fraco) e muito melhor (forte), com
 * a habilidade que explica. Gerado por scripts/escrever-fraquezas.ts a partir
 * da ficha e de ${num(dados.lutas)} lutas simuladas (docs/fraquezas-medidas.json).
 * Não editar à mão: rode os scripts de novo depois de mudar o elenco.
 */
import type { TipoDeFraqueza } from './ponto-fraco';
import type { TipoDeForca } from './ponto-forte';

export interface PontoFracoMedido { tipo: TipoDeFraqueza; rotulo: string; motivo: string }
export interface PontoForteMedido { tipo: TipoDeForca; rotulo: string; motivo: string }

export const pontosFracos: Record<string, PontoFracoMedido[]> = {
${characters.map((c) => `  ${JSON.stringify(c.id)}: ${json(F.fim[c.id]!)},`).join('\n')}
};

/** O ponto fraco em uma frase (o texto do personagem). */
export const fraquezas: Record<string, string> = {
${characters.map((c) => `  ${JSON.stringify(c.id)}: ${JSON.stringify(frase(F.fim[c.id]!))},`).join('\n')}
};

export const pontosFortes: Record<string, PontoForteMedido[]> = {
${characters.map((c) => `  ${JSON.stringify(c.id)}: ${json(S.fim[c.id]!)},`).join('\n')}
};
`);
console.log('fracos por tipo:', Object.fromEntries(F.uso), 'teto', TETO);
console.log('fortes por tipo:', Object.fromEntries(S.uso));
for (const id of ['goku', 'liono', 'lexluthor', 'piccolo', 'korra', 'light', 'saitama', 'pikachu', 'batman', 'hulk', 'mojojojo']) console.log(`${id}\n  + ${frase(S.fim[id] ?? [])}\n  - ${frase(F.fim[id] ?? [])}`);
