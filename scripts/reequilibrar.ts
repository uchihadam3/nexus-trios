/*
 * O reequilíbrio dos buffs e debuffs (src/data/reequilibrio.ts): para cada personagem, mede quanto o trio dele vence e
 * quanto cada efeito contínuo rende por luta; os que rendem pouco sobem até a meta do tipo (com os pisos de Escudo, cura e
 * Fortalecido), e o dano direto (ou a Vida, se o que ganhou só protege ou cura) cai até ele vencer o mesmo tanto de antes,
 * nas mesmas lutas (mesmos parceiros, rivais e sementes).
 *
 * Uso (várias partes em paralelo; retoma de onde parou, pulando quem já está nos arquivos de saída):
 *   npx tsx scripts/reequilibrar.ts <parte> <partes> <lutas> <saida.jsonl> [outras saídas para pular…]
 * Cada linha: {id, antes, depois, mult, dano?, vida?, rende: {tipo: [antes, depois]}}
 */
import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { antesDoReequilibrio, byId } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { reequilibra, type Reequilibrio } from '../src/data/reequilibrio';
import type { Character } from '../src/engine/types';

const [parte, partes, LUTAS] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const saida = process.argv[5]!, todas = process.argv.slice(5);
const feitos = new Set(todas.filter(existsSync).flatMap((f) => readFileSync(f, 'utf8').split('\n').filter(Boolean).map((l) => (JSON.parse(l) as { id: string }).id)));

/* Quanto cada efeito contínuo tem que render por luta (os bons do mesmo tipo rendem isso ou mais). */
const META: Record<string, number> = { bleed: 100, burning: 70, poison: 70, bomb: 80, thorns: 50, summon: 70, regen: 90 };
const ATACA = new Set(['bleed', 'burning', 'poison', 'bomb', 'thorns', 'summon', 'strengthened', 'haste', 'weakened', 'exposed', 'marked', 'slow', 'rooted', 'electric', 'cursed', 'blind', 'confused', 'reflect', 'vampirism']);
const STEP = 0.1, ids = antesDoReequilibrio.map((c) => c.id);
for (const c of antesDoReequilibrio) byId[c.id] = c;

function medir(id: string, ficha: Character, n: number) {
  byId[id] = ficha;
  let r = (ids.indexOf(id) * 2654435761 + 12345) >>> 0;
  const rnd = () => ((r = (Math.imul(r, 1103515245) + 12345) >>> 0) / 2 ** 32);
  const pega = (fora: string[]) => { let x; do x = ids[Math.floor(rnd() * ids.length)]!; while (fora.includes(x)); return x; };
  const rende: Record<string, number> = Object.fromEntries(Object.keys(META).map((k) => [k, 0]));
  let vit = 0, total = 0;
  for (let k = 0; k < n; k++) {
    const t = [id]; t.push(pega(t)); t.push(pega(t)); const o: string[] = []; while (o.length < 3) o.push(pega([...t, ...o]));
    const embaixo = k % 2 === 0, seed = Math.floor(rnd() * 2 ** 31);
    const b = embaixo ? createBattle(t, o, seed, 1) : createBattle(o, t, seed, 1);
    const f = b.fighters.find((x) => x.side === (embaixo ? 'player' : 'enemy') && x.characterId === id)!;
    for (let s = 0; s < 9000 && !b.finished; s++) {
      for (const x of b.fighters) if (x.hp > 0) for (const st of x.statuses) if (st.source === f.uid) {
        if (st.id === 'burning' || st.id === 'poison') rende[st.id]! += st.intensity * STEP;
        if (st.id === 'regen') rende.regen! += Math.min(st.intensity * STEP, Math.max(0, x.maxHp - x.hp));
      }
      const ev = b.nextEvent; stepBattle(b);
      for (const e of b.events) if (e.id >= ev && e.source === f.uid) {
        if (e.kind === 'damage' && e.label === 'Sangramento') rende.bleed! += e.value ?? 0;
        else if (e.kind === 'damage' && e.label === 'Explosão') rende.bomb! += e.value ?? 0;
        else if (e.kind === 'damage' && e.label === 'Espinhos') rende.thorns! += e.value ?? 0;
        else if (e.kind === 'summon') rende.summon! += e.value ?? 0;
      }
    }
    if (!b.finished) continue;
    total++; if ((b.winner === 'player') === embaixo) vit++;
  }
  byId[id] = antesDoReequilibrio.find((c) => c.id === id)!;
  for (const k of Object.keys(rende)) rende[k] = Math.round(rende[k]! / n);
  return { taxa: vit / total, rende };
}

