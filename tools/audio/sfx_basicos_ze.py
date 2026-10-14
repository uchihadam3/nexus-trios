"""Sons dos ataques básicos, lote ze (veja tools/vfx/familias_v2/basicos_ze.py).

O corte com a onda batendo do Tanjiro, o peso da Zangetsu e o rugido grave do Ichigo, o espelho trincando e o corte
calmo do Aizen, o cabo de manobra e as lâminas girando do Levi, os dois cortes secos e o respingo do Blade, o
"shing" longo e frio da Masamune do Sephiroth, o saque da Yamato e os cortes no ar do Vergil, e o zumbido elétrico da
lâmina de alta frequência do Raiden. Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

from sfx_basicos_f import _corte_curto
from sfx_basicos_h import _shing
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SR, VIDRO, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def corte_da_agua_tanjiro(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.2, 500, 3500, 0.7, g=0.5), 0.0)
    poe(x, _corte_curto(rng, 0.16, 1800, 8000, 0.65), 0.18)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * sobe_e_some(n, 0.25, 1.4) * 0.45, 0.14)
    poe(x, graos(rng, n_de(0.4), 26, 0.0, 0.3, 1500, 7000, 0.01) * 0.35, 0.24)
    return reverb(x, 0.35, 0.18, 8000)


def corte_da_zangetsu(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.24, 180, 1400, 0.75, g=0.75), 0.0)
    poe(x, _acerto(rng, v, 0.85, 80), 0.2)
    poe(x, _corte_curto(rng, 0.2, 900, 5000, 0.6), 0.2)
    n = n_de(0.5)
    poe(x, satura(seno(varre(70, 40, n), n), 2.4) * env(n, 0.01, 0.35) * 0.35, 0.2)
    return reverb(x, 0.4, 0.2, 6000)


def espelho_partido_aizen(rng, v):
    x = _z(1.3)
    n = n_de(0.35)
    poe(x, seno(varre(900, 1300, n), n) * sobe_e_some(n, 0.5, 1.2) * 0.04, 0.0)
    for k in range(5):
        poe(x, modal(n_de(0.4), 2400 + 400 * k, rng=rng, **VIDRO) * env(n_de(0.4), 0.001, 0.2) * 0.07, 0.14 + 0.02 * k)
    poe(x, graos(rng, n_de(0.5), 40, 0.0, 0.5, 3000, 11000, 0.006) * 0.4, 0.3)
    poe(x, _shing(rng, 0.5, 3000, 0.18, 0.3), 0.36)
    return reverb(x, 0.6, 0.28, 9000)


def laminas_giratorias_levi(rng, v):
    x = _z(1.1)
    n = n_de(0.14)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * env(n, 0.002, 0.1) * 0.3, 0.0)
    poe(x, modal(n_de(0.1), 3200, rng=rng, **METAL) * 0.05, 0.02)
    for k in range(4):
        poe(x, _whoosh(rng, 0.09, 900, 5200, 0.6, g=0.35), 0.08 + 0.07 * k)
    for k in range(2):
        poe(x, _corte_curto(rng, 0.11, 2000, 9000, 0.55), 0.16 + 0.12 * k)
    return reverb(x, 0.3, 0.15, 9000)


def corte_de_prata_blade(rng, v):
    x = _z(1.1)
    for k in range(2):
        poe(x, _corte_curto(rng, 0.12, 1600, 8500, 0.7), 0.02 + 0.14 * k)
        poe(x, _brilho(rng, 0.3, 3000 + 400 * k, 0.05, METAL), 0.04 + 0.14 * k)
    poe(x, _acerto(rng, v, 0.6, 120), 0.22)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 300, 2200, 2) * env(n, 0.004, 0.2) * 0.35, 0.24)
    return reverb(x, 0.3, 0.15, 7000)


def masamune_sephiroth(rng, v):
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.14, 1200, 7000, 0.5, g=0.45), 0.0)
    poe(x, _shing(rng, 0.9, 2200, 0.24, 0.6), 0.12)
    n = n_de(0.9)
    poe(x, (seno(220, n) + seno(330, n) * 0.6) * sobe_e_some(n, 0.4, 1.4) * 0.025, 0.2)
    return reverb(x, 0.7, 0.3, 7000)


def corte_da_yamato(rng, v):
    x = _z(1.3)
    poe(x, modal(n_de(0.08), 2600, rng=rng, **METAL) * 0.06, 0.0)
    poe(x, _corte_curto(rng, 0.08, 3000, 11000, 0.6), 0.02)
    for k in range(6):
        poe(x, _corte_curto(rng, 0.07, 2200, 10000, 0.35), 0.24 + 0.025 * k)
    poe(x, modal(n_de(0.35), 1800, rng=rng, **METAL) * env(n_de(0.35), 0.001, 0.2) * 0.07, 0.42)
    return reverb(x, 0.45, 0.22, 9000)


def lamina_hf_raiden(rng, v):
    x = _z(1.2)
    n = n_de(0.3)
    poe(x, seno(varre(400, 1600, n), n) * sobe_e_some(n, 0.6, 1.2) * 0.06, 0.0)
    poe(x, _chiado(rng, 0.4, 2000, 9000, 0.005, 0.5), 0.04)
    poe(x, _corte_curto(rng, 0.14, 1500, 8000, 0.7), 0.18)
    poe(x, graos(rng, n_de(0.4), 30, 0.0, 0.3, 2500, 10000, 0.005) * 0.4, 0.2)
    return reverb(x, 0.3, 0.15, 8000)


SONS: dict = {
    "corte-da-agua-tanjiro": (corte_da_agua_tanjiro, "básico de Tanjiro: o corte e a onda da Respiração da Água"),
    "corte-da-zangetsu": (corte_da_zangetsu, "básico de Ichigo: o peso da Zangetsu e o rugido grave"),
    "espelho-partido-aizen": (espelho_partido_aizen, "básico de Aizen: o espelho trincando e o corte calmo"),
    "laminas-giratorias-levi": (laminas_giratorias_levi, "básico de Levi: o cabo de manobra e as lâminas girando"),
    "corte-de-prata-blade": (corte_de_prata_blade, "básico de Blade: dois cortes secos e o respingo"),
    "masamune-sephiroth": (masamune_sephiroth, "básico de Sephiroth: o shing longo e frio da Masamune"),
    "corte-da-yamato": (corte_da_yamato, "básico de Vergil: o saque da Yamato e os cortes no ar"),
    "lamina-hf-raiden": (lamina_hf_raiden, "básico de Raiden: o zumbido elétrico da lâmina de alta frequência"),
}
