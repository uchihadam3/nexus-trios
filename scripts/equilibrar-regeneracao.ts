/*
 * Regeneração honesta: o número escrito é o que cura.
 *
 * Antes, cada aplicação de Regeneração somava na anterior (até 25 de Vida
 * por segundo). Quem aplica toda hora — o traço "Presença" do Capitão
 * Planeta, "Puxar a corda" do Denji, Majin Boo, Ikki, Mumm-Ra… — escrevia
 * "4 Vida/s" e curava 17. Agora a Regeneração não soma: vale a mais forte, e
 * a duração renova (src/data/statuses.ts).
 *
 * Para não mudar a força de ninguém, este script mede quanto cada personagem
 * curava por minuto de luta com Regeneração na regra antiga, e acha o valor
 * que cura o mesmo na regra nova. Ninguém fica abaixo de 4 de Vida por
 * segundo (havia regenerações de 1,4/s, que quase não apareciam).
 *
 * Uso: npx tsx scripts/equilibrar-regeneracao.ts [lutas]   (escreve src/data/regeneracao.ts)
 */
import { writeFileSync } from 'node:fs';
import { characters, regeneracaoDeOrigem } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import { MINIMO_DA_REGENERACAO, valorDaRegeneracao } from '../src/data/regeneracao';
import { createBattle, stepBattle } from '../src/engine/battle';
import type { Effect } from '../src/engine/types';

const N = Number(process.argv[2] ?? 200), TETO = statuses.regen.cap;
const ids = characters.map((c) => c.id);
type Regen = Extract<Effect, { kind: 'status' }>;
const efeitosDe = (id: string): Regen[] => {
  const c = characters.find((x) => x.id === id)!;
  return [...c.skills.flatMap((s) => s.effects), ...c.trait.effects, ...c.basic.effects].filter((e): e is Regen => e.kind === 'status' && e.status === 'regen');
};
const fontes = ids.filter((id) => efeitosDe(id).length);
// os valores de hoje já têm o fator e o mínimo aplicados: volta ao valor de origem
const origem = new Map(fontes.map((id) => [id, regeneracaoDeOrigem.get(id)!]));
const poe = (id: string, valor: (v: number) => number) => efeitosDe(id).forEach((e, i) => { e.value = valor(origem.get(id)![i]!); });

/** Vida por minuto que as Regenerações deste personagem curam, em lutas sorteadas (as mesmas a cada medida). */
function mede(id: string): number {
  let r = 9001 + ids.indexOf(id) * 7919;
  const rnd = () => { r = (Math.imul(r, 1664525) + 1013904223) >>> 0; return r / 4294967296; };
  let cura = 0, tempo = 0;
  for (let n = 0; n < N; n++) {
    const s = new Set<string>([id]);
    while (s.size < 6) s.add(ids[Math.floor(rnd() * ids.length)]!);
    const [a, b, c, d, e, f] = [...s];
    const bt = createBattle([a!, b!, c!], [d!, e!, f!], Math.floor(rnd() * 1e9), 1), eu = bt.fighters.find((x) => x.characterId === id)!;
    for (let t = 0; t < 9000 && !bt.finished; t++) {
      for (const x of bt.fighters) if (x.hp > 0) for (const st of x.statuses) if (st.id === 'regen' && st.source === eu.uid) cura += Math.min(x.maxHp - x.hp, st.intensity * 0.1);
      stepBattle(bt);
    }
    tempo += bt.time;
  }
  return (cura / tempo) * 60;
}

/*
 * Quem aplicava Regeneração sem parar (traço de tempo/dano recebido) curava
 * pouco no começo e muito no fim, quando a soma enchia. Sem somar, a cura vem
 * cheia desde o início, e a mesma cura por minuto vale mais: estes dois
 * ficaram fixos no valor que mantém a chance de vitória de antes (lutas
 * pareadas, mesmas sementes: Capitão Planeta 66%, Mumm-Ra 57%).
 */
const PELA_VITORIA: Record<string, number> = { capitaoplaneta: 3.75, mummra: 2.333 };
const fator: Record<string, number> = {};
for (const id of fontes) {
  statuses.regen.stack = 'add'; poe(id, (v) => v);
  const alvo = mede(id);
  statuses.regen.stack = 'refresh';
  let k = 1;
  for (let passo = 0; passo < 4; passo++) {
    poe(id, (v) => Math.min(TETO, v * k));
    const agora = mede(id);
    if (agora <= 0) break;
    k = Math.max(0.5, Math.min(8, k * alvo / agora));
  }
  // o valor final é inteiro, entre o mínimo e o teto; o fator guarda isso por personagem
  fator[id] = PELA_VITORIA[id] ?? Math.round(k * 1000) / 1000;
  const finais = origem.get(id)!.map((v) => valorDaRegeneracao(v, fator[id]!));
  efeitosDe(id).forEach((e, i) => { e.value = finais[i]!; });
  console.log(id.padEnd(15), 'antes', Math.round(alvo), '/min', '→ agora', Math.round(mede(id)), '/min', '| valores', origem.get(id)!.join(','), '→', finais.join(','));
}
writeFileSync(new URL('../src/data/regeneracao.ts', import.meta.url), `/*
 * Fator da Regeneração de cada personagem, para que a Regeneração que não
 * soma (src/data/statuses.ts) cure o mesmo que curava quando somava — e o
 * número escrito seja o que cura. Gerado por scripts/equilibrar-regeneracao.ts.
 * Mínimo de ${MINIMO_DA_REGENERACAO} de Vida por segundo; teto de ${TETO}.
 */
export const MINIMO_DA_REGENERACAO = ${MINIMO_DA_REGENERACAO};
export const valorDaRegeneracao = (valor: number, fator = 1) => Math.max(MINIMO_DA_REGENERACAO, Math.min(${TETO}, Math.round(valor * fator)));
export const FATOR_DA_REGENERACAO: Record<string, number> = {
${Object.entries(fator).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `  ${JSON.stringify(k)}: ${v},`).join('\n')}
};
`);
