"""Os sons da rodada 53 das habilidades próprias (veja tools/vfx/familias_v2/rodada53.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.3, f0=1500, f1=7000):
    n = n_de(seg)
    t = _t(n)
    corte = (np.sin(2 * math.pi * 55 * t) > 0.2).astype(float)
    return satura(passa(rosa(rng, n), f0, f1, 2) * corte, 3) * env(n, 0.005, seg * 0.5) * g


def _sabre_zumbido(rng, seg, f=110, g=0.04):
    n = n_de(seg)
    t = _t(n)
    x = satura(seno(f, n) + seno(f * 1.02, n) * 0.8 + seno(f * 2, n) * 0.3, 2) + passa(rosa(rng, n), 200, 1500, 2) * 0.15
    return x * (0.85 + 0.15 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.15, 1.2) * g


def _sabre_liga(rng, g=0.04):
    n = n_de(0.35)
    return satura(seno(varre(70, 120, n), n) + passa(rosa(rng, n), 300, 3000, 2) * 0.4, 3) * env(n, 0.01, 0.25) * g


def _blaster(rng, g=0.025):
    """O tiro de blaster ("piu" descendo rápido com o eco metálico)."""
    n = n_de(0.2)
    return satura(seno(varre(2400, 300, n), n), 2) * env(n, 0.002, 0.18) * g


def _tiro(rng, g=0.6):
    x = _z(0.6)
    poe(x, estalo(rng, n_de(0.03), 500, 9000, 0.01) * g * 2.0, 0.0)
    poe(x, _baque(150, 60, 0.15, g * 0.7, 2.5), 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * env(n, 0.002, 0.35) * g * 0.4, 0.0)
    return x


def _cartucho(rng, g=0.012):
    x = _z(0.5)
    for k, d in enumerate((0.0, 0.12, 0.2)):
        poe(x, _sino(rng, 3800 - 300 * k, 0.1, g * (1 - 0.3 * k), METAL), d)
    return x


def _codigo_digital(rng, seg, g=0.01):
    """Os bipes digitais do código caindo."""
    x = _z(seg + 0.2)
    q = np.random.default_rng(23)
    for k in range(int(seg * 25)):
        f = q.choice([1760, 2093, 2349, 2637, 3136])
        n = n_de(0.02)
        poe(x, seno(f, n) * env(n, 0.001, 0.018) * g, k / 25)
    return x


# ------------------------------------------------------------------ Luke

def sabre_verde_luke(rng, v):
    """Luke: o sabre verde ligando e o corte zunindo."""
    x = _z(2.0)
    poe(x, _sabre_liga(rng, 0.045), 0.0)
    poe(x, _sabre_zumbido(rng, 0.6, 120, 0.035), 0.12)
    poe(x, _whoosh(rng, 0.2, 200, 3000, 0.8, 1.3, 0.4), 0.25)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.38)
    n = n_de(0.15)
    poe(x, satura(passa(rosa(rng, n), 1000, 6000, 2), 3) * env(n, 0.005, 0.13) * 0.25, 0.38)
    return reverb(x, 0.6, 0.3)


def defletir(rng, v):
    """Luke: o sabre girando e os tiros de blaster batendo e voltando."""
    x = _z(2.0)
    z = _sabre_zumbido(rng, 0.9, 120, 0.03)
    t = _t(len(z))
    poe(x, z * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t) ** 2), 0.0)
    for k in range(3):
        poe(x, _blaster(rng, 0.02), 0.1 + 0.18 * k)
        poe(x, estalo(rng, n_de(0.02), 2000, 9000, 0.004) * 0.8, 0.25 + 0.18 * k)
        poe(x, _blaster(rng, 0.015), 0.26 + 0.18 * k)
    return reverb(x, 0.6, 0.3)


def luke_preparo(rng, v):
    """Luke (Preparo): a mira do X-Wing apitando até travar (em laço)."""
    x = _z(1.4)
    for k in range(4):
        n = n_de(0.06)
        poe(x, seno(1500 + 150 * k, n) * env(n, 0.003, 0.05) * 0.012, 0.12 * k)
    n2 = n_de(0.3)
    poe(x, seno(2200, n2) * env(n2, 0.01, 0.05) * 0.012, 0.55)
    return reverb(x, 0.5, 0.25)


def tiro_na_trincheira(rng, v):
    """Luke: os torpedos de prótons zunindo, fazendo a curva e a explosão da Estrela."""
    x = _z(2.5)
    for k in range(2):
        n = n_de(0.5)
        poe(x, seno(varre(800, 1400, n), n) * env(n, 0.05, 0.1) * 0.015, 0.05 + 0.06 * k)
        poe(x, _whoosh(rng, 0.45, 1000, 6000, 0.7, 1.3, 0.3), 0.05 + 0.06 * k)
    poe(x, _baque(35, 14, 1.4, 1.0, 3.6), 0.5)
    poe(x, _explosao(rng, 1.1, 35), 0.5)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Palpatine

def raio_da_forca_palpatine(rng, v):
    """Palpatine: os relâmpagos da Força estalando sem parar no rival."""
    x = _z(2.0)
    poe(x, _choque(rng, 0.7, 0.35, 800, 8000), 0.1)
    n = n_de(0.7)
    poe(x, satura(seno(90, n) + seno(95, n), 3) * sobe_e_some(n, 0.2, 1.2) * 0.02, 0.1)
    return reverb(x, 0.6, 0.3)


def tudo_conforme_o_plano(rng, v):
    """Palpatine: a risada do imperador e as peças caindo ("tac-tac-tac")."""
    x = _z(2.3)
    for k in range(5):
        n = n_de(0.1)
        f = 260 * (1 - 0.03 * k)
        poe(x, satura(seno(varre(f * 1.1, f, n), n) + passa(rosa(rng, n), 400, 3000, 2) * 0.6, 3) * env(n, 0.01, 0.08) * 0.022, 0.05 + 0.11 * k)
    for k in range(3):
        poe(x, _baque(300, 180, 0.06, 0.3), 0.6 + 0.07 * k)
        poe(x, _sino(rng, 1047, 0.2, 0.01, METAL), 0.6 + 0.07 * k)
    poe(x, _acorde((147, 175, 208), 0.8, 0.02), 0.75)
    return reverb(x, 0.9, 0.45)


def palpatine_preparo(rng, v):
    """Palpatine (Preparo): a eletricidade zumbindo entre as mãos (em laço)."""
    x = _z(1.4)
    poe(x, _choque(rng, 1.0, 0.18, 1500, 8000), 0.0)
    n = n_de(1.0)
    poe(x, satura(seno(80, n), 3) * sobe_e_some(n, 0.5, 1.2) * 0.015, 0.0)
    return reverb(x, 0.6, 0.3)


def poder_ilimitado(rng, v):
    """Palpatine: "PODER ILIMITADO!" — a tempestade de relâmpagos em todos."""
    x = _z(2.5)
    n = n_de(0.5)
    poe(x, satura(seno(varre(180, 260, n), n) + passa(rosa(rng, n), 300, 3000, 2) * 0.6, 4) * env(n, 0.05, 0.3) * 0.03, 0.0)
    for k in range(3):
        poe(x, _choque(rng, 0.6, 0.3, 800, 8000), 0.2 + 0.08 * k)
    poe(x, _baque(60, 22, 0.6, 0.8, 2.8), 0.35)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Neo

def kung_fu(rng, v):
    """Neo: "eu sei kung fu" — a sequência rápida de golpes."""
    x = _z(2.0)
    poe(x, _codigo_digital(rng, 0.5, 0.008), 0.0)
    for k in range(5):
        poe(x, _whoosh(rng, 0.07, 800, 6000, 0.6, 1.3, 0.25), 0.08 + 0.08 * k)
        poe(x, _baque(170 + 20 * (k % 2), 80, 0.12, 0.45), 0.15 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def parar_as_balas(rng, v):
    """Neo: as balas zunindo, parando no ar (o tempo desacelerando) e caindo no chão."""
    x = _z(2.4)
    for k in range(3):
        n = n_de(0.3)
        poe(x, seno(varre(1200, 300, n), n) * env(n, 0.01, 0.25) * 0.015, 0.05 + 0.04 * k)
    n2 = n_de(0.6)
    poe(x, passa(rosa(rng, n2), 100, 1500, 2) * sobe_e_some(n2, 0.3, 1.2) * 0.15, 0.25)
    for k in range(4):
        poe(x, _sino(rng, 3000 - 200 * k, 0.15, 0.012, METAL), 0.95 + 0.06 * k)
    return reverb(x, 0.8, 0.4)


def neo_preparo(rng, v):
    """Neo (Preparo): o código caindo (os bipes digitais em laço)."""
    x = _z(1.4)
    poe(x, _codigo_digital(rng, 1.0, 0.008), 0.0)
    n = n_de(1.0)
    poe(x, seno(110, n) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    return reverb(x, 0.6, 0.3)


def o_escolhido(rng, v):
    """Neo: o mergulho no rival e o rival se desfazendo em código."""
    x = _z(2.5)
    poe(x, _codigo_digital(rng, 0.4, 0.01), 0.0)
    poe(x, _whoosh(rng, 0.25, 300, 4000, 0.85, 1.3, 0.5), 0.15)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.4)
    poe(x, _explosao(rng, 0.6, 50), 0.4)
    poe(x, _codigo_digital(rng, 0.8, 0.014), 0.45)
    poe(x, _acorde((220, 330, 440, 659), 0.9, 0.02), 0.5)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Agente Smith

def soco_do_agente_smith(rng, v):
    """Agente Smith: o soco reto e seco com o estalo do terno."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.15, 400, 4000, 0.8, 1.3, 0.4), 0.15)
    poe(x, _baque(110, 45, 0.35, 0.8, 2.6), 0.3)
    poe(x, estalo(rng, n_de(0.03), 800, 5000, 0.008) * 0.8, 0.3)
    poe(x, _codigo_digital(rng, 0.3, 0.008), 0.35)
    return reverb(x, 0.5, 0.25)


