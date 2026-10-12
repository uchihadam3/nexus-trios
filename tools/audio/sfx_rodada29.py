"""Os sons da rodada 29 das habilidades próprias (veja tools/vfx/familias_v2/rodada29.py)."""
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


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _kiai(rng, f0, seg=0.18, g=0.05):
    n = n_de(seg)
    return satura(seno(varre(f0, f0 * 0.8, n), n) + passa(rosa(rng, n), 400, 2500, 2) * 0.4, 2.5) * env(n, 0.01, seg * 0.7) * g


# ------------------------------------------------------------------ Spawn

def correntes_necroplasmicas(rng, v):
    """Spawn: as três correntes saindo e chicoteando."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _corrente(rng, 0.35, 8, 0.3), 0.05 * k)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.008), 0.42)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.45)
    return reverb(x, 0.6, 0.3)


def capa_viva(rng, v):
    """Spawn: a capa viva se espalhando (o pano rasgando e chicoteando)."""
    x = _z(2.0)
    for k in range(5):
        poe(x, _whoosh(rng, 0.25, 300, 3000, 0.5, 1.4, 0.3), 0.04 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.01, 0.3) * 0.25, 0.45)
    return reverb(x, 0.6, 0.3)


def spawn_preparo(rng, v):
    """Spawn (Preparo): o necroplasma acendendo (o tom grave e o fogo verde)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(varre(60, 90, n), n), 2.5) * sobe_e_some(n, 0.6, 1.2) * 0.06, 0.0)
    poe(x, _fogo(rng, 1.0, 0.15, 0.7), 0.0)
    return reverb(x, 0.7, 0.35)


def fogo_do_inferno(rng, v):
    """Spawn: a rajada de fogo do inferno."""
    x = _z(2.0)
    poe(x, _fogo(rng, 1.0, 0.45, 0.15), 0.05)
    poe(x, _acorde((110, 131, 165), 0.8, 0.04, 0.05, 0.6), 0.1)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Invencível

def soco_supersonico(rng, v):
    """Invencível: o soco quebrando a barreira do som (o estrondo seco)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 400, 5000, 0.9, 1.3, 0.45), 0.0)
    poe(x, _baque(70, 30, 0.5, 0.9, 3.0), 0.28)
    poe(x, passa(rosa(rng, n_de(0.15)), 100, 3000, 2) * env(n_de(0.15), 0.001, 0.1) * 0.6, 0.28)
    return reverb(x, 0.6, 0.3)


def investida_orbital(rng, v):
    """Invencível: o mergulho do céu (o assobio que desce) e o impacto."""
    x = _z(2.1)
    n = n_de(0.4)
    poe(x, (seno(varre(1600, 400, n), n) * 0.04 + passa(rosa(rng, n), 800, 6000, 2) * 0.25) * sobe_e_some(n, 0.9, 1.0), 0.0)
    poe(x, _baque(55, 25, 0.8, 1.0, 3.0), 0.4)
    poe(x, _explosao(rng, 0.8, 0.5), 0.4)
    return reverb(x, 0.7, 0.35)


def invencivel_preparo(rng, v):
    """Invencível (Preparo): a respiração pesada e a força voltando (o tom que sobe)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.4)
        poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.4, 1.3) * 0.2, 0.05 + 0.45 * k)
    m = n_de(1.0)
    poe(x, seno(varre(150, 350, m), m) * sobe_e_some(m, 0.85, 1.2) * 0.04, 0.0)
    return reverb(x, 0.5, 0.25)


def levantar_de_novo(rng, v):
    """Invencível: o soco de quem levantou (o estrondo e a onda)."""
    x = _z(2.2)
    poe(x, _kiai(rng, 220, 0.3, 0.06), 0.0)
    poe(x, _baque(50, 22, 0.9, 1.0, 3.2), 0.22)
    poe(x, _explosao(rng, 1.0, 0.7), 0.22)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Leonardo

