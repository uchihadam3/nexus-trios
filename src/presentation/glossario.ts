/*
 * O glossário do jogo: cada termo que aparece nas fichas e na batalha, com o
 * que ele quer dizer em uma ou duas frases.
 *
 * A ficha mostrava a explicação na frente de cada efeito — "Aplica Confuso ·
 * 25% de chance do ataque básico atingir a si mesmo" — e com três ou quatro
 * efeitos por habilidade o cartão virava um parágrafo. Agora o cartão mostra
 * só o termo e o número; tocar no termo abre a explicação.
 */
import type { StatusId } from '../engine/types';
import { DEIXAM_VULNERAVEL, statuses } from '../data/statuses';

export interface Termo {
  id: string;
  nome: string;
  /** Cor do ponto e da borda do cartão. */
  cor: string;
  /** "Bom para quem recebe", "Ruim para quem recebe", ou uma categoria. */
  rotulo: string;
  /** O que faz, em linguagem de jogo. */
  texto: string;
  /** Uma linha a mais, quando ajuda (como acumula, um exemplo). */
  extra?: string;
  /** Formas como o termo aparece no texto (além do nome). */
  formas?: string[];
}

const pct = (x: number) => `${Math.round(x * 100)}%`;

/* O que cada Status faz, dito para quem nunca viu o jogo. */
const FAZ: Record<StatusId, string> = {
  exposed: 'Recebe mais dano de todo mundo enquanto durar.',
  marked: 'Fica na mira do trio rival: todos miram nele. Não aumenta o dano e não passa pelo Escudo — serve para o trio inteiro focar no mesmo alvo. Quem marca escolhe o rival que cai mais rápido.',
  electric: 'Choque: cada golpe que ele recebe empurra a próxima ação dele para trás. Não aumenta o dano.',
  paralyzed: 'Não ataca e o Preparo para de avançar. Perde a vez enquanto durar.',
  protected: 'Recebe menos dano. Com 30% ou mais, o Preparo também não pode ser interrompido.',
  slow: 'Demora mais para dar o próximo golpe e para preparar habilidades.',
  rooted: 'Preso no lugar: demora mais para agir. Soma com Lento.',
  haste: 'Dá o próximo golpe e prepara habilidades mais rápido.',
  confused: 'A cada ataque básico, 1 chance em 4 de acertar a si mesmo.',
  regen: 'Recupera Vida sozinho, a cada segundo.',
  burning: 'Perde Vida sozinho, a cada segundo, mesmo sem apanhar.',
  silenced: 'Não começa habilidades novas. O ataque básico continua.',
  strengthened: 'Causa mais dano em tudo: ataque básico e habilidades.',
  weakened: 'Causa menos dano em tudo.',
  vampirism: 'Cada golpe dele cura uma parte do dano que causou. Vale enquanto o Status durar.',
  reflect: 'Cada golpe recebido volta em parte para quem bateu, mesmo se o Escudo segurar.',
  thorns: 'Quem bate leva um dano fixo a cada golpe: pune quem ataca muitas vezes, como golpes rápidos e em área.',
  poison: 'Perde Vida a cada segundo, e o veneno passa por dentro: Escudo e Protegido não seguram. Aplicar de novo soma.',
  bleed: 'Cada vez que ele age (ataque básico ou habilidade), a ferida abre e ele perde Vida. Parado, não sangra.',
  cursed: 'Recebe menos cura e menos Escudo de todo mundo, inclusive dele mesmo.',
  frozen: 'Preso no gelo: não age. O próximo golpe direto quebra o gelo e entra mais forte.',
  sleep: 'Dorme: não age. Acorda quando o sono acaba ou quando leva um golpe direto (Queimadura e Veneno não acordam).',
  blind: 'Pode errar o ataque básico: o golpe passa longe e não faz nada.',
  summon: 'Uma criatura luta ao lado dele e ataca o rival mais ferido a cada 1,5 s. Não tem Vida nem pode ser alvo; some quando o tempo acaba, quando quem invocou cai ou com Dissipar.',
  bomb: 'Uma bomba-relógio grudada no rival: quando o tempo acaba, explode com o dano guardado. Aplicar de novo soma o dano. Purificar desarma.',
  evasion: 'A cada golpe de um rival, uma chance de escapar dele inteiro: nem dano, nem debuff entram. Golpes em todos também podem ser esquivados.',
  barrier: 'Anula os próximos debuffs que um rival tentar pôr nele. Cada debuff anulado gasta uma.',
  provoked: 'Só consegue mirar em quem provocou. Golpes em todos continuam iguais; se quem provocou cair, acaba na hora.',
};

const acumula = (id: StatusId) => {
  const s = statuses[id];
  if (s.stack !== 'add') return 'Aplicar de novo renova o tempo e fica o mais forte; não soma.';
  const teto = id === 'regen' || id === 'burning' ? `${s.cap} de Vida por segundo` : pct(s.cap);
  return `Cada aplicação soma com a anterior, até ${teto}.`;
};

