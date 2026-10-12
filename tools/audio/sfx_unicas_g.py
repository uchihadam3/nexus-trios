"""Os sons da rodada 6 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_g.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def primeiro(rng, v):
    """Hayabusa: as shurikens zunindo e o corte da espada."""
    x = _z(1.8)
    for k in range(4):
        n = n_de(0.3)
        t = _t(n)
        poe(x, passa(rosa(rng, n), 2500, 9000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * t) ** 2) * env(n, 0.005, 0.2) * 0.35, 0.03 + 0.05 * k)
    poe(x, _whoosh(rng, 0.2, 2000, 11000, 0.4, 1.4, 0.8), 0.55)
    poe(x, _sino(rng, 3000, 0.5, 0.07, METAL), 0.62)
    return reverb(x, 0.4, 0.2)


def punicao(rng, v):
    """Cabeça de Pirâmide: a sirene distante, a faca arrastando no chão e o golpe pesado."""
    x = _z(2.2)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(400 + 150 * np.sin(2 * math.pi * 0.8 * t), n) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 300, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 17 * _t(m))) * sobe_e_some(m, 0.5, 1.3) * 0.35, 0.4)
    poe(x, _baque(60, 25, 0.8, 1.0, 2.8), 1.05)
    poe(x, _sino(rng, 420, 0.8, 0.1, METAL), 1.05)
    return reverb(x, 0.7, 0.35)


def inalar(rng, v):
    """Kirby: a sucção (o vento puxando, cada vez mais forte) e o "pop" de engolir."""
    x = _z(1.9)
    n = n_de(1.3)
    poe(x, (passa(rosa(rng, n), 300, 4000, 2) * 0.4 + seno(varre(200, 500, n), n) * 0.04) * sobe_e_some(n, 0.85, 1.0), 0.0)
    m = n_de(0.15)
    poe(x, seno(varre(300, 900, m), m) * env(m, 0.005, 0.1) * 0.08, 1.3)
    poe(x, _brilho(rng, 0.4, 1760, 0.04, CRISTAL), 1.35)
    return reverb(x, 0.4, 0.2)


def banana(rng, v):
    """Donkey Kong: a casca voando (o fiu), o escorregão (o tom que despenca) e o tombo."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.4, 800, 3000, 0.6, 1.3, 0.35), 0.0)
    poe(x, _baque(300, 150, 0.1, 0.25), 0.75)
    n = n_de(0.4)
    poe(x, seno(varre(900, 200, n), n) * env(n, 0.005, 0.3) * 0.06, 0.8)
    poe(x, _baque(110, 50, 0.4, 0.7, 2.0), 1.2)
    for k in range(3):
        poe(x, _sino(rng, 1800 + 300 * k, 0.3, 0.025, CRISTAL), 1.25 + 0.08 * k)
    return reverb(x, 0.4, 0.2)


def vampire_killer(rng, v):
    """Simon: o chicote estalando e a cruz sagrada (o sino e o coro)."""
    x = _z(2.0)
    poe(x, _corrente(rng, 0.45, 10, 0.3), 0.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.008) * 1.2, 0.45)
    poe(x, _sino(rng, 784, 1.2, 0.1, SINO), 0.85)
    poe(x, _acorde((392, 494, 587, 784), 1.1, 0.04, 0.15, 0.6), 0.85)
    return reverb(x, 0.8, 0.4)


def areias(rng, v):
    """Príncipe da Pérsia: a areia escorrendo (o chiado fino) e o tempo desacelerando (o tom que cai)."""
    x = _z(2.0)
    n = n_de(1.6)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.4, 1.2) * 0.2, 0.0)
    poe(x, graos(rng, n, 120, 0.0, 0.9, 4000, 11000, 0.002) * 0.2, 0.0)
    m = n_de(1.2)
    poe(x, seno(varre(700, 200, m, 0.7), m) * sobe_e_some(m, 0.3, 1.2) * 0.05, 0.3)
    poe(x, _sino(rng, 1320, 0.8, 0.04, SINO), 0.2)
    return reverb(x, 0.8, 0.4)


