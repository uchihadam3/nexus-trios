"""Sons dos ataques básicos, lote w (veja tools/vfx/familias_v2/basicos_w.py).

Os dois tapas rápidos do Kuririn, o soco pesado e o cascalho do Kratos, as chamas escuras rugindo do Ganondorf,
o jab de CQC com o "tlin!" do alerta do Snake, o soco de desenho com o plim da moedinha do Mario, o gelo estalando
do Sub-Zero, o estalo de kung fu com a faixa chicoteando do Liu Kang e o estalo elétrico do Jin. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, seno, varre


def _t(n):
    return np.arange(n) / SR


def dois_jabs_kuririn(rng, v):
    """Kuririn: dois jabs rápidos, o segundo mais cheio."""
    x = _z(0.8)
    poe(x, _whoosh(rng, 0.08, 700, 3600, 0.85, g=0.35), 0.0)
    poe(x, B.soco_leve(rng, v) * 0.55, 0.08)
    poe(x, _whoosh(rng, 0.08, 700, 3600, 0.85, g=0.35), 0.12)
    poe(x, _acerto(rng, (v + 1) % 4, 0.9, 125), 0.2)
    return reverb(x, 0.2, 0.1, 6500)


def soco_espartano(rng, v):
    """Kratos: um soco pesado de cima, o chão arrebentando e o cascalho caindo."""
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.2, 250, 2000, 0.85, g=0.55), 0.0)
    poe(x, _acerto(rng, v, 1.25, 85), 0.2)
    poe(x, baque(n_de(0.45), 65, 32, 0.12, 0.6) * 0.65, 0.2)
    poe(x, graos(rng, n_de(0.5), 26, 0.05, 0.45, 500, 3500, 0.012) * 0.55, 0.22)
    return reverb(x, 0.35, 0.16, 5000)


def soco_das_trevas_ganondorf(rng, v):
    """Ganondorf: as chamas escuras rugindo grave em volta do punho e o estouro de magia negra."""
    x = _z(1.15)
    n = n_de(0.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 80, 600, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * env(n, 0.08, 0.25) * 0.55, 0.0)
    poe(x, _whoosh(rng, 0.18, 250, 1800, 0.85, g=0.45), 0.05)
    poe(x, _acerto(rng, v, 1.1, 90), 0.2)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 100, 900, 2) * env(n, 0.01, 0.35) * 0.55, 0.2)
    poe(x, seno(varre(110, 55, n, 1.2), n) * env(n, 0.01, 0.3) * 0.12, 0.2)
    return reverb(x, 0.4, 0.2, 4000)


def soco_cqc(rng, v):
    """Snake: o jab curto e seco e, logo depois, o "tlin!" agudo do alerta."""
    x = _z(0.9)
    poe(x, _whoosh(rng, 0.09, 800, 4200, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.95, 130), 0.12)
    n = n_de(0.35)
    alerta = seno(np.full(n, 1568.0), n) + 0.5 * seno(np.full(n, 3136.0), n)
    poe(x, alerta * env(n, 0.003, 0.22) * 0.12, 0.16)
    return reverb(x, 0.2, 0.1, 7000)


def soco_do_mario(rng, v):
    """Mario: o soco de desenho (um "pof" redondo), o plim da estrelinha e o tlin-tlin da moedinha."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.1, 600, 3000, 0.85, g=0.35), 0.0)
    poe(x, baque(n_de(0.2), 200, 90, 0.05, 0.6) * 0.65, 0.14)
    poe(x, B.soco_leve(rng, v) * 0.45, 0.14)
    for k, f in enumerate((988, 1319)):
        n = n_de(0.25)
        poe(x, (seno(np.full(n, f), n) + 0.3 * seno(np.full(n, 2 * f), n)) * env(n, 0.002, 0.18) * 0.1, 0.2 + 0.08 * k)
    return reverb(x, 0.22, 0.1, 7000)


def soco_glacial(rng, v):
    """Sub-Zero: o frio soprando em volta do punho, o soco e o gelo estalando e quebrando."""
    x = _z(1.15)
    poe(x, _sopro(rng, 0.25, 3000, 10000, 0.3), 0.0)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.42), 0.03)
    poe(x, _acerto(rng, v, 0.95, 120), 0.15)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 3000, 10000, 0.003) * 0.4, 0.16 + 0.02 * k)
    for k in range(6):
        poe(x, modal(n_de(0.25), 2600 + 340 * k, rng=rng, **VIDRO) * 0.06, 0.38 + 0.03 * k)
    return reverb(x, 0.3, 0.15, 7500)


def soco_da_faixa_vermelha(rng, v):
    """Liu Kang: a faixa chicoteando no ar, o soco reto e o estalo seco de kung fu."""
    x = _z(0.85)
    n = n_de(0.18)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 900, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 24 * t)) * env(n, 0.01, 0.12) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.1, 700, 4000, 0.85, g=0.45), 0.02)
    poe(x, _acerto(rng, v, 1.0, 130), 0.13)
    poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.006) * 0.45, 0.13)
    return reverb(x, 0.22, 0.1, 6500)


def soco_eletrico_jin(rng, v):
    """Jin: o soco travado de caratê e o estalo elétrico curto e rasgado."""
    x = _z(0.9)
    poe(x, _whoosh(rng, 0.09, 700, 4000, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 1.0, 125), 0.12)
    poe(x, _chiado(rng, 0.28, 1800, 11000, 0.0025, 0.55), 0.11)
    poe(x, estalo(rng, n_de(0.07), 1000, 9000, 0.01) * 0.55, 0.12)
    return reverb(x, 0.22, 0.1, 7000)


SONS: dict = {
    "dois-jabs-kuririn": (dois_jabs_kuririn, "básico de Kuririn: dois jabs rápidos"),
    "soco-espartano": (soco_espartano, "básico de Kratos: soco pesado e o cascalho caindo"),
    "soco-das-trevas-ganondorf": (soco_das_trevas_ganondorf, "básico de Ganondorf: chamas escuras rugindo e o estouro"),
    "soco-cqc": (soco_cqc, "básico de Snake: jab de CQC e o tlin do alerta"),
    "soco-do-mario": (soco_do_mario, "básico de Mario: o soco de desenho e o plim da moedinha"),
    "soco-glacial": (soco_glacial, "básico de Sub-Zero: o frio soprando e o gelo quebrando"),
    "soco-da-faixa-vermelha": (soco_da_faixa_vermelha, "básico de Liu Kang: a faixa chicoteando e o soco de kung fu"),
    "soco-eletrico-jin": (soco_eletrico_jin, "básico de Jin: o soco de caratê e o estalo elétrico"),
}
