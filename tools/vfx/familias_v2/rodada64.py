"""Rodada 64 das habilidades próprias: as duas que ainda usavam uma família genérica.

- getsuga_tensho_ichigo: a Zangetsu erguida e a lua crescente de energia preta com a borda vermelha voando até o rival
  (antes era o corte de energia genérico).
- gancho_de_garra_mabel: a pistola de gancho da Mabel, a garra voando presa na corda e puxando o rival (Preso)
  (antes era o soco gancho, que não tem nada a ver com o gancho de escalada).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .unicas_kit import (anel, clarao, estouro, icone, particulas, poe, surge)


def _zangetsu(T, x, y, ang, s, k):
    """A Zangetsu: a lâmina larga, sem guarda, com a faixa no cabo."""
    c, sn = math.cos(ang), math.sin(ang)
    px, py = -sn, c
    pts = [(x + px * s * 0.12, y + py * s * 0.12), (x + c * s * 0.9 + px * s * 0.12, y + sn * s * 0.9 + py * s * 0.12),
           (x + c * s, y + sn * s), (x + c * s * 0.85 - px * s * 0.1, y + sn * s * 0.85 - py * s * 0.1), (x - px * s * 0.1, y - py * s * 0.1)]
    g, h = icone(T, pts, k * 1.2, 0.65)
    G = g + T.lines([(x, y, x - c * s * 0.25, y - sn * s * 0.25, 1.0)], s * 0.06) * k
    G += T.polyline([(x - c * s * 0.25, y - sn * s * 0.25), (x - c * s * 0.35 + px * s * 0.1, y - sn * s * 0.35 + py * s * 0.1),
                     (x - c * s * 0.5 - px * s * 0.05, y - sn * s * 0.5 - py * s * 0.05)], s * 0.025) * k
    return G, h


def _crescente(T, x, y, r, w, k):
    """A lua crescente da Getsuga: o miolo escuro (forte) e a borda vermelha brilhando."""
    G = T.arc_band(r, w, -1.4, 1.4, 1.0, 0, x, y, 1.0, True) * k * 1.4
    H = T.arc_band(r * 1.05, w * 0.3, -1.35, 1.35, 1.0, 0, x, y, 1.0, True) * k * 1.4
    return G, H


def _garra(T, x, y, s, ang, abre, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.ring(s * 0.25, s * 0.08, x, y) * k * 1.2
    segs = []
    for lado in (-1, 0, 1):
        a = ang + lado * (0.5 + 0.4 * abre)
        mx, my = x + s * 0.55 * math.cos(a), y + s * 0.55 * math.sin(a)
        b = a - lado * 1.2 if lado else a
        segs += [(x, y, mx, my, 1.0), (mx, my, mx + s * 0.3 * math.cos(b - lado * 0.8), my + s * 0.3 * math.sin(b - lado * 0.8), 1.0)]
    return G + T.lines(segs, s * 0.1) * k * 1.2


def _pistola_gancho(T, x, y, s, k):
    pts = [(-0.6, -0.18), (0.5, -0.18), (0.6, -0.05), (0.5, 0.08), (0.0, 0.08), (-0.1, 0.55), (-0.4, 0.55), (-0.3, 0.08), (-0.6, 0.08)]
    return icone(T, poe(pts, x, y, s), k * 1.2, 0.6)


def getsuga_tensho_ichigo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    # a aura escura subindo e a espada erguida
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.45, 0.58))
    G += T.gauss(-0.55, -0.1, 0.2, 0.35) * pulso(t, 0.0, 0.45) * 0.6
    if k > 0:
        ang = -1.9 + 1.8 * ease_in(rel(t, 0.15, 0.3), 2.2)
        g, h = _zangetsu(T, -0.55, 0.15, ang, 0.6, k)
        G, H = G + g, H + h
    # a lua crescente voando
    u = rel(t, 0.28, 0.6)
    if 0 < u < 1:
        x = -0.4 + 0.85 * ease_out(u, 1.4)
        r = 0.3 + 0.12 * u
        g, h = _crescente(T, x, -0.05, r, 0.07, 1 - rel(u, 0.85, 1))
        G, H = G + g, H + h
        for j in range(4):
            G += T.tapered([(x - r - 0.35, -0.05 + 0.15 * (j - 1.5), x - r * 0.5, -0.05 + 0.18 * (j - 1.5), 0.7)], 0.015)
    g, h = clarao(T, t, 0.52, 0.75, 0.45, -0.05, 1.7, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.55, 0.9, 0.05, 0.7, 0.05, -0.05, 1.0, 1.4)
    G += estouro(T, t, 0.55, 0.9, 16, 780, 0.45, -0.05, 0.6, 0.014)
    G += particulas(T, t, 0.0, 0.5, 14, 781, -0.55, 0.1, 0.25, 0.7, 0.012)
    return G * env, H * env


def gancho_de_garra_mabel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        g, h = _pistola_gancho(T, -0.65, 0.0, 0.45, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.12, 0.25, -0.45, -0.05, 0.6, 1.0)
    G, H = G + g, H + h
    voa = ease_out(rel(t, 0.12, 0.38), 1.6)
    puxa = ease_in(rel(t, 0.55, 0.8), 2)
    if voa > 0 and k > 0:
        x = -0.45 + 0.9 * voa - 0.25 * puxa
        y = -0.05 - 0.06 * math.sin(math.pi * voa) * (1 - puxa)
        G += _garra(T, x, y, 0.2, 0.0, 1 - rel(t, 0.36, 0.45), k)
        # a corda: ondula enquanto voa e estica quando prende
        bamba = (1 - rel(t, 0.38, 0.5)) * 0.04
        pts = [(-0.45 + (x + 0.45) * v, -0.05 + (y + 0.05) * v + bamba * math.sin(v * 12 + t * 30)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.008) * k * 1.2
    m = surge(t, 0.4, 0.55) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(2):
            G += T.ring(0.14, 0.012, 0.45 - 0.25 * puxa, -0.15 + 0.15 * j, 3.0) * m * 1.2
    g, h = clarao(T, t, 0.36, 0.5, 0.45, -0.05, 0.9, 1.0)
    G, H = G + g, H + h
    # o brilho e as estrelinhas da Mabel
    for j in range(5):
        r = (t * 1.5 + j / 5) % 1
        H += T.gauss(-0.1 + 0.12 * j, -0.3 - 0.2 * r, 0.012) * math.sin(math.pi * r) * pulso(t, 0.3, 1.0) * 1.6
    return G * env, H * env


REGISTRO = [
    ("getsuga_tensho_ichigo", getsuga_tensho_ichigo, GRANDE, "Ichigo · a Zangetsu e a lua crescente", False),
    ("gancho_de_garra_mabel", gancho_de_garra_mabel, GRANDE, "Mabel · a pistola de gancho e a corda", False),
]
