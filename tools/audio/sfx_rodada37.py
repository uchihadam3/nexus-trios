"""Os sons da rodada 37 das habilidades próprias (veja tools/vfx/familias_v2/rodada37.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _risada(rng, f=220, n_vezes=4, passo=0.13, g=0.045):
    """A risada (os "hé" curtos e roucos)."""
    x = _z(n_vezes * passo + 0.3)
    for k in range(n_vezes):
        n = n_de(passo * 0.8)
        poe(x, satura(seno(varre(f * 1.1, f, n), n) + passa(rosa(rng, n), 500, 2500, 2) * 0.3, 3) * env(n, 0.005, passo * 0.6) * g, passo * k)
    return x


# ------------------------------------------------------------------ Peter Griffin

def briga_com_o_galo(rng, v):
    """Peter: a briga com o galo (o cacarejo, os socos e as penas)."""
    x = _z(2.0)
    for k in range(3):
        n = n_de(0.12)
        poe(x, satura(seno(varre(900, 1300, n), n), 3) * env(n, 0.005, 0.1) * 0.035, 0.1 + 0.25 * k)
    q = np.random.default_rng(4)
    for k in range(8):
        poe(x, _baque(q.uniform(130, 200), 70, 0.1, 0.4), 0.05 + 0.09 * k)
    poe(x, passa(rosa(rng, n_de(0.8)), 300, 2500, 2) * sobe_e_some(n_de(0.8), 0.3, 1.2) * 0.25, 0.0)
    _estrelinhas(rng, x, 0.6, 4)
    return reverb(x, 0.4, 0.2)


def ideia_terrivel(rng, v):
    """Peter: o "plim" da ideia, o assobio da bomba e a explosão."""
    x = _z(2.2)
    poe(x, _sino(rng, 1568, 0.4, 0.04, CRISTAL), 0.0)
    poe(x, _sino(rng, 2093, 0.4, 0.03, CRISTAL), 0.06)
    n = n_de(0.25)
    poe(x, seno(varre(1400, 700, n), n) * env(n, 0.02, 0.2) * 0.03, 0.38)
    poe(x, _baque(55, 22, 0.9, 1.0, 3.2), 0.6)
    poe(x, _explosao(rng, 0.9, 55), 0.6)
    return reverb(x, 0.6, 0.3)


def peter_preparo(rng, v):
    """Peter (Preparo): a risadinha "hehehe" sacudindo a barriga."""
    x = _z(1.4)
    poe(x, _risada(rng, 230, 6, 0.15, 0.04), 0.05)
    return reverb(x, 0.4, 0.2)


def nhe_he_he(rng, v):
    """Peter: a risada "nhé-hé-hé" em ondas e o tombo ("ssss" segurando o joelho)."""
    x = _z(2.3)
    poe(x, _risada(rng, 200, 5, 0.13, 0.05), 0.0)
    _estrelinhas(rng, x, 0.45, 4)
    poe(x, _baque(100, 40, 0.3, 0.6), 0.65)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.05, 0.4) * 0.2, 0.75)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Stewie Griffin

def raio_de_controle(rng, v):
    """Stewie: a pistola de raio (o "uí-uí-uí" futurista) e o controle da mente."""
    x = _z(1.9)
    n = n_de(0.55)
    t = _t(n)
    poe(x, seno(900 + 500 * np.sin(2 * math.pi * 12 * t), n) * env(n, 0.02, 0.2) * 0.035, 0.15)
    poe(x, seno(varre(400, 250, n_de(0.5)), n_de(0.5)) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * _t(n_de(0.5)))) * env(n_de(0.5), 0.05, 0.4) * 0.03, 0.45)
    return reverb(x, 0.6, 0.3)


def plano_mirabolante(rng, v):
    """Stewie: a planta do plano (o lápis riscando) e os escudos montando."""
    x = _z(2.0)
    for k in range(5):
        n = n_de(0.07)
        poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.01, 0.05) * 0.2, 0.05 + 0.08 * k)
    for k in range(3):
        poe(x, _sino(rng, 784 + 196 * k, 0.4, 0.03, METAL), 0.42 + 0.05 * k)
    poe(x, _brilho(rng, 0.5, 1319, 0.025, CRISTAL), 0.5)
    return reverb(x, 0.5, 0.25)


def stewie_preparo(rng, v):
    """Stewie (Preparo): as engrenagens do plano girando (o tique-taque)."""
    x = _z(1.4)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.45, 0.1 * k)
    n = n_de(1.0)
    poe(x, seno(165, n) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def dominacao_mundial(rng, v):
    """Stewie: "Dominação mundial!" — a fanfarra malvada e o mundo na mira."""
    x = _z(2.3)
    poe(x, _acorde((147, 175, 220, 294), 1.1, 0.04, 0.03, 0.8), 0.0)
    for k in range(2):
        n = n_de(0.06)
        poe(x, seno(2000, n) * env(n, 0.003, 0.05) * 0.03, 0.2 + 0.1 * k)
    poe(x, _acorde((294, 370, 440, 587), 0.9, 0.035, 0.03, 0.7), 0.45)
    poe(x, _brilho(rng, 0.6, 1568, 0.025, CRISTAL), 0.5)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Eric Cartman

def respeitem_minha_autoridade(rng, v):
    """Cartman: "Respeitem minha autoridade!" (o grito estridente em ondas)."""
    x = _z(1.9)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(500, 650, n) * (1 + 0.05 * np.sin(2 * math.pi * 7 * t)), n), 3) * env(n, 0.02, 0.35) * 0.05, 0.1)
    poe(x, _sino(rng, 1047, 0.4, 0.03, METAL), 0.0)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.45)
    return reverb(x, 0.5, 0.25)


def chantagem(rng, v):
    """Cartman: as fotos voando (o "flap-flap") e o "hehe" malvado."""
    x = _z(2.0)
    for k in range(3):
        poe(x, passa(rosa(rng, n_de(0.08)), 1500, 6000, 2) * env(n_de(0.08), 0.005, 0.07) * 0.2, 0.05 + 0.08 * k)
        poe(x, _baque(250, 150, 0.05, 0.2), 0.5 + 0.08 * k)
    poe(x, _risada(rng, 300, 3, 0.12, 0.035), 0.7)
    return reverb(x, 0.4, 0.2)


def cartman_preparo(rng, v):
    """Cartman (Preparo): as mãos se esfregando e o tom malvado."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1000, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.15, 0.0)
    poe(x, _acorde((147, 175, 208), 0.9, 0.025, 0.1, 0.5), 0.1)
    return reverb(x, 0.5, 0.25)


