"""As três habilidades do Naruto, do Ikki de Fênix e do Luffy, desenhadas para eles.

Pedido do jogador: "passa as habilidades do Naruto, do Ikki de Fênix e do Luffy…
as três de cada um, muito bem feitas… se é de perto, de longe, projétil… os
efeitos sonoros muito bem feitos".

Naruto
- clones_naruto: as nuvens de fumaça "puf" estourando em volta do rival, os
  clones aparecendo nelas e a espiral laranja de confusão girando sobre ele.
- rasengan_mao: o Rasengan girando na mão no Preparo (laço).
- rasengan_impacto: a esfera entra girando e perfura em espiral, empurrando
  tudo para a frente (+x).
- modo_kurama: o manto laranja de chakra nele, com as chamas subindo, as caudas
  balançando e o selo em espiral brilhando.

Ikki
- fenix_voando: a fênix de fogo voando com as asas batendo e a cauda de chamas
  (laço, viagem).
- fenix_explosao: a fênix bate no rival e estoura em fogo e penas.
- golpe_fantasma: o golpe na mente: o dedo de luz, os anéis tortos da ilusão e
  o fantasma subindo do rival.
- fenix_asas: as asas de fogo abrindo em volta do Ikki (nele).
- renascimento_chamas: a coluna de fogo no rival, com a fênix subindo dela.

Luffy
- gomu_gatling: os braços esticam de −x e a chuva de punhos acerta o rival.
- corpo_de_borracha: o corpo dele estica e volta como borracha, e os golpes
  ricocheteiam (nele).
- gear_fifth_nika: as nuvens brancas em volta, o brilho do Nika e o tambor da
  libertação batendo (nele).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _chama(cx, base, alt, larg, fase, ondula=0.3):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    pts = []
    for lado in (1, -1):
        rng = range(13) if lado == 1 else range(12, -1, -1)
        for k in rng:
            u = k / 12
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    return pts


def _fumaca(T, cx, cy, r, f):
    """Uma nuvem de fumaça "puf": bolotas que incham e somem."""
    sub = np.random.default_rng(int(cx * 100 + cy * 1000) & 0xFFFF)
    pts = []
    for _ in range(9):
        a = sub.uniform(0, TAU)
        d = r * (0.3 + 0.7 * ease_out(f, 2)) * sub.uniform(0.4, 1)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a) * 0.8, (1 - f) * sub.uniform(0.6, 1)))
    return T.splats(pts, r * 0.45)


def _espiral(T, cx, cy, r, giro, larg=0.02, voltas=2.2):
    pts = [(cx + r * u * math.cos(giro + TAU * voltas * u), cy + r * u * math.sin(giro + TAU * voltas * u)) for u in np.linspace(0.02, 1, 60)]
    return T.polyline(pts, larg)


# =================================================================== Naruto
def clones_naruto(T, t, rng):
    """Clones das sombras: quatro "puf" de fumaça estouram em volta do rival, cada clone aparece no
    meio da sua fumaça (um vulto laranja) e salta nele; a espiral laranja gira sobre a cabeça."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pos = [(-0.55, -0.1), (0.55, -0.15), (-0.35, 0.45), (0.4, 0.45)]
    for j, (x, y) in enumerate(pos):
        t0 = 0.04 * j
        f = rel(t, t0, t0 + 0.4)
        if f <= 0:
            continue
        G += (_fumaca(T, x, y, 0.22, f) * 1.1 + T.ring(0.08 + 0.18 * ease_out(f, 2), 0.02, cx=x, cy=y) * (1 - f)) * env
        H += _fumaca(T, x, y, 0.22, f) * 0.4 * env
        # o clone: um vulto que aparece na fumaça e salta para o rival
        salta = ease_in(rel(t, t0 + 0.2, t0 + 0.45), 1.6)
        vx, vy = x * (1 - salta), y * (1 - salta)
        vis = pulso(t, t0 + 0.12, t0 + 0.5)
        G += (T.gauss(vx, vy, 0.06, 0.12) * 1.2 + T.gauss(vx, vy - 0.12, 0.045)) * vis * env
        G += T.gauss(0, 0, 0.08) * pulso(t, t0 + 0.4, t0 + 0.55) * 1.3 * env
    # a espiral de confusão girando sobre a cabeça
    gira = pulso(t, 0.4, 1.0)
    esp = _espiral(T, 0, -0.45, 0.22, -TAU * 2.5 * t, 0.022, 2.0) * gira
    G += (esp * 1.3 + T.blur(esp, 0.02) * 0.6) * env
    H += esp * 0.6 * env
    return G, H


