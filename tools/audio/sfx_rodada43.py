"""Os sons da rodada 43 das habilidades próprias (veja tools/vfx/familias_v2/rodada43.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _pedrinhas(rng, x, em, n=6, seed=4):
    q = np.random.default_rng(seed)
    for k in range(n):
        poe(x, _baque(q.uniform(180, 320), 100, 0.06, 0.2), em + q.uniform(0, 0.35))


# ------------------------------------------------------------------ Morty

def arma_de_laser_morty(rng, v):
    """Morty: a arma de laser (o "pzzzew" tremido) e o acerto."""
    x = _z(1.8)
    n = n_de(0.35)
    t = _t(n)
    poe(x, (seno(varre(1800, 500, n) * (1 + 0.05 * np.sin(2 * math.pi * 40 * t)), n)) * env(n, 0.005, 0.3) * 0.05, 0.2)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.3)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.008), 0.3)
    return reverb(x, 0.4, 0.2)


def grito_de_panico(rng, v):
    """Morty: "Ai, caramba, Rick!" — o grito tremido em pânico."""
    x = _z(2.0)
    n = n_de(0.7)
    t = _t(n)
    f = 650 * (1 + 0.1 * np.sin(2 * math.pi * 14 * t)) * (1 + 0.15 * np.sin(math.pi * t / t[-1]))
    poe(x, satura(seno(f, n) + 0.4 * seno(f * 2, n), 2.5) * env(n, 0.02, 0.4) * 0.045, 0.05)
    _estrelinhas(rng, x, 0.6)
    return reverb(x, 0.5, 0.25)


def morty_preparo(rng, v):
    """Morty (Preparo): o Morty mau (o acorde frio e grave em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(98, n) + seno(117, n) * 0.6 + seno(147, n) * 0.4) * sobe_e_some(n, 0.6, 1.2) * 0.035, 0.0)
    poe(x, _sino(rng, 1568, 0.6, 0.012, CRISTAL), 0.4)
    return reverb(x, 0.8, 0.4)


def morty_mau(rng, v):
    """Morty: o Morty mau — o espiral girando e o feixe frio no rival."""
    x = _z(2.2)
    n = n_de(0.35)
    t = _t(n)
    poe(x, seno(300 + 100 * np.sin(2 * math.pi * 6 * t), n) * env(n, 0.05, 0.2) * 0.03, 0.0)
    n = n_de(0.45)
    poe(x, satura(seno(varre(200, 150, n), n) + passa(rosa(rng, n), 200, 3000, 2) * 0.4, 2.5) * env(n, 0.01, 0.4) * 0.06, 0.3)
    poe(x, _baque(80, 32, 0.6, 0.9, 2.8), 0.4)
    poe(x, _explosao(rng, 0.4, 70), 0.42)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Tails

def giro_de_cauda(rng, v):
    """Tails: as caudas girando como hélice ("vupvupvup") e as batidas."""
    x = _z(1.9)
    n = n_de(0.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 4000, 2) * (0.3 + 0.7 * np.sin(2 * math.pi * 15 * t) ** 2) * env(n, 0.02, 0.4) * 0.3, 0.0)
    for k in range(3):
        poe(x, _baque(170, 80, 0.1, 0.4), 0.3 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def voo_de_resgate(rng, v):
    """Tails: o voo de hélice e o "plim" dos anéis no trio."""
    x = _z(2.1)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 18 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2093, 0.4, 0.03, CRISTAL), 0.2 + 0.1 * k)
        poe(x, _sino(rng, 2637, 0.4, 0.02, CRISTAL), 0.23 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def tails_preparo(rng, v):
    """Tails (Preparo): a engrenagem girando e o canhão carregando (em laço)."""
    x = _z(1.4)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.015), 1500, 5000, 0.003) * 0.4, 0.12 * k)
    n = n_de(1.0)
    poe(x, seno(varre(300, 900, n), n) * sobe_e_some(n, 0.8, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def canhao_de_energia_tails(rng, v):
    """Tails: o tiro do canhão de energia (o raio elétrico) e o impacto."""
    x = _z(2.0)
    n = n_de(0.45)
    poe(x, satura(seno(varre(800, 500, n), n), 2.5) * env(n, 0.01, 0.4) * 0.05, 0.15)
    poe(x, _trovao(rng, 0.45, 0.35), 0.2)
    poe(x, _baque(100, 40, 0.4, 0.7), 0.3)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Knuckles

def soco_espinhoso(rng, v):
    """Knuckles: o soco da luva com espinhos (o "tchac" metálico)."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 300, 3500, 0.8, 1.3, 0.5), 0.0)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.6), 0.26)
    poe(x, _sino(rng, 784, 0.3, 0.03, METAL), 0.26)
    return reverb(x, 0.5, 0.25)


def escavar(rng, v):
    """Knuckles: cavando o chão (a terra voando) e o monte se formando."""
    x = _z(2.0)
    for k in range(8):
        poe(x, satura(passa(rosa(rng, n_de(0.07)), 150, 1500, 2), 2) * env(n_de(0.07), 0.003, 0.06) * 0.35, 0.05 * k)
    _pedrinhas(rng, x, 0.2)
    poe(x, _baque(90, 40, 0.4, 0.6), 0.45)
    return reverb(x, 0.5, 0.25)


def knuckles_preparo(rng, v):
    """Knuckles (Preparo): o punho erguido e as pedras flutuando (o ronco da terra)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 40, 300, 2) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.0)
    for k in range(4):
        poe(x, _baque(250, 150, 0.05, 0.12), 0.25 * k)
    return reverb(x, 0.5, 0.25)


