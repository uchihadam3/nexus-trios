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
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { pontoFraco, type TipoDeFraqueza } from '../data/ponto-fraco';
import { pontoForte } from '../data/ponto-forte';
import { forcaDoTrio } from '../engine/campaign';
import { combosDoTrio } from '../engine/combos';
import { papelDe } from '../engine/sinergia';
import { porQue } from './porque';

export interface Motivo {
  texto: string; tom: 'bom' | 'alerta';
  /** o porquê, com as habilidades (na explicação maior) */
  porque?: string;
  /** 'trio': é da combinação com quem já está no trio; 'dele': é do próprio personagem, vale em qualquer trio */
  grupo?: 'trio' | 'dele';
}
/* `resumo`: o motivo em poucas palavras, para a frase "Escolha X porque …, … e …" */
type MotivoOrdenado = Motivo & { ordem: number; resumo?: string };
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
const PRIMEIRO = (id: string) => byId[id]!.name.split(/[ ,]/)[0]!;
const REPETIDOS = new Set(characters.map((c) => PRIMEIRO(c.id)).filter((n, i, l) => l.indexOf(n) !== i));
const nome = (id: string) => (REPETIDOS.has(PRIMEIRO(id)) ? byId[id]!.name.split(/[ ,]/).slice(0, 2).join(' ') : PRIMEIRO(id));
/* "É o primeiro a cair…" vira "é o primeiro a cair…" depois dos dois-pontos; nome de habilidade fica como está */
const minuscula = (t: string) => (/^(É|Só|Bate|Em|A|Fica|Derruba|Corta|Põe|Solta|Adianta|As|Mantém|Segura|Nenhum) /.test(t) ? t.charAt(0).toLowerCase() + t.slice(1) : t);
const VIDAS = characters.map((c) => c.hp).sort((a, b) => a - b);
const VIDA_MEDIANA = VIDAS[Math.floor(VIDAS.length / 2)]!;
const percentil = (lista: number[], x: number) => Math.round((100 * lista.filter((v) => v < x).length) / Math.max(1, lista.length));

/* quanto o trio com ele vence (com dois parceiros quaisquer), e em que posição isso o põe no elenco */
const SOLOS = Object.values(DUPLAS).map((d) => d.solo).sort((a, b) => a - b);
const pct = (x: number) => `${Math.round(100 * x)}%`;
const lista3 = (l: string[]) => (l.length > 1 ? `${l.slice(0, -1).join(', ')} e ${l.at(-1)}` : l[0] ?? '');
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
 * As estrelas do time, de 1 a 7, pela porcentagem de trios que ele supera. Os cortes ficam onde a chance de vencer a
 * jornada mais sobe (pedido do dono: "aqui deu um salto, aqui faz sentido mudar de estrela"), com mais trios embaixo e o
 * 7★ só no topo 2%. Medido em 42.000 jornadas (rivais a 90% da Vida, Vida acima do topo 0,25):
 *   1★ até 24% (vence 1,5%) · 2★ 24–38% (5%) · 3★ 38–56% (8%) · 4★ 56–75% (14,5%) · 5★ 75–89% (25,5%) · 6★ 89–98% (43%)
 *   · 7★ 98%+ (59%)
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
  if (pa.cuida && pb.fragil) poe('cuida-fragil', `${A} cura e protege ${B}, que tem pouca Vida`);
  if (pa.daCarga && pb.golpeGrande) poe('carga-golpe', `${A} enche a Carga do golpe grande de ${B}`);
  if (pa.abre && pb.precisaVulneravel) poe('abre-vulneravel', `${A} deixa o rival vulnerável para ${B} atacar`);
  if (pa.forte && pb.precisaFerido) poe('abre-ferido', `${A} fere os rivais e ${B} finaliza quem está ferido`);
  if (pa.reforca && pb.forte) poe('reforca-forte', `${A} reforça ${B}, que já bate forte`);
  if (pa.adianta && pb.golpeGrande) poe('adianta-golpe', `${A} adianta a vez e o golpe grande de ${B} sai antes`);
  if (pa.cuida && pb.vinganca) poe('protege-vinganca', `${A} segura ${B} de pé, e ${B} fica mais forte apanhando`);
  if (pa.prende && pb.forte) poe('controla-dano', `${A} prende os rivais enquanto ${B} bate`);
  if (pa.aplicaStatus && pb.reageAStatus) poe('status-gatilho', `${A} põe Status nos rivais, e isso ativa ${B}`);
  if (pa.provoca && pb.fragil) poe('provoca-fragil', `${A} provoca e puxa os golpes que iriam em ${B}`);
  if (pa.levanta && pb.forte) poe('levanta-forte', `${A} levanta ${B} se ele cair`);
  if (pa.purifica && pb.forte) poe('limpa-forte', `${A} limpa os Status ruins e ${B} segue batendo`);
  return lista;
}

