/*
 * Mecânicas únicas — lote 9: os últimos 54 (Kirby, Link, Dante, Sekiro,
 * Coringa, Optimus, Mario…). Com este lote, todo personagem tem a dele.
 */
import { avisoACada, BUFFS, fracao, maisForte, relogio, st, u, vivo, type Ganchos, type Unica } from './unicas-base';
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
    texto: 'Enquanto o Senhor das Estrelas está de pé, cada habilidade do trio tem 12% de chance de causar +60% de dano.',
    ganchos: {
      causaAliado(m, b, f, aliado, _alvo, g) {
        if (!(g.habilidade && g.direto && m.sorte(b) < 0.12)) return 1;
        m.aviso(b, f, 'Doze por cento', aliado);
        return 1.6;
      },
    },
  },
  groot: {
    nome: 'Galhos que protegem',
    texto: 'Quando Groot fica com menos de 75%, de 50% e de 25% da Vida (1 vez cada), o aliado mais ferido ganha Escudo de 8% da Vida máxima de Groot por 12 s.',
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
    texto: 'Cada habilidade do Lanterna Verde gasta 20% da bateria do anel. Com 20% de bateria ou mais, o Lanterna causa +15% de dano. Quando a bateria fica abaixo de 20%, o Lanterna para 3 s para recarregar (volta a 100%).',
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
    texto: 'A cada 15 s, Shazam grita SHAZAM!: recupera 6% da Vida máxima e causa 40 de dano em um rival aleatório.',
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
    texto: 'Com 90% da Vida ou mais, cada ataque básico de Link solta o feixe da Espada Mestra: 30 de dano em outro rival.',
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
    texto: 'Cada golpe de Dante sobe o Estilo: +4% de dano (até 7 vezes: +28%). Cada ataque ou habilidade que acerta Dante tira 2 níveis de Estilo.',
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
    nome: 'Desvio perfeito',
    texto: 'A cada 18 s, Bayonetta prepara o Witch Time: desvia do próximo ataque ou habilidade que acertaria Bayonetta, e todos os rivais ficam Lento (25% mais lento) por 1,5 s.',
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
    texto: 'Master Chief começa com Escudo de 6% da Vida máxima. Quando esse Escudo quebra, volta inteiro 12 s depois.',
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
    texto: 'Cada golpe de Solid Snake tem 12,5% de chance de deixar o alvo Dormindo por 1,2 s.',
    ganchos: { bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && m.sorte(b) < 0.125) { m.aviso(b, f, 'Zzz', alvo); m.efeitos(b, f, [alvo], [st('sleep', 1, 1.2)]); } } },
  },
  lara: {
    nome: 'Terreno preparado',
    texto: 'Cada ataque básico que acerta Lara Croft tem 33% de chance de deixar quem bateu Preso (65% mais lento) por 1 s.',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && !g.habilidade && vivo(fonte) && m.sorte(b) < 1 / 3) m.efeitos(b, f, [fonte], [st('rooted', 1, 1)]); } },
  },
  megaman: {
    nome: 'Prêmio do chefe',
    texto: 'Cada rival que cai dá a Mega Man um bônus sorteado até o fim da luta (33% de chance cada): Fortalecido (+15% de dano), Acelerado (15% mais rápido) ou Protegido (−15% de dano recebido).',
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
    texto: 'Mario começa pequeno: −15% de Vida máxima. Depois de 5 golpes, come o Super Cogumelo e fica com +15% de Vida máxima (em relação à original). Um golpe de mais de 15% da Vida máxima faz Mario encolher de novo.',
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
    nome: 'Puxão infernal',
    texto: 'A cada 12 s, Scorpion puxa o rival mais perto de agir: esse rival perde toda a barra do Próximo ataque e leva 40 de dano.',
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
    texto: 'Quem acerta Raiden com ataque ou habilidade leva 8 de dano e tem 50% de chance de ficar Eletrificado (−12% da barra por golpe) por 1 s.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.direto || !vivo(fonte) || fonte.side === f.side) return;
        m.dano(b, f, fonte, 8, false, 'Choque');
        if (m.sorte(b) < 0.5) m.efeitos(b, f, [fonte], [st('electric', 0.2, 1)]);
      },
    },
  },
  sekiro: {
    nome: 'Quebra de postura',
    texto: 'Cada golpe de Sekiro enche 20 na postura do rival. Com 100: o rival fica Paralisado por 1,5 s, e o próximo golpe de Sekiro nele causa o dobro de dano.',
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
    texto: 'O Agente 47 causa +50% de dano em quem está Dormindo, Paralisado, Confuso ou Congelado.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.statuses.some((s) => ATORDOADO.includes(s.id)) ? 1.5 : 1) },
  },
  arthas: {
    nome: 'Gélida',
    texto: 'Cada golpe de Arthas tira 5 de Vida máxima do alvo e soma 5 na Vida máxima de Arthas (até +200).',
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
    texto: 'Todo Status ruim em Geralt de Rívia dura só metade do tempo.',
    ganchos: {
      pegouStatus(_m, _b, f, s) { const x = f.statuses.find((y) => y.id === s); if (x) x.remaining /= 2; },
    },
  },
  gordon: {
    nome: 'Traje HEV',
    texto: 'Com menos de 25% da Vida (1 vez por luta): Gordon Freeman cura 15% da Vida máxima, perde todos os Status ruins e, por 5 s, nenhum Status ruim pega nele.',
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
    texto: 'Kirby copia a Mecânica única do primeiro rival que acerta e usa essa mecânica até o fim da luta.',
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
    texto: 'A cada 12 s, Donkey Kong joga uma casca de banana: o próximo rival que for agir escorrega e perde toda a barra do Próximo ataque.',
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
    texto: 'Simon Belmont causa +35% de dano em quem já voltou de uma queda ou tem Regeneração. Cada golpe de Simon tira a Regeneração do alvo.',
    ganchos: {
      causa: (_m, _b, _f, alvo) => (alvo.voltou || alvo.statuses.some((s) => s.id === 'regen') ? 1.35 : 1),
      bateu(_m, _b, _f, alvo, _dano, g) { if (g.direto) alvo.statuses = alvo.statuses.filter((s) => s.id !== 'regen'); },
    },
  },
  majinbuu: {
    nome: 'Come e copia',
    texto: 'Quando Majin Boo derruba um rival, absorve o ponto forte desse rival: +15% de dano (se o rival causava dano), cura de 1% da Vida máxima por segundo (se curava) ou −15% de dano recebido (se protegia, até −30%).',
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
    texto: 'Quando Kuririn cai, os aliados de pé ficam Fortalecido (+25% de dano) por 10 s.',
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
    nome: 'Orgulho do leão',
    texto: 'Cada rival que cai faz Aiolia rugir: os outros rivais ficam Enfraquecido (−15% de dano) por 4 s.',
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
    nome: 'Ninguém volta',
    texto: 'Enquanto Hades está de pé, rival que cai não volta mais: nem por Renascer nem por Reviver.',
    ganchos: { caiu(m, b, f, quem) { if (quem.side !== f.side && !quem.voltou) { quem.voltou = true; quem.renascendo = 0; m.aviso(b, f, 'Juízo', quem); } } },
  },
  madara: {
    nome: 'Chuva de meteoros',
    texto: 'A cada 20 s, Madara Uchiha faz cair um meteoro: 120 de dano divididos entre os rivais de pé.',
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
    texto: 'Quando Minato Namikaze cai, o rival com mais Vida fica Silenciado por 6 s.',
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
    texto: 'Com menos de 20% da Vida, ainda de pé (1 vez por luta): 3 s depois, Cell explode. Cada rival leva dano igual a 18% da Vida máxima de Cell, e Cell fica com 1 de Vida. Se Cell cair antes, não explode e pode tentar de novo depois de renascer.',
    ganchos: {
      // só arma com o Cell de pé, entre 1 de Vida e 20% (o golpe que derruba não arma: aí é o Renascer)
      apanhou(m, b, f) { if (!u(f).bomba && vivo(f) && fracao(f) < 0.2) { u(f).bomba = b.time + 3; m.aviso(b, f, 'Vai explodir!', f); } },
      // caiu durante a contagem: a explosão não sai e não conta como usada (depois de renascer, pode armar de novo)
      morreu(_m, _b, f) { if ((u(f).bomba ?? 0) > 0) u(f).bomba = 0; },
      passo(m, b, f) {
        if (!u(f).bomba || u(f).bomba! < 0 || b.time < u(f).bomba! || !vivo(f)) return;
        u(f).bomba = -1;
        m.aviso(b, f, 'Autodestruição', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, f.maxHp * 0.18, false, 'Explosão');
        f.hp = 1;
      },
    },
  },
  mewtwo: {
    nome: 'Disable',
    texto: 'O primeiro rival que acerta Mewtwo com habilidade fica Silenciado por 3 s (1 vez por rival).',
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
    texto: 'Cada habilidade de Charizard que acerta um rival deixa os outros rivais Queimando (−6 de Vida por segundo) por 2 s.',
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
    texto: '1 vez por luta: quando um golpe ia derrubar um aliado, Genos sacrifica o núcleo: o aliado fica com 1 de Vida, Genos perde metade da Vida que tem e cada rival leva 80 de dano.',
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
    nome: 'Última risada',
    texto: 'Quando o Coringa cai, todos que estão de pé (dos dois trios) ficam Confuso por 2 s.',
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
    texto: 'Lex Luthor causa +25% de dano em rivais com algum Status bom.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.statuses.some((s) => BUFFS.includes(s.id)) ? 1.25 : 1) },
  },
  donatello: {
    nome: 'Armadilha tecnológica',
    texto: 'A cada 15 s, Donatello prende o rival mais perto de agir no campo de contenção: Preso (65% mais lento) por 2 s.',
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
    texto: 'Cada habilidade rival que acertaria o Pernalonga tem 25% de chance de não causar dano no Pernalonga e ir inteira em outro rival.',
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
    texto: 'A cada 15 s (a primeira logo no começo da luta), Ben 10 gira o Omnitrix e vira um alien até a próxima troca, com cerca de 21% de chance cada: Quatro Braços (+20% de dano), Chama (cada golpe deixa o alvo Queimando (−6 de Vida por segundo) por 2 s), XLR8 (age 20% mais rápido) ou Diamante (−15% de dano recebido). Há 17% de chance de o Omnitrix falhar e Ben não virar nada.',
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
    texto: 'Quando Optimus Prime cai, o aliado com mais Vida recebe a Matriz da Liderança: +20% de Vida máxima e Fortalecido (+20% de dano) até o fim da luta.',
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
    texto: 'A cada 15 s, Rick Sanchez manda o rival com mais Vida para outra dimensão por 2 s: esse rival fica Paralisado, e o trio de Rick não causa dano nele nesse tempo.',
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
    nome: 'Aprendiz de feiticeiro',
    texto: 'Cada habilidade de Mickey Mouse cria uma vassoura encantada (até 4). A cada 3 s, cada vassoura causa 10 de dano em um rival aleatório.',
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
    texto: 'A cada 12 s, o Sr. Incrível arremessa um carro no rival com mais Vida: 70 de dano, e esse rival perde 20% da barra do Próximo ataque.',
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
    texto: 'Todo golpe de mais de 10% da Vida máxima da Mulher-Elástica chega com −25% de dano.',
    ganchos: { limita: (_m, _b, f, alvo, valor) => (alvo === f && valor > f.maxHp * 0.1 ? valor * 0.75 : valor) },
  },
  zuko: {
    nome: 'Imune a raio',
    texto: 'Zuko nunca fica Eletrificado: redireciona o raio e devolve 60 de dano em quem tentou. Zuko causa +20% de dano em quem está Eletrificado.',
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
    texto: 'A cada 15 s, Toph faz a terra tremer: o rival mais perto de agir fica Preso (65% mais lento) por 1 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'terremoto', dt, 15, 7)) return;
        const r = m.rivais(b, f).sort((x, y) => y.action - x.action)[0];
        if (r) { m.aviso(b, f, 'Terremoto', r); m.efeitos(b, f, [r], [st('rooted', 1, 1)]); }
      },
    },
  },
  coiote: {
    nome: 'Catálogo ACME',
    texto: 'A cada 15 s, o Coiote recebe uma encomenda ACME (25% de chance cada). Foguete: o Coiote ganha 50% da barra do Próximo ataque. Bigorna: 80 de dano no rival com mais Vida. Ímã: rouba todo o Escudo de um rival e fica com esse Escudo por 10 s. Dinamite: 60 de dano em cada rival, e o Coiote perde 40 de Vida (sem cair por isso).',
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
    nome: 'Comendo poeira',
    texto: 'Cada golpe do Papa-Léguas tem 50% de chance de deixar o alvo Cego (30% de chance de errar o ataque básico) por 1 s.',
    ganchos: { bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && m.sorte(b) < 0.5) m.efeitos(b, f, [alvo], [st('blind', 0.3, 1)]); } },
  },
  jerry: {
    nome: 'Quanto maior, maior o tombo',
    texto: 'Jerry causa +3% de dano para cada 100 de Vida máxima que o alvo tem a mais que Jerry (até +40%).',
    ganchos: { causa: (_m, _b, f, alvo) => 1 + Math.min(0.4, Math.max(0, (alvo.maxHp - f.maxHp) / 100) * 0.03) },
  },
  shredder: {
    nome: 'Corte que sangra',
    texto: 'A cada 4 golpes do Shredder no mesmo rival, esse rival fica Sangrando (−25 de Vida por ação) por 3 s.',
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
    texto: 'Krang começa com +12% de Vida máxima, mas nenhuma cura funciona em Krang.',
    ganchos: {
      inicio(_m, _b, f) { f.maxHp *= 1.12; f.hp = f.maxHp; },
      curaRecebida: () => 0,
    },
  },
  liono: {
    nome: 'Instinto de caçador',
    texto: 'O ataque básico de Lion-O vai no rival mais perto de agir, com +25% de dano.',
    ganchos: {
      alvoDoBasico: (m, b, f) => m.rivais(b, f).sort((x, y) => y.action - x.action)[0],
      causa: (m, b, f, alvo, g) => (g.direto && !g.habilidade && m.rivais(b, f).sort((x, y) => y.action - x.action)[0] === alvo ? 1.25 : 1),
    },
  },
  capitaoplaneta: {
    nome: 'Pelos cinco anéis',
    texto: 'Cada habilidade do Capitão Planeta chama um anel, nesta ordem. Terra: Escudo de 2% da Vida máxima em todo o trio por 8 s. Fogo: todos os rivais ficam Queimando (−3 de Vida por segundo) por 2 s. Vento: todos os rivais perdem 8% da barra do Próximo ataque. Água: todo o trio cura 1,5% da Vida máxima. Coração: todo o trio fica Fortalecido (+4% de dano) por 4 s.',
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
    texto: 'Enquanto o Inspetor Bugiganga está de pé, o aliado que mais causou dano na luta (sem contar o Bugiganga) causa +15% de dano.',
    ganchos: {
      causaAliado(m, b, f, aliado) {
        if (aliado === f) return 1;
        const melhor = b.fighters.filter((x) => x.side === f.side && x !== f && vivo(x)).sort((x, y) => y.stats.damage - x.stats.damage)[0];
        if (melhor === aliado) avisoACada(m, b, f, 'penny', 15, 'Quem resolve é a Penny', aliado);
        return melhor === aliado ? 1.15 : 1;
      },
    },
  },
  galactus: {
    nome: 'Devorador de mundos',
    texto: 'Rivais com menos Vida máxima que Galactus causam −8% de dano em Galactus. Cada rival que cai: Galactus cura 8% da Vida máxima.',
    ganchos: {
      recebe: (_m, _b, f, fonte) => (fonte.side !== f.side && fonte.maxHp < f.maxHp ? 0.92 : 1),
      caiu(m, b, f, quem) { if (quem.side !== f.side) { m.aviso(b, f, 'Devorado', quem); m.cura(b, f, f, f.maxHp * 0.08, 'Devorar'); } },
    },
  },
  dannyphantom: {
    nome: 'Último grito',
    texto: 'Com menos de 30% da Vida (1 vez por luta): Danny Phantom solta o Lamento fantasma: 150 de dano em cada rival, mas Danny fica Paralisado por 2 s.',
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
