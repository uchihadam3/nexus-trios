"""Os sons da rodada 4 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_e.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def planeta(rng, v):
    """Surfista: a prancha cortando o espaço (o zunido metálico) e o planeta marcado (o tom cósmico)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.5, 1500, 8000, 0.6, 1.3, 0.6), 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(2400, 1200, n), n) * env(n, 0.01, 0.3) * 0.03, 0.05)
    poe(x, _acorde((196, 294, 392, 587), 1.2, 0.04, 0.05, 0.7), 0.45)
    poe(x, _sino(rng, 1568, 0.8, 0.05, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def devorador(rng, v):
    """Galactus: o planeta rachando (o ronco enorme) e os pedaços sugados para o alto (o vento que sobe)."""
    x = _z(2.2)
    n = n_de(1.8)
    poe(x, (seno(41, n) + seno(55, n) * 0.6) * sobe_e_some(n, 0.4, 1.2) * 0.12, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.06), 300, 2500, 0.02) * 0.6, 0.25 + 0.08 * k)
    m = n_de(1.3)
    poe(x, passa(rosa(rng, m), 200, 2500, 2) * sobe_e_some(m, 0.7, 1.0) * 0.4, 0.7)
    poe(x, seno(varre(150, 500, m, 1.3), m) * sobe_e_some(m, 0.7, 1.0) * 0.05, 0.7)
    return reverb(x, 0.8, 0.4)


def groot(rng, v):
    """Groot: a madeira rangendo enquanto os galhos crescem e as folhas farfalhando."""
    x = _z(1.9)
    for k in range(6):
        n = n_de(0.25)
        t = _t(n)
        poe(x, satura(seno(140 + 60 * k + 40 * np.sin(2 * math.pi * 30 * t), n), 2) * env(n, 0.02, 0.15) * 0.05, 0.05 + 0.08 * k)
        poe(x, estalo(rng, n_de(0.03), 600, 2500, 0.01) * 0.4, 0.07 + 0.08 * k)
    poe(x, _sopro(rng, 0.9, 2500, 8000, 0.15, 0.4), 0.5)
    poe(x, _acorde((220, 330, 440), 0.8, 0.03, 0.1, 0.5), 0.7)
    return reverb(x, 0.5, 0.25)


def mina(rng, v):
    """Rocket: a mina caindo (o clank), os bipes acelerando e a explosão."""
    x = _z(2.0)
    poe(x, _sino(rng, 600, 0.3, 0.1, METAL), 0.2)
    poe(x, _baque(200, 100, 0.15, 0.4), 0.2)
    t0, passo = 0.35, 0.12
    while t0 < 1.2:
        m = n_de(0.04)
        poe(x, seno(2000, m) * env(m, 0.002, 0.03) * 0.06, t0)
        t0 += passo
        passo = max(0.035, passo * 0.75)
    poe(x, _explosao(rng, 1.0, 55), 1.24)
    return reverb(x, 0.5, 0.25)


def anel_lanterna(rng, v):
    """Lanterna Verde: o anel acendendo (o zumbido de energia) e a bateria recarregando (o tom que sobe)."""
    x = _z(1.9)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(seno(110, n) + seno(220, n) * 0.5, 1.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.06, 0.0)
    m = n_de(0.7)
    poe(x, seno(varre(300, 1200, m, 1.3), m) * sobe_e_some(m, 0.95, 1.0) * 0.05, 0.4)
    poe(x, _brilho(rng, 0.6, 1760, 0.05, CRISTAL), 1.1)
    return reverb(x, 0.6, 0.3)


def hacker(rng, v):
    """Ciborgue: os dados correndo (os bipes de computador) e a varredura."""
    x = _z(1.8)
    q = np.random.default_rng(3)
    for k in range(16):
        m = n_de(0.04)
        poe(x, seno(q.choice([800, 1200, 1600, 2400]), m) * env(m, 0.002, 0.03) * 0.04, 0.03 * k)
    n = n_de(0.6)
    poe(x, seno(varre(400, 1600, n), n) * sobe_e_some(n, 0.5, 1.2) * 0.04, 0.6)
    poe(x, satura(seno(90, n), 2) * env(n, 0.02, 0.4) * 0.05, 0.6)
    return reverb(x, 0.4, 0.2)


