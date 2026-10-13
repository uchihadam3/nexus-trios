"""Ataques básicos com animação própria, lote u: os socos que ainda eram o soco de todo mundo.

Goku, Vegeta, Naruto, Gojo, Flash, Homem de Ferro, Thanos e Gohan. O básico continua um golpe simples (pedido do
jogador: "o ataque básico tem que ser coisa simples… pode ser só um soco"), mas cada soco é do personagem: a
munhequeira azul e o ki dourado do Goku, a luva branca e o ki azul estalando do Vegeta, a espiral e a fumaça do
Naruto, o Infinito que segura o punho do Gojo, os punhos-fantasma e os raios do Flash, a manopla com propulsores
do Homem de Ferro, a Manopla do Infinito do Thanos e o soco calmo com a aura branca do Gohan.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rastro_de_velocidade, rel, vazio
from .basicos_a import _elipse_pts, _nuvem


def _pts(base, cx, cy, esc, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + (x * c - y * s) * esc, cy + (x * s + y * c) * esc) for x, y in base]


def _mao(T, cx, cy, esc, tipo='nu'):
    """O punho de lado com os nós dos dedos para +x. tipo: nu, luva (punho redondo e o punho da luva largo),
    manopla (grande, placas) ou armadura (quadrada, em placas). Devolve (silhueta, detalhes para o núcleo)."""
    if tipo == 'armadura':
        corpo = [(-0.13, -0.15), (0.12, -0.15), (0.17, -0.1), (0.17, 0.1), (0.12, 0.15), (-0.13, 0.15)]
        formas = [(_pts(corpo, cx, cy, esc), 1.0)]
        det = T.lines([(cx + 0.06 * esc, cy - 0.15 * esc, cx + 0.06 * esc, cy + 0.15 * esc, 1.0),
                       (cx + 0.12 * esc, cy - 0.05 * esc, cx + 0.17 * esc, cy - 0.05 * esc, 1.0),
                       (cx + 0.12 * esc, cy + 0.05 * esc, cx + 0.17 * esc, cy + 0.05 * esc, 1.0),
                       (cx - 0.13 * esc, cy, cx + 0.0 * esc, cy, 1.0)], 0.009 * esc)
        return np.clip(T.polys(formas, 0.003), 0, 1), det
    g = {'nu': 1.0, 'luva': 1.12, 'manopla': 1.3}[tipo]
    formas = [(_elipse_pts(cx - 0.02 * esc, cy, 0.13 * esc * g, 0.17 * esc * g), 1.0)]
    for k in range(4):
        formas.append((_elipse_pts(cx + 0.1 * esc * g, cy + (-0.13 + 0.087 * k) * esc * g, 0.075 * esc * g, 0.04 * esc * g), 1.0))
    formas.append((_elipse_pts(cx, cy - 0.17 * esc * g, 0.1 * esc * g, 0.036 * esc * g, 0.15), 1.0))
    det = T.zero()
    for k in range(1, 4):
        y = cy + (-0.13 + 0.087 * k - 0.0435) * esc * g
        det += T.lines([(cx + 0.06 * esc * g, y, cx + 0.16 * esc * g, y, 1.0)], 0.006 * esc)
    return np.clip(T.polys(formas, 0.003), 0, 1), det


def _antebraco(T, cx, cy, esc, comp=0.42, larg=0.11, punho=None):
    """O antebraço atrás do punho; `punho` = (posição 0..1 a partir da mão, largura) da munhequeira/manga."""
    a = [(cx - comp * esc, cy - larg * esc), (cx - 0.08 * esc, cy - (larg + 0.02) * esc),
         (cx - 0.08 * esc, cy + (larg + 0.02) * esc), (cx - comp * esc, cy + larg * esc)]
    A = T.polys([(a, 0.75)], 0.004)
    B = T.zero()
    if punho:
        p, w = punho
        x0 = cx - (0.08 + p * (comp - 0.08)) * esc
        B = T.polys([([(x0 - w * esc, cy - (larg + 0.045) * esc), (x0, cy - (larg + 0.045) * esc),
                       (x0, cy + (larg + 0.045) * esc), (x0 - w * esc, cy + (larg + 0.045) * esc)], 1.0)], 0.004)
    return np.clip(A + B, 0, 1), B


def _estrela_de_contato(T, t, t0, r=0.32, pontas=8, interno=0.38, ang=0.25, dur=0.32):
    k = pulso(t, t0, t0 + dur)
    return T.polys([(estrela(0.0, 0.0, r * k + 0.01, ang, pontas, interno), 1.0)], 0.005) * k


def _anel(T, t, t0, t1, r0, r1, larg, squash=1.0, cx=0.0, cy=0.0):
    u = rel(t, t0, t1)
    if u <= 0 or u >= 1:
        return T.zero()
    return T.ring(r0 + (r1 - r0) * ease_out(u, 2.2), larg * (1 - 0.6 * u), cx, cy, squash) * (1 - u) ** 1.2


def _riscos(T, t, t0, dur, n, r0, r1, larg, seed, a0=-1.3, a1=1.3):
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    q = np.random.default_rng(seed)
    segs = []
    for j in range(n):
        a = a0 + (a1 - a0) * (j + 0.5) / n + q.uniform(-0.12, 0.12)
        d0 = r0 + (r1 - r0) * 0.5 * ease_out(u, 2)
        d1 = d0 + (r1 - r0) * 0.6 * (1 - 0.5 * u) * q.uniform(0.7, 1.1)
        segs.append((d0 * math.cos(a), d0 * math.sin(a), d1 * math.cos(a), d1 * math.sin(a), 1.0))
    return T.tapered(segs, larg) * (1 - u)


def _vai_e_volta(t, chega=0.22, x0=-0.98, x1=-0.14, recua=0.2):
    vem = ease_in(rel(t, 0.0, chega), 1.6)
    volta = ease_out(rel(t, chega + 0.05, 0.62), 2)
    return x0 + (x1 - x0) * vem - recua * volta


# ------------------------------------------------------------------ Goku
def soco_saiyajin(T, t, rng):
    """Goku: o antebraço com a munhequeira azul entra rápido, o ki dourado acende em volta do punho no último
    instante e o soco estoura uma onda de ar com poeira, como nos treinos com o Kaio."""
    G, H = vazio(T)
    env = apaga(t, 0.74, 1)
    px = _vai_e_volta(t)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    M, d = _mao(T, px, 0.0, 1.15)
    A, B = _antebraco(T, px, 0.0, 1.15, punho=(0.12, 0.09))
    corpo = np.clip(M + A, 0, 1) * vis
    # o ki dourado: chamas curtas em volta do punho só no fim da ida
    ki = T.zero()
    kk = pulso(t, 0.1, 0.4)
    if kk > 0:
        q = np.random.default_rng(7)
        segs = []
        for j in range(11):
            a = math.pi * (0.35 + 1.3 * j / 10)
            r0 = 0.2
            r1 = r0 + 0.11 * (0.7 + 0.5 * q.uniform()) * (1 + 0.3 * math.sin(t * 40 + j))
            segs.append((px - 0.02 + r0 * math.cos(a), r0 * math.sin(a) * 1.1, px - 0.02 - 0.04 + r1 * math.cos(a) * 1.05, r1 * math.sin(a) * 1.15, 1.0))
        ki = T.tapered(segs, 0.03) * kk
    linhas = rastro_de_velocidade(T, rng, 6, 0.0, 0.5, 0.15, -px - 0.1, largura=0.016, seed=31) * (1 - rel(t, 0.18, 0.3)) * 0.8
    t0 = 0.22
    est = _estrela_de_contato(T, t, t0, 0.3)
    onda = _anel(T, t, t0, t0 + 0.45, 0.12, 0.68, 0.05, 1.35)
    vida = janela(t, t0, t0 + 0.05) * apaga(t, t0 + 0.2, 0.95)
    poeira = _nuvem(T, 41, 0.05, 0.12, 0.16, ease_out(rel(t, t0, 0.9), 2), 8, 0.1, 1.6) * vida
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 1.5
    G += (corpo * 1.1 + T.blur(corpo, 0.02) * 0.4 + ki * 1.3 + linhas + est * 1.2 + onda * 1.3 + poeira * 0.85 + clarao) * env
    H += (corpo * 0.35 + B * vis * 0.9 + d * vis * 0.8 + ki * 0.8 + est + onda * 0.45 + poeira * 0.4 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Vegeta
def soco_do_principe(T, t, rng):
    """Vegeta: a luva branca de punho largo vem num soco seco, o ki azul estala em faíscas curtas em volta da
    luva e o impacto é uma estrela de pontas afiadas com estilhaços, o golpe orgulhoso do príncipe."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    px = _vai_e_volta(t, 0.2, recua=0.16)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.44, 0.6))
    M, d = _mao(T, px, 0.0, 1.1, 'luva')
    # o punho da luva abre como um sino
    sino = T.polys([(_pts([(-0.08, -0.2), (-0.2, -0.17), (-0.2, 0.17), (-0.08, 0.2)], px, 0.0, 1.1), 1.0)], 0.004)
    A, _ = _antebraco(T, px - 0.12, 0.0, 1.1, 0.34, 0.1)
    corpo = np.clip(M + sino + A * 0.8, 0, 1) * vis
    estalo = T.zero()
    for j in range(4):
        k = pulso(t, 0.04 + 0.05 * j, 0.14 + 0.05 * j)
        if k <= 0:
            continue
        a = -1.1 + 0.75 * j
        x0, y0 = px + 0.18 * math.cos(a), 0.2 * math.sin(a)
        estalo += T.polyline(jagged(np.random.default_rng(90 + j), x0, y0, x0 + 0.2 * math.cos(a), y0 + 0.2 * math.sin(a), 3, 0.2), 0.016) * k
    t0 = 0.2
    est = _estrela_de_contato(T, t, t0, 0.4, 6, 0.22, 0.0, 0.42)
    lascas = _riscos(T, t, t0, 0.5, 9, 0.18, 0.66, 0.03, 12, -1.6, 1.6)
    onda = _anel(T, t, t0, t0 + 0.55, 0.1, 0.56, 0.045, 1.1)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.4
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.4 + estalo * 1.4 + est * 1.3 + lascas * 1.2 + onda + clarao) * env
    H += (corpo * 0.75 + d * vis * 0.4 + estalo * 1.0 + est * 1.1 + lascas * 0.8 + onda * 0.4 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Naruto
def soco_do_naruto(T, t, rng):
    """Naruto: soco de briga com a manga larga do macacão, a espiral do Uzumaki gira no ponto do impacto e
    uma baforada de fumaça fecha o golpe (o mesmo "puf" dos clones)."""
    G, H = vazio(T)
    env = apaga(t, 0.76, 1)
    px = _vai_e_volta(t, 0.22, recua=0.22)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    M, d = _mao(T, px, 0.02, 1.12)
    manga = T.polys([(_pts([(-0.1, -0.14), (-0.5, -0.2), (-0.56, 0.0), (-0.5, 0.21), (-0.1, 0.15)], px, 0.02, 1.12), 0.85)], 0.006)
    punho_manga = T.polys([(_pts([(-0.1, -0.15), (-0.16, -0.17), (-0.16, 0.18), (-0.1, 0.16)], px, 0.02, 1.12), 1.0)], 0.004)
    corpo = np.clip(M + manga + punho_manga, 0, 1) * vis
    t0 = 0.22
    # a espiral: três voltas que giram e abrem
    esp = T.zero()
    ke = pulso(t, t0 - 0.02, t0 + 0.42)
    if ke > 0:
        u = rel(t, t0 - 0.02, t0 + 0.42)
        pts = []
        for j in range(70):
            s = j / 69
            a = s * TAU * 2.6 + u * 9
            r = (0.04 + 0.44 * s) * (0.6 + 0.6 * ease_out(u, 2))
            pts.append((r * math.cos(a), r * math.sin(a) * 0.85))
        esp = T.polyline(pts, 0.032) * ke
    vida = janela(t, t0 + 0.08, t0 + 0.14) * apaga(t, t0 + 0.3, 1.0)
    fumaca = _nuvem(T, 55, 0.05, -0.02, 0.15, ease_out(rel(t, t0 + 0.08, 0.95), 2), 9, 0.16) * vida
    est = _estrela_de_contato(T, t, t0, 0.2)
    clarao = T.gauss(0, 0, 0.12) * pulso(t, t0, t0 + 0.14) * 1.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.4 + esp * 1.7 + fumaca * 0.6 + est + clarao) * env
    H += (corpo * 0.35 + punho_manga * vis * 0.7 + d * vis * 0.8 + esp * 0.9 + fumaca * 0.55 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Gojo
def soco_infinito(T, t, rng):
    """Gojo: o punho vem rápido e quase para no ar a um palmo do alvo (o Infinito deixa tudo devagar, os anéis
    azuis tremem em volta), e de repente entra de uma vez com um estalo seco de luz azul."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vem = ease_out(rel(t, 0.0, 0.16), 2.2)
    devagar = rel(t, 0.16, 0.4)
    entra = ease_in(rel(t, 0.4, 0.46), 2)
    px = -0.98 + 0.62 * vem + 0.08 * devagar + 0.14 * entra - 0.18 * ease_out(rel(t, 0.5, 0.75), 2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.6, 0.74))
    M, d = _mao(T, px, 0.0, 1.05)
    A, _ = _antebraco(T, px, 0.0, 1.05, 0.4, 0.1)
    corpo = np.clip(M + A, 0, 1) * vis
    # os anéis do Infinito em volta do punho parado
    infi = T.zero()
    ki = janela(t, 0.14, 0.2) * (1 - rel(t, 0.4, 0.46))
    if ki > 0:
        for j in range(3):
            fase = (t * 3 + j / 3) % 1
            infi += T.ring(0.08 + 0.3 * fase, 0.016, px + 0.16, 0.0, 0.7) * (1 - fase) * ki
    t0 = 0.45
    estalo = T.polys([(estrela(0, 0, 0.42 * pulso(t, t0, t0 + 0.2) + 0.01, 0.0, 4, 0.12), 1.0)], 0.004) * pulso(t, t0, t0 + 0.2)
    onda = _anel(T, t, t0, t0 + 0.4, 0.06, 0.6, 0.035, 1.0) + _anel(T, t, t0 + 0.06, t0 + 0.46, 0.05, 0.42, 0.025, 1.0)
    clarao = T.gauss(0, 0, 0.14) * pulso(t, t0, t0 + 0.14) * 2.6
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + infi * 1.4 + estalo * 1.4 + onda * 1.2 + clarao) * env
    H += (corpo * 0.35 + d * vis * 0.8 + infi * 0.7 + estalo * 1.2 + onda * 0.5 + clarao * 1.3) * env
    return G, H


# ------------------------------------------------------------------ Flash
def soco_veloz_flash(T, t, rng):
    """Flash: três punhos-fantasma chegam um atrás do outro rápido demais para ver, presos por raios
    finos, e cada um acerta num ponto; o último estoura em raios que saem do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.74, 1)
    alvos = [(-0.08, -0.14), (0.06, 0.14), (0.0, 0.0)]
    for k, (tx, ty) in enumerate(alvos):
        a0 = 0.05 * k
        u = ease_in(rel(t, a0, a0 + 0.13), 1.3)
        if u <= 0:
            continue
        px = -0.95 + (tx - 0.12 + 0.95) * u
        vis = (1 - rel(t, a0 + 0.13, a0 + 0.3)) * (0.55 if k < 2 else 1.0)
        M, d = _mao(T, px, ty, 1.0)
        G += M * vis * 1.0 + T.blur(M, 0.025) * vis * 0.4
        H += d * vis * 0.7 + M * vis * 0.25
        rastro = T.tapered([(px - 0.55, ty, px - 0.05, ty, 1.0)], 0.07) * vis * (1 - rel(t, a0 + 0.1, a0 + 0.2))
        G += rastro * 0.6
        # o raio amarelo que corre junto do rastro
        if vis > 0.1:
            G += T.polyline(jagged(np.random.default_rng(300 + k + int(t * 30)), px - 0.6, ty + 0.06, px - 0.05, ty + 0.03, 3, 0.15), 0.016) * vis * 1.2
        g = pulso(t, a0 + 0.12, a0 + 0.3)
        G += T.gauss(tx, ty, 0.1) * g * 1.4
        H += T.gauss(tx, ty, 0.05) * g * 1.6
    t0 = 0.24
    raios = T.zero()
    kr = pulso(t, t0, t0 + 0.42)
    if kr > 0:
        for j in range(6):
            a = TAU * j / 6 + 0.3
            raios += T.polyline(jagged(np.random.default_rng(500 + j + int(t * 24)), 0.05 * math.cos(a), 0.05 * math.sin(a),
                                       0.55 * math.cos(a), 0.55 * math.sin(a), 3, 0.16), 0.02)
        raios *= kr
    est = _estrela_de_contato(T, t, t0, 0.28)
    onda = _anel(T, t, t0, t0 + 0.38, 0.1, 0.5, 0.035, 1.2)
    G += (raios * 1.4 + est + onda) * env
    H += (raios * 1.0 + est * 0.9 + onda * 0.4) * env
    G *= env
    H *= env
    return G, H