def _rasengan(T, cx, cy, r, giro, brilho=1.0):
    """A esfera do Rasengan: núcleo branco, a casca azul e as linhas curvas girando dentro."""
    esfera = T.gauss(cx, cy, r * 0.75) * 1.2 + T.ring(r, r * 0.12, cx=cx, cy=cy) * 0.9
    linhas = T.zero()
    for k in range(6):
        a0 = giro + TAU * k / 6
        pts = [(cx + r * 0.95 * u * math.cos(a0 + 2.2 * u), cy + r * 0.95 * u * math.sin(a0 + 2.2 * u) * 0.8) for u in np.linspace(0.15, 1, 16)]
        linhas += T.polyline(pts, r * 0.07)
    return (esfera + linhas * 0.9) * brilho, T.gauss(cx, cy, r * 0.35) * 1.6 * brilho + linhas * 0.5 * brilho


def rasengan_mao(T, t, rng):
    """O Rasengan girando na mão: a esfera com as linhas girando, o vento em volta e as partículas
    sendo puxadas para dentro."""
    G, H = vazio(T)
    giro = TAU * t * 3
    g, h = _rasengan(T, 0, 0, 0.32, giro)
    vento = T.ring(0.42, 0.025, squash=1.6) * 0.5 + T.arc_band(0.5, 0.03, giro, giro + 2.0) * 0.6 + T.arc_band(0.5, 0.03, giro + math.pi, giro + math.pi + 2.0) * 0.6
    sub = np.random.default_rng(201)
    ps = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t) % 1
        d = 0.85 * (1 - f) + 0.3
        ps.append((d * math.cos(a + 2 * f), d * math.sin(a + 2 * f), f * sub.uniform(0.4, 1)))
    G += g + vento + T.splats(ps, 0.012)
    H += h + T.splats(ps, 0.008) * 0.5
    return G, H


