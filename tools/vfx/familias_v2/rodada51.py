"""Rodada 51 das habilidades próprias: Chucky, Pennywise, Ghostface, Leatherface, Pinhead e Samara.

Chucky
- facada_do_chucky: o boneco pulando com a faca e as facadas rápidas.
- risada_do_chucky: o "HA HA HA" em letras saltando e as espirais nos rivais (Confuso).
- chucky_preparo: o Preparo do Vodu — o boneco de vodu com os alfinetes e a vela tremendo (laço).
- vodu: o alfinete entrando no boneco e a dor atravessando o rival (Amaldiçoado).

Pennywise
- baloes_vermelhos: os balões subindo e flutuando até o rival, o "pop" (Confuso e Invocação).
- luzes_da_morte: as três luzes girando na boca do palhaço e o transe em todos os rivais (Confuso e Enfraquecido).
- pennywise_preparo: o Preparo do Medo puro — o balão vermelho balançando e os olhos amarelos (laço).
- medo_puro: a boca enorme cheia de dentes abrindo e fechando no rival.

Ghostface
- ligacao_do_ghostface: o telefone tocando, as ondas da ligação e a mira no rival (Marcado e Exposto).
- facada_do_ghostface: a máscara surgindo atrás do rival e a facada.
- ghostface_preparo: o Preparo do Grito final — a máscara do Pânico com o manto esvoaçando (laço).
- grito_final: a máscara gritando em ondas e as facadas em sequência.

Leatherface
- motosserra_de_leatherface: a motosserra roncando, as faíscas e o sangue (Sangrando).
- danca_da_serra: o giro com a serra erguida, o círculo de faíscas sobre todos os rivais (Sangrando).
- leatherface_preparo: o Preparo do Massacre — a motosserra acelerando com a fumaça (laço).
- massacre_da_serra: a serra descendo em cheio no rival e a chuva de faíscas.

Pinhead
- correntes_com_ganchos: as correntes saindo do escuro e os ganchos fisgando todos os rivais (Preso).
- dor_e_prazer: o rosto com a grade de pregos e a corrente puxando o rival (Amaldiçoado).
- pinhead_preparo: o Preparo da Caixa de Lemarchand — a caixa girando e abrindo os padrões dourados (laço).
- caixa_de_lemarchand: a caixa abrindo, as correntes saindo para todos e o silêncio (Silenciado).

Samara
- maldicao_de_sete_dias: o anel da fita e o "7" queimando no rival (Amaldiçoado e Enfraquecido).
- estatica_de_samara: a TV chiando, a estática varrendo todos os rivais (Silenciado).
- samara_preparo: o Preparo do Sai da TV — o poço, o anel de luz e a água pingando (laço).
- sai_da_tv: a TV com a estática e a mão saindo da tela pegando o rival.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CHAMA, GOTA, anel, cheio, clarao, converge, corte, estouro, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


_FACA = [(0, -1), (0.16, -0.7), (0.16, 0.2), (0.1, 0.25), (0.1, 0.95), (-0.1, 0.95), (-0.1, 0.25), (-0.02, 0.2), (-0.02, -0.7)]


def _espiral(T, cx, cy, r, gira, k, w=0.01):
    pts = [(cx + r * u * math.cos(gira + u * 9), cy + r * u * math.sin(gira + u * 9) * 0.8) for u in np.linspace(0.05, 1, 30)]
    return T.polyline(pts, w) * k


def _boneco(T, cx, cy, s, k):
    cab = T.ring(s * 0.3, s * 0.06, cx, cy - s * 0.6) * k * 1.2
    corpo = T.lines([(cx, cy - s * 0.3, cx, cy + s * 0.4, 1.0), (cx - s * 0.4, cy - s * 0.1, cx + s * 0.4, cy - s * 0.1, 1.0),
                     (cx, cy + s * 0.4, cx - s * 0.3, cy + s * 0.9, 1.0), (cx, cy + s * 0.4, cx + s * 0.3, cy + s * 0.9, 1.0)], s * 0.1) * k * 1.1
    return cab + corpo


def _balao(T, cx, cy, s, k):
    G, H = icone(T, poe([(math.cos(a), 1.15 * math.sin(a)) for a in np.linspace(0, TAU, 24)], cx, cy, s), k, 0.55)
    G = G + T.polyline([(cx, cy + s * 1.15), (cx + s * 0.15 * math.sin(cy * 10), cy + s * 2.0), (cx, cy + s * 2.8)], s * 0.06) * k * 1.0
    return G, H + T.gauss(cx - s * 0.35, cy - s * 0.4, s * 0.15) * k * 1.4


def _boca_dentes(T, cx, cy, s, abre, k):
    G = T.arc_band(s, s * 0.12, math.pi, TAU, 0.6 + 0.4 * abre, 0, cx, cy, 0.0) * k * 1.2
    G += T.arc_band(s, s * 0.12, 0.0, math.pi, 0.6 + 0.4 * abre, 0, cx, cy + 0.0, 0.0) * k * 1.2
    for j in range(9):
        a = math.pi + math.pi * (j + 0.5) / 9
        x = cx + s * 0.95 * math.cos(a)
        ytop = cy + s * (0.6 + 0.4 * abre) * math.sin(a)
        G += T.polys([([(x - s * 0.07, ytop), (x + s * 0.07, ytop), (x, ytop + s * 0.25)], 1.0)], 0.002) * k * 1.3
        a2 = math.pi * (j + 0.5) / 9
        x2 = cx + s * 0.95 * math.cos(a2)
        ybot = cy + s * (0.6 + 0.4 * abre) * math.sin(a2)
        G += T.polys([([(x2 - s * 0.07, ybot), (x2 + s * 0.07, ybot), (x2, ybot - s * 0.25)], 1.0)], 0.002) * k * 1.3
    return G


_MASCARA_PANICO = [(0, -1), (0.45, -0.9), (0.6, -0.45), (0.55, 0.1), (0.35, 0.7), (0.15, 1.0), (-0.15, 1.0), (-0.35, 0.7), (-0.55, 0.1),
                   (-0.6, -0.45), (-0.45, -0.9)]


def _ghostface(T, cx, cy, s, k, grito=0.0):
    G, H = icone(T, poe(_MASCARA_PANICO, cx, cy, s), k, 0.6)
    for lado in (-1, 1):
        olho = [(cx + lado * s * 0.12, cy - s * 0.45), (cx + lado * s * 0.42, cy - s * 0.5), (cx + lado * s * 0.4, cy - s * 0.15),
                (cx + lado * s * 0.15, cy - s * 0.2)]
        G = G + T.polys([(olho, 1.0)], 0.003) * k * -0.6
    boca = [(cx - s * 0.12, cy + s * 0.1), (cx + s * 0.12, cy + s * 0.1), (cx + s * 0.08, cy + s * (0.55 + 0.25 * grito)),
            (cx - s * 0.08, cy + s * (0.55 + 0.25 * grito))]
    G = G + T.polys([(boca, 1.0)], 0.003) * k * -0.6
    return G, H


def _serra(T, x, y, ang, s, k, t):
    c, sn = math.cos(ang), math.sin(ang)
    corpo = [(x - c * s * 0.35 - sn * s * 0.15, y - sn * s * 0.35 + c * s * 0.15), (x + sn * s * 0.15 - c * s * 0.35, y - c * s * 0.15 - sn * s * 0.35),
             (x + sn * s * 0.12, y - c * s * 0.12), (x - sn * s * 0.12, y + c * s * 0.12)]
    g, h = icone(T, corpo, k, 0.5)
    lam = [(x - sn * s * 0.08, y + c * s * 0.08), (x + c * s * 1.0 - sn * s * 0.06, y + sn * s * 1.0 + c * s * 0.06),
           (x + c * s * 1.05, y + sn * s * 1.05), (x + c * s * 1.0 + sn * s * 0.06, y + sn * s * 1.0 - c * s * 0.06), (x + sn * s * 0.08, y - c * s * 0.08)]
    g2, h2 = icone(T, lam, k * 1.1, 0.4)
    dentes = []
    for j in range(10):
        u = ((j / 10) + t * 6) % 1
        px, py = x + c * s * u, y + sn * s * u
        dentes.append((px + sn * s * 0.09, py - c * s * 0.09, 0.8))
        dentes.append((px - sn * s * 0.09, py + c * s * 0.09, 0.8))
    return g + g2 + T.splats(dentes, s * 0.015) * k * 1.4, h + h2


def _faiscas(T, t, a, b, cx, cy, n, seed, alcance=0.4):
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    q = np.random.default_rng(seed + int(t * 30))
    segs = []
    for _ in range(n):
        ang = q.uniform(-math.pi, 0.3)
        d = alcance * q.uniform(0.3, 1)
        x1, y1 = cx + d * math.cos(ang), cy + d * math.sin(ang)
        segs.append((cx + d * 0.7 * math.cos(ang), cy + d * 0.7 * math.sin(ang), x1, y1, 1.0))
    return T.tapered(segs, 0.008) * 1.4


def _corrente(T, x0, y0, x1, y1, k, w=0.012):
    n = max(3, int(math.hypot(x1 - x0, y1 - y0) / 0.05))
    G = 0.0
    for j in range(n):
        u = (j + 0.5) / n
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        G = G + T.ring(0.018, w * 0.5, x, y, 1.8 if j % 2 else 0.55) * k
    return G


def _gancho(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s * 0.5, y - sn * s * 0.5, x, y, 1.0)], s * 0.1) * k * 1.2
    G += T.arc_band(s * 0.3, s * 0.08, ang - math.pi * 0.2, ang + math.pi * 0.9, 1.0, 0, x, y + s * 0.3, 1.0) * k * 1.2
    return G


def _caixa(T, cx, cy, s, gira, abre, k):
    G, H = 0.0, 0.0
    c, sn = math.cos(gira), math.sin(gira)
    pts = [(cx + s * (c * x - sn * y * 0.5), cy + s * (sn * x * 0.5 + c * y * 0.85)) for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    g, h = icone(T, pts, k, 0.5)
    G, H = G + g, H + h
    G = G + T.ring(s * 0.45, s * 0.05, cx, cy, 1.0) * k * 1.2
    G = G + T.ring(s * 0.22, s * 0.04, cx, cy, 1.0) * k * 1.2
    for j in range(4):
        a = gira + TAU * j / 4
        G = G + T.lines([(cx + s * 0.22 * math.cos(a), cy + s * 0.22 * math.sin(a), cx + s * 0.45 * math.cos(a), cy + s * 0.45 * math.sin(a), 1.0)], s * 0.04) * k * 1.2
    if abre > 0:
        H = H + T.gauss(cx, cy, s * 0.4 * abre) * k * 1.5
        G = G + T.flare(cx, cy, s * 2.5 * abre, gira, 0.01) * k * 1.0
    return G, H


def _tv(T, cx, cy, s, k, t, estatica=1.0):
    G = T.polyline([(cx - s, cy - s * 0.75), (cx + s, cy - s * 0.75), (cx + s, cy + s * 0.75), (cx - s, cy + s * 0.75), (cx - s, cy - s * 0.75)], s * 0.06) * k * 1.3
    G += T.lines([(cx - s * 0.3, cy - s * 0.75, cx - s * 0.55, cy - s * 1.15, 1.0), (cx + s * 0.3, cy - s * 0.75, cx + s * 0.55, cy - s * 1.15, 1.0)], s * 0.03) * k
    q = np.random.default_rng(int(t * 40))
    pts = [(cx + q.uniform(-0.9, 0.9) * s, cy + q.uniform(-0.65, 0.65) * s, q.uniform(0.3, 1.0) * k * estatica) for _ in range(60)]
    G += T.splats(pts, s * 0.025) * 1.0
    linha = (t * 3) % 1
    G += T.lines([(cx - s * 0.9, cy - s * 0.65 + s * 1.3 * linha, cx + s * 0.9, cy - s * 0.65 + s * 1.3 * linha, 1.0)], s * 0.05) * k * estatica * 0.7
    return G


def _mao_tv(T, cx, cy, s, ang, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(cx - c * s * 1.2, cy - sn * s * 1.2, cx, cy, 1.0)], s * 0.16) * k * 1.0
    for j in range(5):
        a = ang + (j - 2) * 0.28
        L = s * (0.7 if 0 < j < 4 else 0.45)
        G += T.lines([(cx, cy, cx + L * math.cos(a), cy + L * math.sin(a), 1.0)], s * 0.07) * k * 1.2
    return G


# ------------------------------------------------------------------ Chucky

def facada_do_chucky(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.25)
    if 0 < u < 1:
        x = -0.6 + 0.85 * ease_in(u)
        y = 0.1 - 0.3 * math.sin(math.pi * u)
        G += _boneco(T, x, y, 0.24, 1.0)
        g, h = icone(T, poe(_FACA, x + 0.15, y - 0.18, 0.12, 0.8), 1.2, 0.5)
        G, H = G + g, H + h
    for j, ang in enumerate((1.2, 0.6, 1.5)):
        a0 = 0.22 + 0.09 * j
        g, h = corte(T, t, a0, a0 + 0.15, ang, 0.6, 0.05, 0.45 + 0.03 * (j - 1), 0.0)
        G, H = G + g * 1.2, H + h
        g2, h2 = clarao(T, t, a0 + 0.03, a0 + 0.16, 0.45, 0.0, 0.6, 0.9)
        G, H = G + g2, H + h2
    q = np.random.default_rng(110)
    for j in range(8):
        w = rel(t, 0.3 + 0.03 * j, 0.9)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.25, 0.35), q.uniform(-0.4, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.028), (1 - w) * 1.1)
            G, H = G + g3, H + h3
    return G * env, H * env


def _ha(T, cx, cy, s, k):
    """As letras "HA" desenhadas com traços."""
    G = T.lines([(cx - s * 0.9, cy - s * 0.5, cx - s * 0.9, cy + s * 0.5, 1.0), (cx - s * 0.4, cy - s * 0.5, cx - s * 0.4, cy + s * 0.5, 1.0),
                 (cx - s * 0.9, cy, cx - s * 0.4, cy, 1.0), (cx + s * 0.05, cy + s * 0.5, cx + s * 0.35, cy - s * 0.5, 1.0),
                 (cx + s * 0.35, cy - s * 0.5, cx + s * 0.65, cy + s * 0.5, 1.0), (cx + s * 0.17, cy + s * 0.12, cx + s * 0.53, cy + s * 0.12, 1.0)], s * 0.12)
    return G * k


def risada_do_chucky(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        s = surge(t, 0.05 + 0.12 * j, 0.25 + 0.12 * j) * (1 - rel(t, 0.75 + 0.05 * j, 0.9))
        if s > 0:
            pula = 0.04 * abs(math.sin(t * 25 + j))
            G += _ha(T, -0.6 + 0.35 * j, -0.4 - pula, 0.1 * s, 1.3)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = surge(t, 0.45 + 0.05 * i, 0.65 + 0.05 * i) * (1 - rel(t, 0.85, 1))
        if k > 0:
            G += _espiral(T, cx, -0.15, 0.13 * k, -t * 8, 1.4, 0.013)
        G += T.gauss(cx, 0.0, 0.15) * pulso(t, 0.45, 1.0) * 0.3
    return G * env, H * env


def chucky_preparo(T, t, rng):
    G, H = vazio(T)
    G += _boneco(T, -0.1, 0.05, 0.28, 1.0)
    for j in range(3):
        a = -0.6 + 0.6 * j
        x0, y0 = -0.1 + 0.2 * math.cos(a), -0.05 + 0.2 * math.sin(a)
        G += T.lines([(x0, y0, x0 - 0.1 * math.cos(a), y0 - 0.1 * math.sin(a), 1.0)], 0.007) * 1.2
        H += T.gauss(x0, y0, 0.012) * 1.5
    G += T.polys([([(0.25, 0.4), (0.33, 0.4), (0.33, 0.15), (0.25, 0.15)], 1.0)], 0.003) * 1.0
    trem = 0.01 * math.sin(t * 40) + 0.005 * math.sin(t * 27)
    g, h = icone(T, poe(CHAMA, 0.29 + trem, 0.1, 0.045), 1.2, 0.7)
    G, H = G + g, H + h
    G += T.gauss(0.29, 0.08, 0.1) * 0.35
    return G, H


def vodu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if s > 0:
        G += _boneco(T, -0.5, 0.0, 0.25 * s, 1.0)
    u = ease_in(rel(t, 0.2, 0.35), 2)
    if u > 0 and s > 0:
        y0 = -0.45 + 0.3 * u
        G += T.lines([(-0.5, y0, -0.5, y0 - 0.2, 1.0)], 0.01) * s * 1.3
        H += T.gauss(-0.5, y0 - 0.2, 0.018) * s * 1.8
        G += T.gauss(-0.5, -0.15, 0.07) * pulso(t, 0.33, 0.6) * 1.0
    w = rel(t, 0.35, 0.5)
    if 0 < w < 1:
        G += _zap(T, 111, -0.5, -0.15, -0.5 + 0.95 * w, -0.15 + 0.15 * w, 0.014, 4, 0.25) * 1.3
    g2, h2 = clarao(T, t, 0.45, 0.7, 0.45, 0.0, 1.6, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.47, 0.85, 0.05, 0.55, 0.04, 0.0)
    m = surge(t, 0.55, 0.75) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.18 * m, 0.014, 0.45, 0.0) * 1.2
        for j in range(5):
            a = t * 2 + TAU * j / 5
            G += T.lines([(0.45 + 0.1 * m * math.cos(a), 0.1 * m * math.sin(a), 0.45 + 0.2 * m * math.cos(a), 0.2 * m * math.sin(a), 1.0)], 0.008) * 1.2
    G += particulas(T, t, 0.5, 1.0, 12, 112, 0.45, 0.0, 0.15, -0.35, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Pennywise

def baloes_vermelhos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        u = rel(t, 0.05 * j, 0.6 + 0.05 * j)
        if 0 < u < 1:
            x = -0.6 + (0.9 + 0.1 * j) * ease_out(u, 1.2)
            y = -0.1 - 0.25 * math.sin(math.pi * u) + 0.05 * math.sin(u * 8 + j) - 0.08 * (j % 2)
            g, h = _balao(T, x, y, 0.1, 1.1)
            G, H = G + g, H + h
    for j in range(2):
        a0 = 0.65 + 0.08 * j
        g2, h2 = clarao(T, t, a0, a0 + 0.15, 0.4 + 0.1 * j, -0.2 + 0.08 * j, 0.5, 0.9)
        G, H = G + g2, H + h2
        G += estouro(T, t, a0, a0 + 0.3, 8, 113 + j, 0.4 + 0.1 * j, -0.2 + 0.08 * j, 0.2, 0.01)
    k = surge(t, 0.7, 0.88) * (1 - rel(t, 0.9, 1))
    if k > 0:
        G += _espiral(T, 0.45, -0.32, 0.12 * k, -t * 8, 1.3, 0.012)
    return G * env, H * env


def luzes_da_morte(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        G += _boca_dentes(T, -0.55, -0.15, 0.17 * s, 1.0, 1.0)
        for j in range(3):
            a = t * 6 + TAU * j / 3
            x, y = -0.55 + 0.07 * s * math.cos(a), -0.15 + 0.05 * s * math.sin(a)
            H += T.gauss(x, y, 0.02) * s * 2.0
            G += T.gauss(x, y, 0.045) * s * 1.0
    for j in range(4):
        u = rel(t, 0.25 + 0.08 * j, 0.7 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.1 * u, 0.025, -0.5, 0.5, 0.7, 0, -0.5, -0.1, 0.0) * (1 - u) * 1.0
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = surge(t, 0.45 + 0.05 * i, 0.65 + 0.05 * i) * (1 - rel(t, 0.85, 1))
        if k > 0 and i > 0:
            G += _espiral(T, cx, -0.2, 0.13 * k, -t * 8, 1.3, 0.012)
            for lado in (-1, 1):
                H += T.gauss(cx + lado * 0.05, -0.05, 0.012) * k * 1.6
    return G * env, H * env


def pennywise_preparo(T, t, rng):
    G, H = vazio(T)
    bal = 0.05 * math.sin(t * TAU)
    g, h = _balao(T, 0.15 + bal, -0.3, 0.16, 1.1)
    G, H = G + g, H + h
    pisca = 1.0 if (t * 1.3) % 1 < 0.9 else 0.1
    for lado in (-1, 1):
        H += T.gauss(-0.2 + lado * 0.07, 0.15, 0.018) * pisca * 2.0
        G += T.gauss(-0.2 + lado * 0.07, 0.15, 0.04) * pisca * 1.0
    return G, H


def medo_puro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.65, 0.8))
    abre = ease_out(rel(t, 0.1, 0.35), 2) * (1 - ease_in(rel(t, 0.38, 0.48), 2))
    if s > 0:
        G += _boca_dentes(T, 0.45, 0.0, 0.32 * s, abre, 1.0)
        G += T.gauss(0.45, 0.0, 0.25 * s, 0.15 * abre * s + 0.01) * 0.4
        for j in range(3):
            a = t * 8 + TAU * j / 3
            H += T.gauss(0.45 + 0.1 * math.cos(a) * abre, 0.06 * math.sin(a) * abre, 0.025) * abre * 2.0
    g2, h2 = clarao(T, t, 0.45, 0.68, 0.45, 0.0, 1.7, 1.6)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.46, 0.85, 0.05, 0.7, 0.045, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.46, 0.9, 16, 115, 0.45, 0.0, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Ghostface

def _telefone(T, cx, cy, s, k):
    pts = [(cx - s * 0.3, cy - s), (cx + s * 0.3, cy - s), (cx + s * 0.3, cy + s), (cx - s * 0.3, cy + s)]
    g, h = icone(T, pts, k, 0.4)
    g = g + T.lines([(cx, cy - s, cx, cy - s * 1.4, 1.0)], s * 0.1) * k
    return g, h


def ligacao_do_ghostface(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    vibra = 0.012 * math.sin(t * 90) * pulso(t, 0.0, 0.5)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.75, 0.9))
    if s > 0:
        g, h = _telefone(T, -0.55 + vibra, -0.05, 0.18 * s, 1.1)
        G, H = G + g, H + h
        H += T.gauss(-0.55 + vibra, -0.08, 0.02) * (0.5 + 0.5 * math.sin(t * 30)) * s * 1.5
    for j in range(5):
        u = rel(t, 0.1 + 0.08 * j, 0.5 + 0.08 * j)
        if 0 < u < 1:
            x = -0.45 + 0.9 * u
            G += T.arc_band(0.06 + 0.03 * u, 0.012, -0.8, 0.8, 1.0, 0, x, -0.05, 0.0) * (1 - rel(u, 0.7, 1)) * 1.2
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.2 * m, 0.014, 0.45, 0.0) * 1.2
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.13 * m * math.cos(a), 0.13 * m * math.sin(a), 0.45 + 0.26 * m * math.cos(a), 0.26 * m * math.sin(a), 1.0)], 0.01) * 1.3
        g2, h2 = _ghostface(T, 0.45, -0.38, 0.06 * m, 0.9)
        G, H = G + g2, H + h2
    return G * env, H * env


def facada_do_ghostface(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.6, 0.72))
    if s > 0:
        manto = [(0.55, -0.25), (0.85, -0.2), (0.95, 0.4), (0.5, 0.4)]
        g, h = icone(T, manto, s * 0.5, 0.25)
        G, H = G + g, H + h
        g2, h2 = _ghostface(T, 0.72, -0.32, 0.1 * s, 1.1)
        G, H = G + g2, H + h2
    u = ease_in(rel(t, 0.2, 0.35), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        g3, h3 = icone(T, poe(_FACA, 0.6 - 0.12 * u, -0.25 + 0.15 * u, 0.13, -2.3), k * 1.3, 0.5)
        G, H = G + g3, H + h3
    g4, h4 = corte(T, t, 0.3, 0.5, 2.3, 0.8, 0.07, 0.45, 0.0)
    G, H = G + g4 * 1.2, H + h4
    g5, h5 = clarao(T, t, 0.32, 0.55, 0.45, 0.0, 1.2, 1.3)
    G, H = G + g5, H + h5
    q = np.random.default_rng(116)
    for j in range(8):
        w = rel(t, 0.35 + 0.02 * j, 0.9)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.4, 0.1), q.uniform(-0.4, -0.1)
            g6, h6 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.03), (1 - w) * 1.1)
            G, H = G + g6, H + h6
    return G * env, H * env


def ghostface_preparo(T, t, rng):
    G, H = vazio(T)
    for m in range(4):
        y = -0.1 + 0.12 * m
        G += T.polyline([(-0.25 + 0.03 * math.sin(t * 8 + m), y), (0.0, y + 0.05), (0.25 + 0.04 * math.sin(t * 7 + m), y + 0.02)], 0.035) * 0.45
    g, h = _ghostface(T, 0.0, -0.22, 0.15, 1.2, 0.3 + 0.3 * math.sin(t * TAU))
    return G + g, H + h


def grito_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    grito = pulso(t, 0.0, 0.45)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.5, 0.62))
    if s > 0:
        g, h = _ghostface(T, -0.5, -0.2, 0.17 * s, 1.2, grito)
        G, H = G + g, H + h
    for j in range(4):
        u = rel(t, 0.05 + 0.07 * j, 0.45 + 0.07 * j)
        if 0 < u < 1:
            G += T.arc_band(0.12 + 0.9 * u, 0.035 * (1 - 0.5 * u), -0.5, 0.5, 0.75, 0, -0.45, -0.15, 0.0) * (1 - u) * 1.3
    for j, ang in enumerate((2.3, 0.8, 1.6, 2.6)):
        a0 = 0.35 + 0.08 * j
        g2, h2 = corte(T, t, a0, a0 + 0.16, ang, 0.85, 0.06, 0.45, 0.0)
        G, H = G + g2 * 1.2, H + h2
        g3, h3 = clarao(T, t, a0 + 0.03, a0 + 0.18, 0.45, 0.0, 0.8, 1.0)
        G, H = G + g3, H + h3
    G += estouro(T, t, 0.6, 0.95, 14, 117, 0.45, 0.0, 0.55, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Leatherface

def motosserra_de_leatherface(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.6)
    k = 1 - rel(t, 0.7, 0.82)
    if k > 0:
        x = -0.65 + 0.6 * u
        treme = 0.01 * math.sin(t * 80)
        g, h = _serra(T, x, 0.05 + treme, -0.15, 0.55, k * 1.1, t)
        G, H = G + g, H + h
        G += T.gauss(x - 0.12, -0.08, 0.06) * k * 0.3 * (0.5 + 0.5 * math.sin(t * 30))
    G += _faiscas(T, t, 0.3, 0.7, 0.45, 0.0, 10, 118, 0.4)
    g2, h2 = clarao(T, t, 0.3, 0.7, 0.45, 0.0, 0.9, 1.1)
    G, H = G + g2, H + h2
    q = np.random.default_rng(119)
    for j in range(14):
        w = rel(t, 0.32 + 0.025 * j, 0.95)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.2, 0.5), q.uniform(-0.5, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.03), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


def danca_da_serra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.85)
    if k > 0:
        a = t * 14
        g, h = _serra(T, 0.0 + 0.04 * math.cos(a), 0.0, a, 0.45, k * 1.1, t)
        G, H = G + g, H + h
        G += T.ring(0.5, 0.02, 0.0, 0.0, 1.5) * k * 0.7
        G += T.arc_band(0.5, 0.06, a - 1.5, a, 1.5, 0, 0.0, 0.0, 1.0) * k * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.3 + 0.1 * i
        G += _faiscas(T, t, a0, a0 + 0.3, cx, 0.1, 6, 120 + i, 0.25)
        g2, h2 = clarao(T, t, a0, a0 + 0.2, cx, 0.05, 0.4, 0.8)
        G, H = G + g2, H + h2
        q = np.random.default_rng(123 + i)
        for j in range(5):
            w = rel(t, a0 + 0.02 * j, a0 + 0.5)
            if 0 < w < 1:
                vx, vy = q.uniform(-0.2, 0.2), q.uniform(-0.35, -0.1)
                g3, h3 = cheio(T, poe(GOTA, cx + vx * w, 0.05 + vy * w + 0.8 * w * w, 0.025), (1 - w) * 1.1)
                G, H = G + g3, H + h3
    return G * env, H * env


def leatherface_preparo(T, t, rng):
    G, H = vazio(T)
    treme = 0.012 * math.sin(t * 90)
    g, h = _serra(T, -0.3, 0.15 + treme, -0.6, 0.6, 1.0, t)
    G, H = G + g, H + h
    for j in range(3):
        u = (t * 1.5 + j / 3) % 1
        G += T.gauss(-0.45 - 0.1 * u, 0.15 - 0.3 * u, 0.04 + 0.06 * u) * (1 - u) * 0.5
    return G, H


def massacre_da_serra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.35), 2)
    k = 1 - rel(t, 0.7, 0.82)
    if k > 0:
        ang = -2.0 + 1.6 * u
        g, h = _serra(T, -0.05 + 0.2 * u, 0.25, ang, 0.65, k * 1.2, t)
        G, H = G + g, H + h
    G += _faiscas(T, t, 0.32, 0.75, 0.45, 0.0, 14, 126, 0.55)
    g2, h2 = clarao(T, t, 0.32, 0.7, 0.45, 0.0, 1.7, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.34, 0.8, 0.05, 0.6, 0.04, 0.0, 1.0, 1.3)
    q = np.random.default_rng(127)
    for j in range(18):
        w = rel(t, 0.35 + 0.02 * j, 0.95)
        if 0 < w < 1:
            vx, vy = q.uniform(-0.4, 0.5), q.uniform(-0.6, -0.1)
            g3, h3 = cheio(T, poe(GOTA, 0.45 + vx * w, vy * w + 0.9 * w * w, 0.032), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


# ------------------------------------------------------------------ Pinhead

def correntes_com_ganchos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    kk = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        for j, (x0, y0) in enumerate(((cx - 0.4, -0.85), (cx + 0.4, -0.85))):
            u = ease_out(rel(t, 0.05 + 0.06 * i + 0.04 * j, 0.35 + 0.06 * i + 0.04 * j), 2)
            if u > 0 and kk > 0:
                x1, y1 = x0 + (cx - x0) * u, y0 + (-0.05 - y0) * u
                G += _corrente(T, x0, y0, x1, y1, kk * 1.2)
                G += _gancho(T, x1, y1, math.atan2(y1 - y0, x1 - x0), 0.1, kk)
        puxa = pulso(t, 0.45 + 0.05 * i, 1.0)
        if puxa > 0:
            G += T.gauss(cx, 0.0, 0.12) * puxa * 0.4
    return G * env, H * env


def _pinhead(T, cx, cy, s, k):
    G, H = icone(T, poe([(math.cos(a) * 0.75, math.sin(a)) for a in np.linspace(0, TAU, 24)], cx, cy, s), k, 0.35)
    for j in range(-2, 3):
        G = G + T.lines([(cx + j * s * 0.25, cy - s * 0.85, cx + j * s * 0.25, cy + s * 0.7, 1.0)], s * 0.025) * k * 1.0
    for j in range(-3, 4):
        G = G + T.lines([(cx - s * 0.65, cy + j * s * 0.22, cx + s * 0.65, cy + j * s * 0.22, 1.0)], s * 0.025) * k * 1.0
    pts = []
    for j in range(-2, 3):
        for m in range(-3, 4):
            if (j * s * 0.25) ** 2 / 0.56 + (m * s * 0.22) ** 2 < s * s * 0.9:
                pts.append((cx + j * s * 0.25, cy + m * s * 0.22, 1.0))
    H = H + T.splats(pts, s * 0.05) * k * 1.6
    return G, H


def dor_e_prazer(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _pinhead(T, -0.55, -0.2, 0.25 * s, 1.0)
        G, H = G + g, H + h
    u = ease_out(rel(t, 0.2, 0.4), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if u > 0 and k > 0:
        x1 = -0.4 + 0.85 * u
        G += _corrente(T, -0.4, -0.15, x1, -0.03, k * 1.2)
        G += _gancho(T, x1, -0.03, 0.15, 0.1, k)
        puxa = ease_in(rel(t, 0.45, 0.65), 2)
        G += T.gauss(0.45 - 0.08 * puxa, 0.0, 0.12) * pulso(t, 0.4, 1.0) * 0.45
    g2, h2 = clarao(T, t, 0.38, 0.6, 0.45, 0.0, 1.0, 1.1)
    G, H = G + g2, H + h2
    G += particulas(T, t, 0.45, 1.0, 10, 128, 0.45, 0.0, 0.15, -0.3, 0.012)
    return G * env, H * env


def pinhead_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _caixa(T, 0.0, 0.0, 0.26, t * TAU * 0.5, 0.3 + 0.3 * math.sin(t * TAU * 2), 1.0)
    return G + g, H + h


def caixa_de_lemarchand(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.92))
    abre = ease_out(rel(t, 0.2, 0.4), 2)
    if s > 0:
        g, h = _caixa(T, 0.0, -0.45, 0.18 * s, t * 4, abre, 1.1)
        G, H = G + g, H + h
    kk = 1 - rel(t, 0.85, 0.97)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        u = ease_out(rel(t, 0.3 + 0.05 * i, 0.55 + 0.05 * i), 2)
        if u > 0 and kk > 0:
            x1, y1 = cx * u, -0.45 + 0.4 * u
            G += _corrente(T, 0.0, -0.45, x1, y1, kk * 1.2)
            G += _gancho(T, x1, y1, math.atan2(0.4, cx + 1e-6), 0.09, kk)
        m = surge(t, 0.55 + 0.05 * i, 0.75 + 0.05 * i) * kk
        if m > 0:
            G += T.ring(0.07 * m, 0.012, cx, -0.2) * 1.3
            G += T.lines([(cx - 0.05 * m, -0.25, cx + 0.05 * m, -0.15, 1.0)], 0.012) * 1.3
    G += onda_no_chao(T, t, 0.35, 0.9, 1.0, 0.35, 1.2)
    return G * env, H * env


# ------------------------------------------------------------------ Samara

def maldicao_de_sete_dias(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        G += T.ring(0.22 * s, 0.02, 0.45, -0.05) * 1.3
        G += T.gauss(0.45, -0.05, 0.2 * s) * 0.25
        H += T.ring(0.22 * s, 0.006, 0.45, -0.05) * 1.0
    k = ease_out(rel(t, 0.3, 0.5), 2) * (1 - rel(t, 0.85, 0.97))
    if k > 0:
        sete = [(0.38, -0.15), (0.52, -0.15), (0.43, 0.08)]
        G += T.polyline(sete, 0.02) * k * 1.4
        H += T.polyline(sete, 0.007) * k * (0.7 + 0.3 * math.sin(t * 25))
        G += T.lines([(0.42, -0.04, 0.5, -0.04, 1.0)], 0.012) * k * 1.2
    G += converge(T, t, 0.0, 0.35, 10, 129, 0.45, -0.05, 0.45, 0.008)
    m = surge(t, 0.6, 0.78) * (1 - rel(t, 0.9, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.38 + 0.08 * j + 0.1 * rel(t, 0.6, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.06 * m), (0.52, y0)], 0.013) * m * 1.2
    G += particulas(T, t, 0.4, 1.0, 10, 130, 0.45, 0.0, 0.15, -0.3, 0.012)
    return G * env, H * env


def estatica_de_samara(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.75, 0.88))
    if s > 0:
        G += _tv(T, -0.55, -0.1, 0.22 * s, 1.0, t)
    for m in range(5):
        u = rel(t, 0.15 + 0.05 * m, 0.6 + 0.05 * m)
        if 0 < u < 1:
            x = -0.35 + 1.3 * ease_out(u, 1.2)
            q = np.random.default_rng(int(t * 40) + m)
            pts = [(x + q.uniform(-0.1, 0.1), q.uniform(-0.35, 0.3), q.uniform(0.3, 1.0) * (1 - rel(u, 0.7, 1))) for _ in range(25)]
            G += T.splats(pts, 0.01) * 1.0
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = surge(t, 0.5 + 0.05 * i, 0.68 + 0.05 * i) * (1 - rel(t, 0.88, 1))
        if k > 0 and i > 0:
            G += T.ring(0.07 * k, 0.012, cx, -0.3) * 1.3
            G += T.lines([(cx - 0.05 * k, -0.35, cx + 0.05 * k, -0.25, 1.0)], 0.012) * 1.3
            G += T.lines([(cx - 0.15, 0.0, cx + 0.15, 0.0, 1.0)], 0.006) * k * (0.5 + 0.5 * math.sin(t * 50 + i)) * 1.0
    return G * env, H * env


def samara_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.25, 0.04, 0.0, 0.25, 3.0) * 1.0
    G += T.lines([(-0.25, 0.25, -0.25, 0.4, 1.0), (0.25, 0.25, 0.25, 0.4, 1.0)], 0.03) * 1.0
    G += T.ring(0.12, 0.018, 0.0, -0.25, 1.0) * (0.8 + 0.4 * math.sin(t * TAU * 1.5)) * 1.2
    H += T.ring(0.12, 0.006, 0.0, -0.25, 1.0) * (0.6 + 0.3 * math.sin(t * TAU * 1.5))
    u = (t * 2) % 1
    g, h = cheio(T, poe(GOTA, 0.0, -0.1 + 0.35 * u * u, 0.025), (1 - rel(u, 0.85, 1)) * 1.1)
    G, H = G + g, H + h
    G += T.ring(0.03 + 0.15 * ((t * 2 + 0.5) % 1), 0.008, 0.0, 0.25, 3.0) * (1 - (t * 2 + 0.5) % 1) * 1.2
    return G, H


def sai_da_tv(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.75, 0.88))
    if s > 0:
        G += _tv(T, -0.15, 0.0, 0.25 * s, 1.0, t, 1.0)
    u = ease_out(rel(t, 0.25, 0.5), 2)
    k = 1 - rel(t, 0.7, 0.8)
    if u > 0 and k > 0:
        x = -0.1 + 0.5 * u
        G += _mao_tv(T, x, 0.0 + 0.03 * math.sin(t * 20), 0.18, 0.0, k * 1.1)
        cab = 0.15 * u
        G += T.gauss(-0.1 + cab, -0.05, 0.1, 0.13) * k * u * 0.35
        for m in range(6):
            G += T.lines([(-0.15 + cab + 0.02 * m - 0.05, -0.18, -0.15 + cab + 0.02 * m - 0.05 + 0.01 * math.sin(t * 10 + m), 0.1, 1.0)], 0.006) * k * u * 1.0
    g2, h2 = clarao(T, t, 0.45, 0.7, 0.45, 0.0, 1.7, 1.5)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.47, 0.85, 0.05, 0.65, 0.045, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.47, 0.9, 14, 131, 0.45, 0.0, 0.55, 0.013)
    return G * env, H * env


REGISTRO = [
    ("facada_do_chucky", facada_do_chucky, GRANDE, "Chucky · o boneco pulando com a faca", False),
    ("risada_do_chucky", risada_do_chucky, GRANDE, "Chucky · o HA HA HA e as espirais", False),
    ("chucky_preparo", chucky_preparo, MEDIA, "Chucky · o boneco de vodu e a vela (Preparo, laço)", True),
    ("vodu", vodu, GRANDE, "Chucky · o alfinete no boneco", False),
    ("baloes_vermelhos", baloes_vermelhos, GRANDE, "Pennywise · os balões flutuando", False),
    ("luzes_da_morte", luzes_da_morte, GRANDE, "Pennywise · as luzes na boca", False),
    ("pennywise_preparo", pennywise_preparo, MEDIA, "Pennywise · o balão e os olhos amarelos (Preparo, laço)", True),
    ("medo_puro", medo_puro, GRANDE, "Pennywise · a boca cheia de dentes", False),
    ("ligacao_do_ghostface", ligacao_do_ghostface, GRANDE, "Ghostface · o telefone e a mira", False),
    ("facada_do_ghostface", facada_do_ghostface, GRANDE, "Ghostface · a máscara atrás e a facada", False),
    ("ghostface_preparo", ghostface_preparo, MEDIA, "Ghostface · a máscara e o manto (Preparo, laço)", True),
    ("grito_final", grito_final, GRANDE, "Ghostface · o grito e as facadas", False),
    ("motosserra_de_leatherface", motosserra_de_leatherface, GRANDE, "Leatherface · a motosserra e as faíscas", False),
    ("danca_da_serra", danca_da_serra, GRANDE, "Leatherface · o giro com a serra", False),
    ("leatherface_preparo", leatherface_preparo, MEDIA, "Leatherface · a serra acelerando (Preparo, laço)", True),
    ("massacre_da_serra", massacre_da_serra, GRANDE, "Leatherface · a serra descendo em cheio", False),
    ("correntes_com_ganchos", correntes_com_ganchos, GRANDE, "Pinhead · as correntes e os ganchos", False),
    ("dor_e_prazer", dor_e_prazer, GRANDE, "Pinhead · o rosto de pregos e a corrente", False),
    ("pinhead_preparo", pinhead_preparo, MEDIA, "Pinhead · a caixa girando (Preparo, laço)", True),
    ("caixa_de_lemarchand", caixa_de_lemarchand, GRANDE, "Pinhead · a caixa abrindo e as correntes", False),
    ("maldicao_de_sete_dias", maldicao_de_sete_dias, GRANDE, "Samara · o anel e o sete", False),
    ("estatica_de_samara", estatica_de_samara, GRANDE, "Samara · a estática varrendo", False),
    ("samara_preparo", samara_preparo, MEDIA, "Samara · o poço e o anel de luz (Preparo, laço)", True),
    ("sai_da_tv", sai_da_tv, GRANDE, "Samara · a mão saindo da TV", False),
]
