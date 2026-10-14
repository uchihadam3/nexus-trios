"""Ataques básicos com animação própria, lote zg: Leonardo, Samurai Jack, Kenpachi, Link, Dante, Geralt, Alucard e Trunks.

As duas katanas cruzadas do Leonardo com o casco brilhando, o golpe único e calmo do Samurai Jack com as folhas
caindo, a pancada brutal da espada dentada do Kenpachi com a aura amarela, o giro da espada do Link, a estocada da
Rebellion e os dois tiros do Dante, a espada de prata e o Sinal do Geralt, o corte do Alucard que vira morcegos e a
rede de cortes do Trunks.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_ze import _arco_de_corte


# ------------------------------------------------------------------ Leonardo
def katanas_gemeas_leonardo(T, t, rng):
    """Leonardo: as duas katanas cortam juntas em X, uma de cada lado, e o hexágono do casco de tartaruga brilha atrás
    do acerto, com a faixa azul da bandana esvoaçando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cortes = T.zero()
    for x1, y1, x2, y2 in ((-0.6, -0.5, 0.55, 0.45), (-0.6, 0.5, 0.55, -0.45)):
        k = rel(t, 0.02, 0.16)
        if k > 0:
            cortes += T.polys([(lamina(x1, y1, x2, y2, 0.045, ease_out(k, 2.5), rel(t, 0.28, 0.5)), 1.0)], 0.002)
    kh = pulso(t, 0.16, 0.6)
    casco = T.zero()
    if kh > 0:
        r = 0.3 * back(rel(t, 0.16, 0.3), 1.8)
        pts = [(math.cos(a) * r, math.sin(a) * r) for a in np.linspace(0, TAU, 7) + math.pi / 6]
        casco = T.polyline(pts, 0.025) * kh
        casco += sum(T.lines([(0, 0, math.cos(a) * r, math.sin(a) * r, 0.6)], 0.012) for a in np.linspace(0, TAU, 7)[:-1] + math.pi / 6) * kh
    faixa = T.zero()
    kf = janela(t, 0.0, 0.06) * (1 - rel(t, 0.3, 0.5))
    if kf > 0:
        pts = [(-0.55 - 0.35 * s, -0.55 + 0.08 * math.sin(s * 9 - t * 30)) for s in np.linspace(0, 1, 14)]
        faixa = T.polyline(pts, 0.035) * kf
    est = _estrela_de_contato(T, t, 0.16, 0.24, 8, 0.32)
    G += (T.glow(cortes, 1.1, 0.7, 0.02) + casco * 1.1 + faixa * 0.9 + est) * env
    H += (cortes * 1.5 + casco * 0.6 + faixa * 0.4 + est) * env
    return G, H


