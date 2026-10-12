"""Rodada 9 das Mecânicas únicas ativando como habilidade: Cheetara, Mumm-Ra, Homer, Bart, Peter, Stewie, Cartman,
Bill Cipher, Plankton, Macaco Louco, Capitão Planeta, Danny Phantom, Coragem, Senhor Frio, Hera Venenosa, Homem de
Gelo, Gengar, Tenshinhan, Deidara, Violeta, Orihime, Aerith, Katara, Sailor Mercury, Kurama e Ken.

- sem_folego: os riscos da corrida param e as gotas de suor e o bafo de cansaço aparecem.
- mais_poder: as faixas de múmia giram para cima e os olhos vermelhos acendem.
- soneca: a rosquinha gira, a bolha do ronco cresce e os Z sobem.
- nao_fui: o skate passa riscando e a seta aponta para outro.
- galo: a nuvem de briga com as penas voando e as estrelas.
- encolher: o raio de encolher com os anéis e o alvo diminuindo.
- chantagem: o envelope abre e as moedas caem.
- acordo: o triângulo de um olho acende e o fogo azul do aperto de mão.
- formula: o frasco da fórmula voa para longe e o olho do Plankton brilha.
- robo_quebrou: as placas, parafusos e molas do robô voam.
- cinco_aneis: os cinco raios dos anéis se juntam no planeta.
- lamento: as ondas do Lamento fantasma saem em arco.
- aaaah: a boca enorme do grito e as linhas de susto.
- coracao_gelo: o coração de gelo com as rachaduras de geada e o raio frio.
- plantas: as vinhas crescem em espiral com as folhas e os esporos.
- pele_gelo: a armadura de cristais de gelo cresce sobre o corpo.
- fantasma: a bola sombria, o sorriso e os olhos do Gengar.
- kikoho: o triângulo das mãos e a rajada que esmaga.
- katsu: os pássaros de argila voam e explodem (a arte é uma explosão).
- sumiu: a bolha do campo de força e a silhueta que some.
- rejeitar: o escudo de luz das Seis Flores e as pétalas.
- ultima_oracao: a matéria branca desce, a coluna de luz e as pétalas sobem.
- dobra_sangue: os fios que puxam como marionete e as gotas girando.
- analise: o visor e a grade de análise sobre o rival.
- semente: a rosa, a semente que brota e o chicote de espinhos.
- parry: o lampejo azul do parry e o Shoryuken em chamas.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda
from .unicas_b import _silhueta
from .unicas_kit import (CHAMA, CORACAO, DIAMANTE, FOLHA, GOTA, MOEDA, PENA, anel, aura, cheio, chuva, circulo, clarao,
                         converge, corte, estouro, estrela_pts, flor, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _z(cx, cy, s):
    return [(cx - s, cy - s), (cx + s, cy - s), (cx - s, cy + s), (cx + s, cy + s)]


def sem_folego(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(3)
    corre = 1 - rel(t, 0.25, 0.4)
    if corre > 0:
        segs = []
        for j in range(10):
            y = q.uniform(-0.4, 0.4)
            x = q.uniform(-0.8, 0.2) + t * 3
            segs.append((x - 0.5, y, x, y, 1.0))
        G += T.tapered(segs, 0.02) * corre * 1.1
    for j in range(3):
        u = rel(t, 0.35 + 0.08 * j, 0.85 + 0.05 * j)
        if 0 < u < 1:
            x = (-0.25, 0.22, 0.05)[j]
            g, h = icone(T, poe(GOTA, x + 0.05 * u, -0.45 + 0.3 * u, 0.09), (1 - rel(u, 0.8, 1)) * 1.2, 0.5)
            G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.4 + 0.15 * j, 0.7 + 0.15 * j)
        if 0 < u < 1:
            G += T.gauss(0.25 + 0.3 * u, -0.15 - 0.1 * u, 0.04 + 0.08 * u) * (1 - u) * 0.9
    return G * env, H * env


def mais_poder(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.82, 1)
    for j in range(4):
        u = ease_out(rel(t, 0.0 + 0.06 * j, 0.6 + 0.06 * j), 1.5)
        if u > 0:
            pts = _espiral(0, 0.3 - 0.8 * u, 0.15, 0.4, 0.8, TAU * j / 4 + t * 6, 20)
            pts = [(x, y + 0.8 * (i / 20) * u) for i, (x, y) in enumerate(pts)]
            G += T.polyline(pts, 0.04) * k * 0.9
            H += T.polyline(pts, 0.008) * k * 0.4
    olhos = pulso(t, 0.4, 1.0)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.07, -0.35, 0.03, 0.018) * olhos * 2.5
        G += T.gauss(lado * 0.07, -0.35, 0.08, 0.05) * olhos * 1.2
    g, h = aura(T, t, 0.2, 1.0, 0.35, 0, 0.9)
    return (G + g) * env, (H + h) * env


def soneca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.45, 0.6))
    if s > 0:
        G += T.ring(0.25 * s, 0.1 * s + 0.001, 0, 0, 1.0) * 1.1
        q = np.random.default_rng(5)
        segs = []
        for j in range(12):
            a = q.uniform(0, TAU) + t * 4
            r = 0.25 * s
            segs.append((r * math.cos(a), r * math.sin(a), r * math.cos(a) + 0.03 * math.cos(a * 3), r * math.sin(a) + 0.03 * math.sin(a * 3), 1.0))
        H += T.lines(segs, 0.012) * 1.4
    bolha = rel(t, 0.4, 0.9)
    if 0 < bolha < 1:
        r = 0.05 + 0.18 * math.sin(math.pi * bolha)
        G += T.ring(r, 0.012, 0.15, -0.25) * 1.3
        H += T.gauss(0.15 - r * 0.4, -0.25 - r * 0.4, r * 0.2) * 0.8
    for j in range(3):
        u = rel(t, 0.45 + 0.1 * j, 0.95)
        if 0 < u < 1:
            G += T.polyline(_z(-0.15 - 0.1 * j, -0.3 - 0.4 * u, 0.05 + 0.02 * j), 0.02) * (1 - u) * 1.4
    return G * env, H * env


def nao_fui(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.5)
    if 0 < u < 1:
        x = -1.0 + 2.0 * ease_in(u, 1.2)
        skate = [(x - 0.38, 0.22), (x + 0.38, 0.22), (x + 0.45, 0.15), (x + 0.38, 0.28), (x - 0.38, 0.28), (x - 0.45, 0.15)]
        g, h = cheio(T, skate, 1.2)
        G, H = G + g, H + h
        for wx in (-0.15, 0.15):
            G += T.ring(0.05, 0.018, x + wx * 1.7, 0.34) * 1.2
        G += T.tapered([(x - 0.6, 0.27, x - 0.25, 0.27, 0.8)], 0.04)
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = cheio(T, poe([(1, 0), (0.3, -0.5), (0.3, -0.18), (-1, -0.18), (-1, 0.18), (0.3, 0.18), (0.3, 0.5)], 0.3, -0.25, 0.2 * s), 1.3)
        G, H = G + g, H + h
    G += particulas(T, t, 0.05, 0.6, 20, 7, 0, 0.3, 0.6, 0.1, 0.012)
    return G * env, H * env


def galo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.85)
    q = np.random.default_rng(int(t * 20) % 4 + 1)
    pts = [(q.normal(0, 0.22), q.normal(0, 0.15), q.uniform(0.4, 1)) for _ in range(30)]
    G += T.splats(pts, 0.07) * k * 0.7
    for j in range(4):
        a = q.uniform(0, TAU)
        d = q.uniform(0.2, 0.35)
        G += T.lines([(d * math.cos(a), d * math.sin(a), (d + 0.15) * math.cos(a), (d + 0.15) * math.sin(a), 1.0)], 0.03) * k
    for j in range(3):
        g, h = cheio(T, poe(estrela_pts(5, 0.45), q.uniform(-0.3, 0.3), q.uniform(-0.25, 0.25), 0.07), k * 1.3)
        G, H = G + g, H + h * 2
    g, h = chuva(T, t, 0.2, 1.0, PENA, 10, 9, 0.06, -0.3, 0.45, 0.7, 4.0, 1.0)
    return (G + g) * env, (H + h) * env


def encolher(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        G += T.lines([(-0.9, -0.1, -0.9 + 0.9 * ease_out(u), -0.05, 1.0)], 0.03) * 0.9
        for j in range(6):
            x = -0.9 + 0.15 * j + 0.15 * ((t * 6) % 1)
            if x < -0.9 + 0.9 * ease_out(u):
                G += T.ring(0.05, 0.012, x, -0.1 + 0.05 * (x + 0.9) / 0.9, 0.4) * 1.2
    encolhe = ease_in(rel(t, 0.4, 0.8), 2)
    k = 1 - rel(t, 0.85, 1)
    if t > 0.35:
        r = 0.35 * (1 - 0.6 * encolhe)
        G += T.ring(r, 0.025, 0, -0.05) * 1.3 * k + T.gauss(0, -0.05, r * 0.6) * 0.3 * k
        for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.tapered([(1.6 * r * math.cos(a), -0.05 + 1.6 * r * math.sin(a), 1.15 * r * math.cos(a), -0.05 + 1.15 * r * math.sin(a), 1.0)], 0.04) * k
    return G * env, H * env


def chantagem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    abre = ease_out(rel(t, 0.25, 0.45), 2)
    if s > 0:
        w, h0 = 0.3 * s, 0.2 * s
        corpo = [(-w, -h0 - 0.1), (w, -h0 - 0.1), (w, h0 - 0.1), (-w, h0 - 0.1)]
        g, h = icone(T, corpo, 1.1, 0.35)
        G, H = G + g, H + h
        aba_y = -h0 - 0.1 + (0.16 * s) * (1 - 2 * abre)
        G += T.polyline([(-w, -h0 - 0.1), (0, aba_y), (w, -h0 - 0.1)], 0.02) * 1.2
        if abre > 0.5:
            H += T.gauss(0, -0.3, 0.04) * abre * 1.5
    g, h = chuva(T, t, 0.35, 1.0, MOEDA, 10, 7, 0.05, -0.8, 0.4, 0.6, 0.0, 1.0)
    return (G + g) * env, (H + h) * env


def acordo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.85, 1))
    if s > 0:
        tri = [(0, -0.6 * s - 0.05), (0.42 * s, 0.15), (-0.42 * s, 0.15)]
        g, h = icone(T, tri, 1.2, 0.3)
        G, H = G + g, H + h
        for j in range(4):
            y = 0.15 - 0.05 * j * s
            G += T.lines([(-0.35 * s + 0.04 * j * s, -0.05 - 0.04 * j, 0.35 * s - 0.04 * j * s, -0.05 - 0.04 * j, 1.0)], 0.006) * 0.6
        olho = [(0.1 * s * math.cos(a), -0.2 * s + 0.05 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        G += T.polyline(olho + [olho[0]], 0.012) * 1.3
        H += T.gauss(0, -0.2 * s, 0.025 * s + 0.001) * 2 * s
        G += T.ring(0.65 * s, 0.015, 0, -0.1) * 0.8
    fogo = pulso(t, 0.35, 0.95)
    if fogo > 0:
        for j in range(7):
            a = -math.pi / 2 + (j - 3) * 0.25
            g, h = icone(T, poe(CHAMA, 0.55 * math.cos(a), 0.4 + 0.15 * math.sin(a) + 0.3, 0.1 * (1 + 0.15 * math.sin(t * 40 + j))), fogo * 1.1, 0.6)
            G, H = G + g, H + h
    return G * env, H * env


def formula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.15, 0.65)
    x = 0.45 - 1.0 * ease_in(u, 1.5) if u > 0 else 0.45
    y = -0.1 - 0.3 * math.sin(math.pi * u)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        frasco = [(-0.04, -0.2), (0.04, -0.2), (0.04, -0.1), (0.11, -0.02), (0.11, 0.18), (-0.11, 0.18), (-0.11, -0.02), (-0.04, -0.1)]
        g, h = icone(T, poe(frasco, x, y, 2.2 * s, u * 3), 1.2, 0.4)
        G, H = G + g + T.gauss(x, y + 0.08, 0.1) * 0.5 * s, H + h
    olho = pulso(t, 0.55, 1.0)
    if olho > 0:
        G += T.ring(0.12, 0.02, -0.55, -0.35, 1.2) * olho * 1.3
        H += T.gauss(-0.55, -0.35, 0.035) * olho * 2
        G += T.gauss(-0.55, -0.35, 0.07) * olho
    return G * env, H * env


def robo_quebrou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.0, 0.25, 0, 0, 0.9, 1.3)
    G, H = G + g, H + h
    q = np.random.default_rng(13)
    u = rel(t, 0.1, 0.95)
    if u > 0:
        for j in range(12):
            a = q.uniform(0, TAU)
            v0 = q.uniform(0.5, 0.9)
            x = v0 * math.cos(a) * u
            y = v0 * math.sin(a) * u * 0.8 + 0.9 * u * u
            tipo = j % 3
            k = 1 - rel(u, 0.8, 1)
            if tipo == 0:
                g, h = icone(T, poe([(-1, -0.7), (1, -0.7), (1, 0.7), (-1, 0.7)], x, y, 0.11, a + u * 6), k * 1.2, 0.5)
                G, H = G + g, H + h
            elif tipo == 1:
                G += T.ring(0.05, 0.018, x, y) * k * 1.3 + T.lines([(x - 0.035, y, x + 0.035, y, 1.0)], 0.012) * k
            else:
                mola = [(x + 0.06 * math.sin(m * 2.5 + u * 10), y - 0.1 + 0.02 * m) for m in range(10)]
                G += T.polyline(mola, 0.016) * k * 1.3
    return G * env, H * env


def cinco_aneis(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        a = -math.pi / 2 + TAU * j / 5
        u = ease_out(rel(t, 0.05 * j, 0.4 + 0.05 * j), 2)
        k = 1 - rel(t, 0.55, 0.65)
        x0, y0 = 0.85 * math.cos(a), -0.05 + 0.85 * math.sin(a)
        G += T.ring(0.05, 0.015, x0, y0) * surge(t, 0.0, 0.15) * k * 1.2
        if u > 0:
            G += T.lines([(x0, y0, x0 + (0 - x0) * u, y0 + (-0.05 - y0) * u, 1.0)], 0.025) * k * 1.1
            H += T.gauss(x0 + (0 - x0) * u, y0 + (-0.05 - y0) * u, 0.025) * k * 1.4
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        r = 0.25 * s
        G += T.ring(r, 0.03, 0, -0.05) * 1.3 + T.gauss(0, -0.05, r * 0.8) * 0.4
        G += T.ring(r, 0.012, 0, -0.05, 2.5) * 0.8 + T.ring(r, 0.012, 0, -0.05, 1.3) * 0.6
        G += T.lines([(-r, -0.05, r, -0.05, 1.0)], 0.01) * 0.8
    g, h = clarao(T, t, 0.42, 0.62, 0, -0.05, 0.9)
    return (G + g) * env, (H + h) * env


def lamento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cx, cy = -0.55, -0.1
    for j in range(6):
        u = rel(t, 0.05 + 0.1 * j, 0.55 + 0.1 * j)
        if 0 < u < 1:
            r = 0.1 + 1.2 * u
            G += T.arc_band(r, 0.05 * (1 - u) + 0.015, -0.6, 0.6, 1.0, 0.0, cx, cy, 0.0) * (1 - u) * 1.5
    G += T.gauss(cx, cy, 0.06, 0.08) * pulso(t, 0.0, 0.8) * 1.4
    H += T.gauss(cx, cy, 0.03, 0.04) * pulso(t, 0.0, 0.8) * 1.5
    G += particulas(T, t, 0.2, 1.0, 30, 3, 0.2, 0, 0.5, 0.1, 0.012, 0.3)
    return G * env, H * env


def aaaah(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.75, 0.9))
    treme = 0.02 * math.sin(t * 120)
    if s > 0:
        boca = [(treme + 0.2 * s * math.cos(a), -0.05 + 0.28 * s * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, boca, 1.3, 0.5)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.gauss(lado * 0.12 * s + treme, -0.45, 0.06, 0.07) * 0.9 * s
            H += T.gauss(lado * 0.12 * s + treme, -0.45, 0.02) * 1.5 * s
    k = pulso(t, 0.05, 0.85)
    segs = []
    for j in range(12):
        a = TAU * j / 12 + 0.1 * math.sin(t * 50)
        segs.append((0.4 * math.cos(a), -0.05 + 0.4 * math.sin(a), 0.55 * math.cos(a), -0.05 + 0.55 * math.sin(a), 1.0))
    G += T.lines(segs, 0.02) * k * 1.3
    G += anel(T, t, 0.1, 0.6, 0.2, 0.9, 0.04, -0.05) + anel(T, t, 0.3, 0.8, 0.2, 0.9, 0.03, -0.05)
    return G * env, H * env


def coracao_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.35)
    if 0 < u < 1:
        G += T.lines([(-0.95, -0.05, -0.95 + 0.7 * ease_out(u), -0.05, 1.0)], 0.07) * 0.8
        H += T.lines([(-0.95, -0.05, -0.95 + 0.7 * ease_out(u), -0.05, 1.0)], 0.02)
    s = surge(t, 0.25, 0.55) * (1 - rel(t, 0.85, 1))
    if s > 0:
        g, h = icone(T, poe(CORACAO, 0.05, -0.05, 0.35 * s), 1.2, 0.35)
        G, H = G + g, H + h
        q = np.random.default_rng(7)
        for j in range(6):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0.05, -0.05, 0.05 + 0.3 * s * math.cos(a), -0.05 + 0.3 * s * math.sin(a), 3, 0.3), 0.01) * 1.2
    G += particulas(T, t, 0.3, 1.0, 40, 11, 0.05, -0.05, 0.45, -0.15, 0.012)
    return G * env, H * env


def plantas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    q = np.random.default_rng(15)
    for j in range(5):
        u = ease_out(rel(t, 0.04 * j, 0.55 + 0.04 * j), 1.8)
        if u > 0:
            x0 = -0.5 + 0.25 * j
            pts = [(x0 + 0.15 * math.sin(v * 7 + j) * v, 0.45 - 0.9 * v * u) for v in np.linspace(0, 1, 20)]
            G += T.polyline(pts, 0.025) * k * 1.1
            for m in range(3):
                i = 5 + 5 * m
                if i < len(pts) and v_ok(u, i):
                    px, py = pts[i]
                    g, h = icone(T, poe(FOLHA, px + 0.05, py, 0.06, 0.8 + q.uniform(-0.3, 0.3)), k, 0.5)
                    G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 40, 3, 0, -0.1, 0.55, 0.3, 0.014)
    return G * env, H * env


def v_ok(u, i):
    return u > i / 20


def pele_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(19)
    k = 1 - rel(t, 0.85, 1)
    for j in range(16):
        a = q.uniform(0, TAU)
        r = q.uniform(0.2, 0.35)
        cresce = ease_out(rel(t, 0.03 * j, 0.25 + 0.03 * j), 2.5)
        if cresce > 0:
            cx, cy = r * math.cos(a) * 0.8, 0.0 + r * math.sin(a) * 1.2
            comp = q.uniform(0.1, 0.18) * cresce
            cristal = [(cx, cy), (cx + comp * math.cos(a + 0.25), cy + comp * math.sin(a + 0.25)), (cx + comp * 1.5 * math.cos(a), cy + comp * 1.5 * math.sin(a)),
                       (cx + comp * math.cos(a - 0.25), cy + comp * math.sin(a - 0.25))]
            g, h = icone(T, cristal, k, 0.45)
            G, H = G + g, H + h
    G += T.ring(0.3, 0.02, 0, 0, 0.7) * pulso(t, 0.3, 1.0) * 0.8
    G += particulas(T, t, 0.3, 1.0, 26, 7, 0, 0, 0.4, -0.1)
    return G * env, H * env


def fantasma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    cresce = ease_out(rel(t, 0.0, 0.4), 2)
    k = 1 - rel(t, 0.85, 1)
    if cresce > 0:
        r = 0.3 * cresce
        G += T.ring(r, 0.04, 0, 0) * k * 1.1 + T.gauss(0, 0, r * 0.7) * 0.5 * k
        for j in range(6):
            a = TAU * j / 6 + t * 5
            pts = [((r + 0.15 * v) * math.cos(a + 0.6 * v), (r + 0.15 * v) * math.sin(a + 0.6 * v)) for v in np.linspace(0, 1, 8)]
            G += T.polyline(pts, 0.025 * (1 - 0.0)) * k * 0.8
    sorri = surge(t, 0.35, 0.6) * k
    if sorri > 0:
        boca = [(0.18 * sorri * math.cos(a), 0.05 + 0.1 * sorri * math.sin(a)) for a in np.linspace(0.15, math.pi - 0.15, 16)]
        G += T.polyline(boca, 0.02) * 1.4
        dentes = [(0.18 * sorri * math.cos(a), 0.05 + 0.1 * sorri * math.sin(a), 0.18 * sorri * math.cos(a) * 0.9, 0.05 + 0.1 * sorri * math.sin(a) - 0.04, 1.0) for a in np.linspace(0.4, math.pi - 0.4, 6)]
        G += T.lines(dentes, 0.01) * 1.2
        for lado in (-1, 1):
            olho = [(lado * 0.1 + 0.06 * math.cos(a), -0.12 + 0.03 * math.sin(a) - lado * 0.01 * math.cos(a)) for a in np.linspace(0, TAU, 12, endpoint=False)]
            g, h = cheio(T, olho, 1.2 * sorri)
            G, H = G + g, H + h * 2
    return G * env, H * env


def kikoho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        tri = [(0, -0.55), (0.18 * s, -0.25), (-0.18 * s, -0.25)]
        G += T.polyline(tri + [tri[0]], 0.035) * 1.4
        G += T.gauss(0, -0.35, 0.08) * s * 1.2
        H += T.gauss(0, -0.35, 0.04) * s * 1.5
    u = rel(t, 0.4, 0.8)
    if 0 < u < 1:
        kk = (1 - rel(u, 0.6, 1)) * ease_out(rel(u, 0, 0.15))
        w = 0.35
        G += T.polys([([(-0.12, -0.3), (0.12, -0.3), (w, 0.4), (-w, 0.4)], 1.0)], 0.02) * kk * 1.1
        H += T.polys([([(-0.05, -0.3), (0.05, -0.3), (0.15, 0.4), (-0.15, 0.4)], 1.0)], 0.02) * kk * 1.1
    g, h = clarao(T, t, 0.7, 0.9, 0, 0.4, 1.0, 1.4)
    G += onda_no_chao(T, t, 0.7, 1.0, 0.9, 0.42)
    return (G + g) * env, (H + h) * env


def _passaro(cx, cy, s, bate):
    return [(cx - s, cy - s * 0.5 * bate), (cx - s * 0.3, cy), (cx, cy - s * 0.2), (cx + s * 0.3, cy), (cx + s, cy - s * 0.5 * bate), (cx + s * 0.2, cy + s * 0.25),
            (cx - s * 0.2, cy + s * 0.25)]


def katsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(23)
    for j in range(4):
        u = rel(t, 0.0 + 0.05 * j, 0.45 + 0.05 * j)
        if 0 < u < 1:
            x0, y0 = q.uniform(-0.9, -0.5), q.uniform(-0.6, -0.1)
            x, y = x0 + (0.0 - x0) * ease_in(u, 1.3) + q.uniform(-0.15, 0.15) * u, y0 + (0 - y0) * u
            g, h = icone(T, _passaro(x, y, 0.18, math.sin(t * 40 + j)), 1.3, 0.5)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.48, 0.72, 0, 0, 1.4, 2.0)
    G, H = G + g, H + h
    G += anel(T, t, 0.5, 0.95, 0.1, 1.0, 0.07) + estouro(T, t, 0.5, 0.9, 26, 5, 0, 0, 0.9, 0.016)
    G += particulas(T, t, 0.52, 1.0, 50, 9, 0, 0, 0.6, 0.4, 0.025)
    return G * env, H * env


def sumiu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2.5) * (1 - rel(t, 0.85, 1))
    if s > 0:
        r = 0.45 * s
        G += T.ring(r, 0.03, 0, 0) * 1.3 + T.gauss(0, 0, r * 0.75) * 0.3
        H += T.arc_band(r * 0.8, 0.02, 3.6 + t * 2, 4.4 + t * 2, 1.0, 0.0, 0, 0, 1.0) * 1.2
    some = rel(t, 0.3, 0.8)
    S = T.polys([(_silhueta(0, 0.05, 1.0), 1.0)])
    G += (S * 0.3 + _borda(T, S, 0.008) * 1.1) * (1 - some) * (0.6 + 0.4 * math.sin(t * 60) * (some > 0))
    G += particulas(T, t, 0.35, 0.95, 40, 3, 0, 0.05, 0.25, 0.3, 0.012)
    return G * env, H * env


def rejeitar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.15, 0.5), 2.2) * (1 - rel(t, 0.85, 1))
    for j in range(6):
        a = TAU * j / 6 + t * 4
        r = 0.55 - 0.15 * s
        g, h = cheio(T, poe(flor(5, 1.0, 0.3), r * math.cos(a), -0.05 + r * math.sin(a) * 0.6, 0.06), (1 - rel(t, 0.7, 0.9)) * 1.2)
        G, H = G + g, H + h
    if s > 0:
        tri = [(0, -0.45 * s - 0.05), (0.42 * s, 0.3 * s - 0.05), (-0.42 * s, 0.3 * s - 0.05)]
        g, h = icone(T, tri, 1.1, 0.25)
        G, H = G + g, H + h
        G += T.gauss(0, -0.05, 0.25 * s) * 0.3
    return G * env, H * env


def ultima_oracao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    desce = ease_in(rel(t, 0.0, 0.4), 1.6)
    if t < 0.5:
        y = -0.9 + 0.8 * desce
        G += T.gauss(0, y, 0.07) * 1.4
        H += T.gauss(0, y, 0.03) * 1.6
    coluna = pulso(t, 0.35, 0.95)
    if coluna > 0:
        G += T.gauss(0, -0.2, 0.15, 0.8) * coluna * 0.8
        H += T.gauss(0, -0.2, 0.05, 0.8) * coluna * 0.8
    q = np.random.default_rng(29)
    for j in range(10):
        u = rel(t, 0.4 + q.uniform(0, 0.25), 1.0)
        if 0 < u < 1:
            x = q.uniform(-0.4, 0.4)
            g, h = icone(T, poe(flor(5, 1.0, 0.3), x + 0.05 * math.sin(u * 8), 0.4 - 0.9 * u, 0.05, u * 4), (1 - u) * 1.2, 0.5)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.35, 0.55, 0, -0.1, 0.8)
    return (G + g) * env, (H + h) * env


def dobra_sangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(5):
        x = -0.3 + 0.15 * j
        balanca = 0.03 * math.sin(t * 12 + j)
        G += T.lines([(x + balanca, -1.0, x * 0.6, -0.1 + 0.05 * (j % 2), 1.0)], 0.008) * k * 1.2
        H += T.gauss(x * 0.6, -0.1 + 0.05 * (j % 2), 0.02) * k * 1.4
    for j in range(8):
        a = TAU * j / 8 + t * 8
        g, h = cheio(T, poe(GOTA, 0.4 * math.cos(a), 0.15 + 0.15 * math.sin(a), 0.08, a + math.pi), k * 1.2)
        G, H = G + g, H + h
    return G * env, H * env


def analise(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        visor = [(-0.3 * s, -0.55), (0.3 * s, -0.55), (0.25 * s, -0.45), (-0.25 * s, -0.45)]
        g, h = icone(T, visor, 1.2, 0.45)
        G, H = G + g, H + h
    grade = ease_out(rel(t, 0.25, 0.6), 2) * (1 - rel(t, 0.85, 1))
    if grade > 0:
        segs = []
        for j in range(7):
            v = -0.3 + 0.1 * j
            segs.append((-0.3, v * grade, 0.3, v * grade, 1.0))
            segs.append((v * grade, -0.3, v * grade, 0.3, 1.0))
        G += T.lines(segs, 0.006) * 1.1
        G += T.ring(0.42 * grade, 0.015, 0, 0) * 1.1
    scan = rel(t, 0.4, 0.8)
    if 0 < scan < 1:
        y = -0.3 + 0.6 * scan
        G += T.lines([(-0.35, y, 0.35, y, 1.0)], 0.02) * 1.4
        H += T.lines([(-0.35, y, 0.35, y, 1.0)], 0.006)
    return G * env, H * env


def semente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.35, 0.45))
    g, h = icone(T, poe(flor(6, 1.0, 0.35), 0, -0.3, 0.26 * s, t * 3), s * 1.3, 0.5)
    G, H = G + g, H + h
    brota = ease_out(rel(t, 0.4, 0.8), 2)
    k = 1 - rel(t, 0.88, 1)
    if brota > 0:
        G += T.ring(0.03, 0.015, 0, 0.35) * k * 1.2
        caule = [(0.07 * math.sin(v * 5), 0.4 - 0.85 * v * brota) for v in np.linspace(0, 1, 12)]
        G += T.polyline(caule, 0.04) * k * 1.2
        for lado in (-1, 1):
            if brota > 0.5:
                g, h = icone(T, poe(FOLHA, lado * 0.13, 0.4 - 0.5 * brota, 0.14 * brota, lado * 1.0), k * 1.2, 0.5)
                G, H = G + g, H + h
    chicote = rel(t, 0.15, 0.5)
    if 0 < chicote < 1:
        pts = [(-0.7 + 1.4 * v * ease_out(chicote), -0.1 + 0.1 * math.sin(v * 10 - t * 20)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.025) * (1 - chicote) * 1.4
        for i in range(0, 30, 4):
            G += T.gauss(pts[i][0], pts[i][1], 0.015) * (1 - chicote)
    return G * env, H * env


def parry(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    flash = pulso(t, 0.0, 0.25)
    if flash > 0:
        S = T.polys([(_silhueta(0, 0.05, 1.2), 1.0)])
        G += (S * 0.6 + _borda(T, S, 0.01) * 1.5) * flash
        H += S * 0.5 * flash
    u = ease_out(rel(t, 0.3, 0.8), 1.5)
    if 0 < u < 1:
        y = 0.35 - 0.8 * u
        x = 0.1 + 0.15 * u
        for j in range(8):
            v = j / 8
            g, h = icone(T, poe(CHAMA, x - 0.05 * v, y + 0.4 * v, 0.2 * (1 - 0.6 * v), math.pi * 0.05), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.3, 0.6)
            G, H = G + g, H + h
        G += T.gauss(x, y, 0.08) * 1.2
    g, h = clarao(T, t, 0.55, 0.75, 0.25, -0.6, 0.8)
    return (G + g) * env, (H + h) * env


REGISTRO = [
    ("mu_sem_folego", sem_folego, GRANDE, "Cheetara · a corrida e o fôlego acabando", False),
    ("mu_mais_poder", mais_poder, GRANDE, "Mumm-Ra · as faixas e os olhos vermelhos", False),
    ("mu_soneca", soneca, GRANDE, "Homer · a rosquinha e o ronco", False),
    ("mu_nao_fui", nao_fui, GRANDE, "Bart · o skate e a seta", False),
    ("mu_galo", galo, GRANDE, "Peter · a briga com o galo", False),
    ("mu_encolher", encolher, GRANDE, "Stewie · o raio de encolher", False),
    ("mu_chantagem", chantagem, GRANDE, "Cartman · o envelope e as moedas", False),
    ("mu_acordo", acordo, GRANDE, "Bill Cipher · o olho e o fogo azul", False),
    ("mu_formula", formula, GRANDE, "Plankton · a fórmula roubada", False),
    ("mu_robo_quebrou", robo_quebrou, GRANDE, "Macaco Louco · o robô se desmontando", False),
    ("mu_cinco_aneis", cinco_aneis, GRANDE, "Capitão Planeta · os cinco anéis", False),
    ("mu_lamento", lamento, GRANDE, "Danny Phantom · o Lamento fantasma", False),
    ("mu_aaaah", aaaah, GRANDE, "Coragem · o grito", False),
    ("mu_coracao_gelo", coracao_gelo, GRANDE, "Senhor Frio · o coração de gelo", False),
    ("mu_plantas", plantas, GRANDE, "Hera Venenosa · as vinhas e os esporos", False),
    ("mu_pele_gelo", pele_gelo, GRANDE, "Homem de Gelo · a armadura de cristais", False),
    ("mu_fantasma", fantasma, GRANDE, "Gengar · a bola sombria e o sorriso", False),
    ("mu_kikoho", kikoho, GRANDE, "Tenshinhan · o Kikoho", False),
    ("mu_katsu", katsu, GRANDE, "Deidara · os pássaros de argila: Katsu!", False),
    ("mu_sumiu", sumiu, GRANDE, "Violeta · o campo de força e a silhueta que some", False),
    ("mu_rejeitar", rejeitar, GRANDE, "Orihime · o escudo das Seis Flores", False),
    ("mu_ultima_oracao", ultima_oracao, GRANDE, "Aerith · a Última oração", False),
    ("mu_dobra_sangue", dobra_sangue, GRANDE, "Katara · a dobra de sangue", False),
    ("mu_analise", analise, GRANDE, "Sailor Mercury · o visor e a análise", False),
    ("mu_semente", semente, GRANDE, "Kurama · a rosa e a semente", False),
    ("mu_parry", parry, GRANDE, "Ken · o parry e o Shoryuken", False),
]
