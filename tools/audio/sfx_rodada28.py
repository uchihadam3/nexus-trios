"""Os sons da rodada 28 das habilidades próprias (veja tools/vfx/familias_v2/rodada28.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _risada(rng, f0, k=4, passo=0.12, g=0.05):
    x = _z(passo * k + 0.3)
    for j in range(k):
        n = n_de(passo * 0.8)
        poe(x, satura(seno(varre(f0 * (1 + 0.05 * (j % 2)), f0 * 0.85, n), n), 2) * env(n, 0.005, passo * 0.6) * g, passo * j)
    return x


# ------------------------------------------------------------------ Genos

def canhao_incinerador(rng, v):
    """Genos: os braços-canhão disparando o fogo largo."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, seno(varre(400, 1200, n), n) * env(n, 0.01, 0.15) * 0.04, 0.0)
    poe(x, _fogo(rng, 1.1, 0.45, 0.15), 0.1)
    poe(x, _baque(100, 50, 0.3, 0.5), 0.1)
    return reverb(x, 0.5, 0.25)


def rajada_de_misseis(rng, v):
    """Genos: os mísseis saindo (os "fuuu") e caindo em sequência."""
    x = _z(2.0)
    for k in range(9):
        poe(x, _whoosh(rng, 0.25, 800, 5000, 0.5, 1.4, 0.18), 0.03 * k)
    for k in range(9):
        poe(x, _baque(140 + 10 * (k % 3), 60, 0.15, 0.35), 0.45 + 0.03 * k)
    poe(x, _explosao(rng, 0.7, 0.4), 0.5)
    return reverb(x, 0.6, 0.3)


def genos_preparo(rng, v):
    """Genos (Preparo): o núcleo sobrecarregando (o zumbido que sobe) e o vapor."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(varre(120, 400, n), n), 2) * sobe_e_some(n, 0.85, 1.2) * 0.06, 0.0)
    for k in range(2):
        poe(x, passa(rosa(rng, n_de(0.3)), 3000, 9000, 2) * env(n_de(0.3), 0.02, 0.25) * 0.15, 0.3 + 0.4 * k)
    return reverb(x, 0.5, 0.25)


def sobrecarga_genos(rng, v):
    """Genos: o feixe incandescente gigante e a explosão."""
    x = _z(2.2)
    n = n_de(0.8)
    poe(x, (satura(seno(varre(150, 90, n), n), 2.5) * 0.08 + passa(rosa(rng, n), 300, 7000, 2) * 0.3) * env(n, 0.005, 0.6, segura=0.2), 0.0)
    poe(x, _explosao(rng, 1.2, 0.9), 0.22)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Hiei

def espada_de_fogo_hiei(rng, v):
    """Hiei: o corte rapidíssimo com as chamas negras crepitando."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.12, 2500, 10000, 0.8, 1.3, 0.45), 0.05)
    poe(x, _fogo(rng, 0.6, 0.25, 0.15), 0.1)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.9, 1000, 5000, 0.004) * 0.25, 0.1)
    return reverb(x, 0.5, 0.25)


def jagan(rng, v):
    """Hiei: o terceiro olho abrindo (o tom estranho) e as chamas negras."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, seno(varre(300, 900, n, 0.5), n) * env(n, 0.05, 0.3) * 0.04, 0.0)
    poe(x, _sino(rng, 1047, 0.6, 0.04, CRISTAL), 0.25)
    poe(x, _fogo(rng, 0.7, 0.3, 0.2), 0.3)
    return reverb(x, 0.7, 0.35)


def hiei_preparo(rng, v):
    """Hiei (Preparo): as chamas negras girando em volta do braço."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 150, 2500, 2), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.25, 0.0)
    poe(x, satura(seno(70, n), 2) * sobe_e_some(n, 0.7, 1.2) * 0.04, 0.0)
    return reverb(x, 0.6, 0.3)


