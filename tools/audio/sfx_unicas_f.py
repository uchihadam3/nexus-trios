"""Os sons da rodada 5 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_f.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _quadrada(f, n):
    return np.sign(np.sin(2 * math.pi * np.cumsum(np.full(n, f) if np.isscalar(f) else f) / 44100))


def premio(rng, v):
    """Mega Man: o teletransporte (o "biu" que desce) e a arma adquirida (o arpejo de 8 bits)."""
    x = _z(1.8)
    n = n_de(0.3)
    poe(x, _quadrada(varre(1600, 400, n), n) * env(n, 0.005, 0.25) * 0.03, 0.0)
    for k, f in enumerate((523, 659, 784, 1047, 784, 1047, 1319)):
        m = n_de(0.09 if k < 6 else 0.4)
        poe(x, _quadrada(f, m) * env(m, 0.002, 0.07 if k < 6 else 0.3) * 0.03, 0.45 + 0.08 * k)
    return reverb(x, 0.3, 0.15)


def raikousen(rng, v):
    """Zero: o sabre (o zumbido que corta) e o raio correndo pelo chão."""
    x = _z(1.8)
    n = n_de(0.35)
    poe(x, (satura(seno(varre(180, 120, n), n), 2) * 0.1 + passa(rosa(rng, n), 1500, 7000, 2) * 0.3) * env(n, 0.005, 0.25), 0.0)
    poe(x, _whoosh(rng, 0.25, 1500, 9000, 0.5, 1.3, 0.5), 0.0)
    poe(x, _trovao(rng, 0.8, 0.6), 0.3)
    poe(x, graos(rng, n_de(0.6), 50, 0.0, 0.8, 3000, 11000, 0.002) * 0.4, 0.3)
    return reverb(x, 0.5, 0.25)


def cogumelo(rng, v):
    """Mario: o cogumelo saindo (o tom que sobe) e o crescer (as três notas que sobem e piscam)."""
    x = _z(1.9)
    n = n_de(0.4)
    poe(x, _quadrada(varre(300, 900, n), n) * env(n, 0.005, 0.3) * 0.025, 0.0)
    for k, f in enumerate((392, 523, 392, 523, 659, 523, 659, 784)):
        m = n_de(0.08)
        poe(x, _quadrada(f, m) * env(m, 0.002, 0.06) * 0.03, 0.6 + 0.065 * k)
    return reverb(x, 0.3, 0.15)


def furia_bowser(rng, v):
    """Bowser: o rugido do rei e o fogo saindo da boca."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(seno(varre(110, 70, n) * (1 + 0.05 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 100, 1500, 2) * 0.8, 3.0) * env(n, 0.03, 0.45) * 0.2, 0.0)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 150, 4000, 2), 1.8) * sobe_e_some(m, 0.25, 1.3) * 0.55, 0.65)
    return reverb(x, 0.5, 0.25)


def hadouken(rng, v):
    """Ryu: a energia juntando nas mãos (o sopro que gira e sobe) e o brilho."""
    x = _z(1.9)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 3500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * (4 + 8 * t) * t)) * sobe_e_some(n, 0.9, 1.0) * 0.4, 0.0)
    poe(x, seno(varre(150, 450, n, 1.3), n) * sobe_e_some(n, 0.9, 1.0) * 0.08, 0.0)
    poe(x, _baque(140, 70, 0.4, 0.5), 1.1)
    poe(x, _brilho(rng, 0.6, 1320, 0.04, CRISTAL), 1.12)
    return reverb(x, 0.5, 0.25)


def spinning_bird(rng, v):
    """Chun-Li: as pernas girando (o vento que roda rápido) e os chutes."""
    x = _z(1.8)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t) ** 2) * sobe_e_some(n, 0.3, 1.3) * 0.45, 0.0)
    for k in range(5):
        poe(x, _baque(170, 90, 0.12, 0.3), 0.15 + 0.18 * k)
    return reverb(x, 0.5, 0.25)


