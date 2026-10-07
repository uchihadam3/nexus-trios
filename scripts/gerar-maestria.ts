/*
 * FASE H · gera os 750 desafios de Maestria.
 *
 * O documento pede três por personagem, em três degraus, com **pelo menos 2
 * dos 3 ligados à mecânica real** — e proíbe por escrito o padrão "jogue 50
 * partidas".
 *
 * As metas não são escolhidas a dedo: saem das 10.000 lutas que a FASE F já
 * mediu (docs/identidades-medidas.json). Um personagem que cura 500 por luta
 * recebe uma meta de cura proporcional a isso; um que nunca curou não recebe
 * desafio de cura nenhum. É a mesma guarda que o documento exige dos
 * Objetivos — "nunca gerar impossível" — aplicada aqui pelo mesmo motivo.
 *
 * Saída: src/data/maestria.ts, revisável em diff.
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import { podeCumprir, type Desafio, type Feito } from '../src/engine/maestria';
import type { Character } from '../src/engine/types';

/* ---------------------------------------------------------------------------
 * As metas, dimensionadas pelo que o personagem de fato entrega
 * ------------------------------------------------------------------------- */

interface Medida { id: string; [k: string]: number | string }
let medidas: Map<string, Medida> | null = null;
/** Lê as 10.000 lutas da FASE F. Só o script de geração usa isto. */
const carregarMedidas = (): Map<string, Medida> => {
  medidas ??= new Map((JSON.parse(readFileSync('docs/identidades-medidas.json', 'utf8')) as { medidas: Medida[] })
    .medidas.map((m) => [m.id, m]));
  return medidas;
};

/* De onde vem a medida de cada feito, e como ela vira meta. */
const BASE: Record<Feito, { campo: string; porLuta: number; minimo: number; texto: (n: number) => string }> = {
  'usou': { campo: '', porLuta: 1, minimo: 1, texto: () => 'Leve-o para uma batalha e veja o traço dele agir' },
  'curou': { campo: 'cura', porLuta: 1.5, minimo: 300, texto: (n) => `Devolva ${n} de Vida ao trio` },
  'protegeu': { campo: 'protecao', porLuta: 1.5, minimo: 300, texto: (n) => `Absorva ${n} de dano com Escudo` },
  'interrompeu': { campo: 'interrupcoes', porLuta: 3, minimo: 3, texto: (n) => `Corte ${n} Preparos inimigos` },
  'controlou': { campo: 'controleSegundos', porLuta: 2.5, minimo: 10, texto: (n) => `Mantenha inimigos travados por ${n} segundos no total` },
  'area': { campo: 'danoEmArea', porLuta: 2, minimo: 400, texto: (n) => `Cause ${n} de dano acertando vários inimigos de uma vez` },
  'continuo': { campo: 'continuoSegundos', porLuta: 2.5, minimo: 15, texto: (n) => `Deixe inimigos queimando ou eletrificados por ${n} segundos` },
  'abateu': { campo: 'abates', porLuta: 4, minimo: 3, texto: (n) => `Derrube ${n} inimigos` },
  'aguentou': { campo: 'danoRecebido', porLuta: 2, minimo: 1500, texto: (n) => `Absorva ${n} de dano sem o trio cair` },
  'sobreviveu': { campo: 'sobrevive', porLuta: 4, minimo: 3, texto: (n) => `Termine ${n} batalhas de pé` },
  'acumulou': { campo: 'reforcoEmSi', porLuta: 2, minimo: 30, texto: (n) => `Mantenha o próprio reforço ativo por ${n} segundos no total` },
  'explodiu': { campo: 'maiorGolpe', porLuta: 1, minimo: 200, texto: (n) => `Acerte um único golpe de ${n} de dano` },
  'carregou': { campo: 'cargaDada', porLuta: 2, minimo: 150, texto: (n) => `Encha ${n}% de Carga dos seus aliados` },
  'virou': { campo: '', porLuta: 1, minimo: 1, texto: (n) => `Vença ${n} batalha em que o trio esteve atrás na Vantagem` },
};

const arredondar = (n: number) => n >= 1000 ? Math.round(n / 100) * 100 : n >= 100 ? Math.round(n / 10) * 10 : Math.max(1, Math.round(n));

