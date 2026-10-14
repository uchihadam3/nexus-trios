"""Ataques básicos com animação própria, lote zi: Roy Mustang, Justiceiro, Senhor das Estrelas, Rocket, Master Chief,
Leon, Jill e Mega Man.

Os oito dividiam o mesmo "tiro"; agora cada arma conta quem atira: o tiro do coronel com o círculo de transmutação no
acerto, a rajada de três do Justiceiro com a caveira, os dois blasters do Senhor das Estrelas, o canhão grande demais
do Rocket, a rajada traçante do Master Chief no escudo de energia, o tiro e a faca do Leon, a mira laser e os dois
tiros da Jill, e as "balinhas de limão" do Mega Buster.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _estrela_de_contato, _riscos


def _bala(T, t, t0, dur, y0=0.0, y1=0.0, x0=-0.95, x1=0.0, larg=0.04, rastro=0.4):
    """Uma bala/raio voando de (x0,y0) até (x1,y1) entre t0 e t0+dur, com rastro afinando; some ao chegar."""
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    dx, dy = x1 - x0, y1 - y0
    c = math.hypot(dx, dy) or 1
    return T.tapered([(x - dx / c * rastro, y - dy / c * rastro, x, y, 1.0)], larg) + T.gauss(x, y, larg * 0.8) * 1.2


def _boca(T, t, t0, x=-0.9, y=0.0, tam=0.35):
    """O clarão na boca do cano no instante do disparo."""
    return T.flare(x, y, tam, 0.0, 0.012) * pulso(t, t0, t0 + 0.1) * 1.3


# ------------------------------------------------------------------ Roy Mustang
def tiro_do_coronel(T, t, rng):
    """Roy Mustang: um tiro seco e certeiro da pistola do exército e, no acerto, o círculo de transmutação gira por um
    instante com uma faísca de fogo no meio (o Alquimista das Chamas não resiste)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    bala = _bala(T, t, 0.04, 0.14)
    boca = _boca(T, t, 0.02)
    kc = pulso(t, 0.18, 0.6)
    circulo = T.zero()
    if kc > 0:
        r = 0.28 * back(rel(t, 0.18, 0.3), 1.8)
        giro = t * 4
        tri = [(math.cos(giro + k * TAU / 3) * r, math.sin(giro + k * TAU / 3) * r) for k in range(4)]
        circulo = (T.ring(r, 0.014) + T.ring(r * 0.75, 0.01) + T.polyline(tri, 0.012)) * kc
    fogo = T.polys([([(-0.06, 0.06), (0.0, -0.14 - 0.05 * math.sin(t * 40)), (0.06, 0.06)], 1.0)], 0.01) * pulso(t, 0.2, 0.5)
    est = _estrela_de_contato(T, t, 0.18, 0.18, 6, 0.32)
    G += (bala * 1.3 + boca + circulo + fogo + est) * env
    H += (bala * 1.2 + boca * 1.2 + circulo * 0.6 + fogo + est) * env
    return G, H