def copias_do_smith(rng, v):
    """Agente Smith: as cópias surgindo uma a uma ("eu... eu... eu...")."""
    x = _z(2.2)
    for k in range(5):
        n = n_de(0.15)
        f = 140 - 5 * k
        poe(x, satura(seno(varre(f, f * 0.9, n), n), 2) * passa(rosa(rng, n), 200, 1500, 2) * env(n, 0.02, 0.12) * 0.25, 0.05 + 0.1 * k)
        poe(x, _codigo_digital(rng, 0.15, 0.008), 0.05 + 0.1 * k)
    poe(x, _sino(rng, 1760, 0.3, 0.015, METAL), 0.7)
    return reverb(x, 0.8, 0.4)


def smith_preparo(rng, v):
    """Agente Smith (Preparo): o código preto escorrendo (o zumbido grave em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(73.4, n) + seno(77.8, n)) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    poe(x, _codigo_digital(rng, 1.0, 0.006), 0.0)
    return reverb(x, 0.6, 0.3)


def assimilar(rng, v):
    """Agente Smith: a mão entrando no peito e o código passando para ele."""
    x = _z(2.3)
    poe(x, _baque(150, 70, 0.2, 0.5), 0.22)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 15 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.25)
    poe(x, _codigo_digital(rng, 0.6, 0.012), 0.45)
    n2 = n_de(0.5)
    poe(x, seno(varre(600, 200, n2), n2) * env(n2, 0.05, 0.4) * 0.02, 0.5)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ John Wick

def tiro_na_testa_wick(rng, v):
    """John Wick: o tiro seco e preciso e o cartucho tilintando no chão."""
    x = _z(2.0)
    poe(x, _tiro(rng, 0.7), 0.2)
    poe(x, _cartucho(rng, 0.014), 0.55)
    poe(x, _sino(rng, 1319, 0.3, 0.012, METAL), 0.4)
    return reverb(x, 0.6, 0.3)


def lapis(rng, v):
    """John Wick: o lápis girando no ar e cravando."""
    x = _z(1.8)
    n = n_de(0.35)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t) ** 2) * env(n, 0.02, 0.3) * 0.2, 0.0)
    poe(x, _baque(170, 80, 0.15, 0.45), 0.35)
    poe(x, estalo(rng, n_de(0.02), 1000, 6000, 0.004) * 0.8, 0.35)
    return reverb(x, 0.4, 0.2)


def wick_preparo(rng, v):
    """John Wick (Preparo): a moeda de ouro girando no ar ("tlin") (em laço)."""
    x = _z(1.4)
    poe(x, _sino(rng, 2637, 0.6, 0.025, METAL), 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(2637, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t)) * env(n, 0.01, 0.5) * 0.006, 0.05)
    poe(x, _sino(rng, 1976, 0.4, 0.015, METAL), 0.8)
    return reverb(x, 0.6, 0.3)


def excomunicado(rng, v):
    """John Wick: a rajada de seis tiros, os cartuchos e o tiro final."""
    x = _z(2.4)
    for k in range(6):
        poe(x, _tiro(rng, 0.45), 0.1 + 0.07 * k)
        poe(x, _cartucho(rng, 0.008), 0.3 + 0.07 * k)
    poe(x, _tiro(rng, 0.8), 0.58)
    poe(x, _baque(70, 28, 0.6, 0.8, 2.8), 0.6)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ T-800

def escopeta_t800(rng, v):
    """T-800: a escopeta engatilhando ("chk-chk") e o tiro grosso."""
    x = _z(2.1)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.03), 600, 4000, 0.008) * 0.8, 0.05 + 0.1 * k)
        poe(x, _baque(300, 200, 0.05, 0.25), 0.05 + 0.1 * k)
    poe(x, _tiro(rng, 0.9), 0.28)
    poe(x, _baque(60, 22, 0.5, 0.7, 2.6), 0.28)
    poe(x, _cartucho(rng, 0.01), 0.6)
    return reverb(x, 0.7, 0.35)


def eu_voltarei(rng, v):
    """T-800: os servos do endoesqueleto e a placa de metal fechando ("CLANG")."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.15)
        poe(x, satura(seno(varre(300 + 100 * k, 600 + 100 * k, n), n), 2) * env(n, 0.02, 0.1) * 0.012, 0.05 + 0.12 * k)
    poe(x, _sino(rng, 220, 1.0, 0.05, METAL), 0.4)
    poe(x, _baque(100, 50, 0.3, 0.6), 0.4)
    poe(x, _brilho(rng, 0.5, 1568, 0.012, CRISTAL), 0.5)
    return reverb(x, 0.6, 0.3)