/** A meta de um feito para um personagem: o que ele faz por luta, vezes um fator. */
const metaPara = (c: Character, feito: Feito, grau: 'II' | 'III'): number => {
  const base = BASE[feito];
  const fator = grau === 'III' ? 2.6 : 1;
  if (!base.campo) return Math.max(1, Math.round(fator));
  const m = carregarMedidas().get(c.id);
  const porLuta = m ? Number(m[base.campo] ?? 0) : 0;
  const alvo = porLuta > 0 ? porLuta * base.porLuta * fator : base.minimo * fator;
  return arredondar(Math.max(base.minimo * fator * 0.6, alvo));
};

/*
 * A ordem em que os feitos são oferecidos.
 *
 * Os primeiros descrevem melhor um personagem que os últimos: curar e travar
 * Preparos dizem mais do que "derrubou inimigos", que todo mundo faz. Cada um
 * recebe os dois primeiros da lista que o kit dele alcança.
 */
const PREFERENCIA: readonly Feito[] = [
  'curou', 'interrompeu', 'controlou', 'carregou', 'protegeu',
  'area', 'continuo', 'acumulou', 'explodiu', 'aguentou', 'abateu', 'sobreviveu',
];

/** Os três desafios de um personagem, em ordem de degrau. */
const gerarDesafios = (c: Character): [Desafio, Desafio, Desafio] => {
  const possiveis = PREFERENCIA.filter((f) => podeCumprir(c, f));
  const [segundo, terceiro] = [possiveis[0] ?? 'abateu', possiveis[1] ?? 'sobreviveu'];
  return [
    { grau: 'I', titulo: BASE.usou.texto(1), feito: 'usou', meta: 1, mecanico: false },
    { grau: 'II', titulo: BASE[segundo].texto(metaPara(c, segundo, 'II')), feito: segundo, meta: metaPara(c, segundo, 'II'), mecanico: true },
    { grau: 'III', titulo: BASE[terceiro].texto(metaPara(c, terceiro, 'III')), feito: terceiro, meta: metaPara(c, terceiro, 'III'), mecanico: true },
  ];
};


const linhas = characters.map((c) => {
  const tres = gerarDesafios(c);
  const corpo = tres.map((d) => `{grau:'${d.grau}',titulo:${JSON.stringify(d.titulo)},feito:'${d.feito}',meta:${String(d.meta)},mecanico:${String(d.mecanico)}}`).join(',');
  return `  ${/^[a-z][a-z0-9]*$/.test(c.id) ? c.id : `'${c.id}'`}:[${corpo}],`;
}).join('\n');

const CABECALHO = [
  '/*',
  ' * Gerado por scripts/gerar-maestria.ts a partir das 10.000 lutas da FASE F.',
  ' * Nao editar a mao: rode `npx tsx scripts/gerar-maestria.ts`.',
  ' *',
  ' * O porque de cada feito esta em src/engine/maestria.ts.',
  ' */',
  "import type { Desafio } from '../engine/maestria';",
  '',
  'export const desafiosPorPersonagem:Record<string,readonly [Desafio,Desafio,Desafio]> = {',
].join('\n');

writeFileSync('src/data/maestria.ts', `${CABECALHO}\n${linhas}\n};\n`);

/* Relatorio: a distribuicao dos feitos diz se o catalogo separa os personagens. */
const porFeito = new Map<Feito, number>();
let mecanicos = 0, total = 0;
for (const c of characters) {
  for (const d of gerarDesafios(c)) { total += 1; if (d.mecanico) mecanicos += 1; porFeito.set(d.feito, (porFeito.get(d.feito) ?? 0) + 1); }
}
console.log(`${String(characters.length)} personagens · ${String(total)} desafios · ${String(mecanicos)} mecanicos (${(mecanicos / total * 100).toFixed(0)}%)\n`);
for (const [f, n] of [...porFeito].sort((a, b) => b[1] - a[1])) {
  console.log(`  ${f.padEnd(13)}${String(n).padStart(4)}  ${'#'.repeat(Math.round(n / 8))}`);
}
const combos = new Set(characters.map((c) => gerarDesafios(c).slice(1).map((d) => d.feito).join('+')));
console.log(`\npares de feitos distintos: ${String(combos.size)}`);
console.log('\nexemplos:');
for (const id of ['sakura', 'saitama', 'storm', 'pikachu', 'thanos', 'gambit']) {
  const c = characters.find((x) => x.id === id); if (!c) continue;
  console.log(`\n  ${c.name}`);
  for (const d of gerarDesafios(c)) console.log(`    ${d.grau.padEnd(3)} ${d.titulo}`);
}
