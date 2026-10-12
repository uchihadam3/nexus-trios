"""Rodada 32 das habilidades próprias: Mickey, Pato Donald, Pateta, Stitch, Buzz Lightyear e Woody.

Mickey Mouse
- chapeu_de_feiticeiro: o chapéu azul de feiticeiro com a lua e as estrelas, e a magia que cura (Vida e Escudo).
- mickey_preparo: o Preparo da Alegria contagiante — a luva branca acenando e o brilho (laço).
- alegria_contagiante: as orelhas redondas no alto, as notas e o confete estourando no rival (Enfraquecido).

Pato Donald
- ataque_de_furia: a nuvem de briga com os punhos saindo para todo lado (Fortalecido).
- grito_indignado: o balão de fala serrilhado, os rabiscos de raiva e as ondas do grito (Acelerado).
- explosao_de_raiva: o vapor saindo da cabeça e a explosão vermelha em todos (Exposto e Acelerado).

Pateta
- tropecao_do_pateta: o escorregão, o chapéu voando e as estrelinhas (Confuso e Marcado).
- ai_ai_ai: o grito "a-hyuck!" do Pateta voando em espiral e o tombo (Paralisado e Confuso).
- pateta_preparo: o Preparo do Acidente feliz — o Pateta se equilibrando, o chapéu balançando (laço).
- acidente_feliz: o piano caindo do céu em cima dos rivais (Lento).

Stitch
- quatro_bracos: os quatro braços arranhando ao mesmo tempo (as quatro garras).
- mordida_de_stitch: a bocarra azul mordendo todos (Exposto e Vida).
- stitch_preparo: o Preparo do Experimento 626 — as duas pistolas de plasma carregando (laço).
- experimento_626: a rajada de plasma azul das quatro pistolas e o impacto (Fortalecido).

Buzz Lightyear
- laser_do_braco: a mira no rival e o laser vermelho pulsando (Marcado e Exposto).
- modo_de_combate: as asas abrindo com o estalo e o pulso que atrapalha o Preparo (Marcado).
- buzz_preparo: o Preparo do Ao infinito e além! — as asas abertas e o foguete das costas acendendo (laço).
- ao_infinito_e_alem: o voo com o rastro do foguete e a estrela no impacto.

Woody
- plano_do_xerife: a estrela de xerife enorme sobre o trio (Escudo e Fortalecido).
- woody_preparo: o Preparo do Todos juntos — a cordinha das costas sendo puxada (laço).
- todos_juntos: o laço de corda abraçando o trio e as estrelinhas (Acelerado, Carga e Escudo).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (ASA, CHAMA, LUA, NOTA, anel, aura, cheio, circulo, clarao, converge, estouro, estrela_pts, icone, onda_no_chao,
                         particulas, poe, raios, surge)


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


def _cabeca_de_rato(cx, cy, s):
    """As três bolas: a cabeça e as duas orelhas."""
    return [poe(circulo(20), cx, cy, 0.5 * s), poe(circulo(20), cx - 0.5 * s, cy - 0.5 * s, 0.3 * s), poe(circulo(20), cx + 0.5 * s, cy - 0.5 * s, 0.3 * s)]


# ------------------------------------------------------------------ Mickey

_CHAPEU = [(-0.55, 0.6), (0.55, 0.6), (0.4, 0.45), (0.15, -0.2), (0.05, -0.75), (0.25, -1.0), (-0.1, -0.85), (-0.2, -0.3), (-0.4, 0.45)]


def chapeu_de_feiticeiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.7, 0.9))
    if s > 0:
        g, h = icone(T, poe(_CHAPEU, 0, -0.35, 0.3 * s), 1.2, 0.45)
        G, H = G + g, H + h
        g2, h2 = cheio(T, poe(LUA, -0.02, -0.38, 0.05 * s), 1.4)
        G, H = G + g2, H + h2
        for j, (dx, dy) in enumerate(((0.06, -0.28), (-0.06, -0.48), (0.03, -0.2))):
            g3, h3 = cheio(T, poe(estrela_pts(5, 0.45), dx, dy, 0.025 * s), 1.4)
            G, H = G + g3, H + h3
    for j in range(10):
        ang = TAU * j / 10 + t * 3
        u = rel(t, 0.25, 0.9)
        if 0 < u < 1:
            r = 0.15 + 0.35 * u
            g4, h4 = cheio(T, poe(estrela_pts(5, 0.45), r * math.cos(ang), -0.35 + 0.2 + r * 0.7 * math.sin(ang), 0.03), (1 - rel(u, 0.7, 1)) * 1.3)
            G, H = G + g4, H + h4
    g5, h5 = aura(T, t, 0.35, 1.0, 0.38, 0.1, 0.8)
    G += anel(T, t, 0.4, 0.9, 0.1, 0.6, 0.03, 0.1)
    return (G + g5) * env, (H + h5) * env


def mickey_preparo(T, t, rng):
    G, H = vazio(T)
    ang = 0.35 * math.sin(t * TAU * 2)
    cx, cy = 0.15 * math.sin(ang), -0.1
    g, h = icone(T, poe(circulo(20), cx, cy, 0.14), 1.2, 0.6)
    G, H = G + g, H + h
    for j in range(4):
        a = -math.pi / 2 + ang + (j - 1.5) * 0.4
        g2, h2 = icone(T, poe(circulo(14), cx + 0.2 * math.cos(a), cy + 0.2 * math.sin(a), 0.06), 1.1, 0.6)
        G, H = G + g2, H + h2
    G += T.gauss(cx, cy, 0.3) * (0.35 + 0.15 * math.sin(t * 8))
    q = np.random.default_rng(int(t * 10))
    for _ in range(4):
        a = q.uniform(0, TAU)
        g3, h3 = cheio(T, poe(estrela_pts(4, 0.35), cx + 0.35 * math.cos(a), cy + 0.3 * math.sin(a), 0.03), 1.2)
        G, H = G + g3, H + h3
    return G, H


def alegria_contagiante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.55, 0.7))
    if s > 0:
        for pts in _cabeca_de_rato(0.35, -0.45, 0.32 * s):
            g, h = icone(T, pts, 1.1, 0.45)
            G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.1 + 0.05 * j, 0.55 + 0.05 * j)
        if 0 < u < 1:
            x = -0.7 + 1.05 * u
            y = -0.1 - 0.25 * math.sin(math.pi * u) + 0.05 * math.sin(j * 2)
            g2, h2 = cheio(T, poe(NOTA, x, y, 0.08), (1 - rel(u, 0.85, 1)) * 1.4)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.5, 0.7, 0.35, 0.0, 1.0)
    G, H = G + g3, H + h3
    q = np.random.default_rng(7)
    for j in range(22):
        a = q.uniform(0, TAU)
        w = rel(t, 0.52, 0.98)
        if 0 < w < 1:
            r = q.uniform(0.15, 0.6) * ease_out(w, 2)
            x, y = 0.35 + r * math.cos(a), r * 0.8 * math.sin(a) + 0.25 * w * w
            g4, h4 = cheio(T, poe([(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)], x, y, 0.022, a + w * 8), (1 - rel(w, 0.75, 1)) * 1.4)
            G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Pato Donald

def ataque_de_furia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    q = np.random.default_rng(int(t * 25))
    pts = [(0.35 + q.normal(0, 0.14), q.normal(0, 0.12), k * q.uniform(0.4, 0.9)) for _ in range(28)]
    G += T.splats(pts, 0.07) * 0.9
    for j in range(4):
        a = q.uniform(0, TAU)
        if k > 0.2:
            P, nos = _punho(T, 0.35 + 0.3 * math.cos(a), 0.25 * math.sin(a), 1.4, a)
            G += P * 0.8 * k
            H += nos * 0.3 * k
    for j in range(5):
        a = q.uniform(0, TAU)
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0.35 + 0.33 * math.cos(a), 0.28 * math.sin(a), 0.04), k * 1.3)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.35, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


def grito_indignado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        balao = [((0.3 + 0.05 * (j % 2)) * s * math.cos(TAU * j / 18), -0.35 + (0.2 + 0.04 * (j % 2)) * s * math.sin(TAU * j / 18)) for j in range(18)]
        g, h = icone(T, balao, 1.1, 0.4)
        G, H = G + g, H + h
        G += T.lines([(0, -0.47, 0, -0.33, 1.0)], 0.03) * s * 1.4
        G += T.gauss(0, -0.27, 0.022) * s * 1.6
        q = np.random.default_rng(int(t * 14))
        for j in range(3):
            x0 = -0.15 + 0.15 * j
            pts = [(x0 + 0.03 * m, -0.62 + (0.03 if m % 2 else -0.03) + q.normal(0, 0.005)) for m in range(5)]
            G += T.polyline(pts, 0.01) * s * 1.2
    for j in range(3):
        G += T.arc_band(0.25 + 0.15 * ((t * 2.5 + j / 3) % 1), 0.02, -0.6, 0.6, 1.0, 0, 0.15, 0.0, 0.0) * pulso(t, 0.2, 0.9) * (1 - (t * 2.5 + j / 3) % 1) * 1.4
    return G * env, H * env


def explosao_de_raiva(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for lado in (-1, 1):
        for j in range(4):
            u = (t * 3 + j / 4) % 1
            k = pulso(t, 0.0, 0.45)
            G += T.gauss(-0.6 + lado * (0.05 + 0.1 * u), -0.3 - 0.35 * u, 0.03 + 0.05 * u) * (1 - u) * k * 1.2
    vermelho = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.38, 0.45))
    G += T.gauss(-0.6, 0.0, 0.15 * vermelho + 0.01, 0.2 * vermelho + 0.01) * 0.9
    g, h = clarao(T, t, 0.4, 0.62, 0.15, 0.0, 1.6, 1.5)
    G, H = G + g, H + h
    for x in (-0.5, 0.1, 0.65):
        g2, h2 = clarao(T, t, 0.45, 0.65, x, 0.1, 0.6)
        G, H = G + g2, H + h2
    for j in range(2):
        G += anel(T, t, 0.42 + 0.08 * j, 0.9, 0.1, 1.0, 0.045, 0.05)
    G += estouro(T, t, 0.42, 0.95, 18, 5, 0.15, 0.0, 0.85, 0.014)
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.35, 1.5)
    return G * env, H * env


# ------------------------------------------------------------------ Pateta

_CHAPEU_PATETA = [(-0.5, 0.4), (0.5, 0.4), (0.35, 0.15), (0.3, -0.6), (0.0, -0.8), (-0.3, -0.6), (-0.35, 0.15)]


def tropecao_do_pateta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.35)
    if 0 < u < 1:
        G += T.tapered([(-0.7, 0.3, -0.7 + 0.8 * ease_out(u), 0.3, 1.0)], 0.04) * (1 - u) * 1.2
    u = rel(t, 0.1, 0.65)
    if 0 < u < 1:
        x = -0.4 + 0.8 * u
        y = -0.1 - 0.55 * math.sin(math.pi * u)
        g, h = icone(T, poe(_CHAPEU_PATETA, x, y, 0.13, u * TAU * 1.5), 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.0, 0.25, 0.9)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.3, 0.7, 0.5, 0.35, 1.3)
    g3, h3 = _tontas(T, t, 0.45, 1.0, 0.45, -0.15, 4, 0.16, 0.045)
    G, H = G + g3, H + h3
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.13 * s, 0.02, 0.45, 0.1) * 1.2 + T.ring(0.07 * s, 0.015, 0.45, 0.1) * 1.2
        G += T.lines([(0.45 - 0.16 * s, 0.1, 0.45 + 0.16 * s, 0.1, 1.0), (0.45, 0.1 - 0.16 * s, 0.45, 0.1 + 0.16 * s, 1.0)], 0.008) * 1.1
    return G * env, H * env


def ai_ai_ai(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.55)
    if 0 < u < 1:
        pts = []
        for m in range(40):
            v = u * m / 39
            r = 0.35 * (1 - v)
            pts.append((-0.6 + 1.1 * v + r * math.cos(v * 16), -0.2 + r * 0.6 * math.sin(v * 16) - 0.2 * math.sin(math.pi * v)))
        G += T.polyline(pts, 0.025) * (1 - rel(u, 0.85, 1)) * 1.2
        x, y = pts[-1]
        G += T.gauss(x, y, 0.08) * 1.0
        H += T.gauss(x, y, 0.03) * 1.2
    g, h = clarao(T, t, 0.52, 0.72, 0.5, 0.1, 1.2, 1.3)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.52, 0.9, 0.7, 0.35, 1.5)
    G += raios(T, t, 0.55, 0.75, 4, 8, 0.5, 0.0, 0.3, 0.009)
    g2, h2 = _tontas(T, t, 0.6, 1.0, 0.5, -0.2, 4, 0.15, 0.045)
    return (G + g2) * env, (H + h2) * env


def pateta_preparo(T, t, rng):
    G, H = vazio(T)
    ang = 0.4 * math.sin(t * TAU * 1.5)
    g, h = icone(T, poe(_CHAPEU_PATETA, 0.3 * math.sin(ang), -0.25, 0.18, ang), 1.2, 0.5)
    G, H = G + g, H + h
    G += T.lines([(0, 0.4, 0.4 * math.sin(ang), -0.1, 1.0)], 0.025) * 0.9
    for j in range(2):
        u = ((t * 1.8) + j / 2) % 1
        g2, h2 = cheio(T, poe(estrela_pts(4, 0.35), -0.3 + 0.6 * j, -0.3 + 0.2 * u, 0.04), (1 - u) * 1.2)
        G, H = G + g2, H + h2
    return G, H


def acidente_feliz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.gauss(0, 0.32, 0.35 * ease_out(rel(t, 0.0, 0.4)) + 0.01, 0.03) * pulso(t, 0.0, 0.45) * 1.0
    u = ease_in(rel(t, 0.1, 0.45), 2.2)
    k = 1 - rel(t, 0.55, 0.65)
    if u > 0 and k > 0:
        y = -1.0 + 1.15 * u
        piano = [(-0.4, y - 0.18), (0.4, y - 0.18), (0.4, y + 0.1), (-0.4, y + 0.1)]
        g, h = icone(T, piano, k * 1.2, 0.4)
        G, H = G + g, H + h
        teclas = [(-0.38 + 0.076 * m, y + 0.1, -0.38 + 0.076 * m, y + 0.17, 1.0) for m in range(11)]
        G += T.lines(teclas, 0.006) * k * 1.2
        G += T.lines([(-0.4, y + 0.17, 0.4, y + 0.17, 1.0)], 0.01) * k * 1.1
    g2, h2 = clarao(T, t, 0.42, 0.62, 0.0, 0.2, 1.3, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.43, 0.95, 1.0, 0.35, 1.6)
    q = np.random.default_rng(4)
    for j in range(10):
        w = rel(t, 0.45, 0.95)
        if 0 < w < 1:
            a = math.pi + q.uniform(0.2, math.pi - 0.2)
            r = q.uniform(0.3, 0.8) * ease_out(w)
            g3, h3 = cheio(T, poe(NOTA, r * math.cos(a), 0.2 + r * 0.7 * math.sin(a) + 0.3 * w * w, 0.05), (1 - rel(w, 0.7, 1)) * 1.3)
            G, H = G + g3, H + h3
    for x in (-0.55, 0.0, 0.55):
        g4, h4 = _tontas(T, t, 0.6, 1.0, x, -0.15, 3, 0.1, 0.03)
        G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Stitch

def quatro_bracos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (dy, a0) in enumerate(((-0.25, 0.05), (-0.08, 0.12), (0.08, 0.19), (0.25, 0.26))):
        u = rel(t, a0, a0 + 0.22)
        if 0 < u < 1:
            for m in range(3):
                y = dy * 1.4 + (m - 1) * 0.07
                x0, x1 = -0.2 + 0.1 * (j % 2), 0.8
                xe = x0 + (x1 - x0) * min(1, u * 1.8)
                xs = x0 + (x1 - x0) * max(0, u * 1.8 - 0.8)
                G += T.tapered([(xs, y - 0.06 * (1 if j % 2 else -1), xe, y + 0.1 * (1 if j % 2 else -1), 1.0)], 0.04) * 1.4
                H += T.lines([(xs, y, xe, y, 1.0)], 0.005) * 0.8
    g, h = clarao(T, t, 0.25, 0.55, 0.45, 0.0, 0.9)
    G, H = G + g, H + h
    G += estouro(T, t, 0.3, 0.8, 12, 3, 0.45, 0.0, 0.35, 0.012)
    return G * env, H * env


def mordida_de_stitch(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.15, 0.4), 2)
    k = 1 - rel(t, 0.6, 0.75)
    for x in (-0.55, 0.0, 0.55):
        if k > 0 and t > 0.02:
            abre = 0.28 * (1 - fecha) + 0.02
            for lado in (-1, 1):
                y = 0.0 + lado * abre
                arco = [(x + 0.22 * math.cos(a), y + lado * 0.1 * math.sin(a)) for a in np.linspace(0, math.pi, 12)]
                g, h = icone(T, arco, k * 1.1, 0.4)
                G, H = G + g, H + h
                dentes = [(x - 0.18 + 0.072 * m, y, x - 0.18 + 0.072 * m + 0.036, y - lado * 0.06, 1.0) for m in range(6)]
                G += T.lines(dentes, 0.01) * k * 1.3
        g2, h2 = clarao(T, t, 0.38, 0.58, x, 0.0, 0.55)
        G, H = G + g2, H + h2
    G += particulas(T, t, 0.4, 0.95, 12, 3, 0, 0.1, 0.7, 0.4, 0.012)
    return G * env, H * env


def stitch_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 3)
    for lado in (-1, 1):
        cx = lado * 0.22
        G += T.lines([(cx - 0.1 * lado, 0.05, cx + 0.05 * lado, 0.0, 1.0)], 0.05) * 0.8
        G += T.gauss(cx + 0.08 * lado, -0.02, 0.04 + 0.02 * b) * 1.4
        H += T.gauss(cx + 0.08 * lado, -0.02, 0.02) * (1.2 + 0.8 * b)
        G += converge(T, (t * 2) % 1, 0.0, 1.0, 6, int(t * 2) + (lado > 0), cx + 0.08 * lado, -0.02, 0.2)
    return G, H


def experimento_626(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(8):
        a0 = 0.03 * j
        u = rel(t, a0, a0 + 0.22)
        if 0 < u < 1:
            y0 = -0.15 + 0.1 * (j % 4)
            x = -0.7 + 1.2 * u
            y = y0 + (0.0 - y0) * u
            G += T.tapered([(x - 0.18, y + (y0 - y) * 0.2, x, y, 1.0)], 0.05) * 1.3
            H += T.gauss(x, y, 0.025) * 1.5
    g, h = clarao(T, t, 0.22, 0.5, 0.5, 0.0, 1.3, 1.4)
    G, H = G + g, H + h
    u = rel(t, 0.25, 0.7)
    if 0 < u < 1:
        G += T.ring(0.05 + 0.5 * ease_out(u, 2), 0.035 * (1 - 0.5 * u), 0.5, 0.0) * (1 - u) * 1.3
    G += estouro(T, t, 0.25, 0.85, 16, 6, 0.5, 0.0, 0.55, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Buzz Lightyear

def laser_do_braco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        G += T.ring(0.16 * (2 - s), 0.012, 0.55, 0.0) * 1.3
        G += T.lines([(0.55 - 0.24, 0.0, 0.55 - 0.08, 0.0, 1.0), (0.55 + 0.08, 0.0, 0.55 + 0.24, 0.0, 1.0),
                      (0.55, -0.24, 0.55, -0.08, 1.0), (0.55, 0.08, 0.55, 0.24, 1.0)], 0.008) * s * 1.3
    k = pulso(t, 0.25, 0.8)
    if k > 0:
        pis = 0.75 + 0.25 * math.sin(t * 80)
        G += T.tapered([(-0.7, -0.05, 0.55, 0.0, 1.0)], 0.04 * k + 0.005) * pis * 1.4
        H += T.lines([(-0.7, -0.05, 0.55, 0.0, 1.0)], 0.01) * k * pis * 1.7
    g, h = clarao(T, t, 0.28, 0.75, 0.55, 0.0, 0.8)
    G, H = G + g, H + h
    G += particulas(T, t, 0.3, 0.9, 10, 5, 0.55, 0.0, 0.1, 0.3, 0.011)
    return G * env, H * env


def modo_de_combate(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 3) * (1 - rel(t, 0.7, 0.85))
    if abre > 0:
        for lado in (-1, 1):
            asa = [(lado * x, y) for x, y in ASA]
            g, h = icone(T, poe(asa, -0.5, -0.05, 0.3 * abre, -lado * 0.3 * (1 - abre)), 1.1, 0.45)
            G, H = G + g, H + h
        H += T.gauss(-0.5, -0.05, 0.03) * abre * 1.5
    g2, h2 = clarao(T, t, 0.15, 0.3, -0.5, -0.05, 0.6)
    G, H = G + g2, H + h2
    for j in range(3):
        u = rel(t, 0.25 + 0.08 * j, 0.75 + 0.08 * j)
        if 0 < u < 1:
            G += T.ring(0.05 + 0.35 * u, 0.025, -0.5 + 1.0 * u, 0.0, 1.0) * (1 - u) * 1.3
    G += raios(T, t, 0.5, 0.9, 5, 3, 0.5, 0.0, 0.3, 0.01)
    g3, h3 = clarao(T, t, 0.55, 0.75, 0.5, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


def buzz_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        asa = [(lado * x, y) for x, y in ASA]
        g, h = icone(T, poe(asa, 0, -0.05, 0.32), 1.0, 0.45)
        G, H = G + g, H + h
    tremula = 0.8 + 0.2 * math.sin(t * 40)
    for lado in (-1, 1):
        g2, h2 = icone(T, poe(CHAMA, lado * 0.08, 0.25, 0.09 * tremula, math.pi), 1.3, 0.6)
        G, H = G + g2, H + h2 * 1.5
    G += T.gauss(0, 0.25, 0.15) * (0.4 + 0.2 * math.sin(t * 12))
    return G, H


def ao_infinito_e_alem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.6)
    if 0 < u < 1:
        x = -0.85 + 1.4 * u
        y = 0.1 - 0.35 * math.sin(math.pi * u * 0.8)
        xr = -0.85 + 1.4 * max(0, u - 0.35)
        yr = 0.1 - 0.35 * math.sin(math.pi * max(0, u - 0.35) * 0.8)
        G += T.tapered([(xr, yr, x, y, 1.0)], 0.09) * 1.2
        H += T.lines([(xr, yr, x, y, 1.0)], 0.012) * 1.2
        for lado in (-1, 1):
            asa = [(x0, lado * y0) for x0, y0 in ASA]
            g, h = icone(T, poe(asa, x, y, 0.13, math.pi), 1.1, 0.45)
            G, H = G + g, H + h
        G += particulas(T, t, 0.0, 0.4, 16, 3, x - 0.2, y, 0.08, 0.1, 0.012)
    g2, h2 = clarao(T, t, 0.38, 0.62, 0.55, 0.0, 1.6, 1.5)
    G, H = G + g2, H + h2
    s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g3, h3 = icone(T, poe(estrela_pts(5, 0.45), 0.55, 0.0, 0.22 * s, t * 2), 1.2, 0.5)
        G, H = G + g3, H + h3
    G += anel(T, t, 0.4, 0.9, 0.1, 0.7, 0.04, 0.0)
    G += estouro(T, t, 0.4, 0.95, 18, 7, 0.55, 0.0, 0.7, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Woody

def plano_do_xerife(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.75, 0.9))
    if s > 0:
        estrela = estrela_pts(6, 0.6)
        g, h = icone(T, poe(estrela, 0, -0.3, 0.26 * s, t * 0.5), 1.2, 0.45)
        G, H = G + g, H + h
        for j in range(6):
            a = t * 0.5 + TAU * j / 6 - math.pi / 2
            G += T.gauss(0.26 * s * math.cos(a), -0.3 + 0.26 * s * math.sin(a), 0.022) * 1.4
        G += T.ring(0.1 * s, 0.015, 0, -0.3) * 1.2
    g2, h2 = clarao(T, t, 0.3, 0.5, 0, -0.3, 0.7)
    G, H = G + g2, H + h2
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.35, 1.0)
        G += T.ring(0.2, 0.03, x, 0.1, 1.2) * k * 1.0
        G += T.gauss(x, 0.1, 0.17, 0.2) * k * 0.4
    return G * env, H * env


def woody_preparo(T, t, rng):
    G, H = vazio(T)
    u = (t * 1.5) % 1
    puxa = math.sin(math.pi * u)
    x = -0.1 + 0.55 * puxa
    G += T.lines([(-0.35, 0.05, x, 0.05, 1.0)], 0.014) * 1.3
    G += T.ring(0.1, 0.03, x + 0.1, 0.05) * 1.4
    g, h = icone(T, poe(estrela_pts(6, 0.6), -0.35, -0.15, 0.13, t), 1.1, 0.45)
    G, H = G + g, H + h
    G += T.gauss(-0.35, 0.05, 0.07) * 1.0
    H += T.gauss(-0.35, 0.05, 0.03) * (1.0 + 0.6 * puxa)
    G += T.gauss(0, 0, 0.3) * 0.25 * puxa
    return G, H


def todos_juntos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.45), 2)
    if u > 0:
        n = max(2, int(60 * u))
        pts = [(0.85 * math.cos(math.pi - TAU * u * m / (n - 1)), 0.1 + 0.4 * math.sin(math.pi - TAU * u * m / (n - 1))) for m in range(n)]
        G += T.polyline(pts, 0.02) * (1 - rel(t, 0.85, 1)) * 1.3
        G += T.polyline([(x, y + 0.02) for x, y in pts], 0.006) * (1 - rel(t, 0.85, 1)) * 0.7
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.4, 1.0)
        G += T.gauss(x, 0.1, 0.16, 0.24) * k * 0.55
        g, h = _tontas(T, t, 0.45, 1.0, x, -0.3, 3, 0.1, 0.035)
        G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.45, 0.95, 0.95, 0.35, 1.4)
    g2, h2 = clarao(T, t, 0.42, 0.6, 0, 0.1, 0.8)
    return (G + g2) * env, (H + h2) * env


REGISTRO = [
    ("chapeu_de_feiticeiro", chapeu_de_feiticeiro, GRANDE, "Mickey · o chapéu de feiticeiro e as estrelas", False),
    ("mickey_preparo", mickey_preparo, MEDIA, "Mickey · a luva acenando (Preparo, laço)", True),
    ("alegria_contagiante", alegria_contagiante, GRANDE, "Mickey · as orelhas, as notas e o confete", False),
    ("ataque_de_furia", ataque_de_furia, GRANDE, "Pato Donald · a nuvem de briga", False),
    ("grito_indignado", grito_indignado, GRANDE, "Pato Donald · o balão serrilhado e o grito", False),
    ("explosao_de_raiva", explosao_de_raiva, GRANDE, "Pato Donald · o vapor e a explosão vermelha", False),
    ("tropecao_do_pateta", tropecao_do_pateta, GRANDE, "Pateta · o escorregão e o chapéu voando", False),
    ("ai_ai_ai", ai_ai_ai, GRANDE, "Pateta · o voo em espiral e o tombo", False),
    ("pateta_preparo", pateta_preparo, MEDIA, "Pateta · se equilibrando (Preparo, laço)", True),
    ("acidente_feliz", acidente_feliz, GRANDE, "Pateta · o piano caindo", False),
    ("quatro_bracos", quatro_bracos, GRANDE, "Stitch · as quatro garras", False),
    ("mordida_de_stitch", mordida_de_stitch, GRANDE, "Stitch · a bocarra mordendo todos", False),
    ("stitch_preparo", stitch_preparo, MEDIA, "Stitch · as pistolas de plasma carregando (Preparo, laço)", True),
    ("experimento_626", experimento_626, GRANDE, "Stitch · a rajada de plasma", False),
    ("laser_do_braco", laser_do_braco, GRANDE, "Buzz Lightyear · a mira e o laser vermelho", False),
    ("modo_de_combate", modo_de_combate, GRANDE, "Buzz Lightyear · as asas abrindo e o pulso", False),
    ("buzz_preparo", buzz_preparo, MEDIA, "Buzz Lightyear · as asas e o foguete acendendo (Preparo, laço)", True),
    ("ao_infinito_e_alem", ao_infinito_e_alem, GRANDE, "Buzz Lightyear · o voo e a estrela", False),
    ("plano_do_xerife", plano_do_xerife, GRANDE, "Woody · a estrela de xerife sobre o trio", False),
    ("woody_preparo", woody_preparo, MEDIA, "Woody · a cordinha sendo puxada (Preparo, laço)", True),
    ("todos_juntos", todos_juntos, GRANDE, "Woody · o laço de corda abraçando o trio", False),
]
