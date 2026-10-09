/*
 * FASE F · transformar 10.000 lutas em 2 a 4 identidades por personagem.
 *
 * A regra da direção: **mecânica + simulação + override manual**, e duas
 * proibições explícitas — não dar "Cura" por cura incidental, não dar "Dano"
 * só porque ataque básico machuca.
 *
 * O método aqui é comparativo, e é isso que resolve as duas. Cada métrica vira
 * um **percentil dentro do elenco**: não importa se o personagem cura, importa
 * se ele cura mais que os outros 249. Como quase todo mundo causa dano, dano
 * sozinho não rende etiqueta nenhuma; rende "Pressão" quem causa muito **e**
 * de forma constante, e "Explosão" quem concentra num golpe.
 *
 * Alguns termos não têm medida boa e são estruturais. "Carga" é o exemplo: o
 * motor emite evento de carga o tempo todo, então 75% do elenco "dá carga" —
 * usar isso repetiria o erro do "Dano". A evidência honesta é ter um efeito de
 * Carga mirando aliados na ficha, o que poucos têm.
 *
 * Saída: src/data/identidades.ts, revisável em diff.
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import type { Identidade } from '../src/presentation/identities';
import { ordemDasIdentidades } from '../src/presentation/identities';
import type { Character, Effect, StatusId, Target } from '../src/engine/types';

interface Medida { id: string; nome: string; [k: string]: number | string }
const { medidas } = JSON.parse(readFileSync('docs/identidades-medidas.json', 'utf8')) as { medidas: Medida[] };
const porId = new Map(medidas.map((m) => [m.id, m]));

/*
 * O percentil do personagem **dentro do elenco inteiro**, zeros incluídos.
 *
 * A primeira versão comparava só com quem tinha a mesma capacidade — a fila
 * dos curandeiros entre curandeiros — e isso quebrou justamente o caso raro:
 * treze personagens curam aliados, e exigir que estivessem entre os 28%
 * melhores **desses treze** deixava "Cura" com dois donos em 250.
 *
 * Mas curar aliado já é raro. Uma capacidade que 13 de 250 têm é um ótimo
 * distintivo por si só, e quem a tem merece a etiqueta. Comparando contra o
 * elenco inteiro, os treze ficam acima de 0,94 e passam todos, enquanto uma
 * capacidade comum — causar dano, aplicar debuff — só rende etiqueta para quem
 * de fato se destaca nela.
 *
 * Um valor zero continua devolvendo 0: não fazer nada nunca é identidade.
 */
const tabela = new Map<string, number[]>();
const percentil = (campo: string, valor: number): number => {
  if (valor <= 0) return 0;
  let ordenados = tabela.get(campo);
  if (!ordenados) {
    ordenados = medidas.map((m) => m[campo] as number).sort((a, b) => a - b);
    tabela.set(campo, ordenados);
  }
  let i = 0;
  while (i < ordenados.length && ordenados[i]! < valor) i += 1;
  return i / ordenados.length;
};

/* --------------------------------------------------------------------------
 * A parte mecânica: o que a ficha garante, independente de sorteio.
 * ------------------------------------------------------------------------ */

const ALIADOS = new Set<Target>(['self', 'allyWeak', 'allAllies']);
const todosEfeitos = (c: Character): { e: Effect; alvo: Target }[] => [
  ...c.trait.effects.map((e) => ({ e, alvo: e.target ?? c.trait.target })),
  ...c.basic.effects.map((e) => ({ e, alvo: e.target ?? c.basic.target })),
  ...c.skills.flatMap((s) => s.effects.map((e) => ({ e, alvo: e.target ?? s.target }))),
];

const temEfeito = (c: Character, f: (x: { e: Effect; alvo: Target }) => boolean) => todosEfeitos(c).some(f);

/** Habilidades que só saem numa situação específica. */
const condicionais = (c: Character) => c.skills.filter((s) => s.condition !== 'always').length;
/** Carga que vem de apanhar. */
const cargaPorApanhar = (c: Character) =>
  c.skills.reduce((t, s) => t + s.charge.filter((r) => r.on === 'received').reduce((n, r) => n + r.amount, 0), 0);

/* --------------------------------------------------------------------------
 * Cada identidade, com a evidência que a ganha.
 * ------------------------------------------------------------------------ */

const ALTO = 0.72; /* entre os ~28% melhores do elenco naquela métrica */