# ------------------------------------------------------------------ Justiceiro
def rajada_do_justiceiro(T, t, rng):
    """Justiceiro: três tiros em sequência, as cápsulas pulando do lado, e a caveira branca aparece no alvo depois do
    último."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    balas = sum(_bala(T, t, 0.02 + 0.07 * k, 0.12, -0.05 + 0.05 * k, -0.04 + 0.04 * k) for k in range(3))
    boca = sum(_boca(T, t, 0.0 + 0.07 * k) for k in range(3))
    capsulas = T.zero()
    for k in range(3):
        u = rel(t, 0.02 + 0.07 * k, 0.4 + 0.07 * k)
        if 0 < u < 1:
            x, y = -0.85 - 0.1 * u, -0.1 - 0.35 * u + 0.6 * u * u
            capsulas += T.polys([(_elipse_pts(x, y, 0.025, 0.01, u * 12, 8), 1.0)], 0.002) * (1 - u)
    kk = pulso(t, 0.3, 0.8)
    caveira = T.zero()
    if kk > 0:
        s = 0.2 * back(rel(t, 0.3, 0.42), 2.0)
        caveira = T.polys([(_elipse_pts(0, -0.05 * s / 0.2, s, s * 0.85, 0.0, 20), 1.0)], 0.003)
        for dx in (-0.4, 0.4):
            caveira -= T.polys([(_elipse_pts(dx * s, -0.1 * s / 0.2, s * 0.25, s * 0.3, 0.0, 12), 1.0)], 0.003)
        caveira += T.lines([(-0.3 * s + 0.15 * s * k, 0.55 * s, -0.3 * s + 0.15 * s * k, 0.95 * s, 1.0) for k in range(5)], 0.02 * s / 0.2)
        caveira = np.clip(caveira, 0, 1) * kk
    G += (balas * 1.3 + boca + capsulas + caveira * 1.1) * env
    H += (balas * 1.2 + boca * 1.2 + capsulas * 0.6 + caveira * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Senhor das Estrelas
def blasters_do_quill(T, t, rng):
    """Senhor das Estrelas: os dois blasters giram na mão e disparam um de cada vez, dois tiros gordos de plasma
    laranja, e o acerto estoura em anéis."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    giro = T.zero()
    kg = pulso(t, 0.0, 0.16)
    if kg > 0:
        for k, y in enumerate((-0.25, 0.25)):
            a = t * 50 + k
            giro += T.lines([(-0.85, y, -0.85 + math.cos(a) * 0.12, y + math.sin(a) * 0.12, 1.0)], 0.03)
        giro *= kg
    tiros = T.zero()
    for k, (t0, y) in enumerate(((0.1, -0.25), (0.2, 0.25))):
        u = rel(t, t0, t0 + 0.12)
        if 0 < u < 1:
            x = -0.85 + 0.85 * u
            yy = y * (1 - u)
            tiros += T.gauss(x, yy, 0.07, 0.045) * 1.4 + T.tapered([(x - 0.3, yy - y * 0.3 * 0.0, x, yy, 0.8)], 0.06)
        tiros += _boca(T, t, t0, -0.85, y, 0.3)
    aneis = _anel(T, t, 0.22, 0.5, 0.08, 0.35, 0.04) + _anel(T, t, 0.32, 0.6, 0.08, 0.35, 0.04)
    G += (giro + tiros * 1.2 + aneis) * env
    H += (giro * 0.5 + tiros + aneis * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Rocket
def canhao_do_rocket(T, t, rng):
    """Rocket: o canhão grande demais para ele dá um tranco para trás (o recuo com fumaça), e um tiro grosso de plasma
    cruza a tela e explode."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    recuo = 0.12 * pulso(t, 0.05, 0.3)
    cano = T.polys([([(-0.98 - recuo, -0.09), (-0.68 - recuo, -0.11), (-0.68 - recuo, 0.11), (-0.98 - recuo, 0.09)], 1.0)], 0.003) * (1 - rel(t, 0.45, 0.6))
    fumaca = T.zero()
    kf = pulso(t, 0.05, 0.6)
    if kf > 0:
        for k in range(4):
            fumaca += T.gauss(-0.7 - 0.05 * k, -0.1 - 0.1 * k * rel(t, 0.05, 0.6), 0.06 + 0.02 * k)
        fumaca *= kf * 0.5
    u = rel(t, 0.06, 0.2)
    tiro = T.zero()
    if 0 < u < 1:
        x = -0.68 + 0.68 * u
        tiro = T.gauss(x, 0, 0.12, 0.08) * 1.4 + T.tapered([(x - 0.4, 0, x, 0, 1.0)], 0.12)
    bum = T.polys([(estrela(0, 0, 0.38 * pulso(t, 0.2, 0.55) + 0.01, 0.2, 10, 0.5), 1.0)], 0.01) * pulso(t, 0.2, 0.55)
    anel = _anel(T, t, 0.2, 0.6, 0.12, 0.6, 0.06)
    G += (cano + fumaca + tiro * 1.2 + bum * 1.2 + anel) * env
    H += (cano * 0.4 + fumaca * 0.3 + tiro + bum + anel * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Master Chief
def rajada_do_spartan(T, t, rng):
    """Master Chief: uma rajada de quatro tiros traçantes do fuzil de assalto, e o escudo de energia do alvo pisca em
    hexágonos a cada tiro até rachar."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    balas = sum(_bala(T, t, 0.0 + 0.05 * k, 0.1, 0.03 * ((k % 2) * 2 - 1), 0.02 * ((k % 2) * 2 - 1), larg=0.032, rastro=0.45) for k in range(4))
    boca = sum(_boca(T, t, 0.05 * k, tam=0.25) for k in range(4))
    hexs = T.zero()
    ks = pulso(t, 0.1, 0.5)
    if ks > 0:
        for j, (cx, cy) in enumerate(((0, 0), (0.19, 0.11), (-0.19, 0.11), (0, -0.22), (0.19, -0.11), (-0.19, -0.11), (0, 0.22))):
            pts = [(cx + math.cos(a) * 0.11, cy + math.sin(a) * 0.11) for a in np.linspace(0, TAU, 7) + math.pi / 6]
            pisca = 0.5 + 0.5 * math.sin(t * 60 + j)
            hexs += T.polyline(pts, 0.018) * pisca
        hexs *= ks
    racha = T.lines([(0, 0, 0.2, -0.25, 1), (0, 0, -0.22, 0.18, 1), (0, 0, 0.15, 0.25, 1)], 0.012) * pulso(t, 0.3, 0.6)
    G += (balas * 1.3 + boca + hexs + racha) * env
    H += (balas * 1.1 + boca + hexs * 0.6 + racha * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Leon
def tiro_e_faca_leon(T, t, rng):
    """Leon: um tiro na cabeça que faz o alvo cambalear (o anel de atordoado) e, na sequência, a faca de combate num
    corte rápido de perto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    bala = _bala(T, t, 0.02, 0.12, -0.25, -0.25)
    boca = _boca(T, t, 0.0, y=-0.25)
    tonto = T.ring(0.16, 0.012, 0.0, -0.4, 2.2) * pulso(t, 0.14, 0.4)
    estrelinhas = sum(T.gauss(math.cos(t * 12 + k * 2.1) * 0.16, -0.4 + math.sin(t * 12 + k * 2.1) * 0.07, 0.02) for k in range(3)) * pulso(t, 0.14, 0.4)
    kf = rel(t, 0.3, 0.4)
    faca = T.zero()
    if kf > 0:
        faca = T.polys([(lamina(-0.45, 0.35, 0.45, -0.05, 0.04, ease_out(kf, 2.5), rel(t, 0.5, 0.68)), 1.0)], 0.002)
    est = _estrela_de_contato(T, t, 0.38, 0.22, 6, 0.32)
    G += (bala * 1.3 + boca + tonto + estrelinhas * 1.2 + T.glow(faca, 1.1, 0.7, 0.02) + est) * env
    H += (bala * 1.2 + boca + tonto * 0.5 + estrelinhas + faca * 1.5 + est) * env
    return G, H


# ------------------------------------------------------------------ Jill
def mira_da_beretta(T, t, rng):
    """Jill: o ponto vermelho da mira laser encontra o alvo e treme um pouco, e então dois tiros rápidos e precisos
    no mesmo ponto."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    km = janela(t, 0.0, 0.06) * (1 - rel(t, 0.36, 0.44))
    dx, dy = 0.03 * math.sin(t * 37), 0.02 * math.cos(t * 29)
    laser = T.lines([(-0.95, 0.05, dx, dy, 0.6)], 0.006) * km
    ponto = T.gauss(dx, dy, 0.025) * km * 1.5
    balas = sum(_bala(T, t, 0.14 + 0.1 * k, 0.1, 0.05, 0.0) for k in range(2))
    boca = sum(_boca(T, t, 0.13 + 0.1 * k, y=0.05, tam=0.28) for k in range(2))
    est = _estrela_de_contato(T, t, 0.24, 0.16, 6, 0.32) + _estrela_de_contato(T, t, 0.34, 0.18, 6, 0.32, ang=0.6)
    G += (laser + ponto + balas * 1.3 + boca + est) * env
    H += (laser * 0.6 + ponto * 1.4 + balas * 1.2 + boca + est) * env
    return G, H


# ------------------------------------------------------------------ Mega Man
def mega_buster(T, t, rng):
    """Mega Man: o Mega Buster solta três "balinhas de limão" (as bolinhas amarelas ovais, uma atrás da outra), e cada
    uma estoura num brilho pequeno de oito pontas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    balas = T.zero()
    estouros = T.zero()
    for k in range(3):
        t0 = 0.0 + 0.08 * k
        u = rel(t, t0, t0 + 0.14)
        y = 0.08 * (k - 1)
        if 0 < u < 1:
            x = -0.85 + 0.85 * u
            balas += T.polys([(_elipse_pts(x, y * (1 - u), 0.06, 0.04, 0.0, 14), 1.0)], 0.003)
        estouros += T.polys([(estrela(0.03 * (k - 1), y * 0.3, 0.18 * pulso(t, t0 + 0.14, t0 + 0.34) + 0.005, 0.2, 8, 0.4), 1.0)], 0.003) * pulso(t, t0 + 0.14, t0 + 0.34)
    canhao = T.gauss(-0.88, 0, 0.06) * pulso(t, 0.0, 0.35)
    G += (balas * 1.3 + estouros + canhao) * env
    H += (balas * 1.0 + estouros + canhao) * env
    return G, H


REGISTRO = [
    ("tiro_do_coronel", tiro_do_coronel, GRANDE, "básico do Roy Mustang: o tiro e o círculo de transmutação", False),
    ("rajada_do_justiceiro", rajada_do_justiceiro, GRANDE, "básico do Justiceiro: três tiros e a caveira", False),
    ("blasters_do_quill", blasters_do_quill, GRANDE, "básico do Senhor das Estrelas: os dois blasters girando", False),
    ("canhao_do_rocket", canhao_do_rocket, GRANDE, "básico do Rocket: o canhão grande demais e o recuo", False),
    ("rajada_do_spartan", rajada_do_spartan, GRANDE, "básico do Master Chief: a rajada e o escudo em hexágonos", False),
    ("tiro_e_faca_leon", tiro_e_faca_leon, GRANDE, "básico do Leon: o tiro na cabeça e a faca", False),
    ("mira_da_beretta", mira_da_beretta, GRANDE, "básico da Jill: a mira laser e os dois tiros", False),
    ("mega_buster", mega_buster, GRANDE, "básico do Mega Man: as três balinhas do Mega Buster", False),
]
