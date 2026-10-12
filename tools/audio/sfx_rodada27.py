"""Os sons da rodada 27 das habilidades próprias (veja tools/vfx/familias_v2/rodada27.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _areia(rng, seg, g=0.3, pico=0.4):
    n = n_de(seg)
    return passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, pico, 1.2) * g


def _ki(rng, seg, f0=150, f1=300, g=0.06, pico=0.8):
    n = n_de(seg)
    t = _t(n)
    return (satura(seno(varre(f0, f1, n) * (1 + 0.03 * np.sin(2 * math.pi * 9 * t)), n), 2) * g + passa(rosa(rng, n), 800, 5000, 2) * g * 2) * sobe_e_some(n, pico, 1.2)


# ------------------------------------------------------------------ Gaara

def defesa_absoluta(rng, v):
    """Gaara: a areia subindo em parede (o chiado que cresce) e os espinhos."""
    x = _z(1.9)
    poe(x, _areia(rng, 0.7, 0.35, 0.6), 0.0)
    poe(x, _baque(110, 60, 0.3, 0.5, 1.6), 0.4)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006) * 0.4, 0.45 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def escudo_de_areia(rng, v):
    """Gaara: as camadas de areia envolvendo o aliado."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _areia(rng, 0.4, 0.25, 0.5), 0.1 * k)
    poe(x, _acorde((220, 277, 330), 0.7, 0.03, 0.1, 0.5), 0.35)
    return reverb(x, 0.5, 0.25)


def gaara_preparo(rng, v):
    """Gaara (Preparo): a cabaça abrindo (o "pop" da rolha) e a areia girando."""
    x = _z(1.4)
    poe(x, _piu(300, 150, 0.06, 0.05), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.6, 1.0) * 0.25, 0.1)
    return reverb(x, 0.5, 0.25)


def funeral_do_deserto(rng, v):
    """Gaara: a areia engolindo o rival e o aperto final (o esmagar)."""
    x = _z(2.1)
    poe(x, _areia(rng, 0.7, 0.4, 0.7), 0.0)
    poe(x, _baque(70, 30, 0.6, 0.9, 2.8), 0.6)
    poe(x, passa(rosa(rng, n_de(0.3)), 200, 2500, 2) * env(n_de(0.3), 0.002, 0.25) * 0.5, 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Cell

def absorcao_cell(rng, v):
    """Cell: a cauda cravando e sugando a energia (o som de sucção)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 600, 4000, 0.8, 1.4, 0.35), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1000, 4000, 0.008), 0.28)
    n = n_de(0.5)
    poe(x, (seno(varre(600, 200, n), n) * 0.04 + passa(rosa(rng, n), 300, 2000, 2) * 0.2) * env(n, 0.02, 0.45), 0.35)
    return reverb(x, 0.5, 0.25)


def regeneracao_celular(rng, v):
    """Cell: as células se refazendo (os estalinhos molhados) e a aura."""
    x = _z(1.9)
    q = np.random.default_rng(2)
    for k in range(10):
        poe(x, _piu(q.uniform(400, 800), q.uniform(800, 1200), 0.04, 0.025), 0.05 * k)
    poe(x, _ki(rng, 0.8, 120, 220, 0.04, 0.5), 0.2)
    return reverb(x, 0.5, 0.25)


def cell_preparo(rng, v):
    """Cell (Preparo): as asas de inseto zumbindo e a aura."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 40 * t)) * sobe_e_some(n, 0.5, 1.0) * 0.2, 0.0)
    poe(x, _ki(rng, 1.0, 100, 200, 0.03, 0.8), 0.0)
    return reverb(x, 0.5, 0.25)


def forma_perfeita(rng, v):
    """Cell: o Kamehameha perfeito (o "ka-me-ha-me" juntando e o feixe em leque)."""
    x = _z(2.3)
    poe(x, _ki(rng, 0.3, 200, 500, 0.05, 0.95), 0.0)
    n = n_de(0.9)
    poe(x, (satura(seno(varre(120, 80, n), n), 2) * 0.08 + passa(rosa(rng, n), 400, 6000, 2) * 0.3) * env(n, 0.01, 0.6, segura=0.3), 0.25)
    poe(x, _explosao(rng, 0.9, 0.6), 0.42)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Broly

def eraser_cannon(rng, v):
    """Broly: a esfera pequena voando (o zunido) e a explosão enorme."""
    x = _z(2.1)
    n = n_de(0.35)
    poe(x, seno(varre(600, 300, n), n) * env(n, 0.01, 0.3) * 0.04, 0.05)
    poe(x, _explosao(rng, 1.3, 0.95), 0.38)
    poe(x, _baque(50, 25, 0.8, 1.0, 3.0), 0.38)
    return reverb(x, 0.7, 0.35)


def furia_lendaria(rng, v):
    """Broly: o grito do Lendário e a aura verde explodindo."""
    x = _z(2.2)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(seno(varre(120, 90, n) * (1 + 0.05 * np.sin(2 * math.pi * 20 * t)), n) + passa(rosa(rng, n), 200, 3000, 2) * 0.8, 3) * env(n, 0.05, 0.7) * 0.1, 0.0)
    poe(x, _explosao(rng, 0.8, 0.5), 0.05)
    poe(x, graos(rng, n_de(0.8), 60, 0.0, 0.9, 2500, 9000, 0.002) * 0.35, 0.15)
    return reverb(x, 0.6, 0.3)


