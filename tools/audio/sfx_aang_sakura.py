"""Os sons do Aang e da Sakura (veja tools/vfx/familias_v2/aang_sakura.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import CRISTAL, SR, assobio, baque, env, estalo, graos, n_de, passa, poe, reverb, rosa, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _vento_girando(rng, seg, g=1.0, f0=300, f1=1800, giro=7.0):
    """Vento em redemoinho: o assobio com o volume e o brilho girando."""
    n = n_de(seg)
    t = _t(n)
    a = assobio(rng, n, f0, f1, 1.0, 0.45) * (0.6 + 0.4 * np.sin(2 * math.pi * giro * t))
    return a * sobe_e_some(n, 0.5, 1.4) * g


# =================================================================== Aang
def rajada_do_aang(rng, v):
    """Rajada de ar: o bastão girando e o "fuuush" da bola de ar saindo, o voo assobiando e o
    estouro de vento no rival."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.2, 600, 200, 0.5, g=0.5), 0.0)
    poe(x, _vento_girando(rng, 0.6, 0.9, 400, 2200, 9), 0.08)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 150, 2500, 2) * env(n, 0.005, 0.3) * 0.9, 0.6)
    poe(x, baque(n_de(0.4), 110, 55, 0.12, 0.4) * 0.6, 0.6)
    return reverb(x, 0.45, 0.22, 7000)


def dobra_de_agua(rng, v):
    """Dobra de água: a água chicoteando (o "chuá" que corre), o giro em volta do aliado e a bolha
    fechando com o borbulhar e o brilho."""
    x = _z(1.7)
    poe(x, B.agua(rng, v) * 0.7, 0.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 400, 3500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * _t(n))) * sobe_e_some(n, 0.5, 1.4) * 0.6, 0.1)
    for k in range(10):
        f0 = rng.uniform(300, 700)
        m = n_de(0.06)
        poe(x, seno(varre(f0, f0 * 1.8, m, 1.0), m) * env(m, 0.003, 0.04) * 0.15, 0.6 + 0.05 * k + rng.uniform(-0.02, 0.02))
    poe(x, B.escudo(rng, v) * 0.5, 0.7)
    return reverb(x, 0.5, 0.25, 7000)


def avatar_brilho(rng, v):
    """O Estado Avatar acendendo: o acorde profundo de muitas vozes crescendo, o vento girando e o
    estalo do brilho dos olhos."""
    n = n_de(2.2)
    t = _t(n)
    x = sum(seno(nota(nn) * (1 + 0.002 * np.sin(2 * math.pi * 0.5 * t + k)), n) * g for k, (nn, g) in enumerate(((38, 0.14), (45, 0.11), (50, 0.09), (57, 0.07), (62, 0.05))))
    x = x * sobe_e_some(n, 0.92, 1.1)
    x += _vento_girando(rng, 2.2, 0.4, 200, 900, 2)
    poe(x, estalo(rng, n_de(0.1), 2000, 8000, 0.02) * 0.5, 1.9)
    return reverb(x, 0.6, 0.3, 6000)


def estado_avatar_aang(rng, v):
    """O Estado Avatar no campo: o tornado rugindo (vento grave e forte girando), o fogo, a água e a
    pedra passando dentro dele, e o estrondo no fim."""
    x = _z(2.3)
    poe(x, _vento_girando(rng, 1.8, 1.0, 120, 900, 3), 0.0)
    m = n_de(1.6)
    poe(x, passa(rosa(rng, m), 30, 200, 2) * sobe_e_some(m, 0.4, 1.3) * 0.8, 0.1)
    poe(x, B.fogo(rng, v) * 0.35, 0.5)
    poe(x, B.agua(rng, v) * 0.35, 0.8)
    poe(x, B.terra(rng, v) * 0.4, 1.1)
    poe(x, B.explosao(rng, v) * 0.6, 1.5)
    return reverb(x, 0.65, 0.3, 5500)


# =================================================================== Sakura
def controle_de_chakra(rng, v):
    """Controle de chakra: o chakra juntando com precisão (um tom que aperta e sobe) e o "tchim"
    firme no punho."""
    x = _z(1.3)
    n = n_de(0.7)
    f = varre(220, 660, n, 1.3)
    poe(x, (seno(f, n) * 0.2 + seno(f * 1.5, n) * 0.08) * sobe_e_some(n, 0.9, 1.2), 0.0)
    poe(x, graos(rng, n, 14, 0.0, 0.65, 2000, 7000, 0.003, 0.6) * 0.25, 0.0)
    poe(x, _brilho(rng, 0.6, nota(79), 0.25, CRISTAL), 0.68)
    poe(x, baque(n_de(0.3), 160, 90, 0.06, 0.5) * 0.4, 0.68)
    return reverb(x, 0.45, 0.22, 7000)


def forca_monstruosa(rng, v):
    """Força monstruosa: o grito curto, o soco que bate como um terremoto, o chão rachando e as
    pedras caindo."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.18, 300, 1500, 0.8, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.14)
    poe(x, baque(n_de(0.9), 60, 25, 0.4, 1.0) * 1.3, 0.14)
    poe(x, B.terremoto(rng, v) * 0.7, 0.18)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.05), 300, 3000, 0.02) * 0.35, 0.3 + 0.08 * k + rng.uniform(-0.02, 0.02))
    return reverb(x, 0.55, 0.25, 5000)


def byakugou_selo(rng, v):
    """O selo do Byakugou acendendo: um tom grave que pulsa como coração e o chakra subindo."""
    n = n_de(1.3)
    t = _t(n)
    pulso = np.exp(-((t % 0.5) / 0.08)) + 0.6 * np.exp(-(((t - 0.15) % 0.5) / 0.08))
    x = seno(55, n) * pulso * 0.4 + seno(110, n) * pulso * 0.15
    x += sum(seno(nota(nn), n) * 0.05 for nn in (64, 71, 76)) * sobe_e_some(n, 0.9, 1.2)
    return reverb(x, 0.5, 0.25, 6000)


def byakugou(rng, v):
    """Byakugou: a cura grande se espalhando no trio — o acorde quente subindo, os brilhos e o sopro
    suave das pétalas."""
    x = _z(1.8)
    poe(x, B.cura(rng, v) * 0.8, 0.0)
    for k, nn in enumerate((60, 64, 67, 72, 76)):
        poe(x, _brilho(rng, 0.8, nota(nn), 0.13), 0.1 + 0.08 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.5, 1.5) * 0.12, 0.3)
    return reverb(x, 0.6, 0.3, 7000)


SONS: dict = {
    "rajada-do-aang": (rajada_do_aang, "Rajada de ar: a bola de vento e o estouro"),
    "dobra-de-agua": (dobra_de_agua, "Dobra de água: o chicote de água e a bolha"),
    "avatar-brilho": (avatar_brilho, "o Estado Avatar acendendo"),
    "estado-avatar-aang": (estado_avatar_aang, "Estado Avatar: o tornado com os quatro elementos"),
    "controle-de-chakra": (controle_de_chakra, "Controle de chakra: o chakra apertando no punho"),
    "forca-monstruosa": (forca_monstruosa, "Força monstruosa: o soco que racha o chão"),
    "byakugou-selo": (byakugou_selo, "o selo do Byakugou acendendo"),
    "byakugou": (byakugou, "Byakugou: a cura grande no trio"),
}
