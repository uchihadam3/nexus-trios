"""Os sons do Aiolia de Leão e do Arthas (veja tools/vfx/familias_v2/aiolia_arthas.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (CRISTAL, METAL, SR, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido,
                 satura, seno, serra_suave, sobe_e_some, varre)


def _t(n):
    return np.arange(n) / SR


def _crepita(rng, seg, g=1.0, densidade=60):
    """Muitos estalos elétricos curtos (o plasma)."""
    n = n_de(seg)
    return graos(rng, n, int(densidade * seg), 0.0, seg, 2500, 11000, 0.002, 0.8) * g


def _zumbido(rng, seg, f=110.0, g=1.0):
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.01 * np.sin(2 * math.pi * 9 * t)), n, 12) * 0.4
    return passa(z, 80, 3000, 2) * g


def _rugido_de_leao(rng, seg, g=1.0):
    """O rugido do leão: voz grave e áspera que sobe e cai, com o ar rasgado."""
    n = n_de(seg)
    t = _t(n)
    f = 80 + 60 * np.sin(math.pi * t / t[-1]) ** 0.7
    voz = serra_suave(f * (1 + 0.03 * np.sin(2 * math.pi * 6 * t)), n, 24)
    a = passa(voz, 400, 900, 2) + passa(voz, 60, 260, 2) * 0.8
    rasgo = passa(ruido(rng, n), 300, 3000, 2) * 0.45
    return satura((a + rasgo) * sobe_e_some(n, 0.35, 1.3), 2.0) * g


# =================================================================== Aiolia
def relampago_de_plasma(rng, v):
    """Relâmpago de Plasma: o punho estalando, a rajada de raios (muitos estalos em cima de um zumbido
    elétrico) e os acertos pipocando no rival."""
    x = _z(1.5)
    poe(x, estalo(rng, n_de(0.08), 2000, 9000, 0.01) * 1.0, 0.0)
    z = _zumbido(rng, 0.7, 140, 0.5)
    poe(x, z * env(len(z), 0.01, 0.5, segura=0.3), 0.02)
    poe(x, _crepita(rng, 0.7, 0.8, 120), 0.02)
    for k in range(7):
        poe(x, B.raio(rng, v) * 0.18, 0.25 + 0.07 * k + rng.uniform(-0.02, 0.02))
    return reverb(x, 0.4, 0.2, 8000)


def velocidade_da_luz(rng, v):
    """Velocidade da Luz: os cortes de luz rasgando o ar em sequência (assobios muito rápidos) e os
    estalos de plasma em cada cruzamento, terminando num clarão."""
    x = _z(1.6)
    for k in range(10):
        poe(x, assobio(rng, n_de(0.12), 3000, 9000, 1.0, 0.3) * env(n_de(0.12), 0.002, 0.08) * 0.35, 0.04 * k)
        poe(x, estalo(rng, n_de(0.05), 3000, 10000, 0.008) * 0.5, 0.05 + 0.04 * k)
    poe(x, _crepita(rng, 0.6, 0.6, 100), 0.3)
    poe(x, B.raio(rng, v) * 0.6, 0.45)
    poe(x, _brilho(rng, 0.8, nota(88), 0.18), 0.5)
    return reverb(x, 0.45, 0.22, 8000)


def cosmo_leao(rng, v):
    """O cosmo do Aiolia subindo: o acorde dourado crescendo, o zumbido elétrico e um rosnado baixo."""
    n = n_de(1.4)
    x = sum(seno(nota(nn), n) * g for nn, g in ((52, 0.1), (59, 0.08), (64, 0.07), (71, 0.05))) * sobe_e_some(n, 0.9, 1.2)
    x += _crepita(rng, 1.4, 0.3, 40)
    poe(x, _rugido_de_leao(rng, 0.8, 0.25), 0.4)
    return reverb(x, 0.5, 0.25, 7000)


def rugido_do_leao(rng, v):
    """Rugido do Leão: o rugido de verdade saindo, a bola de cosmo voando e a explosão dourada com o
    estalo elétrico que fica."""
    x = _z(2.0)
    poe(x, _rugido_de_leao(rng, 0.9, 0.9), 0.0)
    poe(x, _whoosh(rng, 0.45, 300, 2000, 0.6, g=0.6), 0.2)
    poe(x, B.explosao(rng, v) * 1.0, 0.6)
    poe(x, baque(n_de(0.7), 80, 35, 0.25, 0.8) * 1.0, 0.6)
    poe(x, _crepita(rng, 0.7, 0.6, 70), 0.75)
    return reverb(x, 0.55, 0.25, 6500)


# =================================================================== Arthas
def _vozes_frias(rng, seg, g=1.0):
    """Um coro gelado e sussurrado: ruído filtrado em duas bandas de vogal, oscilando devagar."""
    n = n_de(seg)
    t = _t(n)
    base = rosa(rng, n)
    v1 = passa(base, 500, 800, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.8 * t))
    v2 = passa(base, 1100, 1500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.1 * t + 1))
    return (v1 + v2 * 0.7) * sobe_e_some(n, 0.5, 1.5) * g


def ceifadora_de_almas(rng, v):
    """Ceifadora de Almas: a Frostmourne cortando (o metal frio e o gelo estalando), e a alma
    arrancada — um gemido que é puxado para longe."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.2, 2500, 700, 0.35, g=0.7), 0.0)
    poe(x, B.corte_pesado(rng, v) * 0.9, 0.12)
    poe(x, modal(n_de(0.6), nota(74), rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.4) * 0.2, 0.13)
    poe(x, B.gelo(rng, v) * 0.4, 0.15)
    m = n_de(0.8)
    gemido = seno(varre(520, 260, m, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 5 * _t(m))), m) * 0.12 + _vozes_frias(rng, 0.8, 0.5)
    poe(x, gemido * env(m, 0.08, 0.5), 0.4)
    return reverb(x, 0.6, 0.3, 5000)


