"""Os sons do Hulk (veja tools/vfx/familias_v2/hulk.py): o soco, o Esmagar, o rugido e a fúria."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _whoosh, _z
from som import SR, baque, env, estalo, graos, n_de, passa, poe, reverb, rosa, ruido, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _urro(rng, seg, f0=95.0, f1=70.0, g=1.0, aspero=0.6):
    """O urro do Hulk: uma voz grave e rasgada (dente-de-serra com o tom caindo e tremendo), com os
    formantes de um "RRAAH" e o chiado da garganta."""
    n = n_de(seg)
    t = _t(n)
    f = varre(f0, f1, n, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * 7 * t) + 0.02 * passa(ruido(rng, n), None, 30, 1) / 0.05)
    voz = serra_suave(f, n, 24)
    # formantes de "a" aberto (~700 e ~1200 Hz) e o grave do peito
    a = passa(voz, 550, 900, 2) * 1.2 + passa(voz, 1000, 1500, 2) * 0.7 + passa(voz, 60, 300, 2) * 0.9
    rasgo = passa(ruido(rng, n), 300, 2500, 2) * aspero * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * f * t * 0.5)))
    return satura((a + rasgo * 0.4) * sobe_e_some(n, 0.25, 1.3), 2.2) * g


def soco_do_hulk(rng, v):
    """O soco do Hulk: o vento pesado do braço, o impacto grave e seco, o estalo e a poeira."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.2, 150, 700, 0.8, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.14)
    poe(x, baque(n_de(0.6), 75, 32, 0.22, 0.9) * 1.1, 0.14)
    poe(x, estalo(rng, n_de(0.06), 1200, 5000, 0.015) * 0.7, 0.14)
    poe(x, graos(rng, n_de(0.5), 10, 0.0, 0.45, 300, 2500, 0.01, 0.6) * 0.3, 0.2)
    return reverb(x, 0.4, 0.18, 5000)


def hulk_esmaga(rng, v):
    """Esmagar: um "HRRA" curto, o vento dos punhos descendo, o estrondo no chão (grave e longo), as
    rachaduras, as pedras caindo e o zumbido de quem ficou tonto."""
    x = _z(2.2)
    poe(x, _urro(rng, 0.35, 120, 90, 0.5), 0.0)
    poe(x, _whoosh(rng, 0.25, 200, 1200, 0.9, g=0.7), 0.05)
    poe(x, B.terremoto(rng, v) * 0.9, 0.24)
    poe(x, baque(n_de(1.0), 55, 22, 0.45, 1.0) * 1.4, 0.24)
    poe(x, B.soco_pesado(rng, v) * 0.9, 0.24)
    poe(x, graos(rng, n_de(0.6), 30, 0.0, 0.5, 400, 4000, 0.008, 0.7) * 0.5, 0.26)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 300, 2500, 0.02) * 0.35, 0.7 + 0.1 * k + rng.uniform(-0.03, 0.03))
    m = n_de(0.8)
    tonto = (seno(1300 + 120 * np.sin(2 * math.pi * 6 * _t(m)), m) * 0.06 + seno(1900, m) * 0.03) * env(m, 0.05, 0.5)
    poe(x, tonto, 1.1)
    return reverb(x, 0.6, 0.25, 4500)


def rugido_do_hulk(rng, v):
    """O Rugido: o urro longo e grave do Hulk, com o eco e o tremor do chão por baixo."""
    x = _z(2.0)
    u = _urro(rng, 1.3, 100, 68, 1.0, 0.75)
    poe(x, u, 0.0)
    n = n_de(1.3)
    poe(x, passa(rosa(rng, n), 25, 120, 2) * sobe_e_some(n, 0.3, 1.3) * 0.7, 0.05)
    return reverb(x, 0.7, 0.35, 4000)


def furia_hulk(rng, v):
    """A fúria crescendo: a respiração pesada, o ronco subindo e o estalo dos músculos."""
    x = _z(1.6)
    for k in range(2):
        m = n_de(0.35)
        poe(x, passa(ruido(rng, m), 250, 1800, 2) * sobe_e_some(m, 0.5, 1.4) * 0.35, 0.05 + 0.35 * k)
    poe(x, _urro(rng, 0.8, 70, 110, 0.7, 0.5), 0.7)
    poe(x, B.transformacao(rng, v) * 0.5, 0.6)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.01) * 0.3, 0.75 + 0.12 * k)
    return reverb(x, 0.5, 0.25, 5000)


def mais_forte_ainda(rng, v):
    """O gancho: o grito curto, o vento subindo, o impacto e o rival voando."""
    x = _z(1.4)
    poe(x, _urro(rng, 0.3, 110, 140, 0.45), 0.0)
    poe(x, _whoosh(rng, 0.25, 200, 1500, 0.8, g=0.6), 0.02)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.2)
    poe(x, baque(n_de(0.6), 90, 35, 0.2, 0.9), 0.2)
    poe(x, _whoosh(rng, 0.45, 600, 2500, 0.3, g=0.4), 0.25)
    return reverb(x, 0.45, 0.2, 5500)


SONS: dict = {
    "soco-do-hulk": (soco_do_hulk, "o soco do Hulk: vento pesado e impacto grave"),
    "hulk-esmaga": (hulk_esmaga, "Esmagar: o estrondo dos dois punhos no chão"),
    "rugido-do-hulk": (rugido_do_hulk, "Rugido: o urro longo e grave"),
    "furia-hulk": (furia_hulk, "a fúria do Hulk crescendo"),
    "mais-forte-ainda": (mais_forte_ainda, "Mais forte ainda: o gancho de baixo para cima"),
}
