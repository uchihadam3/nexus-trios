"""Os sons da rodada 21 das habilidades próprias (veja tools/vfx/familias_v2/rodada21.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _tiro(rng, g=0.6):
    n = n_de(0.25)
    return satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.06), 2.5) * g


# ------------------------------------------------------------------ Jill

def kit_primeiros_socorros(rng, v):
    """Jill: a maleta abrindo, o spray de cura e o acorde de vida."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006), 0.05)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.02, 0.3, segura=0.2) * 0.25, 0.3)
    poe(x, _acorde((523, 659, 784, 1047), 0.8, 0.035, 0.05, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


def cobertura_tatica(rng, v):
    """Jill: o sinal de mão (o estalo do rádio) e o trio avançando (os passos e o tom de comando)."""
    x = _z(1.8)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 1500, 4000, 2) * env(n, 0.003, 0.1) * 0.25, 0.0)
    for k in range(3):
        poe(x, _baque(140, 80, 0.12, 0.3), 0.3 + 0.12 * k)
    poe(x, _acorde((294, 370, 440), 0.6, 0.04, 0.02, 0.4), 0.35)
    return reverb(x, 0.5, 0.25)


def jill_preparo(rng, v):
    """Jill (Preparo): a seringa enchendo (o tom líquido que sobe)."""
    x = _z(1.2)
    n = n_de(0.8)
    poe(x, seno(varre(300, 700, n), n) * sobe_e_some(n, 0.8, 1.2) * 0.04, 0.0)
    poe(x, passa(rosa(rng, n), 800, 3000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.08, 0.0)
    return reverb(x, 0.4, 0.2)


def resistencia_adquirida(rng, v):
    """Jill: a vacina injetada (o "tss") e o DNA se fortalecendo (o acorde que cresce)."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.005, 0.15) * 0.3, 0.0)
    poe(x, _acorde((262, 330, 392, 523), 1.2, 0.045, 0.2, 0.8), 0.15)
    poe(x, _sino(rng, 1047, 0.6, 0.05, CRISTAL), 0.4)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Wesker

def deslocamento_wesker(rng, v):
    """Wesker: os deslocamentos rapidíssimos (os "vups" em zigue-zague)."""
    x = _z(1.8)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 1000, 7000, 0.6, 1.4, 0.35), 0.03 + 0.11 * k)
    poe(x, _sino(rng, 2600, 0.3, 0.03, METAL), 0.55)
    return reverb(x, 0.4, 0.2)


def golpe_cruzado(rng, v):
    """Wesker: os dois golpes cruzados e o corte que sangra."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 800, 5000, 0.7, 1.4, 0.45), 0.0 + 0.12 * k)
        poe(x, _baque(150, 70, 0.2, 0.5), 0.12 + 0.12 * k)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 500, 2500, 2) * env(n, 0.01, 0.2) * 0.25, 0.3)
    return reverb(x, 0.5, 0.25)


def supremacia_wesker(rng, v):
    """Wesker: os olhos acendendo (o tom grave) e o soco que paralisa."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, satura(seno(varre(70, 90, n), n), 2.5) * env(n, 0.05, 0.35) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.2, 300, 3000, 0.7, 1.4, 0.4), 0.35)
    poe(x, _baque(70, 30, 0.5, 0.9, 3.0), 0.5)
    poe(x, graos(rng, n_de(0.4), 30, 0.0, 0.9, 2500, 9000, 0.002) * 0.3, 0.55)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Lara

def arco_recurvo(rng, v):
    """Lara: o arco tensionando (o rangido), a flecha voando e cravando."""
    x = _z(1.8)
    n = n_de(0.3)
    poe(x, seno(varre(150, 300, n), n) * env(n, 0.1, 0.2) * 0.04, 0.0)
    poe(x, estalo(rng, n_de(0.03), 600, 3000, 0.008), 0.3)
    poe(x, _whoosh(rng, 0.25, 2000, 8000, 0.6, 1.4, 0.35), 0.32)
    poe(x, _baque(250, 120, 0.12, 0.4), 0.58)
    return reverb(x, 0.5, 0.25)


def armadilha_de_cabo(rng, v):
    """Lara: o disparo do gancho e o cabo enrolando (o zunido que gira)."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005), 0.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.005, 0.25) * 0.25, 0.0)
    m = n_de(0.5)
    t = _t(m)
    poe(x, passa(rosa(rng, m), 600, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * t) ** 2) * env(m, 0.02, 0.4) * 0.3, 0.3)
    return reverb(x, 0.4, 0.2)


def lara_preparo(rng, v):
    """Lara (Preparo): a respiração segurada e o batimento lento."""
    x = _z(1.4)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.5, 1.4) * 0.15, 0.0)
    for k in range(2):
        poe(x, _baque(55, 40, 0.18, 0.35, 1.4), 0.5 + 0.35 * k)
    return reverb(x, 0.4, 0.2)


