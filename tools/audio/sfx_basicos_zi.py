"""Sons dos ataques básicos, lote zi (veja tools/vfx/familias_v2/basicos_zi.py).

O tiro seco do coronel com o estalo da transmutação, a rajada de três com as cápsulas do Justiceiro, os blasters
zunindo do Senhor das Estrelas, o canhão pesado com recuo do Rocket, a rajada do fuzil e o escudo estalando do Master
Chief, o tiro e a faca do Leon, o bipe da mira e os dois tiros da Jill, e o "pew pew pew" do Mega Buster. Tudo
sintetizado.
"""
from __future__ import annotations

import numpy as np

from sfx_basicos_f import _corte_curto
from sfx_basicos_g import _tilintar, _tiro_de_pistola
from sfx_basicos_l import _tiro
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def tiro_do_coronel(rng, v):
    x = _z(1.1)
    poe(x, _tiro_de_pistola(rng, v, 1.0) * 0.8, 0.0)
    n = n_de(0.4)
    poe(x, seno(varre(600, 1400, n), n) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.18)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * sobe_e_some(n, 0.15, 1.4) * 0.3, 0.22)
    return reverb(x, 0.35, 0.16, 7500)


def rajada_do_justiceiro(rng, v):
    x = _z(1.2)
    for k in range(3):
        poe(x, _tiro(rng, 0.6), 0.0 + 0.07 * k)
    poe(x, _tilintar(rng, 0.14), 0.15)
    poe(x, _tilintar(rng, 0.12), 0.3)
    poe(x, baque(n_de(0.4), 70, 40, 0.15, 0.4) * 0.4, 0.3)
    return reverb(x, 0.35, 0.15, 7000)


def blasters_do_quill(rng, v):
    x = _z(1.1)
    for k in range(2):
        n = n_de(0.18)
        poe(x, seno(varre(1800, 500, n), n) * env(n, 0.002, 0.14) * 0.15, 0.1 + 0.1 * k)
        poe(x, passa(rosa(rng, n), 800, 6000, 2) * env(n, 0.001, 0.08) * 0.3, 0.1 + 0.1 * k)
    poe(x, _acerto(rng, v, 0.5, 150), 0.22)
    return reverb(x, 0.35, 0.16, 8000)


def canhao_do_rocket(rng, v):
    x = _z(1.3)
    poe(x, satura(baque(n_de(0.5), 90, 35, 0.15, 1.0), 2.2) * 0.7, 0.05)
    n = n_de(0.25)
    poe(x, seno(varre(1200, 200, n), n) * env(n, 0.002, 0.2) * 0.18, 0.06)
    poe(x, satura(passa(rosa(rng, n_de(0.6)), 60, 4000, 2) * env(n_de(0.6), 0.003, 0.35), 2.0) * 0.6, 0.2)
    return reverb(x, 0.45, 0.2, 6000)


def rajada_do_spartan(rng, v):
    x = _z(1.1)
    for k in range(4):
        poe(x, _tiro(rng, 0.45), 0.0 + 0.05 * k)
    for k in range(4):
        n = n_de(0.08)
        poe(x, seno(varre(2400, 1600, n), n) * env(n, 0.001, 0.06) * 0.05, 0.1 + 0.05 * k)
    poe(x, graos(rng, n_de(0.25), 20, 0.0, 0.4, 3000, 10000, 0.005) * 0.4, 0.32)
    return reverb(x, 0.3, 0.14, 8000)


def tiro_e_faca_leon(rng, v):
    x = _z(1.2)
    poe(x, _tiro_de_pistola(rng, v, 1.1) * 0.75, 0.0)
    poe(x, _corte_curto(rng, 0.1, 2000, 9000, 0.55), 0.32)
    poe(x, _acerto(rng, v, 0.5, 160), 0.36)
    return reverb(x, 0.35, 0.16, 7500)


def mira_da_beretta(rng, v):
    x = _z(1.1)
    n = n_de(0.08)
    poe(x, seno(2200, n) * env(n, 0.002, 0.06) * 0.06, 0.02)
    for k in range(2):
        poe(x, _tiro_de_pistola(rng, v, 1.2) * 0.6, 0.13 + 0.1 * k)
    poe(x, _tilintar(rng, 0.12), 0.3)
    return reverb(x, 0.3, 0.14, 8000)


def mega_buster(rng, v):
    x = _z(1.0)
    for k in range(3):
        n = n_de(0.09)
        poe(x, (seno(varre(1300, 900, n), n) + 0.4 * seno(varre(2600, 1800, n), n)) * env(n, 0.001, 0.07) * 0.14, 0.0 + 0.08 * k)
        m = n_de(0.08)
        poe(x, passa(rosa(rng, m), 1500, 7000, 2) * env(m, 0.001, 0.05) * 0.2, 0.14 + 0.08 * k)
    return reverb(x, 0.25, 0.12, 9000)


SONS: dict = {
    "tiro-do-coronel": (tiro_do_coronel, "básico de Roy Mustang: o tiro e o estalo da transmutação"),
    "rajada-do-justiceiro": (rajada_do_justiceiro, "básico de Justiceiro: três tiros e as cápsulas"),
    "blasters-do-quill": (blasters_do_quill, "básico de Senhor das Estrelas: os dois blasters zunindo"),
    "canhao-do-rocket": (canhao_do_rocket, "básico de Rocket: o canhão pesado e o recuo"),
    "rajada-do-spartan": (rajada_do_spartan, "básico de Master Chief: a rajada e o escudo estalando"),
    "tiro-e-faca-leon": (tiro_e_faca_leon, "básico de Leon: o tiro e a faca"),
    "mira-da-beretta": (mira_da_beretta, "básico de Jill: o bipe da mira e os dois tiros"),
    "mega-buster": (mega_buster, "básico de Mega Man: as três balinhas do Mega Buster"),
}
