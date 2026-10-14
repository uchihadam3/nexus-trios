"""Ataques básicos com animação própria, lote zl: Bowser, Charizard, Visão, Rick, Marvin, Krang, Plankton e Alphonse.

A garra pesada do Bowser com a baforada de fogo, as três garras em chamas do Charizard, o raio dourado da Joia da Mente
do Visão, o raio verde da arma do Rick com o portal no acerto, o desintegrador do Marvin que deixa só o contorno, o raio
rosa da Dimensão X do Krang, o laser minúsculo (e cômico) do Plankton e o punho de armadura do Alphonse com o círculo
de transmutação.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts, _zigue
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


def _feixe(T, t, t0, t1, x0, y0, x1=0.0, y1=0.0, larg=0.05, some=0.18):
    """Um feixe que cresce de (x0,y0) até o alvo entre t0 e t1, segura e some."""
    p = ease_out(rel(t, t0, t1), 2)
    k = 1 - rel(t, t1 + some, t1 + some + 0.15)
    if p <= 0 or k <= 0:
        return T.zero()
    x, y = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    return (T.lines([(x0, y0, x, y, 1.0)], larg) + T.lines([(x0, y0, x, y, 1.0)], larg * 0.35)) * k


# ------------------------------------------------------------------ Bowser
def garra_do_rei_bowser(T, t, rng):
    """Bowser: a garra grossa do Rei dos Koopas desce em três riscos largos e, logo atrás, ele solta uma baforada de
    fogo curta pelo nariz."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    riscos = T.zero()
    k = rel(t, 0.02, 0.16)
    if k > 0:
        riscos = T.polys([(lamina(-0.45 + 0.12 * j, -0.55, 0.15 + 0.12 * j, 0.45, 0.06, ease_out(k, 2.5), rel(t, 0.4, 0.6)), 1.0) for j in range(3)], 0.003)
    fogo = T.zero()
    kf = pulso(t, 0.24, 0.6)
    if kf > 0:
        u = rel(t, 0.24, 0.6)
        for j in range(6):
            fogo += T.gauss(-0.7 + 0.18 * j * u + 0.05 * j, -0.4 + 0.03 * math.sin(t * 30 + j), 0.05 + 0.02 * j)
        fogo *= kf * 0.7
    est = _estrela_de_contato(T, t, 0.16, 0.28, 8, 0.32)
    G += (T.glow(riscos, 1.0, 0.7, 0.025) + fogo + est) * env
    H += (riscos * 1.3 + fogo * 0.6 + est) * env
    return G, H


# ------------------------------------------------------------------ Charizard
def garra_flamejante(T, t, rng):
    """Charizard: a garra rasga com as três unhas em brasa, e o fogo fica queimando nos riscos, com as fagulhas
    subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = rel(t, 0.0, 0.14)
    riscos = T.zero()
    if k > 0:
        riscos = T.polys([(lamina(-0.5, 0.35 - 0.15 * j, 0.45, -0.25 - 0.15 * j, 0.04, ease_out(k, 2.5), rel(t, 0.5, 0.75)), 1.0) for j in range(3)], 0.003)
    chamas = T.zero()
    kc = janela(t, 0.12, 0.2) * apaga(t, 0.45, 0.72)
    if kc > 0:
        formas = []
        for j in range(3):
            for s in (0.25, 0.5, 0.75):
                bx, by = -0.5 + 0.95 * s, 0.35 - 0.15 * j - 0.6 * s
                alt = 0.08 + 0.04 * math.sin(t * 40 + j + s * 7)
                formas.append(([(bx - 0.03, by), (bx, by - alt), (bx + 0.03, by)], 1.0))
        chamas = T.polys(formas, 0.008) * kc
    fagulhas = _gotas(T, t, 0.15, 0.55, 14, 59, tam=0.018, cai=-0.4, alcance=0.4)
    G += (T.glow(riscos, 1.1, 0.8, 0.025) + chamas * 1.1 + fagulhas) * env
    H += (riscos * 1.4 + chamas * 0.7 + fagulhas * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Visão
def raio_da_joia_mente(T, t, rng):
    """Visão: a Joia da Mente na testa brilha (o losango dourado) e solta um raio fino e reto, que acerta e espalha
    pontinhos de luz."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gema = T.polys([([(-0.85, -0.12), (-0.8, -0.05), (-0.85, 0.02), (-0.9, -0.05)], 1.0)], 0.002) * pulso(t, 0.0, 0.45) * 1.3
    feixe = _feixe(T, t, 0.06, 0.16, -0.85, -0.05, 0.0, 0.0, 0.035)
    pontos = _gotas(T, t, 0.16, 0.4, 14, 113, tam=0.014, cai=0.0, alcance=0.4, a0=-3.1, a1=3.1)
    est = _estrela_de_contato(T, t, 0.16, 0.2, 4, 0.3)
    G += (gema + T.glow(feixe, 1.0, 0.7, 0.02) + pontos + est) * env
    H += (gema * 1.3 + feixe * 1.4 + pontos * 0.8 + est) * env
    return G, H