def shazam(rng, v):
    """Shazam: o grito que vira trovão — o raio caindo e o estrondo."""
    x = _z(2.0)
    poe(x, _trovao(rng, 1.4, 1.0), 0.2)
    poe(x, graos(rng, n_de(0.5), 60, 0.0, 0.4, 3000, 11000, 0.002) * 0.5, 0.2)
    poe(x, _baque(80, 40, 0.6, 0.8, 2.5), 0.22)
    poe(x, _acorde((262, 392, 523), 0.9, 0.04, 0.02, 0.5), 0.6)
    return reverb(x, 0.6, 0.3)


def buster(rng, v):
    """Cloud: a Buster Sword descendo (o zunido pesado), o impacto e o chão rachando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.4, 200, 1500, 0.9, 1.6, 0.6), 0.0)
    poe(x, _sino(rng, 900, 0.6, 0.1, METAL), 0.4)
    poe(x, _baque(70, 30, 0.7, 1.0, 2.6), 0.4)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 400, 3000, 0.02) * 0.5, 0.5 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def combo_tifa(rng, v):
    """Tifa: os socos em sequência, cada um mais forte, e o último."""
    x = _z(1.8)
    for k in range(5):
        poe(x, _baque(150 - 15 * k, 70 - 7 * k, 0.15 + 0.03 * k, 0.3 + 0.12 * k, 2.0), 0.05 + 0.13 * k)
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * (0.3 + 0.1 * k), 0.05 + 0.13 * k)
    poe(x, _baque(80, 35, 0.6, 1.0, 2.6), 0.78)
    poe(x, _sopro(rng, 0.5, 200, 3000, 0.3, 0.1), 0.78)
    return reverb(x, 0.4, 0.2)


def asa_negra(rng, v):
    """Sephiroth: a asa abrindo (o bater pesado), o coro sombrio e as penas."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 150, 1500, 2) * sobe_e_some(n, 0.4, 1.4) * 0.6, 0.0)
    m = n_de(1.4)
    poe(x, (seno(147, m) + seno(175, m) * 0.7 + seno(208, m) * 0.5) * sobe_e_some(m, 0.4, 1.2) * 0.05, 0.2)
    poe(x, _sopro(rng, 1.0, 2500, 7000, 0.1, 0.4), 0.5)
    return reverb(x, 0.8, 0.4)


def furia_esparta(rng, v):
    """Kratos: as correntes girando, as lâminas em chamas e o grito de fúria."""
    x = _z(1.9)
    poe(x, _corrente(rng, 0.8, 12, 0.35), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 500, 4000, 0.6, 1.4, 0.4), 0.1 + 0.2 * k)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 150, 3000, 2), 1.7) * sobe_e_some(n, 0.3, 1.3) * 0.4, 0.2)
    m = n_de(0.5)
    poe(x, satura(seno(varre(180, 120, m), m) + passa(rosa(rng, m), 200, 2000, 2) * 0.6, 2.8) * env(m, 0.03, 0.3) * 0.15, 0.7)
    return reverb(x, 0.5, 0.25)


def espada_mestra(rng, v):
    """Link: a espada brilhando (o tilintar) e o feixe voando (o tom que corre)."""
    x = _z(1.8)
    poe(x, _sino(rng, 2093, 0.6, 0.06, CRISTAL), 0.0)
    n = n_de(0.45)
    poe(x, (seno(varre(1800, 900, n), n) * 0.05 + passa(rosa(rng, n), 3000, 9000, 2) * 0.1) * env(n, 0.005, 0.3), 0.55)
    for k, f in enumerate((1568, 1760, 2093, 2349)):
        poe(x, _sino(rng, f, 0.3, 0.03, CRISTAL), 0.3 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def poder_inabalavel(rng, v):
    """Ganondorf: a Triforce acendendo (o acorde pesado e escuro) e a aura roncando."""
    x = _z(2.0)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 50, 600, 2) * sobe_e_some(n, 0.4, 1.2) * 0.4, 0.0)
    poe(x, _acorde((110, 131, 165, 220), 1.4, 0.06, 0.15, 0.8), 0.15)
    poe(x, _sino(rng, 440, 0.9, 0.06, SINO), 0.3)
    poe(x, _baque(60, 30, 0.6, 0.6, 2.2), 0.9)
    return reverb(x, 0.7, 0.35)


