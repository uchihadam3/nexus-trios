"""Sons dos ataques básicos, lote zb (veja tools/vfx/familias_v2/basicos_zb.py).

O estrondo sônico e o soco do Invencível, o metal do sai e o soco bravo do Raphael, o tapa estalado de desenho do
Pica-Pau com os passarinhos, o bip do Omnitrix e o estalo verde do Ben 10, o soco largo com o brilho de poder do
He-Man, o soco de moinho do Popeye com o "tuuut" de navio, o soquinho de esponja com as bolhas do Bob Esponja e o
soco de metal pesado com o servo do Megatron. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, varre


def _t(n):
    return np.arange(n) / SR


def soco_do_invencivel(rng, v):
    x = _z(1.05)
    poe(x, _whoosh(rng, 0.1, 1200, 7000, 0.7, g=0.5), 0.0)
    poe(x, baque(n_de(0.35), 70, 30, 0.1, 0.8) * 0.6, 0.06)
    poe(x, _acerto(rng, v, 1.1, 110), 0.11)
    poe(x, B._carne(rng, n_de(0.15), 0.04, 2.6) * 0.5, 0.11)
    return reverb(x, 0.3, 0.14, 6000)


def soco_de_sai_raphael(rng, v):
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.12, 600, 3600, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 1.05, 120), 0.14)
    poe(x, modal(n_de(0.35), 1350 + 40 * v, rng=rng, **METAL) * 0.12, 0.14)
    return reverb(x, 0.22, 0.1, 6500)


def tapa_do_picapau(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.09, 900, 4500, 0.85, g=0.35), 0.0)
    poe(x, B._tapa(rng, n_de(0.08), 1500, 7000, 0.008) * 1.1, 0.11)
    poe(x, estalo(rng, n_de(0.04), 2500, 9000, 0.004) * 0.5, 0.11)
    for k in range(4):
        n = n_de(0.08)
        poe(x, seno(varre(2400, 3000, n, 1.0), n) * env(n, 0.003, 0.05) * 0.05, 0.25 + 0.08 * k)
    return reverb(x, 0.22, 0.1, 8000)


def soco_do_omnitrix(rng, v):
    x = _z(1.0)
    for k, f in enumerate((1760, 2349)):
        n = n_de(0.06)
        poe(x, np.sign(seno(np.full(n, float(f)), n)) * env(n, 0.002, 0.04) * 0.04, 0.02 + 0.07 * k)
    poe(x, _whoosh(rng, 0.12, 500, 3200, 0.85, g=0.42), 0.02)
    poe(x, _acerto(rng, v, 0.95, 120), 0.14)
    poe(x, _chiado(rng, 0.3, 1500, 8000, 0.004, 0.4), 0.15)
    return reverb(x, 0.25, 0.12, 6500)


def soco_de_eternia(rng, v):
    x = _z(1.15)
    n = n_de(0.3)
    poe(x, seno(varre(220, 440, n, 1.2), n) * env(n, 0.05, 0.2) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.15, 350, 2600, 0.85, g=0.5), 0.04)
    poe(x, _acerto(rng, v, 1.2, 95), 0.16)
    for k, f in enumerate((523, 659, 784)):
        poe(x, _brilho(rng, 0.5, f * 2, 0.03, SINO), 0.17 + 0.03 * k)
    return reverb(x, 0.4, 0.18, 6000)


def soco_da_ancora_popeye(rng, v):
    x = _z(1.15)
    n = n_de(0.25)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * t)) * env(n, 0.03, 0.2) * 0.35, 0.0)
    poe(x, _acerto(rng, v, 1.15, 105), 0.16)
    n = n_de(0.35)
    poe(x, (seno(np.full(n, 196.0), n) + 0.5 * seno(np.full(n, 294.0), n)) * env(n, 0.03, 0.25) * 0.1, 0.2)
    return reverb(x, 0.3, 0.14, 6000)


def soquinho_de_esponja(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.08, 800, 3600, 0.85, g=0.3), 0.0)
    poe(x, baque(n_de(0.2), 220, 110, 0.05, 0.4) * 0.5, 0.13)
    poe(x, passa(rosa(rng, n_de(0.08)), 300, 2000, 2) * env(n_de(0.08), 0.002, 0.05) * 0.4, 0.13)
    for k in range(6):
        n = n_de(0.06)
        f = 700 + 180 * k
        poe(x, seno(varre(f, f * 1.8, n, 1.0), n) * env(n, 0.002, 0.04) * 0.06, 0.18 + 0.05 * k)
    return reverb(x, 0.25, 0.12, 7000)


def soco_decepticon(rng, v):
    x = _z(1.25)
    n = n_de(0.2)
    poe(x, seno(varre(160, 520, n, 1.2), n) * env(n, 0.01, 0.15) * 0.1, 0.0)
    poe(x, _whoosh(rng, 0.2, 200, 1600, 0.9, g=0.5), 0.04)
    poe(x, _acerto(rng, v, 1.2, 80), 0.2)
    poe(x, modal(n_de(0.6), 260 + 10 * v, rng=rng, **METAL) * 0.3, 0.2)
    poe(x, graos(rng, n_de(0.4), 24, 0.0, 0.35, 2000, 8000, 0.004) * 0.35, 0.21)
    return reverb(x, 0.4, 0.18, 5000)


SONS: dict = {
    "soco-do-invencivel": (soco_do_invencivel, "básico de Invencível: o estrondo sônico e o soco"),
    "soco-de-sai-raphael": (soco_de_sai_raphael, "básico de Raphael: o soco com o cabo do sai"),
    "tapa-do-picapau": (tapa_do_picapau, "básico de Pica-Pau: o tapa estalado e os passarinhos"),
    "soco-do-omnitrix": (soco_do_omnitrix, "básico de Ben 10: o bip do Omnitrix e o estalo verde"),
    "soco-de-eternia": (soco_de_eternia, "básico de He-Man: o soco largo com o brilho de poder"),
    "soco-da-ancora-popeye": (soco_da_ancora_popeye, "básico de Popeye: o soco de moinho e o tuuut de navio"),
    "soquinho-de-esponja": (soquinho_de_esponja, "básico de Bob Esponja: o soquinho fofo e as bolhas"),
    "soco-decepticon": (soco_decepticon, "básico de Megatron: o servo e o soco de metal pesado"),
}
