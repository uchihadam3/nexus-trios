"""Sons dos ataques básicos, lote zm (veja tools/vfx/familias_v2/basicos_zm.py).

O círculo mágico e o raio fino da Zoltraak da Frieren, o bastão girando e o estouro cinético do Gambit, o vento em
espiral do Aang, o "bonk" e o "nhac" da cenoura do Pernalonga, os tapinhas desesperados do Salsicha, a trombada com o
"a-hyuck" do Pateta (o tombo e as estrelinhas), a carta voando e o brilho do Enigma do Yugi e o rugido de luz do Dragão
Branco do Kaiba. Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_f import _corte_curto
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def zoltraak_frieren(rng, v):
    x = _z(1.2)
    for k, f in enumerate((1047, 1319, 1568)):
        poe(x, modal(n_de(0.3), f, rng=rng, **SINO) * env(n_de(0.3), 0.001, 0.2) * 0.04, 0.0 + 0.04 * k)
    n = n_de(0.3)
    poe(x, (seno(varre(2600, 2000, n), n) + seno(varre(1300, 1000, n), n) * 0.5) * env(n, 0.002, 0.25) * 0.12, 0.14)
    poe(x, _acerto(rng, v, 0.4, 160), 0.22)
    return reverb(x, 0.5, 0.24, 9500)


def bastao_cinetico_gambit(rng, v):
    x = _z(1.2)
    for k in range(3):
        poe(x, _whoosh(rng, 0.07, 900, 4000, 0.6, g=0.25), 0.0 + 0.06 * k)
    poe(x, _acerto(rng, v, 0.7, 120), 0.22)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 200, 5000, 2) * env(n, 0.002, 0.25), 1.8) * 0.5, 0.22)
    poe(x, _chiado(rng, 0.3, 2500, 9000, 0.006, 0.35), 0.24)
    return reverb(x, 0.4, 0.18, 8000)


def bastao_de_ar_aang(rng, v):
    x = _z(1.2)
    for k in range(3):
        poe(x, _whoosh(rng, 0.08, 1000, 4000, 0.6, g=0.25), 0.0 + 0.06 * k)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * sobe_e_some(n, 0.4, 1.4) * 0.45, 0.1)
    return reverb(x, 0.45, 0.2, 9000)


def cenoura_do_pernalonga(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.14, 600, 3500, 0.85, g=0.35), 0.0)
    poe(x, baque(n_de(0.2), 400, 200, 0.05, 0.8) * 0.5, 0.18)
    poe(x, B._tapa(rng, n_de(0.05), 1500, 7000, 0.004) * 0.6, 0.18)
    poe(x, estalo(rng, n_de(0.06), 2000, 8000, 0.008) * 0.6, 0.42)
    poe(x, graos(rng, n_de(0.12), 8, 0.0, 1.0, 2000, 6000, 0.008) * 0.4, 0.44)
    return reverb(x, 0.25, 0.12, 9000)


def tapas_desesperados(rng, v):
    x = _z(1.1)
    for k in range(6):
        poe(x, B._tapa(rng, n_de(0.04), 1200, 7000, 0.004) * 0.5, 0.04 + 0.05 * k)
    n = n_de(0.25)
    poe(x, seno(varre(700, 1300, n), n) * env(n, 0.01, 0.2) * 0.05, 0.0)
    return reverb(x, 0.25, 0.12, 8500)


def trombada_do_pateta(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.18, 300, 2000, 0.85, g=0.45), 0.0)
    poe(x, satura(baque(n_de(0.4), 110, 50, 0.12, 0.9), 1.8) * 0.6, 0.2)
    poe(x, graos(rng, n_de(0.3), 12, 0.0, 1.0, 200, 2500, 0.02) * 0.4, 0.22)
    for k, f in enumerate((1568, 1976, 2349)):
        poe(x, modal(n_de(0.3), f, rng=rng, **SINO) * env(n_de(0.3), 0.001, 0.2) * 0.035, 0.3 + 0.08 * k)
    return reverb(x, 0.35, 0.16, 8000)


def carta_do_rei_dos_jogos(rng, v):
    x = _z(1.2)
    for k in range(4):
        n = n_de(0.04)
        poe(x, passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.001, 0.03) * 0.3, 0.0 + 0.04 * k)
    poe(x, _acerto(rng, v, 0.5, 160), 0.18)
    n = n_de(0.5)
    poe(x, (seno(392, n) + seno(587, n) * 0.6) * sobe_e_some(n, 0.15, 1.4) * 0.05, 0.18)
    return reverb(x, 0.5, 0.24, 8500)


def carta_do_dragao_branco(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.12, 900, 5000, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.6, 140), 0.14)
    n = n_de(0.6)
    poe(x, (seno(varre(180, 420, n), n) + seno(varre(270, 630, n), n) * 0.5) * sobe_e_some(n, 0.3, 1.3) * 0.12, 0.16)
    poe(x, passa(rosa(rng, n), 800, 6000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.3, 0.16)
    return reverb(x, 0.55, 0.26, 8500)


SONS: dict = {
    "zoltraak-frieren": (zoltraak_frieren, "básico de Frieren: o círculo mágico e a Zoltraak"),
    "bastao-cinetico-gambit": (bastao_cinetico_gambit, "básico de Gambit: o bastão e o estouro cinético"),
    "bastao-de-ar-aang": (bastao_de_ar_aang, "básico de Aang: o bastão e o vento em espiral"),
    "cenoura-do-pernalonga": (cenoura_do_pernalonga, "básico de Pernalonga: o bonk e o nhac da cenoura"),
    "tapas-desesperados": (tapas_desesperados, "básico de Salsicha: os tapinhas desesperados"),
    "trombada-do-pateta": (trombada_do_pateta, "básico de Pateta: a trombada e as estrelinhas"),
    "carta-do-rei-dos-jogos": (carta_do_rei_dos_jogos, "básico de Yugi: a carta e o brilho do Enigma"),
    "carta-do-dragao-branco": (carta_do_dragao_branco, "básico de Kaiba: a carta e o rugido de luz do Dragão Branco"),
}
