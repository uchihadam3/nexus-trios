"""Sons dos ataques básicos, lote x (veja tools/vfx/familias_v2/basicos_x.py).

O aperto molhado e o sangue sendo sugado do DIO, o soco e o broto crescendo com um brilho do Giorno, o soco e o
ronco curto da serra do Denji, o sangue endurecendo e estalando da Power, o "piu" do punho minúsculo virando um
estrondo do Homem-Formiga, o fogo rugindo e os ossos batendo do Motoqueiro, o rasante e o soco cheio da Vampira e
o tapa pegajoso do Venom. Tudo sintetizado.
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


def _gorgolejo(rng, seg, lo=200, hi=1400, taxa=14, g=0.4):
    """Som molhado: ruído grave pulsando irregular (sangue, gosma)."""
    n = n_de(seg)
    t = _t(n)
    mod = 0.5 + 0.5 * np.sin(2 * math.pi * taxa * t + 3 * np.sin(2 * math.pi * 3.1 * t))
    return passa(rosa(rng, n), lo, hi, 2) * mod * env(n, 0.02, seg * 0.6) * g


def toque_vampirico_dio(rng, v):
    """DIO: a mão crava num aperto seco e o sangue é sugado num gorgolejo que sobe."""
    x = _z(1.15)
    poe(x, _whoosh(rng, 0.12, 500, 3000, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.8, 120), 0.13)
    poe(x, _gorgolejo(rng, 0.55, 250, 1600, 11, 0.5), 0.18)
    n = n_de(0.5)
    poe(x, seno(varre(160, 420, n, 1.3), n) * env(n, 0.1, 0.3) * 0.06, 0.2)
    return reverb(x, 0.3, 0.15, 5000)


def soco_da_vida_giorno(rng, v):
    """Giorno: o soco e, logo depois, o broto crescendo num farfalhar e o brilho das flores abrindo."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.12, 500, 3200, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 0.95, 120), 0.13)
    poe(x, graos(rng, n_de(0.4), 22, 0.0, 0.35, 2500, 8000, 0.006) * 0.3, 0.2)
    for k, f in enumerate((1319, 1760, 2093)):
        poe(x, _brilho(rng, 0.4, f, 0.035, CRISTAL), 0.32 + 0.06 * k)
    return reverb(x, 0.3, 0.15, 7000)


def soco_serrilhado(rng, v):
    """Denji: o soco de briga com o ronco curto da serra e o sangue espirrando."""
    x = _z(1.0)
    n = n_de(0.3)
    t = _t(n)
    serra = satura(seno(np.full(n, 95.0), n) * (0.6 + 0.4 * np.sign(np.sin(2 * math.pi * 38 * t))), 3) * env(n, 0.02, 0.22) * 0.18
    poe(x, serra + passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.02, 0.2) * 0.12, 0.0)
    poe(x, _acerto(rng, v, 1.0, 115), 0.13)
    poe(x, _gorgolejo(rng, 0.3, 400, 2500, 20, 0.4), 0.15)
    return reverb(x, 0.25, 0.12, 6000)


def punho_de_sangue_power(rng, v):
    """Power: o sangue endurecendo em espinhos (estalos curtos), o soco e o respingo."""
    x = _z(1.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.004) * 0.35, 0.04 + 0.03 * k)
    poe(x, _whoosh(rng, 0.13, 450, 3000, 0.85, g=0.42), 0.02)
    poe(x, _acerto(rng, v, 1.05, 115), 0.15)
    poe(x, _gorgolejo(rng, 0.3, 400, 2600, 22, 0.45), 0.16)
    return reverb(x, 0.25, 0.12, 6000)


def soco_formiga(rng, v):
    """Homem-Formiga: um "piu" agudinho do punho minúsculo que desce de tom virando um estrondo de soco gigante."""
    x = _z(1.1)
    n = n_de(0.18)
    poe(x, seno(varre(2600, 300, n, 1.6), n) * env(n, 0.005, 0.14) * 0.12, 0.0)
    poe(x, _whoosh(rng, 0.1, 2000, 9000, 0.7, g=0.3), 0.0)
    poe(x, _acerto(rng, v, 1.2, 90), 0.16)
    poe(x, baque(n_de(0.45), 70, 35, 0.12, 0.6) * 0.6, 0.16)
    poe(x, _sopro(rng, 0.4, 200, 1600, 0.35), 0.17)
    return reverb(x, 0.35, 0.16, 5000)


def soco_de_osso_em_chamas(rng, v):
    """Motoqueiro Fantasma: o fogo do inferno rugindo, os ossos estalando no soco e as brasas chiando."""
    x = _z(1.1)
    n = n_de(0.35)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 150, 1200, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 13 * t)) * env(n, 0.05, 0.25) * 0.5, 0.0)
    poe(x, _whoosh(rng, 0.13, 400, 3000, 0.85, g=0.4), 0.03)
    poe(x, _acerto(rng, v, 0.95, 110), 0.15)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 1200, 4000, 0.006) * 0.4, 0.15 + 0.02 * k)
    poe(x, graos(rng, n_de(0.45), 30, 0.0, 0.4, 2000, 8000, 0.004) * 0.35, 0.17)
    return reverb(x, 0.35, 0.16, 5000)


def soco_de_luva_da_vampira(rng, v):
    """Vampira: o rasante do voo, o soco com força emprestada e o choque em dois tempos."""
    x = _z(1.05)
    poe(x, _whoosh(rng, 0.2, 300, 2400, 0.8, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 1.15, 100), 0.14)
    poe(x, baque(n_de(0.35), 85, 40, 0.1, 0.6) * 0.5, 0.14)
    poe(x, _sopro(rng, 0.25, 300, 2200, 0.3), 0.21)
    return reverb(x, 0.3, 0.14, 6000)


def patada_simbionte(rng, v):
    """Venom: o tapa pesado e pegajoso e a gosma esticando e estalando."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.18, 250, 1800, 0.85, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 1.15, 90), 0.18)
    poe(x, _gorgolejo(rng, 0.45, 150, 1000, 9, 0.55), 0.2)
    for k in range(3):
        poe(x, B._tapa(rng, n_de(0.04), 600, 2500, 0.01) * 0.25, 0.3 + 0.06 * k)
    return reverb(x, 0.3, 0.15, 4500)


SONS: dict = {
    "toque-vampirico-dio": (toque_vampirico_dio, "básico de DIO: o aperto e o sangue sendo sugado"),
    "soco-da-vida-giorno": (soco_da_vida_giorno, "básico de Giorno: o soco, o broto e o brilho das flores"),
    "soco-serrilhado": (soco_serrilhado, "básico de Denji: o ronco curto da serra, o soco e o sangue"),
    "punho-de-sangue-power": (punho_de_sangue_power, "básico de Power: o sangue endurecendo e o soco"),
    "soco-formiga": (soco_formiga, "básico de Homem-Formiga: o piu do punho minúsculo virando estrondo"),
    "soco-de-osso-em-chamas": (soco_de_osso_em_chamas, "básico de Motoqueiro Fantasma: fogo rugindo e ossos estalando"),
    "soco-de-luva-da-vampira": (soco_de_luva_da_vampira, "básico de Vampira: o rasante e o soco com força emprestada"),
    "patada-simbionte": (patada_simbionte, "básico de Venom: o tapa pesado e a gosma estalando"),
}
