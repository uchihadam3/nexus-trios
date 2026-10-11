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
    texto: 'O traje só funciona no frio: se nenhum rival está Lento ou Congelado, ele perde 1% da Vida por segundo. Com algum rival gelado, recebe 25% menos dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0 || m.intensidade(r, 'frozen') > 0)) f.hp = Math.max(1, f.hp - f.maxHp * 0.01 * dt);
      },
      recebe: (m, b, f) => (m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0 || m.intensidade(r, 'frozen') > 0) ? 0.75 : 1),
    },
  },
  poisonivy: {
    nome: 'Mãe das plantas',
    texto: 'Nunca fica Envenenada. Todo Veneno nos rivais alimenta o jardim dela: Ivy cura 30% do dano que o Veneno causa.',
    ganchos: {
      imune: (_f, s) => s === 'poison',
      viu(m, b, f, _fonte, alvo, dano, g) { if (alvo.side !== f.side && g.label === 'Veneno') m.cura(b, f, f, dano * 0.3, 'Jardim'); },
    },
  },
  scarecrow: {
    nome: 'Medo',
    texto: 'Quem ele acerta fica com medo por 6 s: causa 25% menos dano nele e no trio dele.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) { if (g.direto) u(f)[`medo${idx(b, alvo)}`] = b.time + 6; },
      recebe: (_m, b, f, fonte) => ((u(f)[`medo${idx(b, fonte)}`] ?? 0) > b.time ? 0.75 : 1),
      recebeAliado: (_m, b, f, _aliado, fonte) => ((u(f)[`medo${idx(b, fonte)}`] ?? 0) > b.time ? 0.75 : 1),
    },
  },
  catwoman: {
    nome: 'Ladra de joias',
    texto: 'Cada golpe dela rouba até 40 do Escudo do alvo e põe o que roubou nela.',
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
    nome: 'Ataque em dupla',
    texto: 'Quando um aliado acerta um rival, Robin entra junto com 30 de dano no mesmo rival (no máximo a cada 2 s).',
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
    texto: 'Os golpes dele desequilibram: cada golpe direto atrasa em 0,4 s a habilidade que o alvo está preparando.',
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
    texto: 'Quem o acerta com um golpe direto fica Lento 10% por 2 s: tocar nele congela a mão.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte)) m.efeitos(b, f, [fonte], [st('slow', 0.1, 2)]); } },
  },
  blackwidow: {
    nome: 'Infiltrada',
    texto: 'Começa disfarçada: até dar o primeiro golpe, não leva dano direto. O primeiro golpe dela causa o dobro.',
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
    texto: 'Cada ataque básico usa a próxima flecha da aljava, em ciclo: explosiva (+60 de dano), elétrica (Eletrificado), de rede (Enraizado 1,5 s) e sônica (Silenciado 1 s).',
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
    texto: 'Pega o rival no contrapé: causa 35% a mais em quem está preparando uma habilidade.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.cast ? 1.35 : 1) },
  },
  spiderwoman: {
    nome: 'Encanto',
    texto: 'O último rival que ela acertou fica encantado: 1 em 4 golpes dele no trio dela não sai.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) { if (g.direto) u(f).encantado = idx(b, alvo); },
      recebe: (m, b, f, fonte, g) => (g.direto && u(f).encantado === idx(b, fonte) && m.sorte(b) < 0.25 ? 0 : 1),
      recebeAliado: (m, b, f, _aliado, fonte, g) => (g.direto && u(f).encantado === idx(b, fonte) && m.sorte(b) < 0.25 ? 0 : 1),
    },
  },

  /* ───────── Desenhos ───────── */
  jake: {
    nome: 'Estica e protege',
    texto: 'Com mais de metade da Vida, Jake se estica na frente dos aliados: eles levam 30% menos de cada golpe, e Jake leva essa parte no lugar.',
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
    nome: 'Sede de vermelho',
    texto: 'A cada 8 s, suga o vermelho do rival mais ferido: tira 6% da Vida máxima dele e cura esse tanto em si.',
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
    texto: 'No começo e a cada 20 s, dá um Coração a si e ao aliado mais ferido: o próximo golpe acima de 100 de dano que eles levariam vira só 100.',
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
    texto: 'Medroso: causa 10% a menos. Mas quando um aliado cai, o medo vira coragem: Acelerado 25% e 50% a mais de dano por 8 s.',
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
    texto: 'Tropeça na hora certa: 1 em 4 golpes que o derrubariam passa por cima da cabeça dele.',
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
    texto: 'Cada golpe dela num rival é uma pista. Com 5 pistas no mesmo rival, ela tira a máscara: ele perde todos os buffs e fica Exposto 25% por 8 s.',
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
    texto: 'A cada 15 s monta uma armadilha: o próximo rival que acertar um aliado dele cai nela — Enraizado 3 s e 80 de dano.',
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
    nome: 'Diário 3',
    texto: 'No começo da luta, procura o rival mais forte no diário. A primeira habilidade dele nesse rival acerta o ponto fraco: causa o triplo.',
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
    texto: 'A cada 12 s, espalha alegria: tira um debuff de cada aliado e cura 3% da Vida de todos.',
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
    texto: 'A cada 4 ataques básicos, já ataca de novo na mesma hora.',
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
    texto: 'A cada 18 s, protege o trio com um campo de força (Barreira em todos) e some por 3 s: nesse tempo não leva dano direto.',
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
    texto: 'A cada 15 s, vira os buffs do rival mais forte do avesso: Fortalecido vira Enfraquecido, Acelerado vira Lento, Protegido vira Exposto, Regeneração vira Veneno…',
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
    nome: 'Descansar',
    texto: 'Ao ficar abaixo de 30% de Vida pela primeira vez, dorme 4 s: não age e recebe metade do dano. Acorda com 60% da Vida.',
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
    nome: 'Debaixo da pedra',
    texto: 'Cabeça vazia: nunca fica Confuso nem Silenciado. A cada 15 s se esconde debaixo da pedra por 2 s: não age e não leva dano.',
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
    texto: 'Golpes normais atravessam o corpo dele: 1 em 3 ataques básicos não pega. E quem acerta Gengar fica Amaldiçoado por 2 s.',
    ganchos: {
      recebe: (m, b, _f, _fonte, g) => (g.direto && !g.habilidade && m.sorte(b) < 1 / 3 ? 0 : 1),
      apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte)) m.efeitos(b, f, [fonte], [st('cursed', 0.3, 2)]); },
    },
  },
  deidara: {
    nome: 'Katsu!',
    texto: 'A arte é uma explosão: quando Deidara cai, ele explode junto e causa 300 de dano em todos os rivais.',
    ganchos: {
      morreu(m, b, f) {
        m.aviso(b, f, 'Katsu!', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 300, false, 'Katsu');
      },
    },
  },
  orihime: {
    nome: 'Rejeitar o acontecido',
    texto: 'As curas dela desfazem o que aconteceu: além de curar, tiram todos os debuffs de quem ela cura.',
    ganchos: {
      curaFeita(_m, _b, _f, alvo) {
        alvo.statuses = alvo.statuses.filter((x) => !NEGATIVOS.includes(x.id));
        return 1;
      },
    },
  },
  kurama: {
    nome: 'Semente da morte',
    texto: 'Quem acerta Kurama leva uma semente. 8 s depois ela brota: 120 de dano e Enraizado por 2 s.',
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
    nome: 'Rumble Ball',
    texto: 'A cada 20 s come uma Rumble Ball e muda de forma por 6 s, em ciclo: Heavy Point (causa 30% a mais), Guard Point (Protegido 40%) e Kung Fu Point (age 40% mais rápido).',
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
    texto: 'Cada habilidade dele aumenta a suspeita sobre o rival mais forte (25 por vez). Em 100, L tem certeza: o trio todo causa 30% a mais nesse rival. Contra Light, a suspeita sobe o dobro.',
    ganchos: {
      usou(m, b, f) {
        const s = u(f);
        if (s.certeza !== undefined) return;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        s.suspeito = idx(b, alvo);
        s.suspeita = (s.suspeita ?? 0) + (alvo.characterId === 'light' ? 50 : 25);
        if (s.suspeita >= 100) { s.certeza = s.suspeito; m.aviso(b, f, 'É ele.', alvo); }
        else m.aviso(b, f, `Suspeita ${s.suspeita}%`, alvo, s.suspeita);
      },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).certeza !== undefined && u(f).certeza === idx(b, alvo) ? 1.3 : 1),
    },
  },
  byakuya: {
    nome: 'Mil lâminas',
    texto: 'Depois de cada habilidade, as pétalas da Senbonzakura continuam cortando: 10 cortes de 12 em rivais aleatórios ao longo de 3 s.',
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
    nome: 'Devil Bringer',
    texto: 'A cada 10 s, o braço do diabo agarra o rival que está preparando a habilidade mais longa e puxa: a preparação é cancelada.',
    ganchos: {
      passo(m, b, f) {
        if ((u(f).braco ?? 0) > b.time) return;
        const alvo = m.rivais(b, f).filter((r) => r.cast && r.cast.duration > 1).sort((x, y) => y.cast!.duration - x.cast!.duration)[0];
        if (!alvo) return;
        u(f).braco = b.time + 10;
        alvo.cast = null;
        m.aviso(b, f, 'Puxado!', alvo);
      },
    },
  },

  /* ───────── Luta ───────── */
  kitana: {
    nome: 'Leque que levanta',
    texto: 'A cada 4 golpes diretos, o leque joga o rival para o alto: ele fica Paralisado por 1 s.',
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
    texto: 'Grande demais para cair com tapa: ataques básicos nunca o derrubam (só habilidades e efeitos).',
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
    texto: 'A cada 10 s grita: todo rival com menos Vida que ele fica Enfraquecido 20% por 4 s.',
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
    texto: 'Mishima não tem pena: o rival que ele acertar abaixo de 12% de Vida é jogado do penhasco e cai na hora.',
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
    texto: 'No começo da luta, leva o aliado mais lento voando: enquanto Tails estiver de pé, os dois agem 20% mais rápido.',
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
    texto: 'Quanto mais tempo sem bater, mais forte o próximo soco: 10% a mais por segundo parado, até 60%.',
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
    texto: 'Enquanto ele está de pé, todos os rivais perdem 0,4% da Vida por segundo. A radiação cresce quando ele apanha: até 1,2% com pouca Vida.',
    ganchos: {
      passo(m, b, f, dt) {
        const taxa = 0.004 + 0.008 * (1 - fracao(f));
        for (const r of m.rivais(b, f)) m.dano(b, f, r, r.maxHp * taxa * dt, false, 'Radiação');
      },
    },
  },
};
