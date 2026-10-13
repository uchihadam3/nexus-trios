"""Os sons da rodada 49 das habilidades próprias (veja tools/vfx/familias_v2/rodada49.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 200, 3000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


def _areia(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 1500, 9000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t + np.sin(2 * math.pi * 0.9 * t) * 3)) * sobe_e_some(n, 0.3, 1.2) * g


def _asas(rng, n_bat, intervalo, g=0.3):
    x = _z(n_bat * intervalo + 0.2)
    for k in range(n_bat):
        n = n_de(0.08)
        poe(x, passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.01, 0.07) * g, k * intervalo)
    return x


def _egipcio(fs, seg, g=0.02):
    """O acorde da escala egípcia (com a segunda menor)."""
    n = n_de(seg)
    t = _t(n)
    x = sum(seno(f, n) * (1.0 / (1 + k)) for k, f in enumerate(fs))
    return x * (0.7 + 0.3 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.3, 1.2) * g


# ------------------------------------------------------------------ Anúbis

def cajado_do_juizo(rng, v):
    """Anúbis: o cajado batendo e o selo da maldição soando grave."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 300, 3000, 0.8, 1.3, 0.4), 0.0)
    poe(x, _baque(120, 50, 0.35, 0.6), 0.28)
    poe(x, _sino(rng, 220, 1.0, 0.04, METAL), 0.3)
    poe(x, _egipcio((147, 156, 220), 0.9, 0.02), 0.4)
    return reverb(x, 0.8, 0.4)


def guia_das_almas(rng, v):
    """Anúbis: o portal do Duat abrindo e a alma subindo de volta ao corpo."""
    x = _z(2.4)
    n = n_de(0.4)
    poe(x, seno(varre(80, 120, n), n) * env(n, 0.2, 0.15) * 0.04, 0.0)
    poe(x, _sopro(rng, 0.8, 300, 3000, 0.15, 0.5), 0.2)
    n2 = n_de(0.6)
    poe(x, seno(varre(300, 900, n2), n2) * env(n2, 0.4, 0.15) * 0.02, 0.25)
    poe(x, _acorde((294, 440, 587, 880), 1.0, 0.022), 0.65)
    poe(x, _brilho(rng, 0.8, 1760, 0.015, CRISTAL), 0.7)
    return reverb(x, 0.9, 0.45)


def anubis_preparo(rng, v):
    """Anúbis (Preparo): a balança rangendo e o coro egípcio grave (em laço)."""
    x = _z(1.4)
    poe(x, _egipcio((110, 117, 165), 1.0, 0.02), 0.0)
    for k in range(2):
        poe(x, _sino(rng, 880 + 100 * k, 0.3, 0.008, METAL), 0.5 * k + 0.2)
    return reverb(x, 0.8, 0.4)


def julgamento_de_anubis(rng, v):
    """Anúbis: a balança pesando ("tlim... tlim") e o veredito caindo no rival."""
    x = _z(2.3)
    poe(x, _sino(rng, 1319, 0.4, 0.02, METAL), 0.05)
    poe(x, _sino(rng, 1175, 0.4, 0.02, METAL), 0.2)
    n = n_de(0.2)
    poe(x, seno(varre(400, 200, n), n) * env(n, 0.05, 0.15) * 0.02, 0.3)
    poe(x, _baque(55, 20, 0.9, 1.0, 3.0), 0.45)
    poe(x, _explosao(rng, 0.5, 55), 0.45)
    poe(x, _egipcio((147, 156, 220, 294), 0.9, 0.02), 0.5)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Rá

def raio_solar_ra(rng, v):
    """Rá: o disco solar acendendo e o feixe chiando de calor."""
    x = _z(2.0)
    poe(x, _acorde((440, 554, 659), 0.6, 0.02), 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.05, 0.3) * 0.25, 0.2)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.35)
    poe(x, _fogo(rng, 0.6, 0.25), 0.4)
    return reverb(x, 0.6, 0.3)


