"""Sons dos ataques básicos, lote v (veja tools/vfx/familias_v2/basicos_v.py).

O jab abafado de luva do Saitama com o "pow" de desenho, os dois impactos do Punho Divergente do Yuji, a sombra
borbulhando do Megumi, o estalo seco da mão em faca do Sukuna, o cristal tilintando do Eren, a aura de Nen
chiando do Gon, a corrente tilintando do Kurapika e o metal com o estalo azul da alquimia do Edward.
Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, seno, varre


def _t(n):
    return np.arange(n) / SR


def jab_de_luva_vermelha(rng, v):
    """Saitama: um jab abafado de luva e o "pow" de desenho animado, curto e sem drama."""
    x = _z(0.8)
    poe(x, _whoosh(rng, 0.1, 600, 3000, 0.85, g=0.35), 0.0)
    poe(x, passa(rosa(rng, n_de(0.08)), 200, 1800, 2) * env(n_de(0.08), 0.002, 0.04) * 0.8, 0.11)
    poe(x, baque(n_de(0.25), 180, 70, 0.06, 0.6) * 0.7, 0.11)
    n = n_de(0.18)
    poe(x, seno(varre(520, 260, n, 1.2), n) * env(n, 0.005, 0.12) * 0.1, 0.12)
    return reverb(x, 0.18, 0.08, 6000)


def soco_divergente(rng, v):
    """Yuji: o soco e, um instante depois, o segundo impacto da energia que chega atrasada, mais grave e estalado."""
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 0.75, 130), 0.13)
    poe(x, _acerto(rng, (v + 1) % 4, 1.05, 90), 0.22)
    poe(x, _chiado(rng, 0.25, 1200, 7000, 0.004, 0.35), 0.22)
    poe(x, baque(n_de(0.3), 80, 40, 0.08, 0.5) * 0.45, 0.22)
    return reverb(x, 0.28, 0.13, 6000)


def soco_das_sombras(rng, v):
    """Megumi: a sombra borbulha e engole o som, o soco sai dela e a tinta escura respinga."""
    x = _z(1.0)
    n = n_de(0.25)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 120, 700, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * t)) * env(n, 0.04, 0.18) * 0.45, 0.0)
    poe(x, _whoosh(rng, 0.13, 300, 2200, 0.85, g=0.4), 0.05)
    poe(x, _acerto(rng, v, 0.95, 105), 0.17)
    poe(x, graos(rng, n_de(0.35), 18, 0.0, 0.3, 400, 2400, 0.012) * 0.5, 0.18)
    return reverb(x, 0.3, 0.15, 4500)


def golpe_de_mao_sukuna(rng, v):
    """Sukuna: o ar rasgado pela mão em faca, um estalo seco e o "tsk" fino do risco."""
    x = _z(0.8)
    poe(x, _whoosh(rng, 0.12, 1200, 6000, 0.8, g=0.5), 0.0)
    poe(x, B._tapa(rng, n_de(0.06), 1800, 7000, 0.006) * 0.9, 0.14)
    poe(x, estalo(rng, n_de(0.05), 2500, 9000, 0.004) * 0.6, 0.14)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 4000, 11000, 2) * env(n, 0.002, 0.08) * 0.3, 0.15)
    poe(x, baque(n_de(0.15), 140, 70, 0.04, 0.5) * 0.35, 0.14)
    return reverb(x, 0.22, 0.1, 7000)


def soco_endurecido(rng, v):
    """Eren: o cristal estala ao endurecer, o soco bate duro e as lascas tilintam caindo."""
    x = _z(1.05)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 3000, 9000, 0.003) * 0.3, 0.06 + 0.03 * k)
    poe(x, _whoosh(rng, 0.14, 400, 3000, 0.85, g=0.45), 0.02)
    poe(x, _acerto(rng, v, 1.05, 110), 0.16)
    for k in range(5):
        poe(x, modal(n_de(0.25), 2200 + 380 * k, rng=rng, **VIDRO) * 0.06, 0.2 + 0.05 * k)
    return reverb(x, 0.3, 0.14, 7000)


def soco_do_gon(rng, v):
    """Gon: a aura de Nen chia subindo, o soco cheio e o estouro redondo."""
    x = _z(0.95)
    n = n_de(0.22)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * env(n, 0.08, 0.1) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.13, 450, 3200, 0.85, g=0.45), 0.04)
    poe(x, _acerto(rng, v, 1.05, 120), 0.17)
    poe(x, baque(n_de(0.3), 110, 45, 0.08, 0.6) * 0.45, 0.17)
    poe(x, _sopro(rng, 0.35, 300, 2400, 0.3), 0.18)
    return reverb(x, 0.28, 0.13, 6000)


def soco_da_corrente(rng, v):
    """Kurapika: a corrente tilintando no balanço, o soco e os elos estalando no impacto."""
    x = _z(1.0)
    for k in range(4):
        poe(x, modal(n_de(0.12), 1800 + 300 * (k % 2), rng=rng, **METAL) * 0.07, 0.02 + 0.04 * k)
    poe(x, _whoosh(rng, 0.13, 500, 3200, 0.85, g=0.42), 0.02)
    poe(x, _acerto(rng, v, 0.95, 120), 0.15)
    for k in range(6):
        poe(x, modal(n_de(0.15), 2100 + 260 * k, rng=rng, **METAL) * 0.06, 0.16 + 0.025 * k)
    return reverb(x, 0.25, 0.12, 7000)


def soco_de_automail(rng, v):
    """Edward: o braço de metal range, o soco bate com peso de aço e a alquimia estala azul."""
    x = _z(1.0)
    n = n_de(0.12)
    poe(x, seno(varre(180, 420, n, 1.3), n) * env(n, 0.01, 0.08) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.13, 450, 3000, 0.85, g=0.42), 0.02)
    poe(x, _acerto(rng, v, 0.85, 115), 0.15)
    poe(x, modal(n_de(0.45), 480 + 25 * v, rng=rng, **METAL) * 0.2, 0.15)
    poe(x, _chiado(rng, 0.3, 2000, 10000, 0.004, 0.4), 0.17)
    poe(x, _brilho(rng, 0.3, 2093, 0.03, CRISTAL), 0.18)
    return reverb(x, 0.25, 0.12, 6500)


SONS: dict = {
    "jab-de-luva-vermelha": (jab_de_luva_vermelha, "básico de Saitama: jab abafado de luva e o pow de desenho"),
    "soco-divergente": (soco_divergente, "básico de Yuji: o soco e o segundo impacto atrasado"),
    "soco-das-sombras": (soco_das_sombras, "básico de Megumi: a sombra borbulhando, o soco e os respingos"),
    "golpe-de-mao-sukuna": (golpe_de_mao_sukuna, "básico de Sukuna: a mão em faca rasgando o ar e o estalo seco"),
    "soco-endurecido": (soco_endurecido, "básico de Eren: o cristal estalando, o soco duro e as lascas tilintando"),
    "soco-do-gon": (soco_do_gon, "básico de Gon: a aura de Nen chiando e o soco cheio"),
    "soco-da-corrente": (soco_da_corrente, "básico de Kurapika: a corrente tilintando e o soco"),
    "soco-de-automail": (soco_de_automail, "básico de Edward: o metal rangendo, o soco de aço e a alquimia estalando"),
}
