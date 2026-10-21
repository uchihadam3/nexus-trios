/*
 * Mecânicas únicas — lote 4: Disney, anime, desenhos e games.
 */
import { curaContinua, fracao, maisFerido, maisForte, quandoVira, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import type { Battle, Effect, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const invoca = (valor: number, duracao: number, rotulo: string): Effect => ({ kind: 'status', status: 'summon', value: valor, duration: duracao, rotulo });
const maisFraco = (m: Motor, b: Battle, f: Fighter) => m.rivais(b, f).sort((x, y) => x.hp - y.hp)[0];
const BONS: StatusId[] = ['strengthened', 'haste', 'protected', 'regen', 'barrier', 'evasion', 'reflect', 'vampirism', 'thorns', 'summon'];
const vidaDoTrio = (xs: Fighter[]) => xs.reduce((n, x) => n + fracao(x), 0);

export const LOTE4: Record<string, Unica> = {
  /* ───────── Gigantes ───────── */
  kingkong: {
    nome: 'Briga de titãs',
    texto: 'King Kong causa +30% de dano em rivais com 1.200 ou mais de Vida máxima.',
    ganchos: { causa: (_m, _b, _f, alvo) => (alvo.maxHp >= 1200 ? 1.3 : 1) },
  },
  shrek: {
    nome: 'Camadas de cebola',
    texto: 'A cada 25% de Vida que Shrek perde, Shrek recebe −12% de dano (até 3 vezes: −36%, com 25% da Vida ou menos).',
    ganchos: {
      passo(m, b, f) {
        // cada camada nova que cai mostra a mecânica ativando; curar fecha a camada de novo
        const n = Math.min(3, Math.floor((1 - fracao(f)) / 0.25));
        if (n > (u(f).camada ?? 0)) m.aviso(b, f, `Camada ${n}`, f);
        u(f).camada = n;
      },
      recebe: (_m, _b, f) => 1 - 0.12 * Math.min(3, Math.floor((1 - fracao(f)) / 0.25)),
    },
  },
  elsa: {
    nome: 'Livre estou',
    texto: 'Elsa nunca fica Lento nem Congelado. Com 50% da Vida ou menos (1 vez por luta): todo o trio de Elsa ganha Barreira (anula 1 debuff) por 8 s, e todos os rivais ficam Lento (25% mais lento) por 6 s.',
    ganchos: {
      imune: (_f, s) => s === 'slow' || s === 'frozen',
      apanhou(m, b, f) {
        if (u(f).castelo || fracao(f) > 0.5) return;
        u(f).castelo = 1;
        m.efeitos(b, f, m.aliados(b, f), [st('barrier', 1, 8)]);
        m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.25, 6)]);
        m.aviso(b, f, 'Livre estou!', f);
      },
    },
  },
  maleficent: {
    nome: 'Fúria da fada',
    texto: 'Com menos de 40% da Vida (1 vez por luta), Malévola vira dragão até o fim da luta: ganha +30% de Vida máxima (e cura essa diferença), e cada golpe de Malévola deixa o alvo Queimando (−12 de Vida por segundo) por 3 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).dragao || fracao(f) >= 0.4) return;
        u(f).dragao = 1;
        const extra = Math.round(f.maxHp * 0.3);
        f.maxHp += extra;
        m.cura(b, f, f, extra, 'Forma de dragão');
        m.aviso(b, f, 'Forma de dragão', f);
      },
      bateu(m, b, f, alvo, _dano, g) { if (u(f).dragao && g.direto && vivo(alvo)) m.efeitos(b, f, [alvo], [st('burning', 12, 3)]); },
    },
  },
  genie: {
    nome: 'Três desejos',
    texto: 'Aos 15, 30 e 45 s de luta, o Gênio realiza um desejo, o que o trio mais precisar: levanta um aliado caído com 40% da Vida máxima; se ninguém caiu, cura 30% da Vida máxima do aliado mais ferido (se esse aliado tiver menos de 50% da Vida); se não, todo o trio fica Fortalecido (+25% de dano) por 8 s.',
    ganchos: {
      passo(m, b, f) {
        const s = u(f);
        if ((s.desejos ?? 0) >= 3 || b.time < 15 * ((s.desejos ?? 0) + 1)) return;
        s.desejos = (s.desejos ?? 0) + 1;
        const caido = b.fighters.find((x) => x.side === f.side && !vivo(x) && !x.voltou && !((x.renascendo ?? 0) > 0));
        if (caido) { m.levanta(b, f, caido, 0.4); m.aviso(b, f, `Desejo ${s.desejos}: de volta!`, caido); return; }
        const ferido = maisFerido(m, b, f);
        if (ferido && fracao(ferido) < 0.5) { m.cura(b, f, ferido, ferido.maxHp * 0.3, 'Desejo'); m.aviso(b, f, `Desejo ${s.desejos}: cura`, ferido); return; }
        m.efeitos(b, f, m.aliados(b, f), [st('strengthened', 0.25, 8)]);
        m.aviso(b, f, `Desejo ${s.desejos}: força`, f);
      },
    },
  },
  scar: {
    nome: 'As hienas',
    texto: 'A cada 10 s, as hienas de Scar atacam o rival mais ferido: 3 golpes de 25 de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'hienas', dt, 10, 6)) return;
        const alvo = m.rivais(b, f).sort((x, y) => fracao(x) - fracao(y))[0];
        if (!alvo) return;
        m.aviso(b, f, 'Hienas!', alvo);
        for (let i = 0; i < 3 && vivo(alvo); i++) m.dano(b, f, alvo, 25, false, 'Hienas');
      },
    },
  },
  jackskellington: {
    nome: 'Natal roubado',
    texto: 'A cada 15 s, Jack Esqueleto entrega presentes. Um aliado aleatório ganha um Status bom surpresa: Fortalecido (+25% de dano), Acelerado (25% mais rápido), Protegido (−30% de dano recebido) ou Regeneração (+15 de Vida por segundo) por 6 s, ou Barreira (anula 1 debuff) por 8 s. Um rival aleatório ganha Marca explosiva (60 de dano) que explode em 4 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'natal', dt, 15, 8)) return;
        const as = m.aliados(b, f), rs = m.rivais(b, f);
        const presentes: Effect[] = [st('strengthened', 0.25, 6), st('haste', 0.25, 6), st('protected', 0.3, 6), st('regen', 15, 6), st('barrier', 1, 8)];
        if (as.length) m.efeitos(b, f, [as[Math.floor(m.sorte(b) * as.length)]!], [presentes[Math.floor(m.sorte(b) * presentes.length)]!]);
        if (rs.length) m.efeitos(b, f, [rs[Math.floor(m.sorte(b) * rs.length)]!], [st('bomb', 60, 4)]);
        m.aviso(b, f, 'Feliz Natal!', f);
      },
    },
  },
  ursula: {
    nome: 'Contrato marinho',
    texto: 'No começo da luta, Úrsula rouba a voz do rival com mais Vida: enquanto Úrsula estiver de pé, a 3ª habilidade desse rival nunca enche a Carga.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).voz = idx(b, a); m.aviso(b, f, 'Voz roubada', a); } },
      passo(_m, b, f) { const a = b.fighters[u(f).voz ?? -1]; if (a && vivo(a)) a.skills[2]!.charge = 0; },
    },
  },

  /* ───────── Anime ───────── */
  deku: {
    nome: 'Controle do One For All',
    texto: 'Izuku Midoriya começa com −10% de dano e ganha +10% a cada habilidade que usa, até +50% (depois de 6 habilidades).',
    ganchos: {
      usou(m, b, f) { if ((u(f).porcento ?? 0) < 6) { u(f).porcento = (u(f).porcento ?? 0) + 1; m.aviso(b, f, `${5 + 8 * u(f).porcento!}%`, f); } },
      causa: (_m, _b, f) => 0.9 + 0.1 * (u(f).porcento ?? 0),
    },
  },
  bakugo: {
    nome: 'Explosões crescentes',
    texto: 'Katsuki Bakugo ganha +1% de dano a cada 2 s de luta (até +40%, aos 80 s).',
    ganchos: {
      passo(m, b, f) {
        const n = Math.min(4, Math.floor(b.time / 20));
        if (n > (u(f).explosoes ?? 0)) { u(f).explosoes = n; m.aviso(b, f, `Explosões +${n * 10}%`, f); }
      },
      causa: (_m, b) => 1 + Math.min(0.4, b.time / 200),
    },
  },
  rimuru: {
    nome: 'Corpo que se adapta',
    texto: 'Depois de pegar um Status ruim uma vez, Rimuru Tempest se adapta: fica imune a esse Status até o fim da luta.',
    ganchos: {
      // pedido do jogador: "depois que é aplicado em você uma vez, você aprende e fica imune"
      pegouStatus(m, b, f, s) {
        const k = `visto_${s}`;
        if (u(f)[k]) return;
        u(f)[k] = 1;
        m.aviso(b, f, 'Analisado: imune', f);
      },
      imune: (f, s) => (u(f)[`visto_${s}`] ?? 0) >= 1,
    },
  },
  ainz: {
    nome: 'Corpo de morto-vivo',
    texto: 'Status ruins que durariam menos de 3 s não pegam em Ainz Ooal Gown.',
    ganchos: { imune: (_f, s, duracao) => duracao < 3 && !BONS.includes(s) },
  },
  lelouch: {
    nome: 'Ordem absoluta',
    texto: 'A cada 10 s, Lelouch rouba todos os Status bons de um rival (o primeiro que tiver algum) e os passa para o aliado mais ferido. Se nenhum rival tiver Status bom, o rival mais forte fica Paralisado por 2 s.',
    ganchos: {
      passo(m, b, f, dt) {
        // pedido do dono: a cada 10 s (era 15; ele estava fraco). Só o tempo quase não mudava nada (quase nunca há o que
        // roubar): sem Status bom nos rivais, o Geass paralisa o mais forte por 2 s (com as habilidades mais fortes,
        // src/data/expanded-roster.ts, a força foi de −0,49 para 0,151)
        if (!relogio(f, 'geass', dt, 10)) return;
        const alvo = m.rivais(b, f).find((r) => r.statuses.some((s) => BONS.includes(s.id) && s.id !== 'summon')) ?? maisForte(m, b, f);
        const quem = maisFerido(m, b, f);
        if (!alvo || !quem) return;
        const buffs = alvo.statuses.filter((s) => BONS.includes(s.id) && s.id !== 'summon');
        if (!buffs.length) { m.efeitos(b, f, [alvo], [st('paralyzed', 1, 2)]); m.aviso(b, f, 'Obedeça!', alvo); return; }
        alvo.statuses = alvo.statuses.filter((s) => !buffs.includes(s));
        m.efeitos(b, f, [quem], buffs.map((s) => st(s.id, s.intensity, Math.max(2, s.remaining))));
        m.aviso(b, f, 'Obedeça!', alvo);
      },
    },
  },
  sesshomaru: {
    nome: 'Orgulho de youkai',
    texto: 'Sesshomaru causa +30% de dano em rivais com mais de 70% da Vida e −30% de dano em rivais com menos de 30% da Vida. Sesshomaru nunca fica Provocado.',
    ganchos: {
      causa: (_m, _b, _f, alvo) => (fracao(alvo) > 0.7 ? 1.3 : fracao(alvo) < 0.3 ? 0.7 : 1),
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && !u(f).orgulho) { u(f).orgulho = 1; m.aviso(b, f, 'Orgulho de youkai', alvo); } },
      imune: (_f, s) => s === 'provoked',
    },
  },
  erza: {
    nome: 'Reequipar',
    texto: 'A cada 8 s, Erza Scarlet troca de armadura conforme a Vida. Com menos de 50% da Vida: Armadura de Adamantina (fica Protegido (−35% de dano recebido) por 8 s). Com 50% da Vida ou mais: Armadura do Purgatório (+30% de dano enquanto Erza estiver com essa armadura).',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'armadura', dt, 8, 0.1)) return;
        const nova = fracao(f) < 0.5 ? 1 : 2;
        if (u(f).armadura === nova) return;
        u(f).armadura = nova;
        if (nova === 1) m.efeitos(b, f, [f], [st('protected', 0.35, 8)]);
        m.aviso(b, f, nova === 1 ? 'Armadura de Adamantina' : 'Armadura do Purgatório', f);
      },
      causa: (_m, _b, f) => (u(f).armadura === 2 ? 1.3 : 1),
    },
  },
  asta: {
    nome: 'Corpo sem magia',
    texto: 'Asta nunca fica Silenciado, Amaldiçoado nem Confuso. Cada golpe de Asta tira 1 Status bom do alvo.',
    ganchos: {
      imune: (_f, s) => s === 'silenced' || s === 'cursed' || s === 'confused',
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const buff = alvo.statuses.find((s) => BONS.includes(s.id));
        if (!buff) return;
        alvo.statuses = alvo.statuses.filter((s) => s !== buff);
        m.aviso(b, f, 'Anulou', alvo);
      },
    },
  },
  rem: {
    nome: 'Fúria de oni',
    texto: 'Enquanto algum aliado de Rem estiver com menos de 30% da Vida, Rem causa +35% de dano e age 20% mais rápido.',
    ganchos: {
      passo(m, b, f) { quandoVira(m, b, f, 'oni', m.aliados(b, f).some((a) => a !== f && fracao(a) < 0.3), 'Fúria de oni', f); },
      causa: (m, b, f) => (m.aliados(b, f).some((a) => a !== f && fracao(a) < 0.3) ? 1.35 : 1),
      ritmo: (m, b, f) => (m.aliados(b, f).some((a) => a !== f && fracao(a) < 0.3) ? 1.2 : 1),
    },
  },
  kirito: {
    nome: 'Jogador solo',
    texto: 'Enquanto o trio de Kirito tiver menos Vida (em %) que os rivais, Kirito causa +15% de dano e age 25% mais rápido.',
    ganchos: {
      passo(m, b, f) { quandoVira(m, b, f, 'solo', vidaDoTrio(m.aliados(b, f)) < vidaDoTrio(m.rivais(b, f)), 'Jogador solo', f); },
      causa: (m, b, f) => (vidaDoTrio(m.aliados(b, f)) < vidaDoTrio(m.rivais(b, f)) ? 1.15 : 1),
      ritmo: (m, b, f) => (vidaDoTrio(m.aliados(b, f)) < vidaDoTrio(m.rivais(b, f)) ? 1.25 : 1),
    },
  },
  senku: {
    nome: 'Dez bilhões por cento',
    texto: 'A cada 10 s, Senku faz um invento, nesta ordem. Remédio: todo o trio cura 10% da Vida máxima. Bateria: +20% de Carga nas habilidades de todo o trio. Pólvora: 60 de dano em cada rival. Lente: o rival com mais Vida fica Exposto (+15% de dano recebido) por 6 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'ciencia', dt, 10, 6)) return;
        const k = (u(f).invento ?? 0) % 4;
        u(f).invento = k + 1;
        if (k === 0) { for (const a of m.aliados(b, f)) m.cura(b, f, a, a.maxHp * 0.1, 'Remédio'); m.aviso(b, f, 'Remédio', f); }
        else if (k === 1) { m.efeitos(b, f, m.aliados(b, f), [{ kind: 'charge', value: 20 }]); m.aviso(b, f, 'Bateria', f); }
        else if (k === 2) { m.aviso(b, f, 'Pólvora', f); for (const r of m.rivais(b, f)) m.dano(b, f, r, 60, false, 'Pólvora'); }
        else { const a = maisForte(m, b, f); if (a) { m.efeitos(b, f, [a], [st('exposed', 0.15, 6)]); m.aviso(b, f, 'Lente', a); } }
      },
    },
  },
  hinata: {
    nome: 'Pontos de chakra',
    texto: 'Cada golpe de Hinata Hyuga fecha um ponto de chakra do alvo: a Carga desse rival passa a encher 5% mais devagar (até 6 pontos: 30% mais devagar).',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo) || !alvo.bonus) return;
        const k = `pontos${idx(b, alvo)}`;
        if ((u(f)[k] ?? 0) >= 6) return;
        u(f)[k] = (u(f)[k] ?? 0) + 1;
        alvo.bonus.carga -= 0.05;
        if (u(f)[k] === 6) m.aviso(b, f, 'Chakra fechado', alvo);
      },
    },
  },
  jiraiya: {
    nome: 'Energia natural',
    texto: 'A cada 15 s, Jiraiya medita 2 s parado e depois causa +40% de dano por 10 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'sabio', dt, 15, 8)) return;
        u(f).medita = b.time + 2; u(f).sabio = b.time + 12;
        m.aviso(b, f, 'Meditando', f);
      },
      parado: (f, b) => (u(f).medita ?? 0) > b.time,
      causa: (_m, b, f) => ((u(f).sabio ?? 0) > b.time && (u(f).medita ?? 0) <= b.time ? 1.4 : 1),
    },
  },
  tsunade: {
    nome: 'Byakugō',
    texto: 'Com menos de 25% da Vida (1 vez por luta): por 6 s, Tsunade cura 6% da Vida máxima por segundo e não pode cair.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).selo && fracao(f) < 0.25) { u(f).selo = b.time + 6; m.aviso(b, f, 'Byakugō', f); } },
      passo(m, b, f, dt) { if ((u(f).selo ?? 0) > b.time) curaContinua(m, b, f, f, f.maxHp * 0.06 * dt, 'Byakugō'); },
      salva: (_m, b, f, alvo) => (alvo === f && (u(f).selo ?? 0) > b.time ? 1 : null),
    },
  },
  sailormars: {
    nome: 'Fogo sagrado',
    texto: 'Todo dano de Queimando nos rivais cura o aliado mais ferido de Sailor Mars em metade desse dano.',
    ganchos: {
      viu(m, b, f, _fonte, alvo, dano, g) {
        if (alvo.side === f.side || g.direto || g.label !== 'Impacto' || m.intensidade(alvo, 'burning') <= 0) return;
        const a = maisFerido(m, b, f);
        if (a) m.cura(b, f, a, dano * 0.5, 'Fogo sagrado');
      },
    },
  },
  steven: {
    nome: 'Proteção que fica',
    texto: 'Os Escudos que Steven Universo dá não acabam com o tempo: só somem quando quebram.',
    ganchos: {
      passo(_m, b, f) { for (const x of b.fighters) for (const s of x.shields) if (s.source === f.uid) s.remaining = Math.max(s.remaining, 5); },
    },
  },
  dexter: {
    nome: 'Dee Dee!',
    texto: 'A cada 10 s, Dexter tenta um invento: 75% de chance de dar +25% de Carga em todas as habilidades de Dexter; 25% de chance de a Dee Dee bagunçar tudo e Dexter ficar 2 s parado.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'lab', dt, 10, 6)) return;
        if (m.sorte(b) < 0.25) { u(f).bagunca = b.time + 2; m.aviso(b, f, 'DEE DEE!', f); return; }
        for (const s of f.skills) if (s.cooldown <= 0) s.charge = Math.min(100, s.charge + 25);
        m.aviso(b, f, 'Funcionou!', f);
      },
      parado: (f, b) => (u(f).bagunca ?? 0) > b.time,
    },
  },
  aku: {
    nome: 'Jogado no futuro',
    texto: 'Com menos de 25% da Vida (1 vez por luta): Aku manda o rival com mais Vida para o futuro, e esse rival fica Paralisado por 8 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).portal || fracao(f) >= 0.25) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        u(f).portal = 1;
        m.efeitos(b, f, [a], [st('paralyzed', 1, 8)]);
        m.aviso(b, f, 'Mandado ao futuro', a);
      },
    },
  },
  megamind: {
    nome: 'Gênio do mal',
    texto: 'No começo da luta, Megamente sorteia 1 de 3 planos (33% de chance cada). Disfarce: não recebe dano de ataques nem de habilidades nos primeiros 10 s. Mecha: +40% de Vida máxima. Desidratar: o rival com mais Vida fica Enfraquecido (−30% de dano) por 15 s.',
    ganchos: {
      inicio(m, b, f) {
        const plano = Math.floor(m.sorte(b) * 3);
        u(f).plano = plano;
        if (plano === 1) { const extra = Math.round(f.maxHp * 0.4); f.maxHp += extra; f.hp += extra; }
        if (plano === 2) { const a = maisForte(m, b, f); if (a) m.efeitos(b, f, [a], [st('weakened', 0.3, 15)]); }
        m.aviso(b, f, ['Plano: disfarce', 'Plano: mecha', 'Plano: desidratar'][plano]!, f);
      },
      recebe: (_m, b, f, _fonte, g) => (u(f).plano === 0 && g.direto && b.time < 10 ? 0 : 1),
    },
  },
  vilgax: {
    nome: 'Armadura que aprende',
    texto: 'Cada golpe que Vilgax recebe de um rival ensina a armadura: Vilgax passa a receber −4% de dano desse rival (até 10 golpes: −40%).',
    ganchos: {
      apanhou(_m, b, f, fonte, _dano, g) { if (g.direto) { const k = `estudo${idx(b, fonte)}`; u(f)[k] = Math.min(10, (u(f)[k] ?? 0) + 1); } },
      recebe: (_m, b, f, fonte) => 1 - 0.04 * (u(f)[`estudo${idx(b, fonte)}`] ?? 0),
    },
  },
  cosmowanda: {
    nome: 'Padrinhos mágicos',
    texto: 'A cada 12 s, Cosmo e Wanda realizam um desejo: a habilidade do trio com mais Carga (fora do Resfriamento) fica pronta na hora.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'desejo', dt, 12, 8)) return;
        let melhor: { a: Fighter; i: number } | undefined;
        for (const a of m.aliados(b, f)) a.skills.forEach((s, i) => { if (s.cooldown <= 0 && s.charge < 100 && (!melhor || s.charge > melhor.a.skills[melhor.i]!.charge)) melhor = { a, i }; });
        if (!melhor) return;
        melhor.a.skills[melhor.i]!.charge = 100;
        m.aviso(b, f, 'Desejo realizado', melhor.a);
      },
    },
  },

  /* ───────── Games ───────── */
  steve: {
    nome: 'Crafting',
    texto: 'A cada 8 golpes, Steve fabrica uma peça, nesta ordem. Armadura de diamante: fica Protegido (−25% de dano recebido) até o fim da luta. Espada de diamante: +30% de dano até o fim da luta. Golem de ferro: Invocação até o fim da luta, que ataca um rival a cada 1,5 s com 45 de dano por ataque.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto) return;
        const s = u(f);
        if ((s.pecas ?? 0) >= 3) return;
        s.recursos = (s.recursos ?? 0) + 1;
        if (s.recursos < 8) return;
        s.recursos = 0; s.pecas = (s.pecas ?? 0) + 1;
        if (s.pecas === 1) { m.efeitos(b, f, [f], [st('protected', 0.25, 999)]); m.aviso(b, f, 'Armadura de diamante', f); }
        else if (s.pecas === 2) m.aviso(b, f, 'Espada de diamante', f);
        else { m.efeitos(b, f, [f], [invoca(45, 999, 'Golem de ferro')]); m.aviso(b, f, 'Golem de ferro', f); }
      },
      causa: (_m, _b, f) => ((u(f).pecas ?? 0) >= 2 ? 1.3 : 1),
    },
  },
  creeper: {
    nome: 'Tssss… BOOM',
    texto: 'A cada 14 s, o Creeper chia 1 s parado e explode: 280 de dano no rival com mais Vida e 80 nos outros rivais. A explosão custa 10% da Vida máxima do Creeper (sem cair por isso).',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.chiando ?? 0) > 0) {
          s.chiando! -= dt;
          if (s.chiando! > 1e-6) return;
          s.chiando = 0;
          const a = maisForte(m, b, f);
          m.aviso(b, f, 'BOOM', a ?? f);
          if (a) m.dano(b, f, a, 280, false, 'Explosão do Creeper');
          for (const r of m.rivais(b, f)) if (r !== a) m.dano(b, f, r, 80, false, 'Explosão do Creeper');
          f.hp = Math.max(1, f.hp - f.maxHp * 0.1);
          return;
        }
        if (relogio(f, 'tss', dt, 14, 8)) { s.chiando = 1; m.aviso(b, f, 'Tssss…', f); }
      },
      parado: (f) => (u(f).chiando ?? 0) > 0,
    },
  },
  pacman: {
    nome: 'Hora de comer',
    texto: 'A cada 22 s, Pac-Man come uma pílula de poder por 6 s: todos os rivais ficam Lento (20% mais lento), e Pac-Man causa +60% de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'pilula', dt, 22, 10)) return;
        u(f).poder = b.time + 6;
        m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.2, 6)]);
        m.aviso(b, f, 'Waka waka!', f);
      },
      causa: (_m, b, f) => ((u(f).poder ?? 0) > b.time ? 1.6 : 1),
    },
  },
  crash: {
    nome: 'Máscara protetora',
    texto: 'Crash Bandicoot começa com 1 máscara Aku Aku: cada máscara anula o próximo ataque ou habilidade que Crash receberia. A cada 20 s, Crash ganha mais 1 máscara; ao juntar 3, as máscaras viram 5 s sem receber dano nenhum.',
    ganchos: {
      inicio(_m, _b, f) { u(f).mascaras = 1; },
      passo(m, b, f, dt) {
        if (!relogio(f, 'mascara', dt, 20, 20)) return;
        u(f).mascaras = (u(f).mascaras ?? 0) + 1;
        if (u(f).mascaras! >= 3) { u(f).mascaras = 0; u(f).invencivel = b.time + 5; m.aviso(b, f, 'Aku Aku invencível!', f); }
        else m.aviso(b, f, 'Máscara', f);
      },
      recebe(m, b, f, fonte, g) {
        if ((u(f).invencivel ?? 0) > b.time) return 0;
        if (!g.direto || !(u(f).mascaras ?? 0)) return 1;
        u(f).mascaras! -= 1;
        m.aviso(b, f, 'A máscara segurou', fonte);
        return 0;
      },
    },
  },
  arthurmorgan: {
    nome: 'Mira certeira',
    texto: 'A cada 18 s, Arthur Morgan usa o Dead Eye: 3 tiros de 60 de dano, cada um no rival com menos Vida naquele momento.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'deadeye', dt, 18, 10)) return;
        m.aviso(b, f, 'Dead Eye', f);
        for (let i = 0; i < 3; i++) { const a = maisFraco(m, b, f); if (a) m.dano(b, f, a, 60, false, 'Dead Eye'); }
      },
    },
  },
  ellie: {
    nome: 'Pegar o que sobrou',
    texto: 'Quando um aliado cai, Ellie pega os suprimentos: cura 20% da Vida máxima e ganha +25% de Carga em todas as habilidades.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side) return;
        m.cura(b, f, f, f.maxHp * 0.2, 'Suprimentos');
        for (const s of f.skills) if (s.cooldown <= 0) s.charge = Math.min(100, s.charge + 25);
        m.aviso(b, f, 'Suprimentos', quem);
      },
    },
  },
  sans: {
    nome: 'Esquiva preguiçosa',
    texto: 'Sans tem 70% de chance de desviar de cada ataque ou habilidade, e cada desvio baixa essa chance em 15 pontos. A cada 10 s, Sans descansa e a chance volta a 70%.',
    ganchos: {
      passo(_m, _b, f, dt) { if (relogio(f, 'descanso', dt, 10, 10)) u(f).cansaco = 0; },
      recebe(m, b, f, fonte, g) {
        if (!g.direto) return 1;
        const chance = Math.max(0, 0.7 - 0.15 * (u(f).cansaco ?? 0));
        if (m.sorte(b) >= chance) return 1;
        u(f).cansaco = (u(f).cansaco ?? 0) + 1;
        m.aviso(b, f, 'Desviou', fonte);
        return 0;
      },
    },
  },
  dovahkiin: {
    nome: 'Devorador de almas',
    texto: 'A cada 12 s, Dovahkiin grita o Fus Ro Dah: 50 de dano em cada rival, mais 50 para cada rival que já caiu na luta.',
    ganchos: {
      caiu(m, b, f, quem) { if (quem.side !== f.side) { u(f).gritos = (u(f).gritos ?? 1) + 1; m.aviso(b, f, 'Alma absorvida', quem); } },
      passo(m, b, f, dt) {
        if (!relogio(f, 'thuum', dt, 12, 8)) return;
        const n = u(f).gritos ?? 1;
        m.aviso(b, f, 'Fus Ro Dah!', f, n);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 50 * n, false, "Thu'um");
      },
    },
  },
  yoshi: {
    nome: 'Engole e bota ovo',
    texto: 'A cada 12 s, Yoshi engole o rival com menos Vida: esse rival fica Paralisado por 2 s e depois sai como ovo, levando 90 de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f), preso = b.fighters[s.engolido ?? -1];
        if (preso && (s.ovo ?? 0) <= b.time && s.engolido !== -1) {
          s.engolido = -1;
          if (vivo(preso)) { m.aviso(b, f, 'Ovo!', preso); m.dano(b, f, preso, 90, false, 'Ovo'); }
        }
        if (!relogio(f, 'lingua', dt, 12, 7)) return;
        const a = maisFraco(m, b, f);
        if (!a) return;
        s.engolido = idx(b, a); s.ovo = b.time + 2;
        m.efeitos(b, f, [a], [st('paralyzed', 1, 2)]);
        m.aviso(b, f, 'Engoliu!', a);
      },
    },
  },
};
