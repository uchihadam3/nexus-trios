"""Sons dos ataques básicos, lote y (veja tools/vfx/familias_v2/basicos_y.py).

O soco de metal e o bip-bip dos circuitos do Ultron, o soco com a risadinha de faíscas e a baforada do Duende
Verde, o soco cósmico enorme do Galactus, a madeira estalando do Groot, a água espirrando do Aquaman, o zumbido
do anel virando luva de luz do Lanterna Verde, o soco cibernético com os bips digitais do Ciborgue e o trovão
curto do Shazam. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, varre


def _t(n):
    return np.arange(n) / SR


def _bip(f, seg=0.05, g=0.08):
    n = n_de(seg)
    return np.sign(seno(np.full(n, float(f)), n)) * env(n, 0.002, seg * 0.6) * g


def soco_de_metal_ultron(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.12, 500, 3200, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.85, 120), 0.14)
    poe(x, modal(n_de(0.4), 540 + 20 * v, rng=rng, **METAL) * 0.2, 0.14)
    for k, f in enumerate((1760, 2349, 1976, 2637)):
        poe(x, _bip(f, 0.04, 0.05), 0.2 + 0.05 * k)
    return reverb(x, 0.22, 0.1, 7000)


def soco_do_duende(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.9, 125), 0.14)
    poe(x, _chiado(rng, 0.3, 2000, 9000, 0.004, 0.35), 0.15)
    poe(x, _sopro(rng, 0.45, 200, 1600, 0.45), 0.16)
    return reverb(x, 0.28, 0.13, 5500)


def pancada_colossal_galactus(rng, v):
    x = _z(1.35)
    poe(x, _whoosh(rng, 0.3, 150, 1200, 0.9, g=0.6), 0.0)
    poe(x, _acerto(rng, v, 1.3, 70), 0.24)
    poe(x, baque(n_de(0.6), 55, 28, 0.18, 0.6) * 0.75, 0.24)
    for k, f in enumerate((1568, 2093, 2637, 3136)):
        poe(x, _brilho(rng, 0.5, f, 0.025, CRISTAL), 0.04 + 0.05 * k)
    return reverb(x, 0.5, 0.22, 4500)


def soco_de_madeira_groot(rng, v):
    x = _z(1.05)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * env(n, 0.05, 0.12) * 0.25, 0.0)
    poe(x, _whoosh(rng, 0.14, 400, 2600, 0.85, g=0.42), 0.03)
    poe(x, _acerto(rng, v, 1.05, 110), 0.17)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.01) * 0.35, 0.17 + 0.03 * k)
    poe(x, graos(rng, n_de(0.4), 14, 0.05, 0.35, 2500, 7000, 0.006) * 0.25, 0.25)
    return reverb(x, 0.28, 0.13, 5500)


def soco_da_mare(rng, v):
    x = _z(1.1)
    n = n_de(0.25)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 17 * t)) * env(n, 0.02, 0.2) * 0.35, 0.0)
    poe(x, _acerto(rng, v, 1.0, 115), 0.15)
    poe(x, passa(rosa(rng, n_de(0.5)), 800, 7000, 2) * env(n_de(0.5), 0.003, 0.25) * 0.5, 0.15)
    poe(x, graos(rng, n_de(0.5), 30, 0.05, 0.45, 1500, 6000, 0.008) * 0.4, 0.2)
    return reverb(x, 0.3, 0.14, 6000)


def soco_de_construto(rng, v):
    x = _z(1.05)
    n = n_de(0.3)
    t = _t(n)
    poe(x, seno(varre(220, 440, n, 1.2), n) * (0.8 + 0.2 * np.sin(2 * math.pi * 40 * t)) * env(n, 0.03, 0.2) * 0.12, 0.0)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.4), 0.05)
    poe(x, _acerto(rng, v, 1.05, 110), 0.17)
    poe(x, _brilho(rng, 0.45, 1319, 0.04, CRISTAL), 0.18)
    poe(x, _chiado(rng, 0.3, 2500, 9000, 0.005, 0.25), 0.22)
    return reverb(x, 0.3, 0.15, 6500)


def soco_cibernetico(rng, v):
    x = _z(1.0)
    n = n_de(0.12)
    poe(x, seno(varre(400, 1200, n, 1.2), n) * env(n, 0.01, 0.08) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.12, 500, 3400, 0.85, g=0.4), 0.02)
    poe(x, _acerto(rng, v, 0.9, 120), 0.15)
    poe(x, modal(n_de(0.35), 680, rng=rng, **METAL) * 0.12, 0.15)
    for k in range(5):
        poe(x, _bip(1200 + 260 * ((k * 3) % 5), 0.03, 0.045), 0.2 + 0.035 * k)
    return reverb(x, 0.22, 0.1, 7000)


def soco_relampago_shazam(rng, v):
    x = _z(1.05)
    poe(x, _whoosh(rng, 0.12, 500, 3400, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 1.05, 115), 0.13)
    poe(x, estalo(rng, n_de(0.08), 800, 9000, 0.012) * 0.7, 0.14)
    poe(x, _chiado(rng, 0.25, 2000, 11000, 0.0025, 0.45), 0.14)
    poe(x, baque(n_de(0.4), 70, 35, 0.12, 0.4) * 0.45, 0.16)
    return reverb(x, 0.35, 0.16, 6000)


SONS: dict = {
    "soco-de-metal-ultron": (soco_de_metal_ultron, "básico de Ultron: soco de metal e os bips dos circuitos"),
    "soco-do-duende": (soco_do_duende, "básico de Duende Verde: o soco, as faíscas e a baforada"),
    "pancada-colossal-galactus": (pancada_colossal_galactus, "básico de Galactus: a pancada cósmica enorme"),
    "soco-de-madeira-groot": (soco_de_madeira_groot, "básico de Groot: a madeira estalando e as folhas"),
    "soco-da-mare": (soco_da_mare, "básico de Aquaman: a água chiando e espirrando"),
    "soco-de-construto": (soco_de_construto, "básico de Lanterna Verde: o zumbido do anel e a luva de luz"),
    "soco-cibernetico": (soco_cibernetico, "básico de Ciborgue: o soco de metal e os bips digitais"),
    "soco-relampago-shazam": (soco_relampago_shazam, "básico de Shazam: o soco e o trovão curto"),
}
