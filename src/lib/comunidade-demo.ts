import type { Conversa, Jogador, Mensagem, Ouvintes, Reacao, ServicoDaComunidade } from './comunidade';

/*
 * Uma comunidade de mentira, sem servidor: só para os testes e para a prévia da tela (VITE_COMUNIDADE_DEMO=true).
 * Ela se comporta como a de verdade — gente entrando e saindo, mensagens chegando, "digitando…", o visto aparecendo
 * quando o outro "abre" a conversa — para dar para ver a tela viva. Nunca vai para o jogo publicado.
 */
export const EU_DEMO = '00000000-0000-4000-8000-000000000000';

const agora = () => Date.now();
const iso = (msAtras: number) => new Date(agora() - msAtras).toISOString();
const MIN = 60_000, H = 60 * MIN;

const PESSOAS: [string, boolean, number, number | null, string[] | null, number][] = [
  // nome, online, há quanto tempo (online desde / saiu), recorde, trio, conquistas
  ['Kakaroto_BR', true, 42 * MIN, 1_912_400, ['goku', 'vegeta', 'gohan'], 212],
  ['MestreDosTrios', true, 3 * MIN, 1_740_300, ['gojo', 'itachi', 'light'], 160],
  ['luffy gear5', true, 18 * MIN, 1_355_000, ['luffy', 'zoro', 'sanji'], 74],
  ['NaruFan_22', true, 1 * MIN, 980_000, ['naruto', 'sasuke', 'kakashi'], 31],
  ['Ana_Sailor', true, 65 * MIN, 1_480_000, ['sailormoon', 'pikachu', 'raven'], 108],
  ['Thanos_Real', false, 25 * MIN, 1_210_000, ['thanos', 'magneto', 'darkseid'], 55],
  ['PikaPika', false, 3 * H, 640_000, ['pikachu', 'charizard', 'mewtwo'], 12],
  ['Zenitsu_dorme', false, 26 * H, 1_102_500, ['zenitsu', 'tanjiro', 'nezuko'], 40],
  ['Rafa_Shinigami', false, 4 * 24 * H, 870_000, ['ichigo', 'byakuya', 'rukia'], 22],
  ['Bia Hero', false, 40 * MIN, 1_590_000, ['wonderwoman', 'batman', 'superman'], 96],
  ['KratosPai', false, 9 * H, 1_005_000, ['kratos', 'thor', 'zeus'], 47],
  ['novato123', false, 0, null, null, 0],
];

