"""Os sons da rodada 17: Groot, Rocket Raccoon, Aquaman, Lanterna Verde e Ciborgue (veja
tools/vfx/familias_v2/rodada17.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _psi
from sfx_rodada15 import _laser
from sfx_rodada16 import _bipes, _explosao, _servo
from som import CRISTAL, METAL, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _madeira(rng, seg, g=0.3):
    """A madeira rangendo e estalando enquanto cresce: o ranger grave que oscila e os estalos secos."""
    n = n_de(seg)
    t = _t(n)
    x = passa(rosa(rng, n), 150, 900, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * (3 + 4 * t / seg) * t))) * 0.7
    x += graos(rng, n, int(seg * 25), 0.0, seg, 600, 3000, 0.01) * 0.6
    return x * sobe_e_some(n, 0.4, 1.2) * g


def _agua(rng, seg, g=0.3, lo=200, hi=4000):
    """A água correndo: o ruído que borbulha com os respingos."""
    n = n_de(seg)
    t = _t(n)
    x = passa(rosa(rng, n), lo, hi, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t + rng.uniform(0, 6)))
    x += graos(rng, n, int(seg * 30), 0.0, seg, 1500, 6000, 0.004) * 0.4
    return x * sobe_e_some(n, 0.4, 1.2) * g


def _construto(n, f, g=0.05):
    """O zumbido verde do anel: o tom firme com o brilho que pulsa."""
    t = _t(n)
    return (seno(f, n) + seno(f * 1.5, n) * 0.4 + seno(f * 2, n) * 0.2) * (0.8 + 0.2 * np.sin(2 * math.pi * 7 * t)) * g


# =================================================================== Groot
def muralha_de_galhos(rng, v):
    """A muralha de galhos: a madeira crescendo e rangendo, as folhas farfalhando e os espinhos saindo."""
    x = _z(1.5)
    poe(x, _madeira(rng, 0.6, 0.45), 0.0)
    poe(x, passa(rosa(rng, n_de(0.4)), 2500, 8000, 2) * sobe_e_some(n_de(0.4), 0.5, 1.3) * 0.12, 0.3)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 2000, 7000, 0.004) * 0.3, 0.5 + 0.04 * k)
    return reverb(x, 0.5, 0.25)


def eu_sou_groot(rng, v):
    """Eu sou Groot: a voz grave e calma ("Eu sou Groot" em três sílabas), as raízes correndo e as flores abrindo."""
    x = _z(1.8)
    for k, (f0, f1) in enumerate(((120, 115), (130, 125), (110, 100))):
        m = n_de(0.18 + 0.05 * k)
        poe(x, passa(satura(seno(varre(f0, f1, m, 1.0) * (1 + 0.03 * np.sin(2 * math.pi * 5 * _t(m))), m), 1.6), None, 1500, 2) * env(m, 0.03, 0.1) * 0.12, 0.02 + 0.2 * k)
    poe(x, _madeira(rng, 0.5, 0.25), 0.3)
    for k in range(3):
        poe(x, _brilho(rng, 0.5, 1047 * (1.12 ** k), 0.04, CRISTAL), 0.55 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def groot_preparo(rng, v):
    """O Preparo das Raízes de captura: as raízes se espalhando debaixo da terra (o ronco e os estalos)."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 40, 300, 2) * sobe_e_some(n, 0.3, 1.0) * 0.4, 0.0)
    poe(x, _madeira(rng, 1.2, 0.2), 0.1)
    return reverb(x, 0.5, 0.25)


def raizes_de_captura(rng, v):
    """As raízes de captura: o chão rachando, as raízes rompendo e enlaçando (o ranger que aperta)."""
    x = _z(1.6)
    poe(x, satura(baque(n_de(0.5), 70, 30, 0.15, 1.0), 1.6) * 0.6 + graos(rng, n_de(0.5), 30, 0.0, 0.3, 400, 3000, 0.01) * 0.5, 0.0)
    poe(x, _madeira(rng, 0.7, 0.5), 0.15)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 200, 1200, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * _t(m))) * env(m, 0.02, 0.25) * 0.3, 0.45)
    return reverb(x, 0.5, 0.25)


# =================================================================== Rocket Raccoon
def armadilha_explosiva(rng, v):
    """A armadilha explosiva: a mina caindo e rolando, os bipes cada vez mais rápidos e a explosão de fumaça."""
    x = _z(1.8)
    poe(x, modal(n_de(0.15), 1200, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.2, 0.05)
    for k in range(3):
        poe(x, _tic(rng), 0.12 + 0.05 * k)
    t0, passo = 0.2, 0.08
    while t0 < 0.44:
        poe(x, seno(2000, n_de(0.025)) * env(n_de(0.025), 0.001, 0.015) * 0.07, t0)
        t0 += passo
        passo = max(0.02, passo * 0.75)
    poe(x, _explosao(rng, 0.6, 80), 0.45)
    poe(x, passa(rosa(rng, n_de(0.6)), 400, 3000, 2) * sobe_e_some(n_de(0.6), 0.2, 1.3) * 0.25, 0.5)
    return reverb(x, 0.5, 0.25)


def _tic(rng):
    return modal(n_de(0.06), 900, rng=rng, **METAL) * env(n_de(0.06), 0.0005, 0.02) * 0.1


def missil_caseiro(rng, v):
    """O míssil caseiro: o motor tossindo (o chiado que falha) em zigue-zague e a explosão."""
    x = _z(1.8)
    n = n_de(0.45)
    falha = 0.6 + 0.4 * (np.sin(2 * math.pi * 11 * _t(n)) > -0.3)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * falha * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.05)
    poe(x, seno(varre(400, 900, n, 1.0) * (1 + 0.08 * np.sin(2 * math.pi * 3 * _t(n))), n) * sobe_e_some(n, 0.3, 1.2) * 0.04, 0.05)
    poe(x, _explosao(rng, 0.8, 60), 0.42)
    return reverb(x, 0.5, 0.25)