def raio_de_gelo(rng, v):
    """Samus: o raio de gelo (o tom gelado que corre) e o gelo estalando ao crescer."""
    x = _z(1.8)
    n = n_de(0.4)
    poe(x, (seno(varre(2400, 1600, n), n) * 0.04 + passa(rosa(rng, n), 2500, 9000, 2) * 0.15) * env(n, 0.005, 0.3), 0.0)
    for k in range(8):
        poe(x, _sino(rng, 2600 + 200 * (k % 4), 0.25, 0.03, VIDRO), 0.35 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.004) * 0.3, 0.35 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def estilo(rng, v):
    """Dante: os tiros das pistolas e o "estilo" subindo (o acorde de rock)."""
    x = _z(1.8)
    for k in range(4):
        n = n_de(0.2)
        poe(x, satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.04), 2.5) * 0.6, 0.05 + 0.1 * k)
        poe(x, _baque(160, 80, 0.15, 0.3), 0.05 + 0.1 * k)
    n = n_de(0.7)
    poe(x, satura(seno(110, n) + seno(165, n) + seno(220, n) * 0.5, 3.0) * env(n, 0.01, 0.4) * 0.06, 0.55)
    poe(x, _brilho(rng, 0.6, 1568, 0.04, CRISTAL), 0.6)
    return reverb(x, 0.5, 0.25)


def concentracao(rng, v):
    """Vergil: o silêncio da concentração, os cortes invisíveis (muitos e finos) e a explosão do Julgamento."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, seno(varre(800, 1600, n), n) * sobe_e_some(n, 0.9, 1.0) * 0.02, 0.0)
    q = np.random.default_rng(5)
    for k in range(14):
        m = n_de(0.06)
        poe(x, passa(rosa(rng, m), 4000, 11000, 2) * env(m, 0.0005, 0.03) * 0.4, 0.1 + q.uniform(0, 0.45))
    poe(x, _explosao(rng, 0.8, 60), 1.1)
    poe(x, _sopro(rng, 0.7, 2000, 9000, 0.2, 0.1), 1.1)
    return reverb(x, 0.6, 0.3)


def witch_time(rng, v):
    """Bayonetta: o tique-taque que desacelera e o som do mundo esticando (o grave que cai)."""
    x = _z(2.0)
    t0, passo = 0.0, 0.08
    while t0 < 1.3:
        poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.004) * 0.6, t0)
        t0 += passo
        passo *= 1.35
    n = n_de(1.4)
    poe(x, seno(varre(600, 150, n, 0.8), n) * sobe_e_some(n, 0.3, 1.3) * 0.06, 0.3)
    poe(x, _sopro(rng, 1.4, 300, 2000, 0.25, 0.3), 0.3)
    return reverb(x, 0.8, 0.4)


def escudo_mjolnir(rng, v):
    """Master Chief: o escudo recarregando (o zumbido que sobe) e o "plim" de cheio."""
    x = _z(1.8)
    n = n_de(1.0)
    poe(x, (seno(varre(200, 900, n, 1.2), n) * 0.06 + passa(rosa(rng, n), 1500, 6000, 2) * 0.1) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _sino(rng, 1760, 0.5, 0.06, VIDRO), 1.0)
    poe(x, _sino(rng, 2637, 0.4, 0.04, VIDRO), 1.05)
    return reverb(x, 0.5, 0.25)


def armadura_doom(rng, v):
    """Doom Slayer: os fragmentos de armadura chegando (os tilintares metálicos) e o riff pesado."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _sino(rng, 1400 + 100 * k, 0.2, 0.04, METAL), 0.05 + 0.07 * k)
    n = n_de(0.9)
    poe(x, satura(seno(73, n) + seno(110, n) * 0.7 + seno(98, n) * 0.5, 4.0) * env(n, 0.005, 0.5) * 0.08, 0.55)
    poe(x, _baque(60, 30, 0.5, 0.6, 2.6), 0.55)
    return reverb(x, 0.4, 0.2)