def messatsu(rng, v):
    """Akuma: o símbolo do Céu (o gongo grave) e a aura escura roncando."""
    x = _z(2.1)
    n = n_de(1.6)
    poe(x, passa(rosa(rng, n), 50, 500, 2) * sobe_e_some(n, 0.3, 1.2) * 0.45, 0.0)
    poe(x, _sino(rng, 110, 1.6, 0.18, SINO), 0.2)
    for k in range(4):
        poe(x, _whoosh(rng, 0.15, 800, 5000, 0.4, 1.4, 0.35), 0.15 + 0.1 * k)
    return reverb(x, 0.8, 0.4)


def venha_ca(rng, v):
    """Scorpion: a lança voando na corda, cravando, o "Venha cá!" (o grito grave) e o puxão."""
    x = _z(1.9)
    poe(x, _corrente(rng, 0.5, 8, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.25, 800, 6000, 0.6, 1.3, 0.5), 0.05)
    poe(x, _sino(rng, 2000, 0.3, 0.07, METAL), 0.3)
    m = n_de(0.4)
    poe(x, satura(seno(varre(200, 140, m), m) + passa(rosa(rng, m), 200, 2000, 2) * 0.5, 2.8) * env(m, 0.02, 0.25) * 0.14, 0.45)
    poe(x, _corrente(rng, 0.4, 8, 0.4), 0.85)
    poe(x, satura(passa(rosa(rng, n_de(0.6)), 150, 3000, 2), 1.6) * sobe_e_some(n_de(0.6), 0.2, 1.3) * 0.3, 0.6)
    return reverb(x, 0.5, 0.25)


def fatality(rng, v):
    """Sub-Zero: o gelo crescendo (os estalos frios), o silêncio e o bloco partindo em pedaços."""
    x = _z(2.0)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.04), 2000, 9000, 0.008) * 0.35, 0.04 * k)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.2, 0.0)
    poe(x, _baque(150, 70, 0.4, 0.6, 2.0), 1.05)
    for k in range(10):
        poe(x, _sino(rng, 2400 + 300 * (k % 5), 0.3, 0.03, VIDRO), 1.05 + 0.025 * k)
    return reverb(x, 0.6, 0.3)


def mortal_kombat(rng, v):
    """Liu Kang: o dragão de fogo subindo (o rugido e as chamas)."""
    x = _z(2.0)
    n = n_de(1.3)
    poe(x, satura(passa(rosa(rng, n), 150, 4000, 2), 1.8) * sobe_e_some(n, 0.6, 1.1) * 0.5, 0.0)
    m = n_de(0.6)
    t = _t(m)
    poe(x, satura(seno(varre(160, 280, m) * (1 + 0.06 * np.sin(2 * math.pi * 20 * t)), m) + passa(rosa(rng, m), 300, 2500, 2) * 0.6, 2.8) * env(m, 0.04, 0.35) * 0.14, 0.75)
    return reverb(x, 0.6, 0.3)


def pele_trovao(rng, v):
    """Raiden: a pele estalando de eletricidade e o trovão."""
    x = _z(1.9)
    poe(x, graos(rng, n_de(1.2), 120, 0.0, 0.9, 2500, 11000, 0.002) * 0.45, 0.0)
    n = n_de(1.2)
    poe(x, satura(seno(60, n) + seno(120, n) * 0.5, 2) * sobe_e_some(n, 0.4, 1.2) * 0.06, 0.0)
    poe(x, _trovao(rng, 1.1, 0.8), 0.35)
    return reverb(x, 0.6, 0.3)