def rasengan_impacto(T, t, rng):
    """O Rasengan entra (vem de −x) girando, perfura o rival em espiral — os anéis girando cada vez
    maiores — e estoura empurrando tudo para a frente (+x), com o rastro em espiral e os destroços."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.15), 1.6)
    giro = TAU * t * 5
    cx = -0.85 + 0.85 * vem
    vis = 1 - rel(t, 0.45, 0.6)
    r = 0.28 * (1 + 0.5 * rel(t, 0.15, 0.45))
    g, h = _rasengan(T, cx, 0, r, giro)
    G += g * vis * env
    H += h * vis * env
    # a perfuração: espirais que crescem e anéis empurrados para +x
    fura = pulso(t, 0.15, 0.75)
    for j in range(3):
        f = rel(t, 0.15 + 0.08 * j, 0.7 + 0.05 * j)
        G += T.ring(0.2 + 0.45 * ease_out(f, 2), 0.03, cx=0.15 + 0.6 * f, squash=1.8) * pulso(t, 0.15 + 0.08 * j, 0.75 + 0.05 * j) * env
    esp = _espiral(T, 0.1, 0, 0.6 * ease_out(rel(t, 0.15, 0.6), 2) + 0.01, giro, 0.025, 2.5) * fura
    k = pulso(t, 0.14, 0.45)
    estouro = T.gauss(0, 0, 0.3) * k * 1.6
    sub = np.random.default_rng(211)
    detritos = []
    for _ in range(18):
        a = sub.normal(0, 0.6)
        d = 0.15 + 0.85 * ease_out(rel(t, 0.18, 0.85), 2) * sub.uniform(0.4, 1)
        detritos.append((estrela(d * math.cos(a), d * math.sin(a), 0.03, a, 4, 0.5), pulso(t, 0.18, 0.85) * sub.uniform(0.5, 1)))
    D = T.polys(detritos, 0.003)
    G += (esp * 1.2 + estouro + D * 1.1) * env
    H += (esp * 0.5 + estouro * 0.9 + D * 0.4) * env
    return G, H


def modo_kurama(T, t, rng):
    """O Manto da Kurama no Naruto: o manto de chakra acende, as chamas laranja sobem em volta do
    corpo, as caudas balançam atrás e o selo em espiral brilha na barriga."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.95) ** 0.5
    acende = ease_out(rel(t, 0.0, 0.3), 2)
    fase = TAU * t * 2
    chamas = []
    for k in range(9):
        x = (k - 4) * 0.1
        alt = (0.55 + 0.2 * math.sin(fase + k)) * acende
        chamas.append((_chama(x, 0.55, alt, 0.1, fase + k * 0.9, 0.35), 0.8))
    Ch = T.polys(chamas, 0.006)
    caudas = T.zero()
    for k in range(5):
        a0 = -math.pi / 2 + (k - 2) * 0.45
        pts = []
        for j in range(20):
            u = j / 19
            a = a0 + 0.5 * math.sin(fase + k + 3 * u) * u
            pts.append((0.15 * math.cos(a) + 0.8 * u * math.cos(a) * acende, 0.1 + 0.8 * u * math.sin(a) * acende))
        caudas += T.polyline(pts, 0.05) * (0.7 + 0.3 * math.sin(fase + k))
    manto = T.ring(0.48, 0.07, cy=0.05, squash=0.8) * acende
    selo = _espiral(T, 0, 0.1, 0.15, -fase, 0.015, 1.6) * acende
    G += (Ch * 1.1 + T.blur(Ch, 0.03) * 0.6 + T.blur(caudas, 0.02) * 0.9 + caudas * 0.6 + manto * 0.8 + selo * 1.2) * env
    H += (Ch * 0.4 + caudas * 0.3 + selo * 0.9) * env
    return G, H


# =================================================================== Ikki
def _fenix(T, cx, cy, esc, bate, ang=0.0):
    """A fênix de perfil, voando para +x: o corpo, o pescoço e a cabeça com crista, as asas com penas
    e a cauda longa em chamas."""
    corpo = [(0.0, -0.05), (0.18, -0.06), (0.3, -0.12), (0.4, -0.1), (0.36, -0.06), (0.28, -0.03), (0.2, 0.04), (0.0, 0.06), (-0.15, 0.03)]
    crista = [(0.33, -0.12), (0.26, -0.24), (0.36, -0.15), (0.38, -0.26), (0.4, -0.12)]
    asa = [(0.12, -0.04)]
    for k in range(6):
        u = k / 5
        asa += [(0.12 - 0.42 * u, -0.06 - (0.42 * bate + 0.12) * math.sin(math.pi * (0.25 + 0.5 * u))), (0.04 - 0.42 * u + 0.06, -0.06 - (0.3 * bate + 0.06) * math.sin(math.pi * (0.25 + 0.5 * u)))]
    asa += [(-0.2, 0.0)]
    f = lambda q: _gira([(x * esc, y * esc) for x, y in q], ang, cx, cy)
    return [(f(corpo), 1.0), (f(crista), 0.9), (f(asa), 0.85)]


