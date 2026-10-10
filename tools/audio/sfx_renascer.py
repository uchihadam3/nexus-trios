"""Os sons do Renascer de cada um (veja tools/vfx/familias_v2/renascer_proprio.py).

espera-<id>: logo depois do nocaute, baixinho (o caído esperando);
volta-<id>: a volta, no volume dos golpes.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _coro(f0, seg, notas=(1, 1.5, 2.0), g=0.1, vib=4.0):
    n = n_de(seg)
    t = _t(n)
    x = np.zeros(n)
    for k, r in enumerate(notas):
        f = f0 * r
        x += (seno(f * (1 + 0.004 * np.sin(2 * math.pi * (vib + k) * t)), n) + seno(f * 1.003, n) * 0.6) * g / (1 + k * 0.4)
    return x * sobe_e_some(n, 0.5, 1.4)


def _grito_de_ave(seg=0.5, f0=1900, f1=1300, g=0.12):
    """O grito da ave (a Fênix): agudo, com vibrato rápido, descendo."""
    n = n_de(seg)
    t = _t(n)
    f = varre(f0, f1, n, 0.8) * (1 + 0.03 * np.sin(2 * math.pi * 28 * t))
    return (seno(f, n) + seno(f * 2, n) * 0.35 + seno(f * 3, n) * 0.12) * env(n, 0.02, seg * 0.7) * g


def _asa(rng, g=0.4):
    n = n_de(0.18)
    return passa(rosa(rng, n), 150, 1500, 2) * sobe_e_some(n, 0.35, 1.5) * g


def _bolha(f=500, g=0.15):
    n = n_de(0.07)
    return seno(varre(f, f * 2.2, n, 0.6), n) * env(n, 0.002, 0.05) * g


def _gosma(rng, g=0.3):
    """O "splorch" molhado: ruído grave filtrado com um tom que desce."""
    n = n_de(0.16)
    return (passa(rosa(rng, n), 100, 900, 2) * 0.7 + seno(varre(300, 90, n, 1.0), n) * 0.5) * env(n, 0.004, 0.12) * g


def _pulsacao(rng, g=0.4):
    """Um batimento: tum-tum grave."""
    x = _z(0.45)
    poe(x, baque(n_de(0.18), 70, 40, 0.09, 0.1) * g, 0.0)
    poe(x, baque(n_de(0.18), 62, 36, 0.09, 0.1) * g * 0.7, 0.2)
    return x


# =================================================================== Ikki
def espera_ikki(rng, v):
    """As cinzas: o crepitar fraco das brasas e o fogo respirando grave por baixo."""
    x = _z(1.6)
    n = n_de(1.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 80, 700, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.8 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.0)
    poe(x, graos(rng, n, 22, 0.0, 1.4, 1800, 6000, 0.004, 0.7) * 0.5, 0.0)
    return reverb(x, 0.4, 0.2)


def volta_ikki(rng, v):
    """A Ave Fênix: as brasas sugadas para dentro, a coluna de fogo rugindo para cima, o grito da
    ave e as asas batendo uma vez."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.45, 300, 1500, 0.9, 1.2, 0.5), 0.0)
    poe(x, B.fogo(rng, v)[: n_de(1.2)] * 0.75, 0.35)
    poe(x, baque(n_de(0.5), 75, 40, 0.25, 0.3) * 0.7, 0.35)
    poe(x, _grito_de_ave(0.7, 2000, 1250, 0.16), 0.6)
    poe(x, _asa(rng, 0.5), 1.0)
    return reverb(x, 0.65, 0.35)


# =================================================================== Jean Grey
def espera_jeangrey(rng, v):
    """O halo telecinético: um zumbido brilhante que gira (vibrato lento) e estrelinhas pingando."""
    x = _z(1.6)
    n = n_de(1.5)
    t = _t(n)
    poe(x, (seno(440 * (1 + 0.01 * np.sin(2 * math.pi * 1.5 * t)), n) * 0.06 + seno(660, n) * 0.04) * sobe_e_some(n, 0.5, 1.2), 0.0)
    for k in range(5):
        poe(x, _brilho(rng, 0.25, 1800 + 300 * k, 0.05), 0.15 + 0.25 * k)
    return reverb(x, 0.7, 0.4)


