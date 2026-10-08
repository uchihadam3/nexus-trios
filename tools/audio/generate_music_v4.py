#!/usr/bin/env python3
"""
Música de batalha v4: "anime arcade" — rock japonês rápido com sintetizadores neon.

A v3 era orquestral (taiko, cordas, coro, sinos) e destoava do jogo: arena
neon verde-limão, golpes de energia, raios, faíscas, personagens de anime e
desenho. Esta é a trilha de jogo de luta de anime:

- 156 BPM em mi menor, bateria de rock (bumbo, caixa estalada, chimbal,
  condução, pratos), baixo sintetizado pulsando em colcheias, guitarras
  distorcidas (power chords abertos e "chugs" abafados, galope no Choque);
- sintetizadores: arpejo brilhante em semicolcheias com eco (as faíscas),
  um "supersaw" heroico que canta o tema, pad largo e risers/impactos nas
  viradas, como os clarões dos golpes;
- seis fases que crescem: Intro (arpejo e subida), Encontro (tema A),
  Choque (tema B, galope), Ponte (meio-tempo, respiro), Clímax (hino e o
  refrão final um tom acima) e Virada (riff frígio e subida de volta).

As mesmas três camadas de antes (base, pulso e tema), em OGG e MP3, com o
laço voltando no Encontro: o jogo sobe pulso e tema conforme a luta esquenta.

Uso: python3 tools/audio/generate_music_v4.py   (gera public/assets/audio/musica-*.ogg e .mp3)
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v3 as v3  # noqa: E402  (filtros, osciladores, sala, MP3)
from generate_music_v3 import adsr, bp, escreve_mp3, hp, hz, lp, pan, quadrada, sala, satura, serra, seno  # noqa: E402

SR = v3.SR
BPM = 156
BEAT = 60 / BPM
BAR = BEAT * 4
S16 = BEAT / 4
BARS = 84
LACO = 8                       # o laço volta para o compasso 9 (o Encontro)
N = int(round(BARS * BAR * SR))
CAUDA = int(3 * SR)
OUT = v3.OUT
rng = np.random.default_rng(156084)


def ruido(n):
    return rng.standard_normal(n)


def poe(dest, x, em_seg, ganho=1.0):
    if ganho != 1.0:
        x = x * ganho
    v3.poe(dest, x, em_seg)


def n_(seg):
    return max(1, int(seg * SR))


def eco(x, atraso, fb=0.35, vezes=4, pingpong=True):
    """Eco em batidas (pingue-pongue): repetições que alternam de lado e escurecem."""
    d = int(atraso * SR)
    y = x.copy()
    eco_ = x.copy()
    for k in range(1, vezes + 1):
        eco_ = lp(eco_, 6000 - 700 * k) * fb
        lado = eco_[:, ::-1] if (pingpong and k % 2) else eco_
        y[d * k:] += lado[: len(y) - d * k]
    return y


# ================================================================== bateria (amostras feitas uma vez)
def bumbo(forte=1.0):
    n = n_(0.42)
    t = np.arange(n) / SR
    f = 48 + 120 * np.exp(-t / 0.028)
    corpo = np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    clique = hp(ruido(n), 2500) * np.exp(-t / 0.004) * 0.5
    return satura(corpo * 1.3 + clique, 1.6) * forte


def caixa(forte=1.0):
    n = n_(0.35)
    t = np.arange(n) / SR
    corpo = np.sin(2 * math.pi * np.cumsum(185 + 60 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.07)
    esteira = bp(ruido(n), 1800, 9000) * np.exp(-t / 0.13)
    estalo = hp(ruido(n), 4000) * np.exp(-t / 0.01)
    return satura(corpo * 0.8 + esteira * 0.9 + estalo * 0.5, 1.4) * forte


def chimbal(aberto=False, forte=1.0):
    n = n_(0.35 if aberto else 0.07)
    t = np.arange(n) / SR
    x = hp(ruido(n), 7000) + 0.3 * hp(quadrada(np.full(n, 3150.0), n) * quadrada(np.full(n, 4720.0), n), 6000)
    return x * np.exp(-t / (0.11 if aberto else 0.018)) * 0.45 * forte


def conducao(forte=1.0):
    n = n_(0.9)
    t = np.arange(n) / SR
    ping = sum(np.sin(2 * math.pi * f * t) * a for f, a in ((3350, .4), (5120, .3), (6900, .25), (8730, .2)))
    return (hp(ruido(n), 6000) * 0.4 + ping * 0.3) * np.exp(-t / 0.35) * 0.4 * forte


def prato(forte=1.0):
    n = n_(2.6)
    t = np.arange(n) / SR
    x = hp(ruido(n), 4500) * (np.exp(-t / 0.9) * 0.8 + np.exp(-t / 0.05) * 0.6)
    return x * 0.55 * forte


def tom(nota, forte=1.0):
    n = n_(0.45)
    t = np.arange(n) / SR
    f = hz(nota) * (1 + 0.5 * np.exp(-t / 0.03))
    return satura(np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2) + hp(ruido(n), 2000) * np.exp(-t / 0.01) * 0.3, 1.5) * forte


def impacto(forte=1.0):
    """O "boom" das viradas (como o clarão de um golpe grande)."""
    n = n_(2.2)
    t = np.arange(n) / SR
    boom = np.sin(2 * math.pi * np.cumsum(30 + 70 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.7)
    estouro = lp(ruido(n), 3000) * np.exp(-t / 0.25) * 0.5
    return satura(boom + estouro, 1.5) * forte


def riser(dur, forte=1.0):
    """Subida de ruído filtrado + tom que sobe: a carga antes de um golpe."""
    n = n_(dur)
    t = np.arange(n) / SR
    u = t / dur
    x = np.zeros(n)
    for k in range(0, n, 1024):
        f = 300 * (40 ** u[k])
        x[k:k + 1024] = bp(ruido(min(1024, n - k)), f * 0.7, min(f * 1.4, SR * 0.45))
    tomzinho = serra(200 * 8 ** u, n) * 0.08
    return (x * 0.6 + tomzinho) * u ** 2 * forte


def caixa_rolando(compassos, inicio=0.25):
    """Rufo de caixa que acelera e cresce até a próxima fase."""
    sinal = np.zeros(n_(compassos * BAR + 0.5))
    pos, total = 0.0, compassos * BAR
    while pos < total:
        u = pos / total
        passo = S16 if u < 0.5 else S16 / 2
        s = caixa(inicio + (1 - inicio) * u)
        i = int(pos * SR)
        sinal[i:i + len(s)] += s[: len(sinal) - i]
        pos += passo
    return sinal


# ================================================================== sintetizadores e guitarras
def baixo(nota, dur, forte=1.0):
    """Baixo sintetizado: serra + quadrada uma oitava abaixo, filtro que fecha (tem harmônicos para o celular)."""
    n = n_(dur + 0.05)
    t = np.arange(n) / SR
    f = hz(nota)
    x = serra(np.full(n, f), n) * 0.7 + quadrada(np.full(n, f / 2), n) * 0.5
    corte = 300 + 2200 * np.exp(-t / 0.07)
    y = np.zeros(n)
    for k in range(0, n, 512):
        y[k:k + 512] = lp(x[k:k + 512], float(corte[k]))
    return satura(y * 1.2, 1.8) * adsr(n, 0.003, 0.15, 0.75, 0.04, dur) * 0.75 * forte


def _distorce(x, ganho=6.0):
    """Amplificador + caixa de guitarra: satura forte e tira o "fizz" e o grave embolado."""
    y = np.tanh(hp(x, 90) * ganho)
    y = lp(y, 4800, 4)
    return y + 0.4 * bp(y, 1500, 3200)


def guitarra(notas, dur, forte=1.0, abafada=False, lado=0.0):
    """Power chord distorcido; abafada = "chug" curto e escuro (palm mute)."""
    n = n_(dur + (0.04 if abafada else 0.12))
    x = np.zeros(n)
    for m in notas:
        for d in (-0.06, 0.06):
            x += serra(np.full(n, hz(m) * 2 ** (d / 12)), n, rng.uniform(0, 1))
    e = adsr(n, 0.002, 0.06 if abafada else 0.4, 0.15 if abafada else 0.8, 0.04 if abafada else 0.1, dur)
    y = _distorce(x * e * 0.4, 7.0 if abafada else 5.0)
    if abafada:
        y = lp(y, 1600)
    y = y * forte * (0.55 if abafada else 0.5)
    # duas guitarras gravadas, uma em cada lado (o "paredão")
    outra = np.roll(y, int(0.011 * SR))
    return np.stack([y * (1 - lado) * 0.9 + outra * 0.25, outra * (1 + lado) * 0.9 + y * 0.25], 1)


def supersaw(nota, dur, forte=1.0, brilho=5200, vibrato=True):
    """O lead heroico: 7 serras desafinadas, vibrato que entra depois do ataque."""
    n = n_(dur + 0.25)
    t = np.arange(n) / SR
    vib = 1 + (0.006 * np.sin(2 * math.pi * 5.6 * t) * np.clip((t - 0.18) / 0.2, 0, 1) if vibrato else 0)
    l = np.zeros(n)
    r = np.zeros(n)
    for k, d in enumerate((-0.19, -0.12, -0.05, 0.0, 0.05, 0.12, 0.19)):
        s = serra(hz(nota) * 2 ** (d / 12) * vib, n, rng.uniform(0, 1))
        p = (k - 3) / 3
        l += s * (1 - p * 0.6)
        r += s * (1 + p * 0.6)
    e = adsr(n, 0.012, 0.2, 0.85, 0.22, dur)
    f = brilho * (0.6 + 0.4 * np.exp(-t / 0.3))
    x = np.stack([l, r], 1) * e[:, None] * 0.11 * forte
    y = np.zeros_like(x)
    for k in range(0, n, 512):
        y[k:k + 512] = lp(x[k:k + 512], float(f[k]))
    return y


def faisca(nota, forte=1.0):
    """Nota do arpejo: pluck quadrado curto e brilhante (as faíscas dos efeitos)."""
    n = n_(0.22)
    t = np.arange(n) / SR
    x = quadrada(np.full(n, hz(nota)), n) * 0.6 + serra(np.full(n, hz(nota) * 2.003), n) * 0.25
    corte = 1200 + 6500 * np.exp(-t / 0.05)
    y = np.zeros(n)
    for k in range(0, n, 256):
        y[k:k + 256] = lp(x[k:k + 256], float(corte[k]))
    return y * np.exp(-t / 0.09) * 0.6 * forte


def pad(notas, dur, forte=1.0, brilho=2200):
    n = n_(dur + 0.6)
    t = np.arange(n) / SR
    l = np.zeros(n)
    r = np.zeros(n)
    for m in notas:
        for d, lado in ((-0.1, 0.8), (0.1, -0.8), (0.0, 0.0)):
            s = serra(hz(m) * 2 ** (d / 12) * (1 + 0.002 * np.sin(2 * math.pi * 0.3 * t)), n, rng.uniform(0, 1))
            l += s * (1 + lado * 0.5)
            r += s * (1 - lado * 0.5)
    e = adsr(n, 0.35, 0.5, 0.85, 0.6, dur)
    return lp(np.stack([l, r], 1), brilho) * e[:, None] * 0.05 * forte


def sino(nota, forte=1.0):
    """Pluck de sino eletrônico (FM) para a Ponte."""
    n = n_(1.2)
    t = np.arange(n) / SR
    f = hz(nota)
    mod = np.sin(2 * math.pi * f * 3.5 * t) * 2.2 * np.exp(-t / 0.15)
    return np.sin(2 * math.pi * f * t + mod) * np.exp(-t / 0.5) * 0.3 * forte


# ================================================================== harmonia e melodias
E2 = 40


def power(raiz):
    return [raiz, raiz + 7, raiz + 12]


ACORDES = {  # nome -> (raiz do baixo, notas do pad)
    "Em": (40, [52, 55, 59]), "C": (36, [48, 52, 55]), "D": (38, [50, 54, 57]), "B": (35, [47, 51, 54]),
    "G": (43, [55, 59, 62]), "Am": (45, [57, 60, 64]), "Bm": (35, [47, 50, 54]), "F": (41, [53, 57, 60]),
    "F#m": (42, [54, 57, 61]), "E": (40, [52, 56, 59]), "A": (45, [57, 61, 64]), "C#": (37, [49, 53, 56]),
}

PROG = (["Em"] * 4 + ["C", "C", "D", "B"]                                                   # Intro 0–7
        + ["Em", "C", "D", "B"] * 4                                                        # Encontro 8–23
        + ["Em", "G", "D", "C", "Am", "C", "B", "B"] * 2                                   # Choque 24–39
        + ["C", "Am", "Em", "D", "C", "Am", "B", "B"]                                      # Ponte 40–47
        + ["C", "D", "Em", "Em", "C", "D", "B", "B"]                                       # Clímax: hino 48–55
        + ["F#m", "D", "E", "C#"] * 4                                                      # Clímax: refrão um tom acima 56–71
        + ["Em", "F", "Em", "F", "Em", "F", "Em", "D"]                                      # Virada: riff frígio 72–79
        + ["B", "B", "B", "B"])                                                             # subida de volta 80–83
assert len(PROG) == BARS

SECOES = [("Intro", 0), ("Encontro", 8), ("Choque", 24), ("Ponte", 40), ("Clímax", 48), ("Virada", 72)]


def secao(b):
    atual = SECOES[0][0]
    for nome, ini in SECOES:
        if b >= ini:
            atual = nome
    return atual


# (início em tempos, duração em tempos, nota MIDI) — frases de 8 compassos
TEMA_A = [(0, 1, 71), (1, 1, 76), (2, .5, 78), (2.5, 1.5, 79),
          (4, .5, 79), (4.5, .5, 78), (5, 1, 76), (6, 1, 79), (7, 1, 76),
          (8, 1.5, 78), (9.5, .5, 81), (10, 1, 78), (11, 1, 74),
          (12, 2, 75), (14, 1, 78), (15, 1, 83),
          (16, 1.5, 83), (17.5, .5, 81), (18, 1, 79), (19, .5, 78), (19.5, .5, 79),
          (20, 2, 76), (22, 1, 79), (23, 1, 84),
          (24, 1, 83), (25, 1, 81), (26, 1, 78), (27, 1, 74),
          (28, 1, 75), (29, 1, 78), (30, 2, 83)]
TEMA_B = [(0, .5, 76), (.5, .5, 76), (1, .5, 79), (1.5, 1.5, 83), (3, .5, 81), (3.5, .5, 79),
          (4, 1, 83), (5, 1, 86), (6, 1, 83), (7, 1, 79),
          (8, 1.5, 81), (9.5, .5, 78), (10, 1, 81), (11, 1, 86),
          (12, 2, 88), (14, 1, 86), (15, 1, 84),
          (16, 1, 84), (17, .5, 83), (17.5, 1.5, 81), (19, 1, 76),
          (20, 1, 79), (21, 1, 81), (22, 1, 83), (23, 1, 84),
          (24, 2, 87), (26, 1, 78), (27, 1, 81),
          (28, 3, 83)]
HINO = [(0, 2, 79), (2, 1, 76), (3, 1, 79),
        (4, 2, 81), (6, 1, 78), (7, 1, 81),
        (8, 3, 83), (11, .5, 81), (11.5, .5, 79),
        (12, 1, 83), (13, 3, 88),
        (16, 1, 88), (17, 1, 86), (18, 1, 84), (19, 1, 83),
        (20, 1, 81), (21, 1, 83), (22, 1, 84), (23, 1, 86),
        (24, 3, 87), (27, 1, 83),
        (28, 2, 90), (30, 2, 87)]
# refrão final em fá# menor (F#m D E C#), o tema A reescrito um tom acima e mais aberto
REFRAO = [(0, 1, 73), (1, 1, 78), (2, .5, 80), (2.5, 1.5, 81),
          (4, .5, 81), (4.5, .5, 80), (5, 1, 78), (6, 1, 81), (7, 1, 78),
          (8, 1.5, 80), (9.5, .5, 83), (10, 1, 80), (11, 1, 76),
          (12, 2, 77), (14, 1, 80), (15, 1, 85),
          (16, 1.5, 85), (17.5, .5, 83), (18, 1, 81), (19, .5, 80), (19.5, .5, 81),
          (20, 2, 78), (22, 1, 81), (23, 1, 86),
          (24, 1, 85), (25, 1, 83), (26, 1, 80), (27, 1, 76),
          (28, 1, 77), (29, 1, 80), (30, 2, 85)]


def bar_t(b):
    return b * BAR


def toca_frase(alvo, frase, t0, transp=0, forte=1.0, brilho=5200, dobra=None):
    for ini, dur, m in frase:
        poe(alvo, supersaw(m + transp, dur * BEAT * 0.94, forte, brilho), t0 + ini * BEAT)
        if dobra is not None:
            poe(alvo, supersaw(m + transp + dobra, dur * BEAT * 0.94, forte * 0.45, brilho * 0.8, False), t0 + ini * BEAT)


# ================================================================== arranjo
def main():
    shape = (N + CAUDA, 2)
    base, pulso, tema = np.zeros(shape), np.zeros(shape), np.zeros(shape)
    base_sala, tema_eco, pulso_eco = np.zeros(shape), np.zeros(shape), np.zeros(shape)

    BUMBO, BUMBO_F = bumbo(0.8), bumbo(1.0)
    CAIXA, CAIXA_F, CAIXA_FANTASMA = caixa(1.0), caixa(1.2), caixa(0.3)
    CHIMBAL, CHIMBAL_F, CHIMBAL_ABERTO = chimbal(False, 0.7), chimbal(False, 1.0), chimbal(True)
    CONDUCAO, PRATO, IMPACTO = conducao(), prato(), impacto()

    def bat(lista, amostra, alvo, t0):
        for p in lista:
            poe(alvo, amostra, t0 + p * S16)

    for b in range(BARS):
        sec = secao(b)
        t0 = bar_t(b)
        local = b - dict(SECOES)[sec]
        raiz, notas_pad = ACORDES[PROG[b]]

        # ------------------------------------------------ arpejo de faíscas (pulso), com eco
        arpeja = (sec == "Intro") or (sec == "Encontro" and local >= 8) or sec in ("Choque", "Ponte") or (sec == "Clímax" and local >= 8)
        if arpeja:
            seq = [notas_pad[0] + 12, notas_pad[1] + 12, notas_pad[2] + 12, notas_pad[1] + 24,
                   notas_pad[2] + 12, notas_pad[0] + 24, notas_pad[1] + 12, notas_pad[2] + 12]
            for k in range(16):
                forte = 0.75 + 0.25 * (k % 4 == 0)
                if sec == "Intro":
                    forte *= 0.35 + 0.65 * (local / 7)
                poe(pulso_eco, pan(faisca(seq[k % 8], forte), 0.4 * (1 if k % 2 else -1)), t0 + k * S16)

        # ------------------------------------------------ pad
        if sec in ("Intro", "Ponte") or (sec == "Clímax" and local < 8):
            poe(base_sala, pad(notas_pad, BAR, 1.0 if sec != "Intro" else 0.6 + 0.4 * local / 7,
                               1400 + 300 * local if sec == "Intro" else 2600), t0)
        elif sec in ("Encontro", "Choque", "Clímax"):
            poe(base_sala, pad(notas_pad, BAR, 0.55, 3000), t0)

        # ------------------------------------------------ baixo
        if sec == "Intro":
            if local >= 4:
                for k in range(8):
                    poe(base, baixo(raiz, BEAT * 0.4, 0.5 + 0.12 * (local - 4)), t0 + k * BEAT / 2)
        elif sec == "Ponte":
            for k in (0, 6, 10):
                poe(base, baixo(raiz, BEAT * (1.4 if k == 0 else 0.9), 0.85), t0 + k * S16)
        elif sec == "Choque":
            # galope: colcheia + duas semicolcheias
            for beat in range(4):
                for p, d in ((0, 2), (2, 1), (3, 1)):
                    poe(base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 0.95), t0 + (beat * 4 + p) * S16)
        elif sec == "Virada" and b < 80:
            for pos, inter in ((0, 0), (3, 0), (6, 0), (8, 1), (11, 0), (14, 3)):
                poe(base, baixo(raiz + inter if PROG[b] == "Em" else raiz, S16 * 2, 1.05), t0 + pos * S16)
        elif sec == "Virada":
            for k in range(8 if b < 82 else 16):
                passo = BEAT / 2 if b < 82 else S16
                poe(base, baixo(raiz, passo * 0.8, 0.8 + 0.05 * (b - 80)), t0 + k * passo)
        else:
            for k in range(8):
                oit = 12 if k in (3, 7) else 0
                poe(base, baixo(raiz + oit, BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)

        # ------------------------------------------------ guitarras (pulso)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        if sec == "Encontro":
            for k in range(8):                                     # chug abafado em colcheias, acorde aberto no 1
                if k == 0:
                    poe(pulso, guitarra(pc, BEAT * 0.9, 0.95), t0)
                else:
                    poe(pulso, guitarra(pc, BEAT * 0.35, 0.8, abafada=True), t0 + k * BEAT / 2)
        elif sec == "Choque":
            for beat in range(4):
                for p, d in ((0, 2), (2, 1), (3, 1)):
                    aberto = beat == 0 and p == 0
                    poe(pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto),
                        t0 + (beat * 4 + p) * S16)
        elif sec == "Clímax":
            if local < 8:
                poe(pulso, guitarra(pc, BAR * 0.95, 1.0), t0)          # acordes abertos, largos
            else:
                for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                    poe(pulso, guitarra(pc, dur * S16 * 0.9, 1.0), t0 + pos * S16)
        elif sec == "Virada":
            if b < 80:
                riff = [(0, 2, 0), (3, 1, 0), (4, 2, 0), (6, 2, 1 if PROG[b] == "Em" else 0), (8, 3, 0), (11, 1, 0), (12, 2, 3), (14, 2, 0)]
                for pos, dur, inter in riff:
                    poe(pulso, guitarra(power(pc[0] + inter), dur * S16 * 0.85, 1.05, abafada=dur < 2), t0 + pos * S16)
            else:
                passo = BEAT if b < 82 else BEAT / 2
                for k in range(int(BAR / passo)):
                    poe(pulso, guitarra(pc, passo * 0.5, 0.7 + 0.1 * (b - 80), abafada=True), t0 + k * passo)
                if b == 83:
                    poe(pulso, guitarra(pc, BAR * 0.9, 1.0), t0 + BAR * 0.5)

        # ------------------------------------------------ bateria
        if sec == "Intro":
            if local >= 4:
                bat([0, 4, 8, 12], BUMBO, base, t0)
                bat(range(2, 16, 4), CHIMBAL, pulso, t0)
            if local == 6:
                poe(base, caixa_rolando(2, 0.15), t0)
                poe(base, riser(BAR * 2), t0)
        elif sec == "Encontro":
            bat([0, 7, 8, 10], BUMBO, base, t0)
            bat([4, 12], CAIXA, base_sala, t0)
            bat([15], CAIXA_FANTASMA, base, t0)
            bat(range(0, 16, 2), CHIMBAL_F, pulso, t0)
            bat(range(1, 16, 2), CHIMBAL, pulso, t0)
            if local == 0:
                poe(base, IMPACTO, t0)
                poe(pulso, PRATO, t0)
            if local == 8:
                poe(pulso, PRATO, t0)
            if local == 15:
                for k, m in enumerate((52, 52, 48, 48, 45, 45, 43, 43)):
                    poe(base, tom(m, 0.9), t0 + (8 + k) * S16)
        elif sec == "Choque":
            bat([0, 2, 3, 6, 8, 10, 11, 14], BUMBO_F, base, t0)
            bat([4, 12], CAIXA_F, base_sala, t0)
            for k in range(0, 16, 2):
                poe(pulso, CONDUCAO, t0 + k * S16)
            if local in (0, 8):
                poe(pulso, PRATO, t0)
                if local == 0:
                    poe(base, IMPACTO, t0, 0.9)
            if local in (7, 15):
                for k, m in enumerate((55, 52, 50, 48, 45, 43, 41, 40)):
                    poe(base, tom(m, 1.0), t0 + (8 + k) * S16)
        elif sec == "Ponte":
            bat([0, 11], BUMBO, base, t0)
            bat([8], CAIXA, base_sala, t0)                          # meio-tempo: respira
            bat(range(0, 16, 4), CHIMBAL, pulso, t0)
            if local == 0:
                poe(base, IMPACTO, t0, 0.7)
                poe(pulso, PRATO, t0, 0.7)
            if local == 6:
                poe(base, caixa_rolando(2, 0.2), t0)
                poe(base, riser(BAR * 2, 1.2), t0)
        elif sec == "Clímax":
            if local < 8:
                bat([0, 3, 6, 8, 11, 14], BUMBO_F, base, t0)
            else:
                bat(range(16), BUMBO, base, t0)                    # bumbo duplo em semicolcheias
            bat([4, 12], CAIXA_F, base_sala, t0)
            for k in range(0, 16, 2):
                poe(pulso, CONDUCAO if local >= 8 else CHIMBAL_ABERTO, t0 + k * S16)
            if local % 4 == 0:
                poe(pulso, PRATO, t0)
            if local in (0, 8):
                poe(base, IMPACTO, t0, 1.1)
            if local == 7:
                poe(base, riser(BAR, 1.2), t0)
                for k, m in enumerate((57, 55, 52, 50, 48, 45, 43, 42)):
                    poe(base, tom(m, 1.0), t0 + (8 + k) * S16)
            if local == 23:
                for k in range(8):
                    poe(base, tom(57 - 2 * k, 1.0), t0 + (8 + k) * S16)
        elif sec == "Virada":
            if b < 80:
                # paradas com o riff: bumbo junto da guitarra
                bat([0, 3, 4, 6, 8, 11, 12, 14], BUMBO_F, base, t0)
                bat([4, 12], CAIXA_F, base_sala, t0)
                bat(range(0, 16, 2), CHIMBAL_F, pulso, t0)
                if local in (0, 4):
                    poe(pulso, PRATO, t0)
                    if local == 0:
                        poe(base, IMPACTO, t0)
            else:
                q = b - 80
                bat([0, 8] if q < 2 else [0, 4, 8, 12], BUMBO_F, base, t0)
                if q == 0:
                    poe(base, caixa_rolando(4, 0.15), t0)
                    poe(base, riser(BAR * 4, 1.3), t0)

        # ------------------------------------------------ tema (lead supersaw, com eco)
        if sec == "Encontro" and local in (0, 8):
            toca_frase(tema_eco, TEMA_A, t0, forte=0.9 if local == 0 else 1.0, dobra=None if local == 0 else -12)
        if sec == "Choque" and local in (0, 8):
            toca_frase(tema_eco, TEMA_B, t0, forte=1.0, dobra=-12 if local == 8 else None)
        if sec == "Ponte":
            seq = [notas_pad[0] + 24, notas_pad[2] + 12, notas_pad[1] + 24, notas_pad[2] + 12]
            for k, m in enumerate(seq):
                poe(tema_eco, pan(sino(m, 0.9), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
            if local == 4:
                poe(tema_eco, supersaw(83, BAR * 1.9, 0.7, 3500), t0)
        if sec == "Clímax":
            if local == 0:
                toca_frase(tema_eco, HINO, t0, forte=1.1, brilho=6000, dobra=-12)
            if local in (8, 16):
                toca_frase(tema_eco, REFRAO, t0, forte=1.15, brilho=6500, dobra=-12 if local == 8 else -5)
        if sec == "Virada" and local == 4:
            # chamada do tema A no riff
            toca_frase(tema_eco, [(0, 1, 76), (1, 1, 77), (2, 2, 76), (4, 1, 79), (5, 1, 77), (6, 2, 76),
                                  (8, 1, 76), (9, 1, 77), (10, 2, 79), (12, 1, 81), (13, 1, 79), (14, 2, 77)], t0, forte=0.9)
        if sec == "Virada" and b >= 80:
            poe(tema_eco, supersaw(71, BAR * 0.95, 0.55 + 0.15 * (b - 80), 2500 + 1200 * (b - 80), False), t0)

    # ------------------------------------------------ efeitos, laço e mixagem
    tema = tema + eco(tema_eco, BEAT * 0.75, 0.28, 3)
    tema = tema + sala(tema_eco, 0.7, 0.18)
    pulso = pulso + eco(pulso_eco, BEAT * 0.75, 0.3, 3)
    base = base + sala(base_sala, 0.6, 0.22)
    pulso = sala(pulso, 0.4, 0.08)

    # equalização para alto-falante de celular: grave contido, médio presente
    def eq(x, corte_grave, presenca):
        x = hp(x, 35, 2)
        x = x - corte_grave * lp(x, 130, 2)
        return x + presenca * bp(x, 1300, 4500, 2)
    base = eq(base, 0.45, 0.2)
    pulso = eq(pulso, 0.6, 0.25)
    tema = eq(tema, 0.2, 0.3)

    ini_laco = int(round(LACO * BAR * SR))

    def fecha(x):
        y = x[:N].copy()
        y[ini_laco:ini_laco + CAUDA] += x[N:N + CAUDA]
        return y

    camadas = {"musica-base": fecha(base), "musica-pulso": fecha(pulso), "musica-tema": fecha(tema)}
    # equilíbrio entre camadas: a base é a mais presente; pulso e tema por baixo dela
    alvo_db = {"musica-base": -19.5, "musica-pulso": -23.0, "musica-tema": -21.5}
    for k, x in camadas.items():
        rms = 20 * math.log10(float(np.sqrt(np.mean(x ** 2))) + 1e-12)
        camadas[k] = x * 10 ** ((alvo_db[k] - rms) / 20)
    if os.environ.get("SAIDA_MUSICA"):
        np.save(OUT / "_mix.npy", sum(camadas.values()).astype(np.float32))
    soma = sum(camadas.values())
    ganho = min(1.0, 0.89 / np.max(np.abs(soma)))
    info = {}
    OUT.mkdir(parents=True, exist_ok=True)
    for nome, x in camadas.items():
        x = x * ganho
        y = x.astype(np.float32)
        destino = OUT / f"{nome}.ogg"
        with sf.SoundFile(destino, "w", SR, 2, format="OGG", subtype="VORBIS", compression_level=0.92) as arq:
            for i in range(0, len(y), SR):
                arq.write(y[i:i + SR])
        escreve_mp3(OUT / f"{nome}.mp3", y, SR)
        rms = 20 * math.log10(float(np.sqrt(np.mean(x ** 2))) + 1e-9)
        info[nome] = {"arquivo": destino.name, "mp3": f"{nome}.mp3", "segundos": round(N / SR, 3), "bytes": destino.stat().st_size, "rmsDb": round(rms, 1)}
        print(f"{nome:14s} {destino.stat().st_size / 1024:7.1f} KB  rms {rms:6.1f} dB")
    secoes = [{"nome": s, "inicio": round(i * BAR, 3)} for s, i in SECOES]
    (OUT / "musica.json").write_text(json.dumps({
        "bpm": BPM, "compassos": BARS, "segundos": round(N / SR, 3), "secoes": secoes, "estilo": "anime arcade (v4)",
        "laco": {"inicio": round(LACO * BAR, 3), "fim": round(N / SR, 3)}, "camadas": info,
    }, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