/* Quando os dois se ajudam do mesmo jeito, uma frase só. */
const MUTUO: Record<string, (a: string, b: string) => string> = {
  'cuida-fragil': (a, b) => `${a} e ${b} se curam e se protegem`,
  'carga-golpe': (a, b) => `${a} e ${b} enchem a Carga um do outro`,
  'abre-vulneravel': (a, b) => `${a} e ${b} abrem os rivais um para o outro`,
  'protege-vinganca': (a, b) => `${a} e ${b} se seguram de pé e crescem apanhando`,
};

/* o que cada tipo de ponto fraco pede de um combo para pesar menos */
const AJUDA_NO_FRACO: Partial<Record<TipoDeFraqueza, { chaves: string[]; da: string }>> = {
  dano: { chaves: ['dano', 'basico'], da: 'mais dano' }, espalha: { chaves: ['dano', 'basico'], da: 'mais dano' },
  cai: { chaves: ['vida', 'defesa', 'escudo'], da: 'mais Vida ou proteção' }, golpe: { chaves: ['vida', 'defesa', 'escudo'], da: 'mais Vida ou proteção' },
  apanhar: { chaves: ['vida', 'defesa', 'escudo'], da: 'mais Vida ou proteção' },
  lento: { chaves: ['ritmo'], da: 'mais ritmo' }, demora: { chaves: ['ritmo', 'carga'], da: 'mais ritmo e Carga' },
  rara: { chaves: ['carga', 'preparo'], da: 'mais Carga' }, espera: { chaves: ['carga', 'preparo'], da: 'mais Carga' }, preparo: { chaves: ['preparo', 'carga'], da: 'Preparo mais rápido' },
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
      motivos.push({ texto: `Forma o combo ${x.nome}${com.length ? ` com ${lista3(com)}` : ''}`, tom: 'bom', grupo: 'trio', ordem: 30 + peso * 20, porque: `${x.nome}: ${x.texto}`, resumo: `combo ${x.nome}` });
      const ajuda = fraco && AJUDA_NO_FRACO[fraco.tipo];
      if (ajuda && !ajudaNoFraco && ajuda.chaves.some((k) => ((x.bonus as Record<string, number | undefined>)[k] ?? 0) > 0)) ajudaNoFraco = `neste trio isso pesa menos: o combo ${x.nome} dá ${ajuda.da}`;
    }
    if (!novos.length && mal) motivos.push({ texto: `Não forma combo com ${trio}`, tom: 'alerta', grupo: 'trio', ordem: contra + 2, porque: `Os combos dão dano, Vida e proteção a mais na luta — é o que mais puxa a porcentagem para cima, e ${nome(c)} não acende nenhum com este trio`, resumo: `não forma combo com ${trio}` });
    // o que a dupla rende além dos combos, medido: as habilidades de um ajudam (ou atrapalham) as do outro
    for (const m of time) {
      const z = ajusteDaDupla(c, m);
      if (z >= 0.2) motivos.push({ texto: `Rende mais junto com ${nome(m)} do que os dois separados`, tom: 'bom', grupo: 'trio', ordem: 26 + z * 10, porque: `Além dos combos, as habilidades de ${nome(c)} e ${nome(m)} se ajudam — a dupla vence uns ${pontos(z)} pontos a mais do que o esperado`, resumo: `rende mais com ${nome(m)}` });
      // o que atrapalha já está descontado na porcentagem: só vira aviso para quem encaixa mal (pedido do jogador:
      // "como ele pode ser melhor que 89% e ainda ser uma escolha ruim?")
      else if (z <= -0.12 && mal) motivos.push({ texto: `Com ${nome(m)} rende menos do que parece`, tom: 'alerta', grupo: 'trio', ordem: contra + 1 - z, porque: `As habilidades de ${nome(c)} e ${nome(m)} atrapalham uma à outra — a dupla vence uns ${pontos(z)} pontos a menos do que o esperado`, resumo: `rende menos com ${nome(m)}` });
    }
    // a dupla medida: com quem já está no trio, se for uma das três melhores dele (ou dele com o candidato)
    for (const m of time) {
      const ida = DUPLAS[c]?.parceiros.find(([p]) => p === m), volta = DUPLAS[m]?.parceiros.find(([p]) => p === c);
      const r = ida?.[1] ?? volta?.[1];
      if (r !== undefined) motivos.push({ texto: `Dupla de ouro com ${nome(m)}: juntos vencem ${pct(r)} das lutas`, tom: 'bom', grupo: 'trio', ordem: 28, porque: `${nome(c)} e ${nome(m)} estão entre as três melhores duplas ${ida ? `de ${nome(c)}` : `de ${nome(m)}`}`, resumo: `dupla de ouro com ${nome(m)}` });
    }
  }
  // a força dele, medida: o trio com ele vence quanto, e em que posição isso o põe no elenco
  const solo = DUPLAS[c]?.solo;
  if (solo !== undefined) {
    const p = percentil(SOLOS, solo);
    if (p >= 70) motivos.push({ texto: `Forte em qualquer trio: com ${nome(c)}, o trio vence ${pct(solo)} das lutas`, tom: 'bom', grupo: 'dele', ordem: time.length ? 9 : 25, porque: `Mais que ${p}% do elenco, com dois parceiros quaisquer`, resumo: 'forte em qualquer trio' });
    // fraco sozinho, mas encaixando bem neste trio: é justamente por isso que vale a pena (não é aviso)
    else if (p < 12 && time.length && encaixe >= 60) motivos.push({ texto: `Sozinho é fraco, mas com ${trio} encaixa bem`, tom: 'bom', grupo: 'trio', ordem: 8, porque: `Com dois parceiros quaisquer, o trio dele vence só ${pct(solo)} das lutas; com este trio ele rende bem mais` });
    else if (p < 12 || (mal && p < 30)) motivos.push({ texto: `Sozinho rende pouco: precisa de parceiros que combinem`, tom: 'alerta', grupo: 'dele', ordem: mal ? contra : time.length ? 1 : 17, porque: `Com dois parceiros quaisquer, o trio com ${nome(c)} vence ${pct(solo)} das lutas, menos que ${100 - p}% do elenco`, resumo: 'rende pouco sozinho' });
  }
  // sem trio ainda: com quem ele vence mais
  if (!time.length && DUPLAS[c]?.parceiros.length) {
    const ps = DUPLAS[c]!.parceiros;
    motivos.push({ texto: `Combina mais com ${lista3(ps.map(([p]) => nome(p)))}`, tom: 'bom', grupo: 'dele', ordem: 18, porque: `As duplas que mais vencem: ${ps.map(([p, r]) => `com ${nome(p)}, ${pct(r)}`).join('; ')}`, resumo: `combina com ${lista3(ps.map(([p]) => nome(p)))}` });
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
    if (!temQuemAguente && aguenta(c)) motivos.push({ texto: `Seu trio ainda não tem quem segure dano: ${nome(c)} aguenta`, tom: 'bom', grupo: 'trio', ordem: 14, resumo: 'segura o dano que o trio não aguenta' });
    else if (!temQuemAguente && mal) motivos.push({ texto: `O trio não tem quem segure dano, e ${nome(c)} também não aguenta`, tom: 'alerta', grupo: 'trio', ordem: contra - 0.5, resumo: 'não segura dano' });
    if (!temQuemCure && papelDe(c).cuida) motivos.push({ texto: `Ninguém do trio cura ou protege: ${nome(c)} faz isso`, tom: 'bom', grupo: 'trio', ordem: 13, resumo: 'traz a cura que falta' });
    else if (!temQuemCure && mal) motivos.push({ texto: `Ninguém do trio cura ou protege, e ${nome(c)} também não`, tom: 'alerta', grupo: 'trio', ordem: contra - 0.6, resumo: 'não traz a cura que falta' });
    if (!time.some((m) => papelDe(m).forte) && papelDe(c).forte) motivos.push({ texto: `Traz o dano forte que falta no trio`, tom: 'bom', grupo: 'trio', ordem: 12, resumo: 'traz o dano forte que falta' });
    if (time.every((m) => papelDe(m).fragil) && papelDe(c).fragil && !papelDe(c).cuida && mal) motivos.push({ texto: `Mais um de pouca Vida: o trio pode cair rápido`, tom: 'alerta', grupo: 'trio', ordem: contra - 0.4, resumo: 'mais um de pouca Vida' });
  }
  /*
   * O que é dele (vale em qualquer trio): o ponto forte, com a habilidade que faz isso, e o ponto fraco, como
   * cuidado — e, se um combo deste trio ajuda justamente nesse ponto fraco, a explicação diz.
   */
  const fortes = pontoForte(byId[c]!);
  fortes.forEach((f, i) => motivos.push({ texto: `${f.rotulo}: ${minuscula(f.motivo)}`, tom: 'bom', grupo: 'dele', ordem: (time.length ? 6 : 20) - i * 3, resumo: f.rotulo.charAt(0).toLowerCase() + f.rotulo.slice(1) }));
  if (fraco) {
    const rotulo = fraco.rotulo.charAt(0).toLowerCase() + fraco.rotulo.slice(1);
    // para quem encaixa mal, o ponto fraco que nenhum combo do trio compensa também entra no "Por que não é a melhor"
    motivos.push({ texto: `Cuidado: ${rotulo} — ${minuscula(fraco.motivo)}`, tom: 'alerta', grupo: 'dele', ordem: time.length ? 0.5 : 16, ...(ajudaNoFraco ? { porque: ajudaNoFraco.charAt(0).toUpperCase() + ajudaNoFraco.slice(1) } : {}), ...(mal && !ajudaNoFraco ? { resumo: rotulo } : {}) });
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
  for (const m of motivos) {
    if (m.tom !== tom || !m.resumo || razoes.includes(m.resumo)) continue;
    if (m.resumo.startsWith('combo ') && razoes.filter((r) => r.startsWith('combo ')).length >= 2) continue;
    razoes.push(m.resumo);
    if (razoes.length === 3) break;
  }
  if (!razoes.length) return undefined;
  return tom === 'bom'
    ? { texto: `Por que escolher ${nome(c)}: ${razoes.join(' · ')}`, tom: 'bom', grupo: 'trio', ordem: 100 }
    : { texto: `Por que não é a melhor: ${razoes.join(' · ')}`, tom: 'alerta', grupo: 'trio', ordem: 99 };
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
    if (!contra && time.length && encaixe < 60) contra = { texto: encaixe < 35 ? `Encaixa pouco: há opções bem melhores para este trio` : `Por que não é a melhor: há quem combine mais com ${lista3(time.map(nome))}`, tom: 'alerta', grupo: 'trio', ordem: 99 };
    if (contra && id !== melhor) contra.porque = `Entre as opções de agora, ${nome(melhor)} encaixa ${Math.min(99, percentil(pool, notas.get(melhor)!))}%`;
    // sem trio ainda e mais fraco que a maioria: o aviso vem primeiro, dizendo com quem ele vale a pena
    if (!time.length && encaixe < 35 && !motivos.some((m) => m.texto.startsWith('Sozinho rende pouco'))) {
      const ps = DUPLAS[id]?.parceiros.map(([p]) => nome(p)) ?? [];
      motivos.unshift({ texto: `Sozinho é mais fraco que a maioria${ps.length ? `: vale a pena com ${lista3(ps)}` : ''}`, tom: 'alerta', grupo: 'dele', ordem: 99 });
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
