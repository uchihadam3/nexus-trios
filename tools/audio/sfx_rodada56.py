"""Os sons da rodada 56 das habilidades próprias (veja tools/vfx/familias_v2/rodada56.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fumaca_magica(rng, seg, g=0.25):
    """A fumaça do Gênio saindo da lâmpada: o sopro que sobe e o brilho cintilando."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 300, 4000, 2) * (0.75 + 0.25 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.4, 1.3) * g


def _risada(rng, f0, vezes, g=0.04, passo=0.09):
    """Uma risada aguda em pulos ("hi-hi-hi"): sílabas curtas descendo."""
    x = _z(passo * vezes + 0.2)
    for k in range(vezes):
        n = n_de(passo * 0.7)
        f = f0 * (1 - 0.04 * k)
        silaba = (seno(varre(f, f * 0.85, n), n) + seno(varre(f * 2, f * 1.7, n), n) * 0.4 + passa(rosa(rng, n), 1500, 5000, 2) * 0.3)
        poe(x, satura(silaba, 2) * env(n, 0.005, passo * 0.5) * g, passo * k)
    return x


def _rosnado(rng, seg, f=80, g=0.06):
    n = n_de(seg)
    t = _t(n)
    return satura(seno(f * (1 + 0.05 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 60, 900, 2) * 1.2, 5) * sobe_e_some(n, 0.35, 1.2) * g


def _choque(rng, seg, g=0.2):
    """O estalo elétrico (os raios verdes do One For All)."""
    x = _z(seg + 0.05)
    q = np.random.default_rng(56)
    for k in range(int(seg * 40)):
        poe(x, estalo(rng, n_de(0.012), 2500, 9000, 0.002) * g * q.uniform(0.3, 1.0), q.uniform(0, seg))
    return x


def _onda_dagua(rng, seg, g=0.4):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 80, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.45, 1.2) * g


# ------------------------------------------------------------------ Gênio

def primeiro_desejo(rng, v):
    """Gênio: a lâmpada esfregada, a fumaça subindo e o "plim" do primeiro desejo."""
    x = _z(2.2)
    poe(x, _sino(rng, 880, 0.4, 0.02, METAL), 0.0)
    poe(x, _fumaca_magica(rng, 0.7, 0.22), 0.1)
    poe(x, _piu(600, 1800, 0.35, 0.03), 0.35)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 1568 + 220 * k, 0.03, CRISTAL), 0.5 + 0.05 * k)
    poe(x, _whoosh(rng, 0.35, 1000, 6000, 0.4, 1.3, 0.35), 0.5)
    return reverb(x, 0.9, 0.45)


def segundo_desejo(rng, v):
    """Gênio: a fumaça, o "tcharam!" e os escudos dourados fechando no trio."""
    x = _z(2.3)
    poe(x, _fumaca_magica(rng, 0.6, 0.2), 0.05)
    poe(x, _acorde((523, 659, 784), 0.25, 0.03), 0.3)
    poe(x, _acorde((659, 831, 988, 1319), 0.8, 0.035), 0.42)
    for k in range(3):
        poe(x, _sino(rng, 330 + 40 * k, 0.6, 0.03, METAL), 0.45 + 0.06 * k)
    return reverb(x, 0.9, 0.45)


def genio_preparo(rng, v):
    """Gênio (Preparo): a lâmpada sendo esfregada ("fric-fric") e a fumaça cintilando (em laço)."""
    x = _z(1.4)
    for k in range(6):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.02, 0.06) * 0.08, 0.05 + 0.16 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(784, n) + seno(1175, n) * 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.01, 0.0)
    return reverb(x, 0.7, 0.35)


