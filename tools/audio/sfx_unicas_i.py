"""Os sons da rodada 8 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_i.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _piu(f0, f1, seg, g=0.05):
    n = n_de(seg)
    return seno(varre(f0, f1, n), n) * env(n, 0.005, seg * 0.7) * g


def desastrado(rng, v):
    """Pateta: o tropeço, o tombo (o baque com a poeira) e os passarinhos girando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 400, 2500, 0.6, 1.4, 0.4), 0.0)
    poe(x, _baque(140, 60, 0.4, 0.8, 2.2), 0.2)
    poe(x, _sopro(rng, 0.6, 200, 2000, 0.3, 0.1), 0.2)
    for k in range(6):
        poe(x, _piu(2200 + 200 * (k % 2), 2600 + 200 * (k % 2), 0.08, 0.035), 0.55 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def destruir(rng, v):
    """Stitch: as garrinhas arranhando e o escudo estilhaçando."""
    x = _z(1.8)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 2000, 9000, 0.5, 1.4, 0.35), 0.15 + 0.05 * k)
    poe(x, estalo(rng, n_de(0.05), 1500, 9000, 0.01), 0.55)
    for k in range(8):
        poe(x, _sino(rng, 2000 + 250 * (k % 4), 0.25, 0.03, VIDRO), 0.55 + 0.03 * k)
    return reverb(x, 0.5, 0.25)


def infinito(rng, v):
    """Buzz: as asas abrindo (o clique e o "fssst"), o laser e o jato."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.04), 1500, 5000, 0.006) * 0.8, 0.0)
    poe(x, passa(rosa(rng, n_de(0.25)), 2000, 7000, 2) * env(n_de(0.25), 0.005, 0.15) * 0.4, 0.02)
    poe(x, _piu(1800, 1700, 0.3, 0.04), 0.55)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.95)
    return reverb(x, 0.5, 0.25)


def cordinha(rng, v):
    """Woody: a cordinha voltando (o zíper de corda) e a frase (os tons de caixinha falante)."""
    x = _z(1.9)
    n = n_de(0.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 60 * t)) * env(n, 0.01, 0.3) * 0.35, 0.0)
    for k, f in enumerate((330, 392, 330, 440, 392)):
        m = n_de(0.12)
        poe(x, satura(seno(f, m) + seno(f * 2, m) * 0.4, 1.4) * env(m, 0.01, 0.09) * 0.04, 0.55 + 0.13 * k)
    poe(x, _sino(rng, 1568, 0.5, 0.04, METAL), 1.25)
    return reverb(x, 0.4, 0.2)


def arremesso_carro(rng, v):
    """Sr. Incrível: o carro voando (o vento pesado) e o estrondo do metal amassando."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.7, 150, 2000, 0.6, 1.5, 0.6), 0.0)
    poe(x, _baque(70, 30, 0.7, 1.0, 2.8), 0.95)
    for k in range(6):
        poe(x, _sino(rng, 300 + 120 * k, 0.4, 0.06, METAL), 0.95 + 0.02 * k)
    poe(x, estalo(rng, n_de(0.08), 800, 6000, 0.03) * 0.6, 0.97)
    return reverb(x, 0.5, 0.25)


def estica(rng, v):
    """Mulher-Elástica: o corpo esticando (o tom que estica e volta, como borracha)."""
    x = _z(1.8)
    n = n_de(1.2)
    t = _t(n)
    f = 220 * (1 + 0.6 * np.sin(math.pi * np.clip(t / 0.9, 0, 1)) ** 2) * (1 + 0.04 * np.sin(2 * math.pi * 14 * t))
    poe(x, satura(seno(f, n), 1.5) * env(n, 0.02, 0.6) * 0.06, 0.05)
    poe(x, _baque(200, 100, 0.2, 0.3), 0.6)
    return reverb(x, 0.4, 0.2)


def estado_avatar(rng, v):
    """Korra: os quatro elementos (água, fogo, terra e ar) girando e o Estado Avatar (o coro e o vento)."""
    x = _z(2.1)
    poe(x, passa(rosa(rng, n_de(0.3)), 300, 2000, 2) * env(n_de(0.3), 0.01, 0.2) * 0.3, 0.0)
    poe(x, satura(passa(rosa(rng, n_de(0.3)), 200, 3000, 2), 1.6) * env(n_de(0.3), 0.01, 0.2) * 0.35, 0.15)
    poe(x, _baque(120, 60, 0.2, 0.4), 0.3)
    poe(x, _whoosh(rng, 0.3, 500, 3000, 0.6, 1.4, 0.35), 0.45)
    poe(x, _acorde((147, 220, 294, 440), 1.4, 0.06, 0.15, 0.8), 0.6)
    return reverb(x, 0.8, 0.4)


