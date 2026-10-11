/*
 * Mecânicas únicas — lote 6: os antigos que mais se pareciam com alguém.
 */
import { fracao, maisFerido, maisForte, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import { byId } from '../data/characters';
import type { Battle, Effect, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const invoca = (valor: number, duracao: number, rotulo: string): Effect => ({ kind: 'status', status: 'summon', value: valor, duration: duracao, rotulo });
const maisFraco = (m: Motor, b: Battle, f: Fighter) => m.rivais(b, f).sort((x, y) => x.hp - y.hp)[0];
const RUINS: StatusId[] = ['paralyzed', 'frozen', 'sleep', 'silenced', 'rooted', 'provoked', 'confused', 'blind', 'poison', 'bleed', 'cursed', 'slow', 'burning', 'exposed', 'marked', 'electric', 'weakened', 'bomb'];
const BONS: StatusId[] = ['strengthened', 'haste', 'protected', 'regen', 'barrier', 'evasion', 'reflect', 'vampirism', 'thorns', 'summon'];
const temRuim = (f: Fighter) => f.statuses.some((s) => RUINS.includes(s.id));

export const LOTE6: Record<string, Unica> = {
  levi: {
    nome: 'Corte na nuca',
    texto: 'O primeiro golpe de Levi em cada rival pega desprevenido e causa o dobro.',
    ganchos: {
      causa(_m, b, f, alvo, g) {
        if (!g.direto || u(f)[`nuca${idx(b, alvo)}`]) return 1;
        u(f)[`nuca${idx(b, alvo)}`] = 1;
        return 2;
      },
    },
  },
  kurapika: {
    nome: 'Corrente do julgamento',
    texto: 'Jura vingança contra o rival mais forte: causa 60% a mais nele. Mas o juramento cobra: cada golpe dele em outro rival custa 4% da própria Vida.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).juramento = idx(b, a); m.aviso(b, f, 'Juramento', a); } },
      causa: (_m, b, f, alvo) => (u(f).juramento === idx(b, alvo) ? 1.6 : 1),
      bateu(_m, b, f, alvo, _dano, g) {
        if (!g.direto || u(f).juramento === idx(b, alvo) || !vivo(b.fighters[u(f).juramento ?? -1] ?? f)) return;
        f.hp = Math.max(1, f.hp - f.maxHp * 0.04);
      },
    },
  },
  dio: {
    nome: 'Road Roller',
    texto: 'Uma vez por luta, quando algum rival estiver Paralisado, Dio larga um rolo compressor em cima dele: 250 de dano.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).rolo) return;
        const a = m.rivais(b, f).find((r) => m.intensidade(r, 'paralyzed') > 0);
        if (!a) return;
        u(f).rolo = 1;
        m.aviso(b, f, 'ROAD ROLLER DA!', a);
        m.dano(b, f, a, 250, false, 'Road Roller');
      },
    },
  },
  makima: {
    nome: 'Domínio',
    texto: 'Quem cai pelas mãos do trio dela passa a obedecer a Makima: luta ao lado dela por 10 s.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quem.side === f.side || quemDerrubou.side !== f.side) return;
        m.efeitos(b, f, [f], [invoca(45, 10, byId[quem.characterId]!.name)]);
        m.aviso(b, f, 'Agora é meu', quem);
      },
    },
  },
  wesker: {
    nome: 'Uroboros',
    texto: 'Abaixo de 30% de Vida, o vírus toma conta: regenera 3% da Vida por segundo, mas perde o controle e os ataques básicos vão em rivais aleatórios.',
    ganchos: {
      passo(m, b, f, dt) { if (fracao(f) < 0.3) { if (!u(f).virus) { u(f).virus = 1; m.aviso(b, f, 'Uroboros', f); } m.cura(b, f, f, f.maxHp * 0.03 * dt, 'Uroboros'); } },
      alvoDoBasico(m, b, f) { if (fracao(f) >= 0.3) return undefined; const rs = m.rivais(b, f); return rs[Math.floor(m.sorte(b) * rs.length)]; },
    },
  },
  shadowhh: {
    nome: 'Sem inibidores',
    texto: 'Abaixo de 40% de Vida, tira os anéis inibidores: causa 50% a mais, mas o poder consome 1,5% da Vida por segundo.',
    ganchos: {
      passo(m, b, f, dt) {
        if (fracao(f) >= 0.4) return;
        if (!u(f).aneis) { u(f).aneis = 1; m.aviso(b, f, 'Inibidores fora', f); }
        f.hp = Math.max(1, f.hp - f.maxHp * 0.015 * dt);
      },
      causa: (_m, _b, f) => (u(f).aneis ? 1.5 : 1),
    },
  },
  ikki: {
    nome: 'Das cinzas, mais forte',
    texto: 'A Fênix sempre volta melhor: depois de renascer, causa 35% a mais e age 15% mais rápido até o fim da luta.',
    ganchos: {
      passo(m, b, f) { if (f.voltou && !u(f).fenix) { u(f).fenix = 1; m.aviso(b, f, 'A Fênix voltou mais forte', f); } },
      causa: (_m, _b, f) => (u(f).fenix ? 1.35 : 1),
      ritmo: (_m, _b, f) => (u(f).fenix ? 1.15 : 1),
    },
  },
  mummra: {
    nome: 'Sempre vivo',
    texto: 'A força dos aliados que caem vai para o sarcófago: cada aliado que cai aumenta a Vida máxima de Mumm-Ra em 20% e o cura nesse tanto.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side) return;
        const extra = Math.round(f.maxHp * 0.2);
        f.maxHp += extra;
        m.cura(b, f, f, extra, 'Sempre vivo');
        m.aviso(b, f, 'Mais poder', quem);
      },
    },
  },
  tanjiro: {
    nome: 'Fio da abertura',
    texto: 'O olfato sente a brecha: a cada 8 s, o próximo golpe dele passa por Escudo e Protegido como se não existissem.',
    ganchos: {
      passo(_m, _b, f, dt) { if (relogio(f, 'fio', dt, 8, 4)) u(f).fio = 1; },
      causa(m, b, f, alvo, g) {
        if (!g.direto || !u(f).fio) return 1;
        u(f).fio = 0;
        const p = m.intensidade(alvo, 'protected'), escudo = alvo.shields.reduce((n, s) => n + s.amount, 0);
        if (escudo > 0) alvo.shields = [];
        m.aviso(b, f, 'Fio da abertura', alvo);
        return p > 0 ? 1 / (1 - p) : 1;
      },
    },
  },
  frieren: {
    nome: 'Mana guardada',
    texto: 'Paciência de elfa: cada segundo sem usar habilidade guarda mana — a próxima habilidade causa 5% a mais por segundo guardado (até 60%).',
    ganchos: {
      passo(_m, _b, f, dt) { u(f).mana = Math.min(12, (u(f).mana ?? 0) + dt); },
      causa: (_m, _b, f, _alvo, g) => (g.habilidade ? 1 + 0.05 * (u(f).mana ?? 0) : 1),
      usou(_m, _b, f) { u(f).mana = 0; },
    },
  },
  loki: {
    nome: 'Era uma ilusão',
    texto: 'Quem derrubou Loki derrubou uma ilusão: uma vez por luta, ele aparece de novo na hora com 30% da Vida, e quem o derrubou fica Confuso 3 s.',
    ganchos: {
      salva(m, b, f, alvo, _dano, fonte) {
        if (alvo !== f || u(f).ilusao) return null;
        u(f).ilusao = 1;
        if (vivo(fonte) && fonte.side !== f.side) m.efeitos(b, f, [fonte], [st('confused', 1, 3)]);
        m.aviso(b, f, 'Era uma ilusão', fonte);
        return f.maxHp * 0.3;
      },
    },
  },
  vergil: {
    nome: 'Concentração',
    texto: 'Enquanto ninguém o acerta, a concentração sobe: 3% a mais de dano por segundo, até 45%. Levar um golpe direto zera.',
    ganchos: {
      passo(_m, _b, f, dt) { u(f).foco = Math.min(15, (u(f).foco ?? 0) + dt); },
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).foco = 0; },
      causa: (_m, _b, f) => 1 + 0.03 * (u(f).foco ?? 0),
    },
  },
  ezio: {
    nome: 'Execução em cadeia',
    texto: 'Ao derrubar um rival, a lâmina oculta já está no próximo: Ezio ataca de novo na mesma hora.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side || !m.rivais(b, f).length) return;
        f.action = 1;
        m.aviso(b, f, 'Próximo', f);
      },
    },
  },
  isaac: {
    nome: 'Desmembramento',
    texto: 'Mire nos membros: os golpes dele causam 40% a mais em quem está Lento.',
    ganchos: { causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'slow') > 0 ? 1.4 : 1) },
  },
  saga: {
    nome: 'Duas vontades',
    texto: 'Troca de personalidade a cada 15 s. Lado bom: o trio fica Protegido 15%. Lado mau: Saga causa 35% a mais e os rivais ficam Enfraquecidos 10%.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'vontade', dt, 15, 0.1)) return;
        const mau = (u(f).lado = ((u(f).lado ?? 1) + 1) % 2) === 1;
        if (mau) m.efeitos(b, f, m.rivais(b, f), [st('weakened', 0.1, 15)]);
        else m.efeitos(b, f, m.aliados(b, f), [st('protected', 0.15, 15)]);
        m.aviso(b, f, mau ? 'Lado mau' : 'Lado bom', f);
      },
      causa: (_m, _b, f) => (u(f).lado === 1 ? 1.35 : 1),
    },
  },
  docinho: {
    nome: 'Briguenta',
    texto: 'Cada golpe que leva a deixa mais brava: 5% a mais de dano por golpe (até 50%). Quando usa a habilidade mais forte, descarrega tudo e zera.',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).raiva = Math.min(10, (u(f).raiva ?? 0) + 1); },
      causa: (_m, _b, f) => 1 + 0.05 * (u(f).raiva ?? 0),
      usou(_m, _b, f, i) { if (i === 2) u(f).raiva = 0; },
    },
  },
  caseyjones: {
    nome: 'Goooool!',
    texto: 'A cada 5 golpes diretos, uma tacada de hóquei manda o rival longe: ele perde toda a barra de ação.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        u(f).tacadas = (u(f).tacadas ?? 0) + 1;
        if (u(f).tacadas! % 5) return;
        alvo.action = 0;
        m.aviso(b, f, 'Goooool!', alvo);
      },
    },
  },
  cheetara: {
    nome: 'Velocidade felina',
    texto: 'Age 35% mais rápido que o normal, mas a cada 20 s precisa recuperar o fôlego: fica 2 s parada.',
    ganchos: {
      ritmo: () => 1.35,
      passo(m, b, f, dt) { if (relogio(f, 'folego', dt, 20, 20)) { u(f).folego = b.time + 2; m.aviso(b, f, 'Sem fôlego', f); } },
      parado: (f, b) => (u(f).folego ?? 0) > b.time,
    },
  },
  yusuke: {
    nome: 'Briga de rua',
    texto: 'Não leva desaforo para casa: causa 40% a mais em quem bateu nele nos últimos 3 s.',
    ganchos: {
      apanhou(_m, b, f, fonte, _dano, g) { if (g.direto) u(f)[`troco${idx(b, fonte)}`] = b.time + 3; },
      causa: (_m, b, f, alvo) => ((u(f)[`troco${idx(b, alvo)}`] ?? 0) > b.time ? 1.4 : 1),
    },
  },
  sailormoon: {
    nome: 'Cristal de Prata',
    texto: 'Uma vez por luta, quando um aliado cai, o Cristal de Prata o traz de volta com 50% da Vida — e Sailor Moon perde metade da Vida que tem.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side || u(f).cristal || quem.voltou || (quem.renascendo ?? 0) > 0) return;
        u(f).cristal = 1;
        m.levanta(b, f, quem, 0.5);
        f.hp = Math.max(1, f.hp / 2);
        m.aviso(b, f, 'Cristal de Prata', quem);
      },
    },
  },
  coragem: {
    nome: 'Grito de pavor',
    texto: 'Quando leva um golpe que tira mais de 15% da Vida dele, grita tão alto que todos os rivais ficam Lentos 20% por 2 s.',
    ganchos: {
      apanhou(m, b, f, _fonte, dano) {
        if (dano < f.maxHp * 0.15) return;
        m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.2, 2)]);
        m.aviso(b, f, 'AAAAAH!', f);
      },
    },
  },
  kenpachi: {
    nome: 'Tapa-olho',
    texto: 'Abaixo de metade da Vida, tira o tapa-olho: causa 45% a mais até o fim da luta — mas larga a defesa e fica Exposto 15%.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).olho || fracao(f) >= 0.5) return;
        u(f).olho = 1;
        m.efeitos(b, f, [f], [st('exposed', 0.15, 999)]);
        m.aviso(b, f, 'Sem tapa-olho', f);
      },
      causa: (_m, _b, f) => (u(f).olho ? 1.45 : 1),
    },
  },
  yor: {
    nome: 'Jardim noturno',
    texto: 'A cada 12 s, uma investida silenciosa no rival com menos Vida: 120 de dano que passam por Escudo e Protegido.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'jardim', dt, 12, 8)) return;
        const a = maisFraco(m, b, f);
        if (!a) return;
        m.aviso(b, f, 'Espinho', a);
        m.dano(b, f, a, 120, false, 'Perfuração');
      },
    },
  },
  kratos: {
    nome: 'Fúria de Esparta',
    texto: 'Dar e levar golpes enche a fúria. Cheia, Kratos explode por 6 s: causa 50% a mais e cura 2% da Vida por segundo.',
    ganchos: {
      bateu(_m, _b, f, _alvo, dano) { u(f).furia = Math.min(100, (u(f).furia ?? 0) + dano / 10); },
      apanhou(_m, _b, f, _fonte, dano) { u(f).furia = Math.min(100, (u(f).furia ?? 0) + dano / 8); },
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.ate ?? 0) > b.time) { m.cura(b, f, f, f.maxHp * 0.02 * dt, 'Fúria'); return; }
        if ((s.furia ?? 0) >= 100) { s.furia = 0; s.ate = b.time + 6; m.aviso(b, f, 'Fúria de Esparta', f); }
      },
      causa: (_m, b, f) => ((u(f).ate ?? 0) > b.time ? 1.5 : 1),
    },
  },
  doomslayer: {
    nome: 'Rasgar e destroçar',
    texto: 'Quanto mais demônios, melhor: causa 10% a mais por rival de pé. Cada rival derrubado vira armadura: Escudo de 15% da Vida dele.',
    ganchos: {
      causa: (m, b, f) => 1 + 0.1 * m.rivais(b, f).length,
      caiu(m, b, f, quem, quemDerrubou) {
        if (quem.side === f.side || quemDerrubou.side !== f.side) return;
        f.shields.push({ amount: f.maxHp * 0.15, remaining: 12, source: f.uid });
        m.aviso(b, f, 'Armadura', f);
      },
    },
  },
  bowser: {
    nome: 'Rei furioso',
    texto: 'Quando um aliado cai, Bowser fica furioso e o castelo inteiro treme: 80 de dano em todos os rivais.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side) return;
        m.aviso(b, f, 'GRAAAR!', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 80, false, 'Rei furioso');
      },
    },
  },
  tuob: {
    nome: 'Pod 042',
    texto: 'O Pod atira sozinho: a cada 5 s, 22 de dano no rival mais forte, mesmo com a 2B travada.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'pod', dt, 5, 3)) return;
        const a = maisForte(m, b, f);
        if (a) m.dano(b, f, a, 22, false, 'Pod');
      },
    },
  },
  leonardo: {
    nome: 'Formação!',
    texto: 'Enquanto os três do trio estão de pé, todos recebem 12% menos dano.',
    ganchos: {
      recebe: (m, b, f) => (m.aliados(b, f).length === 3 ? 0.88 : 1),
      recebeAliado: (m, b, f) => (m.aliados(b, f).length === 3 ? 0.88 : 1),
    },
  },
  woody: {
    nome: 'Puxa a cordinha',
    texto: 'A cada 12 s, puxa a corda e sai uma frase aleatória: "Tem uma cobra na minha bota!" (rival mais forte Lento 20% por 3 s), "Alcance os céus!" (cura 8% do aliado mais ferido) ou "Você é meu parceiro" (Woody Protegido 30% por 4 s).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'corda', dt, 12, 6)) return;
        const k = Math.floor(m.sorte(b) * 3);
        if (k === 0) { const a = maisForte(m, b, f); if (a) m.efeitos(b, f, [a], [st('slow', 0.2, 3)]); m.aviso(b, f, 'Tem uma cobra na minha bota!', a ?? f); }
        else if (k === 1) { const a = maisFerido(m, b, f); if (a) m.cura(b, f, a, a.maxHp * 0.08, 'Corda'); m.aviso(b, f, 'Alcance os céus!', a ?? f); }
        else { m.efeitos(b, f, [f], [st('protected', 0.3, 4)]); m.aviso(b, f, 'Você é meu parceiro', f); }
      },
    },
  },
  gohan: {
    nome: 'Potencial despertado',
    texto: 'A raiva acorda o potencial escondido: quando um aliado cai pela primeira vez, Gohan passa a causar 60% a mais até o fim da luta.',
    ganchos: {
      caiu(m, b, f, quem) { if (quem.side === f.side && !u(f).despertou) { u(f).despertou = 1; m.aviso(b, f, 'Potencial despertado', f); } },
      causa: (_m, _b, f) => (u(f).despertou ? 1.6 : 1),
    },
  },
  ichigo: {
    nome: 'Máscara Hollow',
    texto: 'Abaixo de 40% de Vida, a máscara Hollow aparece por 8 s: age 50% mais rápido e cura 15% de todo dano que causa. Uma vez por luta.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).mascara && fracao(f) < 0.4) { u(f).mascara = b.time + 8; m.aviso(b, f, 'Máscara Hollow', f); } },
      ritmo: (_m, b, f) => ((u(f).mascara ?? 0) > b.time ? 1.5 : 1),
      bateu(m, b, f, _alvo, dano) { if ((u(f).mascara ?? 0) > b.time) m.cura(b, f, f, dano * 0.15, 'Hollow'); },
    },
  },
  denji: {
    nome: 'Puxar a corda',
    texto: 'Uma vez por luta, abaixo de 30% de Vida, puxa a corda do peito: volta a 50% da Vida na hora e fica Fortalecido 25% por 8 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).corda || fracao(f) >= 0.3) return;
        u(f).corda = 1;
        m.cura(b, f, f, f.maxHp * 0.5 - f.hp, 'Puxar a corda');
        m.efeitos(b, f, [f], [st('strengthened', 0.25, 8)]);
        m.aviso(b, f, 'Vrrrum!', f);
      },
    },
  },
  ryu: {
    nome: 'Hadouken carregado',
    texto: 'Segura o golpe para valer: a habilidade mais forte demora o dobro para sair, mas causa o triplo.',
    ganchos: {
      preparo: (_f, i) => (i === 2 ? 2 : 1),
      antes(_m, _b, f, i) { u(f).denjin = i === 2 ? 1 : 0; },
      causa: (_m, _b, f, _alvo, g) => (g.habilidade && u(f).denjin ? 3 : 1),
      usou(_m, _b, f) { u(f).denjin = 0; },
    },
  },
  shaka: {
    nome: 'Rendição dos sentidos',
    texto: 'A cada 10 s, tira um sentido do rival mais forte, nesta ordem: tato (Lento), visão (Cego), audição (Silenciado), olfato (Enfraquecido) e espírito (Paralisado 1 s).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'sentido', dt, 10, 6)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        const k = (u(f).sentido ?? 0) % 5;
        u(f).sentido = k + 1;
        const ef = [st('slow', 0.25, 6), st('blind', 0.3, 6), st('silenced', 1, 3), st('weakened', 0.2, 6), st('paralyzed', 1, 1)][k]!;
        m.efeitos(b, f, [a], [ef]);
        m.aviso(b, f, ['Tato', 'Visão', 'Audição', 'Olfato', 'Espírito'][k]!, a);
      },
    },
  },
  broly: {
    nome: 'Lendário que cresce',
    texto: 'Fica maior a cada golpe que dá: a Vida máxima sobe 3% por golpe direto (até 60%).',
    ganchos: {
      bateu(_m, _b, f, _alvo, _dano, g) {
        if (!g.direto || (u(f).cresceu ?? 0) >= 20) return;
        u(f).cresceu = (u(f).cresceu ?? 0) + 1;
        const extra = f.maxHp * 0.03;
        f.maxHp += extra; f.hp += extra;
      },
    },
  },
  finn: {
    nome: 'Herói',
    texto: 'Protege os pequenos: quando um aliado abaixo de 30% de Vida leva um golpe, Finn Provoca quem bateu (3 s) e puxa a briga para si.',
    ganchos: {
      viu(m, b, f, fonte, alvo, _dano, g) {
        if (!g.direto || alvo === f || alvo.side !== f.side || fracao(alvo) >= 0.3 || fonte.side === f.side || !vivo(fonte)) return;
        if ((u(f).heroi ?? 0) > b.time) return;
        u(f).heroi = b.time + 4;
        m.efeitos(b, f, [fonte], [st('provoked', 1, 3)]);
        m.aviso(b, f, 'Ei, briga comigo!', fonte);
      },
    },
  },
  donald: {
    nome: 'Ataque de nervos',
    texto: 'A cada 3 golpes que leva, perde a paciência: três golpes rápidos de 40 em quem bateu por último.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.direto || fonte.side === f.side) return;
        u(f).paciencia = (u(f).paciencia ?? 0) + 1;
        if (u(f).paciencia! % 3 || !vivo(fonte)) return;
        m.aviso(b, f, 'QUAAACK!', fonte);
        for (let i = 0; i < 3 && vivo(fonte); i++) m.dano(b, f, fonte, 40, false, 'Ataque de nervos');
      },
    },
  },
  tom: {
    nome: 'Lógica de desenho',
    texto: 'Gato de desenho não morre: uma vez por luta, ao cair, volta 6 s depois achatado, com 20% da Vida.',
    ganchos: { morreu(m, b, f) { if (!f.voltou && !u(f).achatado) { u(f).achatado = 1; f.renascendo = 6; m.aviso(b, f, 'Achatado…', f); } } },
  },
  billcipher: {
    nome: 'Acordo',
    texto: 'No começo, faz um acordo com o rival mais forte: os dois causam 30% a mais… mas a letra miúda diz que esse rival recebe o dobro do dano de Bill.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).acordo = idx(b, a); m.efeitos(b, f, [a], [st('strengthened', 0.3, 999)]); m.aviso(b, f, 'Temos um acordo', a); } },
      causa: (_m, b, f, alvo) => 1.3 * (u(f).acordo === idx(b, alvo) ? 2 : 1),
    },
  },
  rukia: {
    nome: 'Dança branca',
    texto: 'As habilidades dela Congelam por 1 s todos os rivais que estão Lentos.',
    ganchos: {
      usou(m, b, f) {
        const lentos = m.rivais(b, f).filter((r) => m.intensidade(r, 'slow') > 0);
        if (!lentos.length) return;
        m.efeitos(b, f, lentos, [st('frozen', 0.2, 1)]);
        m.aviso(b, f, 'Dança branca', lentos[0]);
      },
    },
  },
  punisher: {
    nome: 'Interrogatório',
    texto: 'A cada 12 s, pega o rival mais ferido: ele perde 20 de Carga em todas as habilidades.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'interroga', dt, 12, 8)) return;
        const a = m.rivais(b, f).sort((x, y) => fracao(x) - fracao(y))[0];
        if (!a) return;
        for (const s of a.skills) s.charge = Math.max(0, s.charge - 20);
        m.aviso(b, f, 'Fala!', a);
      },
    },
  },
  aquaman: {
    nome: 'Marés',
    texto: 'A cada 10 s a maré vira: na cheia, o trio cura 3% da Vida; na vazante, os rivais ficam Lentos 10% por 5 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'mare', dt, 10, 5)) return;
        const cheia = (u(f).mare = ((u(f).mare ?? 1) + 1) % 2) === 0;
        if (cheia) for (const a of m.aliados(b, f)) m.cura(b, f, a, a.maxHp * 0.03, 'Maré cheia');
        else m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.1, 5)]);
        m.aviso(b, f, cheia ? 'Maré cheia' : 'Maré vazante', f);
      },
    },
  },
  ganondorf: {
    nome: 'Triforce do Poder',
    texto: 'Ninguém derruba Ganondorf de uma vez: enquanto ele tiver mais de metade da Vida, nenhum golpe o leva abaixo de 1.',
    ganchos: { salva: (_m, _b, f, alvo, dano) => (alvo === f && f.hp > f.maxHp * 0.5 && dano >= f.hp ? 1 : null) },
  },
  subzero: {
    nome: 'Fatality congelante',
    texto: 'Rival Congelado abaixo de 25% de Vida que Sub-Zero acertar é estilhaçado: cai na hora.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo) || fracao(alvo) >= 0.25 || m.intensidade(alvo, 'frozen') <= 0 && !u(f)[`gelo${idx(b, alvo)}`]) return;
        m.aviso(b, f, 'Fatality', alvo);
        m.dano(b, f, alvo, alvo.hp + 1, false, 'Fatality');
      },
      causa(m, b, f, alvo) { u(f)[`gelo${idx(b, alvo)}`] = m.intensidade(alvo, 'frozen') > 0 ? 1 : 0; return 1; },
    },
  },
  frozone: {
    nome: 'Rampa de gelo',
    texto: 'Enquanto algum rival estiver Lento, Gelado escorrega pelas rampas: o trio dele age 12% mais rápido.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0)) return;
        for (const a of m.aliados(b, f)) if (a !== f) a.action = Math.min(1, a.action + dt * 0.035);
      },
      ritmo: (m, b, f) => (m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0) ? 1.12 : 1),
    },
  },
  cartman: {
    nome: 'Chantagem',
    texto: 'A cada 15 s chantageia o rival mais forte: por 5 s, esse rival não consegue machucar Cartman.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'chantagem', dt, 15, 6)) { const a = maisForte(m, b, f); if (a) { u(f).chantagem = idx(b, a); u(f).ate = b.time + 5; m.aviso(b, f, 'Chantagem', a); } } },
      recebe: (_m, b, f, fonte) => ((u(f).ate ?? 0) > b.time && u(f).chantagem === idx(b, fonte) ? 0 : 1),
    },
  },
  beerus: {
    nome: 'Hakai',
    texto: 'Uma vez por luta, aos 20 s, apaga tudo que protege os rivais: todos perdem Escudo, buffs e criaturas invocadas.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).hakai || b.time < 20) return;
        u(f).hakai = 1;
        for (const r of m.rivais(b, f)) { r.shields = []; r.statuses = r.statuses.filter((s) => !BONS.includes(s.id)); }
        m.aviso(b, f, 'Hakai', f);
      },
    },
  },
  scooby: {
    nome: 'Scooby-lanche',
    texto: 'Medroso: tem 25% de Esquiva o tempo todo. A cada 15 s ganha um Scooby-lanche e fica corajoso: causa 40% a mais por 5 s.',
    ganchos: {
      inicio(m, b, f) { m.efeitos(b, f, [f], [st('evasion', 0.25, 999)]); },
      passo(m, b, f, dt) { if (relogio(f, 'lanche', dt, 15, 8)) { u(f).lanche = b.time + 5; m.aviso(b, f, 'Scooby-lanche!', f); } },
      causa: (_m, b, f) => ((u(f).lanche ?? 0) > b.time ? 1.4 : 1),
    },
  },
  pateta: {
    nome: 'Desastrado',
    texto: '1 em 4 golpes dele vira acidente: sai com o dobro da força, mas Pateta também se machuca com 10% do golpe. Ai-ai-ai!',
    ganchos: {
      causa(m, b, f, _alvo, g) { if (!g.direto) return 1; u(f).acidente = m.sorte(b) < 0.25 ? 1 : 0; return u(f).acidente ? 2 : 1; },
      bateu(m, b, f, _alvo, dano) { if (!u(f).acidente) return; u(f).acidente = 0; f.hp = Math.max(1, f.hp - dano * 0.1); m.aviso(b, f, 'Ai-ai-ai!', f); },
    },
  },
  bebop: {
    nome: 'Atropelo',
    texto: 'Quanto menos ação o rival tem guardada, mais forte o atropelo: até 50% a mais em quem acabou de agir.',
    ganchos: { causa: (_m, _b, _f, alvo, g) => (g.direto ? 1 + 0.5 * (1 - alvo.action) : 1) },
  },
  stewie: {
    nome: 'Raio de encolher',
    texto: 'A cada 12 s, encolhe o rival mais forte por 8 s: ele causa 30% menos e perde 15% da Vida máxima enquanto estiver pequeno.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f), alvo = b.fighters[s.encolhido ?? -1];
        if (alvo && (s.ate ?? 0) <= b.time && s.encolhido !== -1) { alvo.maxHp = s.vidaDele!; s.encolhido = -1; }
        if (!relogio(f, 'raio', dt, 12, 6)) return;
        const a = maisForte(m, b, f);
        if (!a || s.encolhido === idx(b, a)) return;
        s.encolhido = idx(b, a); s.ate = b.time + 8; s.vidaDele = a.maxHp;
        a.maxHp = Math.round(a.maxHp * 0.85); a.hp = Math.min(a.hp, a.maxHp);
        m.efeitos(b, f, [a], [st('weakened', 0.3, 8)]);
        m.aviso(b, f, 'Encolhido!', a);
      },
    },
  },
  frieza: {
    nome: 'Crueldade',
    texto: 'Gosta de bater em quem já está sofrendo: causa 30% a mais em rivais com algum Status ruim.',
    ganchos: { causa: (_m, _b, _f, alvo) => (temRuim(alvo) ? 1.3 : 1) },
  },
  carnage: {
    nome: 'Explosão de lâminas',
    texto: 'Cada vez que derruba um rival, o simbionte explode em lâminas: 80 de dano em todos os rivais que sobraram.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        m.aviso(b, f, 'Carnificina', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 80, false, 'Lâminas');
      },
    },
  },
  sukuna: {
    nome: 'Santuário malevolente',
    texto: 'A cada 15 s abre o santuário: por 3 s, todos os rivais levam 20 de dano por segundo, cortados sem parar.',
    ganchos: {
      passo(m, b, f, dt) {
        if ((u(f).santuario ?? 0) > b.time) { for (const r of m.rivais(b, f)) m.dano(b, f, r, 20 * dt, false, 'Santuário'); return; }
        if (relogio(f, 'dominio', dt, 15, 9)) { u(f).santuario = b.time + 3; m.aviso(b, f, 'Santuário malevolente', f); }
      },
    },
  },
  zeromm: {
    nome: 'Raikousen',
    texto: 'A cada 3 habilidades, a próxima sai na hora (sem Preparo) e deixa o alvo Eletrificado.',
    ganchos: {
      usou(m, b, f) {
        if (u(f).raiko) { u(f).raiko = 0; const a = maisForte(m, b, f); if (a) m.efeitos(b, f, [a], [st('electric', 0.3, 4)]); m.aviso(b, f, 'Raikousen', a ?? f); return; }
        u(f).usos = (u(f).usos ?? 0) + 1;
        if (u(f).usos! % 3 === 0) u(f).raiko = 1;
      },
      preparo: (f) => (u(f).raiko ? 0 : 1),
    },
  },
};