def erguer_os_mortos(rng, v):
    """Erguer os mortos: as runas acendendo (um zumbido grave), a terra se abrindo, os ossos
    estalando enquanto as mãos sobem e o escudo fechando com um tom gelado."""
    x = _z(1.9)
    z = _zumbido(rng, 0.8, 60, 0.4)
    poe(x, z * sobe_e_some(len(z), 0.6, 1.4), 0.0)
    poe(x, passa(rosa(rng, n_de(0.5)), 40, 300, 2) * sobe_e_some(n_de(0.5), 0.4, 1.4) * 0.6, 0.15)
    for k in range(9):
        poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.01) * 0.45, 0.3 + 0.05 * k + rng.uniform(-0.015, 0.015))
    poe(x, B.escudo(rng, v) * 0.6, 0.85)
    poe(x, modal(n_de(0.9), nota(62), rng=rng, **CRISTAL) * env(n_de(0.9), 0.002, 0.6) * 0.15, 0.85)
    poe(x, _vozes_frias(rng, 1.0, 0.25), 0.5)
    return reverb(x, 0.6, 0.3, 5000)


def runa_lich(rng, v):
    """As runas girando no Preparo: o coro gelado, o zumbido grave pulsando e o vento frio."""
    n = n_de(2.1)
    t = _t(n)
    x = _vozes_frias(rng, 2.1, 0.5)
    x += _zumbido(rng, 2.1, 55, 0.35) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.8, 1.2)
    x += assobio(rng, n, 400, 1200, 1.0, 0.35) * sobe_e_some(n, 0.8, 1.4) * 0.3
    return reverb(x, 0.65, 0.32, 5000)


def praga_da_carne(rng, v):
    """Praga da Carne: a névoa caindo no campo (um sopro pesado e úmido), o borbulhar doente, os
    gemidos das caveiras, o gelo estalando e a vida sendo sugada de volta."""
    x = _z(2.3)
    m = n_de(0.9)
    poe(x, passa(rosa(rng, m), 80, 900, 2) * sobe_e_some(m, 0.3, 1.4) * 0.8, 0.0)
    for k in range(14):
        f0 = rng.uniform(150, 400)
        b = n_de(0.07)
        poe(x, seno(varre(f0, f0 * 1.6, b, 1.0), b) * env(b, 0.003, 0.05) * 0.15, 0.2 + 0.06 * k + rng.uniform(-0.02, 0.02))
    poe(x, _vozes_frias(rng, 1.2, 0.5), 0.4)
    poe(x, B.gelo(rng, v) * 0.5, 0.6)
    poe(x, B.dreno(rng, v) * 0.6, 1.4)
    return reverb(x, 0.65, 0.3, 4500)


SONS: dict = {
    "relampago-de-plasma": (relampago_de_plasma, "Relâmpago de Plasma: a rajada de raios"),
    "velocidade-da-luz": (velocidade_da_luz, "Velocidade da Luz: os cortes de luz em sequência"),
    "cosmo-leao": (cosmo_leao, "o cosmo dourado do Aiolia subindo"),
    "rugido-do-leao": (rugido_do_leao, "Rugido do Leão: o rugido e a explosão dourada"),
    "ceifadora-de-almas": (ceifadora_de_almas, "Ceifadora de Almas: o corte gelado e a alma arrancada"),
    "erguer-os-mortos": (erguer_os_mortos, "Erguer os mortos: os ossos subindo e o escudo"),
    "runa-lich": (runa_lich, "as runas da Frostmourne girando"),
    "praga-da-carne": (praga_da_carne, "Praga da Carne: a névoa da peste e a vida sugada"),
}
