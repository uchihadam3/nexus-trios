/*
 * FASE E · a clareza como contrato.
 *
 * A regra da direção é "BATEU O OLHO = ENTENDEU", e ela vem com uma lista do
 * que não pode chegar à tela: "alvo válido", "efeito aplicado", "recarga
 * interna", nomes internos, strings técnicas.
 *
 * Auditar uma vez não serve de nada: o roster cresce, alguém escreve uma
 * habilidade nova, e a string técnica volta. Então a auditoria vira teste.
 */
import { readFileSync } from 'node:fs';
import { globSync } from 'node:fs';

import { describe, expect, it } from 'vitest';

import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import { cargasLegiveis, describeCharge, presentSkill, presentStatus, presentTrait, targetNames, targetNamesEm } from '../src/engine/skill-descriptions';

/** Toda linha que o jogador lê na ficha: traço, básico e as três habilidades. */
const linhasDaFicha = (): { quem: string; onde: string; linha: string }[] =>
  characters.flatMap((c) => [
    ...presentTrait(c.trait).effects.map((linha) => ({ quem: c.name, onde: c.trait.name, linha })),
    ...c.skills.flatMap((s) => [
      ...presentSkill(s).effects.map((linha) => ({ quem: c.name, onde: s.name, linha })),
      { quem: c.name, onde: `${s.name} (Carga)`, linha: describeCharge(s.charge) },
    ]),
  ]);

