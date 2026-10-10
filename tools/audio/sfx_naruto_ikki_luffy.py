"""Os sons das habilidades do Naruto, do Ikki e do Luffy (veja tools/vfx/familias_v2/naruto_ikki_luffy.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (CRISTAL, SR, assobio, baque, env, graos, n_de, passa, poe, reverb, rosa, ruido, satura, seno,
                 sobe_e_some, varre)


def _puf(rng, g=1.0):
    """O "puf" da fumaça de um clone: um sopro abafado e curto."""
    n = n_de(0.3)
    return (passa(rosa(rng, n), 150, 1800, 2) * env(n, 0.004, 0.09) * 1.2 + baque(n, 160, 110, 0.05, 0.2) * 0.3) * g


def _giro(rng, seg, f_am=35.0, lo=600, hi=5000):
    """Um zumbido que gira (o Rasengan): ruído filtrado pulsando muito rápido."""
    n = n_de(seg)
    t = np.arange(n) / SR
    return passa(ruido(rng, n), lo, hi, 2) * (0.55 + 0.45 * np.sin(2 * math.pi * f_am * t)) + seno(varre(220, 330, n, 1.0), n) * 0.15


def _grito_de_ave(rng, seg=0.6, f=nota(84)):
    """O grito da fênix: um tom agudo que sobe e cai, com vibrato e aspereza."""
    n = n_de(seg)
    t = np.arange(n) / SR
    curva = f * (1 + 0.25 * np.sin(math.pi * t / seg)) * (1 + 0.02 * np.sin(2 * math.pi * 11 * t))
    fase = 2 * math.pi * np.cumsum(curva) / SR
    x = np.sin(fase) + 0.4 * np.sin(2 * fase) + 0.2 * np.sin(3 * fase)
    return satura(x * env(n, 0.03, seg * 0.6), 1.5) * 0.25


def _fogo_rugindo(rng, seg, g=1.0):
    n = n_de(seg)
    f = B.fogo(rng, 1.0)
    f = f[:n] if len(f) >= n else np.pad(f, (0, n - len(f)))
    return f * g + passa(rosa(rng, n), 60, 900, 2) * sobe_e_some(n, 0.5, 1.4) * 0.4 * g


def _boing(rng, f0=nota(55), seg=0.35, g=1.0):
    """O "boing" de borracha: um tom que balança de altura e morre."""
    n = n_de(seg)
    t = np.arange(n) / SR
    f = f0 * (1 + 0.5 * np.exp(-t * 9) * np.sin(2 * math.pi * 14 * t))
    return np.sin(2 * math.pi * np.cumsum(f) / SR) * env(n, 0.002, seg * 0.5) * 0.35 * g


# --------------------------------------------------------------- Naruto
def clones_naruto(rng, v):
    """Clones das sombras: quatro "puf" de fumaça quase juntos, os clones saltando (sopros curtos) e o
    tom tonto que gira da confusão."""
    x = _z(1.6)
    for k in range(4):
        poe(x, _puf(rng, 0.9), 0.02 + 0.06 * k)
    for k in range(4):
        poe(x, _whoosh(rng, 0.15, 500, 2500, 0.6, g=0.4), 0.3 + 0.05 * k)
    poe(x, B.soco_leve(rng, v) * 0.6, 0.55)
    n = n_de(0.8)
    t = np.arange(n) / SR
    poe(x, seno(nota(72) * (1 + 0.06 * np.sin(2 * math.pi * 5 * t)), n) * env(n, 0.05, 0.4) * 0.12, 0.6)
    return reverb(x, 0.45, 0.2, 6500)


def rasengan_mao(rng, v):
    """O Rasengan girando na mão, no Preparo: o zumbido que gira e cresce."""
    n = n_de(1.1)
    return reverb(_giro(rng, 1.1, 30) * sobe_e_some(n, 0.9, 1.2) * 0.5, 0.3, 0.15, 7000)


def rasengan(rng, v):
    """Rasengan: o zumbido girando no auge, o choque contra o rival virando uma broca (o giro mais
    grave e áspero) e o estouro que empurra tudo, com o vento girando depois."""
    x = _z(1.8)
    poe(x, _giro(rng, 0.35, 40) * 0.5, 0.0)
    poe(x, satura(_giro(rng, 0.5, 55, 200, 2500) * 0.8, 1.6) * env(n_de(0.5), 0.005, 0.3) * 0.7, 0.32)
    poe(x, B.impacto_energia(rng, v) * 0.9, 0.32)
    poe(x, baque(n_de(0.6), 100, 40, 0.22, 0.7) * 1.0, 0.45)
    poe(x, B.explosao(rng, v) * 0.6, 0.5)
    poe(x, assobio(rng, n_de(0.8), 2500, 300, 1.2) * env(n_de(0.8), 0.02, 0.4) * 0.4, 0.55)
    return reverb(x, 0.55, 0.25, 6000)


def modo_kurama(rng, v):
    """Manto da Kurama: o rugido grave da raposa, o chakra acendendo em chamas e o zumbido do manto."""
    x = _z(1.8)
    n = n_de(1.0)
    t = np.arange(n) / SR
    rugido = satura(passa(rosa(rng, n), 70, 1100, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 26 * t)), 3) * sobe_e_some(n, 0.3, 1.3) * 0.7
    poe(x, rugido, 0.0)
    poe(x, seno(varre(70, 50, n, 1.0), n) * env(n, 0.05, 0.6) * 0.3, 0.0)
    poe(x, _fogo_rugindo(rng, 1.0, 0.6), 0.2)
    m = n_de(1.0)
    poe(x, (seno(nota(57), m) + 0.5 * seno(nota(64), m)) * env(m, 0.1, 0.6) * 0.08, 0.4)
    return reverb(x, 0.6, 0.25, 5000)


# --------------------------------------------------------------- Ikki
def ave_fenix(rng, v):
    """Ave Fênix: o fogo acende no punho, a fênix grita e voa (o rugido do fogo passando) e estoura
    no rival em chamas."""
    x = _z(1.9)
    poe(x, _fogo_rugindo(rng, 0.4, 0.5), 0.0)
    poe(x, _grito_de_ave(rng, 0.6, nota(86)), 0.12)
    poe(x, _whoosh(rng, 0.4, 300, 3000, 0.8, g=0.7), 0.2)
    poe(x, B.explosao(rng, v) * 0.9, 0.6)
    poe(x, _fogo_rugindo(rng, 0.9, 0.7), 0.62)
    return reverb(x, 0.55, 0.25, 6000)


def golpe_fantasma(rng, v):
    """Golpe Fantasma: um toque seco (o dedo), um tom estranho que treme e desce (a mente perdendo o
    rumo), ecos e o sopro do fantasma subindo."""
    x = _z(1.8)
    poe(x, B.soco_leve(rng, v) * 0.5, 0.0)
    poe(x, _brilho(rng, 0.5, nota(91), 0.15, CRISTAL), 0.02)
    n = n_de(1.1)
    t = np.arange(n) / SR
    tom = seno(varre(nota(76), nota(52), n, 1.2) * (1 + 0.03 * np.sin(2 * math.pi * 6 * t)), n) + 0.6 * seno(varre(nota(77), nota(53), n, 1.2), n)
    poe(x, tom * env(n, 0.03, 0.7) * 0.15, 0.08)
    poe(x, assobio(rng, n_de(0.8), 500, 2000, 1.0) * sobe_e_some(n_de(0.8), 0.6, 1.4) * 0.35, 0.6)
    return reverb(x, 0.8, 0.4, 4500)


def fenix_asas(rng, v):
    """As asas de fogo abrindo no Ikki (antes do Renascimento): o fogo acende de uma vez."""
    x = _z(1.0)
    poe(x, _fogo_rugindo(rng, 0.9, 0.7) * sobe_e_some(n_de(0.9), 0.5, 1.2), 0.0)
    poe(x, _whoosh(rng, 0.4, 200, 1800, 0.6, g=0.5), 0.0)
    return reverb(x, 0.5, 0.2, 6000)


def renascimento(rng, v):
    """Renascimento: a coluna de fogo sobe rugindo, a fênix grita alto enquanto sobe e o calor estoura."""
    x = _z(2.0)
    poe(x, B.explosao(rng, v) * 0.7, 0.0)
    poe(x, _fogo_rugindo(rng, 1.4, 0.9), 0.0)
    poe(x, baque(n_de(0.7), 90, 35, 0.3, 0.6) * 0.9, 0.0)
    poe(x, _grito_de_ave(rng, 0.8, nota(84)), 0.4)
    poe(x, _brilho(rng, 0.9, nota(79), 0.15, CRISTAL), 0.5)
    return reverb(x, 0.6, 0.28, 5500)


# --------------------------------------------------------------- Luffy
def gomu_gatling(rng, v):
    """Gomu Gomu no Gatling: o braço estica (um "boing" que estica) e a metralhadora de socos — cada
    um com o estalo de borracha —, acelerando no meio."""
    x = _z(1.7)
    poe(x, _boing(rng, nota(48), 0.3, 1.0), 0.0)
    em = 0.15
    for k in range(16):
        poe(x, B.soco_leve(rng, v) * rng.uniform(0.5, 0.75), em)
        poe(x, _boing(rng, nota(60 + rng.integers(-3, 4)), 0.1, 0.35), em)
        em += 0.07 if 3 < k < 12 else 0.09
    poe(x, B.soco_pesado(rng, v) * 0.8, em)
    return reverb(x, 0.45, 0.2, 6500)


def corpo_de_borracha(rng, v):
    """Corpo de borracha: o corpo estica e volta (boings que balançam) e os golpes ricocheteiam
    (zings agudos que se afastam)."""
    x = _z(1.4)
    poe(x, _boing(rng, nota(45), 0.5, 1.2), 0.0)
    poe(x, _boing(rng, nota(52), 0.4, 0.8), 0.22)
    for k in range(3):
        n = n_de(0.3)
        poe(x, seno(varre(nota(88), nota(76), n, 1.0), n) * env(n, 0.002, 0.15) * 0.12, 0.15 + 0.2 * k)
        poe(x, B.soco_leve(rng, v) * 0.35, 0.14 + 0.2 * k)
    return reverb(x, 0.4, 0.2, 7000)


def gear_fifth(rng, v):
    """Gear Fifth: o tambor da libertação (tum-tum… tum-tum), o vento das nuvens e um brilho alegre
    subindo."""
    x = _z(2.0)
    for k in range(4):
        base = 0.0 + 0.45 * k
        for d in (0.0, 0.14):
            poe(x, baque(n_de(0.35), 120, 70, 0.12, 0.4) * 0.9, base + d)
    poe(x, assobio(rng, n_de(1.6), 400, 2000, 1.0) * sobe_e_some(n_de(1.6), 0.6, 1.2) * 0.3, 0.1)
    for k, f in enumerate((67, 72, 76, 79)):
        poe(x, _brilho(rng, 0.6, nota(f), 0.12, CRISTAL), 0.9 + 0.12 * k)
    return reverb(x, 0.55, 0.25, 7000)


SONS: dict = {
    "clones-naruto": (clones_naruto, "Clones das sombras: os puf de fumaça e os clones saltando"),
    "rasengan-mao": (rasengan_mao, "o Rasengan girando na mão, no Preparo"),
    "rasengan": (rasengan, "Rasengan: o giro, a broca e o estouro"),
    "modo-kurama": (modo_kurama, "Manto da Kurama: o rugido e o chakra em chamas"),
    "ave-fenix": (ave_fenix, "Ave Fênix: o grito da fênix e o fogo estourando"),
    "golpe-fantasma": (golpe_fantasma, "Golpe Fantasma: o toque e a mente perdendo o rumo"),
    "fenix-asas": (fenix_asas, "as asas de fogo abrindo no Ikki"),
    "renascimento": (renascimento, "Renascimento: a coluna de fogo e a fênix gritando"),
    "gomu-gatling": (gomu_gatling, "Gomu Gomu no Gatling: o braço esticando e a metralhadora de socos"),
    "corpo-de-borracha": (corpo_de_borracha, "Corpo de borracha: os boings e os ricochetes"),
    "gear-fifth-nika": (gear_fifth, "Gear Fifth: o tambor da libertação e as nuvens"),
}