const avaliar = (c: Character): Map<Identidade, number> => {
  const m = porId.get(c.id);
  if (!m) throw new Error(`sem medição para ${c.id}`);
  const n = (campo: string) => m[campo] as number;
  const p = (campo: string) => percentil(campo, n(campo));
  const notas = new Map<Identidade, number>();
  const dar = (id: Identidade, valor: number) => { if (valor >= ALTO) notas.set(id, valor); };

  /* Ataque — nunca por existir dano, sempre pela forma dele. */
  const golpesAcimaDaMedia = p('golpes');
  dar('Pressão', Math.min(p('dano'), Math.max(golpesAcimaDaMedia, 0.5)) * (golpesAcimaDaMedia > 0.45 ? 1 : 0.6));
  dar('Explosão', p('maiorGolpe') * (n('maiorGolpe') / Math.max(1, n('dano')) > 0.3 ? 1 : 0.85));
  dar('Área', p('danoEmArea'));
  dar('Dano contínuo', p('continuoSegundos'));
  dar('Finalização', p('abates'));

  /* Atrapalhar o adversário. */
  dar('Controle', p('controleSegundos'));
  dar('Interrupção', p('interrupcoes'));
  dar('Ritmo', p('ritmoSegundos'));
  dar('Debuff', p('debuffsEmInimigo'));

  /* Ajudar o trio — e aqui mora a proibição da cura incidental. */
  const curaNosOutros = n('cura') - n('curaEmSi');
  dar('Cura', percentil('curaNosOutros', curaNosOutros));
  dar('Proteção', p('protecao'));
  dar('Buff', p('buffsEmAliado'));
  /*
   * "Carga" é estrutural: o motor emite evento de carga o tempo todo, então a
   * medição diria que 75% do elenco dá Carga. O que distingue é ter um efeito
   * de Carga mirando o trio.
   */
  const daCarga = temEfeito(c, ({ e, alvo }) => e.kind === 'charge' && ALIADOS.has(alvo));
  if (daCarga) notas.set('Carga', percentil('cargaDadaReal', n('cargaDada')));
  /* Suporte é o generalista: ajuda o trio por mais de um caminho. */
  const canais = [percentil('curaNosOutros', curaNosOutros), p('protecao'), p('buffsEmAliado'), daCarga ? 0.9 : 0]
    .filter((x) => x >= 0.6).length;
  if (canais >= 2) notas.set('Suporte', Math.min(0.95, 0.7 + canais * 0.07));

  /* Aguentar. */
  dar('Tanque', Math.min(p('danoRecebido'), p('segundosVivo')));
  dar('Sobrevivência', p('sobrevive'));
  dar('Regeneração', p('curaEmSi'));

  /* O jeito de jogar. */
  dar('Transformação', p('reforcoEmSi'));
  dar('Preparação', p('preparoMaximo'));
  dar('Virada', percentil('taxaDeVirada', n('vitorias') > 0 ? n('viradas') / n('vitorias') : 0));
  const apanhar = cargaPorApanhar(c);
  if (apanhar > 0) {
    const ps = percentil('cargaPorApanhar', apanhar);
    if (ps >= ALTO) notas.set('Contra-ataque', ps);
  }
  const cond = condicionais(c);
  if (cond >= 2) notas.set('Especialista', percentil('condicionais', cond));

  /* Mecânicas que poucos têm: a ficha garante, e a etiqueta vem antes de todas. */
  if (temEfeito(c, ({ e }) => e.kind === 'revive')) notas.set('Reviver', 1);
  if (c.renascer) notas.set('Renascer', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'status' && e.status === 'provoked')) notas.set('Provocar', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'lifesteal' || (e.kind === 'status' && e.status === 'vampirism'))) notas.set('Roubo de vida', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'status' && e.status === 'reflect')) notas.set('Refletir', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'status' && e.status === 'thorns')) notas.set('Espinhos', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'cleanse')) notas.set('Purificar', 1);
  if (temEfeito(c, ({ e }) => e.kind === 'dispel')) notas.set('Dissipar', 1);
  const TAG_DO_STATUS: [StatusId, Identidade][] = [['poison', 'Veneno'], ['bleed', 'Sangramento'], ['cursed', 'Maldição'], ['frozen', 'Congelar'], ['sleep', 'Sono'], ['blind', 'Cegueira'], ['barrier', 'Barreira']];
  for (const [s, tag] of TAG_DO_STATUS) if (temEfeito(c, ({ e }) => e.kind === 'status' && e.status === s)) notas.set(tag, 1);
  return notas;
};

