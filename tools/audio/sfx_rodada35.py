"""Os sons da rodada 35 das habilidades próprias (veja tools/vfx/familias_v2/rodada35.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _miau(rng, seg=0.35, f=600, g=0.05):
    """O miado irritado (o tom que sobe e desce com o vibrato)."""
    n = n_de(seg)
    t = _t(n)
    f_t = f * (1 + 0.5 * np.sin(math.pi * t / t[-1])) * (1 + 0.03 * np.sin(2 * math.pi * 8 * t))
    return satura(seno(f_t, n) + 0.3 * seno(f_t * 2, n), 2) * env(n, 0.03, seg * 0.6) * g


# ------------------------------------------------------------------ Tom

def emboscada_do_tom(rng, v):
    """Tom: a frigideira girando e o "PÉÉÉIM" metálico na cara do rival."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.25, 400, 4000, 0.8, 1.4, 0.45), 0.05)
    poe(x, _sino(rng, 523, 1.0, 0.08, METAL), 0.28)
    poe(x, _sino(rng, 784, 0.8, 0.05, METAL), 0.28)
    poe(x, _baque(150, 70, 0.25, 0.55), 0.28)
    _estrelinhas(rng, x, 0.55)
    return reverb(x, 0.5, 0.25)


def perseguicao(rng, v):
    """Tom: a perseguição (os pés correndo rápido, o miado e a derrapada)."""
    x = _z(2.0)
    for k in range(14):
        poe(x, _baque(220 + 30 * (k % 2), 130, 0.04, 0.17), 0.035 * k)
    poe(x, _miau(rng, 0.3, 650, 0.04), 0.05)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.01, 0.2) * 0.3, 0.5)
    poe(x, _baque(140, 60, 0.3, 0.55), 0.52)
    return reverb(x, 0.4, 0.2)


def tom_preparo(rng, v):
    """Tom (Preparo): as unhas afiando (o raspar ritmado)."""
    x = _z(1.4)
    for k in range(4):
        n = n_de(0.15)
        poe(x, passa(rosa(rng, n), 2500, 9000, 2) * env(n, 0.03, 0.1) * 0.25, 0.25 * k)
    poe(x, _sino(rng, 3136, 0.3, 0.015, METAL), 0.9)
    return reverb(x, 0.4, 0.2)


def pata_certeira(rng, v):
    """Tom: a patada (os três arranhões) e o grito do gato."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 2000, 9000, 0.6, 1.3, 0.4), 0.1 + 0.04 * k)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.4), 0.3)
    poe(x, _miau(rng, 0.45, 750, 0.045), 0.35)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Jerry

def ratoeira_invertida(rng, v):
    """Jerry: a ratoeira armando (o clique) e o "TLEC" fechando no rival."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.6, 0.0)
    poe(x, estalo(rng, n_de(0.06), 800, 6000, 0.012) * 1.4, 0.3)
    poe(x, _sino(rng, 1047, 0.4, 0.04, METAL), 0.3)
    poe(x, _baque(170, 80, 0.15, 0.4), 0.3)
    poe(x, _piu(900, 1600, 0.12, 0.03), 0.5)
    return reverb(x, 0.4, 0.2)


def esconderijo(rng, v):
    """Jerry: o ratinho correndo para o buraco e o rival batendo a cara na parede."""
    x = _z(2.0)
    for k in range(6):
        poe(x, _baque(350 + 40 * (k % 2), 220, 0.03, 0.12), 0.05 + 0.04 * k)
    poe(x, _piu(1200, 1800, 0.08, 0.03), 0.28)
    poe(x, _whoosh(rng, 0.2, 300, 3000, 0.7, 1.4, 0.4), 0.35)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.4), 0.53)
    poe(x, estalo(rng, n_de(0.06), 400, 3000, 0.012), 0.53)
    _estrelinhas(rng, x, 0.65, 4)
    return reverb(x, 0.5, 0.25)