def tranquilizante(rng, v):
    """Snake: o "!" do alerta, o disparo abafado do dardo e o sono chegando."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, (seno(880, n) + seno(1320, n) * 0.5) * env(n, 0.005, 0.2) * 0.06, 0.0)
    m = n_de(0.15)
    poe(x, passa(rosa(rng, m), 300, 3000, 2) * env(m, 0.001, 0.05) * 0.6, 0.65)
    poe(x, _whoosh(rng, 0.2, 2000, 7000, 0.6, 1.3, 0.3), 0.66)
    k = n_de(0.9)
    poe(x, seno(varre(440, 220, k), k) * sobe_e_some(k, 0.3, 1.2) * 0.04, 0.95)
    return reverb(x, 0.5, 0.25)


def zandatsu(rng, v):
    """Raiden: o Modo Lâmina (o tempo lento), os cortes em sequência e o núcleo arrancado."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, seno(varre(400, 200, n), n) * env(n, 0.02, 0.3) * 0.05, 0.0)
    for k in range(9):
        poe(x, _whoosh(rng, 0.08, 3000, 11000, 0.4, 1.4, 0.35), 0.1 + 0.08 * k)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 200, 2000, 2) * env(m, 0.005, 0.15) * 0.4, 1.0)
    poe(x, _sino(rng, 1320, 0.5, 0.05, CRISTAL), 1.05)
    return reverb(x, 0.5, 0.25)


