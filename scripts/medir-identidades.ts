/*
 * FASE F · medir o que cada personagem entrega numa luta.
 *
 * A direção foi explícita sobre o método: **mecânica + simulação + override
 * manual**. Este script faz a parte da simulação, e ela é a que o sistema
 * antigo não tinha.
 *
 * O `rolesFor` que existia perguntava se um efeito de certo tipo **existe** na
 * ficha. A medição da FASE E mostrou aonde isso leva: "Dano" em 250 de 250,
 * porque todo mundo tem ataque básico e ataque básico machuca; "Ritmo" igual
 * para quem aplica um Lento de 5% por 4 s e para quem congela a luta.
 * Existência não é relevância.
 *
 * Então aqui ninguém pergunta o que a ficha promete. Cada personagem entra em
 * lutas 3 contra 3 — ele mais dois aliados sorteados, contra três sorteados,
 * todos com a mesma regra — e o script observa os eventos do combate: quem
 * causou dano e de que tamanho, quem curou, quem protegeu, quanto tempo de
 * controle aplicou, quem estava vivo no fim, quem venceu estando atrás.
 *
 * O resultado vai para docs/identidades-medidas.json. Nada é decidido aqui: as
 * identidades são derivadas desses números em src/presentation/identities.ts,
 * onde a comparação com o elenco inteiro define o que é alto e o que é normal.
 */
import { writeFileSync } from 'node:fs';

import { characters } from '../src/data/characters';
import { statuses } from '../src/data/statuses';
import { createBattle, stepBattle } from '../src/engine/battle';
import type { StatusId } from '../src/engine/types';

const SEMENTES = Number(process.env.SEMENTES ?? 40);

/* Controle duro: tira o turno do alvo, em vez de só atrapalhar. */
const CONTROLE_DURO = new Set<StatusId>(['paralyzed', 'rooted', 'silenced', 'confused', 'frozen', 'sleep']);
/* Os que drenam Vida sozinhos ao longo do tempo. */
const CONTINUOS = new Set<StatusId>(['burning', 'electric', 'poison', 'bleed']);
/* Os que mexem na velocidade da luta. */
const RITMO = new Set<StatusId>(['haste', 'slow']);

export interface Medida {
  id: string; nome: string; lutas: number;
  /* entrega bruta, por luta */
  dano: number; cura: number; protecao: number; abates: number;
  /* forma do dano */
  maiorGolpe: number; golpes: number; danoEmArea: number;
  /* o que aplica nos outros */
  controleSegundos: number; interrupcoes: number; ritmoSegundos: number;
  buffsEmAliado: number; debuffsEmInimigo: number; cargaDada: number;
  continuoSegundos: number;
  /* o que acontece com ele */
  sobrevive: number; danoRecebido: number; segundosVivo: number;
  curaEmSi: number; reforcoEmSi: number;
  /* quando decide */
  vitorias: number; viradas: number; preparoMaximo: number;
}

const medidas: Medida[] = [];

