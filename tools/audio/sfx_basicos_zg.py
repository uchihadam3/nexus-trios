"""Sons dos ataques básicos, lote zg (veja tools/vfx/familias_v2/basicos_zg.py).

As duas katanas do Leonardo, o silêncio e o corte único do Samurai Jack com o vento nas folhas, a pancada bruta e o
ronco da pressão espiritual do Kenpachi, o giro da espada do Link com o "tlim", a estocada e os dois tiros do Dante, o
corte e o Sinal do Geralt, o corte e as asas dos morcegos do Alucard e os quatro cortes com o ki do Trunks. Tudo
sintetizado.
"""
from __future__ import annotations

import numpy as np

from sfx_basicos_f import _corte_curto
from sfx_basicos_h import _shing
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def katanas_gemeas_leonardo(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.12, 900, 5000, 0.7, g=0.4), 0.0)
    poe(x, _corte_curto(rng, 0.12, 1800, 9000, 0.6), 0.14)
    poe(x, _corte_curto(rng, 0.12, 2200, 9500, 0.55), 0.16)
    poe(x, modal(n_de(0.3), 2900, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.15) * 0.05, 0.16)
    return reverb(x, 0.3, 0.15, 8500)


def golpe_unico_jack(rng, v):
    x = _z(1.6)
    poe(x, modal(n_de(0.15), 3300, rng=rng, **METAL) * env(n_de(0.15), 0.001, 0.08) * 0.05, 0.0)
    poe(x, _shing(rng, 0.7, 2600, 0.22, 0.4), 0.18)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * sobe_e_some(n, 0.4, 1.6) * 0.25, 0.3)
    return reverb(x, 0.65, 0.28, 7500)


def corte_brutal_kenpachi(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.2, 150, 1200, 0.8, g=0.8), 0.0)
    poe(x, _acerto(rng, v, 1.0, 70), 0.18)
    poe(x, satura(baque(n_de(0.6), 60, 30, 0.2, 0.8), 2.2) * 0.6, 0.18)
    n = n_de(0.6)
    poe(x, satura(seno(varre(90, 50, n), n), 2.0) * sobe_e_some(n, 0.2, 1.3) * 0.25, 0.2)
    poe(x, graos(rng, n_de(0.4), 24, 0.0, 0.4, 300, 3000, 0.01) * 0.4, 0.22)
    return reverb(x, 0.45, 0.22, 5500)


def giro_da_espada_link(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.3, 500, 3500, 0.5, g=0.55), 0.0)
    poe(x, _corte_curto(rng, 0.12, 1800, 8500, 0.55), 0.2)
    for k, f in enumerate((2093, 2637, 3136)):
        poe(x, modal(n_de(0.4), f, rng=rng, **SINO) * env(n_de(0.4), 0.001, 0.25) * 0.05, 0.3 + 0.04 * k)
    return reverb(x, 0.4, 0.2, 9000)


def rebellion_dante(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.16, 400, 3000, 0.8, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 0.8, 110), 0.16)
    poe(x, _corte_curto(rng, 0.1, 1500, 8000, 0.5), 0.16)
    for k in range(2):
        n = n_de(0.12)
        poe(x, satura(passa(rosa(rng, n), 300, 7000, 2) * env(n, 0.001, 0.05), 2.5) * 0.55, 0.36 + 0.1 * k)
        poe(x, baque(n_de(0.15), 140, 80, 0.04, 0.6) * 0.3, 0.36 + 0.1 * k)
    return reverb(x, 0.35, 0.16, 7500)


def espada_de_prata_geralt(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.2, 500, 3500, 0.7, g=0.5), 0.0)
    poe(x, _corte_curto(rng, 0.14, 1600, 8500, 0.6), 0.2)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 120, 1800, 2) * sobe_e_some(n, 0.15, 1.2) * 0.55, 0.26)
    poe(x, seno(varre(200, 80, n), n) * env(n, 0.005, 0.3) * 0.12, 0.26)
    return reverb(x, 0.45, 0.2, 7000)


def corte_dos_morcegos(rng, v):
    x = _z(1.3)
    poe(x, _corte_curto(rng, 0.12, 2000, 9500, 0.6), 0.02)
    poe(x, _shing(rng, 0.4, 3000, 0.12, 0.3), 0.04)
    for k in range(8):
        n = n_de(0.04)
        poe(x, passa(rosa(rng, n), 600, 3000, 2) * env(n, 0.002, 0.03) * 0.3, 0.24 + 0.05 * k)
    for k in range(3):
        n = n_de(0.05)
        poe(x, seno(varre(5200, 6000, n), n) * env(n, 0.002, 0.03) * 0.03, 0.3 + 0.12 * k)
    return reverb(x, 0.55, 0.25, 7500)


def grade_de_cortes_trunks(rng, v):
    x = _z(1.2)
    for k in range(4):
        poe(x, _corte_curto(rng, 0.07, 2000, 10000, 0.5), 0.02 + 0.05 * k)
    poe(x, _acerto(rng, v, 0.7, 110), 0.26)
    n = n_de(0.45)
    poe(x, (seno(varre(300, 700, n), n) * 0.5 + passa(rosa(rng, n), 800, 5000, 2) * 0.6) * sobe_e_some(n, 0.15, 1.4) * 0.25, 0.26)
    return reverb(x, 0.35, 0.18, 8500)


SONS: dict = {
    "katanas-gemeas-leonardo": (katanas_gemeas_leonardo, "básico de Leonardo: as duas katanas juntas"),
    "golpe-unico-jack": (golpe_unico_jack, "básico de Samurai Jack: o silêncio, o corte único e o vento"),
    "corte-brutal-kenpachi": (corte_brutal_kenpachi, "básico de Kenpachi: a pancada bruta e a pressão espiritual"),
    "giro-da-espada-link": (giro_da_espada_link, "básico de Link: o giro da espada e o tlim"),
    "rebellion-dante": (rebellion_dante, "básico de Dante: a estocada e os dois tiros"),
    "espada-de-prata-geralt": (espada_de_prata_geralt, "básico de Geralt: o corte e o Sinal"),
    "corte-dos-morcegos": (corte_dos_morcegos, "básico de Alucard: o corte e as asas dos morcegos"),
    "grade-de-cortes-trunks": (grade_de_cortes_trunks, "básico de Trunks: quatro cortes e o ki dourado"),
}
