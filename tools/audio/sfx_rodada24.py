"""Os sons da rodada 24 das habilidades próprias (veja tools/vfx/familias_v2/rodada24.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _tiro(rng, g=0.6):
    n = n_de(0.25)
    return satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.06), 2.5) * g


# ------------------------------------------------------------------ Sekiro

def deflexao_sekiro(rng, v):
    """Sekiro: a deflexão perfeita (o "tching" metálico alto e a faísca)."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.04), 2500, 9000, 0.006) * 1.2, 0.12)
    poe(x, _sino(rng, 2900, 0.8, 0.08, METAL), 0.12)
    poe(x, _sino(rng, 4350, 0.5, 0.04, METAL), 0.12)
    poe(x, graos(rng, n_de(0.3), 25, 0.0, 0.6, 3000, 9000, 0.002) * 0.3, 0.14)
    return reverb(x, 0.6, 0.3)


def mikiri(rng, v):
    """Sekiro: o aviso de perigo (o tom grave), a lança vindo e o pisão em cima dela."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, satura(seno(varre(180, 160, n), n), 2.5) * env(n, 0.01, 0.25) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.25, 600, 4000, 0.8, 1.4, 0.35), 0.05)
    poe(x, _baque(110, 50, 0.4, 0.8, 2.6), 0.32)
    poe(x, _sino(rng, 900, 0.4, 0.05, METAL), 0.32)
    return reverb(x, 0.5, 0.25)


def golpe_mortal(rng, v):
    """Sekiro: o golpe mortal (o corte fundo e o jorro)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 1500, 9000, 0.8, 1.3, 0.5), 0.05)
    poe(x, _baque(150, 60, 0.4, 0.7, 2.4), 0.2)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 400, 2500, 2) * env(n, 0.01, 0.4) * 0.3, 0.25)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Malenia

def lamina_de_miquella(rng, v):
    """Malenia: os dois cortes da lâmina protética e a vida voltando (o brilho)."""
    x = _z(1.9)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2000, 9000, 0.7, 1.4, 0.45), 0.0 + 0.15 * k)
        poe(x, _sino(rng, 3300 + 400 * k, 0.4, 0.04, METAL), 0.1 + 0.15 * k)
    poe(x, _acorde((392, 494, 587), 0.6, 0.03, 0.05, 0.5), 0.5)
    return reverb(x, 0.6, 0.3)


def malenia_preparo(rng, v):
    """Malenia (Preparo): o voo no ar (o vento) e a flor abrindo (o tom estranho)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 400, 3000, 0.2, 0.5), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(300, 500, n) * (1 + 0.02 * np.sin(2 * math.pi * 5 * t)), n) * sobe_e_some(n, 0.8, 1.2) * 0.035, 0.0)
    return reverb(x, 0.7, 0.35)


def flor_escarlate(rng, v):
    """Malenia: a flor escarlate explodindo e as pétalas de podridão."""
    x = _z(2.2)
    poe(x, _explosao(rng, 1.0, 0.8), 0.3)
    poe(x, _acorde((147, 175, 208, 262), 1.0, 0.05, 0.02, 0.8), 0.3)
    poe(x, _sopro(rng, 1.0, 300, 3000, 0.25, 0.3), 0.35)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Agente 47

def disfarce(rng, v):
    """Agente 47: o terno ajeitado (o farfalhar), a seringa e o veneno."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 1500, 5000, 2) * env(n, 0.02, 0.2) * 0.2, 0.0)
    poe(x, _piu(2000, 2400, 0.08, 0.02), 0.45)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 400, 2000, 2) * sobe_e_some(m, 0.4, 1.3) * 0.2, 0.6)
    return reverb(x, 0.5, 0.25)


def garrote(rng, v):
    """Agente 47: o fio do garrote esticando (o rangido) e apertando."""
    x = _z(1.8)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(varre(600, 1400, n) * (1 + 0.04 * np.sin(2 * math.pi * 30 * t)), n) * env(n, 0.05, 0.5) * 0.03, 0.1)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.05, 0.5) * 0.15, 0.1)
    poe(x, _baque(130, 70, 0.2, 0.4), 0.6)
    return reverb(x, 0.4, 0.2)


def agent47_preparo(rng, v):
    """Agente 47 (Preparo): a respiração lenta e a luneta ajustando (os cliques)."""
    x = _z(1.4)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.5, 1.4) * 0.12, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.4, 0.2 + 0.25 * k)
    return reverb(x, 0.4, 0.2)


def tiro_planejado(rng, v):
    """Agente 47: o tiro de precisão com silenciador pesado e o impacto distante."""
    x = _z(1.9)
    poe(x, _tiro(rng, 0.7), 0.0)
    poe(x, _baque(100, 45, 0.3, 0.5, 2.2), 0.0)
    poe(x, _whoosh(rng, 0.15, 3000, 10000, 0.6, 1.3, 0.3), 0.03)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.2)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Geralt

