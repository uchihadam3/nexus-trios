"""Rodada 58 das habilidades próprias: Inuyasha, Sesshomaru, Kenshin, Natsu, Erza e Asta.

Inuyasha
- garras_de_aco_inuyasha: as cinco garras vermelhas rasgando em X e o sangue (Sangrando).
- tessaiga: a espada enferrujada virando a Tessaiga gigante e o corte (Exposto).
- inuyasha_preparo: o Preparo da Ferida do Vento — a Tessaiga erguida e o vento girando na lâmina (laço).
- ferida_do_vento: as cinco garras de vento rasgando o chão em leque até todos os rivais.

Sesshomaru
- garras_venenosas: a garra verde pingando veneno e o corte no rival (Envenenado).
- chicote_de_luz_sesshomaru: o chicote de luz saindo do dedo e enrolando o rival (Preso).
- sesshomaru_preparo: o Preparo da Bakusaiga — a lua crescente na testa e a espada com o brilho verde (laço).
- bakusaiga: o corte da Bakusaiga e a carne do rival se desfazendo em veneno verde (Envenenado).

Kenshin
- postura_kenshin: a espada na bainha, o pé firme e a aura (Protegido e Acelerado).
- batoujutsu: a lâmina sakabatō saindo da bainha num relâmpago e o rival paralisado (Paralisado).
- kenshin_preparo: o Preparo do Amakakeru — o pé esquerdo à frente e a espada na bainha brilhando (laço).
- amakakeru: o passo mais rápido que a luz, o corte e o vácuo que puxa o rival.

Natsu
- punho_do_dragao_de_fogo: o punho em chamas acertando o rival (Queimando).
- rugido_do_dragao_natsu: o rugido de fogo em cone saindo da boca em todos os rivais (Queimando).
- natsu_preparo: o Preparo da Lótus carmesim — as chamas girando nas duas mãos (laço).
- lotus_carmesim: a lótus de fogo abrindo em pétalas e a explosão no rival (Queimando).

Erza
- armadura_do_ceu: as asas da armadura e a chuva de espadas em todos os rivais.
- armadura_de_adamantina: os dois escudos de adamantina se juntando na frente do trio (Escudo e Protegido).
- erza_preparo: o Preparo da Armadura do purgatório — o círculo de troca de armadura e as espadas girando (laço).
- armadura_do_purgatorio: a clava de espinhos negra descendo e o rival esmagado.

Asta
- matadora_de_demonios: a espada negra cortando a magia do rival e interrompendo o Preparo (dissipa).
- golpe_antimagia: o corte negro e os selos de magia quebrando no rival (Silenciado).
- asta_preparo: o Preparo do Black Asta — o braço do demônio e a asa negra de um lado (laço).
- black_asta: a asa negra, o salto e o corte antimagia em todos os rivais (dissipa).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, ESCUDO, ESPADA, GOTA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe,
                         surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _lamina(T, x, y, ang, comp, larg, k, curva=0.0):
    """Uma espada de lado: a lâmina (que pode curvar), a guarda e o cabo. Devolve (G, H)."""
    c, s = math.cos(ang), math.sin(ang)
    px, py = -s, c
    pts_a, pts_b = [], []
    for u in np.linspace(0, 1, 14):
        o = curva * math.sin(math.pi * u * 0.9) * comp
        w = larg * (1 - 0.85 * u ** 2)
        cx, cy = x + c * comp * u + px * o, y + s * comp * u + py * o
        pts_a.append((cx + px * w, cy + py * w))
        pts_b.append((cx - px * w * 0.4, cy - py * w * 0.4))
    g, h = icone(T, pts_a + pts_b[::-1], k * 1.2, 0.6)
    G = g + T.lines([(x + px * larg * 2.2, y + py * larg * 2.2, x - px * larg * 2.2, y - py * larg * 2.2, 1.0)], larg * 0.7) * k
    G += T.lines([(x, y, x - c * comp * 0.25, y - s * comp * 0.25, 1.0)], larg * 0.8) * k
    return G, h + T.polyline(pts_a, 0.004) * k * 0.6


def _garra(T, x, y, ang, s, k):
    pts = [(0, -0.12), (0.7, -0.08), (1.0, 0.1), (0.65, 0.02), (0, 0.12)]
    return icone(T, poe(pts, x, y, s, ang), k * 1.2, 0.7)


def _lua_crescente(T, x, y, s, k):
    G = T.arc_band(s, s * 0.3, -2.4, 0.8, 1.0, 0, x, y, 1.0, True) * k * 1.3
    return G


def _clava(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.06) * k * 1.2
    hx, hy = x + c * s * 0.95, y + sn * s * 0.95
    G += T.gauss(hx, hy, s * 0.14) * k * 1.0 + T.ring(s * 0.16, s * 0.03, hx, hy) * k * 1.2
    segs = [(hx + s * 0.15 * math.cos(a), hy + s * 0.15 * math.sin(a), hx + s * 0.28 * math.cos(a), hy + s * 0.28 * math.sin(a), 1.0)
            for a in np.linspace(0, TAU, 9, endpoint=False)]
    return G + T.tapered(segs, s * 0.05) * k * 1.3


def _asa_negra(T, x, y, s, k, lado=-1, t=0.0):
    """A asa de diabo do Asta: uma asa só, rasgada, de um lado."""
    pts = [(0, 0)]
    for j in range(5):
        a = math.pi * (0.55 + 0.1 * j)
        r = 1.0 - 0.12 * j
        pts += [(lado * -r * math.cos(a) * 0.9, -r * math.sin(a) + 0.15 * math.sin(t * 6)), (lado * -r * 0.7 * math.cos(a + 0.1), -r * 0.6 * math.sin(a + 0.1))]
    pts.append((0, 0.3))
    return icone(T, poe(pts, x, y, s), k * 1.1, 0.5)


def _selo_magia(T, x, y, r, k, quebra=0.0):
    G = T.ring(r, r * 0.08, x, y) * k * 1.2
    segs = []
    for j in range(5):
        a = TAU * j / 5 - math.pi / 2
        b = TAU * ((j + 2) % 5) / 5 - math.pi / 2
        segs.append((x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a), x + r * 0.9 * math.cos(b), y + r * 0.9 * math.sin(b), 1.0))
    G += T.lines(segs, r * 0.05) * k
    if quebra > 0:
        G += _zap(T, 581, x - r, y - r * 0.2, x + r, y + r * 0.3, r * 0.08, 4, 0.4) * quebra * 1.5
    return G


# ------------------------------------------------------------------ Inuyasha

def garras_de_aco_inuyasha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, ang in enumerate((0.7, 2.45)):
        a0 = 0.08 + 0.16 * i
        for j in range(5):
            o = (j - 2) * 0.06
            g, h = corte(T, t, a0 + 0.012 * j, a0 + 0.28 + 0.012 * j, ang, 0.9, 0.03, 0.45 + o * math.sin(ang), -0.05 - o * math.cos(ang), 0.05)
            G, H = G + g, H + h
        g, h = clarao(T, t, a0 + 0.08, a0 + 0.28, 0.45, -0.05, 1.0, 1.0)
        G, H = G + g, H + h
    q = rel(t, 0.35, 0.95)
    if 0 < q < 1:
        rr = np.random.default_rng(582)
        for _ in range(9):
            a, v = rr.uniform(-2.8, -0.3), rr.uniform(0.5, 1.0)
            x, y = 0.45 + 0.35 * v * q * math.cos(a), -0.05 + 0.3 * v * q * math.sin(a) + 0.5 * q * q
            g, h = icone(T, poe(GOTA, x, y, 0.03), 1 - q, 0.7)
            G, H = G + g, H + h
    return G * env, H * env


def tessaiga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    cresce = ease_out(rel(t, 0.05, 0.3), 2)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.55, 0.68))
    if k > 0:
        ang = -1.0 + 1.6 * ease_in(rel(t, 0.3, 0.45), 2)
        g, h = _lamina(T, -0.5, 0.15, ang, 0.35 + 0.4 * cresce, 0.035 + 0.06 * cresce, k, 0.06)
        G, H = G + g, H + h
        G += T.gauss(-0.5 + 0.3 * math.cos(ang), 0.15 + 0.3 * math.sin(ang), 0.15) * pulso(t, 0.05, 0.35) * 0.8
    g, h = corte(T, t, 0.35, 0.6, 0.9, 1.2, 0.07, 0.45, -0.05, 0.1)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.38, 0.6, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        G += T.ring(0.2, 0.012, 0.45, -0.05) * m * (0.7 + 0.3 * math.sin(t * 30))
    G += estouro(T, t, 0.38, 0.8, 12, 583, 0.45, -0.05, 0.5, 0.012)
    return G * env, H * env


def inuyasha_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _lamina(T, 0.0, 0.35, -math.pi / 2 + 0.15, 0.75, 0.08, 1.0, 0.05)
    G, H = G + g, H + h
    for j in range(3):
        a = t * TAU * 1.5 + TAU * j / 3
        G += T.arc_band(0.18 + 0.05 * j, 0.02, a, a + 2.2, 0.5, 0, 0.05, -0.1, 1.0) * 1.1
    return G, H


def ferida_do_vento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.4, 0.55))
    if k > 0:
        ang = -1.6 + 1.9 * ease_in(rel(t, 0.15, 0.32), 2)
        g, h = _lamina(T, -0.6, 0.15, ang, 0.7, 0.09, k, 0.05)
        G, H = G + g, H + h
    # as cinco garras de vento rasgando o chão em leque
    for j in range(5):
        u = rel(t, 0.3 + 0.02 * j, 0.75 + 0.02 * j)
        if 0 < u < 1:
            fim = -0.1 + 0.25 * (j - 2)
            x = -0.5 + 1.4 * ease_out(u)
            y = 0.3 + (fim - 0.3) * ease_out(u)
            G += T.tapered([(-0.5, 0.3, x, y, 1.0)], 0.06) * (1 - u) * 1.2
            G += T.arc_band(0.12, 0.02, -1.2, 1.2, 1.0, 0, x - 0.08, y, 1.0, True) * (1 - u) * 1.3
            H += T.gauss(x, y, 0.02) * (1 - u) * 1.8
    G += onda_no_chao(T, t, 0.3, 0.8, 1.0, 0.38, 1.4)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.05 * i, 0.72 + 0.05 * i, cx, -0.05, 0.8, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 26, 584, 0.0, 0.2, 0.8, 0.4, 0.012, 0.4)
    return G * env, H * env


# ------------------------------------------------------------------ Sesshomaru

def garras_venenosas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.18) * (1 - rel(t, 0.5, 0.62))
    u = ease_in(rel(t, 0.12, 0.32), 2)
    if k > 0:
        x = -0.55 + 0.75 * u
        for j in range(4):
            g, h = _garra(T, x, -0.2 + 0.11 * j, 0.2 - 0.1 * j, 0.26, k)
            G, H = G + g, H + h
        G += T.gauss(x + 0.1, -0.05, 0.16) * k * 0.8
        for j in range(3):
            d = (t * 3 + j / 3) % 1
            g, h = icone(T, poe(GOTA, x + 0.1 + 0.07 * (j - 1), 0.15 + 0.25 * d, 0.045), k * (1 - d), 0.7)
            G, H = G + g, H + h
    for j in range(4):
        g, h = corte(T, t, 0.3 + 0.01 * j, 0.55 + 0.01 * j, 0.6, 0.8, 0.03, 0.45 + 0.05 * (j - 1.5), -0.05, 0.05)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.32, 0.52, 0.45, -0.05, 1.0, 1.0)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        for j in range(5):
            r = ((t - 0.5) * 1.5 + j / 5) % 1
            G += T.ring(0.02 + 0.03 * r, 0.006, 0.38 + 0.04 * j, -0.2 - 0.3 * r) * m * (1 - r) * 1.3
        G += T.gauss(0.45, 0.0, 0.2, 0.25) * m * 0.3
    return G * env, H * env


def chicote_de_luz_sesshomaru(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.35), 1.8)
    k = 1 - rel(t, 0.85, 0.97)
    if u > 0 and k > 0:
        pts = []
        for v in np.linspace(0, 1, 40):
            if v > u:
                break
            x = -0.55 + 1.0 * v
            y = -0.1 - 0.25 * math.sin(math.pi * v) + 0.05 * math.sin(v * 14 - t * 20) * (1 - v)
            pts.append((x, y))
        if len(pts) > 1:
            G += T.polyline(pts, 0.02) * k * 1.3
            H += T.polyline(pts, 0.006) * k * 1.6
    enrola = rel(t, 0.35, 0.65)
    if enrola > 0:
        for j in range(3):
            G += T.ring(0.13 + 0.01 * j, 0.012, 0.45, -0.25 + 0.15 * j, 3.0) * min(1, enrola * 2) * k * 1.2
    H += T.gauss(-0.55, -0.1, 0.03) * pulso(t, 0.0, 0.35) * 2.0
    g, h = clarao(T, t, 0.32, 0.52, 0.45, -0.1, 0.9, 1.0)
    G, H = G + g, H + h
    G += particulas(T, t, 0.35, 1.0, 12, 585, 0.45, -0.1, 0.2, 0.3, 0.01)
    return G * env, H * env


def sesshomaru_preparo(T, t, rng):
    G, H = vazio(T)
    G += _lua_crescente(T, -0.25, -0.45, 0.1, 1.0)
    g, h = _lamina(T, -0.1, 0.35, -math.pi / 2 + 0.3, 0.75, 0.05, 1.0, 0.03)
    G, H = G + g, H + h
    G += T.gauss(0.1, -0.05, 0.12, 0.35) * (0.4 + 0.3 * math.sin(t * TAU * 2))
    for j in range(4):
        r = (t + j / 4) % 1
        G += T.ring(0.02 + 0.02 * r, 0.006, 0.15 + 0.05 * math.sin(j * 2), 0.2 - 0.6 * r) * (1 - r) * 1.3
    return G, H


def bakusaiga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.45, 0.6))
    if k > 0:
        ang = -2.0 + 2.2 * ease_in(rel(t, 0.15, 0.3), 2)
        g, h = _lamina(T, -0.45, 0.1, ang, 0.65, 0.05, k, 0.03)
        G, H = G + g, H + h
    g, h = corte(T, t, 0.25, 0.5, 0.55, 1.3, 0.06, 0.45, -0.05, 0.08)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.5, 0.45, -0.05, 1.4, 1.3)
    G, H = G + g, H + h
    # o rival se desfazendo em veneno: as bolhas e as rachaduras verdes que se espalham
    d = rel(t, 0.4, 1.0)
    if 0 < d < 1:
        for j in range(7):
            a = TAU * j / 7 + 0.3
            G += _zap(T, 586 + j, 0.45, -0.05, 0.45 + 0.35 * d * math.cos(a), -0.05 + 0.35 * d * math.sin(a), 0.009, 3, 0.4) * (1 - d) * 1.3
        for j in range(8):
            r = ((t - 0.4) * 2 + j / 8) % 1
            G += T.ring(0.02 + 0.04 * r, 0.007, 0.3 + 0.04 * j, -0.05 - 0.35 * r) * (1 - r) * (1 - d) * 1.4
    G += particulas(T, t, 0.4, 1.0, 20, 587, 0.45, 0.0, 0.3, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Kenshin

def postura_kenshin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        # a bainha na cintura com o cabo para a frente
        G += T.lines([(-0.35, 0.1, 0.25, 0.0, 1.0)], 0.04) * s * 1.1
        G += T.lines([(0.25, 0.0, 0.42, -0.03, 1.0)], 0.03) * s * 1.2
        G += T.ring(0.035, 0.01, 0.25, 0.0) * s * 1.2
        G += T.ring(0.42 * s, 0.018, 0.0, 0.0, 0.9) * 1.0
    G += anel(T, t, 0.1, 0.55, 0.1, 0.6, 0.03, 0.38, 3.0, 1.2)
    v = pulso(t, 0.3, 1.0)
    if v > 0:
        for j in range(4):
            y = -0.35 + 0.2 * j
            o = ((t * 3) + j * 0.31) % 1
            G += T.tapered([(-0.8 + 0.3 * o, y, -0.45 + 0.3 * o, y, 0.8)], 0.014) * v
    G += T.gauss(0.0, -0.05, 0.25, 0.4) * pulso(t, 0.1, 0.9) * 0.3
    G += particulas(T, t, 0.2, 1.0, 12, 588, 0.0, 0.1, 0.4, 0.5, 0.01)
    return G * env, H * env


def batoujutsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = 1 - rel(t, 0.2, 0.3)
    if k > 0:
        G += T.lines([(-0.75, 0.05, -0.3, -0.02, 1.0)], 0.035) * k * 1.1
        H += T.gauss(-0.3, -0.02, 0.02) * pulso(t, 0.05, 0.2) * 2.5
    # o saque num relâmpago: o traço horizontal que atravessa tudo
    u = rel(t, 0.18, 0.3)
    if 0 < u < 1:
        G += T.tapered([(-0.3, -0.02, -0.3 + 1.1 * u, -0.05, 1.0)], 0.04) * 1.5
    g, h = corte(T, t, 0.25, 0.48, -0.05, 1.5, 0.05, 0.2, -0.04, 0.03)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.48, 0.45, -0.05, 1.3, 1.4)
    G, H = G + g, H + h
    m = pulso(t, 0.45, 1.0)
    if m > 0:
        for j in range(3):
            G += _zap(T, 589 + j + int(t * 10), 0.45 - 0.15 + 0.15 * j, -0.3, 0.45 - 0.1 + 0.1 * j, 0.15, 0.008, 3, 0.4) * m * 1.2
        G += T.ring(0.22, 0.01, 0.45, -0.05) * m
    return G * env, H * env


def kenshin_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.5, 0.12, 0.3, 0.0, 1.0)], 0.06) * 1.1
    G += T.lines([(0.3, 0.0, 0.55, -0.04, 1.0)], 0.045) * 1.2
    G += T.ring(0.05, 0.014, 0.3, 0.0) * 1.2
    H += T.gauss(0.3, 0.0, 0.04) * (0.7 + 0.3 * math.sin(t * TAU * 3)) * 2.0
    G += T.gauss(0.0, -0.05, 0.3, 0.4) * (0.3 + 0.15 * math.sin(t * TAU * 2))
    for j in range(8):
        a = TAU * j / 8 + t * TAU
        G += T.tapered([(0.38 * math.cos(a), -0.05 + 0.38 * math.sin(a), 0.5 * math.cos(a), -0.05 + 0.5 * math.sin(a), 0.8)], 0.02) * 1.0
    return G, H


def amakakeru(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    # o passo: a silhueta borrada atravessando
    u = ease_in(rel(t, 0.08, 0.3), 2.5)
    if 0 < u < 1:
        x = -0.6 + 1.0 * u
        G += T.gauss(x, -0.05, 0.06, 0.25) * 1.2
        for j in range(6):
            G += T.tapered([(x - 0.5, -0.3 + 0.1 * j, x - 0.05, -0.3 + 0.1 * j, 0.8)], 0.02) * 1.1
    g, h = corte(T, t, 0.28, 0.5, -0.5, 1.4, 0.08, 0.45, -0.05, 0.1)
    G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.55, 0.45, -0.05, 1.8, 1.7)
    G, H = G + g, H + h
    # o vácuo que puxa: os anéis entrando no rival
    for j in range(4):
        v = rel(t, 0.45 + 0.06 * j, 0.8 + 0.06 * j)
        if 0 < v < 1:
            G += T.ring(0.6 * (1 - ease_out(v)) + 0.03, 0.025, 0.45, -0.05) * v * (1 - v) * 4.0
    G += estouro(T, t, 0.3, 0.75, 16, 590, 0.45, -0.05, 0.65, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Natsu

def punho_do_dragao_de_fogo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.58)
    if u > 0 and k > 0:
        x = -0.5 + 0.75 * u
        P, nos = _punho(T, x, -0.05, 2.3, 0)
        G += P * k
        H += nos * 0.5 * k
        for j in range(5):
            g, h = icone(T, poe(CHAMA, x - 0.12 - 0.08 * j, -0.05 + 0.05 * math.sin(t * 30 + j), 0.09 - 0.012 * j, -math.pi / 2), k * (1 - 0.15 * j), 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.5, 0.45, -0.05, 1.4, 1.4)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.65, 0.05, 0.55, 0.04, -0.05, 1.0, 1.3)
    q = pulso(t, 0.45, 1.0)
    if q > 0:
        for j in range(4):
            g, h = icone(T, poe(CHAMA, 0.33 + 0.08 * j, 0.1 - 0.04 * (j % 2), 0.08 + 0.02 * math.sin(t * 25 + j)), q, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.35, 1.0, 16, 591, 0.45, 0.0, 0.25, 0.6, 0.012)
    return G * env, H * env


def rugido_do_dragao_natsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    G += T.gauss(-0.6, -0.15, 0.08) * pulso(t, 0.0, 0.3) * 1.2
    u = rel(t, 0.1, 0.6)
    if 0 < u < 1:
        q = np.random.default_rng(592 + int(t * 20))
        for _ in range(16):
            a = q.uniform(-0.35, 0.35)
            d = 0.2 + 1.3 * ease_out(u) * q.uniform(0.6, 1.0)
            x, y = -0.6 + d * math.cos(a), -0.15 + d * math.sin(a) * 0.8
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.08 * d, -math.pi / 2 + a), (1 - u) * 0.9 + 0.1, 0.6)
            G, H = G + g, H + h
        G += T.tapered([(-0.6, -0.15, -0.6 + 1.4 * ease_out(u), -0.05, 1.0)], 0.2) * (1 - u) * 0.6
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.4 + 0.05 * i, 0.62 + 0.05 * i, cx, -0.05, 0.7, 0.9)
        G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 24, 593, 0.1, -0.05, 0.8, 0.5, 0.012)
    return G * env, H * env


def natsu_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        cx = lado * 0.3
        G += T.gauss(cx, 0.0, 0.13) * 0.9
        for j in range(5):
            a = t * TAU * 2 * lado + TAU * j / 5
            g, h = icone(T, poe(CHAMA, cx + 0.17 * math.cos(a), 0.0 + 0.17 * math.sin(a), 0.11, a + math.pi / 2), 1.0, 0.6)
            G, H = G + g, H + h
    return G, H


def lotus_carmesim(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    u = ease_in(rel(t, 0.05, 0.28), 2)
    k = 1 - rel(t, 0.4, 0.52)
    if u > 0 and k > 0:
        for lado in (-1, 1):
            P, nos = _punho(T, -0.5 + 0.75 * u, -0.05 + lado * 0.1, 2.0, 0)
            G += P * k * 0.9
        G += T.tapered([(-0.95, -0.05, -0.6 + 0.75 * u, -0.05, 1.0)], 0.12) * k * 0.6
    # a lótus de fogo: as pétalas abrindo em volta do rival
    ab = ease_out(rel(t, 0.3, 0.6), 2)
    kk = 1 - rel(t, 0.75, 0.92)
    if ab > 0 and kk > 0:
        for j in range(8):
            a = TAU * j / 8 + 0.2
            g, h = icone(T, poe(CHAMA, 0.45 + 0.22 * ab * math.cos(a), -0.05 + 0.22 * ab * math.sin(a), 0.1 * ab + 0.01, a + math.pi / 2), kk * 1.1, 0.6)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.6, 0.45, -0.05, 2.0, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.55, 0.95, 0.1, 0.9, 0.05, -0.05, 1.0, 1.5)
    G += estouro(T, t, 0.55, 0.95, 18, 594, 0.45, -0.05, 0.7, 0.015)
    G += particulas(T, t, 0.55, 1.0, 22, 595, 0.45, 0.0, 0.35, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Erza

def armadura_do_ceu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.6, 0.75))
    if s > 0:
        for lado in (-1, 1):
            for j in range(4):
                a = -math.pi / 2 + lado * (0.5 + 0.25 * j)
                G += T.tapered([(-0.6, -0.1, -0.6 + 0.35 * s * math.cos(a), -0.1 + 0.35 * s * math.sin(a), 1.0)], 0.035) * 1.1
    # a chuva de espadas em todos os rivais
    q = np.random.default_rng(596)
    for j in range(12):
        cx = [-0.45, 0.0, 0.45][j % 3] + q.uniform(-0.15, 0.15)
        a0 = 0.25 + q.uniform(0, 0.3)
        u = rel(t, a0, a0 + 0.25)
        if 0 < u < 1:
            y = -0.9 + 1.0 * ease_in(u, 2)
            g, h = icone(T, poe(ESPADA, cx, y, 0.1, 0), 1.1, 0.5)
            G, H = G + g, H + h
            G += T.tapered([(cx, y - 0.35, cx, y - 0.1, 0.6)], 0.02)
        elif u >= 1:
            G += T.lines([(cx, 0.0, cx, 0.12, 1.0)], 0.015) * (1 - rel(t, 0.85, 1)) * 1.2
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.04 * i, 0.7 + 0.04 * i, cx, 0.0, 0.7, 0.9)
        G, H = G + g, H + h
    return G * env, H * env


def armadura_de_adamantina(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    junta = ease_out(rel(t, 0.1, 0.4), 2.5)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        for lado in (-1, 1):
            x = lado * (0.7 - 0.45 * junta) + 0.1
            meia = [(px * 0.5 + lado * 0.25, py) for px, py in ESCUDO if (px <= 0.02 if lado < 0 else px >= -0.02)]
            g, h = icone(T, poe(meia, x - lado * 0.12, -0.05, 0.42 * k), 1.1, 0.5)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.35, 0.55, 0.1, -0.05, 1.2, 1.2)
    G, H = G + g, H + h
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.85, 1))
    if m > 0:
        for cx in (-0.45, 0.0, 0.45):
            G += T.ring(0.25 * m, 0.014, cx, 0.0, 0.9) * 1.1
    G += anel(T, t, 0.38, 0.8, 0.1, 0.9, 0.035, 0.05, 2.5, 1.3)
    return G * env, H * env


def erza_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.38, 0.016, 0.0, -0.05) * 1.0 + T.ring(0.3, 0.008, 0.0, -0.05) * 0.8
    for j in range(5):
        a = t * TAU + TAU * j / 5
        g, h = icone(T, poe(ESPADA, 0.34 * math.cos(a), -0.05 + 0.34 * math.sin(a), 0.08, a + math.pi), 1.0, 0.5)
        G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.15) * (0.4 + 0.3 * math.sin(t * TAU * 3))
    return G, H


def armadura_do_purgatorio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.18) * (1 - rel(t, 0.55, 0.68))
    if k > 0:
        ang = -2.4 + 1.6 * ease_in(rel(t, 0.15, 0.38), 2.2)
        G += _clava(T, -0.1, 0.35, ang, 0.65, k)
        G += T.arc_band(0.65, 0.07, ang - 0.8, ang, 1.0, 0, -0.1, 0.35, 1.0) * k * pulso(t, 0.15, 0.4) * 0.8
    g, h = clarao(T, t, 0.35, 0.6, 0.45, -0.05, 1.8, 1.7)
    G, H = G + g, H + h
    for j in range(5):
        lado = -1 if j % 2 else 1
        G += _zap(T, 597 + j, 0.45, 0.38, 0.45 + lado * (0.15 + 0.08 * (j // 2)) * ease_out(rel(t, 0.38, 0.55)), 0.38 + 0.02 * (j % 3 - 1), 0.012, 4, 0.12) * (1 - rel(t, 0.85, 0.97)) * 1.2
    G += onda_no_chao(T, t, 0.38, 0.9, 0.85, 0.38, 1.6)
    G += estouro(T, t, 0.38, 0.85, 16, 598, 0.45, -0.05, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Asta

def matadora_de_demonios(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # o círculo de magia do rival (o Preparo) que vai ser cortado
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.42, 0.5))
    if s > 0:
        G += _selo_magia(T, 0.45, -0.05, 0.25 * s, 1.0)
    k = surge(t, 0.05, 0.2) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        ang = -1.8 + 2.4 * ease_in(rel(t, 0.2, 0.38), 2)
        g, h = _lamina(T, -0.35, 0.1, ang, 0.75, 0.09, k, 0.0)
        G, H = G + g * 0.7, H + h * 0.3
    g, h = corte(T, t, 0.32, 0.55, 0.85, 1.2, 0.08, 0.45, -0.05, 0.0)
    G, H = G + g, H + h * 0.4
    # os cacos do selo voando (a magia dissipada)
    d = rel(t, 0.4, 0.9)
    if 0 < d < 1:
        q = np.random.default_rng(599)
        for _ in range(10):
            a, v = q.uniform(0, TAU), q.uniform(0.5, 1)
            x, y = 0.45 + 0.4 * v * d * math.cos(a), -0.05 + 0.4 * v * d * math.sin(a)
            G += T.lines([(x - 0.03, y, x + 0.03, y + 0.02, 1.0)], 0.01) * (1 - d) * 1.3
    G += T.gauss(0.45, -0.05, 0.25) * pulso(t, 0.35, 0.7) * 0.4
    return G * env, H * env


def golpe_antimagia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.18) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        ang = -2.0 + 2.6 * ease_in(rel(t, 0.15, 0.32), 2)
        g, h = _lamina(T, -0.45, 0.15, ang, 0.7, 0.08, k, 0.0)
        G, H = G + g * 0.8, H + h * 0.3
        G += T.gauss(-0.2, -0.05, 0.25, 0.2) * k * 0.25
    g, h = corte(T, t, 0.25, 0.48, 1.0, 1.2, 0.07, 0.45, -0.05, 0.05)
    G, H = G + g, H + h * 0.5
    for j in range(3):
        cx, cy = 0.45 + 0.2 * (j - 1), -0.42 + 0.06 * (j % 2)
        s = surge(t, 0.3 + 0.04 * j, 0.45 + 0.04 * j) * (1 - rel(t, 0.85, 1))
        if s > 0:
            G += _selo_magia(T, cx, cy, 0.08 * s, 1.0, rel(t, 0.5, 0.6))
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        G += T.ring(0.08, 0.012, 0.45, 0.05) * m * 1.2 + T.lines([(0.39, 0.0, 0.51, 0.1, 1.0)], 0.012) * m * 1.3
    G += estouro(T, t, 0.3, 0.7, 12, 600, 0.45, -0.05, 0.45, 0.012)
    return G * env, H * env


def asta_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _asa_negra(T, -0.1, -0.05, 0.62, 1.0, -1, t)
    G, H = G + g, H + h
    G += T.lines([(0.0, -0.05, 0.4, 0.25, 1.0)], 0.08) * 1.0
    q = np.random.default_rng(601 + int(t * 15))
    for _ in range(3):
        x0 = q.uniform(0.0, 0.4)
        G += T.polyline(jagged(q, x0, -0.05 + x0 * 0.75, x0 + 0.15, -0.05 + x0 * 0.75 + q.uniform(-0.15, 0.15), 3, 0.4), 0.01) * 1.2
    return G, H


def black_asta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.62))
    sobe = ease_out(rel(t, 0.1, 0.3), 2) * (1 - ease_in(rel(t, 0.3, 0.45), 2))
    if s > 0:
        g, h = _asa_negra(T, -0.4, -0.15 - 0.4 * sobe, 0.35 * s, 1.0, -1, t)
        G, H = G + g, H + h
        g, h = _lamina(T, -0.35, -0.1 - 0.4 * sobe, -0.7 + 1.6 * rel(t, 0.3, 0.45), 0.6, 0.08, s, 0.0)
        G, H = G + g * 0.8, H + h * 0.3
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = corte(T, t, 0.38 + 0.04 * i, 0.62 + 0.04 * i, 0.9 + 0.3 * (i - 1), 0.9, 0.06, cx, -0.05, 0.05)
        G, H = G + g, H + h * 0.5
        g, h = clarao(T, t, 0.4 + 0.04 * i, 0.62 + 0.04 * i, cx, -0.05, 0.8, 0.9)
        G, H = G + g, H + h * 0.6
        m = pulso(t, 0.55 + 0.04 * i, 1.0)
        if m > 0:
            G += _selo_magia(T, cx, -0.42, 0.07, m, 1.0)
    G += onda_no_chao(T, t, 0.42, 0.9, 1.0, 0.38, 1.4)
    G += particulas(T, t, 0.45, 1.0, 22, 602, 0.0, 0.0, 0.8, 0.5, 0.013)
    return G * env, H * env


REGISTRO = [
    ("garras_de_aco_inuyasha", garras_de_aco_inuyasha, GRANDE, "Inuyasha · as garras em X e o sangue", False),
    ("tessaiga", tessaiga, GRANDE, "Inuyasha · a Tessaiga crescendo e o corte", False),
    ("inuyasha_preparo", inuyasha_preparo, MEDIA, "Inuyasha · a Tessaiga e o vento (Preparo, laço)", True),
    ("ferida_do_vento", ferida_do_vento, GRANDE, "Inuyasha · as cinco garras de vento", False),
    ("garras_venenosas", garras_venenosas, GRANDE, "Sesshomaru · a garra pingando veneno", False),
    ("chicote_de_luz_sesshomaru", chicote_de_luz_sesshomaru, GRANDE, "Sesshomaru · o chicote de luz enrolando", False),
    ("sesshomaru_preparo", sesshomaru_preparo, MEDIA, "Sesshomaru · a lua e a Bakusaiga (Preparo, laço)", True),
    ("bakusaiga", bakusaiga, GRANDE, "Sesshomaru · o corte e o veneno se espalhando", False),
    ("postura_kenshin", postura_kenshin, GRANDE, "Kenshin · a espada na bainha e a aura", False),
    ("batoujutsu", batoujutsu, GRANDE, "Kenshin · o saque num relâmpago", False),
    ("kenshin_preparo", kenshin_preparo, MEDIA, "Kenshin · a bainha brilhando (Preparo, laço)", True),
    ("amakakeru", amakakeru, GRANDE, "Kenshin · o passo, o corte e o vácuo", False),
    ("punho_do_dragao_de_fogo", punho_do_dragao_de_fogo, GRANDE, "Natsu · o punho em chamas", False),
    ("rugido_do_dragao_natsu", rugido_do_dragao_natsu, GRANDE, "Natsu · o rugido de fogo em cone", False),
    ("natsu_preparo", natsu_preparo, MEDIA, "Natsu · as chamas nas duas mãos (Preparo, laço)", True),
    ("lotus_carmesim", lotus_carmesim, GRANDE, "Natsu · a lótus de fogo abrindo", False),
    ("armadura_do_ceu", armadura_do_ceu, GRANDE, "Erza · as asas e a chuva de espadas", False),
    ("armadura_de_adamantina", armadura_de_adamantina, GRANDE, "Erza · os dois escudos se juntando", False),
    ("erza_preparo", erza_preparo, MEDIA, "Erza · as espadas girando no círculo (Preparo, laço)", True),
    ("armadura_do_purgatorio", armadura_do_purgatorio, GRANDE, "Erza · a clava de espinhos", False),
    ("matadora_de_demonios", matadora_de_demonios, GRANDE, "Asta · a espada negra cortando a magia", False),
    ("golpe_antimagia", golpe_antimagia, GRANDE, "Asta · o corte e os selos quebrando", False),
    ("asta_preparo", asta_preparo, MEDIA, "Asta · a asa negra (Preparo, laço)", True),
    ("black_asta", black_asta, GRANDE, "Asta · a asa negra e os cortes em todos", False),
]
