/*
 * Dicas de trio — o "técnico" da escolha de personagens.
 *
 * Pedido do jogador: um botão que liga dicas na escolha do trio, bem
 * inteligentes, que ensinam qual personagem combina com qual — a melhor
 * escolha marcada, quanto (%) cada candidato encaixa no trio, um motivo curto
 * e, tocando, uma explicação maior. Quem usa as dicas aprende, mas pontua
 * menos: −25 mil por luta da jornada (src/engine/pontos.ts).
 *
 * Tudo vem do que foi medido em lutas simuladas, não de opinião:
 *   - a força de cada personagem e o peso de cada combinação
 *     (src/data/forca-dos-rivais.ts, scripts/medir-forca.ts);
 *   - os papéis lidos dos kits (src/engine/sinergia.ts): quem dá Carga, quem
 *     cura e protege, quem é frágil, quem bate forte, quem cresce apanhando…
 *
 * O "encaixe" é a posição do candidato entre todo o elenco disponível para
 * este trio: 88% = combina melhor com quem você já escolheu do que 88% dos
 * personagens que poderiam entrar.
 */
import { byId, characters } from '../data/characters';
import { FORCA, PESO_DA_LIGACAO } from '../data/forca-dos-rivais';
import { pontoFraco } from '../data/ponto-fraco';
import { forcaDoTrio } from '../engine/campaign';
import { papelDe } from '../engine/sinergia';
import { porQue } from './porque';

export interface Motivo { texto: string; tom: 'bom' | 'alerta'; /** o porquê, com as habilidades (na explicação maior) */ porque?: string }
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

const nome = (id: string) => byId[id]!.name.split(/[ ,]/)[0]!;
const VIDAS = characters.map((c) => c.hp).sort((a, b) => a - b);
const VIDA_MEDIANA = VIDAS[Math.floor(VIDAS.length / 2)]!;
const FORCAS = Object.values(FORCA).sort((a, b) => a - b);
const percentil = (lista: number[], x: number) => Math.round((100 * lista.filter((v) => v < x).length) / Math.max(1, lista.length));

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

function motivosDe(c: string, time: string[]): (Motivo & { ordem: number })[] {
  const motivos: (Motivo & { ordem: number })[] = [];
  // combinações com quem já está no trio, das que mais ganham lutas para as que menos
  for (const m of time) {
    const ida = combinacoes(c, m), volta = combinacoes(m, c);
    for (const x of ida) {
      const par = volta.find((y) => y.chave === x.chave);
      const porque = [porQue(x.chave, c, m), par ? porQue(x.chave, m, c) : undefined].filter(Boolean).join('. ');
      motivos.push({ texto: (par && MUTUO[x.chave]?.(nome(c), nome(m))) || x.texto, tom: 'bom', ordem: 10 + (par ? 2 : 1) * x.peso * 100, ...(porque ? { porque } : {}) });
    }
    for (const y of volta) if (!ida.some((x) => x.chave === y.chave)) {
      const porque = porQue(y.chave, m, c);
      motivos.push({ texto: y.texto, tom: 'bom', ordem: 10 + y.peso * 100, ...(porque ? { porque } : {}) });
    }
  }
  // o que falta no trio
  if (time.length) {
    if (!time.some(aguenta) && aguenta(c)) motivos.push({ texto: `Seu trio ainda não tem quem segure dano: ${nome(c)} aguenta`, tom: 'bom', ordem: 14 });
    if (!time.some((m) => papelDe(m).cuida) && papelDe(c).cuida) motivos.push({ texto: `Ninguém do trio cura ou protege: ${nome(c)} faz isso`, tom: 'bom', ordem: 13 });
    if (!time.some((m) => papelDe(m).forte) && papelDe(c).forte) motivos.push({ texto: `Traz o dano forte que falta no trio`, tom: 'bom', ordem: 12 });
    if (time.every((m) => papelDe(m).fragil) && papelDe(c).fragil && !papelDe(c).cuida) motivos.push({ texto: `Mais um de pouca Vida: o trio pode cair rápido`, tom: 'alerta', ordem: 11 });
  }
  // força sozinho, medida nas lutas
  const q = percentil(FORCAS, FORCA[c] ?? 0);
  if (q >= 85) motivos.push({ texto: `Um dos mais fortes do jogo`, tom: 'bom', ordem: time.length ? 9 : 20 });
  else if (q >= 60) motivos.push({ texto: `Forte mesmo sozinho`, tom: 'bom', ordem: time.length ? 5 : 15 });
  else if (q <= 20) motivos.push({ texto: `Fraco sozinho: precisa dos parceiros certos`, tom: 'alerta', ordem: time.length ? 4 : 15 });
  else motivos.push({ texto: `Força média sozinho`, tom: 'bom', ordem: time.length ? 1 : 15 });
  return motivos.sort((a, b) => b.ordem - a.ordem);
}

/** As dicas para os candidatos da vez. `fora`: quem não pode entrar (o trio e os banidos). */
export function dicasDoDraft(candidatos: string[], time: string[], fora: string[] = []): DicaDoCandidato[] {
  const nota = (id: string) => (time.length ? forcaDoTrio([...time, id]) : FORCA[id] ?? 0);
  const pool = characters.map((c) => c.id).filter((id) => !time.includes(id) && !fora.includes(id)).map(nota).sort((a, b) => a - b);
  const lista = candidatos.map((id) => {
    const encaixe = Math.min(99, percentil(pool, nota(id)));
    const motivos = motivosDe(id, time);
    // um candidato que encaixa mal começa pelo aviso, mesmo tendo alguma combinação
    if (time.length && encaixe < 35) motivos.unshift({ texto: `Encaixa pouco: há opções bem melhores para este trio`, tom: 'alerta', ordem: 99 });
    const fraco = pontoFraco(byId[id]!.vulnerability, byId[id])[0];
    const detalhe = fraco ? [...motivos, { texto: `Cuidado: fraco contra ${fraco.contra.toLowerCase()} — ${fraco.motivo.charAt(0).toLowerCase()}${fraco.motivo.slice(1)}`, tom: 'alerta' as const, ordem: 0 }] : motivos;
    const limpa = (l: typeof motivos) => l.map(({ texto, tom }) => ({ texto, tom }));
    // na explicação maior, cada combinação vem com o porquê (a habilidade que liga a outra)
    const explica = (l: typeof motivos) => l.map(({ texto, tom, porque }) => ({ texto, tom, ...(porque ? { porque } : {}) }));
    return { id, nota: nota(id), encaixe, curtos: limpa(motivos.slice(0, 2)), detalhe: explica(detalhe) };
  });
  const melhor = lista.reduce((a, b) => (b.nota > a.nota ? b : a), lista[0]!);
  return lista.map((d) => ({ id: d.id, encaixe: d.encaixe, curtos: d.curtos, detalhe: d.detalhe, melhor: d.id === melhor?.id }));
}
