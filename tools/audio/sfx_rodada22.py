"""Os sons da rodada 22 das habilidades próprias (veja tools/vfx/familias_v2/rodada22.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _grito(rng, f0, f1, seg, g=0.07):
    n = n_de(seg)
    t = _t(n)
    return satura(seno(varre(f0, f1, n) * (1 + 0.03 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 300, 2500, 2) * 0.4, 2.5) * env(n, 0.01, seg * 0.7) * g


# ------------------------------------------------------------------ Bowser

def investida_de_casco(rng, v):
    """Bowser: o casco girando (o zumbido que se aproxima) e o tranco."""
    x = _z(1.8)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t) ** 2) * sobe_e_some(n, 0.9, 1.0) * 0.35, 0.0)
    poe(x, _baque(90, 40, 0.4, 0.9, 2.8), 0.43)
    poe(x, _sino(rng, 700, 0.3, 0.04, METAL), 0.43)
    return reverb(x, 0.5, 0.25)


def sopro_flamejante(rng, v):
    """Bowser: o rugido do rei e o sopro de fogo."""
    x = _z(2.0)
    poe(x, _grito(rng, 120, 90, 0.5, 0.08), 0.0)
    poe(x, _fogo(rng, 1.0, 0.4), 0.15)
    return reverb(x, 0.6, 0.3)


def bowser_preparo(rng, v):
    """Bowser (Preparo): o pulo alto (o assobio que sobe) e o rugido abafado."""
    x = _z(1.4)
    n = n_de(0.8)
    poe(x, seno(varre(300, 900, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.035, 0.0)
    poe(x, _whoosh(rng, 0.4, 200, 2000, 0.5, 1.4, 0.35), 0.0)
    return reverb(x, 0.5, 0.25)


def tremor_do_rei(rng, v):
    """Bowser: a queda enorme, o chão rachando e as pedras."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.2, 200, 3000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(55, 25, 0.9, 1.0, 3.2), 0.2)
    poe(x, _explosao(rng, 1.2, 0.8), 0.2)
    q = np.random.default_rng(9)
    for k in range(8):
        poe(x, _baque(q.uniform(150, 300), 90, 0.1, 0.2), 0.45 + q.uniform(0, 0.6))
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Ryu

def hadouken_ryu(rng, v):
    """Ryu: "Hadouken!" (o grito), a bola de energia voando e o impacto com fogo."""
    x = _z(1.9)
    poe(x, _grito(rng, 260, 200, 0.3, 0.06), 0.0)
    n = n_de(0.5)
    poe(x, (seno(varre(500, 300, n), n) * 0.04 + passa(rosa(rng, n), 600, 4000, 2) * 0.2) * env(n, 0.01, 0.45), 0.2)
    poe(x, _baque(150, 60, 0.3, 0.6), 0.68)
    poe(x, _fogo(rng, 0.4, 0.2, 0.1), 0.7)
    return reverb(x, 0.5, 0.25)