def clarao_de_ra(rng, v):
    """Rá: o olho do sol abrindo e o clarão branco ("vuuumm")."""
    x = _z(2.2)
    n = n_de(0.4)
    poe(x, seno(varre(200, 800, n), n) * env(n, 0.35, 0.05) * 0.025, 0.0)
    poe(x, _acorde((523, 659, 784, 1047, 1319), 1.0, 0.03), 0.35)
    n2 = n_de(0.5)
    poe(x, passa(rosa(rng, n2), 3000, 11000, 2) * env(n2, 0.01, 0.45) * 0.25, 0.35)
    return reverb(x, 0.8, 0.4)


def ra_preparo(rng, v):
    """Rá (Preparo): o sol crescendo e a serpente sibilando (em laço)."""
    x = _z(1.4)
    poe(x, _egipcio((220, 233, 330), 1.0, 0.02), 0.0)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.08, 0.4)
    return reverb(x, 0.7, 0.35)


def furia_de_ra(rng, v):
    """Rá: o sol enorme e os três raios queimando os rivais."""
    x = _z(2.4)
    poe(x, _acorde((220, 277, 330, 440), 1.0, 0.025), 0.0)
    for k in range(3):
        n = n_de(0.3)
        poe(x, passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.03, 0.25) * 0.25, 0.3 + 0.05 * k)
        poe(x, _baque(110, 45, 0.3, 0.55), 0.45 + 0.05 * k)
    poe(x, _fogo(rng, 0.9, 0.35), 0.5)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Set

def tempestade_de_areia_set(rng, v):
    """Set: a tempestade de areia uivando e girando nos rivais."""
    x = _z(2.4)
    poe(x, _areia(rng, 1.4, 0.4), 0.0)
    poe(x, _sopro(rng, 1.2, 150, 1200, 0.25, 0.4), 0.1)
    return reverb(x, 0.7, 0.35)


