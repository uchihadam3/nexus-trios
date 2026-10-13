"""Rodada 55 das habilidades próprias: Gandalf, Godzilla, King Kong, Shrek, Elsa e Malévola.

Gandalf
- voce_nao_vai_passar: o cajado batendo na ponte e a parede de luz branca na frente do trio (Barreira e Protegido).
- luz_de_gandalf: o cajado acendendo como um sol branco, cegando os rivais e curando o trio (Cego e Vida).
- gandalf_preparo: o Preparo da Glamdring — o chapéu pontudo, o cajado e a espada brilhando (laço).
- glamdring: a espada élfica azulada cortando em arco.

Godzilla
- pisao_de_godzilla: a pata enorme descendo e o chão tremendo em todos (Lento).
- couraca: as placas das costas acendendo em azul e a couraça (Escudo e Protegido).
- godzilla_preparo: o Preparo do Sopro atômico — as placas dorsais acendendo uma a uma (laço).
- sopro_atomico: o raio azul atômico varrendo todos os rivais (Queimando).

King Kong
- soco_gigante_kong: o punho gigante e o rival voando (Exposto).
- bater_no_peito: o Kong batendo no peito e as ondas do rugido (Provocado e Fortalecido).
- kong_preparo: o Preparo do Machado — o machado de osso com o machado de energia brilhando (laço).
- machado_de_kong: o machado de energia descendo e o corte que racha o chão.

Shrek
- arroto: o arroto verde em onda sobre os rivais e as moscas (Provocado e Enfraquecido).
- abraco_de_ogro: os braços verdes em volta do aliado e o escudo de lama (Escudo e Protegido).
- shrek_preparo: o Preparo do Rugido do pântano — as orelhas de trompete e as bolhas do pântano (laço).
- rugido_do_pantano: o rugido do ogro em ondas, o pântano subindo e prendendo o rival (Preso).

Elsa
- rajada_de_gelo_elsa: os flocos de neve girando na mão e o raio de gelo congelando o rival (Congelado).
- muralha_de_gelo_elsa: os cristais de gelo crescendo na frente do trio (Barreira e Escudo).
- elsa_preparo: o Preparo do Inverno eterno — o floco de neve gigante girando sobre ela (laço).
- inverno_eterno: a nevasca, o gelo crescendo no chão e congelando todos os rivais (Congelado e Lento).

Malévola
- maldicao_do_sono: o fogo verde, o fuso da roca e o rival caindo no sono (Dormindo e Amaldiçoado).
- muro_de_espinhos: os galhos de espinhos subindo e prendendo todos os rivais (Preso).
- malevola_preparo: o Preparo da Forma de dragão — os chifres e o fogo verde girando no cajado (laço).
- forma_de_dragao: a cabeça de dragão e o sopro de fogo verde em todos os rivais (Queimando).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe,
                         surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _floco(T, cx, cy, s, ang, k):
    segs = []
    for j in range(6):
        a = ang + TAU * j / 6
        x2, y2 = cx + s * math.cos(a), cy + s * math.sin(a)
        segs.append((cx, cy, x2, y2, 1.0))
        for f in (0.45, 0.7):
            bx, by = cx + s * f * math.cos(a), cy + s * f * math.sin(a)
            for lado in (-1, 1):
                b = a + lado * 0.7
                segs.append((bx, by, bx + s * 0.25 * math.cos(b), by + s * 0.25 * math.sin(b), 1.0))
    return T.lines(segs, max(0.004, s * 0.06)) * k * 1.3


def _cristal(T, cx, cy, s, k):
    pts = [(cx - s * 0.5, cy), (cx - s * 0.25, cy - s * 1.0), (cx, cy - s * 0.3), (cx + s * 0.15, cy - s * 1.2), (cx + s * 0.35, cy - s * 0.4),
           (cx + s * 0.6, cy - s * 0.8), (cx + s * 0.55, cy)]
    return icone(T, pts, k, 0.4)


def _cajado(T, x, y, s, k, luz=1.0):
    G = T.lines([(x, y + s, x, y - s * 0.8, 1.0)], s * 0.05) * k * 1.2
    G += T.polyline([(x, y - s * 0.8), (x + s * 0.12, y - s * 0.95), (x + s * 0.05, y - s * 1.05), (x - s * 0.08, y - s * 0.95)], s * 0.04) * k * 1.1
    H = T.gauss(x, y - s * 0.95, s * 0.06) * k * 1.5 * luz
    return G + T.gauss(x, y - s * 0.95, s * 0.15) * k * 0.6 * luz, H


def _espada(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.tapered([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.07) * k * 1.3
    G += T.lines([(x - sn * s * 0.12, y + c * s * 0.12, x + sn * s * 0.12, y - c * s * 0.12, 1.0)], s * 0.04) * k * 1.1
    G += T.lines([(x - c * s * 0.2, y - sn * s * 0.2, x, y, 1.0)], s * 0.05) * k * 1.0
    return G, T.lines([(x, y, x + c * s * 0.9, y + sn * s * 0.9, 1.0)], s * 0.015) * k * 1.4


def _placas(T, cx, cy, s, k, acesas=1.0, t=0.0):
    G, H = 0.0, 0.0
    for j in range(5):
        x = cx - s * 0.8 + s * 0.4 * j
        h = s * (0.5 + 0.3 * math.sin(math.pi * j / 4))
        pts = [(x - s * 0.15, cy), (x - s * 0.05, cy - h * 0.6), (x, cy - h), (x + s * 0.08, cy - h * 0.55), (x + s * 0.15, cy)]
        on = 1.0 if acesas >= (j + 1) / 5 else 0.25
        g, hh = icone(T, pts, k * (0.6 + 0.6 * on), 0.4 + 0.3 * on)
        G, H = G + g, H + hh
        H = H + T.gauss(x, cy - h * 0.5, s * 0.08) * k * on * 1.4
    return G, H


def _machado_energia(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.06) * k * 1.2
    hx, hy = x + c * s, y + sn * s
    lam = [(hx + sn * s * 0.05, hy - c * s * 0.05), (hx + sn * s * 0.35 - c * s * 0.15, hy - c * s * 0.35 - sn * s * 0.15),
           (hx + sn * s * 0.4 + c * s * 0.1, hy - c * s * 0.4 + sn * s * 0.1), (hx + sn * s * 0.3 + c * s * 0.3, hy - c * s * 0.3 + sn * s * 0.3),
           (hx + c * s * 0.15, hy + sn * s * 0.15)]
    g, h = icone(T, lam, k * 1.2, 0.6)
    return G + g + T.gauss(hx + sn * s * 0.25, hy - c * s * 0.25, s * 0.25) * k * 0.4, h * 1.3


def _galho_espinhos(T, x0, y0, x1, y1, k, seed, w=0.02):
    q = np.random.default_rng(seed)
    pts = jagged(q, x0, y0, x1, y1, 3, 0.15)
    G = T.polyline(pts, w) * k * 1.2
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mx, my = (ax + bx) / 2, (ay + by) / 2
        a = math.atan2(by - ay, bx - ax) + (math.pi / 2) * (1 if q.random() > 0.5 else -1) + 0.4
        G += T.polys([([(mx - w * 0.8 * math.cos(a + math.pi / 2), my - w * 0.8 * math.sin(a + math.pi / 2)),
                        (mx + w * 0.8 * math.cos(a + math.pi / 2), my + w * 0.8 * math.sin(a + math.pi / 2)),
                        (mx + w * 3 * math.cos(a), my + w * 3 * math.sin(a))], 1.0)], 0.002) * k * 1.3
    return G


# ------------------------------------------------------------------ Gandalf

def voce_nao_vai_passar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    bate = ease_in(rel(t, 0.0, 0.2), 2)
    k = 1 - rel(t, 0.85, 0.97)
    g, h = _cajado(T, -0.05, 0.05 + 0.1 * bate * (1 - rel(t, 0.2, 0.3)), 0.35, k, 1.0 + pulso(t, 0.18, 0.4))
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.18, 0.4, -0.05, 0.38, 1.2, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.2, 0.6, 1.0, 0.38, 1.6)
    s = ease_out(rel(t, 0.25, 0.5), 2)
    if s > 0 and k > 0:
        G += T.gauss(0.25, -0.05, 0.04, 0.45 * s) * k * 1.0
        H += T.gauss(0.25, -0.05, 0.015, 0.4 * s) * k * 1.4
        for m in range(3):
            y = -0.4 + 0.35 * m * s + 0.12 * ((t * 1.5 + m / 3) % 1)
            G += T.lines([(0.2, y, 0.3, y, 1.0)], 0.006) * k * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = pulso(t, 0.4 + 0.05 * i, 1.0)
        G += T.ring(0.16, 0.01, cx, 0.3, 3.0) * m * 1.0
    return G * env, H * env


def luz_de_gandalf(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = pulso(t, 0.0, 0.85)
    g, h = _cajado(T, 0.0, 0.0, 0.35, s, 1.0 + 2.0 * pulso(t, 0.2, 0.6))
    G, H = G + g, H + h
    f = pulso(t, 0.25, 0.65)
    if f > 0:
        H += T.flare(0.0, -0.33, 1.3 * f + 0.01, 0.0, 0.015) * 1.5 + T.flare(0.0, -0.33, 0.9 * f + 0.01, math.pi / 2, 0.012) * 1.5
        G += T.gauss(0.0, -0.33, 0.35 * f + 0.01) * 0.6
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        m = pulso(t, 0.45 + 0.05 * i, 1.0)
        if m > 0:
            for lado in (-1, 1):
                G += T.lines([(cx + lado * 0.06 - 0.03, -0.12, cx + lado * 0.06 + 0.03, -0.06, 1.0),
                              (cx + lado * 0.06 + 0.03, -0.12, cx + lado * 0.06 - 0.03, -0.06, 1.0)], 0.009) * m * 1.2
    G += particulas(T, t, 0.4, 1.0, 16, 195, 0.0, 0.3, 0.7, 0.5, 0.011)
    return G * env, H * env


def gandalf_preparo(T, t, rng):
    G, H = vazio(T)
    chapeu = [(-0.5, 0.15), (-0.2, 0.05), (0.05, -0.9), (0.12, -0.85), (0.2, 0.05), (0.5, 0.15), (0.5, 0.25), (-0.5, 0.25)]
    g, h = icone(T, poe(chapeu, -0.1, -0.1, 0.25), 1.0, 0.35)
    G, H = G + g, H + h
    g2, h2 = _cajado(T, -0.4, 0.05, 0.3, 1.0, 0.8 + 0.4 * math.sin(t * TAU * 2))
    G, H = G + g2, H + h2
    g3, h3 = _espada(T, 0.15, 0.3, -1.3, 0.5, 1.0)
    G, H = G + g3, H + h3
    b = (t * 1.5) % 1
    H += T.gauss(0.15 + 0.5 * b * math.cos(-1.3), 0.3 + 0.5 * b * math.sin(-1.3), 0.02) * 1.6
    return G, H


def glamdring(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.3 + 2.5 * u
        g, h = _espada(T, -0.05 + 0.05 * math.cos(ang), 0.25, ang, 0.6, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.55, 0.07, ang - 1.0, ang, 1.0, 0, -0.05, 0.25, 1.0) * k * 0.8
    g2, h2 = corte(T, t, 0.3, 0.52, 0.6, 1.3, 0.09, 0.45, 0.0, 0.1)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.32, 0.55, 0.45, 0.0, 1.4, 1.4)
    G, H = G + g3, H + h3
    G += anel(T, t, 0.34, 0.75, 0.05, 0.55, 0.04, 0.0)
    G += particulas(T, t, 0.35, 0.95, 14, 196, 0.45, 0.0, 0.25, 0.4, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Godzilla

def pisao_de_godzilla(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        y = -0.7 + 0.95 * u
        pata = [(-0.4, -0.3), (0.4, -0.3), (0.45, 0.15), (0.5, 0.25), (0.25, 0.22), (0.15, 0.3), (0.0, 0.22), (-0.15, 0.3), (-0.25, 0.22),
                (-0.5, 0.25), (-0.45, 0.15)]
        g, h = icone(T, poe(pata, 0.0, y, 0.3), k * 1.1, 0.45)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.28, 0.5, 0.0, 0.35, 1.8, 1.5)
    G, H = G + g2, H + h2
    for j in range(3):
        G += onda_no_chao(T, t, 0.3 + 0.06 * j, 0.95, 1.1, 0.38, 1.6 - 0.3 * j)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        G += estouro(T, t, 0.35 + 0.05 * i, 0.85, 8, 197 + i, cx, 0.35, 0.25, 0.012)
    return G * env, H * env


def couraca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    acesas = ease_out(rel(t, 0.05, 0.45), 1.2)
    g, h = _placas(T, 0.0, 0.1, 0.35, k, acesas, t)
    G, H = G + g, H + h
    s = surge(t, 0.4, 0.62)
    if s > 0 and k > 0:
        G += T.arc_band(0.38 * s, 0.035, math.pi, TAU, 1.0, 0, 0.0, 0.25, 0.0) * k * 1.2
        G += T.gauss(0.0, 0.05, 0.3, 0.2) * k * s * 0.3
        brilho = (t * 1.3) % 1
        a = math.pi + math.pi * brilho
        H += T.gauss(0.38 * s * math.cos(a), 0.25 + 0.38 * s * math.sin(a), 0.02) * k * 1.6
    return G * env, H * env


def godzilla_preparo(T, t, rng):
    G, H = vazio(T)
    acesas = (t * 1.3) % 1.2
    g, h = _placas(T, 0.0, 0.15, 0.3, 1.0, acesas, t)
    G, H = G + g, H + h
    H += T.gauss(0.0, 0.0, 0.25, 0.15) * 0.3 * min(1.0, acesas)
    return G, H


def sopro_atomico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    acesas = ease_out(rel(t, 0.0, 0.25), 1.2)
    kk = 1 - rel(t, 0.3, 0.4)
    if kk > 0:
        g, h = _placas(T, -0.6, -0.15, 0.17, kk, acesas, t)
        G, H = G + g, H + h
    k = pulso(t, 0.25, 0.85)
    if k > 0:
        varre = rel(t, 0.25, 0.75)
        tx = -0.6 + 1.2 * varre
        G += T.tapered([(-0.55, -0.3, tx, 0.05, 1.0)], 0.2) * k * 0.7
        G += T.lines([(-0.55, -0.3, tx, 0.05, 1.0)], 0.04) * k * 1.4
        H += T.lines([(-0.55, -0.3, tx, 0.05, 1.0)], 0.015) * k * 1.4
        q = np.random.default_rng(int(t * 30))
        for _ in range(6):
            u = q.uniform(0.2, 1.0)
            G += T.gauss(-0.55 + (tx + 0.55) * u, -0.3 + 0.35 * u + q.uniform(-0.03, 0.03), 0.015) * k * 1.2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.3 + 0.15 * i
        g2, h2 = clarao(T, t, a0, a0 + 0.2, cx, 0.05, 0.6, 1.2)
        G, H = G + g2, H + h2
        kk2 = pulso(t, a0 + 0.1, 1.0)
        if kk2 > 0:
            for m in range(3):
                g3, h3 = icone(T, poe(CHAMA, cx - 0.08 + 0.08 * m, 0.15 - 0.02 * math.sin(t * 25 + m + i), 0.045), kk2 * 1.0, 0.7)
                G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ King Kong

def soco_gigante_kong(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.32), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.45 + 0.7 * u, 0.0, 3.4, 0)
        G += P * k
        H += nos * 0.5 * k
        G += T.tapered([(-0.95, 0.0, -0.45 + 0.7 * u - 0.15, 0.0, 0.8)], 0.12) * k * 0.6
    g, h = clarao(T, t, 0.3, 0.55, 0.45, 0.0, 1.8, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.32, 0.75, 0.05, 0.75, 0.05, 0.0, 1.0, 1.5)
    w = rel(t, 0.35, 0.8)
    if 0 < w < 1:
        G += T.tapered([(0.45 + 0.4 * w - 0.25, -0.2 * w, 0.45 + 0.4 * w, -0.25 * w, 0.8)], 0.04) * (1 - w) * 1.2
    G += estouro(T, t, 0.33, 0.85, 16, 200, 0.45, 0.0, 0.65, 0.014)
    return G * env, H * env


def bater_no_peito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        a0 = 0.05 + 0.12 * j
        lado = -1 if j % 2 else 1
        bate = pulso(t, a0, a0 + 0.12)
        P, nos = _punho(T, -0.55 + lado * 0.08, -0.05 + 0.05 * bate, 1.4, lado * 0.3)
        G += P * pulso(t, 0.0, 0.7) * 0.6
        g2, h2 = clarao(T, t, a0 + 0.04, a0 + 0.12, -0.55, -0.05, 0.4, 0.7)
        G, H = G + g2, H + h2
        u = rel(t, a0 + 0.05, a0 + 0.5)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 0.9 * u, 0.035 * (1 - 0.5 * u), -0.6, 0.6, 0.75, 0, -0.5, -0.05, 0.0) * (1 - u) * 1.2
    for i, cx in enumerate((0.0, 0.55)):
        m = surge(t, 0.5 + 0.06 * i, 0.68 + 0.06 * i) * (1 - rel(t, 0.88, 1))
        if m > 0:
            for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
                x, y = cx + 0.06 * math.cos(a + math.pi / 4), -0.3 + 0.06 * math.sin(a + math.pi / 4)
                G += T.arc_band(0.05 * m, 0.014, a + 0.4, a + 1.2, 1.0, 0, x, y, 0.0) * 1.3
    G += T.gauss(-0.55, 0.0, 0.3, 0.35) * pulso(t, 0.4, 1.0) * 0.35
    return G * env, H * env


def kong_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _machado_energia(T, -0.15, 0.35, -1.2, 0.55, 1.0 + 0.3 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 10))
    for _ in range(4):
        H += T.gauss(0.1 + q.uniform(-0.15, 0.15), -0.25 + q.uniform(-0.15, 0.15), 0.01) * 1.6
    return G, H


def machado_de_kong(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2.2)
    k = 1 - rel(t, 0.55, 0.65)
    if k > 0:
        ang = -2.3 + 1.9 * u
        g, h = _machado_energia(T, -0.15, 0.4, ang, 0.6, k)
        G, H = G + g, H + h
        if 0 < u < 1:
            G += T.arc_band(0.75, 0.08, ang - 0.9, ang, 1.0, 0, -0.15, 0.4, 1.0) * k * 0.7
    g2, h2 = clarao(T, t, 0.33, 0.6, 0.45, 0.1, 1.8, 1.6)
    G, H = G + g2, H + h2
    racha = ease_out(rel(t, 0.35, 0.55), 2)
    if racha > 0:
        kk = 1 - rel(t, 0.85, 0.97)
        for j in range(5):
            lado = -1 if j % 2 else 1
            G += _zap(T, 201 + j, 0.45, 0.38, 0.45 + lado * (0.2 + 0.1 * (j // 2)) * racha, 0.38 + 0.03 * (j % 3 - 1), 0.014, 4, 0.12) * kk * 1.3
    G += onda_no_chao(T, t, 0.35, 0.9, 0.9, 0.38, 1.6)
    G += estouro(T, t, 0.35, 0.85, 16, 206, 0.45, 0.1, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Shrek

def _orelha(T, cx, cy, s, ang, k):
    c, sn = math.cos(ang), math.sin(ang)
    pts = [(cx - sn * s * 0.15, cy + c * s * 0.15), (cx + c * s * 0.7 - sn * s * 0.08, cy + sn * s * 0.7 + c * s * 0.08),
           (cx + c * s * 1.0 - sn * s * 0.2, cy + sn * s * 1.0 + c * s * 0.2), (cx + c * s * 1.0 + sn * s * 0.2, cy + sn * s * 1.0 - c * s * 0.2),
           (cx + c * s * 0.7 + sn * s * 0.08, cy + sn * s * 0.7 - c * s * 0.08), (cx + sn * s * 0.15, cy - c * s * 0.15)]
    return icone(T, pts, k, 0.45)


def arroto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        u = rel(t, 0.05 + 0.04 * j, 0.6 + 0.04 * j)
        if 0 < u < 1:
            x = -0.5 + 1.3 * ease_out(u, 1.4) * (0.5 + 0.12 * j)
            G += T.gauss(x, -0.05 + 0.05 * math.sin(u * 8 + j), 0.12 + 0.1 * u, 0.1 + 0.06 * u) * (1 - rel(u, 0.7, 1)) * 0.3
    for j in range(3):
        u = rel(t, 0.15 + 0.06 * j, 0.6 + 0.06 * j)
        if 0 < u < 1:
            G += T.arc_band(0.1 + 0.9 * u, 0.04 * (1 - 0.5 * u), -0.5, 0.5, 0.75, 0, -0.5, -0.05, 0.0) * (1 - u) * 1.1
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.4 + 0.05 * i, 1.0)
        if k > 0:
            for m in range(3):
                a = t * 12 + TAU * m / 3 + i
                x, y = cx + 0.12 * math.cos(a), -0.25 + 0.05 * math.sin(a * 1.3)
                G += T.gauss(x, y, 0.012) * k * 1.6
                G += T.lines([(x - 0.015, y - 0.01, x - 0.03, y - 0.025, 1.0), (x + 0.015, y - 0.01, x + 0.03, y - 0.025, 1.0)], 0.004) * k * 1.2
    return G * env, H * env


def abraco_de_ogro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    fecha = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.85, 0.97)
    for lado in (-1, 1):
        a0 = math.pi if lado < 0 else 0.0
        r = 0.3 - 0.05 * fecha
        G += T.arc_band(r, 0.09, a0 - lado * 1.6 * fecha, a0 + 0.01, 0.8, 0, 0.0, 0.05, 0.0) * k * 1.1
    s = surge(t, 0.35, 0.6)
    if s > 0 and k > 0:
        G += T.arc_band(0.32 * s, 0.03, math.pi, TAU, 1.0, 0, 0.0, 0.25, 0.0) * k * 1.2
        G += T.gauss(0.0, 0.05, 0.22, 0.25) * k * s * 0.35
        q = np.random.default_rng(207)
        for _ in range(8):
            a = q.uniform(math.pi, TAU)
            G += T.gauss(0.32 * s * math.cos(a), 0.25 + 0.32 * s * math.sin(a), 0.02) * k * 0.8
    return G * env, H * env


def shrek_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        vib = 0.05 * math.sin(t * TAU * 3)
        g, h = _orelha(T, lado * 0.12, -0.1, 0.25, -math.pi / 2 + lado * (0.9 + vib), 1.1)
        G, H = G + g, H + h
    G += T.gauss(0.0, 0.1, 0.17, 0.15) * 0.7
    for j in range(5):
        u = (t * 1.2 + j / 5) % 1
        x = -0.3 + 0.15 * j
        G += T.ring(0.015 + 0.02 * u, 0.006, x, 0.38 - 0.15 * u) * (1 - u) * 1.3
    return G, H


def rugido_do_pantano(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        u = rel(t, 0.05 + 0.07 * j, 0.5 + 0.07 * j)
        if 0 < u < 1:
            G += T.arc_band(0.12 + 1.0 * u, 0.045 * (1 - 0.5 * u), -0.5, 0.5, 0.75, 0, -0.5, -0.05, 0.0) * (1 - u) * 1.3
    g, h = clarao(T, t, 0.32, 0.55, 0.45, 0.0, 1.3, 1.3)
    G, H = G + g, H + h
    sobe = ease_out(rel(t, 0.4, 0.65), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if sobe > 0 and kk > 0:
        G += T.gauss(0.45, 0.38 - 0.2 * sobe, 0.2, 0.12 * sobe + 0.01) * kk * 0.6
        for j in range(5):
            x = 0.3 + 0.075 * j
            y = 0.38 - (0.2 + 0.08 * (j % 2)) * sobe
            G += T.polyline([(x, 0.38), (x + 0.02 * math.sin(t * 8 + j), (0.38 + y) / 2), (x, y)], 0.016) * kk * 1.1
        for j in range(4):
            u = (t * 1.5 + j / 4) % 1
            G += T.ring(0.015 + 0.02 * u, 0.006, 0.35 + 0.07 * j, 0.25 - 0.15 * u) * (1 - u) * kk * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Elsa

def rajada_de_gelo_elsa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    c = pulso(t, 0.0, 0.35)
    if c > 0:
        G += _floco(T, -0.55, -0.05, 0.08 + 0.03 * c, t * 5, c)
        G += T.gauss(-0.55, -0.05, 0.08) * c * 0.6
    u = rel(t, 0.2, 0.42)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        ponta = -0.5 + 0.95 * min(1.0, ease_in(u) * 1.2)
        G += T.tapered([(-0.5, -0.05, ponta, 0.0, 1.0)], 0.1) * k * 0.7
        G += T.lines([(-0.5, -0.05, ponta, 0.0, 1.0)], 0.018) * k * 1.4
        H += T.lines([(-0.5, -0.05, ponta, 0.0, 1.0)], 0.006) * k
        for j in range(4):
            x = -0.45 + ((t * 2.5 + j / 4) % 1) * (ponta + 0.45)
            G += _floco(T, x, -0.04, 0.03, t * 8 + j, k * 0.9)
    cresce = ease_out(rel(t, 0.4, 0.6), 2)
    kk = 1 - rel(t, 0.88, 1)
    if cresce > 0 and kk > 0:
        for j, dx in enumerate((-0.12, 0.0, 0.12)):
            g, h = _cristal(T, 0.45 + dx, 0.3, (0.22 + 0.06 * (j == 1)) * cresce, kk * 1.1)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.4, 0.6, 0.45, 0.0, 1.1, 1.2)
    return (G + g2) * env, (H + h2) * env


def muralha_de_gelo_elsa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        cresce = ease_out(rel(t, 0.05 + 0.07 * i, 0.4 + 0.07 * i), 2)
        if cresce > 0 and k > 0:
            for j, (dx, s) in enumerate(((-0.1, 0.18), (0.08, 0.26), (0.18, 0.16))):
                g, h = _cristal(T, cx + 0.15 + dx * 0.6, 0.35, s * cresce, k * 1.0)
                G, H = G + g, H + h
            brilho = (t * 1.3 + 0.3 * i) % 1
            H += T.gauss(cx + 0.2, 0.35 - 0.3 * brilho * cresce, 0.02) * k * 1.4
    G += particulas(T, t, 0.2, 1.0, 20, 208, 0.0, 0.1, 0.8, 0.3, 0.01)
    return G * env, H * env


def elsa_preparo(T, t, rng):
    G, H = vazio(T)
    G += _floco(T, 0.0, -0.05, 0.33, t * TAU * 0.3, 1.0)
    G += T.gauss(0.0, -0.05, 0.25) * (0.2 + 0.1 * math.sin(t * TAU * 2))
    for j in range(6):
        a = -t * TAU * 0.5 + TAU * j / 6
        H += T.gauss(0.4 * math.cos(a), -0.05 + 0.25 * math.sin(a), 0.01) * 1.5
    return G, H


def inverno_eterno(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(209)
    for j in range(30):
        a0 = q.uniform(0, 0.4)
        u = rel(t, a0, a0 + 0.5)
        if 0 < u < 1:
            x = -1.0 + 2.0 * u + q.uniform(-0.2, 0.2)
            y = q.uniform(-0.6, 0.3) + 0.15 * u
            G += _floco(T, x, y, 0.025, u * 10 + j, (1 - rel(u, 0.8, 1)) * 1.0)
    for m in range(4):
        u = rel(t, 0.05 * m, 0.5 + 0.05 * m)
        if 0 < u < 1:
            G += T.lines([(-1.0 + 2.0 * u - 0.3, -0.4 + 0.2 * m, -1.0 + 2.0 * u, -0.38 + 0.2 * m, 1.0)], 0.008) * (1 - u) * 1.0
    G += T.gauss(0.0, 0.36, 0.9 * ease_out(rel(t, 0.3, 0.6), 2) + 0.01, 0.04) * (1 - rel(t, 0.85, 0.97)) * 0.6
    kk = 1 - rel(t, 0.88, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        cresce = ease_out(rel(t, 0.4 + 0.06 * i, 0.62 + 0.06 * i), 2)
        if cresce > 0 and kk > 0:
            g, h = _cristal(T, cx, 0.32, 0.3 * cresce, kk * 1.1)
            G, H = G + g, H + h
        g2, h2 = clarao(T, t, 0.55 + 0.06 * i, 0.72 + 0.06 * i, cx, 0.05, 0.4, 0.8)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Malévola

def _chifres(T, cx, cy, s, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        pts = [(cx + lado * s * 0.15, cy), (cx + lado * s * 0.45, cy - s * 0.5), (cx + lado * s * 0.35, cy - s * 1.0), (cx + lado * s * 0.25, cy - s * 0.9),
               (cx + lado * s * 0.3, cy - s * 0.5), (cx + lado * s * 0.05, cy - s * 0.1)]
        g, h = icone(T, pts, k, 0.5)
        G, H = G + g, H + h
    return G, H


def maldicao_do_sono(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        for m in range(3):
            g, h = icone(T, poe(CHAMA, -0.55 + 0.11 * (m - 1), -0.1 - 0.05 * (m == 1), 0.13 * s + 0.015 * math.sin(t * 20 + m)), 1.1, 0.7)
            G, H = G + g, H + h
    u = rel(t, 0.25, 0.5)
    if 0 < u < 1:
        x = -0.45 + 0.9 * ease_in(u)
        G += T.lines([(x - 0.18, -0.16, x + 0.1, -0.12, 1.0)], 0.018) * 1.3
        H += T.gauss(x + 0.1, -0.12, 0.02) * 1.8
        G += T.tapered([(x - 0.35, -0.16, x - 0.1, -0.15, 0.7)], 0.02) * 0.8
    k = pulso(t, 0.5, 1.0)
    if k > 0:
        G += T.gauss(0.45, 0.0, 0.15) * k * 0.35
        for j in range(3):
            u2 = ((t - 0.5) * 1.3 + j / 3) % 1
            x, y = 0.5 + 0.15 * u2, -0.15 - 0.45 * u2
            z = 0.05 + 0.04 * u2
            G += T.lines([(x - z, y - z, x + z, y - z, 1.0), (x + z, y - z, x - z, y + z, 1.0), (x - z, y + z, x + z, y + z, 1.0)], 0.014) * (1 - u2) * k * 1.6
    G += particulas(T, t, 0.45, 1.0, 10, 210, 0.45, 0.0, 0.15, 0.3, 0.012)
    return G * env, H * env


def muro_de_espinhos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        for j, dx in enumerate((-0.15, 0.0, 0.15)):
            sobe = ease_out(rel(t, 0.05 + 0.06 * i + 0.03 * j, 0.4 + 0.06 * i + 0.03 * j), 2)
            if sobe > 0 and kk > 0:
                x1 = cx + dx * 0.4 + 0.1 * math.sin(j * 2 + i)
                G += _galho_espinhos(T, cx + dx, 0.38, x1, 0.38 - (0.45 + 0.1 * (j == 1)) * sobe, kk, 211 + 3 * i + j, 0.018)
        m = pulso(t, 0.4 + 0.06 * i, 1.0)
        if m > 0:
            G += T.gauss(cx, 0.15, 0.13, 0.18) * m * 0.3
    return G * env, H * env


def malevola_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _chifres(T, -0.1, -0.15, 0.3, 1.0)
    G, H = G + g, H + h
    G += T.lines([(0.25, 0.4, 0.25, -0.2, 1.0)], 0.016) * 1.1
    G += T.ring(0.06, 0.012, 0.25, -0.25) * 1.2
    for m in range(3):
        a = t * TAU * 1.5 + TAU * m / 3
        g2, h2 = icone(T, poe(CHAMA, 0.25 + 0.1 * math.cos(a), -0.25 + 0.06 * math.sin(a), 0.035), 1.1, 0.7)
        G, H = G + g2, H + h2
    H += T.gauss(0.25, -0.25, 0.025) * 1.6
    return G, H


def forma_de_dragao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        cabeca = [(-0.9, 0.3), (-0.8, -0.2), (-0.4, -0.45), (0.1, -0.4), (0.7, -0.15), (1.0, 0.0), (0.6, 0.1), (0.95, 0.2), (0.5, 0.3), (-0.3, 0.45)]
        g, h = icone(T, poe(cabeca, -0.6, -0.35, 0.22 * s), 1.1, 0.4)
        G, H = G + g, H + h
        g2, h2 = _chifres(T, -0.7, -0.42, 0.18 * s, 1.0)
        G, H = G + g2, H + h2
        H += T.gauss(-0.6, -0.42, 0.015) * s * 2.0
    k = pulso(t, 0.3, 0.85)
    if k > 0:
        for i, cx in enumerate((-0.55, 0.0, 0.55)):
            q = np.random.default_rng(220 + i + int(t * 20))
            for m in range(6):
                u = ((t * 2 + m / 6 + 0.1 * i) % 1)
                x = -0.4 + (cx + 0.4) * u
                y = -0.3 + 0.35 * u
                g3, h3 = icone(T, poe(CHAMA, x + q.uniform(-0.03, 0.03), y, 0.04 + 0.04 * u, -math.pi / 2 + math.atan2(0.35, cx + 0.4 + 1e-6)),
                               k * (1 - 0.4 * u) * 1.1, 0.7)
                G, H = G + g3, H + h3
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        g4, h4 = clarao(T, t, 0.45 + 0.06 * i, 0.68 + 0.06 * i, cx, 0.05, 0.5, 1.0)
        G, H = G + g4, H + h4
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.35, 1.2)
    return G * env, H * env


REGISTRO = [
    ("voce_nao_vai_passar", voce_nao_vai_passar, GRANDE, "Gandalf · o cajado e a parede de luz", False),
    ("luz_de_gandalf", luz_de_gandalf, GRANDE, "Gandalf · o cajado como um sol branco", False),
    ("gandalf_preparo", gandalf_preparo, MEDIA, "Gandalf · o chapéu, o cajado e a espada (Preparo, laço)", True),
    ("glamdring", glamdring, GRANDE, "Gandalf · a Glamdring em arco", False),
    ("pisao_de_godzilla", pisao_de_godzilla, GRANDE, "Godzilla · a pata e o chão tremendo", False),
    ("couraca", couraca, GRANDE, "Godzilla · as placas acesas e a couraça", False),
    ("godzilla_preparo", godzilla_preparo, MEDIA, "Godzilla · as placas acendendo (Preparo, laço)", True),
    ("sopro_atomico", sopro_atomico, GRANDE, "Godzilla · o raio atômico varrendo", False),
    ("soco_gigante_kong", soco_gigante_kong, GRANDE, "King Kong · o punho gigante", False),
    ("bater_no_peito", bater_no_peito, GRANDE, "King Kong · as batidas no peito", False),
    ("kong_preparo", kong_preparo, MEDIA, "King Kong · o machado de energia (Preparo, laço)", True),
    ("machado_de_kong", machado_de_kong, GRANDE, "King Kong · o machado rachando o chão", False),
    ("arroto", arroto, GRANDE, "Shrek · o arroto e as moscas", False),
    ("abraco_de_ogro", abraco_de_ogro, GRANDE, "Shrek · os braços verdes e o escudo", False),
    ("shrek_preparo", shrek_preparo, MEDIA, "Shrek · as orelhas e as bolhas (Preparo, laço)", True),
    ("rugido_do_pantano", rugido_do_pantano, GRANDE, "Shrek · o rugido e o pântano subindo", False),
    ("rajada_de_gelo_elsa", rajada_de_gelo_elsa, GRANDE, "Elsa · o raio de gelo e os cristais", False),
    ("muralha_de_gelo_elsa", muralha_de_gelo_elsa, GRANDE, "Elsa · os cristais na frente do trio", False),
    ("elsa_preparo", elsa_preparo, MEDIA, "Elsa · o floco gigante girando (Preparo, laço)", True),
    ("inverno_eterno", inverno_eterno, GRANDE, "Elsa · a nevasca e o gelo nos rivais", False),
    ("maldicao_do_sono", maldicao_do_sono, GRANDE, "Malévola · o fogo verde e o fuso", False),
    ("muro_de_espinhos", muro_de_espinhos, GRANDE, "Malévola · os galhos de espinhos", False),
    ("malevola_preparo", malevola_preparo, MEDIA, "Malévola · os chifres e o fogo no cajado (Preparo, laço)", True),
    ("forma_de_dragao", forma_de_dragao, GRANDE, "Malévola · o dragão e o fogo verde", False),
]
