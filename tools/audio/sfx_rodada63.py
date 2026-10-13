"""Os sons da rodada 63 das habilidades próprias (veja tools/vfx/familias_v2/rodada63.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, f0=200, f1=3000):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), f0, f1, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


def _pew(rng, g=0.025):
    """O disparo de desenho antigo ("pew")."""
    n = n_de(0.1)
    return seno(varre(1400, 500, n), n) * env(n, 0.003, 0.07) * g


def _grito(rng, seg, f0=140, g=0.06):
    """O grito do dragão: a voz grave e áspera, com o eco."""
    n = n_de(seg)
    t = _t(n)
    voz = satura(seno(varre(f0, f0 * 0.8, n), n) * (1 + 0.3 * np.sin(2 * math.pi * 25 * t)) + passa(rosa(rng, n), 150, 2500, 2) * 0.7, 4)
    return voz * env(n, 0.02, seg * 0.6) * g


def _boing(rng, f=300, g=0.04):
    n = n_de(0.25)
    t = _t(n)
    return seno(f * (1 + 0.5 * np.exp(-t * 15) * np.sin(2 * math.pi * 12 * t)), n) * env(n, 0.005, 0.2) * g


# ------------------------------------------------------------------ Cuphead

def disparo_de_dedo(rng, v):
    """Cuphead: a rajada de ervilhas ("pew-pew-pew") e o jazz no fundo."""
    x = _z(2.0)
    for k in range(7):
        poe(x, _pew(rng, 0.025), 0.12 + 0.07 * k)
        poe(x, _baque(300, 180, 0.05, 0.15, 1.5), 0.3 + 0.07 * k)
    poe(x, _acorde((233, 294, 349, 415), 0.6, 0.012), 0.1)
    return reverb(x, 0.6, 0.3)


def dash_cuphead(rng, v):
    """Cuphead: o dash ("zip!") e a poeira de desenho."""
    x = _z(1.9)
    n = n_de(0.2)
    poe(x, seno(varre(400, 2000, n), n) * env(n, 0.01, 0.15) * 0.03, 0.1)
    poe(x, _whoosh(rng, 0.25, 800, 5000, 0.4, 1.3, 0.35), 0.1)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * env(n, 0.005, 0.1) * 0.15, 0.15)
    return reverb(x, 0.5, 0.25)


def cuphead_preparo(rng, v):
    """Cuphead (Preparo): as cartas de super enchendo ("plim-plim") em laço."""
    x = _z(1.4)
    for k in range(5):
        poe(x, _brilho(rng, 0.2, 784 + 98 * k, 0.02, CRISTAL), 0.1 + 0.22 * k)
    return reverb(x, 0.6, 0.3)


def super_art_cuphead(rng, v):
    """Cuphead: o Super Art (o raio gigante em espiral com a fanfarra)."""
    x = _z(2.6)
    poe(x, _acorde((349, 440, 523, 698), 0.4, 0.025), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(300, 900, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 20 * t)) + passa(rosa(rng, n), 500, 6000, 2) * 0.6) * env(n, 0.05, 0.5) * 0.08, 0.2)
    poe(x, _baque(45, 18, 0.9, 0.9, 3.0), 0.42)
    poe(x, _explosao(rng, 0.5, 50), 0.45)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Dovahkiin

def machado_de_aco(rng, v):
    """Dovahkiin: o machado de aço descendo ("CHOP") e o tinido."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.25, 200, 3000, 0.85, 1.3, 0.55), 0.1)
    poe(x, _baque(80, 35, 0.4, 0.8, 2.6), 0.33)
    poe(x, _sino(rng, 784, 0.5, 0.03, METAL), 0.33)
    return reverb(x, 0.7, 0.35)


def fus_ro_dah_grito(rng, v):
    """Dovahkiin: "FUS... RO... DAH!" — as três palavras e a onda que empurra todos."""
    x = _z(2.7)
    for k, f in enumerate((150, 135, 120)):
        poe(x, _grito(rng, 0.2 if k < 2 else 0.5, f, 0.05 + 0.02 * k), 0.05 + 0.15 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 80, 2000, 2) * sobe_e_some(n, 0.2, 1.2) * 0.5, 0.4)
    poe(x, _baque(40, 15, 0.8, 0.8, 3.0), 0.4)
    return reverb(x, 1.2, 0.55)


