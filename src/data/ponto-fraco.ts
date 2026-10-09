/*
 * Ponto fraco em poucas palavras.
 *
 * Pedido do jogador: a ficha mostrava a fraqueza como uma parede de texto
 * ("Contra Interrupção: Kamehameha leva 3,0 s de Preparo — se for cortado,
 * perde a jogada principal. Contra esses trios, ganha 6 de cada 100…"). O que
 * a pessoa precisa é bater o olho e entender: "fraco contra Interrupção —
 * Kamehameha demora 3 s para sair". O texto medido (fraquezas.ts, de 20.000
 * lutas) continua sendo a fonte; aqui ele vira etiquetas curtas.
 */
export type TipoDeFraqueza = 'interrupcao' | 'explosao' | 'area' | 'cura' | 'rapidos' | 'continuo' | 'controle' | 'tanques' | 'longa' | 'momento' | 'apanhar';

export interface Fraqueza {
  tipo: TipoDeFraqueza;
  /** O nome curto do que o vence (vai na etiqueta). */
  contra: string;
  /** Por quê, em poucas palavras. */
  motivo: string;
}

const CABECALHOS: [RegExp, TipoDeFraqueza, string][] = [
  [/^Contra Interrupção$/, 'interrupcao', 'Interrupção'],
  [/^Contra Explosão$/, 'explosao', 'Explosão'],
  [/^Contra Área$/, 'area', 'Golpes em área'],
  [/^Contra Cura e Escudo$/, 'cura', 'Cura e Escudo'],
  [/^Contra trios rápidos$/, 'rapidos', 'Trios rápidos'],
  [/^Contra Dano contínuo$/, 'continuo', 'Queimadura'],
  [/^Contra Controle$/, 'controle', 'Controle'],
  [/^Contra Tanques$/, 'tanques', 'Tanques'],
  [/^Em luta longa$/, 'longa', 'Luta longa'],
  [/^Depende do momento$/, 'momento', 'Hora certa'],
  [/^Precisa apanhar para crescer$/, 'apanhar', 'Explosão'],
];
const DIVISOR = /(Contra (?:Interrupção|Explosão|Área|Cura e Escudo|trios rápidos|Dano contínuo|Controle|Tanques)|Em luta longa|Depende do momento|Precisa apanhar para crescer):\s/g;

const CONDICAO: [RegExp, string][] = [
  [/inimigo estiver Exposto/, 'com o rival enfraquecido'],
  [/inimigo estiver em Preparo/, 'com o rival em Preparo'],
  [/trio estiver sob ameaça/, 'com o trio em perigo'],
  [/alvo já estiver ferido/, 'com o alvo ferido'],
];

const numero = (s: string) => s.replace(/,0\b/, '');

function motivoDe(tipo: TipoDeFraqueza, texto: string): string {
  switch (tipo) {
    case 'interrupcao': {
      const m = /^(.+?) leva ([\d,]+) s de Preparo/.exec(texto);
      return m ? `${m[1]} demora ${numero(m[2]!)} s para sair` : 'Golpe principal demora a sair';
    }
    case 'explosao': {
      const m = /só ([\d.]+) de Vida/.exec(texto);
      return m ? `Só ${m[1]} de Vida` : 'Pouca Vida';
    }
    case 'area': return 'Sofre junto com o trio todo';
    case 'cura': return 'Bate em um alvo só';
    case 'rapidos': {
      const m = /a cada ([\d,]+) s/.exec(texto);
      return m ? `Ataca só a cada ${numero(m[1]!)} s` : 'Ataca devagar';
    }
    case 'continuo': return 'Não consegue se limpar';
    case 'controle': return 'Fica preso com facilidade';
    case 'tanques': return 'Não derruba quem aguenta muito';
    case 'longa': return 'Não se cura nem se protege';
    case 'momento': {
      const m = /^(.+?) só sai quando/.exec(texto);
      const quando = CONDICAO.find(([r]) => r.test(texto))?.[1] ?? 'em certas horas';
      return m ? `${m[1]} só sai ${quando}` : `Golpe forte só sai ${quando}`;
    }
    case 'apanhar': {
      const m = /^(.+?) só o fortalece/.exec(texto);
      return m ? `${m[1]} só cresce apanhando` : 'Precisa apanhar para crescer';
    }
  }
}

/** As fraquezas de um personagem, curtas (no máximo duas, a mais forte primeiro). */
export function pontoFraco(texto: string): Fraqueza[] {
  const partes: { cab: string; corpo: string }[] = [];
  let m: RegExpExecArray | null;
  const achados: { cab: string; ini: number; fim: number }[] = [];
  DIVISOR.lastIndex = 0;
  while ((m = DIVISOR.exec(texto))) achados.push({ cab: m[1]!, ini: m.index, fim: m.index + m[0].length });
  achados.forEach((a, k) => partes.push({ cab: a.cab, corpo: texto.slice(a.fim, achados[k + 1]?.ini ?? texto.length).trim() }));
  const lista: Fraqueza[] = [];
  for (const { cab, corpo } of partes) {
    const def = CABECALHOS.find(([r]) => r.test(cab));
    if (!def) continue;
    const [, tipo, contra] = def;
    if (lista.some((x) => x.contra === contra)) continue;
    lista.push({ tipo, contra, motivo: motivoDe(tipo, corpo) });
  }
  if (!lista.length && texto.trim()) {
    // texto antigo, sem os cabeçalhos medidos: a primeira frase, curta
    const frase = texto.split(/[.—]/)[0]!.trim();
    lista.push({ tipo: 'momento', contra: 'Atenção', motivo: frase.length > 48 ? `${frase.slice(0, 46)}…` : frase });
  }
  return lista.slice(0, 2);
}
