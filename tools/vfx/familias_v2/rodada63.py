"""Rodada 63 das habilidades próprias: Cuphead, Dovahkiin, O Cavaleiro, Goro e Yoshi.

Cuphead
- disparo_de_dedo: o dedo apontado e as balas de ervilha em rajada no rival.
- dash_cuphead: o dash para o lado com as listras de desenho dos anos 30 (Esquiva).
- cuphead_preparo: o Preparo do Super Art — as cartas de super enchendo embaixo (laço).
- super_art_cuphead: o raio gigante do Super Art em espiral no rival (Exposto).

Dovahkiin
- machado_de_aco: o machado de aço nórdico descendo no rival.
- fus_ro_dah_grito: o grito do dragão em três ondas (FUS, RO, DAH) e os rivais empurrados (Paralisado e atrasa o Preparo).
- dovahkiin_preparo: o Preparo do Fogo do dragão — as três runas do grito acendendo uma a uma (laço).
- fogo_do_dragao_dovahkiin: o grito de fogo (YOL TOOR SHUL) varrendo todos os rivais (Queimando).

O Cavaleiro
- ferrao_cavaleiro: o ferrão (a agulha) estocando rápido o rival.
- concentrar_cavaleiro: a alma branca se juntando no Cavaleiro e curando (Vida e Esquiva).
- cavaleiro_preparo: o Preparo do Grito do abismo — a máscara de chifres e a sombra subindo (laço).
- grito_do_abismo: os braços de sombra subindo do chão em todos os rivais (Enfraquecido).

Goro
- quatro_socos: os quatro braços socando em sequência o rival (Exposto).
- agarrao_goro: os quatro braços agarrando e prendendo o rival (Paralisado).
- goro_preparo: o Preparo do Pisão — o pé enorme levantado e o chão tremendo (laço).
- pisao_de_goro: o pisão que racha o chão e prende todos os rivais (Preso).

Yoshi
- engolir_yoshi: a língua comprida puxando o rival para a boca (copia a habilidade e Preso).
- ovo_yoshi: o ovo pintado voando e quicando no rival.
- yoshi_preparo: o Preparo do Pisão — o Yoshi pulando bem alto (laço).
- pisao_de_yoshi: o pisão do alto e as estrelinhas em todos os rivais (Lento).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CARTA, CHAMA, CRUZ, anel, clarao, corte, estouro, estrela_pts, icone, onda_no_chao, particulas, poe,
                         surge)

ESTRELA = estrela_pts(5, 0.45)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _machado(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.06) * k * 1.2
    hx, hy = x + c * s * 0.9, y + sn * s * 0.9
    px, py = -sn, c
    lam = [(hx, hy), (hx + px * s * 0.35 - c * s * 0.15, hy + py * s * 0.35 - sn * s * 0.15), (hx + px * s * 0.42 + c * s * 0.05, hy + py * s * 0.42 + sn * s * 0.05),
           (hx + px * s * 0.3 + c * s * 0.22, hy + py * s * 0.3 + sn * s * 0.22), (hx + c * s * 0.1, hy + sn * s * 0.1)]
    g, h = icone(T, lam, k * 1.2, 0.6)
    return G + g, h


def _runa(T, x, y, s, j, k):
    """Uma runa de dragão (os riscos em garra do alfabeto dos dragões)."""
    formas = [[(x - s, y - s, x, y + s, 1.0), (x, y + s, x + s, y - s, 1.0)],
              [(x - s, y - s, x + s, y - s, 1.0), (x, y - s, x, y + s, 1.0), (x - s * 0.6, y + s * 0.2, x + s * 0.6, y + s * 0.2, 1.0)],
              [(x - s, y + s, x, y - s, 1.0), (x, y - s, x + s, y + s, 1.0), (x - s * 0.5, y, x + s * 0.5, y, 1.0)]]
    return T.lines(formas[j % 3], s * 0.18) * k * 1.3


def _ferrao(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.tapered([(x, y, x + c * s, y + sn * s, 1.0)], s * 0.05) * k * 1.4
    G += T.ring(s * 0.06, s * 0.02, x - c * s * 0.05, y - sn * s * 0.05) * k
    return G, T.lines([(x, y, x + c * s * 0.9, y + sn * s * 0.9, 1.0)], s * 0.012) * k * 1.3


def _mascara_chifres(T, x, y, s, k):
    G = T.ring(s * 0.55, s * 0.08, x, y, 0.85) * k * 1.2 + T.gauss(x, y, s * 0.45) * k * 0.3
    for lado in (-1, 1):
        G += T.polyline([(x + lado * s * 0.3, y - s * 0.45), (x + lado * s * 0.45, y - s * 1.0), (x + lado * s * 0.6, y - s * 1.2)], s * 0.08) * k * 1.2
        G += T.gauss(x + lado * s * 0.2, y + s * 0.05, s * 0.12, s * 0.18) * k * 0.8
    return G


def _ovo(T, x, y, s, k, ang=0.0):
    pts = [(x + s * 0.75 * math.cos(a) * math.cos(ang) - s * (0.95 if math.sin(a) < 0 else 0.8) * math.sin(a) * math.sin(ang),
            y + s * 0.75 * math.cos(a) * math.sin(ang) + s * (0.95 if math.sin(a) < 0 else 0.8) * math.sin(a) * math.cos(ang)) for a in np.linspace(0, TAU, 24, endpoint=False)]
    g, h = icone(T, pts, k * 1.2, 0.5)
    G = g
    for j in range(3):
        a = TAU * j / 3 + 0.5
        G += T.gauss(x + s * 0.35 * math.cos(a + ang), y + s * 0.4 * math.sin(a + ang), s * 0.15) * k * 0.9
    return G, h


def _carta_super(T, x, y, s, enche, k):
    G = T.polyline([(x - s * 0.6, y - s), (x + s * 0.6, y - s), (x + s * 0.6, y + s), (x - s * 0.6, y + s), (x - s * 0.6, y - s)], s * 0.08) * k
    if enche > 0:
        G += T.polys([([(x - s * 0.6, y + s), (x + s * 0.6, y + s), (x + s * 0.6, y + s - 2 * s * enche), (x - s * 0.6, y + s - 2 * s * enche)], 1.0)], 0.003) * k * 0.8
    return G


# ------------------------------------------------------------------ Cuphead

def disparo_de_dedo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.7, 0.82))
    if k > 0:
        # a mão de luva branca com o dedo apontado
        G += T.gauss(-0.62, -0.05, 0.11) * k * 1.2 + T.lines([(-0.62, -0.05, -0.42, -0.05, 1.0)], 0.045) * k * 1.3
    for j in range(7):
        a0 = 0.12 + 0.07 * j
        u = rel(t, a0, a0 + 0.2)
        if 0 < u < 1:
            x = -0.42 + 0.87 * u
            y = -0.05 + 0.03 * math.sin(j * 2.1)
            G += T.ring(0.045, 0.018, x, y) * 1.3 + T.tapered([(x - 0.16, y, x - 0.04, y, 0.7)], 0.025)
            H += T.gauss(x, y, 0.012) * 1.8
        g, h = clarao(T, t, a0 + 0.18, a0 + 0.26, 0.45, -0.05 + 0.04 * math.sin(j), 0.35, 0.7)
        G, H = G + g, H + h
    return G * env, H * env


def dash_cuphead(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.1, 0.4), 2.5)
    x = -0.3 + 0.5 * u
    G += T.gauss(x, -0.05, 0.08, 0.2) * (1 - rel(t, 0.85, 1)) * 1.0
    for j in range(6):
        y = -0.3 + 0.1 * j
        G += T.tapered([(x - 0.6, y, x - 0.1, y, 0.9)], 0.018) * pulso(t, 0.1, 0.7) * 1.1
    # o "puf" da poeira de desenho
    p = rel(t, 0.12, 0.5)
    if 0 < p < 1:
        for j in range(4):
            G += T.ring(0.03 + 0.06 * p, 0.012, -0.35 - 0.05 * j, -0.05 + 0.08 * (j - 1.5)) * (1 - p) * 1.3
    G += T.ring(0.3, 0.012, x, -0.05, 0.9) * pulso(t, 0.4, 1.0)
    return G * env, H * env


def cuphead_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(5):
        enche = max(0, min(1, (t * 1.0) * 5 - j))
        G += _carta_super(T, -0.4 + 0.2 * j, 0.0, 0.1, enche, 1.0)
        if enche >= 1:
            H += T.gauss(-0.4 + 0.2 * j, 0.0, 0.03) * 1.2
    return G, H


def super_art_cuphead(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    for j in range(5):
        G += _carta_super(T, -0.75 + 0.1 * j, 0.32, 0.05, 1.0, 1 - rel(t, 0.15, 0.25))
    k = pulso(t, 0.0, 0.35)
    G += T.gauss(-0.55, -0.05, 0.12) * k * 1.2
    u = rel(t, 0.2, 0.7)
    if 0 < u < 1:
        w = 0.18 * math.sin(math.pi * min(1, u * 1.4))
        G += T.tapered([(-0.5, -0.05, -0.5 + 1.1 * ease_out(u), -0.05, 1.0)], w + 0.02) * 1.1
        pts = [(-0.5 + 1.0 * v * ease_out(u), -0.05 + 0.12 * math.sin(v * 18 - t * 30)) for v in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.014) * 1.3
        H += T.lines([(-0.5, -0.05, -0.5 + 1.0 * ease_out(u), -0.05, 1.0)], 0.012) * 1.6
    g, h = clarao(T, t, 0.4, 0.7, 0.45, -0.05, 1.9, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.42, 0.85, 0.05, 0.7, 0.05, -0.05, 1.0, 1.4)
    G += estouro(T, t, 0.42, 0.85, 16, 740, 0.45, -0.05, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Dovahkiin

def machado_de_aco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        ang = -2.3 + 1.9 * ease_in(rel(t, 0.12, 0.35), 2)
        g, h = _machado(T, -0.15, 0.3, ang, 0.6, k)
        G, H = G + g, H + h
        G += T.arc_band(0.6, 0.06, ang - 0.8, ang, 1.0, 0, -0.15, 0.3, 1.0) * k * pulso(t, 0.12, 0.38) * 0.7
    g, h = clarao(T, t, 0.32, 0.55, 0.45, -0.05, 1.4, 1.4)
    G, H = G + g, H + h
    G += anel(T, t, 0.33, 0.7, 0.04, 0.5, 0.04, -0.05, 1.0, 1.3)
    G += estouro(T, t, 0.33, 0.75, 12, 741, 0.45, -0.05, 0.5, 0.012)
    return G * env, H * env


def fus_ro_dah_grito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    for j in range(3):
        a0 = 0.05 + 0.15 * j
        m = surge(t, a0, a0 + 0.1) * (1 - rel(t, 0.7, 0.85))
        if m > 0:
            G += _runa(T, -0.7 + 0.2 * j, -0.5, 0.07 * m, j, 1.0)
        u = rel(t, a0 + 0.05, a0 + 0.55)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.2 * ease_out(u), 0.05 * (1 - 0.5 * u) * (1 + 0.5 * j), -0.65, 0.65, 0.8, 0, -0.6, -0.05, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        e = rel(t, 0.4 + 0.05 * i, 0.75 + 0.05 * i)
        if 0 < e < 1:
            G += T.lines([(cx + 0.15 + 0.2 * e + 0.08 * q, -0.25 + 0.15 * q, cx + 0.3 + 0.2 * e + 0.08 * q, -0.25 + 0.15 * q, 0.7) for q in range(3)], 0.012) * (1 - e)
        m = pulso(t, 0.5 + 0.05 * i, 1.0)
        if m > 0:
            for j in range(2):
                G += _zap(T, 742 + i * 2 + j + int(t * 10), cx - 0.1 + 0.2 * j, -0.3, cx - 0.05 + 0.1 * j, 0.15, 0.007, 3, 0.4) * m
    G += particulas(T, t, 0.3, 1.0, 22, 750, 0.0, 0.1, 0.8, 0.2, 0.012, 0.6)
    return G * env, H * env


def dovahkiin_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(3):
        acesa = 1.0 if (t * 3) % 3 >= j else 0.3
        G += _runa(T, -0.3 + 0.3 * j, -0.05, 0.08, j, acesa)
        H += T.gauss(-0.3 + 0.3 * j, -0.05, 0.05) * acesa * (1.0 if acesa > 0.5 else 0) * 1.2
    G += T.ring(0.45, 0.012, 0.0, -0.05, 2.5) * 0.7
    return G, H


def fogo_do_dragao_dovahkiin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    for j in range(3):
        m = surge(t, 0.05 + 0.08 * j, 0.15 + 0.08 * j) * (1 - rel(t, 0.5, 0.62))
        if m > 0:
            G += _runa(T, -0.7 + 0.2 * j, -0.5, 0.07 * m, j + 1, 1.0)
    u = rel(t, 0.25, 0.75)
    if 0 < u < 1:
        q = np.random.default_rng(751 + int(t * 20))
        for _ in range(18):
            a = q.uniform(-0.4, 0.4)
            d = 0.2 + 1.3 * ease_out(u) * q.uniform(0.5, 1.0)
            x, y = -0.6 + d * math.cos(a), -0.05 + d * math.sin(a) * 0.7
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.08 * d, -math.pi / 2 + a), (1 - u) * 0.9 + 0.1, 0.6)
            G, H = G + g, H + h
        G += T.tapered([(-0.6, -0.05, -0.6 + 1.4 * ease_out(u), 0.0, 1.0)], 0.25) * (1 - u) * 0.5
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.05 * i, 0.72 + 0.05 * i, cx, 0.0, 0.8, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 24, 752, 0.1, -0.05, 0.8, 0.5, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ O Cavaleiro

def ferrao_cavaleiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        a0 = 0.1 + 0.12 * j
        u = ease_in(rel(t, a0, a0 + 0.1), 2)
        kk = 1 - rel(t, a0 + 0.12, a0 + 0.18)
        if u > 0 and kk > 0:
            g, h = _ferrao(T, -0.4 + 0.45 * u, -0.05 + 0.05 * (j - 1), 0.0, 0.5, kk)
            G, H = G + g, H + h
        g, h = clarao(T, t, a0 + 0.08, a0 + 0.16, 0.45, -0.05 + 0.05 * (j - 1), 0.5, 0.9)
        G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.7, 0.04, 0.45, 0.03, -0.05, 1.0, 1.2)
    G += particulas(T, t, 0.3, 1.0, 12, 753, 0.45, -0.05, 0.25, 0.4, 0.011)
    return G * env, H * env


def concentrar_cavaleiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.6)
    if 0 < u < 1:
        q = np.random.default_rng(754)
        for _ in range(14):
            a, d = q.uniform(0, TAU), q.uniform(0.4, 0.7)
            r = d * (1 - ease_in(u, 1.4))
            H += T.gauss(r * math.cos(a), -0.05 + r * math.sin(a), 0.014) * 1.8
            G += T.tapered([(r * 1.2 * math.cos(a), -0.05 + r * 1.2 * math.sin(a), r * math.cos(a), -0.05 + r * math.sin(a), 0.7)], 0.01)
    G += T.gauss(0.0, -0.05, 0.12) * pulso(t, 0.3, 0.8) * 1.3
    g, h = clarao(T, t, 0.55, 0.75, 0.0, -0.05, 1.0, 1.0)
    G, H = G + g, H + h
    c = surge(t, 0.6, 0.78) * (1 - rel(t, 0.88, 1))
    if c > 0:
        g, h = icone(T, poe(CRUZ, 0.0, -0.45, 0.07 * c), 1.2, 0.8)
        G, H = G + g, H + h
    G += _mascara_chifres(T, 0.0, -0.05, 0.3, 0.8)
    return G * env, H * env


def cavaleiro_preparo(T, t, rng):
    G, H = vazio(T)
    G += _mascara_chifres(T, 0.0, -0.05, 0.36, 1.0)
    for j in range(5):
        r = (t + j / 5) % 1
        x = -0.25 + 0.12 * j
        G += T.tapered([(x, 0.35, x + 0.03 * math.sin(r * 8 + j), 0.35 - 0.5 * r, 0.8)], 0.03) * math.sin(math.pi * r) * 0.9
    return G, H


def grito_do_abismo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    G += _mascara_chifres(T, -0.6, -0.15, 0.2, pulso(t, 0.0, 0.5))
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        for j in range(3):
            u = ease_out(rel(t, 0.2 + 0.04 * i + 0.03 * j, 0.55 + 0.04 * i + 0.03 * j), 2)
            k = 1 - rel(t, 0.8, 0.95)
            if u > 0 and k > 0:
                x0 = cx + 0.12 * (j - 1)
                pts = [(x0 + 0.05 * math.sin(v * 6 + t * 10 + j), 0.38 - 0.6 * u * v) for v in np.linspace(0, 1, 16)]
                segs = [(a[0], a[1], b[0], b[1], 1.0 - 0.6 * n / 16) for n, (a, b) in enumerate(zip(pts, pts[1:]))]
                G += T.lines(segs, 0.035) * k * 1.0
                H += T.gauss(pts[-1][0], pts[-1][1], 0.015) * k * 1.5
        g, h = clarao(T, t, 0.45 + 0.04 * i, 0.68 + 0.04 * i, cx, -0.05, 0.7, 0.9)
        G, H = G + g, H + h
        m = pulso(t, 0.6, 1.0)
        if m > 0:
            G += T.lines([(cx + 0.15, -0.3, cx + 0.15, -0.1, 1.0), (cx + 0.1, -0.16, cx + 0.15, -0.1, 1.0), (cx + 0.2, -0.16, cx + 0.15, -0.1, 1.0)], 0.012) * m * 1.2
    G += onda_no_chao(T, t, 0.2, 0.8, 1.0, 0.38, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ Goro

def quatro_socos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        a0 = 0.08 + 0.1 * j
        u = ease_in(rel(t, a0, a0 + 0.1), 2)
        kk = 1 - rel(t, a0 + 0.12, a0 + 0.2)
        if u > 0 and kk > 0:
            y = -0.25 + 0.14 * j
            P, nos = _punho(T, -0.4 + 0.6 * u, y, 1.6, 0)
            G += P * kk
            H += nos * 0.4 * kk
        g, h = clarao(T, t, a0 + 0.08, a0 + 0.16, 0.45, -0.25 + 0.14 * j, 0.5, 0.9)
        G, H = G + g, H + h
    G += anel(T, t, 0.45, 0.8, 0.05, 0.55, 0.04, -0.05, 1.0, 1.3)
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        G += T.ring(0.2, 0.01, 0.45, -0.05) * m * (0.6 + 0.4 * math.sin(t * 30))
    return G * env, H * env


def agarrao_goro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.05, 0.35), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if u > 0 and k > 0:
        for j in range(4):
            y0 = -0.25 + 0.17 * j
            alvo_y = -0.05 + 0.05 * (j - 1.5)
            x = -0.55 + 0.9 * u
            y = y0 + (alvo_y - y0) * rel(t, 0.3, 0.5)
            G += T.lines([(-0.6, y0, x, y, 1.0)], 0.04) * k
            G += T.gauss(x, y, 0.05) * k * 1.0
    m = pulso(t, 0.4, 1.0)
    if m > 0:
        for j in range(3):
            G += _zap(T, 755 + j + int(t * 10), 0.35 + 0.1 * j, -0.3, 0.4 + 0.1 * j, 0.15, 0.008, 3, 0.4) * m * 1.2
    g, h = clarao(T, t, 0.32, 0.5, 0.45, -0.05, 0.8, 1.0)
    G, H = G + g, H + h
    return G * env, H * env


def goro_preparo(T, t, rng):
    G, H = vazio(T)
    sobe = 0.5 + 0.5 * math.sin(t * TAU)
    pe = [(-0.25, 0.0), (0.25, 0.0), (0.3, 0.12), (-0.3, 0.12)]
    g, h = icone(T, poe(pe, 0.0, 0.0 - 0.25 * sobe, 1.0), 1.1, 0.6)
    G, H = G + g, H + h
    G += T.lines([(0.0, -0.5 - 0.25 * sobe, 0.0, -0.0 - 0.25 * sobe, 1.0)], 0.07) * 0.9
    G += T.ring(0.3 + 0.05 * (1 - sobe), 0.014, 0.0, 0.38, 3.0) * (1 - sobe) * 1.2
    return G, H


def pisao_de_goro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2.4)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        y = -0.6 + 0.9 * u
        pe = [(-0.3, 0.0), (0.3, 0.0), (0.36, 0.14), (-0.36, 0.14)]
        g, h = icone(T, poe(pe, 0.0, y, 1.0), k * 1.1, 0.6)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.33, 0.58, 0.0, 0.3, 1.8, 1.6)
    G, H = G + g, H + h
    racha = ease_out(rel(t, 0.35, 0.55), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if racha > 0:
        for j in range(8):
            a = math.pi * j / 7
            G += _zap(T, 760 + j, 0.0, 0.38, 0.9 * racha * math.cos(a), 0.38 + 0.08 * racha * math.sin(a), 0.012, 4, 0.15) * kk * 1.2
    G += onda_no_chao(T, t, 0.35, 0.95, 1.2, 0.38, 1.9)
    m = pulso(t, 0.55, 1.0)
    if m > 0:
        for cx in (-0.45, 0.0, 0.45):
            G += T.ring(0.14, 0.012, cx, 0.3, 3.0) * m * 1.2
    G += particulas(T, t, 0.35, 1.0, 24, 768, 0.0, 0.3, 0.8, 0.5, 0.016)
    return G * env, H * env


# ------------------------------------------------------------------ Yoshi

def engolir_yoshi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sai = ease_out(rel(t, 0.05, 0.3), 2)
    volta = ease_in(rel(t, 0.35, 0.6), 2)
    ponta = -0.5 + 0.95 * sai * (1 - volta)
    if ponta > -0.5:
        G += T.lines([(-0.5, -0.05, ponta, -0.05, 1.0)], 0.03) * 1.2
        G += T.gauss(ponta, -0.05, 0.035) * 1.3
    if volta > 0 and volta < 1:
        G += T.gauss(ponta, -0.05, 0.06) * 0.6
    # o rival engolido virando ovo (Preso)
    m = surge(t, 0.6, 0.78) * (1 - rel(t, 0.9, 1))
    if m > 0:
        g, h = _ovo(T, 0.45, -0.05, 0.13 * m, 1.0)
        G, H = G + g, H + h
        G += T.ring(0.16 * m, 0.012, 0.45, -0.05) * 0.8
    g, h = clarao(T, t, 0.25, 0.4, 0.45, -0.05, 0.7, 0.9)
    G, H = G + g, H + h
    H += T.gauss(-0.5, -0.05, 0.03) * pulso(t, 0.55, 0.8) * 1.6
    return G * env, H * env


def ovo_yoshi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.45)
    if 0 < u < 1:
        e = ease_in(u, 1.3)
        x = -0.55 + 1.0 * e
        y = -0.05 - 0.35 * math.sin(math.pi * e)
        g, h = _ovo(T, x, y, 0.13, 1.0, u * 10)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.2, y + 0.05, x - 0.05, y, 0.6)], 0.02)
    q = rel(t, 0.43, 0.8)
    if 0 < q < 1:
        x = 0.45 + 0.25 * q
        y = -0.05 - 0.3 * math.sin(math.pi * q)
        g, h = _ovo(T, x, y, 0.11 * (1 - rel(q, 0.8, 1)), 1.0, q * 12)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.42, 0.6, 0.45, -0.05, 1.1, 1.2)
    G, H = G + g, H + h
    G += estouro(T, t, 0.43, 0.75, 10, 769, 0.45, -0.05, 0.4, 0.012)
    return G * env, H * env


def yoshi_preparo(T, t, rng):
    G, H = vazio(T)
    salto = abs(math.sin(t * TAU))
    y = 0.25 - 0.55 * salto
    g, h = _ovo(T, 0.0, y, 0.2, 1.0)
    G, H = G + g, H + h
    G += T.ring(0.15 * (1 - salto) + 0.05, 0.012, 0.0, 0.38, 3.0) * (1 - salto) * 1.2
    for lado in (-1, 1):
        G += T.tapered([(lado * 0.1, y + 0.2, lado * 0.15, y + 0.35, 0.8)], 0.02) * salto
    return G, H


def pisao_de_yoshi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    sobe = ease_out(rel(t, 0.0, 0.25), 2)
    desce = ease_in(rel(t, 0.25, 0.4), 2.5)
    y = 0.2 - 0.8 * sobe + 1.0 * desce
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        g, h = _ovo(T, 0.0, min(0.25, y), 0.2, k)
        G, H = G + g, H + h
        if desce > 0:
            G += T.tapered([(0.0, min(0.25, y) - 0.4, 0.0, min(0.25, y) - 0.1, 0.8)], 0.06) * k
    g, h = clarao(T, t, 0.38, 0.6, 0.0, 0.3, 1.6, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.4, 0.95, 1.1, 0.38, 1.8)
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        m = pulso(t, 0.5 + 0.04 * i, 1.0)
        if m > 0:
            for j in range(3):
                a = TAU * j / 3 + t * 8
                g, h = icone(T, poe(ESTRELA, cx + 0.12 * math.cos(a), -0.4 + 0.05 * math.sin(a), 0.04), m, 0.8)
                G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 20, 770, 0.0, 0.3, 0.8, 0.5, 0.014)
    return G * env, H * env


REGISTRO = [
    ("disparo_de_dedo", disparo_de_dedo, GRANDE, "Cuphead · as balas de ervilha em rajada", False),
    ("dash_cuphead", dash_cuphead, GRANDE, "Cuphead · o dash e a poeira de desenho", False),
    ("cuphead_preparo", cuphead_preparo, MEDIA, "Cuphead · as cartas de super enchendo (Preparo, laço)", True),
    ("super_art_cuphead", super_art_cuphead, GRANDE, "Cuphead · o raio do Super Art", False),
    ("machado_de_aco", machado_de_aco, GRANDE, "Dovahkiin · o machado nórdico", False),
    ("fus_ro_dah_grito", fus_ro_dah_grito, GRANDE, "Dovahkiin · as três ondas do grito", False),
    ("dovahkiin_preparo", dovahkiin_preparo, MEDIA, "Dovahkiin · as runas acendendo (Preparo, laço)", True),
    ("fogo_do_dragao_dovahkiin", fogo_do_dragao_dovahkiin, GRANDE, "Dovahkiin · o grito de fogo", False),
    ("ferrao_cavaleiro", ferrao_cavaleiro, GRANDE, "O Cavaleiro · as estocadas do ferrão", False),
    ("concentrar_cavaleiro", concentrar_cavaleiro, GRANDE, "O Cavaleiro · a alma se juntando", False),
    ("cavaleiro_preparo", cavaleiro_preparo, MEDIA, "O Cavaleiro · a máscara e a sombra (Preparo, laço)", True),
    ("grito_do_abismo", grito_do_abismo, GRANDE, "O Cavaleiro · os braços de sombra", False),
    ("quatro_socos", quatro_socos, GRANDE, "Goro · os quatro socos", False),
    ("agarrao_goro", agarrao_goro, GRANDE, "Goro · os quatro braços agarrando", False),
    ("goro_preparo", goro_preparo, MEDIA, "Goro · o pé levantado (Preparo, laço)", True),
    ("pisao_de_goro", pisao_de_goro, GRANDE, "Goro · o pisão rachando o chão", False),
    ("engolir_yoshi", engolir_yoshi, GRANDE, "Yoshi · a língua e o ovo", False),
    ("ovo_yoshi", ovo_yoshi, GRANDE, "Yoshi · o ovo quicando", False),
    ("yoshi_preparo", yoshi_preparo, MEDIA, "Yoshi · pulando alto (Preparo, laço)", True),
    ("pisao_de_yoshi", pisao_de_yoshi, GRANDE, "Yoshi · o pisão e as estrelinhas", False),
]