def volta_jeangrey(rng, v):
    """A Força Fênix: o coro subindo, o estouro de fogo cósmico, o grito da ave longo e o brilho de
    estrelas espalhando."""
    x = _z(2.4)
    poe(x, _coro(220, 1.2, (1, 1.25, 1.5, 2.0), 0.09), 0.0)
    poe(x, B.fogo(rng, v)[: n_de(1.1)] * 0.7, 0.5)
    poe(x, baque(n_de(0.7), 60, 30, 0.35, 0.3) * 0.75, 0.5)
    poe(x, _grito_de_ave(0.9, 2300, 1400, 0.15), 0.7)
    for k in range(8):
        poe(x, _brilho(rng, 0.3, 2200 + 250 * k, 0.05), 0.6 + 0.08 * k)
    return reverb(x, 0.8, 0.4)


# =================================================================== Deadpool
def espera_deadpool(rng, v):
    """Os pedaços se regenerando: os "squish" molhados aqui e ali e um assobio distraído de três
    notas (ele está entediado esperando)."""
    x = _z(1.6)
    for k in range(5):
        poe(x, _gosma(rng, 0.18), 0.05 + 0.27 * k)
    for k, f in enumerate((880, 990, 784)):
        n = n_de(0.18)
        poe(x, seno(f * (1 + 0.01 * np.sin(2 * math.pi * 6 * _t(n))), n) * env(n, 0.02, 0.15) * 0.05, 0.6 + 0.2 * k)
    return reverb(x, 0.3, 0.15)


