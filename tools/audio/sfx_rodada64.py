"""Os sons da rodada 64 das habilidades próprias (veja tools/vfx/familias_v2/rodada64.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, varre


def getsuga_tensho_ichigo(rng, v):
    """Ichigo: "GETSUGA... TENSHŌ!" — a energia subindo, o corte e a lua crescente rasgando o ar."""
    x = _z(2.4)
    n = n_de(0.3)
    poe(x, satura(seno(varre(80, 160, n), n), 3) * env(n, 0.25, 0.05) * 0.04, 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 6000, 0.85, 1.3, 0.6), 0.2)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 300, 6000, 2) + seno(90, n) * 0.4, 3) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.02, 0.3) * 0.3, 0.3)
    poe(x, _baque(50, 20, 0.7, 0.9, 3.0), 0.55)
    poe(x, _explosao(rng, 0.5, 50), 0.55)
    poe(x, _sino(rng, 1319, 0.5, 0.025, METAL), 0.3)
    return reverb(x, 0.9, 0.45)


def gancho_de_garra_mabel(rng, v):
    """Mabel: o disparo da pistola de gancho ("pschhh"), a corda zunindo, o "clang" e o puxão."""
    x = _z(2.2)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 1000, 6000, 2) * env(n, 0.002, 0.1) * 0.3, 0.12)
    n = n_de(0.3)
    poe(x, seno(varre(1200, 600, n), n) * env(n, 0.02, 0.25) * 0.015, 0.14)
    poe(x, _sino(rng, 988, 0.3, 0.03, METAL), 0.38)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005) * 0.4, 0.38)
    poe(x, _whoosh(rng, 0.25, 300, 2000, 0.7, 1.3, 0.35), 0.55)
    for k in range(4):
        poe(x, _brilho(rng, 0.2, 1568 + 200 * k, 0.012, CRISTAL), 0.6 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "getsuga-tensho-ichigo": (getsuga_tensho_ichigo, "Ichigo: Getsuga Tensho"),
    "gancho-de-garra-mabel": (gancho_de_garra_mabel, "Mabel: gancho de garra"),
}
