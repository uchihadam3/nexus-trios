"""Os sons da rodada 15 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_p.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def energia_natural(rng, v):
    """Jiraiya: a natureza entrando (o vento calmo e o sapo) e o poder do sábio (o acorde grave)."""
    x = _z(2.2)
    poe(x, _sopro(rng, 1.0, 300, 2500, 0.3, 0.6), 0.0)
    for k in range(2):
        n = n_de(0.15)
        poe(x, satura(seno(varre(180, 120, n), n), 2) * env(n, 0.01, 0.12) * 0.07, 0.25 + 0.2 * k)
    poe(x, _acorde((110, 165, 220, 277), 1.2, 0.05, 0.1, 0.8), 0.6)
    poe(x, _sino(rng, 440, 0.8, 0.05, SINO), 0.6)
    return reverb(x, 0.7, 0.35)


def byakugo(rng, v):
    """Tsunade: o selo se abrindo (o tom que sobe) e a cura enorme (o coro claro)."""
    x = _z(2.2)
    n = n_de(0.5)
    poe(x, seno(varre(300, 1200, n), n) * sobe_e_some(n, 0.8, 1.2) * 0.04, 0.0)
    poe(x, _sino(rng, 1047, 0.6, 0.06, CRISTAL), 0.3)
    poe(x, _acorde((392, 494, 587, 784), 1.4, 0.05, 0.1, 0.9), 0.35)
    poe(x, _brilho(rng, 1.0, 1568, 0.04, CRISTAL), 0.4)
    return reverb(x, 0.8, 0.4)


def fogo_sagrado(rng, v):
    """Sailor Mars: o selo de fogo (o sino) e as chamas subindo em círculo."""
    x = _z(2.1)
    poe(x, _sino(rng, 660, 0.7, 0.07, SINO), 0.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 200, 3500, 2), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.3, 1.3) * 0.3, 0.15)
    poe(x, _whoosh(rng, 0.4, 400, 3000, 0.7, 1.4, 0.4), 0.25)
    return reverb(x, 0.6, 0.3)


def escudo_rosa(rng, v):
    """Steven: a bolha rosa abrindo (o "plop" e o brilho) e o acorde doce."""
    x = _z(2.0)
    poe(x, _piu(300, 900, 0.12, 0.06), 0.05)
    poe(x, _sino(rng, 1320, 0.6, 0.05, CRISTAL), 0.12)
    poe(x, _acorde((523, 659, 784, 988), 1.0, 0.04, 0.05, 0.7), 0.2)
    return reverb(x, 0.7, 0.35)


def futuro(rng, v):
    """Garnet: a visão (os tons que se dividem em caminhos) e as joias brilhando."""
    x = _z(2.1)
    for k, f in enumerate((440, 554, 659, 831, 988)):
        n = n_de(0.8)
        poe(x, seno(varre(440, f, n), n) * env(n, 0.05, 0.6) * 0.025, 0.1)
    poe(x, _sino(rng, 1760, 0.5, 0.05, CRISTAL), 0.55)
    poe(x, _sino(rng, 2217, 0.5, 0.04, CRISTAL), 0.65)
    return reverb(x, 0.8, 0.4)


def cantada(rng, v):
    """Johnny Bravo: o "Hah!" (o tom grave e confiante), o brilho do topete e os coraçõezinhos."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, satura(seno(varre(160, 130, n), n), 2.5) * env(n, 0.01, 0.15) * 0.08, 0.0)
    poe(x, _brilho(rng, 0.5, 3136, 0.05, CRISTAL), 0.18)
    for k in range(4):
        poe(x, _piu(700 + 120 * k, 1000 + 120 * k, 0.08, 0.04), 0.4 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def dee_dee(rng, v):
    """Dexter: as máquinas do laboratório (as engrenagens e os bipes) e o "funcionou" (o estouro)."""
    x = _z(2.1)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.02), 1200, 4000, 0.004) * 0.4, 0.04 * k)
    for k in range(4):
        poe(x, _quadrada(800 + 200 * (k % 2), n_de(0.07)) * env(n_de(0.07), 0.003, 0.05) * 0.02, 0.15 + 0.08 * k)
    poe(x, _baque(200, 90, 0.2, 0.4), 0.55)
    poe(x, passa(rosa(rng, n_de(0.3)), 500, 6000, 2) * env(n_de(0.3), 0.002, 0.2) * 0.4, 0.55)
    return reverb(x, 0.5, 0.25)


