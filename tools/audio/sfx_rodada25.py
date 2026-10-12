"""Os sons da rodada 25 das habilidades próprias (veja tools/vfx/familias_v2/rodada25.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _areia(rng, seg, g=0.3, pico=0.4):
    n = n_de(seg)
    return passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, pico, 1.2) * g


# ------------------------------------------------------------------ Hayabusa

def lamina_do_dragao(rng, v):
    """Hayabusa: o saque rapidíssimo da Espada do Dragão e o rastro."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.15, 3000, 12000, 0.8, 1.3, 0.5), 0.05)
    poe(x, _sino(rng, 3600, 0.5, 0.05, METAL), 0.1)
    poe(x, _sopro(rng, 0.5, 1000, 5000, 0.12, 0.3), 0.2)
    return reverb(x, 0.5, 0.25)


def arte_do_vento(rng, v):
    """Hayabusa: os redemoinhos de vento cortando."""
    x = _z(1.9)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.05)
    for k in range(5):
        poe(x, _whoosh(rng, 0.08, 2500, 9000, 0.6, 1.4, 0.25), 0.3 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def izuna_otoshi(rng, v):
    """Hayabusa: o salto, o giro no ar e o rival jogado de cabeça no chão."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.3, 300, 3000, 0.7, 1.4, 0.4), 0.0)
    n = n_de(0.25)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 16 * t) ** 2) * env(n, 0.01, 0.2) * 0.3, 0.3)
    poe(x, _baque(60, 25, 0.6, 1.0, 3.0), 0.68)
    poe(x, passa(rosa(rng, n_de(0.3)), 100, 2000, 2) * env(n_de(0.3), 0.002, 0.2) * 0.4, 0.68)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Cabeça de Pirâmide

def presenca_opressiva(rng, v):
    """Cabeça de Pirâmide: a sirene de Silent Hill e os passos pesados."""
    x = _z(2.2)
    n = n_de(1.6)
    t = _t(n)
    f = 300 + 200 * (0.5 - 0.5 * np.cos(2 * math.pi * 0.7 * t))
    poe(x, np.sin(2 * math.pi * np.cumsum(f) / 44100) * sobe_e_some(n, 0.4, 1.0) * 0.04, 0.0)
    for k in range(2):
        poe(x, _baque(70, 35, 0.4, 0.7, 2.2), 0.4 + 0.5 * k)
    return reverb(x, 0.8, 0.4)


def pyramidhead_preparo(rng, v):
    """Cabeça de Pirâmide (Preparo): a Grande Faca arrastando no chão (o raspar de metal)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 7 * t)) * env(n, 0.05, 0.8, segura=0.5) * 0.25, 0.0)
    poe(x, graos(rng, n, 30, 0.0, 0.9, 2000, 7000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.6, 0.3)


def sentenca(rng, v):
    """Cabeça de Pirâmide: a Grande Faca caindo com todo o peso."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.3, 150, 2000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(45, 22, 0.9, 1.0, 3.2), 0.28)
    poe(x, _sino(rng, 400, 0.8, 0.06, METAL), 0.28)
    poe(x, _explosao(rng, 0.8, 0.4), 0.3)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Kirby

def inalar(rng, v):
    """Kirby: a sucção (o vento puxando) e o "pop" quando engole."""
    x = _z(1.9)
    n = n_de(0.75)
    poe(x, passa(rosa(rng, n), 400, 4000, 2) * sobe_e_some(n, 0.85, 1.0) * 0.35, 0.05)
    poe(x, _piu(600, 200, 0.12, 0.06), 0.75)
    poe(x, _baque(200, 120, 0.1, 0.3), 0.78)
    return reverb(x, 0.4, 0.2)


def copia_de_poder(rng, v):
    """Kirby: o brilho da cópia (o arpejo de estrela) e o chapéu novo."""
    x = _z(1.9)
    for k, f in enumerate((784, 988, 1175, 1568)):
        poe(x, _quadrada(f, n_de(0.08)) * env(n_de(0.08), 0.003, 0.06) * 0.02, 0.3 + 0.06 * k)
    poe(x, _brilho(rng, 0.7, 2349, 0.05, CRISTAL), 0.35)
    poe(x, _piu(500, 1000, 0.1, 0.05), 0.6)
    return reverb(x, 0.5, 0.25)


def super_inalacao(rng, v):
    """Kirby: o redemoinho enorme sugando e a estrela cuspida."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 200, 4000, 2), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 10 * t)) * sobe_e_some(n, 0.8, 1.0) * 0.35, 0.0)
    poe(x, _piu(400, 1200, 0.12, 0.06), 0.55)
    poe(x, _whoosh(rng, 0.25, 1000, 6000, 0.5, 1.4, 0.35), 0.55)
    poe(x, _baque(150, 70, 0.3, 0.6), 0.82)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Simon

def vampire_killer(rng, v):
    """Simon: o chicote de corrente estalando e enrolando."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.3, 500, 4000, 0.8, 1.4, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.008) * 1.2, 0.32)
    poe(x, _corrente(rng, 0.35, 8, 0.3), 0.4)
    return reverb(x, 0.6, 0.3)


def cruz_arremessada(rng, v):
    """Simon: a cruz girando (o zumbido de bumerangue) indo e voltando."""
    x = _z(1.9)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * t) ** 2) * (0.4 + 0.6 * np.sin(math.pi * t / 0.9)) * 0.3, 0.05)
    poe(x, _sino(rng, 1568, 0.4, 0.05, SINO), 0.45)
    poe(x, _baque(170, 80, 0.15, 0.4), 0.45)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Príncipe

def rebobinar(rng, v):
    """Príncipe: o tempo voltando (o som ao contrário) e a areia."""
    x = _z(2.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * np.linspace(0.05, 1, n) ** 3 * 0.3, 0.0)
    poe(x, seno(varre(200, 900, n, 2), n) * np.linspace(0.05, 1, n) ** 2 * 0.04, 0.0)
    poe(x, _areia(rng, 0.8, 0.25), 0.4)
    poe(x, _sino(rng, 1047, 0.5, 0.04, CRISTAL), 0.8)
    return reverb(x, 0.7, 0.35)


def prince_preparo(rng, v):
    """Príncipe (Preparo): a areia girando em volta da Adaga."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.7, 1.0) * 0.25, 0.0)
    poe(x, _sino(rng, 1319, 0.5, 0.03, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


def tempestade_de_areia(rng, v):
    """Príncipe: a tempestade de areia varrendo tudo."""
    x = _z(2.1)
    poe(x, _areia(rng, 1.6, 0.4, 0.4), 0.0)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 150, 1200, 2) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.05)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Alucard

def forma_de_nevoa(rng, v):
    """Alucard: o corpo virando névoa (o sopro) e os morcegos."""
    x = _z(2.0)
    poe(x, _sopro(rng, 0.8, 300, 3000, 0.25, 0.4), 0.0)
    for k in range(8):
        poe(x, passa(rosa(rng, n_de(0.05)), 1000, 4000, 2) * env(n_de(0.05), 0.003, 0.03) * 0.25, 0.25 + 0.06 * k)
    poe(x, _piu(6000, 7000, 0.05, 0.02), 0.4)
    return reverb(x, 0.7, 0.35)


def alucard_preparo(rng, v):
    """Alucard (Preparo): as almas girando (os gemidos baixos)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(300, 260, n) * (1 + 0.04 * np.sin(2 * math.pi * 4 * t)), n) * sobe_e_some(n, 0.5, 1.2) * 0.04, 0.0)
    poe(x, seno(varre(450, 400, n) * (1 + 0.04 * np.sin(2 * math.pi * 5 * t)), n) * sobe_e_some(n, 0.6, 1.2) * 0.03, 0.0)
    return reverb(x, 0.8, 0.4)


def ataque_da_alma(rng, v):
    """Alucard: as almas uivando voam e explodem."""
    x = _z(2.0)
    for k in range(4):
        n = n_de(0.4)
        poe(x, seno(varre(700 - 50 * k, 400, n), n) * env(n, 0.02, 0.35) * 0.03, 0.05 + 0.05 * k)
    poe(x, _explosao(rng, 0.8, 0.6), 0.5)
    poe(x, _acorde((147, 175, 220), 0.7, 0.04, 0.02, 0.5), 0.5)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Seiya

def cosmo_ardente(rng, v):
    """Seiya: o cosmo queimando (o tom que sobe) e as estrelas da constelação."""
    x = _z(2.0)
    n = n_de(1.0)
    poe(x, (seno(varre(200, 500, n), n) * 0.05 + passa(rosa(rng, n), 800, 4000, 2) * 0.15) * sobe_e_some(n, 0.5, 1.2), 0.0)
    for k in range(5):
        poe(x, _sino(rng, 1568 + 200 * k, 0.4, 0.03, CRISTAL), 0.3 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


def seiya_preparo(rng, v):
    """Seiya (Preparo): o cosmo concentrando numa esfera (o zumbido que cresce)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(150, 350, n), n) * (1 + 0.05 * np.sin(2 * math.pi * 9 * t)) * 0.05 + passa(rosa(rng, n), 1000, 5000, 2) * 0.1) * sobe_e_some(n, 0.85, 1.2), 0.0)
    return reverb(x, 0.5, 0.25)