def dragao_das_trevas(rng, v):
    """Hiei: o rugido do dragão negro e a onda de fogo."""
    x = _z(2.3)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(140, 70, n) * (1 + 0.05 * np.sin(2 * math.pi * 20 * t)), n) + passa(rosa(rng, n), 150, 2500, 2) * 0.8, 3) * env(n, 0.05, 0.8) * 0.11, 0.0)
    poe(x, _fogo(rng, 1.2, 0.4, 0.3), 0.1)
    poe(x, _baque(55, 25, 0.6, 0.8, 2.8), 0.5)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Sailor Moon

def cura_lunar(rng, v):
    """Sailor Moon: o cetro lunar (o arpejo de caixinha de música) e a luz caindo."""
    x = _z(2.2)
    for k, f in enumerate((784, 988, 1175, 1568, 1319, 1175)):
        poe(x, _sino(rng, f, 0.6, 0.04, CRISTAL), 0.05 + 0.1 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.2, 0.04, 0.2, 0.9), 0.4)
    poe(x, _brilho(rng, 1.0, 2349, 0.04, CRISTAL), 0.4)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Coringa

def gas_do_riso(rng, v):
    """Coringa: o gás saindo (o chiado) e as risadas."""
    x = _z(2.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.2, 1.2) * 0.25, 0.0)
    poe(x, _risada(rng, 320, 5, 0.12, 0.05), 0.35)
    return reverb(x, 0.6, 0.3)


def carta_marcada(rng, v):
    """Coringa: a carta girando no ar e cravando, com o risinho."""
    x = _z(1.9)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t) ** 2) * env(n, 0.01, 0.4) * 0.2, 0.05)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005), 0.48)
    poe(x, _risada(rng, 360, 3, 0.1, 0.04), 0.6)
    return reverb(x, 0.5, 0.25)


def piada_final(rng, v):
    """Coringa: a caixa-surpresa (a musiquinha de manivela), o "boing" da mola e a explosão."""
    x = _z(2.2)
    for k, f in enumerate((523, 587, 659, 523, 659)):
        poe(x, _sino(rng, f * 2, 0.15, 0.03, SINO), 0.04 * k)
    poe(x, seno(varre(200, 600, n_de(0.25)), n_de(0.25)) * env(n_de(0.25), 0.005, 0.2) * 0.05, 0.25)
    poe(x, _risada(rng, 300, 3, 0.1, 0.05), 0.35)
    poe(x, _explosao(rng, 1.0, 0.8), 0.55)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Arlequina

def marreta_arlequina(rng, v):
    """Arlequina: a marreta girando e o "BONK" com o assobio de desenho."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.35, 300, 3000, 0.9, 1.3, 0.45), 0.0)
    poe(x, _baque(200, 90, 0.2, 0.6, 2.0), 0.38)
    poe(x, _sino(rng, 900, 0.3, 0.05, METAL), 0.38)
    poe(x, _piu(1200, 600, 0.25, 0.04), 0.45)
    return reverb(x, 0.4, 0.2)


def pirueta(rng, v):
    """Arlequina: a pirueta (o "uii" e o giro) e o chute."""
    x = _z(1.8)
    poe(x, _piu(600, 1200, 0.2, 0.04), 0.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 1000, 5000, 0.6, 1.4, 0.25), 0.05 + 0.12 * k)
    poe(x, _baque(150, 70, 0.3, 0.6), 0.58)
    return reverb(x, 0.4, 0.2)


def surpresa_explosiva(rng, v):
    """Arlequina: as bombinhas assobiando e estourando uma atrás da outra."""
    x = _z(2.1)
    for k in range(6):
        n = n_de(0.3)
        poe(x, seno(varre(1600, 800, n), n) * env(n, 0.01, 0.25) * 0.02, 0.03 * k)
        poe(x, _explosao(rng, 0.4, 0.25), 0.4 + 0.03 * k)
    poe(x, _sino(rng, 1568, 0.4, 0.03, CRISTAL), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Darkseid

def feixe_omega(rng, v):
    """Darkseid: os olhos acendendo e os dois feixes Ômega fazendo curva."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, satura(seno(varre(60, 80, n), n), 3) * env(n, 0.03, 0.25) * 0.08, 0.0)
    for k in range(2):
        m = n_de(0.5)
        poe(x, (seno(varre(500 + 100 * k, 1100, m), m) * 0.03 + passa(rosa(rng, m), 2000, 8000, 2) * 0.1) * env(m, 0.005, 0.4), 0.15)
    poe(x, _baque(110, 50, 0.4, 0.7, 2.4), 0.55)
    return reverb(x, 0.6, 0.3)