def cetro_do_caos(rng, v):
    """Set: o cetro batendo e o chão rachando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.3, 200, 3000, 0.85, 1.3, 0.45), 0.0)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.28)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 200, 3000, 0.012) * 0.5, 0.32 + 0.05 * k)
    poe(x, _egipcio((147, 156), 0.6, 0.015), 0.4)
    return reverb(x, 0.6, 0.3)


def set_preparo(rng, v):
    """Set (Preparo): a adaga saindo da bainha devagar e o riso abafado (em laço)."""
    x = _z(1.4)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.0)
    for k in range(3):
        n2 = n_de(0.1)
        poe(x, satura(seno(varre(160, 140, n2), n2), 3) * env(n2, 0.01, 0.08) * 0.02, 0.6 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def traicao_de_set(rng, v):
    """Set: o vulto surgindo ("fsss") e a facada pelas costas."""
    x = _z(2.0)
    poe(x, _sopro(rng, 0.25, 500, 3000, 0.2, 0.3), 0.0)
    poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.7, 1.3, 0.4), 0.25)
    poe(x, _baque(100, 40, 0.4, 0.8, 2.6), 0.4)
    poe(x, _sino(rng, 1760, 0.4, 0.025, METAL), 0.4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Ísis

def bencao_de_isis(rng, v):
    """Ísis: as asas abrindo e a luz turquesa curando (o acorde suave)."""
    x = _z(2.2)
    poe(x, _asas(rng, 3, 0.1, 0.25), 0.0)
    poe(x, _acorde((440, 554, 659, 880), 1.0, 0.022), 0.25)
    poe(x, _brilho(rng, 0.8, 1760, 0.015, CRISTAL), 0.35)
    return reverb(x, 0.8, 0.4)


def purificacao_de_isis(rng, v):
    """Ísis: o ankh soando e os debuffs se desfazendo."""
    x = _z(2.2)
    poe(x, _sino(rng, 659, 1.0, 0.04, SINO), 0.0)
    for k in range(3):
        poe(x, _piu(1500, 2500, 0.15, 0.015), 0.4 + 0.06 * k)
    poe(x, _acorde((523, 659, 784), 0.8, 0.02), 0.45)
    return reverb(x, 0.8, 0.4)


def isis_preparo(rng, v):
    """Ísis (Preparo): as asas batendo devagar em volta do ankh (em laço)."""
    x = _z(1.4)
    poe(x, _asas(rng, 2, 0.5, 0.2), 0.0)
    n = n_de(1.0)
    poe(x, (seno(440, n) + seno(659, n) * 0.5) * sobe_e_some(n, 0.5, 1.2) * 0.01, 0.0)
    return reverb(x, 0.7, 0.35)


def ressurreicao_de_isis(rng, v):
    """Ísis: o ankh gigante acendendo, o coro subindo e o aliado voltando."""
    x = _z(2.6)
    n = n_de(0.6)
    poe(x, seno(varre(200, 600, n), n) * env(n, 0.5, 0.1) * 0.025, 0.0)
    poe(x, _acorde((294, 440, 587, 740, 880), 1.4, 0.025), 0.4)
    poe(x, _brilho(rng, 1.0, 1760, 0.02, CRISTAL), 0.55)
    poe(x, _baque(150, 90, 0.2, 0.3), 0.6)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Hórus

def _grito_falcao(rng, g=0.025):
    n = n_de(0.35)
    return satura(seno(varre(2400, 1600, n), n), 2) * env(n, 0.02, 0.3) * g


def garras_do_falcao(rng, v):
    """Hórus: o grito do falcão, o mergulho e as garras rasgando."""
    x = _z(2.0)
    poe(x, _grito_falcao(rng), 0.0)
    poe(x, _whoosh(rng, 0.25, 800, 6000, 0.85, 1.3, 0.4), 0.05)
    for k in range(2):
        for m in range(3):
            n = n_de(0.08)
            poe(x, satura(passa(rosa(rng, n), 1500, 9000, 2), 2) * env(n, 0.004, 0.07) * 0.3, 0.26 + 0.12 * k + 0.015 * m)
        poe(x, _baque(170, 80, 0.15, 0.35), 0.28 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def olho_de_horus(rng, v):
    """Hórus: o olho abrindo ("vung") e a mira travando."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, (seno(varre(200, 600, n), n) + seno(varre(300, 900, n), n) * 0.5) * env(n, 0.2, 0.08) * 0.025, 0.05)
    poe(x, _egipcio((294, 311, 440), 0.7, 0.018), 0.3)
    poe(x, _sino(rng, 1760, 0.4, 0.02, METAL), 0.5)
    poe(x, _sino(rng, 2349, 0.3, 0.012, METAL), 0.56)
    return reverb(x, 0.7, 0.35)


def horus_preparo(rng, v):
    """Hórus (Preparo): as asas batendo e o grito do falcão longe (em laço)."""
    x = _z(1.4)
    poe(x, _asas(rng, 3, 0.33, 0.2), 0.0)
    poe(x, _grito_falcao(rng, 0.012), 0.45)
    return reverb(x, 0.7, 0.35)


def voo_do_falcao(rng, v):
    """Hórus: o falcão mergulhando do alto (o assobio) e o impacto."""
    x = _z(2.2)
    poe(x, _grito_falcao(rng, 0.03), 0.0)
    n = n_de(0.4)
    poe(x, seno(varre(1800, 500, n), n) * env(n, 0.3, 0.05) * 0.02, 0.05)
    poe(x, _whoosh(rng, 0.38, 1000, 8000, 0.9, 1.3, 0.5), 0.05)
    poe(x, _baque(70, 28, 0.6, 0.9, 2.8), 0.42)
    poe(x, _explosao(rng, 0.5, 70), 0.42)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Sekhmet

def _rugido(rng, seg, g=0.06):
    n = n_de(seg)
    return satura(seno(varre(140, 90, n), n) + passa(rosa(rng, n), 100, 1500, 2) * 1.0, 5) * env(n, 0.05, seg * 0.6) * g


def garras_da_leoa(rng, v):
    """Sekhmet: as patas de leoa rasgando duas vezes."""
    x = _z(1.8)
    for k in range(2):
        for m in range(4):
            n = n_de(0.09)
            poe(x, satura(passa(rosa(rng, n), 1200, 8000, 2), 2) * env(n, 0.004, 0.08) * 0.28, 0.08 + 0.17 * k + 0.012 * m)
        poe(x, _baque(150, 70, 0.2, 0.45), 0.12 + 0.17 * k)
    return reverb(x, 0.4, 0.2)


