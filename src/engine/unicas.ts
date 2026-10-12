/*
 * Mecânicas únicas: uma regra que só aquele personagem tem, como a Death Note
 * do Light. Os tipos e as funções auxiliares estão em unicas-base.ts; cada lote
 * de personagens fica no seu arquivo.
 */
import { avisoACada, BUFFS, CONTROLES, curaContinua, fracao, maisFerido, maisForte, quandoVira, relogio, st, trabalho, u, vivo, type Unica } from './unicas-base';
import { LOTE2 } from './unicas-lote2';
import { LOTE3 } from './unicas-lote3';
import { LOTE4 } from './unicas-lote4';
import { LOTE5 } from './unicas-lote5';
import { LOTE6 } from './unicas-lote6';
import { LOTE7 } from './unicas-lote7';
import { LOTE8 } from './unicas-lote8';
import { LOTE9, conheceTodas } from './unicas-lote9';
export type { Ganchos, Golpe, Motor, Unica } from './unicas-base';

const LOTE1: Record<string, Unica> = {
  /* ───────── Força bruta, cada um do seu jeito ───────── */
  drax: {
    nome: 'Vingança',
    texto: 'Drax causa +60% de dano no rival que derrubou um aliado de Drax. Drax nunca fica Confuso.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quem.side !== f.side || quemDerrubou.side === f.side) return;
        u(f).vinganca = b.fighters.indexOf(quemDerrubou);
        m.aviso(b, f, 'Vingança!', quemDerrubou);
      },
      causa: (_m, b, f, alvo) => (u(f).vinganca !== undefined && b.fighters[u(f).vinganca!] === alvo ? 1.6 : 1),
      imune: (_f, s) => s === 'confused',
    },
  },
  johnnybravo: {
    nome: 'Cantada',
    texto: 'A cada 10 s, Johnny Bravo tenta uma cantada no rival com mais Vida: 33% de chance de deixar esse rival Confuso por 3 s; se não der certo, Johnny Bravo fica Fortalecido (+30% de dano) por 6 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'cantada', dt, 10, 6)) return;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        if (m.sorte(b) < 1 / 3) { m.efeitos(b, f, [alvo], [st('confused', 1, 3)]); m.aviso(b, f, 'Cantada certeira', alvo); }
        else { m.efeitos(b, f, [f], [st('strengthened', 0.3, 6)]); m.aviso(b, f, 'Levou um fora', f); }
      },
    },
  },
  hercules: {
    nome: 'Caminho do herói',
    texto: 'Hércules junta Trabalhos: +2 a cada habilidade que usa e +4 a cada rival que derruba. Com 12 Trabalhos, vira Semideus até o fim da luta: +35% de dano e −25% de dano recebido.',
    ganchos: {
      usou(m, b, f) { trabalho(m, b, f, 2); },
      caiu(m, b, f, quem, quemDerrubou) { if (quemDerrubou === f && quem.side !== f.side) trabalho(m, b, f, 4); },
      causa: (_m, _b, f) => (u(f).deus ? 1.35 : 1),
      recebe: (_m, _b, f) => (u(f).deus ? 0.75 : 1),
    },
  },
  allmight: {
    nome: 'Tempo limitado',
    texto: 'All Might começa com +40% de dano e perde 6 pontos desse bônus a cada 10 s, até chegar a −20% de dano. Com menos de 30% da Vida (1 vez por luta), a próxima habilidade de All Might causa o dobro de dano.',
    ganchos: {
      passo(_m, _b, f, dt) {
        const s = u(f);
        s.tempo = (s.tempo ?? 0) + dt;
        if (!s.plus && fracao(f) < 0.3) { s.plus = 1; s.pronto = 1; }
      },
      causa(m, b, f, _alvo, g) {
        const s = u(f), forma = Math.max(-0.2, 0.4 - 0.06 * Math.floor((s.tempo ?? 0) / 10));
        let k = 1 + forma;
        if (s.pronto && g.habilidade) { k *= 2; s.gasto = 1; m.aviso(b, f, 'Plus Ultra!', f); }
        return k;
      },
      usou(_m, _b, f) { if (u(f).gasto) { u(f).pronto = 0; u(f).gasto = 0; } },
    },
  },
  popeye: {
    nome: 'Espinafre',
    texto: 'Com 40% da Vida ou menos (1 vez por luta): Popeye come o espinafre, cura 25% da Vida máxima e fica Fortalecido (+40% de dano) e Acelerado (30% mais rápido) por 8 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).lata || fracao(f) > 0.4) return;
        u(f).lata = 1;
        m.cura(b, f, f, f.maxHp * 0.25, 'Espinafre');
        m.efeitos(b, f, [f], [st('strengthened', 0.4, 8), st('haste', 0.3, 8)]);
        m.aviso(b, f, 'Espinafre!', f);
      },
    },
  },
  homer: {
    nome: 'Soneca',
    texto: 'A cada 18 s, Homer Simpson cochila: fica 3 s parado e cura 4% da Vida máxima por segundo. Ao acordar, o próximo golpe de Homer causa +80% de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f);
        if (s.dormindo) {
          s.dormindo -= dt;
          curaContinua(m, b, f, f, f.maxHp * 0.04 * dt, 'Soneca');
          if (s.dormindo <= 1e-6) { s.dormindo = 0; s.acordou = 1; m.aviso(b, f, "D'oh!", f); }
          return;
        }
        if (relogio(f, 'sono', dt, 18, 12)) { s.dormindo = 3; m.aviso(b, f, 'Cochilo', f); }
      },
      parado: (f) => (u(f).dormindo ?? 0) > 0,
      causa: (_m, _b, f, _alvo, g) => (u(f).acordou && g.direto ? 1.8 : 1),
      bateu(_m, _b, f, _alvo, _dano, g) { if (g.direto) u(f).acordou = 0; },
    },
  },

  /* ───────── Caçadores ───────── */
  artemis: {
    nome: 'Flecha que nunca erra',
    texto: 'Os golpes de Ártemis nunca erram: passam por Esquiva e Cego. Ártemis causa +40% de dano em rivais com Esquiva, Barreira ou Invocação.',
    ganchos: {
      nuncaErra: true,
      causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'evasion') > 0 || m.intensidade(alvo, 'barrier') > 0 || m.intensidade(alvo, 'summon') > 0 ? 1.4 : 1),
    },
  },
  predator: {
    nome: 'Camuflagem e troféus',
    texto: 'Nos primeiros 8 s da luta, o Predador não recebe dano de ataques nem de habilidades. A cada rival que o Predador derruba: +15% de dano até o fim da luta.',
    ganchos: {
      inicio(m, b, f) { m.aviso(b, f, 'Camuflado', f); },
      recebe: (_m, b, _f, _fonte, g) => (g.direto && b.time < 8 ? 0 : 1),
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        u(f).trofeus = (u(f).trofeus ?? 0) + 1;
        m.aviso(b, f, `Troféu ${u(f).trofeus}`, f, u(f).trofeus);
      },
      causa: (_m, _b, f) => 1 + 0.15 * (u(f).trofeus ?? 0),
    },
  },

  /* ───────── Máquinas ───────── */
  ultron: {
    nome: 'Corpos de reserva',
    texto: 'Quando cai, Ultron volta com 25% da Vida máxima e sem Status (até 2 vezes por luta). A cada volta, Ultron fica com −20% de dano até o fim da luta.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo !== f || (u(f).corpos ?? 0) >= 2) return null;
        u(f).corpos = (u(f).corpos ?? 0) + 1;
        f.statuses = []; f.cast = null;
        m.aviso(b, f, `Corpo novo (${u(f).corpos}/2)`, f);
        return f.maxHp * 0.25;
      },
      causa: (_m, _b, f) => 1 - 0.2 * (u(f).corpos ?? 0),
    },
  },
  cyborg: {
    nome: 'Hacker',
    texto: 'A cada 9 s, Ciborgue rouba de um rival o melhor Status bom que encontrar (Barreira, Esquiva, Protegido, Refletir, Vampirismo, Fortalecido, Acelerado, Espinhos ou Regeneração, nessa ordem) e fica com esse Status.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'hack', dt, 9, 5)) return;
        for (const id of BUFFS) {
          const dono = m.rivais(b, f).find((r) => r.statuses.some((s) => s.id === id));
          if (!dono) continue;
          const s = dono.statuses.find((x) => x.id === id)!;
          dono.statuses = dono.statuses.filter((x) => x !== s);
          m.efeitos(b, f, [f], [st(id, s.intensity, Math.max(2, s.remaining))]);
          m.aviso(b, f, 'Hackeado!', dono);
          return;
        }
      },
    },
  },
  t800: {
    nome: 'Exterminador',
    texto: 'O Exterminador T-800 nunca fica Paralisado, Congelado, Dormindo, Confuso, Silenciado, Lento nem Preso. Toda cura no T-800 vale só a metade.',
    ganchos: {
      imune: (_f, s) => CONTROLES.includes(s),
      curaRecebida: () => 0.5,
    },
  },

  /* ───────── Espadas ───────── */
  zoro: {
    nome: 'Nada aconteceu',
    texto: '1 vez por luta: quando um golpe ia derrubar um aliado, Roronoa Zoro leva esse dano no lugar do aliado. Zoro não cai com isso: fica com no mínimo 1 de Vida.',
    ganchos: {
      salva(m, b, f, alvo, dano) {
        if (alvo === f || u(f).nada || !vivo(f)) return null;
        u(f).nada = 1;
        f.hp = Math.max(1, f.hp - dano);
        m.aviso(b, f, 'Nada aconteceu.', alvo);
        return alvo.hp;
      },
    },
  },
  inuyasha: {
    nome: 'Tessaiga carregada',
    texto: 'Inuyasha guarda 25% de todo dano que o trio recebe dos rivais (até 500). Quando usa Ferida do Vento, solta tudo o que guardou como dano extra no rival com mais Vida (se tiver pelo menos 30 guardado).',
    ganchos: {
      viu(_m, _b, f, fonte, alvo, dano) {
        if (alvo.side === f.side && fonte.side !== f.side) u(f).vento = Math.min(500, (u(f).vento ?? 0) + dano / 4);
      },
      usou(m, b, f, i) {
        const v = u(f).vento ?? 0;
        if (i !== 2 || v < 30) return;
        const alvo = maisForte(m, b, f);
        u(f).vento = 0;
        if (alvo) { m.aviso(b, f, 'Bakuryūha!', alvo, v); m.dano(b, f, alvo, v, true, 'Bakuryūha'); }
      },
    },
  },
  kenshin: {
    nome: 'Battōjutsu',
    texto: 'Quando um rival começa um Preparo (no máximo 1 vez a cada 4 s): as habilidades de Kenshin Himura ganham +15% de Carga, e a próxima habilidade de Kenshin causa +25% de dano.',
    ganchos: {
      viuPreparo(m, b, f, quem) {
        if ((u(f).esperaSaque ?? 0) > b.time) return;
        u(f).esperaSaque = b.time + 4;
        for (const s of f.skills) if (s.cooldown <= 0) s.charge = Math.min(100, s.charge + 15);
        u(f).saque = 1;
        m.aviso(b, f, 'Battōjutsu', quem);
      },
      causa: (_m, _b, f, _alvo, g) => (u(f).saque && g.habilidade ? 1.25 : 1),
      usou(_m, _b, f) { u(f).saque = 0; },
    },
  },
  vash: {
    nome: 'Pacifista',
    texto: 'Vash nunca derruba ninguém: o golpe que derrubaria deixa o rival com 1 de Vida. Vash causa +25% de dano, e cada golpe de Vash deixa o alvo Enfraquecido (−15% de dano) por 5 s.',
    ganchos: {
      poupa: true,
      causa: () => 1.25,
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo)) m.efeitos(b, f, [alvo], [st('weakened', 0.15, 5)]); },
    },
  },

  /* ───────── Reações ───────── */
  mob: {
    nome: '???%',
    texto: 'A barra ???% de Mob enche com a Vida que o trio de Mob perde. Quando chega a 100%: cada rival leva 260 de dano e fica Paralisado por 1,5 s; depois a barra zera.',
    ganchos: {
      viu(m, b, f, fonte, alvo, dano) {
        if (alvo.side !== f.side || fonte.side === f.side) return;
        const s = u(f);
        s.emocao = (s.emocao ?? 0) + (100 * dano) / alvo.maxHp;
        if (s.emocao < 100) return;
        s.emocao = 0;
        m.aviso(b, f, '100%', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 260, true, '???%');
        m.efeitos(b, f, m.rivais(b, f), [st('paralyzed', 1, 1.5)]);
      },
    },
  },
  natsu: {
    nome: 'Come fogo',
    texto: 'Natsu Dragneel nunca fica Queimando. Cada vez que alguém (de qualquer trio) começa a ficar Queimando, Natsu cura 40 de Vida e ganha +8% de dano até o fim da luta (no máximo 5 vezes: +40%).',
    ganchos: {
      imune: (_f, s) => s === 'burning',
      passo(m, b, f) {
        const queimando = b.fighters.filter((x) => vivo(x) && x !== f && x.statuses.some((s) => s.id === 'burning')).length;
        const s = u(f);
        if (queimando > (s.chamas ?? 0)) {
          s.fome = Math.min(5, (s.fome ?? 0) + 1);
          m.cura(b, f, f, 40, 'Come fogo');
          m.aviso(b, f, 'Come fogo', f, s.fome);
        }
        s.chamas = queimando;
      },
      causa: (_m, _b, f) => 1 + 0.08 * (u(f).fome ?? 0),
    },
  },
  sanji: {
    nome: 'Cozinheiro do navio',
    texto: 'A cada 15 s, Sanji serve uma refeição ao aliado mais ferido (pode ser o próprio Sanji): esse aliado cura 12% da Vida máxima e fica Fortalecido (+15% de dano) por 6 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'cozinha', dt, 15, 10)) return;
        const alvo = maisFerido(m, b, f);
        if (!alvo) return;
        m.cura(b, f, alvo, alvo.maxHp * 0.12, 'Refeição');
        m.efeitos(b, f, [alvo], [st('strengthened', 0.15, 6)]);
        m.aviso(b, f, 'Refeição servida', alvo);
      },
    },
  },
  ken: {
    nome: 'Parry perfeito',
    texto: 'Ken Masters bloqueia por inteiro o próximo golpe que recebe e devolve 80 de dano em quem bateu. Depois de bloquear, leva 10 s para poder bloquear de novo.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.direto || (u(f).parry ?? 0) > b.time) return 1;
        u(f).parry = b.time + 10;
        m.aviso(b, f, 'Parry!', fonte);
        m.dano(b, f, fonte, 80, false, 'Shōryūken');
        return 0;
      },
    },
  },
  cuphead: {
    nome: 'Cartas de Super',
    texto: 'Cuphead ganha 1 Carta a cada 4 golpes que dá. Todo 4º golpe que Cuphead recebe não causa dano e também dá 1 Carta. Com 5 Cartas: 380 de dano no rival com mais Vida, e as Cartas zeram.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto) return;
        const s = u(f);
        s.golpes = (s.golpes ?? 0) + 1;
        if (s.golpes % 4 === 0) s.cartas = (s.cartas ?? 0) + 1;
        if ((s.cartas ?? 0) >= 5) {
          s.cartas = 0;
          const alvo = maisForte(m, b, f);
          if (alvo) { m.aviso(b, f, 'Super!', alvo); m.dano(b, f, alvo, 380, false, 'Super'); }
        }
      },
      recebe(m, b, f, fonte, g) {
        if (!g.direto) return 1;
        const s = u(f);
        s.recebidos = (s.recebidos ?? 0) + 1;
        if (s.recebidos % 4 !== 0) return 1;
        s.cartas = (s.cartas ?? 0) + 1;
        m.aviso(b, f, 'Parry rosa', fonte);
        return 0;
      },
    },
  },
  neo: {
    nome: 'Desvia de balas',
    texto: 'Neo tem 50% de chance de desviar de cada ataque básico dos rivais.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.direto || g.habilidade || m.sorte(b) >= 0.5) return 1;
        m.aviso(b, f, 'Desviou', fonte);
        return 0;
      },
    },
  },
  spike: {
    nome: 'Seja água',
    texto: 'Quanto menos Vida, mais rápido Spike Spiegel age: +0,75% de velocidade a cada 1% de Vida perdida, até 60% mais rápido (com 20% da Vida ou menos).',
    ganchos: {
      ritmo: (_m, _b, f) => 1 + Math.max(0, Math.min(0.6, (1 - fracao(f)) * 0.75)),
    },
  },
  hollowknight: {
    nome: 'Foco da alma',
    texto: 'Cada golpe que O Cavaleiro dá enche a Alma (cheia com 600 de dano causado). Com a Alma cheia e menos de 60% da Vida: O Cavaleiro fica 1 s parado, cura 25% da Vida máxima e a Alma zera.',
    ganchos: {
      bateu(_m, _b, f, _alvo, dano, g) { if (g.direto) u(f).alma = Math.min(100, (u(f).alma ?? 0) + dano / 6); },
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.foco ?? 0) > 0) { s.foco! -= dt; if (s.foco! <= 1e-6) { s.foco = 0; m.cura(b, f, f, f.maxHp * 0.25, 'Foco'); } return; }
        if ((s.alma ?? 0) >= 100 && fracao(f) < 0.6) { s.alma = 0; s.foco = 1; m.aviso(b, f, 'Foco', f); }
      },
      parado: (f) => (u(f).foco ?? 0) > 0,
    },
  },

  /* ───────── Transformações ───────── */
  jin: {
    nome: 'Gene Devil',
    texto: 'Com 50% da Vida ou menos, até o fim da luta: Jin Kazama causa +20% de dano e ganha Esquiva (15% de chance de desviar).',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).diabo || fracao(f) > 0.5) return;
        u(f).diabo = 1;
        m.efeitos(b, f, [f], [st('evasion', 0.15, 999)]);
        m.aviso(b, f, 'Devil Jin', f);
      },
      causa: (_m, _b, f) => (u(f).diabo ? 1.2 : 1),
    },
  },
  garou: {
    nome: 'Monstro que evolui',
    texto: 'Cada habilidade que acerta Garou o faz evoluir: +3% de dano e −2% de dano recebido, até 10 vezes (no máximo +30% de dano e −20% de dano recebido).',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.habilidade) return;
        const s = u(f);
        if ((s.evolucao ?? 0) >= 10) return;
        s.evolucao = (s.evolucao ?? 0) + 1;
        m.aviso(b, f, `Evoluiu (${s.evolucao})`, fonte, s.evolucao);
      },
      causa: (_m, _b, f) => 1 + 0.03 * (u(f).evolucao ?? 0),
      recebe: (_m, _b, f) => 1 - 0.02 * (u(f).evolucao ?? 0),
    },
  },
  guts: {
    nome: 'Armadura do Berserker',
    texto: '1 vez por luta: quando ia cair, Guts fica de pé com 1 de Vida e luta mais 6 s sem receber dano e com +50% de dano. Quando esses 6 s acabam, Guts cai.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo !== f || u(f).berserk) return null;
        u(f).berserk = b.time + 6;
        m.aviso(b, f, 'Berserker', f);
        return 1;
      },
      recebe: (_m, b, f) => (u(f).berserk && b.time < u(f).berserk! ? 0 : 1),
      causa: (_m, b, f) => (u(f).berserk && b.time < u(f).berserk! ? 1.5 : 1),
      passo(m, b, f) {
        if (u(f).berserk && !u(f).caiu && b.time >= u(f).berserk!) { u(f).caiu = 1; m.dano(b, f, f, f.hp + 1, false, 'Fim do Berserker'); }
      },
    },
  },
  todoroki: {
    nome: 'Gelo e fogo',
    texto: 'Cada habilidade que Shoto Todoroki usa também atinge o rival com mais Vida, alternando: Lento (25% mais lento) por 5 s e Queimando (−14 de Vida por segundo) por 5 s. Se esse rival ficar com os dois ao mesmo tempo, leva 180 de dano e perde os dois.',
    ganchos: {
      usou(m, b, f) {
        const s = u(f), lado = (s.lado ?? 0) % 2;
        s.lado = lado + 1;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        m.efeitos(b, f, [alvo], [lado === 0 ? st('slow', 0.25, 5) : st('burning', 14, 5)]);
        if (alvo.statuses.some((x) => x.id === 'slow') && alvo.statuses.some((x) => x.id === 'burning')) {
          alvo.statuses = alvo.statuses.filter((x) => x.id !== 'slow' && x.id !== 'burning');
          m.aviso(b, f, 'Choque térmico', alvo);
          m.dano(b, f, alvo, 180, false, 'Choque térmico');
        }
      },
    },
  },
  ra: {
    nome: 'Ciclo do sol',
    texto: 'Rá luta em ciclos de 30 s. Dia (20 s): Rá causa +15% de dano e todo o trio cura 0,5% da Vida máxima por segundo. Noite (10 s): Rá causa −15% de dano e fica Protegido (−20% de dano recebido).',
    ganchos: {
      passo(m, b, f, dt) {
        const dia = b.time % 30 < 20, s = u(f);
        if (dia) for (const a of m.aliados(b, f)) curaContinua(m, b, f, a, a.maxHp * 0.005 * dt, 'Sol');
        if ((s.dia ?? 1) !== (dia ? 1 : 0)) {
          s.dia = dia ? 1 : 0;
          if (!dia) m.efeitos(b, f, [f], [st('protected', 0.2, 10)]);
          m.aviso(b, f, dia ? 'Amanhece' : 'Anoitece', f);
        }
      },
      causa: (_m, b) => (b.time % 30 < 20 ? 1.15 : 0.85),
    },
  },

  /* ───────── Mentes e apoio ───────── */
  katara: {
    nome: 'Dobra de sangue',
    texto: 'Aos 40 s de luta (1 vez por luta): por 4 s, o rival com mais Vida usa o ataque básico nos próprios aliados.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).lua || b.time < 40) return;
        const alvo = maisForte(m, b, f);
        if (!alvo || m.aliados(b, alvo).length < 2) return;
        u(f).lua = 1;
        alvo.traido = 4;
        m.aviso(b, f, 'Dobra de sangue', alvo);
      },
    },
  },
  leorio: {
    nome: 'Futuro médico',
    texto: 'As curas de Leorio valem o dobro em quem está com menos de 35% da Vida.',
    ganchos: {
      curaFeita(m, b, f, alvo) {
        if (fracao(alvo) >= 0.35) return 1;
        avisoACada(m, b, f, 'medico', 8, 'Futuro médico', alvo);
        return 2;
      },
    },
  },
  aerith: {
    nome: 'Última oração',
    texto: 'Quando Aerith cai: cada aliado de pé cura 30% da Vida máxima e fica com Regeneração (+12 de Vida por segundo) por 8 s.',
    ganchos: {
      morreu(m, b, f) {
        m.aviso(b, f, 'Última oração', f);
        const vivos = m.aliados(b, f);
        for (const a of vivos) m.cura(b, f, a, a.maxHp * 0.3, 'Última oração');
        m.efeitos(b, f, vivos, [st('regen', 12, 8)]);
      },
    },
  },
  isis: {
    nome: 'Asas protetoras',
    texto: 'Enquanto Ísis está de pé, os aliados de Ísis com menos de 30% da Vida recebem −40% de dano (não vale para a própria Ísis).',
    ganchos: {
      recebeAliado(m, b, f, aliado) {
        if (aliado === f || fracao(aliado) >= 0.3) return 1;
        avisoACada(m, b, f, 'asas', 8, 'Asas protetoras', aliado);
        return 0.6;
      },
    },
  },
  tenshinhan: {
    nome: 'Corpo no limite',
    texto: 'Kikoho custa 15% da Vida máxima de Tenshinhan (só se Tenshinhan tiver mais de 16% da Vida), mas causa +80% de dano.',
    ganchos: {
      causa: (_m, _b, f, _alvo, g) => (g.habilidade && u(f).kikoho ? 1.8 : 1),
      antes(m, b, f, i) {
        if (i !== 2) return;
        u(f).kikoho = 1;
        if (f.hp > f.maxHp * 0.16) { f.hp -= f.maxHp * 0.15; m.aviso(b, f, 'Kikōhō: custa Vida', f); }
      },
      usou(_m, _b, f) { u(f).kikoho = 0; },
    },
  },
  sailormercury: {
    nome: 'Análise do inimigo',
    texto: 'No começo da luta, Sailor Mercury analisa o rival com mais Vida: enquanto Sailor Mercury estiver de pé, o trio de Sailor Mercury causa +15% de dano nesse rival.',
    ganchos: {
      inicio(m, b, f) {
        const alvo = maisForte(m, b, f);
        if (alvo) { u(f).analisado = b.fighters.indexOf(alvo); m.aviso(b, f, 'Analisado', alvo); }
      },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).analisado !== undefined && b.fighters[u(f).analisado!] === alvo ? 1.15 : 1),
    },
  },
  invencivel: {
    nome: 'Sangue viltrumita',
    texto: 'Invencível ganha +1% de dano a cada 2% de Vida perdida (no máximo +30%, com 40% da Vida ou menos).',
    ganchos: { causa: (_m, _b, f) => 1 + Math.min(0.3, (1 - fracao(f)) / 2) },
  },
  hellboy: {
    nome: 'Chifres serrados',
    texto: 'Com menos de 30% da Vida: Hellboy causa +40% de dano e não fica Paralisado, Congelado nem Dormindo.',
    ganchos: {
      passo(m, b, f) { quandoVira(m, b, f, 'chifres', fracao(f) < 0.3, 'Chifres serrados', f); },
      causa: (_m, _b, f) => (fracao(f) < 0.3 ? 1.4 : 1),
      imune: (f, s) => fracao(f) < 0.3 && (s === 'paralyzed' || s === 'frozen' || s === 'sleep'),
    },
  },
  kaneki: {
    nome: 'Fome de ghoul',
    texto: 'Com menos de 50% da Vida, Ken Kaneki cura 15% do dano que causa. Quando Kaneki derruba um rival, cura 20% da Vida máxima.',
    ganchos: {
      bateu(m, b, f, _alvo, dano) { if (fracao(f) < 0.5) m.cura(b, f, f, dano * 0.15, 'Fome'); },
      caiu(m, b, f, quem, quemDerrubou) { if (quemDerrubou === f && quem.side !== f.side) { m.cura(b, f, f, f.maxHp * 0.2, 'Kagune'); m.aviso(b, f, 'Kakuja', f); } },
    },
  },
  venom: {
    nome: 'Simbionte',
    texto: 'Venom recupera 1% da Vida máxima por segundo. Queimando causa o dobro de dano em Venom.',
    ganchos: {
      passo(m, b, f, dt) { curaContinua(m, b, f, f, f.maxHp * 0.01 * dt, 'Simbionte'); },
      recebe: (m, _b, f, _fonte, g) => (!g.direto && g.label === 'Impacto' && m.intensidade(f, 'burning') > 0 ? 2 : 1),
    },
  },
  stitch: {
    nome: 'Destruir tudo',
    texto: 'Cada golpe de Stitch tira do alvo todo o Escudo, a Barreira e a Invocação.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const tinha = alvo.shields.length > 0 || alvo.statuses.some((s) => s.id === 'barrier' || s.id === 'summon');
        if (!tinha) return;
        alvo.shields = [];
        alvo.statuses = alvo.statuses.filter((s) => s.id !== 'barrier' && s.id !== 'summon');
        m.aviso(b, f, 'Destruído!', alvo);
      },
    },
  },
  malenia: {
    nome: 'Podridão escarlate',
    texto: 'Malenia cura 7% do dano que causa. Com 50% da Vida ou menos (1 vez por luta): todos os rivais ficam Envenenado (−14 de Vida por segundo) por 8 s.',
    ganchos: {
      bateu(m, b, f, _alvo, dano) { m.cura(b, f, f, dano * 0.07, 'Podridão'); },
      apanhou(m, b, f) {
        if (u(f).flor || fracao(f) > 0.5) return;
        u(f).flor = 1;
        m.efeitos(b, f, m.rivais(b, f), [st('poison', 14, 8)]);
        m.aviso(b, f, 'Florescer escarlate', f);
      },
    },
  },
  tifa: {
    nome: 'Combo sem parar',
    texto: 'Cada golpe seguido de Tifa Lockhart no mesmo rival causa +6% de dano a mais que o anterior (até +60%). Golpear outro rival zera a sequência.',
    ganchos: {
      causa(_m, b, f, alvo, g) {
        if (!g.direto) return 1;
        const s = u(f), i = b.fighters.indexOf(alvo);
        s.combo = s.alvo === i ? Math.min(10, (s.combo ?? 0) + 1) : 0;
        s.alvo = i;
        return 1 + 0.06 * s.combo;
      },
    },
  },
  chunli: {
    nome: 'Cem chutes',
    texto: 'Chun-Li age 2 vezes mais rápido, mas cada ataque básico causa só 45% do dano. A cada 12 ataques básicos: 60 de dano em cada rival.',
    ganchos: {
      ritmo: () => 2,
      causa: (_m, _b, _f, _alvo, g) => (g.direto && !g.habilidade ? 0.45 : 1),
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || g.habilidade) return;
        u(f).chutes = (u(f).chutes ?? 0) + 1;
        if (u(f).chutes! % 12 !== 0) return;
        m.aviso(b, f, 'Spinning Bird Kick', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 60, false, 'Spinning Bird Kick');
      },
    },
  },
  darthvader: {
    nome: 'Estrangulamento da Força',
    texto: 'A cada 14 s, Darth Vader estrangula o rival com mais Vida por 3 s: esse rival fica Paralisado e perde 35 de Vida por segundo. Durante o estrangulamento, Darth Vader fica parado.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.aperta ?? 0) > 0) {
          const alvo = b.fighters[s.vitima!];
          s.aperta! -= dt;
          if (alvo && vivo(alvo)) m.dano(b, f, alvo, 35 * dt, false, 'Estrangulamento');
          return;
        }
        if (!relogio(f, 'forca', dt, 14, 9)) return;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        s.aperta = 3; s.vitima = b.fighters.indexOf(alvo);
        m.efeitos(b, f, [alvo], [st('paralyzed', 1, 3)]);
        m.aviso(b, f, 'Estrangulamento', alvo);
      },
      parado: (f) => (u(f).aperta ?? 0) > 0,
    },
  },
  garnet: {
    nome: 'Previsão',
    texto: 'Quando um rival começa um Preparo de 2,5 s ou mais (no máximo 1 vez a cada 20 s): todo o trio de Garnet fica Protegido (−40% de dano recebido) até 1 s depois de esse Preparo acabar.',
    ganchos: {
      viuPreparo(m, b, f, quem, preparo) {
        if (preparo < 2.5 || (u(f).visao ?? 0) > b.time) return;
        u(f).visao = b.time + 20;
        m.efeitos(b, f, m.aliados(b, f), [st('protected', 0.4, preparo + 1)]);
        m.aviso(b, f, 'Visão do futuro', quem);
      },
    },
  },
  nami: {
    nome: 'Clima a favor',
    texto: 'A cada 15 s, Nami muda o clima, nesta ordem. Sol: o trio de Nami fica Acelerado (15% mais rápido) por 4 s. Chuva: todos os rivais ficam Lento (15% mais lento) por 4 s. Raio: 70 de dano no rival com mais Vida.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'clima', dt, 15, 10)) return;
        const s = u(f), fase = (s.clima ?? 0) % 3;
        s.clima = fase + 1;
        if (fase === 0) { m.efeitos(b, f, m.aliados(b, f), [st('haste', 0.15, 4)]); m.aviso(b, f, 'Sol', f); }
        else if (fase === 1) { m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.15, 4)]); m.aviso(b, f, 'Chuva', f); }
        else { const alvo = maisForte(m, b, f); if (alvo) { m.aviso(b, f, 'Raio!', alvo); m.dano(b, f, alvo, 70, false, 'Raio'); } }
      },
    },
  },
  palpatine: {
    nome: 'Relâmpago em cadeia',
    texto: 'Todo dano das habilidades de Palpatine também atinge os outros rivais, com metade do dano.',
    ganchos: {
      bateu(m, b, f, alvo, dano, g) {
        if (!g.habilidade || g.label === 'Relâmpago em cadeia') return;
        for (const r of m.rivais(b, f)) if (r !== alvo) m.dano(b, f, r, dano * 0.5, false, 'Relâmpago em cadeia');
      },
    },
  },
};

export const UNICAS: Record<string, Unica> = { ...LOTE1, ...LOTE2, ...LOTE3, ...LOTE4, ...LOTE5, ...LOTE6, ...LOTE7, ...LOTE8, ...LOTE9 };
// o Kirby copia a mecânica de quem ele inala: precisa conhecer todas
conheceTodas(UNICAS);
export const unicaDe = (id: string): Unica | undefined => UNICAS[id];