def soco_do_terremoto(rng, v):
    """Knuckles: o soco no chão (o estrondo), as rachaduras e as pedras caindo."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.3, 150, 2000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(45, 18, 1.1, 1.0, 3.2), 0.28)
    poe(x, _explosao(rng, 0.8, 45), 0.28)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.06), 200, 2500, 0.015) * 0.6, 0.32 + 0.05 * k)
    _pedrinhas(rng, x, 0.45, 8, 7)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Velma

def lupa_da_velma(rng, v):
    """Velma: a lupa examinando e o "Jinkies!" da pista encontrada."""
    x = _z(1.9)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 6000, 2) * env(n, 0.05, 0.3) * 0.08, 0.0)
    for k, f in enumerate((784, 988, 1319)):
        poe(x, _sino(rng, f, 0.4, 0.03, CRISTAL), 0.45 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def cade_meus_oculos(rng, v):
    """Velma: os óculos caindo ("plic") e a Velma tateando ("Meus óculos!")."""
    x = _z(2.0)
    poe(x, _piu(1200, 600, 0.3, 0.025), 0.0)
    poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.005), 0.35)
    poe(x, _sino(rng, 2349, 0.3, 0.02, METAL), 0.35)
    for k in range(3):
        n = n_de(0.1)
        poe(x, satura(seno(varre(500, 600, n), n), 2) * env(n, 0.01, 0.08) * 0.03, 0.55 + 0.13 * k)
    return reverb(x, 0.4, 0.2)


def velma_preparo(rng, v):
    """Velma (Preparo): o raciocínio (as notinhas de "hmm" em laço)."""
    x = _z(1.4)
    for k, f in enumerate((523, 587, 659, 587)):
        n = n_de(0.15)
        poe(x, seno(f, n) * env(n, 0.01, 0.12) * 0.025, 0.25 * k)
    return reverb(x, 0.5, 0.25)


def tirar_a_mascara(rng, v):
    """Velma: a máscara arrancada ("rrrip") e o mistério resolvido."""
    x = _z(2.1)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1000, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 40 * _t(n)) ** 2) * env(n, 0.005, 0.2) * 0.4, 0.25)
    poe(x, _whoosh(rng, 0.3, 500, 4000, 0.7, 1.3, 0.3), 0.3)
    poe(x, _acorde((392, 494, 587, 784), 0.9, 0.035, 0.02, 0.7), 0.45)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Fred

def rede_do_fred(rng, v):
    """Fred: a rede voando (o "fuuu") e caindo em cima do rival."""
    x = _z(1.9)
    poe(x, _sopro(rng, 0.45, 300, 2500, 0.2, 0.4), 0.0)
    poe(x, passa(rosa(rng, n_de(0.2)), 500, 3000, 2) * env(n_de(0.2), 0.01, 0.15) * 0.3, 0.45)
    poe(x, _baque(200, 110, 0.1, 0.3), 0.45)
    return reverb(x, 0.4, 0.2)


def vamos_nos_separar(rng, v):
    """Fred: "Vamos nos separar, pessoal!" — o acorde de aventura e os passos para os lados."""
    x = _z(2.0)
    poe(x, _acorde((262, 330, 392), 0.6, 0.035, 0.02, 0.45), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 800, 5000, 0.6, 1.4, 0.3), 0.2 + 0.06 * k)
    for k in range(6):
        poe(x, _baque(300 + 40 * (k % 2), 180, 0.03, 0.12), 0.45 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def armadilha_perfeita(rng, v):
    """Fred: a corda soltando, a gaiola caindo ("CLANG") e o rival preso."""
    x = _z(2.1)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006), 0.0)
    n = n_de(0.3)
    poe(x, seno(varre(1200, 500, n), n) * env(n, 0.02, 0.25) * 0.03, 0.1)
    poe(x, _baque(120, 50, 0.4, 0.8, 2.4), 0.38)
    poe(x, _sino(rng, 311, 1.0, 0.06, METAL), 0.38)
    poe(x, _sino(rng, 466, 0.8, 0.04, METAL), 0.4)
    _estrelinhas(rng, x, 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Leorio

def soco_teletransportado(rng, v):
    """Leorio: o portal abrindo (o "vuóm") e o soco saindo do outro lado."""
    x = _z(1.9)
    n = n_de(0.35)
    t = _t(n)
    poe(x, seno(varre(200, 500, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 12 * t)) * env(n, 0.05, 0.25) * 0.04, 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 3000, 0.7, 1.3, 0.4), 0.25)
    poe(x, _baque(120, 50, 0.4, 0.8, 2.4), 0.42)
    return reverb(x, 0.6, 0.3)


def primeiros_socorros(rng, v):
    """Leorio: a maleta abrindo, a faixa enrolando e a cura."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006), 0.05)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * _t(n)) ** 2) * env(n, 0.05, 0.4) * 0.15, 0.25)
    poe(x, _acorde((440, 554, 659), 0.8, 0.03, 0.05, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


def leorio_preparo(rng, v):
    """Leorio (Preparo): o bisturi de Nen brilhando (o zumbido fino em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, seno(2400, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.008, 0.0)
    poe(x, graos(rng, n, 15, 0.0, 0.95, 3000, 9000, 0.003) * 0.2, 0.0)
    return reverb(x, 0.6, 0.3)


def bisturi_de_nen(rng, v):
    """Leorio: o corte do bisturi (o silvo finíssimo) e o acerto preciso."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.12, 4000, 14000, 0.8, 1.2, 0.45), 0.25)
    poe(x, _sino(rng, 3136, 0.5, 0.035, METAL), 0.3)
    poe(x, _baque(170, 80, 0.15, 0.35), 0.32)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "arma-de-laser-morty": (arma_de_laser_morty, "Morty: a arma de laser"),
    "grito-de-panico": (grito_de_panico, "Morty: o grito de pânico"),
    "morty-preparo": (morty_preparo, "Morty: o Morty mau (Preparo)"),
    "morty-mau": (morty_mau, "Morty: Morty mau"),
    "giro-de-cauda": (giro_de_cauda, "Tails: o giro de cauda"),
    "voo-de-resgate": (voo_de_resgate, "Tails: o voo de resgate"),
    "tails-preparo": (tails_preparo, "Tails: o canhão carregando (Preparo)"),
    "canhao-de-energia-tails": (canhao_de_energia_tails, "Tails: o canhão de energia"),
    "soco-espinhoso": (soco_espinhoso, "Knuckles: o soco espinhoso"),
    "escavar": (escavar, "Knuckles: escavar"),
    "knuckles-preparo": (knuckles_preparo, "Knuckles: as pedras flutuando (Preparo)"),
    "soco-do-terremoto": (soco_do_terremoto, "Knuckles: o soco do terremoto"),
    "lupa-da-velma": (lupa_da_velma, "Velma: a lupa"),
    "cade-meus-oculos": (cade_meus_oculos, "Velma: Cadê meus óculos?"),
    "velma-preparo": (velma_preparo, "Velma: o raciocínio (Preparo)"),
    "tirar-a-mascara": (tirar_a_mascara, "Velma: tirar a máscara"),
    "rede-do-fred": (rede_do_fred, "Fred: a rede"),
    "vamos-nos-separar": (vamos_nos_separar, "Fred: Vamos nos separar"),
    "armadilha-perfeita": (armadilha_perfeita, "Fred: a armadilha perfeita"),
    "soco-teletransportado": (soco_teletransportado, "Leorio: o soco teletransportado"),
    "primeiros-socorros": (primeiros_socorros, "Leorio: os primeiros socorros"),
    "leorio-preparo": (leorio_preparo, "Leorio: o bisturi brilhando (Preparo)"),
    "bisturi-de-nen": (bisturi_de_nen, "Leorio: o bisturi de Nen"),
}
