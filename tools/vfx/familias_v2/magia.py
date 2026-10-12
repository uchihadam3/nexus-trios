"""Magia e mente: olho, hipnose, tempo, runas, ilusão, portais, sorte, invocação, lua vermelha."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, estrela, faiscas, girado, jagged, janela,
                   lamina, poeira, pulso, rel, smooth, some, vazio)


def olho(T, t, rng):
    """Olho: um olho gigante se abre sobre o alvo, a íris gira e fixa, e fecha num piscar."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.25), 2) * (1 - ease_in(rel(t, 0.75, 0.9), 2))
    h = 0.32 * abre + 0.005
    w = 0.7
    # pálpebras: duas parábolas
    cima = -h * (1 - (T.U / w) ** 2)
    baixo = h * (1 - (T.U / w) ** 2)
    dentro = smooth(T.V - cima, 0, 0.02) * smooth(baixo - T.V, 0, 0.02) * (np.abs(T.U) < w)
    borda = (np.exp(-((T.V - cima) / 0.015) ** 2) + np.exp(-((T.V - baixo) / 0.015) ** 2)) * (np.abs(T.U) < w) * smooth(w - np.abs(T.U), 0, 0.1)
    iris = (T.ring(0.2, 0.025) + T.ring(0.12, 0.012)) * dentro
    marcas = (np.abs(np.cos(3 * (T.ANG - t * 6))) ** 12) * smooth(T.RAD, 0.11, 0.13) * smooth(0.19 - T.RAD, 0, 0.02) * dentro
    pupila = T.gauss(0, 0, 0.05) * dentro * 1.5
    raios = (np.abs(np.cos(T.ANG * 10)) ** 20) * smooth(T.RAD, 0.35, 0.5) * np.exp(-T.RAD * 2) * abre * 0.8
    G += dentro * 0.25 + borda * 1.5 + iris * 1.4 + marcas * 1.2 + pupila + raios
    H += borda * 0.8 + iris * 0.7 + pupila
    return G, H


def hipnose(T, t, rng):
    """Hipnose: espiral girando no alvo, anéis pulsando para dentro, estrelas tontas."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.7, 1)
    esp = (0.5 + 0.5 * np.cos(T.ANG - T.RAD * 18 + t * 18)) ** 6 * smooth(0.7 - T.RAD, 0, 0.15) * smooth(T.RAD, 0.03, 0.08)
    aneis = sum(T.ring(0.7 * (1 - ((t * 1.5 + k / 3) % 1)), 0.015) * math.sin(math.pi * ((t * 1.5 + k / 3) % 1)) for k in range(3))
    G += (esp * 1.4 + aneis * 0.9) * env
    H += esp * 0.6 * env
    return G, H


def runas(T, t, rng):
    """Runas: um círculo de símbolos se acende em volta do alvo e as runas sobem uma a uma."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    sq = 0.35
    aro = (T.ring(0.65, 0.012, cy=0.35, squash=1 / sq) + T.ring(0.55, 0.008, cy=0.35, squash=1 / sq)) * janela(t, 0, 0.2) * 1.3
    sub = np.random.default_rng(601)
    simb = T.zero()
    for k in range(8):
        a = TAU * k / 8 + t * 0.6
        x, y = math.cos(a) * 0.6, 0.35 + math.sin(a) * 0.6 * sq
        sobe = ease_out(rel(t, 0.15 + k * 0.05, 0.6 + k * 0.05), 2) * 0.55
        y -= sobe
        segs = []
        for _ in range(3):
            x1, y1 = x + sub.uniform(-0.05, 0.05), y + sub.uniform(-0.06, 0.06)
            segs.append((x1, y1, x1 + sub.uniform(-0.05, 0.05), y1 + sub.uniform(-0.06, 0.06), 1))
        simb += T.lines(segs, 0.011, 0.002) * janela(t, 0.1 + k * 0.04, 0.2 + k * 0.04)
    G += (aro + T.glow(simb, 1.4, 1.2, 0.02)) * env
    H += (aro * 0.4 + simb) * env
    return G, H


def sarcofago(T, t, rng):
    """Sarcófago: uma caixa escura se fecha em volta do alvo, as faces se encaixam e ela racha em luz."""
    G, H = vazio(T)
    fecha = ease_out(rel(t, 0, 0.3), 2.5)
    env = apaga(t, 0.8, 1)
    w, h = 0.3, 0.55
    d = (1 - fecha) * 0.6
    faces = []
    faces.append(([(-w - d, -h), (-w * 0.2 - d, -h), (-w * 0.2 - d, h), (-w - d, h)], 1))
    faces.append(([(w * 0.2 + d, -h), (w + d, -h), (w + d, h), (w * 0.2 + d, h)], 1))
    faces.append(([(-w * 0.2, -h - d), (w * 0.2, -h - d), (w * 0.2, -h * 0.3 - d), (-w * 0.2, -h * 0.3 - d)], 1))
    f = T.polys(faces, 0.004)
    contorno = f * (1 - smooth(T.blur(f, 0.02), 0.8, 0.97))
    sub = np.random.default_rng(611)
    rach = sum(T.polyline(jagged(sub, sub.uniform(-0.2, 0.2), -h, sub.uniform(-0.2, 0.2), h, 4, 0.2), 0.012, 1) for _ in range(3)) * janela(t, 0.45, 0.55)
    luz = T.gauss(0, 0, 0.22, 0.4) * pulso(t, 0.6, 0.85) * 1.6
    G += (f * 0.35 + contorno * 1.4 + T.glow(rach, 1.4, 1.4, 0.02)) * env + luz
    H += (contorno * 0.5 + rach * 1.2) * env + luz * 0.8
    return G, H