def ryu_preparo(rng, v):
    """Ryu (Preparo): a energia azul juntando entre as mãos (o tom que cresce)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(150, 400, n), n) * (1 + 0.05 * np.sin(2 * math.pi * 9 * t)) * 0.05 + passa(rosa(rng, n), 800, 4000, 2) * 0.1) * sobe_e_some(n, 0.85, 1.2), 0.0)
    return reverb(x, 0.5, 0.25)


def shinku_hadouken(rng, v):
    """Ryu: "Shinku… Hadouken!" e o feixe enorme atravessando."""
    x = _z(2.2)
    poe(x, _grito(rng, 280, 210, 0.35, 0.06), 0.0)
    n = n_de(1.0)
    poe(x, (satura(seno(varre(120, 80, n), n), 2) * 0.08 + passa(rosa(rng, n), 400, 6000, 2) * 0.3) * env(n, 0.01, 0.7, segura=0.3), 0.15)
    poe(x, _explosao(rng, 0.9, 0.6), 0.4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Chun-Li

def spinning_bird_kick(rng, v):
    """Chun-Li: as pernas girando (os "vuups" em sequência) e o chute final."""
    x = _z(1.8)
    for k in range(6):
        poe(x, _whoosh(rng, 0.1, 800, 5000, 0.6, 1.4, 0.3), 0.04 + 0.09 * k)
    poe(x, _baque(170, 80, 0.2, 0.5), 0.62)
    return reverb(x, 0.4, 0.2)


def kikosho(rng, v):
    """Chun-Li: a energia sugada e a explosão azul em volta, com os raios."""
    x = _z(2.0)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 1000, 6000, 2) * sobe_e_some(n, 0.95, 1.0) * 0.25, 0.0)
    poe(x, _explosao(rng, 0.8, 0.7), 0.3)
    poe(x, _acorde((330, 415, 494, 659), 0.8, 0.04, 0.01, 0.6), 0.3)
    poe(x, graos(rng, n_de(0.4), 40, 0.0, 0.9, 2500, 9000, 0.002) * 0.35, 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Akuma

def gou_hadouken(rng, v):
    """Akuma: o Hadouken sombrio (o tom grave e rachado) e o impacto."""
    x = _z(1.9)
    poe(x, _grito(rng, 180, 140, 0.3, 0.07), 0.0)
    n = n_de(0.5)
    poe(x, (satura(seno(varre(300, 180, n), n), 3) * 0.05 + passa(rosa(rng, n), 300, 3000, 2) * 0.2) * env(n, 0.01, 0.45), 0.15)
    poe(x, graos(rng, n_de(0.4), 25, 0.0, 0.9, 1500, 6000, 0.003) * 0.3, 0.2)
    poe(x, _baque(110, 45, 0.4, 0.7, 2.6), 0.62)
    return reverb(x, 0.6, 0.3)


def ashura_senku(rng, v):
    """Akuma: o deslizar fantasma (o sopro que passa) e o golpe."""
    x = _z(1.8)
    poe(x, _sopro(rng, 0.5, 300, 2500, 0.3, 0.6), 0.0)
    poe(x, seno(varre(200, 120, n_de(0.4)), n_de(0.4)) * env(n_de(0.4), 0.05, 0.3) * 0.04, 0.05)
    poe(x, _whoosh(rng, 0.15, 1000, 6000, 0.7, 1.4, 0.4), 0.42)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Scorpion

def teleporte_infernal(rng, v):
    """Scorpion: o fogo do inferno engolindo (o "vush"), reaparecendo atrás e o golpe."""
    x = _z(1.9)
    poe(x, _fogo(rng, 0.35, 0.3, 0.3), 0.0)
    poe(x, _fogo(rng, 0.35, 0.3, 0.2), 0.3)
    poe(x, _whoosh(rng, 0.15, 1000, 6000, 0.7, 1.4, 0.4), 0.52)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.58)
    return reverb(x, 0.6, 0.3)


def scorpion_preparo(rng, v):
    """Scorpion (Preparo): a máscara tirada (o clique) e o crepitar do fogo do inferno."""
    x = _z(1.4)
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006), 0.0)
    poe(x, graos(rng, n_de(1.0), 40, 0.0, 0.95, 1000, 5000, 0.004) * 0.3, 0.1)
    poe(x, _fogo(rng, 1.0, 0.15, 0.6), 0.1)
    return reverb(x, 0.5, 0.25)


def toasty(rng, v):
    """Scorpion: "Toasty!" (o gritinho agudo) e o fogo do inferno saindo da caveira."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(900, 1300, n), n) * env(n, 0.01, 0.25) * 0.04, 0.0)
    poe(x, _fogo(rng, 1.1, 0.45, 0.15), 0.2)
    poe(x, _baque(120, 60, 0.3, 0.5), 0.25)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Sub-Zero