def katanas_gemeas(rng, v):
    """Leonardo: as duas katanas em X (os dois cortes metálicos)."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2500, 10000, 0.7, 1.4, 0.45), 0.05 + 0.07 * k)
        poe(x, _sino(rng, 3300 + 400 * k, 0.5, 0.05, METAL), 0.15 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def formacao(rng, v):
    """Leonardo: "Tartarugas, em formação!" (o tema heroico curto)."""
    x = _z(2.0)
    for k, f in enumerate((392, 494, 587, 784)):
        n = n_de(0.15 if k < 3 else 0.5)
        poe(x, (_quadrada(f, n) * 0.3 + seno(f, n)) * env(n, 0.01, 0.12 if k < 3 else 0.4) * 0.035, 0.1 * k)
    for k in range(3):
        poe(x, _baque(140, 80, 0.12, 0.3), 0.4 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def leonardo_preparo(rng, v):
    """Leonardo (Preparo): as katanas cruzadas na guarda (o metal raspando)."""
    x = _z(1.4)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.6, 1.4) * 0.12, 0.05)
    poe(x, _sino(rng, 3000, 0.6, 0.04, METAL), 0.4)
    return reverb(x, 0.5, 0.25)


def investida_do_lider(rng, v):
    """Leonardo: o avanço do líder e os dois cortes finais."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.35, 600, 5000, 0.9, 1.3, 0.45), 0.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.12, 2500, 10000, 0.7, 1.4, 0.45), 0.33 + 0.05 * k)
        poe(x, _sino(rng, 3000 + 500 * k, 0.5, 0.05, METAL), 0.38 + 0.05 * k)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Raphael

def investida_furiosa(rng, v):
    """Raphael: os sais girando (o zunido) e o avanço com raiva."""
    x = _z(1.9)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 20 * t) ** 2) * env(n, 0.01, 0.4) * 0.2, 0.0)
    poe(x, _kiai(rng, 180, 0.2, 0.06), 0.2)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.4)
    return reverb(x, 0.5, 0.25)


def sem_recuo(rng, v):
    """Raphael: o grito de raiva e o soco de cabeça baixa."""
    x = _z(1.9)
    poe(x, _kiai(rng, 160, 0.35, 0.07), 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 3000, 0.8, 1.4, 0.4), 0.25)
    poe(x, _baque(80, 35, 0.5, 0.9, 2.8), 0.45)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Donatello

def bastao_bo(rng, v):
    """Donatello: o bastão girando (o zunido em hélice) e as batidas."""
    x = _z(1.9)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t) ** 2) * env(n, 0.02, 0.6) * 0.3, 0.0)
    for k in range(3):
        poe(x, _baque(170, 90, 0.12, 0.35), 0.2 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


def dispositivo_tatico(rng, v):
    """Donatello: o aparelho arremessado (as engrenagens e o bipe acelerando)."""
    x = _z(1.9)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.4, 0.05 * k)
    for k in range(6):
        poe(x, seno(1800, n_de(0.04)) * env(n_de(0.04), 0.002, 0.03) * 0.04, 0.35 + 0.12 * (1 - k / 8) * k)
    poe(x, _baque(200, 100, 0.12, 0.3), 0.36)
    return reverb(x, 0.4, 0.2)