def volta_deadpool(rng, v):
    """Deadpool volta: os pedaços grudando (squish, squish, squish, cada vez mais rápido), o "boing"
    de desenho e as duas katanas saindo da bainha (shing, shing)."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _gosma(rng, 0.3), 0.32 * (1 - (1 - k / 6) ** 1.6))
    n = n_de(0.4)
    poe(x, seno(varre(180, 520, n, 0.5) * (1 + 0.08 * np.sin(2 * math.pi * 18 * _t(n))), n) * env(n, 0.005, 0.35) * 0.18, 0.4)
    for k in range(2):
        m = n_de(0.45)
        sh = passa(rosa(rng, m), 3000, 9000, 2) * env(m, 0.005, 0.3) * 0.3 + modal(m, 2400 + 300 * k, rng=rng, **METAL) * env(m, 0.001, 0.4) * 0.12
        poe(x, sh, 0.85 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


# =================================================================== Majin Boo
def espera_majinbuu(rng, v):
    """A poça de gosma: bolhas estourando moles, uma atrás da outra, e o chiado fino do vapor."""
    x = _z(1.6)
    for k in range(9):
        poe(x, _bolha(260 + 60 * (k % 4), 0.14), 0.05 + 0.16 * k)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * sobe_e_some(n, 0.5, 1.4) * 0.05, 0.1)
    return reverb(x, 0.3, 0.15)


def volta_majinbuu(rng, v):
    """Majin Boo se refaz: as gotas vindo de todos os lados (splorch, splorch…), a gosma esticando
    (o "bóóing" elástico que sobe) e o vapor saindo dos furos com o apito de chaleira."""
    x = _z(2.2)
    for k in range(7):
        poe(x, _gosma(rng, 0.28), 0.04 * k + 0.02 * (k % 3))
    n = n_de(0.5)
    poe(x, seno(varre(120, 360, n, 0.7) * (1 + 0.1 * np.sin(2 * math.pi * 12 * _t(n))), n) * env(n, 0.01, 0.45) * 0.22, 0.35)
    m = n_de(1.0)
    poe(x, passa(rosa(rng, m), 2500, 9000, 2) * sobe_e_some(m, 0.15, 1.2) * 0.35, 0.95)
    poe(x, seno(2100 * (1 + 0.006 * np.sin(2 * math.pi * 7 * _t(m))), m) * sobe_e_some(m, 0.2, 1.5) * 0.06, 0.95)
    return reverb(x, 0.5, 0.25)


# =================================================================== Mumm-Ra
def espera_mummra(rng, v):
    """O sarcófago: o zumbido grave e escuro lá de dentro e os sussurros dos espíritos (ruído que
    sobe e desce como vozes)."""
    x = _z(1.6)
    n = n_de(1.5)
    t = _t(n)
    poe(x, (seno(55, n) * 0.18 + seno(58.3, n) * 0.12) * sobe_e_some(n, 0.5, 1.2), 0.0)
    sus = passa(rosa(rng, n), 900, 3500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3.3 * t) * np.sin(2 * math.pi * 0.7 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.12
    poe(x, sus, 0.0)
    return reverb(x, 0.75, 0.4, 3500)


def volta_mummra(rng, v):
    """"Antigos espíritos do mal…": o arrastar de pedra da tampa abrindo, o coro grave e sombrio, o
    trovão e as faixas voando (vuush)."""
    x = _z(2.4)
    n = n_de(0.7)
    poe(x, satura(passa(rosa(rng, n), 50, 500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 23 * _t(n))), 2.2) * sobe_e_some(n, 0.6, 1.2) * 0.4, 0.0)
    poe(x, _coro(73.4, 1.6, (1, 1.19, 1.5), 0.12, 3.0), 0.3)
    poe(x, baque(n_de(0.9), 55, 28, 0.5, 0.5) * 0.85, 0.55)
    poe(x, passa(rosa(rng, n_de(1.0)), 40, 1200, 2) * env(n_de(1.0), 0.01, 0.8) * 0.35, 0.55)
    for k in range(3):
        poe(x, _whoosh(rng, 0.35, 400, 1800, 0.6, 1.4, 0.3), 0.7 + 0.08 * k)
    return reverb(x, 0.8, 0.45, 4000)


# =================================================================== Cell
def espera_cell(rng, v):
    """Uma célula viva: o pulso orgânico (tum… tum…) e um borbulhar baixinho de bio-energia."""
    x = _z(1.6)
    poe(x, _pulsacao(rng, 0.35), 0.0)
    poe(x, _pulsacao(rng, 0.3), 0.8)
    for k in range(6):
        poe(x, _bolha(700 + 90 * k, 0.06), 0.1 + 0.22 * k)
    return reverb(x, 0.35, 0.2)


def volta_cell(rng, v):
    """Cell se refaz: as divisões estalando cada vez mais rápido (pop… pop pop… pop-pop-pop-pop), o
    clarão e a aura rugindo verde."""
    x = _z(2.2)
    tempos = [0.0, 0.18, 0.3, 0.38, 0.44, 0.49, 0.53, 0.56, 0.59, 0.62]
    for k, e in enumerate(tempos):
        poe(x, _bolha(500 + 60 * k, 0.16), e)
    poe(x, baque(n_de(0.6), 80, 40, 0.3, 0.4) * 0.75, 0.68)
    n = n_de(1.2)
    poe(x, satura(passa(rosa(rng, n), 70, 1400, 2), 2) * sobe_e_some(n, 0.25, 1.3) * 0.4, 0.68)
    poe(x, seno(varre(110, 165, n, 1.0), n) * sobe_e_some(n, 0.3, 1.3) * 0.12, 0.68)
    return reverb(x, 0.6, 0.3)


# =================================================================== Mario
_DO = 523.25


def _quadrada(f, seg, g=0.08):
    """A onda de videogame (quadrada suave, só harmônicos ímpares)."""
    n = n_de(seg)
    x = np.zeros(n)
    for h in (1, 3, 5, 7):
        x += seno(f * h, n) / h
    return x * env(n, 0.003, seg * 0.8) * g


def espera_mario(rng, v):
    """O cogumelo pulando: um "plim" de videogame a cada quique (duas notas curtas), bem baixinho."""
    x = _z(1.6)
    for k in range(3):
        poe(x, _quadrada(_DO * 1.5, 0.08, 0.06), 0.1 + 0.5 * k)
        poe(x, _quadrada(_DO * 2, 0.1, 0.05), 0.18 + 0.5 * k)
    return reverb(x, 0.3, 0.15)


def volta_mario(rng, v):
    """A vida a mais: o arpejo subindo em notas de videogame (dó, mi, sol, dó, mi, sol), o "pop" do
    cogumelo e as moedas tilintando."""
    x = _z(2.0)
    for k, r in enumerate((1, 1.26, 1.5, 2, 2.52, 3)):
        poe(x, _quadrada(_DO * r, 0.12, 0.08), 0.07 * k)
    n = n_de(0.12)
    poe(x, seno(varre(300, 900, n, 0.6), n) * env(n, 0.002, 0.1) * 0.25, 0.5)
    for k in range(4):
        poe(x, modal(n_de(0.4), 1975 + 120 * (k % 2), rng=rng, **SINO) * env(n_de(0.4), 0.001, 0.3) * 0.08, 0.62 + 0.11 * k)
        poe(x, modal(n_de(0.4), 2637, rng=rng, **SINO) * env(n_de(0.4), 0.001, 0.3) * 0.06, 0.67 + 0.11 * k)
    return reverb(x, 0.45, 0.2)


# =================================================================== Wolverine
def espera_wolverine(rng, v):
    """A cura: o chiado do vapor saindo da pele e a respiração rosnada, funda."""
    x = _z(1.6)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.08, 0.0)
    for k in range(2):
        m = n_de(0.55)
        t = _t(m)
        rosn = satura(passa(rosa(rng, m), 60, 500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * t)), 2.5) * sobe_e_some(m, 0.5, 1.4) * 0.25
        poe(x, rosn, 0.15 + 0.7 * k)
    return reverb(x, 0.35, 0.2)


def volta_wolverine(rng, v):
    """SNIKT: o rosnado subindo, as três garras saindo de uma vez (o raspão de metal agudo e o
    tinido) e o rugido curto."""
    x = _z(1.8)
    m = n_de(0.5)
    poe(x, satura(passa(rosa(rng, m), 60, 600, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 32 * _t(m))), 2.5) * sobe_e_some(m, 0.7, 1.3) * 0.3, 0.0)
    n = n_de(0.25)
    raspa = passa(rosa(rng, n), 2500, 11000, 2) * env(n, 0.002, 0.16) * 0.5
    poe(x, raspa, 0.42)
    for k in range(3):
        poe(x, modal(n_de(0.6), 3100 + 260 * k, rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.45) * 0.1, 0.43 + 0.012 * k)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000) * 0.5, 0.42)
    m2 = n_de(0.6)
    poe(x, satura(passa(rosa(rng, m2), 80, 1200, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 26 * _t(m2))), 3) * sobe_e_some(m2, 0.3, 1.3) * 0.35, 0.7)
    return reverb(x, 0.45, 0.25)


# =================================================================== Alucard
def espera_alucardcv(rng, v):
    """A névoa: o vento frio girando e os guinchos agudos dos morcegos, longe."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 1.4, 300, 900, 0.5, 1.3, 0.25), 0.0)
    for k in range(4):
        n = n_de(0.05)
        poe(x, seno(varre(5200, 4300, n, 1.0), n) * env(n, 0.003, 0.04) * 0.05, 0.2 + 0.31 * k)
        poe(x, seno(varre(5600, 4700, n, 1.0), n) * env(n, 0.003, 0.04) * 0.04, 0.26 + 0.31 * k)
    return reverb(x, 0.6, 0.35)


