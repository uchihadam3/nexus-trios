"""Sons dos ataques básicos, lote zk (veja tools/vfx/familias_v2/basicos_zk.py).

O chute e o brilho de sininhos da lua da Sailor Moon, o bastão girando e o clique de máquina do Donatello, o chute e o
"plof" da pizza do Michelangelo, o chute com o rugido de fogo do Zuko, o fogo azul mais agudo com o estalo de raio da
Azula, os chicotes de carne estalando do Muzan, as garras e o pulso cinético do Pantera Negra e o simbionte molhado
e afiado da Carnificina. Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_f import _corte_curto
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, lo=200, hi=3000, g=0.5):
    n = n_de(seg)
    return passa(rosa(rng, n), lo, hi, 2) * sobe_e_some(n, 0.3, 1.3) * g + graos(rng, n, int(seg * 60), 0.0, 1.0, 1500, 6000, 0.006) * 0.3


def chute_lunar(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.16, 700, 4500, 0.8, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.6, 150), 0.18)
    for k, f in enumerate((1760, 2217, 2637, 3520)):
        poe(x, modal(n_de(0.4), f, rng=rng, **SINO) * env(n_de(0.4), 0.001, 0.25) * 0.045, 0.2 + 0.04 * k)
    return reverb(x, 0.45, 0.22, 9500)


def chute_e_bo_donatello(rng, v):
    x = _z(1.1)
    for k in range(4):
        poe(x, _whoosh(rng, 0.06, 900, 4000, 0.6, g=0.25), 0.0 + 0.05 * k)
    poe(x, _acerto(rng, v, 0.7, 130), 0.22)
    for k in range(3):
        n = n_de(0.03)
        poe(x, passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.001, 0.02) * 0.3, 0.26 + 0.05 * k)
    return reverb(x, 0.3, 0.14, 8000)


def chute_cowabunga(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.18, 600, 4000, 0.8, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.65, 140), 0.2)
    n = n_de(0.3)
    poe(x, seno(varre(400, 900, n), n) * env(n, 0.005, 0.2) * 0.06, 0.24)
    poe(x, baque(n_de(0.15), 300, 150, 0.04, 0.4) * 0.25, 0.7)
    return reverb(x, 0.35, 0.16, 8000)


def chute_de_fogo_zuko(rng, v):
    x = _z(1.2)
    poe(x, _fogo(rng, 0.45, 150, 2500, 0.6), 0.0)
    poe(x, _acerto(rng, v, 0.7, 120), 0.2)
    return reverb(x, 0.35, 0.16, 7000)


def chute_de_fogo_azul(rng, v):
    x = _z(1.2)
    poe(x, _fogo(rng, 0.45, 600, 6000, 0.55), 0.0)
    poe(x, _acerto(rng, v, 0.6, 140), 0.2)
    poe(x, _chiado(rng, 0.15, 3000, 11000, 0.004, 0.6), 0.2)
    return reverb(x, 0.35, 0.16, 9000)


def chicotes_de_carne_muzan(rng, v):
    x = _z(1.1)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 300, 2500, 0.85, g=0.35), 0.0 + 0.03 * k)
        poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.006) * 0.6, 0.16 + 0.03 * k)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 150, 1500, 2) * env(m, 0.003, 0.2) * 0.4, 0.2)
    return reverb(x, 0.3, 0.14, 6500)


def garras_de_vibranio(rng, v):
    x = _z(1.2)
    for k in range(2):
        poe(x, _corte_curto(rng, 0.1, 1800, 9000, 0.55), 0.02 + 0.1 * k)
    n = n_de(0.5)
    poe(x, (seno(varre(200, 600, n), n) * 0.6 + seno(varre(400, 1200, n), n) * 0.3) * sobe_e_some(n, 0.2, 1.3) * 0.12, 0.2)
    return reverb(x, 0.4, 0.2, 8000)


def laminas_simbiontes(rng, v):
    x = _z(1.2)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 200, 1800, 2) * sobe_e_some(n, 0.4, 1.2) * 0.4, 0.0)
    for k in range(5):
        poe(x, _corte_curto(rng, 0.07, 1500, 8000, 0.4), 0.04 + 0.03 * k)
    poe(x, graos(rng, n_de(0.35), 24, 0.0, 0.5, 400, 3000, 0.01) * 0.4, 0.18)
    return reverb(x, 0.35, 0.16, 6500)


SONS: dict = {
    "chute-lunar": (chute_lunar, "básico de Sailor Moon: o chute e os sininhos da lua"),
    "chute-e-bo-donatello": (chute_e_bo_donatello, "básico de Donatello: o bastão girando e o chute"),
    "chute-cowabunga": (chute_cowabunga, "básico de Michelangelo: o chute e a pizza voando"),
    "chute-de-fogo-zuko": (chute_de_fogo_zuko, "básico de Zuko: o chute com o rugido de fogo"),
    "chute-de-fogo-azul": (chute_de_fogo_azul, "básico de Azula: o fogo azul e o estalo de raio"),
    "chicotes-de-carne-muzan": (chicotes_de_carne_muzan, "básico de Muzan: os chicotes de carne estalando"),
    "garras-de-vibranio": (garras_de_vibranio, "básico de Pantera Negra: as garras e o pulso cinético"),
    "laminas-simbiontes": (laminas_simbiontes, "básico de Carnificina: o simbionte molhado e afiado"),
}