def rocket_preparo(rng, v):
    """O Preparo do Arsenal pesado: as peças encaixando (os "clack" metálicos) e a carga subindo."""
    x = _z(1.4)
    for k in range(5):
        poe(x, modal(n_de(0.12), 1400 - 120 * k, rng=rng, **METAL) * env(n_de(0.12), 0.0005, 0.04) * 0.2 + estalo(rng, n_de(0.12), 1000, 5000, 0.006) * 0.3, 0.05 + 0.1 * k)
    poe(x, _servo(rng, 0.7, 200, 800, 0.05), 0.6)
    return reverb(x, 0.4, 0.2)


# =================================================================== Aquaman
def mare_puxante(rng, v):
    """A maré puxante: a onda subindo, a água puxando para trás (o ruído que se afasta) e as bolhas fechando."""
    x = _z(1.8)
    poe(x, _agua(rng, 0.9, 0.5, 100, 3000), 0.0)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * np.linspace(1, 0, m) * 0.3, 0.3)
    for k in range(3):
        poe(x, seno(varre(500 + 80 * k, 900 + 80 * k, n_de(0.08), 1.0), n_de(0.08)) * env(n_de(0.08), 0.003, 0.05) * 0.06, 0.55 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def aquaman_preparo(rng, v):
    """O Preparo do Comando dos mares: a água girando em volta do tridente e o canto grave do mar."""
    x = _z(1.4)
    poe(x, _agua(rng, 1.4, 0.3, 150, 2500), 0.0)
    n = n_de(1.4)
    poe(x, (seno(98, n) + seno(147, n) * 0.6) * sobe_e_some(n, 0.3, 1.0) * 0.05, 0.0)
    return reverb(x, 0.7, 0.35)


def comando_dos_mares(rng, v):
    """O comando dos mares: a onda gigante subindo (o ronco que cresce), quebrando (o estrondo) e a espuma."""
    x = _z(2.2)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 60, 1500, 2) * sobe_e_some(n, 0.9, 1.1) * 0.6, 0.0)
    poe(x, satura(baque(n_de(1.0), 45, 22, 0.35, 1.0), 1.6) * 0.9, 0.5)
    poe(x, _agua(rng, 1.0, 0.7, 200, 6000), 0.5)
    poe(x, graos(rng, n_de(0.8), 60, 0.0, 0.7, 2000, 8000, 0.004) * 0.4, 0.6)
    return reverb(x, 0.8, 0.4)


# =================================================================== Lanterna Verde
def escudo_de_vontade(rng, v):
    """O escudo de vontade: o anel acendendo, o construto se montando (o zumbido que sobe) e a placa fechando."""
    x = _z(1.5)
    poe(x, _brilho(rng, 0.4, 1568, 0.05, CRISTAL), 0.0)
    n = n_de(0.5)
    poe(x, _construto(n, 330, 0.06) * sobe_e_some(n, 0.7, 1.2), 0.1)
    poe(x, modal(n_de(0.6), 660, rng=rng, **CRISTAL) * env(n_de(0.6), 0.002, 0.3) * 0.15, 0.45)
    return reverb(x, 0.6, 0.3)


def punho_esmeralda(rng, v):
    """O punho esmeralda: o zumbido do construto voando, o soco e as barras da jaula fechando (os "tchang")."""
    x = _z(1.6)
    n = n_de(0.35)
    poe(x, _construto(n, 220, 0.06) * sobe_e_some(n, 0.8, 1.1), 0.0)
    poe(x, _whoosh(rng, 0.25, 300, 1500, 0.85, 1.3, 0.4), 0.05)
    poe(x, satura(baque(n_de(0.4), 90, 45, 0.1, 1.0), 1.6) * 0.8, 0.3)
    for k in range(4):
        poe(x, modal(n_de(0.3), 880 + 60 * k, rng=rng, **CRISTAL) * env(n_de(0.3), 0.001, 0.12) * 0.08, 0.4 + 0.04 * k)
    return reverb(x, 0.5, 0.25)