def volta_alucardcv(rng, v):
    """Alucard se refaz: o redemoinho de névoa fechando, a revoada de morcegos (dezenas de bater de
    asas) mergulhando, a capa estalando aberta e o acorde de órgão gótico, grave e menor."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.7, 1200, 250, 0.8, 1.3, 0.4), 0.0)
    for k in range(14):
        poe(x, _asa(rng, 0.18), 0.08 + 0.035 * k + 0.01 * (k % 3))
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 120, 2400, 2) * env(n, 0.003, 0.2) * 0.55, 0.62)
    m = n_de(1.4)
    org = np.zeros(m)
    for r in (1, 1.19, 1.5, 2):
        org += serra_suave(98 * r, m, 6) * 0.05
    poe(x, passa(org, None, 2500, 2) * sobe_e_some(m, 0.15, 1.4), 0.62)
    return reverb(x, 0.85, 0.45, 4000)


# =================================================================== Muzan
def espera_muzan(rng, v):
    """A carne viva: o batimento forte e molhado e o rangido úmido dos tentáculos se mexendo."""
    x = _z(1.6)
    poe(x, _pulsacao(rng, 0.45), 0.0)
    poe(x, _pulsacao(rng, 0.4), 0.75)
    for k in range(3):
        poe(x, _gosma(rng, 0.12), 0.35 + 0.4 * k)
    return reverb(x, 0.35, 0.2)


def volta_muzan(rng, v):
    """Muzan se remonta: os tentáculos chicoteando de todos os lados (vuush-tchak), a carne fechando
    (o "sllurp" grave), o rugido de demônio e os espinhos saindo (tchk-tchk)."""
    x = _z(2.2)
    for k in range(6):
        poe(x, _whoosh(rng, 0.2, 600, 2200, 0.6, 1.4, 0.3), 0.035 * k)
        poe(x, _gosma(rng, 0.25), 0.16 + 0.035 * k)
    n = n_de(0.5)
    poe(x, (passa(rosa(rng, n), 60, 700, 2) + seno(varre(160, 60, n, 1.0), n) * 0.6) * env(n, 0.01, 0.4) * 0.4, 0.42)
    m = n_de(0.8)
    poe(x, satura(passa(rosa(rng, m), 70, 1000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 22 * _t(m))), 3) * sobe_e_some(m, 0.3, 1.4) * 0.35, 0.6)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.05), 1500, 6000) * 0.35, 0.62 + 0.03 * k)
    return reverb(x, 0.55, 0.3)


# =================================================================== Pain
def espera_pain(rng, v):
    """O Rinnegan: um zumbido grave que ondula (cada onda dos anéis) e o tinido baixo das hastes de
    chakra."""
    x = _z(1.6)
    n = n_de(1.5)
    t = _t(n)
    poe(x, seno(82 * (1 + 0.02 * np.sin(2 * math.pi * 2.6 * t)), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 2.6 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.0)
    for k in range(3):
        poe(x, modal(n_de(0.5), 1400 + 180 * k, rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.35) * 0.04, 0.3 + 0.4 * k)
    return reverb(x, 0.6, 0.35)


def volta_pain(rng, v):
    """Outro corpo assume: o ar sugado para dentro (o silêncio antes), e o Shinra Tensei — a pancada
    surda e enorme que empurra tudo, com o vento rasgando para fora."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.6, 2400, 300, 0.95, 1.2, 0.45), 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(110, 165, n, 1.0), n) * sobe_e_some(n, 0.8, 1.4) * 0.12, 0.1)
    poe(x, baque(n_de(1.0), 48, 24, 0.6, 0.6) * 1.0, 0.62)
    m = n_de(1.2)
    poe(x, satura(passa(rosa(rng, m), 40, 900, 2), 2) * env(m, 0.005, 0.9) * 0.5, 0.62)
    poe(x, _whoosh(rng, 0.9, 300, 2600, 0.15, 1.2, 0.5), 0.64)
    return reverb(x, 0.85, 0.45, 3500)