def fenix_voando(T, t, rng):
    """A fênix do Ikki voando: as asas batendo, a crista acesa e a cauda comprida de chamas com
    brasas soltando para trás."""
    G, H = vazio(T)
    bate = math.sin(TAU * t * 2)
    F = T.polys(_fenix(T, 0.25, 0.05, 1.25, bate), 0.005)
    sub = np.random.default_rng(221)
    cauda = T.tapered([(-0.95, 0.08 + 0.05 * math.sin(TAU * t + k), 0.05, 0.05, 1.0) for k in range(3)], 0.2)
    brasas = []
    for _ in range(18):
        f = (sub.uniform() + t * 1.4) % 1
        brasas.append((0.0 - 0.9 * f, 0.05 + sub.normal(0, 0.05) * (1 + 2 * f), (1 - f) * sub.uniform(0.5, 1)))
    G += F * 1.3 + T.blur(F, 0.03) * 0.8 + cauda * 0.9 + T.blur(cauda, 0.03) * 0.5 + T.splats(brasas, 0.014) * 1.2
    H += F * 0.45 + cauda * 0.3 + T.splats(brasas, 0.008) * 0.6
    return G, H


def fenix_explosao(T, t, rng):
    """A fênix bate no rival e estoura: a bola de fogo cresce, as línguas de chama sobem, as penas de
    fogo voam girando e o anel de calor se abre."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.5)
    bola = T.gauss(0, 0, 0.18 + 0.2 * ease_out(rel(t, 0.0, 0.4), 2)) * k * 1.6
    fase = TAU * t * 2
    chamas = [(_chama((j - 3) * 0.13, 0.25, (0.5 + 0.2 * math.sin(fase + j)) * pulso(t, 0.05, 0.85), 0.11, fase + j, 0.35), 0.8) for j in range(7)]
    Ch = T.polys(chamas, 0.006)
    sub = np.random.default_rng(231)
    penas = []
    for _ in range(12):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.75 * ease_out(rel(t, 0.05, 0.85), 2) * sub.uniform(0.5, 1)
        x, y = d * math.cos(a), d * math.sin(a) + 0.2 * rel(t, 0.3, 1.0)
        penas.append((_gira([(-0.07, 0), (0.0, -0.025), (0.07, 0), (0.0, 0.02)], a + TAU * t * 1.5, x, y), pulso(t, 0.05, 0.9) * sub.uniform(0.5, 1)))
    P = T.polys(penas, 0.003)
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.05, 0.7), 2), 0.04) * pulso(t, 0.05, 0.75)
    G += (bola + Ch * 1.1 + T.blur(Ch, 0.03) * 0.5 + P * 1.2 + anel) * env
    H += (bola * 0.9 + Ch * 0.4 + P * 0.5 + anel * 0.3) * env
    return G, H


def golpe_fantasma(T, t, rng):
    """Golpe Fantasma: um dedo de luz toca a testa do rival, anéis tortos de ilusão se espalham, os
    olhos dele se perdem (estrelinhas girando) e um fantasma sobe dele."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    dedo = T.tapered([(-0.95, -0.25, -0.95 + 0.9 * ease_out(rel(t, 0.0, 0.18), 2), -0.25, 1.0)], 0.05) * (1 - rel(t, 0.2, 0.35))
    k = pulso(t, 0.15, 0.45)
    toque = T.gauss(0, -0.25, 0.08) * k * 1.8 + T.flare(0, -0.25, 0.8 * k + 1e-3, 0.4, 0.012)
    aneis = T.zero()
    for j in range(3):
        f = rel(t, 0.18 + 0.1 * j, 0.85)
        tort = 1 + 0.25 * math.sin(TAU * t * 3 + j)
        aneis += T.ring(0.1 + 0.65 * ease_out(f, 2), 0.025, cy=-0.25 + 0.1 * j, squash=tort) * pulso(t, 0.18 + 0.1 * j, 0.9)
    estrelas = T.polys([(estrela(0.25 * math.cos(TAU * t * 1.5 + TAU * j / 3), -0.5 + 0.08 * math.sin(TAU * t * 1.5 + TAU * j / 3), 0.05, 0.3, 5, 0.45), pulso(t, 0.35, 0.95)) for j in range(3)], 0.003)
    sobe = rel(t, 0.35, 1.0)
    fantasma = (T.gauss(0, -0.1 - 0.6 * sobe, 0.12, 0.18) + T.gauss(0, -0.25 - 0.6 * sobe, 0.08)) * pulso(t, 0.35, 1.0) * 0.9
    G += (dedo * 1.1 + toque + aneis * 1.1 + estrelas * 1.2 + fantasma) * env
    H += (dedo * 0.6 + toque * 0.9 + aneis * 0.3 + estrelas * 0.6) * env
    return G, H


