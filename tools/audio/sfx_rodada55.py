"""Os sons da rodada 55 das habilidades próprias (veja tools/vfx/familias_v2/rodada55.py)."""
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


def _gelo_cresce(rng, seg, g=0.3):
    """O gelo crescendo (os estalinhos cristalinos em cadeia)."""
    x = _z(seg + 0.3)
    q = np.random.default_rng(31)
    for k in range(int(seg * 30)):
        poe(x, estalo(rng, n_de(0.015), 3000, 10000, 0.003) * g * q.uniform(0.3, 1.0), k / 30)
    return x


def _rugido_monstro(rng, seg, f0=90, f1=50, g=0.07):
    n = n_de(seg)
    return satura(seno(varre(f0, f1, n), n) + seno(varre(f0 * 1.5, f1 * 1.5, n), n) * 0.4 + passa(rosa(rng, n), 80, 1500, 2) * 1.0, 6) * env(n, 0.08, seg * 0.6) * g


# ------------------------------------------------------------------ Gandalf

def voce_nao_vai_passar(rng, v):
    """Gandalf: "VOCÊ NÃO VAI PASSAR!" — o cajado batendo na ponte e a luz subindo."""
    x = _z(2.3)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.2)
    poe(x, _sino(rng, 220, 1.2, 0.05, METAL), 0.2)
    n = n_de(0.6)
    poe(x, (seno(varre(300, 900, n), n) + seno(varre(450, 1350, n), n) * 0.5) * env(n, 0.3, 0.2) * 0.02, 0.3)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.022), 0.45)
    return reverb(x, 1.0, 0.5)


def luz_de_gandalf(rng, v):
    """Gandalf: o cajado acendendo como o sol (o coro brilhante) e a cura."""
    x = _z(2.4)
    n = n_de(0.4)
    poe(x, seno(varre(400, 1600, n), n) * env(n, 0.35, 0.05) * 0.02, 0.0)
    poe(x, _acorde((523, 659, 784, 1047, 1319), 1.2, 0.03), 0.3)
    poe(x, _brilho(rng, 1.0, 1760, 0.02, CRISTAL), 0.35)
    return reverb(x, 1.0, 0.5)


def gandalf_preparo(rng, v):
    """Gandalf (Preparo): a espada élfica zumbindo e o cajado brilhando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(659, n) + seno(988, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    poe(x, _sino(rng, 1976, 0.6, 0.01, CRISTAL), 0.4)
    return reverb(x, 0.8, 0.4)


def glamdring(rng, v):
    """Gandalf: a Glamdring cortando (o tinido élfico e o corte)."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 800, 7000, 0.85, 1.3, 0.5), 0.05)
    poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.32)
    poe(x, _sino(rng, 1568, 0.7, 0.035, METAL), 0.32)
    poe(x, _sino(rng, 2349, 0.5, 0.015, CRISTAL), 0.36)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Godzilla

def pisao_de_godzilla(rng, v):
    """Godzilla: a pata gigante descendo e o terremoto."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.3, 60, 800, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(30, 12, 1.5, 1.0, 3.8), 0.28)
    poe(x, _explosao(rng, 1.0, 30), 0.28)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 25, 200, 2) * sobe_e_some(n, 0.1, 1.2) * 0.7, 0.3)
    return reverb(x, 0.8, 0.4)


def couraca(rng, v):
    """Godzilla: as placas acendendo ("vum-vum-vum") e a couraça fechando."""
    x = _z(2.1)
    for k in range(5):
        n = n_de(0.12)
        poe(x, seno(varre(150 + 30 * k, 300 + 30 * k, n), n) * env(n, 0.01, 0.1) * 0.03, 0.05 + 0.08 * k)
    poe(x, _sino(rng, 165, 1.0, 0.05, METAL), 0.45)
    poe(x, _baque(80, 40, 0.3, 0.5), 0.45)
    return reverb(x, 0.8, 0.4)


def godzilla_preparo(rng, v):
    """Godzilla (Preparo): as placas carregando (o zumbido nuclear subindo em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(55 + 40 * t, n) + seno(110 + 80 * t, n) * 0.4, 2) * sobe_e_some(n, 0.7, 1.2) * 0.035, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.004) * 0.25, 0.22 * k + 0.1)
    return reverb(x, 0.7, 0.35)


