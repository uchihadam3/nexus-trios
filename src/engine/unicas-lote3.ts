/*
 * Mecânicas únicas — lote 3: deuses, terror e filmes.
 */
import { CONTROLES, curaContinua, fracao, maisFerido, maisForte, relogio, st, u, vivo, type Motor, type Unica } from './unicas-base';
import type { Battle, Effect, Fighter } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const invoca = (valor: number, duracao: number, rotulo: string): Effect => ({ kind: 'status', status: 'summon', value: valor, duration: duracao, rotulo });
const maisFraco = (m: Motor, b: Battle, f: Fighter) => m.rivais(b, f).sort((x, y) => x.hp - y.hp)[0];

export const LOTE3: Record<string, Unica> = {
  /* ───────── Olimpo ───────── */
  zeus: {
    nome: 'Ira do Olimpo',
    texto: 'A cada 9 s: 90 de dano em quem mais feriu o trio dele.',
    ganchos: {
      viu(_m, b, f, fonte, alvo, dano) { if (alvo.side === f.side && fonte.side !== f.side) u(f)[`ira${idx(b, fonte)}`] = (u(f)[`ira${idx(b, fonte)}`] ?? 0) + dano; },
      passo(m, b, f, dt) {
        if (!relogio(f, 'raio', dt, 9, 7)) return;
        const alvo = m.rivais(b, f).sort((x, y) => (u(f)[`ira${idx(b, y)}`] ?? 0) - (u(f)[`ira${idx(b, x)}`] ?? 0))[0];
        if (!alvo) return;
        m.aviso(b, f, 'Raio do Olimpo', alvo);
        m.dano(b, f, alvo, 90, false, 'Ira do Olimpo');
      },
    },
  },
  poseidon: {
    nome: 'Abalador da terra',
    texto: 'A cada 15 s, todos os rivais perdem metade da ação.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'tremor', dt, 15, 8)) return;
        for (const r of m.rivais(b, f)) r.action *= 0.5;
        m.aviso(b, f, 'Terremoto', f);
      },
    },
  },
  athena: {
    nome: 'Sabedoria compartilhada',
    texto: 'Enquanto ela está de pé, o trio causa 5% a mais e enche a Carga 10% mais rápido.',
    ganchos: {
      inicio(m, b, f) { for (const a of m.aliados(b, f)) if (a.bonus) { a.bonus.carga += 0.1; a.bonus.dano += 0.05; } },
      morreu(m, b, f) { for (const a of b.fighters) if (a.side === f.side && a.bonus) { a.bonus.carga -= 0.1; a.bonus.dano -= 0.05; } m.aviso(b, f, 'A sabedoria se foi', f); },
    },
  },
  ares: {
    nome: 'Deus da guerra',
    texto: 'Cada lutador que cai (de qualquer lado): +12% de dano até o fim.',
    ganchos: {
      caiu(m, b, f) { u(f).guerra = Math.min(6, (u(f).guerra ?? 0) + 1); m.aviso(b, f, 'Mais guerra', f, u(f).guerra); },
      causa: (_m, _b, f) => 1 + 0.12 * (u(f).guerra ?? 0),
    },
  },
  apollo: {
    nome: 'Flechas de sol',
    texto: 'A cada 2 ataques básicos, um cura 60 no aliado mais ferido em vez de causar dano.',
    ganchos: {
      causa(m, b, f, _alvo, g) {
        if (!g.direto || g.habilidade) return 1;
        u(f).flecha = ((u(f).flecha ?? 0) + 1) % 2;
        if (u(f).flecha !== 0) return 1;
        const a = maisFerido(m, b, f);
        if (a) m.cura(b, f, a, 60, 'Flecha de sol');
        return 0;
      },
    },
  },
  hermes: {
    nome: 'Mensageiro veloz',
    texto: 'As habilidades dele saem sem Preparo.',
    ganchos: { preparo: () => 0 },
  },
  aphrodite: {
    nome: 'Pomo da discórdia',
    texto: 'A cada 10 s, o rival mais forte causa 80 de dano em outro rival.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'pomo', dt, 10, 7)) return;
        const rs = m.rivais(b, f).sort((x, y) => y.hp - x.hp);
        if (rs.length < 2) return;
        m.aviso(b, f, 'Discórdia', rs[1]);
        m.dano(b, rs[0]!, rs[1]!, 80, false, 'Discórdia');
      },
    },
  },
  medusa: {
    nome: 'Olhar de pedra',
    texto: '1 em 5 que a atacam ficam Paralisado 2 s.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.direto || !vivo(fonte) || m.sorte(b) >= 0.2) return;
        m.efeitos(b, f, [fonte], [st('paralyzed', 1, 2)]);
        m.aviso(b, f, 'Virou pedra', fonte);
      },
    },
  },
  kronos: {
    nome: 'Voltar no tempo',
    texto: 'Abaixo de 30% da Vida (uma vez), volta à Vida que tinha 10 s antes.',
    ganchos: {
      passo(_m, b, f) {
        const s = u(f), seg = Math.floor(b.time);
        if (s.ultimo === seg) return;
        s.ultimo = seg;
        s[`h${seg % 10}`] = f.hp;
      },
      apanhou(m, b, f) {
        const s = u(f);
        if (s.voltou || fracao(f) >= 0.3 || b.time < 10) return;
        const antes = s[`h${(Math.floor(b.time) + 1) % 10}`] ?? f.hp;
        if (antes <= f.hp) return;
        s.voltou = 1;
        m.aviso(b, f, 'O tempo voltou', f);
        m.cura(b, f, f, antes - f.hp, 'Voltar no tempo');
      },
    },
  },

  /* ───────── Egito e Nórdicos ───────── */
  anubis: {
    nome: 'Guia das almas',
    texto: 'Cada rival que cai: +10% de Vida máxima e cura 10%.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side === f.side) return;
        f.maxHp = Math.round(f.maxHp * 1.1);
        m.cura(b, f, f, f.maxHp * 0.1, 'Guia das almas');
        m.aviso(b, f, 'Alma pesada', quem);
      },
    },
  },
  set: {
    nome: 'Tempestade do deserto',
    texto: 'A cada 10 s, todos os rivais ficam Cego 2 s. Causa 30% a mais em quem está Cego.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'areia', dt, 10, 6)) { m.efeitos(b, f, m.rivais(b, f), [st('blind', 0.3, 2)]); m.aviso(b, f, 'Tempestade de areia', f); } },
      causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'blind') > 0 ? 1.3 : 1),
    },
  },
  horus: {
    nome: 'Olho que tudo vê',
    texto: 'Enquanto ele está de pé, os golpes do trio ignoram Esquiva e Cego.',
    ganchos: { trioNuncaErra: true },
  },
  sekhmet: {
    nome: 'Cheiro de sangue',
    texto: 'Com algum rival Sangrando: age 30% mais rápido e cura 10% do dano que causa.',
    ganchos: {
      ritmo: (m, b, f) => (m.rivais(b, f).some((r) => m.intensidade(r, 'bleed') > 0) ? 1.3 : 1),
      bateu(m, b, f, _alvo, dano) { if (m.rivais(b, f).some((r) => m.intensidade(r, 'bleed') > 0)) m.cura(b, f, f, dano * 0.1, 'Cheiro de sangue'); },
    },
  },
  odin: {
    nome: 'Os corvos contam tudo',
    texto: 'A cada 10 s, a habilidade rival mais perto de sair perde 30 de Carga.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'corvos', dt, 10, 6)) return;
        let melhor: { r: Fighter; i: number } | undefined;
        for (const r of m.rivais(b, f)) r.skills.forEach((s, i) => { if (!melhor || s.charge > melhor.r.skills[melhor.i]!.charge) melhor = { r, i }; });
        if (!melhor) return;
        const sk = melhor.r.skills[melhor.i]!;
        sk.charge = Math.max(0, sk.charge - 30);
        m.aviso(b, f, 'Os corvos viram', melhor.r);
      },
    },
  },
  fenrir: {
    nome: 'Gleipnir',
    texto: 'Nos primeiros 12 s causa 40% a menos. Depois, até o fim: 40% a mais e age 15% mais rápido.',
    ganchos: {
      passo(m, b, f) { if (!u(f).solto && b.time >= 12) { u(f).solto = 1; m.aviso(b, f, 'Correntes quebradas', f); } },
      causa: (_m, b) => (b.time < 12 ? 0.6 : 1.4),
      ritmo: (_m, b) => (b.time < 12 ? 1 : 1.15),
    },
  },
  hel: {
    nome: 'Exército dos mortos',
    texto: 'Aliado que cai volta com 30% da Vida, mas cai de novo 8 s depois.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side || quem.voltou || (quem.renascendo ?? 0) > 0) return;
        m.levanta(b, f, quem, 0.3);
        u(f)[`morto${idx(b, quem)}`] = b.time + 8;
        m.aviso(b, f, 'Morto-vivo', quem);
      },
      passo(m, b, f) {
        for (const a of m.aliados(b, f)) {
          const k = `morto${idx(b, a)}`, ate = u(f)[k];
          if (!ate || b.time < ate) continue;
          u(f)[k] = 0;
          m.dano(b, f, a, a.hp + 1, false, 'O corpo desabou');
        }
      },
    },
  },

  /* ───────── Terror ───────── */
  jason: {
    nome: 'Implacável',
    texto: 'Nenhum golpe tira mais de 150 de Vida dele.',
    ganchos: { limita: (_m, _b, f, alvo, valor) => (alvo === f ? Math.min(valor, 150) : valor) },
  },
  freddy: {
    nome: 'Dentro do sonho',
    texto: 'Os golpes dele não acordam quem está Dormindo e causam o dobro em quem dorme.',
    ganchos: {
      naoAcorda: true,
      causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'sleep') > 0 ? 2 : 1),
    },
  },
  michaelmyers: {
    nome: 'A perseguição',
    texto: 'Só ataca o rival mais fraco, com 50% a mais. Quando ele cai, passa ao próximo.',
    ganchos: {
      alvoDoBasico(m, b, f) {
        let v = b.fighters[u(f).vitima ?? -1];
        if (!v || !vivo(v)) { v = maisFraco(m, b, f); if (v) { u(f).vitima = idx(b, v); m.aviso(b, f, 'Escolheu a vítima', v); } }
        return v;
      },
      causa: (_m, b, f, alvo) => (u(f).vitima === idx(b, alvo) ? 1.5 : 1),
    },
  },
  chucky: {
    nome: 'Troca de alma',
    texto: 'Abaixo de 20% da Vida (uma vez), troca de Vida (em %) com o rival mais saudável, até 60%.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).trocou || fracao(f) >= 0.2) return;
        const alvo = m.rivais(b, f).sort((x, y) => fracao(y) - fracao(x))[0];
        if (!alvo || fracao(alvo) <= fracao(f)) return;
        u(f).trocou = 1;
        const minha = fracao(f), dele = fracao(alvo);
        f.hp = f.maxHp * Math.min(0.6, dele);
        alvo.hp = Math.max(1, alvo.maxHp * minha);
        m.aviso(b, f, 'Damballa!', alvo);
      },
    },
  },
  pennywise: {
    nome: 'Come medo',
    texto: 'Por rival com Status ruim: cura 5 por segundo e causa 6% a mais.',
    ganchos: {
      passo(m, b, f, dt) { const n = comMedo(m, b, f); if (n) curaContinua(m, b, f, f, 5 * n * dt, 'Come medo'); },
      causa: (m, b, f) => 1 + 0.06 * comMedo(m, b, f),
    },
  },
  ghostface: {
    nome: 'Dois assassinos',
    texto: 'A cada 3 ataques básicos, acerta também outro rival com metade.',
    ganchos: {
      bateu(m, b, f, alvo, dano, g) {
        if (!g.direto || g.habilidade) return;
        u(f).facadas = (u(f).facadas ?? 0) + 1;
        if (u(f).facadas! % 3 !== 0) return;
        const outro = m.rivais(b, f).find((r) => r !== alvo) ?? alvo;
        if (!vivo(outro)) return;
        m.aviso(b, f, 'O outro Ghostface', outro);
        m.dano(b, f, outro, dano * 0.5, false, 'Segundo assassino');
      },
    },
  },
  leatherface: {
    nome: 'Corte que não fecha',
    texto: 'Cada golpe direto tira 25 da Vida máxima do alvo (até metade).',
    ganchos: {
      bateu(_m, _b, _f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const base = alvo.u?.vidaOriginal ?? alvo.maxHp;
        (alvo.u ??= {}).vidaOriginal = base;
        alvo.maxHp = Math.max(base * 0.5, alvo.maxHp - 25);
        alvo.hp = Math.min(alvo.hp, alvo.maxHp);
      },
    },
  },
  pinhead: {
    nome: 'A caixa se abre',
    texto: 'Rival que chega a 30% da Vida fica Paralisado 3 s e Sangrando (25 por s, 6 s). Uma vez por rival.',
    ganchos: {
      viu(m, b, f, _fonte, alvo) {
        if (alvo.side === f.side || !vivo(alvo) || fracao(alvo) >= 0.3 || u(f)[`caixa${idx(b, alvo)}`]) return;
        u(f)[`caixa${idx(b, alvo)}`] = 1;
        m.efeitos(b, f, [alvo], [st('paralyzed', 1, 3), st('bleed', 25, 6)]);
        m.aviso(b, f, 'A caixa se abriu', alvo);
      },
    },
  },
  samara: {
    nome: 'Sete dias',
    texto: 'Se ela estiver de pé aos 35 s, o rival mais forte cai. Derrubá-la antes desfaz.',
    ganchos: {
      inicio(m, b, f) { const a = maisForte(m, b, f); if (a) { u(f).fita = idx(b, a); m.aviso(b, f, 'Sete dias…', a); } },
      passo(m, b, f) {
        const s = u(f), alvo = b.fighters[s.fita ?? -1];
        if (!alvo || !vivo(alvo) || s.fim) return;
        const dia = Math.min(7, Math.floor(b.time / 5) + 1);
        if (dia !== s.dia) { s.dia = dia; if (dia < 7) m.aviso(b, f, `Dia ${dia}`, alvo, dia); }
        if (b.time >= 35) { s.fim = 1; m.aviso(b, f, 'Saiu da TV', alvo); m.dano(b, f, alvo, alvo.hp + 1, false, 'Sete dias'); }
      },
    },
  },
  valak: {
    nome: 'Aparição',
    texto: 'A cada 10 s, o próximo golpe no rival com menos Vida causa o dobro e o deixa Confuso 2 s.',
    ganchos: {
      passo(m, b, f, dt) { if (relogio(f, 'aparece', dt, 10, 6)) { const a = maisFraco(m, b, f); if (a) { u(f).atras = idx(b, a); m.aviso(b, f, 'Atrás de você', a); } } },
      causa: (_m, b, f, alvo, g) => (g.direto && u(f).atras === idx(b, alvo) ? 2 : 1),
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && u(f).atras === idx(b, alvo)) { u(f).atras = -1; if (vivo(alvo)) m.efeitos(b, f, [alvo], [st('confused', 1, 2)]); } },
    },
  },
  dracula: {
    nome: 'Névoa',
    texto: 'Abaixo de 30% da Vida (uma vez), por 4 s: não leva dano nem ataca, e cura 15%.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).nevoa || fracao(f) >= 0.3) return;
        u(f).nevoa = b.time + 4;
        m.cura(b, f, f, f.maxHp * 0.15, 'Névoa');
        m.aviso(b, f, 'Virou névoa', f);
      },
      recebe: (_m, b, f) => ((u(f).nevoa ?? 0) > b.time ? 0 : 1),
      parado: (f, b) => (u(f).nevoa ?? 0) > b.time,
    },
  },
  xenomorph: {
    nome: 'Colmeia',
    texto: 'Cada rival que ele derruba vira uma cria que luta ao lado dele por 20 s.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        m.efeitos(b, f, [f], [invoca(40, 20, 'Cria do Xenomorfo')]);
        m.aviso(b, f, 'Nasceu uma cria', quem);
      },
    },
  },

  /* ───────── Filmes ───────── */
  yoda: {
    nome: 'Equilíbrio da Força',
    texto: 'A cada 12 s: se o trio tem menos Vida que os rivais, cura 8% de todos; se tem mais, dá Barreira a todos.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'forca', dt, 12, 8)) return;
        const soma = (xs: Fighter[]) => xs.reduce((n, x) => n + fracao(x), 0) / 3;
        const nos = m.aliados(b, f), eles = m.rivais(b, f);
        if (soma(nos) < soma(eles)) { for (const a of nos) m.cura(b, f, a, a.maxHp * 0.08, 'Equilíbrio'); m.aviso(b, f, 'Equilíbrio: cura', f); }
        else { m.efeitos(b, f, nos, [st('barrier', 1, 6)]); m.aviso(b, f, 'Equilíbrio: barreira', f); }
      },
    },
  },
  luke: {
    nome: 'Última esperança',
    texto: 'Quando fica sozinho: cura 30% da Vida e causa 50% a mais até o fim.',
    ganchos: {
      caiu(m, b, f, quem) {
        if (quem.side !== f.side || u(f).esperanca || m.aliados(b, f).length !== 1) return;
        u(f).esperanca = 1;
        m.cura(b, f, f, f.maxHp * 0.3, 'Esperança');
        m.aviso(b, f, 'Uma nova esperança', f);
      },
      causa: (_m, _b, f) => (u(f).esperanca ? 1.5 : 1),
    },
  },
  agentsmith: {
    nome: 'Mais de mim',
    texto: 'A cada 12 s, cria uma cópia (até 3) que luta junto. Mais cópias, ataques mais fortes.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'copias', dt, 12, 8)) return;
        u(f).copias = Math.min(3, (u(f).copias ?? 0) + 1);
        m.efeitos(b, f, [f], [invoca(18 * u(f).copias!, 12, `Cópias do Smith ×${u(f).copias}`)]);
        m.aviso(b, f, `Mais um Smith (${u(f).copias})`, f, u(f).copias);
      },
    },
  },
  johnwick: {
    nome: 'Baba Yaga',
    texto: 'Cada rival que ele derruba deixa todas as habilidades dele Pronta.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        for (const s of f.skills) { s.charge = 100; s.cooldown = 0; }
        m.aviso(b, f, 'Recarregou', f);
      },
    },
  },
  robocop: {
    nome: 'Corpo de metal',
    texto: 'Não fica Sangrando, Envenenado nem Queimando, mas age 10% mais devagar.',
    ganchos: {
      imune: (_f, s) => s === 'bleed' || s === 'poison' || s === 'burning',
      ritmo: () => 0.9,
    },
  },
  rambo: {
    nome: 'Exército de um homem só',
    texto: '+12% de dano por aliado caído e por rival de pé além do primeiro.',
    ganchos: { causa: (m, b, f) => 1 + 0.12 * (3 - m.aliados(b, f).length + Math.max(0, m.rivais(b, f).length - 1)) },
  },
  indianajones: {
    nome: 'Chicotada',
    texto: 'A cada 8 s, o rival mais forte perde Fortalecido e Escudo e fica Enfraquecido 25% por 4 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'chicote', dt, 8, 5)) return;
        const a = maisForte(m, b, f);
        if (!a) return;
        a.statuses = a.statuses.filter((s) => s.id !== 'strengthened');
        a.shields = [];
        m.efeitos(b, f, [a], [st('weakened', 0.25, 4)]);
        m.aviso(b, f, 'Desarmado', a);
      },
    },
  },
  jacksparrow: {
    nome: 'Parlay!',
    texto: 'Abaixo de 30% da Vida (uma vez), nenhum golpe o acerta por 3 s.',
    ganchos: {
      apanhou(m, b, f) { if (!u(f).parlay && fracao(f) < 0.3) { u(f).parlay = b.time + 3; m.aviso(b, f, 'Parlay!', f); } },
      recebe: (_m, b, f) => ((u(f).parlay ?? 0) > b.time ? 0 : 1),
    },
  },
  harrypotter: {
    nome: 'Proteção da mãe',
    texto: 'O primeiro golpe que o derrubaria volta inteiro em quem lançou.',
    ganchos: {
      salva(m, b, f, alvo, dano, fonte) {
        if (alvo !== f || u(f).mae) return null;
        u(f).mae = 1;
        m.aviso(b, f, 'O golpe voltou', fonte);
        if (fonte !== f && vivo(fonte)) m.dano(b, f, fonte, dano, false, 'Proteção da mãe');
        return f.hp;
      },
    },
  },
  voldemort: {
    nome: 'Horcruxes',
    texto: '3 vezes, com um aliado de pé: o golpe que o derrubaria o deixa com 1 de Vida.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo !== f || (u(f).horcrux ?? 0) >= 3 || m.aliados(b, f).length < 2) return null;
        u(f).horcrux = (u(f).horcrux ?? 0) + 1;
        m.aviso(b, f, `Horcrux destruída (${u(f).horcrux}/3)`, f);
        return 1;
      },
    },
  },
  gandalf: {
    nome: 'O Branco',
    texto: 'Ao cair, volta 12 s depois com 60% da Vida, causando 30% a mais.',
    ganchos: {
      morreu(m, b, f) { if (!f.voltou && !u(f).branco) { u(f).branco = 1; f.renascendo = 12; m.aviso(b, f, 'Ele vai voltar', f); } },
      passo(m, b, f) {
        if (u(f).branco !== 1 || !f.voltou) return;
        u(f).branco = 2;
        if (f.hp < f.maxHp * 0.6) m.cura(b, f, f, f.maxHp * 0.6 - f.hp, 'O Branco');
        m.aviso(b, f, 'Gandalf, o Branco', f);
      },
      causa: (_m, _b, f) => (u(f).branco === 2 ? 1.3 : 1),
    },
  },
};

function comMedo(m: Motor, b: Battle, f: Fighter): number {
  return m.rivais(b, f).filter((r) => r.statuses.some((s) => CONTROLES.includes(s.id) || ['provoked', 'blind', 'cursed', 'exposed', 'weakened', 'poison', 'bleed', 'burning', 'marked', 'electric'].includes(s.id))).length;
}
