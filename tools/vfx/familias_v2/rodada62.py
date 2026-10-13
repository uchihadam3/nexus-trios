"""Rodada 62 das habilidades próprias: Creeper, Pac-Man, Crash, Arthur Morgan, Ellie e Sans.

Creeper
- chiado_creeper: o "sssss" (as ondas verdes) e a marca de explosão piscando no rival (Marca explosiva).
- camuflagem_verde: o corpo de pixels verdes sumindo no mato (Esquiva).
- creeper_preparo: o Preparo da Explosão — o Creeper inchando e piscando branco (laço).
- explosao_creeper: a explosão de pixels em todos os rivais e a cratera (o Creeper também se machuca).

Pac-Man
- comer_pacman: a boca amarela abrindo e fechando ("waka-waka") mordendo o rival e a vida voltando (Roubo de vida).
- pilula_de_poder: a pílula de poder grande piscando e o Pac-Man crescendo (Fortalecido e Acelerado).
- pacman_preparo: o Preparo do Comer fantasma — o labirinto e as bolinhas sendo comidas (laço).
- comer_fantasma: o fantasma azul assustado e o Pac-Man engolindo (dissipa buffs).

Crash
- giro_crash: o redemoinho do giro do Crash batendo em todos os rivais.
- aku_aku_mascara: a máscara Aku Aku flutuando e as penas em volta (Escudo e Protegido).
- caixa_de_nitro: a caixa verde de Nitro voando e explodindo no rival (Marca explosiva).

Arthur Morgan
- dead_eye_arthur: a tela ficando sépia e os X vermelhos marcados no rival (Marcado e Exposto).
- laco_arthur: o laço girando no ar e prendendo o rival (Preso).
- arthur_preparo: o Preparo do Revólver — o cão do revólver armando e o chapéu (laço).
- revolver_arthur: os tiros em sequência do revólver no rival.

Ellie
- canivete_ellie: o canivete cortando rápido e o sangue (Sangrando).
- furtividade_ellie: agachada no mato, a silhueta sumindo e a audição (Esquiva e Acelerado).
- ellie_preparo: o Preparo do Arco silencioso — o arco puxado mirando (laço).
- arco_silencioso: a flecha silenciosa voando e acertando o rival.

Sans
- ossos_sans: as fileiras de ossos subindo do chão e passando pelo rival (Amaldiçoado).
- desviar_sans: o Sans deslizando para o lado, sorrindo, e o golpe passando (Esquiva).
- sans_preparo: o Preparo do Gaster Blaster — o olho azul brilhando e o caveirão aparecendo (laço).
- gaster_blaster: as caveiras de dragão abrindo a boca e o raio em todos os rivais (Amaldiçoado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CRUZ, PENA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _quad(T, x, y, s, k, cheio=0.6):
    return icone(T, [(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)], k, cheio)


def _creeper(T, x, y, s, k, incha=0.0):
    """O rosto do Creeper em pixels: os dois olhos quadrados e a boca em degrau."""
    s2 = s * (1 + 0.25 * incha)
    G, H = _quad(T, x, y, s2, k, 0.35)
    for lado in (-1, 1):
        g, h = _quad(T, x + lado * s2 * 0.45, y - s2 * 0.35, s2 * 0.18, k * 1.2, 1.0)
        G, H = G + g, H + h
    boca = [(x - s2 * 0.12, y - s2 * 0.1), (x + s2 * 0.12, y - s2 * 0.1), (x + s2 * 0.12, y + s2 * 0.15), (x + s2 * 0.3, y + s2 * 0.15),
            (x + s2 * 0.3, y + s2 * 0.6), (x + s2 * 0.12, y + s2 * 0.6), (x + s2 * 0.12, y + s2 * 0.4), (x - s2 * 0.12, y + s2 * 0.4),
            (x - s2 * 0.12, y + s2 * 0.6), (x - s2 * 0.3, y + s2 * 0.6), (x - s2 * 0.3, y + s2 * 0.15), (x - s2 * 0.12, y + s2 * 0.15)]
    g, h = icone(T, boca, k * 1.2, 1.0)
    return G + g, H + h


def _pacman(T, x, y, s, boca, ang, k):
    """O Pac-Man: o círculo amarelo com a boca em cunha (boca = abertura em radianos)."""
    pts = [(x, y)] + [(x + s * math.cos(a + ang), y + s * math.sin(a + ang)) for a in np.linspace(boca / 2, TAU - boca / 2, 30)]
    return icone(T, pts, k * 1.2, 0.75)


def _fantasma(T, x, y, s, k, assustado=True):
    pts = [(x - s, y + s * 0.8)] + [(x + s * math.cos(a), y - s * 0.1 + s * math.sin(a)) for a in np.linspace(math.pi, TAU, 14)] + [(x + s, y + s * 0.8)]
    for j in range(4):
        xx = x + s - s * 0.5 * (j + 0.5)
        pts.append((xx, y + s * (0.55 if j % 2 == 0 else 0.8)))
    g, h = icone(T, pts, k * 1.1, 0.5)
    G = g
    for lado in (-1, 1):
        G += T.gauss(x + lado * s * 0.35, y - s * 0.15, s * 0.1) * k * 1.4
    if assustado:
        G += T.polyline([(x - s * 0.6, y + s * 0.35), (x - s * 0.3, y + s * 0.2), (x, y + s * 0.35), (x + s * 0.3, y + s * 0.2), (x + s * 0.6, y + s * 0.35)], s * 0.08) * k
    return G, h


def _mascara(T, x, y, s, k):
    """A máscara Aku Aku: o rosto de madeira comprido, os olhos e as penas no alto."""
    pts = [(-0.5, -0.9), (0.5, -0.9), (0.6, 0.2), (0.35, 0.95), (-0.35, 0.95), (-0.6, 0.2)]
    g, h = icone(T, poe(pts, x, y, s), k * 1.1, 0.45)
    G, H = g, h
    for lado in (-1, 1):
        G += T.ring(s * 0.15, s * 0.05, x + lado * s * 0.25, y - s * 0.35) * k * 1.2
        H += T.gauss(x + lado * s * 0.25, y - s * 0.35, s * 0.06) * k * 1.6
    G += T.lines([(x - s * 0.3, y + s * 0.45, x + s * 0.3, y + s * 0.45, 1.0)], s * 0.08) * k
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.35
        g, h = icone(T, poe(PENA, x + s * 0.9 * math.cos(a), y - s * 0.7 + s * 0.9 * math.sin(a) * 0.6, s * 0.35, a + math.pi / 2), k, 0.6)
        G, H = G + g, H + h
    return G, H


def _caixa_nitro(T, x, y, s, k, ang=0.0):
    pts = poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], x, y, s, ang)
    g, h = icone(T, pts, k * 1.2, 0.5)
    c, sn = math.cos(ang), math.sin(ang)
    G = g + T.lines([(x - s * c, y - s * sn, x + s * c, y + s * sn, 1.0)], s * 0.12) * k
    G += T.lines([(x - s * c * 0.6 + s * sn * 0.4, y - s * sn * 0.6 - s * c * 0.4, x + s * c * 0.6 + s * sn * 0.4, y + s * sn * 0.6 - s * c * 0.4, 1.0)], s * 0.08) * k * 0.8
    return G, h + T.gauss(x, y, s * 0.4) * k * 0.8


def _x_marca(T, x, y, s, k):
    return T.lines([(x - s, y - s, x + s, y + s, 1.0), (x - s, y + s, x + s, y - s, 1.0)], s * 0.25) * k * 1.4


def _revolver(T, x, y, s, k):
    pts = [(-0.4, -0.12), (0.8, -0.12), (0.8, 0.0), (0.1, 0.05), (0.0, 0.2), (-0.1, 0.55), (-0.4, 0.5), (-0.3, 0.05)]
    g, h = icone(T, poe(pts, x, y, s), k * 1.2, 0.6)
    return g + T.ring(s * 0.13, s * 0.04, x + s * 0.05, y - s * 0.02) * k * 1.2, h


def _arco(T, x, y, s, puxa, k):
    G = T.arc_band(s, s * 0.05, -1.2, 1.2, 1.0, 0, x - s * 0.6, y, 0.0) * k * 1.3
    ty, by = y - s * math.sin(1.2), y + s * math.sin(1.2)
    tx = x - s * 0.6 + s * math.cos(1.2)
    px = tx - s * 0.5 * puxa
    return G + T.lines([(tx, ty, px, y, 1.0), (px, y, tx, by, 1.0)], s * 0.022) * k


def _osso(T, x0, y0, x1, y1, w, k):
    G = T.lines([(x0, y0, x1, y1, 1.0)], w) * k * 1.2
    for (px, py) in ((x0, y0), (x1, y1)):
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / L, dx / L
        G += (T.gauss(px + nx * w * 0.9, py + ny * w * 0.9, w * 0.9) + T.gauss(px - nx * w * 0.9, py - ny * w * 0.9, w * 0.9)) * k * 1.3
    return G


def _gaster(T, x, y, s, abre, ang, k):
    """O Gaster Blaster: o crânio de dragão alongado com a mandíbula que abre e os olhos acesos."""
    c, sn = math.cos(ang), math.sin(ang)
    cranio = [(-0.6, -0.5), (0.3, -0.55), (0.9, -0.25), (1.0, 0.0), (0.4, 0.0), (-0.6, 0.1)]
    mand = [(-0.5, 0.15), (0.4, 0.05 + 0.4 * abre), (0.95, 0.15 + 0.5 * abre), (0.3, 0.35 + 0.4 * abre), (-0.5, 0.45)]
    G, H = 0.0, 0.0
    for pts in (cranio, mand):
        g, h = icone(T, poe(pts, x, y, s, ang), k * 1.1, 0.45)
        G, H = G + g, H + h
    ox, oy = x + (0.0 * c - (-0.25) * sn) * s, y + (0.0 * sn + (-0.25) * c) * s
    H += T.gauss(ox, oy, s * 0.1) * k * 2.2
    G += T.ring(s * 0.14, s * 0.04, ox, oy) * k
    return G, H


# ------------------------------------------------------------------ Creeper

def chiado_creeper(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.55, 0.68))
    if k > 0:
        g, h = _creeper(T, -0.6, -0.05, 0.2, k, 0.3 * math.sin(t * 30) ** 2)
        G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.1 + 0.06 * j, 0.5 + 0.06 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 0.8 * u, 0.025 * (1 - 0.5 * u), -0.6, 0.6, 1.0, 0, -0.55, -0.05, 0.0) * (1 - u) * 1.3
    g, h = clarao(T, t, 0.4, 0.58, 0.45, -0.05, 0.8, 1.0)
    G, H = G + g, H + h
    m = surge(t, 0.5, 0.65) * (1 - rel(t, 0.9, 1))
    if m > 0:
        pis = 1.0 if (t * 8) % 1 < 0.5 else 0.4
        g, h = _creeper(T, 0.45, -0.45, 0.06 * m, pis)
        G, H = G + g, H + h
        G += T.ring(0.18 * m, 0.01, 0.45, -0.05) * pis
    return G * env, H * env


def camuflagem_verde(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    some = pulso(t, 0.15, 0.85)
    q = np.random.default_rng(730)
    for i in range(6):
        for j in range(4):
            x, y = -0.25 + 0.1 * i, -0.3 + 0.12 * j
            vis = 1 - some * (0.5 + 0.5 * q.uniform())
            g, h = _quad(T, x, y, 0.045, vis, 0.6)
            G, H = G + g, H + h
    for j in range(8):
        a = TAU * j / 8
        x = 0.4 * math.cos(a)
        g, h = icone(T, poe(PENA, x, 0.32, 0.08, 0.3 * math.sin(t * 6 + j)), some * 0.9, 0.6)
        G, H = G + g, H + h
    G += T.ring(0.45, 0.012, 0.0, -0.05, 0.9) * pulso(t, 0.4, 1.0) * 0.8
    return G * env, H * env


def creeper_preparo(T, t, rng):
    G, H = vazio(T)
    incha = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = _creeper(T, 0.0, -0.05, 0.22, 1.0, incha)
    G, H = G + g, H + h
    G += T.gauss(0.0, -0.05, 0.3) * (0.3 + 0.6 * incha * ((t * 4) % 1 < 0.5))
    return G, H


def explosao_creeper(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    k = 1 - rel(t, 0.25, 0.3)
    if k > 0:
        g, h = _creeper(T, 0.0, -0.05, 0.18, k, rel(t, 0.0, 0.25))
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.05, 0.3) * pulso(t, 0.1, 0.3) * ((t * 12) % 1 < 0.5) * 1.0
    g, h = clarao(T, t, 0.25, 0.5, 0.0, -0.05, 2.4, 2.2)
    G, H = G + g, H + h
    u = rel(t, 0.27, 0.85)
    if 0 < u < 1:
        q = np.random.default_rng(731)
        for _ in range(26):
            a, v = q.uniform(0, TAU), q.uniform(0.3, 1.0)
            x, y = 0.95 * v * ease_out(u) * math.cos(a), -0.05 + 0.7 * v * ease_out(u) * math.sin(a) + 0.4 * u * u
            g, h = _quad(T, x, y, 0.03 * (1 - u) + 0.006, 1 - u, 0.7)
            G, H = G + g, H + h
        G += T.gauss(0.0, -0.05, 0.1 + 0.5 * u) * (1 - u) * 1.0
    G += onda_no_chao(T, t, 0.28, 0.9, 1.1, 0.38, 1.8)
    G += anel(T, t, 0.28, 0.8, 0.05, 1.0, 0.05, -0.05, 1.0, 1.5)
    cr = rel(t, 0.4, 0.7)
    if cr > 0:
        G += T.ring(0.3 * ease_out(cr), 0.03, 0.0, 0.38, 3.0) * (1 - rel(t, 0.85, 0.97)) * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Pac-Man

def comer_pacman(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.6)
    k = 1 - rel(t, 0.55, 0.68)
    if k > 0:
        x = -0.55 + 0.85 * u
        boca = 0.9 * abs(math.sin(t * 25))
        g, h = _pacman(T, x, -0.05, 0.16, boca, 0.0, k)
        G, H = G + g, H + h
        for j in range(4):
            bx = x + 0.25 + 0.15 * j
            if bx < 0.4:
                H += T.gauss(bx, -0.05, 0.015) * k * 1.8
    g, h = clarao(T, t, 0.32, 0.52, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g, H + h
    # a vida voltando: as bolinhas indo do rival para o Pac-Man
    v = rel(t, 0.45, 0.9)
    if 0 < v < 1:
        for j in range(5):
            w = min(1, max(0, v * 1.5 - j * 0.1))
            x = 0.45 + (-0.25 - 0.45) * ease_in(w)
            H += T.gauss(x, -0.05 - 0.15 * math.sin(math.pi * w), 0.014) * (1 - rel(w, 0.85, 1)) * 1.8
    return G * env, H * env


def pilula_de_poder(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    p = pulso(t, 0.0, 0.4)
    if p > 0:
        pis = 0.6 + 0.4 * math.sin(t * 40)
        G += T.gauss(-0.2, -0.05, 0.06) * p * pis * 1.5 + T.ring(0.07, 0.014, -0.2, -0.05) * p
        H += T.gauss(-0.2, -0.05, 0.03) * p * pis * 2.0
    cresce = ease_out(rel(t, 0.25, 0.55), 2)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        boca = 0.9 * abs(math.sin(t * 20))
        g, h = _pacman(T, -0.5 + 0.2 * rel(t, 0.0, 0.3), -0.05, 0.14 + 0.12 * cresce, boca, 0.0, k)
        G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.7, 0.1, 0.6, 0.035, -0.05, 1.0, 1.3)
    v = pulso(t, 0.45, 1.0)
    if v > 0:
        for j in range(4):
            y = -0.35 + 0.2 * j
            o = ((t * 3) + j * 0.31) % 1
            G += T.tapered([(-0.95 + 0.3 * o, y, -0.65 + 0.3 * o, y, 0.8)], 0.015) * v
    return G * env, H * env


def pacman_preparo(T, t, rng):
    G, H = vazio(T)
    segs = [(-0.5, -0.3, 0.5, -0.3, 1.0), (-0.5, 0.2, 0.5, 0.2, 1.0), (-0.5, -0.3, -0.5, -0.1, 1.0), (0.5, 0.0, 0.5, 0.2, 1.0)]
    G += T.lines(segs, 0.014) * 0.9
    x = -0.4 + 0.8 * (t % 1)
    for j in range(8):
        bx = -0.4 + 0.1 * j
        if bx > x:
            H += T.gauss(bx, -0.05, 0.012) * 1.6
    g, h = _pacman(T, x, -0.05, 0.1, 0.9 * abs(math.sin(t * TAU * 4)), 0.0, 1.0)
    return G + g, H + h


def comer_fantasma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    pisca = 1.0 if (t * 6) % 1 < 0.6 else 0.5
    kf = 1 - rel(t, 0.42, 0.5)
    if kf > 0:
        g, h = _fantasma(T, 0.45, -0.05, 0.16, kf * pisca)
        G, H = G + g, H + h
    u = ease_in(rel(t, 0.1, 0.45), 1.8)
    k = 1 - rel(t, 0.7, 0.82)
    if k > 0:
        boca = 0.95 * abs(math.sin(t * 22))
        g, h = _pacman(T, -0.55 + 1.0 * u, -0.05, 0.2, boca, 0.0, k)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.42, 0.6, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    # os olhinhos do fantasma voltando para casa (os buffs saindo)
    v = rel(t, 0.5, 0.95)
    if 0 < v < 1:
        for lado in (-1, 1):
            G += T.gauss(0.45 + lado * 0.05 + 0.3 * v, -0.1 - 0.4 * v, 0.02) * (1 - v) * 1.4
    G += estouro(T, t, 0.45, 0.8, 12, 732, 0.45, -0.05, 0.45, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Crash

def giro_crash(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = rel(t, 0.0, 0.8)
    if 0 < u < 1:
        x = -0.6 + 1.2 * ease_in(u, 1.2)
        k = 1 - rel(u, 0.85, 1)
        for j in range(4):
            a = t * 30 + TAU * j / 4
            G += T.arc_band(0.12 + 0.05 * j, 0.025, a, a + 2.5, 0.45, 0, x, 0.0, 1.0) * k * 1.2
        G += T.gauss(x, 0.0, 0.08, 0.16) * k * 0.8
        G += T.tapered([(x - 0.4, 0.15, x - 0.1, 0.15, 0.6)], 0.03) * k
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.15 + 0.2 * i, 0.32 + 0.2 * i, cx, -0.05, 0.7, 1.0)
        G, H = G + g, H + h
    G += particulas(T, t, 0.1, 1.0, 20, 733, 0.0, 0.3, 0.7, 0.3, 0.014)
    return G * env, H * env


def aku_aku_mascara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 0.97))
    if s > 0:
        g, h = _mascara(T, 0.15 + 0.03 * math.sin(t * 8), -0.35 + 0.02 * math.sin(t * 12), 0.14 * s, 1.0)
        G, H = G + g, H + h
        G += T.ring(0.38 * s, 0.02, 0.0, -0.05, 0.9) * 1.1
    for j in range(6):
        a = t * TAU + TAU * j / 6
        H += T.gauss(0.36 * math.cos(a), -0.05 + 0.36 * math.sin(a) * 0.9, 0.012) * pulso(t, 0.2, 1.0) * 1.6
    G += anel(T, t, 0.2, 0.6, 0.1, 0.6, 0.03, -0.05, 1.0, 1.2)
    return G * env, H * env


def caixa_de_nitro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.4)
    if 0 < u < 1:
        e = ease_in(u, 1.3)
        g, h = _caixa_nitro(T, -0.55 + 1.0 * e, -0.05 - 0.3 * math.sin(math.pi * e), 0.14, 1.0, u * 8)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.38, 0.6, 0.45, -0.05, 1.6, 1.6)
    G, H = G + g, H + h
    v = rel(t, 0.38, 0.85)
    if 0 < v < 1:
        G += T.gauss(0.45, -0.05, 0.05 + 0.3 * ease_out(v)) * (1 - v) * 1.3
        q = np.random.default_rng(734)
        for _ in range(10):
            a, w = q.uniform(0, TAU), q.uniform(0.4, 1)
            x, y = 0.45 + 0.4 * w * v * math.cos(a), -0.05 + 0.4 * w * v * math.sin(a) + 0.3 * v * v
            G += T.lines([(x - 0.025, y, x + 0.025, y + 0.015, 1.0)], 0.012) * (1 - v) * 1.2
    m = surge(t, 0.6, 0.75) * (1 - rel(t, 0.9, 1))
    if m > 0:
        g, h = _caixa_nitro(T, 0.45, -0.45, 0.05 * m, (0.6 + 0.4 * math.sin(t * 40)))
        G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Arthur Morgan

def dead_eye_arthur(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    # a tela ficando sépia: a vinheta escura em volta
    v = pulso(t, 0.0, 0.9)
    G += T.ring(0.8, 0.14, 0.0, -0.05, 1.3) * v * 0.22
    for j, (px, py) in enumerate(((0.4, -0.25), (0.5, -0.05), (0.42, 0.15))):
        m = surge(t, 0.2 + 0.1 * j, 0.32 + 0.1 * j) * (1 - rel(t, 0.85, 1))
        if m > 0:
            G += _x_marca(T, px, py, 0.05 * m, 1.0)
            H += T.gauss(px, py, 0.02) * m * 1.8
    G += T.ring(0.25, 0.01, 0.45, -0.05) * pulso(t, 0.15, 0.9) * 1.1
    G += T.lines([(0.45, -0.35, 0.45, -0.28, 1.0), (0.45, 0.18, 0.45, 0.25, 1.0), (0.17, -0.05, 0.24, -0.05, 1.0), (0.66, -0.05, 0.73, -0.05, 1.0)], 0.01) * pulso(t, 0.15, 0.9)
    return G * env, H * env


def laco_arthur(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    gira = pulso(t, 0.0, 0.35)
    if gira > 0:
        a = t * 25
        G += T.ring(0.12, 0.012, -0.5, -0.45, 2.5) * gira * 1.2
        G += T.polyline([(-0.55, 0.0), (-0.5 + 0.12 * math.cos(a), -0.45 + 0.05 * math.sin(a))], 0.01) * gira
    u = rel(t, 0.25, 0.5)
    if 0 < u < 1:
        x = -0.5 + 0.95 * ease_out(u)
        y = -0.45 + 0.1 * math.sin(math.pi * u)
        G += T.ring(0.12 - 0.04 * u, 0.012, x, y, 2.5) * 1.2
        G += T.polyline([(-0.55, 0.0), (x - 0.12, y)], 0.01)
    aperta = rel(t, 0.48, 0.65)
    k = 1 - rel(t, 0.85, 0.97)
    if aperta > 0 and k > 0:
        G += T.ring(0.18 - 0.05 * aperta, 0.014, 0.45, -0.1, 3.0) * k * 1.3
        G += T.ring(0.18 - 0.05 * aperta, 0.014, 0.45, 0.05, 3.0) * k * 1.1
        G += T.polyline([(-0.55, 0.0), (0.3, -0.1)], 0.01) * k
    return G * env, H * env


def arthur_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _revolver(T, 0.0, 0.05, 0.45, 1.0)
    G, H = G + g, H + h
    arma = (t * 2) % 1
    G += T.lines([(-0.05, -0.0, -0.05 - 0.05 * arma, -0.08 - 0.04 * arma, 1.0)], 0.02) * 1.2
    # o chapéu por cima
    G += T.arc_band(0.12, 0.03, math.pi, TAU, 1.0, 0, 0.0, -0.35, 0.0) * 1.1 + T.lines([(-0.22, -0.35, 0.22, -0.35, 1.0)], 0.02) * 1.1
    return G, H


def revolver_arthur(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.75, 0.88))
    if k > 0:
        g, h = _revolver(T, -0.65, -0.05, 0.4, k)
        G, H = G + g, H + h
    for j in range(4):
        a0 = 0.22 + 0.1 * j
        g, h = clarao(T, t, a0, a0 + 0.06, -0.38, -0.08, 0.45, 1.1)
        G, H = G + g, H + h
        u = rel(t, a0, a0 + 0.08)
        if 0 < u < 1:
            x = -0.38 + 0.83 * u
            H += T.lines([(x - 0.15, -0.08, x, -0.07 + 0.02 * (j - 1.5) * u, 1.0)], 0.006) * 1.8
        g2, h2 = clarao(T, t, a0 + 0.07, a0 + 0.15, 0.45, -0.07 + 0.03 * (j - 1.5), 0.45, 0.85)
        G, H = G + g2, H + h2
    G += estouro(T, t, 0.55, 0.9, 12, 735, 0.45, -0.05, 0.45, 0.012)
    f = rel(t, 0.6, 1.0)
    if 0 < f < 1:
        pts = [(-0.38 + 0.04 * math.sin(v * 8), -0.08 - 0.3 * v * f) for v in np.linspace(0, 1, 14)]
        G += T.polyline(pts, 0.012) * (1 - f) * 0.9
    return G * env, H * env


# ------------------------------------------------------------------ Ellie

def canivete_ellie(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, (ang, a0) in enumerate(((0.6, 0.15), (2.5, 0.3), (0.9, 0.45))):
        g, h = corte(T, t, a0, a0 + 0.18, ang, 0.55, 0.03, 0.45, -0.05, 0.03)
        G, H = G + g, H + h
        g, h = clarao(T, t, a0 + 0.04, a0 + 0.16, 0.45, -0.05, 0.6, 0.9)
        G, H = G + g, H + h
    q = rel(t, 0.3, 0.95)
    if 0 < q < 1:
        rr = np.random.default_rng(736)
        for _ in range(8):
            a, v = rr.uniform(-2.8, -0.3), rr.uniform(0.5, 1.0)
            x, y = 0.45 + 0.3 * v * q * math.cos(a), -0.05 + 0.25 * v * q * math.sin(a) + 0.45 * q * q
            G += T.gauss(x, y, 0.012) * (1 - q) * 1.4
    return G * env, H * env


def furtividade_ellie(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    some = pulso(t, 0.1, 0.9)
    # a silhueta agachada (cabeça e costas) sumindo
    G += T.gauss(0.0, -0.05, 0.08) * (1 - 0.7 * some) + T.gauss(0.05, 0.1, 0.12, 0.08) * (1 - 0.7 * some)
    # o mato na frente
    for j in range(9):
        x = -0.4 + 0.1 * j
        h = 0.15 + 0.08 * math.sin(j * 1.7)
        G += T.polyline([(x, 0.38), (x + 0.03 * math.sin(t * 3 + j), 0.38 - h)], 0.012) * 1.0
    # a "audição": as ondas saindo
    for j in range(3):
        u = rel(t, 0.3 + 0.12 * j, 0.7 + 0.12 * j)
        if 0 < u < 1:
            G += T.ring(0.1 + 0.6 * u, 0.012, 0.0, -0.05) * (1 - u) * 1.1
    v = pulso(t, 0.4, 1.0)
    if v > 0:
        for j in range(3):
            y = -0.3 + 0.15 * j
            o = ((t * 3) + j * 0.31) % 1
            G += T.tapered([(-0.85 + 0.3 * o, y, -0.55 + 0.3 * o, y, 0.8)], 0.012) * v
    return G * env, H * env


def ellie_preparo(T, t, rng):
    G, H = vazio(T)
    puxa = 0.7 + 0.3 * math.sin(t * TAU * 2)
    G += _arco(T, 0.1, -0.05, 0.4, puxa, 1.0)
    G += T.lines([(-0.25 - 0.2 * puxa, -0.05, 0.3, -0.05, 1.0)], 0.01) * 1.2
    G += T.polys([([(0.3, -0.08), (0.38, -0.05), (0.3, -0.02)], 1.0)], 0.003) * 1.2
    G += T.ring(0.08, 0.008, 0.45, -0.05) * (0.6 + 0.4 * math.sin(t * TAU * 3))
    return G, H


def arco_silencioso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.4, 0.5))
    if k > 0:
        G += _arco(T, -0.45, -0.05, 0.35, 1 - rel(t, 0.25, 0.3), k)
    u = rel(t, 0.28, 0.5)
    if 0 < u < 1:
        x = -0.4 + 0.85 * ease_in(u, 1.3)
        G += T.lines([(x - 0.18, -0.05, x, -0.05, 1.0)], 0.01) * 1.3
        G += T.polys([([(x, -0.08), (x + 0.07, -0.05), (x, -0.02)], 1.0)], 0.003) * 1.3
        G += T.tapered([(x - 0.45, -0.05, x - 0.18, -0.05, 0.5)], 0.008)
    g, h = clarao(T, t, 0.48, 0.65, 0.45, -0.05, 1.0, 1.1)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.lines([(0.32, -0.05, 0.45, -0.05, 1.0)], 0.01) * m * 1.2
    G += anel(T, t, 0.5, 0.8, 0.04, 0.4, 0.025, -0.05, 1.0, 1.2)
    return G * env, H * env


# ------------------------------------------------------------------ Sans

def ossos_sans(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.75)
    if 0 < u < 1:
        for j in range(7):
            x = -0.7 + 0.2 * j + 1.0 * u - 0.5
            if -0.75 < x < 0.85:
                alto = 0.25 + 0.15 * ((j % 3) / 2)
                G += _osso(T, x, 0.38, x, 0.38 - alto * min(1, u * 4), 0.02, 1 - rel(u, 0.85, 1))
    g, h = clarao(T, t, 0.35, 0.55, 0.45, 0.0, 0.9, 1.0)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.ring(0.15, 0.012, 0.45, -0.45) * m * 1.2
        G += _osso(T, 0.38, -0.45, 0.52, -0.45, 0.012, m)
    return G * env, H * env


def desviar_sans(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desliza = pulso(t, 0.1, 0.8)
    x = -0.3 * desliza
    # o crânio do Sans com o sorrisão
    G += T.ring(0.13, 0.014, x, -0.25) * 1.2
    for lado in (-1, 1):
        G += T.gauss(x + lado * 0.05, -0.27, 0.02) * 0.8
    H += T.gauss(x - 0.05, -0.27, 0.012) * (1 if desliza > 0.3 else 0) * 2.0
    G += T.arc_band(0.08, 0.012, 0.3, math.pi - 0.3, 1.0, 0, x, -0.24, 0.0) * 1.2
    G += T.lines([(x, -0.12, x, 0.3, 1.0)], 0.05) * 0.8
    # o golpe passando pelo lugar onde ele estava
    u = rel(t, 0.25, 0.6)
    if 0 < u < 1:
        G += T.tapered([(0.8 - 1.6 * u + 0.3, -0.1, 0.8 - 1.6 * u, -0.1, 1.0)], 0.04) * 1.2
    G += T.gauss(0.0, -0.05, 0.12, 0.3) * desliza * 0.3
    return G * env, H * env


def sans_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.13, 0.014, -0.3, -0.25) * 1.2
    H += T.gauss(-0.35, -0.27, 0.025) * (0.7 + 0.3 * math.sin(t * TAU * 4)) * 2.2
    G += T.gauss(-0.35, -0.27, 0.06) * (0.5 + 0.3 * math.sin(t * TAU * 4))
    g, h = _gaster(T, 0.15, -0.05, 0.32, 0.2 + 0.2 * math.sin(t * TAU), 0.0, 1.0)
    return G + g, H + h


def gaster_blaster(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.94, 1)
    for i, (gx, gy, ang) in enumerate(((-0.6, -0.55, 0.4), (-0.65, 0.1, -0.15))):
        s = surge(t, 0.0 + 0.08 * i, 0.25 + 0.08 * i) * (1 - rel(t, 0.75, 0.88))
        if s > 0:
            abre = ease_out(rel(t, 0.3, 0.45))
            g, h = _gaster(T, gx, gy, 0.26 * s, abre, ang, 1.0)
            G, H = G + g, H + h
            r = pulso(t, 0.42, 0.85)
            if r > 0:
                c, sn = math.cos(ang), math.sin(ang)
                bx, by = gx + 0.28 * c, gy + 0.28 * sn
                G += T.tapered([(bx, by, bx + 1.5 * c, by + 1.5 * sn, 1.0)], 0.12 * r) * 1.0
                H += T.lines([(bx, by, bx + 1.5 * c, by + 1.5 * sn, 1.0)], 0.02) * r * 1.6
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.04 * i, 0.72 + 0.04 * i, cx, -0.05, 0.7, 0.9)
        G, H = G + g, H + h
    G += particulas(T, t, 0.45, 1.0, 22, 737, 0.0, -0.05, 0.8, 0.4, 0.012)
    return G * env, H * env


REGISTRO = [
    ("chiado_creeper", chiado_creeper, GRANDE, "Creeper · o chiado e a marca piscando", False),
    ("camuflagem_verde", camuflagem_verde, GRANDE, "Creeper · os pixels sumindo no mato", False),
    ("creeper_preparo", creeper_preparo, MEDIA, "Creeper · inchando e piscando (Preparo, laço)", True),
    ("explosao_creeper", explosao_creeper, GRANDE, "Creeper · a explosão de pixels", False),
    ("comer_pacman", comer_pacman, GRANDE, "Pac-Man · a mordida e a vida voltando", False),
    ("pilula_de_poder", pilula_de_poder, GRANDE, "Pac-Man · a pílula e o Pac-Man crescendo", False),
    ("pacman_preparo", pacman_preparo, MEDIA, "Pac-Man · o labirinto e as bolinhas (Preparo, laço)", True),
    ("comer_fantasma", comer_fantasma, GRANDE, "Pac-Man · o fantasma azul engolido", False),
    ("giro_crash", giro_crash, GRANDE, "Crash · o redemoinho do giro", False),
    ("aku_aku_mascara", aku_aku_mascara, GRANDE, "Crash · a máscara Aku Aku", False),
    ("caixa_de_nitro", caixa_de_nitro, GRANDE, "Crash · a caixa de Nitro explodindo", False),
    ("dead_eye_arthur", dead_eye_arthur, GRANDE, "Arthur Morgan · a tela sépia e os X", False),
    ("laco_arthur", laco_arthur, GRANDE, "Arthur Morgan · o laço girando e prendendo", False),
    ("arthur_preparo", arthur_preparo, MEDIA, "Arthur Morgan · o revólver e o chapéu (Preparo, laço)", True),
    ("revolver_arthur", revolver_arthur, GRANDE, "Arthur Morgan · os tiros em sequência", False),
    ("canivete_ellie", canivete_ellie, GRANDE, "Ellie · o canivete rápido", False),
    ("furtividade_ellie", furtividade_ellie, GRANDE, "Ellie · agachada no mato e a audição", False),
    ("ellie_preparo", ellie_preparo, MEDIA, "Ellie · o arco puxado (Preparo, laço)", True),
    ("arco_silencioso", arco_silencioso, GRANDE, "Ellie · a flecha silenciosa", False),
    ("ossos_sans", ossos_sans, GRANDE, "Sans · as fileiras de ossos", False),
    ("desviar_sans", desviar_sans, GRANDE, "Sans · deslizando com o sorrisão", False),
    ("sans_preparo", sans_preparo, MEDIA, "Sans · o olho azul e o Gaster Blaster (Preparo, laço)", True),
    ("gaster_blaster", gaster_blaster, GRANDE, "Sans · as caveiras e o raio", False),
]
