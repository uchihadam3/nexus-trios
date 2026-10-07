/*
 * FASE D · calibrar os 250 juntos.
 *
 * A direção foi explícita sobre o método: não vale comparar "dano 300 contra
 * dano 700". Um número alto preso atrás de Preparo longo, Carga cara e
 * condição estreita vale menos que um número médio que sai sempre; e dano em
 * três alvos não vale o triplo de dano em um.
 *
 * Então a medida aqui é a única que responde à pergunta de verdade: **com este
 * personagem no trio, com que frequência o trio ganha?** Cada personagem joga
 * o mesmo conjunto de sementes, com aliados e adversários sorteados pela mesma
 * regra, para que a comparação seja entre eles e não entre sorteios.
 *
 * O script também calcula uma nota estrutural — a "ameaça" que a ficha promete,
 * com retorno decrescente por alvo adicional — e compara com a vitória medida.
 * Onde as duas discordam muito, ou a ficha promete o que não entrega, ou
 * entrega o que não promete. As duas coisas interessam.
 *
 * Nada é alterado aqui. O script mede e ordena.
 */
import { writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import type { Character, Effect } from '../src/engine/types';
import { createBattle, stepBattle } from '../src/engine/battle';

/*
 * Quantas sementes bastam, e por que 24 não bastavam.
 *
 * A primeira rodada usou 24 e produziu uma lista de "fora da curva" que eu
 * quase usei para nerfar e buffar gente. Antes disso, medi o mesmo personagem
 * com três conjuntos diferentes de 24 sementes: o Saitama deu 50,0%, 29,2% e
 * 54,2%. Vinte e cinco pontos de variação sem nada ter mudado.
 *
 * Com esse ruído, qualquer conclusão sobre **um** personagem é sorteio. O que
 * sobrevive é o agregado por família, que junta vários personagens e centenas
 * de lutas — e esse, medido a 100 sementes, dá intervalo de ±4 a 5 pontos.
 *
 * Então: a unidade de calibragem aqui é a família, não o indivíduo. Para
 * decidir sobre um personagem isolado, suba as sementes e olhe o intervalo.
 */
const SEMENTES = Number(process.env.SEMENTES ?? 24);

/* ---------------------------------------------------------------------------
 * A nota estrutural: o que a ficha promete.
 * ------------------------------------------------------------------------- */

/*
 * Retorno decrescente por alvo.
 *
 * Atingir três inimigos não vale três vezes atingir um: parte do dano cai em
 * quem já ia morrer, e o excedente se perde. A direção pediu a métrica
 * explícita, então ela está aqui e não escondida numa constante.
 */
const VALOR_POR_ALVO = { 1: 1, 2: 1.7, 3: 2.2 } as const;
const alvosDe = (alvo: string): 1 | 2 | 3 =>
  alvo === 'allEnemies' || alvo === 'allAllies' ? 3 : 1;

/** Quanto uma habilidade entrega por segundo, já descontado o custo de acesso. */
const notaDaHabilidade = (c: Character, indice: number): number => {
  const s = c.skills[indice]!;
  const multi = VALOR_POR_ALVO[alvosDe(s.target)];

  let bruto = 0;
  for (const e of s.effects as Effect[]) {
    const peso = VALOR_POR_ALVO[alvosDe(e.target ?? s.target)];
    if (e.kind === 'damage') bruto += e.value * peso;
    else if (e.kind === 'heal') bruto += e.value * 0.85 * peso;
    else if (e.kind === 'shield') bruto += e.value * 0.8 * peso;
    else if (e.kind === 'release') bruto += 220 * e.multiplier;
    else if (e.kind === 'interrupt') bruto += 90 * peso;
    else if (e.kind === 'status') {
      /* Controle duro vale mais que um empurrão percentual. */
      const forca = e.status === 'paralyzed' ? 150 : e.status === 'silenced' ? 90
        : e.status === 'rooted' ? 80 : e.status === 'slow' ? 55
        : e.status === 'strengthened' || e.status === 'weakened' ? 70
        : e.status === 'protected' ? 95 : e.status === 'regen' || e.status === 'burning' ? 9
        : 45;
      bruto += forca * e.value * Math.min(3, e.duration / 5) * peso;
    }
  }

  /*
   * O custo de acesso.
   *
   * Carga lenta, Preparo longo, recarga alta e condição estreita são o preço.
   * É o que impede o Soco Sério de parecer quebrado pelo número nominal: ele
   * entrega muito uma vez, e o caminho até lá é caro.
   */
  const porSegundo = s.charge.reduce((soma, r) => soma + r.amount, 0);
  const segundosAteSair = porSegundo > 0 ? 100 / porSegundo : 60;
  const ciclo = Math.max(1, segundosAteSair + s.preparation + s.cooldown * 0.4);
  const riscoDePreparo = 1 - Math.min(0.45, s.preparation * 0.08);
  const estreiteza = s.condition === 'always' ? 1 : s.condition === 'vulnerable' ? 0.82 : 0.75;
  const corrente = s.requiresSkills && s.requiresSkills.length > 0 ? 0.8 : 1;

  return (bruto / ciclo) * riscoDePreparo * estreiteza * corrente * (multi > 1 ? 1 : 1);
};

const notaEstrutural = (c: Character): number => {
  const basico = c.basic.effects.reduce((soma, e) => soma + (e.kind === 'damage' ? e.value : 0), 0) / c.interval;
  const habilidades = [0, 1, 2].reduce((soma, i) => soma + notaDaHabilidade(c, i), 0);
  const resistencia = (c.hp / 1000) * 22;
  return basico * 1.6 + habilidades + resistencia;
};

/* ---------------------------------------------------------------------------
 * A medida de verdade: vitória com o personagem no trio.
 * ------------------------------------------------------------------------- */

interface Medida {
  id: string; nome: string; universo: string;
  vitorias: number; lutas: number; taxa: number;
  danoMedio: number; curaMedia: number; protecaoMedia: number;
  abatesMedios: number; sobrevivencia: number;
  nota: number; poderDeclarado: number;
}

const medidas: Medida[] = [];

for (const [indice, c] of characters.entries()) {
  let vitorias = 0, dano = 0, cura = 0, protecao = 0, abates = 0, vivo = 0;
  for (let s = 0; s < SEMENTES; s += 1) {
    const outros = characters.filter((o) => o.id !== c.id);
    /* A mesma regra de sorteio para todos: o que varia é quem está medindo. */
    const pega = (n: number) => outros[(s * 37 + n * 61 + indice) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 1);
    const eu = b.fighters[0]!;
    for (let passo = 0; passo < 4200 && !b.finished; passo += 1) stepBattle(b);
    if (b.winner === 'player') vitorias += 1;
    dano += eu.stats.damage; cura += eu.stats.healing; protecao += eu.stats.protection;
    abates += eu.stats.kills; if (eu.hp > 0) vivo += 1;
  }
  medidas.push({
    id: c.id, nome: c.name, universo: c.universe,
    vitorias, lutas: SEMENTES, taxa: vitorias / SEMENTES,
    danoMedio: Math.round(dano / SEMENTES), curaMedia: Math.round(cura / SEMENTES),
    protecaoMedia: Math.round(protecao / SEMENTES), abatesMedios: Number((abates / SEMENTES).toFixed(2)),
    sobrevivencia: vivo / SEMENTES,
    nota: Number(notaEstrutural(c).toFixed(1)), poderDeclarado: c.power,
  });
}

medidas.sort((a, b) => b.taxa - a.taxa);

const taxas = medidas.map((m) => m.taxa);
const media = taxas.reduce((a, b) => a + b, 0) / taxas.length;
const desvio = Math.sqrt(taxas.reduce((a, t) => a + (t - media) ** 2, 0) / taxas.length);

/** Fora de dois desvios: candidato a ajuste, não condenado automático. */
const acimaDaCurva = medidas.filter((m) => m.taxa > media + desvio * 2);
const abaixoDaCurva = medidas.filter((m) => m.taxa < media - desvio * 2);

writeFileSync('docs/calibragem-250.json', `${JSON.stringify({
  sementesPorPersonagem: SEMENTES, media, desvio, medidas,
  acimaDaCurva: acimaDaCurva.map((m) => m.nome), abaixoDaCurva: abaixoDaCurva.map((m) => m.nome),
}, null, 2)}\n`);

const linha = (m: Medida) =>
  `  ${(m.taxa * 100).toFixed(1).padStart(5)}%  ${m.nome.padEnd(24)} dano ${String(m.danoMedio).padStart(5)} · cura ${String(m.curaMedia).padStart(4)} · prot ${String(m.protecaoMedia).padStart(4)} · vive ${(m.sobrevivencia * 100).toFixed(0).padStart(3)}% · nota ${String(m.nota).padStart(6)} · poder ${String(m.poderDeclarado)}`;

console.log(`${String(characters.length)} personagens · ${String(SEMENTES)} lutas cada · ${String(characters.length * SEMENTES)} lutas`);
console.log(`vitória média: ${(media * 100).toFixed(1)}% · desvio: ${(desvio * 100).toFixed(1)} pontos\n`);
console.log('=== os 12 mais fortes ===');
for (const m of medidas.slice(0, 12)) console.log(linha(m));
console.log('\n=== os 12 mais fracos ===');
for (const m of medidas.slice(-12)) console.log(linha(m));
console.log(`\n=== acima de dois desvios (${String(acimaDaCurva.length)}) ===`);
for (const m of acimaDaCurva) console.log(linha(m));
console.log(`\n=== abaixo de dois desvios (${String(abaixoDaCurva.length)}) ===`);
for (const m of abaixoDaCurva) console.log(linha(m));

/*
 * O intervalo de confiança, dito junto com o número.
 *
 * Um número sem intervalo convida a agir sobre ruído, que foi exatamente o que
 * quase aconteceu nesta fase.
 */
const erro = (taxa: number, n: number): number => Math.sqrt((taxa * (1 - taxa)) / n) * 1.96 * 100;
console.log(`\nintervalo de confiança de uma medida individual com ${String(SEMENTES)} sementes: ±${erro(0.5, SEMENTES).toFixed(1)} pontos`);
console.log('Acima de ±10, conclusões sobre um personagem isolado são sorteio. Use o agregado por família.');

console.log('\n=== as duas âncoras que a direção nomeou ===');
for (const id of ['saitama', 'storm']) {
  const m = medidas.find((x) => x.id === id)!;
  const posicao = medidas.indexOf(m) + 1;
  console.log(`${m.nome}: ${(m.taxa * 100).toFixed(1)}% de vitória · posição ${String(posicao)} de ${String(medidas.length)} · ${((m.taxa - media) / desvio).toFixed(2)} desvios da média`);
  console.log(linha(m));
}
