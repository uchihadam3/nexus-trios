"""Ataques básicos com animação própria, lote z: Seiya, Hyoga, Ikki, Saga, Aiolia, Doutor Destino, Tifa e Cabeça de
Pirâmide.

Golpes simples, cada um do personagem: o punho de armadura do Seiya com as penas de Pégaso voando no acerto, o soco
gelado do Hyoga com os flocos de neve de seis pontas, o punho em chamas da Fênix do Ikki com as plumas de fogo, os
dois punhos sobrepostos de Gêmeos do Saga com o brilho de galáxia, o soco do Aiolia com a juba dourada do leão
abrindo no acerto, a manopla de ferro do Destino com o selo verde de magia, os três socos curtos de luva da Tifa e a
Grande Faca do Cabeça de Pirâmide descendo pesada com a ferrugem voando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


def _pena(T, cx, cy, tam, ang):
    """Uma pena: a haste e as duas metades da pluma, mais larga no meio."""
    pts = [(-1.0, 0.0), (-0.5, -0.22), (0.3, -0.25), (1.0, 0.0), (0.3, 0.2), (-0.5, 0.18)]
    pl = T.polys([(_pts(pts, cx, cy, tam, ang), 1.0)], 0.003)
    haste = T.polyline(_pts([(-1.15, 0.0), (1.0, 0.0)], cx, cy, tam, ang), 0.006)
    return pl, haste


def _floco(T, cx, cy, r, ang):
    """Floco de neve de seis pontas com os galhinhos."""
    segs = []
    for k in range(6):
        a = ang + TAU * k / 6
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        segs.append((cx, cy, x2, y2, 1.0))
        mx, my = cx + 0.6 * r * math.cos(a), cy + 0.6 * r * math.sin(a)
        for s in (-1, 1):
            segs.append((mx, my, mx + 0.3 * r * math.cos(a + s * 0.8), my + 0.3 * r * math.sin(a + s * 0.8), 1.0))
    return T.lines(segs, max(0.006, r * 0.12))


# ------------------------------------------------------------------ Seiya
def soco_de_pegaso(T, t, rng):
    """Seiya: o punho com a manopla da armadura de bronze vem num soco reto e, no acerto, penas de Pégaso se
    soltam em leque e caem girando (um soco só, não o Meteoro)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.18, 1.1, 'luva', faixa=(0.05, 0.12))
    placa = T.zero()
    if vis > 0.05:
        placa = T.polyline(_pts([(-0.12, -0.17), (-0.2, -0.24), (-0.32, -0.2)], px, 0.0, 1.1), 0.014) * vis
    t0 = 0.2
    u = rel(t, t0 + 0.02, t0 + 0.7)
    penas_g, penas_h = T.zero(), T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(15)
        for _ in range(7):
            a = q.uniform(-2.6, -0.2)
            dd = q.uniform(0.25, 0.6) * ease_out(min(1, u * 1.6), 2)
            x = dd * math.cos(a) + 0.06 * math.sin(u * 8 + a)
            y = dd * math.sin(a) + 0.45 * u * u
            g, h = _pena(T, x, y, 0.13, a + u * 3)
            penas_g += g * (1 - u)
            penas_h += h * (1 - u)
    est = _estrela_de_contato(T, t, t0, 0.3, 8, 0.38)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + penas_g * 1.3 + est + clarao) * env
    H += (corpo * 0.3 + (d + B + placa) * 0.8 + penas_h * 1.2 + penas_g * 0.3 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Hyoga
def soco_do_cisne(T, t, rng):
    """Hyoga: o punho vem soltando a névoa fria do Pó de Diamante e, no acerto, flocos de neve de seis pontas se
    abrem em volta e ficam girando um instante no ar."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.22, 0.16, 1.1, 'luva', faixa=(0.05, 0.1))
    brilhos = T.zero()
    if vis > 0.05:
        q = np.random.default_rng(int(t * 30))
        brilhos = T.splats([(px - q.uniform(0.1, 0.6), q.uniform(-0.18, 0.18), q.uniform(0.4, 1)) for _ in range(10)], 0.012) * vis
    t0 = 0.22
    flocos = T.zero()
    kf = janela(t, t0, t0 + 0.08) * apaga(t, t0 + 0.35, 0.9)
    if kf > 0:
        abre = ease_out(rel(t, t0, t0 + 0.3), 2)
        for k in range(6):
            a = TAU * k / 6 + 0.3
            dd = 0.18 + 0.3 * abre
            flocos += _floco(T, dd * math.cos(a), dd * math.sin(a) + 0.08 * rel(t, t0, 1), 0.07 + 0.03 * (k % 2), t * 2 + k)
        flocos += _floco(T, 0, 0, 0.16 * abre, -t * 2)
        flocos *= kf
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 1.8
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + brilhos * 1.2 + flocos * 1.5 + clarao) * env
    H += (corpo * 0.35 + (d + B) * 0.8 + brilhos * 1.2 + flocos * 1.1 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Ikki
def soco_da_fenix(T, t, rng):
    """Ikki: o punho pega fogo no caminho, as labaredas sobem como plumas, e o acerto espalha penas de fogo que
    sobem queimando, como a Fênix."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.22, 0.16, 1.1, 'luva', faixa=(0.05, 0.1))
    fogo = T.zero()
    kf = janela(t, 0.04, 0.12) * vis
    if kf > 0:
        segs = []
        for j in range(10):
            x0 = px - 0.4 + 0.055 * j
            alto = 0.12 + 0.07 * math.sin(t * 34 + j * 2)
            segs.append((x0, -0.12, x0 - 0.1, -0.12 - alto, 1.0))
        fogo = T.tapered(segs, 0.05) * kf
    t0 = 0.22
    u = rel(t, t0, t0 + 0.65)
    plumas_g, plumas_h = T.zero(), T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(29)
        for _ in range(7):
            a = q.uniform(-2.8, -0.3)
            dd = q.uniform(0.2, 0.55) * ease_out(u, 1.8)
            g, h = _pena(T, dd * math.cos(a), dd * math.sin(a) - 0.3 * u, 0.13, a)
            plumas_g += g * (1 - u)
            plumas_h += h * (1 - u)
    est = _estrela_de_contato(T, t, t0, 0.32, 8, 0.36, 0.2, 0.32)
    clarao = T.gauss(0, 0, 0.17) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + fogo * 1.3 + plumas_g * 1.4 + est + clarao) * env
    H += (corpo * 0.3 + (d + B) * 0.7 + fogo * 0.5 + plumas_h * 1.0 + plumas_g * 0.4 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Saga
def soco_de_gemeos(T, t, rng):
    """Saga: dois punhos iguais chegam juntos, um levemente deslocado do outro (as duas faces de Gêmeos), e o acerto
    abre um brilho de galáxia: um redemoinho de pontinhos de estrela."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.22, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    corpo = T.zero()
    det = T.zero()
    for k, (dy, a) in enumerate([(-0.07, 1.0), (0.07, 0.55)]):
        M, d = _mao(T, px - 0.05 * k, dy, 1.0, 'luva')
        A, _ = _antebraco(T, px - 0.05 * k, dy, 1.0, 0.4, 0.1)
        corpo += np.clip(M + A, 0, 1) * a
        det += d * a
    corpo = np.clip(corpo, 0, 1) * vis
    t0 = 0.22
    u = rel(t, t0, t0 + 0.6)
    galaxia = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(55)
        pts = []
        for j in range(40):
            braco = j % 2
            s = q.uniform(0.1, 1.0)
            a = braco * math.pi + s * 4 + u * 3
            r = s * 0.62 * (0.5 + 0.5 * ease_out(u, 2))
            pts.append((r * math.cos(a), r * math.sin(a) * 0.7, (1 - u) * q.uniform(0.5, 1.0)))
        galaxia = T.splats(pts, 0.025) + T.gauss(0, 0, 0.1) * (1 - u) * 1.4
    est = _estrela_de_contato(T, t, t0, 0.28, 8, 0.38)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + galaxia * 1.4 + est) * env
    H += (corpo * 0.3 + det * vis * 0.8 + galaxia * 1.1 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Aiolia
def soco_do_leao_dourado(T, t, rng):
    """Aiolia: o soco reto e rápido do Cavaleiro de Leão e, no acerto, a juba dourada se abre em volta do ponto do
    golpe (mechas em leque que tremem) com um estalo de luz."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.18, 0.16, 1.1, 'luva', faixa=(0.05, 0.12))
    t0 = 0.18
    juba = T.zero()
    kj = pulso(t, t0, t0 + 0.5)
    if kj > 0:
        segs = []
        for j in range(16):
            a = TAU * j / 16
            r0 = 0.14
            r1 = r0 + (0.24 + 0.08 * math.sin(j * 1.9 + t * 30)) * (0.5 + 0.5 * kj)
            curva = 0.25
            segs.append((r0 * math.cos(a), r0 * math.sin(a), r1 * math.cos(a + curva), r1 * math.sin(a + curva), 1.0))
        juba = T.tapered(segs, 0.06) * kj
    est = _estrela_de_contato(T, t, t0, 0.24, 8, 0.4)
    clarao = T.gauss(0, 0, 0.14) * pulso(t, t0, t0 + 0.16) * 2.4
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + juba * 1.3 + est + clarao) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + juba * 0.6 + est * 0.9 + clarao * 1.3) * env
    return G, H