def redirecionado(rng, v):
    """Zuko: o raio chegando, contornando o corpo (o zumbido que gira) e voltando com o trovão."""
    x = _z(1.9)
    poe(x, graos(rng, n_de(1.2), 140, 0.0, 0.9, 2500, 11000, 0.0015) * 0.45, 0.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(120 + 60 * np.sin(2 * math.pi * 1.2 * t), n), 2) * env(n, 0.02, 0.6, segura=0.3) * 0.08, 0.0)
    poe(x, _trovao(rng, 0.8, 0.7), 1.0)
    return reverb(x, 0.6, 0.3)


def terremoto(rng, v):
    """Toph: o pé batendo no chão, o tremor (o ronco grave) e as pedras subindo."""
    x = _z(2.0)
    poe(x, _baque(80, 35, 0.4, 1.0, 2.6), 0.0)
    n = n_de(1.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 25, 300, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 11 * t)) * env(n, 0.01, 0.8) * 0.7, 0.05)
    for k in range(6):
        poe(x, _baque(150 - 10 * k, 80, 0.2, 0.35, 2.2), 0.3 + 0.08 * k)
        poe(x, estalo(rng, n_de(0.05), 300, 2500, 0.02) * 0.4, 0.3 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def dragao_oeste(rng, v):
    """Iroh: o sopro de fogo enorme (o rugido de chama longo)."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 120, 4500, 2) * (0.75 + 0.25 * np.sin(2 * math.pi * 7 * t)), 2.0) * sobe_e_some(n, 0.25, 1.1) * 0.6, 0.0)
    poe(x, graos(rng, n, 80, 0.0, 0.9, 1500, 7000, 0.004) * 0.3, 0.0)
    poe(x, (seno(98, n) + seno(104, n)) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.0)
    return reverb(x, 0.6, 0.3)


def temporada(rng, v):
    """Patolino: o tiro de espingarda, o bico girando (o assobio) e o "despicable" (o tom torto)."""
    x = _z(1.9)
    m = n_de(0.4)
    poe(x, satura(passa(rosa(rng, m), 100, 7000, 2) * env(m, 0.0005, 0.1), 3.0) * 0.8, 0.0)
    poe(x, _baque(100, 40, 0.4, 0.8, 2.6), 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(900 + 300 * np.sin(2 * math.pi * 10 * t), n) * env(n, 0.02, 0.4) * 0.04, 0.45)
    poe(x, satura(_piu(500, 380, 0.3, 0.08), 2), 1.1)
    return reverb(x, 0.4, 0.2)


def furacao(rng, v):
    """Taz: o furacão (o vento girando rápido e os rosnados)."""
    x = _z(1.9)
    n = n_de(1.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 15 * t) ** 2) * sobe_e_some(n, 0.3, 1.1) * 0.55, 0.0)
    for k in range(4):
        m = n_de(0.12)
        poe(x, satura(seno(varre(200, 140, m), m) + passa(rosa(rng, m), 200, 1500, 2) * 0.6, 3) * env(m, 0.01, 0.08) * 0.08, 0.2 + 0.25 * k)
    return reverb(x, 0.4, 0.2)


def acme(rng, v):
    """Coiote: o assobio da bigorna caindo e a pancada no chão."""
    x = _z(2.0)
    poe(x, _piu(2200, 600, 0.9, 0.05), 0.0)
    poe(x, _sino(rng, 260, 0.9, 0.16, METAL), 0.92)
    poe(x, _baque(70, 30, 0.6, 1.0, 2.6), 0.92)
    poe(x, _sopro(rng, 0.7, 150, 2000, 0.35, 0.1), 0.93)
    return reverb(x, 0.5, 0.25)


def poeira(rng, v):
    """Papa-Léguas: o "bip bip!" e a corrida que levanta a poeira."""
    x = _z(1.9)
    for k in range(2):
        m = n_de(0.12)
        poe(x, (seno(1100, m) + seno(1650, m) * 0.5) * env(m, 0.005, 0.09) * 0.06, 0.05 + 0.18 * k)
    poe(x, _whoosh(rng, 0.3, 500, 8000, 0.5, 1.3, 0.8), 0.45)
    poe(x, _sopro(rng, 1.0, 150, 2500, 0.3, 0.2), 0.5)
    return reverb(x, 0.4, 0.2)


def kaboom(rng, v):
    """Marvin: o Modulador carregando (o tom espacial) e o KABOOM que sacode a terra."""
    x = _z(2.4)
    n = n_de(0.9)
    poe(x, seno(varre(300, 1500, n, 1.3) * (1 + 0.03 * np.sin(2 * math.pi * 30 * _t(n))), n) * sobe_e_some(n, 0.95, 1.0) * 0.05, 0.0)
    poe(x, _explosao(rng, 1.0, 40), 0.9)
    k = n_de(1.4)
    poe(x, passa(rosa(rng, k), 25, 400, 2) * env(k, 0.01, 0.8) * 0.7, 0.9)
    return reverb(x, 0.8, 0.4)


def achatado(rng, v):
    """Tom: a frigideira acertando (o "BLONG" metálico), as estrelinhas e o achatado."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 500, 3000, 0.7, 1.4, 0.35), 0.0)
    poe(x, _sino(rng, 500, 1.0, 0.18, METAL), 0.3)
    poe(x, _baque(150, 70, 0.2, 0.5), 0.3)
    for k in range(5):
        poe(x, _sino(rng, 2400 + 200 * (k % 3), 0.25, 0.025, CRISTAL), 0.7 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def tombo(rng, v):
    """Jerry: a mordiscada no queijo, a marreta subindo e a pancada no grandão."""
    x = _z(1.9)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006) * 0.4, 0.05 + 0.08 * k)
    poe(x, _whoosh(rng, 0.3, 400, 3000, 0.8, 1.4, 0.4), 0.55)
    poe(x, _baque(110, 45, 0.5, 1.0, 2.6), 0.95)
    poe(x, _sino(rng, 700, 0.6, 0.06, METAL), 0.95)
    return reverb(x, 0.4, 0.2)


