"""Sons dos ataques básicos, lote z (veja tools/vfx/familias_v2/basicos_z.py).

O soco de armadura com o bater de asas do Seiya, o soco gelado com o cristal tilintando do Hyoga, o soco em chamas
com o grito agudo de fogo do Ikki, os dois socos sobrepostos e o eco cósmico do Saga, o soco e o rugido curto do
Aiolia, o metal e o zumbido da magia do Destino, os três socos de luva da Tifa e a lâmina pesada arrastando e
batendo do Cabeça de Pirâmide. Tudo sintetizado.
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


def _asas(rng, seg=0.35, bat=9.0, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 300, 2500, 2) * np.clip(np.sin(2 * math.pi * bat * t), 0, 1) ** 2 * env(n, 0.02, seg * 0.6) * g


def soco_de_pegaso(rng, v):
    x = _z(1.05)
    poe(x, _whoosh(rng, 0.12, 500, 3400, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 0.95, 120), 0.13)
    poe(x, modal(n_de(0.35), 760, rng=rng, **METAL) * 0.1, 0.13)
    poe(x, _asas(rng, 0.45, 8, 0.3), 0.16)
    return reverb(x, 0.28, 0.13, 6500)


def soco_do_cisne(rng, v):
    x = _z(1.1)
    poe(x, _sopro(rng, 0.2, 3000, 10000, 0.25), 0.0)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.4), 0.02)
    poe(x, _acerto(rng, v, 0.95, 120), 0.15)
    for k in range(6):
        poe(x, _brilho(rng, 0.3, 2093 + 220 * k, 0.025, CRISTAL), 0.17 + 0.04 * k)
    return reverb(x, 0.35, 0.16, 8000)


def soco_da_fenix(rng, v):
    x = _z(1.1)
    n = n_de(0.3)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1600, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 12 * t)) * env(n, 0.05, 0.2) * 0.45, 0.0)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.4), 0.03)
    poe(x, _acerto(rng, v, 1.0, 115), 0.15)
    n = n_de(0.4)
    poe(x, seno(varre(1400, 2400, n, 1.4), n) * env(n, 0.03, 0.25) * 0.05, 0.17)
    poe(x, graos(rng, n_de(0.45), 26, 0.0, 0.4, 2000, 8000, 0.004) * 0.35, 0.17)
    return reverb(x, 0.35, 0.16, 5500)


def soco_de_gemeos(rng, v):
    x = _z(1.15)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.4), 0.0)
    poe(x, _acerto(rng, v, 0.9, 120), 0.15)
    poe(x, _acerto(rng, (v + 2) % 4, 0.6, 140), 0.18)
    n = n_de(0.6)
    poe(x, (seno(np.full(n, 220.0), n) + seno(np.full(n, 223.0), n)) * env(n, 0.05, 0.4) * 0.06, 0.16)
    for k, f in enumerate((1568, 1976, 2349)):
        poe(x, _brilho(rng, 0.45, f, 0.025, CRISTAL), 0.2 + 0.06 * k)
    return reverb(x, 0.45, 0.2, 6000)


def soco_do_leao_dourado(rng, v):
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.1, 700, 4200, 0.85, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 1.05, 115), 0.12)
    n = n_de(0.35)
    t = _t(n)
    rugido = satura(passa(rosa(rng, n), 90, 700, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * t)), 2.5) * env(n, 0.02, 0.25) * 0.35
    poe(x, rugido, 0.13)
    poe(x, estalo(rng, n_de(0.06), 2000, 9000, 0.008) * 0.45, 0.12)
    return reverb(x, 0.3, 0.14, 6000)


def soco_de_ferro_destino(rng, v):
    x = _z(1.15)
    poe(x, _whoosh(rng, 0.14, 400, 2800, 0.85, g=0.42), 0.0)
    poe(x, _acerto(rng, v, 0.9, 110), 0.15)
    poe(x, modal(n_de(0.5), 420 + 20 * v, rng=rng, **METAL) * 0.22, 0.15)
    n = n_de(0.55)
    t = _t(n)
    poe(x, seno(np.full(n, 330.0), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 6 * t)) * env(n, 0.05, 0.4) * 0.06, 0.17)
    poe(x, _brilho(rng, 0.5, 1047, 0.03, SINO), 0.18)
    return reverb(x, 0.4, 0.18, 5500)


def socos_de_luva_tifa(rng, v):
    x = _z(1.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.07, 800, 4000, 0.85, g=0.3), 0.1 * k)
        poe(x, B.soco_leve(rng, (v + k) % 4) * (0.5 + 0.2 * (k == 2)), 0.08 + 0.1 * k)
    poe(x, baque(n_de(0.2), 120, 60, 0.05, 0.5) * 0.4, 0.28)
    return reverb(x, 0.22, 0.1, 6500)


def grande_faca_piramide(rng, v):
    x = _z(1.35)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 300, 1800, 2) * env(n, 0.08, 0.15) * 0.25, 0.0)
    poe(x, _whoosh(rng, 0.22, 200, 1500, 0.9, g=0.55), 0.08)
    poe(x, _acerto(rng, v, 1.25, 70), 0.24)
    poe(x, modal(n_de(0.7), 210 + 10 * v, rng=rng, **METAL) * 0.3, 0.24)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.45, 1500, 7000, 0.004) * 0.45, 0.25)
    poe(x, baque(n_de(0.5), 60, 30, 0.15, 0.6) * 0.6, 0.24)
    return reverb(x, 0.45, 0.2, 4500)


SONS: dict = {
    "soco-de-pegaso": (soco_de_pegaso, "básico de Seiya: soco de armadura e o bater de asas"),
    "soco-do-cisne": (soco_do_cisne, "básico de Hyoga: o frio e os cristais de gelo tilintando"),
    "soco-da-fenix": (soco_da_fenix, "básico de Ikki: o soco em chamas e as brasas"),
    "soco-de-gemeos": (soco_de_gemeos, "básico de Saga: os dois socos e o eco cósmico"),
    "soco-do-leao-dourado": (soco_do_leao_dourado, "básico de Aiolia: o soco e o rugido curto"),
    "soco-de-ferro-destino": (soco_de_ferro_destino, "básico de Doutor Destino: o metal e o zumbido da magia"),
    "socos-de-luva-tifa": (socos_de_luva_tifa, "básico de Tifa: três socos curtos de luva"),
    "grande-faca-piramide": (grande_faca_piramide, "básico de Cabeça de Pirâmide: a lâmina pesada arrastando e batendo"),
}
