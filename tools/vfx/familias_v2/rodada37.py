"""Rodada 37 das habilidades próprias: Peter Griffin, Stewie Griffin, Eric Cartman, Bill Cipher e Plankton.

Peter Griffin
- briga_com_o_galo: a nuvem de briga com as penas do galo voando e os socos (Confuso e Marcado).
- ideia_terrivel: a lâmpada acendendo sobre a cabeça e virando bomba no rival (Exposto).
- peter_preparo: o Preparo do Nhé-hé-hé — a barriga sacudindo na risada (laço).
- nhe_he_he: a risada em ondas que confunde todos e o tombo segurando o joelho (Confuso e o dano nele mesmo).

Stewie Griffin
- raio_de_controle: a pistola futurista com os anéis em espiral de controle da mente (Marcado e Enfraquecido).
- plano_mirabolante: a planta do plano em grade azul e os escudos montados no trio (Escudo e Fortalecido).
- stewie_preparo: o Preparo da Dominação mundial — as engrenagens do plano girando (laço).
- dominacao_mundial: o globo com a mira, conquistado, e a luz no trio (Acelerado, Fortalecido e Carga).

Eric Cartman
- respeitem_minha_autoridade: o distintivo de polícia e o grito em ondas (Provocado).
- chantagem: as fotos comprometedoras voando até os rivais e o escudo no trio (Enfraquecido e Escudo).
- cartman_preparo: o Preparo do Plano egoísta — as mãos se esfregando e o brilho malvado (laço).
- plano_egoista: a nuvem verde de gás se espalhando por todos (Silenciado e Enfraquecido).

Bill Cipher
- acordo_de_bill: o aperto de mão com a chama azul (Confuso e Marcado).
- realidade_invertida: o triângulo de cabeça para baixo, o mundo girando e o escudo no aliado (Protegido, Escudo e Dissipar).
- bill_preparo: o Preparo do Olho que tudo vê — o triângulo de um olho só pulsando, os tijolos flutuando (laço).
- olho_que_tudo_ve: o olho enorme no céu e os feixes descendo em todos (Confuso).

Plankton
- plano_z: a antena do Balde de Lixo soltando o pulso que trava todos (Lento).
- plankton_preparo: o Preparo do Roubar a fórmula — o olho único apertado e as antenas tremendo (laço).
- roubar_a_formula: a garra puxando a garrafinha da fórmula de todos (Enfraquecido e Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CARTA, ESCUDO, PENA, anel, cheio, circulo, clarao, converge, engrenagem, estouro, estrela_pts, icone, onda_no_chao,
                         poe, raios, surge)


def _tontas(T, t, a, b, cx, cy, n=3, r=0.12, s=0.035):
    G, H = 0.0, 0.0
    k = pulso(t, a, b)
    if k <= 0:
        return G, H
    for j in range(n):
        ang = t * 9 + TAU * j / n
        g, h = cheio(T, poe(estrela_pts(5, 0.45), cx + r * math.cos(ang), cy + r * 0.4 * math.sin(ang), s), k * 1.3)
        G, H = G + g, H + h
    return G, H


def _bomba(T, cx, cy, s, t, k=1.0):
    g, h = icone(T, poe(circulo(22), cx, cy, s), k * 1.1, 0.6)
    pavio = [(cx + s * 0.5, cy - s * 0.85), (cx + s * 0.75, cy - s * 1.2), (cx + s * 1.05, cy - s * 1.3)]
    g = g + T.polyline(pavio, s * 0.1) * k * 1.0
    fx, fy = pavio[-1]
    return g, h + T.gauss(fx, fy, s * 0.15) * k * 2.0 * (0.7 + 0.3 * math.sin(t * 50))


def _olho_triangulo(T, cx, cy, s, k, t, inverte=False):
    """O triângulo do Bill com o olho no meio."""
    if k <= 0 or s <= 0.002:
        return 0.0, 0.0
    sg = -1 if inverte else 1
    tri = [(cx, cy - sg * s), (cx + s * 0.95, cy + sg * s * 0.65), (cx - s * 0.95, cy + sg * s * 0.65)]
    g, h = icone(T, tri, k * 1.1, 0.45)
    pisca = 1.0 if (t * 3) % 1 > 0.08 else 0.2
    olho = [(cx + s * 0.4 * math.cos(a), cy + sg * s * 0.05 + s * 0.2 * math.sin(a) * pisca) for a in np.linspace(0, TAU, 20, endpoint=False)]
    g2, h2 = icone(T, olho, k * 1.2, 0.3)
    return g + g2 + T.gauss(cx, cy + sg * s * 0.05, s * 0.08) * k * 1.6 * pisca, h + h2 + T.gauss(cx, cy + sg * s * 0.05, s * 0.05) * k * 2.0 * pisca


# ------------------------------------------------------------------ Peter Griffin

def briga_com_o_galo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    q = np.random.default_rng(int(t * 25))
    pts = [(0.3 + q.normal(0, 0.16), q.normal(0, 0.13), k * q.uniform(0.4, 0.9)) for _ in range(30)]
    G += T.splats(pts, 0.07) * 0.8
    for _ in range(3):
        a = q.uniform(0, TAU)
        if k > 0.2:
            P, nos = _punho(T, 0.3 + 0.32 * math.cos(a), 0.27 * math.sin(a), 1.3, a)
            G += P * 0.8 * k
            H += nos * 0.3 * k
    q2 = np.random.default_rng(4)
    for j in range(10):
        a = q2.uniform(0, TAU)
        w = rel(t, 0.1 + 0.04 * j, 0.7 + 0.04 * j)
        if 0 < w < 1:
            r = 0.15 + 0.5 * w
            g, h = icone(T, poe(PENA, 0.3 + r * math.cos(a), r * 0.7 * math.sin(a) + 0.2 * w * w, 0.06, a + w * 5), (1 - rel(w, 0.7, 1)) * 1.1, 0.6)
            G, H = G + g, H + h
    g2, h2 = _tontas(T, t, 0.5, 1.0, 0.3, -0.3, 4, 0.14, 0.04)
    return (G + g2) * env, (H + h2) * env


_LAMPADA = [(-0.6, -0.2)] + [(0.6 * math.cos(a), -0.2 + 0.6 * math.sin(a)) for a in np.linspace(math.pi, TAU, 14)] + [(0.6, -0.2), (0.3, 0.45), (0.3, 0.8),
                                                                                                                      (-0.3, 0.8), (-0.3, 0.45)]


def ideia_terrivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.35, 0.42))
    if s > 0:
        g, h = icone(T, poe(_LAMPADA, -0.45, -0.5, 0.25 * s), 1.2, 0.5)
        G, H = G + g, H + h
        H += T.gauss(-0.45, -0.53, 0.05) * s * 2.0
        for j in range(6):
            a = -math.pi / 2 + (j - 2.5) * 0.45
            G += T.lines([(-0.45 + 0.17 * math.cos(a), -0.53 + 0.17 * math.sin(a), -0.45 + 0.26 * math.cos(a), -0.53 + 0.26 * math.sin(a), 1.0)],
                         0.01) * s * 1.3
    u = rel(t, 0.38, 0.6)
    if 0 < u < 1:
        x = -0.45 + 0.95 * u
        y = -0.5 + 0.5 * u - 0.25 * math.sin(math.pi * u)
        g2, h2 = _bomba(T, x, y, 0.13, t)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.58, 0.8, 0.5, 0.0, 1.5, 1.5)
    G, H = G + g3, H + h3
    w = rel(t, 0.6, 0.98)
    if 0 < w < 1:
        G += T.ring(0.06 + 0.55 * ease_out(w, 2), 0.04 * (1 - 0.5 * w), 0.5, 0.0) * (1 - w) * 1.3
    G += estouro(T, t, 0.6, 0.98, 16, 5, 0.5, 0.0, 0.6, 0.014)
    return G * env, H * env


def peter_preparo(T, t, rng):
    G, H = vazio(T)
    sac = math.sin(t * TAU * 4)
    G += T.gauss(0.0, 0.1, 0.22 + 0.02 * sac, 0.17 - 0.02 * sac) * 0.8
    for j in range(3):
        u = ((t * 1.5) + j / 3) % 1
        x = -0.15 + 0.15 * j
        G += T.arc_band(0.05, 0.012, -2.5, -0.6, 1.0, 0, x, -0.3 - 0.25 * u, 0.0) * (1 - u) * 1.3
    return G, H


def nhe_he_he(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        u = rel(t, 0.05 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 0.85 * u, 0.04 * (1 - 0.5 * u), -0.7, 0.7, 0.6, 0, -0.6, 0.0, 0.0) * (1 - u) * 1.3
    for x in (-0.55, 0.0, 0.55):
        g, h = _tontas(T, t, 0.4, 1.0, x + 0.1, -0.25, 3, 0.1, 0.035)
        G, H = G + g, H + h
        g2, h2 = clarao(T, t, 0.35, 0.5, x + 0.1, 0.0, 0.4)
        G, H = G + g2, H + h2
    s = surge(t, 0.6, 0.75) * (1 - rel(t, 0.9, 1))
    if s > 0:
        G += T.gauss(-0.65, 0.3, 0.1 * s, 0.06 * s) * 1.0
        for m in range(3):
            G += T.lines([(-0.6 + 0.07 * m, 0.15, -0.6 + 0.07 * m, 0.05 - 0.04 * s, 1.0)], 0.008) * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Stewie Griffin

def _pistola(T, cx, cy, s, k):
    g, h = icone(T, [(cx - s, cy - s * 0.25), (cx + s * 0.6, cy - s * 0.25), (cx + s, cy), (cx + s * 0.6, cy + s * 0.25), (cx - s * 0.4, cy + s * 0.25),
                     (cx - s * 0.5, cy + s * 0.8), (cx - s * 0.9, cy + s * 0.8)], k * 1.1, 0.45)
    return g + T.ring(s * 0.25, s * 0.06, cx + s * 0.05, cy) * k * 1.2, h


def raio_de_controle(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        g, h = _pistola(T, -0.65, 0.0, 0.14 * s, 1.0)
        G, H = G + g, H + h
    k = pulso(t, 0.15, 0.7)
    if k > 0:
        for j in range(6):
            v = ((t * 2.5) + j / 6) % 1
            x = -0.5 + 1.0 * v
            G += T.ring(0.04 + 0.06 * v, 0.012, x, 0.0, 0.5) * k * 1.3
        G += T.lines([(-0.5, 0.0, 0.5, 0.0, 1.0)], 0.008) * k * 1.0
    m = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        pts = [(0.5 + 0.03 * a * math.cos(a + t * 8), 0.03 * a * math.sin(a + t * 8)) for a in np.linspace(0.5, 9, 40)]
        G += T.polyline(pts, 0.014) * m * 1.3
    return G * env, H * env


def plano_mirabolante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    if k > 0:
        linhas = [(-0.6, -0.6 + 0.1 * m, 0.6, -0.6 + 0.1 * m, 0.5) for m in range(6)] + [(-0.6 + 0.12 * m, -0.6, -0.6 + 0.12 * m, -0.1, 0.5)
                                                                                          for m in range(11)]
        G += T.lines(linhas, 0.004) * k * 1.0
        u = rel(t, 0.05, 0.5)
        G += T.polyline([(-0.4, -0.3), (-0.1, -0.5), (0.2, -0.25), (0.45, -0.45)][:max(2, int(4 * u) + 1)], 0.012) * k * 1.3
    for x in (-0.55, 0.0, 0.55):
        s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
        if s > 0:
            g, h = icone(T, poe(ESCUDO, x, 0.12, 0.15 * s), 1.1, 0.4)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.4, 0.55, 0, 0.1, 0.6)
    return (G + g2) * env, (H + h2) * env


def stewie_preparo(T, t, rng):
    G, H = vazio(T)
    for j, (x, y, r, sentido) in enumerate(((-0.12, 0.0, 0.16, 1), (0.14, -0.12, 0.1, -1.6), (0.12, 0.15, 0.08, -2.0))):
        g, h = icone(T, poe(engrenagem(8, 1.0, 0.78), x, y, r, t * TAU * 0.5 * sentido), 1.1, 0.45)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.3) * (0.3 + 0.15 * math.sin(t * 8))
    return G, H


def dominacao_mundial(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        cx, cy, r = 0.0, -0.4, 0.22 * s
        G += T.ring(r, 0.02, cx, cy) * 1.3
        G += T.arc_band(r, 0.012, 0, math.pi, 0.35, 0, cx, cy, 0.0) * 1.0
        G += T.ring(r * 0.55, 0.01, cx, cy, 3.0) * 0.8
        G += T.lines([(cx, cy - r, cx, cy + r, 1.0)], 0.01) * 0.8
        mira = surge(t, 0.2, 0.4)
        if mira > 0:
            G += T.ring(r * 1.25, 0.012, cx, cy) * mira * 1.2
            G += T.lines([(cx - r * 1.5, cy, cx - r * 0.9, cy, 1.0), (cx + r * 0.9, cy, cx + r * 1.5, cy, 1.0)], 0.01) * mira * 1.2
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.4, 1.0)
        G += T.tapered([(0.0, -0.2, x, 0.1, 1.0)], 0.03) * pulso(t, 0.35, 0.6) * 1.0
        G += T.gauss(x, 0.1, 0.15, 0.22) * k * 0.6
    G += onda_no_chao(T, t, 0.45, 0.95, 0.95, 0.35, 1.3)
    g2, h2 = clarao(T, t, 0.3, 0.5, 0, -0.4, 0.8)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Eric Cartman

def respeitem_minha_autoridade(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.75, 0.9))
    if s > 0:
        g, h = icone(T, poe(estrela_pts(6, 0.6), -0.45, -0.3, 0.18 * s, 0), 1.2, 0.45)
        G, H = G + g, H + h
        G += T.ring(0.07 * s, 0.015, -0.45, -0.3) * 1.2
    for j in range(4):
        u = rel(t, 0.15 + 0.1 * j, 0.6 + 0.1 * j)
        if 0 < u < 1:
            G += T.arc_band(0.2 + 0.8 * u, 0.04 * (1 - 0.5 * u), -0.6, 0.6, 0.7, 0, -0.45, -0.1, 0.0) * (1 - u) * 1.3
    g2, h2 = clarao(T, t, 0.45, 0.65, 0.5, 0.0, 0.9)
    G, H = G + g2, H + h2
    for lado in (-1, 1):
        G += T.lines([(0.5 + lado * 0.05, -0.15, 0.5 + lado * 0.12, -0.25, 1.0)], 0.015) * pulso(t, 0.55, 1.0) * 1.3
    return G * env, H * env


def chantagem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, x in enumerate((0.25, 0.55, 0.8)):
        u = rel(t, 0.05 + 0.08 * j, 0.5 + 0.08 * j)
        if 0 < u < 1:
            px = -0.4 + (x + 0.4) * ease_out(u)
            py = -0.3 - 0.2 * math.sin(math.pi * u) + 0.2 * u
            g, h = icone(T, poe(CARTA, px, py, 0.1, u * 6 + j), 1.2, 0.5)
            G, H = G + g, H + h
            G += T.ring(0.025, 0.007, px, py - 0.02) * 1.3
        g2, h2 = clarao(T, t, 0.5 + 0.08 * j, 0.65 + 0.08 * j, x, -0.1, 0.4)
        G, H = G + g2, H + h2
    for x in (-0.55, 0.0, 0.55):
        s = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
        if s > 0:
            G += T.arc_band(0.2 * s, 0.03, -2.6, -0.5, 1.0, 0, x, 0.3, 0.0) * 1.1
    return G * env, H * env


def cartman_preparo(T, t, rng):
    G, H = vazio(T)
    esf = math.sin(t * TAU * 3)
    for lado in (-1, 1):
        G += T.gauss(lado * (0.06 + 0.03 * esf * lado), 0.1, 0.07, 0.05) * 1.1
    q = np.random.default_rng(int(t * 8))
    for _ in range(3):
        a = q.uniform(0, TAU)
        g, h = cheio(T, poe(estrela_pts(4, 0.3), 0.25 * math.cos(a), -0.1 + 0.2 * math.sin(a), 0.035), 1.3)
        G, H = G + g, H + h
    G += T.gauss(0, 0, 0.25) * (0.3 + 0.15 * esf)
    return G, H


def plano_egoista(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(7)
    k = pulso(t, 0.0, 0.95)
    espalha = ease_out(rel(t, 0.0, 0.6), 2)
    pts = []
    for _ in range(50):
        a = q.uniform(-0.5, 0.5)
        r = q.uniform(0.1, 1.0) * espalha * 1.4
        x = -0.6 + r * math.cos(a) + 0.04 * math.sin(t * 6 + r * 9)
        y = 0.1 + r * 0.6 * math.sin(a) - 0.2 * espalha * q.uniform(0, 1)
        pts.append((x, y, k * q.uniform(0.3, 0.9)))
    G += T.splats(pts, 0.08) * 0.55
    for x in (-0.55, 0.0, 0.55):
        s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
        if s > 0:
            G += T.lines([(x - 0.08 * s, -0.25 - 0.08 * s, x + 0.08 * s, -0.25 + 0.08 * s, 1.0),
                          (x + 0.08 * s, -0.25 - 0.08 * s, x - 0.08 * s, -0.25 + 0.08 * s, 1.0)], 0.018) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Bill Cipher

def acordo_de_bill(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.8, 0.95)
    for lado in (-1, 1):
        x = lado * (0.6 - 0.48 * u)
        G += T.lines([(lado * 0.9, 0.05, x, 0.0, 1.0)], 0.04) * k * 1.0
        G += T.gauss(x, 0.0, 0.06) * k * 1.0
    chama = pulso(t, 0.3, 0.95)
    if chama > 0:
        q = np.random.default_rng(int(t * 30))
        for _ in range(12):
            a = -math.pi / 2 + q.normal(0, 0.5)
            r = q.uniform(0.05, 0.35) * chama
            G += T.gauss(r * math.cos(a), r * math.sin(a), 0.03) * chama * 1.1
        H += T.gauss(0, -0.05, 0.05) * chama * 2.0
    g, h = _olho_triangulo(T, 0.0, -0.55, 0.12 * surge(t, 0.1, 0.3) * (1 - rel(t, 0.8, 0.95)), 1.0 if t > 0.1 else 0, t)
    G, H = G + g, H + h
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.13 * m, 0.016, 0.0, 0.3) * 1.2
    return G * env, H * env


def realidade_invertida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    gira = ease_in(rel(t, 0.0, 0.5), 2) * math.pi
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        tri = [(0.25 * s * math.sin(gira + a), -0.4 - 0.25 * s * math.cos(gira + a)) for a in (0, TAU / 3, 2 * TAU / 3)]
        g, h = icone(T, tri, 1.1, 0.45)
        G, H = G + g, H + h
    for j in range(3):
        a0 = t * 5 * (1 if j % 2 else -1)
        G += T.arc_band(0.5 + 0.12 * j, 0.025, a0, a0 + 3.5, 0.5, 0, 0.0, 0.0, 1.0) * pulso(t, 0.1, 0.8) * 1.0
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g2, h2 = icone(T, poe(ESCUDO, -0.5, 0.05, 0.2 * m), 1.1, 0.4)
        G, H = G + g2, H + h2
    w = rel(t, 0.5, 0.9)
    if 0 < w < 1:
        q = np.random.default_rng(3)
        for _ in range(10):
            a = q.uniform(0, TAU)
            r = 0.1 + 0.35 * w
            G += T.gauss(0.55 + r * math.cos(a), r * math.sin(a), 0.015) * (1 - w) * 1.4
        G += T.ring(0.12 * (1 - w) + 0.02, 0.02, 0.55, 0.0) * (1 - w) * 1.2
    return G * env, H * env


def bill_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _olho_triangulo(T, 0.0, 0.0, 0.2 * (1 + 0.05 * math.sin(t * TAU * 2)), 1.0, t)
    G, H = G + g, H + h
    for j in range(5):
        a = t * TAU * 0.5 + TAU * j / 5
        x, y = 0.38 * math.cos(a), 0.22 * math.sin(a)
        g2, h2 = icone(T, [(x - 0.04, y - 0.025), (x + 0.04, y - 0.025), (x + 0.04, y + 0.025), (x - 0.04, y + 0.025)], 1.0, 0.5)
        G, H = G + g2, H + h2
    G += T.gauss(0, 0, 0.3) * (0.3 + 0.15 * math.sin(t * 9))
    return G, H


def olho_que_tudo_ve(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.8, 0.95))
    g, h = _olho_triangulo(T, 0.0, -0.55, 0.3 * s, 1.0 if s > 0 else 0, t)
    G, H = G + g, H + h
    k = pulso(t, 0.35, 0.8)
    if k > 0:
        for x in (-0.55, 0.0, 0.55):
            G += T.polys([([(-0.02, -0.5), (0.02, -0.5), (x + 0.12, 0.15), (x - 0.12, 0.15)], 1.0)], 0.03) * k * 0.45
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.45, 0.62, x, 0.1, 0.5)
        G, H = G + g2, H + h2
        g3, h3 = _tontas(T, t, 0.55, 1.0, x, -0.15, 3, 0.1, 0.03)
        G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Plankton

def plano_z(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        G += T.lines([(-0.55, 0.35, -0.55, 0.35 - 0.45 * s, 1.0), (-0.65, 0.35, -0.55, 0.15, 1.0), (-0.45, 0.35, -0.55, 0.15, 1.0)], 0.014) * 1.2
        H += T.gauss(-0.55, 0.35 - 0.45 * s, 0.025) * s * (1.5 + math.sin(t * 40))
    for j in range(4):
        u = rel(t, 0.15 + 0.1 * j, 0.65 + 0.1 * j)
        if 0 < u < 1:
            G += T.ring(0.05 + 1.0 * u, 0.03 * (1 - 0.5 * u), -0.55, -0.1, 1.0) * (1 - u) * 1.3
    G += raios(T, t, 0.45, 0.9, 6, 3, 0.2, 0.0, 0.7, 0.009)
    for x in (-0.55, 0.0, 0.55):
        g, h = clarao(T, t, 0.45, 0.6, x + 0.1, 0.05, 0.35)
        G, H = G + g, H + h
    return G * env, H * env


def plankton_preparo(T, t, rng):
    G, H = vazio(T)
    aperta = 0.6 + 0.4 * abs(math.sin(t * TAU))
    olho = [(0.14 * math.cos(a), 0.14 * aperta * math.sin(a)) for a in np.linspace(0, TAU, 24, endpoint=False)]
    g, h = icone(T, olho, 1.2, 0.4)
    G, H = G + g, H + h
    H += T.gauss(0, 0, 0.03) * 2.0
    for lado in (-1, 1):
        treme = 0.03 * math.sin(t * 50 + lado)
        G += T.lines([(lado * 0.06, -0.12, lado * 0.15 + treme, -0.4, 1.0)], 0.01) * 1.2
        G += T.gauss(lado * 0.15 + treme, -0.4, 0.02) * 1.3
    return G, H


_GARRAFA = [(-0.25, 0.9), (0.25, 0.9), (0.3, -0.1), (0.12, -0.4), (0.12, -0.8), (-0.12, -0.8), (-0.12, -0.4), (-0.3, -0.1)]


def roubar_a_formula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.05 + 0.05 * j, 0.25 + 0.05 * j)
        u = ease_in(rel(t, 0.35 + 0.05 * j, 0.7 + 0.05 * j), 1.6)
        k = 1 - rel(t, 0.75 + 0.05 * j, 0.85 + 0.05 * j)
        if s > 0 and k > 0:
            px = x + (-0.85 - x) * u
            py = -0.1 - 0.25 * math.sin(math.pi * u)
            g, h = icone(T, poe(_GARRAFA, px, py, 0.15 * s, u * 3), k * 1.2, 0.5)
            G, H = G + g, H + h
            H += T.gauss(px, py, 0.02) * k * 1.6
        g2, h2 = clarao(T, t, 0.2 + 0.05 * j, 0.35 + 0.05 * j, x, -0.1, 0.4)
        G, H = G + g2, H + h2
    G += converge(T, t, 0.35, 0.85, 14, 3, -0.85, -0.1, 0.5)
    G += T.gauss(-0.85, -0.1, 0.12) * pulso(t, 0.6, 1.0) * 0.8
    return G * env, H * env


REGISTRO = [
    ("briga_com_o_galo", briga_com_o_galo, GRANDE, "Peter Griffin · a briga com as penas do galo", False),
    ("ideia_terrivel", ideia_terrivel, GRANDE, "Peter Griffin · a lâmpada que vira bomba", False),
    ("peter_preparo", peter_preparo, MEDIA, "Peter Griffin · a barriga sacudindo na risada (Preparo, laço)", True),
    ("nhe_he_he", nhe_he_he, GRANDE, "Peter Griffin · a risada em ondas e o tombo", False),
    ("raio_de_controle", raio_de_controle, GRANDE, "Stewie Griffin · a pistola e os anéis de controle", False),
    ("plano_mirabolante", plano_mirabolante, GRANDE, "Stewie Griffin · a planta e os escudos", False),
    ("stewie_preparo", stewie_preparo, MEDIA, "Stewie Griffin · as engrenagens do plano (Preparo, laço)", True),
    ("dominacao_mundial", dominacao_mundial, GRANDE, "Stewie Griffin · o globo na mira e a luz no trio", False),
    ("respeitem_minha_autoridade", respeitem_minha_autoridade, GRANDE, "Eric Cartman · o distintivo e o grito", False),
    ("chantagem", chantagem, GRANDE, "Eric Cartman · as fotos voando e o escudo", False),
    ("cartman_preparo", cartman_preparo, MEDIA, "Eric Cartman · as mãos se esfregando (Preparo, laço)", True),
    ("plano_egoista", plano_egoista, GRANDE, "Eric Cartman · a nuvem verde de gás", False),
    ("acordo_de_bill", acordo_de_bill, GRANDE, "Bill Cipher · o aperto de mão com a chama azul", False),
    ("realidade_invertida", realidade_invertida, GRANDE, "Bill Cipher · o triângulo virando e o escudo", False),
    ("bill_preparo", bill_preparo, MEDIA, "Bill Cipher · o triângulo e os tijolos flutuando (Preparo, laço)", True),
    ("olho_que_tudo_ve", olho_que_tudo_ve, GRANDE, "Bill Cipher · o olho no céu e os feixes", False),
    ("plano_z", plano_z, GRANDE, "Plankton · a antena e o pulso", False),
    ("plankton_preparo", plankton_preparo, MEDIA, "Plankton · o olho apertado e as antenas (Preparo, laço)", True),
    ("roubar_a_formula", roubar_a_formula, GRANDE, "Plankton · as garrafinhas da fórmula puxadas", False),
]