describe('clareza da escrita pública', () => {
  const todas = linhasDaFicha();

  it('cobre a ficha inteira dos 250', () => {
    expect(characters).toHaveLength(250);
    /* traço + 3 habilidades × (efeitos + carga): nunca menos que 4 linhas por lutador. */
    expect(todas.length).toBeGreaterThan(characters.length * 4);
  });

  it.each([
    ['alvo válido', /alvo v[áa]lido/i],
    ['efeito aplicado', /efeito aplicado/i],
    ['recarga interna', /recarga interna/i],
    ['valor indefinido', /\bundefined\b|\bnull\b|\bNaN\b/i],
    ['objeto cru', /\[object /i],
    ['nome interno de alvo', /enemyWeak|enemyStrong|allEnemies|allAllies|allyWeak|randomEnemy|enemyCast/],
    ['nome interno de gatilho', /allyHurt|enemyHurt|negativeStatus|storedEnergy|requiresSkills/],
  ])('nunca mostra "%s" ao jogador', (_rotulo, padrao) => {
    const vazou = todas.filter((l) => padrao.test(l.linha));
    expect(vazou.map((l) => `${l.quem} · ${l.onde} · ${l.linha}`)).toEqual([]);
  });

  /*
   * O defeito que o próprio jogador encontrou.
   *
   * A pergunta foi "o buff fortalecido me parece fraco, só 3% de dano a mais".
   * Estava fraco na leitura, não no jogo: Fortalecido soma a cada aplicação até
   * 80%, e a ficha mostrava só os 3% da primeira. Quem lê precisa ver o teto.
   */
  it('avisa quando um Status soma, e diz até quanto', () => {
    const queSomam = Object.entries(statuses).filter(([, d]) => d.stack === 'add');
    expect(queSomam.length).toBeGreaterThan(0);
    for (const [id, def] of queSomam) {
      const p = presentStatus(id as keyof typeof statuses, 0.03);
      expect(p.accumulation, `${id} não explica que soma`).toBeTruthy();
      /*
       * O sentido, não a frase exata. O que não pode faltar é o jogador saber
       * que **cada** aplicação soma — "soma até 80%" lê como se o Status
       * fosse até 80% e pronto. A redação encurtou quando a ficha passou a
       * agrupar por alvo; a exigência é a mesma.
       */
      expect(p.accumulation).toMatch(/soma (por|a cada) aplica/i);
      /* O teto aparece como número, não como palavra vaga. */
      expect(p.accumulation).toMatch(/\d/);
      expect(def.cap).toBeGreaterThan(0);
    }
  });

  /*
   * "Não deixar 'Lento' solto como se fosse ataque."
   *
   * Sem o verbo, "Lento · 20% mais devagar" podia ser lido como "este
   * personagem é lento" em vez de "este personagem deixa o alvo lento".
   */
  it('anuncia todo Status com "Aplica <Nome>"', () => {
    const nomes = Object.values(statuses).map((s) => s.name);
    const soltos = todas.filter((l) => nomes.some((n) => l.linha.startsWith(`${n} ·`)));
    expect(soltos.map((l) => `${l.quem} · ${l.onde} · ${l.linha}`)).toEqual([]);

    /* E o verbo de fato aparece em quem aplica algo. */
    const comStatus = characters.filter((c) =>
      c.skills.some((s) => s.effects.some((e) => e.kind === 'status')));
    expect(comStatus.length).toBeGreaterThan(100);
    for (const c of comStatus) {
      const texto = c.skills.flatMap((s) => presentSkill(s).effects).join(' | ');
      expect(texto, `${c.name} aplica Status sem dizer "Aplica"`).toMatch(/Aplica /);
    }
  });

  /*
   * "Agregar fontes iguais de Carga. Remover repetição."
   *
   * O motor dispara `time` e `survived` no mesmo passo, sem condição — são a
   * mesma fonte. Seis fichas mostravam as duas como linhas separadas, e a
   * primeira ("por segundo enquanto estiver na luta") sugeria uma condição
   * inexistente: estar na luta é o estado normal, não um requisito.
   */
  it('soma as fontes de Carga que significam a mesma coisa', () => {
    for (const c of characters) {
      for (const s of c.skills) {
        const linhas = cargasLegiveis(s.charge);
        const porSegundo = linhas.filter((l) => /% por segundo$/.test(l));
        expect(porSegundo.length, `${c.name} · ${s.name}: ${linhas.join('; ')}`).toBeLessThanOrEqual(1);
        /* E nenhuma fonte aparece duas vezes com o mesmo texto. */
        expect(new Set(linhas).size).toBe(linhas.length);
      }
    }
  });

  /*
   * O gotejamento passivo vem por último.
   *
   * "+2% por segundo" é verdade em quase toda habilidade do jogo, então ele não
   * diferencia nada. Quando vinha primeiro, quem comparava duas fichas lia a
   * linha irrelevante antes da linha que define a habilidade.
   */
  it('põe o "por segundo" passivo no fim da lista de Carga', () => {
    const foraDeOrdem: string[] = [];
    for (const c of characters) {
      for (const s of c.skills) {
        const linhas = cargasLegiveis(s.charge);
        const i = linhas.findIndex((l) => /% por segundo$/.test(l));
        if (i >= 0 && i < linhas.length - 1) foraDeOrdem.push(`${c.name} · ${s.name}: ${linhas.join('; ')}`);
      }
    }
    expect(foraDeOrdem).toEqual([]);
  });


  /*
   * "Agregar fontes iguais. Remover repetição." vale para o alvo também.
   *
   * "Alvo: inimigo mais ferido" e "Usa quando: ficar pronta, contra inimigo
   * mais ferido" apareciam em linhas vizinhas da mesma ficha.
   */
  it('não repete o alvo na linha de quando usar', () => {
    const repetidas: string[] = [];
    for (const c of characters) {
      for (const s of c.skills) {
        const p = presentSkill(s);
        if (p.useWhen.includes(p.target)) repetidas.push(`${c.name} · ${s.name}: "${p.target}" / "${p.useWhen}"`);
      }
    }
    expect(repetidas).toEqual([]);
  });


  /*
   * A linha "Alvo" só aparece quando ainda tem o que dizer.
   *
   * O jogador apontou a redundância numa ficha: "Aplica Fortalecido em si
   * próprio" e, logo abaixo, "Alvo: o próprio personagem". Na mesma habilidade
   * o dano ia para um inimigo, então o rodapé não era só eco — contradizia, e
   * quem lesse rápido concluiria que a habilidade inteira caía nela.
   */
  it('não repete o alvo quando cada efeito já diz o seu', () => {
    const ecos: string[] = [];
    for (const c of characters) {
      for (const s of c.skills) {
        const p = presentSkill(s);
        if (!p.mostrarAlvo) continue;
        /* Se a linha "Alvo" aparece, ao menos um efeito depende dela. */
        const dependem = s.effects.filter((e) => e.kind !== 'status'
          && (e.target === undefined || e.target === s.target));
        if (dependem.length === 0) ecos.push(`${c.name} · ${s.name}: ${p.effects.join(' | ')} → Alvo ${p.target}`);
      }
    }
    expect(ecos).toEqual([]);
  });

  /*
   * E quando a habilidade acerta lados diferentes, cada linha diz o seu, para
   * ninguém precisar deduzir a quais o rodapé se aplicava.
   */
  it('habilidade de alvos misturados nomeia o alvo em cada linha', () => {
    const faltando: string[] = [];
    for (const c of characters) {
      for (const s of c.skills) {
        const alvos = new Set(s.effects.map((e) => e.target ?? s.target));
        if (alvos.size <= 1) continue;
        const p = presentSkill(s);
        expect(p.mostrarAlvo, `${c.name} · ${s.name} ainda mostra Alvo`).toBe(false);
        p.effects.forEach((linha, i) => {
          const e = s.effects[i]!;
          /* Guardar/liberar energia, a Death Note, reviver e roubo de vida se explicam na própria frase. */
          if (['store', 'release', 'deathnote', 'revive', 'lifesteal', 'copy'].includes(e.kind)) return;
          /* A Invocação diz o nome da criatura ("Invoca Cão divino"): ela luta ao lado de quem invocou. */
          if (e.kind === 'status' && e.status === 'summon') return;
          /* Status diz "em si próprio"; os demais dizem "→ o próprio personagem". */
          const alvo = e.kind === 'status'
            ? targetNamesEm[e.target ?? s.target]
            : targetNames[e.target ?? s.target];
          if (!linha.includes(alvo)) faltando.push(`${c.name} · ${s.name}: "${linha}" devia citar ${alvo}`);
        });
      }
    }
    expect(faltando).toEqual([]);
  });

  it('não repete a mesma fonte de Carga na mesma habilidade', () => {
    for (const c of characters) {
      for (const s of c.skills) {
        const fontes = describeCharge(s.charge).split(';').map((x) => x.replace(/^\+[\d,.]+%?\s*/, '').trim());
        expect(new Set(fontes).size, `${c.name} · ${s.name}: ${describeCharge(s.charge)}`).toBe(fontes.length);
      }
    }
  });

  it('não deixa linha vazia nem truncada na ficha', () => {
    const curtas = todas.filter((l) => l.linha.trim().length < 3);
    expect(curtas.map((l) => `${l.quem} · ${l.onde}`)).toEqual([]);
  });
});

/*
 * A clareza também mora fora da ficha.
 *
 * A auditoria de texto cobria traço, habilidades e Carga — e passou limpa nos
 * 250. Mas um print do celular mostrou a tela inicial dizendo "Conheça os 100
 * lutadores" com 250 no jogo, e a tela de diagnóstico dizendo "300
 * habilidades" com 750. Número de roster escrito à mão envelhece calado: o
 * roster cresce, ninguém lembra da string, e o jogo passa a mentir.
 *
 * Este bloco lê o código das telas e cobra que esses números venham dos dados.
 */
describe('as telas não guardam números de roster escritos à mão', () => {
  const fontes = globSync('src/{screens,components}/**/*.tsx').map((f) => ({ f, texto: readFileSync(f, 'utf8') }));

  it('encontra as telas', () => {
    expect(fontes.length).toBeGreaterThan(5);
  });

  it('não escreve a contagem de lutadores, habilidades ou Status à mão', () => {
    /* Um número literal colado no substantivo é sempre uma contagem congelada. */
    /* Pega as duas formas: "300 habilidades" e "habilidades: 300". */
    const padrao = /['`"][^'`"]*(\b\d{2,4}\s+(?:lutadores|personagens|habilidades|Status|universos|retratos)\b|\b(?:lutadores|personagens|habilidades|Status|universos|retratos):\s*\d{2,4}\b)/g;
    const presos = fontes.flatMap(({ f, texto }) => [...texto.matchAll(padrao)].map((m) => `${f}: ${m[0]}`));
    expect(presos).toEqual([]);
  });

  it('não usa "estado" onde o jogo diz "Status"', () => {
    /*
     * Só texto de uma linha: a primeira versão atravessava quebras de linha e
     * acusava `{ estado, battle }` — nome de variável, não texto de tela.
     */
    const padrao = /['`"][^'`"\n]*\b(estado|estados)\b[^'`"\n]*['`"]/gi;
    const presos = fontes.flatMap(({ f, texto }) => [...texto.matchAll(padrao)].map((m) => `${f}: ${m[0]}`));
    expect(presos).toEqual([]);
  });
});
