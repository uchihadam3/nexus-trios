"""Sons dos ataques básicos, lote zj (veja tools/vfx/familias_v2/basicos_zj.py).

A carga e o disparo do Z-Buster do Zero, o "fft" abafado do silenciador do Agente 47, o tiro e o zumbido da roupa HEV
do Gordon, o estrondo do revólver gigante do Hellboy, o chute com o estalo do salto da Yor, o chute pesado e o ruído
de carne da kagune do Kaneki, o giro e o estalo do caos do Shadow, e a metralhadora de chutes da Chun-Li. Tudo
sintetizado.
"""
from __future__ import annotations

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_f import _corte_curto
from sfx_basicos_g import _tiro_de_pistola
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def z_buster_carregado(rng, v):
    x = _z(1.1)
    n = n_de(0.16)
    poe(x, seno(varre(500, 1800, n), n) * sobe_e_some(n, 0.9, 1.2) * 0.08, 0.0)
    m = n_de(0.25)
    poe(x, (seno(varre(1500, 400, m), m) + 0.5 * passa(rosa(rng, m), 600, 6000, 2)) * env(m, 0.002, 0.18) * 0.2, 0.14)
    poe(x, _acerto(rng, v, 0.6, 130), 0.28)
    return reverb(x, 0.35, 0.16, 8500)


def tiro_silencioso_47(rng, v):
    x = _z(0.9)
    n = n_de(0.08)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.001, 0.05) * 0.6, 0.02)
    poe(x, B._tapa(rng, n_de(0.03), 600, 3000, 0.004) * 0.3, 0.02)
    poe(x, _acerto(rng, v, 0.45, 150), 0.18)
    return reverb(x, 0.2, 0.08, 6000)


def tiro_lambda_gordon(rng, v):
    x = _z(1.1)
    poe(x, _tiro_de_pistola(rng, v, 1.0) * 0.7, 0.0)
    n = n_de(0.35)
    poe(x, seno(varre(800, 1200, n), n) * sobe_e_some(n, 0.2, 1.4) * 0.04, 0.16)
    poe(x, _chiado(rng, 0.3, 2000, 8000, 0.008, 0.35), 0.16)
    return reverb(x, 0.35, 0.15, 8000)


def samaritano_hellboy(rng, v):
    x = _z(1.3)
    poe(x, satura(baque(n_de(0.6), 80, 30, 0.2, 1.0), 2.4) * 0.8, 0.02)
    poe(x, satura(passa(rosa(rng, n_de(0.5)), 80, 6000, 2) * env(n_de(0.5), 0.001, 0.25), 2.2) * 0.7, 0.02)
    poe(x, _acerto(rng, v, 0.8, 90), 0.16)
    return reverb(x, 0.5, 0.22, 6000)


def chute_espinho_yor(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.18, 600, 4000, 0.8, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 0.7, 140), 0.2)
    poe(x, modal(n_de(0.25), 3300, rng=rng, **METAL) * env(n_de(0.25), 0.001, 0.12) * 0.06, 0.2)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.2, 1.5) * 0.15, 0.24)
    return reverb(x, 0.35, 0.16, 8500)


def chute_ghoul_kaneki(rng, v):
    x = _z(1.2)
    n = n_de(0.2)
    poe(x, seno(varre(200, 120, n), n) * sobe_e_some(n, 0.5, 1.2) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.2, 300, 2500, 0.85, g=0.6), 0.02)
    poe(x, _acerto(rng, v, 0.9, 100), 0.22)
    m = n_de(0.3)
    poe(x, satura(passa(rosa(rng, m), 150, 1200, 2) * env(m, 0.003, 0.2), 2.0) * 0.5, 0.2)
    return reverb(x, 0.35, 0.16, 6500)


def chute_do_caos_shadow(rng, v):
    x = _z(1.1)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 800, 6000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.0)
    poe(x, _acerto(rng, v, 0.75, 130), 0.22)
    poe(x, _chiado(rng, 0.3, 2500, 10000, 0.005, 0.5), 0.22)
    return reverb(x, 0.35, 0.16, 8500)


def chute_relampago_chunli(rng, v):
    x = _z(1.1)
    for k in range(8):
        poe(x, B._tapa(rng, n_de(0.04), 900, 6000, 0.004) * (0.5 + 0.1 * (k % 2)), 0.08 + 0.045 * k)
        poe(x, _whoosh(rng, 0.05, 1500, 6000, 0.6, g=0.12), 0.06 + 0.045 * k)
    poe(x, _acerto(rng, v, 0.6, 140), 0.44)
    return reverb(x, 0.3, 0.14, 8500)


SONS: dict = {
    "z-buster-carregado": (z_buster_carregado, "básico de Zero: a carga e o disparo do Z-Buster"),
    "tiro-silencioso-47": (tiro_silencioso_47, "básico de Agente 47: o tiro abafado do silenciador"),
    "tiro-lambda-gordon": (tiro_lambda_gordon, "básico de Gordon Freeman: o tiro e o zumbido da roupa HEV"),
    "samaritano-hellboy": (samaritano_hellboy, "básico de Hellboy: o estrondo do revólver Samaritano"),
    "chute-espinho-yor": (chute_espinho_yor, "básico de Yor: o chute e o estalo do salto"),
    "chute-ghoul-kaneki": (chute_ghoul_kaneki, "básico de Kaneki: o chute pesado e a kagune"),
    "chute-do-caos-shadow": (chute_do_caos_shadow, "básico de Shadow: o giro e o estalo do caos"),
    "chute-relampago-chunli": (chute_relampago_chunli, "básico de Chun-Li: a metralhadora de chutes"),
}
