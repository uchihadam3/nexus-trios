/*
 * Mecânicas únicas — lote 8: os clássicos que faltavam (Vegeta, Naruto, Luffy,
 * Gojo, Batman, Thanos, Itachi, os X-Men…).
 */
import { fracao, maisFerido, maisForte, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import type { Battle, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
/** Um número curto para o nome do golpe (a adaptação do Megumi lembra cada tipo de golpe). */
const marca = (label: string) => { let h = 0; for (const c of label) h = (h * 31 + c.charCodeAt(0)) % 9973; return `golpe${h}`; };
/** O que a Joia da Mente do Visão limpa. */
const MENTE: StatusId[] = ['confused', 'sleep', 'silenced'];
/** Quanto de Vida (em frações somadas) um lado ainda tem. */
const vidaDoLado = (b: Battle, lado: string) => b.fighters.filter((x) => x.side === lado).reduce((n, x) => n + Math.max(0, fracao(x)), 0);

export const LOTE8: Record<string, Unica> = {
  vegeta: {
    nome: 'Zenkai e orgulho',
    texto: 'Cada surra deixa o saiyajin mais forte: a primeira vez abaixo de 50% e de 25% da Vida, a Vida máxima sobe 4% e o dano, 4%. Orgulhoso, a cura dos aliados vale metade nele.',
    ganchos: {
      apanhou(m, b, f) {
        for (const [k, lim] of [['z50', 0.5], ['z25', 0.25]] as const) {
          if (u(f)[k] || fracao(f) >= lim) continue;
          u(f)[k] = 1; u(f).zenkai = (u(f).zenkai ?? 0) + 1;
          f.maxHp *= 1.04; // sobe o teto, não cura (não briga com a Última resistência)
          m.aviso(b, f, 'Zenkai!', f);
        }
      },
      causa: (_m, _b, f) => 1 + 0.04 * (u(f).zenkai ?? 0),
      curaRecebida: (_m, _b, f, fonte) => (fonte === f ? 1 : 0.5),
    },
  },
  naruto: {
    nome: 'Exército de clones',
    texto: 'A cada 12 s faz um clone das sombras (até 2). Cada clone bate junto no ataque básico, com 15%. Um golpe direto nele estoura um clone e faz só metade.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'clone', dt, 12, 4) && (u(f).clones ?? 0) < 2) { u(f).clones = (u(f).clones ?? 0) + 1; m.aviso(b, f, 'Kage Bunshin', f, u(f).clones); } },
      bateu(m, b, f, alvo, dano, g) { if (g.direto && !g.habilidade && (u(f).clones ?? 0) > 0 && vivo(alvo)) m.dano(b, f, alvo, dano * 0.15 * u(f).clones!, false, 'Clones'); },
      recebe(_m, _b, f, _fonte, g) { if (!g.direto || !(u(f).clones ?? 0)) return 1; u(f).clones! -= 1; return 0.5; },
    },
  },
  luffy: {
    nome: 'Corpo de borracha',
    texto: 'Soco não machuca borracha: ataques básicos dos rivais fazem 30% a menos nele, e 15% do golpe volta quicando em quem bateu.',
    ganchos: {
      recebe: (_m, _b, _f, _fonte, g) => (g.direto && !g.habilidade ? 0.7 : 1),
      apanhou(m, b, f, fonte, dano, g) { if (g.direto && !g.habilidade && vivo(fonte)) m.dano(b, f, fonte, dano * 0.21, false, 'Borracha'); },
    },
  },
  gojo: {
    nome: 'Expansão de Domínio',
    texto: 'Quando o Vazio Infinito sai, os rivais se afogam em informação: perdem metade da barra de ação e ficam Silenciados por 2 s.',
    ganchos: {
      usou(m, b, f, i) {
        if (i !== 2) return;
        const rs = m.rivais(b, f);
        m.aviso(b, f, 'Vazio Infinito', f);
        for (const r of rs) r.action *= 0.5;
        m.efeitos(b, f, rs, [st('silenced', 1, 2)]);
      },
    },
  },
  pikachu: {
    nome: 'Bochechas elétricas',
    texto: 'As bochechas guardam eletricidade: cada golpe que dá ou leva enche 1. Com 8, descarrega sozinho: 60 de dano no rival mais forte, que fica Eletrificado.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) { if (g.direto) bochecha(m, b, f); },
      apanhou(m, b, f, _fonte, _dano, g) { if (g.direto) bochecha(m, b, f); },
    },
  },
  saitama: {
    nome: 'Tédio do herói',
    texto: 'Começa entediado: causa 25% a menos. Depois de levar 4 golpes, a luta finalmente fica séria: causa 40% a mais até o fim.',
    ganchos: {
      apanhou(m, b, f, _fonte, _dano, g) {
        if (!g.direto || (u(f).serio ?? 0) >= 4) return;
        u(f).serio = (u(f).serio ?? 0) + 1;
        if (u(f).serio === 4) m.aviso(b, f, 'Modo sério', f);
      },
      causa: (_m, _b, f) => ((u(f).serio ?? 0) >= 4 ? 1.4 : 0.75),
    },
  },
  wolverine: {
    nome: 'Fator de cura',
    texto: 'O corpo fecha cada ferida: 3 s depois de levar um golpe, recupera 25% do dano daquele golpe.',
    ganchos: {
      apanhou(_m, b, f, _fonte, dano) {
        // guarda até duas feridas fechando (a mais nova soma na segunda)
        if (!u(f).f1) { u(f).f1 = dano; u(f).t1 = b.time + 3; } else { u(f).f2 = (u(f).f2 ?? 0) + dano; u(f).t2 ??= b.time + 3; }
      },
      passo(m, b, f) {
        if (u(f).f1 && b.time >= u(f).t1!) {
          m.cura(b, f, f, u(f).f1! * 0.25, 'Fator de cura');
          u(f).f1 = u(f).f2 ?? 0; u(f).t1 = u(f).t2 ?? 0; u(f).f2 = 0; delete u(f).t2;
        }
      },
    },
  },
  batman: {
    nome: 'Cinto de utilidades',
    texto: 'A cada 16 s tira do cinto o que a hora pede: gancho (Escudo de 10% num aliado abaixo de 30% da Vida), bomba de fumaça (se o trio está perdendo, Cega os rivais por 1,5 s) ou batarangue (40 de dano em quem prepara habilidade).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'cinto', dt, 16, 8)) return;
        const ferido = maisFerido(m, b, f);
        if (ferido && fracao(ferido) < 0.3) { m.aviso(b, f, 'Gancho', ferido); ferido.shields.push({ amount: ferido.maxHp * 0.1, remaining: 10, source: f.uid }); return; }
        const rs = m.rivais(b, f);
        if (vidaDoLado(b, f.side) < vidaDoLado(b, f.side === 'player' ? 'enemy' : 'player')) { m.aviso(b, f, 'Bomba de fumaça', f); m.efeitos(b, f, rs, [st('blind', 0.3, 1.5)]); return; }
        const r = rs.find((x) => x.cast) ?? maisForte(m, b, f);
        if (r) { m.aviso(b, f, 'Batarangue', r); m.dano(b, f, r, 40, false, 'Batarangue'); }
      },
    },
  },
  superman: {
    nome: 'Sopro congelante',
    texto: 'A cada 12 s enche o peito e sopra: todos os rivais perdem 30% da barra de ação, e o fogo no trio dele se apaga (sai o Queimando).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'sopro', dt, 12, 6)) return;
        m.aviso(b, f, 'Sopro congelante', f);
        for (const r of m.rivais(b, f)) r.action *= 0.7;
        for (const a of m.aliados(b, f)) a.statuses = a.statuses.filter((s) => s.id !== 'burning');
      },
    },
  },
  spiderman: {
    nome: 'Sentido aranha',
    texto: 'Quando um aliado cai abaixo de 25% da Vida, o Aranha puxa ele com a teia: Escudo de 10% da Vida desse aliado (uma vez por aliado).',
    ganchos: {
      viu(m, b, f, _fonte, alvo) {
        if (alvo.side !== f.side || !vivo(alvo) || fracao(alvo) >= 0.25) return;
        const k = `teia${idx(b, alvo)}`;
        if (u(f)[k]) return;
        u(f)[k] = 1;
        m.aviso(b, f, 'Teia!', alvo);
        alvo.shields.push({ amount: alvo.maxHp * 0.1, remaining: 10, source: f.uid });
      },
    },
  },
  thor: {
    nome: 'Senhor da tempestade',
    texto: '1 em 5 golpes diretos dele Eletrifica o alvo. Enquanto Thor está de pé, rivais Eletrificados levam 12% a mais de todo o trio.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && m.sorte(b) < 0.2) m.efeitos(b, f, [alvo], [st('electric', 0.25, 3)]); },
      causaAliado: (m, _b, _f, _aliado, alvo) => (m.intensidade(alvo, 'electric') > 0 ? 1.12 : 1),
    },
  },
  strange: {
    nome: 'Portais',
    texto: 'A cada 25 s abre um portal: a próxima habilidade de um rival que acertaria o trio passa pela metade no portal, e essa metade sai em cima de outro rival.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'portal', dt, 25, 10)) { u(f).portal = 1; m.aviso(b, f, 'Portal aberto', f); } },
      recebe(m, b, f, fonte, g) { portal(m, b, f, fonte, g.habilidade && g.direto); return 1; },
      recebeAliado(m, b, f, _aliado, fonte, g) { portal(m, b, f, fonte, g.habilidade && g.direto); return 1; },
      limita(m, b, f, _alvo, valor) {
        if (!u(f).desvio) return valor;
        u(f).desvio = 0;
        const de = b.fighters[u(f).de ?? -1];
        const rs = m.rivais(b, f), r = rs.find((x) => x !== de) ?? de;
        if (r && vivo(r)) m.dano(b, f, r, valor / 2, false, 'Portal');
        return valor / 2;
      },
    },
  },
  flash: {
    nome: 'Força de aceleração',
    texto: 'Ele empresta a velocidade: cada ataque básico do Flash adianta em 8% a ação de um aliado.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || g.habilidade) return;
        const outros = m.aliados(b, f).filter((a) => a !== f);
        const a = outros[Math.floor(m.sorte(b) * outros.length)];
        if (a) a.action = Math.min(1, a.action + 0.08);
      },
    },
  },
  wonderwoman: {
    nome: 'Laço da verdade',
    texto: 'O primeiro rival que ela acerta fica laçado: não consegue Esquivar e leva 10% a mais de todo o trio enquanto ela estiver de pé.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && !u(f).laco && vivo(alvo)) { u(f).laco = idx(b, alvo) + 1; m.aviso(b, f, 'Laço da verdade', alvo); } },
      passo(_m, b, f) { const r = b.fighters[(u(f).laco ?? 0) - 1]; if (r) r.statuses = r.statuses.filter((s) => s.id !== 'evasion'); },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).laco === idx(b, alvo) + 1 ? 1.1 : 1),
    },
  },
  captain: {
    nome: 'Avante!',
    texto: 'O trio segue o Capitão: cada vez que ele usa uma habilidade, os outros dois ganham 15% de ação.',
    ganchos: { usou(m, b, f) { for (const a of m.aliados(b, f)) if (a !== f) a.action = Math.min(1, a.action + 0.15); } },
  },
  magneto: {
    nome: 'Polaridade',
    texto: 'Troca de polo a cada 10 s. Atração: os rivais causam 15% a menos no trio. Repulsão: Magneto causa 25% a mais.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'polo', dt, 10)) { u(f).polo = u(f).polo ? 0 : 1; m.aviso(b, f, u(f).polo ? 'Repulsão' : 'Atração', f); } },
      causa: (_m, _b, f) => (u(f).polo ? 1.25 : 1),
      recebeAliado: (_m, _b, f) => (u(f).polo ? 1 : 0.85),
    },
  },
  deadpool: {
    nome: 'Fator de cura absurdo',
    texto: 'Quanto mais pedaço perde, mais rápido cresce de volta: cura 0,5% da Vida por segundo para cada 20% de Vida perdida.',
    ganchos: { passo(m, b, f, dt) { const n = Math.floor((1 - fracao(f)) * 5); if (n > 0) m.cura(b, f, f, f.maxHp * 0.005 * n * dt, 'Fator de cura'); } },
  },
  raven: {
    nome: 'Cura empática',
    texto: 'Ela sente a dor dos amigos: quando um aliado leva um golpe direto, Ravena cura 40% dele no aliado e sente metade disso no próprio corpo (a cada 3 s).',
    ganchos: {
      viu(m, b, f, fonte, alvo, dano, g) {
        if (!g.direto || alvo === f || alvo.side !== f.side || fonte.side === f.side || !vivo(alvo) || (u(f).empatia ?? 0) > b.time) return;
        u(f).empatia = b.time + 3;
        m.cura(b, f, alvo, dano * 0.4, 'Empatia');
        f.hp = Math.max(1, f.hp - dano * 0.2);
      },
    },
  },
  thanos: {
    nome: 'Manopla do Infinito',
    texto: 'Cada habilidade usada encaixa uma Joia (até 6): +4% de dano por Joia. Com as 6, estala os dedos uma vez: cada rival perde 20% da Vida que tem.',
    ganchos: {
      usou(m, b, f) {
        if ((u(f).joias ?? 0) >= 6) return;
        u(f).joias = (u(f).joias ?? 0) + 1;
        m.aviso(b, f, `Joia ${u(f).joias}/6`, f, u(f).joias);
        if (u(f).joias !== 6) return;
        m.aviso(b, f, 'Estalo', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, r.hp * 0.2, false, 'Estalo');
      },
      causa: (_m, _b, f) => 1 + 0.04 * (u(f).joias ?? 0),
    },
  },
  kakashi: {
    nome: 'Ninja que copia',
    texto: 'Copia o que vê: cada habilidade de rival que o acerta dá 15 de Carga para a habilidade dele que está mais vazia.',
    ganchos: {
      apanhou(_m, _b, f, fonte, _dano, g) {
        if (!g.habilidade || fonte.side === f.side) return;
        const s = [...f.skills].sort((x, y) => x.charge - y.charge)[0];
        if (s) s.charge = Math.min(100, s.charge + 15);
      },
    },
  },
  itachi: {
    nome: 'Doença terminal',
    texto: 'Itachi luta doente: perde 2% da Vida a cada 5 s, mas cada golpe dele causa 25% a mais.',
    ganchos: {
      passo(_m, _b, f, dt) { if (relogio(f, 'doenca', dt, 5)) f.hp = Math.max(1, f.hp - f.maxHp * 0.02); },
      causa: () => 1.25,
    },
  },
  sakura: {
    nome: 'Médica de campo',
    texto: 'Cura e protege junto: quem Sakura cura também fica Protegido 10% por 2 s (no máximo uma vez a cada 4 s por aliado).',
    ganchos: {
      curaFeita(m, b, f, alvo) {
        const k = `medica${idx(b, alvo)}`;
        if ((u(f)[k] ?? 0) <= b.time) { u(f)[k] = b.time + 4; m.efeitos(b, f, [alvo], [st('protected', 0.1, 2)]); }
        return 1;
      },
    },
  },
  inosuke: {
    nome: 'Juntas soltas',
    texto: 'Desloca as juntas e escapa: quando fica Paralisado ou Enraizado, se solta na hora e fica só Lento 30% por 1,5 s.',
    ganchos: {
      pegouStatus(m, b, f, s) {
        if (s !== 'paralyzed' && s !== 'rooted') return;
        f.statuses = f.statuses.filter((x) => x.id !== s);
        m.aviso(b, f, 'Juntas soltas', f);
        m.efeitos(b, f, [f], [st('slow', 0.3, 1.5)]);
      },
    },
  },
  muzan: {
    nome: 'Chicotes de carne',
    texto: 'Os braços viram chicotes: o ataque básico acerta os três rivais de uma vez, com 45% da força em cada.',
    ganchos: {
      causa: (_m, _b, _f, _alvo, g) => (g.direto && !g.habilidade ? 0.45 : 1),
      bateu(m, b, f, alvo, dano, g) { if (g.direto && !g.habilidade) for (const r of m.rivais(b, f)) if (r !== alvo) m.dano(b, f, r, dano, false, 'Chicote'); },
    },
  },
  megumi: {
    nome: 'Roda de Mahoraga',
    texto: 'A roda gira e se adapta: cada vez que o mesmo tipo de golpe acerta ele, faz 6% a menos (até 18%).',
    ganchos: {
      recebe(_m, _b, f, _fonte, g) { const k = marca(g.label); return 1 - 0.06 * Math.min(3, u(f)[k] ?? 0); },
      apanhou(_m, _b, f, _fonte, _dano, g) { const k = marca(g.label); u(f)[k] = (u(f)[k] ?? 0) + 1; },
    },
  },
  nobara: {
    nome: 'Boneca de palha',
    texto: 'O último rival que ela acertou fica preso na boneca: 30% do dano que Nobara leva vai também nele.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) { if (g.direto) u(f).boneca = idx(b, alvo); },
      apanhou(m, b, f, _fonte, dano, g) {
        const r = b.fighters[u(f).boneca ?? -1];
        if (g.direto && r && vivo(r)) m.dano(b, f, r, dano * 0.3, false, 'Ressonância');
      },
    },
  },
  aizen: {
    nome: 'Kyoka Suigetsu',
    texto: 'A cada 20 s, o próximo golpe direto nele acerta só uma ilusão: não faz nada, e quem bateu fica Confuso por 1 s.',
    ganchos: {
      passo(_m, _b, f, dt) { if (relogio(f, 'ilusao', dt, 20, 6)) u(f).ilusao = 1; },
      recebe(m, b, f, fonte, g) {
        if (!g.direto || !u(f).ilusao) return 1;
        u(f).ilusao = 0;
        m.aviso(b, f, 'Ilusão', fonte);
        m.efeitos(b, f, [fonte], [st('confused', 1, 1)]);
        return 0;
      },
    },
  },
  eren: {
    nome: 'Endurecimento',
    texto: 'Golpe forte endurece a pele: depois de levar um golpe de mais de 10% da Vida, leva 20% menos por 4 s.',
    ganchos: {
      apanhou(m, b, f, _fonte, dano) { if (dano > f.maxHp * 0.1) { if ((u(f).duro ?? 0) <= b.time) m.aviso(b, f, 'Endurecer', f); u(f).duro = b.time + 4; } },
      recebe: (_m, b, f) => ((u(f).duro ?? 0) > b.time ? 0.8 : 1),
    },
  },
  gon: {
    nome: 'Jajanken',
    texto: 'O ataque básico gira Pedra, Tesoura, Papel: Pedra bate 50% mais forte, Tesoura corta também outro rival (50%), Papel acerta todos os rivais com 25 de dano.',
    ganchos: {
      causa: (_m, _b, f, _alvo, g) => (g.direto && !g.habilidade && (u(f).jan ?? 0) % 3 === 0 ? 1.5 : 1),
      bateu(m, b, f, alvo, dano, g) {
        if (!g.direto || g.habilidade) return;
        const fase = (u(f).jan ?? 0) % 3;
        u(f).jan = (u(f).jan ?? 0) + 1;
        if (fase === 1) { const o = m.rivais(b, f).find((r) => r !== alvo); if (o) m.dano(b, f, o, dano * 0.5, false, 'Tesoura'); }
        if (fase === 2) for (const r of m.rivais(b, f)) m.dano(b, f, r, 25, false, 'Papel');
      },
    },
  },
  killua: {
    nome: 'Godspeed',
    texto: 'Reflexo elétrico: quando um rival começa a preparar uma habilidade, Killua ganha 25% de ação na hora.',
    ganchos: { viuPreparo(_m, _b, f) { f.action = Math.min(1, f.action + 0.25); } },
  },
  edward: {
    nome: 'Transmutação sem círculo',
    texto: 'Bate as mãos e transforma: cada habilidade que usa dá 5 de Carga para as outras duas habilidades dele.',
    ganchos: { usou(_m, _b, f, i) { f.skills.forEach((s, j) => { if (j !== i) s.charge = Math.min(100, s.charge + 5); }); } },
  },
  alphonse: {
    nome: 'Parede transmutada',
    texto: 'Cada golpe direto que Al leva vira uma parede: o próximo golpe direto no aliado mais ferido faz 30% a menos.',
    ganchos: {
      apanhou(_m, _b, f, _fonte, _dano, g) { if (g.direto) u(f).parede = 1; },
      recebeAliado(m, b, f, aliado, _fonte, g) {
        if (!g.direto || !u(f).parede || maisFerido(m, b, f) !== aliado) return 1;
        u(f).parede = 0;
        m.aviso(b, f, 'Parede', aliado);
        return 0.7;
      },
    },
  },
  roy: {
    nome: 'Alquimista das chamas',
    texto: 'Cada 3º golpe direto é um estalo que acende o alvo: Queimando por 2 s. Em quem já está Queimando, Roy causa 8% a mais.',
    ganchos: {
      causa: (_m, _b, _f, alvo, g) => (g.direto && alvo.statuses.some((s) => s.id === 'burning') ? 1.08 : 1),
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo) && (u(f).estalo = (u(f).estalo ?? 0) + 1) % 3 === 0) m.efeitos(b, f, [alvo], [st('burning', 5, 2)]); },
    },
  },
  griffith: {
    nome: 'Eclipse',
    texto: 'A primeira vez que fica abaixo de 25% da Vida, sacrifica a Banda: o aliado com mais Vida perde 30% da Vida que tem, Griffith se cura nesse tanto e renasce como Femto, causando 30% a mais.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).femto || fracao(f) >= 0.25) return;
        u(f).femto = 1;
        const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => y.hp - x.hp)[0];
        m.aviso(b, f, 'Eclipse', a ?? f);
        if (!a) return;
        const parte = a.hp * 0.3;
        a.hp = Math.max(1, a.hp - parte);
        m.cura(b, f, f, parte, 'Eclipse');
      },
      causa: (_m, _b, f) => (u(f).femto ? 1.3 : 1),
    },
  },
  giorno: {
    nome: 'Vida demais',
    texto: 'Gold Experience enche o alvo de vida: a mente dispara e o corpo não acompanha. Cada golpe direto deixa o rival Lento 20% por 1,5 s.',
    ganchos: { bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo)) m.efeitos(b, f, [alvo], [st('slow', 0.2, 1.5)]); } },
  },
  power: {
    nome: 'Covarde e convencida',
    texto: 'Golpe grande nela (mais de 15% da Vida)? Se esconde atrás do aliado com mais Vida, que leva metade. Quando derruba um rival, se gaba: Fortalecida 30% por 6 s.',
    ganchos: {
      limita(m, b, f, alvo, valor) {
        if (alvo !== f || valor <= f.maxHp * 0.15) return valor;
        const a = m.aliados(b, f).filter((x) => x !== f).sort((x, y) => y.hp - x.hp)[0];
        if (!a) return valor;
        m.aviso(b, f, 'Escondida!', a);
        a.hp = Math.max(1, a.hp - valor / 2);
        return valor / 2;
      },
      caiu(m, b, f, quem, quemDerrubou) { if (quem.side !== f.side && quemDerrubou === f) { m.aviso(b, f, 'Viu só?', f); m.efeitos(b, f, [f], [st('strengthened', 0.3, 6)]); } },
    },
  },
  anya: {
    nome: 'Waku waku',
    texto: 'Lê a mente de quem vai atacar: quando um rival começa a preparar uma habilidade, o aliado mais ferido fica Protegido por 1,5 s.',
    ganchos: {
      viuPreparo(m, b, f) {
        if ((u(f).leu ?? 0) > b.time) return;
        u(f).leu = b.time + 3;
        const a = maisFerido(m, b, f);
        if (a) { m.aviso(b, f, 'Waku waku', a); m.efeitos(b, f, [a], [st('protected', 0.3, 1.5)]); }
      },
    },
  },
  jinwoo: {
    nome: 'Sobe de nível',
    texto: 'O único que sobe de nível: a cada 250 de dano causado na luta, ganha 1 nível (até 10). Cada nível dá 3% de dano e 3% de Vida máxima.',
    ganchos: {
      bateu(m, b, f) {
        const n = Math.min(10, Math.floor(f.stats.damage / 250));
        while ((u(f).nivel ?? 0) < n) {
          u(f).nivel = (u(f).nivel ?? 0) + 1;
          const extra = f.maxHp * 0.03; f.maxHp += extra; f.hp += extra;
          m.aviso(b, f, `Nível ${u(f).nivel}`, f, u(f).nivel);
        }
      },
      causa: (_m, _b, f) => 1 + 0.03 * (u(f).nivel ?? 0),
    },
  },
  yugi: {
    nome: 'Coração das cartas',
    texto: 'A cada 13 s compra uma carta: Mago Negro (70 de dano), Pote da Ganância (+30% de ação no trio), Cilindro Mágico (Escudo de 10% da Vida) ou Espadas da Luz (um rival Paralisado 1 s).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'carta', dt, 13, 6)) return;
        const r = maisForte(m, b, f), c = Math.floor(m.sorte(b) * 4);
        if (c === 0 && r) { m.aviso(b, f, 'Mago Negro', r); m.dano(b, f, r, 70, false, 'Mago Negro'); }
        if (c === 1) { m.aviso(b, f, 'Pote da Ganância', f); for (const a of m.aliados(b, f)) a.action = Math.min(1, a.action + 0.3); }
        if (c === 2) { m.aviso(b, f, 'Cilindro Mágico', f); f.shields.push({ amount: f.maxHp * 0.1, remaining: 10, source: f.uid }); }
        if (c === 3 && r) { m.aviso(b, f, 'Espadas da Luz', r); m.efeitos(b, f, [r], [st('paralyzed', 1, 1)]); }
      },
    },
  },
  kaiba: {
    nome: 'Três Olhos Azuis',
    texto: 'Guarda três Dragões Brancos. Na primeira vez abaixo de 75%, 50% e 25% da Vida, um dragão sai: 110 de dano no rival mais forte.',
    ganchos: {
      apanhou(m, b, f) {
        for (const lim of [0.75, 0.5, 0.25]) {
          const k = `dragao${lim * 100}`;
          if (u(f)[k] || fracao(f) >= lim) continue;
          u(f)[k] = 1;
          const r = maisForte(m, b, f);
          if (r) { m.aviso(b, f, 'Dragão Branco', r); m.dano(b, f, r, 110, false, 'Luz Branca'); }
        }
      },
    },
  },
  scarletwitch: {
    nome: 'Probabilidade reescrita',
    texto: 'O caos joga a favor dela: 1 em 8 golpes que levaria é reescrito: não pega, e vira cura de 30% do valor.',
    ganchos: {
      limita(m, b, f, alvo, valor) {
        if (alvo !== f || valor <= 0 || m.sorte(b) >= 0.125) return valor;
        m.aviso(b, f, 'Hex', f);
        m.cura(b, f, f, valor * 0.3, 'Hex');
        return 0;
      },
    },
  },
  vision: {
    nome: 'Joia da Mente',
    texto: 'Quando um aliado fica Confuso, Dormindo ou Silenciado, a Joia da Mente limpa a cabeça dele na hora (no máximo a cada 6 s).',
    ganchos: {
      passo(m, b, f) {
        if ((u(f).joia ?? 0) > b.time) return;
        const a = m.aliados(b, f).find((x) => x.statuses.some((s) => MENTE.includes(s.id)));
        if (!a) return;
        u(f).joia = b.time + 6;
        a.statuses = a.statuses.filter((s) => !MENTE.includes(s.id));
        m.aviso(b, f, 'Joia da Mente', a);
      },
    },
  },
  antman: {
    nome: 'Partículas Pym',
    texto: 'Muda de tamanho a cada 6 s. Pequeno: leva 40% a menos. Gigante: causa 40% a mais, mas leva 20% a mais.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'pym', dt, 6)) { u(f).gigante = u(f).gigante ? 0 : 1; m.aviso(b, f, u(f).gigante ? 'Gigante' : 'Formiga', f); } },
      causa: (_m, _b, f) => (u(f).gigante ? 1.4 : 1),
      recebe: (_m, _b, f) => (u(f).gigante ? 1.2 : 0.6),
    },
  },
  ghostrider: {
    nome: 'Olhar de penitência',
    texto: 'O pecado volta: os golpes dele causam 1% a mais para cada 60 de dano que o alvo já causou na luta (até 50%).',
    ganchos: { causa: (_m, _b, _f, alvo) => 1 + Math.min(0.5, alvo.stats.damage / 6000) },
  },
  blade: {
    nome: 'Caçador de vampiros',
    texto: 'Fareja quem se alimenta: causa 40% a mais em rivais que se curaram nos últimos 5 s.',
    ganchos: {
      curaNoRival(_m, b, f, alvo) { u(f)[`cura${idx(b, alvo)}`] = b.time; return 1; },
      causa: (_m, b, f, alvo) => ((u(f)[`cura${idx(b, alvo)}`] ?? -99) > b.time - 5 ? 1.4 : 1),
    },
  },
  moonknight: {
    nome: 'Crescentes de prata',
    texto: 'Cada golpe direto crava um crescente no alvo (até 5). A próxima habilidade dele nesse rival arranca todos: 25 de dano por crescente.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const k = `lua${idx(b, alvo)}`, n = u(f)[k] ?? 0;
        if (g.habilidade && n) { u(f)[k] = 0; m.aviso(b, f, 'Crescentes', alvo, n); m.dano(b, f, alvo, 25 * n, false, 'Crescentes'); }
        else if (!g.habilidade) u(f)[k] = Math.min(5, n + 1);
      },
    },
  },
  cyclops: {
    nome: 'Óculos de rubi',
    texto: 'Se fosse ficar Cego, o visor cai e o raio sai sem controle: não fica Cego e acerta todos os rivais com 60. O Feixe concentrado causa 30% a mais em quem tem Escudo.',
    ganchos: {
      pegouStatus(m, b, f, s) {
        if (s !== 'blind') return;
        f.statuses = f.statuses.filter((x) => x.id !== 'blind');
        m.aviso(b, f, 'Raio sem controle', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 60, false, 'Raio óptico');
      },
      causa: (_m, _b, _f, alvo, g) => (g.habilidade && g.indice === 2 && alvo.shields.length ? 1.3 : 1),
    },
  },
  jeangrey: {
    nome: 'Elo mental',
    texto: 'Liga a mente do trio: quando um aliado leva um golpe de mais de 15% da Vida dele, Jean segura metade da dor.',
    ganchos: {
      limita(_m, _b, f, alvo, valor) {
        if (alvo === f || !vivo(f) || valor <= alvo.maxHp * 0.15) return valor;
        const parte = valor / 2;
        f.hp = Math.max(1, f.hp - parte * 0.8);
        return valor - parte;
      },
    },
  },
  rogue: {
    nome: 'Toque absorvente',
    texto: 'O primeiro golpe direto em cada rival rouba o poder dele: aquele rival causa 4% a menos e Vampira causa 4% a mais (até 12%).',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto) return;
        const k = `toque${idx(b, alvo)}`;
        if (u(f)[k]) return;
        u(f)[k] = 1; u(f).roubos = (u(f).roubos ?? 0) + 1;
        m.aviso(b, f, 'Toque', alvo);
      },
      causa: (_m, _b, f) => 1 + 0.04 * (u(f).roubos ?? 0),
      recebeAliado: (_m, b, f, _aliado, fonte) => (u(f)[`toque${idx(b, fonte)}`] ? 0.96 : 1),
    },
  },
  gambit: {
    nome: 'Carga cinética',
    texto: 'Cada 3º ataque básico vai com uma carta carregada: explode e acerta todos os rivais com 35 de dano.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || g.habilidade) return;
        u(f).cartas = (u(f).cartas ?? 0) + 1;
        if (u(f).cartas! % 3) return;
        m.aviso(b, f, 'Carta carregada', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 35, false, 'Carta');
      },
    },
  },
  professorx: {
    nome: 'Cérebro',
    texto: 'Coordena o trio de longe: a cada 4 s, o aliado mais atrasado ganha 15% de ação.',
    ganchos: {
      passo(_m, b, f, dt) {
        if (!relogio(f, 'cerebro', dt, 4)) return;
        const a = b.fighters.filter((x) => x.side === f.side && vivo(x)).sort((x, y) => x.action - y.action)[0];
        if (a) a.action = Math.min(1, a.action + 0.15);
      },
    },
  },
  doctordoom: {
    nome: 'Doombots',
    texto: 'Plano de contingência: começa com 3 Doombots na frente. Cada golpe direto nele quebra um robô, que segura até 60 do dano.',
    ganchos: {
      inicio(_m, _b, f) { u(f).bots = 3; },
      recebe(_m, _b, f, _fonte, g) { u(f).direto = g.direto ? 1 : 0; return 1; },
      limita(m, b, f, alvo, valor) {
        if (alvo !== f || !u(f).direto || !(u(f).bots ?? 0)) return valor;
        u(f).bots! -= 1; u(f).direto = 0;
        m.aviso(b, f, 'Doombot', f, u(f).bots);
        return Math.max(0, valor - 60);
      },
    },
  },
  greengoblin: {
    nome: 'Bomba-abóbora',
    texto: 'Cada golpe direto gruda uma abóbora no alvo, que explode 4 s depois: 30 de dano.',
    ganchos: {
      bateu(_m, b, f, alvo, _dano, g) {
        if (!g.direto) return;
        const k = `abobora${idx(b, alvo)}`;
        u(f)[k] ??= b.time + 4;
      },
      passo(m, b, f) {
        for (const r of b.fighters) {
          const k = `abobora${idx(b, r)}`, t = u(f)[k];
          if (t === undefined || b.time < t) continue;
          delete u(f)[k];
          if (vivo(r)) m.dano(b, f, r, 30, false, 'Abóbora');
        }
      },
    },
  },
  silversurfer: {
    nome: 'Arauto de Galactus',
    texto: 'Escolhe um planeta para Galactus: o rival mais forte, que leva 20% a mais dele. Quando o planeta cai, o Surfista se cura em 15% e escolhe outro.',
    ganchos: {
      passo(m, b, f) {
        const p = b.fighters[u(f).planeta ?? -1];
        if (p && vivo(p)) return;
        const r = maisForte(m, b, f);
        if (r) { u(f).planeta = idx(b, r); m.aviso(b, f, 'Planeta escolhido', r); }
      },
      causa: (_m, b, f, alvo) => (u(f).planeta === idx(b, alvo) ? 1.2 : 1),
      caiu(m, b, f, quem) { if (u(f).planeta === idx(b, quem)) m.cura(b, f, f, f.maxHp * 0.15, 'Arauto'); },
    },
  },
};

/* Bochechas do Pikachu: 8 cargas descarregam no rival mais forte. */
function bochecha(m: Motor, b: Battle, f: Fighter) {
  u(f).volts = (u(f).volts ?? 0) + 1;
  if (u(f).volts! < 8) return;
  u(f).volts = 0;
  const r = maisForte(m, b, f);
  if (!r) return;
  m.aviso(b, f, 'Descarga', r);
  m.dano(b, f, r, 60, false, 'Descarga');
  m.efeitos(b, f, [r], [st('electric', 0.25, 3)]);
}
/* Portal do Estranho: a próxima habilidade rival que acertaria o trio é desviada (o `limita` dele faz o desvio). */
function portal(m: Motor, b: Battle, f: Fighter, fonte: Fighter, habilidade: boolean) {
  if (!u(f).portal || !habilidade || fonte.side === f.side) return;
  u(f).portal = 0; u(f).desvio = 1; u(f).de = idx(b, fonte);
  m.aviso(b, f, 'Portal', fonte);
}