def campo_de_contencao(rng, v):
    """Donatello: a grade de laser se fechando (o zumbido elétrico)."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, (_quadrada(220, n) * 0.3 + seno(440, n)) * (0.7 + 0.3 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.025, 0.0)
    poe(x, graos(rng, n_de(0.6), 30, 0.0, 0.9, 2500, 8000, 0.002) * 0.2, 0.1)
    poe(x, _baque(200, 120, 0.1, 0.3), 0.45)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Michelangelo

def giro_maluco(rng, v):
    """Michelangelo: "Cowabunga!" (o grito alegre) e os nunchakus girando."""
    x = _z(1.9)
    n = n_de(0.35)
    poe(x, satura(seno(varre(350, 500, n), n), 1.5) * env(n, 0.01, 0.3) * 0.04, 0.0)
    m = n_de(0.6)
    t = _t(m)
    poe(x, passa(rosa(rng, m), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 16 * t) ** 2) * env(m, 0.01, 0.5) * 0.2, 0.15)
    for k in range(4):
        poe(x, _piu(1500 + 200 * k, 2000 + 200 * k, 0.05, 0.02), 0.5 + 0.06 * k)
    return reverb(x, 0.5, 0.25)


def festa_surpresa(rng, v):
    """Michelangelo: os balões estourando, o confete e a festa."""
    x = _z(2.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 800, 6000, 0.008) * 0.8, 0.15 + 0.15 * k)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.2, 1.3) * 0.15, 0.2)
    for k, f in enumerate((523, 659, 784, 1047)):
        poe(x, _sino(rng, f, 0.3, 0.03, SINO), 0.4 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Constantine

def pacto(rng, v):
    """Constantine: o giz riscando o pentagrama, o isqueiro e o sussurro do pacto."""
    x = _z(2.1)
    for k in range(5):
        n = n_de(0.08)
        poe(x, passa(rosa(rng, n), 2500, 8000, 2) * env(n, 0.005, 0.06) * 0.25, 0.05 + 0.08 * k)
    poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.005), 0.5)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 2000, 6000, 2) * sobe_e_some(m, 0.5, 1.4) * 0.1, 0.55)
    poe(x, _acorde((147, 175, 220), 0.7, 0.04, 0.1, 0.5), 0.5)
    return reverb(x, 0.8, 0.4)


def exorcismo(rng, v):
    """Constantine: a cruz de luz (o coro) e o demônio arrancado (o grito que some)."""
    x = _z(2.1)
    poe(x, _acorde((262, 330, 392, 523), 1.0, 0.045, 0.05, 0.7), 0.1)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(varre(500, 150, n) * (1 + 0.05 * np.sin(2 * math.pi * 20 * t)), n), 2) * env(n, 0.01, 0.5) * 0.05, 0.4)
    return reverb(x, 0.8, 0.4)


def blefe_infernal(rng, v):
    """Constantine: as cartas de tarô viradas e a fumaça do blefe."""
    x = _z(2.0)
    for k in range(3):
        poe(x, passa(rosa(rng, n_de(0.06)), 2000, 7000, 2) * env(n_de(0.06), 0.003, 0.04) * 0.3, 0.05 + 0.08 * k)
    poe(x, _sopro(rng, 0.6, 300, 2500, 0.3, 0.3), 0.55)
    poe(x, seno(varre(400, 300, n_de(0.5)), n_de(0.5)) * env(n_de(0.5), 0.05, 0.4) * 0.03, 0.6)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "correntes-necroplasmicas": (correntes_necroplasmicas, "Spawn: as correntes"),
    "capa-viva": (capa_viva, "Spawn: a capa viva"),
    "spawn-preparo": (spawn_preparo, "Spawn: o necroplasma (Preparo)"),
    "fogo-do-inferno": (fogo_do_inferno, "Spawn: o fogo do inferno"),
    "soco-supersonico": (soco_supersonico, "Invencível: o soco supersônico"),
    "investida-orbital": (investida_orbital, "Invencível: a investida orbital"),
    "invencivel-preparo": (invencivel_preparo, "Invencível: se erguendo (Preparo)"),
    "levantar-de-novo": (levantar_de_novo, "Invencível: levantar de novo"),
    "katanas-gemeas": (katanas_gemeas, "Leonardo: as katanas gêmeas"),
    "formacao": (formacao, "Leonardo: a formação"),
    "leonardo-preparo": (leonardo_preparo, "Leonardo: a guarda (Preparo)"),
    "investida-do-lider": (investida_do_lider, "Leonardo: a investida do líder"),
    "investida-furiosa": (investida_furiosa, "Raphael: a investida furiosa"),
    "sem-recuo": (sem_recuo, "Raphael: sem recuo"),
    "bastao-bo": (bastao_bo, "Donatello: o bastão bo"),
    "dispositivo-tatico": (dispositivo_tatico, "Donatello: o dispositivo tático"),
    "campo-de-contencao": (campo_de_contencao, "Donatello: o campo de contenção"),
    "giro-maluco": (giro_maluco, "Michelangelo: o giro maluco"),
    "festa-surpresa": (festa_surpresa, "Michelangelo: a festa surpresa"),
    "pacto": (pacto, "Constantine: o pacto"),
    "exorcismo": (exorcismo, "Constantine: o exorcismo"),
    "blefe-infernal": (blefe_infernal, "Constantine: o blefe infernal"),
}