def faca(rng, v):
    """Leon: os dois cortes de faca e o aparo (o tinido metálico)."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.4, 1.4, 0.6), 0.15)
    poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.4, 1.4, 0.6), 0.45)
    poe(x, _sino(rng, 3000, 0.5, 0.1, METAL), 0.75)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.006), 0.75)
    return reverb(x, 0.4, 0.2)


def erva(rng, v):
    """Jill: a erva esmagada (o som verde e molhado) e a cura (o acorde suave subindo)."""
    x = _z(1.8)
    for k in range(3):
        m = n_de(0.08)
        poe(x, passa(rosa(rng, m), 1000, 5000, 2) * env(m, 0.002, 0.05) * 0.4, 0.6 + 0.04 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.04, 0.1, 0.6), 0.75)
    poe(x, _brilho(rng, 0.6, 1568, 0.03, CRISTAL), 0.9)
    return reverb(x, 0.5, 0.25)


def uroboros(rng, v):
    """Wesker: os tentáculos se contorcendo (os sons molhados) e o zumbido grave do vírus."""
    x = _z(1.9)
    for k in range(8):
        n = n_de(0.2)
        poe(x, passa(rosa(rng, n), 150, 1500, 2) * env(n, 0.01, 0.1) * 0.35, 0.05 * k)
    m = n_de(1.3)
    t = _t(m)
    poe(x, satura(seno(55 + 5 * np.sin(2 * math.pi * 4 * t), m), 2.5) * sobe_e_some(m, 0.4, 1.2) * 0.12, 0.2)
    poe(x, seno(varre(800, 1200, n_de(0.3)), n_de(0.3)) * env(n_de(0.3), 0.01, 0.2) * 0.03, 0.75)
    return reverb(x, 0.5, 0.25)


def terreno(rng, v):
    """Lara: a armadilha armando (o clique), fechando (o estalo de metal) e prendendo."""
    x = _z(1.7)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.6, 0.05)
    poe(x, _sino(rng, 800, 0.4, 0.12, METAL), 0.5)
    poe(x, _baque(250, 120, 0.15, 0.6, 2.0), 0.5)
    for k in range(3):
        poe(x, _sino(rng, 1600 + 200 * k, 0.15, 0.03, METAL), 0.55 + 0.05 * k)
    return reverb(x, 0.4, 0.2)


def proximo(rng, v):
    """Ezio: a lâmina oculta saltando (o "shink") e o grito da águia."""
    x = _z(1.9)
    poe(x, _sino(rng, 3200, 0.3, 0.08, METAL), 0.0)
    poe(x, estalo(rng, n_de(0.03), 2000, 7000, 0.005) * 0.8, 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(varre(2600, 1800, n, 0.7) * (1 + 0.03 * np.sin(2 * math.pi * 25 * t)), n) * env(n, 0.02, 0.35) * 0.05, 0.4)
    poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.5, 1.4, 0.4), 1.0)
    return reverb(x, 0.7, 0.35)


def aneis(rng, v):
    """Sonic: os anéis se espalhando (o som clássico de perder os anéis: os tilintares que caem)."""
    x = _z(1.8)
    for k in range(10):
        n = n_de(0.25)
        f = 2400 - 60 * k
        poe(x, (seno(f, n) + seno(f * 1.5, n) * 0.5) * env(n, 0.002, 0.12) * 0.035, 0.05 + 0.06 * k)
    poe(x, _baque(200, 100, 0.15, 0.3), 0.0)
    return reverb(x, 0.5, 0.25)


def inibidores(rng, v):
    """Shadow: os inibidores caindo (o clink metálico), o silêncio e a energia do caos explodindo."""
    x = _z(2.0)
    for k in range(2):
        poe(x, _sino(rng, 1800 + 300 * k, 0.4, 0.06, METAL), 0.4 + 0.08 * k)
    n = n_de(0.5)
    poe(x, seno(varre(200, 800, n, 1.5), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.5)
    poe(x, _explosao(rng, 0.9, 60), 0.9)
    poe(x, _trovao(rng, 0.6, 0.3), 0.95)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-planeta": (planeta, "Surfista Prateado: a prancha e o planeta"),
    "mu-devorador": (devorador, "Galactus: o planeta devorado"),
    "mu-groot": (groot, "Groot: os galhos crescendo"),
    "mu-mina": (mina, "Rocket: a mina"),
    "mu-anel-lanterna": (anel_lanterna, "Lanterna Verde: o anel e a bateria"),
    "mu-hacker": (hacker, "Ciborgue: o hacker"),
    "mu-shazam": (shazam, "Shazam: o raio"),
    "mu-buster": (buster, "Cloud: a Buster Sword"),
    "mu-combo-tifa": (combo_tifa, "Tifa: o combo de socos"),
    "mu-asa-negra": (asa_negra, "Sephiroth: a asa negra"),
    "mu-furia-esparta": (furia_esparta, "Kratos: a fúria de Esparta"),
    "mu-espada-mestra": (espada_mestra, "Link: o feixe da Espada Mestra"),
    "mu-poder-inabalavel": (poder_inabalavel, "Ganondorf: a Triforce do Poder"),
    "mu-raio-de-gelo": (raio_de_gelo, "Samus: o raio de gelo"),
    "mu-estilo": (estilo, "Dante: o estilo"),
    "mu-concentracao": (concentracao, "Vergil: o Corte do Julgamento"),
    "mu-witch-time": (witch_time, "Bayonetta: o Witch Time"),
    "mu-escudo-mjolnir": (escudo_mjolnir, "Master Chief: o escudo recarregando"),
    "mu-armadura-doom": (armadura_doom, "Doom Slayer: a armadura"),
    "mu-tranquilizante": (tranquilizante, "Snake: o alerta e o dardo"),
    "mu-zandatsu": (zandatsu, "Raiden: o Zandatsu"),
    "mu-faca": (faca, "Leon: a faca"),
    "mu-erva": (erva, "Jill: a erva"),
    "mu-uroboros": (uroboros, "Wesker: o Uroboros"),
    "mu-terreno": (terreno, "Lara: a armadilha"),
    "mu-proximo": (proximo, "Ezio: a lâmina oculta"),
    "mu-aneis": (aneis, "Sonic: os anéis"),
    "mu-inibidores": (inibidores, "Shadow: os inibidores"),
}