# ------------------------------------------------------------------ Samurai Jack
def golpe_unico_jack(T, t, rng):
    """Samurai Jack: um instante parado (só o brilho do fio na bainha), um único corte horizontal, reto e enorme, e as
    folhas caindo devagar no silêncio depois."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    brilho = T.flare(-0.65, 0.0, 0.5, 0.0, 0.008) * pulso(t, 0.0, 0.2) * 1.2
    k = rel(t, 0.18, 0.24)
    corte = T.zero()
    if k > 0:
        corte = T.polys([(lamina(-0.95, 0.02, 0.95, -0.02, 0.03, ease_out(k, 4), rel(t, 0.5, 0.72)), 1.0)], 0.002)
    eco = T.lines([(-0.95, -0.06, 0.95, -0.06, 0.4), (-0.95, 0.08, 0.95, 0.08, 0.3)], 0.006) * pulso(t, 0.22, 0.45)
    folhas = T.zero()
    q = np.random.default_rng(101)
    for j in range(6):
        x0, atraso = q.uniform(-0.6, 0.6), q.uniform(0.0, 0.2)
        u = rel(t, 0.3 + atraso, 1.0)
        if 0 < u < 1:
            x, y = x0 + 0.1 * math.sin(u * 7 + j), -0.6 + 1.0 * u
            folhas += T.polys([(_elipse_pts(x, y, 0.05, 0.022, u * 6 + j, 10), 1.0)], 0.003) * (1 - u) ** 0.5
    G += (brilho + T.glow(corte, 1.3, 0.9, 0.02) + eco + folhas * 0.9) * env
    H += (brilho * 1.2 + corte * 1.8 + eco * 0.5 + folhas * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Kenpachi
def corte_brutal_kenpachi(T, t, rng):
    """Kenpachi: a espada cheia de dentes desce de cima numa pancada bruta, sem técnica nenhuma, e a pressão espiritual
    amarela explode em volta em pontas, o chão rachando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.18, -2.0, -0.6 + math.pi, 0.5, 0.2, some=(0.3, 0.55))
    ca, sa = math.cos(ah), math.sin(ah)
    vis = 1 - rel(t, 0.2, 0.3)
    nx, ny = -sa, ca
    dentes = []
    for j in range(6):
        u = 0.25 + 0.1 * j
        bx, by = ca * u, sa * u
        dentes.append(([(bx, by), (bx + nx * 0.06 + ca * 0.03, by + ny * 0.06 + sa * 0.03), (bx + ca * 0.08, by + sa * 0.08)], 1.0))
    espada = (T.polys([(lamina(ca * 0.15, sa * 0.15, ca * 0.9, sa * 0.9, 0.05), 1.0)] + dentes, 0.002)) * vis
    ka = pulso(t, 0.18, 0.6)
    aura = T.zero()
    if ka > 0:
        r = 0.2 + 0.25 * ease_out(rel(t, 0.18, 0.5), 2)
        aura = T.polys([(estrela(0, 0, r + 0.15 * ka, 0.1, 14, 0.55), 1.0)], 0.01) * ka
        aura -= T.polys([(estrela(0, 0, r * 0.7, 0.1, 14, 0.55), 1.0)], 0.01) * ka
        aura = np.clip(aura, 0, 1)
    racha = T.lines([(0, 0.25, -0.35, 0.55, 1), (0, 0.25, 0.1, 0.6, 1), (0, 0.25, 0.4, 0.5, 1)], 0.014) * pulso(t, 0.2, 0.7)
    G += (T.glow(rastro, 1.1, 0.9, 0.04) + fio + espada * 1.2 + aura * 1.2 + racha) * env
    H += (fio * 1.4 + rastro * 0.3 + espada + aura * 0.6 + racha * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Link
def giro_da_espada_link(T, t, rng):
    """Link: o giro com a espada (o ataque giratório), um círculo inteiro de corte em volta do alvo com as faíscas
    verdes da carga, e o "tlim" de brilho no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_out(rel(t, 0.02, 0.28), 2)
    sai = apaga(t, 0.36, 0.62)
    giro = T.arc_band(0.5, 0.15, -1.6, -1.6 + TAU * p + 0.01, squash=0.65, crescente=True) * sai
    fio = T.arc_band(0.54, 0.04, -1.6, -1.6 + TAU * p + 0.01, squash=0.65, crescente=True) * sai
    ah = -1.6 + TAU * p
    ca, sa = math.cos(ah), math.sin(ah) * 0.65
    espada = T.polys([(lamina(ca * 0.12, sa * 0.12, ca * 0.62, sa * 0.62, 0.035), 1.0)], 0.002) * (1 - rel(t, 0.28, 0.36))
    faiscas = _riscos(T, t, 0.06, 0.35, 10, 0.3, 0.6, 0.016, 19, 0.0, TAU)
    tlim = T.flare(0.25, -0.3, 0.45, 0.4, 0.01) * pulso(t, 0.3, 0.55) * 1.3
    G += (T.glow(giro, 1.0, 0.8, 0.03) + fio + espada * 1.2 + faiscas + tlim) * env
    H += (fio * 1.4 + espada + faiscas * 0.8 + tlim * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Dante
def rebellion_dante(T, t, rng):
    """Dante: a Rebellion vem numa estocada (o Stinger) com o casaco vermelho em rastro, crava no alvo, e as duas
    pistolas (Ebony & Ivory) dão dois tiros rápidos de estilo no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vem = ease_in(rel(t, 0.0, 0.16), 1.5)
    px = -0.95 + 0.85 * vem
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.3, 0.4))
    espada = T.polys([(lamina(px - 0.55, 0.0, px + 0.1, 0.0, 0.05), 1.0)], 0.002) * vis
    guarda = T.polys([(_elipse_pts(px - 0.5, 0.0, 0.03, 0.09, 0.0, 10), 1.0)], 0.002) * vis
    casaco = T.zero()
    if vis > 0:
        for j in range(3):
            pts = [(px - 0.55 - 0.4 * s, 0.05 * (j - 1) + 0.06 * math.sin(s * 8 + t * 25 + j)) for s in np.linspace(0, 1, 12)]
            casaco += T.polyline(pts, 0.03) * (0.8 - 0.2 * j)
        casaco *= vis
    tiros = T.zero()
    for j, t0 in enumerate((0.36, 0.46)):
        k = pulso(t, t0, t0 + 0.1)
        if k > 0:
            y = -0.12 + 0.24 * j
            tiros += T.tapered([(-0.6, y, 0.0, y * 0.3, 1.0)], 0.025) * k + T.flare(0.0, y * 0.3, 0.3, 0.0, 0.01) * k
    est = _estrela_de_contato(T, t, 0.16, 0.28, 8, 0.3)
    G += (espada * 1.2 + guarda + casaco * 0.9 + tiros * 1.2 + est) * env
    H += (espada * 1.2 + casaco * 0.3 + tiros + est) * env
    return G, H


