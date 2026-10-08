/*
 * O alvo que o efeito herda nem sempre é o alvo que ele quer.
 *
 * Quando um efeito não declara alvo próprio, o motor o aplica em quem a
 * habilidade escolheu: `applyEffects` faz `effect.target ? targets(...) :
 * selected`. Para uma habilidade de ataque isso é exatamente o certo — o dano
 * e o debuff caem em quem foi mirado.
 *
 * Para uma habilidade de **apoio**, é o contrário. Quem escreveu "Byakugou"
 * mirou `allAllies` para a cura e o buff chegarem ao trio, e pôs um
 * `damage(306)` junto sem alvo próprio. O dano herdou `allAllies`: 306 de dano
 * no próprio time, toda vez que a habilidade saía. O mesmo com o Piccolo, que
 * marcava e enfraquecia o aliado que estava tentando defender.
 *
 * Medido em 30 lutas com Sakura, Piccolo e Ichigo juntos: 71 golpes no próprio
 * time, 16.158 de dano, 46 debuffs em aliado. Não é caso raro — são 80 efeitos
 * em 250 personagens, todos no mesmo sentido, porque o descuido é sempre o
 * mesmo: habilidade de apoio com um efeito ofensivo junto.
 *
 * A ficha nunca prometeu isso. Ela diz "306 de dano", e ninguém lê isso como
 * "no meu próprio trio".
 *
 * Então: efeito ofensivo sem alvo próprio, numa parte que mira aliados, passa
 * a mirar inimigo explicitamente. Nada se move no sentido contrário — não
 * existe nenhum caso de cura ou buff herdando alvo inimigo, e se existisse
 * seria a mesma correção espelhada.
 */
import type { Character, Effect, Skill, Target } from '../engine/types';
import { statuses } from './statuses';

const ALIADOS = new Set<Target>(['self', 'allyWeak', 'allAllies']);

/** Dano, interrupção e Status negativo: coisas que ninguém faz no próprio time. */
const ofensivo = (e: Effect): boolean =>
  e.kind === 'damage' || e.kind === 'interrupt'
  || (e.kind === 'status' && statuses[e.status].tone === 'negativo');

/*
 * Para onde o efeito ofensivo vai.
 *
 * `enemyWeak` é o alvo padrão do jogo — é o que o ataque básico de todo mundo
 * usa. Uma habilidade de apoio não escolheu inimigo nenhum, então o dano junto
 * dela segue a mesma regra do ataque básico em vez de inventar uma mira nova.
 */
const ALVO_OFENSIVO: Target = 'enemyWeak';

const alinhar = (effects: readonly Effect[], alvoDaParte: Target): Effect[] => effects.map((e) => {
  let saida = e;
  /* 1 · o efeito ofensivo não cai mais no próprio time. */
  if (saida.target === undefined && ALIADOS.has(alvoDaParte) && ofensivo(saida)) {
    saida = { ...saida, target: ALVO_OFENSIVO };
  }
  /*
   * 2 · e a ficha não anuncia mais do que o motor aceita.
   *
   * `applyStatus` fecha a intensidade no teto do Status. Uma aplicação escrita
   * acima do teto vira um número que aparece na ficha e nunca acontece.
   */
  if (saida.kind === 'status') {
    const teto = statuses[saida.status].cap;
    if (saida.value > teto) saida = { ...saida, value: teto };
  }
  return saida;
});

/*
 * 3 · o mesmo efeito duas vezes vira um só.
 *
 * Uma rodada antiga de balanceamento reforçou algumas habilidades somando um
 * efeito pequeno ao lado do grande, em vez de aumentar o número: a Rosquinha
 * do Homer mostrava "Guarda 150 de energia" e logo abaixo "Guarda 12 de
 * energia". Eram 11 casos em 250 personagens (energia, Escudo, cura, ritmo e
 * um dano). Para esses tipos, somar dá o mesmo resultado na luta — energia e
 * cura somam, o Escudo tem o mesmo teto, o ritmo é limitado do mesmo jeito —
 * e a ficha passa a mostrar uma linha só, com o total.
 */
const SOMAVEIS = new Set<Effect['kind']>(['damage', 'heal', 'shield', 'store', 'shift']);
const chave = (e: Effect, alvo: Target) => [e.kind, e.target ?? alvo, e.kind === 'store' ? e.cap : '', 'value' in e ? Math.sign(e.value) : ''].join('|');
const juntarRepetidos = (effects: readonly Effect[], alvoDaParte: Target): Effect[] => {
  const saida: Effect[] = [];
  for (const e of effects) {
    const igual = SOMAVEIS.has(e.kind) ? saida.findIndex((x) => chave(x, alvoDaParte) === chave(e, alvoDaParte)) : -1;
    const anterior = saida[igual];
    if (anterior && 'value' in anterior && 'value' in e) saida[igual] = { ...anterior, value: Math.round((anterior.value + e.value) * 1000) / 1000 } as Effect;
    else saida.push(e);
  }
  return saida;
};
const arrumar = (effects: readonly Effect[], alvo: Target) => juntarRepetidos(alinhar(effects, alvo), alvo);