def lanca_de_gelo(rng, v):
    """Sub-Zero: a lança de gelo voando (o assobio frio) e o gelo estalando no rival."""
    x = _z(1.8)
    n = n_de(0.4)
    poe(x, (seno(varre(2000, 1200, n), n) * 0.03 + passa(rosa(rng, n), 3000, 9000, 2) * 0.15) * env(n, 0.01, 0.35), 0.05)
    poe(x, graos(rng, n_de(0.4), 40, 0.0, 0.8, 4000, 11000, 0.003) * 0.35, 0.42)
    for k in range(3):
        poe(x, _sino(rng, 2800 + 400 * k, 0.3, 0.03, VIDRO), 0.45 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def clone_congelado(rng, v):
    """Sub-Zero: o clone de gelo se formando (o rangido) e o rival congelando ao bater."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.2, 0.0)
    poe(x, _baque(200, 120, 0.15, 0.4), 0.5)
    poe(x, graos(rng, n_de(0.5), 60, 0.0, 0.9, 3000, 11000, 0.003) * 0.4, 0.7)
    poe(x, _sino(rng, 2200, 0.5, 0.05, VIDRO), 0.7)
    return reverb(x, 0.6, 0.3)


def subzero_preparo(rng, v):
    """Sub-Zero (Preparo): o frio juntando (o vento gelado e os cristais)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 2000, 8000, 0.15, 0.6), 0.0)
    for k in range(4):
        poe(x, _sino(rng, 3000 + 300 * k, 0.25, 0.02, CRISTAL), 0.15 + 0.2 * k)
    return reverb(x, 0.6, 0.3)


def inverno_absoluto(rng, v):
    """Sub-Zero: o raio congelante e os cristais enormes subindo."""
    x = _z(2.1)
    n = n_de(0.6)
    poe(x, (seno(varre(1500, 600, n), n) * 0.04 + passa(rosa(rng, n), 2000, 9000, 2) * 0.25) * env(n, 0.005, 0.5), 0.0)
    for k in range(7):
        poe(x, _sino(rng, 1800 + 250 * k, 0.4, 0.035, VIDRO), 0.25 + 0.03 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.005) * 0.4, 0.25 + 0.03 * k)
    poe(x, _baque(150, 80, 0.3, 0.5), 0.3)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "investida-de-casco": (investida_de_casco, "Bowser: a investida de casco"),
    "sopro-flamejante": (sopro_flamejante, "Bowser: o sopro flamejante"),
    "bowser-preparo": (bowser_preparo, "Bowser: o pulo (Preparo)"),
    "tremor-do-rei": (tremor_do_rei, "Bowser: o tremor do rei"),
    "hadouken-ryu": (hadouken_ryu, "Ryu: Hadouken"),
    "ryu-preparo": (ryu_preparo, "Ryu: a energia (Preparo)"),
    "shinku-hadouken": (shinku_hadouken, "Ryu: Shinku Hadouken"),
    "spinning-bird-kick": (spinning_bird_kick, "Chun-Li: Spinning Bird Kick"),
    "kikosho": (kikosho, "Chun-Li: Kikosho"),
    "gou-hadouken": (gou_hadouken, "Akuma: Gou Hadouken"),
    "ashura-senku": (ashura_senku, "Akuma: Ashura Senku"),
    "teleporte-infernal": (teleporte_infernal, "Scorpion: o teleporte infernal"),
    "scorpion-preparo": (scorpion_preparo, "Scorpion: a caveira (Preparo)"),
    "toasty": (toasty, "Scorpion: Toasty!"),
    "lanca-de-gelo": (lanca_de_gelo, "Sub-Zero: a lança de gelo"),
    "clone-congelado": (clone_congelado, "Sub-Zero: o clone congelado"),
    "subzero-preparo": (subzero_preparo, "Sub-Zero: o frio (Preparo)"),
    "inverno-absoluto": (inverno_absoluto, "Sub-Zero: o inverno absoluto"),
}
