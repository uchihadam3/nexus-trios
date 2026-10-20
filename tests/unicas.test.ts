import { describe, expect, it } from 'vitest';
import { byId } from '../src/data/characters';
import { createBattle, stepBattle } from '../src/engine/battle';
import { SEGUNDOS_DO_BERSERKER, UNICAS } from '../src/engine/unicas';
import type { Battle, Fighter } from '../src/engine/types';

const roda = (b: Battle, segundos: number, ate?: () => boolean) => {
  for (let t = 0; t < segundos * 10 && !b.finished; t++) { stepBattle(b); if (ate?.()) return; }
};
const lutador = (b: Battle, id: string) => b.fighters.find((f) => f.characterId === id)!;
const golpeFatal = (f: Fighter) => f.hp + 5000;

describe('Mecânicas únicas', () => {
  it('cada uma é de um personagem que existe, com nome e texto próprios', () => {
    const nomes = new Set<string>();
    for (const [id, u] of Object.entries(UNICAS)) {
      expect(byId[id], id).toBeDefined();
      expect(u.nome.length, id).toBeGreaterThan(2);
      expect(u.texto.length, id).toBeGreaterThan(30);
      expect(nomes.has(u.nome), `nome repetido: ${u.nome}`).toBe(false);
      nomes.add(u.nome);
      expect(Object.keys(u.ganchos).length, `${id} sem regra`).toBeGreaterThan(0);
    }
  });

  it('Zoro entra na frente do golpe fatal de um aliado, uma vez por luta', () => {
    // Goku não tem Última resistência: sem o Zoro, cairia
    const b = createBattle(['zoro', 'goku', 'batman'], ['saitama', 'thanos', 'hulk'], 5);
    const goku = lutador(b, 'goku'), zoro = lutador(b, 'zoro'), thanos = lutador(b, 'thanos');
    const antes = goku.hp, zoroAntes = zoro.hp;
    applyDamage(b, thanos, goku, golpeFatal(goku));
    expect(goku.hp).toBe(antes);
    expect(zoro.hp).toBeLessThan(zoroAntes);
    expect(zoro.hp).toBeGreaterThanOrEqual(1);
    expect(b.events.some((e) => e.kind === 'unica' && e.label === 'Nada aconteceu.')).toBe(true);
    // a segunda vez já não salva
    applyDamage(b, thanos, goku, golpeFatal(goku));
    expect(goku.hp).toBe(0);
  });

  it('Light escreve um nome na página do relógio quando fica com pouca Vida, uma vez por luta', () => {
    const b = createBattle(['light', 'goku', 'batman'], ['naruto', 'thanos', 'hulk'], 9);
    const light = lutador(b, 'light'), naruto = lutador(b, 'naruto');
    light.investigation[naruto.uid] = 60;
    roda(b, 1);
    expect(naruto.hp).toBeGreaterThan(0);
    light.hp = Math.round(light.maxHp * 0.2);
    stepBattle(b);
    expect(naruto.hp).toBe(0);
    expect(b.events.some((e) => e.kind === 'unica' && e.label === 'Página no relógio')).toBe(true);
    // só uma vez por luta
    const thanos = lutador(b, 'thanos');
    light.investigation[thanos.uid] = 99;
    const vidaThanos = thanos.hp;
    stepBattle(b);
    expect(thanos.hp).toBeGreaterThan(vidaThanos - 200);
  });

  it('Vash nunca derruba ninguém', () => {
    const b = createBattle(['vash', 'naruto', 'goku'], ['saitama', 'thanos', 'hulk'], 9);
    const vash = lutador(b, 'vash'), thanos = lutador(b, 'thanos');
    applyDamage(b, vash, thanos, golpeFatal(thanos));
    expect(thanos.hp).toBe(1);
  });

  it('T-800 não pega controle', () => {
    const b = createBattle(['t800', 'naruto', 'goku'], ['saitama', 'thanos', 'hulk'], 9);
    const t800 = lutador(b, 't800'), saitama = lutador(b, 'saitama');
    applyStatus(b, saitama, t800, 'paralyzed');
    applyStatus(b, saitama, t800, 'sleep');
    expect(t800.statuses.some((s) => s.id === 'paralyzed' || s.id === 'sleep')).toBe(false);
    applyStatus(b, saitama, t800, 'exposed');
    expect(t800.statuses.some((s) => s.id === 'exposed')).toBe(true);
  });

  it('Ultron sobe em corpo novo duas vezes e cai na terceira', () => {
    const b = createBattle(['ultron', 'naruto', 'goku'], ['saitama', 'thanos', 'hulk'], 9);
    const ultron = lutador(b, 'ultron'), saitama = lutador(b, 'saitama');
    applyDamage(b, saitama, ultron, golpeFatal(ultron));
    expect(ultron.hp).toBeCloseTo(ultron.maxHp * 0.25, 0);
    applyDamage(b, saitama, ultron, golpeFatal(ultron));
    expect(ultron.hp).toBeGreaterThan(0);
    applyDamage(b, saitama, ultron, golpeFatal(ultron));
    expect(ultron.hp).toBe(0);
  });

  it('Guts segue de pé com a Armadura do Berserker (10 s, pedido do dono) e depois desaba', () => {
    expect(SEGUNDOS_DO_BERSERKER).toBe(10);
    const b = createBattle(['guts', 'naruto', 'goku'], ['saitama', 'thanos', 'hulk'], 9);
    const guts = lutador(b, 'guts'), saitama = lutador(b, 'saitama');
    applyDamage(b, saitama, guts, golpeFatal(guts));
    expect(guts.hp).toBe(1);
    const fim = b.time + SEGUNDOS_DO_BERSERKER;
    roda(b, SEGUNDOS_DO_BERSERKER - 1);
    if (b.time < fim - 0.2) expect(guts.hp).toBeGreaterThan(0);
    roda(b, 3, () => guts.hp <= 0);
    expect(guts.hp).toBe(0);
  });

  it('o que vale para "o trio" vale também para quem tem a mecânica (Magneto, Vampira) e a habilidade em área inteira (Zelda)', () => {
    const motor = { aviso: () => undefined } as never, golpe = { direto: true, label: 'Impacto', habilidade: true, indice: 0 };
    const b = createBattle(['magneto', 'rogue', 'zelda'], ['saitama', 'thanos', 'hulk'], 5);
    const magneto = lutador(b, 'magneto'), vampira = lutador(b, 'rogue'), zelda = lutador(b, 'zelda'), thanos = lutador(b, 'thanos');
    // Atração (o começo): os rivais causam −15% no trio de Magneto, nele também
    expect(UNICAS.magneto!.ganchos.recebe!(motor, b, magneto, thanos, golpe)).toBeCloseTo(0.85);
    // o rival que a Vampira tocou causa −4% no trio dela, nela também
    (vampira.u ??= {})[`toque${b.fighters.indexOf(thanos)}`] = 1;
    expect(UNICAS.rogue!.ganchos.recebe!(motor, b, vampira, thanos, golpe)).toBeCloseTo(0.96);
    // a primeira habilidade de Thanos em área: todos os alvos no mesmo instante levam −40%; a seguinte, não
    expect(UNICAS.zelda!.ganchos.recebe!(motor, b, zelda, thanos, golpe)).toBeCloseTo(0.6);
    expect(UNICAS.zelda!.ganchos.recebeAliado!(motor, b, zelda, magneto, thanos, golpe)).toBeCloseTo(0.6);
    roda(b, 1);
    expect(UNICAS.zelda!.ganchos.recebe!(motor, b, zelda, thanos, golpe)).toBe(1);
  });

  it('o aviso da mecânica aparece na luta', () => {
    const b = createBattle(['predator', 'naruto', 'goku'], ['saitama', 'thanos', 'hulk'], 9);
    expect(b.events.some((e) => e.kind === 'unica' && e.label === 'Camuflado')).toBe(true);
  });

  it('a luta com mecânicas continua salvável e retoma igual', () => {
    const ids = Object.keys(UNICAS);
    for (let i = 0; i + 6 <= ids.length; i += 6) {
      const a = ids.slice(i, i + 3), r = ids.slice(i + 3, i + 6);
      const b = createBattle(a, r, 77 + i);
      roda(b, 20);
      const copia = JSON.parse(JSON.stringify(b)) as Battle;
      roda(b, 60); roda(copia, 60);
      expect(copia.winner, a.join() + ' × ' + r.join()).toBe(b.winner);
      expect(copia.time).toBeCloseTo(b.time, 6);
    }
  });
});

/* Aplica dano e Status pelo caminho normal do motor (uma habilidade de mentira com o efeito). */
import { applyEffects } from '../src/engine/battle';
function applyDamage(b: Battle, fonte: Fighter, alvo: Fighter, valor: number) {
  applyEffects(b, fonte, [alvo], [{ kind: 'damage', value: valor / Math.max(0.01, 1) }]);
}
function applyStatus(b: Battle, fonte: Fighter, alvo: Fighter, status: 'paralyzed' | 'sleep' | 'exposed') {
  applyEffects(b, fonte, [alvo], [{ kind: 'status', status, value: 0.3, duration: 4 }]);
}
