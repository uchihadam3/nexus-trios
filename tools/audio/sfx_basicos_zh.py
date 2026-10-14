"""Sons dos ataques básicos, lote zh (veja tools/vfx/familias_v2/basicos_zh.py).

O golpe com "plim" de desenho do Finn, as três batidinhas de madeira e o chicote do rabo do Splinter, o corte e o
acorde da joia da She-Ra, o "snikt" e o rasgo das garras do Wolverine, as katanas e a risadinha do Deadpool, o bastão
quicando e o eco do radar do Demolidor, as ilusões sumindo e a adaga do Loki, e a haste negra com o zumbido do
Rinnegan do Pain. Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_f import _corte_curto
from sfx_basicos_h import _shing
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def espada_do_heroi_finn(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.18, 500, 3500, 0.7, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.7, 140), 0.18)
    for k, f in enumerate((1319, 1760, 2349)):
        n = n_de(0.12)
        poe(x, seno(f, n) * env(n, 0.002, 0.08) * 0.06, 0.22 + 0.05 * k)
    return reverb(x, 0.35, 0.16, 9000)


def bengala_do_mestre(rng, v):
    x = _z(1.1)
    for k in range(3):
        poe(x, modal(n_de(0.15), 520 + 40 * k, rng=rng, razoes=[1, 2.7, 5.4], quedas=[0.05, 0.03, 0.02]) * 0.25, 0.08 + 0.1 * k)
        poe(x, B._tapa(rng, n_de(0.04), 900, 5000, 0.004) * 0.5, 0.08 + 0.1 * k)
    poe(x, _whoosh(rng, 0.12, 1500, 7000, 0.6, g=0.35), 0.32)
    return reverb(x, 0.3, 0.14, 8000)


def espada_da_protecao_shera(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.2, 500, 3500, 0.7, g=0.5), 0.0)
    poe(x, _corte_curto(rng, 0.14, 1600, 8500, 0.6), 0.2)
    n = n_de(0.7)
    poe(x, (seno(523, n) + seno(659, n) * 0.8 + seno(784, n) * 0.6) * sobe_e_some(n, 0.15, 1.4) * 0.035, 0.2)
    poe(x, _brilho(rng, 0.5, 2093, 0.05, CRISTAL), 0.22)
    return reverb(x, 0.5, 0.24, 9000)


def garras_de_adamantium(rng, v):
    x = _z(1.1)
    n = n_de(0.08)
    poe(x, passa(rosa(rng, n), 3000, 11000, 2) * env(n, 0.001, 0.05) * 0.5, 0.0)
    poe(x, modal(n_de(0.3), 3600, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.15) * 0.06, 0.0)
    poe(x, _whoosh(rng, 0.12, 700, 4000, 0.8, g=0.4), 0.06)
    for k in range(3):
        poe(x, _corte_curto(rng, 0.1, 1500, 8000, 0.45), 0.18 + 0.02 * k)
    return reverb(x, 0.3, 0.14, 8000)


def katanas_e_piadas(rng, v):
    x = _z(1.2)
    for k in range(2):
        poe(x, _corte_curto(rng, 0.1, 1800, 9000, 0.55), 0.02 + 0.06 * k)
    for k in range(4):
        n = n_de(0.07)
        poe(x, seno(420 + 60 * (k % 2), n) * env(n, 0.005, 0.05) * 0.08, 0.26 + 0.08 * k)
    return reverb(x, 0.3, 0.15, 8000)


def bastao_de_ricochete(rng, v):
    x = _z(1.2)
    for k in range(3):
        poe(x, _whoosh(rng, 0.06, 1200, 4000, 0.6, g=0.25), 0.02 + 0.06 * k)
    poe(x, _acerto(rng, v, 0.7, 140), 0.2)
    poe(x, B._tapa(rng, n_de(0.05), 1200, 6000, 0.004) * 0.4, 0.5)
    for k in range(3):
        n = n_de(0.25)
        poe(x, seno(900 - 150 * k, n) * env(n, 0.002, 0.15) * 0.04, 0.2 + 0.1 * k)
    return reverb(x, 0.5, 0.24, 7000)


def adaga_das_ilusoes(rng, v):
    x = _z(1.2)
    n = n_de(0.3)
    poe(x, seno(varre(700, 1100, n), n) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    for k in range(2):
        m = n_de(0.25)
        poe(x, passa(rosa(rng, m), 400, 3000, 2) * sobe_e_some(m, 0.2, 1.5) * 0.3, 0.18 + 0.04 * k)
    poe(x, _corte_curto(rng, 0.1, 2200, 9500, 0.6), 0.28)
    poe(x, _acerto(rng, v, 0.5, 150), 0.3)
    return reverb(x, 0.45, 0.22, 7500)


def haste_negra_pain(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.16, 600, 4000, 0.85, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.6, 100), 0.16)
    n = n_de(0.7)
    poe(x, (seno(110, n) + seno(165, n) * 0.6) * sobe_e_some(n, 0.2, 1.4) * 0.08, 0.16)
    poe(x, seno(varre(1200, 600, n), n) * sobe_e_some(n, 0.3, 1.4) * 0.025, 0.18)
    return reverb(x, 0.55, 0.26, 6500)


SONS: dict = {
    "espada-do-heroi-finn": (espada_do_heroi_finn, "básico de Finn: o golpe e o plim de desenho"),
    "bengala-do-mestre": (bengala_do_mestre, "básico de Mestre Splinter: três batidinhas de madeira e o rabo"),
    "espada-da-protecao-shera": (espada_da_protecao_shera, "básico de She-Ra: o corte e o acorde da joia"),
    "garras-de-adamantium": (garras_de_adamantium, "básico de Wolverine: o snikt e o rasgo das garras"),
    "katanas-e-piadas": (katanas_e_piadas, "básico de Deadpool: as katanas e a risadinha"),
    "bastao-de-ricochete": (bastao_de_ricochete, "básico de Demolidor: o bastão quicando e o eco do radar"),
    "adaga-das-ilusoes": (adaga_das_ilusoes, "básico de Loki: as ilusões sumindo e a adaga"),
    "haste-negra-pain": (haste_negra_pain, "básico de Pain: a haste negra e o zumbido do Rinnegan"),
}
