"""Ataques básicos com animação própria, lote w: Kuririn, Kratos, Ganondorf, Snake, Mario, Sub-Zero, Liu Kang e Jin.

Golpes simples, cada um do personagem: os dois jabs rápidos do Kuririn, o soco espartano com o braço enfaixado do
Kratos, o punho do Ganondorf envolto em chamas escuras, o soco de CQC do Snake com o "!" de alerta em cima do alvo,
a luva branca do Mario com a estrelinha, o punho coberto de gelo do Sub-Zero, o soco do Liu Kang com as pontas da
faixa vermelha voando e o soco do Jin estalando com as faíscas elétricas do Tekken.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts, _nuvem
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta


def _soco(T, t, chega=0.22, recua=0.18, esc=1.1, tipo='nu', y=0.0, x0=-0.98, x1=-0.14, some=(0.46, 0.62), comp=0.44, larg=0.11, faixa=None):
    """O punho e o antebraço indo e voltando; devolve (corpo, detalhes, x do punho, visibilidade, faixa)."""
    px = _vai_e_volta(t, chega, x0, x1, recua)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, *some))
    M, d = _mao(T, px, y, esc, tipo)
    A, B = _antebraco(T, px, y, esc, comp, larg, faixa)
    return np.clip(M + A, 0, 1) * vis, d * vis, B * vis, px, vis


# ------------------------------------------------------------------ Kuririn
def dois_jabs_kuririn(T, t, rng):
    """Kuririn: dois jabs curtos e rápidos, o primeiro de leve e o segundo firme, com estalinhos de ki em cada um."""
    G, H = vazio(T)
    env = apaga(t, 0.76, 1)
    for k, (a0, y, esc, forca) in enumerate([(0.0, -0.1, 0.9, 0.6), (0.14, 0.06, 1.05, 1.0)]):
        u = ease_in(rel(t, a0, a0 + 0.12), 1.5)
        v = ease_out(rel(t, a0 + 0.14, a0 + 0.3), 2)
        if u <= 0:
            continue
        px = -0.9 + 0.76 * u - 0.3 * v
        vis = (1 - rel(t, a0 + 0.22, a0 + 0.34))
        M, d = _mao(T, px, y, esc)
        A, _ = _antebraco(T, px, y, esc, 0.4, 0.1)
        corpo = np.clip(M + A, 0, 1) * vis
        t0 = a0 + 0.12
        est = T.polys([(estrela(0.02, y, 0.24 * forca * pulso(t, t0, t0 + 0.24) + 0.01, 0.3 * k, 6, 0.4), 1.0)], 0.004) * pulso(t, t0, t0 + 0.24)
        faisca = _riscos(T, t, t0, 0.3, 6, 0.12, 0.36 * forca + 0.1, 0.02, 40 + k, -1.2, 1.2)
        G += corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + est * 1.2 + faisca * 1.1
        H += corpo * 0.3 + d * vis * 0.8 + est + faisca * 0.7
    G += _anel(T, t, 0.26, 0.66, 0.1, 0.48, 0.035, 1.2) * 1.2
    H += _anel(T, t, 0.26, 0.66, 0.1, 0.48, 0.035, 1.2) * 0.4
    return G * env, H * env


# ------------------------------------------------------------------ Kratos
def soco_espartano(T, t, rng):
    """Kratos: o braço enfaixado desce num soco pesado de cima, a fúria espartana acende em riscos em volta do
    punho e o impacto arrebenta com pedaços voando e uma onda grossa."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    u = ease_in(rel(t, 0.0, 0.26), 2.0)
    px, py = -0.95 + 0.8 * u - 0.16 * ease_out(rel(t, 0.32, 0.66), 2), -0.32 + 0.32 * u
    ang = 0.35 * (1 - u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, py, 1.2)
    A = T.polys([(_pts([(-0.08, -0.13), (-0.52, -0.14), (-0.52, 0.14), (-0.08, 0.13)], px, py, 1.2, ang), 0.8)], 0.004)
    corpo = np.clip(M + A, 0, 1) * vis
    faixas = T.zero()
    for k in range(4):
        x0 = -0.16 - 0.09 * k
        faixas += T.polyline(_pts([(x0, -0.15), (x0 - 0.06, 0.15)], px, py, 1.2, ang), 0.016)
    faixas *= vis
    # a fúria: riscos curtos que tremem em volta do punho enquanto ele desce
    furia = T.zero()
    kf = pulso(t, 0.04, 0.3) * vis
    if kf > 0:
        segs = []
        for j in range(8):
            a = TAU * j / 8 + t * 9
            r0 = 0.2 + 0.03 * math.sin(t * 50 + j)
            segs.append((px + r0 * math.cos(a), py + r0 * math.sin(a), px + (r0 + 0.12) * math.cos(a), py + (r0 + 0.12) * math.sin(a), 1.0))
        furia = T.tapered(segs, 0.03) * kf
    t0 = 0.26
    u2 = rel(t, t0, t0 + 0.6)
    pedras = T.zero()
    if 0 < u2 < 1:
        q = np.random.default_rng(77)
        polys = []
        for _ in range(9):
            a = q.uniform(-2.6, -0.5) if q.uniform() < 0.7 else q.uniform(-0.5, 0.5)
            dist = q.uniform(0.2, 0.62) * ease_out(u2, 1.8)
            cx, cy = dist * math.cos(a), dist * math.sin(a) + 0.55 * u2 * u2
            s = q.uniform(0.05, 0.085)
            polys.append((_pts([(-1, -0.6), (0.8, -0.9), (1, 0.5), (-0.3, 1)], cx, cy, s, q.uniform(0, TAU) + u2 * 5), 1 - u2))
        pedras = T.polys(polys, 0.003)
    onda = _anel(T, t, t0, t0 + 0.5, 0.12, 0.72, 0.075, 1.5)
    est = _estrela_de_contato(T, t, t0, 0.38, 8, 0.35, 0.2, 0.36)
    clarao = T.gauss(0, 0, 0.2) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.025) * 0.4 + furia * 1.1 + pedras * 1.4 + onda * 1.3 + est * 1.1 + clarao) * env
    H += (corpo * 0.3 + d * vis * 0.6 + faixas * 1.1 + furia * 0.6 + pedras * 0.8 + onda * 0.4 + est + clarao * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Ganondorf
def soco_das_trevas_ganondorf(T, t, rng):
    """Ganondorf: o punho enorme vem coberto de chamas escuras que sobem em línguas e, no impacto, a magia negra
    estoura num círculo de chamas que se contorce e some."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.24, 0.16, 1.2, 'luva', comp=0.46, larg=0.13)
    chamas = T.zero()
    if vis > 0.05:
        segs = []
        for j in range(12):
            x0 = px - 0.42 + 0.06 * j
            alto = 0.12 + 0.07 * math.sin(t * 28 + j * 2.1) + 0.05 * (j > 7)
            segs.append((x0, -0.14, x0 - 0.1, -0.14 - alto, 1.0))
            segs.append((x0 + 0.03, 0.15, x0 - 0.05, 0.15 + alto * 0.7, 0.8))
        chamas = T.tapered(segs, 0.045) * vis
    t0 = 0.24
    anel_fogo = T.zero()
    kf = pulso(t, t0, t0 + 0.5)
    if kf > 0:
        u = rel(t, t0, t0 + 0.5)
        r = 0.16 + 0.38 * ease_out(u, 2)
        segs = []
        for j in range(16):
            a = TAU * j / 16 + u * 1.5
            ri = r * (1 + 0.12 * math.sin(j * 2.3 + t * 30))
            segs.append((ri * math.cos(a), ri * math.sin(a), (ri + 0.14 * (1 - u)) * math.cos(a + 0.25), (ri + 0.14 * (1 - u)) * math.sin(a + 0.25), 1.0))
        anel_fogo = T.tapered(segs, 0.045) * kf
    nucleo = T.gauss(0, 0, 0.16) * pulso(t, t0, t0 + 0.3) * 1.6
    est = _estrela_de_contato(T, t, t0, 0.3, 7, 0.35, 0.4, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.025) * 0.4 + chamas * 1.3 + anel_fogo * 1.4 + nucleo + est) * env
    H += (corpo * 0.25 + d * 0.6 + chamas * 0.4 + anel_fogo * 0.6 + nucleo * 0.6 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Snake
def soco_cqc(T, t, rng):
    """Snake: um jab de CQC curto e seco com a luva tática e, em cima do alvo, o "!" do alerta pulando, como
    quando o guarda percebe tarde demais."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.18, 0.2, 1.05, 'luva', faixa=(0.0, 0.08))
    t0 = 0.18
    est = _estrela_de_contato(T, t, t0, 0.26, 6, 0.32, 0.1, 0.28)
    riscos = _riscos(T, t, t0, 0.3, 7, 0.18, 0.46, 0.022, 61, -1.0, 1.0)
    # o "!" pula em cima do alvo
    ka = janela(t, t0 + 0.02, t0 + 0.08) * (1 - rel(t, 0.7, 0.86))
    alerta = T.zero()
    if ka > 0:
        pulo = 0.08 * math.sin(math.pi * min(1, rel(t, t0 + 0.02, t0 + 0.2)))
        y0 = -0.5 - pulo
        haste = T.polys([([(-0.045, y0 - 0.2), (0.045, y0 - 0.2), (0.025, y0 + 0.04), (-0.025, y0 + 0.04)], 1.0)], 0.004)
        ponto = T.gauss(0, y0 + 0.11, 0.032) * 2.5
        alerta = np.clip(haste + ponto, 0, 1) * ka
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + est * 1.1 + riscos + alerta * 1.4 + T.blur(alerta, 0.03) * 0.6) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + est + riscos * 0.6 + alerta * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Mario
def soco_do_mario(T, t, rng):
    """Mario: a luva branca redondinha vem num soco de desenho, e o acerto solta a estrelinha de quatro pontas
    girando e uma moedinha que pula e some."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.22, 1.1, 'luva', faixa=(0.0, 0.1))
    t0 = 0.2
    k = pulso(t, t0, t0 + 0.4)
    est4 = T.polys([(estrela(0.05, -0.05, 0.3 * k + 0.01, t * 6, 4, 0.3), 1.0)], 0.004) * k
    u = rel(t, t0 + 0.05, t0 + 0.55)
    moeda = T.zero()
    if 0 < u < 1:
        y = -0.15 - 0.55 * math.sin(math.pi * u * 0.85)
        larg = 0.09 * abs(math.cos(u * 14)) + 0.02
        moeda = (T.gauss(0.18, y, larg, 0.11) * 2.0 - T.gauss(0.18, y, larg * 0.5, 0.06) * 1.2).clip(0, 1) * (1 - u)
    pulinho = _anel(T, t, t0, t0 + 0.35, 0.1, 0.42, 0.035, 1.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + est4 * 1.3 + moeda * 1.4 + pulinho) * env
    H += (corpo * 0.6 + (d + B) * 0.6 + est4 * 1.1 + moeda * 0.9 + pulinho * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Sub-Zero
def soco_glacial(T, t, rng):
    """Sub-Zero: o punho vem coberto de gelo (a névoa fria escorrendo e os cristais na mão) e o acerto congela o
    ponto: espinhos de gelo saem do alvo e quebram em lascas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.16, 1.1)
    nevoa = T.zero()
    if vis > 0.05:
        for j in range(5):
            nevoa += T.gauss(px - 0.15 - 0.12 * j, 0.1 + 0.03 * j + 0.03 * math.sin(t * 20 + j), 0.07 + 0.015 * j) * (1 - j / 6)
        nevoa *= vis * 0.7
    cristais = T.zero()
    if vis > 0.05:
        for (dx, dy, a) in [(0.04, -0.17, -1.9), (0.13, -0.12, -1.2), (-0.05, 0.17, 1.8)]:
            cristais += T.tapered([(px + dx, dy, px + dx + 0.1 * math.cos(a), dy + 0.1 * math.sin(a), 1.0)], 0.03)
        cristais *= vis
    t0 = 0.22
    espinhos = T.zero()
    ke = janela(t, t0, t0 + 0.06) * (1 - rel(t, t0 + 0.3, t0 + 0.45))
    if ke > 0:
        segs = []
        cresce = ease_out(rel(t, t0, t0 + 0.12), 2)
        for j in range(7):
            a = TAU * j / 7 + 0.2
            comp = (0.3 + 0.1 * (j % 2)) * cresce
            segs.append((0.05 * math.cos(a), 0.05 * math.sin(a), comp * math.cos(a), comp * math.sin(a), 1.0))
        espinhos = T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.07) * ke
    u = rel(t, t0 + 0.3, t0 + 0.75)
    lascas = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(91)
        polys = []
        for _ in range(10):
            a = q.uniform(0, TAU)
            dist = 0.15 + q.uniform(0.1, 0.4) * ease_out(u, 1.6)
            cx, cy = dist * math.cos(a), dist * math.sin(a) + 0.4 * u * u
            polys.append((_pts([(0, -1), (0.5, 0), (0, 1.2), (-0.4, 0)], cx, cy, q.uniform(0.04, 0.065), q.uniform(0, TAU)), 1 - u))
        lascas = T.polys(polys, 0.003)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 1.8
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.4 + nevoa + cristais * 1.2 + espinhos * 1.3 + lascas * 1.3 + clarao) * env
    H += (corpo * 0.35 + d * 0.7 + nevoa * 0.5 + cristais * 1.0 + espinhos * 0.9 + lascas * 0.8 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Liu Kang
def soco_da_faixa_vermelha(T, t, rng):
    """Liu Kang: um soco reto e rápido de kung fu, com as duas pontas da faixa da cabeça voando para trás no
    embalo, e o acerto com o estalo seco e os riscos de ar em leque."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.2, 1.05)
    fitas = T.zero()
    if vis > 0.05:
        for k, dy in enumerate((-0.05, 0.05)):
            pts = []
            for j in range(12):
                s = j / 11
                pts.append((px - 0.3 - 0.6 * s, -0.2 + dy + 0.1 * math.sin(s * 6 - t * 30 + k) * s + 0.12 * s))
            fitas += T.polyline(pts, 0.05 - 0.012 * k)
        fitas *= vis
    t0 = 0.2
    est = _estrela_de_contato(T, t, t0, 0.3, 8, 0.36, 0.0, 0.3)
    leque = _riscos(T, t, t0, 0.32, 9, 0.2, 0.6, 0.024, 71, -1.1, 1.1)
    onda = _anel(T, t, t0, t0 + 0.4, 0.1, 0.5, 0.035, 1.1)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + fitas * 1.3 + est * 1.1 + leque * 1.2 + onda + clarao) * env
    H += (corpo * 0.3 + d * 0.8 + fitas * 0.5 + est + leque * 0.7 + onda * 0.4 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Jin
def soco_eletrico_jin(T, t, rng):
    """Jin: o soco de caratê do Kazama, reto e travado, e no contato estala a faísca elétrica azul do Tekken:
    raios curtos e grossos saindo do punho por um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.76, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.18, 0.14, 1.1, 'luva', faixa=(0.0, 0.08))
    t0 = 0.18
    raios = T.zero()
    kr = pulso(t, t0 - 0.02, t0 + 0.42)
    if kr > 0:
        for j in range(7):
            a = -1.5 + 3.0 * j / 6
            x0, y0 = 0.08 * math.cos(a) - 0.04, 0.08 * math.sin(a)
            raios += T.polyline(jagged(np.random.default_rng(800 + j + int(t * 30)), x0, y0, x0 + 0.46 * math.cos(a), y0 + 0.46 * math.sin(a), 3, 0.2), 0.03)
        raios *= kr
    est = _estrela_de_contato(T, t, t0, 0.28, 6, 0.28, 0.0, 0.26)
    clarao = T.gauss(0, 0, 0.16) * pulso(t, t0, t0 + 0.14) * 2.4
    onda = _anel(T, t, t0, t0 + 0.38, 0.1, 0.5, 0.04, 1.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + raios * 1.5 + est + clarao + onda) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + raios * 1.2 + est * 0.9 + clarao * 1.3 + onda * 0.4) * env
    return G, H


REGISTRO = [
    ("dois_jabs_kuririn", dois_jabs_kuririn, GRANDE, "básico do Kuririn: dois jabs rápidos com estalinhos de ki", False),
    ("soco_espartano", soco_espartano, GRANDE, "básico do Kratos: o braço enfaixado, a fúria e as pedras voando", False),
    ("soco_das_trevas_ganondorf", soco_das_trevas_ganondorf, GRANDE, "básico do Ganondorf: o punho em chamas escuras e o círculo de fogo negro", False),
    ("soco_cqc", soco_cqc, GRANDE, "básico do Snake: o jab de CQC e o ! de alerta", False),
    ("soco_do_mario", soco_do_mario, GRANDE, "básico do Mario: a luva branca, a estrelinha e a moedinha", False),
    ("soco_glacial", soco_glacial, GRANDE, "básico do Sub-Zero: o punho de gelo e os espinhos que quebram", False),
    ("soco_da_faixa_vermelha", soco_da_faixa_vermelha, GRANDE, "básico do Liu Kang: o soco reto com a faixa voando", False),
    ("soco_eletrico_jin", soco_eletrico_jin, GRANDE, "básico do Jin: o soco de caratê e a faísca elétrica azul", False),
]