def _sinal_som(rng):
    x = _z(0.6)
    n = n_de(0.3)
    poe(x, (seno(varre(300, 600, n), n) * 0.04 + passa(rosa(rng, n), 1500, 6000, 2) * 0.1) * env(n, 0.01, 0.25), 0.0)
    return x


def sinal_de_quen(rng, v):
    """Geralt: o sinal desenhado no ar e a bolha de Quen zumbindo."""
    x = _z(2.0)
    poe(x, _sinal_som(rng), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(220 * (1 + 0.01 * np.sin(2 * math.pi * 6 * t)), n) * sobe_e_some(n, 0.25, 1.2) * 0.05, 0.25)
    poe(x, _acorde((330, 415, 494, 659), 0.8, 0.035, 0.05, 0.6), 0.3)
    poe(x, graos(rng, n_de(0.6), 20, 0.0, 0.9, 2500, 8000, 0.002) * 0.2, 0.3)
    return reverb(x, 0.6, 0.3)


def sinal_de_igni(rng, v):
    """Geralt: o sinal e o leque de fogo."""
    x = _z(2.0)
    poe(x, _sinal_som(rng), 0.0)
    poe(x, _fogo(rng, 0.9, 0.45, 0.15), 0.2)
    poe(x, _whoosh(rng, 0.4, 300, 3000, 0.6, 1.4, 0.4), 0.2)
    return reverb(x, 0.5, 0.25)


def sinal_de_axii(rng, v):
    """Geralt: o sinal Axii e o transe (o tom que gira e embaralha)."""
    x = _z(2.0)
    poe(x, _sinal_som(rng), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(400 * (1 + 0.1 * np.sin(2 * math.pi * 3 * t)), n) * env(n, 0.05, 0.8) * 0.04, 0.25)
    poe(x, seno(600 * (1 - 0.1 * np.sin(2 * math.pi * 3 * t)), n) * env(n, 0.05, 0.8) * 0.03, 0.25)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Isaac

def desmembramento(rng, v):
    """Isaac: o cortador de plasma carregado e os três cortes."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.05, 0.2) * 0.04, 0.0)
    for k in range(3):
        m = n_de(0.2)
        poe(x, (seno(varre(1500, 500, m), m) * 0.04 + passa(rosa(rng, m), 2000, 8000, 2) * 0.2) * env(m, 0.002, 0.15), 0.3 + 0.1 * k)
        poe(x, _baque(170, 80, 0.12, 0.3), 0.32 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Gordon

def pe_de_cabra(rng, v):
    """Gordon: o pé de cabra girando (o assobio) e o golpe de metal."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.4, 400, 4000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(150, 70, 0.3, 0.6, 2.2), 0.42)
    poe(x, _sino(rng, 1300, 0.6, 0.06, METAL), 0.42)
    return reverb(x, 0.5, 0.25)


def zero_point(rng, v):
    """Gordon: o canhão gravitacional carregando (o zumbido) e o empurrão."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, satura(seno(varre(80, 200, n), n), 2) * sobe_e_some(n, 0.9, 1.0) * 0.06, 0.0)
    poe(x, _baque(80, 40, 0.5, 0.8, 2.6), 0.25)
    poe(x, _whoosh(rng, 0.6, 200, 3000, 0.4, 1.4, 0.5), 0.25)
    poe(x, _sino(rng, 500, 0.6, 0.04, METAL), 0.27)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "deflexao-sekiro": (deflexao_sekiro, "Sekiro: a deflexão"),
    "mikiri": (mikiri, "Sekiro: Mikiri"),
    "golpe-mortal": (golpe_mortal, "Sekiro: o golpe mortal"),
    "lamina-de-miquella": (lamina_de_miquella, "Malenia: a lâmina protética"),
    "malenia-preparo": (malenia_preparo, "Malenia: a flor abrindo (Preparo)"),
    "flor-escarlate": (flor_escarlate, "Malenia: a flor escarlate"),
    "disfarce": (disfarce, "Agente 47: o disfarce"),
    "garrote": (garrote, "Agente 47: o garrote"),
    "agent47-preparo": (agent47_preparo, "Agente 47: a luneta (Preparo)"),
    "tiro-planejado": (tiro_planejado, "Agente 47: o tiro planejado"),
    "sinal-de-quen": (sinal_de_quen, "Geralt: Quen"),
    "sinal-de-igni": (sinal_de_igni, "Geralt: Igni"),
    "sinal-de-axii": (sinal_de_axii, "Geralt: Axii"),
    "desmembramento": (desmembramento, "Isaac: o desmembramento"),
    "pe-de-cabra": (pe_de_cabra, "Gordon: o pé de cabra"),
    "zero-point": (zero_point, "Gordon: o Zero-point"),
}
