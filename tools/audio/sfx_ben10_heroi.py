"""Sons das três habilidades do Ben 10 sem os nomes dos aliens (veja tools/vfx/familias_v2/ben10_heroi.py).

O "zwip" do Omnitrix girando e o pulso verde prendendo o alvo, o relógio superaquecendo em bipes cada vez mais rápidos
até explodir em fogo, e o "É hora do herói": o clique do relógio, o rastro zunindo e o golpe. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _whoosh, _z
from sfx_rodada30 import _fogo
from sfx_unicas_d import _baque, _t
from som import CRISTAL, assobio, env, estalo, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _zwip(rng, seg=0.3, de=260, ate=2200, g=0.32):
    """O Omnitrix girando: o tom que sobe com o brilho."""
    n = n_de(seg)
    t = _t(n)
    f = varre(de, ate, n, 0.9)
    z = seno(f * (1 + 0.08 * np.sin(2 * math.pi * 38 * t)), n) + 0.5 * seno(f * 1.5, n) + 0.3 * seno(f * 2.01, n)
    return satura(z * 0.6, 1.6) * sobe_e_some(n, 0.75, 1.3) * g


def pulso_do_omnitrix(rng, v):
    x = _z(1.6)
    poe(x, _zwip(rng), 0.0)
    for k in range(3):
        m = n_de(0.35)
        poe(x, seno(varre(180, 90, m), m) * env(m, 0.003, 0.3) * 0.25, 0.22 + 0.08 * k)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.004) * 0.6, 0.48 + 0.06 * k)
        poe(x, modal(n_de(0.4), 900 + 140 * k, rng=rng, **CRISTAL) * env(n_de(0.4), 0.001, 0.3) * 0.05, 0.48 + 0.06 * k)
    poe(x, _baque(150, 70, 0.3, 0.45), 0.6)
    return reverb(x, 0.45, 0.22)


def sobrecarga_do_omnitrix(rng, v):
    x = _z(2.0)
    # bipes cada vez mais rápidos e agudos: o relógio superaquecendo
    tempo, k = 0.0, 0
    while tempo < 0.36:
        m = n_de(0.035)
        poe(x, seno(1200 + 120 * k, m) * env(m, 0.002, 0.025) * 0.12, tempo)
        tempo += max(0.03, 0.09 - 0.012 * k)
        k += 1
    poe(x, assobio(rng, n_de(0.36), 400, 5000, 0.9, 0.4) * sobe_e_some(n_de(0.36), 0.9, 1.4) * 0.3, 0.0)
    m = n_de(0.5)
    poe(x, satura(passa(rosa(rng, m), 60, 3000, 2) * env(m, 0.002, 0.3), 2.2) * 0.6, 0.38)
    for j in range(3):
        poe(x, _fogo(rng, 0.45, 0.22, 0.12), 0.42 + 0.05 * j)
        poe(x, _baque(140, 70, 0.2, 0.35), 0.6 + 0.05 * j)
    return reverb(x, 0.5, 0.25)


def hora_do_heroi(rng, v):
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.03), 1500, 7000, 0.004) * 0.7, 0.0)
    poe(x, _zwip(rng, 0.28, 300, 2600, 0.35), 0.02)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 900, 9000, 2) * env(m, 0.002, 0.12) * 0.45, 0.28)
    poe(x, _whoosh(rng, 0.16, 1500, 9000, 0.6, 1.4, 0.45), 0.34)
    poe(x, B.soco_pesado(rng, v) * 1.05, 0.48)
    poe(x, _baque(140, 60, 0.3, 0.55), 0.48)
    return reverb(x, 0.45, 0.2)


SONS: dict = {
    "pulso-do-omnitrix": (pulso_do_omnitrix, "Ben 10: o zwip do Omnitrix e o pulso verde que prende"),
    "sobrecarga-do-omnitrix": (sobrecarga_do_omnitrix, "Ben 10: o relógio superaquecendo e explodindo em fogo"),
    "hora-do-heroi": (hora_do_heroi, "Ben 10: É hora do herói! — o clique, o rastro e o golpe"),
}