def diamante(rng, v):
    """Pantera Cor-de-Rosa: os passos de mansinho (o jazz baixinho) e o brilho do diamante."""
    x = _z(2.0)
    for k, f in enumerate((233, 262, 233, 277, 233, 311)):
        m = n_de(0.15)
        poe(x, (seno(f, m) + seno(f * 2, m) * 0.3) * env(m, 0.01, 0.1) * 0.05, 0.05 + 0.16 * k)
        poe(x, _baque(300, 180, 0.05, 0.08, 1.2), 0.05 + 0.16 * k)
    poe(x, _brilho(rng, 0.8, 2637, 0.05, CRISTAL), 1.0)
    return reverb(x, 0.5, 0.25)


def garras_aco(rng, v):
    """Shredder: as três garras de aço cortando (o metal raspando) e o sangue."""
    x = _z(1.8)
    for k in range(3):
        poe(x, _whoosh(rng, 0.15, 1500, 9000, 0.4, 1.4, 0.5), 0.05 + 0.07 * k)
        poe(x, _sino(rng, 2200 + 300 * k, 0.4, 0.05, METAL), 0.15 + 0.07 * k)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * env(m, 0.01, 0.3) * 0.3, 0.6)
    return reverb(x, 0.5, 0.25)


def contra_golpe(rng, v):
    """Splinter: o bastão girando, o aparo (o toque de madeira) e o contra-golpe."""
    x = _z(1.8)
    for k in range(5):
        poe(x, _whoosh(rng, 0.1, 800, 4000, 0.5, 1.4, 0.3), 0.05 * k)
    poe(x, (seno(420, n_de(0.15)) * 0.5 + passa(rosa(rng, n_de(0.15)), 500, 3000, 2)) * env(n_de(0.15), 0.001, 0.05) * 0.6, 0.65)
    poe(x, _baque(140, 60, 0.4, 0.8, 2.4), 1.0)
    return reverb(x, 0.4, 0.2)


def android(rng, v):
    """Krang: o cérebro gorgolejando na cúpula e a voz robótica (o bipe que treme)."""
    x = _z(1.9)
    for k in range(6):
        m = n_de(0.15)
        f = 200 + 40 * k
        poe(x, seno(varre(f, f * 1.6, m), m) * env(m, 0.01, 0.1) * 0.04, 0.05 + 0.1 * k)
    n = n_de(0.7)
    t = _t(n)
    poe(x, _quadrada(180 + 40 * np.sin(2 * math.pi * 8 * t), n) * env(n, 0.02, 0.5) * 0.02, 0.8)
    return reverb(x, 0.4, 0.2)


