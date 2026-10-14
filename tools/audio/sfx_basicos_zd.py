"""Sons dos ataques básicos, lote zd (veja tools/vfx/familias_v2/basicos_zd.py).

Os três riscos metálicos da Garra de Thundera do Lion-O, o tapinha minúsculo com estalo enorme do Stewie, a garra do robô
do Macaco Louco (servo, vapor e aperto), o punho fantasma do Danny (zunido etéreo que fica sólido), o soco pesado do
Akuma com o ronco escuro do Satsui, o moinho de socos furiosos do Donald, o "tóin" do martelinho do Jerry e o braço de
borracha esticando do Majin Boo. Tudo sintetizado.
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


def soco_da_garra_thundera(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.12, 600, 4000, 0.9, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.95, 120), 0.15)
    for k in range(3):
        n = n_de(0.12)
        poe(x, passa(rosa(rng, n), 3000, 11000, 2) * env(n, 0.002, 0.09) * 0.32, 0.16 + 0.035 * k)
        poe(x, modal(n_de(0.25), 1900 + 260 * k, rng=rng, **METAL) * 0.05, 0.16 + 0.035 * k)
    return reverb(x, 0.28, 0.13, 7500)


def tapinha_do_stewie(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.08, 1500, 6000, 0.7, g=0.25), 0.04)
    poe(x, B._tapa(rng, n_de(0.06), 1800, 9000, 0.004) * 1.1, 0.17)
    poe(x, baque(n_de(0.22), 160, 70, 0.05, 0.5) * 0.5, 0.17)
    return reverb(x, 0.35, 0.16, 9000)


def soco_do_robo_mojo(rng, v):
    x = _z(1.15)
    n = n_de(0.22)
    poe(x, (satura(seno(varre(180, 420, n, 1.0), n), 3.0) * env(n, 0.01, 0.15)) * 0.06, 0.0)
    poe(x, _chiado(rng, 0.3, 0.25), 0.05)
    poe(x, _acerto(rng, v, 1.0, 110), 0.2)
    poe(x, modal(n_de(0.3), 640, rng=rng, **METAL) * 0.1, 0.22)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 5000) * 0.25, 0.24 + 0.03 * k)
    return reverb(x, 0.25, 0.12, 7000)


def soco_fantasma_danny(rng, v):
    x = _z(1.15)
    n = n_de(0.3)
    t = _t(n)
    poe(x, seno(varre(500, 900, n, 1.0), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 9 * t)) * env(n, 0.04, 0.2) * 0.06, 0.0)
    poe(x, _whoosh(rng, 0.14, 800, 5000, 0.8, g=0.35), 0.04)
    poe(x, _acerto(rng, v, 0.9, 130), 0.19)
    poe(x, _brilho(rng, 0.4, 1320, 0.04, CRISTAL), 0.21)
    return reverb(x, 0.4, 0.18, 8000)


def soco_do_satsui(rng, v):
    x = _z(1.15)
    n = n_de(0.35)
    poe(x, satura(passa(rosa(rng, n), 60, 400, 2), 2.0) * env(n, 0.05, 0.25) * 0.4, 0.0)
    poe(x, _whoosh(rng, 0.12, 500, 3500, 0.9, g=0.5), 0.05)
    poe(x, _acerto(rng, v, 1.15, 95), 0.17)
    poe(x, baque(n_de(0.35), 90, 45, 0.08, 0.35) * 0.6, 0.17)
    return reverb(x, 0.32, 0.15, 6000)


def pancada_furiosa_donald(rng, v):
    x = _z(1.2)
    for k in range(4):
        poe(x, _whoosh(rng, 0.07, 700, 4000, 0.6, g=0.25), 0.02 + 0.07 * k)
        poe(x, B.soco_leve(rng, v) * (0.35 + 0.05 * k), 0.08 + 0.07 * k)
    n = n_de(0.18)
    poe(x, satura(seno(varre(600, 380, n, 1.0), n), 4.0) * env(n, 0.01, 0.12) * 0.05, 0.1)
    return reverb(x, 0.22, 0.11, 7000)


def martelinho_do_jerry(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.1, 900, 4500, 0.8, g=0.3), 0.04)
    poe(x, modal(n_de(0.3), 520, rng=rng, **SINO) * 0.12, 0.17)
    n = n_de(0.35)
    poe(x, seno(varre(300, 900, n, 0.8), n) * env(n, 0.005, 0.3) * 0.08, 0.17)
    poe(x, baque(n_de(0.15), 240, 120, 0.04, 0.6) * 0.45, 0.17)
    for k in range(3):
        poe(x, _brilho(rng, 0.2, 2093 + 260 * k, 0.025, CRISTAL), 0.3 + 0.06 * k)
    return reverb(x, 0.25, 0.12, 8500)


def soco_de_borracha_buu(rng, v):
    x = _z(1.2)
    n = n_de(0.25)
    poe(x, seno(varre(150, 420, n, 1.2), n) * env(n, 0.02, 0.18) * 0.08, 0.0)
    poe(x, baque(n_de(0.25), 200, 90, 0.05, 0.6) * 0.6, 0.2)
    poe(x, B.soco_leve(rng, v) * 0.5, 0.2)
    n = n_de(0.3)
    poe(x, seno(varre(420, 140, n, 1.0), n) * env(n, 0.01, 0.25) * 0.07, 0.24)
    return reverb(x, 0.28, 0.13, 7000)


SONS: dict = {
    "soco-da-garra-thundera": (soco_da_garra_thundera, "básico de Lion-O: a Garra de Thundera riscando três vezes"),
    "tapinha-do-stewie": (tapinha_do_stewie, "básico de Stewie: o tapinha e o estalo desproporcional"),
    "soco-do-robo-mojo": (soco_do_robo_mojo, "básico de Macaco Louco: o servo, o vapor e a garra apertando"),
    "soco-fantasma-danny": (soco_fantasma_danny, "básico de Danny Phantom: o zunido fantasma que fica sólido"),
    "soco-do-satsui": (soco_do_satsui, "básico de Akuma: o ronco escuro e o soco pesado"),
    "pancada-furiosa-donald": (pancada_furiosa_donald, "básico de Pato Donald: o moinho de socos furiosos"),
    "martelinho-do-jerry": (martelinho_do_jerry, "básico de Jerry: o tóin do martelinho"),
    "soco-de-borracha-buu": (soco_de_borracha_buu, "básico de Majin Boo: o braço de borracha esticando e voltando"),
}