def darkseid_preparo(rng, v):
    """Darkseid (Preparo): a Equação Anti-Vida se formando (o coro grave e os sussurros)."""
    x = _z(1.5)
    poe(x, _acorde((55, 82, 110), 1.2, 0.05, 0.3, 1.0), 0.0)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 2000, 6000, 2) * sobe_e_some(n, 0.5, 1.4) * 0.08, 0.1)
    return reverb(x, 0.8, 0.4)


def anti_vida(rng, v):
    """Darkseid: a Equação descendo e prendendo a mente (o tom que aperta)."""
    x = _z(2.2)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.15, 0.0)
    m = n_de(0.8)
    poe(x, satura(seno(varre(150, 300, m), m), 2) * env(m, 0.05, 0.6) * 0.06, 0.4)
    poe(x, _acorde((110, 131, 156), 1.0, 0.05, 0.05, 0.8), 0.45)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Lex Luthor

def plano_calculado(rng, v):
    """Lex Luthor: a caneta riscando o plano (os bipes da armadura) e o tiro certeiro."""
    x = _z(2.0)
    for k in range(5):
        n = n_de(0.06)
        poe(x, passa(rosa(rng, n), 2500, 7000, 2) * env(n, 0.005, 0.05) * 0.2, 0.05 + 0.06 * k)
    for k in range(3):
        poe(x, _quadrada(1200 + 200 * k, n_de(0.05)) * env(n_de(0.05), 0.003, 0.04) * 0.02, 0.35 + 0.05 * k)
    n = n_de(0.3)
    poe(x, (seno(varre(1500, 600, n), n) * 0.04 + passa(rosa(rng, n), 2000, 8000, 2) * 0.15) * env(n, 0.003, 0.25), 0.5)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.55)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "canhao-incinerador": (canhao_incinerador, "Genos: o canhão incinerador"),
    "rajada-de-misseis": (rajada_de_misseis, "Genos: a rajada de mísseis"),
    "genos-preparo": (genos_preparo, "Genos: o núcleo (Preparo)"),
    "sobrecarga-genos": (sobrecarga_genos, "Genos: a sobrecarga"),
    "espada-de-fogo-hiei": (espada_de_fogo_hiei, "Hiei: a espada de fogo"),
    "jagan": (jagan, "Hiei: o Jagan"),
    "hiei-preparo": (hiei_preparo, "Hiei: as chamas negras (Preparo)"),
    "dragao-das-trevas": (dragao_das_trevas, "Hiei: o Dragão das Trevas"),
    "cura-lunar": (cura_lunar, "Sailor Moon: a cura lunar"),
    "gas-do-riso": (gas_do_riso, "Coringa: o gás do riso"),
    "carta-marcada": (carta_marcada, "Coringa: a carta marcada"),
    "piada-final": (piada_final, "Coringa: a piada final"),
    "marreta-arlequina": (marreta_arlequina, "Arlequina: a marreta"),
    "pirueta": (pirueta, "Arlequina: a pirueta"),
    "surpresa-explosiva": (surpresa_explosiva, "Arlequina: a surpresa explosiva"),
    "feixe-omega": (feixe_omega, "Darkseid: o Feixe Ômega"),
    "darkseid-preparo": (darkseid_preparo, "Darkseid: a equação (Preparo)"),
    "anti-vida": (anti_vida, "Darkseid: a Equação Anti-Vida"),
    "plano-calculado": (plano_calculado, "Lex Luthor: o plano calculado"),
}
