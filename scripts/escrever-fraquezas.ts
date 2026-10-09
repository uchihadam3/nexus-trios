/*
 * O ponto fraco de cada personagem, escrito a partir do que o derruba.
 *
 * Pedido do jogador: o ponto fraco tem que dizer de verdade contra o que o
 * personagem é ruim e por que ele perde — não uma frase vaga ("perde o
 * controle e perde a luta"). Então cada candidato a fraqueza vem com prova:
 *
 * - da ficha: pouca Vida, ataque lento, golpe principal com Preparo longo,
 *   habilidade que depende de condição, nenhuma cura/Escudo no kit, dano só
 *   em um alvo;
 * - da simulação (docs/fraquezas-medidas.json, 20 mil lutas): quantos Preparos
 *   são cortados, quantos segundos passa preso, quanto cai primeiro, quanto
 *   cai de um golpe só, e quanto vence a menos contra rivais com certa
 *   identidade (Interrupção, Controle, Explosão, Cura…).
 *
 * Cada candidato ganha uma nota pelo tamanho da prova em relação ao elenco; os
 * dois maiores viram o texto, sempre no formato "contra o quê: por quê".
 *
 * Uso: npx tsx scripts/escrever-fraquezas.ts   (escreve src/data/fraquezas.ts)
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import type { Character, Effect, Skill } from '../src/engine/types';
import { statuses } from '../src/data/statuses';

const NOME_DO_STATUS: Record<string, string> = Object.fromEntries(Object.entries(statuses).map(([k, v]) => [k, v.name]));

interface Medida {
  id: string; lutas: number; vitorias: number; taxaDeQueda: number; primeiroACair: number; quedaPorGolpeGrande: number;
  preparos: number; cortados: number; controleSegundos: number; danoContinuoRecebido: number; tempoDeQueda: number | null;
  contra: Record<string, { lutas: number; vitorias: number }>;
}
const dados = JSON.parse(readFileSync('docs/fraquezas-medidas.json', 'utf8')) as { lutas: number; medidas: Medida[] };
const porId = new Map(dados.medidas.map((m) => [m.id, m]));

const num = (v: number, casas = 0) => v.toLocaleString('pt-BR', { maximumFractionDigits: casas, minimumFractionDigits: casas });
const pct = (v: number) => `${Math.round(v * 100)}%`;
/* Posição no elenco, de 0 (menor) a 1 (maior). */
const posicao = (valores: number[], v: number) => valores.filter((x) => x < v).length / Math.max(1, valores.length - 1);

const vidas = characters.map((c) => c.hp), intervalos = characters.map((c) => c.interval);
const med = (k: keyof Medida) => dados.medidas.map((m) => m[k] as number).filter((x) => Number.isFinite(x));
const controles = med('controleSegundos'), primeiros = med('primeiroACair'), golpes = med('quedaPorGolpeGrande'), queimas = med('danoContinuoRecebido');

const SUSTENTO = (e: Effect) => e.kind === 'heal' || e.kind === 'shield' || (e.kind === 'status' && ['regen', 'protected'].includes(e.status));
const temSustento = (c: Character) => [...c.skills.flatMap((s) => s.effects), ...c.trait.effects].some(SUSTENTO);
const temArea = (c: Character) => c.skills.some((s) => s.target === 'allEnemies' || s.effects.some((e) => e.target === 'allEnemies'));
const danoDe = (s: Skill) => s.effects.reduce((t, e) => t + (e.kind === 'damage' ? e.value * (s.target === 'allEnemies' || e.target === 'allEnemies' ? 2.2 : 1) : 0), 0);

const CONDICAO: Record<string, string> = {
  injured: 'o alvo já estiver ferido', enemyCast: 'um inimigo estiver em Preparo',
  threatened: 'o trio estiver sob ameaça', investigated: 'houver um alvo investigado por completo',
  vulnerable: 'um inimigo estiver vulnerável (Exposto, Marcado, Queimando, Envenenado…)', storedEnergy: 'houver energia guardada',
};

/* Quanto ele vence a menos contra rivais com esta identidade (em pontos), bruto. */
function contraBruto(m: Medida, id: string): number | undefined {
  const c = m.contra[id];
  if (!c || c.lutas < 40) return undefined;
  return (m.vitorias - c.vitorias) * 100;
}
/*
 * O normal do elenco contra cada identidade: quando uma mecânica é forte contra
 * quase todo mundo (Provocar, Refletir), "vence menos contra ela" não é ponto
 * fraco de ninguém em particular. Conta só o que passa do normal.
 */
