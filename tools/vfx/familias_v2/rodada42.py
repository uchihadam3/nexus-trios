"""Rodada 42 das habilidades próprias: Zoro, Nami, Sanji, Chopper, Nero e L.

Roronoa Zoro
- oni_giri: as três espadas cruzando juntas no rival, em três riscos (Sangrando).
- tatsumaki_zoro: o tornado de cortes subindo e pegando todos os rivais.
- zoro_preparo: o Preparo do Asura — as três espadas (uma na boca) e a sombra de três cabeças surgindo (laço).
- asura: os nove cortes do demônio de três cabeças e seis braços, de uma vez (Sangrando).

Nami
- bola_de_trovao: a bolinha de nuvem negra soltando o raio no rival (Eletrificado).
- miragem: o ar tremendo e as cópias da Nami se espalhando (Confuso).
- nami_preparo: o Preparo do Tempo do trovão — o bastão girando as bolhas de clima (laço).
- tempo_do_trovao: a nuvem negra no alto e os raios caindo em todos (Eletrificado).

Sanji
- concasser: o chute de cima para baixo como um machado (Exposto).
- diable_jambe: a perna em brasa girando e o chute pegando fogo (Queimando).
- sanji_preparo: o Preparo do Hell Memories — o cigarro aceso e a chama crescendo na perna (laço).
- hell_memories: a explosão de chamas do inferno em todos os rivais (Queimando).

Tony Tony Chopper
- tratamento_de_campo: a maleta, a cruz de médico e a cura com o curativo (Vida e Purificar).
- rumble_ball: a pílula Rumble Ball e o corpo inchando de força (Fortalecido e Protegido).
- chopper_preparo: o Preparo do Monster Point — a Rumble Ball pulsando, o corpo crescendo (laço).
- monster_point: o Chopper gigante e o soco enorme no rival.

Nero
- red_queen: a espada com o acelerador soltando chamas no corte (Exposto).
- devil_bringer: o braço fantasma azul agarrando e puxando o rival (Preso).
- nero_preparo: o Preparo do Showdown — a Red Queen roncando e soltando fogo (laço).
- showdown: a sequência de cortes e tiros da Blue Rose e o último corte enorme.

L
- investigacao: a lupa passando sobre o rival e as pistas ligadas por fios (Marcado e Exposto).
- armadilha_logica: o tabuleiro de lógica se fechando em volta do rival em Preparo (Atrasa e Confuso).
- l_preparo: o Preparo do Caso resolvido — a torre de cubos de açúcar crescendo (laço).
- caso_resolvido: todas as pistas convergindo e o carimbo de "resolvido" no rival (Enfraquecido).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, CRUZ, ESPADA, anel, aura, cheio, circulo, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


def _nuvem(T, cx, cy, s, k):
    G = 0.0
    for dx, dy, r in ((-0.5, 0.1, 0.45), (0.0, -0.1, 0.6), (0.5, 0.1, 0.45), (0.2, 0.15, 0.4), (-0.25, 0.15, 0.4)):
        G = G + T.gauss(cx + dx * s, cy + dy * s, r * s) * k * 0.6
    return G


# ------------------------------------------------------------------ Zoro

def oni_giri(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, ang in enumerate((-0.35, 0.0, 0.35)):
        g, h = corte(T, t, 0.08 + 0.02 * j, 0.38 + 0.02 * j, ang, 1.5, 0.07, 0.15, 0.0)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.35, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for j, ang in enumerate((-0.35, 0.0, 0.35)):
            G += T.lines([(0.35 - 0.3 * math.cos(ang), -0.3 * math.sin(ang), 0.35 + 0.3 * math.cos(ang), 0.3 * math.sin(ang), 1.0)], 0.012) * s * 1.2
    G += estouro(T, t, 0.32, 0.8, 12, 4, 0.35, 0.0, 0.45, 0.012)
    return G * env, H * env


def tatsumaki_zoro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.8)
    for m in range(10):
        v = m / 9
        y = 0.35 - 0.8 * v
        r = 0.2 + 0.6 * v
        a = t * 25 + m * 0.7
        G += T.arc_band(r, 0.022, a, a + 2.2, 0.3, 0, 0.0, y, 1.0) * k * 1.2
    for x in (-0.55, 0.0, 0.55):
        for j in range(2):
            g, h = corte(T, t, 0.2 + 0.15 * j, 0.4 + 0.15 * j, 0.8 * (1 if j else -1), 0.45, 0.04, x, -0.05)
            G, H = G + g, H + h
    G += particulas(T, t, 0.2, 0.9, 20, 4, 0, 0.0, 0.8, 0.8, 0.011)
    return G * env, H * env


def zoro_preparo(T, t, rng):
    G, H = vazio(T)
    for j, a in enumerate((-0.5, 0.0, 0.5)):
        g, h = icone(T, poe(ESPADA, 0.15 * math.sin(a), -0.05, 0.35, a), 1.0, 0.5)
        G, H = G + g, H + h
    b = 0.5 + 0.5 * math.sin(t * TAU * 1.5)
    for lado in (-1, 0, 1):
        G += T.gauss(lado * 0.28, -0.35 + 0.05 * abs(lado), 0.08) * (0.25 + 0.25 * b)
    H += T.gauss(0, -0.4, 0.02) * (1.2 + b)
    return G, H


def asura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        for lado in (-1, 0, 1):
            G += T.gauss(-0.35 + lado * 0.25, -0.35 + 0.05 * abs(lado), 0.12 * s) * 0.7
            H += T.gauss(-0.35 + lado * 0.25, -0.38, 0.015) * s * 1.6
        for lado in (-1, 1):
            for m in range(3):
                a = math.pi / 2 + lado * (0.6 + 0.4 * m)
                G += T.lines([(-0.35, 0.0, -0.35 + 0.4 * s * math.cos(a) * -1, 0.4 * s * math.sin(a) * -1, 1.0)], 0.02) * 1.0
    for j in range(9):
        ang = -1.2 + 0.3 * j
        a0 = 0.35 + 0.015 * j
        g, h = corte(T, t, a0, a0 + 0.22, ang, 1.4, 0.06, 0.4, 0.0)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.45, 0.7, 0.4, 0.0, 1.6, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.5, 0.95, 0.1, 0.7, 0.045, 0.0)
    G += estouro(T, t, 0.5, 0.95, 18, 6, 0.4, 0.0, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Nami

def bola_de_trovao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.8, 0.95)
    x = -0.5 + 1.0 * u
    G += _nuvem(T, x, -0.45, 0.15, k)
    kk = pulso(t, 0.35, 0.7)
    if kk > 0:
        g, h = _raio(T, t, 0.5, -0.4, 0.5, 0.05, kk, 0.022, 2)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.38, 0.6, 0.5, 0.05, 1.0)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.4, 0.75, 5, 3, 0.5, 0.05, 0.3, 0.009)
    return G * env, H * env


def miragem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.9)
    for m in range(5):
        y = -0.4 + 0.18 * m
        pts = [(-0.85 + 1.7 * v, y + 0.02 * math.sin(v * 20 + t * 15 + m)) for v in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.006) * k * 0.9
    espalha = ease_out(rel(t, 0.1, 0.6), 2)
    for j, x in enumerate((-0.6, -0.3, 0.3, 0.6)):
        xx = 0.0 + x * espalha
        G += T.gauss(xx, 0.0, 0.06, 0.16) * k * 0.5 * (0.6 + 0.4 * math.sin(t * 9 + j))
    for x in (-0.55, 0.0, 0.55):
        for j in range(3):
            ang = t * 9 + TAU * j / 3
            g, h = cheio(T, poe(estrela_pts(5, 0.45), x + 0.1 * math.cos(ang), -0.3 + 0.04 * math.sin(ang), 0.03), pulso(t, 0.45, 1.0) * 1.3)
            G, H = G + g, H + h
    return G * env, H * env


def nami_preparo(T, t, rng):
    G, H = vazio(T)
    a = t * TAU
    G += T.lines([(-0.3 * math.cos(a), -0.3 * math.sin(a) * 0.4, 0.3 * math.cos(a), 0.3 * math.sin(a) * 0.4, 1.0)], 0.02) * 1.1
    for j in range(3):
        b = a * 1.5 + TAU * j / 3
        cx, cy = 0.22 * math.cos(b), -0.1 + 0.15 * math.sin(b)
        G += T.ring(0.04, 0.01, cx, cy) * 1.2 + T.gauss(cx, cy, 0.03) * 0.8
    G += _nuvem(T, 0, -0.35, 0.1, 0.6 + 0.3 * math.sin(t * 8))
    return G, H


def tempo_do_trovao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    G += _nuvem(T, 0.0, -0.6, 0.5 * s + 0.01, 0.45 if s > 0 else 0)
    G += T.gauss(0.0, -0.45, 0.6 * s + 0.01, 0.04) * 0.6 * (1 if s > 0 else 0)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        kk = pulso(t, 0.35 + 0.08 * j, 0.6 + 0.08 * j)
        if kk > 0:
            g, h = _raio(T, t, x + 0.08, -0.55, x, 0.05, kk, 0.022, j)
            G, H = G + g, H + h
        g2, h2 = clarao(T, t, 0.4 + 0.08 * j, 0.6 + 0.08 * j, x, 0.05, 0.7)
        G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.4, 0.9, 1.0, 0.35, 1.2)
    return G * env, H * env


# ------------------------------------------------------------------ Sanji

def _perna(T, x0, y0, x1, y1, k, w=0.05):
    G = T.lines([(x0, y0, x1, y1, 1.0)], w) * k * 1.0
    G = G + T.gauss(x1, y1, w * 1.2) * k * 1.2
    return G


def concasser(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.32), 2.2)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        a = -math.pi / 2 - 0.3 + 1.5 * u
        x1, y1 = 0.3 + 0.55 * math.cos(a) * 0.6, -0.15 + 0.55 * math.sin(a)
        G += _perna(T, 0.3 - 0.25, -0.15 + 0.2, x1, y1, k, 0.06)
        if u < 1:
            G += T.arc_band(0.55, 0.06, a - 0.9, a, 0.6, 0, 0.3, -0.15, 1.0) * k * 0.6
    g, h = clarao(T, t, 0.3, 0.52, 0.45, 0.2, 1.3, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.8, 0.7, 0.35, 1.5)
    G += estouro(T, t, 0.32, 0.8, 14, 4, 0.45, 0.2, 0.5, 0.014)
    return G * env, H * env


def diable_jambe(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.55)
    if k > 0:
        a = t * 22
        x1, y1 = -0.2 + 0.55 * math.cos(a), 0.55 * math.sin(a) * 0.6
        G += _perna(T, -0.2, 0.0, x1, y1, k, 0.08)
        for j in range(5):
            b = a - 0.25 * j
            g, h = icone(T, poe(CHAMA, -0.2 + 0.55 * math.cos(b), 0.33 * math.sin(b), 0.12 * (1 - 0.15 * j), b + math.pi / 2), k * (1 - 0.15 * j), 0.6)
            G, H = G + g, H + h * 1.4
    u = ease_in(rel(t, 0.5, 0.65), 2)
    if 0 < u < 1:
        G += _perna(T, -0.2, 0.0, -0.2 + 0.7 * u, 0.0, 1.0, 0.06)
    g2, h2 = clarao(T, t, 0.62, 0.8, 0.5, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    for m in range(4):
        kk = pulso(t, 0.65, 1.0)
        g3, h3 = icone(T, poe(CHAMA, 0.4 + 0.07 * m, 0.05, 0.07 * kk), kk, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def sanji_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.05, -0.3, 0.1, -0.28, 1.0)], 0.012) * 1.1
    H += T.gauss(0.11, -0.28, 0.012) * (1.5 + math.sin(t * 20))
    for j in range(2):
        u = ((t * 1.5) + j / 2) % 1
        G += T.gauss(0.13 + 0.03 * math.sin(u * 8), -0.3 - 0.2 * u, 0.02 + 0.02 * u) * (1 - u) * 0.6
    tremula = 0.8 + 0.2 * math.sin(t * 25)
    G += T.lines([(-0.1, 0.0, 0.1, 0.4, 1.0)], 0.05) * 0.9
    for j in range(4):
        v = j / 3
        g, h = icone(T, poe(CHAMA, -0.1 + 0.2 * v, 0.4 * v - 0.03, 0.06 * tremula), 1.0, 0.6)
        G, H = G + g, H + h * 1.4
    return G, H


def hell_memories(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.3, 14, 3, -0.5, 0.0, 0.4)
    g, h = clarao(T, t, 0.3, 0.55, 0.0, 0.05, 1.8, 1.6)
    G, H = G + g, H + h
    q = np.random.default_rng(5)
    for j in range(22):
        x = q.uniform(-0.85, 0.85)
        a0 = 0.32 + 0.3 * abs(x) / 0.85
        kk = pulso(t, a0, min(1.0, a0 + 0.5))
        if kk > 0:
            g2, h2 = icone(T, poe(CHAMA, x, 0.3 - 0.3 * q.uniform(0, 1) * kk, 0.06 + 0.1 * kk * q.uniform(0.6, 1)), kk * 1.1, 0.6)
            G, H = G + g2, H + h2 * 1.3
    G += anel(T, t, 0.32, 0.85, 0.1, 1.0, 0.05, 0.05)
    G += onda_no_chao(T, t, 0.32, 0.9, 1.0, 0.35, 1.6)
    return G * env, H * env


# ------------------------------------------------------------------ Chopper

def tratamento_de_campo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        g, h = icone(T, [(-0.62, -0.05), (-0.32, -0.05), (-0.32, 0.15), (-0.62, 0.15)], s * 1.1, 0.45)
        G, H = G + g, H + h
        G += T.arc_band(0.06, 0.015, math.pi, TAU, 1.0, 0, -0.47, -0.05, 0.0) * s * 1.2
        g2, h2 = cheio(T, poe(CRUZ, -0.47, 0.05, 0.05 * s), 1.3)
        G, H = G + g2, H + h2
    m = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g3, h3 = icone(T, poe(CRUZ, 0.4, -0.25, 0.12 * m, 0.1), 1.3, 0.5)
        G, H = G + g3, H + h3
        G += T.lines([(0.3, 0.05, 0.5, 0.15, 1.0)], 0.03) * m * 1.0
    g4, h4 = aura(T, t, 0.4, 1.0, 0.3, 0.05, 0.8)
    G += anel(T, t, 0.45, 0.9, 0.1, 0.5, 0.03, 0.05)
    return (G + g4) * env, (H + h4) * env


def _pilula(T, cx, cy, s, ang, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(cx - s * c, cy - s * sn, cx + s * c, cy + s * sn, 1.0)], s * 0.9) * k * 1.0
    G = G + T.lines([(cx - 0.05 * s * sn, cy + 0.05 * s * c, cx + 0.05 * s * sn, cy - 0.05 * s * c, 1.0)], s * 0.95) * k * 0.4
    return G


def rumble_ball(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        G += _pilula(T, -0.3 + 0.3 * u, -0.5 + 0.35 * u - 0.2 * math.sin(math.pi * u), 0.06, u * 6, 1.0)
    cresce = ease_out(rel(t, 0.3, 0.6), 2)
    k = 1 - rel(t, 0.85, 1)
    if cresce > 0:
        r = 0.12 + 0.18 * cresce
        G += T.gauss(0, 0.05, r, r * 1.1) * k * 0.6
        G += T.ring(r * 1.1, 0.025, 0, 0.05, 0.9) * k * 1.2
        for lado in (-1, 1):
            G += T.gauss(lado * r * 0.9, 0.0, r * 0.35) * k * 0.6
    g, h = clarao(T, t, 0.3, 0.48, 0, 0.0, 0.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.4, 0.9, 0.1, 0.65, 0.035, 0.05)
    return G * env, H * env


def chopper_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2.5)
    G += _pilula(T, 0, -0.3, 0.06, t * 3, 1.0 + 0.3 * b)
    H += T.gauss(0, -0.3, 0.03) * (1 + b)
    r = 0.12 + 0.05 * b
    G += T.gauss(0, 0.1, r, r * 1.1) * 0.7
    G += T.ring(r * 1.15, 0.018, 0, 0.1) * 1.0
    return G, H


def monster_point(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.6, 0.75))
    if s > 0:
        G += T.gauss(-0.4, -0.15, 0.25 * s, 0.4 * s) * 0.6
        for lado in (-1, 1):
            chifre = [(-0.4 + lado * 0.1 * s, -0.5 * s - 0.1), (-0.4 + lado * 0.3 * s, -0.9 * s - 0.05), (-0.4 + lado * 0.18 * s, -0.5 * s - 0.1)]
            G += T.polyline(chifre, 0.025) * 1.2
    u = ease_in(rel(t, 0.25, 0.45), 2)
    k = 1 - rel(t, 0.6, 0.72)
    if 0 < u and k > 0:
        P, nos = _punho(T, -0.3 + 0.75 * u, 0.0, 3.6, 0)
        G += P * 0.95 * k
        H += nos * 0.5 * k
    g, h = clarao(T, t, 0.42, 0.62, 0.5, 0.0, 1.6, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.42, 0.9, 0.9, 0.35, 1.6)
    G += estouro(T, t, 0.42, 0.92, 18, 5, 0.5, 0.0, 0.7, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Nero

def red_queen(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = corte(T, t, 0.15, 0.45, -0.6, 1.6, 0.11, 0.3, 0.0, 0.1)
    G, H = G + g * 1.3, H + h
    for j in range(6):
        v = rel(t, 0.12 + 0.03 * j, 0.6)
        if 0 < v < 1:
            x = -0.5 + 1.2 * v
            g2, h2 = icone(T, poe(CHAMA, x, 0.15 - 0.4 * v + 0.05 * j, 0.06 * (1 - v) + 0.01, math.pi * 0.8), (1 - v) * 1.2, 0.6)
            G, H = G + g2, H + h2 * 1.4
    g3, h3 = clarao(T, t, 0.35, 0.55, 0.4, 0.0, 1.1, 1.2)
    G, H = G + g3, H + h3
    return G * env, H * env


def devil_bringer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    volta = ease_in(rel(t, 0.4, 0.7), 1.6)
    alc = vai * (1 - 0.6 * volta)
    if alc > 0.02:
        x0, x1 = -0.6, -0.6 + 1.15 * alc
        G += T.lines([(x0, 0.0, x1, 0.0, 1.0)], 0.12) * 0.7
        G += T.gauss(x1, 0.0, 0.17) * 0.9
        for m in range(4):
            a = -0.7 + 0.45 * m
            G += T.lines([(x1, 0.0, x1 + 0.24 * math.cos(a), 0.24 * math.sin(a), 1.0)], 0.045) * 1.1
        H += T.lines([(x0, 0.0, x1, 0.0, 1.0)], 0.012) * 1.0
    if volta > 0:
        G += T.gauss(0.55 - 0.69 * volta, 0.0, 0.1, 0.18) * (1 - rel(t, 0.7, 0.8)) * 0.8
    g, h = clarao(T, t, 0.28, 0.45, 0.55, 0.0, 0.8)
    return (G + g) * env, (H + h) * env


def nero_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(ESPADA, 0, 0.0, 0.42, 0.4), 1.1, 0.5)
    G, H = G + g, H + h
    ronco = 0.8 + 0.2 * math.sin(t * 40)
    for j in range(3):
        g2, h2 = icone(T, poe(CHAMA, -0.1 + 0.05 * j, 0.25, 0.05 * ronco, math.pi * 0.9), 1.1, 0.6)
        G, H = G + g2, H + h2 * 1.4
    G += T.gauss(-0.05, 0.25, 0.1) * (0.5 + 0.3 * math.sin(t * 40))
    return G, H


def showdown(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(7)
    for j in range(6):
        a0 = 0.03 + 0.07 * j
        if j % 2 == 0:
            g, h = corte(T, t, a0, a0 + 0.15, q.uniform(-1.0, 1.0), 1.0, 0.06, 0.4, 0.0)
            G, H = G + g, H + h
        else:
            k = pulso(t, a0, a0 + 0.1)
            if k > 0:
                G += T.tapered([(-0.6, -0.05 * j, 0.4, 0.0, 1.0)], 0.02) * k * 1.3
                H += T.gauss(-0.6, -0.05 * j, 0.03) * k * 2
        g2, h2 = clarao(T, t, a0 + 0.06, a0 + 0.14, 0.4, 0.0, 0.5)
        G, H = G + g2, H + h2
    g3, h3 = corte(T, t, 0.5, 0.75, -0.7, 1.9, 0.14, 0.4, 0.0, 0.15)
    G, H = G + g3 * 1.3, H + h3
    g4, h4 = clarao(T, t, 0.6, 0.82, 0.4, 0.0, 1.6, 1.5)
    G, H = G + g4, H + h4
    G += estouro(T, t, 0.62, 0.98, 18, 6, 0.4, 0.0, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ L

def _lupa(T, cx, cy, s, k):
    G = T.ring(s, s * 0.15, cx, cy) * k * 1.3
    G = G + T.lines([(cx + s * 0.7, cy + s * 0.7, cx + s * 1.6, cy + s * 1.6, 1.0)], s * 0.22) * k * 1.2
    G = G + T.gauss(cx, cy, s * 0.7) * k * 0.3
    return G, T.gauss(cx - s * 0.35, cy - s * 0.35, s * 0.15) * k * 1.6


def investigacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.5), 1.5)
    k = 1 - rel(t, 0.75, 0.9)
    g, h = _lupa(T, -0.4 + 0.85 * u, -0.15 + 0.08 * math.sin(u * 8), 0.2, k)
    G, H = G + g, H + h
    pistas = [(0.25, -0.35), (0.65, -0.3), (0.3, 0.2), (0.7, 0.15)]
    for j, (x, y) in enumerate(pistas):
        s = surge(t, 0.4 + 0.06 * j, 0.6 + 0.06 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            G += T.ring(0.03 * s, 0.01, x, y) * 1.2
            H += T.gauss(x, y, 0.012) * s * 1.5
            G += T.lines([(x, y, 0.45, -0.05, 1.0)], 0.006) * s * 1.0
    m = surge(t, 0.6, 0.8) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.13 * m, 0.016, 0.45, -0.05) * 1.3
    return G * env, H * env


def armadilha_logica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.0, 0.5), 1.6)
    k = 1 - rel(t, 0.85, 1)
    r = 0.6 - 0.35 * fecha
    linhas = []
    for m in range(5):
        x = 0.45 - r + 2 * r * m / 4
        y = -r * 0.6 + 2 * r * 0.6 * m / 4
        linhas += [(x, -r * 0.6, x, r * 0.6, 1.0), (0.45 - r, y, 0.45 + r, y, 1.0)]
    G += T.lines(linhas, 0.008) * k * 1.2
    cel = int(t * 12) % 16
    cx, cy = 0.45 - r + 2 * r * ((cel % 4) + 0.5) / 4, -r * 0.6 + 2 * r * 0.6 * ((cel // 4) + 0.5) / 4
    G += T.gauss(cx, cy, r * 0.18, r * 0.12) * k * 0.9
    m = surge(t, 0.5, 0.7) * k
    if m > 0:
        pts = [(0.45 + x * 0.45 * m, -0.05 + (y + 0.45) * 0.45 * m) for x, y in
               [(-0.12, -0.5), (-0.06, -0.62), (0.06, -0.64), (0.14, -0.56), (0.13, -0.46), (0.03, -0.38), (0.02, -0.28)]]
        G += T.polyline(pts, 0.018) * 1.3
    return G * env, H * env


def l_preparo(T, t, rng):
    G, H = vazio(T)
    n = 1 + int((t * 5) % 6)
    for j in range(n):
        y = 0.32 - 0.15 * j
        x = 0.025 * math.sin(j * 1.7)
        g, h = icone(T, [(x - 0.07, y - 0.07), (x + 0.07, y - 0.07), (x + 0.07, y + 0.07), (x - 0.07, y + 0.07)], 1.0, 0.5)
        G, H = G + g, H + h
    G += T.lines([(-0.25, 0.37, 0.25, 0.37, 1.0)], 0.01) * 0.9
    return G, H


def caso_resolvido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(4)
    for j in range(8):
        a = TAU * j / 8 + 0.2
        x0, y0 = 0.45 + 0.8 * math.cos(a), 0.6 * math.sin(a)
        u = ease_in(rel(t, 0.05 + 0.02 * j, 0.45 + 0.02 * j), 1.5)
        if 0 < u < 1:
            x, y = x0 + (0.45 - x0) * u, y0 * (1 - u)
            G += T.lines([(x0, y0, x, y, 1.0)], 0.006) * 1.0
            G += T.ring(0.025, 0.008, x, y) * 1.2
    g, h = clarao(T, t, 0.42, 0.62, 0.45, 0.0, 1.5, 1.5)
    G, H = G + g, H + h
    s = surge(t, 0.5, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.22 * s, 0.03, 0.45, 0.0) * 1.3
        G += T.polyline([(0.33, 0.0), (0.42, 0.1), (0.6, -0.12)], 0.035 * s + 0.002) * 1.4
    G += estouro(T, t, 0.45, 0.95, 14, 5, 0.45, 0.0, 0.55, 0.012)
    return G * env, H * env


REGISTRO = [
    ("oni_giri", oni_giri, GRANDE, "Zoro · as três espadas cruzando", False),
    ("tatsumaki_zoro", tatsumaki_zoro, GRANDE, "Zoro · o tornado de cortes", False),
    ("zoro_preparo", zoro_preparo, MEDIA, "Zoro · as três espadas e a sombra (Preparo, laço)", True),
    ("asura", asura, GRANDE, "Zoro · os nove cortes do demônio", False),
    ("bola_de_trovao", bola_de_trovao, GRANDE, "Nami · a nuvem soltando o raio", False),
    ("miragem", miragem, GRANDE, "Nami · o ar tremendo e as cópias", False),
    ("nami_preparo", nami_preparo, MEDIA, "Nami · o bastão girando as bolhas (Preparo, laço)", True),
    ("tempo_do_trovao", tempo_do_trovao, GRANDE, "Nami · a nuvem negra e os raios em todos", False),
    ("concasser", concasser, GRANDE, "Sanji · o chute como machado", False),
    ("diable_jambe", diable_jambe, GRANDE, "Sanji · a perna em brasa girando", False),
    ("sanji_preparo", sanji_preparo, MEDIA, "Sanji · o cigarro e a perna pegando fogo (Preparo, laço)", True),
    ("hell_memories", hell_memories, GRANDE, "Sanji · as chamas do inferno em todos", False),
    ("tratamento_de_campo", tratamento_de_campo, GRANDE, "Chopper · a maleta e a cruz de médico", False),
    ("rumble_ball", rumble_ball, GRANDE, "Chopper · a pílula e o corpo inchando", False),
    ("chopper_preparo", chopper_preparo, MEDIA, "Chopper · a Rumble Ball pulsando (Preparo, laço)", True),
    ("monster_point", monster_point, GRANDE, "Chopper · o monstro e o soco enorme", False),
    ("red_queen", red_queen, GRANDE, "Nero · o corte com as chamas do acelerador", False),
    ("devil_bringer", devil_bringer, GRANDE, "Nero · o braço fantasma agarrando", False),
    ("nero_preparo", nero_preparo, MEDIA, "Nero · a Red Queen roncando (Preparo, laço)", True),
    ("showdown", showdown, GRANDE, "Nero · os cortes, os tiros e o golpe final", False),
    ("investigacao", investigacao, GRANDE, "L · a lupa e as pistas", False),
    ("armadilha_logica", armadilha_logica, GRANDE, "L · o tabuleiro se fechando", False),
    ("l_preparo", l_preparo, MEDIA, "L · a torre de cubos de açúcar (Preparo, laço)", True),
    ("caso_resolvido", caso_resolvido, GRANDE, "L · as pistas convergindo e o visto", False),
]
