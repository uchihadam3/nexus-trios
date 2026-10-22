/*
 * Dicas de trio — o "técnico" da escolha de personagens.
 *
 * Pedido do jogador: um botão que liga dicas na escolha do trio, bem
 * inteligentes, que ensinam qual personagem combina com qual — a melhor
 * escolha marcada, quanto (%) cada candidato encaixa no trio, um motivo curto
 * e, tocando, uma explicação maior. Quem usa as dicas aprende, mas pontua
 * menos: −10 mil por luta da jornada (src/engine/pontos.ts).
 *
 * Tudo vem do que foi medido em lutas simuladas, não de opinião:
 *   - a força de cada personagem e o peso de cada combo, em 4 milhões de lutas
 *     (src/data/forca-dos-rivais.ts), e quanto cada um vence sozinho e com quem
 *     vence mais (src/data/duplas-medidas.ts);
 *   - os combos que o candidato forma com o trio (src/engine/combos.ts);
 *   - os papéis lidos dos kits (src/engine/sinergia.ts): quem dá Carga, quem
 *     cura e protege, quem é frágil, quem bate forte, quem cresce apanhando…
 *
 * O "encaixe" é a posição do candidato entre todo o elenco disponível para
 * este trio: 88% = combina melhor com quem você já escolheu do que 88% dos
 * personagens que poderiam entrar.
 */
import { byId, characters } from '../data/characters';
import { AJUSTE_DAS_DUPLAS, ALFABETO_DAS_DUPLAS, PASSO_DAS_DUPLAS } from '../data/duplas-ajuste';
import { DUPLAS } from '../data/duplas-medidas';
import { PERCENTIS } from '../data/percentis-dos-trios';
import { PERCENTIS_FINOS } from '../data/percentis-finos';
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { pontoFraco, type TipoDeFraqueza } from '../data/ponto-fraco';
import { pontoForte } from '../data/ponto-forte';
import { forcaDoTrio } from '../engine/campaign';
import { combosDoTrio } from '../engine/combos';
import { papelDe } from '../engine/sinergia';
import { porQue } from './porque';
import { IDIOMA, nomeDe, t, tx } from '../i18n/idioma';

export interface Motivo {
  texto: string; tom: 'bom' | 'alerta';
  /** o porquê, com as habilidades (na explicação maior) */
  porque?: string;
  /** 'trio': é da combinação com quem já está no trio; 'dele': é do próprio personagem, vale em qualquer trio */
  grupo?: 'trio' | 'dele';
}
/* `resumo`: o motivo em poucas palavras, para a frase "Escolha X porque …, … e …" */
type MotivoOrdenado = Motivo & { ordem: number; resumo?: string; combo?: boolean; soloFraco?: boolean };
export interface DicaDoCandidato {
  id: string;
  /** 0–100: combina melhor com o trio do que esta % do elenco disponível */
  encaixe: number;
  melhor: boolean;
  /** até dois motivos, para o cartão */
  curtos: Motivo[];
  /** a explicação inteira, para quem toca em "Por quê?" */
  detalhe: Motivo[];
}

