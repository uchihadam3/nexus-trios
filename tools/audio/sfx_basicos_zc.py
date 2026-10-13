"""Sons dos ataques básicos, lote zc (veja tools/vfx/familias_v2/basicos_zc.py).

O zunido de voo e o "pow" da Docinho, o soco borrachudo com o tlin-tlin musical do Mickey, o "rá!" de caratê do Buzz
(só o sopro e o estalo), o soco de pano com o brilho da estrela do Woody, o gelo deslizando do Gelado, o fogo manso
soprando do Iroh, as lâminas raspando do Destruidor e o disco de hóquei estalando do Casey Jones. Tudo sintetizado.
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


def soco_superpoderosa(rng, v):
    x = _z(1.0)
    n = n_de(0.18)
    poe(x, seno(varre(900, 2200, n, 1.3), n) * env(n, 0.01, 0.12) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.1, 1200, 6000, 0.8, g=0.45), 0.02)
    poe(x, baque(n_de(0.25), 170, 80, 0.06, 0.6) * 0.65, 0.12)
    poe(x, B.soco_leve(rng, v) * 0.5, 0.12)
    return reverb(x, 0.25, 0.12, 7000)


def soco_musical_mickey(rng, v):
    x = _z(1.15)
    n = n_de(0.2)
    poe(x, seno(varre(300, 700, n, 1.0), n) * env(n, 0.01, 0.15) * 0.06, 0.0)
    poe(x, baque(n_de(0.2), 220, 110, 0.05, 0.6) * 0.6, 0.15)
    poe(x, B.soco_leve(rng, v) * 0.4, 0.15)
    for k, f in enumerate((1047, 1319, 1568, 2093)):
        n = n_de(0.2)
        poe(x, (seno(np.full(n, float(f)), n) + 0.3 * seno(np.full(n, 2.0 * f), n)) * env(n, 0.004, 0.15) * 0.06, 0.22 + 0.08 * k)
    return reverb(x, 0.25, 0.12, 8000)


def golpe_de_carate_buzz(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.14, 800, 5000, 0.9, g=0.55), 0.04)
    poe(x, B._tapa(rng, n_de(0.07), 1500, 7000, 0.006) * 0.9, 0.17)
    poe(x, _acerto(rng, v, 0.7, 140), 0.17)
    for k in range(3):
        poe(x, _brilho(rng, 0.25, 2349 + 300 * k, 0.025, CRISTAL), 0.2 + 0.05 * k)
    return reverb(x, 0.25, 0.12, 8000)


def soco_do_xerife(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.12, 400, 2600, 0.85, g=0.4), 0.0)
    poe(x, passa(rosa(rng, n_de(0.08)), 200, 1500, 2) * env(n_de(0.08), 0.002, 0.05) * 0.6, 0.15)
    poe(x, baque(n_de(0.2), 150, 70, 0.05, 0.5) * 0.5, 0.15)
    poe(x, _brilho(rng, 0.5, 1760, 0.05, SINO), 0.18)
    return reverb(x, 0.28, 0.13, 7000)


def soco_de_rampa_de_gelo(rng, v):
    x = _z(1.1)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.03, 0.2) * 0.3, 0.0)
    poe(x, seno(varre(400, 900, n, 1.0), n) * env(n, 0.03, 0.2) * 0.04, 0.0)
    poe(x, _acerto(rng, v, 0.95, 120), 0.15)
    for k in range(5):
        poe(x, modal(n_de(0.2), 2500 + 300 * k, rng=rng, **VIDRO) * 0.05, 0.17 + 0.03 * k)
    return reverb(x, 0.3, 0.14, 8000)


def palma_de_fogo_iroh(rng, v):
    x = _z(1.15)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1800, 2) * (0.75 + 0.25 * np.sin(2 * math.pi * 7 * t)) * env(n, 0.08, 0.3) * 0.4, 0.04)
    poe(x, baque(n_de(0.25), 110, 60, 0.07, 0.3) * 0.45, 0.27)
    poe(x, B.soco_leve(rng, v) * 0.35, 0.27)
    poe(x, graos(rng, n_de(0.35), 16, 0.0, 0.3, 2000, 6000, 0.004) * 0.25, 0.28)
    return reverb(x, 0.35, 0.16, 5500)


def soco_de_laminas_destruidor(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.12, 600, 4000, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.9, 120), 0.13)
    for k in range(3):
        n = n_de(0.12)
        poe(x, passa(rosa(rng, n), 3500, 11000, 2) * env(n, 0.002, 0.08) * 0.35, 0.13 + 0.025 * k)
    poe(x, modal(n_de(0.35), 1700, rng=rng, **METAL) * 0.1, 0.14)
    return reverb(x, 0.25, 0.12, 7000)


def soco_de_hoquei(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.12, 400, 2800, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 1.05, 110), 0.14)
    poe(x, B._tapa(rng, n_de(0.05), 1200, 5000, 0.006) * 0.6, 0.16)
    poe(x, _whoosh(rng, 0.2, 1500, 6000, 0.5, g=0.3), 0.17)
    return reverb(x, 0.3, 0.14, 6500)


SONS: dict = {
    "soco-superpoderosa": (soco_superpoderosa, "básico de Docinho: o zunido de voo e o pow"),
    "soco-musical-mickey": (soco_musical_mickey, "básico de Mickey: o soco borrachudo e as notinhas"),
    "golpe-de-carate-buzz": (golpe_de_carate_buzz, "básico de Buzz: o golpe de caratê e o brilho espacial"),
    "soco-do-xerife": (soco_do_xerife, "básico de Woody: o soco de pano e o brilho da estrela"),
    "soco-de-rampa-de-gelo": (soco_de_rampa_de_gelo, "básico de Gelado: o gelo deslizando e os cristais"),
    "palma-de-fogo-iroh": (palma_de_fogo_iroh, "básico de Iroh: o fogo manso soprando e a palma"),
    "soco-de-laminas-destruidor": (soco_de_laminas_destruidor, "básico de Destruidor: as lâminas raspando"),
    "soco-de-hoquei": (soco_de_hoquei, "básico de Casey Jones: o soco e o disco voando"),
}