def jogado_ao_futuro(rng, v):
    """Aku: o portal do tempo girando (o zumbido que roda) e o riso grave."""
    x = _z(2.3)
    n = n_de(1.3)
    t = _t(n)
    poe(x, (satura(seno(80 + 40 * np.sin(2 * math.pi * 3 * t), n), 2) * 0.08 + passa(rosa(rng, n), 300, 2000, 2) * 0.2) * sobe_e_some(n, 0.4, 1.2), 0.0)
    poe(x, seno(varre(600, 150, n_de(0.5), 0.6), n_de(0.5)) * env(n_de(0.5), 0.01, 0.4) * 0.04, 0.4)
    for k in range(3):
        m = n_de(0.2)
        poe(x, satura(seno(varre(100, 85, m), m), 2.5) * env(m, 0.01, 0.15) * 0.08, 0.95 + 0.17 * k)
    return reverb(x, 0.8, 0.4)


def armadura_aprende(rng, v):
    """Vilgax: as placas da armadura se fechando, uma a uma (os baques de metal)."""
    x = _z(2.0)
    for k in range(6):
        poe(x, _baque(160, 90, 0.12, 0.3), 0.1 + 0.08 * k)
        poe(x, _sino(rng, 700 + 60 * k, 0.25, 0.03, METAL), 0.1 + 0.08 * k)
    n = n_de(0.6)
    poe(x, seno(varre(200, 400, n), n) * env(n, 0.05, 0.4) * 0.04, 0.6)
    return reverb(x, 0.5, 0.25)


def desejo_realizado(rng, v):
    """Cosmo e Wanda: o "plim" das varinhas e as estrelinhas caindo."""
    x = _z(2.1)
    poe(x, _sino(rng, 1568, 0.5, 0.06, CRISTAL), 0.2)
    poe(x, _sino(rng, 2093, 0.5, 0.06, CRISTAL), 0.25)
    poe(x, _brilho(rng, 1.0, 2637, 0.05, CRISTAL), 0.3)
    for k in range(6):
        poe(x, _sino(rng, 3000 - 200 * k, 0.2, 0.025, CRISTAL), 0.45 + 0.07 * k)
    return reverb(x, 0.7, 0.35)


def crafting(rng, v):
    """Steve: as batidas na mesa de trabalho e o item novo saindo (o "pop")."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _baque(220, 140, 0.1, 0.3), 0.08 + 0.12 * k)
        poe(x, passa(rosa(rng, n_de(0.06)), 400, 2500, 2) * env(n_de(0.06), 0.002, 0.04) * 0.3, 0.08 + 0.12 * k)
    poe(x, _piu(400, 900, 0.08, 0.06), 0.5)
    poe(x, _sino(rng, 1760, 0.4, 0.04, CRISTAL), 0.55)
    return reverb(x, 0.4, 0.2)


def creeper_boom(rng, v):
    """Creeper: o chiado "tssss" e a explosão."""
    x = _z(2.0)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.9, 0.8) * 0.4, 0.0)
    poe(x, _explosao(rng, 1.2, 0.95), 0.42)
    poe(x, _baque(70, 30, 0.6, 0.9, 3.0), 0.42)
    return reverb(x, 0.5, 0.25)


def waka(rng, v):
    """Pac-Man: o "waka waka" (o tom que vai e volta) e a pílula grande."""
    x = _z(2.0)
    for k in range(6):
        n = n_de(0.1)
        f0, f1 = (300, 600) if k % 2 == 0 else (600, 300)
        poe(x, seno(varre(f0, f1, n), n) * env(n, 0.005, 0.08) * 0.05, 0.05 + 0.12 * k)
    m = n_de(0.5)
    poe(x, seno(varre(400, 1200, m), m) * env(m, 0.01, 0.4) * 0.04, 0.8)
    return reverb(x, 0.4, 0.2)


def aku_aku(rng, v):
    """Crash: a máscara chegando (o sussurro e o tambor tribal) e o brilho."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 500, 4000, 0.7, 1.4, 0.4), 0.0)
    for k in range(4):
        poe(x, _baque(140 - 15 * (k % 2), 80, 0.15, 0.4), 0.25 + 0.1 * k)
    poe(x, _brilho(rng, 0.8, 1760, 0.05, CRISTAL), 0.55)
    poe(x, _acorde((330, 415, 494), 0.7, 0.04, 0.05, 0.5), 0.6)
    return reverb(x, 0.6, 0.3)


