"""Sons dos ataques básicos, lote za (veja tools/vfx/familias_v2/basicos_za.py).

O "pof" fofo e o plim da estrela do Kirby, o estalo de dedo minúsculo e o estrondo desproporcional do Beerus, o
zumbido psíquico do Mewtwo, o ar fluindo e girando do Garou, o vapor e o soco de aço do Genos, o soco de rua do
Yusuke, o soco pesado com o acorde grave do Darkseid e as correntes com o fogo verde do Spawn. Tudo sintetizado.
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


def soquinho_estrelado_kirby(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.08, 800, 3600, 0.85, g=0.3), 0.0)
    poe(x, baque(n_de(0.2), 260, 120, 0.04, 0.6) * 0.6, 0.12)
    n = n_de(0.3)
    poe(x, seno(varre(880, 1760, n, 1.2), n) * env(n, 0.005, 0.2) * 0.08, 0.14)
    for k, f in enumerate((1568, 2093)):
        poe(x, _brilho(rng, 0.3, f, 0.03, CRISTAL), 0.18 + 0.07 * k)
    return reverb(x, 0.22, 0.1, 8000)


def peteleco_divino(rng, v):
    x = _z(1.2)
    poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.003) * 0.6, 0.17)
    poe(x, _acerto(rng, v, 1.2, 70), 0.18)
    poe(x, baque(n_de(0.6), 50, 25, 0.18, 0.6) * 0.7, 0.18)
    poe(x, _sopro(rng, 0.5, 150, 1400, 0.45), 0.19)
    return reverb(x, 0.45, 0.2, 4500)


def pancada_psiquica_mewtwo(rng, v):
    x = _z(1.15)
    n = n_de(0.45)
    t = _t(n)
    poe(x, seno(varre(180, 360, n, 1.2), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 18 * t)) * env(n, 0.05, 0.3) * 0.12, 0.0)
    poe(x, _acerto(rng, v, 0.85, 110), 0.24)
    n = n_de(0.4)
    poe(x, seno(varre(600, 300, n, 1.0), n) * env(n, 0.01, 0.3) * 0.08, 0.24)
    return reverb(x, 0.4, 0.2, 6000)


def punho_da_correnteza(rng, v):
    x = _z(1.1)
    n = n_de(0.3)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 8 * t)) * env(n, 0.05, 0.2) * 0.35, 0.0)
    poe(x, _acerto(rng, v, 1.0, 115), 0.15)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * (6 + 10 * t) * t)) * env(n, 0.02, 0.3) * 0.35, 0.16)
    return reverb(x, 0.3, 0.14, 6000)


def soco_de_aco_genos(rng, v):
    x = _z(1.1)
    poe(x, passa(rosa(rng, n_de(0.25)), 2500, 9000, 2) * env(n_de(0.25), 0.01, 0.2) * 0.35, 0.02)
    poe(x, _whoosh(rng, 0.12, 500, 3200, 0.85, g=0.4), 0.03)
    poe(x, _acerto(rng, v, 0.95, 115), 0.14)
    poe(x, modal(n_de(0.4), 600 + 25 * v, rng=rng, **METAL) * 0.16, 0.14)
    poe(x, _sopro(rng, 0.4, 200, 1500, 0.35), 0.16)
    return reverb(x, 0.28, 0.13, 6000)


def soco_de_rua_yusuke(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.13, 400, 3000, 0.85, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 1.1, 110), 0.14)
    poe(x, _chiado(rng, 0.2, 2500, 9000, 0.005, 0.25), 0.15)
    poe(x, graos(rng, n_de(0.35), 20, 0.0, 0.3, 400, 2500, 0.01) * 0.35, 0.16)
    return reverb(x, 0.25, 0.12, 6000)


def soco_omega(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.25, 180, 1400, 0.9, g=0.55), 0.0)
    poe(x, _acerto(rng, v, 1.25, 75), 0.2)
    n = n_de(0.7)
    acorde = sum(seno(np.full(n, f), n) for f in (55.0, 82.4, 110.0)) / 3
    poe(x, satura(acorde, 2) * env(n, 0.02, 0.5) * 0.25, 0.2)
    poe(x, estalo(rng, n_de(0.08), 600, 5000, 0.015) * 0.4, 0.21)
    return reverb(x, 0.5, 0.22, 4000)


def soco_de_necroplasma(rng, v):
    x = _z(1.1)
    for k in range(4):
        poe(x, modal(n_de(0.12), 1500 + 200 * (k % 2), rng=rng, **METAL) * 0.06, 0.02 + 0.04 * k)
    poe(x, _whoosh(rng, 0.13, 400, 3000, 0.85, g=0.4), 0.02)
    poe(x, _acerto(rng, v, 1.0, 105), 0.15)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 150, 1200, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * env(n, 0.02, 0.3) * 0.5, 0.16)
    return reverb(x, 0.35, 0.16, 5000)


SONS: dict = {
    "soquinho-estrelado-kirby": (soquinho_estrelado_kirby, "básico de Kirby: o pof fofo e o plim da estrela"),
    "peteleco-divino": (peteleco_divino, "básico de Beerus: o estalinho do dedo e o estrondo desproporcional"),
    "pancada-psiquica-mewtwo": (pancada_psiquica_mewtwo, "básico de Mewtwo: o zumbido psíquico e a pancada"),
    "punho-da-correnteza": (punho_da_correnteza, "básico de Garou: o ar fluindo e girando no soco"),
    "soco-de-aco-genos": (soco_de_aco_genos, "básico de Genos: o vapor e o soco de aço"),
    "soco-de-rua-yusuke": (soco_de_rua_yusuke, "básico de Yusuke: o soco de rua e as faíscas espirituais"),
    "soco-omega": (soco_omega, "básico de Darkseid: o soco pesado e o acorde grave"),
    "soco-de-necroplasma": (soco_de_necroplasma, "básico de Spawn: as correntes e o fogo verde"),
}
