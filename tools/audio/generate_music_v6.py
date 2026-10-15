#!/usr/bin/env python3
"""
Música v6: a faixa do PvP ("Arena").

Pedido do jogador: o PvP com "uma música nova de PvP". Mesmo som das faixas de batalha (v4/v5: bateria de rock,
baixo sintetizado, guitarras, supersaw, metais, coro, taikos), com cara de duelo de arena: dois jogadores frente a
frente, a torcida batendo palmas e o tema que sobe de tom no golpe final.

ARENA — fá sustenido menor (com o dó sustenido maior da harmônica), 174 BPM, 72 compassos (~1 min 39 s)
  Entrada      taikos e palmas da torcida, coro, metais chamando: os dois entram na arena
  Duelo        galope, o tema da arena no supersaw e nos metais
  Choque       semicolcheias, arpejos rápidos, metais e guitarra em pergunta e resposta
  Estratégia   meio-tempo, sinos e coro: cada um pensa no próximo time
  Golpe final  hino, e o refrão um tom acima (sol sustenido menor, cadência andaluza)
  Retorno      riff frígio (fá sustenido / sol) e a subida de volta ao Duelo
  (o laço volta para o Duelo)

Sai nas mesmas três camadas (base, pulso, tema), em OGG e MP3, com o mesmo volume das outras: o jogo sobe pulso e
tema quando a luta esquenta.

Uso:  python3 tools/audio/generate_music_v6.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v4 as v4  # noqa: E402
from generate_music_v3 import pan  # noqa: E402
from generate_music_v4 import baixo, caixa, guitarra, pad, power, riser, supersaw  # noqa: E402
from generate_music_v5 import Musica, coro, cordas, corrida, metais, sino_grande, taiko, timpano  # noqa: E402

ACORDES = {
    "F#m": (42, [54, 57, 61]), "D": (38, [50, 54, 57]), "A": (45, [57, 61, 64]), "C#": (37, [49, 53, 56]),
    "Bm": (35, [47, 50, 54]), "E": (40, [52, 56, 59]), "G": (43, [55, 59, 62]),
    # o refrão um tom acima (sol sustenido menor)
    "G#m": (44, [56, 59, 63]), "F#": (42, [54, 58, 61]), "D#": (39, [51, 55, 58]),
}
PROG = (["F#m"] * 4 + ["D", "D", "C#", "C#"]                                             # Entrada 0–7
        + ["F#m", "D", "A", "C#"] * 2 + ["Bm", "F#m", "D", "C#"] * 2                     # Duelo 8–23
        + ["F#m", "E", "D", "C#"] * 2 + ["Bm", "D", "E", "C#", "Bm", "D", "C#", "C#"]    # Choque 24–39
        + ["D", "Bm", "F#m", "C#", "D", "Bm", "E", "C#"]                                 # Estratégia 40–47
        + ["D", "E", "F#m", "F#m", "D", "E", "C#", "C#"]                                 # Golpe final: hino 48–55
        + ["G#m", "F#", "E", "D#"] * 2                                                   # refrão um tom acima 56–63
        + ["F#m", "G", "F#m", "G", "F#m", "G", "C#", "C#"])                              # Retorno 64–71
SECOES = [("Entrada", 0), ("Duelo", 8), ("Choque", 24), ("Estratégia", 40), ("Golpe final", 48), ("Retorno", 64)]

TEMA = [(0, 1, 78), (1, .5, 80), (1.5, .5, 81), (2, 2, 85),
        (4, 1.5, 86), (5.5, .5, 85), (6, 1, 81), (7, 1, 78),
        (8, 2, 81), (10, 1, 80), (11, 1, 81),
        (12, 3, 80), (15, 1, 77),
        (16, 1, 78), (17, 1, 81), (18, 2, 85),
        (20, 1.5, 90), (21.5, .5, 88), (22, 1, 86), (23, 1, 85),
        (24, 2, 88), (26, 1, 85), (27, 1, 81),
        (28, 3, 85), (31, 1, 89),
        (32, 1.5, 86), (33.5, .5, 85), (34, 2, 83),
        (36, 1, 81), (37, 1, 85), (38, 2, 90),
        (40, 1.5, 88), (41.5, .5, 86), (42, 1, 85), (43, 1, 81),
        (44, 3, 80), (47, 1, 77),
        (48, 1, 78), (49, 1, 83), (50, 2, 86),
        (52, 1, 85), (53, 1, 81), (54, 2, 78),
        (56, 2, 81), (58, 1, 85), (59, 1, 86),
        (60, 4, 85)]
LAMENTO = [(0, 3, 81), (3, 1, 78), (4, 3, 78), (7, 1, 81), (8, 2, 85), (10, 2, 83), (12, 4, 80),
           (16, 3, 81), (19, 1, 85), (20, 3, 86), (23, 1, 85), (24, 2, 83), (26, 2, 86), (28, 4, 89)]
HINO = [(0, 2, 81), (2, 1, 78), (3, 1, 81),
        (4, 2, 83), (6, 1, 80), (7, 1, 83),
        (8, 3, 85), (11, .5, 83), (11.5, .5, 81),
        (12, 1, 85), (13, 3, 90),
        (16, 2, 90), (18, 1, 88), (19, 1, 85),
        (20, 2, 88), (22, 1, 83), (23, 1, 88),
        (24, 3, 89), (27, 1, 85),
        (28, 2, 89), (30, 2, 92)]
REFRAO = [(0, 1, 80), (1, 1, 83), (2, 2, 87),
          (4, 2, 85), (6, 1, 82), (7, 1, 85),
          (8, 3, 83), (11, 1, 80),
          (12, 2, 79), (14, 1, 82), (15, 1, 87),
          (16, 1, 92), (17, 1, 90), (18, 2, 87),
          (20, 1, 90), (21, 1, 87), (22, 2, 85),
          (24, 2, 83), (26, 1, 87), (27, 1, 88),
          (28, 3, 91), (31, 1, 87)]


def palmas(forte=1.0):
    """A torcida batendo palma: três caixas curtas e abertas, um pouco fora de tempo umas das outras."""
    a = caixa(0.55 * forte)
    return a


def arena():
    m = Musica("arena", 174, PROG, ACORDES, SECOES, laco=8, semente=174072)
    assert m.compassos == 72
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT
    GALOPE = ((0, 2), (2, 1), (3, 1))
    PALMA = palmas()

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        refrao = sec == "Golpe final" and local >= 8

        # ------------------------------------------------ cordas correndo (base)
        if sec == "Entrada" and local >= 4:
            for k in range(16):
                m.poe(m.base, pan(cordas(notas[0] + (12 if k % 2 == 0 else 24), S16 * 0.8, 0.35 + 0.15 * (local - 4)), 0.25 * (1 if k % 2 else -1)), t0 + k * S16)
        elif sec in ("Duelo", "Choque") or refrao or sec == "Retorno":
            seq = [notas[0] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12, notas[1] + 24]
            for k in range(16):
                m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, 0.85 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad e coro
        if sec == "Entrada":
            m.poe(m.base_sala, pad(notas, BAR, 0.55 + 0.05 * local, 1400 + 220 * local), t0)
            if local >= 2:
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.5 + 0.07 * local), t0)
        elif sec == "Estratégia":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 2200), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.9), t0)
        elif sec == "Golpe final":
            m.poe(m.base_sala, pad(notas, BAR, 0.55, 3400), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.9 if local < 8 else 1.05), t0)
        else:
            m.poe(m.base_sala, pad(notas, BAR, 0.45, 2900), t0)
            if sec == "Duelo":
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.45), t0)

        # ------------------------------------------------ a Entrada: taikos, palmas da torcida, metais chamando
        if sec == "Entrada":
            for k in range(4):                                                   # torcida: palma, palma, (pausa), palma
                for p in (0, 2) if k % 2 == 0 else (0,):
                    m.poe(m.base_sala, pan(PALMA, -0.3 + 0.2 * k), t0 + (k * 4 + p) * S16, 0.8 + 0.06 * local)
            if local in (0, 2, 4):
                m.poe(m.base, m.IMPACTO, t0, 0.9)
                m.poe(m.base, timpano(42, 1.1), t0)
            for k in range(4 if local < 4 else 8 if local < 6 else 16):
                passo = BAR / (4 if local < 4 else 8 if local < 6 else 16)
                m.poe(m.base, taiko(0.45 + 0.07 * local + 0.25 * (k % 4 == 0)), t0 + k * passo)
            if local in (1, 3, 5):
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.4, 1.15), t0)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.0), t0 + BEAT * 2.5)
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.1, 1.1), t0 + BEAT * 3)
            if local == 4:
                m.poe(m.base_sala, pan(sino_grande(54, 0.7), -0.15), t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.25), t0)
                m.poe(m.pulso, guitarra(pc, BAR * 1.9, 0.9), t0)

        # ------------------------------------------------ baixo
        if sec == "Duelo" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)
        elif sec == "Choque":
            for k in range(16):
                m.poe(m.base, baixo(raiz + (12 if k in (6, 14) else 0), S16 * 0.8, 1.05 if k % 4 == 0 else 0.85), t0 + k * S16)
        elif sec == "Estratégia":
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.9), t0 + p * S16)
        elif sec == "Golpe final":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
        elif sec == "Retorno":
            if local < 6:
                for pos, d in ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2)):
                    m.poe(m.base, baixo(raiz, S16 * d * 0.9, 1.05), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.base, baixo(raiz, passo * 0.8, 0.85 + 0.1 * (local - 6)), t0 + k * passo)

        # ------------------------------------------------ guitarras (pulso)
        if sec == "Duelo" or refrao:
            for beat in range(4):
                for p, d in GALOPE:
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)
        elif sec == "Choque":
            for k in range(16):
                aberto = k in (0, 6, 12)                                          # acento 3+3+2 por cima das semicolcheias
                m.poe(m.pulso, guitarra(pc, S16 * (3 if aberto else 0.7), 1.0 if aberto else 0.78, abafada=not aberto), t0 + k * S16)
        elif sec == "Estratégia" and local >= 6:
            m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.6 + 0.3 * (local - 6)), t0)
        elif sec == "Golpe final":
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.0), t0 + pos * S16)
        elif sec == "Retorno":
            if local < 6:
                for pos, d in ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2)):
                    m.poe(m.pulso, guitarra(pc, d * S16 * 0.85, 1.05, abafada=d < 2), t0 + pos * S16)
            else:
                passo = BEAT / 2 if local == 6 else S16
                for k in range(int(BAR / passo)):
                    m.poe(m.pulso, guitarra(pc, passo * 0.5, 0.75 + 0.15 * (local - 6), abafada=True), t0 + k * passo)

        # ------------------------------------------------ bateria
        if sec == "Duelo":
            m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.1)
            if local in (7, 15):
                m.virada_de_tons(t0, [57, 54, 52, 50, 47, 45, 42, 40])
        elif sec == "Choque":
            if local < 8:
                m.bat(range(16), m.BUMBO, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            else:
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat([0, 8], PALMA, m.base_sala, t0, 0.7)                      # a torcida volta
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.0)
            if local == 15:
                m.virada_de_tons(t0, [59, 57, 54, 52, 50, 47, 45, 42])
        elif sec == "Estratégia":
            m.bat([0, 10], m.BUMBO, m.base, t0)
            m.bat([8], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 0.8)
                m.poe(m.pulso, m.PRATO, t0, 0.7)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        elif sec == "Golpe final":
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
            if local == 7:                                                       # a subida para sol sustenido menor
                m.poe(m.base, riser(BAR, 1.3), t0)
                m.virada_de_tons(t0, [59, 57, 54, 52, 50, 47, 45, 44])
        elif sec == "Retorno":
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
        if sec == "Duelo" and local == 0:
            m.frase(m.tema_eco, TEMA, t0, forte=1.05, brilho=5800, voz="ambos")
        if sec == "Choque":
            if local < 8:
                for k, nota in enumerate(corrida(notas)):
                    m.poe(m.tema_eco, supersaw(nota, S16 * 0.9, 0.62 + 0.18 * (k % 4 == 0), 6200, False), t0 + k * S16)
            else:
                # pergunta nos metais, resposta no supersaw
                for pos, d in ((0, 2), (3, 2), (6, 2)):
                    m.poe(m.tema, metais([n + 12 for n in notas], S16 * d * 0.9, 1.15), t0 + pos * S16)
                topo = sorted(n + 24 for n in notas)
                for pos, d, nota in ((8, 2, topo[2]), (10, 2, topo[1]), (12, 4, topo[0] + (12 if topo[0] < 72 else 0))):
                    m.poe(m.tema_eco, supersaw(nota, S16 * d * 0.92, 0.95, 5600), t0 + pos * S16)
        if sec == "Estratégia":
            if local == 0:
                m.frase(m.tema_eco, LAMENTO, t0, forte=0.85, brilho=3400)
            seq = [notas[0] + 24, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k, nota in enumerate(seq):
                m.poe(m.tema_eco, pan(v4.sino(nota, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
        if sec == "Golpe final":
            if local == 0:
                m.frase(m.tema_eco, HINO, t0, forte=1.1, brilho=6000, dobra=-12)
                m.frase(m.tema, HINO, t0, transp=-12, forte=0.55, voz="metal")
            if local == 8:
                m.frase(m.tema_eco, REFRAO, t0, forte=1.15, brilho=6200, dobra=12, ganho_dobra=0.4)
                m.frase(m.tema, REFRAO, t0, transp=-12, forte=0.65, voz="metal")
        if sec == "Retorno":
            if local < 6 and local % 2 == 0:
                m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.9, 1.2), t0)
                m.poe(m.tema, metais([n + 12 for n in m.acorde(b + 1)[1]], BEAT * 0.9, 1.2), t0 + BEAT * 1.5)
            if local == 2:
                m.frase(m.tema_eco, [(0, 1, 78), (1, 1, 79), (2, 2, 78), (4, 1, 81), (5, 1, 79), (6, 2, 78),
                                     (8, 1, 78), (9, 1, 79), (10, 2, 81), (12, 1, 85), (13, 1, 83), (14, 2, 79)], t0, forte=0.95)
            if local >= 6:
                m.poe(m.tema_eco, supersaw(80 + 2 * (local - 6), BAR * 0.95, 0.6 + 0.15 * (local - 6), 2600 + 1500 * (local - 6), False), t0)

    m.renderiza("anime arcade · arena do PvP (v6)")


if __name__ == "__main__":
    arena()