# ------------------------------------------------------------------ Doutor Destino
def soco_de_ferro_destino(T, t, rng):
    """Doutor Destino: a manopla de ferro (placas e rebites) sai da manga do manto num soco frio, e o acerto acende o
    selo verde de magia: um círculo com runas que gira e apaga."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.22, recua=0.16)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, 0.0, 1.1, 'armadura')
    manga = T.polys([(_pts([(-0.2, -0.13), (-0.55, -0.24), (-0.62, 0.0), (-0.55, 0.25), (-0.2, 0.14)], px, 0.0, 1.1), 0.8)], 0.006)
    corpo = np.clip(M + manga, 0, 1) * vis
    rebites = sum(T.gauss(px + dx, dy, 0.012) for dx, dy in [(-0.08, -0.12), (-0.08, 0.12), (0.08, -0.12), (0.08, 0.12)]) * vis
    t0 = 0.22
    selo = T.zero()
    ks = pulso(t, t0, t0 + 0.55)
    if ks > 0:
        r = 0.28 + 0.1 * ease_out(rel(t, t0, t0 + 0.3), 2)
        selo = T.ring(r, 0.016, 0, 0, 1.0) + T.ring(r * 0.72, 0.01, 0, 0, 1.0)
        rot = t * 3
        runas = []
        for k in range(8):
            a = rot + TAU * k / 8
            cx, cy = r * 0.86 * math.cos(a), r * 0.86 * math.sin(a)
            runas.append((cx - 0.02 * math.sin(a), cy + 0.02 * math.cos(a), cx + 0.02 * math.sin(a), cy - 0.02 * math.cos(a), 1.0))
        selo += T.lines(runas, 0.012)
        tri = [(r * 0.72 * math.cos(-rot + TAU * k / 3 - math.pi / 2), r * 0.72 * math.sin(-rot + TAU * k / 3 - math.pi / 2)) for k in range(4)]
        selo += T.polyline(tri, 0.01)
        selo *= ks
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + selo * 1.4 + T.blur(selo, 0.02) * 0.5 + est) * env
    H += (corpo * 0.3 + (d * vis + rebites * 1.4) + selo * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Tifa
def socos_de_luva_tifa(T, t, rng):
    """Tifa: três socos curtos de luva em sequência rápida, alternando a altura, e cada um deixa uma estrelinha;
    o último acerta mais firme e abre um anel."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k, (a0, y) in enumerate([(0.0, -0.12), (0.1, 0.1), (0.2, 0.0)]):
        u = ease_in(rel(t, a0, a0 + 0.1), 1.4)
        if u <= 0:
            continue
        v = ease_out(rel(t, a0 + 0.12, a0 + 0.26), 2)
        px = -0.85 + 0.72 * u - 0.32 * v
        vis = 1 - rel(t, a0 + 0.2, a0 + 0.3)
        M, d = _mao(T, px, y, 0.9, 'luva')
        A, B = _antebraco(T, px, y, 0.9, 0.38, 0.1, (0.0, 0.1))
        corpo = np.clip(M + A, 0, 1) * vis
        t0 = a0 + 0.1
        est = T.polys([(estrela(0.02, y, (0.18 + 0.08 * (k == 2)) * pulso(t, t0, t0 + 0.22) + 0.01, 0.4 * k, 5, 0.42), 1.0)], 0.003) * pulso(t, t0, t0 + 0.22)
        G += corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + est * 1.2
        H += corpo * 0.3 + (d + B) * vis * 0.8 + est
    anel = _anel(T, t, 0.3, 0.7, 0.1, 0.5, 0.04, 1.2)
    G += anel * 1.2
    H += anel * 0.4
    return G * env, H * env