def poder_cosmico(rng, v):
    """Gênio: o punho azul gigante ("POW!" de desenho animado) e as estrelinhas girando."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.3, 120, 1500, 0.9, 1.3, 0.6), 0.05)
    poe(x, _baque(55, 20, 0.9, 1.0, 3.0), 0.33)
    poe(x, _explosao(rng, 0.55, 50), 0.33)
    for k in range(4):
        poe(x, _piu(1400 + 200 * (k % 2), 2000 - 200 * (k % 2), 0.12, 0.02), 0.55 + 0.1 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Scar

def hienas(rng, v):
    """Scar: as hienas correndo (as patas) e as risadas."""
    x = _z(2.3)
    for k in range(10):
        poe(x, _baque(150, 80, 0.06, 0.2), 0.03 + 0.05 * k)
    poe(x, _risada(rng, 900, 6, 0.035), 0.1)
    poe(x, _risada(rng, 1100, 5, 0.03, 0.08), 0.3)
    poe(x, _risada(rng, 780, 6, 0.03), 0.5)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 300, 2500, 0.5, 1.3, 0.3), 0.5 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def garras_de_leao(rng, v):
    """Scar: as duas patadas cruzando ("shhk-shhk") e o rosnado."""
    x = _z(2.0)
    poe(x, _rosnado(rng, 0.4, 90, 0.05), 0.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.7, 1.3, 0.5), 0.1 + 0.18 * k)
        for j in range(3):
            poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.01) * 0.4, 0.17 + 0.18 * k + 0.015 * j)
    poe(x, _baque(100, 50, 0.3, 0.5), 0.35)
    return reverb(x, 0.6, 0.3)


def scar_preparo(rng, v):
    """Scar (Preparo): o rosnado baixo e a música sombria do "Longa vida ao rei" (em laço)."""
    x = _z(1.4)
    poe(x, _rosnado(rng, 1.1, 70, 0.04), 0.0)
    poe(x, _acorde((110, 131, 156), 1.1, 0.018, 0.3, 0.5), 0.1)
    return reverb(x, 0.8, 0.4)


def longa_vida_ao_rei(rng, v):
    """Scar: o "longa vida ao rei", as garras cravando e o rival caindo no desfiladeiro."""
    x = _z(2.7)
    poe(x, _rosnado(rng, 0.45, 110, 0.05), 0.0)
    poe(x, _whoosh(rng, 0.25, 600, 6000, 0.8, 1.3, 0.5), 0.3)
    for j in range(3):
        poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.012) * 0.5, 0.42 + 0.02 * j)
    poe(x, _sino(rng, 1047, 0.4, 0.03, METAL), 0.5)
    poe(x, _piu(900, 200, 0.6, 0.03), 0.6)
    poe(x, _baque(45, 18, 0.9, 1.0, 3.0), 1.15)
    poe(x, _sopro(rng, 0.8, 80, 1500, 0.35), 1.15)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Jack Esqueleto

def susto(rng, v):
    """Jack Esqueleto: o silêncio e o "BUUU!" de repente."""
    x = _z(2.1)
    poe(x, _sopro(rng, 0.25, 200, 1500, 0.08), 0.0)
    n = n_de(0.6)
    t = _t(n)
    voz = seno(varre(160, 110, n), n) + seno(varre(320, 220, n), n) * 0.5 + seno(varre(480, 330, n), n) * 0.25
    poe(x, satura(voz * (1 + 0.2 * np.sin(2 * math.pi * 6 * t)), 3) * env(n, 0.02, 0.4) * 0.06, 0.22)
    poe(x, _baque(80, 40, 0.3, 0.6), 0.22)
    poe(x, _acorde((233, 277, 349), 0.7, 0.02, 0.01, 0.4), 0.3)
    return reverb(x, 0.8, 0.4)


def fogo_de_abobora(rng, v):
    """Jack Esqueleto: a abóbora voando com o fogo crepitando e o estouro de chamas."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.4, 200, 2500, 0.8, 1.3, 0.5), 0.05)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 3500, 2) * env(n, 0.05, 0.2) * 0.25, 0.05)
    poe(x, _explosao(rng, 0.45, 70), 0.38)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.03), 800, 5000, 0.008) * 0.35, 0.45 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def jack_esqueleto_preparo(rng, v):
    """Jack Esqueleto (Preparo): o vento da noite, os morcegos e o xilofone de ossos (em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.2, 300, 1500, 0.08, 0.5), 0.0)
    for k, f in enumerate((587, 698, 622, 523)):
        poe(x, _brilho(rng, 0.25, f, 0.04, METAL), 0.1 + 0.28 * k)
    for k in range(4):
        poe(x, _piu(4000, 5000, 0.03, 0.01), 0.2 + 0.3 * k)
    return reverb(x, 0.8, 0.4)


def noite_das_bruxas(rng, v):
    """Jack Esqueleto: o sino da meia-noite, a revoada de morcegos e o coro de Halloween."""
    x = _z(2.8)
    poe(x, _sino(rng, 196, 1.4, 0.05, SINO), 0.0)
    for k in range(14):
        poe(x, _piu(3500 + 300 * (k % 3), 4500, 0.03, 0.012), 0.25 + 0.04 * k)
        n = n_de(0.05)
        poe(x, passa(rosa(rng, n), 800, 3000, 2) * env(n, 0.005, 0.03) * 0.15, 0.25 + 0.04 * k)
    poe(x, _acorde((147, 175, 208, 247), 1.4, 0.025, 0.2, 0.7), 0.5)
    poe(x, _risada(rng, 300, 5, 0.03, 0.12), 0.9)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Úrsula

def roubar_a_voz(rng, v):
    """Úrsula: a voz sendo puxada (o canto que vai sumindo dentro da concha) e o silêncio."""
    x = _z(2.4)
    n = n_de(1.0)
    t = _t(n)
    canto = (seno(varre(880, 440, n), n) + seno(varre(1320, 660, n), n) * 0.4) * (1 + 0.3 * np.sin(2 * math.pi * 6 * t))
    poe(x, canto * sobe_e_some(n, 0.3, 1.2) * 0.02, 0.2)
    poe(x, _whoosh(rng, 0.7, 3000, 400, 0.6, 1.3, 0.3), 0.3)
    poe(x, _sino(rng, 660, 0.9, 0.04, CRISTAL), 1.05)
    poe(x, _baque(140, 70, 0.15, 0.3), 1.05)
    return reverb(x, 1.0, 0.5)


def tentaculos_de_ursula(rng, v):
    """Úrsula: os tentáculos subindo da água ("splash"), o "squish" das ventosas e o aperto."""
    x = _z(2.3)
    poe(x, _onda_dagua(rng, 0.5, 0.35), 0.05)
    for k in range(4):
        n = n_de(0.08)
        poe(x, satura(passa(rosa(rng, n), 200, 1500, 2), 3) * env(n, 0.01, 0.05) * 0.2, 0.35 + 0.08 * k)
    n = n_de(0.5)
    poe(x, satura(seno(varre(90, 60, n), n), 3) * env(n, 0.05, 0.3) * 0.05, 0.6)
    return reverb(x, 0.8, 0.4)


def ursula_preparo(rng, v):
    """Úrsula (Preparo): o tridente zumbindo, as bolhas e as moreias (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(220, n) + seno(277, n) * 0.6 + seno(330, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    q = np.random.default_rng(560)
    for k in range(7):
        poe(x, _piu(q.uniform(400, 900), q.uniform(1200, 2000), 0.04, 0.012), 0.1 + 0.16 * k)
    return reverb(x, 0.8, 0.4)


def tridente_da_bruxa(rng, v):
    """Úrsula: o redemoinho girando, a risada da bruxa e a onda gigante quebrando nos rivais."""
    x = _z(2.8)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.6, 1.3) * 0.3, 0.0)
    poe(x, _risada(rng, 380, 5, 0.035, 0.11), 0.15)
    poe(x, _onda_dagua(rng, 1.0, 0.5), 0.55)
    poe(x, _baque(50, 25, 0.8, 0.8, 2.5), 0.75)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Deku