# ------------------------------------------------------------------ Geralt
def espada_de_prata_geralt(T, t, rng):
    """Geralt: um corte em pirueta com a espada de prata (o arco largo e baixo) e, no acerto, o Sinal de bruxo
    desenhado no ar (o triângulo com as três linhas do Aard) solta uma onda que empurra."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.22, -3.0, 0.3, 0.55, 0.13, squash=0.7)
    ca, sa = math.cos(ah), math.sin(ah) * 0.7
    espada = T.polys([(lamina(ca * 0.12, sa * 0.12, ca * 0.7, sa * 0.7, 0.03), 1.0)], 0.002) * (1 - rel(t, 0.24, 0.32))
    ks = pulso(t, 0.22, 0.6)
    sinal = T.zero()
    if ks > 0:
        s = 0.22 * back(rel(t, 0.22, 0.34), 1.8)
        tri = [(0, -s), (s * 0.87, s * 0.5), (-s * 0.87, s * 0.5), (0, -s)]
        sinal = T.polyline(tri, 0.02) * ks
        sinal += T.lines([(0, -s * 0.2, 0, s * 0.5, 1), (-s * 0.3, s * 0.05, s * 0.3, s * 0.05, 1)], 0.014) * ks
    onda = _anel(T, t, 0.3, 0.65, 0.15, 0.55, 0.05)
    G += (T.glow(rastro, 1.0, 0.7, 0.03) + fio + espada * 1.2 + sinal * 1.2 + onda) * env
    H += (fio * 1.5 + espada + sinal * 0.9 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Alucard (Castlevania)
def corte_dos_morcegos(T, t, rng):
    """Alucard: um corte elegante e fino da espada, e o rastro do corte se desfaz em morcegos que batem as asas e voam
    para longe."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = rel(t, 0.0, 0.16)
    corte = T.zero()
    if k > 0:
        corte = T.polys([(lamina(-0.7, 0.45, 0.7, -0.45, 0.035, ease_out(k, 3), rel(t, 0.22, 0.42)), 1.0)], 0.002)
    morcegos = T.zero()
    q = np.random.default_rng(47)
    for j in range(6):
        s = q.uniform(0.1, 0.9)
        x0, y0 = -0.7 + 1.4 * s, 0.45 - 0.9 * s
        a = q.uniform(-2.6, -0.5)
        u = rel(t, 0.22 + 0.03 * j, 0.85)
        if 0 < u < 1:
            x, y = x0 + math.cos(a) * 0.6 * u, y0 + math.sin(a) * 0.6 * u
            bate = 0.5 + 0.5 * math.sin(u * 40 + j)
            e = 0.06
            asa = [(x - e * 1.6, y - e * bate), (x - e * 0.6, y + e * 0.2), (x, y - e * 0.2), (x + e * 0.6, y + e * 0.2), (x + e * 1.6, y - e * bate), (x, y + e * 0.5)]
            morcegos += T.polys([(asa, 1.0)], 0.002) * (1 - u)
    G += (T.glow(corte, 1.2, 0.8, 0.02) + morcegos * 1.2) * env
    H += (corte * 1.6 + morcegos * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Trunks
def grade_de_cortes_trunks(T, t, rng):
    """Trunks: a espada passa quatro vezes, rápida demais (duas na horizontal e duas na vertical), deixando uma rede de
    cortes no alvo, e o ki dourado estoura no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cortes = T.zero()
    linhas = ((-0.6, -0.15, 0.6, -0.18), (-0.15, -0.6, -0.12, 0.6), (-0.6, 0.15, 0.6, 0.12), (0.15, -0.6, 0.18, 0.6))
    for j, (x1, y1, x2, y2) in enumerate(linhas):
        t0 = 0.02 + 0.05 * j
        k = rel(t, t0, t0 + 0.06)
        if k > 0:
            cortes += T.polys([(lamina(x1, y1, x2, y2, 0.025, ease_out(k, 3), rel(t, 0.42 + 0.03 * j, 0.62)), 1.0)], 0.002)
    ki = T.gauss(0, 0, 0.18) * pulso(t, 0.24, 0.5) * 1.2
    est = _estrela_de_contato(T, t, 0.26, 0.32, 10, 0.32)
    G += (T.glow(cortes, 1.1, 0.7, 0.02) + ki + est) * env
    H += (cortes * 1.5 + ki * 0.6 + est) * env
    return G, H


REGISTRO = [
    ("katanas_gemeas_leonardo", katanas_gemeas_leonardo, GRANDE, "básico do Leonardo: as duas katanas em X e o casco", False),
    ("golpe_unico_jack", golpe_unico_jack, GRANDE, "básico do Samurai Jack: o golpe único e as folhas caindo", False),
    ("corte_brutal_kenpachi", corte_brutal_kenpachi, GRANDE, "básico do Kenpachi: a espada dentada e a aura amarela", False),
    ("giro_da_espada_link", giro_da_espada_link, GRANDE, "básico do Link: o ataque giratório e o brilho", False),
    ("rebellion_dante", rebellion_dante, GRANDE, "básico do Dante: a estocada da Rebellion e os dois tiros", False),
    ("espada_de_prata_geralt", espada_de_prata_geralt, GRANDE, "básico do Geralt: a espada de prata e o Sinal", False),
    ("corte_dos_morcegos", corte_dos_morcegos, GRANDE, "básico do Alucard: o corte que vira morcegos", False),
    ("grade_de_cortes_trunks", grade_de_cortes_trunks, GRANDE, "básico do Trunks: a rede de cortes e o ki dourado", False),
]