def goool(rng, v):
    """Casey Jones: o taco batendo no disco (o estalo seco) e o disco voando até o alvo."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 400, 3000, 0.8, 1.4, 0.4), 0.0)
    poe(x, (passa(rosa(rng, n_de(0.08)), 1000, 6000, 2) + seno(800, n_de(0.08)) * 0.5) * env(n_de(0.08), 0.0005, 0.03) * 0.8, 0.3)
    poe(x, _whoosh(rng, 0.25, 1500, 7000, 0.5, 1.3, 0.4), 0.32)
    poe(x, _baque(150, 70, 0.3, 0.7, 2.2), 0.62)
    return reverb(x, 0.4, 0.2)


def desprevenido(rng, v):
    """Bebop: o ronco do javali, a investida (os passos pesados) e a trombada."""
    x = _z(1.8)
    n = n_de(0.4)
    t = _t(n)
    poe(x, satura(seno(110 + 20 * np.sin(2 * math.pi * 30 * t), n) + passa(rosa(rng, n), 100, 1000, 2) * 0.7, 3) * env(n, 0.02, 0.25) * 0.14, 0.0)
    for k in range(4):
        poe(x, _baque(90, 50, 0.15, 0.4, 2.0), 0.15 + 0.08 * k)
    poe(x, _baque(80, 35, 0.5, 1.0, 2.8), 0.5)
    return reverb(x, 0.4, 0.2)


def nyeh(rng, v):
    """Esqueleto: o "Nyeh!" (o tom fino e irritado), o cajado acendendo e os raios."""
    x = _z(1.9)
    n = n_de(0.35)
    poe(x, satura(seno(varre(700, 900, n), n) + seno(varre(1400, 1800, n), n) * 0.3, 2) * env(n, 0.01, 0.25) * 0.04, 0.0)
    m = n_de(1.0)
    poe(x, (seno(98, m) + seno(147, m) * 0.5) * sobe_e_some(m, 0.4, 1.2) * 0.06, 0.3)
    poe(x, graos(rng, m, 70, 0.1, 0.9, 2500, 10000, 0.002) * 0.4, 0.4)
    return reverb(x, 0.6, 0.3)


def espada_muda(rng, v):
    """She-Ra: a espada mudando de forma três vezes (o brilho que sobe a cada troca)."""
    x = _z(2.0)
    for k, (f, mat) in enumerate(((1047, METAL), (784, METAL), (1319, CRISTAL))):
        poe(x, _sino(rng, f, 0.5, 0.06, mat), 0.1 + 0.5 * k)
        poe(x, _sopro(rng, 0.3, 2000, 8000, 0.15, 0.6), 0.0 + 0.5 * k)
    poe(x, _acorde((523, 659, 784, 1047), 0.8, 0.04, 0.02, 0.5), 1.15)
    return reverb(x, 0.6, 0.3)


def instinto(rng, v):
    """Lion-O: o rugido do Olho de Thundera e o sinal (o acorde heroico)."""
    x = _z(2.0)
    n = n_de(0.7)
    t = _t(n)
    poe(x, satura(seno(varre(160, 110, n) * (1 + 0.06 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 150, 2000, 2) * 0.7, 3) * env(n, 0.03, 0.4) * 0.15, 0.0)
    poe(x, _acorde((196, 247, 294, 392), 1.2, 0.05, 0.03, 0.7), 0.6)
    poe(x, _brilho(rng, 0.6, 1568, 0.04, CRISTAL), 0.62)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "mu-desastrado": (desastrado, "Pateta: o tombo"),
    "mu-destruir": (destruir, "Stitch: destruir tudo"),
    "mu-infinito": (infinito, "Buzz: ao infinito"),
    "mu-cordinha": (cordinha, "Woody: a cordinha"),
    "mu-arremesso-carro": (arremesso_carro, "Sr. Incrível: o carro"),
    "mu-estica": (estica, "Mulher-Elástica: o corpo que estica"),
    "mu-estado-avatar": (estado_avatar, "Korra: o Estado Avatar"),
    "mu-redirecionado": (redirecionado, "Zuko: o raio redirecionado"),
    "mu-terremoto": (terremoto, "Toph: o terremoto"),
    "mu-dragao-oeste": (dragao_oeste, "Iroh: o Dragão do Oeste"),
    "mu-temporada": (temporada, "Patolino: o tiro"),
    "mu-furacao": (furacao, "Taz: o furacão"),
    "mu-acme": (acme, "Coiote: a bigorna"),
    "mu-poeira": (poeira, "Papa-Léguas: bip bip"),
    "mu-kaboom": (kaboom, "Marvin: o KABOOM"),
    "mu-achatado": (achatado, "Tom: a frigideira"),
    "mu-tombo": (tombo, "Jerry: a marreta"),
    "mu-diamante": (diamante, "Pantera Cor-de-Rosa: o diamante"),
    "mu-garras-aco": (garras_aco, "Shredder: as garras"),
    "mu-contra-golpe": (contra_golpe, "Splinter: o contra-golpe"),
    "mu-android": (android, "Krang: o cérebro"),
    "mu-goool": (goool, "Casey Jones: o taco"),
    "mu-desprevenido": (desprevenido, "Bebop: a investida"),
    "mu-nyeh": (nyeh, "Esqueleto: Nyeh!"),
    "mu-espada-muda": (espada_muda, "She-Ra: a espada que muda"),
    "mu-instinto": (instinto, "Lion-O: o Olho de Thundera"),
}