def dovahkiin_preparo(rng, v):
    """Dovahkiin (Preparo): as runas do grito acendendo (o coro nórdico grave em laço)."""
    x = _z(1.4)
    poe(x, _acorde((98, 147, 196), 1.2, 0.025, 0.3, 0.6), 0.0)
    for k in range(3):
        poe(x, _sino(rng, 392 + 98 * k, 0.4, 0.015, SINO), 0.1 + 0.4 * k)
    return reverb(x, 1.0, 0.5)


def fogo_do_dragao_dovahkiin(rng, v):
    """Dovahkiin: "YOL TOOR SHUL!" — o grito de fogo varrendo todos os rivais."""
    x = _z(2.8)
    for k, f in enumerate((160, 145, 130)):
        poe(x, _grito(rng, 0.18, f, 0.05), 0.05 + 0.08 * k)
    poe(x, _fogo(rng, 1.2, 0.5, 120, 5000), 0.3)
    poe(x, _baque(45, 18, 0.7, 0.7, 2.6), 0.35)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ O Cavaleiro

def ferrao_cavaleiro(rng, v):
    """O Cavaleiro: as três estocadas do ferrão ("tchin-tchin-tchin")."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _whoosh(rng, 0.1, 1500, 7000, 0.6, 1.3, 0.3), 0.1 + 0.12 * k)
        poe(x, _sino(rng, 1568 + 100 * k, 0.25, 0.025, METAL), 0.18 + 0.12 * k)
        poe(x, _baque(160, 90, 0.08, 0.3), 0.18 + 0.12 * k)
    return reverb(x, 0.8, 0.4)


def concentrar_cavaleiro(rng, v):
    """O Cavaleiro: a alma se juntando (o zumbido subindo) e a cura ("vuum")."""
    x = _z(2.0)
    n = n_de(0.7)
    poe(x, seno(varre(200, 700, n), n) * env(n, 0.6, 0.05) * 0.02, 0.0)
    poe(x, _brilho(rng, 0.6, 1047, 0.03, CRISTAL), 0.6)
    poe(x, _acorde((392, 523, 659), 0.8, 0.02), 0.62)
    return reverb(x, 1.0, 0.5)


def cavaleiro_preparo(rng, v):
    """O Cavaleiro (Preparo): a sombra do abismo subindo (o coro baixo e o vento em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.2, 100, 900, 0.15, 0.5), 0.0)
    poe(x, _acorde((87, 104, 131), 1.1, 0.02, 0.3, 0.5), 0.0)
    return reverb(x, 1.0, 0.5)


def grito_do_abismo(rng, v):
    """O Cavaleiro: o grito do abismo e os braços de sombra subindo do chão."""
    x = _z(2.6)
    n = n_de(0.7)
    t = _t(n)
    poe(x, satura(seno(varre(300, 120, n), n) * (1 + 0.3 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 200, 3000, 2) * 0.5, 4) * env(n, 0.03, 0.5) * 0.04, 0.05)
    for k in range(6):
        poe(x, _whoosh(rng, 0.3, 80, 1000, 0.6, 1.3, 0.25), 0.25 + 0.04 * k)
    poe(x, _baque(45, 18, 0.7, 0.7, 2.6), 0.4)
    return reverb(x, 1.1, 0.55)


# ------------------------------------------------------------------ Goro

def quatro_socos(rng, v):
    """Goro: os quatro socos em sequência ("POW-POW-POW-POW")."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 150, 1500, 0.7, 1.3, 0.35), 0.08 + 0.1 * k)
        poe(x, _baque(90, 40, 0.25, 0.8, 2.6), 0.16 + 0.1 * k)
    poe(x, satura(seno(varre(110, 80, n_de(0.4)), n_de(0.4)), 3) * env(n_de(0.4), 0.05, 0.25) * 0.04, 0.6)
    return reverb(x, 0.7, 0.35)


def agarrao_goro(rng, v):
    """Goro: os quatro braços agarrando e apertando o rival."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.15, 200, 1500, 0.6, 1.3, 0.25), 0.05 + 0.04 * k)
    poe(x, _baque(100, 50, 0.3, 0.6), 0.35)
    n = n_de(0.5)
    poe(x, satura(seno(varre(90, 60, n), n), 3) * env(n, 0.05, 0.3) * 0.05, 0.45)
    return reverb(x, 0.7, 0.35)