def caveira(T, t, rng):
    """Caveira: uma caveira de luz surge sobre o alvo, abre a boca e se desfaz em fumaça."""
    G, H = vazio(T)
    s = 0.5 + 0.5 * back(rel(t, 0, 0.3), 1.4)
    env = apaga(t, 0.6, 1)
    u, v = T.U / s, T.V / s
    cranio = smooth(1 - ((u / 0.42) ** 2 + ((v + 0.1) / 0.38) ** 2), 0, 0.1)
    mand = smooth(1 - ((u / 0.25) ** 2 + ((v - 0.28 - 0.06 * pulso(t, 0.3, 0.6)) / 0.13) ** 2), 0, 0.15)
    olhos = smooth(1 - (((np.abs(u) - 0.16) / 0.1) ** 2 + ((v + 0.05) / 0.11) ** 2), 0, 0.15)
    nariz = smooth(1 - ((u / 0.04) ** 2 + ((v - 0.12) / 0.06) ** 2), 0, 0.2)
    corpo = np.clip(cranio + mand - olhos - nariz, 0, 1)
    borda = corpo * (1 - smooth(T.blur(corpo, 0.02), 0.75, 0.95))
    fumo = _subindo(T, 621, t, 0.06, 1)
    some_ = rel(t, 0.55, 1)
    desfaz = corpo * np.clip(1 - some_ * 1.5 + 0.4 * fumo, 0, 1)
    G += (desfaz * 0.6 + borda * 1.4 * (1 - some_)) * env + T.gauss(0, 0, 0.3) * pulso(t, 0.25, 0.6) * 0.4
    H += (borda * 0.6 * (1 - some_)) * env
    return G, H


def sorte(T, t, rng):
    """Sorte: dois dados rolam e quicam, trevos e estrelinhas pulam quando param."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    dados, pontos = [], T.zero()
    for k, x0 in enumerate((-0.25, 0.22)):
        u = rel(t, 0, 0.5)
        x = x0 - 0.5 * (1 - u)
        y = 0.2 - abs(math.sin(u * math.pi * 3)) * 0.35 * (1 - u)
        a = (1 - ease_out(u, 2)) * 8 + k
        s = 0.16
        c, sn = math.cos(a), math.sin(a)
        dados.append(([(x + c * px - sn * py, y + sn * px + c * py) for px, py in ((-s, -s), (s, -s), (s, s), (-s, s))], 1))
        for px, py in ((0, 0), (-0.08, -0.08), (0.08, 0.08))[: 2 + k]:
            pontos += T.gauss(x + c * px - sn * py, y + sn * px + c * py, 0.022)
    d = T.polys(dados, 0.003)
    contorno = d * (1 - smooth(T.blur(d, 0.012), 0.8, 0.97))
    pula = []
    for _ in range(14):
        a = rng.uniform(-math.pi, 0)
        u = rel(t, 0.5, 1)
        pula.append((math.cos(a) * 0.6 * u, 0.1 + math.sin(a) * 0.5 * u + 0.4 * u * u, (1 - u) * (t > 0.5)))
    G += (d * 0.4 + contorno * 1.4 + T.splats(pula, 0.02) * 1.2) * env
    H += (contorno * 0.5 + pontos * 0.5) * env
    G -= pontos * 0.3 * env
    return G, H


def invocacao(T, t, rng):
    """Invocação: um círculo se abre no chão e uma silhueta de luz sobe dele, com faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    abre = ease_out(rel(t, 0, 0.25), 2)
    circ = (T.ring(0.6 * abre, 0.016, cy=0.45, squash=3.5) + T.ring(0.48 * abre, 0.01, cy=0.45, squash=3.5)) * 1.4
    sobe = ease_out(rel(t, 0.2, 0.6), 2)
    y0 = 0.45 - 0.65 * sobe
    sil = smooth(T.gauss(0, y0 - 0.22, 0.09) + T.gauss(0, y0 + 0.08, 0.15, 0.22), 0.45, 0.6) * smooth(0.45 - T.V, 0, 0.05)
    contorno = sil * (1 - smooth(T.blur(sil, 0.015), 0.8, 0.97))
    coluna = np.exp(-(T.U / 0.3) ** 2) * smooth(0.45 - T.V, 0, 0.05) * smooth(T.V + 0.6, 0, 0.4) * pulso(t, 0.15, 0.7) * 0.6
    fa = faiscas(T, rng, t, 18, 0.6, 0.025, cone=(-math.pi + 0.4, -0.4), cy=0.45, inicio=0.2)
    G += (circ + sil * 0.4 + contorno * 1.5 + coluna + fa) * env
    H += (circ * 0.4 + contorno * 0.8) * env
    return G, H


REGISTRO = [
    ("olho", olho, GRANDE, "olho gigante se abrindo", False),
    ("runas", runas, GRANDE, "círculo de runas", False),
    ("sarcofago", sarcofago, GRANDE, "caixa negra fechando", False),
    ("invocacao", invocacao, GRANDE, "silhueta invocada", False),
]