/* o primeiro nome; se outro personagem tem o mesmo (Capitão Planeta, Capitão América), as duas primeiras palavras */
const PRIMEIRO = (id: string) => nomeDe(byId[id]!).split(/[ ,]/)[0]!;
// os nomes repetidos são os do idioma do jogo, então a conta espera o dicionário carregar (fica para o primeiro uso)
let repetidos: Set<string> | undefined;
const REPETIDOS = () => (repetidos ??= new Set(characters.map((c) => PRIMEIRO(c.id)).filter((n, i, l) => l.indexOf(n) !== i)));
const nome = (id: string) => (REPETIDOS().has(PRIMEIRO(id)) ? nomeDe(byId[id]!).split(/[ ,]/).slice(0, 2).join(' ') : PRIMEIRO(id));
/* "É o primeiro a cair…" vira "é o primeiro a cair…" depois dos dois-pontos; nome de habilidade fica como está */
const COMECO_MINUSCULO = IDIOMA === 'en' ? /^(It's|Only|Hits|In|Gets|Takes|Cuts|Puts|Fires|Speeds|Keeps|Holds|No|Stays|Fills|Brings|First|What|The first|Allies') / : /^(É|Só|Bate|Em|A|Fica|Derruba|Corta|Põe|Solta|Adianta|As|Mantém|Segura|Nenhum) /;
const minuscula = (x: string) => (COMECO_MINUSCULO.test(x) ? x.charAt(0).toLowerCase() + x.slice(1) : x);
const VIDAS = characters.map((c) => c.hp).sort((a, b) => a - b);
const VIDA_MEDIANA = VIDAS[Math.floor(VIDAS.length / 2)]!;
const percentil = (lista: number[], x: number) => Math.round((100 * lista.filter((v) => v < x).length) / Math.max(1, lista.length));

/* quanto o trio com ele vence (com dois parceiros quaisquer), e em que posição isso o põe no elenco */
const SOLOS = Object.values(DUPLAS).map((d) => d.solo).sort((a, b) => a - b);
const pct = (x: number) => `${Math.round(100 * x)}%`;
const lista3 = (l: string[]) => (l.length > 1 ? `${l.slice(0, -1).join(', ')}${t(' e ')}${l.at(-1)}` : l[0] ?? '');
const chaveDoCombo = (c: { id: string; de: string[]; para: string[] }) => `${c.id}|${[...c.de, ...c.para].sort().join(',')}`;

/*
 * O quanto a dupla rende além da força dos dois e dos combos (src/data/duplas-ajuste.ts): o que as habilidades
 * de um fazem pelas do outro sem ser combo, medido nas lutas. Um caractere por dupla, na ordem do elenco.
 */
const POSICAO = new Map(characters.map((c, i) => [c.id, i])), TOTAL = characters.length;
const VALOR = new Map([...ALFABETO_DAS_DUPLAS].map((ch, i) => [ch, (i - 32) * PASSO_DAS_DUPLAS]));
export function ajusteDaDupla(a: string, b: string): number {
  let i = POSICAO.get(a), j = POSICAO.get(b);
  if (i === undefined || j === undefined || i === j) return 0;
  if (i > j) [i, j] = [j, i];
  return VALOR.get(AJUSTE_DAS_DUPLAS[i * TOTAL - (i * (i + 1)) / 2 + (j - i - 1)]!) ?? 0;
}
/** A nota de um trio (ou dupla) para as Dicas: a força, os combos e o que cada dupla rende junta. */
export function notaDoTrio(team: readonly string[]): number {
  let n = forcaDoTrio(team);
  for (let a = 0; a < team.length; a++) for (let b = a + 1; b < team.length; b++) n += ajusteDaDupla(team[a]!, team[b]!);
  return n;
}
/*
 * Quanto o trio é melhor que os outros (pedido do dono: "esse trio é melhor que 99%, 98%… dos outros trios"): a posição
 * da nota dele na régua de todos os trios possíveis (src/data/percentis-dos-trios.ts), de 0 a 100.
 */
export function melhorQueOsTrios(team: readonly string[]): number {
  return percentilDaNota(notaDoTrio(team));
}
/** Em que posição (0 a 100) uma nota de trio fica na régua de todos os trios. */
export function percentilDaNota(nota: number): number {
  let p = 0;
  while (p < 100 && PERCENTIS[p + 1]! <= nota) p++;
  return p;
}
/*
 * Dentro do X% do trio, onde ele está (pedido do dono: "melhor que 99%… só que dentro desses 99 existem muitos times, ele
 * é melhor que quantos?"): de 0 a 99, a posição da nota entre os trios da mesma faixa de 1% (a régua fina tem 20 pontos em
 * cada faixa; entre eles, em linha reta). 37 = melhor que 37% dos trios que também são "melhor que X%". O melhor trio de
 * todos (100%) fica com 100.
 */
