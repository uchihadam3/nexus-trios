#!/usr/bin/env python3
"""
Música v7: as faixas das lutas secretas (src/engine/segredos.ts).

Pedido do jogador: "duas músicas novas, muito, muito boas… no estilo das que a gente tem, mas de fase realmente
secreta: a da luta entre a 5 e a 6, e a da luta 11 como se fosse o boss secreto, o mais forte do jogo".

O mesmo som das faixas de batalha (v4/v5/v6: bateria de rock, baixo sintetizado, guitarras, supersaw, metais, coro,
sinos, taikos), em três camadas (base, pulso, tema) e com o mesmo volume, para o jogo subir pulso e tema quando a luta
esquenta.

SEGREDO (luta ★) — si menor com cor dórica (mi maior) e frígia (dó maior), 160 BPM, 72 compassos (~1 min 48 s)
  Segredo      caixinha de música, tique-taque e coro sussurrado: uma porta escondida se abrindo
  Porta        galope, o tema misterioso no supersaw e nos metais
  Labirinto    riff frígio (si / dó), arpejos rápidos, metais e supersaw em pergunta e resposta
  Revelação    meio-tempo, sinos e coro: o segredo aparece
  Tesouro      hino heroico em ré maior, e o refrão meio tom acima (dó menor): o segredo é seu
  Volta        o riff frígio e a subida de volta à Porta
  (o laço volta para a Porta)

LENDA (luta 11) — sol menor com o dominante frígio (lá bemol e ré maior), 176 BPM, 80 compassos (~1 min 49 s)
  Despertar     sinos graves, batida de coração nos taikos, tímpanos e o coro crescendo: algo antigo acorda
  Lenda         galope, o tema do chefe secreto, mais alto e mais escuro que o da luta 10
  Fúria antiga  bumbo duplo, arpejos, metais 3+3+2 e o riff frígio
  Abismo        meio-tempo, coro inteiro e sinos: o peso da lenda
  Último fôlego hino, refrão na cadência andaluza e o refrão final meio tom acima, com coro e metais dobrados
  Renascer      o riff frígio volta e sobe para a Lenda
  (o laço volta para a Lenda)

Uso:  python3 tools/audio/generate_music_v7.py [segredo] [lenda]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v4 as v4  # noqa: E402
from generate_music_v3 import pan  # noqa: E402
from generate_music_v4 import baixo, guitarra, pad, power, riser, supersaw  # noqa: E402
from generate_music_v5 import Musica, coro, cordas, corrida, metais, sino_grande, taiko, timpano  # noqa: E402

GALOPE = ((0, 2), (2, 1), (3, 1))
RIFF = ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2))


# ================================================================== SEGREDO (luta ★)
ACORDES_SEGREDO = {
    "Bm": (47, [59, 62, 66]), "G": (43, [55, 59, 62]), "D": (38, [50, 54, 57]), "A": (45, [57, 61, 64]),
    "E": (40, [52, 56, 59]), "F#": (42, [54, 58, 61]), "Em": (40, [52, 55, 59]), "C": (36, [48, 52, 55]),
    # o refrão do Tesouro meio tom acima (dó menor)
    "Eb": (39, [51, 55, 58]), "Bb": (46, [58, 62, 65]), "Cm": (36, [48, 51, 55]), "Ab": (44, [56, 60, 63]),
}
PROG_SEGREDO = (["Bm", "Bm", "G", "G", "Em", "Em", "F#", "F#"]                         # Segredo 0–7
                + ["Bm", "G", "D", "A", "Bm", "G", "E", "F#"] * 2                       # Porta 8–23
                + ["Bm", "C", "Bm", "C", "G", "A", "F#", "F#"] * 2                      # Labirinto 24–39
                + ["G", "D", "Em", "Bm", "G", "D", "E", "F#"]                           # Revelação 40–47
                + ["D", "A", "Bm", "G", "D", "A", "G", "F#"]                            # Tesouro: hino 48–55
                + ["Eb", "Bb", "Cm", "Ab", "Eb", "Bb", "Ab", "G"]                       # refrão meio tom acima 56–63
                + ["Bm", "C", "Bm", "C", "Bm", "C", "F#", "F#"])                        # Volta 64–71
SECOES_SEGREDO = [("Segredo", 0), ("Porta", 8), ("Labirinto", 24), ("Revelação", 40), ("Tesouro", 48), ("Volta", 64)]

# o tema da Porta: começa no si, sobe ao fá sustenido e passa pelo sol sustenido (a cor dórica) — misterioso
TEMA_SEGREDO = [(0, 1, 71), (1, .5, 74), (1.5, .5, 73), (2, 2, 78),
                (4, 1.5, 79), (5.5, .5, 78), (6, 1, 74), (7, 1, 71),
                (8, 2, 74), (10, 1, 76), (11, 1, 78),
                (12, 3, 76), (15, 1, 73),
                (16, 1, 71), (17, 1, 74), (18, 2, 78),
                (20, 1.5, 83), (21.5, .5, 81), (22, 1, 79), (23, 1, 78),
                (24, 2, 80), (26, 1, 78), (27, 1, 76),
                (28, 3, 82), (31, 1, 78),
                (32, 1.5, 83), (33.5, .5, 81), (34, 2, 78),
                (36, 1.5, 79), (37.5, .5, 78), (38, 2, 74),
                (40, 1, 78), (41, 1, 81), (42, 1, 86), (43, 1, 81),
                (44, 3, 85), (47, 1, 81),
                (48, 1, 83), (49, 1, 86), (50, 2, 90),
                (52, 1, 88), (53, 1, 86), (54, 2, 83),
                (56, 2, 80), (58, 1, 83), (59, 1, 88),
                (60, 4, 85)]
REVELACAO = [(0, 3, 83), (3, 1, 79), (4, 3, 78), (7, 1, 81), (8, 2, 79), (10, 2, 78), (12, 4, 74),
             (16, 3, 79), (19, 1, 83), (20, 3, 81), (23, 1, 78), (24, 2, 80), (26, 2, 83), (28, 4, 82)]
# o hino do Tesouro (ré maior); o refrão é o mesmo hino meio tom acima, sobre os acordes do refrão
HINO_SEGREDO = [(0, 2, 78), (2, 1, 74), (3, 1, 78),
                (4, 2, 81), (6, 1, 76), (7, 1, 81),
                (8, 3, 83), (11, .5, 81), (11.5, .5, 78),
                (12, 1, 79), (13, 3, 86),
                (16, 2, 86), (18, 1, 85), (19, 1, 81),
                (20, 2, 85), (22, 1, 81), (23, 1, 88),
                (24, 3, 86), (27, 1, 83),
                (28, 2, 85), (30, 2, 82)]
# o motivo da Volta (si e dó, frígio)
MOTIVO_VOLTA = [(0, 1, 71), (1, 1, 72), (2, 2, 71), (4, 1, 74), (5, 1, 72), (6, 2, 71),
                (8, 1, 71), (9, 1, 72), (10, 2, 74), (12, 1, 78), (13, 1, 76), (14, 2, 72)]


def caixinha(nota, forte=0.7):
    """Caixinha de música: o sino agudo, curto e de lado."""
    return v4.sino(nota, forte)


def segredo():
    m = Musica("segredo", 160, PROG_SEGREDO, ACORDES_SEGREDO, SECOES_SEGREDO, laco=8, semente=160072)
    assert m.compassos == 72
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        refrao = sec == "Tesouro" and local >= 8

        # ------------------------------------------------ caixinha de música e tique-taque (o Segredo)
        if sec == "Segredo":
            arp = [notas[0] + 24, notas[1] + 24, notas[2] + 24, notas[1] + 36, notas[2] + 24, notas[1] + 24]
            for k in range(8):
                m.poe(m.tema_eco, pan(caixinha(arp[k % 6], 0.55 + 0.04 * local), 0.35 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
            for k in range(4):                                                    # tique-taque do relógio
                m.poe(m.pulso, m.CHIMBAL, t0 + k * BEAT, 0.5 + 0.06 * local)
                m.poe(m.pulso, m.CHIMBAL_ABERTO if local >= 6 else m.CHIMBAL, t0 + k * BEAT + BEAT / 2, 0.25 + 0.05 * local)
            m.poe(m.base_sala, pad(notas, BAR, 0.5 + 0.06 * local, 1100 + 230 * local), t0)
            if local >= 2:
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.4 + 0.07 * local), t0)
            if local in (0, 4):
                m.poe(m.base_sala, pan(sino_grande(47, 0.8), -0.2), t0)
                m.poe(m.base, timpano(35, 0.9), t0)
            if local >= 4:
                for k in range(4 if local < 6 else 8):
                    m.poe(m.base, taiko(0.4 + 0.08 * (local - 4) + 0.25 * (k % 4 == 0)), t0 + k * (BAR / (4 if local < 6 else 8)))
            if local == 5:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.4, 1.05), t0 + BEAT * 2)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.2), t0)
                m.poe(m.pulso, guitarra(pc, BAR * 1.9, 0.85), t0)

        # ------------------------------------------------ cordas correndo (base)
        if sec in ("Porta", "Labirinto") or refrao or sec == "Volta":
            seq = [notas[0] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12, notas[1] + 24]
            for k in range(16):
                m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, 0.8 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad e coro
        if sec == "Revelação":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 2100), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.95), t0)
        elif sec == "Tesouro":
            m.poe(m.base_sala, pad(notas, BAR, 0.55, 3400), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.9 if local < 8 else 1.05), t0)
        elif sec != "Segredo":
            m.poe(m.base_sala, pad(notas, BAR, 0.45, 2700), t0)
            if sec == "Porta":
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.4), t0)

        # ------------------------------------------------ baixo
        if sec == "Porta" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)
        elif sec == "Labirinto":
            for k in range(16):
                m.poe(m.base, baixo(raiz + (12 if k in (6, 14) else 0), S16 * 0.8, 1.05 if k in (0, 3, 6, 10, 13) else 0.82), t0 + k * S16)
        elif sec == "Revelação":
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.9), t0 + p * S16)
        elif sec == "Tesouro":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
        elif sec == "Volta":
            if local < 6:
                for pos, d in RIFF:
                    m.poe(m.base, baixo(raiz, S16 * d * 0.9, 1.05), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.base, baixo(raiz, passo * 0.8, 0.85 + 0.1 * (local - 6)), t0 + k * passo)

        # ------------------------------------------------ guitarras (pulso)
        if sec == "Porta" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif sec == "Labirinto":
            for k in range(16):                                                   # acentos 3+3+3+3+2+2: o labirinto
                aberto = k in (0, 3, 6, 9, 12, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 1.0 if aberto else 0.76, abafada=not aberto), t0 + k * S16)
        elif sec == "Revelação" and local >= 6:
            m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.6 + 0.3 * (local - 6)), t0)
        elif sec == "Tesouro":
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.0), t0 + pos * S16)
        elif sec == "Volta":
            if local < 6:
                for pos, d in RIFF:
                    m.poe(m.pulso, guitarra(pc, d * S16 * 0.85, 1.05, abafada=d < 2), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.pulso, guitarra(pc, passo * 0.5, 0.75 + 0.15 * (local - 6), abafada=True), t0 + k * passo)

        # ------------------------------------------------ bateria
        if sec == "Porta":
            m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.1)
            if local in (7, 15):
                m.virada_de_tons(t0, [59, 57, 54, 52, 50, 47, 45, 42])
        elif sec == "Labirinto":
            m.bat([0, 3, 6, 9, 12, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12] if local < 8 else [4, 10, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(16):
                m.poe(m.pulso, m.CHIMBAL_F if k % 2 == 0 else m.CHIMBAL, t0 + k * S16, 0.9 if k % 4 == 0 else 0.6)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.0)
            if local == 15:
                m.virada_de_tons(t0, [59, 57, 55, 54, 52, 50, 47, 45])
        elif sec == "Revelação":
            m.bat([0, 10], m.BUMBO, m.base, t0)
            m.bat([8], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 0.8)
                m.poe(m.pulso, m.PRATO, t0, 0.7)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        elif sec == "Tesouro":
            if local < 8:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            else:
                m.bat(range(16), m.BUMBO, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO if local >= 8 else m.CHIMBAL_ABERTO, t0 + k * S16)
            if local % (2 if local >= 8 else 4) == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.2)
                m.poe(m.base, timpano(raiz, 1.0), t0)
            if local == 7:                                                        # a subida para dó menor
                m.poe(m.base, riser(BAR, 1.3), t0)
                m.virada_de_tons(t0, [59, 57, 55, 52, 50, 47, 45, 44])
        elif sec == "Volta":
            if local < 6:
                m.bat([0, 3, 4, 6, 8, 11, 12, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
                if local in (0, 4):
                    m.poe(m.pulso, m.PRATO, t0)
                    m.poe(m.base, m.IMPACTO, t0, 0.9)
            else:
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                if local == 6:
                    m.poe(m.base, m.rufo(2, 0.2), t0)
            if local == 4:
                m.poe(m.base, riser(BAR * 4, 1.3), t0)

        # ------------------------------------------------ tema
        if sec == "Porta" and local == 0:
            m.frase(m.tema_eco, TEMA_SEGREDO, t0, forte=1.05, brilho=5600, voz="ambos")
        if sec == "Porta" and local % 2 == 1:                                     # a caixinha de música lembra o segredo
            m.poe(m.tema_eco, pan(caixinha(notas[2] + 24, 0.35), 0.4), t0 + BEAT * 3.5)
        if sec == "Labirinto":
            if local < 8:
                for k, nota in enumerate(corrida(notas)):
                    m.poe(m.tema_eco, supersaw(nota, S16 * 0.9, 0.6 + 0.18 * (k % 4 == 0), 6000, False), t0 + k * S16)
            else:
                for pos, d in ((0, 2), (3, 2), (6, 2)):
                    m.poe(m.tema, metais([n + 12 for n in notas], S16 * d * 0.9, 1.15), t0 + pos * S16)
                topo = sorted(n + 24 for n in notas)
                for pos, d, nota in ((8, 2, topo[2]), (10, 2, topo[1]), (12, 4, topo[0] + (12 if topo[0] < 72 else 0))):
                    m.poe(m.tema_eco, supersaw(nota, S16 * d * 0.92, 0.95, 5600), t0 + pos * S16)
        if sec == "Revelação":
            if local == 0:
                m.frase(m.tema_eco, REVELACAO, t0, forte=0.85, brilho=3400)
            seq = [notas[0] + 24, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k, nota in enumerate(seq):
                m.poe(m.tema_eco, pan(v4.sino(nota, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
            if local in (0, 4):
                m.poe(m.base_sala, pan(sino_grande(notas[0] + 12, 0.6), 0.15), t0)
        if sec == "Tesouro":
            if local == 0:
                m.frase(m.tema_eco, HINO_SEGREDO, t0, forte=1.1, brilho=6000, dobra=-12)
                m.frase(m.tema, HINO_SEGREDO, t0, transp=-12, forte=0.55, voz="metal")
            if local == 8:
                m.frase(m.tema_eco, HINO_SEGREDO, t0, transp=1, forte=1.15, brilho=6200, dobra=12, ganho_dobra=0.4)
                m.frase(m.tema, HINO_SEGREDO, t0, transp=-11, forte=0.65, voz="metal")
                for k in range(8):                                                # a caixinha volta, brilhando por cima
                    m.poe(m.tema_eco, pan(caixinha(HINO_SEGREDO[k * 2][2] + 13, 0.3), 0.45 * (1 if k % 2 else -1)), t0 + k * BAR)
        if sec == "Volta":
            if local < 6 and local % 2 == 0:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.2), t0)
                m.poe(m.tema, metais([n + 12 for n in m.acorde(b + 1)[1]], BEAT * 0.9, 1.2), t0 + BEAT * 1.5)
            if local == 2:
                m.frase(m.tema_eco, MOTIVO_VOLTA, t0, forte=0.95)
            if local >= 6:
                m.poe(m.tema_eco, supersaw(78 + 2 * (local - 6), BAR * 0.95, 0.6 + 0.15 * (local - 6), 2600 + 1500 * (local - 6), False), t0)

    m.renderiza("anime arcade · luta secreta ★ (v7)")


# ================================================================== LENDA (luta 11)
ACORDES_LENDA = {
    "Gm": (43, [55, 58, 62]), "Ab": (44, [56, 60, 63]), "Eb": (39, [51, 55, 58]), "D": (38, [50, 54, 57]),
    "Cm": (36, [48, 51, 55]), "Bb": (34, [46, 50, 53]), "F": (41, [53, 57, 60]),
    # o refrão final meio tom acima (lá bemol menor)
    "Abm": (44, [56, 59, 63]), "Gb": (42, [54, 58, 61]), "E": (40, [52, 56, 59]),
}
PROG_LENDA = (["Gm", "Gm", "Ab", "Ab", "Gm", "Gm", "D", "D"]                            # Despertar 0–7
              + ["Gm", "Eb", "Cm", "D", "Gm", "Eb", "Ab", "D"] * 2                      # Lenda 8–23
              + ["Gm", "Ab", "Gm", "Ab", "Cm", "Ab", "D", "D"] * 2                      # Fúria antiga 24–39
              + ["Eb", "Bb", "Cm", "Gm", "Eb", "Bb", "Ab", "D"]                         # Abismo 40–47
              + ["Eb", "F", "Gm", "Gm", "Eb", "F", "D", "D"]                            # Último fôlego: hino 48–55
              + ["Gm", "F", "Eb", "D"] * 2                                              # refrão (andaluza) 56–63
              + ["Abm", "Gb", "E", "Eb"] * 2                                            # refrão meio tom acima 64–71
              + ["Gm", "Ab", "Gm", "Ab", "Gm", "Ab", "D", "D"])                         # Renascer 72–79
SECOES_LENDA = [("Despertar", 0), ("Lenda", 8), ("Fúria antiga", 24), ("Abismo", 40), ("Último fôlego", 48), ("Renascer", 72)]

# o tema do chefe secreto (sol menor harmônica): mais alto e mais escuro que o da luta 10
TEMA_LENDA = [(0, 1, 79), (1, .5, 82), (1.5, .5, 81), (2, 2, 86),
              (4, 1.5, 87), (5.5, .5, 86), (6, 1, 82), (7, 1, 79),
              (8, 2, 84), (10, 1, 82), (11, 1, 79),
              (12, 3, 78), (15, 1, 81),
              (16, 1, 79), (17, 1, 82), (18, 2, 86),
              (20, 1.5, 91), (21.5, .5, 89), (22, 1, 87), (23, 1, 86),
              (24, 2, 84), (26, 1, 80), (27, 1, 84),
              (28, 3, 81), (31, 1, 78),
              (32, 1.5, 86), (33.5, .5, 84), (34, 2, 82),
              (36, 1.5, 87), (37.5, .5, 86), (38, 2, 82),
              (40, 1, 84), (41, 1, 87), (42, 1, 91), (43, 1, 87),
              (44, 3, 90), (47, 1, 86),
              (48, 1, 86), (49, 1, 91), (50, 2, 91),
              (52, 1, 89), (53, 1, 87), (54, 2, 86),
              (56, 2, 84), (58, 1, 87), (59, 1, 92),
              (60, 4, 90)]
ABISMO = [(0, 3, 82), (3, 1, 79), (4, 3, 77), (7, 1, 82), (8, 2, 84), (10, 2, 82), (12, 4, 79),
          (16, 3, 82), (19, 1, 86), (20, 3, 86), (23, 1, 84), (24, 2, 84), (26, 2, 87), (28, 4, 90)]
HINO_LENDA = [(0, 2, 79), (2, 1, 82), (3, 1, 87),
              (4, 2, 89), (6, 1, 84), (7, 1, 81),
              (8, 3, 86), (11, .5, 84), (11.5, .5, 82),
              (12, 1, 86), (13, 3, 91),
              (16, 2, 91), (18, 1, 87), (19, 1, 82),
              (20, 2, 89), (22, 1, 86), (23, 1, 84),
              (24, 3, 90), (27, 1, 86),
              (28, 2, 90), (30, 2, 93)]
# o refrão sobre a cadência andaluza (sol, fá, mi bemol, ré); no fim, meio tom acima
REFRAO_LENDA = [(0, 1, 79), (1, 1, 82), (2, 2, 86),
                (4, 2, 84), (6, 1, 81), (7, 1, 84),
                (8, 3, 82), (11, 1, 79),
                (12, 2, 78), (14, 1, 81), (15, 1, 86),
                (16, 1, 91), (17, 1, 89), (18, 2, 86),
                (20, 1, 89), (21, 1, 86), (22, 2, 84),
                (24, 2, 82), (26, 1, 86), (27, 1, 87),
                (28, 3, 90), (31, 1, 86)]
MOTIVO_RENASCER = [(0, 1, 79), (1, 1, 80), (2, 2, 79), (4, 1, 82), (5, 1, 80), (6, 2, 79),
                   (8, 1, 79), (9, 1, 80), (10, 2, 82), (12, 1, 86), (13, 1, 84), (14, 2, 80)]


def lenda():
    m = Musica("lenda", 176, PROG_LENDA, ACORDES_LENDA, SECOES_LENDA, laco=8, semente=176080)
    assert m.compassos == 80
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        refrao = sec == "Último fôlego" and local >= 8

        # ------------------------------------------------ o Despertar: sinos graves, coração, tímpanos, coro crescendo
        if sec == "Despertar":
            m.poe(m.base_sala, pad(notas, BAR, 0.6 + 0.05 * local, 900 + 260 * local), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + ([notas[0]] if local >= 4 else []), BAR, 0.5 + 0.08 * local), t0)
            m.poe(m.base_sala, pan(sino_grande(43 if raiz != 44 else 44, 1.0), -0.15), t0)
            m.poe(m.base_sala, pan(sino_grande(55 if raiz != 44 else 56, 0.55), 0.2), t0 + BEAT * 2)
            for k in range(4):                                                    # batida de coração: tum-tum
                m.poe(m.base, taiko(0.55 + 0.06 * local), t0 + k * BEAT)
                m.poe(m.base, taiko(0.32 + 0.05 * local), t0 + k * BEAT + S16 * 1.5)
            if local in (0, 2, 4):
                m.poe(m.base, m.IMPACTO, t0, 1.05)
                m.poe(m.base, timpano(31, 1.25), t0)
            if local in (3, 5):
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.6, 1.25), t0)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.05), t0 + BEAT * 2.5)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.2, 1.15), t0 + BEAT * 3)
            if local >= 6:
                for k in range(16):
                    m.poe(m.base, pan(cordas(notas[0] + (12 if k % 2 == 0 else 24), S16 * 0.8, 0.6 + 0.2 * (local - 6)), 0.25 * (1 if k % 2 else -1)), t0 + k * S16)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
                m.poe(m.pulso, guitarra(pc, BAR * 1.9, 0.95), t0)

        # ------------------------------------------------ cordas correndo (base)
        if sec in ("Lenda", "Fúria antiga") or refrao or sec == "Renascer":
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12]
            for k in range(16):
                m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, 0.88 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad e coro (o coro inteiro no Abismo e no Último fôlego)
        if sec == "Abismo":
            m.poe(m.base_sala, pad(notas, BAR, 0.95, 1900), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0]], BAR, 1.0), t0)
        elif sec == "Último fôlego":
            m.poe(m.base_sala, pad(notas, BAR, 0.6, 3300), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.95 if local < 8 else 1.1), t0)
            if local >= 16:
                m.poe(m.tema, coro([notas[0]], BAR, 0.6), t0)                      # os baixos do coro no fim
        elif sec != "Despertar":
            m.poe(m.base_sala, pad(notas, BAR, 0.5, 2600), t0)
            if sec == "Lenda":
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.55), t0)

        # ------------------------------------------------ baixo
        if sec == "Lenda" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.05), t0 + (beat * 4 + p) * S16)
        elif sec == "Fúria antiga":
            for k in range(16):
                m.poe(m.base, baixo(raiz, S16 * 0.8, 1.08 if k % 4 == 0 else 0.88), t0 + k * S16)
        elif sec == "Abismo":
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.95), t0 + p * S16)
        elif sec == "Último fôlego":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.05 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
        elif sec == "Renascer":
            if local < 6:
                for pos, d in RIFF:
                    m.poe(m.base, baixo(raiz, S16 * d * 0.9, 1.08), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.base, baixo(raiz, passo * 0.8, 0.88 + 0.1 * (local - 6)), t0 + k * passo)

        # ------------------------------------------------ guitarras (pulso)
        if sec == "Lenda" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.05 if aberto else 0.88, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif sec == "Fúria antiga":
            for k in range(16):                                                   # palheta alternada, acento 3+3+2
                aberto = k in (0, 3, 6, 8, 11, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 1.05 if aberto else 0.8, abafada=not aberto), t0 + k * S16)
        elif sec == "Abismo" and local >= 6:
            m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.65 + 0.3 * (local - 6)), t0)
        elif sec == "Último fôlego":
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.05), t0 + pos * S16)
        elif sec == "Renascer":
            if local < 6:
                for pos, d in RIFF:
                    m.poe(m.pulso, guitarra(pc, d * S16 * 0.85, 1.08, abafada=d < 2), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.pulso, guitarra(pc, passo * 0.5, 0.78 + 0.15 * (local - 6), abafada=True), t0 + k * passo)
                if local == 7:
                    m.poe(m.pulso, guitarra(pc, BAR * 0.45, 1.05), t0 + BAR * 0.5)

        # ------------------------------------------------ bateria
        if sec == "Lenda":
            m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.2)
                m.poe(m.base, timpano(31, 1.1), t0)
            if local in (7, 15):
                m.virada_de_tons(t0, [55, 52, 50, 48, 45, 43, 41, 38])
        elif sec == "Fúria antiga":
            m.bat(range(16), m.BUMBO_F if local >= 8 else m.BUMBO, m.base, t0)  # bumbo duplo a fúria inteira
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            if local < 8:
                m.bat([2, 6, 10, 14], m.CAIXA, m.base, t0, 0.5)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 2 == 0:
                m.poe(m.pulso, m.PRATO, t0, 0.85)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.1)
                m.poe(m.base, timpano(raiz, 1.0), t0)
            if local == 15:
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 41])
        elif sec == "Abismo":
            m.bat([0, 10], m.BUMBO_F, m.base, t0)
            m.bat([8], m.CAIXA_F, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local in (0, 4):
                m.poe(m.base, m.IMPACTO, t0, 0.9)
                m.poe(m.pulso, m.PRATO, t0, 0.75)
                m.poe(m.base_sala, pan(sino_grande(notas[0], 0.85), -0.2), t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.35), t0)
        elif sec == "Último fôlego":
            if local < 8:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            else:
                m.bat(range(16), m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO if local >= 8 else m.CHIMBAL_ABERTO, t0 + k * S16)
            if local % (2 if local >= 8 else 4) == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8, 16):
                m.poe(m.base, m.IMPACTO, t0, 1.25)
                m.poe(m.base, timpano(raiz, 1.1), t0)
                m.poe(m.base_sala, pan(sino_grande(raiz + 12, 0.7), 0.15), t0)
            if local in (7, 15):                                                  # as subidas
                m.poe(m.base, riser(BAR, 1.35), t0)
                m.virada_de_tons(t0, [57, 55, 52, 50, 48, 45, 43, 42 if local == 7 else 44])
        elif sec == "Renascer":
            if local < 6:
                m.bat([0, 3, 4, 6, 8, 11, 12, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
                if local in (0, 4):
                    m.poe(m.pulso, m.PRATO, t0)
                    m.poe(m.base, m.IMPACTO, t0, 1.0)
            else:
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                if local == 6:
                    m.poe(m.base, m.rufo(2, 0.2), t0)
            if local == 4:
                m.poe(m.base, riser(BAR * 4, 1.35), t0)

        # ------------------------------------------------ tema
        if sec == "Lenda" and local == 0:
            m.frase(m.tema_eco, TEMA_LENDA, t0, forte=1.08, brilho=5800, voz="ambos")
            m.frase(m.tema, TEMA_LENDA, t0, transp=-24, forte=0.4, voz="metal")       # os metais graves dobram o tema
        if sec == "Fúria antiga":
            if local < 8:
                for k, nota in enumerate(corrida(notas)):
                    m.poe(m.tema_eco, supersaw(nota, S16 * 0.9, 0.64 + 0.18 * (k % 4 == 0), 6200, False), t0 + k * S16)
            else:
                for pos, d in ((0, 2), (3, 2), (6, 2)):
                    m.poe(m.tema, metais([n + 12 for n in notas], S16 * d * 0.9, 1.2), t0 + pos * S16)
                topo = sorted(n + 24 for n in notas)
                for pos, d, nota in ((8, 2, topo[2]), (10, 2, topo[1]), (12, 4, topo[0] + (12 if topo[0] < 72 else 0))):
                    m.poe(m.tema_eco, supersaw(nota, S16 * d * 0.92, 1.0, 5800), t0 + pos * S16)
        if sec == "Abismo":
            if local == 0:
                m.frase(m.tema_eco, ABISMO, t0, forte=0.9, brilho=3200)
                m.frase(m.tema, ABISMO, t0, transp=-12, forte=0.35, voz="metal")
            seq = [notas[0] + 24, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k, nota in enumerate(seq):
                m.poe(m.tema_eco, pan(v4.sino(nota, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
        if sec == "Último fôlego":
            if local == 0:
                m.frase(m.tema_eco, HINO_LENDA, t0, forte=1.12, brilho=6000, dobra=-12)
                m.frase(m.tema, HINO_LENDA, t0, transp=-12, forte=0.6, voz="metal")
            if local == 8:
                m.frase(m.tema_eco, REFRAO_LENDA, t0, forte=1.15, brilho=6200, dobra=12, ganho_dobra=0.38)
                m.frase(m.tema, REFRAO_LENDA, t0, transp=-12, forte=0.65, voz="metal")
            if local == 16:                                                       # o refrão meio tom acima, tudo dobrado
                m.frase(m.tema_eco, REFRAO_LENDA, t0, transp=1, forte=1.22, brilho=6500, dobra=12, ganho_dobra=0.45)
                m.frase(m.tema, REFRAO_LENDA, t0, transp=-11, forte=0.75, voz="metal")
                m.frase(m.tema_eco, REFRAO_LENDA, t0, transp=-4, forte=0.35, brilho=4000)
        if sec == "Renascer":
            if local < 6 and local % 2 == 0:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.25), t0)
                m.poe(m.tema, metais([n + 12 for n in m.acorde(b + 1)[1]], BEAT * 0.9, 1.25), t0 + BEAT * 1.5)
            if local == 2:
                m.frase(m.tema_eco, MOTIVO_RENASCER, t0, forte=1.0)
            if local >= 6:
                m.poe(m.tema_eco, supersaw(79 + 2 * (local - 6), BAR * 0.95, 0.62 + 0.15 * (local - 6), 2600 + 1500 * (local - 6), False), t0)

    m.renderiza("anime arcade · luta 11, o chefe secreto (v7)")


if __name__ == "__main__":
    qual = sys.argv[1:] or ["segredo", "lenda"]
    if "segredo" in qual:
        segredo()
    if "lenda" in qual:
        lenda()