def broly_preparo(rng, v):
    """Broly (Preparo): a esfera verde crescendo na mão (o zumbido grave que sobe)."""
    x = _z(1.4)
    poe(x, _ki(rng, 1.0, 80, 200, 0.06, 0.85), 0.0)
    return reverb(x, 0.5, 0.25)


def gigantic_roar(rng, v):
    """Broly: o rugido enorme em ondas."""
    x = _z(2.4)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(seno(varre(90, 60, n) * (1 + 0.06 * np.sin(2 * math.pi * 18 * t)), n) + passa(rosa(rng, n), 100, 2500, 2), 3) * env(n, 0.03, 0.9) * 0.12, 0.0)
    for k in range(4):
        poe(x, _baque(60, 30, 0.4, 0.5, 2.2), 0.1 + 0.15 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Beerus

def esfera_da_destruicao(rng, v):
    """Beerus: a esfera da destruição (o zumbido denso) e o impacto."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(140 * (1 + 0.04 * np.sin(2 * math.pi * 12 * t)), n), 2.5) * env(n, 0.05, 0.45) * 0.06, 0.0)
    poe(x, _explosao(rng, 1.0, 0.8), 0.58)
    return reverb(x, 0.6, 0.3)


def beerus_preparo(rng, v):
    """Beerus (Preparo): o sol de destruição sobre o dedo (o zumbido que pulsa)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(110, n) + seno(165, n) * 0.5, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.0) * 0.06, 0.0)
    return reverb(x, 0.6, 0.3)


def ira_do_deus(rng, v):
    """Beerus: o sol de destruição caindo e apagando tudo (o estrondo e o silêncio)."""
    x = _z(2.6)
    poe(x, _whoosh(rng, 0.35, 150, 2000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _explosao(rng, 1.6, 1.0), 0.33)
    poe(x, _baque(40, 20, 1.0, 1.0, 3.2), 0.33)
    poe(x, _acorde((73, 110, 147), 1.4, 0.05, 0.01, 1.0), 0.35)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Mewtwo

def psiquico_mewtwo(rng, v):
    """Mewtwo: a onda psíquica (o tom que vibra) e o rival flutuando."""
    x = _z(1.9)
    for k in range(4):
        n = n_de(0.3)
        t = _t(n)
        poe(x, seno(500 * (1 + 0.05 * np.sin(2 * math.pi * 30 * t)), n) * env(n, 0.01, 0.25) * 0.03, 0.05 * k)
    m = n_de(0.6)
    poe(x, seno(varre(300, 600, m), m) * sobe_e_some(m, 0.5, 1.2) * 0.04, 0.4)
    return reverb(x, 0.7, 0.35)


def barreira_mewtwo(rng, v):
    """Mewtwo: a barreira de hexágonos acendendo (os bipes cristalinos) e fechando."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _sino(rng, 1200 + 150 * k, 0.3, 0.03, CRISTAL), 0.1 + 0.05 * k)
    poe(x, _acorde((330, 415, 494, 659), 0.8, 0.035, 0.05, 0.6), 0.35)
    return reverb(x, 0.6, 0.3)


def mewtwo_preparo(rng, v):
    """Mewtwo (Preparo): os olhos brilhando e a energia girando."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(400 * (1 + 0.1 * np.sin(2 * math.pi * 3 * t)), n) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.0)
    poe(x, seno(600 * (1 - 0.1 * np.sin(2 * math.pi * 3 * t)), n) * sobe_e_some(n, 0.6, 1.2) * 0.03, 0.0)
    return reverb(x, 0.7, 0.35)


def tempestade_mental(rng, v):
    """Mewtwo: a tempestade psíquica (os tons que giram e os raios)."""
    x = _z(2.2)
    n = n_de(1.2)
    t = _t(n)
    for k, f in enumerate((300, 450, 600)):
        poe(x, seno(f * (1 + 0.12 * np.sin(2 * math.pi * (3 + k) * t)), n) * sobe_e_some(n, 0.3, 1.2) * 0.03, 0.05)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.008) * 0.6, 0.35 + 0.15 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Garou