export function dentroDaFaixa(nota: number): number {
  const p = percentilDaNota(nota);
  if (p >= 100) return 100;
  let lo = 0, hi = PERCENTIS_FINOS.length - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (PERCENTIS_FINOS[m]! <= nota) lo = m; else hi = m; }
  const a = PERCENTIS_FINOS[lo]!, b = PERCENTIS_FINOS[hi]!;
  // as notas são múltiplos de 0,001 e muitos trios empatam: na nota de um ponto repetido da régua, vale o meio do empate
  let inicio = lo;
  while (a === nota && inicio > 0 && PERCENTIS_FINOS[inicio - 1] === a) inicio--;
  const f = a === nota ? (inicio + lo) / 2 : lo + (b > a ? Math.min(1, Math.max(0, (nota - a) / (b - a))) : 0);
  return Math.min(99, Math.max(0, Math.floor((f / 20 - p) * 100)));
}
/** O "melhor que X% dos trios" e, dentro desse X%, onde ele está (0 a 99). */
export function posicaoDoTrio(team: readonly string[]): { pct: number; dentro: number } {
  const nota = notaDoTrio(team);
  return { pct: percentilDaNota(nota), dentro: dentroDaFaixa(nota) };
}
/*
 * As estrelas do time, de 1 a 7, pela porcentagem de trios que ele supera. Os cortes ficam onde a chance de vencer a
 * jornada mais sobe (pedido do dono: "aqui deu um salto, aqui faz sentido mudar de estrela"), com mais trios embaixo e o
 * 7★ só no topo 2%. Medido em 60.000 jornadas de trios sorteados (motor das habilidades que só miram quem acertam):
 *   1★ até 24% (vence 1,6%) · 2★ 24–38% (4,6%) · 3★ 38–56% (8,1%) · 4★ 56–75% (14,1%) · 5★ 75–89% (25,7%)
 *   · 6★ 89–98% (44%) · 7★ 98%+ (55%) — medido de novo com o Freeza e o Doutor Destino sem a ordem escondida
 */
export const ESTRELAS_MAXIMAS = 7;
export const CORTES_DAS_ESTRELAS: readonly number[] = [24, 38, 56, 75, 89, 98];
export const estrelasDaPorcentagem = (p: number) => 1 + CORTES_DAS_ESTRELAS.filter((c) => p >= c).length;
export const estrelasDoTime = (t: readonly string[]) => estrelasDaPorcentagem(melhorQueOsTrios(t));
/** As estrelas de um trio com esta nota. */
export const estrelasDaNota = (nota: number) => estrelasDaPorcentagem(percentilDaNota(nota));
/* de logit para pontos de vitória, perto de 50% (para a explicação) */
const pontos = (z: number) => Math.round(25 * Math.abs(z));

const aguenta = (id: string) => byId[id]!.hp >= VIDA_MEDIANA * 1.12 || papelDe(id).cuida;

/*
 * As combinações entre dois personagens (A ajuda B), com a frase e o peso
 * medido. Só entram as que de fato ganham lutas nas simulações (peso > 0):
 * as outras soam bem no papel, mas não mudam o resultado — a dica não ensina
 * o que não funciona.
 */