def dead_eye(rng, v):
    """Arthur Morgan: o tempo desacelerando (o batimento grave), as marcas e os três tiros."""
    x = _z(2.0)
    for k in range(2):
        poe(x, _baque(60, 40, 0.25, 0.6, 1.6), 0.0 + 0.25 * k)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 2000, 6000, 0.004) * 0.4, 0.1 + 0.08 * k)
    for k in range(3):
        n = n_de(0.25)
        poe(x, satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.06), 2.5) * 0.7, 0.5 + 0.1 * k)
        poe(x, _baque(150, 70, 0.2, 0.3), 0.5 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def suprimentos(rng, v):
    """Ellie: o zíper da mochila, os itens pegos e o curativo."""
    x = _z(1.9)
    n = n_de(0.3)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 40 * t))) * env(n, 0.01, 0.25) * 0.25, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 800, 3500, 0.008) * 0.5, 0.35 + 0.08 * k)
    poe(x, _acorde((523, 659, 784), 0.6, 0.035, 0.03, 0.4), 0.7)
    return reverb(x, 0.4, 0.2)


def desviou_sans(rng, v):
    """Sans: o olho azul acendendo (o tom elétrico) e o osso passando direto."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(880 * (1 + 0.02 * np.sin(2 * math.pi * 12 * t)), n) * env(n, 0.01, 0.6) * 0.03, 0.0)
    poe(x, _quadrada(220, n_de(0.08)) * env(n_de(0.08), 0.003, 0.06) * 0.03, 0.02)
    poe(x, _whoosh(rng, 0.25, 1000, 6000, 0.6, 1.4, 0.4), 0.2)
    poe(x, _piu(600, 300, 0.12, 0.04), 0.55)
    return reverb(x, 0.5, 0.25)


def super_carta(rng, v):
    """Cuphead: as cartas enchendo (o tom de desenho antigo) e o parry (o estalo e o "plim")."""
    x = _z(2.0)
    for k, f in enumerate((523, 587, 659, 698, 784)):
        poe(x, _quadrada(f, n_de(0.08)) * env(n_de(0.08), 0.003, 0.06) * 0.02, 0.05 + 0.06 * k)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.006), 0.4)
    poe(x, _sino(rng, 1568, 0.5, 0.06, SINO), 0.4)
    poe(x, _acorde((392, 494, 587, 784), 0.6, 0.035, 0.01, 0.4), 0.45)
    return reverb(x, 0.5, 0.25)


def fus_ro_dah(rng, v):
    """Dovahkiin: o grito em três partes (Fus, Ro, Dah) e a onda de força."""
    x = _z(2.2)
    for k, f in enumerate((150, 130, 110)):
        n = n_de(0.18 if k < 2 else 0.35)
        poe(x, satura(seno(varre(f, f * 0.85, n), n) + passa(rosa(rng, n), 200, 2000, 2) * 0.6, 3) * env(n, 0.01, 0.15 if k < 2 else 0.3) * 0.08, 0.05 + 0.15 * k)
    poe(x, _whoosh(rng, 0.6, 150, 2000, 0.9, 1.3, 0.6), 0.35)
    poe(x, _baque(70, 30, 0.5, 0.8, 2.6), 0.4)
    return reverb(x, 0.8, 0.4)


def foco_alma(rng, v):
    """O Cavaleiro: a alma juntando (o tom que sobe) e a cura (o "plim" seco)."""
    x = _z(2.0)
    n = n_de(0.55)
    poe(x, (seno(varre(200, 800, n), n) * 0.05 + passa(rosa(rng, n), 1500, 6000, 2) * 0.1) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _sino(rng, 1320, 0.6, 0.06, VIDRO), 0.55)
    poe(x, _baque(200, 120, 0.15, 0.3), 0.55)
    return reverb(x, 0.7, 0.35)


def quatro_bracos(rng, v):
    """Goro: os quatro socos e o rugido."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.12, 400, 3000, 0.6, 1.4, 0.3), 0.05 + 0.1 * k)
        poe(x, _baque(110, 50, 0.25, 0.6, 2.4), 0.17 + 0.1 * k)
    n = n_de(0.7)
    poe(x, satura(seno(varre(110, 75, n), n) + passa(rosa(rng, n), 150, 1500, 2) * 0.7, 3) * env(n, 0.04, 0.5) * 0.09, 0.6)
    return reverb(x, 0.5, 0.25)


