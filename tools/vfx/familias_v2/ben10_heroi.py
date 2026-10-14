"""Ben 10 sem os nomes dos aliens nas habilidades (pedido do jogador: "ele transforma no fogo e usa Quatro Braços…
fica meio tosco"). As três habilidades agora são do próprio Omnitrix, com a ampulheta verde no centro de cada uma:

- pulso_do_omnitrix: a ampulheta acende no alvo, o pulso verde abre em ondas e três anéis de energia fecham em volta
  dele como algemas (Preso).
- sobrecarga_do_omnitrix: o relógio superaquece piscando, os raios verdes estalam e ele explode em labaredas verdes
  sobre os três rivais (Queimando, e o relógio recarrega).
- hora_do_heroi: "É hora do herói!": a ampulheta cresce enorme, o clarão verde, o rastro de energia cruzando a tela e o
  impacto com as faíscas (Fortalecido).
"""
from __future__ import annotations

import math

from .base import GRANDE, apaga, ease_in, ease_out, pulso, rel, vazio
from .unicas_kit import AMPULHETA, CHAMA, anel, cheio, clarao, converge, estouro, icone, poe, raios, surge


def _relogio(T, t, a, b, cx, cy, s, k=1.0):
    """A ampulheta do Omnitrix dentro do aro do relógio, acesa."""
    g, h = icone(T, poe(AMPULHETA, cx, cy, s * 0.62), k * 1.3, 0.55)
    G = g + T.ring(s, s * 0.14, cx, cy) * k * 1.1
    return G, h * 1.4 + T.gauss(cx, cy, s * 0.5) * 0.5 * k


def pulso_do_omnitrix(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = surge(t, 0.0, 0.22) * (1 - rel(t, 0.55, 0.7))
    if k > 0:
        g, h = _relogio(T, t, 0.0, 0.7, 0.0, 0.0, 0.2 * k, k)
        G, H = G + g, H + h
    for j in range(3):
        G = G + anel(T, t, 0.18 + 0.08 * j, 0.6 + 0.08 * j, 0.1, 0.85, 0.04, 0.0, 1.0, 1.4)
    # as algemas: três anéis que vêm de fora e fecham no alvo, ficam presos e piscam
    for j, sq in enumerate((1.0, 2.6, 2.6)):
        u = rel(t, 0.42 + 0.05 * j, 0.62 + 0.05 * j)
        if u <= 0:
            continue
        r = 0.7 - 0.42 * ease_out(min(u, 1.0), 2.4)
        brilho = (1 - rel(t, 0.82, 0.97)) * (0.9 + 0.3 * math.sin(t * 40 + j))
        if j == 0:
            G = G + T.ring(r, 0.035, 0.0, 0.0) * brilho * 1.3
        else:
            G = G + T.ring(r * 1.25, 0.022, 0.0, -0.16 + 0.32 * (j - 1), sq) * brilho * 1.4
    g, h = clarao(T, t, 0.6, 0.78, 0.0, 0.0, 0.7)
    G, H = G + g, H + h
    G = G + estouro(T, t, 0.6, 0.9, 12, 3, 0.0, 0.0, 0.5, 0.012)
    return G * env, H * env


def sobrecarga_do_omnitrix(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # o relógio piscando, cada vez mais rápido, e os raios estalando
    k = rel(t, 0.0, 0.1) * (1 - rel(t, 0.4, 0.46))
    if k > 0:
        pisca = 0.6 + 0.4 * math.sin(t * (30 + 120 * t))
        g, h = _relogio(T, t, 0.0, 0.46, 0.0, -0.05, 0.18, k * pisca)
        G, H = G + g, H + h
        G = G + raios(T, t, 0.05, 0.42, 4, 11, 0.0, -0.05, 0.38, 0.009)
        G = G + converge(T, t, 0.0, 0.4, 10, 5, 0.0, -0.05, 0.6, 0.01)
    g, h = clarao(T, t, 0.38, 0.55, 0.0, -0.05, 1.0, 1.2)
    G, H = G + g, H + h
    # as labaredas verdes caem em cada rival
    for j, (x, y) in enumerate(((-0.55, 0.12), (0.0, -0.12), (0.55, 0.12))):
        u = rel(t, 0.42 + 0.05 * j, 0.62 + 0.05 * j)
        if 0 < u < 1:
            px, py = x * ease_out(u, 2), -0.05 + (y + 0.05) * u - 0.25 * math.sin(math.pi * u)
            g, h = icone(T, poe(CHAMA, px, py, 0.22, math.pi / 2 + math.atan2(y, x + 1e-6) * 0.3), 1.3, 0.6)
            G, H = G + g, H + h * 1.4
        kk = pulso(t, 0.6 + 0.05 * j, 0.98)
        if kk > 0:
            for m in range(3):
                g, h = icone(T, poe(CHAMA, x - 0.15 + 0.15 * m, y - 0.05 * (m == 1), 0.15 * kk * (1.3 if m == 1 else 1)), kk * 1.2, 0.6)
                G, H = G + g, H + h
        g, h = clarao(T, t, 0.6 + 0.05 * j, 0.74 + 0.05 * j, x, y, 0.45)
        G, H = G + g, H + h
    return G * env, H * env


def hora_do_heroi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    # a ampulheta cresce enorme no centro e some num clarão
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.38))
    if k > 0:
        g, h = _relogio(T, t, 0.0, 0.38, -0.45, 0.0, 0.32 * k, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.42, -0.45, 0.0, 0.9)
    G, H = G + g, H + h
    G = G + anel(T, t, 0.28, 0.55, 0.15, 0.7, 0.04, 0.0, 1.0, 1.2)
    # o rastro verde cruzando até o alvo
    u = rel(t, 0.34, 0.5)
    if u > 0:
        fim = -0.45 + 1.0 * ease_in(min(u, 1.0), 1.4)
        some = 1 - rel(t, 0.55, 0.75)
        for d, w in ((0.0, 0.07), (-0.08, 0.025), (0.08, 0.025)):
            G = G + T.tapered([(-0.95, d * 1.5, fim, d * 0.3, 1.0)], w) * some * 1.2
        H = H + T.lines([(-0.9, 0.0, fim, 0.0, 1.0)], 0.012) * some
    g, h = clarao(T, t, 0.48, 0.68, 0.55, 0.0, 1.1, 1.2)
    G, H = G + g, H + h
    G = G + estouro(T, t, 0.48, 0.85, 16, 7, 0.55, 0.0, 0.55, 0.014)
    ua = rel(t, 0.48, 0.8)
    if 0 < ua < 1:
        G = G + T.ring(0.05 + 0.4 * ease_out(ua, 2.2), 0.035 * (1 - 0.5 * ua), 0.55, 0.0) * (1 - ua) * 1.3
    return G * env, H * env


REGISTRO = [
    ("pulso_do_omnitrix", pulso_do_omnitrix, GRANDE, "Ben 10 · o pulso verde do Omnitrix e as algemas de energia", False),
    ("sobrecarga_do_omnitrix", sobrecarga_do_omnitrix, GRANDE, "Ben 10 · o Omnitrix superaquece e explode em fogo verde", False),
    ("hora_do_heroi", hora_do_heroi, GRANDE, "Ben 10 · É hora do herói: a ampulheta, o rastro verde e o impacto", False),
]