/* A métrica derivada precisa estar na tabela antes de ser consultada. */
tabela.set('curaNosOutros', medidas.map((m) => (m.cura as number) - (m.curaEmSi as number)).sort((a, b) => a - b));
tabela.set('taxaDeVirada', medidas.map((m) => ((m.vitorias as number) > 0 ? (m.viradas as number) / (m.vitorias as number) : 0)).sort((a, b) => a - b));
tabela.set('cargaPorApanhar', characters.map(cargaPorApanhar).sort((a, b) => a - b));
tabela.set('condicionais', characters.map(condicionais).sort((a, b) => a - b));
/* Só entre quem realmente tem efeito de Carga: comparar com os outros 174 seria enganoso. */
const comCarga = new Set(characters.filter((c) => temEfeito(c, ({ e, alvo }) => e.kind === 'charge' && ALIADOS.has(alvo))).map((c) => c.id));
tabela.set('cargaDadaReal', medidas.filter((m) => comCarga.has(m.id)).map((m) => m.cargaDada as number).sort((a, b) => a - b));

/* --------------------------------------------------------------------------
 * Os overrides que a direção nomeou.
 * ------------------------------------------------------------------------ */

/*
 * Quatro personagens vieram com identidade escrita no documento. Onde a
 * medição concorda, não há override; onde discorda, o documento vence e a
 * divergência fica registrada no relatório, porque uma delas é informação
 * sobre o jogo e não sobre o texto: o Saitama recebe "Sobrevivência" por ser
 * quem é, e a simulação diz que ele morre em 77% das lutas. Isso não é um erro
 * de etiqueta, é um personagem que não está fazendo o que deveria.
 */
const overrides: Record<string, readonly Identidade[]> = {
  saitama: ['Explosão', 'Finalização', 'Sobrevivência'],
  storm: ['Área', 'Controle', 'Ritmo'],
  wolverine: ['Pressão', 'Regeneração', 'Sobrevivência'],
  professorx: ['Suporte', 'Controle', 'Ritmo'],
};

/* --------------------------------------------------------------------------
 * Montagem
 * ------------------------------------------------------------------------ */

/*
 * Duas passagens, porque a ordem importa mais que a nota.
 *
 * A primeira versão deste script ordenava por evidência bruta e cortava em
 * quatro — e caiu exatamente no defeito que a FASE E documentou no sistema
 * antigo: a Sailor Moon tinha "Cura" com evidência 0,85 e perdia a vaga para
 * termos comuns com nota um pouco maior. "Cura" ficou com 1 personagem em 250.
 *
 * O problema é que evidência alta não é a mesma coisa que informação. Um termo
 * que 96 personagens têm diz pouco sobre qualquer um deles; um que 13 têm diz
 * muito. Então a primeira passagem levanta todos os candidatos, mede quantos
 * disputam cada termo, e a segunda ordena por **evidência × raridade**.
 *
 * É a correção direta do que a FASE E mediu: antes, a identidade mais rara era
 * a mais silenciada pelo corte.
 */
const candidatos = new Map<string, Map<Identidade, number>>();
const disputam = new Map<Identidade, number>();
for (const c of characters) {
  const notas = avaliar(c);
  candidatos.set(c.id, notas);
  for (const [id] of notas) disputam.set(id, (disputam.get(id) ?? 0) + 1);
}
/** Quanto um termo informa: quem é de poucos vale mais que quem é de muitos. */
const raridade = (id: Identidade): number => 1 - (disputam.get(id) ?? 0) / characters.length * 0.7;

const resultado: Record<string, Identidade[]> = {};
const divergencias: string[] = [];
const porTermo = new Map<Identidade, number>();

