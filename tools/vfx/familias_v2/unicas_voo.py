"""Mecânicas únicas que viajam até o alvo, como as habilidades: o que voa e o que se forma antes de sair.

- genki_dama_reune: a Genki Dama se formando em cima do Goku — a energia vem de todos os lados e a esfera cresce;
- genki_dama_voo: a Genki Dama voando até o alvo — esfera enorme, núcleo branco, contorno que pulsa e faíscas em volta.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, vazio


def genki_dama_reune(T, t, rng):
    """A esfera de energia em cima da cabeça, crescendo; fios de energia vêm de fora e entram nela (laço)."""
    G, H = vazio(T)
    cy = -0.42
    r = 0.24 + 0.03 * math.sin(TAU * t)
    d = np.sqrt(T.U ** 2 + (T.V - cy) ** 2)
    esfera = np.exp(-(d / r) ** 4)
    borda = T.ring(r, 0.035, 0.0, cy)
    nucleo = T.gauss(0.0, cy, r * 0.45)
    redemoinho = T.noise(np.random.default_rng(11), 0.05, 3)
    gira = np.clip(0.5 + 0.6 * np.roll(redemoinho, int(t * T.W) % T.W, axis=1), 0, 1)
    fios = T.zero()
    for k in range(14):
        a = TAU * k / 14 + 0.3 * math.sin(k * 1.7)
        fase = (t + k / 14) % 1
        dist = 1.0 - 0.75 * fase
        x, y = dist * math.cos(a), cy + dist * math.sin(a) * 0.9
        x2, y2 = (dist + 0.16) * math.cos(a), cy + (dist + 0.16) * math.sin(a) * 0.9
        fios += T.lines([(x2, y2, x, y, 1.0)], 0.012, 0.004) * (1 - fase) ** 0.5
    G += esfera * 0.9 + borda * 1.2 + esfera * gira * 0.5 + fios * 1.3
    H += nucleo * 1.4 + borda * 0.5 + fios * 0.6
    return G, H


def genki_dama_voo(T, t, rng):
    """A Genki Dama em viagem (+x): esfera grande, núcleo branco, contorno pulsando e faíscas orbitando (laço)."""
    G, H = vazio(T)
    r = 0.56 + 0.025 * math.sin(TAU * 2 * t)
    d = np.sqrt(T.U ** 2 + T.V ** 2)
    esfera = np.exp(-(d / r) ** 5)
    borda = T.ring(r * 0.98, 0.05)
    nucleo = T.gauss(0.05, 0.0, r * 0.42)
    mar = T.noise(np.random.default_rng(5), 0.07, 3)
    mar = np.clip(0.5 + 0.6 * np.roll(mar, int(t * T.W) % T.W, axis=0), 0, 1)
    rastro = np.exp(-((T.V) / (0.32 * np.clip(-T.U, 0, 1) + 0.12)) ** 2) * np.clip(-T.U - r * 0.6, 0, 0.4) * 1.6
    faiscas = []
    for k in range(10):
        a = TAU * (k / 10 + t * (0.5 + 0.1 * (k % 3)))
        rr = r * (1.08 + 0.08 * math.sin(k * 2.1 + TAU * t))
        faiscas.append((rr * math.cos(a), rr * math.sin(a), 1.0))
    brilhos = T.splats(faiscas, 0.03)
    G += esfera * 0.75 + esfera * mar * 0.6 + borda * 1.1 + rastro * 0.9 + brilhos * 1.4
    H += nucleo * 1.6 + borda * 0.4 + brilhos * 0.8
    return G, H


REGISTRO = [
    ("genki_dama_reune", genki_dama_reune, GRANDE, "Goku · a Genki Dama se formando em cima dele (laço)", True),
    ("genki_dama_voo", genki_dama_voo, MEDIA, "Goku · a Genki Dama voando até o alvo (laço)", True),
]