def ovo_yoshi(rng, v):
    """Yoshi: a língua (o "slurp"), o engolir e o ovo saindo (o "pop")."""
    x = _z(1.9)
    n = n_de(0.25)
    poe(x, seno(varre(400, 1600, n), n) * env(n, 0.005, 0.2) * 0.05, 0.0)
    m = n_de(0.2)
    poe(x, seno(varre(1600, 200, m), m) * env(m, 0.005, 0.18) * 0.05, 0.25)
    poe(x, _baque(180, 90, 0.15, 0.3), 0.42)
    poe(x, _piu(500, 1100, 0.08, 0.06), 0.5)
    poe(x, _sino(rng, 1047, 0.4, 0.04, SINO), 0.55)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "mu-energia-natural": (energia_natural, "Jiraiya: a energia natural"),
    "mu-byakugo": (byakugo, "Tsunade: o Byakugō"),
    "mu-fogo-sagrado": (fogo_sagrado, "Sailor Mars: o fogo sagrado"),
    "mu-escudo-rosa": (escudo_rosa, "Steven: o escudo rosa"),
    "mu-previsao": (futuro, "Garnet: a visão do futuro"),
    "mu-cantada": (cantada, "Johnny Bravo: a cantada"),
    "mu-dee-dee": (dee_dee, "Dexter: o laboratório"),
    "mu-jogado-ao-futuro": (jogado_ao_futuro, "Aku: o portal do tempo"),
    "mu-armadura-aprende": (armadura_aprende, "Vilgax: a armadura"),
    "mu-desejo-realizado": (desejo_realizado, "Cosmo e Wanda: o desejo"),
    "mu-crafting": (crafting, "Steve: crafting"),
    "mu-creeper-boom": (creeper_boom, "Creeper: BOOM"),
    "mu-waka": (waka, "Pac-Man: waka waka"),
    "mu-aku-aku": (aku_aku, "Crash: Aku Aku"),
    "mu-dead-eye": (dead_eye, "Arthur Morgan: Dead Eye"),
    "mu-suprimentos": (suprimentos, "Ellie: os suprimentos"),
    "mu-desviou-sans": (desviou_sans, "Sans: desviou"),
    "mu-super-carta": (super_carta, "Cuphead: Super"),
    "mu-fus-ro-dah": (fus_ro_dah, "Dovahkiin: Fus Ro Dah"),
    "mu-foco-alma": (foco_alma, "O Cavaleiro: o foco"),
    "mu-quatro-bracos": (quatro_bracos, "Goro: os quatro braços"),
    "mu-ovo-yoshi": (ovo_yoshi, "Yoshi: o ovo"),
}