def tiro_perfeito(rng, v):
    """Lara: o tiro único e pesado do rifle e o impacto."""
    x = _z(1.9)
    poe(x, _tiro(rng, 0.9), 0.0)
    poe(x, _baque(110, 45, 0.4, 0.7, 2.6), 0.0)
    poe(x, _baque(150, 60, 0.3, 0.5), 0.22)
    poe(x, _sino(rng, 3000, 0.3, 0.03, METAL), 0.3)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Ezio

def multidao(rng, v):
    """Ezio: o burburinho da multidão em volta e o rival perdido."""
    x = _z(1.9)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.0)
    for k in range(4):
        m = n_de(0.12)
        poe(x, seno(varre(200 + 30 * k, 180, m), m) * env(m, 0.01, 0.1) * 0.03, 0.2 + 0.15 * k)
    return reverb(x, 0.6, 0.3)


def execucao_em_cadeia(rng, v):
    """Ezio: os três golpes da lâmina oculta em sequência e o grito da águia."""
    x = _z(1.9)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 2000, 7000, 0.005), 0.08 + 0.18 * k)
        poe(x, _whoosh(rng, 0.1, 2000, 9000, 0.6, 1.4, 0.3), 0.06 + 0.18 * k)
        poe(x, _baque(160, 80, 0.12, 0.35), 0.1 + 0.18 * k)
    n = n_de(0.4)
    t = _t(n)
    poe(x, seno(varre(2800, 2000, n) * (1 + 0.03 * np.sin(2 * math.pi * 30 * t)), n) * env(n, 0.01, 0.3) * 0.03, 0.65)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Sonic

def homing_attack(rng, v):
    """Sonic: a mira travando (o bipe), a bola girando e o anel dourado."""
    x = _z(1.8)
    poe(x, seno(1500, n_de(0.06)) * env(n_de(0.06), 0.003, 0.05) * 0.04, 0.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * env(n, 0.01, 0.25) * 0.3, 0.15)
    poe(x, _baque(170, 90, 0.15, 0.4), 0.43)
    for k, f in enumerate((1568, 2093)):
        poe(x, _sino(rng, f, 0.4, 0.04, CRISTAL), 0.5 + 0.06 * k)
    return reverb(x, 0.4, 0.2)


def sonic_preparo(rng, v):
    """Sonic (Preparo): as Esmeraldas girando (o brilho que sobe)."""
    x = _z(1.4)
    for k in range(7):
        poe(x, _sino(rng, 784 * 2 ** (k / 7), 0.4, 0.03, CRISTAL), 0.1 * k)
    return reverb(x, 0.6, 0.3)


def super_sonic(rng, v):
    """Sonic: a transformação dourada (o acorde enorme) e a arrancada supersônica."""
    x = _z(2.2)
    poe(x, _acorde((392, 494, 587, 784, 988), 1.2, 0.05, 0.02, 0.9), 0.0)
    poe(x, _brilho(rng, 0.8, 2349, 0.05, CRISTAL), 0.05)
    poe(x, _whoosh(rng, 0.5, 400, 8000, 0.8, 1.3, 0.6), 0.5)
    poe(x, _explosao(rng, 0.8, 0.6), 0.85)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Shadow

def chaos_spear(rng, v):
    """Shadow: as três lanças do Caos (os zunidos elétricos)."""
    x = _z(1.8)
    for k in range(3):
        n = n_de(0.3)
        poe(x, (seno(varre(1800, 900, n), n) * 0.04 + passa(rosa(rng, n), 3000, 9000, 2) * 0.12) * env(n, 0.005, 0.25), 0.05 + 0.08 * k)
    poe(x, graos(rng, n_de(0.3), 20, 0.0, 0.9, 3000, 9000, 0.002) * 0.3, 0.45)
    return reverb(x, 0.5, 0.25)


def chaos_control(rng, v):
    """Shadow: "Chaos Control!" — o relógio parando (o tique que estica) e o tempo congelado."""
    x = _z(2.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 2000, 6000, 0.004) * 0.5, 0.05 + 0.08 * k * (1 + k * 0.3))
    n = n_de(1.0)
    poe(x, seno(varre(600, 150, n, 0.6), n) * env(n, 0.02, 0.8) * 0.05, 0.3)
    poe(x, _acorde((220, 277, 330, 440), 1.0, 0.04, 0.1, 0.8), 0.35)
    return reverb(x, 0.8, 0.4)


