/*
 * Mecânicas únicas: uma regra que só aquele personagem tem, como a Death Note
 * do Light. Os tipos e as funções auxiliares estão em unicas-base.ts; cada lote
 * de personagens fica no seu arquivo.
 */
import { BUFFS, CONTROLES, fracao, maisFerido, maisForte, relogio, st, trabalho, u, vivo, type Unica } from './unicas-base';
import { LOTE2 } from './unicas-lote2';
import { LOTE3 } from './unicas-lote3';
import { LOTE4 } from './unicas-lote4';
import { LOTE5 } from './unicas-lote5';
import { LOTE6 } from './unicas-lote6';
import { LOTE7 } from './unicas-lote7';
import { LOTE8 } from './unicas-lote8';
import { LOTE9, conheceTodas } from './unicas-lote9';
export type { Ganchos, Golpe, Motor, Unica } from './unicas-base';

const LOTE1: Record<string, Unica> = {
  /* ───────── Força bruta, cada um do seu jeito ───────── */
  drax: {
    nome: 'Vingança',
    texto: 'Causa 60% a mais em quem derrubou um aliado. Não fica Confuso.',
    ganchos: {
      caiu(m, b, f, quem, quemDerrubou) {
        if (quem.side !== f.side || quemDerrubou.side === f.side) return;
        u(f).vinganca = b.fighters.indexOf(quemDerrubou);
        m.aviso(b, f, 'Vingança!', quemDerrubou);
      },
      causa: (_m, b, f, alvo) => (u(f).vinganca !== undefined && b.fighters[u(f).vinganca!] === alvo ? 1.6 : 1),
      imune: (_f, s) => s === 'confused',
    },
  },
  johnnybravo: {
    nome: 'Cantada',
    texto: 'A cada 10 s: 1 em 3 deixa o rival mais forte Confuso 3 s; senão, Johnny fica Fortalecido 30% por 6 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'cantada', dt, 10, 6)) return;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        if (m.sorte(b) < 1 / 3) { m.efeitos(b, f, [alvo], [st('confused', 1, 3)]); m.aviso(b, f, 'Cantada certeira', alvo); }
        else { m.efeitos(b, f, [f], [st('strengthened', 0.3, 6)]); m.aviso(b, f, 'Levou um fora', f); }
      },
    },
  },
  hercules: {
    nome: 'Doze trabalhos',
    texto: 'Cada habilidade soma 2, cada rival derrubado 4. Em 12: causa 35% a mais e recebe 25% a menos até o fim.',
    ganchos: {
      usou(m, b, f) { trabalho(m, b, f, 2); },
      caiu(m, b, f, quem, quemDerrubou) { if (quemDerrubou === f && quem.side !== f.side) trabalho(m, b, f, 4); },
      causa: (_m, _b, f) => (u(f).deus ? 1.35 : 1),
      recebe: (_m, _b, f) => (u(f).deus ? 0.75 : 1),
    },
  },
  allmight: {
    nome: 'Tempo limitado',
    texto: 'Começa causando 40% a mais e perde 6% a cada 10 s, até 20% a menos. Abaixo de 30% da Vida (uma vez), a próxima habilidade causa o dobro.',
    ganchos: {
      passo(_m, _b, f, dt) {
        const s = u(f);
        s.tempo = (s.tempo ?? 0) + dt;
        if (!s.plus && fracao(f) < 0.3) { s.plus = 1; s.pronto = 1; }
      },
      causa(m, b, f, _alvo, g) {
        const s = u(f), forma = Math.max(-0.2, 0.4 - 0.06 * Math.floor((s.tempo ?? 0) / 10));
        let k = 1 + forma;
        if (s.pronto && g.habilidade) { k *= 2; s.gasto = 1; m.aviso(b, f, 'Plus Ultra!', f); }
        return k;
      },
      usou(_m, _b, f) { if (u(f).gasto) { u(f).pronto = 0; u(f).gasto = 0; } },
    },
  },
  popeye: {
    nome: 'Espinafre',
    texto: 'Com 40% da Vida (uma vez): cura 25% e fica Fortalecido 40% e Acelerado por 8 s.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).lata || fracao(f) > 0.4) return;
        u(f).lata = 1;
        m.cura(b, f, f, f.maxHp * 0.25, 'Espinafre');
        m.efeitos(b, f, [f], [st('strengthened', 0.4, 8), st('haste', 0.3, 8)]);
        m.aviso(b, f, 'Espinafre!', f);
      },
    },
  },
  homer: {
    nome: 'Soneca',
    texto: 'A cada 18 s, fica 3 s parado curando 4% por segundo. O golpe seguinte causa 80% a mais.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f);
        if (s.dormindo) {
          s.dormindo -= dt;
          m.cura(b, f, f, f.maxHp * 0.04 * dt, 'Soneca');
          if (s.dormindo <= 1e-6) { s.dormindo = 0; s.acordou = 1; m.aviso(b, f, "D'oh!", f); }
          return;
        }
        if (relogio(f, 'sono', dt, 18, 12)) { s.dormindo = 3; m.aviso(b, f, 'Cochilo', f); }
      },
      parado: (f) => (u(f).dormindo ?? 0) > 0,
      causa: (_m, _b, f, _alvo, g) => (u(f).acordou && g.direto ? 1.8 : 1),
      bateu(_m, _b, f, _alvo, _dano, g) { if (g.direto) u(f).acordou = 0; },
    },
  },

  /* ───────── Caçadores ───────── */
  artemis: {
    nome: 'Flecha que nunca erra',
    texto: 'Os golpes dela ignoram Esquiva e Cego. Causa 40% a mais em quem tem Esquiva, Barreira ou Invocação.',
    ganchos: {
      nuncaErra: true,
      causa: (m, _b, _f, alvo) => (m.intensidade(alvo, 'evasion') > 0 || m.intensidade(alvo, 'barrier') > 0 || m.intensidade(alvo, 'summon') > 0 ? 1.4 : 1),
    },
  },
  predator: {
    nome: 'Camuflagem e troféus',
    texto: 'Nos primeiros 8 s não leva golpe. Cada rival que ele derruba: +15% de dano até o fim.',
    ganchos: {
      inicio(m, b, f) { m.aviso(b, f, 'Camuflado', f); },
      recebe: (_m, b, _f, _fonte, g) => (g.direto && b.time < 8 ? 0 : 1),
      caiu(m, b, f, quem, quemDerrubou) {
        if (quemDerrubou !== f || quem.side === f.side) return;
        u(f).trofeus = (u(f).trofeus ?? 0) + 1;
        m.aviso(b, f, `Troféu ${u(f).trofeus}`, f, u(f).trofeus);
      },
      causa: (_m, _b, f) => 1 + 0.15 * (u(f).trofeus ?? 0),
    },
  },

  /* ───────── Máquinas ───────── */
  ultron: {
    nome: 'Corpos de reserva',
    texto: 'Ao cair, volta com 25% da Vida (até 2 vezes), 20% mais fraco a cada volta.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo !== f || (u(f).corpos ?? 0) >= 2) return null;
        u(f).corpos = (u(f).corpos ?? 0) + 1;
        f.statuses = []; f.cast = null;
        m.aviso(b, f, `Corpo novo (${u(f).corpos}/2)`, f);
        return f.maxHp * 0.25;
      },
      causa: (_m, _b, f) => 1 - 0.2 * (u(f).corpos ?? 0),
    },
  },
  cyborg: {
    nome: 'Hacker',
    texto: 'A cada 9 s, rouba o melhor Status bom de um rival.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'hack', dt, 9, 5)) return;
        for (const id of BUFFS) {
          const dono = m.rivais(b, f).find((r) => r.statuses.some((s) => s.id === id));
          if (!dono) continue;
          const s = dono.statuses.find((x) => x.id === id)!;
          dono.statuses = dono.statuses.filter((x) => x !== s);
          m.efeitos(b, f, [f], [st(id, s.intensity, Math.max(2, s.remaining))]);
          m.aviso(b, f, 'Hackeado!', dono);
          return;
        }
      },
    },
  },
  t800: {
    nome: 'Exterminador',
    texto: 'Não fica Paralisado, Congelado, Dormindo, Confuso, Silenciado, Lento nem Preso. Recebe metade da cura.',
    ganchos: {
      imune: (_f, s) => CONTROLES.includes(s),
      curaRecebida: () => 0.5,
    },
  },

  /* ───────── Espadas ───────── */
  zoro: {
    nome: 'Nada aconteceu',
    texto: 'Uma vez: um aliado que ia cair fica de pé, e Zoro leva o golpe (sem cair).',
    ganchos: {
      salva(m, b, f, alvo, dano) {
        if (alvo === f || u(f).nada || !vivo(f)) return null;
        u(f).nada = 1;
        f.hp = Math.max(1, f.hp - dano);
        m.aviso(b, f, 'Nada aconteceu.', alvo);
        return alvo.hp;
      },
    },
  },
  inuyasha: {
    nome: 'Ferida do vento',
    texto: 'Guarda 25% do dano que o trio leva (até 500). A habilidade mais forte solta tudo no rival mais forte.',
    ganchos: {
      viu(_m, _b, f, fonte, alvo, dano) {
        if (alvo.side === f.side && fonte.side !== f.side) u(f).vento = Math.min(500, (u(f).vento ?? 0) + dano / 4);
      },
      usou(m, b, f, i) {
        const v = u(f).vento ?? 0;
        if (i !== 2 || v < 30) return;
        const alvo = maisForte(m, b, f);
        u(f).vento = 0;
        if (alvo) { m.aviso(b, f, 'Bakuryūha!', alvo, v); m.dano(b, f, alvo, v, true, 'Bakuryūha'); }
      },
    },
  },
  kenshin: {
    nome: 'Battōjutsu',
    texto: 'Quando um rival começa um Preparo: +15 de Carga em todas as habilidades e a próxima causa 25% a mais.',
    ganchos: {
      viuPreparo(m, b, f, quem) {
        if ((u(f).esperaSaque ?? 0) > b.time) return;
        u(f).esperaSaque = b.time + 4;
        for (const s of f.skills) if (s.cooldown <= 0) s.charge = Math.min(100, s.charge + 15);
        u(f).saque = 1;
        m.aviso(b, f, 'Battōjutsu', quem);
      },
      causa: (_m, _b, f, _alvo, g) => (u(f).saque && g.habilidade ? 1.25 : 1),
      usou(_m, _b, f) { u(f).saque = 0; },
    },
  },
  vash: {
    nome: 'Pacifista',
    texto: 'Não derruba ninguém (deixa com 1 de Vida). Causa 25% a mais e cada golpe deixa o alvo Enfraquecido 15% por 5 s.',
    ganchos: {
      poupa: true,
      causa: () => 1.25,
      bateu(m, b, f, alvo, _dano, g) { if (g.direto && vivo(alvo)) m.efeitos(b, f, [alvo], [st('weakened', 0.15, 5)]); },
    },
  },

  /* ───────── Reações ───────── */
  mob: {
    nome: '???%',
    texto: 'Enche com a Vida que o trio perde. Cheio: 260 de dano em todos os rivais e Paralisado 1,5 s; depois zera.',
    ganchos: {
      viu(m, b, f, fonte, alvo, dano) {
        if (alvo.side !== f.side || fonte.side === f.side) return;
        const s = u(f);
        s.emocao = (s.emocao ?? 0) + (100 * dano) / alvo.maxHp;
        if (s.emocao < 100) return;
        s.emocao = 0;
        m.aviso(b, f, '100%', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 260, true, '???%');
        m.efeitos(b, f, m.rivais(b, f), [st('paralyzed', 1, 1.5)]);
      },
    },
  },
  natsu: {
    nome: 'Come fogo',
    texto: 'Não fica Queimando. Cada vez que alguém pega fogo: cura 40 e +8% de dano (até 5 vezes).',
    ganchos: {
      imune: (_f, s) => s === 'burning',
      passo(m, b, f) {
        const queimando = b.fighters.filter((x) => vivo(x) && x !== f && x.statuses.some((s) => s.id === 'burning')).length;
        const s = u(f);
        if (queimando > (s.chamas ?? 0)) {
          s.fome = Math.min(5, (s.fome ?? 0) + 1);
          m.cura(b, f, f, 40, 'Come fogo');
          m.aviso(b, f, 'Come fogo', f, s.fome);
        }
        s.chamas = queimando;
      },
      causa: (_m, _b, f) => 1 + 0.08 * (u(f).fome ?? 0),
    },
  },
  sanji: {
    nome: 'Cozinheiro do navio',
    texto: 'A cada 15 s: o aliado mais ferido cura 12% e fica Fortalecido 15% por 6 s.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'cozinha', dt, 15, 10)) return;
        const alvo = maisFerido(m, b, f);
        if (!alvo) return;
        m.cura(b, f, alvo, alvo.maxHp * 0.12, 'Refeição');
        m.efeitos(b, f, [alvo], [st('strengthened', 0.15, 6)]);
        m.aviso(b, f, 'Refeição servida', alvo);
      },
    },
  },
  ken: {
    nome: 'Parry perfeito',
    texto: 'A cada 10 s, bloqueia o próximo golpe direto e devolve 80 de dano.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.direto || (u(f).parry ?? 0) > b.time) return 1;
        u(f).parry = b.time + 10;
        m.aviso(b, f, 'Parry!', fonte);
        m.dano(b, f, fonte, 80, false, 'Shōryūken');
        return 0;
      },
    },
  },
  cuphead: {
    nome: 'Cartas de Super',
    texto: 'A cada 20 golpes dados: 380 de dano no rival mais forte. 1 em 4 golpes recebidos não pega e conta 4.',
    ganchos: {
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto) return;
        const s = u(f);
        s.golpes = (s.golpes ?? 0) + 1;
        if (s.golpes % 4 === 0) s.cartas = (s.cartas ?? 0) + 1;
        if ((s.cartas ?? 0) >= 5) {
          s.cartas = 0;
          const alvo = maisForte(m, b, f);
          if (alvo) { m.aviso(b, f, 'Super!', alvo); m.dano(b, f, alvo, 380, false, 'Super'); }
        }
      },
      recebe(m, b, f, fonte, g) {
        if (!g.direto) return 1;
        const s = u(f);
        s.recebidos = (s.recebidos ?? 0) + 1;
        if (s.recebidos % 4 !== 0) return 1;
        s.cartas = (s.cartas ?? 0) + 1;
        m.aviso(b, f, 'Parry rosa', fonte);
        return 0;
      },
    },
  },
  neo: {
    nome: 'Desvia de balas',
    texto: 'Desvia de metade dos ataques básicos rivais.',
    ganchos: {
      recebe(m, b, f, fonte, g) {
        if (!g.direto || g.habilidade || m.sorte(b) >= 0.5) return 1;
        m.aviso(b, f, 'Desviou', fonte);
        return 0;
      },
    },
  },
  spike: {
    nome: 'Seja água',
    texto: 'Age mais rápido quanto menos Vida tem (até 60% mais rápido com 20%).',
    ganchos: {
      ritmo: (_m, _b, f) => 1 + Math.max(0, Math.min(0.6, (1 - fracao(f)) * 0.75)),
    },
  },
  hollowknight: {
    nome: 'Alma',
    texto: 'Cada golpe dado enche a Alma. Cheia e abaixo de 60% da Vida: 1 s parado e cura 25%.',
    ganchos: {
      bateu(_m, _b, f, _alvo, dano, g) { if (g.direto) u(f).alma = Math.min(100, (u(f).alma ?? 0) + dano / 6); },
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.foco ?? 0) > 0) { s.foco! -= dt; if (s.foco! <= 1e-6) { s.foco = 0; m.cura(b, f, f, f.maxHp * 0.25, 'Foco'); } return; }
        if ((s.alma ?? 0) >= 100 && fracao(f) < 0.6) { s.alma = 0; s.foco = 1; m.aviso(b, f, 'Foco', f); }
      },
      parado: (f) => (u(f).foco ?? 0) > 0,
    },
  },

  /* ───────── Transformações ───────── */
  jin: {
    nome: 'Gene Devil',
    texto: 'Com 50% da Vida, até o fim: causa 20% a mais e ganha 15% de Esquiva.',
    ganchos: {
      apanhou(m, b, f) {
        if (u(f).diabo || fracao(f) > 0.5) return;
        u(f).diabo = 1;
        m.efeitos(b, f, [f], [st('evasion', 0.15, 999)]);
        m.aviso(b, f, 'Devil Jin', f);
      },
      causa: (_m, _b, f) => (u(f).diabo ? 1.2 : 1),
    },
  },
  garou: {
    nome: 'Monstro que evolui',
    texto: 'Cada habilidade que o acerta: +3% de dano e −2% de dano recebido (até 30% e 20%).',
    ganchos: {
      apanhou(m, b, f, fonte, _dano, g) {
        if (!g.habilidade) return;
        const s = u(f);
        if ((s.evolucao ?? 0) >= 10) return;
        s.evolucao = (s.evolucao ?? 0) + 1;
        m.aviso(b, f, `Evoluiu (${s.evolucao})`, fonte, s.evolucao);
      },
      causa: (_m, _b, f) => 1 + 0.03 * (u(f).evolucao ?? 0),
      recebe: (_m, _b, f) => 1 - 0.02 * (u(f).evolucao ?? 0),
    },
  },
  guts: {
    nome: 'Armadura do Berserker',
    texto: 'Ao chegar a 0 de Vida, luta mais 6 s causando 50% a mais. Depois cai.',
    ganchos: {
      salva(m, b, f, alvo) {
        if (alvo !== f || u(f).berserk) return null;
        u(f).berserk = b.time + 6;
        m.aviso(b, f, 'Berserker', f);
        return 1;
      },
      recebe: (_m, b, f) => (u(f).berserk && b.time < u(f).berserk! ? 0 : 1),
      causa: (_m, b, f) => (u(f).berserk && b.time < u(f).berserk! ? 1.5 : 1),
      passo(m, b, f) {
        if (u(f).berserk && !u(f).caiu && b.time >= u(f).berserk!) { u(f).caiu = 1; m.dano(b, f, f, f.hp + 1, false, 'Fim do Berserker'); }
      },
    },
  },
  todoroki: {
    nome: 'Metade e metade',
    texto: 'Habilidades alternam Lento e Queimando. Rival com os dois leva 180 de dano e perde ambos.',
    ganchos: {
      usou(m, b, f) {
        const s = u(f), lado = (s.lado ?? 0) % 2;
        s.lado = lado + 1;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        m.efeitos(b, f, [alvo], [lado === 0 ? st('slow', 0.25, 5) : st('burning', 14, 5)]);
        if (alvo.statuses.some((x) => x.id === 'slow') && alvo.statuses.some((x) => x.id === 'burning')) {
          alvo.statuses = alvo.statuses.filter((x) => x.id !== 'slow' && x.id !== 'burning');
          m.aviso(b, f, 'Choque térmico', alvo);
          m.dano(b, f, alvo, 180, false, 'Choque térmico');
        }
      },
    },
  },
  ra: {
    nome: 'Ciclo do sol',
    texto: '20 s: causa 15% a mais e o trio cura 0,5% por segundo. Depois 10 s: causa 15% a menos e fica Protegido 20%.',
    ganchos: {
      passo(m, b, f, dt) {
        const dia = b.time % 30 < 20, s = u(f);
        if (dia) for (const a of m.aliados(b, f)) m.cura(b, f, a, a.maxHp * 0.005 * dt, 'Sol');
        if ((s.dia ?? 1) !== (dia ? 1 : 0)) {
          s.dia = dia ? 1 : 0;
          if (!dia) m.efeitos(b, f, [f], [st('protected', 0.2, 10)]);
          m.aviso(b, f, dia ? 'Amanhece' : 'Anoitece', f);
        }
      },
      causa: (_m, b) => (b.time % 30 < 20 ? 1.15 : 0.85),
    },
  },

  /* ───────── Mentes e apoio ───────── */
  katara: {
    nome: 'Dobra de sangue',
    texto: 'Aos 40 s (uma vez), por 4 s, o rival mais forte ataca os próprios aliados.',
    ganchos: {
      passo(m, b, f) {
        if (u(f).lua || b.time < 40) return;
        const alvo = maisForte(m, b, f);
        if (!alvo || m.aliados(b, alvo).length < 2) return;
        u(f).lua = 1;
        alvo.traido = 4;
        m.aviso(b, f, 'Dobra de sangue', alvo);
      },
    },
  },
  leorio: {
    nome: 'Futuro médico',
    texto: 'As curas dele valem o dobro em quem está abaixo de 35% da Vida.',
    ganchos: { curaFeita: (_m, _b, _f, alvo) => (fracao(alvo) < 0.35 ? 2 : 1) },
  },
  aerith: {
    nome: 'Última oração',
    texto: 'Se ela cair, os aliados curam 30% da Vida e ganham Regeneração por 8 s.',
    ganchos: {
      morreu(m, b, f) {
        m.aviso(b, f, 'Última oração', f);
        const vivos = m.aliados(b, f);
        for (const a of vivos) m.cura(b, f, a, a.maxHp * 0.3, 'Última oração');
        m.efeitos(b, f, vivos, [st('regen', 12, 8)]);
      },
    },
  },
  isis: {
    nome: 'Asas protetoras',
    texto: 'Enquanto ela está de pé, aliados abaixo de 30% da Vida recebem 40% a menos.',
    ganchos: {
      recebeAliado: (_m, _b, f, aliado) => (aliado !== f && fracao(aliado) < 0.3 ? 0.6 : 1),
    },
  },
  tenshinhan: {
    nome: 'Kikōhō',
    texto: 'A habilidade mais forte custa 15% da Vida dele, mas causa 80% a mais.',
    ganchos: {
      causa: (_m, _b, f, _alvo, g) => (g.habilidade && u(f).kikoho ? 1.8 : 1),
      antes(m, b, f, i) {
        if (i !== 2) return;
        u(f).kikoho = 1;
        if (f.hp > f.maxHp * 0.16) { f.hp -= f.maxHp * 0.15; m.aviso(b, f, 'Kikōhō: custa Vida', f); }
      },
      usou(_m, _b, f) { u(f).kikoho = 0; },
    },
  },
  sailormercury: {
    nome: 'Computador de Mercúrio',
    texto: 'Enquanto ela está de pé, o trio causa 15% a mais no rival mais forte.',
    ganchos: {
      inicio(m, b, f) {
        const alvo = maisForte(m, b, f);
        if (alvo) { u(f).analisado = b.fighters.indexOf(alvo); m.aviso(b, f, 'Analisado', alvo); }
      },
      causaAliado: (_m, b, f, _aliado, alvo) => (u(f).analisado !== undefined && b.fighters[u(f).analisado!] === alvo ? 1.15 : 1),
    },
  },
  invencivel: {
    nome: 'Sangue viltrumita',
    texto: '+1% de dano para cada 2% de Vida perdida (até 30%).',
    ganchos: { causa: (_m, _b, f) => 1 + Math.min(0.3, (1 - fracao(f)) / 2) },
  },
  hellboy: {
    nome: 'Chifres serrados',
    texto: 'Abaixo de 30% da Vida: causa 40% a mais e não fica Paralisado, Congelado nem Dormindo.',
    ganchos: {
      causa: (_m, _b, f) => (fracao(f) < 0.3 ? 1.4 : 1),
      imune: (f, s) => fracao(f) < 0.3 && (s === 'paralyzed' || s === 'frozen' || s === 'sleep'),
    },
  },
  kaneki: {
    nome: 'Fome de ghoul',
    texto: 'Abaixo de 50% da Vida, cura 15% do dano que causa. Ao derrubar um rival, cura 20% da Vida.',
    ganchos: {
      bateu(m, b, f, _alvo, dano) { if (fracao(f) < 0.5) m.cura(b, f, f, dano * 0.15, 'Fome'); },
      caiu(m, b, f, quem, quemDerrubou) { if (quemDerrubou === f && quem.side !== f.side) { m.cura(b, f, f, f.maxHp * 0.2, 'Kagune'); m.aviso(b, f, 'Kakuja', f); } },
    },
  },
  venom: {
    nome: 'Simbionte',
    texto: 'Recupera 1% da Vida por segundo. Queimando causa o dobro nele.',
    ganchos: {
      passo(m, b, f, dt) { m.cura(b, f, f, f.maxHp * 0.01 * dt, 'Simbionte'); },
      recebe: (m, _b, f, _fonte, g) => (!g.direto && g.label === 'Impacto' && m.intensidade(f, 'burning') > 0 ? 2 : 1),
    },
  },
  stitch: {
    nome: 'Experimento 626',
    texto: 'Os golpes dele tiram Escudo, Barreira e Invocação do alvo.',
    ganchos: {
      bateu(m, b, f, alvo, _dano, g) {
        if (!g.direto || !vivo(alvo)) return;
        const tinha = alvo.shields.length > 0 || alvo.statuses.some((s) => s.id === 'barrier' || s.id === 'summon');
        if (!tinha) return;
        alvo.shields = [];
        alvo.statuses = alvo.statuses.filter((s) => s.id !== 'barrier' && s.id !== 'summon');
        m.aviso(b, f, 'Destruído!', alvo);
      },
    },
  },
  malenia: {
    nome: 'Podridão escarlate',
    texto: 'Cura 7% do dano que causa. Ao chegar a 50% da Vida (uma vez), todos os rivais ficam Envenenado (14 por s, 8 s).',
    ganchos: {
      bateu(m, b, f, _alvo, dano) { m.cura(b, f, f, dano * 0.07, 'Podridão'); },
      apanhou(m, b, f) {
        if (u(f).flor || fracao(f) > 0.5) return;
        u(f).flor = 1;
        m.efeitos(b, f, m.rivais(b, f), [st('poison', 14, 8)]);
        m.aviso(b, f, 'Florescer escarlate', f);
      },
    },
  },
  tifa: {
    nome: 'Combo crescente',
    texto: 'Cada golpe seguido no mesmo rival causa 6% a mais (até 60%). Trocar de alvo zera.',
    ganchos: {
      causa(_m, b, f, alvo, g) {
        if (!g.direto) return 1;
        const s = u(f), i = b.fighters.indexOf(alvo);
        s.combo = s.alvo === i ? Math.min(10, (s.combo ?? 0) + 1) : 0;
        s.alvo = i;
        return 1 + 0.06 * s.combo;
      },
    },
  },
  chunli: {
    nome: 'Cem chutes',
    texto: 'Ataca o dobro de vezes, com 45% em cada. A cada 12 golpes, 60 de dano em todos os rivais.',
    ganchos: {
      ritmo: () => 2,
      causa: (_m, _b, _f, _alvo, g) => (g.direto && !g.habilidade ? 0.45 : 1),
      bateu(m, b, f, _alvo, _dano, g) {
        if (!g.direto || g.habilidade) return;
        u(f).chutes = (u(f).chutes ?? 0) + 1;
        if (u(f).chutes! % 12 !== 0) return;
        m.aviso(b, f, 'Spinning Bird Kick', f);
        for (const r of m.rivais(b, f)) m.dano(b, f, r, 60, false, 'Spinning Bird Kick');
      },
    },
  },
  darthvader: {
    nome: 'Estrangulamento da Força',
    texto: 'A cada 14 s, por 3 s, o rival mais forte fica Paralisado e perde 35 por segundo; Vader não age nesse tempo.',
    ganchos: {
      passo(m, b, f, dt) {
        const s = u(f);
        if ((s.aperta ?? 0) > 0) {
          const alvo = b.fighters[s.vitima!];
          s.aperta! -= dt;
          if (alvo && vivo(alvo)) m.dano(b, f, alvo, 35 * dt, false, 'Estrangulamento');
          return;
        }
        if (!relogio(f, 'forca', dt, 14, 9)) return;
        const alvo = maisForte(m, b, f);
        if (!alvo) return;
        s.aperta = 3; s.vitima = b.fighters.indexOf(alvo);
        m.efeitos(b, f, [alvo], [st('paralyzed', 1, 3)]);
        m.aviso(b, f, 'Estrangulamento', alvo);
      },
      parado: (f) => (u(f).aperta ?? 0) > 0,
    },
  },
  garnet: {
    nome: 'Visão do futuro',
    texto: 'Quando um rival começa um Preparo de 2,5 s ou mais, o trio fica Protegido 40% até sair (a cada 20 s).',
    ganchos: {
      viuPreparo(m, b, f, quem, preparo) {
        if (preparo < 2.5 || (u(f).visao ?? 0) > b.time) return;
        u(f).visao = b.time + 20;
        m.efeitos(b, f, m.aliados(b, f), [st('protected', 0.4, preparo + 1)]);
        m.aviso(b, f, 'Visão do futuro', quem);
      },
    },
  },
  nami: {
    nome: 'Clima-Tact',
    texto: 'A cada 15 s alterna: trio Acelerado 15% por 4 s, rivais Lento 15% por 4 s, ou 70 de dano no rival mais forte.',
    ganchos: {
      passo(m, b, f, dt) {
        if (!relogio(f, 'clima', dt, 15, 10)) return;
        const s = u(f), fase = (s.clima ?? 0) % 3;
        s.clima = fase + 1;
        if (fase === 0) { m.efeitos(b, f, m.aliados(b, f), [st('haste', 0.15, 4)]); m.aviso(b, f, 'Sol', f); }
        else if (fase === 1) { m.efeitos(b, f, m.rivais(b, f), [st('slow', 0.15, 4)]); m.aviso(b, f, 'Chuva', f); }
        else { const alvo = maisForte(m, b, f); if (alvo) { m.aviso(b, f, 'Raio!', alvo); m.dano(b, f, alvo, 70, false, 'Raio'); } }
      },
    },
  },
  palpatine: {
    nome: 'Relâmpago em cadeia',
    texto: 'O dano das habilidades dele passa para os outros rivais com metade.',
    ganchos: {
      bateu(m, b, f, alvo, dano, g) {
        if (!g.habilidade || g.label === 'Relâmpago em cadeia') return;
        for (const r of m.rivais(b, f)) if (r !== alvo) m.dano(b, f, r, dano * 0.5, false, 'Relâmpago em cadeia');
      },
    },
  },
};

export const UNICAS: Record<string, Unica> = { ...LOTE1, ...LOTE2, ...LOTE3, ...LOTE4, ...LOTE5, ...LOTE6, ...LOTE7, ...LOTE8, ...LOTE9 };
// o Kirby copia a mecânica de quem ele inala: precisa conhecer todas
conheceTodas(UNICAS);
export const unicaDe = (id: string): Unica | undefined => UNICAS[id];