def sopro_atomico(rng, v):
    """Godzilla: o rugido e o sopro atômico rasgando o ar."""
    x = _z(2.6)
    poe(x, _rugido_monstro(rng, 0.5, 200, 120, 0.05), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 500, 6000, 2) + seno(220, n) * 0.4, 3) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.05, 0.4) * 0.3, 0.3)
    for k in range(3):
        poe(x, _baque(80, 35, 0.3, 0.5), 0.45 + 0.15 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ King Kong

def soco_gigante_kong(rng, v):
    """King Kong: o punho gigante e o rival voando longe."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.3, 80, 1200, 0.9, 1.3, 0.6), 0.0)
    poe(x, _baque(40, 15, 1.2, 1.0, 3.4), 0.3)
    poe(x, _explosao(rng, 0.6, 45), 0.3)
    poe(x, _whoosh(rng, 0.4, 600, 4000, 0.3, 1.3, 0.3), 0.35)
    return reverb(x, 0.7, 0.35)


def bater_no_peito(rng, v):
    """King Kong: as batidas no peito ("BUM-BUM-BUM-BUM") e o rugido."""
    x = _z(2.4)
    for k in range(4):
        poe(x, _baque(70, 40, 0.25, 0.9, 2.6), 0.08 + 0.12 * k)
    poe(x, _rugido_monstro(rng, 0.8, 140, 90, 0.06), 0.55)
    return reverb(x, 0.8, 0.4)


def kong_preparo(rng, v):
    """King Kong (Preparo): o machado de energia zumbindo (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(110, n) + seno(165, n) * 0.5, 3) * (0.7 + 0.3 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.025, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.004) * 0.25, 0.3 * k + 0.1)
    return reverb(x, 0.6, 0.3)


def machado_de_kong(rng, v):
    """King Kong: o machado descendo e rachando o chão."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.35, 150, 2500, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(40, 15, 1.2, 1.0, 3.4), 0.33)
    poe(x, _explosao(rng, 0.8, 40), 0.33)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.5, 0.36 + 0.05 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Shrek

def arroto(rng, v):
    """Shrek: o arroto longo e as moscas zumbindo."""
    x = _z(2.3)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(seno(varre(110, 75, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 18 * t)) + passa(rosa(rng, n), 80, 800, 2) * 0.8, 5) * env(n, 0.03, 0.5) * 0.07, 0.05)
    n2 = n_de(1.0)
    t2 = _t(n2)
    poe(x, seno(220 + 15 * np.sin(2 * math.pi * 7 * t2), n2) * sobe_e_some(n2, 0.4, 1.2) * 0.008, 0.6)
    return reverb(x, 0.6, 0.3)


def abraco_de_ogro(rng, v):
    """Shrek: o abraço apertado ("squish") e o escudo de lama."""
    x = _z(2.0)
    n = n_de(0.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 150, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * t) ** 2) * env(n, 0.05, 0.3) * 0.35, 0.2)
    poe(x, _baque(110, 70, 0.25, 0.5), 0.2)
    for k in range(4):
        poe(x, _piu(300, 150, 0.06, 0.012), 0.45 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def shrek_preparo(rng, v):
    """Shrek (Preparo): as orelhas de trompete ("prrr") e o pântano borbulhando (em laço)."""
    x = _z(1.4)
    n = n_de(0.3)
    poe(x, satura(seno(varre(260, 220, n), n), 4) * env(n, 0.02, 0.25) * 0.02, 0.0)
    for k in range(5):
        poe(x, _piu(250, 450, 0.05, 0.012), 0.35 + 0.18 * k)
    return reverb(x, 0.5, 0.25)


def rugido_do_pantano(rng, v):
    """Shrek: o rugido do ogro e a lama do pântano subindo."""
    x = _z(2.4)
    poe(x, _rugido_monstro(rng, 0.7, 120, 80, 0.07), 0.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 100, 1200, 2) * env(n, 0.1, 0.4) * 0.4, 0.4)
    for k in range(5):
        poe(x, _piu(200, 350, 0.06, 0.014), 0.5 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Elsa

def rajada_de_gelo_elsa(rng, v):
    """Elsa: os flocos girando na mão e o raio de gelo congelando o rival."""
    x = _z(2.1)
    for k in range(4):
        poe(x, _sino(rng, 2093 + 200 * k, 0.4, 0.012, CRISTAL), 0.04 * k)
    poe(x, _whoosh(rng, 0.25, 2000, 10000, 0.7, 1.3, 0.35), 0.2)
    poe(x, _gelo_cresce(rng, 0.3, 0.35), 0.4)
    poe(x, _sino(rng, 1568, 0.6, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.8, 0.4)


def muralha_de_gelo_elsa(rng, v):
    """Elsa: os cristais de gelo crescendo na frente do trio."""
    x = _z(2.2)
    for k in range(3):
        poe(x, _gelo_cresce(rng, 0.3, 0.3), 0.05 + 0.07 * k)
        poe(x, _sino(rng, 1319 + 150 * k, 0.7, 0.02, CRISTAL), 0.3 + 0.07 * k)
    return reverb(x, 0.8, 0.4)


def elsa_preparo(rng, v):
    """Elsa (Preparo): o floco gigante girando (o canto gelado em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(784, n) + seno(1175, n) * 0.5 + seno(1568, n) * 0.25) * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2637 + 300 * k, 0.3, 0.008, CRISTAL), 0.3 * k + 0.1)
    return reverb(x, 1.0, 0.5)


