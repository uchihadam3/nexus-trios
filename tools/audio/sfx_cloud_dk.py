"""Os sons das habilidades do Cloud e do Donkey Kong (veja tools/vfx/familias_v2/cloud_e_dk.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (METAL, SR, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido, satura,
                 seno, sobe_e_some, varre)


def _espadao(rng, seg=0.35, g=1.0, f0=300, f1=2600):
    """O ar cortado por uma espada enorme: um sopro grave e largo que sobe de tom."""
    return _whoosh(rng, seg, f0, f1, 0.7, 1.2, g)


def _clangor(rng, f=nota(50), g=0.5, seg=0.7):
    n = n_de(seg)
    return modal(n, f, rng=rng, **METAL) * env(n, 0.001, seg * 0.4) * g


def _madeira(rng, n, g=1.0):
    """Madeira rachando: estalos médios secos e um corpo oco."""
    x = graos(rng, n, 50, 0.0, n / SR * 0.5, 500, 4000, 0.008, 0.6) * 0.9
    x += passa(ruido(rng, n), 300, 2500, 2) * env(n, 0.001, 0.06) * 0.8
    x += seno(varre(260, 170, n, 1.0), n) * env(n, 0.001, 0.08) * 0.4
    return x * g


# --------------------------------------------------------------- Cloud
def golpe_ascendente(rng, v):
    """Golpe ascendente: a Buster Sword sobe num sopro largo, o impacto pesado com o metal tinindo e os
    estilhaços chiando para cima."""
    x = _z(1.3)
    poe(x, _espadao(rng, 0.4, 0.9, 250, 3200), 0.0)
    poe(x, B.corte_pesado(rng, v) * 1.0, 0.22)
    poe(x, baque(n_de(0.45), 110, 50, 0.16, 0.6) * 0.8, 0.24)
    poe(x, _clangor(rng, nota(55), 0.35, 0.6), 0.24)
    poe(x, graos(rng, n_de(0.6), 30, 0.0, 0.5, 2500, 9000, 0.004, 0.6) * 0.4, 0.3)
    return reverb(x, 0.5, 0.22, 6000)


def postura_de_guarda(rng, v):
    """Postura de guarda: a espada bloqueia (um CLANG de metal grosso com faíscas) e o contra-ataque
    vem logo atrás, num corte pesado."""
    x = _z(1.5)
    poe(x, B.bloqueio(rng, v) * 1.0, 0.0)
    poe(x, _clangor(rng, nota(47), 0.6, 0.9), 0.0)
    poe(x, graos(rng, n_de(0.4), 25, 0.0, 0.3, 3000, 9000, 0.003, 0.6) * 0.45, 0.02)
    poe(x, _espadao(rng, 0.3, 0.8, 300, 2800), 0.42)
    poe(x, B.corte_pesado(rng, v) * 1.0, 0.6)
    poe(x, baque(n_de(0.4), 100, 45, 0.15, 0.6) * 0.7, 0.62)
    return reverb(x, 0.5, 0.22, 6000)


def limite_cloud(rng, v):
    """O Limite do Cloud no Preparo do Omnislash: a energia subindo num zumbido que cresce."""
    n = n_de(1.4)
    t = np.arange(n) / SR
    x = (seno(varre(nota(45), nota(69), n, 1.4), n) * 0.18 + seno(varre(nota(52), nota(76), n, 1.4), n) * 0.1) * (0.7 + 0.3 * np.sin(2 * math.pi * 8 * t))
    x += passa(rosa(rng, n), 800, 6000, 2) * 0.1
    x += graos(rng, n, 40, 0.2, 1.3, 3000, 9000, 0.003, 0.6) * 0.3
    return reverb(x * sobe_e_some(n, 0.95, 1.6), 0.4, 0.2, 7000)


def omnislash(rng, v):
    """Omnislash: os cortes vêm um atrás do outro, cada vez mais rápidos (zás, zás… zás-zás-zás), e o
    corte final cai pesado, com o eco do metal."""
    x = _z(2.2)
    em = 0.0
    for k in range(12):
        poe(x, B.corte(rng, v) * (0.5 + 0.03 * k), em)
        poe(x, _whoosh(rng, 0.12, 800, 4000, 0.5, g=0.35), em - 0.02 if em > 0.02 else 0.0)
        em += 0.13 * (0.85 ** k) + 0.03
    poe(x, _espadao(rng, 0.3, 1.0, 200, 3500), em + 0.05)
    poe(x, B.corte_pesado(rng, v) * 1.3, em + 0.25)
    poe(x, baque(n_de(0.8), 90, 35, 0.3, 0.7) * 1.0, em + 0.25)
    poe(x, _clangor(rng, nota(43), 0.5, 1.2), em + 0.27)
    return reverb(x, 0.6, 0.28, 5500)


# --------------------------------------------------------------- Donkey Kong
def soco_giratorio(rng, v):
    """Soco giratório: o braço girando faz o vento rodar (vuuum-vuuum), e o punho gigante acerta com
    uma pancada surda enorme, levantando o pó."""
    x = _z(1.4)
    n = n_de(0.45)
    t = np.arange(n) / SR
    roda = assobio(rng, n, 200, 900, 1.0) * (0.5 + 0.5 * np.sin(2 * math.pi * (5 + 8 * t) * t)) * sobe_e_some(n, 0.9, 1.3) * 0.7
    poe(x, roda, 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.3, 0.38)
    poe(x, baque(n_de(0.7), 80, 32, 0.28, 0.7) * 1.2, 0.38)
    poe(x, passa(rosa(rng, n_de(0.6)), 100, 1500, 2) * env(n_de(0.6), 0.01, 0.3) * 0.35, 0.42)
    return reverb(x, 0.45, 0.2, 5000)


def barril_arremessado(rng, v):
    """Barril arremessado: o Donkey Kong lança (um grunhido de esforço feito de pancada), o barril
    rola no ar (um zumbido de madeira girando) e se espatifa: madeira estourando e as tábuas caindo."""
    x = _z(1.8)
    poe(x, baque(n_de(0.25), 120, 70, 0.08, 0.5) * 0.6, 0.0)
    n = n_de(0.5)
    t = np.arange(n) / SR
    gira = passa(rosa(rng, n), 150, 1200, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * t)) * sobe_e_some(n, 0.9, 1.2) * 0.5
    poe(x, gira, 0.05)
    poe(x, _madeira(rng, n_de(0.5), 1.2), 0.52)
    poe(x, baque(n_de(0.5), 110, 50, 0.18, 0.6) * 0.9, 0.52)
    for k in range(5):
        poe(x, _madeira(rng, n_de(0.12), 0.35), 0.75 + 0.09 * k + rng.uniform(-0.02, 0.02))
    return reverb(x, 0.45, 0.2, 5500)


def batida_preparo(rng, v):
    """O Donkey Kong batendo no peito antes da batida: pancadas surdas que aceleram."""
    x = _z(1.3)
    em = 0.0
    for k in range(5):
        poe(x, baque(n_de(0.25), 130, 80, 0.07, 0.3) * 0.6, em)
        em += 0.24 * 0.85 ** k
    return reverb(x, 0.35, 0.15, 5000)


def batida_do_gorila(rng, v):
    """Batida do gorila: a pancada no chão (um baque enorme), o chão rachando, o tremor rolando e as
    pedras caindo de volta."""
    x = _z(2.0)
    poe(x, B.terremoto(rng, v) * 1.0, 0.0)
    poe(x, baque(n_de(1.0), 70, 25, 0.4, 0.8) * 1.3, 0.0)
    poe(x, estalo(rng, n_de(0.1), 400, 3500, 0.03) * 0.9, 0.01)
    poe(x, graos(rng, n_de(0.6), 40, 0.0, 0.5, 300, 3000, 0.01, 0.5) * 0.7, 0.05)
    poe(x, satura(passa(rosa(rng, n_de(1.2)), 30, 300, 2) * env(n_de(1.2), 0.02, 0.6), 1.5) * 0.6, 0.05)
    for k in range(6):
        poe(x, baque(n_de(0.15), 160, 90, 0.04, 0.4) * 0.35, 0.6 + 0.12 * k + rng.uniform(-0.03, 0.03))
    return reverb(x, 0.6, 0.25, 4500)


SONS: dict = {
    "golpe-ascendente": (golpe_ascendente, "Golpe ascendente do Cloud: a Buster Sword subindo e o impacto"),
    "postura-de-guarda": (postura_de_guarda, "Postura de guarda: o bloqueio de metal e o contra-ataque"),
    "limite-cloud": (limite_cloud, "o Limite do Cloud crescendo no Preparo"),
    "omnislash": (omnislash, "Omnislash: os cortes cada vez mais rápidos e o corte final"),
    "soco-giratorio": (soco_giratorio, "Soco giratório do Donkey Kong: o braço girando e o soco gigante"),
    "barril-arremessado": (barril_arremessado, "Barril arremessado: o barril girando e se espatifando"),
    "batida-preparo": (batida_preparo, "o Donkey Kong batendo no peito antes da batida"),
    "batida-do-gorila": (batida_do_gorila, "Batida do gorila: o chão rachando e as pedras caindo"),
}
