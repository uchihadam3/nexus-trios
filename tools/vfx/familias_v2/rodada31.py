"""Rodada 31 das habilidades próprias: Optimus Prime, Salsicha, Bob Esponja, Scooby-Doo, Finn, Megatron e Docinho.

Optimus Prime
- escudo_de_energon: o escudo hexagonal de energon azul que se monta peça por peça (Protegido e Escudo).
- rifle_ion: o rifle carregando e o feixe azul de íons no rival (Enfraquecido).
- optimus_preparo: o Preparo do Autobots, avante — a Matriz da Liderança acesa no peito (laço).
- autobots_avante: o símbolo Autobot no alto e a onda azul que sobe no trio (Fortalecido, Acelerado e Escudo).

Salsicha
- fuga_desesperada: as pernas girando como roda, a nuvem de poeira e as gotas de suor (Protegido e Acelerado).
- sanduiche_gigante: o sanduíche de muitos andares se montando, camada por camada (Vida e Acelerado).
- correria: a nuvem de poeira atravessando a tela e as pegadas (Protegido, Acelerado e Vida).

Bob Esponja
- espremer: a esponja espremida, a água esguichando e as bolhas protegendo (Vida e Protegido).

Scooby-Doo
- tropeco: o Scooby rolando, as estrelinhas e o ponto de interrogação (Confuso e Marcado).
- biscoito_scooby: o biscoito-osso jogado para o alto, pego no ar, e os corações (Vida e Protegido).
- scooby_preparo: o Preparo da Sorte de cachorro — o Scooby tremendo, as gotas de medo (laço).
- sorte_de_cachorro: a sequência de acidentes: o barril rolando e as caixas caindo em todos (Lento).

Finn
- espada_de_sangue: a espada vermelha do demônio num corte com as gotas (Sangrando).
- punho_heroico: o punho com o brilho do herói e as estrelinhas (Exposto e Fortalecido).
- finn_preparo: o Preparo do Matemático! — a espada no alto e as faíscas coloridas (laço).
- matematico: a explosão de estrelas e cores do "Matemático!" (Exposto).

Megatron
- canhao_de_fusao: o canhão de fusão roxo varrendo todos os rivais (Preso e Exposto).
- dominio_decepticon: o símbolo Decepticon descendo e esmagando o rival (Silenciado).
- megatron_preparo: o Preparo da Rendição — o canhão de fusão carregando a energia roxa (laço).
- rendicao_decepticon: a onda roxa que esmaga todos contra o chão (Silenciado e Enfraquecido).

Docinho
- soco_relampago: o rastro verde e o soco num piscar (Exposto).
- sequencia_furiosa: os socos verdes em sequência, de vários lados (Acelerado).
- explosao_verde: a bola de energia verde que estoura em todos (Exposto).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CORACAO, ESPADA, GOTA, OSSO, anel, aura, cheio, chuva, clarao, converge, corte, estouro, estrela_pts, icone,
                         onda_no_chao, particulas, poe, raios, surge, voa)


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def _estrelas_tontas(T, t, a, b, cx, cy, n=3, r=0.12, s=0.035):
    G, H = 0.0, 0.0
    k = pulso(t, a, b)
    if k <= 0:
        return G, H
    for j in range(n):
        ang = t * 9 + TAU * j / n
        g, h = cheio(T, poe(estrela_pts(5, 0.45), cx + r * math.cos(ang), cy + r * 0.4 * math.sin(ang), s), k * 1.3)
        G, H = G + g, H + h
    return G, H


# ------------------------------------------------------------------ Optimus Prime

def escudo_de_energon(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    centros = [(0.0, 0.0)] + [(0.2 * math.cos(TAU * k / 6 + math.pi / 6), 0.2 * math.sin(TAU * k / 6 + math.pi / 6)) for k in range(6)]
    for j, (x, y) in enumerate(centros):
        s = surge(t, 0.04 * j, 0.04 * j + 0.25)
        if s > 0:
            g, h = icone(T, _hexagono(x, y, 0.115 * s), (1 - rel(t, 0.88, 1)) * 1.1, 0.4)
            G, H = G + g, H + h
    brilho = pulso(t, 0.35, 0.65)
    G += T.ring(0.38, 0.03, 0, 0) * brilho * 1.3
    G += T.gauss(0, 0, 0.4) * 0.35 * pulso(t, 0.2, 1.0)
    G += anel(T, t, 0.3, 0.8, 0.2, 0.7, 0.025, 0.0)
    return G * env, H * env


def rifle_ion(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.3, 12, 4, -0.6, 0.0, 0.35)
    H += T.gauss(-0.6, 0.0, 0.04 + 0.06 * rel(t, 0.0, 0.3)) * pulso(t, 0.0, 0.4) * 2.0
    k = pulso(t, 0.28, 0.75)
    if k > 0:
        G += T.tapered([(-0.6, 0.0, 0.6, 0.0, 1.0)], 0.12 * k + 0.01) * 1.4
        G += T.gauss(0.0, 0.0, 0.6, 0.06) * k * 0.6
        H += T.lines([(-0.6, 0.0, 0.6, 0.0, 1.0)], 0.022) * k * 1.8
        q = np.random.default_rng(int(t * 40))
        for _ in range(3):
            x = q.uniform(-0.5, 0.5)
            G += T.polyline(jagged(q, x, 0.0, x + 0.15, q.choice([-0.12, 0.12]), 3, 0.3), 0.008) * k * 1.2
    g2, h2 = clarao(T, t, 0.3, 0.65, 0.6, 0.0, 0.9)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.32, 0.8, 12, 5, 0.6, 0.0, 0.4, 0.012)
    return G * env, H * env


_AUTOBOT = [(0, -1), (0.35, -0.7), (0.8, -0.85), (0.9, -0.2), (0.6, 0.5), (0.25, 0.9), (0, 0.6), (-0.25, 0.9), (-0.6, 0.5), (-0.9, -0.2),
            (-0.8, -0.85), (-0.35, -0.7)]


def optimus_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = icone(T, poe(GOTA, 0, 0, 0.18, math.pi), 1.0 + 0.3 * b, 0.5)
    G, H = G + g, H + h
    H += T.gauss(0, 0.02, 0.05) * (1.3 + 0.8 * b)
    G += T.gauss(0, 0.0, 0.3) * (0.3 + 0.2 * b)
    G += T.ring(0.3 + 0.1 * ((t * 2) % 1), 0.02, 0, 0) * (1 - (t * 2) % 1) * 1.1
    return G, H


def autobots_avante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.6, 0.8))
    if s > 0:
        g, h = icone(T, poe(_AUTOBOT, 0, -0.45, 0.22 * s), 1.2, 0.45)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.gauss(lado * 0.09 * s, -0.5, 0.025) * s * 1.6
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.3, 0.95)
        G += T.gauss(x, 0.1, 0.18, 0.28) * k * 0.6
        G += particulas(T, t, 0.3, 0.95, 8, int(x * 10) + 20, x, 0.3, 0.15, 0.6, 0.012)
    G += onda_no_chao(T, t, 0.3, 0.85, 0.95, 0.35, 1.5)
    g2, h2 = clarao(T, t, 0.25, 0.45, 0, -0.45, 0.8)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Salsicha

def fuga_desesperada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    a = t * 50
    G += (T.arc_band(0.24, 0.055, a, a + 4.0, 1.0, 0, -0.1, 0.15, 1.0) + T.arc_band(0.24, 0.055, a + math.pi, a + math.pi + 4.0, 1.0, 0, -0.1, 0.15, 1.0)) * k * 1.3
    q = np.random.default_rng(5)
    pts = [(-0.35 - 0.5 * q.uniform(0, 1) * rel(t, 0.0, 0.8), 0.32 + q.normal(0, 0.05), k * q.uniform(0.3, 0.8)) for _ in range(24)]
    G += T.splats(pts, 0.06) * 0.8
    for j in range(5):
        G += T.lines([(-0.3 - 0.1 * j, -0.2 + 0.1 * j, -0.7 - 0.1 * j, -0.2 + 0.1 * j, 1.0)], 0.006) * k * 1.0
    for j in range(3):
        u = ((t * 2.5) + j / 3) % 1
        g, h = icone(T, poe(GOTA, 0.15 + 0.08 * j - 0.1 * u, -0.45 - 0.1 * math.sin(math.pi * u) + 0.2 * u, 0.045), k * (1 - u) * 1.3, 0.6)
        G, H = G + g, H + h
    return G * env, H * env


def sanduiche_gigante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    camadas = 7
    for j in range(camadas):
        u = ease_in(rel(t, 0.05 * j, 0.05 * j + 0.18), 2)
        if u <= 0:
            continue
        y_alvo = 0.3 - 0.085 * j
        y = -0.9 + (y_alvo + 0.9) * u
        larg = 0.3 if j in (0, camadas - 1) else 0.27 + 0.02 * math.sin(j * 3)
        if j in (0, camadas - 1):
            pts = [(larg * math.cos(a), y - 0.06 * math.sin(a) * (1 if j else -1)) for a in np.linspace(0, math.pi, 14)]
        else:
            pts = [(-larg, y - 0.025), (larg, y - 0.025), (larg + 0.02, y + 0.025), (-larg - 0.02, y + 0.025)]
        g, h = icone(T, pts, (1 - rel(t, 0.88, 1)) * 1.1, 0.5)
        G, H = G + g, H + h
    G += T.lines([(0, -0.35, 0, 0.3, 1.0)], 0.008) * pulso(t, 0.4, 1.0) * 0.9
    g2, h2 = clarao(T, t, 0.45, 0.65, 0, -0.1, 0.6)
    G, H = G + g2, H + h2
    G += particulas(T, t, 0.45, 1.0, 16, 7, 0, 0.0, 0.45, 0.6, 0.014)
    return G * env, H * env


def correria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.7)
    x = -0.9 + 1.8 * ease_out(u, 1.3)
    q = np.random.default_rng(4)
    if 0 < u < 1:
        pts = [(x + q.normal(0, 0.12), 0.15 + q.normal(0, 0.12), q.uniform(0.4, 1.0)) for _ in range(30)]
        G += T.splats(pts, 0.07) * 0.9
        for j in range(6):
            G += T.lines([(x - 0.2, -0.1 + 0.08 * j, x - 0.65, -0.1 + 0.08 * j, 1.0)], 0.007) * 1.1
        g, h = _estrelas_tontas(T, t, 0.0, 0.7, x, -0.15, 3, 0.1, 0.03)
        G, H = G + g, H + h
    for j in range(7):
        px = -0.8 + 0.25 * j
        k = pulso(t, 0.08 * j, 0.6 + 0.05 * j)
        G += (T.gauss(px, 0.38, 0.035, 0.018) + T.gauss(px + 0.06, 0.36, 0.012) * 0.6) * k * 1.1
    G += T.gauss(0, 0.1, 0.5, 0.3) * pulso(t, 0.5, 1.0) * 0.35
    return G * env, H * env


# ------------------------------------------------------------------ Bob Esponja

def espremer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    aperta = math.sin(math.pi * rel(t, 0.0, 0.45))
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        w, hh = 0.2 * (1 - 0.45 * aperta), 0.24 * (1 + 0.15 * aperta)
        g, h = icone(T, [(-w, -hh), (w, -hh), (w, hh), (-w, hh)], k * 1.1, 0.45)
        G, H = G + g, H + h
        q = np.random.default_rng(2)
        for _ in range(7):
            G += T.ring(0.02 + q.uniform(0, 0.02), 0.008, q.uniform(-w * 0.8, w * 0.8), q.uniform(-hh * 0.8, hh * 0.8)) * k * 0.9
    for j in range(8):
        a = TAU * j / 8
        u = rel(t, 0.15, 0.55)
        if 0 < u < 1:
            r = 0.15 + 0.45 * ease_out(u, 1.5)
            g, h = cheio(T, poe(GOTA, r * math.cos(a), r * math.sin(a) + 0.15 * u * u, 0.04, a - math.pi / 2), (1 - u) * 1.4)
            G, H = G + g, H + h
    q = np.random.default_rng(6)
    for j in range(10):
        a = TAU * j / 10 + t * 1.5
        s = surge(t, 0.45 + 0.02 * j, 0.65 + 0.02 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            r = 0.36 + 0.04 * math.sin(j * 2)
            G += T.ring(0.05 * s * q.uniform(0.7, 1.2), 0.01, r * math.cos(a), r * math.sin(a)) * 1.3
            H += T.gauss(r * math.cos(a) - 0.015, r * math.sin(a) - 0.015, 0.008) * s * 1.2
    g2, h2 = aura(T, t, 0.4, 1.0, 0.38, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Scooby-Doo

_INTERROGA = [(-0.12, -0.5), (-0.06, -0.62), (0.06, -0.64), (0.14, -0.56), (0.13, -0.46), (0.03, -0.38), (0.02, -0.28)]


def tropeco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.5)
    if 0 < u < 1:
        x = -0.6 + 1.1 * u
        y = 0.2 - 0.3 * math.sin(math.pi * u)
        ang = u * TAU * 1.5
        G += T.arc_band(0.2, 0.065, ang, ang + 4.5, 1.0, 0, x, y, 1.0) * 1.4
        G += T.gauss(x, y, 0.13) * 0.9
    g, h = clarao(T, t, 0.45, 0.65, 0.5, 0.15, 0.8)
    G, H = G + g, H + h
    g2, h2 = _estrelas_tontas(T, t, 0.5, 1.0, 0.5, -0.2, 4, 0.15, 0.04)
    G, H = G + g2, H + h2
    s = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if s > 0:
        pts = [(0.5 + x * s * 2.0, 0.6 + y * s * 2.0) for x, y in _INTERROGA]
        G += T.polyline(pts, 0.032) * 1.4
        G += T.gauss(0.5, 0.6 - 0.16 * s * 2.0, 0.035) * s * 1.6
    return G * env, H * env


def biscoito_scooby(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.5)
    if 0 < u < 1:
        x = -0.45 + 0.45 * u
        y = 0.1 - 0.75 * math.sin(math.pi * u)
        g, h = icone(T, poe(OSSO, x, y, 0.12, u * TAU * 2), 1.3, 0.6)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.48, 0.65, 0.0, 0.1, 0.6)
    G, H = G + g2, H + h2
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.45
        w = rel(t, 0.5 + 0.04 * j, 0.95)
        if 0 < w < 1:
            r = 0.15 + 0.4 * ease_out(w, 1.5)
            g3, h3 = cheio(T, poe(CORACAO, r * math.cos(a), 0.05 + r * math.sin(a), 0.055), (1 - rel(w, 0.7, 1)) * 1.4)
            G, H = G + g3, H + h3
    G += anel(T, t, 0.5, 0.9, 0.1, 0.55, 0.03, 0.05)
    g4, h4 = aura(T, t, 0.5, 1.0, 0.35, 0.05, 0.8)
    return (G + g4) * env, (H + h4) * env


def scooby_preparo(T, t, rng):
    G, H = vazio(T)
    treme = 0.02 * math.sin(t * 60)
    G += T.gauss(treme, 0.0, 0.16, 0.2) * 0.6
    for lado in (-1, 1):
        G += T.lines([(lado * 0.22 + treme, -0.1, lado * 0.3 + treme, -0.18, 1.0), (lado * 0.24 + treme, 0.0, lado * 0.33 + treme, 0.0, 1.0)], 0.01) * 1.1
    for j in range(3):
        u = ((t * 1.8) + j / 3) % 1
        g, h = cheio(T, poe(GOTA, -0.15 + 0.15 * j, -0.3 + 0.35 * u, 0.04), (1 - u) * 1.3)
        G, H = G + g, H + h
    pts = [(x * 0.8 + treme, y * 0.8 + 0.05) for x, y in _INTERROGA]
    G += T.polyline(pts, 0.018) * (1.0 + 0.3 * math.sin(t * 8))
    return G, H


def sorte_de_cachorro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.55)
    if 0 < u < 1:
        x = -0.9 + 1.8 * u
        ang = u * TAU * 3
        G += T.ring(0.11, 0.03, x, 0.25) * 1.3
        G += T.lines([(x + 0.11 * math.cos(ang + k * math.pi / 2), 0.25 + 0.11 * math.sin(ang + k * math.pi / 2), x, 0.25, 1.0) for k in range(4)],
                     0.01) * 1.1
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        w = ease_in(rel(t, 0.25 + 0.1 * j, 0.5 + 0.1 * j), 2)
        k = 1 - rel(t, 0.7 + 0.05 * j, 0.85 + 0.05 * j)
        if w > 0 and k > 0:
            y = -0.9 + 1.0 * w
            g, h = icone(T, [(x - 0.12, y - 0.12), (x + 0.12, y - 0.12), (x + 0.12, y + 0.12), (x - 0.12, y + 0.12)], k * 1.2, 0.4)
            G, H = G + g, H + h
            G += T.lines([(x - 0.12, y - 0.12, x + 0.12, y + 0.12, 1.0), (x + 0.12, y - 0.12, x - 0.12, y + 0.12, 1.0)], 0.008) * k * 0.9
        g2, h2 = clarao(T, t, 0.48 + 0.1 * j, 0.62 + 0.1 * j, x, 0.1, 0.5)
        G, H = G + g2, H + h2
        g3, h3 = _estrelas_tontas(T, t, 0.55 + 0.1 * j, 1.0, x, -0.15, 3, 0.1, 0.03)
        G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Finn

def espada_de_sangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = corte(T, t, 0.05, 0.4, -0.6, 1.8, 0.16, 0.1, 0.0, 0.12)
    G, H = G + g * 1.3, H + h
    G += T.arc_band(0.5, 0.06, -2.2, -0.6, 1.0, 0, 0.0, 0.25, 1.0, True) * pulso(t, 0.1, 0.5) * 1.1
    q = np.random.default_rng(8)
    for j in range(9):
        x0 = q.uniform(-0.3, 0.5)
        u = rel(t, 0.35 + 0.02 * j, 0.85)
        if 0 < u < 1:
            g2, h2 = cheio(T, poe(GOTA, x0, -0.1 + 0.3 * x0 * -0.4 + 0.45 * u * u, 0.055), (1 - rel(u, 0.7, 1)) * 1.4)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.25, 0.45, 0.2, 0.0, 0.7)
    return (G + g3) * env, (H + h3) * env


def punho_heroico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        P, nos = _punho(T, -0.6 + 1.0 * u, 0.0, 2.6, 0)
        G += P * 0.95 * k
        H += nos * 0.5 * k
        G += T.tapered([(-0.9, 0.0, -0.75 + 1.0 * u, 0.0, 1.0)], 0.12) * k * 0.6
    g, h = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.1, 1.3)
    G, H = G + g, H + h
    G += T.ring(0.08 + 0.35 * rel(t, 0.3, 0.7), 0.025, 0.45, 0.0) * pulso(t, 0.3, 0.7) * 1.2
    for j in range(5):
        a = TAU * j / 5 + 0.3
        w = rel(t, 0.32, 0.8)
        if 0 < w < 1:
            r = 0.1 + 0.4 * ease_out(w)
            g2, h2 = cheio(T, poe(estrela_pts(5, 0.45), 0.45 + r * math.cos(a), r * math.sin(a), 0.045, w * 4), (1 - w) * 1.4)
            G, H = G + g2, H + h2
    return G * env, H * env


def finn_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(ESPADA, 0, -0.1, 0.45, 0), 1.1, 0.5)
    G, H = G + g, H + h
    q = np.random.default_rng(int(t * 12))
    for _ in range(6):
        a = q.uniform(0, TAU)
        r = q.uniform(0.15, 0.4)
        g2, h2 = cheio(T, poe(estrela_pts(4, 0.35), r * math.cos(a), -0.4 + r * math.sin(a) * 0.6, 0.035), 1.2)
        G, H = G + g2, H + h2
    H += T.gauss(0, -0.5, 0.04) * (1.4 + 0.5 * math.sin(t * 9))
    return G, H


def matematico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = corte(T, t, 0.0, 0.3, -0.9, 1.4, 0.09, 0.3, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.22, 0.5, 0.35, 0.0, 1.4, 1.5)
    G, H = G + g2, H + h2
    for j in range(12):
        a = TAU * j / 12
        w = rel(t, 0.25, 0.85)
        if 0 < w < 1:
            r = 0.1 + 0.6 * ease_out(w, 2)
            g3, h3 = cheio(T, poe(estrela_pts(5, 0.45), 0.35 + r * math.cos(a), r * 0.75 * math.sin(a), 0.06 * (1.2 if j % 3 == 0 else 0.8), w * 5),
                           (1 - rel(w, 0.7, 1)) * 1.4)
            G, H = G + g3, H + h3
    for j in range(3):
        u = rel(t, 0.25 + 0.07 * j, 0.7 + 0.07 * j)
        if 0 < u < 1:
            G += T.ring(0.05 + 0.55 * ease_out(u, 2), 0.03 * (1 - 0.5 * u), 0.35, 0.0) * (1 - u) * 1.3
    G += particulas(T, t, 0.3, 1.0, 22, 9, 0.35, 0.0, 0.5, 0.4, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Megatron

_DECEPTICON = [(0, -0.4), (0.35, -0.95), (0.8, -0.7), (0.75, 0.0), (0.4, 0.55), (0.15, 0.95), (0, 0.65), (-0.15, 0.95), (-0.4, 0.55),
               (-0.75, 0.0), (-0.8, -0.7), (-0.35, -0.95)]


def canhao_de_fusao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += converge(T, t, 0.0, 0.25, 12, 3, -0.75, 0.0, 0.3)
    H += T.gauss(-0.75, 0.0, 0.05 + 0.06 * rel(t, 0.0, 0.25)) * pulso(t, 0.0, 0.35) * 2.0
    k = pulso(t, 0.22, 0.7)
    if k > 0:
        varre = rel(t, 0.22, 0.6)
        alvo_y = -0.2 + 0.4 * varre
        alvo_x = 0.75 - 0.15 * math.sin(math.pi * varre)
        G += T.tapered([(-0.75, 0.0, alvo_x, alvo_y, 1.0)], 0.1 * k + 0.01) * 1.3
        H += T.lines([(-0.75, 0.0, alvo_x, alvo_y, 1.0)], 0.014) * k * 1.6
    for j, (x, y) in enumerate(((0.65, -0.2), (0.7, 0.0), (0.65, 0.2))):
        g, h = clarao(T, t, 0.3 + 0.12 * j, 0.5 + 0.12 * j, x, y, 0.6)
        G, H = G + g, H + h
    G += estouro(T, t, 0.4, 0.9, 14, 6, 0.65, 0.0, 0.4, 0.012)
    return G * env, H * env


def dominio_decepticon(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.4)
    k = 1 - rel(t, 0.7, 0.88)
    if u > 0 and k > 0:
        y = -0.9 + 0.95 * u
        g, h = icone(T, poe(_DECEPTICON, 0.3, y, 0.26), k * 1.2, 0.45)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(0.3 + lado * 0.1, y - 0.05, 0.02) * k * 2.0
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.3, 0.1, 1.2, 1.4)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.33, 0.85, 0.8, 0.35, 1.5)
    q = np.random.default_rng(3)
    r = ease_out(rel(t, 0.35, 0.6), 2)
    for j in range(5):
        a = math.pi * (j + 0.5) / 5
        pts = [(0.3, 0.35)] + [(0.3 + 0.6 * r * v * math.cos(a) + q.normal(0, 0.02), 0.35 + 0.1 * r * v * math.sin(a)) for v in (0.33, 0.66, 1.0)]
        G += T.polyline(pts, 0.014) * (1 - rel(t, 0.85, 1)) * 1.2
    return G * env, H * env


def megatron_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.35, 0.0, 0.1, 0.0, 1.0)], 0.07) * 0.8
    G += T.ring(0.07, 0.02, 0.12, 0.0) * 1.2
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 10, int(t * 2), 0.12, 0.0, 0.35)
    H += T.gauss(0.12, 0.0, 0.05 + 0.02 * b) * (1.5 + 0.8 * b)
    G += T.gauss(0.12, 0.0, 0.2) * (0.4 + 0.3 * b)
    return G, H


def rendicao_decepticon(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.5, 0.7))
    if s > 0:
        g, h = icone(T, poe(_DECEPTICON, 0, -0.5, 0.22 * s), 1.2, 0.45)
        G, H = G + g, H + h
    desce = ease_in(rel(t, 0.25, 0.5), 2)
    if 0 < desce < 1:
        y = -0.9 + 1.2 * desce
        G += T.gauss(0, y, 1.2, 0.05) * 1.1
        H += T.gauss(0, y, 1.0, 0.012) * 0.8
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.48, 0.68, x, 0.2, 0.6)
        G, H = G + g2, H + h2
        k = pulso(t, 0.5, 1.0)
        G += T.gauss(x, 0.05, 0.14, 0.22) * k * 0.6
        G += T.lines([(x - 0.1, -0.05, x + 0.1, -0.05, 1.0)], 0.012) * k * 0.9
    G += onda_no_chao(T, t, 0.48, 0.95, 1.0, 0.35, 1.6)
    G += raios(T, t, 0.5, 0.85, 5, 4, 0, 0.2, 0.6, 0.01)
    return G * env, H * env


# ------------------------------------------------------------------ Docinho

def soco_relampago(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.5)
    if u > 0:
        k = 1 - rel(t, 0.5, 0.7)
        x = -0.8 + 1.2 * u
        G += T.tapered([(-0.95, 0.05, x, 0.0, 1.0)], 0.1) * k * 0.9
        H += T.lines([(-0.95, 0.05, x, 0.0, 1.0)], 0.008) * k
        P, nos = _punho(T, x, 0.0, 2.2, 0)
        G += P * 0.9 * k
        H += nos * 0.4 * k
    g, h = clarao(T, t, 0.18, 0.4, 0.45, 0.0, 1.0, 1.2)
    G, H = G + g, H + h
    G += estouro(T, t, 0.2, 0.7, 12, 3, 0.45, 0.0, 0.45, 0.013)
    G += T.ring(0.06 + 0.35 * rel(t, 0.2, 0.6), 0.025, 0.45, 0.0) * pulso(t, 0.2, 0.6) * 1.2
    return G * env, H * env


def sequencia_furiosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(7):
        a0 = 0.05 + 0.1 * j
        k = pulso(t, a0, a0 + 0.14)
        ang = math.pi + (j - 3) * 0.45
        x0, y0 = 0.4 + 0.55 * math.cos(ang), 0.55 * math.sin(ang) * 0.6
        if k > 0:
            G += T.tapered([(x0, y0, 0.4 + 0.15 * math.cos(ang), 0.15 * math.sin(ang) * 0.6, 1.0)], 0.07) * k * 1.0
            P, nos = _punho(T, 0.4 + 0.18 * math.cos(ang), 0.18 * math.sin(ang) * 0.6, 1.5, ang + math.pi)
            G += P * 0.85 * k
            H += nos * 0.3 * k
        g, h = clarao(T, t, a0 + 0.08, a0 + 0.18, 0.4, 0.0, 0.45)
        G, H = G + g, H + h
    G += T.gauss(0.4, 0.0, 0.25) * pulso(t, 0.1, 0.9) * 0.4
    G += anel(T, t, 0.7, 0.98, 0.1, 0.6, 0.03, 0.0)
    return G * env, H * env


def explosao_verde(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    cresce = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.35, 0.45)
    if cresce > 0 and k > 0:
        G += T.gauss(0, -0.3, 0.06 + 0.12 * cresce) * 1.4 * k
        H += T.gauss(0, -0.3, 0.03 + 0.05 * cresce) * 1.6 * k
        G += raios(T, t, 0.0, 0.42, 4, 7, 0, -0.3, 0.25 * cresce + 0.05, 0.008)
    g, h = clarao(T, t, 0.38, 0.62, 0, -0.1, 1.6, 1.5)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.38 + 0.08 * j, 0.85 + 0.06 * j, 0.1, 0.95, 0.04, -0.1, 1.0, 1.4)
    G += estouro(T, t, 0.4, 0.95, 20, 8, 0, -0.1, 0.9, 0.014)
    G += onda_no_chao(T, t, 0.45, 0.95, 1.0, 0.35, 1.4)
    return G * env, H * env


REGISTRO = [
    ("escudo_de_energon", escudo_de_energon, GRANDE, "Optimus Prime · o escudo hexagonal de energon", False),
    ("rifle_ion", rifle_ion, GRANDE, "Optimus Prime · o feixe azul de íons", False),
    ("optimus_preparo", optimus_preparo, MEDIA, "Optimus Prime · a Matriz da Liderança acesa (Preparo, laço)", True),
    ("autobots_avante", autobots_avante, GRANDE, "Optimus Prime · o símbolo Autobot e a onda no trio", False),
    ("fuga_desesperada", fuga_desesperada, GRANDE, "Salsicha · as pernas-roda e a poeira", False),
    ("sanduiche_gigante", sanduiche_gigante, GRANDE, "Salsicha · o sanduíche de muitos andares", False),
    ("correria", correria, GRANDE, "Salsicha · a nuvem de poeira e as pegadas", False),
    ("espremer", espremer, GRANDE, "Bob Esponja · a esponja espremida e as bolhas", False),
    ("tropeco", tropeco, GRANDE, "Scooby-Doo · o rolamento e a interrogação", False),
    ("biscoito_scooby", biscoito_scooby, GRANDE, "Scooby-Doo · o biscoito-osso e os corações", False),
    ("scooby_preparo", scooby_preparo, MEDIA, "Scooby-Doo · tremendo de medo (Preparo, laço)", True),
    ("sorte_de_cachorro", sorte_de_cachorro, GRANDE, "Scooby-Doo · o barril e as caixas caindo", False),
    ("espada_de_sangue", espada_de_sangue, GRANDE, "Finn · o corte vermelho e as gotas", False),
    ("punho_heroico", punho_heroico, GRANDE, "Finn · o punho e as estrelinhas", False),
    ("finn_preparo", finn_preparo, MEDIA, "Finn · a espada no alto e as faíscas (Preparo, laço)", True),
    ("matematico", matematico, GRANDE, "Finn · a explosão de estrelas do Matemático!", False),
    ("canhao_de_fusao", canhao_de_fusao, GRANDE, "Megatron · o feixe roxo varrendo os rivais", False),
    ("dominio_decepticon", dominio_decepticon, GRANDE, "Megatron · o símbolo Decepticon esmagando", False),
    ("megatron_preparo", megatron_preparo, MEDIA, "Megatron · o canhão de fusão carregando (Preparo, laço)", True),
    ("rendicao_decepticon", rendicao_decepticon, GRANDE, "Megatron · a onda roxa que esmaga todos", False),
    ("soco_relampago", soco_relampago, GRANDE, "Docinho · o rastro verde e o soco", False),
    ("sequencia_furiosa", sequencia_furiosa, GRANDE, "Docinho · os socos de vários lados", False),
    ("explosao_verde", explosao_verde, GRANDE, "Docinho · a bola verde que estoura", False),
]
