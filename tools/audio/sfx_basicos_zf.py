"""Sons dos ataques básicos, lote zf (veja tools/vfx/familias_v2/basicos_zf.py).

O estalo da lâmina oculta do Ezio, a corrente chacoalhando e o fogo do Scorpion, o golpe com o brilho de sininhos da
Keyblade do Sora, o corte limpo e os bipes digitais da 2B, os três cortes leves e o sopro da flor da Malenia, os vultos
e o corte em zigue-zague do Hayabusa, a areia do tempo voltando do Príncipe e os cortes de uma vez do Hiei. Tudo
sintetizado.
"""
from __future__ import annotations

import numpy as np

from sfx_basicos_f import _corte_curto
from sfx_basicos_h import _shing
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def lamina_do_credo_ezio(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.14, 500, 3000, 0.8, g=0.4), 0.0)
    n = n_de(0.05)
    poe(x, passa(rosa(rng, n), 2500, 10000, 2) * env(n, 0.001, 0.03) * 0.6, 0.12)
    poe(x, modal(n_de(0.2), 3400, rng=rng, **METAL) * env(n_de(0.2), 0.001, 0.1) * 0.06, 0.12)
    poe(x, _acerto(rng, v, 0.6, 140), 0.18)
    return reverb(x, 0.3, 0.14, 8000)


def lanca_corrente_scorpion(rng, v):
    x = _z(1.2)
    poe(x, graos(rng, n_de(0.25), 22, 0.0, 1.0, 2500, 8000, 0.006) * 0.5, 0.0)
    poe(x, _acerto(rng, v, 0.7, 120), 0.16)
    poe(x, graos(rng, n_de(0.2), 18, 0.0, 1.0, 2000, 7000, 0.006) * 0.45, 0.3)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 150, 2500, 2) * sobe_e_some(n, 0.3, 1.4) * 0.5, 0.18)
    return reverb(x, 0.35, 0.16, 6500)


def keyblade_sora(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.2, 400, 3000, 0.7, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.7, 130), 0.2)
    for k, f in enumerate((1568, 1976, 2349, 3136)):
        poe(x, modal(n_de(0.4), f, rng=rng, **SINO) * env(n_de(0.4), 0.001, 0.25) * 0.05, 0.22 + 0.05 * k)
    return reverb(x, 0.45, 0.22, 9000)


def katana_da_2b(rng, v):
    x = _z(1.1)
    for k in range(2):
        n = n_de(0.04)
        poe(x, seno(1760 + 440 * k, n) * env(n, 0.001, 0.03) * 0.08, 0.0 + 0.05 * k)
    poe(x, _corte_curto(rng, 0.12, 2500, 10000, 0.7), 0.06)
    poe(x, _shing(rng, 0.35, 3200, 0.12, 0.3), 0.08)
    for k in range(6):
        n = n_de(0.03)
        poe(x, seno(2000 + 300 * k, n) * env(n, 0.001, 0.02) * 0.05, 0.24 + 0.04 * k)
    return reverb(x, 0.35, 0.16, 9500)


def flor_escarlate_malenia(rng, v):
    x = _z(1.3)
    for k in range(3):
        poe(x, _corte_curto(rng, 0.08, 2200, 9500, 0.5), 0.0 + 0.08 * k)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 400, 3000, 2) * sobe_e_some(n, 0.25, 1.6) * 0.35, 0.26)
    poe(x, (seno(330, n) + seno(392, n) * 0.6) * sobe_e_some(n, 0.3, 1.5) * 0.03, 0.26)
    return reverb(x, 0.55, 0.26, 7000)


def corte_izuna_hayabusa(rng, v):
    x = _z(1.1)
    for k in range(3):
        poe(x, _whoosh(rng, 0.08, 1200, 6000, 0.6, g=0.3), 0.0 + 0.04 * k)
    for k in range(3):
        poe(x, _corte_curto(rng, 0.07, 2200, 10000, 0.55), 0.13 + 0.04 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * sobe_e_some(n, 0.2, 1.5) * 0.3, 0.3)
    return reverb(x, 0.3, 0.15, 8000)


def adaga_de_areia_principe(rng, v):
    x = _z(1.4)
    poe(x, _corte_curto(rng, 0.12, 1800, 8500, 0.65), 0.02)
    poe(x, graos(rng, n_de(0.7), 60, 0.0, 0.8, 3000, 9000, 0.004) * 0.35, 0.18)
    n = n_de(0.7)
    poe(x, seno(varre(1600, 500, n), n) * sobe_e_some(n, 0.6, 1.3) * 0.04, 0.2)
    return reverb(x, 0.55, 0.25, 8000)


def corte_negro_hiei(rng, v):
    x = _z(1.1)
    n = n_de(0.15)
    poe(x, seno(varre(300, 900, n), n) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    for k in range(6):
        poe(x, _corte_curto(rng, 0.05, 2500, 11000, 0.45), 0.16 + 0.006 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.3, 1.4) * 0.35, 0.2)
    return reverb(x, 0.35, 0.18, 7000)


SONS: dict = {
    "lamina-do-credo-ezio": (lamina_do_credo_ezio, "básico de Ezio: o estalo da lâmina oculta"),
    "lanca-corrente-scorpion": (lanca_corrente_scorpion, "básico de Scorpion: a corrente chacoalhando e o fogo"),
    "keyblade-sora": (keyblade_sora, "básico de Sora: o golpe e os sininhos da Keyblade"),
    "katana-da-2b": (katana_da_2b, "básico de 2B: o corte limpo e os bipes digitais"),
    "flor-escarlate-malenia": (flor_escarlate_malenia, "básico de Malenia: três cortes leves e a flor abrindo"),
    "corte-izuna-hayabusa": (corte_izuna_hayabusa, "básico de Ryu Hayabusa: os vultos e o corte em zigue-zague"),
    "adaga-de-areia-principe": (adaga_de_areia_principe, "básico do Príncipe da Pérsia: a areia do tempo voltando"),
    "corte-negro-hiei": (corte_negro_hiei, "básico de Hiei: os cortes de uma vez e a chama negra"),
}