for (const c of characters) {
  const notas = candidatos.get(c.id)!;
  /*
   * Poucas etiquetas, e só as de verdade.
   *
   * Com quatro por personagem (210 dos 250 tinham quatro) a carta dizia "faz
   * de tudo" e deixava de dizer no que ele é bom. Agora cada etiqueta a mais
   * precisa de evidência mais forte: a primeira sempre entra; a segunda só
   * se ele estiver entre os 15% melhores do elenco naquilo; a terceira, entre
   * os 10%; a quarta só para quem é excepcional (3%).
   */
  const PISO_DA_POSICAO = [0, 0.85, 0.9, 0.97];
  const ordenadas = [...notas].sort((a, b) => b[1] * raridade(b[0]) - a[1] * raridade(a[0]));
  let escolhidas: Identidade[] = [];
  for (const [id, nota] of ordenadas) {
    if (escolhidas.length >= PISO_DA_POSICAO.length) break;
    if (nota >= PISO_DA_POSICAO[escolhidas.length]!) escolhidas.push(id);
  }

  /*
   * O piso de uma.
   *
   * Quem não passou em nada fica com a evidência mais forte que tem, mesmo
   * abaixo do corte: dizer "este personagem é sobretudo isto" continua sendo
   * verdade relativa, e deixar a carta sem etiqueta nenhuma seria pior.
   */
  if (escolhidas.length < 1) {
    const m = porId.get(c.id)!;
    const fallback: [Identidade, number][] = [
      ['Pressão', percentil('dano', m.dano as number)],
      ['Explosão', percentil('maiorGolpe', m.maiorGolpe as number)],
      ['Debuff', percentil('debuffsEmInimigo', m.debuffsEmInimigo as number)],
      ['Finalização', percentil('abates', m.abates as number)],
      ['Tanque', percentil('danoRecebido', m.danoRecebido as number)],
    ];
    for (const [id] of fallback.sort((a, b) => b[1] - a[1])) {
      if (!escolhidas.includes(id)) escolhidas.push(id);
      if (escolhidas.length === 1) break;
    }
  }

  const manual = overrides[c.id];
  if (manual) {
    const faltou = manual.filter((x) => !escolhidas.includes(x));
    if (faltou.length) divergencias.push(`${c.name}: a simulação não deu ${faltou.join(', ')} · medido: ${escolhidas.join(', ')}`);
    escolhidas = [...manual];
  }

  escolhidas.sort((a, b) => ordemDasIdentidades.indexOf(a) - ordemDasIdentidades.indexOf(b));
  resultado[c.id] = escolhidas;
  for (const x of escolhidas) porTermo.set(x, (porTermo.get(x) ?? 0) + 1);
}

const corpo = characters.map((c) => `  ${/^[a-z][a-z0-9]*$/.test(c.id) ? c.id : `'${c.id}'`}:[${resultado[c.id]!.map((x) => `'${x}'`).join(',')}],`).join('\n');
writeFileSync('src/data/identidades.ts', `/*
 * Gerado por scripts/derivar-identidades.ts a partir de 10.000 lutas medidas.
 * Não editar à mão: rode \`npx tsx scripts/medir-identidades.ts\` e depois
 * \`npx tsx scripts/derivar-identidades.ts\`.
 *
 * O porquê de cada identidade está em src/presentation/identities.ts.
 */
import type { Identidade } from '../presentation/identities';

export const identidadesPorPersonagem:Record<string,readonly Identidade[]> = {
${corpo}
};
`);

/* Relatório */
const combinacoes = new Map<string, number>();
for (const c of characters) combinacoes.set(resultado[c.id]!.join(' · '), (combinacoes.get(resultado[c.id]!.join(' · ')) ?? 0) + 1);
console.log(`${String(characters.length)} personagens · ${String(combinacoes.size)} combinações distintas\n`);
console.log('distribuição por termo (nenhum deve dominar o elenco):');
for (const t of ordemDasIdentidades) {
  const n = porTermo.get(t) ?? 0;
  console.log(`  ${t.padEnd(16)}${String(n).padStart(4)}  ${(n / characters.length * 100).toFixed(0).padStart(3)}%  ${'█'.repeat(Math.round(n / 5))}`);
}
const quantidades = characters.map((c) => resultado[c.id]!.length);
console.log(`\nidentidades por personagem: mín ${String(Math.min(...quantidades))} · máx ${String(Math.max(...quantidades))} · média ${(quantidades.reduce((a, b) => a + b, 0) / quantidades.length).toFixed(2)}`);
console.log(`combinação mais repetida: ${[...combinacoes].sort((a, b) => b[1] - a[1])[0]!.join(' → ')}×`);
if (divergencias.length) { console.log('\nonde o override discorda da simulação:'); for (const d of divergencias) console.log(`  ${d}`); }
console.log('\nexemplos:');
for (const id of ['saitama', 'storm', 'wolverine', 'professorx', 'sakura', 'gambit', 'thanos', 'pikachu']) {
  const c = characters.find((x) => x.id === id); if (!c) continue;
  console.log(`  ${c.name.padEnd(18)}${resultado[c.id]!.join(' · ')}`);
}
void statuses;