def devil_jin(rng, v):
    """Jin: as asas abrindo (o bater pesado), o rosnado do Devil e o laser da testa."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 150, 1500, 2) * sobe_e_some(n, 0.4, 1.4) * 0.6, 0.0)
    m = n_de(0.6)
    poe(x, satura(seno(varre(90, 70, m), m) + passa(rosa(rng, m), 100, 900, 2) * 0.7, 3) * env(m, 0.05, 0.35) * 0.15, 0.2)
    k = n_de(0.6)
    poe(x, (satura(seno(varre(900, 700, k), k), 2) * 0.06 + passa(rosa(rng, k), 2000, 8000, 2) * 0.2) * env(k, 0.005, 0.4), 0.9)
    return reverb(x, 0.6, 0.3)


def chute(rng, v):
    """Kazuya: o chute que corta o ar, o impacto e o estalo roxo do gene Devil."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.3, 300, 4000, 0.7, 1.4, 0.7), 0.05)
    poe(x, _baque(110, 45, 0.5, 0.9, 2.6), 0.65)
    poe(x, graos(rng, n_de(0.7), 50, 0.0, 0.8, 2500, 10000, 0.002) * 0.4, 0.66)
    poe(x, _trovao(rng, 0.5, 0.3), 0.7)
    return reverb(x, 0.5, 0.25)


def fusao(rng, v):
    """Sora: a Keyblade girando (o tilintar mágico) e a fusão (as duas notas que se juntam num acorde)."""
    x = _z(1.9)
    n = n_de(0.7)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.3, 0.0)
    m = n_de(0.6)
    poe(x, seno(varre(392, 523, m), m) * env(m, 0.02, 0.4) * 0.04 + seno(varre(659, 523, m), m) * env(m, 0.02, 0.4) * 0.04, 0.5)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.05, 0.01, 0.6), 1.1)
    poe(x, _brilho(rng, 0.6, 2093, 0.04, CRISTAL), 1.12)
    return reverb(x, 0.6, 0.3)


def postura(rng, v):
    """Sekiro: o aço batendo (a postura enchendo), a quebra e o sinal do golpe mortal."""
    x = _z(1.9)
    for k in range(4):
        poe(x, _sino(rng, 1800 + 120 * k, 0.4, 0.07, METAL), 0.05 + 0.18 * k)
    poe(x, _baque(140, 60, 0.4, 0.7, 2.4), 0.8)
    poe(x, estalo(rng, n_de(0.05), 800, 5000, 0.015), 0.8)
    n = n_de(0.9)
    poe(x, (seno(98, n) + seno(104, n)) * env(n, 0.01, 0.6) * 0.1, 1.0)
    return reverb(x, 0.6, 0.3)


def florescer(rng, v):
    """Malenia: a flor desabrochando (o rangido orgânico e o coro) e os esporos se espalhando."""
    x = _z(2.1)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * sobe_e_some(n, 0.7, 1.1) * 0.35, 0.0)
    m = n_de(1.4)
    poe(x, (seno(220, m) + seno(233, m) * 0.7 + seno(330, m) * 0.5) * sobe_e_some(m, 0.5, 1.2) * 0.045, 0.3)
    poe(x, graos(rng, n_de(1.1), 90, 0.0, 0.9, 1500, 7000, 0.004) * 0.3, 0.8)
    poe(x, _sopro(rng, 1.0, 1500, 6000, 0.2, 0.2), 0.8)
    return reverb(x, 0.7, 0.35)


def alvo(rng, v):
    """Agente 47: a mira ajustando (os bipes discretos) e o código lido."""
    x = _z(1.7)
    for k in range(4):
        m = n_de(0.05)
        poe(x, seno(1800, m) * env(m, 0.002, 0.04) * 0.04, 0.05 + 0.12 * k)
    m = n_de(0.25)
    poe(x, seno(varre(1200, 2400, m), m) * env(m, 0.005, 0.2) * 0.04, 0.85)
    poe(x, passa(rosa(rng, m), 2000, 6000, 2) * env(m, 0.005, 0.2) * 0.15, 0.85)
    return reverb(x, 0.3, 0.15)


def gelida(rng, v):
    """Arthas: a Gélida ressoando (o gelo e o metal), as almas gemendo e sendo puxadas."""
    x = _z(2.1)
    poe(x, _sino(rng, 660, 1.4, 0.1, METAL), 0.0)
    poe(x, _sino(rng, 1980, 1.0, 0.04, VIDRO), 0.05)
    for k in range(4):
        n = n_de(0.6)
        t = _t(n)
        poe(x, seno(varre(500 + 60 * k, 300 + 60 * k, n) * (1 + 0.02 * np.sin(2 * math.pi * 5 * t)), n) * sobe_e_some(n, 0.4, 1.2) * 0.025, 0.5 + 0.12 * k)
    poe(x, _sopro(rng, 1.0, 400, 3000, 0.25, 0.6), 0.6)
    return reverb(x, 0.8, 0.4)