const NORMAL_CONTRA = new Map<string, number>();
for (const id of new Set(dados.medidas.flatMap((m) => Object.keys(m.contra)))) {
  const v = dados.medidas.map((m) => contraBruto(m, id)).filter((x): x is number => x !== undefined).sort((a, b) => a - b);
  NORMAL_CONTRA.set(id, v.length ? v[Math.floor(v.length / 2)]! : 0);
}
function contra(m: Medida, id: string): number {
  const d = contraBruto(m, id);
  return d === undefined ? 0 : Math.round(d - (NORMAL_CONTRA.get(id) ?? 0));
}

interface Candidata { nota: number; texto: string; chave: string }

const DANOS = characters.map((x) => Math.max(0, ...x.skills.map(danoDe)));
const mediana = (v: number[]) => [...v].sort((a, b) => a - b)[Math.floor(v.length / 2)]!;
const intervaloTipico = mediana(intervalos);

function candidatas(c: Character, m: Medida): Candidata[] {
  const out: Candidata[] = [];
  const pVida = posicao(vidas, c.hp), pIntervalo = posicao(intervalos, c.interval);
  const forte = [...c.skills].sort((a, b) => danoDe(b) - danoDe(a))[0]!;
  const preparoMax = [...c.skills].sort((a, b) => b.preparation - a.preparation)[0]!;
  const dInt = contra(m, 'Interrupção'), dCtl = contra(m, 'Controle'), dExp = contra(m, 'Explosão'), dArea = contra(m, 'Área');
  const dCura = Math.max(contra(m, 'Cura'), contra(m, 'Proteção')), dCont = contra(m, 'Dano contínuo'), dTanque = contra(m, 'Tanque');
  /* d = pontos percentuais de vitória a menos; dito de um jeito que se entende */
  const aMenos = (d: number) => (d >= 4 ? `. Contra esses trios, ganha ${d} de cada 100 lutas a menos` : '');

  // o golpe principal pode ser cortado
  if (preparoMax.preparation >= 2 || (preparoMax.preparation >= 1.2 && m.cortados >= 0.1)) {
    const nota = (m.cortados - 0.06) * 15 + (preparoMax.preparation - 1.5) * 0.7 + Math.max(0, dInt - 2) * 0.3;
    const medido = m.cortados >= 0.1 ? ` (é cortado em ${pct(m.cortados)} das vezes)` : '';
    out.push({ chave: 'interrupcao', nota, texto: `Contra Interrupção: ${preparoMax.name} leva ${num(preparoMax.preparation, 1)} s de Preparo${medido} — se for cortado, perde a jogada principal${aMenos(dInt)}` });
  }
  // pouca Vida
  if (pVida <= 0.3) {
    const golpe = posicao(golpes, m.quedaPorGolpeGrande) >= 0.7 && m.quedaPorGolpeGrande >= 0.1;
    const nota = (0.3 - pVida) * 10 + Math.max(0, dExp - 2) * 0.3 + (golpe ? 0.5 : 0);
    const prova = golpe ? ` — quando cai, cai de um golpe só em ${pct(m.quedaPorGolpeGrande)} das vezes` : ' — poucos golpes fortes bastam para derrubá-lo';
    out.push({ chave: 'vida', nota, texto: `Contra Explosão: só ${num(c.hp)} de Vida, das menores do elenco${prova}${aMenos(dExp)}` });
  }
  // fica preso
  {
    const nota = (posicao(controles, m.controleSegundos) - 0.75) * 6 + Math.max(0, dCtl - 2) * 0.35;
    out.push({ chave: 'controle', nota, texto: `Contra Controle: passa ${num(m.controleSegundos, 1)} s por luta preso, paralisado ou confuso — tempo em que ${forte.name} não carrega${aMenos(dCtl)}` });
  }
  // sem cura, Escudo nem Regeneração
  if (!temSustento(c)) {
    const nota = 0.8 + (pVida <= 0.4 ? 0.5 : 0) + (posicao(primeiros, m.primeiroACair) >= 0.7 ? 0.4 : 0);
    out.push({ chave: 'sustento', nota, texto: `Em luta longa: o kit é só ataque, de ${forte.name} ao básico — sem cura, Escudo ou Regeneração, depende de um aliado que proteja para não ser desgastado` });
  }
  /*
   * Lento: o ataque básico demora, então quase todo o dano vem das
   * habilidades. Isso só é fraqueza contra quem tira as habilidades dele de
   * jogo (Controle, Interrupção) — "contra trios rápidos" não explicava nada
   * (pedido do jogador: "ataca só a cada três segundos… não faz sentido").
   */
  if (pIntervalo >= 0.75) {
    const quemTrava = Math.max(dCtl, dInt);
    const nota = (pIntervalo - 0.75) * 6 + (c.interval >= 5 ? 0.6 : 0) + Math.max(0, quemTrava - 2) * 0.3;
    const contraQuem = dCtl >= dInt ? 'Controle' : 'Interrupção';
    out.push({ chave: 'lento', nota, texto: `Contra ${contraQuem}: o básico (${c.basic.name}) sai só a cada ${num(c.interval, 1)} s (o comum é ${num(intervaloTipico, 1)} s), então o dano vem das habilidades — travado ou cortado, quase não machuca${aMenos(quemTrava)}` });
  }
  // dano num alvo só, contra quem repõe
  if (!temArea(c) && dCura >= 4) {
    out.push({ chave: 'alvo', nota: dCura * 0.3, texto: `Contra Cura e Escudo: o golpe mais forte, ${forte.name}, acerta um alvo só, e o rival repõe o que ele tira${aMenos(dCura)}` });
  }
  // depende de condição
  const condicional = c.skills.find((s) => s.condition !== 'always' && danoDe(forte) > 0 && danoDe(s) >= danoDe(forte) * 0.6 && CONDICAO[s.condition]);
  if (condicional) {
    const principal = danoDe(condicional) >= danoDe(forte) * 0.9;
    // "alvo ferido" é fácil de cumprir: só conta como fraqueza quando a condição é rara de verdade
    const rara = condicional.condition !== 'injured';
    const golpe = danoDe(condicional) > 0;
    const falta = golpe ? (principal ? 'o golpe mais forte' : 'um dos golpes principais') : 'uma das jogadas principais';
    out.push({ chave: 'condicao', nota: rara ? (principal ? 1.4 : 0.9) : 0.3, texto: `Depende do momento: ${condicional.name} só sai quando ${CONDICAO[condicional.condition]} — sem isso, fica sem ${falta}` });
  }
  // queima
  if (posicao(queimas, m.danoContinuoRecebido) >= 0.8 && dCont >= 4) {
    out.push({ chave: 'continuo', nota: dCont * 0.3, texto: `Contra Dano contínuo: passa ${num(m.danoContinuoRecebido, 1)} s por luta Queimando, Envenenado ou Sangrando e não tem como limpar — com ${num(c.hp)} de Vida, isso pesa${aMenos(dCont)}` });
  }
  // área
  if (dArea >= 6) out.push({ chave: 'area', nota: dArea * 0.3, texto: `Contra Área: com ${num(c.hp)} de Vida, sofre junto com o trio inteiro quando o rival acerta todos de uma vez${aMenos(dArea)}` });
  // precisa apanhar para crescer
  const cresceApanhando = c.trait.on === 'received' && c.trait.effects.some((e) => e.kind === 'status' && ['strengthened', 'haste'].includes(e.status));
  if (cresceApanhando) {
    out.push({ chave: 'apanha', nota: 1.2 + (pVida <= 0.4 ? 0.4 : 0) + Math.max(0, dExp - 2) * 0.2, texto: `Precisa apanhar para crescer: ${c.trait.name} só o fortalece quando ele recebe dano — contra Explosão, cai antes de crescer o bastante para ${forte.name} fazer diferença${aMenos(dExp)}` });
  }
  // tanques
  if (dTanque >= 6) out.push({ chave: 'tanque', nota: dTanque * 0.3, texto: `Contra Tanques: ${forte.name} não dá conta de quem aguenta muito — o rival segura o golpe e continua de pé${aMenos(dTanque)}` });
  /*
   * As mecânicas novas: cada uma só vira ponto fraco quando o kit dá o motivo
   * E a medida mostra que ele vence menos contra quem tem aquela tag.
   */
  const REFORCO_PROPRIO = ['strengthened', 'haste', 'protected', 'regen', 'barrier', 'evasion', 'vampirism', 'reflect', 'thorns'];
  const buff = c.skills.find((s) => s.effects.some((e) => e.kind === 'status' && REFORCO_PROPRIO.includes(e.status) && (e.target ?? s.target) === 'self'));
  const dDis = contra(m, 'Dissipar');
  if (buff && dDis >= 6) {
    const st = buff.effects.find((e) => e.kind === 'status' && REFORCO_PROPRIO.includes(e.status))!;
    out.push({ chave: 'dissipar', nota: dDis * 0.32, texto: `Contra Dissipar: a força dele vem de ${buff.name} (${st.kind === 'status' ? NOME_DO_STATUS[st.status] ?? st.status : ''}) — quem dissipa tira o reforço e ele volta a ser comum${aMenos(dDis)}` });
  }
  const DEBUFF_FORTE = ['paralyzed', 'frozen', 'sleep', 'poison', 'bleed', 'burning', 'cursed', 'confused', 'silenced', 'rooted'];
  const prende = c.skills.find((s) => s.effects.some((e) => e.kind === 'status' && DEBUFF_FORTE.includes(e.status) && (e.target ?? s.target) !== 'self'));
  const dPur = contra(m, 'Purificar');
  if (prende && dPur >= 6) out.push({ chave: 'purificar', nota: dPur * 0.32, texto: `Contra Purificar: o plano dele é ${prende.name} — quem purifica limpa o rival e desfaz a jogada${aMenos(dPur)}` });
  const dProv = contra(m, 'Provocar');
  const umAlvo = forte.target !== 'allEnemies' && !forte.effects.some((e) => e.target === 'allEnemies');
  if (dProv >= 7 && umAlvo) out.push({ chave: 'provocar', nota: dProv * 0.3, texto: `Contra Provocar: o rival que provoca puxa os golpes de ${forte.name} para quem aguenta, longe de quem ele queria derrubar${aMenos(dProv)}` });
  const dEsq = contra(m, 'Esquiva');
  if (dEsq >= 7 && umAlvo && posicao(DANOS, danoDe(forte)) >= 0.5) out.push({ chave: 'esquiva', nota: dEsq * 0.3, texto: `Contra Esquiva: ${forte.name} é um golpe só — se o rival esquiva, a jogada inteira passa longe${aMenos(dEsq)}` });
  const dRef = Math.max(contra(m, 'Refletir'), contra(m, 'Espinhos'));
  if (dRef >= 7 && posicao(DANOS, danoDe(forte)) >= 0.6) out.push({ chave: 'refletir', nota: dRef * 0.3, texto: `Contra Refletir e Espinhos: bate forte com ${forte.name} e leva parte do golpe de volta${aMenos(dRef)}` });
  const dCeg = contra(m, 'Cegueira');
  if (dCeg >= 7) out.push({ chave: 'cegueira', nota: dCeg * 0.3, texto: `Contra Cegueira: o ataque básico (${c.basic.name}) passa longe com frequência, e é ele que enche a Carga das habilidades${aMenos(dCeg)}` });
  return out;
}

