"""Sons dos ataques básicos, lote zl (veja tools/vfx/familias_v2/basicos_zl.py).

A garra pesada e a baforada do Bowser, as garras com o crepitar de fogo do Charizard, o zumbido dourado da Joia da
Mente do Visão, o raio borbulhante e o portal do Rick, o "pew" de desenho do desintegrador do Marvin, o raio
ondulante da Dimensão X do Krang, o "pff" ridículo do laser do Plankton e o soco de metal oco da armadura do
Alphonse. Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

from sfx_basicos_f import _corte_curto
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_basicos_zk import _fogo
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def garra_do_rei_bowser(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.18, 200, 1800, 0.85, g=0.6), 0.0)
    for k in range(3):
        poe(x, _corte_curto(rng, 0.1, 800, 5000, 0.45), 0.14 + 0.015 * k)
    poe(x, _acerto(rng, v, 0.8, 90), 0.16)
    poe(x, _fogo(rng, 0.4, 120, 2000, 0.55), 0.26)
    return reverb(x, 0.4, 0.18, 6000)


def garra_flamejante(rng, v):
    x = _z(1.2)
    for k in range(3):
        poe(x, _corte_curto(rng, 0.1, 1200, 7000, 0.5), 0.02 + 0.02 * k)
    poe(x, _fogo(rng, 0.5, 300, 4000, 0.5), 0.12)
    return reverb(x, 0.35, 0.16, 7000)


def raio_da_joia_mente(rng, v):
    x = _z(1.1)
    n = n_de(0.4)
    poe(x, (seno(880, n) + seno(1320, n) * 0.5) * sobe_e_some(n, 0.3, 1.3) * 0.06, 0.0)
    m = n_de(0.25)
    poe(x, seno(varre(2400, 1800, m), m) * env(m, 0.003, 0.2) * 0.08, 0.06)
    poe(x, _brilho(rng, 0.4, 2637, 0.05, CRISTAL), 0.16)
    return reverb(x, 0.4, 0.2, 9500)


def arma_de_raio_rick(rng, v):
    x = _z(1.2)
    n = n_de(0.2)
    poe(x, seno(varre(300, 1400, n) + 60 * np.sin(np.arange(n) / SR * 90), n) * env(n, 0.002, 0.15) * 0.15, 0.02)
    m = n_de(0.5)
    poe(x, (passa(rosa(rng, m), 300, 3000, 2) * 0.4 + seno(varre(200, 500, m), m) * 0.2) * sobe_e_some(m, 0.2, 1.3) * 0.6, 0.16)
    return reverb(x, 0.45, 0.22, 7500)


def desintegrador_marvin(rng, v):
    x = _z(1.1)
    n = n_de(0.2)
    poe(x, seno(varre(2400, 700, n), n) * env(n, 0.002, 0.16) * 0.14, 0.04)
    poe(x, graos(rng, n_de(0.4), 40, 0.0, 0.6, 2000, 9000, 0.004) * 0.35, 0.2)
    return reverb(x, 0.35, 0.16, 9000)


def raio_da_dimensao_x(rng, v):
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, seno(varre(200, 600, n) + 80 * np.sin(np.arange(n) / SR * 40), n) * sobe_e_some(n, 0.3, 1.2) * 0.12, 0.04)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 150, 2000, 2) * sobe_e_some(m, 0.2, 1.4) * 0.4, 0.18)
    return reverb(x, 0.55, 0.26, 7000)


def laser_minusculo(rng, v):
    x = _z(0.9)
    n = n_de(0.08)
    poe(x, seno(varre(3200, 2600, n), n) * env(n, 0.001, 0.06) * 0.06, 0.05)
    m = n_de(0.1)
    poe(x, passa(rosa(rng, m), 1500, 6000, 2) * env(m, 0.001, 0.06) * 0.15, 0.25)
    return reverb(x, 0.2, 0.08, 9000)


def punho_de_armadura_al(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.16, 300, 2500, 0.85, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 0.8, 100), 0.2)
    poe(x, modal(n_de(0.6), 180, rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.4) * 0.12, 0.2)
    n = n_de(0.4)
    poe(x, seno(varre(500, 900, n), n) * sobe_e_some(n, 0.2, 1.3) * 0.04, 0.22)
    return reverb(x, 0.45, 0.2, 6500)


SONS: dict = {
    "garra-do-rei-bowser": (garra_do_rei_bowser, "básico de Bowser: a garra pesada e a baforada"),
    "garra-flamejante": (garra_flamejante, "básico de Charizard: as garras e o crepitar de fogo"),
    "raio-da-joia-mente": (raio_da_joia_mente, "básico de Visão: o zumbido dourado da Joia da Mente"),
    "arma-de-raio-rick": (arma_de_raio_rick, "básico de Rick: o raio borbulhante e o portal"),
    "desintegrador-marvin": (desintegrador_marvin, "básico de Marvin: o pew do desintegrador"),
    "raio-da-dimensao-x": (raio_da_dimensao_x, "básico de Krang: o raio ondulante da Dimensão X"),
    "laser-minusculo": (laser_minusculo, "básico de Plankton: o pff ridículo do laser"),
    "punho-de-armadura-al": (punho_de_armadura_al, "básico de Alphonse: o soco de metal oco da armadura"),
}