function combinacoes(a: string, b: string): { chave: string; texto: string; peso: number }[] {
  const pa = papelDe(a), pb = papelDe(b), A = nome(a), B = nome(b);
  const lista: { chave: string; texto: string; peso: number }[] = [];
  const poe = (chave: string, texto: string) => { const peso = PESO_DA_LIGACAO[chave] ?? 0; if (peso > 0) lista.push({ chave, texto, peso }); };
  if (pa.cuida && pb.fragil) poe('cuida-fragil', t('{A} cura e protege {B}, que tem pouca Vida', { A, B }));
  if (pa.daCarga && pb.golpeGrande) poe('carga-golpe', t('{A} enche a Carga do golpe grande de {B}', { A, B }));
  if (pa.abre && pb.precisaVulneravel) poe('abre-vulneravel', t('{A} deixa o rival vulnerável para {B} atacar', { A, B }));
  if (pa.forte && pb.precisaFerido) poe('abre-ferido', t('{A} fere os rivais e {B} finaliza quem está ferido', { A, B }));
  if (pa.reforca && pb.forte) poe('reforca-forte', t('{A} reforça {B}, que já bate forte', { A, B }));
  if (pa.adianta && pb.golpeGrande) poe('adianta-golpe', t('{A} adianta a vez e o golpe grande de {B} sai antes', { A, B }));
  if (pa.cuida && pb.vinganca) poe('protege-vinganca', t('{A} segura {B} de pé, e {B} fica mais forte apanhando', { A, B }));
  if (pa.prende && pb.forte) poe('controla-dano', t('{A} prende os rivais enquanto {B} bate', { A, B }));
  if (pa.aplicaStatus && pb.reageAStatus) poe('status-gatilho', t('{A} põe Status nos rivais, e isso ativa {B}', { A, B }));
  if (pa.provoca && pb.fragil) poe('provoca-fragil', t('{A} provoca e puxa os golpes que iriam em {B}', { A, B }));
  if (pa.levanta && pb.forte) poe('levanta-forte', t('{A} levanta {B} se ele cair', { A, B }));
  if (pa.purifica && pb.forte) poe('limpa-forte', t('{A} limpa os Status ruins e {B} segue batendo', { A, B }));
  return lista;
}

/* Quando os dois se ajudam do mesmo jeito, uma frase só. */
const MUTUO: Record<string, (a: string, b: string) => string> = {
  'cuida-fragil': (a, b) => t('{a} e {b} se curam e se protegem', { a, b }),
  'carga-golpe': (a, b) => t('{a} e {b} enchem a Carga um do outro', { a, b }),
  'abre-vulneravel': (a, b) => t('{a} e {b} abrem os rivais um para o outro', { a, b }),
  'protege-vinganca': (a, b) => t('{a} e {b} se seguram de pé e crescem apanhando', { a, b }),
};

/* o que cada tipo de ponto fraco pede de um combo para pesar menos */
const AJUDA_NO_FRACO: Partial<Record<TipoDeFraqueza, { chaves: string[]; da: string }>> = {
  dano: { chaves: ['dano', 'basico'], da: tx('mais dano') }, espalha: { chaves: ['dano', 'basico'], da: tx('mais dano') },
  cai: { chaves: ['vida', 'defesa', 'escudo'], da: tx('mais Vida ou proteção') }, golpe: { chaves: ['vida', 'defesa', 'escudo'], da: tx('mais Vida ou proteção') },
  apanhar: { chaves: ['vida', 'defesa', 'escudo'], da: tx('mais Vida ou proteção') },
  lento: { chaves: ['ritmo'], da: tx('mais ritmo') }, demora: { chaves: ['ritmo', 'carga'], da: tx('mais ritmo e Carga') },
  rara: { chaves: ['carga', 'preparo'], da: tx('mais Carga') }, espera: { chaves: ['carga', 'preparo'], da: tx('mais Carga') }, preparo: { chaves: ['preparo', 'carga'], da: tx('Preparo mais rápido') },
};