def lanterna_preparo(rng, v):
    """O Preparo do Construto adaptável: a lanterna zumbindo (o juramento em tom grave) e o anel carregando."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, _construto(n, 165, 0.05) * sobe_e_some(n, 0.3, 1.0), 0.0)
    poe(x, _construto(n_de(1.0), 330, 0.03) * sobe_e_some(n_de(1.0), 0.9, 1.0), 0.3)
    return reverb(x, 0.6, 0.3)


def construto_adaptavel(rng, v):
    """O construto adaptável: as três formas trocando (os "vuum" que mudam de tom), o míssil indo e o impacto."""
    x = _z(1.6)
    for k, f in enumerate((220, 330, 440)):
        m = n_de(0.15)
        poe(x, _construto(m, f, 0.05) * env(m, 0.01, 0.1), 0.02 + 0.15 * k)
    poe(x, _whoosh(rng, 0.2, 500, 2500, 0.85, 1.3, 0.4), 0.32)
    poe(x, satura(baque(n_de(0.5), 80, 35, 0.15, 1.0), 1.6) * 0.8, 0.48)
    poe(x, _brilho(rng, 0.5, 1319, 0.05, CRISTAL), 0.5)
    return reverb(x, 0.5, 0.25)


# =================================================================== Ciborgue
def varredura_tatica(rng, v):
    """A varredura tática: o olho ligando, a varredura (o tom que passa) com os bipes de dados e a trava."""
    x = _z(1.4)
    poe(x, seno(varre(300, 1200, n_de(0.2), 1.0), n_de(0.2)) * env(n_de(0.2), 0.005, 0.15) * 0.05, 0.0)
    m = n_de(0.45)
    poe(x, seno(900 + 400 * np.sin(2 * math.pi * 2 * _t(m)), m) * sobe_e_some(m, 0.3, 1.3) * 0.03, 0.1)
    poe(x, _bipes(1800, 6, 0.05, 0.04), 0.25)
    poe(x, modal(n_de(0.15), 2000, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.25, 0.5)
    return reverb(x, 0.4, 0.2)


def ciborgue_preparo(rng, v):
    """O Preparo da Adaptação de sistema: o braço transformando (os servos e os encaixes) e a carga zumbindo."""
    x = _z(1.4)
    poe(x, _servo(rng, 0.5, 300, 700, 0.05), 0.0)
    for k in range(3):
        poe(x, modal(n_de(0.1), 1500, rng=rng, **METAL) * env(n_de(0.1), 0.0005, 0.03) * 0.15, 0.2 + 0.15 * k)
    n = n_de(0.8)
    poe(x, seno(varre(200, 900, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.5)
    return reverb(x, 0.4, 0.2)


def adaptacao_de_sistema(rng, v):
    """A adaptação de sistema: o pulso de interferência (o "vuuum" que distorce), a estática do Preparo travando e
    o raio de energia."""
    x = _z(1.6)
    n = n_de(0.35)
    poe(x, satura(_psi(n, 150, 90, 0.2), 2.0) * env(n, 0.01, 0.2) * 0.5, 0.0)
    m = n_de(0.35)
    poe(x, passa(rosa(rng, m), 1000, 9000, 2) * (np.sin(2 * math.pi * 31 * _t(m)) > 0) * sobe_e_some(m, 0.3, 1.2) * 0.3, 0.25)
    poe(x, _laser(rng, 0.35, 1400, 600, 0.15), 0.45)
    poe(x, satura(baque(n_de(0.4), 100, 50, 0.1, 1.0), 1.6) * 0.6, 0.55)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "muralha-de-galhos": (muralha_de_galhos, "Groot: a madeira crescendo e os espinhos"),
    "eu-sou-groot": (eu_sou_groot, "Groot: a voz e as raízes"),
    "groot-preparo": (groot_preparo, "Groot: as raízes debaixo da terra (antes do golpe)"),
    "raizes-de-captura": (raizes_de_captura, "Groot: o chão rachando e as raízes apertando"),
    "armadilha-explosiva": (armadilha_explosiva, "Rocket: os bipes e a explosão"),
    "missil-caseiro": (missil_caseiro, "Rocket: o motor tossindo e a explosão"),
    "rocket-preparo": (rocket_preparo, "Rocket: as peças encaixando (antes do golpe)"),
    "mare-puxante": (mare_puxante, "Aquaman: a onda e as bolhas"),
    "aquaman-preparo": (aquaman_preparo, "Aquaman: a água girando (antes do golpe)"),
    "comando-dos-mares": (comando_dos_mares, "Aquaman: a onda gigante quebrando"),
    "escudo-de-vontade": (escudo_de_vontade, "Lanterna Verde: o anel e o construto"),
    "punho-esmeralda": (punho_esmeralda, "Lanterna Verde: o soco e a jaula"),
    "lanterna-preparo": (lanterna_preparo, "Lanterna Verde: a lanterna zumbindo (antes do golpe)"),
    "construto-adaptavel": (construto_adaptavel, "Lanterna Verde: as formas e o impacto"),
    "varredura-tatica": (varredura_tatica, "Ciborgue: a varredura e os dados"),
    "ciborgue-preparo": (ciborgue_preparo, "Ciborgue: o braço virando canhão (antes do golpe)"),
    "adaptacao-de-sistema": (adaptacao_de_sistema, "Ciborgue: a interferência e o raio"),
}
