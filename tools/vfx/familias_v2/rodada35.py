"""Rodada 35 das habilidades próprias: Tom, Jerry, Pantera Cor-de-Rosa, Destruidor, Mestre Splinter, Krang e Casey Jones.

Tom
- emboscada_do_tom: a frigideira saindo de trás e o "PÉIM" com a marca da frigideira no rival (Exposto e Marca explosiva).
- perseguicao: a correria atrás do rival, as pegadas de gato e a poeira (Marcado).
- tom_preparo: o Preparo da Pata certeira — as unhas afiando com o brilho (laço).
- pata_certeira: a pata gigante descendo, os três arranhões e a marca da patinha (Preso).

Jerry
- ratoeira_invertida: a ratoeira armada fechando com o "TLEC" no rival (Acelerado e Esquiva).
- esconderijo: o buraquinho na parede, o rato sumindo e o rival batendo a cara (Confuso e Lento).
- martelada: o martelo enorme descendo e as estrelinhas (Paralisado e Confuso).

Pantera Cor-de-Rosa
- passo_silencioso: as pegadas na ponta dos pés e o som riscado (Silenciado e Enfraquecido).
- troca_discreta: duas silhuetas trocando de lugar numa nuvenzinha e o golpe (Exposto).
- sumico: a fumaça rosa, a pantera sumindo e a interrogação em todos (Interrompe e Silenciado).

Destruidor
- garras_de_aco: os três riscos paralelos das lâminas da manopla e as gotas (Sangrando).
- investida_do_cla: os ninjas do Clã do Pé convergindo em riscos escuros no rival (Exposto).
- shredder_preparo: o Preparo do Golpe do mestre — a manopla erguida, as lâminas brilhando (laço).
- golpe_do_mestre: a rajada de cortes cruzados sem parar (Exposto).

Mestre Splinter
- postura_do_rato: a meditação, o rabo fazendo o círculo e a luz calma (Protegido e Acelerado).
- redirecionar_splinter: a bengala girando e o golpe sendo desviado de volta (Paralisado e Refletir).
- licao_final: a bengala batendo na cabeça, o "!" e as estrelinhas (Confuso e Enfraquecido).

Krang
- comando_remoto: o cérebro mandando as ondas e o escudo hexagonal no aliado (Escudo e Protegido).
- krang_preparo: o Preparo da Dimensão X — o cérebro pulsando dentro do robô (laço).
- dimensao_x: o portal roxo girando e puxando todos (Interrompe e Confuso).

Casey Jones
- taco_de_hoquei: o taco girando e o disco acertando o rival (Exposto).
- sequencia_bruta: o taco e os socos em sequência (Acelerado).
- gooool: a tacada forte, o disco voando, a rede e o "GOL!" (Paralisado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (GOTA, anel, aura, cheio, circulo, clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao, particulas, poe,
                         surge)


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


def _poeira(T, cx, cy, s, k, seed=3, n=10):
    q = np.random.default_rng(seed)
    pts = [(cx + q.normal(0, s), cy + q.normal(0, s * 0.6), k * q.uniform(0.4, 1.0)) for _ in range(n)]
    return T.splats(pts, s * 0.7)


def _patinha(T, cx, cy, s, k):
    """A marca da pata: a almofada e os quatro dedinhos."""
    if k <= 0:
        return 0.0, 0.0
    g, h = cheio(T, poe(circulo(16), cx, cy + s * 0.25, s * 0.45), k * 1.2)
    for j in range(4):
        a = -math.pi / 2 + (j - 1.5) * 0.5
        g2, h2 = cheio(T, poe(circulo(12), cx + s * 0.75 * math.cos(a), cy + s * 0.25 + s * 0.85 * math.sin(a), s * 0.2), k * 1.2)
        g, h = g + g2, h + h2
    return g, h


_INTERROGA = [(-0.12, -0.5), (-0.06, -0.62), (0.06, -0.64), (0.14, -0.56), (0.13, -0.46), (0.03, -0.38), (0.02, -0.28)]


def _interroga(T, cx, cy, s, k):
    pts = [(cx + x * s, cy + (y + 0.45) * s) for x, y in _INTERROGA]
    return T.polyline(pts, 0.022 * s) * k * 1.3 + T.gauss(cx, cy + 0.27 * s, 0.025 * s) * k * 1.5


# ------------------------------------------------------------------ Tom

_FRIGIDEIRA = [(-0.6, -0.6), (0.6, -0.6), (0.6, 0.6), (-0.6, 0.6)]


def emboscada_do_tom(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        cx, cy = 0.1 + 0.35 * u, -0.45 + 0.45 * u
        g, h = icone(T, poe(circulo(22), cx + 0.05, cy, 0.17), k * 1.2, 0.5)
        G, H = G + g, H + h
        G += T.lines([(cx - 0.12, cy, cx - 0.5, cy - 0.2, 1.0)], 0.03) * k * 1.2
    g2, h2 = clarao(T, t, 0.28, 0.48, 0.5, 0.0, 1.2, 1.3)
    G, H = G + g2, H + h2
    s = surge(t, 0.32, 0.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.16 * s, 0.025, 0.5, 0.0) * 1.2
        G += T.lines([(0.5 - 0.16 * s, 0.0, 0.5 - 0.42 * s, 0.12 * s, 1.0)], 0.02) * 1.1
    for j in range(5):
        a = TAU * j / 5 + 0.3
        w = rel(t, 0.3, 0.75)
        if 0 < w < 1:
            G += T.lines([(0.5 + 0.2 * math.cos(a), 0.2 * math.sin(a), 0.5 + (0.2 + 0.25 * w) * math.cos(a), (0.2 + 0.25 * w) * math.sin(a), 1.0)],
                         0.012) * (1 - w) * 1.4
    g3, h3 = _tontas(T, t, 0.5, 1.0, 0.5, -0.25, 3, 0.12, 0.035)
    return (G + g3) * env, (H + h3) * env


def perseguicao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(6):
        k = pulso(t, 0.05 * j, 0.6 + 0.05 * j)
        x = -0.8 + 0.25 * j
        g, h = _patinha(T, x, 0.3 + (0.04 if j % 2 else -0.04), 0.06, k)
        G, H = G + g, H + h
    u = rel(t, 0.0, 0.55)
    if 0 < u < 1:
        x = -0.7 + 1.2 * ease_out(u, 1.4)
        G += _poeira(T, x - 0.15, 0.15, 0.08, 1.0, int(t * 20), 12) * 1.0
        for m in range(4):
            G += T.lines([(x - 0.25, -0.15 + 0.1 * m, x - 0.7, -0.15 + 0.1 * m, 1.0)], 0.007) * 1.1
    s = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.15 * s, 0.018, 0.55, 0.0) * 1.3 + T.ring(0.07 * s, 0.012, 0.55, 0.0) * 1.2
    g2, h2 = clarao(T, t, 0.5, 0.68, 0.55, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


def tom_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(4):
        x = -0.15 + 0.1 * j
        G += T.tapered([(x, 0.15, x + 0.04, -0.2, 1.0)], 0.03) * 1.1
    u = (t * 2) % 1
    y = 0.15 - 0.35 * u
    H += T.gauss(-0.15 + 0.3 * u + 0.04 * (1 - u), y, 0.02) * 2.0
    G += T.gauss(0, 0, 0.25) * (0.3 + 0.15 * math.sin(t * 12))
    return G, H


def pata_certeira(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        a0 = 0.1 + 0.04 * j
        u = rel(t, a0, a0 + 0.25)
        if 0 < u < 1:
            dx = (j - 1) * 0.12
            xs, ys = 0.25 + dx, -0.4
            xe, ye = 0.5 + dx, 0.35
            p = min(1, u * 1.6)
            G += T.tapered([(xs, ys, xs + (xe - xs) * p, ys + (ye - ys) * p, 1.0)], 0.05) * (1 - rel(u, 0.75, 1)) * 1.4
            H += T.lines([(xs, ys, xs + (xe - xs) * p, ys + (ye - ys) * p, 1.0)], 0.008) * (1 - rel(u, 0.75, 1))
    g, h = clarao(T, t, 0.25, 0.45, 0.4, 0.0, 1.1, 1.3)
    G, H = G + g, H + h
    s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    g2, h2 = _patinha(T, 0.4, -0.05, 0.16 * s, 1.0 if s > 0 else 0)
    G, H = G + g2 * 0.8, H + h2
    G += onda_no_chao(T, t, 0.3, 0.8, 0.6, 0.35, 1.3)
    return G * env, H * env


# ------------------------------------------------------------------ Jerry

def ratoeira_invertida(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        g, h = icone(T, [(0.2, 0.2), (0.75, 0.2), (0.75, 0.3), (0.2, 0.3)], s * 1.1, 0.45)
        G, H = G + g, H + h
        fecha = ease_in(rel(t, 0.25, 0.35), 2)
        a = -math.pi * 0.9 * (1 - fecha) - 0.05
        cx, cy = 0.25, 0.2
        G += T.lines([(cx, cy, cx + 0.45 * math.cos(a), cy + 0.25 * math.sin(a), 1.0)], 0.018) * s * 1.3
        G += T.ring(0.03, 0.01, cx, cy) * s * 1.2
    g2, h2 = clarao(T, t, 0.3, 0.5, 0.5, 0.15, 1.0, 1.2)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.3, 0.75, 12, 3, 0.5, 0.15, 0.4, 0.012)
    for j in range(3):
        u = rel(t, 0.35 + 0.06 * j, 0.9)
        if 0 < u < 1:
            G += T.gauss(-0.4 - 0.25 * u + 0.05 * j, -0.1 + 0.05 * j, 0.04) * (1 - u) * 1.0
    g3, h3 = aura(T, t, 0.5, 1.0, 0.25, 0.0, 0.6)
    return (G + g3 * 0.6) * env, (H + h3 * 0.6) * env


def esconderijo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        buraco = [(-0.2 + 0.18 * s * math.cos(a), 0.35 - 0.24 * s * math.sin(a)) for a in np.linspace(0, math.pi, 18)]
        g, h = icone(T, buraco + [(-0.2 - 0.18 * s, 0.35)], 1.1, 0.7)
        G, H = G + g, H + h
        G += T.lines([(-0.75, 0.35, 0.75, 0.35, 1.0)], 0.01) * s * 0.8
    u = rel(t, 0.05, 0.3)
    if 0 < u < 1:
        G += T.gauss(-0.6 + 0.4 * u, 0.28, 0.04) * (1 - u) * 1.2
        G += T.lines([(-0.75 + 0.4 * u, 0.28, -0.95 + 0.4 * u, 0.28, 1.0)], 0.008) * (1 - u)
    w = rel(t, 0.3, 0.55)
    if 0 < w < 1:
        G += T.gauss(0.6 - 0.75 * ease_in(w), 0.1, 0.1) * 0.9
    g2, h2 = clarao(T, t, 0.52, 0.7, -0.1, 0.15, 1.0, 1.2)
    G, H = G + g2, H + h2
    g3, h3 = _tontas(T, t, 0.55, 1.0, 0.0, -0.2, 4, 0.14, 0.04)
    return (G + g3) * env, (H + h3) * env


def martelada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.2)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        a = -2.0 + 1.6 * u
        px, py = -0.1, 0.35
        hx, hy = px + 0.7 * math.cos(a), py + 0.7 * math.sin(a)
        G += T.lines([(px, py, hx, hy, 1.0)], 0.03) * k * 1.2
        perp = a + math.pi / 2
        cab = [(hx + 0.18 * math.cos(perp) + 0.1 * math.cos(a), hy + 0.18 * math.sin(perp) + 0.1 * math.sin(a)),
               (hx - 0.18 * math.cos(perp) + 0.1 * math.cos(a), hy - 0.18 * math.sin(perp) + 0.1 * math.sin(a)),
               (hx - 0.18 * math.cos(perp) - 0.1 * math.cos(a), hy - 0.18 * math.sin(perp) - 0.1 * math.sin(a)),
               (hx + 0.18 * math.cos(perp) - 0.1 * math.cos(a), hy + 0.18 * math.sin(perp) - 0.1 * math.sin(a))]
        g, h = icone(T, cab, k * 1.2, 0.5)
        G, H = G + g, H + h
        if u < 1:
            G += T.arc_band(0.7, 0.08, a - 0.8, a, 1.0, 0, px, py, 1.0) * k * 0.6
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.55, 0.05, 1.4, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.33, 0.85, 0.8, 0.35, 1.6)
    g3, h3 = _tontas(T, t, 0.45, 1.0, 0.55, -0.25, 5, 0.17, 0.045)
    return (G + g3) * env, (H + h3) * env


# ------------------------------------------------------------------ Pantera Cor-de-Rosa

def passo_silencioso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(6):
        k = pulso(t, 0.06 * j, 0.55 + 0.06 * j)
        x = -0.8 + 0.25 * j
        y = 0.32 + (0.04 if j % 2 else -0.03)
        G += (T.gauss(x, y, 0.035, 0.022) + T.gauss(x + 0.05, y - 0.03, 0.012) * 0.8) * k * 1.3
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if s > 0:
        for m in range(3):
            G += T.arc_band(0.08 + 0.07 * m, 0.015, -0.7, 0.7, 1.0, 0, 0.35, -0.1, 0.0) * s * 1.2
        G += T.lines([(0.38, -0.32 * s - 0.1, 0.72, 0.12 * s - 0.1, 1.0)], 0.025) * 1.4
        G += T.ring(0.25 * s, 0.022, 0.55, -0.1) * 1.2
    g, h = clarao(T, t, 0.4, 0.58, 0.55, -0.1, 0.6)
    return (G + g) * env, (H + h) * env


def troca_discreta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 1.5) if t < 0.35 else 1.0
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        for lado, x0 in ((1, -0.4), (-1, 0.4)):
            x = x0 * (1 - 2 * u)
            G += (T.gauss(x, 0.0, 0.07, 0.18) + T.gauss(x, -0.25, 0.06)) * k * (0.6 if lado > 0 else 0.4)
    G += _poeira(T, 0.0, 0.0, 0.1, pulso(t, 0.15, 0.5), 4, 14) * 0.8
    g, h = corte(T, t, 0.45, 0.7, -0.8, 1.0, 0.07, 0.4, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.55, 0.75, 0.4, 0.0, 1.0)
    return (G + g2) * env, (H + h2) * env


def sumico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.55)
    q = np.random.default_rng(6)
    pts = [(q.normal(-0.5, 0.15), q.normal(0.0, 0.15) - 0.2 * rel(t, 0.0, 0.55), k * q.uniform(0.4, 1.0)) for _ in range(34)]
    G += T.splats(pts, 0.07) * 0.6
    G += T.gauss(-0.5, 0.0, 0.08, 0.2) * (1 - rel(t, 0.05, 0.25)) * 1.0
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.4 + 0.07 * j, 0.6 + 0.07 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            G += _interroga(T, x, -0.2, 0.75 * s, 1.0)
        g, h = clarao(T, t, 0.38 + 0.07 * j, 0.52 + 0.07 * j, x, 0.05, 0.45)
        G, H = G + g, H + h
    return G * env, H * env


# ------------------------------------------------------------------ Destruidor

def garras_de_aco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.03 * j, 0.35 + 0.03 * j)
        if 0 < u < 1:
            dy = (j - 1) * 0.12
            p = min(1, u * 1.8)
            xs, ys, xe, ye = -0.1, -0.35 + dy, 0.85, 0.2 + dy
            G += T.tapered([(xs, ys, xs + (xe - xs) * p, ys + (ye - ys) * p, 1.0)], 0.045) * (1 - rel(u, 0.75, 1)) * 1.5
            H += T.lines([(xs, ys, xs + (xe - xs) * p, ys + (ye - ys) * p, 1.0)], 0.007) * (1 - rel(u, 0.75, 1)) * 1.2
    g, h = clarao(T, t, 0.25, 0.45, 0.4, 0.0, 1.0)
    G, H = G + g, H + h
    q = np.random.default_rng(4)
    for j in range(8):
        x0 = q.uniform(0.2, 0.65)
        u = rel(t, 0.35 + 0.02 * j, 0.9)
        if 0 < u < 1:
            g2, h2 = cheio(T, poe(GOTA, x0, -0.05 + 0.4 * u * u, 0.045), (1 - rel(u, 0.7, 1)) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


def investida_do_cla(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(6):
        a = math.pi * (0.6 + 0.8 * j / 5) + math.pi
        u = rel(t, 0.03 * j, 0.3 + 0.03 * j)
        if 0 < u < 1:
            r0 = 0.9
            r = r0 * (1 - ease_in(u, 1.6)) + 0.08
            x0, y0 = 0.45 + r0 * math.cos(a), 0.45 * r0 * math.sin(a)
            x, y = 0.45 + r * math.cos(a), 0.45 * r * math.sin(a)
            G += T.tapered([(x0 + (x - x0) * 0.3, y0 + (y - y0) * 0.3, x, y, 1.0)], 0.1) * 1.3
            G += T.gauss(x, y, 0.07) * 1.0
    g, h = clarao(T, t, 0.3, 0.55, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.32, 0.8, 14, 4, 0.45, 0.0, 0.45, 0.013)
    return G * env, H * env


def shredder_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.0, 0.15, 2.0, -math.pi / 2)
    G += P * 0.85
    H += nos * 0.3
    for j in range(3):
        x = -0.1 + 0.1 * j
        G += T.tapered([(x, -0.0, x, -0.5, 1.0)], 0.025) * 1.2
    u = (t * 2) % 1
    H += T.gauss(-0.1 + 0.2 * u, -0.5 + 0.4 * u, 0.02) * 2.0
    G += T.gauss(0, -0.2, 0.25) * (0.3 + 0.15 * math.sin(t * 12))
    return G, H


def golpe_do_mestre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(9)
    for j in range(9):
        a0 = 0.03 + 0.06 * j
        ang = q.uniform(-1.3, 1.3)
        g, h = corte(T, t, a0, a0 + 0.2, ang, 1.0, 0.06, 0.4 + q.normal(0, 0.05), q.normal(0, 0.06))
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.5, 0.75, 0.4, 0.0, 1.4, 1.4)
    G, H = G + g2, H + h2
    u = rel(t, 0.55, 0.95)
    if 0 < u < 1:
        G += T.ring(0.08 + 0.5 * ease_out(u, 2), 0.035 * (1 - 0.5 * u), 0.4, 0.0) * (1 - u) * 1.3
    G += estouro(T, t, 0.55, 0.95, 16, 5, 0.4, 0.0, 0.55, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Mestre Splinter

def postura_do_rato(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.5), 2)
    if u > 0:
        pts = []
        for m in range(40):
            v = u * m / 39
            a = math.pi / 2 + TAU * v * 0.95
            pts.append((0.38 * math.cos(a), 0.05 + 0.38 * 0.5 * math.sin(a) + 0.0))
        G += T.polyline(pts, 0.022) * (1 - rel(t, 0.88, 1)) * 1.2
    g, h = aura(T, t, 0.0, 1.0, 0.35, 0.0, 0.9)
    G, H = G + g, H + h
    q = np.random.default_rng(4)
    for j in range(8):
        w = ((t * 0.8 + j / 8) % 1)
        x = q.uniform(-0.5, 0.5)
        G += T.gauss(x + 0.1 * math.sin(w * 6 + j), -0.7 + 1.0 * w, 0.015) * pulso(t, 0.1, 1.0) * (1 - w) * 1.4
    G += anel(T, t, 0.3, 0.85, 0.1, 0.55, 0.025, 0.0)
    return G * env, H * env


def redirecionar_splinter(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.6)
    a = t * 22
    G += T.lines([(-0.2 + 0.3 * math.cos(a), 0.3 * math.sin(a) * 0.6, -0.2 - 0.3 * math.cos(a), -0.3 * math.sin(a) * 0.6, 1.0)], 0.025) * k * 1.3
    G += T.ring(0.3, 0.02, -0.2, 0.0, 0.6) * k * 0.8
    u = rel(t, 0.05, 0.3)
    if 0 < u < 1:
        x = 0.8 - 0.8 * u
        G += T.tapered([(x + 0.25, -0.05, x, 0.0, 1.0)], 0.05) * 1.2
    g, h = clarao(T, t, 0.28, 0.45, 0.05, 0.0, 0.8)
    G, H = G + g, H + h
    w = rel(t, 0.32, 0.6)
    if 0 < w < 1:
        x = 0.05 + 0.6 * ease_out(w)
        G += T.tapered([(x - 0.3, 0.0, x, -0.05, 1.0)], 0.06) * 1.3
    g2, h2 = clarao(T, t, 0.55, 0.72, 0.65, -0.05, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.55, 0.9, 10, 3, 0.65, -0.05, 0.35, 0.012)
    return G * env, H * env


def licao_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        a = -2.4 + 1.3 * u
        px, py = -0.1, 0.4
        hx, hy = px + 0.8 * math.cos(a), py + 0.8 * math.sin(a)
        G += T.lines([(px, py, hx, hy, 1.0)], 0.022) * k * 1.3
        G += T.arc_band(0.08, 0.02, a - 1.5, a + 1.5, 1.0, 0, hx + 0.06 * math.cos(a), hy + 0.06 * math.sin(a), 0.0) * k * 1.2
    g, h = clarao(T, t, 0.28, 0.48, 0.45, -0.25, 1.1, 1.3)
    G, H = G + g, H + h
    s = surge(t, 0.32, 0.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(0.45, -0.75, 0.45, -0.55 * s - 0.05 - 0.15, 1.0)], 0.03) * 1.4
        G += T.gauss(0.45, -0.48, 0.03) * s * 1.6
    g2, h2 = _tontas(T, t, 0.4, 1.0, 0.45, -0.3, 4, 0.15, 0.04)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Krang

def _cerebro(T, cx, cy, s, k, t):
    if k <= 0:
        return 0.0, 0.0
    pts = [(cx + s * math.cos(a) * (1 + 0.08 * math.sin(a * 7)), cy + s * 0.7 * math.sin(a) * (1 + 0.08 * math.sin(a * 7))) for a in np.linspace(0, TAU, 40, endpoint=False)]
    g, h = icone(T, pts, k * 1.1, 0.5)
    rugas = []
    for j in range(4):
        y = cy - s * 0.4 + s * 0.27 * j
        rugas += [(cx - s * 0.6 + s * 0.3 * m, y + s * 0.07 * math.sin(m * 2 + j + t * 4), cx - s * 0.3 + s * 0.3 * m, y - s * 0.07 * math.sin(m * 2 + j + t * 4), 1.0)
                  for m in range(4)]
    return g + T.lines(rugas, s * 0.04) * k * 1.1, h


def comando_remoto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    g, h = _cerebro(T, -0.45, -0.1, 0.16 * s, 1.0 if s > 0 else 0, t)
    G, H = G + g, H + h
    for j in range(3):
        v = ((t * 2) + j / 3) % 1
        G += T.arc_band(0.1 + 0.6 * v, 0.02, -0.5, 0.5, 1.0, 0, -0.45, -0.1, 0.0) * (1 - v) * pulso(t, 0.1, 0.8) * 1.2
    m = surge(t, 0.35, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        hexa = [(0.45 + 0.28 * m * math.cos(TAU * j / 6), 0.0 + 0.28 * m * math.sin(TAU * j / 6)) for j in range(6)]
        g2, h2 = icone(T, hexa, 1.1, 0.35)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.4, 0.55, 0.45, 0.0, 0.6)
    return (G + g3) * env, (H + h3) * env


def krang_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = _cerebro(T, 0.0, 0.0, 0.2 * (1 + 0.06 * b), 1.0 + 0.3 * b, t)
    G, H = G + g, H + h
    G += T.ring(0.28, 0.02, 0, 0.0, 0.8) * 1.0
    G += T.gauss(0, 0, 0.3) * (0.3 + 0.2 * b)
    return G, H


def dimensao_x(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.75, 0.95))
    if abre > 0:
        for j in range(5):
            a = t * 9 + TAU * j / 5
            G += T.arc_band(0.45 * abre * (1 - 0.15 * j), 0.04, a, a + 2.5, 0.55, 0, 0.0, 0.0, 1.0) * 1.2
        G += T.gauss(0, 0, 0.3 * abre + 0.01, 0.18 * abre + 0.01) * 0.9
        H += T.gauss(0, 0, 0.05) * abre * 1.5
    G += converge(T, t, 0.2, 0.75, 22, 5, 0.0, 0.0, 0.9)
    for x in (-0.55, 0.0, 0.55):
        g, h = clarao(T, t, 0.45, 0.62, x, 0.05, 0.45)
        G, H = G + g, H + h
    g2, h2 = _tontas(T, t, 0.55, 1.0, 0.0, -0.35, 5, 0.3, 0.04)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Casey Jones

def _taco(T, px, py, a, s, k):
    hx, hy = px + s * math.cos(a), py + s * math.sin(a)
    G = T.lines([(px, py, hx, hy, 1.0)], 0.035) * k * 1.4
    pe = a + math.pi / 2
    G = G + T.lines([(hx, hy, hx + 0.18 * s * math.cos(pe) + 0.05 * s * math.cos(a), hy + 0.18 * s * math.sin(pe) + 0.05 * s * math.sin(a), 1.0)],
                    0.055) * k * 1.3
    return G


def taco_de_hoquei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        a = -2.2 + 2.0 * u
        G += _taco(T, -0.5, -0.1, a, 0.55, k)
    w = rel(t, 0.22, 0.45)
    if 0 < w < 1:
        x = -0.1 + 0.6 * w
        g, h = cheio(T, poe(circulo(16), x, 0.15, 0.05, 0), 1.4)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.3, 0.15, x, 0.15, 1.0)], 0.04) * 0.9
    g2, h2 = clarao(T, t, 0.42, 0.6, 0.5, 0.15, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.43, 0.85, 12, 3, 0.5, 0.15, 0.4, 0.012)
    return G * env, H * env


def sequencia_bruta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(6):
        a0 = 0.04 + 0.11 * j
        k = pulso(t, a0, a0 + 0.14)
        if k > 0:
            if j % 2 == 0:
                G += _taco(T, 0.05, 0.25, -1.2 - 0.6 * (j % 4 == 0), 0.45, k)
            else:
                P, nos = _punho(T, 0.25, -0.1 + 0.1 * (j % 3), 1.6, 0)
                G += P * 0.9 * k
                H += nos * 0.35 * k
        g, h = clarao(T, t, a0 + 0.06, a0 + 0.16, 0.45, -0.05 + 0.06 * (j % 3), 0.45)
        G, H = G + g, H + h
    G += anel(T, t, 0.7, 0.98, 0.1, 0.55, 0.03, 0.0)
    return G * env, H * env


def gooool(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.2), 2)
    k = 1 - rel(t, 0.35, 0.5)
    if k > 0:
        G += _taco(T, -0.6, -0.3, -2.4 + 2.2 * u, 0.5, k)
    w = rel(t, 0.18, 0.4)
    if 0 < w < 1:
        x = -0.3 + 0.85 * ease_in(w, 1.3)
        g, h = cheio(T, poe(circulo(16), x, 0.15, 0.055), 1.5)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.45, 0.15, x, 0.15, 1.0)], 0.06) * 1.1
    s = surge(t, 0.3, 0.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        rede = [(0.45, 0.35, 0.45, -0.05 - 0.2 * s, 1.0), (0.85, 0.35, 0.85, -0.05 - 0.2 * s, 1.0), (0.45, -0.05 - 0.2 * s, 0.85, -0.05 - 0.2 * s, 1.0)]
        rede += [(0.45 + 0.08 * m, -0.25 * s - 0.05, 0.45 + 0.08 * m, 0.35, 0.4) for m in range(1, 5)]
        rede += [(0.45, 0.35 - 0.1 * m, 0.85, 0.35 - 0.1 * m, 0.4) for m in range(1, 4)]
        G += T.lines(rede, 0.008) * 1.3
    g2, h2 = clarao(T, t, 0.38, 0.6, 0.6, 0.15, 1.4, 1.4)
    G, H = G + g2, H + h2
    G += particulas(T, t, 0.4, 1.0, 26, 6, 0.6, 0.0, 0.5, 0.6, 0.013)
    G += anel(T, t, 0.4, 0.85, 0.1, 0.7, 0.04, 0.1)
    return G * env, H * env


REGISTRO = [
    ("emboscada_do_tom", emboscada_do_tom, GRANDE, "Tom · a frigideira e a marca", False),
    ("perseguicao", perseguicao, GRANDE, "Tom · as pegadas e a poeira da perseguição", False),
    ("tom_preparo", tom_preparo, MEDIA, "Tom · as unhas afiando (Preparo, laço)", True),
    ("pata_certeira", pata_certeira, GRANDE, "Tom · os três arranhões e a marca da pata", False),
    ("ratoeira_invertida", ratoeira_invertida, GRANDE, "Jerry · a ratoeira fechando", False),
    ("esconderijo", esconderijo, GRANDE, "Jerry · o buraquinho na parede", False),
    ("martelada", martelada, GRANDE, "Jerry · o martelo enorme e as estrelinhas", False),
    ("passo_silencioso", passo_silencioso, GRANDE, "Pantera Cor-de-Rosa · as pegadas e o som riscado", False),
    ("troca_discreta", troca_discreta, GRANDE, "Pantera Cor-de-Rosa · as silhuetas trocando", False),
    ("sumico", sumico, GRANDE, "Pantera Cor-de-Rosa · a fumaça e as interrogações", False),
    ("garras_de_aco", garras_de_aco, GRANDE, "Destruidor · os três riscos da manopla", False),
    ("investida_do_cla", investida_do_cla, GRANDE, "Destruidor · os ninjas do Clã convergindo", False),
    ("shredder_preparo", shredder_preparo, MEDIA, "Destruidor · a manopla erguida (Preparo, laço)", True),
    ("golpe_do_mestre", golpe_do_mestre, GRANDE, "Destruidor · a rajada de cortes", False),
    ("postura_do_rato", postura_do_rato, GRANDE, "Mestre Splinter · o rabo em círculo e a meditação", False),
    ("redirecionar_splinter", redirecionar_splinter, GRANDE, "Mestre Splinter · a bengala desviando o golpe", False),
    ("licao_final", licao_final, GRANDE, "Mestre Splinter · a bengalada e as estrelinhas", False),
    ("comando_remoto", comando_remoto, GRANDE, "Krang · as ondas do cérebro e o escudo", False),
    ("krang_preparo", krang_preparo, MEDIA, "Krang · o cérebro pulsando (Preparo, laço)", True),
    ("dimensao_x", dimensao_x, GRANDE, "Krang · o portal roxo da Dimensão X", False),
    ("taco_de_hoquei", taco_de_hoquei, GRANDE, "Casey Jones · o taco e o disco", False),
    ("sequencia_bruta", sequencia_bruta, GRANDE, "Casey Jones · o taco e os socos", False),
    ("gooool", gooool, GRANDE, "Casey Jones · a tacada, o disco e a rede", False),
]