def plano_egoista(rng, v):
    """Cartman: a nuvem de gás (o "prrrrr" grave) se espalhando e o chiado."""
    x = _z(2.3)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(varre(90, 70, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 35 * t)), 4) * env(n, 0.02, 0.45) * 0.07, 0.0)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.2)
    _estrelinhas(rng, x, 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Bill Cipher

def acordo_de_bill(rng, v):
    """Bill Cipher: "Temos um acordo?" — a mão apertando e a chama azul acendendo."""
    x = _z(2.0)
    poe(x, _risada(rng, 600, 3, 0.1, 0.03), 0.0)
    poe(x, _baque(300, 200, 0.05, 0.3), 0.33)
    n = n_de(0.7)
    poe(x, satura(passa(rosa(rng, n), 300, 4000, 2), 2) * sobe_e_some(n, 0.15, 1.2) * 0.25, 0.32)
    poe(x, _sino(rng, 988, 0.6, 0.03, CRISTAL), 0.35)
    return reverb(x, 0.6, 0.3)


def realidade_invertida(rng, v):
    """Bill Cipher: a realidade virando (o som de trás para frente) e o escudo."""
    x = _z(2.0)
    n = n_de(0.5)
    rev = (passa(rosa(rng, n), 500, 5000, 2) * env(n, 0.005, 0.45) * 0.3)[::-1]
    poe(x, rev, 0.0)
    poe(x, seno(varre(200, 800, n), n)[::-1] * env(n, 0.01, 0.4)[::-1] * 0.03, 0.0)
    poe(x, _sino(rng, 784, 0.5, 0.03, METAL), 0.48)
    poe(x, _brilho(rng, 0.5, 1175, 0.025, CRISTAL), 0.55)
    return reverb(x, 0.6, 0.3)


def bill_preparo(rng, v):
    """Bill Cipher (Preparo): o triângulo pulsando e o zumbido estranho em laço."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(330, n) * 0.6 + _quadrada(331.5, n) * 0.2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.035, 0.0)
    poe(x, graos(rng, n, 15, 0.0, 0.95, 2000, 6000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.6, 0.3)


def olho_que_tudo_ve(rng, v):
    """Bill Cipher: o olho enorme abrindo no céu (o acorde estranho) e os feixes."""
    x = _z(2.4)
    poe(x, _acorde((233, 247, 349, 370), 1.3, 0.04, 0.2, 1.0), 0.0)
    n = n_de(0.5)
    poe(x, satura(seno(varre(600, 300, n), n), 2) * env(n, 0.02, 0.4) * 0.04, 0.35)
    poe(x, _baque(80, 30, 0.5, 0.7), 0.45)
    poe(x, _risada(rng, 650, 4, 0.1, 0.03), 0.7)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Plankton

def plano_z(rng, v):
    """Plankton: a antena chiando ("bzz") e o pulso que trava todos."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, _quadrada(120, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * _t(n))) * env(n, 0.02, 0.2) * 0.03, 0.0)
    for k in range(4):
        n = n_de(0.3)
        poe(x, seno(varre(800, 200, n), n) * env(n, 0.005, 0.25) * 0.035, 0.15 + 0.1 * k)
    poe(x, estalo(rng, n_de(0.1), 1500, 7000, 0.02) * 0.6, 0.45)
    return reverb(x, 0.5, 0.25)


def plankton_preparo(rng, v):
    """Plankton (Preparo): a risadinha aguda e as antenas zumbindo."""
    x = _z(1.4)
    poe(x, _risada(rng, 900, 4, 0.1, 0.025), 0.1)
    n = n_de(1.0)
    poe(x, seno(1800, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 20 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.008, 0.0)
    return reverb(x, 0.4, 0.2)


def roubar_a_formula(rng, v):
    """Plankton: a garra puxando as garrafinhas (o "plin" de vidro) e o "Finalmente!"."""
    x = _z(2.2)
    for k in range(3):
        poe(x, _sino(rng, 2349 + 200 * k, 0.4, 0.03, CRISTAL), 0.2 + 0.05 * k)
        poe(x, _whoosh(rng, 0.2, 1000, 6000, 0.7, 1.3, 0.3), 0.35 + 0.05 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * env(n, 0.02, 0.3) * 0.25, 0.4)
    poe(x, _acorde((349, 440, 523), 0.7, 0.03, 0.03, 0.5), 0.8)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "briga-com-o-galo": (briga_com_o_galo, "Peter Griffin: a briga com o galo"),
    "ideia-terrivel": (ideia_terrivel, "Peter Griffin: a ideia terrível"),
    "peter-preparo": (peter_preparo, "Peter Griffin: a risadinha (Preparo)"),
    "nhe-he-he": (nhe_he_he, "Peter Griffin: Nhé-hé-hé"),
    "raio-de-controle": (raio_de_controle, "Stewie Griffin: o raio de controle"),
    "plano-mirabolante": (plano_mirabolante, "Stewie Griffin: o plano mirabolante"),
    "stewie-preparo": (stewie_preparo, "Stewie Griffin: as engrenagens (Preparo)"),
    "dominacao-mundial": (dominacao_mundial, "Stewie Griffin: a dominação mundial"),
    "respeitem-minha-autoridade": (respeitem_minha_autoridade, "Eric Cartman: Respeitem minha autoridade"),
    "chantagem": (chantagem, "Eric Cartman: a chantagem"),
    "cartman-preparo": (cartman_preparo, "Eric Cartman: as mãos se esfregando (Preparo)"),
    "plano-egoista": (plano_egoista, "Eric Cartman: o plano egoísta"),
    "acordo-de-bill": (acordo_de_bill, "Bill Cipher: o acordo"),
    "realidade-invertida": (realidade_invertida, "Bill Cipher: a realidade invertida"),
    "bill-preparo": (bill_preparo, "Bill Cipher: o triângulo pulsando (Preparo)"),
    "olho-que-tudo-ve": (olho_que_tudo_ve, "Bill Cipher: o olho que tudo vê"),
    "plano-z": (plano_z, "Plankton: o Plano Z"),
    "plankton-preparo": (plankton_preparo, "Plankton: as antenas (Preparo)"),
    "roubar-a-formula": (roubar_a_formula, "Plankton: roubar a fórmula"),
}