def contra_fluxo(rng, v):
    """Garou: o desvio fluindo como água e o contra-ataque."""
    x = _z(1.8)
    poe(x, _sopro(rng, 0.45, 600, 3000, 0.25, 0.5), 0.0)
    poe(x, _whoosh(rng, 0.15, 800, 5000, 0.7, 1.4, 0.4), 0.38)
    poe(x, _baque(150, 70, 0.3, 0.6, 2.2), 0.45)
    return reverb(x, 0.5, 0.25)


def cacador_de_herois(rng, v):
    """Garou: o rosnado de monstro e as garras rasgando em X."""
    x = _z(1.9)
    n = n_de(0.4)
    poe(x, satura(seno(varre(130, 100, n), n) + passa(rosa(rng, n), 200, 2000, 2) * 0.7, 3) * env(n, 0.03, 0.3) * 0.07, 0.0)
    for k in range(2):
        for m in range(3):
            poe(x, _whoosh(rng, 0.1, 2000, 8000, 0.6, 1.4, 0.3), 0.1 + 0.15 * k + 0.02 * m)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.3)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "defesa-absoluta": (defesa_absoluta, "Gaara: a defesa absoluta"),
    "escudo-de-areia": (escudo_de_areia, "Gaara: o escudo de areia"),
    "gaara-preparo": (gaara_preparo, "Gaara: a cabaça (Preparo)"),
    "funeral-do-deserto": (funeral_do_deserto, "Gaara: o funeral do deserto"),
    "absorcao-cell": (absorcao_cell, "Cell: a absorção"),
    "regeneracao-celular": (regeneracao_celular, "Cell: a regeneração"),
    "cell-preparo": (cell_preparo, "Cell: as asas (Preparo)"),
    "forma-perfeita": (forma_perfeita, "Cell: a forma perfeita"),
    "eraser-cannon": (eraser_cannon, "Broly: Eraser Cannon"),
    "furia-lendaria": (furia_lendaria, "Broly: a fúria lendária"),
    "broly-preparo": (broly_preparo, "Broly: a esfera (Preparo)"),
    "gigantic-roar": (gigantic_roar, "Broly: Gigantic Roar"),
    "esfera-da-destruicao": (esfera_da_destruicao, "Beerus: a esfera da destruição"),
    "beerus-preparo": (beerus_preparo, "Beerus: o sol (Preparo)"),
    "ira-do-deus": (ira_do_deus, "Beerus: a ira do deus"),
    "psiquico-mewtwo": (psiquico_mewtwo, "Mewtwo: Psíquico"),
    "barreira-mewtwo": (barreira_mewtwo, "Mewtwo: a barreira"),
    "mewtwo-preparo": (mewtwo_preparo, "Mewtwo: os olhos (Preparo)"),
    "tempestade-mental": (tempestade_mental, "Mewtwo: a tempestade mental"),
    "contra-fluxo": (contra_fluxo, "Garou: o contra-fluxo"),
    "cacador-de-herois": (cacador_de_herois, "Garou: o caçador de heróis"),
}
