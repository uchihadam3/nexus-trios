/*
 * Mecânicas únicas — lote 7: mais 55 antigos (Sephiroth, Hulk, Sonic, Goku, Sasuke, Homem de Ferro…).
 */
import { avisoACada, CONTROLES, fracao, maisFerido, maisForte, quandoVira, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import type { Battle, Fighter } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const vidaDoTrio = (xs: Fighter[]) => xs.reduce((n, x) => n + fracao(x), 0);

export const LOTE7: Record<string, Unica> = {
  pyramidhead: {
    nome: 'Punição',
    texto: 'O ataque básico do Cabeça de Pirâmide vai sempre no rival que mais causou dano na luta, e todo dano do Cabeça de Pirâmide nesse rival tem +30%.',
    ganchos: {
      alvoDoBasico: (m, b, f) => m.rivais(b, f).sort((x, y) => y.stats.damage - x.stats.damage)[0],
      causa: (m, b, f, alvo) => (m.rivais(b, f).sort((x, y) => y.stats.damage - x.stats.damage)[0] === alvo ? 1.3 : 1),
    },
  },
  sephiroth: {
    nome: 'Uma asa',
    texto: 'Quando Sephiroth fica com menos de 50% da Vida, até o fim da luta, o ataque básico de Sephiroth acerta também os outros rivais, com 40% do dano.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).asa && fracao(f) < 0.5) { u(f).asa = 1; m.aviso(b, f, 'Asa negra', f); } },
      bateu(m, b, f, alvo, dano, g) {
        if (!u(f).asa || !g.direto || g.habilidade) return;
        for (const r of m.rivais(b, f)) if (r !== alvo) m.dano(b, f, r, dano * 0.4, false, 'Uma asa');
      },
    },
  },
  hyoga: {
    nome: 'Rumo ao zero absoluto',
    texto: 'A cada 5 golpes de Hyoga no mesmo rival, esse rival fica Congelado (+25% de dano no golpe que quebra o gelo) por 2 s, e a contagem recomeça.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const k = `grau${idx(b, alvo)}`;
        u(f)[k] = (u(f)[k] ?? 0) + 1;
        if (u(f)[k]! < 5) return;
        u(f)[k] = 0;
        m.efeitos(b, f, [alvo], [st('frozen', 0.25, 2)]);
        m.aviso(b, f, 'Zero absoluto', alvo);
      },
    },
  },
  camus: {
    nome: 'Esquife de gelo',
    texto: 'Aos 25 s de luta (1 vez por luta), Camus de Aquário prende o rival com mais Vida no esquife de gelo: por 6 s, esse rival fica Paralisado, e o trio de Camus não causa dano nele.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).esquife || b.time < 25) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        u(f).esquife = 1; u(f).preso = idx(b, a); u(f).ate = b.time + 6;
        m.efeitos(b, f, [a], [st('paralyzed', 1, 6)]);
        m.aviso(b, f, 'Esquife de gelo', a);
      },
      causa: (_m, b, f, alvo) => (u(f).preso === idx(b, alvo) && (u(f).ate ?? 0) > b.time ? 0 : 1),
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).preso === idx(b, alvo) && (u(f).ate ?? 0) > b.time ? 0 : 1),
    },
  },
  darkseid: {
    nome: 'Sem esperança',
    texto: 'Enquanto Darkseid está de pé, rivais com menos de 30% da Vida não recebem cura nenhuma.',
    ganchos: {
      curaNoRival(m, b, f, alvo) {
        if (fracao(alvo) >= 0.3) return 1;
        avisoACada(m, b, f, 'esperanca', 8, 'Sem esperança', alvo);
        return 0;
      },
    },
  },
  omniman: {
    nome: 'Orgulho viltrumita',
    texto: 'Se o trio de Omni-Man tem tanta ou mais Vida (em %) que os rivais, Omni-Man causa +25% de dano; se tem menos, causa −15% de dano.',
    ganchos: { causa: (m, b, f) => (vidaDoTrio(m.aliados(b, f)) >= vidaDoTrio(m.rivais(b, f)) ? 1.25 : 0.85) },
  },
  marvin: {
    nome: 'Cadê o kaboom?',
    texto: 'A cada 15 s, Marvin, o Marciano tenta o Modulador: 50% de chance de causar 160 de dano no rival com mais Vida; se não, nada de kaboom.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'modulador', dt, 15, 8)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        if (m.sorte(b) < 0.5) { m.aviso(b, f, 'Cadê o kaboom?', f); return; }
        m.aviso(b, f, 'KABOOM', a);
        m.dano(b, f, a, 160, false, 'Modulador');
      },
    },
  },
  mikasa: {
    nome: 'Ninguém toca neles',
    texto: 'Quando um rival acerta o aliado mais ferido de Mikasa Ackerman, Mikasa causa 60 de dano nesse rival na hora (no máximo 1 vez a cada 4 s).',
    ganchos: {
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (!g.direto || alvo === f || alvo.side !== f.side || fonte.side === f.side || !vivo(fonte)) return;
        if (maisFerido(m, b, f) !== alvo || (u(f).corte ?? 0) > b.time) return;
        u(f).corte = b.time + 4;
        avisoACada(m, b, f, 'protege', 8, 'Ninguém toca neles', fonte);
        m.dano(b, f, fonte, 60, false, 'Proteger quem importa');
      },
    },
  },
  sonic: {
    nome: 'Anéis',
    texto: 'Cada golpe de Sonic dá 1 anel (guarda até 20). Com 10 anéis ou mais, o próximo ataque ou habilidade que Sonic receberia não causa dano e custa 10 anéis.',
    ganchos: {
      bateu(_m, _b, f, _alvo, _dano, g) { if (g.direto) u(f).aneis = Math.min(20, (u(f).aneis ?? 0) + 1); },
      recebe(m, b, f, fonte, g) {
        if (!g.direto || (u(f).aneis ?? 0) < 10) return 1;
        u(f).aneis! -= 10;
        m.aviso(b, f, 'Perdeu os anéis', fonte);
        return 0;
      },
    },
  },
  sora: {
    nome: 'Forma de fusão',
    texto: 'A cada 20 s, Sora faz uma Forma de fusão com um aliado aleatório: por 6 s, Sora age 25% mais rápido, e esse aliado também age mais rápido.',
    ganchos: {
      passo(m, b, f, dt) {
        const outro = b.fighters[u(f).fusao ?? -1];
        if (outro && vivo(outro) && (u(f).ate ?? 0) > b.time) outro.action = Math.min(1, outro.action + dt * 0.08);
        if (!relogio(f, 'drive', dt, 20, 10)) return;
        const as = m.aliados(b, f).filter((a) => a !== f);
        if (!as.length) return;
        const a = as[Math.floor(m.sorte(b) * as.length)]!;
        u(f).fusao = idx(b, a); u(f).ate = b.time + 6;
        m.aviso(b, f, 'Forma de fusão', a);
      },
      ritmo: (_m, b, f) => ((u(f).ate ?? 0) > b.time ? 1.25 : 1),
    },
  },
  shiryu: {
    nome: 'Defesa absoluta',
    texto: 'O primeiro ataque ou habilidade de cada rival em Shiryu não causa dano.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.direto || u(f)[`escudo${idx(b, fonte)}`]) return 1;
        u(f)[`escudo${idx(b, fonte)}`] = 1;
        m.aviso(b, f, 'Escudo do Dragão', fonte);
        return 0;
      },
    },
  },
  gaara: {
    nome: 'Areia que se refaz',
    texto: 'Gaara começa com Escudo de areia de 10% da Vida máxima. Depois de 5 s sem levar golpe, a areia se refaz: +0,6% da Vida máxima de Escudo por segundo, até 10%.',
    ganchos: {
      inicio(m, b, f) { f.shields.push({ amount: f.maxHp * 0.1, remaining: 999, source: f.uid }); m.aviso(b, f, 'Areia que se refaz', f); },
      apanhou(_m, b, f) { u(f).quieto = b.time + 5; },
      passo(_m, b, f, dt) {
        if ((u(f).quieto ?? 0) > b.time) return;
        const areia = f.shields.find((s) => s.source === f.uid && s.remaining > 100);
        if (areia) areia.amount = Math.min(f.maxHp * 0.1, areia.amount + f.maxHp * 0.006 * dt);
        else f.shields.push({ amount: f.maxHp * 0.006 * dt, remaining: 999, source: f.uid });
      },
    },
  },
  bobesponja: {
    nome: 'Esponja',
    texto: '20% de todo dano que Bob Esponja leva vira cura no aliado mais ferido (sem contar o próprio Bob Esponja).',
    ganchos: {
      apanhou(m, b, f, _fonte, dano) {
        const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => fracao(x) - fracao(y))[0];
        if (a) m.cura(b, f, a, dano * 0.2, 'Esponja');
      },
    },
  },
  korra: {
    nome: 'Fúria do Avatar',
    texto: 'Com menos de 35% da Vida (1 vez por luta): por 6 s, Korra entra no Estado Avatar: causa o dobro de dano e nunca fica Paralisado, Congelado, Dormindo, Confuso, Silenciado, Lento nem Preso.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).avatar && fracao(f) < 0.35) { u(f).avatar = b.time + 6; m.aviso(b, f, 'Estado Avatar', f); } },
      causa: (_m, b, f) => ((u(f).avatar ?? 0) > b.time ? 2 : 1),
      imune: (f, s) => (u(f).avatar ?? 0) > 0 && CONTROLES.includes(s) && (u(f).avatar ?? 0) > (u(f).agora ?? 0),
      passo(_m, b, f) { u(f).agora = b.time; },
    },
  },
  taz: {
    nome: 'Furacão da Tasmânia',
    texto: 'Taz nunca fica Preso, Lento nem Provocado. Cada golpe de Taz acerta também outro rival aleatório, com 30% do dano.',
    ganchos: {
      imune: (_f, s) => s === 'rooted' || s === 'slow' || s === 'provoked',
      bateu(m, b, f, alvo, dano, g) {
        if (!g.direto || g.label === 'Redemoinho') return;
        const outros = m.rivais(b, f).filter((r) => r !== alvo);
        if (outros.length) m.dano(b, f, outros[Math.floor(m.sorte(b) * outros.length)]!, dano * 0.3, false, 'Redemoinho');
      },
    },
  },
  blackpanther: {
    nome: 'Traje cinético',
    texto: 'Cada golpe que o Pantera Negra leva guarda energia cinética: +10% de dano no próximo golpe do Pantera Negra (até +60%), que gasta toda a energia.',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).cinetica = Math.min(6, (u(f).cinetica ?? 0) + 1); },
      causa(_m, _b, f, _alvo, g) { if (!g.direto) return 1; const k = 1 + 0.1 * (u(f).cinetica ?? 0); u(f).cinetica = 0; return k; },
    },
  },
  captainmarvel: {
    nome: 'Energia absorvida',
    texto: 'A Capitã Marvel nunca fica Queimando nem Eletrificado. Cada vez que um desses tentaria pegar nela, a Capitã Marvel ganha +10% de dano até o fim da luta (até +50%).',
    ganchos: {
      imune(f, s) {
        if (s !== 'burning' && s !== 'electric') return false;
        u(f).binaria = Math.min(5, (u(f).binaria ?? 0) + 1);
        return true;
      },
      causa: (_m, _b, f) => 1 + 0.1 * (u(f).binaria ?? 0),
    },
  },
  liukang: {
    nome: 'Mortal Kombat',
    texto: 'Quando Liu Kang fica sozinho contra um só rival: +40% de dano e −20% de dano recebido.',
    ganchos: {
      passo(m, b, f) { quandoVira(m, b, f, 'kombat', m.aliados(b, f).length === 1 && m.rivais(b, f).length === 1, 'Mortal Kombat', f); },
      causa: (m, b, f) => (m.aliados(b, f).length === 1 && m.rivais(b, f).length === 1 ? 1.4 : 1),
      recebe: (m, b, f) => (m.aliados(b, f).length === 1 && m.rivais(b, f).length === 1 ? 0.8 : 1),
    },
  },
  storm: {
    nome: 'Tempestade que pula',
    texto: 'A cada 3 s, cada rival Eletrificado leva 15 de dano da Tempestade e passa o choque para outro rival, que fica Eletrificado (−15% da barra por golpe) por 3 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'raios', dt, 3, 3)) return;
        const rs = m.rivais(b, f);
        const eletrificado = rs.find((x) => m.intensidade(x, 'electric') > 0);
        if (eletrificado) avisoACada(m, b, f, 'tempestade', 9, 'Tempestade que pula', eletrificado);
        for (const r of rs.filter((x) => m.intensidade(x, 'electric') > 0)) {
          m.dano(b, f, r, 15, false, 'Tempestade');
          const outro = rs.find((x) => x !== r && m.intensidade(x, 'electric') <= 0);
          if (outro) m.efeitos(b, f, [outro], [st('electric', 0.25, 3)]);
        }
      },
    },
  },
  leon: {
    nome: 'Na faca',
    texto: 'Quando todas as habilidades de Leon S. Kennedy estão em Resfriamento ou ainda carregando (e pelo menos uma está em Resfriamento), o ataque básico de Leon causa +50% de dano.',
    ganchos: {
      passo(m, b, f) { quandoVira(m, b, f, 'faca', f.skills.every((s) => s.cooldown > 0 || s.charge < 100) && f.skills.some((s) => s.cooldown > 0), 'Na faca', f); },
      causa: (_m, _b, f, _alvo, g) => (g.direto && !g.habilidade && f.skills.every((s) => s.cooldown > 0 || s.charge < 100) && f.skills.some((s) => s.cooldown > 0) ? 1.5 : 1),
    },
  },
  hayabusa: {
    nome: 'Primeiro a agir',
    texto: 'Ryu Hayabusa começa a luta com a barra do Próximo ataque cheia. Cada rival que cai enche essa barra de novo.',
    ganchos: {
      inicio(_m, _b, f) { f.action = 1; },
      caiu(_m, _b, f, quem) { if (quem.side !== f.side) f.action = 1; },
    },
  },
  hiei: {
    nome: 'Rápido demais para ver',
    texto: 'Cada habilidade rival em Hiei tem 33% de chance de não causar dano.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.habilidade || m.sorte(b) >= 1 / 3) return 1;
        m.aviso(b, f, 'Não estava lá', fonte);
        return 0;
      },
    },
  },
  samuraijack: {
    nome: 'Lâmina mágica',
    texto: 'Os golpes de Samurai Jack passam pelo Escudo e vão direto na Vida.',
    ganchos: {
      atravessaEscudo: true,
    },
  },
  peter: {
    nome: 'Briga sem fim',
    texto: 'A cada 20 s, Peter Griffin briga com o galo: o rival com mais Vida perde 10% da Vida máxima, e Peter perde 5% da Vida máxima (sem cair por isso).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'galo', dt, 20, 10)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        m.aviso(b, f, 'Briga com o galo!', a);
        m.dano(b, f, a, a.maxHp * 0.1, false, 'Briga');
        f.hp = Math.max(1, f.hp - f.maxHp * 0.05);
      },
    },
  },
  hulk: {
    nome: 'Cada vez maior',
    texto: 'Cada golpe que o Hulk leva deixa o Hulk maior: +0,5% de Vida máxima e +0,5% de dano (até 20 golpes: +10%).',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) {
        if (!g.direto || (u(f).tamanho ?? 0) >= 20) return;
        u(f).tamanho = (u(f).tamanho ?? 0) + 1;
        const extra = f.maxHp * 0.005; f.maxHp += extra; f.hp += extra;
      },
      causa: (_m, _b, f) => 1 + 0.005 * (u(f).tamanho ?? 0),
    },
  },
  rocket: {
    nome: 'Minas espalhadas',
    texto: 'Rocket Raccoon espalha 3 minas: os 3 primeiros golpes de rivais em qualquer um do trio explodem em quem bateu, com 50 de dano cada.',
    ganchos: {
      inicio(_m, _b, f) { u(f).minas = 3; },
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (!g.direto || !(u(f).minas ?? 0) || alvo.side !== f.side || fonte.side === f.side || !vivo(fonte)) return;
        u(f).minas! -= 1;
        m.aviso(b, f, 'Mina!', fonte);
        m.dano(b, f, fonte, 50, false, 'Mina');
      },
    },
  },
  michelangelo: {
    nome: 'Pura improvisação',
    texto: 'O ataque básico de Michelangelo vai num rival aleatório, com um dano sorteado entre metade e o dobro.',
    ganchos: {
      alvoDoBasico(m, b, f) { const rs = m.rivais(b, f); return rs[Math.floor(m.sorte(b) * rs.length)]; },
      causa: (m, b, _f, _alvo, g) => (g.direto && !g.habilidade ? 0.5 + 1.5 * m.sorte(b) : 1),
    },
  },
  azula: {
    nome: 'Prodígio instável',
    texto: 'Com mais de 70% da Vida, Azula causa +30% de dano. Com menos de 30% da Vida, Azula age 25% mais rápido, mas cada golpe tem 20% de chance de errar.',
    ganchos: {
      passo(m, b, f) {
        quandoVira(m, b, f, 'prodigio', fracao(f) > 0.7, 'Prodígio', f);
        quandoVira(m, b, f, 'instavel', fracao(f) < 0.3, 'Instável', f);
      },
      causa: (m, b, f, _alvo, g) => (fracao(f) > 0.7 ? 1.3 : fracao(f) < 0.3 && g.direto && m.sorte(b) < 0.2 ? 0 : 1),
      ritmo: (_m, _b, f) => (fracao(f) < 0.3 ? 1.25 : 1),
    },
  },
  zelda: {
    nome: 'Selo da sabedoria',
    texto: 'A primeira habilidade de cada rival em Zelda ou no trio de Zelda causa −40% de dano.',
    ganchos: {
      recebe: (m, b, f, fonte, g) => selo(m, b, f, f, fonte, g.habilidade),
      recebeAliado: (m, b, f, aliado, fonte, g) => selo(m, b, f, aliado, fonte, g.habilidade),
    },
  },
  shun: {
    nome: 'Corrente que intercepta',
    texto: 'Todo golpe acima de 120 de dano em alguém do trio de Shun chega com 40 a menos.',
    ganchos: {
      limita(m, b, f, alvo, valor) {
        if (valor <= 120) return valor;
        avisoACada(m, b, f, 'corrente', 6, 'Corrente que intercepta', alvo);
        return valor - 40;
      },
    },
  },
  picapau: {
    nome: 'Impossível ignorar',
    texto: 'Quem acerta o Pica-Pau com ataque ou habilidade fica Provocado (só mira no Pica-Pau) por 2 s.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte) && fonte.side !== f.side) m.efeitos(b, f, [fonte], [st('provoked', 1, 2)]); } },
  },
  salsicha: {
    nome: 'Poder escondido',
    texto: 'Quando o Salsicha fica sozinho no trio, causa o triplo de dano.',
    ganchos: {
      causa: (m, b, f) => (m.aliados(b, f).length === 1 ? 3 : 1),
      caiu(m, b, f, quem) { if (quem.side === f.side && m.aliados(b, f).length === 1 && !u(f).poder) { u(f).poder = 1; m.aviso(b, f, 'Zoinks… 1% do poder', f); } },
    },
  },
  patolino: {
    nome: 'Temporada de pato!',
    texto: 'A cada 12 s, Patolino deixa o rival com mais Vida Confuso por 2 s.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'temporada', dt, 12, 7)) { const a = maisForte(m, b, f); if (a) { m.efeitos(b, f, [a], [st('confused', 1, 2)]); m.aviso(b, f, 'Temporada de coelho!', a); } } },
    },
  },
  skeletor: {
    nome: 'Nyeh!',
    texto: 'Cada habilidade de Skeletor que não derruba ninguém deixa Skeletor mais irritado: +4% de dano (até +40%).',
    ganchos: {
      antes(m, b, f) { u(f).caidosAntes = b.fighters.filter((x) => x.side !== f.side && !vivo(x)).length; void m; },
      usou(m, b, f) {
        const agora = b.fighters.filter((x) => x.side !== f.side && !vivo(x)).length;
        if (agora > (u(f).caidosAntes ?? 0) || (u(f).furia ?? 0) >= 10) return;
        u(f).furia = (u(f).furia ?? 0) + 1;
        m.aviso(b, f, 'Nyeh!', f);
      },
      causa: (_m, _b, f) => 1 + 0.04 * (u(f).furia ?? 0),
    },
  },
  mojojojo: {
    nome: 'Blindagem do robô',
    texto: 'O Macaco Louco começa com Escudo de 20% da Vida máxima (o robô). Quando esse Escudo quebra, o Macaco Louco causa +10% de dano até o fim da luta.',
    ganchos: {
      inicio(_m, _b, f) { f.shields.push({ amount: f.maxHp * 0.2, remaining: 999, source: f.uid }); u(f).robo = 1; },
      passo(m, b, f) { if (u(f).robo === 1 && !f.shields.some((s) => s.remaining > 100)) { u(f).robo = 2; m.aviso(b, f, 'O robô quebrou!', f); } },
      causa: (_m, _b, f) => (u(f).robo === 2 ? 1.1 : 1),
    },
  },
  zenitsu: {
    nome: 'Luta dormindo',
    texto: 'Com menos de 65% da Vida, Zenitsu Agatsuma desmaia e luta dormindo até o fim da luta: +60% de dano, e nunca fica Dormindo nem Confuso.',
    ganchos: {
      imune: (f, s) => (u(f).desmaio ?? 0) > 0 && (s === 'sleep' || s === 'confused'),
      apanhou(m, b, f) { if (!u(f).desmaio && fracao(f) < 0.65) { u(f).desmaio = 1; m.aviso(b, f, 'Zzz… Primeira postura', f); } },
      causa: (_m, _b, f) => (u(f).desmaio ? 1.6 : 1),
    },
  },
  loid: {
    nome: 'Operação Strix',
    texto: 'Loid Forger começa a luta com 20% de Carga em todas as habilidades.',
    ganchos: { inicio(_m, _b, f) { for (const s of f.skills) s.charge = 20; } },
  },
  pain: {
    nome: 'Empurrão universal',
    texto: 'A cada 15 s, Pain usa o Shinra Tensei: todos os rivais perdem o Preparo e levam 50 de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'shinra', dt, 15, 9)) return;
        m.aviso(b, f, 'Shinra Tensei', f);
        for (const r of m.rivais(b, f)) { r.cast = null; m.dano(b, f, r, 50, false, 'Shinra Tensei'); }
      },
    },
  },
  spawn: {
    nome: 'Necroplasma',
    texto: 'Com menos de 50% da Vida, Spawn cura 2% da Vida máxima por segundo, até gastar 600 de cura na luta.',
    ganchos: {
      inicio(_m, _b, f) { u(f).necro = 600; },
      passo(m, b, f, dt) {
        if (fracao(f) >= 0.5 || (u(f).necro ?? 0) <= 0) return;
        if (!u(f).necroAviso) { u(f).necroAviso = 1; m.aviso(b, f, 'Necroplasma', f); }
        const c = Math.min(u(f).necro!, f.maxHp * 0.02 * dt);
        u(f).necro! -= c;
        m.cura(b, f, f, c, 'Necroplasma');
      },
    },
  },
  heman: {
    nome: 'Poder de Grayskull',
    texto: 'A cada 20 s, He-Man ergue a Espada do Poder: fica Fortalecido (+40% de dano) e Protegido (−20% de dano recebido) por 5 s.',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'forca', dt, 20, 10)) { m.efeitos(b, f, [f], [st('strengthened', 0.4, 5), st('protected', 0.2, 5)]); m.aviso(b, f, 'Eu tenho a força!', f); } } },
  },
  shera: {
    nome: 'Espada que muda',
    texto: 'Cada habilidade de She-Ra muda a espada, nesta ordem. Escudo: 80 de Escudo por 10 s. Laço: o rival com mais Vida fica Preso (65% mais lento) por 2 s. Espada: a habilidade seguinte de She-Ra causa +50% de dano.',
    ganchos: {
      usou(m, b, f) {
        const k = (u(f).forma ?? 0) % 3;
        u(f).forma = k + 1;
        if (k === 0) { f.shields.push({ amount: 80, remaining: 10, source: f.uid }); m.aviso(b, f, 'Escudo', f); }
        else if (k === 1) { const a = maisForte(m, b, f); if (a) { m.efeitos(b, f, [a], [st('rooted', 1, 2)]); m.aviso(b, f, 'Laço', a); } }
        else { u(f).espada = 1; m.aviso(b, f, 'Espada', f); }
      },
      causa(_m, _b, f, _alvo, g) { return g.habilidade && u(f).espada ? 1.5 : 1; },
      antes(_m, _b, f) { if (u(f).espada === 1) u(f).espada = 2; else if (u(f).espada === 2) u(f).espada = 0; },
    },
  },
  buzz: {
    nome: 'Manobra espacial',
    texto: 'A cada 15 s, Buzz Lightyear voa por 2 s: nesse tempo, ataques básicos de rivais não causam dano em Buzz.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'asas', dt, 15, 8)) { u(f).voo = b.time + 2; m.aviso(b, f, 'Ao infinito e além!', f); } },
      recebe: (_m, b, f, _fonte, g) => ((u(f).voo ?? 0) > b.time && g.direto && !g.habilidade ? 0 : 1),
    },
  },
  pantera: {
    nome: 'O roubo do diamante',
    texto: 'A cada 15 s, a Pantera Cor-de-Rosa rouba o Escudo e a Barreira do rival com mais Vida e dá tudo ao aliado mais ferido (o Escudo roubado dura 10 s).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'roubo', dt, 15, 8)) return;
        const a = maisForte(m, b, f), quem = maisFerido(m, b, f);
        if (!a || !quem) return;
        const escudo = a.shields.reduce((n, s) => n + s.amount, 0), barreira = a.statuses.find((s) => s.id === 'barrier');
        if (!escudo && !barreira) return;
        a.shields = []; a.statuses = a.statuses.filter((s) => s.id !== 'barrier');
        if (escudo) quem.shields.push({ amount: escudo, remaining: 10, source: f.uid });
        if (barreira) m.efeitos(b, f, [quem], [st('barrier', barreira.intensity, Math.max(2, barreira.remaining))]);
        m.aviso(b, f, 'Roubou o diamante', a);
      },
    },
  },
  plankton: {
    nome: 'Ladrão de Carga',
    texto: 'A cada 15 s, Plankton rouba até 25% de Carga da habilidade rival mais cheia e coloca na habilidade mais cheia de Plankton (fora do Resfriamento).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'formula', dt, 15, 8)) return;
        let melhor: { r: Fighter; i: number } | undefined;
        for (const r of m.rivais(b, f)) r.skills.forEach((s, i) => { if (!melhor || s.charge > melhor.r.skills[melhor.i]!.charge) melhor = { r, i }; });
        if (!melhor) return;
        const tirado = Math.min(25, melhor.r.skills[melhor.i]!.charge);
        melhor.r.skills[melhor.i]!.charge -= tirado;
        const minha = f.skills.filter((s) => s.cooldown <= 0).sort((x, y) => y.charge - x.charge)[0];
        if (minha) minha.charge = Math.min(100, minha.charge + tirado);
        m.aviso(b, f, 'A fórmula é minha!', melhor.r);
      },
    },
  },
  princeofpersia: {
    nome: 'Tempo mais lento',
    texto: 'A cada 20 s, o Príncipe da Pérsia usa as Areias do Tempo: todos os rivais ficam Lento (40% mais lento) por 3 s.',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'adaga', dt, 20, 10)) { m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.4, 3)]); m.aviso(b, f, 'Areias do Tempo', f); } } },
  },
  trunks: {
    nome: 'Viagem no tempo',
    texto: 'Aos 40 s de luta (1 vez por luta): se o trio de Trunks tiver menos Vida (em %) que os rivais, todo o trio cura 20% da Vida máxima.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).futuro || b.time < 40) return;
        u(f).futuro = 1;
        if (vidaDoTrio(m.aliados(b, f)) >= vidaDoTrio(m.rivais(b, f))) return;
        for (const a of m.aliados(b, f)) m.cura(b, f, a, a.maxHp * 0.2, 'Do futuro');
        m.aviso(b, f, 'Eu vim do futuro', f);
      },
    },
  },
  iroh: {
    nome: 'Fogo em todos',
    texto: 'A cada 12 s, Iroh solta o Dragão do Oeste: todos os rivais ficam Queimando (−12 de Vida por segundo) por 4 s.',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'dragao', dt, 12, 7)) { m.efeitos(b, f, m.rivais(b, f), [st('burning', 12, 4)]); m.aviso(b, f, 'Dragão do Oeste', f); } } },
  },
  splinter: {
    nome: 'Contra-golpe do mestre',
    texto: 'Cada golpe que o Mestre Splinter leva tem 33% de chance de contra-golpe: 50 de dano em quem bateu, que fica Exposto (+10% de dano recebido) por 3 s.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.direto || fonte.side === f.side || !vivo(fonte) || m.sorte(b) >= 1 / 3) return;
        m.efeitos(b, f, [fonte], [st('exposed', 0.1, 3)]);
        m.dano(b, f, fonte, 50, false, 'Contra-ataque');
      },
    },
  },
  goku: {
    nome: 'Genki Dama',
    texto: 'Aos 30 s de luta (1 vez por luta), Goku lança a Genki Dama no rival com mais Vida: 60 de dano para cada lutador de pé (dos dois trios).',
    ganchos: {
      passo(m, b, f) {
        if (u(f).genki || b.time < 30) return;
        u(f).genki = 1;
        const a = maisForte(m, b, f);
        if (!a) return;
        const n = b.fighters.filter(vivo).length;
        m.aviso(b, f, 'Genki Dama!', a, n);
        // pedido do jogador: "40 de dano por personagem… achei que tava um pouco fraco"
        m.dano(b, f, a, 60 * n, false, 'Genki Dama');
      },
    },
  },
  sasuke: {
    nome: 'Olho que aprende',
    texto: 'Depois de levar uma habilidade de um rival, Sasuke aprende: essa mesma habilidade desse rival nunca mais causa dano em Sasuke.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.habilidade || g.indice === undefined) return 1;
        const k = `lida${idx(b, fonte)}_${g.indice}`;
        if (!u(f)[k]) { u(f)[`vendo${idx(b, fonte)}_${g.indice}`] = 1; return 1; }
        m.aviso(b, f, 'Já vi essa', fonte);
        return 0;
      },
      apanhou(_m, b, f, fonte, _dano, g) { if (g.habilidade && g.indice !== undefined) u(f)[`lida${idx(b, fonte)}_${g.indice}`] = 1; },
    },
  },
  yuji: {
    nome: 'Na zona',
    texto: 'Cada golpe de Yuji Itadori tem 12,5% de chance de Black Flash (o dobro de dano). Depois de um Black Flash, por 8 s, essa chance sobe para 20%.',
    ganchos: {
      causa(m, b, f, alvo, g) {
        if (!g.direto) return 1;
        const chance = (u(f).zona ?? 0) > b.time ? 0.2 : 1 / 8;
        if (m.sorte(b) >= chance) return 1;
        u(f).zona = b.time + 8;
        m.aviso(b, f, 'Black Flash', alvo);
        return 2;
      },
    },
  },
  alucardcv: {
    nome: 'Familiar',
    texto: 'A cada 10 s, o familiar de Alucard causa 25 de dano no rival com mais Vida, e Alucard cura 25 de Vida.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'familiar', dt, 10, 6)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        m.aviso(b, f, 'Familiar', a);
        m.dano(b, f, a, 25, false, 'Familiar');
        m.cura(b, f, f, 25, 'Familiar');
      },
    },
  },
  ironman: {
    nome: 'Reator do Unibeam',
    texto: 'Cada habilidade que alguém do trio do Homem de Ferro usa carrega o reator em 15%. Com o reator em 100%: Unibeam de 200 de dano no rival com mais Vida, e o reator zera.',
    ganchos: {
      passo(m, b, f) {
        const usos = m.aliados(b, f).reduce((n, a) => n + a.stats.skills, 0) + b.fighters.filter((x) => x.side === f.side && !vivo(x)).reduce((n, a) => n + a.stats.skills, 0);
        const novos = usos - (u(f).usos ?? 0);
        u(f).usos = usos;
        if (novos <= 0) return;
        u(f).reator = (u(f).reator ?? 0) + 15 * novos;
        if (u(f).reator! < 100) return;
        u(f).reator = 0;
        const a = maisForte(m, b, f);
        if (a) { m.aviso(b, f, 'Unibeam', a); m.dano(b, f, a, 200, false, 'Unibeam'); }
      },
    },
  },
  piccolo: {
    nome: 'Mentor',
    texto: 'No começo da luta, Piccolo treina o aliado com menos Vida máxima: enquanto Piccolo estiver de pé, esse aliado causa +15% de dano e recebe −15% de dano.',
    ganchos: {
      inicio(m, b, f) {
        const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => x.maxHp - y.maxHp)[0];
        if (a) { u(f).aluno = idx(b, a); m.aviso(b, f, 'Treino', a); }
      },
      causaAliado: (_m, b, f, aliado) => (u(f).aluno === idx(b, aliado) ? 1.15 : 1),
      recebeAliado: (_m, b, f, aliado) => (u(f).aluno === idx(b, aliado) ? 0.85 : 1),
    },
  },
  aang: {
    nome: 'Planador',
    texto: 'Aang tem Esquiva (20% de chance de desviar) a luta toda. Cada vez que desvia, Aang ganha 40% da barra do Próximo ataque.',
    ganchos: {
      inicio(m, b, f) { m.efeitos(b, f, [f], [st('evasion', 0.2, 999)]); },
      desviou(_m, _b, f) { f.action = Math.min(1, f.action + 0.4); },
    },
  },
};

/* Selo da Zelda: a primeira habilidade de cada rival no trio dela perde 40% da força. */
function selo(m: Motor, b: Battle, zelda: Fighter, alvo: Fighter, fonte: Fighter, habilidade: boolean): number {
  if (!habilidade || fonte.side === zelda.side) return 1;
  const k = `selo${idx(b, fonte)}`;
  if (u(zelda)[k]) return 1;
  u(zelda)[k] = 1;
  m.aviso(b, zelda, 'Selo da Luz', alvo);
  return 0.6;
}