# ------------------------------------------------------------------ Rick
def arma_de_raio_rick(T, t, rng):
    """Rick: o tiro verde da arma de raio, meio torto e borbulhante, e no acerto um portal verde abre girando por um
    instante e engole a fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.02, 0.16)
    bolha = T.zero()
    if 0 < u < 1:
        x = -0.85 + 0.85 * u
        y = 0.05 * math.sin(u * 14)
        bolha = T.gauss(x, y, 0.06) * 1.3 + T.polyline([(x - 0.3 * s, y + 0.04 * math.sin(s * 12 + t * 40)) for s in np.linspace(0, 1, 10)], 0.04)
    kp = pulso(t, 0.16, 0.7)
    portal = T.zero()
    if kp > 0:
        r = 0.25 * back(rel(t, 0.16, 0.3), 1.6)
        portal = T.polys([(_elipse_pts(0, 0, r + 0.005, r * 1.2 + 0.005, 0.0, 24), 1.0)], 0.01) * kp * 0.6
        espiral = [(math.cos(a + t * 10) * r * (a / 9), math.sin(a + t * 10) * r * 1.2 * (a / 9)) for a in np.linspace(0, 9, 30)]
        portal += T.polyline(espiral, 0.02) * kp
    G += (bolha * 1.2 + portal) * env
    H += (bolha + portal * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Marvin
def desintegrador_marvin(T, t, rng):
    """Marvin: o raio fininho do desintegrador (com o "pew" de desenho), e o alvo fica só no contorno pontilhado por um
    instante, como se tivesse virado pó, antes de voltar."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    raio = T.polyline(_zigue(-0.9, 0.0, 0.0, 0.0, 9, 0.035), 0.024) * pulso(t, 0.04, 0.22)
    kc = pulso(t, 0.2, 0.7)
    contorno = T.zero()
    if kc > 0:
        pts = [(math.cos(a) * 0.22, math.sin(a) * 0.32) for a in np.linspace(0, TAU, 28)]
        contorno = T.splats([(x, y, 1.0) for x, y in pts], 0.012) * kc
    po = _gotas(T, t, 0.22, 0.5, 18, 127, tam=0.012, cai=0.5, alcance=0.25)
    G += (raio * 1.3 + contorno + po) * env
    H += (raio * 1.2 + contorno * 0.8 + po * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Krang
def raio_da_dimensao_x(T, t, rng):
    """Krang: o raio rosa da Dimensão X sai da barriga do robô em onda grossa e abre uma fenda dimensional no alvo, com
    o contorno tremendo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    onda = T.zero()
    k = ease_out(rel(t, 0.04, 0.18), 2) * (1 - rel(t, 0.38, 0.5))
    if k > 0:
        pts = [(-0.9 + 0.9 * s * k, 0.06 * math.sin(s * 16 - t * 40)) for s in np.linspace(0, 1, 24)]
        onda = T.polyline(pts, 0.06)
    kf = pulso(t, 0.18, 0.65)
    fenda = T.zero()
    if kf > 0:
        pts = [(0.03 * math.sin(s * 20 + t * 30), -0.35 + 0.7 * s) for s in np.linspace(0, 1, 18)]
        fenda = T.polyline(pts, 0.03 + 0.03 * kf) * kf + T.ring(0.3, 0.015, squash=0.5) * kf
    G += (onda * 1.1 + fenda * 1.2) * env
    H += (onda * 0.8 + fenda * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Plankton
def laser_minusculo(T, t, rng):
    """Plankton: um laserzinho minúsculo e ridículo sai do lado, acerta com uma explosãozinha de nada… e uma
    fumacinha sobe; o anel de choque é do tamanho de uma ervilha."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.05, 0.25)
    laser = T.zero()
    if 0 < u < 1:
        x = -0.6 + 0.6 * u
        laser = T.lines([(x - 0.15, 0.0, x, 0.0, 1.0)], 0.022) + T.gauss(x, 0.0, 0.02)
    pff = T.polys([(estrela(0, 0, 0.1 * pulso(t, 0.25, 0.45) + 0.005, 0.3, 6, 0.5), 1.0)], 0.002) * pulso(t, 0.25, 0.45)
    anelzinho = _anel(T, t, 0.25, 0.5, 0.03, 0.16, 0.016)
    fumaca = T.gauss(0.0, -0.08 - 0.2 * rel(t, 0.3, 0.8), 0.04) * pulso(t, 0.3, 0.8) * 0.6
    G += (laser * 1.3 + pff * 1.2 + anelzinho + fumaca) * env
    H += (laser + pff + anelzinho * 0.5 + fumaca * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Alphonse
def punho_de_armadura_al(T, t, rng):
    """Alphonse: o punho da armadura gigante (placas e rebites) vem num soco pesado, e o círculo de transmutação se
    acende no chão sob o alvo no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.22, 0.2, 1.35, 'armadura')
    kc = pulso(t, 0.2, 0.7)
    circulo = T.zero()
    if kc > 0:
        r = 0.4 * back(rel(t, 0.2, 0.32), 1.5)
        circulo = (T.ring(r, 0.016, 0, 0.35, 2.6) + T.ring(r * 0.75, 0.01, 0, 0.35, 2.6)) * kc
        pts = [(math.cos(a) * r * 0.75, 0.35 + math.sin(a) * r * 0.75 / 2.6) for a in np.linspace(0, TAU, 6) - math.pi / 2]
        circulo += T.polyline(pts[::2] + pts[1::2] + [pts[0]], 0.01) * kc
    est = _estrela_de_contato(T, t, 0.22, 0.3, 8, 0.32)
    onda = _anel(T, t, 0.22, 0.6, 0.1, 0.5, 0.05)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.4 + circulo + est + onda) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + circulo * 0.6 + est + onda * 0.4) * env
    return G, H


REGISTRO = [
    ("garra_do_rei_bowser", garra_do_rei_bowser, GRANDE, "básico do Bowser: a garra pesada e a baforada de fogo", False),
    ("garra_flamejante", garra_flamejante, GRANDE, "básico do Charizard: as três garras em brasa", False),
    ("raio_da_joia_mente", raio_da_joia_mente, GRANDE, "básico do Visão: o raio dourado da Joia da Mente", False),
    ("arma_de_raio_rick", arma_de_raio_rick, GRANDE, "básico do Rick: o raio verde e o portal no acerto", False),
    ("desintegrador_marvin", desintegrador_marvin, GRANDE, "básico do Marvin: o desintegrador e o contorno de pó", False),
    ("raio_da_dimensao_x", raio_da_dimensao_x, GRANDE, "básico do Krang: o raio rosa e a fenda dimensional", False),
    ("laser_minusculo", laser_minusculo, GRANDE, "básico do Plankton: o laser minúsculo e a explosãozinha", False),
    ("punho_de_armadura_al", punho_de_armadura_al, GRANDE, "básico do Alphonse: o punho de armadura e o círculo", False),
]