def fenix_asas(T, t, rng):
    """As asas de fogo da fênix abrindo em volta do Ikki: as penas de chama, a crista de fogo e as
    brasas subindo."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.95) ** 0.5
    abre = back(rel(t, 0.0, 0.35), 1.4)
    fase = TAU * t * 2
    asas = []
    for lado in (-1, 1):
        for k in range(7):
            u = k / 6
            a = -math.pi / 2 + lado * (0.5 + 1.1 * u * abre)
            comp = (0.55 + 0.25 * math.sin(math.pi * u)) * abre
            asas.append((_gira([(0, -0.035), (comp, 0), (0, 0.035)], a, lado * 0.05, 0.05), 0.85))
    A = T.polys(asas, 0.006)
    crista = T.polys([(_chama(0, -0.15, 0.4 * abre, 0.1, fase, 0.4), 0.9)], 0.006)
    sub = np.random.default_rng(241)
    brasas = []
    for _ in range(20):
        f = (sub.uniform() + t) % 1
        brasas.append((sub.normal(0, 0.45), 0.4 - 1.0 * f, math.sin(math.pi * f) * sub.uniform(0.4, 1)))
    G += (A * 1.1 + T.blur(A, 0.03) * 0.8 + crista * 1.1 + T.splats(brasas, 0.012)) * env
    H += (A * 0.35 + crista * 0.5 + T.splats(brasas, 0.008) * 0.5) * env
    return G, H


def renascimento_chamas(T, t, rng):
    """Renascimento: uma coluna de fogo sobe no rival, as chamas crescem em volta dele e a fênix sai
    voando para cima de dentro da coluna, abrindo as asas; o rival fica queimando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    fase = TAU * t * 2
    coluna = T.gauss(0, 0.3 - 0.6 * sobe, 0.18, 0.55 * sobe + 0.05) * pulso(t, 0.0, 0.8) * 1.4
    chamas = [(_chama((j - 4) * 0.11, 0.6, (0.6 + 0.4 * math.sin(fase + j * 1.3)) * sobe * pulso(t, 0.0, 0.95), 0.1, fase + j, 0.35), 0.8) for j in range(9)]
    Ch = T.polys(chamas, 0.006)
    voa = rel(t, 0.3, 0.9)
    F = T.polys(_fenix(T, 0.0, 0.1 - 0.75 * ease_out(voa, 1.6), 1.2, math.sin(TAU * t * 3), -math.pi / 2), 0.005) * pulso(t, 0.28, 0.95)
    G += (coluna + Ch * 1.1 + T.blur(Ch, 0.03) * 0.5 + F * 1.3 + T.blur(F, 0.03) * 0.7) * env
    H += (coluna * 0.6 + Ch * 0.4 + F * 0.5) * env
    return G, H


# =================================================================== Luffy
def _punho_luffy(T, x, y, esc=1.0):
    """O punho visto de frente: a bola do punho e os vincos dos dedos."""
    P = T.gauss(x, y, 0.075 * esc, 0.065 * esc) * 1.3 + T.ring(0.07 * esc, 0.014 * esc, cx=x, cy=y)
    vincos = sum(T.polyline([(x + 0.03 * esc, y + d * esc), (x + 0.075 * esc, y + d * esc)], 0.008 * esc) for d in (-0.03, 0.0, 0.03))
    return np.clip(P - vincos * 0.6, 0, None)


