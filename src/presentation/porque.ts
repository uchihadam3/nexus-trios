/*
 * O porquê de cada combinação, com as habilidades de verdade.
 *
 * Pedido do jogador: "essa dica é pra ajudar a pessoa a aprender… tem que
 * falar por quê… vai ajudar o Professor nisso, vai fazer o Omni-Man nisso".
 * A dica curta diz quem ajuda quem; tocando em "Por quê?", esta frase mostra
 * COM QUÊ: a habilidade de um que liga a habilidade do outro.
 */
import { byId } from '../data/characters';
import { DEIXAM_VULNERAVEL, statuses } from '../data/statuses';
import type { Character, Effect, StatusId, Target } from '../engine/types';

const ALIADOS: Target[] = ['allAllies', 'allyWeak'];
const RIVAIS: Target[] = ['enemyWeak', 'enemyStrong', 'enemyCast', 'investigated', 'leastInvestigated', 'allEnemies', 'randomEnemy'];
const PRENDE: StatusId[] = ['paralyzed', 'frozen', 'sleep', 'rooted', 'slow', 'confused', 'silenced', 'weakened', 'blind'];
const REFORCO: StatusId[] = ['strengthened', 'haste', 'protected', 'regen'];

const nome = (id: string) => byId[id]!.name.split(/[ ,]/)[0]!;
const vida = (id: string) => byId[id]!.hp.toLocaleString('pt-BR');
const nomeDoStatus = (s: StatusId) => statuses[s].name;

interface Fonte { nome: string; status?: StatusId }
/* A primeira habilidade (ou o traço, ou o básico) que faz `pred`. */
function fonte(c: Character, pred: (e: Effect, alvo: Target) => boolean): Fonte | undefined {
  for (const s of c.skills) for (const e of s.effects) if (pred(e, e.target ?? s.target)) return { nome: s.name, ...(e.kind === 'status' ? { status: e.status } : {}) };
  for (const e of c.trait.effects) if (pred(e, e.target ?? c.trait.target)) return { nome: c.trait.name, ...(e.kind === 'status' ? { status: e.status } : {}) };
  for (const e of c.basic.effects) if (pred(e, e.target ?? c.basic.target)) return { nome: c.basic.name, ...(e.kind === 'status' ? { status: e.status } : {}) };
  return undefined;
}
const danoDe = (c: Character, i: number) => c.skills[i]!.effects.reduce((n, e) => n + (e.kind === 'damage' ? e.value : 0), 0);
const golpeForte = (c: Character) => c.skills.map((s, i) => ({ s, d: danoDe(c, i) })).sort((a, b) => b.d - a.d)[0]!.s.name;
const golpeGrande = (c: Character) => (c.skills.find((s) => s.preparation >= 2) ?? c.skills.find((s) => s.effects.some((e) => e.kind === 'damage' && e.value >= 400)))?.name ?? golpeForte(c);

