#!/usr/bin/env python3
"""
Música de batalha (versão 3): um tema de luta de verdade, que cresce.

O pedido: música de BATALHA — empolgante, boa de ouvir, sem virar barulho —
de 2 a 2,5 minutos, com fases diferentes, que cresce conforme a luta cresce.

A peça (138 BPM, ré menor, 84 compassos ≈ 2 min 26 s):

  Intro  (1–8)    tensão: cordas graves em semicolcheia, taikos, tímpanos,
                  um sopro que sobe e um corte seco antes de entrar.
  Encontro (9–24) a luta começa: bateria inteira, baixo em colcheia,
                  ostinato de cordas, acordes de guitarra sintética e um
                  contracanto de metais.  i – VI – III – VII.
  Choque (25–40)  o tema heroico na frente (metal + cordas em oitava),
                  bateria mais cheia, viradas de tom-tom.
  Ponte (41–48)   respira sem perder a tensão: meio-tempo, coro, sino,
                  e uma subida de caixa até o B maior.
  Clímax (49–72)  sobe um tom (mi menor): o tema em oitavas com coro e
                  bateria dobrada; fecha com notas longas no alto.
  Virada (73–84)  um riff pesado em ré com o segundo grau menor, e quatro
                  compassos de dominante subindo — que levam de volta ao
                  Encontro: o laço é do compasso 9 ao fim.

Cada luta começa na Intro. Se a luta durar mais que a música, ela volta ao
Encontro (não à Intro). Três camadas que o jogo mistura pela intensidade:

  base   bateria principal, baixo, cordas, pads, tímpanos e efeitos;
  pulso  pratos, percussão extra, arpejos e acordes de guitarra;
  tema   melodia, contracanto de metais, coro e sino.

Todos os instrumentos são sintetizados aqui (serras com polyBLEP, filtros,
ruído), nada é amostrado. Determinístico: a mesma semente gera o mesmo som.

Uso: python3 tools/audio/generate_music_v3.py   (gera public/assets/audio/musica-*.ogg e .mp3)
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from som import passa_tudo, pente  # noqa: E402

SR = 32000
BPM = 138
BEAT = 60 / BPM
BAR = BEAT * 4
S16 = BEAT / 4
BARS = 84
LACO = 8                       # o laço volta para o compasso 9 (índice 8)
N = int(round(BARS * BAR * SR))
CAUDA = int(3 * SR)
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get("SAIDA_MUSICA", ROOT / "public/assets/audio"))
rng = np.random.default_rng(138084)


# ================================================================== básico
def hz(m):
    return 440.0 * 2 ** ((np.asarray(m, dtype=float) - 69) / 12)


def _sos(kind, f, o=2):
    return butter(o, f, kind, fs=SR, output="sos")


def lp(x, f, o=2):
    return sosfilt(_sos("lowpass", min(f, SR * 0.45), o), x, axis=0)


def hp(x, f, o=2):
    return sosfilt(_sos("highpass", f, o), x, axis=0)


def bp(x, a, b, o=2):
    return sosfilt(_sos("bandpass", [a, min(b, SR * 0.45)], o), x, axis=0)


def tempo(n):
    return np.arange(n) / SR


def adsr(n, a=0.005, d=0.1, s=0.7, r=0.1, dur=None):
    """Envelope ADSR; `dur` é quando a nota solta (o resto do vetor é o release)."""
    t = tempo(n)
    dur = n / SR - r if dur is None else dur
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    solta = np.clip(1 - (t - dur) / max(r, 1e-4), 0, 1)
    return e * np.where(t > dur, solta, 1)


def polyblep(fase, dt):
    out = np.zeros_like(fase)
    m = fase < dt
    t = fase[m] / dt[m] if np.ndim(dt) else fase[m] / dt
    out[m] = t + t - t * t - 1
    m2 = fase > 1 - (dt if np.ndim(dt) == 0 else dt)
    t2 = (fase[m2] - 1) / (dt[m2] if np.ndim(dt) else dt)
    out[m2] = t2 * t2 + t2 + t2 + 1
    return out


def serra(freq, n, fase0=0.0):
    """Serra com polyBLEP (sem aliasing feio). `freq` pode variar no tempo."""
    f = np.broadcast_to(np.asarray(freq, dtype=float), (n,))
    dt = f / SR
    fase = (fase0 + np.cumsum(dt)) % 1.0
    return 2 * fase - 1 - polyblep(fase, dt)


def quadrada(freq, n, fase0=0.0):
    return 0.5 * (serra(freq, n, fase0) - serra(freq, n, (fase0 + 0.5) % 1))


def seno(freq, n, fase0=0.0):
    f = np.broadcast_to(np.asarray(freq, dtype=float), (n,))
    return np.sin(2 * math.pi * (fase0 + np.cumsum(f) / SR))


def ruido(n):
    return rng.standard_normal(n)


def pan(sinal, p=0.0):
    a = (p + 1) * math.pi / 4
    return np.stack([sinal * math.cos(a), sinal * math.sin(a)], 1)


def poe(dest, x, em_seg):
    i = int(round(em_seg * SR))
    if x.ndim == 1:
        x = pan(x)
    j = min(len(dest), i + len(x))
    if j > i >= 0:
        dest[i:j] += x[: j - i]


def sala(x, tamanho=0.8, umido=0.3, escuro=5500):
    def lado(sig, atrasos):
        y = sum(pente(sig, d, 0.74 + 0.2 * tamanho) for d in atrasos) / len(atrasos)
        for d, g in ((347, 0.6), (113, 0.6)):
            y = passa_tudo(y, d, g)
        return lp(hp(y, 200), escuro)
    mono = x.mean(axis=1)
    l = lado(mono, [1557, 1617, 1491, 1422])
    r = lado(mono, [1277, 1356, 1188, 1116])
    return x * (1 - umido * 0.25) + np.stack([l, r], 1) * umido


def satura(x, k=2.0):
    return np.tanh(x * k) / math.tanh(k)


# ================================================================== instrumentos
def i_bumbo(forte=1.0):
    n = int(0.42 * SR)
    t = tempo(n)
    f = 46 + 110 * np.exp(-t / 0.028)
    corpo = seno(f, n) * np.exp(-t / 0.2)
    clique = bp(ruido(n), 1500, 6000) * np.exp(-t / 0.004) * 0.35
    return satura(corpo * 1.3 + clique, 1.6) * 0.9 * forte


def i_caixa(forte=1.0):
    n = int(0.35 * SR)
    t = tempo(n)
    corpo = seno(185 * (1 + 0.25 * np.exp(-t / 0.01)), n) * np.exp(-t / 0.06) * 0.55
    esteira = bp(ruido(n), 1800, 9000) * np.exp(-t / 0.11) * 0.9
    estalo = hp(ruido(n), 3000) * np.exp(-t / 0.006) * 0.4
    return satura(corpo + esteira + estalo, 1.3) * 0.55 * forte


def i_chimbal(aberto=False, forte=1.0):
    n = int((0.45 if aberto else 0.07) * SR)
    t = tempo(n)
    metal = sum(quadrada(f, n) for f in (3150, 4370, 5210, 6580)) * 0.25
    x = hp(ruido(n) * 0.6 + metal * 0.5, 7000) * np.exp(-t / (0.18 if aberto else 0.022))
    return x * 0.18 * forte


def i_prato(forte=1.0, dur=2.6):
    n = int(dur * SR)
    t = tempo(n)
    metal = sum(quadrada(f * rng.uniform(0.98, 1.02), n) for f in (2310, 3170, 4120, 5390, 6830)) * 0.2
    x = hp(ruido(n) * 0.7 + metal * 0.4, 4500) * np.exp(-t / (dur * 0.38)) * (1 - np.exp(-t / 0.002))
    return x * 0.22 * forte


def i_condução(forte=1.0):
    n = int(0.6 * SR)
    t = tempo(n)
    sino = sum(seno(f, n) * g for f, g in ((3400, 0.4), (5100, 0.3), (7300, 0.2)))
    x = hp(ruido(n) * 0.3 + sino * 0.5, 3000) * np.exp(-t / 0.28)
    return x * 0.11 * forte


def i_tom(nota, forte=1.0):
    n = int(0.5 * SR)
    t = tempo(n)
    f = hz(nota) * (1 + 0.4 * np.exp(-t / 0.03))
    x = seno(f, n) * np.exp(-t / 0.22) + bp(ruido(n), 200, 2000) * np.exp(-t / 0.02) * 0.3
    return satura(x, 1.4) * 0.6 * forte


def i_taiko(forte=1.0):
    n = int(1.1 * SR)
    t = tempo(n)
    f = 58 + 60 * np.exp(-t / 0.05)
    x = seno(f, n) * np.exp(-t / 0.45) + bp(ruido(n), 80, 900) * np.exp(-t / 0.05) * 0.7
    return satura(x, 1.8) * 0.75 * forte


def i_timpano(nota, forte=1.0, dur=1.6):
    n = int(dur * SR)
    t = tempo(n)
    f = hz(nota) * (1 + 0.06 * np.exp(-t / 0.08))
    x = (seno(f, n) + 0.5 * seno(f * 1.5, n) * np.exp(-t / 0.3) + 0.3 * seno(f * 2.0, n)) * np.exp(-t / (dur * 0.4))
    x += lp(ruido(n), 1200) * np.exp(-t / 0.03) * 0.4
    return x * 0.5 * forte


def i_baixo(nota, dur, forte=1.0):
    n = int((dur + 0.08) * SR)
    f = hz(nota)
    x = serra(f, n) * 0.7 + seno(f, n) * 0.8 + serra(f * 1.005, n) * 0.3
    claro = lp(x, 1400)
    escuro = lp(x, 380)
    t = tempo(n)
    abre = np.exp(-t / 0.07)
    x = escuro * (1 - abre) + claro * abre
    return satura(x * adsr(n, 0.004, 0.15, 0.75, 0.06, dur), 1.6) * 0.42 * forte


def i_cordas_curtas(nota, dur, forte=1.0):
    """Cordas em spiccato (o ostinato que corre por baixo)."""
    n = int((dur + 0.1) * SR)
    f = hz(nota)
    x = sum(serra(f * 2 ** (d / 1200), n, rng.uniform()) for d in (-11, -4, 3, 9, 14)) / 5
    x = lp(x, 2600)
    return x * adsr(n, 0.006, 0.09, 0.25, 0.07, dur) * 0.32 * forte


def i_pad(notas, dur, forte=1.0, brilho=1800):
    n = int((dur + 1.2) * SR)
    out = np.zeros((n, 2))
    for k, m in enumerate(notas):
        f = hz(m)
        for p, d in ((-0.55, -9), (0.55, 9), (0.0, 0)):
            x = serra(f * 2 ** (d / 1200), n, rng.uniform()) + 0.6 * serra(f * 2 ** ((d + 5) / 1200), n, rng.uniform())
            out += pan(x, p)
    out = lp(out, brilho)
    e = adsr(n, 0.5, 0.6, 0.85, 1.1, dur)
    return out * e[:, None] * 0.045 * forte


def i_guitarra(notas, dur, forte=1.0):
    """Acorde de força (fundamental, quinta, oitava) distorcido, como guitarra pesada."""
    n = int((dur + 0.12) * SR)
    x = np.zeros(n)
    for m in notas:
        f = hz(m)
        x += serra(f * 0.997, n, rng.uniform()) + serra(f * 1.003, n, rng.uniform())
    x = satura(hp(x, 90) * 1.4, 4.5)
    x = lp(bp(x, 100, 5000), 3200)
    return x * adsr(n, 0.003, 0.18, 0.55, 0.08, dur) * 0.25 * forte


def i_metal(nota, dur, forte=1.0, brilho=1.0):
    """Metais sintéticos: serras abrindo o filtro no ataque, vibrato depois de um tempo."""
    n = int((dur + 0.22) * SR)
    t = tempo(n)
    vib = 1 + 0.004 * np.sin(2 * math.pi * 5.2 * t) * np.clip((t - 0.25) / 0.3, 0, 1)
    f = hz(nota) * vib
    x = sum(serra(f * 2 ** (d / 1200), n, rng.uniform()) for d in (-7, 0, 7)) / 3
    abre = np.clip(1 - np.exp(-t / 0.05), 0, 1) * (0.55 + 0.45 * np.exp(-t / 0.35))
    x = lp(x, 900 * brilho) * (1 - abre) + lp(x, 3800 * brilho) * abre
    return x * adsr(n, 0.025, 0.25, 0.8, 0.2, dur) * 1.15 * forte


def i_coro(notas, dur, forte=1.0):
    """Coro "ah": serras passando por formantes de vogal, com vibrato lento."""
    n = int((dur + 1.0) * SR)
    t = tempo(n)
    out = np.zeros((n, 2))
    for m in notas:
        for p, d in ((-0.5, -8), (0.5, 8)):
            f = hz(m) * 2 ** (d / 1200) * (1 + 0.006 * np.sin(2 * math.pi * 4.6 * t + rng.uniform(0, 6)))
            x = serra(f, n, rng.uniform())
            v = bp(x, 650, 950) * 1.0 + bp(x, 1050, 1300) * 0.6 + bp(x, 2500, 2900) * 0.25
            out += pan(v, p)
    e = adsr(n, 0.35, 0.5, 0.9, 0.9, dur)
    return out * e[:, None] * 0.38 * forte


def i_sino(nota, forte=1.0):
    n = int(1.4 * SR)
    t = tempo(n)
    f = hz(nota)
    x = sum(seno(f * r, n) * g * np.exp(-t / q) for r, g, q in ((1, 1, 0.9), (2.0, 0.5, 0.5), (3.01, 0.3, 0.3), (4.2, 0.15, 0.2)))
    return x * 0.42 * forte


def i_arpejo(nota, forte=1.0):
    n = int(0.3 * SR)
    t = tempo(n)
    x = serra(hz(nota), n) * 0.6 + quadrada(hz(nota) * 2, n) * 0.25
    x = lp(x, 3000) * np.exp(-t / 0.09)
    return x * 0.14 * forte


def i_sopro(dur, f0=300, f1=6000, forte=1.0):
    """Subida de ruído filtrado (o "riser" antes de uma entrada)."""
    n = int(dur * SR)
    t = tempo(n)
    x = ruido(n)
    centro = f0 * (f1 / f0) ** (t / dur)
    y = np.zeros(n)
    blocos = 32
    for b in range(blocos):
        i, j = b * n // blocos, (b + 1) * n // blocos
        c = centro[(i + j) // 2]
        y[i:j] = bp(x, c * 0.7, c * 1.3)[i:j]
    return y * (t / dur) ** 2 * 0.3 * forte


def i_impacto(forte=1.0):
    """O "boom" de uma entrada: sub grave, ruído e prato."""
    n = int(2.2 * SR)
    t = tempo(n)
    x = seno(38 + 50 * np.exp(-t / 0.06), n) * np.exp(-t / 0.7) * 1.2 + lp(ruido(n), 600) * np.exp(-t / 0.25) * 0.6
    return satura(x, 1.5) * 0.6 * forte


# ================================================================== harmonia
# acorde = (fundamental do baixo, notas do pad/coro)
def triade(raiz, menor):
    t = [raiz, raiz + (3 if menor else 4), raiz + 7]
    return t


def acorde(nome):
    tabela = {
        "Dm": (38, 62, True), "Bb": (34, 58, False), "F": (41, 65, False), "C": (36, 60, False), "A": (33, 57, False),
        "Gm": (31, 55, True), "B": (35, 59, False), "Em": (40, 64, True), "G": (43, 67, False), "D": (38, 62, False),
        "Am": (33, 57, True), "Eb": (39, 63, False),
    }
    baixo, raiz, menor = tabela[nome]
    notas = triade(raiz, menor)
    # voz próxima, centrada perto de 60–70
    notas = [m - 12 if m > 71 else m for m in notas]
    return baixo, sorted(notas)


PROG = (["Dm"] * 4 + ["Bb", "Bb", "C", "A"]                                         # Intro 0–7
        + ["Dm", "Bb", "F", "C"] * 4                                                 # Encontro 8–23
        + ["Dm", "Bb", "F", "C", "Dm", "Bb", "F", "A"] * 2                           # Choque 24–39
        + ["Gm", "Gm", "Bb", "Bb", "C", "C", "B", "B"]                               # Ponte 40–47
        + ["Em", "C", "G", "D", "Em", "C", "G", "B"] * 2                             # Clímax 48–63
        + ["Em", "C", "G", "D", "Am", "C", "D", "B"]                                 # Clímax final 64–71
        + ["Dm", "Dm", "Eb", "Dm", "Dm", "Dm", "Eb", "C"]                            # Virada 72–79
        + ["A", "A", "A", "A"])                                                     # subida 80–83
assert len(PROG) == BARS

SECOES = [("Intro", 0), ("Encontro", 8), ("Choque", 24), ("Ponte", 40), ("Clímax", 48), ("Virada", 72)]


def secao(b):
    nome = SECOES[0][0]
    for s, ini in SECOES:
        if b >= ini:
            nome = s
    return nome


# ================================================================== melodias (em tempos, a partir do compasso)
T1 = [(0, 1.5, 74), (1.5, .5, 69), (2, 1, 74), (3, 1, 76),
      (4, 2, 77), (6, 1, 76), (7, 1, 74),
      (8, 3, 72), (11, 1, 69),
      (12, 1, 72), (13, 1, 74), (14, 2, 76),
      (16, 1.5, 74), (17.5, .5, 69), (18, 1, 74), (19, 1, 77),
      (20, 2, 79), (22, 1, 77), (23, 1, 76),
      (24, 1.5, 81), (25.5, .5, 79), (26, 1, 77), (27, 1, 76),
      (28, 2, 76), (30, 1, 73), (31, 1, 69)]
T2 = [(0, 1.5, 74), (1.5, .5, 69), (2, 1, 74), (3, 1, 76),
      (4, 2, 77), (6, 1, 79), (7, 1, 77),
      (8, 2, 81), (10, 1, 79), (11, 1, 77),
      (12, 1, 76), (13, 1, 77), (14, 2, 79),
      (16, 3, 81), (19, 1, 77),
      (20, 2, 82), (22, 1, 81), (23, 1, 79),
      (24, 2, 77), (26, 1, 76), (27, 1, 74),
      (28, 2, 76), (30, 2, 73)]
FINAL = [(0, 4, 83), (4, 4, 84), (8, 4, 86), (12, 2, 81), (14, 2, 78),
         (16, 4, 84), (20, 4, 79), (24, 2, 78), (26, 2, 81), (28, 4, 75)]
CONTRA = [(0, 1.5, 62), (1.5, .5, 62), (2, 1, 65), (3, 1, 64), (4, 3, 62), (7, 1, 60),
          (8, 1.5, 60), (9.5, .5, 60), (10, 1, 65), (11, 1, 67), (12, 3, 67), (15, 1, 64)]
RIFF_TEMA = [(0, 1.5, 74), (1.5, .5, 69), (2, 1, 74), (3, 1, 76), (4, 4, 77),
             (8, 1.5, 74), (9.5, .5, 69), (10, 1, 74), (11, 1, 72), (12, 4, 74)]


# ================================================================== arranjo
def bar_t(b):
    return b * BAR


def main():
    base = np.zeros((N + CAUDA, 2))
    pulso = np.zeros((N + CAUDA, 2))
    tema = np.zeros((N + CAUDA, 2))
    # caminhos separados para o que recebe sala
    base_sala = np.zeros_like(base)
    tema_sala = np.zeros_like(tema)

    bumbo = [i_bumbo(f) for f in (0.7, 1.0)]
    caixas = [i_caixa(f) for f in (0.35, 1.0, 1.15)]
    chimbais = [i_chimbal(False, f) for f in (0.6, 1.0)] + [i_chimbal(True)]
    taiko = i_taiko()
    prato = i_prato()
    conducao = i_condução()

    for b in range(BARS):
        sec = secao(b)
        t0 = bar_t(b)
        nome = PROG[b]
        raiz_baixo, pad_notas = acorde(nome)
        tr = 0  # tudo já está na tonalidade certa pela progressão
        local = b - dict(SECOES)[sec]

        # ---------------------------------------------------- pads e cordas
        if sec in ("Intro",):
            poe(base_sala, i_pad([raiz_baixo + 12, raiz_baixo + 19], BAR, 0.8, 1200), t0)
        elif sec == "Ponte":
            poe(base_sala, i_pad(pad_notas, BAR, 1.0, 1500), t0)
        elif sec != "Virada" or b >= 80:
            poe(base_sala, i_pad(pad_notas, BAR, 0.75 if sec == "Encontro" else 0.9, 2000), t0)

        # ostinato de cordas em semicolcheia (raiz/quinta/oitava, padrão que gira)
        if sec != "Ponte":
            padrao = [0, 12, 7, 12, 0, 12, 7, 15] if pad_notas[1] - pad_notas[0] == 3 else [0, 12, 7, 12, 0, 12, 7, 16]
            raiz_ost = raiz_baixo + 24
            passo = 1 if sec in ("Intro",) else 1
            for k in range(0, 16, passo):
                m = raiz_ost + padrao[k % 8]
                forte = 0.55 + 0.25 * (k % 4 == 0)
                if sec == "Intro":
                    forte *= 0.5 + 0.5 * (local / 8)
                poe(base, i_cordas_curtas(m, S16 * 0.8, forte), t0 + k * S16)

        # ---------------------------------------------------- baixo
        if sec == "Intro":
            if local >= 4:
                for k in range(8):
                    poe(base, i_baixo(raiz_baixo, BEAT * 0.45, 0.7), t0 + k * BEAT / 2)
        elif sec == "Ponte":
            for k in range(8):
                poe(base, i_baixo(raiz_baixo, BEAT * 0.4, 0.6 + 0.05 * local), t0 + k * BEAT / 2)
        elif sec == "Virada" and b < 80:
            # riff: semicolcheias sincopadas com o segundo grau menor
            riff = [(0, 0), (3, 0), (6, 0), (8, 3), (10, 0), (13, 1), (14, 0)]
            for pos, inter in riff:
                poe(base, i_baixo(raiz_baixo + inter, S16 * 1.6, 1.1), t0 + pos * S16)
                poe(pulso, i_guitarra([raiz_baixo + 12 + inter, raiz_baixo + 19 + inter, raiz_baixo + 24 + inter], S16 * 1.4, 1.1), t0 + pos * S16)
        else:
            for k in range(8):
                oit = 12 if (k % 4 == 3) else 0
                poe(base, i_baixo(raiz_baixo + oit, BEAT * 0.42, 0.95 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)

        # ---------------------------------------------------- bateria
        def bat(lista, amostra, alvo):
            for p in lista:
                poe(alvo, amostra, t0 + p * S16)

        if sec == "Intro":
            bat([0, 8] if local < 6 else [0, 4, 8, 12], taiko, base_sala)
            if local == 0:
                poe(base_sala, i_timpano(38, 1.0, 2.0), t0)
            if local in (6, 7):
                for k in range(16 if local == 6 else 12):
                    poe(base, i_caixa(0.25 + 0.6 * k / 16), t0 + k * S16)
            if local == 6:
                poe(base, i_sopro(BAR * 2 - BEAT, 300, 7000, 1.0), t0)
        elif sec == "Encontro":
            bat([0, 6, 10], bumbo[1], base)
            bat([4, 12], caixas[1], base_sala)
            bat(list(range(0, 16, 2)), chimbais[1], pulso)
            if local % 4 == 3:
                poe(pulso, chimbais[2], t0 + 14 * S16)
            bat([0, 8], taiko, pulso)
            if local == 0:
                poe(base, prato, t0)
                poe(base, i_impacto(1.0), t0)
            if local == 15:
                for k, nota in enumerate([50, 50, 47, 47, 43, 43]):
                    poe(base, i_tom(nota, 0.9), t0 + (10 + k) * S16)
        elif sec == "Choque":
            bat([0, 3, 6, 10, 11], bumbo[1], base)
            bat([4, 12], caixas[2], base_sala)
            bat([7, 15], caixas[0], base)
            for k in range(16):
                poe(pulso, chimbais[k % 2 == 0], t0 + k * S16)
            if local in (0, 8):
                poe(base, prato, t0)
            if local == 0:
                poe(base, i_impacto(1.0), t0)
            if local in (7, 15):
                for k, nota in enumerate([52, 50, 47, 45, 43, 40, 40, 38]):
                    poe(base, i_tom(nota, 1.0), t0 + (8 + k) * S16)
        elif sec == "Ponte":
            bat([0, 10], bumbo[0], base)
            bat([8], caixas[1], base_sala)
            bat(list(range(0, 16, 4)), chimbais[0], pulso)
            if local == 0:
                poe(base, i_impacto(0.8), t0)
            if local >= 6:
                for k in range(16):
                    poe(base, i_caixa(0.2 + 0.8 * ((local - 6) * 16 + k) / 32), t0 + k * S16)
            if local == 6:
                poe(base, i_sopro(BAR * 2, 200, 8000, 1.2), t0)
                poe(base_sala, i_timpano(35, 0.8, 3.0), t0)
        elif sec == "Clímax":
            bat([0, 3, 6, 8, 11, 14], bumbo[1], base)
            bat([4, 12], caixas[2], base_sala)
            bat([15], caixas[0], base)
            for k in range(0, 16, 2):
                poe(pulso, conducao, t0 + k * S16)
            bat([0, 6, 8], taiko, pulso)
            if local % 4 == 0:
                poe(base, prato, t0)
            if local == 0:
                poe(base, i_impacto(1.2), t0)
            if local in (7, 15):
                for k, nota in enumerate([55, 52, 50, 47, 45, 43, 42, 40]):
                    poe(base, i_tom(nota, 1.0), t0 + (8 + k) * S16)
            if local == 23:
                poe(base, i_sopro(BAR, 400, 6000, 0.8), t0)
        elif sec == "Virada":
            if b < 80:
                bat([0, 3, 6, 8, 10, 13, 14], bumbo[1], base)
                bat([4, 12], caixas[2], base_sala)
                for k in range(0, 16, 2):
                    poe(pulso, chimbais[1], t0 + k * S16)
                if local == 0:
                    poe(base, prato, t0)
                    poe(base, i_impacto(1.0), t0)
                if local == 4:
                    poe(base, prato, t0)
            else:
                # quatro compassos de dominante subindo para o Encontro
                q = b - 80
                bat([0, 8] if q < 2 else [0, 4, 8, 12], bumbo[1], base)
                passos = 8 if q < 2 else 16
                for k in range(passos):
                    poe(base, i_caixa(0.3 + 0.7 * (q * 16 + k * (16 // passos)) / 64), t0 + k * (16 // passos) * S16)
                bat([0, 8], taiko, pulso)
                if q == 0:
                    poe(base, i_sopro(BAR * 4 - BEAT * 0.5, 200, 9000, 1.3), t0)
                    poe(base_sala, i_timpano(33, 1.0, 3.0), t0)

        # ---------------------------------------------------- acordes de guitarra (pulso)
        if sec in ("Encontro", "Choque", "Clímax"):
            power = [raiz_baixo + 12, raiz_baixo + 19, raiz_baixo + 24]
            for pos, dur in ((0, 5), (6, 4), (10, 6)):
                poe(pulso, i_guitarra(power, dur * S16 * 0.9, 0.9), t0 + pos * S16)

        # arpejo agudo (pulso) a partir da metade do Encontro e no Clímax
        if (sec == "Encontro" and local >= 8) or sec == "Clímax":
            notas = sorted(pad_notas) + [pad_notas[0] + 12]
            for k in range(16):
                poe(pulso, pan(i_arpejo(notas[k % 4] + 12, 0.8 + 0.2 * (k % 4 == 0)), 0.35 * (1 if k % 2 else -1)), t0 + k * S16)

        # ---------------------------------------------------- tema
        if sec == "Encontro" and local % 4 == 0:
            for (ini, dur, m) in CONTRA:
                poe(tema_sala, pan(i_metal(m, dur * BEAT * 0.95, 0.9, 0.8), -0.25), t0 + ini * BEAT)
        if sec == "Choque" and local % 8 == 0:
            frase = T1 if local == 0 else T2
            for (ini, dur, m) in frase:
                poe(tema_sala, i_metal(m, dur * BEAT * 0.95, 1.0), t0 + ini * BEAT)
                poe(tema_sala, pan(i_cordas_curtas(m - 12, dur * BEAT * 0.9, 0.5), 0.3), t0 + ini * BEAT)
        if sec == "Ponte":
            arpeggio = [pad_notas[0] + 12, pad_notas[1] + 12, pad_notas[2] + 12, pad_notas[1] + 12]
            for k, m in enumerate(arpeggio):
                poe(tema_sala, i_sino(m, 0.9), t0 + k * BEAT)
            poe(tema_sala, i_coro(pad_notas, BAR, 0.8 + 0.05 * local), t0)
        if sec == "Clímax":
            if local in (0, 8):
                frase = T1 if local == 0 else T2
                for (ini, dur, m) in frase:
                    m2 = m + 2
                    poe(tema_sala, i_metal(m2, dur * BEAT * 0.95, 1.1, 1.1), t0 + ini * BEAT)
                    poe(tema_sala, pan(i_metal(m2 - 12, dur * BEAT * 0.95, 0.7, 0.8), -0.3), t0 + ini * BEAT)
            if local == 16:
                for (ini, dur, m) in FINAL:
                    poe(tema_sala, i_metal(m - 12, dur * BEAT * 0.97, 1.15, 1.1), t0 + ini * BEAT)
                    poe(tema_sala, pan(i_metal(m - 24, dur * BEAT * 0.97, 0.75, 0.8), 0.3), t0 + ini * BEAT)
            poe(tema_sala, i_coro([n + 12 for n in pad_notas], BAR, 0.9), t0)
        if sec == "Virada" and local in (4,):
            for (ini, dur, m) in RIFF_TEMA:
                poe(tema_sala, i_metal(m, dur * BEAT * 0.95, 1.0), t0 + ini * BEAT)
        if sec == "Virada" and b >= 80:
            poe(tema_sala, i_coro([57, 61, 64], BAR, 0.6 + 0.15 * (b - 80)), t0)

    # ---------------------------------------------------- sala, laço e mixagem
    base = base + sala(base_sala, 0.8, 0.32)
    tema = tema + sala(tema_sala, 0.85, 0.38)
    pulso = sala(pulso, 0.5, 0.12)

    # equalização: grave no lugar (o celular nem toca abaixo de ~120 Hz, e grave demais embola),
    # médio-agudo mais presente para a melodia e as guitarras aparecerem
    def eq(x, corte_grave=0.55, presenca=0.0):
        x = hp(x, 38, 2)
        x = x - corte_grave * lp(x, 140, 2)
        if presenca:
            x = x + presenca * bp(x, 1200, 4200, 2)
        return x
    base = eq(base, 0.6, 0.25)
    pulso = eq(pulso, 0.5, 0.35)
    tema = eq(tema, 0.3, 0.45)

    ini_laco = int(round(LACO * BAR * SR))

    def fecha(x):
        # o rabo depois do fim volta no começo do laço (o Encontro): emenda sem buraco
        y = x[:N].copy()
        y[ini_laco:ini_laco + CAUDA] += x[N:N + CAUDA]
        return y

    camadas = {"musica-base": fecha(base), "musica-pulso": fecha(pulso), "musica-tema": fecha(tema)}
    np.save(OUT / "_mix.npy", sum(camadas.values()).astype(np.float32)) if os.environ.get("SAIDA_MUSICA") else None
    soma = sum(camadas.values())
    pico = np.max(np.abs(soma))
    ganho = 0.89 / pico
    info = {}
    OUT.mkdir(parents=True, exist_ok=True)
    for nome, x in camadas.items():
        x = x * ganho
        destino = OUT / f"{nome}.ogg"
        y = x.astype(np.float32)
        # em blocos de 1 s: o codificador Vorbis do libsndfile cai com arquivos longos de uma vez só
        with sf.SoundFile(destino, "w", SR, 2, format="OGG", subtype="VORBIS", compression_level=0.92) as arq:
            for i in range(0, len(y), SR):
                arq.write(y[i:i + SR])
        escreve_mp3(OUT / f"{nome}.mp3", y)
        rms = 20 * math.log10(float(np.sqrt(np.mean(x ** 2))) + 1e-9)
        info[nome] = {"arquivo": destino.name, "mp3": f"{nome}.mp3", "segundos": round(N / SR, 3), "bytes": destino.stat().st_size, "rmsDb": round(rms, 1)}
        print(f"{nome:14s} {destino.stat().st_size / 1024:7.1f} KB  rms {rms:6.1f} dB")
    secoes = [{"nome": s, "inicio": round(i * BAR, 3)} for s, i in SECOES]
    (OUT / "musica.json").write_text(json.dumps({
        "bpm": BPM, "compassos": BARS, "segundos": round(N / SR, 3), "secoes": secoes,
        "laco": {"inicio": round(LACO * BAR, 3), "fim": round(N / SR, 3)}, "camadas": info,
    }, indent=1, ensure_ascii=False) + "\n")


def escreve_mp3(destino, y, sr=SR):
    """A mesma camada em MP3: o iPhone/Safari nem sempre decodifica Ogg Vorbis, e
    sem a camada base o jogo cairia na música sintetizada antiga."""
    with sf.SoundFile(destino, "w", sr, 2, format="MP3", subtype="MPEG_LAYER_III", compression_level=0.55) as arq:
        for i in range(0, len(y), sr):
            arq.write(y[i:i + sr])


if __name__ == "__main__":
    main()
