"""Sons dos golpes que saem do personagem e vão até o alvo (veja tools/vfx/familias_v2/viagens.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _whoosh, _z
from som import SR, baque, env, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _rugido_de_dragao(rng, n):
    """O rugido: ruído grave saturado com tremor rápido e um tom que cai."""
    t = np.arange(n) / SR
    x = satura(passa(rosa(rng, n), 90, 1800, 2) * (0.65 + 0.35 * np.sin(2 * math.pi * 31 * t)), 3.2)
    x += seno(varre(180, 75, n, 0.7), n) * 0.35
    return x * sobe_e_some(n, 0.18, 1.2)


def colera_do_dragao(rng, v):
    """Cólera do Dragão: a energia corre do Shiryu até o rival num sopro longo, o dragão ruge, o bote
    estoura no alvo e a espiral sobe num redemoinho que some no alto."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.55, 200, 3200, 0.9, g=0.8), 0.0)
    poe(x, _rugido_de_dragao(rng, n_de(0.8)) * 0.55, 0.18)
    poe(x, B.agua(rng, v)[: n_de(0.7)] * 0.5, 0.5)
    poe(x, baque(n_de(0.6), 80, 32, 0.25, 0.6) * 0.9, 0.5)
    poe(x, B.soco_pesado(rng, v) * 0.7, 0.5)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 400, 4000, 2) * sobe_e_some(n, 0.4, 1.4) * env(n, 0.05, 0.8) * 0.3, 0.7)
    return reverb(x, 0.6, 0.28, 5200)


SONS: dict = {
    "colera-do-dragao": (colera_do_dragao, "Cólera do Dragão do Shiryu: o sopro até o rival, o rugido, o bote e a espiral"),
}