/* `encaixe`: a porcentagem final dele (já com tudo descontado), para não avisar de algo que ela já conta */
function motivosDe(c: string, time: string[], encaixe = 50): MotivoOrdenado[] {
  const motivos: MotivoOrdenado[] = [];
  const mal = time.length > 0 && encaixe < 60, contra = encaixe < 35 ? 80 : 7;  // abaixo de 60%: o que pesa contra, explicado
  const trio = lista3(time.map(nome));
  const fraco = pontoFraco(byId[c]!)[0];
  let ajudaNoFraco: string | undefined;
  /*
   * Os combos de verdade que ele acende com quem já está no trio (os que a luta usa), dos que mais ganham
   * lutas para os que menos (o peso medido em 4 milhões de lutas).
   */
  if (time.length) {
    const antes = new Set(combosDoTrio(time).combos.map(chaveDoCombo));
    const novos = combosDoTrio([...time, c]).combos.filter((x) => !antes.has(chaveDoCombo(x)));
    for (const x of novos) {
      const com = [...new Set([...x.de, ...x.para])].filter((id) => id !== c).map(nome);
      const peso = PESO_DA_LIGACAO[x.id.startsWith('lenda-') ? 'lenda' : x.id] ?? 0.3;
      motivos.push({ texto: com.length ? t('Forma o combo {combo} com {quem}', { combo: t(x.nome), quem: lista3(com) }) : t('Forma o combo {combo}', { combo: t(x.nome) }), tom: 'bom', grupo: 'trio', ordem: 30 + peso * 20, porque: `${t(x.nome)}: ${t(x.texto)}`, resumo: t('combo {combo}', { combo: t(x.nome) }), combo: true });
      const ajuda = fraco && AJUDA_NO_FRACO[fraco.tipo];
      if (ajuda && !ajudaNoFraco && ajuda.chaves.some((k) => ((x.bonus as Record<string, number | undefined>)[k] ?? 0) > 0)) ajudaNoFraco = t('neste trio isso pesa menos: o combo {combo} dá {da}', { combo: t(x.nome), da: t(ajuda.da) });
    }
    if (!novos.length && mal) motivos.push({ texto: t('Não forma combo com {trio}', { trio }), tom: 'alerta', grupo: 'trio', ordem: contra + 2, porque: t('Os combos dão dano, Vida e proteção a mais na luta — é o que mais puxa a porcentagem para cima, e {nome} não acende nenhum com este trio', { nome: nome(c) }), resumo: t('não forma combo com {trio}', { trio }) });
    // o que a dupla rende além dos combos, medido: as habilidades de um ajudam (ou atrapalham) as do outro
    for (const m of time) {
      const z = ajusteDaDupla(c, m);
      if (z >= 0.2) motivos.push({ texto: t('Rende mais junto com {m} do que os dois separados', { m: nome(m) }), tom: 'bom', grupo: 'trio', ordem: 26 + z * 10, porque: t('Além dos combos, as habilidades de {c} e {m} se ajudam — a dupla vence uns {n} pontos a mais do que o esperado', { c: nome(c), m: nome(m), n: pontos(z) }), resumo: t('rende mais com {m}', { m: nome(m) }) });
      // o que atrapalha já está descontado na porcentagem: só vira aviso para quem encaixa mal (pedido do jogador:
      // "como ele pode ser melhor que 89% e ainda ser uma escolha ruim?")
      else if (z <= -0.12 && mal) motivos.push({ texto: t('Com {m} rende menos do que parece', { m: nome(m) }), tom: 'alerta', grupo: 'trio', ordem: contra + 1 - z, porque: t('As habilidades de {c} e {m} atrapalham uma à outra — a dupla vence uns {n} pontos a menos do que o esperado', { c: nome(c), m: nome(m), n: pontos(z) }), resumo: t('rende menos com {m}', { m: nome(m) }) });
    }
    // a dupla medida: com quem já está no trio, se for uma das três melhores dele (ou dele com o candidato)
    for (const m of time) {
      const ida = DUPLAS[c]?.parceiros.find(([p]) => p === m), volta = DUPLAS[m]?.parceiros.find(([p]) => p === c);
      const r = ida?.[1] ?? volta?.[1];
      if (r !== undefined) motivos.push({ texto: t('Dupla de ouro com {m}: juntos vencem {p} das lutas', { m: nome(m), p: pct(r) }), tom: 'bom', grupo: 'trio', ordem: 28, porque: t('{c} e {m} estão entre as três melhores duplas de {de}', { c: nome(c), m: nome(m), de: ida ? nome(c) : nome(m) }), resumo: t('dupla de ouro com {m}', { m: nome(m) }) });
    }
  }
  // a força dele, medida: o trio com ele vence quanto, e em que posição isso o põe no elenco
  const solo = DUPLAS[c]?.solo;
  if (solo !== undefined) {
    const p = percentil(SOLOS, solo);
    if (p >= 70) motivos.push({ texto: t('Forte em qualquer trio: com {nome}, o trio vence {p} das lutas', { nome: nome(c), p: pct(solo) }), tom: 'bom', grupo: 'dele', ordem: time.length ? 9 : 25, porque: t('Mais que {p}% do elenco, com dois parceiros quaisquer', { p }), resumo: t('forte em qualquer trio') });
    // fraco sozinho, mas encaixando bem neste trio: é justamente por isso que vale a pena (não é aviso)
    else if (p < 12 && time.length && encaixe >= 60) motivos.push({ texto: t('Sozinho é fraco, mas com {trio} encaixa bem', { trio }), tom: 'bom', grupo: 'trio', ordem: 8, porque: t('Com dois parceiros quaisquer, o trio dele vence só {p} das lutas; com este trio ele rende bem mais', { p: pct(solo) }) });
    else if (p < 12 || (mal && p < 30)) motivos.push({ texto: t('Sozinho rende pouco: precisa de parceiros que combinem'), tom: 'alerta', grupo: 'dele', ordem: mal ? contra : time.length ? 1 : 17, porque: t('Com dois parceiros quaisquer, o trio com {nome} vence {p} das lutas, menos que {resto}% do elenco', { nome: nome(c), p: pct(solo), resto: 100 - p }), resumo: t('rende pouco sozinho'), soloFraco: true });
  }
  // sem trio ainda: com quem ele vence mais
  if (!time.length && DUPLAS[c]?.parceiros.length) {
    const ps = DUPLAS[c]!.parceiros;
    motivos.push({ texto: t('Combina mais com {quem}', { quem: lista3(ps.map(([p]) => nome(p))) }), tom: 'bom', grupo: 'dele', ordem: 18, porque: t('As duplas que mais vencem: {lista}', { lista: ps.map(([p, r]) => t('com {nome}, {p}', { nome: nome(p), p: pct(r) })).join('; ') }), resumo: t('combina com {quem}', { quem: lista3(ps.map(([p]) => nome(p))) }) });
  }
  // combinações com quem já está no trio, das que mais ganham lutas para as que menos
  for (const m of time) {
    const ida = combinacoes(c, m), volta = combinacoes(m, c);
    for (const x of ida) {
      const par = volta.find((y) => y.chave === x.chave);
      const porque = [porQue(x.chave, c, m), par ? porQue(x.chave, m, c) : undefined].filter(Boolean).join('. ');
      motivos.push({ texto: (par && MUTUO[x.chave]?.(nome(c), nome(m))) || x.texto, tom: 'bom', grupo: 'trio', ordem: 10 + (par ? 2 : 1) * x.peso * 100, ...(porque ? { porque } : {}) });
    }
    for (const y of volta) if (!ida.some((x) => x.chave === y.chave)) {
      const porque = porQue(y.chave, m, c);
      motivos.push({ texto: y.texto, tom: 'bom', grupo: 'trio', ordem: 10 + y.peso * 100, ...(porque ? { porque } : {}) });
    }
  }
  // o que falta no trio: quem traz, ou (para quem encaixa mal) quem também não traz
  if (time.length) {
    const temQuemAguente = time.some(aguenta), temQuemCure = time.some((m) => papelDe(m).cuida);
    if (!temQuemAguente && aguenta(c)) motivos.push({ texto: t('Seu trio ainda não tem quem segure dano: {nome} aguenta', { nome: nome(c) }), tom: 'bom', grupo: 'trio', ordem: 14, resumo: t('segura o dano que o trio não aguenta') });
    else if (!temQuemAguente && mal) motivos.push({ texto: t('O trio não tem quem segure dano, e {nome} também não aguenta', { nome: nome(c) }), tom: 'alerta', grupo: 'trio', ordem: contra - 0.5, resumo: t('não segura dano') });
    if (!temQuemCure && papelDe(c).cuida) motivos.push({ texto: t('Ninguém do trio cura ou protege: {nome} faz isso', { nome: nome(c) }), tom: 'bom', grupo: 'trio', ordem: 13, resumo: t('traz a cura que falta') });
    else if (!temQuemCure && mal) motivos.push({ texto: t('Ninguém do trio cura ou protege, e {nome} também não', { nome: nome(c) }), tom: 'alerta', grupo: 'trio', ordem: contra - 0.6, resumo: t('não traz a cura que falta') });
    if (!time.some((m) => papelDe(m).forte) && papelDe(c).forte) motivos.push({ texto: t('Traz o dano forte que falta no trio'), tom: 'bom', grupo: 'trio', ordem: 12, resumo: t('traz o dano forte que falta') });
    if (time.every((m) => papelDe(m).fragil) && papelDe(c).fragil && !papelDe(c).cuida && mal) motivos.push({ texto: t('Mais um de pouca Vida: o trio pode cair rápido'), tom: 'alerta', grupo: 'trio', ordem: contra - 0.4, resumo: t('mais um de pouca Vida') });
  }
  /*
   * O que é dele (vale em qualquer trio): o ponto forte, com a habilidade que faz isso, e o ponto fraco, como
   * cuidado — e, se um combo deste trio ajuda justamente nesse ponto fraco, a explicação diz.
   */
  const fortes = pontoForte(byId[c]!);
  fortes.forEach((f, i) => motivos.push({ texto: `${t(f.rotulo)}: ${minuscula(t(f.motivo))}`, tom: 'bom', grupo: 'dele', ordem: (time.length ? 6 : 20) - i * 3, resumo: t(f.rotulo).charAt(0).toLowerCase() + t(f.rotulo).slice(1) }));
  if (fraco) {
    const rotulo = t(fraco.rotulo).charAt(0).toLowerCase() + t(fraco.rotulo).slice(1);
    // para quem encaixa mal, o ponto fraco que nenhum combo do trio compensa também entra no "Por que não é a melhor"
    motivos.push({ texto: t('Cuidado: {rotulo} — {motivo}', { rotulo, motivo: minuscula(t(fraco.motivo)) }), tom: 'alerta', grupo: 'dele', ordem: time.length ? 0.5 : 16, ...(ajudaNoFraco ? { porque: ajudaNoFraco.charAt(0).toUpperCase() + ajudaNoFraco.slice(1) } : {}), ...(mal && !ajudaNoFraco ? { resumo: rotulo } : {}) });
  }
  // os motivos repetidos (o mesmo combo por dois caminhos) ficam uma vez só
  const vistos = new Set<string>();
  return motivos.sort((a, b) => b.ordem - a.ordem).filter((m) => (vistos.has(m.texto) ? false : (vistos.add(m.texto), true)));
}