def gomu_gatling(T, t, rng):
    """Gomu Gomu no Gatling: os braços esticam de −x e uma chuva de punhos acerta o rival por todo o
    corpo, um atrás do outro, cada um com o estalo; as linhas de velocidade atrás."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sub = np.random.default_rng(251)
    for j in range(18):
        t0 = 0.04 * j
        f = rel(t, t0, t0 + 0.1)
        vis = pulso(t, t0, t0 + 0.28)
        y = sub.uniform(-0.55, 0.55)
        if vis <= 0:
            continue
        x = sub.uniform(-0.25, 0.2)
        px = -1.0 + (x + 1.0) * ease_out(f, 2.5)
        braco = T.polyline([(-1.0, y * 0.5), (px - 0.07, y)], 0.035) * vis
        G += (braco * 0.9 + _punho_luffy(T, px, y, 1.5) * vis) * env
        H += _punho_luffy(T, px, y, 1.5) * vis * 0.4 * env
        k = pulso(t, t0 + 0.08, t0 + 0.22)
        estalo = T.polys([(estrela(px + 0.08, y, 0.13 * k + 0.005, sub.uniform(0, TAU), 6, 0.4), 1.0)], 0.003) * k
        G += estalo * 1.2 * env
        H += estalo * 0.8 * env
    linhas = T.tapered([(-0.95, y, -0.3, y, 0.6) for y in (-0.45, -0.22, 0.0, 0.22, 0.45)], 0.02) * pulso(t, 0.0, 0.8)
    G += linhas * 0.5 * env
    return G, H


def corpo_de_borracha(T, t, rng):
    """Corpo de borracha: o corpo do Luffy estica e volta (o anel achata e estica como borracha), os
    golpes batem e ricocheteiam para longe, com as linhas de "boing"."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.95) ** 0.5
    mola = math.sin(TAU * t * 2.5) * math.exp(-2.5 * t)
    corpo = T.ring(0.42, 0.06, squash=1.0 + 0.5 * mola) * (0.8 + 0.2 * math.cos(TAU * t * 5))
    sub = np.random.default_rng(261)
    ricochetes = T.zero()
    for j in range(3):
        t0 = 0.1 + 0.2 * j
        a = sub.uniform(0, TAU)
        f = rel(t, t0, t0 + 0.35)
        if f <= 0 or f >= 1:
            continue
        d = 0.45 + 0.5 * ease_out(f, 2)
        ricochetes += T.gauss(d * math.cos(a), d * math.sin(a), 0.035) * (1 - f) * 1.4
        ricochetes += T.polys([(estrela(0.45 * math.cos(a), 0.45 * math.sin(a), 0.1 * pulso(f, 0.0, 0.4) + 0.005, a, 5, 0.4), 1.0)], 0.003) * pulso(f, 0.0, 0.4)
    boing = T.zero()
    for lado in (-1, 1):
        for k in range(3):
            boing += T.arc_band(0.55 + 0.07 * k, 0.012, lado * 0.4 - 0.3 + (math.pi if lado < 0 else 0), lado * 0.4 + 0.3 + (math.pi if lado < 0 else 0)) * pulso(t, 0.1 * k, 0.6 + 0.1 * k)
    # os braços esticam para os lados e voltam como elástico, ondulando
    estica = abs(math.sin(TAU * t * 1.5)) * math.exp(-1.2 * t)
    bracos = T.zero()
    for lado in (-1, 1):
        comp = 0.35 + 0.55 * estica
        pts = [(lado * (0.38 + comp * u), 0.05 * math.sin(TAU * 2 * u + TAU * t * 3) * (1 - u)) for u in np.linspace(0, 1, 24)]
        bracos += T.polyline(pts, 0.035) + _punho_luffy(T, lado * (0.38 + comp), 0.0, 0.9)
    G += (corpo * 1.1 + T.blur(corpo, 0.03) * 0.6 + ricochetes + boing * 0.8 + bracos * 0.9) * env
    H += (corpo * 0.3 + ricochetes * 0.6) * env
    return G, H


