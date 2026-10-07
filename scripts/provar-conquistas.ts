/*
 * Toda conquista precisa ser alcançável.
 *
 * Uma conquista impossível é pior que nenhuma: ela fica na lista para sempre,
 * o jogador tenta, não consegue, e aprende que a lista mente. Este script joga
 * centenas de lutas com trios variados e conta quantas vezes cada uma dispara.
 *
 * Zero é defeito. Um número altíssimo também é: uma conquista que acontece em
 * toda luta não é conquista, é aviso de que a luta aconteceu.
 */
import { characters } from '../src/data/characters';
import { conquistas, conquistasDaBatalha, type Contexto } from '../src/engine/conquistas';
import { createBattle, stepBattle } from '../src/engine/battle';
import { acumularFeitos, fecharFeitos, feitosVazios } from '../src/engine/maestria';
import { acumularRaioX, raioXVazio } from '../src/engine/raio-x';
import { summarizeBattle, type RunBattleSummary } from '../src/engine/run-summary';

const LUTAS = Number(process.env.LUTAS ?? 400);
const vezes = new Map<string, number>();
let total = 0;

/* Jornadas de verdade: o mesmo trio em sequência, para as conquistas de jornada. */
for (let j = 1; j <= Math.ceil(LUTAS / 10); j += 1) {
  const pega = (n: number) => characters[(j * 71 + n * 43) % characters.length]!.id;
  const time = [pega(1), pega(2), pega(3)];
  if (new Set(time).size < 3) continue;
  const jornada: RunBattleSummary[] = [];
  const vistos: string[] = j % 3 === 0 ? [] : characters.slice(0, 60).map((c) => c.id);

  for (let indice = 0; indice < 10; indice += 1) {
    const inimigos = [pega(indice + 4), pega(indice + 5), pega(indice + 6)];
    if (new Set([...time, ...inimigos]).size < 6) continue;
    const b = createBattle(time, inimigos, j * 10 + indice);
    let feitos = feitosVazios(), raioX = raioXVazio(), visto = 0, maiorAtraso = 0;
    for (let p = 0; p < 4200 && !b.finished; p += 1) {
      stepBattle(b);
      maiorAtraso = Math.max(maiorAtraso, -b.dominion);
      const novos = b.events.filter((e) => e.id > visto);
      if (novos.length) {
        visto = Math.max(...novos.map((e) => e.id));
        feitos = acumularFeitos(feitos, novos, b);
        raioX = acumularRaioX(raioX, novos, b);
      }
    }
    const venceu = b.winner === 'player';
    const ctx: Contexto = {
      battle: b, feitos: fecharFeitos(feitos, b, maiorAtraso >= 8), raioX, time, venceu,
      campeao: venceu && indice === 9, maiorAtraso: Math.round(maiorAtraso), indice,
      jornada, vistos, dominados: j % 7 === 0 ? 12 : j % 5 === 0 ? 1 : 0,
    };
    total += 1;
    for (const id of conquistasDaBatalha(ctx, [])) vezes.set(id, (vezes.get(id) ?? 0) + 1);
    jornada.push(summarizeBattle(indice, b));
    if (!venceu) break;
  }
}

console.log(`${String(total)} lutas · ${String(conquistas.length)} conquistas\n`);
const nunca: string[] = [], sempre: string[] = [];
for (const c of conquistas) {
  const n = vezes.get(c.id) ?? 0, pct = n / total * 100;
  if (n === 0) nunca.push(c.nome);
  else if (pct > 80) sempre.push(`${c.nome} (${pct.toFixed(0)}%)`);
  const barra = '#'.repeat(Math.min(30, Math.round(pct / 2)));
  console.log(`  ${c.nome.padEnd(26)}${String(n).padStart(5)}  ${pct.toFixed(1).padStart(5)}%  ${barra}`);
}
console.log();
if (nunca.length) console.log(`NUNCA aconteceram (${String(nunca.length)}): ${nunca.join(', ')}`);
if (sempre.length) console.log(`acontecem quase sempre: ${sempre.join(', ')}`);
if (!nunca.length && !sempre.length) console.log('todas alcançáveis, nenhuma banal.');

/* ---------------------------------------------------------------------------
 * Cenários construídos
 * ------------------------------------------------------------------------- */

/*
 * O sorteio aleatório não alcança tudo, e isso não quer dizer que seja
 * impossível: um trio sorteado quase nunca é do mesmo universo, nem tem três
 * curandeiros, nem chega aos 250 personagens vistos. Essas conquistas são
 * para o jogador que **escolhe** — então a prova precisa escolher também.
 */
import { byId } from '../src/data/characters';

