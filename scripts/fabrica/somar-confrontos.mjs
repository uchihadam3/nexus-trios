// Junta as partes do plano confrontos (scripts/fabrica/lutas.ts): a primeira linha (# motor…), todas as lutas da
// amostra (L), a tabela personagem × personagem somada (M i j n w), a das duplas do mesmo trio (P i j n w) e o total (T).
// O total também vai para o stderr.
// Uso: node somar-confrontos.mjs parte-0.txt parte-1.txt … > lutas.txt
import { readFileSync } from 'node:fs';
const soma = new Map(), duplas = new Map();
let cabeca = '', total = 0;
const saida = [];
for (const f of process.argv.slice(2)) {
  for (const linha of readFileSync(f, 'utf8').split('\n')) {
    if (!linha) continue;
    if (linha[0] === '#') { if (!cabeca) cabeca = linha.replace(/ parte \d+\/\d+/, ''); continue; }
    const x = linha.split(' ');
    if (x[0] === 'L') saida.push(linha);
    else if (x[0] === 'M' || x[0] === 'P') { const m = x[0] === 'M' ? soma : duplas, k = `${x[1]} ${x[2]}`, s = m.get(k) ?? [0, 0]; s[0] += Number(x[3]); s[1] += Number(x[4]); m.set(k, s); }
    else if (x[0] === 'T') total += Number(x[1]);
  }
}
process.stdout.write(`${cabeca}\n${saida.join('\n')}\n`);
const linhas = [];
for (const [letra, m] of [['M', soma], ['P', duplas]]) for (const [k, [n, w]] of m) { linhas.push(`${letra} ${k} ${n} ${w}`); if (linhas.length >= 20000) { process.stdout.write(`${linhas.join('\n')}\n`); linhas.length = 0; } }
process.stdout.write(`${linhas.length ? `${linhas.join('\n')}\n` : ''}T ${total}\n`);
process.stderr.write(`${total}\n`);
