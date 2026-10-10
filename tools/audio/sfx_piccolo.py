"""Os sons das habilidades do Piccolo (veja tools/vfx/familias_v2/piccolo.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (SR, baque, env, estalo, graos, n_de, passa, poe, reverb, rosa, ruido, satura, seno,
                 serra_suave, sobe_e_some, varre)


def _broca(rng, seg, f0, f1, giro=38.0, g=1.0):
    """O som da espiral: um zumbido agudo que "gira" (o volume e o brilho batendo rápido), como uma
    broca de energia."""
    n = n_de(seg)
    t = np.arange(n) / SR
    f = varre(f0, f1, n, 1.5)
    gira = 0.55 + 0.45 * np.sin(2 * math.pi * giro * t)
    corpo = serra_suave(f, n, 6) * 0.5 + seno(f * 2.01, n) * 0.25
    chiado = passa(ruido(rng, n), 3000, 9000, 2) * 0.25
    return (corpo * gira + chiado * (1 - gira)) * g


def makanko_carga(rng, v):
    """Os dedos na testa: o zumbido baixo que sobe devagar, a espiral apertando (o giro acelera) e os
    estalos de energia em volta."""
    n = n_de(1.4)
    t = np.arange(n) / SR
    giro = 8 + 30 * (t / t[-1]) ** 1.5
    fase = 2 * math.pi * np.cumsum(giro) / SR
    f = varre(160, 420, n, 0.8)
    x = (serra_suave(f, n, 5) * 0.3 + seno(f * 1.5, n) * 0.15) * (0.6 + 0.4 * np.sin(fase))
    x = x * sobe_e_some(n, 0.85, 1.4)
    poe(x, graos(rng, n, 16, 0.1, 1.3, 2500, 8000, 0.004, 0.7) * 0.35, 0.0)
    return reverb(x, 0.35, 0.18, 8000)


def makankosappo(rng, v):
    """Makankosappo: o estalo de saída, a broca de energia guinchando (a espiral) e atravessando, o
    furo seco no rival e o raio passando por trás."""
    x = _z(1.6)
    poe(x, estalo(rng, n_de(0.08), 2000, 9000, 0.01) * 1.1, 0.0)
    poe(x, baque(n_de(0.3), 180, 70, 0.08, 0.8) * 0.7, 0.0)
    b = _broca(rng, 0.55, 900, 1800, 46, 0.7)
    poe(x, b * env(len(b), 0.01, 0.5, segura=0.25), 0.02)
    poe(x, _whoosh(rng, 0.35, 1200, 5000, 0.5, g=0.5), 0.05)
    # o furo: um estalo seco e um "tunk" grave
    poe(x, estalo(rng, n_de(0.12), 1500, 7000, 0.02) * 1.3, 0.38)
    poe(x, baque(n_de(0.5), 140, 45, 0.14, 0.9) * 1.1, 0.38)
    poe(x, satura(passa(ruido(rng, n_de(0.25)), 600, 4000, 2) * env(n_de(0.25), 0.001, 0.08), 2) * 0.6, 0.38)
    # o raio sumindo por trás
    c = _broca(rng, 0.45, 1500, 600, 30, 0.35)
    poe(x, c * env(len(c), 0.005, 0.4), 0.42)
    poe(x, graos(rng, n_de(0.5), 14, 0.0, 0.4, 1500, 6000, 0.006, 0.6) * 0.4, 0.42)
    return reverb(x, 0.45, 0.2, 7500)


def escudo_do_mentor(rng, v):
    """Escudo do mentor: o pano pesado da capa batendo no ar, a barreira de ki subindo (um zumbido
    que sobe) e fechando com um "tum" e um brilho."""
    x = _z(1.6)
    n = n_de(0.4)
    capa = passa(rosa(rng, n), 120, 1400, 2) * sobe_e_some(n, 0.35, 1.6) * 0.9
    capa *= 0.7 + 0.3 * np.sin(2 * math.pi * 14 * np.arange(n) / SR)
    poe(x, capa, 0.0)
    poe(x, _whoosh(rng, 0.35, 250, 900, 0.4, g=0.5), 0.02)
    m = n_de(0.6)
    sobe = (serra_suave(varre(110, 330, m, 1.2), m, 6) * 0.25 + seno(varre(220, 660, m, 1.2), m) * 0.15) * sobe_e_some(m, 0.85, 1.3)
    poe(x, sobe, 0.2)
    poe(x, baque(n_de(0.5), 120, 60, 0.18, 0.5) * 0.8, 0.78)
    poe(x, _brilho(rng, 0.9, nota(76), 0.25), 0.78)
    zz = n_de(0.7)
    poe(x, seno(330, zz) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * np.arange(zz) / SR)) * env(zz, 0.05, 0.4) * 0.12, 0.8)
    return reverb(x, 0.5, 0.25, 7000)


def regeneracao_namekiana(rng, v):
    """Regeneração namekiana: as gotas voltando (estalinhos molhados), o braço nascendo num som
    grudento que estica e o tom de vida subindo no fim."""
    x = _z(1.8)
    for k in range(10):
        f0 = rng.uniform(500, 1100)
        m = n_de(0.08)
        gota = seno(varre(f0, f0 * 1.8, m, 1.0), m) * env(m, 0.002, 0.05) * 0.25
        poe(x, gota, 0.03 + 0.05 * k + rng.uniform(-0.015, 0.015))
    m = n_de(0.7)
    t = np.arange(m) / SR
    gruda = passa(rosa(rng, m), 150, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * (6 + 10 * t) * t)) * sobe_e_some(m, 0.6, 1.4) * 0.7
    poe(x, gruda, 0.5)
    poe(x, seno(varre(90, 180, m, 1.0), m) * sobe_e_some(m, 0.7, 1.4) * 0.35, 0.5)
    poe(x, B.cura(rng, v) * 0.6, 1.05)
    for k, nn in enumerate((67, 71, 74, 79)):
        poe(x, _brilho(rng, 0.7, nota(nn), 0.16), 1.05 + 0.07 * k)
    return reverb(x, 0.5, 0.25, 7500)


SONS: dict = {
    "makanko-carga": (makanko_carga, "os dedos na testa e a espiral de ki apertando"),
    "makankosappo": (makankosappo, "Makankosappo: a broca de energia furando o rival"),
    "escudo-do-mentor": (escudo_do_mentor, "Escudo do mentor: a capa e a barreira de ki fechando"),
    "regeneracao-namekiana": (regeneracao_namekiana, "Regeneração namekiana: as gotas e o braço novo"),
}