def delaware_smash(rng, v):
    """Deku: o estalo do peteleco, a pressão do ar e o dedo quebrando."""
    x = _z(2.1)
    poe(x, _choque(rng, 0.25, 0.15), 0.0)
    poe(x, estalo(rng, n_de(0.03), 1000, 6000, 0.006) * 0.8, 0.2)
    poe(x, _whoosh(rng, 0.4, 100, 3000, 0.4, 1.3, 0.8), 0.2)
    poe(x, _baque(60, 25, 0.6, 0.9, 2.8), 0.38)
    poe(x, estalo(rng, n_de(0.04), 300, 2500, 0.012) * 0.6, 0.42)
    return reverb(x, 0.7, 0.35)


def full_cowl_corpo(rng, v):
    """Deku: o Full Cowl ligando (o zumbido elétrico subindo e os estalos verdes)."""
    x = _z(2.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(varre(120, 240, n), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 40 * t)), 3) * sobe_e_some(n, 0.3, 1.2) * 0.025, 0.0)
    poe(x, _choque(rng, 1.0, 0.18), 0.05)
    poe(x, _whoosh(rng, 0.3, 800, 5000, 0.6, 1.3, 0.4), 0.5)
    return reverb(x, 0.6, 0.3)


def deku_preparo(rng, v):
    """Deku (Preparo): o braço carregando 100% (o zumbido subindo e os estalos em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(90 + 60 * t, n) + seno(180 + 120 * t, n) * 0.4, 3) * sobe_e_some(n, 0.6, 1.2) * 0.03, 0.0)
    poe(x, _choque(rng, 1.1, 0.14), 0.05)
    return reverb(x, 0.6, 0.3)


def united_states_of_smash_deku(rng, v):
    """Deku: "UNITED STATES OF SMASH!" — o soco com os raios, a explosão de ar e o braço quebrando."""
    x = _z(2.7)
    poe(x, _choque(rng, 0.35, 0.2), 0.0)
    poe(x, _whoosh(rng, 0.3, 80, 1500, 0.9, 1.3, 0.7), 0.05)
    poe(x, _baque(35, 12, 1.4, 1.0, 3.8), 0.33)
    poe(x, _explosao(rng, 0.9, 35), 0.33)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 150, 3000, 2) * sobe_e_some(n, 0.25, 1.2) * 0.4, 0.38)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 300, 2500, 0.012) * 0.5, 0.45 + 0.05 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ All Might

def texas_smash(rng, v):
    """All Might: o soco reto e a rajada de vento ("FUUUM")."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.2, 200, 2000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _baque(70, 30, 0.5, 0.9, 2.8), 0.22)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 200, 4000, 2) * sobe_e_some(n, 0.15, 1.2) * 0.45, 0.22)
    return reverb(x, 0.7, 0.35)