for (const [indice, c] of characters.entries()) {
  const m: Medida = {
    id: c.id, nome: c.name, lutas: SEMENTES,
    dano: 0, cura: 0, protecao: 0, abates: 0,
    maiorGolpe: 0, golpes: 0, danoEmArea: 0,
    controleSegundos: 0, interrupcoes: 0, ritmoSegundos: 0,
    buffsEmAliado: 0, debuffsEmInimigo: 0, cargaDada: 0, continuoSegundos: 0,
    sobrevive: 0, danoRecebido: 0, segundosVivo: 0, curaEmSi: 0, reforcoEmSi: 0,
    vitorias: 0, viradas: 0,
    preparoMaximo: Math.max(...c.skills.map((s) => s.preparation)),
  };

  for (let s = 0; s < SEMENTES; s += 1) {
    const outros = characters.filter((o) => o.id !== c.id);
    /* Mesma regra de sorteio para todos: o que varia é quem está sendo medido. */
    const pega = (n: number) => outros[(s * 37 + n * 61 + indice) % outros.length]!.id;
    const b = createBattle([c.id, pega(1), pega(2)], [pega(3), pega(4), pega(5)], s + 1);
    const eu = b.fighters[0]!;

    let visto = 0, atrasou = false, vivoAte = 0;
    /* Golpes do mesmo instante contam como um ataque em área. */
    let instante = -1, alvosNoInstante = 0;

    for (let passo = 0; passo < 4200 && !b.finished; passo += 1) {
      stepBattle(b);
      if (eu.hp > 0) vivoAte = b.time;
      /* Esteve atrás na Vantagem em algum momento? Então vencer é virada. */
      if (b.dominion < -8) atrasou = true;

      for (const ev of b.events) {
        if (ev.id <= visto) continue;
        visto = ev.id;
        const fonte = b.fighters.find((f) => f.uid === ev.source);
        const alvo = ev.target ? b.fighters.find((f) => f.uid === ev.target) : undefined;

        /* O que o inimigo faz nele. */
        if (alvo?.uid === eu.uid && ev.kind === 'damage' && fonte?.side !== eu.side) {
          m.danoRecebido += ev.value ?? 0;
        }
        if (fonte?.uid !== eu.uid) continue;

        switch (ev.kind) {
          case 'damage': {
            const v = ev.value ?? 0;
            m.dano += v; m.golpes += 1;
            m.maiorGolpe = Math.max(m.maiorGolpe, v);
            if (Math.abs(ev.time - instante) < 1e-6) { alvosNoInstante += 1; if (alvosNoInstante >= 2) m.danoEmArea += v; }
            else { instante = ev.time; alvosNoInstante = 1; }
            break;
          }
          case 'heal':
            m.cura += ev.value ?? 0;
            if (alvo?.uid === eu.uid) m.curaEmSi += ev.value ?? 0;
            break;
          case 'shield': m.protecao += ev.value ?? 0; break;
          case 'interrupt': m.interrupcoes += 1; break;
          case 'ko': m.abates += 1; break;
          case 'charge': if (alvo && alvo.uid !== eu.uid && alvo.side === eu.side) m.cargaDada += ev.value ?? 0; break;
          case 'status': {
            const id = ev.status;
            if (!id || !alvo) break;
            /* A duração aplicada é o que mede o peso de um Status, não a contagem. */
            const dur = alvo.statuses.find((x) => x.id === id)?.duration ?? 0;
            if (statuses[id].tone === 'negativo' && alvo.side !== eu.side) {
              m.debuffsEmInimigo += 1;
              if (CONTROLE_DURO.has(id)) m.controleSegundos += dur;
              if (CONTINUOS.has(id)) m.continuoSegundos += dur;
              if (RITMO.has(id)) m.ritmoSegundos += dur;
            }
            if (statuses[id].tone === 'positivo' && alvo.side === eu.side) {
              if (alvo.uid === eu.uid) { if (id === 'strengthened' || id === 'haste') m.reforcoEmSi += dur; }
              else m.buffsEmAliado += 1;
              if (RITMO.has(id)) m.ritmoSegundos += dur;
            }
            break;
          }
          default: break;
        }
      }
    }

    if (eu.hp > 0) m.sobrevive += 1;
    m.segundosVivo += vivoAte;
    if (b.winner === 'player') { m.vitorias += 1; if (atrasou) m.viradas += 1; }
  }

  /* Tudo vira média por luta, menos o que já é contagem de lutas. */
  const porLuta = (v: number) => Number((v / SEMENTES).toFixed(2));
  medidas.push({
    ...m,
    dano: porLuta(m.dano), cura: porLuta(m.cura), protecao: porLuta(m.protecao), abates: porLuta(m.abates),
    golpes: porLuta(m.golpes), danoEmArea: porLuta(m.danoEmArea),
    controleSegundos: porLuta(m.controleSegundos), interrupcoes: porLuta(m.interrupcoes),
    ritmoSegundos: porLuta(m.ritmoSegundos), buffsEmAliado: porLuta(m.buffsEmAliado),
    debuffsEmInimigo: porLuta(m.debuffsEmInimigo), cargaDada: porLuta(m.cargaDada),
    continuoSegundos: porLuta(m.continuoSegundos), danoRecebido: porLuta(m.danoRecebido),
    segundosVivo: porLuta(m.segundosVivo), curaEmSi: porLuta(m.curaEmSi), reforcoEmSi: porLuta(m.reforcoEmSi),
    sobrevive: Number((m.sobrevive / SEMENTES).toFixed(3)),
    vitorias: Number((m.vitorias / SEMENTES).toFixed(3)),
    viradas: Number((m.viradas / SEMENTES).toFixed(3)),
  });
  if ((indice + 1) % 50 === 0) console.log(`  ${String(indice + 1)}/${String(characters.length)}`);
}

writeFileSync('docs/identidades-medidas.json', `${JSON.stringify({ sementesPorPersonagem: SEMENTES, medidas }, null, 1)}\n`);
console.log(`\n${String(characters.length)} personagens · ${String(SEMENTES)} lutas cada · ${String(characters.length * SEMENTES)} lutas`);
const amostra = medidas.filter((x) => ['saitama', 'storm', 'wolverine', 'professorx'].includes(x.id));
for (const x of amostra) {
  console.log(`${x.nome}: dano ${String(x.dano)} (maior golpe ${String(x.maiorGolpe)}, área ${String(x.danoEmArea)}) · controle ${String(x.controleSegundos)}s · cura ${String(x.cura)} · vive ${(x.sobrevive * 100).toFixed(0)}%`);
}
