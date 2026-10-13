"""Rodada 54 das habilidades próprias: RoboCop, Rambo, Indiana Jones, Jack Sparrow, Harry Potter e Voldemort.

RoboCop
- auto_9: a pistola Auto-9 saindo da coxa, a rajada de três tiros e a mira do visor (Marcado).
- proteger_o_inocente: as diretrizes passando no visor e o escudo azul no aliado (Escudo e Protegido).
- robocop_preparo: o Preparo do Vivo ou morto — o visor com a linha de mira varrendo (laço).
- vivo_ou_morto: a mira travando e a rajada pesada no rival.

Rambo
- flecha_explosiva_rambo: o arco composto, a flecha com a ponta explosiva cravando e piscando (Marca explosiva).
- faca_de_sobrevivencia: a faca serrilhada girando e o corte.
- rambo_preparo: o Preparo da Emboscada na selva — a faixa vermelha, as folhas e os olhos no mato (laço).
- emboscada_na_selva: as armadilhas de corda e as folhas caindo sobre todos os rivais (Preso).

Indiana Jones
- chicotada: o chicote estalando, enrolando no rival e arrancando o buff (Preso e Dissipar).
- pedra_rolando: a pedra gigante rolando por cima de todos os rivais (Lento).
- indy_preparo: o Preparo da Relíquia — o chapéu e o ídolo dourado brilhando (laço).
- reliquia: o ídolo dourado acendendo e a luz sagrada sobre o trio (Fortalecido e Protegido).

Jack Sparrow
- bussola_magica: a bússola girando sem parar e apontando para o rival (Marcado e Confuso).
- pistola_de_um_tiro: a pistola de pederneira, a fumaça e a única bala.
- sparrow_preparo: o Preparo da Pérola Negra — o chapéu tricórnio e as velas negras ao vento (laço).
- perola_negra: o navio de velas negras, os canhões disparando em todos os rivais (Exposto).

Harry Potter
- expelliarmus_harry: o raio vermelho da varinha e os buffs voando longe (Dissipar).
- protego: o escudo transparente brilhando na frente de cada um do trio (Barreira e Escudo).
- harry_preparo: o Preparo do Expecto Patronum — a varinha erguida e a névoa prateada (laço).
- expecto_patronum: o cervo prateado galopando sobre os rivais e a luz limpando o trio (Purificar).

Voldemort
- crucio: o raio vermelho de dor e o rival se contorcendo (Amaldiçoado).
- imperius: os fios verdes de controle descendo no rival como uma marionete (Confuso e Enfraquecido).
- voldemort_preparo: o Preparo do Avada Kedavra — a varinha de osso e a Marca Negra no alto (laço).
- avada_kedavra: o raio verde da maldição da morte e o clarão verde.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (FOLHA, anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _mira(T, cx, cy, r, k, w=0.012):
    G = T.ring(r, w, cx, cy) * k * 1.2
    for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
        G += T.lines([(cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a), cx + r * 1.3 * math.cos(a), cy + r * 1.3 * math.sin(a), 1.0)], w * 0.8) * k * 1.3
    return G


def _pistola(T, x, y, s, k):
    G = T.lines([(x, y, x + s, y, 1.0)], s * 0.14) * k * 1.2
    G += T.polys([([(x, y - s * 0.05), (x + s * 0.2, y - s * 0.05), (x + s * 0.05, y + s * 0.45), (x - s * 0.15, y + s * 0.45)], 1.0)], 0.003) * k * 1.0
    return G


def _chicote(T, x0, y0, x1, y1, amp, fase, k, w=0.012):
    pts = []
    for u in np.linspace(0, 1, 30):
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + amp * math.sin(u * 7 + fase) * u * (1 - u) * 4
        pts.append((x, y))
    return T.polyline(pts, w) * k


def _varinha(T, x, y, ang, s, k, osso=False):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.tapered([(x - c * s, y - sn * s, x, y, 1.0)], s * 0.06) * k * 1.2
    if osso:
        for u in (0.3, 0.55, 0.8):
            G += T.gauss(x - c * s * u, y - sn * s * u, s * 0.04) * k * 1.4
    return G, T.gauss(x, y, s * 0.04) * k * 1.6


def _cervo_patrono(T, cx, cy, s, k):
    corpo = [(-0.6, 0.2), (-0.55, -0.1), (-0.2, -0.15), (0.3, -0.15), (0.45, -0.35), (0.55, -0.6), (0.7, -0.55), (0.6, -0.3), (0.65, -0.1),
             (0.45, 0.0), (0.4, 0.2), (0.45, 0.6), (0.35, 0.6), (0.25, 0.2), (-0.3, 0.2), (-0.35, 0.6), (-0.45, 0.6), (-0.45, 0.25)]
    g, h = icone(T, poe(corpo, cx, cy, s), k, 0.5)
    for p in ([(0.55, -0.6), (0.5, -0.85), (0.4, -1.0)], [(0.5, -0.85), (0.65, -0.95)], [(0.62, -0.58), (0.75, -0.8), (0.85, -0.88)]):
        g = g + T.polyline([(cx + x * s, cy + y * s) for x, y in p], s * 0.04) * k * 1.2
    return g, h + T.gauss(cx, cy, s * 0.5) * k * 0.6


def _marca_negra(T, cx, cy, s, k, t):
    caveira = [(-0.6, -0.2), (-0.5, -0.75), (0.0, -0.95), (0.5, -0.75), (0.6, -0.2), (0.35, 0.2), (0.3, 0.6), (-0.3, 0.6), (-0.35, 0.2)]
    G, H = icone(T, poe(caveira, cx, cy, s), k, 0.4)
    for lado in (-1, 1):
        G = G + T.gauss(cx + lado * s * 0.25, cy - s * 0.25, s * 0.12) * k * -0.5
    pts = []
    for u in np.linspace(0, 1, 30):
        pts.append((cx + s * 0.1 * math.sin(u * 15 + t * 5), cy + s * 0.4 + s * 1.2 * u))
    G = G + T.polyline(pts, s * 0.08) * k * 1.2
    G = G + T.gauss(cx, cy + s * 1.6, s * 0.12) * k * 1.0
    return G, H


def _navio(T, cx, cy, s, k, t):
    casco = [(-1.0, 0.0), (1.0, 0.0), (0.8, 0.35), (-0.75, 0.35)]
    G, H = icone(T, poe(casco, cx, cy, s), k, 0.5)
    for m, (x, h) in enumerate(((-0.45, 1.1), (0.05, 1.35), (0.55, 1.0))):
        G = G + T.lines([(cx + x * s, cy, cx + x * s, cy - h * s, 1.0)], s * 0.04) * k
        bal = 0.05 * math.sin(t * 6 + m)
        vela = [(cx + x * s - s * 0.3, cy - h * s * 0.9), (cx + x * s + s * (0.3 + bal), cy - h * s * 0.85), (cx + x * s + s * (0.35 + bal), cy - h * s * 0.35),
                (cx + x * s - s * 0.3, cy - h * s * 0.35)]
        g2, h2 = icone(T, vela, k * 0.7, 0.25)
        G, H = G + g2, H + h2
    return G, H


def _bussola(T, cx, cy, r, ang, k):
    G = T.ring(r, r * 0.12, cx, cy) * k * 1.3
    G += T.gauss(cx, cy, r * 0.8) * k * 0.25
    for j in range(8):
        a = TAU * j / 8
        G += T.lines([(cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a), cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a), 1.0)], r * 0.05) * k
    c, sn = math.cos(ang), math.sin(ang)
    agulha = [(cx + c * r * 0.75, cy + sn * r * 0.75), (cx - sn * r * 0.1, cy + c * r * 0.1), (cx - c * r * 0.5, cy - sn * r * 0.5), (cx + sn * r * 0.1, cy - c * r * 0.1)]
    g, h = icone(T, agulha, k * 1.3, 0.6)
    return G + g, h


# ------------------------------------------------------------------ RoboCop

def auto_9(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sai = ease_out(rel(t, 0.0, 0.2), 2)
    k = 1 - rel(t, 0.75, 0.88)
    if k > 0:
        G += _pistola(T, -0.6, 0.15 - 0.2 * sai, 0.42, k)
    for j in range(3):
        a0 = 0.25 + 0.07 * j
        g, h = clarao(T, t, a0, a0 + 0.05, -0.38, -0.05, 0.35, 1.0)
        G, H = G + g, H + h
        u = rel(t, a0, a0 + 0.08)
        if 0 < u < 1:
            x = -0.38 + 0.83 * u
            H += T.lines([(x - 0.15, -0.05, x, -0.05 + 0.02 * (j - 1) * u, 1.0)], 0.006) * 1.8
        g2, h2 = clarao(T, t, a0 + 0.07, a0 + 0.15, 0.45, -0.03 + 0.03 * (j - 1), 0.4, 0.8)
        G, H = G + g2, H + h2
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += _mira(T, 0.45, -0.03, 0.22 * m, 1.0, 0.014)
        G += T.polyline([(0.28, -0.22), (0.62, -0.22), (0.62, 0.16), (0.28, 0.16), (0.28, -0.22)], 0.006) * m * 0.9
    return G * env, H * env


def proteger_o_inocente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    for j in range(3):
        u = rel(t, 0.05 + 0.1 * j, 0.35 + 0.1 * j)
        if 0 < u < 1:
            L = 0.3 * min(1.0, u * 2)
            G += T.lines([(-0.75, -0.5 + 0.08 * j, -0.75 + L, -0.5 + 0.08 * j, 1.0)], 0.012) * (1 - rel(u, 0.8, 1)) * 1.2
    s = surge(t, 0.3, 0.55)
    if s > 0 and k > 0:
        r = 0.26 * s
        G += T.arc_band(r, 0.035, -math.pi * 0.85, -math.pi * 0.15, 1.0, 0, 0.0, 0.15, 0.0) * k * 1.3
        G += T.gauss(0.0, -0.05, 0.2, 0.18) * k * 0.3
        hex_ = [(math.cos(a) * 0.15, -0.05 + math.sin(a) * 0.18) for a in np.linspace(0, TAU, 7)]
        G += T.polyline(hex_, 0.01) * k * s * 1.0
        brilho = (t * 1.5) % 1
        G += T.lines([(-0.2, -0.2 + 0.3 * brilho, 0.2, -0.2 + 0.3 * brilho, 1.0)], 0.007) * k * 0.9
    G += anel(T, t, 0.35, 0.75, 0.1, 0.6, 0.03, 0.15, 3.0)
    return G * env, H * env


def robocop_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.polys([([(-0.4, -0.1), (0.4, -0.1), (0.35, 0.05), (-0.35, 0.05)], 1.0)], 0.01) * 0.5
    x = -0.35 + 0.7 * (0.5 + 0.5 * math.sin(t * TAU * 1.5))
    G += T.lines([(x, -0.1, x, 0.05, 1.0)], 0.01) * 1.3
    H += T.gauss(x, -0.025, 0.02) * 1.8
    G += T.polyline([(-0.42, -0.12), (0.42, -0.12), (0.37, 0.07), (-0.37, 0.07), (-0.42, -0.12)], 0.008) * 1.2
    return G, H


def vivo_ou_morto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    trava = ease_out(rel(t, 0.0, 0.3), 2)
    if t < 0.6:
        G += _mira(T, 0.45, 0.0, 0.3 - 0.17 * trava, 1.0 - rel(t, 0.5, 0.6), 0.012)
    k = pulso(t, 0.0, 0.85)
    if k > 0:
        G += _pistola(T, -0.65, -0.05, 0.22, k)
    for j in range(5):
        a0 = 0.3 + 0.06 * j
        g, h = clarao(T, t, a0, a0 + 0.05, -0.4, -0.05, 0.35, 1.0)
        G, H = G + g, H + h
        u = rel(t, a0, a0 + 0.07)
        if 0 < u < 1:
            H += T.lines([(-0.4 + 0.85 * u - 0.15, -0.05, -0.4 + 0.85 * u, -0.05, 1.0)], 0.007) * 1.8
    g2, h2 = clarao(T, t, 0.38, 0.75, 0.45, 0.0, 1.6, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.4, 0.85, 0.05, 0.6, 0.04, 0.0, 1.0, 1.3)
    G += estouro(T, t, 0.4, 0.9, 16, 184, 0.45, 0.0, 0.55, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Rambo

def _flecha(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s, y - sn * s, x, y, 1.0)], s * 0.05) * k * 1.3
    ponta = [(x + c * s * 0.25, y + sn * s * 0.25), (x - sn * s * 0.12, y + c * s * 0.12), (x + sn * s * 0.12, y - c * s * 0.12)]
    g, h = icone(T, ponta, k * 1.3, 0.6)
    G += T.gauss(x - c * s * 0.05, y - sn * s * 0.05, s * 0.06) * k * 1.2
    return G + g, h


def flecha_explosiva_rambo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.arc_band(0.28, 0.025, -1.1, 1.1, 1.0, 0, -0.75, 0.0, 0.0) * pulso(t, 0.0, 0.4) * 1.2
    u = ease_in(rel(t, 0.05, 0.3), 1.4)
    if 0 < u < 1:
        x = -0.6 + 0.95 * u
        g, h = _flecha(T, x, 0.0, 0.0, 0.4, 1.0)
        G, H = G + g, H + h
    kk = 1 - rel(t, 0.88, 1)
    if t >= 0.3 and kk > 0:
        g, h = _flecha(T, 0.35, 0.0, 0.0, 0.4, kk)
        G, H = G + g, H + h
        pisca = 1.0 if (t * 8) % 1 < 0.5 else 0.2
        H += T.gauss(0.36, 0.0, 0.025) * pisca * kk * 2.0
        G += T.ring(0.07 + 0.08 * ((t * 4) % 1), 0.008, 0.36, 0.0) * (1 - (t * 4) % 1) * kk * 1.2
    g2, h2 = clarao(T, t, 0.28, 0.45, 0.4, 0.0, 0.8, 1.0)
    return (G + g2) * env, (H + h2) * env


_FACA_SERRA = [(0, -1), (0.2, -0.75), (0.22, 0.25), (0.35, 0.3), (0.35, 0.4), (0.1, 0.4), (0.1, 0.95), (-0.1, 0.95), (-0.1, 0.4), (-0.35, 0.4),
               (-0.35, 0.3), (-0.1, 0.25), (-0.12, 0.1), (-0.04, 0.0), (-0.12, -0.1), (-0.04, -0.2), (-0.12, -0.3), (-0.04, -0.4), (-0.1, -0.7)]


def faca_de_sobrevivencia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        x = -0.55 + 0.95 * u
        g, h = icone(T, poe(_FACA_SERRA, x, -0.05, 0.3, t * 20 * (1 - u) + math.pi / 2), k * 1.3, 0.5)
        G, H = G + g, H + h
        if u < 1:
            G += T.ring(0.3, 0.008, x, -0.05) * k * (1 - u) * 0.8
    g2, h2 = corte(T, t, 0.32, 0.52, 0.7, 1.0, 0.08, 0.45, 0.0)
    G, H = G + g2 * 1.2, H + h2
    g3, h3 = clarao(T, t, 0.33, 0.55, 0.45, 0.0, 1.1, 1.2)
    G, H = G + g3, H + h3
    return G * env, H * env


def rambo_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.35, -0.2, 0.35, -0.2, 1.0)], 0.04) * 1.0
    for m in range(2):
        G += _chicote(T, 0.35, -0.2, 0.55, -0.1 + 0.12 * m, 0.04, t * 10 + m, 1.0, 0.02)
    for j in range(8):
        a = math.pi * (j / 7) + 0.1 * math.sin(t * TAU + j)
        g, h = icone(T, poe(FOLHA, 0.45 * math.cos(a), 0.3 - 0.15 * math.sin(a), 0.07, a + math.pi / 2), 0.9, 0.4)
        G, H = G + g, H + h
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, 0.05, 0.012) * 2.0
    return G, H


def emboscada_na_selva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(185)
    for j in range(14):
        x = q.uniform(-0.85, 0.85)
        a0 = q.uniform(0.0, 0.3)
        u = rel(t, a0, a0 + 0.6)
        if 0 < u < 1:
            y = -0.9 + 1.2 * ease_in(u, 1.3)
            g, h = icone(T, poe(FOLHA, x + 0.06 * math.sin(u * 8 + j), y, 0.05, u * 6 + j), (1 - rel(u, 0.85, 1)) * 1.0, 0.4)
            G, H = G + g, H + h
    kk = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        fecha = ease_out(rel(t, 0.3 + 0.07 * i, 0.5 + 0.07 * i), 2)
        if fecha > 0 and kk > 0:
            G += T.lines([(cx, -0.9, cx, -0.9 + 0.75 * fecha, 1.0)], 0.01) * kk * 1.1
            for m in range(3):
                G += T.arc_band(0.14 - 0.015 * m, 0.016, -1.0, -1.0 + TAU * 0.85 * fecha, 0.4, 0, cx, -0.05 + 0.1 * m, 1.0) * kk * 1.3
        g2, h2 = clarao(T, t, 0.45 + 0.07 * i, 0.65 + 0.07 * i, cx, 0.05, 0.4, 0.8)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Indiana Jones

def chicotada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.28), 2)
    k = 1 - rel(t, 0.28, 0.4)
    if u > 0 and k > 0:
        G += _chicote(T, -0.6, 0.0, -0.6 + 1.05 * u, -0.05, 0.2 * (1 - u), t * 30, k * 1.4, 0.02)
    g, h = clarao(T, t, 0.25, 0.38, 0.45, -0.05, 0.6, 1.1)
    G, H = G + g, H + h
    enrola = ease_out(rel(t, 0.3, 0.5), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if enrola > 0 and kk > 0:
        G += _chicote(T, -0.6, 0.0, 0.3, -0.02, 0.03, 0, kk * 1.1, 0.017)
        for m in range(3):
            a0 = -2.5 + m * 0.4
            G += T.arc_band(0.14 - 0.02 * m, 0.016, a0, a0 + TAU * enrola * 0.85, 0.4, 0, 0.45, -0.1 + 0.08 * m, 1.0) * kk * 1.3
    q = np.random.default_rng(186)
    for _ in range(6):
        w = rel(t, 0.5, 0.85)
        if 0 < w < 1:
            a = q.uniform(-math.pi, 0)
            d = 0.05 + 0.3 * ease_out(w)
            g2, h2 = icone(T, poe([(0, -1), (0.8, 0.7), (-0.6, 0.5)], 0.45 + d * math.cos(a), -0.3 + d * math.sin(a) + 0.3 * w * w, 0.03, a + 8 * w),
                           (1 - w) * 1.1, 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


def pedra_rolando(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.75)
    if 0 < u < 1:
        x = -1.1 + 2.2 * ease_in(u, 1.15)
        r = 0.3
        G += T.gauss(x, 0.38 - r, r * 0.9) * 0.6
        G += T.ring(r, 0.03, x, 0.38 - r) * 1.3
        a = -x / r
        for j in range(4):
            aa = a + TAU * j / 4
            G += T.arc_band(r * 0.6, 0.012, aa, aa + 1.0, 1.0, 0, x, 0.38 - r, 0.0) * 1.0
        G += onda_no_chao(T, (t * 4) % 1, 0.0, 1.0, 0.4, 0.38, 0.8)
        q = np.random.default_rng(int(t * 25))
        for _ in range(5):
            G += T.gauss(x - r - q.uniform(0, 0.25), 0.36 - q.uniform(0, 0.12), 0.015) * 1.2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.15 + (cx + 1.1) / 2.2 * 0.6
        g, h = clarao(T, t, a0, a0 + 0.15, cx, 0.1, 0.5, 1.0)
        G, H = G + g, H + h
    return G * env, H * env


def _idolo(T, cx, cy, s, k):
    G, H = icone(T, poe([(-0.5, 0.9), (-0.55, 0.3), (-0.4, -0.2), (-0.45, -0.6), (-0.2, -0.95), (0.2, -0.95), (0.45, -0.6), (0.4, -0.2), (0.55, 0.3),
                         (0.5, 0.9)], cx, cy, s), k, 0.55)
    for lado in (-1, 1):
        H = H + T.gauss(cx + lado * s * 0.15, cy - s * 0.55, s * 0.05) * k * 1.6
    G = G + T.lines([(cx - s * 0.2, cy - s * 0.25, cx + s * 0.2, cy - s * 0.25, 1.0)], s * 0.04) * k
    return G, H


def indy_preparo(T, t, rng):
    G, H = vazio(T)
    chapeu = [(-0.7, 0.2), (-0.4, 0.15), (-0.35, -0.35), (0.35, -0.35), (0.4, 0.15), (0.7, 0.2), (0.7, 0.3), (-0.7, 0.3)]
    g, h = icone(T, poe(chapeu, 0.0, -0.32, 0.22), 1.0, 0.4)
    G, H = G + g, H + h
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g2, h2 = _idolo(T, 0.0, 0.15, 0.14, 1.0 + 0.3 * b)
    G, H = G + g2, H + h2
    G += T.gauss(0.0, 0.15, 0.2) * (0.25 + 0.2 * b)
    return G, H


def reliquia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _idolo(T, 0.0, -0.45, 0.16 * s, 1.2)
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.45, 0.3 * s) * 0.3
        for j in range(10):
            a = TAU * j / 10 + t
            G += T.tapered([(0.2 * math.cos(a), -0.45 + 0.2 * math.sin(a), 0.4 * math.cos(a), -0.45 + 0.4 * math.sin(a), 1.0)], 0.02) * s * 0.7
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.3 + 0.05 * i, 0.5 + 0.05 * i)
        if 0 < u < 1:
            G += T.tapered([(0.0, -0.35, cx * u, -0.35 + 0.5 * u, 1.0)], 0.03) * (1 - u) * 1.2
        k = pulso(t, 0.45 + 0.05 * i, 1.0)
        if k > 0:
            G += T.gauss(cx, 0.15, 0.14, 0.2) * k * 0.4
            G += T.ring(0.18, 0.012, cx, 0.15) * k * 1.0
            for m in range(2):
                y0 = 0.25 - 0.3 * rel(t, 0.45, 1.0) - 0.08 * m
                G += T.polyline([(cx - 0.06, y0 + 0.06), (cx, y0), (cx + 0.06, y0 + 0.06)], 0.014) * k * 1.2
    G += particulas(T, t, 0.3, 1.0, 16, 187, 0.0, -0.2, 0.6, 0.4, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Jack Sparrow

def bussola_magica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    gira = t * 25 * (1 - ease_out(rel(t, 0.2, 0.5), 2)) + 0.25 * ease_out(rel(t, 0.2, 0.5), 2)
    if s > 0:
        g, h = _bussola(T, -0.5, -0.1, 0.28 * s, gira, 1.0)
        G, H = G + g, H + h
    u = rel(t, 0.45, 0.65)
    if 0 < u < 1:
        G += T.tapered([(-0.32, -0.05, -0.32 + 0.77 * u, -0.05 + 0.05 * u, 1.0)], 0.02) * 1.2
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += _mira(T, 0.45, 0.0, 0.2 * m, 1.0, 0.013)
        pts = [(0.45 + 0.12 * u2 * math.cos(-t * 8 + u2 * 9), -0.32 + 0.12 * u2 * math.sin(-t * 8 + u2 * 9) * 0.8) for u2 in np.linspace(0.05, 1, 30)]
        G += T.polyline(pts, 0.012) * m * 1.3
    return G * env, H * env


def pistola_de_um_tiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.7)
    if k > 0:
        G += T.lines([(-0.65, -0.05, -0.38, -0.05, 1.0)], 0.03) * k * 1.2
        G += T.polys([([(-0.65, -0.07), (-0.7, 0.12), (-0.62, 0.15), (-0.58, -0.03)], 1.0)], 0.003) * k * 1.0
    g, h = clarao(T, t, 0.25, 0.4, -0.36, -0.05, 0.6, 1.3)
    G, H = G + g, H + h
    for j in range(5):
        w = rel(t, 0.27, 0.9)
        if 0 < w < 1:
            G += T.gauss(-0.36 + 0.08 * j * w + 0.05 * w, -0.05 - 0.1 * w * (j % 3) * 0.5, 0.03 + 0.05 * w) * (1 - w) * 0.45
    u = rel(t, 0.28, 0.38)
    if 0 < u < 1:
        x = -0.36 + 0.81 * u
        G += T.gauss(x, -0.05, 0.015) * 1.5
        H += T.lines([(x - 0.12, -0.05, x, -0.05, 1.0)], 0.006) * 1.6
    g2, h2 = clarao(T, t, 0.36, 0.6, 0.45, -0.03, 1.5, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.38, 0.75, 0.05, 0.5, 0.04, 0.0)
    G += estouro(T, t, 0.38, 0.8, 12, 188, 0.45, 0.0, 0.45, 0.012)
    return G * env, H * env


def sparrow_preparo(T, t, rng):
    G, H = vazio(T)
    chapeu = [(-0.8, 0.1), (-0.55, -0.15), (-0.3, -0.45), (0.0, -0.25), (0.3, -0.45), (0.55, -0.15), (0.8, 0.1), (0.4, 0.2), (-0.4, 0.2)]
    g, h = icone(T, poe(chapeu, 0.0, -0.05, 0.25), 1.0, 0.4)
    G, H = G + g, H + h
    for m in range(3):
        y = 0.18 + 0.07 * m
        G += T.polyline([(-0.4 + 0.8 * u, y + 0.02 * math.sin(u * 12 + t * TAU * 2 + m)) for u in np.linspace(0, 1, 20)], 0.006) * 0.9
    return G, H


def perola_negra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _navio(T, -0.55, -0.2, 0.22, s, t)
        G, H = G + g, H + h
        G += T.polyline([(-0.95 + 0.8 * u, -0.1 + 0.02 * math.sin(u * 20 + t * 15)) for u in np.linspace(0, 1, 30)], 0.008) * s * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.3 + 0.07 * i
        g2, h2 = clarao(T, t, a0, a0 + 0.08, -0.4, -0.18, 0.3, 1.0)
        G, H = G + g2, H + h2
        u = rel(t, a0, a0 + 0.25)
        if 0 < u < 1:
            x, y = -0.4 + (cx + 0.4) * u, -0.18 - 0.35 * math.sin(math.pi * u) + 0.18 * u
            G += T.gauss(x, y, 0.025) * 1.4
            G += T.tapered([(x - 0.1, y + 0.05 * (1 - 2 * u), x, y, 0.6)], 0.02) * 0.8
        g3, h3 = clarao(T, t, a0 + 0.25, a0 + 0.45, cx, 0.0, 0.55, 1.1)
        G, H = G + g3, H + h3
        G += estouro(T, t, a0 + 0.25, a0 + 0.6, 8, 189 + i, cx, 0.0, 0.3, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Harry Potter

def expelliarmus_harry(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.7)
    g, h = _varinha(T, -0.5, -0.05, 0.0, 0.36, k)
    G, H = G + g, H + h
    u = rel(t, 0.1, 0.35)
    kk = 1 - rel(t, 0.45, 0.55)
    if u > 0 and kk > 0:
        ponta = -0.5 + 0.95 * min(1.0, ease_in(u) * 1.2)
        G += T.tapered([(-0.5, -0.05, ponta, -0.02, 1.0)], 0.06) * kk * 0.8
        G += T.lines([(-0.5, -0.05, ponta, -0.02, 1.0)], 0.014) * kk * 1.4
        H += T.lines([(-0.5, -0.05, ponta, -0.02, 1.0)], 0.005) * kk * 1.2
    g2, h2 = clarao(T, t, 0.3, 0.52, 0.45, -0.02, 1.2, 1.3)
    G, H = G + g2, H + h2
    for j in range(2):
        w = rel(t, 0.38 + 0.06 * j, 0.9)
        if 0 < w < 1:
            x = 0.45 + 0.45 * ease_out(w)
            y = -0.05 - 0.4 * math.sin(math.pi * w * 0.8) + 0.1 * j
            G += T.ring(0.08, 0.014, x, y) * (1 - rel(w, 0.8, 1)) * 1.3
            H += T.gauss(x, y, 0.015) * (1 - rel(w, 0.8, 1)) * 1.4
            G += T.tapered([(0.45, -0.05, x, y, 0.5)], 0.01) * (1 - w) * 0.8
    return G * env, H * env


def protego(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.05 + 0.07 * i, 0.3 + 0.07 * i)
        if s > 0 and k > 0:
            G += T.gauss(cx + 0.18, 0.0, 0.03, 0.25 * s) * k * 0.5
            G += T.arc_band(0.3 * s, 0.03, -0.9, 0.9, 1.0, 0, cx - 0.12, 0.0, 0.0) * k * 1.2
            onda = (t * 1.5 + 0.3 * i) % 1
            G += T.arc_band(0.3 * s * onda, 0.008, -0.9, 0.9, 1.0, 0, cx - 0.12, 0.0, 0.0) * k * (1 - onda) * 0.9
            H += T.arc_band(0.3 * s, 0.006, -0.9, 0.9, 1.0, 0, cx - 0.12, 0.0, 0.0) * k * 0.6
    G += converge(T, t, 0.0, 0.25, 8, 192, 0.0, 0.0, 0.5, 0.007)
    return G * env, H * env


def harry_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _varinha(T, 0.0, -0.25, -math.pi / 2, 0.3, 1.0)
    G, H = G + g, H + h
    for m in range(5):
        a = t * TAU * 0.8 + TAU * m / 5
        G += T.gauss(0.25 * math.cos(a), -0.15 + 0.12 * math.sin(a), 0.09, 0.05) * 0.35
    H += T.gauss(0.0, -0.25, 0.03) * (1.2 + 0.4 * math.sin(t * TAU * 2))
    return G, H


def expecto_patronum(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.5)
    g, h = _varinha(T, -0.65, 0.0, -0.3, 0.2, k)
    G, H = G + g, H + h
    G += T.gauss(-0.6, -0.05, 0.12) * k * 0.6
    u = rel(t, 0.15, 0.75)
    if 0 < u < 1:
        x = -0.6 + 1.3 * ease_in(u, 1.1)
        y = -0.15 - 0.08 * abs(math.sin(u * TAU * 2.5))
        g2, h2 = _cervo_patrono(T, x, y, 0.22, 1.1)
        G, H = G + g2, H + h2
        G += T.tapered([(x - 0.6, y + 0.05, x - 0.15, y, 0.8)], 0.1) * 0.5
        G += particulas(T, (t * 3) % 1, 0.0, 1.0, 8, 193, x - 0.15, y, 0.1, 0.2, 0.01)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.25 + (cx + 0.6) / 1.3 * 0.55
        g3, h3 = clarao(T, t, a0, a0 + 0.2, cx, 0.0, 0.5, 1.0)
        G, H = G + g3, H + h3
    G += anel(T, t, 0.75, 1.0, 0.1, 1.0, 0.03, 0.2, 3.0)
    return G * env, H * env


# ------------------------------------------------------------------ Voldemort

def crucio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    g, h = _varinha(T, -0.5, -0.05, 0.0, 0.22, k, True)
    G, H = G + g, H + h
    kk = pulso(t, 0.15, 0.8)
    if kk > 0:
        for j in range(2):
            G += _zap(T, int(t * 30) + 4 * j, -0.5, -0.05, 0.45, 0.0, 0.016 - 0.006 * j, 4, 0.12) * kk * 1.3
        H += _zap(T, int(t * 30), -0.5, -0.05, 0.45, 0.0, 0.006, 4, 0.12) * kk
        treme = 0.02 * math.sin(t * 50)
        G += T.gauss(0.45 + treme, 0.0, 0.12, 0.2) * kk * 0.45
        for m in range(4):
            a = t * 9 + TAU * m / 4
            G += T.arc_band(0.18, 0.012, a, a + 0.8, 1.0, 0, 0.45 + treme, 0.0, 1.0) * kk * 1.0
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.07 * m, 0.012, 0.45, -0.3) * 1.3
        G += T.lines([(0.4, -0.35, 0.5, -0.25, 1.0)], 0.012) * m * 1.3
    return G * env, H * env


def imperius(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    g, h = _varinha(T, -0.5, -0.1, -0.4, 0.22, k, True)
    G, H = G + g, H + h
    desce = ease_out(rel(t, 0.15, 0.45), 2)
    kk = 1 - rel(t, 0.85, 0.97)
    if desce > 0 and kk > 0:
        for j in range(4):
            x = 0.33 + 0.08 * j
            y1 = -0.85 + (0.7 + 0.1 * (j % 2)) * desce
            G += T.lines([(x + 0.02 * math.sin(t * 6 + j), -0.85, x, y1, 1.0)], 0.005) * kk * 1.3
            H += T.gauss(x, y1, 0.008) * kk * 1.5
        G += T.lines([(0.25, -0.85, 0.65, -0.85, 1.0)], 0.014) * kk * desce * 1.2
        G += T.gauss(0.45, 0.0, 0.12, 0.2) * kk * desce * 0.35
        for lado in (-1, 1):
            H += T.gauss(0.45 + lado * 0.05, -0.12, 0.012) * kk * desce * 1.8
    m = surge(t, 0.55, 0.75) * kk
    if m > 0:
        pts = [(0.45 + 0.1 * u2 * math.cos(-t * 8 + u2 * 9), -0.3 + 0.1 * u2 * math.sin(-t * 8 + u2 * 9) * 0.8) for u2 in np.linspace(0.05, 1, 30)]
        G += T.polyline(pts, 0.011) * m * 1.2
    return G * env, H * env


def voldemort_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _varinha(T, 0.15, 0.1, -2.2, 0.3, 1.0, True)
    G, H = G + g, H + h
    g2, h2 = _marca_negra(T, -0.05, -0.35, 0.09, 0.9 + 0.2 * math.sin(t * TAU), t)
    G, H = G + g2, H + h2
    G += T.gauss(-0.05, -0.3, 0.25) * 0.2
    return G, H


def avada_kedavra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    g, h = _varinha(T, -0.55, -0.05, 0.0, 0.22, k, True)
    G, H = G + g, H + h
    G += converge(T, t, 0.0, 0.3, 12, 194, -0.55, -0.05, 0.35, 0.008)
    u = rel(t, 0.25, 0.42)
    kk = 1 - rel(t, 0.55, 0.68)
    if u > 0 and kk > 0:
        ponta = -0.55 + 1.0 * min(1.0, ease_in(u) * 1.2)
        G += T.tapered([(-0.55, -0.05, ponta, 0.0, 1.0)], 0.13) * kk * 0.8
        G += _zap(T, int(t * 30), -0.55, -0.05, ponta, 0.0, 0.025, 5, 0.12) * kk * 1.4
        H += _zap(T, int(t * 30), -0.55, -0.05, ponta, 0.0, 0.01, 5, 0.12) * kk * 1.2
    g2, h2 = clarao(T, t, 0.4, 0.75, 0.45, 0.0, 2.0, 1.8)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.42, 0.85, 0.05, 0.75, 0.05, 0.0, 1.0, 1.4)
    f = pulso(t, 0.4, 0.7)
    G += T.gauss(0.2, 0.0, 0.8, 0.5) * f * 0.25
    return G * env, H * env


# ------------------------------------------------------------------ Light (Mecânica única)

def pagina_no_relogio(T, t, rng):
    """Light: o relógio abre o fundo falso, a tira do Death Note sai, a caneta escreve o nome e o rival cai."""
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = 1 - rel(t, 0.7, 0.82)
    cx, cy = -0.5, 0.0
    if k > 0:
        # a pulseira e o mostrador
        G += T.lines([(cx - 0.05, cy - 0.32, cx - 0.05, cy - 0.16, 1.0), (cx + 0.05, cy - 0.32, cx + 0.05, cy - 0.16, 1.0),
                      (cx - 0.05, cy + 0.16, cx - 0.05, cy + 0.32, 1.0), (cx + 0.05, cy + 0.16, cx + 0.05, cy + 0.32, 1.0)], 0.02) * k * 1.0
        G += T.ring(0.15, 0.022, cx, cy) * k * 1.3
        G += T.gauss(cx, cy, 0.12) * k * 0.25
        for j in range(12):
            a = TAU * j / 12
            G += T.lines([(cx + 0.11 * math.cos(a), cy + 0.11 * math.sin(a), cx + 0.13 * math.cos(a), cy + 0.13 * math.sin(a), 1.0)], 0.005) * k
        G += T.lines([(cx, cy, cx + 0.07 * math.cos(-1.2), cy + 0.07 * math.sin(-1.2), 1.0), (cx, cy, cx + 0.1 * math.cos(-0.2 - t * 3), cy + 0.1 * math.sin(-0.2 - t * 3), 1.0)], 0.008) * k * 1.3
        # o botão da coroa apertado quatro vezes (o mecanismo)
        for j in range(4):
            H += T.gauss(cx + 0.17, cy, 0.012) * pulso(t, 0.02 + 0.05 * j, 0.06 + 0.05 * j) * 2.0
    # o fundo falso abre e a tira sai
    sai = ease_out(rel(t, 0.2, 0.38), 2)
    if sai > 0 and k > 0:
        x0, x1 = cx + 0.05, cx + 0.05 + 0.45 * sai
        G += T.polys([([(x0, cy + 0.17), (x1, cy + 0.15), (x1, cy + 0.25), (x0, cy + 0.27)], 1.0)], 0.004) * k * 0.6
        G += T.polyline([(x0, cy + 0.17), (x1, cy + 0.15), (x1, cy + 0.25), (x0, cy + 0.27)], 0.006) * k * 1.2
        # a caneta escrevendo o nome
        esc = rel(t, 0.38, 0.55)
        if esc > 0:
            q = np.random.default_rng(250)
            pts = [(x0 + 0.03 + 0.37 * v, cy + 0.2 + 0.025 * math.sin(v * 40) * q.uniform(0.6, 1.0)) for v in np.linspace(0, min(1.0, esc), 30)]
            G += T.polyline(pts, 0.006) * k * 1.4
            px, py = pts[-1]
            G += T.lines([(px, py, px + 0.06, py - 0.12, 1.0)], 0.012) * k * pulso(t, 0.36, 0.6) * 1.3
            H += T.gauss(px, py, 0.012) * k * pulso(t, 0.36, 0.6) * 1.6
    # a sentença viaja até o rival
    u = rel(t, 0.55, 0.68)
    if 0 < u < 1:
        x = -0.05 + 0.5 * ease_in(u)
        G += T.tapered([(x - 0.25, 0.2 - 0.2 * u, x, 0.2 - 0.2 * u, 1.0)], 0.03) * 1.2
    # o coração do rival para (o anel de batida e o X)
    for j in range(2):
        g, h = clarao(T, t, 0.62 + 0.1 * j, 0.72 + 0.1 * j, 0.45, 0.0, 0.6 + 0.6 * j, 1.0)
        G, H = G + g, H + h
        G += anel(T, t, 0.62 + 0.1 * j, 0.95, 0.05, 0.45, 0.03, 0.0)
    m = surge(t, 0.75, 0.88) * (1 - rel(t, 0.92, 1))
    if m > 0:
        G += T.lines([(0.45 - 0.13 * m, -0.13 * m, 0.45 + 0.13 * m, 0.13 * m, 1.0), (0.45 + 0.13 * m, -0.13 * m, 0.45 - 0.13 * m, 0.13 * m, 1.0)], 0.022) * 1.4
    return G * env, H * env


REGISTRO = [
    ("auto_9", auto_9, GRANDE, "RoboCop · a Auto-9 e a mira do visor", False),
    ("proteger_o_inocente", proteger_o_inocente, GRANDE, "RoboCop · as diretrizes e o escudo", False),
    ("robocop_preparo", robocop_preparo, MEDIA, "RoboCop · o visor varrendo (Preparo, laço)", True),
    ("vivo_ou_morto", vivo_ou_morto, GRANDE, "RoboCop · a mira travando e a rajada", False),
    ("flecha_explosiva_rambo", flecha_explosiva_rambo, GRANDE, "Rambo · a flecha com a ponta piscando", False),
    ("faca_de_sobrevivencia", faca_de_sobrevivencia, GRANDE, "Rambo · a faca serrilhada girando", False),
    ("rambo_preparo", rambo_preparo, MEDIA, "Rambo · a faixa e os olhos no mato (Preparo, laço)", True),
    ("emboscada_na_selva", emboscada_na_selva, GRANDE, "Rambo · as armadilhas e as folhas", False),
    ("chicotada", chicotada, GRANDE, "Indiana Jones · o chicote enrolando", False),
    ("pedra_rolando", pedra_rolando, GRANDE, "Indiana Jones · a pedra gigante rolando", False),
    ("indy_preparo", indy_preparo, MEDIA, "Indiana Jones · o chapéu e o ídolo (Preparo, laço)", True),
    ("reliquia", reliquia, GRANDE, "Indiana Jones · o ídolo e a luz no trio", False),
    ("bussola_magica", bussola_magica, GRANDE, "Jack Sparrow · a bússola apontando", False),
    ("pistola_de_um_tiro", pistola_de_um_tiro, GRANDE, "Jack Sparrow · a pistola de um tiro", False),
    ("sparrow_preparo", sparrow_preparo, MEDIA, "Jack Sparrow · o chapéu e o vento (Preparo, laço)", True),
    ("perola_negra", perola_negra, GRANDE, "Jack Sparrow · o navio e os canhões", False),
    ("expelliarmus_harry", expelliarmus_harry, GRANDE, "Harry Potter · o raio vermelho e os buffs voando", False),
    ("protego", protego, GRANDE, "Harry Potter · os escudos transparentes", False),
    ("harry_preparo", harry_preparo, MEDIA, "Harry Potter · a varinha e a névoa prateada (Preparo, laço)", True),
    ("expecto_patronum", expecto_patronum, GRANDE, "Harry Potter · o cervo prateado", False),
    ("crucio", crucio, GRANDE, "Voldemort · o raio de dor", False),
    ("imperius", imperius, GRANDE, "Voldemort · os fios de marionete", False),
    ("voldemort_preparo", voldemort_preparo, MEDIA, "Voldemort · a varinha e a Marca Negra (Preparo, laço)", True),
    ("avada_kedavra", avada_kedavra, GRANDE, "Voldemort · o raio verde da morte", False),
    ("mu_pagina_no_relogio", pagina_no_relogio, GRANDE, "Light · a página escondida no relógio (Mecânica única)", False),
]