def gear_fifth_nika(T, t, rng):
    """Gear Fifth: nuvens brancas fofas em volta do Luffy, o cabelo de fumaça subindo, o brilho do sol do
    Nika atrás e os anéis do tambor da libertação batendo (tum-tum, tum-tum)."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.95) ** 0.5
    acende = ease_out(rel(t, 0.0, 0.3), 2)
    sol = T.gauss(0, -0.1, 0.22) * 0.8 * acende + T.polys([(estrela(0, -0.1, 0.5 * acende + 0.01, TAU * t / 6, 12, 0.6), 0.5)], 0.01) * 0.6
    sub = np.random.default_rng(271)
    nuvens = T.zero()
    for j in range(8):
        a = TAU * j / 8 + TAU * t * 0.2
        r = 0.55 + 0.05 * math.sin(TAU * t + j)
        cx, cy = r * math.cos(a), r * math.sin(a) * 0.8
        for _ in range(3):
            ox, oy = cx + sub.normal(0, 0.05), cy + sub.normal(0, 0.04)
            nuvens += (T.gauss(ox, oy, 0.055) * 0.9 + T.ring(0.065, 0.012, cx=ox, cy=oy) * 0.6) * acende
    cabelo = T.zero()
    for k in range(7):
        x = (k - 3) * 0.07
        f = (t * 1.5 + k * 0.13) % 1
        cabelo += T.gauss(x + 0.04 * math.sin(TAU * f), -0.4 - 0.35 * f, 0.06) * (1 - f)
    # o tambor da libertação: duas batidas por ciclo
    batida = max(math.exp(-((t * 2) % 1) * 8), 0)
    tambor = T.ring(0.3 + 0.35 * (1 - batida), 0.03) * batida
    G += (sol + nuvens * 1.1 + cabelo * 1.1 + tambor * 1.2) * env
    H += (sol * 0.6 + nuvens * 0.8 + cabelo * 0.7 + tambor * 0.5) * env
    return G, H


REGISTRO = [
    ("clones_naruto", clones_naruto, GRANDE, "Naruto · Clones das sombras: fumaça, clones e a espiral", False),
    ("rasengan_mao", rasengan_mao, MEDIA, "Naruto · o Rasengan girando na mão (laço)", True),
    ("rasengan_impacto", rasengan_impacto, GRANDE, "Naruto · o Rasengan perfurando em espiral", False),
    ("modo_kurama", modo_kurama, GRANDE, "Naruto · o Manto da Kurama: chamas, caudas e o selo", False),
    ("fenix_voando", fenix_voando, MEDIA, "Ikki · a fênix de fogo voando (laço)", True),
    ("fenix_explosao", fenix_explosao, GRANDE, "Ikki · a fênix estourando em fogo e penas", False),
    ("golpe_fantasma", golpe_fantasma, GRANDE, "Ikki · Golpe Fantasma: o toque na mente e a ilusão", False),
    ("fenix_asas", fenix_asas, MEDIA, "Ikki · as asas de fogo abrindo nele", False),
    ("renascimento_chamas", renascimento_chamas, GRANDE, "Ikki · Renascimento: a coluna de fogo e a fênix subindo", False),
    ("gomu_gatling", gomu_gatling, GRANDE, "Luffy · Gomu Gomu no Gatling: a chuva de punhos", False),
    ("corpo_de_borracha", corpo_de_borracha, GRANDE, "Luffy · Corpo de borracha: estica e os golpes ricocheteiam", False),
    ("gear_fifth_nika", gear_fifth_nika, GRANDE, "Luffy · Gear Fifth: nuvens, o sol do Nika e o tambor", False),
]
