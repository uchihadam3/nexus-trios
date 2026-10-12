"""Os sons das Mecânicas únicas ativando como uma habilidade (veja tools/vfx/familias_v2/unicas_a.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _z
from som import CRISTAL, SINO, SR, baque, env, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def unica_ativa(rng, v):
    """A ativação: o acorde místico que abre, as runas acendendo (os sinos em sequência) e o brilho subindo."""
    x = _z(1.8)
    m = n_de(1.2)
    poe(x, (seno(262, m) + seno(392, m) * 0.7 + seno(523, m) * 0.5 + seno(659, m) * 0.3) * env(m, 0.04, 0.7) * 0.05, 0.0)
    for k, f in enumerate((784, 880, 988, 1175, 1319, 1568)):
        poe(x, modal(n_de(0.4), f, rng=rng, **SINO) * env(n_de(0.4), 0.002, 0.2) * 0.05, 0.15 + 0.05 * k)
    n = n_de(0.6)
    poe(x, seno(varre(600, 1400, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.03, 0.35)
    return reverb(x, 0.7, 0.35)


def cell_contagem(rng, v):
    """O "Vai explodir!": o zumbido grave que incha e os bipes da contagem acelerando."""
    x = _z(1.8)
    n = n_de(1.5)
    t = _t(n)
    poe(x, satura(seno(varre(60, 140, n, 1.4), n), 2.0) * (0.6 + 0.4 * np.sin(2 * math.pi * (3 + 6 * t) * t)) * sobe_e_some(n, 0.9, 1.0) * 0.12, 0.0)
    t0, passo = 0.1, 0.3
    while t0 < 1.4:
        m = n_de(0.06)
        poe(x, seno(1800, m) * env(m, 0.002, 0.04) * 0.06, t0)
        t0 += passo
        passo = max(0.07, passo * 0.75)
    return reverb(x, 0.5, 0.25)


def cell_autodestruicao(rng, v):
    """A Autodestruição: o silêncio curto, o estrondo enorme e o ronco da onda que passa."""
    x = _z(2.4)
    poe(x, satura(baque(n_de(0.9), 55, 22, 0.35, 1.0), 2.6) * 0.9, 0.05)
    m = n_de(1.6)
    poe(x, satura(passa(rosa(rng, m), 25, 3000, 2) * env(m, 0.002, 0.8), 2.2) * 0.8, 0.05)
    poe(x, passa(rosa(rng, m), 30, 300, 2) * sobe_e_some(m, 0.2, 1.4) * 0.5, 0.3)
    poe(x, graos(rng, n_de(1.0), 40, 0.1, 0.9, 400, 4000, 0.02) * 0.4, 0.4)
    return reverb(x, 0.8, 0.35)


def pontos_de_chakra(rng, v):
    """Os Pontos de chakra: o Byakugan acendendo (o tom que abre), os oito pontos (toques suaves) e as palmas dos
    leões (dois sopros fortes)."""
    x = _z(1.8)
    n = n_de(0.5)
    poe(x, seno(varre(400, 900, n, 1.0), n) * sobe_e_some(n, 0.6, 1.4) * 0.04, 0.0)
    for k in range(8):
        poe(x, modal(n_de(0.25), 1320 + 60 * k, rng=rng, **CRISTAL) * env(n_de(0.25), 0.002, 0.08) * 0.05, 0.25 + 0.05 * k)
    for k in range(2):
        m = n_de(0.3)
        poe(x, (passa(rosa(rng, m), 200, 2500, 2) * 0.4 + satura(baque(m, 120, 60, 0.06, 0.4), 1.5) * 0.3) * sobe_e_some(m, 0.2, 1.5) * 0.8, 0.5 + 0.15 * k)
    poe(x, _brilho(rng, 0.6, 1760, 0.04, SINO), 0.8)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "unica-ativa": (unica_ativa, "Mecânica única: o acorde e as runas acendendo (ativação)"),
    "cell-contagem": (cell_contagem, "Cell: o zumbido inchando e a contagem"),
    "cell-autodestruicao": (cell_autodestruicao, "Cell: o estrondo da Autodestruição"),
    "pontos-de-chakra": (pontos_de_chakra, "Hinata: o Byakugan, os pontos e as palmas"),
}