def shadow_preparo(rng, v):
    """Shadow (Preparo): a Esmeralda vermelha pulsando (o tom que bate)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(220, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.0) * 0.05, 0.0)
    poe(x, _sino(rng, 880, 0.5, 0.03, CRISTAL), 0.2)
    return reverb(x, 0.5, 0.25)


def lanca_das_esmeraldas(rng, v):
    """Shadow: a chuva de lanças caindo (os zunidos em sequência) e os impactos."""
    x = _z(2.0)
    q = np.random.default_rng(14)
    for k in range(10):
        n = n_de(0.15)
        poe(x, seno(varre(2000, 800, n), n) * env(n, 0.005, 0.12) * 0.025, q.uniform(0, 0.45))
    for k in range(5):
        poe(x, _baque(q.uniform(120, 200), 70, 0.15, 0.3), 0.35 + 0.08 * k)
    poe(x, _explosao(rng, 0.8, 0.5), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Zero

def raikousen(rng, v):
    """Zero: o avanço relâmpago (o estalo elétrico que corre) e o corte do sabre."""
    x = _z(1.8)
    poe(x, graos(rng, n_de(0.3), 40, 0.0, 0.9, 2500, 9000, 0.002) * 0.4, 0.05)
    poe(x, _whoosh(rng, 0.2, 1500, 9000, 0.8, 1.3, 0.4), 0.05)
    n = n_de(0.4)
    poe(x, (satura(seno(varre(140, 100, n), n), 2) * 0.06 + passa(rosa(rng, n), 1000, 4000, 2) * 0.1) * env(n, 0.005, 0.3), 0.25)
    return reverb(x, 0.5, 0.25)


def zeromm_preparo(rng, v):
    """Zero (Preparo): o Z-Saber vibrando e carregando (o zumbido que sobe)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(90, 180, n) * (1 + 0.02 * np.sin(2 * math.pi * 7 * t)), n), 2) * sobe_e_some(n, 0.8, 1.2) * 0.07, 0.0)
    return reverb(x, 0.4, 0.2)


def sequencia_final(rng, v):
    """Zero: o grande corte em meia-lua e os raios caindo."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.35, 800, 8000, 0.8, 1.3, 0.55), 0.0)
    n = n_de(0.5)
    poe(x, satura(seno(varre(160, 90, n), n), 2) * env(n, 0.005, 0.4) * 0.08, 0.1)
    poe(x, _trovao(rng, 0.8, 0.45), 0.35)
    poe(x, graos(rng, n_de(0.5), 50, 0.0, 0.9, 2500, 9000, 0.002) * 0.35, 0.35)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Mario

def flor_de_fogo(rng, v):
    """Mario: o "power-up" da flor e as bolas de fogo quicando."""
    x = _z(1.8)
    for k, f in enumerate((523, 659, 784, 1047)):
        poe(x, _quadrada(f, n_de(0.05)) * env(n_de(0.05), 0.003, 0.04) * 0.025, 0.05 * k)
    for k in range(3):
        poe(x, _piu(900, 500, 0.06, 0.04), 0.3 + 0.12 * k)
        poe(x, passa(rosa(rng, n_de(0.08)), 300, 3000, 2) * env(n_de(0.08), 0.005, 0.06) * 0.25, 0.33 + 0.12 * k)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.75)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "kit-primeiros-socorros": (kit_primeiros_socorros, "Jill: o kit de primeiros socorros"),
    "cobertura-tatica": (cobertura_tatica, "Jill: a cobertura tática"),
    "jill-preparo": (jill_preparo, "Jill: a seringa (Preparo)"),
    "resistencia-adquirida": (resistencia_adquirida, "Jill: a resistência adquirida"),
    "deslocamento-wesker": (deslocamento_wesker, "Wesker: o deslocamento"),
    "golpe-cruzado": (golpe_cruzado, "Wesker: o golpe cruzado"),
    "supremacia-wesker": (supremacia_wesker, "Wesker: a supremacia"),
    "arco-recurvo": (arco_recurvo, "Lara: o arco recurvo"),
    "armadilha-de-cabo": (armadilha_de_cabo, "Lara: a armadilha de cabo"),
    "lara-preparo": (lara_preparo, "Lara: a mira (Preparo)"),
    "tiro-perfeito": (tiro_perfeito, "Lara: o tiro perfeito"),
    "multidao": (multidao, "Ezio: a multidão"),
    "execucao-em-cadeia": (execucao_em_cadeia, "Ezio: a execução em cadeia"),
    "homing-attack": (homing_attack, "Sonic: o Homing Attack"),
    "sonic-preparo": (sonic_preparo, "Sonic: as Esmeraldas (Preparo)"),
    "super-sonic": (super_sonic, "Sonic: o Super Sonic"),
    "chaos-spear": (chaos_spear, "Shadow: Chaos Spear"),
    "chaos-control": (chaos_control, "Shadow: Chaos Control"),
    "shadow-preparo": (shadow_preparo, "Shadow: a Esmeralda (Preparo)"),
    "lanca-das-esmeraldas": (lanca_das_esmeraldas, "Shadow: a Lança das Esmeraldas"),
    "raikousen": (raikousen, "Zero: Raikousen"),
    "zeromm-preparo": (zeromm_preparo, "Zero: o Z-Saber (Preparo)"),
    "sequencia-final": (sequencia_final, "Zero: a sequência final"),
    "flor-de-fogo": (flor_de_fogo, "Mario: a flor de fogo"),
}