export function criarComunidadeDemo(): ServicoDaComunidade {
  const jogadores: Jogador[] = PESSOAS.map(([nome, online, ha, recorde, trio, conquistas], i) => ({
    id: `00000000-0000-4000-8000-${String(i + 1).padStart(12, '0')}`, nome, online,
    onlineDesde: online ? iso(ha) : null, vistoEm: ha === 0 && !online ? null : online ? iso(10_000) : iso(ha),
    recorde, trio, conquistas, desde: iso(30 * 24 * H),
  }));
  jogadores.push({ id: EU_DEMO, nome: 'Você', online: true, onlineDesde: iso(2 * MIN), vistoEm: iso(5_000), recorde: 1_410_000, trio: ['sekiro', 'alphonse', 'azula'], conquistas: 63, desde: iso(60 * 24 * H) });
  const id = (n: number) => jogadores[n]!.id;
  let proximo = 1;
  const mensagens: Mensagem[] = [];
  const reacoes: Reacao[] = [];
  const nova = (autor: string, texto: string, msAtras: number, para: string | null = null, respostaA: number | null = null, vista = false) => {
    const m: Mensagem = { id: proximo++, autorId: autor, paraId: para, texto, respostaA, criadaEm: iso(msAtras), vistaEm: vista ? iso(msAtras - 30_000) : null };
    mensagens.push(m);
    return m;
  };
  nova(id(5), 'Alguém já passou de 2 milhões com Thanos?', 26 * H);
  nova(id(0), 'Eu fiz 1,9 mi com Goku, Vegeta e Gohan 🔥', 25 * H);
  const g1 = nova(id(1), 'Gente, o combo do Gojo com o Itachi é absurdo', 50 * MIN);
  nova(id(2), 'Sério? Qual o terceiro?', 48 * MIN, null, g1.id);
  nova(id(1), 'Light. Ele marca o rival mais forte e os dois limpam', 47 * MIN);
  const g2 = nova(id(4), 'Sailor Moon com 10% de pontos tá valendo muito a pena', 30 * MIN);
  nova(EU_DEMO, 'Vou testar hoje! Sekiro tá muito bom também', 28 * MIN);
  nova(id(3), 'Alguém me ensina a pegar combo? Sou novo kkk', 6 * MIN);
  const g3 = nova(id(0), 'Abre o Livro de Combos no início, lá mostra tudo 👊', 5 * MIN);
  nova(id(3), 'Valeu!!', 4 * MIN);
  reacoes.push({ mensagemId: g1.id, playerId: id(0), emoji: '🔥' }, { mensagemId: g1.id, playerId: id(2), emoji: '🔥' }, { mensagemId: g1.id, playerId: EU_DEMO, emoji: '😮' },
    { mensagemId: g2.id, playerId: id(1), emoji: '👏' }, { mensagemId: g3.id, playerId: id(3), emoji: '❤️' });
  // privadas
  nova(id(1), 'E aí! Vi seu Sekiro no ranking, que trio é esse?', 2 * H, EU_DEMO, null, true);
  nova(EU_DEMO, 'Sekiro, Alphonse e Azula. Fiz 1,4 mi', 2 * H - 4 * MIN, id(1), null, true);
  nova(id(1), 'Brabo demais. Quando sair o PvP te desafio 😎', 70 * MIN, EU_DEMO);
  nova(id(1), 'Bora treinar amanhã?', 68 * MIN, EU_DEMO);
  nova(EU_DEMO, 'Volta aqui quando puder, quero te mostrar um trio', 3 * H, id(7), null, false);
  nova(id(4), 'Obrigada pela dica da estrela!', 26 * H, EU_DEMO, null, true);
  nova(EU_DEMO, 'De nada 😄', 26 * H - 2 * MIN, id(4), null, true);

  const ouvintes = new Set<Ouvintes>();
  const avisa = (f: (o: Ouvintes) => void) => { for (const o of ouvintes) f(o); };
  // a vida da comunidade: alguém digita e manda, de tempos em tempos
  const FALAS = ['Alguém online pra trocar ideia de trio?', 'Acabei de liberar o Ichigo! 🎉', 'Esse jogo tá viciante kkk', 'Quem tem o recorde de hoje?', 'GG pra todo mundo 👏'];
  let fala = 0;
  if (typeof window !== 'undefined') setInterval(() => {
    if (!ouvintes.size) return;
    const autor = id([1, 2, 3, 4][fala % 4]!);
    avisa((o) => o.digitando?.(autor, null));
    setTimeout(() => { const m = nova(autor, FALAS[fala++ % FALAS.length]!, 0); avisa((o) => o.mensagem?.(m, 'nova')); }, 2200);
  }, 16_000);

  // uma privada chegando com o jogo aberto (para ver o aviso de mensagem nova)
  if (typeof window !== 'undefined') setTimeout(() => { const m = nova(id(1), 'Tá aí? Bora treinar 👀', 0, EU_DEMO); avisa((o) => o.mensagem?.({ ...m }, 'nova')); }, 9000);

  const espera = <T,>(v: T, ms = 250) => new Promise<T>((r) => setTimeout(() => r(v), ms));
  return {
    jogadores: () => espera(jogadores.filter((j) => j.id !== EU_DEMO).map((j) => ({ ...j }))),
    historico: (com) => {
      const lista = mensagens.filter((m) => com === null ? m.paraId === null : (m.autorId === EU_DEMO && m.paraId === com) || (m.autorId === com && m.paraId === EU_DEMO));
      const ids = new Set(lista.map((m) => m.id));
      return espera({ mensagens: lista.map((m) => ({ ...m })), reacoes: reacoes.filter((r) => ids.has(r.mensagemId) && r.emoji), temMais: false });
    },
    enviar: (texto, para = null, respostaA = null) => {
      const m = nova(EU_DEMO, texto.trim(), 0, para, respostaA);
      setTimeout(() => avisa((o) => o.mensagem?.({ ...m }, 'nova')), 120);
      // na privada com quem está online, o outro "abre" e o visto aparece
      if (para && jogadores.find((j) => j.id === para)?.online) setTimeout(() => { m.vistaEm = new Date().toISOString(); avisa((o) => o.mensagem?.({ ...m }, 'mudou')); }, 2500);
      return espera({ ...m }, 150);
    },
    marcarVistas: async (de) => { for (const m of mensagens) if (m.autorId === de && m.paraId === EU_DEMO && !m.vistaEm) m.vistaEm = new Date().toISOString(); },
    reagir: async (mensagemId, emoji) => {
      const r = reacoes.find((x) => x.mensagemId === mensagemId && x.playerId === EU_DEMO);
      const novo = r?.emoji === emoji ? null : emoji;
      if (r) r.emoji = novo; else reacoes.push({ mensagemId, playerId: EU_DEMO, emoji: novo });
      avisa((o) => o.reacao?.({ mensagemId, playerId: EU_DEMO, emoji: novo }));
    },
    conversas: () => {
      const por = new Map<string, Conversa>();
      for (const m of mensagens) {
        if (m.paraId === null || (m.autorId !== EU_DEMO && m.paraId !== EU_DEMO)) continue;
        const outro = m.autorId === EU_DEMO ? m.paraId : m.autorId, ant = por.get(outro);
        const naoLidas = (ant?.naoLidas ?? 0) + (m.paraId === EU_DEMO && !m.vistaEm ? 1 : 0);
        if (!ant || m.id > ant.ultimaId) por.set(outro, { comId: outro, comNome: jogadores.find((j) => j.id === outro)!.nome, ultimaId: m.id, ultimaTexto: m.texto, ultimaEm: m.criadaEm, ultimaMinha: m.autorId === EU_DEMO, ultimaVista: !!m.vistaEm, naoLidas });
        else ant.naoLidas = naoLidas;
      }
      return espera([...por.values()].sort((a, b) => b.ultimaId - a.ultimaId));
    },
    ping: async () => undefined,
    sair: async () => undefined,
    ouvir: (o) => { ouvintes.add(o); return () => { ouvintes.delete(o); }; },
    avisarDigitando: () => undefined,
  };
}