def estou_aqui(rng, v):
    """All Might: "ESTOU AQUI!" — a risada heroica, a fanfarra dourada e o escudo."""
    x = _z(2.4)
    poe(x, _risada(rng, 200, 4, 0.04, 0.13), 0.0)
    poe(x, _acorde((392, 494, 587), 0.3, 0.03), 0.5)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.035), 0.75)
    poe(x, _sino(rng, 262, 0.8, 0.04, METAL), 0.75)
    return reverb(x, 0.9, 0.45)


def allmight_preparo(rng, v):
    """All Might (Preparo): o One For All carregando (o coro grave subindo em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(131 + 30 * t, n) + seno(196 + 45 * t, n) * 0.6 + seno(262 + 60 * t, n) * 0.4) * sobe_e_some(n, 0.6, 1.2) * 0.02, 0.0)
    poe(x, _sopro(rng, 1.1, 200, 2000, 0.1, 0.6), 0.0)
    return reverb(x, 0.8, 0.4)


def united_states_of_smash_allmight(rng, v):
    """All Might: o mergulho do alto, o soco gigante e o tornado subindo."""
    x = _z(2.9)
    poe(x, _whoosh(rng, 0.4, 2000, 150, 0.9, 1.3, 0.6), 0.0)
    poe(x, _baque(30, 10, 1.6, 1.0, 4.0), 0.38)
    poe(x, _explosao(rng, 1.0, 30), 0.38)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 100, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.45, 0.45)
    poe(x, _acorde((262, 330, 392, 523), 1.0, 0.025, 0.05, 0.6), 0.5)
    return reverb(x, 1.0, 0.5)


SONS: dict = {
    "primeiro-desejo": (primeiro_desejo, "Gênio: o primeiro desejo"),
    "segundo-desejo": (segundo_desejo, "Gênio: o segundo desejo"),
    "genio-preparo": (genio_preparo, "Gênio: a lâmpada esfregada (Preparo)"),
    "poder-cosmico": (poder_cosmico, "Gênio: poder cósmico"),
    "hienas": (hienas, "Scar: as hienas"),
    "garras-de-leao": (garras_de_leao, "Scar: garras de leão"),
    "scar-preparo": (scar_preparo, "Scar: o rosnado sombrio (Preparo)"),
    "longa-vida-ao-rei": (longa_vida_ao_rei, "Scar: longa vida ao rei"),
    "susto": (susto, "Jack Esqueleto: o susto"),
    "fogo-de-abobora": (fogo_de_abobora, "Jack Esqueleto: fogo de abóbora"),
    "jack-esqueleto-preparo": (jack_esqueleto_preparo, "Jack Esqueleto: a noite chegando (Preparo)"),
    "noite-das-bruxas": (noite_das_bruxas, "Jack Esqueleto: noite das bruxas"),
    "roubar-a-voz": (roubar_a_voz, "Úrsula: roubar a voz"),
    "tentaculos-de-ursula": (tentaculos_de_ursula, "Úrsula: os tentáculos"),
    "ursula-preparo": (ursula_preparo, "Úrsula: o tridente zumbindo (Preparo)"),
    "tridente-da-bruxa": (tridente_da_bruxa, "Úrsula: tridente da bruxa"),
    "delaware-smash": (delaware_smash, "Deku: Delaware Smash"),
    "full-cowl-corpo": (full_cowl_corpo, "Deku: Full Cowl"),
    "deku-preparo": (deku_preparo, "Deku: o braço carregando (Preparo)"),
    "united-states-of-smash-deku": (united_states_of_smash_deku, "Deku: United States of Smash"),
    "texas-smash": (texas_smash, "All Might: Texas Smash"),
    "estou-aqui": (estou_aqui, "All Might: estou aqui!"),
    "allmight-preparo": (allmight_preparo, "All Might: o One For All (Preparo)"),
    "united-states-of-smash-allmight": (united_states_of_smash_allmight, "All Might: United States of Smash"),
}