const textos: Record<string, string> = {};
const resumo: Record<string, number> = {};
for (const c of characters) {
  const m = porId.get(c.id);
  if (!m) continue;
  const lista = candidatas(c, m).sort((a, b) => b.nota - a.nota);
  /* O principal vai inteiro, com a prova; o segundo só se for forte e couber, sem a frase de estatística. */
  const [primeira, segunda] = lista;
  let texto = primeira!.texto + '.';
  resumo[primeira!.chave] = (resumo[primeira!.chave] ?? 0) + 1;
  if (segunda && segunda.nota >= 1.3) {
    const curta = segunda.texto.split('. Contra esses trios')[0] + '.';
    if (texto.length + curta.length + 1 <= 240) { texto += ' ' + curta; resumo[segunda.chave] = (resumo[segunda.chave] ?? 0) + 1; }
  }
  textos[c.id] = texto;
}

const corpo = Object.entries(textos).map(([id, t]) => `  ${JSON.stringify(id)}: ${JSON.stringify(t)},`).join('\n');
writeFileSync('src/data/fraquezas.ts', `/*
 * Ponto fraco de cada personagem — gerado por scripts/escrever-fraquezas.ts a
 * partir da ficha e de ${num(dados.lutas)} lutas simuladas (docs/fraquezas-medidas.json).
 * Não editar à mão: rode o script de novo depois de mudar o elenco.
 */
export const fraquezas: Record<string, string> = {
${corpo}
};
`);
console.log('escolhas por tipo:', resumo);
for (const id of ['donald', 'goku', 'nezuko', 'light', 'saitama', 'pikachu', 'batman', 'hulk']) console.log(`${id}: ${textos[id]}`);
