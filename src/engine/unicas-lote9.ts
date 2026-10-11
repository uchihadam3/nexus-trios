/*
 * Mecânicas únicas — lote 9: os últimos 54 (Kirby, Link, Dante, Sekiro,
 * Coringa, Optimus, Mario…). Com este lote, todo personagem tem a dele.
 */
import { BUFFS, fracao, maisForte, relogio, st, u, vivo, type Ganchos, type Unica } from './unicas-base';
import type { Battle, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const ESTILO = ['D', 'C', 'B', 'A', 'S', 'SS', 'SSS'];
const ATORDOADO: StatusId[] = ['sleep', 'paralyzed', 'confused', 'frozen'];

/* O Kirby copia a mecânica de outro: precisa da lista de todas (unicas.ts entrega, sem import em círculo). */
let TODAS: Record<string, Unica> = {};
export const conheceTodas = (t: Record<string, Unica>) => { TODAS = t; };
const copiada = (b: Battle, f: Fighter): Ganchos | undefined => {
  const c = b.fighters[u(f).copia ?? -1];
  return c && c.characterId !== 'kirby' ? TODAS[c.characterId]?.ganchos : undefined;
};

export const LOTE9: Record<string, Unica> = {
  starlord: {
    nome: 'Doze por cento de um plano',
    texto: 'O trio tem 12% de um plano: enquanto Quill está de pé, 12% dos golpes de habilidade do trio saem perfeitos, com 60% a mais.',
    ganchos: { causaAliado: (m, b, _f, _aliado, _alvo, g) => (g.habilidade && g.direto && m.sorte(b) < 0.12 ? 1.6 : 1) },
  },
  groot: {
    nome: 'Galhos que protegem',
    texto: 'Cada vez que Groot perde mais 25% da Vida, uma lasca dele vira armadura no aliado mais ferido: Escudo de 8% da Vida máxima de Groot.',
    ganchos: {
      apanhou(m, b, f) {
        for (const lim of [0.75, 0.5, 0.25]) {
          const k = `lasca${lim * 100}`;
          if (u(f)[k] || fracao(f) >= lim) continue;
          u(f)[k] = 1;
          const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => fracao(x) - fracao(y))[0];
          if (a) { m.aviso(b, f, 'Eu sou Groot', a); a.shields.push({ amount: f.maxHp * 0.08, remaining: 12, source: f.uid }); }
        }
      },
    },
  },
  greenlantern: {
    nome: 'Bateria do anel',
    texto: 'O anel começa com 100% de carga e cada habilidade gasta 20%. Com carga, causa 15% a mais. Sem carga, para 3 s para recarregar no lampião.',
    ganchos: {
      inicio(_m, _b, f) { u(f).anel = 100; },
      usou(m, b, f) {
        u(f).anel = Math.max(0, (u(f).anel ?? 100) - 20);
        if (u(f).anel! < 20) { u(f).recarga = b.time + 3; m.aviso(b, f, 'Recarregando o anel', f); }
      },
      passo(_m, b, f) { if (u(f).recarga && b.time >= u(f).recarga!) { u(f).recarga = 0; u(f).anel = 100; } },
      parado: (f, b) => (u(f).recarga ?? 0) > b.time,
      causa: (_m, _b, f) => ((u(f).anel ?? 100) >= 20 ? 1.15 : 1),
    },
  },
  shazam: {
    nome: 'SHAZAM!',
    texto: 'A cada 15 s grita a palavra mágica e um raio cai: Shazam recupera 6% da Vida e o raio acerta um rival com 40.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'shazam', dt, 15, 7)) return;
        const rs = m.rivais(b, f), r = rs[Math.floor(m.sorte(b) * rs.length)];
        m.aviso(b, f, 'SHAZAM!', f);
        m.cura(b, f, f, f.maxHp * 0.06, 'Raio mágico');
        if (r) m.dano(b, f, r, 40, false, 'Raio mágico');
      },
    },
  },
  link: {
    nome: 'Feixe da Espada Mestra',
    texto: 'Com o coração cheio (90% da Vida ou mais), cada ataque básico solta um feixe da espada que acerta outro rival com 30.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || g.habilidade || fracao(f) < 0.9) return;
        const o = m.rivais(b, f).find((r) => r !== alvo);
        if (o) m.dano(b, f, o, 30, false, 'Feixe da espada');
      },
    },
  },
  dante: {
    nome: 'Estilo',
    texto: 'O estilo sobe a cada golpe direto dele, de D até SSS: 4% a mais de dano por letra. Cada golpe direto que leva derruba 2 letras.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || (u(f).estilo ?? 0) >= 7) return;
        u(f).estilo = (u(f).estilo ?? 0) + 1;
        if (u(f).estilo! >= 5) m.aviso(b, f, ESTILO[u(f).estilo! - 1]!, f);
      },
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).estilo = Math.max(0, (u(f).estilo ?? 0) - 2); },
      causa: (_m, _b, f) => 1 + 0.04 * (u(f).estilo ?? 0),
    },
  },
  bayonetta: {
    nome: 'Witch Time',
    texto: 'A cada 18 s, desvia no último instante do próximo golpe direto e o tempo dos rivais desacelera: todos ficam Lentos 25% por 1,5 s.',
    ganchos: {
      passo(_m, _b, f, dt) { if (relogio(f, 'bruxa', dt, 18, 6)) u(f).bruxa = 1; },
      recebe(m, b, f, _fonte, g) {
        if (!g.direto || !u(f).bruxa) return 1;
        u(f).bruxa = 0;
        m.aviso(b, f, 'Witch Time', f);
        m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.25, 1.5)]);
        return 0;
      },
    },
  },
  masterchief: {
    nome: 'Escudo MJOLNIR',
    texto: 'Começa com Escudo de energia de 6% da Vida. Quando ele quebra, 12 s depois volta inteiro de uma vez.',
    ganchos: {
      inicio(_m, _b, f) { f.shields.push({ amount: f.maxHp * 0.06, remaining: 999, source: f.uid }); },
      passo(m, b, f) {
        if (f.shields.some((s) => s.source === f.uid && s.remaining > 100)) return;
        if (!u(f).volta) { u(f).volta = b.time + 12; return; }
        if (b.time < u(f).volta!) return;
        u(f).volta = 0;
        m.aviso(b, f, 'Escudo recarregado', f);
        f.shields.push({ amount: f.maxHp * 0.06, remaining: 999, source: f.uid });
      },
    },
  },
  snake: {
    nome: 'Tranquilizante',
    texto: 'A arma é de dardos: 1 em 8 golpes diretos dele deixa o alvo Dormindo por 1,2 s.',
    ganchos: { bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && m.sorte(b) < 0.125) { m.aviso(b, f, 'Zzz', alvo); m.efeitos(b, f, [alvo], [st('sleep', 1, 1.2)]); } } },
  },
  lara: {
    nome: 'Armadilha de cabo',
    texto: 'Sempre prepara o terreno: 1 em 3 rivais que a acertam com ataque básico tropeçam no cabo e ficam Enraizados por 1 s.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && !g.habilidade && vivo(fonte) && m.sorte(b) < 1 / 3) m.efeitos(b, f, [fonte], [st('rooted', 1, 1)]); } },
  },
  megaman: {
    nome: 'Arma adquirida',
    texto: 'Cada rival que cai deixa uma arma para ele: Mega Man ganha um poder sorteado até o fim da luta (Fortalecido 15%, Acelerado 15% ou Protegido 15%).',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side === f.side) return;
        const s = (['strengthened', 'haste', 'protected'] as const)[Math.floor(m.sorte(b) * 3)]!;
        m.aviso(b, f, 'Arma adquirida', f);
        m.efeitos(b, f, [f], [st(s, 0.15, 999)]);
      },
    },
  },
  mario: {
    nome: 'Super Cogumelo',
    texto: 'Começa pequeno (15% a menos de Vida máxima). Depois de 5 golpes diretos pega o cogumelo e cresce: +30% de Vida máxima. Um golpe de mais de 15% da Vida o faz encolher de novo.',
    ganchos: {
      inicio(_m, _b, f) { u(f).base = f.maxHp; f.maxHp *= 0.85; f.hp = Math.min(f.hp, f.maxHp); },
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || u(f).grande) return;
        u(f).moedas = (u(f).moedas ?? 0) + 1;
        if (u(f).moedas! < 5) return;
        u(f).grande = 1; u(f).moedas = 0;
        const antes = f.maxHp; f.maxHp = u(f).base! * 1.15; f.hp += f.maxHp - antes;
        m.aviso(b, f, 'Super Cogumelo!', f);
      },
      apanhou(m, b, f, _fonte, dano) {
        if (!u(f).grande || dano <= f.maxHp * 0.15) return;
        u(f).grande = 0;
        f.maxHp = u(f).base! * 0.85; f.hp = Math.min(f.hp, f.maxHp);
        m.aviso(b, f, 'Encolheu', f);
      },
    },
  },
  scorpion: {
    nome: 'Venha cá!',
    texto: 'A cada 12 s, a lança puxa o rival mais perto de agir: a barra de ação dele zera e ele leva 40.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'lanca', dt, 12, 6)) return;
        const r = m.rivais(b, f).sort((x, y) => y.action - x.action)[0];
        if (!r) return;
        m.aviso(b, f, 'Venha cá!', r);
        r.action = 0;
        m.dano(b, f, r, 40, false, 'Lança');
      },
    },
  },
  raidenmk: {
    nome: 'Pele de trovão',
    texto: 'Tocar no deus do trovão dá choque: quem o acerta com um golpe direto leva 8 de dano, e 1 em 2 fica Eletrificado por 1 s.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.direto || !vivo(fonte) || fonte.side === f.side) return;
        m.dano(b, f, fonte, 8, false, 'Choque');
        if (m.sorte(b) < 0.5) m.efeitos(b, f, [fonte], [st('electric', 0.2, 1)]);
      },
    },
  },
  sekiro: {
    nome: 'Postura',
    texto: 'Cada golpe direto enche a postura do rival em 20. Com 100, a postura quebra: o rival fica Paralisado 1,5 s e o próximo golpe do Sekiro nele é um Golpe mortal, com o dobro.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const k = `postura${idx(b, alvo)}`;
        u(f)[k] = (u(f)[k] ?? 0) + 20;
        if (u(f)[k]! < 100) return;
        u(f)[k] = 0; u(f)[`mortal${idx(b, alvo)}`] = 1;
        m.aviso(b, f, 'Postura quebrada', alvo);
        m.efeitos(b, f, [alvo], [st('paralyzed', 1, 1.5)]);
      },
      causa(m, b, f, alvo, g) {
        const k = `mortal${idx(b, alvo)}`;
        if (!g.direto || !u(f)[k]) return 1;
        u(f)[k] = 0;
        m.aviso(b, f, 'Golpe mortal', alvo);
        return 2;
      },
    },
  },
  agent47: {
    nome: 'Alvo indefeso',
    texto: 'Profissional: causa 50% a mais em quem está Dormindo, Paralisado, Confuso ou Congelado.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.statuses.some((s) => ATORDOADO.includes(s.id)) ? 1.5 : 1) },
  },
  arthas: {
    nome: 'Gélida',
    texto: 'A espada rouba a alma aos poucos: cada golpe direto tira 5 de Vida máxima do alvo e soma na de Arthas (até 200).',
    ganchos: {
      bateu(_m, _b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo) || (u(f).almas ?? 0) >= 200) return;
        u(f).almas = (u(f).almas ?? 0) + 5;
        alvo.maxHp -= 5; alvo.hp = Math.min(alvo.hp, alvo.maxHp);
        f.maxHp += 5; f.hp += 5;
      },
    },
  },
  geralt: {
    nome: 'Mutações de bruxo',
    texto: 'O corpo de bruxo aguenta mais: todo Status ruim que pega nele dura só metade.',
    ganchos: {
      pegouStatus(_m, _b, f, s) { const x = f.statuses.find((y) => y.id === s); if (x) x.remaining /= 2; },
    },
  },
  gordon: {
    nome: 'Traje HEV',
    texto: 'O traje cuida dele: a primeira vez abaixo de 25% da Vida, injeta morfina — cura 15%, tira os Status ruins e nenhum pega por 5 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).hev || fracao(f) >= 0.25) return;
        u(f).hev = b.time + 5;
        m.aviso(b, f, 'Morfina administrada', f);
        f.statuses = f.statuses.filter((s) => BUFFS.includes(s.id));
        m.cura(b, f, f, f.maxHp * 0.15, 'HEV');
      },
      pegouStatus(_m, b, f, s) { if ((u(f).hev ?? 0) > b.time) f.statuses = f.statuses.filter((x) => x.id !== s); },
    },
  },
  kirby: {
    nome: 'Inalar e copiar',
    texto: 'Inala o primeiro rival que acerta e copia a Mecânica única dele: Kirby passa a jogar com ela até o fim da luta.',
    ganchos: {
      bateu(m, b, f, alvo, dano, g) {
        if (u(f).copia === undefined) {
          const dele = TODAS[alvo.characterId];
          if (!g.direto || !dele || alvo.characterId === 'kirby') return;
          u(f).copia = idx(b, alvo);
          m.aviso(b, f, `Copiou: ${dele.nome}`, alvo);
          dele.ganchos.inicio?.(m, b, f);
          return;
        }
        copiada(b, f)?.bateu?.(m, b, f, alvo, dano, g);
      },
      passo: (m, b, f, dt) => copiada(b, f)?.passo?.(m, b, f, dt),
      causa: (m, b, f, alvo, g) => copiada(b, f)?.causa?.(m, b, f, alvo, g) ?? 1,
      causaAliado: (m, b, f, aliado, alvo, g) => copiada(b, f)?.causaAliado?.(m, b, f, aliado, alvo, g) ?? 1,
      recebe: (m, b, f, fonte, g) => copiada(b, f)?.recebe?.(m, b, f, fonte, g) ?? 1,
      recebeAliado: (m, b, f, aliado, fonte, g) => copiada(b, f)?.recebeAliado?.(m, b, f, aliado, fonte, g) ?? 1,
      curaRecebida: (m, b, f, fonte) => copiada(b, f)?.curaRecebida?.(m, b, f, fonte) ?? 1,
      curaNoRival: (m, b, f, alvo) => copiada(b, f)?.curaNoRival?.(m, b, f, alvo) ?? 1,
      curaFeita: (m, b, f, alvo) => copiada(b, f)?.curaFeita?.(m, b, f, alvo) ?? 1,
      ritmo: (m, b, f) => copiada(b, f)?.ritmo?.(m, b, f) ?? 1,
      desviou: (m, b, f, fonte) => copiada(b, f)?.desviou?.(m, b, f, fonte),
      apanhou: (m, b, f, fonte, dano, g) => copiada(b, f)?.apanhou?.(m, b, f, fonte, dano, g),
      viu: (m, b, f, fonte, alvo, dano, g) => copiada(b, f)?.viu?.(m, b, f, fonte, alvo, dano, g),
      antes: (m, b, f, i) => copiada(b, f)?.antes?.(m, b, f, i),
      usou: (m, b, f, i) => copiada(b, f)?.usou?.(m, b, f, i),
      viuPreparo: (m, b, f, quem, preparo) => copiada(b, f)?.viuPreparo?.(m, b, f, quem, preparo),
      caiu: (m, b, f, quem, quemDerrubou) => copiada(b, f)?.caiu?.(m, b, f, quem, quemDerrubou),
      salva: (m, b, f, alvo, dano, fonte, g) => copiada(b, f)?.salva?.(m, b, f, alvo, dano, fonte, g) ?? null,
      limita: (m, b, f, alvo, valor) => copiada(b, f)?.limita?.(m, b, f, alvo, valor) ?? valor,
      pegouStatus: (m, b, f, s, fonte) => copiada(b, f)?.pegouStatus?.(m, b, f, s, fonte),
      parado: (f, b) => copiada(b, f)?.parado?.(f, b) ?? false,
      alvoDoBasico: (m, b, f) => copiada(b, f)?.alvoDoBasico?.(m, b, f),
    },
  },
  donkeykong: {
    nome: 'Casca de banana',
    texto: 'A cada 12 s joga uma casca de banana: o próximo rival que for agir escorrega e perde a ação inteira.',
    ganchos: {
      passo(m, b, f, dt) {
        if (relogio(f, 'banana', dt, 12, 5)) u(f).casca = 1;
        if (!u(f).casca) return;
        const r = m.rivais(b, f).find((x) => x.action >= 0.97);
        if (!r) return;
        u(f).casca = 0; r.action = 0;
        m.aviso(b, f, 'Escorregou!', r);
      },
    },
  },
  simonbelmont: {
    nome: 'Vampire Killer',
    texto: 'O chicote dos Belmont é feito para os que não morrem: causa 35% a mais em quem já voltou da queda ou está Regenerando, e cada golpe direto tira a Regeneração.',
    ganchos: {
      causa: (_m, _b, _f, alvo) => (alvo.voltou || alvo.statuses.some((s) => s.id === 'regen') ? 1.35 : 1),
      bateu(_m, _b, _f, alvo, _dano, g) { if (g.direto) alvo.statuses = alvo.statuses.filter((s) => s.id !== 'regen'); },
    },
  },
  majinbuu: {
    nome: 'Absorção',
    texto: 'Quando derruba um rival, absorve o que ele tinha de melhor: se batia, Boo causa 15% a mais; se curava, regenera 1% da Vida por segundo; se protegia, leva 15% menos.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quem.side === f.side || quemDerrubou !== f) return;
        const s = quem.stats, tipo = s.healing > s.damage * 0.5 ? 'cura' : s.protection > s.damage * 0.5 ? 'defesa' : 'dano';
        u(f)[tipo] = (u(f)[tipo] ?? 0) + 1;
        m.aviso(b, f, 'Absorção', quem);
      },
      passo(_m, _b, f, dt) { if (u(f).cura) f.hp = Math.min(f.maxHp, f.hp + f.maxHp * 0.01 * u(f).cura! * dt); },
      causa: (_m, _b, f) => 1 + 0.15 * (u(f).dano ?? 0),
      recebe: (_m, _b, f) => 1 - 0.15 * Math.min(2, u(f).defesa ?? 0),
    },
  },
  kuririn: {
    nome: 'Kuririn não!',
    texto: 'Se Kuririn cair, o trio enlouquece de raiva: os aliados ficam Fortalecidos 25% por 10 s.',
    ganchos: {
      morreu(m, b, f) {
        const as = b.fighters.filter((x) => x.side === f.side && vivo(x));
        if (!as.length) return;
        m.aviso(b, f, 'Kuririn não!', as[0]);
        m.efeitos(b, f, as, [st('strengthened', 0.25, 10)]);
      },
    },
  },
  aiolia: {
    nome: 'Rugido do Leão',
    texto: 'Cada rival que cai faz Aiolia rugir: os outros rivais ficam Enfraquecidos 15% por 4 s.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side === f.side) return;
        const rs = m.rivais(b, f);
        if (!rs.length) return;
        m.aviso(b, f, 'Rugido do Leão', f);
        m.efeitos(b, f, rs, [st('weakened', 0.15, 4)]);
      },
    },
  },
  hadescz: {
    nome: 'Juízo dos mortos',
    texto: 'O submundo não devolve ninguém: rival que cai enquanto Hades está de pé nunca mais volta — nem Renascer, nem Reviver.',
    ganchos: { caiu(m, b, f, quem) { if (quem.side !== f.side && !quem.voltou) { quem.voltou = true; quem.renascendo = 0; m.aviso(b, f, 'Juízo', quem); } } },
  },
  madara: {
    nome: 'Meteoro',
    texto: 'A cada 20 s, puxa um meteoro do céu: 120 de dano divididos entre os rivais de pé (quanto menos rivais, mais dói em cada um).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'meteoro', dt, 20, 10)) return;
        const rs = m.rivais(b, f);
        if (!rs.length) return;
        m.aviso(b, f, 'Meteoro', rs[0]);
        for (const r of rs) m.dano(b, f, r, 120 / rs.length, false, 'Meteoro');
      },
    },
  },
  minato: {
    nome: 'Selo do Ceifador',
    texto: 'Minato dá a vida pelo trio: se ele cair, sela o rival mais forte, que fica Silenciado por 6 s.',
    ganchos: {
      morreu(m, b, f) {
        const r = maisForte(m, b, f);
        if (!r) return;
        m.aviso(b, f, 'Selo do Ceifador', r);
        m.efeitos(b, f, [r], [st('silenced', 1, 6)]);
      },
    },
  },
  cell: {
    nome: 'Autodestruição',
    texto: 'A primeira vez abaixo de 20% da Vida, Cell infla: 3 s depois explode, causando 18% da Vida máxima dele em cada rival — e se refaz de uma célula, com 1 de Vida.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).bomba && fracao(f) < 0.2) { u(f).bomba = b.time + 3; m.aviso(b, f, 'Vai explodir!', f); } },
      passo(m, b, f) {
        if (!u(f).bomba || u(f).bomba! < 0 || b.time < u(f).bomba!) return;
        u(f).bomba = -1;
        m.aviso(b, f, 'Autodestruição', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, f.maxHp * 0.18, false, 'Explosão');
        f.hp = 1;
      },
    },
  },
  mewtwo: {
    nome: 'Disable',
    texto: 'O primeiro rival que acerta Mewtwo com uma habilidade é bloqueado pela mente dele: fica Silenciado por 3 s (uma vez por rival).',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.habilidade || fonte.side === f.side || !vivo(fonte)) return;
        const k = `disable${idx(b, fonte)}`;
        if (u(f)[k]) return;
        u(f)[k] = 1;
        m.aviso(b, f, 'Disable', fonte);
        m.efeitos(b, f, [fonte], [st('silenced', 1, 3)]);
      },
    },
  },
  charizard: {
    nome: 'Fogo que se espalha',
    texto: 'As habilidades dele pegam fogo em volta: quando acertam um rival, os outros rivais também ficam Queimando por 2 s.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.habilidade || !g.direto || (u(f).fogo ?? 0) > b.time) return;
        u(f).fogo = b.time + 0.5;
        m.efeitos(b, f, m.rivais(b, f).filter((r) => r !== alvo), [st('burning', 6, 2)]);
      },
    },
  },
  genos: {
    nome: 'Sacrifício do ciborgue',
    texto: 'Uma vez por luta, quando um aliado ia cair, Genos se joga na frente: o aliado fica com 1 de Vida, Genos perde metade da Vida que tem e o núcleo explode, 80 em todos os rivais.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo === f || u(f).sacrificio || !vivo(f)) return null;
        u(f).sacrificio = 1;
        m.aviso(b, f, 'Sacrifício', alvo);
        f.hp = Math.max(1, f.hp / 2);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 80, false, 'Núcleo');
        return 1;
      },
    },
  },
  coringa: {
    nome: 'Piada final',
    texto: 'Mesmo caindo, o Coringa ri por último: quando ele cai, todo mundo que está de pé na luta — dos dois lados — fica Confuso por 2 s.',
    ganchos: {
      morreu(m, b, f) {
        const todos = b.fighters.filter(vivo);
        if (!todos.length) return;
        m.aviso(b, f, 'HAHAHA', todos[0]);
        m.efeitos(b, f, todos, [st('confused', 1, 2)]);
      },
    },
  },
  lexluthor: {
    nome: 'Ódio dos heróis',
    texto: 'Não suporta quem se acha: causa 25% a mais em rivais que estão com algum Status bom.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.statuses.some((s) => BUFFS.includes(s.id)) ? 1.25 : 1) },
  },
  donatello: {
    nome: 'Campo de contenção',
    texto: 'A cada 15 s, a engenhoca prende o rival mais perto de agir: Enraizado por 2 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'campo', dt, 15, 7)) return;
        const r = m.rivais(b, f).sort((x, y) => y.action - x.action)[0];
        if (r) { m.aviso(b, f, 'Campo de contenção', r); m.efeitos(b, f, [r], [st('rooted', 1, 2)]); }
      },
    },
  },
  pernalonga: {
    nome: 'É temporada de patos!',
    texto: 'Confunde até quem ataca: 1 em 4 habilidades que acertariam o Pernalonga vão parar num aliado de quem lançou.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.habilidade || !g.direto || fonte.side === f.side || m.sorte(b) >= 0.25) return 1;
        u(f).desvio = 1; u(f).de = idx(b, fonte);
        m.aviso(b, f, 'O que é que há?', fonte);
        return 1;
      },
      limita(m, b, f, alvo, valor) {
        if (alvo !== f || !u(f).desvio) return valor;
        u(f).desvio = 0;
        const de = b.fighters[u(f).de ?? -1], rs = m.rivais(b, f), r = rs.find((x) => x !== de) ?? de;
        if (r && vivo(r)) m.dano(b, f, r, valor, false, 'Trapalhada');
        return 0;
      },
    },
  },
  ben10: {
    nome: 'Omnitrix',
    texto: 'A cada 15 s o Omnitrix troca de alien: Quatro Braços (causa 20% a mais), Chama (golpes queimam), XLR8 (age 20% mais rápido) ou Diamante (leva 15% menos). Às vezes erra e não vira nada.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'omnitrix', dt, 15, 0)) return;
        u(f).alien = m.sorte(b) < 1 / 6 ? 4 : Math.floor(m.sorte(b) * 4);
        m.aviso(b, f, ['Quatro Braços', 'Chama', 'XLR8', 'Diamante', 'Ops… nada'][u(f).alien!]!, f);
      },
      causa: (_m, _b, f) => (u(f).alien === 0 ? 1.2 : 1),
      bateu(m, b, f, alvo, _dano, g) { if (u(f).alien === 1 && g.direto && vivo(alvo)) m.efeitos(b, f, [alvo], [st('burning', 6, 2)]); },
      ritmo: (_m, _b, f) => (u(f).alien === 2 ? 1.2 : 1),
      recebe: (_m, _b, f) => (u(f).alien === 3 ? 0.85 : 1),
    },
  },
  optimus: {
    nome: 'Matriz da Liderança',
    texto: 'Se Optimus cair, passa a Matriz para o aliado com mais Vida: ele ganha 20% de Vida máxima e fica Fortalecido 20% até o fim da luta.',
    ganchos: {
      morreu(m, b, f) {
        const a = b.fighters.filter((x) => x.side === f.side && vivo(x)).sort((x, y) => y.hp - x.hp)[0];
        if (!a) return;
        m.aviso(b, f, 'Matriz da Liderança', a);
        const extra = a.maxHp * 0.2; a.maxHp += extra; a.hp += extra;
        m.efeitos(b, f, [a], [st('strengthened', 0.2, 999)]);
      },
    },
  },
  rick: {
    nome: 'Outra dimensão',
    texto: 'A cada 15 s abre um portal debaixo do rival mais forte: ele some por 2 s — não age, e o trio do Rick também não consegue machucá-lo.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'dimensao', dt, 15, 6)) return;
        const r = maisForte(m, b, f);
        if (!r) return;
        u(f).exilio = idx(b, r); u(f).volta = b.time + 2;
        m.aviso(b, f, 'Portal', r);
        m.efeitos(b, f, [r], [st('paralyzed', 1, 2)]);
      },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).exilio === idx(b, alvo) && (u(f).volta ?? 0) > b.time ? 0 : 1),
    },
  },
  mickey: {
    nome: 'Vassouras encantadas',
    texto: 'Cada habilidade do Mickey encanta mais uma vassoura (até 4). A cada 3 s, cada vassoura bate num rival: 10 de dano.',
    ganchos: {
      usou(m, b, f) { if ((u(f).vassouras ?? 0) < 4) { u(f).vassouras = (u(f).vassouras ?? 0) + 1; m.aviso(b, f, 'Vassoura!', f, u(f).vassouras); } },
      passo(m, b, f, dt) {
        if (!relogio(f, 'vassoura', dt, 3) || !(u(f).vassouras ?? 0)) return;
        const rs = m.rivais(b, f);
        for (let i = 0; i < u(f).vassouras! && rs.length; i++) m.dano(b, f, rs[Math.floor(m.sorte(b) * rs.length)]!, 10, false, 'Vassoura');
      },
    },
  },
  srincrivel: {
    nome: 'Arremesso de carro',
    texto: 'A cada 12 s arremessa algo pesado no rival mais forte: 70 de dano, e ele perde 20% da barra de ação.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'carro', dt, 12, 6)) return;
        const r = maisForte(m, b, f);
        if (!r) return;
        m.aviso(b, f, 'Arremesso!', r);
        m.dano(b, f, r, 70, false, 'Arremesso');
        r.action = Math.max(0, r.action - 0.2);
      },
    },
  },
  mulherelastica: {
    nome: 'Corpo que estica',
    texto: 'Estica e amortece: golpes de mais de 10% da Vida dela chegam 25% mais fracos.',
    ganchos: { limita: (_m, _b, f, alvo, valor) => (alvo === f && valor > f.maxHp * 0.1 ? valor * 0.75 : valor) },
  },
  zuko: {
    nome: 'Redirecionar relâmpago',
    texto: 'Aprendeu com o tio: nunca fica Eletrificado — o raio passa pelo corpo e volta como 60 de dano em quem lançou. E causa 20% a mais em rivais Eletrificados.',
    ganchos: {
      pegouStatus(m, b, f, s, fonte) {
        if (s !== 'electric') return;
        f.statuses = f.statuses.filter((x) => x.id !== 'electric');
        m.aviso(b, f, 'Redirecionado!', fonte);
        if (vivo(fonte)) m.dano(b, f, fonte, 60, false, 'Relâmpago');
      },
      causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'electric') > 0 ? 1.2 : 1),
    },
  },
  toph: {
    nome: 'Terremoto',
    texto: 'A cada 15 s sente pelos pés quem vai agir e bate o pé embaixo dele: o rival mais perto de agir fica Enraizado por 1 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'terremoto', dt, 15, 7)) return;
        const r = m.rivais(b, f).sort((x, y) => y.action - x.action)[0];
        if (r) { m.aviso(b, f, 'Terremoto', r); m.efeitos(b, f, [r], [st('rooted', 1, 1)]); }
      },
    },
  },
  coiote: {
    nome: 'Encomenda ACME',
    texto: 'A cada 15 s chega uma caixa ACME sorteada: Foguete (+50% de ação), Bigorna (80 no rival mais forte), Ímã (puxa o Escudo de um rival para ele) ou Dinamite (60 em todos os rivais… e 40 nele).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'acme', dt, 15, 7)) return;
        const c = Math.floor(m.sorte(b) * 4), r = maisForte(m, b, f);
        if (c === 0) { m.aviso(b, f, 'Foguete ACME', f); f.action = Math.min(1, f.action + 0.5); }
        if (c === 1 && r) { m.aviso(b, f, 'Bigorna ACME', r); m.dano(b, f, r, 80, false, 'Bigorna'); }
        if (c === 2) {
          const alvo = m.rivais(b, f).find((x) => x.shields.length);
          m.aviso(b, f, 'Ímã ACME', alvo ?? f);
          if (alvo) { const total = alvo.shields.reduce((n, s) => n + s.amount, 0); alvo.shields = []; f.shields.push({ amount: total, remaining: 10, source: f.uid }); }
        }
        if (c === 3) { m.aviso(b, f, 'Dinamite ACME', f); for (const x of m.rivais(b, f)) m.dano(b, f, x, 60, false, 'Dinamite'); f.hp = Math.max(1, f.hp - 40); }
      },
    },
  },
  papaleguas: {
    nome: 'Poeira na pista',
    texto: 'Passa tão rápido que levanta poeira: metade dos golpes diretos dele deixam o alvo Cego por 1 s.',
    ganchos: { bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && m.sorte(b) < 0.5) m.efeitos(b, f, [alvo], [st('blind', 0.3, 1)]); } },
  },
  jerry: {
    nome: 'Quanto maior, maior o tombo',
    texto: 'O ratinho adora os grandões: causa 3% a mais para cada 100 de Vida máxima que o alvo tem a mais que ele (até 40%).',
    ganchos: { causa: (_m, _b, f, alvo) => 1 + Math.min(0.4, Math.max(0, (alvo.maxHp - f.maxHp) / 100) * 0.03) },
  },
  shredder: {
    nome: 'Garras de aço',
    texto: 'Cada golpe direto deixa um corte no alvo. No 4º corte, as garras abrem a ferida: o rival Sangra forte (25 por segundo, 3 s).',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const k = `corte${idx(b, alvo)}`;
        u(f)[k] = (u(f)[k] ?? 0) + 1;
        if (u(f)[k]! < 4) return;
        u(f)[k] = 0;
        m.aviso(b, f, 'Garras de aço', alvo);
        m.efeitos(b, f, [alvo], [st('bleed', 25, 3)]);
      },
    },
  },
  krang: {
    nome: 'Corpo de andróide',
    texto: 'O cérebro anda num corpo robô gigante: começa com 12% a mais de Vida máxima, mas robô não se cura — nenhuma cura funciona nele.',
    ganchos: {
      inicio(_m, _b, f) { f.maxHp *= 1.12; f.hp = f.maxHp; },
      curaRecebida: () => 0,
    },
  },
  liono: {
    nome: 'Visão além do alcance',
    texto: 'A Espada de Augúrio mostra quem vai agir: o ataque básico vai sempre no rival mais perto de agir, com 25% a mais.',
    ganchos: {
      alvoDoBasico: (m, b, f) => m.rivais(b, f).sort((x, y) => y.action - x.action)[0],
      causa: (m, b, f, alvo, g) => (g.direto && !g.habilidade && m.rivais(b, f).sort((x, y) => y.action - x.action)[0] === alvo ? 1.25 : 1),
    },
  },
  capitaoplaneta: {
    nome: 'Pelos cinco anéis',
    texto: 'Cada habilidade dele chama um anel, em ciclo: Terra (Escudo de 2% no trio), Fogo (rivais Queimando 2 s), Vento (rivais perdem 8% da ação), Água (cura 1,5% do trio) e Coração (trio Fortalecido 4% por 4 s).',
    ganchos: {
      usou(m, b, f) {
        const anel = (u(f).anel ?? 0) % 5; u(f).anel = anel + 1;
        const as = m.aliados(b, f), rs = m.rivais(b, f);
        m.aviso(b, f, ['Terra!', 'Fogo!', 'Vento!', 'Água!', 'Coração!'][anel]!, f);
        if (anel === 0) for (const a of as) a.shields.push({ amount: a.maxHp * 0.02, remaining: 8, source: f.uid });
        if (anel === 1) m.efeitos(b, f, rs, [st('burning', 3, 2)]);
        if (anel === 2) for (const r of rs) r.action = Math.max(0, r.action - 0.08);
        if (anel === 3) for (const a of as) m.cura(b, f, a, a.maxHp * 0.015, 'Água');
        if (anel === 4) m.efeitos(b, f, as, [st('strengthened', 0.04, 4)]);
      },
    },
  },
  bugiganga: {
    nome: 'Quem resolve é a Penny',
    texto: 'Bugiganga atrapalha, mas a sobrinha resolve: enquanto ele está de pé, o aliado que mais causou dano na luta causa 15% a mais.',
    ganchos: {
      causaAliado(_m, b, f, aliado) {
        if (aliado === f) return 1;
        const melhor = b.fighters.filter((x) => x.side === f.side && x !== f && vivo(x)).sort((x, y) => y.stats.damage - x.stats.damage)[0];
        return melhor === aliado ? 1.15 : 1;
      },
    },
  },
  galactus: {
    nome: 'Devorador de mundos',
    texto: 'Grande demais para os insetos: quem tem menos Vida máxima que ele causa 8% a menos nele. E cada rival que cai vira comida: Galactus recupera 8% da Vida.',
    ganchos: {
      recebe: (_m, _b, f, fonte) => (fonte.side !== f.side && fonte.maxHp < f.maxHp ? 0.92 : 1),
      caiu(m, b, f, quem) { if (quem.side !== f.side) { m.aviso(b, f, 'Devorado', quem); m.cura(b, f, f, f.maxHp * 0.08, 'Devorar'); } },
    },
  },
  dannyphantom: {
    nome: 'Lamento fantasma',
    texto: 'Uma vez por luta, abaixo de 30% da Vida, solta o lamento fantasma: 150 de dano em todos os rivais — e fica 2 s Paralisado de cansaço.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).lamento || fracao(f) >= 0.3) return;
        u(f).lamento = 1;
        m.aviso(b, f, 'Lamento fantasma', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 150, false, 'Lamento');
        m.efeitos(b, f, [f], [st('paralyzed', 1, 2)]);
      },
    },
  },
};