def pegaso(rng, v):
    """Seiya: as estrelas acendendo (os tilintares), a constelação e os Meteoros de Pégaso (muitos golpes rápidos)."""
    x = _z(2.0)
    for k, f in enumerate((1568, 1760, 2093, 2349, 2637, 2093, 2349, 2794, 3136)):
        poe(x, _sino(rng, f, 0.3, 0.025, CRISTAL), 0.03 * k)
    for k in range(12):
        poe(x, _baque(200, 120, 0.06, 0.15, 1.5), 1.0 + 0.04 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.005) * 0.25, 1.0 + 0.04 * k)
    return reverb(x, 0.6, 0.3)


def absorcao(rng, v):
    """Majin Boo: a gosma esticando e engolindo, e o vapor saindo dos furos (o apito)."""
    x = _z(2.0)
    for k in range(5):
        n = n_de(0.3)
        poe(x, (passa(rosa(rng, n), 150, 1200, 2) * 0.4 + seno(varre(250, 120, n), n) * 0.06) * env(n, 0.02, 0.2), 0.05 + 0.15 * k)
    m = n_de(0.8)
    poe(x, (passa(rosa(rng, m), 3000, 9000, 2) * 0.25 + seno(2200, m) * 0.02) * sobe_e_some(m, 0.3, 1.3), 1.0)
    return reverb(x, 0.4, 0.2)


def kuririn_nao(rng, v):
    """Kuririn: os seis pontos brilhando, o silêncio e o grito de fúria dourada (a explosão de aura)."""
    x = _z(2.2)
    for k in range(6):
        poe(x, _sino(rng, 1320 + 80 * k, 0.3, 0.025, CRISTAL), 0.03 * k)
    poe(x, _explosao(rng, 1.0, 55), 0.75)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * env(n, 0.01, 0.6) * 0.4, 0.77)
    poe(x, _trovao(rng, 0.8, 0.4), 0.85)
    poe(x, _acorde((262, 330, 392), 1.0, 0.04, 0.05, 0.6), 0.9)
    return reverb(x, 0.6, 0.3)


def escudo_dragao(rng, v):
    """Shiryu: o escudo aparecendo (o metal largo), o golpe batendo e voltando (o clang)."""
    x = _z(1.9)
    poe(x, _sino(rng, 500, 0.8, 0.08, METAL), 0.0)
    poe(x, _whoosh(rng, 0.25, 1000, 5000, 0.8, 1.4, 0.4), 0.7)
    poe(x, _sino(rng, 800, 1.0, 0.16, METAL), 0.95)
    poe(x, _baque(150, 70, 0.3, 0.6), 0.95)
    poe(x, graos(rng, n_de(0.4), 25, 0.0, 0.5, 2000, 8000, 0.004) * 0.4, 0.95)
    return reverb(x, 0.6, 0.3)


def zero_absoluto(rng, v):
    """Hyoga: o Pó de Diamante (o vento gelado girando e os cristais tilintando)."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.0)
    q = np.random.default_rng(3)
    for k in range(14):
        poe(x, _sino(rng, q.uniform(2500, 4000), 0.3, 0.02, VIDRO), 0.1 + 0.09 * k)
    return reverb(x, 0.7, 0.35)


def fenix_ikki(rng, v):
    """Ikki: o grito da Fênix e as asas de fogo batendo."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(varre(1800, 2600, n, 0.6) * (1 + 0.05 * np.sin(2 * math.pi * 14 * t)), n) * env(n, 0.03, 0.45) * 0.06, 0.0)
    for k in range(3):
        m = n_de(0.35)
        poe(x, satura(passa(rosa(rng, m), 150, 3000, 2), 1.7) * sobe_e_some(m, 0.3, 1.4) * 0.5, 0.25 + 0.25 * k)
    return reverb(x, 0.6, 0.3)


