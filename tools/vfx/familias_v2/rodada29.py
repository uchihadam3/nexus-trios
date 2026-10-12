"""Rodada 29 das habilidades próprias: Spawn, Invencível, Leonardo, Raphael, Donatello, Michelangelo e Constantine.

Spawn
- correntes_necroplasmicas: as correntes verdes saindo do corpo e chicoteando o rival.
- capa_viva: a capa vermelha viva se espalha em tiras e prende todos (Preso e Sangrando).
- spawn_preparo: o Preparo do Fogo do inferno — os olhos verdes e o fogo verde subindo pelas mãos (laço).
- fogo_do_inferno: a rajada de fogo verde do inferno (Fortalecido).

Invencível
- soco_supersonico: o soco com o cone de som supersônico (Preso).
- investida_orbital: o voo vindo do céu com o rastro azul e amarelo, e o impacto (Escudo e Fortalecido).
- invencivel_preparo: o Preparo do Levantar de novo — o herói no chão se erguendo, a aura juntando (laço).
- levantar_de_novo: o soco de quem levantou: a onda de choque enorme (Preso e Escudo).

Leonardo
- katanas_gemeas: as duas katanas em X com o brilho azul (Marcado e Enfraquecido).
- formacao: as quatro bandanas (o trio em formação) e as setas de avanço (Acelerado e Escudo).
- leonardo_preparo: o Preparo da Investida do líder — as katanas cruzadas na guarda (laço).
- investida_do_lider: o avanço com as duas katanas em rastro e o corte final (Preparo reduzido).

Raphael
- investida_furiosa: os sais girando e o avanço furioso (Exposto e Fortalecido).
- sem_recuo: o soco de cabeça baixa com a aura vermelha de raiva (Exposto e Acelerado).

Donatello
- bastao_bo: o bastão girando em hélice e varrendo todos (Lento e Enfraquecido).
- dispositivo_tatico: o aparelho de engrenagens com a luz vermelha piscando (Preparo interrompido e Marca explosiva).
- campo_de_contencao: a grade de laser se fechando em volta do rival (Preparo atrasado e Preso).

Michelangelo
- giro_maluco: o giro com os nunchakus e as estrelinhas de tontura (Confuso).
- festa_surpresa: os balões, o confete e as fatias de pizza caindo (Lento).

Constantine
- pacto: o pentagrama riscado no chão e a fumaça do cigarro (Silenciado, Enfraquecido e levantar aliado).
- exorcismo: a cruz de luz e o demônio arrancado do rival (Exposto e Dissipar).
- blefe_infernal: as cartas de tarô e a fumaça, o rival enganado (Preparo interrompido e Confuso).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CARTA, CHAMA, CRUZ, ESPADA, SETA, anel, aura, cheio, chuva, clarao, converge, corte, engrenagem, estouro, estrela_pts,
                         icone, onda_no_chao, particulas, poe, raios, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _elos(T, pts, k=1.0, r=0.022):
    out = 0
    for i in range(len(pts) - 1):
        out = out + T.ring(r, r * 0.35, pts[i][0], pts[i][1], 0.6 if i % 2 else 1.0)
    return out * k * 1.3


def _pentagrama(cx, cy, r, sq=0.5):
    pts = [(cx + r * math.cos(-math.pi / 2 + TAU * j * 2 / 5), cy + r * sq * math.sin(-math.pi / 2 + TAU * j * 2 / 5)) for j in range(6)]
    return pts


# ------------------------------------------------------------------ Spawn

def correntes_necroplasmicas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.75, 0.9)
    for j in range(3):
        u = ease_out(rel(t, 0.05 * j, 0.4 + 0.05 * j), 2)
        if u > 0:
            pts = [(-0.55 + 1.2 * v * u, -0.2 + 0.2 * j + 0.15 * math.sin(v * 6 + j + t * 8) * (1 - v)) for v in np.linspace(0, 1, 28)]
            G += _elos(T, pts, k)
    g, h = clarao(T, t, 0.4, 0.6, 0.65, 0.0, 0.8)
    return (G + g) * env, (H + h) * env


def capa_viva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(7):
        u = ease_out(rel(t, 0.03 * j, 0.45 + 0.03 * j), 2)
        if u > 0:
            ang = -0.6 + 0.2 * j
            pts = [(-0.7 + 1.5 * v * u * math.cos(ang) * 0.9, 1.0 * v * u * math.sin(ang) * 0.6 + 0.06 * math.sin(v * 9 + t * 10 + j)) for v in np.linspace(0, 1, 24)]
            for i in range(len(pts) - 1):
                G += T.lines([(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0)], 0.035 * (1 - 0.6 * i / 24)) * k * 1.0
    for x in (-0.4, 0.15, 0.6):
        e = ease_out(rel(t, 0.45, 0.75), 2)
        if e > 0:
            G += T.arc_band(0.12, 0.02, 0, TAU * e, 0.4, 0, x, 0.1, 1.0) * k * 1.2
    return G * env, H * env


def spawn_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.09, -0.35, 0.025) * (1.6 + 0.4 * math.sin(t * 12))
        G += T.gauss(lado * 0.09, -0.35, 0.06) * 0.9
    for j in range(6):
        u = (t * 1.3 + j / 6) % 1
        lado = -1 if j % 2 else 1
        g, h = icone(T, poe(CHAMA, lado * 0.3 + 0.03 * math.sin(u * 10), 0.3 - 0.45 * u, 0.13 * (1 - 0.5 * u)), (1 - u) * 1.2, 0.6)
        G, H = G + g, H + h
    return G, H


def fogo_do_inferno(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(5)
    u = rel(t, 0.1, 0.85)
    if 0 < u < 1:
        for j in range(26):
            v = (u * 1.3 + j / 26) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            x = -0.5 + 1.25 * v
            y = q.normal(0, 0.07) * v
            g, h = icone(T, poe(CHAMA, x, y, 0.06 + 0.15 * v, math.pi / 2), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.0, 0.25, -0.5, 0.0, 0.6)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Invencível

def soco_supersonico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        P, nos = _punho(T, -0.5 + 0.8 * u, 0.0, 2.2, 0)
        G += P * 0.9 * k
        H += nos * 0.5 * k
    for j in range(4):
        uu = rel(t, 0.25 + 0.05 * j, 0.7 + 0.05 * j)
        if 0 < uu < 1:
            r = 0.1 + 0.4 * uu
            G += T.arc_band(r, 0.03, -1.0, 1.0, 1.0, 0, 0.3 + 0.4 * uu - r, 0.0, 1.0) * (1 - uu) * 1.4
    g, h = clarao(T, t, 0.28, 0.45, 0.4, 0.0, 0.9)
    return (G + g) * env, (H + h) * env


def investida_orbital(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.6)
    if t < 0.42:
        x, y = -0.7 + 1.3 * u, -0.9 + 0.95 * u
        G += T.gauss(x, y, 0.08) * 1.3
        for j, dy in enumerate((-0.03, 0.03)):
            G += T.tapered([(x - 0.6 + dy, y - 0.6 - dy, x, y + dy, 0.6)], 0.035) * (1.2 if j == 0 else 0.8)
    g, h = clarao(T, t, 0.38, 0.6, 0.6, 0.05, 1.3, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.38, 0.9, 0.9, 0.35, 1.6)
    G += T.ring(0.4, 0.035, -0.4, 0.0) * surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1)) * 1.1
    return G * env, H * env


def invencivel_preparo(T, t, rng):
    G, H = vazio(T)
    sobe = 0.5 + 0.5 * math.sin(t * 3)
    G += T.gauss(0, 0.2 - 0.2 * sobe, 0.1, 0.18) * 0.9
    G += converge(T, (t * 1.2) % 1, 0.0, 1.0, 14, 4, 0, 0.0, 0.5, 0.01) * 0.9
    g, h = aura(T, 0.5, 0.0, 1.0, 0.3, 0.0, 0.7)
    return G + g, H + h


def levantar_de_novo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        P, nos = _punho(T, -0.4 + 0.75 * u, 0.0, 2.8, 0)
        G += P * 0.9 * k
        H += nos * 0.6 * k
    g, h = clarao(T, t, 0.22, 0.45, 0.4, 0.0, 1.3, 1.5)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.22 + 0.06 * j, 0.9, 0.08, 0.7 + 0.1 * j, 0.04, 0.0, 1.0, 1.4)
    G += T.ring(0.35, 0.03, -0.45, 0.0) * surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1)) * 1.1
    return G * env, H * env


# ------------------------------------------------------------------ Leonardo

def katanas_gemeas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for k, (a, t0) in enumerate(((0.8, 0.05), (-0.8, 0.12))):
        g, h = corte(T, t, t0, t0 + 0.35, a, 1.4, 0.08, 0.1, 0.0)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.2, 0.4, 0.1, 0.0, 0.8)
    G, H = G + g2, H + h2
    m = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.015, 0.1, 0.0) * 1.3 + T.ring(0.07 * m, 0.012, 0.1, 0.0) * 1.3
    return G * env, H * env


def formacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(4):
        s = surge(t, 0.04 * j, 0.3 + 0.04 * j) * (1 - rel(t, 0.6, 0.75))
        if s > 0:
            x = -0.45 + 0.3 * j
            G += T.lines([(x - 0.1 * s, -0.4, x + 0.1 * s, -0.4, 1.0)], 0.035) * 1.2
            G += T.lines([(x + 0.1 * s, -0.4, x + 0.16 * s, -0.33, 1.0), (x + 0.1 * s, -0.4, x + 0.18 * s, -0.42, 1.0)], 0.015) * 1.2
    for j in range(3):
        u = rel(t, 0.35 + 0.08 * j, 0.85 + 0.04 * j)
        if 0 < u < 1:
            g, h = cheio(T, poe(SETA, -0.4 + 0.4 * j + 0.2 * ease_out(u), 0.1, 0.12), (1 - rel(u, 0.75, 1)) * 1.3)
            G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.35, 0.9, 0.9, 0.38)
    return G * env, H * env


def leonardo_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        g, h = icone(T, poe(ESPADA, lado * 0.08, -0.05, 0.4, lado * 0.6), 1.0, 0.5)
        G, H = G + g, H + h
    H += T.gauss(0, -0.2, 0.04) * (1.2 + 0.5 * math.sin(t * 8))
    return G, H


def investida_do_lider(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 1.5)
    k = 1 - rel(t, 0.5, 0.7)
    if u > 0 and k > 0:
        x = -0.7 + 1.3 * u
        for dy in (-0.08, 0.08):
            G += T.tapered([(x - 0.7, dy, x, dy, 0.5)], 0.035) * k * 1.2
        G += T.gauss(x, 0.0, 0.1, 0.18) * k * 0.8
    for j, a in enumerate((0.9, -0.9)):
        g, h = corte(T, t, 0.32 + 0.05 * j, 0.6 + 0.05 * j, a, 1.4, 0.09, 0.5, 0.0)
        G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.35, 0.55, 0.5, 0.0, 1.1)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Raphael

def _sai(cx, cy, s, ang):
    return poe([(0, -1), (0.06, -0.2), (0.35, -0.45), (0.4, -0.38), (0.1, -0.05), (0.06, 0.5), (-0.06, 0.5), (-0.1, -0.05), (-0.4, -0.38),
                (-0.35, -0.45), (-0.06, -0.2)], cx, cy, s, ang)


def investida_furiosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.5)
    x = -0.6 + 1.1 * u
    k = 1 - rel(t, 0.55, 0.7)
    for lado in (-1, 1):
        g, h = icone(T, _sai(x, lado * 0.18, 0.32, t * 30 * lado), 1.2 * k, 0.6)
        G, H = G + g, H + h
    G += T.tapered([(x - 0.5, 0.0, x - 0.1, 0.0, 0.5)], 0.06) * k
    g2, h2 = clarao(T, t, 0.38, 0.55, 0.55, 0.0, 1.0)
    G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.4, 1.0, 0.35, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


def sem_recuo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = aura(T, t, 0.0, 0.6, 0.45, 0.0, 1.3)
    G, H = G + g, H + h
    u = ease_in(rel(t, 0.2, 0.45), 2)
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        P, nos = _punho(T, -0.4 + 0.8 * u, 0.0, 2.6, 0)
        G += P * 0.9 * k
        H += nos * 0.5 * k
    g2, h2 = clarao(T, t, 0.43, 0.65, 0.45, 0.0, 1.2, 1.4)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.43, 0.85, 16, 4, 0.45, 0.0, 0.55, 0.015)
    return G * env, H * env


# ------------------------------------------------------------------ Donatello

def bastao_bo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.8)
    k = 1 - rel(t, 0.75, 0.9)
    if u < 1:
        x = -0.6 + 1.2 * u
        a = t * 25
        G += T.lines([(x - 0.4 * math.cos(a), -0.05 - 0.15 * math.sin(a), x + 0.4 * math.cos(a), -0.05 + 0.15 * math.sin(a), 1.0)], 0.03) * k * 1.2
        G += T.arc_band(0.4, 0.04, a, a + 1.5, 0.37, 0, x, -0.05, 1.0) * k * 0.9
        G += T.arc_band(0.4, 0.04, a + math.pi, a + math.pi + 1.5, 0.37, 0, x, -0.05, 1.0) * k * 0.9
    for xx in (-0.5, 0.0, 0.5):
        g, h = clarao(T, t, 0.15 + 0.3 * (xx + 0.5), 0.3 + 0.3 * (xx + 0.5), xx, 0.0, 0.5)
        G, H = G + g, H + h
    return G * env, H * env


def dispositivo_tatico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.35)
    x = -0.5 + 1.1 * ease_out(u, 2) if u > 0 else -0.5
    y = -0.3 * math.sin(math.pi * min(1, u))
    s = 1 - rel(t, 0.85, 1)
    g, h = icone(T, poe([(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], x, y, 0.2, 0), s * 1.1, 0.5)
    G, H = G + g, H + h
    g2, h2 = icone(T, poe(engrenagem(8, 1.0, 0.75), x - 0.08, y, 0.1, t * 8), s, 0.4)
    G, H = G + g2, H + h2
    pisca = 1 if int(t * 12) % 2 == 0 else 0.3
    H += T.gauss(x + 0.12, y - 0.06, 0.035) * 2.2 * pisca * s
    G += T.gauss(x + 0.12, y - 0.06, 0.08) * pisca * s
    if u >= 1:
        G += anel(T, t, 0.35, 0.8, 0.05, 0.4, 0.03, y)
    return G * env, H * env


def campo_de_contencao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_out(rel(t, 0.0, 0.45), 2)
    k = 1 - rel(t, 0.85, 1)
    r = 0.7 - 0.35 * fecha
    segs = []
    for j in range(8):
        a = TAU * j / 8 + t * 2
        segs.append((0.3 + r * math.cos(a), r * 0.7 * math.sin(a), 0.3 + r * math.cos(a + TAU / 8), r * 0.7 * math.sin(a + TAU / 8), 1.0))
    G += T.lines(segs, 0.015) * k * 1.4
    H += T.lines(segs, 0.005) * k * 1.2
    for j in range(4):
        y = -0.25 + 0.17 * j
        G += T.lines([(0.3 - r * 0.8, y, 0.3 + r * 0.8, y, 1.0)], 0.006) * k * fecha * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Michelangelo

def giro_maluco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.6)
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        for j in range(2):
            a = t * 30 + j * math.pi
            x1, y1 = 0.35 * math.cos(a), 0.2 * math.sin(a)
            G += T.lines([(0, 0, x1 * 0.5, y1 * 0.5, 1.0)], 0.008) * k * 1.2
            G += T.lines([(x1 * 0.5, y1 * 0.5, x1, y1, 1.0)], 0.03) * k * 1.2
        G += T.ring(0.35, 0.03, 0, 0, 0.57) * k * 0.6
    for j in range(5):
        a = TAU * j / 5 + t * 8
        kk = pulso(t, 0.45, 1.0)
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0.6 + 0.15 * math.cos(a), -0.35 + 0.06 * math.sin(a), 0.04), kk * 1.4)
        G, H = G + g, H + h * 1.5
    return G * env, H * env


def _pizza(cx, cy, s, ang):
    return poe([(0, -0.8), (0.5, 0.6), (-0.5, 0.6)], cx, cy, s, ang)


def festa_surpresa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = rel(t, 0.05 * j, 0.7 + 0.05 * j)
        if 0 < u < 1:
            x = -0.5 + 0.5 * j
            y = 0.3 - 0.9 * ease_out(u)
            g, h = icone(T, [(x + 0.08 * math.cos(a), y + 0.1 * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)], (1 - u) * 1.1, 0.5)
            G, H = G + g, H + h
            G += T.lines([(x, y + 0.1, x + 0.02 * math.sin(u * 10), y + 0.3, 1.0)], 0.006) * (1 - u)
    g2, h2 = chuva(T, t, 0.2, 1.0, [(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)], 30, 3, 0.02, -0.9, 0.4, 0.9, 6.0, 1.3)
    G, H = G + g2, H + h2
    q = np.random.default_rng(8)
    for j in range(5):
        u = rel(t, 0.3 + 0.08 * j, 0.8 + 0.04 * j)
        if 0 < u < 1:
            g3, h3 = icone(T, _pizza(q.uniform(-0.7, 0.7), -0.8 + 1.1 * ease_in(u), 0.09, u * 6 + j), 1.1, 0.6)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Constantine

def pacto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    risca = ease_out(rel(t, 0.0, 0.5), 2)
    k = 1 - rel(t, 0.85, 1)
    pts = _pentagrama(0, 0.3, 0.45)
    n = max(2, int(len(pts) * risca) + 1)
    G += T.polyline(pts[:n], 0.015) * k * 1.4
    G += T.ring(0.45, 0.015, 0, 0.3, 0.5) * k * risca * 1.3
    H += T.polyline(pts[:n], 0.005) * k * 1.2
    q = np.random.default_rng(3)
    u = rel(t, 0.3, 1.0)
    if 0 < u < 1:
        fumo = [(0.4 + 0.08 * math.sin(v * 8 + t * 3), -0.2 - 0.6 * v * u, (1 - v) * 0.6) for v in np.linspace(0, 1, 14)]
        G += T.splats(fumo, 0.04) * 0.9
    g, h = clarao(T, t, 0.45, 0.65, 0, 0.3, 0.6)
    return (G + g) * env, (H + h) * env


def exorcismo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.85))
    g, h = cheio(T, poe(CRUZ, 0.4, -0.1, 0.22 * s), 1.4)
    G, H = G + g, H + h * 2
    g2, h2 = clarao(T, t, 0.2, 0.45, 0.4, -0.1, 1.2)
    G, H = G + g2, H + h2
    u = rel(t, 0.35, 0.9)
    if 0 < u < 1:
        x, y = 0.4 + 0.1 * math.sin(u * 20), -0.1 - 0.7 * ease_out(u)
        demonio = [(x - 0.1, y + 0.1), (x - 0.12, y - 0.05), (x - 0.06, y - 0.02), (x - 0.08, y - 0.14), (x, y - 0.06), (x + 0.08, y - 0.14),
                   (x + 0.06, y - 0.02), (x + 0.12, y - 0.05), (x + 0.1, y + 0.1)]
        g3, h3 = icone(T, demonio, (1 - u) * 1.0, 0.6)
        G, H = G + g3, H + h3
    return G * env, H * env


def blefe_infernal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = ease_out(rel(t, 0.05 * j, 0.35 + 0.05 * j), 2)
        k = 1 - rel(t, 0.6, 0.75)
        if u > 0 and k > 0:
            x = -0.4 + 0.4 * j * u
            g, h = icone(T, poe(CARTA, x, 0.0, 0.16, (j - 1) * 0.3 * u), k * 1.1, 0.6)
            G, H = G + g, H + h
            G += T.ring(0.05, 0.01, x, 0.0) * k
    q = np.random.default_rng(7)
    u = rel(t, 0.55, 1.0)
    if 0 < u < 1:
        pts = [(q.normal(0, 0.4) * (0.5 + u), q.normal(0, 0.2), (1 - u) * q.uniform(0.3, 0.9)) for _ in range(30)]
        G += T.splats(pts, 0.08) * 0.7
    for j in range(3):
        kk = pulso(t, 0.6, 1.0)
        G += T.polyline([(-0.5 + 0.5 * j + 0.08 * math.cos(a), -0.4 + 0.08 * math.sin(a)) for a in np.linspace(0, TAU * 1.5, 20)], 0.01) * kk * 1.2
    return G * env, H * env


REGISTRO = [
    ("correntes_necroplasmicas", correntes_necroplasmicas, GRANDE, "Spawn · as correntes verdes", False),
    ("capa_viva", capa_viva, GRANDE, "Spawn · a capa viva em tiras", False),
    ("spawn_preparo", spawn_preparo, MEDIA, "Spawn · os olhos e o fogo verde (Preparo, laço)", True),
    ("fogo_do_inferno", fogo_do_inferno, GRANDE, "Spawn · a rajada de fogo verde", False),
    ("soco_supersonico", soco_supersonico, GRANDE, "Invencível · o soco e o cone de som", False),
    ("investida_orbital", investida_orbital, GRANDE, "Invencível · o voo do céu e o impacto", False),
    ("invencivel_preparo", invencivel_preparo, MEDIA, "Invencível · se erguendo (Preparo, laço)", True),
    ("levantar_de_novo", levantar_de_novo, GRANDE, "Invencível · o soco de quem levantou", False),
    ("katanas_gemeas", katanas_gemeas, GRANDE, "Leonardo · as katanas em X", False),
    ("formacao", formacao, GRANDE, "Leonardo · as bandanas e as setas", False),
    ("leonardo_preparo", leonardo_preparo, MEDIA, "Leonardo · a guarda das katanas (Preparo, laço)", True),
    ("investida_do_lider", investida_do_lider, GRANDE, "Leonardo · o avanço e o corte final", False),
    ("investida_furiosa", investida_furiosa, GRANDE, "Raphael · os sais girando", False),
    ("sem_recuo", sem_recuo, GRANDE, "Raphael · o soco com a aura de raiva", False),
    ("bastao_bo", bastao_bo, GRANDE, "Donatello · o bastão em hélice", False),
    ("dispositivo_tatico", dispositivo_tatico, GRANDE, "Donatello · o aparelho piscando", False),
    ("campo_de_contencao", campo_de_contencao, GRANDE, "Donatello · a grade de laser", False),
    ("giro_maluco", giro_maluco, GRANDE, "Michelangelo · os nunchakus e as estrelinhas", False),
    ("festa_surpresa", festa_surpresa, GRANDE, "Michelangelo · os balões, o confete e a pizza", False),
    ("pacto", pacto, GRANDE, "Constantine · o pentagrama e a fumaça", False),
    ("exorcismo", exorcismo, GRANDE, "Constantine · a cruz e o demônio", False),
    ("blefe_infernal", blefe_infernal, GRANDE, "Constantine · as cartas de tarô", False),
]