def martelada(rng, v):
    """Jerry: o martelo enorme subindo, descendo e o "BONK"."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.35, 150, 2000, 0.85, 1.3, 0.55), 0.0)
    poe(x, _baque(80, 30, 0.6, 1.0, 3.0), 0.33)
    poe(x, _sino(rng, 330, 0.7, 0.06, METAL), 0.33)
    poe(x, _piu(400, 900, 0.15, 0.03), 0.45)
    _estrelinhas(rng, x, 0.55, 5)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Pantera Cor-de-Rosa

def passo_silencioso(rng, v):
    """Pantera: a ponta dos pés no ritmo do tema (os passinhos) e o "shhh"."""
    x = _z(2.0)
    for k, f in enumerate((311, 330, 370, 392, 311, 330)):
        n = n_de(0.08)
        poe(x, (seno(f, n) * 0.4 + passa(rosa(rng, n), 1000, 3000, 2) * 0.3) * env(n, 0.005, 0.07) * 0.06, 0.06 * k * 1.5)
    poe(x, _sopro(rng, 0.5, 3000, 9000, 0.12, 0.3), 0.45)
    return reverb(x, 0.6, 0.3)


def troca_discreta(rng, v):
    """Pantera: o "puf" da troca de lugar, o deslize e o golpe."""
    x = _z(1.9)
    poe(x, passa(rosa(rng, n_de(0.25)), 500, 4000, 2) * env(n_de(0.25), 0.005, 0.2) * 0.35, 0.15)
    poe(x, _piu(700, 1100, 0.1, 0.03), 0.3)
    poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.7, 1.3, 0.45), 0.45)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.58)
    return reverb(x, 0.5, 0.25)


def sumico(rng, v):
    """Pantera: a fumaça do sumiço e o mistério (o acorde de jazz e o "hmm?")."""
    x = _z(2.2)
    poe(x, passa(rosa(rng, n_de(0.4)), 400, 4000, 2) * env(n_de(0.4), 0.005, 0.35) * 0.35, 0.0)
    poe(x, _acorde((147, 175, 220, 262, 311), 1.2, 0.035, 0.05, 1.0), 0.3)
    for k in range(3):
        poe(x, _piu(600, 800, 0.12, 0.025), 0.45 + 0.07 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Destruidor

def garras_de_aco(rng, v):
    """Destruidor: as três lâminas da manopla rasgando."""
    x = _z(1.8)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 3000, 12000, 0.6, 1.3, 0.45), 0.05 + 0.03 * k)
        poe(x, _sino(rng, 2349 + 200 * k, 0.3, 0.025, METAL), 0.12 + 0.03 * k)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.2)
    return reverb(x, 0.5, 0.25)


def investida_do_cla(rng, v):
    """Destruidor: os ninjas do Clã do Pé chegando de todo lado e o golpe junto."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _whoosh(rng, 0.2, 1000, 7000, 0.8, 1.3, 0.3), 0.03 * k)
    poe(x, _baque(110, 45, 0.45, 0.8, 2.6), 0.3)
    poe(x, estalo(rng, n_de(0.05), 800, 4000, 0.01), 0.3)
    return reverb(x, 0.5, 0.25)


def shredder_preparo(rng, v):
    """Destruidor (Preparo): a manopla erguida (as lâminas raspando e o rosnado)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.3)
        poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.05, 0.2) * 0.15, 0.1 + 0.5 * k)
        poe(x, _sino(rng, 2637, 0.4, 0.02, METAL), 0.35 + 0.5 * k)
    n = n_de(0.9)
    poe(x, satura(seno(varre(90, 75, n), n), 2.5) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    return reverb(x, 0.5, 0.25)


def golpe_do_mestre(rng, v):
    """Destruidor: a rajada de cortes cruzados sem parar e o último golpe."""
    x = _z(2.0)
    for k in range(9):
        poe(x, _whoosh(rng, 0.08, 2500, 11000, 0.6, 1.3, 0.3), 0.03 + 0.06 * k)
        poe(x, _sino(rng, 1760 + 150 * (k % 4), 0.15, 0.015, METAL), 0.1 + 0.06 * k)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.55)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Mestre Splinter

def postura_do_rato(rng, v):
    """Mestre Splinter: a meditação (o gongo, o vento e a flauta calma)."""
    x = _z(2.2)
    poe(x, _sino(rng, 147, 1.6, 0.08, SINO), 0.0)
    poe(x, _sopro(rng, 1.2, 300, 2000, 0.12, 0.4), 0.1)
    for k, f in enumerate((587, 659, 784, 659)):
        n = n_de(0.3)
        poe(x, seno(f, n) * (1 + 0.02 * np.sin(2 * math.pi * 5 * _t(n))) * env(n, 0.05, 0.2) * 0.025, 0.3 + 0.25 * k)
    return reverb(x, 0.9, 0.45)


def redirecionar_splinter(rng, v):
    """Mestre Splinter: a bengala girando ("vuvuvu"), o golpe sendo desviado e voltando."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 600, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * _t(n)) ** 2) * env(n, 0.02, 0.3) * 0.3, 0.0)
    poe(x, _baque(200, 120, 0.1, 0.4), 0.28)
    poe(x, estalo(rng, n_de(0.04), 1000, 4000, 0.008), 0.28)
    poe(x, _whoosh(rng, 0.2, 1000, 6000, 0.7, 1.3, 0.4), 0.35)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.58)
    return reverb(x, 0.5, 0.25)


def licao_final(rng, v):
    """Mestre Splinter: a bengalada na cabeça ("TOC!") e as estrelinhas."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 600, 5000, 0.8, 1.3, 0.4), 0.05)
    poe(x, _baque(300, 200, 0.08, 0.5), 0.3)
    poe(x, estalo(rng, n_de(0.04), 1000, 5000, 0.01) * 1.2, 0.3)
    _estrelinhas(rng, x, 0.45, 4)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Krang

def comando_remoto(rng, v):
    """Krang: o cérebro mandando as ondas (o "uóóó" alienígena) e o escudo ligando."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(400 + 150 * np.sin(2 * math.pi * 5 * t), n) * env(n, 0.05, 0.3) * 0.035, 0.0)
    poe(x, satura(seno(varre(150, 300, n_de(0.3)), n_de(0.3)), 2) * env(n_de(0.3), 0.01, 0.25) * 0.04, 0.35)
    poe(x, _sino(rng, 1319, 0.5, 0.03, METAL), 0.4)
    poe(x, _brilho(rng, 0.5, 1568, 0.025, CRISTAL), 0.45)
    return reverb(x, 0.6, 0.3)


