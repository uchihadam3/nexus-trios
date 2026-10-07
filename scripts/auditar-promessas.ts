/*
 * Tudo que a ficha promete e o combate não entrega.
 *
 * O caso que abriu esta auditoria: a Tempestade mostrava "Aplica Lento 20% por
 * 6 s" e "Aplica Lento 5% por 4 s" na mesma habilidade, nos mesmos inimigos. O
 * motor resolve Status de renovação por `Math.max` nos dois campos, então a
 * segunda linha não mudava nada. Linha morta.
 *
 * Esse não é um defeito isolado, é uma família: toda vez que o número na ficha
 * e o número que o motor usa divergem, o jogador decide com informação falsa.
 * Este script cobre as formas que consigo verificar por leitura dos dados.
 *
 * Sai com código 1 se achar qualquer coisa.
 */
import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import type { Character, Effect, Target } from '../src/engine/types';

interface Achado { tipo: string; quem: string; onde: string; detalhe: string }
const achados: Achado[] = [];
const anotar = (tipo: string, quem: string, onde: string, detalhe: string) => achados.push({ tipo, quem, onde, detalhe });

const ALIADOS: readonly Target[] = ['self', 'allyWeak', 'allAllies'];
const ehAliado = (t: Target) => ALIADOS.includes(t);

/** Traço, básico e as três habilidades, cada um com o alvo que o rege. */
const partesDe = (c: Character) => [
  { onde: `traço "${c.trait.name}"`, effects: c.trait.effects as readonly Effect[], alvo: c.trait.target },
  { onde: 'ataque básico', effects: c.basic.effects as readonly Effect[], alvo: c.basic.target },
  ...c.skills.map((s) => ({ onde: `"${s.name}"`, effects: s.effects as readonly Effect[], alvo: s.target })),
];