def rugido_leao(rng, v):
    """Aiolia: o rugido do leão e o Relâmpago de Plasma (muitos estalos de luz)."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(seno(varre(150, 90, n) * (1 + 0.08 * np.sin(2 * math.pi * 28 * t)), n) + passa(rosa(rng, n), 150, 2000, 2) * 0.8, 3) * env(n, 0.03, 0.45) * 0.18, 0.0)
    poe(x, graos(rng, n_de(1.0), 140, 0.0, 0.9, 2500, 11000, 0.0015) * 0.5, 0.3)
    poe(x, _trovao(rng, 0.7, 0.4), 0.35)
    return reverb(x, 0.6, 0.3)


def esquife(rng, v):
    """Camus: o gelo crescendo em prisma (os rangidos frios que sobem) e o fecho (o cristal batendo)."""
    x = _z(2.1)
    for k in range(10):
        n = n_de(0.15)
        poe(x, seno(varre(800 + 150 * k, 1200 + 150 * k, n), n) * env(n, 0.01, 0.1) * 0.025, 0.08 * k)
        poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.006) * 0.3, 0.08 * k)
    poe(x, _sino(rng, 1760, 1.2, 0.08, VIDRO), 0.9)
    poe(x, _sopro(rng, 1.0, 2500, 8000, 0.15, 0.4), 0.9)
    return reverb(x, 0.8, 0.4)


def juizo(rng, v):
    """Hades: o eclipse (o acorde fundo e escuro) e as lâminas caindo."""
    x = _z(2.1)
    poe(x, _acorde((65, 78, 98, 131), 1.8, 0.07, 0.3, 1.0), 0.0)
    poe(x, passa(rosa(rng, n_de(1.6)), 40, 400, 2) * sobe_e_some(n_de(1.6), 0.3, 1.2) * 0.4, 0.0)
    for k in range(5):
        poe(x, _whoosh(rng, 0.2, 1500, 7000, 0.8, 1.3, 0.3), 0.75 + 0.1 * k)
        poe(x, _sino(rng, 1500 + 120 * k, 0.3, 0.03, METAL), 0.95 + 0.1 * k)
    return reverb(x, 0.8, 0.4)


def meteoro(rng, v):
    """Madara: o meteoro descendo (o ronco que cresce) e o impacto enorme."""
    x = _z(2.4)
    n = n_de(0.9)
    poe(x, (passa(rosa(rng, n), 80, 1500, 2) * 0.5 + seno(varre(80, 50, n), n) * 0.1) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _explosao(rng, 1.0, 45), 0.9)
    k = n_de(1.4)
    poe(x, passa(rosa(rng, k), 30, 400, 2) * env(k, 0.01, 0.8) * 0.6, 0.9)
    poe(x, graos(rng, k, 40, 0.1, 0.9, 300, 3000, 0.01) * 0.3, 1.0)
    return reverb(x, 0.8, 0.4)


def shinra_tensei(rng, v):
    """Pain: o silêncio, a voz baixa (o tom grave) e a onda de repulsão que explode para fora."""
    x = _z(2.2)
    n = n_de(0.7)
    poe(x, (seno(98, n) + seno(147, n) * 0.5) * sobe_e_some(n, 0.8, 1.0) * 0.07, 0.0)
    poe(x, _baque(50, 20, 0.9, 1.0, 3.0), 0.7)
    m = n_de(1.3)
    poe(x, satura(passa(rosa(rng, m), 40, 2500, 2) * env(m, 0.002, 0.6), 2.2) * 0.8, 0.7)
    poe(x, graos(rng, m, 40, 0.1, 0.8, 300, 3000, 0.01) * 0.3, 0.8)
    return reverb(x, 0.8, 0.4)


def selo_ceifador(rng, v):
    """Minato: os kunais voando (o zunido duplo), o teletransporte e o selo (o coro fantasmagórico)."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.4, 1.4, 0.4), 0.05 * k)
    poe(x, estalo(rng, n_de(0.04), 3000, 9000, 0.006) * 0.8, 0.6)
    n = n_de(1.3)
    t = _t(n)
    poe(x, (seno(220, n) + seno(233, n) * 0.8 + seno(330, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.04, 0.65)
    poe(x, _sino(rng, 147, 1.0, 0.1, SINO), 0.7)
    return reverb(x, 0.8, 0.4)


def futuro(rng, v):
    """Trunks: a fenda do tempo abrindo (o zumbido que distorce) e as faíscas da viagem."""
    x = _z(2.0)
    n = n_de(1.5)
    t = _t(n)
    poe(x, satura(seno(110 + 40 * np.sin(2 * math.pi * 2 * t), n) + seno(220 + 60 * np.sin(2 * math.pi * 3 * t), n) * 0.5, 2) * sobe_e_some(n, 0.4, 1.2) * 0.08, 0.0)
    poe(x, graos(rng, n, 80, 0.1, 0.8, 2500, 10000, 0.002) * 0.35, 0.0)
    poe(x, _trovao(rng, 0.6, 0.3), 0.4)
    poe(x, _brilho(rng, 0.6, 1760, 0.04, CRISTAL), 1.5)
    return reverb(x, 0.7, 0.35)


def lendario(rng, v):
    """Broly: a aura lendária roncando cada vez mais alto e o grito."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 60, 1500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 9 * t)), 2.0) * sobe_e_some(n, 0.7, 1.0) * 0.5, 0.0)
    poe(x, graos(rng, n, 60, 0.0, 0.9, 3000, 11000, 0.002) * 0.35, 0.1)
    m = n_de(0.7)
    poe(x, satura(seno(varre(110, 160, m), m) + passa(rosa(rng, m), 150, 2000, 2) * 0.6, 3) * env(m, 0.05, 0.4) * 0.16, 0.8)
    return reverb(x, 0.6, 0.3)


def hakai(rng, v):
    """Beerus: a mão acendendo (o zumbido roxo, baixo) e o alvo se desfazendo (o sussurro que sobe)."""
    x = _z(2.2)
    n = n_de(0.8)
    poe(x, (seno(165, n) + seno(175, n)) * sobe_e_some(n, 0.8, 1.0) * 0.05, 0.0)
    poe(x, _baque(120, 60, 0.2, 0.4), 0.7)
    m = n_de(1.4)
    poe(x, passa(rosa(rng, m), 1500, 7000, 2) * sobe_e_some(m, 0.3, 1.4) * 0.3, 0.8)
    poe(x, graos(rng, m, 100, 0.0, 0.9, 3000, 9000, 0.003) * 0.25, 0.8)
    return reverb(x, 0.8, 0.4)


def fogo_espalha(rng, v):
    """Charizard: a explosão de fogo e as duas línguas de chama correndo para os lados."""
    x = _z(2.0)
    poe(x, _explosao(rng, 0.7, 70), 0.0)
    m = n_de(1.2)
    poe(x, satura(passa(rosa(rng, m), 150, 4000, 2), 1.8) * sobe_e_some(m, 0.3, 1.3) * 0.5, 0.3)
    poe(x, graos(rng, m, 60, 0.0, 0.9, 1500, 7000, 0.004) * 0.3, 0.3)
    return reverb(x, 0.5, 0.25)


def evoluiu(rng, v):
    """Garou: as correntes de água girando (o fluxo que roda) e a evolução (o grave que cresce)."""
    x = _z(1.9)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.4, 0.0)
    m = n_de(0.7)
    poe(x, satura(seno(varre(60, 110, m), m), 2.5) * sobe_e_some(m, 0.8, 1.0) * 0.1, 0.9)
    return reverb(x, 0.6, 0.3)


def sacrificio(rng, v):
    """Genos: o núcleo sobrecarregando (o apito que sobe), as rachaduras e a explosão."""
    x = _z(2.2)
    n = n_de(0.9)
    poe(x, seno(varre(400, 2400, n, 1.4), n) * sobe_e_some(n, 0.95, 1.0) * 0.05, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.01) * 0.6, 0.5 + 0.08 * k)
    poe(x, _explosao(rng, 1.0, 50), 0.9)
    return reverb(x, 0.6, 0.3)


def briga_de_rua(rng, v):
    """Yusuke: a Arma Espiritual carregando no dedo (o zumbido que sobe) e o disparo."""
    x = _z(1.9)
    n = n_de(0.9)
    poe(x, (seno(varre(200, 900, n, 1.3), n) * 0.06 + passa(rosa(rng, n), 800, 5000, 2) * 0.15) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _baque(140, 60, 0.4, 0.7, 2.4), 0.9)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 400, 6000, 2) * env(m, 0.002, 0.3) * 0.5, 0.9)
    poe(x, _laser_curto(rng), 0.92)
    return reverb(x, 0.5, 0.25)


def _laser_curto(rng):
    n = n_de(0.4)
    return seno(varre(1400, 500, n), n) * env(n, 0.003, 0.3) * 0.05


def nao_estava_la(rng, v):
    """Hiei: os passos rápidos sumindo (os sopros curtos) e o Jagan abrindo (o tom que vibra)."""
    x = _z(1.9)
    for k in range(4):
        poe(x, _whoosh(rng, 0.12, 2000, 9000, 0.4, 1.4, 0.4), 0.05 + 0.1 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(300, 450, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.06, 0.7)
    poe(x, _sino(rng, 1047, 0.8, 0.04, VIDRO), 0.75)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-primeiro": (primeiro, "Hayabusa: as shurikens e o corte"),
    "mu-punicao": (punicao, "Cabeça de Pirâmide: a faca arrastando"),
    "mu-inalar": (inalar, "Kirby: inalando"),
    "mu-banana": (banana, "Donkey Kong: a casca de banana"),
    "mu-vampire-killer": (vampire_killer, "Simon: o chicote e a cruz"),
    "mu-areias": (areias, "Príncipe da Pérsia: as Areias do Tempo"),
    "mu-pegaso": (pegaso, "Seiya: os Meteoros de Pégaso"),
    "mu-absorcao": (absorcao, "Majin Boo: a absorção"),
    "mu-kuririn-nao": (kuririn_nao, "Kuririn: a fúria dourada"),
    "mu-escudo-dragao": (escudo_dragao, "Shiryu: o Escudo do Dragão"),
    "mu-zero-absoluto": (zero_absoluto, "Hyoga: o Pó de Diamante"),
    "mu-fenix-ikki": (fenix_ikki, "Ikki: a Fênix"),
    "mu-rugido-leao": (rugido_leao, "Aiolia: o rugido e o Relâmpago de Plasma"),
    "mu-esquife": (esquife, "Camus: o Esquife de Gelo"),
    "mu-juizo": (juizo, "Hades: o juízo"),
    "mu-meteoro": (meteoro, "Madara: o meteoro"),
    "mu-shinra-tensei": (shinra_tensei, "Pain: o Shinra Tensei"),
    "mu-selo-ceifador": (selo_ceifador, "Minato: o Selo do Ceifador"),
    "mu-futuro": (futuro, "Trunks: a fenda do tempo"),
    "mu-lendario": (lendario, "Broly: a aura lendária"),
    "mu-hakai": (hakai, "Beerus: o Hakai"),
    "mu-fogo-espalha": (fogo_espalha, "Charizard: o fogo que se espalha"),
    "mu-evoluiu": (evoluiu, "Garou: a evolução"),
    "mu-sacrificio": (sacrificio, "Genos: o sacrifício"),
    "mu-briga-de-rua": (briga_de_rua, "Yusuke: a Arma Espiritual"),
    "mu-nao-estava-la": (nao_estava_la, "Hiei: não estava lá"),
}