# ------------------------------------------------------------------ Homem de Ferro
def soco_de_armadura(T, t, rng):
    """Homem de Ferro: a manopla quadrada em placas avança empurrada pelos propulsores do punho (duas chamas
    curtas), bate com um "clang" de metal e solta uma chuva de faíscas e o brilho hexagonal do impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.74, 1)
    px = _vai_e_volta(t, 0.22, recua=0.2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    M, d = _mao(T, px, 0.0, 1.15, 'armadura')
    A = T.polys([(_pts([(-0.13, -0.12), (-0.45, -0.13), (-0.45, 0.13), (-0.13, 0.12)], px, 0.0, 1.15), 0.8)], 0.004)
    placas = T.lines([(px - 0.25 * 1.15, -0.13 * 1.15, px - 0.25 * 1.15, 0.13 * 1.15, 1.0),
                      (px - 0.36 * 1.15, -0.13 * 1.15, px - 0.36 * 1.15, 0.13 * 1.15, 1.0)], 0.01)
    corpo = np.clip(M + A, 0, 1) * vis
    jato = T.zero()
    kj = janela(t, 0.0, 0.05) * (1 - rel(t, 0.18, 0.28))
    if kj > 0:
        for dy in (-0.1, 0.1):
            fl = 0.3 + 0.07 * math.sin(t * 60 + dy * 30)
            jato += T.tapered([(px - 0.5 * 1.15 - fl, dy * 1.15, px - 0.47 * 1.15, dy * 1.15, 1.0)], 0.075)
        jato *= kj
    t0 = 0.22
    hexa = T.zero()
    kh = pulso(t, t0, t0 + 0.3)
    if kh > 0:
        r = 0.16 + 0.24 * ease_out(rel(t, t0, t0 + 0.3), 2)
        hx = [(r * math.cos(TAU * j / 6), r * math.sin(TAU * j / 6)) for j in range(6)]
        hexa = T.polyline(hx + [hx[0]], 0.025) * kh
    q = np.random.default_rng(66)
    fa = []
    u = rel(t, t0, t0 + 0.55)
    if 0 < u < 1:
        for _ in range(16):
            a = q.uniform(-2.4, 2.4)
            v = q.uniform(0.45, 1.05)
            x = math.cos(a) * v * ease_out(u, 1.6) * 0.8
            y = math.sin(a) * v * ease_out(u, 1.6) * 0.6 + 0.5 * u * u
            fa.append((x - 0.07 * math.cos(a), y - 0.07 * math.sin(a), x, y, 1 - u))
    faiscas = T.tapered(fa, 0.026) if fa else T.zero()
    clarao = T.gauss(0, 0, 0.16) * pulso(t, t0, t0 + 0.16) * 2.3
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.4 + jato * 1.3 + hexa * 1.3 + faiscas * 2.0 + clarao) * env
    H += (corpo * 0.3 + (d + placas) * vis * 0.9 + jato * 1.0 + hexa * 0.8 + faiscas * 1.1 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Thanos
def soco_da_manopla(T, t, rng):
    """Thanos: a Manopla do Infinito, enorme, desce num soco lento e pesado com as seis Joias brilhando nos
    nós dos dedos e no dorso; o chão do impacto racha em linhas e sobe uma onda grossa."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    vem = ease_in(rel(t, 0.0, 0.3), 2.2)
    px = -1.0 + 0.82 * vem - 0.16 * ease_out(rel(t, 0.36, 0.7), 2)
    py = -0.12 + 0.12 * vem
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.52, 0.68))
    M, d = _mao(T, px, py, 1.15, 'manopla')
    A, B = _antebraco(T, px, py, 1.2, 0.48, 0.15, (0.15, 0.06))
    corpo = np.clip(M + A, 0, 1) * vis
    joias = T.zero()
    for k in range(4):
        joias += T.gauss(px + 0.13 * 1.15 * 1.3, py + (-0.13 + 0.087 * k) * 1.15 * 1.3, 0.022)
    joias += T.gauss(px - 0.03, py - 0.02, 0.035) + T.gauss(px - 0.07, py - 0.2, 0.022)
    joias *= vis * (0.8 + 0.4 * math.sin(t * 25))
    t0 = 0.3
    racha = T.zero()
    kr = janela(t, t0, t0 + 0.05) * apaga(t, t0 + 0.3, 0.95)
    if kr > 0:
        for j in range(7):
            a = -2.6 + 1.0 * j / 6 * 5.2
            pts = jagged(np.random.default_rng(700 + j), 0.0, 0.0, 0.62 * math.cos(a), 0.62 * math.sin(a) * 0.75, 3, 0.18)
            n = max(2, int(len(pts) * ease_out(rel(t, t0, t0 + 0.22), 2)))
            racha += T.polyline(pts[:n], 0.022)
        racha *= kr
    onda = _anel(T, t, t0, t0 + 0.5, 0.12, 0.74, 0.08, 1.6)
    est = _estrela_de_contato(T, t, t0, 0.36, 8, 0.4, 0.2, 0.36)
    clarao = T.gauss(0, 0, 0.22) * pulso(t, t0, t0 + 0.22) * 2.2
    G += (corpo * 1.05 + T.blur(corpo, 0.025) * 0.45 + racha * 1.3 + onda * 1.3 + est * 1.1 + clarao) * env
    H += (corpo * 0.25 + B * vis * 0.6 + joias * 2.2 + racha * 0.8 + onda * 0.4 + est + clarao * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Gohan
def soco_do_gohan(T, t, rng):
    """Gohan: um soco calmo e reto, de quem foi treinado pelo Piccolo; a aura branca contorna o braço só no
    instante do golpe e o impacto abre dois anéis de ar, um dentro do outro, sem exagero."""
    G, H = vazio(T)
    env = apaga(t, 0.74, 1)
    px = _vai_e_volta(t, 0.24, recua=0.15)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.1)
    A, B = _antebraco(T, px, 0.0, 1.1, 0.46, 0.115, (0.55, 0.1))
    corpo = np.clip(M + A, 0, 1) * vis
    contorno = np.clip(T.blur(corpo, 0.03) * 2.2 - corpo * 1.6, 0, 1) * pulso(t, 0.08, 0.4)
    t0 = 0.24
    aneis = _anel(T, t, t0, t0 + 0.42, 0.1, 0.62, 0.04, 1.2) + _anel(T, t, t0 + 0.08, t0 + 0.5, 0.06, 0.38, 0.03, 1.2)
    est = _estrela_de_contato(T, t, t0, 0.26, 8, 0.42)
    poeira = _riscos(T, t, t0, 0.32, 6, 0.2, 0.5, 0.02, 8, -0.9, 0.9)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + contorno * 1.2 + aneis * 1.3 + est + poeira + clarao) * env
    H += (corpo * 0.3 + B * vis * 0.8 + d * vis * 0.8 + contorno * 1.3 + aneis * 0.5 + est * 0.9 + poeira * 0.6 + clarao * 1.2) * env
    return G, H


REGISTRO = [
    ("soco_saiyajin", soco_saiyajin, GRANDE, "básico do Goku: munhequeira azul, ki dourado no punho e a onda de ar com poeira", False),
    ("soco_do_principe", soco_do_principe, GRANDE, "básico do Vegeta: a luva branca, o ki azul estalando e a estrela afiada", False),
    ("soco_do_naruto", soco_do_naruto, GRANDE, "básico do Naruto: a manga larga, a espiral do Uzumaki e o puf de fumaça", False),
    ("soco_infinito", soco_infinito, GRANDE, "básico do Gojo: o punho para no Infinito e entra de uma vez", False),
    ("soco_veloz_flash", soco_veloz_flash, GRANDE, "básico do Flash: três punhos-fantasma e os raios", False),
    ("soco_de_armadura", soco_de_armadura, GRANDE, "básico do Homem de Ferro: manopla com propulsores, clang e faíscas", False),
    ("soco_da_manopla", soco_da_manopla, GRANDE, "básico do Thanos: a Manopla do Infinito com as Joias e o chão rachando", False),
    ("soco_do_gohan", soco_do_gohan, GRANDE, "básico do Gohan: soco calmo, aura branca no braço e dois anéis de ar", False),
]
