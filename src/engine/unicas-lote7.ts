/*
 * Mecânicas únicas — lote 7: mais 55 antigos (Sephiroth, Hulk, Sonic, Goku, Sasuke, Homem de Ferro…).
 */
import { CONTROLES, fracao, maisFerido, maisForte, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import type { Battle, Fighter } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const vidaDoTrio = (xs: Fighter[]) => xs.reduce((n, x) => n + fracao(x), 0);

export const LOTE7: Record<string, Unica> = {
  pyramidhead: {
    nome: 'Punição',
    texto: 'O ataque básico vai sempre no rival que mais causou dano na luta, com 30% a mais.',
    ganchos: {
      alvoDoBasico: (m, b, f) => m.rivais(b, f).sort((x, y) => y.stats.damage - x.stats.damage)[0],
      causa: (m, b, f, alvo) => (m.rivais(b, f).sort((x, y) => y.stats.damage - x.stats.damage)[0] === alvo ? 1.3 : 1),
    },
  },
  sephiroth: {
    nome: 'Uma asa',
    texto: 'Abaixo de 50% da Vida, o ataque básico acerta também os outros rivais com 40%.',
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
    texto: 'No 5º golpe direto no mesmo rival, ele fica Congelado 2 s (e conta de novo).',
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
    texto: 'Aos 25 s (uma vez), o rival mais forte fica 6 s sem agir e sem levar dano.',
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
    texto: 'Enquanto ele está de pé, rivais abaixo de 30% da Vida não recebem cura.',
    ganchos: { curaNoRival: (_m, _b, _f, alvo) => (fracao(alvo) < 0.3 ? 0 : 1) },
  },
  omniman: {
    nome: 'Orgulho viltrumita',
    texto: 'Com mais Vida no trio que os rivais, causa 25% a mais; com menos, 15% a menos.',
    ganchos: { causa: (m, b, f) => (vidaDoTrio(m.aliados(b, f)) >= vidaDoTrio(m.rivais(b, f)) ? 1.25 : 0.85) },
  },
  marvin: {
    nome: 'Cadê o kaboom?',
    texto: 'A cada 15 s, metade das vezes: 160 de dano no rival mais forte.',
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
    texto: 'Quem bate no aliado mais ferido leva 60 de dano na hora (a cada 4 s).',
    ganchos: {
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (!g.direto || alvo === f || alvo.side !== f.side || fonte.side === f.side || !vivo(fonte)) return;
        if (maisFerido(m, b, f) !== alvo || (u(f).corte ?? 0) > b.time) return;
        u(f).corte = b.time + 4;
        m.dano(b, f, fonte, 60, false, 'Proteger quem importa');
      },
    },
  },
  sonic: {
    nome: 'Anéis',
    texto: 'Cada golpe direto dá 1 anel (até 20). Com 10 ou mais, um golpe que levaria gasta 10 anéis em vez de Vida.',
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
    texto: 'A cada 20 s, ele e um aliado agem 25% mais rápido por 6 s.',
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
    texto: 'O primeiro golpe direto de cada rival nele não pega.',
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
    texto: 'Começa com Escudo de 10% da Vida. Depois de 5 s sem levar golpe, recupera 0,6% por segundo (até 10%).',
    ganchos: {
      inicio(_m, _b, f) { f.shields.push({ amount: f.maxHp * 0.1, remaining: 999, source: f.uid }); },
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
    texto: '20% do dano que leva vira cura no aliado mais ferido.',
    ganchos: {
      apanhou(m, b, f, _fonte, dano) {
        const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => fracao(x) - fracao(y))[0];
        if (a) m.cura(b, f, a, dano * 0.2, 'Esponja');
      },
    },
  },
  korra: {
    nome: 'Fúria do Avatar',
    texto: 'Abaixo de 35% da Vida (uma vez), por 6 s: causa o dobro e nenhum controle a segura.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).avatar && fracao(f) < 0.35) { u(f).avatar = b.time + 6; m.aviso(b, f, 'Estado Avatar', f); } },
      causa: (_m, b, f) => ((u(f).avatar ?? 0) > b.time ? 2 : 1),
      imune: (f, s) => (u(f).avatar ?? 0) > 0 && CONTROLES.includes(s) && (u(f).avatar ?? 0) > (u(f).agora ?? 0),
      passo(_m, b, f) { u(f).agora = b.time; },
    },
  },
  taz: {
    nome: 'Furacão da Tasmânia',
    texto: 'Não fica Preso, Lento nem Provocado. Cada golpe direto acerta também um rival aleatório com 30%.',
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
    texto: 'Cada golpe que leva dá +10% de dano no próximo golpe dele (até 60%).',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).cinetica = Math.min(6, (u(f).cinetica ?? 0) + 1); },
      causa(_m, _b, f, _alvo, g) { if (!g.direto) return 1; const k = 1 + 0.1 * (u(f).cinetica ?? 0); u(f).cinetica = 0; return k; },
    },
  },
  captainmarvel: {
    nome: 'Energia absorvida',
    texto: 'Não fica Queimando nem Eletrificado; cada vez que um tentaria, ganha +10% de dano (até 50%).',
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
    texto: 'Sozinho contra um só rival: causa 40% a mais e recebe 20% a menos.',
    ganchos: {
      causa: (m, b, f) => (m.aliados(b, f).length === 1 && m.rivais(b, f).length === 1 ? 1.4 : 1),
      recebe: (m, b, f) => (m.aliados(b, f).length === 1 && m.rivais(b, f).length === 1 ? 0.8 : 1),
    },
  },
  storm: {
    nome: 'Tempestade que pula',
    texto: 'A cada 3 s, cada rival Eletrificado leva 15 de dano e passa o choque para outro rival.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'raios', dt, 3, 3)) return;
        const rs = m.rivais(b, f);
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
    texto: 'Com todas as habilidades em Resfriamento, o ataque básico causa 50% a mais.',
    ganchos: { causa: (_m, _b, f, _alvo, g) => (g.direto && !g.habilidade && f.skills.every((s) => s.cooldown > 0 || s.charge < 100) && f.skills.some((s) => s.cooldown > 0) ? 1.5 : 1) },
  },
  hayabusa: {
    nome: 'Primeiro a agir',
    texto: 'Começa com a ação pronta. Cada rival que cai enche a ação dele de novo.',
    ganchos: {
      inicio(_m, _b, f) { f.action = 1; },
      caiu(_m, _b, f, quem) { if (quem.side !== f.side) f.action = 1; },
    },
  },
  hiei: {
    nome: 'Rápido demais para ver',
    texto: '1 em 3 habilidades rivais nele não pegam.',
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
    texto: 'Os golpes diretos dele ignoram Escudo.',
    ganchos: {
      atravessaEscudo: true,
    },
  },
  peter: {
    nome: 'Briga sem fim',
    texto: 'A cada 20 s: o rival mais forte perde 10% da Vida máxima e Peter 5%.',
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
    texto: 'Cada golpe que leva: +0,5% de Vida máxima e +0,5% de dano (até 10%).',
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
    texto: 'Os 3 primeiros golpes diretos no trio explodem em quem bateu (50 cada).',
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
    texto: 'O ataque básico vai num rival aleatório, com força entre metade e o dobro.',
    ganchos: {
      alvoDoBasico(m, b, f) { const rs = m.rivais(b, f); return rs[Math.floor(m.sorte(b) * rs.length)]; },
      causa: (m, b, _f, _alvo, g) => (g.direto && !g.habilidade ? 0.5 + 1.5 * m.sorte(b) : 1),
    },
  },
  azula: {
    nome: 'Prodígio instável',
    texto: 'Acima de 70% da Vida causa 30% a mais. Abaixo de 30%, age 25% mais rápido, mas 1 em 5 golpes erra.',
    ganchos: {
      causa: (m, b, f, _alvo, g) => (fracao(f) > 0.7 ? 1.3 : fracao(f) < 0.3 && g.direto && m.sorte(b) < 0.2 ? 0 : 1),
      ritmo: (_m, _b, f) => (fracao(f) < 0.3 ? 1.25 : 1),
    },
  },
  zelda: {
    nome: 'Selo da sabedoria',
    texto: 'A primeira habilidade de cada rival no trio perde 40% da força.',
    ganchos: {
      recebe: (m, b, f, fonte, g) => selo(m, b, f, f, fonte, g.habilidade),
      recebeAliado: (m, b, f, aliado, fonte, g) => selo(m, b, f, aliado, fonte, g.habilidade),
    },
  },
  shun: {
    nome: 'Corrente que intercepta',
    texto: 'Golpe acima de 120 em alguém do trio chega 40 mais fraco.',
    ganchos: { limita: (_m, _b, _f, _alvo, valor) => (valor > 120 ? valor - 40 : valor) },
  },
  picapau: {
    nome: 'Impossível ignorar',
    texto: 'Quem o acerta fica Provocado nele por 2 s.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte) && fonte.side !== f.side) m.efeitos(b, f, [fonte], [st('provoked', 1, 2)]); } },
  },
  salsicha: {
    nome: 'Poder escondido',
    texto: 'Quando sobra só ele no trio, causa o triplo.',
    ganchos: {
      causa: (m, b, f) => (m.aliados(b, f).length === 1 ? 3 : 1),
      caiu(m, b, f, quem) { if (quem.side === f.side && m.aliados(b, f).length === 1 && !u(f).poder) { u(f).poder = 1; m.aviso(b, f, 'Zoinks… 1% do poder', f); } },
    },
  },
  patolino: {
    nome: 'Temporada de pato!',
    texto: 'A cada 12 s, o rival mais forte fica Confuso 2 s.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'temporada', dt, 12, 7)) { const a = maisForte(m, b, f); if (a) { m.efeitos(b, f, [a], [st('confused', 1, 2)]); m.aviso(b, f, 'Temporada de coelho!', a); } } },
    },
  },
  skeletor: {
    nome: 'Nyeh!',
    texto: 'Cada habilidade dele que não derruba ninguém: +4% de dano (até 40%).',
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
    texto: 'Começa com Escudo de 20% da Vida. Quando quebra, causa 10% a mais.',
    ganchos: {
      inicio(_m, _b, f) { f.shields.push({ amount: f.maxHp * 0.2, remaining: 999, source: f.uid }); u(f).robo = 1; },
      passo(m, b, f) { if (u(f).robo === 1 && !f.shields.some((s) => s.remaining > 100)) { u(f).robo = 2; m.aviso(b, f, 'O robô quebrou!', f); } },
      causa: (_m, _b, f) => (u(f).robo === 2 ? 1.1 : 1),
    },
  },
  zenitsu: {
    nome: 'Luta dormindo',
    texto: 'Abaixo de 65% da Vida: causa 60% a mais e não fica Dormindo nem Confuso.',
    ganchos: {
      imune: (f, s) => (u(f).desmaio ?? 0) > 0 && (s === 'sleep' || s === 'confused'),
      apanhou(m, b, f) { if (!u(f).desmaio && fracao(f) < 0.65) { u(f).desmaio = 1; m.aviso(b, f, 'Zzz… Primeira postura', f); } },
      causa: (_m, _b, f) => (u(f).desmaio ? 1.6 : 1),
    },
  },
  loid: {
    nome: 'Operação Strix',
    texto: 'Começa com 20 de Carga em todas as habilidades.',
    ganchos: { inicio(_m, _b, f) { for (const s of f.skills) s.charge = 20; } },
  },
  pain: {
    nome: 'Empurrão universal',
    texto: 'A cada 15 s: todos os rivais perdem o Preparo e levam 50 de dano.',
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
    texto: 'Abaixo de 50% da Vida, cura 2% por segundo até gastar 600.',
    ganchos: {
      inicio(_m, _b, f) { u(f).necro = 600; },
      passo(m, b, f, dt) {
        if (fracao(f) >= 0.5 || (u(f).necro ?? 0) <= 0) return;
        const c = Math.min(u(f).necro!, f.maxHp * 0.02 * dt);
        u(f).necro! -= c;
        m.cura(b, f, f, c, 'Necroplasma');
      },
    },
  },
  heman: {
    nome: 'Poder de Grayskull',
    texto: 'A cada 20 s: Fortalecido 40% e Protegido 20% por 5 s.',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'forca', dt, 20, 10)) { m.efeitos(b, f, [f], [st('strengthened', 0.4, 5), st('protected', 0.2, 5)]); m.aviso(b, f, 'Eu tenho a força!', f); } } },
  },
  shera: {
    nome: 'Espada que muda',
    texto: 'Cada habilidade alterna: 80 de Escudo, rival mais forte Preso 2 s, ou a próxima habilidade causa 50% a mais.',
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
    texto: 'A cada 15 s, por 2 s, os ataques básicos dos rivais não o acertam.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'asas', dt, 15, 8)) { u(f).voo = b.time + 2; m.aviso(b, f, 'Ao infinito e além!', f); } },
      recebe: (_m, b, f, _fonte, g) => ((u(f).voo ?? 0) > b.time && g.direto && !g.habilidade ? 0 : 1),
    },
  },
  pantera: {
    nome: 'O roubo do diamante',
    texto: 'A cada 15 s, tira Escudo e Barreira do rival mais forte e dá ao aliado mais ferido.',
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
    texto: 'A cada 15 s, rouba 25 de Carga da habilidade mais cheia de um rival.',
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
    texto: 'A cada 20 s, todos os rivais ficam Lento 40% por 3 s.',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'adaga', dt, 20, 10)) { m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.4, 3)]); m.aviso(b, f, 'Areias do Tempo', f); } } },
  },
  trunks: {
    nome: 'Viagem no tempo',
    texto: 'Aos 40 s (uma vez), se o trio tiver menos Vida que os rivais: o trio cura 20%.',
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
    texto: 'A cada 12 s, todos os rivais ficam Queimando (12 por s, 4 s).',
    ganchos: { passo(m, b, f, dt) { if (relogio(f, 'dragao', dt, 12, 7)) { m.efeitos(b, f, m.rivais(b, f), [st('burning', 12, 4)]); m.aviso(b, f, 'Dragão do Oeste', f); } } },
  },
  splinter: {
    nome: 'Contra-golpe do mestre',
    texto: '1 em 3 golpes diretos que leva: devolve 50 e deixa quem bateu Exposto 10% por 3 s.',
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
    texto: 'Aos 30 s, lança a Genki Dama no rival mais forte: 40 de dano por lutador de pé.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).genki || b.time < 30) return;
        u(f).genki = 1;
        const a = maisForte(m, b, f);
        if (!a) return;
        const n = b.fighters.filter(vivo).length;
        m.aviso(b, f, 'Genki Dama!', a, n);
        m.dano(b, f, a, 40 * n, false, 'Genki Dama');
      },
    },
  },
  sasuke: {
    nome: 'Olho que aprende',
    texto: 'Depois de levar uma habilidade de um rival, desvia dela sempre que vier de novo.',
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
    texto: '1 em 8 golpes diretos causa o dobro. Depois de um, vira 1 em 5 por 8 s.',
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
    texto: 'A cada 10 s: 25 de dano no rival mais forte e Alucard cura 25.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'familiar', dt, 10, 6)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        m.dano(b, f, a, 25, false, 'Familiar');
        m.cura(b, f, f, 25, 'Familiar');
      },
    },
  },
  ironman: {
    nome: 'Reator do Unibeam',
    texto: 'Cada habilidade do trio carrega 15%. Cheio: 200 de dano no rival mais forte.',
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
    texto: 'O aliado mais fraco causa 15% a mais e recebe 15% a menos.',
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
    texto: 'Tem 20% de Esquiva. Cada vez que desvia, ganha 40% de ação.',
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
