/*
 * Mecânicas únicas — lote 2: Gotham e Marvel de rua, desenhos, anime e
 * games. Cada uma é a cara do personagem e não se repete em nenhum outro.
 */
import { fracao, maisFerido, maisForte, relogio, st, u, vivo, type Unica } from './unicas-base';
import { byId } from '../data/characters';
import type { Battle, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const NEGATIVOS: StatusId[] = ['paralyzed', 'frozen', 'sleep', 'silenced', 'rooted', 'provoked', 'confused', 'blind', 'poison', 'bleed', 'cursed', 'slow', 'burning', 'exposed', 'marked', 'electric', 'weakened', 'bomb'];
/** O contrário de cada buff (o feitiço da Gwen). */
const INVERSO: Partial<Record<StatusId, StatusId>> = { strengthened: 'weakened', haste: 'slow', protected: 'exposed', regen: 'poison', evasion: 'blind', vampirism: 'cursed', barrier: 'silenced' };

export const LOTE2: Record<string, Unica> = {
  /* ───────── Gotham ───────── */
  mrfreeze: {
    nome: 'Coração de gelo',
    texto: 'Se nenhum rival estiver Lento ou Congelado, o Senhor Frio perde 1% da Vida máxima por segundo (sem cair por isso). Se algum rival estiver Lento ou Congelado, o Senhor Frio recebe −25% de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0 || m.intensidade(r, 'frozen') > 0)) f.hp = Math.max(1, f.hp - f.maxHp * 0.01 * dt);
      },
      recebe: (m, b, f) => (m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0 || m.intensidade(r, 'frozen') > 0) ? 0.75 : 1),
    },
  },
  poisonivy: {
    nome: 'Mãe das plantas',
    texto: 'Hera Venenosa nunca fica Envenenado. Hera cura 30% de todo dano que Envenenado causa nos rivais.',
    ganchos: {
      imune: (_f, s) => s === 'poison',
      viu(m, b, f, _fonte, alvo, dano, g) { if (alvo.side !== f.side && g.label === 'Veneno') m.cura(b, f, f, dano * 0.3, 'Jardim'); },
    },
  },
  scarecrow: {
    nome: 'Medo',
    texto: 'Por 6 s depois de levar um golpe do Espantalho, o rival causa −25% de dano no Espantalho e no trio do Espantalho.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) { if (g.direto) u(f)[`medo${idx(b, alvo)}`] = b.time + 6; },
      recebe: (_m, b, f, fonte) => ((u(f)[`medo${idx(b, fonte)}`] ?? 0) > b.time ? 0.75 : 1),
      recebeAliado: (_m, b, f, _aliado, fonte) => ((u(f)[`medo${idx(b, fonte)}`] ?? 0) > b.time ? 0.75 : 1),
    },
  },
  catwoman: {
    nome: 'Ladra de joias',
    texto: 'Cada golpe da Mulher-Gato rouba até 40 de Escudo do alvo, e a Mulher-Gato fica com esse Escudo por 10 s.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !alvo.shields.length) return;
        let falta = 40, roubado = 0;
        for (const s of alvo.shields) { const t = Math.min(s.amount, falta); s.amount -= t; falta -= t; roubado += t; }
        alvo.shields = alvo.shields.filter((s) => s.amount > 0.01);
        if (roubado < 1) return;
        f.shields.push({ amount: roubado, remaining: 10, source: f.uid });
        m.aviso(b, f, `Roubou ${Math.round(roubado)} de Escudo`, alvo, roubado);
      },
    },
  },
  robin: {
    nome: 'Sempre junto',
    texto: 'Quando um aliado de Robin acerta um rival com ataque ou habilidade, Robin causa mais 30 de dano nesse rival (no máximo 1 vez a cada 2 s).',
    ganchos: {
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (fonte === f || fonte.side !== f.side || alvo.side === f.side || !g.direto || !vivo(alvo)) return;
        if ((u(f).dupla ?? 0) > b.time) return;
        u(f).dupla = b.time + 2;
        m.dano(b, f, alvo, 30, false, 'Ataque em dupla');
      },
    },
  },
  nightwing: {
    nome: 'Ritmo de trapezista',
    texto: 'Cada golpe do Asa Noturna atrasa em 0,4 s o Preparo do alvo.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !alvo.cast) return;
        alvo.cast.elapsed = Math.max(-1, alvo.cast.elapsed - 0.4);
        m.aviso(b, f, 'Desequilibrou', alvo);
      },
    },
  },

  /* ───────── Marvel ───────── */
  iceman: {
    nome: 'Pele de gelo',
    texto: 'Quem acerta o Homem de Gelo com ataque ou habilidade fica Lento (10% mais lento) por 2 s.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte)) m.efeitos(b, f, [fonte], [st('slow', 0.1, 2)]); } },
  },
  blackwidow: {
    nome: 'Infiltrada',
    texto: 'A Viúva Negra não recebe dano de ataques nem de habilidades até dar o primeiro golpe, e esse primeiro golpe causa o dobro de dano.',
    ganchos: {
      inicio(m, b, f) { m.aviso(b, f, 'Disfarçada', f); },
      recebe: (_m, _b, f, _fonte, g) => (g.direto && !u(f).revelada ? 0 : 1),
      causa(m, b, f, alvo, g) {
        if (!g.direto || u(f).revelada) return 1;
        u(f).revelada = 1;
        m.aviso(b, f, 'Disfarce caiu', alvo);
        return 2;
      },
    },
  },
  hawkeye: {
    nome: 'Aljava de truques',
    texto: 'O ataque básico do Gavião Arqueiro alterna 4 flechas, nesta ordem: +60 de dano; Eletrificado (−18% da barra por golpe) por 4 s; Preso (65% mais lento) por 1,5 s; Silenciado por 1 s.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || g.habilidade || !vivo(alvo)) return;
        const s = u(f), k = (s.flecha ?? 0) % 4;
        s.flecha = k + 1;
        if (k === 0) m.dano(b, f, alvo, 60, false, 'Flecha explosiva');
        else if (k === 1) m.efeitos(b, f, [alvo], [st('electric', 0.3, 4)]);
        else if (k === 2) m.efeitos(b, f, [alvo], [st('rooted', 1, 1.5)]);
        else m.efeitos(b, f, [alvo], [st('silenced', 1, 1)]);
      },
    },
  },
  gamora: {
    nome: 'A mais perigosa da galáxia',
    texto: 'Gamora causa +35% de dano em rivais que estão em Preparo.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.cast ? 1.35 : 1) },
  },
  spiderwoman: {
    nome: 'Encanto',
    texto: 'O último rival que a Mulher-Aranha acertou fica encantado: cada golpe desse rival no trio da Mulher-Aranha tem 25% de chance de não causar dano.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) { if (g.direto) u(f).encantado = idx(b, alvo); },
      recebe: (m, b, f, fonte, g) => (g.direto && u(f).encantado === idx(b, fonte) && m.sorte(b) < 0.25 ? 0 : 1),
      recebeAliado: (m, b, f, _aliado, fonte, g) => (g.direto && u(f).encantado === idx(b, fonte) && m.sorte(b) < 0.25 ? 0 : 1),
    },
  },

  /* ───────── Desenhos ───────── */
  jake: {
    nome: 'Estica e protege',
    texto: 'Com mais de 50% da Vida, Jake estica e protege o trio: os aliados de Jake recebem −30% de dano, e Jake leva essa parte no lugar deles.',
    ganchos: {
      recebeAliado(m, b, f, aliado, fonte, g) {
        if (aliado === f || fracao(f) <= 0.5 || g.label === 'Esticou') return 1;
        u(f).esticar = 1;
        void fonte; void m; void b;
        return 0.7;
      },
      viu(m, b, f, fonte, alvo, dano, g) {
        if (!u(f).esticar || alvo === f || alvo.side !== f.side || g.label === 'Esticou') return;
        u(f).esticar = 0;
        m.dano(b, fonte, f, (dano * 0.3) / 0.7, false, 'Esticou');
      },
    },
  },
  marceline: {
    nome: 'Rainha vampira',
    texto: 'A cada 8 s, Marceline suga o rival mais ferido: esse rival perde 6% da Vida máxima, e Marceline cura esse mesmo tanto.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'vermelho', dt, 8, 6)) return;
        const alvo = m.rivais(b, f).sort((x, y) => fracao(x) - fracao(y))[0];
        if (!alvo) return;
        const v = alvo.maxHp * 0.06;
        m.aviso(b, f, 'Sugou o vermelho', alvo);
        m.dano(b, f, alvo, v, false, 'Sede de vermelho');
        m.cura(b, f, f, v, 'Sede de vermelho');
      },
    },
  },
  peach: {
    nome: 'Coração de princesa',
    texto: 'A cada 20 s, a Princesa Peach dá um Coração para si mesma e para o aliado mais ferido: o próximo golpe acima de 100 de dano em quem tem o Coração causa só 100.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'coracao', dt, 20, 0.1)) return;
        const outro = maisFerido(m, b, f);
        u(f)[`cor${idx(b, f)}`] = 1;
        if (outro) u(f)[`cor${idx(b, outro)}`] = 1;
        m.aviso(b, f, 'Corações', outro ?? f);
      },
      limita(m, b, f, alvo, valor) {
        const k = `cor${idx(b, alvo)}`;
        if (!u(f)[k] || valor <= 100) return valor;
        u(f)[k] = 0;
        m.aviso(b, f, 'O Coração segurou', alvo);
        return 100;
      },
    },
  },
  luigi: {
    nome: 'Coragem de irmão',
    texto: 'Luigi causa −10% de dano. Quando um aliado cai, Luigi ganha coragem por 8 s: +50% de dano e Acelerado (25% mais rápido).',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side) return;
        u(f).coragem = b.time + 8;
        m.efeitos(b, f, [f], [st('haste', 0.25, 8)]);
        m.aviso(b, f, 'Coragem!', f);
      },
      causa: (_m, b, f) => ((u(f).coragem ?? 0) > b.time ? 1.5 : 0.9),
    },
  },
  morty: {
    nome: 'Sorte de principiante',
    texto: 'Cada golpe que derrubaria Morty Smith tem 25% de chance de não causar dano.',
    ganchos: {
      salva(m, b, f, alvo, _dano, fonte) {
        if (alvo !== f || m.sorte(b) >= 0.25) return null;
        m.aviso(b, f, 'Tropeçou!', fonte);
        return f.hp;
      },
    },
  },
  velma: {
    nome: 'Desmascarar',
    texto: 'A cada 5 golpes de Velma Dinkley no mesmo rival: esse rival perde todos os Status bons e fica Exposto (+25% de dano recebido) por 8 s.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const k = `pista${idx(b, alvo)}`, s = u(f);
        s[k] = (s[k] ?? 0) + 1;
        if (s[k]! < 5) return;
        s[k] = 0;
        alvo.statuses = alvo.statuses.filter((x) => NEGATIVOS.includes(x.id));
        m.efeitos(b, f, [alvo], [st('exposed', 0.25, 8)]);
        m.aviso(b, f, 'Desmascarado!', alvo);
      },
    },
  },
  fred: {
    nome: 'Armadilha montada',
    texto: 'A cada 15 s, Fred Jones monta uma armadilha: o próximo rival que acertar alguém do trio de Fred com ataque ou habilidade fica Preso (65% mais lento) por 3 s e leva 80 de dano.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'armadilha', dt, 15, 8) && !u(f).armada) { u(f).armada = 1; m.aviso(b, f, 'Armadilha pronta', f); } },
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (!u(f).armada || !g.direto || alvo.side !== f.side || fonte.side === f.side || !vivo(fonte)) return;
        u(f).armada = 0;
        m.aviso(b, f, 'Pegamos você!', fonte);
        m.efeitos(b, f, [fonte], [st('rooted', 1, 3)]);
        m.dano(b, f, fonte, 80, false, 'Armadilha');
      },
    },
  },
  dipper: {
    nome: 'Pesquisa paranormal',
    texto: 'No começo da luta, Dipper Pines anota no diário o rival com mais Vida. A primeira habilidade de Dipper que acertar esse rival causa o triplo de dano.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).diario = idx(b, a); m.aviso(b, f, 'Está no diário', a); } },
      causa(_m, b, f, alvo, g) {
        if (!g.habilidade || u(f).usado || u(f).diario !== idx(b, alvo)) return 1;
        u(f).achou = 1;
        return 3;
      },
      usou(_m, _b, f) { if (u(f).achou) u(f).usado = 1; },
    },
  },
  mabel: {
    nome: 'Alegria contagiante',
    texto: 'A cada 12 s, Mabel Pines tira 1 Status ruim de cada membro do trio e cura todos em 3% da Vida máxima.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'alegria', dt, 12, 8)) return;
        for (const a of m.aliados(b, f)) {
          const ruim = a.statuses.find((x) => NEGATIVOS.includes(x.id));
          if (ruim) a.statuses = a.statuses.filter((x) => x !== ruim);
          m.cura(b, f, a, a.maxHp * 0.03, 'Alegria');
        }
        m.aviso(b, f, 'Alegria!', f);
      },
    },
  },
  dash: {
    nome: 'Rápido demais',
    texto: 'A cada 4 ataques básicos, Flecha Pêra ataca de novo na hora.',
    ganchos: {
      bateu(_m, _b, f, _alvo, _dano, g) {
        if (!g.direto || g.habilidade) return;
        u(f).golpes = (u(f).golpes ?? 0) + 1;
        if (u(f).golpes! % 4 === 0) f.action = 1;
      },
    },
  },
  violet: {
    nome: 'Sumir',
    texto: 'A cada 18 s, Violeta Pêra dá Barreira (anula 1 debuff) por 6 s a todo o trio e some: por 3 s, Violeta não recebe dano de ataques nem de habilidades.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'campo', dt, 18, 10)) return;
        m.efeitos(b, f, m.aliados(b, f), [st('barrier', 1, 6)]);
        u(f).sumiu = b.time + 3;
        m.aviso(b, f, 'Sumiu', f);
      },
      recebe: (_m, b, f, _fonte, g) => (g.direto && (u(f).sumiu ?? 0) > b.time ? 0 : 1),
    },
  },
  gwen: {
    nome: 'Feitiço de inversão',
    texto: 'A cada 15 s, Gwen Tennyson inverte os Status bons de um rival: Fortalecido vira Enfraquecido, Acelerado vira Lento, Protegido vira Exposto, Regeneração vira Envenenado, Esquiva vira Cego, Vampirismo vira Amaldiçoado e Barreira vira Silenciado (cada um com no máximo 40% de força).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'inverte', dt, 15, 9)) return;
        const alvo = m.rivais(b, f).find((r) => r.statuses.some((s) => INVERSO[s.id])) ?? maisForte(m, b, f);
        if (!alvo) return;
        const troca = alvo.statuses.filter((s) => INVERSO[s.id]);
        if (!troca.length) return;
        alvo.statuses = alvo.statuses.filter((s) => !INVERSO[s.id]);
        m.efeitos(b, f, [alvo], troca.map((s) => st(INVERSO[s.id]!, s.id === 'regen' ? s.intensity : Math.min(0.4, s.intensity), Math.max(2, s.remaining))));
        m.aviso(b, f, 'Invertido!', alvo);
      },
    },
  },
  snorlax: {
    nome: 'Soneca pesada',
    texto: 'Com 30% da Vida ou menos (1 vez por luta): Snorlax dorme 4 s parado, recebendo metade do dano, e acorda com pelo menos 60% da Vida.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).dormiu || fracao(f) > 0.3) return;
        u(f).dormiu = 1; u(f).sono = b.time + 4;
        m.aviso(b, f, 'Zzz…', f);
      },
      parado: (f, b) => (u(f).sono ?? 0) > b.time,
      recebe: (_m, b, f) => ((u(f).sono ?? 0) > b.time ? 0.5 : 1),
      passo(m, b, f) {
        if (!u(f).sono || u(f).acordou || b.time < u(f).sono!) return;
        u(f).acordou = 1;
        if (f.hp < f.maxHp * 0.6) m.cura(b, f, f, f.maxHp * 0.6 - f.hp, 'Descansar');
        m.aviso(b, f, 'Acordou', f);
      },
    },
  },
  patrick: {
    nome: 'Esconderijo',
    texto: 'Patrick Estrela nunca fica Confuso nem Silenciado. A cada 15 s, Patrick se esconde debaixo da pedra por 2 s: não age e não recebe dano.',
    ganchos: {
      imune: (_f, s) => s === 'confused' || s === 'silenced',
      passo(m, b, f, dt) { if (relogio(f, 'pedra', dt, 15, 10)) { u(f).pedra = b.time + 2; m.aviso(b, f, 'Debaixo da pedra', f); } },
      parado: (f, b) => (u(f).pedra ?? 0) > b.time,
      recebe: (_m, b, f) => ((u(f).pedra ?? 0) > b.time ? 0 : 1),
    },
  },

  /* ───────── Anime ───────── */
  gengar: {
    nome: 'Tipo fantasma',
    texto: 'Cada ataque básico em Gengar tem 33% de chance de não causar dano. Quem acerta Gengar com ataque ou habilidade fica Amaldiçoado (−30% de cura recebida) por 2 s.',
    ganchos: {
      recebe: (m, b, _f, _fonte, g) => (g.direto && !g.habilidade && m.sorte(b) < 1 / 3 ? 0 : 1),
      apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte)) m.efeitos(b, f, [fonte], [st('cursed', 0.3, 2)]); },
    },
  },
  deidara: {
    nome: 'Katsu!',
    texto: 'Quando Deidara cai, explode: 300 de dano em cada rival.',
    ganchos: {
      morreu(m, b, f) {
        m.aviso(b, f, 'Katsu!', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 300, false, 'Katsu');
      },
    },
  },
  orihime: {
    nome: 'Rejeitar o acontecido',
    texto: 'Quem Orihime Inoue cura também perde todos os Status ruins.',
    ganchos: {
      curaFeita(_m, _b, _f, alvo) {
        alvo.statuses = alvo.statuses.filter((x) => !NEGATIVOS.includes(x.id));
        return 1;
      },
    },
  },
  kurama: {
    nome: 'Planta que espera',
    texto: 'Quem acerta Kurama com ataque ou habilidade recebe uma semente: 8 s depois, a semente brota, causa 120 de dano e deixa esse rival Preso (65% mais lento) por 2 s. Cada rival carrega só 1 semente por vez.',
    ganchos: {
      apanhou(_m, b, f, fonte, _dano, g) {
        if (!g.direto || fonte.side === f.side || u(f)[`semente${idx(b, fonte)}`]) return;
        u(f)[`semente${idx(b, fonte)}`] = b.time + 8;
      },
      passo(m, b, f) {
        for (const r of m.rivais(b, f)) {
          const k = `semente${idx(b, r)}`, quando = u(f)[k];
          if (!quando || b.time < quando) continue;
          u(f)[k] = 0;
          m.aviso(b, f, 'A semente brotou', r);
          m.efeitos(b, f, [r], [st('rooted', 1, 2)]);
          m.dano(b, f, r, 120, false, 'Semente da morte');
        }
      },
    },
  },
  chopper: {
    nome: 'Sete formas',
    texto: 'A cada 20 s, Tony Tony Chopper come uma Rumble Ball e muda de forma por 6 s, nesta ordem: Heavy Point (+30% de dano), Guard Point (Protegido: −40% de dano recebido) e Kung Fu Point (age 40% mais rápido).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'bola', dt, 20, 12)) return;
        const s = u(f), forma = (s.forma ?? 0) % 3;
        s.forma = forma + 1; s.ate = b.time + 6; s.atual = forma;
        if (forma === 1) m.efeitos(b, f, [f], [st('protected', 0.4, 6)]);
        m.aviso(b, f, ['Heavy Point', 'Guard Point', 'Kung Fu Point'][forma]!, f);
      },
      causa: (_m, b, f) => ((u(f).ate ?? 0) > b.time && u(f).atual === 0 ? 1.3 : 1),
      ritmo: (_m, b, f) => ((u(f).ate ?? 0) > b.time && u(f).atual === 2 ? 1.4 : 1),
    },
  },
  lawliet: {
    nome: 'Suspeito',
    texto: 'Cada habilidade que L usa aumenta a Suspeita sobre o rival com mais Vida em 35 pontos (70 contra Light), começando em 30. Com 100 de Suspeita, o trio de L causa +35% de dano nesse rival até esse rival cair.',
    ganchos: {
      usou(m, b, f) {
        const s = u(f);
        // o culpado caiu: o caso continua no próximo
        if (s.certeza !== undefined) { if (vivo(b.fighters[s.certeza]!)) return; delete s.certeza; s.suspeita = 50; }
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        s.suspeito = idx(b, alvo);
        s.suspeita = (s.suspeita ?? 30) + (alvo.characterId === 'light' ? 70 : 35);
        if (s.suspeita >= 100) { s.certeza = s.suspeito; m.aviso(b, f, 'É ele.', alvo); }
        else m.aviso(b, f, `Suspeita ${s.suspeita}%`, alvo, s.suspeita);
      },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).certeza !== undefined && u(f).certeza === idx(b, alvo) ? 1.35 : 1),
    },
  },
  byakuya: {
    nome: 'Mil lâminas',
    texto: 'Depois de cada habilidade, Byakuya Kuchiki solta 10 pétalas-lâmina ao longo de 3 s: cada uma causa 12 de dano em um rival aleatório.',
    ganchos: {
      usou(_m, _b, f) { u(f).petalas = (u(f).petalas ?? 0) + 10; },
      passo(m, b, f, dt) {
        const s = u(f);
        if (!s.petalas) return;
        s.tic = (s.tic ?? 0) + dt;
        if (s.tic < 0.3) return;
        s.tic = 0; s.petalas -= 1;
        const rs = m.rivais(b, f);
        if (rs.length) m.dano(b, f, rs[Math.floor(m.sorte(b) * rs.length)]!, 12, false, 'Pétalas');
      },
    },
  },
  nero: {
    nome: 'Braço demoníaco',
    texto: 'A cada 8 s, Nero puxa o rival com o Preparo mais longo (de mais de 1 s): esse rival perde o Preparo e leva 90 de dano. Se ninguém estiver em Preparo, Nero causa 60 de dano no rival com mais Vida.',
    ganchos: {
      passo(m, b, f) {
        if ((u(f).braco ?? 0) > b.time) return;
        const alvo = m.rivais(b, f).filter((r) => r.cast && r.cast.duration > 1).sort((x, y) => y.cast!.duration - x.cast!.duration)[0];
        const forte = alvo ?? maisForte(m, b, f);
        if (!forte) return;
        u(f).braco = b.time + 8;
        if (alvo) alvo.cast = null;
        m.aviso(b, f, 'Puxado!', forte);
        m.dano(b, f, forte, alvo ? 90 : 60, false, 'Devil Bringer');
      },
    },
  },

  /* ───────── Luta ───────── */
  kitana: {
    nome: 'Leque que levanta',
    texto: 'A cada 4 golpes de Kitana, o rival atingido fica Paralisado por 1 s.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        u(f).leque = (u(f).leque ?? 0) + 1;
        if (u(f).leque! % 4 === 0) { m.efeitos(b, f, [alvo], [st('paralyzed', 1, 1)]); m.aviso(b, f, 'Para o alto!', alvo); }
      },
    },
  },
  goro: {
    nome: 'Quatro braços',
    texto: 'Ataques básicos nunca derrubam Goro: o que derrubaria deixa Goro com 1 de Vida. Só habilidades e outros efeitos derrubam Goro.',
    ganchos: {
      salva(m, b, f, alvo, _dano, fonte, g) {
        if (alvo !== f || !g.direto || g.habilidade) return null;
        m.aviso(b, f, 'Não caiu no tapa', fonte);
        return 1;
      },
    },
  },
  shaokahn: {
    nome: 'Você é fraco!',
    texto: 'A cada 10 s, todo rival com menos Vida que Shao Kahn fica Enfraquecido (−20% de dano) por 4 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'grito', dt, 10, 5)) return;
        const fracos = m.rivais(b, f).filter((r) => r.hp < f.hp);
        if (!fracos.length) return;
        m.efeitos(b, f, fracos, [st('weakened', 0.2, 4)]);
        m.aviso(b, f, 'Você é fraco!', f);
      },
    },
  },
  heihachi: {
    nome: 'Jogado do penhasco',
    texto: 'Quando Heihachi Mishima acerta um rival com menos de 12% da Vida, esse rival cai na hora.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo) || fracao(alvo) >= 0.12) return;
        m.aviso(b, f, 'Do penhasco!', alvo);
        m.dano(b, f, alvo, alvo.hp + 1, false, 'Penhasco');
      },
    },
  },

  /* ───────── Games ───────── */
  tails: {
    nome: 'Carona nas caudas',
    texto: 'Tails age 20% mais rápido, e o aliado mais lento do trio (escolhido no começo da luta) também age 20% mais rápido.',
    ganchos: {
      inicio(m, b, f) {
        const outro = m.aliados(b, f).filter((a) => a !== f).sort((x, y) => byId[y.characterId]!.interval - byId[x.characterId]!.interval)[0];
        if (outro) { u(f).carona = idx(b, outro); m.aviso(b, f, 'Carona', outro); }
      },
      ritmo: () => 1.2,
      passo(_m, b, f, dt) {
        const o = b.fighters[u(f).carona ?? -1];
        if (o && vivo(o)) o.action = Math.min(1, o.action + (dt * 0.2) / byId[o.characterId]!.interval);
      },
    },
  },
  knuckles: {
    nome: 'Soco carregado',
    texto: 'Cada segundo que Knuckles passa sem bater soma +10% de dano no próximo golpe (até +60%, com 6 s).',
    ganchos: {
      passo(_m, _b, f, dt) { u(f).carga = Math.min(6, (u(f).carga ?? 0) + dt); },
      causa(_m, _b, f, _alvo, g) {
        if (!g.direto) return 1;
        const k = 1 + 0.1 * (u(f).carga ?? 0);
        u(f).carga = 0;
        return k;
      },
    },
  },
  godzilla: {
    nome: 'Radiação',
    texto: 'Enquanto Godzilla está de pé, cada rival perde 0,4% da Vida máxima por segundo. Quanto menos Vida Godzilla tem, mais a radiação queima: até 1,2% por segundo quando Godzilla está quase caindo.',
    ganchos: {
      passo(m, b, f, dt) {
        const taxa = 0.004 + 0.008 * (1 - fracao(f));
        for (const r of m.rivais(b, f)) m.dano(b, f, r, r.maxHp * taxa * dt, false, 'Radiação');
      },
    },
  },
};