def krang_preparo(rng, v):
    """Krang (Preparo): o cérebro pulsando (o borbulhar e o zumbido)."""
    x = _z(1.4)
    q = np.random.default_rng(4)
    for k in range(10):
        f = q.uniform(300, 700)
        poe(x, _piu(f, f * 1.5, 0.05, 0.015), 0.09 * k)
    n = n_de(1.0)
    poe(x, seno(110, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    return reverb(x, 0.5, 0.25)


def dimensao_x(rng, v):
    """Krang: o portal da Dimensão X abrindo (o vórtice que gira e suga)."""
    x = _z(2.3)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 7 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.0)
    poe(x, seno(varre(80, 300, n), n) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    poe(x, _baque(70, 30, 0.5, 0.7), 0.45)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 220 * k, 0.3, 0.02, CRISTAL), 0.6 + 0.07 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Casey Jones

def taco_de_hoquei(rng, v):
    """Casey Jones: o taco batendo no disco ("TÉC") e o disco acertando o rival."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.2, 500, 4000, 0.8, 1.4, 0.45), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.008) * 1.2, 0.22)
    poe(x, _baque(300, 200, 0.06, 0.3), 0.22)
    poe(x, _baque(140, 60, 0.25, 0.55), 0.43)
    return reverb(x, 0.4, 0.2)


def sequencia_bruta(rng, v):
    """Casey Jones: o taco e os socos em sequência."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _whoosh(rng, 0.08, 1000, 6000, 0.6, 1.3, 0.3), 0.04 + 0.11 * k)
        poe(x, _baque(150 + 25 * (k % 2), 65, 0.12, 0.5), 0.1 + 0.11 * k)
        if k % 2 == 0:
            poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006), 0.1 + 0.11 * k)
    return reverb(x, 0.4, 0.2)


def gooool(rng, v):
    """Casey Jones: a tacada fortíssima, o disco na rede e a torcida "GOOOL!"."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.2, 400, 5000, 0.8, 1.4, 0.5), 0.0)
    poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.01) * 1.4, 0.18)
    poe(x, _baque(80, 30, 0.6, 1.0, 3.0), 0.38)
    poe(x, _sino(rng, 880, 0.6, 0.05, METAL), 0.38)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * sobe_e_some(n, 0.25, 1.2) * 0.35, 0.45)
    poe(x, _acorde((262, 330, 392, 523), 0.9, 0.035, 0.03, 0.7), 0.5)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "emboscada-do-tom": (emboscada_do_tom, "Tom: a emboscada"),
    "perseguicao": (perseguicao, "Tom: a perseguição"),
    "tom-preparo": (tom_preparo, "Tom: as unhas afiando (Preparo)"),
    "pata-certeira": (pata_certeira, "Tom: a pata certeira"),
    "ratoeira-invertida": (ratoeira_invertida, "Jerry: a ratoeira invertida"),
    "esconderijo": (esconderijo, "Jerry: o esconderijo"),
    "martelada": (martelada, "Jerry: a martelada"),
    "passo-silencioso": (passo_silencioso, "Pantera Cor-de-Rosa: o passo silencioso"),
    "troca-discreta": (troca_discreta, "Pantera Cor-de-Rosa: a troca discreta"),
    "sumico": (sumico, "Pantera Cor-de-Rosa: o sumiço"),
    "garras-de-aco": (garras_de_aco, "Destruidor: as garras de aço"),
    "investida-do-cla": (investida_do_cla, "Destruidor: a investida do Clã"),
    "shredder-preparo": (shredder_preparo, "Destruidor: a manopla erguida (Preparo)"),
    "golpe-do-mestre": (golpe_do_mestre, "Destruidor: o golpe do mestre"),
    "postura-do-rato": (postura_do_rato, "Mestre Splinter: a postura do rato"),
    "redirecionar-splinter": (redirecionar_splinter, "Mestre Splinter: redirecionar"),
    "licao-final": (licao_final, "Mestre Splinter: a lição final"),
    "comando-remoto": (comando_remoto, "Krang: o comando remoto"),
    "krang-preparo": (krang_preparo, "Krang: o cérebro pulsando (Preparo)"),
    "dimensao-x": (dimensao_x, "Krang: a Dimensão X"),
    "taco-de-hoquei": (taco_de_hoquei, "Casey Jones: o taco de hóquei"),
    "sequencia-bruta": (sequencia_bruta, "Casey Jones: a sequência bruta"),
    "gooool": (gooool, "Casey Jones: Goooool!"),
}