const doStatus = (id: StatusId): Termo => ({
  id, nome: statuses[id].name, cor: statuses[id].color,
  rotulo: statuses[id].tone === 'positivo' ? 'STATUS BOM · para quem recebe' : 'STATUS RUIM · para quem recebe',
  texto: FAZ[id], extra: acumula(id),
  // "Invoca Gomorrah": o verbo da ficha também abre a explicação da Invocação
  ...(id === 'summon' ? { formas: ['Invoca'] } : {}),
});

const MECANICAS: Termo[] = [
  { id: 'escudo', nome: 'Escudo', cor: '#8fd3ff', rotulo: 'PROTEÇÃO', texto: 'Uma camada que absorve o dano antes da Vida. Some quando acaba ou depois de 10 s.', extra: 'Escudos somados não passam de 55% da Vida máxima.' },
  { id: 'energia', nome: 'Energia guardada', cor: '#ffd36b', rotulo: 'RECURSO', formas: ['energia guardada', 'energia'], texto: 'Um estoque que vai enchendo e não faz nada sozinho. Quando o personagem usa a habilidade que "Libera energia", solta tudo de uma vez como dano — e o estoque volta a zero.', extra: 'Quanto mais tempo guardando, maior o golpe.' },
  { id: 'carga', nome: 'Carga', cor: '#b8e282', rotulo: 'COMO AS HABILIDADES ENCHEM', texto: 'Cada habilidade tem uma barra de Carga. Cheia, a habilidade fica pronta. O que enche está escrito ao lado: atacar, apanhar, o tempo passando…' },
  { id: 'preparo', nome: 'Preparo', cor: '#f4d47e', rotulo: 'TEMPO ATÉ SAIR', texto: 'Quanto a habilidade demora para sair depois de começar. Durante o Preparo, o inimigo pode interromper. "Instantâneo" sai na hora.' },
  { id: 'resfriamento', nome: 'Resfriamento', cor: '#9fc3e0', rotulo: 'DESCANSO', texto: 'Depois de usada, a habilidade descansa esse tempo antes de voltar a encher a Carga.' },
  { id: 'usa-quando', nome: 'Usa quando', cor: '#c3a2ff', rotulo: 'CONDIÇÃO', texto: 'Mesmo pronta, a habilidade espera esta situação para sair.' },
  { id: 'proximo-ataque', nome: 'próximo ataque', cor: '#d2f66b', rotulo: 'RITMO', formas: ['próximo ataque'], texto: 'Mexe na vez de agir. Adiantar faz o próximo golpe sair antes; atrasar faz o alvo esperar mais.' },
  { id: 'copiar', nome: 'Copiar', cor: '#ff5a5a', rotulo: 'USA A DO RIVAL', formas: ['Copia a última habilidade'], texto: 'Copia a última habilidade usada por um rival e a usa do lado de quem copiou, com parte da força (dano, cura e Escudo menores; os Status iguais).', extra: 'Death Note, reviver e a própria cópia não se copiam.' },
  { id: 'ultima-resistencia', nome: 'Última resistência', cor: '#ffd36b', rotulo: 'NÃO CAI NA PRIMEIRA', formas: ['Última resistência'], texto: 'Uma vez por luta, o golpe que derrubaria o personagem o deixa com 1 de Vida e Protegido por alguns segundos.', extra: 'A Death Note não respeita: execução não tem resistência.' },
  { id: 'purificar', nome: 'Purificar', cor: '#bfefff', rotulo: 'TIRA DEBUFFS', formas: ['Purifica', 'Purificado'], texto: 'Tira debuffs de um aliado, os que mais atrapalham primeiro: Paralisado, Silenciado, Preso, Provocado, Confuso, Lento… O número diz quantos saem.', extra: 'Só tira o que já está lá: não protege contra o próximo.' },
  { id: 'dissipar', nome: 'Dissipar', cor: '#c3a6ff', rotulo: 'TIRA BUFFS', formas: ['Dissipa', 'Dissipado'], texto: 'Tira buffs de um rival, os que mais ajudam primeiro: Protegido, Refletir, Vampirismo, Fortalecido, Acelerado… O número diz quantos saem.', extra: 'Não quebra Escudo: o Escudo é outra coisa.' },
  { id: 'roubo-de-vida', nome: 'Roubo de vida', cor: '#ff4f6e', rotulo: 'O GOLPE CURA', formas: ['Roubo de vida'], texto: 'A habilidade cura quem a usa em parte do dano que ela mesma causou. Se o golpe for bloqueado ou errar o alvo, cura menos.', extra: 'O Vampirismo é parecido, mas é um Status: enquanto dura, todo golpe cura.' },
  { id: 'reviver', nome: 'Reviver', cor: '#ffe08a', rotulo: 'LEVANTAR QUEM CAIU', formas: ['Levanta um aliado caído', 'aliado caído'], texto: 'Levanta um aliado que caiu, com parte da Vida. Quem levanta só faz isso uma vez por luta, e cada lutador só volta uma vez.', extra: 'Tem Preparo: interromper quem vai reviver deixa o aliado no chão.' },
  { id: 'renascer', nome: 'Renascer', cor: '#ff9a3a', rotulo: 'VOLTA SOZINHO', formas: ['Renasce', 'Renascer'], texto: 'Quando cai, fica em brasas por um instante e volta sozinho com parte da Vida. Uma vez por luta.', extra: 'A Death Note impede: quem é executado não renasce.' },
  { id: 'traco', nome: 'Traço', cor: '#ffd36b', rotulo: 'SEMPRE ATIVO', texto: 'O jeito único de cada lutador: dispara sozinho numa situação (ao apanhar, quando um aliado sofre, quando o trio está perdendo, a cada tantos segundos…). Cada um dos 250 tem o seu — o Blaze do Charizard, o Chá de jasmim do Iroh, a Caixa de papelão do Snake.' },
  { id: 'serie', nome: 'Golpe da série', cor: '#ff9a76', rotulo: 'ATAQUE BÁSICO', formas: ['A cada 3 golpes', 'A cada 4 golpes'], texto: 'O ataque básico conta os golpes: no 3º (ou no 4º), sai o golpe especial do personagem, mais forte ou com um Status — o Rendan Uzumaki do Naruto, o ORA! do Jotaro.' },
  { id: 'ricochete', nome: 'Ricochete', cor: '#ff9a76', rotulo: 'ATAQUE BÁSICO', formas: ['Quica no outro rival'], texto: 'O ataque básico quica e acerta também o outro rival mais ferido, com parte do dano — o escudo do Capitão, o raio do Pikachu.' },
  { id: 'golpe-largo', nome: 'Golpe largo', cor: '#ff9a76', rotulo: 'ATAQUE BÁSICO', formas: ['Pega também um segundo rival'], texto: 'O ataque básico varre e pega também um segundo rival, com parte do dano — a esmagada do Hulk, a espada do Cloud.' },
  { id: 'golpe-que-cura', nome: 'Golpe que cura', cor: '#86e3a8', rotulo: 'ATAQUE BÁSICO', formas: ['vira cura no aliado mais ferido'], texto: 'Parte do dano do ataque básico vira cura no aliado mais ferido — o soco de chakra da Sakura, a Tiara lunar da Sailor Moon.' },
  { id: 'roubar-carga', nome: 'Roubar Carga', cor: '#b8e282', rotulo: 'ATAQUE BÁSICO', formas: ['Rouba'], texto: 'O ataque básico tira Carga da habilidade mais cheia do rival e passa para a habilidade dele que está mais perto de encher — o Kakashi copiando, o Cell absorvendo.' },
  { id: 'vulneravel', nome: 'vulnerável', cor: '#ff8a6b', rotulo: 'USA QUANDO', formas: ['vulnerável'], texto: `Um rival com um Status negativo que abre a guarda: ${DEIXAM_VULNERAVEL.map((x) => statuses[x].name).join(', ').replace(/, ([^,]*)$/, ' ou $1')}.`, extra: 'Lento, Preso, Enfraquecido, Silenciado, Confuso, Provocado e Marca explosiva atrapalham, mas não abrem a guarda: não contam.' },
  { id: 'interrompe', nome: 'Interrupção', cor: '#ff9a76', rotulo: 'CORTAR O GOLPE', formas: ['Interrompe o Preparo', 'Atrasa o Preparo', 'do Preparo'], texto: 'Age em quem está preparando uma habilidade: cancela o golpe, ou empurra para mais tarde, ou encurta o que já foi preparado.' },
];

