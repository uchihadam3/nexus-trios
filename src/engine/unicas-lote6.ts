/*
 * Mecânicas únicas — lote 6: os antigos que mais se pareciam com alguém.
 */
import { curaContinua, fracao, maisFerido, maisForte, quandoVira, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
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
    texto: 'O primeiro golpe de Levi Ackerman em cada rival causa o dobro de dano.',
    ganchos: {
      causa(_m, b, f, alvo, g) {
        if (!g.direto || u(f)[`nuca${idx(b, alvo)}`]) return 1;
        u(f)[`nuca${idx(b, alvo)}`] = 1;
        return 2;
      },
      bateu(m, b, f, alvo, _dano, g) {
        const k = `nucaAviso${idx(b, alvo)}`;
        if (g.direto && u(f)[`nuca${idx(b, alvo)}`] && !u(f)[k]) { u(f)[k] = 1; m.aviso(b, f, 'Corte na nuca', alvo); }
      },
    },
  },
  kurapika: {
    nome: 'Corrente do julgamento',
    texto: 'No começo da luta, Kurapika faz um juramento contra o rival com mais Vida: +60% de dano nesse rival. Enquanto esse rival estiver de pé, cada golpe de Kurapika em outro rival custa 4% da Vida máxima de Kurapika (sem cair por isso).',
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
    texto: '1 vez por luta: quando algum rival fica Paralisado, Dio Brando joga o Road Roller nele: 250 de dano.',
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
    texto: 'Cada rival derrubado pelo trio de Makima luta ao lado de Makima por 10 s: Invocação que ataca um rival a cada 1,5 s com 45 de dano por ataque.',
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
    texto: 'Com menos de 30% da Vida, Albert Wesker recupera 3% da Vida máxima por segundo, mas o ataque básico de Wesker vai em rivais aleatórios.',
    ganchos: {
      passo(m, b, f, dt) { if (fracao(f) < 0.3) { if (!u(f).virus) { u(f).virus = 1; m.aviso(b, f, 'Uroboros', f); } curaContinua(m, b, f, f, f.maxHp * 0.03 * dt, 'Uroboros'); } },
      alvoDoBasico(m, b, f) { if (fracao(f) >= 0.3) return undefined; const rs = m.rivais(b, f); return rs[Math.floor(m.sorte(b) * rs.length)]; },
    },
  },
  shadowhh: {
    nome: 'Sem inibidores',
    texto: 'Com menos de 40% da Vida, Shadow tira os inibidores até o fim da luta: +50% de dano. Enquanto estiver com menos de 40% da Vida, Shadow perde 1,5% da Vida máxima por segundo (sem cair por isso).',
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
    texto: 'Depois de Renascer, Ikki causa +35% de dano e age 15% mais rápido até o fim da luta.',
    ganchos: {
      passo(m, b, f) { if (f.voltou && !u(f).fenix) { u(f).fenix = 1; m.aviso(b, f, 'A Fênix voltou mais forte', f); } },
      causa: (_m, _b, f) => (u(f).fenix ? 1.35 : 1),
      ritmo: (_m, _b, f) => (u(f).fenix ? 1.15 : 1),
    },
  },
  mummra: {
    nome: 'Sempre vivo',
    texto: 'Cada aliado de Mumm-Ra que cai: Mumm-Ra ganha +20% de Vida máxima e cura esse mesmo tanto.',
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
    texto: 'A cada 8 s, Tanjiro Kamado sente o fio da abertura: o próximo golpe de Tanjiro quebra todo o Escudo do alvo e ignora o Protegido desse rival.',
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
    texto: 'Cada segundo que Frieren passa sem usar habilidade soma +5% de dano na próxima habilidade (até +60%, com 12 s).',
    ganchos: {
      passo(_m, _b, f, dt) { u(f).mana = Math.min(12, (u(f).mana ?? 0) + dt); },
      causa: (_m, _b, f, _alvo, g) => (g.habilidade ? 1 + 0.05 * (u(f).mana ?? 0) : 1),
      usou(_m, _b, f) { u(f).mana = 0; },
    },
  },
  loki: {
    nome: 'Era uma ilusão',
    texto: '1 vez por luta: quando ia cair, Loki revela que era uma ilusão. Loki volta na hora com 30% da Vida máxima, e o rival que derrubou Loki fica Confuso por 3 s.',
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
    texto: 'Cada segundo que Vergil passa sem levar ataque nem habilidade soma +3% de dano (até +45%, com 15 s). Levar um golpe zera esse bônus.',
    ganchos: {
      passo(_m, _b, f, dt) { u(f).foco = Math.min(15, (u(f).foco ?? 0) + dt); },
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).foco = 0; },
      causa: (_m, _b, f) => 1 + 0.03 * (u(f).foco ?? 0),
    },
  },
  ezio: {
    nome: 'Um atrás do outro',
    texto: 'Quando Ezio Auditore derruba um rival, ataca de novo na hora (se ainda houver rival de pé).',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side || !m.rivais(b, f).length) return;
        f.action = 1;
        m.aviso(b, f, 'Próximo', f);
      },
    },
  },
  isaac: {
    nome: 'Corte no lento',
    texto: 'Isaac Clarke causa +40% de dano em quem está Lento.',
    ganchos: { causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'slow') > 0 ? 1.4 : 1) },
  },
  saga: {
    nome: 'Lado bom, lado mau',
    texto: 'A cada 15 s, Saga de Gêmeos troca de lado, começando pelo bom. Lado bom: todo o trio de Saga fica Protegido (−10% de dano recebido) por 15 s. Lado mau: Saga causa +20% de dano, e todos os rivais ficam Enfraquecido (−6% de dano) por 15 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'vontade', dt, 15, 0.1)) return;
        const mau = (u(f).lado = ((u(f).lado ?? 1) + 1) % 2) === 1;
        if (mau) m.efeitos(b, f, m.rivais(b, f), [st('weakened', 0.06, 15)]);
        else m.efeitos(b, f, m.aliados(b, f), [st('protected', 0.1, 15)]);
        m.aviso(b, f, mau ? 'Lado mau' : 'Lado bom', f);
      },
      causa: (_m, _b, f) => (u(f).lado === 1 ? 1.2 : 1),
    },
  },
  docinho: {
    nome: 'Briguenta',
    texto: 'Cada golpe que Docinho leva soma +5% de dano (até +50%). Quando Docinho usa Explosão verde, gasta toda essa raiva e o bônus zera.',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).raiva = Math.min(10, (u(f).raiva ?? 0) + 1); },
      causa: (_m, _b, f) => 1 + 0.05 * (u(f).raiva ?? 0),
      usou(_m, _b, f, i) { if (i === 2) u(f).raiva = 0; },
    },
  },
  caseyjones: {
    nome: 'Taco na cabeça',
    texto: 'A cada 5 golpes de Casey Jones, o alvo perde toda a barra do Próximo ataque.',
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
    texto: 'Cheetara age 35% mais rápido, mas a cada 20 s perde o fôlego e fica 2 s parada.',
    ganchos: {
      ritmo: () => 1.35,
      passo(m, b, f, dt) { if (relogio(f, 'folego', dt, 20, 20)) { u(f).folego = b.time + 2; m.aviso(b, f, 'Sem fôlego', f); } },
      parado: (f, b) => (u(f).folego ?? 0) > b.time,
    },
  },
  yusuke: {
    nome: 'Briga de rua',
    texto: 'Yusuke Urameshi causa +40% de dano em quem acertou Yusuke nos últimos 3 s.',
    ganchos: {
      apanhou(_m, b, f, fonte, _dano, g) { if (g.direto) u(f)[`troco${idx(b, fonte)}`] = b.time + 3; },
      causa: (_m, b, f, alvo) => ((u(f)[`troco${idx(b, alvo)}`] ?? 0) > b.time ? 1.4 : 1),
    },
  },
  sailormoon: {
    nome: 'Poder do amor',
    texto: '1 vez por luta: quando um aliado cai (e não vai Renascer), Sailor Moon usa o Cristal de Prata: esse aliado volta com 50% da Vida máxima, e Sailor Moon perde metade da Vida que tem.',
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
    nome: 'Medo contagiante',
    texto: 'Cada vez que Coragem leva de uma vez 15% da Vida máxima ou mais, Coragem grita: todos os rivais ficam Lento (20% mais lento) por 2 s.',
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
    texto: 'Com menos de 50% da Vida (1 vez por luta), Kenpachi Zaraki tira o tapa-olho até o fim da luta: +45% de dano, mas fica Exposto (+15% de dano recebido).',
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
    nome: 'Golpe na mais fraca',
    texto: 'A cada 12 s, Yor Forger crava um espinho no rival com menos Vida: 120 de dano, ignorando Escudo e Protegido.',
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
    texto: 'Dar golpes e levar golpes enche a Fúria de Kratos. Com a Fúria cheia: por 6 s, Kratos causa +50% de dano e cura 2% da Vida máxima por segundo; depois a Fúria zera.',
    ganchos: {
      bateu(_m, _b, f, _alvo, dano) { u(f).furia = Math.min(100, (u(f).furia ?? 0) + dano / 10); },
      apanhou(_m, _b, f, _fonte, dano) { u(f).furia = Math.min(100, (u(f).furia ?? 0) + dano / 8); },
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.ate ?? 0) > b.time) { curaContinua(m, b, f, f, f.maxHp * 0.02 * dt, 'Fúria'); return; }
        if ((s.furia ?? 0) >= 100) { s.furia = 0; s.ate = b.time + 6; m.aviso(b, f, 'Fúria de Esparta', f); }
      },
      causa: (_m, b, f) => ((u(f).ate ?? 0) > b.time ? 1.5 : 1),
    },
  },
  doomslayer: {
    nome: 'Rasgar e destroçar',
    texto: 'Doom Slayer causa +10% de dano para cada rival de pé (com os 3: +30%). Cada rival derrubado pelo trio de Doom Slayer dá a Doom Slayer Escudo de 15% da Vida máxima dele por 12 s.',
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
    texto: 'Quando um aliado de Bowser cai: 80 de dano em cada rival.',
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
    texto: 'A cada 5 s, o Pod 042 causa 22 de dano no rival com mais Vida, mesmo com a 2B parada.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'pod', dt, 5, 3)) return;
        const a = maisForte(m, b, f);
        if (a) { m.aviso(b, f, 'Pod 042', a); m.dano(b, f, a, 22, false, 'Pod'); }
      },
    },
  },
  leonardo: {
    nome: 'Trio unido',
    texto: 'Enquanto os 3 do trio de Leonardo estiverem de pé, todos do trio recebem −12% de dano.',
    ganchos: {
      inicio(m, b, f) { m.aviso(b, f, 'Trio unido', f); },
      recebe: (m, b, f) => (m.aliados(b, f).length === 3 ? 0.88 : 1),
      recebeAliado: (m, b, f) => (m.aliados(b, f).length === 3 ? 0.88 : 1),
    },
  },
  woody: {
    nome: 'Puxa a cordinha',
    texto: 'A cada 12 s, Woody puxa a cordinha e sorteia (33% de chance cada): o rival com mais Vida fica Lento (20% mais lento) por 3 s; o aliado mais ferido cura 8% da Vida máxima; ou Woody fica Protegido (−30% de dano recebido) por 4 s.',
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
    nome: 'Fúria pelo amigo',
    texto: 'Quando um aliado de Gohan cai, Gohan desperta: +60% de dano até o fim da luta.',
    ganchos: {
      caiu(m, b, f, quem) { if (quem.side === f.side && !u(f).despertou) { u(f).despertou = 1; m.aviso(b, f, 'Potencial despertado', f); } },
      causa: (_m, _b, f) => (u(f).despertou ? 1.6 : 1),
    },
  },
  ichigo: {
    nome: 'Hollow interior',
    texto: 'Com menos de 40% da Vida (1 vez por luta): por 8 s, Ichigo Kurosaki age 50% mais rápido e cura 15% do dano que causa.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).mascara && fracao(f) < 0.4) { u(f).mascara = b.time + 8; m.aviso(b, f, 'Máscara Hollow', f); } },
      ritmo: (_m, b, f) => ((u(f).mascara ?? 0) > b.time ? 1.5 : 1),
      bateu(m, b, f, _alvo, dano) { if ((u(f).mascara ?? 0) > b.time) m.cura(b, f, f, dano * 0.15, 'Hollow'); },
    },
  },
  denji: {
    nome: 'Coração de motosserra',
    texto: 'Com menos de 30% da Vida (1 vez por luta): Denji puxa a corda, volta a 50% da Vida e fica Fortalecido (+25% de dano) por 8 s.',
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
    texto: 'O Shinku Hadouken de Ryu demora o dobro do Preparo para sair, mas causa o triplo de dano.',
    ganchos: {
      preparo: (_f, i) => (i === 2 ? 2 : 1),
      antes(_m, _b, f, i) { u(f).denjin = i === 2 ? 1 : 0; },
      causa: (_m, _b, f, _alvo, g) => (g.habilidade && u(f).denjin ? 3 : 1),
      usou(_m, _b, f) { u(f).denjin = 0; },
    },
  },
  shaka: {
    nome: 'Rendição dos sentidos',
    texto: 'A cada 10 s, Shaka de Virgem tira um sentido do rival com mais Vida, nesta ordem: Lento (25% mais lento) por 6 s; Cego (30% de chance de errar o ataque básico) por 6 s; Silenciado por 3 s; Enfraquecido (−20% de dano) por 6 s; Paralisado por 1 s.',
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
    texto: 'Cada golpe de Broly dá +3% de Vida máxima (até 20 golpes: cerca de +80%).',
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
    texto: 'Quando um rival acerta um aliado de Finn que está com menos de 30% da Vida, esse rival fica Provocado (só mira em Finn) por 3 s (no máximo 1 vez a cada 4 s).',
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
    texto: 'A cada 3 golpes que o Pato Donald leva, perde a paciência: 3 golpes de 40 de dano em quem bateu por último.',
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
    texto: 'Quando cai (1 vez por luta), Tom volta 6 s depois com 30% da Vida máxima.',
    ganchos: { morreu(m, b, f) { if (!f.voltou && !u(f).achatado) { u(f).achatado = 1; f.renascendo = 6; m.aviso(b, f, 'Achatado…', f); } } },
  },
  billcipher: {
    nome: 'Pacto perigoso',
    texto: 'Bill Cipher causa +30% de dano. No começo da luta, Bill faz um acordo com o rival com mais Vida: esse rival fica Fortalecido (+30% de dano) até o fim da luta, mas recebe o dobro de dano de Bill.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).acordo = idx(b, a); m.efeitos(b, f, [a], [st('strengthened', 0.3, 999)]); m.aviso(b, f, 'Temos um acordo', a); } },
      causa: (_m, b, f, alvo) => 1.3 * (u(f).acordo === idx(b, alvo) ? 2 : 1),
    },
  },
  rukia: {
    nome: 'Dança branca',
    texto: 'Cada habilidade de Rukia Kuchiki deixa Congelado (+20% de dano no golpe que quebra o gelo) por 1 s todo rival que estiver Lento.',
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
    texto: 'A cada 12 s, o Justiceiro interroga o rival mais ferido: esse rival perde 20% de Carga em todas as habilidades.',
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
    texto: 'A cada 10 s, a maré de Aquaman muda, começando pela cheia. Maré cheia: todo o trio cura 3% da Vida máxima. Maré vazante: todos os rivais ficam Lento (10% mais lento) por 5 s.',
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
    nome: 'Poder inabalável',
    texto: 'Com mais de 10% da Vida, nenhum golpe derruba Ganondorf: o golpe que derrubaria deixa Ganondorf com 1 de Vida.',
    ganchos: {
      salva(m, b, f, alvo, dano) {
        if (alvo !== f || f.hp <= f.maxHp * 0.1 || dano < f.hp) return null;
        m.aviso(b, f, 'Poder inabalável', f);
        return 1;
      },
    },
  },
  subzero: {
    nome: 'Fatality congelante',
    texto: 'Quando Sub-Zero acerta um rival Congelado com menos de 25% da Vida, esse rival cai na hora.',
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
    nome: 'Pista escorregadia',
    texto: 'Enquanto algum rival estiver Lento, Gelado age 12% mais rápido, e os aliados de Gelado também agem mais rápido.',
    ganchos: {
      passo(m, b, f, dt) {
        const pista = m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0);
        quandoVira(m, b, f, 'pista', pista, 'Pista escorregadia', f);
        if (!pista) return;
        for (const a of m.aliados(b, f)) if (a !== f) a.action = Math.min(1, a.action + dt * 0.035);
      },
      ritmo: (m, b, f) => (m.rivais(b, f).some((r) => m.intensidade(r, 'slow') > 0) ? 1.12 : 1),
    },
  },
  cartman: {
    nome: 'Ninguém mexe comigo',
    texto: 'A cada 15 s, Eric Cartman chantageia o rival com mais Vida: por 5 s, esse rival não causa dano em Cartman.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'chantagem', dt, 15, 6)) { const a = maisForte(m, b, f); if (a) { u(f).chantagem = idx(b, a); u(f).ate = b.time + 5; m.aviso(b, f, 'Chantagem', a); } } },
      recebe: (_m, b, f, fonte) => ((u(f).ate ?? 0) > b.time && u(f).chantagem === idx(b, fonte) ? 0 : 1),
    },
  },
  beerus: {
    nome: 'Apagar os bônus',
    texto: 'Aos 20 s de luta (1 vez por luta), Beerus usa o Hakai: todos os rivais perdem o Escudo e todos os Status bons (inclusive Invocação).',
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
    nome: 'Coragem de biscoito',
    texto: 'Scooby-Doo tem Esquiva (25% de chance de desviar) a luta toda. A cada 15 s, Scooby come um Scooby-lanche: +40% de dano por 5 s.',
    ganchos: {
      inicio(m, b, f) { m.efeitos(b, f, [f], [st('evasion', 0.25, 999)]); },
      passo(m, b, f, dt) { if (relogio(f, 'lanche', dt, 15, 8)) { u(f).lanche = b.time + 5; m.aviso(b, f, 'Scooby-lanche!', f); } },
      causa: (_m, b, f) => ((u(f).lanche ?? 0) > b.time ? 1.4 : 1),
    },
  },
  pateta: {
    nome: 'Desastrado',
    texto: 'Cada golpe do Pateta tem 25% de chance de virar acidente: o golpe causa o dobro de dano, mas o Pateta perde 10% desse dano em Vida (sem cair por isso).',
    ganchos: {
      causa(m, b, f, _alvo, g) { if (!g.direto) return 1; u(f).acidente = m.sorte(b) < 0.25 ? 1 : 0; return u(f).acidente ? 2 : 1; },
      bateu(m, b, f, _alvo, dano) { if (!u(f).acidente) return; u(f).acidente = 0; f.hp = Math.max(1, f.hp - dano * 0.1); m.aviso(b, f, 'Ai-ai-ai!', f); },
    },
  },
  bebop: {
    nome: 'Pega desprevenido',
    texto: 'Bebop causa até +50% de dano em quem acabou de agir: quanto mais vazia a barra do Próximo ataque do alvo, maior o bônus.',
    ganchos: { causa: (_m, _b, _f, alvo, g) => (g.direto ? 1 + 0.5 * (1 - alvo.action) : 1) },
  },
  stewie: {
    nome: 'Raio de encolher',
    texto: 'A cada 12 s, Stewie Griffin encolhe o rival com mais Vida por 8 s: esse rival perde 15% da Vida máxima e fica Enfraquecido (−30% de dano).',
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
    nome: 'Prazer no sofrimento',
    texto: 'Freeza causa +30% de dano em rivais com algum Status ruim.',
    ganchos: { causa: (_m, _b, _f, alvo) => (temRuim(alvo) ? 1.3 : 1) },
  },
  carnage: {
    nome: 'Explosão de lâminas',
    texto: 'Quando Carnificina derruba um rival: 80 de dano em cada outro rival.',
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
    texto: 'A cada 15 s, Ryomen Sukuna abre o Santuário malevolente: por 3 s, cada rival perde 20 de Vida por segundo.',
    ganchos: {
      passo(m, b, f, dt) {
        if ((u(f).santuario ?? 0) > b.time) { for (const r of m.rivais(b, f)) m.dano(b, f, r, 20 * dt, false, 'Santuário'); return; }
        if (relogio(f, 'dominio', dt, 15, 9)) { u(f).santuario = b.time + 3; m.aviso(b, f, 'Santuário malevolente', f); }
      },
    },
  },
  zeromm: {
    nome: 'Raio a cada três',
    texto: 'A cada 3 habilidades de Zero, a próxima sai sem Preparo e deixa o rival com mais Vida Eletrificado (−18% da barra por golpe) por 4 s.',
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