/*
 * "Por que escolher Vegeta: combo Dupla de Dragon Ball · dupla de ouro com Goku · traz o dano forte que falta"
 * (pedido do jogador: "é melhor por causa disso, disso e disso"). No máximo dois combos, para variar os motivos.
 * E o espelho, para quem encaixa abaixo de 60%: "Por que não é a melhor: não forma combo com… · …".
 */
function resumoDe(c: string, motivos: MotivoOrdenado[], tom: 'bom' | 'alerta' = 'bom'): MotivoOrdenado | undefined {
  const razoes: string[] = [];
  let combos = 0;
  for (const m of motivos) {
    if (m.tom !== tom || !m.resumo || razoes.includes(m.resumo)) continue;
    if (m.combo && combos >= 2) continue;
    if (m.combo) combos++;
    razoes.push(m.resumo);
    if (razoes.length === 3) break;
  }
  if (!razoes.length) return undefined;
  return tom === 'bom'
    ? { texto: t('Por que escolher {nome}: {razoes}', { nome: nome(c), razoes: razoes.join(' · ') }), tom: 'bom', grupo: 'trio', ordem: 100 }
    : { texto: t('Por que não é a melhor: {razoes}', { razoes: razoes.join(' · ') }), tom: 'alerta', grupo: 'trio', ordem: 99 };
}