export const GLOSSARIO: Termo[] = [...(Object.keys(statuses) as StatusId[]).map(doStatus), ...MECANICAS];
export const termoPorId = Object.fromEntries(GLOSSARIO.map((t) => [t.id, t])) as Record<string, Termo>;

/* Com maiúscula, como na ficha: "lento" numa frase comum não é o Status Lento. Todas as formas, as mais longas primeiro, para "Energia guardada" ganhar de "energia". */
const FORMAS = GLOSSARIO.flatMap((t) => [t.nome, ...(t.formas ?? [])].map((f) => ({ f, t })))
  .sort((a, b) => b.f.length - a.f.length);
const escapa = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const PADRAO = new RegExp(`(?<![\\p{L}])(${FORMAS.map((x) => escapa(x.f)).join('|')})(?![\\p{L}])`, 'gu');

/** Divide um texto em pedaços, marcando os que são termos do glossário. */
export function acharTermos(texto: string): (string | { texto: string; termo: Termo })[] {
  const saida: (string | { texto: string; termo: Termo })[] = [];
  let i = 0;
  for (const m of texto.matchAll(PADRAO)) {
    const achado = FORMAS.find((x) => x.f === m[0]);
    if (!achado || m.index === undefined) continue;
    if (m.index > i) saida.push(texto.slice(i, m.index));
    saida.push({ texto: m[0], termo: achado.t });
    i = m.index + m[0].length;
  }
  if (i < texto.length) saida.push(texto.slice(i));
  return saida;
}