/** A frase do porquê: o que A faz, com qual habilidade, e o que isso liga em B. */
export function porQue(chave: string, a: string, b: string): string | undefined {
  const A = nome(a), B = nome(b), ca = byId[a]!, cb = byId[b]!;
  const aliado = (alvo: Target) => ALIADOS.includes(alvo), rival = (alvo: Target) => RIVAIS.includes(alvo);
  switch (chave) {
    case 'carga-golpe': {
      const f = fonte(ca, (e, alvo) => e.kind === 'charge' && aliado(alvo));
      return f && `${f.nome} de ${A} enche a Carga do trio — e ${golpeGrande(cb)}, o golpe grande de ${B}, sai mais cedo`;
    }
    case 'abre-vulneravel': {
      const f = fonte(ca, (e, alvo) => e.kind === 'status' && DEIXAM_VULNERAVEL.includes(e.status) && rival(alvo));
      const s = cb.skills.find((x) => x.condition === 'vulnerable');
      return f && s && `${f.nome} de ${A} deixa o rival ${nomeDoStatus(f.status!)} — e ${s.name} de ${B} só sai com um rival vulnerável`;
    }
    case 'abre-ferido': {
      const s = cb.skills.find((x) => x.condition === 'injured');
      return s && `${A} fere os rivais com ${golpeForte(ca)} — e ${s.name} de ${B} só sai em alvo ferido`;
    }
    case 'cuida-fragil': {
      const f = fonte(ca, (e, alvo) => (e.kind === 'heal' || e.kind === 'shield') && aliado(alvo));
      return f && `${B} tem só ${vida(b)} de Vida; ${f.nome} de ${A} cura ou dá Escudo a quem está em perigo`;
    }
    case 'reforca-forte': {
      const f = fonte(ca, (e, alvo) => e.kind === 'status' && REFORCO.includes(e.status) && aliado(alvo));
      return f && `${f.nome} de ${A} deixa o trio ${nomeDoStatus(f.status!)} — e ${B} já bate forte com ${golpeForte(cb)}`;
    }
    case 'adianta-golpe': {
      const f = fonte(ca, (e, alvo) => e.kind === 'shift' && ((aliado(alvo) && e.value > 0) || (rival(alvo) && e.value < 0)));
      return f && `${f.nome} de ${A} ganha tempo para o trio — e ${golpeGrande(cb)} de ${B} sai antes`;
    }
    case 'protege-vinganca': {
      const f = fonte(ca, (e, alvo) => (e.kind === 'heal' || e.kind === 'shield') && aliado(alvo));
      if (!f) return undefined;
      // a força dele vem do traço (apanhar, aliado ferido, perdendo) ou de uma habilidade que só sai sob ameaça
      const doTraco = ['received', 'allyHurt', 'losing', 'survived'].includes(cb.trait.on);
      const ameaca = cb.skills.find((x) => x.condition === 'threatened');
      const cresce = doTraco ? `${cb.trait.name} de ${B} cresce quando a luta aperta` : ameaca ? `${ameaca.name} de ${B} sai quando o trio está sob ameaça` : `${B} cresce quando a luta aperta`;
      return `${cresce}; ${f.nome} de ${A} mantém ${B} de pé para isso`;
    }
    case 'controla-dano': {
      const f = fonte(ca, (e, alvo) => ((e.kind === 'status' && PRENDE.includes(e.status)) || e.kind === 'interrupt') && rival(alvo));
      if (!f) return undefined;
      const como = f.status ? `deixa os rivais ${nomeDoStatus(f.status)}` : 'corta os Preparos rivais';
      return `${f.nome} de ${A} ${como} — enquanto isso, ${B} bate com ${golpeForte(cb)}`;
    }
    case 'status-gatilho': {
      const f = fonte(ca, (e, alvo) => e.kind === 'status' && rival(alvo));
      const gatilho = ['status', 'negativeStatus'].includes(cb.trait.on) ? cb.trait.name : cb.skills.find((s) => s.charge.some((r) => r.on === 'status' || r.on === 'negativeStatus'))?.name;
      return f && gatilho && `Cada Status que ${A} põe nos rivais (${f.nome}) carrega ${gatilho} de ${B}`;
    }
    case 'provoca-fragil': {
      const f = fonte(ca, (e) => e.kind === 'status' && e.status === 'provoked');
      return f && `${f.nome} de ${A} provoca os rivais e puxa para ele os golpes que iriam em ${B} (só ${vida(b)} de Vida)`;
    }
    case 'levanta-forte': {
      const f = fonte(ca, (e) => e.kind === 'revive');
      return f && `Se ${B} cair, ${f.nome} de ${A} o levanta — e ele volta a bater com ${golpeForte(cb)}`;
    }
    case 'limpa-forte': {
      const f = fonte(ca, (e, alvo) => e.kind === 'cleanse' && aliado(alvo));
      return f && `${f.nome} de ${A} tira Paralisado, Lento e outros Status ruins do trio — e ${B} continua batendo com ${golpeForte(cb)}`;
    }
  }
  return undefined;
}