SONS: dict = {
    "espera-ikki": (espera_ikki, "Ikki caído: as brasas das cinzas"),
    "volta-ikki": (volta_ikki, "Ikki volta: a Ave Fênix, o fogo e o grito"),
    "espera-jeangrey": (espera_jeangrey, "Jean caída: o halo telecinético"),
    "volta-jeangrey": (volta_jeangrey, "Jean volta: a Força Fênix"),
    "espera-deadpool": (espera_deadpool, "Deadpool caído: os pedaços se regenerando e o assobio"),
    "volta-deadpool": (volta_deadpool, "Deadpool volta: squish, boing e as katanas"),
    "espera-majinbuu": (espera_majinbuu, "Majin Boo caído: a gosma borbulhando"),
    "volta-majinbuu": (volta_majinbuu, "Majin Boo se refaz: as gotas, o boing e o vapor"),
    "espera-mummra": (espera_mummra, "Mumm-Ra caído: o sarcófago e os sussurros"),
    "volta-mummra": (volta_mummra, "Mumm-Ra volta: a tampa, o coro e o trovão"),
    "espera-cell": (espera_cell, "Cell caído: a célula pulsando"),
    "volta-cell": (volta_cell, "Cell se refaz: as divisões e a aura"),
    "espera-mario": (espera_mario, "Mario caído: o cogumelo pulando"),
    "volta-mario": (volta_mario, "Mario volta: o arpejo, o pop e as moedas"),
    "espera-wolverine": (espera_wolverine, "Wolverine caído: o vapor e o rosnado"),
    "volta-wolverine": (volta_wolverine, "Wolverine levanta: SNIKT"),
    "espera-alucardcv": (espera_alucardcv, "Alucard caído: a névoa e os morcegos"),
    "volta-alucardcv": (volta_alucardcv, "Alucard se refaz: a revoada, a capa e o órgão"),
    "espera-muzan": (espera_muzan, "Muzan caído: a carne pulsando"),
    "volta-muzan": (volta_muzan, "Muzan se remonta: os tentáculos e o rugido"),
    "espera-pain": (espera_pain, "Pain caído: o Rinnegan ondulando"),
    "volta-pain": (volta_pain, "Pain volta: o Shinra Tensei"),
}
# a espera é baixinha (como as brasas de sempre); a volta, no volume dos golpes
ALVO = {nome: (-23 if nome.startswith("espera-") else -15) for nome in SONS}