def inverno_eterno(rng, v):
    """Elsa: a nevasca uivando e o gelo prendendo todos os rivais."""
    x = _z(2.6)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.9 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.0)
    for k in range(3):
        poe(x, _gelo_cresce(rng, 0.25, 0.35), 0.45 + 0.07 * k)
        poe(x, _sino(rng, 1760 + 200 * k, 0.5, 0.02, CRISTAL), 0.55 + 0.07 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.018), 0.5)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Malévola

def maldicao_do_sono(rng, v):
    """Malévola: o fogo verde, a risada e o rival adormecendo."""
    x = _z(2.4)
    poe(x, _fogo(rng, 0.5, 0.2, 300, 3000), 0.0)
    for k in range(4):
        n = n_de(0.12)
        f = 300 * (1 - 0.04 * k)
        poe(x, satura(seno(varre(f * 1.1, f, n), n) + passa(rosa(rng, n), 400, 3000, 2) * 0.5, 3) * env(n, 0.01, 0.1) * 0.02, 0.2 + 0.12 * k)
    n2 = n_de(0.8)
    poe(x, seno(varre(500, 250, n2), n2) * sobe_e_some(n2, 0.3, 1.2) * 0.01, 0.8)
    return reverb(x, 1.0, 0.5)


def muro_de_espinhos(rng, v):
    """Malévola: os galhos de espinhos subindo, rangendo e prendendo."""
    x = _z(2.3)
    for k in range(3):
        n = n_de(0.4)
        t = _t(n)
        poe(x, satura(passa(rosa(rng, n), 200, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 15 * t) ** 2), 3) * env(n, 0.05, 0.3) * 0.3, 0.05 + 0.1 * k)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.03), 500, 4000, 0.006) * 0.5, 0.35 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def malevola_preparo(rng, v):
    """Malévola (Preparo): o fogo verde girando no cajado e o coro sombrio (em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.0, 0.12, 300, 3000), 0.0)
    n = n_de(1.0)
    poe(x, (seno(98, n) + seno(117, n) + seno(147, n) * 0.6) * sobe_e_some(n, 0.5, 1.2) * 0.015, 0.0)
    return reverb(x, 0.9, 0.45)


def forma_de_dragao(rng, v):
    """Malévola: o rugido do dragão e o sopro de fogo verde em todos."""
    x = _z(2.6)
    poe(x, _rugido_monstro(rng, 0.7, 160, 90, 0.06), 0.0)
    poe(x, _fogo(rng, 1.0, 0.45, 150, 4000), 0.3)
    for k in range(3):
        poe(x, _baque(80, 35, 0.3, 0.5), 0.45 + 0.08 * k)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "voce-nao-vai-passar": (voce_nao_vai_passar, "Gandalf: você não vai passar"),
    "luz-de-gandalf": (luz_de_gandalf, "Gandalf: a luz de Gandalf"),
    "gandalf-preparo": (gandalf_preparo, "Gandalf: a espada élfica (Preparo)"),
    "glamdring": (glamdring, "Gandalf: Glamdring"),
    "pisao-de-godzilla": (pisao_de_godzilla, "Godzilla: o pisão"),
    "couraca": (couraca, "Godzilla: a couraça"),
    "godzilla-preparo": (godzilla_preparo, "Godzilla: as placas carregando (Preparo)"),
    "sopro-atomico": (sopro_atomico, "Godzilla: o sopro atômico"),
    "soco-gigante-kong": (soco_gigante_kong, "King Kong: o soco gigante"),
    "bater-no-peito": (bater_no_peito, "King Kong: bater no peito"),
    "kong-preparo": (kong_preparo, "King Kong: o machado de energia (Preparo)"),
    "machado-de-kong": (machado_de_kong, "King Kong: o machado de Kong"),
    "arroto": (arroto, "Shrek: o arroto"),
    "abraco-de-ogro": (abraco_de_ogro, "Shrek: o abraço de ogro"),
    "shrek-preparo": (shrek_preparo, "Shrek: as orelhas e o pântano (Preparo)"),
    "rugido-do-pantano": (rugido_do_pantano, "Shrek: o rugido do pântano"),
    "rajada-de-gelo-elsa": (rajada_de_gelo_elsa, "Elsa: a rajada de gelo"),
    "muralha-de-gelo-elsa": (muralha_de_gelo_elsa, "Elsa: a muralha de gelo"),
    "elsa-preparo": (elsa_preparo, "Elsa: o floco gigante (Preparo)"),
    "inverno-eterno": (inverno_eterno, "Elsa: o inverno eterno"),
    "maldicao-do-sono": (maldicao_do_sono, "Malévola: a maldição do sono"),
    "muro-de-espinhos": (muro_de_espinhos, "Malévola: o muro de espinhos"),
    "malevola-preparo": (malevola_preparo, "Malévola: o fogo verde no cajado (Preparo)"),
    "forma-de-dragao": (forma_de_dragao, "Malévola: a forma de dragão"),
}