/** As dicas para os candidatos da vez. `fora`: quem não pode entrar (o trio e os banidos). */
export function dicasDoDraft(candidatos: string[], time: string[], fora: string[] = []): DicaDoCandidato[] {
  // sem trio ainda: quanto o trio com ele vence com dois parceiros quaisquer (medido, com os combos) — a mesma
  // medida do "Forte em qualquer trio" e do "Sozinho rende pouco", para a porcentagem e o texto não se contradizerem
  const nota = (id: string) => (time.length ? notaDoTrio([...time, id]) : DUPLAS[id]?.solo ?? 0.5 + (FORCA[id] ?? 0) / 10);
  const pool = characters.map((c) => c.id).filter((id) => !time.includes(id) && !fora.includes(id)).map(nota).sort((a, b) => a - b);
  const notas = new Map(candidatos.map((id) => [id, nota(id)]));
  const melhor = candidatos.reduce((a, b) => (notas.get(b)! > notas.get(a)! ? b : a), candidatos[0]!);
  const lista = candidatos.map((id) => {
    const encaixe = Math.min(99, percentil(pool, notas.get(id)!));
    const motivos = motivosDe(id, time, encaixe);
    const aFavor = encaixe >= 35 ? resumoDe(id, motivos) : undefined;
    let contra = time.length && encaixe < 60 ? resumoDe(id, motivos, 'alerta') : undefined;
    // nada específico contra e ainda assim abaixo de 60%: diz que há quem combine mais (e qual, logo abaixo)
    if (!contra && time.length && encaixe < 60) contra = { texto: encaixe < 35 ? t('Encaixa pouco: há opções bem melhores para este trio') : t('Por que não é a melhor: há quem combine mais com {trio}', { trio: lista3(time.map(nome)) }), tom: 'alerta', grupo: 'trio', ordem: 99 };
    if (contra && id !== melhor) contra.porque = t('Entre as opções de agora, {nome} encaixa {p}%', { nome: nome(melhor), p: Math.min(99, percentil(pool, notas.get(melhor)!)) });
    // sem trio ainda e mais fraco que a maioria: o aviso vem primeiro, dizendo com quem ele vale a pena
    if (!time.length && encaixe < 35 && !motivos.some((m) => m.soloFraco)) {
      const ps = DUPLAS[id]?.parceiros.map(([p]) => nome(p)) ?? [];
      motivos.unshift({ texto: ps.length ? t('Sozinho é mais fraco que a maioria: vale a pena com {quem}', { quem: lista3(ps) }) : t('Sozinho é mais fraco que a maioria'), tom: 'alerta', grupo: 'dele', ordem: 99 });
    }
    // abaixo de 35%: primeiro o porquê de não ser boa; entre 35% e 60%: os dois lados; de 60% para cima: só o a favor
    const topo = [aFavor, contra].filter((m): m is MotivoOrdenado => !!m);
    const detalhe = [...topo, ...motivos];
    const limpa = (l: MotivoOrdenado[]) => l.map(({ texto, tom }) => ({ texto, tom }));
    // na explicação maior, cada combinação vem com o porquê (a habilidade que liga a outra)
    const explica = (l: MotivoOrdenado[]) => l.map(({ texto, tom, porque, grupo }) => ({ texto, tom, ...(porque ? { porque } : {}), ...(grupo ? { grupo } : {}) }));
    // no cartão: abaixo de 35%, o principal contra primeiro
    const cartao = encaixe < 35 && contra ? [contra, ...motivos] : motivos;
    return { id, encaixe, curtos: limpa(cartao.slice(0, 2)), detalhe: explica(detalhe) };
  });
  return lista.map((d) => ({ id: d.id, encaixe: d.encaixe, curtos: d.curtos, detalhe: d.detalhe, melhor: d.id === melhor }));
}