for (const c of characters) {
  for (const { onde, effects, alvo } of partesDe(c)) {
    const aplicados = effects.flatMap((e, i) =>
      e.kind === 'status' ? [{ i, e, alvo: e.target ?? alvo }] : []);

    for (const { i, e, alvo: alvoReal } of aplicados) {
      const def = statuses[e.status];

      /* 1 · dominada: o motor já guardou um valor maior e mais longo. */
      if (def.stack !== 'add') {
        const dominante = aplicados.find((o) =>
          o.i !== i && o.e.status === e.status && o.alvo === alvoReal &&
          o.e.value >= e.value && o.e.duration >= e.duration &&
          (o.e.value > e.value || o.e.duration > e.duration || o.i < i));
        if (dominante) {
          anotar('linha morta', c.name, onde,
            `${def.name} ${String(e.value)}/${String(e.duration)}s não faz nada: já aplica ${String(dominante.e.value)}/${String(dominante.e.duration)}s em ${alvoReal}`);
        }
      }

      /* 2 · acima do teto: a ficha anuncia um número que o motor corta. */
      if (e.value > def.cap) {
        anotar('passa do teto', c.name, onde,
          `${def.name} anuncia ${String(e.value)}, mas o teto é ${String(def.cap)} — o motor corta`);
      }

      /*
       * 3 · lado errado — mas um custo declarado não é erro.
       *
       * Quinze efeitos ofensivos miram `self` **explicitamente**, e os quinze
       * combinam com a ideia escrita do personagem: o traço da Sailor Moon se
       * chama "Preço do cuidado" e cura o aliado ferindo ela; o Akuma "mata
       * rápido porque não sobrevive a uma luta longa" e fica Exposto ao soltar
       * o Shun Goku Satsu. Isso é desenho, e apagar seria tirar o personagem.
       *
       * A distinção é entre escolher e herdar: mirar `self` é uma decisão de
       * quem escreveu; cair num aliado por falta de alvo próprio é descuido.
       * Ferir o trio inteiro de propósito nunca é custo — é defeito.
       */
      const negativo = def.tone === 'negativo';
      const custoDeclarado = e.target === 'self';
      if (negativo && ehAliado(alvoReal) && !custoDeclarado) {
        anotar('lado errado', c.name, onde, `${def.name} é negativo e cai em ${alvoReal}`);
      }
      if (!negativo && !ehAliado(alvoReal)) {
        anotar('lado errado', c.name, onde, `${def.name} é positivo e cai em ${alvoReal}`);
      }

      /* 4 · sem efeito nenhum. */
      if (e.value <= 0) anotar('valor zero', c.name, onde, `${def.name} com valor ${String(e.value)}`);
      if (e.duration <= 0) anotar('duração zero', c.name, onde, `${def.name} dura ${String(e.duration)}s`);
    }

    /* 5 · cura e escudo em quem não é do time; dano em quem é. */
    for (const e of effects) {
      const alvoReal = e.target ?? alvo;
      if ((e.kind === 'heal' || e.kind === 'shield') && !ehAliado(alvoReal)) {
        anotar('lado errado', c.name, onde, `${e.kind === 'heal' ? 'cura' : 'escudo'} em ${alvoReal}`);
      }
      if (e.kind === 'damage' && ehAliado(alvoReal) && e.target !== 'self') {
        anotar('lado errado', c.name, onde, `dano em ${alvoReal}`);
      }
      if ((e.kind === 'damage' || e.kind === 'heal' || e.kind === 'shield') && e.value <= 0) {
        anotar('valor zero', c.name, onde, `${e.kind} com valor ${String(e.value)}`);
      }
    }
  }

  /* 6 · Carga que não carrega: a habilidade nunca fica pronta. */
  for (const s of c.skills) {
    const total = s.charge.reduce((t, r) => t + r.amount, 0);
    if (total <= 0) anotar('nunca fica pronta', c.name, `"${s.name}"`, 'nenhuma fonte de Carga');
    for (const r of s.charge) {
      if (r.amount <= 0) anotar('Carga zero', c.name, `"${s.name}"`, `fonte "${r.on}" rende ${String(r.amount)}`);
    }
    /*
     * 7 · corrente impossível.
     *
     * `requiresSkills` guarda ÍNDICES, não ids — o motor faz `f.skills[index]`.
     * A primeira versão desta checagem comparava com `skill.id` e acusou dez
     * personagens inocentes. O defeito real é outro: um índice fora das três
     * habilidades, ou uma habilidade que exige a si mesma e portanto nunca sai.
     */
    const meuIndice = c.skills.indexOf(s);
    for (const req of s.requiresSkills ?? []) {
      const indice = Number(req);
      if (!Number.isInteger(indice) || indice < 0 || indice >= c.skills.length) {
        anotar('corrente quebrada', c.name, `"${s.name}"`, `exige a habilidade de índice "${req}", que não existe`);
      } else if (indice === meuIndice) {
        anotar('corrente quebrada', c.name, `"${s.name}"`, 'exige a si mesma: nunca pode sair');
      }
    }
  }
}

const porTipo = new Map<string, number>();
for (const a of achados) porTipo.set(a.tipo, (porTipo.get(a.tipo) ?? 0) + 1);

console.log(`${String(characters.length)} personagens · ${String(characters.length * 5)} blocos de ficha auditados`);
console.log(`achados: ${String(achados.length)}`, Object.fromEntries([...porTipo].sort((a, b) => b[1] - a[1])));
for (const [tipo] of porTipo) {
  console.log(`\n--- ${tipo} ---`);
  for (const a of achados.filter((x) => x.tipo === tipo).slice(0, 8)) console.log(`  ${a.quem} · ${a.onde}: ${a.detalhe}`);
  const n = achados.filter((x) => x.tipo === tipo).length;
  if (n > 8) console.log(`  ... e mais ${String(n - 8)}`);
}
if (achados.length > 0) process.exitCode = 1;