def rugido_de_sekhmet(rng, v):
    """Sekhmet: o rugido da leoa ecoando nos rivais."""
    x = _z(2.2)
    poe(x, _rugido(rng, 0.9, 0.07), 0.05)
    n = n_de(0.8)
    poe(x, seno(55, n) * sobe_e_some(n, 0.2, 1.2) * 0.04, 0.1)
    return reverb(x, 0.9, 0.45)


def sekhmet_preparo(rng, v):
    """Sekhmet (Preparo): a juba em chamas crepitando e o rosnado (em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.0, 0.22), 0.0)
    poe(x, _rugido(rng, 0.5, 0.025), 0.4)
    return reverb(x, 0.6, 0.3)


def furia_da_leoa(rng, v):
    """Sekhmet: o salto, as garras e a vida voltando (o tom que sobe)."""
    x = _z(2.2)
    poe(x, _rugido(rng, 0.35, 0.05), 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 4000, 0.85, 1.3, 0.45), 0.0)
    for k in range(2):
        for m in range(4):
            n = n_de(0.09)
            poe(x, satura(passa(rosa(rng, n), 1200, 8000, 2), 2) * env(n, 0.004, 0.08) * 0.3, 0.28 + 0.07 * k + 0.012 * m)
    poe(x, _baque(90, 35, 0.5, 0.8, 2.6), 0.3)
    n2 = n_de(0.5)
    poe(x, seno(varre(300, 700, n2), n2) * env(n2, 0.1, 0.3) * 0.02, 0.55)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "cajado-do-juizo": (cajado_do_juizo, "Anúbis: o cajado do juízo"),
    "guia-das-almas": (guia_das_almas, "Anúbis: o guia das almas"),
    "anubis-preparo": (anubis_preparo, "Anúbis: a balança (Preparo)"),
    "julgamento-de-anubis": (julgamento_de_anubis, "Anúbis: o julgamento"),
    "raio-solar-ra": (raio_solar_ra, "Rá: o raio solar"),
    "clarao-de-ra": (clarao_de_ra, "Rá: o clarão"),
    "ra-preparo": (ra_preparo, "Rá: o sol crescendo (Preparo)"),
    "furia-de-ra": (furia_de_ra, "Rá: a fúria de Rá"),
    "tempestade-de-areia-set": (tempestade_de_areia_set, "Set: a tempestade de areia"),
    "cetro-do-caos": (cetro_do_caos, "Set: o cetro de Set"),
    "set-preparo": (set_preparo, "Set: a adaga escondida (Preparo)"),
    "traicao-de-set": (traicao_de_set, "Set: a traição"),
    "bencao-de-isis": (bencao_de_isis, "Ísis: a bênção"),
    "purificacao-de-isis": (purificacao_de_isis, "Ísis: a purificação"),
    "isis-preparo": (isis_preparo, "Ísis: as asas e o ankh (Preparo)"),
    "ressurreicao-de-isis": (ressurreicao_de_isis, "Ísis: a ressurreição"),
    "garras-do-falcao": (garras_do_falcao, "Hórus: as garras do falcão"),
    "olho-de-horus": (olho_de_horus, "Hórus: o olho que tudo vê"),
    "horus-preparo": (horus_preparo, "Hórus: as asas (Preparo)"),
    "voo-do-falcao": (voo_do_falcao, "Hórus: o voo do falcão"),
    "garras-da-leoa": (garras_da_leoa, "Sekhmet: as garras da leoa"),
    "rugido-de-sekhmet": (rugido_de_sekhmet, "Sekhmet: o rugido"),
    "sekhmet-preparo": (sekhmet_preparo, "Sekhmet: a juba em chamas (Preparo)"),
    "furia-da-leoa": (furia_da_leoa, "Sekhmet: a fúria da leoa"),
}