def t800_preparo(rng, v):
    """T-800 (Preparo): a visão computando (os bipes e o zumbido em laço)."""
    x = _z(1.4)
    for k in range(6):
        n = n_de(0.03)
        poe(x, seno((880, 1175, 988, 1320, 880, 1047)[k], n) * env(n, 0.002, 0.025) * 0.01, 0.16 * k)
    n2 = n_de(1.0)
    poe(x, satura(seno(60, n2), 2) * sobe_e_some(n2, 0.5, 1.2) * 0.015, 0.0)
    return reverb(x, 0.5, 0.25)


def hasta_la_vista(rng, v):
    """T-800: a energia carregando na arma e o tiro gigante ("hasta la vista, baby")."""
    x = _z(2.5)
    n = n_de(0.5)
    poe(x, seno(varre(80, 400, n), n) * env(n, 0.45, 0.05) * 0.04, 0.0)
    poe(x, _tiro(rng, 1.0), 0.4)
    poe(x, _baque(35, 14, 1.4, 1.0, 3.6), 0.5)
    poe(x, _explosao(rng, 1.1, 35), 0.5)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "sabre-verde-luke": (sabre_verde_luke, "Luke: o sabre verde"),
    "defletir": (defletir, "Luke: defletir"),
    "luke-preparo": (luke_preparo, "Luke: a mira do X-Wing (Preparo)"),
    "tiro-na-trincheira": (tiro_na_trincheira, "Luke: o tiro na trincheira"),
    "raio-da-forca-palpatine": (raio_da_forca_palpatine, "Palpatine: o raio da Força"),
    "tudo-conforme-o-plano": (tudo_conforme_o_plano, "Palpatine: tudo conforme o plano"),
    "palpatine-preparo": (palpatine_preparo, "Palpatine: a eletricidade nas mãos (Preparo)"),
    "poder-ilimitado": (poder_ilimitado, "Palpatine: poder ilimitado"),
    "kung-fu": (kung_fu, "Neo: kung fu"),
    "parar-as-balas": (parar_as_balas, "Neo: parar as balas"),
    "neo-preparo": (neo_preparo, "Neo: o código caindo (Preparo)"),
    "o-escolhido": (o_escolhido, "Neo: o escolhido"),
    "soco-do-agente-smith": (soco_do_agente_smith, "Agente Smith: o soco"),
    "copias-do-smith": (copias_do_smith, "Agente Smith: as cópias"),
    "smith-preparo": (smith_preparo, "Agente Smith: o código escorrendo (Preparo)"),
    "assimilar": (assimilar, "Agente Smith: assimilar"),
    "tiro-na-testa-wick": (tiro_na_testa_wick, "John Wick: o tiro na cabeça"),
    "lapis": (lapis, "John Wick: o lápis"),
    "wick-preparo": (wick_preparo, "John Wick: a moeda de ouro (Preparo)"),
    "excomunicado": (excomunicado, "John Wick: excomunicado"),
    "escopeta-t800": (escopeta_t800, "T-800: a escopeta"),
    "eu-voltarei": (eu_voltarei, "T-800: eu voltarei"),
    "t800-preparo": (t800_preparo, "T-800: a visão computando (Preparo)"),
    "hasta-la-vista": (hasta_la_vista, "T-800: hasta la vista"),
}
