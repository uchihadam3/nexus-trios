/*
 * Mecânicas únicas — lote 5: personagens antigos que tinham um "gêmeo" no
 * jeito de jogar (Seiya, Rafael, Kazuya, Bart…) e os dois últimos novos.
 */
import { fracao, maisForte, relogio, st, u, vivo, type Unica } from './unicas-base';
import type { Battle, Fighter, StatusId } from './types';

const idx = (b: Battle, f: Fighter) => b.fighters.indexOf(f);
const PROVOCACOES: StatusId[] = ['provoked', 'weakened', 'slow', 'exposed', 'marked'];

export const LOTE5: Record<string, Unica> = {
  seiya: {
    nome: 'Armadura de Pégaso',
    texto: 'Cada habilidade que o acerta dá 40 de Escudo.',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.habilidade || !vivo(f)) return;
        f.shields.push({ amount: 40, remaining: 10, source: f.uid });
        m.aviso(b, f, 'A armadura se adaptou', fonte);
      },
    },
  },
  raphael: {
    nome: 'Esquentado',
    texto: 'Cada vez que fica Provocado, Enfraquecido, Lento, Exposto ou Marcado: +15% de dano por 6 s (acumula).',
    ganchos: {
      pegouStatus(m, b, f, s) {
        if (!PROVOCACOES.includes(s)) return;
        u(f)[`raiva${Math.floor(b.time * 10)}`] = 1;
        const lista = Object.keys(u(f)).filter((k) => k.startsWith('raiva'));
        if (lista.length > 6) delete u(f)[lista[0]!];
        m.aviso(b, f, 'Agora ele ficou bravo', f);
      },
      causa: (_m, b, f) => 1 + 0.15 * Object.keys(u(f)).filter((k) => k.startsWith('raiva') && Number(k.slice(5)) / 10 > b.time - 6).length,
    },
  },
  kazuya: {
    nome: 'Chute que empurra',
    texto: 'Cada golpe direto tira 15% da ação do alvo.',
    ganchos: { bateu(_m, _b, _f, alvo, _dano, g) { if (g.direto && vivo(alvo)) alvo.action = Math.max(0, alvo.action - 0.15); } },
  },
  bart: {
    nome: 'Eu não fui!',
    texto: '1 em 4 golpes nele vão num aliado de quem bateu.',
    ganchos: {
      apanhou(m, b, f, fonte, dano, g) {
        if (!g.direto || dano < 1 || m.sorte(b) >= 0.25) return;
        const culpado = m.aliados(b, fonte).find((x) => x !== fonte);
        if (!culpado) return;
        m.cura(b, f, f, dano, 'Eu não fui!');
        m.aviso(b, f, 'Eu não fui!', culpado);
        m.dano(b, fonte, culpado, dano, false, 'Culpa do Bart');
      },
    },
  },
  cloud: {
    nome: 'Buster Sword',
    texto: 'Os golpes dele ignoram metade do Protegido do alvo.',
    ganchos: { causa: (m, _b, _f, alvo) => { const p = m.intensidade(alvo, 'protected'); return p > 0 ? (1 - p / 2) / (1 - p) : 1; } },
  },
  akuma: {
    nome: 'Satsui no Hadō',
    texto: 'Cada rival que derruba: +15% de dano, mas −5% de Vida máxima.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        u(f).satsui = (u(f).satsui ?? 0) + 1;
        f.maxHp = Math.round(f.maxHp * 0.95); f.hp = Math.min(f.hp, f.maxHp);
        m.aviso(b, f, 'Messatsu', f);
      },
      causa: (_m, _b, f) => 1 + 0.15 * (u(f).satsui ?? 0),
    },
  },
  raidenmgr: {
    nome: 'Cortar e tomar',
    texto: 'Ao derrubar um rival: cura 25% da Vida e fica Acelerado 30% por 6 s.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        m.cura(b, f, f, f.maxHp * 0.25, 'Zandatsu');
        m.efeitos(b, f, [f], [st('haste', 0.3, 6)]);
        m.aviso(b, f, 'Zandatsu', quem);
      },
    },
  },
  jotaro: {
    nome: 'Za Warudo',
    texto: 'A cada 20 s, todos os rivais ficam Paralisado 2 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'tempo', dt, 20, 12)) return;
        m.efeitos(b, f, m.rivais(b, f), [st('paralyzed', 1, 2)]);
        m.aviso(b, f, 'Za Warudo!', f);
      },
    },
  },
  daredevil: {
    nome: 'Sentido radar',
    texto: 'Não fica Cego e Esquiva não funciona contra ele. Causa 25% a mais em quem tem menos de 50% da Vida.',
    ganchos: {
      nuncaErra: true,
      imune: (_f, s) => s === 'blind',
      causa: (_m, _b, _f, alvo) => (fracao(alvo) < 0.5 ? 1.25 : 1),
    },
  },
  arlequina: {
    nome: 'Imprevisível',
    texto: 'Cada golpe direto sorteia: 80% a mais de dano, cura 30, deixa o alvo Confuso 2 s, ou nada.',
    ganchos: {
      causa(m, b, f, _alvo, g) {
        if (!g.direto) return 1;
        const k = Math.floor(m.sorte(b) * 4);
        u(f).surpresa = k;
        return k === 0 ? 1.8 : 1;
      },
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto) return;
        if (u(f).surpresa === 1) m.cura(b, f, f, 30, 'Surpresa');
        if (u(f).surpresa === 2 && vivo(alvo)) m.efeitos(b, f, [alvo], [st('confused', 1, 2)]);
        u(f).surpresa = -1;
      },
    },
  },
  samus: {
    nome: 'Raio de gelo e míssil',
    texto: 'A cada 4 ataques básicos, deixa o alvo Congelado 1 s; o golpe seguinte nele causa 60% a mais.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || g.habilidade || !vivo(alvo)) return;
        u(f).tiros = (u(f).tiros ?? 0) + 1;
        if (u(f).tiros! % 4 === 0) { m.efeitos(b, f, [alvo], [st('frozen', 0.2, 1)]); u(f).missil = idx(b, alvo); m.aviso(b, f, 'Raio de gelo', alvo); }
      },
      causa(_m, b, f, alvo, g) {
        if (!g.direto || u(f).missil !== idx(b, alvo) || (u(f).tiros ?? 0) % 4 === 0) return 1;
        u(f).missil = -1;
        return 1.6;
      },
    },
  },
  hisoka: {
    nome: 'Dor compartilhada',
    texto: 'Liga os 2 rivais mais fortes: dano do trio em um passa 30% para o outro.',
    ganchos: {
      inicio(m, b, f) {
        const rs = m.rivais(b, f).sort((x, y) => y.hp - x.hp);
        if (rs.length < 2) return;
        u(f).gruda1 = idx(b, rs[0]!); u(f).gruda2 = idx(b, rs[1]!);
        m.aviso(b, f, 'Bungee Gum', rs[0]);
      },
      viu(m, b, f, fonte, alvo, dano, g) {
        if (fonte.side !== f.side || g.label === 'Bungee Gum') return;
        const i = idx(b, alvo), s = u(f);
        const outro = i === s.gruda1 ? b.fighters[s.gruda2!] : i === s.gruda2 ? b.fighters[s.gruda1!] : undefined;
        if (outro && vivo(outro)) m.dano(b, f, outro, dano * 0.3, false, 'Bungee Gum');
      },
    },
  },
  jill: {
    nome: 'Ervas de Raccoon City',
    texto: 'Ganha uma erva a cada 16 s (até 2). Abaixo de 40% da Vida, cada erva cura 15%.',
    ganchos: {
      passo(m, b, f, dt) {
        if (relogio(f, 'erva', dt, 16, 16)) u(f).ervas = Math.min(2, (u(f).ervas ?? 0) + 1);
        if ((u(f).ervas ?? 0) > 0 && fracao(f) < 0.4) {
          u(f).ervas! -= 1;
          m.cura(b, f, f, f.maxHp * 0.15, 'Erva');
          m.aviso(b, f, 'Usou uma erva', f);
        }
      },
    },
  },
  megatron: {
    nome: 'Tiro devastador',
    texto: 'A cada 3 habilidades: 150 de dano em todos os rivais, e fica 2 s parado.',
    ganchos: {
      usou(m, b, f) {
        u(f).calor = (u(f).calor ?? 0) + 1;
        if (u(f).calor! < 3) return;
        u(f).calor = 0; u(f).esfria = b.time + 2;
        m.aviso(b, f, 'Canhão de fusão', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 150, false, 'Canhão de fusão');
      },
      parado: (f, b) => (u(f).esfria ?? 0) > b.time,
    },
  },
  nezuko: {
    nome: 'Sangue explosivo',
    texto: 'Quem a acerta com golpe direto fica Queimando (15 por s, 3 s).',
    ganchos: { apanhou(m, b, f, fonte, _dano, g) { if (g.direto && vivo(fonte) && fonte.side !== f.side) m.efeitos(b, f, [fonte], [st('burning', 15, 3)]); } },
  },
  constantine: {
    nome: 'Expulsar demônios',
    texto: 'A cada 10 s, tira Invocação e Regeneração dos rivais; cada uma tirada vira 60 de dano.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'exorcismo', dt, 10, 6)) return;
        for (const r of m.rivais(b, f)) {
          const fora = r.statuses.filter((s) => s.id === 'summon' || s.id === 'regen');
          if (!fora.length) continue;
          r.statuses = r.statuses.filter((s) => !fora.includes(s));
          m.aviso(b, f, 'Exorcizado', r);
          m.dano(b, f, r, 60 * fora.length, false, 'Exorcismo');
        }
      },
    },
  },
  yennefer: {
    nome: 'Feitiçaria instável',
    texto: '1 em 4 habilidades dela causa o dobro.',
    ganchos: {
      antes(m, b, f) { u(f).caos = m.sorte(b) < 0.25 ? 1 : 0; if (u(f).caos) m.aviso(b, f, 'Caos!', f); },
      causa: (_m, _b, f, _alvo, g) => (g.habilidade && u(f).caos ? 2 : 1),
      usou(_m, _b, f) { u(f).caos = 0; },
    },
  },
  nemesis: {
    nome: 'Caçada implacável',
    texto: 'Ataca o rival mais forte; cada golpe seguido nele causa 6% a mais (acumula até ele cair).',
    ganchos: {
      alvoDoBasico(m, b, f) {
        let v = b.fighters[u(f).caca ?? -1];
        if (!v || !vivo(v)) { v = maisForte(m, b, f); if (v) { u(f).caca = idx(b, v); u(f).golpes = 0; m.aviso(b, f, 'STARS!', v); } }
        return v;
      },
      causa(_m, b, f, alvo, g) {
        if (!g.direto || u(f).caca !== idx(b, alvo)) return 1;
        u(f).golpes = (u(f).golpes ?? 0) + 1;
        return 1 + 0.06 * Math.min(10, u(f).golpes!);
      },
    },
  },
};
