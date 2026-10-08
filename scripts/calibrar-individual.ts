/*
 * Calibragem individual por medição repetida.
 *
 * Mede os 250, ajusta só quem está fora da faixa, mede de novo, e repete. Cada
 * rodada mede todos — não só os ajustados — porque mexer num personagem muda
 * as lutas dos outros que o encontram.
 *
 * O ajuste é um fator só por personagem: multiplica dano e cura/Escudo, e a
 * Vida pela raiz dele (Vida pesa duas vezes: aguenta mais e dá tempo de agir).
 * Ele anda devagar em direção à faixa, não até o meio: calibrar não é achatar.
 *
 * No fim escreve a tabela em `src/data/calibragem-individual.ts` e confere com
 * sementes que não serviram para escolher nada.
 *
 * Uso: npx tsx scripts/calibrar-individual.ts   (RODADAS=4 SEMENTES=200)
 */
import { readFileSync, writeFileSync } from 'node:fs';

import { byId, personagensSemAjusteIndividual } from '../src/data/characters';
import { calibrarIndividualmente, type AjusteIndividual } from '../src/data/calibragem-individual';
import { createBattle, stepBattle } from '../src/engine/battle';

const RODADAS = Number(process.env.RODADAS ?? 4);
const SEMENTES = Number(process.env.SEMENTES ?? 200);
const PISO = 0.38, TETO = 0.62;
/* Para onde empurrar quem está fora: para dentro da faixa, não para 50%. */
const ALVO_BAIXO = 0.44, ALVO_ALTO = 0.56;
const SENSIBILIDADE = 1.6;
const MENOR = 0.55, MAIOR = 1.9;

/*
 * As âncoras da direção: o Saitama não deve ser nerfado pelo número, e a
 * Tempestade só levaria nerf se a medição confirmasse (e ela não confirma).
 * Deixá-los de fora não basta — na primeira tentativa os outros subiram e os
 * dois caíram para 36% e 37%, um nerf por tabela. Então eles podem subir de
 * volta para a faixa, e nunca descer.
 */
const SO_SOBEM = new Set(['saitama', 'storm']);

/*
 * O Light fica fora. O fator mexe na Vida, e no máximo levava a dele a 1.240:
 * a medição passava a chamá-lo de "Tanque", e a ficha diz "Pouca Vida". O
 * que o segura é a regra da Death Note, e ela foi corrigida na mecânica
 * (`battle.ts`: um alvo de cada vez; no imune, uma vez só).
 */
const FORA = new Set(['light']);

const base = new Map(personagensSemAjusteIndividual.map((c) => [c.id, structuredClone(c)]));
const ids = [...base.keys()];
const fator = new Map<string, number>(ids.map((id) => [id, 1]));

/* Fator 1 é "sem ajuste": nada de arredondar a Vida de quem não foi mexido. */
const ajusteDe = (f: number): AjusteIndividual => (f === 1 ? {} : { dano: f, sustento: f, vida: Number(Math.sqrt(f).toFixed(3)) });

/* Aplica os fatores atuais por cima do elenco que a batalha consulta. */
function aplicar() {
  for (const id of ids) {
    const c = calibrarComFator(base.get(id)!, fator.get(id)!);
    Object.assign(byId[id]!, structuredClone(c));
  }
}
function calibrarComFator(c: (typeof personagensSemAjusteIndividual)[number], f: number) {
  /* Mesmo caminho do jogo, para a medição e o jogo não divergirem. */
  return calibrarIndividualmente(c, ajusteDe(f));
}

function medir(semente0: number): Map<string, number> {
  const taxa = new Map<string, number>();
  for (const [indice, id] of ids.entries()) {
    const outros = ids.filter((o) => o !== id);
    let v = 0;
    for (let s = 0; s < SEMENTES; s += 1) {
      const k = s + semente0;
      const pega = (n: number) => outros[(k * 37 + n * 61 + indice) % outros.length]!;
      const b = createBattle([id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], k + 1);
      for (let passo = 0; passo < 4200 && !b.finished; passo += 1) stepBattle(b);
      if (b.winner === 'player') v += 1;
    }
    taxa.set(id, v / SEMENTES);
  }
  return taxa;
}

const resumo = (t: Map<string, number>) => {
  const xs = [...t.values()], m = xs.reduce((a, b) => a + b, 0) / xs.length;
  const fora = xs.filter((x) => x < PISO || x > TETO).length;
  const dp = Math.sqrt(xs.reduce((a, x) => a + (x - m) ** 2, 0) / xs.length);
  return `média ${(m * 100).toFixed(1)}% · desvio ${(dp * 100).toFixed(1)} · fora da faixa ${String(fora)} · min ${(Math.min(...xs) * 100).toFixed(0)}% max ${(Math.max(...xs) * 100).toFixed(0)}%`;
};

let taxa = new Map<string, number>();
for (let r = 0; r <= RODADAS; r += 1) {
  aplicar();
  taxa = medir(0);
  console.log(`rodada ${String(r)}: ${resumo(taxa)}`);
  if (r === RODADAS) break;
  for (const id of ids) {
    if (FORA.has(id)) continue;
    const t = taxa.get(id)!;
    if (t >= PISO && t <= TETO) continue;
    const alvo = t < PISO ? ALVO_BAIXO : ALVO_ALTO;
    const novo = fator.get(id)! * Math.exp((alvo - t) * SENSIBILIDADE);
    const limitado = Math.min(MAIOR, Math.max(SO_SOBEM.has(id) ? 1 : MENOR, Number(novo.toFixed(2))));
    fator.set(id, limitado);
  }
}

/* Fora da amostra: sementes que não serviram para escolher nada. */
const conferencia = medir(5000);
console.log(`conferência (outras sementes): ${resumo(conferencia)}`);

const ajustados = ids.filter((id) => fator.get(id) !== 1).sort();
const nome = (id: string) => base.get(id)!.name;
const linhas = ajustados.map((id) => {
  const a = ajusteDe(fator.get(id)!);
  return `  ${/^[a-z][a-z0-9]*$/.test(id) ? id : `'${id}'`}: { dano: ${String(a.dano)}, sustento: ${String(a.sustento)}, vida: ${String(a.vida)} }, // ${nome(id)} · ${(conferencia.get(id)! * 100).toFixed(0)}% na conferência`;
});
const tabela = `/* tabela:inicio */\nexport const ajustesIndividuais: Readonly<Record<string, AjusteIndividual>> = {\n${linhas.join('\n')}\n};\n/* tabela:fim */`;
const arquivo = 'src/data/calibragem-individual.ts';
const fonte = readFileSync(arquivo, 'utf8');
writeFileSync(arquivo, fonte.replace(/\/\* tabela:inicio \*\/[\s\S]*\/\* tabela:fim \*\//, tabela));
console.log(`\n${String(ajustados.length)} personagens ajustados; tabela escrita em ${arquivo}`);
for (const id of ajustados) console.log(`  ${nome(id).padEnd(24)} fator ${fator.get(id)!.toFixed(2)} · ${(conferencia.get(id)! * 100).toFixed(0)}% na conferência`);