def goro_preparo(rng, v):
    """Goro (Preparo): o pé enorme levantando e o rosnado (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(65, n) * (1 + 0.1 * np.sin(2 * math.pi * 15 * t)) + passa(rosa(rng, n), 60, 600, 2) * 0.5, 4) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    return reverb(x, 0.8, 0.4)


def pisao_de_goro(rng, v):
    """Goro: o pisão que racha a arena e o tremor em todos."""
    x = _z(2.7)
    poe(x, _whoosh(rng, 0.3, 60, 800, 0.9, 1.3, 0.5), 0.05)
    poe(x, _baque(26, 9, 1.8, 1.0, 4.0), 0.35)
    poe(x, _explosao(rng, 0.9, 30), 0.35)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.4, 0.4 + 0.04 * k)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 30, 300, 2) * sobe_e_some(n, 0.15, 1.2) * 0.6, 0.38)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Yoshi

def engolir_yoshi(rng, v):
    """Yoshi: a língua esticando ("thwip"), o "nhac" e o ovo saindo ("plop")."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, seno(varre(500, 1500, n), n) * env(n, 0.005, 0.15) * 0.03, 0.05)
    n = n_de(0.2)
    poe(x, seno(varre(1500, 400, n), n) * env(n, 0.005, 0.15) * 0.03, 0.35)
    poe(x, _baque(200, 100, 0.1, 0.4), 0.55)
    poe(x, _boing(rng, 500, 0.03), 0.62)
    return reverb(x, 0.5, 0.25)


def ovo_yoshi(rng, v):
    """Yoshi: o ovo voando e quicando no rival ("boing")."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 500, 3000, 0.6, 1.3, 0.3), 0.05)
    poe(x, _baque(140, 70, 0.15, 0.5), 0.43)
    poe(x, _boing(rng, 400, 0.04), 0.43)
    poe(x, _boing(rng, 600, 0.02), 0.7)
    return reverb(x, 0.5, 0.25)


def yoshi_preparo(rng, v):
    """Yoshi (Preparo): os pulinhos ("boing-boing") em laço."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _boing(rng, 350 + 50 * k, 0.025), 0.05 + 0.45 * k)
    return reverb(x, 0.5, 0.25)


def pisao_de_yoshi(rng, v):
    """Yoshi: o pulo bem alto ("uiii"), o pisão e as estrelinhas tontas."""
    x = _z(2.4)
    n = n_de(0.25)
    poe(x, seno(varre(400, 1600, n), n) * env(n, 0.02, 0.2) * 0.03, 0.0)
    n = n_de(0.15)
    poe(x, seno(varre(1600, 300, n), n) * env(n, 0.01, 0.12) * 0.03, 0.25)
    poe(x, _baque(40, 15, 1.0, 1.0, 3.2), 0.4)
    poe(x, _explosao(rng, 0.4, 50), 0.4)
    for k in range(5):
        poe(x, _brilho(rng, 0.2, 1568 + 200 * (k % 3), 0.015, CRISTAL), 0.55 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "disparo-de-dedo": (disparo_de_dedo, "Cuphead: disparo de dedo"),
    "dash-cuphead": (dash_cuphead, "Cuphead: dash"),
    "cuphead-preparo": (cuphead_preparo, "Cuphead: as cartas de super (Preparo)"),
    "super-art-cuphead": (super_art_cuphead, "Cuphead: Super Art"),
    "machado-de-aco": (machado_de_aco, "Dovahkiin: machado de aço"),
    "fus-ro-dah-grito": (fus_ro_dah_grito, "Dovahkiin: Fus Ro Dah"),
    "dovahkiin-preparo": (dovahkiin_preparo, "Dovahkiin: as runas (Preparo)"),
    "fogo-do-dragao-dovahkiin": (fogo_do_dragao_dovahkiin, "Dovahkiin: fogo do dragão"),
    "ferrao-cavaleiro": (ferrao_cavaleiro, "O Cavaleiro: ferrão"),
    "concentrar-cavaleiro": (concentrar_cavaleiro, "O Cavaleiro: concentrar"),
    "cavaleiro-preparo": (cavaleiro_preparo, "O Cavaleiro: a sombra do abismo (Preparo)"),
    "grito-do-abismo": (grito_do_abismo, "O Cavaleiro: grito do abismo"),
    "quatro-socos": (quatro_socos, "Goro: quatro socos"),
    "agarrao-goro": (agarrao_goro, "Goro: agarrão"),
    "goro-preparo": (goro_preparo, "Goro: o pé levantando (Preparo)"),
    "pisao-de-goro": (pisao_de_goro, "Goro: pisão"),
    "engolir-yoshi": (engolir_yoshi, "Yoshi: engolir"),
    "ovo-yoshi": (ovo_yoshi, "Yoshi: ovo"),
    "yoshi-preparo": (yoshi_preparo, "Yoshi: os pulinhos (Preparo)"),
    "pisao-de-yoshi": (pisao_de_yoshi, "Yoshi: pisão"),
}
