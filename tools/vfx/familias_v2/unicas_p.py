"""Rodada 15 das Mecânicas únicas ativando como habilidade: Jiraiya, Tsunade, Sailor Mars, Steven, Garnet, Johnny
Bravo, Dexter, Aku, Vilgax, Cosmo e Wanda, Steve, Creeper, Pac-Man, Crash, Arthur Morgan, Ellie, Sans, Cuphead,
Dovahkiin, O Cavaleiro, Goro e Yoshi.

- energia_natural: a energia da natureza converge e as marcas do sábio acendem nos olhos.
- byakugo: o losango na testa acende e as linhas do selo correm pelo corpo.
- fogo_sagrado: o selo de fogo de Marte gira e as chamas sobem em círculo.
- escudo_rosa: o escudo de bolha com a estrela rosa no meio.
- futuro: o visor triangular mostra os caminhos e a joia brilha.
- cantada: o topete brilha e os corações (um se parte quando leva o fora).
- dee_dee: o laboratório: o frasco, as engrenagens e o "estouro" dos inventos.
- jogado_ao_futuro: o portal do tempo em espiral puxa o rival.
- armadura_aprende: as placas da armadura de Vilgax se fecham, uma por uma.
- desejo_realizado: as varinhas cruzam e as estrelas da coroa caem.
- crafting: a grade da mesa de trabalho e o bloco de diamante surgindo.
- creeper_boom: o creeper pisca branco e explode em cubos.
- waka: a boca do Pac-Man come as pílulas da fileira.
- aku_aku: a máscara de madeira com as penas, girando.
- dead_eye: a tela fica vermelha, as marcas X e os três tiros.
- suprimentos: a mochila abre e os itens (curativo e munição) saem.
- desviou_sans: o olho azul brilha e o osso passa direto.
- super_carta: as cartas enchem e o parry rosa estoura.
- fus_ro_dah: o grito em ondas e as letras do dragão.
- foco_alma: a alma branca converge e a cura brilha.
- quatro_bracos: os quatro punhos de Goro batendo.
- ovo_yoshi: a língua sai, engole e o ovo pintado aparece.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CARTA, CHAMA, CORACAO, CRUZ, DIAMANTE, GEMA, OSSO, PENA, anel, aura, cheio, chuva, clarao, converge, engrenagem,
                         estouro, estrela_pts, icone, onda_no_chao, particulas, poe, raios, runas, surge)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _quad(cx, cy, s, ang=0.0):
    return poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], cx, cy, s, ang)


def energia_natural(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    G += converge(T, t, 0.0, 0.5, 26, 3, 0, -0.05, 0.85, 0.014)
    g, h = aura(T, t, 0.3, 1.0, 0.36, -0.05, 0.9)
    G, H = G + g, H + h
    s = surge(t, 0.4, 0.6) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.gauss(lado * 0.12, -0.12, 0.05 * s + 0.001, 0.025 * s + 0.001) * 1.4 * s
        H += T.gauss(lado * 0.12, -0.12, 0.018 * s + 0.001) * 2.2 * s
        G += T.lines([(lado * 0.07, -0.05, lado * 0.17, -0.02, 1.0)], 0.02) * s * 1.2
    return G * env, H * env


def byakugo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    g, h = cheio(T, poe(DIAMANTE, 0, -0.45, 0.1 * s, 0), 1.4 * s)
    G, H = G + g, H + h * 2
    corre = ease_out(rel(t, 0.25, 0.75), 2)
    if corre > 0:
        for lado in (-1, 1):
            linha = [(lado * (0.05 + 0.25 * v), -0.4 + 0.9 * v + 0.08 * math.sin(v * 9)) for v in np.linspace(0, corre, 24)]
            G += T.polyline(linha, 0.025) * 1.2 * (1 - rel(t, 0.88, 1))
            H += T.polyline(linha, 0.008) * (1 - rel(t, 0.88, 1))
    G += particulas(T, t, 0.3, 1.0, 30, 5, 0, 0.1, 0.4, 0.5, 0.013)
    g2, h2 = aura(T, t, 0.3, 1.0, 0.4, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


def fogo_sagrado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.18 * s, 0.025, 0, -0.05) * 1.3
        G += T.lines([(0.13 * s, -0.18 * s - 0.05, 0.3 * s, -0.35 * s - 0.05, 1.0), (0.3 * s, -0.35 * s - 0.05, 0.18 * s, -0.35 * s - 0.05, 1.0),
                      (0.3 * s, -0.35 * s - 0.05, 0.3 * s, -0.23 * s - 0.05, 1.0)], 0.025) * 1.3
    for j in range(8):
        a = TAU * j / 8 + t * 3
        k = pulso(t, 0.15 + 0.03 * j, 0.9)
        g, h = icone(T, poe(CHAMA, 0.5 * math.cos(a), -0.05 + 0.32 * math.sin(a), 0.16 * k, 0), k, 0.6)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.25, 0.45, 0, -0.05, 0.6)
    return (G + g2) * env, (H + h2) * env


def escudo_rosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.4) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.ring(0.55 * s, 0.04, 0, 0.0) * 1.2
        G += T.gauss(0, 0, 0.5 * s) * 0.35
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0, 0.0, 0.2 * s, 0), 1.2 * s)
        G, H = G + g, H + h
        H += T.arc_band(0.5 * s, 0.02, -2.4, -1.6, 1.0, 0, 0, 0, 1.0) * 1.2
    G += anel(T, t, 0.0, 0.4, 0.1, 0.55, 0.03, 0.0)
    return G * env, H * env


def futuro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        tri = [(-0.35 * s, -0.25), (0.35 * s, -0.25), (0, -0.25 + 0.15 * s)]
        g, h = icone(T, tri, 1.2, 0.5)
        G, H = G + g, H + h
    corre = ease_out(rel(t, 0.25, 0.7), 2)
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.4
        if corre > 0:
            pts = [(0.9 * v * corre * math.cos(a) + 0.05 * math.sin(v * 10 + j), -0.1 + 0.9 * v * corre * -math.sin(a) * -1) for v in np.linspace(0, 1, 16)]
            G += T.polyline(pts, 0.012) * (1.3 if j == 2 else 0.6) * (1 - rel(t, 0.85, 1))
    for lado in (-1, 1):
        g2, h2 = cheio(T, poe(GEMA, lado * 0.55, 0.2, 0.09 * s, 0), 1.2 * s)
        G, H = G + g2, H + h2 * 1.5
    return G * env, H * env


def cantada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.88, 1))
    if s > 0:
        topete = [(-0.22 * s, -0.2)] + [(-0.22 * s + 0.6 * s * v, -0.2 - s * (0.45 * math.sin(math.pi * v * 0.8) + 0.15 * v)) for v in np.linspace(0.1, 1, 10)] + [(0.3 * s, -0.4 * s - 0.2), (0.22 * s, -0.2)]
        g, h = icone(T, topete, 1.1, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.15, 0.35, 0.15, -0.65, 0.4)
    G, H = G + g2, H + h2
    for j in range(4):
        u = rel(t, 0.3 + 0.08 * j, 0.85 + 0.03 * j)
        if 0 < u < 1:
            x = 0.1 + 0.25 * j - 0.3 + 0.1 * math.sin(u * 6 + j)
            y = 0.1 - 0.6 * u
            g3, h3 = cheio(T, poe(CORACAO, x, y, 0.08 * (1 + 0.3 * math.sin(u * 12)), 0), (1 - rel(u, 0.8, 1)) * 1.3)
            G, H = G + g3, H + h3
    return G * env, H * env


def dee_dee(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for j, (x, y, r, v) in enumerate([(-0.35, -0.1, 0.2, 3), (0.0, -0.3, 0.13, -4), (0.3, 0.0, 0.17, 3.5)]):
        g, h = icone(T, poe(engrenagem(9, 1.0, 0.75), x, y, r * s, t * v), s, 0.4)
        G, H = G + g, H + h
    G += estouro(T, t, 0.5, 0.85, 14, 4, 0, -0.1, 0.7, 0.016)
    g2, h2 = clarao(T, t, 0.5, 0.7, 0, -0.1, 0.8)
    return (G + g2) * env, (H + h2) * env


def jogado_ao_futuro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.88, 1))
    for j in range(3):
        pts = _espiral(0, 0, 0.02, 0.6 * s, 1.6, j * TAU / 3 - t * 9)
        G += T.polyline(pts, 0.025) * 1.2
        H += T.polyline(pts, 0.006) * 0.6
    G += T.gauss(0, 0, 0.12 * s + 0.001) * 0.8
    H += T.gauss(0, 0, 0.05 * s + 0.001) * 1.2
    u = ease_in(rel(t, 0.35, 0.8), 2)
    if 0 < u < 1:
        x, y = 0.7 * (1 - u), -0.1 * (1 - u)
        G += T.gauss(x, y, 0.08 * (1 - u) + 0.001) * 1.2
        G += T.tapered([(x + 0.25 * (1 - u), y, x, y, 0.6)], 0.06)
    g2, h2 = runas(T, t, 0.1, 1.0, 0.7, 10, 0.0, 1.0, -2.0)
    return (G + g2 * 0.6) * env, (H + h2) * env


def armadura_aprende(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(6):
        a = -math.pi / 2 + TAU * j / 6
        u = ease_out(rel(t, 0.05 + 0.08 * j, 0.25 + 0.08 * j), 2)
        if u > 0:
            d = 0.38 + 0.4 * (1 - u)
            placa = poe([(-0.6, -0.3), (0.6, -0.3), (0.45, 0.35), (-0.45, 0.35)], d * math.cos(a), -0.05 + d * math.sin(a), 0.22, a + math.pi / 2)
            g, h = icone(T, placa, (1 - rel(t, 0.88, 1)) * 1.1, 0.5)
            G, H = G + g, H + h
            if u >= 1:
                H += T.gauss(d * math.cos(a), -0.05 + d * math.sin(a), 0.03) * pulso(t, 0.25 + 0.08 * j, 0.4 + 0.08 * j) * 2
    G += anel(T, t, 0.6, 0.95, 0.3, 0.8, 0.03, -0.05)
    return G * env, H * env


def desejo_realizado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        ang = lado * (0.9 - 0.5 * s)
        x0, y0 = lado * 0.45, 0.35
        x1, y1 = x0 - lado * 0.5 * s * math.sin(abs(ang) + 0.3), y0 - 0.55 * s
        G += T.lines([(x0, y0, x1, y1, 1.0)], 0.02) * 1.2
        g, h = cheio(T, poe(estrela_pts(5, 0.45), x1, y1, 0.09 * s, t * 3 * lado), 1.4 * s)
        G, H = G + g, H + h * 2
    g2, h2 = clarao(T, t, 0.3, 0.5, 0, -0.25, 0.7)
    G, H = G + g2, H + h2
    g3, h3 = chuva(T, t, 0.35, 1.0, estrela_pts(5, 0.45), 12, 8, 0.05, -0.4, 0.5, 0.6, 3.0, 1.2)
    return (G + g3) * env, (H + h3) * env


def crafting(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.5, 0.7))
    if s > 0:
        segs = []
        for j in range(4):
            v = -0.3 + 0.2 * j
            segs += [(-0.3 * s, v * s, 0.3 * s, v * s, 1.0), (v * s, -0.3 * s, v * s, 0.3 * s, 1.0)]
        G += T.lines(segs, 0.015) * 1.2
        for j in range(9):
            k = pulso(t, 0.1 + 0.03 * j, 0.55)
            G += T.gauss((-0.2 + 0.2 * (j % 3)) * s, (-0.2 + 0.2 * (j // 3)) * s, 0.05) * k * 0.7
    b = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if b > 0:
        topo = [(0, -0.3 * b), (0.28 * b, -0.15 * b), (0, 0), (-0.28 * b, -0.15 * b)]
        lado_e = [(-0.28 * b, -0.15 * b), (0, 0), (0, 0.3 * b), (-0.28 * b, 0.15 * b)]
        lado_d = [(0.28 * b, -0.15 * b), (0, 0), (0, 0.3 * b), (0.28 * b, 0.15 * b)]
        for f, k in ((topo, 1.4), (lado_e, 1.0), (lado_d, 0.7)):
            g, h = icone(T, f, k, 0.6)
            G, H = G + g, H + h
        G += raios(T, t, 0.5, 0.9, 10, 3, 0, 0, 0.5, 0.012)
    return G * env, H * env


def creeper_boom(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    pisca = 1 if (int(t * 16) % 2 == 0 and t < 0.4) else 0
    s = 1 - rel(t, 0.4, 0.45)
    if s > 0:
        G += cheio(T, _quad(0, -0.05, 0.25 * (1 + 0.15 * rel(t, 0.2, 0.4))), 0.9 + 0.6 * pisca)[0]
        H += T.gauss(0, -0.05, 0.25) * pisca * 1.2
        for lado in (-1, 1):
            G -= T.gauss(lado * 0.1, -0.12, 0.04) * 0.7 * s
        G -= T.gauss(0, 0.05, 0.05, 0.08) * 0.7 * s
    g, h = clarao(T, t, 0.4, 0.6, 0, -0.05, 1.4, 1.6)
    G, H = G + g, H + h
    q = np.random.default_rng(11)
    for j in range(14):
        u = rel(t, 0.42, 1.0)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.8 * ease_out(u, 2) * q.uniform(0.5, 1)
            g2, h2 = cheio(T, _quad(d * math.cos(a), -0.05 + d * math.sin(a) + 0.3 * u * u, 0.04, u * 6 + j), (1 - u) * 1.2)
            G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.42, 0.9, 0.95, 0.38)
    return np.maximum(G, 0) * env, H * env


def waka(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    x = -0.7 + 1.4 * ease_out(rel(t, 0.05, 0.85), 1.2)
    boca = 0.5 * abs(math.sin(t * 22))
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.9, 1))
    if s > 0:
        pac = [(x, -0.05)] + [(x + 0.2 * s * math.cos(a), -0.05 + 0.2 * s * math.sin(a)) for a in np.linspace(boca, TAU - boca, 30)]
        g, h = cheio(T, pac, 1.3)
        G, H = G + g, H + h
    for j in range(7):
        px = -0.45 + 0.2 * j
        if px > x + 0.05:
            r = 0.06 if j == 6 else 0.025
            G += T.gauss(px, -0.05, r) * 1.3 * s
            H += T.gauss(px, -0.05, r * 0.5) * 1.5 * s
    return G * env, H * env


def aku_aku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    ang = 0.15 * math.sin(t * 10)
    if s > 0:
        mascara = [(-0.2, -0.3), (0.2, -0.3), (0.25, 0.1), (0.12, 0.35), (-0.12, 0.35), (-0.25, 0.1)]
        g, h = icone(T, poe(mascara, 0, -0.05, s * 1.1, ang), 1.2, 0.5)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(lado * 0.09 * s, -0.12, 0.03) * 1.8 * s
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * 0.35 + ang
            g2, h2 = icone(T, poe(PENA, 0.5 * s * math.cos(a), -0.05 + 0.5 * s * math.sin(a), 0.14 * s, a + math.pi / 2), 1.0, 0.5)
            G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.2, 1.0, 0.42, -0.05, 0.8)
    G += particulas(T, t, 0.3, 1.0, 26, 4, 0, 0, 0.5, 0.3, 0.012)
    return (G + g3) * env, (H + h3) * env


def dead_eye(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    tinge = pulso(t, 0.0, 0.95)
    G += T.gauss(0, 0, 0.9, 0.7) * 0.25 * tinge
    G += T.ring(0.75, 0.05, 0, 0, 0.75) * 0.5 * tinge
    alvos = [(-0.45, -0.2), (0.0, 0.05), (0.45, -0.25)]
    for j, (x, y) in enumerate(alvos):
        m = surge(t, 0.08 + 0.08 * j, 0.25 + 0.08 * j) * (1 - rel(t, 0.5 + 0.1 * j, 0.6 + 0.1 * j))
        if m > 0:
            G += T.lines([(x - 0.06 * m, y - 0.06 * m, x + 0.06 * m, y + 0.06 * m, 1.0), (x + 0.06 * m, y - 0.06 * m, x - 0.06 * m, y + 0.06 * m, 1.0)], 0.02) * 1.5
        g, h = clarao(T, t, 0.5 + 0.1 * j, 0.62 + 0.1 * j, x, y, 0.35)
        G, H = G + g, H + h
    return G * env, H * env


def suprimentos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        mochila = [(-0.22, 0.05), (0.22, 0.05), (0.25, 0.45), (-0.25, 0.45)]
        g, h = icone(T, [(x * s, y) for x, y in mochila], 1.1, 0.5)
        G, H = G + g, H + h
        G += T.arc_band(0.12 * s, 0.02, math.pi, TAU, 1.0, 0, 0, 0.05, 1.0) * 1.1
    for j, forma in enumerate([CRUZ, _quad(0, 0, 1), CRUZ, _quad(0, 0, 1)]):
        u = ease_out(rel(t, 0.3 + 0.08 * j, 0.7 + 0.08 * j), 2)
        if u > 0:
            a = -math.pi / 2 + (j - 1.5) * 0.5
            x, y = 0.6 * u * math.cos(a), 0.05 + 0.6 * u * math.sin(a)
            g2, h2 = cheio(T, poe(forma, x, y, 0.06, 0), (1 - rel(t, 0.85, 1)) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


def desviou_sans(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    olho = pulso(t, 0.0, 0.85)
    G += T.gauss(-0.1, -0.15, 0.1) * olho * 1.4
    H += T.gauss(-0.1, -0.15, 0.04) * olho * 2.5
    G += T.gauss(-0.1, -0.15, 0.25) * olho * 0.5
    rastro = [(-0.1 - 0.35 * v, -0.15 - 0.12 * v + 0.05 * math.sin(v * 8 + t * 20), 1 - v) for v in np.linspace(0, 1, 14)]
    G += T.splats(rastro, 0.04) * olho * 0.9
    u = rel(t, 0.15, 0.6)
    if 0 < u < 1:
        x = 0.9 - 1.8 * u
        g, h = icone(T, poe(OSSO, x, 0.15, 0.3, 0), 1.3, 0.6)
        G, H = G + g, H + h
        G += T.tapered([(x + 0.7, 0.15, x + 0.3, 0.15, 0.6)], 0.06)
    passo = ease_out(rel(t, 0.15, 0.35), 2)
    G += T.gauss(-0.08 - 0.15 * passo, -0.0, 0.2, 0.3) * 0.15 * pulso(t, 0.1, 0.5)
    return G * env, H * env


def super_carta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        u = ease_out(rel(t, 0.05 + 0.06 * j, 0.3 + 0.06 * j), 2)
        if u > 0:
            x = -0.4 + 0.2 * j
            g, h = icone(T, poe(CARTA, x, 0.45 - 0.1 * u, 0.09 * u, 0), (1 - rel(t, 0.85, 1)) * 1.2, 0.7)
            G, H = G + g, H + h
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g2, h2 = cheio(T, poe(estrela_pts(8, 0.5), 0, -0.2, 0.25 * s, t * 4), 1.3 * s)
        G, H = G + g2, H + h2 * 1.5
    G += estouro(T, t, 0.4, 0.8, 12, 6, 0, -0.2, 0.6, 0.014)
    return G * env, H * env


def fus_ro_dah(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        a0 = 0.1 + 0.15 * j
        u = rel(t, a0, a0 + 0.55)
        if 0 < u < 1:
            x = -0.5 + 1.3 * ease_out(u, 2)
            r = 0.15 + 0.4 * u
            G += T.arc_band(r, 0.04 * (1 - 0.5 * u), -0.9, 0.9, 1.0, 0, x - r, -0.05, 1.0) * (1 - u) * 1.6
    g, h = runas(T, t, 0.0, 0.6, 0.3, 3, -0.05, 1.0, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.08, 0.3, -0.45, -0.05, 0.6)
    return (G + g2) * env, (H + h2) * env


def foco_alma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    G += converge(T, t, 0.0, 0.55, 22, 9, 0, -0.05, 0.75, 0.014)
    k = pulso(t, 0.0, 0.6)
    G += T.gauss(0, -0.05, 0.2 * k + 0.001) * 0.7
    H += T.gauss(0, -0.05, 0.08 * k + 0.001) * 1.5
    g, h = clarao(T, t, 0.5, 0.7, 0, -0.05, 0.8)
    G, H = G + g, H + h
    G += particulas(T, t, 0.55, 1.0, 30, 2, 0, 0, 0.5, 0.6, 0.014)
    G += anel(T, t, 0.5, 0.95, 0.1, 0.6, 0.03, -0.05)
    return G * env, H * env


def quatro_bracos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        a0 = 0.05 + 0.1 * j
        k = pulso(t, a0, a0 + 0.3)
        if k > 0:
            lado = -1 if j % 2 == 0 else 1
            y = -0.2 if j < 2 else 0.2
            P, nos = _punho(T, lado * (0.5 - 0.25 * k), y, 2.0, 0 if lado < 0 else math.pi)
            G += P * 0.85 * k
            H += nos * 0.5 * k
            g, h = clarao(T, t, a0 + 0.12, a0 + 0.25, lado * 0.18, y, 0.35)
            G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.4, 0.9, 0.85, 0.38)
    return G * env, H * env


def ovo_yoshi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    lingua = pulso(t, 0.0, 0.4)
    if lingua > 0:
        G += T.tapered([(-0.5, 0.0, -0.5 + 1.1 * lingua, -0.05, 1.0)], 0.07) * 1.3
        G += T.gauss(-0.5 + 1.1 * lingua, -0.05, 0.09) * 1.4
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        ovo = [(0.28 * s * math.cos(a), 0.05 + 0.36 * s * math.sin(a) * (1.0 if math.sin(a) > 0 else 1.2)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, ovo, 1.2, 0.5)
        G, H = G + g, H + h
        for px, py in ((-0.07, -0.05), (0.08, 0.05), (-0.02, 0.15)):
            G += T.gauss(px * 1.5 * s, py * 1.5 * s + 0.05, 0.055 * s + 0.001) * 1.1
        G += raios(T, t, 0.45, 0.8, 8, 2, 0, 0.05, 0.35, 0.012)
    return G * env, H * env


REGISTRO = [
    ("mu_energia_natural", energia_natural, GRANDE, "Jiraiya · a energia natural", False),
    ("mu_byakugo", byakugo, GRANDE, "Tsunade · o Byakugō", False),
    ("mu_fogo_sagrado", fogo_sagrado, GRANDE, "Sailor Mars · o fogo sagrado", False),
    ("mu_escudo_rosa", escudo_rosa, GRANDE, "Steven · o escudo rosa", False),
    ("mu_futuro", futuro, GRANDE, "Garnet · a visão do futuro", False),
    ("mu_cantada", cantada, GRANDE, "Johnny Bravo · a cantada", False),
    ("mu_dee_dee", dee_dee, GRANDE, "Dexter · o laboratório", False),
    ("mu_jogado_ao_futuro", jogado_ao_futuro, GRANDE, "Aku · o portal do tempo", False),
    ("mu_armadura_aprende", armadura_aprende, GRANDE, "Vilgax · a armadura que aprende", False),
    ("mu_desejo_realizado", desejo_realizado, GRANDE, "Cosmo e Wanda · as varinhas", False),
    ("mu_crafting", crafting, GRANDE, "Steve · a mesa de trabalho", False),
    ("mu_creeper_boom", creeper_boom, GRANDE, "Creeper · o BOOM", False),
    ("mu_waka", waka, GRANDE, "Pac-Man · waka waka", False),
    ("mu_aku_aku", aku_aku, GRANDE, "Crash · a máscara Aku Aku", False),
    ("mu_dead_eye", dead_eye, GRANDE, "Arthur Morgan · o Dead Eye", False),
    ("mu_suprimentos", suprimentos, GRANDE, "Ellie · os suprimentos", False),
    ("mu_desviou_sans", desviou_sans, GRANDE, "Sans · o olho azul e o osso", False),
    ("mu_super_carta", super_carta, GRANDE, "Cuphead · as cartas e o parry", False),
    ("mu_fus_ro_dah", fus_ro_dah, GRANDE, "Dovahkiin · Fus Ro Dah", False),
    ("mu_foco_alma", foco_alma, GRANDE, "O Cavaleiro · o foco da alma", False),
    ("mu_quatro_bracos", quatro_bracos, GRANDE, "Goro · os quatro braços", False),
    ("mu_ovo_yoshi", ovo_yoshi, GRANDE, "Yoshi · a língua e o ovo", False),
]