def mutacoes(rng, v):
    """Geralt: o medalhão vibrando (o zumbido metálico) e o sinal Quen (o escudo que liga)."""
    x = _z(1.8)
    n = n_de(0.7)
    t = _t(n)
    poe(x, modal_vibra(rng, n, t), 0.0)
    poe(x, _baque(200, 100, 0.2, 0.3), 0.85)
    poe(x, _acorde((294, 440, 587), 0.8, 0.04, 0.01, 0.5), 0.85)
    poe(x, _sopro(rng, 0.6, 600, 4000, 0.2, 0.15), 0.85)
    return reverb(x, 0.5, 0.25)


def modal_vibra(rng, n, t):
    return _sino(rng, 1200, n / 44100, 0.08, METAL)[:n] * (0.5 + 0.5 * np.sin(2 * math.pi * 28 * t))


def corte_lento(rng, v):
    """Isaac: o cortador ligando (o zumbido de plasma), o disparo e o corte."""
    x = _z(1.8)
    n = n_de(0.8)
    poe(x, (satura(seno(220, n), 2) * 0.05 + passa(rosa(rng, n), 2000, 7000, 2) * 0.1) * sobe_e_some(n, 0.7, 1.2), 0.0)
    m = n_de(0.3)
    poe(x, (seno(varre(1600, 400, m), m) * 0.06 + passa(rosa(rng, m), 1000, 8000, 2) * 0.3) * env(m, 0.002, 0.15), 0.85)
    poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.3, 1.3, 0.4), 0.88)
    return reverb(x, 0.4, 0.2)


def hev(rng, v):
    """Gordon: o traje HEV (os bipes) e a morfina aplicada (o tom de alívio)."""
    x = _z(1.9)
    for k in range(3):
        m = n_de(0.1)
        poe(x, seno(1047, m) * env(m, 0.005, 0.08) * 0.05, 0.05 + 0.13 * k)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * env(n, 0.002, 0.1) * 0.4, 0.6)
    poe(x, _acorde((392, 494, 587), 0.9, 0.04, 0.05, 0.6), 0.75)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "mu-premio": (premio, "Mega Man: arma adquirida"),
    "mu-raikousen": (raikousen, "Zero: o Raikousen"),
    "mu-cogumelo": (cogumelo, "Mario: o Super Cogumelo"),
    "mu-furia-bowser": (furia_bowser, "Bowser: o rugido e o fogo"),
    "mu-hadouken": (hadouken, "Ryu: o Hadouken carregando"),
    "mu-spinning-bird": (spinning_bird, "Chun-Li: o Spinning Bird Kick"),
    "mu-messatsu": (messatsu, "Akuma: o Messatsu"),
    "mu-venha-ca": (venha_ca, "Scorpion: Venha cá!"),
    "mu-fatality": (fatality, "Sub-Zero: o Fatality congelante"),
    "mu-mortal-kombat": (mortal_kombat, "Liu Kang: o dragão de fogo"),
    "mu-pele-trovao": (pele_trovao, "Raiden: a pele de trovão"),
    "mu-devil-jin": (devil_jin, "Jin: o Devil"),
    "mu-chute": (chute, "Kazuya: o chute"),
    "mu-fusao": (fusao, "Sora: a Forma de fusão"),
    "mu-postura": (postura, "Sekiro: a postura quebrada"),
    "mu-florescer": (florescer, "Malenia: o Florescer escarlate"),
    "mu-alvo": (alvo, "Agente 47: o alvo"),
    "mu-gelida": (gelida, "Arthas: a Gélida"),
    "mu-mutacoes": (mutacoes, "Geralt: o medalhão e o Quen"),
    "mu-corte-lento": (corte_lento, "Isaac: o cortador de plasma"),
    "mu-hev": (hev, "Gordon: o traje HEV"),
}
