/*
 * FASE E · a auditoria de clareza.
 *
 * A regra que a direção escreveu é "BATEU O OLHO = ENTENDEU", e ela vem com uma
 * lista do que não pode aparecer para o jogador: "alvo válido", "efeito
 * aplicado", "estado", "recarga interna", nomes internos, strings técnicas.
 *
 * Este script renderiza a ficha inteira dos 250 — traço, ataque básico e as
 * três habilidades — e cobra quatro coisas:
 *
 *   1. todo Status aplicado começa com "Aplica <Nome>";
 *   2. nenhuma string proibida aparece;
 *   3. nada fica indefinido, vazio ou com número quebrado;
 *   4. a mesma fonte de Carga não é listada duas vezes na mesma habilidade.
 *
 * Sai com código 1 se achar qualquer coisa.
 */
import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import { describeCharge, presentSkill, presentTrait } from '../src/engine/skill-descriptions';

/*
 * O que nunca pode chegar ao jogador.
 *
 * São termos do código, não do jogo. Alguns parecem inocentes isolados —
 * "estado" é português comum — mas na ficha de um lutador eles significam que
 * uma string técnica vazou para a tela.
 */
const PROIBIDAS: readonly (readonly [RegExp, string])[] = [
  [/alvo v[áa]lido/i, 'alvo válido'],
  [/efeito aplicado/i, 'efeito aplicado'],
  [/recarga interna/i, 'recarga interna'],
  [/\bundefined\b|\bnull\b|\bNaN\b/i, 'valor indefinido'],
  [/\[object /i, 'objeto cru'],
  [/enemyWeak|enemyStrong|allEnemies|allAllies|allyWeak|randomEnemy|enemyCast/i, 'nome interno de alvo'],
  [/allyHurt|enemyHurt|negativeStatus|storedEnergy|requiresSkills/i, 'nome interno de gatilho'],
  [/\bkind\b|\bstack\b|\bcap\b:/i, 'campo interno'],
];

interface Achado { personagem: string; onde: string; problema: string; texto: string }
const achados: Achado[] = [];

const nomesDeStatus = new Set(Object.values(statuses).map((s) => s.name));

for (const c of characters) {
  const partes: { onde: string; linhas: string[]; carga?: string }[] = [
    { onde: `traço "${c.trait.name}"`, linhas: presentTrait(c.trait).effects },
    ...c.skills.map((s) => {
      const p = presentSkill(s);
      return { onde: `habilidade "${s.name}"`, linhas: p.effects, carga: describeCharge(s.charge) };
    }),
  ];

  for (const parte of partes) {
    for (const linha of parte.linhas) {
      /* 1 · todo Status aplicado se anuncia. */
      const comecaComNomeDeStatus = [...nomesDeStatus].some((n) => linha.startsWith(`${n} ·`));
      if (comecaComNomeDeStatus) {
        achados.push({ personagem: c.name, onde: parte.onde, problema: 'Status sem "Aplica"', texto: linha });
      }
      /* 2 · nada de string técnica. */
      for (const [padrao, rotulo] of PROIBIDAS) {
        if (padrao.test(linha)) achados.push({ personagem: c.name, onde: parte.onde, problema: rotulo, texto: linha });
      }
      /* 3 · nada vazio. */
      if (linha.trim().length < 3) {
        achados.push({ personagem: c.name, onde: parte.onde, problema: 'linha vazia', texto: JSON.stringify(linha) });
      }
    }

    /* 4 · a mesma fonte de Carga não aparece duas vezes. */
    if (parte.carga !== undefined) {
      for (const [padrao, rotulo] of PROIBIDAS) {
        if (padrao.test(parte.carga)) achados.push({ personagem: c.name, onde: parte.onde, problema: `${rotulo} (Carga)`, texto: parte.carga });
      }
      const fontes = parte.carga.split(';').map((x) => x.replace(/^\+[\d,.]+%?\s*/, '').trim());
      const vistas = new Set<string>();
      for (const f of fontes) {
        if (vistas.has(f)) achados.push({ personagem: c.name, onde: parte.onde, problema: 'Carga duplicada na ficha', texto: parte.carga });
        vistas.add(f);
      }
    }
  }
}

const porProblema = new Map<string, number>();
for (const a of achados) porProblema.set(a.problema, (porProblema.get(a.problema) ?? 0) + 1);

console.log(`personagens auditados: ${String(characters.length)}`);
console.log(`achados: ${String(achados.length)}`, Object.fromEntries(porProblema));
for (const a of achados.slice(0, 25)) {
  console.log(`  ${a.personagem} · ${a.onde} · ${a.problema}`);
  console.log(`     ${a.texto}`);
}
if (achados.length > 25) console.log(`  ... e mais ${String(achados.length - 25)}`);

if (achados.length > 0) process.exitCode = 1;