/*
 * 4 · condição que o próprio personagem consegue criar.
 *
 * "Usa quando um inimigo estiver vulnerável" exige alguém Exposto, Marcado,
 * Paralisado, Eletrificado ou Queimando. Quatro personagens tinham essa
 * condição sem aplicar nenhum desses Status — a Forma perfeita do Cell ficava
 * pronta e parada até ele cair, esperando um aliado que talvez nem existisse.
 * Para eles a condição sai; o Preparo que a habilidade já tem continua sendo
 * o custo do golpe.
 */
const DEIXA_VULNERAVEL = new Set(['exposed', 'marked', 'paralyzed', 'electric', 'burning']);
const condicaoAlcancavel = (c: Character): Character => {
  const todos = [...c.trait.effects, ...c.basic.effects, ...c.skills.flatMap((s) => s.effects)];
  const cria = todos.some((e) => e.kind === 'status' && DEIXA_VULNERAVEL.has(e.status));
  if (cria) return c;
  return { ...c, skills: c.skills.map((s) => (s.condition === 'vulnerable' ? { ...s, condition: 'always' as const, preparation: Math.max(s.preparation, 1.2) } : s)) as [Skill, Skill, Skill] };
};

/*
 * 5 · habilidade que quase nunca enchia.
 *
 * Medido em 2.000 lutas, só com quem ficou vivo 30 s ou mais: seis
 * habilidades não saíam em mais da metade das lutas, porque a Carga delas vem
 * de algo que o próprio personagem quase não faz — a Carga máxima do Mega Man
 * enche ao bloquear dano, e ele não tem Escudo. Os cinco personagens venciam
 * de 32% a 41%. Um pouco mais de Carga pelo tempo faz a habilidade aparecer.
 */
const CARGA_EXTRA_POR_TEMPO: Record<string, Partial<Record<0 | 1 | 2, number>>> = {
  vision: { 1: 1.2, 2: 1.4 }, gordon: { 2: 1.2 }, megaman: { 2: 1.2 }, inosuke: { 0: 1.2 }, vegeta: { 1: 1.2 }, aquaman: { 2: 1 },
};
const cargaQueEnche = (c: Character): Character => {
  const extra = CARGA_EXTRA_POR_TEMPO[c.id];
  if (!extra) return c;
  return { ...c, skills: c.skills.map((s, i) => {
    const mais = extra[i as 0 | 1 | 2];
    if (!mais) return s;
    const temTempo = s.charge.some((r) => r.on === 'time');
    const charge = temTempo ? s.charge.map((r) => (r.on === 'time' ? { ...r, amount: Math.round((r.amount + mais) * 10) / 10 } : r)) : [...s.charge, { on: 'time' as const, amount: mais }];
    return { ...s, charge };
  }) as [Skill, Skill, Skill] };
};

/*
 * 6 · toda habilidade tem Preparo.
 *
 * Pedido do jogador: o nome da habilidade aparece no Preparo, e uma habilidade
 * instantânea passava rápido demais para ser lida. As que não tinham Preparo
 * passam a ter 0,5 s — pouco o bastante para quase não mudar a luta, e o
 * suficiente para o nome aparecer antes do golpe.
 */
const PREPARO_MINIMO = 0.5;
const comPreparo = (c: Character): Character => ({
  ...c, skills: c.skills.map((s) => (s.preparation < PREPARO_MINIMO ? { ...s, preparation: PREPARO_MINIMO } : s)) as [Skill, Skill, Skill],
});

/** Aplica o alinhamento ao traço, ao ataque básico e às três habilidades. */
export const alinharEfeitos = (c0: Character): Character => {
  const c = comPreparo(cargaQueEnche(condicaoAlcancavel(c0)));
  return {
  ...c,
  trait: { ...c.trait, effects: arrumar(c.trait.effects, c.trait.target) },
  basic: { ...c.basic, effects: arrumar(c.basic.effects, c.basic.target) },
  /* O tipo guarda exatamente três habilidades, então a tupla é remontada como tupla. */
  skills: c.skills.map((s) => ({ ...s, effects: arrumar(s.effects, s.target) })) as [Skill, Skill, Skill],
  };
};
