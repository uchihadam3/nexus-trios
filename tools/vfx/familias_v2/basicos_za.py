"""Ataques básicos com animação própria, lote za: Kirby, Beerus, Mewtwo, Garou, Genos, Yusuke, Darkseid e Spawn.

Golpes simples, cada um do personagem: o bracinho redondo do Kirby com a estrelinha que pula, o peteleco do Beerus
(dois dedos que estalam e mandam o alvo longe), a palma do Mewtwo empurrando com ondas psíquicas, o Punho da
Correnteza do Garou (o braço que flui como água e desvia a força), o punho de aço do Genos com as aberturas de
calor brilhando, o soco de rua do Yusuke de mão enfaixada, o punho de pedra do Darkseid com o Ω vermelho e o
soco do Spawn com as correntes e o fogo verde de necroplasma.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_v import _elos
from .basicos_w import _soco
from .basicos_x import _gotas


# ------------------------------------------------------------------ Kirby
def soquinho_estrelado_kirby(T, t, rng):
    """Kirby: o bracinho redondo (sem dedos, uma bolinha) dá um soquinho rápido e, no acerto, uma estrela de cinco
    pontas pula do alvo girando e cai, com estrelinhas menores."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.18, -0.9, -0.12, 0.26)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.42, 0.58))
    bola = T.polys([(_elipse_pts(px, 0.0, 0.2, 0.17, 0.0, 20), 1.0)], 0.003)
    braco = T.polys([(_elipse_pts(px - 0.2, 0.0, 0.17, 0.11, 0.0, 16), 0.85)], 0.003)
    corpo = np.clip(bola + braco, 0, 1) * vis
    brilho = T.gauss(px + 0.03, -0.05, 0.03) * vis
    t0 = 0.18
    u = rel(t, t0, t0 + 0.65)
    estrelas = T.zero()
    if 0 < u < 1:
        y = -0.1 - 0.55 * math.sin(math.pi * u * 0.9)
        estrelas += T.polys([(estrela(0.12 + 0.25 * u, y, 0.19, u * 9, 5, 0.45), 1.0)], 0.003)
        for k in range(3):
            a = -2.4 + 0.8 * k
            dd = 0.3 * ease_out(u, 2)
            estrelas += T.polys([(estrela(dd * math.cos(a), dd * math.sin(a) + 0.3 * u * u, 0.075, u * 7, 5, 0.45), 1.0)], 0.002)
        estrelas *= (1 - u ** 3)
    pof = _anel(T, t, t0, t0 + 0.35, 0.08, 0.4, 0.04, 1.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + estrelas * 1.4 + pof) * env
    H += (corpo * 0.45 + brilho * 1.6 + estrelas * 1.1 + pof * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Beerus
def peteleco_divino(T, t, rng):
    """Beerus: a mão para na frente do alvo, o dedo do meio preso no polegar, e solta o peteleco: um estalo
    pequeno, um anel de choque desproporcional e o alvo empurrado (as linhas de ar saindo para trás)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chega = ease_out(rel(t, 0.0, 0.16), 2)
    px = -0.9 + 0.6 * chega - 0.15 * ease_out(rel(t, 0.5, 0.7), 2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.55, 0.7))
    solta = ease_out(rel(t, 0.22, 0.27), 2)
    mao = T.polys([(_elipse_pts(px, 0.0, 0.17, 0.18, 0.0, 18), 1.0)], 0.003)
    dedo = T.polyline([(px + 0.12, -0.03), (px + 0.12 + 0.1 + 0.16 * solta, -0.03 - 0.1 * (1 - solta))], 0.05)
    polegar = T.polyline([(px + 0.06, 0.07), (px + 0.2, 0.0)], 0.045)
    corpo = np.clip(mao + dedo + polegar, 0, 1) * vis
    t0 = 0.26
    estalo = T.polys([(estrela(0.0, 0.0, 0.16 * pulso(t, t0, t0 + 0.15) + 0.01, 0.3, 6, 0.3), 1.0)], 0.003) * pulso(t, t0, t0 + 0.15)
    choque = _anel(T, t, t0, t0 + 0.45, 0.06, 0.9, 0.05, 1.0)
    vento = _riscos(T, t, t0 + 0.04, 0.4, 9, 0.25, 0.85, 0.022, 17, -0.6, 0.6)
    esfera = T.gauss(0, 0, 0.12) * pulso(t, t0, t0 + 0.3) * 1.2
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + estalo * 1.3 + choque * 1.4 + vento * 1.2 + esfera) * env
    H += (corpo * 0.3 + estalo * 1.2 + choque * 0.5 + vento * 0.8 + esfera * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Mewtwo
def pancada_psiquica_mewtwo(T, t, rng):
    """Mewtwo: a mão de três dedos aberta empurra sem tocar, as ondas psíquicas saem da palma em arcos e o alvo leva
    a pancada com o ar torcendo em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = -0.62 + 0.18 * ease_out(rel(t, 0.0, 0.18), 2)
    vis = janela(t, 0.0, 0.06) * (1 - rel(t, 0.55, 0.72))
    palma = T.polys([(_elipse_pts(px, 0.0, 0.09, 0.12, 0.0, 16), 1.0)], 0.003)
    dedos = sum(T.polys([(_elipse_pts(px + 0.12, y, 0.07, 0.03, a, 12), 1.0)], 0.002) for y, a in ((-0.1, -0.4), (0.0, 0.0), (0.1, 0.4)))
    braco = T.polys([([(px - 0.08, -0.07), (px - 0.5, -0.06), (px - 0.5, 0.06), (px - 0.08, 0.07)], 0.8)], 0.003)
    corpo = np.clip(palma + dedos + braco, 0, 1) * vis
    ondas = T.zero()
    for k in range(4):
        u = rel(t, 0.08 + 0.06 * k, 0.4 + 0.06 * k)
        if 0 < u < 1:
            x = px + 0.15 + (0.0 - px) * u
            ondas += T.arc_band(0.12 + 0.18 * u, 0.025, -1.0, 1.0, 1.0, 0.0, x - 0.1, 0.0, 1.0, True) * (1 - u)
    t0 = 0.36
    torce = T.zero()
    kt = pulso(t, t0, t0 + 0.45)
    if kt > 0:
        for j in range(3):
            pts = [((0.12 + 0.12 * j) * math.cos(s + t * 8 + j), (0.12 + 0.12 * j) * math.sin(s + t * 8 + j) * 0.85) for s in np.linspace(0, 4.2, 22)]
            torce += T.polyline(pts, 0.018)
        torce *= kt
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.4 + ondas * 1.4 + torce * 1.3) * env
    H += (corpo * 0.3 + ondas * 0.7 + torce * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Garou
def punho_da_correnteza(T, t, rng):
    """Garou: o Punho da Correnteza (da escola do Bang): o braço vem em curva, fluindo, com linhas de água correndo
    em volta, e o acerto desvia num redemoinho, como a força do outro voltando contra ele."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.22), 1.4)
    px = -0.95 + 0.82 * u - 0.2 * ease_out(rel(t, 0.3, 0.62), 2)
    py = 0.18 * math.sin(math.pi * u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, py, 1.05)
    A, _ = _antebraco(T, px, py, 1.05, 0.4, 0.1)
    corpo = np.clip(M + A, 0, 1) * vis
    fluxo = T.zero()
    if vis > 0.05:
        for k in range(3):
            pts = [(px - 0.2 - 0.7 * s, py + (k - 1) * 0.08 + 0.06 * math.sin(s * 9 - t * 25 + k)) for s in np.linspace(0, 1, 18)]
            fluxo += T.polyline(pts, 0.014)
        fluxo *= vis * (1 - rel(t, 0.18, 0.32))
    t0 = 0.22
    redemoinho = T.zero()
    kr = pulso(t, t0, t0 + 0.5)
    if kr > 0:
        uu = rel(t, t0, t0 + 0.5)
        for j in range(3):
            pts = []
            for s in np.linspace(0, 1, 26):
                a = s * TAU * 1.2 + j * TAU / 3 + uu * 5
                r = 0.05 + 0.4 * s * (0.6 + 0.4 * uu)
                pts.append((r * math.cos(a), r * math.sin(a) * 0.8))
            redemoinho += T.polyline(pts, 0.02)
        redemoinho *= kr
    est = _estrela_de_contato(T, t, t0, 0.24, 7, 0.36)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + fluxo * 1.3 + redemoinho * 1.4 + est) * env
    H += (corpo * 0.3 + d * vis * 0.7 + fluxo * 0.8 + redemoinho * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Genos
def soco_de_aco_genos(T, t, rng):
    """Genos: o punho de aço em placas, com as aberturas de calor no antebraço acendendo, dá o soco e solta uma
    baforada de vapor quente para trás; o acerto é um clarão alaranjado com fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.16, 1.1, 'armadura')
    vents = T.zero()
    kv = pulso(t, 0.05, 0.4) * vis
    if kv > 0:
        for k in range(3):
            x = px - 0.24 - 0.1 * k
            vents += T.lines([(x, -0.08, x, 0.08, 1.0)], 0.022)
        vents *= kv
    vapor = T.zero()
    kp = pulso(t, 0.12, 0.45)
    if kp > 0:
        for k in range(5):
            vapor += T.gauss(px - 0.5 - 0.08 * k, -0.05 - 0.04 * k, 0.06 + 0.02 * k)
        vapor *= kp * 0.6
    t0 = 0.2
    clarao = T.gauss(0, 0, 0.2) * pulso(t, t0, t0 + 0.25) * 2.0
    fumaca = T.zero()
    vf = janela(t, t0 + 0.05, t0 + 0.1) * apaga(t, t0 + 0.3, 0.92)
    if vf > 0:
        cresce = ease_out(rel(t, t0, 0.9), 2)
        for k in range(6):
            a = -0.5 + 1.0 * k / 5 - math.pi / 2
            fumaca += T.gauss(0.2 * cresce * math.cos(a), -0.1 * cresce + 0.2 * cresce * math.sin(a), 0.07 + 0.06 * cresce)
        fumaca *= vf * 0.5
    est = _estrela_de_contato(T, t, t0, 0.3, 8, 0.36)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + vents * 1.2 + vapor + clarao + fumaca + est) * env
    H += (corpo * 0.3 + d * 0.8 + vents * 1.6 + vapor * 0.4 + clarao * 1.2 + fumaca * 0.3 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Yusuke
def soco_de_rua_yusuke(T, t, rng):
    """Yusuke: o soco de briga de rua com a mão enfaixada (as voltas da faixa no punho), um pouco torto, e o acerto
    com a poeira de quadrinho e a energia espiritual azul faiscando um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.6)
    px = -0.95 + 0.82 * u - 0.2 * ease_out(rel(t, 0.28, 0.6), 2)
    py = 0.1 * (1 - u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    M, d = _mao(T, px, py, 1.1)
    A, _ = _antebraco(T, px, py, 1.1, 0.45, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    faixa = T.zero()
    if vis > 0.05:
        for k in range(4):
            x = px - 0.04 - 0.07 * k
            faixa += T.polyline([(x + 0.03, py - 0.17), (x - 0.03, py + 0.17)], 0.012)
        faixa *= vis
    t0 = 0.2
    poeira = T.zero()
    vp = janela(t, t0, t0 + 0.05) * apaga(t, t0 + 0.25, 0.9)
    if vp > 0:
        q = np.random.default_rng(73)
        cresce = ease_out(rel(t, t0, 0.9), 2)
        for _ in range(7):
            a = q.uniform(-2.5, 2.5)
            dd = q.uniform(0.1, 0.3) * (0.5 + cresce)
            poeira += T.gauss(dd * math.cos(a), dd * math.sin(a), 0.05 + 0.04 * cresce)
        poeira *= vp * 0.6
    faiscas = _riscos(T, t, t0, 0.3, 7, 0.12, 0.42, 0.02, 41, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.32, 7, 0.3, 0.4, 0.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + poeira + faiscas * 1.3 + est * 1.1) * env
    H += (corpo * 0.3 + (d * vis + faixa) * 0.9 + poeira * 0.4 + faiscas * 1.0 + est) * env
    return G, H


# ------------------------------------------------------------------ Darkseid
def soco_omega(T, t, rng):
    """Darkseid: o punho de pedra (grande, com rachaduras) vem lento e pesado e, no acerto, o Ω vermelho do Efeito
    Ômega acende em cima do alvo por um instante, com a onda grossa saindo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vem = ease_in(rel(t, 0.0, 0.28), 2.0)
    px = -1.0 + 0.85 * vem - 0.15 * ease_out(rel(t, 0.36, 0.7), 2)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.55, 0.7))
    M, d = _mao(T, px, 0.0, 1.35)
    A, _ = _antebraco(T, px, 0.0, 1.35, 0.42, 0.12)
    corpo = np.clip(M + A, 0, 1) * vis
    rachas = T.zero()
    if vis > 0.05:
        for k in range(3):
            rachas += T.polyline(jagged(np.random.default_rng(60 + k), px - 0.4 + 0.1 * k, -0.12, px - 0.25 + 0.1 * k, 0.12, 3, 0.25), 0.01)
        rachas *= vis
    t0 = 0.28
    ko = pulso(t, t0, t0 + 0.45)
    omega = T.zero()
    if ko > 0:
        r = 0.18
        arco = [(r * math.cos(a), -0.05 + r * math.sin(a)) for a in np.linspace(math.pi * 0.72, math.pi * 2.28, 30)]
        pes = [[(-0.25, 0.15), (-0.08, 0.15)], [(0.08, 0.15), (0.25, 0.15)]]
        omega = T.polyline(arco, 0.045) + sum(T.polyline(p, 0.045) for p in pes)
        omega *= ko
    onda = _anel(T, t, t0, t0 + 0.5, 0.15, 0.72, 0.075, 1.4)
    clarao = T.gauss(0, 0, 0.2) * pulso(t, t0, t0 + 0.2) * 1.8
    G += (corpo * 1.0 + T.blur(corpo, 0.025) * 0.4 + omega * 1.5 + T.blur(omega, 0.03) * 0.6 + onda * 1.3 + clarao) * env
    H += (corpo * 0.25 + d * vis * 0.5 + rachas * 1.0 + omega * 1.1 + onda * 0.4 + clarao * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Spawn
def soco_de_necroplasma(T, t, rng):
    """Spawn: o punho vem com a corrente enrolada no braço chicoteando atrás e o fogo verde de necroplasma subindo; o
    acerto estoura em chamas verdes que sobem e somem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.16, 1.1, 'luva')
    corrente = T.zero()
    if vis > 0.05:
        balanco = math.sin(t * 20) * 0.1
        pts = [(px - 0.3 - 0.08 * j, 0.12 + 0.05 * j + balanco * (j / 7) ** 2) for j in range(8)]
        corrente = _elos(T, pts, 0.04, 0.014) * vis
    chamas = T.zero()
    if vis > 0.05:
        segs = []
        for j in range(9):
            x0 = px - 0.42 + 0.06 * j
            alto = 0.1 + 0.07 * math.sin(t * 32 + j * 1.7)
            segs.append((x0, -0.12, x0 - 0.08, -0.12 - alto, 1.0))
        chamas = T.tapered(segs, 0.045) * vis
    t0 = 0.22
    estouro = T.zero()
    ke = pulso(t, t0, t0 + 0.55)
    if ke > 0:
        uu = rel(t, t0, t0 + 0.55)
        segs = []
        for j in range(12):
            a = -math.pi * (0.05 + 0.9 * j / 11)
            r = 0.15 + 0.3 * uu
            segs.append((0.1 * math.cos(a), 0.1 * math.sin(a), r * math.cos(a), r * math.sin(a) - 0.15 * uu, 1.0))
        estouro = T.tapered(segs, 0.05) * ke
    est = _estrela_de_contato(T, t, t0, 0.26, 7, 0.36)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + corrente * 1.3 + chamas * 1.3 + estouro * 1.4 + est) * env
    H += (corpo * 0.25 + d * 0.6 + corrente * 1.0 + chamas * 0.4 + estouro * 0.6 + est * 0.9) * env
    return G, H


REGISTRO = [
    ("soquinho_estrelado_kirby", soquinho_estrelado_kirby, GRANDE, "básico do Kirby: o bracinho redondo e a estrela que pula", False),
    ("peteleco_divino", peteleco_divino, GRANDE, "básico do Beerus: o peteleco e o anel de choque desproporcional", False),
    ("pancada_psiquica_mewtwo", pancada_psiquica_mewtwo, GRANDE, "básico do Mewtwo: a palma empurrando com ondas psíquicas", False),
    ("punho_da_correnteza", punho_da_correnteza, GRANDE, "básico do Garou: o Punho da Correnteza fluindo e o redemoinho", False),
    ("soco_de_aco_genos", soco_de_aco_genos, GRANDE, "básico do Genos: punho de aço, aberturas de calor e vapor", False),
    ("soco_de_rua_yusuke", soco_de_rua_yusuke, GRANDE, "básico do Yusuke: soco de rua de mão enfaixada", False),
    ("soco_omega", soco_omega, GRANDE, "básico do Darkseid: o punho de pedra e o Ω vermelho", False),
    ("soco_de_necroplasma", soco_de_necroplasma, GRANDE, "básico do Spawn: a corrente e o fogo verde de necroplasma", False),
]