# ------------------------------------------------------------------ Cabeça de Pirâmide
_FACA = [(-0.9, -0.05), (0.25, -0.12), (0.48, -0.06), (0.5, 0.04), (0.25, 0.1), (-0.9, 0.05)]


def grande_faca_piramide(T, t, rng):
    """Cabeça de Pirâmide: a Grande Faca, uma lâmina enorme e enferrujada, sobe devagar e desce pesada no alvo,
    soltando faíscas e lascas de ferrugem que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sobe = ease_out(rel(t, 0.0, 0.18), 2)
    desce = ease_in(rel(t, 0.18, 0.34), 2.4)
    ang = -1.3 * sobe + 1.55 * desce
    piv = (-0.85, -0.05)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.6, 0.76))
    lam = T.polys([(_pts(_FACA, piv[0] + 0.75 * math.cos(ang), piv[1] + 0.75 * math.sin(ang), 1.0, ang), 1.0)], 0.004) * vis
    gume = T.polyline(_pts([(-0.8, -0.04), (0.42, -0.08)], piv[0] + 0.75 * math.cos(ang), piv[1] + 0.75 * math.sin(ang), 1.0, ang), 0.01) * vis
    t0 = 0.34
    faiscas = _riscos(T, t, t0, 0.4, 12, 0.1, 0.55, 0.026, 99, -2.8, -0.3)
    ferrugem = _gotas(T, t, t0, 0.7, 16, 13, tam=0.022, cai=0.6, alcance=0.5, a0=-2.8, a1=0.2)
    onda = _anel(T, t, t0, t0 + 0.5, 0.12, 0.66, 0.07, 1.8)
    clarao = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (lam * 1.05 + T.blur(lam, 0.025) * 0.4 + faiscas * 1.4 + ferrugem * 1.2 + onda * 1.2 + clarao) * env
    H += (lam * 0.25 + gume * 1.2 + faiscas * 1.0 + ferrugem * 0.3 + onda * 0.4 + clarao * 1.1) * env
    return G, H


REGISTRO = [
    ("soco_de_pegaso", soco_de_pegaso, GRANDE, "básico do Seiya: a manopla de bronze e as penas de Pégaso", False),
    ("soco_do_cisne", soco_do_cisne, GRANDE, "básico do Hyoga: o soco gelado e os flocos de neve", False),
    ("soco_da_fenix", soco_da_fenix, GRANDE, "básico do Ikki: o punho em chamas e as plumas de fogo", False),
    ("soco_de_gemeos", soco_de_gemeos, GRANDE, "básico do Saga: os dois punhos de Gêmeos e a galáxia", False),
    ("soco_do_leao_dourado", soco_do_leao_dourado, GRANDE, "básico do Aiolia: o soco e a juba dourada abrindo", False),
    ("soco_de_ferro_destino", soco_de_ferro_destino, GRANDE, "básico do Doutor Destino: a manopla de ferro e o selo verde", False),
    ("socos_de_luva_tifa", socos_de_luva_tifa, GRANDE, "básico da Tifa: três socos curtos de luva", False),
    ("grande_faca_piramide", grande_faca_piramide, GRANDE, "básico do Cabeça de Pirâmide: a Grande Faca descendo pesada", False),
]