def cometa_de_pegaso(rng, v):
    """Seiya: "Cometa de Pégaso!" e a explosão do cosmo."""
    x = _z(2.1)
    n = n_de(0.45)
    poe(x, (seno(varre(500, 300, n), n) * 0.05 + passa(rosa(rng, n), 600, 6000, 2) * 0.25) * env(n, 0.01, 0.4), 0.05)
    poe(x, _explosao(rng, 1.0, 0.8), 0.42)
    poe(x, _acorde((294, 370, 440, 587), 0.9, 0.045, 0.01, 0.7), 0.42)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "lamina-do-dragao": (lamina_do_dragao, "Hayabusa: a Lâmina do Dragão"),
    "arte-do-vento": (arte_do_vento, "Hayabusa: a Arte do Vento"),
    "izuna-otoshi": (izuna_otoshi, "Hayabusa: Izuna Otoshi"),
    "presenca-opressiva": (presenca_opressiva, "Cabeça de Pirâmide: a presença"),
    "pyramidhead-preparo": (pyramidhead_preparo, "Cabeça de Pirâmide: a faca arrastada (Preparo)"),
    "sentenca": (sentenca, "Cabeça de Pirâmide: a sentença"),
    "inalar": (inalar, "Kirby: inalar"),
    "copia-de-poder": (copia_de_poder, "Kirby: a cópia de poder"),
    "super-inalacao": (super_inalacao, "Kirby: a super inalação"),
    "vampire-killer": (vampire_killer, "Simon: o Vampire Killer"),
    "cruz-arremessada": (cruz_arremessada, "Simon: a cruz"),
    "rebobinar": (rebobinar, "Príncipe: rebobinar"),
    "prince-preparo": (prince_preparo, "Príncipe: a areia (Preparo)"),
    "tempestade-de-areia": (tempestade_de_areia, "Príncipe: a tempestade de areia"),
    "forma-de-nevoa": (forma_de_nevoa, "Alucard: a forma de névoa"),
    "alucard-preparo": (alucard_preparo, "Alucard: as almas (Preparo)"),
    "ataque-da-alma": (ataque_da_alma, "Alucard: o ataque da alma"),
    "cosmo-ardente": (cosmo_ardente, "Seiya: o cosmo ardente"),
    "seiya-preparo": (seiya_preparo, "Seiya: o cosmo (Preparo)"),
    "cometa-de-pegaso": (cometa_de_pegaso, "Seiya: o Cometa de Pégaso"),
}