const jogar = (time: string[], inimigos: string[], semente: number) => {
  const b = createBattle(time, inimigos, semente);
  let feitos = feitosVazios(), raioX = raioXVazio(), visto = 0, maiorAtraso = 0;
  for (let p = 0; p < 4200 && !b.finished; p += 1) {
    stepBattle(b);
    maiorAtraso = Math.max(maiorAtraso, -b.dominion);
    const novos = b.events.filter((e) => e.id > visto);
    if (novos.length) {
      visto = Math.max(...novos.map((e) => e.id));
      feitos = acumularFeitos(feitos, novos, b);
      raioX = acumularRaioX(raioX, novos, b);
    }
  }
  return { battle: b, feitos: fecharFeitos(feitos, b, maiorAtraso >= 8), raioX, maiorAtraso: Math.round(maiorAtraso), venceu: b.winner === 'player' };
};

const base = (extra: Partial<Contexto>): Contexto => ({
  battle: extra.battle!, feitos: extra.feitos ?? {}, raioX: extra.raioX ?? raioXVazio(),
  time: extra.time ?? [], venceu: extra.venceu ?? false, campeao: extra.campeao ?? false,
  maiorAtraso: extra.maiorAtraso ?? 0, indice: extra.indice ?? 0, jornada: extra.jornada ?? [],
  vistos: extra.vistos ?? [], dominados: extra.dominados ?? 0,
});

const alcancadas = new Set<string>();
const tentar = (ctx: Contexto) => { for (const id of conquistasDaBatalha(ctx, [])) alcancadas.add(id); };

/* Um trio de curandeiros cura muito mais do que qualquer sorteio produziria. */
for (let s = 1; s <= 40; s += 1) {
  const r = jogar(['sakura', 'sailormoon', 'groot'], ['vegeta', 'raven', 'hulk'], s);
  tentar(base({ ...r, time: ['sakura', 'sailormoon', 'groot'] }));
}

/* Três do mesmo universo: o jogador escolhe, o sorteio não. */
const porUniverso = new Map<string, string[]>();
for (const c of characters) porUniverso.set(c.universe, [...(porUniverso.get(c.universe) ?? []), c.id]);
const grande = [...porUniverso.values()].sort((a, b) => b.length - a.length)[0]!;
for (let s = 1; s <= 40; s += 1) {
  const time = [grande[0]!, grande[1]!, grande[2]!];
  const r = jogar(time, ['pikachu', 'raven', 'inosuke'], s);
  tentar(base({ ...r, time }));
}

/* Lutas longas, com trios resistentes dos dois lados. */
const duros = [...characters].sort((a, b) => b.hp - a.hp).slice(0, 6).map((c) => c.id);
for (let s = 1; s <= 40; s += 1) {
  const time = duros.slice(0, 3);
  const r = jogar(time, duros.slice(3, 6), s);
  tentar(base({ ...r, time }));
}

/* Coleção e jornada perfeita: contadores que o tempo resolve, verificados pela regra. */
{
  const r = jogar(['goku', 'pikachu', 'gojo'], ['vegeta', 'raven', 'hulk'], 1);
  const batalha = r.battle;
  const todos = characters.map((c) => c.id);
  tentar(base({ ...r, time: ['goku', 'pikachu', 'gojo'], vistos: todos, dominados: 15 }));
  const perfeita: RunBattleSummary[] = Array.from({ length: 9 }, (_, i) => ({
    ...summarizeBattle(i, batalha), survivors: 3, won: true,
  }));
  const vivos = { ...batalha, fighters: batalha.fighters.map((f) => f.side === 'player' ? { ...f, hp: f.maxHp } : f) };
  tentar(base({ battle: vivos, feitos: r.feitos, raioX: r.raioX, time: ['goku', 'pikachu', 'gojo'],
    venceu: true, campeao: true, indice: 9, jornada: perfeita, vistos: todos, dominados: 15 }));
  /* E a jornada em que alguém caiu pelo caminho. */
  const tropecou = perfeita.map((b, i) => i === 3 ? { ...b, survivors: 2 } : b);
  tentar(base({ battle: vivos, feitos: r.feitos, raioX: r.raioX, time: ['goku', 'pikachu', 'gojo'],
    venceu: true, campeao: true, indice: 9, jornada: tropecou, vistos: todos, dominados: 15 }));
}

void byId;
const faltam = conquistas.filter((c) => !alcancadas.has(c.id) && (vezes.get(c.id) ?? 0) === 0);
console.log(`\ncenários construídos: ${String(alcancadas.size)} conquistas alcançadas`);
if (faltam.length) {
  console.log(`\nAINDA IMPOSSÍVEIS (${String(faltam.length)}):`);
  for (const c of faltam) console.log(`  ${c.nome} — ${c.dica}`);
  process.exitCode = 1;
} else {
  console.log('todas as 52 são alcançáveis: nenhuma ficou sem prova.');
  process.exitCode = 0;
}
