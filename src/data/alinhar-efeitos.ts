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

/** Aplica o alinhamento ao traço, ao ataque básico e às três habilidades. */
export const alinharEfeitos = (c: Character): Character => ({
  ...c,
  trait: { ...c.trait, effects: alinhar(c.trait.effects, c.trait.target) },
  basic: { ...c.basic, effects: alinhar(c.basic.effects, c.basic.target) },
  /* O tipo guarda exatamente três habilidades, então a tupla é remontada como tupla. */
  skills: c.skills.map((s) => ({ ...s, effects: alinhar(s.effects, s.target) })) as [Skill, Skill, Skill],
});