const usa = (c: Character) => new Set([c.basic, c.trait, ...c.skills].flatMap((x) => x.effects).flatMap((e) => (e.kind === 'status' ? [e.status] : [])));
for (let i = parte; i < ids.length; i += partes) {
  const id = ids[i]!; if (feitos.has(id) || (process.env.SO && !process.env.SO.split(',').includes(id))) continue;
  const c = antesDoReequilibrio[i]!, tem = usa(c);
  const base = medir(id, c, LUTAS);
  const mult: Record<string, number> = {};
  for (const [tipo, meta] of Object.entries(META)) if (tem.has(tipo as never) && base.rende[tipo]! < meta) mult[tipo] = Math.round(Math.min(6, meta / Math.max(1, base.rende[tipo]!)) * 100) / 100;
  const ficha = (a: Reequilibrio) => reequilibra(c, a);
  const sem = JSON.stringify(c) === JSON.stringify(ficha({ mult }));
  if (sem) { appendFileSync(saida, JSON.stringify({ id, antes: base.taxa, depois: base.taxa, mult: {}, rende: {} }) + '\n'); continue; }
  // o que ele ganhou: ataque (corta o dano direto) ou proteção e cura (corta a Vida)
  const melhorado = ficha({ mult }), ganhos = new Set<string>(Object.keys(mult));
  [c.basic, c.trait, ...c.skills].forEach((x, k) => x.effects.forEach((e, j) => { const d = [melhorado.basic, melhorado.trait, ...melhorado.skills][k]!.effects[j]!; if (JSON.stringify(d) !== JSON.stringify(e)) ganhos.add(e.kind === 'status' ? e.status : e.kind); }));
  const alavanca: 'dano' | 'vida' = [...ganhos].some((g) => ATACA.has(g)) ? 'dano' : 'vida';
  const com = (v: number) => ficha({ mult, [alavanca]: v });
  let x0 = 1, y0 = medir(id, com(1), LUTAS).taxa - base.taxa, x = x0, y = y0;
  if (Math.abs(y0) > 0.008) {
    let x1 = y0 > 0 ? 0.9 : 1.1, y1 = medir(id, com(x1), LUTAS).taxa - base.taxa;
    for (let it = 0; it < 3 && Math.abs(y1) > 0.008; it++) {
      const nx = Math.min(1.3, Math.max(0.7, Math.abs(y1 - y0) < 1e-4 ? x1 + (y1 > 0 ? -0.1 : 0.1) : x1 - (y1 * (x1 - x0)) / (y1 - y0)));
      x0 = x1; y0 = y1; x1 = Math.round(nx * 1000) / 1000; y1 = medir(id, com(x1), LUTAS).taxa - base.taxa;
    }
    x = x1; y = y1;
  }
  // o corte chegou no limite e ele ainda vence bem mais: o piso inteiro era demais para ele (cura ou buff no trio todo)
  let piso = 1;
  for (const p of [0.5, 0.25, 0]) {
    if (Math.abs(y) <= 0.015) break;
    piso = p;
    const comPiso = (v: number) => ficha({ mult, piso, [alavanca]: v });
    let a0 = 1, b0 = medir(id, comPiso(1), LUTAS).taxa - base.taxa;
    x = 1; y = b0;
    if (Math.abs(b0) > 0.008) {
      let a1 = b0 > 0 ? 0.9 : 1.1, b1 = medir(id, comPiso(a1), LUTAS).taxa - base.taxa;
      for (let it = 0; it < 3 && Math.abs(b1) > 0.008; it++) {
        const nx = Math.min(1.3, Math.max(0.7, Math.abs(b1 - b0) < 1e-4 ? a1 + (b1 > 0 ? -0.1 : 0.1) : a1 - (b1 * (a1 - a0)) / (b1 - b0)));
        a0 = a1; b0 = b1; a1 = Math.round(nx * 1000) / 1000; b1 = medir(id, comPiso(a1), LUTAS).taxa - base.taxa;
      }
      x = a1; y = b1;
    }
  }
  const final = (v: number) => ficha({ mult, ...(piso < 1 ? { piso } : {}), [alavanca]: v });
  const fim = medir(id, final(x), Math.min(LUTAS, 600));
  appendFileSync(saida, JSON.stringify({ id, antes: base.taxa, depois: base.taxa + y, mult, [alavanca]: x, ...(piso < 1 ? { piso } : {}), rende: Object.fromEntries(Object.keys(META).filter((k) => tem.has(k as never)).map((k) => [k, [base.rende[k], fim.rende[k]]])) }) + '\n');
}
